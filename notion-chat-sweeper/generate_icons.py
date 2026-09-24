#!/usr/bin/env python3
"""Generate the toolbar icons for Notion Chat Sweeper.

A white broom on a rounded square in the panel's accent colour. The solid
badge is deliberate: a bare glyph disappears against one Chrome theme or the
other, and this has to stay findable in the toolbar at 16px.

Drawn upright at 8x, rotated, then downsampled — cheaper than fighting
anti-aliasing on the diagonal. Run:  python3 generate_icons.py
"""

from PIL import Image, ImageDraw

S = 1024                      # supersampled master
ACCENT = (224, 120, 90, 255)  # #e0785a, same as the panel's Delete button
WHITE = (255, 255, 255, 255)
CLEAR = (0, 0, 0, 0)
SIZES = [16, 32, 48, 128]


def broom():
    """An upright broom, centred, on transparency."""
    img = Image.new("RGBA", (S, S), CLEAR)
    d = ImageDraw.Draw(img)

    # handle
    d.rounded_rectangle([0.455 * S, 0.115 * S, 0.545 * S, 0.570 * S],
                        radius=0.045 * S, fill=WHITE)
    # binding where the bristles are lashed on
    d.rounded_rectangle([0.350 * S, 0.535 * S, 0.650 * S, 0.640 * S],
                        radius=0.032 * S, fill=WHITE)
    # bristles, fanning out
    d.polygon([(0.358 * S, 0.630 * S), (0.642 * S, 0.630 * S),
               (0.740 * S, 0.895 * S), (0.260 * S, 0.895 * S)], fill=WHITE)

    # two gaps cut back out of the bristles — alpha 0 overwrites, it doesn't blend
    for x0, x1 in ((0.443, 0.470), (0.530, 0.557)):
        d.polygon([(x0 * S, 0.700 * S), (x1 * S, 0.700 * S),
                   ((x1 + 0.020) * S, 0.900 * S), ((x0 - 0.020) * S, 0.900 * S)],
                  fill=CLEAR)
    return img


def compose():
    canvas = Image.new("RGBA", (S, S), CLEAR)
    ImageDraw.Draw(canvas).rounded_rectangle(
        [0.02 * S, 0.02 * S, 0.98 * S, 0.98 * S], radius=0.22 * S, fill=ACCENT)

    glyph = broom().rotate(-35, resample=Image.BICUBIC, expand=False)
    scale = 0.76
    small = glyph.resize((int(S * scale), int(S * scale)), Image.LANCZOS)
    off = (S - small.width) // 2
    canvas.alpha_composite(small, (off, off + int(0.01 * S)))
    return canvas


def main():
    master = compose()
    for n in SIZES:
        master.resize((n, n), Image.LANCZOS).save(f"icon{n}.png")
        print(f"wrote icon{n}.png")


if __name__ == "__main__":
    main()
