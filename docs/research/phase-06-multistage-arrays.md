# Phase 6 — Multi-stage series and parallel arrays

Branch chosen from `P1.28`, `P4.20`, `P5.26`.
Rationale: `x50 ∝ √D` at fixed velocity, but `Q ∝ D²`. Fine cut and useful flow are only
simultaneously obtainable by multiplying units. Both DIY sources independently arrived here.

## 6.1 The scaling argument

```
# Tier E (derived, see P1.26-P1.28). The core sizing identity for arrays.
#
# Hold vin at the family design value.  Then for one unit:
#     Q_unit  = vin * (a/D) * (b/D) * D**2
#     x50     ∝ sqrt(D)
#
# To hold total Q while shrinking D by factor k (D -> D/k):
#     n_units = k**2                       # unit count grows as the square
#     x50     -> x50 / sqrt(k)             # cut size improves as sqrt only
#
# Cost of a sqrt(2) better cut size: 4x the units.
# Delta_p is UNCHANGED (P1.25) -- the array is not a pressure penalty, it is a plumbing penalty.
```

| ID | Claim | Tier |
|---|---|---|
| `P6.01` | Diminishing returns are severe: 4× the parts for 1.41× the cut size. Arrays make sense as a **second stage on already-cleaned gas**, not as a replacement for the first stage. | E |
| `P6.02` | Independently reached by DIY practice: *"you want the cross-section of the airflow to stay roughly the same throughout the whole device. And since you need smaller cyclones to separate smaller particles, that means more of them are needed to keep up with the airflow"* — 7 small cyclones arranged around the first stage's outlet. | D |

## 6.2 Series staging

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P6.03` | Series staging is the pattern every source converged on: a coarse first stage sized for chip volume, then one or more fine stages on cleaned gas. | D | `S-MTL`, `S-CD-*` |
| `P6.04` | Measured stage split in a two-stage DIY separator: **first stage ≈ 80 % of collected mass**, second ≈ 20 %. Bin volumes were sized on that ratio. | D | `S-CD-build2` |
| `P6.05` | Measured incremental value of a third stage on fine material: 500 g of superfine plywood/oak dust — third stage captured 20 g, moving overall **94 % → 98 %**. On MDF: 107 g fed, third stage took 5 g, **78 % → 84 %**. | D | `S-CD-tweaks` |
| `P6.06` | Cyclone + downstream centrifugal stage measured **99.9 %–99.98 %**, approaching 99.99 %. Baseline commercial cyclone alone: 99.9 % on planer shavings, ~99.5 % (best) on an MDF/plywood mix, dropping below 99 % at very high feed rate. | D | `S-CD-cyclone1` |
| `P6.07` | Absolute mass framing (more useful than percentages): a commercial 4/5" cyclone passed **9–15 g of dust per kg processed** to the filters; the second stage reduced that to **≈1 g/kg**. | D | `S-CD-cyclone1` |
| `P6.08` | Staging shifts *which* stage does what: improving stage 2 means stage 3 only has to handle the smallest sizes. Explicitly used as a design strategy. | D | `S-CD-3rd` |
| `P6.09` | Stage-to-stage coupling is real: the second stage can be **overwhelmed** when the first stage overflows, producing "dust dunes" in the downstream tube and a collapse in efficiency. Bin fill state on stage 1 therefore controls stage 2 performance. | D | `S-CD-psd`, `S-CD-shop` |

## 6.3 Parallel arrays — the failure modes

| ID | Claim | Tier | Src |
|---|---|---|---|
| `P6.10` | Multicyclones **usually measure worse than an isolated cell** at the same conditions. | A | Reznik & Matsnev via `L-MULTI19` |
| `P6.11` | Named causes: (1) inlet flow maldistribution, (2) gas circulation in the **common dust hopper** causing re-entrainment, (3) leakage through gaskets, (4) plugging of gas exits or swirl vanes. All connect to **cross-talk in the dust plenum**. | A | Crane & Behrouzi via secondary |
| `P6.12` | Cross-talk mechanism: unequal flow creates a pressure spread across the cells' dust outlets; gas then flows *between* tubes through the shared hopper. "Donor" cells push gas into the hopper, "receptor" cells draw it back up through their cones — carrying collected fines with it. | A | secondary |
| `P6.13` | Cross-talk is **not detectable from clean-gas flow measurements**: in one study, per-cell clean-gas rates differed by no more than a few percent, yet hopper circulation was a material efficiency loss. | A | flow-visualisation study |
| `P6.14` | Baffles suppressed the circulation but recovered **less than half** the efficiency gap; residual loss was concentrated in particles **smaller than the feed MMD** — i.e. exactly the fraction the array exists to catch. | A | flow-visualisation study |
| `P6.15` | The theoretical benefit of more, smaller cells holds **only on condition** that gas and solids are equally distributed and bypass through the solids outlets is prevented. | A | `L-MULTI19` |
| `P6.16` | Contrarian result: four identical axial-symmetrically arranged cells measured **higher** overall efficiency than a single cyclone (Δp +16.8 %), with no cross flow found in the shared hopper. Attributed to symmetric vortex systems stabilising each other. | A | `L-LIU14` |
| `P6.17` | Arrangement matters: **axial-symmetric** beats central-symmetric for particle-flow uniformity; arrangement optimisation improved the standard deviation of flow distribution by 27.5 %. | A | multi-cyclone arrangement study |
| `P6.18` | Header design rule: divide the upstream passage into one flowpath per cell with **gradually decreasing cross-sectional area**, to minimise area-change losses. | A | patent/design literature |
| `P6.19` | Growing evidence that two-phase flow through multiple parallel paths is **inherently non-uniform**, so cells each designed for optimum flow will collectively run off-optimum. | A | CFB literature |

## 6.4 Reconciliation

| ID | Statement | Tier |
|---|---|---|
| `P6.20` | `P6.10` and `P6.16` are reconciled by `P6.11`+`P6.17`: parallel arrays lose when the hopper is shared and the arrangement is asymmetric; they can win when the arrangement is axially symmetric and the underflows are isolated. **Isolation of the dust outlets is the discriminating variable.** | E |
| `P6.21` | Practical corollary: an array of small cyclones dropping into one common bin is the configuration the literature says fails. Both DIY designs in this corpus do exactly that (`S-MTL`: 7 cyclones into one shared chamber; `S-CD`: two tubes into shared bins until a divider was added). | E |
| `P6.22` | DIY corroboration of `P6.11`(1) and `P6.21`: a community suggestion to give each dust outlet its **own bin** so *"the air cannot travel from left to right and affect the efficiency"* — implemented as an acrylic divider inside the shared bin, because four bins would not fit. | D |
| `P6.23` | DIY corroboration of `P6.19`: with a Y-piece feed, *"large amounts of dust particles are hitting one spot"* and one tube processed almost all the material, overwhelming its stage-2. Fixed only partially by straightening the upstream run. Author's own diagnosis: *"the main performance limitation is the dust distribution difference between the two tubes"* — which motivated collapsing two tubes into one larger tube. | D |
| `P6.24` | Consolidating from two parallel units to one larger unit produced the best results in that series (close to 99.99 % on planer shavings), consistent with `P6.19`/`P6.23`. **Empirical vote against parallelism at small scale.** | D |

## 6.5 Sizing rule for arrays

| ID | Rule | Tier | Src |
|---|---|---|---|
| `P6.25` | Total inlet cross-section of the array should equal the feeding duct cross-section, to hold velocity constant through the device. | D/E | `S-MTL §03:49`; consistent with `P1.33` |
| `P6.26` | Same rule applied in the other series: an inlet redesigned *"with smaller holes so that the total surface area is equal to that of a 100 mm tube"*. | D | `S-CD-tweaks` |
| `P6.27` | This is the correct rule **only if** the array cells are meant to run at the same inlet velocity as the feed duct. Design velocity is a per-family property (`P1.33`), and the transport velocity requirement in the duct (`P8.11`) is a different number. The two coincide only by accident. | E | derived |

## Branch decisions taken from Phase 6

| Branch | Trigger | Goes to |
|---|---|---|
| Underflow isolation is the discriminating variable for arrays | `P6.20` | Phase 10 |
| Stage 1 bin fill state gates whole-system performance | `P6.09` | Phase 8, Phase 10 |
| Percentage efficiency is a bad metric; g/kg is better | `P6.07` | Phase 9 |
