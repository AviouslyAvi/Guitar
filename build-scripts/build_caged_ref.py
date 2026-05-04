"""Condensed 4-page CAGED reference card from Ry Naylor's CAGED Clarity 2.0."""
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from pathlib import Path

OUT = str(Path("/Users/aviouslyavi/Claude/Projects/Avious Music/Guitar") / "CAGED-Reference-Card.pdf")

INK    = HexColor("#1a1a1a")
MUTED  = HexColor("#6b6b6b")
ACCENT = HexColor("#b23b2b")
RULE   = HexColor("#d9d4cc")
BG     = HexColor("#fbf8f3")
SOFT   = HexColor("#efe9dd")

PAGE_W, PAGE_H = LETTER
MX = 0.6 * inch
SERIF = "Times-Roman"
SERIF_B = "Times-Bold"
SERIF_I = "Times-Italic"
SANS = "Helvetica"
SANS_B = "Helvetica-Bold"
MONO = "Courier"

# --------- helpers ---------
def bg(c):
    c.setFillColor(BG); c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

def footer(c, n, total):
    c.setFont(SANS, 8); c.setFillColor(MUTED)
    c.drawString(MX, 0.45 * inch, "CAGED Reference  ·  condensed from Ry Naylor, CAGED Clarity 2.0")
    c.drawRightString(PAGE_W - MX, 0.45 * inch, f"{n} / {total}")

def section(c, y, title, kicker=None):
    if kicker:
        c.setFont(SANS_B, 8); c.setFillColor(ACCENT)
        c.drawString(MX, y + 18, kicker.upper())
    c.setFont(SERIF, 22); c.setFillColor(INK)
    c.drawString(MX, y, title)
    c.setStrokeColor(RULE); c.setLineWidth(0.5)
    c.line(MX, y - 10, PAGE_W - MX, y - 10)
    return y - 28

def h3(c, y, text):
    c.setFont(SANS_B, 9); c.setFillColor(ACCENT)
    c.drawString(MX, y, text.upper())
    return y - 14

def wrap(c, text, x, y, max_w, font, size, leading, color):
    c.setFont(font, size); c.setFillColor(color)
    line = ""
    for w in text.split():
        trial = (line + " " + w).strip()
        if stringWidth(trial, font, size) > max_w:
            c.drawString(x, y, line); y -= leading; line = w
        else:
            line = trial
    if line:
        c.drawString(x, y, line); y -= leading
    return y

def table(c, y, cols, rows, col_widths, head_size=8, body_size=9, row_h=18):
    """Simple table with header row. cols = header strings. rows = list of tuples."""
    x = MX
    # header
    c.setFont(SANS_B, head_size); c.setFillColor(ACCENT)
    cx = x
    for col, w in zip(cols, col_widths):
        c.drawString(cx, y, col.upper())
        cx += w
    y -= 6
    c.setStrokeColor(RULE); c.setLineWidth(0.5)
    c.line(x, y, x + sum(col_widths), y)
    y -= 4
    # rows
    for row in rows:
        cx = x
        for cell, w in zip(row, col_widths):
            # wrap cell within column width
            font = SERIF if cx == x else SANS
            size = body_size + 1 if cx == x else body_size
            c.setFont(font, size); c.setFillColor(INK)
            # one-line draw, truncated visually if too long (rare)
            if stringWidth(str(cell), font, size) > w - 6:
                # wrap multi-line in cell
                yy = y - 12
                line = ""
                for word in str(cell).split():
                    trial = (line + " " + word).strip()
                    if stringWidth(trial, font, size) > w - 6:
                        c.drawString(cx, yy, line)
                        yy -= 11
                        line = word
                    else:
                        line = trial
                if line:
                    c.drawString(cx, yy, line)
            else:
                c.drawString(cx, y - 12, str(cell))
            cx += w
        y -= row_h
        c.setStrokeColor(RULE); c.setLineWidth(0.2)
        c.line(x, y + 4, x + sum(col_widths), y + 4)
    return y - 4

# ========================================
# PAGE 1 — Foundations
# ========================================
def page_1(c):
    bg(c)
    # masthead
    c.setFont(SANS_B, 8); c.setFillColor(ACCENT)
    c.drawString(MX, PAGE_H - 0.55 * inch, "CONDENSED REFERENCE  ·  4 PAGES  ·  CAGED CLARITY 2.0")
    c.setFont(SERIF, 36); c.setFillColor(INK)
    c.drawString(MX, PAGE_H - 1.1 * inch, "CAGED, in four pages.")
    c.setStrokeColor(ACCENT); c.setLineWidth(1.2)
    c.line(MX, PAGE_H - 1.22 * inch, MX + 1.2 * inch, PAGE_H - 1.22 * inch)
    c.setFont(SERIF_I, 11); c.setFillColor(MUTED)
    c.drawString(MX, PAGE_H - 1.5 * inch, "What you actually flip back to. Diagrams stay in the book.")

    y = PAGE_H - 1.95 * inch
    y = h3(c, y, "What CAGED is")
    y = wrap(c, ("CAGED isn't a system someone invented. It's the natural consequence of standard tuning. "
                 "Five open chord shapes (C, A, G, E, D) recur up the neck because the intervals between strings "
                 "force them to. Once you see the five octave shapes, every chord, arpeggio, pentatonic, and scale "
                 "lives inside one of them."),
               MX, y, PAGE_W - 2*MX, SANS, 10, 14, INK)
    y -= 8

    y = h3(c, y, "The 5 octave shapes")
    rows = [
        ("C-Shape", "5(A) → 2(B)",      "headstock", "skip 2 strings; chord tones in order R-3-5-R"),
        ("A-Shape", "5(A) → 3(G)",      "body",      "skip 1 string; missing the 3 in lower octave"),
        ("G-Shape", "6(E) → 3(G), 3(G) → 1(E)", "both", "octave SET; triangle points to headstock"),
        ("E-Shape", "6(E) → 4(D), 4(D) → 1(E)", "both", "octave SET; triangle points to body"),
        ("D-Shape", "4(D) → 2(B)",      "body",      "octave 3 frets up on string 2"),
    ]
    y = table(c, y, ["Shape", "Strings", "Direction", "Notes"], rows,
              [0.85*inch, 1.55*inch, 0.85*inch, 3.65*inch], row_h=20)
    y -= 6

    y = h3(c, y, "The CAGED cycle")
    y = wrap(c,
             "The shapes always appear in the same order as you move up the neck: C → A → G → E → D, "
             "then it repeats. Where you start depends on which string the lowest root sits on. "
             "Think of it as a wheel you can spin in either direction.",
             MX, y, PAGE_W - 2*MX, SANS, 10, 14, INK)
    y -= 4
    rules = [
        "On string 2(B) → 5(A): C-Shape",
        "On string 5(A) → 3(G): A-Shape",
        "On string 3(G) → 1(E): G-Shape",
        "On string 1(E) → 6(E): G-/E-Shape (two-octave bridge)",
        "On string 6(E) → 4(D): E-Shape",
        "On string 4(D) → 2(B): D-Shape",
    ]
    for r in rules:
        c.setFont(MONO, 9); c.setFillColor(MUTED)
        c.drawString(MX + 6, y, "•")
        c.setFont(SANS, 10); c.setFillColor(INK)
        c.drawString(MX + 18, y, r)
        y -= 13
    y -= 8

    y = h3(c, y, "The 6 layers (every shape contains all of them)")
    layers = [
        ("Octave",      "links the root notes; the skeleton"),
        ("Barre chord", "an open chord shape moved up the neck"),
        ("Triads",      "3-note voicings across each string set"),
        ("Arpeggio",    "the chord tones as single notes"),
        ("Pentatonic",  "arpeggio + 2 notes; major or minor"),
        ("Diatonic",    "all 7 notes; major or natural minor"),
    ]
    for name, desc in layers:
        c.setFont(SERIF_B, 11); c.setFillColor(ACCENT)
        c.drawString(MX, y, name)
        c.setFont(SANS, 10); c.setFillColor(INK)
        c.drawString(MX + 1.0 * inch, y, desc)
        y -= 14
    y -= 6

    # Five essentials box
    box_h = 1.05 * inch
    c.setFillColor(SOFT); c.rect(MX, y - box_h, PAGE_W - 2*MX, box_h, fill=1, stroke=0)
    c.setFont(SANS_B, 9); c.setFillColor(ACCENT)
    c.drawString(MX + 12, y - 16, "FIVE ESSENTIALS THAT CARRY EVERYTHING")
    yy = y - 32
    essentials = [
        "Always practice over harmony — drone, chord, or backing track. Never bare patterns.",
        "Think in intervals, not shapes. Say \"root, three, five\" out loud as you play.",
        "Start patterns from the root, not from string 6. Most players cripple themselves here.",
        "Major scale formula: W-W-H-W-W-W-H. Every interval is measured against this ruler.",
    ]
    for e in essentials:
        c.setFont(SERIF, 10); c.setFillColor(ACCENT)
        c.drawString(MX + 12, yy, "·")
        wrap(c, e, MX + 22, yy, PAGE_W - 2*MX - 34, SANS, 10, 13, INK)
        yy -= 14

    footer(c, 1, 4)

# ========================================
# PAGE 2 — The 10 Shapes at a Glance
# ========================================
def page_2(c):
    bg(c)
    y = PAGE_H - 0.85 * inch
    y = section(c, y, "The 10 shapes at a glance", kicker="major + minor")

    y = wrap(c,
             "Every shape sits between two roots and contains every layer above. "
             "Diagrams are in the book — here's the structural view: where each shape lives, "
             "what's distinctive about it, and the order to learn them in.",
             MX, y, PAGE_W - 2*MX, SANS, 10, 14, MUTED)
    y -= 8

    y = h3(c, y, "Major shapes — learn in this order")
    major_rows = [
        ("1. E-Shape", "6(E)–4(D)–1(E)", "Familiar barre chord. Highest ROI first."),
        ("2. A-Shape", "5(A)–3(G)",          "Lower octave missing the 3. Very common rhythm shape."),
        ("3. G-Shape", "6(E)–3(G)–1(E)", "Two-octave triangle pointing to headstock."),
        ("4. C-Shape", "5(A)–2(B)",          "Awkward chord; great triads. Bridges G and A."),
        ("5. D-Shape", "4(D)–2(B)",          "Tightest shape. Useful for upper-octave triads."),
    ]
    y = table(c, y, ["Order", "Span", "Why"], major_rows,
              [1.15*inch, 1.55*inch, 4.2*inch], row_h=20)
    y -= 8

    y = h3(c, y, "Minor shapes — learn in this order")
    minor_rows = [
        ("1. E-Shape min", "6(E)–4(D)–1(E)", "The classic minor pentatonic box."),
        ("2. A-Shape min", "5(A)–3(G)",          "Open Am chord moved up. Very natural."),
        ("3. D-Shape min", "4(D)–2(B)",          "Triads are excellent here."),
        ("4. G-Shape min", "6(E)–3(G)–1(E)", "Tricky chord, useful for soloing."),
        ("5. C-Shape min", "5(A)–2(B)",          "Rarely used as full chord; bridges D and A."),
    ]
    y = table(c, y, ["Order", "Span", "Why"], minor_rows,
              [1.45*inch, 1.55*inch, 3.9*inch], row_h=20)
    y -= 12

    y = h3(c, y, "Adjacency — which shape sits next to which")
    y = wrap(c,
             "Going up the fretboard from any shape, the next shape always follows the CAGED cycle. "
             "When linking shapes, the slide happens on string 6 or string 1, depending on direction.",
             MX, y, PAGE_W - 2*MX, SANS, 10, 14, INK)
    y -= 4
    cycle = "  C  →  A  →  G  →  E  →  D  →  C  →  A  ..."
    c.setFont(SERIF, 14); c.setFillColor(ACCENT)
    c.drawCentredString(PAGE_W / 2, y - 6, cycle)
    y -= 28

    # diagonal roots
    y = h3(c, y, "Root-on-string → which shapes you're standing in")
    diag_rows = [
        ("Root on 6(E)", "G-Shape (towards headstock) OR E-Shape (towards body)"),
        ("Root on 5(A)", "C-Shape (towards headstock) OR A-Shape (towards body)"),
        ("Root on 4(D)", "E-Shape (towards headstock) OR D-Shape (towards body)"),
        ("Root on 3(G)", "G-Shape only — the bridge between high and low octaves"),
    ]
    for col1, col2 in diag_rows:
        c.setFont(SERIF_B, 11); c.setFillColor(ACCENT)
        c.drawString(MX, y, col1)
        c.setFont(SANS, 10); c.setFillColor(INK)
        c.drawString(MX + 1.4 * inch, y, col2)
        y -= 16
    y -= 8

    # Fingering hint box
    box_h = 0.85 * inch
    c.setFillColor(SOFT); c.rect(MX, y - box_h, PAGE_W - 2*MX, box_h, fill=1, stroke=0)
    c.setFont(SANS_B, 9); c.setFillColor(ACCENT)
    c.drawString(MX + 12, y - 16, "FINGERING DECISION RULE")
    yy = y - 32
    yy = wrap(c,
              "If you anchor the root on string 6 with finger 4, you're set up to play notes BEHIND it (toward the headstock). "
              "If you anchor with finger 2, you're set up to play AHEAD of it (toward the body). "
              "That choice tells you which shape you're in.",
              MX + 12, yy, PAGE_W - 2*MX - 24, SANS, 10, 13, INK)

    footer(c, 2, 4)

# ========================================
# PAGE 3 — Intervals & Triads
# ========================================
def page_3(c):
    bg(c)
    y = PAGE_H - 0.85 * inch
    y = section(c, y, "Intervals & triads", kicker="the language underneath")

    y = h3(c, y, "Intervals on a single string (from any root)")
    interval_rows = [
        ("0",  "R",     "root / unison"),
        ("1",  "b2","minor 2nd"),
        ("2",  "2",     "major 2nd / 9"),
        ("3",  "b3","minor 3rd"),
        ("4",  "3",     "major 3rd"),
        ("5",  "4",     "perfect 4th / 11"),
        ("6",  "b5","tritone"),
        ("7",  "5",     "perfect 5th"),
        ("8",  "b6","minor 6th"),
        ("9",  "6",     "major 6th / 13"),
        ("10", "b7","minor 7th"),
        ("11", "7",     "major 7th"),
        ("12", "R",     "octave"),
    ]
    # 3-column interval table
    col_w = (PAGE_W - 2*MX) / 3
    rows_per_col = 5
    start_y = y
    for i, (frets, deg, name) in enumerate(interval_rows):
        col = i // rows_per_col
        row = i % rows_per_col
        cx = MX + col * col_w
        cy = start_y - row * 16
        c.setFont(MONO, 10); c.setFillColor(ACCENT)
        c.drawString(cx, cy, f"+{frets}")
        c.setFont(SERIF_B, 11); c.setFillColor(INK)
        c.drawString(cx + 28, cy, deg)
        c.setFont(SANS, 9); c.setFillColor(MUTED)
        c.drawString(cx + 56, cy, name)
    y = start_y - rows_per_col * 16 - 8
    y -= 8

    y = h3(c, y, "Major scale formula")
    c.setFont(MONO, 12); c.setFillColor(ACCENT)
    c.drawCentredString(PAGE_W / 2, y, "W — W — H — W — W — W — H")
    y -= 14
    c.setFont(SANS, 9); c.setFillColor(MUTED)
    c.drawCentredString(PAGE_W / 2, y, "(W = whole step / 2 frets, H = half step / 1 fret)")
    y -= 18

    y = h3(c, y, "Triad string sets")
    set_rows = [
        ("Set 1", "3(G) - 2(B) - 1(E)", "M3 + P4"),
        ("Set 2", "4(D) - 3(G) - 2(B)", "P4 + M3"),
        ("Set 3", "5(A) - 4(D) - 3(G)", "P4 + P4"),
        ("Set 4", "6(E) - 5(A) - 4(D)", "P4 + P4"),
    ]
    y = table(c, y, ["Set", "Strings", "Intervals"], set_rows,
              [0.7*inch, 2.0*inch, 4.55*inch], row_h=18)
    y -= 8

    y = h3(c, y, "Major triad voicings (3 inversions)")
    inv_rows = [
        ("Root position",     "R - 3 - 5",  "lowest note is the root"),
        ("First inversion",   "3 - 5 - R",  "lowest note is the 3"),
        ("Second inversion",  "5 - R - 3",  "lowest note is the 5"),
    ]
    for label, notes, desc in inv_rows:
        c.setFont(SERIF_B, 11); c.setFillColor(ACCENT)
        c.drawString(MX, y, label)
        c.setFont(MONO, 10); c.setFillColor(INK)
        c.drawString(MX + 1.6 * inch, y, notes)
        c.setFont(SANS, 10); c.setFillColor(MUTED)
        c.drawString(MX + 3.0 * inch, y, desc)
        y -= 16
    y -= 4

    # Minor triad note
    box_h = 0.5 * inch
    c.setFillColor(SOFT); c.rect(MX, y - box_h, PAGE_W - 2*MX, box_h, fill=1, stroke=0)
    c.setFont(SANS_B, 9); c.setFillColor(ACCENT)
    c.drawString(MX + 12, y - 16, "MINOR — ONE CHANGE FROM MAJOR")
    c.setFont(SANS, 10); c.setFillColor(INK)
    c.drawString(MX + 12, y - 30, "Flatten the 3. R-b3-5 instead of R-3-5. Everything else (shapes, sets, voicings) is identical.")
    y -= box_h + 10

    # Chord tone counts
    y = h3(c, y, "Quick math — what's in a shape")
    quick = [
        "Major triad = 3 notes (R, 3, 5)",
        "Major arpeggio = same 3 notes, played one at a time across the shape",
        "Major pentatonic = arpeggio + 2 (R, 2, 3, 5, 6)",
        "Major scale = pentatonic + 2 (R, 2, 3, 4, 5, 6, 7)",
    ]
    for q in quick:
        c.setFont(SERIF, 11); c.setFillColor(ACCENT)
        c.drawString(MX + 6, y, "•")
        c.setFont(SANS, 10); c.setFillColor(INK)
        c.drawString(MX + 18, y, q)
        y -= 14

    footer(c, 3, 4)

# ========================================
# PAGE 4 — Application
# ========================================
def page_4(c):
    bg(c)
    y = PAGE_H - 0.85 * inch
    y = section(c, y, "Application", kicker="open keys, progressions, practice")

    y = h3(c, y, "The 5 Open Keys")
    y = wrap(c,
             "Each open key has a tonic chord that matches one CAGED shape. Learn all five real keys "
             "in open position; then translate any progression to a different \"feel\" by moving up the neck.",
             MX, y, PAGE_W - 2*MX, SANS, 10, 13, INK)
    y -= 4
    open_rows = [
        ("Key of C", "Am",     "C-Shape", "1–IV: F is an E-Shape (exception)"),
        ("Key of G", "Em",     "G-Shape", "1–IV: C is a C-Shape, same fret on string 5"),
        ("Key of D", "Bm",     "D-Shape", "1–IV: G is a G-Shape, same fret on string 3"),
        ("Key of A", "F#m","A-Shape", "1–IV: D is an E-Shape, same fret on string 4"),
        ("Key of E", "C#m","E-Shape", "1–IV: A is an A-Shape, same fret on string 5"),
    ]
    y = table(c, y, ["Real key", "Rel. minor", "I-shape", "I-IV pattern"], open_rows,
              [1.0*inch, 0.9*inch, 1.0*inch, 4.35*inch], row_h=18)
    y -= 6

    y = h3(c, y, "CAGED Key example — D major in the feel of G")
    y = wrap(c,
             "Pick a master shape; build all seven chords of the key from inside it. Stays in one playing "
             "position. Below: each chord of D major when you're anchored in the G-shape (7th position).",
             MX, y, PAGE_W - 2*MX, SANS, 10, 13, INK)
    y -= 4
    caged_key = [
        ("I  (D)",       "G-Shape"),
        ("ii (Em)",      "A-Shape"),
        ("iii (F#m)","C-Shape"),
        ("IV (G)",       "C-Shape"),
        ("V  (A)",       "D-Shape"),
        ("vi (Bm)",      "E-Shape"),
        ("vii° (C#dim)", "E-Shape"),
    ]
    col_w = (PAGE_W - 2*MX) / 4
    rows_per_col = 2
    sy = y
    for i, (chord, shape) in enumerate(caged_key):
        col = i // rows_per_col
        row = i % rows_per_col
        cx = MX + col * col_w
        cy = sy - row * 16
        c.setFont(SERIF_B, 11); c.setFillColor(ACCENT)
        c.drawString(cx, cy, chord)
        c.setFont(SANS, 10); c.setFillColor(INK)
        c.drawString(cx + 0.7 * inch, cy, shape)
    y = sy - (rows_per_col * 16) - 12

    y = h3(c, y, "The 7 practice exercises (Naylor's framework)")
    ex = [
        ("1. Octave shapes",   "Choose 3-4 random notes; play every octave up and down the neck."),
        ("2. Barre + triads",  "Form each CAGED chord; cycle through string sets with a metronome."),
        ("3. Muscle memory",   "Build each layer Root-to-Root, in free time, then with a click."),
        ("4. Alternating layers","Within one shape, ascend the scale, descend the pentatonic, etc."),
        ("5. Static root",     "Same root, flip between major and minor layers. Use a drone."),
        ("6. Linking shapes",  "Slide between two neighbouring shapes on string 1 or 6."),
        ("7. The Walkabout",   "Move through all 5 shapes across the whole fretboard. Three variations."),
    ]
    for label, body in ex:
        c.setFont(SERIF_B, 10); c.setFillColor(ACCENT)
        c.drawString(MX, y, label)
        c.setFont(SANS, 10); c.setFillColor(INK)
        wrap(c, body, MX + 1.5 * inch, y, PAGE_W - 2*MX - 1.5 * inch, SANS, 10, 13, INK)
        y -= 16
    y -= 6

    # Final box
    box_h = 0.75 * inch
    c.setFillColor(SOFT); c.rect(MX, y - box_h, PAGE_W - 2*MX, box_h, fill=1, stroke=0)
    c.setFont(SANS_B, 9); c.setFillColor(ACCENT)
    c.drawString(MX + 12, y - 16, "THE WHOLE BOOK IN ONE LINE")
    c.setFont(SERIF_I, 12); c.setFillColor(INK)
    wrap(c,
         "If you can see the root notes, the CAGED logic bridges the gaps. Everything else is layers on top.",
         MX + 12, y - 34, PAGE_W - 2*MX - 24, SERIF_I, 12, 15, INK)

    footer(c, 4, 4)

def main():
    c = canvas.Canvas(OUT, pagesize=LETTER)
    page_1(c); c.showPage()
    page_2(c); c.showPage()
    page_3(c); c.showPage()
    page_4(c); c.showPage()
    c.save()
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
