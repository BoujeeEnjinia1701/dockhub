"""DockHub prototype build plan pictures (DKH-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps ...]
Sheets and steps can be limited to some numbers: python cad/src/build_plan_media.py sheets 101 104
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/DKH-DWG-101 to 118        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    cad/drawings/DKH-DWG-119 and 120       trial option (vermiculite floor tray) and site pad with anchors (2026-10-02)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
The first prototype fits bays 1 and 2; bays 3 and 4 carry blank plates.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, bay_x, derived, panel_frame, _box  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
C = build_components()
CV = build_components(variant="vermiculite")      # trial option (decided 2026-10-02)
CS = build_components(site=True)                  # site pad and anchors (decided 2026-10-02)
D = derived()
XS = bay_x()
B1 = XS[0]

COL = {"plinth": "#6B7280", "floor": "#A8A29E", "back": "#94A3B8", "side": "#CBD5E1", "boxes": "#15803D",
       "fire": "#DC2626", "shelf": "#78716C", "chargers": "#C2410C", "deck": "#A16207", "plenum": "#4B5563",
       "liners": "#64748B", "cradles": "#0E7490", "rec": "#1F2937", "catch": "#7C3AED", "locks": "#374151",
       "front": "#E7E5E4", "roof": "#B6BCC6", "beams": "#1D4ED8", "fans": "#334155", "hood": "#475569",
       "doors": "#0F766E", "gaskets": "#111827", "hinges": "#9CA3AF", "blanks": "#D6D3D1", "access": "#1F2937",
       "service": "#D1D5DB", "posts": "#374151", "rails": "#52525B", "panel": "#1E3A8A", "clamps": "#A1A1AA",
       "bolt": "#111827", "pack": "#D4A017"}


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def S(*keys):
    return _fuse([C[k].shape for k in keys if k in C])


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


# Leader-line anchors for the joint pictures: build_views points each leader at a vertex near the part's
# centre and top, which can be hidden behind another part in a close-up. jpart() records a model point
# for the leader instead; _anchor_at() then picks the part's vertex nearest to it.
_ANCH = []
_kit_anchor = bv._anchor


def _anchor_at(v):
    import numpy as np
    pt = _ANCH.pop(0) if _ANCH else None
    if pt is None:
        return _kit_anchor(v)
    return v[np.argmin(np.linalg.norm(v - np.asarray(pt, float), axis=1))]


bv._anchor = _anchor_at


def joint(parts_anchors, out, title, **kw):
    """bv.joint with an optional leader point per part: parts_anchors is a list of (Part, point or None)."""
    parts = [p for p, a in parts_anchors if bv._has_volume(p.shape)]
    _ANCH[:] = [a for p, a in parts_anchors if bv._has_volume(p.shape)]
    try:
        return bv.joint(parts, out, title, **kw)
    finally:
        _ANCH.clear()


def win(shape, x0, x1, y0, y1, z0, z1):
    """The part of a shape inside a box."""
    return shape & _box(x0, x1, y0, y1, z0, z1)


def one_bay(shape, xc=B1, pad=95):
    return win(shape, xc - pad, xc + pad, -400, 400, 0, 1600)


# ----------------------------------------------------------------- named parts, in build order
def made():
    return {
        "plinth": part("Plinth", C["plinth"].shape, COL["plinth"]),
        "floor": part("Floor pan and floor bolts", S("floor", "floor_bolts"), COL["floor"]),
        "back": part("Back panel", C["back"].shape, COL["back"]),
        "sides": part("Side panels (2)", S("side_l", "side_r"), COL["side"]),
        "boxes": part("Controller, MPPT and grid boxes", S("controller", "mppt", "grid"), COL["boxes"]),
        "fire": part("Aerosol suppression unit", C["fire"].shape, COL["fire"]),
        "shelf": part("Charger shelf", C["shelf"].shape, COL["shelf"]),
        "chargers": part("Chargers (2)", C["chargers"].shape, COL["chargers"]),
        "deck": part("Bay deck", C["deck"].shape, COL["deck"]),
        "plenum": part("Plenum wall", C["plenum"].shape, COL["plenum"]),
        "liners": part("Bay liners (2)", C["liners"].shape, COL["liners"]),
        "cradles": part("Cradles, receptacles, catch brackets", S("cradles", "receptacles", "catches"), COL["cradles"]),
        "locks": part("Solenoid locks (2)", C["locks"].shape, COL["locks"]),
        "front": part("Front panel", C["front"].shape, COL["front"]),
        "roof": part("Roof panel with beams, fans, detector", S("roof", "beams", "fans", "detector"), COL["roof"]),
        "hood": part("Vent hood", C["hood"].shape, COL["hood"]),
        "doors": part("Bay doors with hinges and gaskets (2)", S("doors", "hinges", "gaskets"), COL["doors"]),
        "blanks": part("Blank plates (2)", C["blanks"].shape, COL["blanks"]),
        "access": part("Access panel", C["access"].shape, COL["access"]),
        "service": part("Service door with hinge, lock, filter", S("service", "service_gasket", "service_hinge", "cam_lock", "filter"),
                        COL["service"]),
        "posts": part("Canopy posts (4) and post bolts", S("posts", "post_bolts"), COL["posts"]),
        "rails": part("Canopy rails (2)", C["rails"].shape, COL["rails"]),
        "panel": part("Solar panel and end clamps", S("panel", "clamps"), COL["panel"]),
    }


ORDER = ["plinth", "floor", "back", "sides", "boxes", "fire", "shelf", "chargers", "deck", "plenum", "liners", "cradles",
         "locks", "front", "roof", "hood", "doors", "blanks", "access", "service", "posts", "rails", "panel"]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    # The shell is pulled apart in place; the parts that go inside it are lined up to the right of it
    R = 1500
    off = {"plinth": (0, 0, -650), "floor": (0, 0, -380), "back": (0, 900, -150), "sides": (0, 0, 0),
           "boxes": (R, 300, -450), "fire": (R + 250, 650, 650), "shelf": (R, 0, -250), "chargers": (R, 0, -40),
           "deck": (R, 0, 120), "plenum": (R, 650, 450), "liners": (R, -200, 600), "cradles": (R, -200, 250),
           "locks": (R + 250, -350, 450), "front": (0, -900, 0), "roof": (0, 0, 300), "hood": (0, 0, 420),
           "doors": (-150, -1500, 150), "blanks": (150, -1500, 150), "access": (450, -1500, 250), "service": (0, -1500, -250),
           "posts": (0, 0, 650), "rails": (0, 0, 820), "panel": (0, 0, 980)}
    side_off = {"sides": None}
    parts = []
    for k in ORDER:
        p = M[k]
        if k == "sides":
            l = Part("Side panels (2)", C["side_l"].shape + _shift(C["side_r"].shape, -1150), COL["side"], None, (-450, 0, 0), 1.0)
            parts.append(l)
            continue
        p.explode = off[k]
        parts.append(p)
    del side_off
    return bv.overview(parts, OUT / "overview.png", "DockHub prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Two bays fitted, bays 3 and 4 blanked. Seen from the front right and above",
                       elev=14, azim=-58, size=(13, 10), dpi=140, key=True)


def _shift(shape, dx=0, dy=0, dz=0):
    from build123d import Pos
    return Pos(dx, dy, dz) * shape


# ----------------------------------------------------------------- making sketches
SHEETS = {}


def sheet(n):
    def deco(fn):
        SHEETS[n] = fn
        return fn
    return deco


def _cs(n, comp, neighbours, title, material, notes, view_shape=None, inset_view=(22, -58), date=DATE, rev="P1", revisions=None):
    return bv.component_sheet(comp, neighbours, project="DockHub", dwg_no=f"DKH-DWG-{n}", title=f"DockHub {title}: making sketch",
                              material=material, notes=notes, date=date, view_shape=view_shape, inset_view=inset_view,
                              rev=rev, revisions=revisions)


def _shell(*keys):
    M = made()
    return [M[k] for k in keys]


@sheet(101)
def s101():
    return _cs(101, part("Plinth", C["plinth"].shape, COL["plinth"]), _shell("floor"),
               "plinth", "Steel channel 100 x 50 x 5 mm (C100), painted or galvanized", [
                   "Four lengths of 100 x 50 x 5 channel: two 1,000 and two 500 mm long",
                   "  outside, ends mitred at 45 degrees, flanges pointing inward.",
                   "Weld the corners all round on a flat table; check the diagonals",
                   "  are equal within 2 mm and the top is flat within 1 mm.",
                   "Bottom flange: four 14 mm anchor holes, 25 mm in from each end",
                   "  and 30 mm in from the front and back edges. Top flange: a 32 mm",
                   "  socket hole straight above each one, so a socket reaches the nut.",
                   "Top flange: eight 11 mm holes for the M10 floor bolts: front, 25 mm",
                   "  in, at 100, 350, 650 and 900 from the left end; back, 25 mm in,",
                   "  at 520 and 680 from the left end; one each end, centred, 25 mm in.",
                   "Grind the welds flush on the top face; paint or galvanize.",
                   "Fit: the floor pan sits flat on the top flange; the walls stand on",
                   "  its edge. Anchors go into the pad at the site, not in the workshop.",
                   "Check: top flat, holes match the floor pan held over it."], inset_view=(25, -60),
               date="2026-10-02", rev="P2", revisions=[("P1", "Making sketch for the prototype build plan", DATE, "AC"),
                                                      ("P2", "Socket holes over the anchors in the top flange", "2026-10-02", "AC")])


@sheet(102)
def s102():
    return _cs(102, part("Floor pan", C["floor"].shape, COL["floor"]), _shell("plinth", "back", "sides"),
               "floor pan", "Galvanized steel sheet 1.5 mm", [
                   "Plate 997 x 497 mm with 25 mm flanges folded up on all four edges;",
                   "  the side flanges stop 25 mm short of each corner (they clear the",
                   "  front and back panel flanges). Fold the long flanges first.",
                   "Holes, measured from the centre lines (x sideways, y front-back):",
                   "  eight 11 mm bolt holes matching the plinth top flange;",
                   "  four 40 mm socket holes over the anchors, at 475 each side and",
                   "  220 each side of the centre, closed later with plastic caps;",
                   "  one 25 mm gland hole for the grid cable at x 340, y 120.",
                   "Fit: bolted to the plinth with eight M10 bolts, heads inside, nuts",
                   "  under the top flange (bolt it with the plinth on trestles).",
                   "The walls are riveted to the flanges with 4 mm blind rivets.",
                   "Check: flanges square, holes line up with the plinth."], inset_view=(30, -60))


@sheet(103)
def s103():
    return _cs(103, part("Back panel", C["back"].shape, COL["back"]), [made()["floor"], part("Left side panel", C["side_l"].shape, COL["side"]), made()["boxes"], made()["fire"]],
               "back panel", "Galvanized steel sheet 1.5 mm", [
                   "Blank 1,000 x 1,400 mm plus a 25 mm flange on each side edge,",
                   "  folded forward (toward the street side) along the full height",
                   "  less 1.5 mm at top and bottom.",
                   "Seen from the front, mark and drill as you fit the parts:",
                   "  the controller, MPPT and grid boxes screw straight to it, each by",
                   "  its own fixing holes (mark through the box), M5 with sealing washers;",
                   "  the aerosol unit's two straps, two M5 each, 1,300 to 1,340 up;",
                   "  two 9 mm holes for the roof beam cleat bolts at 410 and 430 each",
                   "  side of the centre, 1,376 up. Heights from the bottom edge.",
                   "Fit: stands on the floor pan's back flange edge; the side panels",
                   "  overlap its flanges; 4 mm blind rivets at about 100 mm pitch.",
                   "Check: flanges at 90 degrees, panel flat within 3 mm."], inset_view=(25, -60))


@sheet(104)
def s104():
    return _cs(104, part("Side panel", C["side_r"].shape, COL["side"]), _shell("floor", "back", "front", "roof"),
               "side panel (make 2)", "Galvanized steel sheet 1.5 mm", [
                   "Make two, flat, 497 x 1,400 mm; deburr and break the edges.",
                   "No holes are drilled before assembly: drill 4.1 mm rivet holes",
                   "  through the panel into each flange behind it as you fit it.",
                   "Rivet lines, 12 mm in from the edges, 100 mm pitch (heights from the ground):",
                   "  front and back edges, into the front and back panel flanges;",
                   "  bottom edge, into the floor pan flange;",
                   "  top edge, into the roof flange;",
                   "  and across the panel at 674 to 699 mm (bay deck flange),",
                   "  354 to 379 mm (charger shelf flange) and the plenum wall",
                   "  flange, 112 to 132 mm behind the centre line.",
                   "Fit: stands on the floor pan's side flange, outside every flange.",
                   "Check: the two panels are the same, square within 2 mm."], inset_view=(25, -40))


@sheet(105)
def s105():
    return _cs(105, part("Charger shelf", C["shelf"].shape, COL["shelf"]), _shell("back", "sides", "chargers"),
               "charger shelf", "Galvanized steel sheet 1.5 mm", [
                   "Plate 994 x 280 mm with 25 mm flanges folded down on all four",
                   "  edges (fold the long edges first, then the short ones).",
                   "Fit: top face 380 mm above the ground (278.5 above the floor),",
                   "  front edge 60 mm in front of the centre line, back edge 220 mm",
                   "  behind it, clear of the back panel flanges.",
                   "Its side flanges are riveted to the side panels, four rivets each.",
                   "Chargers stand on it, each held by four M5 screws through the shelf",
                   "  at the charger's own fixing holes (mark through the charger),",
                   "  at 345 and 115 left of centre for bays 1 and 2",
                   "  (115 and 345 right of centre for bays 3 and 4 later).",
                   "Check: level within 2 mm when riveted in."], inset_view=(25, -60))


@sheet(106)
def s106():
    return _cs(106, part("Bay deck", C["deck"].shape, COL["deck"]), _shell("sides", "liners", "plenum"),
               "bay deck", "Galvanized steel sheet 1.5 mm", [
                   "Plate 994 x 358.5 mm with 25 mm flanges folded down on all four",
                   "  edges; the side flanges stop 25 mm short of the front edge.",
                   "Top face 700 mm above the ground. Front edge on the front panel,",
                   "  back edge 110 mm behind the centre line (the plenum wall).",
                   "Per fitted bay (centres 392 and 196 left of the centre line):",
                   "  four 5.5 mm holes, 60 mm each side of the bay centre and",
                   "  188.5 and 308.5 mm back from the front edge (cradle screws);",
                   "  one 40 x 30 mm cable hole on the bay centre, 241.5 to 271.5 mm",
                   "  back from the front edge, with an edge grommet.",
                   "Bays 3 and 4 (on and 196 right of the centre line): drill later.",
                   "Fit: side flanges riveted to the side panels, back flange to the",
                   "  plenum wall, front flange to the front panel.",
                   "Check: flat within 2 mm across the width."], inset_view=(30, -60))


@sheet(107)
def s107():
    return _cs(107, part("Plenum wall", C["plenum"].shape, COL["plenum"]), _shell("sides", "deck", "liners"),
               "plenum wall", "Galvanized steel sheet 1.5 mm", [
                   "Plate 994 wide x 823.5 mm tall, standing 110 mm behind the centre",
                   "  line from 673.5 to 1,497 mm above the ground.",
                   "Top flange 20 mm folded forward over 876 mm of the width; side",
                   "  flanges 20 mm folded back, stopping 42 mm below the top.",
                   "Notch both top corners 44 wide x 41 deep, starting 15 mm in from",
                   "  the side edge: the roof beams pass through the notches.",
                   "Vent port per fitted bay: 60 x 60 mm on the bay centre, 466.5 to",
                   "  526.5 mm up from the bottom edge (1,140 to 1,200 above ground).",
                   "Fit: bottom edge riveted to the bay deck's back flange; side flanges",
                   "  to the side panels; top flange to the roof; each liner back",
                   "  riveted to it round the port. Seal the notches with fire-rated",
                   "  sealant once the roof is on.",
                   "Check: the ports line up with the liner ports."], inset_view=(20, -50))


@sheet(108)
def s108():
    ln = one_bay(C["liners"].shape)
    return _cs(108, part("Bay liner", ln, COL["liners"]), _shell("deck", "plenum", "front"),
               "bay liner (make 2)", "Galvanized steel sheet 1.5 mm", [
                   "A box 180 wide, 358.5 deep and 530 tall, open at the front.",
                   "Fold the sides and back from one blank (a U); rivet in a folded",
                   "  floor and top. Fold a 15 mm flange up along the top front edge.",
                   "Back: a 60 x 60 mm vent port, centred, 440 to 500 mm up.",
                   "Floor: four 5.5 mm holes 60 mm each side of the centre, 188.5",
                   "  and 308.5 mm back from the front edge; a 40 x 30 mm cable hole",
                   "  on the centre, 241.5 to 271.5 mm back from the front edge.",
                   "Right wall: two 4.5 mm holes for the solenoid lock, 10 and 25 mm",
                   "  back from the front edge, 260 mm up (mark through the lock).",
                   "Fit: stands on the deck; the top flange is riveted to the back of",
                   "  the front panel above the door opening; the back is riveted to",
                   "  the plenum wall round the port. 16 mm air gap to the next liner.",
                   "Check: square; the port lines up with the plenum wall port."], inset_view=(25, -50))


@sheet(109)
def s109():
    cr = one_bay(C["cradles"].shape)
    return _cs(109, part("Cradle", cr, COL["cradles"]), [part("Bay deck", win(C["deck"].shape, B1 - 120, B1 + 120, -260, 120, 600, 710), COL["deck"]),
                                                          part("Pack", one_bay(C["packs"].shape), COL["pack"])],
               "cradle with guides (print 2)", "Flame-retardant filament, UL 94 V-0, 100 % infill", [
                   "Print one piece: a base 150 x 150 x 28.5 mm with two side guides",
                   "  5 x 90 x 130 mm on top, 46 to 51 mm each side of the centre.",
                   "Plug well, open on top: 58 x 36 x 19.5 mm deep, centred 8 mm",
                   "  behind the cradle centre (toward the plenum).",
                   "Receptacle pocket, open underneath: 72 x 50 x 9 mm, same centre.",
                   "Catch slot: 62 x 4 x 10 mm deep, 58.5 to 62.5 mm behind the centre.",
                   "Four 5.5 mm holes 60 mm each side of the centre, front and back.",
                   "Two heat-set M3 inserts from below for the receptacle flange.",
                   "Fit: the receptacle screws in from below, then the cradle stands on",
                   "  the liner floor on four M5 screws through liner and deck, nuts",
                   "  under the deck. The pack's plug drops into the well.",
                   "Check: a pack dummy 90 x 80 mm slides between the guides freely."], inset_view=(30, -55))


@sheet(110)
def s110():
    ca = one_bay(C["catches"].shape)
    return _cs(110, part("Catch bracket", ca, COL["catch"]), [part("Cradle", one_bay(C["cradles"].shape), COL["cradles"]),
                                                               part("Pack", one_bay(C["packs"].shape), COL["pack"])],
               "catch bracket (make 2)", "Steel strip 60 x 3 mm; catch block 50 x 8 x 8 mm steel", [
                   "Cut 60 x 3 mm strip about 430 mm long; deburr.",
                   "Bend 90 degrees twice: an upright 335 mm tall, a top leg 49.5 mm",
                   "  long reaching back, and a tab 43 mm long turned down.",
                   "Tab: two 4.5 mm holes, 20 mm apart, for M4 screws through the",
                   "  liner back wall.",
                   "Catch block 50 x 8 x 8 mm: rivet or screw it to the front face of",
                   "  the upright, its underside 318 mm above the upright's bottom end.",
                   "  It sits 1 mm behind the pack's latch pawl and just above it.",
                   "Fit: the bottom end stands 10 mm down in the cradle's catch slot;",
                   "  the tab is screwed to the liner back wall.",
                   "Check: with a pack dummy in the cradle the pawl passes under the",
                   "  catch with the 1 mm gap, and the upright is vertical."], inset_view=(20, 60))


@sheet(111)
def s111():
    return _cs(111, part("Front panel", C["front"].shape, COL["front"]), _shell("sides", "deck", "liners"),
               "front panel", "Galvanized steel sheet 1.5 mm, laser cut", [
                   "Blank 1,000 x 1,400 mm, laser cut, with a 25 mm flange folded back",
                   "  on each side edge (full height less 1.5 mm at top and bottom).",
                   "Heights from the bottom edge, sideways from the centre line:",
                   "  four bay openings 150 x 510, 605 to 1,115 up, centred at 392",
                   "  and 196 left, on the centre line, and 196 right;",
                   "  service opening 900 x 500, centred, 50 to 550 up;",
                   "  access cut-out 120 x 300, 340 to 460 right, 780 to 1,080 up.",
                   "Cleat bolt holes 9 mm at 410 and 430 each side, 1,376 up.",
                   "Drill hinge, gasket and blank plate holes at assembly.",
                   "Fit: overlaps the liner top flanges and the deck front flange,",
                   "  riveted; its side flanges sit inside the side panels.",
                   "Check: openings square and in line; 46 mm of panel between",
                   "  neighbouring door openings."], inset_view=(20, -60))


@sheet(112)
def s112():
    return _cs(112, part("Roof panel", C["roof"].shape, COL["roof"]), _shell("sides", "back", "front", "hood"),
               "roof panel", "Galvanized steel sheet 1.5 mm", [
                   "Plate 997 x 497 mm with 40 mm flanges folded down on all four",
                   "  edges; the side flanges stop 25 mm short of each corner.",
                   "Holes, sideways from the centre line and back from the centre:",
                   "  two 110 mm fan holes at 350 each side, 173 back;",
                   "  eight 11 mm post bolt holes at 460 each side, 165 and 235",
                   "  front and back of the centre;",
                   "  one 25 mm gland hole for the panel cable at 200 left, 60 back.",
                   "Front and back flanges: two 9 mm cleat bolt holes at 410 and 430",
                   "  each side, 18 mm up from the flange's lower edge.",
                   "Fit: drops in from above inside the four walls; flanges riveted to",
                   "  the walls, sealed with mastic; the plate's top is flush with the",
                   "  wall tops. The beams, fans and detector are fitted first.",
                   "Check: drops in without forcing; all post holes over the beams."], inset_view=(35, -60))


@sheet(113)
def s113():
    bm = win(C["beams"].shape, 300, 500, -300, 300, 1400, 1600)
    return _cs(113, part("Roof beam", bm, COL["beams"]), [part("Roof", C["roof"].shape, COL["roof"])],
               "roof beam with cleats (make 2)", "Steel angle 40 x 40 x 4 mm, painted", [
                   "Beam: 494 mm of 40 x 40 x 4 angle, ends touching the roof flanges.",
                   "  Horizontal leg: four 11 mm holes 20 mm from the heel, 12 and",
                   "  82 mm from each end.",
                   "Cleats: four 36 mm lengths of the same angle per cabinet.",
                   "  One leg bolts to the beam's upright leg with two M8 bolts;",
                   "  the other carries two welded M8 nuts, 20 mm apart, for the bolts",
                   "  that come through the front (or back) panel and roof flange.",
                   "Drill the beam's upright leg and the cleat together (9 mm).",
                   "Fit: the horizontal leg lies flat under the roof plate on the post",
                   "  line, 460 mm each side of the centre, heel on the inner side;",
                   "  the post bolts pass through roof and beam, nuts under the beam.",
                   "  The cleats bear on the roof's front and back flanges.",
                   "Check: the four bolt holes line up with the roof's post holes."], inset_view=(-35, -60))


@sheet(114)
def s114():
    return _cs(114, part("Vent hood", C["hood"].shape, COL["hood"]), [part("Roof", C["roof"].shape, COL["roof"]),
                                                                       part("Fans", C["fans"].shape, COL["fans"])],
               "vent hood", "Galvanized steel sheet 1.5 mm", [
                   "A box 850 wide, 133 deep and 70 tall, open underneath, folded",
                   "  from sheet: front wall with a 20 mm flange forward; end walls",
                   "  with 8 mm flanges outward; back wall with a 15 mm flange",
                   "  backward; top overhanging the back wall by 10 mm (rain lip).",
                   "Back wall: twelve slots 50 x 40 mm, 12 mm above the roof, on a",
                   "  71.8 mm pitch starting 30 mm from each end.",
                   "Fit: stands on the roof over both fan holes, front face 98.5 mm",
                   "  behind the centre line; flanges riveted and sealed to the roof.",
                   "  Air and any vented gas leave through the back slots, away from",
                   "  the rider side.",
                   "Fit insect mesh behind the slots.",
                   "Check: both fan holes fully inside the hood."], inset_view=(25, 130))


@sheet(115)
def s115():
    dr = one_bay(S("doors"))
    return _cs(115, part("Bay door", dr, COL["doors"]), [part("Front panel", win(C["front"].shape, -700, 0, -300, 0, 600, 1300), COL["front"]),
                                                       part("Hinge", one_bay(C["hinges"].shape), COL["hinges"])],
               "bay door (make 2) and blank plate (make 2)", "Steel plate 2 mm, powder coated", [
                   "Door: 172 x 526 x 2 mm plate; round the corners 3 mm.",
                   "Pull handle on the front, 45 to 70 mm right of the door centre,",
                   "  243 to 283 mm up from the door's bottom edge.",
                   "Lock tongue: a 4 mm steel angle riveted to the back; its tongue",
                   "  stands 21 mm back, 50 to 54 mm right of centre, 253 to 273 mm",
                   "  up, with a 6 mm hole for the lock bolt.",
                   "Hinge: a stainless piano hinge 480 mm long, riveted to the door's",
                   "  front face along its left edge and to the front panel beside it.",
                   "Gasket: 7 x 3 mm closed-cell EPDM strip stuck to the panel round",
                   "  the opening, 1 mm out from its edge.",
                   "Blank plate: the same 172 x 526 plate with four 5.5 mm holes",
                   "  for M5 security screws into rivet nuts in the panel.",
                   "Check: the door closes on the gasket evenly, tongue in the lock."], inset_view=(15, -60))


@sheet(116)
def s116():
    return _cs(116, part("Service door", S("service", "filter"), COL["service"]), [part("Front panel", C["front"].shape, COL["front"])],
               "service door", "Steel plate 2 mm, powder coated", [
                   "Plate 920 x 520 x 2 mm; round the corners 3 mm.",
                   "Intake slot 400 x 80 mm, centred, 30 to 110 mm up from the",
                   "  bottom edge; a 410 x 90 x 10 mm filter pad held behind it by",
                   "  a folded sheet clip frame (four rivets).",
                   "Cam lock: 19 mm hole 420 mm right of centre, 260 mm up; the cam",
                   "  arm turns behind the panel edge, 60 mm long.",
                   "Hinge: stainless piano hinge 460 mm long, riveted to the door's",
                   "  front along its left edge and to the panel beside the opening.",
                   "Gasket: 7 x 3 mm EPDM strip round the opening, 1 mm out from it.",
                   "Fit: covers the 900 x 500 opening with 10 mm overlap all round.",
                   "Check: the cam pulls the door tight onto the gasket."], inset_view=(20, -60))


@sheet(117)
def s117():
    ps = win(C["posts"].shape, 400, 520, -260, -100, 1450, 2400)
    return _cs(117, part("Canopy post", ps, COL["posts"]), [part("Roof", C["roof"].shape, COL["roof"]),
                                                         part("Rail", C["rails"].shape, COL["rails"])],
               "canopy post (make 4)", "Square steel tube 50 x 50 x 3 mm; plate 8 and 6 mm", [
                   "Front posts (2) 766 mm and rear posts (2) 696 mm long on their",
                   "  centre line; cut the top end at 10 degrees, sloping down to the back.",
                   "Base plate 50 x 100 x 8 mm, the post centred on it 25 mm from",
                   "  the outer end; two 11 mm holes on its centre line, 15 and 85 mm",
                   "  from the outer end (235 and 165 mm from the cabinet centre).",
                   "Cap plate 50 x 70 x 6 mm on the sloping top, two 9 mm holes for",
                   "  the rail bolts, 40 mm apart along the slope.",
                   "Weld both plates all round; paint.",
                   "Fit: base plate flat on the roof over the beam, two M10 bolts",
                   "  through plate, roof and beam, nuts under the beam.",
                   "  The rail sits on the cap plate on two M8 bolts.",
                   "Check: post square to the base plate within 1 degree."], inset_view=(20, -50))


@sheet(118)
def s118():
    F = panel_frame()
    rl = win(C["rails"].shape, 300, 600, -900, 600, 1500, 2600)
    flat = F.inverse() * rl
    return _cs(118, part("Canopy rail", rl, COL["rails"]), [part("Posts", C["posts"].shape, COL["posts"]),
                                                         part("Panel", C["panel"].shape, COL["panel"])],
               "canopy rail (make 2)", "Rectangular steel tube 50 x 40 x 3 mm, painted", [
                   "Cut two 1,174 mm lengths of 50 x 40 x 3 tube, 40 mm side up.",
                   "Post bolt holes, 9 mm through both walls, two at each post, 40 mm",
                   "  apart: centred 547 mm (front post) and 954 mm (rear post) from",
                   "  the front end.",
                   "End clamp holes, 9 mm in the top wall, 10 mm from each end.",
                   "Cap both ends with plastic tube caps.",
                   "Fit: the rails run up the slope at 460 mm each side of the centre,",
                   "  20 mm past the panel's front and back edges; the panel frame",
                   "  sits on them and four solar end clamps hold its front and back",
                   "  edges. The slope is 10 degrees, high at the street side.",
                   "Check: both rails in one plane (string line across the tops)."], view_shape=flat, inset_view=(-25, -50))


@sheet(119)
def s119():
    xc = B1
    tray = win(CV["verm_trays"].shape, xc - 95, xc + 95, -400, 0, 690, 760)
    fill = win(CV["verm_fill"].shape, xc - 95, xc + 95, -400, 0, 690, 760)
    low = lambda sh: win(sh, xc - 95, xc + 95, -400, 400, 690, 790)  # noqa: E731  lower part only, so the tray shows
    nb = [part("Bay liner", low(C["liners"].shape), COL["liners"]), part("Cradle", low(C["cradles"].shape), COL["cradles"]),
          part("Vermiculite fill", fill, "#C8A165")]
    return _cs(119, part("Vermiculite floor tray", tray, "#94A3B8"), nb,
               "vermiculite floor tray (trial option, make 1 per bay)", "Stainless steel sheet 1 mm; exfoliated vermiculite", [
                   "TRIAL OPTION for the propagation trial only. The first prototype",
                   "  keeps plain bay floors and the aerosol unit.",
                   "Blank 215 x 208 mm; fold 20 mm sides up all round to give a tray",
                   "  175 wide, 168 front to back and 20 deep; rivet the corner tabs.",
                   "Two 4.1 mm holes in the bottom, on the centre line, 40 mm in from",
                   "  the front and back walls.",
                   "Fit: on the bay liner floor, 2 mm behind the front panel and 3 mm",
                   "  in front of the cradle, 1 mm clear of each liner wall; two 4 mm",
                   "  stainless blind rivets through tray and liner floor.",
                   "Fill with exfoliated vermiculite to 2 mm below the rim, about",
                   "  0.5 L; top up through the bay door after each trial burn.",
                   "Check: the rim is 16 mm above the door opening's bottom edge and",
                   "  10 mm below the pack's connector face, so the pack slides over."],
               inset_view=(50, -60), date="2026-10-02")


@sheet(120)
def s120():
    pad = CS["pad"].shape
    anc = CS["anchors"].shape
    return _cs(120, part("Concrete pad", pad, "#A8A29E"), [part("Plinth", C["plinth"].shape, COL["plinth"]),
                                                          part("M12 anchors (4)", anc, COL["bolt"])],
               "site pad and anchors", "Reinforced concrete C25/30; M12 stainless wedge anchors", [
                   "SITE WORK, after the cabinet is built (safety stop S7).",
                   "Dig 400 mm deep, 1,600 x 1,300 mm; ram 100 mm of gravel in.",
                   "Formwork 1,400 x 1,100 mm inside, top level with the ground.",
                   "10 mm bars at 200 mm both ways, 40 mm from the bottom and the",
                   "  top, on chairs; cast 0.46 m3 from 28 bags of 36 kg premix,",
                   "  vibrated or rodded; keep it damp and wait 7 days.",
                   "Set the cabinet centred on the pad. Through the plinth's anchor",
                   "  holes, drill 12 mm, 115 mm deep; blow the holes clean.",
                   "Drive four M12 x 160 stainless wedge anchors to 100 mm",
                   "  embedment; washer and tamper-resistant nut inside the channel;",
                   "  tighten to the maker's torque with a socket through the floor.",
                   "Anchors 225 mm from the pad ends, 330 mm from front and back.",
                   "Check: each anchor rated for 3.8 kN design tension or more."],
               inset_view=(25, -60), date="2026-10-02")


def sheets(nums=None):
    out = []
    for n in sorted(SHEETS):
        if nums and n not in nums:
            continue
        out.append(SHEETS[n]())
        print("sheet", n)
    return out


# ----------------------------------------------------------------- joints
def joints(nums=None):
    import build123d as b
    out = []
    want = lambda n: not nums or n in nums  # noqa: E731
    Z0, Z1, t = P["plinth_h"], P["roof_z"], P["sheet_t"]
    if want(1):
        bx = (360, 500, -250, -120, -5, 160)
        out.append(joint([
            (part("Plinth: anchor hole, socket hole above it", win(C["plinth"].shape, *bx), COL["plinth"]), (470, -150, 5)),
            (part("Floor pan with anchor socket hole", win(C["floor"].shape, *bx), COL["floor"]), (420, -160, 101.5)),
            (part("M10 floor bolt", win(C["floor_bolts"].shape, *bx), COL["bolt"]), (400, -225, 108)),
            (part("Side panel", win(C["side_r"].shape, *bx), COL["side"]), (499, -140, 150)),
            (part("Front panel", win(C["front"].shape, *bx), COL["front"]), (380, -249, 150))],
            OUT / "joint-01.png", "Joint 1: plinth corner, floor pan and walls (front right corner)",
            subtitle="Seen from inside the cabinet. A socket reaches the anchor nut through the floor and the plinth's top flange",
            elev=35, azim=130, size=(8, 6)))
    if want(2):
        bx = (440, 505, -255, -180, 676, 697)
        out.append(joint([
            (part("Front panel", win(C["front"].shape, *bx), COL["front"]), (460, -249, 697)),
            (part("Front panel side flange", win(win(C["front"].shape, 496, 499, -248.5, -180, 0, 2000), *bx), "#A8A29E"), (498, -230, 697)),
            (part("Side panel", win(C["side_r"].shape, *bx), COL["side"]), (499, -195, 697)),
            (part("Bay deck front flange", win(win(C["deck"].shape, 0, 497, -250, -245, 0, 2000), *bx), COL["deck"]), (455, -248, 697)),
            (part("Bay deck side flange (starts 25 mm back)", win(win(C["deck"].shape, 496.9, 499, -224, 200, 0, 2000), *bx), "#D97706"), (498, -190, 697))],
            OUT / "joint-02.png", "Joint 2: panel corner at the bay deck (front right, cut just under the deck)",
            subtitle="Seen from above. The front panel flange lies inside the side panel; the deck flanges lie on both; blind rivets",
            elev=88, azim=-90, size=(8, 6)))
    if want(3):
        xc = B1
        bx = (xc - 100, xc, -260, 130, 680, 1260)
        out.append(joint([
            (part("Front panel", win(C["front"].shape, *bx), COL["front"]), (xc - 90, -250, 1240)),
            (part("Bay liner (cut on its centre), top flange", win(C["liners"].shape, *bx), COL["liners"]), (xc - 20, -248, 1243)),
            (part("Bay deck", win(C["deck"].shape, *bx), COL["deck"]), (xc - 10, -100, 699)),
            (part("Plenum wall with vent port", win(C["plenum"].shape, *bx), COL["plenum"]), (xc - 10, 111, 1220)),
            (part("Cradle", win(C["cradles"].shape, *bx), COL["cradles"]), (xc - 10, -60, 728))],
            OUT / "joint-03.png", "Joint 3: bay liner on the deck, front panel and plenum wall (bay 1, cut)",
            subtitle="Seen from the front right. Top flange riveted to the front panel; back riveted round the vent port",
            elev=18, azim=-35, size=(8, 6)))
    if want(4):
        xc = B1
        bx = (xc - 100, xc, -60, 115, 695, 1110)
        out.append(joint([
            (part("Bay liner", win(C["liners"].shape, *bx), COL["liners"]), (xc - 50, 109, 1100)),
            (part("Cradle with guides (printed)", win(C["cradles"].shape, *bx), COL["cradles"]), (xc, -50, 725)),
            (part("Receptacle", win(C["receptacles"].shape, *bx), COL["rec"]), (xc, 0, 705)),
            (part("Catch bracket and catch", win(C["catches"].shape, *bx), COL["catch"]), (xc, 85, 1055)),
            (part("SwapCell pack (latch pawl at the back)", win(C["packs"].shape, *bx), COL["pack"]), (xc, 0, 900)),
            (part("Bay deck", win(C["deck"].shape, *bx), COL["deck"]), (xc, 100, 699))],
            OUT / "joint-04.png", "Joint 4: cradle, receptacle and catch bracket (bay 1, cut on its centre)",
            subtitle="Seen from the right. The plug sits in the well; the catch stands just above the pack's latch pawl",
            elev=8, azim=0, size=(8, 7)))
    if want(5):
        xc = XS[1]
        bx = (xc - 105, xc + 95, -275, -205, 940, 975)
        out.append(joint([
            (part("Front panel", win(C["front"].shape, *bx), COL["front"]), (xc + 85, -249, 975)),
            (part("Bay door with handle and lock tongue", win(C["doors"].shape, *bx), COL["doors"]), (xc, -255, 975)),
            (part("Gasket", win(C["gaskets"].shape, *bx), COL["gaskets"]), (xc + 80, -251, 975)),
            (part("Piano hinge", win(C["hinges"].shape, *bx), COL["hinges"]), (xc - 90, -256, 975)),
            (part("Solenoid lock", win(C["locks"].shape, *bx), COL["locks"]), (xc + 70, -225, 975)),
            (part("Bay liner wall", win(C["liners"].shape, *bx), COL["liners"]), (xc + 89, -212, 975))],
            OUT / "joint-05.png", "Joint 5: bay door, hinge, gasket and lock (bay 2, cut at lock height)",
            subtitle="Seen from above, street side at the bottom. The tongue passes inside the gasket into the lock",
            elev=88, azim=-90, size=(9, 6)))
    if want(6):
        px = P["post_x"]
        bx = (395, px, -253, -140, 1445, 1560)
        out.append(joint([
            (part("Front panel", win(C["front"].shape, *bx), COL["front"]), (px, -250, 1450)),
            (part("Roof panel and its front flange", win(C["roof"].shape, *bx), COL["roof"]), (px, -150, 1500)),
            (part("Roof beam (cut) and cleat with weld nuts", win(C["beams"].shape, *bx), COL["beams"]), (px, -200, 1494)),
            (part("Post base plate and post (cut)", win(C["posts"].shape, *bx), COL["posts"]), (px, -200, 1560)),
            (part("M10 post bolts, nuts under the beam", win(C["post_bolts"].shape, *bx), COL["bolt"]), (px, -165, 1515))],
            OUT / "joint-06.png", "Joint 6: roof beam, cleat and front post base (right side, cut on the post line)",
            subtitle="Seen from the right, street side on the left. Cleat bolts come in through the front panel and roof flange",
            elev=12, azim=-15, size=(8, 6)))
    if want(7):
        F = panel_frame()
        from model import post_geometry
        x, y, zb, zt, ly = post_geometry()[3]
        bx = (400, 520, 120, 300, 2120, 2330)
        out.append(bv.joint([
            part("Rear post with cap plate", win(C["posts"].shape, *bx), COL["posts"]),
            part("Rail", win(C["rails"].shape, *bx), COL["rails"]),
            part("Solar panel frame", win(C["panel"].shape, *bx), COL["panel"])],
            OUT / "joint-07.png", "Joint 7: rear post top, cap plate and rail (right side)",
            subtitle="Seen from the right and below. The cap plate is cut to the 10 degree slope; two M8 bolts",
            elev=-10, azim=10, size=(8, 6)))
        bx = (380, 540, -760, -600, 2300, 2500)
        out.append(bv.joint([
            part("Rail end", win(C["rails"].shape, *bx), COL["rails"]),
            part("Panel frame (front edge)", win(C["panel"].shape, *bx), COL["panel"]),
            part("End clamp", win(C["clamps"].shape, *bx), COL["clamps"])],
            OUT / "joint-08.png", "Joint 8: panel end clamp on the rail (front right corner)",
            subtitle="The clamp grips the panel frame's edge against the rail; one M8 bolt into the rail",
            elev=25, azim=-30, size=(8, 6)))
    if want(9):
        fx = P["fan_x"]
        bx = (fx - 110, fx, 60, 255, 1440, 1590)
        out.append(joint([
            (part("Vent hood (cut), slots in its back face", win(C["hood"].shape, *bx), COL["hood"]), (fx, 160, 1570)),
            (part("Fan on 4 mm spacers (cut)", win(C["fans"].shape, *bx), COL["fans"]), (fx, 150, 1470)),
            (part("Roof panel (cut through the fan hole)", win(C["roof"].shape, *bx), COL["roof"]), (fx, 80, 1500)),
            (part("Plenum wall top flange", win(C["plenum"].shape, *bx), COL["plenum"]), (fx, 100, 1497)),
            (part("Back panel", win(C["back"].shape, *bx), COL["back"]), (fx, 249, 1460))],
            OUT / "joint-09.png", "Joint 9: roof fan and vent hood (right fan, cut through its centre)",
            subtitle="Seen from the right, street side on the left. The fan blows up through the roof, into the hood and out at the back",
            elev=12, azim=-10, size=(8, 6)))
    if want(10):
        bx = (370, 505, -275, -238, 388, 412)
        out.append(joint([
            (part("Front panel and its side flange", win(C["front"].shape, *bx), COL["front"]), (480, -249, 412)),
            (part("Service door", win(C["service"].shape, *bx), COL["service"]), (380, -255, 412)),
            (part("Gasket", win(C["service_gasket"].shape, *bx), COL["gaskets"]), (455, -252, 412)),
            (part("Cam lock knob, barrel and cam arm", win(C["cam_lock"].shape, *bx), COL["locks"]), (460, -245, 410))],
            OUT / "joint-10.png", "Joint 10: service door cam lock (cut at lock height)",
            subtitle="Seen from above, street side at the bottom. The cam arm turns behind the panel edge and pulls the door onto the gasket",
            elev=60, azim=-75, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(nums=None):
    M = made()
    out = []

    def st(n, done, new, title, sub, **kw):
        if nums and n not in nums:
            return
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))
        print("step", n)

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)
    a = dict(elev=20, azim=-55)
    pl = [M["plinth"]]
    st(1, pl, [mv(M["floor"], (0, 0, 300))], "floor pan onto the plinth",
       "Plinth on trestles. Eight M10 bolts down through floor and top flange, nuts from below", label_done=True, **a)
    base = pl + [M["floor"]]
    st(2, base, [mv(M["back"], (0, 400, 0))], "back panel",
       "Stand it on the floor pan's back flange edge; clamp; blind rivets through the floor flange", label_done=False, **a)
    st(3, base + [M["back"]], [mv(part("Left side panel", C["side_l"].shape, COL["side"]), (-400, 0, 0)),
                               mv(part("Right side panel", C["side_r"].shape, COL["side"]), (400, 0, 0))],
       "side panels", "Outside the back panel and floor flanges; blind rivets at about 100 mm pitch", label_done=False, **a)
    shell = base + [M["back"], M["sides"]]
    shell_cut = base + [M["back"], part("Left side panel", C["side_l"].shape, COL["side"])]
    st(4, shell_cut, [mv(M["boxes"], (0, -350, 0))], "controller, MPPT and grid boxes onto the back panel",
       "Right side panel hidden. M5 screws through the back panel with sealing washers", label_done=False, elev=18, azim=-40)
    st(5, shell_cut + [M["boxes"]], [mv(M["fire"], (0, -350, 0))], "aerosol suppression unit",
       "On its two straps, M5 screws through the back panel, just under the roof line", label_done=False, elev=18, azim=-40)
    inside = [M["boxes"], M["fire"]]
    st(6, shell_cut + inside, [mv(M["shelf"], (0, -500, 0))], "charger shelf",
       "Slide in from the front; side flanges riveted to both side panels, 380 mm up", label_done=False, elev=18, azim=-40)
    st(7, shell_cut + inside + [M["shelf"]], [mv(M["chargers"], (0, -400, 0))], "chargers onto the shelf",
       "Four M5 screws each through the shelf; bays 1 and 2 only in the first prototype", label_done=False, elev=22, azim=-40)
    low = shell_cut + inside + [M["shelf"], M["chargers"]]
    st(8, low, [mv(M["deck"], (0, -500, 0))], "bay deck",
       "700 mm up; side flanges riveted to the side panels; drill the bay holes first", label_done=False, elev=22, azim=-40)
    st(9, low + [M["deck"]], [mv(M["plenum"], (0, 0, 500))], "plenum wall",
       "Lower in from above; bottom edge riveted to the deck's back flange, side flanges to the side panels",
       label_done=False, elev=22, azim=-40)
    mid = low + [M["deck"], M["plenum"]]
    st(10, mid, [mv(M["liners"], (0, -450, 0))], "bay liners",
       "Slide back onto the deck until the back meets the plenum wall; rivet round the vent ports",
       label_done=False, elev=22, azim=-40)
    st(11, mid + [M["liners"]], [mv(part("Receptacles, then cradles", S("cradles", "receptacles"), COL["cradles"]), (0, -350, 0)),
                                 mv(part("Catch brackets", C["catches"].shape, COL["catch"]), (0, -350, 150))],
       "cradles, receptacles and catch brackets",
       "Receptacle into the cradle from below; cradle on four M5 screws, nuts under the deck; catch tab screwed to the liner back",
       label_done=False, elev=22, azim=-40)
    st(12, mid + [M["liners"], M["cradles"]], [mv(M["locks"], (0, -300, 0))], "solenoid locks",
       "Two M4 screws each through the liner's right wall, bolt toward the door opening", label_done=False, elev=22, azim=-40)
    pre = shell + inside + [M["shelf"], M["chargers"], M["deck"], M["plenum"], M["liners"], M["cradles"], M["locks"]]
    st(13, pre, [mv(M["front"], (0, -500, 0))], "front panel",
       "Flanges inside the side panels; blind rivets into the side panels, deck flange and liner top flanges",
       label_done=False, **a)
    roof_parts = [mv(part("Roof beams with cleats", C["beams"].shape, COL["beams"]), (0, 0, -250)),
                  mv(part("Fans on spacers", C["fans"].shape, COL["fans"]), (0, 0, -150)),
                  mv(part("Heat and smoke detector", C["detector"].shape, "#F87171"), (0, 0, -150))]
    st(14, [part("Roof panel (upside down view)", C["roof"].shape, COL["roof"])], roof_parts, "build the roof sub-assembly",
       "Seen from below. Beams held by the post bolts loosely; fans on M4 screws and 4 mm spacers; detector",
       label_done=True, elev=-35, azim=-55)
    closed = pre + [M["front"]]
    st(15, closed, [mv(M["roof"], (0, 0, 400))], "roof onto the cabinet",
       "Lower in from above; flanges riveted and sealed; cleat bolts in from the front and back into the weld nuts",
       label_done=False, **a)
    top = closed + [M["roof"]]
    st(16, top, [mv(M["hood"], (0, 0, 250))], "vent hood",
       "Seen from behind. Over the two fan holes; flanges riveted and sealed to the roof; slots face the back", label_done=False, elev=25, azim=55)
    st(17, top + [M["hood"]], [mv(M["doors"], (0, -350, 0)), mv(M["blanks"], (0, -350, 0))],
       "bay doors and blank plates",
       "Gasket round each opening; piano hinge riveted on the left; blank plates on four M5 security screws",
       label_done=False, **a)
    st(18, top + [M["hood"], M["doors"], M["blanks"]], [mv(M["access"], (0, -300, 0))], "access panel",
       "Over its cut-out; security screws into rivet nuts; reader and display leads through the cut-out",
       label_done=False, **a)
    body = top + [M["hood"], M["doors"], M["blanks"], M["access"]]
    st(19, body, [mv(M["service"], (0, -400, 0))], "service door",
       "Gasket round the opening; piano hinge riveted on the left; cam lock; filter pad behind the intake slot",
       label_done=False, **a)
    full = body + [M["service"]]
    st(20, full, [mv(M["posts"], (0, 0, 350))], "canopy posts",
       "Base plates over the beams; two M10 bolts each through plate, roof and beam; sealing washers",
       label_done=False, **a)
    st(21, full + [M["posts"]], [mv(M["rails"], (0, 0, 300))], "canopy rails",
       "On the cap plates, two M8 bolts at each post; check both rails lie in one plane", label_done=False, **a)
    st(22, full + [M["posts"], M["rails"]], [mv(M["panel"], (0, 0, 300))], "solar panel",
       "Two people. Panel frame on the rails, high edge to the street; four end clamps; cable through the roof gland",
       label_done=False, **a)
    return out


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "joints", "steps"]
    what = [a for a in args if not a.isdigit()]
    nums = [int(a) for a in args if a.isdigit()] or None
    fns = {"overview": lambda: overview(), "sheets": lambda: sheets(nums), "joints": lambda: joints(nums), "steps": lambda: steps(nums)}
    for w in what:
        r = fns[w]()
        print(w, "->", r)
