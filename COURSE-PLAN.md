# Course site plan — `/learn`

> **Note (May 2026):** the app is being restructured to two top-level sections, **Learn** and **Test**. Tutor folds into Learn as a slide-over panel. `/quiz` becomes `/test` with click-the-fret interaction and customization. `/progress` and standalone `/tutor` are removed. The structural plan lives at `~/.claude/plans/i-want-to-take-jaunty-dream.md`. Curriculum below is unchanged.

Working spec for the lesson section of the Fretboard Tutor app. Lives inside the existing Next.js app at `/learn`. Original content; reference sources (Ry Naylor / CAGED Clarity / musictheory.net / fretjam) are interaction & pedagogy reference only — no quoting, no diagram tracing, no code lifting.

## Scope (v1)

Only the existing 3-week note-fluency curriculum (`lib/curriculum.ts`). No CAGED chord shapes, arpeggios, or scales yet. Course site exists to teach the *why* behind the quiz drills and to give the player something to read on a slow morning.

Hard constraints inherited from `AGENTS.md`:
- No DB, no auth — localStorage only
- Default `LLM_PROVIDER=none` — lessons must work without AI
- One-tap entry; no nested menus
- 3-min reads; no infinite scroll

## Content shape

Each week gets ~3 short lessons, each ≤3 min read, building on each other:

**Week 1 — Strings 6 & 5**
1. *Why these two strings first.* The low E and A strings are the root strings for the most common chord shapes. Naming notes here pays off fastest because every barre chord and every CAGED root sits on one of them.
2. *The five anchor notes.* Open, fret 3, fret 5, fret 7, fret 12. Octaves on string 6: E–G–A–B–E. Same idea on string 5: A–C–D–E–A. Memorise these and you fill in the rest by half-steps.
3. *Octave shapes between strings 6 & 5.* The "two-frets-up-two-strings-down" shape. Worked example: find every G on the neck starting from G on string 6 fret 3.

**Week 2 — Strings 4 & 3**
1. *Cross-checking with week 1.* Same fret on string 4 = note two whole steps above string 6. Use it to verify week-1 recall.
2. *String 3 is the odd one out.* G→B is a major third (3 frets), not a fourth like every other adjacent pair. Why this matters when reading octave shapes.
3. *Octave map across strings 6/5/4/3.* The four shapes. One worked walk-through.

**Week 3 — Strings 2 & 1 + integration**
1. *Finishing the neck.* Strings 2 and 1 reuse the patterns from earlier weeks, offset by string 3's quirk.
2. *Real-time naming while playing.* Why the work/home split exists. Drills you can do without the app.
3. *Gate test prep.* What "name every landing note while soloing" actually means and how to ramp into it.

Total: 9 lessons. Plus one "Welcome to the practice room" intro lesson at `/learn` root.

## Routes

```
/learn               — TOC (3 weeks, 10 lessons, completion rings) on the left,
                       welcome content on the right, Tutor panel triggered top-right
/learn/[slug]        — same shell; lesson content on the right, embedded fretboard,
                       inline scoped <FretboardTest> at the bottom (no customization),
                       "Open full test" link to /test?preset=lesson:<slug>
/test                — full Test page: customizable click-the-fret drill
                       (strings, fret range, naturals/sharps), persisted prefs
```

Slugs: `welcome`, `w1-roots`, `w1-anchors`, `w1-octaves`, `w2-crosscheck`, `w2-string3`, `w2-octave-map`, `w3-finishing`, `w3-naming`, `w3-gate-test`.

## Storage additions

Extend `lib/storage.ts` `Progress`:
```ts
lessonsCompleted: string[]   // slugs
lessonsLastVisited: Record<string, number>  // slug -> ms timestamp
```
No migration needed — additive optional fields with `?? []` defaults on read.

A lesson is "completed" when its end-of-page check ("Got it, drill it") is clicked. Doesn't expire. Idempotent.

## Progressive unlock

Simple, no streak-gating:
- Week 1 lessons all unlocked from day 1
- Week 2 lessons unlock when **Week 1 quiz gate passes** (week-override-aware)
- Week 3 unlocks when Week 2 gate passes
- Lessons within a week unlock in order (lesson 2 needs lesson 1 marked complete)

Rationale: the curriculum is already gated by week; lessons should mirror it. Avoids a separate progress system.

## Lesson → test integration

Each lesson ends with an **inline `<FretboardTest>`** scoped to the lesson's strings/frets, with no customization controls. Below it, a brass capsule link: **Open full test →** routes to `/test?preset=lesson:w1-roots`. Marking the lesson complete happens when the user lands ≥10 answers in the inline test (same streak rule as the standalone `/test`).

**Streak credit:** lesson completion alone does not extend the streak. Only quiz sessions do (existing `total >= 10` rule). This keeps "did the work" the bar, not "read the doc." Avi's preference: "honest assessments preferred over reassurance" — reading without drilling shouldn't fake progress.

## Fretboard component (new)

`components/fretboard.tsx` — reusable SVG, used by lessons today and quiz hints later.

Props:
```ts
type FretboardProps = {
  frets?: number;              // default 12
  highlight?: { string: 1|2|3|4|5|6; fret: number; label?: string; tone?: "brass" | "sage" | "ink" }[];
  showOpen?: boolean;          // default true
  showFretNumbers?: boolean;   // default true
  caption?: string;            // optional, renders below
};
```

Visual rules (matches autumn brand):
- Background: transparent, sits on `card/60` like other inline elements
- Strings: parchment-tinted hairlines, thicker as string number rises
- Frets: brass-edge color, thicker on inlay frets (3, 5, 7, 9, 12)
- Inlay dots: brass at 30% opacity
- Highlighted notes: filled circle in `tone` color, label in display font
- Mobile: 100% width, fixed aspect ratio (3:1 horizontal layout)

Render strategy: inline `<svg>`, no external lib. ~150 LOC.

## Visual style

Reuses every existing brand primitive:
- `.brass-edge` cards for lesson sections
- Display font (New Astro) for headings, body (Mosvita Sans) for prose
- `.sun-arc` behind the lesson title card
- Fretboard captions in `font-mono` JetBrains
- Stagger-in animation on lesson sections (matches current pages)

Lesson header pattern: small kicker (`WEEK 1 · LESSON 2`), display heading, ~1-line subtitle. Matches the dossier card on `/app`.

## Hub integration

`/app` capsule list grows from 3 to 4:
- Quiz (brass, primary)
- **Learn** (new, ink tone)
- Tutor
- Settings

Plus a small "Continue lesson" pill on the Quiz capsule's bottom edge if `lessonsLastVisited` has a recent unfinished lesson.

## What's deferred

- CAGED chord shapes / pentatonics / scales — separate plan when 3-week curriculum is shipped and validated
- Audio playback in lessons (e.g. hearing the octave shape) — possible v2
- Lesson search / table of contents on inner pages — only 10 lessons, not needed
- Bookmarking / notes — lessons are short enough to re-read

## Build order

1. `components/fretboard.tsx` — SVG, prop-driven, manually tested
2. Storage additions — `lessonsCompleted`, `lessonsLastVisited`
3. `/learn` index page — week cards, lesson list, completion rings
4. `/learn/[slug]` template — header, prose, fretboard, "Drill it" button
5. Write the 10 lessons as MDX or typed const (decide: prefer MDX for prose ergonomics, but typed const avoids adding `@next/mdx` and matches `lib/curriculum.ts` style)
6. Hub integration — fourth capsule
7. Quiz post-session "Back to lesson" wiring

Step 5 is the time-sink; everything else is small. Lessons can land one at a time; structure must be in place first.

## Open questions

- **MDX vs typed const for lesson copy?** MDX is nicer for writing but adds a dep and a renderer. Typed const with React fragments is uglier but matches existing patterns. Recommend: typed const for v1, migrate to MDX if writing more than 10 lessons feels painful.
- **"Drill it" should it always launch a fresh quiz, or resume an in-progress one?** Recommend: always fresh, scoped to the lesson's strings. Simpler mental model.
