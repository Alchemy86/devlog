---
title: 'A hundred checks in one session'
tag: 'GBSelfTest'
kicker: 'Object DMA'
card_kicker: 'Test design'
eyebrow: 'GBSelfTest · Test design'
order: 22
description: >-
  A new check found a real bug in TerminalGB on the day it was written — one that thousands of
  rows across five public suites could not see, because of the shape they have.
dek: >-
  A new check found a real bug on the day it was written — one that thousands of rows across
  five public suites could not see, because of the shape they have.
lead: >-
  <code>GB-DMA-06</code> found a real bug in <a
  href="../projects/terminalgb.html">TerminalGB</a> the day it was written. Every public suite
  that emulator gates on was byte-identical either way — thousands of rows across Gambatte,
  Mooneye, Mealybug, SameSuite and the c-sp aggregation.
metrics:
  - num: '192 / 550'
    label: 'Frames of a real cartridge affected'
  - num: '0'
    label: 'Public suite rows that moved'
    accent: true
  - num: '1'
    label: 'Latched flag'
  - num: '102'
    label: 'Checks in one session'
note: >-
  The frame count comes from the TerminalGB run that reproduced the fault. The check is
  <code>GB-DMA-06</code> in GBSelfTest's own registry.
---

<section class="prose" markdown="1">

## The fault

A flag the picture processor keeps about a running object transfer was cleared on one of
the two paths that can notice the transfer has ended, and not the other. The idle arm's
own comment claimed the default machine never reached it.

It does reach it. The transfer's last machine cycle leaves the position counter at its
limit inside the bus tick without the flag moving, so the instruction's remainder is
where the transfer gets noticed to be over.

Once the flag latched, the object scan **never read object memory again for the rest of
the session** — 192 of 550 frames of a real cartridge.

</section>

<section class="prose" markdown="1">

## Why a suite of short ROMs cannot see it

Each one boots, measures one thing and stops. A latch that needs a transfer to end on an
instruction boundary and a scan to follow it never gets the chance.

That is not a criticism of those suites. It is a property of their shape.

<div class="pullquote">
  <p>
    A cartridge that runs a hundred checks back to back in one session is a shape no
    test ROM has.
  </p>
</div>

</section>

<section class="prose" markdown="1">

## The check itself, which is a nice piece of indirection

A cartridge cannot see which objects the scan found. What it *can* see is how long mode
3 took, and ten objects on a line cost the fetcher at least sixty dots.

So: leave object memory entirely empty, put the visible objects in the transfer's
source, and start the transfer so it covers the measured line's scan. A machine whose
scan reads object memory straight through the transfer finds the ten objects the
transfer has already written and is still drawing them. Hardware finds none and is
already in horizontal blank.

Two details are load-bearing rather than decorative. Object memory is left empty on
purpose, so whatever slot the scan last managed to read, it read a zero — the frozen Y
puts the phantom object above the screen, and the check does not depend on where the
freeze landed. And the transfer is sourced from video memory rather than work memory,
because on a monochrome console work memory sits on the cartridge's own bus and a
transfer out of it would feed the processor its own bytes instead of instructions. That
is why every real game's transfer routine lives in high RAM.

</section>

<section class="prose" markdown="1">

## The rule it left behind

When a check is written, run the whole cartridge and read the total, not just that
check's line. A new check that passes in isolation and moves an unrelated area's verdict
has found something.

</section>
