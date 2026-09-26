"""DockHub concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X along the cabinet width, Y front (-Y, street side where riders stand) to back (+Y),
Z up from the sidewalk. Units mm.
Each bay holds one SwapCell pack standing connector down, as in the SwapCell wall dock.
The pack envelope (340 x 90 x 80 mm, handle zone about 35 mm) follows the SwapCell
interface definition v0.2 in the SwapCell design precis.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def union(shapes):
    out = shapes[0]
    for s in shapes[1:]:
        out = out + s
    return out


# Cabinet envelope
W, D = 1000.0, 500.0            # width (X), depth (Y)
Z0, Z1 = 100.0, 1500.0          # body sits on a 100 mm plinth; roof at 1.5 m
T = 3.0                         # sheet thickness shown (massing; 1.5 mm steel in the BOM)
YF, YB = -D / 2, D / 2          # front and back faces
BAY_X = [-392.0, -196.0, 0.0, 196.0]   # bay centre lines, 196 mm pitch
BAY_HW = 86.0                   # half width of a bay opening
BZ0, BZ1 = 700.0, 1220.0        # bay opening, bottom and top (doors 520 mm tall)
TECH_Z1 = 680.0                 # top of the technical compartment

# 1 Cabinet body: hollow shell with four bay openings, and the floor between bays and tech space
body = box(-W / 2, W / 2, YF, YB, Z0, Z1) - box(-W / 2 + T, W / 2 - T, YF + T, YB - T, Z0 + T, Z1 - T)
for xc in BAY_X:
    body = body - box(xc - BAY_HW, xc + BAY_HW, YF - 1, YF + T + 1, BZ0 + 5, BZ1 - 5)
body = body + box(-W / 2 + T, W / 2 - T, YF + T, 140, TECH_Z1, BZ0)          # bay deck

# 2 Bay doors with solenoid locks, and 15 service door for the technical compartment
doors = union([box(xc - BAY_HW, xc + BAY_HW, YF - 6, YF - 2, BZ0 + 5, BZ1 - 5)
               + box(xc + 45, xc + 70, YF - 22, YF - 6, 940, 980) for xc in BAY_X])
service = box(-480, 480, YF - 6, YF - 2, 140, 660) + box(380, 420, YF - 22, YF - 6, 380, 420)

# 3 Bay compartments: steel liner box per bay with a cradle and SwapCell receptacle on the floor
liners, cradles = [], []
for xc in BAY_X:
    liners.append(box(xc - 90, xc + 90, YF + T, 140, BZ0, BZ1 + 10)
                  - box(xc - 87, xc + 87, YF, 137, BZ0 + 3, BZ1 + 7)
                  - box(xc - 30, xc + 30, 130, 145, BZ1 - 80, BZ1 - 20))         # vent port to plenum
    cradles.append(box(xc - 70, xc + 70, -70, 70, BZ0 + 3, BZ0 + 30)
                   + box(xc - 52, xc - 47, -45, 45, BZ0 + 30, BZ0 + 160)          # side guides
                   + box(xc + 47, xc + 52, -45, 45, BZ0 + 30, BZ0 + 160))
bays = union([l + c for l, c in zip(liners, cradles)])

# 4 SwapCell packs (reference), standing connector down in the cradles
PK_Z0 = BZ0 + 30
packs = union([box(xc - 45, xc + 45, -40, 40, PK_Z0, PK_Z0 + 340)
               + box(xc - 42, xc + 42, -12, 12, PK_Z0 + 340, PK_Z0 + 350)
               + box(xc - 42, xc - 30, -12, 12, PK_Z0 + 350, PK_Z0 + 375)
               + box(xc + 30, xc + 42, -12, 12, PK_Z0 + 350, PK_Z0 + 375)
               + box(xc - 42, xc + 42, -12, 12, PK_Z0 + 368, PK_Z0 + 380) for xc in BAY_X])

# 5 Chargers, 54.6 V 5 A, one per bay, on a rack in the technical compartment
rack = box(-470, 470, -60, 230, 380, 390)
chargers = union([box(xc - 80, xc + 80, -20, 180, 390, 460) for xc in (-345, -115, 115, 345)])

# 6 Dock controller (ESP32, four CAN channels, DC contactors, LTE-M modem) in a DIN box
controller = box(-450, -230, 140, 240, 150, 340)
# 13 MPPT solar charge controller
mppt = box(-190, -40, 170, 240, 150, 330)
# 8 Grid input: consumer unit with RCBO, per-charger breakers and surge protection
grid = box(230, 450, 150, 242, 150, 360)

# 7 Access panel column: NFC reader, display and status lights, operable parts below 1.22 m
access = box(310, 490, YF - 4, YF, 850, 1210)
display = box(330, 470, YF - 8, YF - 4, 1060, 1190)
nfc = box(355, 445, YF - 8, YF - 4, 900, 990)

# 9 Fire detection and suppression: aerosol generator along the plenum top, detector puck
fire = (Pos(-60, 200, 1420) * Rot(0, 90, 0) * Cylinder(38, 420)
        + Pos(250, 200, 1470) * Cylinder(45, 25))

# 10 Rear vent plenum wall and roof exhaust louver with fans
plenum = box(-W / 2 + T, W / 2 - T, 140, 150, BZ0, Z1 - T)
louver = box(-420, 420, 160, 240, Z1, Z1 + 70)
for i in range(9):
    x = -380 + i * 90
    louver = louver - box(x, x + 50, 150, 250, Z1 + 20, Z1 + 55)

# 12 Canopy frame: four posts on the roof and two sloping rails; 11 solar panel on top
TILT = 10.0                                   # degrees, front edge higher to shade the rider
PW, PD, PT = 1722.0, 1134.0, 35.0             # 400 W panel, long side along X
PY, PZ = -150.0, 2330.0                       # panel centre
tanT = math.tan(math.radians(TILT))
def under(y):
    """Underside height of the panel at depth y."""
    return PZ - PT / 2 / math.cos(math.radians(TILT)) - (y - PY) * tanT
panel = Pos(0, PY, PZ) * Rot(-TILT, 0, 0) * Box(PW, PD, PT)
RAIL_H = 40.0
rails = union([Pos(x, PY, PZ - PT / 2 - RAIL_H / 2 - 2) * Rot(-TILT, 0, 0) * Box(50, PD - 80, RAIL_H)
               for x in (-440, 440)])
posts = union([box(x - 25, x + 25, y - 25, y + 25, Z1, under(y) - RAIL_H - 5)
               for x in (-440, 440) for y in (-200, 200)])
canopy = rails + posts

# 14 Plinth and anchor frame
plinth = box(-W / 2 - 10, W / 2 + 10, YF - 10, YB + 10, 0, Z0) - box(-W / 2 + 60, W / 2 - 60, YF + 60, YB - 60, -1, Z0 + 1)

parts = [
    Part("Cabinet body, galvanized steel", body, "#D1D5DB", 1),
    Part("Bay doors with solenoid locks (4)", doors, "#0F766E", 2, (0, -1000, 0)),
    Part("Bay compartments with cradle and receptacle (4)", bays, "#9CA3AF", 3, (0, -450, 0)),
    Part("SwapCell packs (reference, 4)", packs, "#D4A017", 4, (0, -250, 1050)),
    Part("Chargers, 54.6 V 5 A (4)", chargers, "#C2410C", 5, (0, -520, -60)),
    Part("Charger rack", rack, "#6B7280", None, (0, -520, -60)),
    Part("Dock controller (ESP32, CAN, LTE-M)", controller, "#15803D", 6, (-800, 300, 750)),
    Part("Access panel (NFC reader, display)", access, "#1F2937", 7, (700, -300, 0)),
    Part("Display", display, "#38BDF8", None, (700, -300, 0)),
    Part("NFC reader", nfc, "#E5E7EB", None, (700, -300, 0)),
    Part("Grid input and protection", grid, "#991B1B", 8, (900, 0, -40)),
    Part("Fire detection and aerosol suppression", fire, "#DC2626", 9, (0, 500, 350)),
    Part("Vent plenum and roof exhaust louver", plenum + louver, "#4B5563", 10, (0, 900, 250)),
    Part("Solar panel, 400 W", panel, "#1E3A8A", 11, (0, 0, 1900)),
    Part("Canopy frame", canopy, "#374151", 12, (0, 0, 1500)),
    Part("MPPT solar charge controller", mppt, "#B45309", 13, (1500, -450, -350)),
    Part("Plinth and anchor frame", plinth, "#6B7280", 14, (0, 0, -350)),
    Part("Service door", service, "#E5E7EB", 15, (0, -1100, -150)),
]

# Street context for the hero: sidewalk, curb and roadway edge
context = [
    Part("Sidewalk", box(-1400, 2100, -1300, 800, -150, 0), "#E5E7EB"),
    Part("Curb", box(-1400, 2100, -1450, -1300, -300, 0), "#C8CDD3"),
    Part("Roadway", box(-1400, 2100, -2100, -1450, -300, -150), "#6B7280"),
]

render_all(
    parts, project="DockHub", title="Street battery swap station concept", dwg_no="DKH-DWG-010",
    key_figures=["4 SwapCell bays; about 30 s per swap (estimate)",
                 "Charge 20 to 80 % in about 1.2 h, full in about 2.3 h",
                 "Peak grid draw about 1.25 kW, single phase (est.)",
                 "20 swaps a day: about 10.1 kWh in, 8.0 kWh to riders (est.)",
                 "400 W solar canopy: about 13 % of that energy (est.)",
                 "About 1.0 x 0.5 m footprint, 2.45 m to canopy top"],
    context=context, cut_exclude=("Solar panel, 400 W", "Canopy frame"),
    flow={"title": "daily energy at 20 swaps a day (all values are estimates)", "unit": "kWh",
          "stages": [("Grid 8.8 + solar 1.3", 10.1), ("Chargers and MPPT", 9.4),
                     ("Pack terminals", 8.5), ("Stored, to riders", 8.0)],
          "losses": [(0, "Cabinet loads (est.)", 0.7), (1, "Charger loss (est.)", 0.9),
                     (2, "Cell charge loss (est.)", 0.5)]},
)
