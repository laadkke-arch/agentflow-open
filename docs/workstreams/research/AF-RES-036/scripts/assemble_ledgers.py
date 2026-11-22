"""Join source aliases, fetch attempts and measured cost units conservatively."""
import collections,csv,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def readl(path):return [json.loads(x) for x in path.read_text().splitlines() if x.strip()] if path.exists() else []
def writej(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def writel(path,rows):path.write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows))
catmap={'consumer':'original_consumer','original_consumer':'original_consumer','current':'current_destination','current_destination':'current_destination','historical':'independent_historical','independent_historical':'independent_historical','other_primary':'other_primary','cross_field_supplement':'cross_field_supplement'}
groups={};alias={};raw_sources=[];attempts=[]
for collector in ('gnu','bioc','cross','root'):
    directory=P/'collectors'/collector
    for raw in readl(directory/'sources.jsonl'):
        raw_sources.append({'collector':collector,**raw})
        sid=raw['source_id'];group=raw.get('duplicate_group',sid)
        counted=raw.get('count_minimum',raw.get('count_toward_minimum',False))
        cats=raw.get('count_categories',raw.get('minimum_categories',raw.get('minimum_category',[]))) or []
        if isinstance(cats,str):cats=[cats]
        cats=[catmap.get(v,v) for v in cats] if counted else []
        variant={'source_id':sid,'collector':collector,'url':raw.get('original_url',raw.get('url')),'fixed_url':raw.get('fixed_version_url',raw.get('fixed_url')),'version':raw.get('version',raw.get('edition')),'publication_date':raw.get('publication_date',raw.get('published_date')),'checked_utc':raw.get('checked_utc'),'read_location':raw.get('read_location',raw.get('location')),'findings':raw.get('findings',raw.get('confirmed',raw.get('verified_content'))),'limitations':raw.get('limitations',raw.get('limits')),'raw_record_path':str((directory/'sources.jsonl').relative_to(P)),'raw_record':raw}
        if group not in groups:
            groups[group]={'source_id':sid,'source_aliases':[],'duplicate_group':group,'kind':raw.get('source_type',raw.get('kind')),'publisher':raw.get('publisher'),'original_url':variant['url'],'fixed_url':variant['fixed_url'],'publication_date':variant['publication_date'],'version':variant['version'],'checked_utc':variant['checked_utc'],'read_location':variant['read_location'],'findings':variant['findings'],'limitations':variant['limitations'],'questions':[],'case_ids':[],'count_minimum':False,'count_categories':[],'variants':[]}
        dst=groups[group];dst['source_aliases'].append(sid);dst['variants'].append(variant)
        dst['count_minimum']|=bool(counted)
        dst['count_categories']=sorted(set(dst['count_categories']+cats))
        supports=raw.get('supports',[])
        dst['questions']=sorted(set(dst['questions']+raw.get('question_ids',raw.get('questions',[]))+[s for s in supports if s.startswith('Q')]))
        dst['case_ids']=sorted(set(dst['case_ids']+raw.get('case_ids',[])+[s for s in supports if s.startswith(('G0','R0'))]))
        alias[sid]=dst['source_id']
    for raw in readl(directory/'attempts.jsonl'):
        attempts.append({'collector':collector,**raw})
attempts += [{'collector':'root',**r} for r in readl(P/'evidence/root-attempts.jsonl')]
seen=set()
for a in attempts:
    key=a.get('attempt_id')
    assert key and key not in seen,('attempt duplicate/missing',key)
    seen.add(key)
sources=list(groups.values());writel(P/'sources.jsonl',sources);writel(P/'attempts.jsonl',attempts)
writej(P/'evidence/source-aliases.json',alias)
counts={'raw_source_records':len(raw_sources),'unique_manuscript_rows':len(sources),'unique_eligible_sources':sum(s['count_minimum'] for s in sources),'categories':dict(collections.Counter(c for s in sources if s['count_minimum'] for c in s['count_categories'])),'duplicate_groups_merged':{s['source_id']:s['source_aliases'] for s in sources if len(s['source_aliases'])>1},'attempt_rows':len(attempts)}
writej(P/'evidence/source-counts.json',counts)

costs=[]
known_uses=collections.defaultdict(set)
for r in readl(P/'references.jsonl'):
    known_uses[r['fetch_attempt_id']].add(r['ref_id'])
for c in readl(P/'components.jsonl'):
    known_uses[c['N']['original_get_attempt_id']].add(c['ref_id'])
    for aid in c['N'].get('extra_fetch_attempt_ids',[]):known_uses[aid].add(c['ref_id'])
for a in attempts:
    if a.get('operation')!='GET':continue
    status=a.get('status');err=a.get('error');body=a.get('received_body_bytes')
    redirect=len(a.get('redirect_chain',[]))
    uses=sorted(set(a.get('case_ids',[]))|known_uses[a['attempt_id']])
    costs.append({'cost_id':a['attempt_id'],'ref_ids':'|'.join(uses),'collector':a['collector'],'round':1,'configuration':a.get('role','external_read'),'url':a.get('url'),'actual_requests':1,'http_exchanges_minimum':1+redirect,'transport_failures':int(bool(err) or (status is not None and status>=400)),'empty_success_body':int(status is not None and 200<=status<300 and body==0),'status':status,'received_body_bytes':body,'temporary_stored_bytes':a.get('stored_bytes'),'durable_stored_bytes':'not_equals_temporary; see retention','elapsed_seconds':a.get('elapsed_seconds'),'same_archive_reuse':0,'logical_uses':len(uses),'measurement':'actual final response body and request tool elapsed','started_utc':a.get('started_utc'),'finished_utc':a.get('finished_utc'),'unmeasured':'wire/header/intermediate redirect body bytes; human/model reading; service operating cost'})
bioc=P/'collectors/bioc/costs.csv'
if bioc.exists():
    for r in csv.DictReader(bioc.open()):
        if r.get('same_archive_reuse')=='1':
            costs.append({'cost_id':r['cost_id'],'ref_ids':r['ref_ids'],'collector':'bioc','round':1,'configuration':'H archive reuse','url':r['url'],'actual_requests':0,'http_exchanges_minimum':0,'transport_failures':0,'empty_success_body':0,'status':None,'received_body_bytes':0,'temporary_stored_bytes':int(r['stored_bytes']),'durable_stored_bytes':'excerpt only','elapsed_seconds':None,'same_archive_reuse':1,'logical_uses':1,'measurement':'actual existing archive reuse; member read timing unmeasured','started_utc':None,'finished_utc':r['finished_utc'],'unmeasured':r['unmeasured']})
keys=list(dict.fromkeys(k for c in costs for k in c))
with (P/'costs.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,keys,lineterminator='\n');w.writeheader();w.writerows(costs)
summary={'actual_get_operations':sum(r['actual_requests'] for r in costs),'minimum_http_exchanges':sum(r['http_exchanges_minimum'] for r in costs),'transport_failures':sum(r['transport_failures'] for r in costs),'empty_2xx_bodies':sum(r['empty_success_body'] for r in costs),'received_final_body_bytes':sum(r['received_body_bytes'] or 0 for r in costs),'temporary_fetch_stored_bytes':sum(r['temporary_stored_bytes'] or 0 for r in costs if r['actual_requests']),'sum_request_elapsed_seconds':round(sum(r['elapsed_seconds'] or 0 for r in costs),6),'archive_reuse_events':sum(r['same_archive_reuse'] for r in costs),'elapsed_is_not_wall_or_human_time':True,'wire_bytes_measured':False,'second_visit_executed':False}
writej(P/'evidence/cost-summary.json',summary)
print(json.dumps({'sources':counts,'costs':summary},ensure_ascii=False))
