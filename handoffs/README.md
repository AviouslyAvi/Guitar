# Restructure handoffs — Learn + Test (multi-chat workflow)

These docs break the Fretboard Tutor restructure (collapse from 5 sections to 2 — Learn + Test) into one focused chat per step. Each handoff is **self-contained**: open it in a fresh Claude chat, paste the contents, and the chat has everything it needs. **Multiple chats can run in parallel** when their steps are independent — see the dependency graph below.

## Read these once before starting (any chat, any step)

- `../BRIEF.md` — product intent (small)
- `../HANDOFF.md` — project state, restructure overview, rules
- `../COURSE-PLAN.md` — curriculum + routes
- `PEDAGOGY.md` — 3-week method, anchor notes, octave shapes, drill protocol, tips & tricks, reference sources

## Files chats should NOT read (token-savers)

- `../Fretboard+Mastery+eBook+(2025).pdf` — 17 MB. On disk for Avi only. Pedagogy is in `PEDAGOGY.md`.
- `../BUILD-PROMPT.md` — historical bootstrap spec, no longer relevant.
- `../app/fretboard-tutor/pnpm-lock.yaml`, `tsconfig.tsbuildinfo`, `.next/` — generated/lockfiles.
- `~/.claude/plans/*` — planning artifacts, not part of the project.
- Other lessons in `lessons.ts` when you're writing one specific lesson — read only your slug.

## Build steps

| # | File | What it builds | Depends on | Model |
|---|---|---|---|---|
| 1 | [01-learn-shell.md](01-learn-shell.md) | `<LearnToc>` + two-column `/learn` shell | — | **Opus 4.7** |
| 2 | [02-tutor-panel.md](02-tutor-panel.md) | `<TutorPanel>` right slide-over | 1 (for placement) | Sonnet 4.6 |
| 3 | [03-fretboard-test-component.md](03-fretboard-test-component.md) | `<FretboardTest>` component | — | **Opus 4.7** |
| 4 | [04-test-page.md](04-test-page.md) | `/test` page with settings + persisted prefs | 3 | **Opus 4.7** |
| 5 | [05-lesson-embed.md](05-lesson-embed.md) | Embed `<FretboardTest>` inline at lesson bottom | 1, 3 | Sonnet 4.6 |
| 6 | [06-cleanup.md](06-cleanup.md) | Prune hub, remove/redirect old routes | 1, 2, 4, 5 | Sonnet 4.6 |
| 7 | [07-walkthrough.md](07-walkthrough.md) | Manual desktop walkthrough + verification | all | Haiku 4.5 |
| 8 | [08-pomodoro-overlay.md](08-pomodoro-overlay.md) | `<PomodoroOverlay>` enforced focus breaks (opt-in) | 1–7 | Sonnet 4.6 |
| 9 | [09-srs.md](09-srs.md) | SM-2 spaced repetition in `lib/srs.ts` | 1–7 | **Opus 4.7** |
| 10 | [10-drill-game-extraction.md](10-drill-game-extraction.md) | Extract `<DrillGame>`: lives, combo, daily high score | 1–7 | **Opus 4.7** |
| Lesson copy | [LESSON-COPY-TEMPLATE.md](LESSON-COPY-TEMPLATE.md) | Per-lesson collaborative writing | structure shipped | Sonnet 4.6 |

**Why these picks:**
- **Opus 4.7** for steps 1, 3, 4 — architectural decisions (component API design, layout system, scoring engine extraction). Worth the cost when one bad call creates rework downstream.
- **Sonnet 4.6** for steps 2, 5, 6 and lesson copy — coding inside an established pattern, prose work, mechanical cleanup. Sonnet handles all of these without trouble.
- **Haiku 4.5** for step 7 — pure walkthrough/verification. No design choices, just running the script and reporting.

You can always upgrade mid-step if you hit something tricky. Don't downgrade mid-step — context already paid for.

## Dependency graph — what can run in parallel

```
Wave 1 (parallel, two chats):
  ├─ Step 1: Learn shell + TOC
  └─ Step 3: FretboardTest component

Wave 2 (parallel after Wave 1, three chats):
  ├─ Step 2: Tutor panel        (needs step 1)
  ├─ Step 4: /test page          (needs step 3)
  └─ Step 5: Lesson embed        (needs steps 1 + 3)

Wave 3 (sequential, one chat each):
  ├─ Step 6: Cleanup             (needs 1, 2, 4, 5)
  └─ Step 7: Walkthrough         (needs everything)

Wave 4 (post-restructure enhancements, parallel — three chats):
  ├─ Step 8: Pomodoro overlay    (independent)
  ├─ Step 9: SRS engine          (independent; pairs well with step 10)
  └─ Step 10: DrillGame extract  (independent)
```

You can collapse the workflow to a single chat per step, or run two/three in parallel as shown. **Do not parallelize Wave 2 with Wave 3** — cleanup must come after the new routes are wired in. Wave 4 is post-launch enhancement; ship Waves 1–3 first.

## Branching strategy — avoid chat collisions

Each chat works on its own git branch off `main`. After commit, merge to `main` before the next dependent chat starts.

```
main
 ├─ restructure/01-learn-shell      ← Step 1 chat
 ├─ restructure/02-tutor-panel      ← Step 2 chat (branches from 01 once merged)
 ├─ restructure/03-fretboard-test   ← Step 3 chat
 ├─ restructure/04-test-page        ← Step 4 chat (branches from 03 once merged)
 ├─ restructure/05-lesson-embed     ← Step 5 chat (branches from 01+03 merged)
 ├─ restructure/06-cleanup          ← Step 6 chat (branches from main with 01,02,04,05)
 └─ restructure/07-walkthrough      ← Step 7 chat (final smoke test)
```

Concretely, when starting any step in a fresh chat:

```bash
cd "/Users/aviouslyavi/Claude/Projects/Avious Music/Guitar/app/fretboard-tutor"
git checkout main
git pull
git checkout -b restructure/<step-name>
# … work …
git commit -m "<step msg>"
# Avi merges to main when satisfied; next dependent chat then pulls main
```

**Rule of thumb:** if two chats touch the same file, they're not parallelizable. The dependency graph above already enforces this — Wave 1 chats touch disjoint files, Wave 2 chats touch disjoint files, and integration happens in Wave 3.

## How to start a chat

1. Open a fresh Claude Code session in the project root.
2. Paste the contents of the relevant `0X-*.md` file as the first message.
3. The chat has everything it needs: context, files to read, what to build, what NOT to do, verification steps, and the commit message.

## Rules that apply to every step

1. **Don't touch lesson `body` content** in `src/lib/lessons.ts`. That's a separate, collaborative phase with Avi (see `LESSON-COPY-TEMPLATE.md`).
2. **Reference sources are interaction & pedagogy reference only** (musictheory.net, fretjam, TrueFire, Pickup Music, Ry Naylor) — no code copying, no copy lifting, no diagram tracing.
3. **`LLM_PROVIDER=none` must keep working** — Tutor degrades gracefully.
4. **Curriculum is fixed** — `lib/curriculum.ts` is not edited.
5. **Commit between steps.** Each step ends with `pnpm build` passing.
6. **Use `Explore` subagent for read-heavy steps** (3, 6) so the main thread stays light.
7. **Model choice:** Opus for steps 1, 3, 4, 9, 10 (architectural). Sonnet 4.6 / Haiku 4.5 for the rest.
8. **Stay in your lane.** A step's handoff lists the files it owns. Don't edit files outside that list — flag them in a follow-up note instead.
9. **Forward-compat for piano.** A `/piano` namespace is on the roadmap inside the same app. Anything in `src/lib/` or `src/components/` that's reusable across topics MUST be named generically (`lib/drill-engine.ts`, `lib/srs.ts`, `lib/pomodoro.ts`, `<DrillGame>`, `<PomodoroOverlay>`, `<TutorPanel>`) — NOT `lib/quiz-engine.ts` or `<FretboardDrillGame>`. Storage keys MUST be topic-namespaced (`fretboard-tutor:guitar:*`, never bare). Companion plan: `~/.claude/plans/i-have-been-working-delegated-riddle.md`.

## Lesson copy phase (after structure ships)

| File | What it does |
|---|---|
| [LESSON-COPY-TEMPLATE.md](LESSON-COPY-TEMPLATE.md) | Per-lesson collaborative writing template — open one chat per lesson, paste this with the slug filled in. Avi has final approval on every body. |
