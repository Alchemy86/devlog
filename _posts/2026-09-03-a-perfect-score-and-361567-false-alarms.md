---
title: 'A perfect score and 361,567 false alarms'
tag: 'AgentGB'
kicker: 'Screen triggers · method'
card_kicker: 'Screen triggers &middot; method'
eyebrow: 'AgentGB · Method'
order: 0
description: >-
  A recogniser scored a held-out balanced accuracy of 1.000 and then fired on more than a
  quarter of 1,383,924 frames of real play. Five rounds of training, one of them poisoned by
  the tool's own advice, and the bug that actually ended the runs was mechanical.
og_title: >-
  A perfect score and 361,567 false alarms
og_description: >-
  A recogniser scored a held-out balanced accuracy of 1.000 and then fired on more than a
  quarter of 1,383,924 frames of real play. The method that dug it out is now a written rule.
dek: >-
  A recogniser scored a held-out balanced accuracy of 1.000 and then said <em>yes</em> to
  361,567 of 1,383,924 frames of real play. Five rounds, one of them poisoned by the tool's own
  refusal message &mdash; and the bug that was actually ending runs turned out to have no
  weights in it at all.
lead: >-
  Every recogniser in AgentGB is a two-class network answering one question about the picture
  on screen. The cheapest way to be wrong about one is to trust the score it prints. On
  2026-09-03 the same mistake was made twice in one day, caught twice, and the way it was caught
  both times was somebody dumping the frames out and looking at them.
metrics:
  - num: '1.000'
    label: 'Held-out accuracy of a trigger that fired on 26% of real play'
  - num: '12'
    label: 'False alarms in 1,383,924 frames, after narrowing what it learned from'
    accent: true
  - num: '0.0408'
    label: 'Highest the blamed recogniser ever read in the town it was blamed for'
  - num: '25<span style="color:var(--ink-soft)">/30</span>'
    label: 'Forest crossings once the real bug was found &mdash; 13 gained, none lost'
note: >-
  The figures here come from AgentGB's own records of 2026-09-03 &mdash;
  <code>docs/transitional-goals.md</code>, <code>docs/trainscene.md</code>, and the
  <code>up-route-2-forest-goal-gate-npcbox</code> and <code>forest-walk-npcbox</code> entries in
  <code>data/transitional-goals.json</code>, with the paired 30-run sweeps read back out of
  their own result JSON. The montages are drawn by
  <code>tools/dump_recognizer_positives.py</code> from the corpora each recogniser was trained
  on; game art is Nintendo/Game Freak's, and these frames are documentation of a measurement.
  The wider project is on the <a href="../projects/agentgb.html">AgentGB project page</a>.
---

<section class="prose" markdown="1">

The recogniser had one job: say whether the player is standing in Viridian City. It is the
sight half of a *give-back* — lose a fight in Viridian Forest, the cartridge blacks the party
out two maps away, and the lesson the run had earned is thrown away with it. Hold that lesson
instead, and hand it back the moment he is somewhere it knows.

It scored a held-out balanced accuracy of 1.000.

Then the probe swept it over 1,383,924 frames of real play from 21 links it had never been
trained on. At 0.999 — the tightest threshold in the sweep — it fired on 361,567 of them.
Twenty-six per cent. It had learned to say *yes*.

That is not bad luck, it is the shape of the question. A closed two-class network puts
everything it has never seen into whichever class is broader, and the held-out split is drawn
from the frames it *was* shown, so it cannot contain that failure by construction. Ask *which
place is this* and the broader class is the positive one.

</section>

<section class="prose" markdown="1">

## Five rounds, and the one that made it worse

`agentgb trainscene` refuses by default. It sweeps both bars at every threshold — the pooled
false-alarm rate over real play, and how many genuine occurrences are still caught, counted as
episodes rather than frames — and if no threshold satisfies both it ships nothing and prints
the areas it is confused by. Five rounds of that:

<table>
  <thead>
    <tr>
      <th>Round</th>
      <th>Negatives</th>
      <th class="num">False alarms / 1,383,924 at 0.999</th>
      <th class="num">Verdict</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>natural only</td><td class="num">361,567 &middot; 26.13%</td><td class="num">refused</td></tr>
    <tr><td>2</td><td>+15 links, 400 rows each</td><td class="num">2,570 &middot; 0.186%</td><td class="num">refused</td></tr>
    <tr><td>3</td><td>the refusal's own printed flag</td><td class="num">—</td><td class="num">killed</td></tr>
    <tr><td>4</td><td>+13 links, 3,000 rows each</td><td class="num">5,257 &middot; 0.380%</td><td class="num">refused</td></tr>
    <tr><td>5</td><td><strong>positives narrowed to <code>mode=0</code></strong></td><td class="num"><strong>12 &middot; 0.0009%</strong></td><td class="num"><strong>pass</strong></td></tr>
  </tbody>
</table>

Every reported round caught 1,500 of 1,500 genuine occurrences. Round 4 is the one to look at: thirteen
more areas of corrections, seven times as many rows each, and it came out worse than round 2.

So the residual got dumped as a montage and looked at. Ninety-two per cent of it was one
screen — the nickname naming grid, map 40 at tile (5,3). A grid of dark glyphs on a light
field, which at 40&times;36 is a town. Four rounds of arithmetic had not said that, and no
aggregate was ever going to.

</section>

<div class="fig-pair" style="max-width:none;">
  <figure class="pixel">
    <p class="cap">Chosen by the byte · poisoned</p>
    <img src="../assets/img/agentgb/recogniser-battle-positives-by-byte.png" width="678" height="2418"
         alt="Fourteen rows of four stacked Game Boy frames. Row 0 is Route 1 grass with the player and a ledge. Rows 1, 3, 7 and 11 contain entirely black rectangles instead of battle screens.">
    <figcaption>
      A different trigger, the same failure, from the day before. Rows 1, 3, 7 and 11 are the
      screen wiping to black; row 0 is plain overworld grass. Every one was labelled <em>a
      battle is on screen</em>.
    </figcaption>
  </figure>
  <figure class="pixel">
    <p class="cap"><span class="accent">Chosen by the phase</span> · honest</p>
    <img src="../assets/img/agentgb/recogniser-battle-positives-by-phase.png" width="678" height="2418"
         alt="Fourteen rows of four stacked Game Boy frames. Every row shows a drawn battle scene with sprites and a text box; none is an entirely black frame.">
    <figcaption>
      The same pile after the selector was narrowed. Nothing was retrained differently and no
      corrections were added &mdash; the positives just stopped containing frames that were not
      the thing. That story is <a href="teaching-a-network-to-notice.html">the previous
      post</a>.
    </figcaption>
  </figure>
</div>

<section class="prose" markdown="1">

The Viridian fix was the same move. Positives narrowed from *every frame on map 1* to
`map=1,mode=0` — the town **outdoors**, with a menu drawn over it no longer counting as the
town. 94,409 frames over 527 tiles.

That took it to **12 false alarms in 1,383,924 frames**, 1,500 of 1,500 occurrences still
caught, weakest genuine fire at p=1.000000. Eleven of the twelve are on one link and the
twelfth is inside the Viridian Mart. Threshold 0.999 rather than the command's recommended
0.99, which is a deliberate departure: the take-the-lowest rule exists because the Game Boy
draws text letter by letter and a tight trigger goes blind on a half-drawn line, and a town is
not drawn progressively. Twelve frames against 251, identical recall.

</section>

<section class="prose" markdown="1">

## The tool poisoned its own round

Round 3 is missing from the table because it was killed rather than reported.

When `trainscene` refuses, it names the areas that fired and prints a ready `--negatives` flag
listing them. Pasting that flag back in is the obvious next move, and here it was the wrong
one: `--negatives` takes **whole episodes, with no selector**. Three of the links it named are
Viridian City almost end to end — `into-the-viridian-mart` is 99.0% map 1,
`north-out-of-viridian` 98.8%, `into-the-pokemon-center` 98.7%.

So the scene being recognised went into the *no* pile. About 18% of that round's negatives were
the thing itself. Held-out balanced accuracy fell 1.000 → 0.927 and stalled, and the round was
abandoned.

The probe was not wrong to name those links — it scores them only on their out-of-scope frames,
correctly. The advice it prints from that is what does not survive contact with a link whose
corpus *is* mostly the scene. Check a patch link's own map distribution before pasting.

</section>

<section class="prose" markdown="1">

## Zero false alarms, then 41 in a town

The forest-entry trigger, built the day before, had the cleanest numbers on the project: 150 of
150 real crossings caught at 0.999, and **zero** false alarms pooled over 495,902 frames across
23 corpora — including a shard of cross-map door fades collected on purpose, because a link's
corpus stops at its map change and the next one starts after it, so the states a run passes
through in between exist in no ordinary corpus at all.

Then a 30-run cold-boot arm came back with `forest-walk-npcbox` firing **41 times on map 1**,
Viridian City. It was the last goal driving in 16 of the 18 failures, and 15 of the 18 ended
inside the Viridian Mart at the full 8,660-decision budget, pressing `left`.

That reads exactly like a false positive, and the structural argument above says a probe cannot
rule one out. Two crews landed on that goal independently on the same day.

</section>

<section class="prose" markdown="1">

## It was innocent

The way to check is to stop probing corpora and score the recogniser on every decision of real
play instead. `harvest_goal_false_positives.py` replays a sweep's recorded attempts through the
same functions a measured run uses, wraps the driver, and writes out the stacks a named goal's
recogniser actually fires on outside its own maps. Eighteen replayed failing attempts, 155,880
decisions:

<table>
  <thead>
    <tr><th>Where</th><th class="num">Decisions</th><th class="num">Peak probability</th></tr>
  </thead>
  <tbody>
    <tr><td>Viridian City</td><td class="num">3,278</td><td class="num">0.0408</td></tr>
    <tr><td>Inside the Viridian Mart</td><td class="num">100,728</td><td class="num">5.4e-05</td></tr>
    <tr><td>Viridian Forest</td><td class="num">—</td><td class="num">0.99996</td></tr>
  </tbody>
</table>

On the one traced seed, the two Viridian decisions it was recorded as "firing" on read
7.7e-17 and 8.9e-08. All 30 episodes' first fire is on map 51, and no episode fires outside the
forest before entering it.

The recogniser never fired in the town at all. A `fired` event in the run record cannot tell a
threshold being cleared from a persisted hold **resuming**, and that one ambiguity is what made
a mechanical bug look like a perception one. A retrain would have changed nothing.

One real risk did fall out of the harvest, and it is worth naming. The only readings above 0.5
anywhere outside the forest are fifteen, all in Oak's Lab, peaking at **0.9576**. Dumped and
looked at, they are the same shape as the entry positives: a solid black transition frame in
the oldest channel of the stack, beside a light textured region and a text box. Which is what
that positive class is made of — 150 near-identical frames of one tile, (17,46), with the
camera clamped at the forest's southern edge so the lower half of every one is black. It is
safe today because the threshold is 0.999 and not 0.95. That is a thinner margin than anybody
knew they had.

</section>

<section class="prose" markdown="1">

## The fault was mechanical

`end_condition.persist_through_other_goals` exists because a hold that spans a long stretch of
play loses the wheel the moment anything else wins a single decision; without it the forest
crossing scored 0/30. As first written it made a hold survive the decisions it does not drive,
and left its ending observable only on the ones it does.

Lose a Bug Catcher fight inside Viridian Forest. The cartridge blacks the party out to Viridian
City while the battle hold is driving. The forest hold is asked nothing, the battle hold
releases at map 1, the forest hold resumes — and the forest's own walking adapter drives the
run around a town it has never seen for the rest of its budget. The event immediately before
every single non-forest fire is a battle hold releasing at map 1 or 0: fourteen trainer
battles, one wild.

The version this trigger replaced was gated on `wCurMap` and was immune by construction. It
re-asked memory every decision, so a teleport stopped it on the next one. Moving to the screen
removed the memory read and quietly removed that property with it. **When a mechanism replaces
a memory read, check which properties the memory read was silently providing.**

The replacement needs no weights. `release_on_text` sweeps a list of phrases at the top of
every decision, before selection, for every persisted hold. A list rather than one phrase,
because a decision samples one frame in 32 and the game draws a line letter by letter:
`BLUE is out of / useable POKéMON!` is up for two sampled decisions, `BLU` for one mid-draw,
and `BLUE blacked / out!` fully drawn for about one. Two phrases give roughly four decisions of
cover instead of one.

Paired on the identical 30 seed pairs, cold boot, seed 42:

<table>
  <thead>
    <tr><th>Whole chain, 30 cold boots</th><th class="num">Crossings</th></tr>
  </thead>
  <tbody>
    <tr><td>persisted hold, no way to end it while evicted</td><td class="num">12/30 &middot; 40.0%</td></tr>
    <tr><td><strong>hold released on the blackout line</strong></td><td class="num"><strong>25/30 &middot; 83.3%</strong></td></tr>
  </tbody>
</table>

Thirteen gained, none lost, McNemar exact p = 0.00024. Milestones 1 to 24 are 30/30 in both
arms, and the change is provably inert where no blackout happens: all 12 runs that already
finished reproduce their exact decision count, 12 of 12, median 2,165.5 either way. Fires on
map 1 went 41 → 0; all 270 fires are on map 51; the first fire is on map 51 in 30 runs of 30.
The trigger everybody suspected was never touched.

Of the five that still fail, four are stuck in a forest battle — no PP left, no running from a
trainer battle — which is a known gap in fighting competence and not this bug. The fifth
released correctly at the blackout and then wandered into the Mart under a different latched
lesson.

</section>

<section class="prose" markdown="1">

## What the day cost

The give-back that started all of this measured a null, and it is recorded as one. Seven
recorded knockout seeds: 2/7 through the forest with no clear, 2/7 clearing, 2/7 clearing and
handing back — the same two seeds every time. Thirty cold boots, paired: 12/30 both arms, zero
gained, zero lost, every one of the 25 milestones identical.

The mechanism itself is clean. Fifteen of the 30 runs got the lesson handed back, every restore
on map 1 and on that stage alone, zero false hand-backs, zero runs ending still-held. It fires
correctly, costs nothing, and rescues nothing at this sample size, because the thing ending the
runs was three maps away in a branch of code with no weights in it.

Five training rounds bought a recogniser that works and does not currently matter. Finding that
out is what made the next fix a one-line declaration.

</section>

<section class="prose" markdown="1">

## The sequence

This is now the written procedure rather than something the crew happens to do.

**1. Dump the positives and look at the montage before training.** Not a description of them —
the actual four-frame stacks, in a picture, in front of a person. It has now caught a poisoned
pile three times where every number said clean.

**2. Small cheap tests first.** A tile distribution, a map histogram, one probe over one link.
An hour of training is a bad way to discover a bad idea.

**3. Let the tool refuse.** A trigger that fires where it should not is not a trigger. The
default false-alarm bar is 0.0 because a trigger behind a hold strands the whole run on one
false positive — relax it deliberately, on evidence, and say so. This one was relaxed to
0.0005, on the argument that the exposure is bounded by where the code can ever ask.

**4. Narrow what it learns from before piling on corrections.** Rounds 2 and 4 added 28 links
of negatives between them and left 5,257 false alarms. Adding `mode=0` to the positive selector
left 12. Every correction teaches the network another place it is not; a narrower positive
teaches it what it is.

</section>

<figure class="pixel">
  <img src="../assets/img/agentgb/recogniser-lead-hp-bar-positives.png" width="678" height="1950"
       alt="Rows of four stacked Game Boy battle frames with the lead Pokémon's HP bar outlined in red, and the crop itself blown up beneath each row. The Pokémon's name, the HP label and the digits all sit outside the red box.">
  <figcaption>
    The same principle in its structural form: a declared crop. This recogniser is 24,082
    parameters and cannot see the name or the level, by construction rather than by hoping a
    balanced corpus makes it ignore them.
  </figcaption>
</figure>

<section class="prose" markdown="1">

**5. Two aimed rounds, then stop and report the trade-off.** Round 4 was the third and it went
backwards. The stopping condition is not "it passed", it is "the next round has a reason".

**6. Measure in a real run, paired, and report what was gained and what was lost.** Both
numbers. 13 gained and 0 lost is a result; 8 gained and 4 lost, which is what an earlier change
on this same chain produced, is not.

And a seventh that only exists because of today: **check who is driving before blaming what
recognised.** Forty-one fires in a town, sixteen of eighteen failures ending under that goal,
and the recogniser's own peak reading there was 0.0408.

</section>
