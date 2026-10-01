---
doc_id: DKH-REQ-001
title: DockHub requirements
project: DockHub
doc_type: Requirements
version: "0.5"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. R6 relaxed to 10 % and R16 redefined to the two-bay fit (DKH-DDR-001); R2 to SwapCell interface v0.3; status from DKH-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Status from DKH-CAL-001 v0.3 after the constructable design (DKH-DDR-003); R16 not met
---

# DockHub requirements

These requirements are checked by calculation in DKH-CAL-001 (TRL 3). They are not yet validated with riders, hosts or a city and will be revised after co-design sessions (see DKH-PRB-001). On 2026-09-25 Amish accepted the review recommendations (DKH-DDR-001, DKH-DDR-002): R6 is relaxed from 20 % to 10 %, R16 covers the four-bay cabinet with two bays fitted, and R2 cites SwapCell interface v0.3 (DKH-DDR-001 item 12). These are decided. Every other target remains as proposed at TRL 2 and will be revised after co-design.

On paper, 9 of 16 requirements are met. **R6, R9 and R16 are not met**; R8 and R15 are at risk; R7 and R14 cannot be verified until hardware exists.

The **design duty case** used throughout is 20 swaps a day, each returning a SwapCell pack at about 15 % state of charge, in a street location with 4.5 peak sun hours and ambient air between -10 and 45 °C. Because a swap needs an empty bay, a station with *n* bays holds *n* - 1 packs.

Table 1. Requirements. Status is from DKH-CAL-001.

| ID | Requirement | Target | Verification | Status at TRL 3 (DKH-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Fast swap | 60 s or less from tapping the reader to closing the second door, for a rider familiar with the station | Task analysis; later timed trials with riders | Met (31 s) |
| R2 | SwapCell compatibility | Every bay builds to SwapCell interface v0.3: envelope, guide faces, blind-mate receptacle with the 10 kΩ INTERLOCK coding resistor, class D catch, CAN heartbeat and message set; no change to the interface | Interface review with the SwapCell project | Met by design review; one CAN channel per bay |
| R3 | Charge speed | 20 to 80 % in 1.5 h or less; full charge in 2.5 h or less, per bay, at 25 °C | Charge profile calculation | Met (1.2 h and 2.3 h) |
| R4 | Throughput | 20 or more swaps a day from 4 bays at the design duty case | Day model with a demand profile | Met by the four-bay fit (20 of 20 served, longest wait 4 min; ceiling 36 a day). The two-bay first prototype serves 9 of 20 |
| R5 | Grid supply | One single-phase branch circuit (120 V 15 A or 230 V 10 A); peak draw 1.5 kW or less | Load calculation | Met (1.25 kW; 11.0 A at 120 V) with chargers of power factor 0.9 or better |
| R6 | Solar contribution | Canopy solar supplies 10 % or more of daily charging energy at the design duty case (relaxed from 20 %, DKH-DDR-001) | Day model | **Not met** (9.3 %; 11.4 % if flat packs are routed to bay 1 in daylight, which turns one rider in 20 away) |
| R7 | Fire detection and response | Detect a pack or bay over 60 °C, or smoke, within 10 s; open that bay's charge contactor within 1 s of detection; sound a local alarm and send a remote alert; vent gas to the rear roof louver, away from the user side | Latency budget; later bench test with a heat source | Not verifiable at TRL 3 (electronic latency 3.1 s, contactor 0.15 s) |
| R8 | Fire containment | A thermal runaway in one bay does not spread to a neighboring bay or pack for 30 min or more, and flame does not leave the cabinet front | Later propagation test by an accredited lab | **At risk**; not verifiable at TRL 3 |
| R9 | Climate | Enclosure IP54 or better; operate at -10 to 45 °C ambient; never charge a pack outside the pack's reported charge temperature window | Thermal calculation; later chamber test | **Not met**: charging pauses above about 29 to 39 °C ambient (pack charge limit 45 °C) and for cold-soaked packs below about -1 °C |
| R10 | Security | 1.5 mm or thicker steel; fail-secure bay locks; cabinet anchored to its pad with tamper-resistant fixings; a pack is released only against a valid token and a returned pack | Design review | Met by design review |
| R11 | Accessibility and use | All operable parts (reader, buttons, bay handles) 0.38 to 1.22 m (15 to 48 in) above the ground; status shown by light and symbol as well as text; usable with gloves and at night | Model check; later user trials | Met (0.73 to 1.10 m) |
| R12 | Privacy and data | No cameras or microphones; logs hold pack ID, bay, time, energy and state of health, with the rider as an opaque token; operates offline for 24 h or more and syncs later | Design review | Met by design review |
| R13 | Sidewalk footprint | Cabinet footprint 1.0 x 0.6 m or less; canopy underside 2.1 m or more above the sidewalk | Model check | Met (1.0 x 0.5 m with a flush plinth; lowest canopy point over the sidewalk 2.17 m) |
| R14 | Maintainability | Any charger, lock, bay cradle or controller replaced in 15 min or less by one technician with hand tools, through the service door | Design review; later timed trial | Not verifiable at TRL 3 |
| R15 | Wind and anchoring | Stays upright and intact at a 30 m/s gust with the canopy fitted | Wind load calculation | **At risk**: overturning 2.9 kN·m against 0.53 kN·m self-weight; needs four anchors of 3.8 kN design tension and a pad, not yet chosen |
| R16 | Cost | Parts 1,200 USD or less for the four-bay cabinet with two bays fitted (first prototype), SwapCell packs excluded (redefined, DKH-DDR-001) | Priced BOM (`bom/bom.csv`) | **Not met** ($1,214, after the parts added to make the design buildable, DKH-DDR-003; $1,438 with all four bays fitted) |

## Assumptions

- SwapCell pack (interface v0.3): 46.8 V nominal, about 468 Wh, 2.85 kg, charge on a certified 54.6 V 5 A charger in 2.3 h to full and 1.2 h for 20 to 80 %, charge window 0 to 45 °C (SWC-PRC-001 v0.3, SWC-CAL-001).
- Charger efficiency about 90 %, cell charge efficiency about 95 %, cabinet auxiliary load about 30 W on average and 40 W peak.
- 400 W panel, 4.5 peak sun hours, 0.8 derate, 96 % MPPT, feeding bay 1 only.
- Packs are released at 80 % state of charge or more, fullest first; riders arrive with a lunch and a dinner peak and leave after waiting 15 min (DKH-CAL-001 Table 1).
- Delivery riders cover roughly 60 to 100 km a day at about 10 Wh/km. This is an assumption to check with riders; it implies 1 to 2 swaps per rider per shift.
- Accessibility reach range from the US ADA forward reach limits (15 to 48 in); local rules may differ.
