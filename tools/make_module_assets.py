"""Generate per-module Odoo App Store assets in the Sa Systems identity.

For every ECOFLOW module this writes:
  addons/<module>/static/description/icon.png    (512x512, store icon)
  addons/<module>/static/description/banner.png  (1200x600, store banner)

Design language: charcoal gradient, brand-red rounded "sa" tile, a per-module
line glyph (drawn with simple vector primitives), the module display name and a
one-line tag. Crisp, modern, on-brand. Pure Pillow -- no external assets needed.
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont

WS = "/Users/fahad/Desktop/Odoo Apps/Waste Management System "
ADDONS = os.path.join(WS, "addons")

# Brand palette (sampled from the Sa Systems logo)
CHARCOAL = (22, 27, 28)
CHARCOAL_2 = (32, 39, 41)
CHARCOAL_3 = (12, 15, 16)
RED = (204, 0, 0)
RED_HI = (232, 72, 44)
WHITE = (255, 255, 255)
MUTE = (171, 181, 186)

FONT_DIR = "/System/Library/Fonts/Supplemental"


def font(size, weight="bold"):
    files = {
        "black": ["Arial Black.ttf", "Arial Bold.ttf"],
        "bold": ["Arial Bold.ttf", "Arial.ttf"],
        "reg": ["Arial.ttf", "Arial Bold.ttf"],
    }[weight]
    for name in files:
        p = os.path.join(FONT_DIR, name)
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    for c in ["/System/Library/Fonts/Helvetica.ttc", "/Library/Fonts/Arial.ttf"]:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()


def vgrad(w, h, top, bot):
    g = Image.new("RGB", (w, h), top)
    dd = ImageDraw.Draw(g)
    for y in range(h):
        t = y / max(1, h - 1)
        col = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        dd.line([(0, y), (w, y)], fill=col)
    return g


def red_tile(w, h, radius_ratio=0.2):
    tile = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    for y in range(h):
        t = y / max(1, h - 1)
        col = tuple(int(RED_HI[i] + (RED[i] - RED_HI[i]) * t) for i in range(3))
        td.line([(0, y), (w, y)], fill=col)
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=int(h * radius_ratio), fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(tile, (0, 0), m)
    return out


def text_center(d, cx, cy, s, f, fill):
    b = d.textbbox((0, 0), s, font=f)
    w, h = b[2] - b[0], b[3] - b[1]
    d.text((cx - w / 2 - b[0], cy - h / 2 - b[1]), s, font=f, fill=fill)


def text_left(d, x, cy, s, f, fill):
    b = d.textbbox((0, 0), s, font=f)
    h = b[3] - b[1]
    d.text((x - b[0], cy - h / 2 - b[1]), s, font=f, fill=fill)
    return b[2] - b[0]


# ---------------------------------------------------------------------------
# Per-module line glyphs. Each draws into ImageDraw `d`, centered in a box
# [x, y, x+sz, y+sz], using brand red strokes on a transparent area.
# ---------------------------------------------------------------------------
def glyph_recycle(d, x, y, sz, col, lw):
    cx, cy = x + sz / 2, y + sz / 2
    r = sz * 0.40
    for k in range(3):
        a0 = 90 + k * 120
        d.arc([cx - r, cy - r, cx + r, cy + r], a0 + 8, a0 + 96, fill=col, width=lw)
        # arrow head
        a = math.radians(a0 + 96)
        ex, ey = cx + r * math.cos(a), cy - r * math.sin(a)
        d.polygon([
            (ex, ey),
            (ex - lw * 1.6 * math.cos(a - 0.5), ey + lw * 1.6 * math.sin(a - 0.5)),
            (ex - lw * 1.6 * math.cos(a + 0.5), ey + lw * 1.6 * math.sin(a + 0.5)),
        ], fill=col)


def glyph_layers(d, x, y, sz, col, lw):
    # stacked database/foundation layers
    cx = x + sz / 2
    w = sz * 0.62
    h = sz * 0.16
    for i, yy in enumerate([0.30, 0.50, 0.70]):
        cy = y + sz * yy
        d.ellipse([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], outline=col, width=lw)


def glyph_truck(d, x, y, sz, col, lw):
    # collection truck silhouette (line)
    bx, by = x + sz * 0.16, y + sz * 0.34
    bw, bh = sz * 0.42, sz * 0.30
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=int(sz * 0.04), outline=col, width=lw)
    cab_x = bx + bw
    d.line([(cab_x, by + bh * 0.15), (cab_x + sz * 0.22, by + bh * 0.15)], fill=col, width=lw)
    d.line([(cab_x + sz * 0.22, by + bh * 0.15), (cab_x + sz * 0.22, by + bh)], fill=col, width=lw)
    d.line([(cab_x, by + bh), (cab_x + sz * 0.22, by + bh)], fill=col, width=lw)
    r = sz * 0.075
    for wx in [bx + bw * 0.3, cab_x + sz * 0.12]:
        wy = by + bh + r * 0.6
        d.ellipse([wx - r, wy - r, wx + r, wy + r], outline=col, width=lw)


def glyph_route(d, x, y, sz, col, lw):
    # winding route with pins
    pts = [
        (x + sz * 0.18, y + sz * 0.74),
        (x + sz * 0.40, y + sz * 0.40),
        (x + sz * 0.60, y + sz * 0.62),
        (x + sz * 0.82, y + sz * 0.26),
    ]
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=col, width=lw)
    for px, py in [pts[0], pts[-1]]:
        rr = sz * 0.06
        d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=col)


def glyph_scale(d, x, y, sz, col, lw):
    # weighbridge / balance
    cx = x + sz / 2
    top = y + sz * 0.20
    d.line([(cx, top), (cx, y + sz * 0.78)], fill=col, width=lw)
    d.line([(x + sz * 0.22, top), (x + sz * 0.78, top)], fill=col, width=lw)
    d.line([(x + sz * 0.30, y + sz * 0.80), (x + sz * 0.70, y + sz * 0.80)], fill=col, width=lw)
    for sx in [x + sz * 0.22, x + sz * 0.78]:
        d.arc([sx - sz * 0.14, top + sz * 0.02, sx + sz * 0.14, top + sz * 0.30], 0, 180, fill=col, width=lw)
        d.line([(sx - sz * 0.14, top), (sx, top + sz * 0.16)], fill=col, width=max(1, lw - 1))
        d.line([(sx + sz * 0.14, top), (sx, top + sz * 0.16)], fill=col, width=max(1, lw - 1))


def glyph_shield(d, x, y, sz, col, lw):
    # compliance shield with check
    cx = x + sz / 2
    top = y + sz * 0.20
    w = sz * 0.50
    pts = [
        (cx - w / 2, top),
        (cx + w / 2, top),
        (cx + w / 2, y + sz * 0.55),
        (cx, y + sz * 0.82),
        (cx - w / 2, y + sz * 0.55),
    ]
    d.line(pts + [pts[0]], fill=col, width=lw, joint="curve")
    d.line([(cx - w * 0.22, y + sz * 0.47), (cx - w * 0.02, y + sz * 0.62),
            (cx + w * 0.30, y + sz * 0.34)], fill=col, width=lw, joint="curve")


def glyph_dash(d, x, y, sz, col, lw):
    # dashboard: bars + arc gauge
    base = y + sz * 0.74
    for i, hh in enumerate([0.22, 0.40, 0.30, 0.50]):
        bx = x + sz * (0.20 + i * 0.15)
        d.line([(bx, base), (bx, base - sz * hh)], fill=col, width=lw)
    d.arc([x + sz * 0.16, y + sz * 0.12, x + sz * 0.84, y + sz * 0.80], 200, 340, fill=col, width=lw)


def glyph_ai(d, x, y, sz, col, lw):
    # neural nodes
    nodes = [
        (x + sz * 0.24, y + sz * 0.30), (x + sz * 0.24, y + sz * 0.70),
        (x + sz * 0.50, y + sz * 0.22), (x + sz * 0.50, y + sz * 0.50), (x + sz * 0.50, y + sz * 0.78),
        (x + sz * 0.76, y + sz * 0.40), (x + sz * 0.76, y + sz * 0.62),
    ]
    edges = [(0, 2), (0, 3), (1, 3), (1, 4), (2, 5), (3, 5), (3, 6), (4, 6)]
    for a, b in edges:
        d.line([nodes[a], nodes[b]], fill=col, width=max(1, lw - 1))
    rr = sz * 0.045
    for nx, ny in nodes:
        d.ellipse([nx - rr, ny - rr, nx + rr, ny + rr], fill=col)


GLYPHS = {
    "ecoflow_base": glyph_layers,
    "ecoflow_collection": glyph_truck,
    "ecoflow_routing": glyph_route,
    "ecoflow_recycling": glyph_recycle,
    "ecoflow_compliance": glyph_shield,
    "ecoflow_dashboard": glyph_dash,
    "ecoflow_ai": glyph_ai,
}

MODULES = {
    "ecoflow_base": ("BASE", "Foundation & Masters", "Waste streams \u00b7 materials \u00b7 zones \u00b7 bins"),
    "ecoflow_collection": ("COLLECTION", "Service & Proof of Service", "Service orders \u00b7 RFID \u00b7 geo \u00b7 photo"),
    "ecoflow_routing": ("ROUTING", "Routes & Dispatch", "Stop sequencing \u00b7 fleet \u00b7 drivers"),
    "ecoflow_recycling": ("RECYCLING", "Weighbridge & Recovery", "Tickets \u00b7 MRF \u00b7 diversion yield"),
    "ecoflow_compliance": ("COMPLIANCE", "Manifests & Permits", "Waste codes \u00b7 chain of custody"),
    "ecoflow_dashboard": ("DASHBOARD", "Cockpit & Branding", "KPIs \u00b7 graphs \u00b7 settings"),
    "ecoflow_ai": ("AI INTELLIGENCE", "Forecasting & Insights", "Predict \u00b7 detect \u00b7 recommend"),
}


# ---------------------------------------------------------------------------
def make_icon(module):
    name, _, _ = MODULES[module]
    glyph = GLYPHS[module]
    S = 1024
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))

    bg = vgrad(S, S, CHARCOAL_2, CHARCOAL_3)
    # red radial glow top-left
    glow = Image.new("L", (S, S), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-S * 0.2, -S * 0.25, S * 0.6, S * 0.45], fill=70)
    glow = glow.resize((S, S))
    red_layer = Image.new("RGB", (S, S), RED)
    bg = Image.composite(red_layer, bg, glow.point(lambda v: int(v * 0.45)))

    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=255)
    img.paste(bg, (0, 0), mask)
    d = ImageDraw.Draw(img)

    # thin red inner border
    d.rounded_rectangle([S * 0.035, S * 0.035, S - S * 0.035, S - S * 0.035],
                        radius=int(S * 0.19), outline=(80, 22, 22), width=int(S * 0.006))

    # module glyph, large, upper area
    glyph(d, int(S * 0.30), int(S * 0.12), int(S * 0.40), RED_HI, int(S * 0.022))

    # red 'sa' tile
    tw, th = int(S * 0.42), int(S * 0.27)
    tile = red_tile(tw, th, 0.20)
    tx, ty = (S - tw) // 2, int(S * 0.50)
    img.paste(tile, (tx, ty), tile)
    d = ImageDraw.Draw(img)
    text_center(d, tx + tw / 2, ty + th / 2, "sa", font(int(th * 0.72), "black"), WHITE)

    # ECOFLOW + module name
    text_center(d, S / 2, int(S * 0.835), "ECOFLOW", font(int(S * 0.064), "black"), WHITE)
    text_center(d, S / 2, int(S * 0.90), name, font(int(S * 0.040), "bold"), (224, 96, 78))

    desc = os.path.join(ADDONS, module, "static", "description")
    os.makedirs(desc, exist_ok=True)
    img.resize((512, 512), Image.LANCZOS).save(os.path.join(desc, "icon.png"))


def make_banner(module):
    name, tag, sub = MODULES[module]
    glyph = GLYPHS[module]
    W, H = 2400, 1200  # supersample 2x of 1200x600
    img = vgrad(W, H, CHARCOAL_2, CHARCOAL_3).convert("RGBA")

    # red glow right side
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([W * 0.55, -H * 0.3, W * 1.25, H * 1.2], fill=90)
    red_layer = Image.new("RGB", (W, H), RED)
    base = Image.composite(red_layer, img.convert("RGB"), glow.point(lambda v: int(v * 0.5)))
    img = base.convert("RGBA")
    d = ImageDraw.Draw(img)

    # faint diagonal grid texture
    for gx in range(-H, W, 90):
        d.line([(gx, 0), (gx + H, H)], fill=(255, 255, 255, 8), width=2)

    pad = int(W * 0.07)
    # red 'sa' tile top-left as logo lockup
    tw, th = int(W * 0.085), int(W * 0.085)
    tile = red_tile(tw, th, 0.22)
    img.paste(tile, (pad, int(H * 0.10)), tile)
    d = ImageDraw.Draw(img)
    text_center(d, pad + tw / 2, int(H * 0.10) + th / 2, "sa", font(int(th * 0.70), "black"), WHITE)
    text_left(d, pad + tw + int(W * 0.018), int(H * 0.10) + th / 2 - int(H * 0.03),
              "Sa Systems", font(int(H * 0.05), "black"), WHITE)
    text_left(d, pad + tw + int(W * 0.018), int(H * 0.10) + th / 2 + int(H * 0.035),
              "ENVIRONMENTAL OPERATIONS", font(int(H * 0.026), "bold"), (208, 214, 218))

    # big module title
    text_left(d, pad, int(H * 0.46), "ECOFLOW", font(int(H * 0.095), "black"), WHITE)
    # name in red
    nx = pad
    ny = int(H * 0.60)
    nf = font(int(H * 0.135), "black")
    b = d.textbbox((0, 0), name, font=nf)
    d.text((nx - b[0], ny - b[1] - (b[3] - b[1]) / 2 + int(H * 0.06)), name, font=nf, fill=(232, 72, 44))

    # tagline + sub
    text_left(d, pad, int(H * 0.80), tag, font(int(H * 0.05), "bold"), WHITE)
    text_left(d, pad, int(H * 0.875), sub, font(int(H * 0.036), "reg"), MUTE)

    # giant glyph on the right
    gx = int(W * 0.66)
    gy = int(H * 0.20)
    gs = int(H * 0.62)
    glyph(d, gx, gy, gs, (255, 255, 255), int(H * 0.012))
    glyph(d, gx - 6, gy - 6, gs, (232, 72, 44), int(H * 0.012))

    desc = os.path.join(ADDONS, module, "static", "description")
    os.makedirs(desc, exist_ok=True)
    img.convert("RGB").resize((1200, 600), Image.LANCZOS).save(os.path.join(desc, "banner.png"))


if __name__ == "__main__":
    for m in MODULES:
        make_icon(m)
        make_banner(m)
        print("assets:", m)
    print("done")
