# reveal-deck

A Claude Code skill for building production-quality Reveal.js slide decks. Works two ways: from a markdown outline, or from scratch given just a topic. Ships with a named theme, component library, and layout system so you can reference specific pieces by name.

## Install

```
/install-skill https://github.com/broeker/reveal-deck
```

This symlinks the skill into `~/.claude/skills/`. The slash command is `/slides`.

**Optional but recommended:** The `frontend-design` skill improves Claude's visual decisions when customizing themes or handling design requests:

```
/install-skill https://github.com/anthropics/skills frontend-design
```

The `/slides` skill works fine without it — all theme and component CSS is self-contained. But if you plan to create custom themes or make significant design changes, `frontend-design` helps.

## Showcase

The toolkit includes a showcase deck that sells itself by being a great deck:

```
examples/showcase.html
```

Open it in any browser — it walks through the toolkit's best features as a polished presentation, demonstrating components in action rather than documenting them. Backdrop images, video backgrounds, SVG diagrams, stat highlights, auto-animate, fragments, split layouts, and more. When new features are added to the toolkit, they should appear in the showcase.

## What is Reveal.js?

[Reveal.js](https://revealjs.com/) is an open-source HTML presentation framework. Instead of PowerPoint or Google Slides, your deck is a single `index.html` file that runs in any web browser. This skill generates that file for you — you don't need to know HTML or CSS.

### Why Reveal.js?

- **Version-controllable** — it's just a text file, so it lives in Git alongside your code
- **No vendor lock-in** — works in any browser, no account or app needed
- **Portable** — email the HTML file, drop it on a server, or open it locally
- **Powerful** — supports animations, speaker notes, PDF export, live code, embedded iframes, and more
- **Themeable** — full control over design via CSS (this skill handles that for you)

### How it works

Your deck is an `index.html` file. To present, you just open it in a browser. That's it.

For local development, Claude will start a simple server for you:

```
http://localhost:8765
```

### Navigation

| Key | Action |
|-----|--------|
| Right arrow / Space | Next slide |
| Left arrow | Previous slide |
| Down arrow | Basement slide (deeper dive) |
| Up arrow | Back up from basement |
| `Esc` | Overview — see all slides, click to jump |
| `S` | Speaker view — notes, timer, next slide preview |
| `B` or `.` | Blackout screen |
| `F` | Fullscreen |
| `Alt + click` | Zoom into an element |
| `?` | Show all shortcuts |

### Slide structure

Slides flow **left to right** for the main narrative. Some slides have **basement slides** below them (navigate down) for deeper dives the presenter can skip or explore.

```
[Title] → [Slide 1] → [Slide 2] → [Slide 3] → [Closing]
                          ↓
                      [Detail 2a]
                          ↓
                      [Detail 2b]
```

### Speaker view

Press `S` to open a separate window with:
- Your speaker notes for the current slide
- A preview of the next slide
- A timer
- Current/total slide count

This is why every slide gets auto-generated speaker notes — they're there when you need them.

## Quick start

### Option A — From a markdown outline

```bash
mkdir ~/decks/my-talk && cd ~/decks/my-talk
```

Write your outline in markdown — one heading per slide, raw notes underneath:

```markdown
## What Is the Thing

A **thing** is a concept that does X. It matters because Y.

Key points:
- Point one
- Point two
- Point three with a lot of detail that might need to be trimmed or
  broken across multiple slides depending on density

## Why It Matters

Without the thing, you lose Z. With it, you gain A and B.
This is a comparison — show it side by side.

## How to Set It Up

Step 1: do this
Step 2: do that
Step 3: verify
```

Then tell Claude:

```
Build a deck from my-outline.md
```

Claude reads your outline, asks 3-5 quick questions, then generates a complete `index.html` in one pass.

### Option B — From a prompt (no outline)

```bash
mkdir ~/decks/my-talk && cd ~/decks/my-talk
```

Just describe what you want:

```
Build a deck about Git rebasing best practices for a team of junior devs
```

Claude will interview you (audience, tone, scope), then generate a proposed outline for your approval. Once you sign off, it builds the full deck. The outline is saved as `OUTLINE.md` for reference.

## What you get

- A single self-contained `index.html` — no external dependencies beyond CDN links
- Auto-calculated slide count and estimated duration on the title slide
- Section dividers inserted at topic breaks
- Components chosen to match content (code blocks, comparison panels, flow diagrams, etc.)
- Additional slides added where Claude spots gaps — flagged with speaker notes

## Iterating

Reference slides by their `{NNN}` slug:

```
tighten {003}
split {007} into two slides
drop {011}
add a section divider before {005}
switch the flow diagram on {007} to a step-list
```

## Themes

Themes define colors, fonts, backgrounds, and recommended components. Currently ships with:

| Theme | Description |
|-------|-------------|
| `electric-dark` | Dark background, neon lime/amber accents, dot-grid texture, terminal aesthetic (default) |

Specify a theme in your INSTRUCTIONS.md or during the interview. If you don't specify, `electric-dark` is used.

### Creating a new theme

Add a `.md` file to `themes/` with:
- YAML frontmatter: `name`, `category: theme`, `description`
- Font imports and family names
- CSS custom properties (must define `--dark`, `--panel`, `--accent`, `--amber`, `--text`, `--muted`, `--border`)
- Base styles, background treatment
- Recommended components list

## Components

Named, reusable UI elements. Reference by name when talking to Claude.

| Component | Description |
|-----------|-------------|
| `panel` | Bordered card with color accent and optional label |
| `codeblock` | Terminal-style code block with faux macOS dots |
| `callout` | Highlighted box for key takeaways |
| `comparison` | Side-by-side good/bad panels and verdict grids |
| `flow` | Horizontal process/lifecycle diagram |
| `step-list` | Numbered step list with circled numbers |
| `file-tree` | Monospace directory tree |
| `table` | Styled data table with accent headers |
| `badge` | Small pill label (status indicators) |
| `motif` | Repeating visual icon system — icon defined by theme (bolt, rocket, logo, etc.) |
| `filepath` | Inline path badge (amber/green variants) |
| `key-item` | Numbered takeaway list with large accent numbers |
| `resource-list` | Categorized link list for references slides |
| `stat-highlight` | Large number/metric with label — for data that needs to land |
| `quote` | Full-width pull quote with attribution — when the quote IS the slide |
| `agenda` | Table of contents with "you are here" highlight — auto-generated from sections |
| `timeline` | Horizontal timeline with milestones/dates — roadmaps, history, phases |
| `icon-grid` | Grid of icon + label + description — feature overviews, capabilities |
| `image` | Background images, inline photos, Unsplash stock, screenshots in browser frames |
| `terminal-embed` | **Advanced:** Live terminal in a slide via ttyd — requires separate install ([setup](#live-terminal-slides)) |
| `effects` | Reveal.js advanced features — fragments, auto-animate, backgrounds, transitions |

### Adding a new component

Create a `.md` file in `components/` with:

```yaml
---
name: my-component
category: component
description: What it does and when to use it.
---
```

Then add `## Usage`, `## HTML`, and `## CSS` sections. Commit and push — it's immediately available for future decks.

## Layouts

Slide-level patterns that combine components into complete slide structures.

| Layout | Description |
|--------|-------------|
| `title-slide` | Opening slide with title, meta, auto-calculated stats |
| `section-divider` | Large-text transition between major topics |
| `content-slide` | Standard workhorse (2-column preferred) |
| `code-slide` | Full-width code-focused slide |
| `comparison-slide` | Side-by-side comparison layout |
| `resources-slide` | Categorized links for references/further reading |
| `basement-slide` | Vertical (down) slides for deeper dives beneath a main slide |
| `split-slide` | 50/50 split — one half visual (color/image), one half content |
| `closing-slide` | Final slide with CTA, contact info, links, optional QR code |

## Effects and advanced features

Reveal.js has powerful features beyond static slides. Some are used automatically; others are available on request.

### Automatic (Claude decides)

These are applied where they clearly help — you don't need to ask:

| Effect | What it does | When Claude uses it |
|--------|-------------|---------------------|
| **Fragments** | Reveals list items one at a time on click | Dense slides with 5+ bullets |
| **Auto-animate** | Smooth morph between two related slides | Slides that build on each other (growing code, expanding lists) |
| **r-fit-text** | Auto-scales text to fill slide width | Section dividers and single-phrase impact slides |

### On request

Ask for these in your outline notes or during iteration:

| Effect | How to request | Example |
|--------|---------------|---------|
| **Image background** | "fullscreen image on {005}" | Full-bleed photo behind slide content |
| **GIF background** | "fullscreen gif on {007}" | Animated GIF as slide background |
| **Video background** | "video background on {003}" | Auto-playing muted video behind content |
| **iframe background** | "embed this URL as an iframe on {010}" | Live webpage as the slide |
| **Parallax** | "add parallax scrolling" | Subtle depth effect as slides change (global) |
| **Transition override** | "zoom into {008}" or "hard cut to {012}" | Per-slide transition style |
| **Background transition** | "zoom the background on {006}" | Animate just the background independently |
| **Live terminal** | "embed a terminal on {005}" | Interactive terminal via ttyd — advanced, [see setup](#live-terminal-slides) |

**Transitions available:** `fade` (default), `slide`, `convex`, `concave`, `zoom`, `none`

**Fragment styles available:** `fade-in` (default), `fade-up`, `fade-down`, `fade-left`, `fade-right`, `highlight-current-blue`, `semi-fade-out`

You can also note these inline in your outline:

```markdown
## The Big Reveal

[fullscreen gif: https://example.com/mind-blown.gif]

This changes everything.

## Live Demo

[iframe: https://my-app.example.com]
```

For the full list of Reveal.js features, see the [official demo](https://revealjs.com/) and [documentation](https://revealjs.com/markup/).

## Images and visuals

### SVG diagrams (auto-generated)

Claude proactively generates inline SVG graphics when a concept benefits from a visual. You don't need to ask — but you can request them explicitly in your outline:

```markdown
## Deploy Pipeline
[diagram: flow from commit to production]

## Drupal Architecture
[diagram: layered stack — theme, logic, data, database]

## Test Coverage
[chart: donut showing 70/20/10 split]
```

Available diagram styles: architecture stacks, network/node diagrams, bar charts, donut charts, funnels, Venn diagrams, gauges, shield/security icons, gear/config icons, and abstract decorative patterns. All rendered in theme colors.

### Photos and background images

Claude adds relevant photos on ~20-30% of slides during generation (section openers, quotes, comparisons). You can also request them in your outline or during iteration using **named image patterns**:

| Pattern | What you get | How to request |
|---------|-------------|----------------|
| `backdrop` | Full-bleed photo behind content, low opacity | "add a backdrop to {005}" |
| `hero` | Photo dominates the slide, minimal text overlay | "make {003} a hero image" |
| `split-image` | 50/50 — photo on one side, content on the other | "split-image on {007}" |
| `inline-image` | Photo beside text in a two-column layout | "add an inline image to {004}" |
| `image-grid` | 2-3 photos in a row with captions | "image-grid on {008}" |
| `screenshot` | Photo in a browser frame (macOS chrome) | "add a screenshot to {006}" |
| `before-after` | Two labeled images side by side | "before-after on {009}" |
| `backdrop-quote` | Background photo behind a pull quote | "backdrop-quote on {010}" |

**In your outline:**
```markdown
## The Team
[split-image: dark office with developers]

## Our Stack
[screenshot: the Drupal admin dashboard]

## Why It Matters
[backdrop: moody server room photo]

## Before and After
[before-after: messy desk vs clean modern setup]
```

**Image sources:**
- **Unsplash** — Claude uses free stock photos via direct URL. No account needed, no attribution required.
- **Local files** — place in an `images/` folder in your deck directory
- **Any URL** — provide a direct image link

### Video embedding

Claude embeds video when you provide a URL or ask for it. All video patterns are on-request only.

| Pattern | What you get | How to request |
|---------|-------------|----------------|
| `video-bg` | Looping muted video behind content, low opacity | "video background on {003}" |
| `video-hero` | Video dominates the slide, text in overlay box | "make {005} a video hero" |
| `video-embed` | YouTube/Vimeo player centered with controls | "embed this YouTube video on {004}" |
| `video-split` | 50/50 — video on one side, content on the other | "video-split on {007}" |
| `video-frame` | Video in browser-frame chrome | "video-frame on {006}" |

**In your outline:**
```markdown
## Product Demo
[video: https://www.youtube.com/watch?v=VIDEO_ID]

## The Vibe
[video-bg: https://cdn.example.com/loop.mp4]
```

**Video sources:** YouTube and Vimeo embeds work reliably (both allow iframe embedding). For background loops, use direct MP4 URLs from free stock video sites (Coverr, Pexels) or local files in a `videos/` folder.

**Screenshots** get a browser-frame treatment (macOS-style dots + URL bar) — recommended over iframes for external websites that block embedding.

### Iframe limitations

Most production websites block iframe embedding via security headers. **Iframe slides are primarily useful for localhost demos** — your dev server, ttyd terminals, or local apps. For external sites, use a screenshot with a link instead.

## Motif system

Each theme defines a **motif** — a repeating visual icon that appears on every slide as a brand signature. For `electric-dark`, the motif is the lightning bolt.

- A large, ghosted motif appears in the background of every content slide
- Smaller motifs appear inline with some headings
- Colors alternate between the theme's accent colors (cyan and amber)

The motif is automatic — Claude places it on every slide during generation. You can override the icon during the interview ("use a rocket instead of the bolt").

## Tips for good results

### Write a good outline

- **One `##` heading per slide idea** — Claude will split or merge as needed
- **Use `###` for deeper dives** — sub-headings become basement (vertical) slides below their parent
- **Include raw notes** — don't worry about length; too much is better than too little
- **Note special requests inline** — "show this as a comparison", "include a diagram here"
- **Request diagrams** — Claude generates inline SVG graphics automatically where they fit, but you can also request them explicitly:
  - `[diagram: layered architecture]`
  - `[chart: bar chart comparing X, Y, Z]`
  - `[diagram: funnel from raw notes to polished deck]`
  - `[chart: donut showing 70/20/10 split]`
  - `[diagram: Venn — dev tools vs ops tools]`
- **Mark what matters** — bold or emphasize key points you don't want lost in condensing

```markdown
## Main Topic              <-- horizontal slide
Core points here.

### Detailed Example        <-- basement slide (navigate down)
Extended walkthrough...

### Reference Commands      <-- second basement slide
More detail...

## Next Topic              <-- back to horizontal flow
```

Claude will also create basement slides on its own when content warrants a deeper dive but would slow the main flow. Basement slides use letter suffixes: `{003a}`, `{003b}`.

### During the interview

- **Be specific about audience** — "developers who know Git but not CI/CD" is better than "technical audience"
- **State the tone** — casual team talk vs. conference presentation changes how Claude writes
- **Flag tricky slides** — if you know slide 5 is too long, say so up front

### During iteration

- **Use slugs** — `{003}` is faster and more precise than "the third slide"
- **Be direct** — "tighten {003}" works better than "can you maybe make slide 3 a bit shorter?"
- **Request component swaps** — "switch {007} from bullets to a `flow` diagram"
- **Make it more visual** — "replace the bullets on {004} with an `icon-grid`", "add a diagram to {005}", "convert {008} to a `step-list`"
- **Ask for additions** — "add a `callout` to {004} with the key takeaway"
- **Request effects** — "fullscreen gif on {005}", "auto-animate {003} to {004}", "add fragments to {006}", "embed this URL as an iframe on {010}"
- **Add images** — use pattern names: "add a `backdrop` to {003}", "`screenshot` on {007}", "`split-image` on {004}", "`hero` on {002}"
- **Move slides vertically** — "move {005} to a basement slide under {004}" or "promote {004a} to the main flow"
- **Browse the showcase** — open `examples/showcase.html` to see every component and pattern with live examples and tips

### Previewing

Every deck includes a `serve.sh` launch script. From your deck directory:

```bash
./serve.sh         # starts server on port 8765
./serve.sh 8766    # or pick a different port
```

The script runs pre-flight checks before starting:
- Verifies `index.html` exists
- Checks if the port is available
- If the deck has live terminal slides, checks that [ttyd](https://github.com/tsl0922/ttyd) is installed and running — and tells you exactly what to do if it isn't

You can also say "spin it up" and Claude will run it for you.

**Requirements:** Python 3 (pre-installed on macOS and Linux). No other dependencies.

### Live terminal slides

> **Advanced feature.** Terminal slides require installing `ttyd`, a separate
> tool that serves a terminal over HTTP. If you don't need live terminal demos,
> skip this section — everything else works without it. If ttyd isn't running
> when you hit a terminal slide, you'll see a blank frame; the rest of the deck
> is unaffected.

To add a terminal slide, ask Claude: "embed a terminal on {005}".

**Install ttyd (one-time):**
```bash
# Ubuntu/Debian
sudo apt install ttyd

# macOS
brew install ttyd
```

**Start before presenting** (the `-W` flag is required — ttyd is read-only by default):
```bash
# Blank terminal
ttyd -W -p 7681 bash &

# Open to a specific directory
ttyd -W -p 7681 bash -c "cd ~/projects/mysite && exec bash" &

# Open a file in an editor
ttyd -W -p 7681 vim /path/to/settings.php &

# Run a command, then stay in the shell
ttyd -W -p 7681 bash -c "drush status; exec bash" &
```

Use different ports for different terminal slides. Kill all after presenting: `pkill ttyd`

`serve.sh` will detect terminal slides and warn you if ttyd isn't installed or running.

## Exporting and sharing

### Markdown export

Ask Claude to export the finished deck as a readable markdown document:

```
export this deck as markdown
```

This generates a clean `.md` file with all slide content, speaker notes as blockquotes, and component markup converted to markdown equivalents (panels become blockquotes, code blocks stay code blocks, etc.). Useful for sharing content without the presentation format, archiving, or as a handout.

### PDF export

Add `?print-pdf` to the URL and print from the browser:

```
http://localhost:8765/?print-pdf
```

Use Chrome/Chromium for best results. Set to landscape, no margins, and enable background graphics.

### Sharing without a server

Since decks are self-contained `index.html` files, you can:
- Drop the file into any static hosting (GitHub Pages, Netlify, S3)
- Email the HTML file directly — it opens in any browser
- Commit it to a repo and share the raw URL

## Decks are standalone

Once generated, a deck is a self-contained `index.html` that doesn't depend on this toolkit at runtime. New components added to the toolkit won't affect existing decks — they're only available for future builds.

## License

MIT
