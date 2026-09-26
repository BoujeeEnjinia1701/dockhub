# BOM notes

All costs are indicative USD prices for a single prototype, not quotes. Suppliers are not yet selected; each line names a supplier type.

- Line numbers match the exploded view (`media/exploded.png`) and the precis (DKH-PRC-001). Line 16 has no callout.
- The BOM is for the first prototype: the cabinet is built for four bays, with bays 1 and 2 fitted (lines 2, 3 and 5 at quantity 2) and bays 3 and 4 closed with blank plates (in line 1). This is DKH-DDR-001 item 1, decided by Amish on 2026-09-25: go with recommendation (DKH-DDR-002).
- Total: $1,199 against the $1,200 budget in `project.yaml`, checked by `docs/04-calcs/sizing.py` (DKH-CAL-001 section 12). The $1 margin means R16 is at risk on indicative prices.
- Each further bay (door, compartment, charger) adds $112; all four bays fitted cost $1,423.
- Line 5 now specifies a charger power factor of 0.9 or better; without power factor correction four chargers overload a 120 V 15 A circuit (DKH-CAL-001 section 6). The price assumes this does not cost more; confirm at supplier selection.
- Line 3 carries the SwapCell interface v0.3 receptacle with its 10 kΩ INTERLOCK coding resistor and a class D latch catch.
- SwapCell packs (line 4) are not in the station cost; they are priced once in the SwapCell BOM at about $414 each (SWC-CAL-001). One bay is always empty, so the prototype holds one resident pack and a four-bay station three, plus one pack per rider in circulation.
- Excluded: concrete pad and anchors into it (four anchors of at least 3.8 kN design tension each, DKH-CAL-001 section 11), electrical connection by an electrician, permits and cellular data plan.
