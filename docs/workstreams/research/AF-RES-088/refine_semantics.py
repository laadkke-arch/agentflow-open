"""Phase-4 scope clarification, prompted by method review; preserves sealed verdicts."""
import csv
import json
from pathlib import Path
P=Path(__file__).resolve().parent

def main():
    rows=[json.loads(x) for x in (P/'revisions.jsonl').read_text().splitlines()]
    for row in rows:
        s=row['semantic_comparison']
        s['text_requirement_change']=s.pop('requirement_change',s.get('text_requirement_change',False))
        s['text_input_information_change']=s.pop('input_information_change',s.get('text_input_information_change',False))
        s['text_solution_clue_added']=s.pop('solution_clue_added',s.get('text_solution_clue_added',False))
        s['full_input_information_change']='unknown' if row['case_id']=='PE1' else ('changed' if s['text_input_information_change'] else 'no_documented_change')
        s['visual_equivalence']='unknown' if row['case_id']=='PE1' else ('not_evaluated' if row['case_id'] in ('PN1','PN2') else 'not_applicable')
        s['full_solution_clue_change']='unknown' if row['case_id']=='PE1' else 'no_documented_change'
        s['clarification_stage']='phase4 method review; no R0/R1 judgment changed'
    (P/'revisions.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
    with (P/'pairs.csv').open() as f: pairs=list(csv.DictReader(f))
    for x in pairs:
        if x['case_id']=='PE1':
            x['counterexample']='text C1/C2 unchanged; old image unavailable; full-input equivalence unknown'
            x['changed_single_axis']='text C1/C2 unchanged; image replacement/embedding; visual semantics unknown'
            x['missing']='R0 A0Wtm.png and image meaning; '+x['missing'] if not x['missing'].startswith('R0 A0Wtm.png') else x['missing']
        elif x['counterexample']=='raw HTML changed with same requirement':
            x['counterexample']='raw HTML changed with same explicit text requirements'
        x['comparison_scope']='explicit text conditions and fixed documentary candidate contract'
        x['full_input_equivalence']='unknown' if x['case_id']=='PE1' else ('changed' if x['case_id']=='JN1' else 'no_documented_change')
    with (P/'pairs.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(pairs[0]),lineterminator='\n');w.writeheader();w.writerows(pairs)
    print('semantic scope clarified; no judgment rows changed')

if __name__=='__main__': main()
