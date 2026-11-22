"""Read-only acceptance-data integrity audit; unmet research gates are not errors in reporting."""
from __future__ import annotations
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[3]
PREFIX='docs/workstreams/research/AF-RES-043/'

def jl(path):return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]
def csvrows(path):
    with path.open(newline='') as f:return list(csv.DictReader(f))

def audit():
    errors=[];checks={}
    def check(name,condition,details):
        checks[name]={'met':bool(condition),'details':details}
        if not condition:errors.append(name)
    cards=jl(ROOT/'cards.jsonl');comps={r['case_id']:r for r in jl(ROOT/'components.jsonl')};key=jl(ROOT/'key.jsonl')
    judgments=csvrows(ROOT/'judgments.csv');reads=csvrows(ROOT/'reads.csv');pairs=csvrows(ROOT/'pairs.csv');sources=jl(ROOT/'sources.jsonl')
    seal=json.loads((ROOT/'evidence/input-seal.json').read_text())
    check('8_cases',len(key)==8,len(key))
    check('32_unique_cards',len(cards)==len({c['card_id'] for c in cards})==32,len(cards))
    check('64_unique_judgments',len(judgments)==len({j['judgment_id'] for j in judgments})==64,len(judgments))
    check('64_case_task_pairs',len(pairs)==len({p['pair_id'] for p in pairs})==64,len(pairs))
    check('card_task_bijection',Counter((j['card_id'],j['task']) for j in judgments)==Counter((c['card_id'],t) for c in cards for t in ('C','H')),len(judgments))
    check('identical_elements',all(c['body']=='\n\n'.join(comps[c['case_id']][e] for e in c['elements']) for c in cards),'B→L→X; missing-X marker retained')
    check('body_hashes',all(hashlib.sha256(c['body'].encode()).hexdigest()==c['sha256'] for c in cards),32)
    check('sealed_key_cards_components',all(hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==seal[field] for f,field in [('cards.jsonl','cards_sha256'),('key.jsonl','key_sha256'),('components.jsonl','components_sha256')]),'phaseII digests')
    raw=[r for reader in ('reader_a','reader_b','reader_c') for r in jl(ROOT/'readers'/reader/'judgments.jsonl')]
    by={j['judgment_id']:j for j in judgments}
    differences=[]
    for r in raw:
        for k,v in r.items():
            expect=json.dumps(v,ensure_ascii=False,sort_keys=True) if isinstance(v,(list,dict,bool)) else str(v)
            if expect!=by[r['judgment_id']][k]:differences.append((r['judgment_id'],k))
    check('raw_judgment_fields_unchanged',not differences,differences)
    rs=json.loads((ROOT/'evidence/read-seal.json').read_text())
    badhash=[f for f,h in rs['file_sha256'].items() if f!='judgments.csv' and hashlib.sha256((ROOT/f).read_bytes()).hexdigest()!=h]
    check('phaseIII_read_hashes',not badhash,badhash)
    opcounts=Counter(r['judgment_id'] for r in reads if r['mode']=='publisher_open')
    check('publisher_budget',len(opcounts)==64 and max(opcounts.values())<=2,dict(Counter(opcounts.values())))
    cm={c['card_id']:c for c in cards}
    firstbad=[];second=[];routebad=[]
    for j in judgments:
        ops=[r for r in reads if r['judgment_id']==j['judgment_id'] and r['mode']=='publisher_open']
        visible=re.findall(r'https?://\S+',cm[j['card_id']]['body'])
        if ops[0]['requested_url'] not in visible:firstbad.append(j['judgment_id'])
        if len(ops)==2:
            r=ops[1];second.append(r)
            if r['parent_read_id']!=ops[0]['read_id'] or r['href_evidence'].startswith('미확인'):routebad.append(r['read_id'])
    check('first_url_card_visible',not firstbad,firstbad)
    check('second_parent_actual_link',not routebad,{'second_opens':len(second),'bad':routebad})
    literal_unknown=[r['read_id'] for r in second if r['href_raw'].startswith('미확인')]
    # This known reporting gap is asserted as a fact, not silently treated as a passed completeness gate.
    check('literal_href_gap_reported_correctly',len(literal_unknown)==7,{'literal_known':len(second)-len(literal_unknown),'denominator':len(second),'unknown_ids':literal_unknown})
    required='source_id original_url pinned_url_or_version publisher event_or_publication_date checked_utc locator source_kind verified_fact limitation question_ids case_ids duplicate_group counted'.split()
    missing=[(s['source_id'],[f for f in required if f not in s]) for s in sources if any(f not in s for f in required)]
    check('source_schema',not missing,missing)
    check('source_ids_unique',len(sources)==len({s['source_id'] for s in sources}),len(sources))
    counted=[s for s in sources if s['counted']]
    check('strict_no_double_count',len(counted)==len({s['duplicate_group'] for s in counted})==23,len(counted))
    sc=json.loads((ROOT/'evidence/source-count-audit.json').read_text())
    works=sc['counted_primary_unique_lower_bound']['works']
    check('28_primary_work_lower_bound',len(works)==len({w['duplicate_group'] for w in works})==28 and all(w['source_id'] in {s['source_id'] for s in sources} for w in works),28)
    text=(ROOT/'RESULT.md').read_text();lines=text.splitlines();tables=[];start=None
    for i,line in enumerate(lines+['']):
        if line.startswith('| '):
            if start is None:start=i
        elif start is not None:
            tables.append({'start_line':start+1,'end_line':i,'data_rows':i-start-2,'lines':lines[start:i]});start=None
    check('required_tables_first',lines[0].startswith('# ') and lines[2].startswith('| ') and tables[0]['data_rows']==32 and tables[1]['data_rows']==16,[(t['start_line'],t['end_line'],t['data_rows']) for t in tables[:2]])
    check('result_ends_three_weaknesses',tables[-1]['data_rows']==3 and lines[-1].startswith('| '),{'start_line':tables[-1]['start_line'],'end_line':tables[-1]['end_line'],'rows':tables[-1]['data_rows']})
    check('markdown_table_column_counts',all(len({len(re.split(r'(?<!\\)\|',line)) for line in t['lines']})==1 for t in tables),'all report tables')
    for filename in ('frame.csv','versions.csv','reads.csv','judgments.csv','pairs.csv'):
        rows=csvrows(ROOT/filename);blank=sum(v=='' for r in rows for v in r.values())
        check('no_implicit_missing_'+filename,blank==0,blank)
    summary=json.loads((ROOT/'evidence/analysis-summary.json').read_text())
    check('pair_partition_sum',all(sum(s[k] for k in ['both_correct','left_only','right_only','both_incorrect','hold_or_unverified','criterion_unknown'])==s['selected_slots'] for s in summary['pair_summary']),48)
    check('strata_kept',Counter(j['stratum'] for j in judgments)=={'natural':32,'correction_first':32},dict(Counter(j['stratum'] for j in judgments)))
    check('independent_audit_present',(ROOT/'evidence/analysis-audit.md').exists() and (ROOT/'evidence/acceptance-audit-notes.md').exists(),'same-model self-audits, not human replication')
    changed=subprocess.check_output(['git','diff','--name-only','333e83c9a46b0c005d22efcccbb5a055b27e904e'],cwd=REPO,text=True).splitlines()
    untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=REPO,text=True).splitlines()
    outside=[p for p in changed+untracked if not p.startswith(PREFIX)]
    check('owned_path_only',not outside,outside)
    control_diff=subprocess.check_output(['git','diff','333e83c9a46b0c005d22efcccbb5a055b27e904e','--','docs/automation/dot-control.json'],cwd=REPO,text=True)
    check('dot_control_unchanged',not control_diff,'no diff')
    return {'integrity_pass':not errors,'errors':errors,'checks':checks,'table_locations':[{k:v for k,v in t.items() if k!='lines'} for t in tables],
       'full_research_acceptance':False,'known_gaps':['mandatory source composition23/24','UCLA old edition and X missing','actual natural consumer target editions unknown','sampling trace gaps','N-S-01 card neutrality','literal href7/9unknown','same-model/order/retrieval-route limitations']}


if __name__=='__main__':
    result=audit();print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if result['integrity_pass'] else 1)
