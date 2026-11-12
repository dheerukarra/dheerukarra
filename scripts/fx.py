"""Reusable SMIL effects: typewriter text and a simple counter of unique ids."""
from lib import *

_uid = [0]


def uid(prefix="c"):
    _uid[0] += 1
    return f"{prefix}{_uid[0]}"


def typed(x, y, text, start, total, color=WHITE, size=14, cps=16, font=None, weight=None, keep=True):
    """Typewriter line revealed char by char with a clip rect (discrete steps).
    Returns (defs, body). `start` is seconds into a `total`-second loop; the line clears when the loop restarts."""
    font = font or MONO
    cw = size * 0.6
    cid = uid("t")
    kt, vals = [0.0], [0]
    for i in range(1, len(text) + 1):
        kt.append(min(0.999, (start + i / cps) / total))
        vals.append(n(i * cw, 1))
    defs = (
        f'<clipPath id="{cid}"><rect x="{n(x)}" y="{n(y - size)}" width="0" height="{n(size * 1.5)}">'
        f'{A("width", vals, total, keytimes=kt, calc="discrete")}</rect></clipPath>'
    )
    w = f' font-weight="{weight}"' if weight else ""
    body = (
        f'<g clip-path="url(#{cid})"><text x="{n(x)}" y="{n(y)}" font-family="{font}" font-size="{size}" fill="{color}"{w} '
        f'textLength="{n(len(text) * cw)}" lengthAdjust="spacingAndGlyphs" xml:space="preserve">{esc(text)}</text></g>'
    )
    return defs, body


def blink(x, y, h, color, total=1.1, w=8):
    return f'<rect x="{n(x)}" y="{n(y)}" width="{w}" height="{h}" fill="{color}">{A("opacity", "1;1;0;0", total, keytimes=[0, .5, .5, 1], calc="discrete")}</rect>'


def fade_in(body, begin, dur=0.6, rise=10):
    """Wrap `body` so it fades/slides in once at `begin` seconds and stays."""
    return (
        f'<g opacity="0">{body}{A("opacity", "0;1", dur, begin=f"{begin}s", fill="freeze", repeat=None)}'
        f'{AT("translate", f"0 {rise};0 0", dur, begin=f"{begin}s", fill="freeze", repeat=None, calc="spline", keytimes=[0, 1], splines=".16 1 .3 1")}</g>'
    )
