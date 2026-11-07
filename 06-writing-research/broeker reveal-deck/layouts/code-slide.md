---
name: code-slide
category: layout
description: Full-width code-focused slide using the codeblock component.
---

## Usage

Use when the primary content is a code snippet, command sequence, or file contents. Minimal surrounding text.

## HTML

```html
<section data-background-color="#060A12">
  <span class="slide-tag">{003}</span>
  <div class="accent-line"></div>
  <h2>Slide Title</h2>
  <p style="margin-bottom:0.8rem;">Brief context for the code below.</p>

  <div class="codeblock">
    <div class="codeblock-header">
      <span class="codeblock-dot" style="background:#FF5F56"></span>
      <span class="codeblock-dot" style="background:#FFBD2E"></span>
      <span class="codeblock-dot" style="background:#27C93F"></span>
    </div>
    <pre><code># Commands or code here
example command --flag value
another command</code></pre>
  </div>
</section>
```
