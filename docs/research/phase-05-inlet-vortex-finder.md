# Phase 5 — Inlet topology and vortex finder

Branch chosen from `P1.04`, `P1.41`, `P2.13`, `P3.05`, `P3.11`.
Rationale: `De/D` is the master trade variable and the optimiser disagrees with classical values;
inlet topology is the one place where a printed part can do something a rolled-sheet part cannot.

## 5.1 Inlet topologies

| ID | Topology | Description | Reported effect | Tier | Src |
|---|---|---|---|---|---|
| `P5.01` | **Tangential slot** (classical) | rectangular duct meeting the barrel on a tangent, flat roof | baseline; `ζ_E = 0` in the Barth loss decomposition | B | `S-TUD §Einlaufformen`, `S-TUD eq.(17)` |
| `P5.02` | **Volute / scroll (wrap-around)** | inlet wraps part of the circumference, roof steps down | ↓ short-circuit flow ⇒ ↑ separation efficiency; **↑ pressure drop** | A | volute-helical inlet study |
| `P5.03` | **Helical roof** | inlet roof descends helically into the barrel | ↑ short-circuit flow ⇒ ↓ separation efficiency; **↓ pressure drop**. Highest aerodynamic efficiency at ~20° roof angle. | A | helical-roof inlet studies |
| `P5.04` | **Axial with swirl vanes** | flow enters axially, vanes impart swirl | listed as an alternative primary mechanism to tangential entry | B | `S-TUD §Wirkprinzip` |
| `P5.05` | **Symmetrical spiral (CSSI)** | two converging spiral inlets | "significantly increases collection efficiency with insignificant increase in pressure drop" | A | `L-ZHAO04` |
| `P5.06` | **Symmetrical double (180°)** | two opposed tangential inlets | **Contradictory literature.** Some report ↑ tangential velocity and ↑ efficiency at equal total area; others report ↓ efficiency *and* ↓ Δp. | A | contradictory; see `V9.08` |
| `P5.07` | Motivation for symmetric/wrap topologies: the single inlet is the *only* asymmetry in a conventional cyclone and is blamed for the precessing vortex core (`P1.43`). | B | secondary |

| ID | Quantitative anchors | Tier |
|---|---|---|
| `P5.08` | Tangential inlet angled 45° vs 0°: efficiency 92 % → 90.5 %, Δp 579 → 620 Pa. Angling costs on both axes for that case. | A |
| `P5.09` | Industrial scroll inlet at 0° vs 30/45/60°: increasing angle **decreased** total Δp. Direction of the efficiency change not captured. | A |
| `P5.10` | Inlet angle effects are reported as **non-monotonic** by some authors and monotonic by others. Do not extrapolate. | A |

## 5.2 The "neutral vane" / air ramp

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P5.11` | Commercial claim: an integrated air ramp with a neutral-vane inlet improves separation efficiency by **20 %**. Patent-protected (US 7282074, USD703401). No supporting data published. | C/E | `W-ONEIDA` |
| `P5.12` | Independent DIY reconstruction and diagnosis of the same mechanism: with a fully open cyclone top, *"air that is spinning inside the cyclone will collide with air that will enter the cyclone"* — audible as a flapping sound at high flow. Fix implemented: a tube segment sliding into the inlet and reaching to the centre of the outlet tube, i.e. a vane separating incoming from circulating flow. | D | `S-CD-cyclone2 §07:59` |
| `P5.13` | The physically correct framing of `P5.11`/`P5.12` is the **volute/scroll benefit of `P5.02`**: preventing the incoming jet from colliding with already-rotating gas is the same thing as suppressing short-circuit and roof-region mixing. A neutral vane is a cheap partial volute. | E | derived, `P5.02` + `P5.12` |
| `P5.14` | A full spiral top section was identified as the correct solution and deliberately deferred in favour of the simpler vane. The DIY series never isolated the vane's contribution — it was introduced alongside other changes in the same test (the author flags this as *"a classical mistake"*). **The 20 % figure has no independent support in this corpus.** | D/E | `S-CD-cyclone2` |

## 5.3 Vortex finder diameter `De`

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P5.15` | `De` ↓ ⇒ `vθmax` ↑ ⇒ efficiency ↑, Δp ↑. Monotonic in both. | A | `L-XIANG08` |
| `P5.16` | Quantified on the Pareto front: `De/D` 0.75 → 0.40 gives `Eu` ×3.9 and `Stk50` ÷5.5 (`P3.05`). Efficiency is bought with pressure at roughly `Δ(cut size) ~ Δ(Eu)^-1.2` over that range. | A/E | `L-SINGH17 Tab.1` + fit |
| `P5.17` | Classical families cluster at `De/D = 0.4–0.5`; optimisers push to 0.28–0.40 when maximising efficiency. The classical value is a **pressure-drop compromise**, not an efficiency optimum. | A/E | `P2.02` + `P3.03` tables |
| `P5.18` | Countervailing report: `De/D = 0.5–0.6` gives the *smallest* pressure drop (Kim & Lee) — consistent with `P5.15` since larger `De` lowers Δp, but it means Stairmand HE's 0.5 is near a Δp optimum, not an efficiency one. | C | secondary |
| `P5.19` | DIY: reducing a downstream separator's air-outlet diameter while moving it clear of the dust-outlet path cut filter carry-over **16 g → 3 g (−80 %)** in one change. Different device class (`P2.31`) but the same physics: outlet area sets core velocity. | D | `S-CD-3rd §13:52` |
| `P5.20` | DIY: reducing outlet tube from 150 mm to 100 mm downstream of a cyclone raised measured resistance but *"didn't affect the airflow"* — i.e. within that system the fan was operating on a flat part of its curve. Measurement was noisy and the author distrusted it. | D | `S-CD-cyclone1 §05:53` |

## 5.4 Vortex finder insertion depth `S`

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P5.21` | `S` exists to prevent short-circuit flow across the roof (`P1.41`). Constraint form used in optimisation: `S > 1.25·a`. | A | `L-SALCEDO01 eq.9` |
| `P5.22` | `S` is subtracted from the available vortex length: `Ln < H − S` (`C9`). Deep insertion trades short-circuit protection for separation length. | A | `L-SALCEDO01 eq.10` |
| `P5.23` | `S-KARAGOZ13` sets `S = b` (insertion equal to inlet width) — much shallower than `P5.21` requires. Classical families sit at `S/D` 0.5–0.625, i.e. `S/a` = 1.0–1.25. **Nobody actually satisfies `S > 1.25a` strictly** (`P2.23`). | E | `S-KARAGOZ13 Tab.1` + `P2.02` |
| `P5.24` | Optimisers drive `S` to the lower bound (`P3.07`) because short-circuiting is not in the objective functions. This is a known blind spot, not a recommendation. | E | derived |
| `P5.25` | An adjustable-depth vortex finder (ring clamp) was built specifically to explore this axis in DIY work; results were not isolated. | D | `S-CD-cyclone2` |
| `P5.26` | Distinct and separately useful: a **second concentric tube protruding into the cyclone gas outlet** created a region where *"dust was spinning between the two walls, preventing dust escaping from the cyclone"*, worth **+50 % captured fine dust**. This is an outlet-side re-separation feature, not a vortex-finder depth effect. | D | `S-CD-cyclone1 §12:16` |

## 5.5 Inlet ducting upstream of the cyclone

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P5.27` | A bend immediately upstream of the inlet concentrates solids on one side of the duct and delivers them to a single spot inside the separator, causing local overload and clogging at high feed rate. | D | `S-CD-tweaks`, `S-CD-inlets` |
| `P5.28` | Mitigation that measurably helped: a **straight run of tube between the bend and the inlet** to let the flow re-develop. Reported as "smoothed out the dust flow and provided some improvement", but "still resulted in varying outcomes". Introduced independently by two DIY sources. | D | `S-CD-tweaks`, `S-CD-cyclone2` |
| `P5.29` | Flex hose is the dominant restriction in a shop branch. Ridges create turbulence and large friction loss; smooth bore raises flow but is less flexible. Keep flex short. | C | `W-WOODWEB` |
| `P5.30` | Inlet **transition geometry matters at the few-percent level**: a scaled-up inlet not compensated at the reducer produced a *"noticeable transition"* and a measurable pressure-loss penalty (88 → 94 mm H₂O, ~7 %). | D | `S-CD-inlets §14:00` |

## Branch decisions taken from Phase 5

| Branch | Trigger | Goes to |
|---|---|---|
| Vane / volute roof is printable in a way sheet metal is not | `P5.02`, `P5.13` | Phase 7, Phase 10 |
| Outlet-side re-separation stage (`P5.26`) is a staging question | `P5.26` | Phase 6 |
| Upstream straight-run requirement is a system-integration constraint | `P5.28` | Phase 8 |
