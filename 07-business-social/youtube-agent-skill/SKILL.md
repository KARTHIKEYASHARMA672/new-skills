---
name: youtube-agent-skill
description: >-
  Eleven YouTube agent skills that run and grow a YouTube channel: video script writing with 21 scored hook formulas (/yt-script), title and thumbnail packaging & linter (/yt-package), transcript-to-EDL editor with dead air removal (/yt-edit), audience retention cliff & slide analyzer (/yt-retention), Shorts extractor (/yt-shorts), validated chapter generator (/yt-chapters), niche virality & outlier multiple ranker (/yt-viral), comment triager & replies (/yt-comment), weekly channel planning (/yt-plan), SEO description & tag optimizer (/yt-seo), and single-fix channel audit (/yt-audit). Use whenever the user asks about YouTube, /yt-script, /yt-package, /yt-edit, /yt-retention, /yt-shorts, /yt-chapters, /yt-viral, /yt-comment, /yt-plan, /yt-seo, /yt-audit, video scripts, hooks, titles, thumbnails, editing, retention, or channel strategy.
---

# 🎥 YouTube Agent Skill Suite

> **Production-grade YouTube operational agent suite featuring 11 specialized workflows and 6 zero-dependency Python tools to script, package, edit, audit, and grow a YouTube channel.**
>
> **Core Principle:** *These skills write and optimize. You upload and publish. Nothing gets published unattended.*

---

## 📋 Quick Command Reference

| Command | Workflow | Included Tool / Script | Primary Output |
| :--- | :--- | :--- | :--- |
| **`/yt-script`** | Scriptwriting from raw idea | `hookscore.py` (21 hook formulas) | Top 2 scored hooks + full spoken script with retention beats |
| **`/yt-package`** | Title & thumbnail pairing | `title.py` (duplication & cut linter) | 60-char title + non-duplicative, punchy thumbnail text |
| **`/yt-edit`** | Edit Decision List from transcript | `deadair.py` (dead air & filler cutter) | EDL with exact timecodes for dead air, fillers, and retakes |
| **`/yt-chapters`** | Validated YouTube chapters | `chapters.py` (pause & boundary detector) | Compliant chapter list starting at `00:00` (min 3 ch, min 10s) |
| **`/yt-retention`** | Audience retention leak analysis | `retention.py` (cliff & slide auditor) | Hook leak % (first 30s), cliffs with transcript quotes, bleed rate |
| **`/yt-shorts`** | Long-form to Shorts extraction | Python-assisted text extraction | 3–5 vertical Short concepts with rewritten first lines |
| **`/yt-viral`** | Niche outlier virality ranker | `swipe.py` (channel-median multiple) | Outlier videos ranked by multiple over channel's own median |
| **`/yt-comment`** | Comment section triage & reply | Persona matching engine | 4-category triage (Questions, Criticism, Stories, Praise) + replies |
| **`/yt-plan`** | Realistic weekly production plan | Creator bandwidth balancer | 1 anchor video + 1 lightweight video + 3 Shorts schedule |
| **`/yt-seo`** | Search & metadata optimization | Tag & query selector | Above-the-fold description, key search queries, high-value tags |
| **`/yt-audit`** | Full-channel bottleneck audit | Diagnostic triage engine | Single highest-leverage bottleneck fix (not a generic list of 20) |

---

## 🛠️ The 6 Standalone Python CLI Tools

Every tool runs on clean Python 3 with standard library only (zero `pip` dependencies):

```bash
# 1. Score and rank hook options against 21 proven formulas
python skills/yt-script/hookscore.py --hook "Here is why your YouTube channel is dying"
python skills/yt-script/hookscore.py hooks.txt

# 2. Lint title and thumbnail as an integrated pairing
python skills/yt-package/title.py --title "I built an AI agent in 24 hours" --thumb "AI AGENT"

# 3. Generate an Edit Decision List (EDL) from an SRT/VTT/Whisper JSON transcript
python skills/yt-edit/deadair.py transcript.srt --floor 0.35

# 4. Generate compliant YouTube chapters from transcript pauses & boundaries
python skills/yt-chapters/chapters.py transcript.srt --target 8

# 5. Diagnose Studio audience retention dropoffs and match against spoken words
python skills/yt-retention/retention.py retention.csv --transcript transcript.srt

# 6. Rank collected niche videos by multiple over channel median
python skills/yt-viral/swipe.py collected.json --min 2.0
```

---

## 🎙️ Voice Profile Configuration (`voice.md`)

Before generating scripts, titles, or replies, check for the creator's voice profile:
- Primary location: `~/.claude/youtube/voice.md`
- Fallback location: `templates/voice.md` within this skill directory

If `voice.md` is empty or missing, request transcripts or links from **three of the creator's existing videos** to infer tone, pacing, vocabulary, forbidden jargon, and personal credentials.

---

## 📖 Detailed Workflow Procedures

### 1. `/yt-script` — Idea into Retention-Engineered Script
- **First 15 Seconds:** The entire video lives or dies here. Write **5 hook options** across the 21 formulas (`skills/yt-script/hooks.json`).
- Run them through `hookscore.py`. Select the top 2 hooks and present both with numerical scores (Specificity, Address, Stakes, Curiosity, Brevity).
- **The Turn (0:15–0:45):** Immediately validate the promise. No generic intro or subscribe begging.
- **The Body:** One core idea per beat with explicit **ON-SCREEN visual cues** marked.
- **The Payoff:** Concretely deliver the promised asset or proof before the video concludes.

### 2. `/yt-package` — Integrated Title & Thumbnail Packaging
- Test title + thumbnail together using `title.py`.
- **Title Rules:** Under 60 characters for desktop/mobile safety. Carries concrete numbers or nouns.
- **Thumbnail Rules:** Never repeat words already in the title. Focus on visual contrast and curiosity.
- Deliver 3 alternative pairings: *Direct / Curiosity / Contrarian*.

### 3. `/yt-edit` — Transcript to Edit Decision List (EDL)
- Feed `transcript.srt`, `.vtt`, or Whisper `.json` into `deadair.py`.
- Flags dead air gaps longer than the threshold (default: 0.35s).
- Identifies filler words (`um`, `uh`, `so yeah`, `basically`) and restart retakes.
- Outputs timestamped EDL with projected runtime reduction.

### 4. `/yt-chapters` — Verified YouTube Chapters
- Run `chapters.py` on your transcript to identify boundary pauses.
- Enforces YouTube's hard requirements: starts at `00:00`, minimum 3 chapters, each chapter ≥10 seconds.
- Formats ready-to-paste description timestamps.

### 5. `/yt-retention` — Audience Retention Leak Diagnostic
- Export CSV from YouTube Studio: *Analytics → Video → Engagement → Audience Retention → Download CSV*.
- Run `retention.py retention.csv [--transcript transcript.srt]`.
- Pinpoints:
  1. **Hook Leak:** Percentage lost in first 30 seconds (target: retain ≥70%).
  2. **Cliffs:** Sudden drops >3% across 5 seconds with transcript quotes of what was said.
  3. **Slide:** Continuous drift slope across the middle section.

### 6. `/yt-shorts` — Long-Form to Vertical Shorts Extraction
- Scans long-form transcripts for self-contained 30–60 second insights.
- Writes a **new punchy opening hook line** for each Short (since the original mid-video section lacks an entry hook).
- Identifies exact start/end timecodes for vertical clipping.

### 7. `/yt-viral` — Niche Outlier Virality Ranker
- Ingests JSON list of niche competitor videos (`title`, `channel`, `views`, `url`).
- Computes each video's view count as a **multiple of that specific channel's median views**.
- Isolates genuinely viral outliers (e.g. 5x+ channel median) and maps title structures to proven formulas.

### 8. `/yt-comment` — Comment Section Triage & Response
- Sorts viewer comments into 4 actionable buckets:
  1. **Questions** (Opportunities for follow-up content or pinned answers)
  2. **Criticisms** (Valid feedback vs bad-faith noise)
  3. **Stories** (Viewer experiences to highlight)
  4. **Praise** (Authentic community building)
- Drafts personalized replies matching `voice.md`.

### 9. `/yt-plan` — Sustainable Weekly Content Plan
- Assesses true creator availability (hours/week).
- Structures a realistic content mix: **1 Anchor Video** (search/authority), **1 Lean Video** (fast reaction/workflow), and **3 Shorts** (reach).

### 10. `/yt-seo` — Search & Discovery Metadata
- Drafts the crucial first 2 lines of the video description (above the fold).
- Targets the 3 specific high-intent search queries the video can realistically win.
- Recommends 5–8 targeted tags (no spam tagging).

### 11. `/yt-audit` — Channel Diagnostic & Single Bottleneck Fix
- Audits channel banner, titles, thumbnails, view-to-sub ratios, and retention history.
- Concludes with **ONE prioritized bottleneck fix** to implement immediately.

---

## 🔒 Safety & Operational Rules

1. **No Direct Publishing:** Never attempt automated upload or posting. All outputs are copy-ready drafts for human review.
2. **Heuristic Honesty:** Hook scores and title rankings are calibrated heuristics, not guarantees of algorithmic success.
3. **No Hallucinated Data:** When analyzing retention or transcripts, only cite actual numbers and quotes present in user-provided files.
