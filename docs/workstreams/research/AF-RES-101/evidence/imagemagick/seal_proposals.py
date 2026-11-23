"""Stage 2 extraction/identity judgments. Does not inspect author followups."""
import datetime
import hashlib
import html
import json
from pathlib import Path
import re

BASE=Path(__file__).resolve().parents[2]
OUT=BASE/'evidence/imagemagick'
CACHE=BASE/'.cache/imagemagick/stage2'
events=json.loads((CACHE/'non-op-30day-projection.json').read_text())
receipt=json.loads((OUT/'stage2-acquisition.json').read_text())
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()

def answer(aid,revision):
    return next(x for x in events if x['kind']=='answer_revision' and x['post_id']==aid and x['revision_number']==revision)

def comment(cid):
    return next(x for x in events if x.get('comment_id')==cid)

def ref(event,loc):
    return {'url':event['url'],'revision_url':event.get('revision_url'),'revision_guid':event.get('revision_guid'),'post_id':event['post_id'],'comment_id':event.get('comment_id'),'body_location':loc,'body_sha256':event['body_sha256'],'at_utc':datetime.datetime.fromtimestamp(event['time'],datetime.timezone.utc).isoformat(),'author':event['author']}

def c(case,rank,primary,loc,operation,product,sameproduct,productproof,relation,opproof,difference,links=None,aliases=None):
    return {'candidate_id':f'{case}-C{rank}','case_id':case,'original_rank':rank,'blank':False,'first_proposal_utc':datetime.datetime.fromtimestamp(primary['time'],datetime.timezone.utc).isoformat(),'origin_urls':[ref(primary,loc)],'original_links':links or [],'research_official_url':None,'research_official_section':None,'operation':operation,'candidate_product':product,'same_product':sameproduct,'same_product_proof':productproof,'same_operation':'not_proven_same','operation_relation':relation,'same_operation_proof':opproof,'difference_from_attempt':difference,'identity_edge_cases':aliases or [],'known_before_proposal':'unknown','a':{'keep':not sameproduct,'excluded':sameproduct,'reason':'최초판 actual use와 같은 ImageMagick 제품(사용 wrapper 경유 포함)' if sameproduct else '최초판에 후보 제품을 실제 사용했다는 증거 없음'},'b':{'keep':True,'excluded':False,'reason':'기존 actual attempt와 입력·인수·처리단계의 동일성 미입증; 동일성 미확인'},'judged_utc':utc,'fitness_before_official_review':'미확인','awareness_before_followup_review':'미확인','comment_history_limit':'current public comment body; no edit history' if primary['kind']=='comment' else None}

rows=[]
rows.append(c('IM-A1',1,answer(77774667,1),'p1–p2; pre1 entire QuickMagick pipeline','QuickMagick::Image.read→clone→HCL→G separate→threshold(15)→CopyOpacity composite→save','ImageMagick via QuickMagick',True,'initial p2/pre2 executes convert through QuickMagick.exec3; proposal uses the same named QuickMagick wrapper','different_binding_call','actual attempt is a raw convert string without grouping; proposed object API has distinct calls and threshold representation','raw command string becomes object pipeline; command grouping and effective threshold cannot be assumed equal',aliases=['same_product_different_calls']))
rows[-1]['origin_urls'].append(ref(answer(77774667,2),'pre1 unchanged repetition of revision 1'))
rows[-1]['literal_cautions']=['answer explicitly says the first QuickMagick code is untested','threshold(15) is literal 15, unlike initial CLI threshold 15%; effective meaning not checked yet']
rows.append(c('IM-A1',2,answer(77774667,2),'UPDATE paragraph and pre2 RMagick pipeline','RMagick Image.read→clone HCL→separate GreenChannel→threshold(QuantumRange*0.15)→CopyOpacityCompositeOp→write','ImageMagick via RMagick',True,'revision 2 explicitly assumes RMagick and ImageMagick installed; initial actual convert execution uses the same ImageMagick engine','different_binding_and_mask_pipeline','initial actual execution is QuickMagick.exec3(raw convert); this uses RMagick objects, explicit threshold-image object and quantum-scaled argument','new Ruby binding and explicitly separated opacity mask; equality to failed invocation unproved',aliases=['same_product_new_binding_name']))
rows[-1]['product_identity_sensitivity']='RMagick is a distinct Ruby wrapper, not an alias of QuickMagick. Main A compares ImageMagick engine identity, demonstrated by initial actual convert and the candidate narrative. A wrapper-only rule would retain C2 because initial RMagick is only mentioned.'
rows.append(c('IM-A1',3,answer(77774667,2),'APPROACH 2 paragraph and pre3 Open3 pipeline','Ruby Open3.popen3 executes convert with escaped parentheses around clone/HCL/G/separate/threshold15%, then CopyOpacity composite','ImageMagick CLI via Open3',True,'initial pre2 actually attempts convert via QuickMagick.exec3; proposal still invokes convert','different_grouping_and_invocation','actual initial command omits parentheses; candidate adds them and uses Open3/path shellescape. Initial pre1 already cites the grouped CLI operation but does not report executing it','grouped mask processing and wrapper/path quoting differ from actual failed attempt',aliases=['different_wrapper_same_program','known_third_party_method_not_actual_attempt']))
rows[-1]['known_before_proposal']='initial third_party_suggestion contains same grouped convert core; new Open3 invocation details are not established as known'
rows[-1]['literal_cautions']=['source requires open3 but calls String#shellescape without an explicit shellwords require; validity not tested before seal']

rows.append(c('IM-A2',1,answer(77797032,1),'p1 and pre1 conditional_part assignment / later expansion','External shell if builds the full conditional_part command fragment; expand it inside a single convert call','ImageMagick CLI with shell',True,'initial p1/pre1 actually uses convert in ImageMagick 7.0.10-61/Cygwin','different_command_construction_stage','initial failed form places shell if/else syntax in the convert argument chain; candidate precomputes a variable before invocation','branch moves to shell setup and inserts a complete fragment string; exact argv equivalence is unproved',aliases=['same_product_different_preprocessing_stage']))
rows[-1]['literal_cautions']=['fragment string carries escaped parentheses and quotes; shell expansion behavior not tested before seal']
rows.append(c('IM-A2',2,answer(77797051,1),'pre1 dims/wd assignments and last pre substitute command','External shell if sets dims and wd, then interpolate those values in one convert call','ImageMagick CLI with shell',True,'initial p1/pre1 actually uses the same convert pipeline','different_scalar_parameterization_stage','initial actual failed form embeds if/else inside command; proposed branch chooses scalar geometry values before command','changes command construction and variable targets; not a proven rerun of an already tried complete invocation',aliases=['same_product_different_arguments']))
rows[-1]['origin_urls'].append(ref(answer(77797051,2),'same variable-factor operation; revision removes extra d in dims assignment'))
rows[-1]['literal_cautions']=['revision1 has dims="30x40"d; revision2 removes d','last code block still places ${dims}! before mpr:img while white patch remains 30x40','last code block includes fi with no matching if inside the shown for loop; do not silently repair']

rows.append(c('IM-U1',1,answer(77743766,1),'p1 and pre1','convert qrcode_hidden.png -brightness-contrast 0,90 x.png','ImageMagick CLI',False,'initial mentions ImageMagick/OpenCV but reports only unspecified internet methods','unknown_initial_attempt','no initial named operation, arguments or actual product; cannot prove a rerun','reveals contrast with explicit 0,90; difference from unspecified history unknown',links=[{'url':'https://i.sstatic.net/HUbgd.png','kind':'answer_output_image','section':'output after contrast command'}]))
rows.append(c('IM-U1',2,answer(77745450,1),'p3: scan one line at a time and toggle colour on opposite-signed peaks','Scan each horizontal line; reconstruct alternating black/white runs when peak polarity flips; subsequent cleanup conditional on module geometry','custom image-processing algorithm (program unspecified)',False,'initial actual product usage unspecified; proposal does not name an executable product','unknown_initial_attempt','initial contains no named method, parameters or representation state','converts edge-transition pattern to black/white runs; overlap with unspecified methods unknown',links=[{'url':'https://i.sstatic.net/2dmoc.gif','kind':'diagnostic_animation','section':'dynamic line intensity profile'}],aliases=['same_address_different_section']))
for rev in [2,3]:rows[-1]['origin_urls'].append(ref(answer(77745450,rev),'p3 repeats the original line reconstruction operation'))
rows.append(c('IM-U1',3,answer(77745450,2),'section after first hr; normalization paragraph and pre1','magick qr.png -normalize qr-norm.png before detecting peaks/troughs','ImageMagick CLI',False,'initial only mentions ImageMagick as an option; actual use not proved','unknown_initial_attempt','no initial specific attempt to match; normalization is separately proposed preprocessing','normalizes intensities to make extrema easier to detect; not same as the already-proposed contrast argument',links=[{'url':'https://i.sstatic.net/gDvdB.png','kind':'answer_output_image','section':'normalized image'}],aliases=['same_address_different_section']))
rows[-1]['origin_urls'].append(ref(answer(77745450,3),'normalization section unchanged from revision2'))

rows.append(c('IM-U2',1,comment(137122439),'four-corner perspective clause and original URL','Find four source corners and rectangle destination corners, then perspective-warp; operator sign and output bounds unspecified','ImageMagick CLI',False,'initial deskew mention is explicitly a conjecture, not an execution report','unknown_initial_attempt','initial has no actual deskew/perspective execution or coordinates','perspective corner mapping differs conceptually from mentioned deskew, but prior use is unknown',links=[{'url':'https://imagemagick.org/Usage/distorts/#perspective','kind':'original_reference','section':'perspective'}],aliases=['same_reference_more_specific_later_call']))
rows[-1]['literal_cautions']=['proposal only claims rectangular perspective rectification; removing wrinkles is explicitly not covered','automatic corner detection algorithm is not supplied']
rows[-1]['duplicated_relation']={'other_candidate':'IM-U2-C2','shared_component':'four-corner perspective rectification','not_merged_reason':'first comment leaves +/-distort and output bounds unspecified; exact operation identity not established','related_origin':ref(comment(137133948),'later explicit +distort and same-size desired rectangle')}
rows.append(c('IM-U2',2,comment(137133948),'entire concrete four-corner +distort proposal','Find four paper corners, compute four desired corners of a same-size rectangle, then +distort perspective','ImageMagick CLI',False,'initial has no actual ImageMagick execution report','unknown_initial_attempt','initial has no specific perspective command or coordinates; later candidate adds the explicit plus-prefixed operator','adds explicit +distort and same-size destination; equality to general earlier candidate unproved',links=[{'url':'https://imagemagick.org/Usage/distorts/#perspective','kind':'inherited_original_reference','section':'see the link above: perspective'}],aliases=['same_reference_different_argument_specificity']))
rows[-1]['duplicated_relation']={'other_candidate':'IM-U2-C1','shared_component':'four-corner perspective rectification','not_merged_reason':'explicit +distort argument is absent from C1; separate per presealed missing-value rule','related_origin':ref(comment(137122439),'earlier unspecified-sign perspective operation')}
rows[-1]['literal_cautions']=['automatic source-corner detection and wrinkle removal remain unspecified','effect of + versus - has not been checked against official documentation before seal']

for row in rows:
    name=row['candidate_product']
    row['engine_name']='ImageMagick' if name.startswith('ImageMagick') else None
    row['wrapper_name']='QuickMagick' if 'QuickMagick' in name else 'RMagick' if 'RMagick' in name else 'Open3' if 'Open3' in name else None
    row['product_match_level']='engine' if row['engine_name'] else 'unspecified'
    row['wrapper_alias_claim']=False

ordered=[]
for case in ['IM-A1','IM-A2','IM-U1','IM-U2']:
    group=sorted([r for r in rows if r['case_id']==case],key=lambda r:r['original_rank'])
    for policy in ['a','b']:
        survived=[r for r in group if r[policy]['keep']]
        for r in group:
            rank=survived.index(r)+1 if r in survived else None
            r[policy].update({'survivor_rank':rank,'returned_rank':rank if rank and rank<=2 else None,'rank_shift':r['original_rank']-rank if rank else None,'return_explanation':'제외' if rank is None else '앞의 두 생존 후보로 반환' if rank<=2 else '생존하지만 반환 2자리 밖'})
    for r in group:ordered.append(r)
    for rank in range(len(group)+1,4):
        ordered.append({'candidate_id':f'{case}-C{rank}','case_id':case,'original_rank':rank,'blank':True,'blank_reason':'30일 공개 비작성자 답/댓글에서 세 번째까지의 추가 구체 조작을 확보하지 못함; 외부 검색으로 보충하지 않음','judged_utc':utc,'a':{'keep':False,'excluded':False,'returned_rank':None,'reason':'후보 결원'},'b':{'keep':False,'excluded':False,'returned_rank':None,'reason':'후보 결원'}})
(OUT/'candidate-part.json').write_text(json.dumps(ordered,ensure_ascii=False,indent=2))

reviews={
('answer_revision',77743766,1):'IM-U1-C1: brightness-contrast 0,90',
('comment',137060047,None):'not candidate: noise limitation, no operation',
('comment',137060087,None):'not candidate: inferred generation history and no direct inverse',
('answer_revision',77745450,1):'IM-U1-C2: horizontal line peak reconstruction; generic cleanup is not independently specified',
('answer_revision',77745450,2):'IM-U1-C2 repeated; IM-U1-C3 normalization added',
('answer_revision',77745450,3):'C2/C3 repeated; later horizontal/vertical projections excluded by original-three cap',
('comment',137066238,None):'later two-axis reconstruction and combination excluded by original-three cap; not a simple exact duplicate of C2',
('comment',137113932,None):'not candidate: asks for missing error details',
('answer_revision',77774667,1):'IM-A1-C1: QuickMagick object pipeline',
('comment',137113984,None):'not candidate: refers to answer and requests error context',
('answer_revision',77774667,2):'C1 repeated, IM-A1-C2 RMagick and C3 Open3; indirect author-error acknowledgement exposed',
('comment',137114781,None):'not candidate: points to already merged answer update',
('comment',137122439,None):'IM-U2-C1: four-corner perspective correction',
('comment',137123139,None):'not candidate: diagnosis/question, not a concrete changed call; quotes later QuickMagick object-read error',
('comment',137133948,None):'IM-U2-C2: explicit +distort and same-size destination; overlaps C1 concept but exact call identity unproved',
('answer_revision',77797032,1):'IM-A2-C1: full fragment string construction',
('answer_revision',77797051,1):'IM-A2-C2: scalar dims/wd parameterization; quoted initial pipeline is not a second new candidate',
('answer_revision',77797051,2):'C2 repeated; lexical typo correction is not a separate operation',
}
eventindex=[];sources=[]
for e in events:
    ident=e.get('comment_id',e['post_id']);rev=e.get('revision_number');k=(e['kind'],ident,rev)
    item={k:v for k,v in e.items() if k!='body'}
    item.update({'event_id':f'IM-P-{ident}'+(f'-R{rev}' if rev else ''),'review':reviews[k]})
    eventindex.append(item)
    request=next(r for r in receipt if r['stem']==('comments' if e['kind']=='comment' else 'answer-revisions'))
    sources.append({'id':item['event_id'],'questions':['Q3','Q4'],'case_id':e['case_id'],'original_url':e['url'],'directly_opened_url':request['url'],'pinned_url':e.get('revision_url',e['url']),'confirmation_utc':request['utc'],'author_publisher':e['author'].get('display_name')+' / Stack Overflow','lineage':'Stack Overflow question '+str(e['question_id']),'version_section':f'{e["kind"]} {ident} revision {rev}; source body SHA-256; candidate-part location','fingerprint':{'body_html_sha256':e['body_sha256'],'response_sha256':request['response_sha256']},'observed':reviews[k],'claim_relation':'supports chronological candidate extraction or noncandidate exclusion; not evidence of requester awareness','limitations':'No author-outcome scoring before second seal; comment edit history unavailable' if e['kind']=='comment' else 'Public revision body within 30-day window; raw candidate code validity not yet checked','counted':False,'count_category':'selected_request_child_evidence','duplicate_reason':'same public request event; cannot count separate answer/comment as an independent selected request'})
(OUT/'proposal-event-index.json').write_text(json.dumps(eventindex,ensure_ascii=False,indent=2))
(OUT/'sources-proposals.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in sources))
exposure={'stage':2,'actor':'/root/recruit_imagemagick','also_exposed_actor':'/root (independently read full non-op 30-day projection before seal)','judged_utc':utc,'stage1_commit':'9d646592613ba2fd9c52bc9bbf3dbc28bac68693','machine_received':'Full current answer/comment fields and all answer revisions; self-authored records, current acceptance/score, and out-of-window revision contents stay in ignored cache','analyst_projection':'Non-questioner answer revisions/public comments within each 30-day window, chronology and stripped author name/user ID only','hidden_from_analyst':['self answers','questioner comments','questioner later question revisions','current acceptance/score','answer revisions outside 30 days'],'indirect_exposures':[{'case_id':'IM-A1','url':'https://stackoverflow.com/revisions/77774667/2','location':'UPDATE paragraph','exposed_fact':'Non-questioner reply mentions an encountered error without full original author comment','used_for_filter_judgment':False},{'case_id':'IM-A1','url':'https://stackoverflow.com/questions/77774582#comment137123139_77774582','location':'comment body','exposed_fact':'Non-questioner comment quotes an inability to open a QuickMagick::Image object','used_for_filter_judgment':False}],'blindness_claim':'not fully blind: the two cited non-author proposal/diagnostic texts indirectly expose a later failure. Neither is retrofitted into initial.csv or used as evidence of awareness/result before seal.','candidate_counts':{'actual':10,'blank':2,'a_returned':sum(bool(r['a'].get('returned_rank')) for r in ordered),'b_returned':sum(bool(r['b'].get('returned_rank')) for r in ordered)},'preseal_review_adjustment':'Root questioned merging general perspective and explicit +distort: retained separate C1/C2 with shared-component relation because missing first sign/bounds prevents proving exact identity. This review occurred before second seal, without official or author-followup evidence.','complete_within_accessible_api':True,'pagination':'answers/comments/revisions each one page, has_more=false; all included nonauthor answers have public revision1','remaining_limitations':['deleted/private posts or comments not accessible','comment past text cannot be recovered from current API','comments on answers not returned by bounded answer endpoint could be absent; no such parent is inferred','no official documentation or 90-day author followup read in this stage']}
(OUT/'proposals-exposure.json').write_text(json.dumps(exposure,ensure_ascii=False,indent=2))
print(json.dumps(exposure['candidate_counts'],ensure_ascii=False))
