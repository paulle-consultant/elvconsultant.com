# Daily BMS Mitsubishi post: runbook

Owner: Paul Le (DHP, official Mitsubishi Electric partner). Runs every day, fully automatic, no approval step. Push straight to `main`.

## 1. Pick the topic
- Open `bms/content-calendar.json`. Take the item whose `date` = today (Asia/Saigon). If none, take the first `planned` item with the earliest date.
- If fewer than 7 `planned` items remain, append 14 new ones (same weekday pillars, new topics, no repeats of published ones).

## 2. Facts
- Product specs ONLY from `bms/product-facts.md`. Never invent a number, price, project reference or client name.
- Regulations, market data, news: look up with web search, open the page, cite it in `sources`.
- Prices: give none unless from a cited source. Use relative words ("chi phí license thấp hơn").

## 3. Write `bms/posts/<date>-<slug>.json`
Keys (see `scripts/bms_post.py` docstring and the 2026-11-05 post as the model):
- `title_vi`/`title_en`: max 7 words. A title, not a sentence.
- `lead_vi`/`lead_en`: 1–2 sentences.
- `sections`: 4 sections in this order: Vấn đề / The problem; Giải pháp / Solution; Phân tích kỹ thuật / Engineering notes; Ứng dụng / Where it fits. HTML allowed: p, ul, ol, li, strong, code.
- `diagram`: one SVG schematic (SĐNL), see rules below. Mandatory.
- `table`: optional (point schedule, IO allocation, comparison).
- `hero_image`: Unsplash photo via the Unsplash tools (search_photos, then download_asset to record the download). Dark, landscape, technical subject (plant room, pipes, control panel, building facade). Use the images.unsplash.com URL with `&w=1600&h=900&fit=crop`. Credit name + photo page URL.
- `sources`, `tags` (5–8), `x_post`, `fb_post`.

Writing rules: Vietnamese the way an engineer writes to a client, direct. No em dash (—), no AI clichés ("trong bối cảnh", "không chỉ… mà còn", "hãy cùng", "giải pháp toàn diện", "In conclusion", "Overall"), no emoji in the article. At least 3 concrete numbers per article. Mention DHP as official Mitsubishi Electric partner only in the CTA (the template does this). Do not use Mitsubishi logos.

## 4. SVG schematic rules
- `viewBox="0 0 960 H"`, H 480–700. Font `'Maison Sans',system-ui,sans-serif`.
- Colours: background transparent (page is #0C0B09); boxes fill #15130F stroke #C9A96A 1px (secondary boxes stroke #5A5141); title text #F3EDE2 15px 500; detail text #B5AC9C 12.5px; protocol/level labels #C9A96A 12px; lines #C9A96A 1.2px; field wiring dashed #B5AC9C.
- Square corners. No gradients, glows, shadows.
- Lines must not run through text. If a label sits on a line, draw a `<rect fill="#0C0B09">` behind it (padding 4px) after the lines and before the label.
- Label every link with its protocol (BACnet/IP, MS/TP, Modbus RTU/TCP, hard-wired 0–10 V …).
- Escape `&` as `&amp;`. Validate with `python3 -c "import xml.dom.minidom;xml.dom.minidom.parseString(open('x.svg').read())"`.

## 5. Build, check, push
1. `python3 scripts/bms_post.py`
2. Screenshot the new page at 1280 and 390 px with Playwright and look at it: no text overlap in the SVG, no horizontal page scroll (only the figure scrolls).
3. Set the calendar item `status` to `published`, add `slug`.
4. `git add bms blog/bms && git commit -m "BMS post <date>: <title_en>"` with the session attribution lines, `git fetch origin main && git rebase origin/main && git push origin HEAD:main`.

## 6. Social (after push)
- X via Typefully, social set 352801 (@PLELVCONSULTANT): one post, English, ≤ 270 characters, NO URL in the text (X rejects API posts with links: 403). End with "Full schematic on the blog, link in bio." publish_at today 08:30 +07:00 (if already past, now + 15 min).
- Facebook page via Metricool, brand 7679282 (Elvconsultant.com), `facebookData.type` POST, `autoPublish` true, media = hero image URL, Vietnamese text 120–220 words ending with the link, the 48-hour SĐNL + BoM offer and 4–5 hashtags. Time 11:30 +07:00 (if past, now + 20 min).
- Both texts: no em dash, no clichés, one concrete number in the first line.

## 7. Report
Send Paul one short message: title, page link, X and Facebook schedule times. If any step failed, say which and why.
