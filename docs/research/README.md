# Cyclonic Separator Research Corpus — Stage 1

**Project goal (Stage 2, NOT this stage):** printable STL set for a cyclonic pre-separator on a
CNC-router vacuum line.
**This stage:** research only. No geometry, no CAD, no chosen dimensions. Output is a decision
substrate for Stage 2.

## Conventions (binding for every file in this corpus)

| Rule | Meaning |
|---|---|
| Reference > full text | Cite `[KEY §loc]`. Never paste source prose. Regeneration commands live in [01-sources.md](01-sources.md). |
| LLM-actionable > readable | Tables, typed claims, pseudocode. No narrative. |
| One notation | Every symbol resolves via [00-notation.md](00-notation.md). Source notation is remapped on entry, never carried through. |
| Claim IDs | Every non-obvious assertion is `P1.03`-style: `<phase>.<seq>`. Referenced elsewhere by ID. |
| Confidence tier | Every claim carries `A`–`E`. See below. Never state a `D`/`E` claim as fact. |
| Pseudocode > code | Models are written as language-neutral pseudocode with explicit units. |
| Skeptical | Contradictions are logged in [phase-09-validation.md](phase-09-validation.md), not silently resolved. |

### Confidence tiers

| Tier | Basis |
|---|---|
| `A` | Peer-reviewed primary work with reported experimental or CFD data |
| `B` | Peer-reviewed review / secondary synthesis / textbook |
| `C` | Engineering handbook, standards body, vendor datasheet |
| `D` | Uncontrolled DIY experiment (single operator, uncalibrated instruments) |
| `E` | Derived in this corpus, or asserted by a source without shown data |

## Phase index

| Phase | File | Scope | Branch chosen from |
|---|---|---|---|
| 1 | [phase-01-physics.md](phase-01-physics.md) | Flow field, forces, cut-size and pressure-drop models, scaling laws | — |
| 2 | [phase-02-design.md](phase-02-design.md) | Standard geometry families, ratio tables, feasibility constraints | P1 |
| 3 | [phase-03-optimization.md](phase-03-optimization.md) | Objective functions, Pareto structure, published optima | P2 |
| 4 | [phase-04-vortex-length-dust-outlet.md](phase-04-vortex-length-dust-outlet.md) | Natural vortex length, vortex end, hopper, re-entrainment | P1.42, P2.17, P3.07, P3.20 |
| 5 | [phase-05-inlet-vortex-finder.md](phase-05-inlet-vortex-finder.md) | Inlet topologies, neutral vane, short-circuit flow, vortex finder | P1.04, P1.41, P3.05 |
| 6 | [phase-06-multistage-arrays.md](phase-06-multistage-arrays.md) | Series staging, parallel arrays, maldistribution, cross-talk | P1.28, P4.20, P5.26 |
| 7 | [phase-07-manufacture-3dprint.md](phase-07-manufacture-3dprint.md) | FDM constraints: buckling, sealing, roughness, splitting | P2.18, P3.24, P4.25 |
| 8 | [phase-08-system-integration.md](phase-08-system-integration.md) | CNC-router duty: PSD, flow, transport velocity, fan matching | P1.31, P1.33, P3.25 |
| 9 | [phase-09-validation.md](phase-09-validation.md) | Measurement method, contradiction log, what the evidence does *not* support | all |
| 10 | [phase-10-design-space.md](phase-10-design-space.md) | Constraint synthesis + open decisions handed to Stage 2 | all |
| 11 | [phase-11-vacuum-source.md](phase-11-vacuum-source.md) | LVHP vacuum source: motor class, parallel topology, 120 V circuit allocation | P8.79–P8.97, P8.67 |

## Reading order for an agent

1. [00-notation.md](00-notation.md) — mandatory, symbols are ambiguous across sources.
2. [phase-10-design-space.md](phase-10-design-space.md) — the compressed answer.
3. [phase-09-validation.md](phase-09-validation.md) — what is *not* established.
4. Drill into individual phases by claim ID only when a decision depends on it.

## Status

Stage 1 complete for phases 1–10. Unexplored branches recorded in
[phase-09-validation.md](phase-09-validation.md) §Deferred.

**Decisions taken:** `Q1` = **shop vac** (2026-07-29). Derivation and downstream effects in
phase-08 §8.6 and [phase-10 §10.8](phase-10-design-space.md#108-consequences-of-q1--shop-vac).
`Q4` = **Bambu Lab P1S**; `Q2` narrowed to **RIDGID WD06701, 40–70 CFM**. Derivations in
phase-08 §8.6–§8.7 and [phase-10 §10.8–§10.9](phase-10-design-space.md).
Governing result: **scale by unit count, not unit size** (`U1`–`U4`).
`Q5` = **2 × Greif 30-gal open-head steel drum** (`P4.78`–`P4.91` — body solved, the flat lid is the part at risk).
**Flexibility lives in the code, not the cyclone** (`F1`–`F6`): Stage 2's deliverable is a parametric
generator plus one fixed printed geometry. `Q6` = **hobbyist on a commercial machine** (Signstech N1313, 4×4 ft, 3 HP). Still open: `Q3` (objective) — does not block.
**Live tension:** the boot passes ~265 CFM; the shop vac gives 40–70 (`P8.81`–`P8.83`, `P8.91`).
**Architecture selected:** single 1D3D cyclone, circumferential courses, one drum + one swap spare —
[phase-10 §10.11](phase-10-design-space.md). **Build 1 is the active scope:** `D`=118 mm @ 55 CFM (estimate; no flow measurement available, `D4`/`D7`).
Build 2 (`D`=240 mm @ 265 CFM) is deferred until the LVHP system is designed — the generator must still carry it (`D9`).

**Stage 1 is closed.** Next deliverable is the parametric generator, not geometry (§10.6).

**LVHP vacuum source (2026-08-01):** phase 11 opened for the CamVac-class drum extractor that
unblocks build 2. Configuration selected (revised same day, `Q-V1` resolved): **3 × 900 W
116392-class tangential bypass motors, parallel — two on the 20 A circuit, one on the 15 A —
lid drilled for four** (`P11.20`). ~235–255 CFM at duty vs the 265 CFM ceiling. Open: `Q-V2`, `Q-V4`, `Q-V5`.
