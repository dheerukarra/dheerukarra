"""Four project cards, one per real repo: jobai, dheeraj-aws-portfolio, polybot, python-learning-platform.
Every claim on a card comes from that repo's own README."""
import math
import random

from fx import *
from lib import *

CW, CH = 620, 360
SX, SY, SW, SH = 22, 58, 576, 160


def frame(name, repo, chip, chip_col, desc, tags, scene_defs, scene_body, title):
    defs = (
        f'<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{PEACH}" stop-opacity=".75"/>'
        f'<stop offset=".5" stop-color="{PLUM}" stop-opacity=".25"/><stop offset="1" stop-color="{ICE}" stop-opacity=".55"/></linearGradient>'
        f'<linearGradient id="scbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#120b2b"/><stop offset="1" stop-color="{BG}"/></linearGradient>'
        f'<clipPath id="sc"><rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="12"/></clipPath>' + scene_defs
    )
    b = [f'<rect x="1" y="1" width="{CW - 2}" height="{CH - 2}" rx="18" fill="{PANEL}" stroke="url(#edge)" stroke-width="1.5"/>']
    b.append(
        f'<text x="24" y="37" font-family="{MONO}" font-size="17" fill="{DIM}" textLength="{n(11 * 10.2)}" lengthAdjust="spacingAndGlyphs">dheerukarra</text>'
        f'<text x="{n(24 + 11 * 10.2 + 8)}" y="37" font-family="{MONO}" font-size="17" fill="{DIM}">/</text>'
        f'<text x="{n(24 + 11 * 10.2 + 28)}" y="37" font-family="{MONO}" font-size="17" font-weight="700" fill="{WHITE}" textLength="{n(len(repo) * 10.2)}" lengthAdjust="spacingAndGlyphs">{esc(repo)}</text>'
    )
    p, w = pill(0, 0, chip, chip_col, size=11, pad=12, h=24)
    b.append(f'<g transform="translate({n(CW - 24 - w)} 17)">{p}</g>')
    b.append(f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="12" fill="url(#scbg)" stroke="{WHITE}" stroke-opacity=".08"/>')
    for gx in range(SX + 24, SX + SW, 24):
        b.append(f'<line x1="{gx}" y1="{SY}" x2="{gx}" y2="{SY + SH}" stroke="{WHITE}" stroke-opacity=".025"/>')
    for gy in range(SY + 20, SY + SH, 20):
        b.append(f'<line x1="{SX}" y1="{gy}" x2="{SX + SW}" y2="{gy}" stroke="{WHITE}" stroke-opacity=".025"/>')
    b.append(f'<g clip-path="url(#sc)"><g transform="translate({SX} {SY})">{scene_body}</g></g>')
    for i, line in enumerate(desc):
        b.append(
            f'<text x="24" y="{246 + i * 22}" font-family="{SANS}" font-size="14" fill="{WHITE if i == 0 else MUTED}" fill-opacity="{1 if i == 0 else .86}" '
            f'textLength="{n(len(line) * 6.85)}" lengthAdjust="spacingAndGlyphs">{esc(line)}</text>'
        )
    x = 24
    for i, t in enumerate(tags):
        col = (PEACH, ICE, LIME, VIOLET)[i % 4]
        p, w = pill(x, 316, t, col, size=11, pad=11, h=24)
        b.append(p)
        x += w + 8
    return svg(name, CW, CH, "".join(b), defs, title)


# ------------------------------------------------------------------ jobai
def scene_jobai():
    T = 6.5
    stages = [("DISCOVER", "SQLite dedupe", True), ("LLM GATEWAY", "caps · kill switch", True), ("SCORE", "planned", False), ("TAILOR", "planned", False), ("REVIEW", "planned", False)]
    xs = [64 + i * 112 for i in range(5)]
    y = 62
    b = []
    for (label, sub, on), cx in zip(stages, xs):
        top = f"{cx},{y - 16} {cx + 46},{y} {cx},{y + 16} {cx - 46},{y}"
        left = f"{cx - 46},{y} {cx},{y + 16} {cx},{y + 26} {cx - 46},{y + 10}"
        right = f"{cx},{y + 16} {cx + 46},{y} {cx + 46},{y + 10} {cx},{y + 26}"
        if on:
            b.append(f'<polygon points="{left}" fill="{LIME}" fill-opacity=".14" stroke="{LIME}" stroke-opacity=".5"/>')
            b.append(f'<polygon points="{right}" fill="{LIME}" fill-opacity=".22" stroke="{LIME}" stroke-opacity=".5"/>')
            b.append(f'<polygon points="{top}" fill="{LIME}" fill-opacity=".20" stroke="{LIME}">{A("fill-opacity", ".14;.45;.14", 2.6, begin=f"{n(cx / 400, 2)}s")}</polygon>')
            col = LIME
        else:
            b.append(f'<polygon points="{top}" fill="none" stroke="{DIM}" stroke-dasharray="4 4"/>')
            b.append(f'<path d="M{cx - 46} {y}V{y + 10}L{cx} {y + 26}L{cx + 46} {y + 10}V{y}" fill="none" stroke="{DIM}" stroke-opacity=".55" stroke-dasharray="3 4"/>')
            col = DIM
        b.append(f'<text x="{cx}" y="{y + 50}" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" fill="{col}" textLength="{n(len(label) * 6.9)}" lengthAdjust="spacingAndGlyphs">{label}</text>')
        b.append(f'<text x="{cx}" y="{y + 65}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{col}" fill-opacity=".8" textLength="{n(len(sub) * 6)}" lengthAdjust="spacingAndGlyphs">{sub}</text>')
    # job cards travel to the first planned stage and dissolve there
    stop = xs[2] - 18
    for i in range(5):
        begin = f"{n(-i * 1.3, 1)}s"
        b.append(
            f'<g opacity="0"><g>'
            f'<rect x="-11" y="-8" width="22" height="16" rx="3" fill="{WHITE}" fill-opacity=".95"/>'
            f'<rect x="-7" y="-4" width="10" height="2.4" rx="1" fill="{PLUM}"/><rect x="-7" y="1" width="14" height="2.4" rx="1" fill="{DIM}"/>'
            f'{AT("translate", f"14 {y - 42};14 {y - 42};{stop} {y - 42};{stop} {y - 42}", T, begin=begin, keytimes=[0, 0.02, 0.5, 1])}'
            f'</g>{A("opacity", "0;1;1;0;0", T, begin=begin, keytimes=[0, 0.04, 0.50, 0.58, 1])}</g>'
        )
    b.append(f'<text x="{xs[2]}" y="{y - 52}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{DIM}" textLength="90" lengthAdjust="spacingAndGlyphs">not built yet</text>')
    return "", "".join(b)


# ------------------------------------------------------------------ portfolio
def scene_portfolio():
    F, SPIN = 36, 14
    phi = (1 + 5 ** 0.5) / 2
    nrm = math.sqrt(1 + phi * phi)
    V = [tuple(c / nrm for c in v) for v in [(0, 1, phi), (0, -1, phi), (0, 1, -phi), (0, -1, -phi), (1, phi, 0), (-1, phi, 0), (1, -phi, 0), (-1, -phi, 0), (phi, 0, 1), (-phi, 0, 1), (phi, 0, -1), (-phi, 0, -1)]]
    E = [(i, j) for i in range(12) for j in range(i + 1, 12) if abs(math.dist(V[i], V[j]) - 2 / nrm) < 1e-6]
    cx, cy, R = 170, 96, 40
    b = [
        f'<rect x="22" y="14" width="296" height="134" rx="10" fill="#0b0720" stroke="{WHITE}" stroke-opacity=".18"/>'
        f'<path d="M22 24a10 10 0 0 1 10-10h276a10 10 0 0 1 10 10v8H22z" fill="{WHITE}" fill-opacity=".07"/>'
        f'<circle cx="36" cy="24" r="3" fill="{CORAL}"/><circle cx="47" cy="24" r="3" fill="{GOLD}"/><circle cx="58" cy="24" r="3" fill="{LIME}"/>'
        f'<text x="76" y="27.5" font-family="{MONO}" font-size="9" fill="{DIM}" textLength="196" lengthAdjust="spacingAndGlyphs">main.d20iokpmvk0ua7.amplifyapp.com</text>'
        f'<circle cx="{cx}" cy="{cy}" r="52" fill="{PLUM}" fill-opacity=".22"/>'
    ]
    proj = [[(cx + R * x, cy - R * y, z) for x, y, z in (rot(v, 2 * math.pi * k / F, math.radians(10), 0.5) for v in V)] for k in range(F + 1)]
    for a, c in E:
        ds = [f"M{n(proj[k][a][0])} {n(proj[k][a][1])}L{n(proj[k][c][0])} {n(proj[k][c][1])}" for k in range(F + 1)]
        ops = [n(0.15 + 0.85 * clamp((proj[k][a][2] + proj[k][c][2]) / 2 + 0.5), 2) for k in range(F + 1)]
        col = PEACH if (a + c) % 3 else MAGENTA
        b.append(f'<path d="{ds[0]}" fill="none" stroke="{col}" stroke-width="1.3" stroke-linecap="round">{A("d", ds, SPIN)}{A("stroke-opacity", ops, SPIN)}</path>')
    for i in range(12):
        xs = [n(proj[k][i][0]) for k in range(F + 1)]
        ys = [n(proj[k][i][1]) for k in range(F + 1)]
        rs = [n(1.2 + 1.8 * clamp((proj[k][i][2] + 1) / 2), 2) for k in range(F + 1)]
        b.append(f'<circle cx="{xs[0]}" cy="{ys[0]}" r="2" fill="{WHITE}">{A("cx", xs, SPIN)}{A("cy", ys, SPIN)}{A("r", rs, SPIN)}</circle>')
    b.append(f'<text x="34" y="140" font-family="{MONO}" font-size="9" fill="{ICE}" textLength="150" lengthAdjust="spacingAndGlyphs">three.js · 12 interactive scenes</text>')
    # deploy path: git push -> Amplify -> live
    nodes = [(366, 66, "github", "git push", WHITE), (458, 66, "awsamplify", "Amplify", PEACH), (550, 66, None, "live", LIME)]
    for (x1, y1, *_), (x2, y2, *_) in zip(nodes, nodes[1:]):
        b.append(f'<line x1="{x1 + 22}" y1="{y1}" x2="{x2 - 22}" y2="{y2}" stroke="{WHITE}" stroke-opacity=".3" stroke-dasharray="3 4"/>')
        for off in (0, 1.2):
            b.append(
                f'<circle r="3.2" fill="{PEACH}" opacity="0"><animateMotion dur="2.4s" begin="{off}s" repeatCount="indefinite" path="M{x1 + 22} {y1}L{x2 - 22} {y2}"/>'
                f'{A("opacity", "0;1;1;0", 2.4, begin=f"{off}s", keytimes=[0, .1, .9, 1])}</circle>'
            )
    for x, y, slug, label, col in nodes:
        b.append(f'<circle cx="{x}" cy="{y}" r="20" fill="#0b0720" stroke="{col}" stroke-opacity=".85" stroke-width="1.4"/>')
        if slug:
            b.append(icon(slug, x - 10, y - 10, 20, WHITE))
        else:
            b.append(f'<path d="M{x - 8} {y}l5.5 6 10.5-12" fill="none" stroke="{LIME}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
        b.append(f'<text x="{x}" y="{y + 38}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{col}" textLength="{n(len(label) * 6.9)}" lengthAdjust="spacingAndGlyphs">{label}</text>')
    b.append(f'<text x="458" y="138" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{MUTED}" textLength="168" lengthAdjust="spacingAndGlyphs">every push to main redeploys</text>')
    return "", "".join(b)


# ------------------------------------------------------------------ polybot
def scene_polybot():
    T = 8.0
    rnd = random.Random(11)
    N = 52
    v, pts = 0.0, []
    for i in range(N):
        v += rnd.uniform(-0.55, 0.62) + 0.03
        pts.append(v)
    lo, hi = min(pts), max(pts)
    X0, Y0, WW, HH = 30, 22, 350, 104
    xy = [(X0 + WW * i / (N - 1), Y0 + HH * (1 - (p - lo) / (hi - lo))) for i, p in enumerate(pts)]
    tot, cum = 0.0, [0.0]
    for a, c in zip(xy, xy[1:]):
        tot += math.dist(a, c)
        cum.append(tot)
    d = "M" + "L".join(f"{n(x)} {n(y)}" for x, y in xy)
    area = d + f"L{n(xy[-1][0])} {Y0 + HH}L{n(xy[0][0])} {Y0 + HH}Z"
    t_end = 6.0
    kt = [0.0] + [(0.2 + (t_end - 0.2) * i / (N - 1)) / T for i in range(N)] + [1.0]
    offs = [n(tot)] + [n(tot - c) for c in cum] + ["0"]
    xs = [n(xy[0][0])] + [n(p[0]) for p in xy] + [n(xy[-1][0])]
    ys = [n(xy[0][1])] + [n(p[1]) for p in xy] + [n(xy[-1][1])]
    defs = (
        f'<linearGradient id="pa" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{PEACH}" stop-opacity=".35"/><stop offset="1" stop-color="{PEACH}" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="pc"><rect x="{X0}" y="{Y0 - 6}" width="0" height="{HH + 12}">{A("width", ["0"] + [n(WW * i / (N - 1)) for i in range(N)] + [n(WW)], T, keytimes=kt)}</rect></clipPath>'
    )
    b = []
    for i in range(5):
        gy = Y0 + HH * i / 4
        b.append(f'<line x1="{X0}" y1="{n(gy)}" x2="{X0 + WW}" y2="{n(gy)}" stroke="{WHITE}" stroke-opacity=".06"/>')
    b.append(f'<g clip-path="url(#pc)"><path d="{area}" fill="url(#pa)"/></g>')
    b.append(f'<path d="{d}" fill="none" stroke="{PEACH}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="{n(tot)}" stroke-dashoffset="{n(tot)}">{A("stroke-dashoffset", offs, T, keytimes=kt)}</path>')
    # scanner beam + head
    b.append(f'<line x1="{xs[0]}" y1="{Y0 - 6}" x2="{xs[0]}" y2="{Y0 + HH + 6}" stroke="{ICE}" stroke-opacity=".6">{A("x1", xs, T, keytimes=kt)}{A("x2", xs, T, keytimes=kt)}</line>')
    b.append(f'<circle r="4.5" fill="{WHITE}" cx="{xs[0]}" cy="{ys[0]}">{A("cx", xs, T, keytimes=kt)}{A("cy", ys, T, keytimes=kt)}</circle>')
    # signals appear as the scanner passes them
    for idx, buy in ((9, True), (22, False), (37, True)):
        px, py = xy[idx]
        tm = 0.2 + (t_end - 0.2) * idx / (N - 1)
        k, vals = window(tm, T - 0.3, T, fade=0.02)
        col = LIME if buy else MAGENTA
        tri = f"{n(px)},{n(py - 15)} {n(px - 6)},{n(py - 5)} {n(px + 6)},{n(py - 5)}" if buy else f"{n(px)},{n(py + 15)} {n(px - 6)},{n(py + 5)} {n(px + 6)},{n(py + 5)}"
        b.append(f'<g opacity="0"><polygon points="{tri}" fill="{col}"/>{A("opacity", vals, T, keytimes=k)}</g>')
    # paper stamp
    b.append(
        f'<g transform="translate(118 44) rotate(-7)" opacity=".92"><rect x="-52" y="-14" width="104" height="26" rx="4" fill="none" stroke="{GOLD}" stroke-width="2"/>'
        f'<text x="0" y="5" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" fill="{GOLD}" letter-spacing="2" textLength="86" lengthAdjust="spacingAndGlyphs">PAPER ONLY</text></g>'
    )
    # pipeline chips
    for i, (label, col) in enumerate((("SCAN MARKETS", ICE), ("SIGNAL", PEACH), ("PAPER TRADE", LIME), ("TELEGRAM ALERT", VIOLET))):
        y = 18 + i * 34
        w = 132
        b.append(
            f'<rect x="418" y="{y}" width="{w}" height="26" rx="13" fill="{col}" fill-opacity=".10" stroke="{col}" stroke-opacity=".7">'
            f'{A("fill-opacity", ".10;.45;.10;.10", 3.2, begin=f"{n(i * 0.55, 2)}s", keytimes=[0, .12, .4, 1])}</rect>'
            f'<text x="{418 + w / 2}" y="{y + 17}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{col}" textLength="{n(len(label) * 6.9)}" lengthAdjust="spacingAndGlyphs">{label}</text>'
        )
        if i < 3:
            b.append(f'<path d="M{418 + w / 2} {y + 26}v8" stroke="{WHITE}" stroke-opacity=".3"/>')
    b.append(f'<text x="484" y="156" text-anchor="middle" font-family="{MONO}" font-size="9.5" fill="{DIM}" textLength="150" lengthAdjust="spacingAndGlyphs">scan every 2-3 minutes</text>')
    return defs, "".join(b)


# ------------------------------------------------------------------ python learning platform
def scene_pylearn():
    T = 10.0
    defs, b = "", []
    b.append(
        f'<rect x="20" y="14" width="318" height="136" rx="10" fill="#0b0720" stroke="{WHITE}" stroke-opacity=".18"/>'
        f'<path d="M20 24a10 10 0 0 1 10-10h298a10 10 0 0 1 10 10v10H20z" fill="{WHITE}" fill-opacity=".07"/>'
        f'<circle cx="34" cy="24" r="3" fill="{CORAL}"/><circle cx="45" cy="24" r="3" fill="{GOLD}"/><circle cx="56" cy="24" r="3" fill="{LIME}"/>'
        f'<text x="76" y="27.5" font-family="{MONO}" font-size="9.5" fill="{DIM}" textLength="62" lengthAdjust="spacingAndGlyphs">exercise.py</text>'
        f'<text x="326" y="27.5" text-anchor="end" font-family="{MONO}" font-size="9" fill="{ICE}" textLength="118" lengthAdjust="spacingAndGlyphs">Pyodide · WebAssembly</text>'
    )
    lines = [("def greet(name):", ICE, 0.6), ('    return f"Hello, {name}!"', WHITE, 2.1), ('print(greet("PyLearn"))', LIME, 4.2)]
    for i, (txt, col, st) in enumerate(lines):
        y = 62 + i * 21
        b.append(f'<text x="30" y="{y}" font-family="{MONO}" font-size="11" fill="{DIM}" fill-opacity=".7">{i + 1}</text>')
        dd, bb = typed(46, y, txt, st, T, col, 13, cps=15)
        defs += dd
        b.append(bb)
    k, vals = window(5.9, T - 0.4, T, fade=0.02)
    b.append(f'<g opacity="0"><text x="46" y="134" font-family="{MONO}" font-size="12" fill="{GOLD}" textLength="130" lengthAdjust="spacingAndGlyphs">&gt; Hello, PyLearn!</text>{A("opacity", vals, T, keytimes=k)}</g>')
    k, vals = window(6.5, T - 0.4, T, fade=0.02)
    p, w = pill(0, 0, "✓ tests passed", LIME, size=11, pad=10, h=24, fill_op=0.22)
    b.append(f'<g opacity="0"><g transform="translate({n(338 - 14 - w)} 122)">{p}</g>{A("opacity", vals, T, keytimes=k)}</g>')
    # XP bar
    b.append(
        f'<text x="370" y="130" font-family="{MONO}" font-size="10" fill="{MUTED}">XP</text><rect x="392" y="122" width="170" height="8" rx="4" fill="{WHITE}" fill-opacity=".10"/>'
        f'<rect x="392" y="122" width="0" height="8" rx="4" fill="{PEACH}">{A("width", "0;0;170;170", T, keytimes=[0, .55, .8, 1], calc="spline", splines="0 0 1 1;.16 1 .3 1;0 0 1 1")}</rect>'
    )

    # 12 achievement badges (hexagons) light up one by one
    def hexpts(cx, cy, r):
        return " ".join(f"{n(cx + r * math.cos(math.radians(60 * i + 30)))},{n(cy + r * math.sin(math.radians(60 * i + 30)))}" for i in range(6))

    for i in range(12):
        col_i, row_i = i % 6, i // 6
        cx, cy = 384 + col_i * 36, 52 + row_i * 36
        t_on = 6.6 + i * 0.2
        k, vals = window(t_on, T - 0.3, T, fade=0.02)
        b.append(f'<polygon points="{hexpts(cx, cy, 15)}" fill="none" stroke="{WHITE}" stroke-opacity=".25"/>')
        b.append(
            f'<g opacity="0"><polygon points="{hexpts(cx, cy, 15)}" fill="{magma(0.45 + 0.5 * i / 11)}" fill-opacity=".9"/>'
            f'<path d="M{n(cx - 4.5)} {cy}l3.2 3.4 6-7" fill="none" stroke="{BG}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>{A("opacity", vals, T, keytimes=k)}</g>'
        )
    return defs, "".join(b)


def cards():
    d, s = scene_jobai()
    frame("card_jobai.svg", "jobai", "EARLY DEVELOPMENT", GOLD,
          ["Self-hosted job-search automation. Working today: job discovery from",
           "Greenhouse, Lever and Ashby, SQLite dedupe, and an LLM gateway with spend",
           "caps, a kill switch and PII redaction. Scoring, tailoring, auto-apply: planned."],
          ["PYTHON 3.12", "SQLITE", "OPENAI", "PYTEST"], d, s, "jobai: self-hosted job search automation, early development")
    d, s = scene_portfolio()
    frame("card_portfolio.svg", "dheeraj-aws-portfolio", "LIVE", LIME,
          ["A 3D portfolio you break open: twelve interactive three.js scenes, a command",
           "palette, a built-in terminal and 15 explorer badges. Plain static files, no",
           "build step, deployed from GitHub to AWS Amplify Hosting on every push."],
          ["THREE.JS", "AWS AMPLIFY", "VANILLA JS"], d, s, "dheeraj-aws-portfolio: a 3D interactive portfolio hosted on AWS Amplify")
    d, s = scene_polybot()
    frame("card_polybot.svg", "polybot", "PAPER TRADING", ICE,
          ["Paper-trading bot for Polymarket prediction markets. Scans markets every",
           "2-3 minutes, generates signals, simulates trades with slippage and risk",
           "limits, and reports through a Telegram bot and a web dashboard (SQLite)."],
          ["PYTHON", "SQLITE", "TELEGRAM", "DASHBOARD"], d, s, "polybot: a Polymarket paper trading bot with signals, Telegram alerts and a dashboard")
    d, s = scene_pylearn()
    frame("card_pylearn.svg", "python-learning-platform", "LIVE DEMO", LIME,
          ["PyLearn: learn Python by coding in the browser. Monaco editor, code runs",
           "client-side via Pyodide (WebAssembly), auto-graded tests, XP, 12 badges,",
           "daily streaks and a leaderboard. React 18, TypeScript and Vite on Netlify."],
          ["REACT 18", "TYPESCRIPT", "VITE", "PYODIDE"], d, s, "python-learning-platform: PyLearn, an in-browser Python learning platform")
