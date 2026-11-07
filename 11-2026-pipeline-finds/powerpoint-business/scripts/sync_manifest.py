#!/usr/bin/env python3
"""Sync slide-manifest.json from SVG element IDs and attributes."""

import argparse
import json
import re
import sys
from pathlib import Path

from lxml import etree

SVG_NS = "http://www.w3.org/2000/svg"
XHTML_NS = "http://www.w3.org/1999/xhtml"
ID_PATTERN = re.compile(r"^s(\d+)-(.+)$")

# Role detection from ID suffix
ROLE_MAP = {
    "title": "title",
    "subtitle": "title",
    "heading": "title",
    "card": "card",
    "stat": "stat",
    "chart": "chart",
    "bullet": "bullet",
    "bullets": "bullet",
    "list": "bullet",
    "image": "image",
    "img": "image",
    "icon": "image",
    "label": "label",
    "caption": "label",
    "footer": "label",
    "divider": "decoration",
    "line": "decoration",
    "bg": "decoration",
    "background": "decoration",
}


def detect_role(id_suffix: str) -> str:
    """Map ID suffix to semantic role."""
    suffix_lower = id_suffix.lower()
    # Direct match
    if suffix_lower in ROLE_MAP:
        return ROLE_MAP[suffix_lower]
    # Prefix match (e.g., 'card1', 'stat-revenue')
    for key, role in ROLE_MAP.items():
        if suffix_lower.startswith(key):
            return role
    return "unknown"


def get_numeric(el: etree._Element, attr: str, default: float = 0.0) -> float:
    """Get numeric attribute value, stripping units."""
    val = el.get(attr)
    if val is None:
        return default
    val = val.strip().rstrip("px").rstrip("pt").rstrip("em").rstrip("%")
    try:
        return float(val)
    except ValueError:
        return default


def extract_text(el: etree._Element) -> str:
    """Extract text content from <text> or <foreignObject>."""
    tag = etree.QName(el.tag).localname if isinstance(el.tag, str) else ""
    if tag == "text":
        return " ".join("".join(el.itertext()).split())
    if tag == "foreignObject":
        # Extract text from HTML children
        texts = []
        for child in el.iter():
            if child.text:
                texts.append(child.text.strip())
            if child.tail:
                texts.append(child.tail.strip())
        return " ".join(t for t in texts if t)
    return ""


def get_bbox(el: etree._Element) -> dict:
    """Extract bounding box from element attributes."""
    tag = etree.QName(el.tag).localname if isinstance(el.tag, str) else ""
    if tag == "circle":
        cx = get_numeric(el, "cx")
        cy = get_numeric(el, "cy")
        r = get_numeric(el, "r")
        return {"x": cx - r, "y": cy - r, "width": r * 2, "height": r * 2}
    if tag == "ellipse":
        cx = get_numeric(el, "cx")
        cy = get_numeric(el, "cy")
        rx = get_numeric(el, "rx")
        ry = get_numeric(el, "ry")
        return {"x": cx - rx, "y": cy - ry, "width": rx * 2, "height": ry * 2}
    return {
        "x": get_numeric(el, "x"),
        "y": get_numeric(el, "y"),
        "width": get_numeric(el, "width"),
        "height": get_numeric(el, "height"),
    }


def bbox_contains(parent_bbox: dict, child_bbox: dict) -> bool:
    """Check if child bbox is geometrically inside parent bbox."""
    px, py = parent_bbox["x"], parent_bbox["y"]
    pw, ph = parent_bbox["width"], parent_bbox["height"]
    cx, cy = child_bbox["x"], child_bbox["y"]
    return (
        px <= cx <= px + pw
        and py <= cy <= py + ph
    )


def detect_layout(elements: list[dict]) -> str:
    """Heuristic layout detection from element positions."""
    cards = [e for e in elements if e["role"] == "card"]
    stats = [e for e in elements if e["role"] == "stat"]

    if not cards and not stats:
        # Check if it's a title slide
        titles = [e for e in elements if e["role"] == "title"]
        if len(titles) >= 1 and len(elements) <= 4:
            return "title"
        return "content"

    items = cards or stats
    n = len(items)

    if n == 1:
        return "single-card"

    # Check if cards are in a grid
    ys = sorted(set(round(e["bbox"]["y"] / 20) * 20 for e in items))
    xs = sorted(set(round(e["bbox"]["x"] / 20) * 20 for e in items))

    if len(ys) == 1:
        return f"{n}-col"
    if len(ys) == 2:
        if n <= 4:
            return "2x2-grid"
        return f"2-row-grid"
    if len(xs) == 1:
        return f"{n}-row"

    return f"{len(xs)}x{len(ys)}-grid"


def parse_svg(svg_path: Path) -> dict | None:
    """Parse one SVG file into a slide manifest entry."""
    try:
        tree = etree.parse(str(svg_path))
    except etree.XMLSyntaxError as e:
        print(f"  WARNING: XML parse error in {svg_path.name}: {e}", file=sys.stderr)
        return None

    root = tree.getroot()
    # Extract slide number from filename
    m = re.search(r"slide-(\d+)", svg_path.stem)
    if not m:
        return None
    slide_idx = int(m.group(1))

    elements: list[dict] = []
    slide_title = ""

    for el in root.iter():
        eid = el.get("id")
        if not eid:
            continue
        id_match = ID_PATTERN.match(eid)
        if not id_match:
            continue

        el_slide_num = int(id_match.group(1))
        suffix = id_match.group(2)

        # Only include elements belonging to this slide
        if el_slide_num != slide_idx:
            continue

        tag = etree.QName(el.tag).localname if isinstance(el.tag, str) else str(el.tag)
        role = detect_role(suffix)
        bbox = get_bbox(el)
        text = extract_text(el)

        entry = {
            "id": eid,
            "tag": tag,
            "role": role,
            "bbox": bbox,
        }
        if text:
            entry["text"] = text

        elements.append(entry)

        if role == "title" and not slide_title:
            slide_title = text

    # Build parent-child hierarchy: cards contain children
    card_elements = [e for e in elements if e["role"] == "card"]
    non_card_elements = [e for e in elements if e["role"] != "card"]

    for card in card_elements:
        children = []
        remaining = []
        for elem in non_card_elements:
            if bbox_contains(card["bbox"], elem["bbox"]):
                children.append(elem)
            else:
                remaining.append(elem)
        if children:
            card["children"] = children
        non_card_elements = remaining

    # Merge: cards (with children) + remaining non-card elements
    final_elements = card_elements + non_card_elements
    final_elements.sort(key=lambda e: (e["bbox"]["y"], e["bbox"]["x"]))

    layout = detect_layout(elements)

    # Detect slide type
    slide_type = "content"
    if layout == "title":
        slide_type = "title"
    elif slide_idx == 1 and any(e["role"] == "title" for e in elements):
        slide_type = "cover"

    return {
        "index": slide_idx,
        "type": slide_type,
        "title": slide_title,
        "layout": layout,
        "svg_file": svg_path.name,
        "elements": final_elements,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync slide-manifest.json from SVG element IDs and attributes."
    )
    parser.add_argument("slides_dir", type=Path, help="Directory containing slide-{nn}.svg files")
    parser.add_argument("output", type=Path, help="Output manifest JSON path")
    parser.add_argument("--theme", type=str, default="corporate_blue", help="Theme name")
    args = parser.parse_args()

    if not args.slides_dir.is_dir():
        print(f"Error: {args.slides_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    svg_files = sorted(
        args.slides_dir.glob("slide-*.svg"),
        key=lambda p: int(re.search(r"(\d+)", p.stem).group(1)) if re.search(r"(\d+)", p.stem) else 0,
    )
    if not svg_files:
        print(f"Error: no slide-*.svg files in {args.slides_dir}", file=sys.stderr)
        sys.exit(1)

    slides = []
    total_elements = 0

    for svg_path in svg_files:
        entry = parse_svg(svg_path)
        if entry:
            total_elements += len(entry["elements"])
            # Count children too
            for elem in entry["elements"]:
                total_elements += len(elem.get("children", []))
            slides.append(entry)

    manifest = {
        "version": "1.0",
        "theme": args.theme,
        "slide_count": len(slides),
        "slides": slides,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Manifest written: {len(slides)} slides, {total_elements} elements -> {args.output}")


if __name__ == "__main__":
    main()
