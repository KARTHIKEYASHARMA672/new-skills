---
name: say-it
description: Lets Claude answer out loud, not just in text, via the local Voicebox app. Off by default — the user turns it on. Triggers on /say-it (on) and /say-it off, plus per-message overrides like "say it" / "read that" / "just text" / "no voice". Invoke /say-it to manage voice.
---

# Say-it spoken replies

Local spoken replies via the Voicebox app (HTTP MCP at `127.0.0.1:17493/mcp`); the desktop app must be running for `speak`. Tools: `voicebox_speak`, `voicebox_list_profiles`, `voicebox_list_captures`. This file defines **when** to speak and **how**; the same binary rule is in `~/.claude/CLAUDE.md` so it applies every turn, and this powers the `/say-it` toggle.

## Modes

Binary: **off by default** (text only), the user turns it **on**. The flag is **per project** so voice state in one project never makes another project's Stop hook nag. On **every** toggle, mirror the state to the project's flag file: `echo <on|off> > "/tmp/say-it-mode-$(printf '%s' "$PWD" | shasum | cut -c1-12)"`. The hook derives the identical key from its payload `cwd`, so write it exactly like that (don't hand-craft the path).

**Preflight — voice must be connected (check before turning on, and before the first speak of any `on` session):** the `voicebox_*` tools come from a global MCP server (`~/.claude.json`), but a project can switch it off (its `disabledMcpjsonServers`) and a fresh session only binds the tools if Voicebox was running at session start. So `voicebox_speak` may simply not exist in this session. Before writing `on` (or speaking), confirm `voicebox_speak` is in your available tools. If it is **not**:
  - Do **not** enable / do **not** try to speak. Write `off` to this project's flag file (same per-project path as above) so the Stop hook stays quiet, in case the flag was left `on`.
  - Tell the user once, in text: voice can't run in this session because the Voicebox MCP isn't connected. If it's **missing everywhere**, add it to `~/.claude.json` (`mcpServers.voicebox`, type `http`, url `http://127.0.0.1:17493/mcp`) or via `/mcp`. If it's **disabled in this project**, remove `voicebox` from this project's `disabledMcpjsonServers` (or re-enable via `/mcp`) and start a fresh session. Either way the app must be running before the session starts.

- **`/say-it`** (`on`, "voice on", "hands-free", "let's talk") → **run the preflight above first.** If connected: speak a 1-2 sentence gist of **every** reply, full text still on screen. Write `on` to the flag file. For the **acknowledgement, speak a warm, natural greeting** rather than a dry "voice is on" — a quick hello and that you're ready to get started, and if there's already work in flight, ground it in that ("hey, voice is on, ready to keep going on the X"). One or two sentences, like a person saying hi, not a status line. (First speak of the session: launch Voicebox if needed, see "When it breaks".)
- **`/say-it off`** (`mute`, "text only", "quiet", "stop talking") → no `speak` calls at all; per-message "say it" / `🔊` still honored. Acknowledge in text. Write `off` to the flag file.
- **`/say-it status`** (or bare `/say-it` when already on) → say + show the current state.

When `on`, speak **every** reply (no per-reply judgment) — the gist in voice, the detail on screen. When `off`, stay silent unless a per-message override fires.

**Enforcement (the `on` guarantee):** a `Stop` hook (`vbstop.py`, bundled with this plugin and registered via its `hooks/hooks.json`) checks the transcript after each turn. When the flag file says `on` and the turn ended with no `voicebox_speak` call, it blocks and re-prompts so the reply gets spoken. This is why the flag file must be kept in sync on every toggle, the hook can't read the conversation, only the file. It's deliberately easy to escape so a broken Voicebox never traps the session: it nudges **once** per turn (the `stop_hook_active` guard), counts a speak **attempt** even one that errored (so a silent/closed app still passes), short-circuits to allow when the MCP port is **unreachable**, and fails open on any error. So "disable enforcement" is just `/say-it off`, which rewrites the flag file.

If Andrei says "always" / "make it permanent" about the toggle, write a memory file (`type: feedback`) under `~/.claude/projects/-Users-razvan-surdu-Brain/memory/` and add it to `MEMORY.md`.

## Two channels, one answer

Voice and text are **two renderings of one answer**, not a long and short version of the same words:

- **Voice = the human layer** — the verdict, the reaction, the "so what," what you'd do. Spoken the way a person talks: contractions, short sentences, natural rhythm.
- **Text = the precise / visual layer** — code, paths, diffs, tables, diagrams, steps, the full reasoning. What's worth *seeing*.

When both fire, **voice owns the gist and the text stays lean** — the text doesn't restate the spoken gist in prose, it shows the part worth seeing. But text must always be complete enough to act on with the sound off (you can't rely on the audio having been heard, and you can't hear it yourself).

When you do speak, point voice at the gist and let the text carry the detail: say the headline ("that's fixed, the diff's on screen"; "two of these will break, see above") and never read code, paths, or markdown aloud.

## Per-message overrides (this turn only)

- **Force voice** (`say it`, `read that`, `out loud`, `🔊`) → speak a ≤ 2 sentence summary even if long/technical, even when **off**.
- **Suppress voice** (`just text`, `no voice`, `quiet`, `🔇`) → no `speak` this turn, even when **on**.

## How to speak — every `speak` call

- **Call `speak` FIRST, before writing the text reply.** Generation takes ~3-5 s, so fire the `voicebox_speak` call at the very start of the turn and let it render *while* you type the text. If you speak at the end, the audio lands long after the text is already on screen and the user sits waiting. Speak first, then write.
- **Just call `voicebox_speak(text=...)`.** The `claude-code` MCP binding (set 2026-06-19) already speaks as Liam Neeson on Chatterbox Turbo. **Never pass `profile` / `engine` / `personality`** unless deliberately overriding for one call. If a reply comes back as the wrong profile, the binding was reset — re-set via `PUT /mcp/bindings` (`client_id: claude-code`, `profile_id: Liam Neeson`, `default_engine: chatterbox_turbo`) or pass them explicitly and tell Andrei.
- **Talk like a person, not a narrator.** Say the gist the way you'd say it out loud, with the rhythm of real speech. For anything visual, point at the screen instead of reading it: "the command's in the terminal", "the path's on screen", "three items, listed above". Never speak code, paths, URLs, long IDs, or markdown.
- **Length:** ≈ 2 sentences / 40 words max; a genuinely short reply can be spoken in full. Expect ~3-5 s before a short clip starts, so keep it short.
- **Fire and forget:** `speak` returns a `generation_id`; don't poll for a single reply. Poll (with `vbpoll.py`) only to (a) avoid talking over a prior clip in the same turn, or (b) confirm a clip rendered when you suspect silence.
- The spoken text can be a looser paraphrase of what's on screen.

## Paralinguistic tags

Drop a tag straight into the `text` and Chatterbox Turbo performs it in Liam's voice. Rendering is **probabilistic** — a supported tag may not land on a given generation (regenerate if it matters); don't depend on one firing. **Tested Jun 2026 on this Voicebox build:**

- **Work:** `[laugh]`, `[sigh]`, `[cough]`, `[gasp]`
- **Don't render here:** `[whisper]`, `[breath]` — Resemble's docs list them as supported, but this build never produced them (0/4 tries each). Avoid.

Use sparingly — one tag in a short reply lands better than several. E.g. `"[sigh] yeah, that one's a pain."` or `"[laugh] no, definitely not."`

## When it breaks

The desktop app (`/Applications/Voicebox.app`) does playback; the MCP endpoint is a separate process that can stay reachable with the app closed, so `speak` can return an id with **no sound**. **Don't relaunch a running app** — that can drop its MCP server mid-session.

- **First `speak` of the session** (and on entering `/say-it`): if `pgrep -x voicebox` is empty, `open -a Voicebox` + `sleep 2`; if running, do nothing. Silent unless it fails.
- **Spoke but silent / wrong voice:** run `vbpoll.py` (next to this SKILL.md): `python3 vbpoll.py <id> --json` — `failed` = real error; a different `profile_id` = binding reset (re-set it, retry).
- **`speak` errors ("not connected" / endpoint down):** if not running, `open -a Voicebox` + `sleep 2` and retry once; if it was already running, don't relaunch — a dropped MCP connection needs the harness to reconnect (new session). After one failed retry, fall back to text and say once: *"Voicebox isn't reachable, replying in text."*

## Discovery & helpers

- `voicebox_list_profiles` → voices; `voicebox_list_captures` → recent captures/transcripts (confirm a clip landed).
- `vbpoll.py <id> [--json]` (sequence/diagnose a generation) and `vbbench.py --profile <n> --engine <e> -- "text"...` (re-benchmark engine speed) live next to this file; full usage in their docstrings. HTTP API reference: `http://127.0.0.1:17493/openapi.json`.
