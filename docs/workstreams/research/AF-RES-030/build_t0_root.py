"""Merge only curated pre-outcome inputs. Never opens downloaded dialogue caches."""
from pathlib import Path
import csv, json, hashlib
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent
PROJECTS = [('matplotlib','matplotlib/matplotlib','M'), ('xarray','pydata/xarray','X'), ('duckdb','duckdb/duckdb','D')]
NOW = datetime.now(timezone.utc).isoformat()
def jl(p): return [json.loads(s) for s in p.read_text().splitlines() if s.strip()]
def dumpj(p, rows): p.write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in rows))
def csvout(p, rows):
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with p.open('w', newline='') as f:
        w=csv.DictWriter(f, keys); w.writeheader(); w.writerows(rows)
def yes(x): return x is True or str(x).lower()=='true'
def first(x,*ks,default=None):
    for k in ks:
        if k in x and x[k] is not None: return x[k]
    return default

initial=[]; question_rows=[]; rawframes=[]
for stream,project,prefix in PROJECTS:
    d=BASE/'streams'/stream
    qs=list(csv.DictReader((d/'questions.csv').open()))
    for x in jl(d/'initial.jsonl'):
        cid=x['case_id']; is_a=x['sample']=='A'
        qcase=[q for q in qs if q['case_id']==cid]
        rank=int(cid.split('B')[1]) if not is_a else None
        info_q=[q for q in qcase if first(q,'question_kind',default='existing_fact') not in ['new_trial_or_candidate_evaluation','new_design_acceptance_request','action_confirmation_not_B']]
        initial.append(dict(case_id=cid, sample='A' if is_a else 'B_screen', project=project,
            root_url=x['root_url'], issue_number=x['issue_number'],
            created_utc=first(x,'created_at','root_created_utc'),
            quarter=first(x,'quarter','selection_window',''),
            author=first(x,'author','root_author'), author_association=x['author_association'],
            maintainer_requester=first(x,'maintainer_requester','supplier_also_requester',default=False),
            goal=first(x,'original_goal','goal'),
            current_root_values=first(x,'known_values','initial_values','root_conditions'),
            initial_location=first(x,'initial_location','initial_fields_source','root_condition_locations'),
            root_body_sha256=first(x,'current_body_sha256','root_sha256','body_sha256'),
            original_grade=x['original_grade'], original_limit=first(x,'original_limit','root_reconstruction'),
            compatibility_grade=first(x,'root_first_compatibility','compatibility_grade','root_compatibility'),
            request_type=x['request_type'], information_score=int(x['information_score']),
            score_basis='current-root proxy; full original unavailable',
            first_strategy=x['first_strategy'], first_response_url=x['first_response_url'],
            first_response_id=x['first_response_id'],
            first_response_utc=first(x,'first_response_utc','first_response_at','first_response_created_utc'),
            first_responder=x['first_responder'], first_response_summary=x['first_response_summary'],
            broad_first_question=bool(qcase), first_information_question=bool(info_q),
            b_screen_rank=rank, b_global_order=(rank-1)*3+{'M':1,'X':2,'D':3}[prefix] if rank else None,
            b_question_eligible=yes(x.get('b_question_eligible')), b_selected=False,
            exposure=x['exposure'], exposure_note=first(x,'exposure_reason','exposure_note'),
            detail_file=f'streams/{stream}/initial.jsonl#{cid}',
            t0_adjudicator=f'{stream} stream reader; root normalization, not independent double coding',
            followups_read_before_seal=False))
    for q in qs:
        question_rows.append(dict(question_id=q['question_id'], case_id=q['case_id'],
            question_comment_id=q['question_comment_id'], question_url=q['question_url'],
            question_utc=first(q,'question_utc','question_at','question_created_utc'),
            questioner=first(q,'question_author','questioner'), variable=q['variable'],
            actual_question_excerpt_ref=f'streams/{stream}/questions.csv#{q["question_id"]}',
            question_kind=first(q,'question_kind',default='existing_fact'),
            value_in_current_root=first(q,'already_in_root','value_in_initial','value_in_current_root'),
            value_in_first_version='미확인; original_grade and partial quote support are separate',
            branch_a=first(q,'predicted_a','predicted_value_a_action','predicted_branch_a'),
            branch_b=first(q,'predicted_b','predicted_value_b_action','predicted_branch_b'),
            predicted_value_a=q.get('value_a','see branch_a'), predicted_value_b=q.get('value_b','see branch_b'),
            frozen_before_author_followup=True, exposure=q.get('exposure'),
            adjudicator=f'{stream} reader', initial_frozen_utc=first(q,'predicted_at_utc','sealed_utc','coded_utc')))
    for j,r in enumerate(csv.DictReader((d/'frame.csv').open()),1):
        cid=r.get('case_id') or (r.get('frame_id') if r.get('frame_id','').startswith(prefix) and r.get('frame_id','') in [x['case_id'] for x in initial] else '')
        rawframes.append(dict(frame_row_id=f'{prefix}-F{j:03}',project=project,case_id=cid,
            issue_number=r['issue_number'],root_url=r['root_url'],
            created_utc=first(r,'created_at','created_utc'),window=first(r,'window','quarter','sample'),
            disposition=first(r,'disposition','eligibility','reason'),
            root_eligible=first(r,'root_eligible','eligibility'),
            reason=r.get('reason'),
            directly_read=first(r,'root_body_displayed','root_directly_read',default='see stream frame; downloaded tail is not read'),
            first_response_read=first(r,'first_response_displayed',default=bool(cid)),
            selected_by_outcome=False, stream_frame=f'streams/{stream}/frame.csv:row{j+1}'))

bpool=sorted([x for x in initial if x['sample']=='B_screen'],key=lambda x:x['b_global_order'])
assert len(bpool)==80
assert [x['b_global_order'] for x in bpool]==list(range(1,81))
bselected=[x for x in bpool if x['b_question_eligible']][:8]
assert [x['case_id'] for x in bselected]==['XB03','DB04','XB06','DB07','XB08','MB09','XB13','XB14']
sel={x['case_id']:i+1 for i,x in enumerate(bselected)}
for x in initial:
    x['b_selected']=x['case_id'] in sel
    x['b_selection_rank']=sel.get(x['case_id'])
    if x['b_selected']: x['sample']='B'
idx={x['case_id']:x for x in initial}
for r in rawframes:
    x=idx.get(r['case_id'],{})
    for k in ['sample','b_screen_rank','b_global_order','b_selected','b_selection_rank','b_question_eligible']:
        r[k]=x.get(k,'')
for q in question_rows: q['sample']=idx[q['case_id']]['sample']

arows=[x for x in initial if x['sample']=='A']; assert len(arows)==24
comparisons=[]
for x in arows:
    if not x['broad_first_question']: continue
    q=x['quarter'].replace('A','')
    cand=[y for y in arows if y['project']==x['project'] and y['quarter'].replace('A','')==q and y['request_type']==x['request_type'] and abs(y['information_score']-x['information_score'])<=1 and y['first_strategy'] in ['directive','conditional_action']]
    ts=lambda s:datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
    cand.sort(key=lambda y:(abs(ts(y['created_utc'])-ts(x['created_utc'])),y['issue_number']))
    y=cand[0] if cand else None
    comparisons.append(dict(pair_id='PAIR-'+x['case_id'],question_case=x['case_id'],
        comparison_case=y['case_id'] if y else '해당 없음',sample='A',
        criteria='same project/quarter/request_type; info_score diff<=1; directive/conditional; nearest creation time',
        all_eligible_candidates=','.join(z['case_id'] for z in cand),
        failure_reason='' if y else 'no same-stratum directive/conditional A case with information difference <=1',
        selection_before_outcomes=True,question_url=x['first_response_url'],
        comparison_url=y['first_response_url'] if y else '',
        question_goal=x['goal'],comparison_goal=y['goal'] if y else '',
        question_info=x['information_score'],comparison_info=y['information_score'] if y else '',
        original_grade_question=x['original_grade'],original_grade_comparison=y['original_grade'] if y else '',
        first_information_question=x['first_information_question'],
        exposure_question=x['exposure'],exposure_comparison=y['exposure'] if y else '',
        outcomes='sealed separately after stage2; not available at selection',
        causal_effect='not identified: different goals and unmeasured difficulty'))

dumpj(BASE/'initial.jsonl',initial)
csvout(BASE/'questions.csv',question_rows)
csvout(BASE/'frame.csv',rawframes)
csvout(BASE/'comparisons.csv',comparisons)
csvout(BASE/'evidence'/'b-selection.csv',[dict(case_id=x['case_id'],project=x['project'],root_url=x['root_url'],b_screen_rank=x['b_screen_rank'],b_global_order=x['b_global_order'],first_question_eligible=x['b_question_eligible'],selected=x['b_selected'],selection_rank=x['b_selection_rank'],first_response_url=x['first_response_url']) for x in bpool])
summary=dict(created_utc=NOW, A=len(arows), B=len(bselected), B_screened=len(bpool),
    B_question_eligible=sum(x['b_question_eligible'] for x in bpool),
    B_selected=[x['case_id'] for x in bselected],
    A_broad_first_question=sum(x['broad_first_question'] for x in arows),
    A_first_information_question=sum(x['first_information_question'] for x in arows),
    A_strategies={k:sum(x['first_strategy']==k for x in arows) for k in sorted(set(x['first_strategy'] for x in arows))},
    question_variables=len(question_rows), metadata_frame_rows=len(rawframes),
    matched_pairs=sum(x['comparison_case']!='해당 없음' for x in comparisons),
    no_matched_pair=sum(x['comparison_case']=='해당 없음' for x in comparisons),
    notes=['first_information_question excludes M03 candidate evaluation; broad first question retains it',
           'reproduction input and prior-action questions remain actual information requests',
           'question quotes are referenced once in stream questions.csv to avoid gratuitous duplication',
           'XB06 first response is >90 days after root; retained in B but separated in timed denominators'])
(BASE/'evidence'/'t0-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
