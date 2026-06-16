"""Process the official Sa Systems (SSS) logo into Odoo-ready brand assets.

Source: /Users/fahad/Desktop/SAG/sasystems-logo option 2.jpg  (CMYK)
Outputs:
  - Brand logo (RGB, charcoal bg) at several widths
  - Transparent-charcoal variant for dark hero use
  - App icon cropped from the authentic "sa" red block, rounded
  - Reports sampled brand colors
"""
import os
from PIL import Image, ImageDraw, ImageFilter

SRC = "/Users/fahad/Desktop/SAG/sasystems-logo option 2.jpg"
WS = "/Users/fahad/Desktop/Odoo Apps/Waste Management System "

# destinations
DASH_IMG = os.path.join(WS, "addons", "ecoflow_dashboard", "static", "src", "img")
DASH_DESC = os.path.join(WS, "addons", "ecoflow_dashboard", "static", "description")
PROD_ASSETS = os.path.join(WS, "product", "assets")
for d in (DASH_IMG, DASH_DESC, PROD_ASSETS):
    os.makedirs(d, exist_ok=True)

img = Image.open(SRC)
if img.mode != "RGB":
    img = img.convert("RGB")
W, H = img.size
px = img.load()
print("source", img.size)

# ---- sample brand colors ----
charcoal = px[20, 20]
red = px[int(W * 0.18), int(H * 0.45)]
print("charcoal bg ~", charcoal, " red block ~", red)


def hexc(c):
    return "#%02X%02X%02X" % c[:3]


print("CHARCOAL", hexc(charcoal), "RED", hexc(red))

# ---- detect the red block bounding box (authentic 'sa' mark) ----
xs, ys = [], []
step = 4
for y in range(0, H, step):
    for x in range(0, W, step):
        r, g, b = px[x, y][:3]
        if r > 150 and g < 90 and b < 90:
            xs.append(x)
            ys.append(y)
if xs:
    rx0, rx1 = min(xs), max(xs)
    ry0, ry1 = min(ys), max(ys)
    print("red block bbox", (rx0, ry0, rx1, ry1))
else:
    rx0, ry0, rx1, ry1 = int(W * 0.08), int(H * 0.2), int(W * 0.33), int(H * 0.78)


def rounded(im, radius_frac=0.22):
    s = im.size[0]
    rad = int(s * radius_frac)
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, s, s], radius=rad, fill=255)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    return out


# ---- APP ICON from the authentic red 'sa' block, padded square on red ----
pad = int((ry1 - ry0) * 0.18)
crop = img.crop((max(rx0 - pad, 0), max(ry0 - pad, 0),
                 min(rx1 + pad, W), min(ry1 + pad, H)))
# make square canvas in brand red, center the sa crop
side = max(crop.size)
icon_src = Image.new("RGB", (side, side), red[:3])
icon_src.paste(crop, ((side - crop.size[0]) // 2, (side - crop.size[1]) // 2))
icon_src = icon_src.resize((512, 512), Image.LANCZOS)
icon = rounded(icon_src, 0.22)
icon.save(os.path.join(DASH_DESC, "icon.png"))
icon.resize((140, 140), Image.LANCZOS).save(os.path.join(DASH_IMG, "icon.png"))
print("icon saved")

# ---- FULL LOGO: trim to content, export at standard widths on charcoal ----
# trim uniform charcoal margins
from PIL import ImageChops

bg = Image.new("RGB", img.size, charcoal[:3])
diff = ImageChops.difference(img, bg)
bbox = diff.getbbox()
margin = 60
if bbox:
    bbox = (max(bbox[0] - margin, 0), max(bbox[1] - margin, 0),
            min(bbox[2] + margin, W), min(bbox[3] + margin, H))
    trimmed = img.crop(bbox)
else:
    trimmed = img
print("trimmed", trimmed.size)


def save_w(im, width, path):
    h = int(im.size[1] * (width / im.size[0]))
    im.resize((width, h), Image.LANCZOS).save(path)
    print("saved", path, (width, h))


# charcoal-bg logo (matches brand sheet) for dark heroes / login
save_w(trimmed, 1000, os.path.join(DASH_IMG, "sa_systems_logo.png"))
save_w(trimmed, 1000, os.path.join(PROD_ASSETS, "sa_systems_logo.png"))
save_w(trimmed, 700, os.path.join(DASH_DESC, "logo.png"))

# ---- copy authentic source for reference ----
trimmed.save(os.path.join(PROD_ASSETS, "sa_systems_logo_full.png"))

# write palette file
with open(os.path.join(WS, "tools", "brand_palette.txt"), "w") as f:
    f.write("CHARCOAL %s\nRED %s\n" % (hexc(charcoal), hexc(red)))
print("DONE. palette:", hexc(charcoal), hexc(red))
