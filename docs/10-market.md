---
doc_id: DKH-MKT-001
title: DockHub market and viability
project: DockHub
doc_type: Market and viability
version: "0.1"
status: Draft
date: 2026-10-31
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-31
    author: Amish Chadha
    change: First market and viability note at the kit 1.9.1 upgrade; prices and benchmarks checked 2026-10-31; no competitor station price is published, so those entries are to assess
---

# DockHub market and viability

DockHub is for delivery-worker groups, courier and cargo-trike fleets, and cities that want a safe alternative to charging packs at home. Commercial swap networks prove demand: New York City's Department of Transportation (DOT) announced a citywide public network of 25 flagship sites on 2025-11-18, with first cabinet installations planned for 2027 and access by paid membership whose price DOT has not stated, and Swobbee's own pilot has logged about 150,000 swaps (CleanTechnica, 2026-02-28). All of those networks are closed: the operator owns pack, cabinet and protocol. An open cabinet built to the SwapCell interface is the gap. No competitor publishes a cabinet or swap price, so the competitive price entries below are **to assess**, and nothing here is invented. Prices and benchmarks were checked 2026-10-31. Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Delivery-worker groups and cooperatives | App-based delivery riders in dense cities, New York City first (DKH-DEC-001) | NYC DOT public network: membership, price not yet stated (2025-11-18); Swobbee station 30 slots, 500 swaps a day, subscription, "contact for pricing" (Levy Electric listing) | 1,519 in parts with two bays fitted and the pad; 1,743 with four bays; packs excluded (bom/bom.csv) | An open cabinet a group can own and run, with packs not locked to one operator |
| Courier and cargo-trike fleets | Depots and loading zones | Gogoro GoStation 24 slots, 1,000 swaps a day capacity, subscription, "contact for pricing" (Levy Electric listing) | As above | Uptime without a second pack per vehicle; pack health data from the CAN log |
| Cities and fire departments | Plazas and sidewalks | Public network cabinets certified to applicable UL standards (NYC DOT, 2025-11-18); costs not stated | As above, plus certification (to assess) | An inspectable, documented design that replaces home charging |
| Emerging-market moto-taxi hubs | Informal transport hubs | Gogoro Network Flex plan, Taiwan, 2019 open beta: TWD 299 a month plus TWD 2.3 per Ah used | As above | Low-cost energy without owning the battery; a 2019 price in another market, shown only for scale |

Running cost: the grid energy of a swap is about USD 0.09 at an assumed USD 0.20 per kWh (DKH-CAL-001 s5, 8.76 kWh for 20 swaps). Revenue, pack cost recovery (USD 414 per pack, three to four packs per station) and membership pricing are **to assess** with a partner.

The viability question is not physics, which DKH-CAL-001 closes on paper, but certification and pack supply. The cabinet is USD 319 over its USD 1,200 target and the fire certification route is unconfirmed (DKH-REG-001 G1), so the first viable route is a private-property pilot with a partner who owns the packs.

## Open route

A sheet metal shop builds the cabinet from the drawings and build plan; a cooperative or fleet installs it on private land with an electrician; the SwapCell project supplies the packs and interface. CERN-OHL-S keeps changes open. The packs are the valuable part (USD 414 each), so the cabinet is the thing to share.

## Sources

- NYC Department of Transportation, press release, 2025-11-18, https://www.nyc.gov/html/dot/html/pr2025/install-public-e-bike-battery-swapping-network-citywide.shtml (checked 2026-10-31): 25 flagship sites, paid membership, price not stated, first installations 2027.
- CleanTechnica, "Battery Swapping Expands In New York City", 2026-02-28, https://cleantechnica.com/2026/02/28/battery-swapping-expands-in-new-york-city/ (checked 2026-10-31): pilot of five stations, about 150,000 swaps by Swobbee since March 2025, no price.
- Levy Electric, Swobbee battery swapping station, https://fleets.levyelectric.com/docking-stations/swobbee-battery-swapping-station (checked 2026-10-31): 30 slots, 500 swaps a day, 11,000 W, "Contact for Pricing".
- Levy Electric, Gogoro GoStation, https://fleets.levyelectric.com/docking-stations/gogoro-gostation (checked 2026-10-31): 24 slots, 1,000 swaps a day capacity, "Contact for Pricing".
- Gogoro, "Gogoro Network Flex Plan", 2019-09-19, https://www.gogoro.com/news/gogoro-network-flex-plan/ (checked 2026-10-31): TWD 299 a month and TWD 2.3 per Ah; no conversion to USD is made here.
- Electricity price of USD 0.20 per kWh is an assumption in DKH-CAL-001, not a checked tariff.
