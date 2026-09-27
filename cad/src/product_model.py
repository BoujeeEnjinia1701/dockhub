"""DockHub product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders of the four-bay fit: a folded steel cabinet with
rounded corners, rivet rows, side intake slots and a dark header sign; four teal bay doors, each
with a clear window onto its SwapCell pack, a gasket outline, hinges, a pull handle, a bay number
and a status light (bays 2 and 3 green, charged; bay 4 amber, charging); the access column with a
lit display, an NFC reader with a lit ring and four bay status lights; the service door with
intake louvers, a cam lock and warning labels; the roof louver with its rain hood; and the
technical compartment (chargers with fins on their rack, controller, grid unit, MPPT controller),
fire unit, plenum and fans for the exploded view. The 400 W canopy is in group "accessory" so the
detail view can frame the cabinet without it. Context is a compact paved sidewalk patch with a curb
and the shared clay mannequin, standing at bay 1 with a charged pack just lifted out by its handle;
bay 1's door is open and its cradle is empty.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS and the helpers in model.py (cabinet, bay
openings and doors, bay compartments, SwapCell v0.3 pack envelope, access panel, service door,
louver, canopy, plinth). Axes as model.py: X along the cabinet width, Y front (-Y, street side) to
back, Z up from the sidewalk. The scene shows packs in bays 2 to 4 (model.py leaves the last bay
empty); see docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))

from build123d import (Axis, Box, Compound, Cylinder, Plane, Pos, Rot, Sphere, Text, extrude, fillet)
from model import PARAMS, bay_x, pack_z0, _box as B

TITLE = "DockHub: street-side battery swap and charging station"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 22, "az": -38,
     "note": "Product render from the front right and above (about 22 deg elevation); rider at left lifting a "
             "charged pack from the open bay 1, packs behind the door windows of bays 2 to 4, access panel "
             "with its lit display at right, solar canopy overhead"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): canopy and solar panel, "
             "cabinet, bay doors, bay compartments and packs, access panel, chargers and rack, controller, "
             "grid unit, MPPT controller, fire unit, plenum and fans, service door, plinth"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 12, "az": -30,
     "note": "Detail from the front right, slightly above (about 12 deg elevation): the cabinet without canopy "
             "or street; bay 1 open with its empty cradle, packs behind the windows of bays 2 to 4 and the "
             "access panel with display, NFC reader and bay status lights"},
]

# Scene settings (render only)
OPEN_BAY = 0                   # index of the bay shown open with its pack in the rider's hand (bay 1)
DOOR_OPEN_DEG = 100.0
BAY_LIGHTS = ["off", "green", "green", "amber"]
RIDER_AT = (-375.0, -345.0)    # where the rider's right hand holds the pack (x, y), in front of bay 1
RIDER_TURN = 160.0             # mannequin rotation about Z (180 faces the cabinet squarely)
RIDER_POSE = dict(shoulder_flex_r=30.0, elbow_flex_r=38.0)

# Colours (restrained product palette; kit accent)
C_BODY = "#E3E5E8"
C_BODY2 = "#CDD1D6"
C_DOOR = "#0F766E"
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_PLINTH = "#3A3F46"
C_METAL = "#B8BEC6"
C_ALU = "#A7AEB6"
C_LINER = "#9CA3AF"
C_PACK = "#3B4048"
C_WINDOW = "#DCEBF5"
C_CELLS = "#1B2536"
C_SCREEN = "#0E1216"
C_UI = "#5EEAD4"
C_UI_W = "#F1F5F9"
C_LED_G = "#22C55E"
C_LED_A = "#F59E0B"
C_LED_OFF = "#3F4650"
C_WHITE = "#F4F4F2"
C_WARN = "#EAB308"
C_RED = "#B91C1C"
C_PCB = "#166534"
C_PAVE = "#CEC9C1"
C_PAVE2 = "#BDB8AF"
C_CURB = "#A8A49D"
C_CLAY = "#9CA3AF"


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _bx(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _front(s):
    return s.faces().sort_by(Axis.Y)[0].edges()


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _par(s, axis):
    return s.edges().filter_by(axis)


def _comp(shapes):
    flat = []
    for s in shapes:
        if s is None:
            continue
        flat.extend(s.solids() if isinstance(s, Compound) else [s])
    shapes = flat
    return shapes[0] if len(shapes) == 1 else Compound(children=shapes)


def _text_front(s, x, y, z, size, depth=0.6, font="IBM Plex Sans", style=None):
    """Raised text on a face that looks toward -Y, centred at (x, z), front at y - depth."""
    pl = Plane(origin=(x, y, z), x_dir=(1, 0, 0), z_dir=(0, -1, 0))
    kw = {"font_size": size, "font": font}
    fp = Path(__file__).resolve().parents[2] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf"
    if fp.exists():
        kw = {"font_size": size, "font_path": str(fp)}
    return extrude(pl * Text(s, **kw), amount=depth)


def _door_rot(shape, hx, hy, deg):
    """Swing a door about the vertical hinge axis through (hx, hy)."""
    return Pos(hx, hy, 0) * Rot(0, 0, deg) * Pos(-hx, -hy, 0) * shape


def _pack_parts(xc, z0, P):
    """SwapCell v0.3 pack at bay centre xc, connector face at z0, lid face toward -Y (as model._pack)."""
    z1 = z0 + P["pack_l"]
    hw, hd = P["pack_w"] / 2, P["pack_d"] / 2
    body = B(xc - hw, xc + hw, -hd, hd, z0, z1)
    body = _fillet_try(body, _par(body, Axis.Z), [8.0, 6.0, 4.0])
    body = _fillet_try(body, _top(body), [3.0, 2.0])
    # parting line between the case and the lid face moulding
    body -= B(xc - hw - 1, xc + hw + 1, -hd + 11, -hd + 12, z0 + 2, z1 + 1) \
        - B(xc - hw + 0.8, xc + hw - 0.8, -hd + 10, -hd + 13, z0 - 1, z1 + 2)
    yc = P["plug_offset"]
    plug = B(xc - P["plug_w"] / 2, xc + P["plug_w"] / 2, yc - P["plug_d"] / 2, yc + P["plug_d"] / 2,
             z0 - P["plug_h"], z0 + 0.5)
    hh = P["handle_h"]
    handle = B(xc - P["handle_w"] / 2, xc + P["handle_w"] / 2, -P["handle_d"] / 2, P["handle_d"] / 2, z1 - 0.5, z1 + hh)
    handle = _fillet_try(handle, _top(handle), [6.0, 4.0, 2.0])
    handle -= B(xc - P["handle_w"] / 2 + 11, xc + P["handle_w"] / 2 - 11, -P["handle_d"], P["handle_d"], z1 - 1, z1 + 25)
    zl = z1 - P["latch_from_top"]
    pawl = B(xc - P["latch_w"] / 2, xc + P["latch_w"] / 2, hd - 0.5, hd + P["latch_proud"],
             zl - P["latch_h"] / 2, zl + P["latch_h"] / 2)
    pawl = _fillet_try(pawl, _par(pawl, Axis.X), [2.0, 1.0])
    fy = -hd
    stripe = B(xc - hw + 10, xc + hw - 10, fy - 0.4, fy + 0.1, z1 - 40, z1 - 30)
    label = B(xc - 30, xc + 30, fy - 0.4, fy + 0.1, z0 + 120, z0 + 200)
    wake = _ycyl(xc, fy - 1.2, z1 - 60, 7.0, 2.6)
    wake = _fillet_try(wake, _front(wake), [1.0, 0.5])
    soc = _comp([B(xc - 22 + 12 * k, xc - 14 + 12 * k, fy - 0.8, fy + 0.1, z1 - 82, z1 - 78) for k in range(4)])
    return [("body", body, C_PACK, "plastic"), ("handle", handle, C_BLACK, "rubber"),
            ("plug", plug, C_BLACK, "plastic"), ("latch pawl", pawl, C_METAL, "metal"),
            ("accent stripe", stripe, C_DOOR, "painted"), ("label", label, C_WHITE, "paper"),
            ("wake button", wake, C_DARK, "rubber"), ("charge gauge (lit)", soc, C_LED_G, "emissive")]


def product_parts(P=PARAMS):
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    W, D, t = P["W"], P["D"], P["sheet_t"]
    Z0, Z1 = P["plinth_h"], P["roof_z"]
    YF, YB = -D / 2, D / 2
    BZ0, BZ1 = P["bay_z0"], P["bay_z1"]
    HW = P["bay_open_w"] / 2
    xs = bay_x(P)
    LY1 = P["liner_y1"]
    pz0 = pack_z0(P)

    # ------------------------------------------------------------ 1 cabinet body
    EB = (0, 0, 0)
    outer = B(-W / 2, W / 2, YF, YB, Z0, Z1)
    outer = _fillet_try(outer, _par(outer, Axis.Z), [12.0, 8.0, 5.0])
    outer = _fillet_try(outer, _top(outer), [6.0, 4.0, 2.0])
    body = outer - B(-W / 2 + t, W / 2 - t, YF + t, YB - t, Z0 + t, Z1 - t)
    for xc in xs:
        body -= B(xc - HW, xc + HW, YF - 1, YF + t + 1, BZ0 + 5, BZ1 - 5)
    body -= B(-480, 480, YF - 1, YF + t + 1, 140, 660)                      # service opening
    body += B(-W / 2 + t, W / 2 - t, YF + t, LY1, BZ0 - t, BZ0)             # bay deck
    # fold seams on the sides at the deck and header lines
    for sx in (-1, 1):
        for zz in (BZ0 - 20, BZ1 + 20):
            body -= B(sx * W / 2 - 0.7, sx * W / 2 + 0.7, YF + 14, YB - 14, zz - 0.8, zz + 0.8)
        # filtered intake slots low on each side (BOM 10)
        for k in range(7):
            zz = 200 + 40 * k
            body -= B(sx * W / 2 - 3, sx * W / 2 + 3, -120, 120, zz, zz + 12)
    add("Cabinet body, powder-coated steel", body, C_BODY, "painted", 1, "shell", EB)

    fil = _comp([_bx(sx * (W / 2 - 4), 0, 341, 2, 252, 302) for sx in (-1, 1)])
    add("Intake filter pads", fil, C_DARK, "fabric", 10, "internal", (0, 0, 0))

    riv = []
    for sx in (-1, 1):
        for y in (YF + 22, YB - 22):
            for k in range(14):
                z = 160 + 95 * k
                riv.append(Pos(sx * W / 2, y, z) * Sphere(3.2) & _bx(sx * (W / 2 + 2), y, z, 4, 8, 8))
    add("Blind rivets", _comp(riv), C_METAL, "metal", 16, "shell", EB)

    # gasket outlines around the bay openings (parting lines round the doors)
    gk = []
    for xc in xs:
        g = B(xc - HW - 5, xc + HW + 5, YF - 2, YF, BZ0, BZ1) - B(xc - HW, xc + HW, YF - 3, YF + 1, BZ0 + 5, BZ1 - 5)
        gk.append(g)
    gk.append(B(-485, 485, YF - 2, YF, 135, 665) - B(-480, 480, YF - 3, YF + 1, 140, 660))
    add("Door gaskets (EPDM)", _comp(gk), C_BLACK, "rubber", 2, "shell", (0, 0, 0))

    # header sign above the bays
    hz0, hz1 = BZ1 + 45, Z1 - 45
    sign = B(-470, 470, YF - 3, YF, hz0, hz1)
    sign = _fillet_try(sign, _par(sign, Axis.Y), [8.0, 5.0])
    sign = _fillet_try(sign, _front(sign), [1.0, 0.5])
    add("Header sign panel", sign, C_DARK, "painted", 1, "shell", (0, -250, 0))
    zc = (hz0 + hz1) / 2
    word = _text_front("DockHub", -250, YF - 3, zc + 4, 80, 1.0)
    add("Header sign lettering", word, C_WHITE, "painted", 1, "shell", (0, -250, 0))
    sub = _text_front("SWAPCELL BATTERY SWAP", 250, YF - 3, zc + 22, 30, 0.8)
    add("Header sign subtitle", sub, C_UI, "painted", 1, "shell", (0, -250, 0))
    tap = _text_front("tap, return, take", 250, YF - 3, zc - 30, 30, 0.8)
    add("Header sign instructions", tap, C_WHITE, "painted", 1, "shell", (0, -250, 0))
    band = B(-470, 470, YF - 3.4, YF - 2.6, hz0, hz0 + 8)
    add("Header accent band", band, C_DOOR, "painted", 1, "shell", (0, -250, 0))

    # ------------------------------------------------------------ 2 bay doors
    hz0h, hz1h = P["door_handle_z"]
    for i, xc in enumerate(xs):
        hx, hy = xc - HW, YF - 2
        rot = DOOR_OPEN_DEG * -1 if i == OPEN_BAY else 0.0
        ED = (0, -1000, 0)
        door = B(xc - HW, xc + HW, YF - 6, YF - 2, BZ0 + 5, BZ1 - 5)
        door = _fillet_try(door, _par(door, Axis.Y), [4.0, 2.0])
        door = _fillet_try(door, _front(door), [1.2, 0.8])
        wx0, wx1, wz0, wz1 = xc - 72, xc + 30, BZ0 + 215, BZ1 - 55
        door -= B(wx0, wx1, YF - 8, YF, wz0, wz1)
        add(f"Bay {i + 1} door, steel", _door_rot(door, hx, hy, rot), C_DOOR, "painted", 2, "shell", ED)
        ring = B(wx0 - 4, wx1 + 4, YF - 7, YF - 5.6, wz0 - 4, wz1 + 4) - B(wx0, wx1, YF - 8, YF, wz0, wz1)
        add(f"Bay {i + 1} window gasket", _door_rot(ring, hx, hy, rot), C_BLACK, "rubber", 2, "shell", ED)
        pane = B(wx0 - 2, wx1 + 2, YF - 5, YF - 3, wz0 - 2, wz1 + 2)
        add(f"Bay {i + 1} window, polycarbonate", _door_rot(pane, hx, hy, rot), C_WINDOW, "clear", 2, "shell", ED)
        hdl = B(xc + 45, xc + 70, YF - 22, YF - 6, hz0h - 20, hz1h + 20)
        hdl -= B(xc + 44, xc + 71, YF - 16, YF - 5, hz0h - 6, hz1h + 6)
        hdl = _fillet_try(hdl, _par(hdl, Axis.X), [3.0, 2.0, 1.0])
        add(f"Bay {i + 1} pull handle", _door_rot(hdl, hx, hy, rot), C_METAL, "metal", 2, "shell", ED)
        lock = _ycyl(xc + 57.5, YF - 7, hz0h - 60, 7.0, 2.0)
        lock = _fillet_try(lock, _front(lock), [0.6, 0.3])
        hinges = _comp([_zcyl(hx - 3, YF - 6, z, 5.0, 60) for z in (BZ0 + 60, BZ1 - 60)])
        num = _text_front(str(i + 1), xc - 50, YF - 6, BZ1 - 30, 30, 0.8)
        add(f"Bay {i + 1} number", _door_rot(num, hx, hy, rot), C_WHITE, "painted", 2, "shell", ED)
        add(f"Bay {i + 1} lock indicator and hinges", _door_rot(_comp([lock, hinges]), hx, hy, rot),
            C_METAL, "metal", 2, "shell", ED)
        led = _ycyl(xc + 50, YF - 7, BZ1 - 30, 5.0, 2.0)
        led = _fillet_try(led, _front(led), [1.5, 1.0])
        st = BAY_LIGHTS[i]
        col, mat, lbl = {"green": (C_LED_G, "emissive", "green, lit"), "amber": (C_LED_A, "emissive", "amber, lit"),
                         "off": (C_LED_OFF, "plastic", "off")}[st]
        add(f"Bay {i + 1} status light ({lbl})", _door_rot(led, hx, hy, rot), col, mat, 2, "shell", ED)

    # ------------------------------------------------------------ 3 bay compartments (as model.py)
    hw, hd = P["pack_w"] / 2, P["pack_d"] / 2
    gc = P["guide_clear"]
    yc = P["plug_offset"]
    liners, cradles, recs, guides, catches = [], [], [], [], []
    for xc in xs:
        liners.append(B(xc - 90, xc + 90, YF + t, LY1, BZ0, BZ1 + 10)
                      - B(xc - 90 + t, xc + 90 - t, YF, LY1 - t, BZ0 + t, BZ1 + 10 - t)
                      - B(xc - 30, xc + 30, LY1 - t - 1, LY1 + 1, BZ1 - 80, BZ1 - 20))
        cr = B(xc - 75, xc + 75, -75, 75, BZ0 + t, pz0)
        cr = _fillet_try(cr, _par(cr, Axis.Z), [6.0, 4.0])
        cr = _fillet_try(cr, _top(cr), [2.0, 1.0])
        cr -= B(xc - P["plug_w"] / 2 - 1, xc + P["plug_w"] / 2 + 1, yc - P["plug_d"] / 2 - 1,
                yc + P["plug_d"] / 2 + 1, pz0 - P["plug_h"] - 1, pz0 + 1)
        cradles.append(cr)
        rc = B(xc - P["plug_w"] / 2 - 8, xc + P["plug_w"] / 2 + 8, yc - P["plug_d"] / 2 - 8,
               yc + P["plug_d"] / 2 + 8, BZ0 + t, pz0 - P["plug_h"] - 1)
        for k in range(5):
            rc += B(xc - 20 + 10 * k - 2, xc - 20 + 10 * k + 2, yc - 6, yc + 6, pz0 - P["plug_h"] - 1, pz0 - P["plug_h"] + 3)
        recs.append(rc)
        for s in (-1, 1):
            g = B(xc + s * (hw + gc) + (0 if s > 0 else -5), xc + s * (hw + gc) + (5 if s > 0 else 0), -45, 45,
                  pz0, pz0 + P["guide_h"])
            guides.append(_fillet_try(g, _top(g), [2.0, 1.0]))
        zl = pz0 + P["pack_l"] - P["latch_from_top"]
        yb = hd + P["latch_proud"] + 1
        catches.append(B(xc - 30, xc + 30, yb + 8, yb + 14, pz0, zl + 30)
                       + B(xc - 25, xc + 25, yb, yb + 8, zl + P["latch_h"] / 2 + 1, zl + P["latch_h"] / 2 + 9))
    EBay = (0, -450, 0)
    add("Bay liners, galvanized steel", _comp(liners), C_LINER, "metal", 3, "internal", EBay)
    add("Bay cradles with guide faces", _comp(cradles), C_DARK, "plastic", 3, "internal", EBay)
    add("Blind-mate receptacles", _comp(recs), C_BLACK, "plastic", 3, "internal", EBay)
    add("Pack side guides", _comp(guides), C_DARK, "plastic", 3, "internal", EBay)
    add("Class D latch catches", _comp(catches), C_METAL, "metal", 3, "internal", EBay)

    # ------------------------------------------------------------ 4 packs in bays 2 to 4
    groups = {}
    for i, xc in enumerate(xs):
        if i == OPEN_BAY:
            continue
        for nm, s, col, mat in _pack_parts(xc, pz0, P):
            groups.setdefault(nm, (col, mat, []))[2].append(s)
    for nm, (col, mat, ss) in groups.items():
        add(f"SwapCell packs, {nm}", _comp(ss), col, mat, 4, "internal", (0, -250, 1050))

    # ------------------------------------------------------------ 5 chargers on their rack
    EC = (0, -520, -60)
    rack = B(-470, 470, -60, 230, 380, 390)
    rack += _comp([B(x - 10, x + 10, -60, -40, 150, 380) for x in (-460, 460)])
    add("Charger rack", rack, C_PLINTH, "painted", 16, "internal", EC)
    chg, fins, clab = [], [], []
    for x in (-345.0, -115.0, 115.0, 345.0):
        c = B(x - 80, x + 80, -20, 180, 390, 452)
        c = _fillet_try(c, _par(c, Axis.Y), [4.0, 2.0])
        chg.append(c)
        for k in range(9):
            fins.append(B(x - 72 + 18 * k - 1.5, x - 72 + 18 * k + 1.5, -18, 178, 452, 460))
        clab.append(B(x - 40, x + 40, -20.4, -19.9, 405, 437))
    add("Chargers, 54.6 V 5 A", _comp(chg), C_DARK, "metal", 5, "internal", EC)
    add("Charger heat sink fins", _comp(fins), C_ALU, "metal", 5, "internal", EC)
    add("Charger rating labels", _comp(clab), C_WHITE, "paper", 5, "internal", EC)

    # ------------------------------------------------------------ 6 controller, 8 grid unit, 13 MPPT
    ctl = B(-450, -230, 140, 240, 150, 340)
    ctl = _fillet_try(ctl, _par(ctl, Axis.Y), [6.0, 4.0])
    add("Dock controller enclosure (ESP32, CAN, LTE-M)", ctl, C_BODY2, "plastic", 6, "internal", (-800, 300, 750))
    cled = _comp([_ycyl(-420 + 14 * k, 139.2, 320, 2.5, 1.6) for k in range(4)])
    add("Dock controller status lights (lit)", cled, C_LED_G, "emissive", 6, "internal", (-800, 300, 750))
    ant = _zcyl(-250, 190, 360, 6, 40)
    ant = _fillet_try(ant, _top(ant), [5.0, 3.0])
    add("LTE-M antenna", ant, C_BLACK, "rubber", 6, "internal", (-800, 300, 750))

    grid = B(230, 450, 150, 242, 150, 360)
    grid = _fillet_try(grid, _par(grid, Axis.Y), [6.0, 4.0])
    grid -= B(250, 430, 149, 156, 230, 320)
    add("Grid input enclosure", grid, C_BODY2, "plastic", 8, "internal", (900, 0, -40))
    brk = _comp([B(258 + 18 * k, 274 + 18 * k, 156, 176, 240, 310) for k in range(9)])
    add("RCBO, breakers and surge protector", brk, C_WHITE, "plastic", 8, "internal", (900, 0, -40))
    tog = _comp([B(263 + 18 * k, 269 + 18 * k, 151, 158, 272, 284) for k in range(9)])
    add("Breaker toggles", tog, C_BLACK, "plastic", 8, "internal", (900, 0, -40))
    iso = _ycyl(340, 149, 190, 18, 4) + B(330, 350, 141, 147, 176, 204)
    add("Lockable isolator", iso, C_RED, "plastic", 8, "internal", (900, 0, -40))

    mppt = B(-190, -40, 170, 240, 150, 330)
    mppt = _fillet_try(mppt, _par(mppt, Axis.Y), [4.0, 2.0])
    add("MPPT solar charge controller", mppt, C_DARK, "metal", 13, "internal", (1500, -450, -350))
    mf = _comp([B(-186 + 12 * k, -180 + 12 * k, 240, 246, 160, 320) for k in range(12)])
    add("MPPT heat sink fins", mf, C_ALU, "metal", 13, "internal", (1500, -450, -350))
    mscr = B(-160, -70, 169.4, 170, 280, 315)
    add("MPPT display", mscr, C_SCREEN, "screen", 13, "internal", (1500, -450, -350))

    # ------------------------------------------------------------ 9 fire detection and suppression
    EF = (0, 500, 350)
    aer = Pos(-60, 200, 1420) * Rot(0, 90, 0) * Cylinder(38, 420)
    aer = _fillet_try(aer, aer.edges(), [6.0, 4.0, 2.0])
    add("Aerosol suppression unit", aer, C_RED, "painted", 9, "internal", EF)
    bands = _comp([_xcyl(x, 200, 1420, 39.5, 12) for x in (-220, 100)])
    add("Aerosol unit straps", bands, C_METAL, "metal", 9, "internal", EF)
    det = Pos(250, 200, 1465) * Cylinder(45, 25)
    det = _fillet_try(det, _bottom_edges(det), [8.0, 5.0])
    add("Heat and smoke detector", det, C_WHITE, "plastic", 9, "internal", EF)

    # ------------------------------------------------------------ 10 plenum, fans, roof louver
    EP = (0, 900, 250)
    plen = B(-W / 2 + t, W / 2 - t, LY1, LY1 + P["plenum_t"], BZ0, Z1 - t)
    for xc in xs:
        plen -= B(xc - 30, xc + 30, LY1 - 1, LY1 + P["plenum_t"] + 1, BZ1 - 80, BZ1 - 20)
    add("Vent plenum wall", plen, C_LINER, "metal", 10, "internal", EP)
    fans, grills = [], []
    for x in (-380, 380):
        f = Pos(x, 185, Z1 - t - 13) * Cylinder(60, 25) - Pos(x, 185, Z1 - t - 27) * Cylinder(56, 20)
        fans.append(f + Pos(x, 185, Z1 - t - 15) * Cylinder(18, 22))
        for r in (22, 36, 50):
            grills.append(Pos(x, 185, Z1 - t - 26) * (Cylinder(r + 1.5, 2) - Cylinder(r - 1.5, 3)))
    add("Plenum fans, 120 mm", _comp(fans), C_BLACK, "plastic", 10, "internal", EP)
    add("Fan guards", _comp(grills), C_METAL, "metal", 10, "internal", EP)

    lv = B(-420, 420, 160, 240, Z1, Z1 + 70)
    for i in range(9):
        x = -380 + i * 90
        lv -= B(x, x + 50, 150, 250, Z1 + 20, Z1 + 55)
    add("Roof louver", lv, C_BODY2, "painted", 10, "shell", (0, 900, 250))
    hood = B(-435, 435, 145, 255, Z1 + 70, Z1 + 76)
    hood = _fillet_try(hood, _par(hood, Axis.Z), [8.0, 5.0])
    hood = _fillet_try(hood, _top(hood), [2.0, 1.0])
    add("Louver rain hood", hood, C_BODY2, "painted", 10, "shell", (0, 900, 330))
    mesh = B(-418, 418, 162, 238, Z1 + 1, Z1 + 3)
    add("Louver insect mesh", mesh, C_DARK, "fabric", 10, "shell", (0, 900, 250))

    # ------------------------------------------------------------ 7 access panel
    EA = (700, -300, 0)
    ax0, ax1 = P["access_x"]
    az0, az1 = P["access_z"]
    col = B(ax0, ax1, YF - 4, YF, az0, az1)
    col = _fillet_try(col, _par(col, Axis.Y), [10.0, 6.0])
    col = _fillet_try(col, _front(col), [1.5, 1.0])
    add("Access panel bezel, steel", col, C_DARK, "painted", 7, "shell", EA)
    dz0, dz1 = P["display_z"]
    disp = B(ax0 + 20, ax1 - 20, YF - 8, YF - 4, dz0, dz1)
    disp = _fillet_try(disp, _par(disp, Axis.Y), [4.0, 2.0])
    add("Display bezel", disp, C_BLACK, "plastic", 7, "shell", EA)
    glass = B(ax0 + 26, ax1 - 26, YF - 8.6, YF - 7.9, dz0 + 6, dz1 - 6)
    add("Display glass", glass, C_SCREEN, "screen", 7, "shell", EA)
    ym = YF - 8.9
    ui = [B(ax0 + 30, ax1 - 30, ym, YF - 8.5, dz1 - 22, dz1 - 12)]                        # title bar
    ui_w = [_text_front("Tap to swap", (ax0 + ax1) / 2, YF - 8.6, dz1 - 44, 15, 0.3)]
    tiles_g, tiles_a = [], []
    for k in range(4):
        x0 = ax0 + 32 + 30 * k
        tl = B(x0, x0 + 24, ym, YF - 8.5, dz0 + 14, dz0 + 52)
        (tiles_a if BAY_LIGHTS[k] == "amber" else tiles_g if BAY_LIGHTS[k] == "green" else ui_w).append(tl)
    add("Display screen content, teal (lit)", _comp(ui), C_UI, "emissive", 7, "shell", EA)
    add("Display screen content, white (lit)", _comp(ui_w), C_UI_W, "emissive", 7, "shell", EA)
    add("Display bay tiles, green (lit)", _comp(tiles_g), C_LED_G, "emissive", 7, "shell", EA)
    add("Display bay tile, amber (lit)", _comp(tiles_a), C_LED_A, "emissive", 7, "shell", EA)
    rz0, rz1 = P["reader_z"]
    rd = B(ax0 + 45, ax1 - 45, YF - 8, YF - 4, rz0, rz1)
    rd = _fillet_try(rd, _par(rd, Axis.Y), [8.0, 5.0])
    rd = _fillet_try(rd, _front(rd), [1.5, 1.0])
    add("NFC reader", rd, C_BODY2, "plastic", 7, "shell", EA)
    rx, rzc = (ax0 + ax1) / 2, (rz0 + rz1) / 2
    ring = _ycyl(rx, YF - 8.3, rzc, 26, 0.8) - _ycyl(rx, YF - 8.3, rzc, 22, 2)
    add("NFC reader ring (lit)", ring, C_UI, "emissive", 7, "shell", EA)
    arcs = []
    for r in (8, 13, 18):
        a = _ycyl(rx - 6, YF - 8.3, rzc, r + 1.3, 0.6) - _ycyl(rx - 6, YF - 8.3, rzc, r - 1.3, 2)
        arcs.append(a & B(rx - 6, rx + 30, YF - 10, YF - 6, rzc - 12, rzc + 12))
    add("Contactless symbol", _comp(arcs), C_DARK, "painted", 7, "shell", EA)
    sl = []
    for k in range(4):
        x = ax0 + 45 + 30 * k
        d = _ycyl(x, YF - 5.5, 1025, 4.0, 3.0)
        d = _fillet_try(d, _front(d), [1.5, 1.0])
        sl.append((k, d))
    for k, d in sl:
        st = BAY_LIGHTS[k]
        col_, mat_ = {"green": (C_LED_G, "emissive"), "amber": (C_LED_A, "emissive"), "off": (C_LED_OFF, "plastic")}[st]
        add(f"Access panel bay {k + 1} light", d, col_, mat_, 7, "shell", EA)
    buz = _comp([_ycyl(rx - 15 + 10 * i, YF - 4.2, az0 + 22, 2.0, 0.6) for i in range(4)])
    add("Buzzer grille", buz, C_BLACK, "plastic", 7, "shell", EA)
    scr = _comp([_ycyl(x, YF - 4.6, z, 3.0, 1.2) for x in (ax0 + 10, ax1 - 10) for z in (az0 + 10, az1 - 10)])
    add("Bezel security screws", scr, C_METAL, "metal", 16, "shell", EA)

    # ------------------------------------------------------------ 15 service door
    ES = (0, -1100, -150)
    sd = B(-480, 480, YF - 6, YF - 2, 140, 660)
    sd = _fillet_try(sd, _par(sd, Axis.Y), [5.0, 3.0])
    sd = _fillet_try(sd, _front(sd), [1.2, 0.8])
    for k in range(6):
        z = 175 + 22 * k
        sd -= B(-420, -120, YF - 7, YF - 1, z, z + 8)
    for k in range(6):
        z = 175 + 22 * k
        sd -= B(120, 320, YF - 7, YF - 1, z, z + 8)
    add("Service door, steel", sd, C_BODY, "painted", 15, "shell", ES)
    sflt = B(-422, 322, YF - 1.5, YF - 0.5, 170, 300)
    add("Service door intake filter", sflt, C_DARK, "fabric", 10, "shell", ES)
    cam = _ycyl(400, YF - 9, 400, 16, 6)
    cam = _fillet_try(cam, _front(cam), [2.0, 1.0])
    cam -= B(398, 402, YF - 13, YF - 10, 390, 410)
    add("Service door cam lock", cam, C_METAL, "metal", 15, "shell", ES)
    shng = _comp([_zcyl(-483, YF - 6, z, 5.0, 70) for z in (220, 580)])
    add("Service door hinges", shng, C_METAL, "metal", 15, "shell", ES)
    warn = B(-440, -320, YF - 6.4, YF - 5.9, 470, 620)
    add("Lithium battery warning label", warn, C_WARN, "paper", 16, "shell", ES)
    wtri = _text_front("!", -380, YF - 6.4, 560, 70, 0.3)
    wbar = _comp([B(-430, -330, YF - 6.7, YF - 6.3, 480 + 12 * k, 486 + 12 * k) for k in range(3)])
    add("Warning label print", _comp([wtri, wbar]), C_BLACK, "paper", 16, "shell", ES)
    info = B(-280, 20, YF - 6.4, YF - 5.9, 540, 620)
    add("Operator information plate", info, C_WHITE, "paper", 16, "shell", ES)
    ink = _comp([B(-270, -40, YF - 6.7, YF - 6.3, 596, 608)]
                + [B(-270, 10 - 40 * (k % 2), YF - 6.7, YF - 6.3, 552 + 12 * k, 557 + 12 * k) for k in range(3)])
    add("Operator plate print", ink, C_DARK, "paper", 16, "shell", ES)

    # ------------------------------------------------------------ 14 plinth
    ai = P["anchor_inset"]
    pl = B(-W / 2, W / 2, YF, YB, 0, Z0)
    pl = _fillet_try(pl, _par(pl, Axis.Z), [12.0, 8.0, 5.0])
    pl -= B(-W / 2 + 60, W / 2 - 60, YF + 60, YB - 60, -1, Z0 + 1)
    for x in (-W / 2 + ai, W / 2 - ai):
        for y in (YF + ai / 2, YB - ai / 2):
            pl -= Pos(x, y, Z0 / 2) * Cylinder(7, Z0 + 2)
    pl -= B(-W / 2 - 1, W / 2 + 1, YF - 1, YF + 1, Z0 - 12, Z0 - 10)       # shadow line under the body
    add("Plinth and anchor frame", pl, C_PLINTH, "painted", 14, "shell", (0, 0, -350))

    # ------------------------------------------------------------ 11, 12 canopy (group accessory)
    pw, pd, pt = P["panel"]
    a = P["tilt_deg"]
    PY, PZ = P["panel_y"], P["panel_z"]
    tanA = math.tan(math.radians(a))
    place = Pos(0, PY, PZ) * Rot(-a, 0, 0)

    def under(y):
        return PZ - pt / 2 / math.cos(math.radians(a)) - (y - PY) * tanA

    fr = B(-pw / 2, pw / 2, -pd / 2, pd / 2, -pt / 2, pt / 2)
    fr = _fillet_try(fr, _par(fr, Axis.Z), [6.0, 4.0])
    fr -= B(-pw / 2 + 22, pw / 2 - 22, -pd / 2 + 22, pd / 2 - 22, -pt / 2 + 4, pt / 2 + 1)
    add("Solar panel frame, aluminium", place * fr, C_ALU, "metal", 11, "accessory", (0, 0, 1900))
    cells = B(-pw / 2 + 22, pw / 2 - 22, -pd / 2 + 22, pd / 2 - 22, pt / 2 - 6, pt / 2 - 3)
    add("Solar panel cells and glass", place * cells, C_CELLS, "screen", 11, "accessory", (0, 0, 1900))
    lines = []
    nx, ny = 12, 6
    cw_, ch_ = (pw - 44) / nx, (pd - 44) / ny
    for i in range(1, nx):
        x = -pw / 2 + 22 + i * cw_
        lines.append(B(x - 1.5, x + 1.5, -pd / 2 + 22, pd / 2 - 22, pt / 2 - 3, pt / 2 - 2.6))
    for j in range(1, ny):
        y = -pd / 2 + 22 + j * ch_
        lines.append(B(-pw / 2 + 22, pw / 2 - 22, y - 1.5, y + 1.5, pt / 2 - 3, pt / 2 - 2.6))
    add("Solar cell gaps", place * _comp(lines), "#C9CED6", "metal", 11, "accessory", (0, 0, 1900))
    jb = B(-60, 60, -40, 40, -pt / 2 - 18, -pt / 2)
    add("Solar junction box", place * jb, C_BLACK, "plastic", 11, "accessory", (0, 0, 1900))

    rh = P["rail_h"]
    rails = _comp([Pos(x, PY, PZ - pt / 2 - rh / 2 - 2) * Rot(-a, 0, 0) * B(-25, 25, -(pd - 80) / 2, (pd - 80) / 2, -rh / 2, rh / 2)
                   for x in (-P["post_x"], P["post_x"])])
    s = P["post"] / 2
    posts, plates, bolts = [], [], []
    for x in (-P["post_x"], P["post_x"]):
        for y in (-P["post_y"], P["post_y"]):
            ps = B(x - s, x + s, y - s, y + s, Z1, under(y) - rh - 5)
            posts.append(_fillet_try(ps, _par(ps, Axis.Z), [4.0, 3.0]))
            bp = B(x - 55, x + 55, y - 55, y + 55, Z1, Z1 + 8)
            plates.append(_fillet_try(bp, _par(bp, Axis.Z), [8.0, 5.0]))
            for dx in (-38, 38):
                for dy in (-38, 38):
                    bolts.append(Pos(x + dx, y + dy, Z1 + 11) * Cylinder(8, 6))
    add("Canopy rails", rails, C_PLINTH, "painted", 12, "accessory", (0, 0, 1500))
    add("Canopy posts, 50 x 50 steel", _comp(posts), C_PLINTH, "painted", 12, "accessory", (0, 0, 1500))
    add("Canopy post base plates", _comp(plates), C_PLINTH, "painted", 12, "accessory", (0, 0, 1200))
    add("Canopy base bolts", _comp(bolts), C_METAL, "metal", 12, "accessory", (0, 0, 1200))

    # ------------------------------------------------------------ context: sidewalk, rider, pack in hand
    tiles = []
    step = 600.0
    x0, x1, y0, y1 = -1200.0, 1050.0, -1200.0, 700.0
    yy = y0
    while yy < y1 - 1:
        xx = x0
        while xx < x1 - 1:
            tiles.append(B(xx + 3, min(xx + step, x1) - 3, yy + 3, min(yy + step, y1) - 3, -20, 0))
            xx += step
        yy += step
    add("Sidewalk paving slabs", _comp(tiles), C_PAVE, "paper", None, "context", (0, 0, 0))
    base = B(x0, x1, y0, y1, -150, -20)
    add("Sidewalk bedding", base, C_PAVE2, "paper", None, "context", (0, 0, 0))
    curb = B(x0, x1, y0 - 160, y0, -150, 0)
    curb = _fillet_try(curb, _front(curb), [20.0, 10.0])
    add("Granite curb", curb, C_CURB, "paper", None, "context", (0, 0, 0))

    from context_parts import mannequin, mannequin_landmarks
    lm = mannequin_landmarks(1750, "stand", **RIDER_POSE)
    hx_, hy_, hz_ = lm["hands"][1]                    # right hand, figure frame
    th = math.radians(RIDER_TURN)
    rx_, ry_ = hx_ * math.cos(th) - hy_ * math.sin(th), hx_ * math.sin(th) + hy_ * math.cos(th)
    px, py = RIDER_AT[0] - rx_, RIDER_AT[1] - ry_
    person = Pos(px, py, 0) * Rot(0, 0, RIDER_TURN) * mannequin(1750, "stand", **RIDER_POSE)
    add("Rider, 1.75 m (clay mannequin)", person, C_CLAY, "clay", None, "context", (0, 0, 0))
    # the charged pack from bay 1, hanging from the right hand by its handle bar
    z1 = hz_ - (P["handle_h"] - 5)
    zp0 = z1 - P["pack_l"]
    move = Pos(RIDER_AT[0], RIDER_AT[1], 0)
    for nm, s, col_, mat_ in _pack_parts(0.0, zp0, P):
        add(f"Pack in hand, {nm}", move * s, col_, mat_, 4, "context", (0, 0, 0))
    return out


def _bottom_edges(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:50s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
