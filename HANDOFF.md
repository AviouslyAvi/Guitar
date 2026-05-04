# Handoff — Fretboard Tutor

Read this once, then resume in `app/fretboard-tutor/`.

## What this is

A personal fretboard-learning webapp for naming every guitar note. Single-user-per-browser via localStorage. Public-facing copy. No accounts, no DB, no paid APIs by default.

```
/Users/aviouslyavi/Claude/Projects/Avious Music/Guitar/
├── HANDOFF.md
└── app/fretboard-tutor/
    ├── AGENTS.md      # read first in a new session
    └── src/
```

Desktop launcher: `~/Desktop/Fretboard Tutor.command` kills `:3000`, runs `pnpm dev`, opens browser.

## Stack

- Next.js 15.5 App Router · TypeScript · Tailwind v4 · shadcn/ui · pnpm
- Vercel AI SDK (`ai`, `@ai-sdk/openai`, `@ai-sdk/anthropic`, `@ai-sdk/react`)
- localStorage state in `src/lib/storage.ts`
- Default tutor: LM Studio at `http://localhost:1234/v1`, model `gemma-4-e4b-it-mlx`
- Default `LLM_PROVIDER=none`; app must still work without AI

## Current State

Routes (current — being restructured to two sections, see "Restructure In Flight" below):

- `/` — public landing, CTA to `/app`
- `/app` — hub with Learn, Quiz, Tutor, Settings capsules
- `/learn` — 3-week course overview with left course path and compact trajectory cards
- `/learn/[slug]` — lesson content with the same course path on the left
- `/quiz` — piano-style note drill, supports `?strings=4,3`, `?frets=0,5,7,12`, `?fromLesson=<slug>`
- `/tutor` — chat; supports queued prompts while assistant is streaming
- `/settings` — timer, daily goal, week override, provider config
- `/progress` — streak, accuracy, answered count, 7-day band, today, recent sessions

Theme:

- Light parchment theme lives in `globals.css` `.dark` block and is currently the effective theme.
- `text-parchment` means primary ink text inside cards.
- `.sun-arc` must be a separate child div inside a relative/overflow-hidden card.

## Completed In Latest Session

Implemented the previously pending handoff items:

1. Quiz stop flow
   - `src/app/quiz/page.tsx`
   - User-facing early stop action is `I'm tired`.
   - Old secondary `Stop` link is now `Back`.
   - Early stop now shows a recap instead of immediately leaving:
     - overall accuracy
     - answered count
     - weakest string
     - short practical advice
     - button to drill the weakest string for 10 prompts
   - Stopping is framed as normal and non-judgmental.
   - Also fixed a quiz hydration mismatch by making the first prompt deterministic, then randomizing after mount.

2. Learn as a course path
   - Added `src/components/course-path.tsx`.
   - `/learn` and `/learn/[slug]` now use a two-column desktop layout:
     - left: ordered 3-week path, clickable unlocked lessons, progress count
     - right: overview or selected lesson
   - `AppShell` widens only `/learn*` routes via `pathname.startsWith("/learn")`.
   - Mobile stacks cleanly; checked at 390×844.

3. 3-week note-fluency trajectory
   - `/learn` now explicitly communicates:
     - Week 1: alphabet, open strings, walking a string, 12th fret
     - Week 2: sharps/flats, 0/5/7/12 anchors, low E/A confidence
     - Week 3: unisons, octaves, horizontal + vertical integration
   - Curriculum data was not changed.

## Verification

From `app/fretboard-tutor/`:

```bash
rtk pnpm build
```

Result: passes.

Browser verification with Playwright:

- `/learn` desktop
- `/learn` mobile at 390×844
- `/quiz?strings=4&frets=0,5,7,12&limit=10`
- Clicked one answer, then `I'm tired`; recap rendered correctly
- Console errors: none after clean dev-server restart

Note: the first build failed once with stale `.next` chunk errors. Clearing `.next` fixed it, matching the known gotcha below.

## Git / Worktree Notes

Current repo root is not a git repo; run git commands inside:

```bash
cd "/Users/aviouslyavi/Claude/Projects/Avious Music/Guitar/app/fretboard-tutor"
```

Known modified files from the latest work:

- `src/app/learn/page.tsx`
- `src/app/learn/[slug]/page.tsx`
- `src/app/quiz/page.tsx`
- `src/components/app-shell.tsx`
- `src/components/course-path.tsx` (new)

Pre-existing modified files that were not part of the latest change and should not be reverted casually:

- `src/app/api/chat/route.ts`
- `src/app/tutor/page.tsx`
- `src/lib/ai.ts`

## Course

10 lessons, original prose. Source reference only: `~/Downloads/Fretboard+Mastery+eBook+(2025).pdf`. Do not quote or trace diagrams.

| Slug | Strings | Frets |
|---|---|---|
| `welcome` | — | — |
| `w1-alphabet` | all 6 | `[0, 12]` |
| `w1-strings` | all 6 | `[0]` |
| `w1-walking` | `[6]` | full |
| `w2-sharps-flats` | `[6, 5]` | `[1,2,4,6,8,10,11]` |
| `w2-reference-points` | all 6 | `[0, 5, 7, 12]` |
| `w2-walking-from` | `[6, 5]` | `[2,4,6,8,9,10,11]` |
| `w3-unison` | `[5, 4, 3, 2]` | full |
| `w3-octave-shapes` | `[4, 3, 2, 1]` | full |
| `w3-drill` | all 6 | full |

Lesson copy is starter draft. Avi plans to rewrite in his voice. Edit `body` blocks in `src/lib/lessons.ts`; keep slugs/titles/drill targets stable unless Avi explicitly changes them.

Diagrams are placeholders. Convention:

- `public/diagrams/<slug>-<n>.png`
- aspect `3:1`
- add `src: "/diagrams/<slug>-<n>.png"` to the relevant diagram block in `src/lib/lessons.ts`

## Tutor Notes

`src/lib/ai.ts` contains:

- tutor system prompt
- canonical 0-12 fretboard map
- `getVerifiedFretboardContext()`

`src/app/api/chat/route.ts` appends deterministic verified note answers when the latest prompt includes a recognizable string + fret. This prevents local models from hallucinating note names.

Important: `@ai-sdk/openai` defaults to Responses API. LM Studio and Ollama only support Chat Completions, so local providers must use `.chat(model)`, not Responses. Multi-turn breaks on turn 2 if this is changed.

## Gotchas

1. Use `rtk` prefix for shell commands. See `/Users/aviouslyavi/.codex/RTK.md`.
2. Read `app/fretboard-tutor/AGENTS.md` before edits.
3. Next docs path mentioned in `AGENTS.md` may not exist in `node_modules`; use local code patterns if docs are absent.
4. `.next` cache gets stale after route/schema/lesson changes. If styles, routes, or chunks look wrong:

```bash
rtk rm -rf .next
rtk pnpm dev
```

5. Work/Home session split is invisible but storage still tracks it. Quiz defaults `session = "work"`. Do not delete the storage shape.
6. Skips and early stops should not pad accuracy. Streak credit is gated separately at `total >= 10`.
7. Qwen 3.5 is a thinking model; output may land in `reasoning_content` and appear empty. Do not default to it.
8. Octave facts:
   - 6→4 and 5→3 are +2 frets
   - 4→2 and 3→1 are +3 frets because of the B string
   - adjacent-string unison shift is 5 frets back, except 3→2 is 4 frets back
9. Old localStorage lesson slugs from prior CAGED course may exist. Unlock logic ignores unknown slugs. No migration needed.

## Restructure In Flight — Learn + Test (May 2026)

The app is being collapsed from five sections to two:

- **Learn** (`/learn`) — TOC on the left (Week 1/2/3 groups, completion rings), lesson content on the right, **Tutor** as a right-side slide-over panel triggered by a top-right button. Each lesson ends with an inline test scoped to the lesson (no customization controls in Learn).
- **Test** (`/test`) — replaces `/quiz`. Click-the-fret interaction (interaction model only — no code copied from musictheory.net). Customizable: strings, fret range, naturals/sharps. Persists preferences to localStorage. From-lesson entries hide the customization panel and lock scope.

Removed routes: standalone `/tutor`, standalone `/progress`. `/quiz` redirects to `/test` for one release, then drops.

Plan file (canonical for this work): `~/.claude/plans/i-want-to-take-jaunty-dream.md`.

### Build order (one chat per step recommended)

1. `<LearnToc>` + two-column `/learn` shell
2. `<TutorPanel>` slide-over wrapping current tutor chat
3. `<FretboardTest>` extracted from quiz logic, scope-prop-driven
4. `/test` page with settings + persisted prefs
5. Embed `<FretboardTest>` inline at bottom of each lesson, scope locked
6. Hub capsule list pruned; `/quiz`, `/tutor`, `/progress` removed/redirected
7. Manual desktop walkthrough → defer mobile polish

### Token-saving rules for this restructure

- One session per build step; commit between steps so the next chat starts clean.
- Use the `Explore` subagent for read-heavy steps (3, 7).
- Don't open `src/lib/ai.ts` (10 KB) unless the step touches AI.
- Keep `BRIEF.md`, `COURSE-PLAN.md`, this file, and the plan file pinned — re-reading them is cheaper than re-explaining.
- Sonnet 4.6 / Haiku 4.5 are fine for prose passes and small UI tweaks. Reserve Opus for steps 1, 3, 4.

## Lesson copy is collaborative — DO NOT rewrite unilaterally

Avi writes the 10 lesson bodies in `src/lib/lessons.ts` himself, in his voice, one focused chat per lesson (or per week). Structural sessions MUST leave `body` content alone unless explicitly told otherwise. When the lesson-copy phase begins, the workflow is:

1. Open one chat per lesson (or per week if grouping is faster).
2. Read the existing entry in `lessons.ts`.
3. Propose a revision grounded in the pedagogy notes in the plan file (anchor notes, octave shapes, 15-min daily protocol, naturals-first, descend-as-well-as-ascend, say notes aloud).
4. Avi edits in chat. Final copy lands in `lessons.ts`. No silent rewrites.

## Reference material — interaction & pedagogy only

The Test interaction model is informed by **musictheory.net/exercises/fretboard**. Pedagogy is informed by **fretjam.com**, TrueFire, Pickup Music, Guitar Nutrition, Riffhard, Guyker, the Ry Naylor *Fretboard Mastery* ebook (on disk in the project root), and an Andrey Lushnikov mnemonic post.

**Build-phase rule:** dev sessions MAY open these pages to verify behavior. They MUST NOT copy code, copy phrasing, or trace diagrams. Anything visual is original; anything textual is Avi's prose.

## Next Good Threads

1. Build step 1 of the restructure: `<LearnToc>` + two-column `/learn` shell.
2. Lesson copy pass in Avi's voice (collaborative — see above).
3. Add the 11 diagram images.
4. Visual polish pass after Avi clicks around the new shell.
5. Phase 3 deploy: Vercel + custom domain.

## Open Decisions (no action — surface before they bite)

- **App rename.** Folder `fretboard-tutor` and "Fretboard Tutor" copy become misleading once the planned `/piano` namespace lands (companion plan: `~/.claude/plans/i-have-been-working-delegated-riddle.md`). Candidates: "Avious Tutor" (matches parent folder `/Avious Music/`), "Music Tutor", or keep slug + change display strings only. Defer until piano deploy phase at the latest. Don't surprise yourself mid-piano-build.
- **`appliedTune` field on lessons.** Piano plan links each day to a YouTube ID for applied practice. Guitar lessons currently don't. Worth adding `appliedTune?: { title; artist; youtubeId? }` to the lesson schema during the **lesson-copy phase** with Avi — not during the structural restructure. Phrase it as: "what's a real song that uses this fret/string/concept that you'd actually want to practice along to?"
- **Forward-compat for piano (locked in).** Generic naming and topic-namespaced storage keys are now mandatory in Wave 1–3 of the restructure (see `handoffs/README.md` rule 9). This decision is made; listed here only so future you remembers why `lib/drill-engine.ts` isn't called `lib/quiz-engine.ts`.

## Avi Preferences

- ADHD-friendly: focused replies, one decision at a time, don’t bury action items
- Honest assessments over reassurance
- Uses pnpm, Codex, Claude Code; no Cursor
- Apple Silicon Mac
- Animations welcome when they support feedback

## Resume Checklist

1. `cd "/Users/aviouslyavi/Claude/Projects/Avious Music/Guitar/app/fretboard-tutor"`
2. Read `AGENTS.md`.
3. Run `rtk git status --short`.
4. If testing UI, start with `rtk pnpm dev`.
5. Ask Avi what he wants next: copy pass, diagrams, polish, or deploy.
