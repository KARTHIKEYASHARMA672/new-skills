---
name: garmin
description: Download Garmin Connect splits CSV for recent activities via a persistent authenticated Chrome profile (driven by agent-browser), then summarize them. Use when Andrei asks for his recent workouts, weekly training summary, or wants Garmin data pulled into his journal or Ironman 2026 vault.
allowed-tools: Bash(bun:*), Bash(agent-browser:*), Bash(mkdir:*), Bash(ls:*), Bash(test:*), Read
---

# Garmin

Pulls splits CSV for recent Garmin Connect activities by driving the `agent-browser` CLI against the **real Chrome browser** with a dedicated persistent profile, prints a JSON manifest, and lets Claude read + summarize the files.

## When to use

- "What did I train this week?" / "summarize my last N days of workouts"
- "Pull my Garmin activities"
- Feeding workout data into `10-journal/YYYY-MM-DD.md` or the Ironman 2026 vault

Don't use during the sabbatical window (2026-04-15 → 2026-06-14) for *work* topics — but Garmin training is personal, so it's fine.

## Requirements

- **`agent-browser`** CLI on `PATH`: `bun add -g agent-browser && agent-browser install`
- **Google Chrome** (the real app, not Chromium) at `/Applications/Google Chrome.app`. Garmin Connect is behind Cloudflare bot protection; the real Chrome binary with a persistent profile passes the challenge, while agent-browser's bundled Chromium gets blocked. Override the path with `AGENT_BROWSER_EXECUTABLE_PATH` if Chrome lives elsewhere.
- `bun` (the script uses only Bun built-ins — no npm deps to install, though `bun install` adds editor types if you're editing it).

The persistent Chrome profile lives at `~/.claude/skills/garmin/profile/` (gitignored) and holds the Garmin login + Cloudflare clearance. The skill **always runs headed** — a Chrome window appears. If the profile is fresh or expired, sign in once in that window and the profile stays authenticated for future runs.

## Usage

```bash
bun ~/.claude/skills/garmin/garmin.ts [--days N] [--ids id,id,...] [--out DIR]
```

Defaults: `--days 7`, `--out ~/Downloads/garmin-<YYYY-MM-DD>/`.

`--ids` overrides date filtering — download specific activities by id (taken from the `/app/activity/{id}` URL on Garmin Connect).

Stdout is a JSON array, one entry per activity:

```json
[
  { "id": "22902156969", "date": "2026-May-16", "name": "Brick Run",
    "type": "Running", "path": "/Users/.../activity-22902156969.csv", "ok": true },
  { "id": "22901823541", "date": "2026-May-16", "name": "ROUVY - Long Z2 Endurance",
    "type": "Virtual Cycling", "path": "/Users/.../activity-22901823541.csv", "ok": true }
]
```

Exit codes: `0` all good · `1` one or more downloads failed · `2` profile expired / sign-in required.

## Handling auth errors

On exit code `2` (stderr: `profile expired or sign-in required`):

1. Tell Andrei: "Your Garmin session expired — a Chrome window is open for you to sign in."
2. The headed Chrome window is already at the Garmin sign-in page (the script left it open). Wait for Andrei to sign in + complete 2FA and confirm he's on the activities list.
3. Re-run the same command. The profile now holds the auth, so it lists activities and downloads.

If you see Cloudflare's "Just a moment…" / "Performing security verification" page, let it settle a few seconds — the script waits up to 30s for the activities list to render before giving up.

## What to do after the script returns

1. Parse the stdout JSON.
2. For each entry with `ok: true`, `Read` the CSV at `path`.
3. The last row of each CSV is the `"Summary"` row — pull distance, time, pace/speed, avg HR, max HR, avg power (cycling only), total ascent.
4. Build a table grouped by date, then a short performance read (Z2 vs threshold work, bricks, long runs, weekly volume). Andrei is training for an Ironman, so frame it in those terms.
5. Report files location: `~/Downloads/garmin-<date>/`.

If any entry has `ok: false`, note which activities failed and the truncated error.

## Notes

- One agent-browser daemon owns the browser. Launch options (real Chrome path, profile, headed, anti-bot flag) only apply to the call that cold-starts the daemon — if one is already running with the wrong options, reset with `agent-browser close --all`.
- Cloudflare evasion rests on two things: driving real Chrome with the persistent profile, and the `--disable-blink-features=AutomationControlled` flag (keeps `navigator.webdriver` false). Don't spoof a fake user-agent — the genuine Chrome UA is less suspicious than a mismatched one.
- Avoid hammering Garmin with rapid navigations — too many automated hits in a row can trip Cloudflare and log the session out. The script navigates once per activity; don't loop it tightly.
- The skill opens the activity's **More…** menu, then downloads via "Export Splits to CSV". Direct API calls to `/gc-api/activity-service/.../typedsplits` return 403 without extra auth headers — don't try to shortcut.
- Future hooks (not yet implemented): auto-append a workout block to `10-journal/YYYY-MM-DD.md`, push rows into the Ironman 2026 training log.
