#!/usr/bin/env python3
"""THE DAILY WORLD - Sunday, November 22, 2026.

A one-page newspaper that sums up the world's news of Sunday 22 November
2026 in a single 1024x1024 image, drawn entirely in code.

Python 3 standard library only. Runs offline and deterministically:
two runs produce byte-identical output. Writes the page to
/output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png).
"""

import os
import struct
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- palette
PAPER = (246, 243, 236)
INK = (18, 18, 18)
GRAY = (92, 92, 92)
RULE = (30, 30, 30)
RED = (158, 32, 27)
BLUE = (24, 62, 120)
LIGHT = (232, 227, 216)
WHITE = (250, 249, 246)

# ------------------------------------------------------------------- font
# Hand-drawn 5x7 bitmap typeface. Each glyph is 7 rows of 5 pixels.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", ".#.#.", "..#..", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "2": (".###.", "#...#", "....#", "..##.", ".#...", "#....", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    "'": (".##..", ".##..", ".#...", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "..##.", "..#..", ".....", "..#.."),
    "%": ("##..#", "##.#.", "....#", "...#.", "..#..", ".#...", "#..##"),
    "$": ("..#..", ".####", "#.#.#", ".###.", ".#.#.", "####.", "..#.."),
    "&": (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    "/": ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    "(": ("...##", "..#..", "..#..", "..#..", "..#..", "..#..", "...##"),
    ")": ("##...", "..#..", "..#..", "..#..", "..#..", "..#..", "##..."),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "=": (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
}
DEGREE = (".##..", "#..#.", ".##..", ".....", ".....", ".....", ".....")
EURO = (".###.", "#....", "####.", "#....", "####.", "#....", ".####")
DOT = (".....", ".....", ".....", ".##..", ".##..", ".....", ".....")


def glyph(ch):
    if ch == "°":
        return DEGREE
    if ch == "€":
        return EURO
    if ch == "·":
        return DOT
    if ch in "—–":
        return FONT["-"]
    if ch == "’":
        return FONT["'"]
    if ch in "“”":
        return FONT['"']
    return FONT.get(ch.upper(), FONT[" "])


# ----------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg) * (w * h)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:i + len(row)] = row

    def line(self, x0, y0, x1, y1, color, thick=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            for t in range(thick):
                self.set(x0, y0 + t, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d2 = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill and d2 <= r * r:
                    self.set(xx, yy, color)
                elif not fill and r * r - 2 * r <= d2 <= r * r:
                    self.set(xx, yy, color)


def text_w(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(cv, x, y, s, scale, color, bold=False):
    cx = x
    for ch in s:
        g = glyph(ch)
        for r in range(7):
            row = g[r]
            for c in range(5):
                if row[c] == "#":
                    cv.rect(cx + c * scale, y + r * scale, scale, scale, color)
                    if bold:
                        cv.rect(cx + c * scale + scale, y + r * scale,
                                scale, scale, color)
        cx += 6 * scale
    return cx


def wrap(s, width, scale):
    """Greedy word wrap: returns list of lines fitting width pixels."""
    maxc = max(1, (width + scale) // (6 * scale))
    lines = []
    cur = ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if len(trial) <= maxc:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            while len(word) > maxc:
                lines.append(word[:maxc])
                word = word[maxc:]
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(cv, x, y, w, s, scale, color, gap=5, bold=False):
    """Draw wrapped text; returns y just below the block."""
    lh = 7 * scale + gap
    for ln in wrap(s, w, scale):
        draw_text(cv, x, y, ln, scale, color, bold)
        y += lh
    return y


def centered(cv, y, s, scale, color, bold=False):
    x = (W - text_w(s, scale)) // 2
    draw_text(cv, x, y, s, scale, color, bold)
    return y + 7 * scale


def write_png(cv, path):
    raw = bytearray()
    stride = cv.w * 3
    for yy in range(cv.h):
        raw.append(0)
        raw += cv.px[yy * stride:(yy + 1) * stride]

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


# ---------------------------------------------------------------- content
LEAD_KICKER = "CLIMATE · ANTALYA, TURKEY"
LEAD_HEAD = "CLIMATE TALKS COLLAPSE OVER TWO WORDS: FOSSIL FUELS"
LEAD_BODY = (
    "ANTALYA - The COP31 climate summit ended on Sunday with no agreement, "
    "the first failure of its kind since Copenhagen in 2009, after the EU "
    "and others rejected a text that never mentioned fossil fuels. The "
    "deal, pushed by co-presidents Turkey and Australia, died 44 hours "
    "after the talks were due to close - the longest COP in history. "
    "Russia, China and Arab states backed the text; the US was absent. It "
    "was the first summit since the UN confirmed an overshoot of the "
    "1.5°C Paris limit."
)

PANEL_STATS = [
    ("194", "DELEGATIONS"),
    ("44H", "HOURS OVERTIME"),
    ("0", "FOSSIL-FUEL MENTIONS"),
    ("100+", "WANTED THE WORDS IN"),
]

SIDE = [
    ("MEXICO · GUASAVE, SINALOA",
     "CARTEL KINGPIN 'EL CHAPO ISIDRO' CAPTURED",
     "Mexican special forces seized Fausto Isidro Meza Flores in Guasave, "
     "Sinaloa, in a raid that left 11 dead. He was on the FBI Most Wanted "
     "list."),
    ("SOUTH KOREA · SEOUL",
     "EDUCATION MINISTER QUITS OVER AI EXAM CHAOS",
     "Choi Kyo-jin, 72, resigned over last-minute rules meant to stop AI "
     "cheating in the college entrance exam. President Lee accepted within "
     "an hour."),
]

BAND1 = [
    ("UKRAINE · DYMER",
     "DRONE LEVELS KYIV FLATS; 14 MISSING",
     "A Russian drone collapsed a five-storey block in Dymer, near Kyiv. "
     "Three people died and 14 are missing."),
    ("GULF · BAHRAIN",
     "IRAN HITS BAHRAIN; TANKERS STRUCK",
     "Bahrain said Iran hit a civilian plant, injuring two. Tehran said "
     "it hit US Patriot radars."),
    ("WEST BANK",
     "SETTLERS TORCH CARS IN WEST BANK",
     "Settlers burned cars and daubed racist graffiti in Palestinian "
     "villages. Eisenkot condemned the arson."),
    ("INDONESIA",
     "FACTORY FIRE: 3 DEAD, 34 MISSING",
     "Rescuers recovered remains in 24 body bags at a burned candy "
     "factory in Cikande. Three workers died."),
]

BAND2 = [
    ("TRADE · BRUSSELS",
     "EU AND INDONESIA SIGN TRADE DEAL",
     "Decade-long talks end: tariffs cut on up to 98.5% of goods."),
    ("SPACE · MERCURY",
     "BEPICOLOMBO REACHES MERCURY",
     "ESA and Japan's probe enters Mercury orbit after an 8-year trip."),
    ("NIGERIA · FUNERAL BOAT",
     "24 MOURNERS DIE AS BOAT CAPSIZES",
     "Mourners travelling to a funeral died when their boat capsized."),
]

TICKER = ("MARKETS  S&P -3.7% · NASDAQ -5.3% · NIKKEI -5.1% · "
          "FTSE -1.0% · BRENT $89.95")

BRIEFS = (
    "WASHINGTON: DEMOCRATS HOLD 258 HOUSE SEATS · SUDAN: DRONES HIT "
    "HOMES AND A UN BUILDING IN KHARTOUM · LIBYA: DRONE HITS RUSSIAN "
    "WARSHIP AT BENGHAZI"
)


# ----------------------------------------------------------------- layout
def masthead(cv):
    draw_text(cv, 40, 14, "WORLD NEWS IN ONE IMAGE", 2, GRAY)
    r = "SUNDAY EDITION · NO. 23"
    draw_text(cv, W - 40 - text_w(r, 2), 14, r, 2, GRAY)
    centered(cv, 36, "THE DAILY WORLD", 9, INK, bold=True)
    cv.rect(40, 106, W - 80, 5, RULE)
    cv.rect(40, 114, W - 80, 2, RULE)


def dateline(cv):
    y = 124
    cv.rect(40, y, W - 80, 36, INK)
    draw_text(cv, 58, y + 11, "LATE FINAL", 2, WHITE, bold=True)
    s = "SUNDAY, NOVEMBER 22, 2026"
    draw_text(cv, (W - text_w(s, 3)) // 2, y + 7, s, 3, WHITE, bold=True)
    r = "ONE PAGE"
    draw_text(cv, W - 58 - text_w(r, 2), y + 11, r, 2, WHITE)


def ticker(cv):
    cv.rect(40, 160, W - 80, 28, LIGHT)
    draw_text(cv, 56, 167, TICKER, 2, INK)


def stats_panel(cv, x, y, w):
    h = 58
    cv.rect(x, y, w, h, LIGHT)
    cv.rect(x, y, w, 2, RULE)
    cv.rect(x, y + h - 2, w, 2, RULE)
    cv.rect(x, y, 2, h, RULE)
    cv.rect(x + w - 2, y, 2, h, RULE)
    cell = w // 4
    for i, (num, lab) in enumerate(PANEL_STATS):
        cx = x + 14 + i * cell
        draw_text(cv, cx, y + 10, num, 3, RED, bold=True)
        draw_text(cv, cx, y + 40, lab, 1, INK)


def story(cv, x, y, w, kicker, head, body):
    draw_text(cv, x, y, kicker, 2, RED, bold=True)
    y += 20
    y = block(cv, x, y, w, head, 2, INK, gap=5, bold=True)
    y += 4
    y = block(cv, x, y, w, body, 2, INK, gap=5)
    return y


def front_page():
    cv = Canvas(W, H, PAPER)
    masthead(cv)
    dateline(cv)
    ticker(cv)

    # ---- zone A: lead story left, two side stories right (y 196..598)
    cv.rect(652, 196, 2, 402, RULE)
    draw_text(cv, 40, 196, LEAD_KICKER, 2, RED, bold=True)
    ly = block(cv, 40, 216, 596, LEAD_HEAD, 4, INK, gap=6, bold=True)
    block(cv, 40, ly + 8, 596, LEAD_BODY, 2, INK, gap=5)
    stats_panel(cv, 40, 534, 596)

    sy = story(cv, 668, 196, 316, *SIDE[0])
    cv.rect(668, 388, 316, 2, RULE)
    story(cv, 668, 400, 316, *SIDE[1])

    # ---- band 1: four columns (y 622..806)
    cv.rect(40, 610, W - 80, 3, RULE)
    colw = (W - 80 - 3 * 24) // 4
    for i, item in enumerate(BAND1):
        cx = 40 + i * (colw + 24)
        if i:
            cv.rect(cx - 12, 622, 1, 172, RULE)
        story(cv, cx, 622, colw, *item)

    # ---- band 2: three columns (y 824..943)
    cv.rect(40, 812, W - 80, 2, RULE)
    colw2 = (W - 80 - 2 * 24) // 3
    for i, item in enumerate(BAND2):
        cx = 40 + i * (colw2 + 24)
        if i:
            cv.rect(cx - 12, 824, 1, 112, RULE)
        story(cv, cx, 824, colw2, *item)

    # ---- in brief strip
    cv.rect(40, 953, W - 80, 24, INK)
    draw_text(cv, 56, 958, "IN BRIEF", 2, WHITE, bold=True)
    src = "SOURCES: REUTERS · AP · BBC · CNN · LE MONDE · FRANCE 24 · AL JAZEERA"
    draw_text(cv, W - 56 - text_w(src, 1), 961, src, 1, WHITE)
    block(cv, 40, 985, W - 80, BRIEFS, 2, INK, gap=4)
    return cv


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    size = write_png(front_page(), path)
    print("wrote %s (%d bytes)" % (path, size))


if __name__ == "__main__":
    main()
