"""Append omitted post-decision adjudication provenance without changing frozen inputs.

Default writes a dry-run preview under this directory. --apply changes the six
explicitly authorized derived ledgers. The historical inputs remain in before/.
No network, reader replay, raw source edits or changes to packet/decision bytes.
"""
from __future__ import annotations
import argparse, collections, copy, csv, hashlib, io, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = HERE.parents[1]
FILES = ['sources.jsonl', 'attempts.jsonl', 'costs.csv',
         'evidence/source-aliases.json', 'evidence/source-counts.json',
         'evidence/cost-summary.json']
SEALED = ['references.jsonl','components.jsonl','packets.jsonl','decisions.csv',
          'reading-plan.json']

def sha(b): return hashlib.sha256(b).hexdigest()
def jl(path): return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]
def js(path): return json.loads(path.read_text())
def dumpj(x): return json.dumps(x, ensure_ascii=False, indent=2)+'\n'
def dumpl(x): return ''.join(json.dumps(r, ensure_ascii=False, sort_keys=True)+'\n' for r in x)
def csvtext(rows):
    f=io.StringIO(newline=''); keys=list(dict.fromkeys(k for r in rows for k in r))
    w=csv.DictWriter(f,keys,lineterminator='\n');w.writeheader();w.writerows(rows)
    return f.getvalue()
def get_stats(rows):
    gs=[x for x in rows if x.get('operation')=='GET']
    return {'actual_get_operations':len(gs),
      'minimum_http_exchanges':sum(1+len(x.get('redirect_chain',[])) for x in gs),
      'transport_failures':sum(bool(x.get('error')) or (x.get('status') is not None and x['status']>=400) for x in gs),
      'empty_2xx_bodies':sum(x.get('status') is not None and 200<=x['status']<300 and x.get('received_body_bytes')==0 for x in gs),
      'received_final_body_bytes':sum(x.get('received_body_bytes') or 0 for x in gs),
      'temporary_fetch_stored_bytes':sum(x.get('stored_bytes') or 0 for x in gs),
      'sum_request_elapsed_seconds':round(sum(x.get('elapsed_seconds') or 0 for x in gs),6)}

# Each mapping is a manuscript/section relationship, not an assertion that two
# complete HTTP bodies are byte identical. Raw hashes remain in each variant.
MAP = {**{f'GNU-C-G{i:02}':f'G-B{i:02}' for i in range(1,7)},
 **{f'GNU-P-{s}':'G-N01' for s in ['ROOT','MAIN','XCU','INTRO','SHELL','PREFACE']},
 **{f'GNU-P-{s}':'GNU-P-NEWROOT' for s in ['NEWROOT','NEWMAIN','NEWSHELL']},
 'GNU-BC-ROOT':'G-N02', 'GNU-BC-README':'G-N02',
 'GNU-GW-CURRENT':'G-N04','GNU-GW-INDEX':'G-N04','GNU-GW-PRESERVED':'G-B03',
 'GNU-GW-MANUAL-DATE':'G-N04','GNU-GCC-CURRENT':'G-N05','GNU-GCC-10_1':'G-H03',
 'GNU-GT-DIR':'G-N06',
 **{f'BC-consumer-R{i:02}':f'BIO-B{i:02}' for i in range(1,6)},
 'BC-original-R01':'BIO-N01','BC-original-R02':'BIO-N02',
 'BC-original-R03':'BIO-N03-LANDING','BC-original-R04':'BIO-L02',
 'BC-original-R05':'BIO-N05-LANDING','BC-original-R06':'BIO-N06',
 'BC-release311':'BC-release311','BC-deseq311-vignette':'BIO-B01',
 'BC-sce311-intro':'BIO-B06','BC-scater311-overview':'BIO-B05',
 'BC-rnaseq311-vignette':'BIO-H01','BC-rnaseq311-source':'BIO-H01',
 'BC-s4-current-source':'BIO-N03-SOURCE','BC-s4311-source':'BIO-N03-SOURCE',
 'BC-s4-manual-current':'BIO-N03-MANUAL'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--apply',action='store_true');args=ap.parse_args()
    old={f:(HERE/'before'/f).read_bytes() for f in FILES}
    sealed_before={f:sha((P/f).read_bytes()) for f in SEALED}
    sources=jl(HERE/'before/sources.jsonl')
    old_sources=copy.deepcopy(sources)
    byid={r['source_id']:r for r in sources}
    aliases=js(HERE/'before/evidence/source-aliases.json')
    attempts=jl(HERE/'before/attempts.jsonl')
    old_costs=list(csv.DictReader(io.StringIO(old['costs.csv'].decode())))
    raw_records=[]; new_attempts=[]; mappings=[]
    for group in ['gnu','bioc']:
        raw_path=f'adjudicators/{group}/sources.jsonl'
        for raw in jl(P/raw_path):
            sid=raw['source_id'];raw_records.append(raw)
            target=MAP.get(sid,sid)
            date=raw.get('publication_date',raw.get('published_dates'))
            location=raw.get('read_section',raw.get('directly_read_sections'))
            observed=raw.get('content_observed',raw.get('content_observation'))
            is_new=target not in byid
            note=('Supplementary post-decision manuscript record; not counted toward minimum. '
                  'All original excerpts/hashes retained; no claim of independent gold.') if is_new else (
                  'Post-decision reread or additional section of established manuscript. '
                  'Canonical grouping does not assert whole-response byte equality.')
            if sid=='BC-consumer-R04':
                note += ' Compound archive includes devel.html (BIO-B04) and intro.html (BIO-B06); alias uses BIO-B04 as carrier, and also_covers_source_ids records BIO-B06.'
            if is_new:
                row={'source_id':target,'source_aliases':[],
                  'duplicate_group':'criterion-supplement:'+target,'kind':'post_decision_primary_or_attempt_record',
                  'publisher':raw.get('publisher'),'original_url':raw.get('url',raw.get('original_request_url')),
                  'fixed_url':raw.get('fixed_url'),'publication_date':date,'version':raw.get('edition'),
                  'checked_utc':raw.get('retrieved_utc'),'read_location':location,
                  'findings':observed,'limitations':raw.get('limitations'),
                  'questions':['Q4'],'case_ids':raw.get('case_ids',[]),
                  'count_minimum':False,'count_categories':[],'variants':[],
                  'supplement_not_counted_reason':note}
                sources.append(row);byid[target]=row
            row=byid[target]
            variant={'source_id':sid,'collector':'adjudicator_'+group,
              'url':raw.get('url',raw.get('original_request_url')),'fixed_url':raw.get('fixed_url'),
              'version':raw.get('edition'),'publication_date':date,
              'checked_utc':raw.get('retrieved_utc'),'read_location':location,
              'findings':observed,'limitations':raw.get('limitations'),
              'raw_record_path':raw_path,'raw_record':raw,'canonical_grouping_note':note}
            if sid=='BC-consumer-R04':variant['also_covers_source_ids']=['BIO-B06']
            row['variants'].append(variant)
            row['source_aliases'].append(sid)
            row['case_ids']=sorted(set(row['case_ids']+raw.get('case_ids',[])))
            row['questions']=sorted(set(row['questions']+['Q4']))
            aliases[sid]=target
            mappings.append({'source_id':sid,'canonical_source_id':target,
              'new_row':is_new,'additional_minimum_credit':0,'reason':note})
        new_attempts += [{'collector':'adjudicator_'+group,**x} for x in jl(P/f'adjudicators/{group}/attempts.jsonl')]
    attempts+=new_attempts
    assert len(attempts)==len({x['attempt_id'] for x in attempts}), 'duplicate attempt IDs'
    cost_actual=[r for r in old_costs if r.get('round')=='1']
    sim=[r for r in old_costs if r.get('round')!='1']
    for a in new_attempts:
        if a.get('operation')!='GET':continue
        status=a.get('status'); body=a.get('received_body_bytes')
        cost_actual.append({'cost_id':a['attempt_id'],'ref_ids':'|'.join(sorted(set(a.get('case_ids',[])))),
          'collector':a['collector'],'round':1,'configuration':a.get('role','criterion_check'),
          'url':a.get('url'),'actual_requests':1,'http_exchanges_minimum':1+len(a.get('redirect_chain',[])),
          'transport_failures':int(bool(a.get('error')) or (status is not None and status>=400)),
          'empty_success_body':int(status is not None and 200<=status<300 and body==0),
          'status':status,'received_body_bytes':body,'temporary_stored_bytes':a.get('stored_bytes'),
          'durable_stored_bytes':'not_equals_temporary; excerpt/provenance retained',
          'elapsed_seconds':a.get('elapsed_seconds'),'same_archive_reuse':0,
          'logical_uses':len(set(a.get('case_ids',[]))),
          'measurement':'actual final response body and request tool elapsed; post-decision criterion',
          'started_utc':a.get('started_utc'),'finished_utc':a.get('finished_utc'),
          'unmeasured':'wire/header/intermediate redirect body bytes; human/model reading; service operating cost'})
    prior=collections.defaultdict(list)
    for row in sorted(cost_actual,key=lambda r:r.get('started_utc') or r.get('finished_utc') or ''):
        if int(row.get('actual_requests') or 0)==0:continue
        seen=prior[row['url']]
        row['exact_url_request_ordinal']=len(seen)+1
        row['previous_failed_same_url']=bool(seen and int(seen[-1]['transport_failures']))
        row['repeat_kind']='retry_after_failure' if row['previous_failed_same_url'] else ('new_observation_same_url' if seen else 'first_measured_url_request')
        seen.append(row)
    old_count=js(HERE/'before/evidence/source-counts.json')
    counts=copy.deepcopy(old_count)
    counts.update({'raw_source_records':old_count['raw_source_records']+len(raw_records),
      'unique_manuscript_rows':len(sources),
      'unique_manuscript_rows_definition':'Canonical ledger rows include noncounted supplementary manuscripts, compound artifact metadata and failed/search records; 50 is the established eligible lower bound.',
      'attempt_rows':len(attempts),'collection_only_scope':old_count,
      'post_decision_adjudicator_source_records':len(raw_records),
      'post_decision_added_minimum_credit':0,
      'eligible_minimum_basis':'Preserved 50 eligible collection-stage manuscripts; added adjudicator records are aliases or explicitly not counted.'})
    counts['duplicate_groups_merged']={s['source_id']:s['source_aliases'] for s in sources if len(s['source_aliases'])>1}
    cost_summary=js(HERE/'before/evidence/cost-summary.json')
    old_summary=copy.deepcopy(cost_summary)
    cost_summary.update(get_stats(attempts))
    cost_summary.update({'scope':'collection plus post-decision adjudication requests; excludes later resume audit requests',
      'collection_only_scope':old_summary,'post_decision_adjudication_scope':get_stats(new_attempts),
      'same_url_additional_gets':sum(max(0,len(v)-1) for v in prior.values()),
      'retry_after_failed_same_url':sum(bool(r.get('previous_failed_same_url')) for r in cost_actual),
      'raw_attempt_rows':len(attempts), 'post_decision_raw_attempt_rows':len(new_attempts)})
    output={'sources.jsonl':dumpl(sources),'attempts.jsonl':dumpl(attempts),
      'costs.csv':csvtext(cost_actual+sim),'evidence/source-aliases.json':dumpj(aliases),
      'evidence/source-counts.json':dumpj(counts),'evidence/cost-summary.json':dumpj(cost_summary)}
    # Fixed original facts, excerpts, categories and variants are retained; only
    # relationships/questions and new adjudicator variants are added.
    invariant_fields=['source_id','duplicate_group','count_minimum','count_categories',
      'kind','publisher','original_url','fixed_url','publication_date','version',
      'checked_utc','read_location','findings','limitations']
    checks={'eligible_count_remains_50':sum(s['count_minimum'] for s in sources)==50,
      'original_canonical_fields_preserved':all(all(byid[r['source_id']][k]==r[k] for k in invariant_fields) for r in old_sources),
      'original_variants_preserved':all(byid[r['source_id']]['variants'][:len(r['variants'])]==r['variants'] for r in old_sources),
      'all_64_adjudicator_aliases_resolve':len(raw_records)==64 and all(r['source_id'] in aliases for r in raw_records),
      'all_64_adjudicator_attempts_join':len(new_attempts)==64 and all(a['attempt_id'] in {x['attempt_id'] for x in attempts} for a in new_attempts),
      'all_GETs_have_one_cost_row':len([x for x in attempts if x.get('operation')=='GET'])==len([r for r in cost_actual if int(r.get('actual_requests') or 0)==1]),
      'sealed_bytes_unchanged':sealed_before=={f:sha((P/f).read_bytes()) for f in SEALED}}
    assert all(checks.values()),checks
    receipt={'basis_commit':'f403243dbf5f097536a1fd9fda55dfce4382329a','apply':args.apply,
      'checks':checks,'source_mappings':mappings,'summary':cost_summary,
      'before_hashes':{f:sha(v) for f,v in old.items()},
      'after_hashes':{f:sha(v.encode()) for f,v in output.items()},'sealed_hashes':sealed_before,
      'new_canonical_rows':len(sources)-len(old_sources)}
    for path,body in output.items():
        dest=HERE/'preview'/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(body)
        if args.apply:(P/path).write_text(body)
    (HERE/('integration-applied.json' if args.apply else 'integration-dry-run.json')).write_text(dumpj(receipt))
    print(json.dumps({'apply':args.apply,'checks':checks,'new_canonical_rows':receipt['new_canonical_rows'],
      'source_rows':len(sources),'source_aliases':len(aliases),'attempt_rows':len(attempts),
      'all_GET':cost_summary['actual_get_operations'],'all_bytes':cost_summary['received_final_body_bytes']},ensure_ascii=False))

if __name__=='__main__':main()
