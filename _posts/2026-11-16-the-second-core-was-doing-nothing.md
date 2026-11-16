---
date: 2026-11-16 22:00:00 +0000
title: 'The second core was doing nothing'
tag: 'Pokewalker'
kicker: 'Software · Performance'
card_kicker: 'Software'
eyebrow: 'Pokewalker · Performance'
description: >-
  The walker now runs two to three times faster on the real board. The walking face went
  from 13.8 to 39.7 frames a second and the open world roughly doubled, by giving the
  ESP32-S3's idle second core the panel, the sensors and half the ground. Not one pixel
  changed.
lead: >-
  The walker's chip has two cores. One of them drew the picture, encoded it, sent it to
  the screen and read the touch panel, one job after another. The other played the
  speaker and spent nine tenths of its time waiting. Now they share the frame.
metrics:
  - num: '13.8 → 39.7'
    label: 'Walking face, frames a second'
    accent: true
  - num: '18.8 → 2.7 ms'
    label: 'Encoding a frame'
  - num: '0'
    label: 'Pixels changed'
note: >-
  Every figure is from the real board, three runs a screen. The frames compared are the
  software's own canvas; the panel itself has not yet been checked by eye since the change.
---

<section class="prose" markdown="1">

The walker is an ESP32-S3 behind a round 412×412 screen. The software draws a 103×103
picture and the board scales it up four times, so every dot is a crisp 4×4 block. Until
today that ran at about 13 frames a second on the walking face and 7 or 8 in the open
world.

It now runs at 39.7 on the walking face, 36.5 with the closed ball spinning, and 14 to 19
across the open world. The drawing code did not get faster. The time went to the second
core.

</section>

<figure class="scrollfig" aria-labelledby="fig-fps-cap">
  <svg viewBox="0 0 720 406" role="img" aria-labelledby="fps-title" xmlns="http://www.w3.org/2000/svg" font-family="'JetBrains Mono', monospace">
      <title id="fps-title">Frames a second on the board, before and after, for eight screens</title>
      <style>
        .gl { stroke: var(--hairline); stroke-width: 1; }
        .ax { fill: var(--ink-soft); font-size: 10px; }
        .lb { fill: var(--ink); font-size: 11.5px; }
        .b0 { fill: var(--ink-soft); }
        .b1 { fill: var(--accent); }
        .v0 { fill: var(--ink-soft); font-size: 10px; }
        .v1 { fill: var(--ink); font-size: 10.5px; font-weight: 700; }
        .lg { fill: var(--ink-soft); font-size: 10.5px; font-weight: 700; letter-spacing: .08em; }
      </style>
      <rect x="200" y="14" width="12" height="12" rx="2" class="b0"/><text x="218" y="24" class="lg">BEFORE</text>
      <rect x="290" y="14" width="12" height="12" rx="2" class="b1"/><text x="308" y="24" class="lg">AFTER</text>
      <line x1="200.0" y1="46" x2="200.0" y2="372" class="gl"/><text x="200.0" y="388" text-anchor="middle" class="ax">0</text>
      <line x1="315.0" y1="46" x2="315.0" y2="372" class="gl"/><text x="315.0" y="388" text-anchor="middle" class="ax">10</text>
      <line x1="430.0" y1="46" x2="430.0" y2="372" class="gl"/><text x="430.0" y="388" text-anchor="middle" class="ax">20</text>
      <line x1="545.0" y1="46" x2="545.0" y2="372" class="gl"/><text x="545.0" y="388" text-anchor="middle" class="ax">30</text>
      <line x1="660.0" y1="46" x2="660.0" y2="372" class="gl"/><text x="660.0" y="388" text-anchor="middle" class="ax">40</text>
      <text x="660" y="402" text-anchor="end" class="ax">frames a second</text>
      <g><title>Closed ball, spinning: 13.2 fps before, 36.5 after (2.8x)</title>
        <text x="190" y="75" text-anchor="end" class="lb">Closed ball, spinning</text>
        <rect x="200" y="58" width="151.8" height="12" rx="2" class="b0"/><text x="356.8" y="68" class="v0">13.2</text>
        <rect x="200" y="72" width="419.8" height="12" rx="2" class="b1"/><text x="624.8" y="82" class="v1">36.5</text>
      </g>
      <g><title>Walking face: 13.8 fps before, 39.7 after (2.9x)</title>
        <text x="190" y="115" text-anchor="end" class="lb">Walking face</text>
        <rect x="200" y="98" width="158.7" height="12" rx="2" class="b0"/><text x="363.7" y="108" class="v0">13.8</text>
        <rect x="200" y="112" width="456.6" height="12" rx="2" class="b1"/><text x="661.5" y="122" class="v1">39.7</text>
      </g>
      <g><title>Quick battle: 12.1 fps before, 24.3 after (2.0x)</title>
        <text x="190" y="155" text-anchor="end" class="lb">Quick battle</text>
        <rect x="200" y="138" width="139.2" height="12" rx="2" class="b0"/><text x="344.1" y="148" class="v0">12.1</text>
        <rect x="200" y="152" width="279.4" height="12" rx="2" class="b1"/><text x="484.4" y="162" class="v1">24.3</text>
      </g>
      <g><title>Park plaza: 8.1 fps before, 15.1 after (1.9x)</title>
        <text x="190" y="195" text-anchor="end" class="lb">Park plaza</text>
        <rect x="200" y="178" width="93.1" height="12" rx="2" class="b0"/><text x="298.1" y="188" class="v0">8.1</text>
        <rect x="200" y="192" width="173.7" height="12" rx="2" class="b1"/><text x="378.6" y="202" class="v1">15.1</text>
      </g>
      <g><title>Gate road, standing: 7.5 fps before, 15.7 after (2.1x)</title>
        <text x="190" y="235" text-anchor="end" class="lb">Gate road, standing</text>
        <rect x="200" y="218" width="86.2" height="12" rx="2" class="b0"/><text x="291.2" y="228" class="v0">7.5</text>
        <rect x="200" y="232" width="180.5" height="12" rx="2" class="b1"/><text x="385.5" y="242" class="v1">15.7</text>
      </g>
      <g><title>Gate road, walking: 6.7 fps before, 14.1 after (2.1x)</title>
        <text x="190" y="275" text-anchor="end" class="lb">Gate road, walking</text>
        <rect x="200" y="258" width="77.0" height="12" rx="2" class="b0"/><text x="282.1" y="268" class="v0">6.7</text>
        <rect x="200" y="272" width="162.2" height="12" rx="2" class="b1"/><text x="367.1" y="282" class="v1">14.1</text>
      </g>
      <g><title>Cerulean, standing: 7.3 fps before, 15.4 after (2.1x)</title>
        <text x="190" y="315" text-anchor="end" class="lb">Cerulean, standing</text>
        <rect x="200" y="298" width="84.0" height="12" rx="2" class="b0"/><text x="288.9" y="308" class="v0">7.3</text>
        <rect x="200" y="312" width="177.1" height="12" rx="2" class="b1"/><text x="382.1" y="322" class="v1">15.4</text>
      </g>
      <g><title>Cerulean, walking: 8.7 fps before, 19.0 after (2.2x)</title>
        <text x="190" y="355" text-anchor="end" class="lb">Cerulean, walking</text>
        <rect x="200" y="338" width="100.0" height="12" rx="2" class="b0"/><text x="305.1" y="348" class="v0">8.7</text>
        <rect x="200" y="352" width="218.5" height="12" rx="2" class="b1"/><text x="423.5" y="362" class="v1">19.0</text>
      </g>
    </svg>
  <figcaption id="fig-fps-cap">
    Frames a second on the board, three runs each. The gate road and Cerulean are two places
    in the open region around the park, measured standing still and walking.
  </figcaption>
</figure>

<section class="prose" markdown="1">

## Where a frame went

The first change was a line of numbers. Every few seconds the board now prints how long
each part of the frame took. On the closed ball it read: 23.2 ms drawing, 18.8 ms
encoding the picture into the panel's colour format, 19.2 ms sending it, and 11.3 ms
reading the touch panel. All on core 0, in a row.

Core 1 ran the speaker and nothing else. It was idle about 90% of the time.

</section>

<figure class="scrollfig" aria-labelledby="fig-tl-cap">
  <svg viewBox="0 0 720 360" role="img" aria-labelledby="tl-title" xmlns="http://www.w3.org/2000/svg" font-family="'JetBrains Mono', monospace">
      <title id="tl-title">One frame on the closed ball, before and after: four jobs in a row on core 0, then core 0 drawing while core 1 sends</title>
      <style>
        .sg { fill: var(--code-bg); stroke: var(--hairline); stroke-width: 1.5; }
        .dr { fill: var(--card); stroke: var(--accent); stroke-width: 2; }
        .id { fill: none; stroke: var(--hairline); stroke-width: 1.5; stroke-dasharray: 4 4; }
        .st { fill: var(--ink); font-size: 11px; font-weight: 700; }
        .sm { fill: var(--ink-soft); font-size: 10px; }
        .ln { fill: var(--ink); font-size: 11px; font-weight: 700; }
        .hd { fill: var(--accent); font-size: 10.5px; font-weight: 700; letter-spacing: .1em; }
        .gl { stroke: var(--hairline); stroke-width: 1; }
        .ax { fill: var(--ink-soft); font-size: 10px; }
        .fr { stroke: var(--ink); stroke-width: 2; }
      </style>
      <text x="8" y="18" class="hd">BEFORE — 13.2 FRAMES A SECOND</text>
      <text x="8" y="51" class="ln">core 0</text>
      <rect x="120.0" y="30" width="166.2" height="34" rx="4" class="dr"/>
      <text x="204.1" y="45" text-anchor="middle" class="st">draw</text>
      <text x="204.1" y="58" text-anchor="middle" class="sm">23.2 ms</text>
      <rect x="288.2" y="30" width="134.3" height="34" rx="4" class="sg"/>
      <text x="356.4" y="45" text-anchor="middle" class="st">encode</text>
      <text x="356.4" y="58" text-anchor="middle" class="sm">18.8 ms</text>
      <rect x="424.5" y="30" width="137.2" height="34" rx="4" class="sg"/>
      <text x="494.1" y="45" text-anchor="middle" class="st">send</text>
      <text x="494.1" y="58" text-anchor="middle" class="sm">19.2 ms</text>
      <rect x="563.7" y="30" width="79.9" height="34" rx="4" class="sg"/>
      <text x="604.7" y="45" text-anchor="middle" class="st">touch</text>
      <text x="604.7" y="58" text-anchor="middle" class="sm">11.3 ms</text>
      <rect x="645.6" y="30" width="52.4" height="34" rx="4" class="dr"/>
      <line x1="644.6" y1="24" x2="644.6" y2="70" class="fr"/>
      <text x="8" y="95" class="ln">core 1</text>
      <rect x="120.0" y="74" width="578.0" height="34" rx="4" class="id"/>
      <text x="410.0" y="95" text-anchor="middle" class="sm">speaker only, idle about 90% of the time</text>
      <text x="8" y="160" class="hd">AFTER — 36.5 FRAMES A SECOND</text>
      <text x="8" y="193" class="ln">core 0</text>
      <rect x="120.0" y="172" width="169.1" height="34" rx="4" class="dr"/>
      <text x="205.6" y="187" text-anchor="middle" class="st">draw</text>
      <text x="205.6" y="200" text-anchor="middle" class="sm">23.6 ms</text>
      <line x1="317.6" y1="166" x2="317.6" y2="212" class="fr"/>
      <rect x="318.6" y="172" width="169.1" height="34" rx="4" class="dr"/>
      <text x="404.2" y="187" text-anchor="middle" class="st">draw</text>
      <text x="404.2" y="200" text-anchor="middle" class="sm">23.6 ms</text>
      <line x1="516.3" y1="166" x2="516.3" y2="212" class="fr"/>
      <rect x="517.3" y="172" width="169.1" height="34" rx="4" class="dr"/>
      <text x="602.8" y="187" text-anchor="middle" class="st">draw</text>
      <text x="602.8" y="200" text-anchor="middle" class="sm">23.6 ms</text>
      <text x="8" y="237" class="ln">core 1</text>
      <rect x="298.4" y="216" width="17.6" height="34" rx="4" class="sg"/>
      <rect x="317.9" y="216" width="111.8" height="34" rx="4" class="sg"/>
      <text x="374.8" y="231" text-anchor="middle" class="st">send</text>
      <text x="374.8" y="244" text-anchor="middle" class="sm">15.7 ms</text>
      <rect x="497.0" y="216" width="17.6" height="34" rx="4" class="sg"/>
      <rect x="516.6" y="216" width="111.8" height="34" rx="4" class="sg"/>
      <text x="573.5" y="231" text-anchor="middle" class="st">send</text>
      <text x="573.5" y="244" text-anchor="middle" class="sm">15.7 ms</text>
      <text x="298.4" y="266" class="sm">encode 2.7 ms</text>
      <text x="120.0" y="286" class="sm">touch and motion sensor read here, during the draw</text>
      <rect x="141.8" y="216" width="6" height="34" rx="2" class="sg"/>
      <rect x="185.2" y="216" width="6" height="34" rx="2" class="sg"/>
      <rect x="228.8" y="216" width="6" height="34" rx="2" class="sg"/>
      <line x1="120.0" y1="316" x2="120.0" y2="322" class="gl"/><text x="120.0" y="336" text-anchor="middle" class="ax">0</text>
      <line x1="192.5" y1="316" x2="192.5" y2="322" class="gl"/><text x="192.5" y="336" text-anchor="middle" class="ax">10</text>
      <line x1="265.0" y1="316" x2="265.0" y2="322" class="gl"/><text x="265.0" y="336" text-anchor="middle" class="ax">20</text>
      <line x1="337.5" y1="316" x2="337.5" y2="322" class="gl"/><text x="337.5" y="336" text-anchor="middle" class="ax">30</text>
      <line x1="410.0" y1="316" x2="410.0" y2="322" class="gl"/><text x="410.0" y="336" text-anchor="middle" class="ax">40</text>
      <line x1="482.5" y1="316" x2="482.5" y2="322" class="gl"/><text x="482.5" y="336" text-anchor="middle" class="ax">50</text>
      <line x1="555.0" y1="316" x2="555.0" y2="322" class="gl"/><text x="555.0" y="336" text-anchor="middle" class="ax">60</text>
      <line x1="627.5" y1="316" x2="627.5" y2="322" class="gl"/><text x="627.5" y="336" text-anchor="middle" class="ax">70</text>
      <line x1="700.0" y1="316" x2="700.0" y2="322" class="gl"/><text x="700.0" y="336" text-anchor="middle" class="ax">80</text>
      <line x1="120.0" y1="316" x2="700.0" y2="316" class="gl"/>
      <text x="700.0" y="352" text-anchor="end" class="ax">milliseconds · a vertical line starts the next frame</text>
    </svg>
  <figcaption id="fig-tl-cap">
    One frame on the closed ball, to scale. Before, core 0 does four jobs in a row. After,
    it only draws, and core 1 encodes and sends the last frame while the next is drawn.
  </figcaption>
</figure>

<section class="prose" markdown="1">

## One table instead of a lookup per pixel

The canvas stores each pixel as one of 256 shades. Turning a shade into the bytes the
panel wants meant working out its colour every time, for every pixel. But within one frame a
shade is always the same colour.

So once a frame the walker builds a table: all 256 shades, each already encoded as the
four panel dots it becomes. A row of the picture is then a run of table lookups.
Encoding fell from 18.8 ms to 2.5 ms on that change alone.

## Sending from the other core

This was the biggest win. When core 0 finishes a picture, it copies the canvas into a
snapshot in PSRAM and posts it to core 1 through a one-slot mailbox. Then it goes straight
on to the next frame. Core 1 encodes the snapshot band by band and puts it on the wire.

Neither side takes a lock. Core 0 only writes the mailbox when it is empty, and core 1
only reads it when it is full. Core 1 never prints either, so when a save to flash parks
it mid-frame, the frame is late and nothing else happens.

The bytes on the wire are the same as before: the same windows, the same transactions, in
the same order. Only the core sending them changed.

Then the band buffers were doubled. Each band now goes out as two halves from two pairs of
DMA buffers, so the next half is encoded while the last one is on the wire.

There is a floor here. The panel's bus runs at 40 MHz on four lanes, the ceiling its
datasheet gives for it, and a full 412×412 frame takes about 16 ms to cross it. The send is now
15.7 ms. That is the bus, not the code.

## Sharing the ground

The open world spends most of its frame on the ground: the grass, paths and water drawn
row by row in perspective. Those rows do not depend on each other, so the two cores can
split them.

Both cores take the next row from one shared counter until none are left. Each row is
written into a buffer, and when every row is done, core 0 copies them into the canvas in
the same order, left to right and top to bottom, that the one-core drawing uses. The
picture cannot change, only when it is ready.

With this and the changes above, the park plaza went from 8.1 to 15.1 frames a second. The battle arena's floor is
drawn the same way now, for a smaller gain.

## The one that went backwards

The spinning closed ball got the same treatment and came out slower on the board. Core 1
is busy sending the previous frame for most of the time the ball is being drawn, so
handing it rows only made core 0 wait. It was taken back out.

## Reading the sensors in the gaps

The touch panel and the accelerometer share one I2C bus. They used to be read between
bands of the panel transfer, and the transfer had moved to core 1. Leaving the reads on
core 0 meant none during a long draw, and the open world's draw is 50 ms and more. The
step counter wants a sample at least 25 times a second.

So while core 0 draws, it lends core 1 the bus. Core 1 reads both sensors on the usual
cadence, between its own bands and rows, and keeps each reading with the time it was
taken. When the picture is done, core 0 takes the bus back and replays the readings
through exactly the code it would have run had it read them itself, at those times.

Touch no longer costs core 0 anything: 11.3 ms became 0. The accelerometer is now read at
about 65 times a second everywhere, up from 30 to 38 in the park.

## Nothing on the screen changed

Every golden frame the test suite keeps is unchanged, and so is the hash of the whole
pixel battle. Tests that draw the same pictures with the work split across two threads
get identical frames. The speaker ran through all of it with no underruns.

Those checks read the canvas, the picture as the software holds it. Nobody has yet looked
at the physical panel after this change, so the last step, from the bytes on the wire to
the glass, is still to be seen.

## What is left

- The park's standing objects still take about 27 ms, all on core 0.
- The walking face and the closed ball are now bound by core 0's own draw, about 23 ms.
- The S3's vector instructions have not been tried on any of it.

The battles this speeds up are the ones in [the stadium post](the-stadium-shakes.html),
and the rest of the device is on [the project page](../projects/pokewalker.html).

</section>
