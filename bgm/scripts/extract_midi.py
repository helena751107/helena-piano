#!/usr/bin/env python3
"""Helena Piano — Audio → MIDI extraction (lightweight, no TensorFlow)
Usage: python3 extract_midi.py audio.wav [output.mid]
       python3 extract_midi.py audio.mp3 --onset-threshold 0.3
Depends: librosa, numpy, scipy, pretty_midi (all installed on S21)
"""

import sys, os, argparse
import numpy as np
import librosa
import pretty_midi

def extract_midi(audio_path, output_path=None, onset_threshold=0.15, min_note_len=0.08):
    if output_path is None:
        output_path = os.path.splitext(audio_path)[0] + '.mid'

    print(f"📥 Loading: {audio_path}")
    y, sr = librosa.load(audio_path, sr=22050, mono=True)
    print(f"   {len(y)/sr:.1f}s, {sr}Hz, mono")

    # Harmonic-percussive separation (keep harmonic = melody)
    print("🔍 Separating harmonic...")
    y_harmonic, _ = librosa.effects.hpss(y)

    # Pitch tracking via CQT
    print("🎹 Tracking pitches (CQT)...")
    hop_length = 512
    cqt = np.abs(librosa.cqt(y_harmonic, sr=sr, hop_length=hop_length,
                              fmin=librosa.note_to_hz('A0'), n_bins=84, bins_per_octave=12))

    # Onset detection
    onset_frames = librosa.onset.onset_detect(y=y_harmonic, sr=sr, hop_length=hop_length,
                                               backtrack=True, units='frames')
    onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=hop_length)
    print(f"   Found {len(onset_times)} onsets")

    if len(onset_times) < 2:
        print("⚠️  너무 적은 onset. 문턱값 낮춰서 재시도...")
        onset_frames = librosa.onset.onset_detect(y=y_harmonic, sr=sr, hop_length=hop_length,
                                                   backtrack=True, units='frames',
                                                   onset_threshold=onset_threshold * 0.5)
        onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=hop_length)
        print(f"   Found {len(onset_times)} onsets (lowered threshold)")

    # Create MIDI
    midi = pretty_midi.PrettyMIDI()
    piano = pretty_midi.Instrument(program=0, name='Extracted Piano')

    for i, onset in enumerate(onset_times):
        # Find pitch at this onset
        frame = librosa.time_to_frames(onset, sr=sr, hop_length=hop_length)
        frame = min(frame, cqt.shape[1] - 1)
        pitch_bin = np.argmax(cqt[:, frame])
        midi_note = pitch_bin + 21  # A0 = MIDI 21

        # End time = next onset or 1 second max
        end_time = onset_times[i + 1] if i + 1 < len(onset_times) else onset + 1.0
        duration = max(end_time - onset, min_note_len)

        # Velocity from CQT magnitude
        velocity = int(np.clip(cqt[pitch_bin, frame] * 127 / cqt.max(), 40, 127))

        note = pretty_midi.Note(velocity=velocity, pitch=midi_note,
                                start=onset, end=onset + duration)
        piano.notes.append(note)

    midi.instruments.append(piano)
    midi.write(output_path)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"✅ {output_path} ({size_kb:.1f}KB, {len(piano.notes)} notes)")
    return output_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Audio → MIDI extraction')
    parser.add_argument('audio', help='Input audio file (.wav/.mp3)')
    parser.add_argument('output', nargs='?', help='Output MIDI file')
    parser.add_argument('--onset-threshold', type=float, default=0.15, help='Onset detection threshold')
    parser.add_argument('--min-note-len', type=float, default=0.08, help='Minimum note length (s)')
    args = parser.parse_args()
    extract_midi(args.audio, args.output, args.onset_threshold, args.min_note_len)
