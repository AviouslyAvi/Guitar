# Step 1 — Learn shell + TOC

**Model:** Opus 4.7 (`claude-opus-4-7`) — architectural; sets the layout pattern every lesson + Tutor panel will live inside.

**Goal:** Convert `/learn` into a two-column desktop layout: TOC on the left, lesson content on the right. Renders the existing 10 lesson bodies unchanged.

**Estimated scope:** small-to-medium. One component + two pages touched.

## Pre-reqs to read in this chat

- `app/fretboard-tutor/AGENTS.md`
- `app/fretboard-tutor/src/components/course-path.tsx` (existing left-column pattern)
- `app/fretboard-tutor/src/components/app-shell.tsx`
- `app/fretboard-tutor/src/lib/lessons.ts` — DO NOT modify body content; just read the structure
- `app/fretboard-tutor/src/lib/curriculum.ts` — week → strings mapping
- `app/fretboard-tutor/src/lib/storage.ts` — `lessonsCompleted`, `lessonsLastVisited`, gate logic

## What to build

1. **`src/components/learn-toc.tsx`** — sticky left column, max width ~320px, ~28% on desktop. Shows three collapsible groups (Week 1 / 2 / 3). Each lesson row: completion ring (filled when in `lessonsCompleted`), title, locked indicator if upstream gate not met. Active lesson highlighted in brass.
2. **`src/app/learn/page.tsx`** — render `<AppShell>` → flex row → `<LearnToc>` + welcome content pane on the right. Use the existing welcome content from current `/learn`.
3. **`src/app/learn/[slug]/page.tsx`** — same shell; right pane renders the slug's lesson body (unchanged) + existing fretboard diagrams. Header pattern: small kicker ("WEEK 1 · LESSON 2"), display heading, 1-line subtitle.
4. **`src/components/app-shell.tsx`** — already widens for `/learn*`. Verify it still works; tweak only if the new two-column needs more horizontal room.

## What NOT to do

- Do not embed the test yet (step 5).
- Do not add the Tutor button yet (step 2).
- Do not rewrite any lesson body in `lessons.ts`.
- Do not modify `curriculum.ts`.
- Do not touch `/quiz`, `/tutor`, `/progress` yet.

## Forward-compat note (cheap if done, painful later)

A separate `/piano` topic is on the roadmap. **Don't build a Guitar | Piano switcher now**, but leave room in the `<AppShell>` header for one ~120 px segment control later. Concretely: don't pin the header to exactly the current control widths; use flex so a future segment slots in without re-layout. Reference: piano plan's "Cross-Pollination" section.

## Files affected

- Add: `src/components/learn-toc.tsx`
- Modify: `src/app/learn/page.tsx`, `src/app/learn/[slug]/page.tsx`, possibly `src/components/app-shell.tsx`
- Reference (read-only): `course-path.tsx`, `lessons.ts`, `curriculum.ts`, `storage.ts`

## Verification

```bash
cd app/fretboard-tutor
pnpm build           # must pass
pnpm dev
```

Walk:
1. `/app` → click Learn → `/learn` renders with TOC left, welcome right.
2. Click a Week 1 lesson → loads in the right pane, TOC stays sticky.
3. Click a locked Week 2 lesson → either disabled or shows lock state.
4. Refresh on `/learn/w1-alphabet` → TOC highlights it as active.
5. Console errors: none.
6. Mobile (≤768px): degraded but readable — TOC stacks above content. Polish is later.

## Hand-off when done

Commit with message like: `learn: two-column shell + TOC`. Note in commit body: "structure only; no body changes; tutor + embedded test still pending in steps 2 + 5".
