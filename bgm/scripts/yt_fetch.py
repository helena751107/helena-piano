"""
Parksy YT Fetch — YouTube 오디오 다운로더 + 클리퍼
Seal / ClipDown PC 버전 (yt-dlp + ffmpeg)

기능:
  - YouTube URL → 최고 품질 오디오 다운로드
  - 시작/끝 타임스탬프로 클립 추출
  - 검색어로 YouTube 검색 후 다운로드
  - 결과를 runner.py 파이프라인으로 자동 연결

Usage:
  # URL 다운로드
  python3 yt_fetch.py "https://youtube.com/watch?v=..."

  # 클립 추출 (1분30초 ~ 2분)
  python3 yt_fetch.py "https://youtube.com/watch?v=..." --start 1:30 --end 2:00

  # 검색 후 첫 번째 결과 다운로드
  python3 yt_fetch.py --search "brahms intermezzo op118"

  # 다운로드 후 바로 파이프라인 실행
  python3 yt_fetch.py "URL" --start 0:30 --end 1:00 --run --emotion nocturne --style faure
"""

import sys, os, subprocess, argparse, json, re, shutil, time

DOWNLOAD_DIR = '/tmp/parksy_yt_downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


# ── 타임스탬프 파싱 ─────────────────────────────────────────

def parse_time(s):
    """'1:30', '90', '1:30:00' → 초(float)"""
    if s is None:
        return None
    s = s.strip()
    parts = s.split(':')
    try:
        if len(parts) == 1:
            return float(parts[0])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    except ValueError:
        pass
    raise ValueError(f"타임스탬프 형식 오류: {s}  (예: 1:30 또는 90)")

def fmt_time(sec):
    """초 → mm:ss"""
    m = int(sec) // 60
    s = int(sec) % 60
    return f"{m}:{s:02d}"


# ── YouTube 검색 ────────────────────────────────────────────

def search_youtube(query, max_results=5):
    """검색어 → [(title, url, duration), ...] 반환"""
    print(f"[yt-dlp] 검색: {query}")
    cmd = [
        'yt-dlp',
        f'ytsearch{max_results}:{query}',
        '--print', '%(title)s|||%(webpage_url)s|||%(duration_string)s',
        '--no-download',
        '--quiet',
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    results = []
    for line in r.stdout.strip().split('\n'):
        if '|||' in line:
            parts = line.split('|||')
            if len(parts) >= 2:
                title = parts[0].strip()
                url = parts[1].strip()
                duration = parts[2].strip() if len(parts) > 2 else '?'
                results.append((title, url, duration))
    return results


def select_result(results):
    """검색 결과 출력 + 선택 (CLI 인터랙티브)"""
    if not results:
        print("[ERROR] 검색 결과 없음")
        return None

    print(f"\n검색 결과 {len(results)}개:\n")
    for i, (title, url, dur) in enumerate(results):
        print(f"  [{i+1}] {title}  ({dur})")
        print(f"       {url}")
    print()

    # 비대화형 환경 (Claude Code)에서는 첫 번째 결과 자동 선택
    if not sys.stdin.isatty():
        print("[auto] 첫 번째 결과 자동 선택")
        return results[0]

    while True:
        try:
            choice = input("선택 (1-{}), q=취소: ".format(len(results))).strip()
            if choice.lower() == 'q':
                return None
            idx = int(choice) - 1
            if 0 <= idx < len(results):
                return results[idx]
        except (ValueError, EOFError):
            return results[0]


# ── 오디오 다운로드 ─────────────────────────────────────────

def get_video_info(url):
    """영상 정보 조회"""
    cmd = ['yt-dlp', '--print', '%(title)s|||%(duration)s', '--no-download', '--quiet', url]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    line = r.stdout.strip()
    if '|||' in line:
        parts = line.split('|||')
        title = parts[0].strip()
        dur = float(parts[1].strip()) if parts[1].strip().replace('.','').isdigit() else 0
        return title, dur
    return 'unknown', 0


def download_audio(url, out_dir=DOWNLOAD_DIR):
    """
    URL → WAV 다운로드
    Returns: wav_path
    """
    title, dur = get_video_info(url)
    safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)[:60]
    out_template = os.path.join(out_dir, f'{safe_title}.%(ext)s')

    print(f"[yt-dlp] 다운로드: {title}  ({fmt_time(dur) if dur else '?'})")

    cmd = [
        'yt-dlp',
        '-f', 'bestaudio',
        '-x',
        '--audio-format', 'wav',
        '--audio-quality', '0',
        '-o', out_template,
        '--no-playlist',
        '--quiet',
        '--progress',
        url,
    ]
    r = subprocess.run(cmd, timeout=300)
    if r.returncode != 0:
        raise RuntimeError(f"yt-dlp 실패 (exit {r.returncode})")

    # 다운로드된 파일 탐색
    wav = os.path.join(out_dir, f'{safe_title}.wav')
    if os.path.exists(wav):
        sz = os.path.getsize(wav) / (1024*1024)
        print(f"[yt-dlp] → {wav}  ({sz:.1f} MB)")
        return wav

    # 확장자 다를 수 있음
    for f in os.listdir(out_dir):
        if f.startswith(safe_title[:30]):
            full = os.path.join(out_dir, f)
            print(f"[yt-dlp] → {full}")
            return full

    raise FileNotFoundError(f"다운로드 파일 못 찾음: {safe_title}")


# ── 클립 추출 ────────────────────────────────────────────────

def clip_audio(audio_path, start_sec=None, end_sec=None, out_path=None):
    """
    start_sec ~ end_sec 구간 추출 → WAV
    둘 다 None이면 원본 그대로 반환
    """
    if start_sec is None and end_sec is None:
        return audio_path

    base = os.path.splitext(audio_path)[0]
    s_tag = fmt_time(start_sec or 0).replace(':', 'm') + 's'
    e_tag = fmt_time(end_sec).replace(':', 'm') + 's' if end_sec else 'end'
    out_path = out_path or f"{base}_clip_{s_tag}-{e_tag}.wav"

    cmd = ['ffmpeg', '-y']
    if start_sec:
        cmd += ['-ss', str(start_sec)]
    cmd += ['-i', audio_path]
    if end_sec:
        duration = end_sec - (start_sec or 0)
        cmd += ['-t', str(duration)]
    cmd += ['-ar', '44100', '-ac', '1', out_path, '-loglevel', 'error']

    subprocess.run(cmd, check=True, timeout=120)
    sz = os.path.getsize(out_path) / (1024*1024)
    print(f"[clip] {fmt_time(start_sec or 0)} ~ {fmt_time(end_sec) if end_sec else 'end'} → {out_path}  ({sz:.1f} MB)")
    return out_path


# ── 파이프라인 연결 ─────────────────────────────────────────

def run_pipeline(audio_path, emotion=None, style='faure', iterations=10):
    """audio_path → runner.py → M4A"""
    import os as _os; runner = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'runner.py')
    cmd = [sys.executable, runner, audio_path, '--iterations', str(iterations)]
    if emotion:
        cmd += ['--emotion', emotion]
    if style:
        cmd += ['--mode', style]
    print(f"\n[pipeline] runner.py 시작...")
    subprocess.run(cmd)


# ── main ────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='YouTube 오디오 다운로드 + 클립 + 파이프라인 연결'
    )
    parser.add_argument('url', nargs='?', help='YouTube URL')
    parser.add_argument('--search', '-s', metavar='QUERY',
                        help='검색어로 YouTube 검색')
    parser.add_argument('--start', metavar='TIME',
                        help='클립 시작 (예: 1:30 또는 90)')
    parser.add_argument('--end', metavar='TIME',
                        help='클립 끝 (예: 2:00 또는 120)')
    parser.add_argument('--run', action='store_true',
                        help='다운로드 후 파이프라인 자동 실행')
    parser.add_argument('--emotion',
                        choices=['triumph','elegy','nocturne','epic','pastoral'],
                        help='편곡 감정 프리셋 (--run 시 사용)')
    parser.add_argument('--style',
                        choices=['bruckner','mahler','faure'],
                        default='faure',
                        help='작곡가 스타일 (--run 시 사용)')
    parser.add_argument('--list', action='store_true',
                        help='검색 결과만 출력 (다운로드 없음)')
    args = parser.parse_args()

    # ── URL 결정 ──
    url = args.url
    if args.search:
        results = search_youtube(args.search)
        if args.list:
            for i, (t, u, d) in enumerate(results):
                print(f"[{i+1}] {t}  ({d})\n    {u}")
            return
        selected = select_result(results)
        if not selected:
            return
        title, url, dur = selected
        print(f"\n선택: {title}  ({dur})")

    if not url:
        parser.print_help()
        return

    # ── 다운로드 ──
    t0 = time.time()
    wav_path = download_audio(url)

    # ── 클립 ──
    start_sec = parse_time(args.start)
    end_sec = parse_time(args.end)
    final_path = clip_audio(wav_path, start_sec, end_sec)

    elapsed = round(time.time() - t0, 1)
    print(f"\n[완료] {final_path}  ({elapsed}s)")

    # ── 파이프라인 연결 ──
    if args.run:
        run_pipeline(final_path, emotion=args.emotion, style=args.style)


if __name__ == '__main__':
    main()
