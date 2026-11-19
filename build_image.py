#!/usr/bin/env python3
"""Render entry.png for news-image-20261119-v2: one page, 45 stories,
all from Thursday 19 November 2026. Pure Pillow, no randomness, no
timestamps -- the output bytes are identical on every run."""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
PAPER = (247, 242, 231)
CARD = (255, 252, 244)
NAVY = (22, 40, 63)
RED = (176, 42, 33)
INK = (38, 36, 32)
GREY = (96, 89, 76)
LINE = (203, 193, 170)
MAPBG = (18, 32, 52)
MAPDOT = (148, 178, 205)
MAPTXT = (214, 224, 236)

FDIR = "/usr/share/fonts/truetype/liberation/"
SERIF = FDIR + "LiberationSerif-Regular.ttf"
SERIF_B = FDIR + "LiberationSerif-Bold.ttf"
SERIF_I = FDIR + "LiberationSerif-Italic.ttf"
SANS = FDIR + "LiberationSans-Regular.ttf"
SANS_B = FDIR + "LiberationSans-Bold.ttf"

FONTS = {}


def F(path, size):
    key = (path, size)
    if key not in FONTS:
        FONTS[key] = ImageFont.truetype(path, size)
    return FONTS[key]


def tw(d, s, font):
    return d.textlength(s, font=font)


def wrap(d, text, font, maxw):
    """Greedy word wrap; returns list of lines that each fit maxw."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if tw(d, trial, font) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def wrap_rich(d, segments, maxw):
    """Wrap a list of (text, font, color) segments word by word.
    Returns list of lines; each line is a list of (word, font, color)."""
    words = []
    for text, font, color in segments:
        for w in text.split(" "):
            if w:
                words.append((w, font, color))
    space = lambda f: tw(d, " ", f)
    lines, cur, curw = [], [], 0.0
    for w, font, color in words:
        ww = tw(d, w, font)
        add = ww if not cur else ww + space(font)
        if cur and curw + add > maxw:
            lines.append(cur)
            cur, curw = [(w, font, color)], ww
        else:
            cur.append((w, font, color))
            curw += add
    if cur:
        lines.append(cur)
    return lines


def draw_rich(d, segments, x, y, maxw, lh, max_lines=None):
    lines = wrap_rich(d, segments, maxw)
    if max_lines:
        lines = lines[:max_lines]
    for i, line in enumerate(lines):
        cx = x
        for j, (w, font, color) in enumerate(line):
            if j:
                cx += tw(d, " ", font)
            d.text((cx, y + i * lh), w, font=font, fill=color)
            cx += tw(d, w, font)
    return len(lines)


def num_badge(d, cx, cy, n, r=10):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    d.text((cx, cy), str(n), font=F(SANS_B, 11 if n < 10 else 10),
           fill=(255, 255, 255), anchor="mm")


# ---------------------------------------------------------------- content
LEADS = [
    dict(n=1, label="SHENZHEN · SUMMIT", art="summit",
         head="Trump, Xi and Putin hold first three-way summit",
         desc="The leaders of the three biggest nuclear powers sit down "
              "together for the first time, at APEC in Shenzhen. "
              "Arms control tops the agenda."),
    dict(n=2, label="NEW YORK · GAMES", art="gta",
         head="GTA VI arrives after a 13-year wait",
         desc="Rockstar's game launches worldwide, New Zealand first at "
              "midnight. 15.9 million pre-orders banked about $1.54bn. "
              "PS5 and Xbox only \u2014 no PC yet."),
    dict(n=3, label="NASDAQ · MARKETS", art="ipo",
         head="Anthropic debuts in biggest IPO on record",
         desc="The AI firm starts trading on Nasdaq Thursday after pricing "
              "at $83 and raising $81.3bn, eclipsing SpaceX's $75bn as "
              "the largest IPO ever."),
]

MIDS = [
    dict(n=4, label="THE HAGUE · LAW", icon="scales",
         head="World Court rules on Rohingya genocide case",
         body="ICJ judgment in The Gambia v. Myanmar over the 2017 "
              "crackdown that drove out 730,000 Rohingya."),
    dict(n=5, label="ANTALYA · CLIMATE", icon="leaf",
         head="COP31 enters its final 48 hours",
         body="Friday deadline, with 'phase out' wording and a "
              "$120bn-a-year adaptation goal still unresolved."),
    dict(n=6, label="ODISHA · STORM", icon="cyclone",
         head="Cyclone Akvan bears down on the coast",
         body="204,070 listed for evacuation; red warnings in six "
              "districts; landfall Friday near Gopalpur."),
    dict(n=7, label="KYIV · WAR", icon="flag",
         head="Ukraine left off the Shenzhen agenda",
         body="Kyiv has no seat at the talks. Aides say the war is off "
              "the agenda; Trump says he will raise it."),
    dict(n=8, label="SHENZHEN · TRADE", icon="trade",
         head="Xi pledges $20m for APEC cooperation",
         body="China funds APEC cooperation, opens a Shenzhen research "
              "centre and pushes a free-trade area."),
    dict(n=9, label="FLORIDA · WEATHER", icon="rain",
         head="Flooded Florida braces for more rain",
         body="A foot of rain fell in hours; Broward and Miami-Dade "
              "schools shut Thursday as more rain threatens."),
    dict(n=10, label="KERCH · WAR", icon="bridge",
         head="Kerch Bridge hit for third time this week",
         body="Overnight strike halts traffic on Russia's Crimea bridge; "
              "damage being assessed, officials say."),
    dict(n=11, label="GAZA · CEASEFIRE", icon="tank",
         head="Israeli tanks cross the Yellow Line",
         body="IDF says it hit a tunnel inside Gaza; Hamas calls it a "
              "flagrant breach of the October ceasefire."),
    dict(n=12, label="TOKYO · DEFENCE", icon="shield",
         head="India and Japan review defence ties",
         body="Fourth 2+2 dialogue: Jaishankar and Rajnath Singh meet "
              "Motegi and Koizumi on maritime security."),
    dict(n=13, label="NEW YORK · ART", icon="frame",
         head="Van Gogh sells for a record $190.4m",
         body="His 'Blossoming Chestnut Trees' (1890) sets an artist "
              "record \u2014 fourth-priciest painting ever sold."),
]

# (number, place, bold keyword, rest) -- stories 14..45
BRIEFS = [
    (14, "MEXICO CITY", "Banxico minutes", "of 3\u20132 cut to 6.25%"),
    (15, "WELLINGTON", "India omit Siraj and Jadeja", "from opening Test XI"),
    (16, "SEOUL", "Lee\u2013Putin talk;", "no sign of US\u2013North Korea talks"),
    (17, "PALO ALTO", "Arora: outages no coincidence,", "AI easing cyberattacks"),
    (18, "SAN JOSE", "Logitech's 7,000 staff", "get a paid gaming day"),
    (19, "BERLIN", "Leave requests up 38%", "for GTA VI launch day"),
    (20, "CHENNAI", "Design firm declares holiday", "for GTA VI launch day"),
    (21, "ABUJA", "Tinubu, Jonathan unveil", "Buhari's authorised biography"),
    (22, "NAIROBI", "Opposition forum", "presses five election reforms"),
    (23, "NAIROBI", "Floods kill six", "as Ruto gives State of the Nation"),
    (24, "SOWETO", "Search resumes", "for missing girl; man dead"),
    (25, "PARIS", "France under 317 weather alerts", "for flood, wind and snow"),
    (26, "BOGOT\u00c1", "Colombia battles", "fire and landslide alerts"),
    (27, "SACRAMENTO", "Atmospheric river", "flood advisories for California"),
    (28, "NEW YORK", "Oil falls Thursday:", "Brent $91.70 on surplus fears"),
    (29, "SHENZHEN", "Musk travels with Trump,", "takes no seat at three-way talks"),
    (30, "ANTALYA", "India demands equity", "and delivered climate finance"),
    (31, "SANTA CLARA", "Nvidia halts H200", "chip shipments to mainland China"),
    (32, "CANBERRA", "Australia sanctions", "West Bank settlers and groups"),
    (33, "MOGADISHU", "Somalia accuses UAE", "of secret bases (attributed)"),
    (34, "WASHINGTON", "Senators warn", "AI cyber threats outpace defences"),
    (35, "SHENZHEN", "Carney resets China ties,", "seeks 'right deal' with US"),
    (36, "BAGHDAD", "Six French ISIL members", "jailed for life in Iraq"),
    (37, "WASHINGTON", "Vance: no 'forever war'", "for the US in the Gulf"),
    (38, "MANAMA", "Bapco refinery", "back above 80% after six strikes"),
    (39, "JAZAN", "Saudi: danger passed", "in three cities after alerts"),
    (40, "DERNA", "Libya seizes", "4m pills, 29kg cocaine and hashish"),
    (41, "MUMBAI", "Goldman upgrades India", "to overweight; Nifty 28,500"),
    (42, "NEW DELHI", "Schools resume in person", "as curbs revoked"),
    (43, "NEW DELHI", "162.5% duty", "hits bulk Scotch whisky imports"),
    (44, "NEW DELHI", "Contempt notice", "over remarks against Chief Justice"),
    (45, "PARIS", "M\u00e9lenchon could win,", "says France's justice minister"),
]

REGIONS = [
    ("ASIA-PACIFIC", 14, (46, 111, 106)),
    ("NORTH AMERICA", 11, (51, 82, 110)),
    ("EUROPE", 8, (181, 122, 30)),
    ("AFRICA", 6, (109, 59, 94)),
    ("MIDDLE EAST", 4, (164, 74, 36)),
    ("LATIN AMERICA", 2, (74, 107, 47)),
]

NUMBERS = [
    ("$81.3bn", "RAISED IN RECORD IPO"),
    ("15.9m", "GTA VI PRE-ORDERS"),
    ("200,000", "LISTED TO EVACUATE"),
    ("$120bn", "ADAPTATION GOAL / YEAR"),
    ("730,000", "ROHINGYA EXPELLED 2017"),
    ("13 yrs", "WAIT FOR GTA VI"),
]

# dot-matrix world map: land runs (row, first col, last col), 76 cols x 30 rows
LAND = [
    [(6, 12), (50, 58), (62, 70)],
    [(4, 16), (47, 71)],
    [(3, 18), (37, 40), (45, 72)],
    [(3, 17), (36, 42), (44, 71)],
    [(4, 16), (36, 44), (44, 70)],
    [(5, 15), (35, 43), (45, 68)],
    [(5, 15), (35, 42), (46, 66), (68, 69)],
    [(6, 14), (35, 41), (47, 63), (65, 67)],
    [(6, 13), (35, 40), (44, 49), (50, 62), (64, 66)],
    [(6, 12), (35, 46), (45, 50), (51, 61)],
    [(7, 11), (36, 47), (45, 49), (51, 57), (58, 62)],
    [(7, 10), (36, 47), (45, 48), (52, 56), (58, 61)],
    [(17, 18), (37, 46), (53, 55), (58, 60), (61, 64)],
    [(17, 19), (37, 46), (54, 54), (58, 65)],
    [(17, 21), (38, 46), (59, 66)],
    [(18, 22), (38, 45), (60, 63)],
    [(18, 23), (39, 45)],
    [(18, 24), (39, 44), (60, 67)],
    [(19, 24), (40, 44), (59, 68)],
    [(19, 24), (40, 43), (60, 67)],
    [(19, 23), (40, 43), (61, 66)],
    [(19, 23), (40, 42)],
    [(20, 22), (40, 42), (45, 45)],
    [(20, 22), (41, 42), (45, 45)],
    [(20, 21)],
    [(20, 21), (70, 71)],
    [(20, 20), (71, 72)],
    [(20, 20)],
    [(20, 20)],
    [],
]

# (story number, longitude, latitude, dx, dy) for the 13 card stories
PINS = [
    (1, 114.1, 22.5, 0, 0), (2, -74.0, 40.7, 0, 0), (3, -122.4, 37.8, 0, 0),
    (4, 4.3, 52.1, 0, 0), (5, 30.7, 36.9, 0, 0), (6, 85.8, 19.8, 0, 0),
    (7, 30.5, 50.4, 0, 0), (8, 114.1, 22.5, 11, 12), (9, -80.2, 26.0, 0, 0),
    (10, 36.5, 45.4, 0, 0), (11, 34.3, 31.4, 0, 0), (12, 139.7, 35.7, 0, 0),
    (13, -74.0, 40.7, 12, 13),
]

# ---------------------------------------------------------------- lead art
def art_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 52, 84))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(13, 30, 50))
    flags = [(36, (58, 92, 160)), (x + w // 2 - 21, (196, 44, 38)),
             (x + w - 78, (232, 230, 222))]
    for fx, col in flags:
        d.line([fx, y + 12, fx, y + h - 14], fill=(220, 220, 210), width=2)
        d.rectangle([fx + 2, y + 12, fx + 42, y + 30], fill=col)
    for sx, sy in [(x + 52, y + 19), (x + 62, y + 19), (x + 57, y + 25),
                   (x + w // 2 - 4, y + 21), (x + w - 60, y + 19),
                   (x + w - 52, y + 25)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(245, 205, 80))
    d.rectangle([x + w - 78 + 2, y + 21, x + w - 36, y + 24], fill=(58, 92, 160))
    d.rectangle([x + w - 78 + 2, y + 27, x + w - 36, y + 30], fill=(196, 44, 38))


def art_gta(d, x, y, w, h):
    bands = [(238, 140, 60), (232, 102, 84), (198, 74, 110),
             (140, 62, 120), (84, 48, 110)]
    bh = h // len(bands) + 1
    for i, col in enumerate(bands):
        d.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh], fill=col)
    d.ellipse([x + w - 96, y + 8, x + w - 56, y + 48], fill=(250, 214, 120))
    base = y + h
    for bx, bw, bh2 in [(6, 26, 22), (38, 18, 30), (88, 22, 18),
                        (196, 20, 26), (252, 26, 20), (286, 18, 30)]:
        d.rectangle([x + bx, base - bh2, x + bx + bw, base], fill=(30, 22, 48))
    for px in (70, 150, 232):
        d.line([x + px, base, x + px - 3, base - 30], fill=(24, 40, 34), width=3)
        for a in range(0, 360, 45):
            import math
            ex = x + px - 3 + 13 * math.cos(math.radians(a + 180))
            ey = base - 30 + 6 * math.sin(math.radians(a + 180)) - 3
            d.line([x + px - 3, base - 30, ex, ey], fill=(24, 40, 34), width=2)


def art_ipo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(233, 240, 224))
    d.line([x + 18, y + 8, x + 18, y + h - 12], fill=(120, 130, 110), width=2)
    d.line([x + 18, y + h - 12, x + w - 12, y + h - 12],
           fill=(120, 130, 110), width=2)
    bars = [(34, 16, (140, 170, 120)), (86, 26, (110, 155, 105)),
            (138, 38, (80, 140, 90)), (190, 52, (176, 42, 33))]
    for bx, bh2, col in bars:
        d.rectangle([x + bx, y + h - 12 - bh2, x + bx + 38, y + h - 12], fill=col)
    d.line([x + 40, y + h - 34, x + 105, y + h - 46, x + 160, y + h - 56,
            x + 232, y + h - 66], fill=NAVY, width=3)
    d.polygon([(x + 232, y + h - 66), (x + 220, y + h - 64),
               (x + 226, y + h - 54)], fill=NAVY)
    d.text((x + w - 52, y + 6), "$", font=F(SERIF_B, 30), fill=(176, 42, 33))


ART = {"summit": art_summit, "gta": art_gta, "ipo": art_ipo}

# ---------------------------------------------------------------- mid icons
def icon(d, name, cx, cy):
    c = NAVY
    if name == "scales":
        d.line([cx, cy - 8, cx, cy + 8], fill=c, width=2)
        d.line([cx - 9, cy - 5, cx + 9, cy - 5], fill=c, width=2)
        d.polygon([(cx - 9, cy - 5), (cx - 14, cy + 3), (cx - 4, cy + 3)], outline=c)
        d.polygon([(cx + 9, cy - 5), (cx + 4, cy + 3), (cx + 14, cy + 3)], outline=c)
        d.line([cx - 5, cy + 9, cx + 5, cy + 9], fill=c, width=2)
    elif name == "leaf":
        d.ellipse([cx - 9, cy - 6, cx + 7, cy + 8], outline=c, width=2)
        d.line([cx - 7, cy + 7, cx + 8, cy - 7], fill=c, width=2)
    elif name == "cyclone":
        for r, a0 in [(9, 20), (6, 140), (3, 260)]:
            d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 240, fill=c, width=2)
    elif name == "flag":
        d.line([cx - 6, cy - 9, cx - 6, cy + 9], fill=c, width=2)
        d.polygon([(cx - 6, cy - 9), (cx + 9, cy - 5), (cx - 6, cy - 1)], fill=RED)
    elif name == "trade":
        d.arc([cx - 9, cy - 9, cx + 9, cy + 9], 300, 130, fill=c, width=2)
        d.arc([cx - 9, cy - 9, cx + 9, cy + 9], 120, 310, fill=c, width=2)
        d.polygon([(cx + 8, cy - 8), (cx + 2, cy - 9), (cx + 7, cy - 2)], fill=c)
        d.polygon([(cx - 8, cy + 8), (cx - 2, cy + 9), (cx - 7, cy + 2)], fill=c)
    elif name == "rain":
        d.arc([cx - 10, cy - 9, cx + 2, cy + 3], 90, 300, fill=c, width=2)
        d.arc([cx - 2, cy - 11, cx + 11, cy + 3], 90, 330, fill=c, width=2)
        d.line([cx - 11, cy + 2, cx + 11, cy + 2], fill=c, width=2)
        for dx in (-6, 0, 6):
            d.line([cx + dx, cy + 5, cx + dx - 2, cy + 10], fill=(58, 92, 160), width=2)
    elif name == "bridge":
        d.arc([cx - 13, cy - 4, cx + 13, cy + 14], 180, 360, fill=c, width=2)
        d.line([cx - 13, cy + 5, cx + 13, cy + 5], fill=c, width=2)
        for dx in (-8, 0, 8):
            d.line([cx + dx, cy - 2, cx + dx, cy + 5], fill=c, width=1)
    elif name == "tank":
        d.rectangle([cx - 11, cy, cx + 8, cy + 6], fill=c)
        d.rectangle([cx - 4, cy - 4, cx + 4, cy], fill=c)
        d.line([cx + 4, cy - 2, cx + 14, cy - 2], fill=c, width=2)
        for dx in (-8, -3, 2, 7):
            d.ellipse([cx + dx - 2, cy + 6, cx + dx + 2, cy + 10], fill=c)
    elif name == "shield":
        d.polygon([(cx, cy - 10), (cx + 8, cy - 7), (cx + 8, cy + 2),
                   (cx, cy + 10), (cx - 8, cy + 2), (cx - 8, cy - 7)], outline=c)
        d.line([cx, cy - 10, cx, cy + 10], fill=c, width=1)
    elif name == "frame":
        d.rectangle([cx - 10, cy - 8, cx + 10, cy + 8], outline=c, width=2)
        d.polygon([(cx - 7, cy + 5), (cx - 1, cy - 2), (cx + 3, cy + 5)], fill=c)
        d.ellipse([cx + 3, cy - 6, cx + 7, cy - 2], fill=RED)


# ---------------------------------------------------------------- build
def main():
    img = Image.new("RGB", (1024, 1024), PAPER)
    d = ImageDraw.Draw(img)
    M, R = 26, 998  # left margin, right edge

    # masthead
    d.text((M, 17), "THE DAY IN WORLD NEWS", font=F(SANS_B, 16), fill=RED)
    d.text((R, 20), "THURSDAY'S NEWS \u00b7 ONE PAGE \u00b7 45 STORIES",
           font=F(SANS_B, 12), fill=NAVY, anchor="ra")
    d.line([M, 43, R, 43], fill=NAVY, width=2)

    # date + subline
    d.text((M, 50), "Thursday 19 November 2026", font=F(SERIF_B, 52), fill=NAVY)
    d.text((M, 110), "Shenzhen's first three-way summit \u00b7 GTA VI finally "
           "lands \u00b7 Anthropic's record IPO \u00b7 a world court rules on "
           "the Rohingya", font=F(SERIF_I, 15), fill=RED)

    # region strip
    segw = (R - M) / 6.0
    for i, (name, count, col) in enumerate(REGIONS):
        x0 = M + i * segw
        d.rectangle([x0, 136, x0 + segw - 2, 162], fill=col)
        label = "%s %d" % (name, count)
        d.text((x0 + (segw - 2) / 2, 149), label, font=F(SANS_B, 11),
               fill=(255, 255, 255), anchor="mm")

    # big numbers strip
    d.line([M, 170, R, 170], fill=LINE, width=1)
    for i, (num, lab) in enumerate(NUMBERS):
        cx = M + i * segw + segw / 2
        d.text((cx, 176), num, font=F(SERIF_B, 25), fill=NAVY, anchor="ma")
        d.text((cx, 205), lab, font=F(SANS_B, 8), fill=GREY, anchor="ma")
    d.line([M, 218, R, 218], fill=LINE, width=1)

    # lead cards
    ly, lh_, lw, gap = 226, 184, 317, 10
    for i, c in enumerate(LEADS):
        x = M + i * (lw + gap)
        d.rectangle([x, ly, x + lw, ly + lh_], fill=CARD, outline=LINE)
        ART[c["art"]](d, x + 1, ly + 1, lw - 2, 62)
        num_badge(d, x + 20, ly + 80, c["n"])
        d.text((x + 36, ly + 80), c["label"], font=F(SANS_B, 11),
               fill=RED, anchor="lm")
        hl = wrap(d, c["head"], F(SERIF_B, 21), lw - 20)
        for j, line in enumerate(hl[:2]):
            d.text((x + 10, ly + 94 + j * 24), line, font=F(SERIF_B, 21),
                   fill=NAVY)
        dl = wrap(d, c["desc"], F(SANS, 11), lw - 20)
        for j, line in enumerate(dl[:3]):
            d.text((x + 10, ly + 144 + j * 14), line, font=F(SANS, 11),
                   fill=INK)

    # mid cards, 2 rows x 5
    mw, mh, mgap = 188, 108, 8
    tints = [(238, 232, 214), (226, 234, 228), (232, 228, 236),
             (236, 230, 220), (224, 232, 238)]
    for idx, c in enumerate(MIDS):
        row, col = divmod(idx, 5)
        x = M + col * (mw + mgap)
        y = 418 + row * (mh + 6)
        d.rectangle([x, y, x + mw, y + mh], fill=CARD, outline=LINE)
        d.rectangle([x + 1, y + 1, x + mw - 1, y + 21], fill=tints[col])
        icon(d, c["icon"], x + 16, y + 11)
        d.text((x + 33, y + 11), c["label"], font=F(SANS_B, 9),
               fill=RED, anchor="lm")
        num_badge(d, x + mw - 16, y + 34, c["n"], r=9)
        hl = wrap(d, c["head"], F(SERIF_B, 13), mw - 40)
        for j, line in enumerate(hl[:2]):
            d.text((x + 8, y + 26 + j * 15), line, font=F(SERIF_B, 13),
                   fill=NAVY)
        bl = wrap(d, c["body"], F(SANS, 9), mw - 16)
        for j, line in enumerate(bl[:3]):
            d.text((x + 8, y + 58 + j * 12), line, font=F(SANS, 9), fill=INK)

    # bottom: map panel (left) + briefs (right)
    by, bh = 640, 296
    d.rectangle([M, by, M + 320, by + bh], fill=MAPBG)
    d.text((M + 12, by + 10), "WHERE IT HAPPENED", font=F(SANS_B, 12),
           fill=MAPTXT)
    d.text((M + 12, by + 28), "The 13 card stories, pinned approximately",
           font=F(SANS, 9), fill=(150, 168, 190))
    mx, my, mw2, mh2 = M + 10, by + 46, 300, 168
    for r, runs in enumerate(LAND):
        for c0, c1 in runs:
            for cc in range(c0, c1 + 1):
                px = mx + cc * (mw2 / 76.0)
                py = my + r * (mh2 / 30.0)
                d.ellipse([px, py, px + 2.4, py + 2.4], fill=MAPDOT)
    for n, lon, lat, dx, dy in PINS:
        px = mx + (lon + 170) / 360.0 * mw2 + dx
        py = my + (75 - lat) / 130.0 * mh2 + dy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255))
        d.text((px, py), str(n), font=F(SANS_B, 9), fill=(255, 255, 255),
               anchor="mm")
    d.text((M + 12, by + 226), "New York hosts stories 2 and 13 and Shenzhen",
           font=F(SANS, 9), fill=(150, 168, 190))
    d.text((M + 12, by + 240), "1 and 8 \u2014 their pins are nudged apart.",
           font=F(SANS, 9), fill=(150, 168, 190))
    d.text((M + 12, by + 262), "Dots: a stylised world, drawn for this page.",
           font=F(SERIF_I, 9), fill=(150, 168, 190))

    bx = M + 334
    d.text((bx, by + 2), "ALSO ON THURSDAY 19 NOVEMBER \u2014 32 MORE STORIES",
           font=F(SANS_B, 13), fill=RED)
    d.line([bx, by + 22, R, by + 22], fill=RED, width=1)
    colw, cgap = 204, 14
    cols = [BRIEFS[:11], BRIEFS[11:22], BRIEFS[22:]]
    for ci, chunk in enumerate(cols):
        x = bx + ci * (colw + cgap)
        y = by + 28
        for n, place, key, rest in chunk:
            segs = [("%d " % n, F(SANS_B, 9), RED),
                    (place + " \u2014 ", F(SANS_B, 9), INK),
                    (key, F(SANS_B, 9), INK),
                    (rest, F(SANS, 9), INK)]
            used = draw_rich(d, segs, x, y, colw, 10.5)
            y += used * 10.5 + 3.5

    # date check box
    dy0 = 942
    d.rectangle([M, dy0, R, dy0 + 36], outline=RED, width=2)
    dc = ("DATE CHECK \u2014 reported Wednesday or earlier, so NOT counted as "
          "Thursday news: Jeffries' 251\u201311 nomination \u00b7 Voyager 1's "
          "one-light-day crossing \u00b7 EU's \u20ac45bn Ukraine loan plan "
          "\u00b7 Pew's 2035 religion projection \u00b7 drones over Kuwait & "
          "Bahrain \u00b7 Bangladesh garment shutdowns \u00b7 Fed minutes "
          "\u00b7 Nvidia earnings \u00b7 first COP31 draft (Mon)")
    dcl = wrap(d, dc, F(SANS, 9), R - M - 24)
    for j, line in enumerate(dcl[:2]):
        d.text((M + 12, dy0 + 6 + j * 12), line, font=F(SANS, 9), fill=RED)

    # footer
    foot = ("Every story here happened, or was first reported, on Thursday "
            "19 November 2026. Disputed claims are attributed. Sources: "
            "Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 Al Jazeera "
            "\u00b7 UN News \u00b7 IMD \u00b7 ICJ. Original drawings.")
    fl = wrap(d, foot, F(SANS, 9), R - M)
    for j, line in enumerate(fl[:2]):
        d.text(((M + R) / 2, 984 + j * 12), line, font=F(SANS, 9),
               fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
