# DockHub

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Smart Cities · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $1,200 USD · **Difficulty:** 4 of 5

A street-side battery swap and charging station for SwapCell packs, serving e-bikes, cargo trikes and delivery riders with charged batteries in seconds.

## Concept rationale

Swapping moves charging out of homes and into a monitored cabinet, improving both safety and rider income.

## Burning platform

Battery fires from charging e-bikes indoors have become a public safety issue in several major cities.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. It builds on SwapCell.

## Problem

Light electric vehicle riders lose working time to charging, and charging lithium packs in homes and hostels causes fires.

## Concept

A street-side battery swap and charging station for SwapCell packs, serving e-bikes, cargo trikes and delivery riders with charged batteries in seconds.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Lockable charging cabinet with SwapCell bays
- Chargers with per-bay protection
- Solar canopy and grid input
- Access controller and app
- Fire detection and suppression

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Lithium cells can overheat, vent and burn. Use protected cells or LiFePO4, fuse every pack, charge only within the cell maker's limits and never leave a first build charging unattended. Mains wiring must be done or checked by a qualified electrician and follow local electrical code. Include fire detection and venting in every cabinet.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (DKH-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `DKH-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Smart cities set.
