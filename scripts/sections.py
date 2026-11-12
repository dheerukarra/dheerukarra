"""Terminal intro, 3D skills embedding space, career commit timeline and footer wave."""
import math
import random

from fx import *
from lib import *


# ------------------------------------------------------------------ terminal
def terminal():
    W, H, T = 1280, 430, 22.0
    defs, b = [], []
    defs.append(f'<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{PEACH}" stop-opacity=".7"/><stop offset=".5" stop-color="{PLUM}" stop-opacity=".25"/><stop offset="1" stop-color="{ICE}" stop-opacity=".5"/></linearGradient>')
    b.append(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="#0b0720" stroke="url(#edge)" stroke-width="1.5"/>')
    b.append(f'<path d="M1 19a18 18 0 0 1 18-18h{W - 38}a18 18 0 0 1 18 18v28H1z" fill="{WHITE}" fill-opacity=".05"/>')
    b.append(f'<circle cx="34" cy="24" r="6" fill="{CORAL}"/><circle cx="56" cy="24" r="6" fill="{GOLD}"/><circle cx="78" cy="24" r="6" fill="{LIME}"/>')
    b.append(f'<text x="{W / 2}" y="30" text-anchor="middle" font-family="{MONO}" font-size="16" fill="{DIM}" textLength="330" lengthAdjust="spacingAndGlyphs">dheeraj@model: ~/profile  (zsh)</text>')
    groups = [
        ("whoami", 0.6, [("dheeraj-reddy-karra · automation tester turned AI-native engineer", WHITE, 1.6)]),
        ("cat education.txt", 3.4, [("M.S. Data Science & AI · University of Central Missouri · expected 05/2027", MUTED, 4.6), ("B.S. Computer Science · cum laude · 3.51 GPA · Dean's List", MUTED, 5.4)]),
        ("ls projects/", 7.4, [("jobai/   polybot/   python-learning-platform/   dheeraj-aws-portfolio/", ICE, 8.4)]),
        ("cat now.md", 10.2, [("directing AI coding agents with constraints, audits and regression checks", PEACH, 11.3)]),
    ]
    size, cw, lh = 20, 12.0, 33
    row = 0
    body = []
    for cmd, st, outs in groups:
        y = 100 + row * lh
        d1, b1 = typed(56, y, "$", st, T, PEACH, size, cps=20)
        d2, b2 = typed(56 + 2 * cw, y, cmd, st + 0.15, T, WHITE, size, cps=24)
        defs += [d1, d2]
        body += [b1, b2]
        row += 1
        for text, col, t0 in outs:
            y = 100 + row * lh
            d3, b3 = typed(56 + 2 * cw, y, text, t0, T, col, size, cps=70)
            defs.append(d3)
            body.append(b3)
            row += 1
    y = 100 + row * lh
    d1, b1 = typed(56, y, "$", 13.2, T, PEACH, size, cps=20)
    defs.append(d1)
    body.append(b1)
    k, vals = window(13.6, T - 1.2, T, fade=0.01)
    body.append(f'<g opacity="0"><rect x="{56 + 2 * cw}" y="{y - 17}" width="11" height="22" fill="{PEACH}">{A("opacity", "1;1;0;0", 1.1, keytimes=[0, .5, .5, 1], calc="discrete")}</rect>{A("opacity", vals, T, keytimes=k)}</g>')
    ok = [0, (T - 1.4) / T, (T - 0.7) / T, 1]
    b.append(f'<g opacity="1">{"".join(body)}{A("opacity", "1;1;0;0", T, keytimes=ok)}</g>')
    svg("terminal.svg", W, H, "".join(b), "".join(defs), "Terminal: whoami, education, projects and what I am working on now")


# ------------------------------------------------------------------ skills as a 3D embedding space
def skills_space():
    W, H = 1280, 500
    F, T = 48, 24.0
    cx, cy, S = 850, 254, 152
    TZ, VX = math.radians(8), math.radians(22)
    rnd = random.Random(5)
    clusters = [
        dict(name="AI & vibe coding", col=PEACH, c=(-1.15, 0.55, 0.35), labels=[("Claude Code", "anthropic"), ("Ollama", "ollama"), ("Gemini CLI", "googlegemini"), ("Prompt engineering", None)]),
        dict(name="Testing & QA", col=LIME, c=(1.1, 0.6, -0.45), labels=[("Selenium", "selenium"), ("Cypress", "cypress"), ("Postman", "postman"), ("JIRA", "jira")]),
        dict(name="Data science & ML", col=ICE, c=(0.25, -0.75, 1.1), labels=[("Python", "python"), ("PyTorch", "pytorch"), ("Pandas", "pandas"), ("NumPy", "numpy")]),
        dict(name="Languages & delivery", col=VIOLET, c=(-0.3, -0.55, -1.15), labels=[("Java", "openjdk"), ("PostgreSQL", "postgresql"), ("MongoDB", "mongodb"), ("Git", "git")]),
    ]
    dirs = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    pts = []  # dict(p, col, label, icon, cl)
    for ci, cl in enumerate(clusters):
        for (lab, ic), d in zip(cl["labels"], dirs):
            nn = math.sqrt(3)
            pts.append(dict(p=tuple(cl["c"][k] + 0.27 * d[k] / nn for k in range(3)), col=cl["col"], label=lab, icon=ic, cl=ci))
        for _ in range(10):
            while True:
                v = [rnd.gauss(0, 0.26) for _ in range(3)]
                if math.sqrt(sum(a * a for a in v)) > 0.38:
                    break
            pts.append(dict(p=tuple(cl["c"][k] + v[k] for k in range(3)), col=cl["col"], label=None, icon=None, cl=ci))
    proj = [[(cx + S * x, cy - S * y, z) for x, y, z in (rot(p["p"], 2 * math.pi * k / F, TZ, VX) for p in pts)] for k in range(F + 1)]
    cproj = [[(cx + S * x, cy - S * y, z) for x, y, z in (rot(cl["c"], 2 * math.pi * k / F, TZ, VX) for cl in clusters)] for k in range(F + 1)]

    defs = (
        f'<radialGradient id="bgp" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{PLUM}" stop-opacity=".40"/><stop offset="1" stop-color="{PLUM}" stop-opacity="0"/></radialGradient>'
        f'<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3.5"/></filter>'
    )
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/><circle cx="{cx}" cy="{cy}" r="380" fill="url(#bgp)"/>']
    for gx in range(0, W, 40):
        b.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{H}" stroke="{WHITE}" stroke-opacity=".025"/>')
    for gy in range(0, H, 40):
        b.append(f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}" stroke="{WHITE}" stroke-opacity=".025"/>')
    # faint links from each point to its nearest labelled point in the cluster
    labelled = [i for i, p in enumerate(pts) if p["label"]]
    for i, p in enumerate(pts):
        if p["label"]:
            continue
        j = min((j for j in labelled if pts[j]["cl"] == p["cl"]), key=lambda j: math.dist(p["p"], pts[j]["p"]))
        ds = [f"M{n(proj[k][i][0])} {n(proj[k][i][1])}L{n(proj[k][j][0])} {n(proj[k][j][1])}" for k in range(F + 1)]
        ops = [n(0.04 + 0.30 * clamp((proj[k][i][2] + proj[k][j][2]) / 2 / 1.9 + 0.5), 2) for k in range(F + 1)]
        b.append(f'<path d="{ds[0]}" fill="none" stroke="{p["col"]}" stroke-width="1">{A("d", ds, T)}{A("stroke-opacity", ops, T)}</path>')
    # points
    for i, p in enumerate(pts):
        xs = [n(proj[k][i][0]) for k in range(F + 1)]
        ys = [n(proj[k][i][1]) for k in range(F + 1)]
        ts = [clamp(proj[k][i][2] / 2.0 + 0.5) for k in range(F + 1)]
        base = 4.2 if p["label"] else 2.4
        rs = [n(base * (0.6 + 0.9 * t), 2) for t in ts]
        os_ = [n(0.25 + 0.75 * t, 2) for t in ts]
        b.append(f'<circle cx="{xs[0]}" cy="{ys[0]}" r="3" fill="{p["col"]}">{A("cx", xs, T)}{A("cy", ys, T)}{A("r", rs, T)}{A("opacity", os_, T)}</circle>')
    # labels with logos
    for i, p in enumerate(pts):
        if not p["label"]:
            continue
        fs = 15
        w = (24 if p["icon"] else 10) + len(p["label"]) * fs * 0.6 + 10
        chip = (
            f'<rect x="10" y="-27" width="{n(w)}" height="26" rx="13" fill="{BG}" fill-opacity=".86" stroke="{p["col"]}" stroke-opacity=".8"/>'
            + (icon(p["icon"], 18, -23, 18, WHITE) if p["icon"] else "")
            + f'<text x="{n(10 + (30 if p["icon"] else 12))}" y="-9" font-family="{MONO}" font-size="{fs}" fill="{WHITE}" textLength="{n(len(p["label"]) * fs * 0.6)}" lengthAdjust="spacingAndGlyphs">{esc(p["label"])}</text>'
        )
        xs = [f"{n(proj[k][i][0])} {n(proj[k][i][1])}" for k in range(F + 1)]
        ts = [clamp(proj[k][i][2] / 2.0 + 0.5) for k in range(F + 1)]
        sc = [n(0.78 + 0.34 * t, 3) for t in ts]
        os_ = [n(0.30 + 0.70 * t, 2) for t in ts]
        b.append(f'<g opacity="1" transform="translate({xs[0]})">{AT("translate", xs, T)}{A("opacity", os_, T)}<g>{AT("scale", sc, T)}{chip}</g></g>')

    # query vector: visits each cluster, lights its 4 nearest neighbours
    PH = T / 4
    star_x, star_y = [], []
    for k in range(F + 1):
        t = T * k / F
        ph = min(3, int(t / PH))
        prev = (ph - 1) % 4
        u = clamp((t - ph * PH) / 1.2)
        e = 1 - (1 - u) ** 3
        a, c = cproj[k][prev], cproj[k][ph]
        star_x.append(n(a[0] + (c[0] - a[0]) * e))
        star_y.append(n(a[1] + (c[1] - a[1]) * e))
    sp = [(0, -13), (3.4, -3.4), (13, 0), (3.4, 3.4), (0, 13), (-3.4, 3.4), (-13, 0), (-3.4, -3.4)]
    star = " ".join(f"{n(x)},{n(y)}" for x, y in sp)
    for ph, cl in enumerate(clusters):
        ids = [i for i, p in enumerate(pts) if p["label"] and p["cl"] == ph]
        k0, v0 = window(ph * PH + 1.2, (ph + 1) * PH - 0.1, T, fade=0.012)
        for i in ids:
            ds = [f"M{n(cproj[k][ph][0])} {n(cproj[k][ph][1])}L{n(proj[k][i][0])} {n(proj[k][i][1])}" for k in range(F + 1)]
            b.append(f'<path d="{ds[0]}" fill="none" stroke="{WHITE}" stroke-width="1.6" stroke-dasharray="4 5" opacity="0">{A("d", ds, T)}{A("opacity", v0, T, keytimes=k0)}</path>')
    b.append(f'<g transform="translate({star_x[0]} {star_y[0]})">{AT("translate", [f"{x} {y}" for x, y in zip(star_x, star_y)], T)}<circle r="22" fill="{WHITE}" opacity=".22" filter="url(#blur)"/><polygon points="{star}" fill="{WHITE}"/></g>')

    # left column
    b.append(f'<text x="70" y="112" font-family="{MONO}" font-size="17" fill="{PEACH}" letter-spacing="1.5" textLength="236" lengthAdjust="spacingAndGlyphs">vector_space.view()</text>')
    b.append(f'<text x="70" y="178" font-family="{SANS}" font-size="52" font-weight="800" fill="{WHITE}" letter-spacing="-1" textLength="392" lengthAdjust="spacingAndGlyphs">Where my skills</text>')
    b.append(f'<text x="70" y="238" font-family="{SANS}" font-size="52" font-weight="800" fill="{PEACH}" letter-spacing="-1" textLength="214" lengthAdjust="spacingAndGlyphs">cluster</text>')
    b.append(f'<text x="70" y="282" font-family="{MONO}" font-size="16" fill="{MUTED}" textLength="380" lengthAdjust="spacingAndGlyphs">toy 3D embedding · each dot is a skill</text>')
    b.append(f'<text x="70" y="308" font-family="{MONO}" font-size="16" fill="{MUTED}" textLength="420" lengthAdjust="spacingAndGlyphs">a query vector visits each cluster in turn</text>')
    for i, cl in enumerate(clusters):
        y = 352 + i * 30
        b.append(f'<circle cx="78" cy="{y - 5}" r="6" fill="{cl["col"]}"/><text x="96" y="{y}" font-family="{MONO}" font-size="17" fill="{WHITE}" textLength="{n(len(cl["name"]) * 10.2)}" lengthAdjust="spacingAndGlyphs">{esc(cl["name"])}</text>')
    # nearest neighbours caption, one per phase
    for ph, cl in enumerate(clusters):
        k0, v0 = window(ph * PH + 1.2, (ph + 1) * PH - 0.1, T, fade=0.012)
        txt = "nearest → " + " · ".join(lab for lab, _ in cl["labels"])
        b.append(f'<g opacity="0"><text x="70" y="478" font-family="{MONO}" font-size="16" fill="{cl["col"]}" textLength="{n(len(txt) * 9.6)}" lengthAdjust="spacingAndGlyphs">{esc(txt)}</text>{A("opacity", v0, T, keytimes=k0)}</g>')
    for x0, y0, sx, sy in ((26, 26, 1, 1), (W - 26, 26, -1, 1), (26, H - 26, 1, -1), (W - 26, H - 26, -1, -1)):
        b.append(f'<path d="M{x0} {y0 + 22 * sy}V{y0}H{x0 + 22 * sx}" fill="none" stroke="{WHITE}" stroke-opacity=".28" stroke-width="1.5"/>')
    svg("skills.svg", W, H, "".join(b), defs, "My skills as a rotating 3D embedding space with four clusters: AI and vibe coding, testing and QA, data science and ML, languages and delivery")


# ------------------------------------------------------------------ career as a commit graph
def career():
    W, H = 1280, 360
    LY = 190
    # (months since 02/2023, id, date, message, detail, side, colour)
    items = [
        (0, "c01", "02/2023", "join ICloud Technologies", "Automation Tester · Selenium, Cypress", "up", ICE),
        (10, "c02", "12/2023", "B.S. Computer Science", "cum laude · 3.51 GPA · Dean's List", "down", PEACH),
        (22, "c03", "12/2024", "join VSquare IT Inc.", "Automation Tester · Java, Selenium", "up", ICE),
        (27, "c04", "05/2025", "wrap up testing roles", "two years of automation testing", "down", LIME),
        (51, "HEAD", "05/2027", "M.S. Data Science & AI", "University of Central Missouri · expected", "up", MAGENTA),
    ]
    x_of = lambda m: 110 + 1060 * m / 51
    defs = (
        f'<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{PEACH}" stop-opacity=".6"/><stop offset=".5" stop-color="{PLUM}" stop-opacity=".2"/><stop offset="1" stop-color="{ICE}" stop-opacity=".45"/></linearGradient>'
        f'<linearGradient id="trunk" x1="0" x2="1"><stop offset="0" stop-color="{ICE}"/><stop offset=".5" stop-color="{PEACH}"/><stop offset="1" stop-color="{MAGENTA}"/></linearGradient>'
    )
    b = [f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="{PANEL}" stroke="url(#edge)" stroke-width="1.5"/>']
    b.append(f'<text x="40" y="52" font-family="{MONO}" font-size="18" fill="{PEACH}" letter-spacing="1" textLength="250" lengthAdjust="spacingAndGlyphs">$ git log --graph</text>')
    # trunk draws in once, then stays
    x0, x1 = x_of(0), x_of(51)
    L = x1 - x0
    b.append(f'<line x1="{n(x0)}" y1="{LY}" x2="{n(x1)}" y2="{LY}" stroke="url(#trunk)" stroke-width="4" stroke-linecap="round" stroke-dasharray="{n(L)}" stroke-dashoffset="{n(L)}">{A("stroke-dashoffset", f"{n(L)};0", 2.4, begin="0.2s", fill="freeze", repeat=None, calc="spline", keytimes=[0, 1], splines=".4 0 .2 1")}</line>')
    # "now" branch: dashed arc from 05/2025 to HEAD carrying the current projects
    xa, xb = x_of(27), x_of(51)
    b.append(f'<path d="M{n(xa)} {LY}C{n(xa + 120)} {LY + 70} {n(xb - 120)} {LY + 70} {n(xb)} {LY}" fill="none" stroke="{MAGENTA}" stroke-width="2" stroke-dasharray="6 7" opacity=".9">{A("stroke-dashoffset", "0;-26", 1.2)}</path>')
    b.append(f'<text x="{n(xb + 10)}" y="{LY + 80}" text-anchor="end" font-family="{MONO}" font-size="15" fill="{MAGENTA}" textLength="400" lengthAdjust="spacingAndGlyphs">branch: now · jobai · polybot · PyLearn · 3D portfolio</text>')
    # packet travelling along the trunk
    b.append(f'<circle r="5" fill="{WHITE}"><animateMotion dur="7s" begin="2.4s" repeatCount="indefinite" path="M{n(x0)} {LY}L{n(x1)} {LY}"/>{A("opacity", "0;1;1;0", 7, begin="2.4s", keytimes=[0, .05, .95, 1])}</circle>')
    for i, (m, cid, date, msg, detail, side, col) in enumerate(items):
        x = x_of(m)
        t0 = 0.4 + m / 51 * 2.0
        sgn = -1 if side == "up" else 1
        block = (
            f'<line x1="{n(x)}" y1="{LY}" x2="{n(x)}" y2="{n(LY + sgn * 30)}" stroke="{col}" stroke-opacity=".7"/>'
            f'<circle cx="{n(x)}" cy="{LY}" r="{10 if cid == "HEAD" else 8}" fill="{BG}" stroke="{col}" stroke-width="3"/>'
        )
        if cid == "HEAD":
            block += f'<circle cx="{n(x)}" cy="{LY}" r="10" fill="none" stroke="{col}" opacity="0">{A("r", "10;30", 2.4)}{A("opacity", ".8;0", 2.4)}</circle>'
        ax = n(x)
        ta = "middle"
        if m == 0:
            ta, ax = "start", n(x - 12)
        if m == 51:
            ta, ax = "end", n(x + 12)
        base = LY + sgn * 44 + (-60 if sgn < 0 else 20)
        block += (
            f'<text x="{ax}" y="{base + 22}" text-anchor="{ta}" font-family="{MONO}" font-size="15" fill="{col}" textLength="{n(len(cid + " · " + date) * 9)}" lengthAdjust="spacingAndGlyphs">{cid} · {date}</text>'
            f'<text x="{ax}" y="{base + 48}" text-anchor="{ta}" font-family="{SANS}" font-size="23" font-weight="700" fill="{WHITE}" textLength="{n(len(msg) * 11.4)}" lengthAdjust="spacingAndGlyphs">{esc(msg)}</text>'
            f'<text x="{ax}" y="{base + 72}" text-anchor="{ta}" font-family="{MONO}" font-size="14" fill="{MUTED}" textLength="{n(len(detail) * 8.4)}" lengthAdjust="spacingAndGlyphs">{esc(detail)}</text>'
        )
        b.append(fade_in(block, n(t0, 2), 0.7, rise=10 * sgn))
    svg("career.svg", W, H, "".join(b), defs, "Career as a git log: automation testing roles from 02/2023, B.S. Computer Science 12/2023, M.S. Data Science and AI expected 05/2027")


# ------------------------------------------------------------------ footer wave
def footer():
    W, H = 1280, 230
    F = 8
    defs = (
        f'<linearGradient id="w1" x1="0" x2="1"><stop offset="0" stop-color="{PLUM}"/><stop offset=".5" stop-color="{MAGENTA}"/><stop offset="1" stop-color="{PEACH}"/></linearGradient>'
        f'<linearGradient id="w2" x1="0" x2="1"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".7"/><stop offset="1" stop-color="{ICE}" stop-opacity=".7"/></linearGradient>'
    )
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']

    def wave(amp, base, freq, phase0, speed):
        ds = []
        for k in range(F + 1):
            ph = phase0 + 2 * math.pi * speed * k / F
            pts = [(x, base + amp * math.sin(freq * x / W * 2 * math.pi + ph) + amp * 0.4 * math.sin(2.3 * freq * x / W * 2 * math.pi - ph)) for x in range(0, W + 1, 40)]
            ds.append("M0 " + str(H) + "L" + "L".join(f"{n(x)} {n(y)}" for x, y in pts) + f"L{W} {H}Z")
        return ds

    for amp, base, fr, ph, sp, fill, op, dur in ((22, 150, 1.4, 0.0, 1, "url(#w2)", 0.55, 9), (26, 168, 1.0, 1.7, -1, "url(#w1)", 0.85, 12)):
        ds = wave(amp, base, fr, ph, sp)
        b.append(f'<path d="{ds[0]}" fill="{fill}" opacity="{op}">{A("d", ds, dur)}</path>')
    b.append(f'<text x="{W / 2}" y="78" text-anchor="middle" font-family="{SANS}" font-size="40" font-weight="800" fill="{WHITE}" letter-spacing="-0.5" textLength="690" lengthAdjust="spacingAndGlyphs">Next epoch: let\'s build something.</text>')
    b.append(f'<text x="{W / 2}" y="112" text-anchor="middle" font-family="{MONO}" font-size="17" fill="{MUTED}" letter-spacing="1" textLength="560" lengthAdjust="spacingAndGlyphs">loss.backward(); optimizer.step(); repeat</text>')
    svg("footer.svg", W, H, "".join(b), defs, "Next epoch: let's build something", radius=0)


def sections():
    terminal()
    skills_space()
    career()
    footer()
