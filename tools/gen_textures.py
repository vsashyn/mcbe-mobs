#!/usr/bin/env python3
"""Generates every entity texture in the add-on, plus both pack icons.

Run from anywhere: python3 tools/gen_textures.py
Writes pikachu.png (64x64), arboliva.png (128x64), thunder_shock.png and
oil_salvo.png (16x16), and both pack_icon.png.

Pikachu's UV slots are written out here and have to stay in step with
models/entity/pikachu.geo.json by hand. Arboliva's are read straight off
models/entity/arboliva.geo.json instead, which is the better way round: 25
cubes are too many to keep in step twice.

Each cube claims a Minecraft box-UV net: 2*depth + 2*width wide, depth +
height tall. On a side face, texture row 0 is the top of the cube.
"""
import json
import math
import os
import random
import struct
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def write_png(path, w, h, px):
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        for x in range(w):
            raw.extend(px[y][x])

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))

    out = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + chunk(b"IEND", b""))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(out)


def canvas(w, h):
    return [[(0, 0, 0, 0) for _ in range(w)] for _ in range(h)]


def rect(px, x, y, w, h, c):
    for j in range(y, y + h):
        for i in range(x, x + w):
            if 0 <= j < len(px) and 0 <= i < len(px[0]):
                px[j][i] = c


def put(px, x, y, c):
    px[y][x] = c


# Pikachu is a single yellow ramp. The only other colours are the black ear
# tips, the eyes and the red cheeks.
A = 255
YEL     = (242, 203, 48, A)
YEL_HI  = (255, 226, 104, A)
YEL_LO  = (214, 168, 28, A)
YEL_LO2 = (188, 143, 20, A)
BELLY   = (252, 222, 120, A)
BLK     = (43, 43, 43, A)
BLK_HI  = (72, 72, 72, A)
RED     = (226, 75, 59, A)
RED_HI  = (240, 110, 92, A)
EYE     = (26, 24, 22, A)
WHT     = (255, 255, 255, A)
MOUTH   = (74, 48, 32, A)
NOSE    = (198, 148, 66, A)
SPARK   = (255, 245, 170, A)
SPARK_C = (255, 255, 255, A)

# Arboliva: leaf green, tan bark, a cream face and deep purple olives.
LEAF      = (124, 196, 96, A)
LEAF_HI   = (176, 228, 128, A)
LEAF_LO   = (86, 152, 66, A)
LEAF_LO2  = (62, 118, 50, A)
TRUNK     = (178, 134, 94, A)
TRUNK_HI  = (206, 168, 124, A)
TRUNK_LO  = (134, 96, 64, A)
TRUNK_LO2 = (104, 72, 46, A)
CREAM     = (244, 240, 226, A)
CREAM_LO  = (206, 198, 180, A)
PLUM      = (132, 54, 108, A)
PLUM_HI   = (176, 96, 150, A)
PLUM_LO   = (88, 34, 72, A)
LID       = (78, 64, 60, A)
MOUTH_A   = (122, 86, 72, A)
OIL       = (94, 80, 34, A)
OIL_HI    = (172, 152, 66, A)
OIL_LO    = (58, 48, 20, A)

# Shiny Rayquaza is charcoal where the ordinary one is emerald, so almost
# every pixel is one of three near-blacks and the whole read has to come
# from the accents: yellow rings, red-outlined belts, pale grey blades.
SCALE     = (68, 66, 74, A)
SCALE_HI  = (104, 102, 112, A)
SCALE_LO  = (40, 39, 45, A)
RAY_YEL   = (247, 214, 43, A)
RAY_RED   = (198, 48, 58, A)
BLADE     = (142, 146, 152, A)
BLADE_LO  = (94, 98, 104, A)
IRIS      = (250, 214, 60, A)
SLIT      = (18, 17, 20, A)
MAW       = (222, 96, 112, A)
FANG      = (242, 244, 248, A)
PULSE     = (128, 74, 196, A)
PULSE_HI  = (204, 162, 252, A)
PULSE_LO  = (72, 36, 120, A)


# Kleavor: sand-coloured chitin, chipped stone plates, and two axe heads that
# are the same stone a shade cooler. The only bright pixels on it are the eyes
# and the horn, which is what makes the face read at mob scale.
CHIT     = (203, 169, 119, A)
CHIT_HI  = (230, 201, 153, A)
CHIT_LO  = (166, 133, 86, A)
CHIT_LO2 = (126, 98, 58, A)
ROCK     = (74, 58, 53, A)
ROCK_HI  = (106, 86, 76, A)
ROCK_LO  = (46, 35, 31, A)
EDGE     = (146, 130, 118, A)
PALE     = (231, 220, 194, A)
PALE_HI  = (246, 240, 224, A)
PALE_LO  = (196, 182, 152, A)
BONE     = (238, 234, 220, A)
BONE_LO  = (196, 190, 170, A)
EYE_W    = (247, 247, 242, A)


# Squirtle is three materials and nothing else: blue hide, a red-brown shell
# and the cream plastron between them. The eyes are the only warm pixels on
# the front of it, so they carry the whole face.
AQUA     = (108, 186, 212, A)
AQUA_HI  = (150, 214, 232, A)
AQUA_LO  = (78, 150, 178, A)
AQUA_LO2 = (56, 118, 146, A)
SHELL    = (166, 88, 58, A)
SHELL_HI = (198, 118, 82, A)
SHELL_LO = (126, 62, 40, A)
SHELL_LO2 = (94, 44, 28, A)
PLATE    = (238, 222, 168, A)
PLATE_HI = (250, 240, 202, A)
PLATE_LO = (206, 186, 130, A)
PLATE_LO2 = (168, 148, 98, A)
RIM      = (246, 240, 226, A)
MAROON   = (124, 48, 84, A)
MAROON_HI = (176, 78, 122, A)
PUPIL    = (46, 20, 34, A)
CLAW     = (238, 232, 214, A)
JET      = (150, 214, 246, A)
JET_HI   = (232, 250, 255, A)
JET_LO   = (86, 152, 200, A)


def faces(u, v, w, h, d):
    """Minecraft box-UV net: (x, y, w, h) per face."""
    return {
        "top":    (u + d,         v,     w, d),
        "bottom": (u + d + w,     v,     w, d),
        "right":  (u,             v + d, d, h),   # -x
        "front":  (u + d,         v + d, w, h),   # -z
        "left":   (u + d + w,     v + d, d, h),   # +x
        "back":   (u + d + w + d, v + d, w, h),   # +z
    }


def paint_box(px, u, v, w, h, d, base, top=None, bottom=None, back=None):
    f = faces(u, v, w, h, d)
    for name, col in (("top", top or base), ("bottom", bottom or base),
                      ("back", back or base), ("right", base),
                      ("front", base), ("left", base)):
        x, y, fw, fh = f[name]
        rect(px, x, y, fw, fh, col)
    return f


def speckle(px, x, y, w, h, col, seed, density=0.16):
    rnd = random.Random(seed)
    for j in range(y, y + h):
        for i in range(x, x + w):
            if rnd.random() < density:
                px[j][i] = col


# ---------------------------------------------------------------- pikachu.png
tex = canvas(64, 64)

# head 8x7x7 at uv(0,0)
hf = paint_box(tex, 0, 0, 8, 7, 7, YEL, top=YEL_HI, bottom=YEL_LO)
for side in ("right", "left", "back"):
    x, y, w, h = hf[side]
    rect(tex, x, y + h - 1, w, 1, YEL_LO)          # shadow under the jaw
speckle(tex, *hf["top"], YEL_HI, seed=1, density=0.10)

fx, fy, _, _ = hf["front"]


def face(c, r, col):
    put(tex, fx + c, fy + r, col)


for c in range(8):
    face(c, 0, YEL_HI)                             # brow catches the light
for ex, gx in ((1, 2), (5, 5)):                    # eyes, mirrored glints
    for c in (ex, ex + 1):
        for r in (1, 2):
            face(c, r, EYE)
    face(gx, 1, WHT)
for cx in (0, 6):                                  # cheek pouches
    for c in (cx, cx + 1):
        for r in (3, 4):
            face(c, r, RED)
    face(cx, 3, RED_HI)
face(3, 3, NOSE)                                   # nose, soft enough to recede
face(4, 3, NOSE)
face(2, 4, MOUTH)                                  # mouth: a flattened "w"
face(5, 4, MOUTH)
face(3, 5, MOUTH)
face(4, 5, MOUTH)

# body 6x5x5 at uv(32,0)
bf = paint_box(tex, 32, 0, 6, 5, 5, YEL, top=YEL_HI, bottom=YEL_LO2)
x, y, w, h = bf["front"]
rect(tex, x, y + 1, w, h - 1, BELLY)               # pale belly

# arms 2x4x2
for u in (0, 10):
    af = paint_box(tex, u, 16, 2, 4, 2, YEL, top=YEL_HI, bottom=YEL_LO2)
    for side in ("right", "front", "left", "back"):
        x, y, w, h = af[side]
        rect(tex, x, y + h - 1, w, 1, YEL_LO)      # paws sit a shade darker

# legs 3x3x3
for u in (20, 34):
    lf = paint_box(tex, u, 16, 3, 3, 3, YEL, top=YEL_LO, bottom=YEL_LO2)
    for side in ("right", "front", "left", "back"):
        x, y, w, h = lf[side]
        rect(tex, x, y + h - 1, w, 1, YEL_LO)      # feet sit a shade darker

# ears: yellow base, black tip
for u in (0, 16):
    paint_box(tex, u, 24, 2, 6, 1, YEL, top=YEL_HI, bottom=YEL_LO)
for u in (8, 24):
    ef = paint_box(tex, u, 24, 2, 3, 1, BLK, top=BLK_HI, bottom=BLK)
    x, y, w, h = ef["front"]
    rect(tex, x, y, w, 1, BLK_HI)

# tail: one solid yellow bolt, no banding
for u, w, hh, d in ((0, 2, 2, 2), (10, 2, 2, 2), (20, 2, 2, 2), (30, 2, 3, 5)):
    paint_box(tex, u, 32, w, hh, d, YEL, top=YEL_HI, bottom=YEL_LO)

write_png(os.path.join(ROOT, "pikachu_RP/textures/entity/pikachu/pikachu.png"),
          64, 64, tex)

# --------------------------------------------------------- thunder_shock.png
sp = canvas(16, 16)
sf = paint_box(sp, 0, 0, 3, 3, 3, SPARK, top=SPARK_C, bottom=SPARK)
for name in sf:
    x, y, w, h = sf[name]
    put(sp, x + w // 2, y + h // 2, SPARK_C)
write_png(os.path.join(ROOT,
          "pikachu_RP/textures/entity/pikachu/thunder_shock.png"), 16, 16, sp)


# --------------------------------------------------------------- arboliva.png
# Painted off the model rather than off a second copy of the UV table, so the
# slots cannot drift out of step with models/entity/arboliva.geo.json. Each
# bone name picks a material; the tree is bark, foliage, one face and fruit.
GEO = os.path.join(ROOT, "pikachu_RP/models/entity/arboliva.geo.json")
arb = next(g for g in json.load(open(GEO))["minecraft:geometry"]
           if g["description"]["identifier"] == "geometry.arboliva")
tex = canvas(arb["description"]["texture_width"],
             arb["description"]["texture_height"])

SIDES = ("right", "front", "left", "back")


def bark(u, v, w, h, d, seed):
    """One lit column and one shaded column per face rounds the trunk off."""
    f = paint_box(tex, u, v, w, h, d, TRUNK, top=TRUNK_HI, bottom=TRUNK_LO2)
    for side in SIDES:
        x, y, fw, fh = f[side]
        rect(tex, x + 1, y, 1, fh, TRUNK_HI)
        rect(tex, x + fw - 1, y, 1, fh, TRUNK_LO)
        rect(tex, x, y + fh - 1, fw, 1, TRUNK_LO2)     # dark toward the roots
        speckle(tex, x, y + 1, fw, max(fh - 2, 1), TRUNK_LO,
                seed=seed + x, density=0.07)           # knots
    return f


def foliage(u, v, w, h, d, seed):
    f = paint_box(tex, u, v, w, h, d, LEAF, top=LEAF_HI, bottom=LEAF_LO2)
    speckle(tex, *f["top"], LEAF, seed=seed, density=0.22)
    for side in SIDES:
        x, y, fw, fh = f[side]
        rect(tex, x, y, fw, 1, LEAF_HI)                # lit on the upper rim
        rect(tex, x, y + fh - 1, fw, 1, LEAF_LO)       # shaded underneath
        speckle(tex, x, y + 1, fw, max(fh - 2, 1), LEAF_LO,
                seed=seed + x, density=0.12)
    return f


def fruit(u, v, w, h, d, seed):
    f = paint_box(tex, u, v, w, h, d, PLUM, top=PLUM_LO, bottom=PLUM_LO)
    for side in SIDES:
        x, y, fw, fh = f[side]
        rect(tex, x, y, fw, 1, PLUM_LO)                # shade at the stem
        put(tex, x, y + 2, PLUM_HI)                    # one gloss pixel
    return f


def facing(u, v, w, h, d, seed):
    """The trunk's top segment: cream, closed eyes, blending into bark below."""
    f = paint_box(tex, u, v, w, h, d, CREAM, top=LEAF_LO, bottom=TRUNK)
    for side in SIDES:
        x, y, fw, fh = f[side]
        rect(tex, x, y, fw, 1, CREAM_LO)               # shade off the canopy
        rect(tex, x, y + fh - 1, fw, 1, TRUNK_HI)      # meets the trunk
    x, y, fw, fh = f["front"]
    for c in (0, 1, 3, 4):
        put(tex, x + c, y + 3, LID)                    # eyes, closed
    put(tex, x, y + 4, CREAM_LO)                       # crease under each lid
    put(tex, x + 4, y + 4, CREAM_LO)
    put(tex, x + 2, y + 5, MOUTH_A)
    return f


MATERIAL = (
    ("olive", fruit),
    ("head", facing),
    ("crown", foliage),
    ("blade", foliage),
    ("branch", foliage),
    ("frond", foliage),
    ("body", bark),
    ("leg", bark),
)

for bone in arb["bones"]:
    paint = next(fn for pre, fn in MATERIAL if bone["name"].startswith(pre))
    for i, cube in enumerate(bone.get("cubes", [])):
        u, v = cube["uv"]
        w, h, d = (int(n) for n in cube["size"])
        paint(u, v, w, h, d, u + v + i)

write_png(os.path.join(ROOT,
          "pikachu_RP/textures/entity/arboliva/arboliva.png"),
          arb["description"]["texture_width"],
          arb["description"]["texture_height"], tex)

# ------------------------------------------------------------- oil_salvo.png
og = canvas(16, 16)
gf = paint_box(og, 0, 0, 3, 3, 3, OIL, top=OIL_HI, bottom=OIL_LO)
for name in gf:
    x, y, w, h = gf[name]
    put(og, x + w // 2, y + h // 2, OIL_HI)
write_png(os.path.join(ROOT,
          "pikachu_RP/textures/entity/arboliva/oil_salvo.png"), 16, 16, og)


# --------------------------------------------------------------- rayquaza.png
# Fifty-odd cubes is too many to keep a hand-written copy of the UV table
# honest against the model, so this one reads its slots back out of the
# geometry that owns them and addresses each cube by bone name.
RAY_GEO = json.load(open(os.path.join(
    ROOT, "pikachu_RP/models/entity/rayquaza.geo.json")))
RAY_BONES = {
    b["name"]: [(c["uv"][0], c["uv"][1], *(int(n) for n in c["size"]))
                for c in b.get("cubes", [])]
    for g in RAY_GEO["minecraft:geometry"]
    if g["description"]["identifier"] == "geometry.rayquaza"
    for b in g["bones"]
}

tex = canvas(128, 128)


def scales(bone, i=0, base=SCALE, top=SCALE_HI, bottom=SCALE_LO):
    """Paints one cube of a bone in body colours and hands back its net."""
    u, v, w, h, d = RAY_BONES[bone][i]
    return paint_box(tex, u, v, w, h, d, base, top=top, bottom=bottom)


def girdle(f, rows, col, sides=("top", "bottom", "right", "left")):
    """Wraps a stripe around a segment at a fixed depth.

    Depth runs down the rows of the top and bottom faces and across the
    columns of the two side faces. Rows are counted out from the middle of
    the face, so the stripe stays centred whichever way round it unwraps.
    """
    for name in sides:
        x, y, fw, fh = f[name]
        for r in rows:
            if name in ("top", "bottom"):
                rect(tex, x, y + fh // 2 + r, fw, 1, col)
            else:
                rect(tex, x + fw // 2 + r, y, 1, fh, col)


def outline(f, name, col):
    x, y, fw, fh = f[name]
    rect(tex, x, y, fw, 1, col)
    rect(tex, x, y + fh - 1, fw, 1, col)
    rect(tex, x, y, 1, fh, col)
    rect(tex, x + fw - 1, y, 1, fh, col)


def belly(f, col=RAY_YEL):
    x, y, fw, fh = f["bottom"]
    rect(tex, x + (fw - 1) // 2, y, 1, fh, col)


# skull and upper snout. The snout underside doubles as the roof of the mouth,
# which is the only place the model shows any colour that is not near-black.
skull = scales("head", 0)
belly(skull)
snout = scales("head", 1)
x, y, fw, fh = snout["bottom"]
rect(tex, x, y, fw, fh, MAW)
rect(tex, x, y, 1, fh, FANG)
rect(tex, x + fw - 1, y, 1, fh, FANG)

for face in ("right", "left"):
    x, y, fw, fh = snout[face]
    rect(tex, x, y + fh - 1, fw, 1, SLIT)           # mouth line, upper half

jaw = scales("jaw")
for face in ("right", "left"):
    x, y, fw, fh = jaw[face]
    rect(tex, x, y, fw, 1, SLIT)                    # mouth line, lower half
x, y, fw, fh = jaw["top"]
rect(tex, x, y, fw, fh, MAW)
rect(tex, x, y, 1, fh, FANG)
rect(tex, x + fw - 1, y, 1, fh, FANG)

plate = scales("disc", base=RAY_YEL, top=BLADE, bottom=SCALE_LO)
x, y, fw, fh = plate["top"]
rect(tex, x + 1, y + 1, fw - 2, fh - 2, BLADE_LO)

for side in ("left", "right"):
    scales(f"brow_{side}", base=SCALE_HI, top=SCALE_HI, bottom=SLIT)
    # the eye is its own slab so the pupil never depends on which way round
    # a side face happens to unwrap
    eye = scales(f"eye_{side}", base=SCALE_LO, top=SCALE_LO, bottom=SCALE_LO)
    x, y, fw, fh = eye[side]
    rect(tex, x, y, fw, fh, IRIS)
    rect(tex, x, y, fw, 1, SLIT)                    # heavy lid
    rect(tex, x + fw // 2, y + 1, 1, fh - 1, SLIT)  # slit pupil

    bf = scales(f"cheek_{side}", base=BLADE, top=BLADE_LO, bottom=BLADE_LO)
    for face in ("left", "right"):
        outline(bf, face, BLADE_LO)

# every fin is the same object: a charcoal web with a red rim on the two
# broad faces, which is what the red rudders on the real thing read as
for bone in RAY_BONES:
    if bone.startswith(("finup_", "findn_", "gill_")):
        # a fin's tip is the far end from the body, which for the pair hanging
        # underneath is the bottom of its net rather than the top
        tip = "bottom" if bone.startswith("findn_") else "top"
        ff = scales(bone, top=SCALE_LO, bottom=SCALE_LO)
        rect(tex, *ff[tip], RAY_RED)
        for face in ("left", "right"):
            x, y, fw, fh = ff[face]
            rect(tex, x, y if tip == "top" else y + fh - 1, fw, 1, RAY_RED)

for side in ("left", "right"):
    for limb in (f"arm_{side}", f"forearm_{side}"):
        scales(limb)
    scales(f"hand_{side}", 0)
    for i in range(1, len(RAY_BONES[f"hand_{side}"])):
        scales(f"hand_{side}", i, base=FANG, top=FANG, bottom=BLADE_LO)

# the serpent itself. Hollow yellow rings and red-staple belts alternate down
# the body the way they do in the artwork; the belt skips the underside, so it
# reads as a staple laid over the back rather than a hoop.
RINGS = ("neck", "body3", "body6", "body8")
BELTS = ("body1", "body4", "body7")
for bone, cubes in RAY_BONES.items():
    if bone != "neck" and not bone.startswith("body") and bone != "tail":
        continue
    sf = scales(bone)
    for name in ("top", "bottom"):
        x, y, fw, fh = sf[name]
        rect(tex, x, y, fw, 1, SCALE_LO)
        rect(tex, x, y + fh - 1, fw, 1, SCALE_LO)
    if bone in RINGS:
        girdle(sf, (-2, 1), RAY_YEL)
    elif bone in BELTS:
        girdle(sf, (-2, 2), RAY_RED, sides=("top", "right", "left"))
    if bone in ("neck", "body1", "body2"):
        belly(sf)

write_png(os.path.join(ROOT,
          "pikachu_RP/textures/entity/rayquaza/rayquaza.png"), 128, 128, tex)

# ------------------------------------------------------------ dragon_pulse.png
dp = canvas(16, 16)
df = paint_box(dp, 0, 0, 4, 4, 4, PULSE, top=PULSE_HI, bottom=PULSE_LO)
for name in df:
    x, y, w, h = df[name]
    rect(dp, x + 1, y + 1, w - 2, h - 2, PULSE_HI)
    put(dp, x + w // 2, y + h // 2, RAY_YEL)
write_png(os.path.join(ROOT,
          "pikachu_RP/textures/entity/rayquaza/dragon_pulse.png"), 16, 16, dp)


# --------------------------------------------------------------- kleavor.png
# Same trick as arboliva: the slots are read back out of the model, and a bone
# name picks the material. Kleavor needs one extra rule, because an axe arm is
# a stone wrist plus the two slabs that make up the blade.
#
# Every plate gets a dark border. Kleavor is one flat tan all over, so without
# an outline per cube the chest, the hanging plate and both thighs merge into a
# single tan mass at mob scale.
KLE_GEO = os.path.join(ROOT, "pikachu_RP/models/entity/kleavor.geo.json")
kle = next(g for g in json.load(open(KLE_GEO))["minecraft:geometry"]
           if g["description"]["identifier"] == "geometry.kleavor")
tex = canvas(kle["description"]["texture_width"],
             kle["description"]["texture_height"])


def outlined(u, v, w, h, d, base, hi, lo, edge):
    f = paint_box(tex, u, v, w, h, d, base, top=hi, bottom=lo)
    for name in f:
        x, y, fw, fh = f[name]
        if fw >= 3 and fh >= 2:
            rect(tex, x, y, fw, 1, edge)
            rect(tex, x, y + fh - 1, fw, 1, edge)
        if fw >= 2 and fh >= 3:
            rect(tex, x, y, 1, fh, edge)
            rect(tex, x + fw - 1, y, 1, fh, edge)
    for side in SIDES:
        x, y, fw, fh = f[side]
        if fw >= 3 and fh >= 3:
            rect(tex, x + 1, y + 1, fw - 2, 1, hi)     # lit just inside the rim
    return f


def chitin(u, v, w, h, d, seed):
    """Shell plate: flat tan inside a hard edge."""
    return outlined(u, v, w, h, d, CHIT, CHIT_HI, CHIT_LO, CHIT_LO2)


def pale(u, v, w, h, d, seed):
    """The joints. Nearly bone-white, which is what separates the thin
    segments from the tan plates they hang off."""
    return outlined(u, v, w, h, d, PALE, PALE_HI, PALE_LO, CHIT_LO)


def stone(u, v, w, h, d, seed):
    """Plate armour: chipped, so the speckle carries both directions."""
    f = paint_box(tex, u, v, w, h, d, ROCK, top=ROCK_HI, bottom=ROCK_LO)
    for name in f:
        x, y, fw, fh = f[name]
        speckle(tex, x, y, fw, fh, ROCK_LO, seed=seed + x, density=0.18)
        speckle(tex, x, y, fw, fh, ROCK_HI, seed=seed + x + 7, density=0.10)
    for side in SIDES:
        x, y, fw, fh = f[side]
        rect(tex, x, y, fw, 1, ROCK_HI)                # facet catching the light
        rect(tex, x, y + fh - 1, fw, 1, ROCK_LO)
    return f


def blade(u, v, w, h, d, seed):
    """An axe slab. Its broad faces are the two w by h ones, front and back.

    The honed edge is the far rim and the underside, so those get the pale
    line and the broad faces get a border to match. Everything else stays
    flat and dark, the way the axes read in the artwork.
    """
    f = paint_box(tex, u, v, w, h, d, ROCK, top=ROCK_LO, bottom=EDGE)
    for name in ("front", "back"):
        x, y, fw, fh = f[name]
        speckle(tex, x, y, fw, fh, ROCK_LO, seed=seed + x, density=0.14)
        speckle(tex, x, y, fw, fh, ROCK_HI, seed=seed + x + 3, density=0.05)
        rect(tex, x, y + fh - 1, fw, 1, EDGE)          # honed underside
    x, y, fw, fh = f["front"]
    rect(tex, x + fw - 1, y, 1, fh, EDGE)              # +x rim, front face
    x, y, fw, fh = f["back"]
    rect(tex, x, y, 1, fh, EDGE)                       # same rim, unwrapped
    for side in ("right", "left"):
        x, y, fw, fh = f[side]
        rect(tex, x, y + fh - 1, fw, 1, EDGE)
    return f


def horn(u, v, w, h, d, seed):
    f = paint_box(tex, u, v, w, h, d, BONE, top=BONE, bottom=BONE_LO)
    for side in SIDES:
        x, y, fw, fh = f[side]
        rect(tex, x, y + fh - 1, fw, 1, BONE_LO)       # dirty where it meets rock
    return f


def visor(u, v, w, h, d, seed):
    """The head, 8 across. Two white eyes, each cut away toward the middle,
    which is the whole of Kleavor's expression."""
    f = chitin(u, v, w, h, d, seed)
    x, y, fw, fh = f["front"]

    def px(c, r, col):
        put(tex, x + c, y + r, col)

    rect(tex, x, y, fw, 1, CHIT_LO)                    # shadow off the helm
    for out, mid, inn in ((0, 1, 2), (7, 6, 5)):
        px(inn, 0, EYE)                                # brow, low on the inside
        px(out, 1, EYE_W)
        px(mid, 1, EYE_W)
        px(inn, 1, EYE)
        px(out, 2, EYE_W)
        px(mid, 2, EYE)
        px(inn, 2, EYE)
    for c in (2, 3, 4, 5):
        px(c, 3, ROCK)                                 # mandible plate
    px(2, 4, ROCK_HI)
    px(5, 4, ROCK_HI)
    px(3, 4, CHIT_LO2)
    px(4, 4, CHIT_LO2)
    return f


KLE_MATERIAL = (
    ("axe", stone),          # cube 0 is the wrist; the slabs are handled below
    ("rock", stone),
    ("claw", stone),
    ("horn", horn),
    ("head", visor),
    ("neck", pale),
    ("forearm", pale),
    ("shin", pale),
    ("body", chitin),
    ("abdomen", chitin),
    ("arm", chitin),
    ("leg", chitin),
    ("foot", chitin),
)

for bone in kle["bones"]:
    for i, cube in enumerate(bone.get("cubes", [])):
        if bone["name"].startswith("axe") and i > 0:
            paint = blade
        else:
            paint = next(fn for pre, fn in KLE_MATERIAL
                         if bone["name"].startswith(pre))
        u, v = cube["uv"]
        w, h, d = (int(n) for n in cube["size"])
        paint(u, v, w, h, d, u + v + i)

write_png(os.path.join(ROOT, "pikachu_RP/textures/entity/kleavor/kleavor.png"),
          kle["description"]["texture_width"],
          kle["description"]["texture_height"], tex)


# --------------------------------------------------------------- squirtle.png
# Read off the model, the same way arboliva and kleavor are.
#
# The one thing worth knowing here is which edge of a face is the front of the
# cube, because the shell's cream rim is drawn along it. The box-UV net
# unwraps right, front, left, back in that order, so on the right face the
# front-most column is the last one and on the left face it is the first. The
# top face's last row and the bottom face's first row meet the front the same
# way.
SQ_GEO = os.path.join(ROOT, "pikachu_RP/models/entity/squirtle.geo.json")
squ = next(g for g in json.load(open(SQ_GEO))["minecraft:geometry"]
           if g["description"]["identifier"] == "geometry.squirtle")
tex = canvas(squ["description"]["texture_width"],
             squ["description"]["texture_height"])


def hide(u, v, w, h, d, seed):
    """Blue skin: lit along the top rim of every side, shaded along the bottom."""
    f = paint_box(tex, u, v, w, h, d, AQUA, top=AQUA_HI, bottom=AQUA_LO2)
    for side in SIDES:
        x, y, fw, fh = f[side]
        rect(tex, x, y, fw, 1, AQUA_HI)
        rect(tex, x, y + fh - 1, fw, 1, AQUA_LO)
    return f


def limb(u, v, w, h, d, seed):
    """An arm or a leg. Same hide, plus pale claws on the leading edge and a
    sole dark enough to read as a foot rather than more of the limb."""
    f = hide(u, v, w, h, d, seed)
    x, y, fw, fh = f["bottom"]
    rect(tex, x, y, fw, fh, AQUA_LO)
    x, y, fw, fh = f["front"]
    for c in range(0, fw, 2):
        put(tex, x + c, y + fh - 1, CLAW)
    return f


def carapace(u, v, w, h, d, seed):
    """The shell. Four plates split by a seam, a cream rim where it meets the
    body, and enough speckle to keep the brown from going flat."""
    f = paint_box(tex, u, v, w, h, d, SHELL, top=SHELL_HI, bottom=SHELL_LO2)
    for name in f:
        x, y, fw, fh = f[name]
        speckle(tex, x, y, fw, fh, SHELL_LO, seed=seed + x, density=0.10)
    for side in SIDES:
        x, y, fw, fh = f[side]
        rect(tex, x, y, fw, 1, SHELL_HI)
        rect(tex, x, y + fh - 1, fw, 1, SHELL_LO2)
    x, y, fw, fh = f["back"]                            # the dome, seen from behind
    rect(tex, x, y, fw, 1, SHELL_LO2)
    rect(tex, x, y + fh - 1, fw, 1, SHELL_LO2)
    rect(tex, x + fw // 2, y, 1, fh, SHELL_LO2)         # seam down the middle
    rect(tex, x, y + fh // 2, fw, 1, SHELL_LO2)         # and across
    x, y, fw, fh = f["right"]                           # rim, front edge of -x
    rect(tex, x + fw - 1, y, 1, fh, RIM)
    x, y, fw, fh = f["left"]                            # rim, front edge of +x
    rect(tex, x, y, 1, fh, RIM)
    x, y, fw, fh = f["top"]
    rect(tex, x, y + fh - 1, fw, 1, RIM)
    x, y, fw, fh = f["bottom"]
    rect(tex, x, y, fw, 1, RIM)
    return f


def plastron(u, v, w, h, d, seed):
    """The belly shield: cream scutes cut into six panels by a hard seam. Its
    back face is buried inside the shell, so it takes the shell's colour."""
    f = paint_box(tex, u, v, w, h, d, PLATE, top=PLATE_LO, bottom=PLATE_LO2,
                  back=SHELL_LO)
    for side in ("right", "front", "left"):
        x, y, fw, fh = f[side]
        rect(tex, x, y, fw, 1, PLATE_HI)
        rect(tex, x, y + fh - 1, fw, 1, PLATE_LO)
    x, y, fw, fh = f["front"]
    rect(tex, x, y, 1, fh, PLATE_LO2)
    rect(tex, x + fw - 1, y, 1, fh, PLATE_LO2)
    rect(tex, x, y + fh - 1, fw, 1, PLATE_LO2)
    rect(tex, x + fw // 2, y, 1, fh, PLATE_LO2)         # centre seam
    rect(tex, x, y + 1, fw, 1, PLATE_LO2)               # two seams across, so
    rect(tex, x, y + 3, fw, 1, PLATE_LO2)               # the shield reads as six
    return f


def visage(u, v, w, h, d, seed):
    """The head. Two tall maroon eyes with a highlight turned outward, a lit
    brow above them and a shaded jaw under the muzzle."""
    f = hide(u, v, w, h, d, seed)
    x, y, fw, fh = f["front"]

    def px(c, r, col):
        put(tex, x + c, y + r, col)

    for c in range(fw):
        px(c, 0, AQUA_HI)                               # brow catches the light
    for c0, glint in ((1, 1), (5, 6)):
        for c in (c0, c0 + 1):
            for r in (1, 2, 3):
                px(c, r, MAROON)
            px(c, 3, PUPIL)                             # eye darkens at the base
        px(glint, 1, WHT)
        px(glint, 2, MAROON_HI)
    for c in (0, 7):                                    # cheeks fall away
        px(c, 4, AQUA_LO)
        px(c, 5, AQUA_LO)
    rect(tex, x, y + fh - 1, fw, 1, AQUA_LO2)           # jaw, under the muzzle
    return f


def muzzle(u, v, w, h, d, seed):
    """The snout: nostrils on top, and the flat smile with its corners turned
    up, which is the whole of Squirtle's expression."""
    f = paint_box(tex, u, v, w, h, d, AQUA, top=AQUA_HI, bottom=AQUA_LO)
    for side in SIDES:
        x, y, fw, fh = f[side]
        rect(tex, x, y, fw, 1, AQUA_HI)
    x, y, fw, fh = f["front"]
    rect(tex, x, y + fh - 1, fw, 1, AQUA_LO2)
    put(tex, x, y + fh - 2, AQUA_LO2)
    put(tex, x + fw - 1, y + fh - 2, AQUA_LO2)
    x, y, fw, fh = f["top"]
    put(tex, x + 1, y + fh - 1, AQUA_LO2)
    put(tex, x + fw - 2, y + fh - 1, AQUA_LO2)
    return f


SQ_MATERIAL = (
    ("shell", carapace),
    ("body", plastron),
    ("head", visage),
    ("snout", muzzle),
    ("arm", limb),
    ("leg", limb),
    ("tail", hide),
)

for bone in squ["bones"]:
    paint = next(fn for pre, fn in SQ_MATERIAL if bone["name"].startswith(pre))
    for i, cube in enumerate(bone.get("cubes", [])):
        u, v = cube["uv"]
        w, h, d = (int(n) for n in cube["size"])
        paint(u, v, w, h, d, u + v + i)

write_png(os.path.join(ROOT,
          "pikachu_RP/textures/entity/squirtle/squirtle.png"),
          squ["description"]["texture_width"],
          squ["description"]["texture_height"], tex)

# ------------------------------------------------------------- water_gun.png
wg = canvas(16, 16)
jf = paint_box(wg, 0, 0, 3, 3, 3, JET, top=JET_HI, bottom=JET_LO)
for name in jf:
    x, y, w, h = jf[name]
    put(wg, x + w // 2, y + h // 2, JET_HI)
write_png(os.path.join(ROOT,
          "pikachu_RP/textures/entity/squirtle/water_gun.png"), 16, 16, wg)


# ------------------------------------------------------------- pack_icon.png
def pack_icon(path):
    ic = canvas(16, 16)
    rect(ic, 0, 0, 16, 16, (58, 52, 40, 255))
    for ex in (2, 11):                             # ears
        rect(ic, ex, 0, 3, 3, BLK)
        rect(ic, ex, 3, 3, 3, YEL)
    rect(ic, 2, 5, 12, 9, YEL)                     # head
    rect(ic, 3, 14, 10, 1, YEL)
    for cx, cy in ((2, 5), (13, 5), (2, 13), (13, 13)):
        ic[cy][cx] = (58, 52, 40, 255)
    rect(ic, 3, 4, 10, 1, YEL_HI)
    for ex in (4, 10):                             # eyes
        rect(ic, ex, 7, 2, 2, EYE)
        ic[7][ex + 1] = WHT
    rect(ic, 2, 10, 2, 2, RED)                     # cheeks
    rect(ic, 12, 10, 2, 2, RED)
    rect(ic, 7, 9, 2, 1, NOSE)
    ic[11][6] = MOUTH
    ic[11][9] = MOUTH
    ic[12][7] = MOUTH
    ic[12][8] = MOUTH
    big = canvas(128, 128)
    for y in range(128):
        for x in range(128):
            big[y][x] = ic[y // 8][x // 8]
    write_png(path, 128, 128, big)


pack_icon(os.path.join(ROOT, "pikachu_RP/pack_icon.png"))
pack_icon(os.path.join(ROOT, "pikachu_BP/pack_icon.png"))
print("textures written")

# ------------------------------------------------------------ poke_ball icons
# Every ball is the same 16x16 sprite with a different button, so the shell is
# written once as a pixel map and OCCUPANTS only carries the colour. Adding a
# mob to the ball system means a line here and a matching entry in
# item_texture.json.
BALL = """
....#######.....
...##xxxx=##....
..#x--xxxxx=#...
.#x-oo-xxxxx=#..
##x----xxxxxx##.
#xxxxxxxxxxxx=#.
#++++++##+++++#.
#+++++#@@#++++#.
#+++++#@@#++++#.
#*ooooo##ooooo#.
##ooooooooooo##.
.#*ooooooooo*#..
..#*ooooooo*#...
...##*****##....
....#######.....
................
""".strip("\n").splitlines()

BALL_INK = {
    "#": (35, 31, 32, A),        # outline
    "x": (239, 64, 54, A),       # the red half
    "-": (244, 122, 114, A),     # its highlight
    "=": (194, 56, 49, A),       # and its shaded rim
    "o": (255, 255, 255, A),     # the white half
    "*": (161, 158, 158, A),
    "+": (88, 88, 90, A),        # the band across the middle
    ".": (0, 0, 0, 0),
}

# The ball is also a mob, lying on the ground where a Pokemon was caught, so
# the same button colour has to land on the 32x32 sheet that wraps
# models/entity/poke_ball.geo.json. That net is five stacked cubes rather than
# anything drawable by rule, so it is a pixel map too.
BALL_MOB = """
........xxxxxxxxoooooooo........
........xxxxxxxxoooooooo........
........xxxxxxxxoooooooo........
........xxxxxxxxoooooooo........
........xxxxxxxxoooooooo........
........xxxxxxxxoooooooo........
........xxxxxxxxoooooooo........
........xxxxxxxxoooooooo........
xxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxx
=xxxxxx==xxxxxx==xxxxxx==xxxxxx=
+++++++++++@@+++++++++++++++++++
oooooooooooooooooooooooooooooooo
................................
......------xxxxxx..............
......------xxxxxx..............
......------xxxxxx..............
......------xxxxxx..............
......------xxxxxx..............
......------xxxxxx..............
xxxxxxxxxxxxxxxxxxxxxxxx........
......oooooo******..............
......oooooo******..............
......oooooo******..............
......oooooo******..............
......oooooo******..............
......oooooo******..............
oooooooooooooooooooooooo........
....----xxxx........oooo****....
....----xxxx........oooo****....
....----xxxx........oooo****....
....----xxxx........oooo****....
xxxxxxxxxxxxxxxxoooooooooooooooo
""".strip("\n").splitlines()

OCCUPANTS = {
    "": (232, 232, 234, A),      # empty, the button unlit
    "pikachu": YEL,
    "arboliva": LEAF,
    "kleavor": (208, 112, 58, A),
    "rayquaza": PULSE_HI,
    "squirtle": AQUA,
}


def stamp(rows, size, button):
    px = canvas(size, size)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            px[y][x] = button if ch == "@" else BALL_INK[ch]
    return px


for who, button in OCCUPANTS.items():
    name = "poke_ball_" + who if who else "poke_ball"
    write_png(os.path.join(ROOT, "pikachu_RP/textures/items", name + ".png"),
              16, 16, stamp(BALL, 16, button))
    write_png(os.path.join(ROOT, "pikachu_RP/textures/entity/poke_ball",
                           name + ".png"), 32, 32, stamp(BALL_MOB, 32, button))
