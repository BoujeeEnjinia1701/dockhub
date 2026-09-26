# Review note: DockHub

## Session 2026-09-25: TRL 3

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (DKH-DDR-001 v0.1): the nine TRL 2 points that carried a recommendation are adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review; four items remain open.
- `docs/04-calcs/01-sizing.md` (DKH-CAL-001 v0.1) with `docs/04-calcs/sizing.py` and `docs/04-calcs/results.csv`: charging, swap time, a minute-step day model for throughput and solar share, daily energy, grid current with power factor, cabinet and pack thermal, fire detection latency and vent path, reach and footprint geometry, CAN load, mass, wind and anchoring, and cost, with a results table for R1 to R16.
- `cad/src/model.py`: parametric build123d model (cabinet, bays with SwapCell v0.3 cradle, guides, class D catch and coded receptacle, reference packs with plug, handle and latch pawl, chargers, controller, access panel, grid unit, fire unit, plenum with fans and louver, canopy, flush plinth with anchor holes, service door). `bays_fitted` switches between the two-bay prototype and the four-bay fit. Exports `cad/step/` and `cad/stl/` (`dockhub-assembly`, `dockhub-assembly-4-bays`, `dockhub-cabinet`, `dockhub-bay`, `dockhub-canopy`); clash check finds none in either fit.
- `cad/src/sheets.py` and `cad/drawings/DKH-DWG-001.svg`, `.pdf`, `.png`: general arrangement of the first prototype (bays 1 and 2 fitted) at Rev P1, marked not for fabrication. DKH-DWG-001 was free because the concept blueprint uses DKH-DWG-010.
- `bom/bom.csv` (16 lines, every line priced with a supplier type) and `bom/bom-notes.md`, now for the two-bay fit.
- `cad/src/concept_media.py` now builds from `model.py` (four-bay fit, three packs, one empty bay); hero, blueprint, cutaway, exploded, flow, `model.glb` and `viewer.html` regenerated and checked by eye; temporary `media/_views*` folders deleted. The kit's cutaway works as is because the model is centered on the origin.
- `docs/01-problem.md`, `docs/02-concept.md` and `docs/03-requirements.md` moved to v0.3 with the adopted items, SwapCell interface v0.3 and numbers from DKH-CAL-001. `project.yaml`: trl 3, trl_target 3, trl_evidence updated; `budget_usd` unchanged at 1200. `README.md`: TRL badge, links, concept numbers, components, BOM and safety text.

### Requirements (DKH-CAL-001)

| ID | Result | Status |
| --- | --- | --- |
| R6 | 9.3 % of charging energy from the canopy (0.74 of 1.38 kWh used); 11.4 % if flat packs are routed to bay 1 in daylight, which turns one rider in 20 away | **Not met** (target relaxed to 10 %) |
| R9 | The pack refuses charge above 45 °C; charging pauses above about 29 to 39 °C ambient and for cold-soaked packs below about -1 °C | **Not met** |
| R8 | Containment needs a propagation test | At risk (not verifiable at TRL 3) |
| R15 | 2.91 kN·m overturning against 0.50 kN·m self-weight; four anchors of 3.8 kN design tension each and a pad, neither chosen | At risk |
| R16 | $1,199 against $1,200 with two of four bays fitted | At risk |
| R7, R14 | Detection latency 3.1 s and contactor 0.15 s on paper; 15 min part swap needs a trial | Not verifiable at TRL 3 |
| R1, R3, R4, R5, R11, R13 | 31 s swap; 1.2 h and 2.3 h charge; 20 of 20 served with four bays; 1.25 kW, 11.0 A at 120 V with power factor 0.95; reach 0.73 to 1.10 m; 1.0 x 0.5 m, canopy 2.18 m clear | Met |
| R2, R10, R12 | SwapCell v0.3 interface, security features, data | Met (design review) |

Counts: 2 not met, 3 at risk, 2 not verifiable at TRL 3, 9 met.

Findings that change the TRL 2 picture:

- A swap needs an empty bay, so *n* bays hold *n* - 1 packs. Four bays give 36 swaps a day at most (TRL 2 said 38). The adopted two-bay prototype holds one pack and serves only 9 of the 20 duty-case swaps: it can demonstrate the station but not run the duty case.
- R5 holds only with power-factor-corrected chargers; at a power factor of 0.6 four chargers draw 17.2 A at 120 V. Line 5 of the BOM now specifies 0.9 or better.
- The cabinet air rises only about 4 to 5 K, not 10 K, but R9 is set by the pack's own 45 °C charge limit, so shading cannot fix it.
- Mass is about 205 kg (prototype, no packs) to 234 kg (four bays, three packs), not 150 to 170 kg.
- Wind: the canopy force is mostly uplift (1,590 N); overturning is 2.91 kN·m, not 3.6 kN·m, but the cabinet still tips and slides without anchors. Front canopy posts pull about 1.25 kN each on the roof frame.
- The TRL 2 plinth (1,020 x 520 mm) broke the 1.0 m width limit of R13; it is now flush with the body.
- SwapCell pack price is $414 (SWC-CAL-001), not $370.

### Decisions recorded (DKH-DDR-001)

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review: build the four-bay cabinet and fit two bays for the first prototype, with `budget_usd` unchanged at $1,200 and redefined to that fit (option (b), $1,450, was not recommended and is not adopted); keep the 400 W canopy and relax R6 to 10 %; four bays in one row; one charger and CAN channel per bay; per-bay steel compartments with a rear plenum; doors locked during a fire alarm; MPPT to bay 1; offline-first NFC access; a 70 % state-of-health gate. The pitch and problem lines had no recommended rewording, so `project.yaml` and the README pitch are unchanged.

### Still awaiting Amish

- Pack ownership model (no recommendation at TRL 2; to follow co-design).
- First pilot site and partner (no recommendation at TRL 2).
- R6 is still not met at 10 %: accept about 9 %, route packs to bay 1 in daylight and accept occasional waits, feed more bays from the sun, or drop the target. No recommendation made.
- R9 is not met: accept daytime charging pauses in hot climates, add active cooling, narrow the design ambient, or raise the charge temperature limit with SwapCell. No recommendation made.
- Whether a two-bay first prototype that cannot run the duty case is acceptable.
- Engineering proposals from this session (DKH-DDR-001 items 12 and 13): SwapCell interface v0.3, an 80 % release level, chargers with a power factor of 0.9 or better, the flush plinth, and the demand profile and 15 min rider patience used in the day model.

### Safety concerns

- Lithium-ion packs of 468 Wh beside a public walkway; fire containment between bays (R8) is unproven and needs a propagation test, which is TRL 4 work and on hold.
- The canopy lifts and tips the cabinet in a 30 m/s gust. Anchors of at least 3.8 kN design tension each into a concrete pad are mandatory, and the canopy posts must bolt through to a roof frame. The pad and anchors are not in the BOM.
- Chargers without power factor correction can overload a 120 V branch circuit.
- A pack can deliver about 500 A into a short; each bay's DC line needs a 60 V DC fuse with at least 1 kA breaking capacity (now in BOM line 16).
- Charging stops in hot weather by design (pack limit 45 °C); the controller must never override that.
- The cabinet weighs about 205 kg empty; it must be moved with lifting equipment.

### Problems and notes

- Shared components: DockHub depends on none of FieldNode, CellGuard, MotionCore, ThermaCart, TwinKit or CalRig; TwinKit stays a later suggestion. SwapCell (reference repo, read-only) is at interface v0.3; DockHub now builds to it, and no conflict was found. The observation that multi-pack hosts need a CAN channel per bay or unique node numbers stands; v0.3 allows node numbers 0 to 7 but packs default to 0.
- The 2 s return check in the swap time depends on how fast a sleeping pack wakes on the coded INTERLOCK loop; SwapCell v0.3 gives no wake time. Worth raising with SwapCell.
- No TRL 4 material exists (`build-log/` holds only its README; `electronics/` and `firmware/` are empty). None was created.
- No unchecked citations were listed at TRL 2, so no WebFetch checks were needed. The README's cited figures are unchanged.
- Process note: during this session one read-only `git status` call was run by mistake (its output was discarded), against the instruction not to run git commands. Nothing was staged, committed or changed by it.

### Recommended next step

TRL 4 is on hold by Amish's instruction, so the next step is a decision, not a build: Amish to review the adopted items in DKH-DDR-001, choose how to handle R6 and R9, decide whether the two-bay first prototype is acceptable, and choose the pack ownership model and first pilot site. For the record only, TRL 4 would need a bench test article of one bay (cradle, coded receptacle, charger, contactor and detection chain), named charger, anchor and aerosol parts with datasheets, a lab test report (TST, environment: lab) covering detection latency and charge pausing, and build log entries; a propagation test for R8 would follow later at an accredited lab.

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (DKH-PRB-001 v0.2): problem with cited fire and charging-time figures, users, operating environment, constraints, out of scope, prior work (Ampersand, Swobbee, Gogoro, India's draft swapping policy, SwapCell), open questions; co-design checklist kept.
- `docs/03-requirements.md` (DKH-REQ-001 v0.2): 16 measurable requirements (R1 to R16) with targets, verification and TRL 2 status, a design duty case and assumptions.
- `docs/02-concept.md` (DKH-PRC-001 v0.2): how it works, 15 numbered components, first-order numbers, eight design choices, relationship to SwapCell, safety section, open questions.
- `cad/src/concept_media.py`: massing model of the cabinet, bays, packs, chargers, controller, access panel, grid input, fire parts, plenum and louver, solar canopy, plinth and service door, in street context (sidewalk, curb, roadway) with the 1.75 m figure.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `model.glb` and `viewer.html`, `exploded.png` (callouts 1 to 15 match the BOM), `cutaway.png`, `flow.png` (daily energy, all values estimates). Temporary `_views` folders removed.
- `bom/bom.csv`: 16 lines with indicative USD prices, numbered to match the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line; Concept rationale, Burning platform, Where it could be used (6 industries, 6 regions), What sparked the idea, Problem, Concept, Key components and Safety expanded with cited sources.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Swap time | about 30 s | R1 met |
| Charge per bay | about 1.2 h (20 to 80 %), 2.3 h full | R3 met |
| Maximum throughput, 4 bays | about 38 swaps a day | R4 met |
| Peak grid draw | about 1.25 kW (10.4 A at 120 V) | R5 met |
| Daily energy at 20 swaps | about 10.1 kWh in, 8.0 kWh stored in packs | |
| Solar share (400 W canopy) | about 1.3 kWh a day, 13 % | **R6 not met** (target 20 %) |
| Interior air at 45 °C ambient | about 55 °C | **R9 not met**: charging derates or pauses |
| Fire containment between bays | not calculated; needs a test | **R8 unverified, at risk** |
| Canopy wind overturning, 30 m/s gust | about 3.6 kN·m against about 0.4 kN·m self-weight | R15 met only if anchored |
| Mass with four packs | about 150 to 170 kg | |
| Parts cost, packs excluded | about $1,423 (4 bays fitted); about $1,199 (2 of 4 fitted) | **R16 not met with 4 bays** |

Requirements not met or at risk: R6 (solar share), R9 (charging at 45 °C ambient), R8 (fire containment unproven), R16 (cost with four bays). R15 depends on anchoring to a concrete pad that is not in the BOM.

### Proposed, awaiting Amish

1. **Budget (R16).** Options: (a) build the four-bay cabinet but fit two bays for the first prototype, about $1,199; (b) raise `budget_usd` to $1,450; (c) a two-bay cabinet. Recommendation: (a). `project.yaml` is unchanged.
2. **Solar target (R6).** Options: keep the 400 W canopy as shade and supplement and relax R6 to 10 %; drop the canopy; or add an off-cabinet array. Recommendation: relax R6 to 10 %.
3. **Pack ownership model:** station-owned pool, rider-owned one-for-one exchange, or fleet packs. The pack pool (about $370 per pack) costs far more than the station. No recommendation until co-design.
4. Four bays in one row at hand height rather than eight in two rows.
5. One certified charger and one CAN channel per bay rather than a shared charger matrix.
6. Separate steel compartment per bay with a rear plenum venting through the roof.
7. Bay doors stay locked during a fire alarm.
8. Solar through an MPPT controller to bay 1 rather than a hybrid inverter.
9. Offline-first NFC access with an optional app.
10. State-of-health gate at 70 % for releasing packs to riders.
11. First pilot site and partner (a delivery-worker group in a high-income city, or a moto-taxi hub in East Africa).
12. `project.yaml` pitch and problem were checked against the sources and left unchanged.

### Safety concerns

- Up to four 468 Wh lithium-ion packs beside a public walkway. Fire containment between bays (R8) is unproven and can only be shown by a propagation test at TRL 4 or later; the aerosol unit does not stop a cell in runaway.
- Mains AC in the technical compartment: electrician installation, RCD, per-charger breakers, surge protection, lockable isolator, earth bonding, separation from the 54.6 V DC side.
- Heat: a sunlit cabinet can exceed pack charge limits; the controller must pause charging.
- Wind: the canopy creates an overturning moment several times the cabinet's self-weight resistance; anchoring is mandatory.
- Siting: keep the vent louver away from doors, windows and people; keep a clear pedestrian path.

### Problems and notes

- SwapCell interface observation, raised for that project rather than changed here: several packs on one host collide at node 0 unless each bay has its own CAN channel (as proposed) or packs get unique node numbers.
- TwinKit is mentioned only as a later suggestion for collecting logs.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).
- WebSearch was unavailable this session. Every cited figure was verified by fetching the source page directly. Gogoro network figures and New York's delivery-worker numbers could not be verified and are left out.

### Recommended next step

Review this note and the media, then decide items 1 to 3. If approved, run `/advance-trl3` to check the thermal, wind, energy and throughput estimates by calculation, and produce the parametric model and drawing sheet.
