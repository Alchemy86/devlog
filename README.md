# devlog

The captain's public engineering log — detailed technical breakdowns of the core
Game Boy work (TerminalGB, AgentGB, AtlasGB). The source repositories are private;
this site is where the work becomes visible, with real numbers and honest trade-offs.

**Live:** https://alchemy86.github.io/devlog/

## How it works

Plain static HTML and CSS. No build step, no framework, no CMS, no JavaScript
dependencies. The only external resource is Google Fonts (IBM Plex Sans + JetBrains
Mono). It is designed to still work untouched in two years.

```
index.html                     # landing page: projects, standing pages, post list
finds.html                     # standing page: Gen 1 cartridge discoveries
agentgb-progress.html          # standing page: the neural player's arc
terminalgb-performance.html    # standing page: throughput and what exactness costs
projects/                      # one HTML file per project: what it is, what it does, its scores
posts/                         # one HTML file per post — one story each
assets/css/main.css            # the whole design system
assets/img/                    # real captures from the source repos (SVG diagrams are inlined)
.nojekyll                      # serve files as-is, skip Jekyll processing
```

A project page is a spec sheet: what it is, a metric band of current scores, the
feature surface, a scores table, the gaps, a short milestone timeline, and links to that
project's posts. Narrative belongs in `posts/`, one story per file.

## Publishing

GitHub Pages serves the `main` branch from the repository root. To publish a change,
merge it to `main` — Pages rebuilds automatically. There is nothing to compile.

## Adding a post

1. Copy an existing file in `posts/` as a starting point — it already wires up the
   fonts, stylesheet, masthead and footer.
2. Write the body using the design-system building blocks documented in
   `assets/css/main.css` (`.eyebrow`, `h2` bordered headings, `.metrics` bands,
   `.callout`, `figure`, tables).
3. Add a `<li>` entry to the post list in `index.html`.

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
