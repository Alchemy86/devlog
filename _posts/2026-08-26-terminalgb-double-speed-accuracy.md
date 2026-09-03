---
title: 'The double-speed bug that cost 2,304 pixels'
tag: 'TerminalGB'
kicker: 'CGB · PPU · double speed'
card_kicker: 'Emulator accuracy'
eyebrow: 'TerminalGB · Emulator accuracy'
order: 17
description: >-
  A one-dot register-commit stagger, calibrated on single-speed test ROMs, silently vanished
  in double speed — drawing a wrong stripe across the screen. Fixing it took an AGE reference
  ROM from 2,304 wrong pixels to a clean pass, and explains why TerminalGB ships two picture
  engines.
og_title: >-
  The double-speed bug that cost 2,304 pixels
og_description: >-
  A one-dot register-commit stagger, calibrated on single-speed ROMs, silently vanished in
  double speed. Why TerminalGB ships two picture engines.
dek: >-
  A register-commit trick worth exactly one dot of time vanished when the CPU clock doubled —
  and a Color game drew a wrong stripe across the screen.
lead: >-
  A register-commit trick worth exactly one dot of time was calibrated against single-speed
  test ROMs. In double speed there was no longer a spare dot to hold it, so it silently
  disappeared and a Color game drew a wrong stripe across the screen.
metrics:
  - num: '2,304'
    label: 'Wrong pixels, before'
    accent: true
  - num: '0'
    label: 'Wrong pixels, after · PASS'
  - num: '23,040'
    label: 'Pixels in a GB frame'
  - num: '1 → 0'
    label: 'Dots of commit stagger'
note: >-
  Every figure here is drawn from TerminalGB's own conformance notes and accuracy scoreboard.
  The reference ROMs cited (AGE, Gambatte, Mooneye GB, Mealybug Tearoom) are public test
  suites; the comparisons are run against hardware-captured images and re-run on every build.
---

<section class="prose" markdown="1">

## The symptom

A Game Boy Color game that flips `LCDC` bits partway through a scanline — the register
that controls which tile sources the picture processor is reading from — came out with a
visibly wrong stripe pattern, but *only* when the console was running in double-speed
mode. The same game in normal speed was pixel-exact.

That "only in double speed" is the whole tell. When one variant of a scene is perfect
and its faster-clocked twin is wrong, the bug is not in the drawing logic — the drawing
logic is provably correct at single speed. The bug is in how time is being counted.

</section>

<section class="prose" markdown="1">

## Two clocks, one of which doubles

The Game Boy Color can switch its CPU into a double-speed mode. The important,
easily-forgotten detail is that this does *not* speed up the screen. The picture
processor's dot clock is fixed; only the CPU's own clock doubles. So the unit that a lot
of internal timing is measured in — the CPU machine cycle, or "M-cycle" — changes width
depending on the mode:

</section>

<figure aria-labelledby="fig1-cap">
  <svg viewBox="0 0 720 300" role="img" xmlns="http://www.w3.org/2000/svg"
       font-family="'JetBrains Mono', monospace">
    <style>
      .cell   { fill: var(--code-bg); stroke: var(--hairline); stroke-width: 1.5; }
      .stag   { fill: var(--accent);  opacity: .18; }
      .stag-b { fill: none; stroke: var(--accent); stroke-width: 1.5; }
      .lbl    { fill: var(--ink-soft); font-size: 12px; letter-spacing: .04em; }
      .ttl    { fill: var(--ink); font-size: 12px; font-weight: 700; letter-spacing: .06em; }
      .ok     { fill: var(--ink); font-size: 12px; }
      .bad    { fill: var(--accent); font-size: 12px; font-weight: 700; }
      .dot    { fill: var(--ink-soft); font-size: 11px; }
    </style>

    <!-- SINGLE SPEED -->
    <text x="0" y="30" class="ttl">SINGLE SPEED — 4 DOTS PER M-CYCLE</text>
    <!-- 4 cells, 120px each -->
    <rect x="0"   y="46" width="120" height="56" class="cell"/>
    <rect x="120" y="46" width="120" height="56" class="cell"/>
    <rect x="240" y="46" width="120" height="56" class="cell"/>
    <rect x="360" y="46" width="120" height="56" class="cell"/>
    <text x="60"  y="80" text-anchor="middle" class="dot">dot 1</text>
    <text x="180" y="80" text-anchor="middle" class="dot">dot 2</text>
    <text x="300" y="80" text-anchor="middle" class="dot">dot 3</text>
    <text x="420" y="80" text-anchor="middle" class="dot">dot 4</text>
    <!-- 1-dot stagger occupies dot 1 -->
    <rect x="0" y="46" width="120" height="56" class="stag"/>
    <rect x="0" y="46" width="120" height="56" class="stag-b"/>
    <text x="60" y="122" text-anchor="middle" class="lbl">stagger</text>
    <text x="300" y="122" text-anchor="middle" class="ok">value applied ✓ (3 dots spare)</text>

    <!-- DOUBLE SPEED -->
    <text x="0" y="196" class="ttl">DOUBLE SPEED — 2 DOTS PER M-CYCLE</text>
    <rect x="0"   y="212" width="120" height="56" class="cell"/>
    <rect x="120" y="212" width="120" height="56" class="cell"/>
    <text x="60"  y="246" text-anchor="middle" class="dot">dot 1</text>
    <text x="180" y="246" text-anchor="middle" class="dot">dot 2</text>
    <!-- 1-dot stagger consumes the whole window (both dots) -->
    <rect x="0" y="212" width="240" height="56" class="stag"/>
    <rect x="0" y="212" width="240" height="56" class="stag-b"/>
    <text x="120" y="288" text-anchor="middle" class="lbl">stagger consumes the entire M-cycle</text>
    <!-- commit falls off the edge -->
    <text x="360" y="246" class="bad">✗ value never applied</text>
    <line x1="240" y1="240" x2="345" y2="240" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 4"/>
  </svg>
  <figcaption id="fig1-cap">
    A one-dot register-commit stagger fits comfortably inside a four-dot M-cycle.
    Halve the M-cycle and the same one dot consumes the whole thing — leaving no
    room for the deferred value to land.
  </figcaption>
</figure>

<section class="prose" markdown="1">

## The one-dot stagger

Real Color hardware doesn't make an `LCDC` write visible at the exact instant the CPU
performs it — a couple of the bits become visible to the picture processor one dot later
than the rest. TerminalGB modelled that faithfully with a one-dot "early" stagger on the
memory unit's `LCDC` write-commit: hold the change back by a dot, then apply it.

The trouble is where that one dot came from. The stagger was calibrated exclusively
against a suite of single-speed reference ROMs, where an M-cycle is four dots wide. A
one-dot delay inside a four-dot budget is comfortable. But in double speed the M-cycle
is only two dots wide, and the deferred value's slot fell off the end of the cycle. The
commit was *silently never applied* — no error, no assertion, just a value that quietly
evaporated and a stripe drawn from the wrong tile source for one dot too long.

<div class="callout">
  <p class="eyebrow">The general trap</p>
  <p>
    A timing offset measured in absolute dots is only correct for the clock it was
    measured on. The moment the surrounding cycle changes width, an offset that
    "fit comfortably" can consume the entire window — and because nothing overflows,
    nothing complains.
  </p>
</div>

</section>

<section class="prose" markdown="1">

## Finding it

It surfaced as a hard reference failure, not a bug report. The accuracy harness runs the
AGE test-ROM `m3-bg-lcdc-ds@cgbBCE` — a Color, double-speed ROM built specifically to
stress mid-scanline `LCDC` writes — and compares the rendered frame against a
hardware-captured reference image. It read **2,304 of 23,040 pixels wrong**. Its
single-speed sibling, `m3-bg-lcdc@cgbBCE`, was already pixel-exact. One passing, one
failing, identical but for the speed switch: that pair is what pointed straight at the
clock, not the renderer.

</section>

<section class="prose" markdown="1">

## The fix

The commit routine now knows what speed it is running at. Where it used to apply a fixed
one-dot stagger, it takes the running `GbSpeed` and drops the stagger to zero when there
is no room for it:

<pre><code>// ppu_write_commit — CGB LCDC arm
let early = match speed {
    GbSpeed::Single =&gt; 1,   // 4-dot M-cycle: a spare dot exists, model the hardware delay
    GbSpeed::Double =&gt; 0,   // 2-dot M-cycle: no spare dot — apply immediately instead
};</code></pre>

Removing the stagger outright in double speed beats leaving it in to be silently
truncated. The single-speed path is untouched, so nothing that already passed regresses.

</section>

<section class="prose" markdown="1">

## What actually happened to the numbers

`m3-bg-lcdc-ds@cgbBCE` went from a 2,304-pixel failure to a pixel-exact pass, moving the
AGE suite from 10 to 11 of 59, and the Gambatte double-speed rows improved on the
accurate engine. Five more rows fell sharply without reaching zero:

<div class="table-wrap">
  <table>
    <thead>
      <tr>
        <th>Reference row (double speed)</th>
        <th class="num">Before</th>
        <th class="num">After</th>
      </tr>
    </thead>
    <tbody>
      <tr><td class="mono">m3-bg-lcdc-ds@cgbBCE</td><td class="num">2,304</td><td class="num">PASS</td></tr>
      <tr><td class="mono">bgtiledata_spx08_ds_3</td><td class="num">1,032</td><td class="num">8</td></tr>
      <tr><td class="mono">bgtiledata_spx08_ds_4</td><td class="num">2,064</td><td class="num">16</td></tr>
      <tr><td class="mono">bgtiledata_spx09_ds_1</td><td class="num">1,144</td><td class="num">8</td></tr>
      <tr><td class="mono">bgtiledata_spx09_ds_3</td><td class="num">1,144</td><td class="num">8</td></tr>
      <tr><td class="mono">bgtiledata_spx09_ds_4</td><td class="num">2,048</td><td class="num">16</td></tr>
    </tbody>
  </table>
</div>

Those remainders are a different, smaller timing discrepancy that the stagger bug was
masking. Eight wrong pixels are reported as eight, so the next person to open that
scoreboard sees exactly how much is left to chase.

The regression is locked in with a test that has teeth: reverting the stagger to a fixed
`1` unconditionally reproduces the original 2,304-pixel failure, so the mistake cannot
quietly come back.

</section>

<section class="prose" markdown="1">

## A note on counting pixels

Not every "wrong pixels" number on the scoreboard is a raw count of differing pixels.
The Mealybug Tearoom comparisons use a shade-rank distance, which is deliberately
unforgiving: a frame that introduces one extra distinct shade can report on the order of
23,040 "wrong" no matter how much of the rest is perfect, and a four-pixel error can
move the total by tens of thousands. Four genuinely wrong pixels there scores 22,070.

So these figures are never converted to a percentage. The 2,304 and the residual counts
above *are* direct pixel counts from the AGE and Gambatte comparisons; a shade-rank
distance is treated as an ordering signal, not a pixel tally.

</section>

<section class="prose" markdown="1">

## Why this needed the accurate engine at all

A one-dot, mid-scanline error is invisible to a fast emulator by construction — which is
exactly why TerminalGB carries two picture engines rather than one.

The **`standard`** engine draws a whole scanline in a single step at the end of mode 3,
from whatever the registers hold at that instant. It is fast and it is correct for the
overwhelming majority of software, but it physically cannot represent "the wrong tile
source for one dot in the middle of a line" — it never looks at the registers mid-line.
The **`identical`** engine walks the real hardware pixel pipeline dot by dot: the
background fetcher, the eight-pixel FIFO, sprite fetches, the window restart, the `SCX &
7` discard. A mid-scanline write lands exactly where a Game Boy puts it — which means a
one-dot timing bug lands exactly there too, and gets caught.

The two are not a quality or an appearance setting. On ordinary games they produce
byte-identical framebuffers — verified across 600 frames of dmg-acid2 plus Blargg's
`cpu_instrs`. The only axis between them is exactness against speed:

<div class="table-wrap">
  <table>
    <thead>
      <tr>
        <th>Test suite</th>
        <th class="num"><code>standard</code></th>
        <th class="num"><code>identical</code></th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Mooneye GB acceptance</td><td class="num">67 / 75</td><td class="num">75 / 75</td></tr>
      <tr><td>Mealybug Tearoom (pixel-exact rows)</td><td class="num">3 / 79</td><td class="num">29 / 79</td></tr>
      <tr><td>Gambatte (5,225 scored rows)</td><td class="num">3,176</td><td class="num">3,622</td></tr>
      <tr><td>GBMicrotest</td><td class="num">252 / 513</td><td class="num">339 / 513</td></tr>
      <tr><td>GB Emulator Shootout (264 rows)</td><td class="num">223</td><td class="num">243</td></tr>
      <tr><td>Frame cost, Pokémon Blue (one P-core)</td><td class="num">0.094 ms</td><td class="num">0.373 ms</td></tr>
    </tbody>
  </table>
</div>

The accurate engine costs roughly four times as much per frame — 0.373 ms against 0.094
ms, still only a couple of percent of a frame's budget on a desktop core. That is cheap
enough to be the default, and it is: `identical` has been the shipping default since it
stopped losing accuracy rows the fast engine kept. But four times the cost is not free
everywhere. On the PSP frontend, where the CPU budget is tight, the emulator
deliberately pins `standard` — an unplayable-but-exact picture helps no one.

That is the whole reason the split exists. The fast engine is what makes the emulator
usable on modest hardware; the accurate engine is what makes a bug like this one
*findable*. Ship only the fast one and the double-speed stripe would still be on screen,
unmeasured and unfixed, because nothing in the pipeline would ever have looked closely
enough to see it.

</section>
