"""DockHub product appearance model (build123d), TRL 3, constructable design (DKH-DDR-003).

Finished-product look for photoreal renders of the four-bay fit, matching the constructable
design accepted on 2026-10-02: riveted 1.5 mm steel panels with folded corners on a welded
channel plinth; four teal 2 mm bay doors on stainless piano hinges over 150 mm openings, each with
a pull handle, a bay number and a status light (bays 2 and 3 green, charged; bay 4 amber,
charging); the access column with a lit display, an NFC reader with a lit ring and four bay status
lights; the service door on a piano hinge with its filtered intake slot, cam lock and warning
labels; a vent hood with rear slots and a rain lip over two square roof fans; the roof beams under
the canopy posts; and the technical compartment (chargers on the folded shelf, controller, grid
unit, MPPT controller), solenoid locks, fire unit, detector and plenum wall for the exploded view.
The 400 W canopy (posts on base and cap plates, rails, end clamps, panel) is in group "accessory"
so the detail view can frame the cabinet without it. Context is a compact paved patch with a curb
and the shared clay mannequin, standing at bay 1 with a charged pack just lifted out by its handle;
bay 1's door is open and its cradle is empty.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension comes from PARAMS and the helpers in model.py; the roof beams, vent hood,
fans, plenum wall, charger shelf, liners, catch brackets, locks, fire unit, detector, canopy posts,
post bolts, rails and end clamps are taken directly from model.build_components(). Render-only
choices, accepted by Amish on 2026-10-02 (DKH-DEC-001): the clear windows in the bay doors (the
built doors are solid steel), the scene state (packs in bays 2 to 4, bay 1 open), the header sign
and markings, and the four-bay fit, captioned "four-bay fit shown".

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))

from build123d import (Axis, Box, Compound, Cylinder, Plane, Pos, Rot, Sphere, Text, extrude, fillet)
from model import PARAMS, bay_x, build_components, derived, pack_z0, panel_frame, _box as B

TITLE = "DockHub: street-side battery swap and charging station"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 22, "az": -38,
     "note": "Four-bay fit shown. Product render from the front right and above (about 22 deg elevation); rider at "
             "left lifting a charged pack from the open bay 1, doors on piano hinges, access panel with its lit "
             "display at right, vent hood and solar canopy overhead. Door windows are shown in renders only; "
             "the built doors are solid steel"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Four-bay fit shown. Exploded view from the front right and above (about 28 deg elevation): canopy "
             "and solar panel on posts and roof beams, vent hood and fans, cabinet, bay doors and hinges, bay "
             "compartments and packs, access panel, chargers on their shelf, controller, grid unit, MPPT "
             "controller, fire unit, plenum, service door, plinth"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 12, "az": -30,
     "note": "Four-bay fit shown. Detail from the front right, slightly above (about 12 deg elevation): the cabinet "
             "without canopy or street; bay 1 open on its piano hinge with an empty cradle, packs in bays 2 to 4 "
             "and the access panel. Door windows are shown in renders only; the built doors are solid steel"},
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

    M = build_components(P, fitted=P["n_bays"])          # the constructable model, all four bays fitted
    dv = derived(P)
    W, D, t = P["W"], P["D"], P["sheet_t"]
    Z0, Z1 = P["plinth_h"], P["roof_z"]
    YF, YB = -D / 2, D / 2
    o0, o1 = P["open_z"]
    HW = P["bay_open_w"] / 2
    xs = bay_x(P)
    LY1 = P["liner_y1"]
    pz0 = pack_z0(P)
    dw, dh, dt = P["door"]
    gw, gt = P["gasket"]
    ydb = YF - gt                                   # door back face
    DF = ydb - dt                                   # door front face
    dz0 = (o0 + o1) / 2 - dh / 2
    so_w, so_0, so_1 = P["service_open"]

    # ------------------------------------------------------------ 1 cabinet body (riveted panels, folded corners)
    EB = (0, 0, 0)
    outer = B(-W / 2, W / 2, YF, YB, Z0, Z1)
    outer = _fillet_try(outer, _par(outer, Axis.Z), [3.0, 2.0])
    outer = _fillet_try(outer, _top(outer), [3.0, 2.0])
    body = outer - B(-W / 2 + t, W / 2 - t, YF + t, YB - t, Z0 + t, Z1 - t)
    for xc in xs:
        body -= B(xc - HW, xc + HW, YF - 1, YF + t + 1, o0, o1)
    body -= B(-so_w, so_w, YF - 1, YF + t + 1, so_0, so_1)                  # service opening
    for sx in (-1, 1):                                                        # fan holes under the hood
        body -= _zcyl(sx * P["fan_x"], P["fan_y"], Z1 - t / 2, P["fan_hole_r"], t + 2)
    add("Cabinet body, powder-coated steel panels", body, C_BODY, "painted", 1, "shell", EB)
    add("Bay deck", M["deck"].shape, C_LINER, "metal", 1, "internal", (0, -450, -40))
    add("Charger shelf", M["shelf"].shape, C_PLINTH, "painted", 1, "internal", (0, -520, -90))
    add("Roof beams and cleats, 40 x 40 angle", M["beams"].shape, C_PLINTH, "painted", 1, "internal", (0, 0, 650))

    riv = []
    for sx in (-1, 1):
        for y in (YF + 12, YB - 12):
            for k in range(14):
                z = 160 + 95 * k
                riv.append(Pos(sx * W / 2, y, z) * Sphere(3.2) & _bx(sx * (W / 2 + 2), y, z, 4, 8, 8))
    for x in [-W / 2 + 60 + 110 * k for k in range(9)]:
        riv.append(Pos(x, YF, Z1 - 20) * Sphere(3.2) & _bx(x, YF - 2, Z1 - 20, 8, 4, 8))
    add("Blind rivets", _comp(riv), C_METAL, "metal", 16, "shell", EB)

    # EPDM gaskets round the bay and service openings, between the doors and the front panel
    add("Door gaskets (EPDM)", _comp([M["gaskets"].shape, M["service_gasket"].shape]), C_BLACK, "rubber", 2, "shell", EB)

    # header sign above the bays
    hz0, hz1 = P["bay_z1"] + 45, Z1 - 45
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

    # ------------------------------------------------------------ 2 bay doors on piano hinges
    hz0h, hz1h = P["door_handle_z"]
    hinge_static = []
    for i, xc in enumerate(xs):
        hx, hy = xc - dw / 2 - 3.5, YF - 3.5                         # piano hinge pin axis (model.py)
        rot = -DOOR_OPEN_DEG if i == OPEN_BAY else 0.0
        ED = (0, -1000, 0)
        door = B(xc - dw / 2, xc + dw / 2, DF, ydb, dz0, dz0 + dh)
        door = _fillet_try(door, _par(door, Axis.Y), [3.0, 2.0])
        door = _fillet_try(door, _front(door), [0.8, 0.5])
        wx0, wx1, wz0, wz1 = xc - 70, xc + 30, o0 + 210, o1 - 50       # render-only window (decided 2026-10-02)
        door -= B(wx0, wx1, DF - 2, ydb + 2, wz0, wz1)
        add(f"Bay {i + 1} door, steel", _door_rot(door, hx, hy, rot), C_DOOR, "painted", 2, "shell", ED)
        ring = B(wx0 - 4, wx1 + 4, DF - 1.2, DF, wz0 - 4, wz1 + 4) - B(wx0, wx1, DF - 2, DF + 1, wz0, wz1)
        add(f"Bay {i + 1} window gasket", _door_rot(ring, hx, hy, rot), C_BLACK, "rubber", 2, "shell", ED)
        pane = B(wx0 - 2, wx1 + 2, DF + 0.2, ydb - 0.2, wz0 - 2, wz1 + 2)
        add(f"Bay {i + 1} window, polycarbonate (render only)", _door_rot(pane, hx, hy, rot), C_WINDOW, "clear", 2, "shell", ED)
        hdl = B(xc + 45, xc + 70, DF - 16, DF, hz0h - 20, hz1h + 20)
        hdl -= B(xc + 44, xc + 71, DF - 10, DF + 1, hz0h - 6, hz1h + 6)
        hdl = _fillet_try(hdl, _par(hdl, Axis.X), [3.0, 2.0, 1.0])
        add(f"Bay {i + 1} pull handle", _door_rot(hdl, hx, hy, rot), C_METAL, "metal", 2, "shell", ED)
        tongue = B(xc + 50, xc + 54, ydb, YF + t + 16.5, 950, 970)
        add(f"Bay {i + 1} lock tongue", _door_rot(tongue, hx, hy, rot), C_METAL, "metal", 2, "internal", ED)
        lock = _ycyl(xc + 57.5, DF - 1, hz0h - 60, 7.0, 2.0)
        lock = _fillet_try(lock, _front(lock), [0.6, 0.3])
        leaf = B(xc - dw / 2, xc - dw / 2 + 16, DF - t, DF, o0 + 15, o1 - 15)
        num = _text_front(str(i + 1), xc - 50, DF, o1 - 25, 30, 0.8)
        add(f"Bay {i + 1} number", _door_rot(num, hx, hy, rot), C_WHITE, "painted", 2, "shell", ED)
        add(f"Bay {i + 1} lock indicator and hinge leaf", _door_rot(_comp([lock, leaf]), hx, hy, rot),
            C_METAL, "metal", 2, "shell", ED)
        hinge_static += [B(xc - dw / 2 - 18, xc - dw / 2 - 7, YF - t, YF, o0 + 15, o1 - 15),
                         _zcyl(hx, hy, (o0 + o1) / 2, 3.5, o1 - o0 - 30)]
        led = _ycyl(xc + 50, DF - 1, o1 - 25, 5.0, 2.0)
        led = _fillet_try(led, _front(led), [1.5, 1.0])
        st = BAY_LIGHTS[i]
        col, mat, lbl = {"green": (C_LED_G, "emissive", "green, lit"), "amber": (C_LED_A, "emissive", "amber, lit"),
                         "off": (C_LED_OFF, "plastic", "off")}[st]
        add(f"Bay {i + 1} status light ({lbl})", _door_rot(led, hx, hy, rot), col, mat, 2, "shell", ED)
    add("Bay door piano hinges, stainless", _comp(hinge_static), C_METAL, "metal", 2, "shell", (0, -1000, 0))
    add("Solenoid locks", M["locks"].shape, C_DARK, "metal", 2, "internal", (0, -700, 0))

    # ------------------------------------------------------------ 3 bay compartments (model.py)
    hw, hd = P["pack_w"] / 2, P["pack_d"] / 2
    yc = P["plug_offset"]
    EBay = (0, -450, 0)
    add("Bay liners, galvanized steel", M["liners"].shape, C_LINER, "metal", 3, "internal", EBay)
    cradles, recs = [], []
    for xc in xs:
        cr = M["cradles"].shape & B(xc - 100, xc + 100, -200, 200, 0, 2000)
        cradles.append(cr)
        rc = B(xc - P["plug_w"] / 2 - 8, xc + P["plug_w"] / 2 + 8, yc - P["plug_d"] / 2 - 8,
               yc + P["plug_d"] / 2 + 8, P["bay_z0"] + t, pz0 - P["plug_h"] - 1.5)
        for k in range(5):
            rc += B(xc - 20 + 10 * k - 2, xc - 20 + 10 * k + 2, yc - 6, yc + 6, pz0 - P["plug_h"] - 1.5, pz0 - P["plug_h"] + 3)
        recs.append(rc)
    add("Bay cradles with guide faces (printed)", _comp(cradles), C_DARK, "plastic", 3, "internal", EBay)
    add("Blind-mate receptacles", _comp(recs), C_BLACK, "plastic", 3, "internal", EBay)
    add("Class D catch brackets", M["catches"].shape, C_METAL, "metal", 3, "internal", EBay)

    # ------------------------------------------------------------ 4 packs in bays 2 to 4
    groups = {}
    for i, xc in enumerate(xs):
        if i == OPEN_BAY:
            continue
        for nm, s, col, mat in _pack_parts(xc, pz0, P):
            groups.setdefault(nm, (col, mat, []))[2].append(s)
    for nm, (col, mat, ss) in groups.items():
        add(f"SwapCell packs, {nm}", _comp(ss), col, mat, 4, "internal", (0, -250, 1050))

    # ------------------------------------------------------------ 5 chargers on the shelf
    EC = (0, -520, -60)
    sz = dv["shelf_z"]
    chg, fins, clab = [], [], []
    for x in dv["charger_x"]:
        c = B(x - 80, x + 80, -20, 180, sz, sz + 62)
        c = _fillet_try(c, _par(c, Axis.Y), [4.0, 2.0])
        chg.append(c)
        for k in range(9):
            fins.append(B(x - 72 + 18 * k - 1.5, x - 72 + 18 * k + 1.5, -18, 178, sz + 62, sz + 70))
        clab.append(B(x - 40, x + 40, -20.4, -19.9, sz + 12, sz + 44))
    add("Chargers, 54.6 V 5 A", _comp(chg), C_DARK, "metal", 5, "internal", EC)
    add("Charger heat sink fins", _comp(fins), C_ALU, "metal", 5, "internal", EC)
    add("Charger rating labels", _comp(clab), C_WHITE, "paper", 5, "internal", EC)

    # ------------------------------------------------------------ 6 controller, 8 grid unit, 13 MPPT (on the back panel)
    ybi = YB - t
    ctl = B(-450, -230, ybi - 100, ybi, 150, 340)
    ctl = _fillet_try(ctl, _par(ctl, Axis.Y), [6.0, 4.0])
    add("Dock controller enclosure (ESP32, CAN, LTE-M)", ctl, C_BODY2, "plastic", 6, "internal", (-800, 300, 750))
    cled = _comp([_ycyl(-420 + 14 * k, ybi - 100.8, 320, 2.5, 1.6) for k in range(4)])
    add("Dock controller status lights (lit)", cled, C_LED_G, "emissive", 6, "internal", (-800, 300, 750))
    ant = _zcyl(-250, ybi - 50, 360, 6, 40)
    ant = _fillet_try(ant, _top(ant), [5.0, 3.0])
    add("LTE-M antenna", ant, C_BLACK, "rubber", 6, "internal", (-800, 300, 750))

    gy0 = ybi - 92
    grid = B(230, 450, gy0, ybi, 150, 350)
    grid = _fillet_try(grid, _par(grid, Axis.Y), [6.0, 4.0])
    grid -= B(250, 430, gy0 - 1, gy0 + 6, 230, 320)
    add("Grid input enclosure", grid, C_BODY2, "plastic", 8, "internal", (900, 0, -40))
    brk = _comp([B(258 + 18 * k, 274 + 18 * k, gy0 + 6, gy0 + 26, 240, 310) for k in range(9)])
    add("RCBO, breakers and surge protector", brk, C_WHITE, "plastic", 8, "internal", (900, 0, -40))
    tog = _comp([B(263 + 18 * k, 269 + 18 * k, gy0 + 1, gy0 + 8, 272, 284) for k in range(9)])
    add("Breaker toggles", tog, C_BLACK, "plastic", 8, "internal", (900, 0, -40))
    iso = _ycyl(340, gy0 - 1, 190, 18, 4) + B(330, 350, gy0 - 9, gy0 - 3, 176, 204)
    add("Lockable isolator", iso, C_RED, "plastic", 8, "internal", (900, 0, -40))

    my0 = ybi - 70
    mppt = B(-190, -40, my0, ybi, 150, 330)
    mppt = _fillet_try(mppt, _par(mppt, Axis.Y), [4.0, 2.0])
    add("MPPT solar charge controller", mppt, C_DARK, "metal", 13, "internal", (1500, -450, -350))
    mf = _comp([B(-186 + 12 * k, -180 + 12 * k, my0 - 6, my0, 160, 320) for k in range(12)])
    add("MPPT heat sink fins", mf, C_ALU, "metal", 13, "internal", (1500, -450, -350))
    mscr = B(-160, -70, my0 - 6.6, my0 - 6, 280, 315)
    add("MPPT display", mscr, C_SCREEN, "screen", 13, "internal", (1500, -450, -350))

    # ------------------------------------------------------------ 9 fire detection and suppression (model.py)
    EF = (0, 500, 350)
    add("Aerosol suppression unit on its straps", M["fire"].shape, C_RED, "painted", 9, "internal", EF)
    add("Heat and smoke detector", M["detector"].shape, C_WHITE, "plastic", 9, "internal", EF)

    # ------------------------------------------------------------ 10 plenum wall, roof fans, vent hood (model.py)
    EP = (0, 900, 250)
    add("Vent plenum wall", M["plenum"].shape, C_LINER, "metal", 10, "internal", EP)
    add("Roof fans, 120 mm", M["fans"].shape, C_BLACK, "plastic", 10, "internal", (0, 900, 450))
    hood = M["hood"].shape
    add("Vent hood with rear slots and rain lip", hood, C_BODY2, "painted", 10, "shell", (0, 900, 600))
    hx_, hyf, hyb, hh = P["hood"]
    mesh = B(-hx_ + t, hx_ - t, hyb - t - 1.2, hyb - t - 0.2, Z1 + 8, Z1 + 56)
    add("Vent hood insect mesh", mesh, C_DARK, "fabric", 10, "shell", (0, 900, 600))

    # ------------------------------------------------------------ 7 access panel
    EA = (700, -300, 0)
    ax0, ax1 = P["access_x"]
    az0, az1 = P["access_z"]
    col = B(ax0, ax1, YF - 4, YF, az0, az1)
    col = _fillet_try(col, _par(col, Axis.Y), [10.0, 6.0])
    col = _fillet_try(col, _front(col), [1.5, 1.0])
    add("Access panel bezel, steel", col, C_DARK, "painted", 7, "shell", EA)
    dz0_, dz1_ = P["display_z"]
    disp = B(ax0 + 20, ax1 - 20, YF - 8, YF - 4, dz0_, dz1_)
    disp = _fillet_try(disp, _par(disp, Axis.Y), [4.0, 2.0])
    add("Display bezel", disp, C_BLACK, "plastic", 7, "shell", EA)
    glass = B(ax0 + 26, ax1 - 26, YF - 8.6, YF - 7.9, dz0_ + 6, dz1_ - 6)
    add("Display glass", glass, C_SCREEN, "screen", 7, "shell", EA)
    ym = YF - 8.9
    ui = [B(ax0 + 30, ax1 - 30, ym, YF - 8.5, dz1_ - 22, dz1_ - 12)]
    ui_w = [_text_front("Tap to swap", (ax0 + ax1) / 2, YF - 8.6, dz1_ - 44, 15, 0.3)]
    tiles_g, tiles_a = [], []
    for k in range(4):
        x0 = ax0 + 32 + 30 * k
        tl = B(x0, x0 + 24, ym, YF - 8.5, dz0_ + 14, dz0_ + 52)
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
    for k in range(4):
        x = ax0 + 45 + 30 * k
        d = _ycyl(x, YF - 5.5, 1025, 4.0, 3.0)
        d = _fillet_try(d, _front(d), [1.5, 1.0])
        col_, mat_ = {"green": (C_LED_G, "emissive"), "amber": (C_LED_A, "emissive"), "off": (C_LED_OFF, "plastic")}[BAY_LIGHTS[k]]
        add(f"Access panel bay {k + 1} light", d, col_, mat_, 7, "shell", EA)
    buz = _comp([_ycyl(rx - 15 + 10 * i, YF - 4.2, az0 + 22, 2.0, 0.6) for i in range(4)])
    add("Buzzer grille", buz, C_BLACK, "plastic", 7, "shell", EA)
    scr = _comp([_ycyl(x, YF - 4.6, z, 3.0, 1.2) for x in (ax0 + 10, ax1 - 10) for z in (az0 + 10, az1 - 10)])
    add("Bezel security screws", scr, C_METAL, "metal", 16, "shell", EA)

    # ------------------------------------------------------------ 15 service door (model.py: piano hinge, intake slot, cam lock)
    ES = (0, -1100, -150)
    sd = M["service"].shape
    sd = _fillet_try(sd, _par(sd, Axis.Y), [3.0, 2.0])
    add("Service door, steel", sd, C_BODY, "painted", 15, "shell", ES)
    add("Service door intake filter pad", M["filter"].shape, C_DARK, "fabric", 10, "shell", ES)
    add("Service door cam lock", M["cam_lock"].shape, C_METAL, "metal", 15, "shell", ES)
    add("Service door piano hinge, stainless", M["service_hinge"].shape, C_METAL, "metal", 15, "shell", ES)
    warn = B(-440, -320, DF - 0.5, DF, 470, 620)
    add("Lithium battery warning label", warn, C_WARN, "paper", 16, "shell", ES)
    wtri = _text_front("!", -380, DF - 0.5, 560, 70, 0.3)
    wbar = _comp([B(-430, -330, DF - 0.8, DF - 0.4, 480 + 12 * k, 486 + 12 * k) for k in range(3)])
    add("Warning label print", _comp([wtri, wbar]), C_BLACK, "paper", 16, "shell", ES)
    info = B(-280, 20, DF - 0.5, DF, 540, 620)
    add("Operator information plate", info, C_WHITE, "paper", 16, "shell", ES)
    ink = _comp([B(-270, -40, DF - 0.8, DF - 0.4, 596, 608)]
                + [B(-270, 10 - 40 * (k % 2), DF - 0.8, DF - 0.4, 552 + 12 * k, 557 + 12 * k) for k in range(3)])
    add("Operator plate print", ink, C_DARK, "paper", 16, "shell", ES)

    # ------------------------------------------------------------ 14 plinth: welded channel frame (model.py)
    pl = M["plinth"].shape
    pl -= B(-W / 2 - 1, W / 2 + 1, YF - 1, YF + 1, Z0 - 12, Z0 - 10)       # shadow line under the body
    add("Plinth, welded steel channel", pl, C_PLINTH, "painted", 14, "shell", (0, 0, -350))
    add("Floor bolts", M["floor_bolts"].shape, C_BLACK, "metal", 16, "internal", (0, 0, -350))

    # ------------------------------------------------------------ 11, 12 canopy (group accessory)
    pw, pd, pt = P["panel"]
    place = panel_frame(P)
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
    add("Canopy posts on base and cap plates", M["posts"].shape, C_PLINTH, "painted", 12, "accessory", (0, 0, 1500))
    add("Canopy post bolts", M["post_bolts"].shape, C_METAL, "metal", 12, "accessory", (0, 0, 1500))
    add("Canopy rails", M["rails"].shape, C_PLINTH, "painted", 12, "accessory", (0, 0, 1700))
    add("Solar panel end clamps", M["clamps"].shape, C_ALU, "metal", 12, "accessory", (0, 0, 1900))

    # ------------------------------------------------------------ context: paved patch, rider, pack in hand
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
