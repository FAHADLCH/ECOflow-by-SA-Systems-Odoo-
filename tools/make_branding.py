"""Generate Sa Systems branded PNG icons and company logo for ECOFLOW."""
import os
import math
import base64
from PIL import Image, ImageDraw, ImageFont

BASE = "addons/ecoflow_dashboard/static"
os.makedirs(BASE + "/description", exist_ok=True)
os.makedirs(BASE + "/src/img", exist_ok=True)

G1 = (22, 163, 74)   # green
G2 = (14, 165, 233)  # blue


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def make_icon(path, size, rounded=True):
    s = size * 4
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))

    grad = Image.new("RGB", (s, s))
    gd = ImageDraw.Draw(grad)
    for y in range(s):
        gd.line([(0, y), (s, y)], fill=lerp(G1, G2, y / s))

    mask = Image.new("L", (s, s), 0)
    md = ImageDraw.Draw(mask)
    r = int(s * 0.22) if rounded else 0
    md.rounded_rectangle([0, 0, s - 1, s - 1], radius=r, fill=255)
    img.paste(grad, (0, 0), mask)

    d = ImageDraw.Draw(img)
    cx, cy = s // 2, s // 2
    rad = int(s * 0.30)
    w = int(s * 0.09)
    d.arc([cx - rad, cy - rad, cx + rad, cy + rad], start=150, end=20,
          fill=(255, 255, 255, 235), width=w)
    d.arc([cx - rad, cy - rad, cx + rad, cy + rad], start=330, end=200,
          fill=(255, 255, 255, 190), width=w)

    def head(angle_deg, col):
        a = math.radians(angle_deg)
        px, py = cx + rad * math.cos(a), cy + rad * math.sin(a)
        sz = int(s * 0.075)
        d.polygon([(px - sz, py - sz), (px + sz, py - sz), (px, py + sz)], fill=col)

    head(20, (255, 255, 255, 235))
    head(200, (255, 255, 255, 190))

    img = img.resize((size, size), Image.LANCZOS)
    img.save(path)
    print("wrote", path, size)


def load_font(path_candidates, sz):
    for p in path_candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()


make_icon(BASE + "/description/icon.png", 140)
make_icon(BASE + "/src/img/icon.png", 140)

# Company logo: mark + wordmark on transparent
W, H, S = 600, 160, 4
img = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
mark = Image.open(BASE + "/description/icon.png").convert("RGBA")
msz = H * S - 28 * S
mark = mark.resize((msz, msz), Image.LANCZOS)
img.alpha_composite(mark, (12 * S, 14 * S))

d = ImageDraw.Draw(img)
bold_paths = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/Library/Fonts/Arial Bold.ttf"]
reg_paths = ["/System/Library/Fonts/Supplemental/Arial.ttf",
             "/Library/Fonts/Arial.ttf"]
big = load_font(bold_paths, 60 * S)
light = load_font(reg_paths, 60 * S)
small = load_font(reg_paths, 17 * S)

x = H * S + 4 * S
d.text((x, 40 * S), "Sa", font=big, fill=(15, 23, 42))
w1 = d.textlength("Sa", font=big)
d.text((x + w1 + 12 * S, 40 * S), "Systems", font=light, fill=(22, 163, 74))
d.text((x + 4 * S, 112 * S),
       "E N V I R O N M E N T A L   O P E R A T I O N S",
       font=small, fill=(100, 116, 139))

img = img.resize((W, H), Image.LANCZOS)
img.save(BASE + "/src/img/sa_systems_logo.png")
print("wrote logo png")

with open(BASE + "/src/img/sa_systems_logo.png", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()
with open("addons/ecoflow_dashboard/static/src/img/logo_b64.txt", "w") as f:
    f.write(b64)
print("logo b64 len", len(b64))
