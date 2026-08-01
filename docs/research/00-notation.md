# Canonical notation

All corpus files use these symbols. Source-specific symbols are remapped on entry (see §Remapping).
Units are SI unless a row says otherwise. Every dimension is also expressed as a ratio to `D`.

## Geometry

| Sym | Ratio form | Unit | Meaning |
|---|---|---|---|
| `D` | — | m | Cyclone body (barrel) inner diameter. The scaling datum. |
| `a` | `a/D` | m | Inlet height (axial dimension of rectangular inlet) |
| `b` | `b/D` | m | Inlet width (radial dimension of rectangular inlet) |
| `De` | `De/D` | m | Vortex finder (gas outlet tube) inner diameter |
| `S` | `S/D` | m | Vortex finder insertion depth below cyclone roof |
| `h` | `h/D` | m | Cylindrical barrel height (roof to cone start) |
| `H` | `H/D` | m | Total separator height (roof to cone tip) |
| `Hc` | `(H−h)/D` | m | Cone height |
| `B` | `B/D` | m | Cone tip (dust outlet) diameter |
| `ε` | — | ° | Cone **semi**-angle: `tan ε = (D−B)/(2·Hc)` |
| `Ln` | `Ln/D` | m | Natural vortex length, measured **from the vortex-finder lip downward** |
| `Ld` | `Ld/D` | m | Dipleg / extension tube length below cone tip |

## Flow and fluid

| Sym | Unit | Meaning |
|---|---|---|
| `Q` | m³/s | Volumetric gas flow through the cyclone |
| `vin` | m/s | Mean inlet velocity, `vin = Q/(a·b)` |
| `vθmax` | m/s | Peak tangential velocity (at the free/forced vortex boundary) |
| `vs` | m/s | Saltation velocity — wall tangential velocity at which deposited solids re-entrain |
| `ρ` | kg/m³ | Gas density (air, 20 °C, 1 atm: 1.20) |
| `μ` | Pa·s | Gas dynamic viscosity (air, 20 °C: 1.81e-5) |
| `Δp` | Pa | Static pressure drop, inlet plane to gas-outlet plane |
| `n` | — | Vortex exponent in `vθ·rⁿ = const` (outer/free vortex) |

## Particulate

| Sym | Unit | Meaning |
|---|---|---|
| `ρp` | kg/m³ | Particle true density (dry softwood ≈ 400–550; MDF ≈ 700–800; use 730 for wood-shop work, see P8.02) |
| `x` | m (report µm) | Particle diameter, aerodynamic equivalent unless stated |
| `x50` | µm | Cut size — diameter collected at 50 % efficiency. `d50` in some sources; identical. |
| `T(x)` | — | Grade (fractional) efficiency at size `x`, 0–1 |
| `η` | — | Overall mass collection efficiency, 0–1 |
| `β` | — | Grade-curve sharpness exponent in the logistic form `T = 1/(1+(x50/x)^β)` |
| `σ_T` | — | Grade-curve slope in log-normal form, `σ_T = x84.1/x50 = x50/x15.9`. **Larger = shallower.** |
| `μ_L` | kg/kg | Solids mass loading, `ṁ_solid / ṁ_gas` |
| `μ_Gr` | kg/kg | Limit loading above which non-size-selective bulk separation occurs |

## Dimensionless

| Sym | Definition | Meaning |
|---|---|---|
| `Eu` | `Δp / (½·ρ·vin²)` | Euler number = dimensionless pressure drop = number of inlet velocity heads |
| `NH` | ≡ `Eu` | "Number of velocity heads". Same quantity, older naming. |
| `Stk50` | `ρp·x50²·vin / (18·μ·D)` | Stokes number at cut size |
| `Re` | `ρ·vin·D/μ` | Cyclone Reynolds number |
| `Ne` | — | Effective number of gas revolutions in the outer vortex |

## Remapping table (source symbol → canonical)

| Source | Their symbol | Canonical |
|---|---|---|
| Koch & Licht / powderprocess | `Dc, Hc, Bc, Sc, Di, Lc, Zc, Ds` | `D, a, b, S, De, h, Hc, B` |
| Elsayed / Singh (co-Kriging) | `Dx, Ht, Bc` | `De, H, B` |
| TU Dresden (Wessely) | `da, di, ri, Tauchrohr, hi, x_TR, U, F` | `D`(body)… see note | 
| Texas A&M (Wang/Parnell) | `Dc, De, W, H(inlet)` | `D, De, b, a` |
| Lapple/Cooper&Alley | `W` (inlet width), `H` (inlet height) | `b`, `a` — **inverted vs `H`=total height elsewhere** |

> **Trap `N.01`:** TU Dresden normalises to the **vortex-finder radius `ri`**, not body diameter.
> Its `Hi = (H−h_inlet)/ri`, `R = ra/ri`, `Re = re/ri`, `F = a·b/(π·ri²)`. Do not mix its ratios
> with `…/D` ratios without converting: `ri = De/2`.

> **Trap `N.02`:** Cooper & Alley / Lapple lineage uses `H` for **inlet height** and `W` for inlet
> width. Everywhere in this corpus `H` = total cyclone height and inlet height is `a`.

> **Trap `N.03`:** "Slope" of a grade curve is reported two incompatible ways. `σ_T` (ratio form,
> larger = shallower) and `β` (exponent form, larger = sharper). Always name which.
