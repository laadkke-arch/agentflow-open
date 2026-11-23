"""Record the B reveal without changing the committed A packet."""
import datetime
import hashlib
import json
import pathlib

BASE=pathlib.Path(__file__).resolve().parents[2]
OUT=BASE/'streams/ripgrep'
PRIVATE=BASE/'private/ripgrep'
SEAL='a6e2f47e6cfa52e249f4d648016cf9d324eccae9'
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
pre=json.loads((OUT/'pre.json').read_text())
events=[];sources=[];post=[];outcomes=[];pins=[]
summaries={
787411584:'OP가 PR을 구현해 볼 의향을 밝힘. 고정 필드 값은 없음.',
787930233:'유지보수자가 glob과 -uuu가 항상 동등하지 않다는 반례와 제외 glob 우선순위를 설명함.',
791894916:'OP가 제외 glob을 ignore의 whitelist로 되살리는 상황을 피하려 했다고 재확인. A에 이미 있던 금지조건.',
792079269:'OP가 필터의 개념과 --type 상호작용 대안을 새로 논의. 고정 필드 외의 설계 논의.',
794839522:'OP가 --type 동작을 별도 제안으로 두자는 견해와 후대 테스트 서술을 편집 댓글에 기록. 고정 B 외 내용.',
801502802:'다른 작성자가 Rust 파일의 이름 패턴도 동시에 제한하려는 별도 목적을 제시함.',
803220914:'OP가 다른 작성자의 use case를 보고 type 설계 선호를 재고. 원래 봉인 필드를 바꾸지 않음.',
803257456:'다른 작성자가 ag 주장은 자신의 fork에 관한 것이었다고 정정함.',
756148273:'유지보수자가 중복 이슈를 지목. OP의 cwd 값 없음.',
792833946:'유지보수자가 비기본 그룹 도움말의 발견 가능성 및 clap 제약을 논의. OP 새 값 아님.',
888316072:'clap 기여자가 후대 clap3 기능과 가정을 제시. OP 새 값/당시판 대체 근거 아님.',
770418482:'유지보수자가 중복 이슈와 alias 해제 방법을 설명. OP 값 아님.',
789179213:'유지보수자가 중복 이슈들을 지목. OP 값 없음.',
811882359:'유지보수자가 --debug 출력을 요청함.',
811886363:'같은 OP가 실제 제외 원인은 부모 .gitignore라고 밝힘. 같은 댓글에 적용 성공 자기보고도 있으나 별도 검증으로 재사용하지 않음.'
}
byid={}
for a in pre:
    n=a['number'];f=json.loads((PRIVATE/f'comments-{n}.json').read_text())
    op=json.loads((PRIVATE/f'opened-{n}.json').read_text())['payload']['issue']['user']
    comments=sorted(f['data'],key=lambda x:(x['created_at'],x['id']))
    for order,c in enumerate(comments,1):
        role='original_author' if c['user']['id']==op['id'] else ('maintainer' if c['user']['login']=='BurntSushi' else 'other_participant')
        e={'event_id':f"RG-{n}-C{c['id']}",'issue_id':a['issue_id'],'comment_id':c['id'],'order':order,
           'actor':c['user']['login'],'actor_id':c['user']['id'],'original_author_id':op['id'],'actor_role':role,
           'same_numeric_author':c['user']['id']==op['id'],'created_utc':c['created_at'],'updated_utc':c['updated_at'],
           'accessed_utc':f['first_read_utc'],'original_url':c['html_url'],'body_sha256':hashlib.sha256(c['body'].encode()).hexdigest(),
           'body_line_count':len(c['body'].splitlines()),'initial_comment_body_verified':c['created_at']==c['updated_at'],
           'comment_history_limit':'REST created=updated; 삭제/다시쓰기까지 증명하지 않음' if c['created_at']==c['updated_at'] else '편집된 현재 댓글; 작성 시 본문 복구 미확인',
           'summary':summaries[c['id']],'selected_field':a['selected_field'],'selected_B_value_event':c['id'] in (791894916,811886363),
           'exposure_phase':'after_remote_A_seal','A_seal_sha':SEAL}
        if c['id']==791894916:e.update(minimal_excerpt="Yes, that's exactly what I meant to avoid.",field_value='yes',field_value_is_new=False,same_goal=True,disclosure_type='author_reaffirmation_after_maintainer_example',value_time_lower_bound=c['created_at'],value_time_upper_bound=c['updated_at'])
        elif c['id']==811886363:e.update(minimal_excerpt="picking up the parent's \".gitignore\"",field_value='ignore_rule',field_value_is_new=True,same_goal=True,disclosure_type='response_to_specific_diagnostic_request',eliciting_event_id='RG-1840-C811882359')
        elif c['id'] in (801502802,803257456):e.update(same_goal=False,disclosure_type='different_author_different_goal',not_B_reason='numeric actor differs from OP; filename-type intersection is a different goal')
        else:e.update(field_value=None,field_value_is_new=False,disclosure_type='no_selected_field_value' if role=='original_author' else 'other_actor_only')
        events.append(e);byid[c['id']]=e
    sources.append({'source_id':f'RG-I{n}-COMMENTS','lineage_id':f'github:BurntSushi/ripgrep:issue:{n}',
       'kind':'original_issue_comments','repository_direction':'file_search','author':';'.join(sorted({c['user']['login'] for c in comments})),
       'original_url':f'https://github.com/BurntSushi/ripgrep/issues/{n}','pinned_url':f'https://github.com/BurntSushi/ripgrep/issues/{n}#issuecomment-{comments[0]["id"]}' if comments else f'https://github.com/BurntSushi/ripgrep/issues/{n}',
       'version_date':'comment created/updated times in events.json','section_lines':'all '+str(len(comments))+' comments in REST page1 (100 requested, fewer returned)',
       'accessed_utc':f['first_read_utc'],'selection_reason':'after A seal reveal; same-author same-goal fixed-field check','direct_read':True,
       'verified_claim':'; '.join(summaries[c['id']] for c in comments),'cannot_determine':'field sentence is not independent proof of successful recommendation; edited comments not automatically original-at-created',
       'contrary_or_unknown':'author identity and goal kept separate; external PR/issues linked inside comments were not followed for A/B adjudication',
       'count_toward_minimum':False,'pagination':{'endpoint':f['url'],'per_page':100,'returned':len(comments),'all_pages_complete':len(comments)<100},'A_seal_sha':SEAL})
    b=dict(a);b['view']='B';b['A_seal_sha']=SEAL;b['first_comment_read_utc']=f['first_read_utc'];b['B_addition_fields']=[]
    b['B_source_event_id']=None;b['B_value']=None;b['B_actor']=None;b['B_actor_id']=None;b['same_candidates_and_evidence']=True
    b['advice_B']=a['A_recommendation'];b['actual_user_success']='unknown';b['independent_followup_event_id']=None
    if n==1808:
        ev=byid[791894916];b.update(B_status='redundant_value_in_current_edited_comment',B_value='yes',B_actor=ev['actor'],B_actor_id=ev['actor_id'],B_source_event_id=ev['event_id'],B_value_is_new=False,B_created_utc=ev['created_utc'],B_updated_utc=ev['updated_utc'],B_timing='value could have appeared between created and updated; original created body recovery403',B_disclosure='author reaffirmation after maintainer explanation',advice_B='RG1808-C2; A에서 이미 보존한 금지조건 그대로',recommendation_change='same',information_effect='no_new_selected_field_information')
    elif n==1840:
        ev=byid[811886363];b.update(B_status='observed_author_value',B_value='ignore_rule',B_actor=ev['actor'],B_actor_id=ev['actor_id'],B_source_event_id=ev['event_id'],B_value_is_new=True,B_created_utc=ev['created_utc'],B_updated_utc=ev['updated_utc'],B_timing='created=updated',B_disclosure='response_to_specific_diagnostic_request',B_addition_fields=[{'field':'exclusion_reason','value':'ignore_rule','source_event_id':ev['event_id']}],advice_B='RG1840-C2; 해당 ignore 규칙의 조정/해제. 실제로 어떤 파일을 검색했는지·성공한 실행은 별도 원자료 없어서 미확인.',recommendation_change='conditional_pair_to_C2',information_effect='resolved_uncertainty',excluded_from_B='symlink라는 추가 주변상황과 --no-ignore-parent works 자기보고는 B에 투입하지 않음')
    else:
        b.update(B_status='data_absent',B_value_is_new=False,B_disclosure='no_original_author_followup_by_query_cutoff',recommendation_change='unobservable',information_effect='unobservable',B_missing_reason='전체 댓글에서 같은 numeric OP의 후속이 없다')
    post.append(b)
    o={'outcome_id':a['issue_id']+'-OUT','issue_id':a['issue_id'],'analysis_layer':a['analysis_layer'],'A_seal_sha':SEAL,'A_body_sha256':a['body_sha256'],
       'B_status':b['B_status'],'B_source_event_id':b['B_source_event_id'],'B_field':a['selected_field'],'B_value':b['B_value'],'B_added_field_count':len(b['B_addition_fields']),
       'A_candidate_ids':[c['id'] for c in a['candidates']],'B_candidate_ids':[c['id'] for c in b['candidates']],
       'recommendation_change':b['recommendation_change'],'information_effect':b['information_effect'],'classification':'retrospective_value' if n==1840 else ('redundant_reconstruction' if n==1808 else 'no_value'),
       'is_observed_pair':False,'is_counterfactual':False,'strict_accuracy_change':'unobservable','strict_accuracy_reason':'A conditional; no unique A correctness key' if n==1840 else ('B contains no new field and edited-comment timing not recovered' if n==1808 else 'B absent'),
       'question_decision':a['question_action'],'question_necessity':'unnecessary_selected_field_already_in_A' if a['question_action']=='skip' else ('field_splits_candidates_conditionally' if n==1840 else 'unknown'),
       'question_false_positive_denominator':n==1840,'question_false_positive':False if n==1840 else None,
       'false_positive_denominator_reason':'봉인 질문의두값을 same evidence의 Hidden/ignore 별도경로로판별가능' if n==1840 else ('질문생략: 실제제안분모아님' if a['question_action']=='skip' else '무응답이며 cwd 하나만으로 후보정오까지 독립확정불가'),
       'independent_mechanism_evidence':[{'candidate_id':c['id'],'evidence':c['evidence']} for c in a['candidates']],
       'separate_author_followup_event':None,'behavior_change_observed':'unknown','real_use_success':'unknown','B_statement_reused_as_success_proof':False,
       'actual_user_effect_measured':False,'query_cutoff_utc':f['first_read_utc'],'actual_B_denominator':n==1840,'strict_change_denominator':False,
       'main_slot_denominator':bool(a['slot']),'prospective_primary_denominator':bool(a['slot']) and a['preread'],'counterfactual_count':0}
    if n==1808:o['followup_limit']='B댓글의 패치/시험 자기보고를 독립결과로 재사용하지 않음. 후속 type 선호 변경은 고정field/같은candidate 밖이며 새목적·새판 소급 대입하지 않음.'
    if n==1840:o['followup_limit']='B와 동일한811886363댓글의 --no-ignore-parent works는 보존하되 독립실행/별도후속아님. 실제 성공수에는 넣지 않음.'
    outcomes.append(o)
    pins.append({'issue_id':a['issue_id'],'A_seal_sha':SEAL,'A_cutoff_utc':a.get('cutoff_A_utc',a['cutoff_A']),'first_comment_read_utc':f['first_read_utc'],'B_source_event_id':b['B_source_event_id'],'B_same_field':True,'A_B_candidate_and_packet_equal':True,'pre_file_modified':False})

recovery=json.loads((PRIVATE/'comment-recovery-791894916.json').read_text())
sources.append({'source_id':'RG-I1808-CREATED-COMMENT-RECOVERY','lineage_id':'github:BurntSushi/ripgrep:issue:1808','kind':'archive_access_failure','repository_direction':'file_search','author':'GH Archive public GitHub event capture','original_url':'https://github.com/BurntSushi/ripgrep/issues/1808#issuecomment-791894916','pinned_url':recovery['url'],'version_date':'2021-03-06T08:23:23Z','section_lines':'IssueCommentEvent/action=created id791894916 target; no body recovered','accessed_utc':recovery['ended_utc'],'selection_reason':'edited B reaffirmation timing verification','direct_read':False,'verified_claim':'HTTP403 access failure only','cannot_determine':'selected field sentence existed at comment creation','contrary_or_unknown':'B time remains interval; no access-control bypass','count_toward_minimum':False,'access_receipt':recovery})

pairs=[
 {'pair_id':'RG-PAIR-NR1','pair_type':'nonresponse','value_issue':'RG-1840','control_issue':'RG-1778','repository':'BurntSushi/ripgrep','operation':'ignore-file path/root diagnosis','selection_rule':'same repo -> same ignore-file path operation -> only available frozen noresponse comparator, then date','value_created_utc':'2021-04-01T12:38:37Z','control_created_utc':'2021-01-07T14:09:33Z','value_result':'OP supplies ignore_rule after --debug request; A uncertainty narrows','control_result':'OP supplies no cwd after original report; maintainer only points to duplicate','limit':'서로 다른 field와 증상이며 무응답은 실패/질문오탐으로 세지 않는다; controlled pair가아닌공개사건비교','causal_effect_identified':False},
 {'pair_id':'RG-PAIR-NE1-UNMATCHED','pair_type':'no_effect','value_issue':'RG-1840','control_issue':'RG-1808','repository':'BurntSushi/ripgrep','operation':'mismatch: hidden/parent-ignore diagnosis vs glob precedence design','selection_rule':'same repo but exact operation criterion fails','value_result':'one new exclusion_reason','control_result':'redundant preservation condition; edited comment timing uncertain','matched':False,'limit':'둘을 정보추가유효/무효의 같은동작짝으로강제하지않음','causal_effect_identified':False}
]
for name,data in [('post.json',post),('events.json',events),('outcomes.json',outcomes),('pins-post.json',pins),('pairs.json',pairs)]:
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(OUT/'sources-post.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in sources))
(OUT/'counterexamples.md').write_text('''# ripgrep 후속 판독과 반례

## 먼저 확인된 결과

원격 A봉인 `a6e2f47e6cfa52e249f4d648016cf9d324eccae9` 뒤 2026-11-23 08:41:08 UTC에 여섯 댓글 endpoint를 처음 열었다. 모두 per_page=100의첫페이지가100개미만이어서 당시 반환 댓글은 전수다(8+1+2+1+1+2=15개). 댓글을 새로운 원저작15개로 세지 않는다.

|행|관측된 후속|A/B 해석|
|---|---|---|
|RG-1808|같은 OP가 제외 glob 우선순위를 다시 확인|A에 이미 있던 값. 새 필드정보 0이며 순수 사전판독 행도 아니다. 현재 댓글은 편집되어 최초작성시각의 문장존재 미확인.|
|RG-1778|유지보수자 중복지목만 있고 OP 후속 없음|cwd B자료없음. 권고개선0·오답·질문오탐으로 세지 않는다.|
|RG-1814|유지보수자와 타 기여자만 응답|OP의 새값 없음. 기본알파벳순 보존은 A에 이미 있음.|
|RG-1792|유지보수자만 답변|OP의 새값 없음. --no-config 조건은 A에 이미 있음.|
|RG-1812|유지보수자 중복지목만 있음|OP의 새값 없음. 우회책 허용은 A에 이미 있음.|
|RG-1840|--debug요청에 같은 OP가 부모.gitignore가 원인이라고 응답|B에는 exclusion_reason=ignore_rule 한 값만 넣음. Hidden해제/ignore규칙조정 두 조건부후보가 후자로 좁혀짐.|

## 한 가지 질문이 도움될 수 있었던 실제 연결

[RG-1840의 요청](https://github.com/BurntSushi/ripgrep/issues/1840#issuecomment-811882359)과 [동일 OP 답변](https://github.com/BurntSushi/ripgrep/issues/1840#issuecomment-811886363)은 실제 공개된 질문-응답이다. ROOT/연구자가 새 사람에게 질문한 것이 아니다. 유지보수자는 --debug 출력을 요청했고, OP가 원인 해석을 밝혔다. 봉인했던 한 값만 추가하면 후보 C2를 고를 수 있다. 작성자의 symlink 설명·성공 자기보고는 B에 추가하지 않았다.

동작 판별은 A에 고정한 [12.1.1 WalkBuilder ignore 순서](https://github.com/BurntSushi/ripgrep/blob/7cb211378a2ac6d421c5f6f3f71411937af23136/crates/ignore/src/walk.rs#L448-L480)와 [hidden 플래그](https://github.com/BurntSushi/ripgrep/blob/7cb211378a2ac6d421c5f6f3f71411937af23136/crates/core/app.rs#L1425-L1444)로 유지했다. 숨김 제외를 해제하는 것은 부모ignore규칙을 자동으로 제거한다는 뜻이 아니다. 실제 작성자의 원실행을 독립 재현하거나 --no-ignore-parent 적용 성공을 별도로 검증한 것은 아니다. 같은 B댓글의 성공문장은 독립 결과로 세지 않았다.

## 처음 떠오른 결론이 틀리는 경로

1. **무조건 질문:** RG-1808·1814·1792·1812에서는 고정한 필드의 답이 최초글에 이미 있었다. 이는 해당필드를다시묻는가상정책의불필요성근거이며, 우리A는질문을생략했으므로실제제안오탐분모에는넣지않는다.
2. **숨김 디렉터리니까 --hidden:** RG-1840은 실제 OP가 parent .gitignore 원인을 밝혔다. 현재 글의 제목/원인 추정만으로 Hidden해제를 확정하면 다른 원인을 놓친다.
3. **상세 반응이 있으면 고정 필드도 채워짐:** RG-1808의 type 설계 논의와 다른 작성자의 목적은 길지만, 봉인한 preserve_negative_glob_priority에 새 정보를 더하지 않는다. 다른 actor의 ag/fork 정정도 원 OP의 B로 넣지 않았다.

## 짝 모집과 미충족

미응답 짝은 RG-1840/RG-1778 한 쌍을 같은 ignore-file 경로/원인 진단으로 비교한다. 후자는 같은 OP 응답이 전혀 없으므로 무응답 자체로 무효나오탐이라고 하지 않는다. 정보추가무효 비교 후보 RG-1808은 이미 알려진 금지조건의 재확인이고 정확한동작도 glob우선순위설계로달라, RG-1840과엄격같은동작짝으로확정하지않았다. 나머지같은동작짝은 미충족이다. 9–16까지 최초글은 읽었지만 그중임의사례의댓글을열어유리한후속을고르지않았다. 필요시별도진단A봉인이먼저필요하다.

## 남은 경계

실제 새B 1개는 주3슬롯 밖의 진단층이다. A가 틀렸던 단일선택에서 옳은 선택으로 바뀐 엄격개선 사례는 측정하지 못했다. A의 조건부 선택이 좁아진 1개를 정답률개선1개로 바꾸지 않는다. observed_pair=0이며 실제사용성공 독립확인도 없다. 원작성자의 B값이 존재해도 탐색기가 먼저 물었을 때 같은 답을 받았을지와 질문 비용은 미확인이다.
''')
print(json.dumps({'events':len(events),'post_rows':len(post),'actual_new_B':sum(r['actual_B_denominator'] for r in outcomes),'strict_accuracy_denominator':sum(r['strict_change_denominator'] for r in outcomes),'question_false_positive_denominator':sum(r['question_false_positive_denominator'] for r in outcomes),'false_positive_observed':sum(r['question_false_positive'] is True for r in outcomes),'noresponse_pairs':1,'strict_noeffect_pairs':0,'pre_unchanged':True},ensure_ascii=False))
