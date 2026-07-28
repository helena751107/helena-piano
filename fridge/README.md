# 🧊 Fridge — 피아노 은하 냉장고

> **생성일**: 2026-07-28 · **조사자**: Claude Code (DTS 감사)  
> **대상**: `REDACTED/parksy-audio` + 28개 연계 레포  
> **목적**: helena-piano 웹진에서 꺼내 쓸 수 있는 자산 전수 조사

---

## 냉장고 안에 든 것

| 파일 | 내용 |
|------|------|
| [01-repo-list.md](01-repo-list.md) | REDACTED 소유 28개 레포 + helena751107 6개 레포 전체 목록 |
| [02-parksy-audio-inventory.md](02-parksy-audio-inventory.md) | parksy-audio 전 디렉토리·파일 인벤토리 (986MB) |
| [03-s21-capabilities.md](03-s21-capabilities.md) | S21 + proot Ubuntu에서 실행 가능한 도구·파이프 목록 |
| [04-pipeline-map.md](04-pipeline-map.md) | MIDI → 렌더링 → YouTube 송출 파이프라인 지도 |
| [05-youtube-catalog.md](05-youtube-catalog.md) | YouTube @뮤지션박씨 39개 영상 카탈로그 |

---

## 핵심 발견

1. **오디오 레포는 이미 존재**: `REDACTED/parksy-audio` — 986MB, MIDI 렌더링·인간화·마스터링·YouTube 송출 풀스택
2. **SoundFont 비교 완료**: FluidR3 vs SGM-HQ vs TOH4 vs Salamander — 백조의 호수 A/B 테스트 완료
3. **YouTube 실적 39건**: 채널 "뮤지션 박씨" (`UCun6b2HD3ekp35PhqbTfOlg`)
4. **S21 폰 구동 가능**: `local-agent/` Python 스크립트들 — MIDI 크롤러·추출·렌더링·TG 봇
5. **헬레나 피아노와 연결만 하면 완성**: parksy-audio = 생산, helena-piano = 전시

---

## 즉시 꺼내 쓸 수 있는 것

| 자산 | 위치 | helena-piano 연결 방안 |
|------|------|----------------------|
| MIDI → MP3 렌더링 | `fluidsynth` + FluidR3 | GitHub Actions / S21 proot |
| 인간화 MIDI | `piano_expression.py`, `humanize_preset.py` | 배경음악 자연스럽게 |
| YouTube 업로더 | `upload-musician.cjs` | Broadcast 구역 자동화 |
| TG 봇 | `bot.py` (36KB) | 원격 렌더링 요청 |
| NPU 제어 | `phone_npu_control.sh` | S21 발열 관리 |
| 퍼블릭 도메인 MIDI | `midi_crawler.py`, `midi_sourcer.py` | 연습용 악보 생성 |
| 감정 프로파일 | `emotion_profile.py` (33KB) | 곡 분위기 태깅 |
| 멜로디 생성기 | `melody_generator.py`, `zero_compose.py` | 단선율 연습곡 생성 |
| 화성 분석 | Mahler·Bruckner·Fauré 분석서 | 레퍼토리 학습 자료 |
