"""Frozen candidate coding before official behavioral evidence or author follow-up."""
import datetime as dt,hashlib,json,pathlib
BASE=pathlib.Path(__file__).resolve().parents[2];OUT=BASE/'evidence/typst';CACHE=BASE/'.cache/typst'
xs=json.loads((CACHE/'proposals-third-party-only.json').read_text()); initial={x['case_id']:x for x in json.loads((OUT/'initial-part.json').read_text())}
now=dt.datetime.now(dt.timezone.utc).isoformat()

def ref(kind,ident,rev=None):
 return next(x for x in xs if x['kind']==kind and (x.get('comment_id')==ident if kind=='comment' else x['post_id']==ident and x['revision_number']==rev))

def loc(x,s):
 b=x['body'];p=b.index(s)
 return {'source_url':x['url'],'fixed_revision_url':x.get('fixed_url'),'body_sha256':x['body_sha256'],'body_char_start':p,'body_char_end_exclusive':p+len(s),'html_line_start':b[:p].count('\n')+1,'html_line_end':b[:p+len(s)].count('\n')+1,'short_excerpt':s}

css=ref('comment',137137082)
box=ref('answer_revision',77790346,1)
page=ref('answer_revision',77878373,1)
helper=ref('answer_revision',77878373,2)
helper2=ref('answer_revision',77878373,3)
red=ref('answer_revision',77894083,1)
redcomment=ref('comment',137401034)
red2=ref('answer_revision',77894083,2)
rows=[]
def add(case,rank,src,operation,product,product_id,delta,sameprod,sameop,oproof,needle,original_links=None,merged=None,unknown=None,original_spelling=None):
 cid=f'{case}-C{rank}';b=initial[case]
 adrop=sameprod is True
 bdrop=sameop is True
 x={'candidate_id':cid,'case_id':case,'question_id':b['question_id'],'blank':False,'original_rank':rank,'proposal_utc':dt.datetime.fromtimestamp(src['created'],dt.timezone.utc).isoformat(),'proposal_timestamp':src['created'],'ordering_key':[src['created'],src.get('comment_id',src['post_id']),src['body'].index(needle)],'source_kind':src['kind'],'source_post_id':src['post_id'],'source_comment_id':src.get('comment_id'),'source_revision_number':src.get('revision_number'),'author':src['owner'].get('display_name'),'original_proposal_url':src['url'],'original_fixed_url':src.get('fixed_url'),'original_links':original_links or [],'other_links_in_source':['https://typst.app/docs/reference/layout/box/#parameters-outset'] if src==box else [],'research_official_url':None,'research_official_section':None,'operation':operation,'original_spelling':original_spelling,'product':product,'product_normalized':product_id,'difference_from_initial':delta,'same_product_as_actual_use':sameprod,'product_identity_proof':('initial actual_products includes Typst; candidate calls Typst constructs' if sameprod else 'initial actual_products empty: actual use unconfirmed' if case.startswith('TY-U') else 'CSS hook/renderer not identified; current document Typst, no evidence of a shared product identity'),'same_operation_as_actual_attempt':sameop,'operation_identity_proof':oproof,'identity_unknowns':unknown or [],'A_decision':'exclude' if adrop else 'keep','A_reason':'same actually tried product: Typst' if adrop else 'actual use/product identity unconfirmed','B_decision':'exclude' if bdrop else 'keep','B_reason':'same input+arguments+stage positively established' if bdrop else ('동일성 미확인: '+ '; '.join(unknown) if unknown else '기존 조작과 본문상 차이; 동일 조작 입증 안 됨'),'A_returned_position':None,'B_returned_position':None,'A_rank_shift':None,'B_rank_shift':None,'return_explanation':delta,'judged_utc':now,'evidence':[loc(src,needle)],'merged_origin_urls':merged or [],'historical_limit':src['historical_scope'],'official_behavior_verified':False,'author_knowledge_or_success_used':False,'validity_before_official_read':'미확인','duplicate_or_alias_note':None}
 rows.append(x)
add('TY-A1',1,css,'If a CSS hook exists, apply CSS border to the elements.','CSS renderer / hook unspecified','unknown_css_host','Initial actual code is Typst grid/page background; no CSS-capable rendering path is stated.',None,None,'No source maps the conditional CSS hook to the actual Typst document or prior attempt.','border: 2px 2px black',unknown=['CSS host/integration','input element representation','valid border syntax/effect'],original_spelling='border: 2px 2px black')
add('TY-A1',2,box,'Wrap every authors.map item in author-box; inside it use box(width:100%,height:100%,stroke:...) rather than one stroked page-background block.','Typst','typst','Stroke moves from page-background grid to a box around each author item; full grid-cell dimensions.',True,False,'Initial pre1 has one stroked block in page background; proposal pre1 wraps each mapped author in box. Different syntactic container/processing stage.','..authors.map(author =&gt; author-box[')
add('TY-A1',3,box,'Use box outset as an alternative margin/size treatment around the per-author content; numeric outset not provided.','Typst','typst','An outset option around author-box content is proposed; no outset occurs in initial tried code.',True,None,'Option is named but no numeric value or fully specified replacement invocation is supplied, so full input/argument identity is unconfirmed.','outset',original_links=['https://typst.app/docs/reference/layout/box/#parameters-outset'],unknown=['outset amount','which width/height parameters remain in the alternative'],original_spelling='outset')
add('TY-A2',1,red,'Keep colMath helper and introduce outer #let red = red, then call colMath from math mode without # before the function.','Typst','typst','Helper body is identical to baseline; the added outer binding changes caller state so red can be referenced as a math variable.',True,False,'Initial failure explicitly says red is not defined after removing function #; proposal adds an outer definition not present in that failed caller. Function-body identity alone is insufficient.','#let red = red',merged=[red2['fixed_url'],ref('comment',137412871)['url']])
add('TY-A2',2,redcomment,'Call colMath in math mode and use #red for the color argument.','Typst','typst','Code-mode escape is attached to the color argument, while the function call and math content stay in math mode.',True,False,'Baseline shows #colMath($s_2^-$, red) and reports failed no-# caller with plain red; proposal specifies #red at the argument.','$colMath(s_2, #red)$',merged=[ref('comment',137449135)['url'],red2['fixed_url'],ref('comment',137560926)['url']],original_spelling='$colMath(s_2, #red)$')
add('TY-U1',1,page,'Place a pagebreak before and after the figure; use the answer’s stated align(center+horizon) centering step.','Typst','typst','No Typst operation was claimed tried. This is explicit manual page separation; original requested equivalence may imply automatic floating but does not settle it.',None,None,'Initial describes a LaTeX analogue, with no asserted Typst execution.','<code>#pagebreak</code>',unknown=['prior Typst operations','exact scope of align around pagebreak alternative'],original_spelling='#pagebreak before and after the figure')
add('TY-U1',2,page,'Place the figure in a page container with local set align(center+horizon).','Typst','typst','A standalone page container isolates the captioned figure and scopes center+horizon alignment. Baseline is only a LaTeX example.',None,None,'Initial has no actual Typst input/call to compare.','#page[',unknown=['prior Typst operations'])
add('TY-U1',3,helper,'Define my-fig(..args,placement:none); placement="p" dispatches to page[align;figure], other values dispatch to figure(..args,placement:placement).','Typst','typst','Adds a helper with conditional placement dispatch, allowing page behavior to be requested at the call site.',None,None,'Initial names LaTeX figure[p] but never asserts execution of this Typst helper or any equivalent call.','#let my-fig(..args, placement: none)',merged=[ref('comment',137323182)['url']],unknown=['prior Typst operations','whether the author wants automatic float placement'],original_spelling='placement: "p"')
# Fixed slots: non-proposals remain blank; no outside search fills them.
for case in ['TY-A1','TY-A2','TY-U1','TY-U2']:
 for rank in range(1,4):
  if not any(x['case_id']==case and x['original_rank']==rank for x in rows):
   rows.append({'candidate_id':f'{case}-C{rank}','case_id':case,'question_id':initial[case]['question_id'],'blank':True,'original_rank':rank,'blank_reason':'No additional concrete third-party operation observed in the complete 30-day answer/comment acquisition.','A_decision':'blank','B_decision':'blank','A_returned_position':None,'B_returned_position':None,'A_rank_shift':None,'B_rank_shift':None,'judged_utc':now,'evidence':['proposals-acquisition.json','proposals-exposure.json'],'author_knowledge_or_success_used':False})
rows.sort(key=lambda x:(['TY-A1','TY-A2','TY-U1','TY-U2'].index(x['case_id']),x['original_rank']))
for case in initial:
 for filt in ['A','B']:
  kept=[x for x in rows if x['case_id']==case and x[filt+'_decision']=='keep']
  for pos,x in enumerate(kept,1):
   if pos<=2:x[filt+'_returned_position']=pos;x[filt+'_rank_shift']=x['original_rank']-pos
   else:x[filt+'_survives_but_outside_top2']=True
# Exact source-repetition joins do not count as additional candidate observations.
rows[[x['candidate_id'] for x in rows].index('TY-A2-C1')]['duplicate_or_alias_note']='The helper body is already known; the candidate is an added binding/caller-state operation, not a renamed new helper.'
rows[[x['candidate_id'] for x in rows].index('TY-A2-C2')]['duplicate_or_alias_note']='Comment instruction and later answer revision repeat the same #red operation; original sources merged, not counted twice.'
rows[[x['candidate_id'] for x in rows].index('TY-U1-C3')]['duplicate_or_alias_note']='Revision3 replaces selector string "p" by page value with corresponding condition/caller changes. Kept as a later implementation variant in pool, not substituted for the first occurrence.'
(OUT/'candidate-part.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
pool=[{'case_id':'TY-A1','pool_order':4,'url':box['fixed_url'],'operation':'box inset alternative','disposition':'after first three; not returned or evaluated by A/B','evidence':loc(box,'inset')},{'case_id':'TY-A1','pool_order':5,'url':box['fixed_url'],'operation':'grid column-gutter addition','disposition':'after first three; not returned or evaluated by A/B','evidence':loc(box,'column-gutter')},{'case_id':'TY-U1','pool_order':4,'url':helper2['fixed_url'],'operation':'my-fig selector and comparison changed from "p" to page; matching caller changed','disposition':'later selector variant after first three; no replacement of sealed first helper','evidence':loc(helper2,'if placement == page')},{'case_id':'TY-U1','url':ref('comment',137323182)['url'],'operation':'custom function wrapping page','disposition':'same helper implementation described again; merged with C3'},{'case_id':'TY-A2','url':red2['fixed_url'],'operation':'outer red binding and #red argument','disposition':'both repeat previously selected C1/C2; origins merged'},{'case_id':'TY-U1','urls':[ref('comment',137294834)['url'],ref('comment',137417647)['url']],'disposition':'site-migration discussion; no document operation'},{'case_id':'TY-A2','urls':[ref('comment',137349814)['url'],ref('comment',137412871)['url'],ref('comment',137449135)['url'],ref('comment',137560926)['url']],'disposition':'scope explanation, existing candidate repetition, or incorporation acknowledgement; no third distinct operation'}]
(OUT/'proposal-pool.json').write_text(json.dumps(pool,ensure_ascii=False,indent=2))
ex=json.loads((OUT/'proposals-exposure.json').read_text())
ex.update({'analyst_viewed_projection_utc':now,'actual_model_exposure':'6 third-party answer revisions and 9 third-party comments; no OP text or accepted marker.','contextual_leakage':['Non-OP comment137323182 addresses the question author and says the answer was updated to be less manual; OP message itself hidden.','Non-OP comments debate their interpretation of TY-A2 original requirement; no author follow-up content read.'],'complete_window_by_case':[{'case_id':c,'from':dt.datetime.fromtimestamp(v['creation_date'],dt.timezone.utc).isoformat(),'through':dt.datetime.fromtimestamp(v['creation_date']+2592000,dt.timezone.utc).isoformat(),'selected_real_candidates':sum(x['case_id']==c and not x['blank'] for x in rows),'blank_slots':sum(x['case_id']==c and x['blank'] for x in rows)} for c,v in initial.items()],'original_proposal_count':8,'blank_slots':4,'outcome_or_official_behavior_used_to_select':False})
(OUT/'proposals-exposure.json').write_text(json.dumps(ex,ensure_ascii=False,indent=2))
source_summaries={
 'SO-P-137137082-0': 'Conditional CSS hook; border:2px 2px black proposed for element outlines; no host identified.',
 'SO-P-77790346-1': 'Per-author box wrapper with 100% width/height and silver dashed stroke; separate outset/inset margin and column-gutter alternatives.',
 'SO-P-77878373-1': 'Manual pagebreak before/after or page container; center+horizon alignment and captioned figure example.',
 'SO-P-137294834-0': 'Suggests moving discussion to tex.stackexchange.com; no document operation.',
 'SO-P-77878373-2': 'Adds my-fig wrapper: placement p selects page/align/figure branch, other placements use figure.',
 'SO-P-137323182-0': 'Answerer describes updated less-manual page-wrapping helper; repeats revised answer operation.',
 'SO-P-77894083-1': 'Defines red in outer code scope then calls existing colMath from math mode; helper body repeats initial request.',
 'SO-P-77878373-3': 'Changes my-fig selector from string p to page value with matching condition/caller; later variant beyond first three.',
 'SO-P-137349814-0': 'Explains code/math builtin scope using nabla analogy; no new concrete third operation.',
 'SO-P-137401034-0': 'Proposes argument-local #red escape in math call, without redefining red.',
 'SO-P-137412871-0': 'Answerer interprets original goal as avoiding # in caller; repeats outer-binding rationale.',
 'SO-P-137417647-0': 'Disagrees with migrating question to TeX because semantics differ; no document operation.',
 'SO-P-137449135-0': 'Explains that #red avoids plain-red math-variable error while preserving math function calling; repeats candidate2.',
 'SO-P-77894083-2': 'Adds #red alternative to existing outer-binding answer; two prior operations, not new candidates.',
 'SO-P-137560926-0': 'Answerer acknowledges incorporating another answerer comment; no request-author success observation.'
}
sources=[]
for x in xs:
 if not any(s['source_id']==('SO-P-'+str(x.get('comment_id',x['post_id']))+'-'+str(x.get('revision_number',0))) for s in sources):
  sid='SO-P-'+str(x.get('comment_id',x['post_id']))+'-'+str(x.get('revision_number',0))
  sources.append({'source_id':sid,'questions':['Q3','Q4'],'case_ids':[x['case_id']],'category':'proposal_within_selected_request','original_url':x['url'],'direct_open_url':next(z['url'] for z in json.loads((OUT/'proposals-acquisition.json').read_text()) if ('/comments?' in z['url'] if x['kind']=='comment' else '/revisions?' in z['url'])),'fixed_url':x.get('fixed_url',x['url']),'checked_utc':now,'author':x['owner'].get('display_name'),'publisher':'Stack Overflow','lineage':'Stack Overflow question '+str(x['question_id']),'version':('comment'+str(x['comment_id'])+' current public body' if x['kind']=='comment' else 'answer'+str(x['post_id'])+' revision'+str(x['revision_number'])),'location':'body chars0:'+str(len(x['body']))+'; candidate-specific char/line ranges in candidate-part/proposal-pool','sha256':x['body_sha256'],'confirmed':source_summaries[sid],'supports_or_refutes':'Supports order, duplicate joins, blank slots, and source-versus-research-link separation.','limitations':x['historical_scope']+'; not an author success/new-awareness observation','counted':False,'duplicate_reason':'same selected public request lineage; do not inflate eight independent cases'})
(OUT/'sources-proposals.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
print(json.dumps({'rows':len(rows),'real':sum(not x['blank'] for x in rows),'blank':sum(x['blank'] for x in rows),'returned_A':[x['candidate_id'] for x in rows if x.get('A_returned_position')],'returned_B':[x['candidate_id'] for x in rows if x.get('B_returned_position')]},ensure_ascii=False,indent=2))
