# Phase 4 — Natural vortex length, the vortex end, and the dust outlet

Branch chosen from `P1.42`, `P2.17`, `P3.07`, `P3.20`.
Rationale: the largest unmodelled loss path, and the one place where classical geometry tables give
no guidance at all.

## 4.1 Natural vortex length `Ln`

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P4.01` | The descending outer vortex does **not** necessarily reach the cone tip. It terminates at a spontaneous axial position — the **vortex end** — where the core attaches to the wall. `Ln` is measured from the vortex-finder lip down to that point. | A | `L-ALEXANDER49`, `L-HOFFMANN01` |
| `P4.02` | Alexander's correlation (still the design-constraint form in use): `Ln = 2.3·De·(D²/(a·b))^(1/3)`. Depends only on `De`, `D` and inlet area. | B | `L-ALEXANDER49` via `L-SALCEDO01 eq.10` |
| `P4.03` | Alexander's data came from cylindrical cyclones of only **30–50 mm** diameter. Applicability outside that range is unestablished. Empirical forms ignoring all other structural and operating parameters have "poor accuracy and applicability". | A | review lit., secondary |
| `P4.04` | Alexander's model consistently predicts the **shortest** `Ln` of the available models. One recent small-diameter experiment measured `Ln = 2.08·D` for a baseline configuration (`b/D=0.28`, `De/D=0.30`, `S/D=0.69`). | A | small-diameter vortex-length study, 2026 |
| `P4.05` | `Ln` **increases** with inlet velocity and with inlet area; **decreases** with wall roughness. | A | `L-KAYA11`, vortex-length review |
| `P4.06` | The vortex end **moves** during operation, which is why measurement is hard. Detection methods: smoke visualisation in a glass body; wall-deposit ring after a solids run; dust-ring position. | A | `L-ALEXANDER49`, vortex-length review |
| `P4.07` | Design rule: **`Ln` should equal or slightly exceed the available separation length.** Two failure modes, both losing efficiency: `Ln` too short (vortex ends inside the cone, deforms, scours) and `Ln` too long (vortex end lands in the bin). Efficiency has a maximum at `Ln ≈ H − S`. | A | `L-HOFFMANN01`, `L-SURMEN11`, `S-KARAGOZ13 §4.2` |
| `P4.08` | Directly measured optimum: `S-KARAGOZ13` varied the limiter position `L` over 320/480/640/800 mm at fixed `Q = 257 m³/h` and found `x50` has a clear **minimum** at intermediate `L`, rising on both sides. The optimum `L` increases with flow rate. Δp was essentially unchanged across all four positions. | A | `S-KARAGOZ13 Fig.5–7` |
| `P4.09` | **`P4.08` is the strongest single result in this corpus for the project**: cyclone length can be varied over 2.5× at constant pressure drop, with cut size varying non-monotonically. Length is a free, cheap, high-leverage variable — and it is the one classical ratio tables fix arbitrarily at `H/D ≈ 4`. | E | derived from `P4.08` + `P2.02` |

## 4.2 The vortex end as the dominant fines-loss path

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P4.10` | In a high-performance cyclone an intense vortex exists **at the dust discharge point**; accumulated dust there re-entrains and leaves via the gas outlet. | B | `L-HOFFSTEIN`, dust-receiver practice |
| `P4.11` | Without a properly designed dust receiver, re-entrainment occurs well below the nominal cyclone discharge. Mitigation is to **extend the distance over which the vortex decays** so the final collection point sits where the vortex is weak. | C | dust-receiver vendor engineering practice |
| `P4.12` | Vortex "wobble"/PVC diminishes collection and accelerates cone erosion (Stein & Hoffmann). | B | `L-HOFFSTEIN` |
| `P4.13` | Direct DIY observation of `P4.10` at shop scale: with excess airflow, *"unwanted swirls in the waste bin, pulling up dust and moving it straight to the filter tube"*. Also, light chips get sucked back into the dip tube **as the bin fills** — i.e. re-entrainment is a function of fill level, not just geometry. | D | `S-CD-inlets`, `S-MTL §09:29` |
| `P4.14` | Bin geometry mattered more than any cyclone-body change in one DIY series: switching to a **larger, round** bin was the community's top recommendation and was adopted. A collapsed bin instantly routed all dust to the filter. | D | `S-CD-cyclone2` |

## 4.3 Dust-outlet countermeasures — comparative

| ID | Device | Mechanism | Reported effect | Tier | Src |
|---|---|---|---|---|---|
| `P4.15` | **Dipleg / downcomer tube** below the cone | extends separation space, weakens back-mixing | efficiency increases notably; optimum length ≈ half the cyclone height; vortex end should sit **exactly at the dipleg end** | A | `L-OBERMAIR`, `L-KAYA09`, dipleg RSM studies |
| `P4.16` | **Apex / counter-cone insert** in the hopper throat | shields the pile from the vortex | effect on classification decreases at high inlet velocity; shape and height both matter | A | Yoshida et al. (2001/2003/2010) via `S-KARAGOZ13 §1` |
| `P4.17` | **Vortex stabiliser plate** (flat disc, downturned rim, dia < body) below the cone | gives the vortex tail a fixed attachment point; suppresses PVC and back-mixing | −11.5 %/−10.9 % on the two swirl peak frequencies; −24.8 % rotational KE in the collector, −14.2 % in the body; **costs pressure drop** | A | Wasilewski / Rafiee, patent literature |
| `P4.18` | **Expansion chamber** between cone and bin | reduces the chance the vortex end sweeps a wall | reduced re-entrainment | C | dust-receiver practice |
| `P4.19` | **Vortex limiter plate, adjustable** (`S-KARAGOZ13`) | terminates the vortex at a chosen height | up to +5 % efficiency; `x50` minimum tunable to flow | A | `S-KARAGOZ13` |
| `P4.20` | **Baffles in a shared hopper** (multicyclone) | suppress inter-cell circulation | suppressed circulation, but recovered **less than half** the efficiency gap vs a single cell | A | parallel-cyclone flow visualisation |
| `P4.21` | Counter-warning: a vortex breaker can **create new re-entrainment zones above the stopper**, and anything that impedes the natural vortex formation weakens it. Killing the vortex generally reduces collection. | B | `L-HOFFSTEIN`, secondary |
| `P4.22` | A small amount of back-mixing is **beneficial** to downward-moving particles, though not to collection efficiency. | B | `L-HOFFSTEIN` |

## 4.4 The `S-KARAGOZ13` conclusion set — applied to a printed shop device

Restated from `S-KARAGOZ13 §5` because it is unusually directly transferable:

| ID | Original conclusion | Relevance here |
|---|---|---|
| `P4.23` | Particles accumulating on internal surfaces increase roughness and degrade a conventional cyclone; this "rarely or never" happens in the double-cylinder design because the friction surface and the separation surface are different components. | FDM parts start rough (`P7.18`, `P7.19`) and wood dust is sticky/static-prone (`P1.46`). A geometry whose *working* surface is not the *friction* surface is attractive. |
| `P4.24` | In a conventional cyclone, particles that have fallen onto internal surfaces can be dragged back into the inner vortex; not so in the double-cylinder design. | Directly the `P4.10` loss path. |
| `P4.25` | The design's length can be increased easily; a conventional cyclone's cannot. | A printed device is length-modular by nature (see `P7.23`–`P7.25` bed-height splitting). |
| `P4.26` | Extra separation duration is obtained by adding length **without extra pressure drop**. | Confirms `P4.09`. |
| `P4.27` | Dust in the bin can be discharged easily and continuously. | Bin ergonomics dominate DIY satisfaction (`P4.14`). |
| `P4.28` | There is an optimum length for each flow; efficiency falls above **and** below it. | The core design tension for variable-duty shop use (`P3.18`). |

## 4.5 Open contradiction

| ID | Contradiction | Status |
|---|---|---|
| `P4.29` | `P4.19` (limiter plate: +5 %, Δp unchanged) vs `P4.17` (stabiliser plate: costs Δp) vs `P4.21` (obstructions weaken the vortex). All three are about placing a plate in the lower separation space. | Unresolved. Likely distinguished by whether the plate is **inside the swirl** (obstruction) or **at the natural vortex end** (termination). Logged in [phase-09](phase-09-validation.md) as `V9.07`. |

## 4.6 The collection vessel as a structural component (answers `Q5`: 5-gallon bucket)

Vessel decided: **standard 5-gallon bucket now, custom vessel later.** Under the shop-vac regime
(`P8.36`: 13–22 kPa sealed) this is the governing structural part, not an accessory (`P7.08`, `P8.52`).

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P4.30` | **Standard big-box 5-gallon buckets collapse under a shop vac + cyclone.** This is a well-documented, commonly reported failure, not a corner case. One report: bucket crushed and *"nearly everything passed straight through to the vac"* — matching `P7.07` exactly (structural failure = total separation failure, not partial). | C/D | `W-BUCKET` |
| `P4.31` | **The lid is frequently the actual failure point, not the walls.** DIY fixes that worked: 6 mm MDF or ½" plywood stiffener under/over the lid, with the cyclone mounting holes drilled through the reinforcement. | D | `W-BUCKET` |
| `P4.32` | Wall-thickness rating (mils) is moulded into the bucket bottom and varies by supplier. One collapse was resolved by moving to a **9-mil** bucket. Oneida's purpose-built vessel is up to **40 % thicker** than a standard bucket, in anti-static resin, with a latched reinforced lid. | C | `W-BUCKET` |
| `P4.33` | Simplest wall fix reported: **bucket-in-bucket nesting**. No fabrication, doubles the effective wall. | D | `W-BUCKET` |
| `P4.34` | **Restricted inlets amplify the collapse risk** — the more the intake is choked, the closer the vessel sits to the vac's sealed pressure. Reported case pairing a 2.25" vac hose with a 1.25" intake. This directly implicates `P8.60`: the WD06701's 1-7/8" hose is already the restricting element, so the bucket sits nearer sealed pressure than a 2.5"-hosed system would. | D/E | `W-BUCKET` + `P8.60` |
| `P4.35` | Outcomes vary by bucket quality — some users never collapse one. Do not treat a single successful sample as validation. Reducing suction (where the vac allows) also mitigates. | D | `W-BUCKET` |
| `P4.36` | Geometry is favourable: a 5-gal bucket is ~286 mm across vs a `D ≈ 120 mm` cyclone (`P8.59`), so the cone tip discharges into a vessel ~2.4× the body diameter. That is a large expansion chamber by `P4.18`, and consistent with the `P4.14` finding that a larger round bin outperformed a small one. **The bucket is aerodynamically good and structurally bad.** | E | derived |
| `P4.37` | Fill-level coupling still applies (`P4.13`): re-entrainment worsens as the bucket fills, and stage performance is gated by bin state (`P6.09`). Usable volume is less than nominal — headroom below the cone tip is functional, not wasted. | A/D | `P4.13`, `P6.09` |
| `P4.38` | Design consequence: **the lid is the part to design, and it is a printed part.** It carries the cyclone, takes the vacuum load, and forms the seal. It should be treated as the primary structural deliverable of build 1, with `M1`/`M2` (buckling, ribbing) applied to it rather than to the cyclone shell. | E | derived from `P4.30`–`P4.32`, `P8.52` |

## 4.7 Vessel substitution: metal pail or larger barrel

Triggered by `P4.30`–`P4.38`. Candidates: a 5-gal steel pail with lever-lock lid, and a 35-gal HDPE
open-top drum with a moulded lid clamped by a steel lever-locking ring.

### 4.7.1 Method

Two bounds are used. The long-cylinder form is a lower bound and turned out to be the wrong tool
here (`P4.40`); the short/intermediate-shell form is the working model and it validates against
observed field behaviour (`P4.41`).

```
# LC -- long-cylinder (Bresse / Levy), unstiffened, infinite length. LOWER BOUND.
    p_cr = 2E/(1-nu^2) * (t/D)^3
# WT -- Windenburg-Trilling short/intermediate shell. WORKING MODEL for L/D <~ 2.
    p_cr = 2.6*E*(t/D)^2.5 / ( (L/D) - 0.45*sqrt(t/D) )
#      L = unstiffened bay length: full height if unribbed, else spacing between rolling hoops.
# E, nu:  HDPE 1.0 GPa short-term / 0.35 GPa long-term (creep) / nu 0.42
#         steel 200 GPa / 0.30 (no room-temperature creep)
# Tier E throughout.
```

| Vessel | `t` mm | `D` mm | bay `L` mm | `t/D` | LC | **WT** | verdict vs 13–22 kPa |
|---|---|---|---|---|---|---|---|
| 5-gal HDPE bucket, short-term | 1.8 | 290 | 380 | 0.0062 | 0.6 kPa | **6.2 kPa** | at risk |
| 5-gal HDPE bucket, **crept** | 1.8 | 290 | 380 | 0.0062 | 0.2 | **2.2 kPa** | at risk |
| bucket-in-bucket, crept | 3.6 | 290 | 380 | 0.0124 | 1.6 | **12.4 kPa** | marginal |
| 35-gal HDPE drum, crept | 3.5 | 480 | 700 | 0.0073 | 0.3 | **2.9 kPa** | at risk |
| 55-gal HDPE open-head, crept | 3.5 | 571 | 889 | 0.0061 | 0.2 | **1.8 kPa** | at risk |
| 5-gal steel pail, 24 ga | 0.61 | 290 | 380 | 0.0021 | 4.1 | **82 kPa** | **safe** ×4 |
| 30-gal steel drum, 20 ga, 2 hoops | 0.91 | 505 | 250 | 0.0018 | 2.6 | **151 kPa** | **safe** ×7 |
| 55-gal steel, 18 ga, **no** hoops | 1.21 | 571 | 851 | 0.0021 | 4.2 | **73 kPa** | **safe** ×3 |
| 55-gal steel, 18 ga, 2 hoops | 1.21 | 571 | 284 | 0.0021 | 4.2 | **226 kPa** | **safe** ×10 |
| 55-gal steel, 18 ga, 3 hoops | 1.21 | 571 | 213 | 0.0021 | 4.2 | **305 kPa** | **safe** ×14 |
| 55-gal steel, 20 ga, 2 hoops | 0.91 | 571 | 284 | 0.0016 | 1.8 | **110 kPa** | **safe** ×5 |

| ID | Claim | Tier |
|---|---|---|
| `P4.39` | Sensitivity, `WT` form: `p_cr ∝ E·(t/D)^2.5 / (L/D)`. **Doubling wall ≈ ×5.7. Halving the unstiffened bay length ≈ ×2.** Steel vs HDPE at equal `t/D` and bay = **×35** in practice (not the ×200 that raw modulus suggests, because HDPE's `t/D` is larger). | E (verified) |
| `P4.40` | **Correction to an earlier reading in this corpus.** The long-cylinder formula predicted that every candidate collapses, which contradicts the fact that buckets survive normal operation. It was the wrong model: these are short shells (`L/D` 0.4–1.8) with heavy end restraint and rolled beads. The Windenburg-Trilling form is the right one and it reproduces observed behaviour — a bucket at **2.2–6.2 kPa** survives ordinary running (a few kPa) and collapses on blockage (13–22 kPa, `P8.53`). Use `WT`. | E |
| `P4.41` | **`WT` is validated by matching the failure mode, not just the failure.** It predicts the bucket sits *between* normal and blocked pressure — which is exactly why bucket collapse is reported as intermittent and blockage-triggered rather than immediate. That agreement is the reason to trust the steel numbers. | E |
| `P4.42a` | **HDPE creep is a distinct failure path.** Long-term modulus is ~⅓ of short-term, so `p_cr` drops ~3× under sustained load: 6.2 → 2.2 kPa for a bucket. This explains the common report that a bucket *"worked at first"* and failed later. **Steel does not creep at room temperature** — the whole failure mode disappears. | E |
| `P4.43a` | Rolling hoops are worth **×3** on a 55-gal steel drum (73 → 226 kPa for 2 hoops). Confirms `M2`/`P7.03`: ring stiffeners beat wall thickness. It also explains why field results vary so much by supplier (`P4.35`) — bead count and depth vary more than wall thickness does. | E (verified) |

### 4.7.2 The counter-intuitive result on size

| ID | Claim | Tier |
|---|---|---|
| `P4.42` | **Plastic containers hold `t/D` roughly constant as they scale** — 5-gal bucket 0.0062, 35-gal 0.0073, 55-gal 0.0061. Under `WT` the longer unstiffened bay then makes bigger plastic **worse**: 6.2 kPa (5-gal) → 2.9 (35-gal) → 1.8 (55-gal) at equal creep state. **A larger plastic drum is a structural downgrade, not an upgrade.** | E (verified) |
| `P4.43` | The same `t/D` invariance holds within steel (24-ga 5-gal pail = 0.0021, 18-ga 55-gal = 0.0021) — but steel drums carry **rolling hoops**, which shorten the bay and recover far more than the added diameter costs. **Size is not the variable; material, gauge and hoop spacing are.** | E |
| `P4.44` | **Gauge is therefore the question to ask of any metal pail, and it is usually not published** — the ATERET 5-gal metal bucket lists no gauge or wall thickness (`W-VESSEL`). At 24 ga it is a ×7 improvement; at 29 ga it is no better than the plastic bucket it replaces. Corroborating warning already in the corpus: thin galvanised cans dent inward and commonly need a band clamp at the rim. **Do not assume "metal" means "stiff".** | C/E |

### 4.7.3 What the lever-ring drum actually buys

| ID | Claim | Tier |
|---|---|---|
| `P4.45` | The photographed 35-gal drum's **steel lever-locking ring is a stiffening ring placed exactly at the mouth** — the highest-stress, least-restrained location, and the one that governs lid seating. It is the single best structural feature of any candidate here, and it is free. | E |
| `P4.46` | It also supplies a **moulded, gasketed, clamped lid**. That removes `P4.31` (lid is the usual failure point) and largely removes `P4.38` (printed lid as the primary structural deliverable). The printed part reduces to a cyclone-mounting adapter through the existing lid — a much smaller structural problem. | E |
| `P4.47` | Aerodynamically better: bin/cyclone diameter ratio goes 2.4 → 4.0. Larger, rounder bins measured better (`P4.14`) and a bigger expansion chamber reduces vortex-end wall sweep (`P4.18`). **No upper bound on useful bin diameter was found in any source** — flagged as unknown, not as endorsement. | E |
| `P4.48` | Fill-level coupling (`P4.37`) strongly favours the larger vessel. CNC routing produces bulky chips; 5 gal ≈ 19 L fills fast, and re-entrainment worsens as it fills. 35 gal is ~7× the emptying interval. | E |
| `P4.49` | Against it: **35 gal of wood dust is 24–33 kg** (at 180–250 kg/m³ bulk density) — an awkward two-hand lift from a drum with no good grip. Plus floor space. Mitigations: a dolly, or simply not filling it. | E (computed) |
| `P4.50` | 35 gal is **grossly oversized relative to the airflow**: at 40–70 CFM (`P8.57`) the vessel is not a capacity constraint at any plausible duty. Its value is emptying interval and structure, not volume. | E |

### 4.7.4 The 55-gallon drum specifically

| ID | Claim | Tier |
|---|---|---|
| `P4.53` | **A standard open-head 55-gal steel drum ends the structural problem outright.** 18 ga with 2 rolling hoops gives `p_cr ≈ 226 kPa` against a 13–22 kPa worst case — a **×10 margin**. Even 20 ga gives ×5, and even with the hoops ignored it gives ×3. No reinforcement, no printed structure, no relief valve strictly needed. | E (verified) |
| `P4.54` | The bolt-ring or lever-ring closure supplies a **gasketed, clamped, moulded lid** — same benefit as `P4.46`, so the printed part reduces to a mounting adapter. This is also the vessel commercial cyclones (Oneida, Clear Vue, Grizzly class) are designed to sit on, so adapter patterns and precedent exist. | C/E |
| `P4.55` | Steel is groundable (`P4.51`) and does not creep (`P4.42a`). Both plastic failure paths vanish. | E |
| `P4.56` | Aerodynamically the best of any candidate: bin/cyclone diameter ratio **4.8** at `D = 120 mm`, and enough headroom that the fill-level coupling of `P4.37` effectively never engages. Still subject to `P4.47` — **no upper bound on useful bin diameter was found in any source.** | E |
| `P4.57` | **The cost is entirely on the handling axis. 208 L of wood dust is 37–52 kg** — not liftable, not tippable by one person. A 55-gal drum is a vessel you must empty *in place*: scoop, shop-vac out, or use a liner. | E (computed) |
| `P4.58` | **Liner bags are the obvious answer and they do not work unaided on the vacuum side** — a bag inside a vessel under 13–22 kPa is drawn inward and up toward the cone. Commercial practice is a wire cage or a rigid inner bin to hold the liner off the wall. Adds back the complexity the drum was chosen to avoid. Not researched further; deferred. | E |
| `P4.59` | Footprint 571 mm dia × 851 mm tall. With `H = 480 mm` of cyclone plus a ~80 mm lid/adapter the roof sits at **~1.41 m**, inlet ~1.2 m. Acceptable in a shop; convenient at bench height for a CNC. Needs a drum dolly for `P4.57`. | E (computed) |
| `P4.60` | **Forward-compatibility warning.** A single 55-gal drum shared by an *n*-cyclone LVHP array (`U2`, `P8.66`) is precisely the shared-open-hopper configuration the literature says fails (`P6.20`, `P6.11`, `P6.12`). If the array path is taken, the drum needs internal dividers — one sealed sector per cell — or separate vessels. Decide this **before** committing to a lid pattern. | A/E |
| `P4.61` | Judgement: 55 gal is **overkill on the one axis that is already solvable and worse on the axes that are not.** A **20–30 gal steel drum of the same construction** keeps a ×5–7 structural margin, keeps the clamped lid, keeps groundability, and brings contents down to 14–28 kg. That is the better engineering choice unless emptying frequency is the dominant complaint. | E |

Contents mass by size, wood dust at 180–250 kg/m³:

| Vessel | Volume | Mass when full |
|---|---|---|
| 5 gal | 19 L | 3.4–4.7 kg |
| 20 gal | 76 L | 14–19 kg |
| 30 gal | 114 L | 20–28 kg |
| 35 gal | 132 L | 24–33 kg |
| 55 gal | 208 L | **38–52 kg** |

### 4.7.5 Ranking for build 1

**Superseded by §4.8.4** once handling was weighted alongside structure. Structural ranking retained
here; final recommendation is `P4.77`.

| Rank | Option | `p_cr` margin | Contents | Rationale |
|---|---|---|---|---|
| 1 | **5-gal steel pail, ≥ 24 ga**, lever-lock lid | ×4 | 3.4–4.7 kg | **Now first** (`P4.77`): adequate structure, groundable, trivial to empty. Blocked only on the unpublished gauge — at 29 ga it is no better than plastic (`P4.44`). |
| 2 | **55 gal open-head steel drum** on a dolly | ×10 | 38–52 kg | Strongest and best aerodynamically (`P4.53`, `P4.56`); the size commercial cyclones are built around. Empty in place with a rim-clamped liner (`P4.73`). Choose if emptying *frequency* is the complaint. |
| 3 | 20–30 gal open-head steel drum | ×5–7 | 18–28 kg | Structurally fine, ergonomically the worst of both (`P4.76`). Demoted from rank 1. |
| 4 | **Bucket-in-bucket, existing 5-gal** | ×0.6 *(marginal)* | 3.4–4.7 kg | 12.4 kPa crept vs a 13–22 kPa worst case — *borderline, not safe*. Zero cost, available today. Needs a reinforced lid (`P4.38`) and ideally a relief valve (`P4.52`). |
| 5 | Larger **plastic** drum (35 / 55 gal HDPE) | ×0.1–0.2 | 24–52 kg | **Worse than the 5-gal bucket** (`P4.42`). Rejected. |
| 6 | Single standard 5-gal bucket | ×0.1–0.3 | 3.4–4.7 kg | The documented failure case (`P4.30`). |
| 7 | **27-gal rectangular storage tote** | **×0.002–0.02** | 18–26 kg | **Rejected** — flat panels fail in bending at ~0.1–1" H₂O (`P4.64`). Different structural class, not a weaker drum (`P4.62`). Usable only *inside* the vacuum boundary, and even then the geometry does not fit (`P4.71`). |

| ID | Claim | Tier |
|---|---|---|
| `P4.51` | Cross-cutting: **a metal vessel is groundable and an HDPE one is not.** Given `P7.31`–`P7.32` (static corrupting both behaviour and measurement) and that a bleed path is the accepted compromise for insulators (`P7.36`), a steel vessel gives a genuine electrical benefit that neither plastic option can. | E |
| `P4.52` | Whichever vessel is chosen, `P8.53` stands: the design load case is **blocked hose with the motor running**, and the cheapest mitigation is not structural at all — a **relief/bleed valve** that caps the vacuum the vessel can ever see. Not yet researched; recorded as a deferred branch. | E |

## 4.8 Rectangular storage totes — categorically unsuitable as a pressure boundary

Candidates: HDX 27-gal Tough Storage Tote; Centrex/Commander 27-gal Tough Box. Both are ribbed
polypropylene boxes with snap-on lids.

### 4.8.1 Why the physics is different

| ID | Claim | Tier |
|---|---|---|
| `P4.62` | **A cylinder resists external pressure in membrane compression; a flat panel has no membrane action and resists purely in bending.** These are different mechanisms with different scaling, and the second is far weaker. A tote is not a weaker drum — it is a different structural class. | E |
| `P4.63` | Flat-panel governing relation: `p ∝ E·t³ / b⁴`, where `b` is the **short span** of the panel. **Span is punishing to the fourth power.** | E |

```
# Roark, rectangular plate, uniform pressure, all edges simply supported:
#   D_flex = E*t^3 / (12*(1-nu^2))
#   w_max  = alpha * p * b^4 / D_flex      b = SHORT span
#   alpha: 0.00406 (a/b=1.0) ... 0.01106 (2.0) ... 0.0142 (long)
# PP: E ~ 1.3 GPa, nu 0.42.  Tier E.
```

### 4.8.2 Numbers for a 27-gal tote (≈777 × 511 × 366 mm, PP, t ≈ 2.5 mm)

| Panel | span | pressure for 10 mm dish | deflection at 13 kPa |
|---|---|---|---|
| Lid / bottom (777×511) | 511 mm | **35 Pa (0.14" H₂O)** | 3.7 m (nonsense — total collapse) |
| Side (777×366) | 366 mm | 101 Pa (0.41") | 1.3 m |
| End (511×366) | 366 mm | 149 Pa (0.60") | 0.87 m |

| ID | Claim | Tier |
|---|---|---|
| `P4.64` | **The lid visibly dishes at ~35 Pa — 0.14" H₂O.** Crediting the moulded ribs a generous ×5–10 still lands at ~1.1" H₂O. The reference point is a crept 5-gal bucket at **2200 Pa (8.8" H₂O)**, and the worst case is 13 000–22 000 Pa. **A 27-gal tote is roughly 10–60× worse than the bucket it would replace, and 3–4 orders of magnitude short of the design load.** | E (verified) |
| `P4.65` | Thickening does not save it: at a 511 mm span you need **t ≈ 12 mm** to reach even 15.7" H₂O. Moulded totes are 2–3 mm. | E (verified) |
| `P4.66` | Span reduction does save it, steeply: 511 → 250 mm is ×18; 511 → 150 mm is ×137. **This is why small thick boxes work where big thin ones cannot** — and it explains why the Festool-bin-based DIY separators in `S-CD` succeeded (short spans, thick walls, and only ~2.5 kPa of dust-collector vacuum, not 13–22 kPa). Do not generalise from those to a 27-gal tote. | E |
| `P4.67` | Secondary defects, independent of the panels: a **snap lid has no gasket and no clamp**, so it neither seals (`P7.14`: leakage is a performance loss) nor resists lift-off; and the tote's ribbing is engineered for *internal* load — contents pushing out and stack loading — not external pressure. | E |
| `P4.68` | **Verdict: rejected as a pressure boundary.** No reinforcement short of building a plywood box around it would qualify, and that is more work than buying a drum. | E |

### 4.8.3 The useful reframing — put the totes inside the vacuum

| ID | Claim | Tier |
|---|---|---|
| `P4.69` | **Anything wholly inside the vacuum boundary sees no pressure differential and therefore needs no strength at all.** An open container inside the vessel equalises through its own open top. This decouples *structure* from *handling* completely: one rigid pressure boundary, plus an arbitrarily flimsy inner container chosen purely for how easy it is to lift and dump. | E |
| `P4.70` | `P4.69` is the direct answer to the emptying problem that motivated this branch, and it rehabilitates cheap commodity containers — just not as the shell. | E |
| `P4.71` | Geometry constraint on `P4.69`: the inner container must **capture essentially the full cone-tip discharge footprint**, or dust piles in the annulus outside it and has to be cleaned separately. A 290 mm bucket inside a 505 mm drum leaves a large dead annulus. A rectangular 777 mm tote does not fit inside any drum at all — **the proposed totes cannot serve as inner liners either.** | E |
| `P4.72` | Workable inner options: (a) a **drum liner bag clamped under the closure ring**; (b) a second thin pail or fibre insert sized near the drum ID; (c) nothing — scoop or vacuum it out in place. | E |
| `P4.73` | Refines `P4.58`. A rim-clamped bag inside a *sealed* vessel is pressure-neutral and stable. The failure mode is **air leaking in behind the bag** — between bag and wall — which then pushes it inward and up toward the cone. So bag liners work **only if the vessel is genuinely airtight**, which is the same requirement the separator already has (`P7.14`). Reported bag-collapse problems are a leak symptom, not an inherent objection. | E |

### 4.8.4 Emptying, reconsidered from first principles

| ID | Claim | Tier |
|---|---|---|
| `P4.74` | The emptying difficulty was **created by the 55-gal choice**, not inherited from the problem. Contents mass: 5 gal = 3.4–4.7 kg; 27–30 gal = 18–28 kg; 55 gal = 38–52 kg. | E (computed) |
| `P4.75` | Router chips are bulky and light (bulk density below the 180–250 kg/m³ used for sawdust), so a 5-gal vessel represents many jobs of hobby CNC work, and emptying it is a light, one-hand, seconds-long task. | E |
| `P4.76` | **The 20–30 gal band is the worst of both:** 18–28 kg is too heavy to empty casually but the volume is still small enough to need emptying regularly. It has no ergonomic sweet spot — its earlier rank-1 placement (`P4.61`) was made on structural grounds only and is **superseded**. | E |
| `P4.77` | Revised recommendation is bimodal. **Small:** 5-gal steel pail, ≥24 ga, ×4 structural margin, trivial emptying, empty often. **Large:** 55-gal steel drum on a dolly, ×10 margin, essentially never emptied, worked as an empty-in-place vessel with a rim-clamped liner (`P4.73`). Choose by whether emptying *effort* or emptying *frequency* is the real complaint. Avoid the middle. | E |

## 4.9 Vessel acquired: 2 × Greif 30-gal open-head steel drum, plain flat lid

`Q5` **CLOSED (2026-08-01).** Two used UN-marked steel drums, dual-marked, flat plain lid, no bung.

### 4.9.1 UN mark decode

`1A2/X400/S/26/ USA/GBC4 47 26` and `1A2/Y1.4/150/26/ USA/GBC4 47 26`

| Field | Meaning | Tier |
|---|---|---|
| `1A2` | `1` drum, `A` steel, `2` **removable head** — confirms open-head with a closing ring | C |
| `X400/S/26` | `X` = Packing Group I performance (valid for PG I/II/III); `400` kg max gross mass; `S` = solids or inner packagings; `26` = manufactured **2026** | C |
| `Y1.4/150/26` | Second, **liquids** rating: PG II/III, specific gravity 1.4, **150 kPa hydraulic test pressure** | C |
| `USA/GBC4` | US authorisation, Greif manufacturer code (`47 26` = plant/serial data) | C |

| ID | Claim | Tier |
|---|---|---|
| `P4.78` | The dual mark is directly useful: a liquids rating means the drum has a **gasketed, sealed, pressure-tested closure**, which is the requirement `P7.14`/`P4.73` impose anyway. 150 kPa is an *internal* hydraulic test and does not bound external collapse, but it evidences seam and closure integrity. | E |
| `P4.79` | `26` = 2026 manufacture, so these are near-new despite being sold used. Closure gasket condition is likely good; verify it exists and is intact. | E |

### 4.9.2 Body — solved

Greif S30BR nominal ≈ 467 mm OD × 724 mm, 34 lb. Back-calculating sheet thickness from that mass
over the 1.405 m² shell area gives **t ≈ 1.1–1.3 mm (18 ga)**.

| `t` | no hoops | 2 rolling hoops | 3 hoops | margin vs 22 kPa (2 hoops) |
|---|---|---|---|---|
| 0.91 mm (20 ga) | 57 kPa | 175 kPa | 237 kPa | ×8 |
| 1.06 mm (19 ga) | 83 kPa | 258 kPa | 349 kPa | ×12 |
| **1.21 mm (18 ga)** | **116 kPa** | **360 kPa** | 487 kPa | **×16** |

| ID | Claim | Tier |
|---|---|---|
| `P4.80` | **The drum body is a non-issue.** Even at 20 ga and ignoring the rolling hoops entirely, it clears the 13–22 kPa worst case by ×2.6. With hoops at the estimated 18 ga it is ×16. No reinforcement, no relief valve required *for the body*. | E (verified) |

### 4.9.3 The flat lid is now the weak point — and it is the one flat panel left

**Confirmed by inspection: the lid is flat with a rolled edge and no bung, retained by a bolt ring.**

A plain flat lid is a **circular plate**, not a shell. `P4.62`/`P4.63` apply again: `σ ∝ p·a²/t²`.
Analysed as a clamped-edge circular plate, 467 mm, **no concentric beads** — the flat profile means
there is no bead credit to take, so the figures below are the operative estimate rather than a
conservative bound.

| `t` | permanent-set pressure | dish at 13 kPa | dish at 22 kPa |
|---|---|---|---|
| 0.91 mm | 5.1 kPa (20" H₂O) | 44 mm | 74 mm |
| 1.06 mm | 6.9 kPa | 28 mm | 47 mm |
| **1.21 mm** | **9.0 kPa (36" H₂O)** | **19 mm** | **31 mm** |
| 1.50 mm | 13.8 kPa | 10 mm | 17 mm |

| ID | Claim | Tier |
|---|---|---|
| `P4.81` | **An unbeaded 18-ga flat lid takes a permanent set at ~9 kPa — below the 13–22 kPa blockage case.** The body is ×16 safe and the lid is ×0.4. This exactly reproduces `P4.31` (lid is the failure point) on a vessel where the walls are no longer in question. | E (verified) |
| `P4.81a` | **The rolled edge and bolt ring justify the clamped boundary condition** used above — they are not extra margin on top of it. A simply-supported lid of the same thickness would deflect ~4.1× more and carry ~1.65× the peak stress. The favourable case is already assumed. | E (verified) |
| `P4.81b` | A **bolt ring** (rather than a lever ring) is the stronger closure: even circumferential clamping, high and adjustable preload, and a convenient bonding point for grounding (`P4.90`). It also resists the curl being drawn radially inward as the lid dishes, which is real restraint the plate model ignores — a modest unquantified credit. | E |
| `P4.81c` | **Serviceability, not yield, is the binding limit.** With a gasketed closure, the lid only has to dish enough to unseat the gasket for the vessel to leak — and leakage is a direct performance loss (`P7.14`), not merely a mess. A 5 mm dish occurs at **~3.5 kPa (14" H₂O)** on an 18-ga lid, which is reachable in *ordinary restricted-inlet operation*, not just at blockage. **Stiffening the lid is therefore a normal-operation requirement, not only a failure-case one.** | E (verified) |
| `P4.81d` | Gasket present and seated is a precondition for `P4.73` (a rim-clamped bag liner is stable only in a genuinely airtight vessel) and for `P8.28`-class leak losses. Inspect it; it is a wear item and these drums are used. | E |
| `P4.82` | Consequence: `P4.38` stands unchanged — **the lid is the structural deliverable**, and it is the part the cyclone mounts through anyway. Effort belongs there, not on the drum and not on the cyclone shell. | E |
| `P4.83` | Fixes, by leverage (`σ ∝ p·a²/t²`, so halving unsupported radius = ×4, doubling thickness = ×4): | E (verified) |

| Fix | Effect |
|---|---|
| Ring support at r = 150 mm | ×2.4 → 22 kPa |
| Central support at r = 117 mm | ×4.0 → 36 kPa |
| 3 radial ribs, effective r = 80 mm | ×8.5 → 76 kPa |
| 9 mm plywood disc bonded to the lid | ×6.6 → 59 kPa |
| **12 mm plywood disc** | **×11.8 → 106 kPa** |
| 18 mm plywood disc | ×26.6 → 238 kPa |

| ID | Claim | Tier |
|---|---|---|
| `P4.84` | **The cyclone mounting flange should be the stiffener.** A large-diameter printed flange with radial ribs running out to the closing ring converts the required mount into the required reinforcement — one part, two jobs. This is the cheapest available path and it is squarely `M2` (ring stiffeners over thickness). | E |
| `P4.85` | `P4.52` (relief/bleed valve) is now clearly worth doing: capping the achievable vacuum below ~9 kPa protects the lid without any structure at all, and protects everything else too. **Promoted from deferred to a build-1 item.** | E |

### 4.9.3a CORRECTION: the lid does not need reinforcement

`P4.81`–`P4.83` are **wrong**. Retained above for the audit trail; superseded here.

| ID | Claim | Tier |
|---|---|---|
| `P4.92` | **The error: small-deflection plate theory was applied ~30× outside its validity.** It holds only while `w < t/2` — for an 18-ga lid that is 0.60 mm, i.e. **423 Pa (1.7" H₂O)**. It was applied at 13 000 Pa. Every deflection and stress figure in `P4.81` is therefore meaningless. | E |
| `P4.93` | **Correct treatment: large-deflection (membrane) behaviour.** Once a flat plate dishes past about its own thickness it stops acting in bending and carries load in membrane tension — a shallow dome, which is vastly stiffer. Timoshenko, clamped circular plate: `w = 0.662·a·(p·a/E·t)^(1/3)`, `σ = 0.423·(E·p²·a²/t²)^(1/3)`. | B/E |
| `P4.94` | **Result for this drum.** 18-ga lid at 13 kPa: **3.6 mm deflection, 46 MPa membrane stress** against ~250 MPa yield. At 22 kPa: 4.3 mm, 65 MPa. Even a 20-ga lid at 22 kPa gives 4.7 mm and 78 MPa. **Elastic throughout — it oil-cans a few millimetres and springs back.** Small-deflection theory had predicted 19–31 mm and yield at 9 kPa. | E (verified) |
| `P4.95` | The one genuine concern is the **hole cut for the cone tip**: it interrupts membrane continuity at the centre and is a stress raiser. That is exactly what the printed socket flange bolted around it restores — so the flange should be a reasonable diameter (150 mm here) and bolted, not glued or point-mounted. | E |
| `P4.96` | **Field corroboration.** The failures reported in the literature search are plastic buckets and thin galvanised trash cans (`P4.30`, `P4.44`). **No reports of steel drum lids collapsing under shop vacs were found**, despite this being an extremely common configuration. The corrected analysis explains why the empirical record looked inconsistent with `P4.81`: `P4.81` was wrong. | D/E |
| `P4.97` | Also revised: the WD06701 is a small 6-gal / 5.8 A machine, so its sealed pressure sits at the **low end** of the generic 53–90" H₂O band — realistically **11–14 kPa**, not 22. The design load was overstated as well as the response. | E |
| `P4.98` | ~~`P4.81c`~~ **withdrawn.** The claim that a 5 mm dish unseats the rim gasket at 3.5 kPa was asserted without a mechanism. The gasket sits in the curl and is clamped circumferentially by the bolt ring; central dishing puts the lid into membrane tension, which pulls the rim *inward against* the ring rather than releasing it. No evidence of gasket release from central dishing was found. | E |
| `P4.99` | **What survives.** The bolt ring is still the right closure; the socket flange should still spread load and reinforce the hole (`P4.95`); and the relief valve (`P4.85`) is still worth fitting — it now protects the vacuum motor and the printed parts rather than the lid. **Dropped entirely: the plywood stiffener disc.** | E |
| `P4.100` | Method lesson for the rest of this corpus: **check the validity range of a closed-form solution before trusting its output**, especially when the answer disagrees with the empirical record. Here the disagreement (`P4.96`) was the signal and it was initially explained away rather than investigated. | E |

### 4.9.4 Two drums — this reverses `P4.76`

| ID | Claim | Tier |
|---|---|---|
| `P4.86` | **`P4.76`/`P4.77` ("avoid 20–30 gal") is superseded.** That verdict assumed one vessel emptied in place. With two drums the workflow is **swap, not empty**: pull the full drum, drop in the empty one, empty the full one outdoors at leisure. The ergonomic objection to the middle size disappears. | E |
| `P4.87` | Contents mass at 114 L: **11 kg** (router/planer shavings, ~100 kg/m³), 17 kg (mixed chips), 28 kg (settled sawdust). For CNC chip duty this is a tippable one-person load, not the 38–52 kg of a 55-gal drum. | E (computed) |
| `P4.88` | Two vessels also satisfy `U5` for a two-cyclone LVHP array without internal dividers — one isolated underflow per cell, which is exactly what `P6.20` requires. The purchase is forward-compatible with the array path at `n = 2`. | E |
| `P4.89` | Stack geometry: 724 (drum) + ~40 (ring/lid) + ~80 (adapter) + 480 (cyclone `H`) ⇒ **roof at ~1.32 m, inlet at ~1.15 m**. Convenient bench height for a CNC. Bin/cyclone diameter ratio **3.9** — a large expansion chamber (`P4.18`), and headroom enough that fill-level coupling (`P4.37`) barely engages. | E (computed) |
| `P4.90` | Steel is groundable (`P4.51`) and the closing ring is a convenient bonding point. Both plastic failure paths — creep (`P4.42a`) and non-conductivity — are gone. | E |

### 4.9.5 Prior contents — resolve before use

These are used drums carrying a PG-I solids rating and a liquids rating at specific gravity 1.4.
Something was shipped in them, and the UN mark describes the packaging, not the contents.

**Before putting these into service, identify what they previously held.** If the prior contents were
a flammable solvent, residue in the seams and chime combined with fine wood dust and a
universal-motor vacuum (which brush-sparks by design) is a genuinely hazardous combination. If the
drums are reconditioned, they have been cleaned and relined and this is not a concern.

If the prior contents cannot be established: wash out thoroughly, air until there is no solvent
odour, and inspect the chime and seams where residue collects. Do not skip this on the basis that
the drums look clean — `P4.91`.

| ID | Claim | Tier |
|---|---|---|
| `P4.91` | Prior contents of a used UN drum are not determinable from the UN mark. **CLOSED 2026-08-01: the drums have been washed and aired out.** Residual-contamination concern discharged. | C/E |

## Branch decisions taken from Phase 4

| Branch | Trigger | Goes to |
|---|---|---|
| Bin as a separator component, not an accessory; fill-level dependence | `P4.13`, `P4.14` | Phase 8, Phase 10 |
| Length-modularity is free performance | `P4.09`, `P4.25` | Phase 7 |
| Shared hoppers cross-talk | `P4.20` | Phase 6 |
