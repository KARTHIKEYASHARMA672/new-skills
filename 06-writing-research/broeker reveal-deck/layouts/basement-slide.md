---
name: basement-slide
category: layout
description: Vertical (basement) slides for deeper dives beneath a main slide. Navigated by pressing down instead of right.
---

> **CSS:** All styles for this layout are in `themes/electric-dark.css`. Do not add CSS from this file.

## Usage

Basement slides sit below a parent slide in Reveal.js's vertical stack. The
audience navigates right for the main flow and down for optional deeper content.
Use them for:

- Detail that supports a main point but would slow down the primary flow
- Examples, demos, or walkthroughs that not every audience needs
- Supplementary data, charts, or references tied to a specific topic
- "Appendix" material the presenter can skip or dive into based on time/audience

### Outline convention

In markdown outlines, `##` headings are main (horizontal) slides and `###`
sub-headings beneath them are basement (vertical) slides:

```markdown
## Main Topic            <-- horizontal slide
### Deeper Dive          <-- basement slide (below Main Topic)
### Another Detail       <-- second basement slide
## Next Main Topic       <-- back to horizontal flow
```

### When Claude should auto-create basement slides

- A slide has too much content even after splitting — move the deep-dive
  portion to a basement slide instead of adding more horizontal slides
- Examples or walkthroughs that illustrate a main point but aren't essential
- Reference material (command lists, config options, links) tied to a topic
- Content flagged as "optional" or "if time permits" in the outline

## HTML

Wrap the parent and its basement slides in a single outer `<section>`:

```html
<!-- Vertical stack: parent + basement slides -->
<section>

  <!-- Parent slide (horizontal flow) -->
  <section data-background-color="#060A12">
    <span class="slide-tag">{003}</span>
    <div class="accent-line"></div>
    <h2>Main Topic</h2>
    <p>Core content here.</p>
    <span class="basement-hint">&#9660; deeper dive below</span>
  </section>

  <!-- Basement slide 1 -->
  <section data-background-color="#060A12">
    <span class="slide-tag">{003a}</span>
    <div class="accent-line" style="background:var(--amber);"></div>
    <h2>Detailed Example</h2>
    <p>Extended content that supports the parent slide.</p>
  </section>

  <!-- Basement slide 2 (optional) -->
  <section data-background-color="#060A12">
    <span class="slide-tag">{003b}</span>
    <div class="accent-line" style="background:var(--amber);"></div>
    <h2>Reference Commands</h2>
    <div class="codeblock">
      <pre><code>example commands here</code></pre>
    </div>
  </section>

</section>
```

### Slug convention

- Parent slide keeps its numeric slug: `{003}`
- Basement slides append a letter: `{003a}`, `{003b}`, `{003c}`
- This keeps the main slug sequence clean while making basement slides
  referenceable during iteration

### Visual cues

The parent slide gets a small down-arrow hint so the presenter knows there's
more below. Basement slides use the amber accent line (instead of cyan) to
visually distinguish them from main-flow slides.
