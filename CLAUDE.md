# Guitar and Piano Tutor — Router

Personal music-fluency project. Two webapps (guitar fretboard tutor + piano tutor) plus the supporting course content, build tooling for printable PDF references, and a set of UI mockup explorations.

## Folder map

| Folder / file | What's there | Notes |
|---|---|---|
| `app/` | The actual Next.js 15 webapps (`fretboard-tutor/`, `fretboard-tutor-piano/`, `piano/`) | See `app/CONTEXT.md` |
| `build-scripts/` | Python scripts that generate printable PDFs (CAGED, notes worksheet) | See `build-scripts/CONTEXT.md` |
| `handoffs/` | Session-to-session resume docs (one per planned/ongoing thread) | See `handoffs/CONTEXT.md` |
| `mockups/` | HTML design explorations (10+ themed mockups for the Learn UI) | See `mockups/CONTEXT.md` |
| `BRIEF.md` | Why this exists, problem framing | Safe entry doc |
| `BRAND.md` | Brand/voice notes | |
| `COURSE-PLAN.md` | Curriculum spec for the guitar `/learn` section | |
| `PIANO-PLAN.md` | Curriculum spec for the piano tutor (41 KB — load only when working on piano) | |
| `BUILD-PROMPT.md` | Spec used to bootstrap the app | Reference; rarely edit |
| `MOCKUPS.md` | Index/notes for the mockups folder | |
| `HANDOFF.md` | **Top-level resume doc** — read first when picking up a session | |
| `REBRAND-BRIEF.md` | Rebrand exploration | |
| `README.md` | Project overview | |
| `Fretboard+Mastery+eBook+(2025).pdf` | Large reference PDF (~17 MB) — **don't load** | Pedagogical reference only |
| `Fretboard-Notes-3-Weeks.pdf` | Generated 3-week notes worksheet | Build-script output |

## Conventions

- Next.js 15 · TypeScript · Tailwind v4 · shadcn/ui · pnpm. Desktop-first.
- `localStorage` only — no DB, no auth, no cloud sync.
- Optional AI tutor via Vercel AI SDK; defaults to `LLM_PROVIDER=none` so the app runs fully offline.
- **Lesson copy is collaborative.** Don't unilaterally rewrite body text in `app/fretboard-tutor/src/lib/lessons.ts` — Avi writes those in his own voice during focused chats.
- Reference material (Ry Naylor's *Fretboard Mastery* PDF, musictheory.net, fretjam, TrueFire, Pickup Music) is for **interaction-model and pedagogy reference only** — no code, copy, or diagram lifting.

## Task → room

| Task | Go to |
|---|---|
| Resume a session / pick up where we left off | `HANDOFF.md` first, then `handoffs/` |
| Build / edit the guitar webapp | `app/CONTEXT.md` → `fretboard-tutor/` |
| Build / edit the piano webapp | `app/CONTEXT.md` → `fretboard-tutor-piano/` or `piano/`; load `PIANO-PLAN.md` |
| Edit a lesson's body copy | `app/fretboard-tutor/src/lib/lessons.ts` — **with Avi**, not unilaterally |
| Curriculum structure changes | `COURSE-PLAN.md` (guitar) or `PIANO-PLAN.md` |
| Generate / edit a printable PDF | `build-scripts/CONTEXT.md` |
| Browse UI design directions | `mockups/CONTEXT.md` |
| Reference the Fretboard Mastery ebook | Don't load it. Cite by chapter if needed. |
