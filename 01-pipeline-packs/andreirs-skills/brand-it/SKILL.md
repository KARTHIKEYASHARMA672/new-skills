---
name: brand-it
description: Applies Andrei's personal brand colors, typography, and visual style to any visual artifact — HTML pages, React components, dashboards, slides, charts, or any rendered output. Use when producing something visual and no other style is specified, or when the user asks for brand colors, design standards, or "make it look right".
---

# Personal Brand Styling

Andrei's visual identity. Apply it to anything rendered for him unless a project already defines its own design system, or he asks for a different look. Dark mode is the default; light mode is always available alongside it.

## Tokens

Drop these into the artifact and reference the variables — never hard-code the hex values inline.

```css
:root {
  /* Dark mode (default) */
  --bg:        #1e1e1e;
  --surface:   #252525;  /* cards, panels */
  --border:    #333333;
  --text:      #ffffff;

  /* Semantic — same role in both modes */
  --success:   #4caf7d;  /* green  — done / confirm */
  --info:      #6b9bd2;  /* blue   — link / neutral action */
  --danger:    #e05c4b;  /* red    — error / warning / destructive */
  --highlight: #c9970a;  /* gold   — callout / accent */
}

@media (prefers-color-scheme: light) {
  :root {
    --bg:      #f5f0e8;
    --surface: #ede8df;
    --border:  #ccc6bb;
    --text:    #1a1a1a;
    /* Semantic colors darken ~20% in light mode */
    --success:   #3a8c63;
    --info:      #4f7cb0;
    --danger:    #c0432f;
    --highlight: #a87c08;
  }
}
```

For a manual toggle, mirror the light values under a `[data-theme="light"]` selector instead of (or alongside) the media query.

## Typography

- Headings: **Inter** 600–700, line-height ~1.15–1.25 (tighter than body)
- Body: **Inter** 400, line-height 1.6
- Code: **JetBrains Mono**
- **Adornments follow the text they sit with.** Section numbers, list markers, badges, and step counters use the heading/body typeface (Inter), not the mono. Reserve JetBrains Mono for actual code, paths, and terminal-style labels — a stray mono numeral next to an Inter heading reads as a mistake.

Load from `fonts.googleapis.com` with a system-font fallback stack so the artifact still reads correctly offline. In artifacts that is the only stylesheet host allowed — `fonts.bunny.net` and self-hosted faces are blocked and fall back silently.

## Icons

Icons work in artifacts, but only three delivery routes survive the sandbox CSP. Pick by how many you need:

- **Under ~15 icons: inline SVG.** Paste the paths from Lucide or Heroicons. `fill="none" stroke="currentColor" stroke-width="2"` so the icon takes the color of the text it sits with — no icon-specific color tokens.
- **More than that, or a full set: Material Symbols from Google Fonts.** `icon_names=` subsets the font to the glyphs you name: 2 KB for eight, against 328 KB unsubsetted. List them alphabetically and add `&display=block`, both per Google's docs.
- **Icon-heavy pages only: a UMD library** from `cdnjs.cloudflare.com` or `cdn.jsdelivr.net/npm/` — Feather 20 KB, Lucide 87 KB and jsdelivr-only. Font Awesome's JS bundle is 536 KB; it never pays off.

Blocked, with no console error and no symptom but blank space: icon-font **CSS** from any CDN (Font Awesome, Bootstrap Icons), icons pulled as remote images, and SVG sprites fetched at runtime.

Material Symbols glyphs are ligatures on the lowercase name, so the icon element needs this reset — an inherited `text-transform: uppercase` from a label style prints the word `check_circle` instead of the icon:

```css
.icon {
  font-family: "Material Symbols Rounded";
  text-transform: none; letter-spacing: normal;
  word-wrap: normal; white-space: nowrap;
  font-variant-ligatures: normal;
}
```

### Every icon carries value

Function over form. An icon is allowed when it does work the text alone does not: it speeds a scan, replaces a label that will not fit, or encodes state redundantly with color for anyone who cannot see the hue.

- **Use one for:** status on a row or tile (done / warning / error), an action on a control too small for a label, a repeated type marker in a list or table, a legend key beside a series.
- **Skip it on:** section headings, prose, nav items that already have a word, and anything where it merely restates the adjacent label. A page with an icon per heading reads as decorated, not designed.
- **Icons obey the semantic colors** — green done, blue neutral action, red error, gold callout. An icon that signals nothing stays in the text color. Never a new accent hue for an icon.
- **One set per page.** Mixing Feather strokes with Material fills reads as an accident.
- 24px standalone, 16–20px inline with text, optically aligned to the cap height, never scaled past its grid.
- **No emoji as UI markers.** Zero color control, no stroke weight, and a different shape on every platform.
- Icon-only controls need an `aria-label`; a decorative icon beside its own label gets `aria-hidden="true"`.
- If you cannot say what a reader learns from an icon, delete it.

## Rules

- **Dark mode first.** Always include light mode, via `prefers-color-scheme` or a manual toggle.
- **Headings use body text color** (white / near-black), never decorative colors.
- **Semantic colors communicate meaning only** — never decoration. Green = success/done, blue = info/neutral action, red = error/warning/delete, gold = callout/highlight.
- **Buttons:** primary action in blue, destructive in red, success confirmation in green.
- **Generous whitespace. No gradients. Minimal UI.**
- **Always responsive.** Mobile breakpoint at 640px.

## Don't

- Don't override a project's existing design system — these are personal defaults, not a mandate.
- Don't use color purely to decorate; if a color appears, it should signal meaning.
- Don't introduce extra accent hues, gradients, or shadows for flair.
