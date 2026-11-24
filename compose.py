#!/usr/bin/env python3
"""The World Today — 24 November 2026. Draws the illustrated broadsheet
entry.png (1024x1024) for the make.fun news-image-20261124 bounty.

Layout (winner of a two-variant test in this session): masthead and a
full-width black date band, then a tall drawn illustration on the left
with the lead headline and summary stacked on the right, five grid
stories as full-width rows with one drawn icon each, and an ALSO TODAY
strip. Everything is drawn with Pillow from plain shapes and text: no
photos, no network, no copied artwork. Run:  python3 compose.py
Writes entry.png next to this file. Deterministic: same bytes every run.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 240, 220)
INK = (23, 19, 12)
RED = (158, 27, 27)
NAVY = (22, 50, 79)
SEA = (24, 58, 92)
SEA_DARK = (16, 40, 66)
SKY_TOP = (232, 214, 176)
SKY_BOT = (246, 226, 178)
GREY = (90, 86, 76)
GOLD = (200, 162, 74)
ORANGE = (232, 116, 28)
FLAME = (244, 164, 40)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def spaced(draw, xy, text, fnt, fill, tracking=3):
    """Draw text with extra letter spacing, centred on x if xy is (cx, y)."""
    cx, y = xy
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


def spaced_left(draw, x, y, text, fnt, fill, tracking=3):
    """Draw text with extra letter spacing, left-aligned at x."""
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


def rule(draw, x0, x1, y, weight=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=weight)


# ---------------------------------------------------------------- icons
def icon_chart(d, x, y, s, col):
    d.rectangle([x, y, x + s, y + s], outline=col, width=3)
    base = y + s - 10
    bars = [0.35, 0.55, 0.45, 0.8]
    bw = s // 6
    for i, f in enumerate(bars):
        bx = x + 8 + i * (bw + 3)
        bh = int((s - 22) * f)
        d.rectangle([bx, base - bh, bx + bw, base], fill=col)
    d.line([(x + 8, base - int((s - 22) * 0.8) - 6),
            (x + s - 8, base - int((s - 22) * 0.8) - 14)], fill=RED, width=3)
    d.polygon([(x + s - 8, base - int((s - 22) * 0.8) - 18),
               (x + s - 2, base - int((s - 22) * 0.8) - 12),
               (x + s - 12, base - int((s - 22) * 0.8) - 8)], fill=RED)


def icon_target(d, x, y, s, col):
    cx, cy = x + s // 2, y + s // 2
    for r in (s // 2 - 2, s // 3, s // 6):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)


def icon_flame(d, x, y, s, col):
    cx = x + s // 2
    d.polygon([(cx, y + 2), (cx + s // 4, y + s // 3),
               (cx + s // 3, y + s // 2), (cx + s // 4, y + s - 6),
               (cx - s // 4, y + s - 6), (cx - s // 3, y + s // 2),
               (cx - s // 4, y + s // 3)], fill=ORANGE)
    d.polygon([(cx, y + s // 2), (cx + s // 7, y + s - 12),
               (cx - s // 7, y + s - 12)], fill=FLAME)


def icon_rocket(d, x, y, s, col):
    cx = x + s // 2
    d.polygon([(cx, y + 2), (cx + s // 4, y + s // 2),
               (cx, y + s * 3 // 4), (cx - s // 4, y + s // 2)], fill=col)
    d.polygon([(cx - s // 4, y + s // 2), (cx - s // 2, y + s * 3 // 4),
               (cx - s // 6, y + s * 2 // 3)], fill=col)
    d.polygon([(cx + s // 4, y + s // 2), (cx + s // 2, y + s * 3 // 4),
               (cx + s // 6, y + s * 2 // 3)], fill=col)
    d.ellipse([cx - 5, y + s // 3, cx + 5, y + s // 3 + 10], fill=CREAM)
    d.polygon([(cx - 6, y + s * 3 // 4), (cx + 6, y + s * 3 // 4),
               (cx, y + s - 2)], fill=ORANGE)


def icon_scales(d, x, y, s, col):
    cx = x + s // 2
    d.line([(cx, y + 4), (cx, y + s - 8)], fill=col, width=3)
    d.line([(x + 6, y + 12), (x + s - 6, y + 12)], fill=col, width=3)
    d.polygon([(x + 2, y + 12), (x + 14, y + 12), (x + 8, y + s - 10)], fill=col)
    d.polygon([(x + s - 14, y + 12), (x + s - 2, y + 12), (x + s - 8, y + s - 10)],
              fill=col)
    d.line([(x + 6, y + s - 6), (x + s - 6, y + s - 6)], fill=col, width=3)


ICONS = {"chart": icon_chart, "target": icon_target, "flame": icon_flame,
         "rocket": icon_rocket, "scales": icon_scales}


# ------------------------------------------------------- lead illustration
def draw_scene(d, x0, y0, x1, y1):
    """Dusk sea at Benghazi port: a grey warship burning at anchor, naval
    drone boats closing in, smoke over the harbour. Flat shapes only."""
    d.rectangle([x0, y0, x1, y1], fill=SKY_TOP)
    horizon = y0 + int((y1 - y0) * 0.48)
    for i in range(6):
        yy = y0 + i * (horizon - y0) // 6
        shade = tuple(int(SKY_TOP[c] + (SKY_BOT[c] - SKY_TOP[c]) * i / 5) for c in range(3))
        d.rectangle([x0, yy, x1, yy + (horizon - y0) // 6 + 1], fill=shade)
    # low sun
    sx, sy, sr = x0 + 92, horizon - 34, 44
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(238, 178, 84))
    d.ellipse([sx - sr + 10, sy - sr + 10, sx + sr - 10, sy + sr - 10],
              fill=(244, 196, 110))
    # distant port skyline
    d.rectangle([x0, horizon - 30, x0 + 130, horizon], fill=(120, 104, 78))
    d.rectangle([x0 + 24, horizon - 52, x0 + 48, horizon], fill=(120, 104, 78))
    d.rectangle([x0 + 78, horizon - 40, x0 + 96, horizon], fill=(120, 104, 78))
    d.rectangle([x1 - 150, horizon - 24, x1 - 30, horizon], fill=(120, 104, 78))
    # sea
    d.rectangle([x0, horizon, x1, y1], fill=SEA)
    d.rectangle([x0, horizon, x1, horizon + 6], fill=SEA_DARK)
    for wy in range(horizon + 18, y1 - 10, 22):
        for wx in range(x0 + 16, x1 - 70, 96):
            d.line([(wx, wy), (wx + 48, wy)], fill=(120, 160, 200), width=2)
    # warship, bow to the right, listing after the strike
    hx0, hx1 = x0 + 60, x1 - 36
    hy = horizon + 46
    d.polygon([(hx0, hy - 44), (hx1, hy - 44), (hx1 - 34, hy + 8),
               (hx0 + 22, hy + 8)], fill=(52, 54, 58))
    d.polygon([(hx0 + 22, hy + 8), (hx1 - 34, hy + 8), (hx1 - 48, hy + 20),
               (hx0 + 48, hy + 20)], fill=(38, 40, 44))
    d.rectangle([hx0 + 110, hy - 96, hx0 + 330, hy - 44], fill=(66, 68, 72))
    d.rectangle([hx0 + 150, hy - 128, hx0 + 250, hy - 96], fill=(66, 68, 72))
    d.line([(hx0 + 200, hy - 128), (hx0 + 200, hy - 152)], fill=(52, 54, 58), width=6)
    d.line([(hx0 + 200, hy - 152), (hx0 + 236, hy - 136)], fill=(52, 54, 58), width=4)
    for wx in range(hx0 + 162, hx0 + 242, 24):
        d.rectangle([wx, hy - 120, wx + 13, hy - 108], fill=(246, 226, 178))
    d.line([(hx0 + 330, hy - 52), (hx0 + 384, hy - 66)], fill=(52, 54, 58), width=7)
    # flames and smoke at midship, kept inside the scene box
    fx = hx0 + 250
    d.polygon([(fx - 44, hy - 44), (fx - 10, hy - 122), (fx + 8, hy - 78),
               (fx + 28, hy - 128), (fx + 50, hy - 44)], fill=ORANGE)
    d.polygon([(fx - 22, hy - 44), (fx - 2, hy - 92), (fx + 18, hy - 44)], fill=FLAME)
    for sx2, sy2, sr2 in [(fx - 20, y0 + 34, 24), (fx + 30, y0 + 16, 30),
                          (fx + 80, y0 + 32, 26), (fx + 120, y0 + 14, 20)]:
        d.ellipse([sx2 - sr2, sy2 - sr2, sx2 + sr2, sy2 + sr2], fill=(74, 72, 68))
    # drone boats with wakes closing in
    for bx, by in [(x0 + 60, horizon + 92), (x0 + 210, horizon + 128)]:
        d.polygon([(bx, by), (bx + 58, by), (bx + 48, by + 14), (bx + 10, by + 14)],
                  fill=(28, 30, 34))
        d.line([(bx - 40, by + 14), (bx + 8, by + 14)], fill=(240, 244, 248), width=3)
        d.line([(bx - 26, by + 21), (bx + 20, by + 21)], fill=(240, 244, 248), width=2)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    tag = "ILLUSTRATION"
    tf = font(SANS_B, 13)
    tw = d.textlength(tag, font=tf) + 16
    d.rectangle([x0, y0, x0 + tw, y0 + 24], fill=NAVY)
    d.text((x0 + 8, y0 + 4), tag, font=tf, fill=(255, 255, 255))


# ------------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=2)
    d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)

    # masthead
    spaced(d, (W // 2, 34), "ONE DAY · ONE PAGE · THE WORLD", font(SANS_B, 14), GREY, 4)
    d.text((W // 2, 52), "The World Today", font=font(SERIF_B, 68),
           fill=INK, anchor="ma")
    rule(d, 36, W - 36, 132, 2)
    rule(d, 36, W - 36, 137, 5)

    # date band
    d.rectangle([36, 150, W - 36, 214], fill=INK)
    d.text((W // 2, 162), "TUESDAY · 24 NOVEMBER · 2026", font=font(SANS_B, 42),
           fill=(255, 255, 255), anchor="ma")

    # ---- lead: illustration left, words right
    draw_scene(d, 36, 232, 560, 520)
    tx = 584
    spaced_left(d, tx, 240, "THE WAR AT SEA", font(SANS_B, 17), RED, 2)
    spaced_left(d, tx, 264, "BENGHAZI, LIBYA", font(SANS_B, 17), RED, 2)
    yy = 288
    for ln in ["UKRAINE SINKS", "RUSSIAN WARSHIP", "OFF LIBYA"]:
        d.text((tx, yy), ln, font=font(SERIF_B, 40), fill=INK)
        yy += 48
    summary = ("Kyiv says seven naval drones sank the corvette Merkury and hit a "
               "weapons cargo ship in Benghazi port. Ukraine calls the strike "
               "self-defence.")
    yy += 8
    for ln in wrap(d, summary, font(SANS, 19), W - 36 - tx):
        d.text((tx, yy), ln, font=font(SANS, 19), fill=INK)
        yy += 26

    rule(d, 36, W - 36, 540, 2)
    rule(d, 36, W - 36, 545, 5)

    # ---- grid: five full-width rows, one icon each
    stories = [
        ("chart", "NVIDIA BRINGS BACK ITS CHIEF",
         "Jensen Huang returns as chief executive; shares jump 31% and lift world markets."),
        ("target", "GAZA STRIKES KILL HAMAS SECURITY CHIEF",
         "Israeli air strikes kill Naeem Abu Nahel and six others in Gaza, medics say."),
        ("flame", "INDONESIA FACTORY FIRE TOLL REACHES 26",
         "Rescuers search the burned Banten candy factory as dozens remain missing."),
        ("rocket", "PAKISTAN ASTRONAUT TO FLY ON CHINA'S STATION",
         "Zeeshan Ali will be the first foreign astronaut aboard the Tiangong space station."),
        ("scales", "SPAIN AMNESTIES PUIGDEMONT",
         "The Supreme Court applies the amnesty law to the exiled former Catalan president."),
    ]
    yy = 564
    for icon, head, summ in stories:
        ICONS[icon](d, 36, yy + 2, 50, NAVY)
        d.text((104, yy), head, font=font(SANS_B, 21), fill=INK)
        d.text((104, yy + 28), summ, font=font(SANS, 16), fill=(52, 48, 40))
        yy += 64

    # ---- also today strip
    d.rectangle([36, 900, W - 36, 962], fill=NAVY)
    d.text((52, 910), "ALSO TODAY", font=font(SANS_B, 17), fill=GOLD)
    items = ("NEPAL: 5.6 quake shakes hills near the China border  •  "
             "NATO vows to defend space after reports of a Russian nuclear satellite  •  "
             "GHANA win the amputee football World Cup")
    al = wrap(d, items, font(SANS, 15), W - 72 - 150)
    y2 = 910
    for ln in al[:2]:
        d.text((52 + 130, y2), ln, font=font(SANS, 15), fill=(255, 255, 255))
        y2 += 20

    # footer
    d.text((W // 2, 974), "Sources: Reuters · AP · BBC · The Guardian · Kyiv Independent",
           font=font(SANS, 12), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    build()
