---
name: video
category: component
description: Video embedding for slides — YouTube/Vimeo embeds, background video loops, inline HTML5 video, and video in browser-frame chrome. Includes auto-pause behavior.
---

> **CSS:** All styles for this component are in `themes/electric-dark.css`. Do not add CSS from this file.

## Usage

Video can appear in slides as full-bleed backgrounds, inline embeds, or
framed players. This component covers all video patterns.

### Named video patterns

Users and Claude reference these by name during building and iteration:

| Pattern | Description | Auto-use? |
|---------|------------|-----------|
| `video-bg` | Full-bleed looping video background, muted, low opacity, content on top | No — on request |
| `video-hero` | Full-bleed video IS the slide (higher opacity), minimal overlay text | No — on request |
| `video-embed` | YouTube/Vimeo iframe centered on slide with controls | No — on request |
| `video-split` | 50/50 layout — video on one side, content on the other | No — on request |
| `video-inline` | HTML5 `<video>` element with controls, styled in content area | No — on request |
| `video-frame` | Video in browser-frame chrome (macOS dots + URL bar) | No — on request |

All video patterns are on-request only. Claude should not add video unless
the user provides a URL or explicitly asks for it.

### Video sources

| Source | Embed format | Notes |
|--------|-------------|-------|
| **YouTube** | `https://www.youtube.com/embed/VIDEO_ID` | Most reliable. Add `?autoplay=1&mute=1&loop=1&playlist=ID` for background use |
| **Vimeo** | `https://player.vimeo.com/video/VIDEO_ID` | Add `?autoplay=1&muted=1&loop=1&background=1` for background use |
| **Local MP4** | `./videos/clip.mp4` | User places files in a `videos/` folder |
| **Direct URL** | Any `.mp4`, `.webm` URL | For `data-background-video` or `<video>` element |
| **Mixkit** | `https://assets.mixkit.co/videos/ID/ID-720.mp4` | Free, no attribution required. Best source for background loops. |
| **Pexels** | Direct MP4 URL from Pexels video downloads | Free for commercial use |

### YouTube URL conversion

Users will paste watch URLs. Convert them to embed format:
```
Watch:  https://www.youtube.com/watch?v=dQw4w9WgXcQ
Embed:  https://www.youtube.com/embed/dQw4w9WgXcQ
```

For background/autoplay use, add parameters:
```
https://www.youtube.com/embed/VIDEO_ID?autoplay=1&mute=1&loop=1&playlist=VIDEO_ID&controls=0&showinfo=0&rel=0
```

Note: `playlist=VIDEO_ID` is required for YouTube loop to work.

## HTML

**Full-bleed background video (looping, muted):**
```html
<section data-background-video="https://assets.mixkit.co/videos/45378/45378-720.mp4"
         data-background-video-loop
         data-background-video-muted
         data-background-opacity="0.25">
  <h2 style="color:#fff; text-shadow: 0 2px 20px rgba(0,0,0,0.5);">Slide Title</h2>
  <p>Content over the video.</p>
</section>
```

**Background video with higher opacity (video-forward):**
```html
<section data-background-video="URL"
         data-background-video-loop
         data-background-video-muted
         data-background-opacity="0.5">
  <div style="background:rgba(6,10,18,0.75); padding:1.5rem 2rem; border-radius:8px; display:inline-block;">
    <h2>Title in overlay box</h2>
    <p>Content stays readable over moving video.</p>
  </div>
</section>
```

**YouTube/Vimeo embed (centered with controls):**
```html
<div class="video-container">
  <iframe src="https://www.youtube.com/embed/VIDEO_ID"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen></iframe>
</div>
```

**YouTube as background (via iframe, no controls):**
```html
<section data-background-iframe="https://www.youtube.com/embed/VIDEO_ID?autoplay=1&mute=1&loop=1&playlist=VIDEO_ID&controls=0&showinfo=0&rel=0"
         data-background-interactive>
  <div style="position:absolute; bottom:2rem; left:3rem; background:rgba(6,10,18,0.85); padding:1rem 1.5rem; border-radius:6px;">
    <h3>Title over YouTube video</h3>
  </div>
</section>
```

**Video in split layout (50/50):**
```html
<div class="cols-2">
  <div>
    <h3>Description</h3>
    <p>Text content alongside the video.</p>
  </div>
  <div>
    <div class="video-container">
      <iframe src="https://www.youtube.com/embed/VIDEO_ID"
              frameborder="0" allowfullscreen></iframe>
    </div>
  </div>
</div>
```

**Inline HTML5 video with controls:**
```html
<video controls data-autoplay
       style="width:80%; border-radius:8px; border:2px solid var(--border); box-shadow: 0 0 30px rgba(170,255,0,0.06);">
  <source src="./videos/demo.mp4" type="video/mp4">
</video>
```

**Video in browser frame:**
```html
<div class="screenshot-frame" style="max-width:80%; margin:0 auto;">
  <div class="screenshot-chrome">
    <span class="mac-dot red"></span>
    <span class="mac-dot yellow"></span>
    <span class="mac-dot green"></span>
    <span class="screenshot-url">youtube.com</span>
  </div>
  <div class="video-container" style="border-radius:0;">
    <iframe src="https://www.youtube.com/embed/VIDEO_ID"
            frameborder="0" allowfullscreen></iframe>
  </div>
</div>
```

## Reveal.js auto-pause behavior

Reveal.js automatically pauses `<video>` and `<audio>` elements when you
navigate away from a slide. When you return, it resumes. This works for:

- `<video>` elements with `data-autoplay` attribute
- `<iframe>` embeds (paused via `postMessage`)
- Background video (`data-background-video`)

No extra JavaScript needed. Just add `data-autoplay` to inline `<video>`
elements for play-on-enter behavior:

```html
<video data-autoplay muted style="width:80%;">
  <source src="demo.mp4" type="video/mp4">
</video>
```

## Tips

- **Background video:** always use `data-background-video-muted` and
  `data-background-video-loop`. Keep opacity at 0.2-0.3 for readability.
  Higher opacity (0.4-0.6) works if text is in an overlay box.
- **YouTube embeds:** convert watch URLs to embed URLs. YouTube allows
  iframe embedding (unlike most sites), so these work reliably.
- **Vimeo:** also allows embedding. For background use, add `?background=1`
  which hides all controls and auto-plays muted.
- **Local video:** remind the user to create a `videos/` folder in their
  deck directory. Keep files small — 720p MP4 at 2-4 Mbps is plenty.
- **Autoplay restrictions:** browsers block autoplay with sound. Background
  videos must be muted. Inline videos with `data-autoplay` should also be
  muted unless the user explicitly wants sound.
- **Aspect ratio:** the `.video-container` CSS handles 16:9 responsively.
  For other ratios, adjust `padding-bottom` (75% for 4:3, 42.85% for 21:9).
- **Performance:** multiple video slides in one deck can be heavy. Limit to
  2-3 video slides per deck for smooth performance.
