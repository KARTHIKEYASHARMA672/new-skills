#!/usr/bin/env python3
"""Generate interactive HTML preview from SVG slides."""

import argparse
import html
import re
import sys
from pathlib import Path


def discover_slides(slides_dir: Path) -> list[Path]:
    """Find slide-{nn}.svg files sorted by number."""
    pattern = re.compile(r"^slide-(\d+)\.svg$")
    matched = []
    for f in slides_dir.iterdir():
        m = pattern.match(f.name)
        if m:
            matched.append((int(m.group(1)), f))
    matched.sort(key=lambda t: t[0])
    if not matched:
        print(f"Error: no slide-*.svg files found in {slides_dir}", file=sys.stderr)
        sys.exit(1)
    return [f for _, f in matched]


def build_html(slide_files: list[Path]) -> str:
    """Build self-contained HTML with gallery/scroll/present modes."""
    slide_count = len(slide_files)

    # Read and sanitize SVG contents
    svgs: list[str] = []
    for sf in slide_files:
        content = sf.read_text(encoding="utf-8")
        # Strip XML declaration if present
        content = re.sub(r"<\?xml[^?]*\?>", "", content).strip()
        svgs.append(content)

    # Build slide divs
    slide_divs = "\n".join(
        f'<div class="slide" data-index="{i}">{svg}</div>'
        for i, svg in enumerate(svgs)
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Slide Preview ({slide_count} slides)</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #1a1a2e; color: #eee; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }}
header {{
  position: sticky; top: 0; z-index: 100;
  background: #16213e; padding: 10px 24px;
  display: flex; align-items: center; gap: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}}
header h1 {{ font-size: 16px; font-weight: 500; flex: 1; }}
header .count {{ font-size: 13px; opacity: 0.7; }}
.mode-btn {{
  background: #0f3460; border: 1px solid #1a508b; color: #eee;
  padding: 6px 14px; border-radius: 4px; cursor: pointer; font-size: 13px;
}}
.mode-btn.active {{ background: #1a508b; border-color: #53a8ff; }}
.mode-btn:hover {{ background: #1a508b; }}

/* Gallery mode */
.gallery {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 16px; padding: 24px; }}
.gallery .slide {{ cursor: pointer; border-radius: 6px; overflow: hidden; border: 2px solid transparent; transition: border-color 0.2s, transform 0.15s; }}
.gallery .slide:hover {{ border-color: #53a8ff; transform: scale(1.02); }}
.gallery .slide svg {{ width: 100%; height: auto; display: block; }}

/* Scroll mode */
.scroll {{ padding: 24px; max-width: 1100px; margin: 0 auto; }}
.scroll .slide {{ margin-bottom: 20px; border-radius: 6px; overflow: hidden; }}
.scroll .slide svg {{ width: 100%; height: auto; display: block; }}

/* Present mode */
.present {{ position: fixed; inset: 0; background: #000; z-index: 200; display: flex; align-items: center; justify-content: center; }}
.present .slide {{ display: none; width: 100%; height: 100%; }}
.present .slide.active {{ display: flex; align-items: center; justify-content: center; }}
.present .slide svg {{ max-width: 100%; max-height: 100%; }}
.present .slide-counter {{
  position: fixed; bottom: 16px; right: 24px; font-size: 14px;
  color: rgba(255,255,255,0.5); z-index: 201;
}}

/* Lightbox (gallery click) */
.lightbox {{
  position: fixed; inset: 0; background: rgba(0,0,0,0.92); z-index: 150;
  display: none; align-items: center; justify-content: center; cursor: pointer;
}}
.lightbox.show {{ display: flex; }}
.lightbox svg {{ max-width: 95%; max-height: 95%; }}
</style>
</head>
<body>
<header>
  <h1>Slide Preview</h1>
  <span class="count">{slide_count} slides</span>
  <button class="mode-btn active" data-mode="gallery">Gallery</button>
  <button class="mode-btn" data-mode="scroll">Scroll</button>
  <button class="mode-btn" data-mode="present">Present</button>
</header>
<main id="container" class="gallery">
{slide_divs}
</main>
<div class="lightbox" id="lightbox"></div>
<script>
(function() {{
  const container = document.getElementById('container');
  const slides = Array.from(container.querySelectorAll('.slide'));
  const lightbox = document.getElementById('lightbox');
  const modeButtons = document.querySelectorAll('.mode-btn');
  let mode = 'gallery';
  let presentIdx = 0;

  function setMode(m) {{
    mode = m;
    container.className = m;
    modeButtons.forEach(b => b.classList.toggle('active', b.dataset.mode === m));
    if (m === 'present') {{
      presentIdx = 0;
      showPresent();
      container.style.display = '';
    }} else {{
      slides.forEach(s => {{ s.classList.remove('active'); s.style.display = ''; }});
      const counter = container.querySelector('.slide-counter');
      if (counter) counter.remove();
    }}
    lightbox.classList.remove('show');
  }}

  function showPresent() {{
    slides.forEach((s, i) => {{
      s.classList.toggle('active', i === presentIdx);
    }});
    let counter = container.querySelector('.slide-counter');
    if (!counter) {{
      counter = document.createElement('div');
      counter.className = 'slide-counter';
      container.appendChild(counter);
    }}
    counter.textContent = (presentIdx + 1) + ' / ' + slides.length;
  }}

  modeButtons.forEach(b => b.addEventListener('click', () => setMode(b.dataset.mode)));

  container.addEventListener('click', function(e) {{
    const slide = e.target.closest('.slide');
    if (!slide) return;
    if (mode === 'gallery') {{
      lightbox.innerHTML = slide.querySelector('svg').outerHTML;
      lightbox.classList.add('show');
    }} else if (mode === 'present') {{
      presentIdx = Math.min(presentIdx + 1, slides.length - 1);
      showPresent();
    }}
  }});

  lightbox.addEventListener('click', () => lightbox.classList.remove('show'));

  document.addEventListener('keydown', function(e) {{
    if (lightbox.classList.contains('show')) {{
      if (e.key === 'Escape') lightbox.classList.remove('show');
      return;
    }}
    if (mode === 'present') {{
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'Enter') {{
        e.preventDefault();
        presentIdx = Math.min(presentIdx + 1, slides.length - 1);
        showPresent();
      }} else if (e.key === 'ArrowLeft') {{
        e.preventDefault();
        presentIdx = Math.max(presentIdx - 1, 0);
        showPresent();
      }} else if (e.key === 'Escape') {{
        setMode('gallery');
      }}
    }}
  }});
}})();
</script>
</body>
</html>"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate interactive HTML preview from SVG slides."
    )
    parser.add_argument("slides_dir", type=Path, help="Directory containing slide-{nn}.svg files")
    parser.add_argument("output", type=Path, help="Output .html file path")
    args = parser.parse_args()

    if not args.slides_dir.is_dir():
        print(f"Error: {args.slides_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    slide_files = discover_slides(args.slides_dir)
    html_content = build_html(slide_files)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html_content, encoding="utf-8")
    print(f"Preview written to {args.output}")


if __name__ == "__main__":
    main()
