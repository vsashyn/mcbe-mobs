#!/usr/bin/env python3
"""Generates every entity texture in the add-on, plus both pack icons.

Run from anywhere: python3 tools/gen_textures.py
Writes pikachu.png (64x64), arboliva.png (128x64), thunder_shock.png and
oil_salvo.png (16x16), moltres.png (256x128), and both pack_icon.png.

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


# Lapras is a plesiosaur in three materials: sky-blue hide with darker
# blotches, a cream throat and belly, and a grey shell of blunt knobs. The
# eyes are the only warm pixels anywhere on it.
LAP        = (108, 172, 214, A)
LAP_HI     = (150, 206, 236, A)
LAP_LO     = (80, 138, 182, A)
LAP_LO2    = (56, 106, 150, A)
LAP_SPOT   = (66, 124, 172, A)
LAP_CREAM  = (240, 232, 202, A)
LAP_CREAM_HI = (252, 248, 228, A)
LAP_CREAM_LO = (206, 194, 158, A)
LAP_EYE    = (118, 82, 48, A)
LAP_EYE_LO = (52, 34, 20, A)
CARA       = (190, 191, 196, A)
CARA_HI    = (221, 222, 226, A)
CARA_LO    = (158, 159, 166, A)
CARA_LO2   = (126, 127, 134, A)
CARA_EDGE  = (104, 105, 112, A)
KNOB       = (223, 224, 228, A)
KNOB_HI    = (243, 244, 247, A)
ICE        = (170, 226, 248, A)
ICE_HI     = (238, 252, 255, A)
ICE_LO     = (104, 172, 218, A)


# Plusle is two materials and no third: a pale cream body, and the red of its
# ears, hands, tail and cheek pouches. The plus inside each pouch is painted
# in the body cream rather than in a lighter red, because a near colour
# vanishes at mob scale and that plus is the one mark that tells it apart.
PL_CREAM     = (244, 236, 176, A)
PL_CREAM_HI  = (253, 249, 214, A)
PL_CREAM_LO  = (214, 203, 140, A)
PL_CREAM_LO2 = (180, 168, 110, A)
PL_BELLY     = (231, 218, 152, A)
PL_RED       = (188, 70, 72, A)
PL_RED_HI    = (216, 100, 98, A)
PL_RED_LO    = (150, 52, 56, A)
PL_RED_LO2   = (116, 40, 44, A)
PL_EYE       = (36, 30, 34, A)
PL_MOUTH     = (118, 48, 64, A)
PL_TONGUE    = (206, 112, 132, A)
PL_NOSE      = (198, 156, 88, A)
PL_SPARK     = (255, 228, 128, A)
PL_SPARK_HI  = (255, 252, 226, A)
PL_SPARK_LO  = (206, 96, 74, A)


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


# ----------------------------------------------------------------- lapras.png
# Painted off the model, the same way arboliva, kleavor and squirtle are.
#
# Lapras is three materials with a hard line between them: blue hide, a cream
# throat and belly, and the grey shell. The cream is what makes the neck read
# at distance, because a blue neck against a blue-grey shell against water is
# otherwise three shades of the same thing.
#
# Unlike the other three, the paint functions here are handed the bone name.
# An ear needs to know which of its side faces is the inner one, and that is
# not recoverable from a UV slot.
LA_GEO = os.path.join(ROOT, "pikachu_RP/models/entity/lapras.geo.json")
lap = next(g for g in json.load(open(LA_GEO))["minecraft:geometry"]
           if g["description"]["identifier"] == "geometry.lapras")
tex = canvas(lap["description"]["texture_width"],
             lap["description"]["texture_height"])


def dapple(f, seed, names=SIDES, n=3):
    """The darker blue blotches. Drawn as 2x2 blocks rather than single
    pixels, because one pixel of a near colour vanishes at mob scale."""
    rnd = random.Random(seed)
    for name in names:
        x, y, fw, fh = f[name]
        if fw < 5 or fh < 5:
            continue
        for _ in range(n):
            rect(tex, rnd.randrange(x + 1, x + fw - 2),
                 rnd.randrange(y + 1, y + fh - 2), 2, 2, LAP_SPOT)
    return f


def pelt(u, v, w, h, d, seed, name="", spots=True):
    """Blue hide: lit along the top rim of every side, shaded along the
    bottom, blotched in between."""
    f = paint_box(tex, u, v, w, h, d, LAP, top=LAP_HI, bottom=LAP_LO2)
    for side in SIDES:
        x, y, fw, fh = f[side]
        rect(tex, x, y, fw, 1, LAP_HI)
        rect(tex, x, y + fh - 1, fw, 1, LAP_LO)
    if spots:
        dapple(f, seed)
    return f


def hull(u, v, w, h, d, seed, name=""):
    """The torso. Everything above the waterline is buried under the shell, so
    the only part that has to be right is the cream keel underneath."""
    f = pelt(u, v, w, h, d, seed, spots=False)
    x, y, fw, fh = f["bottom"]
    rect(tex, x, y, fw, fh, LAP_CREAM)
    rect(tex, x, y, fw, 1, LAP_CREAM_LO)
    x, y, fw, fh = f["front"]                           # the chest, cream to
    rect(tex, x + 1, y + 1, fw - 2, fh - 1, LAP_CREAM)  # the shoulder
    rect(tex, x + 1, y + 1, fw - 2, 1, LAP_CREAM_LO)
    for side in ("right", "left"):                      # the keel turns up the
        x, y, fw, fh = f[side]                          # flanks before it stops
        rect(tex, x, y + fh - 3, fw, 3, LAP_CREAM)
        rect(tex, x, y + fh - 3, fw, 1, LAP_CREAM_LO)
    dapple(f, seed, names=("right", "left"), n=3)
    return f


def throat(u, v, w, h, d, seed, name=""):
    """A neck link. The cream runs up the front and the blue closes over the
    back, so the seam between them lands on the two side faces."""
    f = pelt(u, v, w, h, d, seed, spots=False)
    x, y, fw, fh = f["front"]
    rect(tex, x, y, fw, fh, LAP_CREAM)
    rect(tex, x, y, fw, 1, LAP_CREAM_HI)
    rect(tex, x, y, 1, fh, LAP_CREAM_LO)
    rect(tex, x + fw - 1, y, 1, fh, LAP_CREAM_LO)
    x, y, fw, fh = f["right"]                   # -x: the front is the last column
    rect(tex, x + fw - 1, y, 1, fh, LAP_CREAM_LO)
    x, y, fw, fh = f["left"]                    # +x: the front is the first
    rect(tex, x, y, 1, fh, LAP_CREAM_LO)
    dapple(f, seed, names=("right", "left", "back"), n=2)
    return f


def shellplate(u, v, w, h, d, seed, name=""):
    """One slab of the dome. Speckled two ways so the grey does not go flat,
    lipped pale along the top edge and dark along the bottom, which is what
    turns three stacked boxes into one rounded shell."""
    f = paint_box(tex, u, v, w, h, d, CARA, top=CARA_HI, bottom=CARA_LO2)
    for nm in f:
        x, y, fw, fh = f[nm]
        speckle(tex, x, y, fw, fh, CARA_LO, seed=seed + x, density=0.16)
        speckle(tex, x, y, fw, fh, CARA_HI, seed=seed + x + 91, density=0.10)
    for side in SIDES:
        x, y, fw, fh = f[side]
        rect(tex, x, y, fw, 1, CARA_HI)
        rect(tex, x, y + fh - 1, fw, 1, CARA_EDGE)
    return f


def knobcap(u, v, w, h, d, seed, name=""):
    """One blunt lump. Lighter than the slab it sits on and shaded underneath,
    which is the only relief the shell gets that is not a step."""
    f = paint_box(tex, u, v, w, h, d, KNOB, top=KNOB_HI, bottom=CARA_LO2)
    for side in SIDES:
        x, y, fw, fh = f[side]
        rect(tex, x, y, fw, 1, KNOB_HI)
        rect(tex, x, y + fh - 1, fw, 1, CARA_LO)
    return f


def fin(u, v, w, h, d, seed, name=""):
    """A flipper. Blue and blotched on top, cream along the trailing edge and
    underneath, which is the way it reads in the artwork and the only shading
    that survives a paddle four units thick."""
    f = pelt(u, v, w, h, d, seed, spots=False)
    x, y, fw, fh = f["bottom"]
    rect(tex, x, y, fw, fh, LAP_CREAM_LO)
    x, y, fw, fh = f["back"]                            # +z: the trailing edge
    rect(tex, x, y, fw, fh, LAP_CREAM)
    rect(tex, x, y, fw, 1, LAP_CREAM_HI)
    x, y, fw, fh = f["top"]
    rect(tex, x, y + fh - 1, fw, 1, LAP_CREAM_LO)
    dapple(f, seed, names=("top",), n=4)
    return f


def mien(u, v, w, h, d, seed, name=""):
    """The head: a lit brow, a hard lid stroke, two brown eyes and a cream jaw.

    The eyes are the whole face and they are three pixels wide each, pushed
    out to the corners so three clear pixels of hide bridge them. Everything
    about that is load-bearing. Brown on blue is close in value, so a narrower
    eye or a one-pixel bridge renders as a single dark bar across the head,
    and a bright row anywhere between the brow and the jaw reads as a second
    bar rather than as a cheek. Each eye carries white on its outer pixel and
    the pupil on its inner one, which is what turns two dark squares into a
    pair of eyes looking the same way."""
    f = pelt(u, v, w, h, d, seed, spots=False)
    x, y, fw, fh = f["front"]

    def p(c, r, col):
        put(tex, x + c, y + r, col)

    rect(tex, x, y, fw, 1, LAP_HI)                      # brow catches the light
    for c0, out in ((0, 0), (fw - 3, 2)):               # out: the outer column
        for c in range(c0, c0 + 3):
            p(c, 1, LAP_LO2)                            # the lid stroke
            p(c, 2, LAP_EYE)
            p(c, 3, LAP_EYE_LO)
        p(c0 + out, 2, WHT)                             # sclera, turned outward
        p(c0 + (2 - out), 2, LAP_EYE_LO)                # pupil, turned inward
        p(c0 + out, 3, LAP_EYE)
    for c in (0, fw - 1):                               # cheeks fall away
        p(c, 4, LAP_LO)
    rect(tex, x + 2, y + fh - 1, fw - 4, 1, LAP_CREAM)  # the jaw, one row only
    x, y, fw, fh = f["bottom"]
    rect(tex, x, y, fw, fh, LAP_CREAM_LO)
    dapple(f, seed, names=("right", "left"), n=2)
    return f


def muzzle(u, v, w, h, d, seed, name=""):
    """The snout: nostrils on top and the long flat smile, cream underneath so
    it carries on from the chin."""
    f = pelt(u, v, w, h, d, seed, spots=False)
    x, y, fw, fh = f["bottom"]
    rect(tex, x, y, fw, fh, LAP_CREAM)
    x, y, fw, fh = f["front"]
    rect(tex, x, y + fh - 1, fw, 1, LAP_CREAM)
    rect(tex, x + 1, y + fh - 2, fw - 2, 1, LAP_LO2)    # the mouth line
    x, y, fw, fh = f["top"]
    put(tex, x + 1, y + fh - 1, LAP_LO2)
    put(tex, x + fw - 2, y + fh - 1, LAP_LO2)
    for side in ("right", "left"):
        x, y, fw, fh = f[side]
        rect(tex, x, y + fh - 1, fw, 1, LAP_CREAM)
    return f


def spike(u, v, w, h, d, seed, name=""):
    """The forehead horn. Cream, so it reads against the blue skull."""
    return paint_box(tex, u, v, w, h, d, LAP_CREAM,
                     top=LAP_CREAM_HI, bottom=LAP_CREAM_LO)


def curl(u, v, w, h, d, seed, name=""):
    """One link of an ear. Blue outside, cream on the inner face, which is
    what makes the coil read as a coil and not a blue stub. The inner face of
    the left ear is its -x side and of the right ear its +x, and the net calls
    those 'right' and 'left' respectively."""
    f = pelt(u, v, w, h, d, seed, spots=False)
    x, y, fw, fh = f["right" if "left" in name else "left"]
    rect(tex, x, y, fw, fh, LAP_CREAM_LO)
    rect(tex, x, y, fw, 1, LAP_CREAM_HI)
    return f


LA_MATERIAL = (
    ("shell", shellplate),
    ("knobs", knobcap),
    ("body", hull),
    ("neck", throat),
    ("head", mien),
    ("snout", muzzle),
    ("horn", spike),
    ("ear", curl),
    ("flipper", fin),
    ("tail", pelt),
)

for bone in lap["bones"]:
    paint = next(fn for pre, fn in LA_MATERIAL if bone["name"].startswith(pre))
    for i, cube in enumerate(bone.get("cubes", [])):
        u, v = cube["uv"]
        w, h, d = (int(n) for n in cube["size"])
        paint(u, v, w, h, d, u + v + i, bone["name"])

write_png(os.path.join(ROOT, "pikachu_RP/textures/entity/lapras/lapras.png"),
          lap["description"]["texture_width"],
          lap["description"]["texture_height"], tex)

# -------------------------------------------------------------- ice_beam.png
# The shard is long rather than round, so unlike the other three projectiles
# its sheet is 32x16 and its net is not square.
ib = canvas(32, 16)
sf = paint_box(ib, 0, 0, 3, 3, 7, ICE, top=ICE_HI, bottom=ICE_LO)
for name in sf:
    x, y, w, h = sf[name]
    rect(ib, x, y, w, 1, ICE_HI)
    rect(ib, x, y + h - 1, w, 1, ICE_LO)
for name in ("right", "left"):                      # a bright core down the shard
    x, y, w, h = sf[name]
    rect(ib, x + 1, y + h // 2, w - 2, 1, ICE_HI)
write_png(os.path.join(ROOT,
          "pikachu_RP/textures/entity/lapras/ice_beam.png"), 32, 16, ib)


# ---------------------------------------------------------------- moltres.png
# Galarian Moltres is two materials and nothing else: a body that is almost
# black with scarlet cutting through it, and a flame that is black at the root
# and magenta at the tip. Slots are read back out of the geometry that owns
# them, the same way Rayquaza's are, because 44 cubes is more UV than a
# hand-written table stays honest about.
M_INK      = (26, 24, 30, A)
M_INK_HI   = (54, 50, 62, A)
M_INK_LO   = (15, 14, 18, A)
M_CRIM     = (206, 32, 74, A)
M_CRIM_HI  = (238, 70, 112, A)
M_CRIM_LO  = (148, 18, 52, A)
M_PINK     = (226, 74, 142, A)
M_PINK_HI  = (250, 162, 202, A)
M_PINK_LO  = (172, 34, 98, A)
M_EYE      = (96, 216, 246, A)
M_EYE_LO   = (34, 130, 178, A)
M_TALON    = (18, 17, 22, A)

MOL_GEO = json.load(open(os.path.join(
    ROOT, "pikachu_RP/models/entity/moltres.geo.json")))
MOL_BONES = {
    b["name"]: [(c["uv"][0], c["uv"][1], *(int(n) for n in c["size"]))
                for c in b.get("cubes", [])]
    for g in MOL_GEO["minecraft:geometry"]
    if g["description"]["identifier"] == "geometry.moltres"
    for b in g["bones"]
}

tex = canvas(256, 128)


def mol_mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3)) + (A,)


def mol_ink(bone, i=0, base=M_INK, top=M_INK_HI, bottom=M_INK_LO):
    """One cube of the body, in the near-black the whole bird is under."""
    u, v, w, h, d = MOL_BONES[bone][i]
    return paint_box(tex, u, v, w, h, d, base, top=top, bottom=bottom)


def mol_red(bone, i=0, base=M_CRIM, top=M_CRIM_HI, bottom=M_CRIM_LO):
    u, v, w, h, d = MOL_BONES[bone][i]
    return paint_box(tex, u, v, w, h, d, base, top=top, bottom=bottom)


def mol_flame(bone, i=0, seed=0):
    """A flame: magenta at the tip, charcoal at the root, ragged between.

    The dark climbs each column of the face on a random walk rather than a
    straight line, so the boundary comes out as tongues instead of a horizon.
    Row 0 of an upright face is the top of the cube, which is the end of the
    flame furthest from the bird, so the ramp runs hot to cold down the rows.
    """
    u, v, w, h, d = MOL_BONES[bone][i]
    f = paint_box(tex, u, v, w, h, d, M_PINK, top=M_PINK_HI, bottom=M_INK)
    rnd = random.Random(seed)
    for name in ("front", "back", "left", "right"):
        x, y, fw, fh = f[name]
        for r in range(fh):
            rect(tex, x, y + r, fw, 1,
                 mol_mix(M_PINK_HI, M_PINK_LO, r / max(fh - 1, 1)))
        lvl = fh // 2
        for c in range(fw):
            lvl = max(1, min(fh - 1, lvl + rnd.choice((-2, -1, 0, 1, 2))))
            put(tex, x + c, y + lvl - 1, M_PINK_HI)     # the lit edge of the
            for r in range(lvl, fh):                    # dark, then the dark
                put(tex, x + c, y + r, M_INK if r > lvl else M_INK_HI)
    return f


def mol_edge(f, faces, col):
    """Runs a line along the top of a face, which is the crimson piping the
    artwork puts down every seam where black meets black."""
    for name in faces:
        x, y, fw, fh = f[name]
        rect(tex, x, y, fw, 1, col)


# body. The chest carries a crimson keel down the middle of its underside and
# the same piping along both flanks, which is all the colour the trunk has.
chest = mol_ink("body", 0)
for side in ("left", "right"):
    x, y, fw, fh = chest[side]
    rect(tex, x, y + fh - 2, fw, 1, M_CRIM_LO)
x, y, fw, fh = chest["bottom"]
rect(tex, x + (fw - 2) // 2, y, 2, fh, M_CRIM_LO)
rump = mol_ink("body", 1)
mol_edge(rump, ("left", "right"), M_INK_HI)

for name, *_ in (("neck1",), ("neck2",), ("neck3",)):
    nf = mol_ink(name)
    for side in ("left", "right"):
        x, y, fw, fh = nf[side]
        rect(tex, x, y + fh - 1, fw, 1, M_CRIM_LO)      # the throat line

# head. The cap is crimson, the beak is crimson with a dark ridge, and the eye
# is the one bright thing on the whole model.
skull = mol_ink("head", 0)
x, y, fw, fh = skull["front"]
rect(tex, x, y, fw, 2, M_CRIM)                          # brow band
mol_red("head", 1, base=M_CRIM_HI)

bk = mol_red("beak", 0)
for name in ("top", "left", "right"):
    x, y, fw, fh = bk[name]
    rect(tex, x, y, fw if name == "top" else 1, fh, M_CRIM_LO)
x, y, fw, fh = bk["bottom"]
rect(tex, x, y, fw, fh, M_INK_LO)                       # inside the mouth
mol_red("beak", 1, base=M_CRIM_LO, top=M_CRIM, bottom=M_INK_LO)   # the hook

jw = mol_red("jaw", base=M_CRIM_LO, top=M_INK_LO)
mol_edge(jw, ("left", "right"), M_CRIM)

for side in ("left", "right"):
    ef = mol_ink(f"eye_{side}", base=M_INK_LO, top=M_INK_LO, bottom=M_INK_LO)
    x, y, fw, fh = ef[side]
    rect(tex, x, y, fw, fh, M_EYE)
    rect(tex, x, y + fh - 1, fw, 1, M_EYE_LO)
    put(tex, x + fw - 1, y, WHT)                        # catchlight

# every flame on the bird, seeded off its own name so no two burn alike
for n, bname in enumerate(sorted(MOL_BONES)):
    if bname.startswith(("crest", "plume_", "flame_", "tailflame_")):
        mol_flame(bname, seed=1700 + n)

# wings and tail are black struts, lit along the leading edge
for seg in ("wing", "wingmid", "wingtip"):
    for side in ("left", "right"):
        wf = mol_ink(f"{seg}_{side}")
        mol_edge(wf, ("front",), M_CRIM_LO)
        x, y, fw, fh = wf["top"]
        rect(tex, x, y, fw, 1, M_INK_HI)
for name in ("tail1", "tail2"):
    tf2 = mol_ink(name)
    for side in ("left", "right"):
        x, y, fw, fh = tf2[side]
        rect(tex, x, y, fw, 1, M_CRIM_LO)

# legs. Scarlet down to the toes, then black talons.
for side in ("left", "right"):
    mol_red(f"thigh_{side}")
    mol_red(f"shin_{side}", base=M_CRIM, top=M_CRIM_HI, bottom=M_CRIM_LO)
    ff = mol_red(f"foot_{side}", 0, base=M_CRIM_LO, top=M_CRIM)
    mol_edge(ff, ("front",), M_TALON)
    for i in (1, 2):
        mol_ink(f"foot_{side}", i, base=M_TALON, top=M_INK_HI, bottom=M_TALON)

write_png(os.path.join(ROOT,
          "pikachu_RP/textures/entity/moltres/moltres.png"), 256, 128, tex)

# ------------------------------------------------------------ fiery_wrath.png
# The aura it throws: a magenta shell with a black heart, because the move is
# a Dark-type one wearing fire.
fw_tex = canvas(16, 16)
wf = paint_box(fw_tex, 0, 0, 4, 4, 4, M_PINK, top=M_PINK_HI, bottom=M_PINK_LO)
for name in wf:
    x, y, w, h = wf[name]
    rect(fw_tex, x + 1, y + 1, w - 2, h - 2, M_INK)
    put(fw_tex, x + w // 2, y + h // 2, M_PINK_HI)
write_png(os.path.join(ROOT,
          "pikachu_RP/textures/entity/moltres/fiery_wrath.png"), 16, 16, fw_tex)

# ----------------------------------------------------------------- plusle.png
# Painted off the model, the same way arboliva, kleavor, squirtle and lapras
# are, so the slots cannot drift out of step with models/entity/plusle.geo.json.
#
# Almost every cube on Plusle is one flat cream, which is a problem: a mob
# painted in one colour reads as a lump. What separates the parts is a lit row
# along the top of every side face and a shaded row along the bottom, so each
# box carries its own top and bottom edge and the joints show up as seams.
#
# The paint functions take the bone name because the ears need it. An ear's
# inner face is its -x side on the left of the mob and its +x side on the
# right, and the box-UV net calls those "right" and "left" respectively, so
# which one to darken is not recoverable from the UV slot alone.
PL_GEO = os.path.join(ROOT, "pikachu_RP/models/entity/plusle.geo.json")
plu = next(g for g in json.load(open(PL_GEO))["minecraft:geometry"]
           if g["description"]["identifier"] == "geometry.plusle")
tex = canvas(plu["description"]["texture_width"],
             plu["description"]["texture_height"])


def hide(u, v, w, h, d, seed, name=""):
    """Cream body: lit along the top rim of every side, shaded along the
    bottom. This is the base every other Plusle painter starts from."""
    f = paint_box(tex, u, v, w, h, d, PL_CREAM,
                  top=PL_CREAM_HI, bottom=PL_CREAM_LO2)
    for side in SIDES:
        x, y, fw, fh = f[side]
        rect(tex, x, y, fw, 1, PL_CREAM_HI)
        rect(tex, x, y + fh - 1, fw, 1, PL_CREAM_LO)
    return f


def torso(u, v, w, h, d, seed, name=""):
    """The body, with the darker cream belly on the front. The belly stops one
    pixel short of every edge so the lit and shaded rims survive it, which is
    what keeps the torso from flattening into a single field of cream."""
    f = hide(u, v, w, h, d, seed)
    x, y, fw, fh = f["front"]
    rect(tex, x + 1, y + 2, fw - 2, fh - 3, PL_BELLY)
    rect(tex, x + 1, y + 2, fw - 2, 1, PL_CREAM_LO)
    return f


def mien(u, v, w, h, d, seed, name=""):
    """The face: two tall eyes, a nose, an open mouth and a plus in each cheek.

    Nine columns across eight rows, and the cheeks decide the layout. Plusle's
    pouch is a red disc with a pale plus inside it, and three pixels square is
    not enough for both: a cream cross through a 3x3 red block leaves four
    single red pixels at the corners, which at mob scale is not a pouch, it is
    four specks of noise. So the mark here is the plus itself, drawn in red on
    the bare cream cheek. Five pixels, unmistakable, and it survives being seen
    from ten blocks away.

    The other rule is that the bar of each plus and the mouth may not share a
    row. They did in the first cut, and nine columns of red-dark-red across the
    middle of the face read as one bar rather than as two cheeks and a smile.
    The bars sit one row above the mouth, which is what leaves a clear cream
    row between them."""
    f = hide(u, v, w, h, d, seed)
    x, y, fw, fh = f["front"]
    mid = fw // 2

    def p(c, r, col):
        put(tex, x + c, y + r, col)

    rect(tex, x, y, fw, 1, PL_CREAM_HI)                 # brow catches the light
    for c0 in (1, fw - 3):                              # eyes, three rows tall
        for c in range(c0, c0 + 2):
            for r in (1, 2, 3):
                p(c, r, PL_EYE)
        p(c0, 1, WHT)                                   # both glints one way,
    p(mid, fh - 4, PL_NOSE)                             # as one light source
    rect(tex, x + mid - 1, y + fh - 2, 3, 1, PL_MOUTH)  # the open smile
    p(mid, fh - 1, PL_TONGUE)
    for c0 in (0, fw - 3):                              # a plus in each cheek
        rect(tex, x + c0, y + fh - 3, 3, 1, PL_RED)
        p(c0 + 1, fh - 4, PL_RED)
        p(c0 + 1, fh - 2, PL_RED)
        p(c0 + 1, fh - 3, PL_RED_HI)                    # lit at the crossing
    x, y, fw, fh = f["bottom"]                          # under the jaw
    rect(tex, x, y, fw, fh, PL_CREAM_LO)
    return f


def mitt(u, v, w, h, d, seed, name=""):
    """An arm. Cream to the elbow, red from there down, because the hands are
    the only red Plusle carries below the head and losing them costs the whole
    front view its colour."""
    f = hide(u, v, w, h, d, seed)
    for side in SIDES:
        x, y, fw, fh = f[side]
        rect(tex, x, y + fh - 2, fw, 2, PL_RED)
        rect(tex, x, y + fh - 2, fw, 1, PL_RED_HI)
    x, y, fw, fh = f["bottom"]
    rect(tex, x, y, fw, fh, PL_RED_LO)
    return f


def paw(u, v, w, h, d, seed, name=""):
    """A foot. Cream with a dark sole, so a Plusle standing on grass has a
    line under it rather than melting into the block."""
    f = hide(u, v, w, h, d, seed)
    x, y, fw, fh = f["bottom"]
    rect(tex, x, y, fw, fh, PL_CREAM_LO2)
    return f


def blade(u, v, w, h, d, seed, name=""):
    """One link of an ear. Red outside, a shade darker on the inner face so
    the pair reads as two blades turned toward each other rather than as two
    flat cutouts. The tip link is lightened along its top rim instead, which
    is the only thing keeping a fourteen-degree bend visible at distance."""
    f = paint_box(tex, u, v, w, h, d, PL_RED, top=PL_RED_HI, bottom=PL_RED_LO2)
    for side in SIDES:
        x, y, fw, fh = f[side]
        rect(tex, x, y, fw, 1, PL_RED_HI)
        rect(tex, x, y + fh - 1, fw, 1, PL_RED_LO)
    x, y, fw, fh = f["right" if "left" in name else "left"]
    rect(tex, x, y, fw, fh, PL_RED_LO)
    rect(tex, x, y, fw, 1, PL_RED)
    return f


def cross(u, v, w, h, d, seed, name=""):
    """One bar of the tail. Lit down the middle of every long face rather than
    along an edge: the plus is seen end-on as often as flat, and a bar shaded
    only at its rim goes solid the moment it turns."""
    f = paint_box(tex, u, v, w, h, d, PL_RED, top=PL_RED_HI, bottom=PL_RED_LO2)
    for side in SIDES:
        x, y, fw, fh = f[side]
        rect(tex, x, y, fw, 1, PL_RED_LO)
        rect(tex, x, y + fh - 1, fw, 1, PL_RED_LO2)
        if fw > 2:
            rect(tex, x + 1, y + fh // 2, fw - 2, 1, PL_RED_HI)
    return f


PL_MATERIAL = (
    ("head", mien),
    ("body", torso),
    ("arm", mitt),
    ("leg", paw),
    ("ear_base", hide),
    ("ear", blade),
    ("tail", cross),
)

for bone in plu["bones"]:
    paint = next(fn for pre, fn in PL_MATERIAL if bone["name"].startswith(pre))
    for i, cube in enumerate(bone.get("cubes", [])):
        u, v = cube["uv"]
        w, h, d = (int(n) for n in cube["size"])
        paint(u, v, w, h, d, u + v + i, bone["name"])

write_png(os.path.join(ROOT, "pikachu_RP/textures/entity/plusle/plusle.png"),
          plu["description"]["texture_width"],
          plu["description"]["texture_height"], tex)

# ----------------------------------------------------------------- spark.png
# Two bars on one 32x16 sheet, laid out to match geometry.spark. Bright core,
# red only on the four end caps, because these bars are two and three units
# thick and an edge line on a two-pixel face is the whole face: the first cut
# rimmed every side and the spark came out a rusty cross instead of a spark.
sk = canvas(32, 16)
for u, w, hh, dd, caps in ((0, 2, 6, 2, ("top", "bottom")),
                           (8, 6, 2, 3, ("right", "left"))):
    bf = paint_box(sk, u, 0, w, hh, dd, PL_SPARK,
                   top=PL_SPARK_HI, bottom=PL_SPARK_HI)
    for name in caps:                       # red tips with a hot centre, so
        x, y, fw, fh = bf[name]             # the arms end rather than stop
        rect(sk, x, y, fw, fh, PL_SPARK_LO)
        rect(sk, x + fw // 2 - (fw + 1) % 2, y, 2 - fw % 2, fh, PL_SPARK)
    for name in SIDES:
        x, y, fw, fh = bf[name]
        if fh >= 3:
            rect(sk, x, y, fw, 1, PL_SPARK_HI)
            rect(sk, x, y + fh - 1, fw, 1, PL_SPARK_LO)
        elif fw >= 3:
            rect(sk, x, y, 1, fh, PL_SPARK_LO)
            rect(sk, x + fw - 1, y, 1, fh, PL_SPARK_LO)
write_png(os.path.join(ROOT, "pikachu_RP/textures/entity/plusle/spark.png"),
          32, 16, sk)


# ------------------------------------------------------------------ minun.png
# Read off the model, the same way arboliva, kleavor, squirtle and lapras are.
#
# Minun is two colours and nothing else: a cream body and the blue that marks
# it out as the minus half of the pair. The blue only ever lands on four
# things, the ears, the cheek discs, the paws and the tail bar, so every one
# of them has to carry its share of the read. The cheek disc is the only place
# the minus sign itself is drawn, one cream row cut across three blue ones.
MIN_CREAM     = (243, 235, 184, A)
MIN_CREAM_HI  = (251, 245, 211, A)
MIN_CREAM_LO  = (222, 212, 156, A)
MIN_CREAM_LO2 = (196, 185, 130, A)
MIN_BELLY     = (250, 244, 208, A)
MIN_SKY       = (133, 186, 224, A)
MIN_SKY_HI    = (176, 213, 238, A)
MIN_SKY_LO    = (108, 160, 202, A)
MIN_SKY_LO2   = (86, 133, 178, A)
MIN_EYE       = (32, 40, 66, A)
MIN_EYE_HI    = (62, 78, 118, A)
MIN_NOSE      = (198, 184, 136, A)
MIN_MOUTH     = (166, 148, 104, A)
MIN_BOLT      = (198, 232, 255, A)
MIN_BOLT_HI   = (255, 255, 255, A)
MIN_BOLT_LO   = (96, 168, 226, A)

MI_GEO = os.path.join(ROOT, "pikachu_RP/models/entity/minun.geo.json")
mun = next(g for g in json.load(open(MI_GEO))["minecraft:geometry"]
           if g["description"]["identifier"] == "geometry.minun")
tex = canvas(mun["description"]["texture_width"],
             mun["description"]["texture_height"])


def fur(u, v, w, h, d, i):
    """Cream hide: lit along the top rim of every side, shaded along the
    bottom, which is all the modelling a two-colour mob can take before the
    shading starts competing with the markings."""
    f = paint_box(tex, u, v, w, h, d, MIN_CREAM,
                  top=MIN_CREAM_HI, bottom=MIN_CREAM_LO2)
    for side in SIDES:
        x, y, fw, fh = f[side]
        rect(tex, x, y, fw, 1, MIN_CREAM_HI)
        rect(tex, x, y + fh - 1, fw, 1, MIN_CREAM_LO)
    return f


def torso(u, v, w, h, d, i):
    """The body, with the paler belly patch the artwork puts on the front."""
    f = fur(u, v, w, h, d, i)
    x, y, fw, fh = f["front"]
    rect(tex, x + 1, y + 2, fw - 2, fh - 2, MIN_BELLY)
    return f


def visage(u, v, w, h, d, i):
    """The face. Two round black eyes set wide, a dot of a nose and a mouth
    two texels across, all of it above the cheek discs, which are their own
    cubes and would cover anything painted lower."""
    f = fur(u, v, w, h, d, i)
    x, y, fw, fh = f["front"]

    def px(c, r, col):
        put(tex, x + c, y + r, col)

    for c in range(fw):
        px(c, 0, MIN_CREAM_HI)                     # brow catches the light
    for c0, glint in ((1, 1), (5, 6)):             # eyes, glints turned out
        for c in (c0, c0 + 1):
            for r in (1, 2):
                px(c, r, MIN_EYE)
        px(glint, 1, MIN_BOLT_HI)
    px(3, 3, MIN_NOSE)                             # a nose two texels wide
    px(4, 3, MIN_NOSE)
    px(3, 4, MIN_MOUTH)                            # and a mouth two across
    px(4, 4, MIN_MOUTH)
    rect(tex, x, y + fh - 1, fw, 1, MIN_CREAM_LO)  # jaw
    return f


def cheek(u, v, w, h, d, i):
    """The minus itself: a blue disc with one cream row cut across it. Three
    texels is the smallest square that can hold a bar and still show blue
    above and below it, which is why the cube is 3x3 and not 2x2."""
    f = paint_box(tex, u, v, w, h, d, MIN_SKY,
                  top=MIN_SKY_HI, bottom=MIN_SKY_LO2)
    for name in f:
        x, y, fw, fh = f[name]
        rect(tex, x, y, fw, 1, MIN_SKY_HI)
        rect(tex, x, y + fh - 1, fw, 1, MIN_SKY_LO)
    x, y, fw, fh = f["front"]
    rect(tex, x, y, fw, fh, MIN_SKY)
    rect(tex, x, y + fh // 2, fw, 1, MIN_CREAM)    # the sign
    return f


def blade(u, v, w, h, d, i, name=""):
    """An ear link. Blue with a lit leading edge and a darker rim down both
    sides, so a paddle four texels wide does not read as a flat sticker. The
    top link loses its two upper corners to the rim colour, which is the only
    way to round off an ear tip that is three texels across."""
    f = paint_box(tex, u, v, w, h, d, MIN_SKY,
                  top=MIN_SKY_HI, bottom=MIN_SKY_LO)
    for face in ("front", "back"):
        x, y, fw, fh = f[face]
        rect(tex, x, y, 1, fh, MIN_SKY_LO)
        rect(tex, x + fw - 1, y, 1, fh, MIN_SKY_LO)
        rect(tex, x + 1, y, fw - 2, 1, MIN_SKY_HI)
        if name.endswith("_tip"):
            put(tex, x, y, MIN_SKY_LO2)
            put(tex, x + fw - 1, y, MIN_SKY_LO2)
    for side in ("right", "left"):
        x, y, fw, fh = f[side]
        rect(tex, x, y, fw, fh, MIN_SKY_LO)        # the ear seen edge on
    return f


def foreleg(u, v, w, h, d, i):
    """Arm, then paw. The bone carries both cubes so the blue mitten needs no
    joint of its own; cube 0 is the cream arm and cube 1 is the paw."""
    if i == 0:
        return fur(u, v, w, h, d, i)
    f = paint_box(tex, u, v, w, h, d, MIN_SKY,
                  top=MIN_SKY_HI, bottom=MIN_SKY_LO2)
    for side in SIDES:
        x, y, fw, fh = f[side]
        rect(tex, x, y, fw, 1, MIN_SKY_HI)
        rect(tex, x, y + fh - 1, fw, 1, MIN_SKY_LO2)
    return f


def foot(u, v, w, h, d, i):
    """A leg with a sole dark enough to read as a foot rather than more leg."""
    f = fur(u, v, w, h, d, i)
    x, y, fw, fh = f["bottom"]
    rect(tex, x, y, fw, fh, MIN_CREAM_LO2)
    return f


def minus_bar(u, v, w, h, d, i):
    """The tail bar. Solid blue with a pale core row, because at two texels
    tall the bar needs an inside and an outside to read as a sign rather than
    a stick."""
    f = paint_box(tex, u, v, w, h, d, MIN_SKY,
                  top=MIN_SKY_HI, bottom=MIN_SKY_LO2)
    for name in ("front", "back", "top"):
        x, y, fw, fh = f[name]
        rect(tex, x, y, fw, 1, MIN_SKY_HI)
    for side in ("right", "left"):
        x, y, fw, fh = f[side]
        rect(tex, x, y, fw, fh, MIN_SKY_LO)
    return f


MI_MATERIAL = (
    ("tail_bar", minus_bar),
    ("tail", fur),
    ("cheek", cheek),
    ("ear_root", fur),
    ("ear", blade),
    ("arm", foreleg),
    ("leg", foot),
    ("head", visage),
    ("body", torso),
)

for bone in mun["bones"]:
    paint = next(fn for pre, fn in MI_MATERIAL if bone["name"].startswith(pre))
    for i, cube in enumerate(bone.get("cubes", [])):
        u, v = cube["uv"]
        w, h, d = (int(n) for n in cube["size"])
        if paint is blade:
            paint(u, v, w, h, d, i, bone["name"])
        else:
            paint(u, v, w, h, d, i)

write_png(os.path.join(ROOT, "pikachu_RP/textures/entity/minun/minun.png"),
          mun["description"]["texture_width"],
          mun["description"]["texture_height"], tex)

# ------------------------------------------------------------ minus_spark.png
# Minun's bolt is white at the core and blue at the rim, the other way round
# from Pikachu's, which is all it takes to tell two electric moves apart in
# flight. It is minus_spark and not spark because Plusle throws a spark too,
# and two entities cannot share an identifier.
sp = canvas(16, 16)
bf = paint_box(sp, 0, 0, 3, 3, 3, MIN_BOLT, top=MIN_BOLT_HI, bottom=MIN_BOLT_LO)
for name in bf:
    x, y, w, h = bf[name]
    rect(sp, x, y, w, 1, MIN_BOLT_LO)
    put(sp, x + w // 2, y + h // 2, MIN_BOLT_HI)
write_png(os.path.join(ROOT, "pikachu_RP/textures/entity/minun/minus_spark.png"),
          16, 16, sp)


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
    "moltres": M_PINK,
    "lapras": LAP,
    "minun": MIN_SKY,
    "plusle": PL_RED,
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
