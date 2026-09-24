#!/usr/bin/env python3
"""Generate the toolbar icons for Notion AI Usage.

A white gauge ring, roughly three-quarters filled, on a rounded square in the
extension's accent colour. The solid badge is deliberate — same reasoning as
Chat Sweeper's: a bare glyph vanishes against one Chrome theme or the other,
and this has to stay findable in the toolbar at 16px.

The ring is drawn as filled pies with the middle punched back out in the
accent colour, which is cheaper and cleaner than stroking an arc. Run:

    python3 generate_icons.py
"""

from PIL import Image, ImageDraw

S = 1024                       # supersampled master
ACCENT = (107, 91, 214, 255)   # #6b5bd6 — deliberately not Chat Sweeper's orange
TRACK = (150, 138, 226, 255)   # the unfilled part of the gauge
WHITE = (255, 255, 255, 255)
CLEAR = (0, 0, 0, 0)
SIZES = [16, 32, 48, 128]

FILLED = 0.72                  # matches the "% used" this thing exists to show


def compose():
    canvas = Image.new("RGBA", (S, S), CLEAR)
    d = ImageDraw.Draw(canvas)

    d.rounded_rectangle([0.02 * S, 0.02 * S, 0.98 * S, 0.98 * S],
                        radius=0.22 * S, fill=ACCENT)

    outer = [0.18 * S, 0.18 * S, 0.82 * S, 0.82 * S]
    inner = [0.34 * S, 0.34 * S, 0.66 * S, 0.66 * S]

    d.ellipse(outer, fill=TRACK)                                  # full track
    d.pieslice(outer, start=-90, end=-90 + 360 * FILLED, fill=WHITE)   # used
    d.ellipse(inner, fill=ACCENT)                                 # punch centre

    return canvas


def main():
    master = compose()
    for n in SIZES:
        master.resize((n, n), Image.LANCZOS).save(f"icon{n}.png")
        print(f"wrote icon{n}.png")


if __name__ == "__main__":
    main()
