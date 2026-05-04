# Brief — Fretboard Tutor

## Problem

I've played guitar for 10 years and still can't name notes on the fretboard reliably. Existing apps either gamify it into oblivion or bury the drill behind subscriptions, accounts, and feature bloat. I want to *learn the neck*, not manage another login.

## Goal

Reach the point where I can name every landing note while soloing. Concretely: pass the week-3 gate test — name notes in real time across all six strings, full neck.

## Approach

A personal webapp built around two primitives:

1. **Learn** — 10 short lessons (≤3 min each) explaining the *why* behind each week's drills. TOC on the left, content on the right. Each lesson ends with an inline test scoped to that lesson. An optional Tutor panel slides in from the right for asking "where's the F# on string 4?" without leaving the page; off by default. Reading lessons does not count toward the streak.
2. **Test** — customizable click-the-fret note drill scoped by string, fret range, and accidentals. The actual work. Persists preferences to localStorage. Lesson-embedded tests are the same component with scope locked.

Desktop-first. Mobile polish is a later pass.

## Constraints (chosen, not imposed)

- **No DB, no auth.** Everything in `localStorage`. Single user per browser. Zero ops.
- **Works offline.** `LLM_PROVIDER=none` is the default. AI is a feature, not a dependency.
- **One-tap entry.** Hub → drill in one click. No nested menus, no infinite scroll.
- **Honest progress.** Skips and early stops don't pad accuracy. Streak credit gates at ≥10 answers per session. Reading lessons doesn't fake progress.
- **Original content.** Course prose is mine. Reference sources (Ry Naylor / CAGED Clarity / musictheory.net / fretjam / TrueFire / Pickup Music) are conceptual and interaction-model reference only — no quoting, no diagram tracing, no code lifting.
- **Collaborative lesson writing.** Lesson bodies in `lessons.ts` are not rewritten unilaterally — Avi works each one with Claude in a focused chat.

## Curriculum shape

| Week | Focus |
|---|---|
| 1 | Alphabet, open strings, walking a string, 12th fret |
| 2 | Sharps/flats, 0/5/7/12 anchors, low E/A confidence |
| 3 | Unisons, octaves, horizontal + vertical integration |

Gate per week: pass the quiz at the week's scope before the next week unlocks.

## Stack

Next.js 15 App Router · TypeScript · Tailwind v4 · shadcn/ui · Vercel AI SDK · pnpm. Apple Silicon dev. Deploy target: Vercel + custom domain (deferred until course copy and diagrams are done).

## Status

Shipped: hub, drill, course path, lesson template, tutor, settings, progress. Quiz "I'm tired" recap with weakest-string drill. Course path with progressive unlock.

In flight: restructure to two sections (Learn + Test). Tutor folds into Learn as a slide-over panel. `/quiz` becomes `/test` with click-the-fret interaction and customization. `/progress` and standalone `/tutor` are removed; their data folds into Learn TOC + Test results.

Next threads, in order: structural refactor (Learn TOC + Test page) → lesson copy pass with Avi → 11 diagram images → polish → Vercel deploy.

## Non-goals (for now)

- Multi-user / accounts / cloud sync
- Mobile apps (web works)
- Mobile-first responsive polish (desktop-first; mobile is a later pass)
- CAGED chord shapes, scales, arpeggios — separate plan after note fluency lands
- Audio playback in lessons
- Bookmarks, notes, search

## Why this exists at all

I learn faster when the tool fits the way I think. Every existing fretboard app makes me bend around its model. This one bends around mine.
