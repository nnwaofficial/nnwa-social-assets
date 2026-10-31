"""Content specs for every new NNWA November 2026 creative (design system v2).

python3 creatives.py <render.py> <out-dir> [slug ...]
Renders each spec with the skill's render.py (lead-magnet version + storywrap layout).
Photos are Pexels (free licence), loaded from the Pexels CDN; credit line "Photo via Pexels".
No inline citations on creatives (Hrito's rule): sources sit in captions and first comments.
"""
import json
import os
import subprocess
import sys
import tempfile


def px(i, w=1600):
    return f"https://images.pexels.com/photos/{i}/pexels-photo-{i}.jpeg?auto=compress&cs=tinysrgb&w={w}"


GUIDE = "Free guide: nnwa.in/protein"
COURSES = "Courses: nnwa.in/courses"
CR = "Photo via Pexels"
EB = "/mnt/project-files/ebooks/protein-decoded/source-v3/photos/"

C = {}

# ---------------- Week 1 additions ----------------
C["2026-11-08-diwali"] = dict(layout="glass", theme="photo", photo=px(13689170), credit=CR,
    pill="Happy Diwali", headline="May your home be <em>bright</em> and your table be shared.",
    body="From all of us at NNWA (Nutrition &amp; Wellness Academy).")
C["2026-11-06-li-disease-burden"] = dict(layout="stat", theme="paper", photo=px(8818732), credit=CR, label="Why nutrition literacy matters",
    pill="Indian data", number="56.4", unit="%", stat_label="of India's total disease burden is due to unhealthy diets.",
    chips=["Healthy diets and activity can prevent up to 80% of type 2 diabetes"], cta=GUIDE)

# Festival greeting Stories (1080x1920, no sticker)
C["2026-11-06-story-dhanteras"] = dict(layout="story", theme="photo", photo=px(31372002), credit=CR, pill="Dhanteras",
    label="Shubh Dhanteras", headline="The best <em>wealth</em> is health.", body="Wishing you and your family a happy Dhanteras.", bottom="nnwa.in")
C["2026-11-07-story-choti-diwali-oil"] = dict(layout="story", theme="photo", photo=px(6823599), credit=CR, pill="Frying tonight?",
    label="Kitchen tip", headline="Fried once? <em>Filter</em> it.", body="Use the oil for curries within a day or two, and don't fry with it again. ICMR-NIN advice.", bottom="nnwa.in")
C["2026-11-08-story-diwali"] = dict(layout="story", theme="photo", photo=px(6103203), credit=CR, pill="Happy Diwali",
    label="Shubh Deepavali", headline="Light, family and a <em>shared</em> plate.", body="From all of us at NNWA.", bottom="nnwa.in")
C["2026-11-09-story-govardhan"] = dict(layout="story", theme="photo", photo=px(7685644), credit=CR, pill="Govardhan Puja",
    label="Annakut", headline="Grateful for every <em>harvest</em>.", body="Wishing you a happy Govardhan Puja.", bottom="nnwa.in")
C["2026-11-10-story-bhai-dooj"] = dict(layout="story", theme="photo", photo=px(7685644), credit=CR, pill="Bhai Dooj",
    label="Happy Bhai Dooj", headline="Gift a <em>habit</em> this year.", body="A walk together lasts longer than the sweets. New post today.", bottom="nnwa.in")
C["2026-11-15-story-chhath-arghya"] = dict(layout="story", theme="photo", photo=px(28975092), credit=CR, pill="Chhath Puja",
    label="Sandhya Arghya", headline="Gratitude to the <em>setting</em> sun.", body="To everyone at the ghats today: may your prayers be answered.", bottom="nnwa.in")
C["2026-11-24-story-gurpurab"] = dict(layout="story", theme="photo", photo=px(8818732), credit=CR, pill="Gurpurab",
    label="Guru Nanak Jayanti", headline="Everyone sits <em>together</em>.", body="Wishing you a blessed Guru Nanak Jayanti.", bottom="nnwa.in")
C["course-story-link"] = dict(layout="story", theme="photo", photo=px(8055482), credit=CR, pill="NNWA courses",
    label="100% online", headline="Make nutrition your <em>work</em>.", body="Explore NNWA's courses and talk to a counsellor. Tap the link.", bottom="nnwa.in/courses")

# ---------------- Week 2 ----------------
C["2026-11-10-bhai-dooj"] = dict(name="2026-11-10-bhai-dooj", slides=[
    dict(layout="glass", theme="photo", photo=px(7685644), credit=CR, pill="Bhai Dooj", headline="This Bhai Dooj, gift a <em>habit</em>.",
         body="Add one thing to the tilak and the sweets: something you can do together.", cta=GUIDE),
    dict(layout="step", theme="forest", index="01", headline="Walk <em>together</em>.", photo=px(7880267), photo_tag="30 to 60 minutes",
         body="ICMR-NIN suggests 30 to 60 minutes of moderate activity a day, at least five days a week. A brisk evening walk counts.", credit=CR, cta=GUIDE),
    dict(layout="step", theme="paper", index="02", headline="Add <em>nuts</em> to the mithai box.", photo=px(529632), photo_tag="A better swap",
         body="The Dietary Guidelines for Indians list nuts and seeds as the swap for deep-fried snacks.", credit=CR, cta=GUIDE),
    dict(layout="step", theme="forest", index="03", headline="Share one <em>home-cooked</em> meal.", photo=px(8818732), photo_tag="Half the plate",
         body="Make half the plate vegetables and fruit, the way ICMR-NIN's My Plate for the Day does.", credit=CR, cta=GUIDE),
    dict(layout="cta", theme="paper", headline="Habits last longer than <em>sweets</em>.",
         body="Our free guide, Protein, decoded, has eight easy wins you can share with your sibling.", pill="nnwa.in/protein"),
])
C["2026-11-15-sugar"] = dict(layout="annot", theme="paper", photo=px(13466248), credit=CR, label="After the festival",
    headline="20 to 25 g of <em>sugar</em> a day, at most.",
    tags=[["ICMR-NIN advice", "Avoid added sugar, or keep it to 20 to 25 g a day"], ["Count it all", "Tea, sweets and drinks add up together"]], cta=GUIDE)
C["2026-11-11-education-day"] = dict(name="2026-11-11-education-day", slides=[
    dict(layout="vword", theme="forest", label="National Education Day", word="learn", photo=px(8055482), credit=CR,
         note="Where do you <em>start</em> with nutrition? Four routes, all 100% online.", cta=COURSES),
    dict(layout="step", theme="paper", index="01", headline="Curious? Start <em>small</em>.", body="Introduction to Nutrition is a short first step into how food works.", photo=px(7683820), photo_tag="Short course", credit=CR,
         chips=["Short course", "100% online"], cta=COURSES),
    dict(layout="step", theme="forest", index="02", headline="Want the <em>full</em> grounding?", body="The Certification in Nutrition covers the foundations in depth.", photo=px(4492194), photo_tag="Flagship", credit=CR,
         chips=["Flagship programme", "100% online"], cta=COURSES),
    dict(layout="step", theme="paper", index="03", headline="The most <em>complete</em> pathway.", body="The Diploma in Nutrition, Dietetics &amp; Public Health.", photo=px(7420512), photo_tag="Flagship", credit=CR,
         chips=["Flagship programme", "100% online"], cta=COURSES),
    dict(layout="step", theme="forest", index="04", headline="Know your <em>area</em>?", body="Specialise: Diabetes Educator, Sports Nutrition, Child Nutrition, Food Science &amp; FSSAI and more.", photo=px(7421117), photo_tag="Specialise", credit=CR,
         chips=["Specialisations", "100% online"], cta=COURSES),
    dict(layout="cta", theme="paper", headline="Find your <em>route</em>.", body="Fees, dates and eligibility are on each course page. A counsellor can help you choose.", pill="nnwa.in/courses"),
])
C["2026-11-13-chhath"] = dict(layout="glass", theme="photo", photo=px(28975092), credit=CR, pill="Chhath Puja",
    headline="Gratitude to the <em>sun</em>.", body="To everyone observing Chhath, from all of us at NNWA: may your prayers be answered and your families be well.")
C["2026-11-14-childrens-day"] = dict(name="2026-11-14-childrens-day", slides=[
    dict(layout="stat", theme="paper", photo=px(8954918), credit=CR, label="Children's Day", pill="Indian data", number="40.6", unit="%",
         stat_label="of children aged 1 to 4 in India have anaemia.", chips=["What the numbers ask of us, and what helps"], cta=COURSES),
    dict(layout="step", theme="forest", index="01", headline="Anaemia, by <em>age</em>.", body="Children with anaemia in India.", photo=px(8818732), photo_tag="Iron-rich, varied meals", credit=CR,
         chips=["Age 1 to 4: 40.6%", "Age 5 to 9: 23.5%", "Age 10 to 19: 28.4%", "National survey data"], cta=COURSES),
    dict(layout="step", theme="paper", index="02", headline="About 1 in 10 shows <em>pre-diabetes</em>.", body="10.3% of children aged 5 to 9 and 10.4% of those aged 10 to 19.", photo=px(18488302), photo_tag="Fewer sweets, more play", credit=CR,
         chips=["Age 5 to 9: 10.3%", "Age 10 to 19: 10.4%"], cta=COURSES),
    dict(layout="step", theme="forest", index="03", headline="What <em>helps</em>.", body="From ICMR-NIN's Dietary Guidelines for Indians (2024).",
         chips=["Varied home-cooked food", "Semi-solid foods from 6 months", "60 minutes of play a day", "Fewer HFSS snacks"], cta=COURSES),
    dict(layout="cta", theme="paper", headline="For everyone who feeds a <em>child</em>.", body="Child &amp; Adolescent Nutrition, 100% online at NNWA.", pill="nnwa.in/courses"),
])
C["2026-11-14-diabetes-day"] = dict(layout="stat", theme="forest", photo=px(7420512), credit=CR, label="World Diabetes Day", pill="NFHS-5, adults 18 to 69",
    number="15.6", unit="%", stat_label="of Indian men have diabetes, and 13.5% of women.",
    chips=["Up from 10.5% and 9.7% in 2016", "Healthy diets and activity can prevent up to 80% of type 2 diabetes"], cta=COURSES)

# ---------------- Week 3 ----------------
Q = ["Do you enjoy <em>explaining</em> things to people?", "Will you <em>check</em> a claim before you share it?", "Can you give a few <em>hours</em> a week?",
     "Do you know <em>who</em> you want to help?", "A certificate is a <em>start</em>. Are you ready for the rest?"]
QB = ["Most of nutrition work is conversation: with families, clients and patients.", "Good advice starts with a source. Ours is always ICMR-NIN or FSSAI.",
      "Steady study beats cramming. Online courses fit around work and home.", "Families, athletes, people with diabetes, children: each needs different knowledge.",
      "Knowledge and a certificate open the door. What you do with them is what counts."]
QP = [8489749, 7420735, 8055482, 8954918]
QT = ["Conversation", "Sources", "Time", "Your people"]
C["2026-11-16-right-for-you"] = dict(name="2026-11-16-right-for-you", slides=[
    dict(layout="step", theme="paper", index="5", headline="Is a nutrition course right for <em>you</em>?", body="Five honest questions to answer before you enrol. Swipe.", photo=px(4492194), photo_tag="Before you enrol", credit=CR, cta=COURSES),
] + [dict(layout="step", theme=("forest" if i % 2 == 0 else "paper"), index=f"0{i+1}", headline=Q[i], body=QB[i], photo=px(QP[i]), photo_tag=QT[i], credit=CR, cta=COURSES) for i in range(4)] + [
    dict(layout="cta", theme="forest", headline=Q[4], body=QB[4] + " Mostly yes? Explore NNWA's courses, 100% online.", pill="nnwa.in/courses"),
])
C["2026-11-17-first-six-months"] = dict(layout="glass", theme="photo", photo=px(19380232), credit=CR, pill="National Newborn Week",
    headline="The first six months: breast milk <em>only</em>.", body="Then homemade semi-solid foods, with breastfeeding continued to two years and beyond. ICMR-NIN.", cta=COURSES)
C["2026-11-19-mens-day"] = dict(layout="stat", theme="paper", photo=px(7880267), credit=CR, label="International Men's Day", pill="NFHS-5, men 18 to 69",
    number="24.0", unit="%", stat_label="of Indian men have hypertension, up from 20.2% in 2016.",
    chips=["Salt: not more than 5 g a day", "Move: 30 to 60 minutes, five days a week"], cta=GUIDE)
C["2026-11-20-millets"] = dict(name="2026-11-20-millets", slides=[
    dict(layout="stat", theme="forest", photo=px(7420512), credit=CR, label="Shree Anna", pill="ICMR-NIN", number="20 to 30", unit="%",
         stat_label="of the cereals adults eat should be millets (raw weight).", chips=["Three easy ways to get there"], cta=GUIDE),
    dict(layout="step", theme="paper", index="01", headline="One <em>bajra</em> or jowar roti a day.", body="Swap one wheat roti at lunch or dinner.", photo=px(7421117), photo_tag="Easy swap", credit=CR, cta=GUIDE),
    dict(layout="step", theme="forest", index="02", headline="Ragi in the <em>dosa</em> batter.", body="Mix ragi flour into dosa, idli or chilla batter.", photo=px(7420512), photo_tag="Breakfast", credit=CR, cta=GUIDE, chips=["Breakfast", "Snacks"]),
    dict(layout="step", theme="paper", index="03", headline="Millet <em>khichdi</em>, with dal.", body="Once or twice a week. Millet with dal also gives a better protein mix.", photo="file://" + EB + "f-dal.jpg", photo_tag="With dal", credit=CR, cta=GUIDE, chips=["Dinner", "Better protein mix"]),
    dict(layout="cta", theme="forest", headline="Pair millets with <em>protein</em>.", body="Chapter 4 of our free guide, Protein, decoded, shows the combinations.", pill="nnwa.in/protein"),
])
C["2026-11-21-supplements-myth"] = dict(layout="glass", theme="photo", photo=None, credit=CR, pill="Myth check",
    headline="Protein powder to build muscle? ICMR-NIN says <em>avoid</em>.", body="Combine foods instead: dal with rice or roti, milk and curd, eggs, paneer, fish and chicken.", cta=GUIDE)

# ---------------- Week 4 ----------------
C["2026-11-23-water"] = dict(layout="stat", theme="forest", photo=px(7904429), credit=CR, label="Winter reminder", pill="ICMR-NIN",
    number="8", unit="glasses", stat_label="of water a day, about 2 litres, including other drinks.", chips=["Keep a bottle in sight", "A glass with every meal"], cta=GUIDE)
C["2026-11-24-gurpurab"] = dict(layout="glass", theme="photo", photo=px(8818732), credit=CR, pill="Guru Nanak Jayanti",
    headline="Everyone sits together. Everyone is <em>fed</em>.", body="Wishing you and your family a blessed Gurpurab, from all of us at NNWA.")
C["2026-11-26-milk-day"] = dict(layout="annot", theme="paper", photo=px(8489749), credit=CR, label="National Milk Day",
    headline="300 ml of milk or <em>curd</em> a day.", tags=[["About 10 g protein", "A glass of milk and a katori of dahi"], ["ICMR-NIN", "Part of My Plate for the Day"]], cta=GUIDE)
C["2026-11-27-read-the-label"] = dict(name="2026-11-27-read-the-label", slides=[
    dict(layout="vword", theme="paper", label="Food Science &amp; FSSAI", word="label", photo=px(7420735), credit=CR,
         note="Read any Indian food label in <em>four</em> steps.", cta=COURSES),
    dict(layout="step", theme="forest", index="01", headline="The <em>veg</em> or non-veg symbol.", body="A green or brown mark, required by FSSAI on packaged food.", photo=px(7420735), photo_tag="Step 1", credit=CR, cta=COURSES),
    dict(layout="step", theme="paper", index="02", headline="The FSSAI logo and <em>licence</em> number.", body="It tells you who is responsible for the food.", photo=px(529632), photo_tag="Step 2", credit=CR, cta=COURSES),
    dict(layout="step", theme="forest", index="03", headline="Ingredients, in order of <em>weight</em>.", body="The first ingredient is the one there's most of.", photo=px(7421117), photo_tag="Step 3", credit=CR, cta=COURSES),
    dict(layout="step", theme="paper", index="04", headline="Nutrition <em>information</em>.", body="Per 100 g or per pack. Compare products on the same basis.", photo=px(13466248), photo_tag="Step 4", credit=CR, cta=COURSES),
    dict(layout="cta", theme="forest", headline="Go deeper into food <em>standards</em>.", body="Food Science &amp; FSSAI, 100% online at NNWA.", pill="nnwa.in/courses"),
])
C["2026-11-28-swaps"] = dict(layout="tiles", theme="paper", label="ICMR-NIN swaps", headline="Swap, don't <em>stop</em>.", cta=GUIDE, credit=CR, tiles=[
    dict(photo=px(529632), title="Nuts and seeds", sub="for deep-fried snacks"),
    dict(photo=px(5965988), pos="30% center", title="Whole fruit", sub="for fruit juice"),
    dict(photo=px(18488302), title="Traditional sweets", sub="with whole grains, millets, nuts"),
    dict(photo=px(8489749), title="Buttermilk", sub="for sugary drinks"),
])
C["2026-11-30-make-it-your-work"] = dict(layout="display", theme="photo", photo=px(1546027), credit=CR, label="Admissions open", kicker="Nutrition &amp; Wellness Academy",
    words=["learn", "teach"], sub="Make it your work. 100% online courses in nutrition and wellness, built on Indian guidelines.", cta=COURSES)

# Reel covers (1080x1920). Motion reels are built by reels.py from REELS below.
C["2026-11-12-reel-oil-cover"] = dict(layout="reel", theme="photo", photo=px(6823599), pill="Kitchen check", number="30", unit="g", headline="of oil a day, at most. And never fry <em>twice</em>.")
C["2026-11-18-reel-sources-cover"] = dict(layout="reel", theme="photo", photo=px(4492194), pill="How we work", number="100", unit="%", headline="of our numbers come from Indian <em>government</em> sources.")
C["2026-11-22-reel-breakfasts-cover"] = dict(layout="reel", theme="photo", photo="file://" + EB + "f-dal.jpg", pill="Protein, counted", number="3", unit="breakfasts", headline="Indian, everyday and <em>counted</em>.")
C["2026-11-25-reel-move-cover"] = dict(layout="reel", theme="photo", photo=px(7880267), pill="Move more", number="30", unit="min", headline="five days a week. A brisk <em>walk</em> counts.")
C["2026-11-29-reel-recap-cover"] = dict(layout="reel", theme="photo", photo=px(7420512), pill="Save this", number="6", unit="numbers", headline="from November, all from <em>ICMR-NIN</em>.")

# Motion reels: list of scenes (story layout, no sticker). Each scene ~3.5 s with a slow zoom; end card last.
END = dict(layout="story", theme="forest", photo=None, pill="Free guide", label="Protein, decoded", headline="Get the free <em>guide</em>.", body="34 pages. Every fact from ICMR-NIN and FSSAI. Link in bio.", bottom="nnwa.in/protein")
REELS = {
    "2026-11-04-reel-500g": [("Plate check", "What does <em>500 g</em> look like?", "Vegetables and fruit, every day.", 12765459),
                             ("ICMR-NIN", "<em>400 g</em> of vegetables.", "And 100 g of fruit, for a 2,000 kcal day.", 17223838),
                             ("Try this", "Two katoris of <em>sabzi</em>.", "Plus a bowl of salad and a plate of greens.", 12765459),
                             ("And", "One whole <em>fruit</em>.", "That's about half your plate.", 5965988),
                             ("Next", "The other half needs <em>protein</em>.", "Our free guide shows how.", 8818732)],
    "2026-11-12-reel-oil": [("Kitchen check", "The oil from Diwali. Fry <em>again</em>?", "", 6823599),
                            ("ICMR-NIN", "Reheating oil forms <em>harmful</em> compounds.", "", 6823599),
                            ("Instead", "<em>Filter</em> it. Use it for curries.", "Within a day or two.", 8818732),
                            ("Rule", "Don't fry with it <em>again</em>.", "", 6823599),
                            ("Daily total", "25 to 30 g of oil a <em>day</em>.", "About five to six teaspoons.", 8818732)],
    "2026-11-18-reel-sources": [("How we work", "Where do our <em>numbers</em> come from?", "", 4492194),
                                ("Only", "ICMR-NIN. FSSAI. <em>MoHFW</em>.", "Indian government sources.", 7683820),
                                ("Always", "Every figure, <em>traceable</em>.", "No anonymous studies, no brand claims.", 4492194),
                                ("Check us", "Look up the <em>5 g</em> salt limit.", "Dietary Guidelines for Indians, 2024.", 13466248)],
    "2026-11-22-reel-breakfasts": [("Protein, counted", "Three Indian <em>breakfasts</em>.", "Values from ICMR-NIN's food tables.", 35763746),
                                   ("Breakfast 1", "2 rotis + dal: about <em>13 g</em>.", "60 g atta, 30 g raw dal.", 35763746),
                                   ("Breakfast 2", "1 egg + milk: about <em>14 g</em>.", "One 50 g egg, 200 ml milk.", 11369845),
                                   ("Breakfast 3", "Paneer bhurji + 2 rotis: about <em>15 g</em>.", "50 g paneer.", 6187598),
                                   ("Your number", "60 kg adult: about <em>50 g</em> a day.", "0.83 g per kg, ICMR-NIN.", 8818732)],
    "2026-11-25-reel-move": [("Move more", "30 minutes, five <em>days</em>.", "", 7880267),
                             ("Adults", "30 to 60 minutes of <em>moderate</em> activity.", "At least five days a week.", 7880267),
                             ("Children", "At least <em>60</em> minutes a day.", "Ages 5 to 19.", 8954918),
                             ("It counts", "A brisk <em>walk</em> counts.", "So do stairs, cycling and dancing.", 7880267)],
    "2026-11-29-reel-recap": [("November", "Six numbers to <em>save</em>.", "All from ICMR-NIN.", 7420512),
                              ("1", "0.83 g <em>protein</em> per kg.", "Healthy adults, per day.", 8818732),
                              ("2", "Not more than 5 g <em>salt</em>.", "About one teaspoon.", 13466248),
                              ("3", "25 to 30 g <em>oil</em>.", "Per day, in total.", 6823599),
                              ("4", "20 to 25 g <em>sugar</em>, at most.", "Tea, sweets and drinks.", 13466248),
                              ("5", "About 8 glasses of <em>water</em>.", "Including other drinks.", 7904429),
                              ("6", "30 to 60 minutes of <em>activity</em>.", "Five days a week.", 7880267)],
}


def reel_scene_specs(slug):
    out = []
    for i, (pill, head, body, pid) in enumerate(REELS[slug]):
        out.append(dict(layout="story", theme="photo", photo=px(pid), pill=pill, label="", headline=head, body=body, bottom="nnwa.in/protein", credit=CR))
    return out


def render(render_py, spec, out):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(spec, f)
    subprocess.run([sys.executable, render_py, f.name, out], check=True)
    os.remove(f.name)


if __name__ == "__main__":
    render_py, out_dir = sys.argv[1], sys.argv[2]
    only = sys.argv[3:]
    os.makedirs(out_dir, exist_ok=True)
    for slug, spec in C.items():
        if only and slug not in only:
            continue
        if spec.get("photo", "x") is None:
            spec = dict(spec, photo="file://" + EB + "f-dal.jpg")
        render(render_py, spec, out_dir if "slides" in spec else os.path.join(out_dir, slug + ".png"))
    for slug in REELS:
        if only and slug not in only:
            continue
        sd = os.path.join(out_dir, "_reel-scenes", slug)
        render(render_py, {"name": "scene", "slides": [dict(s, dots=None) for s in reel_scene_specs(slug)]}, sd)
        render(render_py, dict(END, photo=""), os.path.join(sd, "scene-end.png"))
