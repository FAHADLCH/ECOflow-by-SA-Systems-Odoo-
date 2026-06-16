"""Generate the Odoo App Store banner for ecoflow_ai (and a shared one).

Sa Systems brand: charcoal background, red accent, 'sa' tile, product name and
the AI value proposition. 1200x600 is a safe App Store banner size.
"""
import os
from PIL import Image, ImageDraw, ImageFont

WS = "/Users/fahad/Desktop/Odoo Apps/Waste Management System "
TARGETS = [
    os.path.join(WS, "addons", "ecoflow_ai", "static", "description", "banner.png"),
    os.path.join(WS, "addons", "ecoflow_dashboard", "static", "description", "banner.png"),
    os.path.join(WS, "product", "assets", "banner.png"),
]
for t in TARGETS:
    os.makedirs(os.path.dirname(t), exist_ok=True)

CHARCOAL = (22, 27, 28)
CHARCOAL2 = (30, 38, 41)
RED = (204, 0, 0)
WHITE = (255, 255, 255)
MUTE = (170, 178, 184)

W, H = 1200, 600
S = 2
img = Image.new("RGB", (W * S, H * S), CHARCOAL)
d = ImageDraw.Draw(img)


def font(sz, bold=True):
    for c in [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, sz * S)
            except Exception:
                pass
    return ImageFont.load_default()


# gradient bg
for y in range(H * S):
    t = y / (H * S)
    col = tuple(int(CHARCOAL2[i] + (CHARCOAL[i] - CHARCOAL2[i]) * t) for i in range(3))
    d.line([(0, y), (W * S, y)], fill=col)

# red glow top-right
glow = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([int(W*S*0.62), int(-H*S*0.4), int(W*S*1.25), int(H*S*0.55)], fill=(204, 0, 0, 70))
from PIL import ImageFilter
glow = glow.filter(ImageFilter.GaussianBlur(120))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
d = ImageDraw.Draw(img)

# 'sa' brand tile
tx, ty, tw, th = 80 * S, 70 * S, 150 * S, 96 * S
tile = Image.new("RGB", (tw, th), RED)
tmask = Image.new("L", (tw, th), 0)
ImageDraw.Draw(tmask).rounded_rectangle([0, 0, tw, th], radius=18 * S, fill=255)
img.paste(tile, (tx, ty), tmask)
d = ImageDraw.Draw(img)
fsa = font(58)
sb = d.textbbox((0, 0), "sa", font=fsa)
d.text((tx + tw/2 - (sb[2]-sb[0])/2 - sb[0], ty + th/2 - (sb[3]-sb[1])/2 - sb[1]), "sa", font=fsa, fill=WHITE)
d.text((tx + tw + 24*S, ty + 16*S), "Sa Systems", font=font(40), fill=WHITE)
d.text((tx + tw + 26*S, ty + 62*S), "ENVIRONMENTAL OPERATIONS", font=font(16, False), fill=MUTE)

# Headline
d.text((80*S, 240*S), "ECOFLOW", font=font(96), fill=WHITE)
# red AI badge
ax = 80*S + d.textbbox((0,0),"ECOFLOW",font=font(96))[2] + 24*S
d.rounded_rectangle([ax, 250*S, ax + 150*S, 340*S], radius=16*S, fill=RED)
d.text((ax + 26*S, 262*S), "AI", font=font(64), fill=WHITE)

d.text((80*S, 372*S), "Predictive Waste & Recycling ERP", font=font(40, False), fill=(225, 228, 231))

# feature bullets
bullets = [
    "AI demand forecasting & smart dispatch",
    "Predictive bin fill & anomaly detection",
    "Region-aware compliance · Odoo 18 / 19",
]
by = 446 * S
for b in bullets:
    d.ellipse([80*S, by + 6*S, 80*S + 14*S, by + 20*S], fill=RED)
    d.text((106*S, by), b, font=font(22, False), fill=(205, 210, 214))
    by += 40 * S

img = img.resize((W, H), Image.LANCZOS)
for t in TARGETS:
    img.save(t)
print("banner saved to", len(TARGETS), "targets")
