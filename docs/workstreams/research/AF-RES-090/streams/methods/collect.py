from pathlib import Path
import sys,json,re,html
from concurrent.futures import ThreadPoolExecutor
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'tools'))
from http_evidence import fetch
rows=[
 ('M01','https://docs.github.com/en/repositories/working-with-files/using-files/getting-permanent-links-to-files'),
 ('M02','https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files'),
 ('M03','https://html.spec.whatwg.org/multipage/urls-and-fetching.html'),
 ('M04','https://pkgdown.r-lib.org/reference/build_articles.html'),
 ('M05','https://docs.readthedocs.com/platform/stable/versioning-schemes.html'),
 ('M06','https://www.mkdocs.org/user-guide/writing-your-docs/'),
 ('M07','https://www.sphinx-doc.org/en/master/usage/referencing.html'),
]
evidence=Path(__file__).parent/'evidence'
def get(x):
 rid,url=x;rec,b=fetch(url,rid,evidence); s=b.decode(errors='replace'); s=re.sub(r'<(script|style)\b[^>]*>.*?</\1>','',s,flags=re.S); s=html.unescape(re.sub('<[^>]*>',' ',s));s=re.sub(r'\s+',' ',s); (evidence/'raw'/(rid+'.txt')).write_text(s);return {k:rec[k] for k in ['source_id','status','body_bytes','sha256','retrieved_utc']}
with ThreadPoolExecutor(max_workers=4) as ex:
 for r in ex.map(get,rows):print(json.dumps(r))
