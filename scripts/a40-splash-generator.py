from __future__ import annotations
import argparse
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Canvas dimensions for the 12.3" Waveshare
WIDTH = 1920
HEIGHT = 720

# Colors sampled from period A40 Devon / Somerset badge photos
BG = (0, 0, 0)
CHROME_LIGHT = (235, 238, 242)
CHROME = (200, 206, 212)
CHROME_DARK = (130, 136, 142)
ENAMEL_RED = (96, 18, 24)        # Oxblood / maroon vitreous enamel
ENAMEL_RED_HI = (132, 28, 34)    # Highlight side of enamel for depth
ENAMEL_BLUE = (0, 158, 184)      # Robin's egg blue diagonal band
ENAMEL_BLUE_HI = (90, 205, 220)  # Brighter highlight along the band
GOLD = (212, 168, 70)            # Antique gold for '40' and Austin script
GOLD_HI = (245, 215, 130)        # Highlight pass on gold
GOLD_SHADOW = (60, 40, 10)       # Drop shadow under gold


def _load_font(size: int, style: str = "serif") -> ImageFont.FreeTypeFont:
    if style == "cursive":
        candidates = [
            "/System/Library/Fonts/Supplemental/SnellRoundhand.ttc",
            "/System/Library/Fonts/Supplemental/Apple Chancery.ttf",
            "/System/Library/Fonts/Supplemental/Zapfino.ttf",
            "/System/Library/Fonts/Supplemental/Brush Script.ttf",
        ]
    else:
        candidates = [
            "/System/Library/Fonts/Supplemental/Bodoni 72.ttc",
            "/System/Library/Fonts/Supplemental/Didot.ttc",
            "/System/Library/Fonts/Supplemental/BigCaslon.ttf",
            "/System/Library/Fonts/Supplemental/Baskerville.ttc",
            "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        ]

    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()

def _badge_polygon(left, top, right, bottom, foot):
    """Elongated vertical lozenge: flat top, parallel sides, shallow V at bottom.

    `foot` is how far from the bottom edge the V starts (i.e. the height of the
    pointed section at the base).
    """
    cx = (left + right) // 2
    return [
        (left, top),
        (right, top),
        (right, bottom - foot),
        (cx, bottom),
        (left, bottom - foot),
    ]


def _shade_polygon(layer, points, base, highlight, axis="horizontal"):
    """Fill a polygon with a base color, then add a soft highlight gradient.

    Used to fake the wet-enamel look of vitreous color: one side slightly
    brighter than the other.
    """
    draw = ImageDraw.Draw(layer)
    draw.polygon(points, fill=base)

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    bbox = (min(xs), min(ys), max(xs), max(ys))

    grad = Image.new("L", (bbox[2] - bbox[0], bbox[3] - bbox[1]), 0)
    gd = ImageDraw.Draw(grad)
    if axis == "horizontal":
        for x in range(grad.width):
            t = x / max(1, grad.width - 1)
            gd.line([(x, 0), (x, grad.height)], fill=int(40 * (1 - t)))
    else:
        for y in range(grad.height):
            t = y / max(1, grad.height - 1)
            gd.line([(0, y), (grad.width, y)], fill=int(40 * (1 - t)))

    hi = Image.new("RGBA", grad.size, highlight + (255,))
    hi.putalpha(grad)
    layer.paste(hi, (bbox[0], bbox[1]), hi)


def render_splash():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    cx, cy = WIDTH // 2, HEIGHT // 2

    # --- Emblem geometry ---
    w, h = 240, 600
    left, right = cx - w // 2, cx + w // 2
    top, bottom = cy - h // 2, cy + h // 2
    foot = 70  # height of the shallow bottom V

    outer = _badge_polygon(left, top, right, bottom, foot)

    # --- LAYER 1: Stepped chrome bezel (outer dark, mid, inner light) ---
    # Outer dark edge
    draw.polygon(outer, fill=CHROME_DARK)
    # Mid chrome
    step1 = 6
    mid = _badge_polygon(
        left + step1, top + step1, right - step1, bottom - step1, foot
    )
    draw.polygon(mid, fill=CHROME)
    # Inner highlight ring
    step2 = 12
    inner_ring = _badge_polygon(
        left + step2, top + step2, right - step2, bottom - step2, foot
    )
    draw.polygon(inner_ring, fill=CHROME_LIGHT)
    # Enamel well (the actual painted face sits inside this)
    well_inset = 22
    well = _badge_polygon(
        left + well_inset,
        top + well_inset,
        right - well_inset,
        bottom - well_inset,
        foot - 8,
    )

    # --- LAYER 2: Oxblood red enamel base ---
    enamel_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    _shade_polygon(
        enamel_layer, well, ENAMEL_RED, ENAMEL_RED_HI, axis="horizontal"
    )

    # Mask everything inside the enamel well so the diagonal can't escape it
    well_mask = Image.new("L", (WIDTH, HEIGHT), 0)
    ImageDraw.Draw(well_mask).polygon(well, fill=255)

    # --- LAYER 3: Robin's-egg-blue diagonal band (lower-left -> upper-right) ---
    # Top edge of band passes through the badge's top-right inner corner.
    # Bottom edge of band passes through the left-side chevron transition point.
    # Both edges share the original band slope.
    band_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    end_offset = 110  # preserves the original band angle
    span_x = (right - well_inset + 6) - (left + well_inset - 6)
    slope = (-2 * end_offset) / span_x

    # Anchor points the band edges must hit
    tr_anchor = (right - well_inset, top + well_inset)        # top edge target
    bl_anchor = (left + well_inset, bottom - foot)             # bottom edge target

    # Compute y on each edge at the well's left/right x-bounds
    x_left = left + well_inset - 6
    x_right = right - well_inset + 6

    top_y_at_left = tr_anchor[1] + slope * (x_left - tr_anchor[0])
    top_y_at_right = tr_anchor[1] + slope * (x_right - tr_anchor[0])
    bot_y_at_left = bl_anchor[1] + slope * (x_left - bl_anchor[0])
    bot_y_at_right = bl_anchor[1] + slope * (x_right - bl_anchor[0])

    band_pts = [
        (int(x_left), int(top_y_at_left)),
        (int(x_right), int(top_y_at_right)),
        (int(x_right), int(bot_y_at_right)),
        (int(x_left), int(bot_y_at_left)),
    ]
    _shade_polygon(
        band_layer, band_pts, ENAMEL_BLUE, ENAMEL_BLUE_HI, axis="vertical"
    )
    # Clip the band to the well so its edges become straight where they meet the chrome
    band_clipped = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    band_clipped.paste(band_layer, (0, 0), well_mask)
    enamel_layer.alpha_composite(band_clipped)

    # Thin chrome "fences" along both edges of the diagonal stripe (embossed feel)
    fence_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fence_layer)
    fd.line(
        [band_pts[0], band_pts[1]], fill=CHROME_LIGHT + (255,), width=3
    )
    fd.line(
        [band_pts[3], band_pts[2]], fill=CHROME_DARK + (255,), width=3
    )
    fence_clipped = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    fence_clipped.paste(fence_layer, (0, 0), well_mask)
    enamel_layer.alpha_composite(fence_clipped)

    img.paste(enamel_layer, (0, 0), enamel_layer)

    # --- LAYER 4: Gold '40' numerals tucked into corners ---
    # Render "40" in a tall narrow aspect ratio: draw at a moderate point size,
    # then squeeze horizontally so the digits look like an art-deco coachbuilt
    # plate — thin strokes, very tall.
    base_pt = 160
    font_40 = _load_font(base_pt, "serif")

    def _render_tall_numeral(text: str, color, shadow, highlight) -> Image.Image:
        # Render once at full width to measure
        probe = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
        l, t, r, b = ImageDraw.Draw(probe).textbbox((0, 0), text, font=font_40)
        tw = max(1, r - l)
        th = max(1, b - t)
        pad = 16
        canvas = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
        cdraw = ImageDraw.Draw(canvas)
        ox, oy = pad - l, pad - t
        # Drop shadow
        cdraw.text((ox + 2, oy + 2), text, font=font_40, fill=shadow)
        # Highlight
        cdraw.text((ox - 1, oy - 1), text, font=font_40, fill=highlight)
        # Main face
        cdraw.text((ox, oy), text, font=font_40, fill=color)
        # Now squeeze: width × 0.38 keeps the height, shrinks the strokes.
        squeeze = 0.38
        new_size = (max(1, int(canvas.width * squeeze)), canvas.height)
        return canvas.resize(new_size, resample=Image.LANCZOS)

    numeral = _render_tall_numeral("40", GOLD, GOLD_SHADOW, GOLD_HI)

    # Top numeral: pinned to top-left corner of the red field.
    # Bottom numeral: tucked into bottom-right of the red field, just above
    # the chevron tip and nudged slightly inward so it stays in red.
    top_xy = (
        left + well_inset + 8,
        top + well_inset + 4,
    )
    bot_xy = (
        right - well_inset - 8 - numeral.width + 6,
        bottom - foot - numeral.height - 18,
    )
    img.paste(numeral, top_xy, numeral)
    img.paste(numeral, bot_xy, numeral)

    # --- LAYER 5: Gold 'Austin' cursive on the blue band ---
    # Render at full size, then horizontally squeeze (like the '40' numerals)
    # so the script keeps its tall height but fits across the narrow badge.
    badge_inner_w = (right - well_inset) - (left + well_inset)

    def _render_austin(font: ImageFont.FreeTypeFont) -> Image.Image:
        probe = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
        l, t, r, b = ImageDraw.Draw(probe).textbbox((0, 0), "Austin", font=font)
        tw = max(1, r - l)
        th = max(1, b - t)
        pad = 24
        canvas = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
        cdraw = ImageDraw.Draw(canvas)
        ox, oy = pad - l, pad - t
        cdraw.text((ox + 4, oy + 4), "Austin", font=font, fill=GOLD_SHADOW + (180,))
        cdraw.text((ox - 1, oy - 1), "Austin", font=font, fill=GOLD_HI + (255,))
        cdraw.text((ox, oy), "Austin", font=font, fill=GOLD + (255,))
        return canvas

    austin_pt = 150
    austin_canvas = _render_austin(_load_font(austin_pt, "cursive"))

    # Squeeze horizontally only. Lower factor = skinnier letters at same height.
    target_w = int(badge_inner_w * 1.25)
    if austin_canvas.width > target_w:
        new_size = (target_w, austin_canvas.height)
        austin_canvas = austin_canvas.resize(new_size, resample=Image.LANCZOS)
    txt_canvas = austin_canvas

    # The diagonal angle: rise/run from band_pts[0] -> band_pts[1]
    import math
    dx = band_pts[1][0] - band_pts[0][0]
    dy = band_pts[1][1] - band_pts[0][1]
    angle_deg = math.degrees(math.atan2(-dy, dx))  # PIL rotates CCW for positive angle
    # Script tilts slightly less aggressively than the band itself
    text_angle = angle_deg * 0.7
    rotated_txt = txt_canvas.rotate(text_angle, expand=True, resample=Image.BICUBIC)
    # Horizontally centered between the badge edges (nudged slightly left);
    # vertically centered on the blue band's centroid.
    band_cy = sum(p[1] for p in band_pts) // 4
    austin_x_offset = -14
    img.paste(
        rotated_txt,
        (
            cx - rotated_txt.width // 2 + austin_x_offset,
            band_cy - rotated_txt.height // 2,
        ),
        rotated_txt,
    )

    # --- LAYER 6: Soft vignette toward the corners for OEM depth ---
    vignette = Image.new("L", (WIDTH, HEIGHT), 255)
    v_draw = ImageDraw.Draw(vignette)
    v_draw.ellipse([-200, -200, WIDTH + 200, HEIGHT + 200], fill=0)
    vignette = vignette.filter(ImageFilter.GaussianBlur(180))
    img.paste((0, 0, 0), (0, 0), mask=vignette)

    return img

def main():
    here = os.path.dirname(__file__)
    repo_root = os.path.abspath(os.path.join(here, os.pardir))

    default_pi_out = os.path.join(
        here, "output", "a40-dash", "a40-boot-splash-portrait.png"
    )
    default_blog_out = os.path.join(
        repo_root,
        "public",
        "assets",
        "projects",
        "a40-austin",
        "blog",
        "a40-boot-splash-landscape.png",
    )

    parser = argparse.ArgumentParser(
        description=(
            "Render the A40 boot splash. By default writes two files: "
            "a portrait-rotated PNG for the Pi (Plymouth) and a landscape "
            "PNG for the blog frontend."
        )
    )
    parser.add_argument(
        "--rotate",
        type=int,
        default=90,
        choices=[0, 90, 180, 270],
        help="Rotation applied to the Pi/Plymouth output (default: 90).",
    )
    parser.add_argument(
        "--out",
        default=default_pi_out,
        help="Output path for the Pi/Plymouth (rotated) splash.",
    )
    parser.add_argument(
        "--blog-out",
        default=default_blog_out,
        help="Output path for the landscape blog splash. Use '' to skip.",
    )
    args = parser.parse_args()

    base = render_splash()

    # Pi / Plymouth output (pre-rotated to match the panel's portrait native).
    pi_img = base.rotate(args.rotate, expand=True) if args.rotate else base
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    pi_img.save(args.out, "PNG", optimize=True)
    print(f"Pi splash:    {os.path.abspath(args.out)}  ({pi_img.size[0]}x{pi_img.size[1]})")

    # Blog / frontend output (always landscape, never rotated).
    if args.blog_out:
        os.makedirs(os.path.dirname(os.path.abspath(args.blog_out)), exist_ok=True)
        base.save(args.blog_out, "PNG", optimize=True)
        print(f"Blog splash:  {os.path.abspath(args.blog_out)}  ({base.size[0]}x{base.size[1]})")

if __name__ == "__main__":
    main()