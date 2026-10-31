"""NNWA November 2026 campaign: single source of truth for every post.

Run `python3 calendar.py` to regenerate calendar.md and posts.json (used for Buffer scheduling).
Week 1 feed posts (1 to 8 Nov) belong to the lead-magnet thread (PR #4); their captions live in
/mnt/project-files/lead-magnet-funnel/7-day-plan-lead-magnet.md and are referenced here, not rewritten.
"""
import json
import os
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = "https://raw.githubusercontent.com/nnwaofficial/nnwa-social-assets/main/"

GUIDE = "https://nnwa.in/protein"
# Hrito, 31 Oct: nnwa.in/protein is not live yet, schedule without it. While False, guide CTAs carry no URL,
# Instagram keeps "link in bio" (update the bio when the page is live) and the 09:00 link-sticker Stories are held.
GUIDE_LIVE = False
# Greeting posts: no guide line on Facebook or LinkedIn while the guide is not live.
GREETING = {"chhath", "gurpurab"}
COURSES = "https://nnwa.in/courses"  # course page slugs to be confirmed once nnwa.in is reachable


def link(dest, source, medium, content):
    base, camp = (GUIDE, "protein-decoded") if dest == "guide" else (COURSES, "nov-2026-admissions")
    return f"{base}?utm_source={source}&utm_medium={medium}&utm_campaign={camp}&utm_content={content}"


DISCLAIMER = "General information for healthy adults, not medical advice."

# ---------------------------------------------------------------------------
# Feed posts. One per day (two on 14 Nov). Instagram and Facebook share the creative;
# LinkedIn gets its own caption on weekdays (and on 14 Nov, World Diabetes Day).
# fields: d=date, slug, fmt, layout/asset, hook, ig (caption body without CTA line),
#         cta (guide|course), course (name if course CTA), li (LinkedIn caption body or None),
#         src (source keys), alt, tags, owner, note
# ---------------------------------------------------------------------------
P = []


def post(**k):
    P.append(k)


# ---- Week 1: 1 to 8 Nov (feed from PR #4; additions marked new) ----
post(d="2026-11-01", slug="guide-launch", fmt="Carousel, 6 slides", existing=True, hook="A free guide: Protein, decoded",
     cta="guide", li=None, src=["RDA", "IFCT", "FSSAI-label"])
post(d="2026-11-02", slug="fibre", fmt="Static, vertical word", existing=True, hook="Where does your fibre come from?", cta="guide",
     li=("We've written a free 34-page guide for anyone who explains food to other people: Protein, decoded.\n\n"
         "It started with a question we hear every week from learners and their clients: how much protein do I need, and where does it come from on an Indian plate?\n\n"
         "Every number in it comes from Indian government sources: ICMR-NIN's Nutrient Requirements (2020), the Dietary Guidelines for Indians (2024), the Indian Food Composition Tables and FSSAI's labelling rules. There are no brand tie-ins and no supplement advice.\n\n"
         "It includes a 60-second self-check, an Indian food table, eight easy wins and a weekly tracker."),
     li_asset="2026-11-01-guide-launch-01.png", li_alt="Forest green slide reading 'A free guide: Protein, decoded' above the guide's cover.",
     src=["RDA", "DGI-plate", "IFCT", "FSSAI-label"])
post(d="2026-11-03", slug="protein", fmt="Carousel, 5 slides (LinkedIn: document)", existing=True, hook="How much protein you need, in one number", cta="guide", li="see funnel plan", src=["RDA"])
post(d="2026-11-04", slug="reel-500g", fmt="Reel 20 s (motion, new)", new_asset="2026-11-04-reel-500g.mp4", hook="What 500 g of vegetables and fruit looks like", cta="guide",
     li=("400 g of vegetables and 100 g of fruit a day. That's the reference ICMR-NIN's Dietary Guidelines for Indians (2024) use for a 2,000 kcal day, with vegetables, greens and fruit making up about half the plate.\n\n"
         "In counselling, the number lands better when people can see it. Two katoris of sabzi, a bowl of salad, a plate of greens and one fruit gets most people there.\n\n"
         "The other half of the plate is where protein comes in, and that's what our free guide covers."),
     li_asset="2026-11-04-reel-cover-500g.png", li_alt="Reel cover: a glass card over a vegetable photo reading '500 g of vegetables and fruit a day. Here is what that looks like.'",
     src=["DGI-plate"])
post(d="2026-11-05", slug="salt-check", fmt="Static, annotated", existing=True, hook="Not more than 5 g of salt a day", cta="guide", li="see funnel plan (three numbers card)", src=["DGI-salt"])
post(d="2026-11-06", slug="half-your-plate", fmt="Glass over photo", existing=True, hook="Half your plate: vegetables and fruit", cta="guide",
     li=("Dhanteras is a day for investing in what lasts.\n\n"
         "ICMR-NIN's Dietary Guidelines for Indians (2024) estimate that 56.4% of the total disease burden in India is due to unhealthy diets. The same report says healthy diets and physical activity can prevent up to 80% of type 2 diabetes.\n\n"
         "That's why we think nutrition literacy is worth investing in, for professionals and for families. Our free guide is a practical place to start."),
     li_asset="2026-11-06-li-disease-burden.png", li_alt="Paper card with a large '56.4%' and the line 'of India's total disease burden is due to unhealthy diets'. Source: ICMR-NIN, Dietary Guidelines for Indians, 2024.",
     src=["DGI-burden"])
post(d="2026-11-07", slug="eat-the-colours", fmt="4 tiles", existing=True, hook="Four colours for this week's shopping list", cta="guide", li=None, src=[])
post(d="2026-11-08", slug="diwali", fmt="Static greeting, glass over photo (new)", new_asset="2026-11-08-diwali.png", time_ig="10:00", time_fb="10:30",
     hook="Happy Diwali from all of us at NNWA",
     ig=("Happy Diwali from all of us at NNWA.\n\n"
         "Tonight, kitchens across India will be full: the kaju katli someone's mother still makes by hand, the chakli that never lasts till morning, the plate kept aside for the neighbours.\n\n"
         "Enjoy all of it. If you're frying at home, one tip from ICMR-NIN's Dietary Guidelines for Indians (2024): filter the oil once you've finished frying, use it for curries over the next day or two, and don't fry with it again.\n\n"
         "May your home be bright and your table be shared."),
     cta="guide", cta_line="For the days after the festival, our free guide is in the link in bio.",
     li=("Happy Diwali from everyone at NNWA (Nutrition & Wellness Academy).\n\n"
         "One practical note for the season, from ICMR-NIN's Dietary Guidelines for Indians (2024): oil that has been used for frying should be filtered, used for curries within a day or two, and not used for frying again.\n\n"
         "Wishing you and your families a bright and healthy festival."),
     alt="Warm photo of lit clay diyas. A frosted glass card reads 'Happy Diwali. May your home be bright and your table be shared.' NNWA wordmark at the top, nnwa.in at the bottom.",
     src=["DGI-reuse"], tags=["#HappyDiwali", "#NNWA", "#Diwali2026", "#IndianFood"])

# ---- Week 2: 9 to 15 Nov ----
post(d="2026-11-09", slug="learn-apply", fmt="Display statement (moved from 8 Nov)", existing=True, asset="2026-11-08-learn-apply.png", hook="Learn it. Apply it.", cta="course", course="All courses",
     ig=("Learn it. Apply it.\n\n"
         "Festive season is when everyone has nutrition advice: what to skip, what to 'detox' with, what someone's cousin swears by. Knowing what the evidence actually says, and how to explain it to someone you care about, is a skill.\n\n"
         "NNWA (Nutrition & Wellness Academy) teaches it 100% online, from a short introduction to full certifications and diplomas, with every lesson grounded in Indian guidelines."),
     li=("After a week of festive tables, the questions start: what should I cut, should I detox, is this supplement worth it?\n\n"
         "Answering those well takes more than a list of rules. It takes knowing the evidence, and the Indian guidelines behind it, well enough to explain it simply.\n\n"
         "That's what NNWA (Nutrition & Wellness Academy) teaches, 100% online, from short courses to full certifications and diplomas."),
     alt="Photo of green leaves with a large statement 'learn' and 'apply' joined by a brass line and spark. Subline: 100% online certifications in nutrition, wellness and fitness. Evidence first, explained simply.",
     src=[], tags=["#NNWA", "#NutritionCourse", "#OnlineLearning", "#LearnNutrition"])
post(d="2026-11-10", slug="bhai-dooj", fmt="Carousel, 5 slides", hook="This Bhai Dooj, gift a habit",
     ig=("This Bhai Dooj, gift a habit.\n\n"
         "The tilak, the sweets, the gift you've been hiding since Dhanteras. Add one more thing this year, something you can do together.\n\n"
         "Slide 2: a walk. ICMR-NIN suggests adults get 30 to 60 minutes of moderate activity a day, at least five days a week. A brisk evening walk with your sibling counts.\n"
         "Slide 3: a box of nuts and seeds alongside the mithai. The Dietary Guidelines for Indians list nuts and seeds as the swap for deep-fried snacks.\n"
         "Slide 4: one home-cooked meal, with half the plate vegetables and fruit.\n\n"
         "Habits last longer than sweets do."),
     cta="guide", cta_line="Our free guide has eight easy wins you can share with them. Link in bio.",
     li=None,
     alt="Slide 1: photo of a festive thali with a glass card 'This Bhai Dooj, gift a habit'. Slide 2: 'Walk together: 30 to 60 minutes, five days a week'. Slide 3: 'Add nuts and seeds to the mithai box'. Slide 4: 'Share one home-cooked meal: half the plate vegetables and fruit'. Slide 5: NNWA seal, 'Habits last longer than sweets. Free guide: nnwa.in/protein'.",
     src=["DGI-move", "DGI-swap", "DGI-plate"], tags=["#BhaiDooj", "#NNWA", "#HealthyHabits", "#IndianFamilies"])
post(d="2026-11-10", slug="li-sugar", li_only=True, fmt="LinkedIn image (new)", li_asset="2026-11-15-sugar.png", hook="20 to 25 g of sugar a day",
     li=("A useful number for the post-festival conversation: ICMR-NIN's Dietary Guidelines for Indians (2024) advise adults to avoid added sugar or keep it to 20 to 25 g a day.\n\n"
         "For many clients, that's a single piece of mithai plus sugar in two cups of tea. Showing them that is more useful than telling them to 'cut down'.\n\n"
         "Our free guide uses the same approach for protein: one clear number and what it looks like on an Indian plate."),
     li_alt="Paper poster with a spoon of sugar in a dashed ring. Headline: '20 to 25 g of sugar a day, at most.' Notes: 'ICMR-NIN: avoid added sugar or restrict it' and 'Count the sugar in tea, sweets and drinks'.",
     cta="guide", src=["DGI-sugar"])
post(d="2026-11-11", slug="education-day", fmt="Carousel, 6 slides (LinkedIn: document)", hook="National Education Day: where do you start with nutrition?",
     ig=("It's National Education Day, so here's an honest map of how people start learning nutrition with NNWA.\n\n"
         "If you're curious: Introduction to Nutrition is a short first step.\n"
         "If you want a full grounding: the Certification in Nutrition.\n"
         "If you want the most complete pathway: the Diploma in Nutrition, Dietetics & Public Health.\n"
         "If you already know your area: specialisations such as Diabetes Educator, Sports Nutrition, Child Nutrition and Food Science & FSSAI.\n\n"
         "Everything is 100% online. Fees, batch dates and eligibility are on each course page, and a counsellor can help you choose."),
     cta="course", course="All courses",
     li=("National Education Day is a good moment to talk about how people actually move into nutrition work in India.\n\n"
         "At NNWA (Nutrition & Wellness Academy), most learners start in one of four places: a short introduction, the Certification in Nutrition, the Diploma in Nutrition, Dietetics & Public Health, or a focused specialisation such as Diabetes Educator or Food Science & FSSAI.\n\n"
         "All of it is online, and all of it is built on Indian guidelines from ICMR-NIN and FSSAI. The document walks through the four routes."),
     alt="Slide 1: large vertical word 'learn' with 'National Education Day: where do you start with nutrition?'. Slides 2 to 5: one route per slide (Introduction to Nutrition; Certification in Nutrition; Diploma in Nutrition, Dietetics & Public Health; specialisations). Slide 6: NNWA seal, 'Explore the courses: nnwa.in/courses'.",
     src=[], tags=["#NationalEducationDay", "#NNWA", "#NutritionCourse", "#CareerInNutrition"], note="Course names from NNWA's course list; descriptions to be checked against nnwa.in course pages before approval.")
post(d="2026-11-12", slug="reel-oil", fmt="Reel 20 s (motion)", hook="The kadhai of oil from Diwali: fry again or not?",
     ig=("Is the kadhai of oil from Diwali frying still sitting on the stove?\n\n"
         "ICMR-NIN's Dietary Guidelines for Indians (2024) are clear on this. Heating oil again and again creates harmful compounds. Once you've fried in it, filter it, use it for curries within a day or two, and don't fry with it again.\n\n"
         "The guidelines also suggest 25 to 30 g of cooking oil a day in total, which is about five to six teaspoons."),
     cta="guide", cta_line="More practical kitchen numbers are in our free guide. Link in bio.",
     li=("One of the most common kitchen habits in India is also one of the easiest to fix: reusing frying oil.\n\n"
         "ICMR-NIN's Dietary Guidelines for Indians (2024) note that repeatedly heated oil forms harmful compounds. Their household advice: filter oil after frying, use it for curries within a day or two, and don't fry with it again. They suggest 25 to 30 g of cooking oil a day in total.\n\n"
         "It's a simple message that families can act on the same evening."),
     alt="Reel. Scene 1: 'The oil from Diwali frying. Fry again?'. Scene 2: 'Repeated heating forms harmful compounds'. Scene 3: 'Filter it. Use it for curries in a day or two'. Scene 4: 'Don't fry with it again'. Scene 5: '25 to 30 g of oil a day in total'. End card: 'Free guide: nnwa.in/protein'.",
     src=["DGI-reuse", "DGI-oil"], tags=["#CookingOil", "#NNWA", "#IndianKitchen", "#NutritionBasics"])
post(d="2026-11-13", slug="chhath", fmt="Static greeting, glass over photo", hook="Chhath Puja: thanking the sun",
     ig=("Today Chhath begins with Nahay Khay.\n\n"
         "Four days of devotion, discipline and gratitude to Surya and Chhathi Maiya. Families come together at the ghats, the thekua is made at home, and the baskets are filled with the season's harvest: sugarcane, bananas, coconut and fresh fruit.\n\n"
         "To everyone observing Chhath, from all of us at NNWA: may your prayers be answered and your families be well."),
     cta="guide", cta_line="Our free guide is in the link in bio whenever you need it.",
     li=("Chhath Puja begins today. To everyone observing it, from all of us at NNWA: may the coming four days bring you peace, strength and good health.\n\n"
         "If you or someone in your family is fasting and has diabetes, a heart condition or is pregnant, please speak to your doctor before the fast."),
     alt="Photo of the sun rising over a river. A glass card reads 'Chhath Puja. Gratitude to the sun, from all of us at NNWA.'",
     src=[], tags=["#ChhathPuja", "#NNWA", "#Chhath2026", "#Bihar"])
post(d="2026-11-14", slug="childrens-day", fmt="Carousel, 5 slides", time_ig="11:00", time_fb="12:00", hook="Children's Day: what the numbers ask of us",
     ig=("Happy Children's Day.\n\n"
         "Think of the youngest children in your family, the ones who refuse dal and steal the jalebi. Now look at slide 2.\n\n"
         "According to national survey data reported in ICMR-NIN's Dietary Guidelines for Indians (2024), 40.6% of children aged 1 to 4 have anaemia, as do 23.5% of those aged 5 to 9 and 28.4% of those aged 10 to 19. About 1 in 10 children aged 5 to 19 already shows pre-diabetes.\n\n"
         "What helps, per the same guidelines: varied home-cooked food, homemade semi-solid foods from six months, and at least 60 minutes of active play a day.\n\n"
         "If you work with children or parents, our Child & Adolescent Nutrition course covers this properly."),
     cta="course", course="Child & Adolescent Nutrition",
     li=None,
     alt="Slide 1: paper slide with a large '40.6%' and 'of children aged 1 to 4 in India have anaemia'. Slide 2: anaemia by age (40.6%, 23.5%, 28.4%). Slide 3: 'About 1 in 10 children aged 5 to 19 shows pre-diabetes'. Slide 4: 'What helps: varied home food, semi-solid foods from six months, 60 minutes of play a day'. Slide 5: NNWA seal, 'Child & Adolescent Nutrition, 100% online. nnwa.in/courses'.",
     src=["DGI-T1", "DGI-G", "DGI-move"], tags=["#ChildrensDay", "#NNWA", "#ChildNutrition", "#Anaemia"])
post(d="2026-11-14", slug="diabetes-day", fmt="Static, stat", time_ig="19:00", time_fb="19:30", hook="World Diabetes Day: 15.6% of men, 13.5% of women",
     ig=("World Diabetes Day.\n\n"
         "NFHS-5 (2021) data, reported in ICMR-NIN's Dietary Guidelines for Indians (2024), found diabetes in 15.6% of men and 13.5% of women aged 18 to 69. In 2016 the figures were 10.5% and 9.7%.\n\n"
         "The same guidelines say healthy diets and physical activity can prevent up to 80% of type 2 diabetes. That's why counselling and education matter so much.\n\n"
         "If you want to help people manage diabetes day to day, NNWA's Diabetes Educator course is 100% online.\n\n"
         "If you have diabetes, follow your doctor's advice; this post is general information."),
     cta="course", course="Diabetes Educator",
     li=("World Diabetes Day. Two numbers from NFHS-5 (2021), reported in ICMR-NIN's Dietary Guidelines for Indians (2024): diabetes in 15.6% of men and 13.5% of women aged 18 to 69, up from 10.5% and 9.7% in 2016.\n\n"
         "The same guidelines state that healthy diets and physical activity can prevent up to 80% of type 2 diabetes. Prevention at that scale depends on people who can explain food clearly and consistently.\n\n"
         "NNWA's Diabetes Educator course trains exactly that, 100% online."),
     alt="Forest green stat card. Large '15.6%' with the label 'of Indian men aged 18 to 69 have diabetes', then '13.5% of women'. Line: 'Healthy diets and activity can prevent up to 80% of type 2 diabetes. ICMR-NIN'.",
     src=["DGI-T2", "DGI-burden"], tags=["#WorldDiabetesDay", "#NNWA", "#DiabetesEducator", "#DiabetesAwareness"], li_day=True)
post(d="2026-11-15", slug="sugar", fmt="Static, annotated", time_ig="11:00", time_fb="12:00", hook="20 to 25 g of sugar a day, at most",
     ig=("Still finishing the Diwali mithai? Here's the number to keep in mind.\n\n"
         "ICMR-NIN's Dietary Guidelines for Indians (2024) advise adults to avoid added sugar, or keep it to 20 to 25 g a day. That covers the sugar in your tea, sweets and drinks combined.\n\n"
         "No guilt about the festival. Just a number to come back to this week."),
     cta="guide", cta_line="Our free guide has eight easy wins for the week. Link in bio.",
     li=None,
     alt="Paper poster with a spoon of sugar in a dashed ring. Headline: '20 to 25 g of sugar a day, at most.' Notes: 'ICMR-NIN: avoid added sugar or restrict it' and 'Count the sugar in tea, sweets and drinks'. Footer: Free guide: nnwa.in/protein.",
     src=["DGI-sugar"], tags=["#SugarCheck", "#NNWA", "#NutritionBasics", "#AfterDiwali"])

# ---- Week 3: 16 to 22 Nov ----
post(d="2026-11-16", slug="right-for-you", fmt="Carousel, 6 slides (LinkedIn: document)", hook="Is a nutrition course right for you? Five honest questions",
     ig=("Thinking about studying nutrition? Answer these five questions honestly first.\n\n"
         "1. Do you enjoy explaining things to people?\n"
         "2. Are you comfortable checking a claim against a source before you share it?\n"
         "3. Can you set aside a few hours a week for steady study?\n"
         "4. Do you know which group you want to help: families, athletes, people with diabetes, children?\n"
         "5. Are you clear that a course gives you knowledge and a certificate, and that work comes from what you do with it?\n\n"
         "If most answers are yes, have a look at NNWA's courses. They're 100% online, and a counsellor can help you pick one."),
     cta="course", course="All courses",
     li=("Before anyone enrols with us, we'd rather they asked themselves five honest questions. Do they enjoy explaining things? Will they check a claim against its source? Can they give a few hours a week? Do they know who they want to help? And do they understand that a certificate is a start, not a guarantee of work?\n\n"
         "We think clear expectations make better nutrition professionals. The document has all five questions."),
     alt="Slide 1: 'Is a nutrition course right for you? Five honest questions.' Slides 2 to 6: one question per slide, last slide adds 'Explore the courses: nnwa.in/courses'.",
     src=[], tags=["#NutritionCareer", "#NNWA", "#NutritionCourse", "#OnlineLearning"])
post(d="2026-11-17", slug="first-six-months", fmt="Glass over photo", hook="The first six months: breast milk only",
     ig=("It's National Newborn Week (15 to 21 November).\n\n"
         "ICMR-NIN's Dietary Guidelines for Indians (2024) recommend exclusive breastfeeding for the first six months, with breastfeeding continuing to two years and beyond. Soon after six months, babies should start homemade semi-solid foods alongside it.\n\n"
         "Every new mother deserves support with this, from family, from health workers and from people trained to give good advice.\n\n"
         "NNWA's Post-Pregnancy & Lactation Nutrition course is for anyone who wants to give that support properly. 100% online.\n\n"
         "For medical concerns about your baby, please speak to your paediatrician."),
     cta="course", course="Post-Pregnancy & Lactation Nutrition",
     li=("National Newborn Week runs from 15 to 21 November. The Dietary Guidelines for Indians (ICMR-NIN, 2024) keep the core message simple: exclusive breastfeeding for six months, homemade semi-solid foods soon after six months, and breastfeeding continued to two years and beyond.\n\n"
         "Mothers are more likely to follow the guidance when the people around them understand it too. NNWA's Post-Pregnancy & Lactation Nutrition course is built for those people."),
     alt="Soft photo of a baby's feet held in a mother's hands. Glass card: 'The first six months: breast milk only. Then homemade semi-solid foods, and breastfeeding continued to two years and beyond.' Source line: ICMR-NIN.",
     src=["DGI-G"], tags=["#NewbornWeek", "#NNWA", "#Breastfeeding", "#MotherAndChild"])
post(d="2026-11-18", slug="reel-sources", fmt="Reel 20 s (motion)", hook="Why every number we post comes from ICMR-NIN",
     ig=("Why does every NNWA post cite ICMR-NIN, FSSAI or the Ministry of Health?\n\n"
         "Because nutrition advice online is full of numbers nobody can trace. We only use figures from Indian government sources, and we tell you where to find them, so you can check us.\n\n"
         "Try it: the Dietary Guidelines for Indians (2024) are a free PDF on ICMR-NIN's website. Look up the 5 g salt limit yourself.\n\n"
         "Our free guide follows the same rule, with a full source list at the back."),
     cta="guide", cta_line="Get it from the link in bio.",
     li=("A note on how we write. Every number NNWA publishes, on social media, in our free guide and in our courses, comes from an Indian government source: ICMR-NIN, ICMR, FSSAI or the Ministry of Health and Family Welfare.\n\n"
         "It means saying less than we could, and leaving out claims we can't trace. We think that's what trust in health education requires."),
     alt="Reel. Scene 1: 'Where do our numbers come from?'. Scene 2: 'ICMR-NIN. FSSAI. Ministry of Health.' Scene 3: 'Every figure, traceable.' Scene 4: 'Check us: Dietary Guidelines for Indians, 2024'. End card: 'Free guide: nnwa.in/protein'.",
     src=["DGI-salt"], tags=["#EvidenceBased", "#NNWA", "#ICMR", "#NutritionFacts"])
post(d="2026-11-19", slug="mens-day", fmt="Static, stat", hook="International Men's Day: 1 in 4 men",
     ig=("International Men's Day. A number worth a conversation at home.\n\n"
         "NFHS-5 (2021), as reported in ICMR-NIN's Dietary Guidelines for Indians (2024), found hypertension in 24.0% of men aged 18 to 69, up from 20.2% in 2016.\n\n"
         "Two things from the same guidelines that help: not more than 5 g of salt a day, and 30 to 60 minutes of moderate activity on at least five days a week.\n\n"
         "If someone you love hasn't had his blood pressure checked in a while, today's a good day to suggest it."),
     cta="guide", cta_line="Our free guide is in the link in bio.",
     li=("International Men's Day. NFHS-5 (2021) data, reported in ICMR-NIN's Dietary Guidelines for Indians (2024), found hypertension in 24.0% of Indian men aged 18 to 69, up from 20.2% in 2016.\n\n"
         "Most of the levers are everyday ones: salt under 5 g a day and 30 to 60 minutes of moderate activity on most days. Workplace wellness programmes can make both easier."),
     alt="Paper stat card. Large '24.0%' with 'of Indian men aged 18 to 69 have hypertension (NFHS-5, 2021), up from 20.2% in 2016'. Two lines below: 'Salt: not more than 5 g a day' and 'Move: 30 to 60 minutes, five days a week'.",
     src=["DGI-T2", "DGI-salt", "DGI-move"], tags=["#InternationalMensDay", "#NNWA", "#BloodPressure", "#MensHealth"])
post(d="2026-11-20", slug="millets", fmt="Carousel, 5 slides", hook="A fifth to a third of your cereals: millets",
     ig=("How much of your roti and rice should be millets? ICMR-NIN has a number.\n\n"
         "The Dietary Guidelines for Indians (2024) suggest that 20% to 30% of the cereals adults eat (by raw weight) come from millets.\n\n"
         "In practice, that could be a bajra or jowar roti at one meal, ragi in your dosa batter, or a millet khichdi once or twice a week.\n\n"
         "Pair millets with dal and you get a better protein mix too. That's covered in chapter 4 of our free guide."),
     cta="guide", cta_line="Link in bio.",
     li=("A practical target from ICMR-NIN's Dietary Guidelines for Indians (2024): 20% to 30% of adults' cereals, by raw weight, should come from millets.\n\n"
         "It's easier to act on than 'eat more millets'. Swapping one roti or one rice meal a day gets most households close."),
     alt="Slide 1: tiles of bajra, jowar, ragi and foxtail millet, headline '20% to 30% of your cereals: millets'. Slides 2 to 4: ideas (a bajra or jowar roti, ragi in dosa batter, millet khichdi). Slide 5: NNWA seal and 'Free guide: nnwa.in/protein'.",
     src=["DGI-millet"], tags=["#Millets", "#NNWA", "#ShreeAnna", "#IndianNutrition"])
post(d="2026-11-21", slug="supplements-myth", fmt="Glass over photo", time_ig="11:00", time_fb="12:00", hook="Protein powder to build muscle? ICMR-NIN says no",
     ig=("\"Without whey you can't build muscle.\" You've heard it at the gym.\n\n"
         "ICMR-NIN's Dietary Guidelines for Indians (2024) say otherwise. Guideline 8: get good-quality protein from a combination of foods, and avoid protein supplements to build muscle mass.\n\n"
         "Dal with rice or roti, milk and curd, eggs, paneer, fish and chicken can cover a healthy adult's needs (0.83 g per kg of body weight a day).\n\n"
         "If you have a medical condition, follow your doctor's advice."),
     cta="guide", cta_line="Our free guide shows how to reach your number with food. Link in bio.",
     li=None,
     alt="Photo of a bowl of dal and rice. Glass card: 'Protein powder to build muscle? ICMR-NIN advises against it. Combine foods instead.'",
     src=["DGI-G", "RDA"], tags=["#ProteinMyths", "#NNWA", "#ProteinDecoded", "#GymIndia"])
post(d="2026-11-22", slug="reel-breakfasts", fmt="Reel 25 s (motion)", time_ig="11:00", time_fb="12:00", hook="Three Indian breakfasts, protein counted",
     ig=("Three everyday Indian breakfasts, with the protein counted from ICMR-NIN's Indian Food Composition Tables.\n\n"
         "2 rotis (60 g atta) and a bowl of dal (30 g raw): about 13 g.\n"
         "1 egg and a glass of milk (200 ml): about 14 g.\n"
         "50 g paneer bhurji with 2 rotis: about 15 g.\n\n"
         "For a 60 kg adult, the daily need is about 50 g (0.83 g per kg), so breakfast can carry a good share."),
     cta="guide", cta_line="Our free guide has the full food table. Link in bio.",
     li=None,
     alt="Reel. Scene 1: 'Three Indian breakfasts, protein counted'. Scene 2: '2 rotis plus dal: about 13 g'. Scene 3: '1 egg plus a glass of milk: about 14 g'. Scene 4: 'Paneer bhurji plus 2 rotis: about 15 g'. End card: 'Free guide: nnwa.in/protein'.",
     src=["IFCT", "RDA"], tags=["#ProteinDecoded", "#NNWA", "#IndianBreakfast", "#ProteinBasics"])

# ---- Week 4: 23 to 30 Nov ----
post(d="2026-11-23", slug="water", fmt="Static, stat", hook="About eight glasses a day",
     ig=("Winter makes it easy to forget water.\n\n"
         "ICMR-NIN's Dietary Guidelines for Indians (2024) say a normal healthy person needs about eight glasses, roughly two litres, of water a day, including other drinks.\n\n"
         "Keep a bottle where you can see it, and have a glass with every meal."),
     cta="guide", cta_line="More everyday numbers in our free guide. Link in bio.",
     li=("A small reminder for winter: ICMR-NIN's Dietary Guidelines for Indians (2024) put a healthy adult's need at about eight glasses (around two litres) of water a day, including other beverages.\n\n"
         "In offices with heating and long meetings, it's often the first habit to slip."),
     alt="Forest green stat card with a glass of water in a circle. Large '8' with 'glasses of water a day, about 2 litres, including other drinks'. Source ICMR-NIN.",
     src=["DGI-water"], tags=["#DrinkWater", "#NNWA", "#WinterWellness", "#NutritionBasics"])
post(d="2026-11-24", slug="gurpurab", fmt="Static greeting, glass over photo", time_ig="09:00", time_fb="09:30", hook="Guru Nanak Jayanti: everyone eats together",
     ig=("On Guru Nanak Jayanti, we remember a simple idea from the langar: everyone sits in the same row and eats the same food, whoever they are.\n\n"
         "Service, sharing and gratitude. Wishing you and your family a blessed Gurpurab."),
     cta="guide", cta_line="", soft=True,
     li=("Wishing everyone a blessed Guru Nanak Jayanti.\n\n"
         "The langar's idea of serving everyone the same meal, side by side, is one that anyone working in food and health can learn from."),
     alt="Warm photo of a langar meal served in steel plates. Glass card: 'Guru Nanak Jayanti. Everyone sits together. Everyone is fed.'",
     src=[], tags=["#GuruNanakJayanti", "#Gurpurab", "#NNWA", "#Langar"], note="Greeting post: no CTA in the caption out of respect; the first comment carries the guide link.")
post(d="2026-11-25", slug="reel-move", fmt="Reel 20 s (motion)", hook="30 minutes, five days a week",
     ig=("How much should you move? ICMR-NIN gives a number.\n\n"
         "The Dietary Guidelines for Indians (2024) recommend that adults do 30 to 60 minutes of moderate activity a day, on at least five days a week. For children and teenagers, it's at least 60 minutes a day.\n\n"
         "A brisk walk counts. So do climbing the stairs, cycling, dancing at a wedding and playing with the kids."),
     cta="guide", cta_line="Pair it with the right food: our free guide is in the link in bio.",
     li=("ICMR-NIN's Dietary Guidelines for Indians (2024): 30 to 60 minutes of moderate activity a day, on at least five days a week, for adults. At least 60 minutes a day for children aged 5 to 19.\n\n"
         "It's one of the few health targets that needs no equipment. A brisk walk counts."),
     alt="Reel. Scene 1: '30 minutes, five days a week'. Scene 2: 'Adults: 30 to 60 minutes of moderate activity a day'. Scene 3: 'Children: at least 60 minutes'. Scene 4: 'A brisk walk counts'. End card: 'Free guide: nnwa.in/protein'.",
     src=["DGI-move"], tags=["#MoveMore", "#NNWA", "#FitIndia", "#HealthyHabits"])
post(d="2026-11-26", slug="milk-day", fmt="Static, annotated", hook="National Milk Day: 300 ml of milk or curd",
     ig=("It's National Milk Day, marked on Dr Verghese Kurien's birth anniversary.\n\n"
         "ICMR-NIN's My Plate for the Day includes 300 ml of milk or curd, which gives about 10 g of protein. That's a glass of milk and a katori of dahi.\n\n"
         "If you're vegetarian, milk and curd are among the easiest ways to improve the quality of your protein."),
     cta="guide", cta_line="Our free guide shows the rest of the plate. Link in bio.",
     li=("National Milk Day, on Dr Verghese Kurien's birth anniversary. ICMR-NIN's My Plate for the Day includes 300 ml of milk or curd, about 10 g of protein, in a 2,000 kcal Indian diet.\n\n"
         "For vegetarian clients it's one of the simplest protein upgrades to suggest."),
     alt="Paper poster with a glass of milk and a bowl of curd in a dashed ring. Headline: '300 ml of milk or curd a day'. Notes: 'About 10 g of protein' and 'ICMR-NIN My Plate for the Day'.",
     src=["DGI-plate"], tags=["#NationalMilkDay", "#NNWA", "#ProteinDecoded", "#VegetarianProtein"])
post(d="2026-11-27", slug="read-the-label", fmt="Carousel, 5 slides (LinkedIn: document)", hook="Read any Indian food label in four steps",
     ig=("Most packaged food in India carries four things FSSAI requires. Here's what to look at, in order.\n\n"
         "1. The veg or non-veg symbol.\n"
         "2. The FSSAI logo and licence number.\n"
         "3. The ingredient list, in order of weight.\n"
         "4. The nutrition information, per 100 g or per pack.\n\n"
         "If you'd like to understand food standards in depth, NNWA's Food Science & FSSAI course is 100% online."),
     cta="course", course="Food Science & FSSAI",
     li=("FSSAI's Labelling and Display Regulations (2020) require four things on most packaged foods: the veg or non-veg symbol, the FSSAI logo and licence number, an ingredient list in descending order of weight, and nutrition information.\n\n"
         "Teaching clients to read those four is one of the most useful half-hours in nutrition counselling. NNWA's Food Science & FSSAI course goes much further."),
     alt="Slide 1: 'Read any Indian food label in four steps'. Slides 2 to 4: a label with the veg symbol, FSSAI logo and licence number, ingredient list and nutrition panel circled. Slide 5: 'Food Science & FSSAI, 100% online. nnwa.in/courses'.",
     src=["FSSAI-label"], tags=["#FoodLabels", "#NNWA", "#FSSAI", "#FoodScience"])
post(d="2026-11-28", slug="swaps", fmt="4 tiles", time_ig="11:00", time_fb="12:00", hook="Swap, don't stop",
     ig=("Four swaps straight from ICMR-NIN's Dietary Guidelines for Indians (2024).\n\n"
         "Deep-fried snacks: try nuts and seeds.\n"
         "Fruit juice: eat the whole fruit.\n"
         "Refined, high-sugar sweets: choose traditional sweets made with whole grains, millets, nuts and oilseeds.\n"
         "Sugary drinks: buttermilk, lemon water or tender coconut water.\n\n"
         "No food is banned. Small swaps add up."),
     cta="guide", cta_line="Eight more easy wins are in our free guide. Link in bio.",
     li=None,
     alt="Four photo tiles: nuts and seeds, a whole orange, a til-gur ladoo, a glass of buttermilk. Headline: 'Swap, don't stop.' Each tile names the food it replaces.",
     src=["DGI-swap"], tags=["#HealthySwaps", "#NNWA", "#IndianFood", "#EatRight"])
post(d="2026-11-29", slug="reel-recap", fmt="Reel 25 s (motion)", time_ig="11:00", time_fb="12:00", hook="November in six numbers",
     ig=("Six numbers from this month, all from ICMR-NIN.\n\n"
         "0.83 g of protein per kg of body weight a day.\n"
         "Not more than 5 g of salt a day.\n"
         "25 to 30 g of cooking oil a day.\n"
         "20 to 25 g of sugar, at most.\n"
         "About 8 glasses of water.\n"
         "30 to 60 minutes of activity, five days a week.\n\n"
         "Save this one."),
     cta="guide", cta_line="Protein, the first number, gets a whole free guide. Link in bio.",
     li=None,
     alt="Reel. One number per scene: '0.83 g protein per kg', '5 g salt', '25 to 30 g oil', '20 to 25 g sugar', '8 glasses of water', '30 to 60 minutes of activity'. End card: 'Free guide: nnwa.in/protein'.",
     src=["RDA", "DGI-salt", "DGI-oil", "DGI-sugar", "DGI-water", "DGI-move"], tags=["#ProteinDecoded", "#NNWA", "#NutritionBasics", "#SaveThis"])
post(d="2026-11-30", slug="make-it-your-work", fmt="Display statement", hook="Make it your work",
     ig=("All month we've shared numbers from ICMR-NIN and FSSAI. Some of you have been forwarding them to family groups.\n\n"
         "If explaining food clearly is something you'd like to do properly, for your family, your clients or your career, that's what NNWA teaches. 100% online, with every lesson built on Indian guidelines.\n\n"
         "See the courses and talk to a counsellor."),
     cta="course", course="All courses",
     li=("This month we've published one evidence-based number a day, every one traceable to ICMR-NIN or FSSAI.\n\n"
         "If you or your team want to work with that kind of evidence every day, NNWA's courses cover nutrition, diabetes education, sports, child nutrition, food science and more. All online."),
     alt="Photo of fresh produce with a large statement 'learn' and 'teach' joined by a brass line. Subline: 'Make it your work. 100% online courses in nutrition and wellness.' nnwa.in/courses.",
     src=[], tags=["#NNWA", "#NutritionCourse", "#CareerInNutrition", "#OnlineLearning"])



# ---- Week 1 captions, copied from the lead-magnet plan (7-day-plan-lead-magnet.md, 31 Oct 2026) ----
W1_CAPTIONS = {
 "guide-launch": dict(ig=("How much protein do you need, and where does it come from on an Indian plate?\n\n"
     "We wrote a free guide to answer that properly. Protein, decoded has 34 pages and seven short chapters. It includes a 60-second check, your number from ICMR-NIN's 0.83 g per kg, a table of everyday Indian foods, eight easy wins, a weekly tracker and a fridge sheet you can print.\n\n"
     "Every fact in it comes from Indian government sources: ICMR-NIN and FSSAI. It's general information for healthy adults, not medical advice."),
     cta_line="Get it free from the link in bio.", tags=["#ProteinDecoded", "#NNWA", "#IndianNutrition", "#ProteinBasics"],
     alt="Slide 1, forest green slide reading 'A free guide: Protein, decoded' above the guide's cover. Slide 2, 'Seven short chapters' above the contents page. Slide 3, 'Start with a 60-second check'. Slide 4, 'Everyday Indian foods, real numbers'. Slide 5, 'A fridge sheet you can print'. Slide 6, NNWA seal: 'Get it free from the link in bio', nnwa.in/protein."),
 "fibre": dict(ig=("Most of the fibre on an Indian plate comes from four everyday places.\n\n"
     "Whole grains like atta, brown rice, millets and oats. Pulses: dal, rajma, chana, moong. Vegetables, especially with the skin on where it is edible. Whole fruit rather than juice.\n\n"
     "Dal, rajma and chana bring fibre and protein together. Chapter 03 of our free guide, Protein, decoded, shows how much protein each one gives."),
     cta_line="Get it from the link in bio.", tags=["#ProteinDecoded", "#NNWA", "#NutritionBasics", "#IndianNutrition"],
     alt="Forest green poster with the word 'fibre' set vertically beside a bowl of rajma in a dashed ring. Note: 'Four everyday sources: whole grains, pulses, vegetables and fruit.' Footer: Free guide: nnwa.in/protein."),
 "protein": dict(ig=("How much protein do you actually need in a day? One number does most of the work.\n\n"
     "Healthy adults need about 0.83 g of protein per kg of body weight a day. At 60 kg that is about 50 g. Slides 2 to 4 show how to work out yours, how to spread it across meals and which everyday foods to mix.\n\n"
     "Needs are different in pregnancy, older age, kidney disease and heavy training, so check with a qualified expert if any of those apply to you.\n\n"
     "The full guide has the calculator, a table of everyday Indian foods and a weekly tracker."),
     cta_line="It's free from the link in bio.", tags=["#ProteinDecoded", "#NNWA", "#ProteinBasics", "#IndianNutrition"],
     li=("Clients ask \"how much protein?\" more than almost anything else. ICMR-NIN's 2020 Nutrient Requirements for Indians give a clean starting point for healthy adults: 0.83 g per kg of body weight per day.\n\n"
         "The five slides cover the calculation, meal distribution and mixed sources. We've put the full reference into a free 34-page guide: requirements by life stage, an Indian food table and FSSAI label rules, all from government sources."),
     alt="Five-slide carousel. Slide 1: '0.83 g/kg of protein per kg of body weight a day, for healthy adults'. Slides 2 to 4: working out your number, spreading it across meals, mixing foods. Slide 5: NNWA seal, 'Get the full guide, free. nnwa.in/protein'."),
 "salt-check": dict(ig=("Not more than 5 g of salt a day. That's one teaspoon, and it includes the salt already in your food.\n\n"
     "Pickles, papads, namkeen and sauces add up quickly. Taste before you add salt at the table, and check the sodium line on labels.\n\n"
     "Labels hide more than salt. Our free guide, Protein, decoded, shows how to read an Indian food label, including protein claims."),
     cta_line="Link in bio.", tags=["#ProteinDecoded", "#NNWA", "#SaltCheck", "#NutritionBasics"],
     li=("Three reference numbers that come up in almost every nutrition conversation, all from ICMR-NIN: protein 0.83 g/kg/day for healthy adults (2020), salt not more than 5 g a day, and 400 g of vegetables plus 100 g of fruit a day on a 2,000 kcal plate (Dietary Guidelines for Indians, 2024).\n\n"
         "They're starting points, not prescriptions. The protein one is unpacked in our free guide."),
     li_asset="2026-11-05-linkedin-numbers.png", li_alt="Paper card titled 'Three numbers worth knowing': 0.83 g/kg protein, 5 g salt, 400 g vegetables plus 100 g fruit, each under a brass rule.",
     alt="Off-white poster. Headline 'Not more than 5 g of salt a day. That is one teaspoon.' Wooden spoon of salt in a circle with a dashed ring. Notes: 'ICMR-NIN advice: not more than 5 g of salt a day, from all foods' and 'Hidden salt: pickles, papads, namkeen and sauces count too'. Footer: Free guide: nnwa.in/protein."),
 "half-your-plate": dict(ig=("Half your plate: vegetables and fruit.\n\n"
     "ICMR-NIN's Dietary Guidelines for Indians (2024) have vegetables, fruits, greens, tubers and roots forming about half the plate, with the rest shared between cereals, pulses or other protein, and dairy.\n\n"
     "What goes on the other half? Our free guide builds four example Indian days."),
     cta_line="Get it from the link in bio.", tags=["#ProteinDecoded", "#NNWA", "#MyPlate", "#IndianNutrition"], src=["DGI-plate"],
     alt="Photo of a vegetable plate with a frosted glass card: 'Half your plate: vegetables and fruit.' Body: ICMR-NIN's Dietary Guidelines for Indians (2024) suggest filling about half the plate with vegetables, greens and fruit. Footer: Free guide: nnwa.in/protein."),
 "eat-the-colours": dict(ig=("Four colours for this week's shopping list.\n\n"
     "Greens like spinach, methi and lettuce. Reds like tomato, capsicum and beetroot. Yellow and orange like lemon, pumpkin and papaya. Purples like brinjal, jamun and red cabbage. Variety matters more than any single food.\n\n"
     "Add one protein to that list. Our free guide has a one-page fridge sheet to help."),
     cta_line="Link in bio.", tags=["#ProteinDecoded", "#NNWA", "#EatTheRainbow", "#IndianFood"],
     alt="Off-white poster 'Four colours for this week's shopping list' with four photo tiles: greens, reds, yellow and orange, purples, each naming everyday Indian vegetables and fruit. Footer: Free guide: nnwa.in/protein."),
 "learn-apply": dict(),
 "reel-500g": dict(ig=("What does 500 g of vegetables and fruit a day look like?\n\n"
     "ICMR-NIN's Dietary Guidelines for Indians (2024) use 400 g of vegetables and 100 g of fruit a day for a 2,000 kcal plate. Vegetables are half the plate. The other half needs protein, and our free guide shows how to build it."),
     cta_line="Link in bio.", tags=["#ProteinDecoded", "#NNWA", "#EatMoreVeg", "#IndianNutrition"],
     alt="Reel. Scene 1: 'What does 500 g look like?'. Scene 2: '400 g of vegetables, and 100 g of fruit, for a 2,000 kcal day'. Scene 3: 'Two katoris of sabzi, plus a bowl of salad and a plate of greens'. Scene 4: 'One whole fruit'. Scene 5: 'The other half needs protein'. End card: 'Get the free guide. nnwa.in/protein'."),
}
for _p in P:
    _w = W1_CAPTIONS.get(_p["slug"])
    if _w:
        for _k, _v in _w.items():
            if _k == "li" and _p.get("li") and not str(_p["li"]).startswith("see"):
                continue
            if _k == "src":
                _p["src"] = sorted(set(_p.get("src", []) + _v))
                continue
            _p.setdefault(_k, _v) if _k != "li" else _p.__setitem__("li", _v)

# ---------------------------------------------------------------------------
# Timings (IST). General benchmarks for Indian audiences; refine after week 2 with Buffer analytics.
# ---------------------------------------------------------------------------
def wd(d):
    return date.fromisoformat(d).weekday()  # Mon=0


def ig_time(p):
    if p.get("time_ig"):
        return p["time_ig"]
    if "Reel" in p["fmt"]:
        return "20:00" if wd(p["d"]) < 5 else "11:00"
    return "19:00" if wd(p["d"]) < 5 else "11:00"


def fb_time(p):
    return p.get("time_fb") or ("13:00" if wd(p["d"]) < 5 else "12:00")


def li_time(d):
    return "09:30" if wd(d) in (1, 2, 3) else "10:00"


FEST_STORY = {"2026-11-06": "dhanteras", "2026-11-07": "choti-diwali-oil", "2026-11-08": "diwali", "2026-11-09": "govardhan",
              "2026-11-10": "bhai-dooj", "2026-11-15": "chhath-arghya", "2026-11-24": "gurpurab"}

STORY_LINK_FRAMES = ["guide-story-link-1-p03.png", "guide-story-link-2-p21.png", "guide-story-link-3-p29.png", "guide-story-link-4-p31.png"]


def build():
    rows, items = [], []
    start = date(2026, 11, 1)
    for i in range(30):
        d = (start + timedelta(days=i)).isoformat()
        day = [p for p in P if p["d"] == d]
        # morning story: link frame (guide), rotated; course frame on course days
        course_day = any(p.get("cta") == "course" for p in day if not p.get("li_only"))
        if GUIDE_LIVE:
          frame = "stories/course-story-link.jpg" if course_day else STORY_LINK_FRAMES[i % 4]
          dest = "course" if course_day else "guide"
          items.append(dict(date=d, time="09:00", channel="instagram", type="story", asset=frame,
                          link=link(dest, "instagram", "story", f"{d}-am"), note="Link sticker"))
        for p in day:
            if p.get("li_only"):
                items.append(dict(date=d, time=li_time(d), channel="linkedin", type="post", slug=p["slug"], asset=p["li_asset"]))
                continue
            items.append(dict(date=d, time=ig_time(p), channel="instagram", type="reel" if "Reel" in p["fmt"] else "post", slug=p["slug"]))
            items.append(dict(date=d, time=fb_time(p), channel="facebook", type="reel" if "Reel" in p["fmt"] else "post", slug=p["slug"]))
            if p.get("li") and (wd(d) < 5 or p.get("li_day")):
                items.append(dict(date=d, time=li_time(d), channel="linkedin", type="post", slug=p["slug"]))
        if d in FEST_STORY:
            for ch in ("instagram", "facebook"):
                items.append(dict(date=d, time="07:30", channel=ch, type="story", asset=f"stories/{d}-story-{FEST_STORY[d]}.jpg", note="Festival greeting Story"))
        main = [p for p in day if not p.get("li_only")]
        last = main[-1]
        items.append(dict(date=d, time="21:30", channel="instagram", type="story", asset=f"stories/{d}-{last['slug']}-story.jpg", note="Feed post as a Story"))
        items.append(dict(date=d, time="21:30", channel="facebook", type="story", asset=f"stories/{d}-{last['slug']}-story.jpg", note="Feed post as a Story"))
    return items


def md():
    items = build()
    out = ["# NNWA November 2026 calendar (1 to 30 Nov)", "",
           "Playbooks used: social-calendar-builder, social-creative-builder, ig-caption-writer, ig-hashtag-strategist, ig-humanizer (AI-tell pass). Design system v2. Sources: [sources.md](sources.md) (government only).", "",
           "Status: draft for Hrito's approval, week by week. Nothing is scheduled until a week is approved. All times IST.", "",
           f"Totals: {len(items)} Buffer posts ({sum(1 for x in items if x['channel']=='instagram')} Instagram, {sum(1 for x in items if x['channel']=='facebook')} Facebook, {sum(1 for x in items if x['channel']=='linkedin')} LinkedIn), about {len(items)/30:.1f} a day.", "",
           "## Daily rhythm", "",
           "| Slot (IST) | Instagram | Facebook | LinkedIn |", "|---|---|---|---|",
           "| 09:00 | Story: link frame to the free guide (or a course on course days) | | |",
           "| 09:30 to 10:00 | | | Weekday post (Tue to Thu 09:30, Mon/Fri 10:00) |",
           "| 13:00 (weekends 12:00) | | Feed post, Facebook caption | |",
           "| 19:00 weekdays, 11:00 weekends; Reels 20:00 | Feed post or Reel | | |",
           "| 21:30 | Story: today's feed post | Story: today's feed post | |", "",
           "Why these times: Instagram evenings and weekend late mornings, Facebook lunchtime and LinkedIn weekday mornings are the usual peaks for Indian audiences. These are general benchmarks rather than NNWA data, since the channels are new to Buffer. After week 2 I'll check Buffer's analytics and move the slots if needed.", "",
           "## Calendar", "",
           "| Date | Platform | Format | Hook | CTA | Asset needed | Owner |", "|---|---|---|---|---|---|---|"]
    start = date(2026, 11, 1)
    for i in range(30):
        dd = start + timedelta(days=i)
        d = dd.isoformat()
        for p in [p for p in P if p["d"] == d]:
            plat = "LinkedIn" if p.get("li_only") else ("IG + FB" + (" + LinkedIn" if p.get("li") and (wd(d) < 5 or p.get("li_day")) else ""))
            cta = "Free guide" if p.get("cta") == "guide" else f"Course: {p.get('course','')}"
            if p.get("soft"):
                cta = "None in caption; guide link in first comment"
            asset = "PR #4 (exists)" if p.get("existing") else ("Motion reel + cover (Claude)" if "Reel" in p["fmt"] else "New creative (Claude)")
            out.append(f"| {dd:%a %d %b} | {plat} | {p['fmt']} | {p['hook']} | {cta} | {asset} | Claude schedules after approval |")
        out.append(f"| {dd:%a %d %b} | IG + FB Stories | Story x3 | Morning link frame; evening feed repost | Free guide or course link | Story frames (Claude) | Claude schedules |")
    out += ["", "## Festival and awareness days covered", "",
            "| Date | Day | How we mark it |", "|---|---|---|",
            "| Fri 6 Nov | Dhanteras | LinkedIn: invest in health (56.4% disease burden); Story greeting |",
            "| Sat 7 Nov | Choti Diwali | Story: frying-oil tip |",
            "| Sun 8 Nov | Diwali | Greeting post on all three platforms with the oil tip |",
            "| Mon 9 Nov | Govardhan Puja | Story greeting |",
            "| Tue 10 Nov | Bhai Dooj | Carousel: gift a habit |",
            "| Wed 11 Nov | National Education Day | Courses carousel |",
            "| Fri 13 to Mon 16 Nov | Chhath Puja | Greeting post on 13 Nov (Nahay Khay); Story greeting on 15 Nov (Sandhya Arghya) |",
            "| Sat 14 Nov | Children's Day and World Diabetes Day | Two feed posts |",
            "| 15 to 21 Nov | National Newborn Week | Breastfeeding post on 17 Nov |",
            "| Thu 19 Nov | International Men's Day | Hypertension post |",
            "| Tue 24 Nov | Guru Nanak Jayanti | Greeting post, no sales CTA |",
            "| Thu 26 Nov | National Milk Day | Milk and curd post |", "",
            "## Captions", "",
            "Week 1 feed captions (1 to 7 Nov) are in the lead-magnet plan (/mnt/project-files/lead-magnet-funnel/7-day-plan-lead-magnet.md). Everything else is below. Facebook uses the Instagram caption with the link in place of 'link in bio'. Every post has a first comment carrying the link and the sources.", ""]
    for p in P:
        if p.get("existing") and not p.get("ig") and not (p.get("li") and p["li"] != "see funnel plan" and not p.get("li", "").startswith("see")):
            continue
        out.append(f"### {date.fromisoformat(p['d']):%a %d %b}: {p['hook']}")
        out.append(f"Format: {p['fmt']}." + (f" Note: {p['note']}" if p.get("note") else ""))
        out.append("")
        if p.get("ig") and not p.get("li_only"):
            ig, fb, fc_ig, fc_fb = captions(p)
            out += ["**Instagram**", "", "```", ig, "```", "", "First comment (Instagram):", "", "```", fc_ig, "```", "",
                    "**Facebook**", "", "```", fb, "```", "", "First comment (Facebook):", "", "```", fc_fb, "```", ""]
        if p.get("li") and not str(p["li"]).startswith("see"):
            li, fc_li = li_caption(p)
            out += ["**LinkedIn**", "", "```", li, "```", "", "First comment (LinkedIn):", "", "```", fc_li, "```", ""]
        if p.get("alt"):
            out += [f"Alt text: {p['alt']}", ""]
        if p.get("li_alt"):
            out += [f"LinkedIn image alt text: {p['li_alt']}", ""]
    return "\n".join(out), items


SRC_LINE = {
    "DGI-burden": "ICMR-NIN, Dietary Guidelines for Indians, 2024", "DGI-T1": "ICMR-NIN, Dietary Guidelines for Indians, 2024 (CNNS data)",
    "DGI-T2": "ICMR-NIN, Dietary Guidelines for Indians, 2024 (NFHS-5 data)", "DGI-G": "ICMR-NIN, Dietary Guidelines for Indians, 2024",
    "DGI-oil": "ICMR-NIN, Dietary Guidelines for Indians, 2024", "DGI-sugar": "ICMR-NIN, Dietary Guidelines for Indians, 2024",
    "DGI-millet": "ICMR-NIN, Dietary Guidelines for Indians, 2024", "DGI-reuse": "ICMR-NIN, Dietary Guidelines for Indians, 2024",
    "DGI-swap": "ICMR-NIN, Dietary Guidelines for Indians, 2024", "DGI-move": "ICMR-NIN, Dietary Guidelines for Indians, 2024",
    "DGI-water": "ICMR-NIN, Dietary Guidelines for Indians, 2024", "DGI-salt": "ICMR-NIN, Dietary Guidelines for Indians, 2024",
    "DGI-plate": "ICMR-NIN, Dietary Guidelines for Indians, 2024", "RDA": "ICMR-NIN, Nutrient Requirements for Indians, 2020",
    "IFCT": "ICMR-NIN, Indian Food Composition Tables, 2017", "FSSAI-label": "FSSAI, Labelling and Display Regulations, 2020",
}


def sources(p):
    s = []
    for k in p.get("src", []):
        if SRC_LINE[k] not in s:
            s.append(SRC_LINE[k])
    # drop a plain citation when a more specific one for the same document is present
    return [x for x in s if not any(y != x and y.startswith(x) for y in s)]


def captions(p):
    src = sources(p)
    tags = " ".join(p.get("tags", []))
    course = p.get("cta") == "course"
    if course:
        ig_cta = f"Explore {'the course' if p.get('course') != 'All courses' else 'the courses'} from the link in bio."
    else:
        ig_cta = p.get("cta_line", "Get the free guide from the link in bio.")
    ig = p["ig"] + ("\n\n" + ig_cta if ig_cta else "") + ("\n\nSource: " + "; ".join(src) if src else "") + "\n\n" + tags
    fb_cta = ig_cta.replace("from the link in bio", "from the link in the first comment").replace("Link in bio.", "Link in the first comment.").replace("in the link in bio", "in the first comment")
    fb = p["ig"] + ("\n\n" + fb_cta if fb_cta else "") + ("\n\nSource: " + "; ".join(src) if src else "")
    dest = "course" if course else "guide"
    what = ("Courses (100% online): " if course else "Free guide, Protein, decoded: ")
    fc_ig = (("Link in bio: " + ("nnwa.in/courses" if course else "nnwa.in/protein")) +
             ("\nSources: " + "; ".join(src) if src else "") + ("\n" + DISCLAIMER if src else ""))
    fc_fb = what + link(dest, "facebook", "social", f"{p['d']}-{p['slug']}") + ("\nSources: " + "; ".join(src) if src else "")
    if not course and not GUIDE_LIVE:
        fb_cta = "" if (p.get("soft") or p["slug"] in GREETING) else ("It's coming soon. Follow the NNWA page to get it first." if "free guide" in p["ig"] and p["d"] > "2026-11-04" else "Our free guide, Protein, decoded, is coming soon. Follow the NNWA page to get it first.")
        fb = p["ig"] + ("\n\n" + fb_cta if fb_cta else "") + ("\n\nSource: " + "; ".join(src) if src else "")
        fc_ig = "Free guide, Protein, decoded: link in bio." + ("\nSources: " + "; ".join(src) if src else "") + ("\n" + DISCLAIMER if src else "")
        fc_fb = ("" if p["slug"] in GREETING else "Free guide, Protein, decoded: coming soon to this page.\n") + ("Sources: " + "; ".join(src) if src else "")
        fc_fb = fc_fb.strip()
    return ig, fb, fc_ig, fc_fb


def li_caption(p):
    src = sources(p)
    course = p.get("cta") == "course"
    tail = ("Courses are linked in the first comment." if course else "The free guide, Protein, decoded, is linked in the first comment.")
    if not course and not GUIDE_LIVE:
        tail = ("It's coming soon. Follow NNWA to get it first." if "free guide" in p["li"] and p["d"] > "2026-11-04" else "Our free guide, Protein, decoded, is coming soon. Follow NNWA to get it first.")
    if p.get("soft") or (p["slug"] in GREETING and not course):
        tail = ""
    li = p["li"] + ("\n\n" + tail if tail else "") + "\n\n#Nutrition #NutritionEducation #PublicHealth"
    dest = "course" if course else "guide"
    fc = ("Courses: " if course else "Free guide: ") + link(dest, "linkedin", "social", f"{p['d']}-{p['slug']}") + ("\nSources: " + "; ".join(src) if src else "")
    if not course and not GUIDE_LIVE:
        fc = (("" if p["slug"] in GREETING else "Free guide, Protein, decoded: coming soon.\n") + ("Sources: " + "; ".join(src) if src else "")).strip()
    return li, fc


if __name__ == "__main__":
    text, items = md()
    open(os.path.join(HERE, "calendar.md"), "w").write(text + "\n")
    json.dump({"posts": P, "schedule": items}, open(os.path.join(HERE, "posts.json"), "w"), indent=1, ensure_ascii=False)
    print(len(items), "scheduled items;", len(P), "feed/LinkedIn posts")
