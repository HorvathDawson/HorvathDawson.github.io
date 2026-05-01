"""Generate the Austin A40 restomod digital-twin dash asset kit.

Outputs (all PNG, transparent backgrounds where applicable, written to
``public/assets/projects/a40-austin/blog/gauges/``):

  Center (Slot 3, rounded square — slightly narrower than tall):
    - center_tach.png       SR20 0-9000 RPM tach with recessed digital MPH
                            and gear-indicator cutouts (vintage rolling-
                            counter aesthetic).

  Side pills (Slots 1, 2, 4, 5 — vertical stadiums):
    - pill_oil_pressure.png Oil Pressure 0-100 PSI + digital battery volts.
    - pill_coolant_temp.png Coolant temp 100-260 F + digital oil temp.
    - pill_boost.png        Boost -30 inHg to +20 PSI + digital AFR.
    - pill_fuel.png         Fuel level E..F + digital odometer.

  Needles:
    - needle_long.png       Long tapered black needle for the center tach.
    - needle_short.png      Shorter needle for the side pill gauges.

  Preview:
    - dashboard_preview.png All five gauges laid out left-to-right against
                            a wood-grain bezel placeholder, for sanity
                            checking proportions before importing into
                            Godot.

All gauges share a "vintage parchment" aesthetic (warm cream face, soft
charcoal ink, faded chrome bezel rings, classic Futura-style numerals).
"""

from __future__ import annotations

import math
import os
from typing import Callable, Sequence
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Output configuration
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))
OUT_DIR = os.path.join(
    REPO_ROOT, "public", "assets", "projects", "a40-austin", "blog", "gauges"
)
SSAA = 2  # super-sampling factor for anti-aliasing

# ---------------------------------------------------------------------------
# Shared aesthetic (the Restomod Style Guide)
# ---------------------------------------------------------------------------

PARCHMENT = (242, 239, 233, 255)        # #F2EFE9
PARCHMENT_EDGE = (224, 218, 200, 255)
INK = (45, 40, 35, 255)                  # warm charcoal, not pure black
INK_SOFT = (90, 82, 72, 255)
INK_FAINT = (140, 128, 110, 255)
CHROME_OUTER = (70, 65, 58, 255)
CHROME_MID = (185, 180, 168, 255)
CHROME_INNER = (45, 40, 36, 255)
REDLINE = (172, 30, 28, 255)
WARN_AMBER = (200, 130, 30, 255)
COOL_BLUE = (60, 90, 140, 255)
DIGITAL_BG = (28, 24, 20, 255)           # recessed window background
DIGITAL_INK = (235, 220, 190, 255)       # warm "tritium" amber-cream
SHADOW = (0, 0, 0, 90)


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def polar(cx: float, cy: float, r: float, angle_deg: float) -> tuple[float, float]:
    """Math-convention polar -> screen pixel (PIL y-down)."""
    a = math.radians(angle_deg)
    return cx + r * math.cos(a), cy - r * math.sin(a)


def fill_rounded_rect(d: ImageDraw.ImageDraw, cx: float, cy: float,
                      w: float, h: float, r: float, fill) -> None:
    r = max(0.0, min(r, min(w, h) / 2))
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2),
                        radius=r, fill=fill)


def stadium_inner_radius(theta_deg: float, w: float, h: float,
                         margin: float = 0.0, *, vertical: bool = False) -> float:
    """Distance from center to inner edge of a stadium along ray theta.

    Horizontal stadium: rounded ends on left/right (radius = h/2).
    Vertical stadium:   rounded ends on top/bottom (radius = w/2).
    """
    if vertical:
        # Swap roles: a vertical stadium of (w, h) is a horizontal one of
        # (h, w) seen with x and y swapped, i.e. theta -> 90 - theta.
        return stadium_inner_radius(90 - theta_deg, h, w, margin)

    half_h = h / 2
    half_w = w / 2
    flat_half = max(0.0, half_w - half_h)

    a = math.radians(theta_deg)
    dx = math.cos(a)
    dy = -math.sin(a)

    candidates: list[float] = []
    if dy != 0:
        for y_edge in (-half_h, half_h):
            t = y_edge / dy
            if t > 0:
                x = t * dx
                if -flat_half <= x <= flat_half:
                    candidates.append(t)
    for sign in (-1, 1):
        cx0 = sign * flat_half
        B = -2 * dx * cx0
        C = cx0 * cx0 - half_h * half_h
        disc = B * B - 4 * C  # A = 1
        if disc < 0:
            continue
        sq = math.sqrt(disc)
        for t in ((-B + sq) / 2, (-B - sq) / 2):
            if t > 0:
                x = t * dx
                if (sign > 0 and x >= flat_half - 1e-6) or \
                   (sign < 0 and x <= -flat_half + 1e-6):
                    candidates.append(t)
    if not candidates:
        return half_h - margin
    return min(candidates) - margin


def rounded_square_inner_radius(theta_deg: float, w: float, h: float,
                                corner_r: float, margin: float = 0.0) -> float:
    """Distance to the inner edge of a rounded rectangle along ray theta.

    Solves intersection with the 4 straight edges and 4 corner quarter-
    circles, returns the smallest positive distance.
    """
    half_w = w / 2
    half_h = h / 2
    a = math.radians(theta_deg)
    dx = math.cos(a)
    dy = -math.sin(a)

    candidates: list[float] = []
    flat_x_half = half_w - corner_r
    flat_y_half = half_h - corner_r

    # Top / bottom flat edges (y = ±half_h, |x| <= flat_x_half).
    if dy != 0:
        for y_edge in (-half_h, half_h):
            t = y_edge / dy
            if t > 0:
                x = t * dx
                if -flat_x_half <= x <= flat_x_half:
                    candidates.append(t)
    # Left / right flat edges (x = ±half_w, |y| <= flat_y_half).
    if dx != 0:
        for x_edge in (-half_w, half_w):
            t = x_edge / dx
            if t > 0:
                y = t * dy
                if -flat_y_half <= y <= flat_y_half:
                    candidates.append(t)
    # Four corner quarter-circles.
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx0 = sx * flat_x_half
            cy0 = sy * flat_y_half
            B = -2 * (dx * cx0 + dy * cy0)
            C = cx0 * cx0 + cy0 * cy0 - corner_r * corner_r
            disc = B * B - 4 * C
            if disc < 0:
                continue
            sq = math.sqrt(disc)
            for t in ((-B + sq) / 2, (-B - sq) / 2):
                if t > 0:
                    x = t * dx
                    y = t * dy
                    # Must be in the corner quadrant.
                    if ((sx > 0 and x >= flat_x_half - 1e-6) or
                            (sx < 0 and x <= -flat_x_half + 1e-6)) and \
                       ((sy > 0 and y >= flat_y_half - 1e-6) or
                            (sy < 0 and y <= -flat_y_half + 1e-6)):
                        candidates.append(t)

    if not candidates:
        return min(half_w, half_h) - margin
    return min(candidates) - margin


# ---------------------------------------------------------------------------
# "Barrel" shape: rectangle whose left/right edges are arcs of a large-radius
# circle (slightly bulging outward). Top/bottom edges remain straight. Used
# for both the center tach and the side pills (rotated 90° conceptually:
# wide & short for center, narrow & tall for pills).
# ---------------------------------------------------------------------------

def _barrel_arc_geometry(h: float, bulge: float) -> tuple[float, float]:
    """Return (R, cx_offset) for one side arc of a barrel.

    The arc has chord = h (vertical for L/R bulges) and sagitta = bulge.
    R = bulge/2 + h^2 / (8 * bulge).  cx_offset is how far the arc's center
    sits horizontally INSIDE the bounding rectangle's edge (x = ±w/2).
    """
    if bulge <= 0:
        return float("inf"), 0.0
    R = bulge / 2.0 + (h * h) / (8.0 * bulge)
    # Arc center for the right edge sits at x = w/2 + bulge - R (negative
    # if R > bulge, which is the usual case). cx_offset = R - bulge.
    return R, R - bulge


def fill_barrel(d: ImageDraw.ImageDraw, cx: float, cy: float,
                w: float, h: float, bulge: float, fill,
                samples_per_arc: int = 60) -> None:
    """Fill a barrel shape (rectangle + L/R outward arcs)."""
    if bulge <= 0:
        d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), fill=fill)
        return
    R, off = _barrel_arc_geometry(h, bulge)
    pts: list[tuple[float, float]] = []
    # Top edge (left -> right)
    pts.append((cx - w / 2, cy - h / 2))
    pts.append((cx + w / 2, cy - h / 2))
    # Right arc: sweep from top corner outward to (cx + w/2 + bulge, cy)
    # then back to bottom corner. Arc center at (cx + w/2 - off, cy).
    arc_cx = cx + w / 2 - off
    # Angle from arc center to top corner: corner at (cx + w/2, cy - h/2)
    # vector = (off, -h/2). atan2(-(-h/2), off) — but we work in math angles.
    a_top = math.atan2(-(- h / 2), w / 2 - (w / 2 - off))  # = atan2(h/2, off)
    # We sweep CCW around arc center from -a_top to +a_top through 0 (which
    # is the rightmost point of the arc). a_top is the angle ABOVE x-axis;
    # top corner is BELOW center? No — y = cy - h/2 means above (PIL y-down).
    a_top = math.atan2(h / 2, off)
    for i in range(1, samples_per_arc):
        # Go from top corner (-a_top) through 0 to bottom corner (+a_top)
        t = -a_top + (i / samples_per_arc) * (2 * a_top)
        pts.append((arc_cx + R * math.cos(t), cy + R * math.sin(t)))
    # Bottom edge (right -> left)
    pts.append((cx + w / 2, cy + h / 2))
    pts.append((cx - w / 2, cy + h / 2))
    # Left arc: sweep from bottom-left corner through leftmost point to
    # top-left corner. Arc center at (cx - w/2 + off, cy).
    arc_cx = cx - w / 2 + off
    for i in range(1, samples_per_arc):
        t = math.pi - a_top + (i / samples_per_arc) * (2 * a_top)
        # We want to start at bottom-left corner and sweep to top-left,
        # i.e. from angle = pi - a_top (bottom-left, y +h/2) to pi + a_top
        # (top-left, y -h/2). atan2(sin, cos) -> sin negative is up.
        # Actually corner positions:
        #   bottom-left = (cx - w/2, cy + h/2). vec from arc center:
        #     (-off, h/2). angle = atan2(h/2, -off) = pi - a_top.
        #   top-left    = (cx - w/2, cy - h/2). vec = (-off, -h/2).
        #     angle = atan2(-h/2, -off) = -(pi - a_top) = a_top - pi
        #             == pi + a_top (mod 2*pi).
        # So we sweep from (pi - a_top) to (pi + a_top), going through pi.
        pts.append((arc_cx + R * math.cos(t), cy + R * math.sin(t)))
    d.polygon(pts, fill=fill)


def barrel_inner_radius(theta_deg: float, w: float, h: float,
                        bulge: float, margin: float = 0.0) -> float:
    """Distance from center along ray theta to inner edge of a barrel."""
    if bulge <= 0:
        # Plain rectangle.
        return rect_inner_radius(theta_deg, w, h) - margin
    R, off = _barrel_arc_geometry(h, bulge)
    half_w = w / 2
    half_h = h / 2

    a = math.radians(theta_deg)
    dx = math.cos(a)
    dy = -math.sin(a)

    candidates: list[float] = []
    # Top/bottom horizontal edges (y = ±half_h, |x| <= half_w)
    if dy != 0:
        for y_edge in (-half_h, half_h):
            t = y_edge / dy
            if t > 0:
                x = t * dx
                if -half_w <= x <= half_w:
                    candidates.append(t)
    # Left/right arcs centered at (±(half_w - off), 0) with radius R.
    for sign in (-1, 1):
        cx0 = sign * (half_w - off)
        B = -2 * dx * cx0
        C = cx0 * cx0 - R * R
        disc = B * B - 4 * C
        if disc < 0:
            continue
        sq = math.sqrt(disc)
        for t in ((-B + sq) / 2, (-B - sq) / 2):
            if t > 0:
                x = t * dx
                # Must be on the bulge side (|x| > half_w roughly, allowing
                # tiny tolerance for the corners).
                if (sign > 0 and x >= half_w - 1e-3) or \
                   (sign < 0 and x <= -half_w + 1e-3):
                    candidates.append(t)
    if not candidates:
        return min(half_w + bulge, half_h) - margin
    return min(candidates) - margin


def rect_inner_radius(theta_deg: float, w: float, h: float,
                      margin: float = 0.0) -> float:
    a = math.radians(theta_deg)
    dx = math.cos(a)
    dy = -math.sin(a)
    candidates = []
    if dy != 0:
        for y_edge in (-h / 2, h / 2):
            t = y_edge / dy
            if t > 0 and abs(t * dx) <= w / 2:
                candidates.append(t)
    if dx != 0:
        for x_edge in (-w / 2, w / 2):
            t = x_edge / dx
            if t > 0 and abs(t * dy) <= h / 2:
                candidates.append(t)
    return (min(candidates) if candidates else min(w, h) / 2) - margin


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def load_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        # Closest to Gill Sans / Futura on macOS.
        "/System/Library/Fonts/Supplemental/Futura.ttc",
        "/System/Library/Fonts/Supplemental/GillSans.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def load_mono_font(size: int) -> ImageFont.FreeTypeFont:
    """For digital readouts -- use a slightly mechanical-looking mono."""
    candidates = [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Courier.ttc",
        "/System/Library/Fonts/Monaco.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return load_font(size)


def text_size(draw: ImageDraw.ImageDraw, text: str, font) -> tuple[float, float]:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_text_centered(d: ImageDraw.ImageDraw, xy, text, font, fill) -> None:
    bbox = d.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    d.text((xy[0] - w / 2 - bbox[0], xy[1] - h / 2 - bbox[1]),
           text, font=font, fill=fill)


def thick_line(d: ImageDraw.ImageDraw, p1, p2, width: int, fill) -> None:
    d.line((p1[0], p1[1], p2[0], p2[1]), fill=fill, width=int(width))
    r = width / 2
    d.ellipse((p1[0] - r, p1[1] - r, p1[0] + r, p1[1] + r), fill=fill)
    d.ellipse((p2[0] - r, p2[1] - r, p2[0] + r, p2[1] + r), fill=fill)


def draw_recessed_window(d: ImageDraw.ImageDraw, cx, cy, w, h, *,
                         radius: float | None = None) -> None:
    """Inner-shadow rounded box that reads as a cutout in the parchment."""
    if radius is None:
        radius = h * 0.18
    # Outer dark frame
    fill_rounded_rect(d, cx, cy, w + h * 0.08, h + h * 0.08,
                      radius + h * 0.04, (20, 18, 16, 200))
    # Inset highlight (very faint, mimics machined edge)
    fill_rounded_rect(d, cx, cy, w + h * 0.04, h + h * 0.04,
                      radius + h * 0.02, (60, 55, 48, 255))
    # Recessed surface
    fill_rounded_rect(d, cx, cy, w, h, radius, DIGITAL_BG)


# ---------------------------------------------------------------------------
# Center tach (rounded square, slightly narrower than tall)
# ---------------------------------------------------------------------------

CENTER_W = 1200
CENTER_H = 1320  # slightly taller than wide
CENTER_BULGE = 32  # left/right edge bulge in px (large radius, subtle)
CENTER_RPM_MIN = 0
CENTER_RPM_MAX = 9000
CENTER_RPM_REDLINE = 7500
CENTER_SWEEP_START = 225.0  # 0 RPM at lower-left
CENTER_SWEEP_TOTAL = 270.0  # CW through top to lower-right


def render_center_tach() -> Image.Image:
    W, H = CENTER_W * SSAA, CENTER_H * SSAA
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = W / 2, H / 2

    # Bezel rings: barrel shape (rectangle with slightly curved L/R edges)
    bands = [
        (1.000, 1.000, CHROME_OUTER),
        (0.980, 0.980, CHROME_MID),
        (0.958, 0.958, CHROME_INNER),
        (0.940, 0.940, PARCHMENT_EDGE),
        (0.926, 0.926, PARCHMENT),
    ]
    base_bulge = CENTER_BULGE * SSAA
    for sw, sh, color in bands:
        ww = W * sw
        hh = H * sh
        bulge = base_bulge * sw  # scale slightly per ring
        fill_barrel(d, cx, cy, ww, hh, bulge, color)

    face_w = W * 0.926
    face_h = H * 0.926
    face_bulge = base_bulge * 0.926

    def value_to_angle(rpm: float) -> float:
        t = (rpm - CENTER_RPM_MIN) / (CENTER_RPM_MAX - CENTER_RPM_MIN)
        return CENTER_SWEEP_START - t * CENTER_SWEEP_TOTAL

    outer_margin = H * 0.020
    minor_len = H * 0.030
    mid_len = H * 0.058
    major_len = H * 0.092
    minor_w = max(2, int(H * 0.0028))
    mid_w = max(3, int(H * 0.0050))
    major_w = max(5, int(H * 0.0085))

    def tick_pts(rpm: float, length: float):
        a = value_to_angle(rpm)
        outer_r = barrel_inner_radius(
            a, face_w, face_h, face_bulge, margin=outer_margin)
        return polar(cx, cy, outer_r, a), polar(cx, cy, outer_r - length, a)

    # Redline band: dense thick red ticks tracing the outer edge.
    for i in range(81):
        rpm = CENTER_RPM_REDLINE + (i / 80) * (CENTER_RPM_MAX - CENTER_RPM_REDLINE)
        a = value_to_angle(rpm)
        outer_r = barrel_inner_radius(
            a, face_w, face_h, face_bulge, margin=H * 0.012)
        inner_r = outer_r - H * 0.038
        thick_line(d, polar(cx, cy, outer_r, a), polar(cx, cy, inner_r, a),
                   max(6, int(H * 0.012)), REDLINE)

    # Minor ticks every 100, mid every 500, major every 1000.
    for rpm in range(CENTER_RPM_MIN, CENTER_RPM_MAX + 1, 100):
        if rpm % 500 == 0:
            continue
        p1, p2 = tick_pts(rpm, minor_len)
        thick_line(d, p1, p2, minor_w, INK_SOFT)
    for rpm in range(CENTER_RPM_MIN, CENTER_RPM_MAX + 1, 500):
        if rpm % 1000 == 0:
            continue
        col = REDLINE if rpm >= CENTER_RPM_REDLINE else INK
        p1, p2 = tick_pts(rpm, mid_len)
        thick_line(d, p1, p2, mid_w, col)
    for rpm in range(CENTER_RPM_MIN, CENTER_RPM_MAX + 1, 1000):
        col = REDLINE if rpm >= CENTER_RPM_REDLINE else INK
        p1, p2 = tick_pts(rpm, major_len)
        thick_line(d, p1, p2, major_w, col)

    # Numerals 0..9 (slightly smaller so they don't crowd the ticks)
    num_font = load_font(int(H * 0.072))
    num_inset = major_len + H * 0.048
    for rpm in range(CENTER_RPM_MIN, CENTER_RPM_MAX + 1, 1000):
        a = value_to_angle(rpm)
        outer_r = barrel_inner_radius(
            a, face_w, face_h, face_bulge, margin=outer_margin)
        x, y = polar(cx, cy, outer_r - num_inset, a)
        col = REDLINE if rpm >= CENTER_RPM_REDLINE else INK
        draw_text_centered(d, (x, y), str(rpm // 1000), num_font, col)

    # Brand legend - above the hub but below the 4/5 numerals at the top
    # of the sweep, so nothing overlaps the ticks or numerals.
    brand_font = load_font(int(H * 0.034))
    legend_font = load_font(int(H * 0.024))
    draw_text_centered(d, (cx, cy - H * 0.190),
                       "TACHOMETER", brand_font, INK)
    draw_text_centered(d, (cx, cy - H * 0.150),
                       "x 1000  RPM", legend_font, INK_SOFT)

    # Recessed digital cutouts: top = MPH, bottom = gear.
    # Top MPH window (wider)
    mph_w, mph_h = W * 0.40, H * 0.100
    mph_cx, mph_cy = cx, cy + H * 0.150
    draw_recessed_window(d, mph_cx, mph_cy, mph_w, mph_h)
    mph_font = load_mono_font(int(mph_h * 0.60))
    draw_text_centered(d, (mph_cx, mph_cy - mph_h * 0.05),
                       "065", mph_font, DIGITAL_INK)
    mph_label_font = load_font(int(H * 0.022))
    draw_text_centered(d, (mph_cx, mph_cy + mph_h * 0.40),
                       "MPH", mph_label_font, DIGITAL_INK)

    # Bottom gear window (smaller square)
    gear_w, gear_h = H * 0.110, H * 0.110
    gear_cx, gear_cy = cx, cy + H * 0.295
    draw_recessed_window(d, gear_cx, gear_cy, gear_w, gear_h,
                         radius=gear_h * 0.18)
    gear_font = load_font(int(gear_h * 0.70))
    draw_text_centered(d, (gear_cx, gear_cy - gear_h * 0.05),
                       "3", gear_font, DIGITAL_INK)
    draw_text_centered(d, (gear_cx, gear_cy + gear_h * 0.42),
                       "GEAR", mph_label_font, DIGITAL_INK)

    # Center hub cap (needle pivots here)
    hub_r = H * 0.040
    d.ellipse((cx - hub_r, cy - hub_r, cx + hub_r, cy + hub_r),
              fill=(30, 26, 22, 255))
    d.ellipse((cx - hub_r * 0.55, cy - hub_r * 0.55,
               cx + hub_r * 0.55, cy + hub_r * 0.55),
              fill=(85, 78, 66, 255))

    return img.resize((CENTER_W, CENTER_H), Image.LANCZOS)


# ---------------------------------------------------------------------------
# Vertical pill side gauge (parameterised)
# ---------------------------------------------------------------------------

# Pill outer dimensions. The pills are intentionally SHORTER than the
# center tach so they read as secondary instruments.
PILL_W = 520
PILL_H = 900

# Pivot is offset toward one edge; the dial (ticks + numerals + sweep)
# lives on the opposite side. Numbers therefore appear on either the left
# or right side of the gauge.
PILL_PIVOT_INSET_FRAC = 0.18      # pivot inset from the chosen edge
PILL_SWEEP_HALF_DEG = 48.0        # sweep is ±this from horizontal
PILL_BULGE = 22                   # left/right edge bulge in px (subtle)


def render_pill_gauge(*,
                      title: str,
                      sub_title: str,
                      value_min: float,
                      value_max: float,
                      major_step: float,
                      mid_step: float | None,
                      minor_step: float | None,
                      label_formatter: Callable[[float], str],
                      warn_start: float | None = None,
                      warn_end: float | None = None,
                      warn_color=REDLINE,
                      cool_start: float | None = None,
                      cool_end: float | None = None,
                      digital_label: str = "",
                      digital_value: str = "",
                      side: str = "right",
                      ) -> Image.Image:
    """Render a side pill gauge.

    The needle pivots from one inner edge ("inset" from `side`'s OPPOSITE
    edge — i.e. with ``side="right"`` the pivot sits near the LEFT edge so
    the dial fills the right half). The needle sweeps along the dial side
    only, going from value_min at the bottom of that side to value_max at
    the top. Title sits in the top end-cap, digital readout in the bottom
    end-cap.
    """
    W, H = PILL_W * SSAA, PILL_H * SSAA
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx_geom, cy_geom = W / 2, H / 2

    # Bezel rings: barrel shape (rectangle with subtle L/R bulged edges,
    # straight top/bottom). Top/bottom flat ends house the title and
    # digital readout cleanly.
    rings = [
        (1.000, CHROME_OUTER),
        (0.972, CHROME_MID),
        (0.946, CHROME_INNER),
        (0.928, PARCHMENT_EDGE),
        (0.912, PARCHMENT),
    ]
    base_bulge = PILL_BULGE * SSAA
    for s, color in rings:
        ww = W * s
        hh = H * s
        fill_barrel(d, cx_geom, cy_geom, ww, hh, base_bulge * s, color)

    # Pivot location and sweep range.
    pivot_inset_px = W * PILL_PIVOT_INSET_FRAC
    pivot_y = H * 0.50
    if side == "right":
        pivot_x = pivot_inset_px
        # value_min at bottom-right (-half), value_max at top-right (+half)
        sweep_start = -PILL_SWEEP_HALF_DEG
        sweep_end = +PILL_SWEEP_HALF_DEG
    else:  # "left"
        pivot_x = W - pivot_inset_px
        # value_min at bottom-left (180 + half), value_max at top-left (180 - half)
        sweep_start = 180.0 + PILL_SWEEP_HALF_DEG
        sweep_end = 180.0 - PILL_SWEEP_HALF_DEG

    # Reach radius: largest safe radius from pivot that stays inside the
    # face on the dial side. Constant radius -> ticks/numerals form a clean
    # circular arc, regardless of the pill's curved end caps.
    face_margin = W * 0.060
    if side == "right":
        reach = min(H / 2 - face_margin, W - pivot_x - face_margin)
    else:
        reach = min(H / 2 - face_margin, pivot_x - face_margin)

    outer_r = reach
    minor_len = W * 0.060
    mid_len = W * 0.110
    major_len = W * 0.170
    minor_w = max(2, int(W * 0.010))
    mid_w = max(3, int(W * 0.018))
    major_w = max(5, int(W * 0.030))

    def value_to_angle(v: float) -> float:
        t = (v - value_min) / (value_max - value_min)
        return sweep_start + t * (sweep_end - sweep_start)

    def tick_pts(v: float, length: float):
        a = value_to_angle(v)
        return polar(pivot_x, pivot_y, outer_r, a), \
               polar(pivot_x, pivot_y, outer_r - length, a)

    # Coloured arc bands (warn / cool) — dense thick ticks on the outer rim.
    for zone_start, zone_end, zone_color in (
        (warn_start, warn_end, warn_color),
        (cool_start, cool_end, COOL_BLUE),
    ):
        if zone_start is None or zone_end is None:
            continue
        steps = 60
        band_outer = outer_r + W * 0.012
        band_inner = outer_r - W * 0.040
        for i in range(steps + 1):
            v = zone_start + (i / steps) * (zone_end - zone_start)
            a = value_to_angle(v)
            thick_line(d, polar(pivot_x, pivot_y, band_outer, a),
                       polar(pivot_x, pivot_y, band_inner, a),
                       max(6, int(W * 0.020)), zone_color)

    def frange(lo: float, hi: float, step: float):
        n = int(round((hi - lo) / step))
        for i in range(n + 1):
            yield lo + i * step

    if minor_step:
        for v in frange(value_min, value_max, minor_step):
            if mid_step and abs((v - value_min) % mid_step) < 1e-6:
                continue
            if abs((v - value_min) % major_step) < 1e-6:
                continue
            p1, p2 = tick_pts(v, minor_len)
            thick_line(d, p1, p2, minor_w, INK_SOFT)
    if mid_step:
        for v in frange(value_min, value_max, mid_step):
            if abs((v - value_min) % major_step) < 1e-6:
                continue
            in_warn = (warn_start is not None and warn_end is not None
                       and warn_start <= v <= warn_end)
            col = warn_color if in_warn else INK
            p1, p2 = tick_pts(v, mid_len)
            thick_line(d, p1, p2, mid_w, col)
    for v in frange(value_min, value_max, major_step):
        in_warn = (warn_start is not None and warn_end is not None
                   and warn_start <= v <= warn_end)
        col = warn_color if in_warn else INK
        p1, p2 = tick_pts(v, major_len)
        thick_line(d, p1, p2, major_w, col)

    # Numerals — on the dial side, just inside the major ticks.
    num_font = load_font(int(W * 0.082))
    num_inset = major_len + W * 0.060
    for v in frange(value_min, value_max, major_step):
        a = value_to_angle(v)
        x, y = polar(pivot_x, pivot_y, outer_r - num_inset, a)
        in_warn = (warn_start is not None and warn_end is not None
                   and warn_start <= v <= warn_end)
        col = warn_color if in_warn else INK
        draw_text_centered(d, (x, y), label_formatter(v), num_font, col)

    # Title in the TOP end-cap (centered, kept small so it never collides
    # with the upper sweep tip).
    title_font = load_font(int(W * 0.080))
    draw_text_centered(d, (cx_geom, H * 0.058), title, title_font, INK)
    if sub_title:
        sub_font = load_font(int(W * 0.045))
        draw_text_centered(d, (cx_geom, H * 0.092),
                           sub_title, sub_font, INK_SOFT)

    # Recessed digital readout in the BOTTOM end-cap.
    if digital_value:
        win_w = W * 0.56
        win_h = H * 0.072
        win_cx = cx_geom
        win_cy = H * 0.945 - win_h * 0.55
        draw_recessed_window(d, win_cx, win_cy, win_w, win_h,
                             radius=win_h * 0.22)
        val_font = load_mono_font(int(win_h * 0.55))
        draw_text_centered(d, (win_cx, win_cy - win_h * 0.05),
                           digital_value, val_font, DIGITAL_INK)
        if digital_label:
            label_font = load_font(int(W * 0.050))
            draw_text_centered(d, (win_cx, win_cy + win_h * 0.62),
                               digital_label, label_font, DIGITAL_INK)

    # Pivot hub — small, semi-flush.
    hub_r = W * 0.050
    d.ellipse((pivot_x - hub_r, pivot_y - hub_r,
               pivot_x + hub_r, pivot_y + hub_r),
              fill=(30, 26, 22, 255))
    d.ellipse((pivot_x - hub_r * 0.55, pivot_y - hub_r * 0.55,
               pivot_x + hub_r * 0.55, pivot_y + hub_r * 0.55),
              fill=(85, 78, 66, 255))

    return img.resize((PILL_W, PILL_H), Image.LANCZOS)


# ---------------------------------------------------------------------------
# Needles
# ---------------------------------------------------------------------------

def render_needle(out_w: int, out_h: int) -> Image.Image:
    W, H = out_w * SSAA, out_h * SSAA
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = W / 2
    pivot_y = H * 0.78
    pointer_len = pivot_y * 0.96
    tail_len = (H - pivot_y) * 0.85
    base_half = W * 0.22
    tip_half = W * 0.05
    tail_half = W * 0.10
    pt_y = pivot_y - pointer_len
    tl_y = pivot_y + tail_len

    # Drop shadow
    so = max(2, int(W * 0.015))
    d.polygon([
        (cx - tip_half + so, pt_y + so),
        (cx + tip_half + so, pt_y + so),
        (cx + base_half + so, pivot_y + so),
        (cx + tail_half + so, tl_y + so),
        (cx - tail_half + so, tl_y + so),
        (cx - base_half + so, pivot_y + so),
    ], fill=(0, 0, 0, 70))
    # Body
    d.polygon([
        (cx - tip_half, pt_y),
        (cx + tip_half, pt_y),
        (cx + base_half, pivot_y),
        (cx + tail_half, tl_y),
        (cx - tail_half, tl_y),
        (cx - base_half, pivot_y),
    ], fill=(20, 18, 16, 255))
    # Highlight stripe
    hl_t = max(1, int(tip_half * 0.35))
    hl_b = max(2, int(base_half * 0.18))
    d.polygon([
        (cx - hl_t, pt_y + (pivot_y - pt_y) * 0.05),
        (cx + hl_t, pt_y + (pivot_y - pt_y) * 0.05),
        (cx + hl_b, pivot_y - (pivot_y - pt_y) * 0.02),
        (cx - hl_b, pivot_y - (pivot_y - pt_y) * 0.02),
    ], fill=(70, 64, 56, 220))
    # Hub
    hub_r = W * 0.32
    d.ellipse((cx - hub_r, pivot_y - hub_r, cx + hub_r, pivot_y + hub_r),
              fill=(35, 30, 26, 255))
    d.ellipse((cx - hub_r * 0.55, pivot_y - hub_r * 0.55,
               cx + hub_r * 0.55, pivot_y + hub_r * 0.55),
              fill=(110, 100, 88, 255))
    d.ellipse((cx - hub_r * 0.22, pivot_y - hub_r * 0.22,
               cx + hub_r * 0.22, pivot_y + hub_r * 0.22),
              fill=(20, 18, 16, 255))

    return img.resize((out_w, out_h), Image.LANCZOS)


# ---------------------------------------------------------------------------
# Composite preview
# ---------------------------------------------------------------------------

def render_preview(images: dict[str, Image.Image],
                   long_needle: Image.Image,
                   short_needle: Image.Image) -> Image.Image:
    """Lay out the 5 gauges horizontally on a wood-look background, with
    needles overlaid at representative values so the layout can be eyeballed.
    """
    pad = 60
    pill = images["oil"]
    center = images["center"]
    total_w = pad * 2 + pill.width * 4 + center.width + pad * 4
    total_h = pad * 2 + max(pill.height, center.height)
    bg = Image.new("RGBA", (total_w, total_h), (78, 52, 32, 255))
    grain = ImageDraw.Draw(bg)
    for i in range(0, total_w, 6):
        shade = 78 + (i % 17) - 8
        grain.line([(i, 0), (i, total_h)],
                   fill=(max(40, min(110, shade)),
                         max(20, min(80, shade - 30)),
                         max(10, min(60, shade - 45)), 255))

    # Per-gauge pivot (in the gauge image's own coordinates) and a chosen
    # display angle. Angles are math-convention (CCW+ from +x with PIL
    # y-down), which `paste_needle` converts to PIL rotation.
    center_pivot = (CENTER_W // 2, CENTER_H // 2)
    pill_right_pivot = (int(PILL_W * PILL_PIVOT_INSET_FRAC), PILL_H // 2)
    pill_left_pivot = (PILL_W - int(PILL_W * PILL_PIVOT_INSET_FRAC), PILL_H // 2)

    # Center: 4500 RPM (mid-sweep => pointing straight up, math angle 90).
    layout = [
        ("oil",     pill,   pill_right_pivot, short_needle,
            -PILL_SWEEP_HALF_DEG + 0.55 * 2 * PILL_SWEEP_HALF_DEG),  # ~55%
        ("coolant", pill,   pill_left_pivot,  short_needle,
            (180 + PILL_SWEEP_HALF_DEG) - 0.45 * 2 * PILL_SWEEP_HALF_DEG),
        ("center",  center, center_pivot,    long_needle,
            CENTER_SWEEP_START - 0.45 * CENTER_SWEEP_TOTAL),  # ~4000 RPM
        ("boost",   pill,   pill_right_pivot, short_needle,
            -PILL_SWEEP_HALF_DEG + 0.65 * 2 * PILL_SWEEP_HALF_DEG),
        ("fuel",    pill,   pill_left_pivot,  short_needle,
            (180 + PILL_SWEEP_HALF_DEG) - 0.62 * 2 * PILL_SWEEP_HALF_DEG),
    ]

    x = pad
    cy = total_h // 2
    for key, _, pivot, needle, math_angle in layout:
        im = images[key]
        ox = x
        oy = cy - im.height // 2
        bg.paste(im, (ox, oy), im)
        # Place needle. Default needle points UP (math angle 90). Rotation
        # to point at math_angle is (math_angle - 90), CCW positive in PIL.
        # PIL's `rotate(expand=True, center=...)` has a known bug where the
        # expanded bounding box assumes rotation about the image center, so
        # off-center rotations get clipped. Workaround: pad the needle so
        # its pivot lands at the geometric center, then rotate around that.
        nw, nh = needle.size
        pivot_xy = (nw / 2, nh * 0.78)
        # Square canvas big enough that any rotation stays inside.
        diag = int(math.ceil(2 * math.hypot(
            max(pivot_xy[0], nw - pivot_xy[0]),
            max(pivot_xy[1], nh - pivot_xy[1]),
        ))) + 4
        padded = Image.new("RGBA", (diag, diag), (0, 0, 0, 0))
        paste_x = int(round(diag / 2 - pivot_xy[0]))
        paste_y = int(round(diag / 2 - pivot_xy[1]))
        padded.paste(needle, (paste_x, paste_y), needle)
        rot_deg = math_angle - 90
        rotated = padded.rotate(rot_deg, resample=Image.BICUBIC)
        # Now the pivot is at the center of `rotated` (== diag/2, diag/2).
        gx = ox + pivot[0] - diag // 2
        gy = oy + pivot[1] - diag // 2
        bg.alpha_composite(rotated, (gx, gy))
        x += im.width + pad
    return bg


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def ensure_out_dir() -> str:
    os.makedirs(OUT_DIR, exist_ok=True)
    return OUT_DIR


def main() -> None:
    out_dir = ensure_out_dir()
    print("Generating Austin A40 restomod dash kit...")
    print(f"  Output dir : {out_dir}")

    saved: dict[str, Image.Image] = {}

    # --- Center tach ---
    center = render_center_tach()
    p = os.path.join(out_dir, "center_tach.png")
    center.save(p, optimize=True)
    saved["center"] = center
    print(f"  -> center_tach.png      ({center.width}x{center.height})")

    # --- Slot 1: Oil Pressure (warn high) + battery volts digital ---
    oil = render_pill_gauge(
        title="OIL",
        sub_title="PSI",
        value_min=0, value_max=100,
        major_step=20, mid_step=10, minor_step=5,
        label_formatter=lambda v: str(int(round(v))),
        warn_start=85, warn_end=100, warn_color=REDLINE,
        cool_start=0, cool_end=10,  # too-low pressure danger
        digital_label="BATTERY", digital_value="13.8 V",
        side="right",  # far-left slot: faces IN (dial on right half)
    )
    p = os.path.join(out_dir, "pill_oil_pressure.png")
    oil.save(p, optimize=True)
    saved["oil"] = oil
    print(f"  -> pill_oil_pressure.png ({oil.width}x{oil.height})")

    # --- Slot 2: Coolant Temp + oil temp digital ---
    coolant = render_pill_gauge(
        title="WATER",
        sub_title="°F",
        value_min=100, value_max=260,
        major_step=20, mid_step=10, minor_step=5,
        label_formatter=lambda v: str(int(round(v))),
        warn_start=230, warn_end=260, warn_color=REDLINE,
        cool_start=100, cool_end=140,
        digital_label="OIL TEMP", digital_value="210°F",
        side="left",  # inner-left slot: faces OUT (dial on left half)
    )
    p = os.path.join(out_dir, "pill_coolant_temp.png")
    coolant.save(p, optimize=True)
    saved["coolant"] = coolant
    print(f"  -> pill_coolant_temp.png ({coolant.width}x{coolant.height})")

    # --- Slot 4: Boost (-30 inHg .. +20 PSI) + AFR digital ---
    # Use a single linear scale -30..+20, with major step 10, label sign.
    boost = render_pill_gauge(
        title="BOOST",
        sub_title="inHg / PSI",
        value_min=-30, value_max=20,
        major_step=10, mid_step=5, minor_step=1,
        label_formatter=lambda v: f"{int(round(v)):+d}".replace("+0", "0"),
        warn_start=15, warn_end=20, warn_color=REDLINE,
        cool_start=-30, cool_end=0,  # vacuum side
        digital_label="AFR", digital_value="11.5",
        side="right",  # inner-right slot: faces OUT (dial on right half)
    )
    p = os.path.join(out_dir, "pill_boost.png")
    boost.save(p, optimize=True)
    saved["boost"] = boost
    print(f"  -> pill_boost.png        ({boost.width}x{boost.height})")

    # --- Slot 5: Fuel + odometer digital ---
    # Fuel uses 0..1 scaled with E, 1/4, 1/2, 3/4, F labels.
    fuel_labels = {0.0: "E", 0.25: "¼", 0.5: "½", 0.75: "¾", 1.0: "F"}

    def fuel_label(v: float) -> str:
        # Snap to nearest known label.
        k = min(fuel_labels.keys(), key=lambda kk: abs(kk - v))
        return fuel_labels[k]

    fuel = render_pill_gauge(
        title="FUEL",
        sub_title="",
        value_min=0.0, value_max=1.0,
        major_step=0.25, mid_step=0.125, minor_step=0.0625,
        label_formatter=fuel_label,
        warn_start=0.0, warn_end=0.10, warn_color=WARN_AMBER,
        digital_label="ODO", digital_value="042871",
        side="left",  # far-right slot: faces IN (dial on left half)
    )
    p = os.path.join(out_dir, "pill_fuel.png")
    fuel.save(p, optimize=True)
    saved["fuel"] = fuel
    print(f"  -> pill_fuel.png         ({fuel.width}x{fuel.height})")

    # --- Needles ---
    # Center tach: pointer must reach to the inside of the major-tick
    # numerals. Pointer length = H * 0.78 * 0.96 ≈ H * 0.749. Target
    # ≈ 540 px (just past the inner end of the major numerals).
    long_needle = render_needle(80, 720)
    p = os.path.join(out_dir, "needle_long.png")
    long_needle.save(p, optimize=True)
    print(f"  -> needle_long.png       ({long_needle.width}x{long_needle.height})")

    # Side pill: pointer should reach just inside the major-tick numerals.
    # Reach ≈ 395 px; target pointer ≈ 380 px => total height ≈ 510, width
    # ≈12% of height.
    short_needle = render_needle(58, 510)
    p = os.path.join(out_dir, "needle_short.png")
    short_needle.save(p, optimize=True)
    print(f"  -> needle_short.png      ({short_needle.width}x{short_needle.height})")

    # --- Preview composite ---
    preview = render_preview(saved, long_needle, short_needle)
    p = os.path.join(out_dir, "dashboard_preview.png")
    preview.save(p, optimize=True)
    print(f"  -> dashboard_preview.png ({preview.width}x{preview.height})")

    # --- Godot integration notes ---
    print()
    print("Godot integration:")
    print("  Center tach (center_tach.png):")
    print(f"    - size            : {CENTER_W}x{CENTER_H}")
    print(f"    - needle pivot    : ({CENTER_W // 2}, {CENTER_H // 2}) px")
    print( "    - rotation (CW+)  : rot_deg = 135 - (rpm/9000) * 270")
    print(f"    - needle: needle_long.png, pivot ({long_needle.width // 2}, "
          f"{int(long_needle.height * 0.78)})")
    print()
    print("  Pill gauges (pill_*.png):")
    pivot_inset_px = int(PILL_W * PILL_PIVOT_INSET_FRAC)
    print(f"    - size            : {PILL_W}x{PILL_H}")
    print(f"    - needle pivot    : side='right' -> ({pivot_inset_px}, {PILL_H // 2}) px")
    print(f"                        side='left'  -> ({PILL_W - pivot_inset_px}, {PILL_H // 2}) px")
    print(f"    - sweep ±{PILL_SWEEP_HALF_DEG}° from horizontal toward dial side")
    print( "    - rotation (math angle, CCW+ from +x, PIL y-down):")
    print(f"        side='right': angle = -{PILL_SWEEP_HALF_DEG} + t * {2*PILL_SWEEP_HALF_DEG}")
    print(f"        side='left' : angle = (180+{PILL_SWEEP_HALF_DEG}) - t * {2*PILL_SWEEP_HALF_DEG}")
    print(f"    - needle: needle_short.png, pivot ({short_needle.width // 2}, "
          f"{int(short_needle.height * 0.78)})")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
