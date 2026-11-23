"""Join preserved stream records without changing sealed A data.

Run from repository root. Only writes beneath this task's owned path.
This is a data transformation, not an execution of the four investigated tools.
"""
from pathlib import Path
from collections import Counter, defaultdict
import csv, hashlib, json, re

B = Path(__file__).resolve().parents[1]
S = B / 'streams'
SEAL_A = 'a6e2f47e6cfa52e249f4d648016cf9d324eccae9'
SEAL_D = '39eec0e2cff033c9d34b55ae20e52880378ac4ef'
ORDER = ['rclone', 'ripgrep', 'pandoc', 'jq']
REPOS = dict(zip(ORDER, ['rclone/rclone','BurntSushi/ripgrep','jgm/pandoc','jqlang/jq']))
MAIN = {'rclone':[4911,4897,4921], 'ripgrep':[1808,1778,1814], 'pandoc':[7003,7013,7006], 'jq':[2259,2267,2349]}

def read(p):
    if not p.exists(): return []
    o = json.loads(p.read_text())
    return o.get('rows', []) if isinstance(o, dict) else o

def pick(r, *ks, default=''):
    for k in ks:
        if k in r and r[k] is not None: return r[k]
    return default

def dump(v):
    if v is None: return ''
    if isinstance(v, (list,dict)): return json.dumps(v, ensure_ascii=False, separators=(',',':'))
    if isinstance(v,bool): return str(v).lower()
    return v

def write_csv(name, rows, fields=None):
    fields = fields or list(dict.fromkeys(k for r in rows for k in r))
    with (B/name).open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for r in rows:w.writerow({k:dump(r.get(k)) for k in fields})

def utc(v):
    if not v: return ''
    return str(v).replace(' UTC','Z').replace(' ','T').replace('+00:00','Z')

sources={}
for p in sorted(S.glob('*/*source*.jsonl')):
    for line in p.read_text().splitlines():
        if line.strip():
            r=json.loads(line)
            if 'source_id' in r:sources[r['source_id']]=r

enrollment=[]; raw_enroll={}
for stream in ORDER:
    for fname in ['enrollment.json','diagnostic-enrollment.json','enrollment-diagnostic.json','diagnostics-enrollment.json']:
        for r in read(S/stream/fname):
            n=r['number']; iid=r['issue_id']; rank=int(pick(r,'sequence','order','enrollment_rank'))
            raw_enroll[iid]=r
            rec=pick(r,'original_recovery','recovery','edit_recovery',default={})
            if not isinstance(rec,dict): rec={}
            eligible=pick(r,'initial_text_eligible','initial_goal_eligible','eligible_content','original_goal_eligible',default=False)
            selected=n in MAIN[stream]
            enrollment.append(dict(enrollment_id=r['enrollment_id'],issue_id=iid,repository=REPOS[stream],stream=stream,sequence=rank,search_layer='initial8' if rank<=8 else 'diagnostic_next8',queue=r['queue'],queue_rank=pick(r,'queue_rank','rank'),created_utc=utc(pick(r,'created_at','created_utc')),original_url=pick(r,'original_url','url',default=f'https://github.com/{REPOS[stream]}/issues/{n}'),eligible=eligible,selected_main=selected,main_slot=MAIN[stream].index(n)+1 if selected else '',diagnostic_selected=False,entry_status='selected_main' if selected else ('eligible_later_not_replacement' if eligible else 'excluded_retained'),reason=pick(r,'reason','exclusion_reason','selection_reason'),selection_detail=pick(r,'selection_reason','reason'),original_body_sha256=pick(r,'original_body_sha256','opening_body_sha256','body_sha256'),current_body_sha256=r.get('current_body_sha256',''),initial_body_verified=True,edit_recovery='opened event recovered; no assumption from empty edit history',archive_url=pick(r,'archive_url',default=rec.get('url',rec.get('archive_url',''))),archive_event_id=pick(r,'archive_event_id',default=rec.get('event_id','')),archive_line=pick(r,'archive_line',default=rec.get('line','')),initial_read_utc=utc(pick(r,'first_read_utc')),comment_count_used_for_selection=False,resolution_used_for_selection=False,origin_ledger=f'streams/{stream}/{fname}'))
enrollment.sort(key=lambda r:(ORDER.index(r['stream']),r['sequence']))
ei={r['issue_id']:r for r in enrollment}
for en in enrollment:
    rr=raw_enroll[en['issue_id']]
    en['reason']=rr.get('reason') or rr.get('exclusion_reason') or rr.get('selection_reason') or '정해진 큐의 판독·보존행'
    matches=[v for v in sources.values() if re.search(r'/issues/'+str(rr['number'])+r'(?:$|[#/?])',str(v.get('original_url',''))) and REPOS[en['stream']] in str(v.get('original_url','')) and 'comment' not in v.get('kind','') and ('original' in v.get('kind','') or v.get('count_toward_minimum'))]
    src=matches[0] if matches else {}
    en['source_id']=src.get('source_id','')
    if not en['initial_read_utc']:en['initial_read_utc']=utc(src.get('accessed_utc',''))
    if not en['archive_url']:en['archive_url']=pick(src,'archive_url','opening_recovery_url')
    if not en['archive_event_id']:en['archive_event_id']=pick(src,'archive_event_id','opening_event_id')
    if not en['archive_line']:en['archive_line']=pick(src,'archive_line')
    arch=sources.get('RCL-ARCH'+str(rr['number']),{}) if en['stream']=='rclone' else {}
    if arch:
        m=re.search(r'JSONL row (\d+)',arch.get('section_lines',''))
        if m:en['archive_line']=int(m[1])
        en['original_recovery_read_utc']=utc(arch.get('accessed_utc',''))
    else:
        rec=rr.get('original_recovery',rr.get('recovery',{}))
        rec=rec if isinstance(rec,dict) else {}
        en['original_recovery_read_utc']=utc(pick(rec,'accessed_utc','started_utc','ended_utc'))
    en['minimum_count_eligible']=bool(src.get('count_toward_minimum'))
    if en['stream']=='ripgrep' and en['sequence']>8:
        en['initial_body_verified']=False
        en['original_body_sha256']=''
        en['edit_recovery']='current body only; original unrecovered; excluded from chronological original-body analysis'

raw_events=[]; raw_posts={}; raw_outcomes=defaultdict(list); raw_pres=[]
for stream in ORDER:
    for fname in ['pre.json','diagnostics-pre.json','diagnostic-pre.json']:
        for r in read(S/stream/fname):raw_pres.append((stream,fname,r))
    for fname in ['post.json','diagnostic-post.json']:
        for r in read(S/stream/fname):raw_posts[r['issue_id']]=(r,f'streams/{stream}/{fname}')
    for fname in ['outcomes.json','diagnostic-outcomes.json']:
        for r in read(S/stream/fname):raw_outcomes[r['issue_id']].append((r,f'streams/{stream}/{fname}'))
    for fname in ['events.json','diagnostic-events.json']:
        for r in read(S/stream/fname):raw_events.append((stream,r,f'streams/{stream}/{fname}'))

events=[]
for stream,r,origin in raw_events:
    is_open=pick(r,'order','sequence',default=-1)==0 or r.get('event_type')=='original_body'
    created=utc(pick(r,'created_utc','utc'))
    updated=utc(pick(r,'updated_utc',default=created))
    events.append(dict(event_id=r['event_id'],issue_id=r['issue_id'],actor=r['actor'],actor_id=r.get('actor_id',''),actor_role=pick(r,'actor_role'),created_utc=created,updated_utc=updated,event_order=pick(r,'order','sequence'),event_type='original_body' if is_open else pick(r,'event_type',default='issue_comment'),original_url=pick(r,'original_url','original_location'),original_position=pick(r,'original_position','content_location',default=pick(r,'original_url','original_location')),body_sha256=pick(r,'body_sha256'),accessed_utc=utc(pick(r,'accessed_utc','read_utc','first_read_utc')),phase=pick(r,'phase','stage','exposure_phase','exposure_stage'),same_goal=pick(r,'same_goal',default='not_explicitly_adjudicated'),selected_field_relation=pick(r,'selected_field_relation','disclosure_type'),summary=pick(r,'summary'),comment_original_wording='opened_event_recovered' if is_open else ('current_text_unchanged_by_REST_timestamps' if created==updated else 'edited_comment_original_wording_not_recovered'),origin_ledger=origin))

cases=[]; views=[]; pins=[]; outcomes=[]
for stream,fname,a in raw_pres:
    iid=a['issue_id']; n=a['number']; en=ei[iid]
    p,post_origin=raw_posts[iid]
    actual=[(o,f) for o,f in raw_outcomes[iid] if not re.search('counterfactual|observed_pair|PAIR',str(o.get('kind',''))+str(o.get('outcome_id','')))]
    o,out_origin=actual[0]
    main=n in MAIN[stream]; scope='main' if main else 'diagnostic'
    seal=SEAL_A if fname=='pre.json' else SEAL_D
    raw_layer=pick(a,'analysis_layer')
    if stream=='rclone':
        clean=(not main and n not in (4956,4914)); budget_ok=not main
        layer='budget_deviation' if main else ('reconstructed_exposed' if n in (4956,4914) else 'prospective_packet')
    else:
        clean=bool(a.get('preread')) and 'exposed' not in raw_layer
        budget_ok=stream!='ripgrep' and iid not in ('jq-2267','pandoc-7013')
        layer='prospective_packet' if clean else 'reconstructed_exposed'
    clean=clean and budget_ok
    question=pick(a,'question_decision','question_action')
    question='ask' if question in ('ask','ask_one') else 'skip'
    necessity='unnecessary' if question=='skip' else ('conditional_discriminator' if iid in ('pandoc-7013','RG-1840') else 'undecidable')
    field=pick(a,'field','selected_field',default='none_A_sufficient') or 'none_A_sufficient'
    aval=pick(a,'value_in_A','A_field_value','already_in_A',default=None)
    if isinstance(aval,bool) and stream=='rclone' and main:aval=a.get('value_in_A')
    present=bool(pick(a,'field_in_A','already_in_A',default=aval is not None))
    if iid in ('RG-1778','RG-1840'):present=False
    author_id=a.get('author_id') or next((e['actor_id'] for e in events if e['issue_id']==iid and e['actor_role'] in ('OP','original_author')), '')
    if not author_id:author_id={'RG-1778':601396,'RG-1814':884378,'RG-1792':26223174,'RG-1812':2343653}.get(iid,'')
    archive=a.get('archive',{})
    original_hash=pick(a,'original_body_sha256','body_sha256')
    original_url=pick(a,'original_url','first_body_url',default=en['original_url'])
    candidates=[]
    if 'candidates' in a:
        for c in a['candidates']:
            candidates.append({'id':c['id'],'action':pick(c,'action','choice'),'evidence':pick(c,'source_sections','evidence',default=[])})
    else:
        for k in (1,2):
            v=a[f'candidate_{k}']; m=re.match(r'([A-Za-z0-9-]+-C[12]):\s*(.*)',v)
            candidates.append({'id':m.group(1) if m else f'{iid}-C{k}','action':m.group(2) if m else v,'evidence':[]})
    budget=a.get('candidate_budget',{})
    if isinstance(budget,dict):
        for c in candidates:
            if isinstance(budget.get(c['id']),list):c['evidence']=budget[c['id']]
    sections=pick(a,'evidence_sections','sections',default=[])
    ids=pick(a,'source_ids','sources',default=[])
    if stream=='jq':
        for k,c in enumerate(candidates,1):
            for section in sections[f'C{k}']:
                sid=('SRC-JQ-MANUALDEV' if iid=='jq-2267' else 'SRC-JQ-MANUAL16') if 'manual' in section else ('SRC-JQ-UTIL16' if 'util.c' in section else 'SRC-JQ-TESTDEV' if 'jq.test' in section else 'SRC-JQ-AUX16' if 'jv_aux' in section else 'SRC-JQ-PRINT16')
                c['evidence'].append({'source_id':sid,'section':section})
    elif stream=='rclone' and not main:
        for c in candidates:c['evidence']=sections
    version=pick(a,'version')
    for c in candidates:
        for j,ev in enumerate(c['evidence'],1):
            sid=ev['source_id']; sr=sources[sid]
            section=str(ev.get('section','')) + (' L'+ev['lines'] if ev.get('lines') else '')
            url=sr.get('pinned_url',sr.get('original_url',''))
            # All source records pin a SHA; never silently replace a documented version.
            line=re.search(r'L?(\d+)\s*[-–]\s*L?(\d+)',section)
            if line and '/blob/' in url:url=url.split('#')[0]+f'#L{line[1]}-L{line[2]}'
            pins.append(dict(pin_id=f'PIN-{iid}-{c["id"]}-{j}',issue_id=iid,candidate_id=c['id'],source_id=sid,version=version,section=section,pinned_url=url,A_seal_sha=seal,same_packet_A_B=True,documents_limit_per_candidate=2,sections_limit_per_document=1,packet_budget_valid=True,strict_actual_budget_compliant=budget_ok,origin_ledger=f'streams/{stream}/{fname}'))
    bstat=pick(p,'B_status'); bval=p.get('B_value')
    if bstat.startswith('data_ambiguous'):bval=None
    bevent=pick(p,'B_event_id','B_source_event_id',default='')
    btime=utc(pick(p,'B_utc','B_created_utc','B_source_utc'))
    event=next((e for e in events if e['event_id']==bevent),{})
    burl=pick(p,'B_source_url',default=event.get('original_url',''))
    has_b=bval is not None
    new_b=has_b and iid=='RG-1840'
    recchange='conditional_pair_to_C2' if new_b else 'same_direction' if has_b else 'unobservable'
    fpden=iid in ('pandoc-7013','RG-1840')
    fpreason=pick(o,'false_positive_denominator_reason','fp_basis','false_positive_reason','exclusion_reason',default=pick(p,'false_positive_reason','effect_exclusion'))
    followevents=pick(p,'actual_followup_event','author_separate_followup_events','independent_followup_event_id','OP_followup_event_ids',default=pick(o,'independent_followup_event','separate_author_followup_event','author_separate_followup','independent_author_followup_event_ids',default=[]))
    actualfollow=pick(p,'actual_followup','actual_application',default=pick(o,'independent_followup_detail','actual_author_behavior_change','behavior_change_observed',default='unknown'))
    success=pick(p,'actual_success_level','actual_success','actual_user_success',default=pick(o,'actual_author_success','real_use_success','actual_success',default='unknown'))
    unknown=pick(p,'unknowns','meaning','why_not_B','effect_exclusion','independent_correctness',default=pick(o,'followup_limit','exclusion_reason','reason','limitations',default='실행 성공·질문 인과효과·비용 미확인'))
    exposure=pick(a,'exposure','exposure_note','preexposure',default='')
    if stream=='rclone' and not main and n==4956:exposure='현재 검색 제목의 후대 cache full 정보 노출; 최초 제목 복구 후에도 재구성층'
    if iid=='RCL-4914':exposure='현재본문의 후대 core/command 문서링크를 먼저 읽음; 최초판 복구 뒤에도 재구성층. 동일 기준의 PAN7057과 일치시킴.'
    excerpt=pick(a,'first_expression_minimal','initial_excerpt','minimum_excerpt','excerpt',default='')
    questiontext=pick(a,'question')
    goal=pick(a,'goal','purpose');context=pick(a,'context','part');prohibitions=pick(a,'prohibitions','forbidden_condition','explicit_forbidden_conditions')
    aevidence=[ev for c in candidates for ev in c['evidence']]
    firstread=utc(pick(p,'first_comment_read_utc'))
    c=dict(issue_id=iid,stream=stream,repository=REPOS[stream],number=n,sequence=en['sequence'],scope=scope,main_slot=en['main_slot'],layer=layer,raw_layer=raw_layer,clean_packet=clean,strict_budget_compliant=budget_ok,original_body_sha256=original_hash,original_url=original_url,author=a['author'],author_id=author_id,created_utc=en['created_utc'],archive_url=pick(a,'archive_url',default=archive.get('url',en['archive_url'])),archive_event_id=pick(a,'archive_event_id',default=archive.get('event_id',en['archive_event_id'])),archive_line=pick(a,'archive_line',default=archive.get('line',en['archive_line'])),cutoff_A_utc=utc(pick(a,'cutoff_A_utc','cutoff_A')),A_seal_sha=seal,A_origin=f'streams/{stream}/{fname}',A_record_url=f'https://github.com/laadkke-arch/agentflow-open/blob/{seal}/docs/workstreams/research/AF-RES-070/streams/{stream}/{fname}',first_comment_read_utc=firstread,excerpt=excerpt,context=context,goal=goal,prohibitions=prohibitions,field_category=pick(a,'field_category','selected_field_class'),selected_field=field,field_in_A=present,A_value=aval,question_decision=question,question=questiontext,skip_reason=pick(a,'skip_reason',default='최초글에 목적/동작이 이미 특정됨' if question=='skip' else ''),necessity=necessity,candidates=candidates,version=version,version_attribution=pick(a,'version_attribution','version_status',default='sealed version only; executable build hash not independently verified'),advice_A=pick(a,'advice_A','A_recommendation'),if_value_1=pick(a,'if_value_1','if_yes',default=a.get('value_to_change','')),if_value_2=pick(a,'if_value_2','if_no'),B_status=bstat,B_value=bval,B_event_id=bevent,B_actor=pick(p,'B_actor',default=event.get('actor','')),B_actor_id=pick(p,'B_actor_id',default=event.get('actor_id','')),B_utc=btime,B_source_url=burl,B_disclosure=pick(p,'utterance_type','disclosure_type','B_disclosure','B_classification'),B_is_new=new_b,advice_B=pick(p,'advice_B'),recommendation_direction_change=recchange,strict_accuracy_change='unobservable',strict_effect_denominator=False,false_positive_denominator=fpden,false_positive=False if fpden else None,false_positive_basis=fpreason,actual_followup=actualfollow,actual_followup_events=followevents,actual_success=success,unknowns=unknown,exposure_note=exposure,post_origin=post_origin,outcome_origin=out_origin)
    cases.append(c)
    if iid=='RG-1808':
        c['B_value_time_status']='edited_current_comment; first wording unrecovered'
        c['B_value_time_lower_bound']='2021-03-06T08:23:23Z'
        c['B_value_time_upper_bound']='2021-03-06T23:32:42Z'
    else:c['B_value_time_status']='REST created/updated metadata; see EVENTS' if has_b else 'no_injected_value'
    en['diagnostic_selected']=not main
    if not main:en['entry_status']='selected_diagnostic_not_main_replacement'
    for view in ('A','B'):
        views.append(dict(view_id=f'{iid}-{view}',issue_id=iid,view=view,scope=scope,layer=layer,context=context,goal=goal,prohibitions=prohibitions,selected_field=field,field_category=c['field_category'],field_value=aval if view=='A' else bval,field_value_source=original_url if view=='A' else burl,B_status='' if view=='A' else bstat,values_copied_into_B=0 if view=='A' else int(has_b),new_information_values=0 if view=='A' else int(new_b),masked_information='all comments/outcomes at A cutoff; known exposure recorded separately' if view=='A' else 'all other post-A fields kept outside B',question_decision=question,question_or_skip_reason=questiontext if question=='ask' else c['skip_reason'],candidate_ids=[v['id'] for v in candidates],candidate_1=candidates[0]['action'],candidate_2=candidates[1]['action'],advice=c['advice_A'] if view=='A' else c['advice_B'],evidence_sections=aevidence,version=version,A_seal_sha=seal,cutoff_A_utc=c['cutoff_A_utc'],first_comment_read_utc=firstread,original_body_sha256=original_hash,origin_ledger=c['A_origin'] if view=='A' else post_origin))
    outcomes.append(dict(outcome_id=f'OUT-{iid}',issue_id=iid,row_type='case',scope=scope,layer=layer,actual_or_reconstructed='prospectively_sealed_retrospective_thread' if clean else 'reconstructed_or_budget_deviation',question_decision=question,question_necessity=necessity,B_status=bstat,B_value_observed=has_b,B_value_new=new_b,B_source_event=bevent,independent_mechanism_criterion='bounded_version_sections_only',recommendation_direction_change=recchange,strict_accuracy_change='unobservable',strict_effect_denominator=False,strict_effect_exclusion='새 B가 있는 유일 사례도 A가 조건부여서 정답 반전 기준 없음' if new_b else '새 B 또는 완전한 독립 정오 기준 없음; 중복 값은 방향 확인에만 사용',false_positive_denominator=fpden,false_positive=False if fpden else None,false_positive_basis=fpreason,actual_followup_events=followevents,actual_followup=actualfollow,actual_success=success,B_reused_as_success_proof=False,slot_denominator=True,excluded_counterfactual_count=0,unknowns=unknown,origin_ledger=out_origin))

    if not any(e['issue_id']==iid and e['event_type']=='original_body' for e in events):
        events.append(dict(event_id=iid+'-OPEN',issue_id=iid,actor=a['author'],actor_id=author_id,actor_role='OP',created_utc=en['created_utc'],updated_utc=en['created_utc'],event_order=0,event_type='original_body',original_url=original_url,original_position=f"opened event {c['archive_event_id']}; line {c['archive_line']}",body_sha256=original_hash,accessed_utc=c['cutoff_A_utc'],phase='A',same_goal=True,selected_field_relation='initial_input',summary=goal,comment_original_wording='opened_event_recovered',origin_ledger=c['A_origin']))

# Preserve observed interventions and researcher counterfactuals as separate rows.
for iid, pairs in raw_outcomes.items():
    for r,origin in pairs:
        kind=r.get('kind','')
        if not ('counterfactual' in kind or 'observed_pair' in kind):continue
        case=next(c for c in cases if c['issue_id']==iid)
        refs=pick(r,'source_event','evidence_ids',default=[])
        refs=[refs] if isinstance(refs,str) else refs
        outcomes.append(dict(outcome_id=r['outcome_id'],issue_id=iid,row_type='counterfactual' if kind=='counterfactual' else 'observed_pair',scope=case['scope'],layer=kind,actual_or_reconstructed='researcher_counterfactual' if kind=='counterfactual' else 'author_reported_intervention',question_decision='not_AB',question_necessity='not_AB',B_status='not_AB',B_value_observed=False,B_value_new=False,recommendation_direction_change='not_AB',strict_accuracy_change='not_measured',strict_effect_denominator=False,false_positive_denominator=False,false_positive=None,slot_denominator=False,excluded_counterfactual_count=1 if kind=='counterfactual' else 0,actual_followup=pick(r,'reported_outcomes','accuracy_outcome'),actual_followup_events=[v for v in refs if v not in sources],evidence_source_ids=[v for v in refs if v in sources],unknowns=pick(r,'reason_not_B','exclusion_reason'),origin_ledger=origin))
for r in read(S/'jq/observed-pairs.json'):
    outcomes.append(dict(outcome_id=r['outcome_id'],issue_id=r['issue_id'],row_type='observed_pair',scope='diagnostic',layer=r['analysis_layer'],actual_or_reconstructed='author_reported_intervention',question_decision='not_AB',question_necessity='not_AB',B_status='not_AB',B_value_observed=False,B_value_new=False,recommendation_direction_change='not_AB',strict_accuracy_change='not_measured',strict_effect_denominator=False,false_positive_denominator=False,false_positive=None,slot_denominator=False,excluded_counterfactual_count=0,actual_followup=r['result'],actual_followup_events=r['author_event'],unknowns=r['reason'],origin_ledger='streams/jq/observed-pairs.json'))

extra_pairs=[
 ('OBS-pandoc-7006-A','pandoc-7006','main','observed_pair_in_A','original_author','pandoc-7006-OPEN','A에 각주 이미지 뒤 블록 유무의 두 입력·출력. 후속 B가 아니며 최초판 설치버전은 조건부.','streams/pandoc/outcomes.json'),
 ('OBS-pandoc-7039-maintainer','pandoc-7039','diagnostic','other_actor_observed_pair','maintainer','PAN-EVENT-762396233','유지보수자의 class 유무 두 입력/출력 원시험. OP의 class 보존 필요성이나 OP 성공으로 바꾸지 않음.','streams/pandoc/diagnostic-outcomes.json'),
 ('OBS-pandoc-7113-other-field','pandoc-7113','diagnostic','observed_pair_other_field','original_author','PAN-EVENT-786070320','OP의 wrapping div 제거 결과로 타인의 원인 설명이 수정됨. 봉인한 -f/-t 필드의 B는 아님.','streams/pandoc/diagnostic-outcomes.json'),
 ('OBS-jq-2259-A','jq-2259','main','author_report_comparison_in_A','original_author','jq-2259-A0','stdin/raw-input와 파일/rawfile 비교를 최초글에서 보고. 완전한 두 원출력 검증과 한 필드 질문효과는 미확인.','streams/jq/outcomes.json'),
 ('OBS-jq-2267-A','jq-2267','main','author_report_two_versions_in_A','original_author','jq-2267-A0','OP는Debian1.5에서는정상이고a17dd개발판에서는1,null,null이라고보고. 1,null,2는기대출력이며두판의완전한실행출력을독립검증하지않음.','streams/jq/outcomes.json'),
]
for oid,iid,scope,layer,actor,event,desc,origin in extra_pairs:
    outcomes.append(dict(outcome_id=oid,issue_id=iid,row_type='other_actor_observed_pair' if actor=='maintainer' else 'observed_pair',scope=scope,layer=layer,actual_or_reconstructed=actor+'_reported_comparison',question_decision='not_AB',question_necessity='not_AB',B_status='not_AB',B_value_observed=False,B_value_new=False,recommendation_direction_change='not_AB',strict_accuracy_change='not_measured',strict_effect_denominator=False,false_positive_denominator=False,false_positive=None,slot_denominator=False,excluded_counterfactual_count=0,actual_followup=desc,actual_followup_events=event,unknowns='새 B 한필드 효과·독립 재실행·질문 비용 미측정',origin_ledger=origin))

cases.sort(key=lambda r:(ORDER.index(r['stream']),0 if r['scope']=='main' else 1,r['sequence']))
case_index={r['issue_id']:r for r in cases}
events.sort(key=lambda r:(list(case_index).index(r['issue_id']),r['created_utc'],str(r['event_id'])))
seen=set()
for e in events:
    assert e['event_id'] not in seen,e['event_id'];seen.add(e['event_id'])
    if not e['accessed_utc']:e['accessed_utc']=case_index[e['issue_id']]['cutoff_A_utc'] if e['event_type']=='original_body' else case_index[e['issue_id']]['first_comment_read_utc']
    if e['event_type']=='original_body':
        en=ei[e['issue_id']]
        recovered_at=en.get('original_recovery_read_utc')
        if recovered_at:
            e['accessed_utc']=recovered_at
            e['access_time_basis']='original_recovery_recorded_request_time'
        else:e['access_time_basis']='A_cutoff_upper_bound; exact original-section read time not separately logged'
    else:e['access_time_basis']='recorded_comment_fetch_time'

write_csv('ENROLLMENT.csv',enrollment)
write_csv('EVENTS.csv',events)
write_csv('VIEWS.csv',views)
write_csv('OUTCOMES.csv',outcomes)
write_csv('PINS.csv',pins)
(B/'CASES.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
counts={
 'enrollment':len(enrollment),'initial8':sum(r['sequence']<=8 for r in enrollment),'eligible_initial8':sum(r['sequence']<=8 and r['eligible'] for r in enrollment),'original_body_recovered':sum(r['initial_body_verified'] for r in enrollment),'cases':len(cases),'main':sum(c['scope']=='main' for c in cases),'diagnostic':sum(c['scope']=='diagnostic' for c in cases),'events':len(events),'views':len(views),'pins':len(pins),'outcomes':len(outcomes),
 'new_B':sum(c['B_is_new'] for c in cases),'redundant_B':sum(c['B_value'] is not None and not c['B_is_new'] for c in cases),'question_proposed':sum(c['question_decision']=='ask' for c in cases),'question_skipped':sum(c['question_decision']=='skip' for c in cases),'false_positive_denominator':sum(c['false_positive_denominator'] for c in cases),'false_positive_numerator':sum(c['false_positive'] is True for c in cases),'strict_effect_denominator':0,
 'groups':[]}
for scope in ('main','diagnostic'):
 for necessity in ('conditional_discriminator','unnecessary','undecidable'):
    rs=[c for c in cases if c['scope']==scope and c['necessity']==necessity]
    counts['groups'].append(dict(scope=scope,necessity=necessity,slots=len(rs),clean_packet=sum(c['clean_packet'] for c in rs),strict_effect_denominator=0,improved=0,same=0,worsened=0,unobservable=len(rs),excluded_counterfactual=sum(o.get('excluded_counterfactual_count',0) for o in outcomes if o['issue_id'] in {c['issue_id'] for c in rs})))
(B/'evidence/ledger-summary.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(counts,ensure_ascii=False))
