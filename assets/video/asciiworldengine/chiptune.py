#!/usr/bin/env python3
"""Funky retro chiptune for the AsciiWorldEngine lift ride.

Self-authored, procedurally generated — nothing sampled, nothing from the
internet. Three voices in the NES/SID idiom: a duty-cycled pulse bass, a
pulse-wave arpeggio lead, and a noise-burst hat/kick. Public domain.

    python3 chiptune.py out.wav [seconds]
"""
import sys, struct, wave
import numpy as np

SR = 48000
BPM = 128.0
BEAT = 60.0 / BPM          # seconds per quarter note
STEP = BEAT / 4.0          # a 16th note

def midi(n):               # midi note -> Hz
    return 440.0 * 2 ** ((n - 69) / 12.0)

def pulse(freq, dur, duty=0.5, vib=0.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    ph = (t * freq) % 1.0
    if vib:
        ph = ((t * freq) + vib * np.sin(2 * np.pi * 6.0 * t) / freq) % 1.0
    wave_ = np.where(ph < duty, 1.0, -1.0)
    # short attack/decay so steps don't click
    env = np.ones(n)
    a = int(0.004 * SR)
    env[:a] = np.linspace(0, 1, a)
    env[-a:] = np.linspace(1, 0, a)
    return wave_ * env

def noise(dur, decay):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return (np.random.RandomState(0xC17).uniform(-1, 1, n) if False
            else np.random.uniform(-1, 1, n)) * np.exp(-decay * t)

def place(buf, sig, at):
    i = int(at * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i]

# --- the tune -------------------------------------------------------------
# A minor funk loop, 4 bars: Am  F  C  G  (i - VI - III - VII).
# roots (midi) and the chord tones the lead arpeggiates.
BARS = [
    (45, [57, 60, 64, 69]),   # Am : A  C  E  A
    (41, [57, 60, 65, 69]),   # F  : A  C  F  A
    (48, [60, 64, 67, 72]),   # C  : C  E  G  C
    (43, [59, 62, 67, 71]),   # G  : B  D  G  B
]

# A funky 16th-note gate for the bass (x = play, . = rest), one bar = 16 steps
BASSGATE = "x.x.x..xx.x.x.x."
# The lead arpeggio walks the chord tones, syncopated
LEADPAT  = [0, 2, 1, 3, 2, 3, 1, 2, 0, 2, 3, 2, 1, 3, 2, 3]

def build(seconds):
    total = int(seconds * SR) + SR
    bass = np.zeros(total)
    lead = np.zeros(total)
    drum = np.zeros(total)
    bar_len = 16 * STEP
    loop_len = 4 * bar_len
    nloops = int(np.ceil(seconds / loop_len)) + 1
    for L in range(nloops):
        for b, (root, tones) in enumerate(BARS):
            bar_t = L * loop_len + b * bar_len
            for s in range(16):
                at = bar_t + s * STEP
                # bass: root, dropped an octave, punchy short duty
                if BASSGATE[s] == "x":
                    place(bass, 0.42 * pulse(midi(root - 12), STEP * 0.9,
                                             duty=0.5), at)
                # lead: bright pulse arpeggio, thin duty for the chip bite
                note = tones[LEADPAT[s] % len(tones)] + 12
                place(lead, 0.20 * pulse(midi(note), STEP * 0.95,
                                         duty=0.30, vib=2.0), at)
                # drums: kick on the beat, hat on the offbeat 8ths
                if s % 4 == 0:
                    place(drum, 0.5 * noise(0.11, 55) *
                          (np.sin(2 * np.pi * 90 *
                                  (np.arange(int(0.11 * SR)) / SR)) * 0.6 + 1),
                          at)
                if s % 2 == 1:
                    place(drum, 0.14 * noise(0.04, 120), at)
    mix = bass + lead + drum
    mix = mix[: int(seconds * SR)]
    # soft limit
    peak = np.max(np.abs(mix)) or 1.0
    mix = np.tanh(mix / peak * 1.3) * 0.9
    return mix

def main():
    out = sys.argv[1]
    seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 20.0
    mono = build(seconds)
    # tiny stereo spread: lead slightly right, bass centred
    stereo = np.stack([mono, mono], axis=1)
    pcm = (stereo * 32767).astype(np.int16)
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"wrote {out}: {seconds:.1f}s, {BPM:.0f} BPM, A-minor funk loop")

if __name__ == "__main__":
    main()
