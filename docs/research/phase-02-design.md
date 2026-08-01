# Phase 2 — Design of cyclonic separators

Notation: [00-notation.md](00-notation.md). Depends on [phase-01-physics.md](phase-01-physics.md).

## 2.1 The design method that is actually used

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P2.01` | A reverse-flow cyclone is fully specified by **7 ratios + 1 scale**: `a/D, b/D, De/D, S/D, h/D, H/D, B/D`, then `D`. Everything else follows. | A | `L-SINGH17 §2` |
| `P2.02` | Standard practice: pick a published ratio family, then solve `D` from the flow requirement and the family's design inlet velocity. Do not invent ratios. | C | `W-PPN-DESIGN §4.1` |
| `P2.03` | Reason for `P2.02`: no analytical model predicts arbitrary geometry reliably (`P1.13`). Ratio families are compressed experiment. | A | `L-SALCEDO01 §Intro` |

```
# Standard sizing procedure. Tier C. Source: W-PPN-DESIGN §4.
1. inputs: Q, rho, mu, rho_p, target x50, allowable Delta_p
2. choose ratio family F  -> {a/D, b/D, De/D, S/D, h/D, H/D, B/D}, v_design
3. D  = sqrt( Q / (v_design * (a/D) * (b/D)) )        # from Q = vin*a*b
4. derive all absolute dimensions from D and F
5. x50 <- cut-size model (phase-01 §1.3);  Delta_p <- Eu model (phase-01 §1.5)
6. if x50 too large: reduce D  (P1.27) and add units in parallel (P1.28)
   if Delta_p too large: this is NOT fixed by changing D (P1.25) -> change family or vin
7. check feasibility constraints (section 2.4). iterate.
```

## 2.2 Standard geometry families

All values normalised to `D`. **Cross-verified against two independent reproductions of the
Koch & Licht (1977) compilation.**

| Ratio | Stairmand HE | Swift HE | Lapple (std) | Swift (std) | Peterson-Whitby |
|---|---|---|---|---|---|
| `a/D` | 0.5 | 0.44 | 0.5 | 0.5 | 0.583 |
| `b/D` | 0.2 | 0.21 | 0.25 | 0.25 | 0.208 |
| `De/D` | 0.5 | 0.4 | 0.5 | 0.5 | 0.5 |
| `S/D` | 0.5 | 0.5 | 0.625 | 0.6 | 0.583 |
| `h/D` | 1.5 | 1.4 | 2.0 | 1.75 | 1.333 |
| `(H−h)/D` (cone) | 2.5 | 2.5 | 2.0 | 2.0 | 1.84 |
| **`H/D` (total)** | **4.0** | **3.9** | **4.0** | **3.75** | **3.17** |
| `B/D` | 0.375 | 0.4 | 0.25 | 0.4 | 0.5 |
| `a/b` aspect | 2.5 | 2.1 | 2.0 | 2.0 | 2.8 |
| `Eu_SL = 16ab/De²` | 6.4 | 9.24 | 8.0 | 8.0 | 7.76 |

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P2.04` | Stairmand HE is the de-facto baseline for both optimisation studies and CFD validation. | A | `L-SINGH17`, `L-ELSAYED10` |
| `P2.05` | Stairmand's stated inlet aspect target is `a:b = 2.6` (13:5); the tabulated 0.5/0.2 gives 2.5. Treat 2.0–2.6 as the classical band. | C | secondary; `P2.02` table |
| `P2.06` | High-efficiency families have **smaller inlet and outlet areas** than high-throughput families. That is the whole distinction. | C | `W-PPN-DESIGN` |
| `P2.07` | A "Stairmand high-gas-rate" column exists in the standard table (6-column layout: Stairmand HE, Swift HE, Lapple, Swift std, Peterson-Whitby, Stairmand HG). Its numeric values were **not** obtained from a verifiable source in this pass — do not quote them. | E | see `V9.04` |

### Texas A&M families (agricultural / wood-dust lineage — most relevant to this project)

Named `<barrel length in D>D<cone length in D>`. Inlet: `a = D/2`, `b = D/4` (i.e. Lapple inlet).

| Family | `h/D` | `(H−h)/D` | `H/D` | `De/D` | design `vin` | Measured `x50` @ D=152 mm | Measured `σ_T` |
|---|---|---|---|---|---|---|---|
| 1D3D | 1 | 3 | 4 | 0.5 | 16.3 m/s (3200 fpm) | 2.50–4.25 µm | 1.20–1.40 |
| 2D2D | 2 | 2 | 4 | 0.5 | 15.2 m/s (3000 fpm) | 2.74–4.40 µm | 1.20–1.32 |
| 1D2D | 1 | 2 | 3 | 0.5 | 12.2 m/s (2400 fpm) | 2.82–4.50 µm | 1.25–1.33 |

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P2.08` | At their respective design velocities the three TAMU families measured **95.3–99.7 % overall** on dusts with MMD 13–23 µm. 1D3D was best on every dust, 1D2D worst, but the spread was small (≤1.4 pp). | A | `L-WANG02 Tab.4, Tab.6` |
| `P2.09` | The 1D2D exists specifically as a **low-pressure** variant for cotton gins; it buys Δp by shortening and slowing, at a modest efficiency cost. | A | `L-WANG02 §Intro` |
| `P2.10` | 1D3D vs 2D2D: 1D3D has a longer cone and shorter barrel and turns ~1.5× in the barrel + ~4.5× in the cone; 2D2D turns ~3× + ~3×. Total ≈ 6 turns both. | A | `L-WANG01 eq.20` |

## 2.3 Element-by-element design sensitivities

| ID | Element | Direction | Effect | Tier | Src |
|---|---|---|---|---|---|
| `P2.11` | Inlet width `b` ↓ | | `x50` ↓ (better), Δp ↑. **`b` matters more than `a`**, especially for cut size. Optimum `b/a` reported 0.5–0.7. | A | `L-ELSAYED11` |
| `P2.12` | Inlet area `a·b` ↑ | | `vθmax` ↓, Δp ↓, `x50` ↑ (worse), natural vortex length ↑ | A | `L-ELSAYED11`, `L-ALEXANDER49` |
| `P2.13` | Vortex finder `De` ↓ | | `vθmax` ↑, efficiency ↑, Δp ↑. Monotonic, unavoidable trade. | A | `L-XIANG08` |
| `P2.14` | Vortex finder depth `S` ↑ | | reduces short-circuiting; too deep shortens usable separation length | A | `L-SALCEDO01 eq.9`, phase 5 |
| `P2.15` | Cone tip `B` ↓ (while `B > De`) | | efficiency ↑ **without significant Δp increase** | A | `L-XIANG01`, `S-KARAGOZ13 §1` |
| `P2.16` | Cone removed entirely (straight tube) | | fine-particle separation collapses | D | `S-CD-cyclone2` — replaced cone with a plain 300 mm tube; *"the test results made it very clear that we do need a cone to be able to separate out the smaller dust particles"* |
| `P2.17` | Body length `H` ↑ | | efficiency ↑ **only up to the natural vortex length**, then falls. There is an optimum `H` for each flow rate. | A | `S-KARAGOZ13 §4.2`, `L-SURMEN11`, `L-HOFFMANN01` |
| `P2.18` | Wall roughness ↑ | | Δp ↓, `vθ` ↓ (up to −18 %), vortex length ↓, efficiency ↓ (−12 % for >25 µm in one axial-cyclone study). Effect grows with inlet velocity. | A | `L-KAYA11`, secondary CFD |
| `P2.19` | Cone-only roughness | | contradicts `P2.18` in one study (tangential and axial velocity *enhanced*). Unresolved. | A/E | see `V9.05` |

## 2.4 Hard feasibility constraints

The most directly reusable artefact in this phase. Any candidate geometry that violates these is
outside validated practice.

```
# Feasibility constraint set. Tier A. Source: L-SALCEDO01 eq.(2)-(10),
# assembled there from Ramachandran & Leith, Li et al., Licht, and geometric practice.

C1  Delta_p            <= Delta_p_max                      # cost/operating limit; 1.5 kPa used for HE cyclones
C2  6.8 deg  <  eps    <= 16 deg                           # cone SEMI-angle: dust must dislodge and slide
C3  0.5      <  (a*b) / ((pi/4)*De**2)  <  0.735           # inlet area / gas discharge area  (see P2.21)
C4  vin / vs <= 1.25                                       # saltation / re-entrainment ceiling
C5  S < h < H                                              # vortex finder inside the barrel
C6  0.5*De   <  B  <  De                                   # cone tip bracketed by the vortex finder dia.
C7  0.5*(D - De)  >  b                                     # inlet fits the annulus with a clean transition
C8  S > 1.25*a                                             # anti short-circuit
C9  2.3*De*(D**2/(a*b))**(1/3)  <  H - S                   # Alexander natural length must fit inside
```

| ID | Note | Tier |
|---|---|---|
| `P2.20` | `C2` translates to a **cone included angle of 13.6°–32°**. Steeper than 32° included risks bridging/hold-up; shallower than 13.6° wastes height. | A |
| `P2.21` | `C3` **corrected here.** As text-extracted from `L-SALCEDO01 eq.(4)` the ratio reads `(π/4)De²/(a·b)`, which evaluates to 1.96 (Stairmand HE) and 1.57 (Lapple) — both outside the stated 0.5–0.735 bracket. Inverting it resolves cleanly: `a·b / ((π/4)De²)` = **0.509 (Stairmand HE), 0.637 (Lapple), 0.735 (Swift HE — exactly the upper bound), 0.637 (Swift std), 0.617 (Peterson-Whitby)**. All five classical families fall inside the bracket, with two sitting on its edges. The extracted orientation was an OCR/typesetting inversion. Use the corrected form. | E (derived, 5/5 families confirm) | `L-SALCEDO01 eq.4` + arithmetic |
| `P2.22` | `C6` at Stairmand HE: `De/D=0.5`, `B/D=0.375` → `B/De = 0.75`, satisfies `0.5 < 0.75 < 1`. Lapple: `B/De = 0.5`, at the boundary. | E (checked) |
| `P2.23` | `C8` at Stairmand HE: `S=0.5D`, `1.25a = 0.625D` → **violated**. Stairmand HE short-circuits by this criterion. Lapple: `S=0.625D`, `1.25a=0.625D` → exactly at the bound. Treat `C8` as an optimisation preference, not a validity gate. | E (checked) |
| `P2.24` | `C9` at Stairmand HE: `2.3·0.5·(1/(0.5·0.2))^(1/3)` = `1.15·2.154` = `2.48 D` vs `H−S = 3.5 D`. Satisfied with margin. Lapple: `2.3·0.5·(1/0.125)^(1/3)` = `1.15·2 = 2.30 D` vs `3.375 D`. Satisfied. | E (checked) |

## 2.4a Constraint interactions found by mechanising the checks

Discovered by encoding §2.4 as executable assertions in the Stage-2 generator
(`cyclone.py`), against the 1D3D geometry actually selected.

| ID | Claim | Tier |
|---|---|---|
| `P2.32` | **`C3` is two-sided and therefore bounds `De/D` from *both* ends.** For a Lapple/1D3D inlet (`a·b = 0.125·D²`) it admits only **`De/D` = 0.465–0.564**. Below 0.465 the outlet is too small relative to the inlet; above 0.564 too large. | E (verified) |
| `P2.33` | **This partly invalidates `P8.61`.** That claim recommended `De/D` = 0.45–0.50 for LVHP duty; **0.45 is infeasible** — it gives an area ratio of 0.786 against a 0.735 ceiling. The usable recommendation is **0.466–0.50**, and `De/D` = 0.50 (the family value) sits mid-window. | E (verified) |
| `P2.34` | **The 1D3D family sits *exactly* on two constraint bounds simultaneously.** `C6` lower bound: `B = 0.25D` and `0.5·De = 0.25D` — equal. `C7`: `b = 0.25D` and `0.5(D−De) = 0.25D` — equal. Neither is a violation; both are exact contact. | E (verified) |
| `P2.35` | `P2.34` extends the pattern of `P2.21` (Swift HE landing exactly on the `C3` ceiling) and `P2.23` (Stairmand HE landing exactly on `C8`). **The classical families are not merely inside the feasible region — they sit on its faces.** Reading: these constraints were most likely *derived from* the surviving families rather than independently, so they should be treated as a description of validated practice, not as physics. Deviating slightly outside them is a departure from precedent, not necessarily from function. | E |
| `P2.36` | Practical consequence for any generator: bounds must be evaluated **inclusively with a tolerance**, and exact contact reported distinctly from both pass and fail. A strict inequality rejects every classical family. | E |

## 2.5 Non-classical topologies encountered

| ID | Topology | Claimed benefit | Cost | Tier | Src |
|---|---|---|---|---|---|
| `P2.25` | **Double cylinder + movable vortex limiter, no cone** (`S-KARAGOZ13`). Flow enters an inner cylinder (vortex creator, carries the friction), spirals down into a low-friction outer cylinder, reverses at an adjustable limiter plate. | Higher collection than a conventional cyclone of the same `D`; ~5 % gain from tuning limiter position; steeper grade curve; dust does not roughen the working surfaces; length extendable; continuous discharge. | Δp slightly higher at fixed geometry (roughly equal once limiter is tuned); one moving/adjustable part. | A | `S-KARAGOZ13 §5` |
| `P2.26` | **Circumfluent cyclone** | +8 % efficiency at 12–26 m/s; Δp only 1/2 to 1/3 of conventional | complexity | A (2nd-hand) | `S-KARAGOZ13 §1` |
| `P2.27` | **Double cyclone** | lower Δp | **not** higher efficiency unless an electric field is added | A (2nd-hand) | `S-KARAGOZ13 §1` |
| `P2.28` | **Iinoya type (double conical)** | Δp ~10 % lower | efficiency ≈ equal | A (2nd-hand) | `S-KARAGOZ13 §1` |
| `P2.29` | **Post-cyclone** (two annular shells on the gas exit) | +2–20 % overall | +10 % of total Δp | A (2nd-hand) | `S-KARAGOZ13 §1` |
| `P2.30` | **Square cyclone**, **ribbed / grooved body**, **spiral guide body** | spiral guide helps at low flow only; no benefit at high flow | — | A (2nd-hand) | `S-KARAGOZ13 §1` |
| `P2.31` | **Centrifugal / "Gyro-Air" impeller separator** (Harvey G700 class; the `S-CD` platform). Axial flow through a static impeller in a straight tube; dust ports on the tube wall. Not a reverse-flow cyclone — no cone, no vortex finder, no inner vortex. | very compact, horizontal-mountable, stackable in stages | mechanism is unmodelled by any cyclone theory in this corpus | D | `S-CD-build1`, `S-CD-intro` |

## Branch decisions taken from Phase 2

| Branch | Trigger | Goes to |
|---|---|---|
| `P2.17` length optimum ⇒ natural vortex length is the governing constraint, not `H/D` convention | `P2.17`, `C9` | Phase 4 |
| `P2.13`/`P2.14` — `De` and `S` dominate both cut size and short-circuiting | `P2.13` | Phase 5 |
| `P2.18` roughness is set by the printer, not by the designer | `P2.18` | Phase 7 |
| `P2.31` — the strongest DIY empirical dataset comes from a device that is *not* a cyclone | `P2.31` | Phase 9 |
