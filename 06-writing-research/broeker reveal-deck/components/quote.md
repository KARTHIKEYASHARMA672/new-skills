---
name: quote
category: component
description: Large pull quote with attribution. Use for impactful statements, testimonials, or provocative framing. Different from inline blockquotes — this is the star of the slide.
---

> **CSS:** All styles for this component are in `themes/electric-dark.css`. Do not add CSS from this file.

## Usage

Use when a quote IS the content of the slide — not a supporting element but
the main event. Works for speaker quotes, user testimonials, provocative
statements to set up the next section, or key principles.

## HTML

**Standard quote:**
```html
<div class="pull-quote">
  <blockquote class="pull-quote-text">
    The best way to predict the future is to invent it.
  </blockquote>
  <cite class="pull-quote-cite">Alan Kay</cite>
</div>
```

**Quote with role/source:**
```html
<div class="pull-quote">
  <blockquote class="pull-quote-text">
    Skills turned our hard-won workflows into institutional knowledge.
  </blockquote>
  <cite class="pull-quote-cite">
    Sarah Chen <span class="pull-quote-role">— Senior Developer, Electric Citizen</span>
  </cite>
</div>
```