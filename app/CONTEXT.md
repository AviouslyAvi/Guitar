# app/ — The webapps

Three Next.js 15 apps in one folder, all single-user, localStorage-only, no DB.

## Subprojects

| Folder | What it is |
|---|---|
| `fretboard-tutor/` | **The primary app.** Guitar fretboard fluency — Learn (lessons + Tutor side panel) + Test (click-the-fret drill). |
| `fretboard-tutor-piano/` | Piano variant of the same shell. |
| `piano/` | Earlier/alternate piano build. |

## Conventions (all apps)

- Stack: Next.js 15 App Router · TypeScript · Tailwind v4 · shadcn/ui · pnpm · Vercel AI SDK (optional).
- `LLM_PROVIDER=none` is the default — app works fully offline.
- Two sections: `/learn` and `/test`. No `/quiz`, no `/progress`, no standalone `/tutor` (those folded into Learn).
- Desktop-first. Mobile polish is deferred.
- All state in `localStorage`. No accounts.

## Load / skip

- Pick the one subproject you're working in and read its `src/` and `package.json`. Don't load all three.
- `node_modules/`, `.next/`, `dist/`, `build/` — **skip**.
- Key files in `fretboard-tutor`:
  - `src/lib/lessons.ts` — lesson body copy (**don't rewrite without Avi**)
  - `src/lib/curriculum.ts` — curriculum data structure
  - `src/app/learn/` and `src/app/test/` — the two main routes

## Run

```bash
cd app/fretboard-tutor    # or the variant
pnpm install
pnpm dev
```

Desktop launcher: `~/Desktop/Fretboard Tutor.command` kills `:3000`, runs `pnpm dev`, opens the browser.

## Relevant skills

- `vercel:nextjs` — for Next.js App Router questions
- `vercel:shadcn` — for shadcn/ui component patterns
- `vercel:ai-sdk` — only if working on the Tutor panel's AI integration
