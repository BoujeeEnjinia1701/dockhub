"""DockHub general arrangement drawing DKH-DWG-001 (Rev P3, constructable design DKH-DDR-003; site pad and anchors).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/DKH-DWG-001.svg, .pdf and .png from the parametric model, in the
first-prototype fit (bays 1 and 2 fitted, bays 3 and 4 blanked; DKH-DDR-001 item 1).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, assemblies, build_parts, canopy_heights, pack_z0  # noqa: E402

parts = build_parts()
asm = assemblies(parts)["dockhub-assembly"]
work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)
zr, zf, _, _ = canopy_heights()
pz = pack_z0()

s = Sheet(project="DockHub", title="General arrangement, first prototype (2 of 4 bays)", dwg_no="DKH-DWG-001",
          rev="P3", author="Amish Chadha", date="2026-10-02", concept=True,
          material="1.5 mm galvanized steel, powder coat. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA, SwapCell interface v0.3 (DKH-CAL-001)", "2026-09-25", "AC"),
                     ("P2", "Constructable design (DKH-DDR-003)", "2026-10-01", "AC"),
                     ("P3", "Anchors and site pad chosen; socket holes in plinth", "2026-10-02", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 37, 140, 78, label="Isometric view", sublabel="Not to scale")
s.add_notes("Key dimensions and interfaces (mm)", [
    f"Cabinet {P['W']:.0f} x {P['D']:.0f} x {P['roof_z']:.0f}, riveted 1.5 mm panels",
    "  on a welded 100 x 50 channel plinth",
    f"Canopy: 400 W panel at {P['tilt_deg']:.0f} deg; top {zf:.0f}, lowest 2171;",
    "  posts bolt through the roof into 40 x 40 angle beams",
    f"4 bays at {P['bay_pitch']:.0f} pitch, openings {P['bay_open_w']:.0f} x {P['open_z'][1] - P['open_z'][0]:.0f}",
    f"  bays 1 and 2 fitted; 3 and 4 blank plates",
    f"Pack: SwapCell v0.3, 340 x 90 x 80, 393 overall,",
    f"  connector down on cradle at {pz:.0f}; handle top {pz + 375:.0f}",
    "Receptacle: 10 kOhm INTERLOCK coding resistor;",
    "  class D catch; one CAN channel per bay",
    f"Operable parts {pz:.0f} to {pz + 375:.0f} above the sidewalk",
    "Grid: one 120 V 15 A or 230 V 10 A circuit, RCBO",
    "Anchors: 4 x M12 wedge, 3.8 kN design tension each,",
    "  into a 1,400 x 1,100 x 300 pad (site; BOM 17, 18)",
    "Mass about 217 kg without packs (est.)",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=131, width=140)
s.save(ROOT / "cad/drawings/DKH-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/DKH-DWG-001.svg, .pdf, .png")
