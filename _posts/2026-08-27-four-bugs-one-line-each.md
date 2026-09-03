---
title: 'Four bugs, one line each'
tag: 'Portal'
kicker: 'Postgres · CSS'
card_kicker: 'Web'
eyebrow: 'TerminalGB Portal · Web'
order: 24
description: >-
  A dropped field, a RETURNING clause that returns the wrong thing, a bigint that arrived as a
  string, and a CSS grid that could not get narrower than 16rem.
dek: >-
  A dropped field, a RETURNING clause that returns the wrong thing, a bigint that arrived as a
  string, and a grid that could not get narrower than 16rem.
lead: >-
  Four faults from the portal's sharp-edges list. Each cost real time, each has a one-line
  cause, and all four generalise past this codebase.
note: >-
  All four are from the portal's own sharp-edges list, where every entry names the file it
  lives in and the symptom it produced.
---

<section class="prose" markdown="1">

## "The Pokémon images don't work"

The emulator was sending an offer card — sprite, types, determinant total, a shiny
prediction — right alongside the Pokémon spec. The offer endpoint read only the spec and
the save identity beside it. The card object was arriving on every request and being
dropped on the floor, so every offer showed the no-picture placeholder.

The fix came with two rules more interesting than the bug.

The card's sprite is a base64 PNG, not the collection's raw pixel array, so it is
decoded on the way in — indexed or RGB8, non-interlaced — and **the PNG's own header is
the authority on geometry**. A declared width that disagrees is a refusal, and
decompression runs with an exact output limit so a compression bomb cannot spend memory.

And a malformed card is dropped field by field, never a 400. An optional decoration from
the other side of a shared contract must not turn a valid offer into an error — but the
reasons ride back on the reply, precisely because the silent version of that is the bug
above.

</section>

<section class="prose" markdown="1">

## Every poll looked too fast

The device-code login flow enforces a minimum polling interval, and the endpoint has to
both read the last poll time and stamp a new one.

Written the obvious way — one `UPDATE … RETURNING` — it silently never works, because
`RETURNING` sees post-update values. The endpoint reads its own new timestamp, computes
an interval of zero, and interval enforcement quietly does nothing.

The shape that works reads the previous value under a row lock first and updates in a
second common table expression. It was caught before commit by reading the Postgres
documentation rather than by a test — and there is now a test, so a "tidy-up" back to a
single statement turns red.

The same snapshot rule bites twice more in this codebase: a data-modifying CTE is
invisible to the same statement's `SELECT`, so the lapsed-sprite purge must run as a
separate `UPDATE` before the `SELECT` that reads the collection, and the rate limiter
counts only prior attempts — which is why "max" here means allow exactly max, deny the
max-plus-first.

</section>

<section class="prose" markdown="1">

## A row id that was a string

`pg` returns 64-bit integers as JavaScript strings by default, because they do not fit
safely in a double. Every id in this schema is a `bigint`, so `Number.isInteger(id)`
guards silently stopped guarding and ids in JSON quietly became strings. Measured: a
friendship id came back as `"1"`.

One type-parser registration at the database module fixes it globally.

</section>

<section class="prose" markdown="1">

## A grid that could not shrink

The Pokémon cards live in a CSS grid. Written as `repeat(auto-fill, minmax(16rem,
1fr))`, that grid physically cannot get narrower than 16rem — so below about 350 pixels
it made the whole document wider than the viewport and every panel on the page got
clipped mid-word at the right edge. The `min(100%, 16rem)` spelling is load-bearing, not
stylistic.

The same class of fault lived in two other places: the site header, where the brand plus
the navigation come to about 350 pixels with no wrapping allowed; and a form label
inside a card, where a flex item's automatic minimum size is its content width, so a
16rem minimum on one label spilled the card at every width.

All three are one mistake — a rule that sets a floor on the page width — and one
measurement catches all of them:

<figure class="code">
  <pre><code>for (const el of document.querySelectorAll("body *")) {
  const r = el.getBoundingClientRect(),
        p = el.parentElement.getBoundingClientRect();
  if (r.right &gt; p.right + 1) { /* this element overflows its parent */ }
}
document.documentElement.scrollWidth &gt; document.documentElement.clientWidth</code></pre>
  <figcaption>
    Run at 1440, 1024, 800, 600, 420, 360, 320 and 280 pixels, with the in-card
    accept form both closed and open. It finds the element that overflows, not just
    the fact that something does.
  </figcaption>
</figure>

</section>

<section class="prose" markdown="1">

## And one that belongs in no category

`pgrep -f` and `pkill -f` match the process doing the matching. An automated run on this
repository killed itself with a pattern sweep for a dev server, because its own command
line contained the pattern. Kill by the process id you captured when you started the
process.

</section>
