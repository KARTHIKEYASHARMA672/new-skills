#!/usr/bin/env python3
"""vbpoll.py — feedback loop for Voicebox TTS generations.

After a fire-and-forget `voicebox_speak` call you get back a `generation_id`
(and a relative `poll_url` like `/generate/<id>/status`). This script polls that
endpoint until the generation finishes and prints the final status plus how long
it took — so Claude can tell whether a clip actually rendered (and how slow a
given engine is) instead of guessing.

Usage:
    python3 vbpoll.py <generation_id> [--timeout 30] [--interval 0.25] [--json]

Env:
    VOICEBOX_HOST   base URL of the Voicebox server (default http://127.0.0.1:17493)

Exit codes: 0 completed · 1 failed/cancelled · 2 timeout · 3 host unreachable
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


def fetch(url: str) -> dict | None:
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            body = r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        # /status can 404 for a beat right after submit — treat as "not ready yet".
        if e.code == 404:
            return {}
        return None
    except (urllib.error.URLError, ConnectionError, TimeoutError):
        return None
    return _parse_body(body)


def _parse_body(body: str) -> dict:
    """The /status endpoint speaks Server-Sent Events: lines of `data: {json}`.
    Take the last data line; fall back to treating the whole body as JSON."""
    payloads = [ln[5:].strip() for ln in body.splitlines() if ln.startswith("data:")]
    for chunk in (payloads[-1:] or [body.strip()]):
        if not chunk:
            continue
        try:
            return json.loads(chunk)
        except json.JSONDecodeError:
            pass
    return {"_raw": body}


def main() -> int:
    p = argparse.ArgumentParser(description="Poll a Voicebox generation until it completes.")
    p.add_argument("generation_id")
    p.add_argument("--timeout", type=float, default=30.0, help="max seconds to wait (default 30)")
    p.add_argument("--interval", type=float, default=0.25, help="seconds between polls (default 0.25)")
    p.add_argument("--json", action="store_true", help="emit a single JSON line instead of text")
    args = p.parse_args()

    host = os.environ.get("VOICEBOX_HOST", "http://127.0.0.1:17493").rstrip("/")
    url = f"{host}/generate/{args.generation_id}/status"

    start = time.monotonic()
    last: dict | None = None
    # Quick liveness probe: if neither the host root nor the status URL answers, bail.
    if fetch(url) is None and fetch(host) is None:
        out = {"result": "unreachable", "host": host}
        print(json.dumps(out) if args.json else f"unreachable: {host} (is the Voicebox app running?)",
              file=sys.stderr)
        return 3

    while True:
        resp = fetch(url)
        if resp is not None:
            last = resp
        status = ""
        if isinstance(resp, dict):
            status = str(resp.get("status") or resp.get("state") or "").lower()
        elapsed = time.monotonic() - start

        if status in DONE:
            _emit(args.json, "ok", status, elapsed, last)
            return 0
        if status in BAD:
            _emit(args.json, "fail", status, elapsed, last)
            return 1
        if elapsed > args.timeout:
            _emit(args.json, "timeout", status or "unknown", elapsed, last)
            return 2
        time.sleep(args.interval)


def _emit(as_json: bool, result: str, status: str, elapsed: float, last: dict | None) -> None:
    if as_json:
        print(json.dumps({"result": result, "status": status,
                          "elapsed_s": round(elapsed, 2), "last_response": last}))
    else:
        tag = {"ok": "OK     ", "fail": "FAIL   ", "timeout": "TIMEOUT"}[result]
        line = f"{tag} status={status or '?'}  elapsed={elapsed:.2f}s"
        if result != "ok":
            line += f"  resp={last!r}"
        print(line)


if __name__ == "__main__":
    sys.exit(main())
