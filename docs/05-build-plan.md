---
doc_id: DKH-BLD-001
title: DockHub prototype build plan
project: DockHub
doc_type: Build plan
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan, with pictures by component and step; design made constructable (DKH-DDR-003, Draft)
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target; cross-references updated
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Safety stop S7: first site on private property with an existing single-phase circuit (DKH-DEC-001)"
  - version: "0.4"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Approved follow-ups: socket holes in the plinth top flange; anchors and site pad chosen (section 9, DKH-DWG-120); vermiculite floor tray as a trial option (DKH-DWG-119)"
---

# DockHub prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order. The shell is pulled apart in place; the parts that go inside it are lined up on the right.*

The prototype is the full DockHub cabinet, 1,000 mm wide, 500 mm deep and 1,500 mm tall to the roof, with its solar canopy on top, built for four bays with bays 1 and 2 fitted and bays 3 and 4 closed by blank plates. The cabinet is a shell of 1.5 mm galvanized steel panels with folded edges, joined with blind rivets, standing on a welded steel channel plinth. Inside are a charger shelf, a bay deck, a plenum wall at the back, two steel bay liners with printed cradles, and the electrical boxes on the back wall. A roof frame of two steel angles carries the four canopy posts, and two rails on the posts carry the 400 W panel. Figure 1 shows the 23 components in the order they are fitted. The made parts, each with its own making sketch, are the plinth, six shell panels, the shelf, the deck, the plenum wall, the liners, the cradles, the catch brackets, the roof beams, the vent hood, the doors and blank plates, the service door, the posts and the rails. The bought parts are chargers, controller, MPPT controller, grid unit, fire unit and detector, fans, receptacles, locks, access panel and solar panel. The work is sheet metal cut and folded at a sheet metal shop (or on a 1.5 m folder), drilling and blind riveting, a little welding of channel, tube and plate, two 3D prints, and bolting bought units in place. The parts cost about $1,214 from the bill of materials, packs and site works not included.

> **Safety:** The finished cabinet stores and charges lithium-ion packs of about 468 Wh each from mains power, and weighs about 217 kg before packs. No pack goes into it, and no mains supply is connected, until the safety stops of section 6 are passed. All mains wiring is done or checked by a qualified electrician. Cut sheet edges are sharp: deburr them and wear cut-resistant gloves. Welding and cutting galvanized steel gives off zinc fumes: grind the zinc off the weld area and weld with extraction or outdoors. Lift the cabinet with equipment, never by hand.

## 2. What changed to make it buildable

The concept showed what DockHub does; parts of it could not be made, fixed or put together as drawn. Each change below keeps what the station does, and all of them are recorded in decision record DKH-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Cabinet body | One closed steel box with no joints | Six panels with folded flanges (Figures 4 to 7, 16, 19), joined with blind rivets; the front panel is laser cut with all its openings | A sheet metal shop can make it and two people can put it together |
| Roof frame | Named in the bill of materials but not drawn; the canopy posts stood on the 1.5 mm roof sheet | Two 40 x 40 x 4 mm angle beams under the post lines, bolted through cleats to the front and back panels (Figures 17, 18) | Each front post pulls up with about 1.25 kN in a 30 m/s gust; the sheet alone cannot take it |
| Canopy | Posts stopped 5 mm under the rails, the rails 2 mm under the panel, and nothing held the panel | Posts on welded base and cap plates, the cap cut to the 10° slope; rails 1,174 mm long; four end clamps on the panel frame (Figures 26 to 29) | Every joint touches and is bolted; the clamps hold a bought panel without drilling it |
| Plenum wall and vent | A 10 mm slab with no vent ports; fans 120 mm across under an 80 mm louver, with no hole in the roof | A 1.5 mm folded wall with a port behind each bay; two 110 mm roof holes; a folded vent hood with twelve slots in its back face (Figures 10, 20, 21) | Gas and warm air now have a path out, still to the back and away from the rider |
| Bay doors | 172 mm doors hung 2 mm in front of 172 mm openings, with no hinge or gasket land | Openings 150 mm wide; 2 mm doors 172 x 526 mm on piano hinges, closing on an EPDM gasket; the lock tongue on the door enters a solenoid lock on the liner wall (Figures 22, 23) | Leaves 24 mm between doors for the hinge and an 11 mm overlap for the gasket; the pack still has 30 mm each side |
| Cradle and catch | The receptacle and the cradle occupied the same space; guides and catch post stood unattached | One printed cradle with its guides, the receptacle in a pocket underneath, a folded steel catch bracket standing in a slot and screwed to the liner (Figures 13 to 15) | Every part is held and the receptacle fits where the pack's plug lands |
| Liners, deck, shelf | Floated, with no fixing; the charger rack was a 10 mm plate | Folded sheet with flanges riveted to the panels; liners riveted to the front panel and the plenum wall (Figure 12) | Everything inside is fixed to the shell |
| Electrical boxes, fire unit | Floated 8 to 40 mm off the walls | Screwed to the back panel; the aerosol unit on two straps; the detector under the roof | Every unit has a wall to fix to |
| Plinth and anchors | A solid 60 mm ring; anchors under boxes where no tool could reach them | Welded 100 x 50 x 5 mm channel frame; eight M10 floor bolts; anchors 25 mm from the ends, reached through capped holes in the floor (Figure 3) | A tool reaches every anchor nut with the cabinet built |
| Service door | 960 mm opening leaving no land for a hinge | 900 x 500 mm opening; 920 x 520 mm door on a piano hinge with gasket, cam lock and filtered intake slot (Figures 24, 25) | Room for the hinge and the gasket all round |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Left" and "right" are as seen standing in front of the cabinet, facing the doors. Heights are from the ground under the plinth unless a step says otherwise; sideways positions are from the cabinet's centre line. Workshop tolerance is 1 mm on sheet parts and 0.5 mm on hole positions unless a step says otherwise; drawings do not carry tolerances before TRL 4. Rivets are 4 mm blind rivets in 4.1 mm holes at about 100 mm pitch, 12 mm in from the edge, drilled through both parts at assembly.

### 3.1 Plinth

![Figure 2. Making sketch of the plinth](../cad/drawings/DKH-DWG-101.png)

*Figure 2. Plinth making sketch (DKH-DWG-101).*

**What it is and what it is made from.** The steel frame the cabinet stands on and is anchored through. Steel channel 100 x 50 x 5 mm, painted or galvanized after welding.

**How to make it.**

1. Cut two lengths of 1,000 mm and two of 500 mm, outside measurements, ends mitred at 45°, so that the flanges point inward.
2. Lay them on a flat table, clamp, check the diagonals are equal within 2 mm, and weld each corner all round.
3. In the bottom flange, drill four 14 mm anchor holes, 25 mm in from each end and 30 mm in from the front and back edges. In the top flange, straight above each anchor hole, cut a 32 mm socket hole so that a socket can reach the anchor nut from above.
4. In the top flange, drill eight 11 mm holes for the floor bolts: along the front, 25 mm in, at 100, 350, 650 and 900 mm from the left end; along the back, 25 mm in, at 520 and 680 mm from the left end; and one at each end, 25 mm in, centred front to back.
5. Grind the welds flush on the top face, clean off spatter, and paint or galvanize.

**How it fits the parts next to it.** The floor pan sits flat on the top flange and is held by eight M10 bolts, heads inside the cabinet and nuts under the top flange. At the site, four M12 stainless wedge anchors go through the bottom flange into the concrete pad (section 9); inside the cabinet a socket on an extension reaches each anchor nut through a capped 40 mm hole in the floor and the 32 mm hole in the plinth's top flange:

![Figure 3. Joint 1: plinth corner, floor pan and walls](05-build-plan/joint-01.png)

*Figure 3. The front right corner seen from inside: the floor pan on the plinth, a floor bolt, and the socket holes in the floor and the plinth's top flange over the anchor hole.*

**Check before moving on.** The top is flat within 1 mm; the diagonals match within 2 mm; held over the floor pan, every bolt hole lines up.

### 3.2 Floor pan

![Figure 4. Making sketch of the floor pan](../cad/drawings/DKH-DWG-102.png)

*Figure 4. Floor pan making sketch (DKH-DWG-102).*

**What it is and what it is made from.** The floor of the cabinet, which the walls stand on. Galvanized steel sheet 1.5 mm.

**How to make it.**

1. Cut a plate 997 x 497 mm with a 25 mm flange on every edge, and cut the side flanges 25 mm short at each end (corner reliefs), so they clear the flanges of the front and back panels.
2. Fold the long flanges up 90°, then the short ones.
3. Drill eight 11 mm bolt holes through the plate to match the plinth: hold the pan on the plinth and drill through.
4. Cut four 40 mm socket holes over the anchors, 475 mm each side of the centre and 220 mm in front of and behind the centre, and one 25 mm hole for the grid cable gland, 340 mm right of centre and 120 mm behind it.

**How it fits the parts next to it.** It sits on the plinth (Figure 3). The walls stand on the floor plate's edges, outside its flanges, and are riveted through the flanges.

**Check before moving on.** The flanges are square to the plate and the bolt holes line up with the plinth.

### 3.3 Back panel

![Figure 5. Making sketch of the back panel](../cad/drawings/DKH-DWG-103.png)

*Figure 5. Back panel making sketch (DKH-DWG-103).*

**What it is and what it is made from.** The back wall of the cabinet, which also carries the electrical boxes and the fire unit. Galvanized steel sheet 1.5 mm.

**How to make it.**

1. Cut a blank 1,000 x 1,400 mm with a 25 mm flange on each side edge, the flanges 1.5 mm short of the top and bottom edges.
2. Fold both side flanges 90° forward, toward the street side.
3. Leave the box and strap holes until step 4 of section 4, so they are marked through the parts themselves. Heights on the panel are from its bottom edge: the aerosol unit's strap screws go 1,300 to 1,340 mm up, and the roof cleat bolts two 9 mm holes 410 and 430 mm each side of the centre, 1,376 mm up (drilled in step 15).

**How it fits the parts next to it.** It stands on the floor pan's back edge, outside the floor flange; the side panels overlap its side flanges. All joints are blind rivets.

**Check before moving on.** Flanges at 90°, the panel flat within 3 mm.

### 3.4 Side panels (make 2)

![Figure 6. Making sketch of the side panel](../cad/drawings/DKH-DWG-104.png)

*Figure 6. Side panel making sketch (DKH-DWG-104).*

**What it is and what it is made from.** The two flat ends of the cabinet. Galvanized steel sheet 1.5 mm, 497 x 1,400 mm.

**How to make it.**

1. Cut two panels 497 x 1,400 mm and deburr the edges.
2. Drill no holes yet: every rivet hole is drilled through the panel into the flange behind it at assembly. The rivet lines are 12 mm in from the front, back, bottom and top edges, and across the panel where the bay deck flange (674 to 699 mm above the ground), the charger shelf flange (354 to 379 mm) and the plenum wall flange (112 to 132 mm behind the centre line) lie against it.

**How it fits the parts next to it.** Each side panel stands on the floor pan's edge, outside every flange that meets it:

![Figure 7. Joint 2: panel corner at the bay deck](05-build-plan/joint-02.png)

*Figure 7. The front right corner, cut just under the bay deck and seen from above: the front panel's flange lies inside the side panel, the deck's flanges lie on both, and the deck's side flange starts 25 mm back to clear the front panel flange.*

**Check before moving on.** The two panels are the same and square within 2 mm.

### 3.5 Charger shelf

![Figure 8. Making sketch of the charger shelf](../cad/drawings/DKH-DWG-105.png)

*Figure 8. Charger shelf making sketch (DKH-DWG-105).*

**What it is and what it is made from.** The shelf in the technical compartment that the chargers stand on. Galvanized steel sheet 1.5 mm.

**How to make it.**

1. Cut a plate 994 x 280 mm with a 25 mm flange on every edge, corners relieved.
2. Fold all four flanges down 90°, the long edges first.

**How it fits the parts next to it.** Its top face is 380 mm above the ground, from 60 mm in front of the centre line to 220 mm behind it, clear of the back panel's flanges. Its side flanges are riveted to the side panels, four rivets each. Each charger stands on it on four M5 screws through the shelf at the charger's own fixing holes, bay 1's charger centred 345 mm and bay 2's 115 mm left of centre.

**Check before moving on.** Level within 2 mm once riveted.

### 3.6 Bay deck

![Figure 9. Making sketch of the bay deck](../cad/drawings/DKH-DWG-106.png)

*Figure 9. Bay deck making sketch (DKH-DWG-106).*

**What it is and what it is made from.** The floor of the bay row, which the liners stand on. Galvanized steel sheet 1.5 mm.

**How to make it.**

1. Cut a plate 994 x 358.5 mm with a 25 mm flange on every edge; cut the side flanges 25 mm short at the front.
2. Fold all four flanges down 90°.
3. For each fitted bay (bay 1 centred 392 mm left of the centre line, bay 2 196 mm left): drill four 5.5 mm holes 60 mm each side of the bay centre, 188.5 and 308.5 mm back from the front edge, for the cradle screws; and cut a 40 x 30 mm cable hole on the bay centre, 241.5 to 271.5 mm back from the front edge, and fit an edge grommet. Drill bays 3 and 4 (on the centre line and 196 mm right) when they are fitted.

**How it fits the parts next to it.** Its top face is 700 mm above the ground; its front edge meets the front panel and its back edge stands 110 mm behind the centre line. Its side flanges are riveted to the side panels, its back flange to the plenum wall and its front flange to the front panel.

**Check before moving on.** Flat within 2 mm across the width.

### 3.7 Plenum wall

![Figure 10. Making sketch of the plenum wall](../cad/drawings/DKH-DWG-107.png)

*Figure 10. Plenum wall making sketch (DKH-DWG-107).*

**What it is and what it is made from.** The wall behind the bays. The space between it and the back panel is the plenum: charger heat rises up it, and any gas from a bay goes into it through the bay's vent port and out through the roof fans. Galvanized steel sheet 1.5 mm.

**How to make it.**

1. Cut a plate 994 mm wide and 823.5 mm tall, with a 20 mm flange along the top over the middle 876 mm and a 20 mm flange on each side edge that stops 42 mm below the top.
2. Notch both top corners 44 mm wide and 41 mm deep, starting 15 mm in from the side edge: the roof beams pass through these notches.
3. Fold the top flange forward (toward the bays) and the side flanges back.
4. Cut a 60 x 60 mm vent port for each fitted bay, on the bay centre, 466.5 to 526.5 mm up from the bottom edge (1,140 to 1,200 mm above the ground).

**How it fits the parts next to it.** It stands 110 mm behind the centre line from 673.5 to 1,497 mm above the ground. Its bottom edge overlaps the bay deck's back flange and is riveted to it; its side flanges are riveted to the side panels and its top flange to the roof. Each liner's back is riveted to it round the port (Figure 12). Once the roof is on, seal the beam notches with fire-rated sealant.

**Check before moving on.** The ports line up with the liner ports.

### 3.8 Bay liners (make 2)

![Figure 11. Making sketch of the bay liner](../cad/drawings/DKH-DWG-108.png)

*Figure 11. Bay liner making sketch (DKH-DWG-108).*

**What it is and what it is made from.** The steel box each pack stands in, open at the front, which keeps a pack fault inside its own bay. Galvanized steel sheet 1.5 mm.

**How to make it.**

1. Fold the two sides and the back from one blank into a U, 180 mm wide, 358.5 mm deep and 530 mm tall.
2. Fold a floor tray and a top tray and rivet them in. Along the top front edge, fold a 15 mm flange upward.
3. In the back, cut a 60 x 60 mm vent port, centred, 440 to 500 mm up from the liner's bottom.
4. In the floor, drill four 5.5 mm holes and cut a 40 x 30 mm cable hole at the same places as the deck holes (section 3.6).
5. In the right wall, drill the two solenoid lock holes, marked through the lock, near the front edge at 235 to 285 mm up from the liner's bottom.

**How it fits the parts next to it.**

![Figure 12. Joint 3: bay liner, deck, front panel and plenum wall](05-build-plan/joint-03.png)

*Figure 12. Bay 1 cut on its centre: the liner stands on the deck, its top flange lies against the back of the front panel above the door opening, and its back lies against the plenum wall round the vent port.*

The liner stands on the deck, its back flat against the plenum wall and its open front against the back of the front panel. The top flange is riveted to the front panel above the door opening; the back is riveted to the plenum wall round the port, from inside the liner; the floor is held to the deck by the four cradle screws. There is a 16 mm air gap between neighbouring liners and 16.5 mm between bay 1's liner and the side panel.

**Check before moving on.** Square; the port lines up with the plenum wall port.

### 3.9 Cradles (print 2)

![Figure 13. Making sketch of the cradle](../cad/drawings/DKH-DWG-109.png)

*Figure 13. Cradle making sketch (DKH-DWG-109).*

**What it is and what it is made from.** The printed block each pack stands on, with the side guides that steer it onto the receptacle. A flame-retardant filament rated UL 94 V-0, printed at 100 % infill.

**How to make it.**

1. Print one piece: a base 150 x 150 x 28.5 mm with two side guides 5 mm thick, 90 mm long and 130 mm tall on top, their inner faces 46 mm each side of the centre (the pack is 90 mm wide).
2. The print includes: a plug well open on top, 58 x 36 mm and 19.5 mm deep, centred 8 mm behind the cradle centre; a receptacle pocket open underneath, 72 x 50 mm and 9 mm deep, on the same centre; a catch slot 62 x 4 mm and 10 mm deep, 58.5 to 62.5 mm behind the centre; and four 5.5 mm holes 60 mm each side of the centre, front and back.
3. Press two M3 heat-set inserts into the pocket roof for the receptacle flange.
4. Put the receptacle into its pocket from below and fix it with two M3 screws.

**How it fits the parts next to it.**

![Figure 14. Joint 4: cradle, receptacle and catch bracket](05-build-plan/joint-04.png)

*Figure 14. Bay 1 cut on its centre, with a pack in place: the plug sits in the well over the receptacle, and the catch stands just above the pack's latch pawl.*

The cradle stands on the liner floor on four M5 screws down through the liner floor and the deck, nuts under the deck. The receptacle's lead goes down through the cable holes to the technical compartment. The pack stands connector down between the guides with its plug in the well.

**Check before moving on.** A pack dummy 90 x 80 mm slides between the guides without binding.

### 3.10 Catch brackets (make 2)

![Figure 15. Making sketch of the catch bracket](../cad/drawings/DKH-DWG-110.png)

*Figure 15. Catch bracket making sketch (DKH-DWG-110).*

**What it is and what it is made from.** The folded strip that holds the class D catch over the pack's latch pawl. Steel strip 60 x 3 mm, with a 50 x 8 x 8 mm steel catch block.

**How to make it.**

1. Cut 60 x 3 mm strip about 430 mm long and deburr it.
2. Bend it 90° twice: an upright 335 mm tall, a top leg 49.5 mm long reaching back, and a tab 43 mm long turned down.
3. Drill two 4.5 mm holes in the tab, 20 mm apart.
4. Rivet or screw the catch block to the front face of the upright, its underside 318 mm above the upright's bottom end.

**How it fits the parts next to it.** The upright's bottom end stands 10 mm down in the cradle's catch slot; the tab is screwed to the liner back wall with two M4 screws (Figure 14). The catch then sits 1 mm behind the pack's pawl and just above it, as SwapCell interface v0.3 requires.

**Check before moving on.** With a pack dummy in the cradle the pawl passes under the catch with the 1 mm gap; the upright is vertical.

### 3.11 Front panel

![Figure 16. Making sketch of the front panel](../cad/drawings/DKH-DWG-111.png)

*Figure 16. Front panel making sketch (DKH-DWG-111).*

**What it is and what it is made from.** The street face of the cabinet, with the door openings, the service opening and the access panel cut-out. Galvanized steel sheet 1.5 mm, laser cut by the sheet metal shop.

**How to make it.**

1. Cut a blank 1,000 x 1,400 mm with a 25 mm flange on each side edge, the flanges 1.5 mm short of the top and bottom edges. Heights below are from the panel's bottom edge.
2. Cut four bay openings 150 x 510 mm, 605 to 1,115 mm up, centred 392 and 196 mm left of the centre line, on it, and 196 mm right of it.
3. Cut the service opening 900 x 500 mm, centred, 50 to 550 mm up, and the access cut-out 120 x 300 mm, 340 to 460 mm right of centre, 780 to 1,080 mm up.
4. Drill the four roof cleat bolt holes, 9 mm, 410 and 430 mm each side of the centre, 1,376 mm up.
5. Fold the side flanges 90° back. Leave hinge, gasket and blank plate holes until the parts are fitted.

**How it fits the parts next to it.** Its side flanges sit inside the side panels and are riveted through them (Figure 7). Its back face lies on the deck's front flange and on each liner's top flange, all riveted from the front.

**Check before moving on.** Openings square and in line; 46 mm of panel between neighbouring door openings.

### 3.12 Roof beams with cleats (make 2)

![Figure 17. Making sketch of the roof beam](../cad/drawings/DKH-DWG-113.png)

*Figure 17. Roof beam making sketch (DKH-DWG-113).*

**What it is and what it is made from.** The two steel angles under the roof that the canopy posts bolt down into, and that carry the canopy's lift into the front and back panels. Steel angle 40 x 40 x 4 mm, painted.

**How to make it.**

1. Cut two beams 494 mm long. In the horizontal leg of each, drill four 11 mm holes on a line 20 mm from the heel, 12 and 82 mm from each end.
2. Cut four cleats 36 mm long from the same angle. Weld two M8 nuts, 20 mm apart, to the inside face of one leg of each cleat, over 9 mm holes.
3. Clamp a cleat's other leg to each end of a beam's upright leg and drill both 9 mm for two M8 bolts. Bolt them together.

**How it fits the parts next to it.**

![Figure 18. Joint 6: roof beam, cleat and front post base](05-build-plan/joint-06.png)

*Figure 18. Cut on the right post line: the beam's horizontal leg lies under the roof, the post's base plate on top, two M10 bolts through all three; the cleat at the beam end lies against the roof's front flange.*

Each beam's horizontal leg lies flat under the roof plate on a post line, 460 mm each side of the centre, with the upright leg on the inner side, and its ends touch the roof's front and back flanges. The cleats' nut legs lie against the roof flanges; M8 bolts come in from outside through the front (or back) panel and the roof flange into the welded nuts, so nothing has to be reached inside. The post bolts pass through base plate, roof and beam.

**Check before moving on.** The four holes in each beam line up with the post holes in the roof.

### 3.13 Roof panel

![Figure 19. Making sketch of the roof panel](../cad/drawings/DKH-DWG-112.png)

*Figure 19. Roof panel making sketch (DKH-DWG-112).*

**What it is and what it is made from.** The roof of the cabinet; the beams, fans and detector are fitted under it before it goes on. Galvanized steel sheet 1.5 mm.

**How to make it.**

1. Cut a plate 997 x 497 mm with a 40 mm flange on every edge, the side flanges 25 mm short at each end.
2. Fold all four flanges down 90°.
3. Cut two 110 mm fan holes, 350 mm each side of the centre and 173 mm behind it, and one 25 mm hole for the panel cable gland, 200 mm left of centre and 60 mm behind it.
4. Drill eight 11 mm post bolt holes, 460 mm each side of the centre, 165 and 235 mm in front of and behind the centre.
5. In the front and back flanges, drill two 9 mm cleat bolt holes 410 and 430 mm each side of the centre, 18 mm up from the flange's lower edge.

**How it fits the parts next to it.** It drops in from above inside the four walls with its top flush with the wall tops; its flanges are riveted to the walls and sealed with mastic. The fans hang under it on spacers and blow up through the holes into the vent hood:

![Figure 20. Joint 9: roof fan and vent hood](05-build-plan/joint-09.png)

*Figure 20. The right fan cut through its centre: the fan on 4 mm spacers under the roof, the hole above it, and the hood over the hole with its slots at the back.*

**Check before moving on.** It drops in without forcing, with all eight post holes over the beams.

### 3.14 Vent hood

![Figure 21. Making sketch of the vent hood](../cad/drawings/DKH-DWG-114.png)

*Figure 21. Vent hood making sketch (DKH-DWG-114).*

**What it is and what it is made from.** The folded cover over the two fan holes that turns the outflow to the back of the cabinet and keeps rain out. Galvanized steel sheet 1.5 mm.

**How to make it.**

1. Fold a box 850 mm wide, 133 mm deep and 70 mm tall, open underneath: a front wall with a 20 mm flange forward, end walls with 8 mm flanges outward, a back wall with a 15 mm flange backward, and a top that overhangs the back wall by 10 mm as a rain lip.
2. In the back wall, cut twelve slots 50 x 40 mm, 12 mm above the bottom edge, on a 71.8 mm pitch starting 30 mm from each end. Fit insect mesh behind them.

**How it fits the parts next to it.** It stands on the roof over both fan holes, its front face 98.5 mm behind the centre line; its flanges are riveted and sealed to the roof (Figure 20). Air and any vented gas leave through the back slots, away from the rider side.

**Check before moving on.** Both fan holes lie fully inside the hood.

### 3.15 Bay doors and blank plates (make 2 of each)

![Figure 22. Making sketch of the bay door and blank plate](../cad/drawings/DKH-DWG-115.png)

*Figure 22. Bay door and blank plate making sketch (DKH-DWG-115).*

**What it is and what it is made from.** The locking door over each fitted bay, and the plate that closes each unfitted bay. Steel plate 2 mm, powder coated.

**How to make it.**

1. Cut four plates 172 x 526 mm and round the corners 3 mm. Two become doors, two blank plates.
2. Doors: fit the pull handle on the front, 45 to 70 mm right of the door centre and 243 to 283 mm up from its bottom edge. Rivet a small 4 mm steel angle to the back as the lock tongue: the tongue stands 21 mm back from the door, 50 to 54 mm right of centre, 253 to 273 mm up, with a 6 mm hole for the lock bolt.
3. Blank plates: drill four 5.5 mm holes, 10 mm in from the corners, for M5 security screws.

**How it fits the parts next to it.**

![Figure 23. Joint 5: bay door, hinge, gasket and lock](05-build-plan/joint-05.png)

*Figure 23. Bay 2 cut at lock height and seen from above: the hinge on the left, the gasket between door and panel, and the tongue entering the lock on the liner wall.*

Each door covers its 150 mm opening with 11 mm to spare at each side and 8 mm at top and bottom, so it closes on a 7 x 3 mm EPDM gasket stuck to the panel 1 mm out from the opening's edge. A stainless piano hinge 480 mm long is riveted along the door's left edge and to the panel beside it, its knuckle in the 24 mm gap between doors. The tongue passes inside the gasket into the solenoid lock. Blank plates go on four M5 security screws into rivet nuts in the panel.

**Check before moving on.** The door closes onto the gasket evenly and the tongue enters the lock without rubbing.

### 3.16 Service door

![Figure 24. Making sketch of the service door](../cad/drawings/DKH-DWG-116.png)

*Figure 24. Service door making sketch (DKH-DWG-116).*

**What it is and what it is made from.** The locking door over the technical compartment, with the filtered air intake. Steel plate 2 mm, powder coated.

**How to make it.**

1. Cut a plate 920 x 520 mm and round the corners 3 mm.
2. Cut the intake slot 400 x 80 mm, centred, 30 to 110 mm up from the bottom edge, and fold a sheet clip frame that holds a 410 x 90 x 10 mm filter pad behind it (four rivets).
3. Cut a 19 mm hole for the cam lock 420 mm right of centre and 260 mm up from the bottom edge.

**How it fits the parts next to it.**

![Figure 25. Joint 10: service door cam lock](05-build-plan/joint-10.png)

*Figure 25. Cut at lock height and seen from above: the cam arm turns behind the panel edge and pulls the door onto the gasket.*

The door covers the 900 x 500 mm opening with 10 mm to spare all round and closes on a 7 x 3 mm EPDM gasket. A stainless piano hinge 460 mm long runs along its left edge. The cam lock's arm, 60 mm long, turns behind the panel beside the opening.

**Check before moving on.** The cam pulls the door tight onto the gasket.

### 3.17 Canopy posts (make 4)

![Figure 26. Making sketch of the canopy post](../cad/drawings/DKH-DWG-117.png)

*Figure 26. Canopy post making sketch (DKH-DWG-117).*

**What it is and what it is made from.** The four legs of the canopy. Square steel tube 50 x 50 x 3 mm, with base plates 50 x 100 x 8 mm and cap plates 50 x 70 x 6 mm, painted.

**How to make it.**

1. Cut two front posts 766 mm long and two rear posts 696 mm long, measured on the tube's centre line, the top end cut at 10° so it slopes down toward the back.
2. Drill each base plate with two 11 mm holes on its centre line, 15 and 85 mm from its outer end. Weld the post to it, centred, with 25 mm of plate each side of the tube.
3. Drill each cap plate with two 9 mm holes 40 mm apart along the slope, and weld it on the sloping top.
4. Paint.

**How it fits the parts next to it.** Each base plate lies flat on the roof over a beam, its outer end flush with the front (or back) edge of the roof, on two M10 bolts through plate, roof and beam with sealing washers (Figure 18). The rail sits on the cap plate on two M8 bolts:

![Figure 27. Joint 7: rear post top, cap plate and rail](05-build-plan/joint-07.png)

*Figure 27. The right rear post: the cap plate is cut to the 10° slope and the rail sits flat on it.*

**Check before moving on.** Each post is square to its base plate within 1°.

### 3.18 Canopy rails (make 2)

![Figure 28. Making sketch of the canopy rail](../cad/drawings/DKH-DWG-118.png)

*Figure 28. Canopy rail making sketch (DKH-DWG-118), drawn laid flat.*

**What it is and what it is made from.** The two rails the solar panel sits on. Rectangular steel tube 50 x 40 x 3 mm, painted.

**How to make it.**

1. Cut two lengths of 1,174 mm.
2. Drill the post bolt holes, 9 mm through both walls, two at each post, 40 mm apart, centred 547 mm (front post) and 954 mm (rear post) from the front end.
3. Drill a 9 mm end clamp hole in the top wall 10 mm from each end. Cap both ends.

**How it fits the parts next to it.** The rails run up the slope at 460 mm each side of the centre, high at the street side, and run 20 mm past the panel's front and back edges. The panel frame sits on them, and an end clamp at each end of each rail grips the frame's edge:

![Figure 29. Joint 8: panel end clamp on the rail](05-build-plan/joint-08.png)

*Figure 29. The front right end clamp holding the panel frame's edge onto the rail.*

**Check before moving on.** Both rails lie in one plane: a string line across their tops touches all four ends.

### 3.19 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Chargers (line 5).** Certified lithium-ion chargers, 54.6 V, 5 A, CC-CV, 100 to 240 V input, power factor 0.9 or better, with screw-down feet.
- **Dock controller (line 6).** ESP32 with four CAN channels, contactors rated 60 V DC 10 A, current sensors, LTE-M modem and SD card, in a DIN box no larger than 220 x 100 x 190 mm.
- **Access panel (line 7).** Vandal-resistant NFC reader, sunlight-readable display, bay status lights and buzzer on a steel bezel 180 x 360 mm, fixed with security screws.
- **Grid input and protection (line 8).** DIN enclosure no larger than 220 x 92 x 200 mm with a 30 mA RCBO, a breaker per charger, surge protection, lockable isolator and gland. Installed and connected by a qualified electrician.
- **Fire detection and suppression (line 9).** Heat and smoke detector, and a condensed-aerosol unit about 76 mm across and 420 mm long with its maker's two straps.
- **Fans (line 10).** Two 120 x 120 x 25 mm fans, IP55, with corner holes on a 105 mm square; insect mesh; filter pad.
- **Receptacles (line 3).** SwapCell interface v0.3 blind-mate receptacle with its 10 kΩ INTERLOCK coding resistor and NTC, with a flange that fits the 72 x 50 mm pocket.
- **Solenoid locks (line 2).** 12 V fail-secure cabinet locks with a door switch, about 30 x 30 x 50 mm, whose bolt reaches the door tongue.
- **Solar panel (line 11).** 400 W monocrystalline, about 1,722 x 1,134 x 35 mm in an aluminium frame suited to standard end clamps, about 21 kg.
- **MPPT controller (line 13).** PV input up to 100 V, programmable lithium profile at 54.6 V, output limited to 5 A, no larger than 150 x 70 x 180 mm.
- **Anchors (line 17).** Four M12 x 160 mm stainless steel wedge anchors with a published approval for cracked concrete, each with a washer and a tamper-resistant nut; the approval data must give a design tension resistance of at least 3.8 kN at 100 mm embedment in C25/30 concrete. They are fitted at the site (section 9).
- **Hardware (lines 12 and 16).** Four solar end clamps for a 35 mm frame; eight M10 x 30 floor bolts and eight M10 x 40 post bolts with nyloc nuts and sealing washers; M8 cleat and rail bolts; M5 and M4 screws; 4 mm blind rivets; rivet nuts; stainless piano hinges (two 480 mm, one 460 mm); EPDM gasket strip 7 x 3 mm; fire-rated sealant and roof mastic; cable glands; the DC fuse per bay.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in. Two people are needed from step 13 on.

### Step 1: floor pan onto the plinth

![Step 1](05-build-plan/step-01.png)

Stand the plinth on two timber bearers under its ends, about 150 mm high, so a hand reaches under the top flange. Lay the floor pan on it, bolt holes lined up, and fit eight M10 bolts down through floor and flange, nuts from below, tight.

### Step 2: back panel

![Step 2](05-build-plan/step-02.png)

Stand the back panel on the floor pan's back edge, outside the floor flange, and clamp it upright. Drill and rivet through the floor flange.

### Step 3: side panels

![Step 3](05-build-plan/step-03.png)

Stand each side panel on the floor pan's edge, outside the back panel's flange and the floor flange. Check the cabinet is square, then drill and rivet both joints.

### Step 4: controller, MPPT and grid boxes onto the back panel

![Step 4](05-build-plan/step-04.png)

Hold each box against the back panel, mark its fixing holes through it, drill, and fit M5 screws with sealing washers. The controller goes from 450 to 230 mm left of centre, the MPPT controller from 190 to 40 mm left of centre and the grid box from 230 to 450 mm right of centre, all from 150 mm above the ground. **Hold point:** the grid box is connected only by the electrician (S2).

### Step 5: aerosol suppression unit

![Step 5](05-build-plan/step-05.png)

Fit the unit on its two straps, two M5 screws each through the back panel, 1,400 to 1,440 mm above the ground, 60 mm left of centre. Leave its trigger disconnected until S5.

### Step 6: charger shelf

![Step 6](05-build-plan/step-06.png)

Slide the shelf in from the front, top face 380 mm above the ground, and rivet its side flanges to the side panels.

### Step 7: chargers onto the shelf

![Step 7](05-build-plan/step-07.png)

Stand each charger on the shelf, mark through its feet, drill and fit four M5 screws. Leave all mains and DC leads unconnected.

### Step 8: bay deck

![Step 8](05-build-plan/step-08.png)

Drill the bay holes first (section 3.6). Slide the deck in, top face 700 mm above the ground, and rivet its side flanges to the side panels.

### Step 9: plenum wall

![Step 9](05-build-plan/step-09.png)

Lower the wall in from above behind the deck, its bottom edge overlapping the deck's back flange. Rivet it to the deck flange and its side flanges to the side panels.

### Step 10: bay liners

![Step 10](05-build-plan/step-10.png)

Slide each liner back onto the deck until its back touches the plenum wall, with the ports lined up. Rivet the back to the plenum wall round the port from inside the liner.

### Step 11: cradles, receptacles and catch brackets

![Step 11](05-build-plan/step-11.png)

With its receptacle already screwed in from below, set each cradle in its liner, feed the receptacle lead down through the cable holes, and fit four M5 screws through liner floor and deck with nuts under the deck. Stand the catch bracket in the cradle's slot and screw its tab to the liner back wall with two M4 screws.

### Step 12: solenoid locks

![Step 12](05-build-plan/step-12.png)

Fit each lock inside its liner against the right wall, two M4 screws through the wall, bolt toward the door opening.

### Step 13: front panel

![Step 13](05-build-plan/step-13.png)

Offer the front panel up with its side flanges inside the side panels. Rivet through the side panels, then from the front into the deck's front flange, the liners' top flanges and the floor flange.

### Step 14: build the roof sub-assembly

![Step 14](05-build-plan/step-14.png)

Lay the roof upside down on a padded bench. Set the beams with their cleats on the post lines and hold each with two of its post bolts, loosely. Fit the two fans on M4 screws through 4 mm spacers, blowing up through the holes, and the detector between them.

### Step 15: roof onto the cabinet

![Step 15](05-build-plan/step-15.png)

Turn the roof over and lower it in from above, the beams passing through the plenum wall notches. Rivet its flanges to the walls with mastic in the joint, and rivet the plenum wall's top flange to it. Fit the cleat bolts from outside through the front and back panels and roof flanges into the welded nuts, tight. Seal the notches.

### Step 16: vent hood

![Step 16](05-build-plan/step-16.png)

Set the hood over both fan holes, slots to the back, and rivet and seal its flanges to the roof.

### Step 17: bay doors and blank plates

![Step 17](05-build-plan/step-17.png)

Stick the gasket round each fitted opening. Rivet each hinge to the panel, then to the door, so the tongue enters the lock. Fit rivet nuts and the two blank plates over bays 3 and 4 on M5 security screws.

### Step 18: access panel

![Step 18](05-build-plan/step-18.png)

Feed the reader and display leads through the cut-out and fix the bezel over it with security screws into rivet nuts.

### Step 19: service door

![Step 19](05-build-plan/step-19.png)

Stick the gasket round the opening, rivet the hinge to panel and door, and fit the cam lock and the filter pad.

### Step 20: canopy posts

![Step 20](05-build-plan/step-20.png)

Seen with the cabinet complete. Set each post's base plate on the roof over its beam, outer end flush with the roof edge, and replace the two loose bolts with the M10 post bolts through plate, roof and beam, sealing washers under the plate, nyloc nuts under the beam, tight. **Hold point:** S6 before the rails go on.

### Step 21: canopy rails

![Step 21](05-build-plan/step-21.png)

Set each rail on its two cap plates, high end to the street, and fit two M8 bolts at each post. Check both rails lie in one plane before tightening.

### Step 22: solar panel

![Step 22](05-build-plan/step-22.png)

Two people on stable platforms. Lay the panel on the rails, high edge to the street, and fit the four end clamps. Bring the panel cable down through the roof gland to the MPPT controller, unconnected. **Hold point:** S7.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of DKH-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Reach heights | R11 | Tape measure from the ground | Door handles, reader and pack handles all between 0.38 and 1.22 m (0.73 to 1.10 m expected) |
| Gloved swap | R1, R11 | A pack dummy of the SwapCell size and mass, returned and lifted out by a person in work gloves | Pack goes in and out without touching the door opening; under 60 s from tap to closed door |
| Door seal and lock | R9, R10 | Close each door; pull hard with the lock unpowered | Gasket evenly squeezed all round; door stays shut; switch reads closed |
| Receptacle alignment | R2 | Pack dummy with a plug of the interface size dropped in each bay | Plug enters the well without touching its sides; catch 1 mm over the pawl |
| Mains installation | R5 | Electrician's inspection and tests to local code | RCD trips within its rated time; earth continuity to every metal part; isolator locks off |
| Charge with a pack | R3 | One healthy pack, bay 1, attended | Charging starts only after the CAN check; 20 to 80 % in about 1.2 h |
| Shutdown chain | R7 | Warm the bay's receptacle sensor with a heat gun to 60 °C | Contactor opens within 1 s of detection; buzzer, light and remote alert; door stays locked |
| Vent path | R7 | Smoke pencil at a bay's vent port with the fans on | Smoke leaves through the hood's back slots only |
| Canopy height | R13 | Measure from the ground | Lowest canopy point over the walkway 2.1 m or more (2.17 m expected) |
| Mass | | Weigh on a crane scale | About 217 kg without packs |
| Part swap | R14 | Time a technician changing a charger and a lock with hand tools | 15 minutes or less each |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before any cutting or welding.** Zinc ground off weld areas; welding with extraction or outdoors; a fire extinguisher at hand; cut-resistant gloves for sheet.
- **S2. Before the grid box is connected.** A qualified electrician designs and makes the supply connection to local code: RCD, a breaker per charger, surge protection, lockable isolator, and every metal part bonded to earth. Mains and the 54.6 V DC side are kept apart and labelled.
- **S3. Before mains is switched on.** The electrician's tests pass; every DC line has its 60 V DC fuse fitted; all doors and the service door are closed; the isolator is locked off whenever anyone works inside.
- **S4. Before any pack enters the workshop.** The cabinet stands on a non-combustible floor, outdoors or in a fire-rated space, with a lithium-rated extinguisher and a bucket of sand within reach. Every pack has been checked by the SwapCell procedure: no damage, swelling or water, and it answers on CAN.
- **S5. Before the first charge.** The shutdown chain check of section 5 has passed with no pack in the cabinet; the aerosol unit is connected; the first charge is attended the whole time and stopped if any pack passes 45 °C. Never force-charge a pack that does not answer.
- **S6. Before the canopy rails go on.** Every post bolt tight; the cabinet cannot tip: it stands on a level floor and, if outdoors, is anchored or held by ballast and straps.
- **S7. Before the cabinet goes outdoors or to a site.** The first site is private property with an existing single-phase circuit and a responsible host, not a public sidewalk. The cabinet stands on the cast pad of section 9, at least 7 days old, held by the four M12 wedge anchors, each rated for at least 3.8 kN design tension and tightened to the maker's torque; the site is away from building doors and windows with the hood slots facing away from people; a clear walkway beside it. Without the anchors and the pad a 30 m/s gust tips the cabinet with its canopy.

## 7. Tools, skills and workspace

**Tools.** Access to a sheet metal shop with a laser or punch and a folder for 1,400 mm, or a 1.5 m hand folder; MIG welder and angle grinder (or a fabricator for the plinth and posts); drill press and hand drills, drills 3 to 14 mm, step drill to 40 mm, 110 mm hole saw; blind rivet tool and rivet nut tool; M3 heat-set insert tool; files and deburring tool; tape measure, steel rule, square, spirit level and string line; spanners and sockets 8 to 19 mm with an extension long enough to reach the anchor nuts through the floor; torque wrench; 3D printer with a bed of at least 160 x 160 mm that prints a flame-retardant grade; two trestles, timber bearers, a pallet truck or engine crane; two stable work platforms for the canopy; multimeter.

**Skills.** Sheet metal marking out, drilling and riveting; MIG welding of channel, tube and plate (or a fabricator); safe lifting. All mains work is done or checked by a qualified electrician: it is not part of the maker's work. Care with lithium-ion packs to the SwapCell procedure.

**Workspace.** A floor area about 3 x 3 m with 3 m of headroom for the canopy, non-combustible and level; a separate welding and grinding area; the pack area of S4.

**Personal protective equipment.** Safety glasses, cut-resistant gloves for sheet, welding helmet, gloves and jacket, hearing protection for grinding, safety boots; a harness or guard rail if the platforms for the canopy are high enough to need one.

## 8. Where the numbers come from

- Model and fit checks: `cad/src/model.py` (`python cad/src/model.py --check`: no overlaps, 60 joints that must touch all touch; the site pad and anchors and the trial floor trays also fit, and a socket reaches every anchor nut); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/DKH-DWG-101` to `DKH-DWG-120`.
- General arrangement: `cad/drawings/DKH-DWG-001.pdf`, Rev P3.
- Calculations: `docs/04-calcs/01-sizing.md` (DKH-CAL-001 v0.6) and `docs/04-calcs/sizing.py`: mass (section 10), wind and anchors (section 11), cost (section 12), reach and canopy heights (section 9).
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (DKH-DDR-003), with DKH-DDR-001 and DKH-DDR-002; open items in `docs/06-design-decisions.md` (DKH-DEC-001).
- Requirements: `docs/03-requirements.md` (DKH-REQ-001 v0.8).

## 9. Site pad and anchors, and the trial floor tray

### 9.1 Site pad and anchors

![Figure 30. Making sketch of the site pad and anchors](../cad/drawings/DKH-DWG-120.png)

*Figure 30. Site pad and anchors making sketch (DKH-DWG-120).*

**What it is and what it is made from.** The first site is private ground, so the cabinet stands on its own cast pad rather than on whatever the host's ground happens to be. The pad is reinforced concrete, 1,400 x 1,100 x 300 mm, top level with the ground, on 100 mm of rammed gravel; it weighs about 1,110 kg. Four M12 x 160 mm stainless steel wedge anchors hold the plinth to it. With the cabinet, the pad resists tipping at a 30 m/s gust with the safety factors of the calculation note (section 11).

**How to make it.**

1. Dig a hole 1,600 x 1,300 mm and 400 mm deep; ram in 100 mm of gravel.
2. Set formwork 1,400 x 1,100 mm inside, its top level with the ground and checked with a spirit level.
3. Tie a mesh of 10 mm bars at 200 mm both ways near the bottom and another near the top, each with 40 mm of cover, on plastic chairs.
4. Cast about 0.46 m³ of concrete from 28 bags of 36 kg premix, rodded or vibrated, and float the top flat. Keep it damp and leave it for at least 7 days.
5. Set the cabinet centred on the pad. Through each anchor hole in the plinth, drill 12 mm into the concrete, 115 mm deep, and blow the hole clean.
6. Drive each anchor to 100 mm embedment, fit the washer and the tamper-resistant nut inside the channel, and tighten to the anchor maker's torque with a socket through the floor. Cap the floor holes.

**How it fits the parts next to it.** The anchors are 225 mm from the pad's ends and 330 mm from its front and back edges, which keeps them well clear of the concrete edges. Grid power comes in through the cable gland in the floor from the host's existing circuit, laid by the electrician.

**Check before moving on.** The pad is level within 3 mm; each anchor reaches its torque without spinning; safety stop S7 is met. If an engineer confirms that the host already has a slab that does the same job, the pad can be left out.

### 9.2 Trial option: vermiculite floor tray

![Figure 31. Making sketch of the vermiculite floor tray](../cad/drawings/DKH-DWG-119.png)

*Figure 31. Vermiculite floor tray making sketch (DKH-DWG-119). Trial option only.*

**What it is and what it is made from.** The first prototype keeps plain bay floors and the aerosol unit. For the later propagation trial, each bay can instead have a shallow stainless steel tray of exfoliated vermiculite on its floor, in front of the cradle, so that the trial can compare the two. It is 1 mm stainless sheet, 175 x 168 x 20 mm, holding about 0.5 L of vermiculite.

**How to make it.**

1. Cut a blank 215 x 208 mm and fold 20 mm sides up all round; rivet the corner tabs.
2. Drill two 4.1 mm holes in the bottom on the centre line, 40 mm in from the front and back walls.
3. Set the tray on the bay liner's floor, 2 mm behind the front panel and 3 mm in front of the cradle, and rivet it through the liner floor with two 4 mm stainless blind rivets.
4. Fill it with vermiculite to 2 mm below the rim.

**How it fits the parts next to it.** The rim stands 16 mm above the bottom edge of the door opening and 10 mm below the pack's connector face, so a pack still slides in over it and drops into the cradle.

**Check before moving on.** A pack dummy goes in and out without touching the tray or spilling the fill.
