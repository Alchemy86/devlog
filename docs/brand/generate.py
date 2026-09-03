#!/usr/bin/env python3
"""Generate the devlog brand SVGs.

Every letterform is hand-drawn here as a stroked skeleton path -- **no font is
embedded, subset or traced**, so there is no third-party licence in these files.
This is the same approach, the same panel and the same alphabet as TerminalGB's
`docs/brand/generate.py`, AtlasGB's and GBSelfTest's, because the devlog is
where those projects are written up and the marks should read as a family; the
*accent* and the *motif* are the devlog's own.

Run from anywhere:  python3 docs/brand/generate.py
It rewrites `devlog-logo.svg`, `devlog-icon.svg` and `devlog-og.svg`
deterministically.  Edit this file, never the SVGs by hand.
"""

import os

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Palette.  The panel, the border, the wordmark white and the tagline grey are
# TerminalGB's, unchanged -- that is what makes this a sibling and not a
# stranger.  The accent is not: the devlog is not a Game Boy tool, so it does
# not wear the DMG LCD green.  It wears the site's own burnt amber.
#
# Specifically the *dark-mode* amber from `_data/palettes.yml`, not the light
# one.  The panel is near-black, so the light-mode `#A8431F` would sit on it at
# 3.14:1 and fail AA; `#E6935F` sits at 7.84:1.  The palette already solved this
# problem for the site's dark theme and the mark inherits the answer.
BG = "#0d1117"      # near-black panel (matches GitHub dark, works on light)
EDGE = "#30363d"    # faint panel border so the card reads on pure black too
FG = "#f0f3f6"      # wordmark white
GREY = "#8b949e"    # tagline grey
AMBER = "#E6935F"   # devlog accent -- palettes.yml `devlog.dark.accent`

# From the front page's own opening line: "a running record of what gets
# built here".
TAGLINE = "WHAT GETS BUILT HERE"

# ---------------------------------------------------------------------------
# Stroke-skeleton capital letters.  Cap height 100, stroke 26 (half-stroke 13);
# every endpoint is inset 13 so round caps land on the ink edge.  The value is
# (advance width, list of path data).
#
# These are the shapes TerminalGB's, AtlasGB's and GBSelfTest's generators
# already draw, carried over unchanged so all four wordmarks are visibly the
# same alphabet.  Nothing new is drawn here: DEVLOG and WHAT GETS BUILT HERE
# between them need only letters the siblings had already cut.
S = 13
GLYPHS = {
    'T': (72, ["M13 13 H59", "M36 13 V87"]),
    'E': (56, ["M43 13 H13 V87 H43", "M13 50 H36"]),
    'F': (56, ["M43 13 H13 V87", "M13 50 H36"]),
    'R': (68, ["M13 87 V13 H36 A19 19 0 0 1 36 51 H13", "M37 54 L54 87"]),
    'M': (86, ["M13 87 V13 L43 57 L73 13 V87"]),
    'I': (26, ["M13 13 V87"]),
    'N': (64, ["M13 87 V13 L51 87 V13"]),
    'A': (76, ["M11 87 L38 15 L65 87", "M23 62 H53"]),
    'L': (54, ["M13 13 V87 H41"]),
    'G': (70, ["M57 13 H13 V87 H57 V56 H42"]),
    'B': (66, ["M13 13 V87", "M13 13 H35 A18 18 0 0 1 35 49 H13",
               "M13 49 H37 A19 19 0 0 1 37 87 H13"]),
    'O': (64, ["M32 13 A19 37 0 1 0 32 87 A19 37 0 1 0 32 13"]),
    'U': (64, ["M13 13 V68 A19 19 0 0 0 51 68 V13"]),
    'Y': (64, ["M13 13 L32 47 L51 13", "M32 47 V87"]),
    'S': (72, ["M57 13 H36 A23 18.5 0 0 0 36 50 A23 18.5 0 0 1 36 87 H15"]),
    'C': (60, ["M42 18 A19 37 0 1 0 42 82"]),
    'D': (68, ["M13 13 V87", "M13 13 H31 A24 37 0 0 1 31 87 H13"]),
    'P': (62, ["M13 87 V13", "M13 13 H32 A17 18 0 0 1 32 49 H13"]),
    'V': (64, ["M13 13 L32 87 L51 13"]),
    'W': (96, ["M13 13 L33 87 L48 34 L63 87 L83 13"]),
    'H': (66, ["M13 13 V87", "M53 13 V87", "M13 50 H53"]),
    ' ': (30, []),
}
TRACK = 8  # tight letter spacing


def word_width(text, track=TRACK):
    w = 0
    for i, ch in enumerate(text):
        w += GLYPHS[ch][0]
        if i < len(text) - 1:
            w += track
    return w


def draw_word(text, x, y, scale, color, track=TRACK):
    """SVG for `text` with the letter grid's top-left at (x, y)."""
    parts = []
    cx = 0.0
    for ch in text:
        w, paths = GLYPHS[ch]
        for d in paths:
            parts.append(
                f'<path transform="translate({x + cx * scale:.1f} {y:.1f}) '
                f'scale({scale:.4f})" d="{d}" fill="none" stroke="{color}" '
                f'stroke-width="26" stroke-linecap="round" '
                f'stroke-linejoin="round"/>')
        cx += w + track
    return "\n".join(parts)


def svg(width, height, body, comment):
    # "--" cannot appear inside an XML comment, and a mark whose header comment
    # contains one silently fails to parse in every renderer.
    assert "--" not in comment, f"em dash, not two hyphens: {comment!r}"
    return (f"<!-- {comment}\n"
            "     Hand-authored for the devlog. No font embedded, subset or "
            "traced;\n     letterforms are original stroked paths. "
            "Regenerate with docs/brand/generate.py -->\n"
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} '
            f'{height}" width="{width}" height="{height}" role="img">\n'
            f"{body}\n</svg>\n")


def panel(w, h, rx=24):
    return (f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{rx}" '
            f'fill="{BG}" stroke="{EDGE}" stroke-width="2"/>')


def write(name, content):
    path = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as handle:
        handle.write(content)
    print(f"wrote {name} ({len(content)} bytes)")


# ---------------------------------------------------------------------------
# THE MARK.
#
# TerminalGB's motif is a solid block cursor standing where a letter would be;
# AtlasGB's is a four-segment region bar under the wordmark; GBSelfTest's is a
# pass tick leading it.  The devlog keeps the panel, the alphabet, the tight
# tracking and the accent full stop -- that is the family -- and brings its own
# motif: **the margin rule**.
#
# It is not invented for the mark.  It is already in the site: `.pullquote` in
# `assets/css/main.css` is `border-left: 2px solid var(--accent)`, and it is the
# one place the design system marks a passage as worth stopping on.  The mark
# is a whole entry set against that rule -- the wordmark, then the tagline,
# both hanging off one accent line in the margin.
#
# Every sibling centres its tagline under its wordmark.  This one does not, and
# that is the point: a log is left-aligned against its margin, and centring the
# block would put the rule beside nothing.
#
# Nothing here resembles any Nintendo mark, logotype or trade dress; the whole
# vocabulary is a rule, a word and a full stop.

RULE_W = 18     # the margin rule, at the mark's scale
RULE_GAP = 46   # air between the rule and the ink, the way the CSS pads 22px


def margin_rule(x, y, height, colour=AMBER):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{RULE_W}" '
            f'height="{height:.1f}" rx="{RULE_W / 2}" fill="{colour}"/>')


def lockup(W, H, scale, tag_scale, gap):
    """The whole mark -- rule, wordmark, full stop, tagline -- centred in W x H.

    Returns the SVG body.  `gap` is the space between the wordmark's ink floor
    and the tagline's ink ceiling, which is the only thing that changes between
    the 380-tall logo and the 630-tall Open Graph card.
    """
    text = "DEVLOG"
    DOT_R = 16                    # the full stop, bottom-aligned with the ink
    TAG_TRACK = 14                # tagline is wide-tracked, as in every sibling

    word_units = word_width(text) + TRACK + 2 * DOT_R
    word_px = word_units * scale
    tag_px = word_width(TAGLINE, track=TAG_TRACK) * tag_scale
    ink_px = max(word_px, tag_px)

    total_w = RULE_W + RULE_GAP + ink_px
    x0 = (W - total_w) / 2
    tx = x0 + RULE_W + RULE_GAP   # left edge of the letter grid

    # Vertical: stack the two ink bands and centre the pair in the panel.
    #
    # The ink band is the full 0..100 of the letter grid, not the 13..87 the
    # paths run between: the stroke is 26 with round caps, so the cap adds its
    # half-stroke back at both ends. Measuring the paths instead would set the
    # margin rule a half-stroke inside the cap line, which is visible.
    word_ink = 100 * scale
    tag_ink = 100 * tag_scale
    block = word_ink + gap + tag_ink
    ink_top = (H - block) / 2
    y0 = ink_top                          # grid origin sits on the ink ceiling
    ty = ink_top + word_ink + gap

    parts = [panel(W, H, rx=24 if H < 500 else 32)]
    parts.append(margin_rule(x0, ink_top, block))
    parts.append(draw_word(text, tx, y0, scale, FG))
    cx = word_width(text) + TRACK
    parts.append(
        f'<circle cx="{tx + (cx + DOT_R) * scale:.1f}" '
        f'cy="{y0 + (100 - DOT_R) * scale:.1f}" r="{DOT_R * scale:.1f}" '
        f'fill="{AMBER}"/>')
    parts.append(draw_word(TAGLINE, tx, ty, tag_scale, GREY, track=TAG_TRACK))
    return "\n".join(parts)


def logo():
    """The wordmark lockup, 1200x380 -- the sibling marks' own canvas."""
    W, H = 1200, 380
    write("devlog-logo.svg",
          svg(W, H, lockup(W, H, scale=1.70, tag_scale=0.34, gap=46),
              "devlog logo — the margin rule, the wordmark, the full stop"))


def og():
    """The same lockup on a 1200x630 Open Graph card.

    No sibling needs this one: they are repositories, and the devlog is a
    website whose links get unfurled.  1200x630 is the size every unfurler
    crops to, so the mark is drawn at it rather than letterboxed into it.
    """
    W, H = 1200, 630
    write("devlog-og.svg",
          svg(W, H, lockup(W, H, scale=1.95, tag_scale=0.40, gap=76),
              "devlog Open Graph card — the mark at 1200x630"))


def icon():
    """The entry alone -- the margin rule and three lines of an entry beside it.

    Every coordinate is a multiple of 8 inside the 128 box, so at a 16 px
    favicon each unit lands on a whole device pixel: a 2 px accent column and
    three 2 px white rows, the last one short.  That is deliberately unlike the
    siblings at the size where it matters -- TerminalGB's is one tall block,
    AtlasGB's four full-width accent rows, GBSelfTest's a tick -- and none of
    the four can be mistaken for another at 16 px.
    """
    IW = 128
    body = [panel(IW, IW, rx=28)]
    body.append(f'<rect x="24" y="24" width="16" height="80" rx="8" '
                f'fill="{AMBER}"/>')
    for i, w in enumerate((48, 48, 32)):
        body.append(f'<rect x="56" y="{24 + i * 32}" width="{w}" height="16" '
                    f'rx="8" fill="{FG}"/>')
    write("devlog-icon.svg",
          svg(IW, IW, "\n".join(body), "devlog icon — an entry in the margin"))


if __name__ == "__main__":
    logo()
    og()
    icon()
