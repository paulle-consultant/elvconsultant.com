#!/usr/bin/env python3
"""BMS Mitsubishi series (DHP x Diamond Controls) for elvconsultant.com.

Content lives in bms/posts/<date>-<slug>.json. This script renders:
  blog/bms/<date>-<slug>.html   one bilingual article per JSON file
  blog/bms/index.html           the series index, newest first
  bms/feed.json                 machine list used by the social scheduler

Usage: python3 scripts/bms_post.py            (render everything)
JSON keys: date, slug, pillar_vi, pillar_en, title_vi, title_en, lead_vi, lead_en,
  tags[], diagram{svg, caption_vi, caption_en}, sections[{h_vi,h_en,vi,en}] (vi/en = HTML),
  table{caption_vi, caption_en, head[], rows[[]]} (optional), sources[{title,url}],
  x_post, fb_post, hero_note (optional)
"""
import json, glob, os, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, "bms", "posts")
OUT = os.path.join(ROOT, "blog", "bms")
SITE = "https://elvconsultant.com"

VI_DOW = ["THỨ HAI", "THỨ BA", "THỨ TƯ", "THỨ NĂM", "THỨ SÁU", "THỨ BẢY", "CHỦ NHẬT"]

FONTS = "".join(
    f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{w};font-display:swap;src:url(/assets/fonts/{f}-{sub}-{w}-{st}.woff2) format('woff2')}}"
    for fam, f, ws, sts in [("Maison Serif", "cormorant-garamond", [400, 500], ["normal"]),
                            ("Maison Serif", "cormorant-garamond", [400], ["italic"]),
                            ("Maison Sans", "be-vietnam-pro", [300, 400, 500, 600], ["normal"])]
    for w in ws for st in sts for sub in ["vietnamese", "latin-ext", "latin"]
)

CSS = FONTS + """
:root{--bg:#0C0B09;--surface:#15130F;--ink:#F3EDE2;--muted:#B5AC9C;--accent:#C9A96A;--accent-ink:#16120B;--line:#2A251C;--paper:#F7F3EC;--bronze:#7A5A26;
--serif:'Maison Serif',Georgia,serif;--sans:'Maison Sans',system-ui,sans-serif;--track:.16em;--maxw:1080px;--gut:clamp(16px,4vw,40px);--ease-out:cubic-bezier(.23,1,.32,1)}
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);font-weight:300;font-size:17px;line-height:1.75;overflow-x:hidden}
a{color:var(--accent)}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 var(--gut)}
.label{font-size:13px;letter-spacing:var(--track);text-transform:uppercase;font-weight:500;color:var(--accent)}
header.top{border-bottom:1px solid var(--line)}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:68px;flex-wrap:wrap}
.brand{font-family:var(--serif);font-size:22px;color:var(--ink);text-decoration:none;letter-spacing:.02em}
.nav{display:flex;gap:20px;align-items:center;flex-wrap:wrap}
.nav a{color:var(--muted);text-decoration:none;font-size:13px;letter-spacing:var(--track);text-transform:uppercase}
.lang{display:flex;border:1px solid var(--line)}
.lang button{background:none;border:0;color:var(--muted);font:500 13px var(--sans);letter-spacing:var(--track);padding:6px 12px;cursor:pointer}
.lang button[aria-pressed=true]{background:var(--accent);color:var(--accent-ink)}
.lang button:active{transform:scale(.97)}
.hero{padding:clamp(48px,8vw,104px) 0 clamp(32px,5vw,56px);border-bottom:1px solid var(--line)}
.hero h1{font-family:var(--serif);font-weight:400;font-size:clamp(44px,8vw,116px);line-height:1.12;letter-spacing:-.015em;margin:18px 0 26px;max-width:14ch}
.hero .actions{margin-top:28px}.btn-solid{display:inline-flex;align-items:center;min-height:48px;background:var(--accent);color:var(--accent-ink);text-decoration:none;padding:0 24px;font-size:13px;letter-spacing:var(--track);text-transform:uppercase;font-weight:500}.btn-solid:active{transform:scale(.97)}
.photo{margin:0;position:relative}.photo img{display:block;width:100%;height:clamp(260px,46vw,620px);object-fit:cover}.photo figcaption{font-size:13px;color:var(--muted);padding:10px 0 0}
h2.fig{font-family:var(--serif);font-weight:400;font-size:clamp(26px,3vw,34px);line-height:1.2;margin-bottom:18px}
@media (prefers-reduced-motion:no-preference){.rv{opacity:0;transform:translateY(16px);transition:opacity .7s var(--ease-out),transform .7s var(--ease-out)}.rv.in{opacity:1;transform:none}}
.hero .lead{font-size:clamp(18px,2vw,21px);color:var(--muted);max-width:62ch}
.meta{display:flex;gap:10px 24px;flex-wrap:wrap;margin-top:28px;color:var(--muted);font-size:13px;letter-spacing:var(--track);text-transform:uppercase}
.tags{display:flex;gap:8px;flex-wrap:wrap;margin-top:18px}
.tags span{border:1px solid var(--line);padding:3px 10px;font-size:13px;color:var(--muted)}
figure.sdnl{margin:clamp(40px,6vw,72px) 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:28px 0}
figure.sdnl .scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
figure.sdnl svg{display:block;width:100%;min-width:720px;height:auto}
figure.sdnl .hint{display:none;color:var(--muted);font-size:13px;margin-bottom:8px}@media(max-width:760px){figure.sdnl .hint{display:block}}
figure.sdnl figcaption{margin-top:14px;color:var(--muted);font-size:15px}
article .sec{display:grid;grid-template-columns:minmax(0,1fr);gap:8px;padding:clamp(28px,4vw,44px) 0;border-bottom:1px solid var(--line)}
@media(min-width:900px){article .sec{grid-template-columns:260px minmax(0,1fr);gap:48px}}
article h2{font-family:var(--serif);font-weight:400;font-size:clamp(26px,3vw,34px);line-height:1.2}
article .body p{margin-bottom:14px;max-width:68ch}
article .body ul,article .body ol{margin:0 0 14px 22px;max-width:66ch}
article .body li{margin-bottom:6px}
article .body strong{font-weight:500;color:var(--ink)}
article .body code{font-size:15px;background:var(--surface);padding:1px 6px;border:1px solid var(--line)}
.tbl{overflow-x:auto;margin:clamp(28px,4vw,44px) 0}
table{width:100%;border-collapse:collapse;font-size:15px;min-width:560px}
caption{caption-side:top;text-align:left;margin-bottom:12px;color:var(--muted);font-size:13px;letter-spacing:var(--track);text-transform:uppercase}
th,td{text-align:left;padding:12px 14px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-weight:500;color:var(--accent);font-size:13px;letter-spacing:.08em;text-transform:uppercase}
.cta{margin:clamp(48px,7vw,88px) 0;padding:clamp(28px,4vw,48px);background:var(--paper);color:#1B1814}
.cta h3{font-family:var(--serif);font-weight:400;font-size:clamp(26px,3vw,36px);line-height:1.2;margin-bottom:10px}
.cta p{color:#4A4339;max-width:60ch;margin-bottom:20px}
.cta a.btn{display:inline-block;background:#16120B;color:var(--paper);text-decoration:none;padding:12px 22px;font-size:13px;letter-spacing:var(--track);text-transform:uppercase}
.cta a.btn:active{transform:scale(.97)}
.src{padding-bottom:56px;color:var(--muted);font-size:15px}
.src ol{margin-left:20px}
footer{border-top:1px solid var(--line);padding:28px 0;color:var(--muted);font-size:13px;letter-spacing:.06em}
.list{padding:clamp(32px,5vw,56px) 0}
.item{display:grid;grid-template-columns:minmax(0,1fr);gap:6px 40px;padding:28px 0;border-bottom:1px solid var(--line);text-decoration:none;color:var(--ink)}
@media(min-width:900px){.item{grid-template-columns:220px minmax(0,1fr)}}
.item h2{font-family:var(--serif);font-weight:400;font-size:clamp(24px,2.8vw,32px);line-height:1.2}
.item p{color:var(--muted);margin-top:8px;max-width:70ch}
@media (hover:hover) and (pointer:fine){.item h2{transition:color .2s var(--ease-out)}.item:hover h2{color:var(--accent)}.nav a:hover{color:var(--ink)}}
[data-l=en]{display:none}
html[lang=en] [data-l=vi]{display:none}
html[lang=en] [data-l=en]{display:revert}
"""

JS = """<script>
(function(){var els=document.querySelectorAll('.rv');if(!('IntersectionObserver' in window)){els.forEach(e=>e.classList.add('in'));return}var io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{rootMargin:'0px 0px -10% 0px'});els.forEach(e=>io.observe(e))})();
function setLang(l){document.documentElement.lang=l;document.querySelectorAll('.lang button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.set===l));try{localStorage.setItem('lang',l)}catch(e){}}
(function(){var l='vi';try{l=localStorage.getItem('lang')||'vi'}catch(e){}setLang(l);document.querySelectorAll('.lang button').forEach(b=>b.addEventListener('click',()=>setLang(b.dataset.set)))})();
</script>"""


def esc(s):
    return html.escape(s or "", quote=True)


def bi(vi, en, tag="span", raw=False):
    f = (lambda x: x) if raw else esc
    return f'<{tag} data-l="vi">{f(vi)}</{tag}><{tag} data-l="en">{f(en)}</{tag}>'


def head(title, desc, url, extra=""):
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="Paul Le · DHP Technology &amp; Integration">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
{extra}<style>{CSS}</style>
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="/">Paul Le · ELV Consultant</a>
<nav class="nav"><a href="/blog/bms/">BMS Mitsubishi</a><a href="/blog/">Blog</a><a href="/#contact">{bi('Liên hệ','Contact')}</a>
<div class="lang" role="group" aria-label="Language"><button data-set="vi" aria-pressed="true">VI</button><button data-set="en" aria-pressed="false">EN</button></div></nav>
</div></header>
"""


FOOT = """<footer><div class="wrap">© {y} Paul Le · DHP Technology &amp; Integration · <span data-l="vi">Đối tác chính thức Mitsubishi Electric, giải pháp BMS Diamond Controls</span><span data-l="en">Official Mitsubishi Electric partner, Diamond Controls BMS solutions</span> · <a href="/">elvconsultant.com</a></div></footer>
""" + JS + "\n</body>\n</html>\n"


def date_label(d):
    dt = datetime.date.fromisoformat(d)
    return f"{VI_DOW[dt.weekday()]} · {dt.strftime('%d/%m/%Y')}", dt.strftime("%A · %d %b %Y").upper()


def render_post(p):
    url = f"{SITE}/blog/bms/{p['date']}-{p['slug']}.html"
    dvi, den = date_label(p["date"])
    ld = {"@context": "https://schema.org", "@type": "TechArticle", "headline": p["title_en"], "inLanguage": ["vi", "en"],
          "datePublished": p["date"], "author": {"@type": "Person", "name": "Paul Le"},
          "publisher": {"@type": "Organization", "name": "DHP Technology & Integration"}, "mainEntityOfPage": url,
          "keywords": ", ".join(p.get("tags", []))}
    out = [head(f"{p['title_vi']} | BMS Mitsubishi · Paul Le", p["lead_vi"], url,
                f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')]
    out.append('<main class="wrap"><article>')
    out.append(f'<section class="hero"><div class="label">{bi("BMS Mitsubishi · " + p["pillar_vi"], "BMS Mitsubishi · " + p["pillar_en"])}</div>')
    out.append(f'<h1>{bi(p["title_vi"], p["title_en"])}</h1><p class="lead">{bi(p["lead_vi"], p["lead_en"])}</p>')
    out.append(f'<div class="meta">{bi(dvi, den)}<span>Paul Le · DHP</span></div>')
    out.append('<div class="tags">' + "".join(f"<span>{esc(t)}</span>" for t in p.get("tags", [])) + "</div>")
    out.append(f'<div class="actions"><a class="btn-solid" href="/#contact">{bi("Nhận SĐNL + BoM trong 48 giờ", "Get schematic + BoM in 48 h")}</a></div></section>')
    hi = p.get("hero_image")
    if hi:
        out.append(f'<figure class="photo rv"><img src="{esc(hi["src"])}" alt="{esc(hi["alt"])}" width="1600" height="900" fetchpriority="high">'
                   f'<figcaption>Photo: <a href="{esc(hi["credit_url"])}" rel="noopener" target="_blank">{esc(hi["credit"])}</a> / Unsplash</figcaption></figure>')
    dg = p.get("diagram")
    if dg:
        out.append(f'<figure class="sdnl rv"><h2 class="fig">{bi("Sơ đồ nguyên lý","Schematic diagram")}</h2>'
                   f'<div class="hint">{bi("Vuốt ngang để xem toàn bộ sơ đồ", "Swipe sideways to see the full diagram")}</div>'
                   f'<div class="scroll">{dg["svg"]}</div><figcaption>{bi(dg["caption_vi"], dg["caption_en"])}</figcaption></figure>')
    for s in p["sections"]:
        out.append(f'<section class="sec rv"><h2>{bi(s["h_vi"], s["h_en"])}</h2><div class="body">'
                   f'<div data-l="vi">{s["vi"]}</div><div data-l="en">{s["en"]}</div></div></section>')
    t = p.get("table")
    if t:
        rows = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in t["rows"])
        out.append(f'<div class="tbl rv"><h2 class="fig">{bi(t["caption_vi"], t["caption_en"])}</h2><table><thead><tr>'
                   + "".join(f"<th>{esc(h)}</th>" for h in t["head"]) + f"</tr></thead><tbody>{rows}</tbody></table></div>")
    out.append('<aside class="cta">' + bi("Cần BMS Mitsubishi cho dự án của anh/chị?", "Planning a Mitsubishi BMS for your project?", "h3")
               + bi("DHP là đối tác chính thức của Mitsubishi Electric. Gửi bản vẽ M&E, chúng tôi trả về sơ đồ nguyên lý, point schedule và BoM trong 48 giờ.",
                    "DHP is an official Mitsubishi Electric partner. Send your M&E drawings and get a schematic, point schedule and BoM within 48 hours.", "p")
               + f'<a class="btn" href="/#contact">{bi("Đặt lịch tư vấn", "Book a consultation")}</a></aside>')
    if p.get("sources"):
        out.append('<section class="src"><div class="label">' + bi("Nguồn", "Sources") + "</div><ol>"
                   + "".join(f'<li><a href="{esc(s["url"])}" rel="noopener" target="_blank">{esc(s["title"])}</a></li>' if s.get("url") else f"<li>{esc(s['title'])}</li>" for s in p["sources"])
                   + "</ol></section>")
    out.append("</article></main>")
    out.append(FOOT.replace("{y}", p["date"][:4]))
    return "".join(out)


def render_index(posts):
    url = f"{SITE}/blog/bms/"
    out = [head("BMS Mitsubishi Electric · Diamond Controls | Paul Le · DHP",
                "Giải pháp BMS Mitsubishi Electric Diamond Controls (Niagara 4): sơ đồ nguyên lý, cấu hình DDC, ứng dụng khách sạn, văn phòng, bệnh viện, nhà máy.", url)]
    out.append('<main class="wrap"><section class="hero"><div class="label">' + bi("Chuyên mục hằng ngày", "Daily series") + "</div>")
    out.append("<h1>" + bi("BMS Mitsubishi, từng sơ đồ một", "Mitsubishi BMS, one schematic a day") + "</h1>")
    out.append('<p class="lead">' + bi("Mỗi ngày một giải pháp BMS Diamond Controls trên nền Niagara 4: sơ đồ nguyên lý, cấu hình DDC, point schedule và cách áp dụng cho dự án tại Việt Nam.",
                                       "One Diamond Controls BMS solution a day on Niagara 4: schematics, DDC configuration, point schedules and how to apply them to projects in Vietnam.") + "</p></section>")
    out.append('<section class="list">')
    for p in posts:
        dvi, den = date_label(p["date"])
        out.append(f'<a class="item rv" href="/blog/bms/{p["date"]}-{p["slug"]}.html"><div class="label">{bi(dvi, den)}<br>{bi(p["pillar_vi"], p["pillar_en"])}</div>'
                   f'<div><h2>{bi(p["title_vi"], p["title_en"])}</h2><p>{bi(p["lead_vi"], p["lead_en"])}</p></div></a>')
    out.append("</section></main>")
    out.append(FOOT.replace("{y}", str(datetime.date.today().year)))
    return "".join(out)


def main():
    os.makedirs(OUT, exist_ok=True)
    posts = []
    for f in sorted(glob.glob(os.path.join(POSTS, "*.json"))):
        p = json.load(open(f, encoding="utf-8"))
        posts.append(p)
        open(os.path.join(OUT, f"{p['date']}-{p['slug']}.html"), "w", encoding="utf-8").write(render_post(p))
    posts.sort(key=lambda p: p["date"], reverse=True)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(render_index(posts))
    feed = [{"date": p["date"], "slug": p["slug"], "title_vi": p["title_vi"], "title_en": p["title_en"],
             "url": f"{SITE}/blog/bms/{p['date']}-{p['slug']}.html", "x_post": p.get("x_post", ""), "fb_post": p.get("fb_post", "")} for p in posts]
    json.dump(feed, open(os.path.join(ROOT, "bms", "feed.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"rendered {len(posts)} BMS posts")


if __name__ == "__main__":
    main()
