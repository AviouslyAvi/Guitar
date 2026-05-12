# Guitar and Piano Tutor

Personal music-fluency project. Two webapps — a **guitar fretboard tutor** and a **piano tutor** — plus the supporting course content, build scripts for printable PDF references, and a folder of UI mockup explorations.

Single-user, local-first, no cloud. Built to fit the way Avi actually learns.

## What's here

```
app/
  fretboard-tutor/        # Next.js 15 webapp — guitar fretboard tutor (primary app)
  fretboard-tutor-piano/  # Piano tutor (Next.js)
build-scripts/            # Python scripts that generate printable PDFs
handoffs/                 # Session-to-session resume docs
mockups/                  # HTML design explorations for the Learn UI
BRIEF.md                  # What and why
BRAND.md                  # Brand / voice
COURSE-PLAN.md            # Guitar curriculum spec
PIANO-PLAN.md             # Piano curriculum spec (large — load only when relevant)
HANDOFF.md                # Top-level resume doc
```

## Apps

Both apps share the same stack: **Next.js 15 · TypeScript · Tailwind v4 · shadcn/ui · pnpm**. Desktop-first. `localStorage` only — no database, no auth, no cloud sync.

Optional AI tutor via Vercel AI SDK (LM Studio, OpenAI, or Anthropic). Defaults to `LLM_PROVIDER=none` so each app runs fully offline.

Each app has two sections:

- **Learn** — table of contents + lesson view with an inline test at the end of each lesson.
- **Test** — customizable drill (configurable scope, persisted preferences).

## Run

```bash
cd app/fretboard-tutor      # or app/fretboard-tutor-piano
pnpm install
pnpm dev
```

A desktop launcher (`~/Desktop/Fretboard Tutor.command`) kills port `:3000`, runs `pnpm dev`, and opens the browser.

## Build scripts

`build-scripts/` contains Python 3 scripts that generate printable PDFs (CAGED reference, one-page CAGED, 3-week notes worksheet). Run individually:

```bash
python3 build-scripts/build_caged_pdf.py
```

Output PDFs land alongside the script or at the repo root (e.g. `Fretboard-Notes-3-Weeks.pdf`).

## Requirements

- Node 20+ and `pnpm` (for the webapps).
- Python 3 with `reportlab` / `pdfplumber` (for the PDF build scripts).
- macOS for the `.command` launcher (the webapps run anywhere Node does).

## Course content

Lesson copy lives in `app/fretboard-tutor/src/lib/lessons.ts`; curriculum data in `app/fretboard-tutor/src/lib/curriculum.ts`. **Lesson body copy is a collaborative pass** — Avi writes it in his own voice, one chat per lesson. Don't unilaterally rewrite `lessons.ts` body text during structural refactors.

## Reference material — pedagogy only

`Fretboard+Mastery+eBook+(2025).pdf` (Ry Naylor) and online sources (musictheory.net, fretjam, TrueFire, Pickup Music) inform interaction model and pedagogy only. **No code, copy, or diagrams are lifted from any source.** All UI is original; all prose is Avi's.

## Status

Active. Guitar app is the more mature of the two; piano app is being scaffolded against `PIANO-PLAN.md`. See `HANDOFF.md` for the live state of work.

## For contributors / AI

`CLAUDE.md` at the repo root is the router. Each subfolder has a `CONTEXT.md` with room-specific conventions. Start at `CLAUDE.md`.
