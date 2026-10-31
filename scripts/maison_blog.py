#!/usr/bin/env python3
"""Apply the Maison luxury theme to blog pages: recolour old navy/cyan literals, drop Google Fonts,
link ../assets/maison.css. Idempotent. Run by .github/workflows/maison-blog.yml on every push to blog/."""
import re,glob,sys
M={'#00C8E0':'#C9A96A','#4A6280':'#8A8172','#F0F4F8':'#F3EDE2','#1B2A4A':'#2A251C','#A0B4C8':'#B5AC9C','#0D1B35':'#121009','#1E3550':'#2A251C','#07111F':'#0C0B09','#101E30':'#15130F','#00A9BF':'#B39257','#007A8C':'#7A5A26'}
RG={r'rgba\(\s*0\s*,\s*200\s*,\s*224\s*,':'rgba(201,169,106,',r'rgba\(\s*7\s*,\s*17\s*,\s*31\s*,':'rgba(12,11,9,',r'rgba\(\s*74\s*,\s*98\s*,\s*128\s*,':'rgba(138,129,114,',r'rgba\(\s*27\s*,\s*42\s*,\s*74\s*,':'rgba(42,37,28,',r'rgba\(\s*30\s*,\s*53\s*,\s*80\s*,':'rgba(42,37,28,',r'rgba\(\s*1[68]\s*,\s*3[04]\s*,\s*(48|54)\s*,':'rgba(21,19,15,',r'rgba\(\s*1[13]\s*,\s*2[0-7]\s*,\s*(34|43|53)\s*,':'rgba(18,16,9,',r'rgba\(\s*240\s*,\s*244\s*,\s*248\s*,':'rgba(243,237,226,',r'rgba\(\s*160\s*,\s*180\s*,\s*200\s*,':'rgba(181,172,156,'}
LINK='<link rel="stylesheet" href="../assets/maison.css">'
for f in (sys.argv[1:] or glob.glob("blog/*.html")):
    s=open(f,encoding='utf-8').read(); o=s
    for k,v in M.items(): s=re.sub(re.escape(k),v,s,flags=re.I)
    for k,v in RG.items(): s=re.sub(k,v,s,flags=re.I)
    s=re.sub(r'\s*<link[^>]*fonts\.googleapis\.com/css2[^>]*>','',s)
    if 'maison.css' not in s: s=s.replace('</head>','  '+LINK+'\n</head>',1)
    if s!=o: open(f,'w',encoding='utf-8').write(s)
    if s!=o: print('restyled', f)
