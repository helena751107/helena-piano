#!/bin/bash
# ─── Helena Piano BGM Studio — S21 Local Render ──────────
# S21 + proot Ubuntu에서 MIDI → MP3 로컬 렌더링
#
# 사용법:
#   bash render.sh                    # bgm/midi/*.mid 전체 렌더
#   bash render.sh moonlight.mid      # 특정 파일만
#   bash render.sh --soundfont fluidr3  # Fluid R3로 렌더
#   bash render.sh --gain 2.0         # 게인 조정
#
# 필수:
#   apt install fluidsynth ffmpeg fluid-soundfont-gm
# ──────────────────────────────────────────────────────────

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BGM_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
MIDI_DIR="$BGM_DIR/midi"
OUT_DIR="$BGM_DIR/output"

# ── 설정 ─────────────────────────────────────────────────
GAIN=1.5
SAMPLE_RATE=44100
MP3_BITRATE=192k
SOUNDFONT="fluidr3"
SF_PATH=""

mkdir -p "$OUT_DIR"

# ── 인자 파싱 ─────────────────────────────────────────────
MIDI_FILE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --soundfont) SOUNDFONT="$2"; shift 2 ;;
    --gain)      GAIN="$2";      shift 2 ;;
    --help|-h)
      echo "사용법: bash render.sh [파일명] [--soundfont salamander|fluidr3] [--gain 1.5]"
      exit 0 ;;
    *) MIDI_FILE="$1"; shift ;;
  esac
done

# ── SoundFont 찾기 ────────────────────────────────────────
# Fluid R3 GM (Salamander v3 는 SFZ2+ARIA 확장 → fluidsynth 비호환, 2026-08-16 결정)
find_soundfont() {
  for p in \
    "/usr/share/sounds/sf2/FluidR3_GM.sf2" \
    "/usr/share/sounds/sf2/FluidR3_GS.sf2" \
    "/usr/share/sounds/sf2/TimGM6mb.sf2"; do
    if [ -f "$p" ]; then SF_PATH="$p"; return 0; fi
  done

  if [ -z "$SF_PATH" ]; then
    echo "❌ SoundFont 없음. 설치:"
    echo "   apt install fluid-soundfont-gm"
    echo "   또는 Salamander: wget https://github.com/sfzinstruments/SalamanderGrandPiano/releases/download/v3/salamander-grand-piano-v3.sf2"
    exit 1
  fi
}

find_soundfont
echo "🎹 SoundFont: $SOUNDFONT ($(basename "$SF_PATH"))"
echo "🎛️  Gain: ${GAIN}x | Bitrate: $MP3_BITRATE | SR: ${SAMPLE_RATE}Hz"
echo ""

# ── 렌더링 ────────────────────────────────────────────────
render_one() {
  local midi="$1"
  local name
  name=$(basename "$midi" | sed 's/\.mid[i]*$//')
  local wav="$OUT_DIR/$name.wav"
  local mp3="$OUT_DIR/$name.mp3"

  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🎵 $name"

  # MIDI → WAV (fast-render, 오디오 드라이버 우회)
  fluidsynth -ni -F "$wav" -O s16 \
    -r "$SAMPLE_RATE" -g "$GAIN" \
    "$SF_PATH" "$midi" 2>&1 | tail -1

  # WAV → MP3 (LUFS 노멀라이즈)
  ffmpeg -y -i "$wav" \
    -codec:a libmp3lame -b:a "$MP3_BITRATE" \
    -filter:a "loudnorm=I=-16:LRA=11:TP=-1.5" \
    "$mp3" 2>/dev/null

  rm -f "$wav"

  local size dur
  size=$(du -h "$mp3" | cut -f1)
  dur=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$mp3" 2>/dev/null || echo "?")
  echo "   ✅ $mp3 (${size}, ${dur}s)"
}

if [ -n "$MIDI_FILE" ]; then
  # 특정 파일만
  if [ -f "$MIDI_FILE" ]; then
    render_one "$MIDI_FILE"
  elif [ -f "$MIDI_DIR/$MIDI_FILE" ]; then
    render_one "$MIDI_DIR/$MIDI_FILE"
  else
    echo "❌ 파일 없음: $MIDI_FILE"
    exit 1
  fi
else
  # 전체 렌더
  count=0
  for midi in "$MIDI_DIR"/*.mid "$MIDI_DIR"/*.midi; do
    [ -f "$midi" ] || continue
    render_one "$midi"
    count=$((count + 1))
  done
  echo ""
  echo "✅ 완료: $count 트랙 렌더링 ($SOUNDFONT)"
fi
