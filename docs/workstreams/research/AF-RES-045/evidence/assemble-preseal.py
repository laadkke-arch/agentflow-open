"""Assemble the pre-outcome seal from separately recorded research notes. No network."""
import csv,json
from pathlib import Path
B=Path(__file__).resolve().parent.parent
if (B/'outcomes.csv').exists():
 raise SystemExit('Refusing to overwrite a post-outcome ledger; reproduce the sealed commit in a separate checkout.')
R=json.loads((B/'evidence/root-preseal-data.json').read_text())
AUD=json.loads((B/'evidence/audacity-requests-final.json').read_text())
cases=AUD['cases'] if isinstance(AUD,dict) and 'cases' in AUD else AUD['requests'] if isinstance(AUD,dict) and 'requests' in AUD else AUD
requests=list(R['requests'])
for a in cases:
 d=dict(a)
 d['request_id']=d.pop('case_id')
 d['url']='https://github.com/audacity/audacity/issues/'+str(d['issue'])
 d['source_id']='AUD-R'+str(d['issue'])
 d['purpose']=d['author_stated_purpose']
 d['observable']=d['normal_observable']+'; '+d['boundary_observable']
 d['known_names_at_request']=d['known_name_at_request']
 d['body_revision']=d['first_body_status']
 d['checked_utc']=d['opened_at']
 d['prior_outcome_exposure']=d['prior_outcome_exposure']
 d['baseline_api']='Audacity2.3.3@008d8d8c8cb6f6fac9c95f72513f6b0bc98af1dc' if d['request_id']!='AUD03' else 'Audacity2.4.2@16d52f63a4183bba77ef7305d14622958dc0d1d5'
 d['new_choice_relative_request']={'AUD01':'GetTime is author proposal; existing Nyquist getter is contemporaneous API, not new donor-derived invention','AUD02':'RGB/contrast policies and test colors researcher-added; own-color goal already present; edited outcome exposure disclosed','AUD03':'Hard/soft mask and exact5bin toy kernel researcher-added; existing receiver has spectral processing; no donor authorship of DSP algorithm'}[d['request_id']]
 requests.append(d)
def csv_write(path,rows):
 heads=list(dict.fromkeys(k for r in rows for k in r))
 with path.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=heads,lineterminator='\n');w.writeheader()
  for r in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()})
csv_write(B/'requests.csv',requests)
records=list(R['root_sources'])
for file in ['audacity-initial-sources.jsonl','audacity-api-sources.jsonl','spatial-donor-sources.jsonl','temporal-donor-sources.jsonl']:
 records.extend(json.loads(x) for x in (B/'evidence'/file).read_text().splitlines() if x.strip())
def norm(r):
 d=dict(r)
 d['edition_id']=r.get('edition_id',r.get('edition','미확인'))
 d['url']=r.get('url',r.get('source_url'))
 d['checked_utc']=r.get('checked_utc',r.get('accessed_utc'))
 d['exact_locator']=r.get('exact_locator',r.get('locator',r.get('location','미확인')))
 d['publication_date']=r.get('publication_date',r.get('published_at'))
 d['changed_date']=r.get('changed_date',r.get('updated_date',r.get('modified_at')))
 d['questions']=r.get('questions',r.get('question_ids',[]))
 d['case_ids']=r.get('case_ids',r.get('cases',[]))
 if not d.get('allocation') and r.get('minimum_allocation'):
  d['allocation']='donor_temporal' if r['minimum_allocation']=='donor' else r['minimum_allocation']
 d.setdefault('minimum_count',False);d.setdefault('allocation',None)
 d.setdefault('duplicate_of',None)
 if d['source_id'].startswith('MPL-API-'):
  d['checked_utc']='2026-11-22T22:07:46Z'
  d['timestamp_semantics']='Observed UTC after direct opening and relevant-section re-read batch; not inferred publication time.'
 return d
records=[norm(r) for r in records]
byid={r['source_id']:r for r in records}
for p in R['predictions']:
 ids=p['donor_source_ids'].split(';')
 p['donor_urls']='; '.join(byid[s]['url'] for s in ids)
 p['donor_locators']='; '.join(s+': '+byid[s]['exact_locator'] for s in ids)
 p['sealed_input_version']='pre-outcome root-preseal-data + audacity-requests-final'
csv_write(B/'predictions.csv',R['predictions'])
assert len({r['source_id'] for r in records})==len(records)
seen=set()
for r in records:
 if r['minimum_count']:
  assert r['work_id'] not in seen,r['work_id']
  seen.add(r['work_id'])
(B/'sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
m=list(csv.DictReader((B/'evidence/matplotlib-frame.csv').open()))
a=list(csv.DictReader((B/'audacity-frame.csv').open()))
frame=[]
for r in m:
 n=int(r['exposure_rank'])
 frame.append(dict(frame_id='MPL-F'+str(n).zfill(2),repository=r['repository'],exposure_rank=n,issue_number=r['issue_number'],title=r['title'],created_at=r['created_at'],updated_at=r['updated_at'],url=r['url'],body_opened=n<=5,selected=bool(r['request_id']),request_id=r['request_id'],screening_reason=r['reason'],initial_body_revision=r['initial_body_revision'],prior_outcome_exposure='none observed; resolution metadata masked',search_url=next(x['url'] for x in records if x['source_id']=='MPL-SEARCH'),checked_utc=r['checked_utc']))
for r in a:
 frame.append(dict(frame_id=r['frame_id'],repository=r['repository'],exposure_rank=r['rank'],issue_number=r['issue_number'],title=r['title'],created_at=r['created_at'],updated_at=r['updated_at'],url=r['url'],body_opened=r['body_opened'],selected=r['selected'],request_id=r['case_id'],screening_reason=r['reason'],initial_body_revision=r['first_body_version'],prior_outcome_exposure=r['pre_outcome_exposure'],search_url=r['search_url'],checked_utc=r['search_opened_at']))
csv_write(B/'frame.csv',frame)
assert len(requests)==6 and len(R['predictions'])==12 and len(frame)==60
print(json.dumps({'requests':6,'predictions':12,'frame':60,'source_records':len(records),'unique_counted_works':len(seen),'allocations':{c:sum(x['minimum_count'] and x['allocation']==c for x in records) for c in sorted({x['allocation'] for x in records if x['allocation']})}},ensure_ascii=False))
