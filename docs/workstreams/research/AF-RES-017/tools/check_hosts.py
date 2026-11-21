"""One anonymous HEAD per newly encountered host; no body storage or retry."""
import json, urllib.request, urllib.error, urllib.parse, concurrent.futures, datetime
from pathlib import Path
P=Path(__file__).resolve().parents[1]
checked=set('github.com api.github.com raw.githubusercontent.com www.bmj.com pmc.ncbi.nlm.nih.gov www.uspto.gov dl.acm.org www.nber.org martinfowler.com netflixtechblog.com aws.amazon.com'.split())
checked.update(x['host'] for x in json.loads((P/'evidence/methods/NETWORK.json').read_text()))
target={}
for f in [P/'sources.json',P/'evidence/methods/sources.json']:
    for x in json.loads(f.read_text())['sources']:
        u=x['url'];h=urllib.parse.urlparse(u).netloc
        if h and h not in checked:target.setdefault(h,u)
out=P/'evidence/network-followup.json'
if out.exists():raise SystemExit('Already executed: do not retry blocked hosts or overwrite observations.')
def probe(item):
    h,u=item;r={'host':h,'url':u,'accessed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'request':'anonymous HEAD, one attempt, no body storage','level':'D3-fetch','timing_note':'Newly encountered source host; after scope commit, not falsely backdated as preregistration.'}
    try:
        with urllib.request.urlopen(urllib.request.Request(u,method='HEAD'),timeout=8) as res:r.update(status=res.status,final_url=res.geturl())
    except urllib.error.HTTPError as e:r.update(status=e.code,error=str(e))
    except Exception as e:r.update(status=None,error=type(e).__name__+': '+str(e))
    return r
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:results=list(ex.map(probe,sorted(target.items())))
out.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'hosts':len(results),'responses':[{k:r.get(k) for k in ['host','status','error']} for r in results]},ensure_ascii=False))
