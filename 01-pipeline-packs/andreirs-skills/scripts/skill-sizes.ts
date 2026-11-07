#!/usr/bin/env bun
/**
 * Measure each skill's SKILL.md (lines / words / ~tokens) and print a markdown
 * table. Run from the repo root.
 *
 *   bun scripts/skill-sizes.ts          # print the table to stdout
 *   bun scripts/skill-sizes.ts --write  # also rewrite the table in README.md
 *
 * Only SKILL.md is counted — the instruction prose — so bundled templates,
 * scripts, dependencies, and profile data don't distort the comparison. Tokens
 * are estimated as bytes / 4: a rough proxy, good enough to keep us honest about
 * conciseness.
 */
import { readdirSync, statSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const ROOT = process.cwd();
const START = "<!-- skill-sizes:start -->";
const END = "<!-- skill-sizes:end -->";

type Row = { skill: string; lines: number; words: number; tokens: number };

function measure(skillMd: string): Omit<Row, "skill"> {
  const text = readFileSync(skillMd, "utf8");
  return {
    lines: (text.match(/\n/g) ?? []).length,
    words: text.split(/\s+/).filter(Boolean).length,
    tokens: Math.round(Buffer.byteLength(text, "utf8") / 4),
  };
}

// Every top-level dir that contains a SKILL.md is a skill.
const topLevel = readdirSync(ROOT, { withFileTypes: true })
  .filter((e) => e.isDirectory() && e.name !== ".git")
  .map((e) => ({ name: e.name, md: join(ROOT, e.name, "SKILL.md") }));

// Skills bundled inside marketplace plugins: marketplace/plugins/<p>/skills/<s>/SKILL.md
const PLUGINS = join(ROOT, "marketplace", "plugins");
const pluginSkills = (() => {
  try {
    return readdirSync(PLUGINS, { withFileTypes: true })
      .filter((p) => p.isDirectory())
      .flatMap((p) => {
        const skillsDir = join(PLUGINS, p.name, "skills");
        try {
          return readdirSync(skillsDir, { withFileTypes: true })
            .filter((s) => s.isDirectory())
            .map((s) => ({ name: `${s.name} (plugin)`, md: join(skillsDir, s.name, "SKILL.md") }));
        } catch { return []; }
      });
  } catch { return []; }
})();

const rows: Row[] = [...topLevel, ...pluginSkills]
  .filter((e) => { try { return statSync(e.md).isFile(); } catch { return false; } })
  .map((e) => ({ skill: e.name, ...measure(e.md) }))
  .sort((a, b) => b.tokens - a.tokens);

const n = (x: number) => x.toLocaleString("en-US");
const total = rows.reduce(
  (t, r) => ({ lines: t.lines + r.lines, words: t.words + r.words, tokens: t.tokens + r.tokens }),
  { lines: 0, words: 0, tokens: 0 },
);

const table = [
  "| Skill | Lines | Words | ~Tokens |",
  "|---|--:|--:|--:|",
  ...rows.map((r) => `| \`${r.skill}\` | ${n(r.lines)} | ${n(r.words)} | ${n(r.tokens)} |`),
  `| **Total** | **${n(total.lines)}** | **${n(total.words)}** | **${n(total.tokens)}** |`,
].join("\n");

if (process.argv.includes("--write")) {
  const path = join(ROOT, "README.md");
  const readme = readFileSync(path, "utf8");
  const s = readme.indexOf(START), e = readme.indexOf(END);
  if (s === -1 || e === -1) {
    console.error(`Markers ${START} / ${END} not found in README.md`);
    process.exit(1);
  }
  const next = readme.slice(0, s + START.length) + "\n" + table + "\n" + readme.slice(e);
  writeFileSync(path, next);
  console.error("README.md table updated.");
} else {
  console.log(table);
}
