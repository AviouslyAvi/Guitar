from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from pathlib import Path

OUT = str(Path.home() / "Downloads" / "CAGED-One-Page.pdf")

INK    = HexColor("#1a1a1a")
MUTED  = HexColor("#6b6b6b")
ACCENT = HexColor("#b23b2b")
RULE   = HexColor("#d9d4cc")
BG     = HexColor("#fbf8f3")
SOFT   = HexColor("#efe9dd")

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
c.drawString(MX, PAGE_H - 0.55 * inch, "40 MINUTES  \u00b7  11 WEEKS  \u00b7  ONE PAGE")
c.setFont(SERIF, 34); c.setFillColor(INK)
c.drawString(MX, PAGE_H - 1.05 * inch, "CAGED, fastest path.")
c.setStrokeColor(ACCENT); c.setLineWidth(1.2)
c.line(MX, PAGE_H - 1.18 * inch, MX + 1.0 * inch, PAGE_H - 1.18 * inch)

c.setFont(SERIF, 11); c.setFillColor(MUTED)
c.drawString(MX, PAGE_H - 1.45 * inch,
             "Same routine daily. One shape at a time. Half your time is improvising, not drilling.")

# ===== COLUMN SETUP =====
col_gap = 0.35 * inch
col_w = (PAGE_W - 2 * MX - col_gap) / 2
left_x = MX
right_x = MX + col_w + col_gap
top_y = PAGE_H - 1.85 * inch

# ===== LEFT COLUMN: DAILY 40 =====
y = top_y
c.setFont(SANS_B, 8); c.setFillColor(ACCENT)
c.drawString(left_x, y, "THE DAILY 40")
y -= 14
c.setStrokeColor(RULE); c.setLineWidth(0.6)
c.line(left_x, y, left_x + col_w, y)
y -= 18

blocks = [
    ("5",  "Note quiz",
     "Random fret on any string, name the note in under 2 seconds. Use an app."),
    ("10", "Shape work",
     "This week's shape: octave \u2192 chord \u2192 triads \u2192 arpeggio \u2192 pentatonic \u2192 scale. Root to root."),
    ("5",  "Link",
     "Slide from this shape into the neighbor shape and back. Messy is fine."),
    ("20", "Improvise",
     "Backing track in this week's key. Make real music. This is where fluency is built."),
]
for mins, title, body in blocks:
    c.setFont(SERIF, 22); c.setFillColor(ACCENT)
    c.drawString(left_x, y - 4, mins)
    c.setFont(SANS, 7); c.setFillColor(ACCENT)
    c.drawString(left_x + 0.34 * inch, y + 2, "MIN")
    c.setFont(SERIF, 13); c.setFillColor(INK)
    c.drawString(left_x + 0.72 * inch, y, title)
    yy = wrap(c, body, left_x + 0.72 * inch, y - 14,
              col_w - 0.72 * inch, SANS, 9, 12, INK)
    y = yy - 10

# Three rules box
y -= 4
c.setFillColor(SOFT)
box_top = y
box_h = 1.15 * inch
c.rect(left_x, y - box_h, col_w, box_h, fill=1, stroke=0)
c.setFont(SANS_B, 8); c.setFillColor(ACCENT)
c.drawString(left_x + 12, y - 16, "THREE RULES THAT COMPOUND")
yr = y - 34
rules = [
    "Start from the root, not string 6.",
    "Say intervals aloud: \u201croot, three, five.\u201d",
    "No unaccompanied practice. Drone or track, always.",
]
for i, r in enumerate(rules, 1):
    c.setFont(SERIF, 11); c.setFillColor(ACCENT)
    c.drawString(left_x + 12, yr, f"{i}.")
    c.setFont(SERIF, 11); c.setFillColor(INK)
    c.drawString(left_x + 12 + 14, yr, r)
    yr -= 18

y = y - box_h - 14

# Weekly accelerator
c.setFont(SANS_B, 8); c.setFillColor(ACCENT)
c.drawString(left_x, y, "ONCE A WEEK")
y -= 14
c.line(left_x, y, left_x + col_w, y)
y -= 14
items = [
    "Record a 60-second improvisation. Listen back.",
    "Play this week's shape in all 12 keys at 100 BPM.",
    "Take the gate test on the right. Advance or loop.",
]
for it in items:
    c.setFont(SERIF, 11); c.setFillColor(ACCENT)
    c.drawString(left_x, y, "\u2022")
    y = wrap(c, it, left_x + 12, y, col_w - 12, SERIF, 11, 14, INK)
    y -= 2

# ===== RIGHT COLUMN: 11-WEEK CHECKLIST =====
y = top_y
c.setFont(SANS_B, 8); c.setFillColor(ACCENT)
c.drawString(right_x, y, "THE 11-WEEK MAP")
y -= 14
c.setStrokeColor(RULE); c.setLineWidth(0.6)
c.line(right_x, y, right_x + col_w, y)
y -= 16

weeks = [
    ("1",    "Notes & octaves",   "Name any note in 2s. All 5 octave shapes."),
    ("2\u20133", "E-shape major",  "All layers. Improvise over E drone daily."),
    ("4",    "A-shape + E\u2194A", "Link from day one."),
    ("5",    "G-shape + A\u2194G", "Two octaves. Chain three shapes."),
    ("6",    "C and D shapes",    "Compress both. You've got the pattern."),
    ("7",    "Walkabout",         "Slide through all 5 shapes, one root. Then random roots."),
    ("8",    "E & A minor",       "Same routine, minor layers. Static-root test."),
    ("9",    "D, G, C minor",     "Three shapes in one week. Link them."),
    ("10",   "Open keys",         "I\u2013IV\u2013V in C, G, D, A, E. Feel the movement."),
    ("11",   "CAGED keys",        "I\u2013V\u2013vi\u2013IV in any key, any feel. Done."),
]

for wk, focus, body in weeks:
    c.setFont(SANS_B, 10); c.setFillColor(ACCENT)
    c.drawString(right_x, y, f"W{wk}")
    c.setFont(SERIF, 12); c.setFillColor(INK)
    c.drawString(right_x + 0.55 * inch, y, focus)
    yy = wrap(c, body, right_x + 0.55 * inch, y - 13,
              col_w - 0.55 * inch, SANS, 9, 12, MUTED)
    y = yy - 6
    c.setStrokeColor(RULE); c.setLineWidth(0.3)
    c.line(right_x, y + 2, right_x + col_w, y + 2)
    y -= 8

# Gate test box
y -= 4
c.setFillColor(SOFT)
box_h = 1.05 * inch
c.rect(right_x, y - box_h, col_w, box_h, fill=1, stroke=0)
c.setFont(SANS_B, 8); c.setFillColor(ACCENT)
c.drawString(right_x + 12, y - 16, "WEEKLY GATE TEST")
c.setFont(SERIF, 10); c.setFillColor(INK)
gy = y - 32
gate = ("Can you play this week's focus in THREE different root keys, "
        "over a backing track, without stopping? If yes, advance. If no, loop the week. "
        "Moving on too early is the #1 reason players stall.")
wrap(c, gate, right_x + 12, gy, col_w - 24, SERIF, 10, 13, INK)

# ===== FOOTER =====
c.setFont(SANS, 8); c.setFillColor(MUTED)
c.drawString(MX, 0.45 * inch, "Based on Ry Naylor, CAGED Clarity 2.0. For Avi \u2014 April 2026.")
c.drawRightString(PAGE_W - MX, 0.45 * inch, "Print me. Tape me to your stand.")

c.save()
print(f"Wrote {OUT}")
