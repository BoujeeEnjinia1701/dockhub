---
doc_id: DKH-REQ-001
title: DockHub requirements
project: DockHub
doc_type: Requirements
version: "0.2"
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
---

# DockHub requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with riders, hosts or a city, and will be checked by calculation at TRL 3 and revised after co-design sessions (see DKH-PRB-001). Every target is proposed, awaiting Amish.

The **design duty case** used throughout is 20 swaps a day, each returning a SwapCell pack at about 15 % state of charge, in a street location with 4.5 peak sun hours and ambient air between -10 and 45 °C.

Table 1. Requirements. Status is the TRL 2 estimate from DKH-PRC-001.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 2 |
| --- | --- | --- | --- | --- |
| R1 | Fast swap | 60 s or less from tapping the reader to closing the second door, for a rider familiar with the station | Task analysis; later timed trials with riders | Met on estimate (about 30 s) |
| R2 | SwapCell compatibility | Every bay builds to SwapCell interface v0.2: envelope, guide faces, blind-mate receptacle, CAN heartbeat and message set; no change to the interface | Interface review with the SwapCell project | Met by design; one CAN channel per bay needed |
| R3 | Charge speed | 20 to 80 % in 1.5 h or less; full charge in 2.5 h or less, per bay, at 25 °C | Charger and pack datasheets; SwapCell charge estimate | Met on estimate (1.2 h and 2.3 h) |
| R4 | Throughput | 20 or more swaps a day from 4 bays at the design duty case | Queue and energy calculation | Met on estimate (about 38 a day maximum) |
| R5 | Grid supply | One single-phase branch circuit (120 V 15 A or 230 V 10 A); peak draw 1.5 kW or less | Load calculation | Met on estimate (about 1.25 kW) |
| R6 | Solar contribution | Canopy solar supplies 20 % or more of daily charging energy at the design duty case | Solar yield calculation | **Not met** (about 13 %) |
| R7 | Fire detection and response | Detect a pack or bay over 60 °C, or smoke, within 10 s; open that bay's charge contactor within 1 s of detection; sound a local alarm and send a remote alert; vent gas to the rear roof louver, away from the user side | Design review; later bench test with a heat source | Met by design on paper; unverified |
| R8 | Fire containment | A thermal runaway in one bay does not spread to a neighboring bay or pack for 30 min or more, and flame does not leave the cabinet front | Later propagation test by an accredited lab | **Unverified, at risk** |
| R9 | Climate | Enclosure IP54 or better; operate at -10 to 45 °C ambient; never charge a pack outside the pack's reported charge temperature window | Thermal calculation; later chamber test | **Not met at 45 °C** (interior about 55 °C; charging derates) |
| R10 | Security | 1.5 mm or thicker steel; fail-secure bay locks; cabinet anchored to its pad with tamper-resistant fixings; a pack is released only against a valid token and a returned pack | Design review | Met by design |
| R11 | Accessibility and use | All operable parts (reader, buttons, bay handles) 0.38 to 1.22 m (15 to 48 in) above the ground; status shown by light and symbol as well as text; usable with gloves and at night | Model check; later user trials | Met by design (bay handles at about 0.96 m, reader at 0.9 to 1.0 m) |
| R12 | Privacy and data | No cameras or microphones; logs hold pack ID, bay, time, energy and state of health, with the rider as an opaque token; operates offline for 24 h or more and syncs later | Design review | Met by design |
| R13 | Sidewalk footprint | Cabinet footprint 1.0 x 0.6 m or less; canopy underside 2.1 m or more above the sidewalk | Model check | Met (1.0 x 0.5 m; lowest canopy edge about 2.2 m) |
| R14 | Maintainability | Any charger, lock, bay cradle or controller replaced in 15 min or less by one technician with hand tools, through the service door | Design review | Met by design |
| R15 | Wind and anchoring | Stays upright and intact at a 30 m/s gust with the canopy fitted | Wind load calculation | Met only if anchored (overturning about 3.6 kN·m against about 0.4 kN·m from self-weight) |
| R16 | Cost | Parts 1,200 USD or less for a working prototype, SwapCell packs excluded | Priced BOM (`bom/bom.csv`) | **Not met with 4 bays fitted** (about $1,423); met with 2 of 4 bays fitted (about $1,199) |

## Assumptions

- SwapCell pack: 46.8 V nominal, about 468 Wh, charge on a certified 54.6 V 5 A charger, 2.3 h to full and 1.2 h for 20 to 80 %, as in the SwapCell design precis (interface v0.2).
- Charger efficiency about 90 %, cell charge efficiency about 95 %, cabinet auxiliary load (controller, modem, display, fans, lights) about 30 W on average.
- 400 W panel, 4.5 peak sun hours, 0.8 system derate and some clipping at the 5 A bay limit: about 1.3 kWh a day.
- Delivery riders cover roughly 60 to 100 km a day at about 10 Wh/km. This is an assumption to check with riders; it implies 1 to 2 swaps per rider per shift.
- Accessibility reach range from the US ADA forward reach limits (15 to 48 in); local rules may differ.
