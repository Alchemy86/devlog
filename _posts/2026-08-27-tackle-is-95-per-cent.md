---
title: 'TACKLE is 95 per cent and we said 94'
tag: 'AtlasGB'
kicker: 'Cartridge data'
card_kicker: 'Corrections'
eyebrow: 'AtlasGB · Corrections'
order: 18
description: >-
  Nothing failed. A number had been computed from a belief rather than read from the
  cartridge, and it sat in four files for as long as they existed.
lead: >-
  A section of ours literally headed <em>"two things the cartridge settled"</em> recorded that
  TACKLE's accuracy byte is 240 — 94%, where the community usually quotes 95. It is 242. The
  claim had propagated into a policy document, a Rust module's doc comments and a project
  memory file.
metrics:
  - num: '242'
    label: 'The accuracy byte'
  - num: '94.9%'
    label: 'What that is'
    accent: true
  - num: '240'
    label: 'What we published'
  - num: '0'
    label: 'Runs affected'
note: >-
  The move table and the stage-modifier ratios were read off a retail Pokémon Blue cartridge
  with the project's own tools. No ROM is distributed; the reproduction command points at your
  own.
---

<section class="prose" markdown="1">

No run was affected — the code was reading the cartridge all along. Only the prose was
wrong.

It was found by re-reading the move table while writing a page about discoveries, on the
grounds that a page about discoveries which repeats a number without checking it is not
worth having.

</section>

<section class="prose" markdown="1">

## Read the table, and check the rows nobody disputes first

Six bytes per move, straight out of the cartridge:

<div class="table-wrap">
  <table>
    <thead><tr><th>Move</th><th class="num">Id</th><th class="num">Power</th><th class="num">Accuracy byte</th><th class="num">As a percentage</th></tr></thead>
    <tbody>
      <tr><td>POUND</td><td class="num">1</td><td class="num">40</td><td class="num">255</td><td class="num">100%</td></tr>
      <tr><td>SCRATCH</td><td class="num">10</td><td class="num">40</td><td class="num">255</td><td class="num">100%</td></tr>
      <tr><td>VINE WHIP</td><td class="num">22</td><td class="num">35</td><td class="num">255</td><td class="num">100%</td></tr>
      <tr><td><strong>TACKLE</strong></td><td class="num">33</td><td class="num">35</td><td class="num"><strong>242</strong></td><td class="num"><strong>94.9%</strong></td></tr>
      <tr><td>HYPER BEAM</td><td class="num">63</td><td class="num">150</td><td class="num">229</td><td class="num">89.8%</td></tr>
      <tr><td>HYDRO PUMP</td><td class="num">56</td><td class="num">120</td><td class="num">204</td><td class="num">80.0%</td></tr>
    </tbody>
  </table>
</div>

Every row but the one under investigation matches the values Generation 1 is known for.
That is what says the table is being read at the right offset with the right stride.

<figure class="code">
  <pre><code>python3 - "$ROM" &lt;&lt;'PY'
import sys
rom = open(sys.argv[1], 'rb').read()
e = 0x0E * 0x4000 + (33 - 1) * 6   # Moves, 0E:4000, TACKLE is move 33
print("power %d accuracy %d (%.1f%%)" % (rom[e+2], rom[e+4], rom[e+4] * 100 / 255))
PY
# power 35 accuracy 242 (94.9%)</code></pre>
  <figcaption>
    The whole correction, against your own cartridge. No ROM is distributed by the
    project; you point <code>$ROM</code> at yours.
  </figcaption>
</figure>

</section>

<section class="prose" markdown="1">

## Where 240 came from

94% of 255 is 239.7, which rounds to 240. It is the byte you get by computing it from a
percentage you already believed, instead of reading it.

<div class="pullquote">
  <p>
    When you write down a number the cartridge holds, write down the command that
    reads it.
  </p>
</div>

</section>

<section class="prose" markdown="1">

## And the accuracy byte is not the accuracy anyway

The hit calculation scales a move's accuracy byte by the attacker's accuracy stage and
the inverse of the defender's evasion stage. A policy reading the ROM value is reading a
number that has not been true since the first SAND-ATTACK landed.

A Pidgey's SAND-ATTACK takes a 95% TACKLE to **62%** and then **47%**. Both ratios come
out of a stage-modifier table read from the cartridge, located by searching for its own
opening bytes — a signature that occurs exactly once — and re-checked on every read
against two properties: the first pair must be 0.25, and the middle pair must be exactly
1:1, because a table read from the wrong place almost never has a neutral stage in its
middle.

<div class="callout">
  <p class="eyebrow">Found only at N = 3,000</p>
  <p>
    Three of 3,000 attempts at one scenario died in the same shape: at 2 HP against a
    Pokémon on 1 HP, the driver swung rather than escaped, because a good roll would
    end it first. Two separate 600-attempt runs were clean. The bug was not rare in
    the mechanic, it was rare in the route — it needs a Pidgey that has had time to
    use SAND-ATTACK twice.
  </p>
</div>

There is a second trap underneath it, and the atlas carries its own warning about it: in
the stat-stage block, **7 is neutral, not 0**, and the block is zeroed work RAM until
the battle-init routine writes the sevens. A sample taken on the first frames of a
battle reads 0 everywhere and looks like every stat six stages down.

</section>
