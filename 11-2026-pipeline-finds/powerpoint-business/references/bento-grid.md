# Bento Grid Layout System

Flexible card-based layout system inspired by the Japanese bento box. Layout is driven by content semantics, not rigid templates.

## Canvas Specification

- SVG viewBox: `0 0 1280 720`
- Safe area: 60px inset on all sides
- Usable region: **1160 x 600** (x: 60..1220, y: 60..660)
- Coordinate origin: top-left (0,0)

## Core Principles

1. **Flexibility** — 1 to 6+ cards per slide. No fixed grid; cards are placed freely within the safe area.
2. **Hierarchy via size** — the most important card is the largest. A 2:1 area ratio implies 2:1 importance.
3. **Minimum gap** — 20px between any two cards. Never let cards touch or overlap.
4. **Rule of thirds** — align card edges to approximate third lines: x ~ 427 / 853, y ~ 240 / 480. Viewers' eyes naturally settle at intersections.
5. **Aspect ratio range** — individual cards should stay between 1:3 (tall) and 4:1 (wide). Anything outside this range feels awkward.

## Layout Strategies

### 1. single_focus

One large card fills the entire usable area. Best for: hero statements, full-slide images, key quotes.

```
┌──────────────────────────────────┐
│                                  │
│           CARD (1160×600)        │
│                                  │
└──────────────────────────────────┘
```

Dimensions: card at (60, 60) size 1160 x 600.

### 2. two_col_symmetric

Two equal-width columns. Best for: comparisons, before/after, pros/cons.

```
┌───────────────┐ ┌───────────────┐
│               │ │               │
│  LEFT (570)   │ │  RIGHT (570)  │
│               │ │               │
└───────────────┘ └───────────────┘
```

Dimensions: each card 570 x 600. Left at (60, 60), right at (650, 60). Gap: 20px.

### 3. two_col_asymmetric

62:38 split emphasizing the left card. Best for: main content + sidebar, image + description.

```
┌────────────────────┐ ┌──────────┐
│                    │ │          │
│   PRIMARY (710)    │ │ SIDE(430)│
│                    │ │          │
└────────────────────┘ └──────────┘
```

Dimensions: left 710 x 600 at (60, 60), right 430 x 600 at (790, 60). Gap: 20px.

Mirror (38:62) also valid — place primary on right when reading flow demands it.

### 4. three_column

Three equal columns. Best for: 3 features, 3 pillars, triple comparison.

```
┌──────────┐ ┌──────────┐ ┌──────────┐
│          │ │          │ │          │
│  (373)   │ │  (373)   │ │  (373)   │
│          │ │          │ │          │
└──────────┘ └──────────┘ └──────────┘
```

Dimensions: each 373 x 600. Positions: x = 60, 453, 847. Gaps: 20px each.

### 5. hero_grid

Top hero card spanning full width + 2-3 smaller cards below. Best for: headline + supporting points, overview + details.

**2 bottom cards:**
```
┌──────────────────────────────────┐
│          HERO (1160×340)         │
└──────────────────────────────────┘
┌───────────────┐ ┌───────────────┐
│  LEFT (570)   │ │  RIGHT (570)  │
└───────────────┘ └───────────────┘
```

Hero: 1160 x 340 at (60, 60). Bottom left: 570 x 240 at (60, 420). Bottom right: 570 x 240 at (650, 420). Gap: 20px.

**3 bottom cards:**
```
┌──────────────────────────────────┐
│          HERO (1160×340)         │
└──────────────────────────────────┘
┌──────────┐ ┌──────────┐ ┌──────────┐
│   (373)  │ │   (373)  │ │   (373)  │
└──────────┘ └──────────┘ └──────────┘
```

Hero: 1160 x 340 at (60, 60). Bottom cards: each 373 x 240 at y=420, x = 60, 453, 847.

### 6. mixed_grid

Free-form L-shape or T-shape layout. Best for: dashboards with one dominant metric, feature spotlights.

**L-shape example:**
```
┌────────────────────┐ ┌──────────┐
│                    │ │  B (430) │
│   A (710×600)      │ ├──────────┤
│                    │ │  C (430) │
└────────────────────┘ └──────────┘
```

A: 710 x 600 at (60, 60). B: 430 x 290 at (790, 60). C: 430 x 290 at (790, 370). Gap: 20px.

**T-shape example:**
```
┌──────────────────────────────────┐
│          TOP (1160×290)          │
└──────────────────────────────────┘
┌──────────┐ ┌──────────┐ ┌──────────┐
│   (373)  │ │   (373)  │ │   (373)  │
└──────────┘ └──────────┘ └──────────┘
```

Top: 1160 x 290 at (60, 60). Bottom: each 373 x 290 at y=370, x = 60, 453, 847.

### 7. timeline

Horizontal flow of 3-6 nodes connected by a line/arrow. Best for: process flows, project phases, history.

**4 nodes:**
```
  ●─────────●─────────●─────────●
┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐
│(260)│  │(260)│  │(260)│  │(260)│
└─────┘  └─────┘  └─────┘  └─────┘
```

Timeline bar: y = 120, x = 60..1220, stroke-width 3. Node cards: each 260 x 420 at y=180. Positions: x = 60, 340, 620, 900. Gap: 20px.

For 3 nodes: card width 360, x = 60, 440, 820. For 5 nodes: card width 204, x = 60, 284, 508, 732, 956.

### 8. dashboard

Uniform 2x2 or 2x3 grid. Best for: KPI dashboards, metric overviews, multi-stat displays.

**2x2:**
```
┌───────────────┐ ┌───────────────┐
│  TL (570×290) │ │  TR (570×290) │
├───────────────┤ ├───────────────┤
│  BL (570×290) │ │  BR (570×290) │
└───────────────┘ └───────────────┘
```

Each card 570 x 290. Top row y=60, bottom row y=370. Left x=60, right x=650. Gap: 20px.

**2x3:**
```
┌──────────┐ ┌──────────┐ ┌──────────┐
│  (373)   │ │  (373)   │ │  (373)   │
├──────────┤ ├──────────┤ ├──────────┤
│  (373)   │ │  (373)   │ │  (373)   │
└──────────┘ └──────────┘ └──────────┘
```

Each card 373 x 290. Top row y=60, bottom row y=370. Columns x = 60, 453, 847. Gap: 20px.

### 9. horizontal_split

Two horizontal bands. Best for: title + content, context + detail, image + caption.

```
┌──────────────────────────────────┐
│         TOP (1160×350)           │
└──────────────────────────────────┘
┌──────────────────────────────────┐
│        BOTTOM (1160×230)         │
└──────────────────────────────────┘
```

Top: 1160 x 350 at (60, 60). Bottom: 1160 x 230 at (60, 430). Gap: 20px.

Ratio is adjustable: 60:40, 70:30, or 50:50 (each 290 x 1160 at y=60 and y=370).

### 10. full_bleed

Full-slide background (image, gradient, or solid fill) with an overlay text area. Best for: cover slides, section dividers, impactful quotes.

```
┌──────────────────────────────────────┐
│ ┌──────────────────────────────────┐ │
│ │  BACKGROUND (1280×720)           │ │
│ │      ┌───────────────────┐       │ │
│ │      │  OVERLAY (600×300)│       │ │
│ │      └───────────────────┘       │ │
│ └──────────────────────────────────┘ │
└──────────────────────────────────────┘
```

Background: 1280 x 720 at (0, 0), no safe-area constraint. Overlay: semi-transparent card placed within safe area, size and position vary. Typical: 600 x 300 centered at (340, 210).

## Layout Selection Decision Tree

```
Content type?
├─ Single big idea / quote / hero image
│  └─ single_focus or full_bleed
├─ Two things to compare
│  └─ Equal weight? → two_col_symmetric
│  └─ One dominant? → two_col_asymmetric
├─ Three parallel items
│  └─ three_column
├─ Four parallel items (SWOT, 4 pillars)
│  └─ four_column
├─ Five brief items (risks, ratings)
│  └─ five_column
├─ One main + 2-3 supporting
│  └─ hero_grid or mixed_grid
├─ Main visual + sidebar annotations
│  └─ hero_sidebar
├─ Sequential process (3-6 steps)
│  └─ timeline
├─ Progressive narrowing / layered analysis
│  └─ waterfall
├─ 4-6 metrics / KPIs
│  └─ dashboard (2x2 or 2x3)
├─ Hierarchy / positioning analysis
│  └─ Use concentric_circles component
├─ Closed-loop / flywheel logic
│  └─ Use flywheel component
├─ Conversion / filtering stages
│  └─ Use funnel component
├─ Context + detail (narrative flow)
│  └─ horizontal_split
└─ Section transition / emotional impact
   └─ full_bleed
```

### 11. four_column

Four equal columns. Best for: 4 key points, SWOT analysis, quarterly comparison, 4-pillar frameworks.

```
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│       │ │       │ │       │ │       │
│ (272) │ │ (272) │ │ (272) │ │ (272) │
│       │ │       │ │       │ │       │
└───────┘ └───────┘ └───────┘ └───────┘
```

Dimensions: each card 272 x 600. Positions: x = 60, 352, 644, 936. Gaps: 20px each.

With title bar (y=130): each card 272 x 530 at y=130.

### 12. five_column

Five equal columns. Best for: risk lists, 5-step processes, rating scales, multiple brief items.

```
┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
│(216)│ │(216)│ │(216)│ │(216)│ │(216)│
└─────┘ └─────┘ └─────┘ └─────┘ └─────┘
```

Dimensions: each card 216 x 600. Positions: x = 60, 296, 532, 768, 1004. Gaps: 20px each.

**Note**: 5 columns = dense. Keep card content to title + 2-3 bullets max. Use numbered labels (POINT 01) for clarity.

### 13. hero_sidebar

Large hero area (70%) + narrow sidebar (30%) with 2-3 stacked items. Best for: main visual/chart + legend/annotations, feature spotlight + specs.

```
┌──────────────────────┐ ┌────────┐
│                      │ │  A     │
│   HERO (790×600)     │ ├────────┤
│                      │ │  B     │
│                      │ ├────────┤
│                      │ │  C     │
└──────────────────────┘ └────────┘
```

Hero: 790 x 600 at (60, 60). Sidebar items: each 350 x ~187 at x=870. Gap: 20px.

### 14. waterfall

Top-down cascade of 3-4 full-width cards, each progressively indented. Best for: progressive disclosure, layered analysis, funnel logic.

```
┌──────────────────────────────────┐
│          CARD 1 (1160×140)       │
└──────────────────────────────────┘
   ┌───────────────────────────────┐
   │       CARD 2 (1080×140)      │
   └───────────────────────────────┘
      ┌────────────────────────────┐
      │    CARD 3 (1000×140)       │
      └────────────────────────────┘
         ┌─────────────────────────┐
         │   CARD 4 (920×140)      │
         └─────────────────────────┘
```

Card 1: 1160×140 at (60,60). Card 2: 1080×140 at (100,220). Card 3: 1000×140 at (140,380). Card 4: 920×140 at (180,540). Each card indent +40px left, shrink -80px width.

## Page-Level Structure Components

### Section Navigation Bar (top)

Every content slide SHOULD have a navigation bar at the very top (y=0..40):

```
┌──────────────────────────────────────┐
│ BRAND · SECTION NAME           03/16 │ h=40
└──────────────────────────────────────┘
```

- Full width 1280×40
- Left: brand/project name · section name (14px muted)
- Right: page number (14px muted)
- Background: slightly darker than slide bg, or transparent
- Separator: 1px line at y=40

This replaces the old "title bar" concept. Content area starts at y=60 (nav bar + 20px gap).

### Summary Bar (bottom)

Content slides MAY include a summary bar above the footer (y=620..650):

```
┌──────────────────────────────────────┐
│  💡 Key takeaway sentence here       │ h=30
└──────────────────────────────────────┘
```

- Width: 1160, at x=60
- Background: subtle card-bg fill with low opacity, rx=8
- Content: one-sentence takeaway or "金句" in accent color
- Font: 14px, italic or semi-bold

## Numbered Label System

Use numbered labels on cards for sequential information. Applied as a badge variant:

```
POINT 01    STEP 01    RISK 01    LAYER 01    WATCH 01
```

Format: category keyword (UPPERCASE, English) + 2-digit number. Placed at top-left of card as a pill badge. Numbered labels help audiences track position in multi-card layouts (especially 4+ columns).

## Semantic Visualization Components

Beyond static card layouts, these content-driven components can replace or supplement cards:

### Concentric Circles (for hierarchy/positioning)

3-4 nested circles showing layers from core to edge:
```
        ╭───────────────╮
      ╭─│   ╭───────╮   │─╮
    ╭─│ │ ╭─│ CORE  │─╮ │ │─╮
    │ │ │ │ ╰───────╯ │ │ │ │
    │ │ │ ╰─── L2 ───╯ │ │ │
    │ │ ╰──── L3 ──────╯ │ │
    │ ╰───── L4 ─────────╯ │
    ╰────── OUTER ─────────╯
```

Use `<circle>` with increasing r, decreasing opacity. Labels at each ring.

### Flywheel / Cycle Diagram (for closed-loop logic)

4-6 nodes in a circle connected by curved arrows:
```
        ╭──→ Step 1 ──╮
        │              │
    Step 4          Step 2
        │              │
        ╰── Step 3 ←──╯
```

Use `<circle>` for nodes, `<path>` with arc commands for arrows. Center label for the cycle name.

### Funnel Diagram (for conversion/filtering)

Progressively narrowing horizontal bars:
```
┌──────────────────────────────┐  Stage 1 (100%)
└──┌──────────────────────┐──┘
   └──┌────────────────┐──┘      Stage 2 (60%)
      └──┌──────────┐──┘
         └──┌────┐──┘            Stage 3 (25%)
            └────┘
```

Use `<polygon>` or stacked `<rect>` with decreasing width. Value labels right-aligned.

## Constraints

## Information Density Targets

| Page Type | Target Info Units | Max Key Points | Notes |
|-----------|------------------|----------------|-------|
| cover / end | 2-3 | 0 | title + subtitle + visual only |
| section_divider | 1-2 | 0 | part title + subtitle |
| content | 3-5 | 3 | standard text + cards |
| data / dashboard | 4-7 | 2 | with 2-5 data visualizations |
| comparison | 4-6 | 2-3 per column | |
| timeline / process | 3-6 | 3-6 nodes | |
| quote / full_bleed | 1-2 | 0 | quote + attribution only |

Exceeding the max by >2 info units is a Major review issue. Cover/quote with >3 units is Critical.
See `references/cognitive-design.md` for the evidence base (Miller's Law).

## Card Aspect Ratio Constraints

- **Minimum**: 1:2 (width:height) — no card narrower than half its height
- **Maximum**: 4:1 (width:height) — no card wider than 4x its height
- **Recommended ratios**: 16:9, 4:3, 1:1, 3:4

Cards outside this range feel awkward and waste space.

## Content-Adaptive Sizing

| Content Volume | Adaptation |
|---------------|------------|
| Single metric | Big Number: 48-72px centered, label below |
| Short (< 30 words) | Standard: 16-20px body, 24px padding |
| Medium (30-80 words) | Reduce body to 16px, padding to 20px |
| Long (> 80 words) | Reduce body to 14px, padding to 16px |
| > 5 bullets | Split into 2-column layout within card |
| > 8 bullets | Split across two cards |

Prefer splitting over shrinking below 14px.

## Constraints

- **Never reuse the same layout strategy 3 or more consecutive slides.** Alternate between at least 2 different strategies in any 3-slide window.
- Cards must not extend outside the safe area (x: 60..1220, y: 60..660) except for full_bleed backgrounds.
- All gap calculations assume 20px minimum. Increase to 24-30px for breathing room on sparse slides.
- When a slide has a title bar (h=50, y=60..110), the card region shifts to y=130..660 (usable height = 530).
