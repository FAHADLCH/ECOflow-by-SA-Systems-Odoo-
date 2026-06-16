"""Premium Odoo Apps Store description panels for the single ECOFLOW app.

The Odoo Apps Store sanitises description HTML and strips ALL inline CSS, so a
styled <div> layout collapses to plain text. To guarantee the page renders
exactly as designed, the whole premium layout is baked into image panels here
and index.html becomes a clean stack of <img> tags.

Pure Pillow, designed at 2x and downscaled to 1200px-wide PNGs for crisp retina.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WS = "/Users/fahad/Desktop/Odoo Apps/Waste Management System "
DESC = os.path.join(WS, "ecoflow", "static", "description")
FONT_DIR = "/System/Library/Fonts/Supplemental"

# ---- palette -------------------------------------------------------------
RED = (204, 0, 0)
RED_HI = (232, 72, 44)
CHAR0 = (12, 15, 16)
CHAR1 = (22, 27, 28)
CHAR2 = (30, 38, 41)
INK = (22, 27, 28)
BODY = (82, 88, 92)
SUB = (106, 111, 116)
MUTE = (174, 180, 184)
FAINT = (199, 204, 208)
CARDBG = (255, 255, 255)
CARDBORD = (231, 233, 235)
LIGHTBG = (238, 240, 241)
PANEL_LIGHT = (244, 246, 247)
REDTINT = (253, 236, 234)
WHITE = (255, 255, 255)

S = 2                 # supersample factor
W = 1200 * S          # working width
M = 70 * S            # outer margin


def font(size, weight="bold"):
    files = {"black": ["Arial Black.ttf", "Arial Bold.ttf"],
             "bold": ["Arial Bold.ttf", "Arial.ttf"],
             "reg": ["Arial.ttf", "Arial Bold.ttf"]}[weight]
    for name in files:
        p = os.path.join(FONT_DIR, name)
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, int(size))
            except Exception:
                pass
    return ImageFont.load_default()


def vgrad(w, h, top_c, bot_c):
    g = Image.new("L", (1, h))
    for y in range(h):
        g.putpixel((0, y), int(255 * y / max(1, h - 1)))
    g = g.resize((w, h))
    return Image.composite(Image.new("RGB", (w, h), bot_c),
                           Image.new("RGB", (w, h), top_c), g)


def hgrad(w, h, left_c, right_c):
    g = Image.new("L", (w, 1))
    for x in range(w):
        g.putpixel((x, 0), int(255 * x / max(1, w - 1)))
    g = g.resize((w, h))
    return Image.composite(Image.new("RGB", (w, h), right_c),
                           Image.new("RGB", (w, h), left_c), g)


def glow(panel, cx, cy, radius, color, alpha):
    layer = Image.new("RGBA", panel.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
              fill=color + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(radius // 3))
    panel.alpha_composite(layer)


def round_grad(w, h, c0, c1, r):
    base = hgrad(w, h, c0, c1).convert("RGBA")
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(base, (0, 0), mask)
    return out


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def par(d, x, y, text, fnt, fill, max_w, leading):
    for ln in wrap(d, text, fnt, max_w):
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def eyebrow(d, x, y, text, color=RED, size=15 * S):
    f = font(size, "black")
    d.text((x, y), text.upper(), font=f, fill=color)
    return y


def tri(d, x, y, s, color):
    d.polygon([(x, y), (x, y + s), (x + int(s * 0.85), y + s // 2)], fill=color)


def check_badge(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    w = max(2 * S, int(r * 0.34))
    d.line([(cx - int(r * 0.45), cy + int(r * 0.02)),
            (cx - int(r * 0.05), cy + int(r * 0.4)),
            (cx + int(r * 0.5), cy - int(r * 0.4))], fill=WHITE, width=w,
           joint="curve")


def save(panel, name):
    if panel.mode == "RGBA":
        bg = Image.new("RGB", panel.size, WHITE)
        bg.paste(panel, (0, 0), panel)
        panel = bg
    panel = panel.resize((panel.width // S, panel.height // S), Image.LANCZOS)
    out = os.path.join(DESC, name)
    panel.save(out, "PNG")
    print("saved", name, panel.size)


# =========================================================================
# 1. HERO
# =========================================================================
def panel_hero():
    H = 600 * S
    img = Image.new("RGB", (W, H), PANEL_LIGHT)
    d = ImageDraw.Draw(img)
    x = M
    y = 84 * S
    # red pill
    pill_f = font(16 * S, "black")
    pt = "THE COMPLETE PLATFORM  ·  ONE APP"
    pw = d.textlength(pt, font=pill_f)
    ph = 46 * S
    pill = round_grad(int(pw) + 44 * S, ph, RED, RED_HI, ph // 2)
    img.paste(pill, (x, y), pill)
    d.text((x + 22 * S, y + 12 * S), pt, font=pill_f, fill=WHITE)
    y += ph + 34 * S
    # headline (two lines, second red) — auto-fit to column width
    l1 = "The AI-native command center for"
    l2 = "waste, recycling & the circular economy."
    hsize = 58 * S
    while hsize > 30 * S:
        h1 = font(hsize, "black")
        if max(d.textlength(l1, font=h1),
               d.textlength(l2, font=h1)) <= W - 2 * M:
            break
        hsize -= S
    h1 = font(hsize, "black")
    lh = int(hsize * 1.16)
    d.text((x, y), l1, font=h1, fill=INK)
    y += lh
    d.text((x, y), l2, font=h1, fill=RED)
    y += lh + 26 * S
    # subtitle
    body_f = font(23 * S, "reg")
    y = par(d, x, y,
            "ECOFLOW turns a waste hauler into a data-driven environmental "
            "operations platform. Every bin lifted, kilometre driven and tonne "
            "recovered is captured once, reconciled automatically, and turned "
            "into a decision \u2014 powered by forecasting AI that runs entirely "
            "on your own server.",
            body_f, BODY, W - 2 * M, 38 * S)
    y += 26 * S
    # value pills
    chips = ["AI demand forecasting", "Predictive bin fill",
             "Smart route optimization", "Live operations cockpit",
             "e-Chain-of-custody"]
    cf = font(18 * S, "bold")
    cx, cy = x, y
    for c in chips:
        cw = int(d.textlength(c, font=cf)) + 36 * S
        if cx + cw > W - M:
            cx = x
            cy += 56 * S
        d.rounded_rectangle([cx, cy, cx + cw, cy + 44 * S], 22 * S, fill=CHAR1)
        d.text((cx + 18 * S, cy + 11 * S), c, font=cf, fill=WHITE)
        cx += cw + 14 * S
    save(img, "panel_hero.png")


# =========================================================================
# 2. STATS (dark)
# =========================================================================
def panel_stats():
    H = 290 * S
    img = vgrad(W, H, CHAR2, CHAR0).convert("RGBA")
    glow(img, int(W * 0.86), int(H * 0.12), 230 * S, RED_HI, 95)
    d = ImageDraw.Draw(img)
    x = M
    y = 70 * S
    eyebrow(d, x, y, "Built to move the needle", RED_HI)
    y += 50 * S
    stats = [("\u221222%", "fewer wasted miles with optimized routing"),
             ("+15%", "diversion & recovery uplift"),
             ("+10pt", "on-time collection rate"),
             ("100%", "private, on-premise AI \u2014 no data leaves you")]
    col_w = (W - 2 * M) // 4
    nf = font(58 * S, "black")
    lf = font(18 * S, "reg")
    for i, (big, lab) in enumerate(stats):
        cxx = x + i * col_w
        d.text((cxx, y), big, font=nf, fill=WHITE)
        par(d, cxx, y + 78 * S, lab, lf, MUTE, col_w - 24 * S, 26 * S)
    save(img, "panel_stats.png")


# =========================================================================
# 3. FEATURES (light) — intro + 9 cards
# =========================================================================
def panel_features():
    feats = [
        ("01", "AI demand forecasting",
         "Time-series models predict volumes per stream, zone and site so you crew, route and bill ahead of demand \u2014 not behind it."),
        ("02", "Predictive bin fill-levels",
         "Know when each container will be full and service it just in time \u2014 eliminating overflow complaints and half-empty lifts."),
        ("03", "Smart route optimization",
         "A nearest-neighbour sequencer builds the shortest ordered run per zone, with live vehicle & driver assignment and scoring."),
        ("04", "Proof-of-service capture",
         "Every lift recorded with RFID tag, GPS coordinates, timestamp and photo \u2014 irrefutable evidence for disputes and SLAs."),
        ("05", "Weighbridge & recovery",
         "Inbound / outbound tickets feed MRF process batches with mass-balance checks, recovered outputs and live diversion yield."),
        ("06", "Compliance on autopilot",
         "Electronic chain-of-custody manifests, a regulatory waste-code library and a permit register that warns before expiry."),
        ("07", "Live operations cockpit",
         "A branded real-time dashboard with KPI tiles, graph & pivot analysis across every domain \u2014 one pane of glass."),
        ("08", "Anomaly detection & insight",
         "Flags contamination, overweight loads and missed-stop patterns, then explains them in plain language you can act on."),
        ("09", "Global & multi-currency",
         "Commodity pricing and recovered-value figures are multi-currency by default, with regional regulatory profiles built in."),
    ]
    cols, gap = 3, 22 * S
    card_w = (W - 2 * M - (cols - 1) * gap) // cols
    card_h = 300 * S
    rows = 3
    intro_h = 300 * S
    H = intro_h + rows * card_h + (rows - 1) * gap + 80 * S
    img = Image.new("RGB", (W, H), PANEL_LIGHT)
    d = ImageDraw.Draw(img)
    # intro (centered)
    eb = font(15 * S, "black")
    t = "ONE APPLICATION  ·  ZERO ADD-ONS TO CHASE"
    d.text(((W - d.textlength(t, font=eb)) / 2, 78 * S), t, font=eb, fill=RED)
    h2 = font(40 * S, "black")
    t2 = "Everything an operator needs, working as one"
    d.text(((W - d.textlength(t2, font=h2)) / 2, 116 * S), t2, font=h2, fill=INK)
    sf = font(20 * S, "reg")
    sub = ("Collection, routing, recovery, compliance, analytics and AI \u2014 "
           "engineered together, installed once. No integration tax.")
    lines = wrap(d, sub, sf, W - 320 * S)
    sy = 180 * S
    for ln in lines:
        d.text(((W - d.textlength(ln, font=sf)) / 2, sy), ln, font=sf, fill=BODY)
        sy += 30 * S
    # cards
    nf = font(22 * S, "black")
    tf = font(23 * S, "black")
    bf = font(17.5 * S, "reg")
    for i, (num, title, desc) in enumerate(feats):
        r, c = divmod(i, cols)
        cx = M + c * (card_w + gap)
        cy = intro_h + r * (card_h + gap)
        d.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], 18 * S,
                            fill=CARDBG, outline=CARDBORD, width=S)
        # red gradient top accent
        acc = round_grad(card_w - 36 * S, 6 * S, RED, RED_HI, 3 * S)
        img.paste(acc, (cx + 18 * S, cy + 0), acc)
        pad = 30 * S
        # number tile
        tile = round_grad(54 * S, 54 * S, RED, RED_HI, 14 * S)
        img.paste(tile, (cx + pad, cy + pad), tile)
        d = ImageDraw.Draw(img)
        nw = d.textlength(num, font=nf)
        d.text((cx + pad + (54 * S - nw) / 2, cy + pad + 13 * S), num,
               font=nf, fill=WHITE)
        ty = cy + pad + 74 * S
        ty = par(d, cx + pad, ty, title, tf, INK, card_w - 2 * pad, 30 * S)
        ty += 8 * S
        par(d, cx + pad, ty, desc, bf, BODY, card_w - 2 * pad, 27 * S)
    save(img, "panel_features.png")


# =========================================================================
# 4. AI SPOTLIGHT (dark)
# =========================================================================
def panel_ai():
    H = 560 * S
    img = vgrad(W, H, CHAR1, CHAR0).convert("RGBA")
    glow(img, int(W * 0.10), int(H * 0.96), 280 * S, RED, 95)
    d = ImageDraw.Draw(img)
    x = M
    y = 72 * S
    pf = font(15 * S, "black")
    pt = "PRIVACY-FIRST AI"
    pw = int(d.textlength(pt, font=pf))
    d.rounded_rectangle([x, y, x + pw + 36 * S, y + 40 * S], 20 * S, fill=RED)
    d.text((x + 18 * S, y + 10 * S), pt, font=pf, fill=WHITE)
    y += 60 * S
    col_w = int(W * 0.46) - M
    h2 = font(34 * S, "black")
    for ln in wrap(d, "Intelligence that never leaves your server", h2, col_w):
        d.text((x, y), ln, font=h2, fill=WHITE)
        y += 44 * S
    y += 14 * S
    bf = font(20 * S, "reg")
    par(d, x, y,
        "ECOFLOW's forecasting, prediction and scoring run 100% on-premise. "
        "No third-party API, no data egress, no subscription meter. Your "
        "operational data stays yours \u2014 a hard requirement for municipal "
        "and regulated contracts.",
        bf, (199, 204, 208), col_w, 32 * S)
    rows = ["Demand forecasting per stream & zone",
            "Predictive fill-level & service timing",
            "Route efficiency scoring",
            "Anomaly detection & plain-language insights"]
    rf = font(19 * S, "bold")
    rx = M + col_w + 50 * S
    rw = W - rx - M
    ry = 150 * S
    for r in rows:
        d.rounded_rectangle([rx, ry, rx + rw, ry + 76 * S], 14 * S,
                            fill=(34, 42, 45), outline=(58, 68, 72), width=S)
        tri(d, rx + 26 * S, ry + 28 * S, 20 * S, RED_HI)
        d.text((rx + 60 * S, ry + 26 * S), r, font=rf, fill=(232, 236, 238))
        ry += 90 * S
    save(img, "panel_ai.png")


# =========================================================================
# 5. WORKFLOW (light)
# =========================================================================
def panel_workflow():
    H = 420 * S
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    eb = font(15 * S, "black")
    t = "END TO END"
    d.text(((W - d.textlength(t, font=eb)) / 2, 64 * S), t, font=eb, fill=RED)
    h2 = font(36 * S, "black")
    t2 = "One unbroken operational thread"
    d.text(((W - d.textlength(t2, font=h2)) / 2, 100 * S), t2, font=h2, fill=INK)
    steps = [("1", "Plan", "Services & demand"),
             ("2", "Route", "Optimized runs"),
             ("3", "Execute", "Field capture"),
             ("4", "Recover", "Weigh & process"),
             ("5", "Comply", "Manifests & permits"),
             ("6", "Optimize", "AI closes the loop")]
    n = len(steps)
    gap = 18 * S
    cw = (W - 2 * M - (n - 1) * gap) // n
    ch = 170 * S
    cy = 200 * S
    nf = font(20 * S, "black")
    tf = font(22 * S, "black")
    sf = font(15 * S, "reg")
    for i, (num, name, sub) in enumerate(steps):
        cx = M + i * (cw + gap)
        last = i == n - 1
        if last:
            card = round_grad(cw, ch, RED, RED_HI, 16 * S)
            img.paste(card, (cx, cy), card)
            d = ImageDraw.Draw(img)
            circ_fill, num_fill = WHITE, RED
            name_fill, sub_fill = WHITE, (255, 227, 222)
        else:
            d.rounded_rectangle([cx, cy, cx + cw, cy + ch], 16 * S,
                                fill=(250, 251, 251), outline=CARDBORD, width=S)
            circ_fill, num_fill = CHAR1, WHITE
            name_fill, sub_fill = INK, SUB
        # number circle
        cxc = cx + cw // 2
        d.ellipse([cxc - 19 * S, cy + 22 * S, cxc + 19 * S, cy + 60 * S],
                  fill=circ_fill)
        nw = d.textlength(num, font=nf)
        d.text((cxc - nw / 2, cy + 31 * S), num, font=nf, fill=num_fill)
        nmw = d.textlength(name, font=tf)
        d.text((cxc - nmw / 2, cy + 78 * S), name, font=tf, fill=name_fill)
        for j, ln in enumerate(wrap(d, sub, sf, cw - 20 * S)):
            lw = d.textlength(ln, font=sf)
            d.text((cxc - lw / 2, cy + 116 * S + j * 22 * S), ln,
                   font=sf, fill=sub_fill)
    save(img, "panel_workflow.png")


# =========================================================================
# 6. CAPABILITIES (light) — under the hood checklist + regions
# =========================================================================
def panel_capabilities():
    items = [
        ("Waste-stream & material masters", "hazard classes, codes, units, market pricing"),
        ("RFID-tagged bin & container registry", "by type, capacity, status and location"),
        ("Flexible service catalog", "flat, per-lift or per-tonne billing with SLA windows"),
        ("Service orders & events", "tracked from draft to done with full audit chatter"),
        ("Daily route plans", "ordered stops, depot anchoring and distance metrics"),
        ("Fleet & driver assignment", "integrated with native Odoo Fleet"),
        ("Weighbridge tickets", "gross / tare / net with source traceability"),
        ("MRF process batches", "mass-balance validation and recovered-output valuation"),
        ("Electronic manifests", "generator \u2192 transporter \u2192 facility custody"),
        ("Permit register", "automated expiry monitoring & alerts"),
        ("Role-based security", "operator, dispatcher and manager tiers"),
        ("Native Odoo 18 & 19", "modern list / form views, chatter and activities"),
    ]
    regions = ["EU \u00b7 EWC \u00b7 EUR", "UK \u00b7 EA \u00b7 GBP",
               "US \u00b7 EPA/RCRA \u00b7 USD", "Australia \u00b7 NEPM \u00b7 AUD",
               "GCC/MENA \u00b7 AED", "India \u00b7 CPCB/SWM \u00b7 INR",
               "Global \u00b7 ISO \u00b7 USD"]
    col_gap = 60 * S
    col_w = (W - 2 * M - col_gap) // 2
    row_h = 84 * S
    rows = (len(items) + 1) // 2
    list_top = 150 * S
    regions_top = list_top + rows * row_h + 64 * S
    H = regions_top + 230 * S
    img = Image.new("RGB", (W, H), PANEL_LIGHT)
    d = ImageDraw.Draw(img)
    eyebrow(d, M, 70 * S, "Under the hood", RED)
    h2 = font(30 * S, "black")
    d.text((M, 100 * S), "Everything in the box", font=h2, fill=INK)
    lead = font(19 * S, "black")
    body = font(16.5 * S, "reg")
    for i, (title, desc) in enumerate(items):
        c, r = i % 2, i // 2
        cx = M + c * (col_w + col_gap)
        cy = list_top + r * row_h
        check_badge(d, cx + 12 * S, cy + 16 * S, 13 * S)
        d.text((cx + 42 * S, cy), title, font=lead, fill=INK)
        d.text((cx + 42 * S, cy + 30 * S), desc, font=body, fill=SUB)
        d.line([(cx, cy + row_h - 18 * S), (cx + col_w, cy + row_h - 18 * S)],
               fill=CARDBORD, width=S)
    # regions
    eyebrow(d, M, regions_top, "Global by design", RED)
    h3 = font(26 * S, "black")
    d.text((M, regions_top + 30 * S),
           "Pick your region \u2014 framework, units & currency follow",
           font=h3, fill=INK)
    rf = font(17 * S, "bold")
    rx, ry = M, regions_top + 92 * S
    for r in regions:
        rw = int(d.textlength(r, font=rf)) + 52 * S
        if rx + rw > W - M:
            rx = M
            ry += 58 * S
        d.rounded_rectangle([rx, ry, rx + rw, ry + 46 * S], 12 * S,
                            fill=WHITE, outline=(224, 226, 228), width=S)
        d.ellipse([rx + 18 * S, ry + 18 * S, rx + 28 * S, ry + 28 * S], fill=RED)
        d.text((rx + 38 * S, ry + 12 * S), r, font=rf, fill=INK)
        rx += rw + 12 * S
    save(img, "panel_capabilities.png")


# =========================================================================
# 7. PRICING + FOOTER (dark)
# =========================================================================
def panel_pricing():
    H = 540 * S
    img = vgrad(W, H, CHAR2, CHAR0).convert("RGBA")
    glow(img, int(W * 0.5), int(H * 0.5), 320 * S, RED, 55)
    d = ImageDraw.Draw(img)
    x = M
    y = 70 * S
    pf = font(15 * S, "black")
    pt = "ONE LICENCE  ·  EVERYTHING"
    pw = int(d.textlength(pt, font=pf))
    d.rounded_rectangle([x, y, x + pw + 36 * S, y + 40 * S], 20 * S, fill=RED)
    d.text((x + 18 * S, y + 10 * S), pt, font=pf, fill=WHITE)
    y += 62 * S
    col_w = int(W * 0.52) - M
    h2 = font(33 * S, "black")
    for ln in wrap(d, "The whole platform, in a single purchase", h2, col_w):
        d.text((x, y), ln, font=h2, fill=WHITE)
        y += 42 * S
    y += 12 * S
    bf = font(19 * S, "reg")
    par(d, x, y,
        "No tiered editions, no paid add-ons, no per-feature upsell. Install "
        "one app and you have the complete operational stack \u2014 masters, "
        "collection, routing, recovery, compliance, the live cockpit and the "
        "on-premise AI engine \u2014 ready for Odoo 18 & 19.",
        bf, (199, 204, 208), col_w, 31 * S)
    # price card (right) — solid glass tint
    pcw, pch = 360 * S, 250 * S
    px = W - M - pcw
    py = 110 * S
    d.rounded_rectangle([px, py, px + pcw, py + pch], 22 * S,
                        fill=(36, 44, 48), outline=(70, 80, 84), width=S)
    sf = font(14 * S, "black")
    d.text((px + 40 * S, py + 34 * S), "ONE-TIME", font=sf, fill=MUTE)
    pf2 = font(76 * S, "black")
    d.text((px + 36 * S, py + 58 * S), "$299", font=pf2, fill=WHITE)
    lf = font(17 * S, "reg")
    d.text((px + 40 * S, py + 158 * S), "USD  ·  OPL-1 licence",
           font=lf, fill=MUTE)
    cta_f = font(18 * S, "black")
    cta = round_grad(int(d.textlength("Get ECOFLOW", font=cta_f)) + 56 * S,
                     50 * S, RED, RED_HI, 25 * S)
    img.paste(cta, (px + 40 * S, py + 186 * S), cta)
    d = ImageDraw.Draw(img)
    d.text((px + 68 * S, py + 199 * S), "Get ECOFLOW", font=cta_f, fill=WHITE)
    # footer
    fy = H - 116 * S
    d.line([(M, fy), (W - M, fy)], fill=(64, 72, 76), width=S)
    ff = font(17 * S, "bold")
    d.text((M, fy + 32 * S),
           "Designed & maintained by SA Systems  ·  sasystems.solutions",
           font=ff, fill=(214, 219, 221))
    ff2 = font(15 * S, "reg")
    d.text((M, fy + 64 * S),
           "info@sasystems.solutions   ·   Compatible with Odoo 18.0 & 19.0"
           "   ·   Multi-currency   ·   OPL-1",
           font=ff2, fill=MUTE)
    save(img, "panel_pricing.png")


if __name__ == "__main__":
    panel_hero()
    panel_stats()
    panel_features()
    panel_ai()
    panel_workflow()
    panel_capabilities()
    panel_pricing()
    print("all panels done")
