#!/usr/bin/env python3
"""Execute two minimal counterexamples; no candidate package/integration is run."""
import json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
def apply_top_level_replace(doc, ops):
    out=dict(doc)
    for op in ops:
        assert op['op']=='replace' and op['path']=='/title' and 'title' in out
        out['title']=op['value']
    return out
pA={'op':'replace','path':'/title','value':'A'}
pB={'op':'replace','path':'/title','value':'B'}
initial={'title':'0'}
a=apply_top_level_replace(initial,[pA,pB]);b=apply_top_level_replace(initial,[pB,pA])
assert a!=b
admit=[0,1,2,3,4];duration=10;t=4.5
active=sum(start<=t<start+duration for start in admit)
assert min(y-x for x,y in zip(admit,admit[1:]))>=1 and active==5
obj={'study':'AF-RES-016','level':'D3-run: synthetic mathematical traces only',
 'json_patch_order':{'source':'I03 RFC 6902 §3/§4.3; fixed 004 R03','initial':initial,'patches':[pA,pB],
 'replica_a_order':['A','B'],'replica_b_order':['B','A'],'replica_a_result':a,'replica_b_result':b,
 'same_all_patches':True,'converged':False,'scope':'Top-level replace subset only; not a full RFC implementation, network run, or IndexedDB persistence test.'},
 'rate_not_concurrency':{'source':'I02 aiolimiter time-based admission semantics; H hypothesis that rate alone guarantees active≤4',
 'hypothetical_rule':'capacity 1, refill 1 per second; no completion-dependent permit','admission_times_seconds':admit,
 'each_job_duration_seconds':duration,'observation_time_seconds':t,'active_jobs':active,'required_active_max':4,
 'time_rate_rule_satisfied':True,'concurrency_bound_satisfied':False,
 'scope':'A permitted schedule under time-only admission, not execution of aiolimiter or a real asyncio queue. No claim that the original empty proposal asserted this standalone design.'}}
(BASE/'evidence/toy-counterexamples.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'patch_converged':a==b,'rate_admission_active':active},ensure_ascii=False))
