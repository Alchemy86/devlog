---
title: 'The day that added nothing'
tag: 'AgentGB'
kicker: 'Controls'
card_kicker: 'Method'
eyebrow: 'AgentGB · Method'
order: 10
description: >-
  Five identical training runs, a 23-point spread, and two published numbers that turned out
  not to be readable.
dek: >-
  Five identical training runs scored 100, 92, 92, 85 and 77 per cent. Every ablation
  published before that lacked the control.
lead: >-
  On 18 August 2026 this project added no capability whatsoever. What it did instead was prove
  that two numbers it had already published were not readable. Every result since is
  trustworthy because of it.
metrics:
  - num: '<span class="accent">23</span> pts'
    label: 'Band between identical runs'
  - num: '100% → 52.7%'
    label: 'Same policy, same tile'
  - num: '6 vs 22'
    label: 'Distinct people-layouts'
  - num: '0'
    label: 'New links that day'
note: >-
  The five-run band and the 100% / 52.7% spread are the project's own published controls, each
  recorded beside the command that produced it.
---

<section class="prose" markdown="1">

## The training run is the largest term, and it had no control

Five runs of the identical configuration on one link scored:

<div class="table-wrap">
  <table>
    <thead><tr><th>Run of an identical configuration</th><th class="num">1</th><th class="num">2</th><th class="num">3</th><th class="num">4</th><th class="num">5</th></tr></thead>
    <tbody>
      <tr><td>Cold success rate</td><td class="num">100.00%</td><td class="num">92.33%</td><td class="num">92.33%</td><td class="num">84.63%</td><td class="num">77.00%</td></tr>
    </tbody>
  </table>
</div>

A 23-point band, most of it the seed and the rest the BLAS thread count. Every ablation
published before that day lacked the control, which means every one of them could have
been measuring the draw rather than the change.

A fit does not reproduce. Same seed, same recipe, a differently-loaded machine, and you
get different weights.

</section>

<section class="prose" markdown="1">

## Cold evaluation over a state pool is optimistic by about a factor of two

Every state in a start-state pool is frozen from one traversal, so the map's own people
barely move between them. Same policy, same tile, 150 attempts: 100% under a 0–96 frame
start offset, **52.7% under 0–3,000**.

Six distinct people-layouts against twenty-two. That is the whole difference.

Every rate published since carries both spreads. The gap between them is the measure of
how brittle a student is.

<div class="pullquote">
  <p>
    A person standing in the way is drawn on the screen. The screen-only student pays
    nothing measurable for the wider spread; the feature-vector student it replaced
    halved.
  </p>
</div>

</section>

<section class="prose" markdown="1">

## Then the naming rule

On 21 August, in one evening, this project reported a rate to the captain as belonging
to the committed network when it did not — twice. Once because a results page never
named which weights produced its headline. Once because a sampling result measured on
one student was carried onto a different one.

Both reports were plausible, both were wrong, and nothing in the repository could have
caught either.

The fix is a check that fails a build the same way it failed the captain. A page opts in
with a marker in its first forty lines. Every table on an opted-in page that contains a
percentage-looking cell must carry one of: a per-row attribution column, a weights
filename in its rows, or the literal word `unattributed`.

The opt-in matters. Most tables in the repository are about the teacher — a scripted
program, never versioned by weights — or about cartridge mechanics. Neither has this
ambiguity.

</section>

<section class="prose" markdown="1">

## And the checker passed for the wrong reason

An early version carried a sticky "have we seen a model name anywhere in this file yet"
flag. A single mention in a page's opening paragraph made every table below it
unfailable, no matter how far below and no matter what it was about.

It was caught by deleting a real table's attribution column and watching the check still
pass. Each table is now judged on its own.

<div class="pullquote">
  <p>
    A rate with no model name attached is not a verified rate.
  </p>
  <cite>The rule this repository keeps</cite>
</div>

</section>
