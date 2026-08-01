# Phase 7 — Manufacturing constraints for an FDM-printed separator

Branch chosen from `P2.18`, `P3.24`, `P4.25`, `P5.13`.
Rationale: the optimisation literature treats geometry as free and surfaces as smooth. Both
assumptions fail for FDM. This phase establishes what the process actually constrains.

## 7.1 Structural — the load case is external pressure

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P7.01` | The separator body is a **vacuum vessel**, not a pressure vessel. The limiting failure mode is **buckling (stability)**, not hoop stress. Hoop-stress sizing gives absurdly thin walls and is the wrong calculation. | A | vacuum-vessel design literature |
| `P7.02` | Any out-of-roundness or local dent creates a force imbalance that can initiate collapse; distortion need not reach full buckling to be dangerous because it introduces bending into the wall. | A | same |
| `P7.03` | Standard mitigation is **stiffening rings/hoops to maintain curvature**, not uniform wall thickening. Alternatives: internal lattice (a printed UHV chamber used a graded gyroid TPMS lattice + 2.5 mm internal skin), and preserving symmetry so ports stay perpendicular to load paths. | A | same, incl. AM UHV chamber study |
| `P7.04` | FDM violates the isotropy assumption in shell-buckling formulas. Thin-walled structures of few perimeters must be treated as a **laminate**; per-layer fibre orientation materially changes deformation. Many-layer solids approach isotropy; walls do not. | A | `L-THINWALL20` |
| `P7.05` | Measured spread is large and parameter-driven: thin-walled FDM columns in axial compression buckled at PLA 1175 ± 32 N, PETG-1 1910 ± 34 N, PETG-2 1315 ± 27 N. Two PETG configurations differed by 45 %. **Print parameters dominate material choice.** | A | `L-BUCKLE25` |
| `P7.06` | Real load magnitude for this application is small but not negligible: a shop vac can pull >60" WC ≈ 15 kPa; a dust collector <10" WC ≈ 2.5 kPa. `P8.17`–`P8.19` cover which regime applies. | C | `W-ONEIDA` |
| `P7.07` | Field evidence that this is a live risk: a printed 300 mm cyclone was deliberately tested at **maximum power with total blockage** and the author's stated relief was *"I'm glad that it didn't implode."* A dust bin under the same test **did collapse**, and at that moment all dust bypassed to the filter. | D | `S-CD-cyclone2` |
| `P7.08` | The bin — usually treated as an accessory — is the weakest structural element and its failure is a total-performance failure, not a partial one. | E | derived from `P7.07`, `P4.14` |

## 7.2 Sealing

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P7.09` | PETG is the preferred FDM material for airtightness: hydrophobic, better layer adhesion than PLA. | C | print-community + vendor guidance |
| `P7.10` | Slicer/geometry rules that recur across independent sources: wall thickness ≥ 1.2–1.6 mm; 3–5 perimeters; no vase mode; layer height 0.1–0.2 mm; flow 102–105 %; extrusion width > nozzle diameter; higher extrusion temperature. | C | multiple vendor/community sources |
| `P7.11` | Controlled study (Taguchi/ANOVA over perimeters, flow, temperature, layer height, speed on PETG vessels): **number of perimeters and flow are the dominant parameters** for watertightness; one vessel achieved zero leakage. | A | PETG watertightness study |
| `P7.12` | Below ~2 bar differential an untreated print is plausibly adequate; above it, epoxy sealing is generally required. Vacuum service is ~1 bar maximum differential, so unsealed PETG is in range — but untreated PETG contains voids and crevices. | C | same |
| `P7.13` | Practical sealing approach used successfully in DIY builds: **O-rings** at tube/part interfaces (preferred, allows disassembly for testing), or **compression tape** at bin-to-baseplate joints, plus **printed TPU gaskets with a serrated face**, with the mating printed surface serrated to match. | D | `S-CD-build1`, `S-MTL §07:29` |
| `P7.14` | Explicit design intent from a DIY source: *"Everything has to be really airtight so that the pressure loss wouldn't be too big."* Leakage is a performance loss, not only a mess problem — it robs the tool of transport velocity (`P8.11`). | D | `S-MTL` |
| `P7.15` | Threaded printed joints work if clearance is added deliberately: DIY practice is to add margin between threads in CAD (Fusion press-pull on the thread faces) — *"that makes them just connect so much easier."* | D | `S-MTL §07:29` |
| `P7.16` | Heat-set threaded inserts (M4) are the DIY standard for repeatedly-disassembled printed joints. | D | `S-MTL` |
| `P7.17` | Printed parts **shrink and expand over time**; locking nuts were adopted for that reason. Bolted printed assemblies loosen without them. | D | `S-CD-cyclone2`, `S-CD-inlets` |

## 7.3 Surface roughness — an unavoidable variable, direction disputed

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P7.18` | Literature position: roughness ↑ ⇒ `vθ` ↓, vortex length ↓, efficiency ↓, Δp ↓ (`P2.18`). Effect grows with inlet velocity. Roughness heights 0–0.68 mm studied on a 31 mm cyclone. | A | `L-KAYA11` |
| `P7.19` | **A printed cone's layer lines are within that studied roughness band.** A 0.2 mm layer height gives roughness of the same order as the tested range. This is not a negligible manufacturing detail. | E | derived, `P7.18` + `S-MTL` (0.2 mm layers) |
| `P7.20` | DIY test of the opposite hypothesis: a cone printed with a deliberate **0.5 mm wood-grain texture** on the inner wall (CNC Kitchen BumpMesh) measured **99.95 %**, *"slightly better than without the pattern"*. Author's own caveat: *"it is still way too early to draw conclusions with only a few tests performed."* Fines were observed collecting in the riffles. | D | `S-CD-cyclone2 §11:58` |
| `P7.21` | `P7.18` and `P7.20` conflict in direction. Candidate reconciliations: (a) the DIY result is inside measurement noise; (b) macro-riffles trap a boundary layer of dust and act differently from micro-roughness; (c) `P7.18`'s efficiency loss is dominated by coarse particles (>25 µm) which the DIY test did not resolve. Unresolved — `V9.09`. | E | derived |
| `P7.22` | Karagöz's countermeasure is more robust than either: design so the **friction surface and the separation surface are different components** (`P4.23`). Roughness then only costs swirl generation, not separation. | A | `S-KARAGOZ13 §2` |

## 7.4 Splitting, orientation, and print envelope

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P7.23` | Body diameter is capped by the printer bed, not by the design. A 300 mm cyclone was the maximum achievable *"with only the right nozzle and the minimum amount of support material"* on a large-format machine. | D | `S-CD-cyclone2` |
| `P7.24` | Standard split is **barrel / cone**, with a further cone split and a bolted flange when the cone exceeds bed height. Flanges need reinforcement — the first attempt was not strong enough. | D | `S-CD-cyclone2` |
| `P7.25` | Length-modularity is nearly free for a printed device (`P4.25`), and length is a high-leverage, low-Δp-cost variable (`P4.09`). **Splitting the body into stackable length modules converts a manufacturing constraint into a tuning mechanism.** | E | derived, `P4.09` + `P7.24` |
| `P7.26` | Roof/top profile can be tuned to eliminate local support material; a redesign for that reason also fixed first-layer print failures. Support-free geometry is a first-class design objective, not an afterthought. | D | `S-CD-cyclone2 §17:00` |
| `P7.27` | Print orientation controls overhang quality on swirl features: a mirrored impeller curled on the overhang side when sliced counter-clockwise; switching the slicer to clockwise print direction (so the overhang prints last) fixed it. Also affected by ambient temperature. | D | `S-CD-build1` |
| `P7.28` | Chamfers/fillets are added at transitions for aerodynamic reasons *and* printability; one DIY source is explicit that the aerodynamic benefit is assumed, not measured (*"I just hope that helps"*). | D | `S-MTL §03:49` |
| `P7.29` | Acrylic body tube is a viable hybrid (printed ends + bought tube), but acrylic is brittle, melts when cut, and is **strongly triboelectric** — it took a shock hard enough that the author flagged it, and charge only cleared by rinsing with water. | D | `S-CD-build1`, `S-CD-cyclone2` |
| `P7.30` | Transparent body sections are extremely valuable for diagnosis: dust-line count, dune formation, and vortex behaviour were all observed directly, and observations drove design changes. | D | `S-CD-cyclone2`, `S-CD-3rd` |

## 7.5 Electrostatics

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P7.31` | Fine wood dust in insulating plastic ducting charges strongly. Observed effects: dust adhering to walls, dust behaviour changing between test runs, painful discharges, and charge persisting until washed off. | D | `S-CD-cyclone2`, `S-CD-tweaks` |
| `P7.32` | Static **corrupts measurement**: reused test dust became statically charged and produced *"almost unrealistically high"* results, forcing the author to re-mill fresh dust. Merely emptying dust from a plastic bag charged it. | D | `S-CD-cyclone2` |
| `P7.33` | Consensus among woodworking sources: static ignition of a dust deflagration in a **hobby-scale** plastic-ducted system is not a realistic hazard; the practical argument is dust concentration (order 1 lb/min of fine dust through 4" duct would be needed to sustain an explosive mixture). Grounding is done to stop shocks. Sparks from metal striking a fan impeller are the more credible ignition source. | C | `W-WOODWEB` and woodworking community consensus |
| `P7.34` | This changes for commercial operation: NFPA 664/652 (now consolidated into **NFPA 660**) require grounding and bonding of all equipment handling combustible dust plus a Dust Hazard Analysis reviewed every 5 years, and are enforced on small commercial shops. | C | `W-NFPA` |
| `P7.35` | Commercial cyclones in this class advertise **static-dissipative construction** (HDPE with additive). A plain PETG print does not have this property. | C | `W-ONEIDA` |
| `P7.36` | Design-relevant conclusion: treat static as a **measurement-integrity and nuisance** problem at hobby scale (`P7.32`), and as a **compliance** problem if the machine is commercial. Do not treat grounding of an insulator as effective; a bleed path through a high-value resistor is the commonly suggested compromise. | E | derived from `P7.31`–`P7.35` |

## Branch decisions taken from Phase 7

| Branch | Trigger | Goes to |
|---|---|---|
| Bin structural adequacy is a first-class requirement | `P7.07`, `P7.08` | Phase 10 |
| Length-module splitting as a tuning mechanism | `P7.25` | Phase 10 |
| Static corrupts DIY measurement ⇒ affects how much of the `S-CD` dataset is usable | `P7.32` | Phase 9 |
| Vacuum vs dust-collector pressure regime decides wall sizing | `P7.06` | Phase 8 |
