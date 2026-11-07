<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://i.ibb.co/S70hpx4q/skills-header-dark.png">
  <img alt="Skills — from idea to shipped code" src="https://i.ibb.co/pvk4mZKx/skills-header-light.png">
</picture>

# Skills

A personal collection of reusable skills for Claude Code and other LLM tools. The source for the banner above lives in [`assets/skills-map.html`](assets/skills-map.html).

## Skills

| Skill | Description |
|---|---|
| [`spike-it`](spike-it/SKILL.md) | Answer one technical question with throwaway code — scrappy prototype outside the repo, report the learning, drop the code |
| [`interview`](interview/SKILL.md) | High-level interview to align on the shape of a plan (~3-6 questions) |
| [`poke-holes`](poke-holes/SKILL.md) | Focused review that hunts for weak spots and hidden assumptions (~6-12 questions) |
| [`grill-me`](grill-me/SKILL.md) | Exhaustive walk of every branch of the decision tree, hands off to `to-spec` |
| [`to-spec`](to-spec/SKILL.md) | Capture the why and what into a lean six-section spec under `docs/specs/` (capture-first) |
| [`domain-docs`](domain-docs/SKILL.md) | Maintain the `GLOSSARY.md` glossary and `docs/adr/` decision records |
| [`improve-architecture`](improve-architecture/SKILL.md) | Find deepening opportunities (shallow→deep modules) and present them as a visual HTML report |
| [`to-html`](to-html/SKILL.md) | Render what's been discussed as a single self-contained HTML page — explainer, matrix, dashboard, cheat-sheet |
| [`show-it`](show-it/SKILL.md) | Show an idea in a live auto-refreshing browser page — mockups, comparisons, charts, layouts — so a picture lands it faster than a paragraph |
| [`explain-diff`](explain-diff/SKILL.md) | Teach how a diff, branch, or PR works as a self-contained interactive HTML page — background, intuition, code walkthrough, diagrams, and a quiz (adapted from Geoffrey Litt) |
| [`explain-topic`](explain-topic/SKILL.md) | Sibling of `explain-diff` for non-code — teach a topic, decision, or design worked out in the conversation as a self-contained interactive HTML page with a quiz |
| [`to-issues`](to-issues/SKILL.md) | Break a plan or spec into independently-grabbable issues as thin vertical slices |
| [`implement-tdd`](implement-tdd/SKILL.md) | Build an existing plan test-first, one behavior at a time, red-green-refactor |
| [`orchestrate-tdd`](orchestrate-tdd/SKILL.md) | Drive a list of issues to completion by spawning one TDD agent per slice, sizing the model, verifying and reviewing each result |
| [`prove-it`](prove-it/SKILL.md) | Drive the running app like a human to confirm the changed flows work end to end (pass/fail verdict) |
| [`break-it`](break-it/SKILL.md) | Adversarial exploratory testing — drive the running app to find the bugs a human QA would catch |
| [`record-it`](record-it/SKILL.md) | Record a Full HD MP4 demo of a flow in the running app, with a visible cursor, click ripples and captions |
| [`sitrep`](sitrep/SKILL.md) | Mid-session status brief in chat — goal, why, what landed, what's in flight, what's blocked, the next step; writes nothing and doesn't end the session |
| [`wrap-up`](wrap-up/SKILL.md) | Close out the session in chat — why it started, what got done, what changed, what was decided, what's open, and the next step |
| [`handoff`](handoff/SKILL.md) | Summarise the current conversation into a handoff doc for the next session |
| [`handoff-cowork`](handoff-cowork/SKILL.md) | Cowork variant of `handoff` — writes the doc to the scratchpad, presents it, and gives a paste prompt for a fresh Cowork chat |
| [`save-session`](save-session/SKILL.md) | Bookmark the current session into the Obsidian daily note with a title, start time, summary, and a copy-paste `--remote-control` resume command |
| [`session-recap`](session-recap/SKILL.md) | Summarize a day's Claude Code sessions across all projects, then offer to bookmark any of them via `save-session` |
| [`weekly-claude-reflection`](weekly-claude-reflection/SKILL.md) | Weekly retro on the memories + CLAUDE.md across all projects — promote recurring lessons to global, prune stale, dedupe, flag conflicts; nothing changes without confirmation |
| [`to-atomic-commits`](to-atomic-commits/SKILL.md) | Split uncommitted changes into logical atomic commits, respecting detected commit conventions |
| [`garmin`](garmin/SKILL.md) | Download Garmin Connect activity splits and summarize workouts |
| [`brand-it`](brand-it/SKILL.md) | Apply Andrei's personal brand colors, typography, and visual style to any rendered artifact |
| [`polish-ux`](polish-ux/SKILL.md) | Review-and-fix pass over an HTML artifact — verify it renders, then fix layout, interaction states, consistency, and accessibility defects |
| [`brand-it-cowork`](brand-it-cowork/SKILL.md) | Cowork variant of `brand-it` — maps the brand onto each Cowork surface (live artifacts, inline `show_widget`, HTML/React artifacts, pptx/docx/pdf) and their constraints |
| [`fable-mode`](fable-mode/SKILL.md) | Make any model operate with Fable 5's judgment, planning, verification, and reasoning habits ("fable mode") |
| [`say-it`](marketplace/plugins/say-it/skills/say-it/SKILL.md) (plugin) | Let Claude answer out loud via the local Voicebox app; off by default, toggled per project |

### Size at a glance

Each skill's `SKILL.md` — the instruction prose only — measured to keep us honest about conciseness. Tokens are estimated as `bytes ÷ 4`. Regenerate after any change with `bun scripts/skill-sizes.ts --write`.

<!-- skill-sizes:start -->
| Skill | Lines | Words | ~Tokens |
|---|--:|--:|--:|
| `orchestrate-tdd` | 146 | 1,782 | 2,729 |
| `say-it (plugin)` | 73 | 1,499 | 2,325 |
| `implement-tdd` | 150 | 1,344 | 1,965 |
| `save-session` | 67 | 1,086 | 1,664 |
| `polish-ux` | 44 | 960 | 1,553 |
| `explain-topic` | 54 | 950 | 1,523 |
| `to-html` | 62 | 963 | 1,480 |
| `brand-it` | 102 | 906 | 1,465 |
| `record-it` | 71 | 987 | 1,445 |
| `weekly-claude-reflection` | 56 | 836 | 1,436 |
| `show-it` | 59 | 959 | 1,422 |
| `improve-architecture` | 69 | 884 | 1,420 |
| `domain-docs` | 105 | 872 | 1,409 |
| `to-spec` | 105 | 878 | 1,401 |
| `brand-it-cowork` | 62 | 835 | 1,400 |
| `explain-diff` | 54 | 844 | 1,376 |
| `garmin` | 76 | 761 | 1,269 |
| `fable-mode` | 46 | 807 | 1,172 |
| `to-issues` | 102 | 728 | 1,132 |
| `handoff-cowork` | 49 | 752 | 1,122 |
| `session-recap` | 47 | 622 | 985 |
| `to-atomic-commits` | 81 | 591 | 937 |
| `break-it` | 37 | 386 | 619 |
| `spike-it` | 37 | 414 | 617 |
| `grill-me` | 32 | 401 | 608 |
| `poke-holes` | 37 | 321 | 503 |
| `prove-it` | 29 | 328 | 493 |
| `wrap-up` | 28 | 271 | 400 |
| `sitrep` | 30 | 277 | 388 |
| `interview` | 27 | 228 | 367 |
| `handoff` | 26 | 204 | 311 |
| **Total** | **1,963** | **23,676** | **36,936** |
<!-- skill-sizes:end -->

### Requirements

Most skills are prose-only and need nothing beyond Claude. These few shell out to external tools — install them before use:

| Tool | Used by | Install |
|---|---|---|
| `bun` | `garmin`, `show-it`, installing `agent-browser` | [bun.sh](https://bun.sh) |
| [`agent-browser`](https://agent-browser.dev) | `garmin`, `prove-it`, `break-it`, `polish-ux`, `record-it` | `bun add -g agent-browser && agent-browser install` |
| Google Chrome (real app) | `garmin` | [google.com/chrome](https://www.google.com/chrome/) |
| `ffmpeg` | `record-it` | `brew install ffmpeg` |
| `python3` | `say-it` (hook + helper scripts), `to-html` + `polish-ux` (preview server), `session-recap` (digest script), `weekly-claude-reflection` (inventory script) | preinstalled on macOS |
| [Voicebox](https://github.com/jamiepine/voicebox) (desktop app) | `say-it` | see the [repo](https://github.com/jamiepine/voicebox); must be running for voice |
| [Obsidian](https://obsidian.md) | `save-session`, `session-recap` (optional save step), `weekly-claude-reflection` (autonomous handoff) | edit the `CONFIGURE ME` block in `save-session/scripts/session-info.sh` to point at your journal vault, folder, and date format |

`garmin` drives real Chrome with a persistent authenticated profile (to pass Garmin's Cloudflare bot check) and always runs headed — see its [SKILL.md](garmin/SKILL.md) for the one-time sign-in.

### From idea to shipped code

The plan-and-build skills chain together. Pick the review depth that fits, turn the result into work, then implement it:

1. **Shape the plan** — three depth tiers for stress-testing a plan, pick based on how deep you want to go:
   - **interview** → quick alignment, big-picture only
   - **poke-holes** → probe the 2-3 riskiest parts
   - **grill-me** → exhaustive, then hands off to `to-spec`
2. **Capture it** — `to-spec` structures the resolved plan into a lean six-section spec under `docs/specs/`. Capture-first: it records what's been decided, asking only for missing required pieces.
3. **Break it down** — `to-issues` slices the spec into independently-grabbable issues.
4. **Build it** — `implement-tdd` consumes the spec or issues and builds them test-first.
5. **Check it in the real app** — once it's built and the suite is green, drive the running app like a human: **prove-it** confirms the changed flows work end to end; **break-it** throws nasty inputs and edge cases at them to find what a human QA would catch. Distinct from the test suite (`implement-tdd`/`orchestrate-tdd`) — this is the manual, browser-driven pass.

For a batch of issues you'd rather not build by hand, **orchestrate-tdd** sits one level above `implement-tdd`: instead of coding, it spawns one agent per slice (running `implement-tdd` on that slice), sizes each to the cheapest model that fits, then independently re-runs the tests and reviews the diff before advancing. Reviews are tier-gated (skip trivial, `simplify` for simple, `code-review` for complex, plus a final cross-slice pass), failures retry then escalate to the most-capable model, and it writes status back to the tracker as each slice lands. Use it to drive a whole `to-issues` backlog to a reviewed branch autonomously.

**spike-it** sits before step 1, for when the plan can't be shaped until a technical question is answered. It writes deliberately throwaway code in the scratchpad (never in the repo), runs it, and reports the answer with evidence, then drops the code. The learning is the artifact; hand it on to `to-spec`, `domain-docs`, or `to-issues`.

**domain-docs** runs alongside this flow as the keeper of durable domain knowledge: the `GLOSSARY.md` glossary and `docs/adr/` decision records. `grill-me` and `to-spec` flag fuzzy terms and hard-to-reverse decisions and point here to record them; it also works standalone.

**improve-architecture** feeds the front of this flow for existing codebases: it surveys the code, surfaces the strongest deepening opportunities as a visual HTML report, and stops. Take a chosen candidate into `grill-me` to design it, or `to-issues` to slice it.

**show-it** is a display tool any flow can reach for: when a picture would land an idea faster than a paragraph (a layout, a chart, two designs side by side), it opens a live auto-refreshing browser page so the user sees what you mean while the conversation continues in the terminal. Triggers on "show it", "visualize this", or "render this".

**explain-diff** is the deep-explainer for a code change: point it at a diff, branch, or PR and it produces a self-contained interactive HTML page (background → intuition → code walkthrough → diagrams → a five-question quiz). Where `to-html` renders whatever's been discussed, `explain-diff` is the focused "teach how this change works, then quiz me on it" variant. Adapted from Geoffrey Litt's gist, with the quiz anti-gaming rules (deterministic option shuffle, length-matched options) folded in from community feedback.

**explain-topic** is its non-code sibling: same teaching spine and quiz, but the subject is something worked out in the conversation (an architecture, a decision and its trade-offs, a researched topic, a hard concept) rather than a diff. It grounds the page in what was actually said plus anything readable, and marks gaps instead of inventing them. Reach for `to-html` when you just want the discussion rendered; reach for `explain-topic` when you want it *taught*, with a quiz.

**polish-ux** is the craft pass for any of these HTML outputs. Where `brand-it` owns the visual identity (tokens, fonts, color meaning), `polish-ux` checks the page is actually built well: it serves and screenshots the page to prove it renders, then fixes the recurring defects (broken layout, missing hover/focus/disabled states, mismatched type, accessibility gaps). Run it on output from `to-html`, `show-it`, `explain-diff`, `explain-topic`, or `improve-architecture` before handing it off.

**wrap-up** closes the session for *you*: a one-screen summary in chat covering why the work started, what got done, what changed, what was decided, what's still open, and the single next step. **handoff** covers the other audience: when work spans multiple sessions or collaborators, it writes a doc so a fresh agent can pick up where the last one left off.

### Other

- **fable-mode** → a behavioral overlay for weaker or faster models: say "fable mode" and the session adopts Fable 5's working habits (evidence before action, verify by running things, lead with the outcome, finish the turn). Stays on until "fable mode off".
- **garmin** → pull recent Garmin Connect activity data and summarize it.
- **say-it** (plugin) → let Claude answer out loud via the local Voicebox app; off by default, toggled per project.
- **save-session** → bookmark the current Claude Code session into the Obsidian daily note with a copy-paste, remote-control-enabled resume command, so you can jump back in later from any terminal or your phone.
- **session-recap** → summarize a day's Claude Code sessions across all projects (today, yesterday, or a date), then offer to bookmark any of them into the daily note via `save-session`.

## Inspiration

This collection draws on the ideas, structure, and conventions of:

- **Anthropic** — the official skills repo: [anthropics/skills](https://github.com/anthropics/skills)
- **Matt Pocock** — [mattpocock/skills](https://github.com/mattpocock/skills)
- **Geoffrey Litt** — [`explain-diff`](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524) is adapted from his gist; the quiz anti-gaming rules fold in [community feedback](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524#comments) on the original

## Connect

Built by Razvan Andrei Surdu in Europe — [surdu.eu](https://surdu.eu/) · [github.com/andreiRS](https://github.com/andreiRS)
