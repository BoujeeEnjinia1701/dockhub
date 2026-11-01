"""DockHub parametric model, kit 1.9 interface (STANDARDS section 24), detail level D3 for every option.

Run from the repo root:
    python .kit/cad_check.py --export     fidelity check, STEP per part and per assembly (cad/step/)
    python cad/src/model.py               part list with masses, and STL of the chosen design (cad/stl/)

Axes: X along the cabinet width, Y front (-Y, street side where riders stand) to back (+Y), Z up from the
sidewalk (ground level is z = 0). Units mm. Each pack stands connector down, lid face toward the rider and back
face (latch pawl) toward the plenum, as in the SwapCell wall dock (interface v0.3).

Options (DKH-OPT-001). Option A is the current design (DKH-PRC-001, DKH-DDR-003); it is modelled as built for the
first prototype: a cabinet built for four bays with bays 1 and 2 fitted and bays 3 and 4 closed by blank plates.
    A  Swap bays: four steel compartments, each with its own door, charger and CAN channel; the rider lifts a
       charged pack out by hand. Free-standing cabinet on a cast pad with a 400 W solar canopy.
    B  Rotary magazine: four pack pockets on a motor-indexed turret behind one rider hatch; the rider never
       opens a compartment that holds a charging pack. Same plinth, pad, anchors and canopy.
    C  Locker bank: six lockers in which riders charge their own packs; nothing is swapped and there is no
       pool of packs. Same plinth, pad and anchors, no canopy.

Every part is a cad_parts.part() dict: made, bought, fastener, weld or context. BOM line numbers are given for
option A only (the chosen option). `components(option, fitted=None, variant=None, site=True)` also takes the number of
fitted bays (four for the media), the trial vermiculite floor ("vermiculite") and whether the site pad and anchors
are included. `grouped()` returns the parts of option A merged by build-plan group for the build plan pictures.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Cylinder, Compound, Location, Plane, Pos, Rot, Sketch, Circle, extrude, Rectangle  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402
from dkh_parts import (bx, cx, cy, cz, fuse, drill, slab, bead, bead_tri, rivet, pointing, piano_hinge, fan_120,  # noqa: E402
                       screw, frame)

TITLE = "DockHub"

# Top-level parameters (mm). Edit these, not the geometry below. The calculations read them.
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
    "plenum_t": 1.5,                 # plenum wall is folded 1.5 mm sheet
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
    # Site (R15, decided 2026-10-02: first pilot on private ground): cast pad and anchors
    "pad": (1400.0, 1100.0, 300.0),  # reinforced concrete pad, X by Y by depth, top flush with the ground, cabinet centred
    "anchor": (12.0, 100.0, 160.0),  # M12 stainless wedge anchor: diameter, embedment, overall length
    # Trial option (decided 2026-10-02): vermiculite-filled bay floor for the propagation trial
    "verm_tray": (20.0, 1.0, 2.0),   # tray height, stainless sheet thickness, fill level below the rim
    # Option B: rotary magazine (DKH-OPT-001)
    "turret_d": 420.0, "turret_r": 140.0, "turret_h": 380.0, "pocket": (100.0, 90.0, 3.0),
    "turret_y": 5.0, "disc_t": 6.0, "cradle_b": 120.0, "index_z": 600.0,
    # Option C: locker bank (DKH-OPT-001)
    "lockers": (3, 2), "locker_w": 290.0, "locker_h": 210.0,
}
P = PARAMS

OPTIONS = {"A": "Swap bays in a steel cabinet", "B": "Rotary magazine behind one hatch", "C": "Locker bank, charge in place"}
PRINCIPLES = {
    "A": "Four steel compartments each hold one SwapCell pack on its own charger; the rider returns a flat pack and "
         "lifts a charged one out by hand, and a fault is vented to a rear plenum.",
    "B": "Four pack pockets ride on a motor-indexed turret; one hatch presents the fullest pack to the rider, so no "
         "compartment with a charging pack is ever opened.",
    "C": "Six locked lockers charge the rider's own pack while they work and return it later; nothing is swapped and "
         "the station owns no packs.",
}
CHOSEN = "A"
OPTION_VIEWS = {k: {"el": 22, "az": -38, "scale": "person", "ground_z": 0} for k in OPTIONS}
ALLOWED_CONTACTS = [("split pin", "clevis pin")]

VERM_GAP = 3.0                       # trial tray ends this far in front of the cradle, mm
SOCKET_R = 14.0                      # radius of a 19 mm socket on an extension, for the anchor nut access check, mm

# exploded-view offsets by BOM line (mm), as the exploded view of DKH-PRC-001 Figure 3
EXPLODE = {1: (0, 0, 0), 2: (0, -1000, 0), 3: (0, -450, 0), 4: (0, -250, 1050), 5: (0, -520, -60), 6: (-800, 300, 750),
           7: (700, -300, 0), 8: (900, 0, -40), 9: (0, 500, 350), 10: (0, 900, 250), 11: (0, 0, 1900), 12: (0, 0, 1500),
           13: (1500, -450, -350), 14: (0, 0, -350), 15: (0, -1100, -150), 16: (0, 0, 0), 17: (0, 0, -300), 18: (0, 0, -300),
           19: (0, -450, 0)}


# ---------------------------------------------------------------------------- derived positions and helpers
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
    return Pos(0, p["panel_y"], p["panel_z"]) * Rot(-p["tilt_deg"], 0, 0)


def to_global(ly, lz, p=PARAMS):
    """Global (y, z) of a point at panel-local (ly, lz)."""
    a = math.radians(-p["tilt_deg"])
    return p["panel_y"] + ly * math.cos(a) - lz * math.sin(a), p["panel_z"] + ly * math.sin(a) + lz * math.cos(a)


def post_geometry(p=PARAMS):
    """Each canopy post: (x, y, z_bottom_of_post, z_top_at_axis, local y of the post axis on the cap plane)."""
    pt = p["panel"][2]
    lz_cap = -pt / 2 - p["rail_h"] - p["cap_t"]          # underside of the cap plate, panel-local
    a = math.radians(p["tilt_deg"])
    out = []
    for x in (-p["post_x"], p["post_x"]):
        for y in (-p["post_y"], p["post_y"]):
            ly = (y - p["panel_y"] + lz_cap * math.sin(-a)) / math.cos(-a)
            _, ztop = to_global(ly, lz_cap, p)
            out.append((x, y, p["roof_z"] + p["base_plate"][2], ztop, ly))
    return out


def derived(p=PARAMS):
    W, D, t = p["W"], p["D"], p["sheet_t"]
    return {
        "xi": W / 2 - t, "yf": -D / 2, "yb": D / 2, "yfi": -D / 2 + t, "ybi": D / 2 - t,
        "z0": p["plinth_h"], "z1": p["roof_z"], "flx": W / 2 - 2 * t, "notch_y": D / 2 - t - p["flange"],
        "deck_z": p["bay_z0"], "shelf_z": 380.0,
        "floor_bolts": [(-400, -225), (-150, -225), (150, -225), (400, -225), (20, 225), (180, 225), (-475, 0), (475, 0)],
        "anchors": [(sx * p["anchor_x"], sy * (D / 2 - p["anchor_inset"] / 2)) for sx in (-1, 1) for sy in (-1, 1)],
        "charger_x": [-345.0, -115.0, 115.0, 345.0],
        "post_bolts_y": (165.0, 235.0),
    }


# ---------------------------------------------------------------------------- the part collector
class Kit:
    """Collects part dicts and lets later steps drill holes into parts already added."""

    def __init__(self, chosen=True):
        self.parts, self.by = [], {}
        self.chosen = chosen             # only the chosen option (A) carries BOM line numbers

    def add(self, key, name, shape, material, kind="made", bom=None, group=None, color=None, explode=None):
        group = group or key
        ex = EXPLODE.get(bom, (0, 0, 0)) if explode is None else explode
        q = part(name, shape, material, kind=kind, bom=bom if self.chosen else None, group=group, color=color, explode=ex)
        self.parts.append(q)
        self.by.setdefault(key, []).append(q)
        return q

    def one(self, key):
        return self.by[key][0]

    def drill(self, key, cutters, which=0):
        q = self.by[key][which]
        q["shape"] = drill(q["shape"], cutters)

    def rivets(self, keys, pts, direction, grip, bom=16, group=None, name="4 mm blind rivet, galvanized"):
        """Blind rivets with head on the outer face at each point, pointing along 'direction'. Holes are drilled in
        every part named in keys (a key or (key, index))."""
        cutters = [pointing(Pos(0, 0, -(grip + 4) / 2 + 1.0) * Cylinder(2.1, grip + 4), pt, direction) for pt in pts]
        for k in keys:
            key, idx = (k if isinstance(k, tuple) else (k, 0))
            self.drill(key, cutters, idx)
        for pt in pts:
            self.add("rivets", name, rivet(pt, direction, grip), "zinc_plated", kind="fastener", bom=bom, group=group or "rivets",
                     explode=EXPLODE.get(bom, (0, 0, 0)))

    def bolt(self, d, grip, loc, key, bom, material="zinc_plated", label="", group=None, extra=None, dir_z=None):
        """Bolt, two washers and nut clamping a joint; the joint's top face at the origin of 'loc' (a Location or
        Pos*Rot); returns nothing, adds four fastener parts."""
        for nm, shp in cp.hex_bolt_set(d, grip, extra):
            self.add(key, nm + label, loc * shp, material, kind="fastener", bom=bom, group=group or key, explode=EXPLODE.get(bom, (0, 0, 0)))


def box_holes(r, z0, z1, pts):
    return [cz(r, z0, z1, x, y) for x, y in pts]


def L_angle(a, b, t, length, axis_dir="z"):
    """cp.angle moved so its heel is at the origin, legs along +X and +Y, extruded along +Z (kept for clarity)."""
    return cp.angle(a, b, t, length)


# ---------------------------------------------------------------------------- shared shell and site builders
def plinth_parts(K, p=P, bom=14, holes=True):
    """Welded 100 x 50 x 5 channel plinth, four mitred members with flanges inward, with anchor and body bolt holes."""
    d = derived(p)
    W, D = p["W"], p["D"]
    ch_d, ch_f, ch_t = p["channel"]
    zh = p["plinth_h"]
    holes_top, holes_bot = [], []
    if holes:
        for x, y in d["anchors"]:
            holes_bot.append(cz(7.0, -1, ch_t + 1, x, y))
            holes_top.append(cz(16.0, zh - ch_t - 1, zh + 1, x, y))
        for x, y in d["floor_bolts"]:
            holes_top.append(cz(5.5, zh - ch_t - 1, zh + 1, x, y))
    mit = lambda pts: extrude_poly(pts, zh + 2, -1)
    sides = {
        "front": ((-W / 2, -D / 2), (W / 2, -D / 2), (W / 2 - ch_f, -D / 2 + ch_f), (-W / 2 + ch_f, -D / 2 + ch_f)),
        "back": ((W / 2, D / 2), (-W / 2, D / 2), (-W / 2 + ch_f, D / 2 - ch_f), (W / 2 - ch_f, D / 2 - ch_f)),
        "left": ((-W / 2, D / 2), (-W / 2, -D / 2), (-W / 2 + ch_f, -D / 2 + ch_f), (-W / 2 + ch_f, D / 2 - ch_f)),
        "right": ((W / 2, -D / 2), (W / 2, D / 2), (W / 2 - ch_f, D / 2 - ch_f), (W / 2 - ch_f, -D / 2 + ch_f)),
    }
    for nm, quad in sides.items():
        horiz = nm in ("front", "back")
        if horiz:
            ys = -D / 2 if nm == "front" else D / 2 - ch_t
            web = bx(-W / 2, W / 2, ys, ys + ch_t, 0, zh)
            sg = 1 if nm == "front" else -1
            yi = (-D / 2 + ch_t) if nm == "front" else (D / 2 - ch_t)
            fl_y = (-D / 2, -D / 2 + ch_f) if nm == "front" else (D / 2 - ch_f, D / 2)
            fl = [bx(-W / 2, W / 2, fl_y[0], fl_y[1], 0, ch_t), bx(-W / 2, W / 2, fl_y[0], fl_y[1], zh - ch_t, zh)]
        else:
            xs = -W / 2 if nm == "left" else W / 2 - ch_t
            web = bx(xs, xs + ch_t, -D / 2, D / 2, 0, zh)
            fl_x = (-W / 2, -W / 2 + ch_f) if nm == "left" else (W / 2 - ch_f, W / 2)
            fl = [bx(fl_x[0], fl_x[1], -D / 2, D / 2, 0, ch_t), bx(fl_x[0], fl_x[1], -D / 2, D / 2, zh - ch_t, zh)]
        member = fuse([web] + fl) & mit(quad)
        member = drill(member, holes_top + holes_bot)
        K.add("plinth", f"Plinth channel, {nm} member, 100 x 50 x 5 mitred", member, "painted_steel", bom=bom, color="#6B7280")
    # mitre welds: bead on the inside web corner of each mitre, the full height of the web between the flanges
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        ox, oy = sx * (W / 2 - ch_t), sy * (D / 2 - ch_t)
        K.add("plinth_welds", "Mitre weld, plinth corner", bead((ox, oy, ch_t), (0, 0, 1), zh - 2 * ch_t, 5.0, (-sx, 0, 0), (0, -sy, 0)),
              "mild_steel", kind="weld", bom=bom, group="plinth", explode=EXPLODE.get(bom, (0, 0, 0)))


def extrude_poly(pts, h, z0=0.0):
    from build123d import Polygon
    a = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, list(pts[1:]) + [pts[0]]))
    pts = list(pts) if a > 0 else list(reversed(pts))
    return Pos(0, 0, z0) * extrude(Polygon(*pts, align=None), h)


def site_parts(K, p=P, bom_pad=18, bom_anchor=17):
    """Cast pad (top flush with the ground at z = 0) and the four M12 stainless wedge anchors with washer and nut."""
    d = derived(p)
    pL, pB, pH = p["pad"]
    ad, emb, alen = p["anchor"]
    ch_t = p["channel"][2]
    pad = bx(-pL / 2, pL / 2, -pB / 2, pB / 2, -pH, 0)
    cut = [cz(ad / 2, -emb, 1, x, y) for x, y in d["anchors"]]
    pad = break_edges(pad - Compound(cut), 3.0) if False else drill(pad, cut)
    K.add("pad", "Concrete pad (site)", pad, "concrete", bom=bom_pad, group="pad")
    for x, y in d["anchors"]:
        stud = Pos(x, y, 0) * Pos(0, 0, -emb) * cp.round_bar(ad, alen, 0.8)
        K.add("anchors", "M12 x 160 wedge anchor stud, A4 stainless", stud, "stainless", kind="bought", bom=bom_anchor)
        K.add("anchors", "M12 washer (ISO 7089), A4", Pos(x, y, ch_t) * cp.washer(12), "stainless", kind="fastener", bom=bom_anchor)
        K.add("anchors", "M12 tamper-resistant nut, A4", Pos(x, y, ch_t + 2.5) * cp.hex_nut(12), "stainless", kind="fastener", bom=bom_anchor)


def hole_pts_floor(p=P):
    return derived(p)["floor_bolts"]


def floor_bolt_sets(K, p=P, bom=16):
    d = derived(p)
    zh, t = p["plinth_h"], p["sheet_t"]
    for x, y in d["floor_bolts"]:
        K.bolt(10, t + p["channel"][2], Pos(x, y, zh + t), "floor_bolts", bom, extra=8.0)


def shell_panels(K, p, front_cutouts, front_holes=(), roof_extra_holes=(), floor_extra_holes=(), back_extra=(), bom=1):
    """Floor pan, back panel, two side panels, front panel and roof panel, as 1.5 mm galvanized sheet with folded
    flanges, powder coated. front_cutouts: [(x0, x1, z0, z1, r)] openings in the front panel."""
    d = derived(p)
    t, fl, rfl = p["sheet_t"], p["flange"], p["roof_flange"]
    xi, flx, ny = d["xi"], d["flx"], d["notch_y"]
    yf, yb, yfi, ybi = d["yf"], d["yb"], d["yfi"], d["ybi"]
    Z0, Z1, W = d["z0"], d["z1"], p["W"]
    col = "#E5E7EB"
    # floor pan: plate between the walls, 25 mm flanges up, corners notched
    floor = fuse([bx(-xi, xi, -ybi, ybi, Z0, Z0 + t), bx(-flx, flx, yfi, yfi + t, Z0 + t, Z0 + t + fl),
                  bx(-flx, flx, ybi - t, ybi, Z0 + t, Z0 + t + fl), bx(-xi, -flx, -ny, ny, Z0 + t, Z0 + t + fl),
                  bx(flx, xi, -ny, ny, Z0 + t, Z0 + t + fl)])
    cut = [cz(5.5, Z0 - 1, Z0 + t + 1, x, y) for x, y in d["floor_bolts"]] + [cz(12.5, Z0 - 1, Z0 + t + 1, 340, 120)]
    cut += [cz(20.0, Z0 - 1, Z0 + t + 1, x, y) for x, y in d["anchors"]] + list(floor_extra_holes)
    K.add("floor", "Floor pan, 1.5 mm galvanized, folded", drill(floor, cut), "painted_steel", bom=bom, color=col)
    back = fuse([bx(-W / 2, W / 2, ybi, yb, Z0, Z1), bx(-xi, -flx, ny, ybi, Z0 + t, Z1 - t), bx(flx, xi, ny, ybi, Z0 + t, Z1 - t)])
    K.add("back", "Back panel, 1.5 mm galvanized, folded", drill(back, list(back_extra)), "painted_steel", bom=bom, color=col)
    K.add("side_l", "Left side panel, 1.5 mm galvanized", bx(-W / 2, -xi, yfi, ybi, Z0, Z1), "painted_steel", bom=bom, color=col)
    K.add("side_r", "Right side panel, 1.5 mm galvanized", bx(xi, W / 2, yfi, ybi, Z0, Z1), "painted_steel", bom=bom, color=col)
    for k in ("side_l", "side_r"):
        K.one(k)["shape"] = break_edges(K.one(k)["shape"], 0.4)
    front = fuse([bx(-W / 2, W / 2, yf, yfi, Z0, Z1), bx(-xi, -flx, yfi, -ny, Z0 + t, Z1 - t), bx(flx, xi, yfi, -ny, Z0 + t, Z1 - t)])
    front = drill(front, [cy_rect(a0, a1, z0, z1, r, yf - 1, yfi + 1) for a0, a1, z0, z1, r in front_cutouts] + list(front_holes))
    K.add("front", "Front panel, 1.5 mm galvanized, laser cut", front, "painted_steel", bom=bom, color=col)
    roof = fuse([bx(-xi, xi, -ybi, ybi, Z1 - t, Z1), bx(-flx, flx, yfi, yfi + t, Z1 - t - rfl, Z1 - t),
                 bx(-flx, flx, ybi - t, ybi, Z1 - t - rfl, Z1 - t), bx(-xi, -flx, -ny, ny, Z1 - t - rfl, Z1 - t),
                 bx(flx, xi, -ny, ny, Z1 - t - rfl, Z1 - t)])
    K.add("roof", "Roof panel, 1.5 mm galvanized, folded", drill(roof, list(roof_extra_holes)), "painted_steel", bom=bom, color=col)


def cy_rect(a0, a1, z0, z1, r, y0, y1):
    """A through cutter for a rounded rectangle opening in a plate normal to Y, from y0 to y1."""
    from build123d import RectangleRounded, Location, Plane
    w, h = a1 - a0, z1 - z0
    sk = Sketch() + RectangleRounded(w, h, max(0.05, min(r, min(w, h) / 2 - 0.01)))
    s = extrude(sk, y1 - y0)                       # local z from 0 to y1 - y0
    return Location(Plane(origin=((a0 + a1) / 2, y1, (z0 + z1) / 2), x_dir=(1, 0, 0), z_dir=(0, -1, 0))) * s


def shell_rivets(K, p, front_zs=(200, 400, 600, 800, 1000, 1200, 1400), bom=16):
    """Blind rivets along the main shell seams: sides to the front and back flanges, floor and roof flanges."""
    d = derived(p)
    xi, t = d["xi"], p["sheet_t"]
    W = p["W"]
    Z0, Z1 = d["z0"], d["z1"]
    for sx in (-1, 1):
        sk = "side_l" if sx < 0 else "side_r"
        pts_f = [(sx * W / 2, -236.0, z) for z in front_zs]
        pts_b = [(sx * W / 2, 236.0, z) for z in front_zs]
        K.rivets([sk, "front"], pts_f, (sx, 0, 0), 2 * t)
        K.rivets([sk, "back"], pts_b, (sx, 0, 0), 2 * t)
        K.rivets([sk, "floor"], [(sx * W / 2, y, Z0 + 14.0) for y in (-150.0, 0.0, 150.0)], (sx, 0, 0), 2 * t)
        K.rivets([sk, "roof"], [(sx * W / 2, y, Z1 - 20.0) for y in (-150.0, 0.0, 150.0)], (sx, 0, 0), 2 * t)
    xs = (-400.0, -200.0, 0.0, 200.0, 400.0)
    K.rivets(["front", "floor"], [(x, -250.0, Z0 + 14.0) for x in xs], (0, -1, 0), 2 * t)
    K.rivets(["back", "floor"], [(x, 250.0, Z0 + 14.0) for x in xs], (0, 1, 0), 2 * t)
    K.rivets(["front", "roof"], [(x, -250.0, Z1 - 20.0) for x in (-380.0, -190.0, 0.0, 190.0, 380.0)], (0, -1, 0), 2 * t)
    K.rivets(["back", "roof"], [(x, 250.0, Z1 - 20.0) for x in (-380.0, -190.0, 0.0, 190.0, 380.0)], (0, 1, 0), 2 * t)


def make_box_part(K, key, name, x0, x1, y0, y1, z0, z1, material, bom, r=3.0, color=None, kind="bought", group=None):
    s = break_edges(bx(x0, x1, y0, y1, z0, z1), r)
    return K.add(key, name, s, material, kind=kind, bom=bom, color=color, group=group)


# ---------------------------------------------------------------------------- option A
def pack_part(K, xc, p, n, bom=4, key="packs"):
    """SwapCell v0.3 reference pack standing connector down at bay centre xc (one solid, envelope as the interface)."""
    z0 = pack_z0(p)
    z1 = z0 + p["pack_l"]
    hw, hd = p["pack_w"] / 2, p["pack_d"] / 2
    body = break_edges(bx(xc - hw, xc + hw, -hd, hd, z0, z1), 4.0)
    yc = p["plug_offset"]
    plug = bx(xc - p["plug_w"] / 2, xc + p["plug_w"] / 2, yc - p["plug_d"] / 2, yc + p["plug_d"] / 2, z0 - p["plug_h"], z0)
    hh = p["handle_h"]
    handle = bx(xc - p["handle_w"] / 2, xc + p["handle_w"] / 2, -p["handle_d"] / 2, p["handle_d"] / 2, z1 - 1, z1 + hh) \
        - bx(xc - p["handle_w"] / 2 + 11, xc + p["handle_w"] / 2 - 11, -p["handle_d"], p["handle_d"], z1 - 2, z1 + 25)
    zl = z1 - p["latch_from_top"]
    pawl = bx(xc - p["latch_w"] / 2, xc + p["latch_w"] / 2, hd - 1, hd + p["latch_proud"], zl - p["latch_h"] / 2, zl + p["latch_h"] / 2)
    s = fuse([body, break_edges(plug, 0.8), break_edges(handle, 1.5), break_edges(pawl, 1.0)])
    return K.add(key, f"SwapCell v0.3 pack {n} (reference)", s, "matte_black", kind="bought", bom=bom, color="#D4A017")


def _boxes(K, p, mppt=True):
    """Dock controller, MPPT charge controller and grid input enclosure screwed to the back panel."""
    d = derived(p)
    t = p["sheet_t"]
    yb, ybi = d["yb"], d["ybi"]
    ybx = {"controller": (-450, -230, 150, 340, ybi - 100, "Dock controller enclosure (ESP32, CAN, LTE-M)", "matte_black", 6, "#15803D"),
           "mppt": (-190, -40, 150, 330, ybi - 70, "MPPT solar charge controller", "aluminium", 13, "#B45309"),
           "grid": (230, 450, 150, 350, ybi - 92, "Grid input enclosure, DIN, with RCBO and isolator", "matte_black", 8, "#991B1B")}
    if not mppt:
        ybx.pop("mppt")
    for key, (xa, xb, za, zb, y0, nm, mat, bom, col) in ybx.items():
        pts = [(xa + 15, za + 15), (xb - 15, za + 15), (xa + 15, zb - 15), (xb - 15, zb - 15)]
        body = break_edges(bx(xa, xb, y0, ybi, za, zb), 4.0)
        body = drill(body, [cy(2.6, ybi - 8, ybi + 1, x, z) for x, z in pts])
        K.add(key, nm, body, mat, kind="bought", bom=bom, color=col)
        K.drill("back", [cy(2.6, ybi - 1, yb + 1, x, z) for x, z in pts])
        for x, z in pts:
            K.add("box_screws", "M5 pan head screw, zinc", pointing(screw(5, t + 8.0, 9.0, 3.0), (x, yb, z), (0, 1, 0)), "zinc_plated",
                  kind="fastener", bom=16, explode=EXPLODE[16])


def _a1(fitted=None, p=P):
    K = Kit()
    d = derived(p)
    fitted = p["bays_fitted"] if fitted is None else fitted
    W, D, t = p["W"], p["D"], p["sheet_t"]
    xi, flx, ny = d["xi"], d["flx"], d["notch_y"]
    yf, yb, yfi, ybi = d["yf"], d["yb"], d["yfi"], d["ybi"]
    Z0, Z1 = d["z0"], d["z1"]
    fl, rfl = p["flange"], p["roof_flange"]
    xs = bay_x(p)
    fit, blank = xs[:fitted], xs[fitted:]
    o0, o1 = p["open_z"]
    HW = p["bay_open_w"] / 2
    so_w, so_0, so_1 = p["service_open"]
    LY1, pt_ = p["liner_y1"], p["plenum_t"]
    dz = d["deck_z"]
    pz0 = pack_z0(p)
    hw, hd = p["pack_w"] / 2, p["pack_d"] / 2
    lw, lt = p["liner_w"] / 2, p["liner_top"]
    dw, dh, dt = p["door"]
    gw, gt = p["gasket"]
    ydb = yf - gt
    dz0 = (o0 + o1) / 2 - dh / 2
    sz = d["shelf_z"]
    bw, bt = p["beam"]

    # ------------------------------------------------------------ 14 plinth and 1 shell
    plinth_parts(K, p)
    openings = [(xc - HW, xc + HW, o0, o1, 4.0) for xc in xs] + [(-so_w, so_w, so_0, so_1, 6.0), (340.0, 460.0, 880.0, 1180.0, 4.0)]
    fan_holes = [cz(p["fan_hole_r"], Z1 - t - 1, Z1 + 1, sx * p["fan_x"], p["fan_y"]) for sx in (-1, 1)]
    post_holes = [cz(5.5, Z1 - t - 1, Z1 + 1, sx * p["post_x"], sy * yy) for sx in (-1, 1) for sy in (-1, 1) for yy in d["post_bolts_y"]]
    shell_panels(K, p, openings, roof_extra_holes=fan_holes + post_holes + [cz(12.5, Z1 - t - 1, Z1 + 1, -200, 60)])
    shell_rivets(K, p)
    floor_bolt_sets(K, p)

    # ------------------------------------------------------------ deck, shelf, plenum wall
    deck = fuse([bx(-flx, flx, yfi, LY1, dz - t, dz), bx(-flx, flx, yfi, yfi + t, dz - t - fl, dz - t),
                 bx(-flx, flx, LY1 - t, LY1, dz - t - fl, dz - t), bx(-xi, -flx, -ny, LY1, dz - t - fl, dz),
                 bx(flx, xi, -ny, LY1, dz - t - fl, dz)])
    bay_cut = []
    for xc in fit:
        bay_cut.append(bx(xc - 20, xc + 20, p["plug_offset"] - 15, p["plug_offset"] + 15, dz - t - 1, dz + 1))
        bay_cut += [cz(2.75, dz - t - 1, dz + 1, xc + sx * 60, sy * 60) for sx in (-1, 1) for sy in (-1, 1)]
    K.add("deck", "Bay deck, 1.5 mm galvanized, folded", drill(deck, bay_cut), "painted_steel", bom=1, color="#9CA3AF")
    shelf = fuse([bx(-flx, flx, -60, 220, sz - t, sz), bx(-flx, flx, -60, -60 + t, sz - t - fl, sz - t),
                  bx(-flx, flx, 220 - t, 220, sz - t - fl, sz - t), bx(-xi, -flx, -60, 220, sz - t - fl, sz),
                  bx(flx, xi, -60, 220, sz - t - fl, sz)])
    shelf_cut = [cz(3.0, sz - t - 1, sz + 1, x + ex, ey) for x in d["charger_x"][:fitted] for ex in (-60, 60) for ey in (-26, 186)]
    K.add("shelf", "Charger shelf, 1.5 mm galvanized, folded", drill(shelf, shelf_cut), "painted_steel", bom=1, color="#9CA3AF")
    px0 = p["post_x"] - bw / 2 - 2
    plenum = fuse([bx(-flx, flx, LY1, LY1 + pt_, dz - t - fl, Z1 - 2 * t), bx(-px0, px0, LY1 - 20, LY1 + pt_, Z1 - 2 * t, Z1 - t),
                   bx(-xi, -flx, LY1 + pt_, LY1 + pt_ + 20, dz - t - fl, 1455), bx(flx, xi, LY1 + pt_, LY1 + pt_ + 20, dz - t - fl, 1455)])
    pc = [bx(sx * px0 - (0 if sx > 0 else bw + 4), sx * px0 + (bw + 4 if sx > 0 else 0), LY1 - 21, LY1 + pt_ + 1, Z1 - t - bw - 2, Z1)
          for sx in (-1, 1)]
    pc += [bx(xc - 30, xc + 30, LY1 - 1, LY1 + pt_ + 1, 1140, 1200) for xc in fit]
    K.add("plenum", "Plenum wall, 1.5 mm galvanized, folded", drill(plenum, pc), "painted_steel", bom=10, color="#4B5563")
    for sx in (-1, 1):
        sk = "side_l" if sx < 0 else "side_r"
        K.rivets([sk, "deck"], [(sx * W / 2, y, dz - 13.0) for y in (-150.0, 0.0)], (sx, 0, 0), 2 * t)
        K.rivets([sk, "shelf"], [(sx * W / 2, y, sz - 13.0) for y in (-40.0, 40.0, 120.0, 200.0)], (sx, 0, 0), 2 * t)
        K.rivets([sk, "plenum"], [(sx * W / 2, LY1 + pt_ + 10.0, z) for z in (700.0, 900.0, 1100.0, 1300.0, 1440.0)], (sx, 0, 0), 2 * t)
    K.rivets(["front", "deck"], [(x, -250.0, dz - 13.0) for x in (-400.0, -200.0, 0.0, 200.0, 400.0)], (0, -1, 0), 2 * t)

    # ------------------------------------------------------------ 6, 13, 8 boxes on the back panel; 5 chargers
    _boxes(K, p)
    for i, x in enumerate(d["charger_x"][:fitted]):
        body = fuse([bx(x - 80, x + 80, -20, 180, sz, sz + 70)] + [bx(x - 72 + 18 * k - 1.5, x - 72 + 18 * k + 1.5, -18, 178, sz + 70, sz + 78) for k in range(9)]
                    + [bx(x - 70, x - 50, -32, -20, sz, sz + 4), bx(x + 50, x + 70, -32, -20, sz, sz + 4),
                       bx(x - 70, x - 50, 180, 192, sz, sz + 4), bx(x + 50, x + 70, 180, 192, sz, sz + 4)])
        body = drill(break_edges(body, 1.0), [cz(2.9, sz - 1, sz + 5, x + ex, ey) for ex in (-60, 60) for ey in (-26, 186)])
        K.add("chargers", f"Charger {i + 1}, 54.6 V 5 A, with heat sink", body, "aluminium", kind="bought", bom=5, color="#C2410C")
        for ex in (-60, 60):
            for ey in (-26, 186):
                K.bolt(5, t + 4, Pos(x + ex, ey, sz + 4), "charger_screws", 16, extra=3.0)

    # ------------------------------------------------------------ bays: liner, cradle, receptacle, catch, lock, pack
    cz0 = dz + t
    cw = p["cradle_w"] / 2
    yc = p["plug_offset"]
    zl = pz0 + p["pack_l"] - p["latch_from_top"]
    yb_ = hd + p["latch_proud"] + 1
    g = p["guide_clear"]
    lz0, lz1 = p["lock_z"]
    zlock = 960.0
    for i, xc in enumerate(fit):
        n = i + 1
        ln = bx(xc - lw, xc + lw, yfi, LY1, dz, lt) - bx(xc - lw + t, xc + lw - t, yfi - 1, LY1 - t, dz + t, lt - t)
        ln = ln + bx(xc - lw, xc + lw, yfi, yfi + t, lt, lt + 15)
        lc = [bx(xc - 30, xc + 30, LY1 - t - 1, LY1 + 1, 1140, 1200), bx(xc - 20, xc + 20, yc - 15, yc + 15, dz - 1, dz + t + 1)]
        lc += [cz(2.75, dz - 1, dz + t + 1, xc + sx * 60, sy * 60) for sx in (-1, 1) for sy in (-1, 1)]
        K.add("liners", f"Bay {n} liner, 1.5 mm galvanized, folded box", drill(ln, lc), "painted_steel", bom=3, color="#9CA3AF")
        K.rivets(["front", ("liners", n - 1)], [(xc - 60.0, yf, lt + 8.0), (xc + 60.0, yf, lt + 8.0)], (0, -1, 0), 2 * t)
        cr = bx(xc - cw, xc + cw, -cw, cw, cz0, pz0)
        cr = cr - bx(xc - p["plug_w"] / 2 - 1, xc + p["plug_w"] / 2 + 1, yc - p["plug_d"] / 2 - 1, yc + p["plug_d"] / 2 + 1, pz0 - p["plug_h"] - 1.5, pz0 + 1)
        cr = cr - bx(xc - p["plug_w"] / 2 - 8, xc + p["plug_w"] / 2 + 8, yc - p["plug_d"] / 2 - 8, yc + p["plug_d"] / 2 + 8, cz0 - 1, pz0 - p["plug_h"] - 1.5)
        cr = cr - bx(xc - 31, xc + 31, yb_ + 8 - 0.5, yb_ + 11.5, pz0 - 10, pz0 + 1)
        cr = cr + bx(xc - hw - g - 5, xc - hw - g, -45, 45, pz0, pz0 + p["guide_h"]) + bx(xc + hw + g, xc + hw + g + 5, -45, 45, pz0, pz0 + p["guide_h"])
        scr = [(xc + sx * 60, sy * 60) for sx in (-1, 1) for sy in (-1, 1)]
        cr = drill(cr, [cz(2.75, cz0 - 1, pz0 + 1, x, y) for x, y in scr] + [cz(5.0, pz0 - 5, pz0 + 1, x, y) for x, y in scr])
        K.add("cradles", f"Bay {n} cradle with guide faces (printed)", cr, "hdpe_black", bom=3, color="#0E7490")
        for x, y in scr:
            K.bolt(5, (pz0 - 5 - cz0) + 2 * t, Pos(x, y, pz0 - 5), "cradle_screws", 16, extra=3.0)
        rec = bx(xc - 36, xc + 36, yc - 25, yc + 25, cz0, pz0 - p["plug_h"] - 1.5) - bx(xc - 28, xc + 28, yc - 17, yc + 17, pz0 - p["plug_h"] - 4.5, pz0)
        rec = rec + fuse([cz(1.2, pz0 - p["plug_h"] - 4.5, pz0 - p["plug_h"] - 1.5, xc - 20 + 8 * k, yc) for k in range(6)])
        K.add("receptacles", f"Bay {n} SwapCell v0.3 receptacle with coding resistor", rec, "hdpe_black", kind="bought", bom=3, color="#1F2937")
        yp0, yp1 = yb_ + 8, yb_ + 11
        ztop = zl + 30
        cat = fuse([bx(xc - 30, xc + 30, yp0, yp1, pz0 - 10, ztop), bx(xc - 30, xc + 30, yp0, LY1 - t, ztop - 3, ztop),
                    bx(xc - 30, xc + 30, LY1 - t - 3, LY1 - t, ztop - 43, ztop - 3), bx(xc - 25, xc + 25, yb_, yp0, zl + p["latch_h"] / 2 + 1, zl + p["latch_h"] / 2 + 9)])
        K.add("catches", f"Bay {n} catch bracket, 3 mm steel", break_edges(cat, 0.5), "painted_steel", bom=3, color="#7C3AED")
        lock = break_edges(bx(xc + lw - t - 30, xc + lw - t, yfi + 2.5, yfi + 32.5, lz0, lz1), 1.5)
        lock = drill(lock, [cx(2.8, xc + lw - t - 31, xc + lw - t + 1, yfi + 8.0, zlock)]
                     + [cx(2.0, xc + lw - t - 8, xc + lw - t + 1, yy, zz) for yy in (yfi + 6.0, yfi + 29.0) for zz in (lz0 + 6, lz1 - 6)])
        K.add("locks", f"Bay {n} solenoid lock, 12 V fail-secure", lock, "matte_black", kind="bought", bom=2, color="#374151")
        K.add("locks", f"Bay {n} lock plunger", cx(2.75, xc + 49.0, xc + lw - t - 30, yfi + 8.0, zlock), "stainless", kind="bought", bom=2)
        K.drill("liners", [cx(2.1, xc + lw - 2, xc + lw + 1, yy, zz) for yy in (yfi + 6.0, yfi + 29.0) for zz in (lz0 + 6, lz1 - 6)], n - 1)
        for yy in (yfi + 6.0, yfi + 29.0):
            for zz in (lz0 + 6, lz1 - 6):
                K.add("lock_screws", "M4 pan head screw, zinc", pointing(screw(4, t + 6.0, 7.5, 2.6), (xc + lw, yy, zz), (1, 0, 0)), "zinc_plated",
                      kind="fastener", bom=16, explode=EXPLODE[16])
        if i < fitted - 1:
            pack_part(K, xc, p, n)
    return K, d, fit, blank, xs


def _a2(K, p, fitted, fit, blank, xs):
    """Doors, hinges, blank plates, access panel, service door, fire unit, fans, vent hood."""
    d = derived(p)
    t = p["sheet_t"]
    yf, yfi, ybi, yb = d["yf"], d["yfi"], d["ybi"], d["yb"]
    Z1 = d["z1"]
    o0, o1 = p["open_z"]
    HW = p["bay_open_w"] / 2
    so_w, so_0, so_1 = p["service_open"]
    dw, dh, dt = p["door"]
    gw, gt = p["gasket"]
    ydb = yf - gt
    dz0 = (o0 + o1) / 2 - dh / 2
    hz0, hz1 = p["door_handle_z"]
    hdl_pts = lambda xc: [(xc + 57.5, hz0 + 2.0), (xc + 57.5, hz1 - 2.0)]
    for i, xc in enumerate(fit):
        n = i + 1
        xl = xc - dw / 2
        door = slab("y", ydb - dt, ydb, xl, xl + dw, dz0, dz0 + dh, r=8.0, edge=0.5)
        door = drill(door, [cy(2.1, ydb - dt - 1, ydb + 1, x, z) for x, z in hdl_pts(xc)]
                     + [cy(2.1, ydb - dt - 1, ydb + 1, xc + 36.0, z) for z in (955.0, 965.0)])
        K.add("doors", f"Bay {n} door, 2 mm steel", door, "painted_steel", bom=2, color="#0F766E")
        gk = bx(xc - HW - 1 - gw, xc + HW + 1 + gw, ydb, yf, o0 - 1 - gw, o1 + 1 + gw) - bx(xc - HW - 1, xc + HW + 1, ydb - 1, yf + 1, o0 - 1, o1 + 1)
        K.add("gaskets", f"Bay {n} door gasket, EPDM 7 x 3", break_edges(gk, 0.6), "epdm", kind="bought", bom=2)
        hbar = fuse([cz(6.0, hz0 + 4.0, hz1 - 4.0, xc + 57.5, ydb - dt - 16.0)] + [cy(4.0, ydb - dt - 16.0, ydb - dt, x, z) for x, z in hdl_pts(xc)])
        hbar = drill(break_edges(hbar, 1.0), [cy(2.0, ydb - dt - 8.0, ydb - dt + 0.5, x, z) for x, z in hdl_pts(xc)])
        K.add("handles", f"Bay {n} pull handle, stainless", hbar, "stainless", kind="bought", bom=2)
        for x, z in hdl_pts(xc):
            K.add("handle_screws", "M4 button screw, A2", pointing(screw(4, 10.0, 7.0, 2.2), (x, ydb, z), (0, 1, 0)), "stainless",
                  kind="fastener", bom=2)
        tg = fuse([bx(xc + 30, xc + 54, ydb, ydb + 4, 950, 970), bx(xc + 50, xc + 54, ydb, yfi + 16.5, 950, 970)])
        tg = drill(tg, [cx(3.0, xc + 49, xc + 55, yfi + 8.0, 960.0)] + [cy(2.1, ydb - 1, ydb + 5, xc + 36.0, z) for z in (955.0, 965.0)])
        K.add("tongues", f"Bay {n} lock tongue, 4 mm angle", break_edges(tg, 0.4), "painted_steel", bom=2, color="#9CA3AF")
        for z in (955.0, 965.0):
            K.add("rivets", "4 mm blind rivet, galvanized", rivet((xc + 36.0, ydb - dt, z), (0, -1, 0), dt + 4.0), "zinc_plated", kind="fastener", bom=2,
                  group="rivets", explode=EXPLODE[2])
        hx_, hy_ = xl - 3.5, yf - 3.5
        body, pin = piano_hinge(xl - 18, xl + 24, yf - t, t, hx_, hy_, o0 + 15, o1 - 15, 0, 0, ydb - dt - t)
        body = drill(body, [cy(2.1, yf - t - 1, yf + 1, xl - 12.0, o0 + 40.0 + k * 100.0) for k in range(5)]
                     + [cy(2.1, ydb - dt - t - 1, ydb + 1, xl + 14.0, o0 + 40.0 + k * 100.0) for k in range(5)])
        K.add("hinges", f"Bay {n} piano hinge, 480 mm, stainless", body, "stainless", kind="bought", bom=2)
        K.add("hinges", f"Bay {n} hinge pin", pin, "stainless", kind="bought", bom=2)
        zr = [o0 + 40.0 + k * 100.0 for k in range(5)]
        for z in zr:
            K.add("rivets", "4 mm blind rivet, stainless", rivet((xl - 12.0, yf - t, z), (0, -1, 0), 2 * t), "stainless", kind="fastener", bom=2,
                  group="rivets", explode=EXPLODE[2])
            K.add("rivets", "4 mm blind rivet, stainless", rivet((xl + 14.0, ydb - dt - t, z), (0, -1, 0), t + dt), "stainless", kind="fastener", bom=2,
                  group="rivets", explode=EXPLODE[2])
        K.drill("front", [cy(2.1, yf - 1, yfi + 1, xl - 12.0, z) for z in zr])
        K.drill("doors", [cy(2.1, ydb - dt - 1, ydb + 1, xl + 14.0, z) for z in zr], i)
    # blank plates over unfitted bays on four M5 security screws
    for xc in blank:
        xl = xc - dw / 2
        pts = [(xc + sx * 80.0, z) for sx in (-1, 1) for z in (dz0 + 30.0, dz0 + dh - 30.0)]
        plate = slab("y", yf - 2, yf, xl, xl + dw, dz0, dz0 + dh, r=8.0, edge=0.5, holes=[])
        plate = drill(plate, [cy(2.7, yf - 3, yf + 1, x, z) for x, z in pts])
        K.add("blanks", "Blank plate, 2 mm steel", plate, "painted_steel", bom=1, color="#D1D5DB")
        K.drill("front", [cy(2.6, yf - 1, yfi + 1, x, z) for x, z in pts])
        for x, z in pts:
            K.add("blank_screws", "M5 security screw, A2", pointing(screw(5, 2 + t + 4.0, 9.5, 3.0), (x, yf - 2, z), (0, -1, 0)), "stainless",
                  kind="fastener", bom=1)

    _access(K, p)
    _service(K, p)
    _fire(K, p)
    _fans(K, p)
    _hood(K, p, True)


def _access(K, p):
    """Access panel: bezel, display and NFC reader behind glass, four security screws."""
    d = derived(p)
    t = p["sheet_t"]
    yf, yfi, ybi, yb = d["yf"], d["yfi"], d["ybi"], d["yb"]
    Z1 = d["z1"]
    o0, o1 = p["open_z"]
    dw, dh, dt = p["door"]
    gw, gt = p["gasket"]
    ydb = yf - gt
    so_w, so_0, so_1 = p["service_open"]
    hz0, hz1 = p["door_handle_z"]
    xs = bay_x(p)
    ax0, ax1 = p["access_x"]
    az0, az1 = p["access_z"]
    win_d = (345.0, 455.0, 1060.0, 1170.0)
    win_r = (355.0, 445.0, 900.0, 990.0)
    scr = [(320.0, 862.0), (480.0, 862.0), (320.0, 1198.0), (480.0, 1198.0)]
    bez = slab("y", yf - 4, yf, ax0, ax1, az0, az1, r=10.0, edge=0.8,
               holes=[(x, z, 4.2) for x, z in scr], cutouts=[(win_d[0], win_d[1], win_d[2], win_d[3], 3.0), (win_r[0], win_r[1], win_r[2], win_r[3], 3.0)])
    K.add("access", "Access panel bezel, 4 mm steel", bez, "painted_steel", bom=7, color="#1F2937")
    K.add("access", "Display glass", slab("y", yf - 4, yf, win_d[0], win_d[1], win_d[2], win_d[3], r=3.0, edge=0), "glass", kind="bought", bom=7, color="#0E1216")
    K.add("access", "Display module, 5 in", break_edges(bx(346, 454, yf, yf + 12, 1050, 1178), 1.5), "matte_black", kind="bought", bom=7)
    K.add("access", "NFC reader face", slab("y", yf - 4, yf, win_r[0], win_r[1], win_r[2], win_r[3], r=3.0, edge=0), "polycarbonate", kind="bought", bom=7, color="#CDD1D6")
    K.add("access", "NFC reader board", break_edges(bx(358, 442, yf, yf + 10, 903, 987), 1.0), "matte_black", kind="bought", bom=7)
    K.drill("front", [cy(2.1, yf - 1, yfi + 1, x, z) for x, z in scr])
    for x, z in scr:
        K.add("access_screws", "M4 security screw, A2", pointing(screw(4, 4 + t + 2.0, 8.0, 2.6), (x, yf - 4, z), (0, -1, 0)), "stainless",
              kind="fastener", bom=7)


def _service(K, p):
    """Service door on a piano hinge with gasket, cam lock and filter pad."""
    d = derived(p)
    t = p["sheet_t"]
    yf, yfi, ybi, yb = d["yf"], d["yfi"], d["ybi"], d["yb"]
    Z1 = d["z1"]
    o0, o1 = p["open_z"]
    dw, dh, dt = p["door"]
    gw, gt = p["gasket"]
    ydb = yf - gt
    so_w, so_0, so_1 = p["service_open"]
    hz0, hz1 = p["door_handle_z"]
    xs = bay_x(p)
    sw = so_w + 10
    sd = slab("y", ydb - dt, ydb, -sw, sw, so_0 - 10, so_1 + 10, r=8.0, edge=0.5, holes=[(420.0, 400.0, 19.0)],
              cutouts=[(-p["intake"][0], p["intake"][0], p["intake"][1], p["intake"][2], 4.0)])
    sd = drill(sd, [cy(2.1, ydb - dt - 1, ydb + 1, x, z) for x, z in ((-210.0, 160.0), (210.0, 160.0), (-210.0, 260.0), (210.0, 260.0))])
    K.add("service", "Service door, 2 mm steel", sd, "painted_steel", bom=15, color="#E5E7EB")
    sg = bx(-so_w - 1 - gw, so_w + 1 + gw, ydb, yf, so_0 - 1 - gw, so_1 + 1 + gw) - bx(-so_w - 1, so_w + 1, ydb - 1, yf + 1, so_0 - 1, so_1 + 1)
    K.add("service_gasket", "Service door gasket, EPDM 7 x 3", break_edges(sg, 0.6), "epdm", kind="bought", bom=15)
    hx_, hy_ = -sw - 3.5, yf - 3.5
    zs = [z for z in (so_0 + 50.0 + k * 100.0 for k in range(5)) if z <= so_1 - 25.0]   # rivets stay on the hinge (a shortened door has four)
    body, pin = piano_hinge(-sw - 18, -sw + 24, yf - t, t, hx_, hy_, so_0 + 20, so_1 - 20, 0, 0, ydb - dt - t)
    body = drill(body, [cy(2.1, yf - t - 1, yf + 1, -sw - 12.0, z) for z in zs] + [cy(2.1, ydb - dt - t - 1, ydb + 1, -sw + 14.0, z) for z in zs])
    K.add("service_hinge", "Service door piano hinge, 460 mm, stainless", body, "stainless", kind="bought", bom=15)
    K.add("service_hinge", "Service door hinge pin", pin, "stainless", kind="bought", bom=15)
    K.drill("front", [cy(2.1, yf - 1, yfi + 1, -sw - 12.0, z) for z in zs])
    K.drill("service", [cy(2.1, ydb - dt - 1, ydb + 1, -sw + 14.0, z) for z in zs])
    for z in zs:
        K.add("rivets", "4 mm blind rivet, stainless", rivet((-sw - 12.0, yf - t, z), (0, -1, 0), 2 * t), "stainless", kind="fastener", bom=15,
              group="rivets", explode=EXPLODE[15])
        K.add("rivets", "4 mm blind rivet, stainless", rivet((-sw + 14.0, ydb - dt - t, z), (0, -1, 0), t + dt), "stainless", kind="fastener", bom=15,
              group="rivets", explode=EXPLODE[15])
    cam = fuse([cy(12.0, ydb - dt - 6.0, ydb - dt, 420.0, 400.0), cy(9.0, ydb - dt, yfi + 3.0, 420.0, 400.0), bx(410, 470, yfi + 0.5, yfi + 3.5, 390, 410)])
    K.add("cam_lock", "Cam lock, 19 mm, with cam", break_edges(cam, 0.6), "stainless", kind="bought", bom=15)
    frame = slab("y", ydb, ydb + 1.5, -215.0, 215.0, 155.0, 265.0, r=3.0, edge=0.3, cutouts=[(-195.0, 195.0, 175.0, 245.0, 3.0)],
                 holes=[(x, z, 4.2) for x, z in ((-210.0, 160.0), (210.0, 160.0), (-210.0, 260.0), (210.0, 260.0))])
    K.add("filter", "Filter clip frame, 1.5 mm sheet", frame, "painted_steel", bom=10, color="#9CA3AF")
    K.add("filter", "Intake filter pad, 410 x 90 x 10", break_edges(bx(-205, 205, ydb + 1.5, ydb + 11.5, 165, 255), 1.0), "canvas", kind="bought", bom=10,
          color="#FDE68A")
    for x, z in ((-210.0, 160.0), (210.0, 160.0), (-210.0, 260.0), (210.0, 260.0)):
        K.add("rivets", "4 mm blind rivet, galvanized", rivet((x, ydb - dt, z), (0, -1, 0), dt + 1.5), "zinc_plated", kind="fastener", bom=10,
              group="rivets", explode=EXPLODE[10])


def _fire(K, p):
    """Aerosol suppression unit on two straps, and the heat and smoke detector."""
    d = derived(p)
    t = p["sheet_t"]
    yf, yfi, ybi, yb = d["yf"], d["yfi"], d["ybi"], d["yb"]
    Z1 = d["z1"]
    fyc = ybi - 46.0
    fire = break_edges(Pos(-60, fyc, 1420) * Rot(0, 90, 0) * Cylinder(38, 420), 3.0)
    K.add("fire", "Condensed-aerosol suppression unit, 76 x 420", fire, "safety_red", kind="bought", bom=9)
    for sxx in (-210, 90):
        ring = Pos(sxx, fyc, 1420) * Rot(0, 90, 0) * (Cylinder(40, 20) - Cylinder(38, 22))
        brk = bx(sxx - 10, sxx + 10, fyc + 40, ybi, 1400, 1440)
        sb = drill(fuse([ring, brk]), [cy(2.5, ybi - 7, ybi + 1, sxx, z) for z in (1410.0, 1430.0)])
        K.add("fire_straps", "Strap and bracket, 2 mm stainless", sb, "stainless", kind="bought", bom=9)
        K.drill("back", [cy(2.6, ybi - 1, yb + 1, sxx, z) for z in (1410.0, 1430.0)])
        for z in (1410.0, 1430.0):
            K.add("fire_screws", "M5 pan head screw, zinc", pointing(screw(5, t + 4.0, 9.0, 3.0), (sxx, yb, z), (0, 1, 0)), "zinc_plated",
                  kind="fastener", bom=9)
    det = break_edges(Pos(200, 160, Z1 - t - 25 / 2) * Cylinder(45, 25), 3.0)
    det = drill(det, [cz(2.0, Z1 - t - 8, Z1 - t + 1, 200 + dx, 160) for dx in (-30.0, 30.0)])
    K.add("detector", "Heat and smoke detector", det, "insulated_white", kind="bought", bom=9, color="#F87171")
    K.drill("roof", [cz(2.2, Z1 - t - 1, Z1 + 1, 200 + dx, 160) for dx in (-30.0, 30.0)])
    for dx in (-30.0, 30.0):
        K.add("detector_screws", "M4 pan head screw, zinc", pointing(screw(4, t + 8.0, 7.5, 2.6), (200 + dx, 160, Z1), (0, 0, 1)), "zinc_plated",
              kind="fastener", bom=9)


def _fans(K, p):
    """Two 120 mm roof fans on 4 mm spacers."""
    d = derived(p)
    t = p["sheet_t"]
    yf, yfi, ybi, yb = d["yf"], d["yfi"], d["ybi"], d["yb"]
    Z1 = d["z1"]
    fcorner = [(ex, ey) for ex in (-52.5, 52.5) for ey in (-52.5, 52.5)]
    for sx in (-1, 1):
        fx = sx * p["fan_x"]
        frame, rotor = fan_120(fx, p["fan_y"], Z1 - t - 4)
        K.add("fans", f"Fan {'right' if sx > 0 else 'left'}, 120 mm IP55, frame", frame, "matte_black", kind="bought", bom=10)
        K.add("fans", f"Fan {'right' if sx > 0 else 'left'}, rotor", rotor, "matte_black", kind="bought", bom=10)
        K.drill("roof", [cz(2.2, Z1 - t - 1, Z1 + 1, fx + ex, p["fan_y"] + ey) for ex, ey in fcorner])
        for ex, ey in fcorner:
            sp = cp.round_tube(8.0, 1.9, 4.0)
            K.add("fan_spacers", "Fan spacer, 4 mm", Pos(fx + ex, p["fan_y"] + ey, Z1 - t - 4) * sp, "zinc_plated", kind="fastener", bom=10)
            K.add("fan_screws", "M4 pan head screw, zinc", pointing(screw(4, t + 4 + 25.0, 7.5, 2.6), (fx + ex, p["fan_y"] + ey, Z1), (0, 0, 1)), "zinc_plated",
                  kind="fastener", bom=10)


def _hood(K, p, plenum=True):
    """Vent hood over the fans, riveted to the roof (and to the plenum wall when there is one)."""
    d = derived(p)
    t = p["sheet_t"]
    yf, yfi, ybi, yb = d["yf"], d["yfi"], d["ybi"], d["yb"]
    Z1 = d["z1"]
    hx, hyf, hyb, hh = p["hood"]
    n, sw_, sh_ = p["hood_slots"]
    hood = fuse([bx(-hx, hx, hyf, hyf + t, Z1, Z1 + hh), bx(-hx, hx, hyf - 20, hyf, Z1, Z1 + t), bx(-hx, -hx + t, hyf + t, hyb - t, Z1, Z1 + hh),
                 bx(hx - t, hx, hyf + t, hyb - t, Z1, Z1 + hh), bx(-hx - 8, -hx, hyf + t, hyb - t, Z1, Z1 + t), bx(hx, hx + 8, hyf + t, hyb - t, Z1, Z1 + t),
                 bx(-hx, hx, hyf, hyb + 10, Z1 + hh - t, Z1 + hh), bx(-hx, hx, hyb - t, hyb, Z1, Z1 + hh - t), bx(-hx, hx, hyb, hyb + 15, Z1, Z1 + t)])
    pitch = (2 * hx - 60) / (n - 1)
    cuts = [bx(-hx + 30 + i * pitch - sw_ / 2, -hx + 30 + i * pitch + sw_ / 2, hyb - t - 1, hyb + 1, Z1 + 12, Z1 + 12 + sh_) for i in range(n)]
    hrv_f = [(x, 88.0, Z1 + t) for x in (-300.0, -100.0, 100.0, 300.0)]
    hrv_b = [(x, 239.0, Z1 + t) for x in (-300.0, -100.0, 100.0, 300.0)]
    hrv_s = [(sx * (hx + 4), y, Z1 + t) for sx in (-1, 1) for y in (140.0, 200.0)]
    hood = drill(hood, cuts + [pointing(Pos(0, 0, -2.0) * Cylinder(2.1, 4.0 + 1), pt, (0, 0, 1)) for pt in hrv_f + hrv_b + hrv_s])
    K.add("hood", "Vent hood with rear slots and rain lip, 1.5 mm", hood, "painted_steel", bom=10, color="#4B5563")
    K.drill("roof", [cz(2.1, Z1 - t - 1, Z1 + 1, pt[0], pt[1]) for pt in hrv_f + hrv_b + hrv_s])
    for pt in hrv_f + hrv_b + hrv_s:
        K.add("rivets", "4 mm blind rivet, galvanized", rivet(pt, (0, 0, 1), 2 * t), "zinc_plated", kind="fastener", bom=10, group="rivets",
              explode=EXPLODE[10])
    if plenum:
        K.rivets(["roof", ("plenum", 0)], [(x, 105.0, Z1) for x in (-300.0, -100.0, 100.0, 300.0)], (0, 0, 1), 2 * t, bom=10)



# ---------------------------------------------------------------------------- roof frame, glands, canopy (shared)
def _gland(K, xy, z_face, up, t, bom=16):
    """M25 cable gland through a 25 mm hole in a 1.5 mm panel. 'up' is 1 when the gland head is above the face at z_face
    (roof) and -1 when the head is below it (flip), the lock nut on the other side."""
    x, y = xy
    head = cz(15.0, 0, 8.0, 0, 0)
    barrel = cz(12.3, -(t + 7.0), 0.0, 0, 0)
    body = break_edges(fuse([head, barrel]), 0.6) - cz(6.0, -(t + 8.0), 9.0, 0, 0)
    lock = break_edges(cz(15.0, -(t + 6.0), -t, 0, 0) - cz(12.3, -(t + 8.0), 0.0, 0, 0), 0.5)
    loc = Pos(x, y, z_face) * (Rot(180, 0, 0) if up < 0 else Rot(0, 0, 0))
    K.add("glands", "M25 cable gland, nylon", loc * body, "polycarbonate", kind="bought", bom=bom, explode=EXPLODE.get(bom, (0, 0, 0)))
    K.add("glands", "M25 gland lock nut", loc * lock, "polycarbonate", kind="fastener", bom=bom, explode=EXPLODE.get(bom, (0, 0, 0)))


def roof_frame(K, p):
    """Two 40 x 40 x 4 angle roof beams under the canopy post lines, four 4 mm cleats, M8 bolts and weld nuts."""
    d = derived(p)
    t = p["sheet_t"]
    yf, yb, yfi, ybi = d["yf"], d["yb"], d["yfi"], d["ybi"]
    Z1 = d["z1"]
    bw, bt = p["beam"]
    yb0 = -(yfi + t)                                  # the beams run between the roof's front and back flanges
    zv0, zv1 = Z1 - t - bw, Z1 - t - bt               # vertical leg of the beam and the cleat legs
    zc = (zv0 + zv1) / 2
    bolt_pts = [(sx * p["post_x"], sy * yy) for sx in (-1, 1) for sy in (-1, 1) for yy in d["post_bolts_y"]]
    for sx in (-1, 1):
        x_in = sx * (p["post_x"] - bw / 2)
        beam = Location(Plane(origin=(x_in, -sx * yb0, Z1 - t), x_dir=(sx, 0, 0), z_dir=(0, sx, 0))) * cp.angle(bw, bw, bt, 2 * yb0)
        beam = drill(beam, [cz(5.5, Z1 - t - bt - 1, Z1 - t + 1, x, y) for x, y in bolt_pts if x * sx > 0]
                     + [cx(4.5, min(x_in, x_in + sx * bt) - 1, max(x_in, x_in + sx * bt) + 1, y, zc) for y in (-223.0, 223.0)])
        nm = "left" if sx < 0 else "right"
        K.add("beams", f"Roof beam {nm}, 40 x 40 x 4 angle", beam, "mild_steel", bom=1, color="#374151")
        for sy in (-1, 1):
            ya, yb2 = sorted((sy * (yb0 - bt), sy * yb0))
            wall = bx(min(x_in, x_in - sx * bw), max(x_in, x_in - sx * bw), ya, yb2, zv0, zv1)
            yl0, yl1 = sorted((sy * (yb0 - bt), sy * (yb0 - bt) - sy * bw))
            leg = bx(min(x_in, x_in - sx * bt), max(x_in, x_in - sx * bt), yl0, yl1, zv0, zv1)
            xw = x_in - sx * 20.0
            cl = drill(break_edges(fuse([wall, leg]), 0.5), [cy(4.5, ya - 1, yb2 + 1, xw, zc), cx(4.5, min(x_in, x_in - sx * bt) - 1, max(x_in, x_in - sx * bt) + 1, sy * (yb0 - bt - 20.0), zc)])
            fr = "front" if sy < 0 else "back"
            K.add("cleats", f"Roof beam cleat {nm} {fr}, 4 mm steel angle", cl, "mild_steel", bom=1, color="#374151")
            # cleat to roof flange: M8 pan head screw from outside through the front or back panel, flange and cleat, into a weld nut
            ypan = yf if sy < 0 else yb
            ysgn = -sy
            K.drill("front" if sy < 0 else "back", [cy(4.5, min(yf, yfi) - 1, yfi + 1, xw, zc)] if sy < 0 else [cy(4.5, ybi - 1, yb + 1, xw, zc)])
            K.drill("roof", [cy(4.5, yfi - 1, yfi + t + 1, xw, zc)] if sy < 0 else [cy(4.5, ybi - t - 1, ybi + 1, xw, zc)])
            K.add("cleat_screws", "M8 x 20 pan head screw, zinc", pointing(screw(8, 20.0, 16.0, 5.5), (xw, ypan, zc), (0, ysgn * -1, 0)), "zinc_plated",
                  kind="fastener", bom=16, explode=EXPLODE[16])
            yn = sy * (yb0 - bt)                      # inner face of the cleat wall leg
            K.add("cleat_nuts", "M8 weld nut, zinc", pointing(cp.hex_nut(8), (xw, yn, zc), (0, -sy, 0)), "zinc_plated", kind="fastener", bom=1,
                  explode=EXPLODE[1])
            # cleat to beam: M8 bolt set along X, head outside the beam
            K.bolt(8, 2 * bt, frame((x_in + sx * bt, sy * (yb0 - bt - 20.0), zc), (sx, 0, 0)), "cleat_bolts", 16, extra=3.0)


def _loc_panel(p):
    """The panel frame as a Location (panel local x along the long side, y up the slope, z normal)."""
    return panel_frame(p)


def _frame_ring(w, h, off0, off1, z0, z1):
    """Rectangular ring of outer w x h reduced by offsets off0 (outer) and off1 (inner) per side, from z0 to z1."""
    outer = Pos(0, 0, z0) * extrude(Sketch() + Rectangle(w - 2 * off0, h - 2 * off0), z1 - z0)
    inner = Pos(0, 0, z0 - 1) * extrude(Sketch() + Rectangle(w - 2 * off1, h - 2 * off1), z1 - z0 + 2)
    return outer - inner


def solar_panel(K, p, bom=11):
    """400 W module: aluminium frame, glass and cell laminate, junction box, two leads with plug connectors."""
    F = panel_frame(p)
    pw, pd, pth = p["panel"]
    h = pth / 2
    ring = _frame_ring(pw, pd, 0, 4.0, -h, h)
    ledge = _frame_ring(pw, pd, 4.0, 12.0, 5.0, 8.0)
    lip = _frame_ring(pw, pd, 4.0, 9.0, 14.0, h)
    frm = break_edges(fuse([ring, ledge, lip]), 0.5)
    K.add("panel", "Solar panel aluminium frame", F * frm, "aluminium", kind="bought", bom=bom, color="#9CA3AF")
    lam = break_edges(Pos(0, 0, 11.0) * Box(pw - 8.0, pd - 8.0, 6.0), 0.8)
    K.add("panel", "Solar panel glass and cell laminate", F * lam, "glass", kind="bought", bom=bom, color="#1E3A8A")
    jb = break_edges(Pos(0, 330.0, -3.0) * Box(120.0, 80.0, 22.0), 2.0)
    jb = drill(jb, [cz(3.0, -14.0, -13.0, 0, 330.0)])
    K.add("panel", "Panel junction box", F * jb, "matte_black", kind="bought", bom=bom, color="#111827")
    for sx_ in (-1, 1):
        lead = Pos(sx_ * 30.0, 450.0, -3.0) * Rot(90, 0, 0) * Cylinder(2.5, 140.0)
        K.add("panel", "Panel lead, 4 mm2 solar cable", F * lead, "rubber_belt", kind="bought", bom=bom)
        plug = break_edges(Pos(sx_ * 30.0, 535.0, -3.0) * Rot(90, 0, 0) * Cylinder(6.0, 30.0), 1.0)
        K.add("panel", "Solar connector, plug", F * plug, "matte_black", kind="bought", bom=bom)


def canopy(K, p):
    """Canopy: four 50 x 50 x 3 posts welded to 8 mm base plates and cut and welded to 6 mm cap plates at the 10 degree
    tilt, eight M10 bolts through the roof into the roof beams, two 50 x 40 x 3 rails bolted to the caps, four end clamps
    on M8 bolts, and the solar panel."""
    d = derived(p)
    t = p["sheet_t"]
    Z1, D = d["z1"], p["D"]
    bw, bt = p["beam"]
    F = panel_frame(p)
    pw, pd, pth = p["panel"]
    rh, rw, ro = p["rail_h"], p["rail_w"], p["rail_over"]
    bpw, bpl, bpt = p["base_plate"]
    s, tt = p["post"] / 2, p["post_t"]
    lz_cap = -pth / 2 - rh - p["cap_t"]
    lz_rail = -pth / 2 - rh
    a = math.radians(-p["tilt_deg"])
    cut = F * bx(-3000, 3000, -3000, 3000, -3000, lz_cap)
    for k, (x, y, zb, zt, ly) in enumerate(post_geometry(p)):
        n = k + 1
        tube = Pos(x, y, zb) * cp.shs(p["post"], tt, zt + 60 - zb)
        tube = tube & cut
        K.add("posts", f"Canopy post {n}, 50 x 50 x 3 SHS", tube, "mild_steel", bom=12, color="#374151")
        cap = bx(x - s, x + s, ly - 35, ly + 35, lz_cap, lz_cap + p["cap_t"])
        cap = drill(break_edges(cap, 0.8), [cz(4.5, lz_cap - 1, lz_cap + p["cap_t"] + 1, x, ly)])
        K.add("caps", f"Canopy post {n} cap plate, 6 mm", F * cap, "mild_steel", bom=12, color="#374151")
        y0, y1 = max(y - s - 25, -D / 2), min(y + s + 25, D / 2)
        base = bx(x - bpw / 2, x + bpw / 2, y0, y1, Z1, Z1 + bpt)
        base = drill(break_edges(base, 0.8), [cz(5.5, Z1 - 1, Z1 + bpt + 1, x, math.copysign(yy, y)) for yy in d["post_bolts_y"]])
        K.add("bases", f"Canopy post {n} base plate, 8 mm", base, "mild_steel", bom=12, color="#374151")
        for yy in d["post_bolts_y"]:
            K.bolt(10, bpt + t + bt, Pos(x, math.copysign(yy, y), Z1 + bpt), "post_bolts", 12, extra=None)
        # stitch welds on the two faces that face along Y: 8 mm beads at each end of the face, clear of the bolt washers
        for sg in (-1, 1):
            yface = y + sg * s
            for xs_ in (x - 19, x + 11):
                K.add("welds", "Stitch weld, post to base plate", bead((xs_, yface, Z1 + bpt), (1, 0, 0), 8.0, 4.0, (0, sg, 0), (0, 0, 1)),
                      "mild_steel", kind="weld", bom=12, group="posts")
            # post to cap plate: the cap underside is tilted, so the bead section is a triangle in the Y-Z plane
            A0 = to_global(0.0, lz_cap, p)
            U = (to_global(1.0, lz_cap, p)[0] - A0[0], to_global(1.0, lz_cap, p)[1] - A0[1])
            sc = (yface - A0[0]) / U[0]
            Py, Pz = A0[0] + sc * U[0], A0[1] + sc * U[1]
            for xs_ in (x - 19, x + 11):
                K.add("welds", "Stitch weld, post to cap plate",
                      bead_tri((xs_, Py, Pz), (xs_, Py + sg * 4.0 * abs(U[0]), Pz + sg * 4.0 * U[1] * (1 if U[0] > 0 else -1)),
                               (xs_, Py, Pz - 4.0), (1, 0, 0), 8.0), "mild_steel", kind="weld", bom=12, group="posts")
    # rails and their bolts to the cap plates
    cap_pts = [(x, ly) for (x, y, zb, zt, ly) in post_geometry(p)]
    for x in (-p["post_x"], p["post_x"]):
        L = pd / 2 + ro
        rail = Pos(x, L, lz_rail + rh / 2) * Rot(90, 0, 0) * cp.rhs(rw, rh, 3.0, 2 * L)
        holes = [cz(4.5, lz_rail - 1, lz_rail + 4, cx_, ly) for (cx_, ly) in cap_pts if cx_ == x]
        for sg in (-1, 1):
            holes.append(cz(4.5, -pth / 2 - 4, -pth / 2 + 1, x, sg * (pd / 2 + 12.5)))
        K.add("rails", f"Canopy rail {'left' if x < 0 else 'right'}, 50 x 40 x 3 RHS", F * drill(rail, holes), "mild_steel", bom=12, color="#52525B")
    for (cx_, ly) in cap_pts:
        K.bolt(8, 9.0, F * Pos(cx_, ly, lz_rail + 3.0), "rail_bolts", 12, extra=3.0)
    # end clamps
    for x in (-p["post_x"], p["post_x"]):
        for sg in (-1, 1):
            e = sg * pd / 2
            base = bx(x - 20, x + 20, min(e, e + sg * 19), max(e, e + sg * 19), -pth / 2, -pth / 2 + 4)
            up = bx(x - 20, x + 20, min(e, e + sg * 4), max(e, e + sg * 4), -pth / 2, pth / 2 + 4)
            lip = bx(x - 20, x + 20, min(e - sg * 8, e + sg * 4), max(e - sg * 8, e + sg * 4), pth / 2, pth / 2 + 4)
            cl = drill(break_edges(fuse([base, up, lip]), 0.5), [cz(4.5, -pth / 2 - 1, -pth / 2 + 5, x, sg * (pd / 2 + 12.5))])
            K.add("clamps", "Panel end clamp, 4 mm steel", F * cl, "zinc_plated", bom=12, color="#A1A1AA")
            K.bolt(8, 7.0, F * Pos(x, sg * (pd / 2 + 12.5), -pth / 2 + 4), "clamp_bolts", 12, extra=2.0)
    solar_panel(K, p)


def roof_glands(K, p):
    d = derived(p)
    t = p["sheet_t"]
    _gland(K, (-200.0, 60.0), d["z1"], 1, t)
    _gland(K, (340.0, 120.0), d["z0"] + t, 1, t)


def vermiculite_floor(K, p, fit):
    """Trial option (line 19): a 1 mm stainless tray of exfoliated vermiculite on each fitted bay floor, in front of the cradle,
    riveted through the liner floor and the deck."""
    d = derived(p)
    t = p["sheet_t"]
    yfi = d["yfi"]
    dz = d["deck_z"]
    lw = p["liner_w"] / 2
    cw = p["cradle_w"] / 2
    vh, vt, vfree = p["verm_tray"]
    for i, xc in enumerate(fit):
        x0, x1 = xc - lw + t + 1, xc + lw - t - 1
        y0, y1 = yfi + 2, -cw - VERM_GAP
        z0 = dz + t
        pts = [(x, y) for x in (xc - 70.0, xc + 70.0) for y in (-230.0, -100.0)]
        tray = bx(x0, x1, y0, y1, z0, z0 + vh) - bx(x0 + vt, x1 - vt, y0 + vt, y1 - vt, z0 + vt, z0 + vh + 1)
        tray = drill(break_edges(tray, 0.4), [cz(2.1, z0 - 1, z0 + vt + 1, x, y) for x, y in pts])
        K.add("verm_trays", f"Bay {i + 1} vermiculite tray, 1 mm stainless", tray, "stainless", bom=19, color="#94A3B8")
        fill = bx(x0 + vt + 0.6, x1 - vt - 0.6, y0 + vt + 0.6, y1 - vt - 0.6, z0 + vt + 0.6, z0 + vh - vfree)
        fill = drill(fill, [cz(4.5, z0, z0 + vt + 5, x, y) for x, y in pts])
        K.add("verm_fill", f"Bay {i + 1} exfoliated vermiculite fill", fill, "sand", bom=19, color="#C8A165")
        for x, y in pts:
            K.add("rivets", "4 mm blind rivet, stainless", rivet((x, y, z0 + vt), (0, 0, 1), vt + 2 * t), "stainless", kind="fastener", bom=19,
                  group="rivets", explode=EXPLODE[19])
        cutters = [cz(2.1, z0 - 2 * t - 1, z0 + 1, x, y) for x, y in pts]
        K.drill("liners", cutters, i)
        K.drill("deck", cutters)


def option_a(fitted=None, variant=None, site=True, p=P):
    K, d, fit, blank, xs = _a1(fitted, p)
    nf = len(fit)
    _a2(K, p, nf, fit, blank, xs)
    roof_frame(K, p)
    roof_glands(K, p)
    canopy(K, p)
    if variant == "vermiculite":
        vermiculite_floor(K, p, fit)
    if site:
        site_parts(K, p)
    return K


def components(option="A", fitted=None, variant=None, site=True):
    """Parts of one option as cad_parts.part() dicts. Option A is built as the first prototype (two bays fitted) unless
    'fitted' says otherwise."""
    if option == "A":
        return option_a(fitted, variant, site).parts
    if option == "B":
        return option_b(site).parts
    if option == "C":
        return option_c(site).parts
    raise KeyError(option)


# ---------------------------------------------------------------------------- shared builders for options B and C
def _shelf(K, p, n, sz=380.0, idx=0, first=0, label0=None):
    """Charger shelf (folded 1.5 mm sheet riveted to the side panels) at height sz, with n chargers on it."""
    d = derived(p)
    t, fl = p["sheet_t"], p["flange"]
    xi, flx = d["xi"], d["flx"]
    W = p["W"]
    shelf = fuse([bx(-flx, flx, -60, 220, sz - t, sz), bx(-flx, flx, -60, -60 + t, sz - t - fl, sz - t),
                  bx(-flx, flx, 220 - t, 220, sz - t - fl, sz - t), bx(-xi, -flx, -60, 220, sz - t - fl, sz),
                  bx(flx, xi, -60, 220, sz - t - fl, sz)])
    xsel = d["charger_x"][first:first + n]
    cut = [cz(3.0, sz - t - 1, sz + 1, x + ex, ey) for x in xsel for ex in (-60, 60) for ey in (-26, 186)]
    K.add("shelf", f"Charger shelf {idx + 1}, 1.5 mm galvanized, folded", drill(shelf, cut), "painted_steel", bom=1, color="#9CA3AF")
    for sx in (-1, 1):
        K.rivets([("side_l" if sx < 0 else "side_r"), ("shelf", idx)], [(sx * W / 2, y, sz - 13.0) for y in (-40.0, 40.0, 120.0, 200.0)],
                 (sx, 0, 0), 2 * t)
    for i, x in enumerate(xsel):
        body = fuse([bx(x - 80, x + 80, -20, 180, sz, sz + 70)] + [bx(x - 72 + 18 * k - 1.5, x - 72 + 18 * k + 1.5, -18, 178, sz + 70, sz + 78) for k in range(9)]
                    + [bx(x - 70, x - 50, -32, -20, sz, sz + 4), bx(x + 50, x + 70, -32, -20, sz, sz + 4),
                       bx(x - 70, x - 50, 180, 192, sz, sz + 4), bx(x + 50, x + 70, 180, 192, sz, sz + 4)])
        body = drill(break_edges(body, 1.0), [cz(2.9, sz - 1, sz + 5, x + ex, ey) for ex in (-60, 60) for ey in (-26, 186)])
        K.add("chargers", f"Charger {(first if label0 is None else label0) + i + 1}, 54.6 V 5 A, with heat sink", body, "aluminium", kind="bought", bom=5, color="#C2410C")
        for ex in (-60, 60):
            for ey in (-26, 186):
                K.bolt(5, t + 4, Pos(x + ex, ey, sz + 4), "charger_screws", 16, extra=3.0)


def _door2(K, p, xc, zc, ow, oh, dw, dh, n, lwo, label="Door"):
    """Door on a continuous hinge with gasket, pull handle and lock tongue, over an opening ow x oh centred at (xc, zc) in the
    front panel. lwo is the outer half width of the box behind the opening (the lock sits on its right wall)."""
    d = derived(p)
    t = p["sheet_t"]
    yf, yfi = d["yf"], d["yfi"]
    dt = p["door"][2]
    gw, gt = p["gasket"]
    ydb = yf - gt
    o0, o1 = zc - oh / 2, zc + oh / 2
    HW = ow / 2
    xl = xc - dw / 2
    dz0 = zc - dh / 2
    hx_ = xc + dw / 2 - 28.5
    hpts = [(hx_, zc - 18.0), (hx_, zc + 18.0)]
    xt = xc + lwo - 40.0
    door = slab("y", ydb - dt, ydb, xl, xl + dw, dz0, dz0 + dh, r=8.0, edge=0.5)
    door = drill(door, [cy(2.1, ydb - dt - 1, ydb + 1, x, z) for x, z in hpts] + [cy(2.1, ydb - dt - 1, ydb + 1, xc + lwo - 54.0, zc + k) for k in (-5.0, 5.0)])
    K.add("doors", f"{label} {n} door, 2 mm steel", door, "painted_steel", bom=2, color="#0F766E")
    gk = bx(xc - HW - 1 - gw, xc + HW + 1 + gw, ydb, yf, o0 - 1 - gw, o1 + 1 + gw) - bx(xc - HW - 1, xc + HW + 1, ydb - 1, yf + 1, o0 - 1, o1 + 1)
    K.add("gaskets", f"{label} {n} door gasket, EPDM 7 x 3", break_edges(gk, 0.6), "epdm", kind="bought", bom=2)
    hbar = fuse([cz(6.0, zc - 16.0, zc + 16.0, hx_, ydb - dt - 16.0)] + [cy(4.0, ydb - dt - 16.0, ydb - dt, x, z) for x, z in hpts])
    hbar = drill(break_edges(hbar, 1.0), [cy(2.0, ydb - dt - 8.0, ydb - dt + 0.5, x, z) for x, z in hpts])
    K.add("handles", f"{label} {n} pull handle, stainless", hbar, "stainless", kind="bought", bom=2)
    for x, z in hpts:
        K.add("handle_screws", "M4 button screw, A2", pointing(screw(4, 10.0, 7.0, 2.2), (x, ydb, z), (0, 1, 0)), "stainless", kind="fastener", bom=2)
    tg = fuse([bx(xc + lwo - 60, xt + 4, ydb, ydb + 4, zc - 10, zc + 10), bx(xt, xt + 4, ydb, yfi + 16.5, zc - 10, zc + 10)])
    tg = drill(tg, [cx(3.0, xt - 1, xt + 5, yfi + 8.0, zc)] + [cy(2.1, ydb - 1, ydb + 5, xc + lwo - 54.0, zc + k) for k in (-5.0, 5.0)])
    K.add("tongues", f"{label} {n} lock tongue, 4 mm angle", break_edges(tg, 0.4), "painted_steel", bom=2, color="#9CA3AF")
    for k in (-5.0, 5.0):
        K.add("rivets", "4 mm blind rivet, galvanized", rivet((xc + lwo - 54.0, ydb - dt, zc + k), (0, -1, 0), dt + 4.0), "zinc_plated", kind="fastener",
              bom=2, group="rivets")
    hxb, hyb = xl - 3.5, yf - 3.5
    body, pin = piano_hinge(xl - 18, xl + 24, yf - t, t, hxb, hyb, o0 + 15, o1 - 15, 0, 0, ydb - dt - t)
    nr = int((oh - 80.0) // 100.0) + 1
    zr = [o0 + 40.0 + k * 100.0 for k in range(nr)]
    body = drill(body, [cy(2.1, yf - t - 1, yf + 1, xl - 12.0, z) for z in zr] + [cy(2.1, ydb - dt - t - 1, ydb + 1, xl + 14.0, z) for z in zr])
    K.add("hinges", f"{label} {n} piano hinge, stainless", body, "stainless", kind="bought", bom=2)
    K.add("hinges", f"{label} {n} hinge pin", pin, "stainless", kind="bought", bom=2)
    for z in zr:
        K.add("rivets", "4 mm blind rivet, stainless", rivet((xl - 12.0, yf - t, z), (0, -1, 0), 2 * t), "stainless", kind="fastener", bom=2, group="rivets")
        K.add("rivets", "4 mm blind rivet, stainless", rivet((xl + 14.0, ydb - dt - t, z), (0, -1, 0), t + dt), "stainless", kind="fastener", bom=2,
              group="rivets")
    K.drill("front", [cy(2.1, yf - 1, yfi + 1, xl - 12.0, z) for z in zr])
    K.drill("doors", [cy(2.1, ydb - dt - 1, ydb + 1, xl + 14.0, z) for z in zr], len(K.by["doors"]) - 1)


def _lock2(K, p, xc, zc, lwo, key, idx, n, label="Door"):
    """12 V solenoid lock on the right wall of the box named by (key, idx), plunger through the door tongue, four M4 screws."""
    d = derived(p)
    t = p["sheet_t"]
    yfi = d["yfi"]
    xt = xc + lwo - 40.0
    lock = break_edges(bx(xc + lwo - t - 30, xc + lwo - t, yfi + 2.5, yfi + 32.5, zc - 25, zc + 25), 1.5)
    ys = (yfi + 6.0, yfi + 29.0)
    zs = (zc - 19.0, zc + 19.0)
    lock = drill(lock, [cx(2.8, xc + lwo - t - 31, xc + lwo - t + 1, yfi + 8.0, zc)] + [cx(2.0, xc + lwo - t - 8, xc + lwo - t + 1, yy, zz) for yy in ys for zz in zs])
    K.add("locks", f"{label} {n} solenoid lock, 12 V fail-secure", lock, "matte_black", kind="bought", bom=2, color="#374151")
    K.add("locks", f"{label} {n} lock plunger", cx(2.75, xt - 1, xc + lwo - t - 30, yfi + 8.0, zc), "stainless", kind="bought", bom=2)
    K.drill(key, [cx(2.1, xc + lwo - 2, xc + lwo + 1, yy, zz) for yy in ys for zz in zs], idx)
    for yy in ys:
        for zz in zs:
            K.add("lock_screws", "M4 pan head screw, zinc", pointing(screw(4, t + 6.0, 7.5, 2.6), (xc + lwo, yy, zz), (1, 0, 0)), "zinc_plated", kind="fastener", bom=16)


def _shell_bc(K, p, openings, solar, fan_extra=()):
    """The cabinet shared by options B and C: plinth, shell, rivets, floor bolts, rear boxes, glands, fire unit and
    detector, two roof fans and vent hood. With solar: roof beams, canopy and MPPT controller."""
    d = derived(p)
    t = p["sheet_t"]
    Z1 = d["z1"]
    plinth_parts(K, p)
    fan_holes = [cz(p["fan_hole_r"], Z1 - t - 1, Z1 + 1, sx * p["fan_x"], p["fan_y"]) for sx in (-1, 1)]
    holes = fan_holes + [cz(12.5, Z1 - t - 1, Z1 + 1, -200, 60)]
    if solar:
        holes += [cz(5.5, Z1 - t - 1, Z1 + 1, sx * p["post_x"], sy * yy) for sx in (-1, 1) for sy in (-1, 1) for yy in d["post_bolts_y"]]
    shell_panels(K, p, openings, roof_extra_holes=holes)
    shell_rivets(K, p)
    floor_bolt_sets(K, p)
    _boxes(K, p, mppt=solar)
    _access(K, p)
    _service(K, p)
    _fire(K, p)
    _fans(K, p)
    _hood(K, p, False)
    if solar:
        roof_frame(K, p)
    roof_glands(K, p)
    if solar:
        canopy(K, p)


# ---------------------------------------------------------------------------- option B: rotary magazine
def option_b(site=True, p=P):
    K = Kit(chosen=False)
    d = derived(p)
    t = p["sheet_t"]
    xi = d["xi"]
    yf, yfi, ybi = d["yf"], d["yfi"], d["ybi"]
    Z0, Z1 = d["z0"], d["z1"]
    o0, o1 = p["open_z"]
    HW = p["bay_open_w"] / 2
    so_w, so_0, so_1 = p["service_open"]
    lw, lt, dz = p["liner_w"] / 2, p["liner_top"], d["deck_z"]
    dw, dh, dt = p["door"]
    _shell_bc(K, p, [(-HW, HW, o0, o1, 4.0), (-so_w, so_w, so_0, so_1, 6.0), (340.0, 460.0, 880.0, 1180.0, 4.0)], solar=True)
    _shelf(K, p, 4)
    # hatch chute: a short folded box behind the one hatch, carrying the lock
    depth = 36.0
    ch = bx(-lw, lw, yfi, yfi + depth, dz, lt) - bx(-lw + t, lw - t, yfi - 1, yfi + depth + 1, dz + t, lt - t)
    ch = fuse([ch, bx(-lw, lw, yfi, yfi + t, lt, lt + 15), bx(-lw, lw, yfi, yfi + t, dz - 15, dz)])
    K.add("liners", "Hatch chute, 1.5 mm galvanized, folded box", ch, "painted_steel", color="#9CA3AF")
    K.rivets(["front", "liners"], [(sx * 60.0, yf, z) for sx in (-1, 1) for z in (lt + 8.0, dz - 8.0)], (0, -1, 0), 2 * t, bom=None)
    _door2(K, p, 0.0, 960.0, 2 * HW, o1 - o0, dw, dh, 1, lw, "Hatch")
    _lock2(K, p, 0.0, 960.0, lw, "liners", 0, 1, "Hatch")

    # support pan for the indexer, 3 mm, screwed to the side panels
    zp, ts = p["index_z"], 3.0
    Ya, R = p["turret_y"], p["turret_r"]
    xf = xi - ts
    pan = fuse([bx(-xf, xf, -150, 160, zp - ts, zp), bx(-xi, -xf, -150, 160, zp - ts - 40, zp), bx(xf, xi, -150, 160, zp - ts - 40, zp),
                bx(-xf, xf, -150, -150 + ts, zp - ts - 25, zp - ts), bx(-xf, xf, 160 - ts, 160, zp - ts - 25, zp - ts)])
    ib = [(sx * 95.0, Ya + sy * 95.0) for sx in (-1, 1) for sy in (-1, 1)]
    pan = drill(pan, [cz(4.5, zp - ts - 1, zp + 1, x, y) for x, y in ib])
    K.add("pan", "Indexer support pan, 3 mm, folded", pan, "painted_steel", color="#9CA3AF")
    for sx in (-1, 1):
        sk = "side_l" if sx < 0 else "side_r"
        pts = [(sx * (xi + t), y, zp - 20.0) for y in (-120.0, 5.0, 130.0)]
        K.drill(sk, [cx(3.3, sx * (xi - 1), sx * (xi + t + 1), y, z) for _, y, z in pts])
        K.drill("pan", [cx(3.0, sx * (xf - 1), sx * (xi + 1), y, z) for _, y, z in pts], 0)
        for x, y, z in pts:
            K.add("pan_screws", "M6 button screw, zinc", pointing(screw(6, 9.0, 11.0, 3.6), (x, y, z), (sx, 0, 0)), "zinc_plated", kind="fastener")
    # rotary indexing table with stepper drive: one bought unit, base flange bolted down, table plate tapped for the turret disc
    disc_z0 = dz - 4.5 - p["disc_t"]                  # disc bottom, 695.5
    tb = disc_z0                                      # table plate top
    flange = bx(-110, 110, Ya - 110, Ya + 110, zp, zp + 15)
    housing = cz(80.0, zp + 15, tb - 20, 0, Ya)
    table = cz(125.0, tb - 20, tb, 0, Ya)
    motor = fuse([bx(80, 88, Ya - 40, Ya + 40, 625, 705 - 60), bx(88, 178, Ya - 28.5, Ya + 28.5, 645 - 28.5, 645 + 28.5)])
    unit = fuse([flange, housing, table, motor])
    tp = [(28.3 * sx, Ya + 28.3 * sy) for sx in (-1, 1) for sy in (-1, 1)]
    unit = drill(break_edges(unit, 0.8), [cz(4.5, zp - 1, zp + 16, x, y) for x, y in ib] + [cz(4.0, tb - 14, tb + 1, x, y) for x, y in tp])
    K.add("indexer", "Rotary indexing table, 250 mm, stepper drive", unit, "mild_steel", kind="bought", color="#1F2937")
    for x, y in ib:
        K.bolt(8, 15 + ts, Pos(x, y, zp + 15), "index_bolts", None, extra=3.0)
    # turret disc
    disc = Pos(0, Ya, disc_z0) * extrude(Sketch() + Circle(210.0), p["disc_t"])
    disc_cut = [cz(4.5, disc_z0 - 1, dz + 1, x, y) for x, y in tp]
    K.add("disc", "Turret disc, 6 mm steel plate", disc, "painted_steel", color="#6B7280")
    for x, y in tp:
        K.add("disc_bolts", "M8 x 20 hex bolt (ISO 4017)", Pos(x, y, dz - 4.5 + 0.0) * cp.hex_bolt(8, 20.0), "zinc_plated", kind="fastener")
    # four pockets
    pz0 = pack_z0(p)
    cz0 = dz + t
    cb = p["cradle_b"] / 2
    yc = p["plug_offset"]
    hw, hd = p["pack_w"] / 2, p["pack_d"] / 2
    g = p["guide_clear"]
    yb_ = hd + p["latch_proud"] + 1
    zl = pz0 + p["pack_l"] - p["latch_from_top"]
    Wy = 82.0
    for k, ang in enumerate((0, 90, 180, 270)):
        n = k + 1
        T = Pos(0, Ya, 0) * Rot(0, 0, ang) * Pos(0, -R, 0)
        cz_disc = disc_z0
        cr = bx(-cb, cb, -cb, cb, cz0, pz0)
        cr = cr - bx(-p["plug_w"] / 2 - 1, p["plug_w"] / 2 + 1, yc - p["plug_d"] / 2 - 1, yc + p["plug_d"] / 2 + 1, pz0 - p["plug_h"] - 1.5, pz0 + 1)
        cr = cr - bx(-p["plug_w"] / 2 - 8, p["plug_w"] / 2 + 8, yc - p["plug_d"] / 2 - 8, yc + p["plug_d"] / 2 + 8, cz0 - 1, pz0 - p["plug_h"] - 1.5)
        cr = cr - bx(-31, 31, yb_ + 8 - 0.5, yb_ + 11.5, pz0 - 10, pz0 + 1)
        cr = cr + bx(-hw - g - 5, -hw - g, -45, 45, pz0, pz0 + p["guide_h"]) + bx(hw + g, hw + g + 5, -45, 45, pz0, pz0 + p["guide_h"])
        scr = [(sx * 45.0, sy * 45.0) for sx in (-1, 1) for sy in (-1, 1)]
        cr = drill(cr, [cz(2.75, cz0 - 1, pz0 + 1, x, y) for x, y in scr] + [cz(5.0, pz0 - 5, pz0 + 1, x, y) for x, y in scr])
        K.add("cradles", f"Pocket {n} cradle with guide faces (printed)", T * cr, "hdpe_black", color="#0E7490")
        for x, y in scr:
            K.add("cradle_screws", "M5 x 30 button screw, zinc", T * pointing(screw(5, 30.0, 9.5, 3.0), (x, y, pz0 - 5), (0, 0, 1)), "zinc_plated", kind="fastener")
        rec = bx(-36, 36, yc - 25, yc + 25, cz0, pz0 - p["plug_h"] - 1.5) - bx(-28, 28, yc - 17, yc + 17, pz0 - p["plug_h"] - 4.5, pz0)
        rec = rec + fuse([cz(1.2, pz0 - p["plug_h"] - 4.5, pz0 - p["plug_h"] - 1.5, -20 + 8 * j, yc) for j in range(6)])
        K.add("receptacles", f"Pocket {n} SwapCell v0.3 receptacle", T * rec, "hdpe_black", kind="bought", color="#1F2937")
        # back plate: web, side flanges toward the pack, foot flange screwed to the disc
        ztop_w = pz0 + 300.0
        web = fuse([bx(-53.5, 53.5, Wy, Wy + t, cz0, ztop_w), bx(-53.5, -52.0, 62.0, Wy, cz0, ztop_w), bx(52.0, 53.5, 62.0, Wy, cz0, ztop_w),
                    bx(-30, 30, Wy + t, Wy + t + 15, cz0, cz0 + t)])
        fpts = [(-20.0, Wy + t + 8.5 + 4.0), (20.0, Wy + t + 8.5 + 4.0)]
        fpts = [(x, 91.0) for x in (-20.0, 20.0)]
        web = drill(web, [cz(2.75, cz0 - 1, cz0 + t + 1, x, y) for x, y in fpts])
        ztop = zl + 30
        cat = fuse([bx(-30, 30, yb_ + 8, yb_ + 11, pz0 - 10, ztop), bx(-30, 30, yb_ + 8, Wy, ztop - 3, ztop), bx(-30, 30, Wy - 3, Wy, ztop - 43, ztop - 3),
                    bx(-25, 25, yb_, yb_ + 8, zl + p["latch_h"] / 2 + 1, zl + p["latch_h"] / 2 + 9)])
        rv = [(sx * 15.0, Wy + t, ztop - 23.0) for sx in (-1, 1)]
        cutters = [cy(2.1, Wy - 4, Wy + t + 1, x, z) for x, _, z in rv]
        web = drill(web, cutters)
        cat = drill(break_edges(cat, 0.5), cutters)
        K.add("pocket_plates", f"Pocket {n} back plate, 1.5 mm", T * web, "painted_steel", color="#9CA3AF")
        K.add("catches", f"Pocket {n} catch bracket, 3 mm steel", T * cat, "painted_steel", color="#7C3AED")
        for x, y, z in rv:
            K.add("rivets", "4 mm blind rivet, galvanized", T * rivet((x, y, z), (0, 1, 0), t + 3.0), "zinc_plated", kind="fastener")
        for x, y in fpts:
            K.add("foot_screws", "M5 button screw, zinc", T * pointing(screw(5, 7.0, 9.5, 3.0), (x, y, cz0 + t), (0, 0, 1)), "zinc_plated", kind="fastener")
        disc_cut += [(T * cz(2.5, cz_disc - 1, dz, x, y)) for x, y in scr + fpts]
        disc_cut.append(T * bx(-20, 20, yc - 15, yc + 15, cz_disc - 1, dz + 1))
        if k < 3:
            q = pack_part(K, 0.0, p, n)
            q["shape"] = T * q["shape"]
    K.drill("disc", disc_cut)
    if site:
        site_parts(K, p)
    return K


# ---------------------------------------------------------------------------- option C: locker bank
LOCKER_COLS = (-320.0, 20.0)
LOCKER_ROWS = (1190.0, 960.0, 730.0)      # top handle at 1.21 m, inside the 1.22 m reach limit (R11)


def option_c(site=True, p=P):
    p = dict(p, service_open=(p["service_open"][0], p["service_open"][1], 590.0))   # service door shortened to clear the bottom locker
    K = Kit(chosen=False)
    d = derived(p)
    t = p["sheet_t"]
    yf, yfi, ybi = d["yf"], d["yfi"], d["ybi"]
    so_w, so_0, so_1 = p["service_open"]
    ow, oh = p["locker_w"], p["locker_h"]
    lwo = ow / 2 + t
    dw, dh = ow + 22.0, oh + 14.0
    depth = 420.0
    pos = [(xc, zc) for zc in LOCKER_ROWS for xc in LOCKER_COLS]
    openings = [(xc - ow / 2, xc + ow / 2, zc - oh / 2, zc + oh / 2, 4.0) for xc, zc in pos]
    openings += [(-so_w, so_w, so_0, so_1, 6.0), (340.0, 460.0, 880.0, 1180.0, 4.0)]
    _shell_bc(K, p, openings, solar=False)
    _shelf(K, p, 4)
    _shelf(K, p, 2, sz=520.0, idx=1, label0=4)
    yB = yfi + depth - t
    for n, (xc, zc) in enumerate(pos, start=1):
        zf = zc - oh / 2
        car = bx(xc - lwo, xc + lwo, yfi, yfi + depth, zf - t, zc + oh / 2 + t) - bx(xc - ow / 2, xc + ow / 2, yfi - 1, yB, zf, zc + oh / 2)
        car = fuse([car, bx(xc + lwo, xc + lwo + 20, yfi, yfi + t, zc - 35, zc + 45)])
        yT0, yT1 = yfi + 20.0, yB - 26.0
        tpts = [(xc + sx * 57.5, y) for sx in (-1, 1) for y in (yT0 + 30.0, yT1 - 30.0)]
        car = drill(car, [cz(2.75, zf - t - 1, zf + 1, x, y) for x, y in tpts])
        K.add("lockers", f"Locker {n} box, 1.5 mm galvanized, folded", car, "painted_steel", color="#9CA3AF")
        K.rivets(["front", ("lockers", n - 1)], [(xc + lwo + 12.0, yf, zc - 20.0), (xc + lwo + 12.0, yf, zc + 30.0)], (0, -1, 0), 2 * t, bom=None)
        tray = fuse([bx(xc - 65, xc + 65, yT0, yT1, zf, zf + 12), bx(xc - 50, xc - 46.5, yT0, yT1, zf + 12, zf + 37), bx(xc + 46.5, xc + 50, yT0, yT1, zf + 12, zf + 37)])
        tray = drill(break_edges(tray, 0.6), [cz(2.75, zf - 1, zf + 13, x, y) for x, y in tpts])
        K.add("trays", f"Locker {n} pack tray (printed)", tray, "hdpe_black", color="#0E7490")
        for x, y in tpts:
            K.bolt(5, 12.0 + t, Pos(x, y, zf + 12), "tray_screws", None, extra=3.0)
        zp_ = zf + 12 + 40.0
        hs = bx(xc - 36, xc + 36, yB - 26, yB, zp_ - 20, zp_ + 36) - bx(xc - 29, xc + 29, yB - 27, yB - 3, zp_ - 10, zp_ + 26)
        K.add("receptacles", f"Locker {n} SwapCell v0.3 receptacle housing", break_edges(hs, 0.6), "hdpe_black", kind="bought", color="#1F2937")
        if n in (1, 4):
            q = pack_part(K, 0.0, p, n, key="packs")
            q["name"] = f"Rider's own SwapCell v0.3 pack in locker {n}"
            q["shape"] = Pos(xc, yB - 26, zp_) * Rot(90, 0, 0) * Pos(0, 0, -pack_z0(p)) * q["shape"]
        _door2(K, p, xc, zc, ow, oh, dw, dh, n, lwo, "Locker")
        _lock2(K, p, xc, zc, lwo, "lockers", n - 1, n, "Locker")
    if site:
        site_parts(K, p)
    return K


# ---------------------------------------------------------------------------- adapter for the build plan pictures
class Comp:
    """One build-plan component: the merged shape of every model part that belongs to it."""

    def __init__(self, key, shape, bom=None):
        self.key, self.shape, self.bom = key, shape, bom


# build-plan component -> model part keys merged into it
LEGACY = {
    "plinth": ("plinth", "plinth_welds"), "floor": ("floor",), "back": ("back",), "side_l": ("side_l",), "side_r": ("side_r",),
    "front": ("front",), "roof": ("roof",), "floor_bolts": ("floor_bolts",), "deck": ("deck",), "shelf": ("shelf",), "plenum": ("plenum",),
    "boxes": ("controller", "mppt", "grid"), "controller": ("controller",), "mppt": ("mppt",), "grid": ("grid",), "chargers": ("chargers",), "liners": ("liners",), "cradles": ("cradles",),
    "receptacles": ("receptacles",), "catches": ("catches",), "locks": ("locks",), "packs": ("packs",),
    "doors": ("doors", "handles", "tongues"), "gaskets": ("gaskets",), "hinges": ("hinges",), "blanks": ("blanks",), "access": ("access",),
    "service": ("service",), "service_gasket": ("service_gasket",), "service_hinge": ("service_hinge",), "cam_lock": ("cam_lock",),
    "filter": ("filter",), "fire": ("fire", "fire_straps"), "detector": ("detector",), "fans": ("fans", "fan_spacers"), "hood": ("hood",),
    "beams": ("beams", "cleats"), "posts": ("posts", "caps", "bases", "welds"), "post_bolts": ("post_bolts",), "rails": ("rails",),
    "clamps": ("clamps",), "panel": ("panel",), "verm_trays": ("verm_trays",), "verm_fill": ("verm_fill",), "pad": ("pad",), "anchors": ("anchors",),
}


def build_components(p=PARAMS, fitted=None, variant=None, site=False):
    """Option A merged by build-plan component, as {key: Comp}, for the build plan pictures (cad/src/build_plan_media.py)."""
    K = option_a(fitted, variant, site, p)
    out = {}
    for name, keys in LEGACY.items():
        shapes = [q["shape"] for k in keys for q in K.by.get(k, [])]
        if shapes:
            out[name] = Comp(name, shapes[0] if len(shapes) == 1 else Compound(shapes))
    return out


_box = bx


def _compound(parts):
    return Compound([q["shape"] for q in parts])


def assemblies():
    """Assemblies exported as STEP and STL (cad/step, cad/stl): name -> Compound."""
    A2 = option_a(None, None, False)
    A4 = option_a(P["n_bays"], None, False)
    A1 = option_a(1, "vermiculite", True)
    sel = lambda K, boms: [q for q in K.parts if q["bom"] in boms]
    return {
        "dockhub-assembly": _compound(A2.parts),
        "dockhub-assembly-4-bays": _compound(A4.parts),
        "dockhub-cabinet": _compound(sel(A2, (1, 2, 10, 14, 15))),
        "dockhub-bay": _compound([q for q in A1.parts if q["bom"] == 3 and q["group"] in ("liners", "cradles", "receptacles", "catches")]),
        "dockhub-canopy": _compound(sel(A2, (11, 12))),
        "dockhub-bay-vermiculite": _compound([q for q in A1.parts if q["group"] in ("liners", "cradles", "receptacles", "catches", "verm_trays", "verm_fill")]),
        "dockhub-site-pad": _compound([q for q in A1.parts if q["group"] in ("plinth", "pad", "anchors")]),
    }, A2


if __name__ == "__main__":
    from build123d import export_step, export_stl
    root = HERE.parents[0]
    (root / "step").mkdir(exist_ok=True)
    (root / "stl").mkdir(exist_ok=True)
    asm, A2 = assemblies()
    for name, shape in asm.items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"), tolerance=0.15, angular_tolerance=0.9)
        bb = shape.bounding_box()
        print(f"{name:26s} {bb.size.X:7.1f} x {bb.size.Y:7.1f} x {bb.size.Z:7.1f} mm")
    zr, zf, yf_, yr = canopy_heights()
    print(f"canopy: rear edge underside {zr:.0f} mm, front edge top {zf:.0f} mm, panel spans y {yf_:.0f} to {yr:.0f} mm")
    big = 5000.0
    outside = Pos(0, -P["D"] / 2 - big / 2, 0) * Box(big, big, big) + Pos(0, P["D"] / 2 + big / 2, 0) * Box(big, big, big)
    zs = []
    for q in A2.parts:
        if q["group"] in ("rails", "panel", "clamps"):
            for sol in q["shape"].solids():
                try:
                    r = sol & outside
                    if r is not None and r.volume > 1.0:
                        zs.append(r.bounding_box().min.Z)
                except Exception:
                    pass
    print(f"canopy lowest point outside the footprint {min(zs):.0f} mm")
    for k, v in key_heights().items():
        print(f"height {k}: {v} mm")
    from collections import defaultdict
    mass = defaultdict(float)
    for q in A2.parts:
        mass[q["bom"]] += cp.mass_kg(q)
    print("mass by BOM line (kg), two-bay prototype without the site pad and anchors:")
    for b in sorted(k for k in mass if k):
        print(f"  {b:2d}  {mass[b]:7.1f}")
    print(f"  total {sum(v for k, v in mass.items() if k not in (17, 18)):7.1f} kg (lines 17 and 18 are the site)")
