#!/usr/bin/env python3
"""AF-RES-030: normalize three adjudicated streams without changing sealed inputs.

No network, no product execution. JSONL/CSV research processing only. Source event
objects retain their native fields; normalized flags are explicit rather than
silently treating a missing value as false. Run from any cwd with Python 3.
"""
from pathlib import Path
from datetime import datetime, timedelta, timezone
import csv
import hashlib
import json

P = Path(__file__).resolve().parent
SEAL = '9de54923257d613359348c8ccee2ff8225c8a0d8'

def jl(path):
    return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]

def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def write_jl(path, rows):
    path.write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in rows))

def dt(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00')) if s else None

def tm(e):
    return e.get('utc') or e.get('at') or e.get('created_utc')

def actor(e):
    return e.get('author') or e.get('actor')

def win(e, created, days):
    t=dt(tm(e))
    return bool(t and dt(created) <= t <= dt(created)+timedelta(days=days))

def write_csv(path, rows, columns=None):
    columns = columns or list(rows[0])
    with path.open('w', newline='') as f:
        w=csv.DictWriter(f, fieldnames=columns, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)

def normalize():
    initial={r['case_id']:r for r in jl(P/'initial.jsonl')}
    output=[]
    for stream in ('matplotlib','xarray','duckdb'):
        path=P/'streams'/stream/'chains.jsonl'
        for raw in jl(path):
            cid=raw['case_id']; i=initial[cid]; created=i['created_utc']
            qs=[]; ans=[]
            for e in raw.get('questions',[]):
                info=(e.get('strict_information_question',False) if stream=='matplotlib' else
                      e.get('real_information_request',False) and e.get('target')=='root_author' if stream=='xarray' else
                      e.get('kind')=='information_request')
                q=dict(e)
                q.update(utc=tm(e),actor=actor(e),is_information_request_to_original_author=bool(info),
                    variables=e.get('variables') or [e.get('variable')],
                    root30=win(e,created,30),root90=win(e,created,90),
                    episode_id=e.get('question_episode_id') or e.get('question_id'))
                if cid=='XB14': q['episode_id']='XB14-backend-and-remote'
                qs.append(q)
            qmap={q['question_id']:q for q in qs}
            for e in raw.get('answers',[]):
                q=qmap.get(e.get('question_id'))
                if stream=='matplotlib':
                    strict=bool(q and q.get('same_variable_direct'))
                    rkey=q.get('reply_roundtrip_key') if q else None
                    wait=q.get('answer_wait_hours') if q else None
                    variables=q['variables'] if strict else []
                    is_author=e.get('root_author',False)
                elif stream=='xarray':
                    strict=e.get('strict_same_variable_answer',False)
                    rkey=e.get('roundtrip_key');wait=e.get('wait_hours');variables=e.get('variables',[])
                    is_author=e.get('is_root_author',False)
                else:
                    strict=e.get('same_variable',False) and e.get('same_original_requester',False)
                    rkey=e.get('roundtrip_key');wait=e.get('wait_hours')
                    variables=q['variables'] if strict and q else []
                    is_author=e.get('same_original_requester',False)
                a=dict(e)
                a.update(utc=tm(e),actor=actor(e),is_original_author=bool(is_author),
                    strict_same_variable_existing_answer=bool(strict and q and q['is_information_request_to_original_author']),
                    variables=variables,question_id=e.get('question_id'),roundtrip_key=rkey,wait_hours=wait,
                    root30=win(e,created,30),root90=win(e,created,90),
                    answer_class=e.get('classification') or e.get('category'))
                ans.append(a)
            recs=[]
            for e in raw.get('recommendation_changes',raw.get('recommendations',[])):
                a=e.get('after') if isinstance(e.get('after'),dict) else e
                v=dict(e)
                v.update(utc=tm(a),url=a.get('url') or e.get('after_url') or e.get('url'),actor=actor(a),
                    strict_linked_change=bool(e.get('strict_linked_change',e.get('strict_linked_recommendation_change',False))),
                    root30=win(a,created,30),root90=win(a,created,90))
                recs.append(v)
            executions=[]
            for e in raw.get('executions',[]):
                if stream=='matplotlib':
                    is_new=e.get('new_execution_for_original_goal',False)
                    result=e.get('classification'); same=is_new
                    full=raw.get('full_goal_success_case',False) and result=='success'
                elif stream=='xarray':
                    is_new=e.get('new_execution',False);result=e.get('result');same=e.get('same_original_target',False)
                    full=e.get('full_original_goal') is True
                else:
                    is_new=e.get('kind') in ('new_execution_success','new_execution_failure')
                    result={'new_execution_success':'success','new_execution_failure':'failure'}.get(e.get('kind'),e.get('kind'))
                    same=e.get('same_goal',False)
                    full=cid=='D08' and result=='success'
                v=dict(e)
                v.update(utc=tm(e),actor=actor(e),result_normalized=result,
                    new_original_goal_execution=bool(is_new and same),full_original_goal_success=bool(full),
                    root30=win(e,created,30),root90=win(e,created,90))
                executions.append(v)
            if stream=='matplotlib':
                unknown=[{'fact':raw.get('unknown'),'reason':'원작성자 공개후속의 검증 범위 제한',
                    'last_url':raw.get('last_confirmed_location'),'next_evidence':raw.get('next_material')}]
                comments={f'root{d}':sum(m.get(f'within_root{d}',False) for m in raw['messages']) for d in (30,90)}
            elif stream=='xarray':
                unknown=raw.get('unknowns',[])
                comments={f'root{d}':raw['observation'][f'root{d}_human_comments'] for d in (30,90)}
            else:
                unknown=raw.get('unknowns',[])
                comments={f'root{d}':raw['windows'][f'root{d}_comment_count'] for d in (30,90)}
            r={
                'case_id':cid,'sample':i['sample'],'project':i['project'],'root_url':i['root_url'],
                'created_utc':created,'author':i['author'],'author_association':i['author_association'],
                'maintainer_requester':i['maintainer_requester'],'quarter':i['quarter'],
                'first_strategy':i['first_strategy'],'broad_first_question':i['broad_first_question'],
                'first_information_question':i['first_information_question'],
                'first_response_utc':i['first_response_utc'],'first_responder':i['first_responder'],
                'first_response_url':i['first_response_url'],'original_grade':i['original_grade'],
                'exposure_frozen':i['exposure'],
                'exposure_effective':bool(i['exposure'] or raw.get('exposure_effective',False) or raw.get('exposure_confirmed_after_followup',False)),
                'seal_sha':SEAL,'stream_file':str(path.relative_to(P)),
                'stream_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                'normalizer':'root; three stream adjudications normalized, not blind independent recoding',
                'windows':{f'root{d}_end':(dt(created)+timedelta(days=d)).isoformat() for d in (30,90)},
                'public_snapshot_complete':True,'historical_deleted_content':'미확인: 미표시 삭제의 부재는 입증할 수 없음',
                'questions':qs,'answers':ans,'recommendations':recs,'executions':executions,
                'provider_implementations':raw.get('provider_implementations',raw.get('supplier_implementations',[])),
                'other_events':raw.get('other_events',[]),'late_history':raw.get('late_history',[]),
                'unknowns':unknown,'observed_comment_counts':comments,
                'direct_support':raw.get('technical_sources',raw.get('provider_source_ids',[])),
                'unmeasured_costs':'미확인: 클릭·읽기 시간·대신할 노동에 대한 독립 로그 없음',
            }
            for d in (30,90):
                w=f'root{d}'
                q=[x for x in qs if x[w] and x['is_information_request_to_original_author']]
                qids={x['question_id'] for x in q}
                a=[x for x in ans if x[w] and x['is_original_author'] and x['question_id'] in qids]
                direct=[x for x in a if x['strict_same_variable_existing_answer']]
                ex=[x for x in executions if x[w] and x['new_original_goal_execution']]
                strict_keys={x['roundtrip_key'] for x in direct if x['roundtrip_key']}
                reply_keys={x['roundtrip_key'] for x in a if x['roundtrip_key']}
                answered={x['question_id'] for x in a}
                direct_vars={(qmap[x['question_id']]['episode_id'],v) for x in direct for v in x['variables']}
                metrics={
                    'information_question':bool(q),'question_utterances':len({x['comment_id'] for x in q}),
                    'question_episodes':len({x['episode_id'] for x in q}),
                    'question_variables':len({(x['episode_id'],v) for x in q for v in x['variables']}),
                    'same_variable_answer':bool(direct),'strict_answer_variable_count':len(direct_vars),
                    'strict_answer_roundtrips':len(strict_keys),'any_author_reply_roundtrips':len(reply_keys),
                    'strict_roundtrip_keys':sorted(strict_keys),'reply_roundtrip_keys':sorted(reply_keys),
                    'linked_recommendation_change':any(x[w] and x['strict_linked_change'] for x in recs),
                    'new_execution_success':any(x['result_normalized']=='success' for x in ex),
                    'new_execution_failure':any(x['result_normalized']=='failure' for x in ex),
                    'full_goal_success':any(x['result_normalized']=='success' and x['full_original_goal_success'] for x in ex),
                    'unanswered_question_utterances':len({x['comment_id'] for x in q if x['question_id'] not in answered}),
                    'no_author_reply_to_any_information_question':bool(q) and not bool(a),
                    'strict_wait_hours':[x['wait_hours'] for x in direct if x.get('wait_hours') is not None],
                    'comment_count':comments[w],
                }
                metrics['chain_success']=metrics['same_variable_answer'] and metrics['linked_recommendation_change'] and metrics['new_execution_success']
                r[w]=metrics
            output.append(r)
    output.sort(key=lambda r:(r['sample'], {'matplotlib/matplotlib':0,'pydata/xarray':1,'duckdb/duckdb':2}[r['project']], r['created_utc']))
    return output

def aggregate(rows):
    out={'n':len(rows),'case_ids':[r['case_id'] for r in rows]}
    flags=('information_question','same_variable_answer','linked_recommendation_change','new_execution_success','new_execution_failure','full_goal_success','chain_success','no_author_reply_to_any_information_question')
    numeric=('question_utterances','question_episodes','question_variables','strict_answer_variable_count','strict_answer_roundtrips','any_author_reply_roundtrips','unanswered_question_utterances','comment_count')
    for flag in flags:
        out[flag]=sum(r['root30'][flag] for r in rows)
        out[flag+'_ids']=[r['case_id'] for r in rows if r['root30'][flag]]
    for n in numeric:out[n]=sum(r['root30'][n] for r in rows)
    waits=[v for r in rows for v in r['root30']['strict_wait_hours']]
    out['strict_wait_min_hours']=min(waits) if waits else None
    out['strict_wait_max_hours']=max(waits) if waits else None
    out['first_information_question']=sum(r['first_information_question'] for r in rows)
    out['first_broad_question']=sum(r['broad_first_question'] for r in rows)
    out['original_whole_confirmed']=sum(r['original_grade']=='O' for r in rows)
    out['current_overlap_cases']=[r['case_id'] for r in rows if r['case_id'] in ['M01','XB03','DB07']]
    out['exposed_cases']=[r['case_id'] for r in rows if r['exposure_effective']]
    out['root90_comment_count']=sum(r['root90']['comment_count'] for r in rows)
    out['root90_same_metrics']=all(all(r['root30'][k]==r['root90'][k] for k in flags) for r in rows)
    out['unique_requester_handles']=len({r['author'] for r in rows})
    out['unique_first_responder_handles']=len({r['first_responder'] for r in rows if r['first_responder']})
    return out

def main():
    rows=normalize()
    write_jl(P/'chains.jsonl',rows)
    flat=[]
    for r in rows:
        a={k:r[k] for k in ['case_id','sample','project','created_utc','author','maintainer_requester','first_strategy','first_information_question','original_grade','exposure_frozen','exposure_effective']}
        a.update({k:v for k,v in r['root30'].items() if not isinstance(v,(list,dict))})
        flat.append(a)
    write_csv(P/'analysis.csv',flat)
    groups={}
    for sample in ('A','B'):
        base=[r for r in rows if r['sample']==sample]
        groups[sample+'_all']=aggregate(base)
        groups[sample+'_information_question']=aggregate([r for r in base if r['root30']['information_question']])
        groups[sample+'_direct_answer']=aggregate([r for r in base if r['root30']['same_variable_answer']])
        groups[sample+'_same_goal_execution']=aggregate([r for r in base if r['root30']['new_execution_success'] or r['root30']['new_execution_failure']])
        groups[sample+'_same_goal_execution_success']=aggregate([r for r in base if r['root30']['new_execution_success']])
        groups[sample+'_unexposed']=aggregate([r for r in base if not r['exposure_effective']])
        groups[sample+'_nonmaintainer']=aggregate([r for r in base if not r['maintainer_requester']])
        seen=set();dedup=[]
        for r in sorted(base,key=lambda x:x['created_utc']):
            if r['author'] not in seen:dedup.append(r);seen.add(r['author'])
        groups[sample+'_first_per_requester_handle']=aggregate(dedup)
        groups[sample+'_whole_original']=aggregate([r for r in base if r['original_grade']=='O'])
    dump(P/'evidence/denominators.json',{'seal_sha':SEAL,'unit':'root/case unless variable, utterance, episode, roundtrip or comment explicitly named','window':'root+30days primary; root+90days separate','groups':groups})
    sens=[]
    for k,g in groups.items():
        if k.endswith(('_unexposed','_nonmaintainer','_first_per_requester_handle','_whole_original')):
            sens.append({'subset':k,'cases':g['n'],'information_question':g['information_question'],
                'direct_answer':g['same_variable_answer'],'strict_change':g['linked_recommendation_change'],
                'execution_success':g['new_execution_success'],'execution_failure':g['new_execution_failure'],
                'full_goal_success':g['full_goal_success'],'case_ids':','.join(g['case_ids']),
                'zero_denominator':'해당 없음' if not g['n'] else ''})
    write_csv(P/'sensitivity.csv',sens)
    variable_rows=[]
    for r in rows:
        for q in r['questions']:
            for variable in q['variables']:
                variable_rows.append({'case_id':r['case_id'],'sample':r['sample'],'question_id':q['question_id'],
                    'episode_id':q['episode_id'],'comment_id':q['comment_id'],'question_url':q['url'],'question_utc':q['utc'],
                    'variable':variable,'information_to_original_author':q['is_information_request_to_original_author'],
                    'root30':q['root30'],'root90':q['root90'],
                    'prediction_source':'questions.csv@'+SEAL if q.get('presealed') or q.get('predictions_source') or q.get('predictions_sealed_before_outcome') else '후발 질문; 사전 봉인 예상 분기 없음',
                    'detail_source':r['stream_file']+'#'+q['question_id']})
    write_csv(P/'question-audit.csv',variable_rows)
    print(json.dumps({k: {a:g[a] for a in ['n','information_question','same_variable_answer','linked_recommendation_change','new_execution_success','new_execution_failure','full_goal_success','strict_answer_variable_count','strict_answer_roundtrips','any_author_reply_roundtrips','strict_wait_min_hours','strict_wait_max_hours','comment_count','root90_comment_count']} for k,g in groups.items() if k in ['A_all','B_all']},ensure_ascii=False))

if __name__=='__main__':main()
