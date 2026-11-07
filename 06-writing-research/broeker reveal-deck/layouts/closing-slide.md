---
name: closing-slide
category: layout
description: Dedicated closing slide with call to action, contact info, and optional QR code. Different from title slide in purpose and tone.
---

> **CSS:** All styles for this layout are in `themes/electric-dark.css`. Do not add CSS from this file.

## Usage

Final slide of the deck. Should leave the audience with a clear next step
or memorable takeaway. Can include contact info, links, QR codes, or a
strong closing statement.

## HTML

**CTA closing:**
```html
<section data-background-color="#060A12">
  <span class="slide-tag">{015}</span>
  <div class="accent-line"></div>
  <h2 class="glow" style="font-size:2.5em;">Start Building Skills Today</h2>
  <p style="font-size:0.85em; color:var(--muted); max-width:65%; margin-top:0.8rem;">
    Pick one workflow you repeated this week. Turn it into a skill.
    Share it with the team.
  </p>

  <div class="closing-links">
    <div class="closing-link">
      <span class="closing-link-label">Docs</span>
      <a href="https://code.claude.com/docs/en/skills">code.claude.com/docs</a>
    </div>
    <div class="closing-link">
      <span class="closing-link-label">Team repo</span>
      <a href="https://github.com/electriccitizen/skills">electriccitizen/skills</a>
    </div>
  </div>
</section>
```

**With QR code (inline SVG or image):**
```html
<div class="closing-qr">
  <img src="qr-code.svg" alt="QR code" width="120">
  <span class="closing-link-label">Scan to get started</span>
</div>
```
