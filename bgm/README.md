# 🎹 Helena Piano — BGM Studio

> **모든 YouTube 채널의 배경음악 공급소**  
> MIDI를 넣으면 Fluid R3 GM으로 렌더링된 MP3가 나옵니다.

---

## 아키텍처

```
                      ┌─────────────────────┐
                      │   YouTube 음원       │
                      │   (Public Domain)    │
                      └─────────┬───────────┘
                                │
              ┌─────────────────▼─────────────────┐
              │  steal.py (parksy-audio)          │
              │  yt-dlp → Demucs → basic-pitch    │
              │  오디오 분리 → MIDI 추출           │
              └─────────────────┬─────────────────┘
                                │
              ┌─────────────────▼─────────────────┐
              │  bgm/midi/*.mid                   │
              │  (Public Domain MIDI 저장소)       │
              └─────────────────┬─────────────────┘
                                │
              ┌─────────────────▼─────────────────┐
              │  GitHub Actions / S21 로컬        │
              │  fluidsynth + Fluid R3 GM         │
              │  MIDI → WAV → MP3 (192kbps)       │
              └─────────────────┬─────────────────┘
                                │
              ┌─────────────────▼─────────────────┐
              │  bgm/output/*.mp3                 │
              │  GitHub Pages CDN                 │
              │  https://helena751107.github.io   │
              │  /helena-piano/bgm/output/        │
              └─────────────────┬─────────────────┘
                                │
         ┌──────────────────────┼──────────────────────┐
         │                      │                      │
         ▼                      ▼                      ▼
   @HelenaPark-e7c       @helena_phone          기타 채널
   (찬양·클래식)          (연주·브이로그)        (배경음악)
```

---

## 디렉토리 구조

```
bgm/
├── README.md           ← 이 파일
├── midi/               ← 🎼 MIDI 파일 (Public Domain)
│   └── .gitkeep
├── output/             ← 🎧 렌더링된 MP3 (GitHub Actions 자동 생성)
│   ├── .gitkeep
│   └── catalog.json    ←   MP3 URL 카탈로그 (자동 생성)
├── sources/            ← 📋 MIDI 소스 목록·라이선스
│   └── README.md
└── scripts/
    └── render.sh       ← 🖥️ S21 로컬 렌더링 스크립트
```

---

## 사용법

### GitHub Actions (자동)

1. `bgm/midi/` 에 `.mid` 파일을 넣고 push
2. GitHub Actions가 자동으로 렌더링 → `bgm/output/` 에 MP3 커밋
3. GitHub Pages URL로 바로 사용 가능:
   ```
   https://helena751107.github.io/helena-piano/bgm/output/곡제목.mp3
   ```

### S21 로컬 렌더링

```bash
# proot Ubuntu에서
apt install fluidsynth ffmpeg fluid-soundfont-gm

# 렌더링 (기본: Fluid R3 GM)
bash bgm/scripts/render.sh                    # 전체
bash bgm/scripts/render.sh moonlight.mid       # 특정 파일
bash bgm/scripts/render.sh --soundfont fluidr3 # Fluid R3 로 (기본과 동일)
```

### MIDI → MP3 한 줄

```bash
fluidsynth -ni -g 1.5 -r 44100 /usr/share/sounds/sf2/FluidR3_GM.sf2 input.mid -F output.wav
ffmpeg -i output.wav -b:a 320k output.mp3
```

---

## SoundFont 비교

| SoundFont | 피아노 음색 | 크기 | 라이선스 | 특징 |
|-----------|------------|------|----------|------|
| **Fluid R3 GM** | Steinway 샘플 | 141MB | MIT | 128악기, 범용 (fluidsynth 100% 호환) |
| ~~Salamander Grand Piano~~ | Yamaha C5 | 244MB | MIT | ⚠️ SFZ2+ARIA 확장 → fluidsynth 비호환 |
| TimGM6mb | GM 기본 | 6MB | GPL | 경량, 저품질 |

**BGM Studio 기본값: Fluid R3 GM** (피아노 특화)

> **왜 Salamander 를 안 쓰나?** Salamander Grand Piano v3 는 SFZ2 + ARIA 확장
> (keyswitch·note-selfmasking 등)으로 **Plogue sforzando 전용**이다. fluidsynth 는 ARIA
> opcode 를 지원하지 않아 로드해도 제대로 울리지 않는다. → CI(render-bgm.yml)와 로컬
> 렌더 모두 Fluid R3 GM 으로 통일했다 (2026-08-16).

---

## MIDI 소싱

### Public Domain (자유 사용)
- **IMSLP**: https://imslp.org — 클래식 악보 → MIDI
- **Mutopia Project**: https://www.mutopiaproject.org — 공개 도메인 악보+MIDI
- **Kunst der Fuge**: https://www.kunstderfuge.com — 클래식 MIDI
- **Classical Archives**: https://www.classicalarchives.com — MIDI 다수

### YouTube → MIDI 추출 (parksy-audio 파이프)
```bash
python3 steal.py "https://youtube.com/watch?v=..."
# → Demucs 소스 분리 → basic-pitch MIDI 추출 → 편곡 → 렌더링
```

### 생성 (AI 작곡)
```bash
# parksy-audio pipeline
python3 composer_v2.py --emotion "peaceful" --style "chopin" --output bgm/midi/new_piece.mid
```

---

## 다른 YouTube 채널에서 사용

```markdown
[배경음악 출처]
BGM: Helena Piano Studio
https://helena751107.github.io/helena-piano/bgm/output/{곡명}.mp3
```

---

## 라이선스

- **MIDI 파일**: 각 소스 라이선스 확인 (Public Domain / CC0 / CC-BY)
- **렌더링된 MP3**: SoundFont 라이선스에 따름
  - Fluid R3 GM: MIT → 자유 사용
- **BGM Studio 코드**: MIT
