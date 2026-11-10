import math
import os
import struct
import zlib

ROOT = os.path.dirname(os.path.abspath(__file__))


def save_png(path, width, height, pixels):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    raw = b"".join(b"\x00" + bytes(channel for pixel in pixels[y * width:(y + 1) * width] for channel in pixel) for y in range(height))
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">2I5B", width, height, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    with open(path, "wb") as output:
        output.write(data)


W = H = 128
p = [(0, 0, 0, 0)] * (W * H)

def rect(x0, y0, x1, y1, color):
    for y in range(max(0, y0), min(H, y1)):
        for x in range(max(0, x0), min(W, x1)):
            p[y * W + x] = color

def noise_rect(x0, y0, x1, y1, base, shade, seed=0):
    rect(x0, y0, x1, y1, base)
    for y in range(y0, y1):
        for x in range(x0, x1):
            if ((x * 17 + y * 31 + seed) % 13) == 0:
                p[y * W + x] = shade

# Face and skin sections.
noise_rect(0, 0, 32, 32, (242, 190, 143, 255), (230, 164, 116, 255), 5)
rect(5, 8, 27, 10, (48, 38, 34, 255))
rect(7, 12, 11, 14, (37, 70, 105, 255))
rect(21, 12, 25, 14, (37, 70, 105, 255))
rect(8, 12, 10, 13, (245, 245, 235, 255))
rect(22, 12, 24, 13, (245, 245, 235, 255))
rect(9, 12, 10, 14, (72, 143, 179, 255))
rect(23, 12, 24, 14, (72, 143, 179, 255))
for y in (18, 21, 24):
    rect(5, y, 10, y + 1, (171, 112, 91, 255)); rect(22, y, 27, y + 1, (171, 112, 91, 255))
rect(13, 20, 19, 21, (166, 89, 79, 255))
rect(14, 23, 18, 24, (120, 54, 53, 255))
# Orange spiky hair and dark blond shadows.
noise_rect(0, 32, 32, 48, (238, 132, 32, 255), (255, 176, 54, 255), 9)
for x, top in [(1, 37), (5, 32), (10, 35), (15, 31), (20, 34), (25, 32), (30, 37)]:
    rect(x, top, min(32, x + 4), 40, (250, 159, 43, 255))
rect(0, 45, 32, 48, (205, 100, 26, 255))
# Headband plate and cloth.
rect(32, 0, 64, 16, (56, 63, 72, 255)); rect(36, 4, 60, 12, (172, 183, 191, 255))
rect(43, 6, 53, 10, (75, 83, 91, 255)); rect(45, 5, 47, 11, (58, 65, 72, 255))
rect(47, 5, 49, 11, (58, 65, 72, 255)); rect(48, 6, 52, 8, (58, 65, 72, 255))
# Jacket torso atlas, with blue shoulders and orange front.
noise_rect(32, 32, 64, 64, (236, 115, 30, 255), (255, 145, 39, 255), 11)
rect(32, 32, 64, 38, (30, 49, 92, 255)); rect(32, 58, 64, 64, (31, 48, 88, 255))
rect(46, 38, 49, 57, (242, 184, 79, 255)); rect(47, 39, 48, 56, (255, 222, 138, 255))
rect(35, 40, 40, 52, (224, 80, 31, 255)); rect(56, 40, 61, 52, (224, 80, 31, 255))
# Blue sleeves and orange cuff accents.
noise_rect(48, 64, 64, 96, (37, 56, 103, 255), (56, 78, 128, 255), 13)
rect(48, 90, 64, 96, (234, 112, 32, 255)); rect(64, 64, 80, 96, (37, 56, 103, 255))
rect(64, 90, 80, 96, (234, 112, 32, 255))
# Pants and sandals.
noise_rect(0, 64, 16, 96, (39, 54, 91, 255), (55, 71, 109, 255), 17)
noise_rect(16, 64, 32, 96, (39, 54, 91, 255), (55, 71, 109, 255), 19)
rect(0, 91, 16, 96, (198, 79, 28, 255)); rect(16, 91, 32, 96, (198, 79, 28, 255))
rect(0, 96, 16, 112, (57, 47, 43, 255)); rect(16, 96, 32, 112, (57, 47, 43, 255))
rect(2, 98, 14, 101, (112, 100, 84, 255)); rect(18, 98, 30, 101, (112, 100, 84, 255))
# Hands and neck.
noise_rect(32, 96, 48, 112, (242, 190, 143, 255), (230, 164, 116, 255), 21)
rect(48, 96, 64, 112, (242, 190, 143, 255)); rect(32, 112, 64, 128, (35, 54, 97, 255))
# Small atlas detail tiles and jacket back.
noise_rect(64, 32, 96, 64, (31, 49, 93, 255), (50, 70, 117, 255), 23)
rect(70, 39, 90, 59, (239, 119, 32, 255)); rect(74, 43, 86, 55, (247, 149, 46, 255))
rect(80, 45, 84, 53, (58, 61, 68, 255))
noise_rect(96, 0, 128, 32, (238, 132, 32, 255), (255, 176, 54, 255), 27)
rect(96, 0, 128, 6, (56, 63, 72, 255)); rect(96, 6, 128, 10, (172, 183, 191, 255))
# Remaining UV zones use cloth/skin details, avoiding transparent default faces.
for y in range(112, 128):
    for x in range(0, 128):
        if p[y * W + x][3] == 0:
            p[y * W + x] = (36, 52, 89, 255)
for y in range(0, 128):
    for x in range(80, 128):
        if p[y * W + x][3] == 0:
            p[y * W + x] = (239, 126, 33, 255) if (x + y) % 7 else (255, 174, 49, 255)
save_png(os.path.join(ROOT, "resource_pack/textures/entity/naruto.png"), W, H, p)

def icon(kind):
    size = 32
    pixels = [(0, 0, 0, 0)] * (size * size)
    def box(x0, y0, x1, y1, color):
        for y in range(y0, y1):
            for x in range(x0, x1): pixels[y * size + x] = color
    if kind == "naruto_headband":
        box(4, 12, 28, 20, (54, 62, 74, 255)); box(7, 13, 25, 18, (173, 185, 194, 255)); box(14, 14, 19, 17, (61, 68, 76, 255)); box(15, 13, 16, 18, (61, 68, 76, 255))
    elif kind == "rasengan":
        for y in range(size):
            for x in range(size):
                d = math.hypot(x - 16, y - 16)
                if d < 12: pixels[y * size + x] = (43, 139, 255, 255) if int(d * 2 + x + y) % 3 else (194, 236, 255, 255)
        box(14, 10, 18, 22, (244, 252, 255, 255))
    else:
        box(8, 4, 24, 28, (214, 182, 111, 255)); box(10, 6, 22, 26, (241, 222, 163, 255)); box(12, 10, 20, 22, (53, 67, 93, 255)); box(14, 12, 18, 20, (239, 133, 38, 255))
    save_png(os.path.join(ROOT, f"resource_pack/textures/items/{kind}.png"), size, size, pixels)

for item in ("naruto_headband", "rasengan", "shadow_clone_scroll"):
    icon(item)
print("Generated Naruto 128x128 texture and three item icons.")
