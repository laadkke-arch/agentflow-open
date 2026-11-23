"""AF-RES-054: exact integer arithmetic for declared public margins.

No participant rows are fabricated. `illustration` records are explicitly
constructed arithmetic examples, never recovered study observations.
"""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent


def cell_table(n, q, t, x):
    """Rows quality pass/fail; columns in-time yes/no."""
    cells = {"both": x, "quality_only": q-x,
             "time_only": t-x, "neither": n-q-t+x}
    if any(not isinstance(v, int) or v < 0 for v in cells.values()):
        raise ValueError("invalid integer 2x2 table")
    assert sum(cells.values()) == n
    assert cells["both"] + cells["quality_only"] == q
    assert cells["both"] + cells["time_only"] == t
    return cells


def frechet(n, q, t):
    if not all(isinstance(v, int) for v in (n, q, t)) or not 0 <= q <= n or not 0 <= t <= n:
        raise ValueError("need exact same-population integer margins")
    lower, upper = max(0, q+t-n), min(q, t)
    return {"N": n, "q": q, "t": t, "lower": lower, "upper": upper,
            "lower_table": cell_table(n,q,t,lower),
            "upper_table": cell_table(n,q,t,upper),
            "rate_interval": [str(Fraction(lower,n)), str(Fraction(upper,n))] if n else None}


def contrast(treat, control):
    if not treat["N"] or not control["N"]:
        return {"status": "해당 없음", "reason": "zero conditional denominator"}
    lo = Fraction(treat["lower"],treat["N"])-Fraction(control["upper"],control["N"])
    hi = Fraction(treat["upper"],treat["N"])-Fraction(control["lower"],control["N"])
    return {"lower_fraction": str(lo), "upper_fraction": str(hi),
            "lower_percentage_points": float(100*lo),
            "upper_percentage_points": float(100*hi),
            "interval_kind": "identification range, not a sampling confidence interval",
            "sign": "positive" if lo>0 else "negative" if hi<0 else "nonnegative" if lo==0 and hi>0 else "nonpositive" if hi==0 and lo<0 else "zero" if lo==hi==0 else "not identified"}


def all_task_patterns(margins, intersection):
    """Return a compressed integer witness for four binary tasks, N=12.

    A witness is a feasible synthetic allocation consistent with published
    totals, not a participant ledger and not used to infer individual effects.
    We enumerate triples' bit patterns and complete the fourth using exact
    constraints, retaining only grouped pattern counts.
    """
    n=12
    # Use bounded dynamic programming, pruning on every required total.
    patterns=list(product((0,1), repeat=4))
    target=tuple(margins)+(intersection,)
    memo={}
    def visit(i, remain, residual):
        key=(i,remain,residual)
        if key in memo: return None
        if any(v<0 or v>remain for v in residual): return None
        if i==len(patterns):
            return [] if remain==0 and all(v==0 for v in residual) else None
        p=patterns[i]; vec=p+(int(all(p)),)
        maxk=min([remain]+[residual[j] for j,v in enumerate(vec) if v])
        for k in range(maxk,-1,-1):
            nextres=tuple(residual[j]-k*vec[j] for j in range(5))
            r=visit(i+1,remain-k,nextres)
            if r is not None: return ([{"pass_pattern":"".join(map(str,p)),"count":k}] if k else [])+r
        memo[key]=True
        return None
    witness=visit(0,n,target)
    if witness is not None:
        assert sum(r["count"] for r in witness)==n
        for j,m in enumerate(margins):
            assert sum(r["count"] for r in witness if r["pass_pattern"][j]=="1")==m
        assert sum(r["count"] for r in witness if r["pass_pattern"]=="1111")==intersection
    return witness


def main():
    checks=0
    for n in range(1,26):
        for q in range(n+1):
            for t in range(n+1):
                r=frechet(n,q,t)
                admissible=[x for x in range(n+1) if all(v>=0 for v in (x,q-x,t-x,n-q-t+x))]
                assert min(admissible)==r["lower"] and max(admissible)==r["upper"]
                checks+=1
    illustrative_T=frechet(10,8,9)
    illustrative_C=frechet(10,8,8)
    observed_T={"N":12,"lower":3,"upper":3}
    observed_C={"N":12,"lower":1,"upper":1}
    patterns={}
    for name,margins,reported in [("eXoaDocs",[11,11,3,3],3),("JavaDocs",[10,8,4,1],1)]:
        candidate_low=max(0,sum(margins)-3*12)
        candidate_high=min(margins)
        patterns[name]={"N":12,"task_margins":margins,
            "marginal_only_all_four_interval":[candidate_low,candidate_high],
            "author_reported_all_four_within_40min":reported,
            "valid_witness":all_task_patterns(margins,reported),
            "marginal_only_zero_witness_rejected_by_author_joint_statement":all_task_patterns(margins,0),
            "witness_status":"constructed grouped table, not observed participant records"}
    result={"generated_at_utc":datetime.now(timezone.utc).isoformat(),
        "exact_frechet_cases_verified":checks,
        "table_cell_order":"both,quality_only,time_only,neither",
        "B02_author_joint":{"treatment":observed_T,"control":observed_C,
            "contrast":contrast(observed_T,observed_C),
            "source":"https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf#page=21; section5.3.2",
            "t_envelope_using_only_q_equals_x":{"treatment_range":[3,12],"control_range":[1,12],"status":"weak conditional envelope; does not incorporate Table XII partial submissions or establish a sharp full-publication t range"},
            "weak_constraint_t_extreme_tables":{"treatment_t3":cell_table(12,3,3,3),"treatment_t12":cell_table(12,3,12,3),
                "control_t1":cell_table(12,1,1,1),"control_t12":cell_table(12,1,12,1)},
            "partial_submission_same_clock_sensitivity":{"assumption":"t counts any partial final artifact submitted by40min, and Table XII task passes imply that same-clock submission","treatment_t_range":[11,12],"control_t_range":[10,12],"treatment_lower_t_table":cell_table(12,3,11,3),"control_lower_t_table":cell_table(12,1,10,1),"observed_t":False,"joint_x_unchanged":True}},
        "B02_four_task_consistency":patterns,
        "illustration_only_same_margins_opposite_sign":{"not_a_study_estimate":True,
            "treatment":illustrative_T,"control":illustrative_C,
            "contrast":contrast(illustrative_T,illustrative_C),
            "positive_world":{"T_x":8,"C_x":6,"difference":"1/5"},
            "negative_world":{"T_x":7,"C_x":8,"difference":"-1/10"}},
        "B01_clock_only_envelope":{"N_each":10,"treatment_t":9,"control_t":8,
            "treatment_envelope":[0,9],"control_envelope":[0,8],
            "contrast_conditional_arithmetic_envelope":["-4/5","9/10"],
            "status":"original binary quality criterion undefined; envelope is not an identified original-endpoint estimate"}}
    out=ROOT/'evidence'/'calculation-check.json';out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({"status":"passed","exact_frechet_cases_verified":checks,"output":str(out.relative_to(ROOT)),"B02_contrast":result['B02_author_joint']['contrast']},ensure_ascii=False))


if __name__ == '__main__':
    main()
