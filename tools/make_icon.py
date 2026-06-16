"""Generate a clean, branded ECOFLOW app icon in the Sa Systems identity.

Design: charcoal rounded square, brand-red rounded tile with white "sa"
wordmark (authentic Sa Systems treatment), and a subtle recycling arc to
signal waste/recycling. Crisp at 512 and 140 px.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

WS = "/Users/fahad/Desktop/Odoo Apps/Waste Management System "
DASH_IMG = os.path.join(WS, "addons", "ecoflow_dashboard", "static", "src", "img")
DASH_DESC = os.path.join(WS, "addons", "ecoflow_dashboard", "static", "description")
PROD = os.path.join(WS, "product", "assets")

CHARCOAL = (22, 27, 28)
CHARCOAL_2 = (32, 39, 41)
RED = (204, 0, 0)
RED_HI = (228, 30, 26)
WHITE = (255, 255, 255)

S = 1024  # supersample
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)


def font(size, bold=True):
    for c in [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()


# charcoal background, vertical subtle gradient
bg = Image.new("RGB", (S, S), CHARCOAL)
bd = ImageDraw.Draw(bg)
for y in range(S):
    t = y / S
    col = tuple(int(CHARCOAL_2[i] + (CHARCOAL[i] - CHARCOAL_2[i]) * t) for i in range(3))
    bd.line([(0, y), (S, y)], fill=col)
mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, S, S], radius=int(S * 0.22), fill=255)
img.paste(bg, (0, 0), mask)
d = ImageDraw.Draw(img)

# subtle recycling arcs (eco motif) in dim red, behind the tile
cx, cy = S * 0.5, S * 0.5
for k in range(3):
    ang0 = 90 + k * 120
    bbox = [S * 0.16, S * 0.16, S * 0.84, S * 0.84]
    d.arc(bbox, ang0 + 12, ang0 + 96, fill=(120, 30, 30), width=int(S * 0.022))

# brand-red rounded tile (the 'sa' block)
tw, th = int(S * 0.60), int(S * 0.40)
tx, ty = (S - tw) // 2, int(S * 0.30)
tile = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
td = ImageDraw.Draw(tile)
# red gradient
for y in range(th):
    t = y / th
    col = tuple(int(RED_HI[i] + (RED[i] - RED_HI[i]) * t) for i in range(3))
    td.line([(0, y), (tw, y)], fill=col)
tmask = Image.new("L", (tw, th), 0)
ImageDraw.Draw(tmask).rounded_rectangle([0, 0, tw, th], radius=int(th * 0.18), fill=255)
img.paste(tile, (tx, ty), tmask)
d = ImageDraw.Draw(img)

# white "sa" wordmark centered in tile
f = font(int(th * 0.74))
tb = d.textbbox((0, 0), "sa", font=f)
twd, thd = tb[2] - tb[0], tb[3] - tb[1]
d.text((tx + tw / 2 - twd / 2 - tb[0], ty + th / 2 - thd / 2 - tb[1]), "sa", font=f, fill=WHITE)

# small "ECOFLOW" label under tile
f2 = font(int(S * 0.072))
lab = "ECOFLOW"
lb = d.textbbox((0, 0), lab, font=f2)
lwd = lb[2] - lb[0]
d.text((S / 2 - lwd / 2 - lb[0], int(S * 0.74)), lab, font=f2, fill=(235, 235, 235))

# downscale
out = img.resize((512, 512), Image.LANCZOS)
out.save(os.path.join(DASH_DESC, "icon.png"))
out.resize((140, 140), Image.LANCZOS).save(os.path.join(DASH_IMG, "icon.png"))
out.resize((256, 256), Image.LANCZOS).save(os.path.join(PROD, "icon.png"))
print("icon written 512/140/256")
