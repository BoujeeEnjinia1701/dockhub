---
doc_id: DKH-RSK-001
title: DockHub risk register and hazard analysis
project: DockHub
doc_type: Risk register and hazard analysis
version: "0.1"
status: Draft
date: 2026-10-31
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-31
    author: Amish Chadha
    change: First risk register, preliminary hazard analysis (stage P1) and first-pass design FMEA (stage P3) for option A at the kit 1.9.1 upgrade
---

# DockHub risk register and hazard analysis

The top project risk is cost and sourcing: the parts come to USD 1,519 against a USD 1,200 target and the pack supply depends on the SwapCell project. The top hazard is a thermal runaway of a lithium pack in a bay on a public sidewalk, controlled by the steel compartment, the detector, the aerosol unit, the vent plenum and the rule that no pack is charged outside its window; the highest design FMEA scores are a runaway that spreads to a neighbouring bay (RPN 120), a pack that overheats on a hot day (RPN 72) and gas that collects in the plenum once the fans stop (RPN 60). Scores are 1 to 5. Risk is likelihood times impact. Method: STANDARDS section 23.

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | No co-design partner | Candidate partner (Los Deliveristas Unidos, DKH-DEC-001) not yet approached | Requirements stay desk assumptions; no TRL 4 | 3 | 5 | Amish | Approach the partner before TRL 4 |
| P2 | Over the cost target | USD 1,519 parts against USD 1,200; pad USD 265 | Prototype is not built within the target | 4 | 3 | Amish | Keep as a target; use a host slab where an engineer confirms it; review at supplier selection (DKH-DEC-001 O3) |
| P3 | SwapCell interface changes | Pack project revises v0.3 | Receptacle, cradle and CAN set change | 2 | 4 | SwapCell project | Build to v0.3; conflicts raised with the SwapCell project (DKH-DDR-001) |
| P4 | Fire certification route unclear | FDNY guide covers charging cabinets, not swap stations by name (DKH-REG-001 G1) | Cabinet cannot be sited | 3 | 5 | Design lead | Ask FDNY early; UL 1487 route costed at TRL 4 |
| P5 | Charger power factor too low | Cheapest certified chargers lack PFC | 17.2 A at 120 V, over a 15 A circuit | 3 | 3 | Design lead | Buy PFC chargers; to confirm at purchase (DKH-DEC-001 to-confirm item 1) |
| P6 | Pilot site too hot | Summer highs well above 30 C | Charging pauses in the afternoon, fewer swaps | 3 | 3 | Design lead | Choose a site with highs near 30 C (DKH-DEC-001); revisit cooling for hot climates |
| P7 | Pack supply and deposits | Station-owned pool not funded | No charged packs to swap | 3 | 4 | Partner | Confirm the ownership model in co-design (DKH-DEC-001) |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Fire from a pack thermal runaway | Cell defect, abuse, over-temperature, crushed pack | Burns, smoke, fire spreading to the street or a building | 5 | 3 | Steel compartment per bay; detector within 10 s and contactor in 1 s; condensed aerosol; vent plenum to a rear roof hood; doors locked during an alarm; pack refuses charge outside 0 to 45 C; propagation test planned | 3 |
| H2 | Toxic or flammable gas at the door | Venting pack | Irritation, burns | 4 | 2 | Gas leaves by the plenum to the rear roof; door locked during alarm; fans stop on aerosol discharge (DKH-DEC-001 D1) | 2 |
| H3 | Electric shock | 120 or 230 V mains in the technical compartment; 54.6 V pack terminals | Shock, burns | 5 | 2 | RCBO in the grid unit; mains only behind the locked service door; blind-mate receptacle; INTERLOCK coding resistor; isolate before service | 2 |
| H4 | Door pinch | Hand in the door gap as the steel door shuts | Crushed finger | 3 | 3 | Doors close by hand on piano hinges with an EPDM gasket, no powered closing; broken edges | 2 |
| H5 | Cabinet falls over | 30 m/s gust on the canopy; vandal pulling | Crush injury, damage | 5 | 2 | Four M12 anchors into a 1.1 t pad, equilibrium factor 1.12; canopy lowest point 2.17 m | 3 |
| H6 | Strain from lifting a pack | 2.85 kg lifted from a low bay | Back or wrist strain | 2 | 3 | Connector 0.73 m and handle top 1.105 m above the ground; pack far under lifting limits | 1 |
| H7 | Burn from a hot pack | A pack taken just after charging | Minor burn | 2 | 2 | Pack temperature window; released at 80 % state of charge | 1 |
| H8 | Trip or collision on the sidewalk | Plinth and canopy edges in a pedestrian way | Fall, cut, bump | 3 | 3 | 1.0 x 0.5 m footprint; broken edges; canopy above 2.1 m; private property first | 2 |
| H9 | Theft and vandalism | Packs are valuable; unattended | Loss, forced entry, damaged locks | 3 | 4 | 1.5 mm steel, fail-secure locks, anchored plinth, tokens plus a returned pack | 3 |
| H10 | Installer injury at the pad | About 1.1 t of concrete, drilling into concrete | Dust, crush, strain | 4 | 2 | Mask and eye protection; lifting aid; 7 day cure before anchoring (build plan safety stops) | 2 |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Bay compartment and liner | Contain a runaway | Heat soaks through to the next bay | Second pack goes into runaway | 0.7 to 1 MJ into about 7 kg of liner; the gap is air | 5 | 4 | 6 | 120 | Propagation trial with plain and vermiculite floors (DKH-DEC-001); heat-soak bound 248 K (STEM S11) |
| F2 | Roof fans and aerosol unit | Vent gas and suppress flame | Fans sweep out the aerosol | Flame not suppressed | Fans ran on alarm | 4 | 2 | 4 | 32 | Fixed by D1: fans stop on discharge; retention test in a mock-up (S13) |
| F3 | Charger and pack | Charge within the window | Pack above 45 C on a hot day | Charging pauses; pack ageing | Ambient near 30 C plus 4.2 K cabinet rise plus up to 10.8 K pack rise | 3 | 4 | 6 | 72 | Controller pauses; site choice; STEM S9 |
| F4 | Detector and NTC | Detect over 60 C or smoke in 10 s | Sensor lags or is blocked | Late alarm, late contactor | Thermal lag; dust in the bay | 5 | 3 | 4 | 60 | Bench test of detection time at TRL 4 (S26); clean at service |
| F5 | Door gasket and hood | Keep IP54 | Water or dust enters | Corroded contacts, charger failure | Cut gasket, blocked rain lip, clogged filter | 3 | 3 | 4 | 36 | Enclosure test at TRL 4 (S27); filter change on the service list |
| F6 | Solenoid lock and door switch | Hold the door; confirm the return | Lock jams shut or fails open | Pack trapped, or released without a return | Water, wear, failed switch | 3 | 3 | 3 | 27 | Service release from inside; switch checked by the controller; spares |
| F7 | Receptacle and cradle | Blind-mate the pack | Misaligned contacts, damaged pins | Pack not detected, or arcing | Cradle tolerance, abuse | 4 | 2 | 4 | 32 | Guide faces on the cradle; contact check before charge |
| F8 | Anchors and pad | Hold the station down | Anchor pulls out in a gust | Cabinet moves or falls | Cracked concrete, wrong torque; 3.8 kN needed | 5 | 2 | 4 | 40 | Pull test each anchor; confirm the maker's rating (DKH-DEC-001 to-confirm item 9) |
| F9 | Controller and CAN | Run the bays | Controller hangs | Bays stop; locks stay secure | Firmware fault, power dip | 3 | 3 | 3 | 27 | Watchdog; bays stay locked and chargers hold a safe state; 24 h offline operation |
| F10 | Canopy and panel | Shade and make power | Post bolt loosens | Panel shifts, hits rider | Vibration | 4 | 2 | 4 | 32 | Locking nuts; inspect at service |
| F11 | Plenum with fans stopped | Vent hot gas after an aerosol discharge | Unburnt gas collects and ignites | Pressure pulse, door or hood damaged, flame at the hood | Fans stopped by fix D1; only the 240 cm2 hood slot vents | 5 | 2 | 6 | 60 | Calculate gas volume and an explosion-venting area; hold-time alternative (DKH-DEC-001 O4, STEM S29) |

## Sources

- DKH-CAL-001 for the loads, temperatures, latencies and masses quoted; DKH-STM-001 for the claims behind F1 to F4; DKH-REG-001 for P4.
- Hazard and FMEA scores are the author's judgment on a 1 to 5 scale, not field data.
