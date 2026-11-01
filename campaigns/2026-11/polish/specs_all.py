"""Collect every static November creative spec into one {output file: spec} map.

python3 polish/specs_all.py <out.json>
Sources: creatives.py (new creatives), week1-specs/ and the skill's v2 examples (1 to 8 Nov).
"""
import copy, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
CAMP = os.path.dirname(HERE)
sys.path.insert(0, CAMP)
import creatives as CR  # noqa: E402

EX = os.environ.get("NNWA_SKILL", "") + "/templates/examples/"
LM = "/mnt/project-files/lead-magnet-funnel/creative-source/"
W1CTA = "Free tools: nnwa.in"


def ld(p):
    return json.load(open(p))


def w1(p, **kw):
    d = ld(p)
    for s in d.get("slides", [d]):
        if "cta" in s:  # held guide link (nnwa.in/protein) -> Free tools, as on the other week-1 posts
            s["cta"] = W1CTA
    d.update(kw)
    return d


S = {}
S["2026-11-02-fibre.png"] = w1(os.path.join(CAMP, "week1-specs/d1-fibre-vword.json"))
S["2026-11-03-protein"] = w1(os.path.join(CAMP, "week1-specs/d2-protein-carousel.json"), name="2026-11-03-protein")
S["2026-11-04-reel-cover-500g.png"] = w1(EX + "d3-veg-reel.json")
S["2026-11-05-salt-check.png"] = w1(os.path.join(CAMP, "week1-specs/d4-salt-annot.json"))
S["2026-11-05-linkedin-numbers.png"] = w1(LM + "fmt-linkedin-report.json")
S["2026-11-06-half-your-plate.png"] = w1(LM + "d5-plate-glass.json")
S["2026-11-07-eat-the-colours.png"] = w1(LM + "d6-colours-tiles.json")
S["2026-11-08-learn-apply.png"] = w1(LM + "d7-brand-display.json")
for slug, spec in CR.C.items():
    spec = copy.deepcopy(spec)
    if spec.get("photo", "x") is None:
        spec["photo"] = "file://" + CR.EB + "f-dal.jpg"
    if "slides" in spec:
        S[slug] = spec
    else:
        S[slug + (".png")] = spec

if __name__ == "__main__":
    json.dump(S, open(sys.argv[1], "w"), indent=1)
    print(len(S), "specs")
