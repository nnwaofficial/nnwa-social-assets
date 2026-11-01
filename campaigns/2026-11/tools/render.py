"""Render NNWA v2 creatives (PNG + JPG) from a content JSON.

Usage:
    python3 scripts/render.py content.json out.png
    python3 scripts/render.py content.json out-dir/        # carousel: one file per slide

content.json (see templates/examples/ for one of each layout):
    {"layout": "glass", "theme": "photo", "photo": "path-or-url", ...fields}
    or {"slides": [ {...}, {...} ], "name": "protein-carousel"}  for carousels

Layouts and sizes:
    glass, vword, stat, annot, tiles, display, step, cta, report, bookpage   1080 x 1350
    reel, story                                                     1080 x 1920
    yt                                                              1280 x 720
    title, lower                                                    1920 x 1080
Themes: forest | paper | photo.  Text fields accept <em> (one Fraunces italic
word) and <b> only; everything else is escaped by the caller's discipline.
"""
import json
import os
import sys
import uuid

import subprocess
import tempfile

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # fall back to Node Playwright via scripts/shoot.js
    sync_playwright = None

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(SKILL, "templates")
SIZES = {"reel": (1080, 1920), "story": (1080, 1920), "storywrap": (1080, 1920), "yt": (1280, 720), "title": (1920, 1080), "lower": (1920, 1080)}
SPARK = '<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 0c.6 6.4 5.6 11.4 12 12-6.4.6-11.4 5.6-12 12-.6-6.4-5.6-11.4-12-12C6.4 11.4 11.4 6.4 12 0z"/></svg>'


def src(p):
    if not p:
        return ""
    if p.startswith(("http://", "https://", "file://", "data:")):
        return p
    return "file://" + os.path.abspath(p)


def logo(theme):
    f = "nnwa-wordmark.png" if theme == "paper" else "nnwa-wordmark-white.png"
    return f'<img class="logo" src="../design-system/assets/{f}" alt="">'


CTA = {"text": ""}


def url_text():
    """Right-hand brandbar text: the lead-magnet CTA when the content sets "cta", else nnwa.in."""
    return CTA["text"] or "nnwa.in"


def brandbar(d, theme):
    credit = f'<span class="credit">{d["credit"]}</span>' if d.get("credit") else ""
    return f'<div class="brandbar">{logo(theme)}{credit}<span class="url">{url_text()}</span></div>'


def photo(d, cls="", extra=""):
    pos = d.get("photo_pos", "center")
    return f'<div class="photo {cls}" style="background-image:url(\'{src(d.get("photo"))}\');background-position:{pos}">{extra}</div>'


def dots(d):
    if not d.get("dots"):
        return ""
    i, n = d["dots"]
    return '<div class="dots">' + "".join('<i class="on"></i>' if k == i else "<i></i>" for k in range(1, n + 1)) + "</div>"


def body(d):
    t = d.get("theme", "forest")
    L = d["layout"]
    g = d.get
    if L == "glass":
        return f'''{photo(d, "overlay")}<div class="topbar">{logo(t)}{dots(d) and ""}</div>{dots(d)}
<div class="card glass"><span class="overline center"><i class="rule"></i>{g("pill","")}<i class="rule"></i></span><div class="h1">{g("headline")}</div><div class="body">{g("body","")}</div></div>
<div class="brandbar"><span class="credit">{g("credit","")}</span><span class="url">{url_text()}</span></div>'''
    if L == "vword":
        return f'''<div class="topbar"><span class="label">{g("label","")}</span></div>
<div class="ring"></div>{photo(d, "circle")}<div class="word">{g("word")}</div>
<div class="note"><div class="bar"></div><p>{g("note")}</p></div>{brandbar({"credit": g("credit")}, t)}'''
    if L == "stat":
        chips = "".join(f'<span>{c}</span>' for c in g("chips", []))
        return f'''<div class="topbar"><span class="label">{g("label","")}</span></div>{dots(d)}
<div class="ring"></div>{photo(d, "circle")}
<div class="eyebrowrow"><span class="overline"><i class="rule"></i>{g("pill","")}</span></div>
<div class="num">{g("number")}<small>{g("unit","")}</small></div><div class="stat-label">{g("stat_label")}</div>
<div class="facts">{chips}</div><p class="fine">{g("fine","")}</p>{brandbar({"credit": g("credit")}, t)}'''
    if L == "annot":
        a, b = g("tags")
        return f'''<div class="head"><span class="label">{g("label","")}</span><div class="h1" style="margin-top:22px">{g("headline")}</div></div>
<div class="ring"></div>{photo(d, "circle")}
<div class="tag left"><div class="label">{a[0]}</div><p>{a[1]}</p></div><div class="tag right"><div class="label">{b[0]}</div><p>{b[1]}</p></div>
<p class="fine">{g("fine","")}</p>{brandbar({"credit": g("credit")}, t)}'''
    if L == "tiles":
        tiles = "".join(f'<div class="tile" style="background-image:url(\'{src(x["photo"])}\');background-position:{x.get("pos","center")}"><div class="glass"><b>{x["title"]}</b><span>{x["sub"]}</span></div></div>' for x in g("tiles"))
        return f'''<div class="head"><span class="label">{g("label","")}</span><div class="h1" style="margin-top:22px">{g("headline")}</div></div>{dots(d)}
<div class="grid">{tiles}</div><p class="fine">{g("fine","")}</p>{brandbar({"credit": g("credit")}, t)}'''
    if L == "display":
        w1, w2 = g("words")
        return f'''{photo(d, "overlay")}<div class="topbar">{logo(t)}<span class="label">{g("label","")}</span></div>
<div class="kicker label">{g("kicker","")}</div><div class="words"><span>{w1}</span><span class="link">{SPARK}</span><span>{w2}</span></div>
<p class="sub">{g("sub","")}</p><div class="brandbar"><span class="credit">{g("credit","")}</span><span class="url">{url_text()}</span></div>'''
    if L == "step":
        ph = photo(d, "", f'<span class="overline"><i class="rule"></i>{g("photo_tag","")}</span>') if g("photo") else ""
        chips = '<div class="facts">' + "".join(f'<span>{c}</span>' for c in g("chips", [])) + "</div>" if g("chips") else ""
        call = f'<div class="callout glass"><span class="label">{g("callout_label","")}</span><div class="calc">{g("callout")}</div></div>' if g("callout") else ""
        return f'''{dots(d)}<div class="index">{g("index")}</div>
<div class="content"><div class="h2">{g("headline")}</div><div class="body">{g("body","")}</div>{chips}</div>{ph}{call}{brandbar({"credit": g("credit")}, t)}'''
    if L == "cta":
        return f'''{dots(d)}<div class="content"><img class="seal" src="../design-system/assets/nnwa-seal.png" alt=""><div class="h1">{g("headline")}</div><div class="body">{g("body","")}</div><div><span class="overline"><i class="rule"></i>{g("pill","")}</span></div></div>{brandbar({}, t)}'''
    if L == "reel":
        return f'''{photo(d, "overlay")}<div class="safe"><div class="card glass"><span class="overline center"><i class="rule"></i>{g("pill","")}<i class="rule"></i></span><div class="num">{g("number")}<small>{g("unit","")}</small></div><div class="h2">{g("headline")}</div></div></div>
<div class="reelmark">{logo(t)}</div>'''
    if L == "story":
        return f'''{photo(d, "overlay")}<div class="top">{logo(t)}<span class="overline"><i class="rule"></i>{g("pill","")}</span></div>
<div class="card glass"><span class="label">{g("label","")}</span><div class="h1" style="font-size:76px">{g("headline")}</div><div class="body">{g("body","")}</div>{('<div class="sticker">'+g("sticker")+'</div>') if g("sticker") else ""}</div>
<div class="bottom"><span class="url">{g("bottom","nnwa.in")}</span></div>'''
    if L == "storywrap":
        return f'''<div class="top">{logo(t)}<span class="overline"><i class="rule"></i>{g("pill","New post")}</span></div>
<img class="feed" src="{src(g("feed"))}" alt=""><div class="cap"><div class="h2">{g("headline","")}</div><span class="url">{g("bottom","nnwa.in")}</span></div>'''
    if L == "yt":
        return f'''{photo(d)}<span class="overline"><i class="rule"></i>{g("pill","")}</span><div class="word">{g("word")}</div>
<div class="glass badge">{g("badge","")}</div>{logo(t)}'''
    if L == "title":
        return f'''{photo(d, "overlay") if g("photo") else ""}<div class="content"><span class="ep">{g("ep","")}</span><div class="h1">{g("headline")}</div><div class="body">{g("body","")}</div></div>{logo(t)}'''
    if L == "lower":
        demo = f'<div class="demo" style="background-image:url(\'{src(g("demo_bg"))}\')"></div>' if g("demo_bg") else ""
        return f'''{demo}<div class="bar3"><div class="accent"></div><div class="glass"><span class="name">{g("name")}</span><span class="role">{g("role")}</span></div></div>
<img class="seal" src="../design-system/assets/nnwa-seal.png" alt="">'''
    if L == "bookpage":
        return f'''{dots(d)}<div class="head"><div class="h2">{g("headline")}</div></div>
<div class="page" style="background-image:url(\'{src(g("page"))}\')"></div>{brandbar({"credit": g("credit")}, t)}'''
    if L == "report":
        cols = "".join(f'<div class="col"><div class="v">{c["v"]}<small>{c.get("u","")}</small></div><div class="k">{c["k"]}</div><div class="meter"><i style="width:{c.get("m",50)}%"></i></div></div>' for c in g("cols"))
        return f'''<div class="panel">{photo(d)}<div class="inner"><span class="label">{g("label","")}</span><div class="h1">{g("headline")}</div></div></div>
<div class="cols">{cols}</div><p class="fine">{g("fine","")}</p>{brandbar({"credit": g("credit")}, "paper")}'''
    raise SystemExit("unknown layout " + L)


def page(d):
    CTA["text"] = d.get("cta", "")
    w, h = SIZES.get(d["layout"], (1080, 1350))
    t = d.get("theme", "forest")
    transparent = "transparent" if d["layout"] == "lower" and not d.get("demo_bg") else ""
    html = f'''<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="../design-system/tokens.css"><link rel="stylesheet" href="components.css">
<style>:root{{--w:{w}px;--h:{h}px}}</style></head>
<body class="theme-{t} {transparent}"><div class="canvas l-{d["layout"]}">{body(d)}</div></body></html>'''
    return html, w, h


def shoot(browser, d, out_png):
    html, w, h = page(d)
    tmp = os.path.join(TPL, f"_render-{uuid.uuid4().hex[:8]}.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)
    try:
        pg = browser.new_page(viewport={"width": w, "height": h})
        pg.goto("file://" + tmp)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_load_state("networkidle")
        pg.wait_for_timeout(250)
        os.makedirs(os.path.dirname(os.path.abspath(out_png)), exist_ok=True)
        pg.screenshot(path=out_png, omit_background=d["layout"] == "lower")
        if d["layout"] != "lower":
            pg.screenshot(path=os.path.splitext(out_png)[0] + ".jpg", type="jpeg", quality=90)
        pg.close()
    finally:
        os.remove(tmp)
    print("wrote", out_png)


def jobs_for(data, out):
    if "slides" in data:
        n = len(data["slides"])
        for i, s in enumerate(data["slides"], 1):
            s.setdefault("dots", [i, n])
            yield s, os.path.join(out, f"{data.get('name','slide')}-{i:02d}.png")
    else:
        yield data, out


def main_node(data, out):
    jobs, tmps = [], []
    for d, png in jobs_for(data, out):
        html, w, h = page(d)
        tmp = os.path.join(TPL, f"_render-{uuid.uuid4().hex[:8]}.html")
        open(tmp, "w", encoding="utf-8").write(html)
        tmps.append(tmp)
        os.makedirs(os.path.dirname(os.path.abspath(png)), exist_ok=True)
        jobs.append({"html": tmp, "w": w, "h": h, "out": os.path.abspath(png), "transparent": d["layout"] == "lower" and not d.get("demo_bg")})
    jf = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    json.dump(jobs, jf)
    jf.close()
    try:
        subprocess.run(["node", os.path.join(SKILL, "scripts", "shoot.js"), jf.name], check=True)
    finally:
        for t in tmps + [jf.name]:
            os.remove(t)


def main(content, out):
    with open(content, encoding="utf-8") as f:
        data = json.load(f)
    if sync_playwright is None:
        return main_node(data, out)
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception:
            browser = p.chromium.launch(executable_path=os.environ.get("NNWA_CHROMIUM", "/opt/pw-browsers/chromium"), args=["--no-sandbox"])
        if "slides" in data:
            n = len(data["slides"])
            for i, s in enumerate(data["slides"], 1):
                s.setdefault("dots", [i, n])
                shoot(browser, s, os.path.join(out, f"{data.get('name','slide')}-{i:02d}.png"))
        else:
            shoot(browser, data, out)
        browser.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
