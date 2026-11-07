# SVG Generation Conventions

Standards for generating SVG slides in the PowerPoint Business skill. All SVG output must comply with these rules.

## Canvas

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
```

- viewBox: `0 0 1280 720` (fixed, never change)
- Safe area: 60px inset on all sides (usable region: 60,60 to 1220,660)
- Only `full_bleed` backgrounds may extend to the canvas edge

## Element ID Format

Pattern: `s{nn}-{role}-{index}`

- `nn` — 2-digit slide number (01-99)
- `role` — semantic role of the element
- `index` — 1-based counter within the role on that slide

| Role       | Used for                              | Example           |
|------------|---------------------------------------|-------------------|
| `title`    | Slide title text                      | `s03-title-1`     |
| `subtitle` | Subtitle / tagline                    | `s01-subtitle-1`  |
| `card`     | Bento grid card container (`<g>`)     | `s05-card-1`      |
| `stat`     | Statistic / KPI number                | `s07-stat-1`      |
| `chart`    | Chart container                       | `s08-chart-1`     |
| `bullet`   | Bullet list container                 | `s04-bullet-1`    |
| `image`    | Image placeholder or embedded image   | `s06-image-1`     |
| `icon`     | Icon element                          | `s03-icon-1`      |
| `bg`       | Background element                    | `s01-bg-1`        |
| `label`    | Axis label, annotation, footnote      | `s08-label-1`     |
| `connector`| Arrow, line, timeline bar             | `s09-connector-1` |

All IDs must be unique across the entire SVG document.

## Font Stack

```css
font-family: "Helvetica Neue", Arial, "PingFang SC", "Noto Sans SC", sans-serif;
```

Apply this stack to every text element. Never use serif fonts unless the theme explicitly requires it.

## Text Rendering Strategy

### Single-line text: use `<text>`

Titles, stat numbers, axis labels, captions — anything that fits on one line.

```xml
<text id="s03-title-1"
      x="60" y="95"
      font-family="Helvetica Neue, Arial, PingFang SC, Noto Sans SC, sans-serif"
      font-size="36" font-weight="700"
      fill="#1A1A2E">
  Quarterly Revenue Growth
</text>
```

For centered text, add `text-anchor="middle"` and set `x` to the horizontal center.

### Multi-line text: use `<foreignObject>` + HTML

Card body text, bullet lists, paragraphs — anything that wraps or has internal structure.

```xml
<foreignObject id="s05-bullet-1" x="80" y="150" width="500" height="400">
  <div xmlns="http://www.w3.org/1999/xhtml"
       style="font-family: Helvetica Neue, Arial, PingFang SC, Noto Sans SC, sans-serif;
              font-size: 18px; line-height: 1.6; color: #4A5568;">
    <ul style="margin: 0; padding-left: 20px;">
      <li>Market expansion into Southeast Asia</li>
      <li>Customer retention improved to 94%</li>
      <li>New product line launching Q3</li>
    </ul>
  </div>
</foreignObject>
```

**Rules for `<foreignObject>`:**
- Always include `xmlns="http://www.w3.org/1999/xhtml"` on the root HTML element.
- Set explicit `width` and `height` on the `<foreignObject>` tag.
- Use inline styles only (no `<style>` blocks inside foreignObject).
- Never nest `<svg>` inside `<foreignObject>`.

### Stat number with label

```xml
<g id="s07-stat-1">
  <text x="350" y="300"
        font-family="Helvetica Neue, Arial, PingFang SC, Noto Sans SC, sans-serif"
        font-size="56" font-weight="700" text-anchor="middle"
        fill="#1E3A5F">
    $4.2M
  </text>
  <text x="350" y="340"
        font-family="Helvetica Neue, Arial, PingFang SC, Noto Sans SC, sans-serif"
        font-size="16" text-anchor="middle"
        fill="#8896A6">
    Annual Revenue
  </text>
</g>
```

## Chart Rendering

### Simple charts: inline SVG

Render bar charts, pie charts, and line charts as native SVG elements. This keeps output self-contained and avoids external dependencies.

**Bar chart example:**

```xml
<g id="s08-chart-1" transform="translate(100, 180)">
  <!-- Y axis -->
  <line x1="0" y1="0" x2="0" y2="350" stroke="#D0D0D0" stroke-width="1"/>
  <!-- X axis -->
  <line x1="0" y1="350" x2="900" y2="350" stroke="#D0D0D0" stroke-width="1"/>
  <!-- Bars -->
  <rect x="60"  y="150" width="80" height="200" rx="4" fill="#1E3A5F"/>
  <rect x="220" y="100" width="80" height="250" rx="4" fill="#4A7FB5"/>
  <rect x="380" y="50"  width="80" height="300" rx="4" fill="#E8A838"/>
  <rect x="540" y="180" width="80" height="170" rx="4" fill="#2ECC71"/>
  <!-- Labels -->
  <text x="100" y="380" text-anchor="middle" font-size="14" fill="#4A5568">Q1</text>
  <text x="260" y="380" text-anchor="middle" font-size="14" fill="#4A5568">Q2</text>
  <text x="420" y="380" text-anchor="middle" font-size="14" fill="#4A5568">Q3</text>
  <text x="580" y="380" text-anchor="middle" font-size="14" fill="#4A5568">Q4</text>
  <!-- Value labels on bars -->
  <text x="100" y="140" text-anchor="middle" font-size="13" font-weight="600" fill="#1E3A5F">$2.0M</text>
  <text x="260" y="90"  text-anchor="middle" font-size="13" font-weight="600" fill="#4A7FB5">$2.5M</text>
  <text x="420" y="40"  text-anchor="middle" font-size="13" font-weight="600" fill="#E8A838">$3.0M</text>
  <text x="580" y="170" text-anchor="middle" font-size="13" font-weight="600" fill="#2ECC71">$1.7M</text>
</g>
```

**Donut / pie chart example (using stroke-dasharray):**

```xml
<g id="s08-chart-2" transform="translate(640, 360)">
  <!-- Background ring -->
  <circle cx="0" cy="0" r="120" fill="none" stroke="#EDF2F7" stroke-width="40"/>
  <!-- Segment 1: 45% (circumference = 2*pi*120 ≈ 754) -->
  <circle cx="0" cy="0" r="120" fill="none"
          stroke="#1E3A5F" stroke-width="40"
          stroke-dasharray="339.3 414.7"
          stroke-dashoffset="188.5"
          transform="rotate(-90)"/>
  <!-- Segment 2: 30% -->
  <circle cx="0" cy="0" r="120" fill="none"
          stroke="#4A7FB5" stroke-width="40"
          stroke-dasharray="226.2 527.8"
          stroke-dashoffset="-150.8"
          transform="rotate(-90)"/>
  <!-- Segment 3: 25% -->
  <circle cx="0" cy="0" r="120" fill="none"
          stroke="#E8A838" stroke-width="40"
          stroke-dasharray="188.5 565.5"
          stroke-dashoffset="-377.0"
          transform="rotate(-90)"/>
  <!-- Center label -->
  <text x="0" y="8" text-anchor="middle" font-size="28" font-weight="700" fill="#1A1A2E">$4.2M</text>
</g>
```

**Line chart example:**

```xml
<g id="s08-chart-3" transform="translate(100, 150)">
  <!-- Grid lines -->
  <line x1="0" y1="0"   x2="900" y2="0"   stroke="#EDF2F7" stroke-width="1"/>
  <line x1="0" y1="100" x2="900" y2="100" stroke="#EDF2F7" stroke-width="1"/>
  <line x1="0" y1="200" x2="900" y2="200" stroke="#EDF2F7" stroke-width="1"/>
  <line x1="0" y1="300" x2="900" y2="300" stroke="#D0D0D0" stroke-width="1"/>
  <!-- Line -->
  <polyline points="0,250 180,200 360,120 540,160 720,60 900,80"
            fill="none" stroke="#1E3A5F" stroke-width="3" stroke-linejoin="round"/>
  <!-- Data points -->
  <circle cx="0"   cy="250" r="5" fill="#1E3A5F"/>
  <circle cx="180" cy="200" r="5" fill="#1E3A5F"/>
  <circle cx="360" cy="120" r="5" fill="#1E3A5F"/>
  <circle cx="540" cy="160" r="5" fill="#1E3A5F"/>
  <circle cx="720" cy="60"  r="5" fill="#1E3A5F"/>
  <circle cx="900" cy="80"  r="5" fill="#1E3A5F"/>
</g>
```

### Complex charts: matplotlib SVG

When a chart is too complex for hand-written SVG (scatter with regression, heatmaps, advanced statistical plots), generate it with matplotlib, export as SVG, and inline the `<g>` content:

```python
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 5))
# ... plot ...
fig.savefig('chart.svg', format='svg', transparent=True, bbox_inches='tight')
```

Then extract the inner `<g>` from the matplotlib SVG and embed it with a `transform` to position it on the slide canvas.

## Draft Neutral Palette

Before theme injection, all slides use this neutral palette for structure validation:

| Role          | Color     | Usage                           |
|---------------|-----------|---------------------------------|
| Background    | `#F5F5F5` | Slide background                |
| Card fill     | `#FFFFFF` | Card body                       |
| Border        | `#D0D0D0` | Card borders, axis lines        |
| Text primary  | `#333333` | Headings, body text             |
| Text secondary| `#666666` | Subtitles, descriptions         |
| Accent        | `#888888` | Placeholder for theme accent    |

## Theme Injection Rules

When applying a theme from `themes.yaml`, replace draft colors according to this mapping:

| SVG element                   | Theme token          |
|-------------------------------|----------------------|
| Slide background `<rect>`     | `background`         |
| Card fill `<rect>`            | `card_bg`            |
| Card border stroke            | `card_style.border_color` |
| Card border-radius            | `card_style.border_radius` |
| Card shadow `<filter>`        | `card_style.shadow.*`|
| Title `<text>` fill           | `text_primary`       |
| Body text fill                | `text_secondary`     |
| Muted / caption fill          | `text_muted`         |
| Accent elements (bars, lines) | `accent`             |
| Chart data series              | `chart_colors[0..5]` |
| Cover slide background        | `slide_overrides.cover.background` |
| Cover slide text               | `slide_overrides.cover.text_color` |
| Section divider background     | `slide_overrides.section_divider.background` |
| Section divider text           | `slide_overrides.section_divider.text_color` |
| Gradient fills                 | `gradients.*` (see below) |

## SVG `<defs>` Section

Place all reusable definitions at the top of the SVG, immediately after the opening `<svg>` tag.

### Gradients

```xml
<defs>
  <!-- Linear gradient from theme -->
  <linearGradient id="grad-cover" x1="0%" y1="0%" x2="100%" y2="100%">
    <!-- angle approximated via x1/y1/x2/y2; 135deg ≈ x1=0%,y1=0%,x2=100%,y2=100% -->
    <stop offset="0%"   stop-color="#1E3A5F"/>
    <stop offset="60%"  stop-color="#2A5080"/>
    <stop offset="100%" stop-color="#4A7FB5"/>
  </linearGradient>
</defs>
```

Angle-to-coordinate mapping for `linearGradient`:

| Angle | x1  | y1  | x2   | y2   |
|-------|-----|-----|------|------|
| 0     | 0%  | 100%| 0%   | 0%   |
| 90    | 0%  | 0%  | 100% | 0%   |
| 135   | 0%  | 0%  | 100% | 100% |
| 180   | 0%  | 0%  | 0%   | 100% |

### Shadows (drop shadow filter)

```xml
<defs>
  <filter id="shadow-card" x="-5%" y="-5%" width="110%" height="115%">
    <feDropShadow dx="0" dy="2" stdDeviation="6"
                  flood-color="#1E3A5F" flood-opacity="0.08"/>
  </filter>
</defs>

<!-- Usage -->
<rect x="60" y="60" width="570" height="290" rx="8"
      fill="#F7F9FC" stroke="#E2E8F0" stroke-width="1"
      filter="url(#shadow-card)"/>
```

Map theme `card_style.shadow` fields: `blur` -> `stdDeviation`, `offset_y` -> `dy`, `color` -> `flood-color` (add #), `opacity` -> `flood-opacity`.

### Patterns (decoration)

```xml
<defs>
  <!-- Dot pattern for warm_earth theme -->
  <pattern id="pat-dots" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
    <circle cx="10" cy="10" r="1.5" fill="#6B4C3B" opacity="0.06"/>
  </pattern>

  <!-- Grid pattern for tech_dark theme -->
  <pattern id="pat-grid" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
    <line x1="40" y1="0" x2="40" y2="40" stroke="#2A3A4A" stroke-width="0.5"/>
    <line x1="0" y1="40" x2="40" y2="40" stroke="#2A3A4A" stroke-width="0.5"/>
  </pattern>
</defs>

<!-- Apply as background overlay -->
<rect x="0" y="0" width="1280" height="720" fill="url(#pat-grid)"/>
```

## Visual Richness: Multi-Layer Background Stack

Every content slide MUST have at least 4 background layers. This is the single biggest factor that separates professional slides from sparse ones.

### Layer Stack (bottom to top)

```
Layer 1: Base gradient      — linearGradient, fills entire canvas
Layer 2: Grain texture      — <pattern> with tiny circles, 6-8% opacity
Layer 3: Grid or dots       — <pattern> with lines/dots, 3-5% opacity
Layer 4: Radial glow spots  — 2-3 radialGradient circles at corners/edges, 8-15% opacity
Layer 5: Decorative curves  — 1-2 Bezier <path> strokes with gradient, 5-15% opacity
```

### Layer 1: Base Gradient

Never use a flat solid color. Always use a multi-stop gradient:

```xml
<defs>
  <linearGradient id="s03-bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#0F1419"/>
    <stop offset="50%" stop-color="#141E2A"/>
    <stop offset="100%" stop-color="#1A2840"/>
  </linearGradient>
</defs>
<rect id="s03-bg-01" x="0" y="0" width="1280" height="720" fill="url(#s03-bg-grad)"/>
```

### Layer 2: Grain Texture

Adds subtle paper-like texture. Creates visual depth:

```xml
<defs>
  <pattern id="s03-grain" x="0" y="0" width="4" height="4" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="0.5" fill="#FFFFFF"/>
  </pattern>
</defs>
<rect id="s03-bg-02" x="0" y="0" width="1280" height="720" fill="url(#s03-grain)" opacity="0.06"/>
```

### Layer 3: Grid Pattern

Subtle reference grid creates "technical/blueprint" feel:

```xml
<defs>
  <pattern id="s03-grid" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
    <line x1="40" y1="0" x2="40" y2="40" stroke="#FFFFFF" stroke-width="0.5" opacity="0.04"/>
    <line x1="0" y1="40" x2="40" y2="40" stroke="#FFFFFF" stroke-width="0.04" opacity="0.04"/>
  </pattern>
</defs>
<rect id="s03-bg-03" x="0" y="0" width="1280" height="720" fill="url(#s03-grid)"/>
```

### Layer 4: Radial Glow Spots

Colored light pools at 2-3 corners. Creates atmospheric depth:

```xml
<defs>
  <radialGradient id="s03-glow-tl" cx="15%" cy="20%" r="40%">
    <stop offset="0%" stop-color="#00D4FF" stop-opacity="0.12"/>
    <stop offset="100%" stop-color="#00D4FF" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="s03-glow-br" cx="85%" cy="80%" r="35%">
    <stop offset="0%" stop-color="#8B5CF6" stop-opacity="0.08"/>
    <stop offset="100%" stop-color="#8B5CF6" stop-opacity="0"/>
  </radialGradient>
</defs>
<rect id="s03-bg-04" x="0" y="0" width="1280" height="720" fill="url(#s03-glow-tl)"/>
<rect id="s03-bg-05" x="0" y="0" width="1280" height="720" fill="url(#s03-glow-br)"/>
```

### Layer 5: Decorative Bezier Curves

1-2 sweeping arcs with gradient stroke. Adds dynamic energy:

```xml
<defs>
  <linearGradient id="s03-curve-grad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#00D4FF" stop-opacity="0.15"/>
    <stop offset="50%" stop-color="#8B5CF6" stop-opacity="0.08"/>
    <stop offset="100%" stop-color="#00D4FF" stop-opacity="0"/>
  </linearGradient>
</defs>
<!-- Wide arc -->
<path id="s03-deco-01" d="M-100,500 C200,200 600,100 1380,300"
      fill="none" stroke="url(#s03-curve-grad)" stroke-width="120" opacity="0.5"/>
<!-- Thin accent arc -->
<path id="s03-deco-02" d="M-50,520 C220,220 620,120 1400,320"
      fill="none" stroke="url(#s03-curve-grad)" stroke-width="2" opacity="0.3"/>
```

### Cover/End Slides

Cover and end slides add 2 more layers:
- **Geometric decorations**: diagonal lines (white, 3-4% opacity, stroke-width 60-120)
- **Accent bar**: gradient-filled thin rectangle below title

---

## Three-Level Elevation System

Cards use elevation to establish Z-axis hierarchy. Hero/focus cards float higher:

```xml
<defs>
  <!-- Level 1: Subtle — supporting cards -->
  <filter id="s03-shadow-sm" x="-3%" y="-3%" width="106%" height="110%">
    <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#000000" flood-opacity="0.12"/>
  </filter>

  <!-- Level 2: Medium — standard cards (default) -->
  <filter id="s03-shadow-md" x="-5%" y="-5%" width="110%" height="118%">
    <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="0.20"/>
  </filter>

  <!-- Level 3: Heavy — hero/focus cards, floating panels -->
  <filter id="s03-shadow-lg" x="-8%" y="-8%" width="116%" height="128%">
    <feDropShadow dx="0" dy="16" stdDeviation="24" flood-color="#000000" flood-opacity="0.28"/>
  </filter>
</defs>
```

Usage rule: each slide should have mixed elevation — not all cards at the same level.

---

## Card Visual Depth

Cards must have 3 simultaneous visual properties:

1. **Gradient fill** — semi-transparent dual-color gradient, not flat solid:
```xml
<defs>
  <linearGradient id="s03-card-fill" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#1A2332" stop-opacity="0.96"/>
    <stop offset="100%" stop-color="#1E2A3C" stop-opacity="0.92"/>
  </linearGradient>
</defs>
```

2. **Fine border** — 1px stroke with theme border color
3. **Elevation shadow** — shadow-md or shadow-lg from the elevation system
4. **Large border-radius** — rx="20" to "28" for modern feel (not rx="8")

Combined:
```xml
<rect id="s03-card-01" x="60" y="130" width="570" height="400"
      rx="24" fill="url(#s03-card-fill)"
      stroke="#2A3A4A" stroke-width="1"
      filter="url(#s03-shadow-md)"/>
```

---

## Pill Badge (Tag Component)

Small rounded-rectangle labels for classification, status, and feature tags. Essential for information density:

```xml
<!-- Single pill badge -->
<g id="s05-badge-01" transform="translate(80, 140)">
  <rect width="140" height="28" rx="14" fill="#0C1B2E" stroke="#2A3A4A" stroke-width="1"/>
  <text x="70" y="19" text-anchor="middle"
        font-family="Helvetica Neue, Arial, PingFang SC, Noto Sans SC, sans-serif"
        font-size="13" fill="#00D4FF">
    Agent 编排
  </text>
</g>
```

Badge variations:
- **Accent badge**: `fill="none" stroke="#00D4FF"` — outlined, for category tags
- **Solid badge**: `fill="#00D4FF" stroke="none"`, text white — for highlights
- **Subtle badge**: `fill="#1A2332" stroke="#2A3A4A"` — for secondary info
- **Status badge**: add a 6px circle before text for status indicators

Use 3-8 badges per content slide. Group them in rows or scatter within cards.

---

## Data Visualization Components

### Big Number + Delta

```xml
<g id="s05-stat-01">
  <text x="300" y="250" text-anchor="middle" font-size="64" font-weight="700" fill="#00D4FF">$52.6B</text>
  <text x="300" y="285" text-anchor="middle" font-size="16" fill="#8899AA">2030 年 AI Agent 市场规模</text>
  <!-- Delta indicator -->
  <g transform="translate(380, 232)">
    <polygon points="0,8 5,0 10,8" fill="#10B981"/>
    <text x="14" y="8" font-size="14" font-weight="600" fill="#10B981">46.3%</text>
  </g>
</g>
```

### Progress Bar

```xml
<g id="s07-progress-01" transform="translate(100, 300)">
  <text x="0" y="-8" font-size="14" fill="#E8ECF1">RAG 准确率</text>
  <rect x="0" y="0" width="400" height="8" rx="4" fill="#1A2332"/>
  <rect x="0" y="0" width="340" height="8" rx="4" fill="url(#accent-grad)"/>
  <text x="410" y="8" font-size="14" font-weight="600" fill="#00D4FF">85%</text>
</g>
```

### Sparkline (mini line chart)

```xml
<g id="s07-spark-01" transform="translate(100, 350)">
  <polyline points="0,30 20,25 40,28 60,15 80,18 100,5"
            fill="none" stroke="#00D4FF" stroke-width="2" stroke-linejoin="round"/>
  <circle cx="100" cy="5" r="3" fill="#00D4FF"/>
</g>
```

### Icon Circles

For feature icons, use bordered circles with Unicode symbols:

```xml
<g id="s06-icon-01" transform="translate(100, 160)">
  <circle cx="24" cy="24" r="24" fill="none" stroke="#00D4FF" stroke-width="1.5"/>
  <text x="24" y="30" text-anchor="middle" font-size="20" fill="#00D4FF">⟐</text>
</g>
```

---

## Footer Information Bar

Every content slide (not cover/end) should have a footer bar:

```xml
<!-- Footer separator -->
<line id="s03-footer-line" x1="60" y1="650" x2="1220" y2="650" stroke="#2A3A4A" stroke-width="1"/>
<!-- Footer content -->
<text id="s03-footer-source" x="80" y="672" font-size="12" fill="#556677">
  Source: MarketsandMarkets, 2025 | Confidential
</text>
<text id="s03-footer-page" x="1200" y="672" text-anchor="end" font-size="12" fill="#556677">
  03 / 16
</text>
```

---

## Minimum Visual Density Requirements

| Slide type | Min visual components | Examples of what counts |
|---|---|---|
| Cover / End | 6+ | gradient bg, grain, glow spots, curves, title, accent bar, footer line |
| Content slide | 8+ | bg layers, title bar, 2+ cards, badges, stat numbers, charts, footer |
| Data slide | 10+ | bg layers, title bar, stat cards, charts, progress bars, badges, source |
| Section divider | 5+ | gradient bg, glow, title, subtitle, accent element |

"Empty space" should be **intentional breathing room**, not absence of design. Even negative space should sit atop a multi-layer background.

---

## CJK Typography Rules

1. **Full-width punctuation** — Chinese punctuation (，。！？：；""''【】) must remain full-width. Never replace with half-width equivalents.
2. **Number-CJK spacing** — Insert a thin space (U+2009 or CSS `margin: 0 2px`) between adjacent Latin/number characters and CJK characters. Example: `增长 42%` not `增长42%`.
3. **Line height** — CJK-heavy text needs `line-height: 1.7` minimum (vs 1.5 for Latin). Set on the `<div>` inside `<foreignObject>`.
4. **No justification** — Use `text-align: left` for CJK body text. Justified CJK text creates uneven spacing between characters.
5. **Font size floor** — CJK characters below 12px become illegible on projected slides. Minimum font size for any CJK text is 12px.
6. **Mixed-script alignment** — When CJK and Latin text appear on the same line, use `vertical-align: baseline`. The font stack (PingFang SC after Helvetica Neue) ensures consistent baseline alignment.
7. **Line width capacity** — CJK characters are ~1.8x wider than Latin at same font-size. Latin capacity: `card_width / (font_size * 0.6)` chars/line. CJK capacity: `card_width / (font_size * 1.1)` chars/line.
8. **Emphasis by bold, not italic** — CJK italic rendering is typographically poor. Use `font-weight: bold` for emphasis, never `font-style: italic`.
9. **Punctuation kerning** — No line should start with closing punctuation (。、」』）】) or end with opening punctuation (「『（【).

---

## Dynamic Font Sizing

Instead of fixed sizes, calculate based on content length:

### Slide Title
```
font_size = clamp(28, 44 - (char_count - 15) * 0.5, 44)
```

### Card Title
```
font_size = clamp(18, 32 - (char_count - 20) * 0.7, 32)
```

### CJK Adjustment
For text with >30% CJK characters, multiply `char_count` by 1.8 before applying the formula.

### Examples
| Text | Chars | Effective | Result |
|------|-------|-----------|--------|
| "Q3 Revenue" | 10 | 10 | 44px (max) |
| "综合分析供应链中断影响" | 10 CJK | 18 | 43px |
| "Comprehensive Analysis of Global Supply Chain Disruptions" | 58 | 58 | 28px (min) |

---

## Text Overflow Strategy

SVG does not auto-wrap or auto-shrink. Prevent overflow with this cascade:

1. **Shrink**: Reduce font-size in 2px steps. Floor: **14px** body, **18px** card title.
2. **Truncate**: At floor, truncate with "..." if still overflowing.
3. **Split**: If content exceeds any single card's capacity, split into multiple cards.

### Line Capacity Estimation
```
Latin lines per card:  chars_per_line = card_width / (font_size * 0.6)
CJK lines per card:   chars_per_line = card_width / (font_size * 1.1)
Max lines:            (card_height - 80) / (font_size * line_height_factor)
  line_height_factor: 1.4 Latin, 1.7 CJK
```

---

## Three-Tier Information Hierarchy

Every slide must have exactly three distinguishable visual tiers. See `references/cognitive-design.md` for the evidence base.

| Tier | Role | Font Size | Opacity | Whitespace |
|------|------|-----------|---------|------------|
| **Primary** | Title, hero number, key message | 36-72px | 1.0 | Generous (20px+) |
| **Secondary** | Supporting data, subheads, card titles | 18-24px | 0.8-1.0 | Moderate (12px) |
| **Tertiary** | Source, footnotes, page numbers, labels | 12-14px | 0.5-0.7 | Minimal |

**Rules**:
- If only 2 tiers distinguishable → hierarchy too flat → increase contrast
- Primary: only **one** element per slide. Two competing primaries = no primary.
- Tertiary elements should never draw attention first in a 3-second glance.
