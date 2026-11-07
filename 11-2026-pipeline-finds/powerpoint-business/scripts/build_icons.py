#!/usr/bin/env python3
"""Extract curated Lucide icons into a JSON index for the PowerPoint Business skill."""

import argparse
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

CURATED_ICONS = {
    "general": [
        "arrow-up", "arrow-down", "arrow-left", "arrow-right",
        "chevron-up", "chevron-down", "chevron-left", "chevron-right",
        "check", "x", "plus", "minus", "search", "settings", "menu",
        "home", "external-link", "link", "copy", "download", "upload",
        "refresh-cw", "maximize", "minimize", "filter", "move",
        "grip-vertical", "more-horizontal", "more-vertical", "hash",
        "at-sign", "percent", "zap", "layers", "layout", "grid-2x2", "list",
    ],
    "communication": [
        "mail", "message-square", "message-circle", "phone", "globe",
        "share-2", "send", "inbox", "bell", "megaphone", "rss", "wifi",
        "podcast", "volume-2", "mic", "video", "monitor", "smartphone",
        "tablet", "laptop",
    ],
    "data": [
        "bar-chart-2", "bar-chart-3", "chart-line", "chart-pie",
        "trending-up", "trending-down", "activity", "database", "server",
        "hard-drive", "cpu", "calculator", "sigma", "table",
        "calendar", "clock", "timer", "hourglass",
        "git-branch", "git-merge", "git-pull-request",
    ],
    "business": [
        "briefcase", "building-2", "dollar-sign", "credit-card", "wallet",
        "banknote", "receipt", "shopping-cart", "shopping-bag", "store",
        "trophy", "award", "medal", "badge-check", "handshake",
        "presentation", "clipboard", "file-text", "folder", "archive",
        "printer", "scale", "landmark",
    ],
    "education": [
        "book", "book-open", "book-marked", "notebook", "library",
        "graduation-cap", "school", "pen", "pencil", "pencil-line",
        "highlighter", "eraser", "ruler", "compass", "flask",
        "microscope", "telescope", "atom", "dna", "brain",
        "lightbulb", "lamp", "puzzle", "backpack", "apple",
        "clipboard-list", "file-check", "badge-info",
    ],
    "humanities": [
        "heart", "eye", "ear", "hand", "users", "user", "user-check",
        "feather", "scroll", "quote", "type", "text", "align-left",
        "align-center", "heading", "bold", "italic", "underline",
        "palette", "brush", "frame", "music",
    ],
    "nature": [
        "sun", "moon", "cloud", "cloud-rain", "snowflake", "wind",
        "thermometer", "droplets", "leaf", "tree-deciduous", "flower-2",
        "mountain", "waves", "flame", "sparkles", "sunrise", "sunset",
    ],
    "status": [
        "alert-circle", "alert-triangle", "info", "check-circle",
        "x-circle", "help-circle", "ban", "shield", "shield-check",
        "lock", "unlock", "key", "eye-off", "power",
        "toggle-left", "toggle-right", "loader", "circle-dot",
        "flag", "star", "bookmark", "thumbs-up", "thumbs-down",
        "smile", "frown",
    ],
    "arrows": [
        "arrow-up-right", "arrow-down-right", "corner-down-right",
        "corner-up-right", "move-right", "chevrons-right",
        "undo-2", "redo-2", "repeat", "rotate-cw", "rotate-ccw",
        "shuffle", "maximize-2", "minimize-2",
    ],
}

SVG_NS = "http://www.w3.org/2000/svg"
ELEMENT_TAGS = {"path", "circle", "rect", "line", "polyline", "polygon", "ellipse"}


def parse_svg(svg_path: Path) -> list[dict]:
    tree = ET.parse(svg_path)
    root = tree.getroot()
    elements = []
    for elem in root.iter():
        tag = elem.tag.replace(f"{{{SVG_NS}}}", "")
        if tag not in ELEMENT_TAGS:
            continue
        attrs = {}
        for k, v in elem.attrib.items():
            if k in ("class", "xmlns"):
                continue
            attrs[k] = v
        attrs["tag"] = tag
        elements.append(attrs)
    return elements


def build_icons(lucide_path: Path) -> dict:
    icons = {}
    total = 0
    missing = []

    for category, names in CURATED_ICONS.items():
        for name in names:
            svg_file = lucide_path / f"{name}.svg"
            if not svg_file.exists():
                missing.append(name)
                continue
            elements = parse_svg(svg_file)
            if not elements:
                missing.append(name)
                continue
            icons[name] = {
                "category": category,
                "viewBox": "0 0 24 24",
                "elements": elements,
            }
            total += 1

    if missing:
        print(f"Warning: {len(missing)} icons not found: {', '.join(missing[:10])}{'...' if len(missing) > 10 else ''}", file=sys.stderr)

    return {"meta": {"total": total, "viewBox": "0 0 24 24", "style": "stroke", "source": "lucide"}, "categories": {cat: list(CURATED_ICONS[cat]) for cat in CURATED_ICONS}, "icons": icons}


def main():
    parser = argparse.ArgumentParser(description="Build icon index from Lucide SVGs")
    parser.add_argument("--lucide-path", required=True, help="Path to lucide-static/icons/ directory")
    parser.add_argument("--output", default="references/icons.json", help="Output JSON file")
    args = parser.parse_args()

    lucide_path = Path(args.lucide_path)
    if not lucide_path.is_dir():
        print(f"Error: {lucide_path} is not a directory", file=sys.stderr)
        sys.exit(1)

    result = build_icons(lucide_path)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Built {result['meta']['total']} icons → {output}")


if __name__ == "__main__":
    main()
