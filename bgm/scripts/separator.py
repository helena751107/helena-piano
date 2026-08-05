"""
Parksy Separator — Demucs v4 소스 분리 (Priority 1)
오디오 → 보컬 / 베이스 / 드럼 / 기타(멜로디) 4트랙 분리

Usage:
  python3 separator.py audio.wav
  python3 separator.py audio.mp3 --track melody   # 멜로디 트랙만 반환
  python3 separator.py audio.wav --track vocals
"""

import subprocess, os, sys, argparse, shutil

MODELS = {
    'htdemucs':     'htdemucs',        # 기본 (빠름, 범용)
    'htdemucs_ft':  'htdemucs_ft',     # 파인튜닝 (더 정확, 느림)
    'mdx_extra':    'mdx_extra',       # MDX 베이스 (보컬 분리 특화)
}

TRACK_MAP = {
    'vocals':  'vocals',
    'bass':    'bass',
    'drums':   'drums',
    'melody':  'other',   # Demucs에서 'other' = 멜로디/기타
    'other':   'other',
}

SEP_DIR = '/tmp/parksy_separated'


def separate(audio_path, model='htdemucs', out_dir=SEP_DIR):
    """
    Demucs로 소스 분리
    Returns: dict {'vocals': path, 'bass': path, 'drums': path, 'other': path}
    """
    audio_path = audio_path.replace('D:\\', '/mnt/d/').replace('\\', '/')
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"파일 없음: {audio_path}")

    name = os.path.splitext(os.path.basename(audio_path))[0]
    os.makedirs(out_dir, exist_ok=True)

    print(f"[demucs] {model} 분리 중: {os.path.basename(audio_path)}")
    print(f"  (첫 실행 시 모델 다운로드 약 300MB — 이후 캐시됨)")

    cmd = [
        sys.executable, '-m', 'demucs',
        '--name', model,
        '--out', out_dir,
        '--mp3',          # MP3로 저장 (용량 절약)
        audio_path,
    ]

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        # WAV로 재시도
        cmd_wav = [c for c in cmd if c != '--mp3']
        r = subprocess.run(cmd_wav, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"[demucs] STDERR: {r.stderr[-500:]}")
            raise RuntimeError(f"Demucs 실패 (exit {r.returncode})")

    # 출력 경로 탐색
    model_dir = os.path.join(out_dir, model, name)
    tracks = {}
    for track_name in ['vocals', 'bass', 'drums', 'other']:
        for ext in ['mp3', 'wav']:
            p = os.path.join(model_dir, f'{track_name}.{ext}')
            if os.path.exists(p):
                tracks[track_name] = p
                sz = os.path.getsize(p) / (1024*1024)
                print(f"  [{track_name}] {p}  ({sz:.1f} MB)")
                break

    return tracks


def get_melody_track(audio_path, model='htdemucs'):
    """
    오디오에서 멜로디(other) 트랙만 추출
    Returns: melody_wav_path
    """
    tracks = separate(audio_path, model)
    melody = tracks.get('other') or tracks.get('vocals')
    if not melody:
        print("[separator] 분리 실패 — 원본 반환")
        return audio_path
    return melody


def analyze_source(audio_path):
    """
    librosa로 기본 분석: key, tempo, beat grid
    Returns: dict
    """
    import librosa, numpy as np
    print(f"[librosa] 분석 중...")
    y, sr = librosa.load(audio_path, sr=22050, mono=True)

    # 템포 + 비트
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)

    # 조성 추정 (Krumhansl-Schmuckler)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_mean = chroma.mean(axis=1)
    key_idx = int(chroma_mean.argmax())
    NOTE_NAMES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    key_name = NOTE_NAMES[key_idx]

    # RMS 에너지 (다이나믹 레인지)
    rms = librosa.feature.rms(y=y)[0]
    dyn_range = float(20 * np.log10(rms.max() / (rms.mean() + 1e-9)))

    result = {
        'tempo_bpm': round(float(tempo), 1),
        'beat_count': len(beats),
        'estimated_key': key_name,
        'duration_sec': round(len(y) / sr, 1),
        'dynamic_range_db': round(dyn_range, 1),
    }
    print(f"  BPM: {result['tempo_bpm']}  Key: {key_name}  길이: {result['duration_sec']}s")
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('audio', help='오디오 파일 (WAV/MP3)')
    parser.add_argument('--track', choices=list(TRACK_MAP.keys()),
                        help='특정 트랙만 반환')
    parser.add_argument('--model', choices=list(MODELS.keys()),
                        default='htdemucs', help='Demucs 모델')
    parser.add_argument('--analyze', action='store_true',
                        help='librosa 분석 결과 출력')
    args = parser.parse_args()

    if args.analyze:
        info = analyze_source(args.audio)
        import json
        print(json.dumps(info, indent=2, ensure_ascii=False))

    tracks = separate(args.audio, args.model)

    if args.track:
        internal = TRACK_MAP[args.track]
        path = tracks.get(internal)
        if path:
            print(f"\n[결과] {args.track}: {path}")
        else:
            print(f"[ERROR] {args.track} 트랙 없음")
    else:
        print(f"\n[결과] 전체 분리 완료:")
        for k, v in tracks.items():
            print(f"  {k}: {v}")
