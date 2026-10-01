---
doc_id: DKH-DEC-001
title: DockHub design decisions register
project: DockHub
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions from the review note, the decision records and the build plan work
---

# DockHub design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design for construction | Accept the changes P1 to P12 as made, or ask for changes | Accept | The whole build plan | DKH-DDR-003, Table 1 |
| 2 | R16 not met: $1,214 against the $1,200 budget | (a) raise `budget_usd` to $1,250; (b) keep $1,200 and recover $14 at supplier selection; (c) keep $1,200 and accept R16 as not met until parts are priced | (a) | Purchasing at TRL 4 | DKH-DDR-003, A1 |
| 3 | Bay door hinges on the outside of the front panel (R10) | (a) stainless piano hinges with peened pins, as modelled; (b) concealed hinges, needing a wider bay pitch or welded hinges | (a) for the prototype | Bay doors (build plan section 3.15, step 17) | DKH-DDR-003, A2 |
| 4 | How to close R6 (9.3 % solar against 10 %) | Accept about 9 %; route flat packs to bay 1 in daylight and accept occasional waits; feed more bays from the sun; drop the target | None yet | Controller logic and MPPT wiring; not the cabinet build | DKH-DDR-002, Table 2 |
| 5 | How to close R9 (charging pauses above about 29 to 39 °C ambient) | Accept daytime pauses in hot climates; add active cooling; narrow the design ambient; raise the charge limit with SwapCell | None yet | Fans and vent hood if cooling is added | DKH-DDR-002, Table 2 |
| 6 | Pack ownership model | Station-owned pool, rider-owned one-for-one exchange, fleet packs | None yet; to follow co-design | Not part of the build | DKH-DDR-001 item 10 |
| 7 | First pilot site and partner | A delivery-worker group in a high-income city, or a moto-taxi hub in East Africa | None yet | Siting, supply and anchoring (safety stop S7) | DKH-DDR-001 item 11 |
| 8 | Propagation test and standard for R8 | Which lithium-ion propagation test a later version aims for, and whether a workshop-built cabinet can pass it | None yet | Liners, plenum and fire unit at TRL 4 and later | DKH-PRC-001, Open questions |
| 9 | Fire suppression | Keep the condensed-aerosol unit, or use sand or vermiculite-filled bay floors and a sealed, vented compartment | None yet | Fire unit (build plan step 5) | DKH-PRC-001, Open questions |
| 10 | Siting permissions and electrical supply host in the first pilot city | To be found with the pilot partner | None yet | Safety stops S2 and S7 | DKH-PRC-001, Open questions |
| 11 | Riders who do not want to share identity | Anonymous prepaid cards or another token | None yet | Access panel software only | DKH-PRC-001, Open questions |
| 12 | Product renders: clear windows in the bay doors | Render-only windows with solid steel doors in the build, or fire-rated glazing priced against R16 | Solid steel doors in the build; windows render-only | None (the build plan has solid doors) | Review note, 2026-09-26, item 1 |
| 13 | Product renders: scene state, header sign and markings, four-bay fit caption | Accept as render choices | Accept; settle sign wording with branding | None | Review note, 2026-09-26, items 2, 3 and 5 |
| 14 | Update the photoreal renders, card and social preview to the constructable design | Re-render on Amish's Mac after decision 1 | Re-render after decision 1 | None | DKH-DDR-003, Consequences |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | Charger footprint and fixing holes, and that its power factor is 0.9 or better | The shelf holes are marked from the charger; R5 holds only with power-factor-corrected chargers | DKH-CAL-001 section 6; BOM line 5 |
| 2 | Controller, MPPT and grid box sizes (no larger than 220 x 100 x 190, 150 x 70 x 180 and 220 x 92 x 200 mm) | They must fit between the floor flange and the shelf flange on the back panel | DKH-DDR-003, P9 |
| 3 | Solenoid lock size (about 30 x 30 x 50 mm) and bolt throw | The tongue position on the door is set from it | DKH-DDR-003, P6 |
| 4 | SwapCell v0.3 receptacle flange and fixing | The cradle's 72 x 50 x 9 mm pocket and its two M3 inserts are set from it | DKH-DDR-003, P7 |
| 5 | Fans 120 x 120 x 25 mm with corner holes on a 105 mm square | The roof holes and spacer positions are set from them | DKH-DDR-003, P5 |
| 6 | Aerosol unit size (about 76 x 420 mm) and its straps | Its position under the roof line, clear of the fans and beams | DKH-DDR-003, P9 |
| 7 | Solar panel size, frame depth (35 mm) and that the maker allows end clamps | The rail length and clamps are set from it | DKH-DDR-003, P3 |
| 8 | A printable flame-retardant filament rated UL 94 V-0 | The cradle material | DKH-DDR-003, P7 |
| 9 | Anchors with a design tension of at least 3.8 kN in the host concrete, and the pad | R15 stays at risk until they are chosen; not in the BOM | DKH-CAL-001 section 11 |

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items with a recommendation: four-bay cabinet with bays 1 and 2 fitted and `budget_usd` $1,200 for that fit; 400 W canopy kept and R6 relaxed to 10 %; four bays in one row; one charger and CAN channel per bay; steel compartment per bay with a rear plenum; doors locked during a fire alarm; MPPT to bay 1; offline-first NFC access; 70 % health gate | Amish: "i accept all your recommendations, go with them across all repos." | DKH-DDR-001, DKH-DDR-002 |
| 2026-09-25 | TRL 3 engineering proposals: build to SwapCell interface v0.3; release packs at 80 % state of charge or more; chargers with a power factor of 0.9 or better; plinth flush with the body; 15 min rider patience and the demand profile of DKH-CAL-001; two-bay first prototype that cannot run the duty case | Amish, same instruction | DKH-DDR-001 items 12 and 13, DKH-DDR-002 |
| 2026-09-30 | Make each design physically buildable while drawing the build plan, recording every change | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The resulting changes are open (decision 1) | DKH-DDR-003 |
| 2026-09-30 | Outstanding decisions are kept in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it." | STANDARDS section 18 |
