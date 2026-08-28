# How `lift-ride.mp4` was made

`lift-ride.mp4` is AsciiWorldEngine's lift, cut as a short film in ShowReel from
the sequence the captain called: open on a bare terminal, the run command types
itself out, the city comes up, walk the avenue and look up the towers, then into
the lift and up over the rooftops. Everything on screen is a real capture of the
running engine or ShowReel's own typography; nothing is stock and nothing is
faked. `lift-ride.film.jsonc` is the whole film as data, and this file says where
each of its inputs came from.

All engine capture used the source repo (`~/Github/firstmate/projects/asciicity`,
the AsciiWorldEngine crate — dir `asciicity`, project renamed) at its default
seed, `0xACC17`, so the street, the tower you look up, and the lift you ride are
one city. The two `.mp4` inputs are 1280×720 (the film's own size) at CRF 23 —
ShowReel source, not delivery; the delivery is `lift-ride.mp4` at CRF 36.

## `street-capture.mp4` — the city, then looking up

The shipped `--film` recorder, driven by a script (see `docs/film.md` in the
source repo). It writes one SVG per tick, encoded with the librsvg pipeline that
doc prints:

```
asciicity --film --script street.txt --out frames --name a --cols 180 --rows 60 --fps 30
ffmpeg -y -framerate 30 -start_number 1 -i frames/a-%06d.svg \
  -vf "scale=-1:720:flags=lanczos,crop=1280:720" -c:v libx264 -pix_fmt yuv420p -crf 23 street-capture.mp4
```

`street.txt`, the beats, in order:

```
2.5s wait                 # the reveal: the city fills in on the pavement
5s   walk                 # down the avenue at a walking pace
0.7s turn-right           # turn toward the towers flanking the avenue
1.4s turn-right look-up   # sweep the eye up their faces
2s   look-up              # hold — the towers looming overhead
```

Looking straight up in the middle of an avenue frames sky between the buildings;
turning to face the flanking towers first frames their faces and spired tops, so
the look-up ends on the towers, not the night sky.

## `lift-ride-capture.mp4` — into the lift, and up over the city

The first cut of this clip faced the shaft wall and pitched **down** at the
street — half the frame was floor. That was the whole note. This one holds the
pitch **up-and-out at the skyline** and drifts it gently down as the car climbs,
so the rooftops slide past the glass and you never see more floor than sky.

Captured with a private `--ride-film` mode added to a **scratch clone** of the
engine (not shipped, same footing as the previous cut's `--ride-shot`). It drives
the real lift the way a player does — walk in off the lobby, one press of the up
button, which commits the car to the top of the shaft and lets go of you
(`Lift::call`, `docs/lift.md`) — then stands at the back of the car facing the
**outward** glass and writes every tick of the hands-free climb. Nothing is driven
behind the engine's back: the car runs itself on its own smoothstep; only the
camera pose is set, the same way the shipped `--lift` evidence shots set theirs.
The one thing that mode adds is the pose: face the street glass (`face_street`),
and hold the pitch on a ramp from `+0.03` near the pavement to `-0.20` up by the
rooftops — level would leave empty sky over the skyline at the top, and down
would put the floor back in shot. `--pitch` biases the ramp.

```
asciicity --ride-film --out frames --name ride --cols 180 --rows 60 --fps 30
ffmpeg ... (same librsvg + scale/crop/x264 line as above) ... lift-ride-capture.mp4
```

## `lift-chiptune.wav` — the soundtrack, arranged to the cuts

`chiptune.py` (committed alongside), a funky-retro A-minor pulse-wave chiptune —
self-authored, procedurally generated, nothing sampled, nothing from the
internet, public domain, the position ShowReel takes on its own demo bed. It is
**arranged to the film**, not laid under it: a sparse intro (arpeggio and a soft
hat, no bass, no kick) under the opening terminal, a rising noise sweep through
the bar before the cut, the full band dropping in with a crash on the beat the
city is revealed (`--drop 3.75`), the funk driving through the street and the
ride, and a one-bar resolve to the tonic at the end so it lands.

```
python3 chiptune.py lift-chiptune.wav 30.0
```

An agent cannot hear it: it was checked by `ffprobe` (a real 30 s stereo stream),
`volumedetect` (mean −12.8 dB, peak −2.2 dB — a sensible level, no clip), a
`showwavespic` waveform (the quiet intro, the drop's spike at ~3.75 s, the resolve)
and a `showspectrumpic` spectrogram (a real 16th-note grid and pitched voices, not
noise) — stated plainly rather than claimed as listened to.

## `lift-ride.mp4` — the ShowReel render

The film is authored at 1280×720, so the master **is** the 720p cut the page
ships. CRF 36 keeps it to a few MB (~4.6 MB) — the ASCII detail is expensive to
compress, and at 720p in a page figure the small softening is a fair trade.

```
showreel render lift-ride.film.jsonc -A . --crf 36 -o lift-ride.mp4
```

Two transitions carry it, chosen for the job rather than for variety: a hard
**cut** on the beat for the reveal (the "boom"), and a **cross-blur** dissolve to
bridge looking-up-at-the-tower into the lift inside it. `lift-ride-poster.png` is
the ride-skyline frame at 20.5 s, extracted with `ffmpeg -ss` and quantised to
256 colours like the seed stills.
