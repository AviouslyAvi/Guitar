# Step 3 — `<FretboardTest>` component

**Model:** Opus 4.7 (`claude-opus-4-7`) — defines the component API every other step depends on; extracts scoring logic without breaking it.

**Goal:** Build a reusable click-the-fret test component. Given a scope (strings, fret range, naturals/sharps/double-accidentals), it shows a target note ("Click every F#"), the user clicks the fret on the SVG fretboard, and it scores them. Same scoring rules as existing `/quiz`.

**Estimated scope:** medium. Pure component + extracted logic. Read-heavy — use `Explore` subagent to map `src/app/quiz/*`.

## Use Explore subagent first

Spawn an `Explore` agent with this brief:

> Map every file under `app/fretboard-tutor/src/app/quiz/` and any helpers it imports from `src/lib/`. Return: (1) the answer-checking function, (2) the streak / accuracy / session-recording functions in `storage.ts`, (3) the data structure for a "prompt" (string + fret + expected note), (4) the early-stop "I'm tired" recap path, (5) the hydration-mismatch fix referenced in HANDOFF.md. Do NOT propose changes; just report file paths, function names, and signatures. Keep the report under 300 words.

## Pre-reqs to read in this chat (after Explore reports back)

Whatever the Explore agent flagged. Likely:
- `src/app/quiz/page.tsx`
- `src/lib/storage.ts` — session recording, streak gate (≥10 answers), accuracy
- existing `<Fretboard>` SVG component (per `COURSE-PLAN.md`, may live as `components/fretboard.tsx`)

## Architecture rule (forward-compat for piano)

`/piano` is on the roadmap and will need the same drill loop (lives, scoring, streaks, "I'm tired" recap). To avoid a painful refactor later:

- **All scoring/progression/recap logic lives in `src/lib/drill-engine.ts`** — pure functions, no React, no fretboard concepts.
- **`<FretboardTest>` is a thin guitar-specific shell** that wires the engine to the SVG fretboard and click handlers.
- **Do not name the engine module `quiz-engine.ts` or `fretboard-engine.ts`.** It's a generic drill engine; piano will reuse it.
- Engine API sketch:
  ```ts
  // lib/drill-engine.ts
  export type DrillItem<T> = { prompt: T; answer: unknown };
  export type DrillState<T> = { items: DrillItem<T>[]; index: number; correct: number; wrong: number; streak: number };
  export function nextItem<T>(state: DrillState<T>): DrillState<T>;
  export function recordAnswer<T>(state: DrillState<T>, correct: boolean): DrillState<T>;
  export function shouldCreditStreak(state: DrillState<T>): boolean;  // existing >=10 rule
  ```
- The engine reads/writes session results via callback props from `<FretboardTest>`, not by importing storage directly. Storage stays one layer up.

## What to build

1. **`src/components/fretboard-test.tsx`** — props:
   ```ts
   type Scope = {
     strings: number[];          // 1..6
     frets: [number, number];    // [low, high], inclusive
     accidentals: "naturals" | "naturals+sharps" | "all";
     limit?: number;             // optional question count; null = open
     showSettings?: boolean;     // if true, render scope controls; default false
   };
   type Props = {
     scope: Scope;
     onComplete?: (result: { correct: number; total: number; weakestString?: number }) => void;
     fromLesson?: string;        // lesson slug if embedded
   };
   ```
2. **Interaction model** (informed by musictheory.net but original code):
   - Show target note above the board: "Click every **F#**"
   - User clicks a fret cell on the SVG. Correct → brass flash + tone, advance. Wrong → ink flash + reveal correct fret for ~1.5s, then advance.
   - Live score strip: correct/total, accuracy %, streak.
   - "I'm tired" early-stop button reuses existing recap (weakest-string drill suggestion).
3. **Hydration:** first prompt is deterministic (matches existing fix in `quiz/page.tsx`); randomize after mount.
4. **Scoring:** call into the same storage helpers `/quiz` uses today. Streak credit gates at `total >= 10` — do not change that rule.

## What NOT to do

- Do not delete or modify `src/app/quiz/page.tsx` yet (step 6).
- Do not change scoring rules in `storage.ts`.
- Do not add a settings panel inside the component yet — `showSettings` exists but its UI lands in step 4.
- Do not copy any code from musictheory.net or fretjam. Behavior reference only.

## Files affected

- Add: `src/components/fretboard-test.tsx`, `src/lib/drill-engine.ts`
- Modify: extract scoring/progression helpers from `quiz/page.tsx` into `src/lib/drill-engine.ts`. If extraction is risky, copy the logic into `drill-engine.ts` and leave `/quiz` alone — step 6 deletes it.
- Reference (read-only): `quiz/page.tsx`, `storage.ts`, existing fretboard SVG

## Verification

Component is not yet wired into any page. Verify in isolation:
1. Add a temporary `/test-preview` route that renders `<FretboardTest scope={{ strings: [6,5], frets: [0,12], accidentals: "naturals" }} />`.
2. Click correct fret → brass flash, score increments.
3. Click wrong fret → ink flash, correct fret revealed.
4. Land 10 answers → streak credit applied (check storage).
5. "I'm tired" → recap renders.
6. `pnpm build` passes.
7. **Delete the temp route** before committing.

## Hand-off when done

Commit: `feat: FretboardTest component (click-the-fret)`. Note: "/quiz still primary; /test page lands in step 4".
