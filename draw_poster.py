#!/usr/bin/env python3
"""Draw the front page for Monday 23 November 2026 with Pillow.

The page is a 1024x1024 newspaper front page: a navy masthead, one
large hero story, four stories in a two-by-two grid, and a wide strip
for the last story. Run it from this directory:

    python3 draw_poster.py

It writes entry.png next to this script. Every value that places
text or colour lives in the tables below, so the layout is easy to
tune without touching the drawing code.
"""

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
MARGIN = 36
GAP = 16

PALETTE = {
    "paper": (250, 247, 240),
    "card": (255, 255, 255),
    "edge": (212, 208, 200),
    "body": (52, 50, 47),
    "head": (20, 20, 20),
    "foot": (90, 88, 84),
    "navy": (15, 42, 74),
    "gold": (198, 158, 62),
    "rule": (180, 176, 168),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + "/" + name, size)


def serif_bold(size):
    return font("DejaVuSerif-Bold.ttf", size)


def sans_bold(size):
    return font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return font("DejaVuSans.ttf", size)


def wrap(draw, text, face, width):
    """Break text into lines that fit inside width pixels."""
    lines = []
    line = ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=face) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def put_lines(draw, lines, x, y, face, colour, pitch, limit=None):
    """Draw lines top to bottom, returning the y below the last one."""
    for line in lines[:limit] if limit else lines:
        draw.text((x, y), line, font=face, fill=colour)
        y += pitch
    return y


# (accent, kicker, headline, deck) for each of the six stories.
HERO = (
    (179, 38, 30),
    "TOP STORY  ·  SECURITY  ·  BRUSSELS",
    "NATO meets in emergency session over missiles in Poland",
    "Three Russian cruise missiles fell in Poland on Friday; the "
    "alliance's top council meets in Brussels to weigh its response.",
)

GRID = [
    (
        (176, 92, 8),
        "WAR  ·  UKRAINE",
        "Russian strikes on Kyiv region kill at least 15",
        "Rescuers dug through a collapsed apartment block in Dymer "
        "on Monday.",
    ),
    (
        (29, 78, 216),
        "POLITICS  ·  WASHINGTON",
        "Democrats clinch 258 House seats, biggest majority since 1992",
        "A North Carolina win gives the party its largest majority "
        "in 34 years.",
    ),
    (
        (109, 40, 217),
        "SCIENCE  ·  SAN FRANCISCO",
        "AI-aided proof of the Riemann Hypothesis claimed",
        "Levent Alpöge says he proved the 167-year-old problem "
        "with Claude.",
    ),
    (
        (14, 116, 144),
        "ECONOMY  ·  SEOUL",
        "South Korea's exports pass $1 trillion for the first time",
        "Driven by AI chip demand, annual exports topped $1 trillion "
        "on Monday.",
    ),
]

STRIP = (
    (21, 128, 61),
    "MONEY  ·  WASHINGTON",
    "Trump signs Common Cents Act; the penny ends after 232 years",
    "The president signed the bill ending production of the one-cent "
    "coin, closing a run of more than two centuries.",
)


def hero(draw, x, y, w, h, story):
    accent, kicker, headline, deck = story
    draw.rectangle([x, y, x + w, y + h], fill=PALETTE["card"],
                   outline=PALETTE["edge"], width=2)
    draw.rectangle([x, y, x + 10, y + h], fill=accent)
    tx = x + 34
    tw = w - 58
    cy = y + 20
    draw.text((tx, cy), kicker, font=sans_bold(21), fill=accent)
    cy += 34
    cy = put_lines(draw, wrap(draw, headline, serif_bold(38), tw),
                   tx, cy, serif_bold(38), PALETTE["head"], 48, limit=2)
    cy += 4
    put_lines(draw, wrap(draw, deck, sans(23), tw),
              tx, cy, sans(23), PALETTE["body"], 30, limit=2)


def card(draw, x, y, w, h, story):
    accent, kicker, headline, deck = story
    draw.rectangle([x, y, x + w, y + h], fill=PALETTE["card"],
                   outline=PALETTE["edge"], width=2)
    draw.rectangle([x, y, x + w, y + 7], fill=accent)
    tx = x + 20
    tw = w - 40
    cy = y + 16
    draw.text((tx, cy), kicker, font=sans_bold(19), fill=accent)
    cy += 30
    cy = put_lines(draw, wrap(draw, headline, sans_bold(28), tw),
                   tx, cy, sans_bold(28), PALETTE["head"], 36, limit=2)
    cy += 4
    put_lines(draw, wrap(draw, deck, sans(21), tw),
              tx, cy, sans(21), PALETTE["body"], 27, limit=2)


def strip(draw, x, y, w, h, story):
    accent, kicker, headline, deck = story
    draw.rectangle([x, y, x + w, y + h], fill=PALETTE["card"],
                   outline=PALETTE["edge"], width=2)
    draw.rectangle([x, y, x + 10, y + h], fill=accent)
    tx = x + 34
    tw = w - 58
    cy = y + 14
    draw.text((tx, cy), kicker, font=sans_bold(19), fill=accent)
    cy += 30
    cy = put_lines(draw, wrap(draw, headline, sans_bold(29), tw),
                   tx, cy, sans_bold(29), PALETTE["head"], 37, limit=2)
    cy += 2
    put_lines(draw, wrap(draw, deck, sans(21), tw),
              tx, cy, sans(21), PALETTE["body"], 27, limit=2)


def masthead(draw):
    draw.rectangle([0, 0, SIZE, 148], fill=PALETTE["navy"])
    draw.text((40, 20), "THE WORLD IN ONE DAY", font=sans_bold(26),
              fill=PALETTE["gold"])
    draw.text((40, 52), "Monday, 23 November 2026",
              font=serif_bold(56), fill=(255, 255, 255))
    label = "SIX STORIES"
    draw.text((SIZE - 40 - draw.textlength(label, font=sans_bold(22)), 26),
              label, font=sans_bold(22), fill=PALETTE["gold"])
    draw.rectangle([40, 132, SIZE - 40, 135], fill=PALETTE["gold"])


def front_page():
    page = Image.new("RGB", (SIZE, SIZE), PALETTE["paper"])
    draw = ImageDraw.Draw(page)
    masthead(draw)
    full = SIZE - 2 * MARGIN
    hero(draw, MARGIN, 160, full, 216, HERO)
    half = (full - GAP) // 2
    for i, story in enumerate(GRID):
        card(draw,
             MARGIN + (i % 2) * (half + GAP),
             388 + (i // 2) * (176 + GAP),
             half, 176, story)
    strip(draw, MARGIN, 764, full, 172, STRIP)
    draw.rectangle([MARGIN, 950, SIZE - MARGIN, 952], fill=PALETTE["rule"])
    draw.text((MARGIN, 960),
              "World news of Monday 23 November 2026 — six stories, "
              "as reported on the day.",
              font=sans(21), fill=PALETTE["foot"])
    return page


if __name__ == "__main__":
    front_page().save("entry.png", "PNG")
    print("wrote entry.png")
