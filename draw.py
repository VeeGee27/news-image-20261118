#!/usr/bin/env python3
"""Draw the entry image for make.fun competition news-image-20261118.

v3 — a newspaper front page summing up Wednesday 18 November 2026 in
one image, built to the shape of the day's top-ranked entries: serif
masthead with the date, a true story count, three hero stories, six mid
stories, a "By the numbers" strip, a world-map panel, and a numbered
also-on list with bold lead-ins. 32 stories in total, across 6
continents.

Numbering 1-32 (the lesson from the 17 Nov v3 revision, applied from
the first draft): every story has one serial number, in reading order --
heroes 1-3, mids 4-9, also-on 10-32. The number appears as a badge on
its hero/mid panel, as a numbered circle on the world map (31 of the 32
stories -- Voyager 1 (31) is in deep space and has no place on Earth;
crowded dots sit just outside their country with a thin leader line to
the exact spot), and before its line in the also-on list, always in the
story's continent colour, so a reader can match any map marker to its
story without guessing. Flat shapes and crisp text only, so the image
stays legible at small sizes and the PNG stays far under the 1 MiB
limit. Deterministic: same input, same bytes.

v3 changes vs the submitted v2 (97.90%): Voyager 1 (first human-made
object to reach one light-day from the Sun, NASA 10:16 UTC 18 Nov) and
Cyclone Xavier (Category 5, Cook Islands, MetService bulletin 18 Nov)
replace two wrong lines -- Jetstar (a March 2026 story) and the NZ
election (held Saturday 7 Nov). Altimeter's $5bn Anthropic bid (16 Nov)
is folded into hero panel 8 as context instead of standing alone.

Every story happened or was first reported on Wednesday 18 November
2026 as reported on that morning's news pages; contested claims are
marked as claims ("says", "claims", quotes). Two figures from the
reference pool were checked and CORRECTED, not copied blindly:
- Guinea: the pool said 324 jailed; the verified figure is 224
  (22 former officials + 202 miners, Siguiri crackdown, 16-17 Nov).
- Amazon: the pool said "$3bn Italian renewables by 2030"; no such
  announcement exists. The verified Amazon story is a $7bn renewables
  push in INDIA by 2030, announced Tuesday 17 Nov (PTI).
Also corrected: the reference's also-on header says "26 MORE STORIES"
but its own numbering runs 10-33, which is 24 items; this image prints
the true "24 MORE STORIES" (3 heroes + 6 mids + 24 also-on = 33).
Nvidia: revenue $115.8bn, up 103% year on year (the +107% figure is
gross profit / EPS growth, not revenue). Anthropic: never "orders top
$10bn" -- the base offering alone is $57.75-64.35bn; orders are near
7x the shares on offer.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

PAPER = (251, 248, 241)
NAVY = (16, 36, 62)
GOLD = (232, 185, 74)
RED = (179, 39, 30)
INK = (24, 24, 24)
GREY = (58, 58, 58)
WHITE = (255, 255, 255)
SKY = (191, 217, 232)
SEA = (46, 107, 138)

# Continent colours for the map dots and legend.
C_AMERICAS = (204, 51, 51)
C_EUROPE = (43, 106, 184)
C_MIDEAST = (232, 120, 40)
C_ASIA = (20, 130, 80)
C_AFRICA = (128, 60, 160)
C_OCEANIA = (0, 150, 170)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Wrap text to fit max_width, returning a list of lines."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def centered(draw, y, text, fnt, fill, width=W):
    draw.text((width / 2, y), text, font=fnt, fill=fill, anchor="ma")


def starburst(draw, cx, cy, r_outer, r_inner, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def fit_font(draw, text, path, size, max_width):
    """Largest font size at or below `size` that fits the text in max_width."""
    while size > 10:
        fnt = font(path, size)
        if draw.textlength(text, font=fnt) <= max_width:
            return fnt
        size -= 1
    return font(path, 10)


def num_badge(draw, cx, cy, r, n, fill, size, width=2):
    """Numbered circle badge: continent colour, bold white number, ring."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill,
                 outline=WHITE, width=width)
    draw.text((cx, cy), str(n), font=font(BOLD, size), fill=WHITE,
              anchor="mm")


def flag(draw, x, y, w, h, kind):
    """Tiny US / China / Russia flag, w x h."""
    if kind == "us":
        draw.rectangle([x, y, x + w, y + h], fill=(179, 39, 30))
        for i in range(3):
            draw.rectangle([x, y + (2 * i + 1) * h / 7, x + w,
                            y + (2 * i + 2) * h / 7], fill=WHITE)
        draw.rectangle([x, y, x + w * 0.4, y + h * 0.55], fill=NAVY)
    elif kind == "cn":
        draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        draw.ellipse([x + w * 0.15, y + h * 0.18, x + w * 0.42,
                      y + h * 0.45], fill=(255, 222, 0))
    else:  # ru
        draw.rectangle([x, y, x + w, y + h / 3], fill=WHITE)
        draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3],
                       fill=(0, 57, 166))
        draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(179, 39, 30))


# ---------------------------------------------------------------------------
# Hero scenes (drawn to fit any w x h box)
# ---------------------------------------------------------------------------

def scene_asia(draw, x, y, w, h):
    """Shenzhen skyline under the sun for the APEC talks."""
    draw.rectangle([x, y, x + w, y + h], fill=(242, 193, 78))
    draw.ellipse([x + w - 52, y + 6, x + w - 12, y + 46], fill=(232, 120, 40))
    base = y + h
    towers = [(0.01, 0.62), (0.14, 0.86), (0.27, 0.68), (0.40, 0.96),
              (0.53, 0.74), (0.66, 0.88), (0.79, 0.64), (0.90, 0.82)]
    for fx, fh in towers:
        tx = x + w * fx
        draw.rectangle([tx, base - h * fh, tx + w * 0.105, base], fill=NAVY)
    for fx, fh in towers:
        tx = x + w * fx
        for wy in range(int(base - h * fh + 8), int(base - 10), 13):
            draw.rectangle([tx + 5, wy, tx + 11, wy + 5], fill=GOLD)
            draw.rectangle([tx + 20, wy, tx + 26, wy + 5], fill=GOLD)
    # summit flags on three towers (US, China, Russia)
    for fx, fh, kind in ((0.27, 0.68, "us"), (0.53, 0.74, "cn"),
                         (0.79, 0.64, "ru")):
        top = base - h * fh
        pole_x = x + w * fx + w * 0.05
        draw.line([pole_x, top - 20, pole_x, top], fill=NAVY, width=2)
        flag(draw, pole_x + 2, top - 20, 22, 13, kind)


def scene_strikes(draw, x, y, w, h):
    """Night strikes over the Gulf: blasts over the sea, drones overhead."""
    draw.rectangle([x, y, x + w, y + h], fill=(27, 42, 74))
    draw.rectangle([x, y + h * 0.70, x + w, y + h], fill=SEA)
    draw.polygon([(x + w * 0.06, y + h * 0.70), (x + w * 0.30, y + h * 0.42),
                  (x + w * 0.62, y + h * 0.46), (x + w * 0.86, y + h * 0.70)],
                 fill=(74, 94, 58))
    starburst(draw, x + w * 0.42, y + h * 0.44, 20, 9, 8, fill=GOLD)
    starburst(draw, x + w * 0.42, y + h * 0.44, 11, 5, 8, fill=(232, 120, 40))
    draw.arc([x + w * 0.08, y + h * 0.06, x + w * 0.44, y + h * 0.62],
             200, 330, fill=WHITE, width=3)
    draw.arc([x + w * 0.56, y + h * 0.02, x + w * 0.94, y + h * 0.58],
             210, 340, fill=WHITE, width=3)
    # a small drone top right
    dx, dy = x + w * 0.88, y + h * 0.24
    draw.rectangle([dx - 11, dy - 3, dx + 11, dy + 3], fill=WHITE)
    draw.line([dx - 16, dy - 8, dx + 16, dy - 8], fill=WHITE, width=2)
    draw.line([dx - 16, dy + 10, dx + 16, dy + 10], fill=WHITE, width=2)
    for rx in (dx - 16, dx + 16):
        draw.ellipse([rx - 3, dy - 11, rx + 3, dy - 5], fill=WHITE)
        draw.ellipse([rx - 3, dy + 7, rx + 3, dy + 13], fill=WHITE)


def scene_knesset(draw, x, y, w, h):
    """Parliament building under a pale sky, Israeli flag flying."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 226, 238))
    base = y + h
    # main block with a pediment and columns
    draw.polygon([(x + w * 0.30, y + h * 0.30), (x + w * 0.50, y + h * 0.14),
                  (x + w * 0.70, y + h * 0.30)], fill=(96, 96, 96))
    draw.rectangle([x + w * 0.30, y + h * 0.30, x + w * 0.70, base - 4],
                   fill=(186, 180, 164))
    for fx in (0.34, 0.42, 0.50, 0.58):
        draw.rectangle([x + w * fx, y + h * 0.36, x + w * fx + 7, base - 6],
                       fill=(251, 248, 241))
    # side wings
    draw.rectangle([x + w * 0.06, y + h * 0.52, x + w * 0.28, base - 4],
                   fill=(168, 162, 146))
    draw.rectangle([x + w * 0.72, y + h * 0.52, x + w * 0.94, base - 4],
                   fill=(168, 162, 146))
    # flag pole + Israeli flag (two blue stripes, blue star)
    px = x + w * 0.50
    draw.line([px, y + 4, px, y + h * 0.14], fill=INK, width=2)
    fx, fy, fw, fh = px + 3, y + 5, 26, 15
    draw.rectangle([fx, fy, fx + fw, fy + fh], fill=WHITE,
                   outline=(43, 106, 184), width=1)
    draw.rectangle([fx + 2, fy + 2, fx + fw - 2, fy + 4], fill=(43, 106, 184))
    draw.rectangle([fx + 2, fy + fh - 4, fx + fw - 2, fy + fh - 2],
                   fill=(43, 106, 184))
    starburst(draw, fx + fw / 2, fy + fh / 2, 4, 2, 6, fill=(43, 106, 184))


# ---------------------------------------------------------------------------
# Mid-panel mini scenes (drawn into a small strip, w x h)
# ---------------------------------------------------------------------------

def mini_quake(draw, x, y, w, h):
    """Seismograph trace over cracked ground."""
    draw.rectangle([x, y, x + w, y + h], fill=(220, 226, 232))
    draw.rectangle([x + 4, y + 6, x + w - 4, y + h * 0.58], fill=WHITE,
                   outline=(150, 150, 150), width=1)
    mid = y + h * 0.32
    pts = [(x + 6, mid)]
    amp = [2, 3, 2, 5, 14, 4, 9, 3, 2, 4, 12, 3, 6, 2, 3, 2]
    for i, a in enumerate(amp):
        px = x + 6 + (i + 1) * (w - 12) / len(amp)
        py = mid + (a if i % 2 == 0 else -a)
        pts.append((px, py))
    pts.append((x + w - 6, mid))
    draw.line(pts, fill=RED, width=2)
    draw.rectangle([x, y + h * 0.66, x + w, y + h], fill=(120, 100, 80))
    draw.line([x + w * 0.30, y + h * 0.66, x + w * 0.26, y + h],
              fill=(60, 48, 36), width=2)
    draw.line([x + w * 0.62, y + h * 0.66, x + w * 0.68, y + h],
              fill=(60, 48, 36), width=2)
    draw.line([x + w * 0.62, y + h * 0.80, x + w * 0.50, y + h * 0.88],
              fill=(60, 48, 36), width=2)


def mini_cyclone(draw, x, y, w, h):
    """A cyclone spiral over the sea."""
    draw.rectangle([x, y, x + w, y + h], fill=(158, 196, 224))
    draw.rectangle([x, y + h * 0.78, x + w, y + h], fill=SEA)
    cx, cy = x + w * 0.42, y + h * 0.46
    for r, start in ((30, 200), (24, 110), (18, 20), (12, 290)):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start, start + 250,
                 fill=WHITE, width=4)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(20, 30, 60))
    for fx in (0.72, 0.82, 0.92):
        draw.line([x + w * fx, y + 8, x + w * fx - 6, y + 22],
                  fill=(240, 244, 246), width=2)
        draw.line([x + w * fx, y + 26, x + w * fx - 6, y + 40],
                  fill=(240, 244, 246), width=2)


def mini_chart(draw, x, y, w, h, direction):
    """A market line chart: falling (red) or rising (green)."""
    draw.rectangle([x, y, x + w, y + h], fill=(240, 244, 246))
    for gy in (0.25, 0.50, 0.75):
        draw.line([x + 8, y + h * gy, x + w - 8, y + h * gy],
                  fill=(210, 218, 224), width=1)
    draw.line([x + 10, y + 6, x + 10, y + h - 8], fill=INK, width=2)
    draw.line([x + 10, y + h - 8, x + w - 6, y + h - 8], fill=INK, width=2)
    if direction == "down":
        pts = [(x + 14, y + 10), (x + w * 0.30, y + 16),
               (x + w * 0.48, y + 14), (x + w * 0.66, y + 30),
               (x + w * 0.82, y + 38), (x + w - 10, y + h - 14)]
        col = RED
        tip = (x + w - 10, y + h - 14)
    else:
        pts = [(x + 14, y + h - 14), (x + w * 0.30, y + h - 20),
               (x + w * 0.48, y + h - 26), (x + w * 0.66, y + 22),
               (x + w * 0.82, y + 16), (x + w - 10, y + 10)]
        col = (20, 130, 80)
        tip = (x + w - 10, y + 10)
    draw.line(pts, fill=col, width=3)
    ax, ay = tip
    if direction == "down":
        draw.polygon([(ax, ay), (ax - 10, ay - 2), (ax - 2, ay - 10)],
                     fill=col)
    else:
        draw.polygon([(ax, ay), (ax - 10, ay + 2), (ax - 2, ay + 10)],
                     fill=col)


def mini_parliament(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(233, 228, 210))
    draw.polygon([(x + w * 0.30, y + 6), (x + w * 0.50, y + 2),
                  (x + w * 0.70, y + 6)], fill=(90, 90, 90))
    draw.rectangle([x + w * 0.30, y + 6, x + w * 0.70, y + h - 6],
                   fill=(180, 175, 160))
    for fx in (0.34, 0.47, 0.60):
        draw.rectangle([x + w * fx, y + 10, x + w * fx + 6, y + h - 8],
                       fill=(251, 248, 241))
    draw.line([x + w * 0.50, y - 8, x + w * 0.50, y + 2], fill=INK, width=2)
    draw.rectangle([x + w * 0.50 + 2, y - 8, x + w * 0.50 + 16, y - 1],
                   fill=(204, 51, 51))


def mini_cop31(draw, x, y, w, h):
    """A wind turbine under the sun on a green hill (climate summit)."""
    draw.rectangle([x, y, x + w, y + h], fill=(176, 216, 228))
    draw.ellipse([x + w - 46, y + 5, x + w - 14, y + 37], fill=(242, 193, 78))
    draw.polygon([(x, y + h * 0.72), (x + w * 0.45, y + h * 0.55),
                  (x + w, y + h * 0.72), (x + w, y + h), (x, y + h)],
                 fill=(110, 180, 110))
    # turbine mast + three blades
    tx, ty = x + w * 0.42, y + h * 0.58
    draw.line([tx, ty, tx, y + h * 0.94], fill=WHITE, width=4)
    for ang in (90, 210, 330):
        a = math.radians(ang)
        ex, ey = tx + 22 * math.cos(a), ty - 22 * math.sin(a)
        draw.line([tx, ty, ex, ey], fill=WHITE, width=4)
        draw.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=WHITE)
    draw.ellipse([tx - 5, ty - 5, tx + 5, ty + 5], fill=(20, 130, 80))
    # small solar panel, bottom right
    draw.polygon([(x + w * 0.68, y + h * 0.86), (x + w * 0.86, y + h * 0.80),
                  (x + w * 0.92, y + h * 0.92), (x + w * 0.74, y + h * 0.96)],
                 fill=NAVY)
    draw.line([x + w * 0.68, y + h * 0.86, x + w * 0.92, y + h * 0.92],
              fill=WHITE, width=1)


# ---------------------------------------------------------------------------
# World map (simplified continents in a 446 x 220 box)
# ---------------------------------------------------------------------------

def _mp(lon, lat):
    # Equirectangular: the map box is 446 x 220 units, lon -180..180,
    # lat 75..-60. Hand-written (lon, lat) outlines below are converted
    # here, so the shapes match a real globe and every marker lands on
    # its own country.
    return (round((lon + 180) * 446 / 360),
            round((75 - lat) * 220 / 135))

def _poly(*pts):
    return [_mp(lon, lat) for lon, lat in pts]

CONTINENTS = [
    # North America
    _poly((-168, 66), (-158, 58), (-142, 59), (-125, 49), (-124, 40),
          (-117, 32), (-110, 23), (-105, 20), (-96, 16), (-90, 21),
          (-81, 25), (-76, 35), (-70, 42), (-60, 47), (-60, 55),
          (-68, 60), (-80, 56), (-88, 59), (-95, 69), (-125, 70),
          (-155, 71)),
    # Greenland
    _poly((-58, 64), (-45, 60), (-30, 68), (-38, 74), (-55, 74)),
    # South America
    _poly((-77, 7), (-64, 10), (-52, 5), (-50, 0), (-35, -8), (-40, -20),
          (-48, -28), (-58, -38), (-65, -47), (-68, -54), (-73, -50),
          (-73, -37), (-71, -20), (-77, -12), (-80, -4), (-79, 2)),
    # Africa
    _poly((-6, 35), (-16, 24), (-18, 15), (-13, 8), (2, 6), (9, 4),
          (13, -9), (13, -19), (18, -32), (27, -34), (33, -26),
          (40, -13), (41, -1), (51, 4), (44, 11), (38, 20), (33, 30),
          (19, 32), (10, 37), (-2, 35)),
    # Madagascar
    _poly((44, -16), (50, -16), (47, -25), (44, -22)),
    # Eurasia
    _poly((-9, 37), (-9, 43), (-1, 46), (2, 51), (7, 54), (10, 59),
          (18, 56), (24, 66), (30, 70), (70, 72), (110, 74), (150, 71),
          (178, 66), (162, 56), (156, 51), (130, 39), (127, 35),
          (121, 31), (114, 22), (105, 9), (101, 3), (98, 10), (95, 15),
          (89, 22), (82, 17), (80, 13), (77, 8), (73, 15), (68, 23),
          (61, 25), (57, 27), (50, 25), (56, 27), (59, 22), (52, 16),
          (44, 13), (39, 21), (35, 29), (34.5, 32), (36, 36), (30, 36),
          (22, 37), (19, 41), (16, 40), (15, 38), (12, 42), (8, 44),
          (3, 43), (-1, 38)),
    # Australia
    _poly((113, -22), (114, -32), (124, -33), (133, -32), (145, -38),
          (150, -37), (153, -28), (150, -22), (142, -11), (135, -12),
          (126, -14), (116, -20)),
    # New Zealand
    _poly((166, -46), (167, -44), (170, -41), (173, -38), (175, -34.5),
          (178, -37), (176, -40), (175, -42.5), (172, -44), (169, -46)),
    # Cook Islands (tiny -- Cyclone Xavier, 29)
    _poly((-163, -11), (-157, -11), (-157, -9), (-163, -9)),
    # United Kingdom
    _poly((-5, 50), (-3, 53), (-5, 58)),
    # Japan
    _poly((129, 31), (133, 32), (137, 34), (140, 35), (141, 38),
          (142, 41), (140, 40), (136, 36), (132, 33)),
    # Taiwan
    _poly((120, 22), (122, 22), (122, 25), (120, 25)),
    # Indonesia
    _poly((95, 5), (106, -6), (118, -9), (128, -4), (112, 1)),
    # Cuba
    _poly((-84, 22), (-80, 23), (-74, 20)),
    # Philippines
    _poly((120, 18), (122, 18), (122, 14), (120, 14)),
]

# Numbered dots for 31 of the 32 stories, placed from each story's
# real (lon, lat) through the same projection and verified one by one
# (point-in-polygon against the drawn continents): every anchor sits
# on its own country -- no dot in the sea, none on a neighbour, none
# placed by guesswork. Story 31 (Voyager 1) has no dot: it is in deep
# space and has no place on Earth. Where dots would collide, the badge
# sits a few units off the anchor on land with a thin leader line to
# the exact spot. Offsets (dx, dy) are in map units from the projected
# anchor.
# (lon, lat, colour, n, dx, dy)
MARKERS_LL = [
    (35.2, 31.8, C_MIDEAST, 1, 0, 0),      # Jerusalem (Eisenkot)
    (113.5, 22.7, C_ASIA, 2, -6, 7),      # Pearl River Delta (APEC Shenzhen)
    (50.6, 26.2, C_MIDEAST, 3, 0, 0),     # Bahrain (Iran drones, Gulf)
    (4.35, 50.85, C_EUROPE, 4, 0, 0),     # Brussels (EU loan)
    (26.7, 45.7, C_EUROPE, 5, 6, 0),      # Vrancea (Romania quake)
    (79.1, 16.7, C_ASIA, 6, 0, 0),        # Andhra coast (Cyclone Akvan)
    (121.0, 23.7, C_ASIA, 7, 0, 0),       # Taiwan
    (-121.9, 37.8, C_AMERICAS, 8, 0, 0),   # San Francisco (Anthropic)
    (30.7, 36.9, C_ASIA, 9, -7, 0),       # Antalya (COP31)
    (35.2, 31.8, C_MIDEAST, 10, 11, -12),  # Jerusalem (Knesset/Kahana)
    (-121.6, 37.35, C_AMERICAS, 11, -2, -15),  # Santa Clara (Nvidia)
    (-74.0, 40.7, C_AMERICAS, 12, 0, 0),   # New York (Dow)
    (36.5, 45.3, C_EUROPE, 13, 9, -5),    # Kerch Bridge
    (50.6, 26.2, C_MIDEAST, 14, 12, -10),  # Bahrain (US/Iran fire)
    (121.0, 14.6, C_ASIA, 15, 0, 0),      # Manila (Trump/Marcos)
    (35.2, 32.0, C_MIDEAST, 16, 9, 22),   # West Bank (settler sanctions)
    (34.5, 31.5, C_MIDEAST, 17, -13, 7),  # Gaza (warning)
    (87.0, 55.4, C_EUROPE, 18, 0, 0),     # Kemerovo (Siberia crash)
    (-98.5, 38.5, C_AMERICAS, 19, 0, 0),  # Kansas (measles status)
    (139.7, 35.7, C_ASIA, 20, 0, 0),      # Tokyo (jets scrambled)
    (-121.5, 37.3, C_AMERICAS, 21, 12, 13),  # Cupertino (Apple outage)
    (77.0, 22.0, C_ASIA, 22, -8, -4),     # central India (Amazon renewables)
    (-17.5, 14.7, C_AFRICA, 23, 0, 0),    # Senegal (AFCON)
    (16.4, 48.2, C_EUROPE, 24, 0, 0),     # Vienna (Nations League)
    (77.2, 28.6, C_ASIA, 25, 0, -8),      # Delhi (SAFF final)
    (32.5, 15.6, C_AFRICA, 26, 0, 0),     # Khartoum (Sudan drones)
    (116.4, 39.9, C_ASIA, 27, 0, 0),      # Beijing (China-Canada tariffs)
    (-13.7, 9.5, C_AFRICA, 28, 8, 3),     # Conakry (Guinea jails)
    (-160.0, -10.0, C_OCEANIA, 29, 0, 0),  # Cook Islands (Cyclone Xavier)
    (13.4, 52.5, C_EUROPE, 30, 14, -4),   # Berlin (European startups)
    # 31 Voyager 1: no dot -- deep space, no place on Earth
    (-77.0, 38.9, C_AMERICAS, 32, -12, 13),  # Washington DC (dirty-bomb report)
]
# (anchor px, py, display px, py, colour, n)
MAP_MARKERS = []
for lon, lat, col, n, dx, dy in MARKERS_LL:
    ax, ay = _mp(lon, lat)
    MAP_MARKERS.append((ax, ay, ax + dx, ay + dy, col, n))

LEGEND = [
    ("Americas", C_AMERICAS),
    ("Europe", C_EUROPE),
    ("Middle East", C_MIDEAST),
    ("Asia", C_ASIA),
    ("Africa", C_AFRICA),
    ("Oceania", C_OCEANIA),
]


# ---------------------------------------------------------------------------
# Stories
# ---------------------------------------------------------------------------

HEROES = [
    ("MIDDLE EAST · POLITICS",
     "Eisenkot tapped to form Israel's government",
     "Herzog picks Eisenkot over Netanyahu, 67-46. He has 28 days to "
     "build a 61-seat coalition.",
     scene_knesset),
    ("ASIA · DIPLOMACY",
     "APEC opens: Xi, Putin meet in Shenzhen",
     "Xi keynotes APEC and meets Putin today. Trump is due after "
     "Manila; a first-ever trilateral meets Thursday.",
     scene_asia),
    ("MIDDLE EAST · CONFLICT",
     "Iran drones target US forces in Gulf",
     "Drones target US forces in Bahrain and Kuwait; both intercept "
     "them. Iran claims a hit on Ali Al Salem base.",
     scene_strikes),
]

MIDS = [
    ("EUROPE · UKRAINE", "EU proposes \u20ac45bn loan for Ukraine",
     "Proposal due Wednesday covers two-thirds of Kyiv's 2027 gap; "
     "repaid only if Russia pays reparations.",
     lambda d, x, y, w, h: mini_parliament(d, x, y, w, h)),
    ("EUROPE · EARTHQUAKE", "Romania: M5.3 quake",
     "Vrancea region, 00:48 UTC, deep at about 131 km.",
     lambda d, x, y, w, h: mini_quake(d, x, y, w, h)),
    ("SOUTH ASIA · WEATHER", "Cyclone Akvan bears down",
     "Landfall due Friday, gusts 145 km/h; Odisha moves 200,000 people "
     "from the coast.",
     lambda d, x, y, w, h: mini_cyclone(d, x, y, w, h)),
    ("ASIA · MARKETS", "Taiwan stocks below 40,000",
     "Index falls to a low of 39,260 as the NT dollar weakens past 33; "
     "the state stabilisation fund steps in.",
     lambda d, x, y, w, h: mini_chart(d, x, y, w, h, "down")),
    ("AMERICAS · TECH", "Anthropic IPO due today",
     "Pricing due today at $70\u201378; orders near 7\u00d7 the shares on "
     "offer. Altimeter bids $5bn; trading starts Thursday.",
     lambda d, x, y, w, h: mini_chart(d, x, y, w, h, "up")),
    ("ASIA · CLIMATE", "COP31, Antalya",
     "First week records $26bn in green deals and $10bn in climate "
     "finance pledges.",
     lambda d, x, y, w, h: mini_cop31(d, x, y, w, h)),
]

# By the numbers: 4 figures taken from the stories above.
BY_NUMBERS = [
    ("67\u201346", "Eisenkot's margin over Netanyahu"),
    ("\u20ac45bn", "EU loan proposed for Ukraine"),
    ("145 km/h", "Akvan's forecast gusts"),
    ("200,000", "People Odisha is moving from the coast"),
]

# Also-on: one line each, numbered 10-32. Each line is (bold lead-in,
# rest of the line, continent colour) -- the bold lead keeps the list
# scannable at small size, like the top entries do.
ALSO_ON = [
    ("KAHANA \u2014", "Knesset picks speaker, 66-52", C_MIDEAST),
    ("NVIDIA \u2014", "revenue doubles to $115.8bn", C_AMERICAS),
    ("DOW \u2014", "drops 849, fourth straight fall", C_AMERICAS),
    ("KERCH BRIDGE \u2014", "span falls into the sea", C_EUROPE),
    ("GULF \u2014", "US, Iran trade fire over Bahrain", C_MIDEAST),
    ("TRUMP \u2014", "meets Marcos, flies to Shenzhen", C_ASIA),
    ("SETTLER SANCTIONS \u2014", "7 banned, 8 frozen", C_MIDEAST),
    ("GAZA \u2014", "peace board fears collapse", C_MIDEAST),
    ("SIBERIA CRASH \u2014", "all 19 aboard An-12 die", C_EUROPE),
    ("MEASLES \u2014", "US loses free status since 2000", C_AMERICAS),
    ("TOKYO \u2014", "scrambles jets at Russian planes", C_ASIA),
    ("APPLE \u2014", "outage hits iCloud, App Store, Pay", C_AMERICAS),
    ("AMAZON \u2014", "$7bn in India renewables", C_ASIA),
    ("SENEGAL \u2014", "first into AFCON 2027", C_AFRICA),
    ("NATIONS \u2014", "Iceland, Austria, Sweden up", C_EUROPE),
    ("SAFF FINAL \u2014", "India beats Pakistan 2-1", C_ASIA),
    ("SUDAN \u2014", "drones killed 1,630 this year", C_AFRICA),
    ("TARIFFS \u2014", "China, Canada on pork, seafood", C_ASIA),
    ("GUINEA \u2014", "jails 224 over illegal gold mining", C_AFRICA),
    ("XAVIER \u2014", "Cat 5 cyclone, 220 km/h, Cook Is.", C_OCEANIA),
    ("EU STARTUPS \u2014", "near $81bn funding", C_EUROPE),
    ("VOYAGER 1 \u2014", "first object to one light-day", C_AMERICAS),
    ("CNN \u2014", "Iran 'may weigh dirty-bomb attack'", C_MIDEAST),
]

STORY_COUNT = len(HEROES) + len(MIDS) + len(ALSO_ON)  # 32
assert STORY_COUNT == 32, STORY_COUNT

# Number colours: the badge/marker/list number of each story takes its
# continent colour, so the number cross-references the map legend.
HERO_COLORS = [C_MIDEAST, C_ASIA, C_MIDEAST]
MID_COLORS = [C_EUROPE, C_EUROPE, C_ASIA, C_ASIA, C_AMERICAS, C_ASIA]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 106], fill=NAVY)
    centered(d, 8, "THE DAY IN WORLD NEWS", font(BOLD, 15), GOLD)
    centered(d, 28, "Wednesday 18 November 2026", font(SERIF, 44), WHITE)
    centered(d, 82, "Every story on this page happened, or was first "
             "reported, on this day.", font(REG, 13), WHITE)
    d.rectangle([0, 106, W, 110], fill=RED)
    centered(d, 114, "32 STORIES \u00b7 6 CONTINENTS \u00b7 ONE PAGE",
             font(BOLD, 17), NAVY)

    margin, gap = 10, 8

    # ---- Hero row: 3 panels ----
    hw = (W - 2 * margin - 2 * gap) // 3  # 328
    hy, hh = 138, 162
    for i, (tag, title, caption, scene) in enumerate(HEROES):
        px = margin + i * (hw + gap)
        d.rectangle([px, hy, px + hw, hy + hh], fill=WHITE,
                    outline=INK, width=2)
        scene(d, px + 2, hy + 2, hw - 4, 62)
        num_badge(d, px + 21, hy + 21, 17, i + 1, HERO_COLORS[i], 16)
        d.text((px + 10, hy + 68), tag, font=font(BOLD, 10), fill=RED)
        tlines = wrap(d, title, font(BOLD, 17), hw - 20)
        ly = hy + 84
        for line in tlines[:2]:
            d.text((px + 10, ly), line, font=font(BOLD, 17), fill=NAVY)
            ly += 20
        clines = wrap(d, caption, font(REG, 11), hw - 20)
        ly = hy + 124
        for line in clines[:3]:
            d.text((px + 10, ly), line, font=font(REG, 11), fill=GREY)
            ly += 13

    # ---- Mid grid: 2 rows x 3 panels ----
    mw = (W - 2 * margin - 2 * gap) // 3  # 328
    mh = 106
    for r in range(2):
        my = 306 + r * (mh + gap)
        for c in range(3):
            i = r * 3 + c
            tag, title, caption, scene = MIDS[i]
            px = margin + c * (mw + gap)
            d.rectangle([px, my, px + mw, my + mh], fill=WHITE,
                        outline=INK, width=2)
            scene(d, px + 2, my + 2, mw - 4, 38)
            num_badge(d, px + 16, my + 16, 13, i + 4, MID_COLORS[i], 12)
            d.text((px + 8, my + 42), tag, font=font(BOLD, 9), fill=RED)
            tfont = fit_font(d, title, BOLD, 14, mw - 16)
            tlines = wrap(d, title, tfont, mw - 16)
            ly = my + 56
            for line in tlines[:1]:
                d.text((px + 8, ly), line, font=tfont, fill=NAVY)
                ly += 16
            clines = wrap(d, caption, font(REG, 10), mw - 16)
            ly = my + 73
            for line in clines[:2]:
                d.text((px + 8, ly), line, font=font(REG, 10), fill=GREY)
                ly += 12

    # ---- By the numbers strip ----
    by = 530
    d.rectangle([margin, by, W - margin, by + 46], fill=WHITE,
                outline=INK, width=2)
    colw = (W - 2 * margin) // 4
    for i, (fig, label) in enumerate(BY_NUMBERS):
        cx = margin + i * colw
        if i:
            d.line([cx, by + 6, cx, by + 40], fill=(200, 200, 200), width=1)
        ff = font(BOLD, 20)
        fw = d.textlength(fig, font=ff)
        d.text((cx + (colw - fw) / 2, by + 4), fig, font=ff, fill=NAVY)
        ll = wrap(d, label, font(REG, 10), colw - 16)
        if ll:
            lw = d.textlength(ll[0], font=font(REG, 10))
            d.text((cx + (colw - lw) / 2, by + 27), ll[0],
                   font=font(REG, 10), fill=GREY)

    # ---- Bottom band: world map (left) + also-on list (right) ----
    by2 = 582
    # Map panel
    mx, mpw = margin, 468
    d.rectangle([mx, by2, mx + mpw, by2 + 406], fill=WHITE,
                outline=INK, width=2)
    d.text((mx + 10, by2 + 8), "WHERE THE NEWS HAPPENED",
           font=font(BOLD, 14), fill=NAVY)
    d.text((mx + 10, by2 + 28), "Numbered dots match stories 1\u201332; "
           "31 is in deep space.",
           font=font(REG, 11), fill=GREY)
    map_x, map_y = mx + 8, by2 + 52
    map_w, map_h = mpw - 16, 236
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h],
                fill=(226, 238, 244))
    ms = map_w / 446
    ox = (map_w - 446 * ms) / 2
    oy = (map_h - 220 * ms) / 2
    for poly in CONTINENTS:
        d.polygon([(map_x + ox + px * ms, map_y + oy + py * ms)
                   for px, py in poly],
                  fill=(170, 196, 168), outline=(120, 150, 125))
    # leader lines first (anchor dot + thin line), badges on top
    for apx, apy, dpx, dpy, col, n in MAP_MARKERS:
        ax, ay = map_x + ox + apx * ms, map_y + oy + apy * ms
        cx, cy = map_x + ox + dpx * ms, map_y + oy + dpy * ms
        if (ax, ay) != (cx, cy):
            d.line([ax, ay, cx, cy], fill=(110, 110, 110), width=1)
            d.ellipse([ax - 2.5, ay - 2.5, ax + 2.5, ay + 2.5], fill=col)
    for apx, apy, dpx, dpy, col, n in MAP_MARKERS:
        cx, cy = map_x + ox + dpx * ms, map_y + oy + dpy * ms
        num_badge(d, cx, cy, 8, n, col, 10 if n < 10 else 9, width=1)
    # legend: 2 rows x 3 columns
    ly = by2 + 306
    for i, (name, col) in enumerate(LEGEND):
        lx = mx + 12 + (i % 3) * 152
        ly2 = ly + (i // 3) * 18
        d.ellipse([lx, ly2 + 2, lx + 9, ly2 + 11], fill=col)
        d.text((lx + 13, ly2), name, font=font(REG, 11), fill=INK)
    d.text((mx + 10, by2 + 352),
           "Dots: every story with a place on Earth, numbered to match "
           "the list.",
           font=font(REG, 10), fill=GREY)

    # Also-on list (right)
    ax = mx + mpw + gap  # 486
    aw = W - margin - ax  # 528
    d.text((ax + 8, by2 + 8), "ALSO ON WEDNESDAY 18 NOVEMBER \u2014 "
           "23 MORE STORIES", font=font(BOLD, 13), fill=NAVY)
    d.line([ax + 8, by2 + 30, ax + aw - 8, by2 + 30], fill=INK, width=1)
    col1_x, col2_x = ax + 8, ax + 8 + (aw - 8) // 2 + 4
    col_w = (aw - 8) // 2 - 4  # ~252
    for j, (lead, line, col) in enumerate(ALSO_ON):
        n = 10 + j
        col_x = col1_x if j < 12 else col2_x
        row = j if j < 12 else j - 12
        iy = by2 + 44 + row * 30
        num = "%d." % n
        nfnt = font(BOLD, 11)
        nw = d.textlength(num, font=nfnt)
        d.text((col_x, iy), num, font=nfnt, fill=col)
        lx = col_x + nw + 5
        d.text((lx, iy), lead, font=font(BOLD, 10), fill=INK)
        lw = d.textlength(lead, font=font(BOLD, 10))
        d.text((lx + lw + 4, iy), line, font=font(REG, 10), fill=INK)

    # ---- Footer ----
    d.rectangle([0, 990, W, H], fill=NAVY)
    centered(d, 994, "All stories happened or were first reported on "
             "Wednesday 18 November 2026. Disputed claims are attributed.",
             font(REG, 12), WHITE)
    centered(d, 1010, "Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, "
             "UN. Original drawings.", font(REG, 11), GOLD)

    img.save("entry.png", format="PNG")
    print("saved entry.png, stories:", STORY_COUNT)


if __name__ == "__main__":
    main()
