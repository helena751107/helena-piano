# 02 — `parksy-audio` 완전 인벤토리

> **레포**: `REDACTED/parksy-audio` · **크기**: 986MB · **언어**: HTML (web frontend) + Python  
> **설명**: Audio experiments, narration, and sound assets for Parksy's production and broadcasting workflow.  
> **Pages**: `https://REDACTED.github.io/parksy-audio`

---

## 디렉토리 구조 전체

```
parksy-audio/ (986MB)
├── README.md                          — 레포 소개
├── CLAUDE.md                          — AI 에이전트 규칙
├── SEASON.md                          — 시즌 기획 (15KB)
├── DIVISION-MAP.json                  — 가상 조직도 (7.6KB)
├── DIVISION-README.md                 — 조직 설명 (5.3KB)
├── repo.manifest.json                 — 레포 매니페스트
├── status.json                        — 상태
├── run.py                             — 메인 실행기 (14KB)
├── requirements.txt                   — Python 의존성
├── .pre-commit-config.yaml
├── .gitignore
├── .env.example
├── youtube-setup.json                 — YouTube 채널 설정
│
├── 📁 assets/                         — 웹 에셋 (현재 manifest만)
│   └── manifest.json                  —   AIVA 워크플로우용 BGM/SFX/Intro/Loops 카탈로그
│
├── 🧪 test-samples/
│   ├── sample.mp3                     — 8.9MB 테스트 오디오
│   ├── output.mid                     — 28KB 렌더링 출력
│   └── cli-output.mid                 — 28KB CLI 출력
│
├── 🎬 pre-season/                     — 🔥 메인 작업 디렉토리
│   ├── 🎵 렌더링 결과물
│   │   ├── swan_lake_original.mid    — 9KB 백조의 호수 원본
│   │   ├── swan_lake_fluidsynth.mp4  — 7.9MB FluidSynth 기본
│   │   ├── swan_lake_fluidr3.mp4     — 10.3MB Fluid R3 SoundFont
│   │   ├── swan_lake_sgm_hq.mp4      — 10.2MB SGM-HQ SoundFont
│   │   ├── swan_lake_toh.mp4         — 10.3MB TOH SoundFont
│   │   ├── swan_lake_toh4.mp4        — 10.3MB TOH4 SoundFont
│   │   ├── carnival_swan_toh4.mp4    — 5.3MB 사육제 + TOH4
│   │   └── carnival_wind.mp4         — 5.3MB 사육제 Wind
│   │
│   ├── 🔧 파이프라인 (pipeline/)
│   │   ├── composer.py               — 12KB 작곡
│   │   ├── composer_v2.py            — 35KB 작곡 v2
│   │   ├── harmony_library.py        — 42KB 화성 라이브러리
│   │   ├── overture_presets.py       — 30KB 서곡 프리셋
│   │   ├── chord_engine.py           — 27KB 코드 엔진
│   │   ├── melody_generator.py       — 18KB 멜로디 생성
│   │   ├── arranger.py               — 22KB 편곡
│   │   ├── humanizer.py              — 9KB 인간화
│   │   ├── mastering.py              — 7KB 마스터링
│   │   ├── optimizer.py              — 15KB 최적화
│   │   ├── score_engine.py           — 8KB 악보 엔진
│   │   ├── separator.py              — 5KB 음원 분리
│   │   ├── transcriber.py            — 7KB 채보
│   │   ├── voice_synthesizer.py      — 8KB 음성 합성
│   │   ├── singing_pipeline.py       — 19KB 노래 파이프라인
│   │   ├── zero_compose.py           — 13KB 제로 컴포즈
│   │   ├── runner.py                 — 15KB 실행기
│   │   ├── make_shorts.py            — 5KB 쇼츠 제작
│   │   └── yt_fetch.py              — 10KB YouTube 가져오기
│   │
│   ├── 🧠 분석 문서
│   │   ├── mahler-harmony-analysis.md    — 22KB 말러 화성 분석
│   │   ├── bruckner-harmony-analysis.md  — 17KB 브루크너 화성 분석
│   │   └── faure-harmony-analysis.md     — 16KB 포레 화성 분석
│   │
│   ├── 🎹 연습·세션
│   │   ├── ParksyLog_20260326_202357.md  — 56KB 세션 로그
│   │   ├── ParksyLog_20260328_235225.md  — 114KB 세션 로그
│   │   ├── CLAUDE.md                     — 85KB AI 워크플로우
│   │   ├── REAPER_DAW_CLAUDE_MD.md       — 4KB Reaper DAW 연동
│   │   ├── ph_mission_brief.md           — 7KB 미션 브리핑
│   │   ├── ph_push_instruct.md           — 5KB 푸시 지침
│   │   └── index.html                    — 33KB 웹 인터페이스
│   │
│   ├── 🎛️ MCP 서버
│   │   ├── parksy_compose_mcp.py     — 14KB 작곡 MCP
│   │   ├── parksy_spotify_mcp.py     — 19KB Spotify MCP
│   │   ├── mcp_music/                — 음악 MCP
│   │   ├── mcp_parksy/               — Parksy MCP
│   │   └── mcp_voice/               — 음성 MCP
│   │
│   ├── 📦 기타
│   │   ├── overtures_master_100.xlsx — 3개 파일, 각 22KB
│   │   ├── package.json
│   │   ├── requirements.txt
│   │   ├── install.sh                — 5KB 설치 스크립트
│   │   ├── start_wsl2_mcp.sh         — WSL2 MCP 시작
│   │   ├── fluidsynth_render.py      — 2KB FluidSynth 렌더 예제
│   │   ├── process_queue.py          — 16KB 큐 처리
│   │   ├── file_00000000...png       — 1MB 스크린샷
│   │   ├── queue/                    — 작업 큐
│   │   ├── releases/                 — 릴리즈
│   │   ├── recipes/                  — 레시피
│   │   ├── spotify/                  — Spotify 연동
│   │   ├── server/                   — 서버
│   │   ├── session-logs/             — 세션 로그
│   │   ├── instructions/             — 지침
│   │   ├── local-engine/             — 로컬 엔진
│   │   ├── lyria3/                   — Lyria3
│   │   ├── gcp_training/             — GCP 훈련
│   │   ├── app/                      — 앱
│   │   ├── _queue/                   — 대기열
│   │   ├── xtract/                   — 추출 도구
│   │   └── 00_TRUTH/                 — 진실
│   │
│   └── 🧪 작업 디렉토리
│       ├── labs/
│       │   ├── bbcso/                — BBC Symphony Orchestra
│       │   └── slot_strategy/        — 슬롯 전략
│       └── 강희철_박사/
│           └── 01_ESG_뮤지션OS_사업제안_20260705.md
│
├── 🎛️ core/                          — 코어 라이브러리
│   ├── pipeline.py                   — 47KB ⭐ 메인 파이프라인
│   ├── emotion_profile.py            — 33KB 감정 프로파일
│   ├── humanize.py                   — 26KB 인간화
│   ├── optimizer.py                  — 18KB 최적화
│   ├── bassoon.py                    — 11KB 바순
│   ├── gate.py                       — 11KB 게이트
│   ├── visual.py                     — 9KB 시각화
│   ├── legal.py                      — 6KB 저작권 검증
│   ├── render_base.py                — 2KB 렌더링 기본
│   └── __init__.py
│
├── 🎛️ engines/                       — 엔진
│   ├── sourcepool_harvester.py       — 27KB 소스풀 수확기
│   ├── render_orchestral.py          — 16KB 오케스트라 렌더링
│   ├── score_engine.py               — 8KB 악보 엔진
│   ├── kdf_miner.py                  — 7KB KDF 마이너
│   ├── sourcepool/                   — 소스풀
│   └── __init__.py
│
├── 🤖 local-agent/                   — 🔥 S21 폰 실행 에이전트
│   ├── bot.py                        — 36KB ⭐ 텔레그램 봇 (메인)
│   ├── bot.py.bak                    — 10KB 백업
│   ├── midi_crawler.py               — 24KB MIDI 크롤러
│   ├── midi_sourcer.py               — 13KB MIDI 소스 검색
│   ├── piano_expression.py           — 26KB 피아노 표현
│   ├── humanize_preset.py            — 8KB 인간화 프리셋
│   ├── extract_midi.py               — 3KB MIDI 추출
│   ├── clean_midi.py                 — 3KB MIDI 정리
│   ├── trim_midi.py                  — 2KB MIDI 트리밍
│   ├── merge_midi.py                 — 1KB MIDI 병합
│   ├── midi_info.py                  — 461B MIDI 정보
│   ├── make_video.py                 — 3KB 비디오 제작
│   ├── gradient_mp4.py               — 3KB 그라데이션 MP4
│   ├── audio_cut.py                  — 3KB 오디오 커팅
│   ├── audio_check.py                — 2KB 오디오 검사
│   ├── check_norm.py                 — 868B 노멀라이즈 체크
│   ├── run_render.py                 — 1KB 렌더 실행
│   ├── run_render_h.py               — 1KB 인간화 렌더
│   ├── run_nocturne.py               — 752B 야상곡 렌더
│   ├── run_fire_asmr.py              — 25KB Fire ASMR 실행
│   ├── demo_bossa.py                 — 4KB 보사노바 데모
│   ├── demo_tchaikovsky.py           — 2KB 차이콥스키 데모
│   ├── steal.py                      — 10KB (YouTube→MIDI)
│   ├── server.py                     — 6KB 웹 서버
│   ├── session_logger.py             — 6KB 세션 로거
│   ├── mcp_healthcheck.sh            — 7KB MCP 상태 확인
│   ├── beta_onboard.sh               — 4KB 베타 온보딩
│   ├── start_bot.sh                  — 755B 봇 시작
│   ├── config.py                     — 3KB 설정
│   ├── telegram_config.json          — 295B TG 설정
│   ├── optimal_config.json           — 924B 최적 설정
│   ├── requirements.txt
│   ├── README.md
│   ├── .last_update_id
│   ├── .gitignore
│   ├── outputs/                      — 출력물
│   ├── sourcepool/                   — 소스풀
│   ├── scripts/                      — 보조 스크립트
│   ├── session-logs/                 — 세션 로그
│   ├── reaper-templates/             — Reaper DAW 템플릿
│   └── 테스트 파일들
│       ├── test_api.py
│       ├── test_full.py
│       ├── test_merge.py
│       ├── test_phase2.py
│       ├── test_phase2_full.py
│       ├── test_phase2_run.py
│       ├── test_render.py
│       ├── test_render_quick.py
│       ├── test_req.json
│       └── test_video.py
│
├── 🔧 scripts/                       — 자동화 스크립트
│   ├── auto_chain.py                 — 10KB 자동 연쇄
│   ├── batch_chain.py                — 13KB 배치 연쇄
│   ├── batch_render_all.py           — 5KB 전체 배치 렌더
│   ├── batch_emotion.py              — 4KB 감정 배치
│   ├── batch_thumbnails.py           — 2KB 썸네일 배치
│   ├── humanize-midi.py              — 15KB MIDI 인간화
│   ├── singing_pipeline.py           — 25KB 노래 파이프라인
│   ├── pro_score.py                  — 12KB 프로 악보
│   ├── kokoro_engine.py              — 5KB Kokoro TTS
│   ├── tts_engine.py                 — 8KB TTS 엔진
│   ├── sovits_worker.py              — 7KB SoVITS 음성
│   ├── xtts_worker.py                — 11KB XTTS 음성
│   ├── npu_worker.py                 — 18KB NPU 워커
│   ├── phone_npu_control.sh          — 3KB S21 NPU 제어
│   ├── fetch_youtube_stats.py        — 7KB YT 통계
│   ├── scan_videos.py                — 4KB 비디오 스캔
│   ├── generate_analytics.py         — 11KB 분석 생성
│   ├── generate_composer_index.py    — 8KB 작곡가 색인
│   ├── generate_gallery.py           — 15KB 갤러리 생성
│   ├── gen_thumbnail.py              — 7KB 썸네일 생성
│   ├── connect_sourcepool.py         — 3KB 소스풀 연결
│   ├── update-manifest.js            — 2KB 매니페스트 갱신
│   ├── update_composers.py           — 8KB 작곡가 갱신
│   ├── send_batch_report.py          — 3KB 배치 보고
│   ├── check_upload_readiness.sh     — 5KB 업로드 준비 체크
│   ├── auto_commit.sh                — 1KB 자동 커밋
│   ├── midi-analysis-prompt.md       — 4KB MIDI 분석 프롬프트
│   └── piano-checklist.md            — 3KB 피아노 체크리스트
│
├── 🚀 deploy/                        — 배포
│   ├── youtube_analytics.py          — 8KB YT 분석
│   ├── youtube_meta.py               — 7KB YT 메타데이터
│   ├── telegram_notify.py            — 4KB TG 알림
│   └── __init__.py
│
├── 🛠️ tools/                         — 도구
│   ├── apply_lut.py                  — 2KB LUT 적용
│   ├── deploy-musician.sh            — 9KB 뮤지션 배포
│   ├── fountain_to_shotlist.py       — 2KB 파운틴→샷리스트
│   ├── gdrive-sync.sh                — 4KB Google Drive 동기화
│   ├── sync-lyria3-to-image.sh       — 3KB Lyria3→이미지 동기화
│   ├── update-musician-manifest.js   — 5KB 뮤지션 매니페스트
│   └── youtube/
│       ├── upload-musician.cjs       — 8KB ⭐ YouTube 업로드
│       ├── youtube-studio.js         — 13KB YouTube Studio 제어
│       ├── auth.js                   — 5KB OAuth 인증
│       ├── musician-config.json      — 1KB 설정
│       ├── UPLOAD-HOWTO.md           — 4KB 업로드 가이드
│       ├── update_box_catalog.py     — 2KB 카탈로그 갱신
│       └── uploads/                  — 업로드 대기열
│
├── 🌐 web/                           — 웹 프론트엔드
│   ├── index.html                    — 34KB 메인 페이지
│   ├── 404.html                      — 2KB
│   ├── manifest.json                 — 2KB
│   ├── sw.js                         — 2KB 서비스 워커
│   ├── app/                          — 앱
│   ├── assets/                       — 웹 에셋
│   ├── data/                         — 웹 데이터
│   └── outputs/                      — 웹 출력
│
├── 📚 docs/                          — 문서 (27종)
│   ├── 00-COPYRIGHT-AXIOMS.md        — 13KB 저작권 공리
│   ├── 01-ROLE-ARCHITECTURE.md       — 2KB 역할 구조
│   ├── 02-MUSIC-INDUSTRY-THESIS.md   — 7KB 음악산업 논문
│   ├── 03-SOURCEPOOL.md              — 5KB 소스풀
│   ├── 04-COMMUNITY-RESEARCH-BRIDGE.md — 5KB 커뮤니티 리서치
│   ├── 05-FRAMEWORK-JUSTIFICATION.md — 4KB 프레임워크 정당화
│   ├── 06-ECOSYSTEM-MOAT-REPORT.md   — 5KB 생태계 해자
│   ├── 07-CYBORG-ARCHITECTURE.md     — 5KB 사이보그 건축
│   ├── 08-COMMUNITY-RESEARCH-VALIDATION.md — 8KB 커뮤니티 검증
│   ├── 09-BRAND-MANIFESTO.md         — 15KB 브랜드 선언
│   ├── 10-SLOT-STRATEGY.md           — 10KB 슬롯 전략
│   ├── 11-LITERATURE-FILM-AI-APPRECIATION.md — 22KB 문학·영화·AI
│   ├── 12-ART-PHILOSOPHY-ENDING-CREDITS.md — 17KB 예술철학
│   ├── 13-FILM-KIT-INVENTORY.md      — 19KB 영화 키트
│   ├── 14-PD-TRIO-SELECTION-WHITEPAPER.md — 7KB PD 트리오
│   ├── 15-SHAMAN-TRIO-SELECTION.md   — 8KB 샤먼 트리오
│   ├── 16-DEBUSSY-TRANSLATOR-ENGINE.md — 11KB 드뷔시 번역기
│   ├── 17-PLUG-ARCHITECTURE.md       — 9KB 플러그 건축
│   ├── 18-THOUGHT-PROCESS-2026-07-12.md — 17KB 사고 과정
│   ├── 19-COMPLETE-ARCHITECTURE-REFERENCE.md — 17KB 전체 건축 참조
│   ├── 20-INVENTORY-REPORT-2026-07-12.md — 6KB 인벤토리 보고서
│   ├── 21-SEVEN-PERSON-LINEUP-VERIFICATION.md — 8KB 7인 라인업
│   ├── 22-VIRTUAL-DIVISION-ORGANIZATION.md — 8KB 가상 부서 조직
│   ├── 23-EXECUTION-PLAN-2026-07-12.md — 3KB 실행 계획
│   ├── 24-DIVISION-DIAGRAM.md        — 4KB 부서 다이어그램
│   ├── 25-LANDING-PAGE-SPEC.md       — 5KB 랜딩 페이지 스펙
│   ├── 26-WEB-STRUCTURE-SYNC.md      — 4KB 웹 구조 동기화
│   ├── 27-PERSONA-DEPARTMENT-MATRIX.md — 5KB 페르소나 부서 매트릭스
│   ├── INVENTORY-REPORT.md           — 18KB 인벤토리 보고서
│   ├── PSYCHOLOGY-OF-MUSICIAN-FANTASY.md — 16KB 뮤지션 환상 심리학
│   ├── README.md
│   ├── REPO-REFERENCE-MAP.md         — 4KB 레포 참조 맵
│   ├── dev-logs/                     — 개발 로그
│   ├── legal/                        — 법률 문서
│   ├── modules/                      — 모듈 문서
│   ├── pre-season/                   — 프리시즌 문서
│   ├── schedule/                     — 일정
│   └── specs/                        — 스펙
│
├── 📊 data/
│   ├── youtube-catalog.json          — 7KB YouTube 영상 카탈로그
│   └── .gitkeep
│
├── .github/
│   └── workflows/                    — GitHub Actions
│
└── pipeline/ (symlink)               — → pre-season/pipeline/
```

---

## 핵심 파일 크기 순위 (Top 20)

| 순위 | 파일 | 크기 | 카테고리 |
|------|------|------|----------|
| 1 | `core/pipeline.py` | 47KB | 메인 파이프라인 |
| 2 | `pre-season/pipeline/harmony_library.py` | 42KB | 화성 라이브러리 |
| 3 | `local-agent/bot.py` | 36KB | TG 봇 |
| 4 | `pre-season/pipeline/composer_v2.py` | 35KB | 작곡 v2 |
| 5 | `pre-season/index.html` | 33KB | 웹 UI |
| 6 | `core/emotion_profile.py` | 33KB | 감정 프로파일 |
| 7 | `pre-season/pipeline/overture_presets.py` | 30KB | 서곡 프리셋 |
| 8 | `pre-season/pipeline/chord_engine.py` | 27KB | 코드 엔진 |
| 9 | `engines/sourcepool_harvester.py` | 27KB | 소스풀 |
| 10 | `core/humanize.py` | 26KB | 인간화 |
| 11 | `local-agent/piano_expression.py` | 26KB | 피아노 표현 |
| 12 | `scripts/singing_pipeline.py` | 25KB | 노래 파이프 |
| 13 | `local-agent/run_fire_asmr.py` | 25KB | Fire ASMR |
| 14 | `local-agent/midi_crawler.py` | 24KB | MIDI 크롤러 |
| 15 | `pre-season/pipeline/arranger.py` | 22KB | 편곡 |
| 16 | `pre-season/pipeline/singing_pipeline.py` | 19KB | 노래 파이프 |
| 17 | `pre-season/parksy_spotify_mcp.py` | 19KB | Spotify MCP |
| 18 | `core/optimizer.py` | 18KB | 최적화 |
| 19 | `scripts/npu_worker.py` | 18KB | NPU 워커 |
| 20 | `pre-season/pipeline/melody_generator.py` | 18KB | 멜로디 생성 |
