"""Render a high-resolution ECOFLOW Operations Cockpit demo image.

Uses the real KPI values verified from the live Odoo database and the
Sa Systems brand palette / logo. Produces a crisp marketing-grade PNG
that mirrors the in-app OWL cockpit layout.
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.path.join(BASE, "product", "assets", "sa_systems_logo.png")
OUT = os.path.join(BASE, "product", "assets", "demo_cockpit.png")

# Brand palette
GREEN = (22, 163, 74)
BLUE = (14, 165, 233)
AMBER = (245, 158, 11)
RED = (239, 68, 68)
INK = (15, 23, 42)
SUBTLE = (100, 116, 139)
CANVAS = (244, 247, 250)
CARD = (255, 255, 255)
BORDER = (226, 232, 240)

W, H = 1480, 1020
SCALE = 2  # supersample for crisp text
img = Image.new("RGB", (W * SCALE, H * SCALE), CANVAS)
d = ImageDraw.Draw(img)


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size * SCALE)
            except Exception:
                continue
    return ImageFont.load_default()


def rrect(box, radius, fill=None, outline=None, width=1):
    d.rounded_rectangle(
        [box[0] * SCALE, box[1] * SCALE, box[2] * SCALE, box[3] * SCALE],
        radius=radius * SCALE, fill=fill, outline=outline, width=width * SCALE,
    )


def text(pos, s, fnt, fill, anchor="la"):
    d.text((pos[0] * SCALE, pos[1] * SCALE), s, font=fnt, fill=fill, anchor=anchor)


def hgrad(box, c1, c2, radius=0):
    x0, y0, x1, y1 = box
    w = (x1 - x0) * SCALE
    h = (y1 - y0) * SCALE
    grad = Image.new("RGB", (w, h), c1)
    gd = ImageDraw.Draw(grad)
    for x in range(w):
        t = x / max(w - 1, 1)
        col = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
        gd.line([(x, 0), (x, h)], fill=col)
    if radius:
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, w, h], radius=radius * SCALE, fill=255)
        img.paste(grad, (x0 * SCALE, y0 * SCALE), mask)
    else:
        img.paste(grad, (x0 * SCALE, y0 * SCALE))


PAD = 40

# ---- Hero ----
hero = (PAD, PAD, W - PAD, 196)
hgrad(hero, GREEN, BLUE, radius=22)
# logo
try:
    logo = Image.open(LOGO).convert("RGBA")
    lh = 70 * SCALE
    lw = int(logo.width * (lh / logo.height))
    logo = logo.resize((lw, lh))
    # white rounded chip behind logo
    chip = (PAD + 28, 70, PAD + 28 + lw // SCALE + 28, 70 + 86)
    rrect(chip, 16, fill=CARD)
    img.paste(logo, ((PAD + 42) * SCALE, 78 * SCALE), logo)
    title_x = chip[2] + 28
except Exception:
    title_x = PAD + 40

text((title_x, 78), "ECOFLOW", font(34, True), (255, 255, 255))
text((title_x, 122), "Operations Cockpit", font(22, False), (235, 255, 245))
text((title_x, 154), "Real-time environmental operations & diversion performance",
     font(14), (225, 245, 240))
# refresh pill
rrect((W - PAD - 150, 92, W - PAD - 28, 132), 20, fill=(255, 255, 255))
text((W - PAD - 89, 112), "\u21bb  Refresh", font(15, True), GREEN, anchor="mm")


def section_label(y, label):
    text((PAD + 4, y), label.upper(), font(13, True), SUBTLE)
    text((PAD + 4, y), label.upper(), font(13, True), SUBTLE)


def kpi_card(box, label, value, sub, accent, bar=None):
    rrect(box, 16, fill=CARD, outline=BORDER, width=1)
    # accent bar on left
    d.rounded_rectangle(
        [box[0] * SCALE, (box[1] + 14) * SCALE, (box[0] + 6) * SCALE, (box[3] - 14) * SCALE],
        radius=3 * SCALE, fill=accent,
    )
    text((box[0] + 24, box[1] + 20), label.upper(), font(12, True), SUBTLE)
    text((box[0] + 24, box[1] + 44), value, font(42, True), INK)
    text((box[0] + 24, box[3] - 34), sub, font(13), SUBTLE)
    if bar is not None:
        bx0, bx1 = box[0] + 24, box[2] - 24
        by = box[3] - 52
        d.rounded_rectangle([bx0 * SCALE, by * SCALE, bx1 * SCALE, (by + 8) * SCALE],
                            radius=4 * SCALE, fill=(237, 242, 247))
        fillw = bx0 + (bx1 - bx0) * min(bar, 1.0)
        d.rounded_rectangle([bx0 * SCALE, by * SCALE, fillw * SCALE, (by + 8) * SCALE],
                            radius=4 * SCALE, fill=accent)


def row(y, cards):
    n = len(cards)
    gap = 24
    total = W - 2 * PAD
    cw = (total - gap * (n - 1)) / n
    ch = 150
    for i, c in enumerate(cards):
        x0 = PAD + i * (cw + gap)
        kpi_card((x0, y, x0 + cw, y + ch), *c)
    return y + ch


# ---- Section 1: Today's Collections ----
y = 230
section_label(y, "Today's Collections")
y = row(y + 26, [
    ("Orders Scheduled", "8", "For today", GREEN, None),
    ("Serviced", "3", "37.5% completion", GREEN, 0.375),
    ("Missed", "1", "Needs follow-up", RED, None),
    ("Active Routes", "1", "13.1 km planned", BLUE, None),
])

# ---- Section 2: Recovery & Diversion ----
y += 34
section_label(y, "Recovery & Diversion")
y = row(y + 26, [
    ("Diversion Rate", "85%", "Target 75%", GREEN, 0.85),
    ("Tonnes Handled", "30.1", "Posted weigh tickets", BLUE, None),
    ("Recovered Material", "8,500 kg", "From completed batches", GREEN, None),
])

# ---- Section 3: Compliance ----
y += 34
section_label(y, "Compliance")
y = row(y + 26, [
    ("Permits Expiring", "2", "Within expiry window", AMBER, None),
    ("Permits Expired", "0", "Action required", GREEN, None),
    ("Open Manifests", "1", "In progress", BLUE, None),
])

# ---- Footer strip ----
text((PAD + 4, H - 40), "Sa Systems  \u2022  ECOFLOW Environmental Operations  \u2022  Odoo 18 / 19",
     font(13), SUBTLE)

img = img.resize((W, H), Image.LANCZOS)
img.save(OUT)
print("Saved", OUT, img.size)
