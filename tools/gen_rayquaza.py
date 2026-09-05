#!/usr/bin/env python3
"""Generates Rayquaza's geometry and animations.

Run from anywhere: python3 tools/gen_rayquaza.py
Writes models/entity/rayquaza.geo.json and animations/rayquaza.animation.json.
Run tools/gen_textures.py afterwards: it reads its UV slots back out of the
model, so a change here has to be followed through to the texture.

Rayquaza is forty-six cubes and ten chained segments. Both files are laid out
from tables rather than by hand because the UV net has to be packed without
overlap and every segment has to lag the one in front of it by the same amount,
and neither survives being edited a cube at a time.
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RP = os.path.join(ROOT, "pikachu_RP")
TW = TH = 128
CY = 16.0                      # the serpent's centre line, one block up

# ------------------------------------------------------------------ geometry
bones = []


def bone(name, parent=None, pivot=(0, CY, 0), rotation=None):
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
                       "size": [round(v, 3) for v in size]})


bone("root", pivot=(0, CY, 0))

# The skull steps down into the muzzle rather than running out as one box, so
# the head keeps a snake's taper and the mouth line has somewhere to sit.
head = bone("head", "root", pivot=(0, CY, -9))
cube(head, (-3.5, 12.5, -20), (7, 7, 11))      # skull
cube(head, (-2.5, 15, -27), (5, 4, 7))         # muzzle

jaw = bone("jaw", "head", pivot=(0, 15, -19))
cube(jaw, (-2, 12, -27), (4, 3, 8))

disc = bone("disc", "head", pivot=(0, 19.5, -17))
cube(disc, (-2.5, 19.5, -19), (5, 1, 5))       # the plate on the forehead

for s, x in (("left", 1), ("right", -1)):
    e = bone(f"eye_{s}", "head", pivot=(x * 3.5, 17, -18))
    cube(e, (3 if x > 0 else -4, 15.5, -19.5), (1, 3, 5))

    b = bone(f"brow_{s}", "head", pivot=(x * 3, 19, -18))
    cube(b, (3.3 if x > 0 else -4.3, 18.5, -20), (1, 1, 6))

    k = bone(f"cheek_{s}", "head", pivot=(x * 3.5, 15, -14),
             rotation=(85, 0, -30 * x))
    cube(k, (3 if x > 0 else -4, 15, -15.5), (1, 10, 3))

# name, front z, back z, cube width == height, what rides on it
SEGMENTS = [
    ("neck",  -9,  -2, 6, "ring"),
    ("body1", -2,   5, 7, "arms"),
    ("body2",  5,  12, 7, "fins"),
    ("body3", 12,  19, 6, "ring"),
    ("body4", 19,  26, 6, "belt"),
    ("body5", 26,  33, 6, "fins"),
    ("body6", 33,  40, 5, "ring"),
    ("body7", 40,  47, 4, "belt"),
    ("body8", 47,  54, 3, "ring"),
    ("tail",  54,  62, 3, "tailfin"),
]

parent = "root"
for name, z0, z1, w, deco in SEGMENTS:
    hw = w / 2.0
    seg = bone(name, parent, pivot=(0, CY, z0))
    cube(seg, (-hw, CY - hw, z0), (w, w, z1 - z0))
    mid = (z0 + z1) / 2.0
    parent = name

    if deco == "arms":
        for s, x in (("left", 1), ("right", -1)):
            # arms carried out, down and swept forward, not straight out
            a = bone(f"arm_{s}", name, pivot=(x * hw, CY, mid),
                     rotation=(0, 20 * x, -35 * x))
            cube(a, (hw if x > 0 else -hw - 4, 14.5, mid - 1.5), (4, 3, 3))
            f = bone(f"forearm_{s}", f"arm_{s}", pivot=(x * (hw + 4), CY, mid),
                     rotation=(0, 0, -28 * x))
            cube(f, (hw + 4 if x > 0 else -hw - 8, 14.5, mid - 1.5), (4, 3, 3))
            h = bone(f"hand_{s}", f"forearm_{s}", pivot=(x * (hw + 8), CY, mid),
                     rotation=(0, 0, -12 * x))
            cube(h, (hw + 8 if x > 0 else -hw - 11, 14.5, mid - 1.5), (3, 3, 3))
            cx = hw + 11 if x > 0 else -hw - 13
            for dz in (-1.4, -0.2, 1.0):           # three claws
                cube(h, (cx, 15.5, mid + dz), (2, 1, 1))
        deco = "belt"

    if deco in ("fins", "tailfin"):
        # Low rudders rather than square paddles, raked back along the body,
        # in the X of four the artwork puts at every finned station.
        fh, fd = (5, 9) if deco == "tailfin" else (3, 7)
        for s, x in (("left", 1), ("right", -1)):
            up = bone(f"finup_{s}_{name}", name, pivot=(x * (hw - 0.5), CY + hw, mid),
                      rotation=(18, 0, -38 * x))
            cube(up, (hw - 1 if x > 0 else -hw, CY + hw, mid - fd / 2.0), (1, fh, fd))
            dn = bone(f"findn_{s}_{name}", name, pivot=(x * (hw - 0.5), CY - hw, mid),
                      rotation=(-18, 0, 38 * x))
            cube(dn, (hw - 1 if x > 0 else -hw, CY - hw - fh, mid - fd / 2.0), (1, fh, fd))

for s, x in (("left", 1), ("right", -1)):          # the flaps behind the jaw
    n = bone(f"gill_{s}", "neck", pivot=(x * 3, CY + 1, -7), rotation=(15, 0, -55 * x))
    cube(n, (2.5 if x > 0 else -3.5, CY + 1, -8.5), (1, 5, 6))


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
        {"description": {"identifier": "geometry.rayquaza",
                         "texture_width": TW, "texture_height": TH,
                         "visible_bounds_width": 10, "visible_bounds_height": 5,
                         "visible_bounds_offset": [0, 1, 1]},
         "bones": bones},
        {"description": {"identifier": "geometry.dragon_pulse",
                         "texture_width": 16, "texture_height": 16,
                         "visible_bounds_width": 1, "visible_bounds_height": 1,
                         "visible_bounds_offset": [0, 0, 0]},
         "bones": [{"name": "core", "pivot": [0, 0, 0],
                    "cubes": [{"origin": [-2, -2, -2], "size": [4, 4, 4],
                               "uv": [0, 0]}]}]},
    ],
}

out = os.path.join(RP, "models/entity/rayquaza.geo.json")
with open(out, "w") as f:
    json.dump(geo, f, indent=2)
    f.write("\n")
print("wrote", out)


# ---------------------------------------------------------------- animations
# The whole rig is one travelling wave: every segment runs the same sine, each
# lagging the segment in front, so the curve moves head to tail instead of the
# body swinging as a unit.
CHAIN = [name for name, *_ in SEGMENTS]
FINS = [f"{p}_{s}_{seg}" for seg in ("body2", "body5", "tail")
        for p in ("finup", "findn") for s in ("left", "right")]
GILLS = ["gill_left", "gill_right"]


def wave(speed, lag, yaw, roll):
    """One bone chain running a sine that lags further back down the body."""
    out = {}
    for i, name in enumerate(CHAIN):
        p = i * lag
        out[name] = {"rotation": [
            0,
            f"math.sin(query.life_time * {speed} - {p}) * {yaw}",
            f"math.cos(query.life_time * {speed} - {p}) * {roll}",
        ]}
    return out


def flutter(speed, amp):
    out = {}
    for i, name in enumerate(FINS):
        out[name] = {"rotation": [
            f"math.sin(query.life_time * {speed} + {i * 30}) * {amp}", 0, 0]}
    for i, name in enumerate(GILLS):
        sign = 1 if name.endswith("left") else -1
        out[name] = {"rotation": [
            0, 0, f"math.sin(query.life_time * {speed * 0.8:g}) * {amp * 1.5 * sign:g}"]}
    return out


def arms(speed, amp, lift=0):
    out = {}
    for s, sign in (("left", 1), ("right", -1)):
        out[f"arm_{s}"] = {"rotation": [
            f"math.sin(query.life_time * {speed}) * {amp}", 0, lift * sign]}
        out[f"forearm_{s}"] = {"rotation": [
            f"math.sin(query.life_time * {speed} + 60) * {amp * 1.4:g}", 0, 0]}
        out[f"hand_{s}"] = {"rotation": [
            f"math.sin(query.life_time * {speed} + 120) * {amp:g}", 0, 0]}
    return out


def cheeks(amp, flare=0):
    out = {}
    for s, sign in (("left", 1), ("right", -1)):
        out[f"cheek_{s}"] = {"rotation": [
            f"math.sin(query.life_time * 110 + {60 if s == 'left' else 0}) * {amp}",
            0, flare * -sign]}
    return out


# Station keeping. Rayquaza never lands, so its rest pose is a slow coil that
# drifts up and down on the spot.
hover = {"loop": True, "bones": {
    "root": {
        "position": [0, "math.sin(query.life_time * 55) * 1.4", 0],
        "rotation": ["math.sin(query.life_time * 40) * 3", 0,
                     "math.sin(query.life_time * 32) * 5"],
    },
    "head": {"rotation": ["math.sin(query.life_time * 70) * 2",
                          "-math.sin(query.life_time * 95) * 4", 0]},
    "jaw": {"rotation": ["2 + math.sin(query.life_time * 45) * 2", 0, 0]},
}}
hover["bones"].update(wave(95, 50, 8, 3))
hover["bones"].update(flutter(120, 5))
hover["bones"].update(arms(70, 4))
hover["bones"].update(cheeks(3))

# Travelling. The wave tightens and speeds up, the body straightens out and the
# arms fold back along it.
glide = {"loop": True, "bones": {
    "root": {
        "position": [0, "math.sin(query.life_time * 110) * 0.7", 0],
        "rotation": [0, 0, "math.sin(query.life_time * 100) * 6"],
    },
    "head": {"rotation": [0, "-math.sin(query.life_time * 200) * 3", 0]},
    "jaw": {"rotation": [1, 0, 0]},
}}
glide["bones"].update(wave(200, 42, 5.5, 2))
glide["bones"].update(flutter(220, 7))
glide["bones"].update(arms(150, 5, lift=-18))
glide["bones"].update(cheeks(5))

# Hunting. Short fast wave, mouth open, jaw blades flared, claws forward.
hunt = {"loop": True, "bones": {
    "root": {
        "position": [0, "math.sin(query.life_time * 160) * 0.5", 0],
        "rotation": ["math.sin(query.life_time * 130) * 4", 0,
                     "math.sin(query.life_time * 150) * 8"],
    },
    "head": {"rotation": ["math.sin(query.life_time * 300) * 3",
                          "-math.sin(query.life_time * 300) * 2", 0]},
    "jaw": {"rotation": ["20 + math.sin(query.life_time * 240) * 9", 0, 0]},
}}
hunt["bones"].update(wave(300, 36, 4.5, 1.5))
hunt["bones"].update(flutter(320, 9))
hunt["bones"].update(arms(240, 8, lift=26))
hunt["bones"].update(cheeks(7, flare=14))

anims = {
    "format_version": "1.8.0",
    "animations": {
        "animation.rayquaza.hover": hover,
        "animation.rayquaza.glide": glide,
        "animation.rayquaza.hunt": hunt,
        "animation.rayquaza.look_at_target": {
            "loop": True,
            "bones": {"head": {"rotation": ["query.target_x_rotation",
                                            "query.target_y_rotation", 0]}},
        },
        "animation.dragon_pulse.spin": {
            "loop": True,
            "animation_length": 0.1,
            "particle_effects": {"0.0": {"effect": "trail"}},
            "bones": {"core": {"rotation": ["query.life_time * 620",
                                            "query.life_time * 480", 0]}},
        },
    },
}

out = os.path.join(RP, "animations/rayquaza.animation.json")
with open(out, "w") as f:
    json.dump(anims, f, indent=2)
    f.write("\n")
print("wrote", out)
