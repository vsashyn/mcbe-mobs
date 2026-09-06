#!/usr/bin/env python3
"""Generates Gouging Fire's geometry and animations.

Run from anywhere: python3 tools/gen_gouging_fire.py
Writes models/entity/gouging_fire.geo.json and
animations/gouging_fire.animation.json. Run tools/gen_textures.py afterwards:
the texture is painted off the UV slots packed here, so a change to a cube has
to be followed through to the paint.

Gouging Fire is a lion built on a ceratopsian skull. Four things carry the
read and everything else is scaffolding under them: the red four-pointed
faceplate, the gold frill with five horns swept off each side of it, the grey
smoke that lies the length of its back and trails off behind like a tail, and
the sheer mass of the shoulders. Sixty-odd cubes, shelf-packed into a 256x256
sheet, because that is far more UV than a hand-written table stays honest
about.

Cube sizes stay whole numbers: a fractional size makes a fractional net and
the net has to land on whole pixels. Origins may be fractional.

Sign conventions, both of which were settled by rendering rather than by
reading docs. Bedrock applies a bone's rotation as Rx(-rx) * Ry(-ry) * Rz(rz)
about its pivot, so a negative X pitches the front of the mob up, and on a
bone standing up out of its pivot a negative Z tips it toward +x.
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RP = os.path.join(ROOT, "pikachu_RP")
TW = TH = 256

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


SIDES = (("left", 1), ("right", -1))


def out(x, w, off):
    """Left-hand origin for a cube of width w sitting `off` out from centre."""
    return off if x > 0 else -off - w


# ------------------------------------------------------------------ geometry
# Chest and rump are two boxes, not one. The artwork puts almost all of the
# mass over the forelegs and lets the hindquarters fall away behind it, and a
# single barrel loses that entirely: it reads as a cow.
body = bone("body", pivot=(0, 24, 0))
cube(body, (-8, 19, -15), (16, 14, 16))          # chest
cube(body, (-7, 19, 1), (14, 12, 12))            # rump

# The cream bib. It has to stand a little proud of the chest, because painting
# cream onto the chest's own front face puts it behind the forelegs and none
# of it survives at mob scale.
ruff = bone("ruff", "body", pivot=(0, 25, -15))
cube(ruff, (-8, 20, -17), (16, 10, 3))

# The smoke. Six links lying the length of the back from the shoulders out
# past the rump, each pitched a few degrees higher than the last so the chain
# lifts and trails, and each parented to the one in front so a nudge at the
# shoulder runs all the way to the tip. Sizes shrink down the chain; equal
# boxes read as a fence, not as something coming apart in the air.
smoke_links = (
    ("smoke1", None, (0, 33, -4), (-6.5, 30, -11), (13, 7, 13), 0),
    ("smoke2", "smoke1", (0, 33, 4), (-6, 30, 0), (12, 7, 11), -2),
    ("smoke3", "smoke2", (0, 33, 12), (-5, 30, 9), (10, 7, 10), -4),
    ("smoke4", "smoke3", (0, 33, 19), (-4, 30, 17), (8, 6, 9), -7),
    ("smoke5", "smoke4", (0, 34, 26), (-3, 31, 24), (6, 5, 8), -9),
    ("smoke6", "smoke5", (0, 34, 31), (-2, 31, 30), (4, 4, 6), -11),
)
for name, parent, pivot, origin, size, pitch in smoke_links:
    b = bone(name, parent or "body", pivot=pivot, rotation=(pitch, 0, 0))
    cube(b, origin, size)

# Five grey spikes along the back, each one rooted a unit down inside the
# smoke link it rides rather than on the spine underneath. Sunk into the
# spine they would be swallowed whole: the smoke is thirteen wide and the
# spikes are three, so nothing of them survives from any angle but dead
# side-on. Riding the crest they read the way the artwork has them, and they
# billow with the smoke for free.
SPIKES = (("smoke1", (-1.5, 36, -9), (3, 7, 2)),
          ("smoke1", (-1.5, 36, -2), (3, 7, 2)),
          ("smoke2", (-1.5, 36, 4), (3, 6, 2)),
          ("smoke3", (-1.5, 35, 11), (3, 5, 2)),
          ("smoke4", (-1, 34, 18), (2, 4, 2)))
for i, (parent, origin, size) in enumerate(SPIKES):
    sp = bone(f"spike{i}", parent, pivot=(0, origin[1], origin[2] + size[2] / 2))
    cube(sp, origin, size)

# A collar in front of the shoulder link and a lump on each side of it. Six
# clean boxes in a row read as a caterpillar, and the front of the chain ends
# in a flat wall right where the neck leaves the shoulders unless something
# steps down off it.
collar = bone("collar", "smoke1", pivot=(0, 34, -12))
cube(collar, (-6, 30, -16), (12, 7, 6))

for side, x in SIDES:
    p = bone(f"puff_{side}", "smoke1", pivot=(x * 6, 34, -6))
    cube(p, (out(x, 4, 4.5), 30, -12), (4, 6, 9))

# Neck and skull. The head sits forward of the shoulders rather than over
# them, which is the difference between a beast about to charge and one
# standing to attention. The neck is deliberately five units narrower than the
# skull: matched, the two read as a single brown wedge sloping off the
# shoulders and the head stops existing.
neck = bone("neck", "body", pivot=(0, 29, -14), rotation=(-14, 0, 0))
cube(neck, (-4.5, 26, -22), (9, 9, 9))

head = bone("head", "neck", pivot=(0, 32, -22), rotation=(-2, 0, 0))
cube(head, (-7, 25, -33), (14, 14, 12))

# The faceplate: two crossed bars, red, standing a little off the skull. Four
# points, which is what the Pokedex art has, and the crossing is where the two
# green-and-red roundels sit.
face = bone("faceplate", "head", pivot=(0, 32, -33))
cube(face, (-2.5, 26, -35), (5, 13, 2))          # upright bar
cube(face, (-8, 30, -34.5), (16, 4, 2))          # crossbar

# The grey moustache plate over the muzzle.
muzzle = bone("muzzle", "head", pivot=(0, 27, -33))
cube(muzzle, (-5.5, 25, -36), (11, 4, 3))

# Blue eyes in short green fur, set above the crossbar and outside the upright
# one, which is the only gap in the faceplate they fit through. Both offsets
# are half-unit so no face of the eye ends up flush with a face of the plate:
# flush faces z-fight, overlapping volumes do not.
for side, x in SIDES:
    e = bone(f"eye_{side}", "head", pivot=(x * 4.5, 35, -33))
    cube(e, (out(x, 3, 3), 34, -34), (3, 3, 1))

# The frill. Raked back over the neck the way a ceratopsian carries one; stood
# upright it reads as a signboard nailed to the mob's forehead.
frill = bone("frill", "head", pivot=(0, 38, -23), rotation=(-32, 0, 0))
cube(frill, (-10, 37, -25), (20, 9, 3))

# Five horns a side, swept off the frill rim on an ellipse: near-vertical at
# the crown, near-horizontal at the cheek, longest through the middle of the
# fan. Z tips a horn outward, and it is negated against the side because on a
# bone standing up out of its pivot a negative Z is the one that leans toward
# +x.
RIM_X, RIM_Y, RIM_C = 10.0, 4.5, 41.5
for side, x in SIDES:
    for i, (ang, length) in enumerate(((14, 5), (36, 7), (58, 8),
                                       (80, 7), (100, 5))):
        rad = math.radians(ang)
        rx0 = x * RIM_X * math.sin(rad)
        ry0 = RIM_C + RIM_Y * math.cos(rad)
        h = bone(f"horn_{side}{i}", "frill", pivot=(rx0, ry0, -23.5),
                 rotation=(-10, (i - 2) * 9 * x, -x * ang))
        cube(h, (rx0 - 1, ry0 - 1, -24.5), (2, length, 2))

# Two fur strands a side, brown with a gold end, hung off the jaw line. They
# are the only part of the head that swings, so they are what sells the weight
# of it when the mob turns.
for side, x in SIDES:
    for j, (zy, zz) in enumerate(((32, -30), (30, -25))):
        top = bone(f"strand_{side}{j}", "head", pivot=(x * 7, zy, zz),
                   rotation=(34, 0, -x * 10))
        cube(top, (out(x, 3, 6), zy - 7, zz - 1.5), (3, 7, 3))
        tip = bone(f"strandtip_{side}{j}", f"strand_{side}{j}",
                   pivot=(x * 7, zy - 7, zz), rotation=(16, 0, 0))
        cube(tip, (out(x, 2, 6.5), zy - 11, zz - 1), (2, 4, 2))

# Forelegs carry the mass, so they are a size up on the hind pair and stand
# nearly straight under the shoulder. Three cubes each: thigh, shin, paw.
for side, x in SIDES:
    t = bone(f"foreleg_{side}", "body", pivot=(x * 5.5, 20, -11))
    cube(t, (out(x, 6, 2.5), 9, -14.5), (6, 11, 7))
    s = bone(f"foreshin_{side}", f"foreleg_{side}", pivot=(x * 5.5, 9, -11))
    cube(s, (out(x, 4, 3.5), 2, -13.5), (4, 7, 5))
    p = bone(f"forepaw_{side}", f"foreshin_{side}", pivot=(x * 5.5, 2, -11))
    cube(p, (out(x, 7, 2), 0, -16), (7, 2, 8))
    # Three red claws, sunk a unit back into the paw so no pair of faces ends
    # up coplanar. Coplanar faces z-fight; overlapping volumes do not.
    for k, dx in enumerate((0.25, 2.25, 4.25)):
        c = bone(f"claw_{side}{k}", f"forepaw_{side}", pivot=(x * 5.5, 1, -16))
        cube(c, (out(x, 1, 2.5 + dx), 0, -17.5), (1, 1, 2))

# Hind legs fold under the rump rather than standing straight, and each one
# carries three green spurs down its outer face.
for side, x in SIDES:
    t = bone(f"hindleg_{side}", "body", pivot=(x * 5.5, 20, 8))
    cube(t, (out(x, 7, 2), 9, 4), (7, 11, 8))
    for k, (sy, sz) in enumerate(((16, 5), (13, 4.5), (10, 4))):
        sp = bone(f"spur_{side}{k}", f"hindleg_{side}", pivot=(x * 8, sy, sz))
        cube(sp, (out(x, 1, 8.5), sy, sz), (1, 2, 3))
    s = bone(f"hindshin_{side}", f"hindleg_{side}", pivot=(x * 5.5, 9, 8))
    cube(s, (out(x, 4, 3.5), 2, 5.5), (4, 7, 5))
    p = bone(f"hindpaw_{side}", f"hindshin_{side}", pivot=(x * 5.5, 2, 8))
    cube(p, (out(x, 7, 2), 0, 3), (7, 2, 7))


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

print(f"{len(slots)} cubes in {len(bones)} bones, packed into "
      f"{shelves[-1][0] + shelves[-1][1]}/{TH} rows")

geo = {
    "format_version": "1.12.0",
    "minecraft:geometry": [
        {"description": {"identifier": "geometry.gouging_fire",
                         "texture_width": TW, "texture_height": TH,
                         "visible_bounds_width": 5, "visible_bounds_height": 4,
                         "visible_bounds_offset": [0, 1.6, 0]},
         "bones": bones},
        {"description": {"identifier": "geometry.raging_fury",
                         "texture_width": 32, "texture_height": 16,
                         "visible_bounds_width": 1, "visible_bounds_height": 1,
                         "visible_bounds_offset": [0, 0, 0]},
         "bones": [{"name": "flame", "pivot": [0, 0, 0],
                    "cubes": [{"origin": [-2, -2, -4], "size": [4, 4, 8],
                               "uv": [0, 0]}]}]},
    ],
}

path = os.path.join(RP, "models/entity/gouging_fire.geo.json")
with open(path, "w") as f:
    json.dump(geo, f, indent=2)
    f.write("\n")
print("wrote", path)


# ---------------------------------------------------------------- animations
# Everything below is written against the bone names above, so a rename up
# there has to come down here too. validate.py catches that one.
SMOKE = [n for n, *_ in smoke_links]
STRANDS = [f"strand_{s}{j}" for s, _ in SIDES for j in (0, 1)]
TIPS = [f"strandtip_{s}{j}" for s, _ in SIDES for j in (0, 1)]


def q(expr):
    return expr


# The smoke is its own clip, played on top of whatever else is running, so it
# never freezes when the mob stops moving. Nothing else animates these bones,
# which is what keeps the two clips from fighting over them.
#
# Each link is a half second behind the one in front of it and swings a little
# wider, so the motion arrives at the tip as a roll rather than as six boxes
# agreeing. The vertical term is doubled in frequency against the sway: smoke
# rises faster than it wanders.
smoke_clip = {"loop": True, "bones": {}}
for i, name in enumerate(SMOKE):
    lag = i * 46
    amp = 1.6 + i * 1.5
    smoke_clip["bones"][name] = {
        "rotation": [
            q(f"math.sin(query.life_time * 42 - {lag}) * {round(amp * 0.7, 2)}"),
            q(f"math.sin(query.life_time * 28 - {lag}) * {round(amp, 2)}"),
            q(f"math.cos(query.life_time * 33 - {lag}) * {round(amp * 0.8, 2)}"),
        ],
        "scale": [
            q(f"1 + math.sin(query.life_time * 55 - {lag * 2}) * 0.045"),
            q(f"1 + math.cos(query.life_time * 47 - {lag * 2}) * 0.06"),
            q(f"1 + math.sin(query.life_time * 51 - {lag * 2}) * 0.045"),
        ],
    }
smoke_clip["bones"]["collar"] = {
    "rotation": [q("math.sin(query.life_time * 36) * 2.5"),
                 q("math.cos(query.life_time * 24) * 3"), 0],
    "scale": q("1 + math.sin(query.life_time * 49) * 0.05"),
}
for side, x in SIDES:
    smoke_clip["bones"][f"puff_{side}"] = {
        "rotation": [
            q(f"math.cos(query.life_time * 38 - {60 if x > 0 else 0}) * 4"),
            q(f"math.sin(query.life_time * 31) * {5 * x}"), 0],
        "scale": q("1 + math.sin(query.life_time * 44 + "
                   f"{0 if x > 0 else 90}) * 0.07"),
    }


def swing(bone_map, speed, phase_of, amp_of, damped=True):
    """Sine swing on X, keyed off distance travelled so it tracks foot speed."""
    d = " * query.modified_move_speed" if damped else ""
    for name in bone_map:
        yield name, {"rotation": [
            q(f"math.cos(query.modified_distance_moved * {speed} - "
              f"{phase_of[name]}) * {amp_of[name]}{d}"), 0, 0]}


# Walk. A quadruped moves on diagonals: the near foreleg swings with the far
# hind leg, so the two pairs are half a cycle apart. The shins trail their own
# thigh by a quarter cycle, which is what folds the leg on the way through and
# straightens it on the way down; without that lag the legs scissor like a
# pair of compasses.
#
# The two pairs fold opposite ways, and getting that backwards is the single
# thing that stops a four-legged walk reading as four-legged. A foreleg breaks
# at the elbow, which is behind the leg, so the shin swings back as the paw
# lifts; a hind leg breaks at the hock, which points the other way, so its
# shin swings forward under the body.
GAIT = 15
walk = {"loop": True, "bones": {}}
for side, x in SIDES:
    ph = 0 if x > 0 else 180
    walk["bones"][f"foreleg_{side}"] = {"rotation": [
        q(f"math.cos(query.modified_distance_moved * {GAIT} - {ph}) * 34"
          " * query.modified_move_speed"), 0, 0]}
    walk["bones"][f"foreshin_{side}"] = {"rotation": [
        q(f"(1 - math.cos(query.modified_distance_moved * {GAIT} - {ph + 70}))"
          " * 15 * query.modified_move_speed"), 0, 0]}
    walk["bones"][f"forepaw_{side}"] = {"rotation": [
        q(f"math.cos(query.modified_distance_moved * {GAIT} - {ph + 130}) * 12"
          " * query.modified_move_speed"), 0, 0]}
    walk["bones"][f"hindleg_{side}"] = {"rotation": [
        q(f"math.cos(query.modified_distance_moved * {GAIT} - {ph + 180}) * 30"
          " * query.modified_move_speed"), 0, 0]}
    walk["bones"][f"hindshin_{side}"] = {"rotation": [
        q(f"(math.cos(query.modified_distance_moved * {GAIT} - {ph + 250}) - 1)"
          " * 16 * query.modified_move_speed"), 0, 0]}
    walk["bones"][f"hindpaw_{side}"] = {"rotation": [
        q(f"math.cos(query.modified_distance_moved * {GAIT} - {ph + 300}) * 14"
          " * query.modified_move_speed"), 0, 0]}
    for j in (0, 1):
        walk["bones"][f"strand_{side}{j}"] = {"rotation": [
            q(f"math.cos(query.modified_distance_moved * {GAIT * 2} - {j * 40})"
              " * 9 * query.modified_move_speed"), 0, 0]}

# The body rides at twice the gait frequency, because both diagonals land in
# one stride and each landing is a nod.
walk["bones"]["body"] = {
    "rotation": [
        q(f"math.cos(query.modified_distance_moved * {GAIT * 2}) * 2.5"
          " * query.modified_move_speed"),
        0,
        q(f"math.sin(query.modified_distance_moved * {GAIT}) * 3"
          " * query.modified_move_speed"),
    ],
    "position": [
        0,
        q(f"math.cos(query.modified_distance_moved * {GAIT * 2}) * 0.7"
          " * query.modified_move_speed"),
        0,
    ],
}
walk["bones"]["neck"] = {"rotation": [
    q(f"math.cos(query.modified_distance_moved * {GAIT * 2} - 50) * 3"
      " * query.modified_move_speed"), 0,
    q(f"-math.sin(query.modified_distance_moved * {GAIT}) * 2.5"
      " * query.modified_move_speed")]}
walk["bones"]["head"] = {"rotation": [
    q(f"math.cos(query.modified_distance_moved * {GAIT * 2} - 110) * 4"
      " * query.modified_move_speed"), 0, 0]}

# Idle. A heavy animal standing still still moves: the chest fills, the head
# drifts, the strands hang and swing on their own slower clock.
idle = {"loop": True, "bones": {
    "body": {
        "rotation": [q("math.sin(query.life_time * 34) * 0.8"), 0, 0],
        "position": [0, q("math.sin(query.life_time * 34) * 0.22"), 0],
    },
    "neck": {"rotation": [q("math.sin(query.life_time * 34 - 40) * 1.4"),
                          q("math.sin(query.life_time * 11) * 2.5"), 0]},
    "head": {"rotation": [q("math.sin(query.life_time * 34 - 90) * 1.8"),
                          q("math.sin(query.life_time * 9) * 4"), 0]},
    "ruff": {"scale": [1, q("1 + math.sin(query.life_time * 34) * 0.03"), 1]},
}}
for j, name in enumerate(STRANDS):
    idle["bones"][name] = {"rotation": [
        q(f"math.sin(query.life_time * 22 - {j * 55}) * 4"), 0,
        q(f"math.cos(query.life_time * 17 - {j * 55}) * 3")]}
for j, name in enumerate(TIPS):
    idle["bones"][name] = {"rotation": [
        q(f"math.sin(query.life_time * 22 - {j * 55 + 60}) * 5"), 0, 0]}

# Roar. The wind-up rocks back onto the hind legs and lifts the skull, then
# the whole mass comes down and forward through the crossbar of the faceplate.
# 0.9 s end to end, matched to the delayed_attack's attack_duration so the hit
# lands on the slam rather than somewhere in the recovery.
roar = {"loop": True, "animation_length": 0.9, "bones": {
    "body": {
        "rotation": {"0.0": [0, 0, 0], "0.3": [-17, 0, 0], "0.45": [10, 0, 0],
                     "0.62": [3, 0, 0], "0.9": [0, 0, 0]},
        "position": {"0.0": [0, 0, 0], "0.3": [0, 1.6, 2.2],
                     "0.45": [0, -0.8, -2.6], "0.9": [0, 0, 0]},
    },
    "neck": {"rotation": {"0.0": [0, 0, 0], "0.3": [-26, 0, 0],
                          "0.45": [22, 0, 0], "0.62": [6, 0, 0],
                          "0.9": [0, 0, 0]}},
    "head": {"rotation": {"0.0": [0, 0, 0], "0.28": [-20, 0, 0],
                          "0.45": [26, 0, 0], "0.62": [4, 0, 0],
                          "0.9": [0, 0, 0]}},
    "frill": {"rotation": {"0.0": [0, 0, 0], "0.3": [10, 0, 0],
                           "0.48": [-8, 0, 0], "0.9": [0, 0, 0]}},
    "muzzle": {"position": {"0.0": [0, 0, 0], "0.3": [0, -0.6, -0.4],
                            "0.45": [0, 0, 0], "0.9": [0, 0, 0]}},
}}
for side, x in SIDES:
    roar["bones"][f"foreleg_{side}"] = {"rotation": {
        "0.0": [0, 0, 0], "0.3": [-46, 0, 0], "0.45": [24, 0, 0],
        "0.62": [-6, 0, 0], "0.9": [0, 0, 0]}}
    roar["bones"][f"foreshin_{side}"] = {"rotation": {
        "0.0": [0, 0, 0], "0.3": [-30, 0, 0], "0.45": [12, 0, 0],
        "0.9": [0, 0, 0]}}
    roar["bones"][f"hindleg_{side}"] = {"rotation": {
        "0.0": [0, 0, 0], "0.3": [14, 0, 0], "0.45": [-10, 0, 0],
        "0.9": [0, 0, 0]}}
    for j in (0, 1):
        roar["bones"][f"strand_{side}{j}"] = {"rotation": {
            "0.0": [0, 0, 0], "0.34": [-34, 0, 0], "0.5": [30, 0, 0],
            "0.7": [-8, 0, 0], "0.9": [0, 0, 0]}}

# Head tracking is shared out between the neck and the skull instead of landing
# on the skull alone. An animal this heavy turns from the shoulder; putting the
# whole turn on the head snaps the frill off the end of the neck.
track = {
    "neck": {"rotation": [q("query.target_x_rotation * 0.3"),
                          q("query.target_y_rotation * 0.45"), 0]},
    "head": {"rotation": [q("query.target_x_rotation * 0.5"),
                          q("query.target_y_rotation * 0.55"), 0]},
}

anims = {
    "format_version": "1.8.0",
    "animations": {
        "animation.gouging_fire.idle": idle,
        "animation.gouging_fire.walk": walk,
        "animation.gouging_fire.roar": roar,
        "animation.gouging_fire.smoke": smoke_clip,
        "animation.gouging_fire.look_at_target": {"loop": True, "bones": track},
        "animation.raging_fury.spin": {
            "loop": True,
            "animation_length": 0.1,
            "bones": {"flame": {"rotation": [
                0, 0, q("query.life_time * 900")]}},
        },
    },
}

path = os.path.join(RP, "animations/gouging_fire.animation.json")
with open(path, "w") as f:
    json.dump(anims, f, indent=2)
    f.write("\n")
print("wrote", path)
