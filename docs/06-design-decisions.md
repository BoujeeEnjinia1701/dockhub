---
doc_id: DKH-DEC-001
title: DockHub design decisions register
project: DockHub
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions from the review note, the decision records and the build plan work
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Amish approved the recommendations for open decisions 1 to 13 (DKH-DDR-003 accepted); moved to decisions made"
---

# DockHub design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

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
| 9 | Anchors with a design tension of at least 3.8 kN in the host concrete, and the pad | R15 stays at risk until they are chosen; not in the BOM. The first pilot is on private property (decided 2026-10-02), so the host's ground sets the pad | DKH-CAL-001 section 11 |

## Value engineering

Value-engineering target: USD 1,200 (a hypothetical control target, not a limit), for the four-bay cabinet with two bays fitted and SwapCell packs excluded. Estimated cost of the constructable design: USD 1,214 (USD 14 over the target). All four bays fitted cost an estimated USD 1,438; each further bay adds USD 112.

Main cost drivers: the parts added to make the design buildable took the estimate from USD 1,199 to USD 1,214, namely the canopy end clamps, post plates and bolts (line 12, USD 60 to USD 70) and the service door hinge (line 15, USD 30 to USD 35). All prices are indicative.

Savings worth trying: recovering the USD 14 at supplier selection.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items with a recommendation: four-bay cabinet with bays 1 and 2 fitted and a $1,200 value-engineering target (`budget_usd`) for that fit; 400 W canopy kept and R6 relaxed to 10 %; four bays in one row; one charger and CAN channel per bay; steel compartment per bay with a rear plenum; doors locked during a fire alarm; MPPT to bay 1; offline-first NFC access; 70 % health gate | Amish: "i accept all your recommendations, go with them across all repos." | DKH-DDR-001, DKH-DDR-002 |
| 2026-09-25 | TRL 3 engineering proposals: build to SwapCell interface v0.3; release packs at 80 % state of charge or more; chargers with a power factor of 0.9 or better; plinth flush with the body; 15 min rider patience and the demand profile of DKH-CAL-001; two-bay first prototype that cannot run the duty case | Amish, same instruction | DKH-DDR-001 items 12 and 13, DKH-DDR-002 |
| 2026-09-30 | Make each design physically buildable while drawing the build plan, recording every change | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The resulting changes were accepted on 2026-10-02 (below) | DKH-DDR-003 |
| 2026-09-30 | Outstanding decisions are kept in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it." | STANDARDS section 18 |
| 2026-10-02 | Design for construction accepted: the changes P1 to P12 and their knock-on changes, as made | Amish: "i approve your recommendations for all 555 open decisions." | DKH-DDR-003, Table 1 |
| 2026-10-02 | Bay door hinges: stainless piano hinges with the pin ends peened over (option a) for the prototype; reviewed after the first site visit | Amish: "i approve your recommendations for all 555 open decisions." | DKH-DDR-003, A2 |
| 2026-10-02 | R6 restated as about 9 % of charging energy, with normal routing kept; switching the solar charger to whichever bay holds the flattest pack is to be tried as a TRL 4 controller change, not a cabinet change | Amish: "i approve your recommendations for all 555 open decisions." | DKH-DDR-002, Table 2 |
| 2026-10-02 | R9: keep the pack's 45 °C charge limit and accept daytime charging pauses; R9's charging range restated as full-rate charging up to about 30 °C ambient, with the cold-soak limit near -1 °C stated; the first pilot site is chosen with summer highs near that; active cooling revisited only for a hot-climate site | Amish: "i approve your recommendations for all 555 open decisions." | DKH-DDR-002, Table 2 |
| 2026-10-02 | Pack ownership: a station-owned pool of packs exchanged one for one, as the concept and R10 assume; to be confirmed in co-design | Amish: "i approve your recommendations for all 555 open decisions." | DKH-DDR-001 item 10 |
| 2026-10-02 | First pilot partner: a delivery-worker group in a high-income city, with New York City first and Los Deliveristas Unidos (Workers Justice Project) as the first candidate partner to approach | Amish: "i approve your recommendations for all 555 open decisions." | DKH-DDR-001 item 11 |
| 2026-10-02 | Propagation test for R8: a later version aims at a UL 9540A unit-level propagation test, with a heater-triggered runaway in one bay at an outdoor test site first, before paying an accredited lab | Amish: "i approve your recommendations for all 555 open decisions." | DKH-PRC-001, Open questions |
| 2026-10-02 | Fire suppression: keep the condensed-aerosol unit for the first prototype and test vermiculite-filled bay floors as a variant in the propagation trial; choose on the result | Amish: "i approve your recommendations for all 555 open decisions." | DKH-PRC-001, Open questions |
| 2026-10-02 | Siting: the first pilot on private property with an existing single-phase circuit (the partner's own premises or a willing business frontage), not on a public sidewalk; a city sidewalk permit is sought only for a second site | Amish: "i approve your recommendations for all 555 open decisions." | DKH-PRC-001, Open questions |
| 2026-10-02 | Riders who do not want to share identity: anonymous prepaid NFC cards sold by the partner, each carrying a pack deposit, alongside named tokens | Amish: "i approve your recommendations for all 555 open decisions." | DKH-PRC-001, Open questions |
| 2026-10-02 | Product renders: solid steel doors in the build; the clear windows are shown in the renders only | Amish: "i approve your recommendations for all 555 open decisions." | Review note, 2026-09-26, item 1 |
| 2026-10-02 | Product renders: scene state, header sign and markings accepted as render choices; renders captioned 'four-bay fit shown'; sign wording settled with branding | Amish: "i approve your recommendations for all 555 open decisions." | Review note, 2026-09-26, items 2, 3 and 5 |
| 2026-10-02 | Re-render the photoreal renders, card and social preview on Amish's Mac to the constructable design, now that decisions 1 and 2 are made | Amish: "i approve your recommendations for all 555 open decisions." | DKH-DDR-003, Consequences |
