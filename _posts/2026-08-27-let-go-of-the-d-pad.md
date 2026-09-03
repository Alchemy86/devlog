---
title: 'Let go of the D-pad'
tag: 'PixelGB'
kicker: 'Emulator driving'
card_kicker: 'Capture'
eyebrow: 'PixelGB · Capture'
order: 20
description: >-
  One line took a cartridge map capture from 113 maps to 216. A door is a warp on both sides,
  and a player still holding the direction walks straight back out.
lead: >-
  PixelGB photographs every map in a Pokémon Blue cartridge by walking the game into it.
  Holding the direction for a fixed number of frames reaches every open map in the game and
  almost no building.
metrics:
  - num: '113'
    label: 'Maps, holding the D-pad'
  - num: '216'
    label: 'Releasing on arrival'
    accent: true
  - num: '226'
    label: 'Maps in the cartridge'
  - num: '31'
    label: 'Maps a text box nearly cost'
note: >-
  All figures come from one run of <code>pixelgb verify</code> against a Pokémon Blue
  cartridge, written up in the project's own verification record.
---

<section class="prose" markdown="1">

## Getting in at all

Writing a map number into `wCurMap` crashes the game. The whole map header sits
underneath it, so the engine ends up reading the new map's blocks through the old map's
pointers.

The safe route is `wWarpEntries`: redirect one of the current room's own warps at the
target map and walk the player into it. The engine loads the destination header itself —
`LoadMapHeader`, the tileset copy into video RAM, the palette, the objects, the screen.
Everything after the walk is the game's own.

So PixelGB plays the opening, saves the machine's state the moment it stands on a real
map, and for each of the 226 maps rewinds to that moment, points one warp at the target
and walks in.

</section>

<section class="prose" markdown="1">

## And then one line was worth a hundred maps

<div class="pullquote">
  <p>
    Let go of the D-pad the instant the map changes.
  </p>
  <cite>The single most important line in <code>warp_to</code></cite>
</div>

A door is a warp on both sides. You arrive on the doormat, and a player still holding
the direction takes one more step and walks straight back out.

Holding: 113 maps photographed. Releasing on arrival: 216.

</section>

<section class="prose" markdown="1">

## The one that was stranger: shop clerks talk

Several maps put a text box up the moment you arrive, and Generation 1 does that by
parking the window layer at `WY = 0`. Which means the window covers the entire screen
and the map is drawn through it.

An earlier version of the comparison excluded "wherever the window is", the way it
excludes sprites — and so masked the whole picture. 31 maps went from exact to
inconclusive and two to no-alignment, with nothing in the report to say why.

The right answer was not to subtract the text box but to dismiss it, the way a player
does: press B until the window is off-screen again, requiring several consecutive clear
checks, because the window parks off-screen for a few frames between two boxes of one
conversation.

It looked like a tolerance problem and it was a modelling one.

</section>

<section class="prose" markdown="1">

## What it did not rescue

The Hall of Fame. Walk in and Oak starts talking, and his script is not one you can
press B through — it inducts the party. PixelGB presses B up to eighty times and
requires four consecutive clear checks before photographing; this one still has a text
box up when the budget runs out, so it is counted on its own.

Ten more maps have nowhere to arrive: a warp names a destination warp on the far side
and these have none, so the camera comes to rest outside the map. Those and the Hall of
Fame are the eleven named on the [project page](../projects/pixelgb.html).

</section>
