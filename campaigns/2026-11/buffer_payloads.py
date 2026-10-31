"""Build Buffer create_post payloads from calendar.py.

python3 buffer_payloads.py  ->  buffer-payloads.json (one create_post argument set per scheduled item)
Images and videos are served from the public repo on the branch below (raw.githubusercontent.com).
"""
import glob
import re
import json
import os

import calendar as cal  # local calendar.py (shadows the stdlib module on purpose)

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", "2026", "11"))
BRANCH = "claude/project-thread-gc5kzu"
RAW = f"https://raw.githubusercontent.com/nnwaofficial/nnwa-social-assets/{BRANCH}/2026/11/"
CH = {"instagram": "6ae4f9312f1f5ed64825c25d", "facebook": "6ae4f9992f1f5ed64825c8c2", "linkedin": "6ae4f9c42f1f5ed64825cb2f"}
LI_PDF = {"protein": "2026-11-03-protein-carousel-linkedin.pdf", "education-day": "2026-11-11-education-day-linkedin.pdf",
          "right-for-you": "2026-11-16-right-for-you-linkedin.pdf", "read-the-label": "2026-11-27-read-the-label-linkedin.pdf"}
STORY_ALT = "NNWA Story frame. {}"


def need(rel):
    if not os.path.exists(os.path.join(ASSETS, rel)):
        raise SystemExit(f"missing asset {rel}")
    return RAW + rel


def feed_files(p):
    slides = sorted(glob.glob(os.path.join(ASSETS, f"*-{p['slug']}-0[0-9].png")))
    if slides:
        return [os.path.basename(s) for s in slides]
    one = glob.glob(os.path.join(ASSETS, f"*-{p['slug']}.png"))
    if len(one) != 1:
        raise SystemExit(f"no unique feed image for {p['slug']}: {one}")
    return [os.path.basename(one[0])]


def cover(p):
    c = glob.glob(os.path.join(ASSETS, f"*{p['slug'].replace('reel-', 'reel-cover-')}.png")) + \
        glob.glob(os.path.join(ASSETS, f"*-{p['slug']}-cover.png"))
    return os.path.basename(c[0])


def split_alt(alt, n):
    """Per-slide alt text: 'Slide 1: ... Slide 2: ...' is split; otherwise slide 1 gets the full text."""
    if n == 1:
        return [alt]
    parts = re.split(r"(?=Slides? \d)", alt)
    if len(parts) == 1:
        return [alt] + [f"Slide {k} of {n}." for k in range(2, n + 1)]
    head = parts[0].strip()
    per = {}
    for part in parts[1:]:
        m = re.match(r"Slides? (\d+)(?: to (\d+))?", part)
        a, b = int(m.group(1)), int(m.group(2) or m.group(1))
        for k in range(a, b + 1):
            per[k] = part.strip()
    out = []
    for k in range(1, n + 1):
        t = per.get(k) or (alt if k == 1 else f"Slide {k} of {n}.")
        out.append((head + " " + t).strip() if k == 1 and head else t)
    return out


def images(files, alt):
    alts = split_alt(alt, len(files))
    return [{"image": {"url": need(f), "metadata": {"altText": t}}} for f, t in zip(files, alts)]


def due(it):
    return f"{it['date']}T{it['time']}:00+05:30"


def build():
    P = {p["slug"]: p for p in cal.P}
    out = []
    for it in cal.build():
        ch, typ = it["channel"], it["type"]
        a = dict(channelId=CH[ch], schedulingType="automatic", mode="customScheduled", dueAt=due(it))
        key = f"{it['date']} {it['time']} {ch} {typ} {it.get('slug') or it.get('asset')}"
        if typ == "story":
            stem = os.path.basename(it["asset"]).rsplit(".", 1)[0]
            wrap = stem[11:-6] if stem.endswith("-story") else None
            if wrap in P:
                alt = "Story version of today's post. " + split_alt(P[wrap].get("alt") or "", 9)[0]
            else:
                alt = "NNWA festival greeting Story for " + stem.split("story-", 1)[-1].replace("-", " ").title() + "."
            a["assets"] = images([it["asset"]], alt)
            if ch == "instagram":
                m = {"type": "story", "shouldShareToFeed": False}
                if it.get("link") and cal.GUIDE_LIVE:
                    m["link"] = it["link"]
                a["metadata"] = {"instagram": m}
            else:
                a["metadata"] = {"facebook": {"type": "story"}}
            out.append({"key": key, "args": a})
            continue
        p = P[it["slug"]]
        if ch == "linkedin":
            text, fc = cal.li_caption(p)
            a["text"] = text
            a["metadata"] = {"linkedin": {"firstComment": fc}} if fc else {}
            if p.get("li_asset"):
                a["assets"] = images([p["li_asset"]], p.get("li_alt") or p["alt"])
            elif p["slug"] in LI_PDF:
                first = feed_files(p)[0]
                a["assets"] = [{"document": {"url": need(LI_PDF[p["slug"]]), "title": p["hook"], "thumbnailUrl": need(first)}}]
            elif "Reel" in p["fmt"]:
                a["assets"] = [{"video": {"url": need(f"reels/{p['d']}-{p['slug']}.mp4")}}]
            else:
                a["assets"] = images(feed_files(p), p["alt"])
            out.append({"key": key, "args": a})
            continue
        ig, fb, fc_ig, fc_fb = cal.captions(p)
        if typ == "reel":
            a["assets"] = [{"video": {"url": need(f"reels/{p['d']}-{p['slug']}.mp4")}}]
        else:
            a["assets"] = images(feed_files(p), p["alt"])
        if ch == "instagram":
            a["text"] = ig
            a["metadata"] = {"instagram": {"type": typ, "shouldShareToFeed": True, "firstComment": fc_ig}}
        else:
            a["text"] = fb
            a["metadata"] = {"facebook": ({"type": typ, "firstComment": fc_fb} if fc_fb else {"type": typ})}
        out.append({"key": key, "args": a})
    return out


if __name__ == "__main__":
    items = build()
    json.dump(items, open(os.path.join(HERE, "buffer-payloads.json"), "w"), indent=1, ensure_ascii=False)
    print(len(items), "payloads")
