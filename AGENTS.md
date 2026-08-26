# Project agent memory

The captain's public engineering blog, served at https://alchemy86.github.io/devlog

## What this is

Static site documenting the private GB projects (TerminalGB, AgentGB, AtlasGB).
Plain HTML + CSS, no build step, no framework, no JS dependencies. The only external
resource is Google Fonts. It must still work untouched in two years — keep it that way.

## Build / test / deploy

- **Build:** none. There is nothing to compile.
- **Test:** none automated. Validate structurally (well-formed HTML, asset paths) and,
  where possible, visually. Preview locally with `python3 -m http.server` from the repo
  root.
- **Deploy:** GitHub Pages serves `main` from the repository root (`source: main /`).
  A merge to `main` publishes; Pages rebuilds within ~a minute. `.nojekyll` is present
  so files are served as-is. Nothing goes live until content is on `main`.

## Structure

- `index.html` — landing page + post list.
- `posts/*.html` — one self-contained file per post (each wires its own fonts, CSS,
  masthead, footer). Add a new post's `<li>` to the list in `index.html`.
- `assets/css/main.css` — the entire design system, documented inline.

## Design system (do not drift)

Crossover of grownowgames.com restraint and Claude-artifact technical typography:
IBM Plex Sans body + JetBrains Mono for headings/eyebrows/data; warm paper `#F3F5EE`,
white cards, hairline `#DDE1D4`, one amber accent `#A8431F`; mono uppercase eyebrows;
`h2` = small uppercase mono with a 2px bottom rule (the signature move); metric bands;
tables for comparison. Full light + dark via CSS custom properties and
`prefers-color-scheme`. 1000px container, ~66ch prose measure, ~52px section rhythm.

## Editorial rule (non-negotiable)

Every number on the site must be verifiable against the source project. If a claim
cannot be checked, it does not get published — this holds even against a remembered
figure. When the source disagrees with a briefed number, the source wins and the
discrepancy is surfaced. Several briefed figures did not survive verification and were
corrected against the repos:

- TerminalGB double-speed: brief said `7,672 → 56`; source has no such figures. The
  post uses the real `2,304 → PASS` (AGE `m3-bg-lcdc-ds@cgbBCE`).
- AgentGB: brief said `29/30` cold boots with "one Squirtle run fails on Route 1". The
  repo inverts this — the shipped student is `177/300 (59%)` on a natural starter
  spread, the **Bulbasaur** line is what fails on Route 1 (123/123 failures), and the
  **Squirtle** line is `300/300`. A `300/300` chain existed but on uncommitted weights
  that no longer exist, so the re-runnable `177/300` is what the page quotes.

When building a project page or post, verify each briefed number against the source
repo (`~/Github/firstmate/projects/<project>/`) before publishing it.

## Git / accounts

Pushes to this repo need the **Alchemy86** GitHub account, not RT-Aaron. No AI
attribution in commits, PRs, or docs — this is a standing instruction and is about
credit only (documenting an AI feature is fine; crediting an AI as author is not).
