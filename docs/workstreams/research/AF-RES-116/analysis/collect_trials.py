#!/usr/bin/env python3
"""Export bounded-reader observations and audit protocol/citation integrity.

No semantic grading, answer reconstruction, or packet changes. Missing sessions
are unobserved planned positions, not failures or zero-success observations.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from datetime import datetime
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import sys

OWN=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(OWN/'viewer'))
from reader import Corpus, actions_for, read_events, canonical, utc

MAX_OPENS=3
DISPLAY_LIMIT=1500


def digest(raw):return hashlib.sha256(raw if isinstance(raw,bytes) else raw.encode()).hexdigest()
def offset_time(value):return datetime.fromisoformat(value.replace('Z','+00:00'))
def seconds(a,b):
    if not a or not b:return None
    try:return (offset_time(b)-offset_time(a)).total_seconds()
    except (TypeError,ValueError):return None
def relative(path):
    path=Path(path).resolve()
    return str(path.relative_to(OWN)) if path.is_relative_to(OWN) else str(path)
def read_jsonl(path):return [json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]
def serial_lines(rows):return ''.join(canonical(x)+'\n' for x in rows)


def visible_unions(views):
    grouped=defaultdict(list)
    for v in views:
        a=v.get('offset_start');b=v.get('offset_end');did=v.get('doc_id')
        if isinstance(did,str) and type(a) is int and type(b) is int and 0<=a<b:
            grouped[did].append((a,b))
    merged={}
    for did,spans in grouped.items():
        out=[]
        for a,b in sorted(spans):
            if out and a<=out[-1][1]:out[-1][1]=max(out[-1][1],b)
            else:out.append([a,b])
        merged[did]=out
    return dict(sorted(merged.items()))


def quote_matches(citation,views,documents):
    """Exact source matching is limited to contiguous cumulatively seen spans.

    A citation may use a previous opening, but cannot stitch across an unread
    gap, across documents, or across the source/body vs viewer-navigation divide.
    Optional whitespace-normalized matches are diagnostic, not exact support.
    """
    result={'citation':citation,'text_visible':False,'exact_source_visible':False,'exact_display_visible':False,'doc_id_matches':None,'claimed_interval_correct':None,'strict_supported':False,'match_status':'invalid_citation','source_matches':[],'other_document_matches':[],'normalization_only_matches':[],'display_matches':[]}
    if not isinstance(citation,dict) or not isinstance(citation.get('quote'),str):return result
    quote=citation['quote'];claimed=citation.get('doc_id')
    if not quote.strip():result['match_status']='empty_quote';return result
    union=visible_unions(views)
    def search(did,spans,normal=False):
        if did not in documents:return []
        text=documents[did]['text'];found=[]
        for a,b in spans:
            segment=text[a:b]
            if normal:
                q=re.sub(r'\s+',' ',quote).strip();s=re.sub(r'\s+',' ',segment).strip()
                if q and q in s:found.append({'doc_id':did,'visible_interval':[a,b],'offset_exact':False})
            else:
                pos=segment.find(quote)
                while pos>=0:
                    found.append({'doc_id':did,'start':a+pos,'end':a+pos+len(quote),'visible_interval':[a,b]})
                    pos=segment.find(quote,pos+1)
        return found
    for did,spans in union.items():
        found=search(did,spans)
        if claimed is None or claimed==did:result['source_matches'].extend(found)
        else:result['other_document_matches'].extend(found)
        if (claimed is None or claimed==did) and not found:result['normalization_only_matches'].extend(search(did,spans,True))
    for index,v in enumerate(views,1):
        if claimed is not None and claimed!=v.get('doc_id'):continue
        display=v.get('display_text','')
        if isinstance(display,str) and quote in display:
            result['display_matches'].append({'opening':index,'doc_id':v.get('doc_id'),'display_sha256':v.get('display_sha256'),'display_offset':display.index(quote)})
    result['exact_source_visible']=bool(result['source_matches'])
    result['exact_display_visible']=bool(result['display_matches'])
    result['text_visible']=result['exact_source_visible'] or result['exact_display_visible']
    result['doc_id_matches']=bool(result['text_visible']) if claimed is not None else None
    if 'start' in citation or 'end' in citation:
        a=citation.get('start');b=citation.get('end')
        result['claimed_interval_correct']=False
        if type(a) is int and type(b) is int and a<b:
            candidates=[claimed] if isinstance(claimed,str) else list(union)
            for did in candidates:
                if did in documents and 0<=a<b<=len(documents[did]['text']):
                    inside=any(lo<=a and b<=hi for lo,hi in union.get(did,[]))
                    if inside and documents[did]['text'][a:b]==quote:result['claimed_interval_correct']=True
    result['strict_supported']=result['exact_source_visible'] and result['claimed_interval_correct'] is not False
    if result['strict_supported']:result['match_status']='exact_visible_source'
    elif result['exact_source_visible']:result['match_status']='exact_visible_source_wrong_claimed_offset'
    elif result['exact_display_visible']:result['match_status']='viewer_display_only_not_source_proof'
    elif result['other_document_matches']:result['match_status']='quote_visible_only_in_different_document'
    elif result['normalization_only_matches']:result['match_status']='whitespace_normalization_only'
    else:result['match_status']='not_in_cumulative_visible_intervals'
    result['semantic_support_or_correctness']='not_evaluated'
    return result


def load_log(path):
    raw=Path(path).read_bytes();errors=[];text=None;events=[]
    try:text=raw.decode('utf-8')
    except UnicodeDecodeError as exc:errors.append({'code':'invalid_utf8','detail':str(exc)})
    chain_valid=False
    if text is not None:
        try:events=read_events(io.StringIO(text));chain_valid=True
        except (ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:
            errors.append({'code':'hash_chain_or_json_invalid','detail':str(exc)})
            # Preserve decodable raw observations, but mark them unverified.
            for line_number,line in enumerate(text.splitlines(),1):
                try:
                    item=json.loads(line)
                    if isinstance(item,dict):events.append(item)
                    else:errors.append({'code':'non_object_event','line':line_number})
                except json.JSONDecodeError:errors.append({'code':'unparseable_event','line':line_number})
    return events,chain_valid,errors,{'path':relative(path),'sha256':digest(raw),'bytes':len(raw)}


def audit_session(packet,events,chain_valid,initial_errors,corpus,engine_sha):
    sid=packet['packet_id'];errors=list(initial_errors);warnings=[];exposures=[];answers={};choices={};pending=None;finish=None;init=None;known=set();history=[];previous_time=None
    def fail(code,event=None,detail=None):
        item={'code':code}
        if event is not None:item['seq']=event.get('seq')
        if detail is not None:item['detail']=detail
        errors.append(item)
    if events and events[0].get('event')!='init':fail('first_event_not_init',events[0])
    for e in events:
        kind=e.get('event');at=e.get('at_utc')
        try:
            parsed=offset_time(at)
            if parsed.tzinfo is None:raise ValueError('timezone missing')
            if previous_time and parsed<previous_time:fail('event_utc_not_monotonic',e)
            previous_time=parsed
        except (ValueError,TypeError,AttributeError):fail('invalid_event_utc',e)
        if e.get('session')!=sid:fail('event_session_mismatch',e)
        if kind=='init':
            if init is not None:fail('duplicate_init',e)
            init=e
            for field,expected in [('corpus_sha256',corpus.sha256),('engine_sha256',engine_sha),('start_doc',packet.get('start_doc_id')),('max_opens',MAX_OPENS),('max_display_codepoints',DISPLAY_LIMIT)]:
                if e.get(field)!=expected:fail('init_pin_mismatch',e,{'field':field,'expected':expected,'actual':e.get(field)})
            if e.get('start_offset',0)!=0:fail('unexpected_start_offset',e)
        elif kind=='rejected_action':
            continue  # A denied request itself does not expose a document.
        elif kind=='choice':
            if finish is not None:fail('accepted_choice_after_finish',e)
            if init is None:fail('choice_before_init',e)
            if pending is not None:fail('choice_without_consuming_prior_choice',e)
            step=len(exposures)+1
            if e.get('next_step')!=step:fail('choice_step_mismatch',e)
            if step>MAX_OPENS:fail('choice_exceeds_budget',e)
            prior=answers.get(step-1)
            if step>1 and prior is None:fail('next_choice_before_previous_answer',e)
            if e.get('previous_answer_event_sha256')!=(prior.get('event_sha256') if prior else None):fail('choice_previous_answer_hash_mismatch',e)
            if not isinstance(e.get('selection_reason'),str) or not e['selection_reason'].strip():fail('choice_reason_missing',e)
            action=e.get('action');target=e.get('target',{})
            if step==1:
                if action!='open':fail('first_choice_not_open',e)
                if target.get('doc_id')!=packet.get('start_doc_id') or target.get('offset')!=0:fail('initial_target_mismatch',e)
            else:
                allowed=actions_for(corpus,history,known) if history else {}
                if action not in allowed:fail('chosen_action_not_previously_visible_or_available',e)
                elif target!=allowed[action]:fail('choice_target_mismatch',e)
            pending=e;choices[e.get('event_sha256',f'bad-choice-{len(choices)}')]=e
        elif kind=='exposure':
            if finish is not None:fail('exposure_after_finish',e)
            step=len(exposures)+1
            if e.get('step')!=step:fail('exposure_step_mismatch',e)
            if step>MAX_OPENS:fail('exposure_exceeds_budget',e)
            if pending is None:fail('exposure_without_choice',e)
            elif e.get('choice_event_sha256')!=pending.get('event_sha256') or e.get('action')!=pending.get('action'):fail('exposure_choice_link_mismatch',e)
            v=e.get('view',{})
            if not isinstance(v,dict):fail('view_not_object',e);v={}
            if pending and (v.get('doc_id')!=pending.get('target',{}).get('doc_id') or v.get('offset_start')!=pending.get('target',{}).get('offset')):fail('view_does_not_match_choice_target',e)
            try:
                expected=corpus.render(v.get('doc_id'),v.get('offset_start'))
                if expected!=v:
                    mismatch=[k for k in set(expected)|set(v) if expected.get(k)!=v.get(k)]
                    fail('view_differs_from_frozen_renderer',e,sorted(mismatch))
            except (ValueError,TypeError,KeyError):fail('view_cannot_be_reproduced',e)
            display=v.get('display_text','')
            if not isinstance(display,str):fail('display_not_string',e);display=''
            if len(display)>DISPLAY_LIMIT:fail('display_exceeds_1500',e)
            if v.get('display_codepoints')!=len(display) or v.get('display_utf8_bytes')!=len(display.encode()):fail('display_character_or_byte_count_mismatch',e)
            if v.get('display_sha256')!=digest(display):fail('display_hash_mismatch',e)
            for total,one,two in [('display_codepoints','content_codepoints','total_navigation_codepoints'),('display_utf8_bytes','content_utf8_bytes','total_navigation_utf8_bytes')]:
                if not all(type(v.get(k)) is int for k in [total,one,two]) or v.get(one,0)+v.get(two,0)!=v.get(total):fail('disjoint_body_navigation_sum_mismatch',e,total)
            exposures.append(e);history.append(v);known.update(v.get('visible_link_ids',[]))
            if e.get('known_link_ids_after')!=sorted(known):fail('known_links_accumulation_mismatch',e)
            allowed=actions_for(corpus,history,known) if step<MAX_OPENS else {}
            if e.get('allowed_actions_after')!=allowed:fail('allowed_actions_after_mismatch',e)
            for field,viewfield in [('cumulative_display_codepoints','display_codepoints'),('cumulative_display_utf8_bytes','display_utf8_bytes')]:
                total=sum(x.get('view',{}).get(viewfield,0) for x in exposures)
                if e.get(field)!=total:fail('cumulative_cost_mismatch',e,field)
            pending=None
        elif kind=='answer':
            if finish is not None:fail('answer_after_finish',e)
            step=e.get('step')
            if type(step) is not int or step!=len(exposures) or not exposures:fail('answer_step_mismatch',e)
            if step in answers:fail('duplicate_stage_answer',e)
            if exposures and e.get('exposure_event_sha256')!=exposures[-1].get('event_sha256'):fail('answer_exposure_hash_mismatch',e)
            if e.get('recorded_before_next_open') is not True:fail('answer_precedes_next_flag_missing',e)
            answer=e.get('answer',{})
            if not isinstance(answer,dict):fail('answer_not_object',e);answer={}
            if not all(isinstance(answer.get(k),str) and answer[k].strip() for k in ['operation','preservation','exceptions','disposition']):fail('answer_required_fields_missing',e)
            if not isinstance(answer.get('citations',[]),list):fail('answer_citations_not_list',e)
            if type(step) is int:answers[step]=e
        elif kind=='finish':
            if finish is not None:fail('duplicate_finish',e)
            if pending is not None:fail('finish_with_pending_choice',e)
            n=len(exposures);last=answers.get(n)
            if n==0 or last is None:fail('finish_before_stage_answer',e)
            if e.get('observed_steps')!=n:fail('finish_observed_count_mismatch',e)
            if e.get('early_stop')!=(n<MAX_OPENS):fail('finish_early_stop_mismatch',e)
            if e.get('unobserved_early_stop_positions')!=MAX_OPENS-n:fail('finish_unused_positions_mismatch',e)
            if e.get('final_answer_event_sha256')!=(last.get('event_sha256') if last else None):fail('finish_answer_hash_mismatch',e)
            finish=e
        else:fail('unknown_event_type',e,kind)
    if events and init is None:fail('missing_init')
    if pending is not None:warnings.append('choice_recorded_but_no_following_exposure_yet')
    if exposures and len(exposures) not in answers:warnings.append('last_exposure_has_no_stage_answer_yet')
    if events and finish is None:warnings.append('session_not_finished_at_collection')
    return {'session':sid,'chain_valid':chain_valid,'audit_valid':chain_valid and not errors,'errors':errors,'warnings':warnings,'init':init,'exposures':exposures,'answers':answers,'choices':choices,'finish':finish,'events':events}


def packet_errors(packet,corpus_sha):
    errors=[]
    if packet.get('corp_sha256',packet.get('corpus_sha256'))!=corpus_sha:errors.append({'code':'packet_corpus_pin_mismatch','packet_id':packet.get('packet_id')})
    for text,chars,bytes_ in [('hint','hint_codepoints','hint_utf8_bytes'),('full_packet_text','packet_codepoints','packet_utf8_bytes'),('common_request','request_codepoints','request_utf8_bytes')]:
        s=packet.get(text)
        if isinstance(s,str):
            if packet.get(chars)!=len(s) or packet.get(bytes_)!=len(s.encode()):errors.append({'code':'packet_text_cost_mismatch','packet_id':packet.get('packet_id'),'text_field':text})
    return errors


def collect(packets,readers,corpus,engine_sha,expected_packets=18):
    trails=[];slots=[];citation_rows=[];sessions=[];errors=[];inputs=[];bycase=defaultdict(dict)
    ids=[p.get('packet_id') for p in packets]
    if len(ids)!=len(set(ids)) or not all(isinstance(x,str) and re.fullmatch(r'[A-Za-z0-9_-]+',x) for x in ids):raise ValueError('packet IDs must be unique safe session IDs')
    if expected_packets is not None and len(packets)!=expected_packets:errors.append({'code':'planned_packet_count_mismatch','expected':expected_packets,'actual':len(packets)})
    for packet in packets:
        sid=packet['packet_id'];cid=packet['case_id'];condition=packet['condition'];errors.extend(packet_errors(packet,corpus.sha256))
        if condition in bycase[cid]:errors.append({'code':'duplicate_case_condition','case_id':cid,'condition':condition})
        bycase[cid][condition]=sid
        logfile=Path(readers)/sid/'events.jsonl'
        if logfile.exists():
            events,valid,initial,input_record=load_log(logfile);inputs.append(input_record)
            audit=audit_session(packet,events,valid,initial,corpus,engine_sha)
        else:
            audit={'session':sid,'chain_valid':None,'audit_valid':None,'errors':[],'warnings':[],'init':None,'exposures':[],'answers':{},'choices':{},'finish':None,'events':[]}
        errors.extend({'session':sid,**x} for x in audit['errors'])
        exposures=audit['exposures'];n=len(exposures);finish=audit['finish'];early=bool(finish and finish.get('early_stop') is True and n<MAX_OPENS)
        packet_status='early_stop' if early else ('observed' if n else 'unstarted')
        view_history=[]
        for index,e in enumerate(exposures,1):
            step=e.get('step',index);v=e.get('view',{});view_history.append(v)
            choice=audit['choices'].get(e.get('choice_event_sha256'),{})
            answer=audit['answers'].get(step,{})
            next_choice=next((x for x in audit['events'] if x.get('event')=='choice' and x.get('next_step')==step+1),{})
            checks=[]
            for cindex,citation in enumerate(answer.get('answer',{}).get('citations',[]),1):
                checked=quote_matches(citation,view_history,corpus.documents)
                checked.update({'session':sid,'packet_id':sid,'case_id':cid,'condition':condition,'step':step,'citation_index':cindex,'answer_event_sha256':answer.get('event_sha256'),'session_audit_valid':audit['audit_valid']})
                checked['verified_quote_presence']=checked['strict_supported'] and audit['audit_valid'] is True
                citation_rows.append(checked);checks.append({'citation_index':cindex,'match_status':checked['match_status'],'strict_supported':checked['strict_supported']})
            cost_fields=['body_codepoints','body_utf8_bytes','navigation_codepoints','navigation_utf8_bytes','source_slice_codepoints','source_slice_utf8_bytes','content_codepoints','content_utf8_bytes','document_navigation_codepoints','document_navigation_utf8_bytes','total_navigation_codepoints','total_navigation_utf8_bytes','display_codepoints','display_utf8_bytes']
            trails.append({
                'session':sid,'packet_id':sid,'case_id':cid,'condition':condition,'layer':packet.get('layer'),'step':step,
                'planned_stage':type(step) is int and 1<=step<=MAX_OPENS,'observation_status':'observed','session_audit_valid':audit['audit_valid'],
                'reader_id':(audit['init'] or {}).get('reader_id'),'engine_sha256':(audit['init'] or {}).get('engine_sha256'),'corpus_sha256':(audit['init'] or {}).get('corpus_sha256'),
                'common_start_url':packet.get('start_url'),'document_version':packet.get('document_version'),'hint':packet.get('hint'),'hint_codepoints':packet.get('hint_codepoints'),'hint_utf8_bytes':packet.get('hint_utf8_bytes'),'packet_codepoints':packet.get('packet_codepoints'),'packet_utf8_bytes':packet.get('packet_utf8_bytes'),
                'choice':choice,'choice_reason':choice.get('selection_reason'),'choice_at_utc':choice.get('at_utc'),
                'exposure_at_utc':e.get('at_utc'),'answer_at_utc':answer.get('at_utc'),'next_choice_at_utc':next_choice.get('at_utc'),
                'duration':{'choice_to_exposure_seconds':seconds(choice.get('at_utc'),e.get('at_utc')),'exposure_to_answer_seconds':seconds(e.get('at_utc'),answer.get('at_utc')),'answer_to_next_choice_seconds':seconds(answer.get('at_utc'),next_choice.get('at_utc')),'engine_exposure_command_wall_seconds':e.get('command_wall_seconds'),'engine_reported_elapsed_since_exposure_seconds':answer.get('elapsed_since_exposure_seconds'),'active_human_reading_seconds':None,'interpretation':'measured wall intervals include tool and scheduling latency; not human time savings'},
                'view':v,'display_sha256':v.get('display_sha256'),'arrival_url':v.get('arrival_url'),'arrival_url_kind':v.get('arrival_url_kind'),'fragment':v.get('fragment'),'doc_id':v.get('doc_id'),'offset_start':v.get('offset_start'),'offset_end':v.get('offset_end'),
                'cost':{k:v.get(k) for k in cost_fields},'cumulative_display_codepoints':e.get('cumulative_display_codepoints'),'cumulative_display_utf8_bytes':e.get('cumulative_display_utf8_bytes'),
                'answer_original':answer.get('answer'),'answer_recorded':bool(answer),'answer_event_sha256':answer.get('event_sha256'),'exposure_event_sha256':e.get('event_sha256'),'source_log':relative(logfile),'citation_checks':checks,'semantic_grade':'not_evaluated','independent_context_verified_by_exporter':False,
            })
        steps_seen={e.get('step') for e in exposures if type(e.get('step')) is int}
        for step in range(1,MAX_OPENS+1):
            status='observed' if step in steps_seen else ('early_stop' if early else 'unstarted')
            slots.append({'packet_id':sid,'session':sid,'case_id':cid,'condition':condition,'step':step,'status':status,'session_status':packet_status,'session_audit_valid':audit['audit_valid'],'answer_recorded':step in audit['answers'],'reason':('logged exposure' if status=='observed' else 'explicit finish before budget exhausted' if status=='early_stop' else 'session has no exposure' if not n else 'planned stage not yet reached at collection')})
        sessions.append({'session':sid,'packet_id':sid,'case_id':cid,'condition':condition,'planned_case_condition_order':packet.get('case_condition_order'),'status':packet_status,'initialized':audit['init'] is not None,'initialized_utc':(audit['init'] or {}).get('at_utc'),'first_exposure_utc':exposures[0].get('at_utc') if exposures else None,'finished':finish is not None,'finished_utc':finish.get('at_utc') if finish else None,'observed_openings':n,'answered_stages':len(audit['answers']),'early_stop_positions':MAX_OPENS-n if early else 0,'unstarted_positions':MAX_OPENS-n if not early and n<MAX_OPENS else 0,'chain_valid':audit['chain_valid'],'audit_valid':audit['audit_valid'],'errors':audit['errors'],'warnings':audit['warnings'],'measured_session_wall_seconds':finish.get('measured_session_wall_seconds') if finish else None,'independent_context_verified_by_exporter':False})
    for cid,conditions in bycase.items():
        if set(conditions)!={'A','B','C'}:errors.append({'code':'case_does_not_have_exact_ABC_packets','case_id':cid,'conditions':sorted(conditions)})
    slotcounts=Counter(x['status'] for x in slots);packetcounts=Counter(x['status'] for x in sessions)
    costs={}
    for condition in ['A','B','C']:
        selected=[r for r in trails if r['condition']==condition]
        costs[condition]={'logged_openings':len(selected),'validated_logged_openings':sum(r['session_audit_valid'] is True for r in selected),'display_codepoints':sum((r['cost'].get('display_codepoints') or 0) for r in selected),'display_utf8_bytes':sum((r['cost'].get('display_utf8_bytes') or 0) for r in selected),'content_codepoints':sum((r['cost'].get('content_codepoints') or 0) for r in selected),'total_navigation_codepoints':sum((r['cost'].get('total_navigation_codepoints') or 0) for r in selected)}
    summary={'schema':1,'collected_utc':utc(),'method':'mechanical_trial_export_no_semantic_grades','planned_packets':len(packets),'planned_stage_positions':len(packets)*MAX_OPENS,'packet_status_counts':{x:packetcounts[x] for x in ['observed','early_stop','unstarted']},'stage_status_counts':{x:slotcounts[x] for x in ['observed','early_stop','unstarted']},'planned_positions_reconciled':sum(slotcounts.values())==len(packets)*MAX_OPENS,'packets_with_any_observation':sum(x['observed_openings']>0 for x in sessions),'finished_packets':sum(x['finished'] for x in sessions),'fully_observed_and_answered_packets':sum(x['observed_openings']==MAX_OPENS and x['answered_stages']==MAX_OPENS for x in sessions),'total_logged_exposures':len(trails),'logged_exposures_outside_planned_positions':sum(not r['planned_stage'] for r in trails),'validated_logged_exposures':sum(r['session_audit_valid'] is True for r in trails),'unverified_logged_exposures':sum(r['session_audit_valid'] is not True for r in trails),'corpus_sha256':corpus.sha256,'expected_engine_sha256':engine_sha,'sessions':sessions,'case_condition_sessions':[{'case_id':cid,**conditions} for cid,conditions in sorted(bycase.items())],'log_inputs':inputs,'audit_errors':errors,'protocol_audit_passed':not errors,'citation_counts':{'total':len(citation_rows),'strict_supported':sum(x['strict_supported'] for x in citation_rows),'verified_quote_presence':sum(x['verified_quote_presence'] for x in citation_rows),'by_match_status':dict(Counter(x['match_status'] for x in citation_rows))},'observed_costs_by_condition':costs,'semantic_answer_grades_produced':False,'notes':['Missing sessions/stages remain unstarted, not observed failures or zero-success answers.','Observed means an exposure record exists; audit validity and completed answers are separate fields.','An early-stopped packet contributes its actual observed stages plus explicit unused early_stop positions.','Citation presence does not establish a claim is correct or that all conditions/exceptions are supported.','The exporter does not prove independent model contexts, active human time, or adoption.']}
    return {'trails':trails,'slots':slots,'citation_checks':citation_rows,'summary':summary}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packets',default=str(OWN/'packets.jsonl'));p.add_argument('--readers',default=str(OWN/'readers'));p.add_argument('--corpus',default=str(OWN/'corpus.json.gz'));p.add_argument('--engine',default=str(OWN/'viewer/reader.py'))
    action=p.add_mutually_exclusive_group();action.add_argument('--write',action='store_true');action.add_argument('--check',action='store_true')
    p.add_argument('--expected-packets',type=int,default=18)
    a=p.parse_args();packet_raw=Path(a.packets).read_bytes();packets=[json.loads(x) for x in packet_raw.decode().splitlines() if x.strip()];corpus=Corpus.load(a.corpus);engine_sha=digest(Path(a.engine).read_bytes())
    data=collect(packets,Path(a.readers),corpus,engine_sha,a.expected_packets)
    summary=data['summary'];summary['packet_input']={'path':relative(a.packets),'sha256':digest(packet_raw),'bytes':len(packet_raw)};summary['exporter_sha256']=digest(Path(__file__).read_bytes())
    outputs={OWN/'trails.jsonl':serial_lines(data['trails']),OWN/'analysis/trial-slots.jsonl':serial_lines(data['slots']),OWN/'analysis/citation-checks.jsonl':serial_lines(data['citation_checks']),OWN/'analysis/trial-summary.json':json.dumps(summary,ensure_ascii=False,indent=2)+'\n'}
    check_errors=[]
    if a.write:
        for path,text in outputs.items():path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
    elif a.check:
        for path,text in outputs.items():
            if not path.exists():check_errors.append({'path':relative(path),'error':'derived output missing'});continue
            actual=path.read_text()
            if path.name=='trial-summary.json':
                old=json.loads(actual);new=json.loads(text);old.pop('collected_utc',None);new.pop('collected_utc',None)
                same=old==new
            else:same=actual==text
            if not same:check_errors.append({'path':relative(path),'error':'derived output differs'})
    result={k:summary[k] for k in ['planned_packets','planned_stage_positions','packet_status_counts','stage_status_counts','total_logged_exposures','validated_logged_exposures','finished_packets','protocol_audit_passed','citation_counts']}
    result.update(written=a.write,check_requested=a.check,check_errors=check_errors,semantic_grades_produced=False)
    print(json.dumps(result,ensure_ascii=False))
    return 0 if summary['protocol_audit_passed'] and not check_errors else 2


if __name__=='__main__':raise SystemExit(main())
