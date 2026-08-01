# Phase 8 — System integration: CNC-router dust as a duty specification

Branch chosen from `P1.19`, `P1.33`, `P2.14`, `P3.25`, `P5.28`, `P6.09`, `P7.06`.
Rationale: every performance number in phases 1–7 is conditional on an operating point. This phase
establishes what the operating point actually is for the stated application.

## 8.1 The material

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P8.01` | CNC routing produces a **bimodal** feed: coarse chips/curls from the cutter plus a fine fraction from the same cut. Both arrive simultaneously in the same duct. | E | derived; `W-WOODWEB` classes CNC with planers/jointers as high-chip-volume |
| `P8.02` | Particle density for wood-shop cyclone calculations: **730 kg/m³** (used as the worked value in teaching material for a wood-shop sanding cyclone). Softwood solid ≈ 400–550; MDF ≈ 700–800. Note this is far below the 2500 kg/m³ mineral dusts most cyclone data is taken with. | C | `W-PSU` example |
| `P8.03` | Low `ρp` directly worsens cut size: `x50 ∝ 1/√(ρp−ρ)`. Wood at 730 vs mineral at 2500 gives **`x50` 1.85× larger** for identical geometry and flow. **Published cyclone efficiencies on mineral dust do not transfer to wood.** | E | derived from `x50_lapple` |
| `P8.04` | MDF sanding dust: ~96 % below 100 µm; **79.6 % below 40 µm**. More than 95 % is inhalable (<100 µm). MDF produces more respirable dust than any other common woodworking operation. | A | `W-MDFDUST` |
| `P8.05` | Respirable (<10 µm) **mass** fraction for machining: MDF 0.01–18 % of total mass; particleboard 0.01–4.5 %. For sanding of dense hardwood: PM10 8.8 %, PM2.5 2.9 %, PM1 0.9 %. | A | `W-MDFDUST`, sanding studies |
| `P8.06` | Sieve analysis **underestimates** the fine fraction. Laser sizing of beech sanding dust found particles <10 µm in **every** sieve fraction including coarse ones; ultrafines down to ~0.7 µm detected. Sieve-based DIY PSD splits are therefore lower bounds on fines. | A | `W-MDFDUST` |
| `P8.07` | DIY sieve result consistent with `P8.06` being a floor: MDF sawdust was **entirely <1 mm, about half <0.5 mm**. Behaviour differs sharply by material — MDF dust *"acts more like sand"*, plywood/oak dust is *"very sticky"*. | D | `S-CD-tweaks` |
| `P8.08` | Measured DIY efficiency is strongly material-dependent on one fixed device: baking flour 64 %, sawdust 88–92 %, planer shavings 98–99 %, sugar 99.0 %. **Material is a bigger variable than any geometry change reported in that series.** | D | `S-CD-psd` |
| `P8.09` | Cross-checking `P8.08` against `P1.14`: a 30× spread in efficiency across materials is what a grade-efficiency curve *predicts* when feed MMD moves across `x50`. The DIY numbers are consistent with a single `x50`, not with the device behaving differently per material. | E | derived |
| `P8.10` | Coarse material present with fines **degrades fine capture** (`P1.45`) — trash >100 µm disrupts the wall strand pattern. This is exactly the CNC duty (`P8.01`), and it is the one loading effect that hurts rather than helps. | A | `L-WANG02 §Intro` |

## 8.2 Flow requirement

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P8.11` | Minimum transport (conveying) velocity for woodworking debris: **3500 fpm (17.8 m/s) in mains, 4000 fpm (20.3 m/s) in branches**; 4000–4500 fpm typical for heavier chip loads. Below this, chips drop out in the duct. | C | `W-WOODWEB` |
| `P8.12` | Resulting flow per branch: 4" = **350 CFM (0.165 m³/s)**; 5" = 545 CFM; 6" = **785 CFM (0.370 m³/s)** at 4000 fpm. | E (arithmetic, verified) | `W-WOODWEB` |
| `P8.13` | Oversizing duct is counterproductive: larger duct lowers velocity below transport and material settles. Size for **both** CFM and velocity. | C | `W-WOODWEB` |
| `P8.14` | Real capacity is "CFM **at** static pressure", not the manufacturer's free-air figure. Add 20–30 % margin. | C | `W-WOODWEB` |
| `P8.15` | **Direct collision with `P1.33`.** Duct transport velocity (17.8–20.3 m/s) is *above* every Texas A&M cyclone design velocity (12.2–16.3 m/s), and above the classical high-efficiency band. A cyclone fed straight from a transport-velocity branch runs **fast**, i.e. on the re-entrainment side of the efficiency peak (`P1.31`). | E | derived from `P8.11` + `P1.33` |
| `P8.16` | Resolution direction: the cyclone inlet area is a **free variable** — `vin = Q/(a·b)`, so `a·b` can be set to hit the family design velocity independently of the duct diameter. The inlet is a diffuser from the duct, not a continuation of it. This contradicts the DIY area-matching rule `P6.25`/`P6.26`. | E | derived; see `V9.10` |

## 8.3 The two incompatible source machines

| ID | | Shop vac / vacuum line | Dust collector / impeller blower |
|---|---|---|---|
| `P8.17` | Flow | < 250 CFM (< 0.12 m³/s) | > 350 CFM, typically 700–1200 |
| | Static pressure | > 60" WC (> 15 kPa) | < 10" WC (< 2.5 kPa) |
| | Suited cyclone | small-body, e.g. Dust Deputy class | large-body, e.g. Super Dust Deputy class |
| | Tier / Src | C / `W-ONEIDA` | C / `W-ONEIDA` |

| ID | Claim | Tier |
|---|---|---|
| `P8.18` | Vendor is explicit that these are **opposite** duty points and that using a high-flow cyclone on a shop vac (or vice versa) does not work. | C |
| `P8.19` | The project brief says *"vacuum air line from a CNC Router table"* — which of these two regimes applies is **undetermined and is the single highest-leverage open question** for Stage 2. It sets `D`, wall thickness (`P7.06`), and whether a multi-stage array is even feasible. | E |
| `P8.20` | Consequence of `P8.19` on `D`: at the Stairmand HE inlet (`a·b = 0.1·D²`) and `vin = 15 m/s`, `Q = 1.5·D²`. So `D = √(Q/1.5)`. For a shop-vac 0.10 m³/s ⇒ `D ≈ 258 mm`. For a 785-CFM branch, 0.37 m³/s ⇒ `D ≈ 497 mm`. Halving `vin` to a shop-vac-realistic value scales `D` up by √2 further. **A correctly-proportioned high-efficiency cyclone for either regime is large.** | E (derived) |
| `P8.21` | Cross-check on `P8.20` from published commercial specs. The 6" unit is rated **850–1200 CFM (0.40–0.57 m³/s)** through a **6" (152 mm) inlet port**, area 0.0182 m². That gives a port velocity of **22–31 m/s** — 1.4–2.0× the classical design band of `P1.33`. Overall envelope 37.5" tall × 18×19" footprint. Caveat: the port is round and feeds a neutral-vane/air-ramp inlet, so the *slot* velocity at the barrel differs from the port velocity; the calculation bounds the duct-side condition only. Directionally, commercial units are packaged small and run fast, trading cut size for envelope. | E (derived from `W-ONEIDA`) |
| `P8.22` | And the measured consequence of `P8.21`: that commercial cyclone class passed **9–15 g/kg** to the filters (`P6.07`) and its filters *"still get clogged quickly with very fine dust that could have been filtered out"*. Consistent with a device deliberately sized small and fast. | D + E |

## 8.4 Downstream: what happens to what escapes

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P8.23` | The purpose of the separator in this system is **filter protection and bin logistics**, not absolute air cleanliness — a filter follows it regardless. | D/E | `S-MTL`, `S-CD-*` |
| `P8.24` | Filters are worst at ~**0.3 µm** — an order of magnitude below any cyclone's cut size. Cyclones and filters are not substitutes. | D | `S-CD-air` |
| `P8.25` | Field observation contradicting the naive model: filter bags clog *"from the smallest particles over time and not just from the big ones."* Therefore a separator that removes only the coarse fraction extends filter life less than mass-percentage figures suggest. | D | `S-MTL §11:42` |
| `P8.26` | Long-run field result of an effective separator: 250 m of floorboards machined, six large bags collected, collector not emptied once; residual was fine dust adhering to the filter bag. | D | `S-CD-shop` |
| `P8.27` | Filter resistance is a large fraction of system loss and is directly measurable: paper towel media 12 cm H₂O on one motor (unusable); vacuum bag 28 cm; **cartridge filters 8–21 mm** H₂O for 2–3 stacked. Large-area pleated media is the correct choice. Air-speed penalty of good filters vs none: only ~5 %. | D | `S-CD-year` |
| `P8.28` | System losses outside the separator can exceed anything a geometry change buys: sealing an idle motor outlet gained **6–17 % airflow**. Fixed pipe instead of flex increased air speed measurably. | D | `S-CD-valve`, `S-CD-tweaks` |
| `P8.29` | Ranking implied by `P8.28`: leak sealing and duct smoothness are higher-yield than cyclone geometry refinement, at least until the obvious losses are gone. | E | derived |

## 8.5 The measurement chain at shop scale

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P8.30` | Feed-rate reference points: plunge saw in 18 mm MDF ≈ **10 kg/h**; thicknesser/planer at continuous feed ≈ **6–7 kg/h**; DIY test feed rates were pushed to 20–45 kg/h and beyond. A cabinet saw exceeds the plunge-saw figure. | D | `S-CD-cyclone1`, `S-CD-psd`, `S-CD-year` |
| `P8.31` | Very high feed rates occur in a shop only when vacuuming piles from the floor, not during machining. Optimise for the **low-to-normal** feed band. | D | `S-CD-cyclone1` |
| `P8.32` | Efficiency collapses fast outside that band: 7 tests at increasing feed rate ended at **92.8 %** for the fastest 8-second run; another series *"all five tests scored above 90 %"* at high rate vs near-99.99 % at normal rate. | D | `S-CD-inlets` |
| `P8.33` | U-tube water manometer across the device is the practical Δp instrument at this scale; measured third-stage penalty was **160 mm H₂O and −15 % air speed**, later reduced. | D | `S-CD-3rd` |
| `P8.34` | Weighing a removable downstream filter cartridge is the practical efficiency instrument — far better than opening the collector each time. | D | `S-CD-year` |
| `P8.35` | **Scale resolution is the binding measurement limit.** A scale displaying 0.1 g was accurate only to ~1 g; two scales gave different readouts on the same object; captured masses of 1.5 g were being reported to 0.1 g. Author's mitigation: five weighings averaged. This makes any claim above ~99.9 % on a 1.5 kg feed unsupportable — see `V9.11`. | D | `S-CD-3rd` |

## 8.6 Resolved duty: **shop vac** (answers `Q1`, 2026-07-29)

Source machine is a shop vacuum, not a dust collector. `P8.17` right-hand column is void.
Everything below is derived from that decision and verified arithmetically.

### 8.6.1 The operating envelope

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P8.36` | Shop-vac sealed (static) pressure: **53–90" H₂O = 13–22 kPa**. Roughly 6–9× a dust collector's ~10" H₂O. | C | vendor spec sheets, vacuum-testing literature |
| `P8.37` | Published CFM and water-lift are the two **endpoints** of the fan curve and never occur together. Rated CFM is usually free-air or at a stated orifice (one spec sheet: 60 CFM max airflow, 53" sealed pressure, ASTM-tested on a 1.25" hose). Neither endpoint describes the operating point. | C | ASTM F558-19 practice, vendor notes |
| `P8.38` | Working flow band adopted for this project: **50–150 CFM (0.024–0.071 m³/s)**. Lower bound is the vendor-stated minimum for cyclone separation to work at all (50 CFM); upper bound is a generous large-vac figure. | C/E | `W-ONEIDA` Dust Deputy guidance |
| `P8.39` | A shop vac loses only **~10 %** flow to a 2.5" hose, where a 1 HP dust collector loses ~60 % (233 → 91 CFM). The pressure headroom is real and is the defining property of this regime. A two-bucket cyclone's resistance measured ≈ **10 ft of 2.5" hose**. | C | Wandel hose measurements |
| `P8.40` | Commercial precedent is the **Dust Deputy** class, not Super Dust Deputy: tapered **2" ports**, fits vac inlets 1.5–2.5", minimum 50 CFM recommended. Oneida's stated sizing rule for this class is **match port sizes**, not CFM. | C | `W-ONEIDA` |

### 8.6.2 Body diameter falls out immediately

`D = √( Q / (vin · (a/D)(b/D)) )` at `vin = 15 m/s`:

| Flow | `D`, Lapple inlet (`ab=0.125D²`) | `D`, Stairmand HE inlet (`ab=0.10D²`) |
|---|---|---|
| 50 CFM | 112 mm | 125 mm |
| 100 CFM | 159 mm | 177 mm |
| 150 CFM | 194 mm | 217 mm |

| ID | Claim | Tier |
|---|---|---|
| `P8.41` | **A correctly-proportioned high-efficiency cyclone for a shop vac is 110–220 mm in body diameter.** This is comfortably inside FDM print envelopes (`P7.23` records 300 mm achieved). The `P8.20` concern about size applied to the dust-collector regime and is now void. | E (verified) |
| `P8.42` | Total height at `H/D = 4` (`G8`) is therefore **450–870 mm** — 3–5 bed-heights, so length-module splitting (`P7.25`, `A2`) is mandatory rather than optional. | E |

### 8.6.3 Pressure drop is close to free — this re-weights the Pareto front

Δp for a Lapple-inlet cyclone at `D = 150 mm`, `Eu` from `Eu_SL = 16ab/De²`:

| `De/D` | `Eu` | Δp @ 100 CFM | as % of 53" sealed |
|---|---|---|---|
| 0.60 | 5.6 | 3.8" H₂O | 7 % |
| 0.50 | 8.0 | 5.4" H₂O | 10 % |
| 0.45 | 9.9 | 6.7" H₂O | 13 % |
| 0.40 | 12.5 | 8.5" H₂O | 16 % |
| 0.35 | 16.3 | 11.1" H₂O | 21 % |
| 0.30 | 22.2 | 15.1" H₂O | 28 % |

| ID | Claim | Tier |
|---|---|---|
| `P8.43` | **Narrowing the vortex finder from `De/D = 0.5` to 0.35 costs ~6" H₂O out of 53–90" available.** In the dust-collector regime (<10" total) that move is unaffordable; here it is not. The shop vac makes the *efficiency* end of the `De/D` Pareto front (`P3.05`) reachable. | E (verified) |
| `P8.44` | Caveat: pressure headroom is not free flow. Every inch of Δp moves the vac up its curve and costs CFM, which costs transport velocity in the hose (`P8.45`). The correct framing is that Δp is cheap **relative to the alternative regime**, not costless. The fan curve, not the sealed-pressure number, is the real budget — and it is not published (`P8.37`). | E |

### 8.6.4 Hose diameter is now the binding coupled constraint

Hose velocity (m/s), and the CFM each size needs to reach the 20.3 m/s branch transport spec (`P8.11`):

| Hose | 50 CFM | 75 | 100 | 125 | 150 | CFM for 20.3 m/s |
|---|---|---|---|---|---|---|
| 1.25" | 29.8 | 44.7 | 59.6 | 74.5 | 89.4 | 34 |
| 1.5" | 20.7 | 31.0 | 41.4 | 51.7 | 62.1 | 49 |
| 2.0" | 11.6 | 17.5 | 23.3 | 29.1 | 34.9 | 87 |
| 2.5" | 7.5 | 11.2 | 14.9 | 18.6 | 22.4 | 136 |

| ID | Claim | Tier |
|---|---|---|
| `P8.45` | Shop-vac systems hold transport velocity by using **small hose**, not high flow. A 2.5" hose needs 136 CFM to meet the branch spec — above most shop vacs' working flow. **A 2.5" hose on a 100 CFM vac is below woodworking transport velocity (14.9 vs 20.3 m/s)** and will drop chips in horizontal runs. | E (verified) |
| `P8.46` | **`V9.10` partially reverses in this regime.** At 2.5"/100 CFM the hose runs at 14.9 m/s — already inside the cyclone design band — so inlet-area ≈ hose-area (the DIY rule `P6.25`) is approximately correct and no diffuser is needed. At 2.0"/100 CFM the hose runs 23.3 m/s and the inlet **must** diffuse to reach 15 m/s. The rule that survives is `O3` (choose `a·b` from `vin`), and it happens to coincide with area-matching only for the larger hose. | E (verified) |
| `P8.47` | The design tension is therefore: **small hose = good transport, bad cyclone inlet; large hose = good cyclone inlet, bad transport.** With a CNC dust shoe the hose is short and largely vertical, which weakens the transport argument — but the shoe port size is usually fixed by the machine. | E |
| `P8.48` | The commercial 2" Dust Deputy port spans **11.6 m/s @ 50 CFM to 34.9 m/s @ 150 CFM** — i.e. it is only inside the design band at the bottom of its own rated range and is 2.3× over it at the top. Same finding as `P8.21`: this product class is packaged for fit, not for cut size. | E (verified) |

### 8.6.5 Cut-size scale check

Lapple closed form (`P1.27`), `D = 150 mm`, wood at `ρp = 730`:

| Flow | `vin` | `x50` |
|---|---|---|
| 50 CFM | 8.4 m/s | 5.2 µm |
| 75 CFM | 12.6 m/s | 4.2 µm |
| 100 CFM | 16.8 m/s | 3.6 µm |
| 125 CFM | 21.0 m/s | 3.3 µm |
| 150 CFM | 25.2 m/s | 3.0 µm |

| ID | Claim | Tier |
|---|---|---|
| `P8.49` | Order-of-magnitude cut size for this class of machine is **3–5 µm**. This is a *scale check*, not a prediction — but note `P1.16`: Lapple's error is concentrated in the grade-curve **slope**, while its `x50` agreed with measurement within ~20 %. Using Lapple for `x50` alone is the defensible part of it. This relaxes `V9.25` to: cut size may be estimated to ±~50 %; grade curves may not. | E (verified) |
| `P8.50` | Reading `P8.49` against the material (`P8.04`: ~80 % of MDF sanding dust below 40 µm): at `x50 ≈ 4 µm` and Lapple reference points (`P1.14`), particles ≥12 µm are ~90 % collected and ≥20 µm ~96 %. The escaping fraction is the sub-10 µm tail — which is exactly the respirable fraction (`P8.05`) and exactly what clogs filters (`P8.25`). **A shop-vac cyclone is a chip-and-coarse-dust separator; it does not solve the health-relevant fraction.** Consistent with `P8.23`. | E |
| `P8.51` | The `x50` column above **improves with flow** while `P1.31` says efficiency turns over above the design velocity. The two meet around 100–125 CFM at `D = 150 mm` (`vin` 17–21 m/s, already at/above the 12–17 m/s band of `O1`). Above that, the model says better and the physics says worse. **Trust the physics; the model has no re-entrainment term.** | E |

### 8.6.6 Structural consequence

| ID | Claim | Tier |
|---|---|---|
| `P8.52` | `M5` hardens. Full blockage puts **13–22 kPa** on the shell and bin, not 2.5 kPa. `P7.07` records a bin collapsing under the dust-collector regime; this regime is 6–9× worse. Buckling design (`M1`, `M2`) moves from prudent to load-bearing, and the collection vessel is the governing part. | E |
| `P8.53` | Mitigation available for free: a shop vac cannot reach sealed pressure while flow exists. The worst case is a **blocked hose with the motor running** — a routine event with a CNC dust shoe cutting into a pocket. This is a design load case, not an edge case. | E |

## 8.7 Hardware fixed: RIDGID WD06701 + Bambu Lab P1S (narrows `Q2`, answers `Q4`)

Stated future intent: build a multi-motor **LVHP** unit later. "Start small, plan flexibly."

### 8.7.1 The vacuum

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P8.54` | `WD06701` is a variant SKU in RIDGID's WD0670/WD0671 6-gallon family (discontinued; HD0600 NXT is the stated replacement). Same-platform `WD0671EX` spec: **120 V, 5.8 A, 3.5 peak HP, 6 gal, 44 CFM, 1-7/8" × 7 ft hose**. | C | `W-RIDGID` |
| `P8.55` | The 44 CFM figure's measurement basis is not disclosed beyond RIDGID's blanket note that *"CFM specifications are based on average motor performance."* Treat as indicative, not a design input (`P8.37`). | C | `W-RIDGID` |
| `P8.56` | Independent anemometer data on the same brand's larger vacs, for bounding: a 14-gal RIDGID measured **140 CFM** (true 2.5" smooth-bore), **138** (stock 2.5"), **113** (RIDGID "Pro" hose, which is actually 1-7/8" mid-hose), **92** (Festool 36/32 mm). A separate test found a stock shop-vac hose delivering 52 CFM and a larger pool hose 69 CFM on the same machine. | D | `W-HOSETEST` |
| `P8.57` | **Working flow band adopted for the WD06701: 40–70 CFM (0.019–0.033 m³/s).** Rationale: 44 CFM nominal on a 6-gal/3.5 pHP machine, and the 1-7/8" hose measured as the restricting element on a much larger vac (`P8.56`). Supersedes the generic 50–150 CFM of `P8.38` for the *first build*. | E | derived |
| `P8.58` | Going to a true 2.5" smooth-bore hose recovers ~15–20 % CFM on this class of machine — **not** the 30–50 % often claimed. Mid-hose ID, not cuff size, is what matters; ribbing costs as much as diameter. | D | `W-HOSETEST` |

### 8.7.2 Body diameter for this vacuum

`vin = 15 m/s`, Lapple inlet (`a·b = 0.125·D²`), wood `ρp = 730`:

| Flow | Hose velocity (1-7/8") | `D` @ `vin`=15 | `D` @ `vin`=13 | `x50` | `H = 4D` |
|---|---|---|---|---|---|
| 40 CFM | 10.6 m/s | 100 mm | 108 mm | 3.15 µm | 401 mm |
| 44 CFM | 11.7 m/s | 105 mm | 113 mm | 3.22 µm | 421 mm |
| 50 CFM | 13.2 m/s | 112 mm | 121 mm | 3.33 µm | 449 mm |
| 60 CFM | 15.9 m/s | 123 mm | 132 mm | 3.48 µm | 492 mm |
| 70 CFM | 18.5 m/s | 133 mm | 143 mm | 3.62 µm | 531 mm |

| ID | Claim | Tier |
|---|---|---|
| `P8.59` | **Design point: `D ≈ 120 mm`, `H ≈ 480 mm`.** Across the whole 40–70 CFM uncertainty band `D` moves only 100→133 mm and `x50` only 3.15→3.62 µm (**±7 %**). The flow uncertainty in `P8.55` is therefore *not* design-blocking — a 120 mm body is defensible without measuring the vac first. | E (verified) |
| `P8.60` | **The 1-7/8" hose runs below woodworking branch transport velocity across the entire band.** 20.3 m/s needs 76.6 CFM through that hose; the vac delivers ~40–70. Chips will settle in horizontal runs, and the cyclone's Δp will push flow lower still. Mitigation is short, sloped or vertical hose — which a CNC dust shoe naturally provides. Do not add long horizontal hose. | E (verified) |

### 8.7.3 `De/D` on a small vac — `P8.43` is weaker here

At `D = 120 mm`, 60 CFM (`vin` = 15.7 m/s):

| `De/D` | `Eu` | Δp |
|---|---|---|
| 0.55 | 6.6 | 3.9" H₂O |
| 0.50 | 8.0 | 4.8" H₂O |
| 0.45 | 9.9 | 5.9" H₂O |
| 0.40 | 12.5 | 7.5" H₂O |
| 0.35 | 16.3 | 9.7" H₂O |
| 0.30 | 22.2 | 13.2" H₂O |

| ID | Claim | Tier |
|---|---|---|
| `P8.61` | `P8.43` holds in kind but is weaker in degree for a 6-gal vac. The pressure is available, but every inch of Δp costs CFM, and CFM is what is already short (`P8.60`). **Recommend `De/D` = ~~0.45~~ 0.466–0.50 for the first build** (lower bound corrected by `P2.33` — 0.45 violates `C3`), not the 0.35 the Pareto front would favour. | E |
| `P8.62` | `De/D` affordability is roughly **scale-invariant** across the planned upgrade: adding motors in parallel raises flow at approximately constant pressure, and `vin` is held constant by design, so Δp (∝ `vin²`) does not change. The `De/D` decision does not need to be re-made at the LVHP stage. | E |

### 8.7.4 Scaling to the multi-motor LVHP — the important result

Holding `vin` = 15 m/s and growing a **single** cyclone with flow:

| Total flow | `D` | `H = 4D` | `x50` | 250 mm modules |
|---|---|---|---|---|
| 60 CFM | 123 mm | 492 mm | 3.48 µm | 2 |
| 120 CFM | 174 mm | 695 mm | 4.14 µm | 3 |
| 180 CFM | 213 mm | 851 mm | 4.59 µm | 4 |
| 240 CFM | 246 mm | 983 mm | 4.93 µm | 4 |

| ID | Claim | Tier |
|---|---|---|
| `P8.63` | **Scaling up flow with a single cyclone makes the cut size worse** — 3.48 → 4.93 µm from 60 to 240 CFM. This is `P1.26` (`x50 ∝ √D`) doing exactly what it says. The small vac is the *better* separator; the LVHP upgrade buys capture-at-source and duct capacity, not finer separation. | E (verified) |
| `P8.64` | **Therefore: scale by replicating the unit, not by growing it.** 4 × 123 mm cyclones at 240 CFM hold `x50` at 3.48 µm where 1 × 246 mm gives 4.93 µm. Each unit sees `Q_total/n` at the same `D`, so `vin`, `Eu` and `x50` are all preserved; parallel paths keep Δp unchanged. This is `P1.28` used correctly. | E (verified) |
| `P8.65` | `P8.64` also resolves the flexibility problem: **the same ~120 mm module is the right unit at both scales.** No re-sizing, no re-design, no compromise geometry. It converts an uncertain future flow from a design risk into a unit count. | E |
| `P8.66` | `P8.64` reinstates the array architecture (`A5`, rejected under `P8.38` assumptions) **for the LVHP phase only** — subject to `P6.20`: the underflows must be isolated (one bin per cell, or a properly baffled plenum), and `P6.17` (axial-symmetric arrangement). A shared open hopper is the configuration the literature says fails. | E |
| `P8.67` | Precedent alignment: the entire `S-CD` dataset was developed on a **triple-motor CamVac** — i.e. exactly the multi-motor LVHP being planned. Its system-level findings (idle-motor sealing worth 6–17 % airflow, filter-tube instrumentation, motor-count vs efficiency behaviour, `P1.34` over-flow re-entrainment) transfer to the LVHP phase far more directly than to the single-vac phase. `V9.20`'s device-class caveat still applies to its *cyclone geometry* conclusions. | E |

### 8.7.5 Printer envelope (answers `Q4`)

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P8.68` | P1S build volume **256 × 256 × 256 mm**. Bambu Studio caps Z at **250 mm** by default to avoid bed collisions, and the filament-cutter stopper removes **18 × 28 mm at the front-left corner**. Full 256³ requires deviating from stock configuration and is not recommended. | C | `W-BAMBU` |
| `P8.69` | A circle's bounding box is `D × D`; rotating it on the bed gains nothing. **Max printable body diameter ≈ 240–250 mm.** The 120 mm design point (`P8.59`) uses half the bed, and even the 246 mm single-cyclone LVHP case (`P8.63`) would just fit — but `P8.64` makes that case unnecessary. | E | derived |
| `P8.70` | `H ≈ 480 mm` at `D = 120 mm` ⇒ **2 length modules** at 250 mm. `S2` (splitting mandatory) is satisfied cheaply, and `P7.25`/`A2` length tuning comes free. | E | derived |
| `P8.71` | The P1S is **enclosed with a carbon filter**, so ASA/ABS are available in addition to PETG. ASA offers higher stiffness and temperature margin — relevant to the buckling load case `S5` (`P8.52`). PETG remains the lower-risk default for sealing (`P7.09`). Material choice is a live `S5` trade, not settled. | C/E | `W-BAMBU`, `P7.09` |
| `P8.72` | Nozzle choice is a genuine three-way trade on this project: a **0.6 mm** nozzle cuts print time on ~500 mm of body, gives thicker perimeters (helping both sealing `P7.11` and buckling `M1`), but raises layer height and therefore internal roughness (`P7.19`, and the disputed `V9.09`). Not resolvable from the literature; a candidate for the first empirical test. | E | derived |

## 8.8 The machine: Signstech N1313, 4×4 ft, 3 HP spindle (answers `Q6`)

Hobbyist operating a machinist-renewed **commercial** router. 1300 × 1300 mm work area, 3 HP spindle.

### 8.8.1 `Q6` — regulatory

| ID | Claim | Tier |
|---|---|---|
| `P8.73` | NFPA 664 / 660 are **facility**-scoped (workplaces, wood processing and woodworking facilities). A hobbyist in a private shop is outside their enforcement scope: no DHA obligation, no mandated bonding programme. **The machine being commercial does not make the use commercial.** If the shop ever takes paid work or employs anyone, this flips. | C/E |
| `P8.74` | The *quantity* argument that made hobby-scale dust safe (`P7.33`) thins here but does not break. At 17–37 kg/h of chips and 10–15 % fines, airborne fines are **0.06–0.20 lb/min** against the ~1 lb/min-in-4"-duct figure cited for a sustainable explosive mixture — a **5–16× margin**, down from the comfortable order-of-magnitude a hand-fed hobby tool enjoys. | E (computed) |
| `P8.75` | The more realistic exposure is not deflagration but **accumulated fire load and housekeeping**: 20–28 kg of wood dust sitting in a steel drum, plus surface accumulation, plus a spark source. Steel vessels (`P4.90`) and bonding are cheap insurance and are already the chosen path. | E |

### 8.8.2 Chip production — the machine is an industrial-rate dust source

MDF at 750 kg/m³; `MRR = RDOC × ADOC × feed`; chips bulk 3–5× solid volume.

| Cut | MRR | Mass rate | 30-gal drum fills in |
|---|---|---|---|
| ¼" bit, 0.25 × 0.125, 120 ipm | 3.8 in³/min | 2.8 kg/h | 6–10 h |
| ½" bit, 0.5 × 0.25, 180 ipm | 22.5 in³/min | **16.6 kg/h** | **1–1.7 h** |
| ½" bit, 0.5 × 0.5, 200 ipm (hogging) | 50 in³/min | **36.9 kg/h** | **28–46 min** |

| ID | Claim | Tier |
|---|---|---|
| `P8.76` | **A 3 HP router at moderate feed produces 17 kg/h — 2.5× the planer that motivated the entire `S-CD` research programme (`P8.30`), and above the 10 kg/h plunge saw.** At hogging rates 37 kg/h sits at the very top of the feed band where `S-CD` measured efficiency collapsing (`P8.32`, `P1.39`). | E (computed) |
| `P8.77` | Those fill times are **continuous cutting**. Real hobby duty is perhaps 20–40 % cutting time, so a 30-gal drum is realistically hours to a day of work. The two-drum swap (`P4.86`) is well matched to that. | E |
| `P8.78` | 3 HP is not the limiting factor: wood and MDF unit power is ~0.05–0.10 HP per in³/min, so a 3 HP spindle is rarely power-limited in sheet goods. **Rigidity, feed limits and chip evacuation bind first** — chip evacuation being the one this project owns. | C |

### 8.8.3 The capture problem — this is the finding that matters

| Boot port | flow at 4000 fpm |
|---|---|
| 1-7/8" (the vac's hose) | 77 CFM |
| 2.5" | 136 CFM |
| 3" | 196 CFM |
| **4" (typical for this machine class)** | **349 CFM** |
| 5" | 545 CFM |
| 6" | 785 CFM |

| ID | Claim | Tier |
|---|---|---|
| `P8.79` | Practitioner consensus for CNC routers: **≥600 CFM at the tool** with the boot in contact with the work; commonly 800–1000 CFM; manufacturer recommendations run 1000–5000 CFM with ≥7" duct. A 4" boot caps near 350–400 CFM and is itself considered the bottleneck. | C |
| `P8.80` | CNC also demands **static pressure ≥14" WC** because reaching a moving gantry requires long small-bore flex, which is friction-dominated. | C |
| `P8.81` | **The WD06701 delivers 40–70 CFM. That is ~6× short of what a 4" boot passes and ~11× short of the 600 CFM practitioner floor.** On static pressure it is *over*-supplied (53–90" vs 14" needed). **This is an HVLP application being fed by an LVHP source** — the mismatch is in the one axis that cannot be traded. | E (verified) |
| `P8.82` | Consequence to state plainly: at 40–70 CFM the boot will not capture chips from a 3 HP cut in sheet goods. Chips will scatter. The shop vac is adequate for **small bits, light passes, engraving, and vacuuming the table** — not for production routing on a 4×4 machine. | E |
| `P8.83` | **This does not invalidate build 1.** Cyclone sizing is `D = √(Q/(vin·(a/D)(b/D)))` — it follows whatever flow it is given. A 118 mm unit on the shop vac is a correct, well-proportioned cyclone at 55 CFM, and it validates the generator, the drum lid (`P4.82`), the sealing scheme, and the measurement rig (`V9.17`) — all of which carry forward unchanged. Build it; just size expectations to `P8.82`. | E |

### 8.8.4 The LVHP target, and where the printer becomes binding

`vin` = 15 m/s, Lapple inlet:

| System flow | single-cyclone `D` | `x50` | `H` | printable on P1S? |
|---|---|---|---|---|
| 55 CFM (now) | 118 mm | 3.41 µm | 471 mm | yes |
| 120 CFM | 174 mm | 4.14 µm | 695 mm | yes |
| 230 CFM | 241 mm | 4.88 µm | 962 mm | **at the limit** |
| 350 CFM (4" boot) | 297 mm | 5.4 µm | 1188 mm | **no** |
| 600 CFM (floor) | 389 mm | 6.20 µm | 1554 mm | **no** |

| ID | Claim | Tier |
|---|---|---|
| ~~`P8.84`~~ | ~~Max printable single unit on a P1S is `D` ≈ 240 mm.~~ **WITHDRAWN — see `P8.84a`.** | — |
| ~~`P8.85`~~ | ~~Unit replication is therefore the only available path.~~ **WITHDRAWN — see `P8.85a`.** | — |
| `P8.84a` | **Correction (user, 2026-08-01): bed size does not cap `D`.** A body larger than the bed is printed as circumferential courses split into arc segments and assembled. `D` is limited only by the seam count and assembly effort one is willing to accept. | E |
| `P8.85a` | Unit replication is therefore **an option, not a necessity**, at any flow. It is chosen for cut-size reasons (`x50 ∝ √D`) or underflow-isolation reasons, not because the printer forces it. | E |
| `P8.86` | **Correction to `P8.65`/`U3`.** The claim that "the same ~120 mm module is correct at both scales" held for a 60 → 240 CFM step. Against a 350–600 CFM target it does not: holding `D` = 118 mm would need 6–11 units. **What carries across scales is the *generator*, not the unit** — which is exactly what `F1`–`F6` bought. Build 1 at `D` ≈ 118 mm; regenerate at 174–240 mm when the LVHP lands. Two prints, one model, no redesign. | E |
| `P8.87` | Unit-size trade at the LVHP stage: smaller units cut finer but multiply parts and underflows (`P4.88`, `P6.20`). 5 × 174 mm gives `x50` 4.14 µm; 3 × 240 mm gives 4.88 µm with fewer bins to isolate. **Two isolated drums are already owned, which favours `n` = 2–3.** | E |
| ~~`P8.88`~~ | ~~Establish the boot port size.~~ **ANSWERED — see §8.9.** | — |

## 8.9 Boot spec measured: 3.5" ID / 3.75" OD port, 5" square shroud

| ID | Claim | Tier |
|---|---|---|
| `P8.89` | Boot port **3.5" ID** (88.9 mm), area **62.1 cm²**. This is the system ceiling — everything downstream can only pass what the port passes. | E (verified) |
| `P8.90` | Flow the port supports, by velocity: 197 CFM @ 15 m/s · **267 CFM @ 20.3 m/s (minimum branch transport)** · 329 @ 25 · 395 @ 30. Above ~25 m/s the friction penalty rises steeply and the port becomes a loss source rather than a duct. | E (verified) |
| `P8.91` | **Practical LVHP target is therefore ~265 CFM, not the 600 CFM of `P8.79`.** The port physically cannot deliver 600 CFM at a sane velocity. This is *good* news — it halves the target and makes the whole system smaller. | E |
| `P8.92` | It also revises `P8.81`: the WD06701's 40–70 CFM is **~4–7× short of the port's own capability**, not 11× short of an unreachable figure. Same conclusion (`P8.82`), less dramatic gap. | E |
| `P8.93` | The **5" square shroud** is a tight boot for a 4×4 machine, and that is favourable: the literature's own emphasis is that boot-to-work contact and containment beat raw CFM (`P8.79`). A small well-sealed shroud at 265 CFM will out-capture a large loose one at 600. | C/E |
| `P8.94` | At 265 CFM the duct from boot to cyclone runs at 20.3 m/s — exactly minimum transport, no margin. **Keep the run short, smooth-bore, and avoid horizontal sections**; any diameter increase downstream drops below transport velocity. | E |

### Cyclone sizing against the real ceiling

`vin` = 15 m/s, Lapple inlet:

| Flow | `D` | `x50` | `H` | inlet `a × b` | inlet area ÷ boot area |
|---|---|---|---|---|---|
| 55 CFM (shop vac now) | 118 mm | 3.41 µm | 471 mm | 59 × 29 mm | 0.28× |
| 200 CFM | 224 mm | 4.71 µm | 897 mm | 112 × 56 mm | 1.01× |
| **265 CFM (boot ceiling)** | **258 mm** | **5.05 µm** | **1033 mm** | **129 × 65 mm** | **1.34×** |
| 330 CFM | 288 mm | 5.34 µm | 1153 mm | 144 × 72 mm | 1.67× |

| ID | Claim | Tier |
|---|---|---|
| `P8.95` | **`S4` flips back at LVHP scale.** At 55 CFM the hose runs slower than the cyclone design band, so no diffuser is needed. At 265 CFM the cyclone inlet is **1.34× the boot area**, so the inlet *must* expand — `O3` governs again and the transition is a real diffuser. The two build stages need opposite inlet treatments; the generator must compute this rather than assume either. | E (verified) |
| `P8.96` | Two ways to reach 265 CFM, both viable: **(a) one 258 mm cyclone**, printed as segmented courses, feeding one drum, `x50` = 5.05 µm; **(b) two 183 mm cyclones**, each printable whole, one per drum, `x50` = 4.25 µm (**16 % finer**). | E (verified) |
| `P8.97` | Recommendation leans **(a)**. A two-way split reintroduces exactly the maldistribution the evidence warns about — `P6.23` measured one branch taking almost all the dust behind a Y-piece, and `P6.24` found consolidating two units into one gave that project's best result. The 16 % cut-size gain is smaller than the risk. It also leaves the second drum free for its best use: the **swap spare** (`P4.86`). | E |

## 8.10 Printing a body larger than the bed

Structural check of the printed shell itself as a vacuum vessel, Windenburg-Trilling, need > 22 kPa:

| Material | `D` | `t` | rib spacing | `p_cr` |
|---|---|---|---|---|
| PETG | 120 | 2.5 | 250 mm | 161 kPa (×7) |
| PETG | 240 | 3.0 | 250 mm | 92 kPa (×4) |
| PETG | 240 | 4.0 | 80 mm | 678 kPa (×31) |
| PETG | 390 | 4.0 | 250 mm | 93 kPa (×4) |
| PETG | 390 | 4.0 | 80 mm | 347 kPa (×16) |
| ASA | 390 | 6.0 | 80 mm | 1125 kPa (×51) |

| ID | Claim | Tier |
|---|---|---|
| `P8.98` | **The printed shell is not the structural problem at any plausible size.** Even 390 mm at 4 mm wall with no ribs clears 22 kPa by ×4. The drum lid (`P4.81`) remains the weak part of the whole assembly by a wide margin. | E (verified) |
| `P8.99` | **A flanged circumferential joint is a free stiffening ring.** Dropping the unsupported bay from 250 → 80 mm is worth ×3.6–7. Segmenting a tall body into courses therefore *improves* its buckling margin rather than degrading it — the opposite of the intuition. | E (verified) |
| `P8.100` | **Axial (vertical) seams are favourable under external pressure.** The load path is hoop *compression*, which presses arc segments together rather than pulling them apart. Strength is not the concern for axial seams — **leakage and roundness are.** | E |
| `P8.101` | Out-of-roundness is the genuine risk of segmenting (`P7.02`): buckling is acutely sensitive to ovality, and a multi-segment course is harder to hold round than a printed-in-one shell. Mitigation is the same ring that solves everything else — a stiff flange at every course boundary, sized to hold circularity during assembly. | E |
| `P8.102` | Remaining real costs of segmenting: internal seam **steps in the swirl path** (roughness discontinuity, `P7.19`/`V9.09` — disputed direction, so minimise rather than exploit); more gasket length; more fasteners; alignment features on every joint. None are structural. | E |
| `P8.103` | Generator requirement: support **both** split axes — circumferential courses for `H` > bed Z, and arc segments for `D` > bed X/Y — with flange, gasket groove, and alignment features generated automatically at each seam. `D` and `H` then become free parameters rather than bed-limited ones (`F1`, `F2`). | E |

## Branch decisions taken from Phase 8

| Branch | Trigger | Goes to |
|---|---|---|
| Duct velocity vs cyclone design velocity conflict | `P8.15`, `P8.16` | Phase 9 (`V9.10`), Phase 10 |
| Source-machine regime is undetermined | `P8.19` | Phase 10 (blocking open question) |
| Scale resolution invalidates the top of the DIY dataset | `P8.35` | Phase 9 |
| Wood `ρp` invalidates transfer of mineral-dust efficiency data | `P8.03` | Phase 9, Phase 10 |
