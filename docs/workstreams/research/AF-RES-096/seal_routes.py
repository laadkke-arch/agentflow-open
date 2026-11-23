"""Assemble the pre-outcome records from original route rows, without outcomes."""
from pathlib import Path
import csv, datetime, hashlib, json

ROOT=Path(__file__).resolve().parent

def jl(path):
    return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]

def main():
    protocol=json.loads((ROOT/'protocol.json').read_text())
    search=jl(ROOT/'evidence/search-events.jsonl')
    combined=list(search); pairs=[]; route_rows=[]; failures=[]
    for case in protocol['cases']:
        results={}
        for route in case['route_order']:
            folder=ROOT/'evidence/routes'/f'{case["case_id"]}-{route}'
            j=json.loads((folder/'judgment.json').read_text())
            ev=jl(folder/'access.jsonl');combined.extend(ev)
            exp=json.loads((folder/'exposure.json').read_text())
            opened=[r for r in ev if r['event']=='body_attempt' and r['status']=='success']
            attempts=[r for r in ev if r['event']=='body_attempt']
            exposed={r['file_id'] for r in exp['slots'] if r['file_id']}
            successful={r['file_id'] for r in opened}
            returned={r['file_id'] for r in j['returned_sources']}
            used=set(j.get('used_file_ids',[]))
            invalid=[]
            if len(attempts)>4:invalid.append('attempt_budget_exceeded')
            if len(j['returned_sources'])>2:invalid.append('return_link_budget_exceeded')
            if not successful<=exposed:invalid.append('unexposed_file_opened')
            if not used<=successful or not returned<=successful:invalid.append('unopened_evidence_used')
            if j['judgment']=='완결' and not used<=returned:invalid.append('complete_depends_on_nonreturned_source')
            actual_searches=sum(e['event']=='search' and e['case_id']==case['case_id'] and e['route']==route for e in search)
            if actual_searches!=2:invalid.append('search_budget_not_two')
            if [r['slot'] for r in attempts]!=[s['slot'] for s in exp['slots'] if not s['empty']]:invalid.append('open_order_or_fixed_four_policy_changed')
            adjacent={s['file_id'] for s in exp['slots'] if s.get('role')=='adjacent'}
            rr={'case_id':case['case_id'],'route':route,'searches':actual_searches,
                'attempts':len(attempts),'failures':sum(r['status']!='success' for r in attempts),
                'remaining_body_budget':4-len(attempts),'judgment':j['judgment'],
                'returned_file_ids':sorted(returned),'used_file_ids':sorted(used),
                'exposed_file_ids':[s['file_id'] for s in exp['slots']],
                'adjacent_exposed_file_ids':sorted(adjacent),
                'adjacent_opened_file_ids':sorted(adjacent&successful),
                'adjacent_returned_file_ids':sorted(adjacent&returned),
                'first_access_utc':attempts[0]['started_utc'] if attempts else None,
                'last_access_utc':attempts[-1]['finished_utc'] if attempts else None,
                'judgment_utc':j['read_completed_utc'],'comparison_faults':invalid}
            route_rows.append(rr);results[route]=rr
            if invalid:failures.append({'case_id':case['case_id'],'route':route,'faults':invalid})
        a,b=results['A'],results['B']
        ac=a['judgment']=='완결';bc=b['judgment']=='완결'
        pair='양쪽' if ac and bc else 'A만' if ac else 'B만' if bc else '어느 쪽도 아님'
        faults=a['comparison_faults']+b['comparison_faults']
        pairs.append({'case_id':case['case_id'],'question_id':case['question_id'],'stratum':case['stratum'],
                      'route_order':';'.join(case['route_order']),'frozen_A':a['judgment'],'frozen_B':b['judgment'],
                      'frozen_pair':pair,'strict_pair':'비교불가' if faults else pair,
                      'strict_comparable':not faults,'comparison_faults':';'.join(faults),
                      'A_attempts':a['attempts'],'B_attempts':b['attempts'],
                      'B_adjacent_exposed':bool(b['adjacent_exposed_file_ids']),
                      'B_adjacent_opened':bool(b['adjacent_opened_file_ids']),
                      'B_adjacent_returned':bool(b['adjacent_returned_file_ids']),
                      'B_completeness_differs_from_A':ac!=bc,'r0_url':case['r0_url'],
                      'limitation':'same tag researcher crossover; documentary judgment under comparison versions; original user runtime not verified'})
    combined.sort(key=lambda e:(e.get('started_utc') or e.get('created_utc') or e.get('utc') or '',e['case_id'],e['route']))
    (ROOT/'exposure.jsonl').write_text(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in combined))
    with (ROOT/'pairs.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(pairs[0]));w.writeheader();w.writerows(pairs)
    counts={}
    for group in ['all','boundary','control']:
        rows=[r for r in pairs if group=='all' or r['stratum']==group]
        counts[group]={k:sum(r['strict_pair']==k for r in rows) for k in ['A만','B만','양쪽','어느 쪽도 아님','비교불가']}
        counts[group]['planned_pairs']=len(rows)
        counts[group]['comparable_pairs']=sum(r['strict_comparable'] for r in rows)
    discordant=sum(r['strict_pair'] in ['A만','B만'] for r in pairs)
    obj={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'phase':'before public outcomes; remote seal2 pending','cases':len(pairs),'routes':len(route_rows),
         'searches':sum(r['searches'] for r in route_rows),'body_attempts':sum(r['attempts'] for r in route_rows),
         'failed_body_attempts':sum(r['failures'] for r in route_rows),'counts':counts,
         'B_boundary_adjacent_exposed':sum(r['B_adjacent_exposed'] for r in pairs),
         'B_boundary_adjacent_opened':sum(r['B_adjacent_opened'] for r in pairs),
         'B_boundary_adjacent_returned':sum(r['B_adjacent_returned'] for r in pairs),
         'discordant_pairs':discordant,'B_win_fraction_among_discordant':
         sum(r['strict_pair']=='B만' for r in pairs)/discordant if discordant else '산출 불가 (분모 0)',
         'route_rows':route_rows,'faults':failures}
    (ROOT/'evidence/pre-outcome-metrics.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in obj.items() if k!='route_rows'},ensure_ascii=False,indent=2))
    raise SystemExit(1 if failures else 0)

if __name__=='__main__':main()
