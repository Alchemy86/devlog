---
title: 'The transfer controller owns the bus'
tag: 'TerminalGB'
kicker: 'OAM DMA · PPU'
card_kicker: 'Hardware modelling'
eyebrow: 'TerminalGB · Hardware modelling'
order: 15
description: >-
  Object DMA is usually modelled as a copy that blocks the CPU. It is also an address-bus
  conflict, and the sprite scan is on the other end of those lines.
dek: >-
  Object DMA is usually modelled as a copy. It is also an address-bus conflict, and the sprite
  scan is on the other end of those lines.
lead: >-
  Object DMA — the routine every Game Boy game uses to push sprite data into object memory —
  is usually modelled as a copy that takes 640 cycles and locks the CPU out of most of the
  memory map. That is the data half of one physical rule. The address half is the interesting
  one.
metrics:
  - num: '238 → <span class="accent">239</span>'
    label: 'Shootout, of 264'
  - num: '3,613 → 3,617'
    label: 'Gambatte rows'
  - num: '0'
    label: 'Rows lost'
  - num: '80'
    label: 'Dots the scan reads nothing'
note: >-
  The sweep and the suite scores are from TerminalGB's own conformance baselines, re-run in
  CI. The Shootout figure is measured through the Shootout's own published manifest.
---

<section class="prose" markdown="1">

The transfer controller has no address bus of its own. While a transfer runs it drives
the object-memory address lines — and the picture processor's object scan is on the
other end of them.

So for the eighty dots of the scan the PPU cannot read a single entry. Its Y/X latch
keeps whatever it last held, and all forty object slots are judged against that one
stale pair.

Modelling that took the Shootout from 238 to 239 of 264 and Gambatte from 3,613 to 3,617
scored rows, with zero losses and everything else byte-identical on both picture
engines. One row — but it was `ashiepaws/strikethrough.gb`, the first row that suite has
ever scored here.

</section>

<section class="prose" markdown="1">

## The constant was derived, not chosen

The controller takes the bus a fixed number of dots after the write to `$FF46`, and that
number is the one free parameter in the whole model. It came out of eight ROMs.

Gambatte's `late_sp{00,01,02,39}x_{1,2}` each put the write one machine cycle either
side of one scan slot. `sp00x_2` finds object 0 while `sp01x_1` misses object 1, which
brackets the arm. The `sp02x`/`sp39x` pair — same DMA phase, different slot — rules out
every uniform shift.

Then it was swept across the whole 811-row `oamdma/` group:

<div class="table-wrap">
  <table>
    <thead>
      <tr><th>Arm delay (dots)</th><th class="num">0</th><th class="num">1</th><th class="num">2</th><th class="num">3</th><th class="num">4</th></tr>
    </thead>
    <tbody>
      <tr><td>Gambatte <span class="mono">oamdma/</span> rows passing, of 811</td><td class="num">742</td><td class="num"><strong>744</strong></td><td class="num"><strong>744</strong></td><td class="num">738</td><td class="num">738</td></tr>
    </tbody>
  </table>
</div>

The scan reads on even dots, so 1 and 2 are the same machine. A curve with a flat top
two dots wide, and a physical reason for the width — that is what a derived constant
looks like, as opposed to the one value that made a favourite test go green.

</section>

<section class="prose" markdown="1">

## The data half came first, and was worth four hundred rows

Three days earlier the same physical rule was modelled from the other side: while the
transfer runs, the CPU and the controller share one bus, so the CPU's reads of most of
the map come back as whatever the transfer is putting on it.

Gambatte went from 2,682 to 3,083 of the rows scored at the time. Four hundred rows,
from modelling a bus conflict instead of a copy.

<div class="pullquote">
  <p>
    A peripheral that moves bytes is doing two things at once, and only one of them
    is the copy.
  </p>
</div>

</section>

<section class="prose" markdown="1">

## And then a sibling project found the flag

[GBSelfTest](../projects/gbselftest.html)'s object-DMA check found a real bug in this
model on the day it was written: the flag the PPU keeps about a running transfer was
cleared on one of the two paths that can notice the transfer has ended, and not the
other. Once it latched, the object scan never read object memory again for the rest of
the session.

Thousands of rows across five public suites were byte-identical either way. [Why they
could not see it →](a-hundred-checks-in-one-session.html)

</section>
