# Build Prompt — Fretboard Tutor Webapp

Paste the **START PROMPT** section into Codex (or any other coding agent). It is self-contained and assumes no prior context.

The build is split into **three phases**. Phase 1 is a complete, usable app you can practice with the same evening. Phases 2 and 3 are additive. Tell the agent which phase to execute; it will not silently expand scope.

---

## START PROMPT

You are building a personal fretboard-learning webapp for a guitarist with ADHD who:

- Plays guitar (10 years, plays complex songs, knows the CAGED system).
- Cannot name notes on the fretboard yet — that is the entire point of this app.
- Practices ~40 min/day, split as 20 min at work (no guitar, phone-friendly) and 20 min at home (with guitar).
- Wants to follow a 3-week structured curriculum with weekly gates.
- Will not pay for any API in v1. The app must be fully usable with zero AI configured.

### Where to build

Build in **`/Users/aviouslyavi/Claude/Projects/Avious Music/Guitar/app/`** with the project name `fretboard-tutor`.

### Tech stack — non-negotiable

- **Next.js 15** App Router, TypeScript, Tailwind v4.
- **shadcn/ui** for components: `button`, `card`, `dialog`, `tabs`, `input`, `badge`, `progress`, `sonner`.
- **Vercel AI SDK** (`ai`) — but only installed in Phase 2. Phase 1 has no AI dependency.
- **`next-pwa`** — Phase 2 only.
- **No database, no auth.** localStorage via a single typed `useProgress()` hook.
- **pnpm** as the package manager.

### Curriculum content — embed verbatim

Hard-code as a typed const in `lib/curriculum.ts`. Do not invent your own.

```ts
export type Week = {
  id: 1 | 2 | 3;
  title: string;
  strings: number[]; // 1 = high E, 6 = low E
  goal: string;
  gateTest: string;
  workSession: string[];
  homeSession: string[];
};

export const WEEKS: Week[] = [
  {
    id: 1,
    title: "Strings 6 & 5",
    strings: [6, 5],
    goal: "Sub-2-second recall on the CAGED root strings.",
    gateTest:
      "Can you name any fret on strings 6 and 5 in under 2 seconds, cold?",
    workSession: [
      "10 min — note-quiz mode in this app",
      "5 min — eyes closed, name every note on strings 6 & 5 up to fret 12",
      "5 min — pick a random note; locate it on all six strings using octave shapes",
    ],
    homeSession: [
      "10 min — play a known scale, name every note aloud as you play it",
      "5 min — play a known song; call out the root of each chord",
      "5 min — improvise over a drone; name every landing note aloud",
    ],
  },
  {
    id: 2,
    title: "Strings 4 & 3",
    strings: [4, 3],
    goal: "Cross-check with octaves from week 1.",
    gateTest: "Name notes on strings 6, 5, 4, 3 without hesitation.",
    workSession: [
      "10 min — quiz mode, this app",
      "5 min — octave verification: pick a note on string 6, find it on string 4 (same fret +2)",
      "5 min — flashcards on strings 4 & 3",
    ],
    homeSession: [
      "10 min — play a scale, name every note aloud",
      "5 min — play a song, name the root of each chord",
      "5 min — improvise, name landing notes",
    ],
  },
  {
    id: 3,
    title: "Strings 2 & 1 + integration",
    strings: [2, 1],
    goal: "Finish the neck. Real test: solo while naming.",
    gateTest:
      "Solo over a backing track and name every landing note aloud.",
    workSession: [
      "10 min — quiz across all six strings",
      "5 min — random-note octave hunt",
      "5 min — visualize the full fretboard from memory",
    ],
    homeSession: [
      "10 min — scales across all strings, naming aloud",
      "5 min — chord roots in any song",
      "5 min — improvisation with naming",
    ],
  },
];

export const NOTES = ["E","F","F#","G","G#","A","A#","B","C","C#","D","D#"] as const;
export const OPEN: Record<number, (typeof NOTES)[number]> = {
  1: "E", 2: "B", 3: "G", 4: "D", 5: "A", 6: "E",
};
export function noteAt(stringNum: 1|2|3|4|5|6, fret: number) {
  const openIdx = NOTES.indexOf(OPEN[stringNum]);
  return NOTES[(openIdx + fret) % 12];
}
```

### Streak & progress (localStorage shape)

```ts
type Progress = {
  streakCount: number;
  lastActiveDate: string; // YYYY-MM-DD
  currentWeek: 1 | 2 | 3;
  weekStartedAt: string;
  totalQuestions: number;
  totalCorrect: number;
  sessionsToday: { work: boolean; home: boolean };
  history: Array<{ date: string; correct: number; total: number }>;
};
```

Streak rule: increment if the user completes at least one session (work or home, ≥10 questions answered) on a new calendar day. Reset to 0 if a day is missed.

### ADHD-aware UX rules — non-negotiable across all phases

1. **One-tap start.** From `/`, the quiz must be running within one tap.
2. **Big visible streak** on every screen, top-right. Number, not text.
3. **Loud feedback.** Right answer = green flash + brief sound. Wrong = red flash + the correct note shown for 1.5s. Use `sonner` for streak milestones (3, 7, 14, 21 days).
4. **No infinite scroll, no nested menus.** If a screen needs more than 7 visible elements, redesign it.
5. **Skip-friendly.** "I don't have my guitar" / "I'm tired" buttons that still log a partial session. Never punish the user with a streak-loss for a 10-question check-in.
6. **Dark mode by default.** Lower visual noise.

---

## PHASE 1 — Ship a usable app tonight (~2–3 hours)

This is the only phase you should execute unless told otherwise. At the end, the user can `pnpm dev` and start practicing notes the next morning.

### Build steps for Phase 1

1. `mkdir app && cd app && pnpm create next-app@latest fretboard-tutor --typescript --tailwind --app --src-dir --import-alias "@/*" --no-eslint`. Then `cd fretboard-tutor`.
2. Init shadcn: `pnpm dlx shadcn@latest init`. Add the components listed above.
3. Install only: `pnpm add zod`. **Do NOT install `ai` or any AI SDK packages in Phase 1.**
4. Implement `lib/curriculum.ts` exactly as specified.
5. Implement `lib/storage.ts` — typed localStorage helpers with Zod validation. Export a `useProgress()` hook.
6. Build the routes in this order:
   - `/` — Home. Big streak number top-right. Two big buttons: "Start work session" / "Start home session". Current week badge.
   - `/quiz` — Random fret prompt restricted to the current week's strings. 12 note buttons (C, C#, D … B). Timed (default 10s/q, 20 questions/session). Right = green, wrong = red + correct answer for 1.5s.
   - `/progress` — Streak history, weekly gate status, total questions, accuracy %.
   - `/settings` — Quiz timer length, daily goal in minutes, week override (in case the user wants to redo a week).
7. Run `pnpm build` to verify it compiles. Run `pnpm dev` and confirm `localhost:3000` works end-to-end: home → start session → quiz with feedback → returns to home with streak incremented.
8. Write a short README: how to run, current scope (Phase 1, no AI), and a "Next up" section listing Phase 2/3 features.

### What Phase 1 explicitly does NOT include

- No `/tutor` route.
- No AI SDK installed.
- No PWA / manifest.
- No provider settings UI.
- No deployment instructions.

When Phase 1 is done, stop. Tell the user: "Phase 1 complete. The app is at `app/fretboard-tutor`. Run `pnpm dev` to use it. Tell me when you want Phase 2."

---

## PHASE 2 — Add the local tutor (~1–2 hours, run only when user asks)

Adds an optional LLM tutor that runs against a local Ollama instance on the user's Mac. Default is `LLM_PROVIDER=none` so the app remains fully functional with zero configuration.

### Build steps for Phase 2

1. `pnpm add ai @ai-sdk/openai @ai-sdk/anthropic next-pwa`. (LM Studio is OpenAI-compatible, so we don't need a separate Ollama package.)
2. Create `lib/ai.ts`:

```ts
import { createOpenAI } from "@ai-sdk/openai";
import { anthropic } from "@ai-sdk/anthropic";

export type Provider = "none" | "lmstudio" | "ollama" | "anthropic";

export function getProvider(): Provider {
  return (process.env.LLM_PROVIDER as Provider) ?? "none";
}

export function getModel() {
  const provider = getProvider();
  if (provider === "none") return null;

  if (provider === "lmstudio") {
    // LM Studio exposes an OpenAI-compatible server, default port 1234.
    const lmstudio = createOpenAI({
      baseURL: process.env.LMSTUDIO_BASE_URL ?? "http://localhost:1234/v1",
      apiKey: "lm-studio", // LM Studio ignores this but the SDK requires a string
    });
    return lmstudio(process.env.LMSTUDIO_MODEL ?? "qwen3.5-9b");
  }

  if (provider === "ollama") {
    // Ollama is also OpenAI-compatible at /v1
    const ollama = createOpenAI({
      baseURL: process.env.OLLAMA_BASE_URL ?? "http://localhost:11434/v1",
      apiKey: "ollama",
    });
    return ollama(process.env.OLLAMA_MODEL ?? "gemma3:4b");
  }

  if (provider === "anthropic") {
    return anthropic(process.env.ANTHROPIC_MODEL ?? "claude-haiku-4-5");
  }

  // Future providers (uncomment when wanted):
  // if (provider === "openai") {
  //   const openai = createOpenAI({ apiKey: process.env.OPENAI_API_KEY! });
  //   return openai(process.env.OPENAI_MODEL ?? "gpt-5.5-mini");
  // }
  // if (provider === "minimax") {
  //   const minimax = createOpenAI({
  //     baseURL: "https://api.minimax.chat/v1",
  //     apiKey: process.env.MINIMAX_API_KEY!,
  //   });
  //   return minimax(process.env.MINIMAX_MODEL ?? "MiniMax-M1");
  // }

  return null;
}
```

3. Add `/tutor` route. If `getModel()` returns `null`, render a friendly card: *"Tutor not configured. Add a provider in Settings — local LM Studio is free."* Link to `/settings`. Do NOT crash, do NOT show an error.
4. Add API route `/api/chat` that uses `streamText` from the AI SDK with `getModel()`. If the model is null, return a 200 with a static message; do not 500.
5. Tutor system prompt (cache when using Anthropic):

```
You are a friendly, concise fretboard tutor for a guitarist who knows
CAGED but is learning note names. Keep replies under 60 words unless
asked for detail. When hinting at a note, use CAGED octave shapes —
e.g. "same fret two strings up from the 5th-string A is the same A on
string 3." Celebrate streaks. Never lecture. Be warm.
```

6. Extend `/settings` with a provider toggle (none / LM Studio / Ollama / Anthropic), base URL field, model identifier field, and API key field for Anthropic (saved to localStorage, only sent to your own server actions, never logged). Reasonable defaults for LM Studio: base URL `http://localhost:1234/v1`, model `qwen3.5-9b`.
7. Add `next-pwa` config and a manifest so the user can install the app on their phone home screen.
8. Create `.env.example`:

```
# Default: no AI tutor. The app is fully usable without this.
LLM_PROVIDER=none

# To enable a local tutor via LM Studio (free, Mac-only):
#   1. Open LM Studio
#   2. Load Qwen 3.5 9B (preferred — stronger instruction-following) or Gemma 4 4B
#   3. Developer tab → toggle "Start Server" (default port 1234)
#   4. Copy the model identifier shown in the server panel
#   5. Set:
# LLM_PROVIDER=lmstudio
# LMSTUDIO_BASE_URL=http://localhost:1234/v1
# LMSTUDIO_MODEL=qwen3.5-9b   # or gemma-4-e4b-it-mlx for the smaller, faster option

# To enable a local tutor via Ollama (alternative to LM Studio):
# LLM_PROVIDER=ollama
# OLLAMA_BASE_URL=http://localhost:11434/v1
# OLLAMA_MODEL=gemma3:4b

# To enable Claude (paid):
# LLM_PROVIDER=anthropic
# ANTHROPIC_API_KEY=sk-ant-...
# ANTHROPIC_MODEL=claude-haiku-4-5
```

9. Update README: how to start LM Studio's server and load a model, how to flip providers, how to install as PWA on iOS/Android. Mention Ollama as an alternative for users who prefer the CLI.

When Phase 2 is done, stop. Tell the user: "Phase 2 complete. Tutor works locally with Ollama. Tell me when you want Phase 3."

---

## PHASE 3 — Paid providers + deployment (run only when user asks)

1. Add commented-out `case` statements in `getModel()` for OpenAI (GPT-5.5), MiniMax, and any other provider the user wants. Each one is a single `pnpm add` away.
2. Document deployment to Vercel: env vars, custom domain, how to expose a local Ollama tunnel via Cloudflare Tunnel (with auth via Cloudflare Access) if the user wants to use their Mac as the inference host while the frontend lives on Vercel.
3. Add a tiny "Provider" indicator in the corner of `/tutor` so the user knows whether they're talking to local Gemma, Claude, etc.

---

## Do NOT (across all phases) — STRENGTHENED FOR CODEX

Codex / GPT-5.5 has a mild creative-drift tendency. Resist it. Specifically:

- Do not add authentication. Single-user personal app.
- Do not add a database. localStorage is enough.
- Do not add Storybook, Cypress, Playwright, ESLint extras, Prettier configs beyond defaults, Husky, lint-staged, or any tooling not in the explicit dependency list.
- Do not invent additional weeks or curriculum content.
- Animations are welcome when they support feedback or transitions. Avoid only animations that distract from reading, block interaction, or trigger motion sensitivity. Do not add UI emojis unless asked.
- Do not refactor away from the prescribed file structure. If the existing structure feels suboptimal, leave it alone.
- Do not add features the user did not ask for. If you find yourself wanting to ("oh, I should also add X"), STOP and ask first.
- Do not advance to Phase 2 or Phase 3 without explicit instruction. Stop at the end of the current phase.
- Do not add unit tests in Phase 1. The user will tell you if they want them.
- Do not change the tech stack. Next.js 15 + Tailwind v4 + shadcn + pnpm, full stop.

When in genuine doubt about scope, ask one short question rather than expanding the work.

## END PROMPT

---

# AGENTS.md (for Codex)

Codex automatically reads `AGENTS.md` from the project root in every session. The agent that scaffolds Phase 1 should also create this file at `app/fretboard-tutor/AGENTS.md` with the following content, so future Codex sessions inherit the constraints automatically:

```markdown
# Agent guide — fretboard-tutor

This is a personal fretboard-learning webapp. Single user. ADHD-aware UX. No paid APIs by default.

## Stack (do not change)
- Next.js 15 App Router, TypeScript, Tailwind v4
- shadcn/ui, pnpm
- localStorage for all state, no database, no auth
- Optional Vercel AI SDK with provider abstraction in `lib/ai.ts`

## Hard constraints
- Default `LLM_PROVIDER=none`. The app must work fully without AI configured.
- Tutor route degrades gracefully when no provider is set.
- No emojis in UI text. No celebration animations beyond a green flash + sonner toast at streak milestones.
- One-tap start from home. No onboarding flows.
- Don't add tooling (Storybook, Cypress, ESLint extras, Husky, etc.) without being asked.

## Curriculum is fixed
The 3-week curriculum lives in `lib/curriculum.ts` as a typed const. Do not modify it without explicit user instruction.

## When in doubt
Ask one short question. Do not silently expand scope.
```
