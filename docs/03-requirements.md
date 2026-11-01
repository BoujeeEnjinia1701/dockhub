---
doc_id: DKH-PRS-001
title: DockHub product requirements and specifications
project: DockHub
doc_type: Product requirements and specifications
version: '0.9'
status: Draft
date: '2026-10-31'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: '0.1'
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: '0.2'
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2
- version: '0.3'
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. R6 relaxed to 10 % and R16 redefined to the two-bay fit (DKH-DDR-001); R2 to SwapCell interface v0.3; status from DKH-CAL-001
- version: '0.4'
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: '0.5'
  date: '2026-10-01'
  author: Amish Chadha
  change: Status from DKH-CAL-001 v0.3 after the constructable design (DKH-DDR-003); R16 not met
- version: '0.6'
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: '0.7'
  date: '2026-10-02'
  author: Amish Chadha
  change: R6 restated as about 9 % and R9 as full-rate charging up to about 30 °C ambient (DKH-DEC-001); status updated
- version: '0.8'
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Status from DKH-CAL-001 v0.6 after the approved follow-ups: R15 met with the anchors and site pad chosen; R16 USD 1,519 with them; R12 token list with anonymous prepaid cards'
- version: '0.9'
  date: '2026-10-31'
  author: Amish Chadha
  change: 'Migrated at the kit 1.9.1 upgrade: R1 to R16 became PR-001 to PR-016 in the PRS columns with a Was column, every PR traced to a user requirement in DKH-URS-001; PR-017 added for the aerosol fan rule (DKH-DEC-001 D1); targets, wording and status unchanged'
---

# DockHub product requirements and specifications

What the station must do, each requirement traced to a user need in DKH-URS-001 (links in DKH-RTM-001). The requirements describe option A, swap bays in a steel cabinet, the current design, which is carried forward unchanged; the concept options are scored in DKH-OPT-001 and the choice is proposed, awaiting Amish. They were numbered R1 to R16 before kit 1.8; the **Was** column keeps the old numbers, which the calculation note (DKH-CAL-001) and the build plan still use. They are checked by calculation in DKH-CAL-001 (TRL 3) and are not yet validated with riders, hosts or a city (DKH-PRB-001). On 2026-09-25 Amish accepted the review recommendations (DKH-DDR-001, DKH-DDR-002): PR-006 relaxed from 20 % to 10 %, PR-016 covers the four-bay cabinet with two bays fitted, and PR-002 cites SwapCell interface v0.3. On 2026-10-02 Amish restated PR-006 as about 9 % and PR-009 as full-rate charging up to about 30 C ambient (DKH-DEC-001).

**On paper, 12 of 17 are met or met by design, with qualifications from the independent review (PR-005, PR-006, PR-009, PR-015, PR-017).** PR-016 (cost) is over its value-engineering target; PR-008 (fire containment) and PR-009 (climate) are at risk; PR-007 (fire detection) and PR-014 (maintainability) cannot be verified until hardware exists. The STEM check (DKH-STM-001) adds PR-017.

The **design duty case** used throughout is 20 swaps a day, each returning a SwapCell pack at about 15 % state of charge, in a street location with 4.5 peak sun hours and ambient air between -10 and 45 C. Because a swap needs an empty bay, a station with *n* bays holds *n* - 1 packs.

Table 1. Product requirements and specifications. Status at TRL 3 from DKH-CAL-001 (python docs/04-calcs/sizing.py).

| ID | Was | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | R1 | UR-001 | Performance | Fast swap | 60 s or less from tapping the reader to closing the second door, for a rider familiar with the station | 60 | max | s | Task analysis; later timed trials with riders | Met (31 s) |
| PR-002 | R2 | UR-005 | Interface | SwapCell compatibility | Every bay builds to SwapCell interface v0.3: envelope, guide faces, blind-mate receptacle with the 10 kΩ INTERLOCK coding resistor, class D catch, CAN heartbeat and message set; no change to the interface | v0.3 | exact | n/a | Interface review with the SwapCell project | Met by design review; one CAN channel per bay |
| PR-003 | R3 | UR-002 | Performance | Charge speed | 20 to 80 % in 1.5 h or less; full charge in 2.5 h or less, per bay, at 25 °C | 1.5 (20 to 80 %); 2.5 (full) | max | h | Charge profile calculation | Met (1.2 h and 2.3 h) |
| PR-004 | R4 | UR-002 | Performance | Throughput | 20 or more swaps a day from 4 bays at the design duty case | 20 | min | swaps a day | Day model with a demand profile | Met by the four-bay fit (20 of 20 served, longest wait 4 min; ceiling 36 a day). The two-bay first prototype serves 9 of 20 |
| PR-005 | R5 | UR-009 | Logistics | Grid supply | One single-phase branch circuit (120 V 15 A or 230 V 10 A); peak draw 1.5 kW or less | 1.5 | max | kW | Load calculation | Met (1.25 kW; 11.0 A at 120 V) with chargers of power factor 0.9 or better Independent review (DKH-STM-001): at 10 % low mains voltage constant-power chargers draw 12.2 A at 120 V, over the 12 A continuous limit if all four run; the simulated day runs at most 3 (8.3 A); low-voltage case to add to DKH-CAL-001 |
| PR-006 | R6 | UR-013 | Performance | Solar contribution | Canopy solar supplies about 9 % of daily charging energy at the design duty case, with normal routing (restated on 2026-10-02, DKH-DEC-001; relaxed from 20 % to 10 % by DKH-DDR-001) | 9 | about | % of charging energy | Day model | Met on paper, thin margin (9.3 %; 11.4 % if flat packs are routed to bay 1 in daylight, which turns one rider in 20 away, so normal routing is kept; 16.1 % if the solar output is later switched to the flattest pack, a TRL 4 trial) Basis: 9.3 % is measured at the pack terminals; at the inputs (0.77 kWh panel against 8.04 kWh grid to chargers) it is 8.7 %, on one clear design day; the definition is proposed, awaiting Amish (DKH-DEC-001 O6) |
| PR-007 | R7 | UR-003 | Safety | Fire detection and response | Detect a pack or bay over 60 °C, or smoke, within 10 s; open that bay's charge contactor within 1 s of detection; sound a local alarm and send a remote alert; vent gas to the rear roof louver, away from the user side | 10 detect; 1 contactor | max | s | Latency budget; later bench test with a heat source | Not verifiable at TRL 3 (electronic latency 3.1 s, contactor 0.15 s) |
| PR-008 | R8 | UR-003 | Safety | Fire containment | A thermal runaway in one bay does not spread to a neighboring bay or pack for 30 min or more, and flame does not leave the cabinet front | 30 | min | min | Later propagation test by an accredited lab | **At risk**; not verifiable at TRL 3 |
| PR-009 | R9 | UR-004 | Environment and durability | Climate | Enclosure IP54 or better; operate (store and swap) at -10 to 45 °C ambient; full-rate charging up to about 30 °C ambient, with daytime pauses accepted above it and no charging start for cold-soaked packs below about -1 °C; never charge a pack outside the pack's reported charge temperature window (restated on 2026-10-02, DKH-DEC-001) | IP54; -10 to 45; 30 | min IP; range; about | code; C; C | Thermal calculation; later chamber test | **At risk**: uninterrupted charging needs ambient below about 29 to 39 °C (pack charge limit 45 °C), so the warmest bay may pause just under 30 °C; cold-soaked packs cannot start below about -1 °C, as now stated IP54 is not demonstrated: the vent slots and filtered intake make it doubtful until an enclosure test (STEM S27); the lowest calculated limit for uninterrupted charging is 29.4 C (S9) |
| PR-010 | R10 | UR-007 | Security | Security | 1.5 mm or thicker steel; fail-secure bay locks; cabinet anchored to its pad with tamper-resistant fixings; a pack is released only against a valid token and a returned pack | 1.5 | min | mm | Design review | Met by design review |
| PR-011 | R11 | UR-008 | Usability | Accessibility and use | All operable parts (reader, buttons, bay handles) 0.38 to 1.22 m (15 to 48 in) above the ground; status shown by light and symbol as well as text; usable with gloves and at night | 0.38 to 1.22 | range | m | Model check; later user trials | Met (0.73 to 1.10 m) |
| PR-012 | R12 | UR-010 | Privacy | Privacy and data | No cameras or microphones; logs hold pack ID, bay, time, energy and state of health, with the rider as an opaque token; operates offline for 24 h or more and syncs later | 0 cameras; 24 | min | h offline | Design review | Met by design review (token list of 200 kB, including anonymous prepaid cards with a pack deposit) |
| PR-013 | R13 | UR-009 | Logistics | Sidewalk footprint | Cabinet footprint 1.0 x 0.6 m or less; canopy underside 2.1 m or more above the sidewalk | 1.0 x 0.6; 2.1 | max; min | m; m | Model check | Met (1.0 x 0.5 m with a flush plinth; lowest canopy point over the sidewalk 2.17 m) |
| PR-014 | R14 | UR-011 | Maintenance | Maintainability | Any charger, lock, bay cradle or controller replaced in 15 min or less by one technician with hand tools, through the service door | 15 | max | min | Design review; later timed trial | Not verifiable at TRL 3 |
| PR-015 | R15 | UR-006 | Safety | Wind and anchoring | Stays upright and intact at a 30 m/s gust with the canopy fitted | 30 | min | m/s gust | Wind load calculation | Met on paper: four M12 stainless wedge anchors (3.8 kN design tension each) into a 1,400 x 1,100 x 300 mm cast pad of about 1,109 kg; equilibrium factor 1.12 at a 30 m/s gust. The anchor rating is confirmed from the maker's data when bought Upright only; STEM S16 is plausible (6 % margin; anchor design tension 4.13 kN with matching factors, proposed 4.2 kN, DKH-DEC-001 O5). The canopy being intact (panel clamps, roof pull-through at 1,251 N per post) and wind from other directions are not yet checked |
| PR-016 | R16 | UR-012 | Cost | Cost | Parts 1,200 USD or less for the four-bay cabinet with two bays fitted (first prototype), SwapCell packs excluded (redefined, DKH-DDR-001) | 1,200 | max | USD | Priced BOM (`bom/bom.csv`) | **Over the value-engineering target by $319** ($1,519 against $1,200: $1,214 for the buildable cabinet, DKH-DDR-003, plus $305 for the anchors and site pad chosen on 2026-10-02; $1,743 with all four bays fitted) |
| PR-017 | new | UR-003 | Safety | Aerosol is kept in | On a condensed-aerosol discharge in a bay the controller shall stop both roof fans and leave the plenum to the passive hood slot (240 cm2 free area), and restart the fans only on a technician's reset; PR-007's vent path to the roof is then the passive hood slot (DKH-DEC-001 D1, from DKH-STM-001 S13) | 1 fan-off rule | Pass or fail | n/a | Design review; retention test in a bay mock-up (TRL 4) | Met by design (control rule); retention time to measure at TRL 4 (S13); gas build-up with the fans stopped is not yet assessed (S29, DKH-DEC-001 O4, proposed, awaiting Amish) |

## Assumptions

- SwapCell pack (interface v0.3): 46.8 V nominal, about 468 Wh, 2.85 kg, charge on a certified 54.6 V 5 A charger in 2.3 h to full and 1.2 h for 20 to 80 %, charge window 0 to 45 °C (SWC-PRC-001 v0.3, SWC-CAL-001).
- Charger efficiency about 90 %, cell charge efficiency about 95 %, cabinet auxiliary load about 30 W on average and 40 W peak.
- 400 W panel, 4.5 peak sun hours, 0.8 derate, 96 % MPPT, feeding bay 1 only.
- Packs are released at 80 % state of charge or more, fullest first; riders arrive with a lunch and a dinner peak and leave after waiting 15 min (DKH-CAL-001 Table 1).
- Delivery riders cover roughly 60 to 100 km a day at about 10 Wh/km. This is an assumption to check with riders; it implies 1 to 2 swaps per rider per shift.
- Accessibility reach range from the US ADA forward reach limits (15 to 48 in); local rules may differ.
