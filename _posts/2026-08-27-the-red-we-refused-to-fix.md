---
title: 'The red we refused to fix'
tag: 'TerminalGB'
kicker: 'Calibration'
card_kicker: 'Method'
eyebrow: 'TerminalGB · Method'
order: 16
description: >-
  One sweep would have turned a failing test green. Taking it would have moved every Color
  cartridge's divider on the evidence of a single row.
lead: >-
  <code>csp/bully</code> shows a black screen. It comes down to one failing check — the
  Color-mode boot system counter — and there is an obvious way to fix it: sweep the counter
  until bully goes green. It was not taken, and not out of timidity.
note: >-
  Every suite score here is from TerminalGB's own checked-in conformance baselines, re-run in
  CI on every push and red on a change in either direction.
---

<section class="prose" markdown="1">

## Why sweeping would have been wrong

Bully waits for `LY >= $90` before reading the divider. So what it pins is not the
counter. It is the *phase between the system counter and the picture processor* at boot
hand-off — two unknowns multiplied together.

And no published ROM measures where a Color boot ROM leaves the PPU for a Color
cartridge. Fitting one unknown to absorb another would have moved every Color
cartridge's divider, and with it its audio phase and its random number generator, on the
evidence of one row.

<div class="pullquote">
  <p>
    A test going green is not evidence when the change that made it green touched
    two things and the test only measures their product.
  </p>
</div>

</section>

<section class="prose" markdown="1">

## The counter did change, later, for a different reason

A second independent source arrived. Gambatte's `div/start_inc_{1,2}_cgb04c` take the
genuine Color path and pin both the divider's value *and* the exact machine cycle its
low byte wraps on, at a fixed distance with no `LY` wait.

So they measure the counter alone — precisely the confound the original objection named.
The constant moved on their evidence.

Bully's row is still red, byte-identical in both picture modes, because the PPU half is
untouched. Two crews' work settled half a question; the other half is still open, and
the red row is what says so.

</section>

<section class="prose" markdown="1">

## The other red that stays

Blargg's `oam_bug` fails on a Color console here. All eight sub-tests pass on DMG, where
the object-memory corruption defect is modelled faithfully. Color silicon has no such
defect, so real hardware fails that ROM too. Passing it would be the bug.

Both rows are kept on the board rather than excluded, because a suppressed red is
indistinguishable from a fixed one six months later.

</section>
