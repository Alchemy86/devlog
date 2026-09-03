---
title: 'The ledge in Viridian City'
tag: 'AtlasGB'
kicker: 'Topology'
card_kicker: 'Map data'
eyebrow: 'AtlasGB · Map data'
order: 19
description: >-
  Seventeen runs of six hundred died on the same row of the same town. A flood fill said the
  tile was reachable, and the flood fill was right.
lead: >-
  One scenario lost 17 of 600 attempts, every one of them on the same row of Viridian City,
  sliding between x=26 and x=32 with the leg's first waypoint at (29,26) unreachable above it.
  The first model of the trap was topological, and it was wrong.
metrics:
  - num: '<span class="accent">17</span> / 600'
    label: 'Attempts lost'
  - num: '8'
    label: 'Ledge entries in the cartridge'
  - num: '0'
    label: 'Facing up'
  - num: '13'
    label: 'Steps in the path a flood fill found'
note: >-
  The walkability grid and the ledge table were read off a retail Pokémon Blue cartridge by
  the repository's own audit tool, with no emulator run.
---

<section class="prose" markdown="1">

A flood fill says (29,26) is fine. There is a 13-step path back to it crossing no warp
tile. It reports nothing.

Two things had to be modelled exactly before any check could catch it.

**The ledge.** Stepping down off row 26 does not land on row 27. It jumps to row 28. And
the one-wayness is in the cartridge's own data — eight ledge entries, for facing down,
left and right, and none for up.

**The walker.** A greedy waypoint walker is not a path-finder. Below a one-way ledge it
slides along the wall, which is precisely what the 17 failing runs did.

<figure class="code">
  <pre><code>          0123456789012345678901234567890123456789
  y=25    ####....######........#.##..........####
  y=26    ####....######......................####   &lt;- the waypoint was (29,26)
  y=27    ###############.###.####################   &lt;- ledge; gaps only at x=15, 19
  y=28    ...#................................####   &lt;- where 17 runs slid, x=26..32
  y=29    ...#.................#..............####
  y=30    ...#................................####

(29,26) walkable=True   step down -&gt; (29,28)     a two-tile jump over row 27
(29,28) walkable=True   step up   -&gt; None        nothing comes back
LedgeTiles: 8 entries, facings down/left/right, none for up

GoTo simulated below the ledge, target (29,26):
  from (29,28) -&gt; stops at (32,28)
  from (30,28) -&gt; stops at (27,28)
  from (26,28) -&gt; stops at (31,28)</code></pre>
  <figcaption>
    Viridian City rows 25–30, read off the retail cartridge with no emulator run at
    all — and the failure reproduced from it in three lines. Where the walker stops
    is exactly the x=26…32 slide the 600-attempt corpus reported.
  </figcaption>
</figure>

</section>

<section class="prose" markdown="1">

## The repair is not a bigger budget

The row the mart door opens onto crosses the city cleanly, sits six rows above the
ledge, and the rest of the chain finishes even from below the ledge. So the leg turns
west first, and an overshoot costs nothing.

This shape has now appeared three times, which is what makes it a rule rather than three
anecdotes:

<div class="pullquote">
  <p>
    A waypoint whose overshoot is unrecoverable is a waypoint pointing at a trap.
    Prefer the turning point with slack around it.
  </p>
</div>

</section>

<section class="prose" markdown="1">

## The tool that checks it over-reports, on purpose

It cannot know whether an overshoot is reachable — that needs the map's people, and a
person in the way is what pushed the walker over the ledge in the first place — and it
has no model of the driver's stuck-sidestep. So it is a design aid, not a gate, and it
says so.

</section>
