---
doc_id: DKH-DDR-003
title: DockHub design for construction
project: DockHub
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** Draft. The changes in Table 1 were made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The items in Table 3 are Proposed, awaiting Amish.

## Context

On 2026-09-30 Amish asked for every repo's build plan to show how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of DockHub (DKH-DDR-001, DKH-DDR-002) showed what the station does with correct proportions, but it was a massing model: the cabinet was one closed box, many parts floated in the air with no fixing, some overlapped inside one part where the clash check could not see them, and some joints could not be reached to assemble.

The changes keep what DockHub does: the same 1,000 x 500 mm footprint and 1,500 mm cabinet, four bays at 196 mm pitch with bays 1 and 2 fitted, the SwapCell interface v0.3 cradle, receptacle and catch, the same pack, charger, controller, access, grid, fire and canopy parts, the same reach heights and the same canopy panel position and tilt. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now models 41 components one by one and runs a fit check (`python cad/src/model.py --check`): no two components overlap, in either the two-bay or the four-bay fit, and all 60 joints that must touch do touch.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The cabinet body was one hollow box with no joints, so it could not be made from sheet. | Six 1.5 mm galvanized panels: a laser-cut front panel and a back panel, each with 25 mm side flanges folded inward; two flat side panels outside those flanges; a floor pan with 25 mm flanges up and a roof with 40 mm flanges down, both inside the walls with corner reliefs. All joints are 4 mm blind rivets at about 100 mm pitch. | A sheet metal shop can cut and fold every panel, and two people can rivet them together from outside. No part depends on welding thin galvanized sheet. |
| P2 | The canopy posts stood on the 1.5 mm roof sheet. BOM line 1 named a roof frame but the model had none. Each front post pulls up with about 1.25 kN at a 30 m/s gust. | Two 40 x 40 x 4 mm angle beams, 494 mm long, under the roof on the post lines (460 mm each side of the centre). Each end carries a cleat of the same angle bolted to the beam with two M8 bolts and carrying two welded M8 nuts; bolts come in from outside through the front (or back) panel and the roof flange into those nuts. The posts bolt through the roof into the beams with two M10 bolts each. | Takes the uplift straight into the front and back panels and down to the plinth. Welded nuts mean no bolt has to be reached inside the closed cabinet. |
| P3 | The posts stopped 5 mm below the rails, the rails 2 mm below the panel, and nothing held the panel. | Posts welded to 50 x 100 x 8 mm base plates and to 50 x 70 x 6 mm cap plates cut to the 10° slope; rails sit on the cap plates on two M8 bolts each; rails lengthened from 1,054 to 1,174 mm so that four solar end clamps hold the panel frame's front and back edges. | Every canopy joint touches and is bolted. End clamps hold a bought panel without drilling its frame. The lowest canopy point over the walkway moves from 2.18 to 2.17 m (R13 still met). |
| P4 | The plenum wall was a 10 mm slab with no openings, so the liners' vent ports opened onto a solid wall. | A 1.5 mm folded wall with a 60 x 60 mm port behind each fitted bay, riveted to the bay deck's back flange, the side panels and the roof; its top corners are notched for the roof beams and sealed with fire-rated sealant. | Gas from a bay now reaches the plenum. Plenum section 1,366 cm². |
| P5 | Two 120 mm fans were drawn under an 80 mm deep louver with no hole in the roof; the louver was a solid block with slots cut through it. | Two 110 mm holes in the roof; square 120 mm fans hung under it on 4 mm spacers; a folded vent hood 850 x 133 x 70 mm over both holes, with twelve 50 x 40 mm slots in its back face, a rain lip, and flanges riveted and sealed to the roof. | Air and gas now have a path out, still to the back and up, away from the rider. Slot area 240 cm² (was 158 cm² of louver); air speed through it about 1.0 m/s [DKH-CAL-001 section 8]. |
| P6 | Bay doors 172 mm wide were hung 2 mm in front of 172 mm openings with no hinge, no gasket land and no lock. | Door openings narrowed to 150 mm. Doors 172 x 526 x 2 mm overlap the opening by 11 mm each side and 8 mm top and bottom, close on a 7 x 3 mm EPDM gasket, hang on a stainless piano hinge along the left edge, and carry a lock tongue that enters a 12 V solenoid lock screwed to the liner's right wall. | Leaves 24 mm between doors for the hinge knuckle and leaf. The pack (90 mm) still has 30 mm each side, and the handle top is 110 mm below the opening top. Reach heights are unchanged (R11). |
| P7 | The receptacle and the cradle occupied the same space (hidden because both were in one part); the side guides and catch post stood on nothing. | One printed cradle with its guides, a plug well on top and a receptacle pocket underneath; the receptacle screws into the pocket from below; the cradle stands on the liner floor on four M5 screws through liner floor and bay deck. The catch is on a folded 60 x 3 mm steel bracket that stands in a slot in the cradle and is screwed to the liner back wall. The cradle is printed in a flame-retardant (UL 94 V-0) filament. | Every part is held, and the receptacle sits where the pack's plug lands (interface v0.3 unchanged). A V-0 grade keeps the cradle from feeding a fire in the bay. |
| P8 | The bay liners, bay deck and charger rack floated with no fixing; the rack was a 10 mm plate. | Liners folded from 1.5 mm sheet with a 15 mm top flange riveted to the back of the front panel, the back riveted to the plenum wall round the port, the floor held by the cradle screws. Deck and charger shelf are 1.5 mm folded sheet with flanges riveted to the side panels and front panel. | Everything inside is fixed to the shell. The 16 mm gap between liners is kept. |
| P9 | The controller, MPPT and grid boxes floated 8 to 40 mm in front of the back panel; the aerosol unit and detector floated in the plenum. The grid box clashed with the new shelf flange. | The three boxes screw straight to the back panel with sealing washers; the grid box is 200 mm tall (was 210). The aerosol unit is held on its maker's two straps screwed to the back panel; the detector is screwed under the roof. | Every unit has a wall to fix to and none needs a new bracket. |
| P10 | The plinth was a solid 60 mm ring; the floor had no fixing to it; the anchor points were under the electrical boxes, where no tool could reach them once the cabinet was built. | A welded frame of 100 x 50 x 5 mm channel, flanges inward; eight M10 floor bolts through the floor pan and the top flange; anchors moved to 25 mm from the ends (still 30 mm from the front and back edges) and reached with a socket through four capped 40 mm holes in the floor. | A tool reaches every anchor nut with the cabinet complete. The wind calculation uses the front-to-back anchor spacing, which is unchanged. |
| P11 | The service opening was 960 mm wide, leaving no land for a hinge or gasket; the door floated; the filtered intake in BOM line 10 was not drawn. | Opening 900 x 500 mm; door 920 x 520 x 2 mm on a stainless piano hinge with a gasket and a cam lock whose arm turns behind the panel; a 400 x 80 mm intake slot with a filter pad behind it. | Room for hinge and gasket; the intake feeds the technical compartment and the plenum above it. |
| P12 | No order existed in which the roof frame could be bolted, because the cleat bolts would be inside a closed box. | Assembly order set in the build plan: shell, inside parts and front panel first; the roof is built as a sub-assembly with its beams, fans and detector and lowered in; cleat bolts go in from outside into welded nuts. | Every fixing can be reached when it is made. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | Two-bay prototype without packs 217 kg (was 205 kg); four bays with three packs 247 kg (was 234 kg) [DKH-CAL-001 section 10]. | Roof frame, post plates, hinges, clamps, catch brackets (9.6 kg) and the shelf and hood sheet. |
| Wind and anchors | Self-weight resists 0.53 kN·m (was 0.50) against 2.91 kN·m; front anchor design tension 3.79 kN (was 3.83) [section 11]. R15 stays at risk. | Higher mass. |
| Cost | BOM line 12 $60 to $70 (end clamps, post plates, bolts) and line 15 $30 to $35 (piano hinge): total $1,214 with two bays fitted (was $1,199) against the $1,200 value-engineering target (`budget_usd`), so R16 moves from at risk to **over the target by $14**. `budget_usd` is unchanged. All four bays $1,438. | Parts added for construction. Lines 1, 2, 3, 10, 14 and 16 were re-specified without a price change: the roof frame, door hinges, gaskets and fasteners were already in their scope. |
| Drawings | DKH-DWG-001 Rev P2; making sketches DKH-DWG-101 to 118 added. | Follows the model. |
| Documents | DKH-CAL-001 v0.4, DKH-PRC-001 v0.6, DKH-REQ-001 v0.6: mass, wind, vent path, canopy height, opening width, cost and R16 status updated; build plan DKH-BLD-001 and design decisions register DKH-DEC-001 added. | Follows the model. |
| Thermal, charging, throughput, grid, reach | Unchanged. | The cabinet, bays, packs and canopy keep their size and position. |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A2 | The bay doors now hang on piano hinges riveted to the outside of the front panel. A hinge pin on the outside can be attacked, which bears on R10 (security). | (a) stainless piano hinges with the pin ends peened over, as modelled; (b) concealed hinges inside the liner, which need a wider bay pitch or welded hinges. | (a) for the prototype; review after the first site visit. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan DKH-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Cost is reported against the value-engineering target: USD 1,200 (a hypothetical control target, not a limit) against an estimated USD 1,214 for the constructable design, USD 14 over; the register lists cost drivers and savings worth trying.
- Requirement status: two not met (R6, R9), one over its value-engineering target (R16), two at risk (R8, R15), two not verifiable at TRL 3 (R7, R14), nine met (DKH-CAL-001 v0.4).
- The photoreal renders (`media/render-*.png`, made on Amish's Mac), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept: 172 mm door openings, no hinges, a louver block instead of the hood. They need updating on Amish's Mac, where Blender is. The appearance model's own door windows remain the separate open item from the 2026-09-26 session.
- The bought parts (chargers, boxes, locks, receptacle, fans, aerosol unit, panel) are chosen at TRL 4; their sizes and fixings must be checked against the model then (design decisions register, "To confirm when parts are bought").
