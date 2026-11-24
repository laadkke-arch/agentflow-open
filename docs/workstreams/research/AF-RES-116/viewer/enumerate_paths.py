#!/usr/bin/env python3
"""Exhaustively enumerate bounded navigation, or replay a deterministic witness.

Outputs are position replay, not observed reader choices or semantic judgements.
Enumerates every allowed action sequence without merging histories: remembered
links and the previous view can differ even at the same document offset.
"""
from collections import deque, Counter
from pathlib import Path
import argparse
import json
import time
from reader import Corpus, MAX_OPENS, actions_for, canonical, digest, owned_path, utc


def enumerate_paths(corpus, start_doc, start_offset=0, max_nodes=200000):
    start = time.perf_counter()
    queue = deque([([], [], set(), 'open', {'doc_id':start_doc,'offset':start_offset,'kind':'initial_open'})])
    nodes, views = [], {}
    per_depth = Counter()
    while queue and len(nodes) < max_nodes:
        history, prior_actions, known, action, target = queue.popleft()
        view = corpus.render(target['doc_id'], target['offset'])
        view_key = digest(canonical({'doc_id':view['doc_id'],'offset':view['offset_start'],'display_sha256':view['display_sha256']}))
        views.setdefault(view_key, view)
        new_history = history + [view]
        new_actions = prior_actions + [action]
        new_known = known | set(view['visible_link_ids'])
        allowed = actions_for(corpus, new_history, new_known) if len(new_history)<MAX_OPENS else {}
        node = {
            'node_id':f'n{len(nodes)+1:06d}','depth':len(new_history),'actions':new_actions,
            'views':[digest(canonical({'doc_id':v['doc_id'],'offset':v['offset_start'],'display_sha256':v['display_sha256']})) for v in new_history],
            'intervals':[{'doc_id':v['doc_id'],'start':v['offset_start'],'end':v['offset_end']} for v in new_history],
            'known_link_ids':sorted(new_known),'allowed_actions':allowed,
            'cumulative_display_codepoints':sum(v['display_codepoints'] for v in new_history),
            'cumulative_display_utf8_bytes':sum(v['display_utf8_bytes'] for v in new_history),
            'terminal':len(new_history)==MAX_OPENS,
        }
        nodes.append(node); per_depth[len(new_history)]+=1
        for next_action, next_target in allowed.items():
            queue.append((new_history,new_actions,new_known,next_action,next_target))
    summary = {
        'method':'exhaustive_offline_position_enumeration','created_utc':utc(),
        'corpus_sha256':corpus.sha256,'start_doc':start_doc,'start_offset':start_offset,
        'max_opens':MAX_OPENS,'max_nodes':max_nodes,'enumeration_complete':not queue,
        'remaining_queue_entries':len(queue),'nodes':len(nodes),'distinct_views':len(views),
        'nodes_by_depth':dict(sorted(per_depth.items())),
        'command_wall_seconds':time.perf_counter()-start,
        'unreachable_claim_allowed_only_if_complete_and_gold_is_sufficient':True,
        'semantic_reachability_judgement':None,'human_or_AI_reader_choices_observed':False,
    }
    return nodes, views, summary


def replay(corpus,start_doc,actions,start_offset=0):
    if not actions or actions[0]!='open' or not 1<=len(actions)<=MAX_OPENS:
        raise ValueError('witness requires 1..3 actions beginning with open')
    history=[];known=set();result=[]
    for step,action in enumerate(actions,1):
        if step==1:
            target={'doc_id':start_doc,'offset':start_offset,'kind':'initial_open'}
        else:
            allowed=actions_for(corpus,history,known)
            if action not in allowed:
                raise ValueError(f'witness step {step} uses a hidden or unavailable action')
            target=allowed[action]
        view=corpus.render(target['doc_id'],target['offset'])
        history.append(view);known|=set(view['visible_link_ids'])
        result.append({'step':step,'action':action,'target':target,'view':view,'allowed_actions_after':actions_for(corpus,history,known) if step<MAX_OPENS else {}})
    return {'method':'deterministic_position_replay','created_utc':utc(),'corpus_sha256':corpus.sha256,'start_doc':start_doc,'actions':actions,'observed_new_reader_choice':False,'steps':result}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--corpus',required=True);p.add_argument('--start-doc',required=True)
    p.add_argument('--start-offset',type=int,default=0);p.add_argument('--out',required=True)
    p.add_argument('--max-nodes',type=int,default=200000);p.add_argument('--witness')
    a=p.parse_args();corpus=Corpus.load(a.corpus);out=owned_path(a.out)
    if a.witness:
        data=replay(corpus,a.start_doc,json.loads(a.witness),a.start_offset)
        out.parent.mkdir(parents=True,exist_ok=True)
        if out.exists(): raise ValueError('refusing to overwrite a witness; use a new path')
        out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({'witness_file':str(out),'steps':len(data['steps']),'method':data['method']}))
    else:
        if a.max_nodes<1: raise ValueError('max-nodes must be positive')
        if out.exists(): raise ValueError('refusing to overwrite enumeration; use a new path')
        nodes,views,summary=enumerate_paths(corpus,a.start_doc,a.start_offset,a.max_nodes)
        out.mkdir(parents=True)
        (out/'paths.jsonl').write_text(''.join(canonical(n)+'\n' for n in nodes))
        (out/'views.jsonl').write_text(''.join(canonical({'view_id':k,**v})+'\n' for k,v in views.items()))
        (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':main()
