# Phase 3 — Optimization of cyclone geometry

Notation: [00-notation.md](00-notation.md). Depends on phases [1](phase-01-physics.md), [2](phase-02-design.md).

## 3.1 Problem statement

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P3.01` | The canonical formulation is **bi-objective**: minimise `Eu` (pressure drop) and minimise `Stk50` (cut size), over the 7 ratios of `P2.01`. Both objectives are dimensionless, so the result is scale-free. | A | `L-SINGH17 §2` |
| `P3.02` | The two objectives genuinely conflict. There is no single optimum, only a Pareto front. Every published "optimal cyclone" is a point choice on that front plus an undeclared weighting. | A | `L-SINGH17 §6` |
| `P3.03` | Objective evaluation must be surrogate-based: a single CFD run of a cyclone takes weeks; a physical test takes longer. Analytical models are cheap but wrong (`P1.13`). Modern work fuses fidelities (co-Kriging over analytical + CFD + experiment). | A | `L-SINGH17 §1` |
| `P3.04` | Alternative objective when cost matters: efficiency/cost ratio (Licht criterion), which yields a *different* geometry from pure efficiency maximisation. `L-SALCEDO01` publishes both (`RS_VHE` vs `RS_K`). | A | `L-SALCEDO01 §Optimization` |

```
# Reference formulation. Tier A. Source: L-SINGH17 eq.(3).
minimise over x = (a, b, De, H, h, S, B)      # all as ratios of D
    Eu(x)          via Ramachandran model      (phase-01 §1.5)
    Stk50(x)       via Iozia & Leith model     (phase-01 §1.3)
subject to
    0.40 <= a  <= 0.70
    0.14 <= b  <= 0.40
    0.40 <= De <= 0.75
    3.0  <= H  <= 7.0
    1.0  <= h  <= 2.0
    0.4  <= S  <= 2.0
    0.2  <= B  <= 0.4
# Reference operating point used there: D = 31 mm, Q = 50 L/min, rho = 1.225,
# rho_p = 860 kg/m3, mu = 1.7894e-5 Pa.s  (a health-aerosol sampling cyclone)
```

## 3.2 Structure of the Pareto front — the actionable result

From `L-SINGH17 Tab.1` (100 Pareto-optimal solutions, SMS-EMOA, 10 000 evaluations).
Reading the front from low-Δp to fine-cut:

| Variable | Behaviour across the whole front | Interpretation |
|---|---|---|
| `a` | pinned at **0.400** (lower bound) in every one of 100 solutions | inlet height wants to be as small as allowed; bound-limited |
| `H` | pinned at **4.000** in every solution | total height 4·D is a genuine interior optimum, not a bound artefact (bounds were 3–7) |
| `S` | pinned at or just above **0.40** (lower bound) | vortex finder wants to be shallow |
| `B` | pinned at or just above **0.20** (lower bound) | cone tip wants to be as small as allowed |
| `h` | scattered **1.00–1.80**, no trend | weak objective sensitivity → free design variable |
| `b` | **0.14–0.26**, non-monotonic | secondary trade lever |
| `De` | **0.75 → 0.40**, monotonically decreasing along the front | **the single dominant trade variable** |
| `Eu` | 0.40 → 1.58 | |
| `log(Stk50·10³)` | 1.22 → 0.48 | |

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P3.05` | **`De/D` is the master trade knob.** Sweeping it 0.75→0.40 moves `Eu` 0.40→1.58 (≈4×) while `Stk50` falls ≈5.5×. Everything else on the front is second-order. Confirms `P2.13` quantitatively. | A | `L-SINGH17 Tab.1` |
| `P3.06` | `H/D = 4` emerging as an interior optimum independently reproduces the Stairmand HE and Lapple total height (`P2.02` table). Strong convergent evidence. | A/E | `L-SINGH17 Tab.1` + `P2.02` |
| `P3.07` | `B/D` and `S/D` both drive to their lower bounds. The optimiser is being *stopped by the bounds*, not by physics. Both are exactly the variables governed by re-entrainment and short-circuit effects the objective functions do not model (`P1.41`, `P1.42`). **Do not read these as design recommendations.** | E | derived; `L-SINGH17` bounds vs `P1.41`/`P1.42` |
| `P3.08` | `h/D` being insensitive means barrel height is available to spend on manufacturability (print-bed height, bin clearance) at low performance cost — provided `H/D` and the vortex length constraint are held. | E | derived from front scatter |

## 3.3 Published optimised geometries

| Ratio | Stairmand HE (ref) | Elsayed/Lacor optimum | `RS_VHE` (max η) | `RS_K` (max η/cost) | Iozia-Leith optimum |
|---|---|---|---|---|---|
| `a/D` | 0.5 | ≈ Stairmand HE | 0.270–0.360 | 0.270–0.310 | 0.350 |
| `b/D` | 0.2 | | 0.270–0.360 | 0.270–0.310 | 0.350 |
| `S/D` | 0.5 | | 0.330–0.495 | 0.330–0.395 | 0.350 |
| `De/D` | 0.5 | | 0.280–0.370 | 0.395–0.405 | 0.390 |
| `h/D` | 1.5 | | 1.001–1.300 | 2.050–2.260 | 1.500 |
| `H/D` | 4.0 | | 4.050–4.250 | 3.500–3.700 | 5.000 |
| `B/D` | 0.375 | | 0.200–0.300 | 0.250–0.300 | 0.375 |

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P3.09` | Elsayed & Lacor's min-Δp optimum came out **close to Stairmand HE**, achieving −27 % Δp and −20 % cut size vs Stairmand. A second reported optimum nearly halved Δp but slightly worsened cut size. | A | `L-ELSAYED10`, `L-ELSAYED12` (via abstracts) |
| `P3.10` | `RS_VHE` and `RS_K` both use an **essentially square inlet** (`a ≈ b`), against the classical 2.0–2.6 aspect (`P2.05`). This is the sharpest disagreement between optimisation output and classical practice in the corpus. | A | `L-SALCEDO01 Tab.2` |
| `P3.11` | Both optimised designs use a **narrower vortex finder** than Stairmand HE; `RS_VHE` narrowest (`De/D` down to 0.28). Consistent with `P3.05`. | A | `L-SALCEDO01` |
| `P3.12` | `RS_VHE` (efficiency-maximising) has a barrel **~50 % shorter** than Stairmand HE and is ~6 % longer overall; `RS_K` (cost-optimising) has a barrel ~50 % **longer** and is ~12 % shorter overall. Barrel height moves in opposite directions under the two objectives — corroborating `P3.08` that `h` is weakly constrained. | A | `L-SALCEDO01` |
| `P3.13` | `RS_VHE` measured `Eu = 3.4` (Bohnet & Lorenz model matched measurement); Dirgo's model predicted 9.4 for the same geometry. Optimisation results are **strongly conditional on the Δp model chosen** — `L-SALCEDO01` states this explicitly. | A | `L-SALCEDO01 §Pressure Drop` |
| `P3.14` | Against a 106-design literature survey, `RS_VHE` shares at most 4 of 7 ratios with any published design, and 20–40 published designs share nothing with it. The classical families do not span the useful design space. | A | `L-SALCEDO01 Fig.2` |
| `P3.15` | Dirgo & Leith's earlier optimisation produced geometries that **failed to show improvement in pilot testing**. Optimisation without a validated performance model is not predictive. | A | `L-SALCEDO01 §Intro` |

## 3.4 Optimisation of operating point rather than geometry

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P3.16` | For a *given* geometry there exists an optimum inlet velocity (`P1.31`–`P1.33`) and, coupled to it, an optimum separator length equal to the natural vortex length at that flow (`P2.17`). Both shift with flow rate. | A | `S-KARAGOZ13 §4.2`, `L-SURMEN11` |
| `P3.17` | `S-KARAGOZ13` exploits this by making the length **adjustable in service** via a sliding vortex limiter: raise flow → slide the limiter down. Measured effect: up to ~5 % efficiency gain over a fixed-length equivalent at matched Δp; `x50` shows a clear minimum vs limiter position `L`, rising again on both sides. | A | `S-KARAGOZ13 §4.1–4.2, Fig.7` |
| `P3.18` | Corollary for a variable-duty shop system (a CNC with gates, multiple tools, filter loading): a fixed-geometry cyclone is optimal at exactly one operating point. Either the operating point is pinned, or the geometry is made adjustable. | E | derived from `P3.16`–`P3.17` |
| `P3.19` | DIY corroboration of the same axis: a vortex-finder insertion depth made adjustable "to experiment with the depth at which the vortex finder is inserted", and a 100 mm tube protruding into the cyclone outlet gave **+50 % captured fine dust** on its own. | D | `S-CD-cyclone2`, `S-CD-cyclone1` |

## 3.5 What the optimisation literature does *not* optimise

| ID | Omitted from every objective function found | Why it matters here |
|---|---|---|
| `P3.20` | Dust-outlet/hopper geometry and re-entrainment (`B` appears, the bin does not) | dominant loss path at shop scale — phase 4 |
| `P3.21` | Solids loading effects (`P1.36`) — all cited work is **low-mass-loading** | shop dust is high-loading in bursts |
| `P3.22` | Bulk/coarse fraction disruption (`P1.45`) | CNC routing produces chips and fines simultaneously |
| `P3.23` | Wall roughness (fixed as smooth) | FDM parts are not smooth — phase 7 |
| `P3.24` | Manufacturability, part count, seal count, emptying ergonomics | dominates a printed shop device |
| `P3.25` | Off-design behaviour (front is computed at one `Q`) | shop flow varies with gates and filter loading |

## Branch decisions taken from Phase 3

| Branch | Trigger | Goes to |
|---|---|---|
| `B/D` and `S/D` bound-pinning is masking unmodelled physics | `P3.07`, `P3.20` | Phase 4 (dust outlet), Phase 5 (vortex finder) |
| `De/D` is the master knob and disagrees with classical values | `P3.05`, `P3.11` | Phase 5 |
| Optimisation ignores manufacturability entirely | `P3.24` | Phase 7 |
| Off-design behaviour is unmodelled but is the actual duty cycle | `P3.25`, `P3.18` | Phase 8 |
