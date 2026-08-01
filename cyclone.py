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
        f"arc split {'REQUIRED' if s.needs_arc_split else 'not needed'}",
        f"- Course splits at z = {', '.join(f'{z:.0f}' for z in s.split_z) or 'n/a'} mm above cone tip",
        f"- Flange OD {s.D+2*s.wall+2*s.flange_w:.0f} mm, {s.n_bolts} x M4",
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
        "| `body_course_01` | wide end down | cone narrows upward at "
        f"{s.cone_semi_angle:.1f} deg - self-supporting |",
        "| `body_course_02` | **roof down** | flat face, best adhesion; the inlet duct "
        f"bridges {s.b:.0f} mm |",
        "| `vortex_finder` | collar down | |",
        "| `lid_socket` | plate down | |",
        "",
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


def _shell(s: Spec):
    """Solid body: cone + barrel + roof + tangential inlet, bored out."""
    ri_tip, ri_body = s.B / 2, s.D / 2
    z_j, z_top = s.cone_h, s.H  # junction, roof underside

    up = (Align.CENTER, Align.CENTER, Align.MIN)
    outer = Cone(ri_tip + s.wall, ri_body + s.wall, z_j, align=up)
    outer += Pos(0, 0, z_j) * Cylinder(ri_body + s.wall, s.h + s.wall, align=up)

    # tangential inlet: outer wall of the duct is tangent to the barrel bore.
    y_c = ri_body - s.b / 2
    z_c = z_top - s.a / 2
    # Area-matched rect->round morph, not a diffuser: 29.5x59 = 1740 mm2 vs
    # a 47.6 dia round = 1780 mm2. Kept short so the course fits the bed in X.
    duct_len = s.a
    spigot = 25.0
    # The rect section must sit INSIDE the barrel wall: a union across exactly
    # coincident faces leaves two disconnected solids (OCCT), so overlap by 2*wall.
    x_rect = -(ri_body + s.wall) + 2 * s.wall
    x_round = x_rect - duct_len
    x_end = x_round - spigot

    # outer duct
    pl_r_o = Plane(origin=(x_rect, y_c, z_c), z_dir=(1, 0, 0))
    pl_c_o = Plane(origin=(x_round, y_c, z_c), z_dir=(1, 0, 0))
    outer += loft(
        [pl_r_o * Rectangle(s.b + 2 * s.wall, s.a + 2 * s.wall),
         pl_c_o * Circle(s.hose_id / 2 + s.wall)]
    )
    outer += Pos(x_end, y_c, z_c) * Rot(0, 90, 0) * Cylinder(
        s.hose_id / 2 + s.wall, spigot, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )

    # ---- bores ----
    inner = Cone(ri_tip, ri_body, z_j, align=up)
    inner += Pos(0, 0, z_j) * Cylinder(ri_body, s.h, align=up)

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

    body = outer - inner
    # vortex finder bore through the roof, with print clearance for a separate tube
    body -= Pos(0, 0, s.H - s.S) * Cylinder(
        s.De / 2 + s.wall + s.fit, s.S + s.wall + 1, align=up
    )
    return body


def _flange(s: Spec, z_lo: float, r_inner: float):
    """Annular flange occupying z_lo .. z_lo+flange_t, bored to r_inner, with bolt holes."""
    up = (Align.CENTER, Align.CENTER, Align.MIN)
    r_o = s.D / 2 + s.wall + s.flange_w
    fl = Pos(0, 0, z_lo) * Cylinder(r_o, s.flange_t, align=up)
    fl -= Pos(0, 0, z_lo - 1) * Cylinder(r_inner, s.flange_t + 2, align=up)
    pcd = s.D / 2 + s.wall + s.flange_w / 2
    for i in range(s.n_bolts):
        ang = 2 * math.pi * i / s.n_bolts
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


def body_courses(s: Spec) -> dict:
    """Split the shell into printable courses joined by butt flanges + a register boss."""
    shell = _shell(s)
    zs = s.split_z
    if not zs:
        return {"body": shell}

    up = (Align.CENTER, Align.CENTER, Align.MIN)
    reg_h = 8.0
    total = s.H + s.wall
    bounds = [0.0] + list(zs) + [total]
    parts: dict = {}

    for i in range(len(bounds) - 1):
        lo, hi = bounds[i], bounds[i + 1]
        seg = shell
        if lo > 0:
            seg = _largest(seg.split(Plane.XY.offset(lo), keep=Keep.TOP))
        if hi < total:
            seg = _largest(seg.split(Plane.XY.offset(hi), keep=Keep.BOTTOM))

        if lo > 0:  # bottom flange of this course
            seg += _flange(s, lo, _radius_at(s, lo))
        if hi < total:  # top flange + register boss that plugs into the next course
            seg += _flange(s, hi - s.flange_t, _radius_at(s, hi - s.flange_t))
            r_i = _radius_at(s, hi)
            boss = Pos(0, 0, hi) * Cylinder(r_i - s.fit, reg_h, align=up)
            boss -= Pos(0, 0, hi - 1) * Cylinder(r_i - s.fit - s.wall, reg_h + 2, align=up)
            seg += boss

        parts[f"body_course_{i+1:02d}"] = seg
    return parts


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
    # S8: needs arc splitting, which is specified (P8.103) but NOT YET IMPLEMENTED.
    "build2": Spec(
        name="build2",
        D=240.0,
        Q_cfm=265.0,
        hose_id=88.9,
        accepted=frozenset({"O1", "S8"}),
    ),
}


def build(s: Spec, outdir: Path, step: bool = True) -> list[Path]:
    if s.needs_arc_split:
        raise NotImplementedError(
            f"{s.name}: flange OD {s.D+2*s.wall+2*s.flange_w:.0f} mm exceeds the "
            f"{s.bed_xy:.0f} mm bed. Arc splitting is specified (P8.103) but not yet "
            "implemented - refusing to emit parts that will not print."
        )
    outdir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    parts = body_courses(s)
    parts["vortex_finder"] = vortex_finder(s)
    parts["lid_socket"] = lid_socket(s)
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
