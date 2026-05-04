from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
import os

OUT = str(Path.home() / "Downloads" / "CAGED-Practice-Guide.pdf")

INK = HexColor("#1a1a1a")
MUTED = HexColor("#6b6b6b")
ACCENT = HexColor("#b23b2b")
RULE = HexColor("#d9d4cc")
BG = HexColor("#fbf8f3")

PAGE_W, PAGE_H = LETTER
MARGIN_X = 0.9 * inch
MARGIN_TOP = 1.0 * inch
MARGIN_BOT = 0.9 * inch

try:
    pdfmetrics.registerFont(TTFont("Inter", "/System/Library/Fonts/Supplemental/Georgia.ttf"))
    SERIF = "Inter"
except Exception:
    SERIF = "Times-Roman"
SANS = "Helvetica"
SANS_B = "Helvetica-Bold"
SANS_O = "Helvetica-Oblique"

def draw_page_bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

def footer(c, page_num, total):
    c.setFont(SANS, 8)
    c.setFillColor(MUTED)
    c.drawString(MARGIN_X, 0.5 * inch, "CAGED \u2014 40-min Daily Guide")
    c.drawRightString(PAGE_W - MARGIN_X, 0.5 * inch, f"{page_num} / {total}")

def section_title(c, y, text, kicker=None):
    if kicker:
        c.setFont(SANS_B, 8)
        c.setFillColor(ACCENT)
        c.drawString(MARGIN_X, y + 18, kicker.upper())
    c.setFont(SERIF, 22)
    c.setFillColor(INK)
    c.drawString(MARGIN_X, y, text)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.5)
    c.line(MARGIN_X, y - 10, PAGE_W - MARGIN_X, y - 10)
    return y - 34

def para(c, y, text, size=10.5, leading=15, font=SANS, color=INK, width=None):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    if width is None:
        width = PAGE_W - 2 * MARGIN_X
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    line = ""
    for w in words:
        trial = (line + " " + w).strip()
        if stringWidth(trial, font, size) > width:
            c.drawString(MARGIN_X, y, line)
            y -= leading
            line = w
        else:
            line = trial
    if line:
        c.drawString(MARGIN_X, y, line)
        y -= leading
    return y

# ---------------- PAGE 1: COVER ----------------
def page_cover(c):
    draw_page_bg(c)
    # Small kicker
    c.setFont(SANS_B, 9)
    c.setFillColor(ACCENT)
    c.drawString(MARGIN_X, PAGE_H - 1.4 * inch, "40 MINUTES A DAY  \u00b7  16 WEEKS")

    c.setFont(SERIF, 44)
    c.setFillColor(INK)
    c.drawString(MARGIN_X, PAGE_H - 2.3 * inch, "CAGED,")
    c.drawString(MARGIN_X, PAGE_H - 2.9 * inch, "simply.")

    c.setStrokeColor(ACCENT)
    c.setLineWidth(1.2)
    c.line(MARGIN_X, PAGE_H - 3.15 * inch, MARGIN_X + 1.2 * inch, PAGE_H - 3.15 * inch)

    c.setFont(SERIF, 13)
    c.setFillColor(MUTED)
    y = PAGE_H - 3.6 * inch
    y = para(c, y, "A minimal practice companion to Ry Naylor's", size=13, leading=18, font=SERIF, color=MUTED)
    y = para(c, y, "CAGED Clarity 2.0. Same routine every day.", size=13, leading=18, font=SERIF, color=MUTED)
    y = para(c, y, "One shape at a time. Root to root.", size=13, leading=18, font=SERIF, color=MUTED)

    # Big numbered promise
    y = PAGE_H - 6.0 * inch
    items = [
        ("01", "Know the fretboard."),
        ("02", "See chords, arpeggios, scales as one map."),
        ("03", "Solo in any key, anywhere on the neck."),
    ]
    for num, text in items:
        c.setFont(SERIF, 28)
        c.setFillColor(ACCENT)
        c.drawString(MARGIN_X, y, num)
        c.setFont(SERIF, 14)
        c.setFillColor(INK)
        c.drawString(MARGIN_X + 0.7 * inch, y + 4, text)
        y -= 0.55 * inch

    footer(c, 1, 4)

# ---------------- PAGE 2: DAILY ROUTINE ----------------
def page_routine(c):
    draw_page_bg(c)
    y = PAGE_H - MARGIN_TOP
    y = section_title(c, y, "The daily 40", kicker="routine")

    c.setFont(SANS, 10.5)
    c.setFillColor(MUTED)
    y = para(c, y, "Same four blocks. Every day. Metronome on for blocks 2 and 3. Drone on for block 4.",
             size=10.5, leading=15, font=SANS, color=MUTED)
    y -= 12

    blocks = [
        ("5 min",  "Warm up",       "Name and find notes on strings 6 and 5. Add more strings as weeks go on."),
        ("10 min", "Chord layer",   "This week's shape: octave \u2192 barre chord \u2192 triads across the string sets."),
        ("15 min", "Melody layer",  "Same shape: arpeggio \u2192 pentatonic \u2192 full scale. Always root to root."),
        ("10 min", "Play music",    "Improvise over a drone or backing track in this week's key. Non-negotiable."),
    ]

    from reportlab.pdfbase.pdfmetrics import stringWidth
    for time, title, body in blocks:
        c.setFont(SANS_B, 11)
        c.setFillColor(ACCENT)
        c.drawString(MARGIN_X, y, time)
        c.setFont(SERIF, 15)
        c.setFillColor(INK)
        c.drawString(MARGIN_X + 1.0 * inch, y, title)
        yy = y - 18
        c.setFont(SANS, 10.5)
        c.setFillColor(INK)
        max_w = PAGE_W - 2 * MARGIN_X - 1.0 * inch
        words = body.split()
        line = ""
        for w in words:
            trial = (line + " " + w).strip()
            if stringWidth(trial, SANS, 10.5) > max_w:
                c.drawString(MARGIN_X + 1.0 * inch, yy, line)
                yy -= 14
                line = w
            else:
                line = trial
        if line:
            c.drawString(MARGIN_X + 1.0 * inch, yy, line)
            yy -= 14
        y = yy - 10
        c.setStrokeColor(RULE)
        c.setLineWidth(0.4)
        c.line(MARGIN_X, y + 6, PAGE_W - MARGIN_X, y + 6)
        y -= 14

    # Three rules
    y -= 10
    c.setFont(SANS_B, 9)
    c.setFillColor(ACCENT)
    c.drawString(MARGIN_X, y, "THREE RULES THAT DO MOST OF THE WORK")
    y -= 20
    rules = [
        "Start from the root, not from string 6.",
        "Say the intervals out loud: \u201croot, three, five.\u201d",
        "Always play over harmony. Shapes without sound are just finger patterns.",
    ]
    for i, r in enumerate(rules, 1):
        c.setFont(SERIF, 13)
        c.setFillColor(ACCENT)
        c.drawString(MARGIN_X, y, f"{i}.")
        c.setFont(SERIF, 13)
        c.setFillColor(INK)
        c.drawString(MARGIN_X + 0.3 * inch, y, r)
        y -= 22

    footer(c, 2, 4)

# ---------------- PAGE 3: 16-WEEK MAP ----------------
def page_map(c):
    draw_page_bg(c)
    y = PAGE_H - MARGIN_TOP
    y = section_title(c, y, "The 16-week map", kicker="one shape at a time")

    c.setFont(SANS, 10.5)
    c.setFillColor(MUTED)
    y = para(c, y, "Don't rush ahead. Finish a shape before starting the next. If a week feels thin, loop it.",
             size=10.5, leading=15, font=SANS, color=MUTED)
    y -= 8

    phases = [
        ("Weeks 1\u20132",  "Prereqs",        "Notes on strings 6 & 5. All five octave shapes."),
        ("Weeks 3\u20135",  "E-shape major",  "Full layers. This is the foundation."),
        ("Weeks 6\u20137",  "A-shape major",  "Then link E \u2194 A with slides."),
        ("Weeks 8\u20139",  "G-shape major",  "Two octaves. Link A \u2194 G."),
        ("Week 10",         "C-shape major",  "Link G \u2194 C."),
        ("Week 11",         "D-shape major",  "Link C \u2194 D. Walk all five shapes."),
        ("Weeks 12\u201313","E & A minor",    "Same routine, minor layers."),
        ("Week 14",         "D, G, C minor",  "Faster now. Three in one week."),
        ("Weeks 15\u201316","Progressions",   "I\u2013V\u2013vi\u2013IV in each \u201cfeel.\u201d Music, at last."),
    ]

    row_h = 0.52 * inch
    col_time_x = MARGIN_X
    col_title_x = MARGIN_X + 1.35 * inch
    col_body_x  = MARGIN_X + 3.4 * inch

    # Header
    c.setFont(SANS_B, 8)
    c.setFillColor(MUTED)
    c.drawString(col_time_x, y, "WHEN")
    c.drawString(col_title_x, y, "FOCUS")
    c.drawString(col_body_x, y, "WHAT YOU'LL DO")
    y -= 10
    c.setStrokeColor(RULE)
    c.setLineWidth(0.5)
    c.line(MARGIN_X, y, PAGE_W - MARGIN_X, y)
    y -= 6

    for when, focus, body in phases:
        row_top = y
        c.setFont(SANS_B, 10.5)
        c.setFillColor(ACCENT)
        c.drawString(col_time_x, y - 12, when)
        c.setFont(SERIF, 13)
        c.setFillColor(INK)
        c.drawString(col_title_x, y - 12, focus)
        c.setFont(SANS, 10)
        c.setFillColor(INK)
        # wrap body
        from reportlab.pdfbase.pdfmetrics import stringWidth
        max_w = PAGE_W - MARGIN_X - col_body_x
        words = body.split()
        line = ""
        yy = y - 12
        for w in words:
            trial = (line + " " + w).strip()
            if stringWidth(trial, SANS, 10) > max_w:
                c.drawString(col_body_x, yy, line)
                yy -= 13
                line = w
            else:
                line = trial
        if line:
            c.drawString(col_body_x, yy, line)
            yy -= 13
        y = min(y - row_h, yy - 6)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.3)
        c.line(MARGIN_X, y + 4, PAGE_W - MARGIN_X, y + 4)

    footer(c, 3, 4)

# ---------------- PAGE 4: MILESTONES & SETUP ----------------
def page_check(c):
    draw_page_bg(c)
    y = PAGE_H - MARGIN_TOP
    y = section_title(c, y, "How you know it's working", kicker="milestones")

    milestones = [
        ("After week 5",
         "You can solo for 30 seconds in E minor over a backing track using only the E-shape pentatonic."),
        ("After week 11",
         "You can find any note on the fretboard in under two seconds by seeing which shape it lives in."),
        ("After week 16",
         "Given any I\u2013V\u2013vi\u2013IV, you can play it and solo over it in at least two different shapes."),
    ]

    for when, text in milestones:
        c.setFont(SANS_B, 9)
        c.setFillColor(ACCENT)
        c.drawString(MARGIN_X, y, when.upper())
        y -= 16
        y = para(c, y, text, size=12, leading=17, font=SERIF, color=INK)
        y -= 12

    y -= 8
    c.setStrokeColor(RULE)
    c.setLineWidth(0.5)
    c.line(MARGIN_X, y, PAGE_W - MARGIN_X, y)
    y -= 28

    # Setup
    c.setFont(SANS_B, 8)
    c.setFillColor(ACCENT)
    c.drawString(MARGIN_X, y, "SET UP ONCE, TONIGHT")
    y -= 20

    setup = [
        "Metronome app (Tempo by Frozen Ape works well).",
        "Bookmark dronetonetool.com for single-note drones.",
        "Find one backing track in E minor on YouTube.",
        "Print the shape summaries that came with the book.",
    ]
    for i, s in enumerate(setup, 1):
        c.setFont(SERIF, 12)
        c.setFillColor(ACCENT)
        c.drawString(MARGIN_X, y, f"{i}.")
        c.setFont(SERIF, 12)
        c.setFillColor(INK)
        c.drawString(MARGIN_X + 0.3 * inch, y, s)
        y -= 20

    y -= 10
    c.setStrokeColor(RULE)
    c.line(MARGIN_X, y, PAGE_W - MARGIN_X, y)
    y -= 28

    # Closing note
    c.setFont(SERIF, 13)
    c.setFillColor(INK)
    c.drawString(MARGIN_X, y, "That's the whole plan.")
    y -= 22
    c.setFont(SANS, 10.5)
    c.setFillColor(MUTED)
    y = para(c, y,
             "Ten years without the fretboard ends with forty focused minutes a day. "
             "Not with cleverness. With repetition, in context, root to root.",
             size=10.5, leading=15, font=SANS, color=MUTED)

    footer(c, 4, 4)

def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    c = canvas.Canvas(OUT, pagesize=LETTER)
    page_cover(c); c.showPage()
    page_routine(c); c.showPage()
    page_map(c); c.showPage()
    page_check(c); c.showPage()
    c.save()
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
