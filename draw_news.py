#!/usr/bin/env python3
"""Draw the news-image-20261118 entry: a 1024x1024 infographic summing
up Wednesday 18 November 2026's world news.

Stories (all verified against Reuters, BBC, BusinessWorld, AJP and
India Meteorological Department reporting):
  1. Trump meets Marcos Jr. in Manila, then flies to Shenzhen.
  2. The APEC leaders' meeting opens in Shenzhen (18-19 Nov).
  3. Cyclone Akvan becomes a severe cyclonic storm; Andhra Pradesh braces.
  4. Day 264 of the US-Iran war: Hormuz tanker attacks go on.
  5. (strip) Northern Ireland reach the Nations League top tier.
  6. (strip) Tomorrow: Trump, Xi and Putin meet in Shenzhen.

Build time only. Run: python3 draw_news.py  (writes entry.png next
to this file). Uses Pillow and DejaVu fonts; no network.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

NAVY = (11, 29, 51)
NAVY_DARK = (8, 22, 40)
PANEL = (20, 48, 76)
PANEL_ALT = (24, 56, 88)
GOLD = (242, 183, 5)
WHITE = (255, 255, 255)
BODY = (213, 222, 232)
MUTED = (150, 168, 188)
RULE = (242, 183, 5)
RED = (228, 87, 46)
TEAL = (23, 163, 152)
AMBER = (246, 174, 45)
CRIMSON = (196, 69, 54)
GREEN = (46, 160, 90)
BLUE = (46, 134, 171)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MAST = font("DejaVuSans-Bold.ttf", 56)
F_DATE = font("DejaVuSans-Bold.ttf", 38)
F_KICK = font("DejaVuSans-Bold.ttf", 17)
F_HEAD = font("DejaVuSans-Bold.ttf", 31)
F_BODY = font("DejaVuSans.ttf", 22)
F_STRIP_HEAD = font("DejaVuSans-Bold.ttf", 24)
F_STRIP_BODY = font("DejaVuSans.ttf", 21)
F_FOOT = font("DejaVuSans.ttf", 18)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
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


def draw_panel(draw, x, y, w, h, tag, tag_color, headline, body, icon):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=18, fill=PANEL)
    # Tag chip.
    chip_w = draw.textlength(tag, font=F_KICK) + 26
    draw.rounded_rectangle([x + 22, y + 20, x + 22 + chip_w, y + 52],
                           radius=16, fill=tag_color)
    draw.text((x + 35, y + 25), tag, font=F_KICK, fill=WHITE)
    # Simple icon on the right of the tag row.
    icon(draw, x + w - 78, y + 18)
    # Headline.
    lines = wrap(draw, headline, F_HEAD, w - 44)
    ty = y + 66
    for line in lines:
        draw.text((x + 22, ty), line, font=F_HEAD, fill=WHITE)
        ty += 38
    # Body.
    by = ty + 8
    for line in wrap(draw, body, F_BODY, w - 44):
        draw.text((x + 22, by), line, font=F_BODY, fill=BODY)
        by += 29


def icon_plane(draw, x, y):
    # Stylised jet, nose right: fuselage, swept wings, tail fin.
    draw.polygon([(x + 4, y + 26), (x + 46, y + 26), (x + 58, y + 31),
                  (x + 46, y + 36), (x + 4, y + 36)], fill=GOLD)
    draw.polygon([(x + 20, y + 36), (x + 32, y + 36), (x + 26, y + 52),
                  (x + 18, y + 52)], fill=GOLD)
    draw.polygon([(x + 20, y + 26), (x + 30, y + 26), (x + 24, y + 12),
                  (x + 16, y + 12)], fill=GOLD)
    draw.polygon([(x + 4, y + 26), (x + 12, y + 26), (x + 8, y + 14),
                  (x + 2, y + 14)], fill=GOLD)


def icon_towers(draw, x, y):
    # Skyline: three towers with lit windows.
    for bx, bw, bh in [(x + 4, 14, 44), (x + 22, 16, 56), (x + 42, 14, 38)]:
        draw.rectangle([bx, y + 60 - bh, bx + bw, y + 60], fill=TEAL)
        for wy in range(y + 60 - bh + 6, y + 54, 10):
            draw.rectangle([bx + 3, wy, bx + bw - 3, wy + 3], fill=GOLD)


def icon_spiral(draw, x, y):
    # Cyclone: concentric arcs.
    for r, col in [(28, AMBER), (21, WHITE), (14, AMBER), (7, WHITE)]:
        draw.arc([x + 30 - r, y + 30 - r, x + 30 + r, y + 30 + r],
                 start=20, end=300, fill=col, width=4)


def icon_ship(draw, x, y):
    # Tanker: hull, deck, funnel, waves.
    draw.polygon([(x + 2, y + 34), (x + 58, y + 34), (x + 50, y + 52),
                  (x + 10, y + 52)], fill=CRIMSON)
    draw.rectangle([x + 38, y + 20, x + 48, y + 34], fill=WHITE)
    draw.rectangle([x + 12, y + 26, x + 30, y + 34], fill=WHITE)
    for wx in (x + 2, x + 24, x + 46):
        draw.arc([wx, y + 54, wx + 12, y + 62], start=0, end=180,
                 fill=BLUE, width=3)


def main():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # Header band.
    draw.rectangle([0, 0, W, 158], fill=NAVY_DARK)
    draw.rectangle([0, 158, W, 164], fill=RULE)
    draw.text((36, 26), "THE WORLD IN ONE IMAGE", font=F_MAST, fill=WHITE)
    draw.text((36, 98), "WEDNESDAY  18  NOVEMBER  2026",
              font=F_DATE, fill=GOLD)

    # 2x2 story grid.
    gx, gy = 24, 184
    pw, ph = 476, 288
    gap = 24
    stories = [
        ("DIPLOMACY  ·  MANILA", RED,
         "Trump meets Marcos, then flies to Shenzhen",
         "After Quad talks, the US president holds a bilateral with "
         "Ferdinand Marcos Jr. — then on to APEC and Thursday's "
         "trilateral with Xi and Putin.", icon_plane),
        ("TRADE  ·  SHENZHEN", TEAL,
         "APEC leaders' summit opens in China",
         "Leaders gather for the 18–19 November meeting hosted by Xi "
         "Jinping; trade and curbs on China's access to AI chips top "
         "the agenda.", icon_towers),
        ("WEATHER  ·  BAY OF BENGAL", AMBER,
         "Cyclone Akvan turns severe",
         "The storm strengthens over the Bay of Bengal on Wednesday; "
         "Andhra Pradesh braces for heavy rain and 100–110 km/h "
         "winds, landfall due Friday.", icon_spiral),
        ("CONFLICT  ·  STRAIT OF HORMUZ", CRIMSON,
         "War at sea goes on — day 264",
         "Tankers keep being hit near the Strait of Hormuz, a third "
         "US carrier is on station, and indirect US–Iran talks stay "
         "stalled.", icon_ship),
    ]
    for i, (tag, color, head, body, ic) in enumerate(stories):
        x = gx + (i % 2) * (pw + gap)
        y = gy + (i // 2) * (ph + gap)
        draw_panel(draw, x, y, pw, ph, tag, color, head, body, ic)

    # Bottom strip: sport + tomorrow.
    sy = gy + 2 * ph + gap + 12
    draw.rounded_rectangle([gx, sy, W - gx, sy + 118], radius=18,
                           fill=PANEL_ALT)
    draw.text((gx + 22, sy + 14), "SPORT", font=F_STRIP_HEAD, fill=GREEN)
    draw.text((gx + 22, sy + 46),
              "Northern Ireland reach the Nations League top tier for "
              "the first time — 1–1 in Hungary.",
              font=F_STRIP_BODY, fill=BODY)
    draw.text((gx + 22, sy + 76),
              "TOMORROW:  Trump, Xi and Putin meet in Shenzhen.",
              font=F_STRIP_BODY, fill=BODY)

    # Footer.
    fy = H - 56
    draw.rectangle([0, fy - 14, W, H], fill=NAVY_DARK)
    draw.text((36, fy), "Sources: Reuters · BBC · BusinessWorld · IMD — "
              "every story happened or was first reported on 18 Nov 2026.",
              font=F_FOOT, fill=MUTED)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
