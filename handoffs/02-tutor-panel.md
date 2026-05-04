# Step 2 — Tutor slide-over panel

**Model:** Sonnet 4.6 (`claude-sonnet-4-6`) — wrapping an existing chat in a known UI pattern, no new design decisions.

**Goal:** Add a Tutor button to the top-right corner of the lesson content pane. Clicking opens a right-side slide-over panel (~420px wide) wrapping the existing tutor chat. The lesson + TOC stay visible underneath.

**Estimated scope:** small. One new component + chat reuse + lesson page wiring.

## Pre-reqs to read in this chat

- `app/fretboard-tutor/src/app/tutor/page.tsx` — existing chat UI; extract the chat body, leave the page route intact for now (removed in step 6)
- `app/fretboard-tutor/src/app/api/chat/route.ts` — chat backend; do NOT modify
- `app/fretboard-tutor/src/lib/ai.ts` — system prompt + verified fretboard context; do NOT modify behavior, only extend the system prompt input to optionally include lesson context
- `app/fretboard-tutor/src/lib/storage.ts` — provider config check (`LLM_PROVIDER`)

## What to build

1. **`src/components/tutor-panel.tsx`** — slide-over from the right. Backdrop dims (low opacity), ESC closes, click-outside closes. Wraps the chat body extracted from `tutor/page.tsx`. Props:
   ```ts
   type Props = {
     topic?: "guitar" | "piano";  // default "guitar"
     lessonContext?: { slug: string; title: string; body: string };
     open: boolean;
     onClose: () => void;
   };
   ```
   The `topic` prop is forwarded to the chat request body (e.g. `?topic=guitar`). The chat backend's system-prompt switching by topic is a future change — for now accept the prop and pass it through. **Why now:** `/piano` is on the roadmap and will use the same panel; adding the prop later is a breaking refactor.
2. **Top-right Tutor button** added to the lesson content pane in `src/app/learn/[slug]/page.tsx` and `src/app/learn/page.tsx`. Brass capsule, label "Tutor". Disabled / dimmed state when `LLM_PROVIDER === "none"` (with tooltip: "Configure provider in Settings").
3. **System prompt extension:** if `lessonContext` is passed, prepend a short block to the chat's system prompt — "Current lesson: {title}. Lesson notes:\n{body}\n---". Keep the rest of `ai.ts` unchanged.
4. **State:** open/close lives in the lesson page component (`useState`). Don't add a global store.

## What NOT to do

- Do not delete `src/app/tutor/page.tsx` yet (step 6 handles that).
- Do not modify `route.ts` or the verified-fretboard logic.
- Do not change the streaming behavior or queueing.
- Do not add new dependencies.
- Do not touch lesson body content.

## Files affected

- Add: `src/components/tutor-panel.tsx`
- Modify: `src/app/learn/page.tsx`, `src/app/learn/[slug]/page.tsx`, possibly `src/lib/ai.ts` (prompt only, additive)
- Reference (read-only): `src/app/tutor/page.tsx`, `src/app/api/chat/route.ts`

## Verification

```bash
cd app/fretboard-tutor
pnpm build
pnpm dev
```

Walk:
1. `/learn/w1-alphabet` → top-right Tutor button visible.
2. Click → panel slides from the right, lesson visible underneath, focus moves into chat input.
3. Ask "where's F# on string 4?" → answer references string 4 + correct fret. With LM Studio off, the dimmed-button tooltip explains how to configure.
4. ESC closes; click outside closes.
5. Open again, ask a follow-up referencing the lesson — system prompt should give the lesson context to the model.
6. With `LLM_PROVIDER=none` in env, button is dimmed and the rest of the page works unchanged.
7. Console errors: none.

## Hand-off when done

Commit: `learn: tutor slide-over panel with lesson context`. Note: "standalone /tutor route still alive; cleanup in step 6".
