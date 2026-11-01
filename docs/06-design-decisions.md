---
doc_id: DKH-DEC-001
title: DockHub design decisions register
project: DockHub
doc_type: Design decisions register
version: "0.5"
status: Draft
date: '2026-10-31'
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
  - version: "0.4"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Approved follow-ups carried out: anchors and pad chosen (To confirm item 9 now the anchor rating only); value engineering restated with them"
  - version: "0.5"
    date: '2026-10-31'
    author: Amish Chadha
    change: "Kit 1.9.1 upgrade: concept selection proposed (DKH-DDR-004, awaiting Amish); STEM check fix D1 decided under the standing instruction of 2026-10-23; the model rebuilt to the kit 1.9 interface with no change to any design dimension"
---

# DockHub design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision | Options | Recommendation | Record |
| --- | --- | --- | --- | --- |
| O1 | Concept: which working principle to carry | A swap bays (120 of 155), B rotary magazine (102), C locker bank (90) | A, current design, 15 % ahead of B. **Proposed, awaiting Amish** | DKH-DDR-004, DKH-OPT-001 |
| O2 | Whether to accept the three STEM rows still open on the fire side (S11 propagation, S13 retention, S23 fumes, S29 gas build-up) as TRL 4 trial items | Accept as trial items or fund a bench test earlier | Accept; they cannot close on paper. **Proposed, awaiting Amish** | DKH-STM-001 |
| O3 | Budget: the design is $319 over the $1,200 target | Keep as a target; drop the pad where the host has a slab; fit two bays only | Keep as a target and review at supplier selection. **Proposed, awaiting Amish** | DKH-FEA-001 |
| O4 | Fire vent trade-off of D1: with the fans stopped on aerosol discharge, unburnt gas can collect in the plenum (STEM S29) | Keep D1 as made; fans off for a fixed hold then restarted; or leave the fans running and drop the aerosol unit | Fans off for a hold time set by the retention test, then restarted; an explosion-venting area to be calculated. **Proposed, awaiting Amish** | DKH-STM-001 S13, S29 |
| O5 | Anchor rating: the independent review gets 4.13 kN design tension, not 3.79 kN, when the 1.5 and 0.9 factors are applied to the anchors | Ask for 3.8 kN as now; ask for 4.2 kN | Ask for 4.2 kN when buying; BOM line 17 text unchanged until Amish decides. **Proposed, awaiting Amish** | DKH-STM-001 S16 |
| O6 | Solar share definition: 9.3 % at the pack terminals, 8.7 % at the inputs | Keep the pack-terminal basis; use the input basis | Keep the pack-terminal basis and state it. **Proposed, awaiting Amish** | DKH-PRS-001 PR-006 |

No decision from 2026-10-02 is reopened.

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
| 9 | The chosen M12 stainless wedge anchors (BOM line 17) have an approval giving a design tension resistance of at least 3.8 kN at 100 mm embedment in C25/30 concrete, 225 mm from the pad edge | R15 is met on paper with the anchors and the cast pad (BOM line 18) chosen on 2026-10-02; the anchor rating is the remaining check | DKH-CAL-001 section 11 |

## Value engineering

Value-engineering target: USD 1,200. Estimated cost of the constructable design: USD 1,519 (USD 319 over the target). The target is a hypothetical control target, not a limit, for the four-bay cabinet with two bays fitted and SwapCell packs excluded. The estimate now includes the anchors and cast site pad chosen on 2026-10-02 (lines 17 and 18, USD 305); without them it is USD 1,214. All four bays fitted cost an estimated USD 1,743; each further bay adds USD 112. The vermiculite floor tray (line 19, about USD 11 a bay) is a trial option and is not in the estimate.

Main cost drivers: the site pad (line 18, USD 265: 28 bags of premixed concrete, mesh, formwork and gravel), then the parts added to make the design buildable, which took the estimate from USD 1,199 to USD 1,214 (canopy end clamps, post plates and bolts, line 12, USD 60 to USD 70; service door hinge, line 15, USD 30 to USD 35), and the anchors (line 17, USD 40). All prices are indicative.

Savings worth trying: using the host's own slab instead of the cast pad where an engineer confirms it does the same job (up to USD 265); ready-mixed concrete instead of bags if the supplier delivers a small load; recovering the USD 14 of construction parts at supplier selection.

## Decisions made under the standing instruction

Amish, 2026-10-23: when a STEM check row fails, propose and implement the best fix in the same session and record it as decided under that instruction. A fix that changes the working principle, pitch or scope goes to Amish instead.

| # | Date | Decision | Decided by | Record |
| --- | --- | --- | --- | --- |
| D1 | 2026-10-31 | STEM row S13: the roof fans ran on an alarm and would have swept out the condensed-aerosol agent. Fix: on aerosol discharge the controller stops both fans and the plenum vents through the passive hood slot (240 cm2); the fans restart only on a technician's reset. No part, price or dimension changes (new requirement PR-017) | Amish's standing instruction of 2026-10-23, applied in the kit 1.9.1 session; he can reverse it | DKH-STM-001 |
| D2 | 2026-10-31 | Kit 1.9 model rebuild: `cad/src/model.py` rewritten to the kit 1.9 interface (D3, every option); every design dimension and BOM price kept. Dimension changes: none (the model weighs 234.5 kg for the two-bay prototype without packs, the pad or anchors, against the 217 kg estimate in DKH-CAL-001; the extra self-weight helps the wind case, so the calculation stays). BOM line 12 wording now describes the end clamps and stitch welds as modelled; no price change. Repo helpers in `cad/src/dkh_parts.py` | Brief for the kit 1.9.1 upgrade | DKH-OPT-001 |

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
