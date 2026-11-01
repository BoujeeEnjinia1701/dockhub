---
doc_id: DKH-DDR-004
title: DockHub concept selection
project: DockHub
doc_type: Design decision record
version: "0.1"
status: Draft
date: 2026-10-31
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-31
    author: Amish Chadha
    change: Concept options scored at the kit 1.9.1 upgrade; option A recommended; proposed, awaiting Amish
---

# 0004: Concept selection

- **Date:** 2026-10-31
- **Status:** proposed. Awaiting Amish. Nothing is recorded as decided here.

## Context

Kit 1.8 asks every repo for at least two concept options with different working principles, scored against the user requirements (DKH-URS-001). DockHub was designed before the kit, so its current design is option A and is not redesigned without Amish's go. Options B and C were added and modelled to D3 in `cad/src/model.py` (DKH-OPT-001).

## Options considered

- **A, swap bays in a steel cabinet:** four bays in a row, a compartment, door and charger each, tap, return, take. Score 120 of 155.
- **B, rotary magazine behind one hatch:** a motor-indexed turret of four pockets behind one hatch. Score 102.
- **C, locker bank, charge in place:** six lockers; riders charge their own packs; no pool and no canopy. Score 90.

A leads B by 15 %, so the 10 % rule does not send both to Amish.

## Decision

Recommended, awaiting Amish: carry **option A**. The precis, requirements, calculations, drawing, BOM and build plan keep describing A. B and C stay in the model as alternatives; B is the one to revisit if the propagation trial favours a magazine or if a single hatch matters more than the extra moving parts.

## Consequences

If Amish accepts A, `concept_chosen` in `project.yaml` changes from "A (proposed)" to "A" and DKH-DEC-001 records the date. If he prefers B or C, a new precis, calculation note and build plan are needed; that is a TRL 2 redo for the option and is not started.
