# NNWA November 2026 campaign

A lead campaign for 1 to 30 Nov 2026 on Instagram, Facebook and LinkedIn, scheduled through Buffer. All 158 posts for 1 to 30 Nov were scheduled on 31 Oct 2026, without the guide link.

- `calendar.md`: the 30-day calendar, daily rhythm, festival days, and paste-ready captions with first comments and alt text.
- `posts.json`: the machine-readable schedule.
- `buffer_payloads.py` / `buffer-payloads.json`: the exact Buffer create_post arguments (158 posts) that were scheduled.
- `sources.md`: every fact, with its government source and page.
- `ig-grid-preview.jpg`: the November Instagram grid, newest post first.
- `creatives.py`, `reels.py`, `wraps.py`: the scripts that render the creatives, the motion reels and the daily Stories. `tools/` holds the render.py and components.css they ran with: the lead-magnet version plus a `storywrap` layout and a no-sticker Story option.

Assets are in `2026/11/` (feed posts, carousels, LinkedIn PDFs, reel covers), `2026/11/stories/` and `2026/11/reels/`. The 1 to 8 Nov feed posts come from PR #4 and are not changed here.

## Rules applied
- Facts come from government sources only (ICMR-NIN, FSSAI, MoHFW data). Creatives carry no citations; sources go in the caption and the first comment.
- Each post has one CTA: the free guide (nnwa.in/protein) or a course (nnwa.in/courses). No comment-keyword CTAs and no DM automation.
- No fees, batch dates, placement or outcome claims. The MSU line is not used.
- Greeting posts are respectful and carry no sales CTA in the caption (Guru Nanak Jayanti).

## Status (31 Oct 2026)
- 158 posts are scheduled in Buffer (IG, FB, LinkedIn, 1 to 30 Nov). Buffer reads images and videos from this branch's raw URLs, so do not delete or rename `claude/project-thread-gc5kzu` or anything under `2026/11/` before 1 Dec 2026.
- The guide (nnwa.in/protein) is not live, so `GUIDE_LIVE = False` in calendar.py: Instagram says "link in bio", Facebook and LinkedIn say "coming soon, follow NNWA", and the 30 morning link-sticker Stories are held (not scheduled).
- Greeting posts (Chhath, Gurpurab) carry no guide line and no guide first comment.
- Hand edits made at send time: festival Story alt text for Choti Diwali, Govardhan Puja, Chhath and Gurpurab; 18 Nov LinkedIn uses the full "coming soon" line; 30 Nov IG/FB end with "See the courses and talk to a counsellor: link in bio / link in the first comment."

## When the guide goes live
1. Point the Instagram bio link at the guide.
2. Set `GUIDE_LIVE = True`, rerun calendar.py and buffer_payloads.py, then edit the remaining scheduled FB and LinkedIn posts to add the link, and schedule the 09:00 link Stories (the Story frames show a link-sticker placeholder, so add the sticker in Buffer).

## Still open
1. Course page URLs and descriptions need checking against nnwa.in, which is blocked in this environment.
2. Several creatives print nnwa.in/protein (for example the 1 Nov launch carousel and reel end cards); it should resolve once the guide is live.
3. Reels are silent; add audio in the app if wanted.
