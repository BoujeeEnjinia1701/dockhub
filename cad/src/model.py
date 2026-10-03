"""DockHub parametric model (build123d), TRL 3, constructable design (DKH-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL, print envelopes, heights and the fit check
    python cad/src/model.py --check    fit check only (overlaps and faces that must touch)

Every component is modelled as it is made or bought (DKH-DDR-003): a cabinet shell of folded
1.5 mm galvanized panels riveted together on a welded channel plinth, a roof frame of steel angle
that carries the canopy posts, a bay deck, charger shelf and plenum wall of folded sheet, bay liners
riveted to the front panel and the plenum wall, printed cradles with their guides, catch brackets,
doors on piano hinges with gaskets and solenoid locks, a vent hood over two roof fans, and a canopy
of welded posts, rails and panel end clamps. `build_components()` returns them one by one;
`build_parts()` groups them by BOM line for the concept media.

Axes: X along the cabinet width, Y front (-Y, street side where riders stand) to back (+Y),
Z up from the sidewalk. Units mm. Each pack stands connector down, lid face toward the rider and
back face (latch pawl) toward the plenum, as in the SwapCell wall dock (interface v0.3).

Configurations (DKH-DDR-001 item 1): the cabinet is built for four bays. The first prototype
fits bays 1 and 2 (PARAMS["bays_fitted"] = 2); bays 3 and 4 are closed with blank plates.
The concept media show the full four-bay fit.

Options added on 2026-10-02 (DKH-DEC-001): build_components(variant="vermiculite") adds a stainless
tray of exfoliated vermiculite on the floor of each fitted bay, in front of the cradle, for the
propagation trial (the first prototype keeps the aerosol unit and plain floors); and
build_components(site=True) adds the cast concrete pad and the four M12 wedge anchors of the first
pilot site on private ground (R15), which are outside the build plan.
"""
import math
import sys
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Cabinet (DKH-PRC-001, R10, R13)
    "W": 1000.0, "D": 500.0,         # footprint, X by Y; the plinth is flush with the body
    "plinth_h": 100.0,               # welded 100 x 50 x 5 channel plinth; the body floor sits on it
    "channel": (100.0, 50.0, 5.0),   # plinth channel: depth, flange width, thickness
    "roof_z": 1500.0,                # top of the body
    "sheet_t": 1.5,                  # galvanized steel sheet (R10)
    "flange": 25.0,                  # folded flange on floor, deck, shelf and plenum wall
    "roof_flange": 40.0,             # roof down-flange (the roof beam cleats bolt through it)
    "tech_z1": 680.0,                # top of the technical compartment
    # Bays (R11): four in one row at hand height
    "n_bays": 4, "bays_fitted": 2,
    "bay_pitch": 196.0, "bay_open_w": 150.0,   # opening narrowed from 172 (DDR-003) to leave a hinge land between doors
    "bay_z0": 700.0, "bay_z1": 1220.0,   # bay floor and top of the liner opening zone
    "open_z": (705.0, 1215.0),       # door opening in the front panel
    "liner_w": 180.0, "liner_y1": 110.0, "liner_top": 1230.0,
    "plenum_t": 1.5,                 # plenum wall is folded 1.5 mm sheet (was a 10 mm massing slab)
    "cradle_h": 30.0,                # cradle; pack connector face rests on its top
    "cradle_w": 150.0,
    "guide_h": 130.0,                # side guides printed with the cradle
    "door": (172.0, 526.0, 2.0),     # bay door plate: width, height, thickness (11 mm overlap each side)
    "gasket": (7.0, 3.0),            # EPDM gasket strip width and compressed thickness
    "door_handle_z": (940.0, 980.0),
    "lock_z": (935.0, 985.0),
    # SwapCell interface v0.3 envelope (SWC-PRC-001 v0.3)
    "pack_l": 340.0, "pack_w": 90.0, "pack_d": 80.0,
    "plug_w": 56.0, "plug_d": 34.0, "plug_h": 18.0, "plug_offset": 8.0,
    "handle_w": 84.0, "handle_d": 22.0, "handle_h": 35.0,
    "latch_w": 36.0, "latch_from_top": 45.0, "latch_proud": 10.0, "latch_h": 24.0,
    "guide_clear": 1.0,
    # Access panel (R11): reader and display
    "access_x": (310.0, 490.0), "access_z": (850.0, 1210.0),
    "reader_z": (900.0, 990.0), "display_z": (1060.0, 1190.0),
    # Service opening and door
    "service_open": (450.0, 150.0, 650.0),       # half width, bottom, top
    "intake": (200.0, 170.0, 250.0),             # filtered intake slot in the service door: half width, bottom, top
    # Vent: two 120 mm fans under the roof blowing into a hood with slots on its back face
    "fan_x": 350.0, "fan_y": 173.0, "fan_hole_r": 55.0,
    "hood": (425.0, 98.5, 231.5, 70.0),          # half width, front face y, back face y, height
    "hood_slots": (12, 50.0, 40.0),              # number, width, height of the rear slots
    # Canopy (R6, R13, R15): 400 W panel, long side along X
    "panel": (1722.0, 1134.0, 35.0), "tilt_deg": 10.0,
    "panel_y": -150.0, "panel_z": 2330.0,     # panel centre
    "post": 50.0, "post_t": 3.0, "post_x": 460.0, "post_y": 200.0, "rail_h": 40.0, "rail_w": 50.0,
    "rail_over": 20.0,               # rail runs past each panel edge for the end clamp
    "base_plate": (50.0, 100.0, 8.0), "cap_t": 6.0,
    "beam": (40.0, 4.0),             # roof beams and cleats: 40 x 40 x 4 steel angle
    # Plinth anchors (R15): four M12 at this inset from the plinth edges
    "anchor_inset": 60.0,            # front-to-back: anchors 30 mm in from the front and back edges
    "anchor_x": 475.0,               # sideways: anchors 25 mm in from the ends, clear of the boxes above them
    # Site (R15, decided 2026-10-02: first pilot on private ground): cast pad and anchors, outside the build plan
    "pad": (1400.0, 1100.0, 300.0),  # reinforced concrete pad, X by Y by depth, top flush with the ground, cabinet centred
    "anchor": (12.0, 100.0, 160.0),  # M12 stainless wedge anchor: diameter, embedment, overall length
    # Trial option (decided 2026-10-02): vermiculite-filled bay floor for the propagation trial
    "verm_tray": (20.0, 1.0, 2.0),   # tray height, stainless sheet thickness, fill level below the rim
}


VERM_GAP = 3.0                       # trial tray ends this far in front of the cradle, mm
SOCKET_R = 14.0                      # radius of a 19 mm socket on an extension, for the anchor nut access check, mm


# ---------------------------------------------------------------------------- helpers
def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _cz(r, z0, z1, x, y):
    from build123d import Cylinder, Pos
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def _cy(r, y0, y1, x, z):
    from build123d import Cylinder, Pos, Rot
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)


def _union(shapes):
    shapes = [s for s in shapes if s is not None]
    out = shapes[0]
    for s in shapes[1:]:
        out = out + s
    return out


def bay_x(p=PARAMS):
    """Bay centre lines, bay 1 at -X."""
    n = p["n_bays"]
    return [(i - (n - 1) / 2) * p["bay_pitch"] - p["bay_pitch"] / 2 for i in range(n)]


def pack_z0(p=PARAMS):
    """Height of the pack connector face (resting on the cradle)."""
    return p["bay_z0"] + p["sheet_t"] + p["cradle_h"] - 1.5


def canopy_heights(p=PARAMS):
    """Underside of the panel at its rear (lowest) edge and top of its front edge, mm."""
    pw, pd, pt = p["panel"]
    a = math.radians(p["tilt_deg"])
    half = pd / 2
    z_rear_under = p["panel_z"] - half * math.sin(a) - pt / 2 * math.cos(a)
    z_front_top = p["panel_z"] + half * math.sin(a) + pt / 2 * math.cos(a)
    y_front = p["panel_y"] - half * math.cos(a)
    y_rear = p["panel_y"] + half * math.cos(a)
    return z_rear_under, z_front_top, y_front, y_rear


def key_heights(p=PARAMS):
    """Heights of operable parts and pack features for the R11 reach check, mm."""
    z0 = pack_z0(p)
    return {
        "pack connector face": z0,
        "pack body top": z0 + p["pack_l"],
        "pack handle top": z0 + p["pack_l"] + p["handle_h"],
        "door handle": p["door_handle_z"],
        "reader": p["reader_z"],
        "display": p["display_z"],
        "bay opening top": p["open_z"][1],
    }


def panel_frame(p=PARAMS):
    """Location of the panel's own axes (x along the long side, y up the slope toward the street, z normal)."""
    from build123d import Pos, Rot
    return Pos(0, p["panel_y"], p["panel_z"]) * Rot(-p["tilt_deg"], 0, 0)


def to_global(ly, lz, p=PARAMS):
    """Global (y, z) of a point at panel-local (ly, lz)."""
    a = math.radians(-p["tilt_deg"])
    return p["panel_y"] + ly * math.cos(a) - lz * math.sin(a), p["panel_z"] + ly * math.sin(a) + lz * math.cos(a)


def to_local(y, z, p=PARAMS):
    a = math.radians(-p["tilt_deg"])
    dy, dz = y - p["panel_y"], z - p["panel_z"]
    return dy * math.cos(a) + dz * math.sin(a), -dy * math.sin(a) + dz * math.cos(a)


def post_geometry(p=PARAMS):
    """Each canopy post: (x, y, z_bottom_of_post, z_top_at_axis, local y of the post axis on the cap plane)."""
    pt = p["panel"][2]
    lz_cap = -pt / 2 - p["rail_h"] - p["cap_t"]          # underside of the cap plate, panel-local
    a = math.radians(p["tilt_deg"])
    out = []
    for x in (-p["post_x"], p["post_x"]):
        for y in (-p["post_y"], p["post_y"]):
            # solve y = PY + ly cos(-a) - lz sin(-a) for ly with lz = lz_cap
            ly = (y - p["panel_y"] + lz_cap * math.sin(-a)) / math.cos(-a)
            _, ztop = to_global(ly, lz_cap, p)
            out.append((x, y, p["roof_z"] + p["base_plate"][2], ztop, ly))
    return out


def _pack(xc, p):
    """SwapCell v0.3 reference pack standing connector down at bay centre xc."""
    b = _box
    z0 = pack_z0(p); z1 = z0 + p["pack_l"]
    hw, hd = p["pack_w"] / 2, p["pack_d"] / 2
    body = b(xc - hw, xc + hw, -hd, hd, z0, z1)
    yc = p["plug_offset"]
    plug = b(xc - p["plug_w"] / 2, xc + p["plug_w"] / 2, yc - p["plug_d"] / 2, yc + p["plug_d"] / 2,
             z0 - p["plug_h"], z0)
    hh = p["handle_h"]
    handle = b(xc - p["handle_w"] / 2, xc + p["handle_w"] / 2, -p["handle_d"] / 2, p["handle_d"] / 2, z1, z1 + hh) \
        - b(xc - p["handle_w"] / 2 + 11, xc + p["handle_w"] / 2 - 11, -p["handle_d"], p["handle_d"], z1 - 1, z1 + 25)
    zl = z1 - p["latch_from_top"]
    pawl = b(xc - p["latch_w"] / 2, xc + p["latch_w"] / 2, hd, hd + p["latch_proud"],
             zl - p["latch_h"] / 2, zl + p["latch_h"] / 2)
    return body + plug + handle + pawl


# ---------------------------------------------------------------------------- derived positions
def derived(p=PARAMS):
    W, D, t = p["W"], p["D"], p["sheet_t"]
    d = {
        "xi": W / 2 - t,                     # inner face of the side panels
        "yf": -D / 2, "yb": D / 2,
        "yfi": -D / 2 + t, "ybi": D / 2 - t,  # inner faces of front and back panels
        "z0": p["plinth_h"], "z1": p["roof_z"],
        "flx": W / 2 - 2 * t,                # inner face of a flange lying on a side panel
        "notch_y": D / 2 - t - p["flange"],  # front and back panel side flanges end here
        "deck_z": p["bay_z0"],               # top of the bay deck
        "shelf_z": 380.0,                    # top of the charger shelf
        "floor_bolts": [(-400, -225), (-150, -225), (150, -225), (400, -225), (20, 225), (180, 225), (-475, 0), (475, 0)],
        "anchors": [(sx * p["anchor_x"], sy * (D / 2 - p["anchor_inset"] / 2)) for sx in (-1, 1) for sy in (-1, 1)],
        "charger_x": [-345.0, -115.0, 115.0, 345.0],
        "post_bolts_y": (165.0, 235.0),
    }
    return d


# ---------------------------------------------------------------------------- components
class Comp:
    def __init__(self, key, name, shape, color, bom, explode=(0, 0, 0)):
        self.key, self.name, self.shape, self.color, self.bom, self.explode = key, name, shape, color, bom, explode


def build_components(p=PARAMS, fitted=None, variant=None, site=False):
    """Every component as made or bought, as a dict key -> Comp, in build order.
    variant="vermiculite" adds the trial bay floor trays; site=True adds the pad and anchors."""
    from build123d import Pos
    b = _box
    fitted = p["bays_fitted"] if fitted is None else fitted
    d = derived(p)
    W, D, t = p["W"], p["D"], p["sheet_t"]
    xi, flx, ny = d["xi"], d["flx"], d["notch_y"]
    yf, yb, yfi, ybi = d["yf"], d["yb"], d["yfi"], d["ybi"]
    Z0, Z1 = d["z0"], d["z1"]
    fl, rfl = p["flange"], p["roof_flange"]
    xs = bay_x(p)
    fit, blank = xs[:fitted], xs[fitted:]
    C = {}

    def add(key, name, shape, color, bom, explode=(0, 0, 0)):
        C[key] = Comp(key, name, shape, color, bom, explode)

    # 1 Plinth: 100 x 50 x 5 channel, mitred and welded, flanges inward; anchor holes in the bottom flange,
    #   body bolt holes in the top flange
    ch_d, ch_f, ch_t = p["channel"]
    plinth = b(-W / 2, W / 2, yf, yb, 0, Z0) - b(-W / 2 + ch_t, W / 2 - ch_t, yf + ch_t, yb - ch_t, ch_t, Z0 - ch_t) \
        - b(-W / 2 + ch_f, W / 2 - ch_f, yf + ch_f, yb - ch_f, -1, Z0 + 1)
    for x, y in d["anchors"]:
        plinth = plinth - _cz(7.0, -1, ch_t + 1, x, y)
        plinth = plinth - _cz(16.0, Z0 - ch_t - 1, Z0 + 1, x, y)      # 32 mm socket hole in the top flange over each anchor
    for x, y in d["floor_bolts"]:
        plinth = plinth - _cz(5.5, Z0 - ch_t - 1, Z0 + 1, x, y)
    add("plinth", "Plinth", plinth, "#6B7280", 14)

    # 2 Floor pan: plate between the walls, 25 mm flanges up, corners notched
    floor = b(-xi, xi, -ybi, ybi, Z0, Z0 + t) \
        + b(-flx, flx, yfi, yfi + t, Z0 + t, Z0 + t + fl) + b(-flx, flx, ybi - t, ybi, Z0 + t, Z0 + t + fl) \
        + b(-xi, -flx, -ny, ny, Z0 + t, Z0 + t + fl) + b(flx, xi, -ny, ny, Z0 + t, Z0 + t + fl)
    for x, y in d["floor_bolts"]:
        floor = floor - _cz(5.5, Z0 - 1, Z0 + t + 1, x, y)
    floor = floor - _cz(12.5, Z0 - 1, Z0 + t + 1, 340, 120)            # grid cable gland
    for x, y in d["anchors"]:
        floor = floor - _cz(20.0, Z0 - 1, Z0 + t + 1, x, y)            # socket access to the anchor nuts, capped
    add("floor", "Floor pan", floor, "#C7CBD1", 1)
    fb = _union([_cz(5.0, Z0 - ch_t - 6, Z0 + t, x, y) + _cz(8.5, Z0 + t, Z0 + t + 7, x, y) for x, y in d["floor_bolts"]])
    add("floor_bolts", "Floor bolts, M10 (8)", fb, "#111827", 16)

    # 3 Back panel with forward side flanges; the electrical boxes screw to it
    back = b(-W / 2, W / 2, ybi, yb, Z0, Z1) + b(-xi, -flx, ny, ybi, Z0 + t, Z1 - t) + b(flx, xi, ny, ybi, Z0 + t, Z1 - t)
    add("back", "Back panel", back, "#D1D5DB", 1)

    # 4 Side panels, flat
    add("side_l", "Left side panel", b(-W / 2, -xi, yfi, ybi, Z0, Z1), "#D1D5DB", 1)
    add("side_r", "Right side panel", b(xi, W / 2, yfi, ybi, Z0, Z1), "#D1D5DB", 1)

    # 5 Charger shelf: folded sheet, side flanges riveted to the side panels
    sz = d["shelf_z"]
    shelf = b(-flx, flx, -60, 220, sz - t, sz) + b(-flx, flx, -60, -60 + t, sz - t - fl, sz - t) \
        + b(-flx, flx, 220 - t, 220, sz - t - fl, sz - t) + b(-xi, -flx, -60, 220, sz - t - fl, sz) + b(flx, xi, -60, 220, sz - t - fl, sz)
    add("shelf", "Charger shelf", shelf, "#9CA3AF", 1)

    # 6 Electrical boxes on the back panel, chargers on the shelf
    add("controller", "Dock controller (ESP32, CAN, LTE-M)", b(-450, -230, ybi - 100, ybi, 150, 340), "#15803D", 6)
    add("mppt", "MPPT solar charge controller", b(-190, -40, ybi - 70, ybi, 150, 330), "#B45309", 13)
    add("grid", "Grid input and protection", b(230, 450, ybi - 92, ybi, 150, 350), "#991B1B", 8)
    add("chargers", "Chargers, 54.6 V 5 A", _union([b(x - 80, x + 80, -20, 180, sz, sz + 70) for x in d["charger_x"][:fitted]]),
        "#C2410C", 5)

    # 7 Bay deck: folded sheet, flanges down; per fitted bay four cradle screw holes and a cable hole
    dz = d["deck_z"]
    deck = b(-flx, flx, yfi, p["liner_y1"], dz - t, dz) + b(-flx, flx, yfi, yfi + t, dz - t - fl, dz - t) \
        + b(-flx, flx, p["liner_y1"] - t, p["liner_y1"], dz - t - fl, dz - t) \
        + b(-xi, -flx, -ny, p["liner_y1"], dz - t - fl, dz) + b(flx, xi, -ny, p["liner_y1"], dz - t - fl, dz)

    def bay_holes(xc, z0, z1):
        h = b(xc - 20, xc + 20, p["plug_offset"] - 15, p["plug_offset"] + 15, z0, z1)
        for sx in (-1, 1):
            for sy in (-1, 1):
                h = h + _cz(2.75, z0, z1, xc + sx * 60, sy * 60)
        return h
    for xc in fit:
        deck = deck - bay_holes(xc, dz - t - 1, dz + 1)
    add("deck", "Bay deck", deck, "#9CA3AF", 1)

    # 8 Front panel: laser cut with the bay, service and access openings; side flanges folded back
    o0, o1 = p["open_z"]
    HW = p["bay_open_w"] / 2
    so_w, so_0, so_1 = p["service_open"]
    front = b(-W / 2, W / 2, yf, yfi, Z0, Z1)
    for xc in xs:
        front = front - b(xc - HW, xc + HW, yf - 1, yfi + 1, o0, o1)
    front = front - b(-so_w, so_w, yf - 1, yfi + 1, so_0, so_1) - b(340, 460, yf - 1, yfi + 1, 880, 1180)
    front = front + b(-xi, -flx, yfi, -ny, Z0 + t, Z1 - t) + b(flx, xi, yfi, -ny, Z0 + t, Z1 - t)
    add("front", "Front panel", front, "#E5E7EB", 1)

    # 9 Plenum wall: folded sheet with a vent port per fitted bay; notched at the top for the roof beams
    LY1, pt_ = p["liner_y1"], p["plenum_t"]
    bw, bt = p["beam"]
    px0 = p["post_x"] - bw / 2 - 2
    plenum = b(-flx, flx, LY1, LY1 + pt_, dz - t - fl, Z1 - 2 * t) + b(-px0 + 0, px0, LY1 - 20, LY1 + pt_, Z1 - 2 * t, Z1 - t) \
        + b(-xi, -flx, LY1 + pt_, LY1 + pt_ + 20, dz - t - fl, 1455) + b(flx, xi, LY1 + pt_, LY1 + pt_ + 20, dz - t - fl, 1455)
    for sx in (-1, 1):
        plenum = plenum - b(sx * px0 - (0 if sx > 0 else bw + 4), sx * px0 + (bw + 4 if sx > 0 else 0), LY1 - 21, LY1 + pt_ + 1, Z1 - t - bw - 2, Z1)
    for xc in fit:
        plenum = plenum - b(xc - 30, xc + 30, LY1 - 1, LY1 + pt_ + 1, 1140, 1200)
    add("plenum", "Plenum wall", plenum, "#4B5563", 10)

    # 10 Bay liners: folded box open at the front, top flange riveted to the front panel, back riveted to the plenum
    lw = p["liner_w"] / 2
    lt = p["liner_top"]
    liners = []
    for xc in fit:
        ln = b(xc - lw, xc + lw, yfi, LY1, dz, lt) - b(xc - lw + t, xc + lw - t, yfi - 1, LY1 - t, dz + t, lt - t) \
            - b(xc - 30, xc + 30, LY1 - t - 1, LY1 + 1, 1140, 1200) + b(xc - lw, xc + lw, yfi, yfi + t, lt, lt + 15)
        ln = ln - bay_holes(xc, dz - 1, dz + t + 1)
        liners.append(ln)
    add("liners", "Bay liners", _union(liners), "#9CA3AF", 3)

    # 11 Cradles (printed, guides printed on), receptacles, catch brackets
    pz0 = pack_z0(p)
    cz0 = dz + t
    hw, hd = p["pack_w"] / 2, p["pack_d"] / 2
    cw = p["cradle_w"] / 2
    yc = p["plug_offset"]
    zl = pz0 + p["pack_l"] - p["latch_from_top"]
    yb_ = hd + p["latch_proud"] + 1
    cradles, recs, catches = [], [], []
    for xc in fit:
        cr = b(xc - cw, xc + cw, -cw, cw, cz0, pz0)
        cr = cr - b(xc - p["plug_w"] / 2 - 1, xc + p["plug_w"] / 2 + 1, yc - p["plug_d"] / 2 - 1, yc + p["plug_d"] / 2 + 1,
                    pz0 - p["plug_h"] - 1.5, pz0 + 1)
        cr = cr - b(xc - p["plug_w"] / 2 - 8, xc + p["plug_w"] / 2 + 8, yc - p["plug_d"] / 2 - 8, yc + p["plug_d"] / 2 + 8,
                    cz0 - 1, pz0 - p["plug_h"] - 1.5)
        cr = cr - b(xc - 31, xc + 31, yb_ + 8 - 0.5, yb_ + 11.5, pz0 - 10, pz0 + 1)          # slot for the catch bracket
        for sx in (-1, 1):
            for sy in (-1, 1):
                cr = cr - _cz(2.75, cz0 - 1, pz0 + 1, xc + sx * 60, sy * 60)
        g = p["guide_clear"]
        cr = cr + b(xc - hw - g - 5, xc - hw - g, -45, 45, pz0, pz0 + p["guide_h"]) \
            + b(xc + hw + g, xc + hw + g + 5, -45, 45, pz0, pz0 + p["guide_h"])
        cradles.append(cr)
        recs.append(b(xc - p["plug_w"] / 2 - 8, xc + p["plug_w"] / 2 + 8, yc - p["plug_d"] / 2 - 8, yc + p["plug_d"] / 2 + 8,
                      cz0, pz0 - p["plug_h"] - 1.5))
        yp0, yp1 = yb_ + 8, yb_ + 11
        ztop = zl + 30
        cat = b(xc - 30, xc + 30, yp0, yp1, pz0 - 10, ztop) + b(xc - 30, xc + 30, yp0, LY1 - t, ztop - 3, ztop) \
            + b(xc - 30, xc + 30, LY1 - t - 3, LY1 - t, ztop - 43, ztop - 3) \
            + b(xc - 25, xc + 25, yb_, yp0, zl + p["latch_h"] / 2 + 1, zl + p["latch_h"] / 2 + 9)
        catches.append(cat)
    add("cradles", "Cradles with guides (printed)", _union(cradles), "#0E7490", 3)
    add("receptacles", "SwapCell receptacles", _union(recs), "#1F2937", 3)
    add("catches", "Catch brackets", _union(catches), "#7C3AED", 3)

    # 12 Solenoid locks on the liner wall
    lz0, lz1 = p["lock_z"]
    add("locks", "Solenoid locks", _union([b(xc + lw - t - 30, xc + lw - t, yfi + 2.5, yfi + 32.5, lz0, lz1) for xc in fit]),
        "#374151", 2)

    # 13 Bay doors (plate, handle, lock tongue), gaskets, piano hinges; blank plates on unfitted bays
    dw, dh, dt = p["door"]
    gw, gt = p["gasket"]
    dz0 = (o0 + o1) / 2 - dh / 2
    hz0, hz1 = p["door_handle_z"]
    ydb = yf - gt                                  # door back face
    doors, gaskets, hinges = [], [], []
    for xc in fit:
        doors.append(b(xc - dw / 2, xc + dw / 2, ydb - dt, ydb, dz0, dz0 + dh)
                     + b(xc + 45, xc + 70, ydb - dt - 16, ydb - dt, hz0, hz1)
                     + b(xc + 50, xc + 54, ydb, yfi + 16.5, 950, 970))
        gaskets.append(b(xc - HW - 1 - gw, xc + HW + 1 + gw, ydb, yf, o0 - 1 - gw, o1 + 1 + gw)
                       - b(xc - HW - 1, xc + HW + 1, ydb - 1, yf + 1, o0 - 1, o1 + 1))
        hx = xc - dw / 2 - 3.5
        hinges.append(b(xc - dw / 2 - 18, xc - dw / 2 - 7, yf - t, yf, o0 + 15, o1 - 15)
                      + _cz(3.5, o0 + 15, o1 - 15, hx, yf - 3.5)
                      + b(xc - dw / 2, xc - dw / 2 + 16, ydb - dt - t, ydb - dt, o0 + 15, o1 - 15))
    add("doors", "Bay doors", _union(doors), "#0F766E", 2)
    add("gaskets", "Door gaskets", _union(gaskets), "#111827", 2)
    add("hinges", "Door hinges", _union(hinges), "#9CA3AF", 2)
    if blank:
        add("blanks", "Blank plates", _union([b(xc - dw / 2, xc + dw / 2, yf - 2, yf, dz0, dz0 + dh) for xc in blank]), "#D1D5DB", 1)

    # 14 Access panel on the front
    ax0, ax1 = p["access_x"]
    add("access", "Access panel (NFC reader, display)", b(ax0, ax1, yf - 4, yf, *p["access_z"])
        + b(ax0 + 20, ax1 - 20, yf - 8, yf - 4, *p["display_z"]) + b(ax0 + 45, ax1 - 45, yf - 8, yf - 4, *p["reader_z"]), "#1F2937", 7)

    # 15 Service door with intake slot, filter pad, piano hinge and cam lock
    sw = so_w + 10
    sd = b(-sw, sw, ydb - dt, ydb, so_0 - 10, so_1 + 10)
    iw, iz0, iz1 = p["intake"]
    sd = sd - b(-iw, iw, ydb - dt - 1, ydb + 1, iz0, iz1) - _cy(9.5, ydb - dt - 1, ydb + 1, 420, 400)
    add("service", "Service door", sd, "#E5E7EB", 15)
    add("service_gasket", "Service door gasket", b(-so_w - 1 - gw, so_w + 1 + gw, ydb, yf, so_0 - 1 - gw, so_1 + 1 + gw)
        - b(-so_w - 1, so_w + 1, ydb - 1, yf + 1, so_0 - 1, so_1 + 1), "#111827", 15)
    add("service_hinge", "Service door hinge", b(-sw - 18, -sw - 7, yf - t, yf, so_0 + 20, so_1 - 20)
        + _cz(3.5, so_0 + 20, so_1 - 20, -sw - 3.5, yf - 3.5) + b(-sw, -sw + 16, ydb - dt - t, ydb - dt, so_0 + 20, so_1 - 20),
        "#9CA3AF", 15)
    add("cam_lock", "Cam lock", _cy(15, ydb - dt - 15, ydb - dt, 420, 400) + _cy(9, ydb - dt, yfi + 3, 420, 400)
        + b(410, 470, yfi + 0.5, yfi + 3.5, 390, 410), "#374151", 15)
    add("filter", "Intake filter pad", b(-iw - 5, iw + 5, ydb, ydb + 10, iz0 - 5, iz1 + 5), "#FDE68A", 10)

    # 16 Roof panel: plate between the walls, 40 mm down-flanges (corners notched); fan, gland and post bolt holes
    roof = b(-xi, xi, -ybi, ybi, Z1 - t, Z1) + b(-flx, flx, yfi, yfi + t, Z1 - t - rfl, Z1 - t) \
        + b(-flx, flx, ybi - t, ybi, Z1 - t - rfl, Z1 - t) \
        + b(-xi, -flx, -ny, ny, Z1 - t - rfl, Z1 - t) + b(flx, xi, -ny, ny, Z1 - t - rfl, Z1 - t)
    for sx in (-1, 1):
        roof = roof - _cz(p["fan_hole_r"], Z1 - t - 1, Z1 + 1, sx * p["fan_x"], p["fan_y"])
        for sy in (-1, 1):
            for yy in d["post_bolts_y"]:
                roof = roof - _cz(5.5, Z1 - t - 1, Z1 + 1, sx * p["post_x"], sy * yy)
    roof = roof - _cz(12.5, Z1 - t - 1, Z1 + 1, -200, 60)
    add("roof", "Roof panel", roof, "#D1D5DB", 1)

    # 17 Roof beams (40 x 40 x 4 angle) under the post lines, each bolted to a cleat at each end
    beams = []
    yb0 = -(yfi + t)                               # beam runs to the roof's front and back flanges
    ycl = yb0 - bt                                 # cleat face on the flange side
    for sx in (-1, 1):
        x_out, x_in = sx * (p["post_x"] + bw / 2), sx * (p["post_x"] - bw / 2)
        hl = b(min(x_out, x_in), max(x_out, x_in), -yb0, yb0, Z1 - t - bt, Z1 - t)
        for sy in (-1, 1):
            for yy in d["post_bolts_y"]:
                hl = hl - _cz(5.5, Z1 - t - bt - 1, Z1, sx * p["post_x"], sy * yy)
        vl = b(min(x_in, x_in + sx * bt), max(x_in, x_in + sx * bt), -yb0, yb0, Z1 - t - bw, Z1 - t - bt)
        beam = hl + vl
        for sy in (-1, 1):
            y_wall = -ycl if sy < 0 else ycl             # inner face of the cleat's wall leg
            ya, yb2 = (y_wall - bt, y_wall) if sy < 0 else (y_wall, y_wall + bt)
            xa, xb = sorted((x_in, x_in - sx * bw))
            leg_wall = b(xa, xb, min(ya, yb2), max(ya, yb2), Z1 - t - bw, Z1 - t - bt)
            xc0, xc1 = sorted((x_in, x_in - sx * bt))
            yl0, yl1 = sorted((y_wall, y_wall - sy * bw))
            leg_beam = b(xc0, xc1, yl0, yl1, Z1 - t - bw, Z1 - t - bt)
            beam = beam + leg_wall + leg_beam
        beams.append(beam)
    add("beams", "Roof beams and cleats", _union(beams), "#374151", 1)

    # 18 Roof fans (on 4 mm spacers), fire unit on its straps, heat and smoke detector
    fans = []
    for sx in (-1, 1):
        fx = sx * p["fan_x"]
        f = b(fx - 60, fx + 60, p["fan_y"] - 60, p["fan_y"] + 60, Z1 - t - 4 - 25, Z1 - t - 4)
        for ex in (-52.5, 52.5):
            for ey in (-52.5, 52.5):
                f = f + _cz(4, Z1 - t - 4, Z1 - t, fx + ex, p["fan_y"] + ey)
        fans.append(f)
    add("fans", "Roof fans, 120 mm (2)", _union(fans), "#4B5563", 10)
    from build123d import Rot, Cylinder
    fyc = ybi - 41.5
    fire = Pos(-60, fyc, 1420) * Rot(0, 90, 0) * Cylinder(38, 420)
    for sxx in (-210, 90):
        fire = fire + (Pos(sxx, fyc, 1420) * Rot(0, 90, 0) * (Cylinder(40, 20) - Cylinder(38, 22))) \
            + b(sxx - 10, sxx + 10, fyc + 32, ybi, 1400, 1440)
    add("fire", "Aerosol suppression unit on its straps", fire, "#DC2626", 9)
    add("detector", "Heat and smoke detector", _cz(45, Z1 - t - 25, Z1 - t, 200, 160), "#F87171", 9)

    # 19 Vent hood over the fans, slots on its back face, flanges riveted to the roof
    hx, hyf, hyb, hh = p["hood"]
    n, sw_, sh_ = p["hood_slots"]
    hood = b(-hx, hx, hyf, hyf + t, Z1, Z1 + hh) + b(-hx, hx, hyf - 20, hyf, Z1, Z1 + t) \
        + b(-hx, -hx + t, hyf + t, hyb - t, Z1, Z1 + hh) + b(hx - t, hx, hyf + t, hyb - t, Z1, Z1 + hh) \
        + b(-hx - 8, -hx, hyf + t, hyb - t, Z1, Z1 + t) + b(hx, hx + 8, hyf + t, hyb - t, Z1, Z1 + t) \
        + b(-hx, hx, hyf, hyb + 10, Z1 + hh - t, Z1 + hh) \
        + b(-hx, hx, hyb - t, hyb, Z1, Z1 + hh - t) + b(-hx, hx, hyb, hyb + 15, Z1, Z1 + t)
    pitch = (2 * hx - 60) / (n - 1)
    for i in range(n):
        x = -hx + 30 + i * pitch
        hood = hood - b(x - sw_ / 2, x + sw_ / 2, hyb - t - 1, hyb + 1, Z1 + 12, Z1 + 12 + sh_)
    add("hood", "Vent hood", hood, "#4B5563", 10)

    # 20 Canopy: posts (50 x 50 x 3 SHS) welded to base and cap plates, rails (50 x 40 x 3 RHS), end clamps, panel
    F = panel_frame(p)
    pw, pd, pth = p["panel"]
    rh, rw, ro = p["rail_h"], p["rail_w"], p["rail_over"]
    bpw, bpl, bpt = p["base_plate"]
    posts, rails, clamps, pbolts = [], [], [], []
    for (x, y, zb, zt, ly) in post_geometry(p):
        s = p["post"] / 2
        tt = p["post_t"]
        cut = F * b(-3000, 3000, -3000, 3000, -3000, -pth / 2 - rh - p["cap_t"])
        tube = (b(x - s, x + s, y - s, y + s, zb, zt + 60) - b(x - s + tt, x + s - tt, y - s + tt, y + s - tt, zb - 1, zt + 61)) & cut
        cap = F * b(x - s, x + s, ly - 35, ly + 35, -pth / 2 - rh - p["cap_t"], -pth / 2 - rh)
        y0, y1 = (y - s - 25, y + s + 25)
        y0, y1 = max(y0, -D / 2), min(y1, D / 2)
        base = b(x - bpw / 2, x + bpw / 2, y0, y1, Z1, Z1 + bpt)
        for yy in d["post_bolts_y"]:
            base = base - _cz(5.5, Z1 - 1, Z1 + bpt + 1, x, math.copysign(yy, y))
            pbolts.append(_cz(5.0, Z1 - t - bt - 10, Z1 + bpt, x, math.copysign(yy, y))
                          + _cz(8.5, Z1 + bpt, Z1 + bpt + 7, x, math.copysign(yy, y))
                          + _cz(8.5, Z1 - t - bt - 9, Z1 - t - bt, x, math.copysign(yy, y)))
        posts.append(tube + cap + base)
    for x in (-p["post_x"], p["post_x"]):
        L = pd / 2 + ro
        rails.append(F * (b(x - rw / 2, x + rw / 2, -L, L, -pth / 2 - rh, -pth / 2)
                          - b(x - rw / 2 + 3, x + rw / 2 - 3, -L - 1, L + 1, -pth / 2 - rh + 3, -pth / 2 - 3)))
        for sy in (-1, 1):
            e = sy * pd / 2
            y0, y1 = sorted((e, e + sy * 15))
            yl0, yl1 = sorted((e - sy * 8, e + sy * 15))
            clamps.append(F * (b(x - 20, x + 20, y0, y1, -pth / 2, pth / 2 + 4) + b(x - 20, x + 20, yl0, yl1, pth / 2, pth / 2 + 4)))
    add("posts", "Canopy posts (4)", _union(posts), "#374151", 12)
    add("post_bolts", "Post bolts, M10 (8)", _union(pbolts), "#111827", 12)
    add("rails", "Canopy rails (2)", _union(rails), "#52525B", 12)
    add("panel", "Solar panel, 400 W", F * b(-pw / 2, pw / 2, -pd / 2, pd / 2, -pth / 2, pth / 2), "#1E3A8A", 11)
    add("clamps", "Panel end clamps (4)", _union(clamps), "#A1A1AA", 12)

    # 21 SwapCell packs (reference): one in each fitted bay except the empty bay (last fitted bay)
    if fitted > 1:
        add("packs", "SwapCell packs (reference)", _union([_pack(xc, p) for xc in fit[:-1]]), "#D4A017", 4)

    # 22 Trial option: vermiculite bay floor, a folded stainless tray riveted to the liner floor in front of the cradle,
    #    filled with exfoliated vermiculite to 2 mm below its rim (catches and smothers ejecta at the bay floor)
    if variant == "vermiculite":
        vh, vt, vfree = p["verm_tray"]
        trays, fills = [], []
        for xc in fit:
            x0, x1 = xc - lw + t + 1, xc + lw - t - 1
            y0, y1 = yfi + 2, -cw - VERM_GAP
            z0 = dz + t
            tr = b(x0, x1, y0, y1, z0, z0 + vh) - b(x0 + vt, x1 - vt, y0 + vt, y1 - vt, z0 + vt, z0 + vh + 1)
            trays.append(tr)
            fills.append(b(x0 + vt, x1 - vt, y0 + vt, y1 - vt, z0 + vt, z0 + vh - vfree))
        add("verm_trays", "Vermiculite floor trays (trial option)", _union(trays), "#94A3B8", 19)
        add("verm_fill", "Exfoliated vermiculite fill (trial option)", _union(fills), "#C8A165", 19)

    # 23 Site (outside the build plan): reinforced concrete pad, top flush with the ground, and four M12 wedge anchors
    #    through the plinth's bottom flange, each with a washer and a tamper-resistant nut inside the channel
    if site:
        pL, pB, pH = p["pad"]
        ad, emb, alen = p["anchor"]
        pad = b(-pL / 2, pL / 2, -pB / 2, pB / 2, -pH, 0)
        anc = []
        for x, y in d["anchors"]:
            pad = pad - _cz(ad / 2, -emb, 1, x, y)
            anc.append(_cz(ad / 2, -emb, ch_t + alen - emb, x, y) + _cz(12.0, ch_t, ch_t + 2.5, x, y)
                       + _cz(9.5, ch_t + 2.5, ch_t + 13.5, x, y))
        add("pad", "Concrete pad (site)", pad, "#A8A29E", 18)
        add("anchors", "Wedge anchors, M12 stainless (4)", _union(anc), "#111827", 17)
    return C


# ---------------------------------------------------------------------------- BOM groups for the concept media
GROUPS = [
    ("Cabinet body, galvanized steel", "#D1D5DB", 1, (0, 0, 0)),
    ("Bay doors with solenoid locks", "#0F766E", 2, (0, -1000, 0)),
    ("Bay compartments with cradle and receptacle", "#9CA3AF", 3, (0, -450, 0)),
    ("SwapCell packs (reference)", "#D4A017", 4, (0, -250, 1050)),
    ("Chargers, 54.6 V 5 A", "#C2410C", 5, (0, -520, -60)),
    ("Dock controller (ESP32, CAN, LTE-M)", "#15803D", 6, (-800, 300, 750)),
    ("Access panel (NFC reader, display)", "#1F2937", 7, (700, -300, 0)),
    ("Grid input and protection", "#991B1B", 8, (900, 0, -40)),
    ("Fire detection and aerosol suppression", "#DC2626", 9, (0, 500, 350)),
    ("Vent plenum, fans and roof hood", "#4B5563", 10, (0, 900, 250)),
    ("Solar panel, 400 W", "#1E3A8A", 11, (0, 0, 1900)),
    ("Canopy frame", "#374151", 12, (0, 0, 1500)),
    ("MPPT solar charge controller", "#B45309", 13, (1500, -450, -350)),
    ("Plinth and anchor frame", "#6B7280", 14, (0, 0, -350)),
    ("Service door", "#E5E7EB", 15, (0, -1100, -150)),
]


def build_parts(p=PARAMS, fitted=None, comps=None):
    """BOM-grouped parts for the concept media: list of (name, shape, colour, bom_item, explode_offset).
    Fixings (line 16) are left out."""
    C = comps or build_components(p, fitted)
    out = []
    for name, col, bom, ex in GROUPS:
        shapes = [c.shape for c in C.values() if c.bom == bom]
        if shapes:
            out.append((name, _union(shapes), col, bom, ex))
    return out


def assemblies(parts=None, parts4=None):
    from build123d import Compound
    parts = parts or build_parts()
    parts4 = parts4 or build_parts(fitted=PARAMS["n_bays"])
    by = {bom: s for _, s, _, bom, _ in parts if bom}
    return {
        "dockhub-assembly": Compound([s for _, s, _, _, _ in parts]),
        "dockhub-assembly-4-bays": Compound([s for _, s, _, _, _ in parts4]),
        "dockhub-cabinet": Compound([by[1], by[10], by[14], by[15]]),
        "dockhub-bay": [s for n, s, _, b_, _ in build_parts(fitted=1) if b_ == 3][0],
        "dockhub-canopy": Compound([by[11], by[12]]),
        "dockhub-bay-vermiculite": Compound([c.shape for k, c in build_components(fitted=1, variant="vermiculite").items()
                                             if c.bom in (3, 19)]),
        "dockhub-site-pad": Compound([c.shape for k, c in build_components(site=True).items() if k in ("plinth", "pad", "anchors")]),
    }


# ---------------------------------------------------------------------------- fit check
# Faces that must touch (the joint is made there)
CONTACTS = [
    ("plinth", "floor"), ("floor_bolts", "floor"), ("floor", "front"), ("floor", "back"), ("floor", "side_l"), ("floor", "side_r"),
    ("front", "side_l"), ("front", "side_r"), ("back", "side_l"), ("back", "side_r"),
    ("shelf", "side_l"), ("shelf", "side_r"), ("chargers", "shelf"),
    ("controller", "back"), ("mppt", "back"), ("grid", "back"),
    ("deck", "front"), ("deck", "side_l"), ("deck", "side_r"),
    ("plenum", "deck"), ("plenum", "side_l"), ("plenum", "side_r"), ("plenum", "roof"),
    ("liners", "deck"), ("liners", "front"), ("liners", "plenum"),
    ("cradles", "liners"), ("receptacles", "liners"), ("catches", "cradles"), ("catches", "liners"),
    ("locks", "liners"), ("gaskets", "front"), ("gaskets", "doors"), ("hinges", "front"), ("hinges", "doors"),
    ("access", "front"), ("service", "service_gasket"), ("service_gasket", "front"), ("service_hinge", "front"),
    ("service_hinge", "service"), ("cam_lock", "service"), ("filter", "service"),
    ("roof", "front"), ("roof", "back"), ("roof", "side_l"), ("roof", "side_r"), ("beams", "roof"),
    ("fans", "roof"), ("fire", "back"), ("detector", "roof"), ("hood", "roof"),
    ("posts", "roof"), ("post_bolts", "posts"), ("post_bolts", "beams"), ("rails", "posts"), ("panel", "rails"),
    ("clamps", "rails"), ("clamps", "panel"), ("blanks", "front"), ("packs", "cradles"),
    ("verm_trays", "liners"), ("verm_fill", "verm_trays"), ("pad", "plinth"), ("anchors", "plinth"), ("anchors", "pad"),
]
ALLOWED = set()


def _bb_apart(A, B, pad=0.0):
    return (A.min.X > B.max.X + pad or B.min.X > A.max.X + pad or A.min.Y > B.max.Y + pad or B.min.Y > A.max.Y + pad
            or A.min.Z > B.max.Z + pad or B.min.Z > A.max.Z + pad)


def _solids(shape):
    return list(shape.solids()) or [shape]


def check_fits(C=None, tol=1.0, verbose=True):
    """No two components may overlap (intersection volume under tol mm3), and every CONTACTS pair must touch."""
    C = C or build_components()
    keys = list(C)
    sol = {k: [(s, s.bounding_box()) for s in _solids(C[k].shape)] for k in keys}
    bbs = {k: C[k].shape.bounding_box() for k in keys}
    overlaps = []
    for i, a in enumerate(keys):
        for bk in keys[i + 1:]:
            if frozenset((a, bk)) in ALLOWED or _bb_apart(bbs[a], bbs[bk]):
                continue
            v = 0.0
            for sa, ba in sol[a]:
                for sb, bb_ in sol[bk]:
                    if _bb_apart(ba, bb_):
                        continue
                    r = sa & sb
                    v += r.volume if r is not None else 0.0
            if v >= tol:
                overlaps.append((a, bk, v))
    gaps = []
    n_contacts = 0
    for ka, kb in CONTACTS:
        if ka not in C or kb not in C:
            continue
        n_contacts += 1
        near = [(sa, sb) for sa, ba in sol[ka] for sb, bb_ in sol[kb] if not _bb_apart(ba, bb_, 1.0)]
        dist = min(sa.distance_to(sb) for sa, sb in near) if near else 99.0
        if dist > 0.05:
            gaps.append((ka, kb, dist))
    if verbose:
        print(f"fit check: {len(keys)} components; {len(overlaps)} overlaps; {n_contacts} contacts checked, {len(gaps)} missing")
        for o in overlaps:
            print(f"  OVERLAP {o[0]} / {o[1]}: {o[2]:.1f} mm3")
        for g in gaps:
            print(f"  NO CONTACT {g[0]} / {g[1]}: {g[2]:.2f} mm apart")
    return overlaps, gaps, n_contacts


def socket_access(C=None):
    """A socket on an extension must reach each anchor nut from inside the cabinet: the column from the nut top up
    through the floor must be clear of every component. Returns the intruding volume per component, mm3."""
    C = C or build_components(site=True)
    p = PARAMS
    d = derived(p)
    ch_t = p["channel"][2]
    z_nut = ch_t + 13.5
    col = _union([_cz(SOCKET_R, z_nut + 0.5, d["z0"] + p["sheet_t"] + 50, x, y) for x, y in d["anchors"]])
    out = {}
    for k, c in C.items():
        if k == "anchors":
            continue
        r = c.shape & col
        v = r.volume if r is not None else 0.0
        if v > 1.0:
            out[k] = v
    return out


def clearances(C=None):
    """Clearances that matter for building and use, mm."""
    C = C or build_components(fitted=PARAMS["n_bays"])
    p = PARAMS
    xs = bay_x(p)
    dw = p["door"][0]
    out = {
        "gap between neighbouring bay doors": p["bay_pitch"] - dw,
        "hinge land to the next door": p["bay_pitch"] - dw - 18,
        "pack to door opening, each side": p["bay_open_w"] / 2 - p["pack_w"] / 2,
        "pack handle top to opening top": p["open_z"][1] - key_heights()["pack handle top"],
        "bay 1 liner to side panel": (xs[0] - p["liner_w"] / 2) + (p["W"] / 2 - p["sheet_t"]),
        "liner to liner": p["bay_pitch"] - p["liner_w"],
        "door 4 to access panel": p["access_x"][0] - (xs[3] + dw / 2),
        "fan to plenum wall": p["fan_y"] - 60 - p["liner_y1"] - p["plenum_t"],
        "hood end to rear post base plate": p["post_x"] - p["post"] / 2 - p["hood"][0] - 8,
        "vermiculite tray to cradle": VERM_GAP,
        "vermiculite fill top to pack connector face": pack_z0(p) - (p["bay_z0"] + p["sheet_t"] + p["verm_tray"][0] - p["verm_tray"][2]),
        "vermiculite tray rim to bay opening bottom": p["bay_z0"] + p["sheet_t"] + p["verm_tray"][0] - p["open_z"][0],
        "anchor to pad edge, sideways": p["pad"][0] / 2 - p["anchor_x"],
        "anchor to pad edge, front and back": p["pad"][1] / 2 - (p["D"] / 2 - p["anchor_inset"] / 2),
    }
    return out


if __name__ == "__main__":
    if "--check" in sys.argv:
        C2 = build_components()
        o, g, n = check_fits(C2)
        C4 = build_components(fitted=PARAMS["n_bays"])
        o4, g4, n4 = check_fits(C4)
        print("vermiculite floor variant (trial option), four bays:")
        oV, gV, nV = check_fits(build_components(fitted=PARAMS["n_bays"], variant="vermiculite"))
        print("site: pad and anchors under the two-bay prototype:")
        CS = build_components(site=True)
        oS, gS, nS = check_fits(CS)
        sa = socket_access(CS)
        print(f"anchor nut socket access: {'clear' if not sa else 'BLOCKED by ' + ', '.join(f'{k} {v:.0f} mm3' for k, v in sa.items())}")
        for k, v in clearances(C4).items():
            print(f"clearance {k}: {v:.1f} mm")
        sys.exit(1 if (o or g or o4 or g4 or oV or gV or oS or gS or sa) else 0)
    from build123d import export_step, export_stl, Box, Pos
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    C2 = build_components()
    parts = build_parts(comps=C2)
    parts4 = build_parts(fitted=PARAMS["n_bays"])
    for name, shape in assemblies(parts, parts4).items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.5)
        bb = shape.bounding_box()
        print(f"{name:26s} {bb.size.X:7.1f} x {bb.size.Y:7.1f} x {bb.size.Z:7.1f} mm")
    zr, zf, yf, yr = canopy_heights()
    print(f"canopy: rear edge underside {zr:.0f} mm, front edge top {zf:.0f} mm, panel spans y {yf:.0f} to {yr:.0f} mm")
    canopy = [C2[k].shape for k in ("rails", "panel", "clamps")]
    big = 5000.0
    outside = Pos(0, -PARAMS["D"] / 2 - big / 2, 0) * Box(big, big, big) + Pos(0, PARAMS["D"] / 2 + big / 2, 0) * Box(big, big, big)
    zmin_out = min((c & outside).bounding_box().min.Z for c in canopy)
    print(f"canopy lowest point outside the footprint {zmin_out:.0f} mm")
    for k, v in key_heights().items():
        print(f"height {k}: {v} mm")
    check_fits(C2)
