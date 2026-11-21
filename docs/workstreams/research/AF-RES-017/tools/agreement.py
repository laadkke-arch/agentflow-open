"""Exact labels, unweighted Cohen kappa, and unchanged raw-response integration."""
import json,hashlib,collections,datetime
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def read(f):return json.loads((P/f).read_text())
def sha(f):return hashlib.sha256((P/f).read_bytes()).hexdigest()
a=read('coding/coder-a.json');b=read('coding/coder-b.json')
A={x['id']:x for x in a['labels']};B={x['id']:x for x in b['labels']}
assert len(A)==len(B)==40 and set(A)==set(B)
axes=['missed_form','missed_contribution','missed_relation','legacy_S1','late_discovery_status']
out={'review_type':'내부 별도 검토; same extracted evidence, fresh context and separately selectable model','A_model':a['model'],'B_model':b['model'],'A_freeze_commit':'70fa1b691601a0cc9fb751db518fd4c5cad06bf8','A_sha256':sha('coding/coder-a.json'),'B_raw_sha256':sha('coding/coder-b.json'),'blind_packet_sha256':sha('coding/blind-packet.json'),'n':40,'axes':{},'limitations':['No human review. Models share provider ecosystem; statistical independence is not established.','Both coders receive the same collector extraction, so this tests coding reproducibility rather than independent source extraction.','A and B raw labels are not adjudicated or changed to improve agreement.'],'diagnostics':b.get('diagnostics',[])}
for k in axes:
    ac=collections.Counter(x[k] for x in A.values());bc=collections.Counter(x[k] for x in B.values());labels=sorted(set(ac)|set(bc));agree=sum(A[i][k]==B[i][k] for i in A);po=agree/40;pe=sum(ac[l]*bc[l] for l in labels)/1600
    conf={l:{r:sum(A[i][k]==l and B[i][k]==r for i in A) for r in labels} for l in labels}
    out['axes'][k]={'agree':agree,'n':40,'agreement':po,'expected_chance_agreement':pe,'cohen_kappa':(po-pe)/(1-pe) if pe!=1 else None,'A_counts':dict(ac),'B_counts':dict(bc),'confusion_matrix_A_rows_B_columns':conf,'disagreements':[{'id':i,'A':A[i][k],'B':B[i][k],'B_reason':B[i]['reason']} for i in sorted(A) if A[i][k]!=B[i][k]]}
for name,kk in [('joint_requested_axes',axes[:3]),('joint_all_axes',axes)]:
    n=sum(all(A[i][k]==B[i][k] for k in kk) for i in A);out[name]={'agree':n,'n':40,'agreement':n/40}
out['dominance_check']={'primary_axes_over_80_percent':[{ 'axis':k,'coder':who,'label':l,'count':n} for k in axes for who,d in [('A',A),('B',B)] for l,n in collections.Counter(x[k] for x in d.values()).items() if n/40>=.8],'prominence_note':'Real historical prominence is unknown40/40 because dated metrics were not collected; synthetic negative and positive evidence checks do not fill that gap.'}
if (P/'coding/positive-diagnostic-response.json').exists():
    extra=read('coding/positive-diagnostic-response.json');diag=b['diagnostics']+extra['diagnostics'];expected={f'D{i:02d}':i>=8 for i in range(1,11)}
    out['discrimination_diagnostics']={'n':10,'met_expected':sum(x['claim_supported']==expected[x['id']] for x in diag),'negative_checks':7,'positive_checks':3,'additional_raw_sha256':sha('coding/positive-diagnostic-response.json'),'results':diag,'limit':'Explicit synthetic sanity checks, not a blinded diagnostic benchmark or validation of missing historical data. No real-case labels were re-coded.'}
(P/'coding/agreement.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
cases=read('cases/CASES.json')
for c in cases:c['coder_b']=B[c['id']]
(P/'cases/CASES.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'axes':{k:{j:v[j] for j in ['agree','n','agreement','cohen_kappa']} for k,v in out['axes'].items()},'joint_requested_axes':out['joint_requested_axes'],'joint_all_axes':out['joint_all_axes'],'dominance':out['dominance_check'],'disagreements':{k:[{'id':x['id'],'A':x['A'],'B':x['B']} for x in v['disagreements']] for k,v in out['axes'].items()}},ensure_ascii=False))
