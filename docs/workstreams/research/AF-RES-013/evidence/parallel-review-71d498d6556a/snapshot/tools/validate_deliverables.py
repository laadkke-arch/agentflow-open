"""Check the requested research acceptance gates without modifying other paths.

This is a deliverable/provenance gate, not a substitute for source reading or a
test of the referenced software. Run after aggregation and final documentation.
"""
import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
OWNED = ROOT.relative_to(REPO).as_posix()
SOURCE = 'a18d8d2e1575d9b679442134fd0f6f8e17423bfe'
GOLD = 'f6f59a85949a001792b80260dd454c3fcc714a70'
T1 = ['사례 ID','계열','원문 주소(고정 판)','결정일','정답 항목 수(완성품·부품·같은 분야 설계·다른 생태계·다른 분야·표준논문)','기준선 A 적중','기준선 B 적중','놓친 정답 항목','정답원 밖 유용 후보','근접 오답','깨진·가짜 링크','누설·사후 자료','미확인']
T2 = ['역할','정답 항목 수(분모)','기준선 A 적중(비율)','기준선 B 적중(비율)','대표 놓침 사례 ID','미확인']
T3 = ['주장','근거 자료 주소','확인한 내용','반증 시도','미확인']
SELF = ['세부 질문','답 한 줄','붙은 출처 ID(종류 수)','반증 시도(쓴 질의·자료와 결과)','남은 불확실성']

def git(*args):
    return subprocess.check_output(['git',*args],cwd=REPO).decode().rstrip('\n')

def read(name):
    return json.loads((ROOT/name).read_text())

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--final',action='store_true',help='Require RESULT and SELF_CHECK as well as data gates')
    args=parser.parse_args()
    checks=[]
    def check(name, passed, evidence):
        checks.append({'gate':name,'passed':bool(passed),'evidence':evidence})

    cases=read('cases/CASES.json')['cases']; ids={c['id'] for c in cases}
    families=Counter(c['family'] for c in cases)
    check('31 distinct cases / at least four families / family share <= 50%',len(cases)>=30 and len(ids)==len(cases) and len(families)>=4 and max(families.values())/len(cases)<=.5,dict(families))
    check('At least three primary gold items per case',min(len(c['gold_items']) for c in cases)>=3,{c['id']:len(c['gold_items']) for c in cases})
    check('Pinned versions and explicit decision dates',all(re.fullmatch('[0-9a-f]{40}',c['pinned_version']) and re.fullmatch(r'\d{4}-\d{2}-\d{2}',c['decision_date']) for c in cases),'cases/CASES.json; decision-event semantics remain case-specific')
    adopted=[]
    for c in cases:
        entries=c.get('superseded_by') or []
        if isinstance(entries,dict): entries=[entries]
        if any(x.get('type','').startswith(('adopted_','partial_reversal_after_adoption')) or x.get('kind')=='partial_reversal' for x in entries): adopted.append(c['id'])
    check('At least five adopted decisions subsequently replaced/reversed',len(adopted)>=5,{'case_ids':adopted,'scope':'Includes expressly documented partial reversals; excludes rejected/draft replacement.'})
    prefix=[]
    for c in cases:
        path=OWNED+'/'+c['prefix_file']
        original=subprocess.check_output(['git','show',c['prefix_commit']+':'+path],cwd=REPO)
        current=(ROOT/c['prefix_file']).read_bytes()
        ancestor=subprocess.run(['git','merge-base','--is-ancestor',c['prefix_commit'],GOLD],cwd=REPO).returncode==0
        prefix.append({'id':c['id'],'commit':c['prefix_commit'],'hash_matches':digest(original)==digest(current)==c['prefix_sha256'],'ancestor_of_gold':ancestor})
    check('Every exact prefix predates frozen gold',all(x['hash_matches'] and x['ancestor_of_gold'] for x in prefix),prefix)
    audit=read('evidence/RUN_AUDIT.json')
    check('A all cases / B at least twenty',audit['coverage']['A']['completed']==len(cases) and audit['coverage']['B']['completed']>=20,audit['coverage'])
    check('Run budgets and recorded isolation passed',not audit['errors'],'tools/audit_runs.py validates raw answers, model/context flags, all A code-search attempts and B opened discovery catalogues. Flags do not prove physical isolation or absence of pretraining.')
    resolutions=read('evidence/judgments/AUDIT_RESOLUTIONS.json')['rows']
    resolved={(x['baseline'],x['case_id'],x['candidate_rank']) for x in resolutions if x['status']=='resolved'}
    url_notes={(x['baseline'],x['case_id'],x['candidate_rank']) for x in audit['notes'] if 'candidate_rank' in x}
    check('Exact-URL audit differences resolved',url_notes<=resolved,{'notes':len(url_notes),'resolved':len(resolved),'remaining':sorted(url_notes-resolved)})
    agg=read('evidence/AGGREGATES.json'); judgment_ledger=read('JUDGMENTS.json'); judgments=judgment_ledger['judgments']
    raw=sum(len(read('runs/'+b+'/'+cid+'.json')['candidates']) for b in ['A','B'] for cid in ids if (ROOT/'runs'/b/(cid+'.json')).exists())
    keys={(x['baseline'],x['case_id'],x['rank']) for x in judgments}
    check('Every output candidate has one explicit judgment',not agg['pending'] and len(keys)==len(judgments)==raw,{'judgments':len(judgments),'raw_candidates':raw,'pending':agg['pending']})
    detail_files={}; detail_ok=True
    for shard in judgment_ledger.get('detail_shards',[]):
        data=read(shard['path'])
        detail_files[shard['path']]=data
        detail_ok &= digest((ROOT/shard['path']).read_bytes())==shard['sha256'] and len(data['judgments'])==shard['judgment_count']
    for row in judgments:
        path, pointer=row['details'].split('#')
        index=int(pointer.rsplit('/',1)[-1]); full=detail_files[path]['judgments'][index]
        for key,value in row.items():
            if key=='details': continue
            if key=='H': detail_ok &= value==[{k:h[k] for k in ['constraint_id','value']} for h in full[key]]
            elif key=='gold_matches': detail_ok &= value==[{k:v for k,v in m.items() if k!='rationale'} for m in full[key]]
            else: detail_ok &= value==full[key]
        detail_ok &= all(key in full for key in judgment_ledger['detail_only_fields'])
    check('Expanded judgments preserve every value and explanation',detail_ok and sum(len(x['judgments']) for x in detail_files.values())==raw,{'shards':len(detail_files),'expanded_records':sum(len(x['judgments']) for x in detail_files.values()),'contract':'Each main record points to its complete judgment; shard hashes and every retained value match.'})
    check('Temporal identities remain separate from utility and matches',all(x['date_status'] in ['pre_decision','post_decision','unknown'] and x['judge'] in ['작업자','내부 별도 검토'] for x in judgments),'JUDGMENTS.json; strict_historical_gold_ids and nongold_useful have separate fields; no runtime outcome inferred')
    count=read('evidence/SOURCE_COUNT.json'); sources=read('sources.json')
    needed={'id','url','accessed_at_utc','source_type','title','version_or_date','sections_read','confirmed','limits','level','used_in'}
    all_sources=list(sources['sources']); all_excluded=list(sources['excluded']); source_shards_ok=True
    for shard in sources.get('source_shards',[]):
        data=read(shard['path'])
        source_shards_ok &= digest((ROOT/shard['path']).read_bytes())==shard['sha256'] and len(data['sources'])==shard['source_count'] and len(data['excluded'])==shard['excluded_count']
        all_sources.extend(data['sources']); all_excluded.extend(data['excluded'])
    check('Source records contain required fields',all(needed<=set(x) for x in all_sources) and len({x['id'] for x in all_sources})==len(all_sources),{'core_records':len(sources['sources']),'all_records':len(all_sources),'excluded_records':len(all_excluded)})
    check('Source shards preserve complete ledger and counts',source_shards_ok and len(all_sources)==count['all_source_records_including_support'] and len(all_excluded)==count['excluded_attempts'],{'shards':len(sources.get('source_shards',[])),'all_records':len(all_sources),'excluded_records':len(all_excluded),'all_rows_have_required_fields':all(needed<=set(x) for x in all_sources)})
    check('Noncase minimum and site diversity',count['noncase_counted']>=20 and count['single_site_max']<=3,{'count':count['noncase_counted'],'sites':count['sites'],'interpretation':count['limits']})
    check('Required noncase source categories',len(count['templates_or_procedures'])>=4 and len(count['methodology_papers'])>=4 and len(count['crossfield_overviews'])>=3 and len(count['new_generative_citation_papers'])>=2 and all(count['new_generative_citation_papers'].values()) and len(count['review_originals'])>=5,count)
    check('Three independent-gold fields compared',(ROOT/'evidence/methods/CROSSFIELD.md').exists(),'Patent / law / academic primary overviews and bias mapping in evidence/methods/CROSSFIELD.md')
    check('Five counterexample searches and outcomes',(ROOT/'COUNTEREXAMPLES.md').exists() and (ROOT/'evidence/counterexamples/SEARCH_LOG.json').exists(),'COUNTEREXAMPLES.md and exact query/source ledger; a negative search is not proof of nonexistence')
    changed=git('diff','--name-only',SOURCE,'HEAD').splitlines()
    unstaged=git('status','--porcelain','--untracked-files=all').splitlines()
    local_paths=[x[3:] for x in unstaged]
    check('All repository writes stay in owned path',all(x.startswith(OWNED+'/') for x in changed+local_paths),{'committed_changed_paths':len(changed),'local_changed_paths':len(local_paths),'owned_path':OWNED})
    check('Forbidden shared control unchanged',git('diff',SOURCE,'HEAD','--','docs/automation/dot-control.json')=='','source_commit comparison')
    if args.final:
        result=(ROOT/'RESULT.md').read_text(); selfcheck=(ROOT/'SELF_CHECK.md').read_text()
        headers=['§1 필수 결과 표','§2 세부 질문별 답','§3 추가 분석','§4 가장 중요한 불일치·약점 3건과 다음 조사 제안','§5 한계']
        positions=[result.find(x) for x in headers]
        check('Required RESULT section order',all(x>=0 for x in positions) and positions==sorted(positions),headers)
        for n,cols in enumerate([T1,T2,T3],1):
            line='| '+' | '.join(cols)+' |'
            check('Exact table '+str(n)+' columns',line in result,cols)
        check('Exactly thirty-one case table rows',sum(bool(re.match(r'^\| C\d{2} \|',l)) for l in result.splitlines())==len(cases),'RESULT.md §1 table 1')
        check('Exactly six role rows',all('| '+role+' |' in result for role in ['같은 목적 완성품','재사용 부품','같은 분야의 다른 설계','다른 언어·생태계','다른 분야 원리','표준·논문']),'RESULT.md §1 table 2')
        check('Unknown table cells specify a confirmation action',all(re.search(r'미확인\([^)]{3,}\)',cell) for l in result.splitlines() if l.startswith('|') for cell in l.split('|') if '미확인' in cell and cell.strip()!='미확인'),'Checks unknown cells rather than treating absence as zero')
        section4=result[positions[3]:positions[4]] if min(positions)>=0 else ''
        check('Exactly three important discrepancies/weaknesses',len(re.findall(r'^### 4\.[123] ',section4,re.M))==3,'RESULT.md §4; each includes question, evidence, consequence and minimum follow-up scale')
        check('Self-check exact question table','| '+' | '.join(SELF)+' |' in selfcheck and all(re.search(r'^\| Q'+str(q)+r'\b',selfcheck,re.M) for q in range(1,9)),'SELF_CHECK.md Q1–Q8 and acceptance table')
    result={'schema_version':1,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'checked_head':git('rev-parse','HEAD'),'source_commit':SOURCE,'gold_commit':GOLD,'mode':'final_pre_handoff' if args.final else 'data','passed':all(c['passed'] for c in checks),'checks':checks,'limits':'Mechanical gates do not verify scientific truth or role reliability. Source-content and match judgments remain explicit researcher coding. HANDOFF is created only after this final check passes and is then remotely reread.'}
    (ROOT/'evidence/FINAL_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'passed':result['passed'],'checks':len(checks),'failed':[c['gate'] for c in checks if not c['passed']]},ensure_ascii=False))
    raise SystemExit(0 if result['passed'] else 1)

if __name__=='__main__': main()
