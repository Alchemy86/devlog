# devlog

The captain's public engineering log — a running record of what he builds, with real
numbers and honest trade-offs. Game Boy work at the moment: TerminalGB, AgentGB, AtlasGB,
PixelGB, GBSelfTest and the Portal, alongside Glyphsmith, ShowReel and AsciiWorldEngine.
The source repositories are mostly private; this site is where the work becomes visible.

**Live:** https://alchemy86.github.io/devlog/

It is also a small, complete blog you can clone and write in. Drop a markdown file into
`_posts/`, push, and it is live — styled, listed on the front page, with its own metadata.

## Adding a post

1. Create `_posts/YYYY-MM-DD-your-title.md`.
2. Give it front matter and write the body in markdown.
3. Commit and push.

That is the whole procedure. **There is no build step.** GitHub Pages runs Jekyll on
every push, so nothing on the site can drift out of date with its source — there is no
generated HTML in the repository to forget to regenerate.

The smallest post that works:

```markdown
---
title: 'The red we refused to fix'
tag: 'TerminalGB'
kicker: 'Calibration'
eyebrow: 'TerminalGB · Method'
description: >-
  One sweep would have turned a failing test green.
lead: >-
  <code>csp/bully</code> shows a black screen, and there is an obvious way to fix it.
note: >-
  Every suite score here is from TerminalGB's own checked-in baselines.
---

## Why sweeping would have been wrong

Bully waits for `LY >= $90` before reading the divider, so what it pins is not the
counter. It is the *phase between two clocks* at boot hand-off.
```

### Front matter

| Field | Required | What it does |
| --- | --- | --- |
| `title` | yes | Headline, `<title>`, and the card on the front page |
| `tag` | yes | Project chip in the post meta and on the card |
| `kicker` | yes | Middle item of the post's own meta line |
| `eyebrow` | yes | Small mono label above the headline |
| `description` | yes | `<meta name="description">`, and the card blurb unless `dek` is set |
| `lead` | yes | The large opening paragraph |
| `note` | no | The small closing note under the rule |
| `og_title` · `og_description` | no | Override the Open Graph tags; both default to the above |
| `dek` | no | Front-page card blurb, when it should differ from `description` |
| `card_kicker` | no | Front-page card kicker, when it should differ from `kicker` |
| `order` | no | Position in the front-page list, lowest first. **Leave it out and the post goes to the top** |
| `metrics` | no | The headline metric band — a list of `num` / `label`, with `accent: true` to pick one out |

A metric band:

```yaml
metrics:
  - num: '242'
    label: 'The accuracy byte'
  - num: '94.9%'
    label: 'What that is'
    accent: true
```

### The body

Ordinary markdown: `##` headings, paragraphs, lists, `*emphasis*`, `**strong**`,
`` `code` ``, links, and fenced code blocks. Each `##` starts a new prose section, which
is the shape every page here has.

Raw HTML works too, and that is how the richer components are written — figures, tables,
pullquotes, inline SVG. A block placed **outside** a `<section class="prose">` runs the
full width of the container; one **inside** a section is capped to the reading measure.
The existing posts mark their sections explicitly:

```html
<section class="prose" markdown="1">

## A heading

Prose, which kramdown renders because of `markdown="1"`.

</section>

<div class="fig-pair">…</div>   <!-- outside a section: full width -->
```

If you write a plain markdown post with no `<section>` markers at all, the layout adds
one section per `##` for you, so the simple case needs nothing.

## Changing the look

Set one value in `_config.yml`:

```yaml
palette: midnight
```

The choices are **`devlog`** (the default — warm paper, burnt amber), **`midnight`**
(steel blue, signal blue accent), **`terminal`** (phosphor green) and **`press`**
(newsprint, press red). Each defines a full light *and* dark set, and every text and
accent colour in all four clears WCAG AA against its own background in both modes.

The colours themselves live in `_data/palettes.yml` — ten values per mode. To make your
own, copy a block, rename it, change the values, and point `palette:` at it. Nothing else
in the site needs to know.

> Jekyll reserves `theme:` for gem-based themes, so the key here is `palette:` — setting
> `theme:` to a colour name would fail the build looking for a gem.

## Previewing locally (optional)

Not required — pushing is enough. If you want to see it first:

```sh
bundle install
bundle exec jekyll serve
```

That uses the `github-pages` gem, the same stack GitHub runs, so a local preview matches
the live build.

## How it works

```
_config.yml                    # site settings, palette choice, and the kramdown options that keep typography literal
_data/palettes.yml             # the named colour palettes
_layouts/post.html             # the post shell: head, masthead, header, metric band, footer
_posts/                        # one markdown file per post — one story each
index.html                     # landing page; the post list is generated from _posts
finds.html                     # standing page: Gen 1 cartridge discoveries
agentgb-progress.html          # standing page: the neural player's arc
terminalgb-performance.html    # standing page: throughput and what exactness costs
projects/                      # one HTML file per project: what it is, what it does, its scores
assets/css/main.css            # the whole design system
assets/img/                    # real captures from the source repos (SVG diagrams are inlined)
```

Posts are markdown. Everything else — the project pages and the three standing pages — is
hand-written HTML with no front matter, which Jekyll copies through untouched. The only
external resource is Google Fonts (IBM Plex Sans + JetBrains Mono).

Posts publish at `/posts/<slug>.html`, the same URLs the site has always used, set by the
`permalink` in `_config.yml`.

`kramdown` is configured not to generate heading ids, curl quotes, or rewrite `--` and
`...`. The pages set their own typography and entities; the renderer leaves both alone.

A project page is a spec sheet: what it is, a metric band of current scores, the feature
surface, a scores table, the gaps, a short milestone timeline, and links to that project's
posts. Narrative belongs in `_posts/`, one story per file.

## Publishing

GitHub Pages builds the `main` branch. Push to `main` and Pages rebuilds within about a
minute.

## Design language

A crossover between the restraint of grownowgames.com and the structured technical
typography of Claude artifact pages:

- **Type** — IBM Plex Sans for body, JetBrains Mono for headings, eyebrows and data.
- **Palette** — warm paper background, white cards, hairline rules, one amber accent.
  Full light and dark, driven by CSS custom properties and `prefers-color-scheme`.
- **Structure** — mono uppercase eyebrow labels, `h2` as small uppercase mono with a
  2px bottom rule, headline metric bands, tables for structured comparison.

## Editorial rule

Every number on this site is one we can stand behind. If a claim cannot be verified
against the source project, it does not get published — and where a figure has gone out
of date, it is corrected against the source rather than annotated as stale.
