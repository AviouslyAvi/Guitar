from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from pathlib import Path

OUT = str(Path.home() / "Downloads" / "Fretboard-Notes-3-Weeks.pdf")

INK    = HexColor("#1a1a1a")
MUTED  = HexColor("#6b6b6b")
ACCENT = HexColor("#b23b2b")
RULE   = HexColor("#d9d4cc")
BG     = HexColor("#fbf8f3")
SOFT   = HexColor("#efe9dd")
DESK   = HexColor("#2b5f7a")
HOME   = HexColor("#b23b2b")

PAGE_W, PAGE_H = LETTER
MX = 0.55 * inch
SERIF = "Times-Roman"
SANS = "Helvetica"
SANS_B = "Helvetica-Bold"

def wrap(c, text, x, y, max_w, font, size, leading, color):
    c.setFont(font, size); c.setFillColor(color)
    words = text.split(); line = ""
    for w in words:
        trial = (line + " " + w).strip()
        if stringWidth(trial, font, size) > max_w:
            c.drawString(x, y, line); y -= leading; line = w
        else:
            line = trial
    if line:
        c.drawString(x, y, line); y -= leading
    return y

c = canvas.Canvas(OUT, pagesize=LETTER)
c.setFillColor(BG); c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

# ===== HEADER =====
c.setFont(SANS_B, 8); c.setFillColor(ACCENT)
c.drawString(MX, PAGE_H - 0.55 * inch, "3 WEEKS  \u00b7  20 MIN AT WORK  \u00b7  20 MIN AT HOME")
c.setFont(SERIF, 32); c.setFillColor(INK)
c.drawString(MX, PAGE_H - 1.02 * inch, "Fretboard notes, finally.")
c.setStrokeColor(ACCENT); c.setLineWidth(1.2)
c.line(MX, PAGE_H - 1.15 * inch, MX + 1.0 * inch, PAGE_H - 1.15 * inch)

c.setFont(SERIF, 11); c.setFillColor(MUTED)
c.drawString(MX, PAGE_H - 1.42 * inch,
             "You already play. You already know CAGED. You're adding labels, not learning guitar.")

# ===== DAILY SPLIT =====
y = PAGE_H - 1.85 * inch
c.setFont(SANS_B, 8); c.setFillColor(ACCENT)
c.drawString(MX, y, "THE DAILY SPLIT")
y -= 14
c.setStrokeColor(RULE); c.setLineWidth(0.6)
c.line(MX, y, PAGE_W - MX, y)
y -= 20

# Two-column session boxes
col_gap = 0.3 * inch
col_w = (PAGE_W - 2 * MX - col_gap) / 2

# LEFT: AT WORK
c.setFillColor(SOFT)
box_h = 1.55 * inch
c.rect(MX, y - box_h, col_w, box_h, fill=1, stroke=0)

c.setFont(SANS_B, 9); c.setFillColor(DESK)
c.drawString(MX + 14, y - 18, "AT WORK  \u00b7  20 MIN  \u00b7  NO GUITAR")
c.setFont(SERIF, 14); c.setFillColor(INK)
c.drawString(MX + 14, y - 38, "Mental reps")

wy = y - 56
desk_items = [
    "10 min: note-quiz app on your phone. Fretastic, Fretboard Trainer, or Justin Guitar's note finder.",
    "5 min: close your eyes. Name every note on strings 6 and 5 up to fret 12.",
    "5 min: pick a random note. Where does it live on all six strings? Use octave shapes.",
]
for item in desk_items:
    c.setFont(SERIF, 10); c.setFillColor(DESK)
    c.drawString(MX + 14, wy, "\u2022")
    wy = wrap(c, item, MX + 14 + 10, wy, col_w - 34, SANS, 9, 12, INK)
    wy -= 3

# RIGHT: AT HOME
hx = MX + col_w + col_gap
c.setFillColor(SOFT)
c.rect(hx, y - box_h, col_w, box_h, fill=1, stroke=0)

c.setFont(SANS_B, 9); c.setFillColor(HOME)
c.drawString(hx + 14, y - 18, "AT HOME  \u00b7  20 MIN  \u00b7  WITH GUITAR")
c.setFont(SERIF, 14); c.setFillColor(INK)
c.drawString(hx + 14, y - 38, "Play and name")

hy = y - 56
home_items = [
    "10 min: play a scale you know. Name every note out loud as you play it. Slowly.",
    "5 min: play a song you already know. Call out the root of each chord as it lands.",
    "5 min: improvise over a drone. Name every note you land on, even badly.",
]
for item in home_items:
    c.setFont(SERIF, 10); c.setFillColor(HOME)
    c.drawString(hx + 14, hy, "\u2022")
    hy = wrap(c, item, hx + 14 + 10, hy, col_w - 34, SANS, 9, 12, INK)
    hy -= 3

y = y - box_h - 24

# ===== THE 3 WEEKS =====
c.setFont(SANS_B, 8); c.setFillColor(ACCENT)
c.drawString(MX, y, "THE 3 WEEKS")
y -= 14
c.setStrokeColor(RULE); c.setLineWidth(0.6)
c.line(MX, y, PAGE_W - MX, y)
y -= 18

weeks = [
    ("WEEK 1", "Strings 6 & 5",
     "The CAGED root strings. Most important. Sub-2-second recall by Friday.",
     "Pass: name any fret on either string in under 2 seconds, cold."),
    ("WEEK 2", "Strings 4 & 3",
     "Add the middle pair. Cross-check with octaves from week 1 \u2014 it's built in.",
     "Pass: name notes on all four strings without hesitation."),
    ("WEEK 3", "Strings 2 & 1 + integration",
     "Finish the neck. Then do the real test: play music while naming.",
     "Pass: solo over a backing track and name every landing note aloud."),
]

for label, title, body, gate in weeks:
    c.setFont(SANS_B, 10); c.setFillColor(ACCENT)
    c.drawString(MX, y, label)
    c.setFont(SERIF, 14); c.setFillColor(INK)
    c.drawString(MX + 0.85 * inch, y, title)
    yy = wrap(c, body, MX + 0.85 * inch, y - 16, PAGE_W - 2 * MX - 0.85 * inch, SANS, 10, 13, MUTED)
    c.setFont(SANS_B, 8); c.setFillColor(ACCENT)
    c.drawString(MX + 0.85 * inch, yy - 4, "GATE")
    wrap(c, gate, MX + 0.85 * inch + 32, yy - 4, PAGE_W - 2 * MX - 0.85 * inch - 32,
         SERIF, 10, 13, INK)
    y = yy - 26
    c.setStrokeColor(RULE); c.setLineWidth(0.3)
    c.line(MX, y + 6, PAGE_W - MX, y + 6)
    y -= 10

# ===== THREE THINGS THAT WORK =====
y -= 4
c.setFont(SANS_B, 8); c.setFillColor(ACCENT)
c.drawString(MX, y, "THREE THINGS THAT MAKE IT STICK")
y -= 16
rules = [
    ("Say it out loud.",
     "Silent practice builds fingers, not names. Your mouth forces retrieval."),
    ("Twice a day beats once.",
     "Sleep consolidates memory. Two sessions = two consolidation windows."),
    ("Use octaves as the cheat code.",
     "You know CAGED. Same fret, two strings up = same note. Built-in verification."),
]
for i, (head, body) in enumerate(rules, 1):
    c.setFont(SERIF, 12); c.setFillColor(ACCENT)
    c.drawString(MX, y, f"{i}.")
    c.setFont(SERIF, 12); c.setFillColor(INK)
    c.drawString(MX + 16, y, head)
    head_w = stringWidth(head, SERIF, 12)
    c.setFont(SANS, 10); c.setFillColor(MUTED)
    c.drawString(MX + 16 + head_w + 6, y, body)
    y -= 20

# ===== FOOTER =====
c.setFont(SANS, 8); c.setFillColor(MUTED)
c.drawString(MX, 0.45 * inch, "For Avi \u2014 April 2026. You already play. You're labeling, not learning.")
c.drawRightString(PAGE_W - MX, 0.45 * inch, "Print me. Phone + stand.")

c.save()
print(f"Wrote {OUT}")
