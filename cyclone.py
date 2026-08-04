"""Parametric reverse-flow cyclone separator generator.

Design basis: docs/research/ (Stage 1 corpus). Claim IDs in comments refer to it.
Everything is driven from `Spec`; geometry is derived, never hand-entered.

    uv run python cyclone.py --preset build1
    uv run python cyclone.py --preset build2 --check-only
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass, replace
from pathlib import Path

from build123d import (
    Align,
    Box,
    Circle,
    Cone,
    Cylinder,
    Keep,
    Plane,
    Pos,
    Rectangle,
    Rot,
    export_step,
    export_stl,
    loft,
)

CFM_TO_M3S = 1 / 2118.88
IN_H2O = 249.09  # Pa
MU_AIR = 1.81e-5  # Pa.s
RHO_AIR = 1.20  # kg/m3
RHO_WOOD = 730.0  # kg/m3  (P8.02)


# --------------------------------------------------------------------------- spec


@dataclass(frozen=True)
class Spec:
    """All dimensions mm, flow CFM. Ratios are of body diameter D."""

    name: str = "build1"

    # --- duty ---
    Q_cfm: float = 55.0  # P8.57 band 40-70, midpoint adopted (D4)
    hose_id: float = 47.6  # 1-7/8" shop vac hose (P8.89 is the *boot*, this is the vac)

    # --- cyclone: 1D3D family (phase-10 section 10.11) ---
    D: float = 118.0
    a_r: float = 0.50  # inlet height / D
    b_r: float = 0.25  # inlet width / D
    # P8.61 recommends 0.45-0.50, but G3 only admits 0.466-0.564 at 1D3D inlet
    # proportions, so 0.45 is infeasible. 0.50 is the family value and sits mid-window.
    De_r: float = 0.50  # vortex finder dia / D
    S_r: float = 0.50  # vortex finder insertion / D
    h_r: float = 1.00  # barrel height / D        (1D3D)
    cone_r: float = 3.00  # cone height / D          (1D3D)
    B_r: float = 0.25  # cone tip dia / D

    # --- manufacture ---
    # Wall is slicer-aligned: an exact multiple of extrusion width so the shell is
    # solid perimeters with ZERO infill. 5 x 0.45 = 2.25 mm gives a x9 buckling
    # margin at D=118 (need ~14 kPa), and P7.11 says perimeter count is what
    # actually drives air-tightness.
    nozzle: float = 0.40
    line_width: float = 0.45
    perimeters: int = 5
    layer_h: float = 0.20
    bed_z: float = 250.0  # P1S usable Z (P8.68)
    bed_xy: float = 248.0  # P1S usable XY
    flange_w: float = 12.0  # radial width of course flanges
    flange_t: float = 5.0
    n_bolts: int = 6
    bolt_dia: float = 4.4  # M4 clearance
    oring_cord: float = 3.0
    fit: float = 0.30  # printed clearance per side

    # --- vessel (2 x Greif 30-gal open head, P4.78) ---
    # No plywood stiffener: P4.81 was wrong (see P4.92-P4.96). The steel lid carries
    # this load in membrane action. The printed flange only has to spread the
    # cyclone's weight and reinforce the edge of the hole cut for the cone tip.
    socket_od: float = 150.0
    socket_bolts: int = 6
    socket_bolt_dia: float = 5.5

    # Gate IDs knowingly accepted for this spec, with the rationale recorded in
    # docs/research/. Anything not listed here is a hard stop.
    accepted: frozenset = frozenset()

    # ---------------------------------------------------------------- derived

    @property
    def wall(self) -> float:
        """Slicer-aligned shell thickness."""
        return self.perimeters * self.line_width

    @property
    def a(self) -> float:
        return self.a_r * self.D

    @property
    def b(self) -> float:
        return self.b_r * self.D

    @property
    def De(self) -> float:
        return self.De_r * self.D

    @property
    def S(self) -> float:
        return self.S_r * self.D

    @property
    def h(self) -> float:
        return self.h_r * self.D

    @property
    def cone_h(self) -> float:
        return self.cone_r * self.D

    @property
    def B(self) -> float:
        return self.B_r * self.D

    @property
    def H(self) -> float:
        return self.h + self.cone_h

    @property
    def Q(self) -> float:
        """m3/s"""
        return self.Q_cfm * CFM_TO_M3S

    @property
    def inlet_area(self) -> float:
        """m2"""
        return (self.a / 1000) * (self.b / 1000)

    @property
    def vin(self) -> float:
        """Mean inlet velocity, m/s."""
        return self.Q / self.inlet_area

    @property
    def cone_semi_angle(self) -> float:
        """degrees; G2 wants 6.8 < eps <= 16"""
        return math.degrees(math.atan((self.D - self.B) / 2 / self.cone_h))

    @property
    def x50(self) -> float:
        """Lapple cut size, micron. Ne=6 (P2.10). Tier E, +/-50% (P8.49)."""
        return (
            math.sqrt(
                9
                * MU_AIR
                * (self.b / 1000)
                / (2 * math.pi * 6 * self.vin * (RHO_WOOD - RHO_AIR))
            )
            * 1e6
        )

    @property
    def Eu(self) -> float:
        """Shepherd-Lapple velocity heads (P1.5)."""
        return 16 * self.a * self.b / self.De**2

    @property
    def dp(self) -> float:
        """Pa"""
        return self.Eu * 0.5 * RHO_AIR * self.vin**2

    @property
    def natural_vortex_len(self) -> float:
        """Alexander, mm (P4.02)."""
        return 2.3 * self.De * (self.D**2 / (self.a * self.b)) ** (1 / 3)

    @property
    def n_courses(self) -> int:
        return max(1, math.ceil((self.H + self.wall) / self.bed_z))

    @property
    def split_z(self) -> list[float]:
        """Course boundaries, measured from the cone tip (z=0)."""
        n = self.n_courses
        if n == 1:
            return []
        total = self.H + self.wall
        return [total * i / n for i in range(1, n)]

    @property
    def needs_arc_split(self) -> bool:
        return self.D + 2 * self.wall + 2 * self.flange_w > self.bed_xy

    @property
    def De_r_window(self) -> tuple[float, float]:
        """Feasible De/D range under G3, given this inlet. Smaller = finer cut."""
        ab = self.a * self.b
        lo = math.sqrt(ab / (0.735 * math.pi / 4)) / self.D
        hi = math.sqrt(ab / (0.500 * math.pi / 4)) / self.D
        return lo, hi


# --------------------------------------------------------------------------- checks


GATES = {"G1", "G2", "G3", "G4", "G5", "G7", "G8", "O1", "M3", "S8"}
PREFERENCES = {"G6", "O3"}  # P2.23: G6 is violated by Stairmand HE itself


def check(s: Spec) -> list[tuple[str, bool, str]]:
    """Constraint set from phase-10 section 10.2. Returns (id, passed, detail)."""
    r: list[tuple[str, bool, str]] = []

    def add(cid, ok, detail):
        r.append((cid, bool(ok), detail))

    def add_range(cid, val, lo, hi, detail, tol=1e-6):
        """Inclusive bounds; flags when a value sits exactly on one (classical
        families routinely do -- see P2.21 for Swift HE on G3)."""
        ok = lo - tol <= val <= hi + tol
        at = abs(val - lo) <= tol or abs(val - hi) <= tol
        r.append((cid, ok, detail + (" -- AT BOUND" if at else "")))

    add("G1", s.S < s.h < s.H, f"S={s.S:.1f} < h={s.h:.1f} < H={s.H:.1f}")
    eps = s.cone_semi_angle
    add("G2", 6.8 < eps <= 16.0, f"cone semi-angle {eps:.1f} deg (want 6.8-16)")
    g3 = (s.a * s.b) / (math.pi / 4 * s.De**2)
    lo, hi = s.De_r_window
    add(
        "G3",
        0.5 < g3 < 0.735,
        f"inlet/outlet area ratio {g3:.3f} (want 0.5-0.735) "
        f"=> feasible De/D {lo:.3f}-{hi:.3f}, have {s.De_r:.3f}",
    )
    add_range(
        "G4", s.B, 0.5 * s.De, s.De,
        f"B={s.B:.1f} within 0.5*De={0.5*s.De:.1f} .. De={s.De:.1f}",
    )
    add_range(
        "G5", s.b, 0.0, 0.5 * (s.D - s.De),
        f"b={s.b:.1f} <= 0.5*(D-De)={0.5*(s.D-s.De):.1f}",
    )
    add("G6", s.S > 1.25 * s.a, f"S={s.S:.1f} vs 1.25a={1.25*s.a:.1f} (PREFERENCE, P2.23)")
    ln = s.natural_vortex_len
    add("G7", ln <= s.H - s.S, f"Alexander Ln={ln:.0f} <= H-S={s.H-s.S:.0f}")
    add("G8", abs(s.H / s.D - 4.0) < 0.5, f"H/D={s.H/s.D:.2f} (want ~4)")

    add("O1", 12.0 <= s.vin <= 17.0, f"vin={s.vin:.1f} m/s (band 12-17)")
    # O2 (saltation) needs vs, which no model here provides -- recorded, not checked.
    add("O3", True, f"inlet area set from vin: a x b = {s.a:.1f} x {s.b:.1f} mm")

    add("M3", s.wall >= 1.6, f"wall {s.wall} mm")
    add(
        "S8",
        not s.needs_arc_split,
        f"flange OD {s.D+2*s.wall+2*s.flange_w:.0f} vs bed {s.bed_xy:.0f} mm"
        + (" -> ARC SPLIT REQUIRED" if s.needs_arc_split else ""),
    )
    return r


def _mass_g(s: Spec, density: float = 1.27) -> float:
    """Rough print mass: wall volume of every part, at 100% shell density."""
    parts = list(body_courses(s).values()) + [vortex_finder(s), lid_socket(s)]
    if s.needs_arc_split:
        parts.append(inlet_duct(s))
    return sum(p.volume for p in parts) / 1000 * density


def report(s: Spec) -> str:
    rows = check(s)
    lines = [
        f"# Cyclone `{s.name}`",
        "",
        f"Generated from `cyclone.py`. Design basis: `docs/research/`.",
        "",
        "## Duty",
        "",
        f"| Flow | {s.Q_cfm:.0f} CFM ({s.Q*1000:.1f} L/s) |",
        "|---|---|",
        f"| Inlet velocity `vin` | **{s.vin:.1f} m/s** |",
        f"| Cut size `x50` (Lapple, +/-50%) | **{s.x50:.2f} um** |",
        f"| Euler number `Eu` | {s.Eu:.1f} |",
        f"| Pressure drop | {s.dp:.0f} Pa = {s.dp/IN_H2O:.1f}\" H2O |",
        "",
        "## Geometry",
        "",
        "| Dim | Ratio | mm |",
        "|---|---|---|",
        f"| Body `D` | 1.00 | **{s.D:.1f}** |",
        f"| Inlet height `a` | {s.a_r:.2f} | {s.a:.1f} |",
        f"| Inlet width `b` | {s.b_r:.2f} | {s.b:.1f} |",
        f"| Vortex finder `De` | {s.De_r:.2f} | {s.De:.1f} |",
        f"| Insertion `S` | {s.S_r:.2f} | {s.S:.1f} |",
        f"| Barrel `h` | {s.h_r:.2f} | {s.h:.1f} |",
        f"| Cone height | {s.cone_r:.2f} | {s.cone_h:.1f} |",
        f"| Total `H` | {s.H/s.D:.2f} | {s.H:.1f} |",
        f"| Cone tip `B` | {s.B_r:.2f} | {s.B:.1f} |",
        f"| Cone semi-angle | - | {s.cone_semi_angle:.1f} deg |",
        "",
        "## Manufacture",
        "",
        f"- Wall {s.wall:.1f} mm, courses **{s.n_courses}**, "
        + (
            f"arc split: segments per course {'+'.join(str(n) for n in arc_plan(s))} "
            f"= **{sum(arc_plan(s))} shell prints** (S8/P8.103)"
            if s.needs_arc_split
            else "arc split not needed"
        ),
        f"- Course splits at z = {', '.join(f'{z:.0f}' for z in s.split_z) or 'n/a'} mm above cone tip",
        f"- Barrel flange OD {2*_course_R(s, s.H):.0f} mm; cone-joint flanges sized to the joint",
        f"- Filament (solid perimeters, PETG @ 1.27 g/cm3): **~{_mass_g(s):.0f} g**",
        "",
        "### Slicer settings",
        "",
        "| Setting | Value | Why |",
        "|---|---|---|",
        f"| Nozzle | {s.nozzle:.1f} mm | |",
        f"| Wall loop width | {s.line_width:.2f} mm | wall = perimeters x width, exactly |",
        f"| Wall loops | **{s.perimeters}** | gives {s.wall:.2f} mm shell |",
        f"| Layer height | {s.layer_h:.2f} mm | |",
        "| Infill | **0 %** | the shell is solid perimeters; there is nothing to fill |",
        "| Top/bottom layers | 5 | flanges and roof only |",
        "| Supports | none | see orientation below |",
        "| Material | PETG | P7.09; ASA if the enclosure is warm and stiffness matters |",
        "",
        "### Print orientation (all support-free)",
        "",
        "| Part | On the bed | Note |",
        "|---|---|---|",
        "| cone courses / arcs | wide end down | cone narrows upward at "
        f"{s.cone_semi_angle:.1f} deg - self-supporting |",
        "| top course / arcs | **roof down** | flat face, best adhesion"
        + ("" if s.needs_arc_split else f"; the inlet duct bridges {s.b:.0f} mm")
        + " |",
        "| `vortex_finder` | collar down | |",
        "| `lid_socket` | plate down | |",
    ] + (
        [
            "| `inlet_duct` | flange plate down | rect->round morph rises near-vertical |",
            "",
            "Axial seams (arc segments): M4 through the seam webs, foam tape or a thin "
            "silicone bead on the web faces. Seams are in compression under vacuum "
            "(P8.100) - they need sealing and roundness, not strength.",
            "",
        ]
        if s.needs_arc_split
        else [""]
    ) + [
        "### Drum lid",
        "",
        drill_pattern(s),
        "",
        "## Constraints",
        "",
        "| ID | Result | Detail |",
        "|---|---|---|",
    ]
    for cid, ok, detail in rows:
        if ok:
            verdict = "PASS"
        elif cid in s.accepted:
            verdict = "accepted"
        elif cid in PREFERENCES:
            verdict = "warn"
        else:
            verdict = "**FAIL**"
        lines.append(f"| `{cid}` | {verdict} | {detail} |")
    lines += [
        "",
        f"Feasible `De/D` window for this inlet: **{s.De_r_window[0]:.3f}-{s.De_r_window[1]:.3f}** "
        f"(G3). Smaller = finer cut, more pressure drop.",
        "",
        "Not machine-checked: `O2` (saltation, needs `vs`, which no model in the corpus supplies).",
        "`G6` and `O3` are preferences, not gates (P2.23 - Stairmand HE violates G6 too).",
        "",
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------- geometry
#
# Coordinates: origin at the CONE TIP, +Z up.
#   z = 0            cone tip, inner radius B/2
#   z = cone_h       cone/barrel junction, inner radius D/2
#   z = cone_h + h   barrel top = roof underside
#   z = H + wall     roof top


DUCT_STUB = 20.0  # rect stub beyond the barrel OD to the bolt-on duct frame (arc mode)


def _duct_frame(s: Spec) -> dict:
    """Shared geometry of the bolt-on inlet joint (arc-split builds, P12.06/D8)."""
    ri_body = s.D / 2
    y_c = ri_body - s.b / 2
    z_c = s.H - s.a / 2
    fw = s.flange_w
    x_f = -(ri_body + s.wall + DUCT_STUB)  # frame face plane
    z_lo = z_c - s.a / 2 - s.wall - fw
    z_hi = min(z_c + s.a / 2 + s.wall + fw, s.H + s.wall)  # capped at roof top
    holes = []  # (y, z) — U pattern: 4 side, 2 bottom; roof caps the top edge
    y_side = s.b / 2 + s.wall + fw / 2
    for sy in (-1, 1):
        for dz in (-s.a / 4, s.a / 4):
            holes.append((y_c + sy * y_side, z_c + dz))
    z_bot = z_c - (s.a / 2 + s.wall + fw / 2)
    for dy in (-s.b / 4, s.b / 4):
        holes.append((y_c + dy, z_bot))
    return dict(y_c=y_c, z_c=z_c, x_f=x_f, z_lo=z_lo, z_hi=z_hi,
                frame_w=s.b + 2 * s.wall + 2 * fw, holes=holes)


def _solids(s: Spec):
    """(outer, void). void = every air-side volume: flow cavity, duct bore, finder
    clearance. Kept separate so arc-seam webs can be carved to never enter the flow."""
    ri_tip, ri_body = s.B / 2, s.D / 2
    z_j, z_top = s.cone_h, s.H  # junction, roof underside

    up = (Align.CENTER, Align.CENTER, Align.MIN)
    outer = Cone(ri_tip + s.wall, ri_body + s.wall, z_j, align=up)
    outer += Pos(0, 0, z_j) * Cylinder(ri_body + s.wall, s.h + s.wall, align=up)

    # tangential inlet: outer wall of the duct is tangent to the barrel bore.
    y_c = ri_body - s.b / 2
    z_c = z_top - s.a / 2
    # The rect section must sit INSIDE the barrel wall: a union across exactly
    # coincident faces leaves two disconnected solids (OCCT), so overlap by 2*wall.
    x_rect = -(ri_body + s.wall) + 2 * s.wall

    inner = Cone(ri_tip, ri_body, z_j, align=up)
    inner += Pos(0, 0, z_j) * Cylinder(ri_body, s.h, align=up)

    if s.needs_arc_split:
        # Integral duct would overflow the bed (P12.06): keep only a rect stub and a
        # bolt frame; the morph+spigot become the separate `inlet_duct` part (D8).
        f = _duct_frame(s)
        x_f = f["x_f"]
        outer += Pos((x_rect + x_f) / 2, y_c, z_c) * Box(
            x_rect - x_f, s.b + 2 * s.wall, s.a + 2 * s.wall
        )
        outer += Pos(x_f + s.flange_t / 2, y_c, (f["z_lo"] + f["z_hi"]) / 2) * Box(
            s.flange_t, f["frame_w"], f["z_hi"] - f["z_lo"]
        )
        for yy, zz in f["holes"]:
            outer -= Pos(x_f + s.flange_t / 2, yy, zz) * Rot(0, 90, 0) * Cylinder(
                s.bolt_dia / 2, 2 * s.flange_t + 6, align=(Align.CENTER, Align.CENTER, Align.CENTER)
            )
        duct_bore = Pos((x_rect + x_f - 2) / 2, y_c, z_c) * Box(
            x_rect - x_f + 2, s.b, s.a
        )
    else:
        # Area-matched rect->round morph printed integral with the top course.
        duct_len = s.a
        spigot = 25.0
        x_round = x_rect - duct_len
        x_end = x_round - spigot
        pl_r_o = Plane(origin=(x_rect, y_c, z_c), z_dir=(1, 0, 0))
        pl_c_o = Plane(origin=(x_round, y_c, z_c), z_dir=(1, 0, 0))
        outer += loft(
            [pl_r_o * Rectangle(s.b + 2 * s.wall, s.a + 2 * s.wall),
             pl_c_o * Circle(s.hose_id / 2 + s.wall)]
        )
        outer += Pos(x_end, y_c, z_c) * Rot(0, 90, 0) * Cylinder(
            s.hose_id / 2 + s.wall, spigot, align=(Align.CENTER, Align.CENTER, Align.MIN)
        )
        pl_r_i = Plane(origin=(x_rect + 0.01, y_c, z_c), z_dir=(1, 0, 0))
        pl_c_i = Plane(origin=(x_round, y_c, z_c), z_dir=(1, 0, 0))
        duct_bore = loft([pl_r_i * Rectangle(s.b, s.a), pl_c_i * Circle(s.hose_id / 2)])
        duct_bore += Pos(x_end - 1, y_c, z_c) * Rot(0, 90, 0) * Cylinder(
            s.hose_id / 2, spigot + 1, align=(Align.CENTER, Align.CENTER, Align.MIN)
        )

    # extend the rectangular mouth inward so it fully opens into the barrel
    duct_bore += Pos(x_rect + ri_body / 2, y_c, z_c) * Box(
        ri_body + 2 * s.wall, s.b, s.a
    )
    inner += duct_bore

    # vortex finder bore through the roof, with print clearance for a separate tube
    void = inner + Pos(0, 0, s.H - s.S) * Cylinder(
        s.De / 2 + s.wall + s.fit, s.S + s.wall + 1, align=up
    )
    return outer, void


def _shell(s: Spec):
    """Solid body: cone + barrel + roof + tangential inlet, bored out."""
    outer, void = _solids(s)
    return outer - void


def _joint_bolts(s: Spec, pcd: float) -> int:
    """Bolt count so spacing stays <= ~90 mm on big joints (P7.14 - joints leak first)."""
    return max(s.n_bolts, math.ceil(2 * math.pi * pcd / 90.0))


def _flange(s: Spec, z_lo: float, r_inner: float, r_joint: float):
    """Annular flange occupying z_lo .. z_lo+flange_t, bored to r_inner, with bolt holes.

    Sized to the JOINT radius, not D: cone-joint flanges stay local, so lower cone
    courses can print whole even when the barrel needs arc splitting (P12.06).
    """
    up = (Align.CENTER, Align.CENTER, Align.MIN)
    r_o = r_joint + s.wall + s.flange_w
    fl = Pos(0, 0, z_lo) * Cylinder(r_o, s.flange_t, align=up)
    fl -= Pos(0, 0, z_lo - 1) * Cylinder(r_inner, s.flange_t + 2, align=up)
    pcd = r_joint + s.wall + s.flange_w / 2
    n = _joint_bolts(s, pcd)
    for i in range(n):
        ang = 2 * math.pi * i / n
        fl -= Pos(pcd * math.cos(ang), pcd * math.sin(ang), z_lo - 1) * Cylinder(
            s.bolt_dia / 2, s.flange_t + 2, align=up
        )
    return fl


def _radius_at(s: Spec, z: float) -> float:
    """Inner radius of the shell at height z."""
    if z <= 0:
        return s.B / 2
    if z >= s.cone_h:
        return s.D / 2
    return s.B / 2 + (s.D / 2 - s.B / 2) * z / s.cone_h


def _largest(shape):
    """split() may return a list when the cut disconnects the body."""
    if isinstance(shape, (list, tuple)):
        return max(shape, key=lambda x: x.volume)
    if hasattr(shape, "solids") and len(shape.solids()) > 1:
        return max(shape.solids(), key=lambda x: x.volume)
    return shape


# ------------------------------------------------------------------ arc split (S8/P8.103)
#
# A course whose flange OD exceeds the bed splits into n arc segments about Z.
# Axial seams are in COMPRESSION under vacuum (P8.100): the webs + bolts provide
# alignment and sealing clamp, not strength. Min-bbox rule: an arc of outer radius
# R and angle 2pi/n, axis-aligned, boxes to R*(1-cos(2pi/n)) x R.


def _n_arcs(s: Spec, R: float) -> int:
    """Fewest segments so one segment of outer radius R fits the bed."""
    if 2 * R <= s.bed_xy:
        return 1
    for n in range(3, 13):  # n=2 boxes to 2R x R, never fits once 2R > bed
        if R <= s.bed_xy and R * (1 - math.cos(2 * math.pi / n)) <= s.bed_xy:
            return n
    raise ValueError(f"segment radius {R:.0f} mm cannot fit a {s.bed_xy:.0f} mm bed")


def _course_bounds(s: Spec) -> list[tuple[float, float]]:
    total = s.H + s.wall
    bounds = [0.0] + list(s.split_z) + [total]
    return list(zip(bounds, bounds[1:]))


def _course_R(s: Spec, hi: float) -> float:
    """Governing outer radius of a course = its widest flange + the register lip."""
    return _radius_at(s, min(hi, s.H)) + s.wall + s.flange_w + s.fit + s.wall


def arc_plan(s: Spec) -> list[int]:
    """Segments per course, bottom to top."""
    return [_n_arcs(s, _course_R(s, hi)) for _, hi in _course_bounds(s)]


def _duct_window(s: Spec) -> tuple[float, float]:
    """Angular span (rad) the inlet stub occupies on the barrel wall."""
    ri_body = s.D / 2
    y_c = ri_body - s.b / 2
    theta_c = math.atan2(y_c, -(ri_body + s.wall))
    half = math.atan((s.b / 2 + s.wall + s.flange_w + 8) / ri_body)
    return theta_c - half, theta_c + half


def _ang_dist(a: float, b: float) -> float:
    d = abs(a - b) % (2 * math.pi)
    return min(d, 2 * math.pi - d)


def _seam_offset(s: Spec, n: int, lo: float, hi: float, has_duct: bool) -> float:
    """Rotate the seam pattern so no seam crosses the inlet stub or lands on a
    horizontal-flange bolt hole. Deterministic search; falls back to best-effort."""
    phi = 2 * math.pi / n
    total = s.H + s.wall
    bolt_angles = []
    clearance = 0.05  # rad floor
    for z_joint in ([lo] if lo > 0 else []) + ([hi] if hi < total else []):
        pcd = _radius_at(s, min(z_joint, s.H)) + s.wall + s.flange_w / 2
        nb = _joint_bolts(s, pcd)
        bolt_angles += [(2 * math.pi * i / nb, pcd) for i in range(nb)]
        clearance = max(clearance, ((s.bolt_dia + s.flange_t) / 2 + 2) / pcd)
    win = _duct_window(s) if has_duct else None

    best, best_score = 0.0, -1.0
    for step in range(180):
        off = phi * step / 180
        seams = [off + k * phi for k in range(n)]
        if win and any(win[0] - 0.1 < th % (2 * math.pi) < win[1] + 0.1 for th in seams):
            continue
        score = min(
            (_ang_dist(th, ba) for th in seams for ba, _ in bolt_angles),
            default=math.pi,
        )
        if score > best_score:
            best, best_score = off, score
        if score >= clearance:
            return off
    if best_score < 0:
        raise ValueError(f"no seam offset clears the inlet stub with n={n}")
    return best  # bolt clash unavoidable; closest approach still best_score rad


def _course_arcs(s: Spec, seg, lo: float, hi: float, n: int, void, has_duct: bool) -> dict:
    """Cut one course into n sectors, each with seam webs + bolt holes."""
    up = (Align.CENTER, Align.CENTER, Align.MIN)
    lo3 = (Align.MIN, Align.MIN, Align.MIN)
    R = _course_R(s, hi)
    phi = 2 * math.pi / n
    off = _seam_offset(s, n, lo, hi, has_duct)
    hz = hi - lo
    r_b = R - s.flange_w / 2
    zs_bolt = [lo + 18, hi - 18] + ([lo + hz / 2] if hz > 150 else [])
    parts = {}
    big = 4 * R
    ctr = (Align.CENTER, Align.CENTER, Align.CENTER)
    z_mid = lo - 1 + (hz + 14) / 2
    for k in range(n):
        t1 = off + k * phi
        # sector = seg cut by two half-spaces (valid for phi <= 180 deg); Cylinder's
        # arc_size can't be used - align centres the pie's bbox, moving the apex off axis
        hs1 = Rot(0, 0, math.degrees(t1)) * Pos(0, big / 2, z_mid) * Box(
            2 * big, big, hz + 14, align=ctr
        )
        hs2 = Rot(0, 0, math.degrees(t1 + phi)) * Pos(0, -big / 2, z_mid) * Box(
            2 * big, big, hz + 14, align=ctr
        )
        sector = seg & hs1 & hs2
        w1 = Rot(0, 0, math.degrees(t1)) * Pos(0, 0, lo) * Box(
            R, s.flange_t, hz, align=lo3
        )
        w2 = Rot(0, 0, math.degrees(t1 + phi)) * Pos(0, 0, lo) * Box(
            R, s.flange_t, hz, align=(Align.MIN, Align.MAX, Align.MIN)
        )
        webs = (w1 + w2) - void
        for th in (t1, t1 + phi):
            for zb in zs_bolt:
                hole = Rot(0, 0, math.degrees(th)) * Pos(r_b, 0, zb) * Rot(90, 0, 0) * Cylinder(
                    s.bolt_dia / 2, 2 * s.flange_t + 6,
                    align=(Align.CENTER, Align.CENTER, Align.CENTER),
                )
                webs -= hole
                sector -= hole
        # rotate the seam onto +X: bbox becomes R*(1-cos(phi)) x R, provably on-bed
        parts[f"arc{k+1}"] = Rot(0, 0, -math.degrees(t1)) * (sector + webs)
    return parts


def body_courses(s: Spec) -> dict:
    """Split the shell into printable courses joined by butt flanges + a register boss.
    Courses whose flanges overflow the bed split further into arc segments (S8/P8.103)."""
    outer, void = _solids(s)
    shell = outer - void
    zs = s.split_z
    if not zs and not s.needs_arc_split:
        return {"body": shell}

    up = (Align.CENTER, Align.CENTER, Align.MIN)
    reg_h = 8.0
    total = s.H + s.wall
    plan = arc_plan(s)
    z_duct_lo = s.H - s.a  # inlet stub z-window (arc mode)
    parts: dict = {}

    for i, (lo, hi) in enumerate(_course_bounds(s)):
        seg = shell
        if lo > 0:
            seg = _largest(seg.split(Plane.XY.offset(lo), keep=Keep.TOP))
        if hi < total:
            seg = _largest(seg.split(Plane.XY.offset(hi), keep=Keep.BOTTOM))

        if lo > 0:  # bottom flange of this course
            seg += _flange(s, lo, _radius_at(s, lo), _radius_at(s, lo))
        if hi < total:
            # top flange + register lip that wraps the NEXT course's flange OD.
            # External (an internal bore boss disconnects at barrel joints - the fit
            # gap has no cone slope to bridge - and would ledge into the flow).
            seg += _flange(s, hi - s.flange_t, _radius_at(s, hi - s.flange_t), _radius_at(s, hi))
            r_o = _radius_at(s, hi) + s.wall + s.flange_w  # joint flange OD, both sides
            foot = Pos(0, 0, hi - s.flange_t) * Cylinder(
                r_o + s.fit + s.wall, s.flange_t, align=up
            )
            foot -= Pos(0, 0, hi - s.flange_t - 1) * Cylinder(r_o - 2, s.flange_t + 2, align=up)
            neck = Pos(0, 0, hi - 1) * Cylinder(r_o + s.fit + s.wall, reg_h + 1, align=up)
            neck -= Pos(0, 0, hi - 2) * Cylinder(r_o + s.fit, reg_h + 3, align=up)
            seg += foot + neck

        name = f"body_course_{i+1:02d}"
        if plan[i] == 1:
            parts[name] = seg
        else:
            has_duct = s.needs_arc_split and hi > z_duct_lo
            for suffix, arc in _course_arcs(s, seg, lo, hi, plan[i], void, has_duct).items():
                parts[f"{name}_{suffix}"] = arc
    return parts


def inlet_duct(s: Spec):
    """Bolt-on inlet for arc-split builds: frame + rect->round morph + hose spigot.

    The integral duct overflows the bed once D is barrel-course size (P12.06), and a
    separate inlet is independently re-printable anyway (D8). Diffuser or contraction
    falls out of the areas — no separate decision (O3, P12.07). Print flange-down.
    """
    f = _duct_frame(s)
    y_c, z_c, x_f = f["y_c"], f["z_c"], f["x_f"]
    morph, spigot, lead = 120.0, 25.0, 10.0
    x_plate = x_f - s.flange_t  # plate occupies x_f-flange_t .. x_f (mates the frame face)
    x_round = x_plate - lead - morph
    x_end = x_round - spigot

    part = Pos(x_f - s.flange_t / 2, y_c, (f["z_lo"] + f["z_hi"]) / 2) * Box(
        s.flange_t, f["frame_w"], f["z_hi"] - f["z_lo"]
    )
    # rect lead-out, overlapping the plate so the union is robust
    part += Pos((x_f + x_plate - lead) / 2, y_c, z_c) * Box(
        x_f - x_plate + lead, s.b + 2 * s.wall, s.a + 2 * s.wall
    )
    pl_r_o = Plane(origin=(x_plate - lead, y_c, z_c), z_dir=(1, 0, 0))
    pl_c_o = Plane(origin=(x_round, y_c, z_c), z_dir=(1, 0, 0))
    part += loft(
        [pl_r_o * Rectangle(s.b + 2 * s.wall, s.a + 2 * s.wall),
         pl_c_o * Circle(s.hose_id / 2 + s.wall)]
    )
    part += Pos(x_end, y_c, z_c) * Rot(0, 90, 0) * Cylinder(
        s.hose_id / 2 + s.wall, spigot, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )

    bore = Pos((x_f + 2 + x_plate - lead) / 2, y_c, z_c) * Box(
        x_f + 2 - (x_plate - lead), s.b, s.a
    )
    pl_r_i = Plane(origin=(x_plate - lead + 0.01, y_c, z_c), z_dir=(1, 0, 0))
    bore += loft([pl_r_i * Rectangle(s.b, s.a), pl_c_o * Circle(s.hose_id / 2)])
    bore += Pos(x_end - 1, y_c, z_c) * Rot(0, 90, 0) * Cylinder(
        s.hose_id / 2, spigot + 2, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    part -= bore
    for yy, zz in f["holes"]:
        part -= Pos(x_f - s.flange_t / 2, yy, zz) * Rot(0, 90, 0) * Cylinder(
            s.bolt_dia / 2, 2 * s.flange_t + 6, align=(Align.CENTER, Align.CENTER, Align.CENTER)
        )
    return part


def vortex_finder(s: Spec):
    """Separate tube so `De` can be re-tried without reprinting the body (P8.61, F2)."""
    up = (Align.CENTER, Align.CENTER, Align.MIN)
    stub = 45.0
    total = s.S + s.wall + stub
    t = Cylinder(s.De / 2 + s.wall, total, align=up) - Cylinder(s.De / 2, total, align=up)
    # collar that lands on the roof
    t += Pos(0, 0, s.S) * Cylinder(s.De / 2 + s.wall + s.flange_w / 2, s.wall, align=up)
    t -= Pos(0, 0, s.S - 1) * Cylinder(s.De / 2, s.wall + 2, align=up)
    return t


def lid_socket(s: Spec):
    """Bolts through the drum lid; receives the cone tip and reinforces the hole.

    Not a stiffener - the lid does not need one (P4.92). This spreads the cyclone's
    weight and restores membrane continuity around the cut-out.
    """
    up = (Align.CENTER, Align.CENTER, Align.MIN)
    r_tip_o = s.B / 2 + s.wall
    plate_r = s.socket_od / 2
    collar_h = 20.0
    part = Cylinder(plate_r, s.flange_t, align=up)
    part += Pos(0, 0, s.flange_t) * Cylinder(r_tip_o + s.wall + s.fit + 2, collar_h, align=up)
    part -= Cylinder(r_tip_o + s.fit, s.flange_t + collar_h + 1, align=up)
    pcd = plate_r - 14
    for i in range(s.socket_bolts):
        ang = 2 * math.pi * i / s.socket_bolts
        part -= Pos(pcd * math.cos(ang), pcd * math.sin(ang), -1) * Cylinder(
            s.socket_bolt_dia / 2, s.flange_t + 2, align=up
        )
    return part


def drill_pattern(s: Spec) -> str:
    """What to cut in the steel drum lid."""
    pcd = s.socket_od / 2 - 14
    bore = s.B + 2 * s.wall + 2 * s.fit + 4
    return "\n".join(
        [
            f"- Centre hole **{bore:.0f} mm dia** (cone tip clearance)",
            f"- {s.socket_bolts} x {s.socket_bolt_dia:.1f} mm holes on a "
            f"**{2*pcd:.0f} mm bolt circle**",
            "- Deburr both sides. The hole edge is the one stress raiser in the lid,",
            "  which is why the socket flange bolts around it (P4.95).",
        ]
    )


# --------------------------------------------------------------------------- build


PRESETS = {
    "build1": Spec(name="build1"),
    # Build-2 target (P8.91, D1). Deferred until the LVHP system exists (D9).
    # O1: vin 17.4 m/s, 7% over 1D3D design velocity - judged acceptable (D2).
    "build2": Spec(
        name="build2",
        D=240.0,
        Q_cfm=265.0,
        hose_id=88.9,
        accepted=frozenset({"O1", "S8"}),
    ),
    # SC0075 HVLP duty (phase-12). Pressure is the scarce axis (P12.01): vin sits
    # at the LOW end of O1 so cyclone dp stays ~3" H2O (P12.04). Q=350 CFM is
    # provisional pending measured flow (P12.02, Q-H1). De/D=0.50 is the dp-relief
    # ceiling under G4. Barrel courses exceed the bed -> arc split (P12.06).
    "sc0075": Spec(
        name="sc0075",
        D=325.0,
        Q_cfm=350.0,
        hose_id=100.0,
        accepted=frozenset({"S8"}),
    ),
}


def build(s: Spec, outdir: Path, step: bool = True) -> list[Path]:
    outdir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    parts = body_courses(s)
    parts["vortex_finder"] = vortex_finder(s)
    parts["lid_socket"] = lid_socket(s)
    if s.needs_arc_split:
        parts["inlet_duct"] = inlet_duct(s)
    for name, shape in parts.items():
        p = outdir / f"{name}.stl"
        export_stl(shape, str(p))
        written.append(p)
        if step:
            ps = outdir / f"{name}.step"
            export_step(shape, str(ps))
            written.append(ps)
    rp = outdir / "report.md"
    rp.write_text(report(s), encoding="utf-8")
    written.append(rp)
    return written


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--preset", default="build1", choices=sorted(PRESETS))
    ap.add_argument("--out", default=None)
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--De-ratio", type=float, default=None)
    ap.add_argument("--cfm", type=float, default=None)
    args = ap.parse_args()

    s = PRESETS[args.preset]
    if args.De_ratio is not None:
        s = replace(s, De_r=args.De_ratio)
    if args.cfm is not None:
        s = replace(s, Q_cfm=args.cfm)

    print(report(s))
    failed = [c for c, ok, _ in check(s) if not ok and c in GATES and c not in s.accepted]
    if args.check_only:
        return 1 if failed else 0
    if failed:
        print(f"\n!! {len(failed)} constraint(s) failed: {', '.join(failed)}")
        print("   Generating anyway - review the report before printing.\n")
    out = Path(args.out or f"out/{s.name}")
    for p in build(s, out):
        print(f"  wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
