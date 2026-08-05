"""
Parksy Transcriber — 악기 인식 후 최적 모델 라우팅 (Priority 5)
기존 basic-pitch 단일 모델 → 악기별 전문 모델 분기

라우팅:
  피아노/클래식  → piano_transcription (Qiuqiang Kong)
  보컬/콧노래   → CREPE + basic-pitch
  기타/복합     → basic-pitch (기본)

Usage:
  python3 transcriber.py audio.wav
  python3 transcriber.py audio.wav --mode piano
  python3 transcriber.py audio.wav --mode auto   (자동 감지)
"""

import os, sys, subprocess, argparse, warnings
warnings.filterwarnings('ignore')
import os as _os
_PIPELINE_DIR = _os.path.dirname(_os.path.abspath(__file__))
sys.path.insert(0, _PIPELINE_DIR)


def detect_instrument(audio_path):
    """
    librosa 스펙트럴 분석으로 악기 유형 추정
    Returns: 'piano' | 'vocal' | 'general'
    """
    try:
        import librosa, numpy as np
        y, sr = librosa.load(audio_path, sr=22050, mono=True, duration=30)

        # 스펙트럴 중심 (높을수록 밝은 음색)
        cent = librosa.feature.spectral_centroid(y=y, sr=sr)[0].mean()

        # 제로 크로싱 레이트 (높을수록 타격음/노이즈)
        zcr = librosa.feature.zero_crossing_rate(y)[0].mean()

        # 하모닉/퍼커시브 분리
        y_harm, y_perc = librosa.effects.hpss(y)
        harm_ratio = float(np.abs(y_harm).mean() / (np.abs(y).mean() + 1e-9))

        print(f"  [분석] spectral_centroid={cent:.0f}Hz  zcr={zcr:.4f}  harmonic={harm_ratio:.2f}")

        if harm_ratio > 0.7 and cent < 2000:
            return 'piano'
        elif harm_ratio > 0.6 and 1500 < cent < 4000:
            return 'vocal'
        else:
            return 'general'
    except Exception as e:
        print(f"  [분석 실패] {e} → general")
        return 'general'


def transcribe_piano(audio_path, output_mid=None):
    """piano_transcription 사용 (피아노 최적화)"""
    if output_mid is None:
        output_mid = os.path.splitext(audio_path)[0] + '_piano.mid'

    print(f"[transcriber] piano_transcription 모드")
    try:
        from piano_transcription_inference import PianoTranscription, sample_rate, load_audio
        audio, _ = load_audio(audio_path, sr=sample_rate, mono=True)
        transcriptor = PianoTranscription(device='cpu', checkpoint_path=None)
        transcriptor.transcribe(audio, output_mid)
        n = _count_notes(output_mid)
        print(f"[transcriber] → {output_mid}  ({n} notes)")
        return output_mid, n
    except Exception as e:
        print(f"[transcriber] piano_transcription 실패: {e} → basic-pitch fallback")
        return transcribe_basic_pitch(audio_path, output_mid)


def transcribe_basic_pitch(audio_path, output_mid=None):
    """basic-pitch 범용 전사"""
    if output_mid is None:
        output_mid = os.path.splitext(audio_path)[0] + '_bp.mid'

    print(f"[transcriber] basic-pitch 모드")
    from basic_pitch.inference import predict, Model
    from basic_pitch import ICASSP_2022_MODEL_PATH
    import librosa

    model = Model(ICASSP_2022_MODEL_PATH)
    _, midi_data, _ = predict(audio_path, model)
    midi_data.write(output_mid)
    n = sum(1 for inst in midi_data.instruments for _ in inst.notes)
    print(f"[transcriber] → {output_mid}  ({n} notes)")
    return output_mid, n


def transcribe_vocal(audio_path, output_mid=None):
    """
    보컬/콧노래: CREPE 피치 감지 → MIDI
    CREPE 없으면 basic-pitch fallback
    """
    if output_mid is None:
        output_mid = os.path.splitext(audio_path)[0] + '_vocal.mid'

    print(f"[transcriber] vocal/CREPE 모드")
    try:
        import crepe
        import librosa, numpy as np
        import mido

        y, sr = librosa.load(audio_path, sr=16000, mono=True)
        time, frequency, confidence, activation = crepe.predict(
            y, sr, model_capacity='medium', viterbi=True, verbose=0
        )

        # 신뢰도 낮은 구간 제거 (0.5 이하 = 묵음)
        mid = mido.MidiFile(ticks_per_beat=480)
        track = mido.MidiTrack()
        mid.tracks.append(track)
        track.append(mido.MetaMessage('set_tempo', tempo=500000, time=0))

        prev_note = None
        prev_tick = 0
        CONF_THRESHOLD = 0.5
        SEC_PER_TICK = 500000 / (480 * 1_000_000)

        for i, (t, f, c) in enumerate(zip(time, frequency, confidence)):
            if c < CONF_THRESHOLD:
                if prev_note:
                    tick = int(t / SEC_PER_TICK)
                    track.append(mido.Message('note_off', note=prev_note,
                                              velocity=0, time=tick - prev_tick))
                    prev_tick = tick
                    prev_note = None
                continue

            note = int(round(librosa.hz_to_midi(f)))
            note = max(21, min(108, note))
            tick = int(t / SEC_PER_TICK)
            vel = min(127, int(c * 100))

            if note != prev_note:
                if prev_note:
                    track.append(mido.Message('note_off', note=prev_note,
                                              velocity=0, time=tick - prev_tick))
                    prev_tick = tick
                track.append(mido.Message('note_on', note=note,
                                          velocity=vel, time=tick - prev_tick))
                prev_tick = tick
                prev_note = note

        mid.save(output_mid)
        n = _count_notes(output_mid)
        print(f"[transcriber] → {output_mid}  ({n} notes)")
        return output_mid, n

    except ImportError:
        print("[transcriber] crepe 미설치 → basic-pitch fallback")
        return transcribe_basic_pitch(audio_path, output_mid)
    except Exception as e:
        print(f"[transcriber] CREPE 실패: {e} → basic-pitch fallback")
        return transcribe_basic_pitch(audio_path, output_mid)


def _count_notes(midi_path):
    try:
        import mido
        mid = mido.MidiFile(midi_path)
        return sum(1 for t in mid.tracks for m in t
                   if m.type == 'note_on' and m.velocity > 0)
    except:
        return 0


def transcribe(audio_path, mode='auto', output_mid=None):
    """
    메인 진입점 — mode에 따라 분기
    mode: 'auto' | 'piano' | 'vocal' | 'basic'
    Returns: (midi_path, note_count)
    """
    audio_path = audio_path.replace('D:\\', '/mnt/d/').replace('\\', '/')

    if mode == 'auto':
        print(f"[transcriber] 악기 자동 감지 중...")
        mode = detect_instrument(audio_path)
        print(f"  → 감지 결과: {mode}")

    if mode == 'piano':
        return transcribe_piano(audio_path, output_mid)
    elif mode == 'vocal':
        return transcribe_vocal(audio_path, output_mid)
    else:
        return transcribe_basic_pitch(audio_path, output_mid)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('audio', help='오디오 파일')
    parser.add_argument('--mode', choices=['auto', 'piano', 'vocal', 'basic'],
                        default='auto', help='전사 모드 (default: auto)')
    parser.add_argument('--out', help='출력 MIDI 경로')
    args = parser.parse_args()

    mid, n = transcribe(args.audio, args.mode, args.out)
    print(f"완료: {mid}  ({n} notes)")
