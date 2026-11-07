#!/usr/bin/env bun
// Drives Garmin Connect through the `agent-browser` CLI (no Playwright).
// State (cookies + localStorage) is persisted under the named session
// "garmin", so once you sign in headed the session survives across runs.
import { existsSync, mkdirSync } from "node:fs";
import { homedir } from "node:os";
import { join, resolve } from "node:path";

type Activity = {
  id: string;
  date: string;
  name: string;
  type: string;
};

type Result = Activity & {
  path?: string;
  ok: boolean;
  err?: string;
};

const SCRIPT_DIR = new URL(".", import.meta.url).pathname;
const PROFILE_DIR = join(SCRIPT_DIR, "profile");
const ACTIVITIES_URL = "https://connect.garmin.com/app/activities";
const ACTIVITY_URL = (id: string) =>
  `https://connect.garmin.com/app/activity/${id}`;

// Garmin Connect sits behind Cloudflare bot management. The bundled Chromium +
// state-save approach gets challenged and logged out; driving the *real* Chrome
// binary with a dedicated persistent profile passes the challenge and keeps
// auth on disk across runs. So this skill always runs headed against that
// profile — sign in once and the profile stays authenticated.
const CHROME =
  process.env.AGENT_BROWSER_EXECUTABLE_PATH ||
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

function parseArgs(argv: string[]) {
  const args = {
    days: 7,
    ids: [] as string[],
    out: "",
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--days") args.days = parseInt(argv[++i], 10);
    else if (a === "--ids")
      args.ids = argv[++i].split(",").map((s) => s.trim()).filter(Boolean);
    else if (a === "--out") args.out = argv[++i];
    // --headed accepted for backward compat; we always run headed now.
  }
  if (!args.out) {
    const today = new Date().toISOString().slice(0, 10);
    args.out = join(homedir(), "Downloads", `garmin-${today}`);
  }
  args.out = resolve(args.out.replace(/^~/, homedir()));
  return args;
}

// Run an agent-browser command against the persistent Garmin Chrome profile.
async function ab(
  cmd: string[],
  opts: { stdin?: string; timeoutMs?: number } = {},
): Promise<{ stdout: string; stderr: string; code: number }> {
  // Launch options (executable, profile, headed, anti-bot flag) are honored on
  // the call that cold-starts the daemon and harmlessly ignored on later calls.
  // --disable-blink-features=AutomationControlled keeps navigator.webdriver false.
  const globals = [
    "--executable-path",
    CHROME,
    "--profile",
    PROFILE_DIR,
    "--headed",
    "--args",
    "--disable-blink-features=AutomationControlled",
  ];
  const proc = Bun.spawn(["agent-browser", ...globals, ...cmd], {
    stdin: opts.stdin ? new TextEncoder().encode(opts.stdin) : "ignore",
    stdout: "pipe",
    stderr: "pipe",
  });
  const code = await proc.exited;
  const stdout = await new Response(proc.stdout).text();
  const stderr = await new Response(proc.stderr).text();
  return { stdout, stderr, code };
}

// Run JavaScript in the page and parse its JSON result. The eval context reuses
// globals across calls, so each body runs inside its own IIFE to avoid
// "Identifier already declared" collisions; the body must `return` its value.
async function evalJson<T>(body: string): Promise<T> {
  const js = `(() => {\n${body}\n})();`;
  const { stdout, stderr, code } = await ab(["eval", "--stdin"], { stdin: js });
  if (code !== 0) throw new Error(`eval failed: ${stderr || stdout}`);
  const trimmed = stdout.trim();
  try {
    return JSON.parse(trimmed) as T;
  } catch {
    throw new Error(`eval did not return JSON: ${trimmed.slice(0, 200)}`);
  }
}

async function ensureSignedIn() {
  await ab(["open", ACTIVITIES_URL]);
  // Cloudflare's "Just a moment" interstitial can sit for a few seconds before
  // the activities list renders, so wait for an activity row rather than
  // checking the URL immediately.
  const w = await ab(["wait", 'a[href^="/app/activity/"]'], {
    timeoutMs: 30000,
  });
  if (w.code !== 0) {
    const url = (await ab(["get", "url"])).stdout.trim();
    if (url.includes("sso.garmin.com") || url.includes("/sign-in")) {
      process.stderr.write(
        "profile expired or sign-in required — a headed Chrome window is open; sign in there, then re-run\n",
      );
    } else {
      process.stderr.write(`no activities loaded: ${w.stderr || w.stdout}\n`);
    }
    process.exit(2);
  }
}

async function listActivities(): Promise<Activity[]> {
  // Mirrors the old Playwright $$eval scrape, run via agent-browser eval.
  const js = `
    const seen = new Set();
    const out = [];
    for (const a of document.querySelectorAll('a[href^="/app/activity/"]')) {
      const href = a.getAttribute("href") || "";
      const m = href.match(/\\/app\\/activity\\/(\\d+)/);
      if (!m) continue;
      const id = m[1];
      if (seen.has(id)) continue;
      seen.add(id);
      const name = (a.textContent || "").trim();
      // Walk up to the smallest ancestor that holds exactly this one activity link.
      let row = a;
      for (let i = 0; i < 8; i++) {
        const parent = row.parentElement;
        if (!parent) break;
        if (parent.querySelectorAll('a[href^="/app/activity/"]').length > 1) break;
        row = parent;
      }
      const text = row.innerText || "";
      const dateMatch = text.match(
        /(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\s+(\\d{1,2})\\s*\\n?\\s*(\\d{4})/,
      );
      const date = dateMatch
        ? dateMatch[3] + "-" + dateMatch[1] + "-" + dateMatch[2].padStart(2, "0")
        : "";
      let typeText = "";
      for (const btn of row.querySelectorAll("button")) {
        const label = (btn.getAttribute("aria-label") || "").trim();
        const t = (btn.textContent || "").trim();
        const candidate = label || t.replace(/▼/g, "").trim();
        if (!candidate) continue;
        if (/^(Event|Course|Edit|Like|Favorite|Toggle|Privacy|More)/i.test(candidate)) continue;
        if (candidate.length > 40) continue;
        typeText = candidate;
        break;
      }
      out.push({ id, date, name, type: typeText });
    }
    return out;
  `;
  return await evalJson<Activity[]>(js);
}

function monthIdx(mon: string): number {
  return ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"].indexOf(mon);
}

function activityDateObj(a: Activity): Date | null {
  // a.date is "YYYY-Mon-DD" e.g. "2026-May-16"
  const m = a.date.match(/^(\d{4})-([A-Za-z]{3})-(\d{2})$/);
  if (!m) return null;
  const mi = monthIdx(m[2]);
  if (mi < 0) return null;
  return new Date(parseInt(m[1], 10), mi, parseInt(m[3], 10));
}

async function downloadOne(id: string, outDir: string): Promise<string> {
  await ab(["open", ACTIVITY_URL(id)]);
  // SPA: wait for the "More..." control that opens the export menu.
  const ready = await ab(["wait", '[title="More..."]'], { timeoutMs: 25000 });
  if (ready.code !== 0) throw new Error("activity page never loaded the More menu");

  // Open the More menu and tag the "Export Splits to CSV" item with a stable
  // selector we can hand to `download`.
  const opened = await evalJson<boolean>(`
    const more = document.querySelector('[title="More..."]');
    const toggle = more && (more.querySelector('[aria-label="Toggle Menu"]') || more.querySelector('button'));
    if (toggle) toggle.click();
    const items = document.querySelectorAll('a, button, li, span, div');
    let found = false;
    for (const el of items) {
      if ((el.textContent || "").trim() === "Export Splits to CSV") {
        el.setAttribute("data-ab-export", "1");
        found = true;
        break;
      }
    }
    return found;
  `);
  if (!opened) throw new Error('"Export Splits to CSV" not found in More menu');

  const path = join(outDir, `activity-${id}.csv`);
  const dl = await ab(["download", '[data-ab-export="1"]', path], {
    timeoutMs: 25000,
  });
  if (dl.code !== 0 || !existsSync(path)) {
    throw new Error(`download failed: ${dl.stderr || dl.stdout}`);
  }
  return path;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!existsSync(args.out)) mkdirSync(args.out, { recursive: true });

  try {
    await ensureSignedIn();
    const all = await listActivities();

    let targets: Activity[];
    if (args.ids.length > 0) {
      const byId = new Map(all.map((a) => [a.id, a]));
      targets = args.ids.map(
        (id) => byId.get(id) ?? { id, date: "", name: "", type: "" },
      );
    } else {
      const cutoff = new Date();
      cutoff.setHours(0, 0, 0, 0);
      cutoff.setDate(cutoff.getDate() - (args.days - 1));
      targets = all.filter((a) => {
        const d = activityDateObj(a);
        return d !== null && d >= cutoff;
      });
    }

    const results: Result[] = [];
    for (const a of targets) {
      try {
        const path = await downloadOne(a.id, args.out);
        results.push({ ...a, path, ok: true });
      } catch (e) {
        results.push({ ...a, ok: false, err: String(e).slice(0, 300) });
      }
    }

    console.log(JSON.stringify(results, null, 2));
    process.exit(results.length > 0 && results.every((r) => r.ok) ? 0 : 1);
  } catch (e) {
    process.stderr.write(`fatal: ${String(e)}\n`);
    process.exit(1);
  }
}

main();
