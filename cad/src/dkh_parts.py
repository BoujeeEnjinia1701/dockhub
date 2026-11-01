"""DockHub repo-specific CAD helpers (kit 1.9 parts library extensions; STANDARDS section 24).

These sit beside .kit/cad_parts.py and add what a sheet metal cabinet needs:

    bx, cx, cy, cz   box by extents and cylinders along X, Y or Z
    fuse             union of shapes into one solid
    slab             flat plate on an axis-aligned plane with rounded corners, rectangular cut-outs and round holes
    bead             a fillet weld bead along any axis with its two legs along any two directions
    rivet            a 4 mm blind rivet (dome head, shank, set tail) pointing along any axis
    piano_hinge      a continuous hinge: leaves and barrel in one solid, plus its pin
    fan_120          a 120 mm axial fan: frame, hub and blades
    plug             helper to drill several round holes at once

All sizes in millimetres. Axes as model.py: X across the cabinet, Y front (-Y) to back (+Y), Z up.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import (Box, Cylinder, Compound, Location, Plane, Polygon, Pos, Rot, Sketch, RectangleRounded, Circle,  # noqa: E402
                       Cone, extrude)
from cad_parts import break_edges  # noqa: E402


def bx(x0, x1, y0, y1, z0, z1):
    """Box by extents."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def cz(r, z0, z1, x, y):
    z0, z1 = min(z0, z1), max(z0, z1)
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def cy(r, y0, y1, x, z):
    y0, y1 = min(y0, y1), max(y0, y1)
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)


def cx(r, x0, x1, y, z):
    x0, x1 = min(x0, x1), max(x0, x1)
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def fuse(shapes):
    """One solid from several touching or overlapping shapes."""
    shapes = [s for s in shapes if s is not None]
    out = shapes[0]
    for s in shapes[1:]:
        out = out + s
    return out


def drill(shape, cutters):
    """Cut a list of tool shapes from a shape in one operation."""
    cutters = [c for c in cutters if c is not None]
    if not cutters:
        return shape
    return shape - Compound(cutters) if len(cutters) > 1 else shape - cutters[0]


# the rotation that turns a local +Z axis to point along a global unit direction
_ROT = {(0, 0, 1): (0, 0, 0), (0, 0, -1): (180, 0, 0), (1, 0, 0): (0, 90, 0), (-1, 0, 0): (0, -90, 0),
        (0, 1, 0): (-90, 0, 0), (0, -1, 0): (90, 0, 0)}


def pointing(shape, xyz, direction):
    """Place a shape built along +Z so that its +Z points along 'direction' (a unit axis), at xyz."""
    return Pos(*xyz) * Rot(*_ROT[tuple(int(v) for v in direction)]) * shape


def frame(xyz, direction):
    """Location that puts a part built along +Z (top face at z = 0) at xyz with its +Z along a unit axis."""
    return Pos(*xyz) * Rot(*_ROT[tuple(int(v) for v in direction)])


def slab(axis, c0, c1, a0, a1, b0, b1, holes=(), cutouts=(), r=3.0, edge=0.4):
    """Flat plate whose thickness runs along 'axis' from c0 to c1. The in-plane axes are (x, y) for a z plate,
    (x, z) for a y plate and (y, z) for an x plate. holes: [(a, b, diameter)], cutouts: [(a0, a1, b0, b1, radius)].
    Corners rounded to r, edges broken by 'edge' (0 to leave sharp)."""
    t = c1 - c0
    w, h = a1 - a0, b1 - b0
    sk = Sketch() + Pos((a0 + a1) / 2, (b0 + b1) / 2) * RectangleRounded(w, h, max(0.05, min(r, min(w, h) / 2 - 0.01)))
    for ca0, ca1, cb0, cb1, cr in cutouts:
        cw, ch = ca1 - ca0, cb1 - cb0
        sk -= Pos((ca0 + ca1) / 2, (cb0 + cb1) / 2) * RectangleRounded(cw, ch, max(0.05, min(cr, min(cw, ch) / 2 - 0.01)))
    for a, b, d in holes:
        sk -= Pos(a, b) * Circle(d / 2)
    s = extrude(sk, t)                      # z from 0 to t, in-plane axes x and y
    if edge:
        s = break_edges(s, min(edge, t / 3))
    if axis == "z":
        return Pos(0, 0, c0) * s
    if axis == "y":                         # thickness toward -Y from c1; local y -> +Z
        return Location(Plane(origin=(0, c1, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0))) * s
    if axis == "x":                         # thickness toward +X from c0; local x -> +Y, local y -> +Z
        return Location(Plane(origin=(c0, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))) * s
    raise ValueError(axis)


def bead(origin, along, length, leg, d1, d2):
    """Fillet weld bead (triangular section) from 'origin' along the unit vector 'along' for 'length', with its two
    legs of size 'leg' along the unit vectors d1 and d2, both at right angles to 'along'. Place it in the joint
    corner: origin on the line where the two faces meet, d1 and d2 pointing away from the corner along the faces."""
    ax = tuple(float(v) for v in along)
    d1 = tuple(float(v) for v in d1)
    d2 = tuple(float(v) for v in d2)
    loc = Location(Plane(origin=tuple(origin), x_dir=d1, z_dir=ax))
    y_dir = (ax[1] * d1[2] - ax[2] * d1[1], ax[2] * d1[0] - ax[0] * d1[2], ax[0] * d1[1] - ax[1] * d1[0])
    sgn = 1.0 if sum(a * b for a, b in zip(y_dir, d2)) > 0 else -1.0
    pts = [(0, 0), (leg, 0), (0, sgn * leg)]
    if sgn < 0:
        pts = [pts[0], pts[2], pts[1]]
    solid = extrude(Polygon(*pts, align=None), length)
    return loc * solid


def rivet(xyz, direction, grip, d=4.0):
    """4 mm blind rivet: domed head of 8 mm on the outer face (z = 0 plane), mandrel stump, shank down the grip,
    set tail 2 mm beyond. 'direction' is the unit vector pointing out of the outer face."""
    head = Pos(0, 0, 0.6) * Cylinder(d, 1.2)
    head = break_edges(head, 0.4)
    shank = Pos(0, 0, -(grip + 1.5) / 2) * Cylinder(d / 2, grip + 1.5)
    tail = Pos(0, 0, -(grip + 1.5) - 1.0) * Cylinder(d * 0.62, 2.0)
    stump = Pos(0, 0, 1.2 + 0.4) * Cylinder(0.8, 0.8)
    return pointing(head + shank + tail + stump, xyz, direction)


def piano_hinge(x0, x1, y_leaf_a, t, hx, hy, z0, z1, xb0, xb1, y_leaf_b, barrel_r=3.5, bore_r=2.0):
    """Continuous (piano) hinge about the vertical axis through (hx, hy), from z0 to z1, closed: one leaf lies on the
    panel (plane y_leaf_a to y_leaf_a + t, x from x0 to the barrel) and one on the door (plane y_leaf_b to
    y_leaf_b + t, x from the barrel to x1). Returns (leaves and barrel, pin) with the pin bore cut in the first."""
    barrel = cz(barrel_r, z0, z1, hx, hy)
    leaf_a = bx(min(x0, hx - 1.0), hx - 1.0, y_leaf_a, y_leaf_a + t, z0, z1)
    leaf_b = bx(hx + 1.0, max(x1, hx + 1.0), y_leaf_b, y_leaf_b + t, z0, z1)
    body = fuse([barrel, leaf_a, leaf_b]) - cz(bore_r, z0 - 1, z1 + 1, hx, hy)
    pin = break_edges(cz(bore_r - 0.05, z0 + 0.5, z1 - 0.5, hx, hy), 0.3)
    return body, pin


def fan_120(cx_, cy_, z_top, depth=25.0, d=120.0):
    """120 mm axial fan with its axis along Z, top face at z_top. Returns (frame, rotor): a square frame with a round
    bore and corner holes, and a hub with seven swept blades."""
    s = d / 2
    z0 = z_top - depth
    frame = Pos(cx_, cy_, z0 + depth / 2) * Box(d, d, depth)
    frame = break_edges(frame, 3.0)
    frame -= Pos(cx_, cy_, z0 + depth / 2) * Cylinder(55.0, depth + 2)
    for ex in (-52.5, 52.5):
        for ey in (-52.5, 52.5):
            frame -= Pos(cx_ + ex, cy_ + ey, z0 + depth / 2) * Cylinder(2.25, depth + 2)
    hub = Pos(cx_, cy_, z0 + depth / 2) * Cylinder(21.0, depth - 4)
    hub = break_edges(hub, 2.0)
    blades = []
    for k in range(7):
        b = Pos(34.0, 0, 0) * Rot(0, 22, 0) * Box(32.0, 11.0, 1.4)
        blades.append(Pos(cx_, cy_, z0 + depth / 2) * Rot(0, 0, k * 360 / 7) * b)
    spokes = []
    for k in range(3):   # struts holding the motor to the frame, behind the blades
        spokes.append(Pos(cx_, cy_, z0 + 2.0) * Rot(0, 0, k * 120 + 15) * Pos(38.0, 0, 0) * Box(34.0, 4.0, 3.0))
    rotor = fuse([hub] + blades)
    frame = frame + fuse(spokes)
    return frame, rotor


def bead_tri(p0, p1, p2, along, length):
    """Weld bead whose section is the triangle p0, p1, p2 (three points in the plane at right angles to 'along'),
    run for 'length' along the unit vector 'along'. Use it where the two faces of the joint are not at 90 degrees."""
    ax = tuple(float(v) for v in along)
    sub = lambda a, b: tuple(x - y for x, y in zip(a, b))
    dot = lambda a, b: sum(x * y for x, y in zip(a, b))
    u = sub(p1, p0)
    lu = math.sqrt(dot(u, u))
    u = tuple(v / lu for v in u)
    v_dir = (ax[1] * u[2] - ax[2] * u[1], ax[2] * u[0] - ax[0] * u[2], ax[0] * u[1] - ax[1] * u[0])
    w = sub(p2, p0)
    pts = [(0, 0), (lu, 0), (dot(w, u), dot(w, v_dir))]
    if pts[2][1] < 0:
        pts = [pts[0], pts[2], pts[1]]
    return Location(Plane(origin=tuple(p0), x_dir=u, z_dir=ax)) * extrude(Polygon(*pts, align=None), length)


def screw(d, length, head_d=None, head_h=None):
    """Pan head screw along -Z: head from z 0 to head_h, shank from z 0 down to -length."""
    head_d = head_d or d * 1.9
    head_h = head_h or d * 0.65
    head = break_edges(Pos(0, 0, head_h / 2) * Cylinder(head_d / 2, head_h), min(0.6, head_h / 3))
    return head + Pos(0, 0, -length / 2) * Cylinder(d / 2, length)
