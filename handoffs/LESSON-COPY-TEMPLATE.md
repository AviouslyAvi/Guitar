# Lesson copy — collaborative writing template

**Model:** Sonnet 4.6 (`claude-sonnet-4-6`) — prose work in an established voice. Don't use Opus; it's overkill and slower for copy iteration.

Use this in a **fresh chat per lesson** (or per week, if you want to batch). The chat reads only the files it needs. Avi has final approval on every body. No silent rewrites.

## Fill in before starting

- **Lesson slug:** `___` (e.g. `w1-alphabet`)
- **Week:** `___` (1, 2, or 3)
- **Strings in scope:** `___`
- **Frets in scope:** `___`

## Paste this as the first message

> I'm writing the lesson body for `<slug>`. I want to do this collaboratively — propose a draft, I'll redirect, we iterate.
>
> Read in this order, nothing else:
> 1. `app/fretboard-tutor/src/lib/lessons.ts` — find my entry for `<slug>`, read the existing `body` and `drill` fields. Don't read other lessons.
> 2. `handoffs/PEDAGOGY.md` — the 3-week method, anchor notes, octave shapes, daily drill protocol, tips & tricks. Use these as the conceptual ground.
> 3. `BRIEF.md` — voice + constraints (≤3 min read, original prose, honest progress, no padding).
>
> **Do NOT read other lessons, BUILD-PROMPT.md, the PDF, or `src/lib/ai.ts`.** Those are out of scope for copy work.
>
> **Voice rules:**
> - Direct, second-person, no fluff. No "let's embark on a journey."
> - Concrete > abstract. Show the fret, name the note, move on.
> - 3-min read max. If a section feels long, cut it.
> - No quoting from any source. Not from Ry Naylor, not from musictheory.net, not from the PDF.
> - No emojis unless I ask.
>
> **Structure each lesson:**
> - Kicker line (e.g. "WEEK 1 · LESSON 2")
> - Display heading (4–7 words)
> - 1-line subtitle (the promise: what you'll be able to do after this)
> - 2–4 short prose blocks. Each block has a clear claim and a worked example.
> - One or two `<Fretboard>` callouts (with the highlight prop spec) where a diagram earns its keep.
> - A 1-line "what to do next" pointing at the embedded test.
>
> Propose a draft for `<slug>` only. I'll edit in chat. When we're done, write the final body back to `lessons.ts` — leave `slug`, `title`, `drill`, and any other non-body fields untouched.

## What NOT to do in a copy chat

- Do not modify `slug`, `title`, `drill`, `unlockAfter`, or any other structural field.
- Do not modify `lib/curriculum.ts`.
- Do not touch other lessons "while you're in there."
- Do not refactor any component, page, or storage code.
- Do not propose new diagrams that don't exist in `public/diagrams/`. If a diagram is needed, note it as a TODO in commit message.
- Do not paraphrase the Ry Naylor PDF, fretjam, or musictheory.net. The pedagogy is in `PEDAGOGY.md` — that's enough.

## When done

Commit message: `lessons: <slug> copy pass`. Body should include "voice pass with Avi". Leave other lessons untouched.
