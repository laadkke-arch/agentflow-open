"""Integrate resume provenance while preserving the completed experiment scope.

Uses the before-resume snapshot only. No raw record, packet, decision or completed
experimental cost-summary changes. Additional sources receive no minimum credit.
"""
import collections,copy,csv,datetime,hashlib,io,json
from pathlib import Path

HERE=Path(__file__).resolve().parent
P=HERE.parents[1]
BEFORE=HERE/'before-resume'
def jl(path):return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
def js(path):return json.loads(path.read_text())
def h(b):return hashlib.sha256(b).hexdigest()
def textj(d):return json.dumps(d,ensure_ascii=False,indent=2)+'\n'
def textl(rs):return ''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rs)
def csvtext(rs):
    f=io.StringIO(newline='');ks=list(dict.fromkeys(k for r in rs for k in r))
    w=csv.DictWriter(f,ks,lineterminator='\n');w.writeheader();w.writerows(rs);return f.getvalue()
def getstats(rs):
    gs=[a for a in rs if a.get('operation')=='GET']
    return {'actual_get_operations':len(gs),'minimum_http_exchanges':sum(1+len(a.get('redirect_chain',[])) for a in gs),
      'failed_GETs':sum(bool(a.get('error')) or (a.get('status') is not None and a['status']>=400) for a in gs),
      'received_final_body_bytes':sum(a.get('received_body_bytes') or 0 for a in gs),
      'temporary_full_body_stored_bytes':sum(a.get('stored_bytes') or 0 for a in gs),
      'sum_request_elapsed_seconds':round(sum(a.get('elapsed_seconds') or 0 for a in gs),6)}

sources=jl(BEFORE/'sources.jsonl');old_sources=copy.deepcopy(sources)
byid={r['source_id']:r for r in sources};aliases=js(BEFORE/'evidence/source-aliases.json')
attempts=jl(BEFORE/'attempts.jsonl');costs=list(csv.DictReader((BEFORE/'costs.csv').open()))
sourcecount=js(BEFORE/'evidence/source-counts.json')
sealed={n:h((P/n).read_bytes()) for n in ['references.jsonl','components.jsonl','packets.jsonl','decisions.csv','reading-plan.json']}
original_summary_hash=h((P/'evidence/cost-summary.json').read_bytes())
mapping={'RS-01':'BIO-N01','RS-02':'BIO-H01','RS-03':'G-N01','RS-04':'G-N01',
  'RS-05':'GNU-P-NEWROOT','RS-06':'BIO-N03-LANDING','RS-07':'BIO-N03-SOURCE','RS-08':'G-N05','RS-09':'G-H03'}
new_source_records=[]
for raw_path,collector in [('review/resume-sources/sources.jsonl','resume_sources'),('review/resume-cross-costs/sources.jsonl','resume_cross_costs')]:
    for raw in jl(P/raw_path):
        sid=raw['source_id'];target=mapping.get(sid,raw.get('existing_source_id'))
        assert target in byid,(sid,target)
        row=byid[target]
        variant={'source_id':sid,'collector':collector,'phase':'resume_audit',
          'url':raw.get('original_url'),'fixed_url':raw.get('fixed_url'),
          'version':raw.get('version'),'publication_date':raw.get('publication_date'),
          'checked_utc':raw.get('checked_utc',raw.get('receipt_recorded_utc')),
          'read_location':raw.get('read_location'),'findings':raw.get('findings',raw.get('read_status')),
          'limitations':raw.get('limitations'),'raw_record_path':raw_path,'raw_record':raw,
          'canonical_grouping_note':'Post-seal targeted audit/reread; existing manuscript only; additional minimum credit 0; failed tool attempts remain failed.'}
        row['variants'].append(variant);row['source_aliases'].append(sid)
        row['questions']=sorted(set(row['questions']+raw.get('questions',[])))
        row['case_ids']=sorted(set(row['case_ids']+raw.get('case_ids',[])))
        aliases[sid]=target;new_source_records.append({'source_id':sid,'canonical_source_id':target,'additional_minimum_credit':0})

# Correct an inaccurate section name in the current canonical locator only.
# The original collector record and original variant are deliberately preserved.
ons=byid['CX-G02'];prior_location=ons['read_location']
ons['read_location']='Section 1, Overview of main changes; web lines 87–90 (318 local authorities, boundaries as of 1 April 2023)'
ons['read_location_correction']={'previous':prior_location,'current':ons['read_location'],
  'reason':'Resume direct reread found the section title is Overview of main changes, not Main points/About this release.',
  'supporting_source_alias':'RCC-CX-G02','supporting_attempt_ids':['RCC-OPEN-07','RCC-FIND-04','RCC-FIND-06'],
  'original_raw_and_variant_preserved':True}

new_attempts=[]
for name,collector in [('review/resume-sources/attempts.jsonl','resume_sources'),
  ('review/resume-sources/unmetered-attempts.jsonl','resume_sources'),
  ('review/resume-cross-costs/attempts.jsonl','resume_cross_costs')]:
    new_attempts.extend({'collector':collector,**a,'phase':'resume_audit','raw_record_path':name} for a in jl(P/name))
root=js(P/'evidence/resume-web-reads.json')
for i,a in enumerate(root['reads'],1):
    aid=f'ROOT-RESUME-WEB-{i:02}'
    new_attempts.append({'attempt_id':aid,'collector':'resume_root','phase':'resume_audit','operation':'web_open',
      'url':a['url'],'source_id':a['source_alias'],'source_alias':a['source_alias'],
      'result':a['outcome'],'read_location':a.get('read_location'),'findings':a.get('finding'),
      'limitations':a.get('limit',a.get('next_path')),'checked_utc_window':root['checked_utc_window'],
      'measurement':'actual logical web open; request UTC, transport/cache exchanges, bytes and elapsed unmeasured',
      'received_body_bytes':None,'stored_bytes':None,'elapsed_seconds':None,
      'raw_record_path':'evidence/resume-web-reads.json','raw_record_index':i-1})
assert len(new_attempts)==35
attempts.extend(new_attempts)
assert len(attempts)==len({a['attempt_id'] for a in attempts})
for a in new_attempts:
    measured=a.get('operation')=='GET'
    cost={'cost_id':a['attempt_id'],'ref_ids':'|'.join(a.get('case_ids',[])),
      'collector':a['collector'],'phase':'resume_audit','round':'resume_audit',
      'configuration':a.get('role',a['operation']),'url':a.get('url'),
      'actual_requests':1 if measured else '',
      'logical_tool_actions':1,'http_exchanges_minimum':1+len(a.get('redirect_chain',[])) if measured else '',
      'transport_failures':int(bool(a.get('error')) or (a.get('status') is not None and a['status']>=400)) if measured else '',
      'status':a.get('status'),'received_body_bytes':a.get('received_body_bytes') if measured else '',
      'temporary_stored_bytes':a.get('stored_bytes') if measured else '',
      'durable_stored_bytes':'excerpt/provenance only; full-body byte count is not durable evidence size',
      'elapsed_seconds':a.get('elapsed_seconds') if measured else '',
      'measurement':a.get('measurement'),'started_utc':a.get('started_utc'),
      'finished_utc':a.get('finished_utc',a.get('logged_utc',a.get('receipt_recorded_utc'))),
      'result':a.get('result',a.get('error')),'unmeasured':'wire/header/cache transport; human/model reading; service cost; unmetered tool body/elapsed'}
    costs.append(cost)
gs=getstats(new_attempts)
unmetered=[a for a in new_attempts if a['operation']!='GET']
summary={'phase':'resume_audit','scope':'Targeted post-seal source/Q7/root rereads only; separate from completed216GET experiment',
  'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'measured_GET_scope':gs,
  'unmetered_logical_actions':{'total':len(unmetered),'web_actions':24,'local_failed_setup_actions':1,
    'web_failure_attempt_ids':['RS-WEB-01','RS-WEB-02','RS-WEB-03','RS-WEB-04','RCC-OPEN-05','RCC-OPEN-06','ROOT-RESUME-WEB-01','ROOT-RESUME-WEB-02'],
    'find_no_exact_match_attempt_ids':['RCC-FIND-05','RCC-FIND-07'],
    'counts_are_not_HTTP_requests':True,'bytes_elapsed_transport':'unmeasured'},
  'completed_experiment_summary_preserved':'evidence/cost-summary.json',
  'combined_measured_GET_scope':getstats(attempts),
  'total_attempt_rows':len(attempts),'resume_attempt_rows':len(new_attempts),
  'reread_source_aliases':new_source_records,'additional_minimum_credit':0,
  'limits':['Do not add unmetered web opens/finds to measured GET or HTTP exchange counts.',
    'Zero full-body stored bytes for resume GET means no full raw response retained; excerpt/provenance storage is separate.',
    'Summed request elapsed is not wall time, reader labor, token cost or service cost.',
    'Second visit in replay-costs.csv remains a simulation; these audits did not execute its C1/C2 task.']}
sourcecount['raw_source_records']+=len(new_source_records)
sourcecount['resume_audit_source_records']=len(new_source_records)
sourcecount['resume_audit_added_minimum_credit']=0
sourcecount['attempt_rows']=len(attempts)
sourcecount['duplicate_groups_merged']={s['source_id']:s['source_aliases'] for s in sources if len(s['source_aliases'])>1}
out={'sources.jsonl':textl(sources),'attempts.jsonl':textl(attempts),'costs.csv':csvtext(costs),
  'evidence/source-aliases.json':textj(aliases),'evidence/source-counts.json':textj(sourcecount),
  'evidence/resume-cost-summary.json':textj(summary)}
checks={'canonical_rows_remain81':len(sources)==81,'eligible_minimum_remains50':sum(s['count_minimum'] for s in sources)==50,
  'eighteen_reread_aliases_added':len(new_source_records)==18 and len(aliases)==144,
  'all_previous_variants_preserved':all(byid[s['source_id']]['variants'][:len(s['variants'])]==s['variants'] for s in old_sources),
  'all35_attempts_added':len(attempts)==301 and len(new_attempts)==35,
  'all303_cost_rows':len(costs)==303,
  'sealed_bytes_preserved':sealed=={n:h((P/n).read_bytes()) for n in sealed},
  'completed216_summary_preserved':h((P/'evidence/cost-summary.json').read_bytes())==original_summary_hash,
  'all_source_id_refs_join':all(a.get('source_id') is None or a['source_id'] in aliases for a in new_attempts)}
assert all(checks.values()),checks
for n,s in out.items():(P/n).write_text(s)
receipt={'checks':checks,'output_sha256':{n:h(s.encode()) for n,s in out.items()},
  'sealed_sha256':sealed,'completed_cost_summary_sha256':original_summary_hash,
  'summary':summary,'CX_G02_correction':ons['read_location_correction']}
(HERE/'resume-integration-applied.json').write_text(textj(receipt))
print(json.dumps({'checks':checks,'measured_resume':gs,'all_measured_GET':summary['combined_measured_GET_scope']},ensure_ascii=False))
