"""DockHub concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X along the cabinet width, Y front (-Y, street side where riders stand) to back (+Y),
Z up from the sidewalk. Units mm. Geometry comes from cad/src/model.py, so the media match
the STEP files and drawing DKH-DWG-001. The media show the full four-bay fit with three
resident packs and one empty bay; the first prototype fits bays 1 and 2 (DKH-DDR-001).
Flow values are printed by docs/04-calcs/sizing.py (DKH-CAL-001).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build123d import Box, Pos
from concept import Part, render_all
from model import PARAMS, build_parts

parts = [Part(n, shape, colour, bom, ex) for n, shape, colour, bom, ex in build_parts(fitted=PARAMS["n_bays"])]


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


# Street context for the hero: sidewalk, curb and roadway edge
context = [
    Part("Sidewalk", box(-1400, 2100, -1300, 800, -150, 0), "#E5E7EB"),
    Part("Curb", box(-1400, 2100, -1450, -1300, -300, 0), "#C8CDD3"),
    Part("Roadway", box(-1400, 2100, -2100, -1450, -300, -150), "#6B7280"),
]

render_all(
    parts, project="DockHub", title="Street battery swap station concept", dwg_no="DKH-DWG-010", date="2026-09-25",
    key_figures=["4 SwapCell v0.3 bays, 3 packs resident; swap about 31 s",
                 "Charge 20 to 80 % in 1.2 h, 15 to 100 % in 2.0 h",
                 "Peak grid draw 1.25 kW, single phase (est.)",
                 "20 swaps a day: 8.8 kWh grid, 0.77 kWh solar (est.)",
                 "Solar 9.3 % of charging energy (R6 not met)",
                 "1.0 x 0.5 m footprint, 2.45 m to canopy top"],
    context=context, cut_exclude=("Solar panel, 400 W", "Canopy frame"),
    flow={"title": "daily energy at 20 swaps a day, four bays (estimates, DKH-CAL-001)", "unit": "kWh",
          "stages": [("Grid 8.76 + solar 0.77", 9.53), ("Chargers and MPPT", 8.81),
                     ("Pack terminals", 7.98), ("Stored, to riders", 7.58)],
          "losses": [(0, "Loads", 0.72), (1, "Conversion", 0.84),
                     (2, "Cells", 0.40)]},
)
