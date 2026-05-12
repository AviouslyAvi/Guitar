# build-scripts/ — Printable PDF generators

Python 3 scripts that emit printable reference sheets (CAGED system charts, fretboard notes worksheets). Output PDFs land at repo root (e.g. `Fretboard-Notes-3-Weeks.pdf`).

## Files

| Script | Output |
|---|---|
| `build_caged_pdf.py` | Full CAGED reference PDF |
| `build_caged_one_page.py` | Condensed one-page CAGED chart |
| `build_caged_ref.py` | Detailed CAGED reference build |
| `build_notes_page.py` | 3-week fretboard notes worksheet |
| `fonts/` | Embedded fonts for the generated PDFs |

## Load / skip

- Read the script you're editing; they're standalone.
- Don't `Read` the `fonts/` binaries.

## Pipeline

Run individually with `python3 build_<name>.py`. Each prints to a hardcoded output path (check the top of the script). Uses `reportlab` (and possibly `pdfplumber`/`pypdf`) — see the `pdf` skill.

## Relevant skills

- `pdf` / `anthropic-skills:pdf` — for layout, generation, visual verification.
