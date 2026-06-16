"""Master brand-asset generator for ECOFLOW by SA Systems.

Uses the AUTHENTIC high-res SA Systems logo
(/Users/fahad/Desktop/SAG/sasystems-logo option 2.jpg, CMYK 3557x1685) and
produces, for every module:
  static/description/icon.png    512x512  (authentic red "sa" block, rounded)
  static/description/banner.png  1200x600 (real logo lockup + module glyph)
  static/description/sa_logo.png ~1400w   (full real logo, charcoal bg, trimmed)

Also refreshes the cockpit/product copies. Pure Pillow.
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageChops

SRC = "/Users/fahad/Desktop/SAG/sasystems-logo option 2.jpg"
WS = "/Users/fahad/Desktop/Odoo Apps/Waste Management System "
ADDONS = os.path.join(WS, "addons")
PROD = os.path.join(WS, "product", "assets")
DASH_IMG = os.path.join(ADDONS, "ecoflow_dashboard", "static", "src", "img")
AI_IMG = os.path.join(ADDONS, "ecoflow_ai", "static", "src", "img")

CHARCOAL = (22, 27, 28)
CHARCOAL_2 = (30, 38, 41)
CHARCOAL_3 = (12, 15, 16)
RED = (204, 0, 0)
RED_HI = (232, 72, 44)
WHITE = (255, 255, 255)
MUTE = (171, 181, 186)
FONT_DIR = "/System/Library/Fonts/Supplemental"


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


# ---------------------------------------------------------------------------
# Load + prepare the authentic logo
# ---------------------------------------------------------------------------
src = Image.open(SRC)
if src.mode != "RGB":
    src = src.convert("RGB")
W, H = src.size
px = src.load()
charcoal_bg = px[20, 20][:3]
red_sample = px[int(W * 0.18), int(H * 0.45)][:3]

# trim uniform charcoal margins -> full logo
bg = Image.new("RGB", src.size, charcoal_bg)
bbox = ImageChops.difference(src, bg).getbbox()
m = 50
if bbox:
    bbox = (max(bbox[0] - m, 0), max(bbox[1] - m, 0),
            min(bbox[2] + m, W), min(bbox[3] + m, H))
    full = src.crop(bbox)
else:
    full = src
FW, FH = full.size

# detect the red "sa" block bounding box (authentic icon element)
xs, ys = [], []
for y in range(0, H, 4):
    for x in range(0, W, 4):
        r, g, b = px[x, y][:3]
        if r > 150 and g < 90 and b < 90:
            xs.append(x); ys.append(y)
rx0, ry0, rx1, ry1 = min(xs), min(ys), max(xs), max(ys)


def save_w(im, width, path):
    h = int(im.size[1] * (width / im.size[0]))
    im.resize((width, h), Image.LANCZOS).save(path)


def rounded(im, frac=0.22):
    s = im.size[0]
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, s, s], radius=int(s * frac), fill=255)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    return out


def vgrad(w, h, top, bot):
    g = Image.new("RGB", (w, h), top)
    dd = ImageDraw.Draw(g)
    for y in range(h):
        t = y / max(1, h - 1)
        dd.line([(0, y), (w, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return g


# authentic "sa" red block icon (square, rounded) ------------------------------
# crop TIGHT to the red block only (exclude black frame + "Systems" box)
inset_x = int((rx1 - rx0) * 0.015)
inset_y = int((ry1 - ry0) * 0.015)
crop = src.crop((rx0 + inset_x, ry0 + inset_y, rx1 - inset_x, ry1 - inset_y))
# square red canvas with even margin, the authentic "sa" centered
margin = int(max(crop.size) * 0.16)
side = max(crop.size) + margin * 2
icon_sq = Image.new("RGB", (side, side), red_sample)
icon_sq.paste(crop, ((side - crop.size[0]) // 2, (side - crop.size[1]) // 2))
ICON_BLOCK = icon_sq.resize((512, 512), Image.LANCZOS)


# per-module line glyphs (subtle accent, drawn) -------------------------------
def g_layers(d, x, y, s, c, lw):
    cx = x + s / 2; w = s * 0.6; h = s * 0.16
    for yy in (0.30, 0.50, 0.70):
        cy = y + s * yy
        d.ellipse([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], outline=c, width=lw)


def g_truck(d, x, y, s, c, lw):
    bx, by = x + s * 0.14, y + s * 0.36; bw, bh = s * 0.42, s * 0.30
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=int(s * 0.04), outline=c, width=lw)
    cab = bx + bw
    d.line([(cab, by + bh * .15), (cab + s * .22, by + bh * .15)], fill=c, width=lw)
    d.line([(cab + s * .22, by + bh * .15), (cab + s * .22, by + bh)], fill=c, width=lw)
    d.line([(cab, by + bh), (cab + s * .22, by + bh)], fill=c, width=lw)
    r = s * 0.075
    for wx in (bx + bw * .3, cab + s * .12):
        wy = by + bh + r * .6
        d.ellipse([wx - r, wy - r, wx + r, wy + r], outline=c, width=lw)


def g_route(d, x, y, s, c, lw):
    pts = [(x + s * .18, y + s * .74), (x + s * .40, y + s * .40), (x + s * .60, y + s * .62), (x + s * .82, y + s * .26)]
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=c, width=lw)
    for pxy in (pts[0], pts[-1]):
        rr = s * .06
        d.ellipse([pxy[0] - rr, pxy[1] - rr, pxy[0] + rr, pxy[1] + rr], fill=c)


def g_recycle(d, x, y, s, c, lw):
    cx, cy = x + s / 2, y + s / 2; r = s * .40
    for k in range(3):
        a0 = 90 + k * 120
        d.arc([cx - r, cy - r, cx + r, cy + r], a0 + 8, a0 + 96, fill=c, width=lw)


def g_scale(d, x, y, s, c, lw):
    cx = x + s / 2; top = y + s * .20
    d.line([(cx, top), (cx, y + s * .78)], fill=c, width=lw)
    d.line([(x + s * .22, top), (x + s * .78, top)], fill=c, width=lw)
    d.line([(x + s * .30, y + s * .80), (x + s * .70, y + s * .80)], fill=c, width=lw)
    for sx in (x + s * .22, x + s * .78):
        d.arc([sx - s * .14, top + s * .02, sx + s * .14, top + s * .30], 0, 180, fill=c, width=lw)


def g_shield(d, x, y, s, c, lw):
    cx = x + s / 2; top = y + s * .20; w = s * .50
    pts = [(cx - w / 2, top), (cx + w / 2, top), (cx + w / 2, y + s * .55), (cx, y + s * .82), (cx - w / 2, y + s * .55)]
    d.line(pts + [pts[0]], fill=c, width=lw, joint="curve")
    d.line([(cx - w * .22, y + s * .47), (cx - w * .02, y + s * .62), (cx + w * .30, y + s * .34)], fill=c, width=lw, joint="curve")


def g_dash(d, x, y, s, c, lw):
    base = y + s * .74
    for i, hh in enumerate((.22, .40, .30, .50)):
        bx = x + s * (.20 + i * .15)
        d.line([(bx, base), (bx, base - s * hh)], fill=c, width=lw)
    d.arc([x + s * .16, y + s * .12, x + s * .84, y + s * .80], 200, 340, fill=c, width=lw)


def g_ai(d, x, y, s, c, lw):
    nodes = [(x + s * .24, y + s * .30), (x + s * .24, y + s * .70), (x + s * .50, y + s * .22),
             (x + s * .50, y + s * .50), (x + s * .50, y + s * .78), (x + s * .76, y + s * .40), (x + s * .76, y + s * .62)]
    for a, b in [(0, 2), (0, 3), (1, 3), (1, 4), (2, 5), (3, 5), (3, 6), (4, 6)]:
        d.line([nodes[a], nodes[b]], fill=c, width=max(1, lw - 1))
    for nx, ny in nodes:
        rr = s * .045
        d.ellipse([nx - rr, ny - rr, nx + rr, ny + rr], fill=c)


GLYPH = {"ecoflow_base": g_layers, "ecoflow_collection": g_truck, "ecoflow_routing": g_route,
         "ecoflow_recycling": g_recycle, "ecoflow_compliance": g_shield,
         "ecoflow_dashboard": g_dash, "ecoflow_ai": g_ai}

MODULES = {
    "ecoflow_base": ("BASE", "Foundation & Masters"),
    "ecoflow_collection": ("COLLECTION", "Service & Proof of Service"),
    "ecoflow_routing": ("ROUTING", "Routes & Dispatch"),
    "ecoflow_recycling": ("RECYCLING", "Weighbridge & Recovery"),
    "ecoflow_compliance": ("COMPLIANCE", "Manifests & Permits"),
    "ecoflow_dashboard": ("DASHBOARD", "Cockpit & Branding"),
    "ecoflow_ai": ("AI INTELLIGENCE", "Forecasting & Insights"),
}


def text_center(d, cx, cy, s, f, fill):
    b = d.textbbox((0, 0), s, font=f)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], cy - (b[3] - b[1]) / 2 - b[1]), s, font=f, fill=fill)


def text_left(d, x, cy, s, f, fill):
    b = d.textbbox((0, 0), s, font=f)
    d.text((x - b[0], cy - (b[3] - b[1]) / 2 - b[1]), s, font=f, fill=fill)
    return b[2] - b[0]


def make_icon(mod):
    name = MODULES[mod][0]
    glyph = GLYPH[mod]
    S = 1024
    base = ICON_BLOCK.resize((S, S), Image.LANCZOS).convert("RGBA")
    # rounded mask
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=255)
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    out.paste(base, (0, 0), mask)
    d = ImageDraw.Draw(out)
    # subtle charcoal chip bottom-right holding the module glyph
    cw = int(S * 0.34)
    cx0, cy0 = S - cw - int(S * 0.05), S - cw - int(S * 0.05)
    chip = Image.new("RGBA", (cw, cw), (0, 0, 0, 0))
    cm = Image.new("L", (cw, cw), 0)
    ImageDraw.Draw(cm).rounded_rectangle([0, 0, cw - 1, cw - 1], radius=int(cw * 0.26), fill=235)
    chipbg = Image.new("RGBA", (cw, cw), (18, 22, 24, 255))
    out.paste(chipbg, (cx0, cy0), cm)
    d = ImageDraw.Draw(out)
    glyph(d, cx0 + int(cw * 0.14), cy0 + int(cw * 0.14), int(cw * 0.72), WHITE, int(S * 0.016))
    desc = os.path.join(ADDONS, mod, "static", "description")
    os.makedirs(desc, exist_ok=True)
    out.resize((512, 512), Image.LANCZOS).save(os.path.join(desc, "icon.png"))


def make_banner(mod):
    name, tag = MODULES[mod]
    glyph = GLYPH[mod]
    Wd, Hd = 2400, 1200
    img = vgrad(Wd, Hd, CHARCOAL_2, CHARCOAL_3).convert("RGBA")
    glow = Image.new("L", (Wd, Hd), 0)
    ImageDraw.Draw(glow).ellipse([Wd * .55, -Hd * .3, Wd * 1.25, Hd * 1.2], fill=90)
    img = Image.composite(Image.new("RGB", (Wd, Hd), RED), img.convert("RGB"),
                          glow.point(lambda v: int(v * .5))).convert("RGBA")
    d = ImageDraw.Draw(img)
    for gx in range(-Hd, Wd, 90):
        d.line([(gx, 0), (gx + Hd, Hd)], fill=(255, 255, 255, 8), width=2)

    pad = int(Wd * .065)
    # REAL logo, composited top-left (charcoal-on-charcoal blends cleanly)
    logo_w = int(Wd * 0.30)
    logo = full.resize((logo_w, int(FH * logo_w / FW)), Image.LANCZOS)
    img.paste(logo, (pad, int(Hd * 0.085)))
    d = ImageDraw.Draw(img)

    # big module title
    text_left(d, pad, int(Hd * .52), "ECOFLOW", font(int(Hd * .095), "black"), WHITE)
    nf = font(int(Hd * .135), "black")
    b = d.textbbox((0, 0), name, font=nf)
    d.text((pad - b[0], int(Hd * .60) - b[1] - (b[3] - b[1]) / 2 + int(Hd * .06)), name, font=nf, fill=RED_HI)
    text_left(d, pad, int(Hd * .82), tag, font(int(Hd * .05), "bold"), WHITE)
    text_left(d, pad, int(Hd * .89), "by SA Systems  \u00b7  www.sasystems.solutions", font(int(Hd * .034), "reg"), MUTE)

    gx, gy, gs = int(Wd * .66), int(Hd * .26), int(Hd * .54)
    glyph(d, gx, gy, gs, (255, 255, 255), int(Hd * .012))
    glyph(d, gx - 6, gy - 6, gs, RED_HI, int(Hd * .012))

    desc = os.path.join(ADDONS, mod, "static", "description")
    img.convert("RGB").resize((1200, 600), Image.LANCZOS).save(os.path.join(desc, "banner.png"))


if __name__ == "__main__":
    # distribute the full real logo everywhere
    for mod in MODULES:
        desc = os.path.join(ADDONS, mod, "static", "description")
        os.makedirs(desc, exist_ok=True)
        save_w(full, 1400, os.path.join(desc, "sa_logo.png"))
        make_icon(mod)
        make_banner(mod)
        print("brand assets:", mod)
    # cockpit + AI + product copies (charcoal-bg full logo)
    for d in (DASH_IMG, AI_IMG, PROD):
        os.makedirs(d, exist_ok=True)
        save_w(full, 1200, os.path.join(d, "sa_systems_logo.png"))
    save_w(full, 1600, os.path.join(PROD, "sa_systems_logo_full.png"))
    print("DONE charcoal", "#%02X%02X%02X" % charcoal_bg, "red", "#%02X%02X%02X" % red_sample)
