"""Export the whole November 2026 social calendar (as scheduled in Buffer) to Excel.

python3 export_xlsx.py <buffer-list-json> [<buffer-list-json> ...]  -> NNWA-November-2026-social-calendar.xlsx
The Buffer list files are raw list_posts results; they supply status and post IDs. Captions, first comments,
sources and CTAs come from buffer-payloads.json, am-stories/am-stories.json and highlights/start-here.json.
"""
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calendar as cal  # noqa: E402  (campaign calendar.py)

CH = {"6ae4f9312f1f5ed64825c25d": "Instagram", "6ae4f9992f1f5ed64825c8c2": "Facebook", "6ae4f9c42f1f5ed64825cb2f": "LinkedIn"}
IST = timezone(timedelta(hours=5, minutes=30))
RAW_AM = "https://raw.githubusercontent.com/nnwaofficial/nnwa-social-assets/claude/project-thread-gc5kzu/2026/11/stories/am/"
RAW_HL = "https://raw.githubusercontent.com/nnwaofficial/nnwa-social-assets/claude/project-thread-gc5kzu/2026/11/highlights/"

HL = {  # Instagram Highlight for the 21:30 feed-repost Stories (see highlights/HIGHLIGHTS.md)
    "Start here": {"seventeen", "reel-sources"},
    "Courses": {"learn-apply", "education-day", "right-for-you", "make-it-your-work"},
    "Eat well": {"fibre", "reel-500g", "salt-check", "half-your-plate", "eat-the-colours", "reel-oil", "sugar", "first-six-months",
                 "millets", "water", "reel-move", "read-the-label", "swaps"},
    "Protein": {"protein", "supplements-myth", "reel-breakfasts", "milk-day"},
    "The numbers": {"diabetes-day", "mens-day", "reel-recap"},
    "Festivals": {"diwali", "bhai-dooj", "chhath", "gurpurab"},
}
FESTIVAL_NAMES = {"dhanteras": "Dhanteras", "choti-diwali-oil": "Choti Diwali", "diwali": "Diwali", "govardhan": "Govardhan Puja",
                  "bhai-dooj": "Bhai Dooj", "chhath-arghya": "Chhath Puja", "gurpurab": "Guru Nanak Jayanti"}


def post_by_slug(slug):
    for p in cal.P:
        if p["slug"] == slug:
            return p
    return None


def utc_key(channel_id, due):
    t = datetime.fromisoformat(due).astimezone(timezone.utc)
    return channel_id, t.strftime("%Y-%m-%dT%H:%M")


def lead(p):
    if not p:
        return "", ""
    g = cal.GREET_LEAD.get(p["slug"], {})
    mag = p.get("mag") or g.get("mag")
    course = p.get("course") or g.get("course") or ""
    res = f"{cal.MAG[mag][0]} ({cal.SITE}{cal.MAG[mag][1]})" if mag else ""
    if course:
        course = f"{course} ({cal.SITE}{cal.CRS[course]})"
    return res, course


def rows():
    out = []
    pay = json.load(open(os.path.join(HERE, "buffer-payloads.json")))
    pay = pay if isinstance(pay, list) else list(pay.values())[0]
    for x in pay:
        a = x["args"]
        date, time, _ch, typ, rest = x["key"].split(" ", 4)
        plat = CH[a["channelId"]]
        meta = list(a.get("metadata", {}).values())[0] if a.get("metadata") else {}
        assets = a.get("assets", [])
        urls = [list(v.values())[0]["url"] for v in assets]
        alts = [list(v.values())[0].get("metadata", {}).get("altText", "") or list(v.values())[0].get("title", "") for v in assets]
        hl = ""
        if typ == "story":
            fname = rest.split("/")[-1]
            if "-story-" in fname:  # festival greeting
                fest = fname.split("-story-")[1].rsplit(".", 1)[0]
                p, fmt, title, hl = None, "Story, festival greeting", f"{FESTIVAL_NAMES.get(fest, fest)} greeting", "Festivals"
            else:
                slug = fname[len(date) + 1:].rsplit("-story", 1)[0]
                p = post_by_slug(slug)
                fmt, title = "Story, today's post", (p["hook"] if p else slug)
                hl = next((k for k, v in HL.items() if slug in v), "")
            if plat != "Instagram":
                hl = ""
        else:
            p = post_by_slug(rest)
            fmt = p["fmt"] if p else ""
            if plat == "LinkedIn" and rest in ("protein", "education-day", "right-for-you", "read-the-label"):
                fmt = "LinkedIn document (PDF carousel)"
            elif typ == "reel":
                fmt = "Reel (motion graphics, original music)"
            title = p["hook"] if p else rest
        res, course = lead(p) if typ != "story" else ("", "")
        src = "; ".join(cal.sources(p)) if (p and typ != "story") else ""
        out.append(dict(date=date, time=time, platform=plat, type=typ.capitalize(), fmt=fmt, title=title,
                        caption=a.get("text", ""), comment=meta.get("firstComment") or "", resource=res, course=course,
                        link=meta.get("link", ""), assets="\n".join(urls), alt="\n".join(alts), sources=src, hl=hl,
                        key=utc_key(a["channelId"], a["dueAt"])))
    # 09:00 morning link Stories
    seen = set()
    for s in json.load(open(os.path.join(HERE, "am-stories", "am-stories.json"))):
        name, path = cal.MAG[s["mag"]]
        hl = "Free tools" if s["mag"] not in seen else ""
        seen.add(s["mag"])
        out.append(dict(date=s["date"], time="09:00", platform="Instagram", type="Story", fmt="Story, morning link sticker",
                        title=f"Today's {s['kind'].lower()}: {name}", caption="", comment="", resource=f"{name} ({cal.SITE}{path})",
                        course=s["course"], link=s["link"], assets=RAW_AM + s["file"], alt=s["alt"], sources="", hl=hl,
                        key=utc_key("6ae4f9312f1f5ed64825c25d", s["date"] + "T09:00:00+05:30")))
    # Start here Stories (for the Highlight)
    for i, f in enumerate(json.load(open(os.path.join(HERE, "highlights", "start-here.json")))):
        t = f"18:0{i}"
        out.append(dict(date="2026-11-01", time=t, platform="Instagram", type="Story", fmt="Story, Start here (Highlight)",
                        title=f"Start here {i + 1} of 3: " + f["head"].replace("<em>", "").replace("</em>", ""), caption="", comment="",
                        resource="Free calculators and guides (https://nnwa.in/tools/)" if i == 2 else "", course="",
                        link="https://nnwa.in/tools/?utm_source=instagram&utm_medium=story&utm_campaign=nov-2026&utm_content=start-here" if i == 2 else "",
                        assets=RAW_HL + f"start-here-{i + 1}.jpg", alt=" ".join(r.replace("&amp;", "&") for r in f["rows"]), sources="",
                        hl="Start here", key=utc_key("6ae4f9312f1f5ed64825c25d", f"2026-11-01T{t}:00+05:30")))
    return out


def main(files):
    buf = {}
    for f in files:
        d = json.loads(json.load(open(f))[0]["text"])
        for e in d["edges"]:
            n = e.get("node", e)
            t = datetime.fromisoformat(n["dueAt"].replace("Z", "+00:00"))
            buf.setdefault((n["channelId"], t.strftime("%Y-%m-%dT%H:%M")), []).append(n)
    R = rows()
    for r in R:
        cands = buf.get(r["key"], [])
        # two posts can share a minute (24 Nov 09:00 IG feed + Story): match Stories to the item without caption text
        n = next((x for x in cands if bool(x.get("text")) == bool(r["caption"])), cands[0] if cands else None)
        if n:
            cands.remove(n)
        r["status"] = n["status"] if n else "NOT IN BUFFER"
        r["bid"] = n["id"] if n else ""
    extra = [x for v in buf.values() for x in v]
    R.sort(key=lambda r: (r["date"], r["time"], ["Instagram", "Facebook", "LinkedIn"].index(r["platform"])))

    wb = Workbook()
    forest, brass, paper, sage = "123A2F", "C8A04B", "FBF8F1", "E3ECE6"
    hfont = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
    hfill = PatternFill("solid", fgColor=forest)
    thin = Side(style="thin", color="D9D4C7")
    wrap = Alignment(wrap_text=True, vertical="top")

    # ---- Read me ----
    ws = wb.active
    ws.title = "Read me"
    info = [
        ("NNWA social media calendar: November 2026", None),
        ("Exported 1 Nov 2026 (IST) from Buffer and the campaign source files. All times IST.", None),
        ("", None),
        ("Scheduled in Buffer", f"{sum(1 for r in R if r['status'] == 'scheduled')} of {len(R)} rows (status checked live in Buffer at export)"),
        ("Channels", "Instagram nnwa.official, Facebook NNWA page, LinkedIn NNWA page"),
        ("Campaign rules", "Facts only from Indian government sources, cited in captions and first comments; no fees, dates or seats in posts; no outcome promises; 3 to 5 hashtags; no emojis; alt text on every image."),
        ("Held", "1 Nov 'Protein, decoded' guide launch is held until nnwa.in/protein is live."),
        ("Next batches (not in posts)", "11 Nov 2026 and 11 Dec 2026. The website moves to 11 Dec on 12 Nov."),
        ("Your actions", "Set the Instagram bio link to nnwa.in/tools/. Play one reel with sound before 4 Nov. Build the 7 Instagram Highlights (see 'IG Highlight' column)."),
        ("Asset links", "Raw GitHub URLs on branch claude/project-thread-gc5kzu. Do not delete the branch before 1 Dec 2026."),
        ("Sheets", "Calendar (every scheduled item), Daily summary, Sources."),
    ]
    for i, (k, v) in enumerate(info, 1):
        ws.cell(i, 1, k)
        if v:
            ws.cell(i, 2, v).alignment = wrap
            ws.cell(i, 1).font = Font(bold=True, color=forest)
    ws["A1"].font = Font(bold=True, size=16, color=forest)
    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 110

    # ---- Calendar ----
    ws = wb.create_sheet("Calendar")
    cols = [("Date", 11), ("Day", 6), ("Time (IST)", 9), ("Platform", 11), ("Type", 8), ("Format", 26), ("Title / hook", 38),
            ("Caption", 70), ("First comment", 60), ("Free resource (CTA)", 40), ("Course", 40), ("Story link sticker", 40),
            ("Asset URL(s)", 50), ("Alt text", 50), ("Sources (government)", 40), ("IG Highlight", 13), ("Buffer status", 12), ("Buffer post ID", 26)]
    for j, (h, w) in enumerate(cols, 1):
        c = ws.cell(1, j, h)
        c.font, c.fill, c.alignment = hfont, hfill, Alignment(vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(j)].width = w
    pfill = {"Instagram": PatternFill("solid", fgColor="F6EFE0"), "Facebook": PatternFill("solid", fgColor="E8EEF6"), "LinkedIn": PatternFill("solid", fgColor=sage)}
    for i, r in enumerate(R, 2):
        d = datetime.fromisoformat(r["date"])
        vals = [d.date(), d.strftime("%a"), r["time"], r["platform"], r["type"], r["fmt"], r["title"], r["caption"], r["comment"],
                r["resource"], r["course"], r["link"], r["assets"], r["alt"], r["sources"], r["hl"], r["status"], r["bid"]]
        for j, v in enumerate(vals, 1):
            c = ws.cell(i, j, v)
            c.alignment = wrap
            c.border = Border(bottom=thin)
        ws.cell(i, 1).number_format = "dd mmm yyyy"
        ws.cell(i, 4).fill = pfill[r["platform"]]
        if r["status"] != "scheduled":
            ws.cell(i, 17).font = Font(bold=True, color="B00020")
        ws.row_dimensions[i].height = 90 if r["caption"] else 45
    ws.freeze_panes = "E2"
    tab = Table(displayName="Calendar", ref=f"A1:{get_column_letter(len(cols))}{len(R) + 1}")
    tab.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showRowStripes=False)
    ws.add_table(tab)

    # ---- Daily summary ----
    ws = wb.create_sheet("Daily summary")
    heads = ["Date", "Day", "IG feed/reel", "IG Stories", "FB feed/reel", "FB Stories", "LinkedIn", "Total", "Feed topic"]
    for j, h in enumerate(heads, 1):
        c = ws.cell(1, j, h)
        c.font, c.fill = hfont, hfill
    by = defaultdict(Counter)
    topic = defaultdict(list)
    for r in R:
        k = r["platform"][:2] + ("S" if r["type"] == "Story" else "F")
        by[r["date"]][k] += 1
        if r["platform"] == "Instagram" and r["type"] != "Story":
            topic[r["date"]].append(r["title"])
    tot = Counter()
    for i, dte in enumerate(sorted(by), 2):
        c = by[dte]
        row = [datetime.fromisoformat(dte).date(), datetime.fromisoformat(dte).strftime("%a"), c["InF"], c["InS"], c["FaF"], c["FaS"],
               c["LiF"], sum(c.values()), " | ".join(topic[dte])]
        for j, v in enumerate(row, 1):
            ws.cell(i, j, v)
        ws.cell(i, 1).number_format = "dd mmm yyyy"
        tot.update(c)
    n = len(by) + 2
    ws.cell(n, 1, "Total").font = Font(bold=True)
    for j, k in enumerate(["InF", "InS", "FaF", "FaS", "LiF"], 3):
        ws.cell(n, j, f"=SUM({get_column_letter(j)}2:{get_column_letter(j)}{n - 1})").font = Font(bold=True)
    ws.cell(n, 8, f"=SUM(H2:H{n - 1})").font = Font(bold=True)
    for j, w in enumerate([12, 6, 12, 10, 12, 10, 10, 8, 80], 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = "A2"

    # ---- Sources ----
    ws = wb.create_sheet("Sources")
    for j, h in enumerate(["Key", "Source", "Where", "What it supports"], 1):
        c = ws.cell(1, j, h)
        c.font, c.fill = hfont, hfill
    i = 2
    for line in open(os.path.join(HERE, "sources.md")):
        if line.startswith("| ") and not line.startswith("| Key") and not line.startswith("|---"):
            parts = [x.strip() for x in line.strip().strip("|").split("|")]
            for j, v in enumerate(parts[:4], 1):
                ws.cell(i, j, v).alignment = wrap
            i += 1
    for j, w in enumerate([14, 50, 30, 90], 1):
        ws.column_dimensions[get_column_letter(j)].width = w

    out = os.path.join(HERE, "NNWA-November-2026-social-calendar.xlsx")
    wb.save(out)
    print(out, len(R), "rows;", Counter(r["status"] for r in R), "; in Buffer but not in sources:", len(extra))
    for n in extra:
        print("  extra", n["id"], n["channelService"], n["dueAt"])


if __name__ == "__main__":
    main(sys.argv[1:])
