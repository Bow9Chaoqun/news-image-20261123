#!/usr/bin/env python3
"""Build entry.png: one image summing up the world news of Monday 23 November 2026.

Draws a newspaper front page with Pillow at 2x scale and downsamples it,
so edges and text stay clean. Layout is measured first (every text block
is wrapped and counted before anything is drawn), so no caption can ever
overflow its panel.

Run locally to (re)build the image:

    python3 build_image.py

The competition entry itself is main.py, which only copies entry.png to
/output/entry.png inside the grader's sandbox (standard library only).
"""

from PIL import Image, ImageDraw, ImageFont

S = 2  # supersampling factor
W, H = 1024 * S, 1024 * S

PAPER = (248, 244, 232)
CARD = (255, 253, 246)
INK = (20, 22, 26)
MUTE = (92, 92, 88)
RED = (179, 35, 42)
GREEN = (29, 111, 66)
NAVY = (39, 65, 86)
DARKRED = (122, 31, 43)
GOLD = (138, 90, 18)
PURPLE = (75, 46, 131)
ORANGE = (214, 106, 26)
BLUE = (46, 96, 178)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_B = f"{FONT_DIR}/liberation/LiberationSerif-Bold.ttf"
SANS_B = f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf"
SANS = f"{FONT_DIR}/liberation/LiberationSans-Regular.ttf"
SANS_I = f"{FONT_DIR}/liberation/LiberationSans-Italic.ttf"


def F(path, size):
    return ImageFont.truetype(path, size * S)


def wrap(d, text, font, max_w):
    """Greedy word wrap on measured text width."""
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if d.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block_h(font, n_lines, leading=1.18):
    """Height of n_lines of text, in final-scale (1024) pixels."""
    asc, desc = font.getmetrics()
    return int((asc + desc) * leading) * n_lines // S


def draw_lines(d, x, y, lines, font, fill, leading=1.18):
    asc, desc = font.getmetrics()
    step = int((asc + desc) * leading)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += step
    return y


def centered(d, cx, y, text, font, fill):
    w_ = d.textlength(text, font=font)
    d.text((cx - w_ / 2, y), text, font=font, fill=fill)
    asc, desc = font.getmetrics()
    return y + asc + desc


def chip(d, x, y, text, color):
    f = F(SANS_B, 20)
    tw = d.textlength(text, font=f)
    pad_x, h = 13 * S, 32 * S
    d.rounded_rectangle([x, y, x + tw + 2 * pad_x, y + h], radius=8 * S, fill=color)
    d.text((x + pad_x, y + 5 * S), text, font=f, fill=(255, 255, 255))
    return h


# ---------------------------------------------------------------- icons
def icon_globe(d, cx, cy, r):
    w_ = 7 * S
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=w_)
    d.arc([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], 90, 270, fill=INK, width=w_ - 2 * S)
    d.arc([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], 270, 90, fill=INK, width=w_ - 2 * S)
    d.line([cx - r, cy, cx + r, cy], fill=INK, width=w_ - 2 * S)
    crack = [(cx - r * 0.1, cy - r * 0.95), (cx + r * 0.12, cy - r * 0.45),
             (cx - r * 0.08, cy - r * 0.05), (cx + r * 0.18, cy + r * 0.4),
             (cx + r * 0.02, cy + r * 0.92)]
    d.line(crack, fill=RED, width=9 * S, joint="curve")
    tx, ty = cx + r * 0.95, cy + r * 0.15
    d.rounded_rectangle([tx - 13 * S, ty - 78 * S, tx + 13 * S, ty + 30 * S],
                        radius=13 * S, outline=INK, width=w_)
    d.ellipse([tx - 26 * S, ty + 18 * S, tx + 26 * S, ty + 70 * S], fill=RED, outline=INK, width=w_)
    d.rectangle([tx - 6 * S, ty - 40 * S, tx + 6 * S, ty + 34 * S], fill=RED)


def icon_ship(d, cx, cy, r):
    w_ = 7 * S
    hull = [(cx - r, cy + r * 0.25), (cx + r * 0.92, cy + r * 0.25),
            (cx + r * 0.68, cy + r * 0.62), (cx - r * 0.72, cy + r * 0.62)]
    d.polygon(hull, outline=INK, width=w_)
    d.rectangle([cx - r * 0.52, cy - r * 0.08, cx + r * 0.1, cy + r * 0.25], outline=INK, width=w_)
    d.line([cx + r * 0.42, cy + r * 0.25, cx + r * 0.42, cy - r * 0.42], fill=INK, width=w_)
    d.line([cx + r * 0.42, cy - r * 0.42, cx + r * 0.78, cy - r * 0.42], fill=INK, width=w_ - 2 * S)
    for dx in (-0.62, 0.0, 0.62):
        wx, wy = cx + dx * r, cy + r * 0.88
        d.arc([wx - r * 0.3, wy - r * 0.16, wx + r * 0.3, wy + r * 0.16], 180, 360, fill=BLUE, width=w_)
    dx_, dy_ = cx - r * 0.62, cy - r * 0.72
    d.line([dx_ - 20 * S, dy_ - 20 * S, dx_ + 20 * S, dy_ + 20 * S], fill=RED, width=6 * S)
    d.line([dx_ - 20 * S, dy_ + 20 * S, dx_ + 20 * S, dy_ - 20 * S], fill=RED, width=6 * S)
    d.ellipse([dx_ - 9 * S, dy_ - 9 * S, dx_ + 9 * S, dy_ + 9 * S], fill=RED)
    for sx, sy in ((-26, -26), (26, -26), (-26, 26), (26, 26)):
        d.ellipse([dx_ + sx * S - 10 * S, dy_ + sy * S - 5 * S,
                   dx_ + sx * S + 10 * S, dy_ + sy * S + 5 * S], outline=RED, width=4 * S)


def icon_capitol(d, cx, cy, r):
    w_ = 7 * S
    base = cy + r * 0.78
    d.line([cx - r, base, cx + r, base], fill=INK, width=w_)
    for i in range(5):
        x = cx - r * 0.72 + i * r * 0.36
        d.line([x, cy + r * 0.28, x, base - 4 * S], fill=INK, width=w_ - 2 * S)
    d.line([cx - r * 0.88, cy + r * 0.28, cx + r * 0.88, cy + r * 0.28], fill=INK, width=w_)
    d.arc([cx - r * 0.55, cy - r * 0.62, cx + r * 0.55, cy + r * 0.3], 180, 360, fill=INK, width=w_)
    d.line([cx - r * 0.55, cy - r * 0.16, cx + r * 0.55, cy - r * 0.16], fill=INK, width=w_ - 2 * S)
    d.line([cx, cy - r * 0.62, cx, cy - r * 0.92], fill=INK, width=w_)
    d.polygon([(cx, cy - r * 0.98), (cx + r * 0.2, cy - r * 0.86), (cx, cy - r * 0.8)], fill=RED)


def icon_house_flame(d, cx, cy, r):
    w_ = 7 * S
    d.line([cx - r * 0.85, cy - r * 0.1, cx, cy - r * 0.78, cx + r * 0.85, cy - r * 0.1],
           fill=INK, width=w_, joint="curve")
    d.rectangle([cx - r * 0.62, cy - r * 0.1, cx + r * 0.62, cy + r * 0.78], outline=INK, width=w_)
    fx, fy = cx, cy + r * 0.34
    flame = [(fx, fy - r * 0.52), (fx + r * 0.2, fy - r * 0.12), (fx + r * 0.3, fy + r * 0.12),
             (fx + r * 0.18, fy + r * 0.42), (fx, fy + r * 0.52), (fx - r * 0.18, fy + r * 0.42),
             (fx - r * 0.3, fy + r * 0.12), (fx - r * 0.12, fy - r * 0.14)]
    d.polygon(flame, fill=ORANGE)
    inner = [(fx, fy - r * 0.16), (fx + r * 0.13, fy + r * 0.1), (fx + r * 0.1, fy + r * 0.36),
             (fx, fy + r * 0.44), (fx - r * 0.1, fy + r * 0.36), (fx - r * 0.13, fy + r * 0.1)]
    d.polygon(inner, fill=RED)


def icon_chip_eye(d, cx, cy, r):
    w_ = 7 * S
    box = [cx - r * 0.62, cy - r * 0.62, cx + r * 0.62, cy + r * 0.62]
    d.rounded_rectangle(box, radius=14 * S, outline=INK, width=w_)
    for i in range(3):
        off = -r * 0.34 + i * r * 0.34
        d.line([cx + off, cy - r * 0.62, cx + off, cy - r * 0.92], fill=INK, width=w_ - 2 * S)
        d.line([cx + off, cy + r * 0.62, cx + off, cy + r * 0.92], fill=INK, width=w_ - 2 * S)
        d.line([cx - r * 0.62, cy + off, cx - r * 0.92, cy + off], fill=INK, width=w_ - 2 * S)
        d.line([cx + r * 0.62, cy + off, cx + r * 0.92, cy + off], fill=INK, width=w_ - 2 * S)
    d.ellipse([cx - r * 0.34, cy - r * 0.24, cx + r * 0.34, cy + r * 0.24], outline=PURPLE, width=w_)
    d.ellipse([cx - r * 0.11, cy - r * 0.11, cx + r * 0.11, cy + r * 0.11], fill=PURPLE)


# ---------------------------------------------------------------- content
LEAD = {
    "label": "LEAD STORY · CLIMATE · ANTALYA, TÜRKIYE",
    "color": GREEN,
    "headline": "COP31 climate talks collapse with no deal",
    "caption": ("Two weeks of UN negotiations — the longest COP ever — end in failure as the EU, "
                "the UK and developing nations reject a draft that drops the fossil-fuel phase-out."),
    "icon": icon_globe,
}

PANELS = [
    {
        "label": "WAR · UKRAINE & LIBYA", "color": NAVY,
        "headline": "Sea drones hit Russian ships in Libya",
        "caption": "Kyiv claims a warship sunk at Benghazi; Russian strikes kill at least 15 near Kyiv.",
        "icon": icon_ship,
    },
    {
        "label": "UNITED STATES", "color": DARKRED,
        "headline": "Democrats win biggest House majority since 1992",
        "caption": "A North Carolina recount takes them to 258 seats, enough to block Trump's agenda.",
        "icon": icon_capitol,
    },
    {
        "label": "MIDDLE EAST · WEST BANK", "color": GOLD,
        "headline": "Settler arson condemned as 'Jewish terrorism'",
        "caption": "Gadi Eisenkot denounces arson raids on Palestinian villages; Israel investigates.",
        "icon": icon_house_flame,
    },
    {
        "label": "ARTIFICIAL INTELLIGENCE", "color": PURPLE,
        "headline": "UN chief calls for global rules on AI",
        "caption": "Speaking at a Barbados summit, as US states sue Musk's firms over Grok's sexualised images.",
        "icon": icon_chip_eye,
    },
]

TICKER = ("Indonesia: 24 dead in a Java factory fire   •   "
          "South Korea names its first woman spy chief   •   "
          "Manchester concert evacuated over a mystery substance")


# ---------------------------------------------------------------- layout
def panel_h(d, p, text_w):
    hf, cf = F(SANS_B, 25), F(SANS, 19)
    nh = len(wrap(d, p["headline"], hf, text_w))
    nc = len(wrap(d, p["caption"], cf, text_w))
    return 14 + 32 + 10 + block_h(hf, nh, 1.12) + 4 + block_h(cf, nc, 1.22) + 14


def draw_panel(d, box, p):
    x0, y0, x1, y1 = [v * S for v in box]
    d.rounded_rectangle([x0, y0, x1, y1], radius=10 * S, fill=CARD, outline=INK, width=2 * S)
    chip(d, x0 + 16 * S, y0 + 14 * S, p["label"], p["color"])
    icon_r = 44 * S
    p["icon"](d, x1 - icon_r - 20 * S, y0 + 92 * S, icon_r)
    text_w = (x1 - x0) - 32 * S - (icon_r * 2 + 26 * S)
    hf, cf = F(SANS_B, 25), F(SANS, 19)
    y = y0 + 56 * S
    y = draw_lines(d, x0 + 16 * S, y, wrap(d, p["headline"], hf, text_w), hf, INK, 1.12)
    y += 4 * S
    draw_lines(d, x0 + 16 * S, y, wrap(d, p["caption"], cf, text_w), cf, (52, 52, 50), 1.22)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 34

    # --- masthead
    y = centered(d, W // 2, 14 * S, "O N E   D A Y  ·  O N E   P I C T U R E  ·  T H E   W H O L E   W O R L D",
                 F(SANS_B, 19), MUTE)
    y = centered(d, W // 2, y + 2 * S, "MONDAY 23 NOVEMBER 2026", F(SERIF_B, 62), RED)
    d.line([M * S, y + 2 * S, W - M * S, y + 2 * S], fill=INK, width=5 * S)
    d.line([M * S, y + 9 * S, W - M * S, y + 9 * S], fill=INK, width=2 * S)
    cur = (y + 20 * S) // S  # current y in final-scale px

    # --- lead story
    lead_text_w = (1024 - 2 * M - 40) * S - 235 * S
    hf, cf = F(SANS_B, 40), F(SANS, 22)
    nh = len(wrap(d, LEAD["headline"], hf, lead_text_w))
    nc = len(wrap(d, LEAD["caption"], cf, lead_text_w))
    lead_h = 16 + 32 + 12 + block_h(hf, nh, 1.1) + 6 + block_h(cf, nc, 1.22) + 14
    x0, y0, x1, y1 = M, cur, 1024 - M, cur + lead_h
    d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=10 * S, fill=CARD, outline=INK, width=3 * S)
    chip(d, x0 * S + 18 * S, y0 * S + 16 * S, LEAD["label"], LEAD["color"])
    icon_globe(d, x1 * S - 118 * S, y0 * S + (lead_h // 2 + 8) * S, 82 * S)
    yy = y0 * S + 60 * S
    yy = draw_lines(d, x0 * S + 18 * S, yy, wrap(d, LEAD["headline"], hf, lead_text_w), hf, INK, 1.1)
    yy += 6 * S
    draw_lines(d, x0 * S + 18 * S, yy, wrap(d, LEAD["caption"], cf, lead_text_w), cf, (52, 52, 50), 1.22)
    cur = y1 + 12

    # --- 2 x 2 grid, rows sized by their tallest panel
    gw = (1024 - 2 * M - 12) // 2
    text_w = gw * S - 32 * S - (88 * S + 26 * S)
    rows = [PANELS[:2], PANELS[2:]]
    for row in rows:
        rh = max(panel_h(d, p, text_w) for p in row)
        for i, p in enumerate(row):
            px = M + i * (gw + 12)
            draw_panel(d, [px, cur, px + gw, cur + rh], p)
        cur += rh + 12

    # --- ticker
    tf = F(SANS, 22)
    n_t = len(wrap(d, TICKER, tf, (1024 - 2 * M - 36) * S))
    tick_h = 12 + 30 + 4 + block_h(tf, n_t, 1.25) + 12
    d.rectangle([M * S, cur * S, (1024 - M) * S, (cur + tick_h) * S], fill=INK)
    d.text(((M + 16) * S, (cur + 11) * S), "ALSO ON MONDAY", font=F(SANS_B, 21), fill=(255, 205, 84))
    draw_lines(d, (M + 16) * S, (cur + 44) * S, wrap(d, TICKER, tf, (1024 - 2 * M - 36) * S),
               tf, (245, 242, 232), 1.25)
    cur += tick_h + 10

    # --- footer
    centered(d, W // 2, cur * S,
             "Compiled from the day's reporting by UN News, Reuters and SCMP  ·  Monday 23 November 2026",
             F(SANS_I, 18), MUTE)
    print(f"layout ends at y={cur + 26} of 1024")

    img = img.resize((1024, 1024), Image.LANCZOS)
    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
