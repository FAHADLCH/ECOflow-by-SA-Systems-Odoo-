"""Create a transparent-background variant of the Sa Systems logo for use on
light surfaces (nav, footer). We sample the charcoal background colour from the
corners and make near-matching pixels transparent, keeping the red block, the
black 'Systems' box, white text and the white border.
"""
import os
from PIL import Image

WS = "/Users/fahad/Desktop/Odoo Apps/Waste Management System "
SRC = os.path.join(WS, "product", "assets", "sa_systems_logo.png")
OUTS = [
    os.path.join(WS, "product", "assets", "sa_systems_logo_trans.png"),
]

img = Image.open(SRC).convert("RGBA")
px = img.load()
w, h = img.size

# sample background from the four corners (avg)
corners = [px[2, 2], px[w - 3, 2], px[2, h - 3], px[w - 3, h - 3]]
bg = tuple(sum(c[i] for c in corners) // 4 for i in range(3))


def close(a, b, tol):
    return all(abs(a[i] - b[i]) <= tol for i in range(3))


# Flood-fill style: only clear pixels connected to the border that match bg.
# Simpler + safe: clear any pixel close to bg AND darker than the black box.
# The 'Systems' box is near-black (~10,10,10); bg charcoal is ~ (22,27,28).
# Use a tight tolerance so we don't eat the black box.
TOL = 14
from collections import deque

visited = bytearray(w * h)
q = deque()


def idx(x, y):
    return y * w + x


# seed from all border pixels that match bg
for x in range(w):
    for y in (0, h - 1):
        if close(px[x, y], bg, TOL):
            q.append((x, y))
            visited[idx(x, y)] = 1
for y in range(h):
    for x in (0, w - 1):
        if close(px[x, y], bg, TOL) and not visited[idx(x, y)]:
            q.append((x, y))
            visited[idx(x, y)] = 1

while q:
    x, y = q.popleft()
    px[x, y] = (0, 0, 0, 0)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h and not visited[idx(nx, ny)]:
            if close(px[nx, ny], bg, TOL):
                visited[idx(nx, ny)] = 1
                q.append((nx, ny))

# crop to content bbox
bbox = img.getbbox()
if bbox:
    img = img.crop(bbox)

for o in OUTS:
    img.save(o)
print("transparent logo saved:", img.size, "bg sampled:", bg)
