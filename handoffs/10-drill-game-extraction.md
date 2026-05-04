# Step 10 — Extract `<DrillGame>` (lives, combo, daily high score)

**Model:** Opus 4.7 (`claude-opus-4-7`) — refactor of the core drill component; shape ripples through both topics.

**Goal:** Refactor `<FretboardTest>` into a generic `<DrillGame>` + a thin guitar adapter. Add the dopamine-engine mechanics from the piano plan: 3 lives per round, combo multiplier (x2 on 5-streak, x3 on 10-streak), daily high score per item type.

**Source:** piano sprint plan's "Steal from Piano → Apply to Guitar" — listed High priority. The piano `<ChordTimerGame>` is supposed to share this base; building it generically once is much cheaper than building twice.

**Depends on:** steps 1–7 (restructure) complete. Step 9 (SRS) optional but synergizes well — if SRS is in, due items get the lives/combo treatment too.

## Pre-reqs to read in this chat

- `app/fretboard-tutor/src/components/fretboard-test.tsx`
- `app/fretboard-tutor/src/lib/drill-engine.ts` (from step 3) — already engine-shaped; this step extracts the *render layer*
- `app/fretboard-tutor/AGENTS.md` — animation/feedback rules

## What to build

1. **`src/components/drill-game.tsx`** — generic, item-type-parameterized:
   ```ts
   type Props<TItem, TInput> = {
     items: TItem[];
     renderPrompt: (item: TItem) => ReactNode;
     renderInput: (onAnswer: (input: TInput) => void) => ReactNode;
     checkAnswer: (item: TItem, input: TInput) => boolean;
     lives?: number;             // default 3
     comboTiers?: { streak: number; multiplier: number }[];  // default [{5,2},{10,3}]
     onRoundComplete: (score: { correct: number; wrong: number; bestCombo: number; points: number }) => void;
   };
   ```
2. **Lives:** start at 3. Wrong answer → -1 life, ink flash + reveal. 0 lives → round ends with recap.
3. **Combo:** consecutive correct increments combo counter. Hits the tiers → multiplier kicks in for points. Wrong resets combo.
4. **Points:** `points = baseValue * multiplier`. Track session total + daily high score per topic in storage.
5. **`<FretboardTest>`** — refactor to be a thin wrapper around `<DrillGame>`:
   - `renderPrompt` shows the target note
   - `renderInput` is the SVG fretboard with click handlers
   - `checkAnswer` compares clicked fret to expected
6. **Storage additions:**
   ```ts
   dailyHighScores?: Record<string, { date: string; points: number }>;
   // key: `guitar:drill` etc. Piano will use `piano:drill`.
   ```
7. **UX (per AGENTS.md):**
   - Combo milestone (x2, x3) triggers a sonner toast.
   - Last life lost → red flash + small "Out of lives" pulse, then recap. No game-over screen wall.
   - Animations support feedback; never block reading.

## What NOT to do

- Do not bake guitar concepts into `<DrillGame>` or its props. The component is type-generic.
- Do not change the existing streak-credit rule (≥10 answers gates the 1-day streak). Combo + lives are additive — separate from the daily streak system.
- Do not break `<FretboardTest>`'s public API — pages that consume it (the inline lesson embed, `/test`) keep working without changes.
- Do not name the storage key with "fretboard" — `guitar:drill` for the topic prefix.

## Files affected

- Add: `src/components/drill-game.tsx`
- Modify: `src/components/fretboard-test.tsx` (becomes a thin wrapper), `src/lib/storage.ts` (additive), possibly `src/lib/drill-engine.ts` if combo/lives logic belongs in the engine instead of the component
- Reference (read-only): `AGENTS.md`

## Verification

```bash
cd app/fretboard-tutor
pnpm build
pnpm dev
```

Walk:
1. `/test` or any embedded lesson test → 3 lives indicator visible.
2. Get 5 in a row → combo x2 toast, points displayed accelerate.
3. Get 10 in a row → x3 toast.
4. Miss once → combo resets, multiplier returns to x1.
5. Miss 3 total in a round → round ends, recap shows correct/wrong/best-combo/points + daily high score.
6. Daily high score persists across page reloads (localStorage).
7. Existing flows unchanged: streak credit at ≥10 still triggers, "I'm tired" recap still works, lesson completion ring still fills.

## Hand-off when done

Commit: `refactor: DrillGame generic + lives/combo for guitar`. Note: "piano sprint can adopt without rewriting".
