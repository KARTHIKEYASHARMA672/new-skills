---
name: brand-it-cowork
description: "Cowork-specific companion to `brand-it`. Applies Andrei's personal brand — colors, typography, flat dark-mode-first style — mapped onto the surfaces Cowork actually renders on: live artifacts, inline show_widget visualizations, HTML/React artifacts, and pptx/docx/pdf deliverables. Use when producing something visual for Andrei inside Cowork, or when he asks for his brand across a Cowork deck, doc, widget, or dashboard. Outside Cowork, use `brand-it` instead."
---

# Andrei's brand — Cowork surfaces

Andrei's visual identity, adapted to the surfaces Cowork actually renders on. The identity itself is constant; what changes per surface is *how much of it you hard-code*. The trap on Cowork is forcing custom hex and fonts onto a surface that already has its own themed design system — that fights the host and looks worse, not more on-brand. So first figure out which surface you're rendering to, then follow the matching section.

Apply this unless a project already defines its own design system, or Andrei asks for a different look.

## The identity

```css
/* Dark mode is the default. Light mode always available alongside it. */
--bg:        #1e1e1e;   /* light: #f5f0e8 */
--surface:   #252525;   /* light: #ede8df — cards, panels */
--border:    #333333;   /* light: #ccc6bb */
--text:      #ffffff;   /* light: #1a1a1a */

/* Semantic — meaning only, never decoration. ~20% darker in light mode. */
--success:   #4caf7d;   /* light: #3a8c63 — green,  done / confirm */
--info:      #6b9bd2;   /* light: #4f7cb0 — blue,   link / neutral action */
--danger:    #e05c4b;   /* light: #c0432f — red,    error / warning / destructive */
--highlight: #c9970a;   /* light: #a87c08 — gold,   callout / accent */
```

Type: **Inter** for headings (600–700) and body (400, line-height 1.6); **JetBrains Mono** for code.

Principles, in Andrei's words: dark mode first, headings use the plain text color (never a decorative hue), color signals meaning or it doesn't appear, generous whitespace, no gradients, no extra accent hues, minimal UI, always responsive (mobile at 640px). These happen to match how Cowork's own surfaces want to look, which is why the mapping below is mostly painless.

## Surface: live artifacts and standalone HTML / React artifacts

Full pages you author from scratch (`create_artifact`, `.html`, `.jsx`) — here the identity applies in full. Define the tokens above as CSS variables and reference them; never hard-code hex inline. Dark mode is the default; include light mode via `prefers-color-scheme` or a `[data-theme="light"]` toggle.

Watch the Cowork constraints:

- **Fonts** load only from allowlisted CDNs — `fonts.googleapis.com` / `fonts.gstatic.com` (or `cdnjs.cloudflare.com`). Always give a system-font fallback stack so it reads correctly if the font is blocked.
- **Live artifacts** (`create_artifact`) may only pull JS from CDN for Chart.js, Grid.js, and Mermaid; everything else must be inline. **No `localStorage`/`sessionStorage`** in any artifact — keep state in memory (React state or JS variables). `localStorage` for remembering a filter choice is fine *only* in a live artifact per its own rules, not in chat artifacts.
- Charts can't read CSS variables from a canvas — pass the resolved hex (`--info` #6b9bd2, etc.) directly, and keep the semantic mapping.

## Surface: inline visualizations (show_widget)

These render inside chat on a host-owned canvas with its own themed design system that already auto-adapts to light/dark. Do **not** paste Andrei's hex or load Inter here — you'd be fighting the host and it'll look grafted-on. Instead, honor the identity's *principles* (which already align) using the host's tokens:

- Outer container stays **transparent** — the host provides the background. Never set `--bg` here.
- Text uses `var(--text-primary)` / `var(--text-secondary)`; surfaces use `var(--surface-1)` / `var(--surface-2)`; borders use `var(--border)`. These flip for dark/light automatically.
- For semantic meaning use the role tokens — `--text-success` / `--bg-success`, `--text-danger`, `--text-accent` — which carry the same green=done, red=error, blue=neutral-action meaning Andrei's palette does.
- For categorical color in diagrams/charts use the built-in ramp classes (`c-blue`, `c-teal`, `c-amber`…), not custom hues. Andrei's "no gradients, flat, minimal, whitespace, color = meaning" rules are the house rules here anyway.

The one-line test: on an inline widget, express Andrei's *taste* through the host's variables; save his literal *tokens* for full pages you own end to end.

## Surface: documents and decks (pptx / docx / pdf)

Print and slides are light surfaces — dark-mode-first doesn't apply. Use the light-mode palette: paper `#f5f0e8` or white background, text `#1a1a1a`, headings in the text color at Inter 600–700, body Inter 400. Reserve the semantic colors for accents that carry meaning — a gold (`#a87c08`) callout box, a green (`#3a8c63`) positive figure, a red (`#c0432f`) risk flag — never as decoration on every heading. Code or monospaced data uses JetBrains Mono. Keep the same restraint: whitespace, no gradients, no extra hues.

## Don't

- Don't override a project's existing design system — these are Andrei's personal defaults, not a mandate.
- Don't hard-code the dark-mode hex into an inline `show_widget` — use the host tokens there.
- Don't use color to decorate; if a color appears, it signals meaning.
- Don't add gradients, shadows for flair, or accent hues beyond the four semantic colors.
