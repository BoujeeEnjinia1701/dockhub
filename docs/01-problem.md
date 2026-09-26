---
doc_id: DKH-PRB-001
title: DockHub problem statement
project: DockHub
doc_type: Problem statement
version: "0.3"
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
  change: Populate to TRL 2 (problem, users, context, constraints, prior work)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. Budget scope (four-bay cabinet, two bays fitted) and SwapCell interface v0.3 per DKH-DDR-001; open questions updated from DKH-CAL-001
---

# DockHub problem statement

Riders who earn a living on light electric vehicles have two poor ways to recharge: wait hours at a socket, or take the battery home and charge it overnight in a flat, hostel or shared room. The first costs working time; the second is a leading cause of lithium-ion battery fires in homes. A shared, monitored place to exchange a flat pack for a charged one would address both.

## The problem

Light electric vehicle packs take hours to charge. India's draft battery swapping policy notes that "regular charging takes at least 3 to 4 hours" for electric two- and three-wheelers, while a swap "is done in minutes" ([NITI Aayog, draft battery swapping policy, April 2022](https://www.niti.gov.in/sites/default/files/2022-04/20220420_Battery_Swapping_Policy_Draft_0.pdf)). A delivery rider on a single pack must either stop work for that time or carry a second pack and charge it wherever they sleep.

Charging at home is where the fire risk sits. The US Consumer Product Safety Commission found 227 micromobility battery incidents from 2019 to 2023, associated with 39 deaths and 181 injuries; 120 of those incidents happened during charging ([Federal Register, 24 June 2026](https://www.federalregister.gov/documents/2026/06/24/2026-12749/safety-standard-for-lithium-ion-batteries-used-in-micromobility-products-and-electrical-systems-of)). New York City recorded 268 lithium-ion battery fires and 18 deaths in 2023, and 277 fires in 2024 ([FDNY](https://www.nyc.gov/site/fdny/news/03-25/fdny-commissioner-robert-s-tucker-significant-progress-the-battle-against-lithium-ion)). London Fire Brigade attended a record 206 e-bike and e-scooter fires in 2025; each of the five people killed in such fires in London since 2023 did not own the e-bike involved ([London Fire Brigade](https://www.london-fire.gov.uk/news/2026-news/january/record-number-of-e-bike-and-e-scooter-fires-across-london-in-2025-as-brigade-calls-for-regulation-to-be-introduced)). The people at risk include neighbors and family, not only riders.

Commercial swap networks exist, but each is closed: the pack, cabinet, protocol and data belong to one operator, and a rider or small fleet is locked into that operator's batteries. The portfolio's SwapCell project defines an open pack and interface. What is missing is an open, street-side cabinet that stores, charges, checks and hands out those packs, which a city, a cooperative of riders or a small fleet could build and run.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| App-based delivery rider | A charged pack in under a minute, near the delivery zone, at any hour; no pack in the bedroom overnight | Dense city centers; long shifts, often evenings and weekends |
| Cargo trike and courier fleet operator | Predictable uptime without buying a second pack per vehicle; pack health data | Depots and curbside loading zones |
| Moto-taxi or e-scooter rider in emerging markets | Low-cost energy without owning the battery | Informal transport hubs, markets |
| City transport or fire safety department | Fewer home battery fires; a safe, visible alternative that uses little sidewalk | Sidewalks, plazas, parking lanes |
| Host (shop, restaurant, building owner) | Low-effort hosting with a clear electrical load and safety case | Shopfronts, parking areas with a power supply |
| Technician | Replace a charger, lock or bay in minutes; read pack logs | Field service with hand tools |

## Operating environment

- Outdoor, on a sidewalk or plaza, exposed to rain, dust, sun and road salt; ambient roughly -10 to 45 °C (14 to 113 °F).
- Unattended around the clock, in public, so exposed to vandalism and theft.
- Fed from a single-phase supply of the kind available at a shopfront or streetlight cabinet (120 V or 230 V).
- Used by people with gloves, in the dark, in a hurry, and with a range of languages and abilities.

## Constraints

- Garage-buildable prototype, about $1,200 USD in parts for the four-bay cabinet with two bays fitted, excluding SwapCell packs (DKH-DDR-001 item 1, adopted for TRL 3 and open for Amish's review).
- Built from folded sheet steel, off-the-shelf certified chargers and hobby-grade controllers; no custom mains electronics.
- Must build to SwapCell interface v0.3 (envelope, coded connector, latch class, CAN message set) without changing it; conflicts are raised with the SwapCell project.
- No cameras or microphones. The station records pack identity, energy and a rider token, not personal data beyond what access requires.
- Siting on public land needs permission from the city and the power utility; the prototype is for a private forecourt or a supervised pilot.

## Out of scope

- Payment processing and pricing (the concept provides an access token only).
- Charging of non-SwapCell batteries, or of whole vehicles.
- Cars, motorcycles or any vehicle needing packs larger than one SwapCell double pack.
- Fleet routing, rebalancing of packs between stations and a multi-station back end beyond a simple log export.

## Prior work

- Closed commercial swap networks prove the model at scale. Ampersand reports more than 10,000 electric motorcycles and 20,000 battery swaps a day in Rwanda and Kenya ([Ampersand](https://www.ampersand.energy/)). Swobbee runs 24/7 swap stations for delivery riders in Berlin and New York City ([Swobbee](https://www.swobbee.com/)). Gogoro operates a scooter swap network in Taiwan and has announced expansions to markets including Chile, Korea, Singapore and the Philippines ([Gogoro news](https://www.gogoro.com/news/)).
- India's draft policy asks for interoperable, BMS-enabled packs with remote monitoring and for open ecosystems that let "other market players" build compatible products ([NITI Aayog, 2022](https://www.niti.gov.in/sites/default/files/2022-04/20220420_Battery_Swapping_Policy_Draft_0.pdf)).
- SwapCell (portfolio) defines the pack, blind-mate connector, CAN heartbeat and in-pack state-of-health log that DockHub builds on. Its single-pack wall dock is the pattern for each DockHub bay.

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design

## Open questions

- Which first site and partner: a rider cooperative or workers' center in a high-income city, or a moto-taxi hub in East Africa? Proposed, awaiting Amish.
- Who owns the packs in circulation: the station operator (subscription), the riders (deposit and exchange) or a fleet? This drives cost and the access design. Proposed, awaiting Amish.
- How far do riders travel in a shift, and how many swaps a day does one station need to serve, at what hours? The 20 swaps a day and the lunch and dinner peaks used in DKH-CAL-001 are assumptions to test.
- How long will a rider wait for a charged pack before leaving? DKH-CAL-001 assumes 15 min.
- How hot does the first pilot site get? The SwapCell pack does not charge above 45 °C, so in hot afternoons DockHub pauses charging (DKH-CAL-001 section 7).
