"""
Parksy Humanizer — MIDI 인간화 엔진 (Priority 2)
로봇 같은 MIDI → 사람이 연주한 것처럼

적용 기법:
  1. 미세 타이밍 편차 (±5~20ms 가우시안)
  2. 강박 러시 / 약박 레이지 (스윙 필)
  3. 루바토 (프레이즈 끝에서 살짝 느려짐)
  4. 벨로시티 미세 편차 (같은 강도라도 미세하게 다름)
  5. 페달 시뮬레이션 (서스테인 오버랩)
"""

import mido, random, math, os, argparse
from copy import deepcopy

# ── 프리셋 ─────────────────────────────────────────────────────
PRESETS = {
    'piano': {
        'timing_std_ms':  8,    # 타이밍 흔들림 (ms)
        'rush_beats':     0.6,  # 강박 러시 (ticks, 음수=앞으로)
        'lazy_beats':     0.4,  # 약박 레이지
        'rubato_strength':0.3,  # 루바토 세기 (0~1)
        'rubato_window':  8,    # 루바토 탐지 윈도우 (음표 수)
        'vel_std':        6,    # 벨로시티 랜덤 편차
        'pedal':          True, # 서스테인 페달 시뮬
        'pedal_overlap':  0.15, # 다음 음과 겹치는 비율
    },
    'strings': {
        'timing_std_ms':  12,
        'rush_beats':     0.3,
        'lazy_beats':     0.7,
        'rubato_strength':0.5,
        'rubato_window':  6,
        'vel_std':        8,
        'pedal':          False,
        'pedal_overlap':  0,
    },
    'gentle': {
        'timing_std_ms':  4,
        'rush_beats':     0.2,
        'lazy_beats':     0.3,
        'rubato_strength':0.2,
        'rubato_window':  10,
        'vel_std':        3,
        'pedal':          True,
        'pedal_overlap':  0.10,
    },
    'expressive': {
        'timing_std_ms':  15,
        'rush_beats':     0.8,
        'lazy_beats':     0.6,
        'rubato_strength':0.6,
        'rubato_window':  5,
        'vel_std':        10,
        'pedal':          True,
        'pedal_overlap':  0.20,
    },
}


def get_tempo_tpb(mid):
    tempo = 500000
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                tempo = msg.tempo
    return tempo, mid.ticks_per_beat


def ms_to_ticks(ms, tempo, tpb):
    """밀리초 → MIDI tick 수"""
    sec_per_tick = tempo / (tpb * 1_000_000)
    return int(ms / 1000 / sec_per_tick)


def collect_events(mid):
    """전 트랙 → [(abs_tick, msg)] 합산"""
    events = []
    for track in mid.tracks:
        abs_t = 0
        for msg in track:
            abs_t += msg.time
            events.append((abs_t, msg.copy()))
    return sorted(events, key=lambda x: x[0])


def rebuild_track(events, ref_msgs):
    """이벤트 리스트 → MidiTrack"""
    track = mido.MidiTrack()
    # 원본 템포/메타 메시지 먼저
    for msg in ref_msgs:
        if msg.is_meta:
            track.append(msg.copy())

    sorted_ev = sorted(events, key=lambda x: x[0])
    prev = 0
    for abs_t, msg in sorted_ev:
        if msg.is_meta:
            continue
        delta = max(0, abs_t - prev)
        track.append(msg.copy(time=delta))
        prev = abs_t
    return track


def humanize(midi_path, preset='piano', output_path=None, seed=None):
    """
    MIDI 파일에 인간화 적용
    Returns: output_path
    """
    if seed is not None:
        random.seed(seed)

    p = PRESETS.get(preset, PRESETS['piano'])
    mid = mido.MidiFile(midi_path)
    tempo, tpb = get_tempo_tpb(mid)

    timing_ticks = ms_to_ticks(p['timing_std_ms'], tempo, tpb)

    new_mid = mido.MidiFile(ticks_per_beat=tpb)
    new_mid.type = mid.type

    # 트랙별 처리
    for track_idx, track in enumerate(mid.tracks):
        events = []
        abs_t = 0
        note_events = []

        for msg in track:
            abs_t += msg.time
            events.append((abs_t, msg.copy()))
            if msg.type == 'note_on' and msg.velocity > 0:
                note_events.append((abs_t, len(events) - 1))

        if not note_events:
            new_mid.tracks.append(deepcopy(track))
            continue

        n = len(note_events)
        modified = list(events)

        # ── 1. 루바토 탐지 (프레이즈 끝 음표 느려짐) ──────────────
        rubato_ticks = []
        window = p['rubato_window']
        for i in range(n):
            # 음표 간격 분석
            if i + 1 < n:
                gap = note_events[i+1][0] - note_events[i][0]
            else:
                gap = tpb  # 기본

            # 프레이즈 끝 탐지: 다음 음이 현저히 멀면 루바토
            if i + 1 < n:
                next_gap = note_events[min(i+2, n-1)][0] - note_events[min(i+1, n-1)][0]
                if gap > next_gap * 1.8 and p['rubato_strength'] > 0:
                    # 이 음표 뒤로 루바토 지연
                    delay = int(tpb * 0.08 * p['rubato_strength'])
                    rubato_ticks.append((i, delay))

        rubato_map = dict(rubato_ticks)

        # ── 2. 타이밍 + 루바토 + 러시/레이지 적용 ────────────────
        cumulative_offset = 0

        for i, (orig_tick, ev_idx) in enumerate(note_events):
            abs_t_orig, msg = modified[ev_idx]

            # 가우시안 타이밍 편차
            jitter = int(random.gauss(0, timing_ticks))
            jitter = max(-timing_ticks * 2, min(timing_ticks * 2, jitter))

            # 강박/약박 (비트 기준 4분음표 단위)
            beat_pos = (orig_tick % (tpb * 4)) / tpb  # 0~4 내 위치
            if beat_pos < 0.5 or (1.9 < beat_pos < 2.1):  # 강박
                jitter -= int(tpb * 0.02 * p['rush_beats'])
            else:  # 약박
                jitter += int(tpb * 0.01 * p['lazy_beats'])

            # 루바토
            rubato_delay = rubato_map.get(i, 0)
            cumulative_offset += rubato_delay

            new_tick = max(0, abs_t_orig + jitter + cumulative_offset)
            modified[ev_idx] = (new_tick, msg)

            # 3. 벨로시티 편차
            vel_jitter = int(random.gauss(0, p['vel_std']))
            new_vel = max(1, min(127, msg.velocity + vel_jitter))
            modified[ev_idx] = (new_tick, msg.copy(velocity=new_vel))

        # ── 4. 페달 시뮬레이션 ─────────────────────────────────────
        pedal_events = []
        if p['pedal']:
            overlap_ticks = int(tpb * p['pedal_overlap'])
            for i, (orig_tick, ev_idx) in enumerate(note_events):
                abs_t_mod, msg = modified[ev_idx]
                # 다음 음표 시작 직전에 페달 off → 다시 on
                if i + 1 < n:
                    next_tick = modified[note_events[i+1][1]][0]
                    pedal_off_tick = max(abs_t_mod, next_tick - overlap_ticks)
                    pedal_on_tick = next_tick

                    if i == 0:
                        pedal_events.append((abs_t_mod, mido.Message('control_change',
                            channel=msg.channel, control=64, value=127, time=0)))
                    pedal_events.append((pedal_off_tick, mido.Message('control_change',
                        channel=msg.channel, control=64, value=0, time=0)))
                    pedal_events.append((pedal_on_tick, mido.Message('control_change',
                        channel=msg.channel, control=64, value=127, time=0)))

        # ── 트랙 재조립 ─────────────────────────────────────────────
        all_events = modified + pedal_events
        all_events.sort(key=lambda x: x[0])

        new_track = mido.MidiTrack()
        meta_added = False
        prev = 0
        for abs_t, msg in all_events:
            if msg.is_meta:
                if not meta_added:
                    new_track.append(msg.copy(time=0))
                continue
            delta = max(0, abs_t - prev)
            new_track.append(msg.copy(time=delta))
            prev = abs_t

        # 템포/메타 메시지 앞에 삽입
        final_track = mido.MidiTrack()
        for msg in track:
            if msg.is_meta:
                final_track.append(msg.copy())
        for msg in new_track:
            final_track.append(msg)
        new_mid.tracks.append(final_track)

    # 저장
    if output_path is None:
        base = os.path.splitext(midi_path)[0]
        output_path = f"{base}_human.mid"

    new_mid.save(output_path)
    print(f"[humanizer] {preset} → {output_path}")
    return output_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('midi', help='입력 MIDI')
    parser.add_argument('--preset', choices=list(PRESETS.keys()), default='piano')
    parser.add_argument('--out', help='출력 경로')
    parser.add_argument('--seed', type=int, help='랜덤 시드 (재현용)')
    args = parser.parse_args()
    humanize(args.midi, args.preset, args.out, args.seed)
