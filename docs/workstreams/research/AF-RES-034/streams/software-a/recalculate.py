"""AF-RES-034 SW-A: published aggregate arithmetic, not study replication."""
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, variance

ROOT = Path(__file__).resolve().parent
def read_rows(name):
    return [json.loads(x) for x in (ROOT / name).read_text().splitlines() if x]

def welch_interval(a, b):
    from scipy.stats import t
    n1, n0 = len(a), len(b)
    v1, v0 = variance(a), variance(b)
    se = math.sqrt(v1/n1 + v0/n0)
    df = (v1/n1 + v0/n0)**2 / ((v1/n1)**2/(n1-1)+(v0/n0)**2/(n0-1))
    delta = mean(a)-mean(b)
    width = t.ppf(.975,df)*se
    return dict(difference=delta, standard_error=se, df=df,
                ci95=[delta-width,delta+width],
                assumption="independent participants, approximately normal arm means; exploratory small n5/5")

def main():
    sources, studies, effects = (read_rows(x) for x in ("sources.jsonl", "studies.jsonl", "effects.jsonl"))
    ids = {x['source_id'] for x in sources}
    assert len(ids) == len(sources)
    assert all(x['source_id'] in ids for x in studies+effects)
    core = {x['study_family'] for x in sources if x['count_minimum']}
    assert core <= {x['study_family'] for x in studies}
    numerical = {}
    for x in effects:
        inp = x.get('input')
        if isinstance(inp,dict) and isinstance(inp.get('treatment'),(float,int)) and isinstance(inp.get('control'),(float,int)):
            a,b=inp['treatment'],inp['control']
            numerical[x['comparison_id']] = dict(difference=a-b,ratio=a/b,relative_pct=100*(a-b)/b)
            if 'ratio' in (x.get('result') or {}):
                assert math.isclose(x['result']['ratio'],a/b,rel_tol=1e-10)
    quality_matrix = [
        [0,1,0,1,0,1,0,1,1,1],
        [0,0,0,0,0,0,0,.5,.5,1],
        [0,0,1,.5,0,0,.5,0,1,1],
        [.5,0,0,1,0,0,0,1,.5,0],
    ]
    example_matrix = [
        [1,1,0,1,0,1,0,1,1,1],
        [1,0,0,1,0,0,1,1,1,0],
        [0,0,1,0,0,0,1,0,1,1],
        [1,0,0,1,0,0,1,1,1,0],
    ]
    treatment_idx,control_idx = [0,2,4,6,9],[1,3,5,7,8]
    totals = [sum(col) for col in zip(*quality_matrix)]
    chosen = [sum(col) for col in zip(*example_matrix)]
    tq,cq=[totals[i] for i in treatment_idx],[totals[i] for i in control_idx]
    te,ce=[chosen[i] for i in treatment_idx],[chosen[i] for i in control_idx]
    assert mean(tq)==1 and mean(cq)==2 and mean(te)==1.8 and mean(ce)==2.4
    complete_counts = [sum(quality_matrix[j][i]==1 for j in range(4) for i in idx) for idx in (treatment_idx,control_idx)]
    assert complete_counts == [4,8]
    report = {
        'checked_utc':datetime.now(timezone.utc).isoformat(),
        'exit_status':0,
        'scope':'published aggregate extraction arithmetic and joins only; not human study execution',
        'input_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ('sources.jsonl','studies.jsonl','effects.jsonl')},
        'counts':{'source_rows':len(sources),'core_families':len(core),'arm_rows':len(studies),'effect_rows':len(effects),'independent_artifact_originals':0},
        'numerical_effects':numerical,
        'exampleoverflow':{'quality_table_5_1':quality_matrix,'example_table_5_3':example_matrix,'participant_total_scores':totals,'participant_selected_examples':chosen,'full_correct_task_counts':complete_counts,'all_assigned_tasks_per_arm':20,'quality_welch95':welch_interval(tq,cq),'selected_examples_welch95':welch_interval(te,ce)},
        'not_verified':['No external raw time dataset','Codelets per-step analysis n missing; no CI despite SD','Assieme graph values not digitized','No delayed rework effects']
    }
    (ROOT/'arithmetic-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'counts':report['counts'],'quality_welch95':report['exampleoverflow']['quality_welch95'],'exit_status':0},ensure_ascii=False))

if __name__ == '__main__':
    main()
