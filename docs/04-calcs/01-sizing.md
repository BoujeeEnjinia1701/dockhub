---
doc_id: DKH-CAL-001
title: DockHub sizing calculations
project: DockHub
doc_type: Calculation note
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (charging, swap time, throughput and solar day model, grid, thermal, fire timing, geometry, mass, wind and anchoring, cost) against SwapCell interface v0.3
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# DockHub sizing calculations

On paper, the four-bay DockHub meets nine of its sixteen requirements. **Two are not met.** R6: the 400 W canopy supplies 9.3 % of the charging energy at the duty case, below even the relaxed 10 % target. R9: the SwapCell pack refuses charge above 45 °C, so charging pauses whenever ambient air exceeds about 29 to 39 °C, well below the 45 °C design ambient. Three are **at risk**: R8 (fire containment, only a propagation test can show it), R15 (the canopy makes the cabinet overturn unless anchored; the anchors and pad are not yet chosen) and R16 ($1,199 against $1,200 with two bays fitted). R7 and R14 cannot be verified until hardware exists.

Two findings change the TRL 2 picture. First, a swap needs an empty bay for the returned pack, so a station with *n* bays holds *n* - 1 packs. The four-bay station has three working packs (36 swaps a day at most, released full), and the two-bay first prototype has one, which serves only 9 of the 20 duty-case swaps. Second, the cabinet with its canopy frame weighs about 205 to 234 kg, not 150 to 170 kg.

Every number here is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads the geometry parameters from `cad/src/model.py` and the costs from `bom/bom.csv`. All values are first-principles estimates; nothing is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design.*

| Input | Value | Basis |
| --- | --- | --- |
| Pack | 13S2P, 46.8 V nominal, up to 54.6 V, 10 Ah, 468 Wh, 110 mΩ, 2.85 kg, 393 mm overall; charge window 0 to 45 °C | SwapCell interface v0.3, SWC-CAL-001 |
| Pack heat path | 1.17 W/K to the surrounding air, 32 min time constant | SWC-CAL-001 (open air) |
| Charger | 5 A CC to 85 %, then CV tapering linearly to 1 A (0.6 h); 90 % efficient; 303 W input at the end of CC | SWC-CAL-001; certified charger |
| Cell charge efficiency | 95 % for energy accounting; heat in the pack between I²R (2.75 W) and all of the 5 % loss (13.7 W) | SWC-CAL-001 |
| Duty case | 20 swaps a day, packs returned at 15 %, released at 80 % or more (fullest first) | DKH-REQ-001; release threshold decided by Amish, 2026-09-25 (DKH-DDR-002) |
| Demand profile | Arrivals at 07:30, 08:30, 09:30, 11:00, 11:45, 12:15, 12:45, 13:15, 14:00, 15:30, 16:30, 17:30, 18:00, 18:30, 19:00, 19:30, 20:00, 20:30, 21:15 and 22:30; a rider leaves after waiting 15 min | Lunch and dinner peaks; to be tested with riders |
| Cabinet loads | 30 W average, 40 W peak | Controller, modem, display, lights, fans, locks |
| Charger power factor | 0.95 with power factor correction, 0.6 without | Typical ranges; the chosen charger must be checked |
| Branch circuit | 120 V 15 A or 230 V 10 A, continuous load 80 % of the rating | Common practice for continuous loads |
| Solar | 400 W, 4.5 peak sun hours on a sine profile from 06:00 to 18:00, 0.8 derate, MPPT 96 %, 50 V mean charging voltage; bay 1 uses the MPPT when it offers 50 W or more, otherwise its AC charger | Clear day in a sunny city; control rule for the MPPT to bay 1 decided by Amish, 2026-09-25 (DKH-DDR-002) |
| Cabinet heat transfer | Film coefficients 17 W/(m² K) outside and 8 W/(m² K) inside; two 120 mm fans at 90 m³/h free air each, half lost to the filter and louver | Still air with light wind; typical fans |
| Sun on the cabinet | 500 W/m² on the front and one end wall, absorptance 0.35 (light powder coat); roof shaded by the canopy | Afternoon sun |
| Wind | 30 m/s gust, air 1.225 kg/m³; panel force coefficient 1.5 normal to the panel with the centre of pressure a quarter of the panel depth from its centre; body drag coefficient 1.3; posts 2.0; load factor 1.5 for the anchors; friction 0.4 | TRL 2 assumption for the panel; typical values otherwise |
| Steel | 7,850 kg/m³, 1.5 mm sheet, 15 % added for hems and flanges | Decided sheet gauge (R10) |

## 2. Charging (R3)

With the SwapCell charge profile, a pack charges from 20 to 80 % in **1.20 h** and from empty to full in **2.30 h** (1.70 h CC and 0.60 h CV). R3 (1.5 h and 2.5 h) is met. A pack returned at 15 % reaches the 80 % release level in 1.30 h and full in 2.00 h.

Each full recharge from 15 % stores 397.8 Wh, takes 418.7 Wh from the charger and 465.3 Wh from the grid, about $0.093 of electricity at an assumed $0.20/kWh. Each charger draws 303 W at the end of CC and loses about 30 W as heat.

## 3. Swap time (R1)

*Table 2. Task analysis for a rider who knows the station.*

| Step | Time (s) |
| --- | --- |
| Tap card or phone; token checked offline | 3 |
| Empty bay door unlocks | 1 |
| Open door, place the flat pack connector down | 8 |
| Close door | 2 |
| Controller confirms the return (door switch, coded INTERLOCK, pack identity on CAN) | 2 |
| Second door unlocks; open it and lift out the charged pack | 10 |
| Close door, step away | 5 |
| **Total** | **31** |

R1 (60 s) is met with a margin of about half. The 2 s return check depends on how fast a sleeping pack wakes on the coded INTERLOCK loop and answers the heartbeat; SwapCell interface v0.3 gives no wake time, so this is an assumption.

## 4. Throughput and solar share (R4, R6)

**One bay is always empty.** A swap starts by placing the flat pack in an empty bay, so a station with *n* bays runs with *n* - 1 packs. The ceiling is (*n* - 1) x 24 h divided by the recharge time: **36 swaps a day** for four bays with packs released full, or 55 at the 80 % release level; **12** (or 18) for the two-bay first prototype. At a peak, four bays can serve about 2.3 swaps an hour after the first three; two bays serve 0.77.

A minute-step model of the design day (the script runs three identical days and reports the third) gives Table 3.

*Table 3. Design day, 20 swaps, packs returned at 15 %.*

| Case | Served | Longest wait | Solar used | Solar share of charging energy |
| --- | --- | --- | --- | --- |
| Four bays, fullest pack released first | 20 of 20 | 4 min | 0.74 of 1.38 kWh | **9.3 %** |
| Four bays, bay 1 released first when the sun is up | 19 of 20 | 0 (one rider leaves after 15 min) | 0.86 of 1.38 kWh | 11.4 % |
| Two bays (first prototype) | 9 of 20 | 0 (11 riders leave) | 0.69 of 1.38 kWh | 19.9 % |

**R4 is met by the four-bay fit**: all 20 riders are served and only one waits, for 4 minutes. The two-bay prototype, adopted to meet the budget (DKH-DDR-001 item 1), can show the swap, charge and safety chain but cannot run the duty case.

**R6 is not met.** The panel gives 1.44 kWh of DC on the design day and the MPPT delivers 1.38 kWh, but it can feed only bay 1. Bay 1 is sometimes the empty bay and at other times holds a pack that is already full, so only 0.74 kWh reaches a pack: 9.3 % of the charging energy against the relaxed 10 % target. Sending flat packs to bay 1 in daylight raises the share to 11.4 %, but solar charging at up to 181 W is slower than the 5 A AC charger, so fewer packs are ready at the dinner peak and one rider in 20 leaves. The TRL 2 estimate of 13 % assumed all the solar energy would be used. The peak MPPT output of 181 W is below the 5 A bay limit (about 250 W), so there is no clipping on the design day.

## 5. Daily energy

At the duty case the four-bay station takes **8.76 kWh a day from the grid** (8.04 kWh to the chargers and 0.72 kWh for cabinet loads) and 0.77 kWh from the panel, and stores 7.58 kWh in the packs riders take away. Losses are 0.80 kWh in the chargers, 0.03 kWh in the MPPT and 0.40 kWh in the cells. Figure 2 of DKH-PRC-001 uses these values. Grid energy per swap, including the cabinet loads, costs about $0.088 at $0.20/kWh.

## 6. Grid supply (R5)

With four chargers at the end of CC and 40 W of auxiliaries, the peak real power is **1,253 W**, inside the 1.5 kW target (647 W with two bays fitted). In the day model at most three chargers run at once, because one bay is always empty.

*Table 4. Supply current with four chargers running.*

| Charger power factor | Apparent power | 120 V (12 A continuous limit) | 230 V (8 A continuous limit) |
| --- | --- | --- | --- |
| 0.95 (with correction) | 1,317 VA | 11.0 A | 5.7 A |
| 0.6 (without) | 2,062 VA | **17.2 A** | **9.0 A** |

R5 is met **only with chargers whose power factor is 0.9 or better**; without power factor correction four chargers overload a 120 V 15 A circuit and exceed the continuous limit of a 230 V 10 A circuit. `bom/bom.csv` line 5 now specifies this.

## 7. Thermal (R9)

The cabinet skin has an area of 5.20 m², a U-value of 5.44 W/(m² K) and a loss conductance of 28.3 W/K; the fans move 90 m³/h (53 cfm), worth 30.1 W/K. With three packs charging, the heat inside is 91 W from the chargers, 8 to 41 W from the packs, 30 W of cabinet loads and 118 W of sun through the walls. The cabinet air rises only **4.2 to 4.8 K** above ambient, less than the 10 K assumed at TRL 2, so at 45 °C ambient it is about 49 °C, not 55 °C.

That does not rescue R9, because the pack itself refuses to charge above 45 °C. By the end of the CC phase a pack is 2.2 to 10.8 K above the cabinet air, so **uninterrupted 5 A charging needs ambient air below about 29 to 39 °C**. At the 45 °C design ambient the packs are at 51 to 61 °C and do not charge at all; a fixed 5 A charger can only pause. At the cold end, an idle cabinet runs only 1.1 K above ambient with the fans off, so a pack that has cooled in the cabinet cannot start charging below about -1 °C; a pack returned warm from a ride can. The requirement that the station never charges outside the pack's window is met by the pack and the controller, but the operating range is not: **R9 is not met**. Shading, a lighter finish or more airflow cannot bring air at 45 °C below the 45 °C limit; that needs active cooling, a pack with a higher charge limit or a narrower design ambient, which is Amish's call.

## 8. Fire detection and venting (R7, R8)

The electronic part of the detection chain takes about **3.1 s**: a 1 s NTC sample period, two confirming samples and a 0.1 s controller loop, leaving 6.9 s of the 10 s target for the sensor's own thermal lag. A pack's over-temperature fault arrives on CAN as soon as it changes. Opening the bay contactor takes about **0.15 s** (0.10 s decision and 0.05 s drop-out), inside the 1 s target. Smoke transport to the plenum detector and the sensor lag can only be measured, so R7 is **not verifiable at TRL 3**.

The vent path widens from each 36 cm² bay port into a 1,281 cm² plenum and out through 158 cm² of louver, where the fans move air at about 1.6 m/s. Whether this path, two 1.5 mm steel walls and the air gap stop a runaway from spreading for 30 min (R8) can be shown only by a propagation test, which is TRL 4 work and on hold. R8 stays **at risk**.

## 9. Geometry (R2, R11, R13)

The model places the pack's connector face on the cradle at 730 mm and its handle top at 1,105 mm. The door opening is 510 x 172 mm against the 393 mm overall pack, leaving 115 mm above the handle for the hand; the rider lifts the pack 19 mm to clear the receptacle. Every operable part lies between 0.73 and 1.10 m (door handles 0.94 to 0.98 m, reader 0.90 to 0.99 m), inside the 0.38 to 1.22 m range: **R11 met**.

The plinth is now flush with the body, so the footprint is 1,000 x 500 mm (door handles add 22 mm at the front); at TRL 2 it was 1,020 x 520 mm, which broke the 1.0 m width limit. The panel's rear edge underside is at 2,214 mm and its front top edge at 2,446 mm; the lowest canopy point over the sidewalk is a rail end at 2,179 mm (printed by `cad/src/model.py`). **R13 met.**

For R2, each bay builds to SwapCell interface v0.3 without changing it: a blind-mate receptacle with a 10 kΩ coding resistor in the INTERLOCK loop (item W), dock host type 1 in the heartbeat, a class D gravity catch for the pack's latch pawl (item V) and a CAN channel per bay at 250 kbit/s. At 34.1 frames per second one pack loads its channel to 1.8 %; the four SPI CAN controllers need about 17.5 kbit/s of SPI traffic in all. Packs still default to node 0, and v0.3 node numbers 0 to 7 do not remove the need for separate channels, because a pack's node number would have to change at every station. **R2 met by design review.**

For R12, a 64 B log record per swap is 1.28 kB a day, and a list of 10,000 rider tokens at 16 B each is 160 kB, both trivial for the controller's flash and SD card over 24 h offline. **R12 met by design review.**

## 10. Mass

*Table 5. Mass of the four-bay station with three packs.*

| Part | Mass (kg) |
| --- | --- |
| Sheet steel, 9.92 m² at 1.5 mm plus 15 % | 134.4 |
| Plinth, 4.0 m of 100 x 50 x 5 mm channel | 29.8 |
| Canopy posts and rails | 21.0 |
| Solar panel | 21.0 |
| Chargers (4) | 4.8 |
| Cradles and receptacles (4) | 2.0 |
| Controller, MPPT, grid unit, access panel, fire unit, fans, wiring | 12.0 |
| Packs (3) | 8.6 |
| **Total** | **234** |

The two-bay prototype without packs weighs about **205 kg**, which is used for the wind check. The TRL 2 estimate of 150 to 170 kg counted about 8 m² of sheet; the model's bay liners, deck, plenum wall and charger rack bring it to 9.92 m².

## 11. Wind and anchoring (R15)

At a 30 m/s gust the dynamic pressure is 551 Pa. The 1.95 m² panel takes a normal force of 1,615 N, which at 10° of tilt is 280 N sideways and **1,590 N of uplift**, acting 429 mm in front of the cabinet centre; the posts add 158 N and the body 1,075 N of drag. About the rear bottom edge this gives an overturning moment of **2.91 kN·m**, against 0.50 kN·m from the prototype's own weight: a factor of 0.17. Unanchored, the cabinet would tip, and friction alone (169 N) would not stop it sliding either. The TRL 2 note treated the canopy force as horizontal and missed the uplift; the corrected moment is lower than its 3.6 kN·m, but the conclusion stands.

With four M12 anchors 30 mm in from the front and rear edges, each front anchor carries **2.56 kN** of tension, **3.83 kN** with the 1.5 load factor, and each anchor about 0.57 kN of design shear. Each front canopy post pulls up on the roof frame with about 1,251 N, so the posts must bolt through to a frame, not to the 1.5 mm roof sheet alone; the posts themselves see only 9.4 MPa in bending (50 x 50 x 3 mm hollow section, 714 mm long). R15 is **at risk** until an anchor with a rated design tension of at least 3.8 kN in the host concrete and a pad are chosen; neither is in the BOM.

## 12. Cost (R16)

*Table 6. Cost summary from `bom/bom.csv` (two of four bays fitted).*

| Group | Lines | Cost (USD) |
| --- | --- | --- |
| Cabinet, doors, service door, plinth | 1, 2, 14, 15 | 374 |
| Bays (2): compartments, chargers | 3, 5 | 180 |
| Controller, access, grid, wiring | 6, 7, 8, 16 | 250 |
| Fire detection and venting | 9, 10 | 155 |
| Solar canopy and MPPT | 11, 12, 13 | 240 |
| **Total** | 1 to 16 | **1,199** |

The total is $1 under the $1,200 budget, so R16 is **at risk** on indicative prices. Each further bay adds $112; all four bays fitted cost $1,423. SwapCell packs are not in the station cost: the prototype needs one resident pack and the four-bay station three, at about $414 each in the SwapCell BOM, plus one per rider in circulation.

## 13. Results against requirements

*Table 7. Requirement status. Not met, at risk and not verifiable items first.*

| ID | Value (DKH-CAL-001) | Target | Status |
| --- | --- | --- | --- |
| R6 | 9.3 % of charging energy (0.74 of 1.38 kWh used); 11.4 % with solar steering, which turns one rider away | 10 % or more (relaxed from 20 %, DKH-DDR-001) | **Not met** |
| R9 | Charging pauses above about 29 to 39 °C ambient and for cold-soaked packs below about -1 °C; charge window enforced | -10 to 45 °C ambient; never charge outside the pack window | **Not met** |
| R8 | Two 1.5 mm steel walls and a gap between packs; vent path to the roof | No spread for 30 min | At risk (not verifiable at TRL 3) |
| R15 | Overturning 2.9 kN·m against 0.50 kN·m self-weight; anchors 3.8 kN design tension each | Upright at a 30 m/s gust | At risk (anchors and pad not chosen) |
| R16 | $1,199 with two of four bays fitted ($1,423 with four) | $1,200, packs excluded | At risk |
| R7 | Electronic latency 3.1 s; contactor 0.15 s | Detect in 10 s; contactor in 1 s | Not verifiable at TRL 3 |
| R14 | All parts reached through the service door or a bay door with hand tools | 15 min per part | Not verifiable at TRL 3 |
| R1 | 31 s task analysis | 60 s or less | Met |
| R2 | Interface v0.3: coded INTERLOCK receptacle, host type 1, class D catch, one CAN channel per bay | Build to the SwapCell interface, no change | Met (design review) |
| R3 | 20 to 80 % in 1.2 h; full in 2.3 h | 1.5 h; 2.5 h | Met |
| R4 | Four bays: 20 of 20 served, longest wait 4 min; ceiling 36 a day. Two-bay prototype: 9 of 20 | 20 a day from 4 bays | Met (four bays) |
| R5 | 1.25 kW; 11.0 A at 120 V with power factor 0.95 (17.2 A at 0.6) | 1.5 kW; one branch circuit | Met (power factor 0.9 or better) |
| R10 | 1.5 mm steel, fail-secure locks, anchored plinth, token plus returned pack | Security features | Met (design review) |
| R11 | Operable parts 0.73 to 1.10 m | 0.38 to 1.22 m | Met |
| R12 | 1.28 kB of log a day; 160 kB token list | No cameras; 24 h offline | Met (design review) |
| R13 | 1.0 x 0.5 m; lowest canopy point over the sidewalk 2.18 m | 1.0 x 0.6 m; 2.1 m | Met |

Counts: 2 not met, 3 at risk, 2 not verifiable at TRL 3, 9 met.

## 14. Checks against earlier documents

The TRL 2 figures in DKH-PRC-001 v0.2 and DKH-REQ-001 v0.2 were checked against this script and corrected in v0.3:

- Maximum throughput 38 to 36 swaps a day (three working packs, not four); two bays 19 to 12 a day.
- Solar share 13 % to 9.3 % (bay 1 cannot always use the sun); no clipping on the design day.
- Daily energy at 20 swaps 10.1 kWh in and 8.0 kWh stored to 9.53 kWh in (8.76 grid, 0.77 solar) and 7.58 kWh stored, because packs leave at 80 % or more.
- Swap time 30 s to 31 s with the return check.
- Cabinet air rise 10 K to 4.2 to 4.8 K; the R9 shortfall is now set by the pack's 45 °C charge limit rather than by the cabinet air.
- Mass 150 to 170 kg to 205 kg (prototype, no packs) and 234 kg (four bays, three packs).
- Wind: 3.6 kN·m to 2.91 kN·m with the panel force resolved into uplift and drag, and anchor loads now given.
- Footprint 1,020 x 520 mm to 1,000 x 500 mm (plinth made flush).
- SwapCell pack price $370 to $414 (SWC-CAL-001).

> **Safety:** These are paper estimates for a cabinet that stores and charges lithium-ion packs of about 468 Wh beside a public walkway from mains power. They do not replace an electrician's design of the supply, a structural check of the anchors and pad, or a propagation test. No cabinet may be built, powered or anchored in a public place from this note; building and testing are TRL 4 work and on hold by Amish's instruction.
