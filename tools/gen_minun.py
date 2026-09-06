#!/usr/bin/env python3
"""Generates Minun's geometry.

Run from anywhere: python3 tools/gen_minun.py
Writes models/entity/minun.geo.json. Run tools/gen_textures.py afterwards:
the texture is painted off this model, so a change here has to be followed
through to the sheet.

Minun is a cream mouse whose whole silhouette is three blue shapes: two long
flat ears in a V, two cheek discs with a minus cut into them, and a minus bar
on the end of a stub tail. Everything else is body. The ears are a three-link
chain each, narrow at the skull and widest two thirds of the way up, because a
single tapering box reads as a rabbit and Minun's ears are paddles.

Cube sizes stay whole numbers: box UV is one texel per model unit, so a
fractional size makes a fractional net. Origins may be fractional, and several
are, to sink one cube far enough into its neighbour that no pair of faces ends
up coplanar and z-fighting.
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RP = os.path.join(ROOT, "pikachu_RP")
TW = TH = 64

bones = []


def bone(name, parent=None, pivot=(0, 0, 0), rotation=None):
    b = {"name": name, "pivot": [round(v, 3) for v in pivot]}
    if parent:
        b["parent"] = parent
    if rotation:
        b["rotation"] = [round(v, 3) for v in rotation]
    b["cubes"] = []
    bones.append(b)
    return b


def cube(b, origin, size):
    b["cubes"].append({"origin": [round(v, 3) for v in origin],
                       "size": [int(v) for v in size]})


# The torso. Narrower than Pikachu's and no deeper, because Minun carries its
# weight in the head and the ears and a barrel chest fights that.
body = bone("body", pivot=(0, 3, 0))
cube(body, (-3, 3, -2.5), (6, 5, 5))

# The head is the same 8x7x7 ball Pikachu wears. It is the one measurement in
# the pack that is worth copying outright: at 16 texels per block it is the
# smallest box a face fits on without the eyes touching the jaw.
head = bone("head", "body", pivot=(0, 8, 0))
cube(head, (-4, 8, -3.5), (8, 7, 7))

# Cheek pouches, half a unit proud of the face and a full unit past the
# temple, so they bulge in the front view and still catch light from the side.
# Sunk 0.3 into the skull rather than flush against it: flush faces z-fight.
# Set any closer together than this and the two discs stop reading as cheeks
# and start reading as one band across the muzzle.
for side, x in (("left", 1), ("right", -1)):
    c = bone(f"cheek_{side}", "head", pivot=(x * 3, 10.5, -3.5))
    cube(c, (2 if x > 0 else -5, 9, -4.2), (3, 3, 1))

# A cream knuckle at the base of each ear. In the artwork the ear does not
# grow straight out of the skull; it sits on a small round mound the same
# colour as the head, and that mound is what keeps the blue from starting
# abruptly at the hairline.
for side, x in (("left", 1), ("right", -1)):
    r = bone(f"ear_root_{side}", "head", pivot=(x * 2.5, 15, -0.5))
    cube(r, (1 if x > 0 else -4, 13.8, -2), (3, 2, 3))

# The ears: 12 units of blue on a 7 unit head, standing straight up the way
# Pikachu's do and leaning 8 degrees back. They carry no roll at all. An
# earlier build splayed them 34 degrees into a V, which reads as a V in one
# renderer and as a pair of ears crossed over the skull in the other, because
# the sign of a z rotation is the one thing about a Bedrock bone that is easy
# to get backwards. Upright is not ambiguous, and it is what Minun's own
# artwork shows when it is standing still. Widths go 2, 4, 3: narrow at the
# skull, widest across the middle, rounded off at the tip.
#
# The two ears clear each other by a unit at the widest link, so nothing here
# needs a roll to keep them apart. Only the idle sway leans them, a couple of
# degrees each way and mirrored, which cannot cross them either.
for side, x in (("left", 1), ("right", -1)):
    lo = 1.5 if x > 0 else -3.5
    base = bone(f"ear_{side}", "head", pivot=(x * 2.5, 15.5, -0.5),
                rotation=(-8, 0, 0))
    cube(base, (lo, 15.5, -1), (2, 3, 1))

    mid = bone(f"ear_{side}_mid", f"ear_{side}", pivot=(x * 2.5, 18.5, -0.5))
    cube(mid, (lo - 1, 18.4, -1), (4, 6, 1))

    tip = bone(f"ear_{side}_tip", f"ear_{side}_mid", pivot=(x * 2.5, 24.4, -0.5))
    cube(tip, (lo - 0.5, 24.2, -1), (3, 3, 1))

# Stubby arms with no digits, ending in a blue mitten. Two cubes in one bone
# so the paw can take its own colour without needing its own joint, and rolled
# six degrees out so the paws clear the hips.
for side, x in (("left", 1), ("right", -1)):
    a = bone(f"arm_{side}", "body", pivot=(x * 3, 7.5, -0.25), rotation=(0, 0, 6 * x))
    cube(a, (2.6 if x > 0 else -4.6, 4.5, -1.25), (2, 3, 2))
    cube(a, (2.6 if x > 0 else -4.6, 2.5, -1.25), (2, 2, 2))

# Feet wide enough to stand on. Same 3x3x3 blocks Pikachu uses, set half a
# unit forward so the mob does not look like it is leaning back.
for side, x in (("left", 1), ("right", -1)):
    l = bone(f"leg_{side}", "body", pivot=(x * 1.5, 3, 0))
    cube(l, (0 if x > 0 else -3, 0, -1.6), (3, 3, 3))

# The tail is a short cream stub carrying a blue bar, and the bar is the whole
# point of it: six units across, two thick, hung square behind the mob. A
# tamed Minun walks in front of its owner most of the time, so the minus has
# to read from behind, which is why the bar runs across x rather than back
# along z. Fifteen degrees of droop on the stub keeps it off the hips.
tail = bone("tail", "body", pivot=(0, 5, 2.5), rotation=(-15, 0, 0))
cube(tail, (-1, 4.4, 2), (2, 2, 3))

bar = bone("tail_bar", "tail", pivot=(0, 5.4, 5), rotation=(-10, 0, 0))
cube(bar, (-3, 4.4, 4.6), (6, 2, 2))


def net(c):
    w, h, d = c["size"]
    return math.ceil(2 * d + 2 * w), math.ceil(d + h)


slots = [(net(c)[1], net(c)[0], b["name"], c) for b in bones for c in b["cubes"]]
slots.sort(key=lambda s: (-s[0], -s[1]))

shelves = []
for nh, nw, bname, c in slots:
    for sh in shelves:
        if sh[1] >= nh and sh[2] + nw <= TW:
            c["uv"] = [sh[2], sh[0]]
            sh[2] += nw
            break
    else:
        y = shelves[-1][0] + shelves[-1][1] if shelves else 0
        if y + nh > TH:
            sys.exit(f"texture too small: no room for {bname}")
        shelves.append([y, nh, nw])
        c["uv"] = [0, y]

print(f"{len(slots)} cubes packed into {shelves[-1][0] + shelves[-1][1]}/{TH} rows")

geo = {
    "format_version": "1.12.0",
    "minecraft:geometry": [
        {"description": {"identifier": "geometry.minun",
                         "texture_width": TW, "texture_height": TH,
                         "visible_bounds_width": 2.5,
                         "visible_bounds_height": 2.5,
                         "visible_bounds_offset": [0, 1, 0]},
         "bones": bones},
        {"description": {"identifier": "geometry.minus_spark",
                         "texture_width": 16, "texture_height": 16,
                         "visible_bounds_width": 1, "visible_bounds_height": 1,
                         "visible_bounds_offset": [0, 0, 0]},
         "bones": [{"name": "bolt", "pivot": [0, 0, 0],
                    "cubes": [{"origin": [-1.5, -1.5, -1.5], "size": [3, 3, 3],
                               "uv": [0, 0]}]}]},
    ],
}

out = os.path.join(RP, "models/entity/minun.geo.json")
with open(out, "w") as f:
    json.dump(geo, f, indent=2)
    f.write("\n")
print("wrote", out)
