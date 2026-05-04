# Guitar

Personal fretboard-learning project. A single-user webapp for naming every note on the guitar neck, plus the supporting course content and build tooling.

## What's here

```
.
├── app/fretboard-tutor/   # Next.js 15 webapp (the actual product)
├── build-scripts/         # Python scripts that generate CAGED + notes PDFs
├── BUILD-PROMPT.md        # Spec used to bootstrap the app
├── COURSE-PLAN.md         # Working spec for the /learn section
└── HANDOFF.md             # Session-to-session resume notes
```

## App: Fretboard Tutor

Next.js 15 · TypeScript · Tailwind v4 · shadcn/ui · pnpm. localStorage only — no DB, no auth. Optional AI tutor via Vercel AI SDK (LM Studio, OpenAI, or Anthropic); defaults to `LLM_PROVIDER=none` so the app works fully offline.

Routes: `/` landing · `/app` hub · `/learn` 3-week course · `/quiz` note drill · `/tutor` chat · `/settings` · `/progress`.

```bash
cd app/fretboard-tutor
pnpm install
pnpm dev
```

Desktop launcher: `~/Desktop/Fretboard Tutor.command` kills `:3000`, runs `pnpm dev`, opens the browser.

## Course

10 lessons across 3 weeks of note fluency — alphabet and open strings → reference points and sharps/flats → unisons, octaves, and full-neck integration. Lesson copy lives in `app/fretboard-tutor/src/lib/lessons.ts`. Curriculum data lives in `src/lib/curriculum.ts`.

## Build scripts

`build-scripts/` generates printable PDFs (CAGED reference, one-page CAGED, 3-week notes worksheet). Run individually with Python 3.

## Resume / handoff

`HANDOFF.md` is the source of truth for session state, gotchas, and next threads. Read it first.
