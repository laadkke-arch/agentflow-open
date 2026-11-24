#!/usr/bin/env python3
"""Match declared gold intervals against previously enumerated visible intervals.

This is a mechanical coverage analysis, not a semantic gold author or an
independent reader. It never repairs requirements, guesses absent spans, or reads
packets. No corpus/reader/graph input is modified.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import time

from reader import Corpus, OWNED, canonical, owned_path, utc


def sha(raw):return hashlib.sha256(raw).hexdigest()


def read_raw(path):
    path=Path(path);raw=path.read_bytes()
    text=(gzip.decompress(raw) if path.suffix=='.gz' or raw.startswith(b'\x1f\x8b') else raw).decode('utf-8')
    return text,{'path':str(path),'input_sha256':sha(raw),'bytes':len(raw)}


def input_file(directory,name):
    for p in [directory/name,directory/(name+'.gz')]:
        if p.is_file():return p
    raise ValueError(f'missing {name} in {directory}')


def union_intervals(intervals):
    """Return disjoint per-document half-open unions; adjacency is contiguous.

    Never concatenate ranges from different documents or bridge an unread gap.
    Zero-length source views are ignored; malformed input is rejected.
    """
    grouped={}
    for x in intervals:
        did=x.get('doc_id');a=x.get('start');b=x.get('end')
        if not isinstance(did,str) or not did or type(a) is not int or type(b) is not int or a<0 or b<a:
            raise ValueError('invalid visible interval')
        if a==b:continue
        grouped.setdefault(did,[]).append((a,b))
    result={}
    for did,ranges in grouped.items():
        out=[]
        for a,b in sorted(ranges):
            if out and a<=out[-1][1]:out[-1][1]=max(out[-1][1],b)
            else:out.append([a,b])
        result[did]=out
    return dict(sorted(result.items()))


def covered(union,interval):
    return any(a<=interval['start'] and interval['end']<=b for a,b in union.get(interval['doc_id'],[]))


def normalize_interval(item,doc_lengths):
    result=dict(item) if isinstance(item,dict) else {'invalid_input':repr(item)}
    did=result.get('doc_id');a=result.get('start');b=result.get('end')
    if not isinstance(did,str) or not did or type(a) is not int or type(b) is not int or a<0 or b<=a:
        result.update(classification='invalid',reason='require a document identifier and nonempty half-open integer interval')
    elif result.get('outside_corpus') is True or did not in doc_lengths:
        result.update(classification='outside_fixed_corpus',reason=result.get('outside_reason') or ('explicitly outside sealed corpus' if result.get('outside_corpus') else 'document not present in sealed corpus'))
    elif b>doc_lengths[did]:
        result.update(classification='invalid',reason='interval exceeds fixed document length; cannot silently clamp')
    else:result.update(classification='inside_fixed_corpus',reason=None)
    return result


def normalize_alternatives(mode,doc_lengths):
    alternatives=mode.get('alternatives',[])
    if not isinstance(alternatives,list):raise ValueError('mode alternatives must be a list')
    rows=[]
    for index,item in enumerate(alternatives,1):
        if isinstance(item,list):aid=f'alt{index}';intervals=item
        elif isinstance(item,dict):aid=item.get('id',f'alt{index}');intervals=item.get('intervals',[])
        else:raise ValueError('each alternative must be an interval list or {id, intervals}')
        if not isinstance(aid,str) or not aid:raise ValueError('alternative ID must be nonempty')
        if not isinstance(intervals,list):raise ValueError('alternative intervals must be a list')
        normalized=[normalize_interval(x,doc_lengths) for x in intervals]
        invalid=not normalized or any(x['classification']=='invalid' for x in normalized)
        outside=any(x['classification']=='outside_fixed_corpus' for x in normalized)
        rows.append({'id':aid,'intervals':normalized,'invalid':invalid,'contains_outside_corpus':outside,'matchable_in_fixed_corpus':not invalid and not outside,'empty_alternative_is_not_evidence':not normalized})
    if len({x['id'] for x in rows})!=len(rows):raise ValueError('alternative IDs must be unique within a mode')
    return rows


@dataclass
class Graph:
    directory: Path
    summary: dict
    paths: list
    views: dict
    inputs: list


def load_graph(directory,corpus_sha,doc_lengths):
    directory=Path(directory);inputs=[]
    t,r=read_raw(input_file(directory,'summary.json'));summary=json.loads(t);inputs.append(r)
    if summary.get('corpus_sha256')!=corpus_sha:
        raise ValueError(f'graph/corpus SHA mismatch in {directory.name}')
    t,r=read_raw(input_file(directory,'views.jsonl'));inputs.append(r);views={}
    for line in t.splitlines():
        if not line.strip():continue
        v=json.loads(line);key=v['view_id']
        if key in views:raise ValueError('duplicate view ID')
        if v.get('corpus_sha256')!=corpus_sha:raise ValueError('view/corpus SHA mismatch')
        did=v.get('doc_id');a=v.get('offset_start');b=v.get('offset_end')
        if did not in doc_lengths or type(a) is not int or type(b) is not int or not 0<=a<=b<=doc_lengths[did]:
            raise ValueError('view interval outside fixed document')
        if v.get('display_codepoints')!=len(v['display_text']) or v.get('display_sha256')!=sha(v['display_text'].encode()):
            raise ValueError('view display hash/length mismatch')
        # Do not copy document text into coverage results.
        views[key]={k:v[k] for k in ['doc_id','offset_start','offset_end','display_sha256','display_codepoints','display_utf8_bytes']}
    t,r=read_raw(input_file(directory,'paths.jsonl'));inputs.append(r);paths=[];node_ids=set()
    for line in t.splitlines():
        if not line.strip():continue
        p=json.loads(line)
        if p['node_id'] in node_ids:raise ValueError('duplicate path node ID')
        node_ids.add(p['node_id'])
        ids=p['views'];intervals=p['intervals'];depth=p['depth']
        if len(ids)!=depth or len(intervals)!=depth or len(p['actions'])!=depth:
            raise ValueError('path depth/action/view count mismatch')
        for key,x in zip(ids,intervals):
            if key not in views:raise ValueError('path refers to unknown view')
            v=views[key]
            if x!={'doc_id':v['doc_id'],'start':v['offset_start'],'end':v['offset_end']}:
                raise ValueError('path interval differs from fixed visible view')
        p['visible_union']=union_intervals(intervals)
        paths.append(p)
    if summary.get('nodes')!=len(paths) or summary.get('distinct_views')!=len(views):
        raise ValueError('enumeration summary count mismatch')
    return Graph(directory,summary,paths,views,inputs)


def relevant_missing_inputs(case,mode,name):
    result=[]
    for source,items in [('case',case.get('missing_inputs',[])),('mode',mode.get('missing_inputs',[]))]:
        if not isinstance(items,list):raise ValueError('missing_inputs must be a list')
        for item in items:
            if isinstance(item,dict):
                needed=item.get('required_for')
                if needed is not None and (not isinstance(needed,list) or not all(isinstance(x,str) for x in needed)):
                    raise ValueError('required_for must be a list of mode names')
                if needed is not None and name not in needed:continue
            result.append({'scope':source,'input':item})
    return result


def analyze_mode(case,mode_name,mode,graph,doc_lengths):
    if isinstance(mode,list):mode={'alternatives':mode}
    if not isinstance(mode,dict):raise ValueError('mode must be an object or alternative list')
    alternatives=normalize_alternatives(mode,doc_lengths)
    semantic_complete=mode.get('semantic_complete',case.get('semantic_gold_complete')) is True
    missing=relevant_missing_inputs(case,mode,mode_name)
    matches=[]
    for path in graph.paths:
        found=[a['id'] for a in alternatives if a['matchable_in_fixed_corpus'] and all(covered(path['visible_union'],x) for x in a['intervals'])]
        if found:
            matches.append({'case_id':case['case_id'],'mode':mode_name,'node_id':path['node_id'],'depth':path['depth'],'actions':path['actions'],'matching_alternatives':found,'visible_union':path['visible_union'],'view_ids':path['views'],'display_sha256s':[graph.views[v]['display_sha256'] for v in path['views']],'cumulative_display_codepoints':path['cumulative_display_codepoints'],'cumulative_display_utf8_bytes':path['cumulative_display_utf8_bytes'],'method':'fixed_interval_coverage; not an observed reader choice'})
    matches.sort(key=lambda x:(x['depth'],x['node_id']))
    invalid=any(a['invalid'] for a in alternatives)
    outside=[{'alternative_id':a['id'],**x} for a in alternatives for x in a['intervals'] if x['classification']=='outside_fixed_corpus']
    complete=graph.summary.get('enumeration_complete') is True
    if matches:interval_status='reachable'
    elif not alternatives:interval_status='unknown_no_requirements'
    elif invalid:interval_status='unknown_invalid_requirements'
    elif complete:interval_status='unreachable_in_fixed_graph'
    else:interval_status='unknown_incomplete_graph'
    # A complete declared route can establish coverage despite a partial graph.
    # No-match requires exhaustive graph plus a complete semantic requirement set.
    # Missing inputs are epistemic gaps, unlike known outside-corpus requirements.
    if not semantic_complete or missing:semantic_status='unknown'
    elif interval_status=='reachable':semantic_status='reachable_in_fixed_viewer'
    elif interval_status=='unreachable_in_fixed_graph':semantic_status='unreachable_in_fixed_viewer'
    else:semantic_status='unknown'
    if semantic_status=='unreachable_in_fixed_viewer' and outside:
        reason='Complete declared requirements include outside-corpus intervals, or remaining allowed alternatives lack coverage; conclusion is limited to the sealed viewer.'
    elif semantic_status=='unreachable_in_fixed_viewer':
        reason='Every allowed path was enumerated and no complete declared alternative is fully visible.'
    elif semantic_status=='reachable_in_fixed_viewer':
        reason='At least one allowed path covers one complete declared all-interval alternative.'
    else:
        reason='Semantic completeness, missing inputs, invalid requirements, or unfinished enumeration prevent a semantic reachability determination.'
    result={
        'case_id':case['case_id'],'mode':mode_name,'start_doc_id':graph.summary.get('start_doc'),
        'start_offset':graph.summary.get('start_offset',0),'graph_directory':str(graph.directory),
        'graph_complete':complete,'graph_nodes':len(graph.paths),'graph_distinct_views':len(graph.views),
        'case_semantic_gold_complete':case.get('semantic_gold_complete'),'mode_semantic_complete':semantic_complete,
        'missing_inputs':missing,'outside_corpus_intervals':outside,'invalid_alternatives':[a['id'] for a in alternatives if a['invalid']],
        'normalized_alternatives':alternatives,'matching_paths':len(matches),'matching_paths_by_depth':dict(sorted(Counter(x['depth'] for x in matches).items())),
        'earliest_depth':matches[0]['depth'] if matches else None,
        'witness':matches[0] if matches else None,'interval_reachability':interval_status,
        'semantic_reachability':semantic_status,'reason':reason,
        'unrestricted_web_reachability':'not_evaluated','new_reader_choices_observed':False,
        'required_intervals_are_supplied_gold_not_discovered_by_helper':True,
    }
    return result,matches


def case_modes(case):
    if 'modes' in case:
        if not isinstance(case['modes'],dict):raise ValueError('case modes must be an object')
        return case['modes']
    return {name:{'alternatives':case[name+'_alternatives']} for name in ['target','operation','full'] if name+'_alternatives' in case}


def resolve_graph(case,raw_root,corpus_sha,doc_lengths,cache):
    key=case.get('graph') or case['case_id']
    directory=(raw_root/key).resolve()
    if not directory.is_relative_to(raw_root.resolve()):raise ValueError('graph directory must stay below raw-root')
    if not directory.is_dir():
        # Fall back to exact start-doc match, never semantic title matching.
        candidates=[]
        for d in sorted(raw_root.iterdir()):
            if not d.is_dir():continue
            try:t,r=read_raw(input_file(d,'summary.json'));s=json.loads(t)
            except (ValueError,OSError):continue
            if s.get('start_doc')==case.get('start_doc_id') and s.get('start_offset',0)==case.get('start_offset',0):candidates.append(d)
        if len(candidates)!=1:raise ValueError('case needs an exact graph directory or unique fixed start_doc_id')
        directory=candidates[0]
    if directory not in cache:cache[directory]=load_graph(directory,corpus_sha,doc_lengths)
    graph=cache[directory]
    if case.get('start_doc_id') and graph.summary.get('start_doc')!=case['start_doc_id']:
        raise ValueError('case start_doc_id does not match chosen graph')
    if case.get('start_offset',0)!=graph.summary.get('start_offset',0):raise ValueError('case start offset does not match graph')
    return graph


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--requirements',required=True)
    p.add_argument('--corpus',default=str(OWNED/'corpus.json.gz'))
    p.add_argument('--raw-root',default=str(OWNED/'reachability/raw'))
    p.add_argument('--out-dir',required=True)
    args=p.parse_args();started=utc();tic=time.monotonic()
    corpus=Corpus.load(args.corpus);doc_lengths={did:len(d['text']) for did,d in corpus.documents.items()}
    text,requirements_input=read_raw(args.requirements);data=json.loads(text)
    cases=data.get('cases') if isinstance(data,dict) else data
    if not isinstance(cases,list) or not cases:raise ValueError('requirements need a nonempty cases list')
    if isinstance(data,dict) and data.get('corpus_sha256') and data['corpus_sha256']!=corpus.sha256:raise ValueError('declared gold corpus hash mismatch')
    if len({c['case_id'] for c in cases})!=len(cases):raise ValueError('case IDs must be unique')
    out=owned_path(args.out_dir)
    if out.exists():raise ValueError('refusing to overwrite a prior analysis directory; use a new versioned path')
    cache={};summaries=[];allmatches=[];unprovided=[]
    for case in cases:
        graph=resolve_graph(case,Path(args.raw_root).resolve(),corpus.sha256,doc_lengths,cache)
        modes=case_modes(case)
        if not modes:unprovided.append({'case_id':case['case_id'],'status':'unknown_no_modes_supplied'})
        for name,mode in modes.items():
            summary,matches=analyze_mode(case,name,mode,graph,doc_lengths)
            summaries.append(summary);allmatches.extend(matches)
    out.mkdir(parents=True)
    match_bytes=''.join(canonical(x)+'\n' for x in allmatches).encode()
    match_gzip=gzip.compress(match_bytes,mtime=0)
    (out/'matching-paths.jsonl.gz').write_bytes(match_gzip)
    result={'schema':1,'method':'mechanical_gold_interval_coverage','started_utc':started,'finished_utc':utc(),'wall_seconds':time.monotonic()-tic,'corpus_sha256':corpus.sha256,'requirements_input':requirements_input,'graph_inputs':[r for graph in cache.values() for r in graph.inputs],'case_count':len(cases),'mode_count':len(summaries),'matching_path_records':len(allmatches),'matching_paths_file':'matching-paths.jsonl.gz','matching_paths_sha256':sha(match_gzip),'results':summaries,'unprovided_modes':unprovided,'helper_sha256':sha(Path(__file__).read_bytes()),'natural_semantic_claims_without_supplied_gold':False,'source_or_reader_inputs_changed':False,'notes':['Interval containment is documentary exposure coverage, not correctness of a reader answer.','Matching path records include every enumerated covered prefix, including later revisits; inspect depth counts or earliest_depth for minimum opens.','A known required interval outside the sealed corpus is impossible in this viewer, but not proof of absence from the full official web.','missing_inputs or incomplete semantic gold keep semantic reachability unknown even when all currently supplied spans are covered.','Only a graph-complete no-match may support fixed-viewer non-reachability, and only with declared semantic completeness.']}
    (out/'coverage-summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'output_directory':str(out),'case_count':len(cases),'mode_count':len(summaries),'matching_path_records':len(allmatches),'semantic_claims_depend_on_supplied_gold':True}))


if __name__=='__main__':main()
