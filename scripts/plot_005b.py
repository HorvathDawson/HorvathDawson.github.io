"""
Generate engineering plots for the A40 build blog.

Outputs PNG files to public/assets/projects/a40-austin/blog/plots/
Run from the repo root: python scripts/plot_005b.py

Constants come from the 005b analysis:
  - Miata NA front track 1405 mm, A40 target 1230 mm
  - CG: Miata 460 mm, A40 estimated 575 mm (+/-50 mm)
  - RC: Miata 45 mm, A40 39 mm (0.875 scaling)
  - Sprung mass: Miata 820 kg, A40 850 kg
  - Total mass: 950 kg
  - Front spring: 25 N/mm, MR 0.9 -> wheel rate 20,250 N/m
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from matplotlib.ticker import MultipleLocator

# ── Palette (matches blog CSS vars) ──────────────────────────
BG = "#0f172a"
TEXT = "#fcf7f0"
GOLD = "#f3de40"
PINK = "#f65e79"
PURPLE = "#8a3ab9"
BLUE = "#4978f4"
GRID = "#1e293b"
GRID2 = "#334155"
MIATA_C = "#3898ec"
A40_C = PINK
GREEN = "#34d399"

OUT_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "public",
    "assets",
    "projects",
    "a40-austin",
    "blog",
    "plots",
)
os.makedirs(OUT_DIR, exist_ok=True)

DPI = 250


def styled_fig(nrows=1, ncols=1, figsize=(7, 4.5)):
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    fig.patch.set_facecolor(BG)
    for ax in axes.flat if hasattr(axes, "flat") else [axes]:
        ax.set_facecolor(BG)
        ax.tick_params(colors=TEXT, labelsize=9)
        ax.xaxis.label.set_color(TEXT)
        ax.yaxis.label.set_color(TEXT)
        ax.title.set_color(TEXT)
        for spine in ax.spines.values():
            spine.set_color(GRID2)
        ax.grid(True, color=GRID, linewidth=0.5, alpha=0.6)
    return fig, axes


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  saved {path}")


# ── Shared constants ─────────────────────────────────────────
T_MIATA = 1405
T_A40 = 1230
H_CG_MIATA = 460
H_CG_A40 = 575
M_TOTAL = 950
M_S_MIATA = 820
M_S_A40 = 850
G_ACC = 9.81
AY = 0.8
KW_FRONT = 20_250
G_SHEAR = 80e9
L_EFF = 400  # mm ARB effective torsional length
# Installation ratio back-calculated from the post's stated value:
# stock Miata 19mm front ARB adds ~10,000 N-m/rad of front roll stiffness.
# K_bar(19mm) = 2,559 N-m/rad.  IR = sqrt(10000 / 2559) = 1.977.
# Actual measurement from the donor car will refine this.
IR_BAR = 1.977

# Rear: live axle on four-link.  Roll stiffness uses the spring base
# (lateral distance between coilover mounts on the axle housing), not
# the track width.  Estimated spring base ~950mm (narrowed Ford 8-inch
# housing, coilovers mounted near the bearing caps).
# Rear spring: 20 N/mm, MR ~1.0 (coilover acts directly on the axle tube).
# K_phi_r = K_w_rear * spring_base^2 / 2 = 20000 * 0.95^2 / 2 = 9,025 N-m/rad
SPRING_BASE_REAR = 950  # mm
KW_REAR = 20_000  # N/m (20 N/mm spring, MR ~1.0)
K_PHI_REAR = KW_REAR * (SPRING_BASE_REAR / 1000) ** 2 / 2  # 9,025

K_PHI_SPRING = KW_FRONT * (T_A40 / 1000) ** 2 / 2 + K_PHI_REAR  # ~24,343

# ── Miata NA front suspension geometry (all in mm) ────────────────
# Source: frontcontrolarms.pdf + frontcontrolpickups.pdf.
# All values marked TBD must be verified against the actual donor car.
# Coordinate convention: +x outboard, +y forward, +z up. Origin at hub/BJ.
SUSP = dict(
    # ── Knuckle / heights (front view) ──
    hub_z_ground=265,  # hub centre height above ground at ride height
    kpi_deg=12.0,  # kingpin inclination angle (front view, inward lean)
    # ── Knuckle BJ and steering arm positions relative to hub centre ──────────
    # Convention: (lat, fa, h) — lat outboard+, fa forward+, h up+, all mm.
    # Source: photogrammetric scan CAD model — treat as estimated until verified.
    lbj_from_hub=(-74.924, -8.827, -93.605),
    ubj_from_hub=(-124.698, -8.827, +139.400),
    steer_from_hub=(-65.990, +97.216, -75.697),
    # ── LCA inner pivot positions (confirmed from drawing) ─────────────────────
    # Lateral: from car CL.  Fore-aft origin: LCA front pivot.
    # BJ is lca_bj_fa mm FORWARD of the LCA front pivot.
    lca_from_cl=328.0,  # LCA inner pivot line: mm from car CL (both front & rear)
    lca_fa_span=323.5,  # LCA fore-aft span front-to-rear (c-t-c, mm)
    lca_bj_fa=25.0,  # BJ is 25 mm forward of LCA front pivot
    lca_z_rise=25.0,  # [est] LCA inner pivot is 25 mm ABOVE LBJ height (+ = above)
    # Coilover and ARB mounts: explicit (perp_from_pivot_line, fore-aft in arm frame)
    # Both lie on horizontal lines (constant y) between BJ and the pivot line.
    lca_coilover_perp=240.0,  # coilover: mm outboard from pivot line (x = -374.5+240 = -134.5)
    lca_coilover_fa=+25.0,  # coilover: fore-aft = +25mm (forward of BJ)
    lca_arb_perp=185.0,  # ARB end-link: mm outboard from pivot line (x = -374.5+185 = -189.5)
    lca_arb_fa=+35.0,  # ARB end-link: fore-aft = +35mm (forward of BJ)
    # ── UCA inner pivot positions (confirmed from drawing) ─────────────────────
    # UCA inner pivots sit 50mm outboard of LCA inner pivots (378mm from CL).
    # Pivot positions are fore-aft from BJ (not symmetric).
    uca_hub_to_pivot=324.5,  # lateral: hub centre to UCA inner pivot line (mm)
    uca_fa_front=113.5,  # UCA front pivot: +113.5mm forward of BJ
    uca_fa_rear=143.5,  # UCA rear pivot: 143.5mm rearward of BJ (negative in coords)
    uca_z_front=192.0,  # UCA front pivot height above LCA pivot [verify]
    uca_z_rear=170.0,  # UCA rear pivot height above LCA pivot [verify]
    uca_z_drop=15.0,  # [est] UCA inner pivot 15 mm below UBJ height (+ = below UBJ)
    # ── Pivot bushing dimensions (fore-aft length, mm) ──────────────────
    lca_f_bushing=73.0,  # LCA front pivot bushing length (mm)
    lca_r_bushing=60.0,  # LCA rear pivot bushing length (mm)
    uca_bushing=56.0,  # UCA pivot bushing length (mm, both pivots)
    pivot_width=10.0,  # visual width for all pivot rectangles (mm)
    # ── Tire (for RC construction) ──
    tire_w=185,  # tire section width mm
    tire_od=577,  # 185/60R14 outer diameter mm
)


def susp_geometry():
    """Return derived suspension pickup positions in car-frame coordinates.

    All positions are (lat, fa, z) tuples:
      lat: mm from car CL         (+outboard)
      fa:  mm from LCA front pivot (+forward, −rearward)
      z:   mm from LCA inner pivot height (+up)

    Call this from any plot that needs pickup coordinates. Updating SUSP
    propagates to every consumer automatically.
    """
    HT = T_MIATA / 2  # 702.5 mm half-track
    uca_lat_cl = HT - SUSP["uca_hub_to_pivot"]  # 378.0 mm from car CL
    return dict(
        half_track=HT,
        lca_hub_to_pivot=HT - SUSP["lca_from_cl"],  # 374.5 mm hub centre to inner pivot
        # Inner pivot positions (lat from CL, fa from LCA-F pivot, z from LCA pivot)
        lca_f=(SUSP["lca_from_cl"], 0.0, 0.0),
        lca_r=(SUSP["lca_from_cl"], -SUSP["lca_fa_span"], 0.0),
        uca_f=(
            uca_lat_cl,
            SUSP["lca_bj_fa"] + SUSP["uca_fa_front"],
            SUSP["uca_z_front"],
        ),
        uca_r=(uca_lat_cl, SUSP["lca_bj_fa"] - SUSP["uca_fa_rear"], SUSP["uca_z_rear"]),
        # Coilover and ARB mounts on LCA (lateral from CL, fa from LCA-F pivot, z=0)
        coilover=(
            SUSP["lca_from_cl"] + SUSP["lca_coilover_perp"],
            SUSP["lca_coilover_fa"],
            0.0,
        ),
        arb=(SUSP["lca_from_cl"] + SUSP["lca_arb_perp"], SUSP["lca_arb_fa"], 0.0),
    )


def arb_K_bar(d_mm):
    """Torsional stiffness of a solid round bar (N-m/rad)."""
    return G_SHEAR * np.pi * (d_mm / 1000) ** 4 / (32 * L_EFF / 1000)


def arb_roll_stiffness(d_mm):
    """Roll stiffness contribution from one ARB (N-m/rad)."""
    return arb_K_bar(d_mm) * IR_BAR**2


def roll_angle_deg(cg_mm, K_phi_total, m_s=M_S_A40, h_rc=None):
    if h_rc is None:
        h_rc = H_RC_A40
    arm = (cg_mm - h_rc) / 1000
    moment = m_s * AY * G_ACC * arm
    grav = m_s * G_ACC * arm
    denom = np.where(K_phi_total - grav > 0, K_phi_total - grav, np.nan)
    return np.degrees(moment / denom)


# ====================================================================
# 1. Roll angle vs CG height, parameterized by ARB diameter
# ====================================================================
def plot_roll_vs_cg():
    fig, ax = styled_fig(figsize=(7, 5.2))
    cg = np.linspace(350, 700, 400)

    roll_spring = roll_angle_deg(cg, K_PHI_SPRING)
    ax.plot(
        cg,
        roll_spring,
        color=TEXT,
        linewidth=2,
        alpha=0.5,
        linestyle="--",
        label=f"Springs only ({K_PHI_SPRING/1000:.1f} kN-m/rad)",
    )

    diameters = [19, 22, 25, 28]
    colors = [PURPLE, BLUE, GREEN, GOLD]
    for d, c in zip(diameters, colors):
        K_front = arb_roll_stiffness(d)
        K_rear = K_front * 0.7
        K_total = K_PHI_SPRING + K_front + K_rear
        K_bar = arb_K_bar(d)
        roll = roll_angle_deg(cg, K_total)
        ax.plot(
            cg,
            roll,
            color=c,
            linewidth=1.8,
            label=f"{d} mm  ({K_bar/1000:.1f} kN-m/rad bar, {K_total/1000:.0f} total)",
        )

    ax.axhline(
        3.5, color=PINK, linestyle=":", linewidth=1, alpha=0.6, label="3.5\u00b0 target"
    )
    ax.axvline(575, color=TEXT, linestyle=":", linewidth=0.6, alpha=0.3)
    ax.text(578, 17, "est. CG", color=TEXT, fontsize=7, alpha=0.5)

    # CG sensitivity: annotate key CG values with springs-only roll
    # Place labels alternating above/below and offset enough to clear the curve
    cg_points = [500, 550, 600]
    y_offsets = [1.8, -2.0, 1.8]
    for cg_val, dy in zip(cg_points, y_offsets):
        roll_val = roll_angle_deg(np.array([cg_val]), K_PHI_SPRING)[0]
        ax.plot(cg_val, roll_val, "s", color=TEXT, markersize=4, alpha=0.6, zorder=5)
        ax.annotate(
            f"{roll_val:.1f}\u00b0",
            xy=(cg_val, roll_val),
            xytext=(cg_val, roll_val + dy),
            fontsize=6.5,
            color=TEXT,
            alpha=0.6,
            ha="center",
            arrowprops=dict(arrowstyle="-", color=TEXT, lw=0.4, alpha=0.3),
        )

    ax.set_xlabel("CG height (mm)")
    ax.set_ylabel("Body roll at 0.8 G (\u00b0)")
    ax.set_title("Roll angle vs CG height by front ARB diameter")
    ax.legend(
        fontsize=7, facecolor=BG, edgecolor=GRID2, labelcolor=TEXT, loc="upper left"
    )
    ax.set_xlim(350, 700)
    ax.set_ylim(0, 20)
    ax.xaxis.set_major_locator(MultipleLocator(50))
    save(fig, "roll_vs_cg.png")


# ====================================================================
# 1b. Front-view roll center construction: Miata vs A40 track
#
#     All pickup points are defined relative to:
#       x = 0  at vehicle centreline
#       y = 0  at the ground plane
#     Outer (ball-joint) positions are at the wheel centre x-coordinate.
#     Inner pivot positions are inboard of the ball joints.
#
#     To plug in real suspension numbers later, change the values in
#     the ``pickups`` dicts below.  Everything else (IC, RC, tire
#     rectangle, construction lines) is computed from those inputs.
# ====================================================================
def _build_suspension(half_track, *, hub_z_ground=None, tire_od=None):
    """Derive front-view suspension positions for one side.

    All dimensions come from SUSP.  Only *half_track* changes between
    configurations (702.5 mm for Miata, 615 mm for A40).  The entire
    assembly translates inboard, preserving arm geometry.

    Optional overrides:
      hub_z_ground — hub centre height above ground (default: SUSP value).
      tire_od      — tire outer diameter for drawing (default: SUSP value).

    Returns a dict with absolute positions for the right side:
        lbj, ubj, lca_inner, uca_inner, cp, ic, rc — numpy [x, y]
        x = lateral from car CL (mm), y = height above ground (mm).
    """
    ht = half_track
    hz = hub_z_ground if hub_z_ground is not None else SUSP["hub_z_ground"]
    tod = tire_od if tire_od is not None else SUSP["tire_od"]

    # Ball joints: hub centre + scan offset
    lbj = np.array([ht + SUSP["lbj_from_hub"][0], hz + SUSP["lbj_from_hub"][2]])
    ubj = np.array([ht + SUSP["ubj_from_hub"][0], hz + SUSP["ubj_from_hub"][2]])

    # Inner pivots: inboard of hub centre by arm lateral dimensions.
    # These lateral values are hub-to-inner-pivot, NOT BJ-to-inner-pivot.
    lca_hub_to_pivot = T_MIATA / 2 - SUSP["lca_from_cl"]  # 374.5 mm
    lca_inner = np.array([ht - lca_hub_to_pivot, lbj[1] + SUSP["lca_z_rise"]])

    uca_inner = np.array([ht - SUSP["uca_hub_to_pivot"], ubj[1] - SUSP["uca_z_drop"]])

    cp = np.array([ht, 0.0])

    # Instant centre: intersection of the two arm lines extended
    d_low = lbj - lca_inner
    d_up = ubj - uca_inner
    A_mat = np.array([[d_low[0], -d_up[0]], [d_low[1], -d_up[1]]])
    b_vec = uca_inner - lca_inner
    ts = np.linalg.solve(A_mat, b_vec)
    ic = lca_inner + ts[0] * d_low

    # RC height: line from contact patch through IC to centreline (x=0)
    d_rc = ic - cp
    t_rc = -cp[0] / d_rc[0]
    rc = cp + t_rc * d_rc

    return dict(
        half_track=ht,
        tire_w=SUSP["tire_w"],
        tire_od=tod,
        lbj=lbj,
        ubj=ubj,
        lca_inner=lca_inner,
        uca_inner=uca_inner,
        cp=cp,
        ic=ic,
        rc=rc,
    )


# RC heights computed from geometry model (mm above ground).
_A40_OD = 646.0
H_RC_MIATA = _build_suspension(T_MIATA / 2)["rc"][1]
H_RC_A40 = _build_suspension(
    T_A40 / 2,
    hub_z_ground=SUSP["hub_z_ground"] + (_A40_OD - SUSP["tire_od"]) / 2,
    tire_od=_A40_OD,
)["rc"][1]


def plot_rc_construction():
    """Front-view RC construction: Miata vs A40 track width.

    Both configurations use the stock Miata tire (185/60R14, 577 mm OD)
    and the same hub height.  Only the track width changes.
    """
    fig, ax = styled_fig(figsize=(10, 8))
    ax.set_aspect(2)

    stock_od = 577.0
    stock_hz = SUSP["hub_z_ground"]

    configs = [
        ("Miata track (1405 mm)", T_MIATA / 2, stock_hz, stock_od, MIATA_C, 0.45),
        ("A40 track (1230 mm)", T_A40 / 2, stock_hz, stock_od, A40_C, 0.90),
    ]

    def draw_side(half_track, hub_z, tire_od, color, alpha, side=1):
        p = _build_suspension(half_track, hub_z_ground=hub_z, tire_od=tire_od)
        s = side

        def mx(pt):
            return np.array([s * pt[0], pt[1]])

        lbj = mx(p["lbj"])
        ubj = mx(p["ubj"])
        lca_inner = mx(p["lca_inner"])
        uca_inner = mx(p["uca_inner"])
        cp = mx(p["cp"])
        ic = mx(p["ic"])
        htx = s * p["half_track"]

        tire_h = p["tire_od"]
        tw = p["tire_w"]
        tire_rect = plt.Rectangle(
            (htx - tw / 2, 0),
            tw,
            tire_h,
            linewidth=1.2,
            edgecolor=color,
            facecolor=color,
            alpha=alpha * 0.10,
            zorder=2,
        )
        ax.add_patch(tire_rect)
        xs = [htx - tw / 2, htx + tw / 2, htx + tw / 2, htx - tw / 2, htx - tw / 2]
        ys = [0, 0, tire_h, tire_h, 0]
        ax.plot(xs, ys, color=color, linewidth=1.0, alpha=alpha * 0.45, zorder=3)

        ax.plot(
            [lca_inner[0], lbj[0]],
            [lca_inner[1], lbj[1]],
            color=color,
            linewidth=2.5,
            alpha=alpha,
            solid_capstyle="round",
        )
        ax.plot(
            [uca_inner[0], ubj[0]],
            [uca_inner[1], ubj[1]],
            color=color,
            linewidth=2.5,
            alpha=alpha,
            solid_capstyle="round",
        )
        ax.plot(
            [lbj[0], ubj[0]],
            [lbj[1], ubj[1]],
            color=color,
            linewidth=3,
            alpha=alpha,
            solid_capstyle="round",
        )
        for pt in [lca_inner, uca_inner, lbj, ubj]:
            ax.plot(pt[0], pt[1], "o", color=color, markersize=4, alpha=alpha, zorder=5)

        ax.plot(
            [lca_inner[0], ic[0]],
            [lca_inner[1], ic[1]],
            color=color,
            linewidth=0.8,
            alpha=alpha * 0.4,
            linestyle="--",
        )
        ax.plot(
            [uca_inner[0], ic[0]],
            [uca_inner[1], ic[1]],
            color=color,
            linewidth=0.8,
            alpha=alpha * 0.4,
            linestyle="--",
        )
        ax.plot(ic[0], ic[1], "D", color=color, markersize=5, alpha=alpha, zorder=5)

        return ic, cp

    def draw_rc_lines(ic_r, cp_r, ic_l, cp_l, color, alpha):
        rc_pts = []
        for cp_pt, ic_pt in [(cp_r, ic_r), (cp_l, ic_l)]:
            d = ic_pt - cp_pt
            t = -cp_pt[0] / d[0]
            rc = cp_pt + t * d
            ax.plot(
                [cp_pt[0], ic_pt[0], rc[0]],
                [cp_pt[1], ic_pt[1], rc[1]],
                color=color,
                linewidth=1.2,
                alpha=alpha * 0.7,
                linestyle="-.",
                zorder=4,
            )
            rc_pts.append(rc)
        rc_y = (rc_pts[0][1] + rc_pts[1][1]) / 2
        ax.plot(
            0,
            rc_y,
            "s",
            color=color,
            markersize=8,
            alpha=min(alpha + 0.2, 1.0),
            zorder=6,
        )
        return rc_y

    rc_results = []
    ann_offsets = [55, -55]
    for idx, (label, ht, hz, od, col, alp) in enumerate(configs):
        ic_r, cp_r = draw_side(ht, hz, od, col, alp, side=1)
        ic_l, cp_l = draw_side(ht, hz, od, col, alp, side=-1)
        rc_y = draw_rc_lines(ic_r, cp_r, ic_l, cp_l, col, alp)
        rc_results.append((label, rc_y, col, alp))

        ax.annotate(
            f"RC = {rc_y:.1f} mm",
            xy=(0, rc_y),
            xytext=(120, rc_y + ann_offsets[idx]),
            fontsize=8,
            color=col,
            fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=col, lw=0.8),
        )

    # IC labels (right side only)
    for idx, (label, ht, hz, od, col, alp) in enumerate(configs):
        p = _build_suspension(ht, hub_z_ground=hz, tire_od=od)
        ic = p["ic"]
        short = "Miata" if idx == 0 else "A40"
        yoff = 40 if idx == 0 else -50
        ax.annotate(
            f"IC ({short})",
            xy=(ic[0], ic[1]),
            xytext=(ic[0] + 120, ic[1] + yoff),
            fontsize=7.5,
            color=col,
            alpha=max(alp, 0.6),
            arrowprops=dict(arrowstyle="->", color=col, lw=0.6, alpha=0.4),
        )

    ax.axhline(0, color=TEXT, linewidth=1, alpha=0.3)
    ax.axvline(0, color=TEXT, linewidth=0.5, alpha=0.2, linestyle=":")

    ax.text(
        T_MIATA / 2,
        -30,
        f"Miata ({T_MIATA} mm)",
        color=MIATA_C,
        fontsize=7.5,
        ha="center",
        alpha=0.5,
    )
    ax.text(
        T_A40 / 2,
        -30,
        f"A40 ({T_A40} mm)",
        color=A40_C,
        fontsize=7.5,
        ha="center",
        alpha=0.85,
    )
    ax.text(5, -30, "CL", color=TEXT, fontsize=7, alpha=0.3, ha="left")

    ratio = rc_results[1][1] / rc_results[0][1]
    ax.text(
        0.02,
        0.97,
        f"Track ratio: {T_A40}/{T_MIATA} = {T_A40 / T_MIATA:.3f}\n"
        f"RC ratio: {rc_results[1][1]:.1f}/{rc_results[0][1]:.1f} = {ratio:.3f}\n"
        f"Same linkage shifted inboard.\n"
        f"Narrowing alone lowers the RC.",
        fontsize=8,
        color=TEXT,
        alpha=0.8,
        transform=ax.transAxes,
        va="top",
        ha="left",
        bbox=dict(boxstyle="round,pad=0.4", fc=BG, ec=GRID2, alpha=0.9),
    )

    ax.set_xlabel("Front view position (mm)")
    ax.set_ylabel("Height (mm)")
    ax.set_title("Roll centre construction: Miata vs A40 track width")

    # Auto-fit limits to include tires, ICs, and RC points
    x_pad = 180
    all_x = [T_MIATA / 2, -T_MIATA / 2, T_A40 / 2, -T_A40 / 2]
    all_y = [0, stock_od]
    for idx2, (_, ht2, hz2, od2, _, _) in enumerate(configs):
        p2 = _build_suspension(ht2, hub_z_ground=hz2, tire_od=od2)
        all_x.extend([p2["ic"][0], -p2["ic"][0]])
        all_y.append(p2["ic"][1])
    for _, rc_y2, _, _ in rc_results:
        all_y.append(rc_y2)
    ax.set_xlim(min(all_x) - x_pad, max(all_x) + x_pad)
    ax.set_ylim(min(all_y) - 60, max(all_y) + 100)

    from matplotlib.lines import Line2D

    legend_elements = [
        Line2D([0], [0], color=col, linewidth=2.5, alpha=alp, label=label)
        for label, _, col, alp in rc_results
    ]
    ax.legend(
        handles=legend_elements,
        fontsize=7.5,
        facecolor=BG,
        edgecolor=GRID2,
        labelcolor=TEXT,
        loc="upper right",
    )

    save(fig, "rc_construction.png")


# ====================================================================
# 1c. RC construction — tire-size comparison at A40 track
# ====================================================================
def plot_rc_tire_comparison():
    """Front-view RC construction: stock Miata vs stock A40 tire height.

    Both configurations use the A40 track width (1230 mm).  Only the
    tire diameter changes, shifting the entire assembly vertically.
    """
    fig, ax = styled_fig(figsize=(10, 8))
    ax.set_aspect(2)

    stock_od = 577.0  # 185/60R14
    a40_od = 646.0  # 5.25-16 (stock A40)
    stock_hz = SUSP["hub_z_ground"]  # 265 mm
    delta_r = (a40_od - stock_od) / 2  # +34.5 mm
    a40_hz = stock_hz + delta_r

    tires = [
        ("185/60R14 (stock Miata)", stock_od, stock_hz, MIATA_C, 0.45),
        ("5.25-16 (stock A40)", a40_od, a40_hz, A40_C, 0.90),
    ]
    ht = T_A40 / 2  # all at A40 track

    def draw_side(half_track, hub_z, tire_od, color, alpha, side=1):
        p = _build_suspension(half_track, hub_z_ground=hub_z, tire_od=tire_od)
        s = side

        def mx(pt):
            return np.array([s * pt[0], pt[1]])

        lbj = mx(p["lbj"])
        ubj = mx(p["ubj"])
        lca_inner = mx(p["lca_inner"])
        uca_inner = mx(p["uca_inner"])
        cp = mx(p["cp"])
        ic = mx(p["ic"])
        htx = s * p["half_track"]

        # Tire rectangle
        tire_h = p["tire_od"]
        tw = p["tire_w"]
        tire_rect = plt.Rectangle(
            (htx - tw / 2, 0),
            tw,
            tire_h,
            linewidth=1.2,
            edgecolor=color,
            facecolor=color,
            alpha=alpha * 0.10,
            zorder=2,
        )
        ax.add_patch(tire_rect)
        xs = [htx - tw / 2, htx + tw / 2, htx + tw / 2, htx - tw / 2, htx - tw / 2]
        ys = [0, 0, tire_h, tire_h, 0]
        ax.plot(xs, ys, color=color, linewidth=1.0, alpha=alpha * 0.45, zorder=3)

        # Arms
        ax.plot(
            [lca_inner[0], lbj[0]],
            [lca_inner[1], lbj[1]],
            color=color,
            linewidth=2.2,
            alpha=alpha,
            solid_capstyle="round",
        )
        ax.plot(
            [uca_inner[0], ubj[0]],
            [uca_inner[1], ubj[1]],
            color=color,
            linewidth=2.2,
            alpha=alpha,
            solid_capstyle="round",
        )
        ax.plot(
            [lbj[0], ubj[0]],
            [lbj[1], ubj[1]],
            color=color,
            linewidth=2.8,
            alpha=alpha,
            solid_capstyle="round",
        )
        for pt in [lca_inner, uca_inner, lbj, ubj]:
            ax.plot(
                pt[0], pt[1], "o", color=color, markersize=3.5, alpha=alpha, zorder=5
            )

        # Extension lines to IC
        ax.plot(
            [lca_inner[0], ic[0]],
            [lca_inner[1], ic[1]],
            color=color,
            linewidth=0.7,
            alpha=alpha * 0.35,
            linestyle="--",
        )
        ax.plot(
            [uca_inner[0], ic[0]],
            [uca_inner[1], ic[1]],
            color=color,
            linewidth=0.7,
            alpha=alpha * 0.35,
            linestyle="--",
        )
        ax.plot(ic[0], ic[1], "D", color=color, markersize=4, alpha=alpha, zorder=5)

        return ic, cp

    def draw_rc_lines(ic_r, cp_r, ic_l, cp_l, color, alpha):
        rc_pts = []
        for cp_pt, ic_pt in [(cp_r, ic_r), (cp_l, ic_l)]:
            d = ic_pt - cp_pt
            t = -cp_pt[0] / d[0]
            rc = cp_pt + t * d
            ax.plot(
                [cp_pt[0], ic_pt[0], rc[0]],
                [cp_pt[1], ic_pt[1], rc[1]],
                color=color,
                linewidth=1.0,
                alpha=alpha * 0.6,
                linestyle="-.",
                zorder=4,
            )
            rc_pts.append(rc)
        rc_y = (rc_pts[0][1] + rc_pts[1][1]) / 2
        ax.plot(
            0,
            rc_y,
            "s",
            color=color,
            markersize=7,
            alpha=min(alpha + 0.15, 1.0),
            zorder=6,
        )
        return rc_y

    # Draw each tire configuration
    rc_values = []
    ann_offsets = [55, -55]  # stagger annotations
    for idx, (label, od, hz, col, alp) in enumerate(tires):
        ic_r, cp_r = draw_side(ht, hz, od, col, alp, side=1)
        ic_l, cp_l = draw_side(ht, hz, od, col, alp, side=-1)
        rc_y = draw_rc_lines(ic_r, cp_r, ic_l, cp_l, col, alp)
        rc_values.append((label, od, rc_y, col, alp))

        # RC annotation
        ax.annotate(
            f"RC = {rc_y:.1f} mm  ({label})",
            xy=(0, rc_y),
            xytext=(120, rc_y + ann_offsets[idx]),
            fontsize=7.5,
            color=col,
            fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=col, lw=0.7),
        )

    # Ground line & centreline
    ax.axhline(0, color=TEXT, linewidth=1, alpha=0.3)
    ax.axvline(0, color=TEXT, linewidth=0.5, alpha=0.2, linestyle=":")

    # Track label
    ax.text(
        ht,
        -30,
        f"A40 track ({T_A40} mm)",
        color=A40_C,
        fontsize=7.5,
        ha="center",
        alpha=0.85,
    )
    ax.text(5, -30, "CL", color=TEXT, fontsize=7, alpha=0.3, ha="left")

    # Info box
    lines = [f"Track: {T_A40} mm (all configs)"]
    for label, od, rc_y, _, _ in rc_values:
        lines.append(f"{label}: OD {od:.0f} mm, RC {rc_y:.1f} mm")
    ax.text(
        0.02,
        0.97,
        "\n".join(lines),
        fontsize=7,
        color=TEXT,
        alpha=0.8,
        transform=ax.transAxes,
        va="top",
        ha="left",
        bbox=dict(boxstyle="round,pad=0.4", fc=BG, ec=GRID2, alpha=0.9),
    )

    ax.set_xlabel("Front view position (mm)")
    ax.set_ylabel("Height (mm)")
    ax.set_title("Roll centre construction: tire height at A40 track")

    # Auto-fit limits
    x_pad = 180
    all_x = [ht, -ht]
    all_y = [0, a40_od, stock_od]
    for _, od2, hz2, _, _ in tires:
        p2 = _build_suspension(ht, hub_z_ground=hz2, tire_od=od2)
        all_x.extend([p2["ic"][0], -p2["ic"][0]])
        all_y.append(p2["ic"][1])
    for _, _, rc_y2, _, _ in rc_values:
        all_y.append(rc_y2)
    ax.set_xlim(min(all_x) - x_pad, max(all_x) + x_pad)
    ax.set_ylim(min(all_y) - 60, max(all_y) + 100)

    from matplotlib.lines import Line2D

    legend_elements = [
        Line2D([0], [0], color=col, linewidth=2.2, alpha=alp, label=label)
        for label, _, _, col, alp in rc_values
    ]
    ax.legend(
        handles=legend_elements,
        fontsize=7,
        facecolor=BG,
        edgecolor=GRID2,
        labelcolor=TEXT,
        loc="upper right",
    )

    save(fig, "rc_tire_comparison.png")


# ====================================================================
# 1d. RC construction — combined: 2 tracks × 2 tire heights
# ====================================================================
def plot_rc_combined():
    """Front-view RC construction: stock Miata vs the actual A40 build.

    Miata: stock track (1405 mm) + stock tire (577 mm OD).
    A40:   narrowed track (1230 mm) + taller tire (646 mm OD).
    """
    fig, ax = styled_fig(figsize=(10, 8))
    ax.set_aspect(2)

    stock_od = 577.0
    a40_od = 646.0
    stock_hz = SUSP["hub_z_ground"]
    delta_r = (a40_od - stock_od) / 2
    a40_hz = stock_hz + delta_r

    configs = [
        (
            "Stock Miata (1405 mm, 577 mm OD)",
            T_MIATA / 2,
            stock_hz,
            stock_od,
            MIATA_C,
            0.45,
        ),
        ("A40 build (1230 mm, 646 mm OD)", T_A40 / 2, a40_hz, a40_od, A40_C, 0.90),
    ]

    def draw_side(half_track, hub_z, tire_od, color, alpha, side=1):
        p = _build_suspension(half_track, hub_z_ground=hub_z, tire_od=tire_od)
        s = side

        def mx(pt):
            return np.array([s * pt[0], pt[1]])

        lbj = mx(p["lbj"])
        ubj = mx(p["ubj"])
        lca_inner = mx(p["lca_inner"])
        uca_inner = mx(p["uca_inner"])
        cp = mx(p["cp"])
        ic = mx(p["ic"])
        htx = s * p["half_track"]

        tire_h = p["tire_od"]
        tw = p["tire_w"]
        rect = plt.Rectangle(
            (htx - tw / 2, 0),
            tw,
            tire_h,
            linewidth=1.0,
            edgecolor=color,
            facecolor=color,
            alpha=alpha * 0.08,
            zorder=2,
        )
        ax.add_patch(rect)
        xs = [htx - tw / 2, htx + tw / 2, htx + tw / 2, htx - tw / 2, htx - tw / 2]
        ys = [0, 0, tire_h, tire_h, 0]
        ax.plot(xs, ys, color=color, linewidth=0.9, alpha=alpha * 0.4, zorder=3)

        ax.plot(
            [lca_inner[0], lbj[0]],
            [lca_inner[1], lbj[1]],
            color=color,
            linewidth=2.0,
            alpha=alpha,
            solid_capstyle="round",
        )
        ax.plot(
            [uca_inner[0], ubj[0]],
            [uca_inner[1], ubj[1]],
            color=color,
            linewidth=2.0,
            alpha=alpha,
            solid_capstyle="round",
        )
        ax.plot(
            [lbj[0], ubj[0]],
            [lbj[1], ubj[1]],
            color=color,
            linewidth=2.5,
            alpha=alpha,
            solid_capstyle="round",
        )
        for pt in [lca_inner, uca_inner, lbj, ubj]:
            ax.plot(
                pt[0], pt[1], "o", color=color, markersize=3.5, alpha=alpha, zorder=5
            )

        ax.plot(
            [lca_inner[0], ic[0]],
            [lca_inner[1], ic[1]],
            color=color,
            linewidth=0.6,
            alpha=alpha * 0.3,
            linestyle="--",
        )
        ax.plot(
            [uca_inner[0], ic[0]],
            [uca_inner[1], ic[1]],
            color=color,
            linewidth=0.6,
            alpha=alpha * 0.3,
            linestyle="--",
        )
        ax.plot(ic[0], ic[1], "D", color=color, markersize=4, alpha=alpha, zorder=5)
        return ic, cp

    def draw_rc_lines(ic_r, cp_r, ic_l, cp_l, color, alpha):
        rc_pts = []
        for cp_pt, ic_pt in [(cp_r, ic_r), (cp_l, ic_l)]:
            d = ic_pt - cp_pt
            t = -cp_pt[0] / d[0]
            rc = cp_pt + t * d
            ax.plot(
                [cp_pt[0], ic_pt[0], rc[0]],
                [cp_pt[1], ic_pt[1], rc[1]],
                color=color,
                linewidth=0.9,
                alpha=alpha * 0.55,
                linestyle="-.",
                zorder=4,
            )
            rc_pts.append(rc)
        rc_y = (rc_pts[0][1] + rc_pts[1][1]) / 2
        ax.plot(
            0,
            rc_y,
            "s",
            color=color,
            markersize=7,
            alpha=min(alpha + 0.15, 1.0),
            zorder=6,
        )
        return rc_y

    rc_results = []
    ann_offsets = [55, -55]
    all_ic = []
    for idx, (label, ht, hz, od, col, alp) in enumerate(configs):
        ic_r, cp_r = draw_side(ht, hz, od, col, alp, side=1)
        ic_l, cp_l = draw_side(ht, hz, od, col, alp, side=-1)
        rc_y = draw_rc_lines(ic_r, cp_r, ic_l, cp_l, col, alp)
        rc_results.append((label, rc_y, col, alp))
        # Collect IC positions for auto-fitting limits
        p = _build_suspension(ht, hub_z_ground=hz, tire_od=od)
        all_ic.append(p["ic"])
        ax.annotate(
            f"RC = {rc_y:.1f} mm",
            xy=(0, rc_y),
            xytext=(120, rc_y + ann_offsets[idx]),
            fontsize=7.5,
            color=col,
            fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=col, lw=0.7),
        )

    ax.axhline(0, color=TEXT, linewidth=1, alpha=0.3)
    ax.axvline(0, color=TEXT, linewidth=0.5, alpha=0.2, linestyle=":")

    ax.text(
        T_MIATA / 2,
        -30,
        f"Miata ({T_MIATA} mm)",
        color=MIATA_C,
        fontsize=7.5,
        ha="center",
        alpha=0.5,
    )
    ax.text(
        T_A40 / 2,
        -30,
        f"A40 ({T_A40} mm)",
        color=A40_C,
        fontsize=7.5,
        ha="center",
        alpha=0.85,
    )
    ax.text(5, -30, "CL", color=TEXT, fontsize=7, alpha=0.3, ha="left")

    # Info box
    ratio = rc_results[1][1] / rc_results[0][1]
    ax.text(
        0.02,
        0.97,
        f"Miata: track {T_MIATA} mm, tire OD {stock_od:.0f} mm\n"
        f"A40: track {T_A40} mm, tire OD {a40_od:.0f} mm\n"
        f"RC ratio: {rc_results[1][1]:.1f}/{rc_results[0][1]:.1f} = {ratio:.3f}",
        fontsize=7.5,
        color=TEXT,
        alpha=0.8,
        transform=ax.transAxes,
        va="top",
        ha="left",
        bbox=dict(boxstyle="round,pad=0.4", fc=BG, ec=GRID2, alpha=0.9),
    )

    ax.set_xlabel("Front view position (mm)")
    ax.set_ylabel("Height (mm)")
    ax.set_title("Roll centre construction: stock Miata vs A40 build")

    # Auto-fit limits to include tires, ICs, and RC points
    x_pad = 180
    all_x = [T_MIATA / 2, -T_MIATA / 2, T_A40 / 2, -T_A40 / 2]
    all_y = [0, stock_od, a40_od]
    for ic_pt in all_ic:
        all_x.extend([ic_pt[0], -ic_pt[0]])
        all_y.append(ic_pt[1])
    for _, rc_y, _, _ in rc_results:
        all_y.append(rc_y)
    ax.set_xlim(min(all_x) - x_pad, max(all_x) + x_pad)
    ax.set_ylim(min(all_y) - 60, max(all_y) + 100)

    from matplotlib.lines import Line2D

    legend_elements = [
        Line2D([0], [0], color=col, linewidth=2.2, alpha=alp, label=label)
        for label, _, col, alp in rc_results
    ]
    ax.legend(
        handles=legend_elements,
        fontsize=7,
        facecolor=BG,
        edgecolor=GRID2,
        labelcolor=TEXT,
        loc="upper right",
    )

    save(fig, "rc_combined.png")


# ====================================================================
# 2. Track width effects (ratios vs track)
# ====================================================================
def plot_track_effects():
    fig, ax = styled_fig()
    tracks = np.linspace(1000, 1500, 200)
    ratio = tracks / T_MIATA

    ax.plot(tracks, ratio, color=BLUE, linewidth=2, label="Roll center height ratio")
    ax.plot(
        tracks, ratio**2, color=PURPLE, linewidth=2, label="Spring roll stiffness ratio"
    )
    ax.plot(tracks, 1 / ratio, color=PINK, linewidth=2, label="Weight transfer ratio")

    ax.axvline(T_MIATA, color=MIATA_C, linestyle="--", linewidth=1, alpha=0.6)
    ax.axvline(T_A40, color=A40_C, linestyle="--", linewidth=1, alpha=0.6)
    ax.text(T_MIATA + 8, 1.42, "Miata", color=MIATA_C, fontsize=8, alpha=0.7)
    ax.text(T_A40 + 8, 1.42, "A40", color=A40_C, fontsize=8, alpha=0.7)
    ax.axhline(1.0, color=TEXT, linestyle=":", linewidth=0.5, alpha=0.3)

    ax.set_xlabel("Front track width (mm)")
    ax.set_ylabel("Ratio relative to stock Miata")
    ax.set_title("How track width affects key parameters")
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID2, labelcolor=TEXT)
    ax.set_xlim(1000, 1500)
    ax.set_ylim(0.4, 1.6)
    save(fig, "track_effects.png")


# ====================================================================
# 3. ARB sizing: required roll stiffness vs target angle, by diameter
# ====================================================================
def plot_arb_sizing():
    fig, ax = styled_fig()
    target_roll = np.linspace(2.0, 6.0, 200)
    target_rad = np.radians(target_roll)

    arm = (H_CG_A40 - H_RC_A40) / 1000
    moment = M_S_A40 * AY * G_ACC * arm
    grav = M_S_A40 * G_ACC * arm
    K_req = moment / target_rad + grav
    ax.plot(
        target_roll,
        K_req / 1000,
        color=TEXT,
        linewidth=2,
        alpha=0.8,
        label="Required total (CG = 575 mm)",
    )

    # CG uncertainty band
    for cg_edge in [525, 625]:
        a = (cg_edge - H_RC_A40) / 1000
        K = (M_S_A40 * AY * G_ACC * a) / target_rad + M_S_A40 * G_ACC * a
        ax.plot(target_roll, K / 1000, color=TEXT, linewidth=0.8, alpha=0.3)
    a_lo = (525 - H_RC_A40) / 1000
    a_hi = (625 - H_RC_A40) / 1000
    K_lo = (M_S_A40 * AY * G_ACC * a_lo) / target_rad + M_S_A40 * G_ACC * a_lo
    K_hi = (M_S_A40 * AY * G_ACC * a_hi) / target_rad + M_S_A40 * G_ACC * a_hi
    ax.fill_between(
        target_roll,
        K_lo / 1000,
        K_hi / 1000,
        alpha=0.1,
        color=TEXT,
        label="CG range 525-625 mm",
    )

    ax.axhline(
        K_PHI_SPRING / 1000,
        color=PINK,
        linestyle=":",
        linewidth=1,
        alpha=0.6,
        label=f"Springs only ({K_PHI_SPRING/1000:.1f} kN-m/rad)",
    )
    diameters = [19, 22, 25, 28]
    colors = [PURPLE, BLUE, GREEN, GOLD]
    for d, c in zip(diameters, colors):
        K_total = K_PHI_SPRING + arb_roll_stiffness(d) + arb_roll_stiffness(d) * 0.7
        K_bar = arb_K_bar(d)
        ax.axhline(K_total / 1000, color=c, linestyle="--", linewidth=1.2, alpha=0.7)
        ax.text(
            2.15,
            K_total / 1000 + 1.0,
            f"{d}mm ({K_bar/1000:.1f} kN-m/rad)",
            color=c,
            fontsize=7,
            ha="left",
            va="bottom",
        )

    ax.set_xlabel("Target body roll at 0.8 G (\u00b0)")
    ax.set_ylabel("Roll stiffness (kN-m/rad)")
    ax.set_title("ARB sizing: required stiffness vs target roll angle")
    ax.legend(
        fontsize=7, facecolor=BG, edgecolor=GRID2, labelcolor=TEXT, loc="upper right"
    )
    ax.set_xlim(2, 6)
    ax.set_ylim(20, 110)
    save(fig, "arb_sizing.png")


# ====================================================================
# 4. Motion ratio effects (MR^2 scaling)
# ====================================================================
def plot_motion_ratio():
    fig, ax = styled_fig()
    mr = np.linspace(0.5, 1.0, 200)

    wheel_rate_factor = (mr / 0.9) ** 2
    spring_comp = 1 / wheel_rate_factor

    ax.plot(
        mr,
        wheel_rate_factor,
        color=BLUE,
        linewidth=2,
        label="Wheel rate factor (vs MR = 0.9)",
    )
    ax.plot(
        mr,
        spring_comp,
        color=PINK,
        linewidth=2,
        label="Spring rate compensation needed",
    )
    ax.axvline(0.9, color=MIATA_C, linestyle="--", linewidth=1, alpha=0.5)
    ax.axvline(0.7, color=A40_C, linestyle="--", linewidth=1, alpha=0.5)
    ax.text(0.905, 0.45, "stock\nMR", color=MIATA_C, fontsize=7, alpha=0.7)
    ax.text(0.705, 0.45, "if forced\ndown", color=A40_C, fontsize=7, alpha=0.7)
    ax.axhline(1.0, color=TEXT, linestyle=":", linewidth=0.5, alpha=0.3)

    ax.set_xlabel("Motion ratio")
    ax.set_ylabel("Multiplier")
    ax.set_title("Motion ratio scaling: wheel rate and spring compensation")
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID2, labelcolor=TEXT)
    ax.set_xlim(0.5, 1.0)
    ax.set_ylim(0, 3.5)
    save(fig, "motion_ratio.png")


# ====================================================================
# 5. Ride frequency carpet
# ====================================================================
def plot_ride_frequency():
    fig, ax = styled_fig()
    ks = np.linspace(10, 50, 200)
    MR = 0.9

    colors = [BLUE, PURPLE, PINK, GOLD]
    masses = [180, 210, 240, 270]

    for mc, c in zip(masses, colors):
        kw = ks * 1000 * MR**2
        fn = 1 / (2 * np.pi) * np.sqrt(kw / mc)
        ax.plot(ks, fn, color=c, linewidth=1.8, label=f"{mc} kg corner mass")

    ax.axhspan(1.2, 1.6, color=GOLD, alpha=0.08)
    ax.axhline(1.2, color=GOLD, linestyle="--", linewidth=0.8, alpha=0.4)
    ax.axhline(1.6, color=GOLD, linestyle="--", linewidth=0.8, alpha=0.4)
    ax.text(11, 1.38, "1.2-1.6 Hz street target", color=GOLD, fontsize=7.5, alpha=0.7)

    ax.annotate(
        "A40 front ~234 kg corner\n" "18-28 N/mm \u2192 1.2-1.6 Hz",
        xy=(38, 2.15),
        fontsize=7.5,
        color=TEXT,
        alpha=0.7,
        bbox=dict(boxstyle="round,pad=0.3", fc=BG, ec=GRID2, alpha=0.9),
    )

    ax.set_xlabel("Spring rate (N/mm)")
    ax.set_ylabel("Natural frequency (Hz)")
    ax.set_title(f"Ride frequency vs spring rate  (MR = {MR})")
    ax.legend(
        fontsize=8, facecolor=BG, edgecolor=GRID2, labelcolor=TEXT, loc="upper left"
    )
    ax.set_xlim(10, 50)
    ax.set_ylim(0.5, 3.0)
    save(fig, "ride_frequency.png")


# ====================================================================
# 6. Ackermann geometry helpers and plots
#
#    All pickup points are parameterised so real values can be swapped
#    in later.  Coordinate convention (top view):
#      x = lateral (positive = driver-right)
#      y = longitudinal (positive = forward, 0 = front axle line)
# ====================================================================
WB_MIATA = 2265
WB_A40 = 2350

# Fixed Miata NA knuckle convergence angle (hardware)
THETA_KNUCKLE = np.arctan((T_MIATA / 2) / WB_MIATA)  # ~17.23 deg

# Schematic dimensions (mm) — replace with measured values when available
RACK_FWD = 100  # rack centre-line, mm ahead of front-axle line
STEER_ARM_L = 120  # steering arm length (tie-rod end to kingpin axis)
KPI_OFFSET = 50  # kingpin lateral offset inboard of wheel centre
TIRE_W_TOP = 185  # tire section width (top-view rectangle)
TIRE_L_TOP = 500  # tyre footprint-to-rim visual length (schematic)


def _ideal_inside(d_out_deg, track_mm, wb_mm):
    """Ideal Ackermann inside-wheel angle for a given outside angle."""
    d_out = np.radians(d_out_deg)
    r_outer = wb_mm / np.tan(d_out)
    r_inner = r_outer - track_mm
    return np.degrees(np.arctan(wb_mm / r_inner))


def _draw_angled_rect(
    ax, cx, cy, w, h, angle_deg, color, alpha, lw=1.5, fill_alpha=None
):
    """Draw a filled+outlined rectangle centred at (cx, cy), rotated."""
    corners = np.array(
        [
            [-w / 2, -h / 2],
            [w / 2, -h / 2],
            [w / 2, h / 2],
            [-w / 2, h / 2],
            [-w / 2, -h / 2],
        ]
    )
    rad = np.radians(angle_deg)
    rot = np.array([[np.cos(rad), -np.sin(rad)], [np.sin(rad), np.cos(rad)]])
    pts = corners @ rot.T + np.array([cx, cy])
    if fill_alpha is not None:
        from matplotlib.patches import Polygon

        ax.add_patch(
            Polygon(pts[:4], closed=True, facecolor=color, alpha=fill_alpha, zorder=2)
        )
    ax.plot(
        pts[:, 0],
        pts[:, 1],
        color=color,
        linewidth=lw,
        alpha=alpha,
        solid_capstyle="round",
        zorder=3,
    )


# ────────────────────────────────────────────────────────────────────
# 6a.  Static top-view: rack, steering arms, kingpin, tires,
#      convergence lines for Miata stock and A40 narrowed.
# ────────────────────────────────────────────────────────────────────
def plot_ackermann_topview():
    fig, ax = styled_fig(figsize=(10, 9))
    ax.set_aspect("equal")
    from matplotlib.lines import Line2D

    configs = [
        # (label, track, wb, color, alpha, lw)
        ("Miata stock", T_MIATA, WB_MIATA, MIATA_C, 0.35, 1.2),
        ("A40 narrowed", T_A40, WB_A40, A40_C, 0.9, 2.0),
    ]

    convergence_pts = {}

    for label, track, wb, color, alpha, lw in configs:
        ht = track / 2
        # Convergence distance of the *Miata knuckle* at this track
        d_conv = ht / np.tan(THETA_KNUCKLE)
        convergence_pts[label] = d_conv

        for side in [-1, 1]:
            # ── Tire rectangle (top view, 0 deg steer for static) ──
            _draw_angled_rect(
                ax,
                side * ht,
                0,
                TIRE_W_TOP,
                TIRE_L_TOP,
                0,
                color,
                alpha * 0.6,
                lw=lw * 0.6,
                fill_alpha=alpha * 0.08,
            )

            # ── Kingpin axis ──
            kp_x = side * (ht - KPI_OFFSET)
            ax.plot(
                kp_x,
                0,
                "x",
                color=color,
                markersize=7,
                markeredgewidth=lw,
                alpha=alpha,
                zorder=5,
            )

            # ── Steering arm: from kingpin FORWARD toward the rack ──
            # The convergence line runs from (0, -d_conv) through the
            # kingpin and onward forward.  The steering arm is the short
            # segment from the kingpin forward to the tie-rod ball joint.
            # Direction from convergence point to kingpin (forward):
            dx = kp_x - 0  # lateral: kingpin x
            dy = 0 - (-d_conv)  # longitudinal: 0 - (-d_conv) = +d_conv
            arm_len_norm = np.hypot(dx, dy)
            arm_end_x = kp_x + STEER_ARM_L * (dx / arm_len_norm)
            arm_end_y = 0 + STEER_ARM_L * (dy / arm_len_norm)
            ax.plot(
                [kp_x, arm_end_x],
                [0, arm_end_y],
                color=GOLD if label.startswith("A40") else color,
                linewidth=lw * 1.2,
                alpha=alpha,
                solid_capstyle="round",
                zorder=4,
            )

            # Tie-rod end dot
            ax.plot(
                arm_end_x,
                arm_end_y,
                "o",
                color=GOLD if label.startswith("A40") else color,
                markersize=4,
                alpha=alpha,
                zorder=5,
            )

            # ── Convergence line: from kingpin to convergence point ──
            ax.plot(
                [kp_x, 0],
                [0, -d_conv],
                color=GOLD if label.startswith("A40") else color,
                linewidth=lw,
                alpha=alpha * 0.7,
                linestyle="--",
            )

        # ── Front axle line ──
        ax.plot([-ht, ht], [0, 0], color=color, linewidth=lw, alpha=alpha)

        # ── Rack (horizontal bar ahead of front axle) ──
        rack_half = ht - KPI_OFFSET - 20  # rough: rack end near tie-rod end
        ax.plot(
            [-rack_half, rack_half],
            [RACK_FWD, RACK_FWD],
            color=color,
            linewidth=lw * 1.5,
            alpha=alpha * 0.7,
            solid_capstyle="round",
        )
        if label.startswith("A40"):
            ax.text(
                0,
                RACK_FWD + 25,
                "rack",
                color=color,
                fontsize=7,
                alpha=0.6,
                ha="center",
            )

        # ── Rear axle line ──
        ax.plot(
            [-ht - 80, ht + 80],
            [-wb, -wb],
            color=color,
            linewidth=lw * 0.8,
            alpha=alpha * 0.5,
        )

        # Convergence point marker
        ax.plot(
            0,
            -d_conv,
            "o",
            color=GOLD if label.startswith("A40") else color,
            markersize=7 if label.startswith("A40") else 5,
            alpha=alpha,
            zorder=5,
        )

    # ── Ideal convergence for A40 (green dotted to rear axle) ──
    ht_a = T_A40 / 2
    for side in [-1, 1]:
        kp_x_ideal = side * (ht_a - KPI_OFFSET)  # through the kingpin
        ax.plot(
            [kp_x_ideal, 0],
            [0, -WB_A40],
            color=GREEN,
            linewidth=1.2,
            alpha=0.4,
            linestyle=":",
        )
    ax.plot(0, -WB_A40, "o", color=GREEN, markersize=6, alpha=0.5, zorder=5)

    # ── Annotate the mismatch ──
    d_actual = convergence_pts["A40 narrowed"]
    gap = WB_A40 - d_actual
    ax.annotate(
        "",
        xy=(50, -WB_A40),
        xytext=(50, -d_actual),
        arrowprops=dict(arrowstyle="<->", color=TEXT, lw=1.5),
    )
    ax.text(
        70,
        -(d_actual + gap / 2),
        f"{gap:.0f} mm gap",
        color=TEXT,
        fontsize=8,
        va="center",
        alpha=0.8,
    )

    # Label convergence points
    ax.text(
        -120,
        -d_actual + 40,
        f"Knuckle converges at {d_actual:.0f} mm",
        color=GOLD,
        fontsize=7.5,
        ha="right",
        alpha=0.9,
    )
    ax.text(
        -120,
        -WB_A40 - 50,
        f"Ideal: rear axle at {WB_A40} mm",
        color=GREEN,
        fontsize=7.5,
        ha="right",
        alpha=0.7,
    )

    # Angle annotations
    angle_knuckle_deg = np.degrees(THETA_KNUCKLE)
    angle_ideal_deg = np.degrees(np.arctan(ht_a / WB_A40))
    ax.annotate(
        f"Knuckle: {angle_knuckle_deg:.1f}\u00b0 (fixed)",
        xy=(ht_a, 0),
        xytext=(ht_a + 130, -300),
        fontsize=8,
        color=GOLD,
        arrowprops=dict(arrowstyle="->", color=GOLD, lw=0.8),
    )
    ax.annotate(
        f"Ideal: {angle_ideal_deg:.1f}\u00b0",
        xy=(ht_a, 0),
        xytext=(ht_a + 130, -500),
        fontsize=8,
        color=GREEN,
        alpha=0.7,
        arrowprops=dict(arrowstyle="->", color=GREEN, lw=0.6, alpha=0.5),
    )

    # Axle labels
    ax.text(
        ht_a + 120,
        -WB_A40,
        "A40 rear axle",
        color=A40_C,
        fontsize=7.5,
        va="center",
        alpha=0.8,
    )
    ax.text(
        T_MIATA / 2 + 120,
        -WB_MIATA,
        "Miata rear axle",
        color=MIATA_C,
        fontsize=7.5,
        va="center",
        alpha=0.4,
    )

    # Centerline
    ax.axvline(0, color=TEXT, linewidth=0.5, alpha=0.15, linestyle=":")

    ax.set_xlabel("Lateral position (mm)")
    ax.set_ylabel("Longitudinal position (mm)")
    ax.set_title("Top view: rack, steering arms, and knuckle convergence")
    ax.set_xlim(-800, 1000)
    ax.set_ylim(-2600, 450)

    legend_elements = [
        Line2D(
            [0],
            [0],
            color=MIATA_C,
            linewidth=1.5,
            alpha=0.4,
            label="Miata stock (T=1405, WB=2265)",
        ),
        Line2D(
            [0], [0], color=A40_C, linewidth=2, label="A40 layout (T=1230, WB=2350)"
        ),
        Line2D([0], [0], color=GOLD, linewidth=2, label="Miata knuckle convergence"),
        Line2D(
            [0],
            [0],
            color=GREEN,
            linewidth=1.2,
            linestyle=":",
            label="Ideal A40 convergence (to rear axle)",
        ),
    ]
    ax.legend(
        handles=legend_elements,
        fontsize=7,
        facecolor=BG,
        edgecolor=GRID2,
        labelcolor=TEXT,
        loc="upper left",
    )

    save(fig, "ackermann_topview.png")


# ────────────────────────────────────────────────────────────────────
# 6b.  ICR geometry: Miata knuckle vs ideal for the A40.
#      Single panel at 35 deg outer lock — large enough that both
#      ICRs fit within the plot area while the tires remain readable.
#      The Ackermann gap is the same conceptually at any lock angle.
# ────────────────────────────────────────────────────────────────────
def plot_ackermann_turn():
    from matplotlib.lines import Line2D

    fig, ax = styled_fig(figsize=(9, 7))
    ax.set_aspect("equal")

    track = T_A40  # 1230
    wb = WB_A40  # 2350
    ht = track / 2  # 615
    d_actual_wb = ht / np.tan(THETA_KNUCKLE)  # ~1983 mm

    d_out_deg = 35
    d_out = np.radians(d_out_deg)
    d_in_ideal_deg = _ideal_inside(d_out_deg, T_A40, WB_A40)
    d_in_ideal = np.radians(d_in_ideal_deg)
    d_in_actual_deg = _ideal_inside(d_out_deg, T_A40, d_actual_wb)
    d_in_actual = np.radians(d_in_actual_deg)
    error_deg = d_in_actual_deg - d_in_ideal_deg

    # ── ICR via line-line intersection ──
    # Left turn: both wheels steer LEFT (positive CCW angle in _draw_angled_rect).
    # Wheel heading after CCW rotation θ: (-sin θ, cos θ).
    # Wheel axle (perp to heading, toward ICR on the left): (-cos θ, -sin θ).
    # Outer at (+ht,0): P(t) = (ht - t·cos(d_out),  -t·sin(d_out))
    # Inner at (-ht,0): Q(s) = (-ht - s·cos(d_in), -s·sin(d_in))
    # Solving x,y equal:
    #   t = 2·ht·sin(d_in) / sin(d_in - d_out)
    #   ICR = (ht - t·cos(d_out),  -t·sin(d_out))
    def _icr(d_in_r):
        t = 2 * ht * np.sin(d_in_r) / np.sin(d_in_r - d_out)
        return ht - t * np.cos(d_out), -t * np.sin(d_out)

    icr_i = _icr(d_in_ideal)  # ideal  ICR — should be at y ≈ -2350 (rear axle)
    icr_a = _icr(d_in_actual)  # actual ICR — should be at y ≈ -1987 (ahead)

    # ── Rear axle: bold, separate horizontal ──
    ax.axhline(-wb, color=TEXT, linewidth=2.2, alpha=0.55, zorder=3)
    ax.text(
        ht + 85,
        -wb + 42,
        f"A40 rear axle ({wb} mm)",
        fontsize=8,
        color=TEXT,
        alpha=0.65,
    )

    # ── Front axle ──
    ax.plot([-ht - 70, ht + 70], [0, 0], color=A40_C, linewidth=1.2, alpha=0.5)

    # ── Wheel rectangles ──
    _draw_angled_rect(
        ax,
        ht,
        0,
        TIRE_W_TOP,
        TIRE_L_TOP,
        d_out_deg,
        A40_C,
        0.85,
        lw=2.0,
        fill_alpha=0.10,
    )
    _draw_angled_rect(
        ax,
        -ht,
        0,
        TIRE_W_TOP,
        TIRE_L_TOP,
        d_in_ideal_deg,
        GREEN,
        0.60,
        lw=1.5,
        fill_alpha=0.07,
    )
    _draw_angled_rect(
        ax,
        -ht,
        0,
        TIRE_W_TOP,
        TIRE_L_TOP,
        d_in_actual_deg,
        GOLD,
        0.90,
        lw=2.0,
        fill_alpha=0.10,
    )

    # ── Perpendicular lines from each wheel centre toward its ICR ──
    # Both ICRs lie on the outer wheel's ray (same d_out).
    # Draw outer to the ideal (further) ICR — it passes through actual ICR too.
    ax.plot(
        [ht, icr_i[0]],
        [0, icr_i[1]],
        color=A40_C,
        linewidth=1.0,
        alpha=0.45,
        linestyle="--",
    )
    # Inner ideal → ideal ICR
    ax.plot(
        [-ht, icr_i[0]],
        [0, icr_i[1]],
        color=GREEN,
        linewidth=1.3,
        alpha=0.65,
        linestyle=":",
    )
    # Inner actual → actual ICR (hits outer ray at a different, closer point)
    ax.plot(
        [-ht, icr_a[0]],
        [0, icr_a[1]],
        color=GOLD,
        linewidth=1.6,
        alpha=0.80,
        linestyle="--",
    )

    # ── ICR dots ──
    ax.plot(*icr_i, "o", color=GREEN, markersize=10, zorder=5)
    ax.plot(*icr_a, "o", color=GOLD, markersize=10, zorder=5)

    # ── Horizontal dashed lines at each ICR y-level ──
    ax.axhline(icr_i[1], color=GREEN, linewidth=1.0, alpha=0.35, linestyle="--")
    ax.axhline(icr_a[1], color=GOLD, linewidth=1.2, alpha=0.50, linestyle="--")

    # ── ICR labels ──
    ax.text(
        icr_i[0] - 60,
        icr_i[1] - 70,
        f"Ideal ICR\n({-icr_i[1]:.0f} mm = rear axle)",
        color=GREEN,
        fontsize=7.5,
        ha="right",
        alpha=0.85,
    )
    ax.text(
        icr_a[0] - 60,
        icr_a[1] + 65,
        f"Miata knuckle ICR\n({-icr_a[1]:.0f} mm)",
        color=GOLD,
        fontsize=7.5,
        ha="right",
        alpha=0.90,
    )

    # ── Gap: actual ICR to rear axle ──
    gap_mm = abs(-wb - icr_a[1])
    arr_x = ht + 210
    ax.annotate(
        "",
        xy=(arr_x, -wb),
        xytext=(arr_x, icr_a[1]),
        arrowprops=dict(arrowstyle="<->", color=TEXT, lw=1.5, shrinkA=0, shrinkB=0),
    )
    ax.text(
        arr_x + 25,
        (-wb + icr_a[1]) / 2,
        f"{gap_mm:.0f} mm\nahead of\nrear axle",
        fontsize=8.5,
        color=TEXT,
        va="center",
        alpha=0.9,
        fontweight="bold",
    )

    # ── Info box (top-left) ──
    info = (
        f"Outer: {d_out_deg}\u00b0   Ideal inner: {d_in_ideal_deg:.1f}\u00b0\n"
        f"Actual inner: {d_in_actual_deg:.1f}\u00b0   Excess: +{error_deg:.2f}\u00b0"
    )
    ax.text(
        0.02,
        0.98,
        info,
        color=TEXT,
        fontsize=8.5,
        ha="left",
        va="top",
        transform=ax.transAxes,
        bbox=dict(boxstyle="round,pad=0.4", fc=BG, ec=GRID2, alpha=0.9),
    )

    ax.axvline(0, color=TEXT, linewidth=0.5, alpha=0.1, linestyle=":")
    ax.set_xlabel("Lateral position (mm)")
    ax.set_ylabel("Longitudinal position (mm)")
    ax.set_title(
        f"ICR at {d_out_deg}\u00b0 outer lock: Miata stock knuckle vs ideal\n"
        f"A40 +50 track (1230 mm)  x  wheelbase 2350 mm",
        fontsize=10,
    )

    ax.set_xlim(min(icr_i[0], icr_a[0]) - 280, ht + 420)
    ax.set_ylim(-wb - 160, TIRE_L_TOP / 2 + 120)

    legend_elements = [
        Line2D([0], [0], color=A40_C, linewidth=2.0, label="Outer wheel"),
        Line2D(
            [0],
            [0],
            color=GREEN,
            linewidth=1.5,
            linestyle=":",
            label=f"Ideal inner ({d_in_ideal_deg:.1f}\u00b0) — ICR on rear axle",
        ),
        Line2D(
            [0],
            [0],
            color=GOLD,
            linewidth=2.0,
            linestyle="--",
            label=f"Actual inner ({d_in_actual_deg:.1f}\u00b0) — ICR ahead",
        ),
        Line2D(
            [0],
            [0],
            color=TEXT,
            linewidth=2.2,
            alpha=0.55,
            label=f"A40 rear axle ({wb} mm)",
        ),
    ]
    ax.legend(
        handles=legend_elements,
        fontsize=7.5,
        facecolor=BG,
        edgecolor=GRID2,
        labelcolor=TEXT,
        loc="lower left",
    )

    fig.tight_layout()
    save(fig, "ackermann_turn.png")


# ────────────────────────────────────────────────────────────────────
# 6c.  Ackermann error assessment: is the stock knuckle acceptable?
#      Top: error curve with driving scenarios and turn radii.
#      Bottom: context bars comparing error to other steering variations.
# ────────────────────────────────────────────────────────────────────
def plot_ackermann():
    fig, (ax_top, ax_bot) = styled_fig(nrows=2, ncols=1, figsize=(8, 7.5))

    delta_out = np.linspace(0.5, 30, 500)

    a40_ideal = _ideal_inside(delta_out, T_A40, WB_A40)
    d_actual = (T_A40 / 2) / np.tan(THETA_KNUCKLE)
    a40_actual = _ideal_inside(delta_out, T_A40, d_actual)
    total_error = a40_actual - a40_ideal

    # ── Top panel: error curve with scenario regions ──
    # Scenario bands: colour-coded, with turn radius included in label.
    # R = WB / tan(delta_out) gives the approximate turn radius.
    scenarios = [
        (1.5, 5, "Highway\nlane change\nR > 27 m", BLUE, 0.06),
        (5, 10, "Circuit\nsweeper\nR 13-27 m", PURPLE, 0.06),
        (10, 18, "Autox\ncorner\nR 7-13 m", GREEN, 0.07),
        (18, 25, "Autox\nslalom/\nhairpin\nR 5-7 m", GOLD, 0.07),
        (25, 30, "Parking\nR < 5 m", PINK, 0.05),
    ]
    for lo, hi, label, c, a in scenarios:
        ax_top.axvspan(lo, hi, color=c, alpha=a)
        ax_top.text(
            (lo + hi) / 2,
            2.65,
            label,
            color=c,
            fontsize=6.5,
            ha="center",
            va="top",
            alpha=0.8,
            linespacing=1.15,
        )

    # Error curve
    ax_top.plot(delta_out, total_error, color=TEXT, linewidth=2.5, zorder=4)
    ax_top.fill_between(delta_out, 0, total_error, color=TEXT, alpha=0.06)

    # Tire slip angle reference line
    ax_top.axhline(4.0, color=GREEN, linestyle="--", linewidth=1, alpha=0.35)
    ax_top.text(
        0.8,
        4.15,
        "Tire slip angle at 0.8 G (~4\u00b0)",
        color=GREEN,
        fontsize=6.5,
        alpha=0.6,
    )

    # Mark key driving points on the curve with scenario context
    callouts = [
        (3, "Highway", BLUE, (0.6, 0.18)),
        (8, "Fast circuit", PURPLE, (1.0, 0.15)),
        (15, "Autox sweeper", GREEN, (-5.0, 0.25)),
        (20, "Autox slalom", GOLD, (-5.5, 0.20)),
        (25, "Tight hairpin", PINK, (-5.5, -0.35)),
    ]
    for angle, label, c, (dx, dy) in callouts:
        idx = np.argmin(np.abs(delta_out - angle))
        err = total_error[idx]
        ax_top.plot(
            angle,
            err,
            "o",
            color=c,
            markersize=6,
            zorder=5,
            markeredgecolor=TEXT,
            markeredgewidth=0.5,
        )
        ax_top.annotate(
            f"{label}\n{err:.2f}\u00b0 error",
            xy=(angle, err),
            xytext=(angle + dx, err + dy),
            fontsize=7,
            color=c,
            fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=c, lw=0.8),
            zorder=6,
        )

    ax_top.set_xlabel("Outside wheel angle (\u00b0)")
    ax_top.set_ylabel("Excess Ackermann (\u00b0)")
    ax_top.set_title(
        "Ackermann error: Miata stock knuckle (17.2\u00b0) on A40\n"
        "Track 1230 mm, wheelbase 2350 mm",
        fontsize=10,
    )
    ax_top.set_xlim(0, 30)
    ax_top.set_ylim(-0.05, 5.0)

    # Secondary x-axis: approximate turn radius
    ax_r = ax_top.secondary_xaxis(
        "top",
        functions=(
            lambda d: WB_A40 / 1000 / np.tan(np.radians(np.clip(d, 0.5, 89))),
            lambda r: np.degrees(np.arctan(WB_A40 / 1000 / np.clip(r, 0.1, 999))),
        ),
    )
    ax_r.set_xlabel("Approximate turn radius (m)", color=TEXT, fontsize=8)
    ax_r.tick_params(colors=TEXT, labelsize=8)
    r_ticks = [5, 7, 10, 15, 25, 50]
    ax_r.set_xticks(r_ticks)
    ax_r.set_xticklabels([f"{r} m" for r in r_ticks])

    # ── Bottom panel: context comparison bars ──
    # Use 20 deg (autocross slalom) as the reference point
    err_20 = total_error[np.argmin(np.abs(delta_out - 20))]
    err_15 = total_error[np.argmin(np.abs(delta_out - 15))]
    sources = [
        (f"Ackermann error\nat 15\u00b0 (autox corner)", err_15, GREEN),
        (f"Ackermann error\nat 20\u00b0 (autox slalom)", err_20, GOLD),
        ("Tire pressure\n\u00b11 psi variation", 0.3, PURPLE),
        ("Bushing compliance\nsteer (typical)", 0.7, BLUE),
        ("Driver steering\ninput noise", 0.5, MIATA_C),
        ("Tire slip angle\nat 0.8 G", 4.0, GREEN),
    ]
    labels = [s[0] for s in sources]
    values = [s[1] for s in sources]
    bcolors = [s[2] for s in sources]

    bars = ax_bot.barh(
        labels,
        values,
        color=bcolors,
        alpha=0.7,
        height=0.6,
        edgecolor=bcolors,
        linewidth=1.2,
    )
    for bar, val in zip(bars, values):
        ax_bot.text(
            val + 0.08,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.2f}\u00b0" if val < 1.0 else f"{val:.1f}\u00b0",
            color=TEXT,
            fontsize=8,
            va="center",
            alpha=0.9,
        )

    ax_bot.set_xlabel("Steering angle variation (\u00b0)")
    ax_bot.set_title(
        "Context: error at autocross lock vs other steering variations", fontsize=9
    )
    ax_bot.set_xlim(0, 5.0)
    ax_bot.invert_yaxis()

    fig.tight_layout(h_pad=2.5)
    save(fig, "ackermann.png")


# ====================================================================
# 7. ARB bar diameter vs torsional + roll stiffness (D^4)
# ====================================================================
def plot_bar_stiffness():
    fig, ax = styled_fig()
    d = np.linspace(16, 32, 200)
    K_bar = arb_K_bar(d)

    ax.plot(d, K_bar, color=BLUE, linewidth=2)
    markers = [
        (19, "stock Miata", (2.5, -800), "left"),
        (22, "sport/R", (2.5, 1200), "left"),
        (25, "aftermarket", (2.5, 1800), "left"),
    ]
    for dd, label, (dx, dy), ha in markers:
        k = arb_K_bar(dd)
        ax.plot(dd, k, "o", color=GOLD, markersize=7, zorder=5)
        ax.annotate(
            f"{dd}mm ({label})\n{k:,.0f} N-m/rad",
            xy=(dd, k),
            xytext=(dd + dx, k + dy),
            fontsize=7,
            color=TEXT,
            alpha=0.8,
            ha=ha,
            arrowprops=dict(arrowstyle="->", color=TEXT, lw=0.5),
        )

    ax2 = ax.twinx()
    ax2.set_facecolor(BG)
    ax2.tick_params(colors=TEXT, labelsize=9)
    K_roll = arb_roll_stiffness(d)
    ax2.plot(d, K_roll / 1000, color=PINK, linewidth=1.5, linestyle="--", alpha=0.7)
    ax2.set_ylabel("ARB roll stiffness (kN-m/rad)", color=PINK)
    ax2.yaxis.label.set_color(PINK)
    for spine in ax2.spines.values():
        spine.set_color(GRID2)

    ax.set_xlabel("Bar diameter (mm)")
    ax.set_ylabel("Torsional stiffness (N-m/rad)")
    ax.set_title(f"ARB stiffness vs diameter  (L_eff = {L_EFF} mm)")
    ax.set_xlim(16, 32)
    save(fig, "bar_stiffness.png")


# ====================================================================
# 8. Weight transfer: CG bands for each track width
# ====================================================================
def plot_weight_transfer():
    fig, ax = styled_fig()
    ay_range = np.linspace(0.1, 1.2, 200)
    cg_lo, cg_hi = 525, 625  # CG uncertainty band: 575 +/- 50mm

    wt_miata = M_TOTAL * ay_range * G_ACC * (H_CG_MIATA / 1000) / (T_MIATA / 1000)
    ax.plot(
        ay_range, wt_miata, color=MIATA_C, linewidth=2, label="Miata (T=1405, CG=460)"
    )

    wt_a40_lo = M_TOTAL * ay_range * G_ACC * (cg_lo / 1000) / (T_A40 / 1000)
    wt_a40_hi = M_TOTAL * ay_range * G_ACC * (cg_hi / 1000) / (T_A40 / 1000)
    ax.fill_between(
        ay_range,
        wt_a40_lo,
        wt_a40_hi,
        alpha=0.25,
        color=PINK,
        label=f"A40 T=1230, CG={cg_lo}-{cg_hi}",
    )

    wt_stock_lo = M_TOTAL * ay_range * G_ACC * (cg_lo / 1000) / (T_MIATA / 1000)
    wt_stock_hi = M_TOTAL * ay_range * G_ACC * (cg_hi / 1000) / (T_MIATA / 1000)
    ax.fill_between(
        ay_range,
        wt_stock_lo,
        wt_stock_hi,
        alpha=0.15,
        color=PURPLE,
        label=f"A40 CG at Miata track (T=1405)",
    )

    ax.axvline(0.8, color=TEXT, linestyle=":", linewidth=0.5, alpha=0.3)
    ax.text(0.82, 500, "0.8 G", color=TEXT, fontsize=7, alpha=0.5)

    ax.set_xlabel("Lateral acceleration (G)")
    ax.set_ylabel("Lateral weight transfer (N)")
    ax.set_title("Weight transfer: track width + CG height effects")
    ax.legend(
        fontsize=7.5, facecolor=BG, edgecolor=GRID2, labelcolor=TEXT, loc="upper left"
    )
    ax.set_xlim(0.1, 1.2)
    ax.set_ylim(0, 6000)
    save(fig, "weight_transfer.png")


# ====================================================================
# 9. Jacking: RC vs tire size (ride height shifts RC)
# ====================================================================
def plot_jacking():
    fig, ax = styled_fig()

    rc = np.linspace(0, 180, 400)
    half_t = T_A40 / 2
    jack_pct = rc / half_t * 100
    jack_force = M_TOTAL * AY * G_ACC * (rc / half_t)

    ax.plot(
        rc, jack_pct, color=BLUE, linewidth=2, label=f"Jacking ratio (T = {T_A40} mm)"
    )

    ax.axvspan(0, 60, color=GREEN, alpha=0.06)
    ax.axvspan(60, 120, color=GOLD, alpha=0.06)
    ax.axvspan(120, 180, color=PINK, alpha=0.06)
    ax.text(
        30,
        27,
        "low jacking\n(race / formula)",
        color=GREEN,
        fontsize=7,
        ha="center",
        alpha=0.7,
    )
    ax.text(
        90, 27, "moderate\n(sports car)", color=GOLD, fontsize=7, ha="center", alpha=0.7
    )
    ax.text(
        150,
        27,
        "high\n(production DWB)",
        color=PINK,
        fontsize=7,
        ha="center",
        alpha=0.7,
    )

    # Compute actual RC from geometry model for key configs
    stock_od = 577.0
    a40_od = 646.0
    stock_hz = SUSP["hub_z_ground"]
    delta_r = (a40_od - stock_od) / 2
    a40_hz = stock_hz + delta_r

    p_miata = _build_suspension(T_MIATA / 2)
    p_a40 = _build_suspension(T_A40 / 2)
    p_a40_tall = _build_suspension(T_A40 / 2, hub_z_ground=a40_hz, tire_od=a40_od)

    markers = [
        ("Stock Miata (1405 mm track)", p_miata["rc"][1], T_MIATA / 2, MIATA_C),
        ("A40, Miata tire", p_a40["rc"][1], half_t, BLUE),
        ("A40, A40 tire (build)", p_a40_tall["rc"][1], half_t, A40_C),
    ]
    label_positions = [(40, 24), (40, 21.5), (40, 19)]
    for (lbl, rc_val, ht_val, col), (tx, ty) in zip(markers, label_positions):
        jp = rc_val / ht_val * 100
        ax.plot(rc_val, jp, "o", color=col, markersize=8, zorder=5)
        ax.annotate(
            f"{lbl}\nRC={rc_val:.1f} mm, {jp:.1f}%",
            xy=(rc_val, jp),
            xytext=(tx, ty),
            fontsize=6.5,
            color=col,
            arrowprops=dict(arrowstyle="->", color=col, lw=0.6),
        )

    ax2 = ax.twinx()
    ax2.set_facecolor(BG)
    ax2.tick_params(colors=TEXT, labelsize=9)
    ax2.plot(rc, jack_force, color=PINK, linewidth=1.2, linestyle="--", alpha=0.5)
    ax2.set_ylabel("Jacking force at 0.8 G (N)", color=PINK)
    ax2.yaxis.label.set_color(PINK)
    for spine in ax2.spines.values():
        spine.set_color(GRID2)

    ax.set_xlabel("Roll center height (mm)")
    ax.set_ylabel("Jacking ratio (%)")
    ax.set_title(f"Jacking vs roll center height  (T = {T_A40} mm)")
    ax.legend(
        fontsize=7, facecolor=BG, edgecolor=GRID2, labelcolor=TEXT, loc="upper left"
    )
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 30)
    ax2.set_ylim(0, jack_force[-1] * 1.05)
    save(fig, "jacking.png")


# ====================================================================
# 10. Rack narrowing vs track width (replaces both tables)
# ====================================================================
def plot_rack_narrowing():
    fig, ax = styled_fig(figsize=(7, 5))

    track = np.linspace(1100, 1450, 300)
    # From data: rack_narrowing = T_MIATA - track  (linear relationship
    # derived from OO->track->narrowing table; verified at all three points)
    rack_narrowing = T_MIATA - track

    ax.plot(track, rack_narrowing, color=BLUE, linewidth=2.5)

    # Difficulty zones
    ax.axhspan(0, 152, color=GREEN, alpha=0.10)
    ax.axhspan(152, 203, color=GOLD, alpha=0.08)
    ax.axhspan(203, 254, color=PURPLE, alpha=0.08)
    ax.axhspan(254, 310, color=PINK, alpha=0.10)

    ax.text(
        1420, 76, 'Routine (<6"/152mm)', color=GREEN, fontsize=8, ha="right", alpha=0.8
    )
    ax.text(
        1420,
        177,
        'Moderate (6-8"/203mm)',
        color=GOLD,
        fontsize=8,
        ha="right",
        alpha=0.8,
    )
    ax.text(
        1420,
        228,
        'Difficult (8-10"/254mm)',
        color=PURPLE,
        fontsize=8,
        ha="right",
        alpha=0.8,
    )
    ax.text(1420, 268, 'Limit (>10")', color=PINK, fontsize=8, ha="right", alpha=0.8)

    scenarios = [
        (1180, "stock OO (1365)", PINK, (-80, 45)),
        (1205, "+25mm OO (1390)", PURPLE, (-80, 40)),
        (1230, "+50mm OO (1415)", GREEN, (50, 40)),
    ]
    for t, lbl, c, (dx, dy) in scenarios:
        n = T_MIATA - t
        ax.plot(t, n, "o", color=c, markersize=9, zorder=5)
        ax.annotate(
            f'{lbl}\n{n:.0f}mm ({n/25.4:.1f}")',
            xy=(t, n),
            xytext=(t + dx, n + dy),
            fontsize=7.5,
            color=c,
            ha="center",
            arrowprops=dict(arrowstyle="->", color=c, lw=0.7),
            bbox=dict(boxstyle="round,pad=0.2", fc=BG, ec=c, alpha=0.8),
        )

    ax.set_xlabel("Front track width (mm)")
    ax.set_ylabel("Rack narrowing required (mm)")
    ax.set_title("Miata NA rack: narrowing required vs track width")
    ax.set_xlim(1100, 1450)
    ax.set_ylim(0, 310)

    ax_in = ax.secondary_yaxis(
        "right", functions=(lambda x: x / 25.4, lambda x: x * 25.4)
    )
    ax_in.set_ylabel("Rack narrowing (inches)")
    ax_in.tick_params(colors=TEXT, labelsize=9)
    ax_in.yaxis.label.set_color(TEXT)

    save(fig, "rack_narrowing.png")


# ====================================================================
# 13. Control arm geometry reference — plan-view schematic
# ====================================================================
# Shared helper used by all 4 control-arm plots
# ── coordinate convention ──────────────────────────────────────────
#   +x = outboard (toward wheel)   +y = forward (toward nose)
# ── geometry origin ────────────────────────────────────────────────
#   BJ at (0, 0) for all plan-view plots; pivots are at (-lat, ±fa)
# ══════════════════════════════════════════════════════════════════


def _draw_arm_core(
    ax,
    inner_f,
    inner_r,
    bj,
    mounts=None,
    color=GOLD,
    label="",
    show_annotations=True,
    bushing_lengths=None,
):
    """Draw an A-arm in plan view.  inner_f/inner_r/bj are np.array([x, y]).
    BJ at origin by convention; pivots at negative x (inboard).
    bushing_lengths: (front_len, rear_len) in mm for pivot rectangles."""
    inner_f = np.array(inner_f, dtype=float)
    inner_r = np.array(inner_r, dtype=float)
    bj = np.array(bj, dtype=float)

    # Arm blades
    for ip in (inner_f, inner_r):
        ax.plot(
            [ip[0], bj[0]],
            [ip[1], bj[1]],
            color=color,
            lw=2.5,
            solid_capstyle="round",
            zorder=3,
        )

    # Cross-brace between inner pivots
    ax.plot(
        [inner_f[0], inner_r[0]],
        [inner_f[1], inner_r[1]],
        color=color,
        lw=1.5,
        linestyle="--",
        alpha=0.45,
        zorder=3,
    )

    # Inner pivot markers — rectangles representing bushing extents
    pw = SUSP["pivot_width"]  # visual lateral width for all pivots
    for ip, tag, y_off, bush_len in zip(
        (inner_f, inner_r),
        ("Front pivot", "Rear pivot"),
        (20, -28),
        (bushing_lengths or (0, 0)),
    ):
        if bush_len > 0:
            rect = plt.Rectangle(
                (ip[0] - pw / 2, ip[1] - bush_len / 2),
                pw,
                bush_len,
                edgecolor=color,
                facecolor=color,
                alpha=0.18,
                lw=1.2,
                zorder=2,
            )
            ax.add_patch(rect)
        ax.plot(*ip, "s", color=color, markersize=7, zorder=5)
        ax.text(
            ip[0],
            ip[1] + y_off,
            tag,
            fontsize=6.5,
            color=color,
            alpha=0.85,
            ha="center",
        )

    # BJ marker
    ax.plot(*bj, "o", color=color, markersize=11, zorder=5)
    ax.text(bj[0] + 6, bj[1] - 18, "BJ", fontsize=7, color=color, alpha=0.9)

    # Extra mount points
    if mounts:
        for (mx, my), mlabel in mounts:
            ax.plot(mx, my, "^", color=GREEN, markersize=8, zorder=5)
            ax.text(mx + 6, my + 12, mlabel, fontsize=6.5, color=GREEN, alpha=0.9)

    mid = (inner_f + inner_r) / 2.0
    if show_annotations:
        span = np.linalg.norm(bj - mid)
        ax.annotate(
            "",
            xy=tuple(bj),
            xytext=tuple(mid),
            arrowprops=dict(arrowstyle="<->", color=TEXT, lw=0.8, alpha=0.6),
        )
        ax.text(
            (mid[0] + bj[0]) / 2,
            (mid[1] + bj[1]) / 2 + 12,
            f"≈{span:.0f} mm",
            fontsize=7,
            color=TEXT,
            ha="center",
            alpha=0.75,
        )

    if label:
        ax.set_title(label, color=TEXT, fontsize=9, pad=7)


def _note(ax):
    """Small 'verify against donor' reminder."""
    ax.text(
        0.01,
        0.01,
        "Dimensions from technical drawings — verify against donor car before fabrication.",
        transform=ax.transAxes,
        fontsize=6,
        color=TEXT,
        alpha=0.4,
        va="bottom",
    )


# ── derive all LCA arm-local coordinates from SUSP ──────────────────────────
# BJ at origin (0, 0).  +x outboard, +y forward.
# Both pivots at x = -(T_MIATA/2 - lca_from_cl) = -374.5 mm.
# BJ is lca_bj_fa = 25 mm forward of LCA-front-pivot
#   → front pivot at y = -25, rear pivot at y = -(25 + 323.5) = -348.5.
# Coilover and ARB lie on horizontal lines (constant y) between BJ and the pivot line.
def _lca_coords():
    lca_lat = T_MIATA / 2 - SUSP["lca_from_cl"]  # 374.5 mm
    bj = np.array([0.0, 0.0])
    f = np.array([-lca_lat, -SUSP["lca_bj_fa"]], dtype=float)  # (-374.5, -25)
    r = np.array(
        [-lca_lat, -(SUSP["lca_bj_fa"] + SUSP["lca_fa_span"])], dtype=float
    )  # (-374.5, -348.5)
    # Coilover: 240mm outboard of pivot line, y = +25mm (forward of BJ)
    cov = np.array(
        [-lca_lat + SUSP["lca_coilover_perp"], SUSP["lca_coilover_fa"]]
    )  # (-134.5, +25)
    # ARB end-link: 185mm outboard of pivot line, y = +35mm
    arb = np.array(
        [-lca_lat + SUSP["lca_arb_perp"], SUSP["lca_arb_fa"]]
    )  # (-189.5, +35)
    return bj, f, r, cov, arb


def _uca_coords():
    # BJ at origin, +x outboard, +y forward.
    # UCA pivots: 324.5mm inboard of hub, +113.5 / -143.5 mm from BJ.
    bj = np.array([0.0, 0.0])
    f = np.array(
        [-SUSP["uca_hub_to_pivot"], SUSP["uca_fa_front"]], dtype=float
    )  # (-324.5, +113.5)
    r = np.array(
        [-SUSP["uca_hub_to_pivot"], -SUSP["uca_fa_rear"]], dtype=float
    )  # (-324.5, -143.5)
    return bj, f, r


# ====================================================================
# 13a. LCA plan view
# ====================================================================
def plot_lca_plan():
    """Top-down view of the Miata NA front lower control arm.

    Geometry (BJ at origin, +x outboard, +y forward):
      Both pivots: x = -(T_MIATA/2 - lca_from_cl) = -374.5 mm inboard
      Front pivot: y = -lca_bj_fa           = -25.0 mm  (rearward of BJ)
      Rear  pivot: y = -(lca_bj_fa+lca_fa_span) = -348.5 mm  (rearward of BJ)
      Fore-aft span = lca_fa_span = 323.5 mm
      Coilover: lca_coilover_perp = 240 mm outboard from pivot line.
    """
    fig, ax = styled_fig(figsize=(9, 7))

    bj, lca_f, lca_r, cov_pt, arb_pt = _lca_coords()

    _draw_arm_core(
        ax,
        lca_f,
        lca_r,
        bj,
        mounts=[
            (
                cov_pt,
                f"Coilover\n({SUSP['lca_coilover_perp']:.0f}mm out, {SUSP['lca_coilover_fa']:.0f}mm)",
            ),
            (
                arb_pt,
                f"ARB link\n({SUSP['lca_arb_perp']:.0f}mm out, {SUSP['lca_arb_fa']:.0f}mm)",
            ),
        ],
        color=GOLD,
        label="LCA — plan view (top-down)",
        show_annotations=False,
        bushing_lengths=(SUSP["lca_f_bushing"], SUSP["lca_r_bushing"]),
    )

    # ── dimension callouts ──────────────────────────────────────────
    lca_lat = abs(lca_f[0])  # 374.5 mm
    # Lateral: both pivots → BJ  (both at same inboard distance)
    y_bot = lca_r[1] - 30  # below rear pivot
    ax.annotate(
        "",
        xy=(bj[0], y_bot),
        xytext=(lca_r[0], y_bot),
        arrowprops=dict(arrowstyle="<->", color=TEXT, lw=1.0, alpha=0.7),
    )
    ax.text(
        (bj[0] + lca_r[0]) / 2,
        y_bot - 14,
        f"{lca_lat:.0f} mm  (inner pivots → BJ, lateral — both equal)",
        fontsize=7,
        color=TEXT,
        ha="center",
        alpha=0.85,
    )

    # Fore-aft: front pivot rearward of BJ (−25 mm)
    ax.annotate(
        "",
        xy=(lca_f[0] - 15, bj[1]),
        xytext=(lca_f[0] - 15, lca_f[1]),
        arrowprops=dict(arrowstyle="<->", color=TEXT, lw=0.8, alpha=0.6),
    )
    ax.text(
        lca_f[0] - 28,
        lca_f[1] / 2,
        f"−{SUSP['lca_bj_fa']:.0f} mm\nrear",
        fontsize=6.5,
        color=TEXT,
        ha="right",
        va="center",
        alpha=0.8,
    )

    # Fore-aft: rear pivot rearward of BJ (−348.5 mm)
    rear_fa_total = SUSP["lca_bj_fa"] + SUSP["lca_fa_span"]
    ax.annotate(
        "",
        xy=(lca_r[0] - 40, bj[1]),
        xytext=(lca_r[0] - 40, lca_r[1]),
        arrowprops=dict(arrowstyle="<->", color=TEXT, lw=0.8, alpha=0.6),
    )
    ax.text(
        lca_r[0] - 53,
        lca_r[1] / 2,
        f"−{rear_fa_total:.0f} mm\nrear",
        fontsize=6.5,
        color=TEXT,
        ha="right",
        va="center",
        alpha=0.8,
    )

    # Fore-aft span between pivots (= lca_fa_span = 323.5 mm)
    mid_x = lca_r[0] - 70
    ax.annotate(
        "",
        xy=(mid_x, lca_f[1]),
        xytext=(mid_x, lca_r[1]),
        arrowprops=dict(arrowstyle="<->", color=GOLD, lw=0.9, alpha=0.55),
    )
    ax.text(
        mid_x - 8,
        (lca_f[1] + lca_r[1]) / 2,
        f"{SUSP['lca_fa_span']:.0f} mm\nspan",
        fontsize=6.5,
        color=GOLD,
        ha="right",
        va="center",
        alpha=0.8,
    )

    # BJ reference lines
    ax.axhline(bj[1], color=GRID2, lw=0.9, alpha=0.55, linestyle=":")
    ax.text(
        bj[0] + 8, bj[1] + 4, "BJ (fore-aft ref)", fontsize=6, color=TEXT, alpha=0.4
    )
    ax.axvline(bj[0], color=GRID2, lw=0.6, alpha=0.3, linestyle=":")

    ax.set_xlabel("+x outboard (BJ at 0) →  (mm)")
    ax.set_ylabel("← Rear    +y forward →  (mm)")
    ax.set_aspect("equal")
    pad = 40
    all_x = [bj[0], lca_f[0], lca_r[0], cov_pt[0], arb_pt[0]]
    all_y = [bj[1] + 20, lca_f[1], lca_r[1], y_bot - 28]
    ax.set_xlim(min(all_x) - pad, max(all_x) + pad)
    ax.set_ylim(min(all_y) - pad, max(all_y) + pad)
    _note(ax)
    save(fig, "lca_plan.png")


# ====================================================================
# 13b. UCA plan view
# ====================================================================
def plot_uca_plan():
    """Top-down view of the Miata NA front upper control arm."""
    fig, ax = styled_fig(figsize=(8, 6))

    bj, uca_f, uca_r = _uca_coords()

    _draw_arm_core(
        ax,
        uca_f,
        uca_r,
        bj,
        color=BLUE,
        label="UCA — plan view (top-down)",
        show_annotations=False,
        bushing_lengths=(SUSP["uca_bushing"], SUSP["uca_bushing"]),
    )

    uca_lat = abs(uca_f[0])  # 324.5 mm
    spread = uca_f[1] - uca_r[1]  # 113.5 + 143.5 = 257 mm
    y_bot = uca_r[1] - 25

    # Lateral: pivot → BJ
    ax.annotate(
        "",
        xy=(bj[0], y_bot),
        xytext=(uca_f[0], y_bot),
        arrowprops=dict(arrowstyle="<->", color=TEXT, lw=1.0, alpha=0.7),
    )
    ax.text(
        (bj[0] + uca_f[0]) / 2,
        y_bot - 14,
        f"{uca_lat:.0f} mm  (inner pivot → BJ, lateral)",
        fontsize=7,
        color=TEXT,
        ha="center",
        alpha=0.85,
    )

    # Fore-aft offsets (relative to BJ)
    for ip, label in [
        (uca_f, f"+{uca_f[1]:.0f} mm\nfwd"),
        (uca_r, f"−{abs(uca_r[1]):.0f} mm\nrear"),
    ]:
        ax.annotate(
            "",
            xy=(ip[0] - 18, bj[1]),
            xytext=(ip[0] - 18, ip[1]),
            arrowprops=dict(arrowstyle="<->", color=TEXT, lw=0.8, alpha=0.6),
        )
        ax.text(
            ip[0] - 30,
            ip[1] / 2,
            label,
            fontsize=6.5,
            color=TEXT,
            ha="right",
            va="center",
            alpha=0.8,
        )

    # Spread
    mid_x = (uca_f[0] + uca_r[0]) / 2 + 25
    ax.annotate(
        "",
        xy=(mid_x, uca_f[1]),
        xytext=(mid_x, uca_r[1]),
        arrowprops=dict(arrowstyle="<->", color=BLUE, lw=0.9, alpha=0.55),
    )
    ax.text(
        mid_x + 8,
        (uca_f[1] + uca_r[1]) / 2,
        f"{spread:.0f} mm\nspan",
        fontsize=6.5,
        color=BLUE,
        ha="left",
        va="center",
        alpha=0.8,
    )

    ax.axhline(bj[1], color=GRID2, lw=0.9, alpha=0.55, linestyle=":")
    ax.text(bj[0] + 6, bj[1] + 4, "BJ fore-aft ref", fontsize=6, color=TEXT, alpha=0.4)
    ax.axvline(bj[0], color=GRID2, lw=0.6, alpha=0.3, linestyle=":")

    ax.set_xlabel("+x outboard (BJ at 0) →  (mm)")
    ax.set_ylabel("← Rear    +y forward →  (mm)")
    ax.set_aspect("equal")
    pad = 36
    all_x = [bj[0], uca_f[0], uca_r[0]]
    all_y = [bj[1], uca_f[1], uca_r[1], y_bot - 28]
    ax.set_xlim(min(all_x) - pad, max(all_x) + pad)
    ax.set_ylim(min(all_y) - pad, max(all_y) + pad)
    _note(ax)
    save(fig, "uca_plan.png")


# ====================================================================
# 13c. Knuckle / spindle front view
# ====================================================================
def plot_knuckle_3view():
    """Three-view knuckle/spindle schematic (front, side, plan).

    All positions relative to hub centre (hub = 0, 0, 0).
    Coordinates: lat = outboard+, fa = forward+, h = up+ (mm).
    Source: photogrammetric scan CAD model — treat as estimated.
    """
    from matplotlib.gridspec import GridSpec

    # ── knuckle geometry ───────────────────────────────────────────
    lbj_lat, lbj_fa, lbj_h = SUSP["lbj_from_hub"]
    ubj_lat, ubj_fa, ubj_h = SUSP["ubj_from_hub"]
    steer_lat, steer_fa, steer_h = SUSP["steer_from_hub"]
    # KPI calculated from actual LBJ/UBJ positions (front view: lat × h plane)
    kpi_rad = np.arctan2(abs(ubj_lat - lbj_lat), ubj_h - lbj_h)
    kpi_deg = np.degrees(kpi_rad)
    # Caster calculated from actual LBJ/UBJ fore-aft offset (side view: fa × h plane)
    caster_rad = np.arctan2(abs(ubj_fa - lbj_fa), ubj_h - lbj_h)
    caster_deg = np.degrees(caster_rad)
    span = ubj_h - lbj_h  # total BJ vertical span ≈233mm
    HUB_R = 38  # hub bearing circle display radius (mm)

    # ── axis limits ────────────────────────────────────────────────
    # Computed to clear: hub rect/circle + HUB_R=38, all BJ/steer points,
    # span arrows, height labels, KPI arc text, dimension annotations.
    lat_min, lat_max = -185, 110  # span = 295
    fa_min, fa_max = -55, 140  # span = 195 (was -35 — clipped hub at -38)
    h_min, h_max = -140, 185  # span = 325
    lat_span = lat_max - lat_min
    fa_span = fa_max - fa_min
    h_span = h_max - h_min

    # ── figure layout: 2×2, plan view spans both columns ────────────────
    # Height ratios derived so all three panels are equal-aspect.
    h1 = fa_span * (lat_span + fa_span) / lat_span
    FIG_W = 9.0
    fig_h = FIG_W * (h_span / (lat_span + fa_span) + fa_span / lat_span)
    fig_h = max(fig_h, 10.0)

    fig = plt.figure(figsize=(FIG_W, fig_h), facecolor=BG)
    gs = GridSpec(
        2,
        2,
        figure=fig,
        height_ratios=[h_span, h1],
        width_ratios=[lat_span, fa_span],
        hspace=0.50,
        wspace=0.44,
    )
    ax_frt = fig.add_subplot(gs[0, 0])
    ax_sid = fig.add_subplot(gs[0, 1])
    ax_plan = fig.add_subplot(gs[1, :])

    for ax in (ax_frt, ax_sid, ax_plan):
        ax.set_facecolor(BG)
        ax.tick_params(colors=TEXT, labelsize=8)
        ax.xaxis.label.set_color(TEXT)
        ax.yaxis.label.set_color(TEXT)
        ax.title.set_color(TEXT)
        for spine in ax.spines.values():
            spine.set_color(GRID2)
        ax.grid(True, color=GRID, linewidth=0.5, alpha=0.6)

    def hub_circle(ax, cx, cy):
        ax.add_patch(
            plt.Circle(
                (cx, cy), HUB_R, color=TEXT, fill=False, lw=1.5, alpha=0.28, zorder=3
            )
        )
        ax.plot(cx, cy, "+", color=TEXT, ms=10, mew=1.5, alpha=0.45, zorder=4)

    def hub_rect(ax, cx, cy, w, h):
        """Edge-on hub outline as a rectangle centred on (cx, cy).

        w = full extent along x-axis of this panel.
        h = full extent along y-axis of this panel.
        Side view (fa × height): w=barrel_depth, h=diameter.
        Plan view (lat × fa):    w=diameter,      h=barrel_depth.
        """
        rect = plt.Rectangle(
            (cx - w / 2, cy - h / 2),
            w,
            h,
            edgecolor=TEXT,
            facecolor="none",
            lw=1.5,
            alpha=0.28,
            zorder=3,
        )
        ax.add_patch(rect)
        ax.plot(cx, cy, "+", color=TEXT, ms=10, mew=1.5, alpha=0.45, zorder=4)

    def arr_v(ax, x, y0, y1, label, color=TEXT, xoff=10, ha="left"):
        """Vertical dimension arrow with side label."""
        ax.annotate(
            "",
            xy=(x, y1),
            xytext=(x, y0),
            arrowprops=dict(arrowstyle="<->", color=color, lw=0.9, alpha=0.75),
        )
        ax.text(
            x + xoff,
            (y0 + y1) / 2,
            label,
            fontsize=7,
            color=color,
            ha=ha,
            va="center",
            alpha=0.9,
        )

    def arr_h(ax, x0, x1, y, label, color=TEXT, yoff=8, ha="center"):
        """Horizontal dimension arrow with label above/below."""
        ax.annotate(
            "",
            xy=(x1, y),
            xytext=(x0, y),
            arrowprops=dict(arrowstyle="<->", color=color, lw=0.9, alpha=0.75),
        )
        ax.text(
            (x0 + x1) / 2,
            y + yoff,
            label,
            fontsize=7,
            color=color,
            ha=ha,
            va="bottom" if yoff > 0 else "top",
            alpha=0.9,
        )

    # ═══════════════════════════════════════
    # FRONT VIEW  (lat × h)
    # ═══════════════════════════════════════
    # Faint cross-view guides at key heights and laterals
    for h_val, col in [(lbj_h, GOLD), (ubj_h, BLUE), (steer_h, GREEN)]:
        ax_frt.axhline(h_val, color=col, lw=0.8, ls=":", alpha=0.22)
    for lat_val, col in [(lbj_lat, GOLD), (ubj_lat, BLUE), (steer_lat, GREEN)]:
        ax_frt.axvline(lat_val, color=col, lw=0.7, ls=":", alpha=0.18)

    hub_rect(
        ax_frt, 0, 0, w=28, h=HUB_R * 2
    )  # barrel edge: narrow in lat, tall as diameter
    ax_frt.axhline(0, color=TEXT, lw=0.7, alpha=0.22)
    ax_frt.axvline(0, color=TEXT, lw=0.7, alpha=0.22)

    ax_frt.plot(
        [lbj_lat, ubj_lat],
        [lbj_h, ubj_h],
        color=PINK,
        lw=2.5,
        solid_capstyle="round",
        zorder=3,
        label=f"Kingpin axis  KPI {kpi_deg:.1f}°",
    )
    ax_frt.plot(lbj_lat, lbj_h, "o", color=GOLD, ms=10, zorder=5, label="LBJ")
    ax_frt.plot(ubj_lat, ubj_h, "o", color=BLUE, ms=10, zorder=5, label="UBJ")
    ax_frt.plot(
        steer_lat, steer_h, "D", color=GREEN, ms=9, zorder=5, label="Steering arm"
    )

    # ── KPI angle annotation ──
    # Vertical reference line from LBJ upward — shows what 0° would look like
    arc_r = 60
    ax_frt.plot(
        [lbj_lat, lbj_lat],
        [lbj_h, lbj_h + arc_r + 10],
        color=TEXT,
        lw=0.9,
        ls="--",
        alpha=0.35,
        zorder=2,
    )
    # Filled wedge between vertical and kingpin axis
    theta_base = np.pi / 2  # straight up
    theta_kpi = np.pi / 2 + kpi_rad  # kingpin direction (inboard lean)
    theta_fill = np.linspace(theta_base, theta_kpi, 60)
    fill_x = lbj_lat + arc_r * np.cos(theta_fill)
    fill_y = lbj_h + arc_r * np.sin(theta_fill)
    ax_frt.fill(
        np.concatenate([[lbj_lat], fill_x, [lbj_lat]]),
        np.concatenate([[lbj_h], fill_y, [lbj_h]]),
        color=PINK,
        alpha=0.12,
        zorder=2,
    )
    # Arc outline
    ax_frt.plot(fill_x, fill_y, color=PINK, lw=1.6, alpha=0.85, zorder=4)
    # Angle label inside arc with background box
    mid_theta = (theta_base + theta_kpi) / 2
    label_r = arc_r + 18
    ax_frt.text(
        lbj_lat + label_r * np.cos(mid_theta),
        lbj_h + label_r * np.sin(mid_theta),
        f"KPI\n{kpi_deg:.1f}°",
        fontsize=8.5,
        color=PINK,
        fontweight="bold",
        ha="right",
        va="bottom",
        bbox=dict(boxstyle="round,pad=0.25", fc=BG, ec=PINK, alpha=0.85, lw=0.8),
    )

    # Height labels on right side — push further right so they don't crowd the span arrow
    lbl_lat = 55
    for h_val, lbl, col in [
        (ubj_h, f"UBJ  {ubj_h:+.1f} mm", BLUE),
        (0, "Hub CL  0 (ref)", TEXT),
        (steer_h, f"Steer {steer_h:+.1f} mm", GREEN),
        (lbj_h, f"LBJ  {lbj_h:+.1f} mm", GOLD),
    ]:
        ax_frt.axhline(h_val, color=col, lw=0.5, ls=":", alpha=0.18)
        ax_frt.text(
            lbl_lat, h_val + 4, lbl, fontsize=7, color=col, alpha=0.82, va="bottom"
        )

    # KPI lateral spread dim (at bottom)
    arr_h(
        ax_frt,
        ubj_lat,
        lbj_lat,
        h_min + 22,
        f"{abs(ubj_lat - lbj_lat):.1f} mm lateral",
        PINK,
        yoff=10,
    )
    # Span dim (left of the kingpin line)
    arr_v(
        ax_frt,
        ubj_lat - 20,
        lbj_h,
        ubj_h,
        f"{span:.1f} mm span",
        PINK,
        xoff=-4,
        ha="right",
    )

    ax_frt.set_xlim(lat_min, lat_max)
    ax_frt.set_ylim(h_min, h_max)
    ax_frt.set_aspect("equal", adjustable="box")
    ax_frt.set_xlabel("Lateral from hub CL (mm, outboard = +)", fontsize=8)
    ax_frt.set_ylabel("Height from hub CL (mm, up = +)", fontsize=8)
    ax_frt.set_title("Front view", color=TEXT, fontsize=9, pad=6)
    ax_frt.legend(
        fontsize=7, facecolor=BG, edgecolor=GRID2, labelcolor=TEXT, loc="lower right"
    )

    # ═══════════════════════════════════════
    # SIDE VIEW  (fa × h) — shares h axis with front view
    # ═══════════════════════════════════════
    for h_val, col in [(lbj_h, GOLD), (ubj_h, BLUE), (steer_h, GREEN)]:
        ax_sid.axhline(h_val, color=col, lw=0.8, ls=":", alpha=0.22)
    for fa_val, col in [(lbj_fa, GOLD), (steer_fa, GREEN)]:
        ax_sid.axvline(fa_val, color=col, lw=0.7, ls=":", alpha=0.18)

    hub_circle(ax_sid, 0, 0)  # face-on: looking along lateral axis at hub bearing face
    ax_sid.axhline(0, color=TEXT, lw=0.7, alpha=0.22)
    ax_sid.axvline(0, color=TEXT, lw=0.7, alpha=0.22)

    # Kingpin in side view: LBJ and UBJ share same fa → vertical line
    ax_sid.plot(
        [lbj_fa, ubj_fa],
        [lbj_h, ubj_h],
        color=PINK,
        lw=2.5,
        solid_capstyle="round",
        zorder=3,
    )
    ax_sid.plot(lbj_fa, lbj_h, "o", color=GOLD, ms=10, zorder=5)
    ax_sid.plot(ubj_fa, ubj_h, "o", color=BLUE, ms=10, zorder=5)
    ax_sid.plot(steer_fa, steer_h, "D", color=GREEN, ms=9, zorder=5)

    # ── Caster angle (= offset of kingpin axis from vertical in fa×h plane) ──
    # LBJ and UBJ share the same fa in this scan, so caster from knuckle ≈ 0°.
    # Draw the arc regardless to make this explicit.
    arc_r_cas = 55
    vertical_ref_y1 = lbj_h + arc_r_cas + 10
    ax_sid.plot(
        [lbj_fa, lbj_fa],
        [lbj_h, vertical_ref_y1],
        color=TEXT,
        lw=0.9,
        ls="--",
        alpha=0.35,
        zorder=2,
    )
    theta_cas_base = np.pi / 2
    # Direction: UBJ is rearward (more negative fa) → clockwise from vertical
    cas_sign = 1 if (ubj_fa - lbj_fa) >= 0 else -1
    theta_cas_kpi = theta_cas_base - cas_sign * caster_rad
    theta_cas_arr = np.linspace(theta_cas_base, theta_cas_kpi, 40)
    cas_arc_x = lbj_fa + arc_r_cas * np.cos(theta_cas_arr)
    cas_arc_y = lbj_h + arc_r_cas * np.sin(theta_cas_arr)
    ax_sid.fill(
        np.concatenate([[lbj_fa], cas_arc_x, [lbj_fa]]),
        np.concatenate([[lbj_h], cas_arc_y, [lbj_h]]),
        color=PINK,
        alpha=0.10,
        zorder=2,
    )
    ax_sid.plot(cas_arc_x, cas_arc_y, color=PINK, lw=1.6, alpha=0.8, zorder=4)
    mid_cas = (theta_cas_base + theta_cas_kpi) / 2
    label_r_cas = arc_r_cas + 16
    ax_sid.text(
        lbj_fa + label_r_cas * np.cos(mid_cas),
        lbj_h + label_r_cas * np.sin(mid_cas),
        f"Caster\n{caster_deg:.1f}°",
        fontsize=8.5,
        color=PINK,
        fontweight="bold",
        ha="left",
        va="bottom",
        bbox=dict(boxstyle="round,pad=0.25", fc=BG, ec=PINK, alpha=0.85, lw=0.8),
    )

    # Span label beside kingpin
    arr_v(ax_sid, lbj_fa + 18, lbj_h, ubj_h, f"{span:.1f} mm", PINK)
    # Steer arm forward reach
    arr_h(ax_sid, 0, steer_fa, steer_h - 22, f"{steer_fa:.1f} mm fwd", GREEN, yoff=-13)
    # Steer arm height label
    ax_sid.text(
        steer_fa + 5,
        steer_h + 4,
        f"{steer_h:+.1f} mm",
        fontsize=7,
        color=GREEN,
        alpha=0.82,
    )

    # Note: LBJ and UBJ share the same fore-aft position → caster is set
    # by the inner pickup geometry, not the knuckle casting.
    ax_sid.text(
        0.02,
        0.98,
        f"BJ fa offset: {lbj_fa:.1f} mm (both)",
        fontsize=6.5,
        color=TEXT,
        alpha=0.5,
        transform=ax_sid.transAxes,
        va="top",
        ha="left",
    )

    ax_sid.set_xlim(fa_min, fa_max)
    ax_sid.set_ylim(h_min, h_max)
    ax_sid.set_aspect("equal", adjustable="box")
    ax_sid.set_xlabel("Fore-aft from hub CL (mm, fwd = +)", fontsize=8)
    ax_sid.set_ylabel("Height from hub CL (mm, up = +)", fontsize=8)
    ax_sid.set_title("Side view (outboard)", color=TEXT, fontsize=9, pad=6)

    # ═══════════════════════════════════════
    # PLAN VIEW  (lat × fa) — shares lat axis with front, fa axis with side
    # ═══════════════════════════════════════
    for fa_val, col in [(lbj_fa, GOLD), (steer_fa, GREEN)]:
        ax_plan.axhline(fa_val, color=col, lw=0.8, ls=":", alpha=0.22)
    for lat_val, col in [(lbj_lat, GOLD), (ubj_lat, BLUE), (steer_lat, GREEN)]:
        ax_plan.axvline(lat_val, color=col, lw=0.7, ls=":", alpha=0.18)

    hub_rect(
        ax_plan, 0, 0, w=28, h=HUB_R * 2
    )  # barrel top: narrow in lat, wide as diameter in fa
    ax_plan.axhline(0, color=TEXT, lw=0.7, alpha=0.22)
    ax_plan.axvline(0, color=TEXT, lw=0.7, alpha=0.22)

    ax_plan.plot(lbj_lat, lbj_fa, "o", color=GOLD, ms=10, zorder=5, label="LBJ")
    ax_plan.plot(ubj_lat, ubj_fa, "o", color=BLUE, ms=10, zorder=5, label="UBJ")
    ax_plan.plot(
        steer_lat, steer_fa, "D", color=GREEN, ms=9, zorder=5, label="Steer arm"
    )
    # KPI line in plan — shows lateral spread between LBJ and UBJ from above
    ax_plan.plot(
        [lbj_lat, ubj_lat],
        [lbj_fa, ubj_fa],
        color=PINK,
        lw=2.5,
        solid_capstyle="round",
        zorder=3,
        label="Kingpin axis",
    )

    # LBJ lateral from hub
    arr_h(
        ax_plan, lbj_lat, 0, lbj_fa + 16, f"{abs(lbj_lat):.1f} mm inboard", GOLD, yoff=9
    )
    # UBJ additional inboard vs LBJ
    arr_h(
        ax_plan,
        ubj_lat,
        lbj_lat,
        ubj_fa - 14,
        f"{abs(ubj_lat - lbj_lat):.1f} mm more",
        PINK,
        yoff=-13,
    )
    # Steer arm forward reach
    arr_v(
        ax_plan,
        steer_lat - 22,
        0,
        steer_fa,
        f"{steer_fa:.1f} mm fwd",
        GREEN,
        xoff=-4,
        ha="right",
    )

    # Point labels
    for lat, fa, lbl, col, ha in [
        (lbj_lat, lbj_fa, f"LBJ ({lbj_lat:.1f}, {lbj_fa:.1f})", GOLD, "left"),
        (ubj_lat, ubj_fa, f"UBJ ({ubj_lat:.1f}, {ubj_fa:.1f})", BLUE, "left"),
        (
            steer_lat,
            steer_fa,
            f"Steer ({steer_lat:.1f}, {steer_fa:.1f})",
            GREEN,
            "right",
        ),
    ]:
        xoff = 7 if ha == "left" else -7
        ax_plan.text(
            lat + xoff,
            fa + 5,
            lbl,
            fontsize=7,
            color=col,
            ha=ha,
            va="bottom",
            alpha=0.85,
        )

    ax_plan.set_xlim(lat_min, lat_max)
    ax_plan.set_ylim(fa_min, fa_max)
    ax_plan.set_aspect("equal", adjustable="box")
    ax_plan.set_xlabel("Lateral from hub CL (mm, outboard = +)", fontsize=8)
    ax_plan.set_ylabel("Fore-aft from hub CL (mm, fwd = +)", fontsize=8)
    ax_plan.set_title("Plan view (top-down)", color=TEXT, fontsize=9, pad=6)
    ax_plan.legend(
        fontsize=7.5, facecolor=BG, edgecolor=GRID2, labelcolor=TEXT, loc="upper right"
    )

    fig.suptitle(
        "Miata NA front knuckle / spindle — 3-view schematic\n"
        "All positions relative to hub centre (0, 0, 0)  |  "
        "CAD scan estimate — not yet verified against donor",
        color=TEXT,
        fontsize=8.5,
        y=1.01,
    )
    _note(ax_plan)
    save(fig, "knuckle_3view.png")


# ====================================================================
# 13d. Pickup point — 3-view schematic (front / plan / side)
# ====================================================================
def plot_pickups_3view():
    """Three-view schematic of confirmed inner pivot pickup positions.

    Both sides of the car are shown in the front and plan views.
    Panels are stacked vertically: front view / plan view / side view.
    Lateral from car CL is on the bottom (X) axis for both front and plan views.

    Reference frame:
      Lateral:  from car CL (+right / outboard).
      Fore-aft: from LCA front pivot (+forward, −rearward).
      Height:   from LCA pivot height (+up).
    """
    from matplotlib.gridspec import GridSpec
    from matplotlib.lines import Line2D

    # ── confirmed pivot coordinates ──────────────────────────────────
    g = susp_geometry()
    LCA_lat = g["lca_f"][0]  # 328 mm from car CL
    UCA_lat = g["uca_f"][0]  # 378.0 mm from car CL
    LCAF_fa = g["lca_f"][1]
    LCAF_z = g["lca_f"][2]  # 0, 0
    LCAR_fa = g["lca_r"][1]
    LCAR_z = g["lca_r"][2]  # −323.5, 0
    UCAF_fa = g["uca_f"][1]
    UCAF_z = g["uca_f"][2]  # +138.5, +192
    UCAR_fa = g["uca_r"][1]
    UCAR_z = g["uca_r"][2]  # −118.5, +170
    HT_MIATA = g["half_track"]  # 702.5 mm

    # ── axis ranges ──────────────────────────────────────────────────
    lat_pad = 130
    lat_lim = UCA_lat + lat_pad
    fa_min, fa_max = LCAR_fa - 80, UCAF_fa + 140
    z_min, z_max = -80, 290

    # ── figure sizing — equal aspect requires height ratios to match data extents ──
    # X span for front/plan panels: 2 * lat_lim
    # Y span for front:  z_max - z_min
    # Y span for plan:   fa_max - fa_min
    # X span for side:   fa_max - fa_min  (same as plan Y)
    # Y span for side:   z_max - z_min    (same as front Y)
    # All panels have the same allocated figure width (GridSpec 1 col).
    # To minimise whitespace, allocated height ∝ data-Y / data-X × panel-width.
    # panel-width is equal for all; data-X for front/plan = 2*lat_lim,
    # for side = fa_max - fa_min.
    lat_span = 2 * lat_lim
    fa_span = fa_max - fa_min
    z_span = z_max - z_min
    hr_front = z_span / lat_span  # front: z over lateral
    hr_plan = fa_span / lat_span  # plan:  fa  over lateral
    hr_side = z_span / fa_span  # side:  z   over fa (narrower X span)
    # side panel's effective height in the figure = hr_side × (fa_span/lat_span)
    # because its content only fills fa_span/lat_span of the width
    hr_side_fig = z_span / lat_span  # same physics — z and lateral share denominator
    FIG_W = 16.0
    MARGIN = 0.82  # fraction of figure height used by axes (rest = margins/labels)
    fig_h = (hr_front + hr_plan + hr_side_fig) * FIG_W * MARGIN
    fig_h = max(fig_h, 14.0)  # floor so labels don't get crushed

    fig = plt.figure(figsize=(FIG_W, fig_h), facecolor=BG)
    gs = GridSpec(
        3, 1, figure=fig, height_ratios=[hr_front, hr_plan, hr_side_fig], hspace=0.55
    )
    ax_front = fig.add_subplot(gs[0])
    ax_plan = fig.add_subplot(gs[1])
    ax_side = fig.add_subplot(gs[2])

    for ax in (ax_front, ax_plan, ax_side):
        ax.set_facecolor(BG)
        ax.tick_params(colors=TEXT, labelsize=8)
        ax.xaxis.label.set_color(TEXT)
        ax.yaxis.label.set_color(TEXT)
        ax.title.set_color(TEXT)
        for spine in ax.spines.values():
            spine.set_color(GRID2)
        ax.grid(True, color=GRID, linewidth=0.5, alpha=0.6)

    def dim(ax, p1, p2, label, color=TEXT, xoff=0, yoff=7, ha="center"):
        ax.annotate(
            "",
            xy=p2,
            xytext=p1,
            arrowprops=dict(arrowstyle="<->", color=color, lw=0.9, alpha=0.75),
        )
        mid = ((p1[0] + p2[0]) / 2 + xoff, (p1[1] + p2[1]) / 2 + yoff)
        ax.text(*mid, label, fontsize=6.5, color=color, ha=ha, va="bottom", alpha=0.9)

    legend_handles = [
        Line2D(
            [0],
            [0],
            color=GOLD,
            lw=2.5,
            marker="s",
            markersize=7,
            label="LCA inner pivots",
        ),
        Line2D(
            [0],
            [0],
            color=BLUE,
            lw=2.5,
            marker="^",
            markersize=7,
            label="UCA inner pivots",
        ),
    ]

    # ═══════════════════════════════════════════════════════════════════
    # TOP: Front view — both sides
    # X = lateral from car CL (+right / outboard),  Y = height from LCA pivot
    # ═══════════════════════════════════════════════════════════════════
    # Faint horizontal guide lines connecting matching left/right pivots
    ax_front.axhline(UCAF_z, color=BLUE, lw=0.9, ls=":", alpha=0.25, zorder=1)
    ax_front.axhline(UCAR_z, color=BLUE, lw=0.9, ls=":", alpha=0.25, zorder=1)

    pw = SUSP["pivot_width"]
    rpw = 26  # display width for pivot rectangles (wider than physical pw)

    for side in (+1, -1):
        lca_x = side * LCA_lat
        uca_x = side * UCA_lat

        # Pivot bushing rectangles (front view: rpw × rpw squares)
        for px, pz, col in [
            (lca_x, LCAF_z, GOLD),
            (uca_x, UCAF_z, BLUE),
            (uca_x, UCAR_z, BLUE),
        ]:
            rect = plt.Rectangle(
                (px - rpw / 2, pz - rpw / 2),
                rpw,
                rpw,
                edgecolor=col,
                facecolor=col,
                alpha=0.22,
                lw=1.2,
                zorder=2,
            )
            ax_front.add_patch(rect)

        ax_front.plot(lca_x, LCAF_z, "s", color=GOLD, markersize=10, zorder=5)
        ax_front.plot(uca_x, UCAF_z, "^", color=BLUE, markersize=9, zorder=5)
        ax_front.plot(uca_x, UCAR_z, "^", color=BLUE, markersize=9, zorder=5)
        ax_front.axvline(lca_x, color=GOLD, lw=0.4, alpha=0.18, linestyle=":")
        ax_front.axvline(uca_x, color=BLUE, lw=0.4, alpha=0.18, linestyle=":")

        if side == 1:
            ax_front.text(
                lca_x - 10,
                LCAF_z - 24,
                f"LCA ±{LCA_lat:.1f}mm",
                fontsize=6.5,
                color=GOLD,
                ha="right",
            )
            ax_front.text(
                uca_x + 10,
                UCAF_z + 16,
                f"UCA-F +{UCAF_z:.1f}mm",
                fontsize=6.5,
                color=BLUE,
            )
            ax_front.text(
                uca_x + 10,
                UCAR_z - 28,
                f"UCA-R +{UCAR_z:.1f}mm",
                fontsize=6.5,
                color=BLUE,
            )
            dim(
                ax_front,
                (lca_x, z_min + 18),
                (uca_x, z_min + 18),
                f"{UCA_lat - LCA_lat:.1f}mm",
                TEXT,
                yoff=10,
                ha="center",
            )
            dim(
                ax_front,
                (uca_x + 30, 0),
                (uca_x + 30, UCAF_z),
                f"+{UCAF_z:.1f}mm",
                BLUE,
                ha="left",
            )

    ax_front.axvline(0, color=GRID2, lw=1.0, alpha=0.55, linestyle="--")
    ax_front.text(2, z_max - 20, "Car CL", fontsize=6.5, color=GRID2, alpha=0.7)
    ax_front.axhline(0, color=GOLD, lw=0.5, alpha=0.3, linestyle=":")
    ax_front.text(
        -lat_lim + 4, 4, "LCA pivot height (ref)", fontsize=5.5, color=GOLD, alpha=0.5
    )
    ax_front.set_xlim(-lat_lim, lat_lim)
    ax_front.set_ylim(z_min, z_max)
    ax_front.set_aspect("equal", adjustable="box")
    ax_front.set_xlabel(
        "← left side car          Lateral from car CL (mm)          right side car →"
    )
    ax_front.set_ylabel("Height from LCA pivot (mm)")
    ax_front.set_title("Front view — both sides", color=TEXT, fontsize=9, pad=6)
    ax_front.legend(
        handles=legend_handles,
        fontsize=7,
        facecolor=BG,
        edgecolor=GRID2,
        labelcolor=TEXT,
        loc="upper center",
        ncol=2,
        bbox_to_anchor=(0.5, 0.98),
    )

    # ═══════════════════════════════════════════════════════════════════
    # MIDDLE: Plan view — both sides
    # X = lateral from car CL (+right / outboard),  Y = fore-aft from LCA-front pivot (+fwd)
    # ═══════════════════════════════════════════════════════════════════
    ax_plan.axhline(LCAR_fa, color=GOLD, lw=0.9, ls=":", alpha=0.25, zorder=1)
    ax_plan.axhline(UCAF_fa, color=BLUE, lw=0.9, ls=":", alpha=0.25, zorder=1)
    ax_plan.axhline(UCAR_fa, color=BLUE, lw=0.9, ls=":", alpha=0.25, zorder=1)

    for side in (+1, -1):
        lca_x = side * LCA_lat
        uca_x = side * UCA_lat

        # Pivot bushing rectangles (plan view: rpw lateral × bushing fore-aft)
        for px, py, bush, col in [
            (lca_x, LCAF_fa, SUSP["lca_f_bushing"], GOLD),
            (lca_x, LCAR_fa, SUSP["lca_r_bushing"], GOLD),
            (uca_x, UCAF_fa, SUSP["uca_bushing"], BLUE),
            (uca_x, UCAR_fa, SUSP["uca_bushing"], BLUE),
        ]:
            rect = plt.Rectangle(
                (px - rpw / 2, py - bush / 2),
                rpw,
                bush,
                edgecolor=col,
                facecolor=col,
                alpha=0.22,
                lw=1.2,
                zorder=2,
            )
            ax_plan.add_patch(rect)

        # LCA arm line
        ax_plan.plot(
            [lca_x, lca_x],
            [LCAF_fa, LCAR_fa],
            color=GOLD,
            lw=2.5,
            solid_capstyle="round",
            zorder=3,
        )
        ax_plan.plot(lca_x, LCAF_fa, "s", color=GOLD, markersize=9, zorder=5)
        ax_plan.plot(lca_x, LCAR_fa, "s", color=GOLD, markersize=9, zorder=5)

        # UCA arm line
        ax_plan.plot(
            [uca_x, uca_x],
            [UCAF_fa, UCAR_fa],
            color=BLUE,
            lw=2.5,
            solid_capstyle="round",
            zorder=3,
        )
        ax_plan.plot(uca_x, UCAF_fa, "^", color=BLUE, markersize=9, zorder=5)
        ax_plan.plot(uca_x, UCAR_fa, "^", color=BLUE, markersize=9, zorder=5)

        ax_plan.axvline(lca_x, color=GOLD, lw=0.4, alpha=0.18, linestyle=":")
        ax_plan.axvline(uca_x, color=BLUE, lw=0.4, alpha=0.18, linestyle=":")

        if side == 1:
            # LCA labels: inboard (left) of arm so they don't collide with UCA labels
            ax_plan.text(
                lca_x - 10,
                LCAF_fa + 14,
                f"LCA-front ({lca_x:.1f}, 0)",
                fontsize=6.5,
                color=GOLD,
                ha="right",
            )
            ax_plan.text(
                lca_x - 10,
                LCAR_fa - 22,
                f"LCA-rear ({lca_x:.1f}, {LCAR_fa:.1f})",
                fontsize=6.5,
                color=GOLD,
                ha="right",
            )
            # UCA labels: outboard (right) of arm
            ax_plan.text(
                uca_x + 10,
                UCAF_fa + 14,
                f"UCA-F ({uca_x:.1f}, +{UCAF_fa:.1f})",
                fontsize=6.5,
                color=BLUE,
            )
            ax_plan.text(
                uca_x + 10,
                UCAR_fa - 22,
                f"UCA-R ({uca_x:.1f}, {UCAR_fa:.1f})",
                fontsize=6.5,
                color=BLUE,
            )
            # LCA fore-aft span dim: left of LCA column
            dim(
                ax_plan,
                (lca_x - 35, LCAF_fa),
                (lca_x - 35, LCAR_fa),
                f"{abs(LCAR_fa):.1f}mm",
                GOLD,
                xoff=0,
                yoff=0,
                ha="right",
            )
            # UCA fore-aft span dim: right of UCA column
            dim(
                ax_plan,
                (uca_x + 35, UCAF_fa),
                (uca_x + 35, UCAR_fa),
                f"{UCAF_fa - UCAR_fa:.1f}mm",
                BLUE,
                xoff=0,
                yoff=0,
                ha="left",
            )
            # LCA→UCA lateral dim at bottom
            dim(
                ax_plan,
                (lca_x, fa_min + 20),
                (uca_x, fa_min + 20),
                f"{UCA_lat - LCA_lat:.1f}mm",
                TEXT,
                yoff=10,
                ha="center",
            )

    ax_plan.axhline(0, color=GOLD, lw=0.5, alpha=0.3, linestyle=":")
    ax_plan.text(
        -lat_lim + 4, 5, "LCA-front pivot (FA ref)", fontsize=5.5, color=GOLD, alpha=0.5
    )
    ax_plan.axvline(0, color=GRID2, lw=1.0, alpha=0.55, linestyle="--")
    ax_plan.text(4, fa_max - 14, "Car CL", fontsize=6.5, color=GRID2, alpha=0.7)
    ax_plan.set_xlim(-lat_lim, lat_lim)
    ax_plan.set_ylim(fa_min, fa_max)
    ax_plan.set_aspect("equal", adjustable="box")
    ax_plan.set_xlabel(
        "← left side car          Lateral from car CL (mm)          right side car →"
    )
    ax_plan.set_ylabel(
        "← back          Fore-aft from LCA-front pivot (mm)          front →"
    )
    ax_plan.set_title(
        "Plan view (top-down) — both sides", color=TEXT, fontsize=9, pad=6
    )

    # ═══════════════════════════════════════════════════════════════════
    # BOTTOM: Side view — single side (fore-aft × height)
    # X = fore-aft from LCA-front pivot (+fwd),  Y = height
    # ═══════════════════════════════════════════════════════════════════
    # Pivot bushing rectangles (side view: bushing fore-aft × rpw height)
    for px, pz, bush, col in [
        (LCAF_fa, LCAF_z, SUSP["lca_f_bushing"], GOLD),
        (LCAR_fa, LCAR_z, SUSP["lca_r_bushing"], GOLD),
        (UCAF_fa, UCAF_z, SUSP["uca_bushing"], BLUE),
        (UCAR_fa, UCAR_z, SUSP["uca_bushing"], BLUE),
    ]:
        rect = plt.Rectangle(
            (px - bush / 2, pz - rpw / 2),
            bush,
            rpw,
            edgecolor=col,
            facecolor=col,
            alpha=0.22,
            lw=1.2,
            zorder=2,
        )
        ax_side.add_patch(rect)

    ax_side.plot(
        [LCAF_fa, LCAR_fa],
        [LCAF_z, LCAR_z],
        color=GOLD,
        lw=2.5,
        solid_capstyle="round",
        zorder=3,
    )
    ax_side.plot(LCAF_fa, LCAF_z, "s", color=GOLD, markersize=9, zorder=5)
    ax_side.plot(LCAR_fa, LCAR_z, "s", color=GOLD, markersize=9, zorder=5)

    ax_side.plot(
        [UCAF_fa, UCAR_fa],
        [UCAF_z, UCAR_z],
        color=BLUE,
        lw=2.5,
        solid_capstyle="round",
        zorder=3,
    )
    ax_side.plot(UCAF_fa, UCAF_z, "^", color=BLUE, markersize=9, zorder=5)
    ax_side.plot(UCAR_fa, UCAR_z, "^", color=BLUE, markersize=9, zorder=5)

    ax_side.plot(
        [LCAF_fa, UCAF_fa],
        [LCAF_z, UCAF_z],
        color=TEXT,
        lw=0.7,
        alpha=0.18,
        linestyle=":",
        zorder=2,
    )
    ax_side.plot(
        [LCAR_fa, UCAR_fa],
        [LCAR_z, UCAR_z],
        color=TEXT,
        lw=0.7,
        alpha=0.18,
        linestyle=":",
        zorder=2,
    )

    # LCA labels below points, UCA labels above — well separated
    ax_side.text(
        LCAF_fa + 10, LCAF_z - 26, "LCA-front (0, 0)", fontsize=6.5, color=GOLD
    )
    ax_side.text(
        LCAR_fa + 10,
        LCAR_z - 26,
        f"LCA-rear ({LCAR_fa:.1f}, 0)",
        fontsize=6.5,
        color=GOLD,
    )
    ax_side.text(
        UCAF_fa + 10,
        UCAF_z + 18,
        f"UCA-front (+{UCAF_fa:.1f}, +{UCAF_z:.1f})",
        fontsize=6.5,
        color=BLUE,
    )
    ax_side.text(
        UCAR_fa + 10,
        UCAR_z + 18,
        f"UCA-rear ({UCAR_fa:.1f}, +{UCAR_z:.1f})",
        fontsize=6.5,
        color=BLUE,
    )

    dim(
        ax_side,
        (LCAF_fa, z_min + 18),
        (LCAR_fa, z_min + 18),
        f"{abs(LCAR_fa):.1f}mm",
        GOLD,
        yoff=-18,
        ha="center",
    )
    dim(
        ax_side,
        (UCAF_fa + 30, 0),
        (UCAF_fa + 30, UCAF_z),
        f"+{UCAF_z:.1f}mm",
        BLUE,
        ha="left",
    )
    dim(
        ax_side,
        (UCAR_fa - 30, 0),
        (UCAR_fa - 30, UCAR_z),
        f"+{UCAR_z:.1f}mm",
        BLUE,
        ha="right",
    )

    ax_side.axhline(0, color=GOLD, lw=0.5, alpha=0.3, linestyle=":")
    ax_side.axvline(0, color=GOLD, lw=0.5, alpha=0.3, linestyle=":")
    ax_side.text(3, 4, "LCA-front pivot (ref)", fontsize=5.5, color=GOLD, alpha=0.5)
    ax_side.set_xlim(fa_min, fa_max)
    ax_side.set_ylim(z_min, z_max)
    ax_side.set_aspect("equal", adjustable="box")
    ax_side.set_xlabel(
        "← back          Fore-aft from LCA-front pivot (mm)          front →"
    )
    ax_side.set_ylabel("Height from LCA pivot (mm)")
    ax_side.set_title("Side view", color=TEXT, fontsize=9, pad=6)

    fig.suptitle(
        "Miata NA front suspension — inner pivot pickup positions\n"
        "Lateral from car CL  /  Fore-aft from LCA-front pivot  /  Height from LCA pivot",
        color=TEXT,
        fontsize=9,
        y=1.01,
    )
    _note(ax_side)
    save(fig, "pickups_3view.png")


# ====================================================================
# Driveshaft geometry (013 rear axle post)
# ====================================================================
TRANS_ANGLE_DEG = 3.0  # transmission tilt (nose-down), degrees
DS_DROP_IN = 3.5  # driveshaft vertical drop, inches
DS_LENGTH_IN = 37.0  # driveshaft horizontal run, inches
PINION_ANGLE_DEG = 3.0  # pinion angle (parallel to motor), degrees

DS_ANGLE_DEG = np.degrees(np.arctan2(DS_DROP_IN, DS_LENGTH_IN))
FRONT_UJ_DEG = DS_ANGLE_DEG - TRANS_ANGLE_DEG
REAR_UJ_DEG = DS_ANGLE_DEG - PINION_ANGLE_DEG


def plot_driveshaft_angles():
    fig, ax = styled_fig(figsize=(10, 5.5))
    ax.set_aspect("equal")
    ax.grid(False)

    x_trans = 0.0
    y_trans = 0.0
    trans_rad = np.radians(-TRANS_ANGLE_DEG)
    ds_rad = np.radians(-DS_ANGLE_DEG)
    pin_rad = np.radians(-PINION_ANGLE_DEG)

    trans_stub = 8.0
    tx0 = x_trans - trans_stub * np.cos(trans_rad)
    ty0 = y_trans - trans_stub * np.sin(trans_rad)

    ds_x1 = x_trans + DS_LENGTH_IN * np.cos(ds_rad)
    ds_y1 = y_trans + DS_LENGTH_IN * np.sin(ds_rad)

    pin_stub = 6.0
    px1 = ds_x1 + pin_stub * np.cos(pin_rad)
    py1 = ds_y1 + pin_stub * np.sin(pin_rad)

    lw_main = 2.5
    ax.plot(
        [tx0, x_trans],
        [ty0, y_trans],
        color=BLUE,
        lw=lw_main,
        solid_capstyle="round",
        label=f"Trans output ({TRANS_ANGLE_DEG:.0f}\u00b0 down)",
    )
    ax.plot(
        [x_trans, ds_x1],
        [y_trans, ds_y1],
        color=GOLD,
        lw=lw_main,
        solid_capstyle="round",
        label=f"Driveshaft ({DS_ANGLE_DEG:.1f}\u00b0 down)",
    )
    ax.plot(
        [ds_x1, px1],
        [ds_y1, py1],
        color=A40_C,
        lw=lw_main,
        solid_capstyle="round",
        label=f"Pinion input ({PINION_ANGLE_DEG:.0f}\u00b0 down)",
    )

    ax.axhline(0, color=TEXT, lw=0.6, ls=":", alpha=0.3)
    ax.plot(
        [ds_x1 - 6, ds_x1 + 8], [ds_y1, ds_y1], color=TEXT, lw=0.6, ls=":", alpha=0.3
    )

    for ux, uy in [(x_trans, y_trans), (ds_x1, ds_y1)]:
        ax.plot(ux, uy, "o", color=GREEN, markersize=10, zorder=10)
        ax.plot(ux, uy, "o", color=BG, markersize=5, zorder=11)

    arc_r = 6.0
    front_arc = Arc(
        (x_trans, y_trans),
        2 * arc_r,
        2 * arc_r,
        angle=0,
        theta1=-DS_ANGLE_DEG,
        theta2=-TRANS_ANGLE_DEG,
        color=GREEN,
        lw=2,
        zorder=8,
    )
    ax.add_patch(front_arc)
    mid_f = np.radians(-(TRANS_ANGLE_DEG + DS_ANGLE_DEG) / 2)
    ax.text(
        x_trans + (arc_r + 1.5) * np.cos(mid_f),
        y_trans + (arc_r + 1.5) * np.sin(mid_f),
        f"{FRONT_UJ_DEG:.1f}\u00b0",
        color=GREEN,
        fontsize=11,
        fontweight="bold",
        ha="center",
        va="center",
        zorder=12,
    )

    rear_arc_r = 5.0
    rear_arc = Arc(
        (ds_x1, ds_y1),
        2 * rear_arc_r,
        2 * rear_arc_r,
        angle=0,
        theta1=180 - PINION_ANGLE_DEG,
        theta2=180 - DS_ANGLE_DEG,
        color=GREEN,
        lw=2,
        zorder=8,
    )
    ax.add_patch(rear_arc)
    mid_r = np.radians(180 - (PINION_ANGLE_DEG + DS_ANGLE_DEG) / 2)
    ax.text(
        ds_x1 + (rear_arc_r + 1.5) * np.cos(mid_r),
        ds_y1 + (rear_arc_r + 1.5) * np.sin(mid_r),
        f"{REAR_UJ_DEG:.1f}\u00b0",
        color=GREEN,
        fontsize=11,
        fontweight="bold",
        ha="center",
        va="center",
        zorder=12,
    )

    dim_x = ds_x1 + 2.5
    ax.annotate(
        "",
        xy=(dim_x, ds_y1),
        xytext=(dim_x, y_trans),
        arrowprops=dict(arrowstyle="<->", color=TEXT, lw=1),
    )
    ax.text(
        dim_x + 0.8,
        (y_trans + ds_y1) / 2,
        f'{DS_DROP_IN}" drop',
        color=TEXT,
        fontsize=8,
        ha="left",
        va="center",
    )

    dim_y = min(ds_y1, ty0) - 1.8
    ax.annotate(
        "",
        xy=(x_trans, dim_y),
        xytext=(ds_x1, dim_y),
        arrowprops=dict(arrowstyle="<->", color=TEXT, lw=1),
    )
    ax.text(
        (x_trans + ds_x1) / 2,
        dim_y - 0.6,
        f'{DS_LENGTH_IN}" center-to-center',
        color=TEXT,
        fontsize=8,
        ha="center",
        va="top",
    )

    ax.text(
        tx0 + 1.0,
        ty0 + 1.2,
        "SR20DET / Trans",
        color=BLUE,
        fontsize=9,
        ha="left",
        va="bottom",
    )
    ax.text(
        px1 - 0.5,
        py1 + 1.2,
        'Ford 8" Pinion',
        color=A40_C,
        fontsize=9,
        ha="right",
        va="bottom",
    )
    ax.text(
        x_trans + 0.8,
        y_trans - 1.2,
        "Front\nU-joint",
        color=GREEN,
        fontsize=7.5,
        ha="center",
        va="top",
    )
    ax.text(
        ds_x1 - 0.8,
        ds_y1 - 1.2,
        "Rear\nU-joint",
        color=GREEN,
        fontsize=7.5,
        ha="center",
        va="top",
    )

    ax.set_title("Driveshaft angle layout (side view at ride height)")
    ax.set_xlabel("Horizontal distance (in)")
    ax.set_ylabel("Vertical (in)")
    ax.legend(
        fontsize=7.5, facecolor=BG, edgecolor=GRID2, labelcolor=TEXT, loc="lower left"
    )
    pad = 3
    ax.set_xlim(tx0 - pad, px1 + pad + 3)
    ax.set_ylim(min(ds_y1, ty0) - pad - 1, max(ty0, py1) + pad)
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_major_locator(MultipleLocator(2))
    save(fig, "driveshaft_angles.png")


def plot_ujoint_life():
    """U-joint life vs operating angle (inverse proportional model)."""
    fig, ax = styled_fig(figsize=(7, 4.5))

    L_REF = 5000
    THETA_REF = 3.0
    theta = np.linspace(0.5, 15, 500)
    life = L_REF * (THETA_REF / theta)

    ax.plot(
        theta, life, color=GOLD, lw=2.5, label="U-joint life (3000 RPM, rated load)"
    )
    ax.fill_between(theta, life, alpha=0.08, color=GOLD)

    ax.axvspan(0.5, 3, color=GREEN, alpha=0.06)
    ax.axvspan(3, 5, color=GOLD, alpha=0.06)
    ax.axvspan(5, 15, color=PINK, alpha=0.06)
    ax.text(
        1.75,
        13000,
        "ideal\n(1-3\u00b0)",
        color=GREEN,
        fontsize=7,
        ha="center",
        alpha=0.7,
    )
    ax.text(
        4.0,
        13000,
        "acceptable\n(3-5\u00b0)",
        color=GOLD,
        fontsize=7,
        ha="center",
        alpha=0.7,
    )
    ax.text(
        10.0,
        13000,
        "service life concern\n(>5\u00b0)",
        color=PINK,
        fontsize=7,
        ha="center",
        alpha=0.7,
    )

    markers = [
        (FRONT_UJ_DEG, f"A40 build ({FRONT_UJ_DEG:.1f}\u00b0)", GREEN),
        (3.0, "Rated (3.0\u00b0)", BLUE),
        (6.0, "Double angle (6.0\u00b0)", PINK),
    ]
    label_ys = [9500, 7000, 4500]
    for (ang, lbl, col), ly in zip(markers, label_ys):
        lf = L_REF * THETA_REF / ang
        ax.plot(ang, lf, "o", color=col, markersize=8, zorder=5)
        ax.annotate(
            f"{lbl}\n{lf:.0f} hrs",
            xy=(ang, lf),
            xytext=(ang + 1.8, ly),
            fontsize=7,
            color=col,
            arrowprops=dict(arrowstyle="->", color=col, lw=0.6),
        )

    ax.axhline(L_REF, color=TEXT, ls=":", lw=0.8, alpha=0.4)
    ax.text(
        14.5,
        L_REF + 300,
        "5000 hrs\n(rated)",
        color=TEXT,
        fontsize=6.5,
        ha="right",
        va="bottom",
        alpha=0.5,
    )

    ax.set_xlabel("U-joint operating angle (\u00b0)")
    ax.set_ylabel("Life expectancy (hours at 3000 RPM)")
    ax.set_title("U-joint life vs operating angle (constant load)")
    ax.set_xlim(0.5, 15)
    ax.set_ylim(0, 15000)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(2500))
    ax.legend(
        fontsize=7, facecolor=BG, edgecolor=GRID2, labelcolor=TEXT, loc="upper right"
    )
    save(fig, "ujoint_life.png")


# ====================================================================
def main():
    print("Generating plots...")
    plot_roll_vs_cg()
    plot_rc_construction()
    plot_rc_tire_comparison()
    plot_rc_combined()
    plot_track_effects()
    plot_arb_sizing()
    plot_ride_frequency()
    plot_ackermann()
    plot_ackermann_topview()
    plot_ackermann_turn()
    plot_motion_ratio()
    plot_weight_transfer()
    plot_jacking()
    plot_rack_narrowing()
    plot_lca_plan()
    plot_uca_plan()
    plot_knuckle_3view()
    plot_pickups_3view()
    plot_driveshaft_angles()
    plot_ujoint_life()
    print("Done.")


if __name__ == "__main__":
    main()
