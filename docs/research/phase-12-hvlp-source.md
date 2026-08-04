# Phase 12 — HVLP source (Shopmax SC0075) and the second cyclone duty

Scope: the SC0075 dust collector as a second, independent vacuum source, and the cyclone
design point it forces. **Decision (user, 2026-08-03): keep both source paths.** The
phase-11 LVHP drum vacuum remains a future build; the SC0075 path is now the active one.

Current layout: **CNC → cyclone drum (regenerated for SC0075 duty) → SC0075.**

Notation per [00-notation.md](00-notation.md). Phase-11 symbols reused (`WL`, `Q_o`).

## 12.1 Sources

| Key | Source | Tier basis |
|---|---|---|
| `S-H1` | Shopmax SC0075 HVLP dust collector, user-owned: 120 V, 0.74 HP (~550 W), rated 677 CFM, 3.94" (100 mm) hose ID | C (nameplate only — no fan curve, no static rating) |

## 12.2 Regime — the axes swap

The shop-vac and phase-11 sources are LVHP: pressure over-supplied 4–7×, flow scarce
(`P11.02`… §11.2). The SC0075 is the opposite machine.

| | Twin-900W (`P11.25`) | SC0075 |
|---|---|---|
| Sealed static | 81.8" H₂O (20.4 kPa) | ~7–8" H₂O (~2 kPa, typical 0.74 HP single-stage impeller) |
| Rated open flow | ~194 CFM (2 × 97) | 677 CFM (free-air marketing; see `P12.02`) |
| Expected duty flow | ~160 CFM | ~300–400 CFM |
| Scarce axis | flow | **pressure** |

| ID | Claim | Tier |
|---|---|---|
| `P12.01` | **Pressure is now the scarce axis.** Cyclone Δp becomes the dominant system loss: an HVLP impeller's steep fan curve trades flow for every inch of added static. The Δp budget for the cyclone is **≤ ~3" H₂O**; the `De/D`-narrowing logic of `S6`/`P8.61` (pressure cheap, spend it) inverts here. `S7` ("De/D is scale-invariant, don't re-decide") applied within the LVHP path only — a regime change re-opens it. | E |
| `P12.02` | **677 CFM is not a design input.** It is an unloaded free-air figure (`P8.37` discipline applies to dust collectors exactly as to shop vacs). Real delivered flow through hose + cyclone + bag is estimated 300–400 CFM. **350 CFM is adopted as the provisional design flow**, same pattern as `D4`. | C/E |
| `P12.03` | Objective for this duty is finally concrete (`Q3`): **heavy-chip dropout ahead of the impeller and bag** — a single-stage collector passes every chip through its fan; the cyclone converts it to a two-stage machine. Mass removal, not fine cut. `x50` ≈ 6–7 µm is acceptable. | E |

## 12.3 Design point

At fixed inlet ratios Δp depends only on `vin` (`Eu` = 8 heads, Shepherd-Lapple):
Δp = 4.95" at 16 m/s, **3.0" at 12.5 m/s**. So the HVLP design point sits at the **low
end of the `O1` band**, not at the 1D3D family velocity.

| ID | Claim | Tier |
|---|---|---|
| `P12.04` | Design point: **1D3D ratios, `De/D` = 0.50, `vin` ≈ 12.5 m/s, Q = 350 CFM → `D` = 325 mm**, H = 1300 mm, Δp = 3.0" H₂O, `x50` ≈ 6.2 µm. `De/D` cannot go above 0.50 to buy more Δp relief: `G4` (`B > De/2`) caps it at the family `B/D` = 0.25. | E |
| `P12.05` | Robustness across the unknown flow band: at 300 CFM `vin` = 10.7 m/s (below `O1` floor — weak field, coarser cut, still drops chips); at 400 CFM `vin` = 14.3, Δp = 3.9". The geometry degrades gracefully in both directions; regenerate `D` after measurement if the miss is large. | E |
| `P12.06` | **Arc-split is now unavoidable, not deferred.** Flange OD at `D` = 325 is ~352 mm ≫ 248 mm bed. Barrel courses split into arc segments (axial seams in compression, `P8.100`); lower cone courses drop below bed size and stay monolithic. `P8.103` moves from "specified, not implemented" to **required implementation**. A monolithic bed-cap alternative is dead: `D` ≤ ~220 forces `vin` > 20 m/s at any useful HVLP flow. | E (verified against generator gate `S8`) |
| `P12.07` | Inlet is a **diffuser** again: 100 mm hose runs 21.0 m/s at 350 CFM; inlet area is 1.68× hose area. The `S4`/`S11` inversion pattern repeats — each source gets its own answer, computed not assumed (`O3`). | E |
| `P12.08` | 4" hose transport: 20.3 m/s needs ~340 CFM. At the expected duty point the hose rides at/just below transport — keep the CNC-to-cyclone run short and sloped/vertical (`S3` discipline). | E |
| `P12.09` | **Structural load collapses.** Blocked-hose worst case ≈ sealed static ≈ 2 kPa — under the drum lid's 3.5 kPa gasket-unseating dish (`Q5` data) with margin, and 10× under the phase-11 case. For this source the relief valve (`P11.36`) is moot and the lid stiffening requirement relaxes. The phase-11 numbers still govern the *vac-build* drum when that happens. | E |
| `P12.10` | Capture: ~300+ CFM meets or exceeds the 265 CFM boot ceiling (`P8.91`). The binding problem of the whole project (`P8.81`, capture not separation) is substantially resolved by this source. | E |

## 12.4 What this supersedes — and what it does not

| Item | Status |
|---|---|
| Phase-11 twin-900W build | **Kept, future** (`F1`/`F5`: the generator carries both duties as presets; nothing is discarded) |
| `S6` (`De/D` 0.45–0.50, CFM scarce) | Holds for shop-vac/LVHP presets; **direction inverts** for HVLP (`P12.01`) — 0.50 is now the Δp-relief end, pinned by `G4` |
| `S7` (De/D scale-invariant, don't re-decide) | Scoped to within-regime scaling only |
| `D9` build-2 target (240 mm / 265 CFM) | Still recorded for the vac path; SC0075 preset is a third, separate duty |
| Relief valve day-one mandate (`P11.17`) | Vac-build only (`P12.09`) |

## 12.5 Open questions

| ID | Question | Blocks |
|---|---|---|
| `Q-H1` | **Measured delivered flow** at the hose end, unit assembled, bag on (`V9.17` rig). Decides final `D`. | cutting geometry |
| `Q-H2` | SC0075 static curve — even two points (sealed lift, free flow) bounds the Δp trade far better than the nameplate. | `P12.05` refinement |
