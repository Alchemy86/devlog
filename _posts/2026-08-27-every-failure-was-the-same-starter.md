---
title: 'Every failure was the same starter'
tag: 'AgentGB'
kicker: 'Swarm film · reporting rules'
card_kicker: 'Measurement'
eyebrow: 'AgentGB · Measurement'
order: 8
description: >-
  A 26-agent swarm scored 88.5% and looked healthy. Watching the film instead of reading the
  table showed all three failures were Squirtle runs — one chance in 2,600. What the number
  could not show, and the reporting rule that came out of it.
og_title: >-
  Every failure was the same starter
og_description: >-
  88.5% looked fine. Watching the film showed a whole third of the population failing every
  single time.
dek: >-
  A twenty-six agent swarm scored 88.5% and looked healthy. Watching the film instead of
  reading the table showed all three failures were the same starter Pok&eacute;mon — one
  chance in 2,600.
lead: >-
  A twenty-six agent swarm completed the whole sixteen-link chain 88.5% of the time. That is a
  good number, it was correctly computed, and it was hiding something a table structurally
  cannot show: all three failures were the same starter Pokémon. Not most. All. One chance in
  2,600.
metrics:
  - num: '88.5<span class="accent">%</span>'
    label: 'What the table said'
  - num: '<span class="accent">0</span> / 3'
    label: 'Squirtle runs that finished'
  - num: '0.00038'
    label: 'p, under a no-species-effect null'
  - num: '26 / 26'
    label: 'After three fixes'
note: >-
  Every figure here comes from this project's own swarm and certification tooling against one
  named weights file, recorded with its sample size, its temperature and its confidence
  interval. The starter each agent chose is read off the cartridge by the harness and is never
  visible to the policy. The mechanism the chain is built on has its own write-up: <a
  href="the-doubling-back-wall.html">the wall you hit walking home</a>. The wider arc is on
  the <a href="../agentgb-progress.html">AgentGB progress page</a>.
---

<section class="prose" markdown="1">

## The number was fine. That was the problem.

Twenty-three of twenty-six agents completed every milestone from a cold boot: out of the
bedroom, up Route 1, into the Mart, back down again, and the Pokédex in hand. The
confidence interval was reported, the failures were located to a tile, and the three
that stopped were noted as stopping in Oak's Lab and on Route 1.

Everything about that report was true. Nothing about it said that one entire third of
the population failed **every single time it was drawn**.

The reason it was caught at all is that the captain watched the film rather than reading
the table. Twenty-six agents on screen at once, each in its own cell, each playing its
own run — and the eye does something a summary statistic does not. It groups. Three
agents stuck in the same room, and all three had the same Pokémon.

</section>

<figure class="scrollfig" aria-labelledby="fig-swarm-cap">
  <svg viewBox="0 0 720 296" role="img" xmlns="http://www.w3.org/2000/svg" font-family="'JetBrains Mono', monospace">
    <style>
      .c  { fill: var(--code-bg); stroke: var(--hairline); stroke-width: 1.5; }
      .c.f{ fill: none; stroke: var(--accent); stroke-width: 2; stroke-dasharray: 4 3; }
      .sp { fill: var(--ink); font-size: 15px; font-weight: 700; }
      .sp.f{ fill: var(--accent); }
      .mk { fill: var(--ink-soft); font-size: 12px; }
      .mk.f{ fill: var(--accent); font-weight: 700; }
      .hd { fill: var(--ink); font-size: 11.5px; font-weight: 700; letter-spacing: .1em; }
      .hs { fill: var(--ink-soft); font-size: 10.5px; }
    </style>
    <text x="0" y="16" class="hd">BEFORE — 23 / 26 = 88.5%</text>
    <text x="696" y="16" text-anchor="end" class="hs">BULBASAUR 21/21 · CHARMANDER 2/2 · SQUIRTLE 0/3</text>
    <rect x="0" y="28" width="48" height="48" rx="6" class="c"/>
    <text x="24.0" y="50" text-anchor="middle" class="sp">B</text>
    <text x="24.0" y="66" text-anchor="middle" class="mk">✓</text>
    <rect x="54" y="28" width="48" height="48" rx="6" class="c"/>
    <text x="78.0" y="50" text-anchor="middle" class="sp">B</text>
    <text x="78.0" y="66" text-anchor="middle" class="mk">✓</text>
    <rect x="108" y="28" width="48" height="48" rx="6" class="c"/>
    <text x="132.0" y="50" text-anchor="middle" class="sp">B</text>
    <text x="132.0" y="66" text-anchor="middle" class="mk">✓</text>
    <rect x="162" y="28" width="48" height="48" rx="6" class="c"/>
    <text x="186.0" y="50" text-anchor="middle" class="sp">B</text>
    <text x="186.0" y="66" text-anchor="middle" class="mk">✓</text>
    <rect x="216" y="28" width="48" height="48" rx="6" class="c"/>
    <text x="240.0" y="50" text-anchor="middle" class="sp">B</text>
    <text x="240.0" y="66" text-anchor="middle" class="mk">✓</text>
    <rect x="270" y="28" width="48" height="48" rx="6" class="c"/>
    <text x="294.0" y="50" text-anchor="middle" class="sp">B</text>
    <text x="294.0" y="66" text-anchor="middle" class="mk">✓</text>
    <rect x="324" y="28" width="48" height="48" rx="6" class="c"/>
    <text x="348.0" y="50" text-anchor="middle" class="sp">B</text>
    <text x="348.0" y="66" text-anchor="middle" class="mk">✓</text>
    <rect x="378" y="28" width="48" height="48" rx="6" class="c"/>
    <text x="402.0" y="50" text-anchor="middle" class="sp">B</text>
    <text x="402.0" y="66" text-anchor="middle" class="mk">✓</text>
    <rect x="432" y="28" width="48" height="48" rx="6" class="c"/>
    <text x="456.0" y="50" text-anchor="middle" class="sp">B</text>
    <text x="456.0" y="66" text-anchor="middle" class="mk">✓</text>
    <rect x="486" y="28" width="48" height="48" rx="6" class="c"/>
    <text x="510.0" y="50" text-anchor="middle" class="sp">B</text>
    <text x="510.0" y="66" text-anchor="middle" class="mk">✓</text>
    <rect x="540" y="28" width="48" height="48" rx="6" class="c"/>
    <text x="564.0" y="50" text-anchor="middle" class="sp">B</text>
    <text x="564.0" y="66" text-anchor="middle" class="mk">✓</text>
    <rect x="594" y="28" width="48" height="48" rx="6" class="c"/>
    <text x="618.0" y="50" text-anchor="middle" class="sp">B</text>
    <text x="618.0" y="66" text-anchor="middle" class="mk">✓</text>
    <rect x="648" y="28" width="48" height="48" rx="6" class="c"/>
    <text x="672.0" y="50" text-anchor="middle" class="sp">B</text>
    <text x="672.0" y="66" text-anchor="middle" class="mk">✓</text>
    <rect x="0" y="82" width="48" height="48" rx="6" class="c"/>
    <text x="24.0" y="104" text-anchor="middle" class="sp">B</text>
    <text x="24.0" y="120" text-anchor="middle" class="mk">✓</text>
    <rect x="54" y="82" width="48" height="48" rx="6" class="c"/>
    <text x="78.0" y="104" text-anchor="middle" class="sp">B</text>
    <text x="78.0" y="120" text-anchor="middle" class="mk">✓</text>
    <rect x="108" y="82" width="48" height="48" rx="6" class="c"/>
    <text x="132.0" y="104" text-anchor="middle" class="sp">B</text>
    <text x="132.0" y="120" text-anchor="middle" class="mk">✓</text>
    <rect x="162" y="82" width="48" height="48" rx="6" class="c"/>
    <text x="186.0" y="104" text-anchor="middle" class="sp">B</text>
    <text x="186.0" y="120" text-anchor="middle" class="mk">✓</text>
    <rect x="216" y="82" width="48" height="48" rx="6" class="c"/>
    <text x="240.0" y="104" text-anchor="middle" class="sp">B</text>
    <text x="240.0" y="120" text-anchor="middle" class="mk">✓</text>
    <rect x="270" y="82" width="48" height="48" rx="6" class="c"/>
    <text x="294.0" y="104" text-anchor="middle" class="sp">B</text>
    <text x="294.0" y="120" text-anchor="middle" class="mk">✓</text>
    <rect x="324" y="82" width="48" height="48" rx="6" class="c"/>
    <text x="348.0" y="104" text-anchor="middle" class="sp">B</text>
    <text x="348.0" y="120" text-anchor="middle" class="mk">✓</text>
    <rect x="378" y="82" width="48" height="48" rx="6" class="c"/>
    <text x="402.0" y="104" text-anchor="middle" class="sp">B</text>
    <text x="402.0" y="120" text-anchor="middle" class="mk">✓</text>
    <rect x="432" y="82" width="48" height="48" rx="6" class="c"/>
    <text x="456.0" y="104" text-anchor="middle" class="sp">C</text>
    <text x="456.0" y="120" text-anchor="middle" class="mk">✓</text>
    <rect x="486" y="82" width="48" height="48" rx="6" class="c"/>
    <text x="510.0" y="104" text-anchor="middle" class="sp">C</text>
    <text x="510.0" y="120" text-anchor="middle" class="mk">✓</text>
    <rect x="540" y="82" width="48" height="48" rx="6" class="c f"/>
    <text x="564.0" y="104" text-anchor="middle" class="sp f">S</text>
    <text x="564.0" y="120" text-anchor="middle" class="mk f">✗</text>
    <rect x="594" y="82" width="48" height="48" rx="6" class="c f"/>
    <text x="618.0" y="104" text-anchor="middle" class="sp f">S</text>
    <text x="618.0" y="120" text-anchor="middle" class="mk f">✗</text>
    <rect x="648" y="82" width="48" height="48" rx="6" class="c f"/>
    <text x="672.0" y="104" text-anchor="middle" class="sp f">S</text>
    <text x="672.0" y="120" text-anchor="middle" class="mk f">✗</text>
    <text x="0" y="174" class="hd">AFTER THREE FIXES — 26 / 26 = 100.0%</text>
    <text x="696" y="174" text-anchor="end" class="hs">BULBASAUR 21/21 · CHARMANDER 2/2 · SQUIRTLE 3/3</text>
    <rect x="0" y="186" width="48" height="48" rx="6" class="c"/>
    <text x="24.0" y="208" text-anchor="middle" class="sp">B</text>
    <text x="24.0" y="224" text-anchor="middle" class="mk">✓</text>
    <rect x="54" y="186" width="48" height="48" rx="6" class="c"/>
    <text x="78.0" y="208" text-anchor="middle" class="sp">B</text>
    <text x="78.0" y="224" text-anchor="middle" class="mk">✓</text>
    <rect x="108" y="186" width="48" height="48" rx="6" class="c"/>
    <text x="132.0" y="208" text-anchor="middle" class="sp">B</text>
    <text x="132.0" y="224" text-anchor="middle" class="mk">✓</text>
    <rect x="162" y="186" width="48" height="48" rx="6" class="c"/>
    <text x="186.0" y="208" text-anchor="middle" class="sp">B</text>
    <text x="186.0" y="224" text-anchor="middle" class="mk">✓</text>
    <rect x="216" y="186" width="48" height="48" rx="6" class="c"/>
    <text x="240.0" y="208" text-anchor="middle" class="sp">B</text>
    <text x="240.0" y="224" text-anchor="middle" class="mk">✓</text>
    <rect x="270" y="186" width="48" height="48" rx="6" class="c"/>
    <text x="294.0" y="208" text-anchor="middle" class="sp">B</text>
    <text x="294.0" y="224" text-anchor="middle" class="mk">✓</text>
    <rect x="324" y="186" width="48" height="48" rx="6" class="c"/>
    <text x="348.0" y="208" text-anchor="middle" class="sp">B</text>
    <text x="348.0" y="224" text-anchor="middle" class="mk">✓</text>
    <rect x="378" y="186" width="48" height="48" rx="6" class="c"/>
    <text x="402.0" y="208" text-anchor="middle" class="sp">B</text>
    <text x="402.0" y="224" text-anchor="middle" class="mk">✓</text>
    <rect x="432" y="186" width="48" height="48" rx="6" class="c"/>
    <text x="456.0" y="208" text-anchor="middle" class="sp">B</text>
    <text x="456.0" y="224" text-anchor="middle" class="mk">✓</text>
    <rect x="486" y="186" width="48" height="48" rx="6" class="c"/>
    <text x="510.0" y="208" text-anchor="middle" class="sp">B</text>
    <text x="510.0" y="224" text-anchor="middle" class="mk">✓</text>
    <rect x="540" y="186" width="48" height="48" rx="6" class="c"/>
    <text x="564.0" y="208" text-anchor="middle" class="sp">B</text>
    <text x="564.0" y="224" text-anchor="middle" class="mk">✓</text>
    <rect x="594" y="186" width="48" height="48" rx="6" class="c"/>
    <text x="618.0" y="208" text-anchor="middle" class="sp">B</text>
    <text x="618.0" y="224" text-anchor="middle" class="mk">✓</text>
    <rect x="648" y="186" width="48" height="48" rx="6" class="c"/>
    <text x="672.0" y="208" text-anchor="middle" class="sp">B</text>
    <text x="672.0" y="224" text-anchor="middle" class="mk">✓</text>
    <rect x="0" y="240" width="48" height="48" rx="6" class="c"/>
    <text x="24.0" y="262" text-anchor="middle" class="sp">B</text>
    <text x="24.0" y="278" text-anchor="middle" class="mk">✓</text>
    <rect x="54" y="240" width="48" height="48" rx="6" class="c"/>
    <text x="78.0" y="262" text-anchor="middle" class="sp">B</text>
    <text x="78.0" y="278" text-anchor="middle" class="mk">✓</text>
    <rect x="108" y="240" width="48" height="48" rx="6" class="c"/>
    <text x="132.0" y="262" text-anchor="middle" class="sp">B</text>
    <text x="132.0" y="278" text-anchor="middle" class="mk">✓</text>
    <rect x="162" y="240" width="48" height="48" rx="6" class="c"/>
    <text x="186.0" y="262" text-anchor="middle" class="sp">B</text>
    <text x="186.0" y="278" text-anchor="middle" class="mk">✓</text>
    <rect x="216" y="240" width="48" height="48" rx="6" class="c"/>
    <text x="240.0" y="262" text-anchor="middle" class="sp">B</text>
    <text x="240.0" y="278" text-anchor="middle" class="mk">✓</text>
    <rect x="270" y="240" width="48" height="48" rx="6" class="c"/>
    <text x="294.0" y="262" text-anchor="middle" class="sp">B</text>
    <text x="294.0" y="278" text-anchor="middle" class="mk">✓</text>
    <rect x="324" y="240" width="48" height="48" rx="6" class="c"/>
    <text x="348.0" y="262" text-anchor="middle" class="sp">B</text>
    <text x="348.0" y="278" text-anchor="middle" class="mk">✓</text>
    <rect x="378" y="240" width="48" height="48" rx="6" class="c"/>
    <text x="402.0" y="262" text-anchor="middle" class="sp">B</text>
    <text x="402.0" y="278" text-anchor="middle" class="mk">✓</text>
    <rect x="432" y="240" width="48" height="48" rx="6" class="c"/>
    <text x="456.0" y="262" text-anchor="middle" class="sp">C</text>
    <text x="456.0" y="278" text-anchor="middle" class="mk">✓</text>
    <rect x="486" y="240" width="48" height="48" rx="6" class="c"/>
    <text x="510.0" y="262" text-anchor="middle" class="sp">C</text>
    <text x="510.0" y="278" text-anchor="middle" class="mk">✓</text>
    <rect x="540" y="240" width="48" height="48" rx="6" class="c"/>
    <text x="564.0" y="262" text-anchor="middle" class="sp">S</text>
    <text x="564.0" y="278" text-anchor="middle" class="mk">✓</text>
    <rect x="594" y="240" width="48" height="48" rx="6" class="c"/>
    <text x="618.0" y="262" text-anchor="middle" class="sp">S</text>
    <text x="618.0" y="278" text-anchor="middle" class="mk">✓</text>
    <rect x="648" y="240" width="48" height="48" rx="6" class="c"/>
    <text x="672.0" y="262" text-anchor="middle" class="sp">S</text>
    <text x="672.0" y="278" text-anchor="middle" class="mk">✓</text>
  </svg>        <figcaption id="fig-swarm-cap">
    <strong>The same twenty-six runs, before and after.</strong> B, C and S are the
    starter each agent chose for itself — the harness reads it back off the cartridge,
    and the network never sees it. Every dashed cell is a run that did not finish. The
    aggregate moved from 88.5% to 100.0%, but the aggregate is not the finding. The
    <em>shape</em> is.
  </figcaption>
</figure>

<section class="prose" markdown="1">

## One in two thousand six hundred

"All three failures were the same thing" is exactly the sort of pattern a human finds in
noise, so: with 21 Bulbasaur, 2 Charmander and 3 Squirtle runs and no species effect at
all, the probability that the three failures land on the three Squirtle runs is about
**1 in 2,600**. p ≈ 0.00038.

That is not a coincidence you shrug at. And it was the *second* time this exact shape of
bug had appeared in this project, which is what turned it from an incident into a rule.

<div class="callout">
  <p class="eyebrow">The standing order that came out of it</p>
  <p>
    <strong>Report per starter on every certification and every swarm.</strong> Not
    when it looks relevant. Every time. An aggregate over a population with a
    structural split in it is a number that is simultaneously correct and useless.
  </p>
</div>

</section>

<section class="prose" markdown="1">

## Why the film sees what the table cannot

Not because a film is nicer to look at. Because of what each representation can carry.

A completion table has one row per milestone and one rate per row. It is a *marginal* —
it has already summed over the population, and a correlation between a run's hidden
attribute and its outcome is exactly the information summing destroys. You cannot
recover it from the table no matter how carefully you read, because it is not in the
table.

The film has not summed over anything yet. Every agent is still a separate object on
screen, carrying everything about itself, and the failures are visible *as a group* —
three cells stuck in the same room at the same time is a thing you see rather than
compute.

<div class="pullquote">
  <p>
    The swarm film is not a nicer way of showing the number. It is the only artefact
    in the pipeline where the population has not been collapsed yet.
  </p>
  <cite>What this cost, and what it bought</cite>
</div>

It is not free. The film that showed this takes roughly twenty-four screenshots per
decision per agent — gigabytes — where the table costs nothing but the emulation. It is
the expensive artefact, and this is what it is for.

</section>

<section class="prose" markdown="1">

## Three separate causes, none of them the one first suspected

The obvious hypothesis was that the training corpus was biased toward one starter, so
the student was simply worse with the others. That was checked, and it is not what was
happening.

The starter *choice* is genuinely balanced. At the chain's own entry state the first
decision carries 0.992 bits of entropy, and over 500 sampled attempts the committed
student takes Bulbasaur 254 times, Squirtle 127 and Charmander 118, reaching the goal in
499 of 500. That is a real three-way split, not a collapse.

What *was* true, and actionable, is narrower and less obvious: two of the links on the
return leg have exactly **one** recorded start state each, so their corpora contained
**zero species variation** — regardless of how balanced the entry choice was. The
student had simply never been shown those rooms with a Squirtle in the party.

Pulling the three failures apart gave three unrelated causes:

</section>

<div class="cards">
  <div class="card">
    <div class="card-hd">
      <p class="kicker">Two agents</p>
      <h3>Reached Oak and never spoke to him</h3>
    </div>
    <div class="card-bd">
      <p>
        They walked into him, forever. At the four interaction tiles, facing correctly,
        the base policy's own prediction is the right button only <strong>4.55%</strong>
        of the time — the corpus mostly demonstrates the <em>dialogue</em> that follows
        the first press, not the press that starts it.
      </p>
      <p>
        Fixed with a dedicated goal whose positives were harvested structurally from the
        link's own existing corpora at the four declared tile-and-facing spots.
      </p>
    </div>
  </div>
  <div class="card">
    <div class="card-hd">
      <p class="kicker">One agent</p>
      <h3>Deadlocked in a battle menu for 3,600 decisions</h3>
    </div>
    <div class="card-bd">
      <p>
        Traced directly on a real seed: a wild Rattata at 8/23 HP, and the agent pressed
        <code>right</code> forever with the HP never once changing. The return crossing
        of Route 1 was still set to flee-only — the exact state the <em>outbound</em>
        crossing had been in before its own upgrade.
      </p>
      <p>
        It was also explicitly ruled out that the trainer-battle goal was false-firing
        here: its own history had stopped growing well before the deadlock began.
      </p>
    </div>
  </div>
  <div class="card">
    <div class="card-hd">
      <p class="kicker">One agent</p>
      <h3>Whited out and never recovered</h3>
    </div>
    <div class="card-bd">
      <p>
        The rule that a whiteout must not end a run was already active. The real gap was
        that nothing had ever taught the student what to do once it wakes up at home.
      </p>
      <p>
        Fixed for free: a whiteout this early teleports the party to the player's own
        house, and the link's goal is simply "be outdoors in Pallet Town" — so walking
        out of the house satisfies it, and two existing links already do exactly that at
        100%. No new data was collected at all.
      </p>
    </div>
  </div>
</div>

<section class="prose" markdown="1">

## The fix that broke everything, and what it taught

The first wiring of the Oak-interaction goal took the whole chain from 88.5% to **0 of
150**.

The trigger tile it had been trained on — one specific tile, facing one specific
direction — is, independently, the chain's own *entry* tile for taking a starter six
links earlier. Same physical room, visited three times by this chain for three different
reasons. An ungated goal that fires whenever it recognises its screen fired on the very
first approach to the Poké Balls and broke every single run.

The fix was structural rather than a heuristic: the late-chain goals are now only ever
consulted once a return-leg stage has *already* latched. Not by convention — by
construction. A screen that a return-leg goal happens to recognise can no longer hijack
the outward leg, however visually identical it is to something further down the chain.

There is a general shape here worth naming. In a route that revisits the same rooms, **a
recogniser's precision is not a property of the recogniser**. It is a property of the
recogniser *and* the window of the episode it is allowed to look in. Ours was excellent
at its job and catastrophic without a gate.

</section>

<section class="prose" markdown="1">

## Where it landed

After the three fixes, an eight-agent smoke test first — 8/8 — before committing to the
long run. Then a cold-boot certification at N=150:

<div class="table-wrap">
  <table>
    <thead>
      <tr>
        <th>Starter</th>
        <th class="num">Completed the whole chain</th>
        <th class="num">Rate</th>
        <th class="num">95% interval</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>BULBASAUR</td><td class="num">87 / 90</td><td class="num">96.7%</td><td class="num">90.7–98.9%</td></tr>
      <tr><td>CHARMANDER</td><td class="num">13 / 13</td><td class="num">100.0%</td><td class="num">77.2–100.0%</td></tr>
      <tr><td>SQUIRTLE</td><td class="num">45 / 47</td><td class="num">95.7%</td><td class="num">85.8–98.8%</td></tr>
      <tr><td><strong>All sixteen links</strong></td><td class="num"><strong>145 / 150</strong></td><td class="num"><strong>96.67%</strong></td><td class="num"><strong>92.4–98.6%</strong></td></tr>
    </tbody>
  </table>
</div>

No starter anywhere near zero, all three intervals overlapping heavily. The filmed swarm
at N=26 came back 26/26 — the first time this chain's film has shown every starter
completing at 100%, where the previous one showed a third of them at zero.

N=150 is not the project's 3,000-attempt convention, and bounds failure near 2%, not
0.1%. And Charmander's 13/13 has a lower interval bound of 77.2%: thirteen runs is
evidence of not-obviously-broken, not of perfection.

</section>

<section class="prose" markdown="1">

## What this actually generalises to

Very little of the above is about Pokémon.

An agent population with a self-selected hidden attribute — which tool it picked, which
branch it took, which variant it was served — will produce an aggregate success rate
that is arithmetically correct and behaviourally meaningless the moment that attribute
correlates with outcome. The failure mode is not a wrong number. It is a right number
answering a question nobody asked.

Two cheap defences came out of this. Break every rate down by the attribute, whether or
not you expect it to matter. And keep one artefact in the pipeline where the population
has not been collapsed yet — expensive, rarely looked at, and the only place a
structural split is visible before it becomes a mystery.

</section>
