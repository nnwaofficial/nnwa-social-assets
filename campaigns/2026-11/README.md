# NNWA November 2026 campaign

A lead campaign for 1 to 30 Nov 2026 on Instagram, Facebook and LinkedIn, scheduled through Buffer. 154 posts for 1 to 30 Nov are scheduled. On 31 Oct 2026 every post was moved off the Protein, decoded guide onto a course-linked free resource on nnwa.in.

- `calendar.md`: the 30-day calendar, daily rhythm, festival days, and paste-ready captions with first comments and alt text.
- `posts.json`: the machine-readable schedule.
- `buffer_payloads.py` / `buffer-payloads.json`: the exact Buffer create_post arguments (154 posts) as scheduled.
- `sources.md`: every fact, with its government source and page.
- `ig-grid-preview.jpg`: the November Instagram grid, newest post first.
- `motion/`: the reel motion engine (31 Oct 2026). `reel.html` draws any frame deterministically (masked kinetic type, Fraunces weight morphs, count-up numbers, circle, panel and inset transitions, parallax photos, light leak, grain); `reels.json` holds the scenes (same sourced facts); `render.js` captures 30 fps into ffmpeg: `node motion/render.js 2026/11/reels`. `audio.py` composes an original 120 BPM track (key per reel) and haptic sound effects from the engine's `events()`, so every tick, whoosh, pop and chime lands on its animation; the mix is normalised to -14 LUFS. Everything is synthesised, so there is no music licence to manage.
- `creatives.py`, `reels.py` (superseded by motion/), `wraps.py`: the scripts that render the creatives, the motion reels and the daily Stories. `tools/` holds the render.py and components.css they ran with: the lead-magnet version plus a `storywrap` layout and a no-sticker Story option.

Assets are in `2026/11/` (feed posts, carousels, LinkedIn PDFs, reel covers), `2026/11/stories/` and `2026/11/reels/`. The 1 to 8 Nov feed posts come from PR #4; their CTA footers were re-rendered from `week1-specs/` (now "Free tools: nnwa.in").

## Rules applied
- Facts come from government sources only (ICMR-NIN, FSSAI, MoHFW data). Creatives carry no citations; sources go in the caption and the first comment.
- Each post names one relevant NNWA course in the caption, and its first comment links one free resource on nnwa.in (a calculator, a guide or the gated Indian Diet Starter Guide) plus the course page, with UTM tags (utm_campaign=nov-2026). Instagram comments carry plain nnwa.in paths, since IG links are not clickable. The mapping is the `LEAD` block in calendar.py. No comment-keyword CTAs and no DM automation.
- No fees, batch dates, placement or outcome claims. The MSU line is not used.
- Greeting posts (Diwali, Chhath, Guru Nanak Jayanti) carry no sales CTA in the caption; their first comment still links a free resource and a course (`GREET_LEAD` in calendar.py). Every feed post has a first comment; Stories cannot carry one.

## Status (31 Oct 2026)
- 154 posts are scheduled in Buffer (IG, FB, LinkedIn, 1 to 30 Nov). Buffer reads images and videos from this branch's raw URLs, so do not delete or rename `claude/project-thread-gc5kzu` or anything under `2026/11/` before 1 Dec 2026. Re-rendered files were sent to Buffer with `?v=2` on the URL so it fetched the new versions.
- Protein, decoded is no longer the default CTA. The 1 Nov launch post (`guide-launch`, IG + FB + two Stories) is held via `HELD` in calendar.py and was deleted from Buffer, so 1 Nov has no feed post. The 30 morning link-sticker Stories are still not scheduled.
- Greeting posts (Diwali, Chhath, Gurpurab) carry no sales line in the caption; the free resource and course go in the first comment.

## To restore the guide launch
1. Make nnwa.in/protein live and point the Instagram bio at it (or a link page).
2. Remove `guide-launch` from `HELD`, set `GUIDE_LIVE = True`, rerun calendar.py and buffer_payloads.py, and create the four guide-launch posts in Buffer.

## Still open
1. Next batches start 11 Nov and 11 Dec 2026 (Hrito, 31 Oct). The CMS (Sanity, Diploma programme) already holds 11 Nov; it has no field for a second date, so 11 Dec has to go on the site after 11 Nov passes or via a schema change. Social posts still carry no dates.
2. Hrito to set the Instagram bio link to nnwa.in/tools/ and play one reel with sound before 4 Nov (no tool can edit the bio, and Claude cannot hear audio).
3. Reels carry original synthesised music and sound effects (no licence needed). Instagram may still suggest trending audio in the app; that is optional.

## Morning link Stories (added 31 Oct 2026)
Hrito asked for a 09:00 Instagram Story every day linking to that day's free nnwa.in resource. `am-stories/am_stories.py` maps each day's feed post to its resource (LEAD / GREET_LEAD in calendar.py) and writes `am-stories.json`; `am-stories/render.js` renders `am.html` to 1080x1920 JPGs in `2026/11/stories/am/`. Each Story: resource name, what you get (taken from the resource page on nnwa.in), the day's post, the matching course, and a clear zone for the link sticker (Buffer `instagram.link`, UTM medium=story). All 30 are scheduled in Buffer. Instagram only: Facebook Stories cannot carry links. These replace the old guide link-sticker frames (GUIDE_LIVE branch in build()).
