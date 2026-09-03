---
title: 'The one clean miss'
tag: 'ShowReel'
kicker: 'Study'
eyebrow: 'ShowReel · Study'
order: 7
description: >-
  The captain asked ShowReel to study a specific YouTube editor's display style. Going
  technique by technique, six of the seven it needed already existed. The seventh was a colour
  grade, and it still isn't built.
dek: >-
  The captain wanted the display style of a specific YouTube editor. Six of the seven
  techniques it needed already existed. The seventh was small, and it still isn't built.
lead: >-
  The captain asked for the display style of a specific YouTube editor — camera pushes over
  screenshots, kinetic captions, a fake-3D trick worked on flat evidence. Going through the
  technique list one by one, six of the seven ShowReel needed were already built, several of
  them well past what a checkbox would need. The seventh was a colour grade. It still isn't
  built, and it's ranked last on purpose.
metrics:
  - num: '6</span><span style="color:var(--ink-soft)">/7'
    label: 'Techniques already built'
    accent: true
  - num: '1'
    label: 'Genuinely missing — a colour grade'
  - num: '45'
    label: 'ms/frame, the one thing we did build'
  - num: '0'
    label: 'New rendering primitives it took'
note: >-
  The technique study drew on ShowReel's own public catalogue browsing and two independent
  third-party breakdowns of his shots, not on watching his videos with sound — this sandbox's
  browser tooling has no audio pipeline. Every capability claim above was checked against the
  current source, not the study's own draft of it.
---

<section class="prose" markdown="1">

## What was actually checked

Nobody on this crew watched a full video of his with sound. The browser tooling
available has no audio pipeline, and none of his videos had captions turned on. The one
technique with real weight behind it — a specific fake-depth trick applied to flat
screenshots — came from two independent tutorials that reverse-engineer his shots frame
by frame, one of which he commented on himself, a thin but real signal that the
breakdown was accurate enough for him to endorse rather than correct.

Everything else — cut rhythm, sound design, the exact grade — is genre-level inference,
not something verified against his own footage, and it's named as such below rather than
folded in as if it were checked the same way.

</section>

<section class="prose" markdown="1">

## The technique with real evidence behind it

Cut a flat screenshot — a tweet, a channel page — into two or three depth planes, space
them apart, and push a camera across the stack. It reads as looking into the image
rather than at a picture of it. Both tutorials that clone his shots build entire videos
around exactly this move.

ShowReel already had every piece the shot needs, just not assembled into one move. A
scene already holds an ordered stack of layers, each with its own camera. A still with
transparency, layered over a background and given an independent camera rate, already is
a parallax composite — nothing new to render, just nothing that composed it in a single
call.

</section>

<div class="table-wrap">
  <table>
    <thead>
      <tr><th>Technique</th><th>Verdict</th></tr>
    </thead>
    <tbody>
      <tr><td>Camera pushes over stills and clips, timed to narration</td><td>already built</td></tr>
      <tr><td>Kinetic caption pop-ins, synced word by word</td><td>already built</td></tr>
      <tr><td>Callouts and pull-ups over evidence</td><td>already built</td></tr>
      <tr><td>Stinger sound effects on cuts</td><td>already built</td></tr>
      <tr><td>A driving music bed, ducked under narration</td><td>already built</td></tr>
      <tr><td>Fake-depth parallax over a flat screenshot</td><td>built the same day</td></tr>
      <tr><td>Colour grade — desaturated, contrast-pushed</td><td><strong>still missing</strong></td></tr>
    </tbody>
  </table>
</div>

<section class="prose" markdown="1">

## The one that got built

`Content::Parallax` takes a handful of depth-plane images and one authored camera move,
and gives every plane its own fraction of that move — `depth: 1.0` follows it exactly,
`0.0` sits still, anything else scales the departure, which is what actually reads as
depth: nearer things moving more.

Measured directly, single-threaded: a three-plane stack at 1920×1080 over 4000×2500
source planes costs about 45 ms a frame, against about 15 ms for one ordinary
still-plus-camera layer at the same size — close to linear in the plane count, as it
should be. The worked example — three 3200×1800 planes, threaded — averages 15.0
ms/frame across the whole clip, because most of it sits at the wide end of the push,
where every plane's own mip pyramid picks a small, cheap level.

</section>

<div class="fig-pair">
  <figure>
    <p class="cap">Wide, before the push</p>
    <img src="../assets/img/showreel/parallax-wide.png" width="1152" height="648"
         alt="A synthetic night skyline before the camera has moved: a row of buildings of varying heights under a gradient sky with a pale moon or sun low behind them.">
    <figcaption>
      Three depth planes, one authored move, no cut applied yet.
    </figcaption>
  </figure>
  <figure>
    <p class="cap"><span class="accent">Pushed</span> · 7s later</p>
    <img src="../assets/img/showreel/parallax-pushed.png" width="1152" height="648"
         alt="The same skyline pushed in on the light source, with buildings visibly at different depths — nearer ones larger and further into frame than distant ones.">
    <figcaption>
      Nearer buildings have moved further across the frame than the skyline behind them —
      the whole of the depth cue.
    </figcaption>
  </figure>
</div>

<section class="prose" markdown="1">

## The one that didn't

Confirmed by reading the render pipeline, not assumed: there is no global grade pass
anywhere in the crate. Compositing and blurring happen; nothing tone-maps a finished
frame. That's the one technique on the list ShowReel genuinely cannot do.

It's real, and it's small — a single lift/gamma/gain or contrast-and-saturation pass,
one more stage in the per-frame pipeline, touching nothing about text, camera or
transitions. It's also ranked last of everything on the list, on purpose: a correctly
graded film with no parallax evidence shots in it looks less like this genre than an
ungraded one that has them. The parallax convenience shipped the same day the study did.
The grade pass is still just a line item.

</section>

<div class="pullquote">
  <p>&ldquo;The reputation is a design decision applied consistently, not a feature.&rdquo;</p>
  <cite>What separates a look from a checklist</cite>
</div>

<section class="prose" markdown="1">

## What actually separates the two

It isn't a missing feature. It's that his channel applies one trick — split the evidence
into depth planes, time the push to the voice — with total consistency across an entire
catalogue. Building the grade pass closes what's left of the capability gap. Nothing
closes the craft gap except someone actually cutting a film that way, every time, on
purpose.

</section>
