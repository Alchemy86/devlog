---
date: 2026-11-26 23:00:00 +0000
title: 'The high byte was nearly always zero'
tag: 'Pokewalker'
kicker: 'Software · Performance'
card_kicker: 'Software'
eyebrow: 'Pokewalker · Performance'
description: >-
  The walker now draws every Pokémon's walk, stand and sleep itself from a few kilobytes of
  maths, packs that maths 130 KB smaller with a trick from a 927 KB open-world game, and
  is clawing back the frames a new set of buildings cost it on a chip where one 64-bit
  divide takes three quarters of a microsecond.
lead: >-
  The walker had 224 KB of art storage left and a stand cycle that would not fit in it.
  The way out was to stop storing pictures of Pokémon at all, and then to notice that half
  the numbers left behind were zeros pretending to be data.
metrics:
  - num: '130 KB'
    label: 'Saved on the motion data, losslessly'
    accent: true
  - num: '75 → 5.9 KB'
    label: 'The high-byte plane, packed'
  - num: '0.74 µs'
    label: 'One 64-bit divide on the chip'
---

<section class="prose" markdown="1">

The walker is an ESP32-S3 behind a round screen, and its art lives in a 6.16 MB slice of
flash. Every Pokémon that follows you has to come out of that slice. A week ago each one
walked on two pictures, left foot and right foot, flipped back and forth. Then we gave all
251 of them a real walk cycle, and the obvious way to ship it, baking the frames, filled
the slice to within 224 KB. The stand cycle did not fit at all.

So the walker stopped storing pictures.

## Drawing the Pokémon instead of storing them

Each follower is already a small bundle of maths: shapes, colours and the keyframes of
its walk, stand and sleep. The desktop build has always drawn from those. Now the walker
does too. The first time it needs a frame, say Pikachu facing left, three steps into its
walk, it draws it, which takes 6.7 ms for a 32×32 follower and 27.5 ms for something the
size of Lugia. It then keeps the result in the board's spare RAM. Every later visit to that
frame costs about ten microseconds.

Over a whole run around the park the lead Pokémon drew 93 frames and then never drew
another. The frame rate did not notice.

| Follower data for all 251 | Size |
|---|---|
| Baked frames, walk and stand at 15 frames a second | 26.1 MB |
| Baked frames, eight a cycle, walk and stand | 8.5 MB |
| Baked frames, three-frame walk, no stand | 1.60 MB |
| **The maths itself: walk, stand and sleep** | **1.38 MB** |

The maths is smaller than even the cheapest pictures, and it carries all three motions at
full smoothness. The walker drew it pixel for pixel the same as the desktop does; a test
checks every phase of Bulbasaur and Pikachu against the desktop renderer.

## The trick from a 927 KB GTA

Then came a video: [someone built a GTA-style game in under a megabyte](https://github.com/shaydex-codes/outonparole),
city, cops, helicopter and all. The part worth stealing was how it stores animation. It
does not write down where a bone is on every frame. It writes down how far it moved since
the last one.

That matters because a walk is smooth. An arm at 1,203, then 1,205, then 1,208 becomes
1,203, then 2, then 3. The numbers collapse towards zero.

Our motion keys are 16-bit, two bytes each. Once they are tiny, the high byte of almost
every one is zero. So instead of storing each number's two bytes side by side, we store
all the low bytes in one run and all the high bytes in another. The second run is a long
stretch of nothing, and the compressor eats it.

There was one catch. A step backwards, minus two, is stored by a computer as 65,534, and
its high byte is anything but zero. Splitting the bytes without fixing that made things
worse, not better. The fix is a renumbering called zigzag, which maps 0, −1, 1, −2, 2 to 0,
1, 2, 3, 4, so small moves in either direction stay small.

| Motion data for all 251, packed | Size |
|---|---|
| As it was | 1,366,998 B |
| Differences, bytes side by side | 1,287,616 B |
| Differences, bytes split | 1,306,655 B |
| **Differences, zigzag, bytes split** | **1,236,962 B** |

The high-byte run alone went from 75 KB to 5.9 KB. In total, 130 KB came off, and every
one of the 251 bundles comes back byte for byte. Unpacking happens once per species, an estimated
millisecond or two on the board, and its loops touch no multiplies or divides at all.

## The chip's price list

The other half of the job was speed, and here the walker had gone backwards. On 16 Nov
[the second core went to work](the-second-core-was-doing-nothing.html) and the open world
roughly doubled: 14.1 frames a second walking along the gate road. Ten days later the same
walk ran at 3.3.

Night and rain were the first suspects, since the walker had been measured after dark. Pinning
its clock to noon changed nothing. Timing each part of a frame found it straight away: the
new 3D buildings along the road were taking 187 ms of a gate-road frame, against 45 ms for
the whole of the ground.

Each building pixel was costing about 2,000 cycles, and the reason was on the chip's price
list:

| On the ESP32-S3 | Cost |
|---|---|
| One 32-bit divide | about 0.2 µs |
| One 64-bit multiply | 0.33 µs |
| One 64-bit divide | 0.74 µs |

The S3 has no hardware for 64-bit maths, so every one of those is a call into a library
routine. The building code did three 64-bit divides per pixel, plus an edge test that
redid a remainder for every edge of every face. On a desktop that is nothing. Here it was
the frame.

## What carried over, and what did not

The ASCII city engine draws its skyline fast by casting one ray per screen column and
giving up on everything hidden behind a nearer wall. That only works when walls are
upright on screen and sit on a grid. The walker's camera tilts 14 degrees down, its
buildings stand at any angle, and their roofs are gables, hips and domes. The column trick
does not fit.

The idea behind it does. Each building face is now filled a row at a time straight from
its edges, with no hit test per pixel and no divide per row. That is what the walker runs
today. The next step is on the bench: buildings drawn nearest first, each claiming the
pixels it covers, so a building hidden behind another is never coloured at all, and
neither is the ground behind it.

| Frames a second on the board, noon | 16 Nov | Before the fix | Now |
|---|---|---|---|
| Park plaza | 15.1 | 6.8 | about 10 |
| Gate road, standing | 15.7 | 5.6 | 10–12 |
| Gate road, walking | 14.1 | 3.3 | 7.7–9 |

The picture is the same apart from 0.1% of pixels at the edges of windows.

## Where it goes next

The motion data is now the small part of a follower. Its shapes are about 1.05 MB of what
is left, and they are next. On the speed side, the gate road is still five frames a second
short of where it was on 16 Nov, and the buildings are not finished being cheap.

The rest of the device is on [the project page](../projects/pokewalker.html).

</section>
