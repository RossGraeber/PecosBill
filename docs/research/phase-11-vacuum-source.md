# Phase 11 — LVHP vacuum source (CamVac-class drum extractor)

Scope: motor selection, motor count/topology, and 120 VAC circuit allocation for the
drum-based vacuum device that feeds the cyclone (build 2 unblocks on this, `D9`).
Vessel: one of the four Greif 30-gal open-head steel drums. Branch context:
`P8.79`–`P8.97` (duty), `P8.67` (CamVac precedent), `P4.85`/`P4.99` (relief valve).

Notation per [00-notation.md](00-notation.md). New symbols: `WL` sealed water lift
("H₂O), `AW` air watts, `I` nameplate amps, `Q_o` open-flow CFM.

## 11.1 Sources

| Key | Source | Tier basis |
|---|---|---|
| `S-V1` | Record Power / Highland CamVac CGV386-6 listing (90 L, 3000 W, 230 V, 3 × 1000 W, max SP 81", 4" inlet) | C |
| `S-V2` | Stockroom Supply CamVac listings — 90 L 2-motor and 3-motor variants sold in North America on 110–120 V | C |
| `S-V3` | Ametek Lamb catalog data via distributors (Kleen-Rite, Vacuum Specialists, Imperial): 116765-xx (5.7", 3-stage, 120 V, 13.1 A, `WL` 136, `Q_o` 95–116, 465 AW); 117549-12 (7.2", 2-stage, 120 V, 14.8 A, 1675 W, `WL` 125.4, `Q_o` 114.8, 484 AW) | C |
| `S-V4` | Generic Amazon-class 5.7" 3-stage 120 V clones: ~1500 W, `Q_o` ~104, `WL` ~137, ~530 AW | C (weak) |
| `S-V5` | Carpet-extractor industry practice on series vs parallel motor stacking (Aramsco, Cleansmart, vacsuperstore) | C |
| `S-V6` | NEC: 15 A / 20 A branch circuits at 120 V; 80 % rule for continuous loads (≥3 h) | C |

The user's candidate motor link (`a.co/d/04oTWe5r`) did not resolve from this
environment; §11.1–§11.8 were first drafted assuming an `S-V4`-class ~1500 W unit.
**`Q-V1` is now resolved by product screenshot (2026-08-01): `S-V7`.** §11.9 records
the corrections; where §11.4–§11.5 conflict with §11.9, §11.9 governs.

| Key | Source | Tier basis |
|---|---|---|
| `S-V7` | User screenshot of the linked listing: 116392-00-pattern clone, 120 V 50/60 Hz, 5.7", 2-stage tangential bypass, **900 W (≈7.5 A)**, **97.0 CFM @ 2" orifice**, **81.8" H₂O sealed**, Class B, open enclosure | C (weak — clone marketing card, no curve) |
| `S-V8` | User screenshots (2026-08-01): 116765-13/00-pattern clone, 120 V, 5.7", 3-stage tangential bypass, **1400 W (≈11.7 A)**, **95.3 CFM @ 2" orifice**, **136" H₂O sealed**, 8" tall, Class B open | C (weak — same caveat) |
| `S-V9` | User screenshots (2026-08-01): another 116392-00-pattern clone card, **1100 W (≈9.2 A)**, otherwise identical air numbers to `S-V7`: 97.0 CFM @ 2", 81.8" sealed, 2-stage 5.7", 6.8" tall | C (weak — same caveat) |

## 11.2 Duty restated (from phase 8)

| Quantity | Value | Source |
|---|---|---|
| Flow target | **265 CFM** (boot-port ceiling) | `P8.91` |
| Static needed at source | **≥14" WC** duct/boot + ~4.3" cyclone (`vin` held) + 1–2" filter ≈ **~20" WC** | `P8.80`, build-1 report |
| Pressure available from any vac-motor source | 90–137" WC sealed | `S-V3` |

**Flow is the scarce axis; pressure is over-supplied 4–7×.** This is `P8.81`'s
mismatch, and it dictates every choice below.

## 11.3 Claims — motor class

| ID | Claim | Tier |
|---|---|---|
| `P11.01` | Tangential **bypass** motors are the correct class for continuous duty: cooling air is a separate circuit from working air, so a loaded (high-vacuum, low-flow) working stream does not starve motor cooling. Flow-through motors derate or die under exactly the blocked/filter-loaded conditions a dust extractor sees. Confirms the user's instinct. | C |
| `P11.02` | Tangential (vs peripheral) discharge gives a single exhaust port per motor — duct it to a common muffler/outside without sealing the whole motor compartment. Also wet-safe (debris never crosses windings). | C |
| `P11.03` | These are universal (brushed) motors: brush life ~600–800 h typical. Consumable; buy brush sets with the motors. Two smaller motors double brush maintenance vs one motor — accepted cost. | C/E |
| `P11.04` | 120 V caps a *single* vac motor near **1675 W / 14.8 A / ~115 CFM open** (`S-V3` 7.2" 2-stage is about the largest common unit). There is no single 120 V motor that reaches the CamVac's 3000 W — the CamVac itself only gets there by stacking 1000 W units. | C |

## 11.4 Claims — topology (the user's actual question)

| ID | Claim | Tier |
|---|---|---|
| `P11.05` | **Parallel** (motors side-by-side on the drum lid, shared plenum — the CamVac arrangement): flow ≈ sum of motors, sealed lift ≈ single motor. **Series** (one motor's exhaust into the next's intake): lift ×1.6–1.7, flow ≈ single motor, second motor eats hot air and dies young. | C (`S-V5`) |
| `P11.06` | **Parallel is unambiguously correct here.** The duty needs ~20" of a motor's 130"+ lift and every CFM it can get (`§11.2`). Series stacks the axis already over-supplied 6× and gains nothing on the scarce one. This is the same result as `P8.62` (parallel motors raise flow at ~constant Δp, `vin` and cyclone Δp unchanged). | E (verified against `S-V5`) |
| `P11.07` | The carpet-industry caveat that parallel gains are eaten by hose restriction (`S-V5`) does **not** apply: that failure mode is a 1.5" wand at 100+" WC. This system runs 3–4" smooth duct at ~20" WC — the parallel CFM is real. | E |
| `P11.08` | **Two lower-watt motors beat one high-watt motor**, and it is not close: 2 × 5.7" 3-stage ≈ 190–210 CFM at the ~20" working point vs ~105 for the biggest single motor. CFM-per-amp is flat across motor sizes (~8–9 CFM/A), so the only way to more flow on 120 V is more motors on more circuits. Single-motor option is strictly dominated. | E (verified) |
| `P11.09` | At the ~20" WC working point a bypass motor delivers ~85–90 % of `Q_o` (working point sits at ~15 % of sealed lift, high-flow end of the curve). Basis for all CFM-at-duty numbers here. | E |

## 11.5 Claims — circuits (NEC, 120 V only)

| ID | Claim | Tier |
|---|---|---|
| `P11.10` | Budget per circuit (continuous-load rule, `S-V6`): 15 A → 12 A / 1440 W; 20 A → 16 A / 1920 W. A ~12.5 A motor therefore **fills one circuit** — nameplate is at open flow, working draw runs ~90 % (~11 A), which fits a 15 A circuit but with no headroom for the shop lights. **One motor per circuit, nothing else on it.** | C/E |
| `P11.11` | Two ~12.5 A motors on one 20 A circuit (25 A nameplate, ~22 A working) trips. Two motors sharing a 20 A circuit requires ≤8 A units (~950 W), whose `Q_o` ~85 gives ~150 CFM total — legal but leaves 40+ CFM vs dedicated circuits. Only take this if a second circuit truly cannot be had. | E (verified) |
| `P11.12` | **Recommended configuration: 2 × 5.7" 3-stage ~1350–1500 W motors, parallel on the drum lid, one on the 15 A circuit, one on the 20 A circuit, independently switched.** ~2700–3000 W input, ~1000 AW, **~190–210 CFM at duty** — the electrical twin of the CamVac twin-motor 110 V unit `S-V2` already sold in North America. | E |
| `P11.13` | **Provision a third motor position** (blanked until used): a third motor on a second 20 A circuit reaches **~280–300 CFM ≥ the 265 CFM ceiling** and reproduces the `S-CD` triple-CamVac (`P8.67`). Drill the lid for 3, install 2. Lid holes are the cheap part; a second lid is the fallback if not. | E |
| `P11.14` | Independent switches are not a convenience: `P8.67` measured **6–17 % airflow lost through idle motors** — an unpowered motor is a leak path. Fit flap/blanking seals over idle motor intakes, and stagger switch-on so both inrushes don't share a breaker-cycle. | C/E |

## 11.6 Claims — consequences downstream

| ID | Claim | Tier |
|---|---|---|
| `P11.15` | At 2-motor flow (~200 CFM) the 3.5" boot port runs ~15 m/s — **below the 20.3 m/s branch transport minimum** (`P8.90`). Either run the branch at 3" (20.7 m/s at 200 CFM) until motor 3 exists, or accept settling in the 3.5" run. The 4"-everywhere plan is a 3-motor plan. | E (verified) |
| `P11.16` | Cyclone regeneration at measured flow, not nameplate: 200 CFM → `D` ≈ 224 mm, `x50` 4.71 µm; 265 CFM → 258 mm, 5.05 µm (`§8.8` table). Measure with the `V9.17` rig on the assembled vacuum **before** cutting build-2 geometry. | E |
| `P11.17` | Blocked-inlet sealed lift ~130" WC ≈ **32 kPa external on the drum** — and on the cyclone drum upstream, since a blockage at the boot puts full lift on everything. The CamVac runs a comparable drum at 81" (20 kPa) max (`S-V1`). Until the Greif drum's collapse pressure is established, the relief valve (`P4.85`, `P4.99`) is **mandatory on day one**, set ≤20 kPa (~80" WC). Test: crush margin is the cheapest thing to be wrong about. | E |
| `P11.18` | Motors exhaust ~2.7–3 kW of heat + carbon dust at the operator. Duct the tangential exhausts (`P11.02`) to a common outlet away from the work; this is also the noise fix (CamVac precedent: exhaust muffling dominates perceived loudness). | C/E |

## 11.7 Answer to the design question

**Two lower-wattage motors in parallel beat one higher-wattage motor** — pressure is
the axis already over-supplied; only motor count buys flow, and 120 V caps any single
motor at ~1675 W anyway (`P11.04`, `P11.06`, `P11.08`).

**Optimal mix given 15 A + 20 A outlets:** one ~1350–1500 W 5.7" 3-stage tangential
bypass motor per circuit, parallel plenum, independent switches, blanking seals, lid
drilled for a third motor on a future second 20 A circuit (`P11.12`–`P11.14`).
Expected duty point: **~200 CFM / ~20" WC now, ~280+ CFM with motor 3** vs the 265 CFM
system ceiling (`P8.91`).

## 11.8 Open questions

| ID | Question | Blocks |
|---|---|---|
| ~~`Q-V1`~~ | **RESOLVED** — see `S-V7` and §11.9. | — |
| `Q-V2` | Greif 30-gal drum collapse pressure (test to failure with the spare, or find rating). Sets the relief valve margin. Stakes lowered by `P11.21` (20.4 kPa max vs 32). | `P11.17` |
| ~~`Q-V3`~~ | **DISSOLVED by `P11.20`** — three motors now fit the two circuits already available; no second 20 A circuit needed. | — |
| `Q-V4` | Filter/separator order on the vacuum drum itself (CamVac-style internal cartridge vs bag) — separate phase; the cyclone upstream changes the loading assumptions vs a stock CamVac. | build 2 |
| `Q-V5` | Clone quality: `S-V7` card gives no duty rating, no brush spec, no curve. Buy one, run it hard for an hour, measure flow (`V9.17` rig) and temperature before ordering the fleet. | `P11.25` |

## 11.10 Constraint added: single plug, single circuit (user decision, 2026-08-01)

`C-V1`: **the device runs from one cord and one plug on one branch circuit.** No
multi-circuit wiring. This supersedes the circuit-allocation half of §11.9; the
topology findings (`P11.05`–`P11.08`) stand.

The whole trade now reduces to one number: **~1800 W nameplate is the most a single
120 V plug can carry** (20 A circuit, 16 A continuous budget). The only question is
how to spend it, and §11.2 already answered that: on flow, not lift.

| Config (one plug) | Nameplate | CFM @ ~20" duty | Verdict |
|---|---|---|---|
| **2 × `S-V7` 900 W parallel** | **15.0 A** | **~160–165** | **selected — most flow a plug can buy** |
| 1 × 8.4" 2-stage (~13 A, 142 CFM @ 2") | ~13 A | ~125–130 | fewer parts, 20 % less flow, no staged mode |
| 1 × `S-V8` 1400 W | 11.7 A | ~88 | half the flow; lift nobody needs |
| 1 × `S-V7` 900 W | 7.5 A | ~80 | runs on any outlet; underuses even a 15 A circuit |
| 2 × `S-V8` 1400 W | 23.3 A | — | violates `C-V1` on any single circuit |

| ID | Claim | Tier |
|---|---|---|
| `P11.24` | `S-V8` (1400 W / 136" / 95.3 CFM) buys **lift, not flow** — 95.3 CFM vs 97.0 for the 900 W unit, at 1.56× the amps. Under `C-V1` amps are the whole budget, so `S-V8` is the wrong motor for this duty in any count. Flow-per-amp: 12.9 (`S-V7`) vs 8.1 (`S-V8`). | E (verified) |
| `P11.25` | **Final configuration (supersedes `P11.20`, `P11.22`, `P11.23`): 2 × `S-V7` 900 W motors, parallel on the drum lid, one cord with a NEMA 5-20P plug into the 20 A outlet.** 15 A nameplate ≤ 16 A continuous budget; ~13.5 A working. Independent motor switches stay (`P11.14` — staged mode + staggered inrush), sealed lift stays 81.8" (20.4 kPa, `P11.21`). This is electrically the twin-motor 110 V CamVac (`S-V2`), one plug and all. | E (verified) |
| `P11.26` | The 5-20P plug is required, not optional: a 15 A nameplate cord-connected appliance does not belong on a 5-15P/15 A receptacle (12 A continuous ceiling). The 15 A outlet is not a fallback for the pair — fallback on a 15 A-only circuit is running **one** motor (7.5 A), which the independent switches give for free. | C/E |
| `P11.27` | Duty point becomes **~160 CFM plateau** (was ~235–255 under the 3-motor plan). Consequences: branch duct at **2.5"** holds transport (23.8 m/s); 3" is marginal (16.6 m/s < 20.3); the 3.5" boot port runs ~12 m/s — keep the boot run short and vertical-ish, expect some settling in it (`P8.94` discipline applies double). | E (verified) |
| `P11.28` | Cyclone regen target at the plateau: `D` ≈ **200 mm**, `x50` ≈ **4.45 µm**, printable whole on the P1S (`P8.69`) — build 2 gets *simpler* under `C-V1`: no segmented courses, no diffuser question at 1.0× area ratio (`P8.95` re-check at 160 CFM). Measure first (`V9.17`), then generate. | E |
| `P11.29` | Capture expectation, stated honestly: 160 CFM is ~60 % of the 265 CFM port ceiling — a large step up from 55, still short of full-boot capture on heavy sheet-goods cuts (`P8.82` softened, not erased). The upgrade path that respects `C-V1` is a second identical single-plug unit on the other circuit later (per-branch extraction), not more motors on this one. | E |
| `P11.30` | The `S-V9` "1100 W" card is **not a middle option**: air numbers are identical to `S-V7` (97.0 CFM / 81.8") — same 116392 fan pack, hotter nameplate. It adds amps (10.5 CFM/A vs 12.9) and zero air. A pair is 18.3 A nameplate > 16 A continuous budget — fails `C-V1` on a 20 A circuit. Reject. | E (verified) |
| `P11.31` | `S-V7` vs `S-V9` also demonstrates that **clone wattage labels are marketing, not measurements** — the same fan pack is sold as 900 W and 1100 W. Sharpens `Q-V5`: on the shakedown unit, *measure* amps with a meter at the real duty point; the pair-on-one-plug plan is contingent on measured draw ≈ 7.5 A, not on the card. If a "900 W" unit measures >8 A, the fleet plan needs re-checking against the 16 A budget. | E |

## 11.9 Q-V1 resolved — the 900 W motor changes the answer for the better

The linked motor (`S-V7`) is a **lower-lift, high-flow-per-amp** unit: 97 CFM at only
7.5 A, because it spends its wattage on flow, not on lift nobody needs (81.8" vs 137").
That is precisely the right shape for this duty (§11.2). Flow-per-amp ≈ **12.9 CFM/A**
vs ~8–9 for the `S-V3`/`S-V4` class — a ~50 % better use of scarce circuit amps.

| ID | Claim | Tier |
|---|---|---|
| `P11.19` | 2" orifice is near-free-air for a 5.7" motor: treat 97 CFM as ≈ `Q_o`. Working point ~20" WC is now 24 % of the (lower) sealed lift, so per-motor delivery at duty derates to ~80–85 % ≈ **78–82 CFM** (vs `P11.09`'s 85–90 % for high-lift motors). | E |
| `P11.20` | **Revised configuration (supersedes `P11.12`–`P11.13`): three `S-V7` motors, parallel, on the two existing circuits — two on the 20 A (15 A nameplate ≤ 16 A continuous budget, working ~13.5 A), one on the 15 A (7.5 A ≪ 12 A).** ~2700 W input, **~235–255 CFM at duty** — at or within reach of the 265 CFM ceiling with no new wiring. The 1500 W-class plan needed a third circuit for the same flow. Drill the lid for 4; install 3. | E (verified) |
| `P11.21` | Sealed lift 81.8" = **20.4 kPa** — essentially identical to the CamVac's 81" on the same style of drum (`S-V1`). Blocked-inlet drum load drops from 32 kPa (`P11.17`) to a figure with commercial precedent. Relief valve stays (protects printed parts and motors, `P4.85`/`P4.99`), but the drum-crush margin question is now bounded by a working commercial example. | C/E |
| `P11.22` | A fourth motor (second 20 A circuit, lid position 4) gives ~320+ CFM — above the 265 CFM port ceiling (`P8.90`), so it buys headroom against filter loading, not capture. Defer until measured flow says the plateau matters. | E |
| `P11.23` | Per-motor at duty is ~80 CFM not ~100: with only **two** motors running (~160 CFM), even a 3" branch is marginal (18.7 m/s < 20.3). The two-motor state is a cleanup/light-duty mode; **routing runs happen with all three on** (`P11.14` seals cover any idle position). | E (verified) |
