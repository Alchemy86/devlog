# Project agent memory

The captain's public engineering blog, served at https://alchemy86.github.io/devlog

## What this is

Static site: the captain's ongoing record of his own work. Its current contents are the
private GB projects (TerminalGB, AgentGB, AtlasGB, PixelGB, GBSelfTest, the Portal) plus
Glyphsmith, the logo/house-text generator that is not GB work — the site is **not defined as
a Game Boy family** — the opener and the site-level meta description
must stay true as other work is added. Page-scoped copy naming Game Boy is fine; site-scoped
copy that does is not.

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

- `index.html` — landing page: hero, project grid, standing-page cards, post list.
- `finds.html` · `agentgb-progress.html` · `terminalgb-performance.html` — the standing
  pages (see **Standing pages**). Root-level, same self-contained shape as a post.
- `posts/*.html` — one self-contained file per post (each wires its own fonts, CSS,
  masthead, footer). Add a new post's `<li>` to the list in `index.html`.
- `projects/*.html` — one page per project, same self-contained shape as a post.
  **A project page is a spec sheet, not an essay** — see **Voice and page shape**.
- `assets/css/main.css` — the entire design system, documented inline.
- `assets/img/<project>/` — real captures copied out of the source repos. See **Images**.

## Voice and page shape (non-negotiable, set 2026-08-27)

Load the **`human-writeups`** skill before writing or revising any prose here. It owns
the standard. The captain's verdict on the first version of this site was that it was
"not written like a person", and the rewrite that followed is what the current pages are.
The four failures it names, in the order they showed up here:

1. **Showing your working.** State the finding, not how you counted it. "1,419 entries are
   verified against both the ROM and a live run" — never the `csv.DictReader` sentence.
2. **Meta-commentary about the writing.** Never say what you chose to delete, mark, keep or
   surface. In particular: **never annotate a figure as stale.** Go to the source repo, read
   the current number, and publish it as if it were always the current number.
3. **Defending yourself in prose.** A condition on a number is a few words ("N=150", "load
   1.3"), not a paragraph on why it was measured that way.
4. **Throat-clearing.** Start with the thing.

The structure that follows from it:

- **Project pages lead with what it is, what it does, and its current test scores.** Hero,
  metric band, a `.cards` grid of the feature surface, a scores table, the gaps as
  `ul.gaps`, a short milestone timeline, then links to that project's posts. Nothing else
  earns that space.
- **Every narrative is a post.** A story on a project page is a post trying to escape —
  move it to `posts/` and link it from both the project page and `index.html`.
- **`.provenance` stays** (every project and standing page ends with one) but it is two
  short paragraphs naming the source and the licensing position, not a method write-up.

## Design system (do not drift)

Crossover of grownowgames.com restraint and Claude-artifact technical typography:
IBM Plex Sans body + JetBrains Mono for headings/eyebrows/data; warm paper `#F3F5EE`,
white cards, hairline `#DDE1D4`, one amber accent `#A8431F`; mono uppercase eyebrows;
`h2` = small uppercase mono with a 2px bottom rule (the signature move); metric bands;
tables for comparison. Full light + dark via CSS custom properties and
`prefers-color-scheme`. 1000px container, ~66ch prose measure, ~52px section rhythm.

The long-form project pages added five components to the bottom of `main.css`, in the same
style and using only the existing tokens: `figure.pixel` / `figure.narrow` (real captures),
`.fig-pair` (a before/after pair, stacking under 640px), `figure.code` (a snippet with a
caption), `.pullquote`, and `.provenance` (the "where these numbers come from" strip every
project page ends with). Extend that list rather than inventing a parallel system.

## Editorial rule (non-negotiable)

Every number on the site must be verifiable against the source project. If a claim
cannot be checked, it does not get published — this holds even against a remembered
figure. When the source disagrees with a briefed number, the source wins. **Correct it,
do not caveat it**: read the current value out of the repo and publish that. A stale
figure never gets an annotation saying it is stale (see **Voice and page shape**).
Several briefed figures did not survive verification and were corrected against the
repos:

- TerminalGB double-speed: brief said `7,672 → 56`; source has no such figures. The
  post uses the real `2,304 → PASS` (AGE `m3-bg-lcdc-ds@cgbBCE`).
- TerminalGB conformance: `Mooneye acceptance 13/66` and `SameSuite APU 2/61` are
  historical attribution figures the gameboy repo keeps deliberately ungated — never
  publish them as current. Current, from the baselines (27 Aug 2026): Mooneye acceptance
  **67/75 `standard`, 75/75 `identical`** (all eight fast-engine failures are
  `acceptance/ppu`), SameSuite audio **66/69** in both engines.
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
- `projects/glyphsmith.html` → `glyphsmith/` (repo `Alchemy86/Glyphsmith`, public — the only
  source repo that isn't private). The logo/house-text generator every other project's mark is
  drawn with; `python3 gallery/verify.py` and `python3 -m pytest tests/` are the two commands
  that back its numbers. SVGs on the page are copied byte-for-byte from `brand/`, `specimen/`
  and `gallery/originals/` — never re-rendered.
- `projects/showreel.html` and `posts/the-number-that-could-have-sunk-it.html` /
  `posts/the-one-clean-miss.html` → `showreel/` (repo `Alchemy86/ShowReel`, private, and —
  with Glyphsmith — one of two non-GB pages on this site). `docs/performance.md`,
  `docs/native-encode-audit.md` and `docs/anarchist-study.md` back the project page's figures;
  `examples/kanto_reel.rs` backs the first post. Line/module counts on the project page are
  counted directly from `src/` (`find src -name '*.rs' | xargs wc -l`), not quoted from a doc —
  they grow every session, so re-count before requoting. Two different image conventions
  coexist in `assets/img/showreel/`: `title-card.png`, `bursts.png` and `pull-back-mid.png`
  are real frames pulled with ffmpeg from a render of `kanto_reel.rs`, not from `showreel`'s
  own committed `docs/stills/`; the rest (`browser-editor.png`, `wasm-whole-map.png`,
  `parallax-wide.png`, `parallax-pushed.png`) are `docs/stills/` originals copied straight
  across and re-compressed losslessly (`magick compare -metric AE` against the source must
  print `0`) since they are already real committed captures of the crate's own tooling, not
  of the Kanto example. No page on this site links to `Alchemy86/ShowReel` or to any other
  private repo by URL — none of the project pages do, so that is the standing convention, not
  an oversight.
  The page's lead video is ShowReel's own demo reel — `docs/showreel-reel.mobile.mp4` in the
  source repo, copied byte-for-byte to `assets/video/showreel/showreel-reel-mobile.mp4` (verify
  with `sha1sum`) — rendered by ShowReel itself from `examples/showreel_demo.film.jsonc`. It has
  real audio and runs 52.6s, so it gets `controls` and a poster, never `autoplay`. A Pokémon
  swarm clip rendered by AgentGB's own film tooling briefly led this page; it was moved off
  entirely (it belongs on `projects/agentgb.html`, where it is the only place a battle's map
  position can't show it) because another tool's output at the top of ShowReel's own page
  demonstrated nothing about ShowReel. The same swarm footage now appears inside ShowReel's own
  reel instead, as the "live footage" scene — composited by ShowReel, which is the honest way to
  show it here.

## Standing pages (added 2026-08-27)

Three pages at the repository root accumulate rather than being published once. Each is
linked from `index.html`'s own `#pages` section and follows the same shape: `.page-hero`
with a `.hero-facts` strip, a `.toc` card, sections built from `.tiles` / `.card` /
`dl.spec`, and a closing `.gaps` list plus `.provenance`.

- `finds.html` — Gen 1 cartridge discoveries, one `<section>` per entry, each ending in a
  `dl.spec` with *lives at* / *how it was verified* / *kind*. Source is atlasgb's
  `atlases/pokemon-rb/docs/discoveries.md`. **Append entries; do not renumber existing ones**
  (the `#id` anchors are linked from elsewhere).
- `agentgb-progress.html` — the arc as a `.timeline`, the current standing, and the honest
  gaps. Source is agentgb's `docs/progress.md` (stages 0-8, dated) plus `docs/return-leg-adapter.md`
  and `AGENTS.md` for everything after 24 Aug 2026; `docs/results.md` is **stale** (3 links).
- `terminalgb-performance.html` — throughput and what exactness costs. Source is the gameboy
  repo's `docs/measured/throughput-baseline.md` and `docs/measured/against-the-field.md`.
  **Every throughput figure must carry its load average** — the same binary reads 0.0581 vs
  0.0909 ms/frame between load 0.3 and load 16. The feature surface moved off this page to
  `projects/terminalgb.html` on 2026-08-27; do not duplicate it back.

The design-system additions these needed are at the bottom of `main.css` under
*Extensions for the standing pages*: `.page-hero`/`.hero-facts`, `.toc`, `.sec-head`,
`.tiles`/`.tile`, `.card`/`.card-hd`/`.card-bd`/`.card-ft`/`.cards`, `a.card`, `.chip`,
`dl.spec`, `.gaps`, and `figure.scrollfig` (a wide data SVG scrolls sideways under 700px
instead of shrinking to unreadable — apply it to any SVG wider than about 500px).

## ROM figures re-derived here, and how

Verified against `Pokemon - Blue Version (USA, Europe) (SGB Enhanced).gb` (sha1
`d7037c83e1ae5b39bde3c30787637ba1d4c48ce2`), which lives under the gameboy repo's
`target/` — atlasgb ships no ROM. Re-run these before requoting:

- **NINTEN / SONY**: encode `A`-`Z` as `$80`-`$99` with a `$50` terminator and search the
  whole image — exactly one hit each, at file offsets `0x45AA` and `0x45B1` (= bank 1
  `$45AA`/`$45B1`, since bank 1 maps 1:1). The 18 bytes from `0x45AA` are what the
  byte-map figure on `finds.html` is drawn from.
- **`EvosMovesPointerTable` is at bank `$0E` `$705C`** (file `0x3B05C`), found by property:
  the unique offset in the whole ROM whose 190 consecutive little-endian words all land in
  `$4000-$7FFF` *and* whose records parse as valid evolution/learnset bytes. `PokedexOrder`
  is at file `0x41024`. Parsing gives 580/56 for the naive first-151 read and 728/72 for
  both the `PokedexOrder`-filtered and the all-190 read — all four figures reproduced.
- **Suite scores are countable, not quotable.** Every row of the picture-engine tables on
  `terminalgb-performance.html` and `projects/terminalgb.html` is counted from the gameboy
  repo's `testharness/*baseline*.txt` — split each line on `=` and count values starting
  `PASS`. `*_accurate_baseline.txt` is the `identical` engine; the bare name is `standard`.
  `mooneye_baseline.txt` is acceptance + emulator-only pooled (95/103 standard, 103/103
  accurate). The Shootout figure (243/264, 5th of 19) is **not** baseline-derivable — it
  comes from `docs/shootout.md`.
- **Two different frame-cost pairs exist and they are not interchangeable.** The
  engine-against-engine comparison is `0.373 ms identical / 0.094 ms standard`, picture on,
  one P-core (gameboy `docs/picture-modes.md`). The throughput page's `0.0454` and `0.4962`
  come from `docs/measured/throughput-baseline.md` and are *different configurations*
  (pixels off at load 1.3 versus picture on at load 16) — pairing them as an engine
  comparison overstates the cost by 2.5×.

## Images

Real captures only — never stock art, never an invented screenshot, never a diagram of
something that does not exist. Assets live in `assets/img/<project>/` and are copied out
of the source repos, never re-rendered:

```sh
magick <src>.png -strip -define png:compression-level=9 -define png:compression-filter=5 <dst>.png
magick compare -metric AE <src>.png <dst>.png null:      # must print 0
```

That re-compresses losslessly (typically 40-60% smaller, and 574K -> 12K on one badly
stored file) and the `compare` step is the gate: a copy that is not pixel-identical to the
source does not land. Game Boy screenshots carry `class="pixel"` on the `<figure>`
(`image-rendering: pixelated`) — a four-shade picture must never be smoothed by the
browser, which is the same rule PixelGB and TerminalGB both enforce in code.

AtlasGB has no images of its own. Its chart is an inline SVG built from
`atlases/pokemon-rb/data/atlas.tsv` (tally the `verify` column with `csv.DictReader` +
`collections.Counter`), and the page says so in its own figcaption. Any future
AtlasGB visual has to be generated from that repo's real contents the same way.

## Video (added 2026-08-28)

Real captures only, same rule as images, copied byte-for-byte (`sha1sum` the source and the
copy) rather than re-encoded — re-encoding is a last resort and must be justified and
verified (compare a decoded frame) if it ever happens. Files live in `assets/video/<project>/`,
poster frames are extracted with `ffmpeg -ss <t> -vframes 1` and compressed exactly like any
other PNG (see **Images**). A `<video>` gets `figure` treatment via two rules at the bottom of
`main.css` (*Figures carrying real footage*): plain `figure video { width:100%; height:auto;
... }`, and a `.clip-auto` class for a muted autoplay loop that swaps to a sibling `.clip-poster`
`<img>` under `prefers-reduced-motion: reduce` — pure CSS, no script, matching the rest of the
site.

**Gotcha:** unlike `<img>`, a `<video>`'s `height` HTML attribute resolves as a real CSS height
even when only `width` is styled — `figure video { width:100% }` alone leaves `height` pinned
to the attribute (e.g. a 1280×720 clip stays 720px tall in a 300px-wide column, badly
letterboxed). `height: auto` is required and is already in the rule above; don't drop it.

A video that autoplays only starts once it scrolls near the viewport (Chromium defers
off-screen autoplay to save resources) — expected behaviour, not a bug, and exactly what
`preload="metadata"` is for. Never autoplay anything with real length or unmuted audio;
`.clip-auto` is for a short, silent, loop-forever hero only. A longer clip gets `controls`, a
`poster`, and no `autoplay` attribute at all.

Current example: `projects/showreel.html`'s hero and `projects/agentgb.html`'s swarm-view
figure both draw on AgentGB's own film tooling (`agentgb pixelmapfilm` / `pixelchainfilm`,
`~/Github/firstmate/projects/agentgb/src/agentgb/video.py`) — never imply ShowReel rendered
game footage it didn't; say whose tooling made a clip in its caption.

## Two source-repo docs that disagree with themselves — trust these

Verified 2026-08-26 while writing the project pages; re-check before requoting:

- **agentgb `README.md` § "The student in this repository" is stale.** It still names
  `pixel-fix7-round1` / sha `8963691…` as the committed file. The committed file is the
  goal-conditioned **star pupil**, sha `b2bb79082c88c486c8d6e146be000627a59af3efaa19a9fc75641e957262c109`
  (`git log` commit `e604ec6`, "models: promote the star pupil"). **`models/README.md` is
  authoritative on which weights ship**; `sha256sum models/pixel-student.npz` settles it.
- **mapgb `AGENTS.md` disagrees with `docs/verification.md` twice**, and
  `docs/verification.md` is the one that came out of a run: it is **216 photographed**
  (not 226) and **22 of 248 map ids are placeholders** (not twelve; 248 − 226 = 22).

## Figures verified by counting, not by quoting

`models/pixel-student.npz` loaded with NumPy, summing `.size` over the arrays:
conv1/2/3 = 15,504 · `fc` = 102,528 · `action` = 774 → **118,806** inference core
(86.3% is the single dense layer, 13.1% the three convolutions), plus `film3` 320 and
`goal_head` 3,204 → **122,330** weights and one metadata string in the committed
goal-conditioned file. The file's own `meta` records `in_shape [4, 36, 40]`,
`n_actions 6`, `observation "screen"`.

## Local preview and verification

`python3 -m http.server` from the repo root, then screenshot with headless Chrome:

```sh
google-chrome --headless --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size=1280,16000 --virtual-time-budget=8000 --screenshot=out.png <url>
```

**`chrome-devtools-axi` does not work here** — every `snapshot`/`eval`/`screenshot` fails
with `Invalid arguments ... Required at pageId`, in both the default and a named session.
Use the Chrome command above instead. There is also a structural check worth re-running
after any edit: parse every `.html` with `html.parser` for unclosed/mismatched tags,
resolve every relative `src`/`href` against the filesystem, and assert every `<img>` has
an `alt`.

## Git / accounts

Pushes to this repo need the **Alchemy86** GitHub account, not RT-Aaron. No AI
attribution in commits, PRs, or docs — this is a standing instruction and is about
credit only (documenting an AI feature is fine; crediting an AI as author is not).

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this project.
Do not repeat what the codebase already shows; point to the authoritative file or command instead.
Prefer rewriting or pruning existing entries over appending new ones.
When updating this file, preserve this bar for all agents and keep entries concise.
