---
doc_id: DKH-PRC-001
title: DockHub design precis
project: DockHub
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, first-order numbers, safety, media)
---

# DockHub design precis

## Summary

DockHub is a sidewalk cabinet, 1.0 m wide and 0.5 m deep, with four lockable steel bays that each hold and charge one SwapCell pack. A rider taps a card or phone, returns a flat pack to an open bay and takes a charged one from another, in about 30 seconds. Each bay is a copy of the SwapCell wall dock: a cradle with the blind-mate receptacle, a certified 54.6 V 5 A charger and a CAN channel that checks the pack before charging. Every bay is its own steel compartment venting to a rear plenum, so a pack fault is detected, cut off and ducted away from the user side. A 400 W solar canopy shades the front and supplies part of the energy; the grid supplies the rest through one single-phase circuit. At TRL 2 the concept meets its speed, throughput and grid targets on estimates, but misses the solar share (R6), cannot charge at the top of its temperature range (R9), has unverified fire containment (R8) and is over the $1,200 budget with all four bays fitted (R16 in DKH-REQ-001).

![DockHub on a sidewalk](../media/hero.png)

*Figure 1. DockHub on a sidewalk with a 1.75 m person for scale. Massing model; concept, not for fabrication.*

## How it works

1. **Identify.** The rider taps an NFC card or phone on the access panel (BOM 7). The controller (6) checks the token against its local list, so the station works without a network connection.
2. **Return.** An empty bay door (2) unlocks. The rider places the flat pack connector down in the cradle (3) and closes the door. The receptacle mates ground first, then power and CAN, and the interlock last, as the SwapCell interface requires.
3. **Check.** The controller sends the SwapCell dock heartbeat on that bay's CAN channel. The pack reports its identity, limits, temperatures and state of health. A pack with a fault, damage flag or state of health below the threshold stays locked in and is flagged for a technician; the rider still gets a charged pack.
4. **Release.** The door of the fullest healthy pack unlocks; the rider takes it and closes the door. The controller logs the pair of pack IDs against the rider token.
5. **Charge.** When the pack's limits allow, the controller closes that bay's DC contactor and its charger (5) runs CC-CV to 54.6 V. Bay 1 can also charge from the solar panel (11) through the MPPT controller (13) when the sun is up.
6. **Watch.** A thermistor at every receptacle, the pack's own temperature reports and a heat and smoke detector (9) are read every second. On an alarm the bay contactor opens, fans (10) run, the bay door stays locked, a light and buzzer warn people to stand back and an alert goes out by LTE-M.

![Daily energy flow](../media/flow.png)

*Figure 2. Daily energy at the design duty case of 20 swaps a day. All values are estimates.*

## Main components

Table 1. Main components. Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

| BOM | Component | Concept choice | Notes |
| --- | --- | --- | --- |
| 1 | Cabinet body | 1.5 mm galvanized steel, folded and riveted, 1,000 x 500 x 1,400 mm on a 100 mm plinth; bay row at 0.70 to 1.22 m, technical compartment below | IP54 target; powder coat |
| 2 | Bay doors (4) | Steel doors with gaskets and 12 V fail-secure solenoid locks and door switches | Locked unless the controller releases them |
| 3 | Bay compartments (4) | Steel liner per bay with a vent port to the plenum, cradle with SwapCell guide faces and receptacle, NTC at the receptacle | Mirrors the SwapCell wall dock; pack stands connector down |
| 4 | SwapCell packs (4, reference) | 46.8 V nominal, about 468 Wh, 340 x 90 x 80 mm | From the SwapCell project; not in station cost |
| 5 | Chargers (4) | Certified 54.6 V 5 A CC-CV lithium-ion chargers, about 300 W input each | No custom mains electronics |
| 6 | Dock controller | ESP32, four SPI CAN controllers (one channel per bay), DC contactors, current sensors, LTE-M modem, SD card | One channel per bay because every SwapCell pack answers as node 0 by default |
| 7 | Access panel | NFC reader, display and per-bay status lights at 0.85 to 1.21 m | Reader at 0.9 to 1.0 m |
| 8 | Grid input and protection | RCBO (30 mA), a breaker per charger, surge protection and isolator | Installed by a qualified electrician |
| 9 | Fire detection and suppression | Heat and smoke detector in the plenum, condensed-aerosol unit along the plenum top | Aerosol can suppress flame but cannot stop a cell in runaway |
| 10 | Vent plenum and roof louver | Rear plenum behind the bays, roof louver with rain hood and two fans | Takes charger heat and any vented gas up and out at the back |
| 11 | Solar panel | 400 W monocrystalline, tilted 10 degrees, front edge at about 2.45 m | Shades the rider and the front of the cabinet |
| 12 | Canopy frame | Four 50 mm square steel posts and two rails on the roof | Needs the plinth anchored (see numbers) |
| 13 | MPPT controller | Programmable lithium profile at 54.6 V, output limited to 5 A, feeding bay 1 | Bay 1 keeps its AC charger as a fallback |
| 14 | Plinth and anchor frame | Steel channel frame with four M12 anchors to a concrete pad | Pad not in BOM |
| 15 | Service door | Full-width steel door over the technical compartment with a cam lock | Technician access only |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with BOM numbers. Line 16 (wiring and hardware) is not shown.*

![Cutaway](../media/cutaway.png)

*Figure 4. Section through the cabinet from the front: four packs (4) in their bay compartments (3) above the chargers (5), controller (6), MPPT controller (13) and grid input (8); the plenum wall (10) is behind the bays and the roof louver above.*

## First-order numbers

All values are estimates at TRL 2, to be checked by calculation at TRL 3.

Table 2. First-order numbers.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Swap time | about 30 s | Tap 3 s, open and place 8 s, close 2 s, second door and take 10 s, close and walk 5 s | R1 met |
| Charge time per bay | about 1.2 h (20 to 80 %), about 2.3 h to full | SwapCell precis, 5 A charger | R3 met |
| Energy per swap | about 400 Wh stored, about 470 Wh from the supply | Pack returned at 15 %: 0.85 x 468 Wh; charger 90 %, cell 95 % | |
| Maximum throughput | about 38 swaps a day | 4 bays, one full charge per bay about every 2.5 h | R4 met |
| Daily energy at 20 swaps | about 10.1 kWh in, 8.0 kWh stored in packs | 9.4 kWh to chargers plus 0.7 kWh cabinet loads (30 W average) | |
| Solar share | about 1.3 kWh a day, about 13 % | 400 W x 4.5 h x 0.8, less clipping at the 5 A bay limit | **R6 not met** |
| Peak grid draw | about 1.25 kW | 4 x 300 W chargers plus about 40 W auxiliaries; about 10.4 A at 120 V, 5.4 A at 230 V | R5 met |
| Heat inside the cabinet | about 200 W at full charge | Charger losses 4 x 30 W, pack losses 4 x 14 W, auxiliaries | |
| Airflow for a 10 K rise | about 60 m³/h (35 cfm) | 200 W / (1.2 kg/m³ x 1,005 J/(kg·K) x 10 K) | Two 120 mm fans suffice |
| Interior air at 45 °C ambient | about 55 °C | 10 K rise above ambient, canopy shading the roof | **R9 not met**: packs above their charge limit; charging pauses or derates |
| Riders served | about 10 to 20 a day | 20 swaps, 1 to 2 swaps per rider per shift (assumed 60 to 100 km at 10 Wh/km) | Assumption to test with riders |
| Mass | about 150 to 170 kg with four packs | Steel sheet about 8 m² at 11.8 kg/m² (about 95 kg), panel 21 kg, frame and plinth 35 kg, chargers and electronics 8 kg, packs 11 kg | |
| Wind load on canopy | about 1.6 kN at a 30 m/s gust; about 3.6 kN·m overturning | Panel 1.95 m², dynamic pressure 540 Pa, force coefficient 1.5 assumed, lever arm about 2.3 m | R15 met only when anchored |
| Parts cost | about $1,423 with four bays fitted; about $1,199 with two fitted | `bom/bom.csv`, packs excluded | **R16 not met with four bays** |
| Energy cost per swap | about $0.09 | 0.47 kWh at an assumed $0.20/kWh | |

## Key design choices

Each of these is proposed, awaiting Amish.

1. **One SwapCell dock per bay, in a shared cabinet.** Each bay reuses the SwapCell dock cradle, charger and handshake, so DockHub adds only the cabinet, access, safety and energy supply. Alternative: one large shared charger with a switched output matrix (fewer parts, but a new power design and a single point of failure). Recommendation: one certified charger per bay.
2. **Four bays in one row at hand height.** Keeps the footprint to 1.0 x 0.5 m and every handle within reach. Alternatives: eight bays in two rows (more throughput, but upper or lower bays fall outside the 0.38 to 1.22 m reach range), or two bays (cheaper, about 19 swaps a day maximum). Recommendation: a four-bay cabinet, with two bays fitted for the first prototype to meet the budget.
3. **Separate steel compartment per bay with a rear plenum.** A venting pack's gas and flame go to the back and up through the roof louver, not out of the door the user is standing at, and each pack is separated from its neighbors by two steel walls and an air gap. Alternative: an open rack in one compartment (cheaper and simpler, but a single fault exposes every pack). Recommendation: per-bay compartments.
4. **Doors stay locked during a fire alarm.** Keeps people from opening a bay with a pack in runaway; the fire service opens the cabinet with a key. The trade-off is that a rider cannot retrieve a returned pack during an alarm. Recommendation: locked, with a clear warning light and a sign.
5. **Grid first, solar as a supplement.** A 400 W canopy supplies about 13 % at 20 swaps a day. Options: (a) keep the 400 W canopy as shade and supplement, and relax R6 to 10 %; (b) remove the canopy to cut cost and wind load; (c) a larger off-cabinet array, outside this budget. Recommendation: (a).
6. **Solar feeds one bay directly through an MPPT controller.** Avoids an inverter and keeps all mains parts certified. Alternative: a small hybrid inverter feeding the AC bus (all bays can use solar, but adds cost and mains electronics). Recommendation: MPPT to bay 1.
7. **Offline-first access with NFC tokens.** The station keeps a token list and a log and syncs over LTE-M when it can. Alternative: phone app only (no reader, but riders without data or a smartphone are excluded). Recommendation: NFC with an optional app.
8. **Pack health gate.** Packs below 70 % state of health, with a fault record or outside the charge temperature window are held for a technician, using the SwapCell in-pack log. Recommendation: 70 % as the first threshold.

## Relationship to other lab projects

- **SwapCell** (pack, interface v0.2, wall dock). DockHub builds to the interface and changes nothing in it. One observation for SwapCell: a multi-bay dock needs either a CAN channel per bay, as proposed here, or unique pack node numbers. This is raised for the SwapCell project, not solved locally.
- **TwinKit** could later collect DockHub's logs alongside other lab devices. That is a suggestion only and is not part of this concept.

## Safety

> **Safety:** DockHub stores and charges up to four lithium-ion packs of about 468 Wh each, next to a public walkway, from mains power. A cell in thermal runaway vents flammable, toxic gas and can ignite its neighbors; a pack fire is hard to extinguish and can re-ignite hours later. Treat the cabinet as a fire hazard at every stage of building and testing.

- **Lithium cells.** Charge only packs that pass the CAN check; never force-charge a pack that does not answer. Hold damaged, wet or faulted packs in their bay, uncharged, until a technician removes them to a fireproof container. Build and test the first cabinet on a non-combustible surface, outdoors or in a fire-rated space, with a lithium-rated extinguisher and a sand bucket at hand, and never leave it charging unattended until the detection and shutdown chain has been tested.
- **Fire containment is unproven.** The per-bay compartments and plenum are a concept. Whether they stop one pack's runaway from spreading (R8) can only be shown by a propagation test, which is TRL 4 or later work. Condensed-aerosol suppression can knock down flame but does not cool cells in runaway.
- **Mains voltage.** The technical compartment holds 120 V or 230 V AC wiring. It must be installed or checked by a qualified electrician under local electrical code, with an RCD (GFCI), per-charger breakers, surge protection, a lockable isolator and bonding of all metal parts to protective earth. Keep mains and the 54.6 V DC side physically separated and labeled.
- **DC contacts.** Receptacle contacts are at up to 54.6 V DC and a pack can deliver hundreds of amperes into a short. Contacts stay dead until the SwapCell interlock closes and a heartbeat is valid.
- **Public siting.** Place the cabinet away from building entrances, exits and windows, with the plenum louver venting away from people. Anchor the plinth; the canopy creates a large overturning moment in wind. Keep a clear pedestrian path beside the cabinet.
- **Pinch and sharp edges.** Fold or hem all sheet edges; door locks must not pinch fingers. Canopy edges above head height need rounded corners.
- **Heat.** A dark cabinet in sun can exceed pack charge limits; the controller must pause charging when the pack or bay is too hot.

## Open questions

- Pack ownership model: station-owned pool, rider-owned packs exchanged one for one, or fleet packs? Proposed, awaiting Amish.
- Which lithium-ion propagation test and standard should a later version aim for, and can a garage-built cabinet realistically pass it?
- Is an aerosol unit worth its cost, or would sand or vermiculite-filled bay floors and a sealed, vented compartment be better?
- Can the cabinet be kept below the pack charge limit in hot climates by shading, a white finish and more airflow, or does it need active cooling?
- Which siting permissions apply on public sidewalks in the first pilot city, and who hosts the electrical supply?
- How are riders who do not want to share identity served (anonymous prepaid cards)?
