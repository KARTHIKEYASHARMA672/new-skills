#!/usr/bin/env python3
"""vbbench.py — benchmark Voicebox TTS: generation time vs audio length per voice.

For each text it: POSTs to /speak (which also autoplays on the speakers, mirroring
the MCP voicebox_speak), times how long until the SSE /status stream reports the
generation finished, reads the `duration` (seconds of audio) from the result, then
sleeps `duration + buffer` so the next clip never overlaps the one still playing.

Usage:
    python3 vbbench.py --profile "Liam Neeson" [--engine chatterbox_turbo] [--buffer 0.6] -- "text one" "text two" ...

Env:
    VOICEBOX_HOST   base URL (default http://127.0.0.1:17493)

Prints one result line per text and a summary; exit 0 if all succeeded.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

DONE = {"completed", "complete", "done", "ready", "success", "succeeded"}
BAD = {"failed", "error", "errored", "cancelled", "canceled"}


def _post(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def _parse_sse(body: str) -> dict:
    payloads = [ln[5:].strip() for ln in body.splitlines() if ln.startswith("data:")]
    for chunk in reversed(payloads or [body.strip()]):
        if not chunk:
            continue
        try:
            return json.loads(chunk)
        except json.JSONDecodeError:
            continue
    return {"_raw": body}


def _wait(host: str, gen_id: str, timeout: float) -> tuple[str, dict, float]:
    """Block on the SSE status stream until the generation ends. Returns
    (status, last_payload, elapsed_seconds)."""
    url = f"{host}/generate/{gen_id}/status"
    start = time.monotonic()
    last: dict = {}
    while time.monotonic() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                body = r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                time.sleep(0.2)
                continue
            raise
        last = _parse_sse(body)
        status = str(last.get("status") or last.get("state") or "").lower()
        if status in DONE or status in BAD:
            return status, last, time.monotonic() - start
        time.sleep(0.1)
    return "timeout", last, time.monotonic() - start


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--profile", required=True)
    p.add_argument("--engine", default=None,
                   help="kokoro | qwen | qwen_custom_voice | luxtts | chatterbox | chatterbox_turbo | tada")
    p.add_argument("--buffer", type=float, default=0.6, help="extra seconds to wait after audio length")
    p.add_argument("--timeout", type=float, default=120.0)
    p.add_argument("--personality", action="store_true")
    p.add_argument("texts", nargs="+")
    args = p.parse_args()

    host = os.environ.get("VOICEBOX_HOST", "http://127.0.0.1:17493").rstrip("/")
    rows = []
    ok = True
    for i, text in enumerate(args.texts, 1):
        body = {"text": text, "profile": args.profile}
        if args.engine:
            body["engine"] = args.engine
        if args.personality:
            body["personality"] = True
        t0 = time.monotonic()
        try:
            resp = _post(f"{host}/speak", body)
        except urllib.error.HTTPError as e:
            print(f"#{i} HTTP {e.code}: {e.read().decode('utf-8','replace')[:300]}", file=sys.stderr)
            ok = False
            continue
        gen_id = resp.get("id", "")
        status, last, _ = _wait(host, gen_id, args.timeout)
        gen_time = time.monotonic() - t0
        audio_len = last.get("duration")
        eng = last.get("engine") or resp.get("engine") or args.engine or "?"
        prof = last.get("profile_id") or args.profile
        chars = len(text)
        rows.append((i, chars, status, gen_time, audio_len, eng))
        rtf = (gen_time / audio_len) if audio_len else None
        print(f"#{i:>2}  chars={chars:>4}  status={status:<10} gen={gen_time:6.2f}s  "
              f"audio={audio_len if audio_len is None else f'{audio_len:5.2f}s'}  "
              f"rtf={'n/a' if rtf is None else f'{rtf:.2f}x'}  engine={eng}")
        if status != "completed":
            ok = False
        # Don't talk over the clip that's now playing.
        if audio_len:
            time.sleep(audio_len + args.buffer)
        else:
            time.sleep(args.buffer)

    if rows:
        good = [r for r in rows if r[2] == "completed" and r[4]]
        if good:
            avg_gen = sum(r[3] for r in good) / len(good)
            avg_rtf = sum(r[3] / r[4] for r in good) / len(good)
            print(f"--- {args.profile} ({rows[0][5]}): avg gen={avg_gen:.2f}s  avg rtf={avg_rtf:.2f}x  "
                  f"(rtf = generation time / seconds of audio; lower is faster)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
