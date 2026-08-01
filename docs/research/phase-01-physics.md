# Phase 1 — Physics of cyclonic separation

Notation: [00-notation.md](00-notation.md). Sources: [01-sources.md](01-sources.md).

## 1.1 Mechanism

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P1.01` | Separation principle is **centrifugal cross-flow separation** (*Zentrifugalkraft­querstromabscheidung*): a tangential or vaned-axial feed creates a 3-D strongly turbulent swirl; centrifugal force drives particles radially to the wall; wall-bound particles fall out; gas reverses axially and exits through the vortex finder. | B | `S-TUD §1` |
| `P1.02` | Flow field decomposes into two coaxial regions. **Outer / quasi-free (potential) vortex**, outside the vortex-finder radius: `vθ·rⁿ = const`. **Inner / forced (solid-body) vortex**, inside it: `vθ/r = const`. The composite is a Rankine vortex; radial `vθ` profile is an inverted-W. | B | `S-TUD §2`, `L-WANG01 §Theory` |
| `P1.03` | Measured vortex exponent `n = 0.5–0.8` for gas cyclones (`0.7–0.8` for hydrocyclones). `n → 0` at the free/forced boundary, `n = −1` inside the forced core. | B | `S-TUD §2`, `L-WANG01 eq.1` |
| `P1.04` | `vθmax` occurs at the free/forced boundary, at roughly one third of the body radius, and rises as `De` falls. | B | `L-XIANG08`, secondary |
| `P1.05` | Radial pressure gradient follows `dp/dr = ρ·vθ²/r`; static pressure is maximum at the wall and minimum on the axis. A sub-atmospheric axis core is therefore intrinsic. | B | `L-WANG01 eq.3–4` |
| `P1.06` | Tangential velocity is the dominant component and sets the centrifugal force; axial and radial components govern residence time and the inward drag that opposes separation. | B | `L-WANG01`, `S-TUD §2` |

## 1.2 Force balance and cut size (equilibrium-orbit family)

**Barth control surface**: the cylindrical surface at the vortex-finder radius. A particle whose
centrifugal force exactly balances the inward Stokes drag there orbits indefinitely → collected 50 %
of the time → defines `x50`.

```
# Equilibrium-orbit cut size — Barth / Muschelknautz form.  Units SI.
# Source: S-TUD eq.(4)-(14).  Tier B.
#
# F_centrifugal = (pi/6)*x^3*rho_p * vtheta_i^2 / r_i
# F_drag        = 3*pi*mu*x*v_r_i            (Stokes, laminar, Re_p < 1)
# Setting equal and solving for x:

function x50_barth(Q, De, H_i, U, rho_p, mu):
    r_i  = De/2                       # control-surface radius
    # H_i  = axial length of control surface / r_i   (dimensionless)
    # U    = vtheta_i / v_i  ratio of tangential to mean vortex-finder velocity
    return 3 * sqrt( (mu / rho_p) * (r_i**3 / Q) * (pi / (U**2 * H_i)) )
    # S-TUD eq.(14): x_TR = 3*sqrt( (mu/rho_s) * (pi*r_i^3) / (U^2 * H_i * Qdot) )
```

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P1.07` | Stokes drag (`c_W = 24/Re`) is the assumption underpinning every closed-form cut-size model here. Valid while particle Reynolds number at `x50` is `< 1`; for fine wood dust in air this holds comfortably (`Re_p ~ 1e-2`). | B | `S-TUD §2`, MDPI cut-size review |
| `P1.08` | `x50` falls (better separation) with: larger `H_i` (slender cyclone), **smaller `ri` i.e. smaller cyclone**, larger `U`, larger `Q`. | B | `S-TUD §2 list` |
| `P1.09` | Muschelknautz tangential-velocity ratio: `U = 1 / (α·F + λ·something(Re))` — `α` = inlet coefficient (geometry-dependent), `λ` = wall friction coefficient. `λ = 0.005` clean gas; `0.005·(1+2√μ_L)` for `μ_L<1`; `0.005·(1+3√μ_L)` for `μ_L>1`. `F = a·b/(π·ri²)`. Slot inlet `α = 1 − 0.36·F^0.45`… (exact printed form partially unreadable in the PDF — see `V9.03`). | B/E | `S-TUD eq.(15)` |
| `P1.10` | Wall friction enters the cut size through `U`. Barth was the first model to include friction; Muschelknautz refined it. Alexander's earlier model treated `n` purely empirically. | B | secondary review |

## 1.3 Cut size — competing model families

| Family | Basis | Key relation | Tier | Src |
|---|---|---|---|---|
| Lapple / CCD (1951) | residence time × effective turns | `x50 = √( 9·μ·b / (2π·Ne·vin·(ρp−ρ)) )` | B | `L-LAPPLE51`, `W-PSU` |
| Barth / Muschelknautz | equilibrium orbit at control surface | `S-TUD eq.(14)` above | B | `S-TUD` |
| Leith & Licht (1972) | back-mixed turbulent transport | `η = 1 − exp(−2·(C·Ψ)^(1/(2n+2)))` | C | `W-PPN-LL` |
| Iozia & Leith (1989/90) | equilibrium orbit + regressed core geometry | `x50 = √( 9·μ·Q / (π·Hcs·ρp·vθmax²) )` | A | `L-IOZIALEITH89` |
| Mothes & Löffler | finite particle turbulent diffusivity between zones | numerical, needs `Dr` | A | `L-SALCEDO01 §Model` |

```
# Lapple effective turns and cut size.  Tier B.  Valid strictly for 2D2D-proportioned cyclones.
function Ne_lapple(a, h, H):        return (1/a) * ( h + (H - h)/2 )
function x50_lapple(mu, b, Ne, vin, rho_p, rho):
    return sqrt( 9*mu*b / (2*pi*Ne*vin*(rho_p - rho)) )

# Iozia & Leith regressed core quantities.  Tier A (constants disputed, see V9.01).
function vtheta_max(vin, a, b, D, De, H):
    return 6.1 * vin * (a*b/D**2)**-0.61 * (De/D)**-0.74 * (H/D)**-0.33
function core_diameter(D, a, b, De):
    return 0.52 * D * (a*b/D**2)**-0.25 * (De/D)**1.53
```

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P1.11` | Lapple `Ne` and the "generalised" Lapple grade curve **under-predict** real collection efficiency and over-predict emissions. Measured overall efficiency 95–99.7 % vs Lapple-predicted 79–89 % on the same hardware. | A | `L-WANG02 Tab.6` |
| `P1.12` | Model ranking on pooled grade-efficiency data: Mothes & Löffler ≳ Iozia & Leith > Lapple ≈ Barth ≈ Leith-Licht ≈ Dietz. Iozia & Leith systematically **under**-predicts collection. | A | `L-SALCEDO01 Tab.1`, `L-IOZIALEITH89` |
| `P1.13` | No model family gives consistently good predictions across geometries, dusts and operating points. Industry practice is to only build geometries that have been physically tested. 98–106 distinct published "high-efficiency" designs exist. | A | `L-SALCEDO01 §Intro` |

## 1.4 Grade-efficiency curve shape

```
# Two interchangeable parameterisations. Never mix them (Trap N.03).
T_logistic(x)  = 1 / (1 + (x50/x)**beta)          # beta larger  => sharper
T_lognormal(x) = Phi( ln(x/x50) / ln(sigma_T) )   # sigma_T larger => shallower
# Lapple's classical curve is the beta = 2 case.
```

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P1.14` | Lapple `β = 2` reference points: `x/x50` = 0.5→20 %, 1→50 %, 2→80 %, 3→90 %, 5→96.2 %, 10→99 %. Rule of thumb: **2× cut size ≈ 80 %, 3× ≈ 90 %, 5× ≈ 96 %**. | B | `L-LAPPLE51` via `W-PSU` |
| `P1.15` | `β` for real reverse-flow cyclones is typically 2–3; `β = 2` is the safe preliminary value. | C | `W-PPN-DESIGN` (`Γ ≈ 3 ± 1` steepness factor) |
| `P1.16` | Measured curves are **sharper** than Lapple predicts. Measured `σ_T` = 1.20–1.40 across 1D3D/2D2D/1D2D vs Lapple-model `σ_T` = 2.12–2.20 on identical hardware. This — not the cut size — is the main reason Lapple under-predicts η. Measured `x50` was 4.0–4.5 µm vs Lapple 3.5–4.8 µm, i.e. cut size agreed within ~20 %. | A | `L-WANG02 Fig.7–9` |
| `P1.17` | Grade curve shape is not a pure function of geometry: measured cut point varied with the **inlet PSD** (2.5 µm for a fine dust vs 4.25 µm for fly ash in the same cyclone) but was independent of inlet loading over 1.5–3 g/m³. | A | `L-WANG02 Tab.5` |
| `P1.18` | Spilger approximation for a tangential aerocyclone: `T(x) = (1 + 9.14·(x50/x)^3.5)^-0.53`. VDI/Muschelknautz alternative assumes an RRSB feed: `T(x) = 1 − exp(−1.3·(x/x50,3A)^1.2)`. | B | `S-TUD eq.(22)(23)` |

## 1.5 Pressure drop

```
# Universal form. Everything below is a way of estimating Eu.
Delta_p = Eu * 0.5 * rho * vin**2

# Shepherd & Lapple (1939) -- geometry-light, only inlet & outlet dimensions.
Eu_SL   = 16 * a * b / De**2              # 7.5 instead of 16 when an inlet vane is fitted

# Ramachandran et al. (1991) -- recommended for optimisation work.
Eu_RAMA = 20 * (S*a*b/D**2) / ( (De/D)**2 * ((H - S)/D) )**(1/3)
```

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P1.19` | `Eu` is independent of operating conditions for `Re > 5e4`; it is a pure geometry number in that regime. | A | `L-SINGH17 §2` |
| `P1.20` | Shepherd-Lapple treats all swirl energy remaining in the vortex finder as lost, and responds to **no** dimension other than `a`, `b`, `De`. It therefore predicts identical Δp for a tall and a short cyclone. Known defect, widely restated. | B | `L-WANG01 §Intro`, `W-PPN-DESIGN` |
| `P1.21` | Barth-type models decompose Δp into inlet + main-swirl + vortex-finder terms and respond to body geometry and wall friction. `S-TUD eq.(16)(17)` gives `Δp = Δp_E + Δp_H + Δp_i`, with `ζ_i = 2 + 3·U^(4/3) + U²` and `ζ_H = U²/(…)`. Slot inlet `ζ_E = 0`; spiral inlet `ζ_E = f(R,F)`. | B | `S-TUD eq.(16)–(17)` |
| `P1.22` | Elsayed recommends **Ramachandran** over Shepherd-Lapple and Barth for `Eu` prediction. A separate comparison found the full Muschelknautz method lowest-residual against experiment. Both cannot be simultaneously best — see `V9.02`. | A/B | `L-SINGH17 §2`; secondary review |
| `P1.23` | Predicted-vs-measured scatter across models is severe: some models over-predict by >2×. For one optimised geometry, Dirgo's model gave `Eu = 9.4` where Bohnet & Lorenz gave 3.4 and measurement favoured 3.4. Reported `Eu` for real cyclones at a nominal computed 9.4 scattered 2–11. | A | `L-SALCEDO01 §Pressure Drop` |
| `P1.24` | Typical operating envelope for industrial aerocyclones: `Δp = 500–2000 Pa` (broader 300–2500), `Eu = 10–20` (range 5–40). | B | `S-TUD §Typische Zyklonparameter` |
| `P1.25` | Frictional loss in the outer vortex is the dominant term, and `L/Ds` (spiral travel length over effective stream-tube diameter) is a **constant for a given geometry family**. Consequence: **Δp is independent of cyclone diameter** at fixed inlet velocity. 1D3D: `L = 9.96·D`, `L/Ds = 39.84`. 2D2D: `L = 13.08·D`, `L/Ds = 52.32`. | A | `L-WANG01 eq.20–22` |

## 1.6 Scaling laws — the load-bearing result for this project

| ID | Claim | Tier | Derivation |
|---|---|---|---|
| `P1.26` | **At fixed inlet velocity, `x50 ∝ √D`.** Halving cyclone diameter improves the cut size by √2 ≈ 1.41×. | E (derived, cross-checked 2 ways) | From `x50_lapple` with `b ∝ D`, `vin` fixed, `Ne` fixed → `x50 ∝ √D`. Independently from `S-TUD eq.(14)`: `x50 ∝ √(ri³/Q)`, and `Q ∝ vin·D²` ⇒ `x50 ∝ √(D/vin)`. |
| `P1.27` | **At fixed volumetric flow, `x50 ∝ D^1.5`.** From `x50 = √(3μD³/(128π·Q·Δρ))` for standard Lapple proportions. | E (derived) | `W-PSU` closed form, algebra re-derived and confirmed against `x50_lapple` with `Ne=6`, `b=D/4`, `a=D/2`. |
| `P1.28` | **Flow capacity ∝ D².** Therefore holding both `x50` and `Q` requires *n* parallel small cyclones, `n ∝ (D_big/D_small)²`. This is the entire justification for multicyclones. | E (derived) | `Q = vin·a·b ∝ vin·D²` |
| `P1.29` | Δp does **not** improve by going small (`P1.25`). The cost of small cyclones is paid in count and in plumbing, not in pressure. | A/E | `L-WANG01` + `P1.28` |
| `P1.30` | Typical single-cyclone envelope: body diameter 2 cm – 5 m; `Q` 1 – 200 000 m³/h; achievable cut size `x50 ≥ 1–5 µm`; clean-gas concentration 100–200 mg/m³ from inlet up to 1000 g/m³. | B | `S-TUD §1, §Typische` |

## 1.7 Inlet velocity — the non-monotonic axis

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P1.31` | Collection efficiency **rises then falls** with inlet velocity. Above an optimum, re-entrainment of wall-deposited solids (saltation) and turbulent dispersion dominate the added centrifugal force. | A | `L-SALCEDO01 §Constraints`, `L-WANG02 §Testing` |
| `P1.32` | Design constraint used in published optimisation: `vin / vs ≤ 1.25`, where `vs` is the saltation velocity (a function of geometry, particle density and operating conditions). | A | `L-SALCEDO01 eq.5` |
| `P1.33` | Texas A&M design velocities, empirically derived per geometry family: 1D3D = 3200 fpm (16.3 m/s); 2D2D = 3000 fpm (15.2 m/s); 1D2D = 2400 fpm (12.2 m/s). *"A dramatic increase in exit concentrations has been observed at velocities significantly higher than the design velocities."* | A | `L-WANG02 Tab.1`, `L-WANG01` |
| `P1.34` | DIY corroboration at shop scale: excess airflow through a fixed separator lowered efficiency — 3 motors caused "unwanted swirls in the waste bin pulling dust up into the filter" where 2 motors did not; a small 3rd-stage separator ran at "way too high" air speed and collected only 75 %. | D | `S-CD-inlets`, `S-CD-cyclone2` |
| `P1.35` | The optimum is *velocity*, not *power*. Under-flowing is equally destructive but for a different reason: it fails to entrain material at the tool and lets it drop out in the hose. | D | `S-CD-cyclone1` |

## 1.8 Solids loading

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P1.36` | Two loading regimes. Below a **limit loading `μ_Gr`**, separation is size-selective by settling velocity. Above it, the excess fraction `(μ_L − μ_Gr)` separates **spontaneously and non-selectively** at the inlet as a wall-hugging strand (*Gutsträhne*) that slides to the bin. Cause: turbulence damping by the solids reduces the carrying capacity of the flow. | B | `S-TUD §Modellierung` |
| `P1.37` | Overall efficiency with loading: `η = 1 − ((1−μ_Gr/μ_L))·∫T(x)q_A(x)dx` for `μ_L > μ_Gr`; plain `∫T(x)q_A(x)dx` otherwise. High loading therefore *raises* apparent overall efficiency. | B | `S-TUD eq.(21)` |
| `P1.38` | Muschelknautz/Klose limit-loading estimate: `μ_Gr = 0.21·(x̄_50,3/x_TR)^…·(…)` — the printed form in `S-TUD eq.(19)(20)` is partially garbled in text extraction; treat as a pointer to VDI-Wärmeatlas, not as a usable formula. | E | `S-TUD eq.(19)(20)`, see `V9.03` |
| `P1.39` | Consequence for benchmarking: an overall-efficiency number measured at high feed rate is **not comparable** to one measured at low feed rate, and neither is a property of the cyclone alone. All DIY percentages in this corpus are loading-contaminated. | E | derived from `P1.36`–`P1.37` |
| `P1.40` | Empirical shape of the same effect: measured `x50` was independent of loading over 1.5–3 g/m³ (a low-loading band), so `P1.36` bites well above ordinary shop concentrations. | A | `L-WANG02` |

## 1.9 Loss mechanisms that no cut-size model captures

| ID | Mechanism | Effect | Tier | Src |
|---|---|---|---|---|
| `P1.41` | **Short-circuit flow** — gas passing directly from inlet to vortex finder across the roof without completing a turn. | Direct bypass of fines | A | `L-SALCEDO01 eq.9` (`S > 1.25·a` exists to prevent it) |
| `P1.42` | **Vortex-end re-entrainment** — the descending vortex terminates on a wall or on the collected pile and scours it. | Dominant fines loss | A | phase 4 |
| `P1.43` | **Precessing vortex core (PVC) / vortex wobble** — asymmetry (chiefly the single inlet) makes the core precess; degrades collection and erodes the cone. | Efficiency + wear | B | `L-HOFFSTEIN` via secondary |
| `P1.44` | **Wall deposit growth** — accumulating particles raise effective wall roughness in service, reducing `vθ` and vortex length over time. | Progressive degradation | A | `S-KARAGOZ13 §5.1`, `L-KAYA11` |
| `P1.45` | **Trash disruption** — particles >100 µm tumbling through the separator disrupt the wall strand pattern and sharply raise fine-particle emission. FECs are *not* independent of the coarse fraction present. | Fines loss when coarse present | A | `L-WANG02 §Intro` |
| `P1.46` | **Electrostatic adhesion / charging** — insulating walls and dry fine dust build charge; charged fines adhere to walls and to each other, changing effective size and wall behaviour. Repeated re-use of test dust changed measured results. | Corrupts both performance and measurement | D | `S-CD-cyclone2`, `S-CD-tweaks` |

## Branch decisions taken from Phase 1

| Branch | Trigger | Goes to |
|---|---|---|
| Natural vortex length is the mechanism behind `P1.42` and the length optimum in `S-KARAGOZ13` | `P1.42` | Phase 4 |
| `vθmax` is set mainly by `De` (`P1.04`), and short-circuiting by `S` (`P1.41`) — both are inlet/outlet topology questions | `P1.41`, `P1.04` | Phase 5 |
| `P1.26`–`P1.28` make the small-cyclone-array trade explicit and quantitative | `P1.28` | Phase 6 |
| Wall roughness (`P1.44`) is a manufacturing variable, not a design constant, for FDM parts | `P1.44` | Phase 7 |
| `vin` optimum (`P1.31`–`P1.35`) couples the cyclone to the fan and duct, not just to itself | `P1.33` | Phase 8 |
