#!/usr/bin/env python3
"""Generates the Pikachu entity textures and pack icons.

Run from anywhere: python3 tools/gen_textures.py
Writes pikachu.png (64x64), thunder_shock.png (16x16) and both pack_icon.png.

UV slots here must stay in step with models/entity/pikachu.geo.json. Each cube
claims a Minecraft box-UV net: 2*depth + 2*width wide, depth + height tall.
"""
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
