---
title: 'Three ways this cartridge was wrong about itself'
tag: 'GBSelfTest'
kicker: 'Self-tests'
card_kicker: 'Corrections'
eyebrow: 'GBSelfTest · Corrections'
order: 23
description: >-
  A verdict decided by which checks failed above it, a subroutine that ate a measurement, and
  two checks that skipped on every console, forever.
lead: >-
  A project whose whole pitch is <em>measure it, do not assume it</em> collects a specific
  kind of failure: the assumption you did not notice you were making. All three of these
  shipped.
note: >-
  All three are written up beside their fixes in GBSelfTest's own notes, with the emulator
  revisions each disagreement was observed on.
---

<section class="prose" markdown="1">

## The run decided the verdict, not the machine

`GB-CYC-07` shipped once in a form that zeroed the timer counter and then restarted the
divider. Three cycles separate those two writes, and whether the tapped bit falls inside
them depends on the counter phase the check was entered in — which is set by how much
code ran above it.

So the verdict was decided by which checks failed earlier. It passed on one emulator and
failed on SameBoy, and swapping the earlier failures swapped the answer.

Restart the counter first and zero the timer after it, and sweep more than one delay
rather than sampling once. Anything that reads a timer edge and does not do both is
measuring the rest of the run.

</section>

<section class="prose" markdown="1">

## A subroutine that quietly ate the measurement

`FlipSpeed` runs the documented STOP-based speed-switch sequence and, like every
subroutine in that file, makes no promise about which registers survive it. It loads `A`
repeatedly on the way through.

A check that measured something into `A`, called `FlipSpeed` to return to the starting
speed, then compared against `A`, was comparing `FlipSpeed`'s own leftover value.

It does so silently, producing a plausible and constant wrong number rather than a
crash. It shipped in `GB-PPU-07`'s double-speed half and was caught only because the
wrong number (`$1`) disagreed with an independent measurement on two unrelated emulators
that had already established the right one (`$2`).

</section>

<section class="prose" markdown="1">

## Two checks that skipped on every console, forever

This is the best of the three, because nothing about it looks wrong.

The build did not pass `rgbfix -c`, so the ROM's header byte at `$0143` was `$00` — and
a real Color console boots a cartridge with no Color flag into DMG compatibility mode,
where `KEY1` and double speed do not exist at all.

Meanwhile the cartridge's own console detection still correctly reported CGB, because it
reads the boot handover registers, which do not care about the cartridge's header.

So a double-speed check written the ordinary way built, linked, and skipped on every
run, on every console, forever. Nothing looked wrong until somebody specifically asked
whether it had ever run. Confirmed by building both ways and watching `GB-CYC-09` and
`GB-PPU-07` go from permanently-skip to actually-run, with no change to any other
check's verdict on any console.

<div class="callout">
  <p class="eyebrow">Which is why a skip is counted separately</p>
  <p>
    A skip is not a pass, and it is not a failure either. Each one prints its own
    reason in the run, so a skipped row is never silent — and two of the 102 do not
    judge at all: they report, printing the number they saw and leaving the verdict
    to a reader who has real hardware, because no published reference settles what
    the right answer is.
  </p>
</div>

</section>
