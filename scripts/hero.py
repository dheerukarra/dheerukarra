"""Hero: a shaded 3D loss landscape. Plain gradient descent gets stuck in a local minimum while
gradient descent with momentum rolls into the global minimum ("Automation tester" -> "AI-native engineer").
The optimiser paths are real numeric gradient descent on the toy surface below, nothing is made up."""
import math

from lib import *

W, H = 1280, 560
CX, CY = 905, 318          # screen centre of the surface
AZ, EL = math.radians(-38), math.radians(31)
DIST, FOC, K = 9.0, 1250.0, 1.15
DOM = 1.7
T = 15.0                   # loop length (s)


def loss(x, y):
    return (0.20 * (x * x + y * y) + 0.20 * math.sin(2.1 * x) * math.sin(1.9 * y)
            - 1.20 * math.exp(-((x - 0.55) ** 2 + (y - 0.35) ** 2) / 0.20)
            - 0.60 * math.exp(-((x + 0.85) ** 2 + (y + 0.65) ** 2) / 0.13))


def grad(x, y, h=1e-4):
    return (loss(x + h, y) - loss(x - h, y)) / (2 * h), (loss(x, y + h) - loss(x, y - h)) / (2 * h)


def descend(x, y, lr, beta, steps):
    vx = vy = 0.0
    path = [(x, y)]
    for _ in range(steps):
        gx, gy = grad(x, y)
        vx, vy = beta * vx - lr * gx, beta * vy - lr * gy
        x, y = max(-DOM, min(DOM, x + vx)), max(-DOM, min(DOM, y + vy))
        path.append((x, y))
        if len(path) > 12 and math.dist(path[-1], path[-2]) < 0.0015:
            break
    return path


def project(gx, gy, hh):
    X, Y, Z = gx, hh, gy
    c, s = math.cos(AZ), math.sin(AZ)
    x, z = c * X + s * Z, -s * X + c * Z
    c, s = math.cos(EL), math.sin(EL)
    up, depth = c * Y - s * z, s * Y + c * z
    k = FOC / (DIST - depth)
    return CX + k * x, CY - k * up, depth


def shade(hexcol, f):
    r, g, b = (int(hexcol[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(v * f))) for v in (r, g, b))


def surface_polys(N=34):
    step = 2 * DOM / N
    light = (-0.40, 0.80, 0.45)
    ln = math.sqrt(sum(v * v for v in light))
    light = tuple(v / ln for v in light)
    polys = []
    for i in range(N):
        for j in range(N):
            xs = (-DOM + i * step, -DOM + (i + 1) * step)
            ys = (-DOM + j * step, -DOM + (j + 1) * step)
            corners = [(xs[0], ys[0]), (xs[1], ys[0]), (xs[1], ys[1]), (xs[0], ys[1])]
            pts = [project(x, y, K * loss(x, y)) for x, y in corners]
            mx, my = (xs[0] + xs[1]) / 2, (ys[0] + ys[1]) / 2
            dx = (loss(mx + 1e-3, my) - loss(mx - 1e-3, my)) / 2e-3 * K
            dz = (loss(mx, my + 1e-3) - loss(mx, my - 1e-3)) / 2e-3 * K
            nx, ny, nz = -dx, 1.0, -dz
            nl = math.sqrt(nx * nx + ny * ny + nz * nz)
            lum = max(0.0, (nx * light[0] + ny * light[1] + nz * light[2]) / nl)
            tn = (loss(mx, my) + 1.05) / 2.0
            t = (1 - max(0.0, min(1.0, tn))) ** 1.35
            col = shade(magma(0.05 + 0.95 * t), 0.62 + 0.62 * lum)
            depth = sum(p[2] for p in pts) / 4
            polys.append((depth, pts, col))
    polys.sort(key=lambda p: p[0])
    return polys


def timeline(path, t0, t1):
    """Key times for a path. Real gradient descent is front-loaded (big steps first, then a long crawl),
    so time is a blend of step index and on-screen distance travelled, which keeps the descent readable."""
    xy = [project(x, y, K * loss(x, y))[:2] for x, y in path]
    cum = [0.0]
    for a, b in zip(xy, xy[1:]):
        cum.append(cum[-1] + math.dist(a, b))
    m = len(path) - 1
    u = [0.30 * i / m + 0.70 * cum[i] / cum[-1] for i in range(m + 1)]
    return [0.0] + [(t0 + (t1 - t0) * v) / T for v in u] + [1.0]


def optimiser(path, t0, t1, color, glow, dashed=False):
    pts = [project(x, y, K * loss(x, y) + 0.07) for x, y in path]
    xy = [(p[0], p[1]) for p in pts]
    kt = timeline(path, t0, t1)
    xs = [n(xy[0][0])] + [n(p[0]) for p in xy] + [n(xy[-1][0])]
    ys = [n(xy[0][1])] + [n(p[1]) for p in xy] + [n(xy[-1][1])]
    cum, tot = [0.0], 0.0
    for a, b in zip(xy, xy[1:]):
        tot += math.dist(a, b)
        cum.append(tot)
    offs = [n(tot)] + [n(tot - c) for c in cum] + [n(0)]
    d = "M" + "L".join(f"{n(x)} {n(y)}" for x, y in xy)
    ok, ov = window(t0 - 0.2, T - 1.4, T, fade=0.02)
    g = f'<g opacity="0">{A("opacity", ov, T, keytimes=ok)}'
    g += (
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" '
        f'stroke-dasharray="{n(tot)}" stroke-dashoffset="{n(tot)}"{" opacity=" + chr(34) + ".75" + chr(34) if dashed else ""}>'
        f'{A("stroke-dashoffset", offs, T, keytimes=kt)}</path>'
    )
    g += f'<circle r="13" fill="{glow}" opacity=".30" cx="{xs[0]}" cy="{ys[0]}">{A("cx", xs, T, keytimes=kt)}{A("cy", ys, T, keytimes=kt)}</circle>'
    g += f'<circle r="5" fill="{WHITE}" cx="{xs[0]}" cy="{ys[0]}">{A("cx", xs, T, keytimes=kt)}{A("cy", ys, T, keytimes=kt)}</circle></g>'
    return g, xy


def tag(x, y, text, color, size=12, anchor="start", appear=None):
    w = len(text) * size * 0.62 + 18
    x0 = x if anchor == "start" else x - w / 2 if anchor == "middle" else x - w
    s = (
        f'<rect x="{n(x0)}" y="{n(y - 17)}" width="{n(w)}" height="24" rx="12" fill="{BG}" fill-opacity=".82" stroke="{color}" stroke-opacity=".8"/>'
        f'<text x="{n(x0 + 9)}" y="{n(y)}" font-family="{MONO}" font-size="{size}" fill="{color}" textLength="{n(w - 18)}" lengthAdjust="spacingAndGlyphs">{esc(text)}</text>'
    )
    if appear:
        a, b = appear
        k, v = window(a, b, T, fade=0.02)
        s = f'<g opacity="0">{A("opacity", v, T, keytimes=k)}{s}</g>'
    return s


def hero():
    stuck = descend(-1.4, -1.3, 0.10, 0.0, 90)
    win = descend(-1.4, 0.9, 0.045, 0.88, 220)
    win = win[:: max(1, len(win) // 70)] + [win[-1]]
    stuck = stuck[:: max(1, len(stuck) // 55)] + [stuck[-1]]
    print("stuck ends", [round(v, 2) for v in stuck[-1]], "loss", round(loss(*stuck[-1]), 3), "| winner ends", [round(v, 2) for v in win[-1]], "loss", round(loss(*win[-1]), 3))

    defs = f"""
<radialGradient id="glowp" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{PEACH}" stop-opacity=".9"/><stop offset="1" stop-color="{PEACH}" stop-opacity="0"/></radialGradient>
<radialGradient id="bgp" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{PLUM}" stop-opacity=".42"/><stop offset="1" stop-color="{PLUM}" stop-opacity="0"/></radialGradient>
<radialGradient id="bgi" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{ICE}" stop-opacity=".10"/><stop offset="1" stop-color="{ICE}" stop-opacity="0"/></radialGradient>
<linearGradient id="beam" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{PEACH}" stop-opacity=".95"/><stop offset="1" stop-color="{PEACH}" stop-opacity="0"/></linearGradient>
<linearGradient id="nameg" x1="0" x2="1"><stop offset="0" stop-color="{WHITE}"/><stop offset=".6" stop-color="{WHITE}"/><stop offset="1" stop-color="{PEACH}"/></linearGradient>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
<clipPath id="r1"><rect x="40" y="136" width="0" height="80">{A("width", "0;520", 1.1, begin="0.25s", calc="spline", keytimes=[0, 1], splines=".16 1 .3 1", fill="freeze", repeat=None)}</rect></clipPath>
<clipPath id="r2"><rect x="40" y="206" width="0" height="80">{A("width", "0;520", 1.3, begin="0.5s", calc="spline", keytimes=[0, 1], splines=".16 1 .3 1", fill="freeze", repeat=None)}</rect></clipPath>
"""
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    b.append(f'<circle cx="930" cy="300" r="470" fill="url(#bgp)"/><circle cx="120" cy="40" r="330" fill="url(#bgi)"/>')
    # faint graph paper
    for gx in range(0, W, 40):
        b.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{H}" stroke="{WHITE}" stroke-opacity=".028"/>')
    for gy in range(0, H, 40):
        b.append(f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}" stroke="{WHITE}" stroke-opacity=".028"/>')

    # base plane grid under the surface
    base = -1.55
    for i in range(0, 13):
        u = -DOM + 2 * DOM * i / 12
        a1, b1 = project(u, -DOM, base), project(u, DOM, base)
        a2, b2 = project(-DOM, u, base), project(DOM, u, base)
        b.append(f'<line x1="{n(a1[0])}" y1="{n(a1[1])}" x2="{n(b1[0])}" y2="{n(b1[1])}" stroke="{ICE}" stroke-opacity=".16"/>')
        b.append(f'<line x1="{n(a2[0])}" y1="{n(a2[1])}" x2="{n(b2[0])}" y2="{n(b2[1])}" stroke="{ICE}" stroke-opacity=".16"/>')

    # the loss surface (sways a hair so the camera feels alive)
    surf = ['<g>' + AT("rotate", f"-0.7 {CX} {CY};0.7 {CX} {CY};-0.7 {CX} {CY}", 16, calc="spline", keytimes=[0, .5, 1], splines=".45 0 .55 1;.45 0 .55 1")]
    for _, pts, col in surface_polys():
        surf.append(
            f'<polygon points="{" ".join(f"{n(x)},{n(y)}" for x, y, _ in pts)}" fill="{col}" stroke="{WHITE}" stroke-opacity=".07" stroke-width=".5"/>'
        )

    # minima markers + optimisers ride on the same sway
    gmin = project(0.52, 0.32, K * loss(0.52, 0.32))
    lmin = project(stuck[-1][0], stuck[-1][1], K * loss(*stuck[-1]))
    start = project(win[0][0], win[0][1], K * loss(*win[0]))

    surf.append(f'<ellipse cx="{n(gmin[0])}" cy="{n(gmin[1])}" rx="46" ry="26" fill="url(#glowp)" opacity=".75">{A("opacity", ".45;.9;.45", 3, calc="spline", keytimes=[0, .5, 1], splines=".45 0 .55 1;.45 0 .55 1")}</ellipse>')

    g1, _ = optimiser(stuck, 0.9, 6.0, ICE, ICE, dashed=True)
    g2, _ = optimiser(win, 1.8, 9.4, PEACH, PEACH)
    surf += [g1, g2]

    # arrival effects
    ak, av = window(9.4, T - 1.4, T, fade=0.02)
    surf.append(
        f'<g opacity="0">{A("opacity", av, T, keytimes=ak)}'
        f'<rect x="{n(gmin[0] - 1)}" y="{n(gmin[1] - 150)}" width="2" height="150" fill="url(#beam)"/>'
        + "".join(
            f'<ellipse cx="{n(gmin[0])}" cy="{n(gmin[1])}" rx="8" ry="4" fill="none" stroke="{PEACH}" stroke-width="1.6" opacity="0">'
            f'{A("rx", "8;60", 2.4, begin=f"{off}s")}{A("ry", "4;27", 2.4, begin=f"{off}s")}{A("opacity", ".9;0", 2.4, begin=f"{off}s")}</ellipse>'
            for off in (0, 1.2)
        )
        + '</g>'
    )
    surf.append(tag(gmin[0] + 62, gmin[1] + 4, "AI-native engineer", PEACH, 13, "start", (9.4, T - 1.4)))
    lk, lv_ = window(9.4, T - 1.4, T, fade=0.02)
    surf.append(f'<line x1="{n(gmin[0] + 8)}" y1="{n(gmin[1])}" x2="{n(gmin[0] + 62)}" y2="{n(gmin[1] - 6)}" stroke="{PEACH}" stroke-opacity=".7" opacity="0">{A("opacity", lv_, T, keytimes=lk)}</line>')
    surf.append(tag(lmin[0] - 26, lmin[1] - 34, "local minimum", ICE, 11, "end", (6.0, T - 1.4)))
    surf.append(tag(start[0], start[1] - 20, "Automation tester", WHITE, 12, "middle", (1.2, T - 1.4)))
    surf.append(f'<line x1="{n(start[0])}" y1="{n(start[1])}" x2="{n(start[0])}" y2="{n(start[1] - 20)}" stroke="{WHITE}" stroke-opacity=".6"/>')
    surf.append("</g>")
    b += surf

    # legend
    b.append(f'<circle cx="612" cy="539" r="4" fill="{ICE}"/><text x="624" y="543" font-family="{MONO}" font-size="12" fill="{MUTED}" textLength="248" lengthAdjust="spacingAndGlyphs">plain gradient descent: stuck</text>')
    b.append(f'<circle cx="896" cy="539" r="4" fill="{PEACH}"/><text x="908" y="543" font-family="{MONO}" font-size="12" fill="{MUTED}" textLength="248" lengthAdjust="spacingAndGlyphs">with momentum: converges</text>')
    b.append(f'<text x="1244" y="38" text-anchor="end" font-family="{MONO}" font-size="12" fill="{DIM}" letter-spacing="1.5">toy loss surface · illustration</text>')

    # --- left column
    b.append(f'<circle cx="78" cy="104" r="5" fill="{PEACH}">{A("opacity", "1;.25;1", 1.6)}</circle>')
    b.append(
        f'<text x="96" y="109" font-family="{MONO}" font-size="16" fill="{PEACH}" letter-spacing="1.5" textLength="150" lengthAdjust="spacingAndGlyphs">$ python train.py</text>'
        f'<rect x="254" y="96" width="9" height="17" fill="{PEACH}">{A("opacity", "1;1;0;0", 1.1, keytimes=[0, .5, .5, 1], calc="discrete")}</rect>'
    )

    def name(y, label, tl, fill, op=None):
        return (
            f'<text x="72" y="{y}" font-family="{SANS}" font-size="66" font-weight="800" fill="{fill}" letter-spacing="-1.5" '
            f'textLength="{tl}" lengthAdjust="spacingAndGlyphs"{" opacity=" + chr(34) + str(op) + chr(34) if op is not None else ""}>{label}'
        )

    for clip, y, label, tl, fill in (("r1", 190, "DHEERAJ", 292, WHITE), ("r2", 262, "REDDY KARRA", 458, "url(#nameg)")):
        b.append(f'<g clip-path="url(#{clip})">{name(y, label, tl, fill)}</text></g>')
        for col, dx in ((ICE, -4), (MAGENTA, 3)):
            kt = [0, .9, .915, .93, .945, .96, 1]
            b.append(
                name(y, label, tl, col, op=0)
                + A("opacity", "0;0;.8;0;.55;0;0", 6.5, begin="2.4s", keytimes=kt)
                + AT("translate", f"0 0;0 0;{dx} 0;{-dx} 0;{dx // 2} 0;0 0;0 0", 6.5, begin="2.4s", keytimes=kt)
                + "</text>"
            )

    roles = ["Automation tester → AI-native engineer", "jobai · polybot · PyLearn · 3D portfolio"]
    TR = 8.0
    for i, role in enumerate(roles):
        kt, vals = window(i * TR / 2, (i + 1) * TR / 2, TR, fade=0.04)
        b.append(
            f'<g opacity="0"><text x="72" y="312" font-family="{SANS}" font-size="22" font-weight="500" fill="{WHITE}" '
            f'textLength="{n(len(role) * 11.3, 0)}" lengthAdjust="spacingAndGlyphs"><tspan fill="{PEACH}">▸ </tspan>{esc(role)}</text>'
            f'{A("opacity", vals, TR, begin="1.6s", keytimes=kt)}</g>'
        )

    x = 72
    for i, (label, col) in enumerate((("PYTHON", PEACH), ("LLM TOOLING", ICE), ("QA AUTOMATION", LIME), ("DATA SCIENCE", VIOLET))):
        p, w = pill(x, 344, label, col)
        bg = n(2 + i * 0.18, 2)
        b.append(
            f'<g opacity="0">{p}{A("opacity", "0;1", 0.6, begin=f"{bg}s", fill="freeze", repeat=None)}'
            f'{AT("translate", "0 10;0 0", 0.6, begin=f"{bg}s", fill="freeze", repeat=None, calc="spline", keytimes=[0, 1], splines=".16 1 .3 1")}</g>'
        )
        x += w + 10

    # --- loss curve of the converging optimiser, drawn in sync with it
    lv = [loss(*p) for p in win]
    lo, hi = min(lv), max(lv)
    X0, Y0, WW, HH = 72, 408, 380, 78
    pts = [(X0 + WW * i / (len(lv) - 1), Y0 + HH * (1 - (v - lo) / (hi - lo))) for i, v in enumerate(lv)]
    tot = sum(math.dist(a, c) for a, c in zip(pts, pts[1:]))
    cum, run = [0.0], 0.0
    for a, c in zip(pts, pts[1:]):
        run += math.dist(a, c)
        cum.append(run)
    kt = timeline(win, 1.8, 9.4)
    offs = [n(tot)] + [n(tot - c) for c in cum] + ["0"]
    dstr = "M" + "L".join(f"{n(px)} {n(py)}" for px, py in pts)
    xs_ = [n(pts[0][0])] + [n(p[0]) for p in pts] + [n(pts[-1][0])]
    ys_ = [n(pts[0][1])] + [n(p[1]) for p in pts] + [n(pts[-1][1])]
    ok, ov = window(1.6, T - 1.4, T, fade=0.02)
    b.append(f'<line x1="{X0}" y1="{Y0 + HH + 8}" x2="{X0 + WW}" y2="{Y0 + HH + 8}" stroke="{WHITE}" stroke-opacity=".2"/><line x1="{X0 - 8}" y1="{Y0 - 6}" x2="{X0 - 8}" y2="{Y0 + HH + 8}" stroke="{WHITE}" stroke-opacity=".2"/>')
    b.append(f'<text x="{X0 - 8}" y="{Y0 - 14}" font-family="{MONO}" font-size="11" fill="{DIM}" letter-spacing="1">loss</text><text x="{X0 + WW}" y="{Y0 + HH + 26}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{DIM}" letter-spacing="1">steps</text>')
    b.append(
        f'<g opacity="0">{A("opacity", ov, T, keytimes=ok)}'
        f'<path d="{dstr}" fill="none" stroke="{PEACH}" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="{n(tot)}" stroke-dashoffset="{n(tot)}">{A("stroke-dashoffset", offs, T, keytimes=kt)}</path>'
        f'<circle r="4.5" fill="{WHITE}" cx="{xs_[0]}" cy="{ys_[0]}">{A("cx", xs_, T, keytimes=kt)}{A("cy", ys_, T, keytimes=kt)}</circle></g>'
    )

    # HUD corner brackets
    for x0, y0, sx, sy in ((26, 26, 1, 1), (W - 26, 26, -1, 1), (26, H - 26, 1, -1), (W - 26, H - 26, -1, -1)):
        b.append(f'<path d="M{x0} {y0 + 22 * sy}V{y0}H{x0 + 22 * sx}" fill="none" stroke="{WHITE}" stroke-opacity=".28" stroke-width="1.5"/>')

    svg("hero.svg", W, H, "".join(b), defs, "Dheeraj Reddy Karra: a 3D loss landscape where gradient descent takes an automation tester to an AI-native engineer")
