# 04 — MIDI → 렌더링 → YouTube 송출 파이프라인 지도

> parksy-audio 파이프라인 전체 흐름 — helena-piano "Record → Broadcast" 구역과 매핑

---

## 전체 파이프라인

```
┌─────────────────────────────────────────────────────────────────┐
│                        SOURCE POOL                               │
│  ┌──────────┐  ┌───────────┐  ┌────────────┐  ┌──────────────┐ │
│  │ Public   │  │ YouTube   │  │ ABC 악보   │  │ 단선율       │ │
│  │ Domain   │  │ 추출      │  │ (abcmidi)  │  │ 멜로디 입력  │ │
│  │ MIDI     │  │ steal.py  │  │            │  │              │ │
│  └────┬─────┘  └─────┬─────┘  └─────┬──────┘  └──────┬───────┘ │
│       │              │              │                │          │
│       └──────────────┴──────────────┴────────────────┘          │
│                              │                                   │
│                    ┌─────────▼─────────┐                        │
│                    │  SOURCEPOOL       │                        │
│                    │  HARVESTER        │                        │
│                    │  (27KB)           │                        │
│                    └─────────┬─────────┘                        │
└──────────────────────────────┼──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                     COMPOSITION ENGINE                           │
│  ┌──────────┐  ┌───────────┐  ┌────────────┐  ┌──────────────┐ │
│  │ Composer │  │ Harmony   │  │ Chord      │  │ Melody       │ │
│  │ v2 (35K) │  │ Library   │  │ Engine     │  │ Generator    │ │
│  │          │  │ (42KB)    │  │ (27KB)     │  │ (18KB)       │ │
│  └────┬─────┘  └─────┬─────┘  └─────┬──────┘  └──────┬───────┘ │
│       └──────────────┴──────────────┴────────────────┘          │
│                              │                                   │
│                    ┌─────────▼─────────┐                        │
│                    │  ARRANGER (22KB)  │                        │
│                    └─────────┬─────────┘                        │
└──────────────────────────────┼──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                     HUMANIZATION                                 │
│  ┌──────────┐  ┌───────────┐  ┌────────────┐                   │
│  │ Humanize │  │ Piano     │  │ Emotion    │                   │
│  │ (26KB)   │  │ Express.  │  │ Profile    │                   │
│  │          │  │ (26KB)    │  │ (33KB)     │                   │
│  └────┬─────┘  └─────┬─────┘  └─────┬──────┘                   │
│       └──────────────┴──────────────┘                           │
│                              │                                   │
│                    ┌─────────▼─────────┐                        │
│                    │  HUMANIZED MIDI   │                        │
│                    └─────────┬─────────┘                        │
└──────────────────────────────┼──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                     RENDERING                                    │
│  ┌──────────┐  ┌───────────┐  ┌────────────┐  ┌──────────────┐ │
│  │ FluidSynth│  │ Timidity  │  │ WildMidi   │  │ Render       │ │
│  │ + FluidR3│  │ + FreePats│  │ + GUS      │  │ Orchestral   │ │
│  │ (SF2)    │  │ (SF2)     │  │ (Pat)      │  │ (16KB)       │ │
│  └────┬─────┘  └─────┬─────┘  └─────┬──────┘  └──────┬───────┘ │
│       │              │              │                │          │
│       └──────────────┴──────────────┴────────────────┘          │
│                              │                                   │
│                    ┌─────────▼─────────┐                        │
│                    │  RAW WAV (16bit)  │                        │
│                    └─────────┬─────────┘                        │
└──────────────────────────────┼──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                     POST-PRODUCTION                              │
│  ┌──────────┐  ┌───────────┐  ┌────────────┐                   │
│  │ Master   │  │ Visual    │  │ Make Video │                   │
│  │ EQ/Comp  │  │ Gradient  │  │ MP4 output │                   │
│  │ (7KB)    │  │ MP4 (3KB) │  │ (3KB)      │                   │
│  └────┬─────┘  └─────┬─────┘  └─────┬──────┘                   │
│       └──────────────┴──────────────┘                           │
│                              │                                   │
│                    ┌─────────▼─────────┐                        │
│                    │  FINAL MP4/MP3    │                        │
│                    └─────────┬─────────┘                        │
└──────────────────────────────┼──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                     DISTRIBUTION                                 │
│  ┌──────────┐  ┌───────────┐  ┌────────────┐  ┌──────────────┐ │
│  │ YouTube  │  │ GitHub    │  │ Spotify    │  │ TG Delivery  │ │
│  │ Upload   │  │ Pages     │  │ MCP        │  │ Bot          │ │
│  │ (8KB)    │  │ (web/)    │  │ (19KB)     │  │ (36KB)       │ │
│  └──────────┘  └───────────┘  └────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## helena-piano 웹진 ↔ parksy-audio 매핑

| 웹진 구역 | parksy-audio 자산 | 연결 방식 |
|-----------|-------------------|-----------|
| **01 Practice** | `midi_crawler.py` → 연습곡 MIDI 수집 | GitHub Actions 주간 크롤 |
| **02 Repertoire** | `composer_v2.py`, `melody_generator.py` | 레퍼토리 목록 자동 생성 |
| **03 Record** | `fluidsynth` + `run_render.py` | MIDI → MP3 원클릭 렌더 |
| **04 Broadcast** | `upload-musician.cjs`, `youtube-studio.js` | YouTube 자동 송출 |
| **Session card** | `session_logger.py` | 연습 세션 로깅 |
| **Rhythm** | `emotion_profile.py` → 감정 태깅 | 곡 분위기 분류 |

---

## GitHub Actions 워크플로우 구상

```yaml
# .github/workflows/render-piano.yml
name: Render Piano BGM
on:
  push:
    paths: ['midi/*.mid']
  workflow_dispatch:

jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install fluidsynth + soundfont
        run: sudo apt-get install -y fluidsynth fluid-soundfont-gm ffmpeg
      - name: Render MIDI → MP3
        run: |
          for midi in midi/*.mid; do
            name=$(basename "$midi" .mid)
            fluidsynth -ni /usr/share/sounds/sf2/FluidR3_GM.sf2 "$midi" -F "output/$name.wav"
            ffmpeg -i "output/$name.wav" -codec:a libmp3lame -b:a 192k "output/$name.mp3"
          done
      - uses: actions/upload-artifact@v4
        with:
          name: piano-bgm
          path: output/*.mp3
```
