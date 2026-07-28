# 03 — S21 + proot Ubuntu 실행 가능 자산

> 환경: S21 (aarch64) + Termux + proot-distro Ubuntu 26.04  
> parksy-audio 자산 중 이 폰에서 바로 돌릴 수 있는 것

---

## ✅ 즉시 실행 가능 (Python 3)

### MIDI 처리

| 스크립트 | 기능 | 의존성 |
|----------|------|--------|
| `local-agent/midi_crawler.py` | Public domain MIDI 크롤링 | `requests, bs4` |
| `local-agent/midi_sourcer.py` | MIDI 소스 검색·필터링 | `requests` |
| `local-agent/extract_midi.py` | YouTube→MIDI 추출 | `yt-dlp, pydub` |
| `local-agent/clean_midi.py` | MIDI 정리·노멀라이즈 | `mido` |
| `local-agent/trim_midi.py` | MIDI 앞뒤 자르기 | `mido` |
| `local-agent/merge_midi.py` | MIDI 트랙 병합 | `mido` |
| `local-agent/midi_info.py` | MIDI 메타정보 출력 | `mido` |

### 피아노 표현·인간화

| 스크립트 | 기능 | 의존성 |
|----------|------|--------|
| `local-agent/piano_expression.py` | 피아노 벨로서티·페달·타이밍 인간화 | `mido` |
| `local-agent/humanize_preset.py` | 인간화 프리셋 적용 | `mido` |
| `core/humanize.py` | 고급 인간화 (미세 타이밍·다이내믹) | `mido, numpy` |
| `core/emotion_profile.py` | 감정 태그 → 연주 파라미터 매핑 | `mido` |

### 렌더링 (FluidSynth 필수)

| 스크립트 | 기능 | 의존성 |
|----------|------|--------|
| `pre-season/fluidsynth_render.py` | FluidSynth 호출 래퍼 | `fluidsynth` |
| `local-agent/run_render.py` | 단일 MIDI → MP3 | `fluidsynth, ffmpeg` |
| `local-agent/run_render_h.py` | 인간화 + 렌더링 콤보 | `fluidsynth, ffmpeg, mido` |
| `local-agent/run_nocturne.py` | 야상곡 전용 렌더 | `fluidsynth, ffmpeg` |
| `engines/render_orchestral.py` | 오케스트라 렌더링 | `fluidsynth, ffmpeg` |

### 오디오 후처리

| 스크립트 | 기능 | 의존성 |
|----------|------|--------|
| `local-agent/audio_cut.py` | 오디오 구간 커팅 | `ffmpeg` |
| `local-agent/audio_check.py` | 오디오 품질 검사 | `ffmpeg` |
| `local-agent/check_norm.py` | LUFS 노멀라이즈 체크 | `ffmpeg` |
| `local-agent/make_video.py` | 오디오 + 정적 이미지 → MP4 | `ffmpeg` |
| `local-agent/gradient_mp4.py` | 그라데이션 배경 + 오디오 → MP4 | `ffmpeg` |
| `pre-season/pipeline/mastering.py` | 마스터링 (EQ·컴프레서·리미터) | `ffmpeg, numpy` |

### YouTube

| 스크립트 | 기능 | 의존성 |
|----------|------|--------|
| `tools/youtube/upload-musician.cjs` | YouTube 업로드 | `node, googleapis` |
| `tools/youtube/youtube-studio.js` | YouTube Studio 제어 | `node, playwright` |
| `tools/youtube/auth.js` | OAuth 토큰 관리 | `node, googleapis` |
| `deploy/youtube_meta.py` | YouTube 메타데이터 생성 | `python3` |
| `scripts/fetch_youtube_stats.py` | YouTube 통계 수집 | `requests` |

### 텔레그램 봇 (핵심)

| 스크립트 | 기능 | 의존성 |
|----------|------|--------|
| `local-agent/bot.py` | **메인 TG 봇** — MIDI→MP3 원격 렌더링 | `telebot, fluidsynth, ffmpeg, mido` |
| `local-agent/server.py` | 로컬 웹 서버 | `flask` |
| `local-agent/session_logger.py` | 세션 로깅 | `sqlite3` |
| `deploy/telegram_notify.py` | TG 알림 전송 | `requests` |

### S21 NPU·하드웨어

| 스크립트 | 기능 | 의존성 |
|----------|------|--------|
| `scripts/phone_npu_control.sh` | S21 NPU 발열 제어 | `bash, su` |
| `scripts/npu_worker.py` | NPU 워크로드 실행 | `python3` (삼성 NPU SDK) |

---

## 📦 설치 명령 (S21 proot Ubuntu)

```bash
# 기본 MIDI/오디오 도구
apt install -y fluidsynth fluid-soundfont-gm fluid-soundfont-gs ffmpeg lame
apt install -y python3-midiutil python3-mido python3-rtmidi
apt install -y timidity wildmidi freepats

# Python 패키지
pip install mido python-rtmidi pydub numpy requests yt-dlp

# Node.js (YouTube 업로드용)
apt install -y nodejs npm
npm install googleapis playwright

# Fluid R3 SoundFont 경로
ls /usr/share/sounds/sf2/FluidR3_GM.sf2   # 141MB
ls /usr/share/sounds/sf2/FluidR3_GS.sf2   # GS 확장
```

---

## ⚠️ 제한 사항

| 항목 | 이유 | 대안 |
|------|------|------|
| BBCSO 샘플 (`labs/bbcso/`) | 라이선스·용량 | Fluid R3 GM으로 대체 |
| Reaper DAW (`reaper-templates/`) | Windows/macOS 전용 | WaveformTrack (Linux DAW) 검토 |
| WSL2 전용 스크립트 | Windows 의존 | 경로 수정으로 대응 |
| Playwright headful | proot에서 GUI 까다로움 | headless 모드 사용 |
| SoVITS/XTTS 음성 합성 | GPU 필요, aarch64 미지원 | Kokoro TTS로 대체 (CPU only) |

---

## 🎯 우선순위 추천

1. **MIDI → MP3 렌더링** — `fluidsynth` + FluidR3, 가장 기본
2. **인간화** — `piano_expression.py` → 기계적 MIDI를 자연스럽게
3. **TG 봇** — `bot.py` → 폰에서 원격으로 렌더링 요청
4. **MIDI 크롤링** — `midi_crawler.py` → 퍼블릭 도메인 곡 수집
5. **YouTube 업로드** — `upload-musician.cjs` → 자동 송출
