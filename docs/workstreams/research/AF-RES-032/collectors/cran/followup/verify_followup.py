"""Meaningful integrity and date checks for R evidence; does not execute downloaded code."""
from pathlib import Path
import csv, datetime as dt, hashlib, json, subprocess, tarfile
from collections import Counter

P=Path(__file__).resolve().parent
B=P.parent
def digest(b): return hashlib.sha256(b).hexdigest()
def jl(p): return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
def j(p): return json.loads((P/p).read_text())
checks=[]
def check(condition,met,evidence,note=''):
    checks.append(dict(condition=condition,met=bool(met),evidence=evidence,note=note))
original=B/'final/references.jsonl'
check('Sealed six original R references remain byte-identical',digest(original.read_bytes())=='963b0df48e0626135ac9c8b1197976b1f1d12543ffd48ed5a86e42a7789c07cc',str(original.relative_to(B)),digest(original.read_bytes()))
inventory=j('all-editions-inventory.json');obs=jl(P/'archive_observations.jsonl');sources=jl(P/'sources.jsonl');cases=j('cases.json')
check('Every enumerated archive has exactly one actual observation',
      len(obs)==len(inventory)==78 and Counter(x['archive_id'] for x in obs)==Counter(x['archive_id'] for x in inventory),
      ['all-editions-inventory.json','archive_observations.jsonl'])
check('All archive observations succeeded',all('error' not in x for x in obs),'archive_observations.jsonl')
hash_good=0;member_good=0;missing_good=0;publication_good=0
for x in obs:
    f=next(z/x['archive_id'] for z in [P/'cache',B/'cache'] if (z/x['archive_id']).exists())
    if digest(f.read_bytes())==x['archive_sha256']:hash_good+=1
    with tarfile.open(f,'r:gz') as t:
        names=t.getnames()
        desc=t.extractfile(x['project']+'/DESCRIPTION').read()
        if digest(desc)==x['publication_description_sha256'] and ('Date/Publication: '+x['publication_raw']).encode() in desc:publication_good+=1
        for d in x['documents']:
            if d['original_member_present']:
                if digest(t.extractfile(d['member_path']).read())==d['member_sha256']:member_good+=1
            elif d['member_path'] not in names:missing_good+=1
check('All downloaded archive SHA256 values reproduce',hash_good==78,'archive_observations.jsonl',str(hash_good))
check('All present member hashes and absent-member claims reproduce',member_good+missing_good==156,'archive_observations.jsonl',json.dumps(dict(member_hashes=member_good,missing_members=missing_good)))
check('All publication strings come from exact original DESCRIPTION bytes',publication_good==78,'excerpts/*DESCRIPTION* and archive_observations.jsonl',str(publication_good))
ex=j('excerpt-manifest.json')
check('Every retained snippet SHA256 reproduces',all(digest((P/x['path']).read_bytes())==x['sha256'] for x in ex),'excerpt-manifest.json',str(len(ex)))
ids=[x['source_id'] for x in sources]
check('Source identifiers are unique',len(ids)==len(set(ids)),'sources.jsonl',str(len(ids)))
check('Every case source id resolves',all(s in ids for c in cases for s in c['source_ids']),'cases.json and sources.jsonl')
counted=[s for s in sources if s['count_minimum']]
check('Counted sources have unique duplicate groups',len({s['duplicate_group'] for s in counted})==len(counted),'sources.jsonl')
check('Minimum contribution has four actual changed compiled HTML documents',
      sum(s['count_minimum'] and s['count_category']=='consumer_followup' for s in sources)==4 and
      all(s['kind']=='actual_CRAN_archive_compiled_HTML' for s in sources if s['count_minimum'] and s['count_category']=='consumer_followup'),
      'sources.jsonl',json.dumps([s['source_id'] for s in sources if s['count_minimum'] and s['count_category']=='consumer_followup']))
intervals=j('intervals.json');bad=[]
for i in intervals:
    if 'seconds' in i:
        a=dt.datetime.fromisoformat(i['start'].replace('Z','+00:00'));b=dt.datetime.fromisoformat(i['end'].replace('Z','+00:00'))
        if (b-a).total_seconds()!=i['seconds'] or abs(i['days']-i['seconds']/86400)>1e-12:bad.append(i['interval_id'])
check('Recorded UTC second/day arithmetic reproduces',not bad,'intervals.json',json.dumps(bad))
check('No unknown start is mislabeled right-censored',all(not i['right_censored'] for i in intervals),'intervals.json')
check('Six references and frozen purposes preserved',len(cases)==6 and {c['reference_id'] for c in cases}=={r['reference_id'] for r in jl(original)},'cases.json; ../final/references.jsonl')
check('Purpose changes/retirement excluded from strict correction intervals',
      all(not i.get('eligible_for_strict_upstream_publication',False) for i in intervals) and
      all(not i.get('eligible_for_aux_source_publication',False) for i in intervals if i['reference_id'] in ['A-R04','A-R06']),
      'intervals.json')
check('Three same-purpose source-to-publication pairs correspond to only two commits',
      len([i for i in intervals if i.get('eligible_for_aux_source_publication')])==3 and
      len({i['start'] for i in intervals if i.get('eligible_for_aux_source_publication')})==2,'intervals.json')
current=j('current-http.json');mdn=next(c for c in cases if c['reference_id']=='A-R03');hold=next(c for c in cases if c['reference_id']=='A-R04');bts=next(c for c in cases if c['reference_id']=='A-R06')
check('Key maintain/hold/replace judgments preserve distinct HTTP and purpose evidence',
      mdn['verdict']=='유지' and hold['verdict']=='보류' and hold['current_http']['final_fragment_present'] is True and bts['verdict']=='교체' and bts['current_http']['status']==200 and bts['current_http']['needed_section_present'] is False,
      ['cases.json','excerpts/R-U04-install-anchor-fragment.txt','excerpts/R-U06-full-redirect-payload.html'])
check('Independent external review or blind prediction not falsely claimed',all(c['blinded_comparison_status'].startswith('not performed') for c in cases),'cases.json')
git=subprocess.run(['git','rev-parse','HEAD'],cwd=P,check=True,capture_output=True,text=True).stdout.strip()
inputs={n:digest((P/n).read_bytes()) for n in ['sources.jsonl','cases.json','intervals.json','chains.json','archive_observations.jsonl','all-editions-inventory.json','excerpt-manifest.json','verify_followup.py']}
receipt=dict(executed_at_utc=dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00','Z'),
             command='python docs/workstreams/research/AF-RES-032/collectors/cran/followup/verify_followup.py',
             target_git_HEAD=git,scope='Local working-tree R collector files; this is not a receipt for later root commits',
             input_sha256=inputs,checks=checks,passed=sum(c['met'] for c in checks),total=len(checks),
             exit_code=0 if all(c['met'] for c in checks) else 1,
             limitations=['Same collector integrity recheck, not independent external review.',
                          'No package installation, rendering, reader execution, or UI click is tested.',
                          'Root must perform whole-workstream session check --fetch and remote fixed-SHA reread before handoff.'])
(P/'verification.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
cost=[]
for c in cases:
    rid=c['reference_id'];ss=[s for s in sources if rid in s['reference_ids']]
    relevant_dates=['upstream_effective','consumer_source_edit','consumer_merge','consumer_build','reader_report','reader_click']
    cost.append(dict(reference_id=rid,enumerated_archive_opens=c['read_archives'],compiled_document_observations=c['read_archives'],
                     critical_boundary_document_rereads=len([x for x in j('boundary-direct-reads.json') if x['reference_id']==rid]),
                     source_records_including_duplicates=len(ss),counted_unique_followup_sources=sum(s['count_minimum'] and s['count_category']=='consumer_followup' for s in ss),
                     missing_clock_fields=sum(c['date_roles'][k] is None for k in relevant_dates),
                     missing_clock_field_names=';'.join(k for k in relevant_dates if c['date_roles'][k] is None),
                     cost_unit_note='Archive opens / compiled-document states / source records; not elapsed human time and not independent originals. No masked-view external rereads performed.'))
with (P/'costs.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(cost[0]));w.writeheader();w.writerows(cost)
print(json.dumps(dict(passed=receipt['passed'],total=receipt['total'],exit_code=receipt['exit_code'],target_git_HEAD=git,input_sha256=inputs),indent=2))
raise SystemExit(receipt['exit_code'])
