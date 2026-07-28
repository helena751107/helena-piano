# 🎼 MIDI 소스 카탈로그

> BGM Studio에 사용 가능한 Public Domain MIDI 소스 목록

---

## 무료 MIDI 라이브러리

### 클래식 (전부 Public Domain)

| 소스 | URL | 곡 수 | 형식 |
|------|-----|-------|------|
| **Mutopia Project** | https://mutopiaproject.org | 2,000+ | LilyPond + MIDI |
| **IMSLP** | https://imslp.org | 전체 클래식 | PDF + 일부 MIDI |
| **Kunst der Fuge** | https://kunstderfuge.com | 1,000+ | MIDI |
| **Classical Archives** | https://classicalarchives.com | 5,000+ | MIDI (유료) |
| **FreePD** | https://freepd.com | 800+ | MP3 + MIDI |

### 무료 MIDI 검색

| 소스 | URL | 특징 |
|------|-----|------|
| **bitMidi** | https://bitmidi.com | 검색 + 미리듣기 |
| **MIDI World** | https://midiworld.com | 클래식 특화 |
| **FreeMidi** | https://freemidi.org | 장르별 |

---

## YouTube → MIDI 추출 파이프

`parksy-audio/local-agent/steal.py` 사용:

```bash
# 1. YouTube URL에서 MIDI 추출
python3 steal.py "https://youtube.com/watch?v=..."

# 2. 검색 + 추출
python3 steal.py --search "brahms intermezzo op 118 no 2"

# 3. 구간 지정 추출
python3 steal.py "URL" --start 0:30 --end 3:00

# 4. 감정 태그 + 스타일
python3 steal.py "URL" --emotion nocturne --style chopin
```

### 필요 의존성

```bash
pip install yt-dlp demucs basic-pitch mido
# Demucs 첫 실행 시 모델 다운로드 (~300MB, 이후 캐시)
```

---

## 추천: 헬레나 찬양·영국국가 테마

### 가능한 소스

| 곡 | 작곡가 | Public Domain | MIDI 소스 |
|----|--------|---------------|-----------|
| God Save the King | Thomas Arne (1745) | ✅ 확실 | Classical Archives, Mutopia |
| Jerusalem | Hubert Parry (1916) | ✅ 확실 | IMSLP, Kunst der Fuge |
| Amazing Grace | John Newton (1779) | ✅ 확실 | bitMidi, FreeMidi |
| Air on G String | J.S. Bach (1720s) | ✅ 확실 | Mutopia, bitMidi |
| Jesu Joy of Man's Desiring | J.S. Bach (1723) | ✅ 확실 | Mutopia, bitMidi |
| Ave Maria | Schubert (1825) | ✅ 확실 | Classical Archives |
| Hallelujah | Handel (1741) | ✅ 확실 | Mutopia, bitMidi |
| Canon in D | Pachelbel (1680s) | ✅ 확실 | bitMidi, Mutopia |

### @HelenaPark-e7c 찬양 테마 추천

1. **God Save the King** (영국국가) → Salamander 렌더 → 찬양 영상 BGM
2. **Amazing Grace** → 느린 템포, 묵상용
3. **Air on G String** → 우아한 배경
4. **Jesu Joy** → 경쾌한 찬양

---

## MIDI 파일 명명 규칙

```
bgm/midi/
├── bach_prelude_c_major.mid      — 작곡가_제목_조성
├── chopin_nocturne_op9_no1.mid   — 작곡가_제목_작품번호
├── amazing_grace_f_major.mid     — 곡명_조성 (편곡)
└── parksy_original_001.mid       — 자작곡 (parksy_original_번호)
```

---

## 라이선스 체크리스트

MIDI 파일을 추가하기 전 확인:

- [ ] 작곡가 사망 후 70년 경과? (1955년 이전 사망 = Public Domain)
- [ ] MIDI 파일 자체가 CC0/CC-BY 라이선스?
- [ ] 편곡에 저작권 없는가? (원곡 그대로)
- [ ] SoundFont 라이선스 확인 (Salamander = MIT)
