# BOM notes

All costs are indicative USD prices for a single prototype, not quotes. Suppliers are not yet selected; each line names a supplier type and gives its price basis.

- Line numbers match the exploded view (`media/exploded.png`) and the precis (DKH-PRC-001). Lines 16 to 19 have no callout.
- The BOM is for the first prototype: the cabinet is built for four bays, with bays 1 and 2 fitted (lines 2, 3 and 5 at quantity 2) and bays 3 and 4 closed with blank plates (in line 1). This is DKH-DDR-001 item 1, decided by Amish on 2026-09-25: go with recommendation (DKH-DDR-002).
- Value-engineering target: USD 1,200. Estimated cost of the constructable design: USD 1,519 (USD 319 over the target), checked by `docs/04-calcs/sizing.py` (DKH-CAL-001 section 12). `budget_usd` in `project.yaml` is unchanged.
- Lines 17 and 18 (added 2026-10-02): four M12 stainless wedge anchors (USD 10 each, retail price for approved stainless anchors plus a security nut) and a cast reinforced concrete pad 1,400 x 1,100 x 300 mm (USD 265: 28 bags of 36 kg premix at about USD 6.50, USD 40 of 10 mm bar mesh, USD 25 of formwork and USD 18 of gravel). They are for the first pilot on private ground (decided 2026-10-02) and are sized in DKH-CAL-001 section 11. Without them the estimate is USD 1,214.
- Line 19 (added 2026-10-02) is the vermiculite bay floor tray, a trial option for the propagation trial at about USD 11 a bay (tray about USD 8, vermiculite about USD 3). Its quantity is 0: it is not fitted to the first prototype and not in the total.
- Each further bay (door, compartment, charger) adds USD 112; all four bays fitted cost USD 1,743.
- Line 5 specifies a charger power factor of 0.9 or better; without power factor correction four chargers overload a 120 V 15 A circuit (DKH-CAL-001 section 6). The price assumes this does not cost more; confirm at supplier selection.
- Line 3 carries the SwapCell interface v0.3 receptacle with its 10 kΩ INTERLOCK coding resistor and a class D latch catch.
- SwapCell packs (line 4) are not in the station cost; they are priced once in the SwapCell BOM at about USD 414 each (SWC-CAL-001). One bay is always empty, so the prototype holds one resident pack and a four-bay station three, plus one pack per rider in circulation.
- Mass: 217 kg for the two-bay prototype without packs and 247 kg for four bays with three packs (DKH-CAL-001 section 10); the site pad adds about 1,109 kg of concrete.
- Excluded: electrical connection by an electrician, permits, anonymous prepaid cards (sold by the partner) and the cellular data plan.
