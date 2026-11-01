---
doc_id: DKH-FEA-001
title: DockHub feasibility assessment
project: DockHub
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: 2026-10-31
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-31
    author: Amish Chadha
    change: First feasibility assessment at the kit 1.9.1 upgrade, for the current design (option A) at TRL 3
---

# DockHub feasibility assessment

**Closed at TRL 3: feasible on paper, with three risks that only hardware can retire.** The calculation note (DKH-CAL-001) shows 11 of 16 original requirements met, a 31 s swap, 1.25 kW peak grid draw and a station that stays upright in a 30 m/s gust. The cabinet is built from folded sheet steel, off-the-shelf certified chargers and hobby-grade controllers, and the model (cad/src/model.py, D3) has 537 parts that fit with no interference. What remains unproven is fire containment (PR-008), charging on hot days (PR-009) and cost: the parts come to USD 1,519 against the USD 1,200 target. Method: STANDARDS section 19.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | Four bays in one riveted cabinet, a compartment, cradle, receptacle, charger and CAN channel each; 31 s swap; 36 swaps a day ceiling; 234.5 kg for the two-bay prototype in the model | High | Two bays serve only 9 of the 20 daily swaps; the four-bay fit is needed for the duty case | DKH-STM-001 S1 to S8; DKH-CAL-001 s2 to s6 |
| Materials | 1.5 mm galvanized steel sheet, stainless hinges and anchors, EPDM gaskets, a printable flame-retardant cradle | High | Cradle filament rated UL 94 V-0 to confirm; coating life in road salt (S19) | DKH-STM-001 S19; DKH-DEC-001 to-confirm item 8 |
| Manufacturing and assembly | Laser-cut and folded panels, blind rivets, a welded channel plinth, bolted canopy; build plan with 12 stages | Medium | Needs a sheet metal shop and a welder; tolerances at the folds to confirm | DKH-BLD-001 (docs/05-build-plan.md); cad/src/model.py |
| Power and controls | One 120 V 15 A or 230 V 10 A circuit; four chargers with power factor 0.9 or better; a controller with a CAN channel per bay | Medium | At 120 V the draw is 11.0 A with PFC chargers, 17.2 A without: the chargers must have PFC | DKH-CAL-001 s6; DKH-STM-001 S3 |
| Safety | Detector, condensed aerosol, steel compartments, vent plenum and hood | Low | Runaway propagation cannot be excluded on paper (S11); aerosol retention (S13); fumes at the door (S23) | DKH-STM-001 S11, S13, S23; DKH-RSK-001 |
| Supply of parts | Certified chargers, a controller, a 400 W panel and the SwapCell pack are bought; sheet and plinth from a local shop | Medium | The pack is the SwapCell project's (USD 414 each, not in the cost); charger PFC and footprint to confirm | bom/bom.csv; DKH-DEC-001 to-confirm items 1 to 9 |
| Cost | USD 1,519 with anchors and pad, USD 1,214 without, USD 1,743 with all four bays | Low | Over the target by USD 319 (PR-016); the hypothetical control target is Amish's to keep or move | bom/bom.csv; DKH-CAL-001 s12 |
| Site and permits | Private forecourt with a single-phase circuit; a pad and anchors; fire review | Medium | A public sidewalk needs consent, a Certificate of Approval route that treats a swap cabinet as a charging cabinet is unconfirmed | DKH-REG-001 G1, G4, G5 |
| Market | Open, owner-run swap cabinets for a delivery workforce that has few safe places to charge; operators exist | Medium | A closed incumbent network may crowd out an open one; pack supply depends on SwapCell | DKH-MKT-001 |

Ratings: High, Medium, Low.
