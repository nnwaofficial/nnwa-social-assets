"""Render specs and run the collision audit (Node Playwright).

python3 audit.py <skill-dir> <specs.json> <out-dir> [filter ...]
specs.json: {"<output file name>": spec, ...}; carousels expand to <name>-NN.png.
Writes PNG + JPG per creative, prints every collision and saves _audit.json.
"""
import json, os, subprocess, sys, tempfile, uuid
sys.path.insert(0, os.path.join(sys.argv[1], "scripts"))
import render as R  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

specs = json.load(open(sys.argv[2]))
out = os.path.abspath(sys.argv[3])
only = sys.argv[4:]
os.makedirs(out, exist_ok=True)
jobs, tmps = [], []
for fname, spec in specs.items():
    if only and not any(o in fname for o in only):
        continue
    items = [(s, f"{spec['name']}-{i:02d}.png") for i, s in enumerate(spec["slides"], 1)] if "slides" in spec else [(spec, fname)]
    for i, (s, png) in enumerate(items, 1):
        if "slides" in spec:
            s.setdefault("dots", [i, len(items)])
        html, w, h = R.page(s)
        tmp = os.path.join(R.TPL, f"_audit-{uuid.uuid4().hex[:8]}.html")
        open(tmp, "w").write(html)
        tmps.append(tmp)
        jobs.append({"html": tmp, "w": w, "h": h, "out": os.path.join(out, png), "transparent": False})
jf = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
json.dump(jobs, jf); jf.close()
try:
    subprocess.run(["node", os.path.join(HERE, "audit-shoot.js"), jf.name, os.path.join(out, "_audit.json")], check=True)
finally:
    for t in tmps + [jf.name]:
        os.remove(t)
