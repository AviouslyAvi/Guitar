# Step 5 — Embed `<FretboardTest>` in lessons

**Model:** Sonnet 4.6 (`claude-sonnet-4-6`) — wiring an existing component into existing pages with a small scope helper. No new architectural calls.

**Goal:** Render the test inline at the bottom of every lesson, scope locked to that lesson's strings/frets/accidentals, no customization controls. Below it, an "Open full test" link to `/test?preset=lesson:<slug>`.

**Depends on:** steps 3 + 4 complete.

## Pre-reqs to read in this chat

- `app/fretboard-tutor/src/app/learn/[slug]/page.tsx`
- `app/fretboard-tutor/src/lib/lessons.ts` — read each lesson's `drill` target (strings + frets); DO NOT modify body content
- `app/fretboard-tutor/src/components/fretboard-test.tsx`
- `app/fretboard-tutor/src/lib/storage.ts` — `lessonsCompleted` write

## What to build

1. In `src/app/learn/[slug]/page.tsx`, after the lesson body + diagrams, render:
   ```tsx
   <FretboardTest
     scope={lessonScope(slug)}
     fromLesson={slug}
     showSettings={false}
     onComplete={(result) => {
       if (result.total >= 10) markLessonComplete(slug);
     }}
   />
   ```
2. **`lessonScope(slug)`** — small helper in `src/lib/lessons.ts` (or new `src/lib/lesson-scope.ts`) that maps slug → `Scope`. Use the existing `drill` field on each lesson.
3. **Below the inline test:** brass capsule link `Open full test →` to `/test?preset=lesson:${slug}`.
4. **Welcome lesson** (`/learn` index): no embedded test — it's the intro. Show a dimmed "Pick a lesson to start drilling" placeholder where the test would be.
5. **Marking complete:** lesson is marked complete after ≥10 answered (same gate as streak credit). Idempotent — no harm if already complete.

## What NOT to do

- Do not modify lesson body content.
- Do not let the lesson user customize the scope inline (`showSettings={false}` enforces this).
- Do not duplicate the score strip — `<FretboardTest>` renders its own.
- Do not delete `/quiz` yet (step 6).

## Files affected

- Modify: `src/app/learn/[slug]/page.tsx`, `src/lib/lessons.ts` (add helper only), possibly `src/app/learn/page.tsx` (placeholder)
- Reference (read-only): `<FretboardTest>`, storage helpers

## Verification

```bash
cd app/fretboard-tutor
pnpm build
pnpm dev
```

Walk:
1. `/learn/w1-alphabet` → scroll to bottom → inline test renders with the lesson's scope, no settings controls.
2. Click correct fret → score updates inline. No customization UI visible.
3. Land 10 answers → lesson row in the TOC shows completion ring filled.
4. Click "Open full test →" → lands on `/test?preset=lesson:w1-alphabet` with same scope locked.
5. Refresh `/learn/w1-alphabet` → completion persists; ring stays filled.
6. `/learn` index → welcome placeholder, no test.
7. Tutor button still works (step 2 not regressed).
8. Console errors: none.

## Hand-off when done

Commit: `learn: embed FretboardTest inline at lesson bottom`. Note: "lessons now self-contained; /quiz still routable but unused — deleted in step 6".
