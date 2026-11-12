"""Shared helpers for generating the animated SVG assets of the profile README.

Everything is plain SVG + SMIL (no scripts, no external fonts or images), so it renders
inside a GitHub <img> tag. Run `python3 scripts/build.py` to regenerate ./assets.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "assets"))
os.makedirs(OUT, exist_ok=True)
ICONS = json.load(open(os.path.join(HERE, "icons.json")))

# palette: "magma on ink" (deep purple -> magenta -> peach, one ice-blue counter accent)
BG = "#070512"
PANEL = "#0e0a22"
WHITE = "#fbf1de"      # cream, used for text
PEACH = "#fe9f6d"
CORAL = "#f1605d"
MAGENTA = "#de4968"
PLUM = "#8c2981"
VIOLET = "#a58bff"
ICE = "#6fd3ff"
LIME = "#8de0a6"
GOLD = "#fcd35c"
RED = "#ff5c6c"
MUTED = "#a59cc0"
DIM = "#6f6890"

# magma-like colour ramp for height / depth maps (t in 0..1)
_MAGMA = [(0.0, (7, 5, 18)), (0.18, (40, 12, 84)), (0.36, (96, 22, 112)), (0.52, (156, 42, 104)),
          (0.68, (222, 73, 104)), (0.82, (254, 159, 109)), (1.0, (252, 253, 191))]


def magma(t):
    t = max(0.0, min(1.0, t))
    for (t0, c0), (t1, c1) in zip(_MAGMA, _MAGMA[1:]):
        if t <= t1:
            u = (t - t0) / (t1 - t0)
            return "#%02x%02x%02x" % tuple(int(round(a + (b - a) * u)) for a, b in zip(c0, c1))
    return "#fcfdbf"

MONO = "ui-monospace,'SFMono-Regular','Cascadia Code',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "'Segoe UI',system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif"


def n(x, d=1):
    s = f"{x:.{d}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(name, w, h, body, defs="", title="", radius=18):
    s = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
        f'<defs>{defs}<clipPath id="rc"><rect width="{w}" height="{h}" rx="{radius}"/></clipPath></defs>'
        f'<g clip-path="url(#rc)">{body}</g></svg>'
    )
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(s)
    print(f"{name}: {len(s) / 1024:.0f} KB")
    return path


def A(attr, values, dur, begin="0s", keytimes=None, calc=None, repeat="indefinite", fill=None, splines=None):
    """<animate>. `values` may be a list (joined by ;) or a string."""
    v = values if isinstance(values, str) else ";".join(str(x) for x in values)
    s = f'<animate attributeName="{attr}" values="{v}" dur="{dur}s" begin="{begin}"'
    if repeat:
        s += f' repeatCount="{repeat}"'
    if keytimes:
        s += f' keyTimes="{";".join(n(k, 4) for k in keytimes)}"'
    if calc:
        s += f' calcMode="{calc}"'
    if splines:
        s += f' keySplines="{splines}"'
    if fill:
        s += f' fill="{fill}"'
    return s + "/>"


def AT(kind, values, dur, begin="0s", keytimes=None, calc=None, repeat="indefinite", fill=None, splines=None):
    """<animateTransform>."""
    v = values if isinstance(values, str) else ";".join(str(x) for x in values)
    s = f'<animateTransform attributeName="transform" type="{kind}" values="{v}" dur="{dur}s" begin="{begin}"'
    if repeat:
        s += f' repeatCount="{repeat}"'
    if keytimes:
        s += f' keyTimes="{";".join(n(k, 4) for k in keytimes)}"'
    if calc:
        s += f' calcMode="{calc}"'
    if splines:
        s += f' keySplines="{splines}"'
    if fill:
        s += f' fill="{fill}"'
    return s + "/>"


def window(start, end, total, fade=0.02):
    """keyTimes/values for an opacity that is 1 between start..end (seconds) of a `total`-second loop."""
    s, e = start / total, end / total
    kt = [0.0]
    vals = [0]
    if s > 0:
        kt.append(s)
        vals.append(0)
    kt.append(min(1.0, s + fade))
    vals.append(1)
    kt.append(max(s + fade, e - fade))
    vals.append(1)
    kt.append(e)
    vals.append(0)
    if e < 1.0:
        kt.append(1.0)
        vals.append(0)
    # strictly increasing key times
    out_k, out_v = [], []
    for k, v in zip(kt, vals):
        if out_k and k <= out_k[-1]:
            k = out_k[-1] + 1e-4
        out_k.append(k)
        out_v.append(v)
    return out_k, out_v


def icon(slug, x, y, size, fill=WHITE, opacity=1):
    ic = ICONS.get(slug)
    if not ic:
        return ""
    sc = size / 24
    return f'<path transform="translate({n(x)} {n(y)}) scale({n(sc, 3)})" d="{ic["path"]}" fill="{fill}" opacity="{opacity}"/>'


def sphere_points(count):
    """Fibonacci sphere: evenly spread unit vectors."""
    pts = []
    ga = math.pi * (3 - math.sqrt(5))
    for i in range(count):
        y = 1 - 2 * (i + 0.5) / count
        rad = math.sqrt(1 - y * y)
        th = ga * i
        pts.append((math.cos(th) * rad, y, math.sin(th) * rad))
    return pts


def rot(p, yaw=0.0, tilt_z=0.0, view_x=0.0):
    """Rotate about Y (spin), Z (axis tilt) then X (camera looks slightly from above). +z points at the viewer."""
    x, y, z = p
    c, s = math.cos(yaw), math.sin(yaw)
    x, z = c * x + s * z, -s * x + c * z
    c, s = math.cos(tilt_z), math.sin(tilt_z)
    x, y = c * x - s * y, s * x + c * y
    c, s = math.cos(view_x), math.sin(view_x)
    y, z = c * y - s * z, s * y + c * z
    return x, y, z


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def pill(x, y, text, color, size=13, pad=14, h=26, char_w=None, fill_op=0.10):
    """Outlined mono pill; returns (svg, width)."""
    cw = char_w or size * 0.62
    w = len(text) * cw + pad * 2
    tl = len(text) * cw
    s = (
        f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{h}" rx="{h / 2}" fill="{color}" fill-opacity="{fill_op}" '
        f'stroke="{color}" stroke-opacity=".7"/>'
        f'<text x="{n(x + pad)}" y="{n(y + h / 2 + size * 0.35)}" font-family="{MONO}" font-size="{size}" fill="{color}" '
        f'textLength="{n(tl)}" lengthAdjust="spacingAndGlyphs">{esc(text)}</text>'
    )
    return s, w
