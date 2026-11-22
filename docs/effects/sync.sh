#!/usr/bin/env bash
# Brings the Visual Effects shelf (effects.html) up to date with pw-shorts, in one go:
#
#   docs/effects/sync.sh            render what is new or changed, then commit and push to main
#   docs/effects/sync.sh --dry-run  the same, but stop before committing
#   docs/effects/sync.sh --all      re-render every effect, not only the new or changed ones
#
# Every effect is defined once, in the pokewalker repo's
# software/pw-shorts/src/fxgallery.rs (ENTRIES and LEVELS). This script builds
# pw-shorts there and runs `pw-shorts fx-gallery CACHE --sync`, which renders
# only the effects whose preview is missing or whose definition changed since
# it was last rendered (CACHE/stamps.txt). The new previews are copied into
# assets/img/effects/ (the posters recompressed losslessly and checked pixel for
# pixel), files no effect uses any more are removed, and the generated
# effects.json replaces _data/shelves/effects.json. The work happens in its own
# worktree (its own, reset to origin/main on every run), so whatever branch this
# checkout is on is never touched. A push to main publishes the site.
#
#   PW     the pokewalker checkout to build from (default ~/Github/pokewalker-fx-gallery;
#          its branch takes in pokewalker's main before each run)
#   CACHE  where previews are rendered and kept between runs
#          (default ~/Github/pokewalker/outputs/fx-gallery)
#   WT     the blog worktree the commit is made in (default ~/Github/devlog-wt/effects-sync)
#   LOCK   heavy jobs queue behind this lock, one at a time, each in a memory-capped scope
#          (default ~/Github/pokewalker/outputs/making-of/.heavy.lock, shared with the film renders)
set -euo pipefail
dry=0 all=0
for a in "$@"; do
  case $a in
    --dry-run) dry=1 ;;
    --all) all=1 ;;
    *) echo "unknown option $a" >&2; exit 2 ;;
  esac
done
blog=$(cd "$(dirname "$0")/../.." && pwd)
PW=${PW:-$HOME/Github/pokewalker-fx-gallery}
CACHE=${CACHE:-$HOME/Github/pokewalker/outputs/fx-gallery}
WT=${WT:-$HOME/Github/devlog-wt/effects-sync}
LOCK=${LOCK:-$HOME/Github/pokewalker/outputs/making-of/.heavy.lock}
mkdir -p "$(dirname "$LOCK")"
capped() { flock "$LOCK" systemd-run --user --scope -q -p MemoryMax="$1" -p MemorySwapMax=0 "${@:2}"; }

echo "1/5 pokewalker: take in main, build pw-shorts"
if [ "$(git -C "$PW" rev-list --count HEAD..main)" -gt 0 ]; then
  git -C "$PW" merge --no-edit -q main
fi
(cd "$PW/software" && capped 8G cargo build --release -q -j 6 -p pw-shorts)

echo "2/5 blog: a fresh worktree on origin/main"
git -C "$blog" fetch -q origin main
if [ -d "$WT" ]; then
  git -C "$WT" checkout -q -f -B effects-sync origin/main
  git -C "$WT" clean -q -fd
else
  git -C "$blog" worktree add -q -B effects-sync "$WT" origin/main
fi
img=$WT/assets/img/effects

echo "3/5 render what is new or changed"
mkdir -p "$CACHE"
if [ ! -e "$CACHE/stamps.txt" ] && [ $all = 0 ]; then
  for f in "$img"/*.webp "$img"/*.png; do
    [ -e "$CACHE/$(basename "$f")" ] || cp -p "$f" "$CACHE/"
  done
fi
[ -e "$CACHE/.synced" ] || touch "$CACHE/.synced"
if [ $all = 1 ]; then rm -f "$CACHE/stamps.txt"; fi
sync_flag=--sync
[ $all = 1 ] && sync_flag=
(cd "$PW/software" && capped 6G "$PW/software/target/release/pw-shorts" fx-gallery "$CACHE" $sync_flag)

echo "4/5 copy into the blog"
changed=()
for w in "$CACHE"/*.webp; do
  b=$(basename "$w")
  if ! cmp -s "$w" "$img/$b"; then cp "$w" "$img/$b"; changed+=("${b%.webp}"); fi
done
for p in "$CACHE"/*.png; do
  b=$(basename "$p")
  [ "$p" -nt "$CACHE/.synced" ] || [ ! -e "$img/$b" ] || continue
  capped 2G magick "$p" -strip -define png:compression-level=9 -define png:compression-filter=5 "$img/$b"
  capped 2G magick compare -metric AE "$p" "$img/$b" null: 2>/dev/null || { echo "$b did not survive recompression pixel for pixel" >&2; exit 1; }
done
touch "$CACHE/.synced"
cp "$CACHE/effects.json" "$WT/_data/shelves/effects.json"
python3 - "$WT/_data/shelves/effects.json" "$img" <<'EOF'
import json, os, sys
used = set()
for e in json.load(open(sys.argv[1])):
    used |= {e["preview"], e["poster"]}
    for l in e["levels"]:
        used |= {l["preview"], l["poster"]}
for f in os.listdir(sys.argv[2]):
    if f not in used:
        os.remove(os.path.join(sys.argv[2], f))
        print("   retired", f)
EOF

echo "5/5 commit and push"
cd "$WT"
git add -A _data/shelves/effects.json assets/img/effects
if git diff --cached --quiet; then
  echo "the shelf is already up to date"
  exit 0
fi
git diff --cached --stat | tail -1
if [ $dry = 1 ]; then
  echo "dry run: staged in $WT, not committed"
  exit 0
fi
names=$(printf '%s\n' "${changed[@]}" | sed 's/--.*//' | sort -u | paste -sd, - | sed 's/,/, /g')
git commit -q -m "Effects shelf: sync from pw-shorts fx-gallery${names:+ ($names)}"
active=$(gh auth status 2>/dev/null | grep -B3 "Active account: true" | grep -o "account [^ ]*" | cut -d' ' -f2 || true)
gh auth switch -u Alchemy86 >/dev/null 2>&1 || true
git push -q origin HEAD:main
[ -n "$active" ] && gh auth switch -u "$active" >/dev/null 2>&1 || true
echo "pushed $(git log --oneline -1)"
