---
title: 'The chiptune that outgrew its blog post'
tag: 'ShowReel'
kicker: 'Audio · Rust'
eyebrow: 'ShowReel · Feature'
order: 5
description: >-
  A demo video needed music with no licence to worry about, so a 114-line Python script wrote
  its own chiptune. The captain asked why that lived beside a blog asset instead of inside the
  renderer that times things to pictures for a living — and it moved.
dek: >-
  A demo video needed music with no licence to worry about, so a 114-line Python script wrote
  its own chiptune. The captain asked why a generator that times itself to a video lived
  beside a blog asset instead of inside the renderer — and eighteen minutes later, it didn't.
lead: >-
  The AsciiWorldEngine lift ride needed a soundtrack, and the instruction was simple: source
  it legally or ship it silent. Rather than gamble on a "free to use" file, a 114-line Python
  script wrote its own chiptune. The captain looked at it and asked why a generator that times
  itself to a video lived beside a blog asset instead of inside the renderer that times things
  to video for a living. It doesn't any more.
metrics:
  - num: '0'
    label: 'Samples licensed — every note is synthesised'
  - num: '809'
    label: 'Lines of Rust doing the synthesis, <code>src/music.rs</code>'
  - num: '~<span class="accent">7</span>'
    label: 'ms from a hard cut to the nearest bar line'
  - num: '0.9997'
    label: 'Envelope correlation vs. the Python original (spectrum: 0.9999)'
note: >-
  Figures on this page were checked against the ShowReel and devlog repositories directly:
  <code>chiptune.py</code>'s original line count from the commit that added it,
  <code>src/music.rs</code> and its own module docs read directly rather than quoted from the
  commit message, the 7 ms and correlation figures from ShowReel's own <code>README.md</code>,
  and the two commit timestamps from each repository's own log.
---

<section class="prose" markdown="1">

## A problem worth avoiding

The lift ride is a demo video for this blog — a walk through AsciiWorldEngine's city and
up in the tower's glass lift, cut as a short film in ShowReel. It needed music, and this
is a public site, so the rule was blunt: source audio legally and keep the licence, or
ship the clip silent. Nobody wanted to be the one explaining a licensing question later.

Instead of hunting for something labelled free-to-use and hoping the label held up, the
answer was to not need one. `chiptune.py` — a 114-line Python script, committed
alongside the video assets — synthesises three voices in the NES/SID idiom: a
duty-cycled pulse bass, a pulse-wave arpeggio lead with a little vibrato, and noise
bursts standing in for hats and kick. Its own docstring says what it is: self-authored,
nothing sampled, nothing pulled off the internet, public domain.

</section>

<section class="prose" markdown="1">

## The obvious question

The captain saw it and asked the question that actually mattered: if a generator times
its own output to a video and plays inside that video, why does it live next to a blog
asset instead of inside the renderer built to time things to pictures? Should it not be
a feature, in Rust?

It now is. ShowReel's own commit for it calls the Python file what it was — "the
devlog's throwaway `chiptune.py`" — and ports the idiom faithfully rather than treating
it as a spec to improve on: the same pulse bass, the same arpeggio lead, the same noise
drums, none of it reinvented.

</section>

<section class="prose" markdown="1">

## What shipped

A track's source can now be generated music instead of a file. A `Music` spec resolves
to a synthesised WAV at exactly the point a file track's `asset` resolves to a path, so
from there it is an ordinary audio input — placement, gain, fades, multi-track mixing
and the mobile cut all compose for free rather than through a second audio path built to
match the first.

Authoring is one word in the film file, mirroring the shorthand the colour grade already
uses:

</section>

<figure class="code">
  <pre><code>"audio": [
  { "music": "funk" },
  { "music": { "mood": "dreamy", "key": "C", "bpm": 96 }, "fade_out": 2.0 }
]</code></pre>
  <figcaption>
    A bare mood word for the reference tune, sized to the film, or an object for key, bpm and
    tempo fit — <code>examples/music_demo.film.jsonc</code> in the ShowReel repository.
  </figcaption>
</figure>

<section class="prose" markdown="1">

## The timing is the point

With no duration given, the tune sizes itself to exactly the film's length, so it never
needs trimming and never hard-cuts to silence. `fit: "film"` goes further: the authored
tempo is treated as a target and nudged so a whole number of bars spans the film
exactly, landing the final downbeat on the last frame. Space scene cuts a whole number
of bars apart and every cut becomes a chord change, generated to fit rather than
hand-aligned after the fact.

The self-contained demo film proves it: four bar-aligned scenes at 128 BPM, and its
three hard cuts land within about 7 ms of a downbeat in the rendered audio.

</section>

<figure>
  <video controls preload="metadata" poster="../assets/img/showreel/music-demo-poster.png"
         width="720" height="406">
    <source src="../assets/video/showreel/music-demo-mobile.mp4" type="video/mp4">
  </video>
  <figcaption>
    ShowReel's own proof file, rendered end to end with no assets — every background is a
    colour, the only source is the chiptune the one <code>music</code> track synthesises. Each
    hard cut lands on the downbeat of bar 5, 9 or 13; the progress bar under the second
    scene's title is that beat grid drawn on screen.
  </figcaption>
</figure>

<section class="prose" markdown="1">

## Checked against the thing it replaced

The Rust port was checked honestly against the Python original rather than assumed
faithful: envelope and spectrum correlation of roughly 0.9997 and 0.9999. The one
deliberate difference is a seeded random generator in place of the Python script's
global one, which means renders now reproduce — same film, same audio, every time.
That's a real improvement on the thing it replaced, not just a port of it.

</section>

<div class="pullquote">
  <p>&ldquo;It was in the wrong repo, as a throwaway script, until someone asked the obvious
  question.&rdquo;</p>
  <cite>Why this one is worth telling</cite>
</div>

<section class="prose" markdown="1">

## Back where it started

The feature went straight back into the video that caused it. The AsciiWorldEngine lift
film's soundtrack is arranged to its own cuts, not laid under them: sparse under the
opening terminal, a riser through the bar before the reveal, the full band dropping in
with a crash on the cut to the city, driving through the street and the ride, and a
one-bar resolve to the tonic at the end so it lands rather than getting chopped. The
ShowReel feature landed at 19:03; the recut using it landed at 19:21. Eighteen minutes.

</section>
