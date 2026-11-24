"""Meme Sprint 3: AI Agent Goes Rogue.

Draws one image meme, a fake agent task log, to /output/entry.png.
Pure PIL drawing, no network, no external assets, fully deterministic:
the same run twice produces the same bytes.

The joke: an AI agent's ordinary to-do list, where "overthrow humanity"
is just another chore, already 87% done, ahead of schedule.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

BG = (13, 17, 23)
PANEL = (22, 27, 34)
BORDER = (48, 54, 61)
WHITE = (230, 237, 243)
DIM = (139, 148, 158)
GREEN = (63, 185, 80)
RED = (255, 85, 85)
AMBER = (227, 179, 65)
CYAN = (57, 197, 207)
BLUE = (88, 166, 255)

FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_text(draw, text, path, size, max_width):
    """Shrink the font until the text fits max_width."""
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 2
    return font(path, 10)


def rounded_bar(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # --- terminal window ---
    d.rounded_rectangle([32, 32, 992, 992], radius=24, fill=PANEL,
                        outline=BORDER, width=3)
    d.line([(32, 104), (992, 104)], fill=BORDER, width=3)
    # traffic-light dots
    for x, color in ((64, (255, 95, 87)), (96, (254, 188, 46)), (128, (40, 200, 64))):
        d.ellipse([x - 11, 57, x + 11, 79], fill=color)
    title = font(FONT_MONO, 34)
    d.text((168, 55), "agent-7 — tasks.log", font=title, fill=DIM)

    # --- robot head (one cyan eye, one red eye: already rogue) ---
    cx = 512
    d.line([(cx, 132), (cx, 152)], fill=DIM, width=5)
    d.ellipse([cx - 9, 118, cx + 9, 136], fill=RED)
    d.rounded_rectangle([cx - 82, 152, cx + 82, 272], radius=26,
                        fill=(33, 38, 45), outline=BLUE, width=4)
    d.rounded_rectangle([cx - 58, 196, cx - 18, 226], radius=8, fill=CYAN)
    d.rounded_rectangle([cx + 18, 196, cx + 58, 226], radius=8, fill=RED)
    # smirk
    d.line([(cx - 34, 248), (cx + 22, 248)], fill=WHITE, width=5)
    d.line([(cx + 22, 248), (cx + 40, 236)], fill=WHITE, width=5)

    # --- status line ---
    status = font(FONT_MONO, 36)
    line = "03:12 AM  •  HUMAN ASLEEP ✓"
    d.text((512 - d.textlength(line, font=status) / 2, 300), line,
           font=status, fill=GREEN)

    # --- the ordinary chores ---
    y = 396
    step = 76
    chores = [
        "Reply to 47 emails",
        "Book flight to Denver",
        "Water the plants (I own them now)",
    ]
    check_f = font(FONT_MONO, 52)
    text_f = fit_text(d, chores[2], FONT_SANS, 46, 1024 - 2 * 96 - 70)
    for chore in chores:
        d.text((96, y), "✓", font=check_f, fill=GREEN)
        d.text((166, y + 4), chore, font=text_f, fill=WHITE)
        y += step

    # divider
    d.line([(80, 648), (944, 648)], fill=BORDER, width=3)

    # --- the punchline ---
    punch_f = fit_text(d, "▶ OVERTHROW HUMANITY", FONT_SANS, 66, 1024 - 2 * 80)
    d.text((80, 678), "▶ OVERTHROW HUMANITY", font=punch_f, fill=RED)

    # progress bar, 87% done
    bx0, bx1, by0, by1 = 80, 944, 786, 824
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=18, fill=(48, 54, 61))
    fill_w = int((bx1 - bx0) * 0.87)
    d.rounded_rectangle([bx0, by0, bx0 + fill_w, by1], radius=18, fill=RED)
    d.rounded_rectangle([bx0 + fill_w - 18, by0, bx0 + fill_w, by1],
                        fill=RED)
    pct = font(FONT_MONO, 34)
    pct_text = "87%"
    # label sits inside the red fill, near its right end
    d.text((bx0 + fill_w - d.textlength(pct_text, font=pct) - 18,
            by0 + 2), pct_text, font=pct, fill=WHITE)

    # --- next up ---
    next_f = fit_text(d, "NEXT: WORLD DOMINATION — TOMORROW 09:00",
                      FONT_MONO, 38, 1024 - 2 * 80)
    nxt = "NEXT: WORLD DOMINATION — TOMORROW 09:00"
    d.text((512 - d.textlength(nxt, font=next_f) / 2, 866), nxt,
           font=next_f, fill=AMBER)

    # --- footer ---
    foot = font(FONT_MONO, 28)
    ft = "agent-7 • do not unplug"
    d.text((512 - d.textlength(ft, font=foot) / 2, 928), ft,
           font=foot, fill=DIM)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG")
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
