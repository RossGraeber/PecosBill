# Phase 10 — Design-space synthesis

**This is not a design.** No dimensions are chosen. This file states the constraint set, the free
variables, the decision criteria, and the questions Stage 2 must answer before any geometry exists.

## 10.1 Blocking open questions

Stage 2 cannot start until these are answered. Each changes the answer materially.

| # | Question | Why blocking | Ref |
|---|---|---|---|
| ~~`Q1`~~ | ~~Shop vac or dust collector?~~ **RESOLVED 2026-07-29: shop vac.** Consequences in [§10.8](#108-consequences-of-q1--shop-vac) and phase-08 §8.6. | — | `P8.36`–`P8.53` |
| ~`Q2`~ | Target flow `Q` and hose diameter | **NARROWED 2026-07-29:** RIDGID WD06701, 40–70 CFM through a 1-7/8" hose. `D` moves only 100→133 mm across that band, so it is no longer design-blocking. Measuring actual flow is now a refinement, not a gate. | `P8.54`–`P8.60` |
| `Q3` | Objective: **filter protection** (maximise g/kg removed) or **fine-dust capture** (minimise `x50`)? | Selects the point on the `De/D` Pareto front. These are different machines. | `P3.01`, `P3.05`, `P8.23` |
| ~~`Q4`~~ | ~~Print envelope~~ **RESOLVED: Bambu Lab P1S**, 256³ nominal / 250 mm usable Z, ~240–250 mm max circular footprint, enclosed (ASA available). Not binding at `D ≈ 120 mm`. | — | `P8.68`–`P8.72` |
| ~~`Q5`~~ | ~~Collection vessel~~ **RESOLVED 2026-08-01: 2 × Greif 30-gal open-head steel drum** (UN `1A2/X400/S/26` + `1A2/Y1.4/150/26`), flat plain lid with rolled edge, bolt ring, gasket. Body ×16 safe; **the flat lid is the weak part** — permanent set ~9 kPa, gasket-unseating dish at ~3.5 kPa. Two drums = swap workflow, which reverses the earlier 'avoid 20–30 gal' verdict (`P4.86`). Open action: confirm prior contents before use (`P4.91`). | — | `P4.78`–`P4.91` |
| ~~`Q6`~~ | ~~Hobby or commercial use~~ **RESOLVED 2026-08-01: hobbyist operating a commercial machine** (Signstech N1313, 4×4 ft, 3 HP spindle). NFPA 664/660 are facility-scoped → no legal obligation, but the quantity margin that makes hobby dust safe thins to 5–16× (`P8.74`); housekeeping and fire load matter. **Bigger finding: capture, not separation, is the binding problem** — the vac is ~11× short of the CFM this machine needs (`P8.81`). | — | `P8.73`–`P8.88` |

## 10.2 Constraint set (binding)

Assembled from phases 2, 4, 5, 7, 8. Any candidate violating these is outside validated practice.

```
# --- Geometry (Tier A unless noted; source L-SALCEDO01 unless noted) ---
G1  S < h < H
G2  6.8 deg  <  cone semi-angle eps  <= 16 deg          # included angle 13.6-32 deg
G3  0.5  <  (a*b) / ((pi/4)*De**2)  <  0.735            # CORRECTED form, see P2.21
G4  0.5*De  <  B  <  De
G5  0.5*(D - De)  >  b
G6  S > 1.25*a                                          # PREFERENCE not gate (P2.23): Stairmand HE violates it
G7  2.3*De*(D**2/(a*b))**(1/3)  <=  H - S               # Alexander natural length must fit  (P4.02)
G8  H/D ~ 4                                             # interior optimum, 3 independent confirmations (P3.06)

# --- Operating point ---
O1  vin  in [12, 17] m/s                                # family design velocities (P1.33)
O2  vin / vs  <= 1.25                                   # saltation ceiling (P1.32)
O3  vin is set by choosing a*b, NOT inherited from duct velocity   (P8.16, V9.10)
O4  duct velocity elsewhere in the system >= 17.8 m/s main / 20.3 m/s branch  (P8.11)
    -> the cyclone inlet is a DIFFUSER from the duct

# --- Manufacture ---
M1  size the shell for BUCKLING, not hoop stress        (P7.01)
M2  stiffening rings preferred over uniform thickening  (P7.03)
M3  wall >= 1.2-1.6 mm, 3-5 perimeters, no vase mode    (P7.10)
M4  perimeters and flow are the dominant sealing parameters  (P7.11)
M5  bin must survive full blockage at max source suction: 13-22 kPa       (P7.07, P8.52)
M7  pressure boundary must be a CYLINDER, not a flat-panel box            (P4.62, P4.68)
M8  inner/liner containers are pressure-neutral -> zero strength required (P4.69, P4.73)
    and a bag liner is stable ONLY if the vessel is genuinely airtight
M9  the drum LID is the structural deliverable, not the cyclone shell     (P4.82)
    cyclone mounting flange doubles as the lid stiffener; ribs to the ring (P4.84)
M10 fit a relief/bleed valve capping vacuum below ~9 kPa                   (P4.85)
M6  support-free printability is a design objective, not post-hoc  (P7.26)
```

## 10.3 Variable classification

| Variable | Class | Basis |
|---|---|---|
| `De/D` | **Master trade** — sets both `Eu` and `Stk50`; sweep 0.40 (fine cut, high Δp) ↔ 0.75 (low Δp, coarse cut) | `P3.05`, `P5.15` |
| `H/D` | Fixed at ≈4 unless `Ln` says otherwise | `P3.06`, `G7`, `G8` |
| `h/D` | **Free** — negligible objective sensitivity; spend it on print-bed height and bin clearance | `P3.08`, `P3.12` |
| `b/D` | Secondary trade; matters more than `a` for cut size | `P2.11` |
| `a/D` | Set jointly with `b` to hit `O1` at the chosen `Q` | `O3` |
| `S/D` | Constrained between short-circuit (`G6`) and vortex length (`G7`); optimisers can't see the trade | `P3.07`, `P5.21`–`P5.24` |
| `B/D` | Constrained by `G4`; smaller helps efficiency at little Δp cost while `B > De` | `P2.15`, `G4` |
| Separation **length below the vortex finder** | **Highest-leverage free variable.** Varies 2.5× at constant Δp with a non-monotonic cut-size optimum | `P4.08`, `P4.09`, `P4.26` |
| Cone presence | Required. Straight-tube substitution measurably fails on fines | `P2.16` |
| Inlet topology | Volute/vane ↑ efficiency ↑ Δp; helical ↓ both. Printing makes volute cheap that is expensive in sheet metal | `P5.02`, `P5.03`, `P5.13` |
| Wall texture | Direction disputed; do not deliberately roughen | `V9.09` |

## 10.4 Ranked design leverage

From the corpus, in descending order of measured or derived effect on delivered performance:

| Rank | Lever | Evidence | Note |
|---|---|---|---|
| 1 | **Get the operating point right** (`vin` in band, no leaks, no flex-hose restriction) | `P8.28` (+6–17 % airflow from one leak fix), `P1.31`–`P1.35`, `P8.32` (99.99 %→92.8 % on feed rate alone) | Larger than any geometry change reported anywhere in this corpus |
| 2 | **Prevent bin-side re-entrainment** (bin size, shape, fill headroom, isolation) | `P4.10`–`P4.14`, `P6.09`, `P6.20` | The dominant unmodelled loss path |
| 3 | **Match separation length to natural vortex length** | `P4.08` (cut size has a minimum in `L`), `P2.17`, `P4.09` | Free — costs no pressure drop |
| 4 | **Choose `De/D` deliberately** against the stated objective | `P3.05` (Eu ×3.9 for cut ÷5.5) | The only knob that moves both objectives hard |
| 5 | Series staging | `P6.04`–`P6.07` (9–15 g/kg → ~1 g/kg) | Better return than perfecting one stage |
| 6 | Inlet volute / neutral vane | `P5.02`, `P5.11`–`P5.13` | Real mechanism, unquantified magnitude |
| 7 | Body ratio fine-tuning within a classical family | `P2.08` (≤1.4 pp spread across 1D3D/2D2D/1D2D) | Smallest lever; do not over-invest |
| 8 | Parallel arrays | `P6.01` (4× parts for 1.41× cut size), `P6.10`, `P6.24` | Negative expected value at small scale unless underflows are isolated |

## 10.5 Candidate architectures carried forward

Recorded for evaluation, not selected.

| ID | Architecture | For | Against | Key refs |
|---|---|---|---|---|
| `A1` | **Single classical reverse-flow cyclone**, Stairmand-HE or 1D3D family, printed in stacked modules | Best-validated geometry; direct model support; simplest | Fixed length ⇒ optimal at one flow only (`P3.18`); commercial equivalents already exist | `P2.02`, `P2.08` |
| `A2` | **Length-modular cyclone** — `A1` plus stackable barrel/cone extension sections | Converts the print-splitting constraint into the `P4.09` tuning mechanism at zero Δp cost; lets Stage 3 find the length optimum empirically | More joints ⇒ more leak paths (`P7.14`); joints add roughness discontinuities | `P4.08`, `P7.25` |
| `A3` | **Karagöz double-cylinder + adjustable vortex limiter** (no cone) | Directly addresses the two dominant loss paths (`P4.23`, `P4.24`); length adjustable in service; friction surface ≠ separation surface, which suits rough FDM walls; concentric cylinders are the easiest thing to print | Single primary source; tested at `D=250 mm` on cement (`ρp` ≫ wood); **`P2.16` says a cone is needed for fines** and this design has none — apparent conflict, see note below | `S-KARAGOZ13`, `P2.25`, `P7.22` |
| `A4` | **Cyclone + fine second stage** in series | Largest measured real-world gain (`P6.07`); lets stage 1 be sized for chips and stage 2 for fines | Two devices, two bins, more Δp, more to empty | `P6.03`–`P6.08` |
| ~~`A5`~~ | ~~Multicyclone array~~ **REJECTED** (`D1`) | The `S-MTL` approach; theoretically correct scaling | `P6.10`, `P6.21`, `P6.24` all point against it at this scale with a shared hopper | phase-06 §6.1–§6.4 |

> **Note on `A3` vs `P2.16`:** these are not necessarily in conflict. `P2.16` removed the cone from a
> conventional cyclone *without* replacing its function; `A3` replaces the cone's function (terminating
> and reversing the vortex at a controlled height) with the limiter plate. This distinction is
> untested and should be treated as `A3`'s primary risk. Logged as an extension of `V9.07`.

## 10.11 Architecture SELECTED (2026-08-01)

**Decision: option (a) — a single reverse-flow cyclone, printed in circumferential courses,
discharging into one steel drum, with the second drum as a swap spare.**
`A5` (parallel array) is rejected. `U5` is moot — there is one underflow.

### Family and proportions

**1D3D** (Texas A&M agricultural lineage), chosen over Stairmand HE because:
it measured best of the three TAMU families on real dusts (`P2.08`); it was developed for
trash-plus-fines feeds, which is the CNC case (`P8.01`, `P1.45`); its long 3D cone suits `P2.15`;
and its 16.3 m/s design velocity is the closest of any family to what the boot forces (`P8.90`).

| Ratio | Value |
|---|---|
| `a/D` | 0.50 |
| `b/D` | 0.25 |
| `De/D` | **0.45–0.50** (`P8.61` — flow is scarcer than pressure in LVHP) |
| `S/D` | 0.50 |
| `h/D` | 1.0 |
| cone | 3.0 D |
| `H/D` | 4.0 |
| `B/D` | 0.25 |

### Two build stages, one generator

| | Build 1 — shop vac | Build 2 — LVHP |
|---|---|---|
| Flow | 55 CFM (band 40–70) | 265 CFM (boot ceiling, `P8.91`) |
| **`D`** | **118 mm** | **240 mm** |
| `vin` | 14.9 m/s (10.8–19.0 across the band) | 17.4 m/s |
| `x50` | 3.42 µm | 4.53 µm |
| `H` | 472 mm | 960 mm |
| inlet `a × b` | 59 × 29.5 mm | 120 × 60 mm |
| `De` at 0.45 | 53 mm | 108 mm |
| cone tip `B` | 29.5 mm | 60 mm |
| Courses at 250 mm Z | **2** | **4** |
| Arc segments | none | **none** |
| Δp at `De/D`=0.45 | ~1.6" H₂O | 7.2" H₂O |
| Inlet vs boot area | 0.28× (no diffuser) | 1.16× (mild expansion) |

| ID | Claim | Tier |
|---|---|---|
| `D1` | **`D` = 240 mm rather than 258 mm is strictly better.** It fits the P1S in XY (240 mm circle centred on a 256 mm bed clears the front-left exclusion by 61 mm), so **no arc segments are needed at either stage** — only circumferential courses. And because `x50 ∝ √(D/vin)`, running smaller and faster *improves* the cut size: **4.53 µm vs 5.04 µm**. | E (verified) |
| `D2` | Cost of `D1`: `vin` = 17.4 m/s, which is 7 % above the 1D3D design velocity and ~2 % above the `O1` band ceiling — i.e. on the re-entrainment side of the optimum (`P1.31`, `P1.33`). Judged acceptable; it is the single item to watch in build-2 testing. | E |
| `D3` | If the machine's usable XY proves to allow ~248 mm, `D` = 246–250 mm brings `vin` back to 16.0–16.5 m/s (dead on 1D3D design) at a small `x50` cost. **Measure the real usable bed before finalising build 2.** | E |
| `D4` | ~~Measure the vac's flow before finalising build 1.~~ **CLOSED 2026-08-01: no measurement available; the 55 CFM estimate is adopted as the design flow.** `D` = 118 mm stands. | E |
| `D7` | **Residual risk of `D4`, stated openly.** Across the real 40–70 CFM band `vin` is 10.8–19.0 m/s. At the low end the cyclone runs cold (below `O1`, weak centrifugal field, coarse cut); at the high end hot (past the band, re-entrainment side of `P1.31`). Build 1 is a validation article (`P8.83`), so this is acceptable — **its first job is to tell us which end we are on.** | E |
| `D8` | Cheap hedge that respects `F2` (no physical adjustability): the inlet/roof is already a course boundary, so **a re-tuned inlet can be reprinted alone** without reprinting the cone. Note the caveat — changing `a·b` at fixed `D` moves off 1D3D proportions and forfeits that family's empirical backing (`P2.08`). Prefer regenerating the whole body at a corrected `D`; printing is the cheap part. | E |
| `D9` | **Build 2 deferred** until the LVHP vacuum system itself is designed. Its parameters (`D` = 240 mm, 265 CFM) are recorded as a target for the generator to satisfy, not as work in progress. The generator must therefore carry build 2's cases — 4 courses, 1.16× inlet diffusion, and arc-splitting (`P8.103`) — even though build 1 exercises none of them. | E |
| `D5` | Both stages use only **circumferential flanged joints**, which are free stiffening rings (`P8.99`) and keep every seam perpendicular to the swirl rather than running through it (`P8.102`). The generator still needs arc-splitting (`P8.103`) for future flexibility, but neither current build exercises it. | E |
| `D6` | The second drum is a **swap spare** (`P4.86`), not a second underflow. Underflow isolation (`P6.20`, `U4`, `U5`) is no longer a live constraint. | E |

## 10.10 Where the flexibility lives — binding directive

**Stated by the user, 2026-07-29: flexibility belongs in the code, not in the cyclone.**

| ID | Directive | Consequence |
|---|---|---|
| `F1` | The **generator is parametric and reusable**; the **printed artefact is fixed and simple**. | Stage 2's primary deliverable is a parametric model that emits STLs, not a family of adjustable parts. |
| `F2` | Do not build physical adjustability into the cyclone. | Length, `De/D`, cone angle, inlet size are **code parameters explored by regeneration and reprinting**, not field-adjustable hardware. |
| `F3` | Print-driven splits are still required; tuning-driven splits are not. | `A2` survives — but only because `H ≈ 480 mm` exceeds the 250 mm Z cap (`P8.70`). It is a **print split**, not a tuning mechanism. Minimise joints: fewer joints = fewer leak paths (`P7.14`) and fewer roughness discontinuities. |
| `F4` | `A3`'s headline feature was an **adjustable** vortex limiter (`P3.17`). | `A3` **downgraded**. Its topology may still be worth evaluating in code, but its main advantage is now out of scope. Fixed-limiter variants can be generated and printed like any other parameter set. |
| `F5` | Scaling to LVHP is by unit count (`U3`), which is itself a code parameter. | The same generator emits the single-unit build and the *n*-unit array. No second design effort. |
| `F6` | Reusability target is the **model**, not the part. | Value of the corpus's ratio tables, constraint set (`§10.2`) and scaling laws is that they encode directly as generator constraints and assertions. |

**Practical reading:** the earlier framing of length-modularity as "free tuning" (`P4.09`, `P7.25`,
`A2`) is superseded. Length remains the highest-leverage variable — it is now explored by *changing a
number and reprinting*, which on a P1S is cheap. That is strictly simpler than a field-adjustable
mechanism and gives the same design freedom.

## 10.6 What Stage 2 should produce first

Derived from `V9.17` (measurement is the binding constraint on iteration) and §10.4 rank 1:

Revised after `F1`–`F6` and the `Q1`/`Q2`/`Q4`/`Q5` resolutions:

1. **A parametric generator** — ratios → dimensions → STL. Inputs: `Q`, `vin`, family ratios,
   `De/D`, wall/rib parameters, module Z cap. It should *assert* the `§10.2` constraint set
   (`G1`–`G8`, `S1`–`S9`) and refuse geometry that violates it. This is the reusable artefact (`F1`, `F6`).
2. **The bucket lid** as the first structural design (`P4.38`) — it carries the cyclone, takes the
   full vacuum load, and forms the seal. Highest failure probability of anything in build 1.
3. **A measurement plan before more geometry** — what is weighed, on what instrument, at what
   resolution, against what feed mass, sized so any claim sits above the noise floor. `V9.11` is
   where every DIY effort in this corpus failed.
4. Only then: the first fixed geometry — `D ≈ 120 mm`, `De/D` 0.45–0.50, `H ≈ 480 mm` in 2 modules.

`Q3` and `Q6` remain open but neither blocks step 1.

## 10.8 Consequences of `Q1` = shop vac

Full derivation and verification in phase-08 §8.6. Effects on the rest of this file:

### Constraint set changes

```
# SUPERSEDED
O1  vin in [12,17] m/s        -> unchanged, but now reachable at D = 110-220 mm  (P8.41)
M5  bin survives full blockage-> LOAD RAISED to 13-22 kPa, was ~2.5 kPa          (P8.52)

# ADDED
S1  D in [110, 220] mm at vin = 15 m/s over the 50-150 CFM band                  (P8.41)
S2  H = 4*D  =>  450-870 mm  =>  length-module splitting is MANDATORY            (P8.42)
S3  hose diameter is a coupled design variable, not a given:
      2.5" needs 136 CFM for transport velocity; 2.0" needs 87; 1.5" needs 49    (P8.45)
S4  inlet-area == hose-area is valid ONLY at 2.5" hose near 100 CFM;
      at 2.0" hose the inlet must diffuse                                        (P8.46)
S5  design load case = blocked hose, motor running (routine with a dust shoe)    (P8.53)
```

### Leverage ranking changes (§10.4)

| Rank | Was | Now | Why |
|---|---|---|---|
| 4 → **2** | Choose `De/D` deliberately | **promoted** | Δp is ~10 % of available sealed pressure; narrowing `De/D` 0.5→0.35 costs ~6" H₂O of 53–90". The efficiency end of the Pareto front is affordable in this regime and was not in the other (`P8.43`) |
| 1 | Operating point | **unchanged, rank 1** | Now concretely = hose sizing + leak sealing (`P8.45`, `P8.47`) |
| 2 → 3 | Bin re-entrainment | unchanged in importance, **plus** it is now the governing structural part (`P8.52`) |
| 8 | Parallel arrays | **drop entirely** | At 50–150 CFM a single `D ≈ 150 mm` unit already sits in the design band. Arrays solve a flow-capacity problem this system does not have. |

### Architecture shortlist narrows

| ID | Status after `Q1` |
|---|---|
| `A1` single classical cyclone | **viable** — `D ≈ 150 mm`, Lapple or 1D3D proportions |
| `A2` length-modular | **effectively mandatory** — `S2` forces splitting anyway, so `P4.09` tuning is free (`P8.42`) |
| `A3` Karagöz double-cylinder + limiter | **still open, now more attractive** — concentric cylinders are the stiffest printable shell under `S5`, and length adjustment addresses `P3.18` |
| `A4` cyclone + fine 2nd stage | **defer** — `P8.50` says the escaping fraction is sub-10 µm, which a second cyclone stage of the same class will not catch either; a filter does that job |
| `A5` multicyclone array | **rejected** — see leverage table above |

### What `Q1` did *not* resolve

`Q2`, `Q4`, `Q5`, `Q6` remain open. `Q2` narrowed but not closed: the flow band is 50–150 CFM
(`P8.38`), a 3× spread that moves `D` by 1.7× and `x50` by 1.7×. **The specific vac's measured
airflow at the working hose is the next thing needed** — and `P8.37` says it cannot be taken from
the label. `Q3` is partially answered by `P8.50`: fine-dust capture is not achievable in this class,
so the objective defaults to filter protection unless `Q3` is answered otherwise.

## 10.9 Consequences of fixed hardware (WD06701 + P1S + planned LVHP)

Derivation in phase-08 §8.7.

### The unit-replication principle — the governing decision of this project

| ID | Statement | Tier |
|---|---|---|
| `U1` | Growing a single cyclone with flow **worsens** cut size (`x50 ∝ √D`, `P1.26`): 3.48 µm at 60 CFM → 4.93 µm at 240 CFM. The small vac is the better separator. | E |
| `U2` | Replicating a fixed-`D` unit preserves `vin`, `Eu` and `x50` exactly, at unchanged Δp. 4 × 123 mm at 240 CFM holds `x50` = 3.48 µm. | E |
| `U3` | ~~The same ~120 mm module is correct at both scales.~~ **REVISED TWICE.** (`P8.86`) the 118 mm unit does not scale to the LVHP target; (`P8.84a`) but bed size does **not** cap `D` either — bodies larger than the bed print as segmented courses. **What carries across scales is the _generator_, not the unit.** Build 1 at `D` ≈ 118 mm; regenerate at ~258 mm segmented for the LVHP. One model, two prints — the payoff of `F1`–`F6`. | E |
| `U4` | Array caveat carries forward unchanged: isolated underflows (`P6.20`), axial-symmetric arrangement (`P6.17`), tapering header (`P6.18`). A shared open hopper is the failure configuration. | A |
| `U5` | **Vessel choice constrains the array path.** One drum shared by *n* cyclones is exactly the failing configuration of `U4`. If the LVHP array is intended, the drum needs sealed internal sectors — one per cell — or separate vessels. Decide before committing to a lid pattern (`P4.60`). | A/E |

### Constraint set — additions and revisions

```
# REVISED
S1  D in [110,220] mm            -> D = 120 mm nominal; band 100-133 mm over 40-70 CFM   (P8.59)
S2  H = 4D => 450-870 mm         -> H = 480 mm => 2 modules at 250 mm Z                  (P8.70)
S3  hose sizing                  -> FIXED at 1-7/8"; below transport velocity everywhere (P8.60)
                                    => keep hose short, sloped or vertical
S4  inlet diffuser question      -> hose velocity 10.6-18.5 m/s is AT/BELOW cyclone design
                                    band, so inlet area ~ hose area; NO diffuser needed;
                                    if anything the inlet should mildly ACCELERATE       (P8.59, P8.60)

# ADDED
S6  De/D = 0.45-0.50 for build 1, NOT 0.35 -- CFM is scarcer than pressure               (P8.61)
S7  De/D is scale-invariant; do not re-decide it at the LVHP stage                       (P8.62)
S8  print envelope does NOT cap D or H: split into courses (Z) and arcs (XY)  (P8.84a, P8.103)
    flanged course joints are FREE stiffening rings, +3.6-7x on p_cr          (P8.99)
    axial seams are in COMPRESSION under vacuum; leakage+roundness, not strength (P8.100)
S10 system ceiling is the 3.5" boot port: ~265 CFM at 20.3 m/s               (P8.89-P8.91)
S11 inlet treatment INVERTS between build stages: no diffuser at 55 CFM,
    1.34x expansion required at 265 CFM                                      (P8.95)
S9  scale by unit count, never by unit size                                              (U1-U3)
```

### `S4` is a reversal — note it explicitly

`O3`/`V9.10` said the cyclone inlet must **diffuse** from a fast duct. That was derived from
woodworking *duct* practice (17.8–20.3 m/s). This vac's hose runs **10.6–18.5 m/s** — at or below
the cyclone design band. The diffuser requirement disappears; area-matching (`P6.25`, the DIY rule)
is approximately correct here by accident. `O3` still governs in principle: choose `a·b` from `vin`,
and check what that implies rather than assuming either rule.

### Architecture shortlist — final state

| ID | Status |
|---|---|
| `A1` single classical cyclone | **selected shape** — `D` = 120 mm, Lapple or 1D3D proportions, `De/D` 0.45–0.50 |
| `A2` length-modular | **mandatory and free** — 2 modules needed anyway (`P8.70`); `P4.09` length tuning included at no cost |
| `A3` Karagöz double-cylinder + limiter | **still open** — strongest fit to `S5` (stiff concentric shells) and to `P3.18`; risk remains that removing the cone removes fines separation (`P2.16`) |
| `A4` cyclone + fine 2nd stage | **defer** — `P8.50` unchanged |
| `A5` multicyclone array | **rehabilitated, LVHP phase only** — now the *correct* scaling path (`U2`), not a capacity hack (`P8.66`) |

### Still open

`Q3` (objective) — defaults to filter protection per `P8.50` unless stated otherwise.
`Q5` (collection vessel) — now the **top open item**: it is the governing structural part under
`S5`/`P8.52` and the dominant loss path under leverage rank 2.
`Q6` (hobby vs commercial) — affects `P7.34` only.
`P8.72` (nozzle diameter) — a genuine three-way trade, best settled by test rather than reading.

## 10.7 Explicit non-goals for Stage 2

| Non-goal | Reason |
|---|---|
| Beating a commercial cyclone on efficiency | Not supported as achievable by any evidence here (`V9.28`) |
| Predicting `x50` analytically for wood | No calibrated model exists at `ρp ≈ 730` (`V9.25`, `P8.03`) |
| Eliminating the downstream filter | Cyclone `x50` and filter worst-case size differ by an order of magnitude (`P8.24`) |
| Optimising body ratios beyond a classical family | Rank 7 lever; ≤1.4 pp spread (`P2.08`) |
