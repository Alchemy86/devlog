# Project agent memory

The captain's public engineering blog, served at https://alchemy86.github.io/devlog

## What this is

Static site: the captain's ongoing record of his own work. Its current contents are the
private GB projects (TerminalGB, AgentGB, AtlasGB, PixelGB, GBSelfTest, the Portal) plus three
non-GB projects — Glyphsmith (the logo/house-text generator), ShowReel (the film renderer) and
AsciiWorldEngine (the walkable ASCII city) — the site is **not defined as a Game Boy family** —
the opener and the site-level meta description must stay true as other work is added. Page-scoped
copy naming Game Boy is fine; site-scoped copy that does is not.

Markdown posts + plain HTML + CSS, built by GitHub's own Jekyll. No framework, no JS
dependencies, nothing to run locally. The only external resource is Google Fonts. It must
still work untouched in two years — keep it that way.

## Build / test / deploy

- **Build:** none locally. **GitHub Pages runs Jekyll** (converted 2026-09-03; `.nojekyll`
  is gone). No generated HTML is committed, so nothing can go stale against its source.
- **Test:** none automated. Validate structurally (well-formed HTML, asset paths) and,
  where possible, visually. To render the real thing without a Ruby install:
  `podman run --rm -v "$PWD":/srv:z -w /srv docker.io/library/ruby:3.3 bash -c 'gem install
  bundler -N -q && bundle install --quiet && bundle exec jekyll build -d /srv/_site'`, then
  `python3 -m http.server` from `_site/`. `bundle exec jekyll serve` works if Ruby is local.
- **Deploy:** GitHub Pages serves `main` from the repository root (`source: main /`).
  A push to `main` publishes; Pages rebuilds within ~a minute. Nothing goes live until
  content is on `main`.

## Structure

- `index.html` — landing page: hero, project grid, standing-page cards, post list.
- `finds.html` · `agentgb-progress.html` · `terminalgb-performance.html` — the standing
  pages (see **Standing pages**). Root-level, same self-contained shape as a post.
- `_posts/YYYY-MM-DD-<slug>.md` — one markdown file per post: YAML front matter plus a
  body. Published at `/posts/<slug>.html` (unchanged URLs) by the `permalink` in
  `_config.yml`. **Adding a post is dropping a file in — the index list is generated from
  `_posts`, never hand-edited.** Front-matter fields and the section rule are documented in
  `README.md`; don't duplicate that list here.
- `_layouts/post.html` — the post shell (head, og tags, masthead, post header, metric
  band, closing note, footer). The only place that chrome lives now.
- `_config.yml` — site settings, the `/posts/:title.html` permalink, and kramdown options
  set so it does **not** generate heading ids, curl quotes, or rewrite `--` / `...`. The
  pages carry their own typography and entities; those options are what keep the rendered
  text byte-faithful to the hand-written originals. Don't relax them casually.
- A post body wraps its prose in `<section class="prose" markdown="1">`. Blocks placed
  *outside* a section run the full container width; inside one they are capped to the
  reading measure — `.prose > *` in `main.css` is what makes that distinction visible, so
  placement is a layout decision, not a formatting whim. A plain markdown post with no
  section markers gets one section per `##` from the layout.
- `projects/*.html` — one page per project, same self-contained shape as a post.
  **A project page is a spec sheet, not an essay** — see **Voice and page shape**.
- `assets/css/main.css` — the entire design system, documented inline. It is now
  Liquid-processed (front matter at the top): the ten colour tokens in `:root` and in the
  `prefers-color-scheme: dark` block are filled from `_data/palettes.yml`, selected by
  `palette:` in `_config.yml`. **`devlog` is the default and renders byte-identical to the
  hand-written original** — verify that with `cmp` after any change here. The key is
  `palette:`, not `theme:`; Jekyll reserves `theme:` for gem themes and a colour name there
  fails the build. Everything below the token blocks is ordinary CSS — keep it that way,
  since `{{` or `{%` anywhere in this file would now be parsed as Liquid.
- `_data/palettes.yml` — four named palettes (`devlog`, `midnight`, `terminal`, `press`),
  each with a full light and dark set. All clear WCAG AA (lowest measured 5.48:1) in both
  modes; keep any new one to that bar.
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
- `projects/agentgb.html` → `agentgb/` (the neural player). AgentGB is the site's
  **flagship** (set 2026-08-29): `index.html` carries a full-width `.feature-banner`
  above `#projects` (CSS at the bottom of `main.css`, "Feature banner") linking straight
  to this page, image `assets/img/agentgb/pixel-observation.png` (see the Brock gotcha
  below for why this isn't `brock-swarm-poster.png` any more). The project page is
  the hub — its own "Writing" section groups AgentGB posts into four chapter `.card`s
  rather than one flat list; add the next post by dropping a new `<li>` into whichever
  chapter it belongs to, or a new chapter `.card` if it doesn't fit one.
  **`AGENTS.md` in the agentgb repo runs ahead of its own polished `docs/` and
  `README.md`** — when a figure disagrees between them, `AGENTS.md`'s mtime wins; check
  it first, not last. As of 2026-08-31 the committed chain is **twenty-one links**
  (through `buy-pokeballs`, three more than the prior `north-out-of-pallet-again`
  headline): **600/600 cold boots**, N=600, record
  `pixel-chainchamberedheal-n600-floor092-LANDING.json`, seed 42. It does not reach
  Pewter and has not fought Brock. Two mechanisms shipped the same day: **NoEffectDecay**
  (a confidence gate above 0.80 took the argmax, and a no-op on a static screen could
  never unlock it — 14/14 recorded failures across three 600-run sweeps were this one
  bug; the fix subtracts a flat amount from a repeated no-op action's logit, taking
  594/600 to 600/600) and **chambered goals** (an arm condition read from cartridge
  memory decoupled from a fire condition read from the screen — 306/600 runs now detour
  to a Pokémon Center and heal mid-chain at zero cost). Both are written up in
  `posts/exponential-decay-of-belief.html`. Per-milestone median decisions and the
  diagnostic fields (`whole_chain`, `links_completed_histogram`, `stopped_at`,
  `stopped_in_mode`, `wild_battle_trap`) are read straight out of the certification JSON
  (e.g. under a `pokemon-run-*` scratch dir, `policy_sha256` checked against
  `models/pixel-student.npz`) — re-derive from a fresh JSON, don't requote. **Save-state
  size is `~142 KB`, not the `170 KB` figure in `docs/no-pixels.md`** — the agentgb
  repo's own `AGENTS.md` style guide flags that file as the stale one; use 142 KB.
  The recogniser write-up published as `posts/teaching-a-network-to-notice.html` was
  authored in the agentgb repo (`docs/writing/teaching-a-network-to-notice.md`, commit
  `4d9c5fe`) and republished here; that in-repo copy stays as the record. Its six montages
  are `assets/img/agentgb/recogniser-*.png`, copied from the repo's
  `docs/media/recognisers/` and renamed with the `recogniser-` prefix to disambiguate
  inside the shared agentgb image folder. The full-frame recogniser's **118,290**
  parameters is a *different network* from the student's 118,806 inference core and is not
  a variant of the `118,291` transcription slip below: it is the same trunk with a 2-class
  head instead of the 6-way one (118,806 - 774 + 258 = 118,290).

  The engine-drift story (a TerminalGB commit silently flipping the default render
  engine, costing the chain 41/50=82% against the pinned 50/50=100%, at the prior
  18-link length) is documented in the agentgb repo's `docs/emulator-pin.md`, closing
  section.
  **Gotcha, found 2026-08-31: `assets/img/agentgb/brock-swarm-poster.png` and
  `assets/video/agentgb/brock-battles-swarm-mobile.mp4` are stale.** The poster's own
  baked-in overlay reads "link 17 of 17" and "BROCK: 600 BATTLES AT ONCE" — evidence of
  a longer chain concept that no longer matches the committed chain (21 links, ending at
  `buy-pokeballs`, no Brock fight). Removed from `index.html`'s feature banner and from
  the project page; do not reintroduce a Brock claim from these two files without
  re-verifying against the agentgb repo first. New AgentGB media:
  `assets/video/agentgb/mapswarm-mobile.mp4` (600-agent map swarm, re-encoded at 60fps
  from `mapswarm600-full.mp4` under `pokemon-run-h5/evaluation/chain/` — mobile cuts of
  AgentGB swarm/chain footage are 60fps here, not the 30fps convention the agentgb
  repo's own `docs/media/README.md` uses, per the captain's standing instruction that a
  walk cycle never drops below 60fps) and `assets/img/agentgb/parcel-latch-grid.png` (a
  full-res frame from `pixel-chain-gridcoldboot-overlay-proof-highlight.mp4` under the
  same dir, captured on a development checkpoint named on the frame itself, not the
  shipped weights — caption accordingly).
- `projects/atlasgb.html` → `atlasgb/`.
- `projects/pixelgb.html` → `mapgb/`. **Gotcha:** the dir is `mapgb` but the project was
  renamed to **PixelGB** (crate `pixelgb`, repo `Alchemy86/PixelGB`). It is the
  picture-extraction project and is NOT AgentGB — the brief's "AgentGB/PixelGB" conflated
  two separate projects.
- `projects/gbselftest.html` → `gbselftest/`.
- `projects/terminalgb-portal.html` → `terminalgb-portal/`.
- `projects/glyphsmith.html` → `glyphsmith/` (repo `Alchemy86/Glyphsmith`, public — the only
  source repo that isn't private). The logo/house-text generator every other project's mark is
  drawn with; `glyphsmith coverage`, `python3 gallery/verify.py` and `python3 -m pytest tests/`
  are the commands that back its numbers (79 glyphs / 24 inherited / 55 drawn here, 14/14 marks
  byte-identical, 302 tests, as of commit `18fe3d0`, 28 Aug 2026). SVGs on the page are copied
  byte-for-byte from `brand/`, `specimen/` and `gallery/originals/` — never re-rendered; the two
  specimen sheets (the full alphabet, and the ten-icon library added in `18fe3d0`) live at
  `assets/img/glyphsmith/alphabet-specimen.svg` and `icons-specimen.svg`, renamed from the
  source repo's `specimen/alphabet.svg` / `specimen/icons.svg` to disambiguate from the other
  projects' own logo/icon files already in that folder. **`@` is deliberately not a glyph** —
  it's one of five rejected marks (`@ ¢ ° ÷ ±`) documented in `docs/alphabet.md`; a briefed list
  of "new characters" that includes `@` is wrong and should be checked against
  `glyphsmith.alphabet.GLYPHS` before publishing.
- `projects/showreel.html` and `posts/the-number-that-could-have-sunk-it.html` /
  `posts/the-one-clean-miss.html` / `posts/the-chiptune-that-outgrew-its-blog-post.html` →
  `showreel/` (repo `Alchemy86/ShowReel`, private — one of
  three non-GB pages on this site, with Glyphsmith and AsciiWorldEngine). `docs/performance.md`,
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
  Generated music (commit `64475d6`, 28 Aug 2026) is `src/music.rs`, not a `src/music/` dir —
  re-`wc -l` before requoting a line count, same reason as the crate's own `src/`. It ports
  `chiptune.py` from this repo's `assets/video/asciiworldengine/` (a throwaway asset script,
  committed there first at 114 lines; it later grew to 193 when the AsciiWorldEngine lift film's
  cut needed the chiptune arranged rather than looped — re-`wc -l` that file too, don't requote
  114 as current). The 7ms-to-downbeat and 0.9997/0.9999 correlation figures are asserted in
  ShowReel's own `README.md` and commit message, not independently re-derivable from a script in
  this repo — cite them from there. `assets/video/showreel/music-demo-mobile.mp4` and its poster
  are ShowReel's own `docs/music-demo.mobile.mp4`, copied byte-for-byte (`sha1sum`) — a render of
  `examples/music_demo.film.jsonc`, ships no assets of its own.
- `projects/asciiworldengine.html` → **`asciicity/`** (repo `Alchemy86/AsciiWorldEngine`; the
  local dir is named `asciicity`, not `asciiworldengine` — a mismatch between the project's brand
  and its repo dirname, not a typo to "fix" back), made **public** on 2026-08-28 — the second
  public source repo after Glyphsmith, so this page links to it directly; that is a deliberate
  exception to the "no page links to a private repo" convention above, not a precedent for the
  still-private ones). `docs/performance.md` backs the frame-cost table; `src/registrations.txt`
  backs the one passing line that the traffic carries real registrations (the page no longer
  features plates — the captain cut that back on 2026-08-28: a passing reference only, no
  legibility write-up, no dedicated screenshots). Line/module count is
  `find src -name '*.rs' | xargs wc -l` — re-count before requoting, same reason as ShowReel (was
  14,785 lines / 18 modules as of commit `cdfe484`, 28 Aug 2026 — it grows every session). The
  opening leads with the three things the captain named — Rust, runs in your terminal,
  seed-generated — plus a pasteable `git clone … && ./play`. Seed determinism is real and verified
  in `src/rng.rs` (every cell is `hash3(coord, seed)`; "a seed is a promise, not a hint"). The
  `seed-42.png` / `seed-1337.png` comparison pair are `--vista --seed N --at 0,0 --cols 200 --rows
  44` captures (same viewpoint, two seeds), `.svg` rendered to PNG and quantised to 256 colours.
  `city-street.png`, the repo's own earlier committed still, was retired from the page on
  2026-08-29 in favour of a `--view blocks` capture of the street (see below) — do not re-add it
  without also re-deciding which look the page's hero street shot should show.

  **The `--view` mode** (commit `cdfe484`, 28 Aug 2026) added `--view classic|blocks|middle`, a
  run parameter read the same way `--weather` is and cycled live with `B`: `blocks` fills the
  frame buffer's existing per-cell background plane (dead code before this, wired end to end but
  never written to) behind every surface; `middle` fills buildings only. The fill is derived at
  `Grid::put` from the glyph's own hue (`shade(rgb)`, a flat `render::BLOCK_SHADE` = 0.30
  downscale) and stores nothing new on the world model. `docs/base-colour.md` is the study that
  preceded it (commit `2c8b608`) and carries the *why a mode, not a flag* reasoning — read that,
  not just the commit message, before writing anything about this feature again. `tools/bench-view.sh`
  is the project's own tool for both comparisons this feature needs (engine before/after via
  `git archive`, and classic-vs-blocks on one binary) — use it rather than hand-rolling a
  benchmark; it warns on the load average itself. The render also got faster in the same commit
  (two per-row hoists in `sky` and `ground`, found while profiling the fill's cost) — current
  baseline is **0.537 ms/frame** street / **0.517 ms indoors** / **1,860 fps** ceiling / 207 cells
  kept by the occlusion cull, all from `docs/performance.md`, re-verify before requoting as these
  move with every render change. Post: `posts/three-bytes-a-cell-doing-nothing.html`, which
  independently re-ran `tools/bench-view.sh` rather than quoting the doc figures — its numbers
  (−4.7% engine, +19.2% blocks-over-classic) were measured on a moderately loaded machine (load
  ~7–8, not the settled <0.5 the project's own docs ask for) and differ slightly from the
  project's own settled-machine figures for that reason; both are real, neither is wrong.

  The lift-ride video (recut as a FILM 2026-08-28) is the page's marquee. It ships as
  `assets/video/asciiworldengine/lift-ride.mp4` — a 720p `<video controls preload="metadata"
  poster=…>` (ShowReel pattern, copied from `projects/showreel.html`), ~4.6 MB, WITH audio; the
  poster is `assets/img/asciiworldengine/lift-ride-poster.png`. It is no longer one clip: it is a
  30 s sequence the captain shot-listed — open on a bare terminal, `./play` types itself out, a
  hard cut to the city, walk the avenue and look up the towers, then into the lift and up over the
  rooftops. Everything about how it was made lives in `lift-ride.assets.md` alongside; read that
  before touching it. The load-bearing facts, so they are not re-broken:

  - **The ride looks UP-and-OUT at the skyline, never down at the floor.** The captain's whole
    note on the first cut was "we're half looking at the floor". The `--lift` mode's `face_street`
    pose pitches DOWN (−0.42) — that is the bug, not the fix. Ride pitch here is a ramp from
    `+0.03` at the pavement to `−0.20` up by the rooftops (level leaves empty sky over the skyline
    at the top; down puts the floor back in). Judge any recut by eye: more floor than sky is wrong.
  - **Two captures, both real engine, seed `0xACC17`** (default — one city for street, tower and
    lift): `street-capture.mp4` from the shipped `--film --script` recorder (`docs/film.md`),
    `lift-ride-capture.mp4` from a private `--ride-film` mode on a scratch clone (walk in, one
    `ACT` press, face the outward glass, write every tick of the hands-free climb). Both are 720p
    CRF 23 — ShowReel SOURCE, not delivery. The scratch mode is not committed (same footing as the
    prior `--ride-shot`); the pose and pitch ramp are in `lift-ride.assets.md`.
  - **The chiptune is arranged to the cuts**, not laid under them: sparse intro under the terminal,
    a riser, the band dropping in with a crash on the reveal cut (`--drop 3.75`), a resolve at the
    end. `chiptune.py` is now seeded (`np.random.seed`), so `lift-chiptune.wav` reproduces
    byte-for-byte from it — `sha1sum` the two to check. Self-authored, public domain.
  - **The film is `lift-ride.film.jsonc`** (1280×720), the terminal built from `text` layers with a
    `chars` entrance (the typing) and two transitions with taste — a `cut` for the boom, a
    `cross-blur` for the look-up→lift bridge. Rendered `showreel render … --crf 36 -o lift-ride.mp4`
    (CRF 36 because dense ASCII is expensive to compress; keeps it to a few MB).

  NOTE: an agent cannot literally hear audio — verify a soundtrack by ffprobe (stream present),
  `volumedetect` (a sensible level, no clip) and a `showspectrumpic` spectrogram (real rhythm, not
  noise), and say so plainly rather than claiming you listened.

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

**Layout gotcha:** `.prose > * { max-width: var(--measure) }` (78ch) caps figures *and*
`.fig-pair`, so a side-by-side pair inside `.prose` gets ~390px columns. Fine for the wide,
short before/afters `.fig-pair` was built for (271-colours' 1000x572 pair); it shrinks a tall
montage to half its native width and the in-image labels stop being readable. A one-off
`style="max-width:none;"` on that `.fig-pair` gives it the full 1000px container instead —
inline styles on a `figure` are already site convention (`posts/*.html` uses
`style="margin-inline:auto;"`). Two 678px-wide images still cannot both be native side by
side; the comparison has to carry on gestalt, with the specifics stated in the figcaptions.

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

A short, silent hero loop can also ship as a plain `<img>` GIF instead of a `.clip-auto`
`<video>` — a GIF autoplays and loops on its own with no CSS or `prefers-reduced-motion`
handling needed, so it is the simpler choice when the source is already going through
ShowReel's own `showreel gif` export (palette-optimised, generated from the actual footage).
Reach for a `<video>` when a clip has audio or real length: a short silent loop is a `.clip-auto`
`<video>` (or a GIF); a longer clip with sound gets `<video controls preload="metadata"
poster=…>` and no `autoplay` — `projects/asciiworldengine.html`'s lift-ride clip is that case
(720p, a synthesised chiptune in it — see the lift-ride block under **Source repositories**).

## Project-grid wordmarks (added 2026-08-28)

`index.html`'s project cards show each project's real Glyphsmith wordmark, not plain
text: `<img class="pc-name" src="assets/img/glyphsmith/<slug>-logo.svg" alt="<Project Name>">`,
CSS-fixed at `height: 40px; width: auto` (`.project-card .pc-name` in `main.css`) so the grid
stays even — each SVG's own aspect ratio (1200×380 for most, 1400×420 for ShowReel and
AsciiWorldEngine) decides its width. `alt` is the bare project name only (not a motif
description) since the image stands in
for the heading text a screen reader or images-off browser would otherwise show. The mark's own
panel background (`#0d1117`, fixed regardless of accent) is baked into every file and is
designed to sit on both the light and dark page background — that's the family palette, not a
theme bug; see `glyphsmith/glyphsmith/palette.py` in the source repo.

Eight of the nine SVGs (AsciiWorldEngine included) already lived at
`assets/img/glyphsmith/<slug>-logo.svg` (copied for `projects/glyphsmith.html`'s own gallery —
see **Source repositories** above). TerminalGB Portal had no mark anywhere. It was generated
fresh with Glyphsmith's own public API (not by editing
the CLI's default fit, which overflows badly at 1200px wide for an 18-character word) —
`Mark(word="TERMINALGB PORTAL", tagline="TRADE OVER THE WEB", accent="dmg",
content_width=1000, cap_y=110)`, `dmg` reused because Portal ships on top of TerminalGB. It has
**no motif** — every other mark's motif (block cursor, D-pad, region bar, …) is bespoke code
specific to that project's own concept, and inventing one for Portal would be guessing at a
visual metaphor, not reading one out of a source repo. A motif-less `Mark` is first-class
Glyphsmith output (the CLI itself prints a note explaining the icon is a bare panel in that
case, not an error), so this is the honest result, not a placeholder. Its icon variant is
generated the same way but is a bare panel with nothing in it — not committed, since nothing on
this site would use it; regenerate from the `Mark(...)` call above if a use appears.
Project pages do **not** carry these marks in their hero — `projects/glyphsmith.html` sets the
precedent by keeping its own hero plain-text `<h1>` and showing its wordmark later as an
explained `<figure>` with a caption, not as hero furniture; the hero is prose-and-metrics only
per **Voice and page shape**, so a logo image there would be shoehorned.

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
`n_actions 6`, `observation "screen"`. `assets/img/agentgb/pixel-network.png` bakes in
this exact arithmetic (`1,616+4,640+9,248+102,528+774 = 118,806`, "every parameter that
ships") and is drawn live from the policy object, so it's the fastest way to re-check
this figure without loading the file yourself.

**Gotcha, found 2026-08-31:** a firstmate-supplied facts sheet gave this network's
weight count as `118,291` — arithmetically unreachable from the architecture it itself
described (three stride-2 convs 16/32/32, 800→128 dense, 6-way softmax; that shape only
ever sums to 118,806) and for the same sha256-identified file as above. Treated as a
transcription slip and not published; `projects/agentgb.html` and `index.html` use
118,806. If a future facts sheet repeats `118,291`, re-derive from the npz or from
`pixel-network.png` rather than trusting the sheet.

## Local preview and verification

`python3 -m http.server` from the repo root, then screenshot with headless Chrome:

```sh
google-chrome --headless --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size=1280,16000 --virtual-time-budget=8000 --screenshot=out.png <url>
```

**Dark mode in headless Chrome is `--blink-settings=preferredColorScheme=0`** (0 = dark,
1 = light). `2` is not an error and not dark — it silently renders light, so a "dark mode"
check written with `2` is really a second light-mode check.

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
