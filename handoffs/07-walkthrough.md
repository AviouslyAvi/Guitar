# Step 7 — Manual desktop walkthrough + verification

**Model:** Haiku 4.5 (`claude-haiku-4-5-20251001`) — pure verification, no design choices. Upgrade to Sonnet 4.6 only if a real bug surfaces and needs investigation.

**Goal:** End-to-end smoke test of the restructured app on desktop. No code changes unless a regression is found. If a real bug surfaces, fix it minimally; anything bigger gets logged as a follow-up, not bundled here.

**Depends on:** steps 1–6 complete.

## Pre-reqs

- A clean dev server: `rm -rf .next && pnpm dev`
- Optionally a configured `LLM_PROVIDER` (LM Studio with Gemma is fine) so the Tutor panel can be exercised end-to-end. The walkthrough also covers the `none` path.

## Walkthrough script

Run through this in order. Take a note of any issue, fix only if trivial.

### Hub
1. Open `/`. Click CTA → `/app`.
2. Hub shows three capsules: **Learn**, **Test**, **Settings**. No Quiz, no Tutor, no Progress.

### Learn
3. Click **Learn** → `/learn`. TOC on the left (~28% width), welcome copy on the right, Tutor button top-right of the content pane.
4. TOC shows three groups: Week 1 / Week 2 / Week 3. Week 1 lessons unlocked; Weeks 2+3 locked until gates pass.
5. Click first Week 1 lesson → loads in the right pane, TOC stays sticky, active row highlighted in brass.
6. Scroll to the bottom of the lesson → inline test renders, no customization controls, target note above the board.
7. Click correct fret → brass flash, score increments. Click wrong fret → ink flash + reveal.
8. Land 10 answers → TOC completion ring fills in for that lesson, streak ticks if eligible.
9. Click **Open full test →** below the inline test → routes to `/test?preset=lesson:<slug>`, scope locked, "Lesson scope · open full test" pill at top, settings panel hidden.

### Tutor panel
10. Back on a lesson. Click **Tutor** top-right.
11. Panel slides from the right; lesson + TOC visible behind it. Focus moves into chat input.
12. Ask "where's F# on string 4?" → reply references string 4, correct fret. ESC closes the panel.
13. Re-open the panel; ask a follow-up — assistant should still have the lesson context.
14. Switch `LLM_PROVIDER=none` (env or settings) → Tutor button visibly dimmed; tooltip explains how to enable; rest of the page unaffected.

### Test
15. Visit `/test` directly → settings expanded with last-used scope.
16. Change scope (strings [4,3], frets [0,7], naturals+sharps), Start → drill matches. "I'm tired" → recap renders with weakest-string suggestion.
17. Refresh `/test` → settings persisted.
18. Land 10 answers → streak credit applied (visible in any UI that surfaces streak; check storage if no UI).

### Old routes (sanity)
19. `/quiz` → redirects to `/test`.
20. `/tutor` → 404 or redirect to `/learn`.
21. `/progress` → 404.

### Mobile (≤768px) — known to be degraded, just confirm nothing's broken
22. Resize to 390×844. TOC stacks above content (or collapses to a top drawer). Tutor button still tappable. Inline test renders. Polish is a later pass — note any blockers but don't fix here.

### Console + build
23. `pnpm build` passes.
24. Browser console: zero errors across the walkthrough.
25. `git status` clean (no stray files from temp routes etc.).

## When done

If everything passed: tag the commit (`git tag restructure-v1`) and update `HANDOFF.md` "Current State" section to reflect the new routes. The lesson-copy phase can begin (see `LESSON-COPY-TEMPLATE.md`).

If anything failed: log issues in a new `handoffs/08-fixes.md` with file:line refs and reproduce steps.
