# Step 9 — SM-2 spaced repetition (`lib/srs.ts`)

**Model:** Opus 4.7 (`claude-opus-4-7`) — schema + algorithm choices ripple through every drill session afterward.

**Goal:** Add spaced repetition. Each weak string/fret pair gets `easeFactor`, `interval`, `nextReviewAt`. The next session surfaces due items first. Generic engine — piano will reuse it for chords.

**Source:** piano sprint plan's "Steal from Piano → Apply to Guitar" — listed High priority. Avi already has session-history data; this turns it into resurfacing.

**Depends on:** restructure (steps 1–7) complete. Could land before or after Pomodoro (step 8) — independent.

## Pre-reqs to read in this chat

- `app/fretboard-tutor/src/lib/storage.ts` — current session/answer recording
- `app/fretboard-tutor/src/lib/drill-engine.ts` (from step 3) — where SRS hooks in
- The SM-2 algorithm (one paragraph; Wikipedia "SuperMemo SM-2" is enough)

## What to build

1. **`src/lib/srs.ts`** — generic over item ID type:
   ```ts
   export type SrsItem = {
     id: string;                  // e.g. "guitar:string-6:fret-5" or "piano:Cmaj9:A-form"
     easeFactor: number;          // default 2.5
     interval: number;            // days to next review; default 1
     nextReviewAt: string;        // ISO timestamp
     lastResult?: "pass" | "fail";
     reps: number;                // total reviews
   };
   export function review(item: SrsItem, result: "pass" | "fail", now = new Date()): SrsItem;
   export function dueItems(items: SrsItem[], now = new Date()): SrsItem[];
   export function scheduleNew(id: string, now = new Date()): SrsItem;
   ```
   SM-2 lite: pass → `interval *= easeFactor`, ease nudges up; fail → `interval = 1`, ease nudges down (floor 1.3).
2. **`src/lib/storage.ts`** — additive:
   ```ts
   guitarSrs?: { items: SrsItem[] };
   ```
   Read with `?? { items: [] }`. No migration.
3. **Drill integration** — when `<FretboardTest>` records a wrong answer, register/update the SRS item. When starting a new round, weight the prompt selection toward due items (existing weakest-string logic still applies; SRS is layered on, not replacing).
4. **`/test` UI** — small "Reviewing N due items" pill at the top of a session if any are due. Optional, can be deferred.

## What NOT to do

- Do not name the file `guitar-srs.ts`. It's generic. Piano will use the same engine with different item IDs.
- Do not write a full Anki clone. SM-2 lite is enough.
- Do not change existing streak-credit rules.
- Do not require Pomodoro (step 8) — independent.

## Files affected

- Add: `src/lib/srs.ts`
- Modify: `src/lib/storage.ts` (additive), `src/lib/drill-engine.ts`, `src/app/test/page.tsx`
- Reference (read-only): existing storage/session helpers

## Verification

```bash
cd app/fretboard-tutor
pnpm build
pnpm dev
```

Walk:
1. `/test` → miss "string 6 fret 5" three times → close session.
2. Inspect localStorage → `guitarSrs.items` has the entry, `nextReviewAt` near today.
3. Start a fresh `/test` round → that prompt appears early.
4. Pass it twice → `interval` increases, `nextReviewAt` pushes ~6 days out.
5. Fail it once → `interval` resets to 1.
6. Items not yet seen still appear at normal frequency (SRS is additive, not exclusive).

## Hand-off when done

Commit: `feat: SM-2 spaced repetition for guitar drill`. Note: "engine generic; piano sprint will reuse".
