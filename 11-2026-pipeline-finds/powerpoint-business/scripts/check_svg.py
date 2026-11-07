#!/usr/bin/env python3
"""Automated SVG quality checks: well-formedness, safe area, contrast, gaps, IDs."""

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import NamedTuple

from lxml import etree

EXPECTED_VIEWBOX = "0 0 1280 720"
SAFE_LEFT = 60
SAFE_TOP = 60
SAFE_RIGHT = 1220
SAFE_BOTTOM = 660
MIN_FONT_SIZE = 12
MIN_CONTRAST_RATIO = 4.5
MIN_CARD_GAP = 20
ID_PATTERN = re.compile(r"^s(\d+)-(.+)$")
SVG_NS = "http://www.w3.org/2000/svg"


class Issue(NamedTuple):
    severity: str  # FAIL, WARN
    check: str
    message: str


def parse_color(color_str: str | None) -> tuple[int, int, int] | None:
    """Parse CSS color string to (r, g, b). Supports #rgb, #rrggbb, rgb(), named basics."""
    if not color_str:
        return None
    color_str = color_str.strip().lower()

    named = {
        "white": (255, 255, 255), "black": (0, 0, 0), "red": (255, 0, 0),
        "green": (0, 128, 0), "blue": (0, 0, 255), "yellow": (255, 255, 0),
        "gray": (128, 128, 128), "grey": (128, 128, 128), "orange": (255, 165, 0),
        "navy": (0, 0, 128), "darkblue": (0, 0, 139), "transparent": None,
        "none": None,
    }
    if color_str in named:
        return named[color_str]

    if color_str.startswith("#"):
        h = color_str[1:]
        if len(h) == 3:
            return (int(h[0]*2, 16), int(h[1]*2, 16), int(h[2]*2, 16))
        if len(h) == 6:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    m = re.match(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", color_str)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))

    return None


def relative_luminance(r: int, g: int, b: int) -> float:
    """WCAG 2.1 relative luminance from sRGB values (0-255)."""
    def linearize(v: int) -> float:
        s = v / 255.0
        return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(fg: tuple[int, int, int], bg: tuple[int, int, int]) -> float:
    """WCAG contrast ratio between two colors."""
    l1 = relative_luminance(*fg)
    l2 = relative_luminance(*bg)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def get_numeric(el: etree._Element, attr: str, default: float = 0.0) -> float:
    """Get numeric attribute, stripping units like 'px'."""
    val = el.get(attr)
    if val is None:
        return default
    val = val.strip().rstrip("px").rstrip("pt").rstrip("em")
    try:
        return float(val)
    except ValueError:
        return default


def get_font_size(el: etree._Element) -> float | None:
    """Extract font-size from element attributes or style."""
    fs = el.get("font-size")
    if not fs:
        style = el.get("style", "")
        m = re.search(r"font-size:\s*([\d.]+)", style)
        if m:
            return float(m.group(1))
        return None
    fs = fs.strip().rstrip("px").rstrip("pt")
    try:
        return float(fs)
    except ValueError:
        return None


def get_fill_color(el: etree._Element) -> tuple[int, int, int] | None:
    """Get fill/color from element, checking attributes and inline style."""
    fill = el.get("fill")
    if fill:
        c = parse_color(fill)
        if c:
            return c
    style = el.get("style", "")
    for prop in ("fill", "color"):
        m = re.search(rf"{prop}:\s*([^;]+)", style)
        if m:
            c = parse_color(m.group(1).strip())
            if c:
                return c
    return None


def find_background_color(el: etree._Element, root: etree._Element) -> tuple[int, int, int]:
    """Walk up ancestors to find nearest background fill; default white."""
    parent = el.getparent()
    while parent is not None:
        fill = get_fill_color(parent)
        if fill:
            return fill
        parent = parent.getparent()
    # Check root-level rect (common SVG slide background)
    for child in root:
        tag = etree.QName(child.tag).localname if isinstance(child.tag, str) else ""
        if tag == "rect":
            x = get_numeric(child, "x", 0)
            y = get_numeric(child, "y", 0)
            w = get_numeric(child, "width", 0)
            h = get_numeric(child, "height", 0)
            if w >= 1200 and h >= 680:
                c = get_fill_color(child)
                if c:
                    return c
    return (255, 255, 255)


def check_svg(svg_path: Path) -> list[Issue]:
    """Run all checks on a single SVG file."""
    issues: list[Issue] = []
    slide_name = svg_path.name

    # 1. XML well-formedness
    try:
        tree = etree.parse(str(svg_path))
    except etree.XMLSyntaxError as e:
        issues.append(Issue("FAIL", "xml", f"XML parse error: {e}"))
        return issues
    root = tree.getroot()

    # 2. viewBox check
    vb = root.get("viewBox", "")
    if vb != EXPECTED_VIEWBOX:
        issues.append(Issue("FAIL", "viewBox", f"Expected '{EXPECTED_VIEWBOX}', got '{vb}'"))

    # Gather all elements for remaining checks
    all_elements = list(root.iter())

    # 3. Safe area check
    for el in all_elements:
        tag = etree.QName(el.tag).localname if isinstance(el.tag, str) else ""
        if tag not in ("rect", "text", "foreignObject", "image", "g"):
            continue
        if tag == "g":
            continue
        x = get_numeric(el, "x")
        y = get_numeric(el, "y")
        w = get_numeric(el, "width", 0)
        h = get_numeric(el, "height", 0)
        # Skip full-canvas background rects
        if tag == "rect" and w >= 1200 and h >= 680:
            continue
        eid = el.get("id", tag)
        if x < SAFE_LEFT:
            issues.append(Issue("FAIL", "safe-area", f"{eid}: x={x} < {SAFE_LEFT}"))
        if y < SAFE_TOP:
            issues.append(Issue("FAIL", "safe-area", f"{eid}: y={y} < {SAFE_TOP}"))
        if w > 0 and x + w > SAFE_RIGHT:
            issues.append(Issue("FAIL", "safe-area", f"{eid}: x+w={x+w} > {SAFE_RIGHT}"))
        if h > 0 and y + h > SAFE_BOTTOM:
            issues.append(Issue("FAIL", "safe-area", f"{eid}: y+h={y+h} > {SAFE_BOTTOM}"))

    # 4. Font size check
    for el in all_elements:
        tag = etree.QName(el.tag).localname if isinstance(el.tag, str) else ""
        if tag != "text":
            continue
        fs = get_font_size(el)
        if fs is not None and fs < MIN_FONT_SIZE:
            eid = el.get("id", "text")
            issues.append(Issue("FAIL", "font-size", f"{eid}: font-size={fs} < {MIN_FONT_SIZE}"))

    # 5. Contrast check
    for el in all_elements:
        tag = etree.QName(el.tag).localname if isinstance(el.tag, str) else ""
        if tag != "text":
            continue
        fg = get_fill_color(el)
        if not fg:
            fg = (0, 0, 0)  # default text color
        bg = find_background_color(el, root)
        ratio = contrast_ratio(fg, bg)
        if ratio < MIN_CONTRAST_RATIO:
            eid = el.get("id", "text")
            issues.append(Issue(
                "FAIL", "contrast",
                f"{eid}: ratio={ratio:.2f} < {MIN_CONTRAST_RATIO} "
                f"(fg=#{fg[0]:02x}{fg[1]:02x}{fg[2]:02x} on bg=#{bg[0]:02x}{bg[1]:02x}{bg[2]:02x})"
            ))

    # 6. ID pattern check
    significant_tags = {"rect", "text", "foreignObject", "image", "circle", "ellipse", "path", "polygon"}
    for el in all_elements:
        tag = etree.QName(el.tag).localname if isinstance(el.tag, str) else ""
        if tag not in significant_tags:
            continue
        # Skip background rects
        if tag == "rect":
            w = get_numeric(el, "width", 0)
            h = get_numeric(el, "height", 0)
            if w >= 1200 and h >= 680:
                continue
        eid = el.get("id")
        if not eid:
            # Compute a positional hint
            x = get_numeric(el, "x")
            y = get_numeric(el, "y")
            issues.append(Issue("WARN", "id-missing", f"<{tag}> at ({x},{y}) has no id"))
        elif not ID_PATTERN.match(eid):
            issues.append(Issue("WARN", "id-pattern", f"id='{eid}' doesn't match s{{nn}}-{{role}}"))

    # 7. Card gap check
    rects: list[tuple[str, float, float, float, float]] = []
    for el in all_elements:
        tag = etree.QName(el.tag).localname if isinstance(el.tag, str) else ""
        if tag != "rect":
            continue
        w = get_numeric(el, "width", 0)
        h = get_numeric(el, "height", 0)
        if w >= 1200 and h >= 680:
            continue
        if w < 50 or h < 50:
            continue
        eid = el.get("id", "rect")
        x = get_numeric(el, "x")
        y = get_numeric(el, "y")
        rects.append((eid, x, y, w, h))

    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            id_a, xa, ya, wa, ha = rects[i]
            id_b, xb, yb, wb, hb = rects[j]
            # Horizontal gap (same row, overlapping vertically)
            v_overlap = not (ya + ha <= yb or yb + hb <= ya)
            if v_overlap:
                h_gap = max(xb - (xa + wa), xa - (xb + wb))
                if 0 < h_gap < MIN_CARD_GAP:
                    issues.append(Issue(
                        "FAIL", "card-gap",
                        f"{id_a} <-> {id_b}: horizontal gap={h_gap:.0f}px < {MIN_CARD_GAP}"
                    ))
            # Vertical gap (same column, overlapping horizontally)
            h_overlap = not (xa + wa <= xb or xb + wb <= xa)
            if h_overlap:
                v_gap = max(yb - (ya + ha), ya - (yb + hb))
                if 0 < v_gap < MIN_CARD_GAP:
                    issues.append(Issue(
                        "FAIL", "card-gap",
                        f"{id_a} <-> {id_b}: vertical gap={v_gap:.0f}px < {MIN_CARD_GAP}"
                    ))

    return issues


def check_manifest_consistency(
    slides_dir: Path, manifest_path: Path, slide_issues: dict[str, list[Issue]]
) -> list[Issue]:
    """Verify manifest text content matches SVG element text."""
    issues: list[Issue] = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        issues.append(Issue("FAIL", "manifest", f"Cannot read manifest: {e}"))
        return issues

    for slide_entry in manifest.get("slides", []):
        svg_file = slide_entry.get("svg_file", "")
        svg_path = slides_dir / svg_file
        if not svg_path.exists():
            issues.append(Issue("FAIL", "manifest", f"SVG not found: {svg_file}"))
            continue
        try:
            tree = etree.parse(str(svg_path))
        except etree.XMLSyntaxError:
            continue
        root = tree.getroot()

        for elem_entry in slide_entry.get("elements", []):
            eid = elem_entry.get("id")
            expected_text = elem_entry.get("text", "").strip()
            if not eid or not expected_text:
                continue
            found = root.xpath(f"//*[@id='{eid}']")
            if not found:
                issues.append(Issue("WARN", "manifest", f"{svg_file}: id='{eid}' not found in SVG"))
                continue
            actual_text = "".join(found[0].itertext()).strip()
            if actual_text != expected_text:
                issues.append(Issue(
                    "WARN", "manifest",
                    f"{svg_file}: id='{eid}' text mismatch: "
                    f"manifest='{expected_text[:40]}...' vs svg='{actual_text[:40]}...'"
                ))
    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Automated SVG quality checks.")
    parser.add_argument("slides_dir", type=Path, help="Directory containing slide SVGs")
    parser.add_argument(
        "--manifest", type=Path, default=None,
        help="Optional manifest.json for content consistency check",
    )
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

    all_issues: dict[str, list[Issue]] = {}
    total_fail = 0
    total_warn = 0

    for svg_path in svg_files:
        issues = check_svg(svg_path)
        all_issues[svg_path.name] = issues
        total_fail += sum(1 for i in issues if i.severity == "FAIL")
        total_warn += sum(1 for i in issues if i.severity == "WARN")

    # Manifest check
    manifest_issues: list[Issue] = []
    if args.manifest:
        manifest_issues = check_manifest_consistency(args.slides_dir, args.manifest, all_issues)
        total_fail += sum(1 for i in manifest_issues if i.severity == "FAIL")
        total_warn += sum(1 for i in manifest_issues if i.severity == "WARN")

    # Output results
    print(f"\n{'='*60}")
    print(f"SVG Quality Report: {len(svg_files)} slides")
    print(f"{'='*60}\n")

    for svg_name, issues in all_issues.items():
        fails = [i for i in issues if i.severity == "FAIL"]
        warns = [i for i in issues if i.severity == "WARN"]
        status = "PASS" if not fails else "FAIL"
        marker = "  " if status == "PASS" else "X "
        warn_str = f" ({len(warns)} warnings)" if warns else ""
        print(f"[{marker}] {svg_name}: {status}{warn_str}")
        for issue in issues:
            prefix = "FAIL" if issue.severity == "FAIL" else "WARN"
            print(f"     [{prefix}] {issue.check}: {issue.message}")

    if manifest_issues:
        print(f"\n--- Manifest Consistency ---")
        for issue in manifest_issues:
            prefix = "FAIL" if issue.severity == "FAIL" else "WARN"
            print(f"  [{prefix}] {issue.check}: {issue.message}")

    print(f"\n{'='*60}")
    print(f"Summary: {total_fail} failures, {total_warn} warnings across {len(svg_files)} slides")
    if total_fail == 0:
        print("Result: ALL CHECKS PASSED")
    else:
        print("Result: CHECKS FAILED")
    print(f"{'='*60}\n")

    sys.exit(1 if total_fail > 0 else 0)


if __name__ == "__main__":
    main()
