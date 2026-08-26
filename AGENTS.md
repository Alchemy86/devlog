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
  repo inverts this — the failing line is **Bulbasaur** (`177/300`, and all `123`
  failures end in a battle on Route 1), while Squirtle and Charmander are `300/300`.
  A `300/300` whole-chain headline existed but on `fix9s0`, uncommitted weights that no
  longer exist, so the page quotes the committed `177/300` instead.

  **Three corrections found on 2026-08-26, after the page had already published them —
  re-check these before touching `projects/agentgb.html`:**
  1. `177/300` is **not** "a natural starter spread". It was measured under **argmax**,
     where the entry tile reads `right` at probability `1.0000` / `0.0000` bits of
     entropy, so every one of the 300 boots takes the *same* starter. `AGENTS.md` in the
     agentgb repo is explicit: "the published 177/300 = 59.0% is an argmax figure and is
     not the number a sampled run should be judged against."
  2. The per-starter `300/300` figures are **separately trained arms** (`squirtb-s0`,
     `ctl-s0`), one seed each — *not* the shipped network with its starter forced. Both
     were staged and removed on the captain's "one model only, the varied one" ruling.
  3. `177/300` belongs to `ball3b-s0` and is **stale relative to what ships**. The
     committed student is several generations later (goal-conditioned `parcelroute`
     lineage, plus adapters) and **no later arm has an N=300 chain run at all**. The
     agentgb README carries this as a standing block quote; do not publish `177/300` as
     "what the student that ships does".

  The current re-runnable figure for the committed weights is `starter-choice.md` §9:
  `models/pixel-student.npz` on `take-a-starter`, N=500 sampled at T=1.0 — Bulbasaur 254
  / Charmander 118 / Squirtle 127, reaching the goal `499/500 = 99.8%`.

  General lesson: this repo names its models, and a rate without a model name attached is
  not a verified rate. Always carry the `.npz` identity alongside the number.

When building a project page or post, verify each briefed number against the source
repo (`~/Github/firstmate/projects/<project>/`) before publishing it.

## Source repositories (which page is backed by which repo)

Project pages live in `projects/` and draw their facts from private repos under
`~/Github/firstmate/projects/`:

- `projects/terminalgb.html` → `gameboy/` (the emulator is named **TerminalGB**; the
  repo/dir is `gameboy`).
- `projects/agentgb.html` → `agentgb/` (the neural player).
- `projects/atlasgb.html` → `atlasgb/`.
- `projects/pixelgb.html` → `mapgb/`. **Gotcha:** the dir is `mapgb` but the project was
  renamed to **PixelGB** (crate `pixelgb`, repo `Alchemy86/PixelGB`). It is the
  picture-extraction project and is NOT AgentGB — the brief's "AgentGB/PixelGB" conflated
  two separate projects.
- `projects/gbselftest.html` → `gbselftest/`.
- `projects/terminalgb-portal.html` → `terminalgb-portal/`.

## Git / accounts

Pushes to this repo need the **Alchemy86** GitHub account, not RT-Aaron. No AI
attribution in commits, PRs, or docs — this is a standing instruction and is about
credit only (documenting an AI feature is fine; crediting an AI as author is not).
