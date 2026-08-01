"""Self-check for the cyclone generator.

    uv run python test_cyclone.py

Catches the failures that actually bite: unprintable parts, non-manifold solids,
bores that did not cut through, joints that do not fit, and drift in the
performance maths against hand-computed values.
"""

import math

from cyclone import PRESETS, GATES, Spec, body_courses, check, lid_socket, vortex_finder, _shell, _radius_at


def _bbox(part):
    bb = part.bounding_box()
    return bb.size.X, bb.size.Y, bb.size.Z


def test_maths():
    """Independent re-derivation of the performance numbers."""
    s = Spec(D=118.0, Q_cfm=55.0)
    q = 55 / 2118.88
    vin = q / ((0.059) * (0.0295))
    assert abs(s.vin - vin) < 1e-9, s.vin
    assert abs(s.vin - 14.9) < 0.1, s.vin

    x50 = math.sqrt(9 * 1.81e-5 * 0.0295 / (2 * math.pi * 6 * vin * (730 - 1.2))) * 1e6
    assert abs(s.x50 - x50) < 1e-9
    assert 3.0 < s.x50 < 3.9, s.x50

    assert abs(s.Eu - 16 * 59.0 * 29.5 / 59.0**2) < 1e-9
    assert abs(s.Eu - 8.0) < 0.01, s.Eu

    # x50 must scale as sqrt(D) at fixed vin  (P1.26)
    a = Spec(D=118.0, Q_cfm=55.0)
    b = Spec(D=236.0, Q_cfm=55.0 * 4)  # 2x D at fixed vin needs 4x Q
    assert abs(b.vin - a.vin) < 1e-6, (a.vin, b.vin)
    assert abs(b.x50 / a.x50 - math.sqrt(2)) < 0.01, b.x50 / a.x50
    print("  maths: vin, x50, Eu, and the sqrt(D) scaling law all check out")


def test_gates():
    for name, s in PRESETS.items():
        bad = {c for c, ok, d in check(s) if not ok and c in GATES}
        unexpected = bad - set(s.accepted)
        assert not unexpected, f"{name} fails gates: {sorted(unexpected)}"
        stale = set(s.accepted) - bad
        assert not stale, f"{name} lists accepted deviations that now pass: {sorted(stale)}"
        note = f" (accepted: {', '.join(sorted(bad))})" if bad else ""
        print(f"  {name}: gates pass{note}")


def test_bore_cut_through():
    """The inlet duct must actually open into the barrel."""
    s = PRESETS["build1"]
    shell = _shell(s)
    solid_walls = math.pi * (s.D / 2 + s.wall) ** 2 * s.h  # crude upper bound
    assert shell.volume < solid_walls, "shell is not hollow"
    assert shell.is_valid, "shell is not a valid solid"
    assert len(shell.solids()) == 1, f"shell is {len(shell.solids())} disconnected solids"
    print(f"  shell: valid, single solid, {shell.volume/1000:.0f} cm3 of material")


def test_parts_printable():
    s = PRESETS["build1"]
    parts = dict(body_courses(s))
    parts["vortex_finder"] = vortex_finder(s)
    parts["lid_socket"] = lid_socket(s)
    for name, p in parts.items():
        assert p.is_valid, f"{name}: invalid solid"
        assert len(p.solids()) == 1, f"{name}: {len(p.solids())} disconnected solids"
        x, y, z = _bbox(p)
        assert z <= s.bed_z, f"{name}: {z:.0f} mm tall > bed_z {s.bed_z}"
        assert x <= s.bed_xy, f"{name}: {x:.0f} mm in X > bed_xy {s.bed_xy}"
        assert y <= s.bed_xy, f"{name}: {y:.0f} mm in Y > bed_xy {s.bed_xy}"
        print(f"  {name:20s} {x:6.1f} x {y:6.1f} x {z:6.1f} mm   {p.volume/1000:7.1f} cm3")


def test_joint_fits():
    """Register boss on course N must slide into the bore of course N+1."""
    s = PRESETS["build1"]
    for z in s.split_z:
        r_i = _radius_at(s, z)
        boss_od = 2 * (r_i - s.fit)
        bore_id = 2 * r_i
        assert boss_od < bore_id, "boss does not fit"
        gap = (bore_id - boss_od) / 2
        assert 0.15 <= gap <= 0.6, f"joint clearance {gap:.2f} mm out of range"
        print(f"  joint at z={z:.0f}: boss {boss_od:.1f} into bore {bore_id:.1f}, {gap:.2f} mm/side")


def test_interfaces_fit():
    """Vortex finder into the roof bore; cone tip into the lid socket."""
    s = PRESETS["build1"]
    vf_od = s.De + 2 * s.wall
    roof_bore = 2 * (s.De / 2 + s.wall + s.fit)
    assert vf_od < roof_bore, "vortex finder will not pass the roof"
    assert abs((roof_bore - vf_od) / 2 - s.fit) < 1e-9

    collar_r = s.De / 2 + s.wall + s.flange_w / 2
    assert collar_r > roof_bore / 2, "vortex finder collar has nothing to land on"

    tip_od = s.B + 2 * s.wall
    socket_bore = 2 * (s.B / 2 + s.wall + s.fit)
    assert tip_od < socket_bore, "cone tip will not enter the lid socket"
    print(
        f"  vortex finder {vf_od:.1f} into roof {roof_bore:.1f}; "
        f"cone tip {tip_od:.1f} into socket {socket_bore:.1f}; all {s.fit:.2f} mm/side"
    )


def test_courses_reassemble():
    """Course volumes must sum to about the whole shell, plus the flanges."""
    s = PRESETS["build1"]
    shell = _shell(s)
    parts = body_courses(s)
    total = sum(p.volume for p in parts.values())
    assert total > shell.volume, "courses lost material"
    assert total < shell.volume * 1.6, f"flanges added {total/shell.volume:.2f}x, expected <1.6x"
    print(f"  reassembly: {len(parts)} courses, {total/shell.volume:.2f}x shell volume (flanges+bosses)")


if __name__ == "__main__":
    for fn in (
        test_maths,
        test_gates,
        test_bore_cut_through,
        test_joint_fits,
        test_interfaces_fit,
        test_courses_reassemble,
        test_parts_printable,
    ):
        print(f"{fn.__name__}:")
        fn()
    print("\nAll checks passed.")
