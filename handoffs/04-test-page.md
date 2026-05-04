# Step 4 — `/test` page

**Model:** Opus 4.7 (`claude-opus-4-7`) — settings model, persisted preferences, and lesson-preset routing are decisions that shape how `<FretboardTest>` is consumed everywhere else.

**Goal:** Build the standalone `/test` page that hosts `<FretboardTest>` with a customizable settings panel. Persists settings to localStorage. Supports `?preset=lesson:<slug>` to lock scope and hide the panel.

**Depends on:** step 3 complete.

## Pre-reqs to read in this chat

- `app/fretboard-tutor/src/components/fretboard-test.tsx` (from step 3)
- `app/fretboard-tutor/src/lib/storage.ts` — add a `testSettings` blob; mirror existing additive-pattern (`?? defaults`)
- `app/fretboard-tutor/src/lib/curriculum.ts` — for lesson-preset → scope mapping

## What to build

1. **`src/app/test/page.tsx`** — single column, max ~960px, three zones top→bottom:
   - **Settings panel (collapsible):** strings (1–6 checkboxes), fret range (slider 0–12 / 0–24), accidentals radio (naturals / naturals+sharps / all), question count (10 / 25 / open).
   - **`<FretboardTest>`** with the current scope.
   - **Live score strip** is rendered inside the component — page just hosts.
2. **Defaults:** Week 1 scope on first visit (`{ strings: [6,5], frets: [0,12], accidentals: "naturals" }`). After first session, persist last-used settings.
3. **Storage (topic-namespaced for forward-compat with `/piano`):** persist as `fretboard-tutor:guitar:test-settings` (or whatever namespace pattern the existing storage layer uses — match it). **Do NOT use a bare `testSettings` key** — piano will need its own settings under `fretboard-tutor:piano:*` and bare keys collide. Schema:
   ```ts
   guitarTestSettings?: {
     strings: number[];
     frets: [number, number];
     accidentals: "naturals" | "naturals+sharps" | "all";
     limit: number | null;
   };
   ```
   Read with `?? defaults`. No migration.
4. **Lesson preset:** `?preset=lesson:w1-roots` → look up the slug in `lessons.ts` (or a small `slug → scope` map), hide the settings panel, render a pill at top: "Lesson scope · open full test" linking to `/test`.

## What NOT to do

- Do not embed in lessons yet (step 5).
- Do not delete `/quiz` (step 6).
- Do not change `<FretboardTest>` internals — extend props if needed but treat the component as stable.
- Do not modify curriculum data.

## Files affected

- Add: `src/app/test/page.tsx`
- Modify: `src/lib/storage.ts` (additive)
- Reference (read-only): `<FretboardTest>`, `lessons.ts`, `curriculum.ts`

## Verification

```bash
cd app/fretboard-tutor
pnpm build
pnpm dev
```

Walk:
1. Visit `/test` directly → settings panel expanded with Week 1 defaults.
2. Change strings to [4, 3], fret range to [0, 7], accidentals to all → click Start → drill matches scope.
3. Refresh `/test` → settings remember the last choice.
4. Visit `/test?preset=lesson:w1-alphabet` → settings panel hidden, scope locked to that lesson, "Open full test" pill at top → clicking it returns to `/test` with the persisted settings.
5. Land 10 answers → streak credit applied; weekly gate logic still works against the existing rule.
6. `LLM_PROVIDER=none` → page works unchanged (no AI here anyway).

## Hand-off when done

Commit: `feat: /test page with customizable scope`. Note: "preset preview works for lessons; lessons themselves still link to /quiz until step 5".
