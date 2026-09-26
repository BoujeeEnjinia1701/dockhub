---
doc_id: DKH-DDR-002
title: DockHub recommendations accepted
project: DockHub
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of all review recommendations, what changed in the repo and the items still open
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted by Amish on 2026-09-25 for every item that carried a recommendation. Items with no recommendation remain proposed, awaiting Amish.

## Context

DKH-DDR-001 and the review note (`docs/REVIEW.md`) listed the TRL 2 review items and the TRL 3 engineering proposals. Items with a recommendation had been adopted for TRL 3 work but stayed open for Amish's review. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item that carried a recommendation is therefore decided as recommended. Where the recommendation named one option among several, that option is the decision. Items with no recommendation are not decided by this record.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item (DKH-DDR-001 number) | Decision | What changed in the repo |
| --- | --- | --- | --- |
| 1 | Budget, R16 (1) | Option (a): build the four-bay cabinet and fit bays 1 and 2 for the first prototype. `budget_usd` stays at $1,200 and covers that fit; SwapCell packs are excluded | Already applied at TRL 3 (`project.yaml`, DKH-REQ-001 R16, `bom/bom.csv`, `cad/src/model.py`, DKH-DWG-001). Status wording updated in DKH-DDR-001 v0.2, DKH-REQ-001 v0.4 and `bom/bom-notes.md`. Budget unchanged: $1,200 before and after |
| 2 | Solar target, R6 (2) | Keep the 400 W canopy as shade and supplement; R6 relaxed from 20 % to 10 % | Already applied in DKH-REQ-001 R6; wording updated in DKH-REQ-001 v0.4 and DKH-PRC-001 v0.4. R6 is still not met (9.3 %) |
| 3 | Bay layout (3) | Four bays in one row at hand height | No change; already in DKH-PRC-001 and `model.py` |
| 4 | Charging architecture (4) | One certified charger and one CAN channel per bay | No change; already in DKH-PRC-001 and BOM lines 5 and 6 |
| 5 | Fire separation (5) | Separate steel compartment per bay with a rear plenum venting through the roof | No change; already in DKH-PRC-001 and `model.py` |
| 6 | Doors during a fire alarm (6) | Bay doors stay locked | No change; already in DKH-PRC-001 |
| 7 | Solar connection (7) | MPPT controller feeding bay 1, no hybrid inverter | No change to the design; DKH-CAL-001 v0.2 now cites the MPPT control rule as decided |
| 8 | Access (8) | Offline-first NFC access with an optional app | No change; already in DKH-PRC-001 |
| 9 | Pack health gate (9) | Hold packs below 70 % state of health | No change; already in DKH-PRC-001 |
| 10 | SwapCell interface (12) | Build to SwapCell interface v0.3 | No change; already cited in DKH-REQ-001 R2 and DKH-PRC-001 |
| 11 | TRL 3 engineering proposals (13) | Release packs at 80 % state of charge or more; chargers with a power factor of 0.9 or better; plinth flush with the body (1,000 x 500 mm); 15 min rider patience and the demand profile of DKH-CAL-001 | No change to numbers; DKH-CAL-001 v0.2 and `sizing.py` now cite the release threshold as decided |
| 12 | Two-bay first prototype that cannot run the duty case (review note, TRL 3 session) | Accepted with item 1: the prototype demonstrates the station with one resident pack; the duty case needs the four-bay fit ($1,423) | Recorded here and in `docs/REVIEW.md` |

No design change follows from these decisions: each was already built into the TRL 3 model, BOM, drawing and calculations. The GA drawing DKH-DWG-001 stays at Rev P1 (regenerated, geometry and notes unchanged), and DKH-CAL-001 results are unchanged.

The TRL 2 review made no recommendation to reword the `project.yaml` pitch or problem, so they are unchanged.

## Items still open

*Table 2. Proposed, awaiting Amish (no recommendation was made).*

| Item | Options |
| --- | --- |
| Pack ownership model (DKH-DDR-001 item 10) | Station-owned pool, rider-owned one-for-one exchange, or fleet packs; to follow co-design |
| First pilot site and partner (DKH-DDR-001 item 11) | A delivery-worker group in a high-income city, or a moto-taxi hub in East Africa |
| How to close R6 (9.3 % against 10 %) | Accept about 9 %, route flat packs to bay 1 in daylight and accept occasional waits, feed more bays from the sun, or drop the target |
| How to close R9 (charging pauses above about 29 to 39 °C ambient) | Accept daytime pauses in hot climates, add active cooling, narrow the design ambient, or raise the charge temperature limit with SwapCell |

## Consequences

- Requirement status is unchanged: R6 and R9 not met; R8, R15 and R16 at risk; R7 and R14 not verifiable at TRL 3; nine met.
- Cross-repo actions (recorded in `docs/REVIEW.md`, not changed here): ask SwapCell for the pack wake time on the coded INTERLOCK loop, which sets the 2 s return check; note for SwapCell that multi-bay hosts need a CAN channel per bay because packs default to node 0.
- TRL 4 work (bench bay, propagation test, anchor and charger selection with datasheets, purchasing) stays on hold by Amish's instruction. `trl` and `trl_target` stay at 3.
