#!/usr/bin/env python3
"""Generates Galarian Moltres's geometry and animations.

Run from anywhere: python3 tools/gen_moltres.py
Writes models/entity/moltres.geo.json and animations/moltres.animation.json.
Run tools/gen_textures.py afterwards: it reads its UV slots back out of the
model, so a change here has to be followed through to the texture.

Galarian Moltres is a black bird carrying a magenta flame instead of feathers.
Everything that burns is its own bone, forty-odd cubes in all, because a flame
that never moves stops reading as fire the moment you look at it. The bones,
the UV net and the clips all come out of tables here for the same reason
Rayquaza's do: the net has to pack without overlap, the three wing joints have
to lag each other by the same amount every time, and neither survives being
edited a cube at a time.

Sizes stay whole numbers. A fractional width makes a fractional UV net, and
the net cannot land on whole pixels.
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RP = os.path.join(ROOT, "pikachu_RP")
TW, TH = 256, 128
CY = 17.0                      # the bird's centre line, one block up

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
                       "size": [int(v) for v in size]})


bone("root", pivot=(0, CY - 3, 0))

# Chest and rump are two boxes rather than one, so the body tapers back into
# the tail instead of ending in a wall. Both are kept narrow on purpose: the
# artwork is nearly all wing and flame, and a barrel chest eats that.
body = bone("body", "root", pivot=(0, CY, 0))
cube(body, (-4, 13, -9), (8, 9, 11))            # chest
cube(body, (-3, 13, 2), (6, 7, 7))              # rump

# The neck arcs down and forward and the head lifts back out of it, which is
# the S every long-necked bird holds in the air and the pose the artwork uses.
NECK = [("neck1", "body", (0, 21, -8), 12, (-2.5, 18.5, -14), (5, 5, 6)),
        ("neck2", "neck1", (0, 21, -14), 8, (-2, 19, -20), (4, 4, 6)),
        ("neck3", "neck2", (0, 21, -20), 4, (-2, 19, -25), (4, 4, 5))]
for name, parent, pivot, pitch, origin, size in NECK:
    n = bone(name, parent, pivot=pivot, rotation=(pitch, 0, 0))
    cube(n, origin, size)

head = bone("head", "neck3", pivot=(0, 21, -25), rotation=(-16, 0, 0))
cube(head, (-3, 18, -31), (6, 6, 6))            # skull
cube(head, (-2.5, 24, -30), (5, 1, 4))          # the scarlet cap over the eyes

# The beak is long, thin and hooked at the tip. The hook is its own cube so it
# keeps a hard step instead of tapering away into the jaw line.
beak = bone("beak", "head", pivot=(0, 21.5, -31))
cube(beak, (-1.5, 20, -39), (3, 3, 8))
cube(beak, (-1.5, 17, -39), (3, 3, 3))

jaw = bone("jaw", "head", pivot=(0, 20, -31))
cube(jaw, (-1, 18, -38), (2, 2, 7))

for s, x in (("left", 1), ("right", -1)):
    e = bone(f"eye_{s}", "head", pivot=(x * 3, 22, -29))
    cube(e, (2.9 if x > 0 else -3.9, 20.5, -30.5), (1, 2, 3))

# Every flame on the bird is a thin upright sheet raked backwards, never a
# slab. Fire has no volume to speak of, and a five-wide block of it reads as a
# crate painted pink.
CREST = [("crest1", "head", (0, 24, -27), -30, (-1, 24, -29), (2, 7, 5)),
         ("crest2", "crest1", (0, 31, -28), -45, (-1, 31, -30), (2, 6, 4)),
         ("crest3", "crest2", (0, 37, -29), -55, (-1, 37, -30), (2, 5, 3))]
for name, parent, pivot, pitch, origin, size in CREST:
    c = bone(name, parent, pivot=pivot, rotation=(pitch, 0, 0))
    cube(c, origin, size)

for s, x in (("left", 1), ("right", -1)):       # flame streaming off the nape
    p = bone(f"plume_{s}", "neck1", pivot=(x * 2.5, 22, -9),
             rotation=(-20, -25 * x, -30 * x))
    cube(p, (2 if x > 0 else -4, 22, -12), (2, 8, 9))

# Each wing is three joints out from the shoulder. Splitting it three ways is
# what lets the tip lag the shoulder in the flap; one bone per wing beats like
# a plank. A few degrees of sweep on each joint rakes the tip behind the
# shoulder, which is the difference between a bird and a cross.
WING = [("wing", "body", 4, (4, 20, -9), (10, 2, 14), 8, 8,
         ((6, 22, -2), (5, 22, -6), (2, 11, 10), -30, -20),
         ((11, 22, 0), (10, 22, -3), (2, 9, 9), -22, -28)),
        ("wingmid", "wing", 14, (14, 20, -8), (8, 2, 12), 10, 6,
         ((16, 22, -2), (15, 22, -5), (2, 10, 9), -28, -26),
         ((20, 22, 0), (19, 22, -2), (2, 8, 8), -20, -32)),
        ("wingtip", "wingmid", 22, (22, 20, -6), (7, 2, 10), 12, 5,
         ((24, 21, -2), (23, 21, -4), (2, 9, 8), -30, -30),
         ((27, 21, 0), (26, 21, -1), (2, 7, 7), -22, -38))]
for seg, parent, hinge, org, size, sweep, rake, *feathers in WING:
    for s, x in (("left", 1), ("right", -1)):
        p = "body" if parent == "body" else f"{parent}_{s}"
        w = bone(f"{seg}_{s}", p, pivot=(x * hinge, 21, -4),
                 rotation=(0, rake * x, sweep * x))
        cube(w, (org[0] if x > 0 else -org[0] - size[0], org[1], org[2]), size)
        for tag, (piv, forg, fsize, pitch, roll) in zip("ab", feathers):
            f = bone(f"flame_{seg}_{s}_{tag}", f"{seg}_{s}",
                     pivot=(x * piv[0], piv[1], piv[2]),
                     rotation=(pitch, 0, roll * x))
            cube(f, (forg[0] if x > 0 else -forg[0] - fsize[0],
                     forg[1], forg[2]), fsize)

# Tail: two black lengths, then four flames fanning off the end of them.
tail1 = bone("tail1", "body", pivot=(0, 18, 8), rotation=(6, 0, 0))
cube(tail1, (-3, 15, 8), (6, 5, 9))
tail2 = bone("tail2", "tail1", pivot=(0, 17.5, 17), rotation=(5, 0, 0))
cube(tail2, (-2.5, 15, 17), (5, 4, 8))

tf = bone("tailflame_c", "tail2", pivot=(0, 17, 25), rotation=(-10, 0, 0))
cube(tf, (-1, 15, 25), (2, 8, 12))
tu = bone("tailflame_up", "tail2", pivot=(0, 19, 22), rotation=(-38, 0, 0))
cube(tu, (-1, 19, 21), (2, 7, 10))
for s, x in (("left", 1), ("right", -1)):
    t = bone(f"tailflame_{s}", "tail1", pivot=(x * 3, 18, 14),
             rotation=(-15, -24 * x, -18 * x))
    cube(t, (2 if x > 0 else -4, 17, 14), (2, 9, 12))

# Legs hang scarlet and end in black talons, two forward and the heel behind.
for s, x in (("left", 1), ("right", -1)):
    t = bone(f"thigh_{s}", "body", pivot=(x * 3, 13, -1), rotation=(12, 0, 0))
    cube(t, (1.5 if x > 0 else -4.5, 7, -2.5), (3, 6, 3))
    sh = bone(f"shin_{s}", f"thigh_{s}", pivot=(x * 3, 7, -1), rotation=(-20, 0, 0))
    cube(sh, (2 if x > 0 else -4, 2, -2), (2, 5, 2))
    ft = bone(f"foot_{s}", f"shin_{s}", pivot=(x * 3, 2, -1))
    cube(ft, (2 if x > 0 else -4, 1, -5), (2, 1, 6))
    cube(ft, (1 if x > 0 else -5, 0, -7), (1, 1, 3))     # outer talon
    cube(ft, (3 if x > 0 else -3, 0, -7), (1, 1, 3))     # inner talon


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
        {"description": {"identifier": "geometry.moltres",
                         "texture_width": TW, "texture_height": TH,
                         "visible_bounds_width": 7, "visible_bounds_height": 5,
                         "visible_bounds_offset": [0, 1, 0]},
         "bones": bones},
        {"description": {"identifier": "geometry.fiery_wrath",
                         "texture_width": 16, "texture_height": 16,
                         "visible_bounds_width": 1, "visible_bounds_height": 1,
                         "visible_bounds_offset": [0, 0, 0]},
         "bones": [{"name": "core", "pivot": [0, 0, 0],
                    "cubes": [{"origin": [-2, -2, -2], "size": [4, 4, 4],
                               "uv": [0, 0]}]}]},
    ],
}

out = os.path.join(RP, "models/entity/moltres.geo.json")
with open(out, "w") as f:
    json.dump(geo, f, indent=2)
    f.write("\n")
print("wrote", out)


# ---------------------------------------------------------------- animations
# Three things move at once and they move on different clocks: the wings beat,
# the neck rides the beat a half cycle behind, and every flame flickers on top
# of both at a rate that has nothing to do with either.
JOINTS = [("wing", 0), ("wingmid", 40), ("wingtip", 80)]     # degrees of lag
FLAMES = [b["name"] for b in bones
          if b["name"].startswith(("flame_", "plume_", "crest", "tailflame_"))]


def flap(speed, amp, base, feather):
    """The wingbeat. Each joint out from the shoulder lags the one inside it.

    Left and right take the same expression with the roll negated, which is
    the only way a pair of wings stays a pair once the amplitude changes.
    """
    out = {}
    for i, (seg, lag) in enumerate(JOINTS):
        phase = f" - {lag}" if lag else ""
        beat = f"math.sin(query.life_time * {speed}{phase})"
        # the tip turns its leading edge into the stroke a quarter cycle early,
        # so the wing carves rather than swats
        pitch = (f"math.sin(query.life_time * {speed}{phase} + 90) "
                 f"* {feather * (i + 1) / 2:g}")
        for s, x in (("left", 1), ("right", -1)):
            roll = f"{base:g} + {beat} * {amp:g}"
            out[f"{seg}_{s}"] = {"rotation": [pitch, 0,
                                              roll if x < 0 else f"-({roll})"]}
    return out


def flicker(speed, amp):
    """Every flame bone, each one out of step with the last.

    Rotation alone reads as a wobble, so the scale breathes with it: a flame
    that grows and shrinks while it leans is the part that sells the fire.
    """
    out = {}
    for i, name in enumerate(FLAMES):
        t = f"query.life_time * {speed}"
        grow = f"1 + math.sin({t} * 1.3 + {i * 29}) * {amp / 110:.3f}"
        out[name] = {
            "rotation": [f"math.sin({t} + {i * 37}) * {amp:g}", 0,
                         f"math.cos({t} * 0.8 + {i * 53}) * {amp * 0.7:g}"],
            "scale": [grow, grow, grow],
        }
    return out


def neck(pitch, sway, speed):
    """Straightens or coils the arc, and rides it on the wingbeat."""
    out = {}
    for i, (name, *_) in enumerate(NECK):
        out[name] = {"rotation": [
            (f"{pitch:g} + " if pitch else "")
            + f"math.sin(query.life_time * {speed} + {i * 30}) * 2.5",
            f"math.sin(query.life_time * {speed * 0.4:g} + {i * 40}) * {sway:g}",
            0]}
    return out


def legs(thigh, shin, speed=0):
    out = {}
    for s in ("left", "right"):
        drift = (f" + math.sin(query.life_time * {speed}"
                 f"{' + 40' if s == 'right' else ''}) * 4") if speed else ""
        out[f"thigh_{s}"] = {"rotation": [f"{thigh:g}{drift}" if drift
                                          else thigh, 0, 0]}
        out[f"shin_{s}"] = {"rotation": [shin, 0, 0]}
    return out


def tail(spread, speed):
    out = {"tail1": {"rotation": [f"math.sin(query.life_time * {speed}) * 3",
                                  f"math.sin(query.life_time * {speed * 0.6:g}) * 4",
                                  0]},
           "tail2": {"rotation": [f"math.sin(query.life_time * {speed} - 40) * 4",
                                  f"math.sin(query.life_time * {speed * 0.6:g} - 50) * 5",
                                  0]}}
    for s, x in (("left", 1), ("right", -1)):
        out[f"tailflame_{s}"] = {"rotation": [0, -spread * x, 0]}
    return out


# Station keeping. Deep slow beats that carry the whole bird up and down on
# the stroke, legs hanging, head turning to watch the ground.
hover = {"loop": True, "bones": {
    "root": {
        "position": [0, "math.sin(query.life_time * 90 + 90) * 1.6", 0],
        "rotation": ["math.sin(query.life_time * 90) * 3", 0,
                     "math.sin(query.life_time * 34) * 4"],
    },
    "head": {"rotation": ["math.sin(query.life_time * 70) * 3",
                          "math.sin(query.life_time * 45) * 6", 0]},
    "jaw": {"rotation": ["3 + math.sin(query.life_time * 38) * 3", 0, 0]},
}}
hover["bones"].update(flap(90, 26, 6, 10))
hover["bones"].update(flicker(180, 6))
hover["bones"].update(neck(0, 5, 60))
hover["bones"].update(legs(6, -14, 50))
hover["bones"].update(tail(0, 55))

# Travelling. Wings held out and barely working, body tipped forward onto the
# line of flight, legs folded back under the tail, flames raked behind.
glide = {"loop": True, "bones": {
    "root": {
        "position": [0, "math.sin(query.life_time * 55) * 0.9", 0],
        "rotation": [6, 0, "math.sin(query.life_time * 48) * 7"],
    },
    "head": {"rotation": ["-4 + math.sin(query.life_time * 120) * 1.5",
                          "math.sin(query.life_time * 70) * 3", 0]},
    "jaw": {"rotation": [1, 0, 0]},
}}
glide["bones"].update(flap(55, 9, 2, 5))
glide["bones"].update(flicker(260, 8))
glide["bones"].update(neck(-9, 3, 90))
glide["bones"].update(legs(52, 62))
glide["bones"].update(tail(-6, 80))

# Hunting. Short hard beats, neck coiled back over the shoulders, beak wide,
# talons swung forward under the chest.
hunt = {"loop": True, "bones": {
    "root": {
        "position": [0, "math.sin(query.life_time * 190 + 90) * 0.8", 0],
        "rotation": ["4 + math.sin(query.life_time * 190) * 5", 0,
                     "math.sin(query.life_time * 120) * 9"],
    },
    "head": {"rotation": ["6 + math.sin(query.life_time * 260) * 4",
                          "math.sin(query.life_time * 150) * 4", 0]},
    "jaw": {"rotation": ["26 + math.sin(query.life_time * 210) * 8", 0, 0]},
}}
hunt["bones"].update(flap(190, 34, 10, 16))
hunt["bones"].update(flicker(420, 11))
hunt["bones"].update(neck(7, 7, 200))
hunt["bones"].update(legs(-38, -22, 160))
hunt["bones"].update(tail(9, 170))

# Head tracking is shared out down the whole neck instead of landing on the
# skull. A bird turns to look; only the last third of the turn is its head,
# and putting it all on one bone snaps the beak off the end of the neck.
track = {}
for name, w in (("neck1", 0.25), ("neck2", 0.25), ("neck3", 0.2), ("head", 0.3)):
    track[name] = {"rotation": [f"query.target_x_rotation * {w:g}",
                                f"query.target_y_rotation * {w:g}", 0]}

anims = {
    "format_version": "1.8.0",
    "animations": {
        "animation.moltres.hover": hover,
        "animation.moltres.glide": glide,
        "animation.moltres.hunt": hunt,
        "animation.moltres.look_at_target": {"loop": True, "bones": track},
        "animation.fiery_wrath.spin": {
            "loop": True,
            "animation_length": 0.1,
            "particle_effects": {"0.0": {"effect": "trail"}},
            "bones": {"core": {"rotation": ["query.life_time * 540",
                                            "query.life_time * 700", 0]}},
        },
    },
}

out = os.path.join(RP, "animations/moltres.animation.json")
with open(out, "w") as f:
    json.dump(anims, f, indent=2)
    f.write("\n")
print("wrote", out)
