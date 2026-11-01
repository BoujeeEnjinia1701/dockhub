---
doc_id: DKH-PLN-001
title: DockHub project plan
project: DockHub
doc_type: Project plan
version: "0.1"
status: Draft
date: 2026-10-31
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-31
    author: Amish Chadha
    change: First plan at the kit 1.9.1 upgrade; stages P0 to P3 done on paper, P4 to P6 on hold under the stage cap
---

# DockHub project plan

DockHub is at stage P3 (design outputs), TRL 3. The current design is option A; the concept choice is proposed, awaiting Amish (DKH-DDR-004). The calculation note, the D3 model of all three options, the drawings, the priced BOM and the build plan are done. The next gate, P4 (verification, TRL 4), is on hold while the portfolio stage cap is P3 (`.kit/PHASE.yaml`). Method: STANDARDS section 19.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Concept choice | Amish Chadha | DKH-DDR-004, DKH-OPT-001 | Proposed, awaiting Amish |
| Partner and site | Amish Chadha | A delivery-worker group, New York City first, on private property (DKH-DEC-001) | Not started |
| Requirements | Design lead | DKH-URS-001, DKH-PRS-001, DKH-RTM-001 | Done on paper; partner review pending |
| Calculations and model | Design lead | DKH-CAL-001; D3 model of options A, B and C; STEP and STL | Done 2026-10-31 |
| Drawings, BOM, build plan | Design lead | DKH-DWG-001, DWG-101 onward, bom/bom.csv, DKH-BLD-001 | Done |
| Risk, market, regulatory | Design lead | DKH-RSK-001 with design FMEA, DKH-MKT-001, DKH-REG-001 | Done 2026-10-31 |
| Renders | Coordinator | Options picture (Blender), product renders | Options picture to render by the coordinator |
| Verification (P4) | Partner workshop | Propagation trial, detector timing, IP54 test, build | On hold (stage cap P3) |

## Resources needed

Table 2. Resources.

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Design lead (Claude with Amish's review) | P1 to P3 documents | Sessions done | 0 |
| Prototype parts | Two-bay cabinet with anchors and pad (P4, on hold) | | 1,519 (bom/bom.csv; target 1,200) |
| SwapCell packs | One resident pack for the prototype | | 414 each (SwapCell BOM, not in the cabinet cost) |
| Sheet metal shop and electrician | Cabinet and mains connection | | To assess |
| Fire certification route | UL 1487 test and FDNY approval (DKH-REG-001 G1, G2) | | To assess; FDNY lists a USD 625 application fee |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB, STM, OPT, REG, FEA, PLN | Done 2026-10-31 |
| P1 Definition | URS, PRS, RSK, MKT, REG complete | Done 2026-10-31 |
| P2 Design inputs | PRS targets, CAL, RTM, DDR, STEM check closed by calculation | Done 2026-10-31; ten STEM rows need hardware |
| P3 Design outputs | Model (D3), STEP, DWG, BOM, BLD, DEC, FMEA | Done 2026-10-31 |
| P4 Verification | Propagation trial, detector timing, enclosure test, charge pause on a hot day | On hold |
| P5 to P6 | Pilot with a partner, launch | On hold |

## Next steps and decision requested

Requested from Amish: the concept choice (DKH-DDR-004, option A recommended), whether to keep the USD 1,200 target against a USD 1,519 estimate, and whether the fire rows S11, S13 and S23 may stay open as TRL 4 trial items. The recommended next step is a partner and, when the cap allows, TRL 4: the propagation trial with plain and vermiculite bay floors.

## References

Gogoro. "Gogoro Network Flex Plan." September 19, 2019. https://www.gogoro.com/news/gogoro-network-flex-plan/.

CleanTechnica. "Battery Swapping Expands In New York City." February 28, 2026. https://cleantechnica.com/2026/02/28/battery-swapping-expands-in-new-york-city/.

FDNY. *E-Micromobility Approval Guide.* Accessed October 31, 2026. https://www.nyc.gov/assets/fdny/downloads/pdf/business/e-micromobility-approval-guide.pdf.

Levy Electric. "Swobbee Battery Swapping Station" and "Gogoro GoStation." Accessed October 31, 2026. https://fleets.levyelectric.com/docking-stations/swobbee-battery-swapping-station; https://fleets.levyelectric.com/docking-stations/gogoro-gostation.

NYC Department of Transportation. Press release, November 18, 2025. https://www.nyc.gov/html/dot/html/pr2025/install-public-e-bike-battery-swapping-network-citywide.shtml.

US Access Board. "Chapter 3: Operable Parts." Accessed October 31, 2026. https://www.access-board.gov/ada/guides/chapter-3-operable-parts/.
