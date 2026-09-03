---
title: '293 runs stopped on the same text box'
tag: 'AgentGB'
kicker: 'Behavioural cloning'
card_kicker: 'Training data'
eyebrow: 'AgentGB · Training data'
order: 11
description: >-
  A nine-link chain collapsed from 300 of 300 to 7. The student was doing exactly what its
  supervisor had told it to do.
lead: >-
  Adding the three links that leave Pallet Town made a nine-link chain collapse from 300 of
  300 to <strong>7 of 300</strong>. Every one of the 293 lost runs stopped in the same room,
  in the same posture, on the same text box.
metrics:
  - num: '<span class="accent">7</span> / 300'
    label: 'Cold boots completing'
  - num: '293'
    label: 'Stopped in one room'
  - num: '400 / 400'
    label: 'Decisions pressing a direction'
  - num: '12.84%'
    label: 'Label drift on the worst link'
note: >-
  The label-drift figures and the chain rates are the project's own recorded measurements,
  each stored beside the command that produced it.
---

<section class="prose" markdown="1">

Oak's Lab, tile (5,3), the message *"Gramps! What about me?"* — the student pressing a
direction at an open text box for 400 decisions out of 400 without moving a single tile.

That specificity is the useful part. A perception failure scatters. A student that fails
293 times in one room, on one tile, on one message, is not confused about what it is
seeing.

</section>

<section class="prose" markdown="1">

## The bug was in the teacher

Every teacher in the repository answers an open text box with `B`. Except the navigation
teacher, which gated that rule on a mode flag — and that flag reads "overworld" while a
box is on the screen.

For five links nothing noticed, because no navigation link had ever been in a room with
a conversation in it. The link that leaves the lab is the first. It put thousands of
frames of an open text box into the corpus *labelled with a direction*.

A direction press re-triggers the box. The student learned that faithfully and did it
four hundred times.

<div class="pullquote">
  <p>
    The picture was fine. The student did exactly what its supervisor said. It was a
    label bug, not a perception bug.
  </p>
</div>

</section>

<section class="prose" markdown="1">

## Measuring the blast radius

The fix is one shared helper. The interesting question was how much else the bug had
poisoned: 12.84% label drift on the link that leaves the lab, and 1.43–3.63% on the four
other navigation links.

Both the before and the after are published, because the after is not legible without
the before.

</section>

<section class="prose" markdown="1">

## Which weights these numbers belong to

The 7-of-300 and 300-of-300 figures belong to an earlier, uncommitted arm of the student
which always took Charmander. They are a before-and-after on one training arm, which is
what they are, and not a score for the file that ships. The shipped student's own rates
are on the [project page](../projects/agentgb.html).

</section>
