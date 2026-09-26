---
doc_id: DKH-DDR-001
title: DockHub TRL 2 review decisions
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
  change: Record the TRL 2 review items adopted for TRL 3 under Amish's 2026-09-25 instruction, and the items that remain open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** proposed. The recommendations in items 1 to 9 are adopted for TRL 3 work pending Amish's review; items 10 to 13 remain proposed, awaiting Amish.

## Context

The TRL 2 review note (`docs/REVIEW.md`, session of 2026-09-25) listed twelve points as "Proposed, awaiting Amish". On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed the DockHub points item by item. Under that instruction, every point that carried a recommendation is adopted as recommended so that the TRL 3 calculations, model and drawing can proceed, and each stays open for his review. Points with no recommendation stay "Proposed, awaiting Amish". TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 2 session) and DKH-PRC-001 v0.2, "Key design choices". They are not repeated here.

## Decision

*Table 1. Items adopted for TRL 3.*

| # | Item | Status | Where it now lives |
| --- | --- | --- | --- |
| 1 | Budget (R16): build the four-bay cabinet and fit two bays for the first prototype (option a) | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. `budget_usd` stays at $1,200 and now covers the four-bay cabinet with bays 1 and 2 fitted; SwapCell packs stay excluded | DKH-REQ-001 v0.3 R16, `bom/bom.csv`, `cad/src/model.py` (`bays_fitted`), DKH-DWG-001 |
| 2 | Solar target (R6): keep the 400 W canopy as shade and supplement, and relax R6 from 20 % to 10 % | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | DKH-REQ-001 v0.3 R6, DKH-PRC-001 v0.3 |
| 3 | Four bays in one row at hand height rather than eight in two rows | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | DKH-PRC-001 v0.3, `cad/src/model.py` |
| 4 | One certified charger and one CAN channel per bay rather than a shared charger matrix | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | DKH-PRC-001 v0.3, `bom/bom.csv` lines 5 and 6 |
| 5 | Separate steel compartment per bay with a rear plenum venting through the roof | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | DKH-PRC-001 v0.3, `cad/src/model.py` |
| 6 | Bay doors stay locked during a fire alarm | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | DKH-PRC-001 v0.3 |
| 7 | Solar through an MPPT controller to bay 1 rather than a hybrid inverter | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | DKH-PRC-001 v0.3, `bom/bom.csv` line 13 |
| 8 | Offline-first NFC access with an optional app | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | DKH-PRC-001 v0.3 |
| 9 | State-of-health gate at 70 % for releasing packs to riders | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | DKH-PRC-001 v0.3 |

The TRL 2 review checked the `project.yaml` pitch and problem lines against the sources and left them unchanged; it did not recommend a new wording, so nothing was applied to `project.yaml` or `README.md` under this record.

### Items that remain open

*Table 2. Open items.*

| # | Item | Status |
| --- | --- | --- |
| 10 | Pack ownership model: station-owned pool, rider-owned one-for-one exchange, or fleet packs | Proposed, awaiting Amish. No recommendation was made at TRL 2 (to follow co-design) |
| 11 | First pilot site and partner: a delivery-worker group in a high-income city, or a moto-taxi hub in East Africa | Proposed, awaiting Amish. No recommendation was made at TRL 2 |
| 12 | Building to SwapCell interface v0.3 instead of v0.2 (coded INTERLOCK receptacle, item W; dock host type 1; class D catch, item V). SwapCell issued v0.3 on 2026-09-25 with Amish's approval of its additions; DockHub adopts it because a v0.3 pack stays dead in a receptacle without the 10 kΩ coding resistor | Engineering proposal made at TRL 3, open for Amish's review |
| 13 | TRL 3 engineering proposals in DKH-CAL-001: release a pack at 80 % state of charge or more; chargers with a power factor of 0.9 or better; a flush plinth (1,000 x 500 mm) to keep the footprint inside R13; a 15 min rider patience and the demand profile used in the throughput model | Engineering proposals, awaiting Amish's confirmation |

## Consequences

- R6 is now judged against 10 %. DKH-CAL-001 finds 9.3 % with the service-first release rule, so **R6 is still not met**; routing flat packs into bay 1 in daylight reaches 11.4 % but turns one rider in 20 away at the dinner peak.
- R16 is judged on the two-bay fit: $1,199 against $1,200 (at risk). A two-bay prototype holds only one resident pack, because one bay must always be empty to receive a returned pack. It serves 9 of the 20 duty-case swaps, so it demonstrates the station but cannot run the duty case; R4 is met only by the four-bay fit ($1,423).
- The budget figure in `project.yaml` is unchanged. Option (b) of item 1 ($1,450) was not recommended and is not adopted.
- DockHub cites SwapCell interface v0.3 (item 12). Nothing in the SwapCell interface is changed by DockHub.
