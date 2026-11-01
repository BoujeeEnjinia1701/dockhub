---
doc_id: DKH-STM-001
title: DockHub STEM check
project: DockHub
doc_type: STEM check
version: "0.1"
status: Draft
date: 2026-10-31
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-31
    author: Amish Chadha
    change: First STEM check of the existing design (option A) at the kit 1.9.1 upgrade, with the TRL 3 calculation note DKH-CAL-001 v0.6; one detail fixed under the standing instruction (DKH-DEC-001 D1)
---

# DockHub STEM check

Verdict: the working principle (a cabinet that stores, charges, checks and hands out SwapCell packs from bays, fed by a single-phase circuit with a small solar canopy) sits within known science. The charging, energy balance, wind-pressure, pad-mass, lifting, reach, bus-load and detection-latency rows are within known science and close against the TRL 3 calculation note DKH-CAL-001. One detail failed in the first check and was fixed under Amish's standing instruction of 2026-10-23: the roof fans ran on a fire alarm and would have swept the condensed-aerosol agent out of the cabinet (D1: the fans stop on discharge and the passive hood slot vents by buoyancy). The independent review then found that the fix leaves unburnt gas in the plenum (S29), which is a safety trade-off and goes to Amish (DKH-DEC-001 O4). Of the 29 claims, **15 are within known science and 14 remain plausible, to confirm**: S7 (swap step times), S8 and S10 (cabinet heat balance in still air and in the cold), S9 (full-rate charging up to 30 C ambient, lowest calculated limit 29.4 C), S11 (no spread of a runaway for 30 min, which the heat-soak bound does not exclude), S13 and S29 (aerosol retention and gas build-up), S16 (anchors and pad, 6 % margin), S17 (canopy clearance), S19 and S20 (coating life, aerosol residue), S23 (fumes at the door), S26 and S27 (sensor lag, IP54). None can be closed by calculation, so `stem_check` stays **open**. Method: STANDARDS section 20. Calculations: `docs/04-calcs/stem_check.py` (figures from `docs/04-calcs/sizing.py`, DKH-CAL-001).

## Claims checked

Table 1. Claims, governing science and verdicts (generated from `docs/04-calcs/stem_results.csv`).

<!-- STM_TABLE -->
| # | Claim | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | A bay charges a pack from 20 to 80 % in about 1.2 h | Physics | Electromagnetism and circuits | Charge = current x time: 0.6 x 10 Ah at the 5 A constant-current stage | claimed 1.2 h, estimate 1.2 h (ratio 1.00) | Within known science | DKH-CAL-001 s2 (1.20 h) |
| S2 | A pack charges from empty to full in about 2.3 h at 25 C | Physics | Electromagnetism and circuits | Constant current to 85 % (1.7 h), then a 0.6 h tapering constant-voltage stage (SWC-CAL-001) | claimed 2.3 h, estimate 2.3 h (ratio 1.00) | Within known science | DKH-CAL-001 s2 (2.30 h) |
| S3 | Four bays draw a peak of 1.25 kW from the grid | Physics | Electromagnetism and circuits | P = 4 x (54.6 V x 5 A / 0.90) plus 40 W of cabinet load; an upper bound, since one bay is always empty and the simulated day never runs more than 3 chargers at once | claimed 1.25 kW, estimate 1.25 kW (ratio 1.00) | Within known science | DKH-CAL-001 s6 (1253 W; 3 chargers at once in the simulated day) |
| S4 | Daily energy at 20 swaps: grid and solar in equal stored energy plus losses | Physics | Thermodynamics | Conservation of energy over a day (first law); the losses are computed independently as 10 % in the charger and 5 % in the cells (0.80 and 0.40 kWh), not by subtraction | in 9.53 kWh, out 9.53 kWh | Within known science | DKH-CAL-001 s5 (9.53 kWh in) |
| S5 | A 400 W panel gives about 1.38 kWh a day at the MPPT output (4.5 sun hours); 0.74 kWh of it reaches the packs | Physics | Electromagnetism and circuits | Rated power x peak sun hours x 0.8 derate x 0.96 MPPT efficiency | claimed 1.382 kWh, estimate 1.38 kWh (ratio 1.00) | Within known science | DKH-CAL-001 s4 (1382 Wh) |
| S6 | At most 36 swaps a day from 3 resident packs released full (55 at the adopted 80 % release; 24 with one bay out of service) | Mathematics | Orders of magnitude | Packs x hours in a day / hours to recharge a returned pack (15 to 100 %, 2.0 h) | claimed 36 swaps, estimate 36 swaps (ratio 1.00) | Within known science | DKH-CAL-001 s4 |
| S7 | A swap takes 60 s or less for a familiar rider | Mathematics | Orders of magnitude | Sum of the task steps: tap 3, unlock 1, open and place 8, close 2, confirm 2, unlock 10, lift and close 5 s = 31 s; every step time and the 2 s pack wake is an assumption | 31 s against 60 s; step times to measure with riders | Plausible, to confirm at TRL 3 | Open |
| S8 | With 3 packs charging the cabinet air rises about 4.2 K above ambient | Physics | Thermodynamics | Steady heat balance: heat = (wall UA + fan flow x rho cp) x rise = 247 W / 58.4 W/K = 4.23 K, reproduced; it assumes half the fans' free-air flow, a lightly windy outside film and fully mixed air; the independent review finds 8.7 K with the fans off and about 5.5 K in still air, and the air at the packs in closed bays is hotter than the cabinet average | 4.2 K in the stated case; still-air and fan-failure cases to add | Plausible, to confirm at TRL 3 | Open |
| S9 | A pack charges at full rate without passing its 45 C limit at 30 C ambient (R9) | Physics | Thermodynamics | Pack temperature = ambient + cabinet air rise + pack rise at the end of constant current; highest ambient for uninterrupted charging 29.4 C (5 % loss bound) to 38.6 C (I2R only); the pack refuses charge above 45 C, so the failure mode is a pause, not damage | 29.4 to 38.6 C against the 30 C wanted: the warmest bay may pause just under 30 C; the review notes the figure uses the pack's open-air heat path in a closed bay and a cabinet-temperature start, so the true limit may be lower | Plausible, to confirm at TRL 3 | Open |
| S10 | An idle cabinet with the fans off stays about 1 K above ambient in the cold | Physics | Thermodynamics | Steady heat balance: 30 W of controller load through a wall UA of 28.3 W/K = 1.06 K; the 30 W includes fan power and vent losses through the hood slot and intake are not counted, so the cold-start limit is nearer 0 C than -1 C | 1.1 K in the stated case; vent losses to add | Plausible, to confirm at TRL 3 | DKH-CAL-001 s7 |
| S11 | A runaway in one bay does not spread to a neighbouring bay for 30 min (R8) | Physics | Thermodynamics | Bounding heat soak: 0.85 MJ (0.7 to 1 MJ of the 1.7 MJ stored) into 7 kg of steel liner of c = 490 J/(kg K) is a 248 K rise if all of it stays in the wall; in practice most leaves with the vented gas and ejecta and the gap between liners is air | Bound 248 K: propagation is plausible and cannot be excluded on paper; the propagation trial decides | Plausible, to confirm at TRL 3 | Open |
| S12 | A condensed-aerosol unit stops the flame of a runaway but not the cells (R7) | Physics | Thermodynamics | Condensed aerosol interrupts flame chemistry in the enclosed volume and does not cool a cell that makes its own heat and oxidiser; the design keeps a vented path and a steel barrier for the cells themselves (DKH-PRC-001 item 9) | Claim restated to flame only; cells are handled by S11 | Within known science | Standard result |
| S13 | The aerosol stays in the bay long enough to act while the vent path is open (R7) | Physics | Fluid mechanics | The roof fans ran on alarm and exchanged the plenum air (90 m3/h), sweeping out the agent; fix DKH-DEC-001 D1: on aerosol discharge the fans stop and the plenum is left to the passive hood slot (240 cm2 free area), which vents by buoyancy | Retention time to measure in the bay mock-up (TRL 4) | Plausible, to confirm at TRL 3 | Open |
| S14 | A 30 m/s gust gives a dynamic pressure of about 550 Pa | Physics | Fluid mechanics | q = 1/2 rho v^2 with rho = 1.225 kg/m3; the 30 m/s gust is the requirement, not a code value for a site (site design wind speed to assess) | claimed 551 Pa, estimate 551 Pa (ratio 1.00) | Within known science | DKH-CAL-001 s11 (551 Pa) |
| S15 | The 1,400 x 1,100 x 300 mm concrete pad weighs about 1,109 kg | Mathematics | Units and dimensional analysis | Volume x 2,400 kg/m3 | claimed 1109 kg, estimate 1.11e+03 kg (ratio 1.00) | Within known science | DKH-CAL-001 s11 |
| S16 | Cabinet, canopy and pad stay upright at a 30 m/s gust (R15) | Physics | Mechanics and statics | Overturning about the pad's rear edge: 0.9 x restoring moment against 1.5 x overturning moment, factor 1.0 needed (a 6 % margin in wind speed); four M12 wedge anchors at 3.8 kN design tension each, 4.13 kN if the same factors (1.5 on wind, 0.9 on weight) are applied to the anchors; wind from the front only | 1.12 factor >= 1 factor | Plausible, to confirm at TRL 3 | DKH-CAL-001 s11 (7.15 kN m restoring, 3.84 kN m overturning) |
| S17 | The lowest canopy point over the sidewalk is 2.1 m or more above it (R13) | Engineering and technology | Standards practice | Canopy rail height from the model: panel tilted 10 degrees, lowest rail point outside the footprint 2,171 mm | 2171 mm >= 2100 mm | Plausible, to confirm at TRL 3 | DKH-CAL-001 s9; cad/src/model.py |
| S18 | A pack is never charged outside its 0 to 45 C window | Chemistry | Electrochemistry and batteries | Lithium-ion cells plate lithium on the anode when charged cold and age fast when charged hot; the SwapCell v0.3 pack reports its window on CAN and the charger contactor opens outside it (SWC-PRC-001 v0.3, SWC-CAL-001) | Standard cell behaviour; window enforced by pack and controller | Within known science | DKH-CAL-001 s7 |
| S19 | Zinc-coated steel panels, powder coat, stainless anchors and plated fasteners last 10 years on a sidewalk with road salt | Chemistry | Materials and polymer chemistry | Zinc corrodes slowly under powder coat; cut edges, rivet holes and the zinc-to-stainless couple at anchors and fixings are the weak points and are sealed or separated by gaskets and washers (DKH-DDR-003); service life is not calculable | Coating and fastener life to qualify on a sample cabinet | Plausible, to confirm at TRL 3 | Open |
| S20 | Aerosol residue after a discharge does not damage the electronics beyond a clean-up | Chemistry | Materials and polymer chemistry | Condensed-aerosol residues are fine, slightly conductive and hygroscopic salts; the bay compartments are separate from the technical compartment and the residue is wiped off the bay (DKH-PRC-001 item 9) | Residue behaviour to check against the unit's data sheet when bought | Plausible, to confirm at TRL 3 | Open |
| S21 | A rider lifts a 2.85 kg pack one-handed with no strain | Biology | Human factors and ergonomics | Far below the 23 kg load constant of the revised NIOSH lifting equation (NIOSH Publication 94-110, value to confirm; the equation covers two-handed lifts and a one-handed limit is not cited, the margin is a factor of eight); lift height 0.73 to 1.10 m is within the favourable band | 2.85 kg <= 23 kg | Within known science | DKH-CAL-001 s9 |
| S22 | Every operable part lies within the 0.38 to 1.22 m reach range (R11) | Biology | Human factors and ergonomics | US ADA forward reach range for a seated or standing user, 15 to 48 in; the highest operable part is the pack handle top at 1,105 mm | 1.105 m <= 1.22 m | Within known science | DKH-CAL-001 s9 (0.73 to 1.10 m) |
| S23 | Fumes of a runaway in a bay do not reach the rider at the front | Biology | Toxicology and exposure | Gas leaves by a plenum to a rear roof hood, away from the street side; the bay door is locked during an alarm (DKH-DDR-002); an enclosed 468 Wh pack makes toxic gas (HF is the usual concern) and the concentration at the door is not calculated | Dispersion and a leak path at the door seal to assess | Plausible, to confirm at TRL 3 | Open |
| S24 | One CAN channel per bay at 250 kbit/s carries the dock traffic at under 3 % load (1.8 % in the script, 2.2 % with worst-case bit stuffing) | Engineering and technology | Standards practice | Frames per second x about 160 bits per worst-case extended frame with stuffing / bit rate | claimed 1.8 %, estimate 2.18 % (ratio 0.82) | Within known science | DKH-CAL-001 s9 (1.8 %) |
| S25 | Electronic detection latency is within the 10 s the fire requirement allows (R7) | Engineering and technology | Standards practice | Electronic latency 3.1 s (1 s sample, 2 s confirm, 0.1 s loop); the sensor response comes on top (S26) | 3.1 s <= 10 s | Within known science | DKH-CAL-001 s8 |
| S28 | The charge contactor opens within the 1 s after detection that R7 allows | Engineering and technology | Standards practice | Decision 0.10 s plus contactor drop-out 0.05 s | 0.15 s <= 1 s | Within known science | DKH-CAL-001 s8 |
| S29 | Vent gas collecting in the plenum, with the fans stopped by fix D1, does not ignite or explode | Physics | Fluid mechanics | Unburnt cell gas is flammable and can burn violently after the flame is out; with the fans stopped the passive hood slot (240 cm2) is the only vent, and no explosion-venting area is calculated (raised by the independent review) | Gas build-up and venting area to assess; the trade-off against S13 goes to Amish (DKH-DEC-001 O4) | Plausible, to confirm at TRL 3 | Open |
| S26 | The sensors respond within the remaining 6.9 s | Engineering and technology | Manufacturing tolerances | Thermal lag of the NTC and detector in the bay air, and smoke entry time, are not in the calculation; vendor data needed | To assess when the sensors are chosen | Plausible, to confirm at TRL 3 | Open |
| S27 | The cabinet reaches IP54 with vent slots, a filtered intake and the roof hood (R9) | Engineering and technology | Standards practice | IP54 is dust-protected and splash-proof; a hood with a rain lip, a gasketed door set and a filtered intake can meet it, but the rating comes from a test, not a calculation | Enclosure test (IEC 60529) at TRL 4 | Plausible, to confirm at TRL 3 | Open |
<!-- /STM_TABLE -->

Verdicts: **Within known science**, **Plausible, to confirm at TRL 3**, **Fails, fix proposed**, **Fails**.

## Fixes made under the standing instruction

| Item | What failed | Fix (DKH-DEC-001) | Result |
| --- | --- | --- | --- |
| Aerosol retention | The roof fans ran on every alarm to vent gas (90 m3/h through the plenum). A condensed-aerosol unit works only while its agent stays in the compartment, so the fans would have blown the agent out within about a minute and left the flame free to burn | D1: on aerosol discharge the controller stops both fans and leaves the plenum to the passive hood slot (240 cm2 free area), which still vents hot gas by buoyancy; fans restart only on a technician's reset. No part, price or dimension changes | S13 plausible: retention time to measure in a bay mock-up at TRL 4. S29 added: with the fans stopped, unburnt gas can collect in the plenum; the alternative (fans off for a fixed hold, then restarted) is Amish's choice (DKH-DEC-001 O4). R7 is unchanged (detection and contactor times do not depend on the fans) |

The fix does not change the working principle, the pitch or the scope; its safety trade-off (S29) is not decided here. It is recorded in DKH-DEC-001 as decided under Amish's standing instruction of 2026-10-23, and he can reverse it.

Two items were restated, not failed. S12 originally read "the aerosol unit stops a runaway"; it stops flame, not cells, so the claim now says so and the cells are handled by the steel barrier (S11). S9 and S11 are the two rows behind R9 and R8, which the requirements already list as at risk.

## Fields not relevant

None. Every field is touched: physics (charging, heat, wind, statics), chemistry (cell charge window, corrosion, aerosol residue), biology (lifting, reach, fumes), mathematics (units, orders of magnitude, throughput ceiling) and engineering (data bus, detection latency, enclosure rating).

## Concept options

- Option A, swap bays in a steel cabinet (the current design): the rows above.
- Option B, rotary magazine behind one hatch: within known science in principle (indexing turrets are standard); the motor-indexed turret needs power and data across a rotating joint (a slip ring or a flexible lead that winds up), which is plausible, to confirm. A runaway in the turret has no steel wall between packs but the pockets, so S11 is worse for B.
- Option C, locker bank, charge in place: within known science (each rider charges their own pack in a locker, so no pool and no canopy). Charging unattended in lockers puts a rider's pack, of unknown history, in the station, so the fire rows S11 to S13 stay open and the pack-health gate cannot rely on a station-owned pool.

## Independent review

A second reviewer (`claude -p --model claude-opus-5-5`, run headless on 2026-10-31 with read-only access to this document, the calculation note DKH-CAL-001, the product requirements DKH-PRS-001 and `sizing.py`, and none of the author's reasoning) was asked to refute every "Within known science" row and recompute the headline numbers by hand. It could not run `sizing.py` (it imports the CAD model) and worked from the printed values. What it found and what changed:

| Item | Finding | Change |
| --- | --- | --- |
| S1, S2, S14, S15, S22 | Upheld | S2 now says "at 25 C" |
| S3 | Upheld; one bay is always empty, so 1.25 kW is an upper bound | Wording says upper bound |
| S4 | Weakened: the script's losses close the balance by subtraction | Losses stated independently (10 % charger, 5 % cells give 0.80 and 0.40 kWh, which agree) |
| S5 | Refuted as worded: 1.38 kWh is the MPPT output, only 0.74 kWh reaches the packs | Wording corrected |
| S6 | Weakened: 36 assumes packs released full; 55 at the adopted 80 % release; 24 with one bay out | Both ceilings stated |
| S7 | Weakened: every step time is an assumption | Downgraded to plausible |
| S8 | Weakened: 4.22 K reproduced but assumes half the fan flow and a windy outside film; 8.7 K with the fans off, about 5.5 K in still air | Downgraded to plausible; still-air and fan-failure cases to add to DKH-CAL-001 |
| S9 | Verdict right, number optimistic: closed-bay heat path and warm returned packs not modelled | Text says the true limit may be lower; stays plausible, PR-009 at risk |
| S10 | Weakened: the 30 W includes fan power; vent losses ignored; cold limit nearer 0 C | Downgraded to plausible |
| S12 and fix D1 | Upheld in science, but the fix keeps unburnt vent gas in the plenum, which can burn violently once the flame is out | New S29 (plausible), FMEA F11, PR-017 and decision O4 to Amish; not decided here |
| S16 and anchors | Weakened: the pad check reproduces (1.12, a 6 % margin in wind speed), but applying 1.5 on wind and 0.9 on weight to the anchors gives 4.13 kN, not 3.79 kN; only frontal wind is checked; pad edge pressure about 19 kPa unfactored (about 61 kPa factored), not 8.4 kPa | `sizing.py` prints the 4.13 kN and edge-pressure figures as a sensitivity; the BOM line 17 rating asked for goes to Amish as O5 (4.2 kN); other wind directions and soil bearing are listed as open |
| S18 | Weakened: charging at 0.5C between 0 and 10 C can still plate lithium | Carried as an open item for the SwapCell project (low-temperature current derating) |
| S21 | Weakened: the NIOSH equation is for two-handed lifts | Wording says so; the factor-of-eight margin stands |
| S24 | Weakened: worst-case stuffing gives 2.2 %, not under 2 % | Claim restated as under 3 % |
| S25 | Weakened: R7 sets two limits | Split into S25 (detection, 3.1 s of 10 s) and S28 (contactor, 0.15 s of 1 s) |
| PR-006 | Weakened: 9.3 % is at the pack terminals; at the inputs (0.77 kWh panel against 8.04 kWh grid to chargers) it is 8.7 %, at one clear design day | PR-006 status states both bases; the definition goes to Amish as O6 |
| PR-005 | Weakened: a 10 % low mains voltage gives 12.2 A on constant-power chargers | Stated in PR-005 status; low-voltage case to add to DKH-CAL-001 |
| PR-015 | The files disagree and "intact" is never checked (panel clamps, roof pull-through at 1,251 N per post) | PR-015 status says upright only; intact not yet checked |
| PR-007 and PR-017 | Conflict: vent to the roof louver versus fans stopped | PR-017 now says the vent path is the passive hood slot; PR-007 is read with it |
| PR-009 | IP54 missing from its status | Added |
| Document wording | Dates and counts | Document dates moved to 2026-10-31, the date the sources were accessed |
| Missing | Wind from other directions, snow and ice on the canopy, condensation in the cold, low-voltage and inrush, throughput with random arrivals, canopy fixings | Carried as open items in the review note; none is calculated at TRL 3 |

The reviewer would also call S16 and S9 not met at their stated margins. They stay plausible and the matching requirements (PR-009, PR-015) are shown with their qualifications.

## Sources

- SwapCell project, SWC-PRC-001 v0.3 and SWC-CAL-001 (pack: 46.8 V nominal, 468 Wh, 54.6 V 5 A charge, 0 to 45 C charge window, thermal constant 32 min), the portfolio's pack and interface definition.
- NIOSH, *Applications Manual for the Revised NIOSH Lifting Equation*, Publication 94-110 (23 kg load constant). The load constant is quoted from memory of the standard; the page could not be fetched on 2026-10-31, so it is **to confirm** (S21). The margin is a factor of eight, so the verdict does not depend on it.
- US Access Board, *Guide to the ADA Standards, Chapter 3: Operable Parts* (unobstructed reach 15 to 48 in above the floor), https://www.access-board.gov/ada/guides/chapter-3-operable-parts/, accessed 2026-10-31 (S22).
- IEC 60529, degrees of protection provided by enclosures (IP code), named for the later enclosure test (S27); its text has not been read for this document.
- Steel specific heat of 490 J/(kg K) and aerosol residue behaviour are textbook and data-sheet values to replace with the supplier's data for the unit and steel chosen (S11, S20).
