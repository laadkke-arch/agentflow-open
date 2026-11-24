#!/usr/bin/env python3
"""Read-only acceptance of the research ledger, graph and report relationships.

Replays deterministic evidence; never claims new reader observations or validates
historical software behavior. By default also regenerates every permitted path.
"""
from pathlib import Path
from collections import Counter,defaultdict
from datetime import datetime,timezone
import argparse,csv,gzip,hashlib,json,re,subprocess,sys,time

OWN=Path(__file__).resolve().parent.parent
REPO=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=OWN,text=True).strip())
PREFIX=str(OWN.relative_to(REPO))+'/'
sys.path[:0]=[str(OWN/'viewer'),str(OWN/'analysis')]
from reader import Corpus
from enumerate_paths import enumerate_paths,replay
from analyze_coverage import load_graph,analyze_mode
from build_results import build

def jl(name):return [json.loads(s) for s in (OWN/name).read_text().splitlines() if s.strip()]
def js(name):return json.loads((OWN/name).read_text())
def sha(raw):return hashlib.sha256(raw).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def utc():return datetime.now(timezone.utc).isoformat()
def plain(obj):return json.loads(json.dumps(obj,ensure_ascii=False))

def run(deep=True):
    result={};corpus=Corpus.load(OWN/'corpus.json.gz');docs=corpus.documents
    # Recheck immutable phase inputs against their actual Git objects.
    phase_files={
      '7a76c8ccefb6243b84e86efce16b62ba8b47ec2d':['SCOPE.md','manifest.json'],
      '878f2e1b8d053f6eea4e3473d5b467ca98476a01':['cases.json','frame.csv'],
      '762fe1fc57b3b5f765f9d13537fa9c15b71b5b80':['packets.jsonl','authoring/draft-packets.jsonl','authoring/phrase-provenance.jsonl','authoring/author-exposure.jsonl'],
      '8b57d241d88cb6c5ddf3454d2b28fa3fb46fd473':['corpus.json.gz','viewer/reader.py','gold-work/pandoc/gold.json','gold-work/pandoc/target-spans.json','gold-work/imagemagick/gold.json','gold-work/imagemagick/target-spans.json','calibration/preregistered-cases.json'],
      '47e8d24ad9c0313f6d1a361882198f42307a0d5d':[f'readers/r{i:02}/events.jsonl' for i in range(1,19)]}
    for seal,names in phase_files.items():
        for n in names:assert (OWN/n).read_bytes()==git('show',seal+':'+PREFIX+n),(seal,n)
    result['immutable_phase_files']=sum(map(len,phase_files.values()))
    cases=js('cases.json')['cases'];packets=jl('packets.jsonl');trails=jl('trails.jsonl')
    assert len(cases)==6 and len(packets)==18 and len(trails)==54
    assert len({(t['packet_id'],t['step']) for t in trails})==54
    bypacket=defaultdict(list)
    for t in trails:bypacket[t['packet_id']].append(t)
    sessions={s['session']:s for s in js('analysis/trial-summary.json')['sessions']}
    for c in cases:
        pp=[p for p in packets if p['case_id']==c['case_id']]
        assert {p['condition'] for p in pp}==set('ABC')
        assert len({p['start_url'] for p in pp})==len({p['document_version'] for p in pp})==1
        pmap={p['condition']:p for p in pp};b,cc=pmap['B'],pmap['C']
        assert b['hint_codepoints']==cc['hint_codepoints'] and 50<=b['hint_codepoints']<=100
        assert all(p['hint_codepoints']==len(p['hint']) and p['hint_utf8_bytes']==len(p['hint'].encode()) for p in pp)
        ordered=sorted(pp,key=lambda p:sessions[p['packet_id']]['initialized_utc'])
        assert ''.join(p['condition'] for p in ordered)==c['condition_order']
        for p,q in zip(ordered,ordered[1:]):assert sessions[p['packet_id']]['finished_utc']<=sessions[q['packet_id']]['initialized_utc']
    # Every real route is replayable with the same visible options and bytes.
    for p in packets:
        rr=bypacket[p['packet_id']];assert [r['step'] for r in rr]==[1,2,3]
        actual=replay(corpus,p['start_doc_id'],[r['choice']['action'] for r in rr])
        for old,new in zip(rr,actual['steps']):
            v=new['view'];assert v==old['view']
            assert v['display_codepoints']<=1500
            assert v['content_codepoints']+v['total_navigation_codepoints']==v['display_codepoints']
            assert v['content_utf8_bytes']+v['total_navigation_utf8_bytes']==v['display_utf8_bytes']
            assert sha(v['display_text'].encode())==old['display_sha256']
    result['actual_recipient_routes_replayed']=18;result['actual_displays_exact']=54
    # Complete graph comparison is independent of the prose impossibility claim.
    req=js('gold-intervals.json')['cases'];lengths={d:len(v['text']) for d,v in docs.items()}
    frozen={(r['case_id'],r['mode']):r for r in jl('reachability.jsonl')};npaths=0
    for c in req:
        cid=c['case_id'];directory=OWN/'reachability/raw'/cid
        graph=load_graph(directory,corpus.sha256,lengths)
        assert graph.summary['enumeration_complete'] and graph.summary['remaining_queue_entries']==0
        npaths+=len(graph.paths)
        if deep:
            nodes,views,summary=enumerate_paths(corpus,c['start_doc_id'])
            old_nodes=jl(f'reachability/raw/{cid}/paths.jsonl')
            old_views={v['view_id']:{k:x for k,x in v.items() if k!='view_id'} for v in jl(f'reachability/raw/{cid}/views.jsonl')}
            assert nodes==old_nodes and views==old_views
            assert summary['enumeration_complete'] and summary['remaining_queue_entries']==0
        for mode,rule in c['modes'].items():
            observed,_=analyze_mode(c,mode,rule,graph,lengths);saved=frozen[cid,mode]
            for k,v in observed.items():
                if k!='graph_directory':assert plain(v)==saved[k],(cid,mode,k)
    result['bounded_graphs_complete']=6;result['path_prefix_nodes']=npaths
    result['all_paths_reenumerated']=deep;result['coverage_modes_recomputed']=len(frozen)
    # Separate constructed witness/near-wrong and post-reference start-only layers.
    cal=js('calibration/preregistered-cases.json');checks=js('calibration/replay-check.json')['checks']
    for c in cal:
        for label,key in [('witness','witness_actions'),('near-wrong','near_wrong_actions')]:
            if key not in c:continue
            rr=replay(corpus,c['start_doc'],c[key]);got=[]
            for interval in c['required_intervals']:
                got.append(any(v['view']['doc_id']==interval['doc_id'] and v['view']['offset_start']<=interval['start'] and interval['end']<=v['view']['offset_end'] for v in rr['steps']))
            expected=next(x for x in checks if x['case_id']==c['case_id'] and x['path_kind']==label)
            assert got==expected['coverage_by_required_interval'] and all(got)==expected['all_required_supported']
    d0=js('calibration/start-only-diagnostic.json');assert corpus.render('i7114_processing',0)==d0['view']
    result['constructed_replays_verified']=3;result['post_reference_start_only_verified']=1
    # Judge evidence must come from the same recipient's earlier/current displays.
    mapping={m['masked_id']:m['packet_id'] for m in js('evaluation/masking-map.json')}
    judgment_rows=[];evidence_quotes=0
    for family in ['pandoc','imagemagick']:
        receipt=js(f'evaluation/evaluator-{family}.json')
        rows=jl(f'evaluation/judgments-{family}.jsonl');assert len(rows)==27
        judgment_rows.extend(rows)
        for r in rows:
            sid=mapping[r['masked_id']];visible=[t for t in bypacket[sid] if t['step']<=r['step']]
            for e in r['evidence_used']:
                q=e.get('quote');assert q and any(q in t['view']['display_text'] for t in visible),(sid,r['step'],q)
                if 'start' in e and 'end' in e:
                    assert docs[e['doc_id']]['text'][e['start']:e['end']]==q
                    assert any(t['doc_id']==e['doc_id'] and t['offset_start']<=e['start'] and e['end']<=t['offset_end'] for t in visible)
                evidence_quotes+=1
    assert len({(r['masked_id'],r['step']) for r in judgment_rows})==54
    result['masked_judgments']=54;result['judge_evidence_quotes_visible']=evidence_quotes
    sources=jl('sources.jsonl');counted=[s for s in sources if s['unique_counted']]
    assert len({s['source_id'] for s in sources})==len(sources)
    assert len({s['work_id'] for s in counted})==len(counted)
    allocation=Counter(s['allocation'] for s in counted)
    for k,n in {'natural_request':6,'definition':8,'regression':6,'cross_domain_supplement':4}.items():assert allocation[k]>=n
    assert all(s['author'] and s['read_sections'] and s['original_url'] and s['checked_utc'] for s in counted)
    assert not any(s['unique_counted'] for s in sources if s['ledger_origin'] in ['recipient_reopen','source_audit_reopen'])
    result['source_rows']=len(sources);result['unique_works']=len(counted);result['allocation']=dict(allocation)
    # Rebuild all required tables and numeric ledgers from immutable inputs.
    for n,raw in build().items():assert (OWN/n).read_bytes()==raw.encode(),n
    metrics=js('metrics.json');answers=list(csv.DictReader((OWN/'answers.csv').open()));pairs=list(csv.DictReader((OWN/'pairs.csv').open()))
    assert len(answers)==54 and len(pairs)==18
    assert metrics['natural']['full_reachable_cases']==0 and metrics['natural']['reachable_opportunity_success_rate'] is None
    assert metrics['natural']['partial_reconstruction_stages']==sum(r['partial_reconstruction'] for r in judgment_rows)
    assert metrics['natural']['counterexample_flag_stages']==sum(r['counterexample_found'] for r in judgment_rows)
    assert metrics['total_reader_display_codepoints']==sum(t['cost']['display_codepoints'] for t in trails)
    assert metrics['total_reader_display_utf8_bytes']==sum(t['cost']['display_utf8_bytes'] for t in trails)
    assert next(a for a in answers if a['packet_id']=='r03' and a['step']=='3')['partial_reconstruction']=='False'
    errors=[a for a in answers if a['citation_unmatched_count']!='0'];assert len(errors)==1 and errors[0]['row_id']=='r13-s2'
    assert all(p['delta_opens_right_minus_left']=='0' for p in pairs)
    result['answers_rows']=54;result['pair_rows']=18;result['required_tables_exact_rebuild']=True
    report=(OWN/'RESULT.md').read_text();assert report.startswith('## 표 1.')
    assert report.index('## 표 1.')<report.index('## 표 2.')<report.index('## 표 3.')<report.index('## Q1.')
    sections=re.split(r'(?:^|\n)## 표 [123][^\n]*\n',report)
    for index,count in [(1,9),(2,54),(3,18)]:
        lines=[]
        for line in sections[index].splitlines():
            if line.startswith('| '):lines.append(line)
            elif lines:break
        assert len(lines)==count+2,(index,len(lines))
    ending=report.rstrip().split('\n')[-5:]
    assert ending[0].startswith('| 가장 중요한 불일치·약점') and all(x.startswith('| ') for x in ending)
    missing=[];links=0
    for name in ['RESULT.md','SELF_CHECK.md','reproduce.md']:
        for target in re.findall(r'\]\(([^)]+)\)',(OWN/name).read_text()):
            if '://' in target or target.startswith('#'):continue
            target=target.split('#')[0]
            if not target:continue
            links+=1
            path=(OWN/target).resolve()
            if not path.exists() and target!='evidence/acceptance-evidence.json':missing.append([name,target])
    assert not missing,missing
    result['relative_report_links_checked']=links
    result['future_acceptance_receipt_allowed_missing']='evidence/acceptance-evidence.json is written only after the result commit'
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--skip-reenumeration',action='store_true');ap.add_argument('--output');args=ap.parse_args()
    started=utc();tick=time.monotonic();head=git('rev-parse','HEAD').decode().strip()
    result=run(not args.skip_reenumeration)
    receipt={'check':'AF-RES-116 artifact acceptance','actor':'root deterministic checker','input_sha':head,'working_tree_dirty':bool(git('status','--porcelain').strip()),'checker_sha256':sha(Path(__file__).read_bytes()),'started_utc':started,'completed_utc':utc(),'wall_seconds':time.monotonic()-tick,'exit_code':0,'checks':result,'scope':'frozen corpus, provenance, recorded routes, semantic-judgment linkage, counts and report reconstruction; no new semantic evaluator or historical runtime'}
    if args.output:
        out=Path(args.output).resolve();assert out.is_relative_to(OWN);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(receipt,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
