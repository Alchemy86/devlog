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
index.html                     # landing page + post list
posts/                         # one HTML file per post
assets/css/main.css            # the whole design system
assets/img/                    # post images (SVG diagrams are inlined)
.nojekyll                      # serve files as-is, skip Jekyll processing
```

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
against the source project, it does not get published.
