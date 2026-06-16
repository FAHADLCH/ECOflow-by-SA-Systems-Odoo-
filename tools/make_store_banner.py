"""Premium Odoo Apps Store banner for the single ECOFLOW app (SA Systems).

Charcoal + red brand, honeycomb motif, white SA Systems lockup, bold ECOFLOW
wordmark, AI badge, value tagline and outcome stat chips. No 'Base' wording.
Pure Pillow. 1200x600 @2x supersample.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WS = "/Users/fahad/Desktop/Odoo Apps/Waste Management System "
LOGO = os.path.join(WS, "ecoflow", "static", "src", "img", "sa_systems_logo.png")
OUT = os.path.join(WS, "ecoflow", "static", "description", "banner.png")

CHARCOAL = (18, 23, 24)
CHARCOAL2 = (30, 38, 41)
CHARCOAL3 = (10, 13, 14)
RED = (204, 0, 0)
RED_HI = (232, 72, 44)
WHITE = (255, 255, 255)
MUTE = (171, 181, 186)
FONT_DIR = "/System/Library/Fonts/Supplemental"

W, H, S = 1200, 600, 2


def font(size, weight="bold"):
    files = {"black": ["Arial Black.ttf", "Arial Bold.ttf"],
             "bold": ["Arial Bold.ttf", "Arial.ttf"],
             "reg": ["Arial.ttf", "Arial Bold.ttf"]}[weight]
    for name in files:
        p = os.path.join(FONT_DIR, name)
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


img = Image.new("RGB", (W * S, H * S), CHARCOAL)
d = ImageDraw.Draw(img)

# diagonal charcoal gradient
for y in range(H * S):
    t = y / (H * S)
    col = tuple(int(CHARCOAL2[i] + (CHARCOAL3[i] - CHARCOAL2[i]) * t) for i in range(3))
    d.line([(0, y), (W * S, y)], fill=col)

# subtle diagonal pinstripes
stripe = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
sd = ImageDraw.Draw(stripe)
gap = 26 * S
for k in range(-H, W + H, 26):
    x = k * S
    sd.line([(x, 0), (x + H * S, H * S)], fill=(255, 255, 255, 9), width=max(1, S))
img = Image.alpha_composite(img.convert("RGBA"), stripe).convert("RGB")
d = ImageDraw.Draw(img)

# red glow + honeycomb motif on the right
glow = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([int(W * S * 0.60), int(-H * S * 0.45), int(W * S * 1.30), int(H * S * 0.75)],
           fill=(204, 0, 0, 95))
gd.ellipse([int(W * S * 0.78), int(H * S * 0.45), int(W * S * 1.25), int(H * S * 1.25)],
           fill=(232, 72, 44, 70))
glow = glow.filter(ImageFilter.GaussianBlur(150))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
d = ImageDraw.Draw(img)


def hexagon(cx, cy, r, width, fill):
    pts = [(cx + r * math.cos(math.pi / 180 * (60 * i - 30)),
            cy + r * math.sin(math.pi / 180 * (60 * i - 30))) for i in range(6)]
    d.line(pts + [pts[0]], fill=fill, width=width, joint="curve")


# honeycomb cluster, right side
hr = 58 * S
hx, hy = int(W * S * 0.84), int(H * S * 0.46)
dx = hr * math.cos(math.radians(30)) * 2
dy = hr * 1.5
cells = [(0, 0), (1, 0), (-1, 0), (0.5, 1), (-0.5, 1), (0.5, -1), (-0.5, -1), (1, -1), (1.5, 0)]
for i, (cxn, cyn) in enumerate(cells):
    cx = hx + cxn * dx
    cy = hy + cyn * dy
    col = (235, 90, 60) if i % 3 == 0 else (120, 60, 60)
    hexagon(cx, cy, hr, max(2, 3 * S), col)

# white SA Systems lockup, top-left
logo = Image.open(LOGO).convert("RGBA")
lw = int(212 * S)
lh = int(logo.size[1] * lw / logo.size[0])
logo = logo.resize((lw, lh), Image.LANCZOS)
logo_x, logo_y = 80 * S, 52 * S
img.paste(logo, (logo_x, logo_y), logo)
d = ImageDraw.Draw(img)
logo_bottom = logo_y + lh

# eyebrow ribbon
eye_y = logo_bottom + 22 * S
d.text((82 * S, eye_y), "ENVIRONMENTAL OPERATIONS PLATFORM",
       font=font(19, "bold"), fill=MUTE)

# headline ECOFLOW + AI badge
hx0 = 78 * S
hy0 = eye_y + 34 * S
fhead = font(112, "black")
d.text((hx0, hy0), "ECOFLOW", font=fhead, fill=WHITE)
hbb = d.textbbox((hx0, hy0), "ECOFLOW", font=fhead)
hw = hbb[2]
head_h = hbb[3] - hy0
bx = hw + 26 * S
btop = hy0 + 16 * S
bbot = hy0 + head_h
d.rounded_rectangle([bx, btop, bx + 160 * S, bbot], radius=18 * S, fill=RED)
fai = font(66, "black")
aibb = d.textbbox((0, 0), "AI", font=fai)
d.text((bx + 80 * S - (aibb[2] - aibb[0]) / 2 - aibb[0],
        (btop + bbot) / 2 - (aibb[3] - aibb[1]) / 2 - aibb[1]),
       "AI", font=fai, fill=WHITE)

# tagline
tag_y = bbot + 30 * S
d.text((80 * S, tag_y), "AI-native intelligence for waste, recycling",
       font=font(33, "reg"), fill=(228, 231, 233))
d.text((80 * S, tag_y + 42 * S), "& the circular economy.",
       font=font(33, "reg"), fill=(228, 231, 233))

# outcome stat chips
chips = [("\u221222%", "wasted miles"), ("+15%", "recovery rate"),
         ("100%", "on-prem AI"), ("Odoo 18\u00b719", "native")]
cx = 80 * S
cy = H * S - 96 * S
for big, small in chips:
    fb = font(29, "black")
    fs = font(15, "reg")
    bw = d.textbbox((0, 0), big, font=fb)[2]
    sw = d.textbbox((0, 0), small, font=fs)[2]
    cw = max(bw, sw) + 38 * S
    d.rounded_rectangle([cx, cy, cx + cw, cy + 72 * S], radius=14 * S,
                        fill=(28, 35, 37), outline=(60, 70, 72), width=max(1, S))
    d.text((cx + 19 * S, cy + 12 * S), big, font=fb, fill=RED_HI)
    d.text((cx + 19 * S, cy + 47 * S), small, font=fs, fill=MUTE)
    cx += cw + 16 * S

img = img.resize((W, H), Image.LANCZOS)
img.save(OUT)
print("premium banner saved:", OUT)
