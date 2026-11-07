---
name: agenda
category: component
description: Table of contents / agenda showing deck structure with optional "you are here" highlight. Auto-generate from section dividers.
---

> **CSS:** All styles for this component are in `themes/electric-dark.css`. Do not add CSS from this file.

## Usage

Use near the beginning of a deck (after the title slide) and optionally
repeat at section transitions with the current section highlighted. Most
valuable for decks with 10+ slides or 3+ major sections.

Claude should auto-generate this from the section dividers in the deck.

## HTML

**Full agenda:**
```html
<div class="agenda">
  <div class="agenda-item active">
    <span class="agenda-num">01</span>
    <span class="agenda-title">What Are Skills?</span>
  </div>
  <div class="agenda-item">
    <span class="agenda-num">02</span>
    <span class="agenda-title">Building Your First Skill</span>
  </div>
  <div class="agenda-item">
    <span class="agenda-num">03</span>
    <span class="agenda-title">Sharing and Collaboration</span>
  </div>
  <div class="agenda-item">
    <span class="agenda-num">04</span>
    <span class="agenda-title">Resources</span>
  </div>
</div>
```

**Compact horizontal variant (for repeating at section breaks):**
```html
<div class="agenda-bar">
  <span class="agenda-bar-item done">Intro</span>
  <span class="agenda-bar-sep">/</span>
  <span class="agenda-bar-item active">Building</span>
  <span class="agenda-bar-sep">/</span>
  <span class="agenda-bar-item">Sharing</span>
  <span class="agenda-bar-sep">/</span>
  <span class="agenda-bar-item">Resources</span>
</div>
```