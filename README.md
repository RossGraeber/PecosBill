# PecosBill

Parametric cyclonic dust separator for a CNC router vacuum line.

- **Stage 1 — research (complete):** [`docs/research/`](docs/research/) — 460 claim-ID'd findings
  with confidence tiers, a contradiction log, and the constraint set the generator enforces.
  Start at [`docs/research/README.md`](docs/research/README.md).
- **Stage 2 — generator (in progress):** [`cyclone.py`](cyclone.py) emits STL + STEP + a report
  from a parameter set. The printed part is fixed and simple; the flexibility lives here.

## Use

```bash
uv run python cyclone.py --preset build1          # generate into out/build1/
uv run python cyclone.py --check-only             # constraints only, no geometry
uv run python cyclone.py --cfm 45 --De-ratio 0.48 # sweep a parameter
uv run python test_cyclone.py                     # self-check
```

`--check-only` exits non-zero if a gate fails, so it drops into CI or a pre-print hook.

## Current target — build 1

Sized for a RIDGID WD06701 shop vac at an **estimated** 55 CFM (no flow meter available; the real
band is 40–70 CFM, which puts `vin` anywhere in 10.8–19.0 m/s — see `D7`). Build 1 is a validation
article, not the production separator: its first job is to tell us which end of that band we are on.

| | |
|---|---|
| Family | 1D3D (Texas A&M) |
| Body `D` | 118 mm |
| `x50` | ~3.4 µm (Lapple, ±50 %) |
| Δp | 4.3" H₂O |
| Height | 472 mm, 2 printed courses |
| Filament | ~740 g PETG (solid perimeters, 0 % infill) |
| Vessel | Greif 30-gal open-head steel drum |

Build 2 (`D` = 240 mm at 265 CFM, the boot's ceiling) is deferred until the LVHP vacuum system is
designed. Its preset exists and passes its constraint checks, but generation is **refused** — it
needs arc-splitting, which is specified (`P8.103`) and not yet implemented.

## Output

```
out/build1/
  body_course_01.stl/.step   lower cone + register boss
  body_course_02.stl/.step   upper cone + barrel + tangential inlet + roof
  vortex_finder.stl/.step    separate, so De can be re-tried without reprinting the body
  lid_socket.stl/.step       bolts through the drum lid, receives the cone tip
  report.md                  dimensions, performance, constraint results
```

## Before printing

1. Cut the drum lid per the drill pattern in `report.md`. Deburr both sides — the hole edge is the
   only stress raiser in the lid (`P4.95`).
2. Fit a relief valve. It no longer protects the lid (it does not need protecting, `P4.94`) but it
   still caps the load on the printed parts and the vacuum motor (`P4.85`, `P4.99`).
3. Check the drum's closure gasket. A rim-clamped bag liner later depends on the vessel being
   genuinely airtight (`P4.73`, `P7.14`).
