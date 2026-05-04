# Step 6 — Cleanup: prune hub, remove old routes

**Model:** Sonnet 4.6 (`claude-sonnet-4-6`) — mechanical: search, redirect, delete. The Explore subagent does the read-heavy work first.

**Goal:** Hub capsule list down to **Learn / Test / Settings**. Remove standalone `/tutor` and `/progress` routes. Redirect `/quiz` → `/test` (keep one release as a courtesy, then drop).

**Depends on:** steps 1–5 complete and verified.

**Use Explore subagent first** to surface every reference to `/quiz`, `/tutor`, `/progress` across the codebase so nothing breaks silently.

## Use Explore subagent first

Spawn Explore with this brief:

> Search `app/fretboard-tutor/src/` for every reference to the strings `/quiz`, `/tutor`, `/progress` (links, route components, redirects, copy mentions in JSX). Also check `next.config.ts` and `public/manifest*` for hardcoded paths. Return a list of file:line references grouped by route. Under 200 words.

## Pre-reqs to read in this chat (after Explore reports)

Whatever Explore flags. Likely:
- `src/app/app/page.tsx` (hub capsules)
- `src/app/quiz/page.tsx` (delete or redirect)
- `src/app/tutor/page.tsx` (delete)
- `src/app/progress/page.tsx` (delete)
- `next.config.ts` (add `redirects()` for `/quiz` → `/test`)

## What to do

1. **Hub:** in `src/app/app/page.tsx` reduce capsule list to: Learn (brass primary), Test (brass), Settings (ink). Remove Tutor and Quiz capsules, remove Progress capsule. Move any small progress hints into the Learn capsule subtitle (e.g. "3/10 lessons · 12-day streak").
2. **`/quiz` redirect:** add to `next.config.ts`:
   ```ts
   async redirects() {
     return [{ source: "/quiz", destination: "/test", permanent: false }];
   }
   ```
   Then delete `src/app/quiz/`.
3. **Delete `src/app/tutor/`** entirely. The chat lives only as `<TutorPanel>` now.
4. **Delete `src/app/progress/`** entirely. The progress data is visible in the Learn TOC (completion rings) and `/test` results.
5. **Storage:** keep all existing fields. No migration. Old fields just go unread. Don't delete the storage shape — historical sessions are fine to leave on disk.
6. **Settings page:** if it had any "Tutor provider" section that linked to `/tutor`, leave the section but drop the link.

## What NOT to do

- Do not delete or rename any storage keys (avoid wiping historical data on existing browsers).
- Do not touch `src/lib/curriculum.ts` or lesson `body` content.
- Do not remove the redirect after this release — drop in a later cleanup.
- Do not delete `src/app/api/chat/route.ts` (still used by `<TutorPanel>`).

## Files affected

- Modify: `src/app/app/page.tsx`, `next.config.ts`
- Delete: `src/app/quiz/`, `src/app/tutor/`, `src/app/progress/`
- Reference (read-only): explore report

## Verification

```bash
cd app/fretboard-tutor
pnpm build           # MUST pass after deletions
pnpm dev
```

Walk:
1. `/app` → three capsules only: Learn, Test, Settings.
2. `/quiz` → 307 redirect to `/test`.
3. `/tutor` → 404 (or redirect to `/learn` if you wired one).
4. `/progress` → 404.
5. `/learn/w1-alphabet` → Tutor button still works (panel intact).
6. Chat backend `/api/chat` still responds (Tutor panel proves this).
7. Settings page unchanged otherwise.
8. Console errors: none. No dangling imports.
9. `git grep -n "/quiz\|/tutor\|/progress"` should only match the redirect, copy/links to `/test`, or comments.

## Hand-off when done

Commit: `chore: prune routes, redirect /quiz to /test`. Note: "/quiz redirect lives one release; drop in next pass."
