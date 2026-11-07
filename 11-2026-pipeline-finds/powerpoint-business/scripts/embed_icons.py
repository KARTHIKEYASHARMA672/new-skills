#!/usr/bin/env python3
"""Post-process SVG files: replace <use data-icon="name"/> placeholders with actual icon paths."""

import argparse
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"

ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", XLINK_NS)


def render_icon_element(elem_data: dict, fill: str) -> str:
    tag = elem_data.get("tag", "path")
    attrs = {k: v for k, v in elem_data.items() if k != "tag"}
    attrs.pop("class", None)
    if tag == "path":
        attrs["fill"] = "none"
        attrs["stroke"] = fill
        attrs["stroke-width"] = attrs.get("stroke-width", "2")
        attrs["stroke-linecap"] = "round"
        attrs["stroke-linejoin"] = "round"
    elif tag in ("circle", "ellipse"):
        attrs["fill"] = "none"
        attrs["stroke"] = fill
        attrs["stroke-width"] = attrs.get("stroke-width", "2")
    elif tag in ("line", "polyline", "polygon"):
        attrs["fill"] = "none" if tag != "polygon" else attrs.get("fill", "none")
        attrs["stroke"] = fill
        attrs["stroke-width"] = attrs.get("stroke-width", "2")
        attrs["stroke-linecap"] = "round"
        attrs["stroke-linejoin"] = "round"
    elif tag == "rect":
        attrs["fill"] = "none"
        attrs["stroke"] = fill
        attrs["stroke-width"] = attrs.get("stroke-width", "2")
        attrs["rx"] = attrs.get("rx", "0")

    attr_str = " ".join(f'{k}="{v}"' for k, v in attrs.items())
    return f"<{tag} {attr_str}/>"


def embed_icons_in_svg(svg_path: Path, icons: dict, in_place: bool = False) -> bool:
    content = svg_path.read_text(encoding="utf-8")
    pattern = re.compile(
        r'<use\s+data-icon="([^"]+)"'
        r'(?:\s+x="([^"]*)")?'
        r'(?:\s+y="([^"]*)")?'
        r'(?:\s+width="([^"]*)")?'
        r'(?:\s+height="([^"]*)")?'
        r'(?:\s+fill="([^"]*)")?'
        r'[^/]*/>'
    )

    replacements = 0

    def replace_use(match):
        nonlocal replacements
        name = match.group(1)
        x = match.group(2) or "0"
        y = match.group(3) or "0"
        w = match.group(4) or "24"
        h = match.group(5) or "24"
        fill = match.group(6) or "currentColor"

        icon_data = icons.get("icons", {}).get(name)
        if not icon_data:
            print(f"  Warning: icon '{name}' not found in icons.json", file=sys.stderr)
            return match.group(0)

        scale_x = float(w) / 24
        scale_y = float(h) / 24

        inner = "\n".join(f"    {render_icon_element(e, fill)}" for e in icon_data["elements"])
        replacements += 1
        return (
            f'<g id="icon-{name}-{replacements}" '
            f'transform="translate({x},{y}) scale({scale_x},{scale_y})">\n'
            f"{inner}\n"
            f"  </g>"
        )

    result = pattern.sub(replace_use, content)

    if replacements > 0:
        output_path = svg_path if in_place else svg_path.with_suffix(".embedded.svg")
        output_path.write_text(result, encoding="utf-8")
        print(f"  {svg_path.name}: {replacements} icons embedded")
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Embed icon placeholders in SVG files")
    parser.add_argument("slides_dir", help="Directory containing SVG files")
    parser.add_argument("--icons", default="references/icons.json", help="Path to icons.json")
    parser.add_argument("--in-place", action="store_true", help="Modify files in place")
    args = parser.parse_args()

    icons_path = Path(args.icons)
    if not icons_path.exists():
        print(f"Error: {icons_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(icons_path) as f:
        icons = json.load(f)

    slides_dir = Path(args.slides_dir)
    svg_files = sorted(slides_dir.glob("*.svg"))
    if not svg_files:
        print(f"No SVG files found in {slides_dir}")
        return

    total = 0
    for svg_file in svg_files:
        if embed_icons_in_svg(svg_file, icons, args.in_place):
            total += 1

    print(f"Done: {total} files processed")


if __name__ == "__main__":
    main()
