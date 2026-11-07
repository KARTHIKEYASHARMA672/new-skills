#!/usr/bin/env python3
"""animated-aws-arch — render a light-theme, left-to-right, animated AWS
architecture SVG from a JSON spec.

Usage:
    python3 gen_arch.py spec.json out.svg

The SVG is self-contained (official AWS icons inlined, no external assets) and
animates via CSS marching-ants dashes + SMIL traveling dots. See ../SKILL.md for
the spec schema, layout conventions, and the render/verify loop.
"""
import json, re, sys, pathlib

ICON_DIR = pathlib.Path(__file__).resolve().parent.parent / "icons"

# --- theme -----------------------------------------------------------------
BG = "#FBFCFE"; GRID = "#EAEFF6"; INK = "#16202E"; SUB = "#5A6B7B"
FLOW = {  # flow-name -> color
    "request": "#1D4ED8", "reply": "#0F766E", "schedule": "#15803D",
    "ambient": "#7E22CE", "garden": "#B45309", "tool": "#0369A1", "aux": "#94A3B8",
}
FLOW_LABEL = {"request": "request →", "reply": "reply ←", "schedule": "scheduling",
              "ambient": "ambient", "garden": "gardening", "tool": "tools/memory", "aux": "aux"}
GROUP_STYLE = {  # kind -> (stroke, dash, fill, label-color)
    "region": ("#00A4A6", "9 5", "rgba(0,164,166,0.045)", "#0B7E7F"),
    "subnet": ("#8C4FFF", "6 4", "rgba(140,79,255,0.06)", "#7C3AED"),
    "event":  ("#E7157B", "3 4", "rgba(231,21,123,0.04)", "#B21667"),
}
# gradient (older) icons flattened to their flat AWS category color to match the
# newer flat squid icons. Icons not listed keep their native fill (fine either way).
FLATTEN = {
    "eventbridge": "#E7157B", "secretsmanager": "#DD344C", "sqs": "#E7157B",
    "sns": "#E7157B", "stepfunctions": "#E7157B", "ses": "#E7157B", "connect": "#E7157B",
    "kms": "#DD344C", "iam": "#DD344C", "cognito": "#DD344C", "guardduty": "#DD344C", "waf": "#DD344C",
    "vpc": "#8C4FFF", "route53": "#8C4FFF", "elb": "#8C4FFF", "nat": "#8C4FFF",
    "igw": "#8C4FFF", "endpoints": "#8C4FFF", "peering": "#8C4FFF", "networkfirewall": "#8C4FFF",
    "ec2": "#ED7100", "ecs": "#ED7100", "eks": "#ED7100", "autoscaling": "#ED7100",
    "rds": "#C925D1", "sagemaker": "#01A88D",
}

# --- official-icon loader (namespace ids so multiple inline icons don't clash) --
def load_icon(key):
    txt = (ICON_DIR / f"{key}.svg").read_text()
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', txt)
    vw = float(m.group(1)) if m else 64.0
    inner = re.sub(r'<\?xml[^>]*\?>', '', txt)
    inner = re.sub(r'<svg[^>]*>', '', inner, count=1).rsplit('</svg>', 1)[0]
    inner = re.sub(r'<title>.*?</title>', '', inner, flags=re.S)
    inner = re.sub(r'<desc>.*?</desc>', '', inner, flags=re.S)
    inner = re.sub(r'<!--.*?-->', '', inner, flags=re.S)
    for i in sorted(set(re.findall(r'id="([^"]+)"', inner)), key=len, reverse=True):
        n = f'{key}__{i}'
        inner = inner.replace(f'id="{i}"', f'id="{n}"').replace(f'url(#{i})', f'url(#{n})').replace(f'href="#{i}"', f'href="#{n}"')
    if key in FLATTEN:
        inner = re.sub(r'fill="url\(#' + re.escape(key) + r'__[^"]+\)"', f'fill="{FLATTEN[key]}"', inner, count=1)
    return inner, vw

# --- non-AWS tiles (glyph on a flat rounded tile) --------------------------
def _bubble(cx, cy):
    return (f'<path d="M{cx-13} {cy-9} h26 a4 4 0 0 1 4 4 v11 a4 4 0 0 1 -4 4 h-15 l-7 6 v-6 h-4 a4 4 0 0 1 -4 -4 v-11 a4 4 0 0 1 4 -4 z" fill="#fff"/>'
            + "".join(f'<circle cx="{cx-6+6*k}" cy="{cy+1}" r="1.8" fill="#fff" opacity="0.001"/>' for k in range(3))
            + f'<circle cx="{cx-6}" cy="{cy+1}" r="1.7" fill="#00998C"/><circle cx="{cx}" cy="{cy+1}" r="1.7" fill="#00998C"/><circle cx="{cx+6}" cy="{cy+1}" r="1.7" fill="#00998C"/>')
def _gateway(cx, cy):
    return f'<path d="M{cx-11} {cy-8} l9 8 l-9 8 M{cx-1} {cy-8} l9 8 l-9 8" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
def _search(cx, cy):
    return (f'<circle cx="{cx-3}" cy="{cy-3}" r="8" fill="none" stroke="#fff" stroke-width="2.6"/>'
            f'<line x1="{cx+3}" y1="{cy+3}" x2="{cx+10}" y2="{cy+10}" stroke="#fff" stroke-width="2.8" stroke-linecap="round"/>')
def _dot(cx, cy):
    return f'<circle cx="{cx}" cy="{cy}" r="7" fill="none" stroke="#fff" stroke-width="2.4"/><circle cx="{cx}" cy="{cy}" r="1.8" fill="#fff"/>'
TILE = {"lark": ("#00B5A5", _bubble), "gateway": ("#4F46E5", _gateway),
        "external": ("#475569", _search), "generic": ("#64748B", _dot)}

def draw_node(n):
    cx, cy = n["x"], n["y"]; ic = n["icon"]; sz = 46
    if ic.startswith("tile:"):
        fill, gl = TILE[ic.split(":", 1)[1]]
        x, y = cx - sz/2, cy - sz/2
        body = f'<rect x="{x:.1f}" y="{y:.1f}" width="{sz}" height="{sz}" rx="8" fill="{fill}"/>' + gl(cx, cy)
    else:
        inner, vw = load_icon(ic); s = sz/vw
        body = f'<g transform="translate({cx-sz/2:.2f},{cy-sz/2:.2f}) scale({s:.4f})">{inner}</g>'
    t = f'<text x="{cx}" y="{cy+38}" text-anchor="middle" font-size="13" font-weight="700" fill="{INK}">{n["label"]}</text>'
    if n.get("sub"):
        t += f'<text x="{cx}" y="{cy+51}" text-anchor="middle" font-size="9.5" fill="{SUB}">{n["sub"]}</text>'
    return body + t

# --- geometry --------------------------------------------------------------
def render(spec):
    N = {n["id"]: n for n in spec["nodes"]}
    W = spec.get("canvas", {}).get("w", 1480); H = spec.get("canvas", {}).get("h", 900)

    def anch(nid, side):
        n = N[nid]; cx, cy = n["x"], n["y"]; h = 23
        return {"t": (cx, cy-h), "b": (cx, cy+h), "l": (cx-h, cy), "r": (cx+h, cy)}[side]

    def path_of(e):
        pts = [anch(e["from"], e.get("fs", "r"))] + [tuple(p) for p in e.get("mids", [])] + [anch(e["to"], e.get("ts", "l"))]
        return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)

    EP = {(e["from"], e["to"]): path_of(e) for e in spec["edges"]}
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
             f'font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',Helvetica,Arial,sans-serif" '
             f'role="img" aria-label="{spec.get("title","architecture")}">')
    o.append(f'<title>{spec.get("title","")}</title>')
    o.append('<defs>')
    o.append(f'<pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse"><path d="M34 0 H0 V34" fill="none" stroke="{GRID}" stroke-width="1"/></pattern>')
    o.append('<marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1 L9 5 L1 9" fill="none" stroke="context-stroke" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></marker>')
    o.append('<style>@media (prefers-reduced-motion: no-preference){'
             '.flow{stroke-dasharray:6 6;animation:dm .8s linear infinite}}'
             '@keyframes dm{to{stroke-dashoffset:-12}}</style>')
    o.append('</defs>')
    o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#grid)"/>')
    if spec.get("title"):
        o.append(f'<text x="40" y="46" font-size="21" font-weight="800" fill="{INK}">{spec["title"]}</text>')
    if spec.get("subtitle"):
        o.append(f'<text x="40" y="68" font-size="12" fill="{SUB}">{spec["subtitle"]}</text>')

    # groups
    for g in spec.get("groups", []):
        st, dash, fill, lc = GROUP_STYLE[g["kind"]]
        o.append(f'<rect x="{g["x"]}" y="{g["y"]}" width="{g["w"]}" height="{g["h"]}" rx="12" fill="{fill}" stroke="{st}" stroke-width="1.5" stroke-dasharray="{dash}"/>')
        lx = g.get("lx", g["x"] + 18)
        ly = g["y"] + g["h"] - 10 if g.get("labelPos") == "bottom" else g["y"] + 20
        ly = g.get("ly", ly)
        o.append(f'<text x="{lx}" y="{ly}" font-size="11" font-weight="700" fill="{lc}">{g["label"]}</text>')

    # edges + labels
    for e in spec["edges"]:
        c = FLOW[e["flow"]]; d = EP[(e["from"], e["to"])]
        if e.get("static"):
            o.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="1.4" stroke-dasharray="2 5" opacity="0.7"/>')
        else:
            o.append(f'<path class="flow" d="{d}" fill="none" stroke="{c}" stroke-width="2" marker-end="url(#ah)"/>')
    for e in spec["edges"]:
        if e.get("label") and e.get("lxy"):
            lx, ly = e["lxy"]; w = 6.6*len(e["label"]) + 8
            o.append(f'<rect x="{lx-w/2:.0f}" y="{ly-10:.0f}" width="{w:.0f}" height="14" rx="3" fill="{BG}" opacity="0.92"/>')
            o.append(f'<text x="{lx}" y="{ly}" text-anchor="middle" font-size="9.5" fill="#48586a">{e["label"]}</text>')

    # traveling dots (journeys)
    for jn in spec.get("journeys", []):
        c = FLOW[jn["flow"]]; dur = jn.get("dur", 2.4); rev = jn.get("reverse", False)
        hops = jn["hops"]; r = 3.4 if rev else 4
        for j, (a, b) in enumerate(hops):
            d = EP.get((a, b))
            if not d:  # allow reverse hops that reuse a forward edge drawn the other way
                d = EP.get((b, a))
            if not d:
                continue
            beg = f'{j*dur/len(hops):.2f}s'
            kp = ' keyPoints="1;0" keyTimes="0;1" calcMode="linear"' if rev else ''
            o.append(f'<circle r="{r}" fill="{c}"><animateMotion dur="{dur}s" begin="{beg}" repeatCount="indefinite"{kp} path="{d}"/></circle>')

    # nodes
    for n in spec["nodes"]:
        o.append(draw_node(n))

    # numbered step badges on spine edges
    for a, b, num in spec.get("steps", []):
        (x0, y0), (x1, y1) = anch(a, "r"), anch(b, "l")
        mx, my = (x0+x1)/2, (y0+y1)/2
        o.append(f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="9" fill="#232F3E"/>'
                 f'<text x="{mx:.0f}" y="{my+3.4:.0f}" text-anchor="middle" font-size="10.5" font-weight="700" fill="#fff">{num}</text>')

    # legend (bottom-left)
    leg = spec.get("legend", [])
    if leg:
        ly = spec.get("legendY", H - 94); lx = 40
        o.append(f'<text x="{lx}" y="{ly+4}" font-size="11" font-weight="700" fill="{INK}">Flows</text>'); lx += 52
        for f in leg:
            txt = FLOW_LABEL.get(f, f)
            o.append(f'<circle cx="{lx}" cy="{ly}" r="5" fill="{FLOW[f]}"/><text x="{lx+10}" y="{ly+4}" font-size="10.5" fill="{SUB}">{txt}</text>')
            lx += 30 + 7*len(txt)
    if spec.get("footer"):
        o.append(f'<text x="40" y="{(spec.get("legendY", H-94))+26}" font-size="10" fill="{SUB}">{spec["footer"]}</text>')

    o.append('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: gen_arch.py spec.json out.svg")
    spec = json.loads(pathlib.Path(sys.argv[1]).read_text())
    pathlib.Path(sys.argv[2]).write_text(render(spec))
    print(f"wrote {sys.argv[2]}  ({len(spec['nodes'])} nodes, {len(spec['edges'])} edges)")
