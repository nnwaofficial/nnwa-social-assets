"""Build the 21:30 'today's feed post' Story for each day (storywrap layout).

python3 wraps.py <render.py> <feed-dir-week1> <feed-dir-new> <out-dir>
"""
import json, os, subprocess, sys, tempfile
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calendar as cal  # noqa: E402  (this folder's calendar.py)

render_py, w1, new, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
W1 = {"guide-launch": "2026-11-01-guide-launch-01.png", "fibre": "2026-11-02-fibre.png", "protein": "2026-11-03-protein-01.png",
      "reel-500g": "2026-11-04-reel-cover-500g.png", "salt-check": "2026-11-05-salt-check.png", "half-your-plate": "2026-11-06-half-your-plate.png",
      "eat-the-colours": "2026-11-07-eat-the-colours.png", "learn-apply": "2026-11-08-learn-apply.png"}
jobs = []
for p in cal.P:
    if p.get("li_only"):
        continue
    days = [q for q in cal.P if q["d"] == p["d"] and not q.get("li_only")]
    if p is not days[-1]:
        continue
    slug = p["slug"]
    if slug in W1:
        feed = os.path.join(w1, W1[slug])
    else:
        base = os.path.join(new, f"{p['d']}-{slug}")
        feed = next((f for f in (base + ".png", base + "-01.png", os.path.join(new, f"{p['d']}-{slug}-cover.png")) if os.path.exists(f)), None)
    if not feed:
        print("missing feed for", slug); continue
    px = Image.open(feed).convert("L").resize((10, 10)).getpixel((0, 0))
    theme = "paper" if px < 128 else "forest"
    reel = "Reel" in p["fmt"]
    spec = dict(layout="storywrap", theme=theme, feed=os.path.abspath(feed), pill="New reel" if reel else "New post",
                headline=p["hook"].replace("NNWA", "NNWA"), bottom="Tap to watch" if reel else "Tap to see the post")
    jobs.append((spec, os.path.join(out, f"{p['d']}-{slug}-story.png")))
for spec, png in jobs:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(spec, f)
    subprocess.run([sys.executable, render_py, f.name, png], check=True, capture_output=True)
    os.remove(f.name)
    print("wrote", png)
