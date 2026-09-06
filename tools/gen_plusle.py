#!/usr/bin/env python3
"""Generates Plusle's geometry.

Run from anywhere: python3 tools/gen_plusle.py
Writes models/entity/plusle.geo.json. Run tools/gen_textures.py afterwards:
it paints off this model, so a change here has to be followed through to the
texture.

Plusle is a head with ears on it. The head is nine units across on a seven
unit body, the ears run one and a half times the height of the skull, and the
tail is a plus sign eleven units tall standing clear of the back. Those three
proportions are the whole read; everything else is a cream box.

Two rules run through the cube list. Sizes stay whole numbers, because a
fractional size makes a fractional box-UV net and the net has to land on whole
pixels. And no two cubes end up with a face on the same plane: touching faces
z-fight, overlapping volumes do not, so every joint here sinks half a unit
into the part it hangs off and every child is a shade narrower or wider than
its parent rather than flush with it. The tail is where that matters most: a
plus built as two crossed bars of equal thickness has four coplanar faces
straight through the middle of it, so the crossbar is three units thick
against the upright's two.
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


# The body. Seven across and six tall, which is deliberately shorter than the
# skull above it: Plusle is a head with a body attached, and the moment the
# torso matches the head for height the whole thing reads as a bear cub.
body = bone("body", pivot=(0, 3, 0))
cube(body, (-3.5, 2.5, -3), (7, 6, 6))

# Legs sunk half a unit into the body and a quarter unit inside its flanks, so
# neither the top face nor either side lands on a face of the torso.
for side, x in (("left", 1), ("right", -1)):
    b = bone(f"leg_{side}", "body", pivot=(x * 1.75, 3, 0))
    cube(b, (0.25 if x > 0 else -3.25, 0, -1.5), (3, 3, 3))

# Arms hang from the shoulder and splay eight degrees out. Plusle holds them
# away from the body in every piece of art it has ever appeared in, and eight
# degrees is enough to open a gap at the elbow without reading as a shrug.
# Positive roll swings the left side outward and the right side in, which is
# why the sign is tied to which side the arm is on.
for side, x in (("left", 1), ("right", -1)):
    b = bone(f"arm_{side}", "body", pivot=(x * 3.5, 7, 0), rotation=(0, 0, 8 * x))
    cube(b, (3 if x > 0 else -5, 3, -1), (2, 5, 2))

# The head out-measures the body on every axis: nine across on a seven-wide
# torso, eight tall on a six-tall one, eight deep on a six-deep one. That one
# proportion carries more of the likeness than any pixel on the face does.
head = bone("head", "body", pivot=(0, 8.5, 0))
cube(head, (-4.5, 8, -4), (9, 8, 8))
# Sit on the two cheek pouches, on the surface of the face rather than inside
# it, so the sparks the cheer animation throws come off the plus marks.
head["locators"] = {"cheek_left": [3, 10.5, -4.1],
                    "cheek_right": [-3, 10.5, -4.1]}

# The cream nub each ear grows out of. Without it the red starts at the skull
# and the ear reads as a horn stuck on rather than as an ear.
for side, x in (("left", 1), ("right", -1)):
    b = bone(f"ear_base_{side}", "head", pivot=(x * 2.75, 15, 0))
    cube(b, (1.25 if x > 0 else -4.25, 14.5, -1.5), (3, 3, 3))

# The ears. Two links each: a seven-unit blade four wide leaning six degrees
# back, then a five-unit tip three wide stacked straight on top of it. Neither
# link rolls. They were splayed twenty and fourteen degrees out, which reads
# as a V from one side of the sign and as a pair crossed over the skull from
# the other, and the sign of a z rotation on a Bedrock bone is the easiest
# thing here to get backwards. Standing them upright the way Pikachu's stand
# settles it, and the pair still clears itself by three units at the blade.
# Four units wide rather than three because a narrower ear reads as an antenna
# at mob scale; these are meant to look like broad flat blades. Every link is
# a different width from the one it hangs off, so no side face is shared down
# the chain.
for side, x in (("left", 1), ("right", -1)):
    b = bone(f"ear_{side}", f"ear_base_{side}", pivot=(x * 2.75, 16.5, 0),
             rotation=(-6, 0, 0))
    cube(b, (1.5 if x > 0 else -5.5, 16.5, -1), (4, 7, 2))

    t = bone(f"ear_{side}_tip", f"ear_{side}", pivot=(x * 2.75, 23.5, 0))
    cube(t, (2 if x > 0 else -5, 23, -0.5), (3, 5, 1))

# The tail is a plus sign eleven units tall, and where it sits is the whole
# problem with it. Built flush against the rump it disappears: the body is six
# deep and the head eight, so a plus standing at the back of the torso has its
# entire front arm inside the mob. Tilting it back out of the way instead
# turns the plus into a diagonal cross, which is Plusle's one unmistakable
# mark rendered wrong. So it stands upright and the crossbar carries it: the
# front arm runs four units forward into the gap under the back of the skull
# and anchors there, which leaves all four arms of the plus against sky from
# the side and costs no extra cube to hold it on.
#
# The bars are two thick and the crossbar three, each stepping wider than the
# piece it threads through, so nowhere in the join do two faces land on the
# same plane. A plus built as two crossed bars of equal thickness z-fights
# straight down the middle of itself.
tail = bone("tail", "body", pivot=(0, 6, 4), rotation=(-5, 0, 0))
cube(tail, (-1, 3.5, 5), (2, 5, 2))
cube(tail, (-1.5, 7.5, 2), (3, 3, 8))
cube(tail, (-1, 9.5, 5), (2, 5, 2))


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
        {"description": {"identifier": "geometry.plusle",
                         "texture_width": TW, "texture_height": TH,
                         "visible_bounds_width": 3,
                         "visible_bounds_height": 2.5,
                         "visible_bounds_offset": [0, 1.1, 0.3]},
         "bones": bones},
        # Spark is a plus too, so a shot in the air says which of the pair
        # fired it before it lands. Two bars, the flat one three deep against
        # the upright's two, for the same reason the tail's are.
        {"description": {"identifier": "geometry.spark",
                         "texture_width": 32, "texture_height": 16,
                         "visible_bounds_width": 1, "visible_bounds_height": 1,
                         "visible_bounds_offset": [0, 0, 0]},
         "bones": [{"name": "bolt", "pivot": [0, 0, 0], "cubes": [
             {"origin": [-1, -3, -1], "size": [2, 6, 2], "uv": [0, 0]},
             {"origin": [-3, -1, -1.5], "size": [6, 2, 3], "uv": [8, 0]}]}]},
    ],
}

out = os.path.join(RP, "models/entity/plusle.geo.json")
with open(out, "w") as f:
    json.dump(geo, f, indent=2)
    f.write("\n")
print("wrote", out)
