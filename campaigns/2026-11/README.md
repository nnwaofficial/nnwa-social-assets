# NNWA November 2026 campaign

A lead campaign for 1 to 30 Nov 2026 on Instagram, Facebook and LinkedIn, scheduled through Buffer. 154 posts for 1 to 30 Nov are scheduled. On 31 Oct 2026 every post was moved off the Protein, decoded guide onto a course-linked free resource on nnwa.in.

- `calendar.md`: the 30-day calendar, daily rhythm, festival days, and paste-ready captions with first comments and alt text.
- `posts.json`: the machine-readable schedule.
- `buffer_payloads.py` / `buffer-payloads.json`: the exact Buffer create_post arguments (154 posts) as scheduled.
- `sources.md`: every fact, with its government source and page.
- `ig-grid-preview.jpg`: the November Instagram grid, newest post first.
- `creatives.py`, `reels.py`, `wraps.py`: the scripts that render the creatives, the motion reels and the daily Stories. `tools/` holds the render.py and components.css they ran with: the lead-magnet version plus a `storywrap` layout and a no-sticker Story option.

Assets are in `2026/11/` (feed posts, carousels, LinkedIn PDFs, reel covers), `2026/11/stories/` and `2026/11/reels/`. The 1 to 8 Nov feed posts come from PR #4; their CTA footers were re-rendered from `week1-specs/` (now "Free tools: nnwa.in").

## Rules applied
- Facts come from government sources only (ICMR-NIN, FSSAI, MoHFW data). Creatives carry no citations; sources go in the caption and the first comment.
- Each post names one relevant NNWA course in the caption, and its first comment links one free resource on nnwa.in (a calculator, a guide or the gated Indian Diet Starter Guide) plus the course page, with UTM tags (utm_campaign=nov-2026). Instagram comments carry plain nnwa.in paths, since IG links are not clickable. The mapping is the `LEAD` block in calendar.py. No comment-keyword CTAs and no DM automation.
- No fees, batch dates, placement or outcome claims. The MSU line is not used.
- Greeting posts are respectful and carry no sales CTA in the caption (Guru Nanak Jayanti).

## Status (31 Oct 2026)
- 154 posts are scheduled in Buffer (IG, FB, LinkedIn, 1 to 30 Nov). Buffer reads images and videos from this branch's raw URLs, so do not delete or rename `claude/project-thread-gc5kzu` or anything under `2026/11/` before 1 Dec 2026. Re-rendered files were sent to Buffer with `?v=2` on the URL so it fetched the new versions.
- Protein, decoded is no longer the default CTA. The 1 Nov launch post (`guide-launch`, IG + FB + two Stories) is held via `HELD` in calendar.py and was deleted from Buffer, so 1 Nov has no feed post. The 30 morning link-sticker Stories are still not scheduled.
- Greeting posts (Diwali, Chhath, Gurpurab) carry no sales line; sources go in the first comment only.

## To restore the guide launch
1. Make nnwa.in/protein live and point the Instagram bio at it (or a link page).
2. Remove `guide-launch` from `HELD`, set `GUIDE_LIVE = True`, rerun calendar.py and buffer_payloads.py, and create the four guide-launch posts in Buffer.

## Still open
1. The nnwa.in header banner shows "Next batch begins 11 October 2026", which is in the past.
2. Instagram has one bio link; point it at nnwa.in/tools/ or a link page so each post's resource is reachable.
3. Reels are silent; add audio in the app if wanted.
