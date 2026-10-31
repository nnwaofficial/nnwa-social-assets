# Protein, decoded: NNWA e-book (Edition 1, v3 "Editorial" design system)

Playbooks used: list-growth-designer (lead-magnet structure), content-writer (long-form copy), ig-humanizer pass, NNWA e-book design system "Editorial" (built 31 Oct 2026 from Hrito's 7 references and NNWA brand colours).

- Final file: `nnwa-protein-decoded-ebook.pdf` (A4 portrait, 24 pages, about 5 MB)
- Page previews: `pages/page-01.jpg` to `page-24.jpg`
- Design-system reference sheet: `design-system-sheet.jpg`
- Source: `source-v3/` (`ebook-system.css` holds every visual decision; `make_book.py` writes the HTML from page templates; `build.js` renders the PDF with Node Playwright; fonts and logos come from `skills-library/nnwa-social-posting/design-system/assets/`, copied into `source-v3/assets/` before building)
- Earlier versions: `_archive-v1/` (first social-style build), `redesign-v2-samples/` (mixed-style samples)

## Design system in one paragraph
12-column grid, 64 px side margins, 8 px spacing. Poppins for everything plus one Fraunces Italic word per title. Forest for dark grounds (cover, chapter openers, back cover, all on a thin brass line grid), paper for content pages, sage for panels and info strips, brass for numerals and rules. Nine page templates: cover, contents, chapter opener, content, data (big numerals), food card (circle plate photo + info strip), workbook (tracker, form boxes), sources, back cover. Same header, footer and title position on every inner page. Radius 10 / 16 / 50%, 1 px hairlines, no gradients.

Title rule (Hrito, 31 Oct 2026): no small tracked-caps label above a headline and no italic accent word on inner pages (read as generic AI design). Inner pages use the title row: brass chapter number, thin brass bar, Poppins Medium 32 title set tight on one line, 1.5 px forest rule under it. Numbered list items put the number beside the heading, never above it. In-page labels are sentence case. Fraunces Italic stays only on cover, openers and back cover.

Line-grid rule (Hrito, 31 Oct 2026): text never crosses a grid line. On forest pages every text block sits in a merged block of whole cells (`cell(col, row, w, h)` in `make_book.py`; grid is 8 x 12 cells inside a 40 px frame).

## Page plan
| # | Template | Content |
|---|---|---|
| 1 | Cover | Protein, decoded |
| 2 | Contents | 7 chapters, how to use, disclaimer |
| 3, 4 | Opener + content | 01 What protein does |
| 5, 6, 7 | Opener + content + data | 02 How much you need (0.83 g/kg, weight table) |
| 8, 9, 10 | Opener + data + content | 03 Where to find it (serving table, pairings) |
| 11, 12, 13 | Food cards | Dal and chawal, paneer, eggs |
| 14, 15 | Opener + content | 04 An example day (about 50 g) |
| 16, 17 | Opener + content | 05 Myths, checked |
| 18, 19 | Opener + content | 06 Supplements, carefully |
| 20, 21, 22 | Opener + workbook | 07 Weekly tracker, checklist and calculator |
| 23 | Sources | Sources, photo log, full disclaimer |
| 24 | Back cover | About NNWA, nnwa.in, @nnwa.official |

## Citation rule (Hrito, 31 Oct 2026)
Facts come only from government authorities (Priorities 1 to 4; associations removed). No citation marks, flags or source lines inside the pages (Hrito, comment on page 4): all citations sit in the bibliography on page 23, which lists each source with the pages that use it. In make_book.py, R(k) is an invisible marker that maps a page to source k; claims that cannot be sourced are deleted, never flagged.
1. ICMR-NIN, A Brief Note on Nutrient Requirements for Indians, the RDA and the EAR, 2020 (nin.res.in/rdabook/brief_note.pdf)
2. ICMR-NIN, Dietary Guidelines for Indians, 2024 (nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf)
3. ICMR-NIN, Indian Food Composition Tables, 2017 (nin.res.in/ebooks/IFCT2017_16122024.pdf)
4. FSSAI, Labelling and Display Regulations, 2020 (compendium 23.09.2021)
5. FSSAI, Advertising and Claims Regulations, 2018 (gazette notification)

Still unsourced: none. Every printed fact was checked against the documents above on 31 Oct 2026; unsourceable claims were rewritten or deleted. Full claim-by-claim log: fact-check-2026-10-31.md.

## Remaining checks
1. The full Nutrient Requirements 2020 report is only hosted on Google Drive (blocked by this environment), so source 1 is ICMR-NIN's own 6-page brief note of it, which carries the protein table.
2. Pexels photographer names: credited "Photo via Pexels" (design thread owns photos).

## Compliance notes
No outcome promises. Disclaimer on pages 2, 6, 19, 23. No course names, fees, dates or MSU line. No identifiable faces.

## Figma
Not yet added: Figma Starter plan MCP call cap. Earlier script in `source/` covers v1 only; regenerate for v3 when the cap resets.

## Photo style (31 Oct 2026, Hrito: "keep the photos very aesthetic")
One moody, top-down Indian food set from Pexels, colour-graded by NNWA (colour 0.86, contrast 1.04, 6% brass warm wash, shadows tinted forest). Photos sit in full grid cells on the cover (cols 0-3, rows 5-8) and each chapter opener (cols 4-7, rows 7-10), and as 380 px rounded panels on food cards. Graded files: source-v3/photos/cover.jpg, o1-o7.jpg, f-dal/f-paneer/f-egg.jpg. Pexels IDs: cover 29148133; openers 7090131, 15613811, 20408435, 8312083, 6546429, 2112789, 2831799; food 12737917, 12737805, 8625813. Photographer names [verify].

## Lead-magnet pages (31 Oct 2026)
Book is 34 pages. Engagement pages (names kept stable for the funnel thread's posts and emails): p03 "Your 60-second protein check" (self-check quiz), p21 "Eight easy wins" (quick wins), p31 "Stick this on your fridge" (printable cheat sheet), p29 weekly tracker, p33 "What to do next" (CTA: tracker, Protein in practice emails, share nnwa.in/protein [verify redirect], nnwa.in certifications; PDF links carry utm_source=ebook&utm_medium=pdf&utm_campaign=protein-decoded). Page numbers in the contents and cross-references are automatic: key("name") before a page, @@name@@ in text.
