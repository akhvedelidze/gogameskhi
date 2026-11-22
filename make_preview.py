from pathlib import Path
from bs4 import BeautifulSoup
import json, posixpath, base64
r=Path(__file__).resolve().parent; pages={}; fallback='data:image/svg+xml;base64,'+base64.b64encode((r/'assets/image-fallback.svg').read_bytes()).decode()
for f in sorted(r.rglob('*.html')):
 name=f.relative_to(r).as_posix(); soup=BeautifulSoup(f.read_text(),'html.parser'); body=soup.body
 for a in body.select('a[href]'):
  h=a['href']
  if not h.startswith(('http:','https:','#','mailto:')): a['href']='#/'+posixpath.normpath(posixpath.join(posixpath.dirname(name),h))
 for img in body.select('img[data-fallback]'):img['data-fallback']=fallback
 pages[name]={'html':body.decode_contents(),'title':soup.title.text,'lang':soup.html['lang']}
css=(r/'assets/style.css').read_text(); js=(r/'assets/main.js').read_text(); js=js.replace('(()=>{','function wirePage(){',1).replace('})();','}',1).replace('wirePhotoFallback();','')
font='<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Georgian:wght@400;600;700;800;900&display=swap" rel="stylesheet">'
script='const pages='+json.dumps(pages,ensure_ascii=False).replace('</','<\\/')+''';function renderPage(){const k=location.hash.startsWith('#/')?location.hash.slice(2):'index.html';const p=pages[k]||pages['index.html'];document.documentElement.lang=p.lang;document.title=p.title;document.body.innerHTML=p.html;wirePage();wirePhotoFallback();window.scrollTo(0,0);}window.addEventListener('hashchange',()=>{if(!location.hash||location.hash.startsWith('#/'))renderPage()});renderPage();'''
output='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="goga-preview" content="direct-youtube"><title>Goga Meskhi — Preview V5</title>'+font+'<style>'+css+'</style></head><body>'+pages['index.html']['html']+'<script>'+js+'\n'+script+'</script></body></html>'
(r.parent/'Goga_Meskhi_Website_Preview_v5.html').write_text(output)
