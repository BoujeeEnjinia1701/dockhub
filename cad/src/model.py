"""DockHub parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl, prints the main envelopes and key heights,
and runs a clash check between the main parts.

Massing-plus detail: correct interfaces (SwapCell interface v0.3 pack envelope with plug,
handle zone and latch pawl; cradle, side guides, class D latch catch and blind-mate receptacle
in each bay) and main dimensions; not fabrication detail.

Axes: X along the cabinet width, Y front (-Y, street side where riders stand) to back (+Y),
Z up from the sidewalk. Units mm. Each pack stands connector down, lid face (wake button)
toward the rider and back face (latch pawl) toward the plenum, as in the SwapCell wall dock.

Configurations (DKH-DDR-001 item 1): the cabinet is built for four bays. The first prototype
fits bays 1 and 2 (PARAMS["bays_fitted"] = 2); bays 3 and 4 are closed with blank plates.
The concept media show the full four-bay fit.
"""
import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Cabinet (DKH-PRC-001 v0.3, R10, R13)
    "W": 1000.0, "D": 500.0,         # footprint, X by Y; the plinth is flush with the body
    "plinth_h": 100.0,               # steel channel plinth; body sits on it
    "roof_z": 1500.0,                # top of the body
    "sheet_t": 1.5,                  # galvanized steel sheet (R10)
    "tech_z1": 680.0,                # top of the technical compartment
    # Bays (R11): four in one row at hand height
    "n_bays": 4, "bays_fitted": 2,
    "bay_pitch": 196.0, "bay_open_w": 172.0,
    "bay_z0": 700.0, "bay_z1": 1220.0,   # bay opening, bottom and top (door 510 mm tall)
    "liner_y1": 110.0,               # back of the bay liners; plenum wall behind
    "plenum_t": 10.0,
    "cradle_h": 30.0,                # cradle shelf; pack connector face rests on its top
    "guide_h": 130.0,                # side guides above the cradle
    "door_handle_z": (940.0, 980.0),
    # SwapCell interface v0.3 envelope (SWC-PRC-001 v0.3)
    "pack_l": 340.0, "pack_w": 90.0, "pack_d": 80.0,
    "plug_w": 56.0, "plug_d": 34.0, "plug_h": 18.0, "plug_offset": 8.0,
    "handle_w": 84.0, "handle_d": 22.0, "handle_h": 35.0,
    "latch_w": 36.0, "latch_from_top": 45.0, "latch_proud": 10.0, "latch_h": 24.0,
    "guide_clear": 1.0,
    # Access panel (R11): reader and display
    "access_x": (310.0, 490.0), "access_z": (850.0, 1210.0),
    "reader_z": (900.0, 990.0), "display_z": (1060.0, 1190.0),
    # Canopy (R6, R13, R15): 400 W panel, long side along X
    "panel": (1722.0, 1134.0, 35.0), "tilt_deg": 10.0,
    "panel_y": -150.0, "panel_z": 2330.0,     # panel centre
    "post": 50.0, "post_x": 460.0, "post_y": 200.0, "rail_h": 40.0,
    # Plinth anchors (R15): four M12 at this inset from the plinth edges
    "anchor_inset": 60.0,
}


def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _union(shapes):
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
    return p["bay_z0"] + p["cradle_h"]


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
        "bay opening top": p["bay_z1"],
    }


def _pack(xc, p):
    """SwapCell v0.3 reference pack standing connector down at bay centre xc."""
    from build123d import Pos  # noqa: F401
    b = _box
    z0 = pack_z0(p); z1 = z0 + p["pack_l"]
    hw, hd = p["pack_w"] / 2, p["pack_d"] / 2
    body = b(xc - hw, xc + hw, -hd, hd, z0, z1)
    yc = p["plug_offset"]                      # plug offset toward the back (latch) face, +Y
    plug = b(xc - p["plug_w"] / 2, xc + p["plug_w"] / 2, yc - p["plug_d"] / 2, yc + p["plug_d"] / 2,
             z0 - p["plug_h"], z0)
    hh = p["handle_h"]
    handle = b(xc - p["handle_w"] / 2, xc + p["handle_w"] / 2, -p["handle_d"] / 2, p["handle_d"] / 2, z1, z1 + hh) \
        - b(xc - p["handle_w"] / 2 + 11, xc + p["handle_w"] / 2 - 11, -p["handle_d"], p["handle_d"], z1 - 1, z1 + 25)
    zl = z1 - p["latch_from_top"]
    pawl = b(xc - p["latch_w"] / 2, xc + p["latch_w"] / 2, hd, hd + p["latch_proud"],
             zl - p["latch_h"] / 2, zl + p["latch_h"] / 2)
    return body + plug + handle + pawl


def build_parts(p=PARAMS, fitted=None):
    """Return a list of (name, shape, colour, bom_item, explode_offset).

    fitted: number of bays fitted (default p["bays_fitted"]); unfitted bays get blank plates.
    """
    from build123d import Cylinder, Pos, Rot
    b = _box
    fitted = p["bays_fitted"] if fitted is None else fitted
    W, D, t = p["W"], p["D"], p["sheet_t"]
    Z0, Z1 = p["plinth_h"], p["roof_z"]
    YF, YB = -D / 2, D / 2
    BZ0, BZ1 = p["bay_z0"], p["bay_z1"]
    HW = p["bay_open_w"] / 2
    xs = bay_x(p)
    fit = xs[:fitted]
    blank = xs[fitted:]
    LY1 = p["liner_y1"]
    gc = p["guide_clear"]

    # 1 Cabinet body: hollow shell with four bay openings, bay deck, blank plates on unfitted bays
    body = b(-W / 2, W / 2, YF, YB, Z0, Z1) - b(-W / 2 + t, W / 2 - t, YF + t, YB - t, Z0 + t, Z1 - t)
    for xc in xs:
        body = body - b(xc - HW, xc + HW, YF - 1, YF + t + 1, BZ0 + 5, BZ1 - 5)
    body = body - b(-480, 480, YF - 1, YF + t + 1, 140, 660)                         # service opening
    body = body + b(-W / 2 + t, W / 2 - t, YF + t, LY1, BZ0 - t, BZ0)                # bay deck (tech space below)
    for xc in blank:
        body = body + b(xc - HW - 4, xc + HW + 4, YF - 3, YF, BZ0 + 1, BZ1 - 1)      # blank plate

    # 2 Bay doors with solenoid locks and pull handles (fitted bays)
    hz0, hz1 = p["door_handle_z"]
    doors = _union([b(xc - HW, xc + HW, YF - 6, YF - 2, BZ0 + 5, BZ1 - 5)
                    + b(xc + 45, xc + 70, YF - 22, YF - 6, hz0, hz1) for xc in fit])

    # 3 Bay compartments: steel liner with vent port, cradle, side guides, class D catch,
    #   blind-mate receptacle (10 kOhm INTERLOCK coding resistor inside, item W)
    pz0 = pack_z0(p)
    hw, hd = p["pack_w"] / 2, p["pack_d"] / 2
    bays = []
    for xc in fit:
        liner = b(xc - 90, xc + 90, YF + t, LY1, BZ0, BZ1 + 10) \
            - b(xc - 90 + t, xc + 90 - t, YF, LY1 - t, BZ0 + t, BZ1 + 10 - t) \
            - b(xc - 30, xc + 30, LY1 - t - 1, LY1 + 1, BZ1 - 80, BZ1 - 20)            # vent port to plenum
        yc = p["plug_offset"]
        cradle = b(xc - 75, xc + 75, -75, 75, BZ0 + t, pz0) \
            - b(xc - p["plug_w"] / 2 - 1, xc + p["plug_w"] / 2 + 1, yc - p["plug_d"] / 2 - 1,
                yc + p["plug_d"] / 2 + 1, pz0 - p["plug_h"] - 1, pz0 + 1)             # receptacle pocket
        receptacle = b(xc - p["plug_w"] / 2 - 8, xc + p["plug_w"] / 2 + 8, yc - p["plug_d"] / 2 - 8,
                       yc + p["plug_d"] / 2 + 8, BZ0 + t, pz0 - p["plug_h"] - 1)
        guides = b(xc - hw - gc - 5, xc - hw - gc, -45, 45, pz0, pz0 + p["guide_h"]) \
            + b(xc + hw + gc, xc + hw + gc + 5, -45, 45, pz0, pz0 + p["guide_h"])
        zl = pz0 + p["pack_l"] - p["latch_from_top"]
        yb = hd + p["latch_proud"] + 1
        catch_post = b(xc - 30, xc + 30, yb + 8, yb + 14, pz0, zl + 30)
        catch = b(xc - 25, xc + 25, yb, yb + 8, zl + p["latch_h"] / 2 + 1, zl + p["latch_h"] / 2 + 9)
        bays.append(liner + cradle + receptacle + guides + catch_post + catch)
    bays = _union(bays)

    # 4 SwapCell packs (reference): one in each fitted bay except the empty bay (last fitted bay)
    packs = _union([_pack(xc, p) for xc in fit[:-1]]) if fitted > 1 else None

    # 5 Chargers, 54.6 V 5 A, one per fitted bay, on a rack in the technical compartment
    rack = b(-470, 470, -60, 230, 380, 390)
    cx = [-345.0, -115.0, 115.0, 345.0][:fitted]
    chargers = _union([b(x - 80, x + 80, -20, 180, 390, 460) for x in cx])

    # 6 Dock controller (ESP32, four CAN channels, contactors, LTE-M) in a DIN box
    controller = b(-450, -230, 140, 240, 150, 340)
    # 7 Access panel column with NFC reader and display
    ax0, ax1 = p["access_x"]
    access = b(ax0, ax1, YF - 4, YF, *p["access_z"])
    display = b(ax0 + 20, ax1 - 20, YF - 8, YF - 4, *p["display_z"])
    nfc = b(ax0 + 45, ax1 - 45, YF - 8, YF - 4, *p["reader_z"])
    # 8 Grid input and protection
    grid = b(230, 450, 150, 242, 150, 360)
    # 9 Fire detection and suppression: aerosol generator along the plenum top, detector puck
    fire = Pos(-60, 200, 1420) * Rot(0, 90, 0) * Cylinder(38, 420) + Pos(250, 200, 1465) * Cylinder(45, 25)
    # 10 Rear vent plenum wall, two fans under the roof and the exhaust louver
    plenum = b(-W / 2 + t, W / 2 - t, LY1, LY1 + p["plenum_t"], BZ0, Z1 - t)
    fans = _union([Pos(x, 185, Z1 - t - 13) * Cylinder(60, 25) for x in (-380, 380)])
    louver = b(-420, 420, 160, 240, Z1, Z1 + 70)
    for i in range(9):
        x = -380 + i * 90
        louver = louver - b(x, x + 50, 150, 250, Z1 + 20, Z1 + 55)
    # 13 MPPT solar charge controller
    mppt = b(-190, -40, 170, 240, 150, 330)

    # 11 Solar panel and 12 canopy frame (posts on the roof frame, two tilted rails)
    pw, pd, pt = p["panel"]
    a = p["tilt_deg"]
    PY, PZ = p["panel_y"], p["panel_z"]
    tanA = math.tan(math.radians(a))

    def under(y):
        return PZ - pt / 2 / math.cos(math.radians(a)) - (y - PY) * tanA

    panel = Pos(0, PY, PZ) * Rot(-a, 0, 0) * b(-pw / 2, pw / 2, -pd / 2, pd / 2, -pt / 2, pt / 2)
    rh = p["rail_h"]
    rails = _union([Pos(x, PY, PZ - pt / 2 - rh / 2 - 2) * Rot(-a, 0, 0) * b(-25, 25, -(pd - 80) / 2, (pd - 80) / 2, -rh / 2, rh / 2)
                    for x in (-p["post_x"], p["post_x"])])
    s = p["post"] / 2
    posts = _union([b(x - s, x + s, y - s, y + s, Z1, under(y) - rh - 5)
                    for x in (-p["post_x"], p["post_x"]) for y in (-p["post_y"], p["post_y"])])

    # 14 Plinth and anchor frame, flush with the body (R13), four M12 anchor points
    ai = p["anchor_inset"]
    plinth = b(-W / 2, W / 2, YF, YB, 0, Z0) - b(-W / 2 + 60, W / 2 - 60, YF + 60, YB - 60, -1, Z0 + 1)
    for x in (-W / 2 + ai, W / 2 - ai):
        for y in (YF + ai / 2, YB - ai / 2):
            plinth = plinth - Pos(x, y, Z0 / 2) * Cylinder(7, Z0 + 2)
    # 15 Service door
    service = b(-480, 480, YF - 6, YF - 2, 140, 660) + b(380, 420, YF - 22, YF - 6, 380, 420)

    parts = [
        ("Cabinet body, galvanized steel", body, "#D1D5DB", 1, (0, 0, 0)),
        ("Bay doors with solenoid locks", doors, "#0F766E", 2, (0, -1000, 0)),
        ("Bay compartments with cradle and receptacle", bays, "#9CA3AF", 3, (0, -450, 0)),
    ]
    if packs is not None:
        parts.append(("SwapCell packs (reference)", packs, "#D4A017", 4, (0, -250, 1050)))
    parts += [
        ("Chargers, 54.6 V 5 A", chargers, "#C2410C", 5, (0, -520, -60)),
        ("Charger rack", rack, "#6B7280", None, (0, -520, -60)),
        ("Dock controller (ESP32, CAN, LTE-M)", controller, "#15803D", 6, (-800, 300, 750)),
        ("Access panel (NFC reader, display)", access, "#1F2937", 7, (700, -300, 0)),
        ("Display", display, "#38BDF8", None, (700, -300, 0)),
        ("NFC reader", nfc, "#E5E7EB", None, (700, -300, 0)),
        ("Grid input and protection", grid, "#991B1B", 8, (900, 0, -40)),
        ("Fire detection and aerosol suppression", fire, "#DC2626", 9, (0, 500, 350)),
        ("Vent plenum, fans and roof louver", plenum + fans + louver, "#4B5563", 10, (0, 900, 250)),
        ("Solar panel, 400 W", panel, "#1E3A8A", 11, (0, 0, 1900)),
        ("Canopy frame", rails + posts, "#374151", 12, (0, 0, 1500)),
        ("MPPT solar charge controller", mppt, "#B45309", 13, (1500, -450, -350)),
        ("Plinth and anchor frame", plinth, "#6B7280", 14, (0, 0, -350)),
        ("Service door", service, "#E5E7EB", 15, (0, -1100, -150)),
    ]
    return parts


def assemblies(parts=None, parts4=None):
    from build123d import Compound
    parts = parts or build_parts()
    parts4 = parts4 or build_parts(fitted=PARAMS["n_bays"])
    by = {bom: s for _, s, _, bom, _ in parts if bom}
    return {
        "dockhub-assembly": Compound([s for _, s, _, _, _ in parts]),
        "dockhub-assembly-4-bays": Compound([s for _, s, _, _, _ in parts4]),
        "dockhub-cabinet": Compound([by[1], by[10], by[14], by[15]]),
        "dockhub-bay": build_parts(fitted=1)[2][1],
        "dockhub-canopy": Compound([by[11], by[12]]),
    }


if __name__ == "__main__":
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    parts4 = build_parts(fitted=PARAMS["n_bays"])
    for name, shape in assemblies(parts, parts4).items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"))
        bb = shape.bounding_box()
        print(f"{name:26s} {bb.size.X:7.1f} x {bb.size.Y:7.1f} x {bb.size.Z:7.1f} mm")
    zr, zf, yf, yr = canopy_heights()
    print(f"canopy: rear edge underside {zr:.0f} mm, front edge top {zf:.0f} mm, panel spans y {yf:.0f} to {yr:.0f} mm")
    canopy = [s for n, s, _, bom, _ in parts if bom in (11, 12)]
    zmin = min(c.bounding_box().min.Z for c in canopy)
    # lowest canopy point outside the cabinet footprint (over the sidewalk)
    from build123d import Box, Pos
    big = 5000.0
    outside = Pos(0, -PARAMS["D"] / 2 - big / 2, 0) * Box(big, big, big) + Pos(0, PARAMS["D"] / 2 + big / 2, 0) * Box(big, big, big)
    zmin_out = min((c & outside).bounding_box().min.Z for c in canopy)
    print(f"canopy lowest point {zmin:.0f} mm (over the roof); lowest point outside the footprint {zmin_out:.0f} mm")
    for k, v in key_heights().items():
        print(f"height {k}: {v} mm")
    # Clash check between main parts (volume of pairwise intersections)
    for label, ps in (("2 bays fitted", parts), ("4 bays fitted", parts4)):
        worst = 0.0
        for i in range(len(ps)):
            for j in range(i + 1, len(ps)):
                v = (ps[i][1] & ps[j][1]).volume
                if v > 1.0:
                    print(f"clash ({label}) {ps[i][0]} / {ps[j][0]}: {v:.0f} mm3")
                    worst = max(worst, v)
        print(f"clash check ({label}): " + ("none" if worst == 0 else "see above"))
    vols = {n: s.volume for n, s, _, _, _ in parts4}
    print(f"steel sheet volume in body {vols['Cabinet body, galvanized steel'] / 1e6:.2f} L, "
          f"bays (4) {vols['Bay compartments with cradle and receptacle'] / 1e6:.2f} L")
