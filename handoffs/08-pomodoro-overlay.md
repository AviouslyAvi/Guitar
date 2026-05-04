# Step 8 — `<PomodoroOverlay>` enforced focus breaks

**Model:** Sonnet 4.6 (`claude-sonnet-4-6`) — UI overlay + small state machine, no architectural decisions.

**Goal:** Build a generic, topic-agnostic `<PomodoroOverlay>` that enforces 5-minute breaks between focus blocks. Wire it into `/test` so the guitar drill gets ADHD-friendly forced rest. Same component will be reused by `/piano` later.

**Source:** lifted from the piano sprint plan's "Steal from Piano → Apply to Guitar" list (high priority).

**Depends on:** restructure (steps 1–7) complete. This is a follow-up enhancement, not part of the core restructure.

## Pre-reqs to read in this chat

- `app/fretboard-tutor/src/lib/storage.ts` — pomodoro config lives in settings
- `app/fretboard-tutor/src/app/test/page.tsx` — host of the overlay
- `app/fretboard-tutor/AGENTS.md` — animation/feedback UX rules

## What to build

1. **`src/components/pomodoro-overlay.tsx`** — full-screen overlay (shadcn Dialog primitive). Props:
   ```ts
   type Props = {
     focusMinutes: number;     // default 15
     breakMinutes: number;     // default 5
     mode: "focus" | "break";
     onPhaseEnd: (next: "focus" | "break") => void;
     allowSkip?: boolean;      // default true; logs the skip
   };
   ```
   Auto-advances from focus → break → focus. During break, locks navigation away; can skip with explicit "Skip break" button (logged).
2. **`src/lib/pomodoro.ts`** — pure timer state machine. `start`, `pause`, `tick`, `phaseEnd`. No React, no DOM.
3. **Settings extension** in `storage.ts`:
   ```ts
   pomodoroFocusMinutes: z.number().int().min(5).max(60).default(15),
   pomodoroBreakMinutes: z.number().int().min(2).max(15).default(5),
   pomodoroEnabled: z.boolean().default(false),  // off by default, opt-in
   ```
4. **Wire into `/test`** — when `pomodoroEnabled`, after each round (or after N answers configurable), the overlay appears. ESC does NOT close it during break. Skip button is visible.
5. **Settings UI** — a "Focus mode" section with: enable toggle, focus minutes (slider 5–60), break minutes (slider 2–15). Defaults: 15/5 (ADHD-evidence-based per piano plan).

## What NOT to do

- Do not enable Pomodoro by default. Opt-in via Settings. Avi may dislike forced breaks — let him choose.
- Do not gate `/learn` lessons behind Pomodoro — only `/test`.
- Do not bake "guitar" into the component or lib — `<PomodoroOverlay>` and `lib/pomodoro.ts` are reusable by `/piano`.
- Do not log break skips to AI/telemetry — localStorage only.

## Files affected

- Add: `src/components/pomodoro-overlay.tsx`, `src/lib/pomodoro.ts`
- Modify: `src/lib/storage.ts` (additive), `src/app/test/page.tsx`, `src/app/settings/page.tsx`
- Reference (read-only): `AGENTS.md`

## Verification

```bash
cd app/fretboard-tutor
pnpm build
pnpm dev
```

Walk:
1. `/settings` → enable Focus mode, set 1/1 (1-minute focus, 1-minute break for fast testing).
2. `/test` → start a round → after the focus minute elapses, overlay appears with 1-min countdown.
3. ESC during break → does nothing.
4. Click Skip break → overlay closes; localStorage shows the skip event count incremented.
5. Let break run out → overlay closes automatically, drill resumes.
6. Disable Focus mode → `/test` works without overlay.

## Hand-off when done

Commit: `feat: pomodoro overlay (opt-in)`. Note: "generic component; piano sprint will reuse".
