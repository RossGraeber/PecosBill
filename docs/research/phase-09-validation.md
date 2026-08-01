# Phase 9 — Validation, contradictions, and what the evidence does not support

This file is the corpus's skepticism ledger. Nothing here is resolved by preference; unresolved
items stay unresolved and are marked as such.

## 9.1 Contradiction log

| ID | Contradiction | Sides | Status / resolution |
|---|---|---|---|
| `V9.01` | Iozia & Leith core-diameter regression constants | `d_c = 0.52·D·(ab/D²)^-0.25·(De/D)^1.53` (widely cited) vs `0.47 … ^1.4` (also seen) | **Unresolved.** Likely a 1989-paper vs 1990-paper divergence. Primary is paywalled (403). Use 0.52/1.53 and flag. |
| `V9.02` | Best `Eu` model | `L-SINGH17` recommends Ramachandran > Shepherd-Lapple > Barth. A separate comparison found the full Muschelknautz method lowest-residual. Other reviews name Shepherd-Lapple or Stairmand best. | **Unresolved and probably unresolvable in general.** `L-SALCEDO01` handles it correctly: run several models, take the worst case as a design constraint, then measure. Adopt that. |
| `V9.03` | `S-TUD` equations (15), (19), (20) | Text extraction from the PDF mangles the inline fractions and radicals. | **Do not use as formulas.** They are pointers to VDI-Wärmeatlas / Muschelknautz-Klose. `S-TUD` eq.(14) and the geometry/parameter tables extracted cleanly and are usable. |
| `V9.04` | Stairmand high-gas-rate column values | Referenced by multiple secondary sources as column 5 of the standard 6-column table; numeric values not obtained from any source verified in this pass. | **Excluded from `P2.02`.** Do not quote from memory. |
| `V9.05` | Cone-only wall roughness | `L-KAYA11` lineage: roughness ↓ `vθ`, ↓ efficiency. One cone-specific study: roughness *enhanced* tangential and axial velocity. | **Unresolved.** Possibly a cone-vs-barrel distinction (the cone is where radius is shrinking and the boundary layer is thinnest). |
| `V9.06` | *(resolved)* `L-SALCEDO01` eq.(4) area-ratio orientation | As extracted, all five classical families violate it. | **Resolved by arithmetic** — the ratio is inverted; corrected form in `P2.21`. 5/5 families then fall inside the bracket, two exactly on its edges. |
| `V9.07` | Plates in the lower separation space | `P4.19` limiter: +5 %, Δp unchanged. `P4.17` stabiliser: costs Δp. `P4.21`: obstructions weaken the vortex and reduce collection. | **Unresolved.** Working hypothesis: a plate **at** the natural vortex end terminates it (good); a plate **inside** the swirl obstructs it (bad). Requires `Ln` to be known, which it usually isn't. |
| `V9.08` | Symmetrical double inlets | Some studies: ↑ tangential velocity, ↑ efficiency at equal area. Others: ↓ efficiency **and** ↓ Δp. | **Unresolved.** Literature is explicitly described as contradictory by reviewers. |
| `V9.09` | Wall texture direction | `P7.18` roughness harms. `P7.20` deliberate 0.5 mm riffles measured marginally better. | **Unresolved.** `P7.20` is a single uncontrolled test that its own author declined to draw conclusions from. |
| `V9.10` | Inlet area sizing rule | DIY rule (`P6.25`, `P6.26`): match total inlet area to duct area. Design theory (`P1.33`, `P8.16`): set inlet area to hit the family design velocity. | **Resolved in favour of theory.** These coincide only if the duct transport velocity equals the cyclone design velocity, and `P8.15` shows it does not (17.8–20.3 vs 12.2–16.3 m/s). The DIY rule preserves velocity where the design rule deliberately changes it. |
| `V9.11` | DIY efficiency claims above ~99.9 % | Claimed 99.95 %, 99.98 %, "close to 99.99 %". Instrument: a scale displaying 0.1 g but accurate to ~1 g, on captured masses of 0.36–3 g against feeds of 1.3–1.5 kg. | **Not supported.** At 1.5 kg feed, 99.99 % = 0.15 g escape, i.e. below the instrument's true resolution. The author identified this problem himself and mitigated by 5× averaging, which reduces random error but not the systematic offset between two scales that disagreed. **Treat everything above 99.9 % in `S-CD` as "at or beyond the noise floor".** |
| `V9.13x` | *(resolved)* Long-cylinder buckling formula predicted collapse of every candidate vessel, contradicting the fact that buckets survive normal running. | **Resolved** — wrong model for short, bead-stiffened shells. Windenburg-Trilling reproduces the observed blockage-triggered failure mode and is now the working model (`P4.40`, `P4.41`). |
| `V9.14x` | *(resolved)* Small-deflection plate theory predicted the steel drum lid yields at 9 kPa, contradicting the total absence of field reports of steel drum lids failing under shop vacs. | **Resolved — the theory was applied ~30× outside its validity window** (`P4.92`). Large-deflection membrane analysis gives 3.6 mm elastic deflection at 46 MPa (`P4.94`). The empirical record was right and the model was wrong. The plywood stiffener recommendation is withdrawn (`P4.99`). |
| `V9.12` | `W-PSU` standard-Lapple pressure-drop constant | Lecture notes give `Δp = 2621.44·ρ·Q²/D⁴`. Deriving from `Eu_SL = 16ab/De² = 8` for Lapple proportions and `vin = 8Q/D²` gives `Δp = 4ρvin² = 256·ρ·Q²/D⁴`. Ratio 10.24×. | **Unresolved; use the derived form.** The cut-size closed form from the same notes (`x50 = √(3μD³/(128π·Q·Δρ))`) **was** independently re-derived here from `x50_lapple` with `Ne=6, b=D/4, a=D/2` and matches exactly, so the notes are not generally unreliable — the discrepancy is isolated to the Δp constant. |

## 9.2 Evidence quality assessment of the DIY corpus

The `S-CD` series is the largest body of *quantitative, repeated, shop-scale* separator testing found.
It is also the source most likely to be over-trusted. Assessment:

| ID | Strength | Detail |
|---|---|---|
| `V9.13` | Purpose-built test rig | Removable weighable filter cartridge downstream (`P8.34`); U-tube manometer at multiple stations (`P8.33`); anemometer with a printed centring jig; feed metered by mass and timed. |
| `V9.14` | Repetition | 15 tests in one comparison; 7 and 9 tests across feed-rate sweeps; 5 replications adopted after discovering scale error. |
| `V9.15` | Honest negative reporting | Failures, collapsed bins, invalid tests, and the "classical mistake" of changing two variables at once are all reported rather than suppressed. |
| `V9.16` | Absolute-mass framing | `P6.07` reports g/kg rather than percentages — the correct framing at these efficiency levels. |

| ID | Weakness | Consequence |
|---|---|---|
| `V9.17` | Instrument resolution (`V9.11`) | Ceiling on credible claims ≈ 99.9 %. |
| `V9.18` | Confounded changes | Acrylic tube + neutral vane introduced in the same test; author flags it. Several "improvements" are never isolated. |
| `V9.19` | Static charge (`P7.32`) | Reused test dust produced *"almost unrealistically high"* results. At least one comparison was discarded for this reason. Charge state is an uncontrolled variable throughout. |
| `V9.20` | Device class | Most of the series tests a **centrifugal impeller separator** (`P2.31`), not a reverse-flow cyclone. Its results transfer as *system* evidence (bins, sealing, feed rate, filters), **not** as cyclone-geometry evidence. Only `S-CD-cyclone1` and `S-CD-cyclone2` test cyclones proper. |
| `V9.21` | Feed material not characterised to a PSD | Sieve fractions only (`P8.07`), and sieving understates fines (`P8.06`). No `x50` or grade curve was ever measured — only overall mass efficiency, which is loading- and PSD-dependent (`P1.39`, `P1.17`). |
| `V9.22` | No pressure-drop/efficiency pairing on the cyclone builds | Air speed and resistance measured, but the author's own instrument *"is just not capable to collect useful data behind the decimal point"* for the airflow comparison that mattered. |

| ID | Verdict |
|---|---|
| `V9.23` | Use `S-CD` for: failure modes, system losses, ergonomics, feed-rate sensitivity, relative direction of changes, and order-of-magnitude g/kg carry-over. **Do not** use it for: cut sizes, grade curves, absolute efficiencies above 99.9 %, or attributing a gain to a specific geometric feature. |
| `V9.24` | `S-MTL` is a build log, not a test: no quantified efficiency, no pressure measurement, and its only performance statement is qualitative (*"some small particles definitely reached the back, but it's not a lot"*, and *"that is honestly up to further testing"*). Use it for construction technique and for the multicyclone area-matching idea only. |

## 9.3 Claims deliberately **not** made

| ID | Non-claim |
|---|---|
| `V9.25` | No cut size is predicted for any candidate geometry. Every model in phase-01 §1.3 has known error bands that exceed the differences between candidate designs, and none has been calibrated for wood at `ρp ≈ 730` (`P8.03`). |
| `V9.26` | The 20 % neutral-vane improvement figure (`P5.11`) is a vendor claim with no published data and no independent replication (`P5.14`). It is recorded, not accepted. |
| `V9.27` | Commercial cyclone performance figures (Harvey 99.7 %, Oneida marketing) are unverified vendor claims; the one independent measurement in this corpus put a commercial cyclone at 99.9 % on shavings and below 99.5 % on MDF (`P6.06`). |
| `V9.28` | Nothing in this corpus establishes that a printed cyclone can outperform a moulded commercial one. The single DIY comparison favouring the printed unit (`S-CD-cyclone2`) is confounded (`V9.18`) and sits at the noise floor (`V9.11`). |
| `V9.29` | No claim is made about explosion risk beyond `P7.33`–`P7.34`. That is a regulatory question determined by whether the machine is commercial, not an engineering question resolved here. |

## 9.4 Verification performed in this corpus

| ID | What was checked | Method | Result |
|---|---|---|---|
| `V9.30` | Koch & Licht standard geometry table | Two independent page fetches reproducing the same compilation | Agreed on all 35 values |
| `V9.31` | `x50 ∝ √D` at fixed `vin` | Derived twice — once from `x50_lapple`, once from `S-TUD` eq.(14) | Agreed |
| `V9.32` | `W-PSU` closed-form Lapple cut size | Re-derived from `x50_lapple` with Lapple proportions and `Ne=6` | Exact match (`3μD³/(128π·Q·Δρ)`) |
| `V9.33` | `L-SALCEDO01` constraint `C3` | Evaluated against all 5 classical families both ways | Inverted form confirmed (`P2.21`) |
| `V9.34` | `L-SALCEDO01` constraints `C6`, `C8`, `C9` | Evaluated against Stairmand HE and Lapple | `C6` ✓, `C9` ✓ with margin, **`C8` violated by Stairmand HE** — downgraded to a preference (`P2.23`) |
| `V9.35` | `Eu_SL` for each classical family | Computed `16ab/De²` from `P2.02` table | 6.4–9.24; consistent with the 5–40 industrial range of `P1.24` |
| `V9.36` | `P8.12` duct CFM figures | Recomputed from duct area × velocity | 4"=349, 6"=785 CFM at 4000 fpm ✓ |
| `V9.37` | `L-SINGH17` Pareto structure | Read all 100 tabulated solutions, checked which variables were bound-pinned | `a`, `H`, `S`, `B` pinned; `De` monotone; `h` free (phase-03 §3.2 table) |

## 9.5 Deferred branches (candidate phases 11+)

| Branch | Why deferred | Priority for Stage 2 |
|---|---|---|
| Muschelknautz method (MM) full implementation from VDI-Wärmeatlas | primary source not held; `S-TUD` extraction incomplete (`V9.03`) | Medium — would give a loading-aware model, the one thing missing |
| CFD/DEM as a design tool | out of scope for Stage 1; `P3.03` notes cost | Low |
| Erosion and service life | not relevant at hobby duty | Low |
| Hydrocyclone literature | different `n`, different regime | None |
| Acoustics / noise | not raised by the brief | Low |
| Automatic bin-full detection | arises directly from `P6.09` + `P4.13` (fill level gates performance) | **High** — cheap and addresses a dominant failure mode |
| Anti-static filament / conductive liner | arises from `P7.31`–`P7.36` | Medium |
| Instrumented test rig design for Stage 3 | `V9.17` shows measurement is the binding constraint on iteration | **High** |
| Liner-bag support (cage or rigid inner bin) for a large drum on the vacuum side | `P4.58` — bags collapse inward under 13–22 kPa; needed only if a big drum is chosen | Medium |
| ~~Vacuum relief / bleed valve~~ | **Promoted to a build-1 item** (`P4.85`) — caps load below the lid's ~9 kPa set point | — |
| Short-shell external-pressure buckling with stiffening rings (real `p_cr`, not the long-cylinder bound) | `P4.40` shows the simple formula is unusable for absolute values; ribbed short shells need the proper treatment | Medium |
