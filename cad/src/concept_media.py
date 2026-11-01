"""DockHub concept media (TRL 3), generated from the kit 1.9 model.

Run from the repo root:  python cad/src/concept_media.py [all|hero|cutaway|exploded|flow|web|blueprint ...]
With no argument it draws everything with .kit/concept.py render_all. The model has about 540 solids, so
the parts are grouped by BOM line (one picture part per line, fasteners and welds with the line they belong
to) to keep the renderers quick. Geometry comes from cad/src/model.py components("A", fitted=4); flow values
are printed by docs/04-calcs/sizing.py (DKH-CAL-001).

Axes: X along the cabinet width, Y front (-Y, street side where riders stand) to back (+Y), Z up from the
sidewalk. Units mm. The media show the full four-bay fit with three resident packs and one empty bay; the
first prototype fits bays 1 and 2 (DKH-DDR-001). Label: CONCEPT, NOT FOR FABRICATION.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(Path(__file__).resolve().parent)]
from build123d import Box, Compound, Pos  # noqa: E402
import concept as K  # noqa: E402
from concept import Part  # noqa: E402
import model as M  # noqa: E402

MD = ROOT / "media"


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _bom_names():
    out = {}
    for r in csv.DictReader((ROOT / "bom/bom.csv").open()):
        n, _, name = r["item"].partition(" ")
        out[int(n)] = name
    return out


def parts():
    """One Part per BOM line (parts without a line are grouped by their model group), four-bay fit."""
    names = _bom_names()
    groups = {}
    for q in M.components(M.CHOSEN, fitted=M.PARAMS["n_bays"], site=False):
        if q["kind"] == "context":
            continue
        key = ("bom", q["bom"]) if q["bom"] else ("grp", q["group"])
        groups.setdefault(key, []).append(q)
    out = []
    for (kind, k), qs in groups.items():
        big = max(qs, key=lambda q: q["shape"].volume)
        name = names.get(k, big["name"]) if kind == "bom" else big["name"]
        out.append(Part(name, Compound(children=[q["shape"] for q in qs]), big["color"],
                        k if kind == "bom" else None, tuple(big["explode"])))
    return out


# Street context for the hero: sidewalk, curb and roadway edge
context = [
    Part("Sidewalk", box(-1400, 2100, -1300, 800, -150, 0), "#E5E7EB"),
    Part("Curb", box(-1400, 2100, -1450, -1300, -300, 0), "#C8CDD3"),
    Part("Roadway", box(-1400, 2100, -2100, -1450, -300, -150), "#6B7280"),
]

KEY_FIGURES = ["4 SwapCell v0.3 bays, 3 packs resident; swap about 31 s",
               "Charge 20 to 80 % in 1.2 h, 15 to 100 % in 2.0 h",
               "Peak grid draw 1.25 kW, single phase (est.)",
               "20 swaps a day: 8.8 kWh grid, 0.77 kWh solar (est.)",
               "Solar 9.3 % of charging energy (R6 met at about 9 %)",
               "1.0 x 0.5 m footprint, 2.45 m to canopy top"]
FLOW = {"title": "daily energy at 20 swaps a day, four bays (estimates, DKH-CAL-001)", "unit": "kWh",
        "stages": [("Grid 8.76 + solar 0.77", 9.53), ("Chargers and MPPT", 8.81),
                   ("Pack terminals", 7.98), ("Stored, to riders", 7.58)],
        "losses": [(0, "Loads", 0.72), (1, "Conversion", 0.84), (2, "Cells", 0.40)]}


CUT_EXCLUDE = tuple(n for k, n in _bom_names().items() if "anopy" in n or "olar" in n)


def everything():
    return K.render_all(parts(), project="DockHub", title="Street battery swap station concept", dwg_no="DKH-DWG-010",
                        date="2026-10-31", rev="P3", key_figures=KEY_FIGURES, context=context,
                        cut_exclude=CUT_EXCLUDE, flow=FLOW)


def cutaway():
    """Front half removed, cut solid by solid (a boolean on the grouped compounds needs over 6 GB for 540 solids)."""
    import gc
    cutter = Pos(0, 2000, 0) * Box(6000, 4000, 6000)          # keeps y >= 0
    names = _bom_names()
    groups = {}
    for q in M.components(M.CHOSEN, fitted=M.PARAMS["n_bays"], site=False):
        if q["kind"] == "context" or (q["bom"] in (11, 12)):
            continue
        try:
            sh = q["shape"] & cutter
        except Exception:
            continue
        if sh is None or sh.volume < 1e-3:
            continue
        groups.setdefault(q["bom"], []).append((sh, q))
        gc.collect()
    ps = []
    for bom, lst in groups.items():
        big = max(lst, key=lambda t: t[1]["shape"].volume)[1]
        ps.append(Part(names.get(bom, big["name"]), Compound(children=[t[0] for t in lst]), big["color"], bom, (0, 0, 0)))
    return K._render(ps, MD / "cutaway.png", azim=-90, elev=18, title="DockHub: cutaway",
                     note="Front half removed; seen from the front and above, 18 deg elevation")


def web():
    """The 3D viewer model. Angular deflection 0.6 rad (not the kit's 0.35) keeps model.glb under about 20 MB: the D3 model has
    about 400 fasteners and the kit's setting gives 30 MB."""
    import build123d
    kit = build123d.export_gltf
    build123d.export_gltf = lambda shape, path, **kw: kit(shape, path, **{**kw, "linear_deflection": 0.2, "angular_deflection": 0.6})
    try:
        return K.export_web_model(parts(), "media", title="DockHub: street battery swap station")
    finally:
        build123d.export_gltf = kit


def blueprint():
    """The blueprint concept sheet (same layout as concept.render_all)."""
    from drawing import Sheet, project_views
    ps = parts()
    work = MD / "_views"
    views = project_views(Compound(children=[p.shape for p in ps]), work)
    shown = K.with_scale_figure(ps + context)
    views["iso"] = project_views(Compound(children=[p.shape for p in shown]), MD / "_views_fig")["iso"]
    sh = Sheet(project="DockHub", title="Street battery swap station concept", dwg_no="DKH-DWG-010", rev="P3", author="Amish Chadha",
               date="2026-10-31", theme="blueprint", material="Massing model for concept communication",
               revisions=[("P3", "Concept sheet", "2026-10-31", "AC")])
    sh.add_ortho(views)
    sh.add_svg(views["iso"], 276, 32, 140, 118, label="Isometric view", sublabel="Not to scale; figure is a 1.75 m person")
    sh.add_notes("Key figures", KEY_FIGURES, x=276, y=168, width=140)
    sh.save(MD / "concept-blueprint")
    import shutil
    for d in ("_views", "_views_fig"):
        shutil.rmtree(MD / d, ignore_errors=True)
    return MD / "concept-blueprint.png"


if __name__ == "__main__":
    fns = {"cutaway": cutaway, "blueprint": blueprint,
           "hero": lambda: K._render(K.with_scale_figure(parts() + context), MD / "hero.png", title="DockHub",
                                     note="Seen from the front right and above. Grey figure: 1.75 m person for scale"),
           "exploded": lambda: K._render(parts(), MD / "exploded.png", offsets=True, labels=True, title="DockHub: exploded view",
                                         note="Seen from the front right and above; numbers match bom/bom.csv"),
           "flow": lambda: K.flow_diagram(FLOW["stages"], MD / "flow.png", "DockHub: " + FLOW["title"], "kWh", FLOW["losses"]),
           "web": web,
           "all": everything}
    for w in sys.argv[1:] or ["all"]:
        print(w, "->", fns[w]())
