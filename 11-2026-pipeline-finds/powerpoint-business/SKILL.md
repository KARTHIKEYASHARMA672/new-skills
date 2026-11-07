---
name: powerpoint-business
description: |
  Create visually polished business and humanities PowerPoint presentations using SVG-native generation.
  LLM generates SVG slides directly (1280x720) — exported as editable SVG-embedded PPTX (Office 365+).
  5 specialized agent roles (Consultant → Researcher → Planner → Designer → Reviewer) collaborate
  through a 8-phase pipeline with user approval gates. Bento Grid card layouts, 14 themes
  (10 business + 4 academic/humanities), 206 Lucide SVG icons, 28 chart templates,
  CRAP design optimizer, and semantic manifest for natural language editing.
  Trigger on: powerpoint, pptx, PPT, 做PPT, 做幻灯片, business slides, 商务PPT, business presentation,
  做个报告, 做个演示, make slides (when business/humanities context), prepare a presentation (non-academic),
  商务报告, 企业介绍, 产品发布, investor deck, pitch deck, 汇报, training deck, marketing presentation.
  Even if the user just says "make slides" or "做个演示" without specifying format, trigger this skill
  when the context is clearly business/humanities — not academic. If ambiguous, ask the user.
  Do NOT trigger on: beamer, latex slides, .tex, tikz, academic paper, theorem, proof, seminar,
  讨论班, 论文讲解 — those belong to the beamer or powerpoint-slides (academic) skill.
argument-hint: "[action] [topic/file] — actions: create, edit, undo, retheme, export, preview, review"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent", "AskUserQuestion", "TaskCreate", "TaskUpdate", "TaskList", "TaskGet", "WebSearch", "WebFetch"]
---

# PowerPoint Business — SVG-Native Slide Generation

Business/humanities presentation skill. Full lifecycle:
analyze → interview → research → outline → plan → draft SVG → design SVG → export.

Execution model: LLM generates SVG (1280x720) per slide → SVG embedded in OOXML PPTX (editable in Office 365+, PNG fallback for older versions).
Editing: natural language → semantic manifest element lookup → targeted SVG regeneration.

---

## 0. Quick Reference

| Action | Command | Description |
|--------|---------|-------------|
| Create from topic/file | `create [topic]` | Full Phase 0-7 pipeline |
| Edit slides | `edit [project]` | Natural language editing |
| Undo edit | `undo [project] [slide]` | Restore previous slide version |
| Switch theme | `retheme [project] [theme]` | Regenerate Design SVGs from Drafts |
| Export | `export [project]` | Re-export PPTX + HTML |
| Preview | `preview [project]` | Generate and open HTML preview |
| Review | `review [project]` | Run Reviewer QA on slides |
| CRAP Review | `review [project] --crap` | Run CRAP design optimization check |

Parse `$ARGUMENTS` to determine action. If none specified, ask.

---

## 1. Hard Rules

1. **Semantic IDs on every SVG element** — `s{nn}-{role}-{index}` format. No anonymous elements.
2. **Safe area** — 60px padding on all sides. Canvas 1280x720, usable area 1160x600.
3. **Card gap >= 20px** — never closer.
4. **No external image references** — all inline. User images: base64 embedded.
5. **Draft ≠ Design** — Design phase must not alter text content or card count. Minor size adjustments for theme fit OK.
6. **Layout diversity** — never use same layout for 3+ consecutive slides.
7. **Information density** — max 7 bullets, max 5 cards, max 80 CJK chars per card body.
8. **Font size floor** — minimum 12px.
9. **Color contrast** — WCAG AA >= 4.5:1. Verified by `check_svg.py`.
10. **Manifest sync** — after any SVG change, run `sync_manifest.py`. Script is source of truth.
11. **Two HARD STOPs** — user confirms requirements (Phase 1) and outline (Phase 3).
12. **Research tags** — web-sourced info tagged: confirmed / probable / unverified.
13. **`<foreignObject>` for multi-line text** — card bodies use `<foreignObject>` + HTML div. Single-line (titles, stats) use `<text>`.
14. **Version before edit** — copy current SVG to `slides/history/` before any edit.

---

## 2. Themes & Layout

**14 themes** (10 business + 4 academic/humanities):
- Business: Corporate Blue (default), Warm Earth, Minimal White, Tech Dark, Emerald Gold, Royal Purple, Sunset Coral, Nordic Sage, Ocean Teal, Rose Dusk.
- Academic/Humanities: Zen Ink (禅意水墨), Academic Classic (学术经典), Parchment (自然书卷), Pure Academic (极简学术).

**14 Bento Grid layouts** + 3 semantic visualization components: content-driven, not template-based.
**206 Lucide SVG icons** across 9 categories: general, communication, data, business, education, humanities, nature, status, arrows.
**28 chart templates** indexed by analysis goal in `references/charts-index.json`.

**Read `references/themes.yaml`** for full theme definitions (color scheme, typography, card style, elevation, decoration).
**Read `references/bento-grid.md`** for layout strategies, density targets, card constraints, and structural components.
**Read `references/svg-conventions.md`** for SVG generation rules (IDs, fonts, multi-layer backgrounds, dynamic sizing, data viz).
**Read `references/cognitive-design.md`** for evidence-based design principles (Miller's Law, Mayer, Gestalt, cognitive load, narrative arc).

---

## 3. Agent Roles

5 specialized roles, orchestrated by Lead Agent (this skill). Each role has a dedicated
system prompt in `prompts/`. Dispatch as Agent subagents with the corresponding prompt.

| Role | Prompt | Phases | Key Output |
|------|--------|--------|------------|
| Consultant | `prompts/consultant.md` | 0-1 | `requirements.md` |
| Researcher | `prompts/researcher.md` | 2 | `research/chapter-{nn}.md` |
| Planner | `prompts/planner.md` | 3-4 | `outline.json` + `planning-draft.md` |
| Designer | `prompts/designer.md` | 5-6 | `slides/*.svg` + `slide-manifest.json` |
| Reviewer | `prompts/reviewer.md` | 6 QA | `reviews/*.md` + `reviews/scores.json` |

**Role boundaries**: each role reads only upstream outputs, never modifies other roles' artifacts.
Reviewer feedback routes to the correct role (content issues → Planner, visual → Designer).

---

## 4. Actions

### 4.1 `create [topic/file]` — Full Pipeline (Phase 0-7)

#### Phase 0: Material Analysis (Consultant)

Read user-provided materials (PDF, Word, text, URL). Extract key information, data points,
logical structure, target audience cues. If user provides only a topic string with no materials,
note that Phase 2 research will be essential.

**Proceed directly to Phase 1 — do not present analysis yet.**

#### Phase 1: Requirements Interview (Consultant) — HARD STOP

Dispatch Consultant agent with `prompts/consultant.md`. The Consultant handles:
- Interactive requirements interview via `AskUserQuestion` tool (questions, options, recommendations)
- Additional topic-specific questions as needed beyond baseline 5
- Produces `requirements.md` (audience, purpose, scope, style, content strategy, rough chapter outline)

**User must confirm requirements before proceeding.**

#### Phase 2: Web Research (Researcher) — Optional

Only if user requested. Dispatch Researcher agent. Read `prompts/researcher.md`.

Process: Planner produces rough outline first → Researcher supplements per chapter using
grok-search → Planner refines. Max 1 iteration cycle.

Output: `research/chapter-{nn}.md` files, confidence-tagged.

#### Phase 3: Pyramid Outline (Planner) — HARD STOP

Dispatch Planner agent. Read `prompts/planner.md`.

Apply Pyramid Principle + select narrative framework (Pyramid/SCQA/PAS/Hero's Journey).
Output structured `outline.json`.

**Present outline to user. User must approve before proceeding.**

#### Phase 4: Planning Draft (Planner)

Same Planner agent continues. For each page, produce 8-field planning card:

| Field | Content |
|-------|---------|
| Objective | What this slide achieves |
| Core Message | Single takeaway |
| Evidence | Data source |
| Layout | Bento Grid type + card count |
| Info Hierarchy | Primary > Secondary > Tertiary |
| Keywords | Key terms and numbers |
| Visual Elements | Charts, diagrams, images |
| Design Notes | Guidance for Designer |

Output: `planning-draft.md`

#### Phase 5: Draft SVG (Designer)

Dispatch Designer agent. Read `prompts/designer.md`.

Generate one SVG per slide (1280x720). Focus on content + layout, neutral gray palette.
Every element gets semantic ID. Batch: 3-5 slides per subagent.

Output: `drafts/slide-{nn}-draft.svg`

#### Phase 6: Design SVG + QA (Designer + Reviewer)

Designer injects theme style onto Draft SVGs. Does NOT change content/layout, only visual polish.

Then Reviewer runs two-layer QA:
1. `scripts/check_svg.py` — automated (well-formedness, safe area, contrast, gaps)
2. LLM review — layout balance, density, typography, aesthetics

Quality gate: >= 7.0 pass, 5.0-6.9 fix loop (max 2 rounds), < 5.0 redesign.

Output: `slides/slide-{nn}.svg` + `slide-manifest.json` + `reviews/`

#### Phase 7: Export

```bash
# Generate manifest from final SVGs
python ~/.claude/skills/powerpoint-business/scripts/sync_manifest.py slides/ slide-manifest.json

# Export PPTX (SVG-embed, editable in Office 365+)
python ~/.claude/skills/powerpoint-business/scripts/export_pptx.py slides/ output/presentation.pptx

# Generate HTML preview
python ~/.claude/skills/powerpoint-business/scripts/preview.py slides/ output/index.html

# Open preview
open output/index.html
```

#### Post-Creation Checklist

```
[ ] All SVGs well-formed (check_svg.py passes)
[ ] Manifest synced (sync_manifest.py run)
[ ] QA score >= 7.0
[ ] Layout diversity — no 3+ consecutive same layout
[ ] PPTX generated and non-empty
[ ] HTML preview opens correctly
[ ] Speaker notes in output/speaker-notes.md
```

---

### 4.2 `edit [project]`

Natural language editing. User describes change in plain language.

1. Read `slide-manifest.json` to locate target element(s)
2. Backup current SVG to `slides/history/slide-{nn}.v{ver}.svg`
3. Dispatch Designer with current SVG + targeted instruction
4. Run `sync_manifest.py` to update manifest
5. Re-export PPTX + HTML

**Edit granularity**:
- Element edit: single text/color/size change
- Slide redesign: regenerate entire slide
- Theme switch: → use `retheme` action instead
- Batch replace: find-and-replace across all slides

---

### 4.3 `undo [project] [slide]`

Restore previous version from `slides/history/`. Update manifest. Re-export.

---

### 4.4 `retheme [project] [theme]`

Regenerate all Design SVGs from Draft SVGs using new theme. Drafts in `drafts/` are preserved.
Re-run full QA cycle. Re-export.

---

### 4.5 `export [project]`

Re-export from current SVGs:
```bash
python ~/.claude/skills/powerpoint-business/scripts/export_pptx.py slides/ output/presentation.pptx
python ~/.claude/skills/powerpoint-business/scripts/preview.py slides/ output/index.html
```

---

### 4.6 `preview [project]`

Generate HTML preview and open in browser:
```bash
python ~/.claude/skills/powerpoint-business/scripts/preview.py slides/ output/index.html
open output/index.html
```

---

### 4.7 `review [project]`

Run Reviewer on existing slides. Dispatch Reviewer agent with `prompts/reviewer.md`.
Produces `reviews/` directory with per-slide reports and scores.

---

## 5. Dependencies

**Required**:
```bash
pip install python-pptx lxml cairosvg
```

**Optional**:
- `matplotlib` — complex statistical charts (simple charts are inline SVG)
- `soffice` (LibreOffice) — PPTX → PDF QA verification

**Check before first run**:
```bash
python -c "import cairosvg; print('cairosvg OK')"
python -c "from pptx import Presentation; print('python-pptx OK')"
```

---

## 6. Troubleshooting

| Problem | Fix |
|---------|-----|
| cairosvg import error | `pip install cairosvg`; macOS may need `brew install cairo` |
| SVG text not wrapping | Use `<foreignObject>` for multi-line text, not `<text>` |
| PPTX blank slides | Check SVG well-formedness with `check_svg.py`; SVG-embed requires Office 365+ |
| Font fallback in preview | Install Noto Sans SC: `brew install font-noto-sans-cjk-sc` |
| Manifest out of sync | Run `sync_manifest.py` to regenerate from SVG |
| Reviewer score low | Check `reviews/` for specific issues; fix and re-run Design phase |
| matplotlib not found | `pip install matplotlib`; only needed for complex charts |
