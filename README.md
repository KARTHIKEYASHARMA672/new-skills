# Agent Skills Collection ("founded skills")

An internet-sourced agent-skill library in **SKILL.md format** (agentskills.io / Anthropic skill spec): each skill is a folder containing a `SKILL.md` file with YAML frontmatter (`name`, `description`, instructions). OpenCode and other agent loaders discover and trigger these automatically.

Assembled in **November 2026** in two passes:
1. **Curation pass** — ~20 parallel research agents pulled from public GitHub repos, official vendor bundles and community marketplaces, then curated into 9 category folders (~453 skills).
2. **Revisit pass (Nov 7, 2026)** — live registry sweeps (skills.sh, Tessl, marketplaces), awesome-list mining, and a video/ YouTube review produced a fresh 2026 shortlist. 51 new skills (68 including nested sub-skills) were cloned, license-checked and merged as categories `10-2026-fresh-finds/` and `11-2026-pipeline-finds/`, plus the accompanying **`Agent-Skills-Research-Report.pdf`**.

## Categories

| Folder | What's inside | SKILL.md |
|---|---|---|
| `01-pipeline-packs` | Multi-step workflow bundles: `superpowers-obra`, `mattpocock-engineering` (20), `mattpocock-productivity` (7), `compound-engineering-every` (37), `addyosmani-agent-skills` (25), `vercel-agent-skills` (9), `andreirs-skills` (31), `fpigeonjr-skills` (24), `planning-with-files-manus`, `shadcn-improve` | 170 |
| `02-official-vendor` | Official vendor bundles: `anthropics` (12 + template), `openai-curated-bundle` (39), `microsoft`, `huggingface` (25), `langchain-bundle`, `pydantic`, `supabase`, `prisma`, `hashnode`, `greensock-gsap` | 149 |
| `03-debug-review-test` | Debugging, code review, testing: `ahmedasmar-devops`, `anmolnagpal-devops`, `dividedby`, `glebis`, `ilude python-testing`, `microsoft-debugpy pytest` | 14 |
| `04-data-pipelines` | Data/analytics workflows: `dbt-labs-bundle`, `aws-samples`, `datavelopers`, `juanlurg-data-science`, `mohitjandwani` | 30 |
| `05-design-frontend` | UI/design/front-end: `shadcn`, `pbakaus impeccable`, `emilkowalski-animation`, `ui-ux-pro-max`, `atlassian-dataviz`, `coleam00 excalidraw-diagram` | 29 |
| `06-writing-research` | Writing & research: `robertnowell deep-research`, `kepano obsidian`, `lfurze book-editor`, `jeffzi write-plan/write-prose/write-doc`, `throokie article-writing`, `broeker reveal-deck`, `alirezarezvani`, `conventional-commits-nicholaswagner` | 20 |
| `07-business-social` | Marketing & social media: `charlie947-social-media`, `analyst-kit-finance`, `alirezarezvani` | 35 |
| `08-meta-discovery` | Skills about skills: `vercel find-skills`, `throokie-skill-creator`, `throokie-skill-stocktake` | 3 |
| `09-created-by-me` | Original skills authored for this collection: **perfect-task-pipeline**, **subagent-squad-orchestrator**, **pdf-report-builder** | 3 |
| `10-2026-fresh-finds` | 2026-verified fresh picks (MIT/Apache/CC0): `build-design`, `better-interface`, `hallmark`, `taste-skill`, `humanizer`, `emil-design-eng`, `motion-director`, `baoyu-diagram`, `anydesign`, `core-web-vitals`, `python-testing-patterns`, `durable-objects`, `migrate-to-rust`, `security-audit`, `differential-review`, `supabase-postgres-best-practices`, `prisma-client-api`, `aws-cdk-development`, `biopython`, `move-code-quality`, `hyperframes-cli`, `remotion-best-practices`, `caveman`, `microsoft-foundry`, `beads`, `pda-reframing`, `ios-simulator-skill`, `master-claude-for-legal`, `recursive-research`, `strategy-red-team`, `ponytail` (+ nested sub-skills in `data2story`, `microsoft-foundry`) | 36 |
| `11-2026-pipeline-finds` | Verified end-to-end pipeline skills (raw in → finished artifact out): `paper-writing`, `researchclaw`, `deep-research-cn`, `data2story`, `gtm-dashboard-builder`, `executive-dashboard-generator`, `data-visual-report-builder`, `prd-to-issues`, `new-app-pipeline`, `skill-deck`, `powerpoint-business`, `slide-skill`, `claude-shorts`, `videocut`, `kinocut-repurpose`, `content-engine`, `podcast-content-suite`, `gated-debug`, `fix-failing-tests`, `bug-hunt` | 32 |

## Numbers (verified Nov 7, 2026)

**521 `SKILL.md` files** · **6,597 files** · **102.8 MB** · **zero `.git` directories**

`170 + 149 + 14 + 30 + 29 + 20 + 35 + 3 + 3 + 36 + 32 = 521`

## How to use

- Point OpenCode at a skill folder, or copy the folder(s) you want into `.agents/skills/` — the loader finds anything containing a valid `SKILL.md`.
- Read the `description` in each `SKILL.md` to learn when the agent auto-triggers it.
- Verify a folder actually contains a `SKILL.md` before installing it.
- **Don't install all 521 skills globally** — that is context bloat. Cherry-pick what matches your workflow, e.g. `pdf-report-builder` + `perfect-task-pipeline` + `subagent-squad-orchestrator` for gated end-to-end work, or `docx/xlsx/pdf/pptx` + `webapp-testing` for document production.

## Provenance

Sources are public GitHub repos, official vendor bundles and community marketplaces (skills.sh, Tessl, agenticskills.io, agentskills.codes, claudemarketplaces.com, claudskills.com, skillsdirectory.com, buildwithclaude.com, brisk.vision/skills, opencodeskills.dev). Licenses remain with the upstream authors; anything without a license, or under CC BY-NC / CC BY-SA / GPL-3.0 was excluded or clearly flagged in the report. Full research trail, methodology, videos watched, sites visited (300+ URLs) and the complete verification receipt are in **`Agent-Skills-Research-Report.pdf`** in this folder.

*Last updated: November 7, 2026.*
