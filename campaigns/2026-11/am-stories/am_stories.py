"""Morning link Stories (09:00 IST, Instagram) for 1 to 30 Nov 2026.

Hrito, 31 Oct 2026: "add Stories with links to the free tools for each day's resource ... make the best informative design".
Each Story shows the free nnwa.in resource behind that day's feed post, with a link sticker to it.
Descriptions are taken from each resource page on nnwa.in (read 31 Oct 2026); no new health facts.

python3 am_stories.py            -> am-stories.json (render specs + Buffer link per day)
node render.js <out-dir>         -> 1080x1920 JPGs
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import calendar as cal  # noqa: E402  (campaign calendar.py)

# kind, headline (one <em> word), what-you-get rows, optional flow (inputs -> output) for calculators
R = {
    "starter": ("Free ebook", "Indian Diet <em>Starter</em> Guide",
                ["Balanced plates, built from Indian meals", "Portions you can picture", "Easy swaps, grounded in ICMR-NIN guidance"], None),
    "food-guide": ("Free guide", "Indian Foods and <em>Nutrients</em>",
                   ["What a plate actually contains", "Protein, iron and calcium in Indian foods", "Why absorption matters as much as intake"], None),
    "protein-calc": ("Free calculator", "Protein <em>Calculator</em>",
                     ["Your daily range, in grams", "Anchored to ICMR-NIN's 0.83 g per kg", "What the number can't tell you"],
                     (["Your weight", "Your goal"], "Daily protein range")),
    "bp-guide": ("Free guide", "High Blood Pressure <em>Diet</em>",
                 ["Where salt hides in Indian food", "Cutting salt without losing taste", "Potassium-rich Indian foods, with one caution"], None),
    "food-counter": ("Free calculator", "Indian Food Calorie <em>Counter</em>",
                     ["Count by the roti, bowl, plate and glass", "Calories and protein together", "Figures from ICMR-NIN's food tables"],
                     (["Roti", "Bowl", "Glass"], "Calories and protein for the meal")),
    "compare": ("Free comparison", "Every course, side by <em>side</em>",
                ["Fees, durations and certificates", "Who should take which course", "Choose a route before a course"], None),
    "become": ("Free guide", "How to become a <em>nutritionist</em> in India",
               ["The route, stage by stage", "For school leavers, graduates and career changers", "Choosing a qualification someone else can check"], None),
    "regional": ("Free guide", "Regional Indian <em>Diets</em>",
                 ["Why there's no single Indian diet", "Five questions that read any regional pattern", "Six regions, rice-and-fish to wheat-and-dairy"], None),
    "recipes": ("Free ebook (PDF)", "150 Indian <em>Recipes</em>",
                ["Real regional recipes", "A nutrition note on every one", "Time and servings for each dish"], None),
    "diabetes-risk": ("Free calculator", "Indian Diabetes <em>Risk</em> Score",
                      ["Four questions", "A score out of 100", "What to do about the result"],
                      (["Four questions"], "A score out of 100")),
    "prediabetes": ("Free guide", "Prediabetes <em>Diet</em> in India",
                    ["What prediabetes means, and the tests that show it", "What to change first in an Indian diet", "Rice and roti portions, and a sample day"], None),
    "evaluate": ("Free guide", "How to <em>check</em> a nutrition institute",
                 ["Seven checks before you enrol", "Legal entity, awarding body, named faculty", "Refund terms and verifiable certificates"], None),
    "pregnancy": ("Free guide", "Pregnancy <em>Diet</em> in India",
                  ["Nutrition, trimester by trimester", "Iron, folate, calcium and B12 foods", "Nausea, fasting and family myths"], None),
    "credentials": ("Free guide", "Nutrition <em>Credentials</em> in India",
                    ["NCVET, NSQF, NCrF and ISO, explained", "What each one actually claims", "A four-minute check for any provider"], None),
    "water-calc": ("Free calculator", "Water Intake <em>Calculator</em>",
                   ["A daily range, not a rule", "Built for Indian heat and outdoor work", "When more is too much"],
                   (["Weight", "Exercise", "Climate"], "Daily fluid range")),
    "tdee": ("Free calculator", "Daily Energy <em>Calculator</em>",
             ["Your maintenance calories", "Activity levels explained through Indian routines", "What the estimate can't tell you"],
             (["Body details", "Activity level"], "Maintenance calories")),
    "calorie": ("Free calculator", "Calorie <em>Calculator</em>",
                ["Maintenance, mild deficit and surplus", "A suggested macro split for Indian meals", "Choosing your activity level honestly"],
                (["Body details", "Activity level"], "Daily calorie needs")),
    "practice": ("Free guide", "Building a nutrition <em>practice</em>",
                 ["Scope: what a practice may and may not do", "GST, DPDP consent and advertising rules", "Pricing, clients and records"], None),
}

# 14 Nov has two feed posts; the Story follows World Diabetes Day.
PICK = {"2026-11-14": "diabetes-day"}


def day_posts():
    out = {}
    for p in cal.P:
        if p.get("li_only"):
            continue
        d = p["d"]
        if d in PICK and p["slug"] != PICK[d]:
            continue
        out.setdefault(d, p)
    return out


def main():
    specs = []
    for i, (d, p) in enumerate(sorted(day_posts().items())):
        g = cal.GREET_LEAD.get(p["slug"], {})
        mag = p.get("mag") or g.get("mag")
        course = p.get("course") or g.get("course")
        name, path = cal.MAG[mag]
        kind, head, rows, flow = R[mag]
        url = f"{cal.SITE}{path}?utm_source=instagram&utm_medium=story&utm_campaign={cal.CAMPAIGN}&utm_content={d}-am"
        clabel = "All NNWA courses" if course == "All courses" else course
        day = int(d[-2:])
        specs.append(dict(
            date=d, slug=p["slug"], file=f"{d}-am-{mag}.jpg", link=url, mag=mag,
            theme="forest" if day % 2 else "paper", day=f"{day:02d}", kind=kind, head=head, rows=rows,
            flow=flow, post=p["hook"], course=clabel, site="nnwa.in",
            alt=(f"NNWA morning Story, day {day} of November. Today's {kind.lower()}: {name}. "
                 f"What you get: {'; '.join(rows)}. Goes with today's post, '{p['hook']}'. "
                 f"Go deeper: {clabel}, 100% online. Link sticker to nnwa.in{path}."),
        ))
    json.dump(specs, open(os.path.join(HERE, "am-stories.json"), "w"), indent=1, ensure_ascii=False)
    print(len(specs), "stories")


if __name__ == "__main__":
    main()
