---
doc_id: DKH-REG-001
title: DockHub regulatory and standards register
project: DockHub
doc_type: Regulatory register
version: "0.1"
status: Draft
date: 2026-10-31
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-31
    author: Amish Chadha
    change: First register at the kit 1.9.1 upgrade, researched for the current design (option A) with New York City as the first candidate city (DKH-DEC-001); sources cited with the date checked
---

# DockHub regulatory and standards register

A street-side station that stores and charges lithium-ion packs unattended is regulated mostly through fire, electrical and public-space rules, not through a single product certificate. New York City, the first candidate city, shows the pattern: its Department of Transportation announced in November 2025 a citywide public battery-swapping network of 25 flagship sites, to be placed only in cabinets "properly certified to applicable UL standards" and cleared by the Fire Department (FDNY), with fire suppression, real-time battery health monitoring and automatic alerts. The FDNY guide for battery charging cabinets then sets the certification route (UL 1487 fire testing, a hazard mitigation analysis, a Certificate of Approval and, outdoors, a site survey and a DOT Revocable Consent on public property). The same guide does not mention swapping stations by name, so whether a DockHub cabinet is treated as a charging cabinet or needs its own approval is **to assess** with FDNY. DockHub's first pilot is on private property (DKH-DEC-001), which avoids the street consent but not the fire review. Not legal advice; every row marked "to assess" needs a qualified reviewer, and rules differ by jurisdiction. Nothing here needs certification before TRL 4.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | FDNY Certificate of Approval for battery charging cabinets (TM-2 application, UL 1487 test report, hazard mitigation analysis by a registered design professional); fees listed by FDNY: $625 for the application, $420 for an outdoor site application | New York City | Approval of an enclosure that charges battery packs | The cabinet charges packs in an enclosed cabinet, which the Fire Code allows only with FDNY approval; whether a swap cabinet follows the same route is not stated | Design lead with a registered design professional | To assess with FDNY |
| G2 | UL 1487, battery containment enclosures | United States (cited by FDNY) | Fire containment of a battery enclosure, tested by a national laboratory | The bay compartments and cabinet are a battery containment design; no test planned before TRL 4 | Design lead | Certification needed later |
| G3 | UL 4900, micromobility charging equipment; UL 2849, UL 2272 and UL 2271 for e-bike systems and batteries | United States (cited by FDNY) | Listing of charging equipment and the packs it charges | Chargers and the SwapCell pack should be listed; the pack's listing is the SwapCell project's | SwapCell project; design lead | To assess |
| G4 | NYC DOT public e-bike battery swapping network (announced 2025-11-18): certified cabinets, fire suppression, real-time battery health monitoring, alerts to the system provider; membership access, prices not yet stated | New York City | Rules for cabinets placed on the city's sidewalks | DockHub's design has detection, suppression, health reporting and alerts; certification is the open item | Co-design partner | To assess |
| G5 | NYC DOT Revocable Consent for equipment on public property; FDNY Site Survey Inspection, Letter of No Objection and DOB electrical permit (ED16A) for outdoor installations | New York City | Siting and electrical work | Needed for a public sidewalk site, not for the first private pilot's circuit review beyond the electrical permit | Co-design partner | To assess; first pilot on private property |
| G6 | NFPA 855, installation of stationary energy storage systems; UL 9540A, thermal runaway propagation test method | United States (named by number; texts not consulted) | Spacing, protection and a propagation test for battery storage | The aerosol versus vermiculite trial (DKH-DEC-001) aims at a UL 9540A style unit-level test before an accredited lab; applicability of NFPA 855 to about 2 kWh of packs is unknown | Design lead | To assess |
| G7 | NFPA 70 (National Electrical Code) and local electrical rules; the grid input is a single circuit with an RCBO | United States (named by number; text not consulted) | Wiring, protection, outdoor equipment | One 120 V 15 A or 230 V 10 A circuit; installation by a licensed electrical contractor | Licensed electrician | To assess |
| G8 | CPSC proposed safety standard for lithium-ion batteries used in micromobility products (Federal Register, 2026-06-24, document 2026-12749) | United States | Safety of micromobility batteries and their electrical systems | Bears on the packs; DockHub does not make packs | SwapCell project | To assess |
| G9 | ANSI/NEMA 250 enclosure type designations and IEC 60529 IP codes | United States; international (named; texts not consulted) | Weather and dust protection of enclosures | R9 asks for IP54; FDNY refers to NEMA 250 weatherization for cabinets | Design lead | To assess; test at TRL 4 |
| G10 | ADA Standards, operable parts: reach range 15 to 48 in above the floor | United States | Reachable controls | All operable parts at 0.73 to 1.10 m (PR-011) | Design lead | Met by design |
| G11 | Radio and mains-EMC approval of the modem and chargers (FCC or CE marks, as the bought parts carry) | Country of deployment | Radio equipment | Bought modem and chargers must already be marked; DockHub adds no radio design | Design lead | To assess when parts are chosen |
| G12 | Data protection for the rider token and swap log | Country of deployment (for example GDPR in the EU) | Personal data | No cameras or microphones; logs hold an opaque token (PR-012); whether a token is personal data is to assess | Co-design partner | To assess |
| G13 | Manual handling and lone work for the technician and the pack lift | Country of deployment | Lifting and site safety | A 2.85 kg pack; the cabinet is installed with a lifting aid (the 1.1 t pad needs a crane or ready-mix delivery) | Design lead | To assess |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- NYC Department of Transportation, press release "NYC DOT takes first steps to install public e-bike battery swapping network citywide", 2025-11-18, https://www.nyc.gov/html/dot/html/pr2025/install-public-e-bike-battery-swapping-network-citywide.shtml, accessed 2026-10-31 (G4, G5).
- FDNY, *E-Micromobility Approval Guide* (battery charging cabinets, UL 1487, UL 4900, COA and outdoor site survey, fees), https://www.nyc.gov/assets/fdny/downloads/pdf/business/e-micromobility-approval-guide.pdf, accessed 2026-10-31 (G1, G2, G3, G5, G9).
- CleanTechnica, "Battery Swapping Expands In New York City", 2026-02-28, https://cleantechnica.com/2026/02/28/battery-swapping-expands-in-new-york-city/, accessed 2026-10-31 (pilot and citywide plan; no standard named).
- US Access Board, *Guide to the ADA Standards, Chapter 3: Operable Parts*, https://www.access-board.gov/ada/guides/chapter-3-operable-parts/, accessed 2026-10-31 (G10).
- US Consumer Product Safety Commission via the Federal Register, 2026-06-24, https://www.federalregister.gov/documents/2026/06/24/2026-12749/safety-standard-for-lithium-ion-batteries-used-in-micromobility-products-and-electrical-systems-of, as cited in DKH-PRB-001 (G8); the document was not re-read for this register.
- Standards named by number only (G6, G7, G9 NFPA, IEC, UL 9540A, UL 2849, UL 2272, UL 2271): texts not consulted; each applicability is to be confirmed by the role named.
