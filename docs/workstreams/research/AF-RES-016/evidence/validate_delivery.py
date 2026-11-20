#!/usr/bin/env python3
"""Acceptance verification of frozen artifacts and required report structure.
This does not create new research labels or claim human/product validation.
"""
import contextlib,csv,hashlib,io,json,math,re,runpy,subprocess,sys
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
from report_tables import T1_HEADERS,T2_HEADERS,T3_HEADERS,T4_HEADERS,t1_rows,t2_rows
BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[3]
OWN='docs/workstreams/research/AF-RES-016/'
SOURCE='24b22f8a068d02fa5be2aaaa0df50d241f7602a4'
A='0981732949cdea358c4ffa27aafd4ae50d310bbe';B='674f1c8eb99e531acee7531c8f1495f721c4dffd'
CHECKS=[]
def load(name):return json.loads((BASE/name).read_text())
def check(name,ok,evidence):
 CHECKS.append({'check':name,'pass':bool(ok),'evidence':evidence})
 if not ok:raise AssertionError(name+': '+str(evidence))
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def same(x,y):return x is None and y is None or x is not None and y is not None and abs(x-y)<1e-12

def verify():
 u=load('sample/units.json')['units'];a=load('coding/coder-a.json');b=load('coding/coder-b.json');ids=[x['unit_id'] for x in u]
 check('198 units in prescribed strata',len(ids)==198 and len(set(ids))==198 and Counter(x['sample'] for x in u)=={'011':120,'012':60,'004':18},dict(Counter(x['sample'] for x in u)))
 allowed={'S1':{'product','component','principle','mixed','unknown'},'S2':{'whole','part','reference','comparison','none','mixed','unknown'},'form':{'app','service','library','framework','standard','document','pattern','research','data','mixed','unknown'}}
 for name,obj in [('a',a),('b',b)]:
  rows=obj['rows'];check(name+' full unique ID coverage',len(rows)==198 and set(x['unit_id'] for x in rows)==set(ids) and len(set(x['unit_id'] for x in rows))==198,'198 rows')
  check(name+' all schemes and contributions valid',all(r['S1'] in allowed['S1'] and r['S2'] in allowed['S2'] and r['S3']['form'] in allowed['form'] and r['S3']['contribution']==r['S2'] and bool(r['reason'].strip()) for r in rows),'S1+S2+S3 per unit; S3 contribution is the S2 variable')
  raw=list(csv.DictReader((BASE/f'coding/coder-{name}-raw.tsv').open(),delimiter='\t'));index={r['unit_id']:r for r in rows}
  valid=len(raw)==198
  for r in raw:
   q=index[r['unit_id']];valid=valid and all(r[k]==q[k] for k in ('S1','S2','confidence','ambiguity','reason')) and r['form' if name=='a' else 'S3_form']==q['S3']['form']
   if name=='b':valid=valid and r['S3_contribution']==q['S3']['contribution']
  check(name+' raw response semantics preserved',valid,'TSV fields equal JSON, no re-labeling')
 frozen=load('coding/coder-a-freeze.json')['sha256']
 for p,h in frozen.items():check('frozen hash '+p,digest(BASE/p)==h,h)
 for r in load('coding/coder-b-provenance.json')['evidence_inputs_read']+load('coding/coder-b-provenance.json')['outputs']:
  check('B provenance hash '+Path(r['path']).name,digest(Path(r['path']))==r['sha256'],r['sha256'])
 check('A freeze is direct parent of B raw commit',git('rev-parse',B+'^')==A,{'a':A,'b':B})
 check('scope and codebook preceded coding',git('merge-base','68d1ee68bf2b0a6e636970ce71c89d2bba2b9bd0',A)=='68d1ee68bf2b0a6e636970ce71c89d2bba2b9bd0','pre-codebook commit ancestor of A')
 check('frozen codebook has three synthetic boundary examples per value',len([l for l in (BASE/'CODEBOOK.md').read_text().splitlines() if l.startswith('| ') and all(k in l for k in ('A:','B:','C:'))])==23,'5 S1 + 7 S2 + 11 form = 23 values; A/B/C examples each')
 # Re-run sampling in memory, including the direct LIST.md writer.
 captured={}
 class CapturePath:
  def __init__(self,name=''):self.name=name
  def __truediv__(self,name):return CapturePath(name)
  def write_text(self,s,*args,**kwargs):captured[self.name]=s;return len(s)
 m=runpy.run_path(str(BASE/'sample/select.py'),run_name='sample_replay_only')
 m['main'].__globals__['OUT']=CapturePath()
 with contextlib.redirect_stdout(io.StringIO()):m['main']()
 check('sample script replay byte-identical without writing inputs',set(captured)=={'units.json','baseline.json','selection.json','LIST.md'} and all(text==(BASE/'sample'/name).read_text() for name,text in captured.items()),list(captured))
 # Independent point estimate implementation from contingency counts.
 g=load('evidence/agreement.json');ai={r['unit_id']:r for r in a['rows']};bi={r['unit_id']:r for r in b['rows']}
 def lab(r,s):return (r['S3']['form'],r['S3']['contribution']) if s=='S3' else r['S3']['form'] if s=='S3_form' else r[s]
 for r in g['main']:
  ii=[x['unit_id'] for x in u if x['sample']==r['sample']];aa=[lab(ai[i],r['scheme']) for i in ii];bb=[lab(bi[i],r['scheme']) for i in ii]
  ca,cb=Counter(aa),Counter(bb);n=len(ii);ag=sum(x==y for x,y in zip(aa,bb));po=ag/n;pe=sum(ca[k]*cb[k] for k in ca.keys()|cb.keys())/n**2;k=(po-pe)/(1-pe) if pe<1 else None
  check('point estimate '+r['sample']+'/'+r['scheme'],r['n']==n and r['agree']==ag and same(r['po'],po) and same(r['pe'],pe) and same(r['kappa'],k),{'agree':ag,'n':n,'kappa':k})
  check('CI metadata '+r['sample']+'/'+r['scheme'],r['bootstrap_replicates']==5000 and 0<=r['undefined_kappa_replicates']<=5000 and len(r['kappa_ci95'])==2 and r['kappa_ci95'][0]<=r['kappa_ci95'][1] and len(r['po_ci95'])==2,'CI values independently recalculated in verification-audit.md; metadata and order checked here')
 check('baseline reproduces old149 and same120',g['baseline']['011_all_149']['agree']==75 and g['baseline']['011_all_149']['n']==149 and g['baseline']['011_selected_120']['agree']==66 and g['baseline']['011_selected_120']['n']==120,'75/149 and 66/120')
 dis=load('evidence/disagreements.json')['rows'];adj=load('coding/adjudication.json');impact=load('evidence/impact.json')
 expected_dis={i for i in ids if any(lab(ai[i],s)!=lab(bi[i],s) for s in ('S1','S2','S3'))}
 check('59 distinct disagreements and complete diagnostic review',len(dis)==59 and {r['unit_id'] for r in dis}==expected_dis=={r['unit_id'] for r in adj['rows']},Counter(r['sample'] for r in dis))
 check('diagnostic distribution',Counter(r['primary_type'] for r in adj['rows'])=={'경계 정의 부족':35,'문맥 부족':18,'실제 다의성':6},adj['primary_type_counts'])
 selected=load('evidence/impact-selection.json')['unit_ids']
 check('30 actual disagreement cases reviewed',len(impact['rows'])==len(set(selected))==30 and [r['unit_id'] for r in impact['rows']]==selected and set(selected)<=expected_dis,'30/59 selected by fixed sorted evenly-spaced rule')
 check('Q7 is transparently a shared manual judgment audit',all(r['judgment_a']==r['judgment_b'] and not r['label_only_changed'] for r in impact['rows']) and impact['summary']['insufficient_cases']==14 and impact['summary']['overall_label_not_assigned_cases']==15 and '독립적으로' in impact['serialization_note'],impact['summary'])
 check('Q7 fixed/new-use contrasts separated',len(impact['new_use_hypotheses'])==2 and all(not x['included_in_main_change_rate'] and x['level']=='H' for x in impact['new_use_hypotheses']),'2 hypothetical new-use T contrasts, 0 added to observed main changes')
 gates=load('evidence/role-filter-counterexample.json')['rows']
 for coder,accepted,mismatches in [('a',7,2),('b',8,3)]:
  rr=[r for r in gates if r['coder']==coder]
  check('role gate counts '+coder,len(rr)==18 and sum(r['prior_document_expectation']=='DIRECT_DOCUMENTED' for r in rr)==7 and sum(r['known_documented_case_lost_by_product_gate'] for r in rr)==3 and sum(r['hypothetical_product_only_gate'] for r in rr)==accepted and sum(r['known_mismatch_admitted_by_product_gate'] for r in rr)==mismatches,{'direct':7,'lost':3,'accepted':accepted,'mismatch_accepted':mismatches})
 src=load('sources.json');counted=[r for r in src['sources'] if r['counts_toward_external_minimum']];by=Counter(r['conservative_site_key'] for r in counted)
 req={'id','url','accessed_at_utc','source_type','title','version_or_date','sections_read','confirmed','limits','level','used_in'}
 check('source records all required fields and unique IDs',all(req<=set(r) and all(r[k] for k in req) for r in src['sources']) and len({r['id'] for r in src['sources']})==len(src['sources']),len(src['sources']))
 check('34 sources meet conservative 3-per-site minimum',len(counted)==34 and max(by.values())<=3 and all(r['level'] in ('D1','D2') for r in counted),dict(by))
 check('required source categories',len(src['audit']['software_scheme_families'])==8 and len(src['audit']['other_field_principles'])==4 and len(src['audit']['indexing_empirical_ids'])==5 and len(src['audit']['metric_method_ids'])==7,src['audit'])
 check('failed/snippet readings excluded',len(src['excluded'])==52 and all(not r['id'].startswith(('V','I','MS')) for r in counted),'52 attempt records excluded; prior/candidate/supplement not counted')
 # The first four tables must exactly match prescribed headers and rendered data.
 result=(BASE/'RESULT.md').read_text();tables=[];block=[]
 for line in result.splitlines()+['']:
  if line.startswith('|'):block.append(line)
  elif block:tables.append(block);block=[]
 expected_headers=[T1_HEADERS,T2_HEADERS,T3_HEADERS,T4_HEADERS];expected_rows=[t1_rows(),t2_rows(),[[r[h] for h in T3_HEADERS] for r in load('evidence/vocab-map-data.json')['rows']],[[r[h] for h in T4_HEADERS] for r in load('evidence/claims.json')['rows']]]
 from report_tables import table
 for n,(h,rs) in enumerate(zip(expected_headers,expected_rows),1):
  check('RESULT table '+str(n)+' exact columns and data', '\n'.join(tables[n-1])==table(h,rs),{'columns':h,'rows':len(rs)})
 starts=[result.index('## §'+str(n)) for n in range(1,6)]
 check('RESULT sections ordered',starts==sorted(starts),'§1 tables → §2 answers → §3 analysis → §4 three weaknesses → §5 limits')
 sec4=result[starts[3]:starts[4]]
 check('RESULT exactly three structured weaknesses',len(re.findall(r'^### [123]\. ',sec4,re.M))==3 and all(sec4.count('**'+x+':**')==3 for x in ('무엇이 어긋나거나 약한가','근거 위치','이것이 틀리면 바뀌는 결론','다음 조사 제안')),'three cases, four requested components each')
 check('named inaccessible originals disclosed',all(x in result for x in ('Hooper','Markey','미확인','Cohen')) and (BASE/'evidence/reliability-supplement.json').exists(),'Named classics remain open; source count does not substitute for their reading')
 changed=git('diff','--name-only',SOURCE,'HEAD').splitlines()+git('diff','--name-only').splitlines()+git('ls-files','--others','--exclude-standard').splitlines()
 check('all changed/untracked paths within owned_path',all(x.startswith(OWN) for x in changed),{'changed_path_count':len(set(changed))})
 check('branch ancestry',git('branch','--show-current')=='work/research-af-res-016' and git('merge-base',SOURCE,'HEAD')==SOURCE,{'source_commit':SOURCE,'branch':'work/research-af-res-016'})
 for required in ['SCOPE.md','CODEBOOK.md','SCHEMES.md','AGREEMENT.md','IMPACT.md','VOCAB_MAP.md','RESULT.md','sources.json']:
  check('deliverable exists '+required,(BASE/required).is_file(),required)

if __name__=='__main__':
 error=None
 try:verify()
 except Exception as exc:error=str(exc)
 obj={'study':'AF-RES-016','checked_at_utc':datetime.now(timezone.utc).isoformat(),'head_at_check':git('rev-parse','HEAD'),
 'status':'PASS' if error is None else 'FAIL','check_count':len(CHECKS),'checks':CHECKS,'error':error,
 'scope':'Artifact integrity, required table structure, frozen-order and numerical consistency. Not a statement of human reproducibility or completion of inaccessible-original reading.',
 'known_open_requirements':[{'requirement':'Hooper1965 and Markey1984 named original full-body reading','status':'not completed','reason':'Public original acquisition failed; explicit blocked exception and next first action required in SELF_CHECK/HANDOFF.'}],
 'independent_review':'evidence/verification-audit.md includes independent point/cluster-CI recomputation without reusing analyze.py functions.'}
 (BASE/'evidence/validation.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'status':obj['status'],'checks':len(CHECKS),'error':error},ensure_ascii=False))
 if error:sys.exit(1)
