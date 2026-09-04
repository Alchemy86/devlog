---
title: 'The trap was always on the map'
tag: 'AgentGB'
kicker: 'Control flow · diagnosis'
card_kicker: 'Control flow &middot; diagnosis'
eyebrow: 'AgentGB · Diagnosis'
description: >-
  Collapsing the student into one compiled file did not break him. It changed which way he
  walked, and the new way went through a fault that had been sitting in the shared control
  flow all along.
og_title: >-
  The trap was always on the map
og_description: >-
  A faithful copy of the student finished 0 of 10 cold boots where the original finished 8.
  The copy was not the bug. It was the instrument that found one.
dek: >-
  A compiled copy of the student finished 0 of 10 cold boots where the original finished 8.
  Nothing was retrained and the two paths pick the identical button a thousand times running.
  The obvious conclusion &mdash; the new thing is broken &mdash; was wrong.
lead: >-
  The student had two ways of being run: one for our own emulator, one for mGBA. They were
  collapsed into a single compiled artefact holding the network and every piece of decision
  logic around it. It was proved byte-identical to the old construction, and then it lost ten
  cold boots out of ten while the thing it was proved identical to won eight.
metrics:
  - num: '0</span><span style="color:var(--ink-soft)">/10'
    label: 'Cold boots finished by the compiled student'
    accent: true
  - num: '8<span style="color:var(--ink-soft)">/10</span>'
    label: 'Finished by the old path — same weights, same settings, paired'
  - num: '0.608'
    label: 'What the battle recogniser reads on an ordinary shop confirmation box'
  - num: '1,000'
    label: 'Paired decisions on which the two paths chose the identical button'
note: >-
  The paired run figures, the 0.608 reading and the decision numbers are AgentGB's own records
  from 2026-09-04, in <code>docs/single-artifact.md</code> and the commit that added
  <code>src/agentgb/artifact_driver.py</code>. The thresholds are read out of
  <code>data/transitional-goals.json</code>; the thousand-decision equivalence check is
  <code>tools/test_artifact_driver.py</code>, re-run for this post. The project is on the <a
  href="../projects/agentgb.html">AgentGB project page</a>.
---

<section class="prose" markdown="1">

## Ten cold boots, none of them finished

The paired comparison was the ordinary kind: same weights, same sampling settings, same
chain, ten cold boots each, one path against the other. The compiled artefact finished
**0 of 10**. The flexible construction it was built to replace finished **8 of 10**.

On mGBA, three boots each: the old foreign driver **2 of 3**, the artefact **0 of 3**, all
three of them stranded at 20 or 21 of the chain's 25 links, in the same shop.

There is an obvious reading of those numbers and it was available immediately. One thing
changed, that thing is an ONNX export, ONNX exports are fiddly, file it as "the compiled
graph is wrong" and move on. That reading is wrong, and the only reason it did not get
filed is that somebody went and measured the actual frame the runs were dying on instead of
reasoning about which component was newest.

</section>

<section class="prose" markdown="1">

## Nothing was retrained

Worth stating plainly, because everything after it depends on it.

The collapse compiles the base network, every recogniser and adapter the running config
needs, and the control flow itself — the sticky chain's latch and successor walk, a
transient goal's scope and eligibility, a chamber's arm and disarm, a battle hold's
patience counter — into one graph. `src/agentgb/artifact_driver.py` is the only place
either runner touches it: build the observation, hand it over with the previous decision's
state, take back the action and the next state. No latch logic left in the runners at all.

The weights file is untouched. Same sha256 before and after. It is a compile of what
already existed, not a rebuild of it, and the guard that proves it picks the same buttons
runs a thousand paired decisions of synthetic noise across five seeds — three greedy, two
sampled with the production confidence gate and decay — with zero disagreements, latch
state and held stage included.

So: two paths, provably identical on every decision anyone had checked, one of them
winning eight runs and the other winning none.

</section>

<section class="prose" markdown="1">

## New does not mean guilty

The runs were all dying in the same place, so the frame they were dying on was the thing to
look at.

`battle-on-screen-recognizer` — the shared network that answers "is a battle still
happening" — reads **0.608** on an ordinary shop purchase-confirmation box. Not a near-tie
against its threshold. A confident, wrong yes, on a screen with no battle anywhere in it.
The dialogue box in a shop confirmation is a black-bordered text box, and so is the one in
a fight.

That reading was taken by calling the real, native network directly on the real frame, with
no ONNX runtime involved in the measurement at all. The compiled graph is not in the
picture. The fault is in the shared control flow both paths run, and it was in there before
the collapse was written.

<div class="pullquote">
  <p>The compiled version did not add a fault. It changed the route, and the new route went
  through one.</p>
</div>

</section>

<section class="prose" markdown="1">

## Two thresholds on one network, and the loose one is the one that gets fooled

The battle wheel asks that recogniser two different questions with two different bars.

To *enter* a hold, the entry gate wants **0.999**. To *release* one, the end condition
checks the same network against **0.5**, holding while it stays above, with a release
patience of 24 decisions. Both `battle-hold-trainer` and `battle-hold-wild` share that
gate.

A phantom battle at 0.608 can never start a hold. It clears 0.5 comfortably, and 0.999 not
at all. What it can do is keep a dead one alive.

A real rival fight around decision 201 leaves the trainer hold latched with its miss counter
climbing normally — 606, 608, and onward to 630 by decision 1092, far past a patience of 24.
It never expires, because every time the run walks back into a shop and reads a
confirmation box, the same shared gate says 0.608, the counter resets to zero, and the stale
hold re-arms. The trainer battle's adapter — not the walking adapter the chain has long
since moved on to — keeps pressing through the shop's confirmation screens, buying one
item at a time until the wallet is empty and the chain stalls.

Every part of that is reachable by the old path too. It is one recogniser, one threshold
and one counter, all of them shipped and certified long before this task started.

</section>

<section class="prose" markdown="1">

## A difference too small to fail a check, and large enough to change the route

The graph is verified against a numpy reference that re-implements the same control flow,
and the check it has to pass is a maximum absolute difference in the logits below `1e-3`.
It passes. onnxruntime and native numpy do not compute a convolution to the last bit, and
sub-`0.001` is a reasonable place to draw the line.

It is also enough to flip a near-tied argmax, which was confirmed directly at decision 546
of a real run: `up` against `right`, the pick depending on which backend did the arithmetic,
with no goal latched on either driver. No control-flow machinery active. Just the base
network, two backends, and a tie broken two different ways.

From there the trajectories are simply different runs. The artefact's route revisits the
shop while that stale hold has not yet expired far more often than the flexible driver's
route does, on these ten seeds. Same map, different walk. Sharing the RNG stream between
the two drivers was tried and removes one source of divergence; the identical N=10
comparison with it enabled still returns 0/10, because the argmax flip is not an RNG
question.

</section>

<section class="prose" markdown="1">

## A faithful copy is a measuring instrument

The useful thing here is not the bug. It is what the pair of paths turned out to be good
for.

Two implementations that provably agree on every decision in isolation diverged completely
in practice, and the divergence carried information. The synthetic checks could not have
found this, and it is clear why once you look at them: random noise never triggers a real
battle, and the graph's own verification forces a handful of degenerate frames, never a
multi-thousand-decision sequence with a real fight followed by a real shop visit. Neither
check is weak. They answer a different question from "safe to drive a long chain run
with".

The 8-out-of-10 was the misleading number. Eighty per cent looks like a spread of ordinary
bad luck, and it was concealing a specific trap that the winning route happened to miss
most of the time. It took a harmless numerical nudge — small enough to pass every
tolerance the project sets — to make the trap show up ten times out of ten. A rate that
good can hide a fault this sharp, and the way it stopped hiding was a second
implementation walking a slightly different line through the same map.

`--use-artifact` is an explicit flag rather than the default because of that measurement.
The first design routed to the artefact automatically whenever the goal set and the policy
matched what it was compiled for. A plain run today is byte-for-byte what it was before
any of this.

</section>

<section class="prose" markdown="1">

## What is still open

The fix is not written. There are two candidates and they are not the same fix.

The first is that the recogniser never learned what a shop confirmation box looks like —
it was trained to tell battle screens from the rest of the game, and a black-bordered
dialogue in a shop is a negative it apparently never saw enough of. That is answered with
frames and a retrain.

The second is that the hold is wrong to re-arm off a single frame at all, whatever the
recogniser says. A patience counter that resets to zero on one reading above a loose
threshold has no memory of having climbed to 630, and a mechanism that can be revived by
one frame of noise is fragile even when the network under it is right.

A crew is deciding between them on evidence now. Until it lands, the collapsed path stays
behind its flag and out of the promotion workflow, because promoting it would mean shipping
a route that walks into this reliably.

</section>
