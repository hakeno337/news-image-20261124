#!/usr/bin/env python3
"""The World Today — 24 November 2026, second setting. Draws the
illustrated broadsheet entry.png (1024x1024) for the make.fun
news-image-20261124 bounty, revised against the first setting:

- the lead summary now ends well clear of the rule beneath it (in the
  first setting its last line sat on the rule);
- grid headlines and summaries are set larger (24 / 18 px) and every
  summary is tightened until it fits its row on one line, so the page
  still reads at the judge's 300-pixel width;
- the smoke in the lead illustration stays inside its frame, the
  warship gains a bridge tower and a gun turret so it reads as a
  warship, and the naval drone boats are drawn larger with wakes;
- the scales and rocket icons are redrawn to read at small size;
- the ALSO TODAY strip is set larger, on two balanced lines.

Same day's news, same stories, same attributions as the first setting.
Everything is drawn with Pillow from plain shapes and text: no photos,
no network, no copied artwork. Run:  python3 compose.py
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
    """A plain rocket: capsule body, round window, two fins, flame."""
    cx = x + s // 2
    body_w = s // 3
    top, body_bot = y + 2, y + s * 2 // 3
    d.polygon([(cx - body_w // 2, body_bot), (cx - body_w // 2, y + s // 3),
               (cx, top), (cx + body_w // 2, y + s // 3),
               (cx + body_w // 2, body_bot)], fill=col)
    d.ellipse([cx - 5, y + s // 3, cx + 5, y + s // 3 + 10], fill=CREAM)
    d.polygon([(cx - body_w // 2, body_bot - 8), (cx - body_w // 2 - 9, body_bot + 6),
               (cx - body_w // 2, body_bot + 6)], fill=col)
    d.polygon([(cx + body_w // 2, body_bot - 8), (cx + body_w // 2 + 9, body_bot + 6),
               (cx + body_w // 2, body_bot + 6)], fill=col)
    d.polygon([(cx - 6, body_bot + 4), (cx + 6, body_bot + 4),
               (cx, y + s - 2)], fill=ORANGE)


def icon_scales(d, x, y, s, col):
    """Balance scales: post, beam, and two pans hung on chain lines."""
    cx = x + s // 2
    beam_y = y + 10
    d.line([(cx, y + 4), (cx, y + s - 10)], fill=col, width=4)
    d.line([(x + 6, beam_y), (x + s - 6, beam_y)], fill=col, width=4)
    d.ellipse([cx - 4, y, cx + 4, y + 8], fill=col)
    for px in (x + 14, x + s - 14):
        pan_y = y + s - 16
        d.line([(px - 8, beam_y), (px, pan_y), (px + 8, beam_y)], fill=col, width=2)
        d.pieslice([px - 13, pan_y - 6, px + 13, pan_y + 10], 0, 180, fill=col)
    d.line([(x + 8, y + s - 6), (x + s - 8, y + s - 6)], fill=col, width=4)


ICONS = {"chart": icon_chart, "target": icon_target, "flame": icon_flame,
         "rocket": icon_rocket, "scales": icon_scales}


# ------------------------------------------------------- lead illustration
def draw_scene(d, x0, y0, x1, y1):
    """Dusk sea at Benghazi port: a grey warship burning at anchor, naval
    drone boats closing in, smoke over the harbour. Flat shapes only,
    and every shape kept inside the frame."""
    d.rectangle([x0, y0, x1, y1], fill=SKY_TOP)
    horizon = y0 + int((y1 - y0) * 0.48)
    for i in range(6):
        yy = y0 + i * (horizon - y0) // 6
        shade = tuple(int(SKY_TOP[c] + (SKY_BOT[c] - SKY_TOP[c]) * i / 5) for c in range(3))
        d.rectangle([x0, yy, x1, yy + (horizon - y0) // 6 + 1], fill=shade)
    # low sun
    sx, sy, sr = x0 + 92, horizon - 30, 40
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(238, 178, 84))
    d.ellipse([sx - sr + 9, sy - sr + 9, sx + sr - 9, sy + sr - 9],
              fill=(244, 196, 110))
    # distant port skyline
    d.rectangle([x0, horizon - 26, x0 + 130, horizon], fill=(120, 104, 78))
    d.rectangle([x0 + 24, horizon - 46, x0 + 48, horizon], fill=(120, 104, 78))
    d.rectangle([x0 + 78, horizon - 34, x0 + 96, horizon], fill=(120, 104, 78))
    d.rectangle([x1 - 150, horizon - 20, x1 - 30, horizon], fill=(120, 104, 78))
    # sea
    d.rectangle([x0, horizon, x1, y1], fill=SEA)
    d.rectangle([x0, horizon, x1, horizon + 6], fill=SEA_DARK)
    for wy in range(horizon + 16, y1 - 8, 20):
        for wx in range(x0 + 16, x1 - 70, 96):
            d.line([(wx, wy), (wx + 48, wy)], fill=(120, 160, 200), width=2)
    # warship, bow to the right: hull, deck houses, bridge tower, mast,
    # and a forward gun turret, so it reads as a warship at any size
    hx0, hx1 = x0 + 56, x1 - 32
    hy = horizon + 42
    d.polygon([(hx0, hy - 40), (hx1, hy - 40), (hx1 - 32, hy + 10),
               (hx0 + 20, hy + 10)], fill=(52, 54, 58))
    d.polygon([(hx0 + 20, hy + 10), (hx1 - 32, hy + 10), (hx1 - 46, hy + 22),
               (hx0 + 46, hy + 22)], fill=(38, 40, 44))
    d.rectangle([hx0 + 120, hy - 88, hx0 + 330, hy - 40], fill=(66, 68, 72))
    d.rectangle([hx0 + 168, hy - 118, hx0 + 258, hy - 88], fill=(66, 68, 72))
    for wx in range(hx0 + 180, hx0 + 246, 22):
        d.rectangle([wx, hy - 110, wx + 12, hy - 100], fill=(246, 226, 178))
    d.line([(hx0 + 213, hy - 118), (hx0 + 213, hy - 142)], fill=(52, 54, 58), width=6)
    d.line([(hx0 + 213, hy - 142), (hx0 + 248, hy - 128)], fill=(52, 54, 58), width=4)
    # forward gun turret and barrel, clear of the flames amidships
    d.polygon([(hx0 + 348, hy - 40), (hx0 + 356, hy - 58), (hx0 + 404, hy - 58),
               (hx0 + 412, hy - 40)], fill=(66, 68, 72))
    d.line([(hx0 + 404, hy - 52), (hx0 + 448, hy - 62)], fill=(52, 54, 58), width=6)
    # flames and smoke amidships, smoke puffs kept inside the frame
    fx = hx0 + 262
    d.polygon([(fx - 42, hy - 40), (fx - 10, hy - 112), (fx + 6, hy - 70),
               (fx + 26, hy - 118), (fx + 48, hy - 40)], fill=ORANGE)
    d.polygon([(fx - 20, hy - 40), (fx - 2, hy - 84), (fx + 16, hy - 40)], fill=FLAME)
    for sx2, sy2, sr2 in [(fx - 26, y0 + 40, 22), (fx + 22, y0 + 34, 27),
                          (fx + 72, y0 + 42, 23), (fx + 112, y0 + 32, 18)]:
        d.ellipse([sx2 - sr2, sy2 - sr2, sx2 + sr2, sy2 + sr2], fill=(74, 72, 68))
    # drone boats with white wakes, big enough to see closing in and
    # kept clear of the hull above and the frame's bottom edge
    for bx, by in [(x0 + 52, horizon + 96), (x0 + 300, horizon + 100)]:
        d.polygon([(bx, by), (bx + 74, by), (bx + 62, by + 16), (bx + 12, by + 16)],
                  fill=(28, 30, 34))
        d.rectangle([bx + 26, by - 7, bx + 48, by], fill=(28, 30, 34))
        d.line([(bx - 52, by + 15), (bx + 10, by + 15)], fill=(240, 244, 248), width=3)
        d.line([(bx - 36, by + 23), (bx + 22, by + 23)], fill=(240, 244, 248), width=2)
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
    spaced(d, (W // 2, 30), "ONE DAY · ONE PAGE · THE WORLD", font(SANS_B, 14), GREY, 4)
    d.text((W // 2, 46), "The World Today", font=font(SERIF_B, 62),
           fill=INK, anchor="ma")
    rule(d, 36, W - 36, 120, 2)
    rule(d, 36, W - 36, 125, 5)

    # date band
    d.rectangle([36, 138, W - 36, 200], fill=INK)
    d.text((W // 2, 148), "TUESDAY · 24 NOVEMBER · 2026", font=font(SANS_B, 40),
           fill=(255, 255, 255), anchor="ma")

    # ---- lead: illustration left, words right; the summary wraps to
    # four lines and ends at about y 506, clear of the rule at 524
    draw_scene(d, 36, 216, 560, 480)
    tx = 584
    spaced_left(d, tx, 222, "THE WAR AT SEA", font(SANS_B, 16), RED, 2)
    spaced_left(d, tx, 245, "BENGHAZI, LIBYA", font(SANS_B, 16), RED, 2)
    yy = 268
    for ln in ["UKRAINE SINKS", "RUSSIAN WARSHIP", "OFF LIBYA"]:
        d.text((tx, yy), ln, font=font(SERIF_B, 40), fill=INK)
        yy += 46
    summary = ("Kyiv says seven naval drones sank the corvette Merkury and "
               "hit a weapons cargo ship in Benghazi port — a strike "
               "Ukraine calls self-defence.")
    yy += 6
    for ln in wrap(d, summary, font(SANS, 19), W - 36 - tx):
        d.text((tx, yy), ln, font=font(SANS, 19), fill=INK)
        yy += 25

    rule(d, 36, W - 36, 524, 2)
    rule(d, 36, W - 36, 529, 5)

    # ---- grid: five full-width rows, one icon each; each summary is
    # written to fit its row on a single line at 18 px
    stories = [
        ("chart", "NVIDIA BRINGS BACK ITS CHIEF",
         "Jensen Huang returns as chief executive; shares jump 31%, lifting world markets."),
        ("target", "GAZA STRIKES KILL HAMAS SECURITY CHIEF",
         "Israeli air strikes kill Naeem Abu Nahel and six others in Gaza, medics say."),
        ("flame", "INDONESIA FACTORY FIRE TOLL REACHES 26",
         "Rescuers search the burned Banten candy factory as dozens remain missing."),
        ("rocket", "PAKISTAN ASTRONAUT TO FLY ON CHINA'S STATION",
         "Zeeshan Ali will be the first foreign astronaut aboard the Tiangong station."),
        ("scales", "SPAIN AMNESTIES PUIGDEMONT",
         "The Supreme Court applies the amnesty law to the exiled Catalan ex-president."),
    ]
    yy = 548
    for icon, head, summ in stories:
        ICONS[icon](d, 36, yy + 2, 56, NAVY)
        d.text((108, yy), head, font=font(SANS_B, 24), fill=INK)
        d.text((108, yy + 31), summ, font=font(SANS, 18), fill=(52, 48, 40))
        yy += 68

    # ---- also today strip: two balanced lines at 17 px
    d.rectangle([36, 902, W - 36, 966], fill=NAVY)
    d.text((52, 912), "ALSO TODAY", font=font(SANS_B, 17), fill=GOLD)
    # the three items, split by hand into two lines measured to fit the
    # strip beside the label (715 and 763 of the 784 px available)
    lines = [
        "NEPAL: 5.6 quake shakes hills near the China border  •  NATO vows to defend space",
        "after reports of a Russian nuclear satellite  •  GHANA win the amputee football World Cup",
    ]
    y2 = 912
    for ln in lines:
        d.text((52 + 138, y2), ln, font=font(SANS, 17), fill=(255, 255, 255))
        y2 += 24

    # footer
    d.text((W // 2, 978), "Sources: Reuters · AP · BBC · The Guardian · Kyiv Independent",
           font=font(SANS, 12), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    build()
