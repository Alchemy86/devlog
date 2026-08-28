#!/usr/bin/env python3
"""Funky retro chiptune for the AsciiWorldEngine lift film, cut to the sequence.

Self-authored, procedurally generated — nothing sampled, nothing from the
internet. Three voices in the NES/SID idiom: a duty-cycled pulse bass, a
pulse-wave arpeggio lead, and a noise-burst hat/kick. Public domain.

Unlike a flat loop, this is ARRANGED to the film's cuts, so the music answers
the picture rather than running underneath it:

  * an INTRO under the opening terminal — just the arpeggio and a soft hat,
    building, no bass and no kick yet;
  * a RISER through the bar before the drop — a rising noise sweep;
  * the BAND DROPS IN on the beat the city is revealed (`--drop`), full bass,
    kick and lead, with a crash on the downbeat — the "boom";
  * the funk DRIVES through the street and the ride;
  * a one-bar RESOLVE to the tonic at the end, so it lands rather than being
    chopped. A short fade-out is left to the film (ShowReel's `fade_out`).

    python3 chiptune.py out.wav [seconds] [--drop SECONDS]

`--drop` defaults to two bars in (3.75 s at 128 BPM), which is where the film
cuts from the terminal to the city.
"""
import sys, wave
import numpy as np

SR = 48000
BPM = 128.0
BEAT = 60.0 / BPM          # seconds per quarter note
STEP = BEAT / 4.0          # a 16th note
BAR = 16 * STEP            # one bar = 4 beats


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
    return np.random.uniform(-1, 1, n) * np.exp(-decay * t)


def riser(dur):
    # A rising noise sweep: white noise under a swelling, slightly rising
    # envelope — the tension before the drop.
    n = int(dur * SR)
    t = np.arange(n) / SR
    swell = (t / dur) ** 2.2
    bright = np.random.uniform(-1, 1, n) * (0.3 + 0.7 * (t / dur))
    return bright * swell


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
LEADPAT = [0, 2, 1, 3, 2, 3, 1, 2, 0, 2, 3, 2, 1, 3, 2, 3]


def build(seconds, drop):
    # Seed the RNG so the noise voices (hats, kick, riser, crash) are the same
    # every run — the committed .wav is then byte-for-byte reproducible from this
    # script, not merely "an equivalent tune".
    np.random.seed(0xC17)
    total = int(seconds * SR) + SR
    bass = np.zeros(total)
    lead = np.zeros(total)
    drum = np.zeros(total)

    nbars = int(np.ceil(seconds / BAR)) + 1
    drop_bar = max(1, int(round(drop / BAR)))
    last_bar = int(seconds / BAR)   # the bar the RESOLVE lands in

    for B in range(nbars):
        bar_t = B * BAR
        # After the drop the loop runs Am F C G. The last bar resolves to Am,
        # whatever the loop would otherwise play, so the piece lands home.
        if B >= last_bar:
            root, tones = BARS[0]           # Am
        else:
            root, tones = BARS[(B - drop_bar) % 4] if B >= drop_bar else BARS[0]

        intro = B < drop_bar
        resolve = B >= last_bar

        for s in range(16):
            at = bar_t + s * STEP
            # bass: root dropped an octave, punchy short duty
            if BASSGATE[s] == "x":
                if intro:
                    # only a soft heartbeat on the downbeats during the intro
                    if s == 0 or s == 8:
                        place(bass, 0.22 * pulse(midi(root - 12), STEP * 1.4, duty=0.5), at)
                else:
                    place(bass, 0.42 * pulse(midi(root - 12), STEP * 0.9, duty=0.5), at)
            # lead: bright pulse arpeggio, thin duty for the chip bite
            note = tones[LEADPAT[s] % len(tones)] + 12
            lead_gain = 0.11 if intro else 0.20
            place(lead, lead_gain * pulse(midi(note), STEP * 0.95, duty=0.30, vib=2.0), at)
            # drums
            if intro:
                # a soft hat building, no kick yet
                if s % 4 == 2:
                    place(drum, 0.08 * noise(0.04, 120), at)
            else:
                if s % 4 == 0:
                    kick = 0.5 * noise(0.11, 55) * (
                        np.sin(2 * np.pi * 90 * (np.arange(int(0.11 * SR)) / SR)) * 0.6 + 1)
                    place(drum, kick, at)
                if s % 2 == 1:
                    place(drum, 0.14 * noise(0.04, 120), at)

        # the RISER fills the bar before the drop, swelling into it
        if B == drop_bar - 1:
            place(drum, 0.5 * riser(BAR), bar_t)
        # the CRASH lands on the drop downbeat — the "boom"
        if B == drop_bar:
            crash = 0.6 * noise(0.7, 6) * (
                np.sin(2 * np.pi * 200 * (np.arange(int(0.7 * SR)) / SR)) * 0.3 + 1)
            place(drum, crash, bar_t)
        # a final tonic hit on the resolve downbeat, so the end sounds landed
        if B == last_bar:
            place(bass, 0.5 * pulse(midi(BARS[0][0] - 12), BEAT * 2.0, duty=0.5), bar_t)
            place(lead, 0.24 * pulse(midi(69), BEAT * 2.0, duty=0.30, vib=2.0), bar_t)

    mix = bass + lead + drum
    mix = mix[: int(seconds * SR)]
    # soft limit
    peak = np.max(np.abs(mix)) or 1.0
    mix = np.tanh(mix / peak * 1.3) * 0.9
    return mix


def main():
    out = sys.argv[1]
    seconds = 30.0
    drop = 2 * BAR   # two bars in — the terminal-to-city cut
    rest = sys.argv[2:]
    i = 0
    while i < len(rest):
        if rest[i] == "--drop":
            drop = float(rest[i + 1]); i += 2
        else:
            seconds = float(rest[i]); i += 1
    mono = build(seconds, drop)
    # tiny stereo spread: lead slightly right, bass centred
    stereo = np.stack([mono, mono], axis=1)
    pcm = (stereo * 32767).astype(np.int16)
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"wrote {out}: {seconds:.1f}s, {BPM:.0f} BPM, A-minor funk, "
          f"drop at {drop:.3f}s (bar {round(drop/BAR)+1})")


if __name__ == "__main__":
    main()
