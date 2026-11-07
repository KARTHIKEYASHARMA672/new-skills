#!/usr/bin/env python3
"""Stop hook: enforce that Claude spoke this turn when say-it mode is `on`.

Registered as a `Stop` hook by this plugin's hooks/hooks.json. The harness runs
it every time Claude finishes a turn and feeds it a JSON payload on stdin:
  { session_id, transcript_path, stop_hook_active, cwd, hook_event_name }

Logic:
  - Read the mode from the per-project flag file (written by the /say-it
    toggle). The path is /tmp/say-it-mode-<sha1(cwd)[:12]> so voice state is
    isolated per project; the skill derives the identical key from $PWD.
    Only `on` is enforced; `off`/missing -> allow stop (exit 0).
  - If stop_hook_active is already set, allow stop (avoid infinite re-prompts).
  - Scan the transcript back to the last real user turn. If any
    `voicebox_speak` tool call happened in this turn -> allow stop.
  - Otherwise emit {"decision":"block","reason":...} so Claude must go again
    and actually speak.

Fail-open: any error -> allow stop. A voice nag must never wedge a session.
"""
import hashlib
import json
import socket
import sys

VOICEBOX_HOST = ("127.0.0.1", 17493)


def mode_file(cwd):
    """Per-project flag path. The /say-it skill writes the same path from
    $PWD (`printf %s "$PWD" | shasum | cut -c1-12`), so on/off state never
    bleeds across projects/sessions the way a single global file did."""
    key = hashlib.sha1((cwd or "").encode()).hexdigest()[:12]
    return "/tmp/say-it-mode-" + key


def voicebox_reachable():
    """True if the Voicebox MCP endpoint accepts a connection. When it's down,
    speaking is impossible, so we must not nag the model to do it."""
    try:
        with socket.create_connection(VOICEBOX_HOST, timeout=1):
            return True
    except Exception:
        return False


def allow():
    sys.exit(0)


def block(reason):
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        allow()

    # Avoid loops: if we already blocked once this turn, let it stop.
    if payload.get("stop_hook_active"):
        allow()

    try:
        with open(mode_file(payload.get("cwd", ""))) as f:
            mode = f.read().strip()
    except Exception:
        mode = "off"

    if mode != "on":
        allow()

    transcript_path = payload.get("transcript_path")
    if not transcript_path:
        allow()

    try:
        with open(transcript_path) as f:
            lines = [json.loads(l) for l in f if l.strip()]
    except Exception:
        allow()

    # Walk backward to the last genuine user prompt, watching for a speak call.
    for obj in reversed(lines):
        typ = obj.get("type")
        msg = obj.get("message", {})
        content = msg.get("content")

        if typ == "assistant" and isinstance(content, list):
            for item in content:
                if item.get("type") == "tool_use" and "voicebox_speak" in item.get("name", ""):
                    allow()

        elif typ == "user":
            # A tool_result is also stored as a user message; it's part of the
            # same turn, so only a real text prompt is the turn boundary.
            if isinstance(content, str):
                break
            if isinstance(content, list) and any(i.get("type") == "text" for i in content):
                break

    # No speak attempt this turn. Only nag if speaking is actually possible —
    # if Voicebox is down, let the turn end (the skill falls back to text).
    if not voicebox_reachable():
        allow()

    block(
        "say-it mode is `on` but you ended this turn without calling "
        "voicebox_speak. Speak a short natural gist of your reply now "
        "(see the say-it skill: voice owns the gist, ~2 sentences), then stop."
    )


if __name__ == "__main__":
    main()
