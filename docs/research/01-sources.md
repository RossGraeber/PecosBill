# Source register

Citation keys are stable. `§loc` = section/page/timestamp within the source.
`Tier` = default confidence contributed by this source (individual claims may be downgraded).

## Seeds (supplied in this repo)

| Key | Tier | Source | Local | Notes |
|---|---|---|---|---|
| `S-KARAGOZ13` | A | Karagöz, Avci, Sürmen, Şendoğan (2013) *Design and performance evaluation of a new cyclone separator*, J. Aerosol Sci. 59:57–64 | `Design_and_performance_evaluation_of_a_n.pdf` | Double-cylinder + movable vortex limiter, no cone. Experimental, cement dust. |
| `S-TUD` | B | Wessely, B. — *Zyklonabscheider*, TU Dresden, AG Mechanische Verfahrenstechnik lecture notes | `zyklonabscheider.pdf` | Barth/Muschelknautz derivation, VDI-Wärmeatlas lineage. Equations numbered (1)–(23). |
| `S-MTL` | D | manutechlab, *This 3D print saves hours of my life — Cyclone separator build*, YouTube `r7l1OLJz-zU` | — | 3D-printed 1st-stage cyclone + 7× parallel 2nd stage. Cites `S-TUD` as its design basis. |
| `S-CD` | D | Capturing Dust (Ruud / Makerr-Studio), YouTube `@CapturingDust`, 15 videos | — | Quantitative DIY separator testing series. Per-video keys below. |

### `S-CD` sub-keys

| Key | Video ID | Title (abbrev.) | Contribution |
|---|---|---|---|
| `S-CD-intro` | `Rek9JS93cDw` | Channel intro | Lineage: Harvey Gyro Air G700 → Under Dunn → Pilson Guitars → this |
| `S-CD-mk2` | `F0A8KP7Q6Y0` | They Were So Close | 99.6 % single unreliable measurement; Harvey claim 99.7 % |
| `S-CD-build1` | `bCNDPIjRccw` | Built it Again (€200) | Acrylic vs PVC tube build, O-ring sealing, print orientation |
| `S-CD-build2` | `j7K9fEa8Re8` | Baseplate + bins | Bin sealing, T-loc, 1st:2nd stage split ≈ 80:20 by mass |
| `S-CD-psd` | `oS5XjIMpJDc` | Dust, Sizes… (Part 3) | Efficiency vs material: flour 64 %, sawdust 88–92 %, shavings 98–99 %, sugar 99.0 % |
| `S-CD-tweaks` | `BDPNMnRbd3o` | Small Changes, Massive Effect | 3rd stage prototype; sieve fractions; area-matched inlet; ultrafine penetration test |
| `S-CD-3rd` | `b8vZ6c8PIvw` | Supercharged my Centrifugal Separator | U-tube manometer method; outlet-diameter change 16 g→3 g in filter; scale accuracy problem |
| `S-CD-year` | `oz4CENU0_kQ` | 1 Year to Improve Dust Collection | Filter-tube test rig; cartridge vs bag resistance; 99.7 % at 45 kg/h |
| `S-CD-inlets` | `tZCCDNiilhE` | Cyclonised my Separator | Cyclone-style inlets; feed-rate collapse to 92.8 %; pressure loss vs inlet scaling |
| `S-CD-cyclone1` | `S1seMU0ixcs` | Supercharged a Cyclone | Oneida SDD 4/5 baseline: 99.9 % shavings, ~99.5 % MDF; 9–15 g/kg escaping |
| `S-CD-cyclone2` | `vspF43frvKE` | Simplified this 3D Printed Cyclone | Fully printed 300 mm cyclone; 98.4 %→99.95 %; neutral vane; cone-vs-tube test; wall texture test |
| `S-CD-valve` | `rWP6IuOOTwI` | Ball Valve for CamVac | +6–15 % airflow by blocking idle motor outlet |
| `S-CD-air` | `ng0CcTls65Q` | DIY HEPA vs Festool SYS-AIR | Air-cleaner comparison; 0.3 µm is worst-case filter size |
| `S-CD-shop` | `uUOQLDqXV3o` | Overhead Dust Collection | Long-run field result: 250 m floorboards, 6 bags collected |
| `S-CD-30min` | `ENybYVAr11Q` | 30-min planer test | Long-form material sweep (no captions available) |

**Regenerating `S-MTL` / `S-CD` text** (transcripts are deliberately not stored here — reference > full text):

```
yt-dlp --skip-download --write-auto-subs --write-subs --sub-lang 'en.*' \
       --sub-format vtt --write-description -o '%(id)s.%(ext)s' \
       'https://www.youtube.com/@CapturingDust/videos'
```

## Literature

| Key | Tier | Source | Access |
|---|---|---|---|
| `L-STAIRMAND51` | B | Stairmand, C.J. (1951) *The design and performance of cyclone separators*, Trans. IChemE 29:356–383 | via compilations |
| `L-SHEPLAP39` | B | Shepherd & Lapple (1939) *Flow pattern and pressure drop in cyclone dust collectors*, Ind. Eng. Chem. 31(8):972–984 | via compilations |
| `L-LAPPLE51` | B | Lapple (1951) — Classical Cyclone Design (CCD) grade-efficiency curve | via compilations |
| `L-SWIFT69` | B | Swift, P. (1969) Steam Heat. Engr. 38:453–456 | via compilations |
| `L-ALEXANDER49` | B | Alexander, R.M. (1949) *Fundamentals of cyclone design and operation*, Proc. Aust. IMM 152:203–228 | via compilations |
| `L-BARTH56` | B | Barth, W. (1956) equilibrium-orbit model | via `S-TUD`, `L-HOFFSTEIN` |
| `L-MUSCH72` | B | Muschelknautz, E. (1972) CIT 44(1+2):63–71; VDI-Wärmeatlas 6th ed. (1991) | via `S-TUD` |
| `L-KOCHLICHT77` | C | Koch & Licht (1977) standard-geometry compilation table | reproduced at powderprocess.net |
| `L-IOZIALEITH89` | A | Iozia & Leith (1989) *Effect of cyclone dimensions on gas flow pattern and collection efficiency*, Aerosol Sci. Technol. 10(3):491–500 | abstract + secondary |
| `L-IOZIALEITH90` | A | Iozia & Leith (1990) *The logistic function and cyclone fractional efficiency*, Aerosol Sci. Technol. | abstract + secondary |
| `L-RAMA91` | A | Ramachandran, Leith, Dirgo, Feldman (1991) *Cyclone optimization based on a new empirical model for pressure drop*, Aerosol Sci. Technol. 15:135–148 | doi:10.1080/02786829108959520 |
| `L-WANG01` | A | Wang, Parnell, Shaw (2001) *Analysis of cyclone pressure drop*, Beltwide Cotton Conf. 2:1325–1329 | open PDF, cotton.org |
| `L-WANG02` | A | Wang, Parnell, Shaw (2002) *Study of the cyclone fractional efficiency curves*, CIGR J. Sci. Res. Dev. IV, BC 02 002 | open PDF, cigrjournal.org |
| `L-SALCEDO01` | A | Salcedo & Cândido (2001) *Global optimization of reverse-flow gas cyclones*, Sep. Sci. Technol. 36(12):2707–2731 | open PDF, advancedcyclonesystems.com |
| `L-SINGH17` | A | Singh, Couckuyt, Elsayed, Deschrijver, Dhaene (2017) *Multi-objective geometry optimization of a gas cyclone using triple-fidelity co-Kriging surrogate models*, J. Optim. Theory Appl. | doi:10.1007/s10957-017-1114-3, open access |
| `L-ELSAYED10` | A | Elsayed & Lacor (2010) Chem. Eng. Sci. 65:6048–6058 — min-Δp geometry optimization | abstract + secondary |
| `L-ELSAYED11` | A | Elsayed & Lacor (2011) Appl. Math. Model. 35:1952–1968 — inlet dimension effects | abstract + `S-KARAGOZ13` §1 |
| `L-ELSAYED12` | A | Elsayed & Lacor (2012) Powder Technol. 217:84–99 — RBF-ANN + NSGA-II Pareto | abstract + secondary |
| `L-KAYA11` | A | Kaya, Karagöz, Avci (2011) *Effects of surface roughness on the performance of tangential inlet cyclone separators*, Aerosol Sci. Technol. 45(8):988–995 | abstract + secondary |
| `L-KARAGOZ05` | A | Karagöz & Avci (2005) *Modelling of the pressure drop in tangential inlet cyclone separators*, Aerosol Sci. Technol. 39:857–865 | abstract |
| `L-AVCI13` | A | Avci, Karagöz, Sürmen (2013) *Development of a new method for evaluating vortex length in reversed flow cyclone separators*, Powder Technol. 235:460–466 | abstract |
| `L-KAYA09` | A | Kaya & Karagöz (2009) *Numerical investigation of performance characteristics of a cyclone prolonged with a dipleg*, Chem. Eng. J. 151:39–45 | via `S-KARAGOZ13` refs |
| `L-DIRGO85` | A | Dirgo & Leith (1985) *Cyclone collection efficiency: comparison of experimental results with theoretical predictions*, Aerosol Sci. Technol. | abstract |
| `L-BOHNET97` | B | Bohnet, M. (1997) cyclone model — basis of the powderprocess.net step-by-step method | via `W-PPN-DESIGN` |
| `L-BOHNETLORENZ` | A | Bohnet & Lorenz — pressure-drop model; best match to measurement for the `RS_VHE` geometry | via `L-SALCEDO01` |
| `L-MOTHES` | A | Mothes & Löffler — finite-diffusivity collection model | via `L-SALCEDO01` |
| `L-YOSHIDA` | A | Yoshida et al. (2001, 2003, 2010) — apex-cone height/shape effects on classification | via `S-KARAGOZ13` refs |
| `L-SURMEN11` | A | Sürmen, Avci, Karamangil (2011) *Prediction of the maximum-efficiency cyclone length…*, Powder Technol. 207:1–8 | abstract |
| `L-HOFFMANN01` | A | Hoffmann, de Groot, Peng, Dries, Kater (2001) *Advantages and risks in increasing cyclone separator length*, AIChE J. 47(11):2452–2460 | abstract |
| `L-HOFFSTEIN` | B | Hoffmann & Stein — *Gas Cyclones and Swirl Tubes: Principles, Design and Operation* (2nd ed.) | book, not held |
| `L-XIANG01` | A | Xiang, Park, Lee — cone dimension effects, J. Aerosol Sci. / Particul. Sci. Technol. | abstract + `S-KARAGOZ13` §1 |
| `L-XIANG08` | A | Xiang & Lee (2008) *Effects of exit tube diameter on the flow field in cyclones*, Particul. Sci. Technol. 26:467–481 | abstract + `S-KARAGOZ13` §1 |
| `L-ZHAO04` | A | Zhao, Shen, Kang (2004) *Development of a symmetrical spiral inlet…*, Powder Technol. 145:47–50 | abstract |
| `L-OBERMAIR` | A | Obermair & Staudinger — dust outlet geometry study (5 configurations) | secondary |
| `L-MULTI19` | A | Muschelknautz, U. (2019) *Design criteria for multicyclones in a limited space*, Powder Technol. | abstract |
| `L-LIU14` | A | Liu et al. (2014) *Performance and flow behavior of four identical parallel cyclones*, Sep. Purif. Technol. | abstract |
| `L-BUCKLE25` | A | (2025) *Investigation of buckling and failure in thin-walled columns fabricated from PLA and PETG using FDM* | PMC12297988 |
| `L-THINWALL20` | A | *The impact of 3D printing parameters on the post-buckling behavior of thin-walled structures* | PMC7660314 |

## Secondary / engineering references

| Key | Tier | Source |
|---|---|---|
| `W-PPN-DESIGN` | C | powderprocess.net — *Cyclone design step by step* (Bohnet 1997 method + Koch & Licht table) |
| `W-PPN-LL` | C | powderprocess.net — *Design of a cyclone (Leith & Licht)* |
| `W-PSU` | C | Cimbala, J.M. — ME 405/433 Lapple cyclone lecture notes, Penn State |
| `W-ONEIDA` | C | Oneida Air Systems product data, Super Dust Deputy / SDD XL; patents US7282074, USD703401 |
| `W-WOODWEB` | C | WOODWEB knowledge base — duct velocity and CFM practice for wood shops |
| `W-NFPA` | C | NFPA 664 / NFPA 652, consolidated into NFPA 660 — combustible wood dust |
| `W-MDFDUST` | A | J. Wood Sci. (2020) 66:55 and (2022) — MDF dust morphology, sieve vs image analysis |
| `W-MDFEXP` | A | Occup. Environ. Med. pilot study — inhalable/respirable exposure, MDF vs softwood |
| `W-RIDGID` | C | RIDGID product data, WD0670/WD0671/WD06701 6-gallon family and HD0600 NXT replacement; WD0671EX spec listing (120 V, 5.8 A, 3.5 peak HP, 44 CFM, 1-7/8"×7 ft hose) |
| `W-BAMBU` | C | Bambu Lab P1S technical specs + Bambu Wiki *Print volume limitations* (256³ nominal, 250 mm default Z cap, 18×28 mm front-left exclusion) |
| `W-BUCKET` | C/D | Oneida FAQ *How do I prevent my bucket from collapsing…* + All-Clear collapse-proof bucket product data (≤40 % thicker wall, anti-static resin, latched reinforced lid); LumberJocks threads on bucket and lid collapse and DIY reinforcement |
| `W-VESSEL` | C/E | Candidate vessels considered: ATERET 5-gal black metal bucket w/ lever-lock lid (Amazon B0C78KQ6W6 — **gauge and dimensions not published**); 35-gal HDPE open-top drum with moulded lid + steel lever-locking ring (user photograph, 2026-07-29) |
| `W-HOSETEST` | D | Anemometer hose tests: Sawmill Creek *Real CFM measurements of various shop vac hoses* (14-gal RIDGID: 140/138/113/92 CFM by hose); woodgears.ca *Effect of hoses on dust collectors* (Wandel) |

## Retrieval notes

- `tandfonline.com`, `sciencedirect.com`, `oaktrust.library.tamu.edu` return HTTP 403 to automated
  fetch. Claims sourced from them here are via abstracts or independent secondary reproduction and
  are tiered accordingly.
- `WebFetch` cannot read PDFs. Use direct download + `pypdf` text extraction.
