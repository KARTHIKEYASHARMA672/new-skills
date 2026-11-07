---
name: effects
category: component
description: Reveal.js advanced features — fragments, auto-animate, background media, transitions, and more. Some used automatically by Claude, others available on request.
---

## Overview

Reveal.js has powerful built-in features beyond static slides. This component
documents what's available, what Claude should use automatically, and what
requires the user to request.

---

## Auto-use (Claude applies these by default)

### Fragments (build/reveal)

Reveal list items or content blocks incrementally. Use on slides with 4+
bullet points or when pacing matters. Don't use on every slide — only where
progressive reveal actually helps comprehension.

```html
<ul>
  <li class="fragment">First point (visible immediately)</li>
  <li class="fragment">Second point (appears on click)</li>
  <li class="fragment">Third point</li>
</ul>
```

**Fragment styles** (use sparingly):
```html
<li class="fragment fade-in">Default — fades in</li>
<li class="fragment fade-up">Slides up while fading in</li>
<li class="fragment highlight-current-blue">Highlights when current, dims after</li>
<li class="fragment semi-fade-out">Partially fades out when next appears</li>
```

**When to auto-use:** Slides with 5+ bullets, step-by-step reveals, or when
earlier points would distract from later ones. Skip on slides where seeing
everything at once is better (comparisons, reference tables).

### Auto-animate (between related slides)

Smooth morphing between two slides that share elements. Use when splitting
content across slides or showing progressive builds of a concept.

```html
<section data-auto-animate>
  <h2>Building a Skill</h2>
  <div class="codeblock">
    <pre><code>my-skill/
└── SKILL.md</code></pre>
  </div>
</section>

<section data-auto-animate>
  <h2>Building a Skill</h2>
  <div class="codeblock">
    <pre><code>my-skill/
├── SKILL.md
├── scripts/
├── references/
└── assets/</code></pre>
  </div>
</section>
```

Matching elements need the same `data-id` attribute to animate between slides:
```html
<!-- Slide 1 -->
<h2 data-id="title">Step One</h2>
<p data-id="desc">Start here.</p>

<!-- Slide 2 -->
<h2 data-id="title">Step Two</h2>
<p data-id="desc">Then do this.</p>
```

**When to auto-use:** Slides that split a growing list, code that builds up,
or a concept that evolves across 2-3 slides. Don't use between unrelated slides.

### r-fit-text

Auto-scales text to fill the slide width. **Use cautiously** — on long text
it can overflow the right edge of the viewport. Prefer fixed `font-size` on
section dividers (e.g. `style="font-size:3.5em;"`) and reserve `r-fit-text`
for very short text (1-3 words) or when combined with `max-width: 100%`.

```html
<!-- Preferred for section dividers -->
<h1 style="font-size:3.5em;">Section Title</h1>

<!-- r-fit-text only for very short text -->
<h2 class="r-fit-text" style="max-width:100%;">GO</h2>
```

**When to auto-use:** Single-word or very short impact statements only.
For section dividers, use fixed font-size instead. Never on slides with
mixed content or titles longer than 3-4 words.

---

## On-request (user must ask for these)

These features are powerful but opinionated. Claude should not use them unless
the user requests them — either in the outline notes, during the interview,
or during iteration.

### Image background

Full-bleed image behind the slide content. Darkens automatically for readability.

```html
<section data-background-image="https://example.com/image.jpg"
         data-background-size="cover"
         data-background-opacity="0.3">
  <h2>Slide Title</h2>
  <p>Content over the image.</p>
</section>
```

**User triggers:** "make {005} a fullscreen image background", "use this image
as the background for the title slide", or noting an image URL in the outline.

### GIF background

Full-bleed animated GIF. Same as image background but with motion.

```html
<section data-background-image="https://example.com/animation.gif"
         data-background-size="cover"
         data-background-opacity="0.25">
  <h2>Slide Title</h2>
</section>
```

**User triggers:** "make {007} a fullscreen gif", "use this gif as background".

**Tip:** Keep opacity low (0.2-0.3) so text remains readable. For a GIF-only
slide with no text overlay, opacity can go higher (0.6-0.8).

### Video background

Embedded video as slide background. Auto-plays, muted by default.
See the `video` component for the full video pattern catalog (YouTube/Vimeo
embeds, split layouts, browser-frame treatment, inline HTML5 video).

```html
<section data-background-video="https://assets.mixkit.co/videos/45378/45378-720.mp4"
         data-background-video-loop
         data-background-video-muted
         data-background-opacity="0.3">
  <h2>Slide Title</h2>
</section>
```

**User triggers:** "embed this video as a background", "video background on {003}".

### iframe background

Embed a live webpage as the slide background. Interactive by default.

```html
<section data-background-iframe="https://example.com"
         data-background-interactive>
  <!-- Optional overlay content -->
  <div style="position:absolute; bottom:2rem; left:3rem; background:rgba(6,10,18,0.85); padding:1rem 1.5rem; border-radius:6px;">
    <h3>Live Demo</h3>
  </div>
</section>
```

**User triggers:** "embed this URL as an iframe slide", "make {010} a live
iframe of this page".

**Important limitation:** Most websites block iframe embedding via
`X-Frame-Options` or `Content-Security-Policy` headers. **Iframe slides
are primarily useful for localhost demos** — your own dev server, ttyd
terminals, local apps, or tools running on `localhost`. Very few
production websites allow framing.

**What works in iframes:**
- `localhost` services (ttyd, dev servers, local apps)
- Sites you control (where you can set permissive headers)
- Embeddable widgets (CodePen, JSFiddle, Google Maps, YouTube)

**What doesn't work (blocked by most sites):**
- Most production websites (Drupal.org, GitHub, etc.)
- SaaS apps, government sites, banks, social media

**If the user requests an iframe for a site that blocks it:** warn them
and suggest alternatives — a full-bleed screenshot as a background image
with a clickable link overlay, or switch to a localhost demo.

### Parallax background

Subtle depth effect on a repeating background image as slides change.
Set globally in Reveal.initialize, not per-slide.

```js
Reveal.initialize({
  parallaxBackgroundImage: 'https://example.com/pattern.png',
  parallaxBackgroundSize: '2000px 1200px',
  parallaxBackgroundHorizontal: 200,
  parallaxBackgroundVertical: 50
});
```

**User triggers:** "add parallax scrolling", "use a parallax background".

**Note:** Parallax replaces the theme's background treatment (dot-grid, etc.)
so only enable when the user explicitly wants it.

### Per-slide transitions

Override the global transition for a specific slide. Use for emphasis or
dramatic effect.

```html
<!-- Zoom in for dramatic reveal -->
<section data-transition="zoom">

<!-- Slide in from a specific direction -->
<section data-transition="slide-in fade-out">

<!-- No transition (instant cut) -->
<section data-transition="none">
```

Available transitions: `none`, `fade`, `slide`, `convex`, `concave`, `zoom`

**User triggers:** "zoom into {008}", "hard cut to {012}", "make the
transition to {005} dramatic".

### Background transitions

Transition just the background independently of content.

```html
<section data-background-transition="zoom"
         data-background-color="#1a1a2e">
```

**User triggers:** "zoom the background on {006}", usually paired with a
background image or color change.

---

## Interview additions

During the interview, if the content seems to warrant it, Claude can ask:

- "Some of these slides would work well with progressive reveal (fragments) —
  want me to use that on denser slides?"
- "Slides {003}-{005} build on each other — want me to auto-animate between them?"
- "I see you mentioned a GIF/video/URL in your notes — want that as a
  fullscreen background or embedded in the slide content?"

---

## Restraint guidelines

- **Fragments:** Use on ~30-40% of slides max. Not every list needs a build.
- **Auto-animate:** Only between 2-3 related slides. Never chain more than 3.
- **r-fit-text:** Section dividers and impact moments only.
- **Background media:** Only when explicitly requested or noted in the outline.
- **Transition overrides:** Rare — the global `fade` is almost always right.
- **Parallax:** Global setting, only on explicit request.
- **iframes:** Only on explicit request with a URL provided.

The goal is a polished, professional deck — not a tech demo of Reveal.js features.
