#!/usr/bin/env python3
"""Front page for Monday 23 November 2026, drawn with Pillow.

Six stories from the day are laid out as a newspaper front page on a
1024 by 1024 canvas: a hero block for the top story, a two-by-two grid
for four more, and a wide strip for the last. Run from this directory:

    python3 draw_poster.py

and the finished page is saved as entry.png next to this script.
"""

from PIL import Image, ImageDraw, ImageFont

CANVAS = (1024, 1024)
BACKGROUND = (250, 247, 240)
CARD = (255, 255, 255)
CARD_EDGE = (212, 208, 200)
BODY_INK = (52, 50, 47)
HEAD_INK = (20, 20, 20)
FOOT_INK = (90, 88, 84)
MASTHEAD = (15, 42, 74)
RULE = (198, 158, 62)

DEJAVU = "/usr/share/fonts/truetype/dejavu"


def typeface(filename, points):
    return ImageFont.truetype(DEJAVU + "/" + filename, points)


SERIF_BOLD = lambda pts: typeface("DejaVuSerif-Bold.ttf", pts)
SANS_BOLD = lambda pts: typeface("DejaVuSans-Bold.ttf", pts)
SANS = lambda pts: typeface("DejaVuSans.ttf", pts)


def fit_lines(pen, sentence, face, max_px):
    """Split a sentence into lines no wider than max_px."""
    wrapped = []
    current = ""
    for word in sentence.split():
        candidate = (current + " " + word).strip()
        if pen.textlength(candidate, font=face) <= max_px:
            current = candidate
        else:
            if current:
                wrapped.append(current)
            current = word
    if current:
        wrapped.append(current)
    return wrapped


# Each story: accent colour, section label, headline, deck.
HERO = {
    "tone": (179, 38, 30),
    "tag": "TOP STORY  ·  SECURITY  ·  BRUSSELS",
    "head": "NATO meets in emergency session over missiles in Poland",
    "deck": "Three Russian cruise missiles fell in Poland on Friday; the "
            "alliance's top council meets in Brussels to weigh its response.",
}

NEWS = [
    {
        "tone": (176, 92, 8),
        "tag": "WAR  ·  UKRAINE",
        "head": "Russian strikes on Kyiv region kill at least 15",
        "deck": "Rescuers dug through a collapsed apartment block in Dymer "
                "on Monday.",
    },
    {
        "tone": (29, 78, 216),
        "tag": "POLITICS  ·  WASHINGTON",
        "head": "Democrats clinch 258 House seats, biggest majority since 1992",
        "deck": "A North Carolina win gives the party its largest majority "
                "in 34 years.",
    },
    {
        "tone": (109, 40, 217),
        "tag": "SCIENCE  ·  SAN FRANCISCO",
        "head": "AI-aided proof of the Riemann Hypothesis claimed",
        "deck": "Levent Alpöge says he proved the 167-year-old problem "
                "with Claude.",
    },
    {
        "tone": (14, 116, 144),
        "tag": "ECONOMY  ·  SEOUL",
        "head": "South Korea's exports pass $1 trillion for the first time",
        "deck": "Driven by AI chip demand, annual exports topped $1 trillion "
                "on Monday.",
    },
]

STRIP = {
    "tone": (21, 128, 61),
    "tag": "MONEY  ·  WASHINGTON",
    "head": "Trump signs Common Cents Act; the penny ends after 232 years",
    "deck": "The president signed the bill ending production of the one-cent "
            "coin, closing a run of more than two centuries.",
}


def hero_card(pen, left, top, width, height, item):
    pen.rectangle([left, top, left + width, top + height],
                  fill=CARD, outline=CARD_EDGE, width=2)
    pen.rectangle([left, top, left + 10, top + height], fill=item["tone"])
    inner_left = left + 34
    inner_width = width - 58
    cursor = top + 20
    pen.text((inner_left, cursor), item["tag"],
             font=SANS_BOLD(21), fill=item["tone"])
    cursor += 34
    for line in fit_lines(pen, item["head"], SERIF_BOLD(38),
                          inner_width)[:2]:
        pen.text((inner_left, cursor), line, font=SERIF_BOLD(38),
                 fill=HEAD_INK)
        cursor += 48
    cursor += 4
    for line in fit_lines(pen, item["deck"], SANS(23), inner_width)[:2]:
        pen.text((inner_left, cursor), line, font=SANS(23), fill=BODY_INK)
        cursor += 30


def story_card(pen, left, top, width, height, item):
    pen.rectangle([left, top, left + width, top + height],
                  fill=CARD, outline=CARD_EDGE, width=2)
    pen.rectangle([left, top, left + width, top + 7], fill=item["tone"])
    inner_left = left + 20
    inner_width = width - 40
    cursor = top + 16
    pen.text((inner_left, cursor), item["tag"],
             font=SANS_BOLD(19), fill=item["tone"])
    cursor += 30
    for line in fit_lines(pen, item["head"], SANS_BOLD(28),
                          inner_width)[:2]:
        pen.text((inner_left, cursor), line, font=SANS_BOLD(28),
                 fill=HEAD_INK)
        cursor += 36
    cursor += 4
    for line in fit_lines(pen, item["deck"], SANS(21), inner_width)[:2]:
        pen.text((inner_left, cursor), line, font=SANS(21), fill=BODY_INK)
        cursor += 27


def strip_card(pen, left, top, width, height, item):
    pen.rectangle([left, top, left + width, top + height],
                  fill=CARD, outline=CARD_EDGE, width=2)
    pen.rectangle([left, top, left + 10, top + height], fill=item["tone"])
    inner_left = left + 34
    inner_width = width - 58
    cursor = top + 14
    pen.text((inner_left, cursor), item["tag"],
             font=SANS_BOLD(19), fill=item["tone"])
    cursor += 30
    for line in fit_lines(pen, item["head"], SANS_BOLD(29),
                          inner_width)[:2]:
        pen.text((inner_left, cursor), line, font=SANS_BOLD(29),
                 fill=HEAD_INK)
        cursor += 37
    cursor += 2
    for line in fit_lines(pen, item["deck"], SANS(21), inner_width)[:2]:
        pen.text((inner_left, cursor), line, font=SANS(21), fill=BODY_INK)
        cursor += 27


def build_page():
    page = Image.new("RGB", CANVAS, BACKGROUND)
    pen = ImageDraw.Draw(page)

    # Masthead: paper name, the date, and a gold rule.
    pen.rectangle([0, 0, 1024, 148], fill=MASTHEAD)
    pen.text((40, 20), "THE WORLD IN ONE DAY", font=SANS_BOLD(26),
             fill=RULE)
    pen.text((40, 52), "Monday, 23 November 2026",
             font=SERIF_BOLD(56), fill=(255, 255, 255))
    pen.text((1024 - 40 - pen.textlength("SIX STORIES", font=SANS_BOLD(22)),
              26), "SIX STORIES", font=SANS_BOLD(22), fill=RULE)
    pen.rectangle([40, 132, 1024 - 40, 135], fill=RULE)

    outer, gutter = 36, 16
    # Hero block: the top story, full width.
    hero_card(pen, outer, 160, 1024 - 2 * outer, 216, HERO)

    # Four stories in a 2-by-2 grid.
    card_w = (1024 - 2 * outer - gutter) // 2
    card_h = 176
    first_row = 388
    for index, item in enumerate(NEWS):
        col = index % 2
        row = index // 2
        story_card(pen,
                   outer + col * (card_w + gutter),
                   first_row + row * (card_h + gutter),
                   card_w, card_h, item)

    # Wide strip for the last story.
    strip_card(pen, outer, 764, 1024 - 2 * outer, 172, STRIP)

    # Footer line under the grid.
    rule_y = 950
    pen.rectangle([outer, rule_y, 1024 - outer, rule_y + 2],
                  fill=(180, 176, 168))
    pen.text((outer, rule_y + 10),
             "World news of Monday 23 November 2026 — six stories, "
             "as reported on the day.",
             font=SANS(21), fill=FOOT_INK)
    return page


if __name__ == "__main__":
    build_page().save("entry.png", "PNG")
    print("wrote entry.png")
