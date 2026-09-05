#!/usr/bin/env python3
"""Generates Lapras's geometry.

Run from anywhere: python3 tools/gen_lapras.py
Writes models/entity/lapras.geo.json. Run tools/gen_textures.py afterwards:
it paints off this model, so a change here has to be followed through to the
texture.

Lapras is thirty cubes and the widest mob in the pack, so its UV net is
shelf-packed here rather than written by hand. Cube sizes stay whole numbers,
because a fractional size makes a fractional net and the net has to land on
whole pixels. Origins may be fractional; only sizes may not.

The rig is a shell with three things hanging off it: a four-link neck up the
front, four flippers on the corners, and a coiled ear on each side of the head
built as its own three-link chain, which is what turns three boxes into a
ram's horn.
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RP = os.path.join(ROOT, "pikachu_RP")
TW = TH = 128

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


# The torso. Wider than it is tall and longer than it is wide, so what shows
# under the shell is a cream keel rather than an animal's flank.
body = bone("body", pivot=(0, 7, 0))
cube(body, (-7, 2, -9), (14, 11, 18))

# The shell is three slabs stepping inward, not one box. One box renders as a
# crate no matter how it is painted; three give the dome a rim, a shoulder and
# a crown, and the two steps do more for the silhouette than any pixel can.
# It also has to stay roughly as tall as the neck: the artwork splits Lapras
# about half and half, and a shell any shorter turns it into a swan.
shell = bone("shell", "body", pivot=(0, 14, 2))
cube(shell, (-9, 8, -8), (18, 6, 21))
cube(shell, (-8, 13, -6), (16, 6, 18))
cube(shell, (-5, 18, -4), (10, 6, 14))

# Blunt knobs, sunk into the slab they sit on so no pair of faces ends up
# coplanar. Coplanar faces z-fight; overlapping volumes do not.
knobs = bone("knobs", "shell", pivot=(0, 14, 2))
for origin, size in (((-2, 22, 1), (4, 3, 4)),        # the crown
                     ((3, 20, -2), (3, 3, 3)),        # ring around the crown
                     ((-6, 20, -2), (3, 3, 3)),
                     ((-1.5, 20, 6), (3, 3, 3)),
                     ((6, 16, -3), (3, 3, 3)),        # on the middle shoulder
                     ((-9, 16, -3), (3, 3, 3)),
                     ((6, 16, 7), (3, 3, 3)),
                     ((-9, 16, 7), (3, 3, 3)),
                     ((8, 10, 2), (3, 3, 3)),         # out on the rim
                     ((-11, 10, 2), (3, 3, 3))):
    cube(knobs, origin, size)

# The neck stands close to vertical and only leans in at the joints. Three
# degrees a link is enough: the pitches compound, and a plesiosaur that leans
# any harder reads as a mob falling over rather than one looking ahead.
neck = bone("neck_base", "body", pivot=(0, 12, -5), rotation=(-3, 0, 0))
cube(neck, (-3.5, 12, -8.5), (7, 7, 7))

mid = bone("neck_mid", "neck_base", pivot=(0, 19, -5), rotation=(-4, 0, 0))
cube(mid, (-3, 19, -8), (6, 6, 6))

top = bone("neck_top", "neck_mid", pivot=(0, 25, -5), rotation=(-5, 0, 0))
cube(top, (-2.5, 25, -7.5), (5, 5, 5))

# Nine wide over a five-wide neck. The head has to out-measure the link under
# it or the whole neck reads as one tapering post with a face painted on the
# end of it.
head = bone("head", "neck_top", pivot=(0, 31, -5), rotation=(-6, 0, 0))
cube(head, (-4.5, 28, -9.5), (9, 7, 7))

# The muzzle hangs off the bottom half of the skull, not the middle of it.
# Centred, it covers exactly the rows the eyes are painted on and the face
# disappears behind it.
snout = bone("snout", "head", pivot=(0, 30, -9.5))
cube(snout, (-2.5, 28.5, -12.5), (5, 3, 3))

horn = bone("horn", "head", pivot=(0, 34, -7), rotation=(-18, 0, 0))
cube(horn, (-1, 33.5, -8), (2, 5, 2))

# Each ear is four short links turned 70 degrees against the one before it, so
# the chain comes through 280 and closes a loop about four units across behind
# the skull. Every number here was arrived at by getting it wrong first:
# longer links widen the coil into a carrying handle, a steeper angle knots it
# into a lump, curling it forward puts the tip through the face, and too much
# splay turns the pair into antennae. The base link is pitched 38 degrees back
# before the coil even starts, which is what stops the pair standing up in the
# front view like a lyre; nine degrees of splay is all it takes after that to
# keep them off the skull.
for side, x in (("left", 1), ("right", -1)):
    ex = 3 if x > 0 else -6
    prev, py = f"ear_{side}", 33.5
    b = bone(prev, "head", pivot=(x * 4, py, -3), rotation=(38, 0, 9 * x))
    cube(b, (ex, py, -4.5), (3, 3, 3))
    for link in ("b", "c"):
        py += 3
        name = f"ear_{side}_{link}"
        b = bone(name, prev, pivot=(x * 4, py, -3), rotation=(70, 0, 0))
        cube(b, (ex, py, -4.5), (3, 3, 3))
        prev = name
    b = bone(f"ear_{side}_tip", prev, pivot=(x * 4, py + 3, -3), rotation=(70, 0, 0))
    cube(b, (ex, py + 3, -4), (3, 2, 2))

# Four paddles, the front pair longer than the back pair the way the Pokedex
# has them. Each roots two units inside the flank so no gap opens at the
# shoulder; yaw splays the front pair forward and the back pair aft, and the
# roll drops each tip so the mob rests on its keel rather than on four points.
for side, x in (("left", 1), ("right", -1)):
    f = bone(f"flipper_front_{side}", "body", pivot=(x * 6, 5, -5),
             rotation=(0, 20 * x, -12 * x))
    cube(f, (6 if x > 0 else -18, 1, -10), (12, 4, 9))

    r = bone(f"flipper_rear_{side}", "body", pivot=(x * 6, 5, 4),
             rotation=(0, -22 * x, -10 * x))
    cube(r, (6 if x > 0 else -16, 1, 1), (10, 4, 8))

tail = bone("tail", "body", pivot=(0, 6, 9), rotation=(-15, 0, 0))
cube(tail, (-2.5, 4, 9), (5, 4, 5))


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
        {"description": {"identifier": "geometry.lapras",
                         "texture_width": TW, "texture_height": TH,
                         "visible_bounds_width": 4, "visible_bounds_height": 3.5,
                         "visible_bounds_offset": [0, 1.4, 0]},
         "bones": bones},
        {"description": {"identifier": "geometry.ice_beam",
                         "texture_width": 32, "texture_height": 16,
                         "visible_bounds_width": 1, "visible_bounds_height": 1,
                         "visible_bounds_offset": [0, 0, 0]},
         "bones": [{"name": "shard", "pivot": [0, 0, 0],
                    "cubes": [{"origin": [-1.5, -1.5, -3.5], "size": [3, 3, 7],
                               "uv": [0, 0]}]}]},
    ],
}

out = os.path.join(RP, "models/entity/lapras.geo.json")
with open(out, "w") as f:
    json.dump(geo, f, indent=2)
    f.write("\n")
print("wrote", out)
