"""Master brand-asset generator for ECOFLOW by SA Systems.

Source: the authentic high-res SA Systems logo
(/Users/fahad/Downloads/Sa systems logo.png, transparent RGBA 4308x2574):
red + grey hexagon honeycomb mark over black "sa systems" wordmark.

Produces, for every module:
  static/description/icon.png    512x512  (honeycomb mark on a charcoal tile)
  static/description/banner.png  1200x600 (white-text logo lockup + module glyph)
  static/description/sa_logo.png ~1200w   (white-text logo, transparent)

Plus white-text logo copies for the cockpit, AI center and product site, and a
dark-text transparent copy for light surfaces. Pure Pillow.
"""
import os
from PIL import Image, ImageDraw, ImageFont

SRC = "/Users/fahad/Downloads/Sa systems logo.png"
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
# Load + trim the authentic transparent logo
# ---------------------------------------------------------------------------
src = Image.open(SRC).convert("RGBA")
bbox = src.split()[3].getbbox()
full = src.crop(bbox) if bbox else src
FW, FH = full.size


def white_text(im):
    """Recolour the near-black wordmark to white; keep red + grey + alpha."""
    out = im.copy()
    px = out.load()
    w, h = out.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a > 0 and r < 95 and g < 95 and b < 95:
                px[x, y] = (255, 255, 255, a)
    return out


FULL_WHITE = white_text(full)


def split_mark(im):
    """Return just the honeycomb mark (logo above the wordmark gap)."""
    alpha = im.split()[3]
    sw = 240
    sh = max(1, int(im.size[1] * sw / im.size[0]))
    small = alpha.resize((sw, sh))
    data = list(small.getdata())
    rows = [sum(data[y * sw + x] > 30 for x in range(sw)) for y in range(sh)]
    best_len, best_mid, run, start = 0, sh, 0, None
    for y in range(sh):
        if rows[y] == 0:
            if start is None:
                start = y
            run += 1
        else:
            if run > best_len and start and start > sh * 0.25:
                best_len, best_mid = run, start + run // 2
            run, start = 0, None
    cut = int(best_mid / sh * im.size[1])
    return im.crop((0, 0, im.size[0], cut))


MARK = split_mark(full)
MW, MH = MARK.size


def save_w(im, width, path):
    h = int(im.size[1] * (width / im.size[0]))
    im.resize((width, h), Image.LANCZOS).save(path)


def vgrad(w, h, top, bot):
    g = Image.new("RGB", (w, h), top)
    dd = ImageDraw.Draw(g)
    for y in range(h):
        t = y / max(1, h - 1)
        dd.line([(0, y), (w, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return g


# --- per-module line glyphs --------------------------------------------------
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


def text_left(d, x, cy, s, f, fill):
    b = d.textbbox((0, 0), s, font=f)
    d.text((x - b[0], cy - (b[3] - b[1]) / 2 - b[1]), s, font=f, fill=fill)
    return b[2] - b[0]


def make_icon(mod):
    glyph = GLYPH[mod]
    S = 1024
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    tile = vgrad(S, S, CHARCOAL_2, CHARCOAL_3).convert("RGBA")
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=255)
    out.paste(tile, (0, 0), mask)
    mw = int(S * 0.70)
    mark = MARK.resize((mw, int(MH * mw / MW)), Image.LANCZOS)
    out.alpha_composite(mark, ((S - mw) // 2, (S - mark.size[1]) // 2 - int(S * 0.03)))
    cw = int(S * 0.30)
    cx0, cy0 = S - cw - int(S * 0.055), S - cw - int(S * 0.055)
    cm = Image.new("L", (cw, cw), 0)
    ImageDraw.Draw(cm).rounded_rectangle([0, 0, cw - 1, cw - 1], radius=int(cw * 0.28), fill=255)
    chip = Image.new("RGBA", (cw, cw), RED + (255,))
    out.paste(chip, (cx0, cy0), cm)
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
    logo_w = int(Wd * 0.26)
    logo = FULL_WHITE.resize((logo_w, int(FH * logo_w / FW)), Image.LANCZOS)
    img.alpha_composite(logo, (pad, int(Hd * 0.10)))
    d = ImageDraw.Draw(img)

    text_left(d, pad, int(Hd * .56), "ECOFLOW", font(int(Hd * .095), "black"), WHITE)
    nf = font(int(Hd * .135), "black")
    b = d.textbbox((0, 0), name, font=nf)
    d.text((pad - b[0], int(Hd * .63) - b[1]), name, font=nf, fill=RED_HI)
    text_left(d, pad, int(Hd * .855), tag, font(int(Hd * .05), "bold"), WHITE)
    text_left(d, pad, int(Hd * .92), "by SA Systems  \u00b7  www.sasystems.solutions", font(int(Hd * .033), "reg"), MUTE)

    gx, gy, gs = int(Wd * .66), int(Hd * .26), int(Hd * .54)
    glyph(d, gx, gy, gs, (255, 255, 255), int(Hd * .012))
    glyph(d, gx - 6, gy - 6, gs, RED_HI, int(Hd * .012))

    desc = os.path.join(ADDONS, mod, "static", "description")
    img.convert("RGB").resize((1200, 600), Image.LANCZOS).save(os.path.join(desc, "banner.png"))


if __name__ == "__main__":
    for mod in MODULES:
        desc = os.path.join(ADDONS, mod, "static", "description")
        os.makedirs(desc, exist_ok=True)
        save_w(FULL_WHITE, 1200, os.path.join(desc, "sa_logo.png"))
        make_icon(mod)
        make_banner(mod)
        print("brand assets:", mod)
    for d in (DASH_IMG, AI_IMG, PROD):
        os.makedirs(d, exist_ok=True)
        save_w(FULL_WHITE, 1200, os.path.join(d, "sa_systems_logo.png"))
    save_w(FULL_WHITE, 1800, os.path.join(PROD, "sa_systems_logo_full.png"))
    save_w(full, 1800, os.path.join(PROD, "sa_systems_logo_dark.png"))
    save_w(full, 1200, os.path.join(PROD, "sa_systems_logo_trans.png"))
    print("DONE - mark", MARK.size, "full", full.size)
