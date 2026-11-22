"""Read four independent field documents; no workbook mutation or remote write."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import json
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / 'cache'
CACHE.mkdir(parents=True, exist_ok=True)
BASE = 'https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/'
ARTICLE = BASE + 'articles/reconciliationofmidyearpopulationestimateswithcensus2021englandandwales/2023-02-28'
DATA = BASE + 'datasets/estimatesofthepopulationforenglandandwales/mid20222023localauthorityboundaires'
FILES = [
    ('F01', 'https://apps.cio.ny.gov/apps/mediaContact/public/view.cfm?parm=926C019C-DE79-DD17-D6493016DF74143F_5D9C1A27-C9C7-90C0-217C93A974EEA6D8', 'html'),
    ('F02', 'https://www.nyc.gov/assets/planning/download/pdf/planning-level/transportation/covid19-transportation/20200421.pdf', 'pdf'),
    ('F03-current', ARTICLE + '/previous/', 'html'),
    ('F03-v1', ARTICLE + '/previous/v1', 'html'),
    ('F03-v2', ARTICLE + '/previous/v2', 'html'),
    ('F04-index', DATA, 'html'),
    ('F04-v1', 'https://www.ons.gov.uk/file?uri=%2Fpeoplepopulationandcommunity%2Fpopulationandmigration%2Fpopulationestimates%2Fdatasets%2Festimatesofthepopulationforenglandandwales%2Fmid20222023localauthorityboundaires%2Fprevious%2Fv1%2Fmye22tablesew2023geogs.xlsx', 'xlsx'),
    ('F04-v2', 'https://www.ons.gov.uk/file?uri=%2Fpeoplepopulationandcommunity%2Fpopulationandmigration%2Fpopulationestimates%2Fdatasets%2Festimatesofthepopulationforenglandandwales%2Fmid20222023localauthorityboundaires%2Fprevious%2Fv2%2Fmye22tablesew2023geogsv2.xlsx', 'xlsx'),
]

class Plain(HTMLParser):
    def __init__(self):
        super().__init__(); self.out=[]; self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.skip += 1
        if tag in ('p','div','li','h1','h2','h3','h4','tr','br'): self.out.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.skip=max(0,self.skip-1)
        if tag in ('p','div','li','h1','h2','h3','h4','tr'): self.out.append('\n')
    def handle_data(self, data):
        if not self.skip: self.out.append(data)

def fetch(item):
    source_id,url,ext=item
    a={'attempt_id':'FIELD-DIRECT-'+source_id,'source_id':source_id.split('-')[0],
       'kind':'direct_body_open','url':url,'started_utc':datetime.now(timezone.utc).isoformat()}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (public research)'})
        with urllib.request.urlopen(req,timeout=45) as r:
            raw=r.read(); a.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'))
        path=CACHE/(source_id+'.'+ext); path.write_bytes(raw)
        a.update(body_sha256=sha256(raw).hexdigest(),bytes=len(raw),cache_path=str(path.relative_to(ROOT.parent)),outcome='opened')
        if ext=='html':
            p=Plain();p.feed(raw.decode('utf-8',errors='replace'))
            text='\n'.join(' '.join(x.split()) for x in ''.join(p.out).splitlines() if x.strip())+'\n'
            (CACHE/(source_id+'.txt')).write_text(text)
            a['text_sha256']=sha256(text.encode()).hexdigest()
        elif ext=='pdf':
            r=subprocess.run(['pdftotext','-layout',str(path),str(CACHE/(source_id+'.txt'))],capture_output=True,text=True)
            a['extract_exit_code']=r.returncode
        return a
    except Exception as e:
        a.update(outcome='failed',error=type(e).__name__+': '+str(e),next_action='Use already-open web extraction or official alternate version; do not infer content from search snippet')
        return a

if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(fetch,FILES))
    for a in rows: a['ended_utc']=datetime.now(timezone.utc).isoformat()
    (ROOT/'field_fetch_attempts.jsonl').write_text(''.join(json.dumps(a,ensure_ascii=False)+'\n' for a in rows))
    print(json.dumps([{k:v for k,v in a.items() if k in ('attempt_id','outcome','status','bytes','error')} for a in rows],indent=2))
