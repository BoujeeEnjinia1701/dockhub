# Review note: DockHub

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
