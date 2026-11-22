"""Structural checks plus optional anonymous URL access receipts; not human validation."""
from pathlib import Path
import re, json, hashlib, csv, sys
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor

BASE = Path(__file__).resolve().parents[1]
URL = re.compile(r'\]\((https?://[^\s)]+)\)')
required = {'source_id','original_url','pinned_url_or_version','publisher','published_or_event_date','checked_utc','locator','source_kind','verified_fact','limitation','question_ids','case_ids','duplicate_group','counted'}
sources = [json.loads(s) for s in (BASE/'sources.jsonl').read_text().splitlines() if s.strip()]
checks = []
arms = []
all_urls = []
for case in ('P02','P04','P06','N08'):
    p = BASE/'packets'/case
    files = {name:(p/name).read_text() for name in ('t0.md','arm-A.md','arm-B.md','arm-C.md','t1.md')}
    b,c = files['arm-B.md'],files['arm-C.md']
    ub,uc = URL.findall(b),URL.findall(c)
    c_without_explanations = '\n'.join(line for line in c.splitlines() if not line.startswith('   '))
    normalize = lambda s: '\n'.join(line.rstrip() for line in s.splitlines() if line.strip())
    record = {'case_id':case,'B_urls':ub,'C_urls':uc,'same_urls_order_versions':ub==uc,'count':len(ub),
              'max_three':len(ub)<=3,'B_unicode_chars':len(b),'C_unicode_chars':len(c),'added_unicode_chars':len(c)-len(b),
              'B_sha256':hashlib.sha256(b.encode()).hexdigest(),'C_sha256':hashlib.sha256(c.encode()).hexdigest(),
              'only_explanation_paragraphs_differ':normalize(b)==normalize(c_without_explanations),
              'A_has_no_curated_urls':len(URL.findall(files['arm-A.md']))==0,
              't0_t1_have_no_answer_urls':len(URL.findall(files['t0.md']+files['t1.md']))==0,
              'all_original_ids_in_t0_and_t1':all(f'{case}-R1' in files[x] and (f'{case}-R3' in files[x] or '~R3' in files[x]) for x in ('t0.md','t1.md'))}
    if case == 'P06':
        record['float_literals_preserved']='index1=2.0' in files['t0.md'] and 'index1=3.0' in files['t1.md']
    arms.append(record)
    all_urls.extend(ub)
    checks.append(all(record[k] for k in ('same_urls_order_versions','max_three','only_explanation_paragraphs_differ','A_has_no_curated_urls','t0_t1_have_no_answer_urls','all_original_ids_in_t0_and_t1')))

report={'kind':'MATERIAL_STRUCTURE_NOT_HUMAN_EFFECT','checked_utc':datetime.now(timezone.utc).isoformat(),
        'case_checks':arms,'participant_files':len(list((BASE/'packets').glob('*/*.md'))),
        'source_rows':len(sources),'unique_source_ids':len({r['source_id'] for r in sources}),
        'missing_source_keys':{r['source_id']:sorted(required-set(r)) for r in sources if required-set(r)},
        'counted_rows':sum(r['counted'] for r in sources),'counted_unique_groups':len({r['duplicate_group'] for r in sources if r['counted']}),
        'frame_rows':len(list(csv.DictReader((BASE/'frame.csv').open()))),
        'semantic_review':'evidence/semantic-review.json; structural equality cannot establish accurate explanation or absence of bias'}
report['structural_pass']=all(checks) and report['participant_files']==20 and not report['missing_source_keys'] and report['unique_source_ids']==report['source_rows']
(BASE/'evidence/material-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

if '--access' in sys.argv:
    def check(url):
        row={'requested_url':url,'checked_utc':datetime.now(timezone.utc).isoformat(),'mode':'anonymous HTTPS GET without credentials or session cookies','counted_as_new_source':False}
        try:
            with urlopen(Request(url,headers={'User-Agent':'AF-RES-038-public-access-check'}),timeout=25) as r:
                body=r.read()
                row.update(status=r.status,final_url=r.url,bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),body_retained=False)
        except Exception as exc:
            row.update(status='unverified',error=str(exc),next_action='같은 URL을 공개 브라우저에서 재시도하여 전 군 공통 접근을 확인한다.')
        return row
    with ThreadPoolExecutor(max_workers=4) as pool:
        access=list(pool.map(check,all_urls))
    (BASE/'evidence/public-access.json').write_text(json.dumps({'requests':access,'opened':sum(r['status']==200 for r in access),'denominator':len(access),'content_already_read_in_sources':True},ensure_ascii=False,indent=2)+'\n')
    report['anonymous_access_ok']=sum(r['status']==200 for r in access)
print(json.dumps({k:v for k,v in report.items() if k!='case_checks'},ensure_ascii=False))
if not report['structural_pass']:
    raise SystemExit(1)
