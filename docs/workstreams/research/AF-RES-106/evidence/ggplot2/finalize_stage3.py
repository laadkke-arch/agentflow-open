"""Derive post-seal adjudication artifacts from inspected, immutable raw evidence.

Does not write the frozen frame/predictions/SCOPE. Run with python -B.
Judgments are explicit author readings below, not inferred from equal hashes.
"""
from pathlib import Path
import json, hashlib, datetime, re, collections, subprocess

D = Path(__file__).resolve().parent
ROOT = D.parents[1]
UTC = datetime.datetime.now(datetime.timezone.utc).isoformat()
SEAL = '8054c2221d4023ba03c904d96f13928219d36c3d'
OBS = {
 'GG-M1': '양판 첫 예제는 seed596의 diamonds100행, carat/price, shape=cut 및 순서형 shape 경고를 유지한다. 정확한 R/scale-shape.r→R/scale-shape.R 이동을 Upkeep diff와 현재 @examples로 연결했다. 새 PNG가 해당 절의 첫 img로 직접 참조된다.',
 'GG-M2': '양판 mtcars wt/mpg 산점도에 같은 한 행 df(2.62,21.0→3.57,15.0)를 사용한 geom_curve와 geom_segment가 있다. R/geom-segment.r→.R은 R100, geom-curve는 include 경로 교정과 함께 제거/추가되어 diff와 rdname/호출로 후계를 확인했다.',
 'GG-G1': '양판 seed596의 diamonds1000행, cut/carat/clarity, geom_boxplot(outlier.size=0), geom_point(pch=21,position_jitterdodge())가 같다. 새 이미지의 그룹별 상자와 점을 직접 확인했다. 내부 ndodge 계산 변경은 같은 공개 방법의 소멸이 아니다.',
 'GG-G2': '양판 economics date/unemploy, linewidth=uempmed, geom_line(lineend="round") 첫 예제가 같다. 시간축 실업자수와 중앙 실업기간의 선 두께를 PNG에서 확인했다.',
 'GG-X1': '양판 첫 예제는 mtcars vs/am의 geom_point(alpha=0.1) 기준 그림이다. 두 번째 stat="unique" 결과로 첫 예제를 바꾸지 않는다. PNG의 네 겹침 위치와 author @examples를 확인했다.',
 'GG-X2': '양판 첫 예제는 mtcars mpg/wt 산점도의 cyl 연속 색상 범례를 labs(colour="Cylinders")로 이름 짓는다. R/labels.R의 첫 @examples(update_labels)가 아니라 labs의 두 번째 @examples와 연결한다.',
 'GG-X3': '양판 mtcars2 wt/mpg/gear 산점도에 제목·부제·caption·Figure1과 theme_gray()를 붙인 첫 예제가 같다. theme_bw 등 뒤 예제를 첫 예제로 교체하지 않았다.',
 'GG-S1': '사전 지정 대표 register_theme_elements: custom ggxyz.panel.annotation을 element_text와 el_def로 등록하고 CoordCartesian render_fg/element_render를 호출하여 blue annotation을 표시한다. R/theme-elements.r→.R R100 이동 뒤 같은 첫 코드가 남는다.',
 'GG-S2': '사전 지정 대표 guide_axis: mpg cty*100/hwy*100을 class별 facet_wrap하고 guide_axis(n.dodge=2)를 쓰는 첫 코드가 남는다. R/guides-axis.r→R/guides-axis.R 이후 ggproto rewrite에서 R/guide-axis.R로 구현이 바뀌지만 공개 예제 API 방법은 이어진다.',
}
EVENT_OBS = {
 '04a5ef274e912bee76180154b25d8bca0206feb1': 'Upkeep2023의 .r→.R 변경. scale-shape, geom-segment, theme-elements는 R100. geom-curve는 include 경로가 바뀌어 exact-rename 모드에서 D/A로 보였지만 GitHub rename 분류·diff·새 @examples/rdname을 함께 읽으면 역할 계승이다.',
 'b9f43f2a7d93548b0794bc527b0f18ff0f028681': 'guide system을 ggproto로 변경; R/guides-axis.R 삭제와 R/guide-axis.R 추가. guide_axis(n.dodge=2)의 공개 예제는 새 저자 소스와 발행 절에 유지된다. 내부 class/dispatch 변경을 독자 API 방법 실패로 세지 않았다.',
 '5074f11bb10f28e37f89c1601400f4a5bffcd9f4': 'R/range.r의 내부 Range/continuous_range/discrete_range를 없애고 scales의 ContinuousRange/DiscreteRange를 쓴다는 NEWS와 호출 교체 diff 확인. @noRd 내부 helper이므로 독자 예제 삭제 사례 분모에 넣지 않는다.',
 '202029b1979c7d92920f2b17fbeb7ddf1d37b208': 'R/utilities-table.R 내부 grob 크기 helper 제거와 Collate 교정 확인. 사전 옛 적격 예제와 연결되지 않아 보조 예제 삭제 분모에서 제외한다.',
 '4daadf7221439831260dedfa901b9616821154b0': 'PositionJitterdodge의 length(unique0(unlist(ndodge)))를 vec_unique_count(unlist(ndodge))로 바꾼 성능 diff. 공개 첫 예제와 position_jitterdodge() API는 양판에 유지된다. 보조 D/R 모집 사건이 아니라 주 G1 해석의 공식 변경 근거다.',
}
def dump(name,obj):
 (D/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def digest(b): return hashlib.sha256(b).hexdigest()
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def rel(p): return str(p.relative_to(ROOT))
rows = json.loads((D/'audit-extraction.json').read_text())['rows']
pred = json.loads((D/'predictions.json').read_text())
predmap = {x['case_id']:x for x in pred}
rawdir = D/'raw'; rawdir.mkdir(exist_ok=True)
sources=[]; validations=[]
prior_raw = subprocess.check_output(['git','show','092f4c5c56451bceb53e632f4bddf33db6cda168:docs/workstreams/research/AF-RES-102/sources.jsonl'],cwd=D,text=True)
prior=json.loads((D/'inherited-exclusions.json').read_text())
prior_urls=set()
for ln in prior_raw.splitlines():
 x=json.loads(ln)
 for key in ['original_url','fixed_url']:
  if x.get(key):prior_urls.add(x[key].split('#')[0])

def record(r,kind,meta,cache,category,countable,observation):
 b=((D/'.cache'/cache) if (D/'.cache'/cache).exists() else (rawdir/cache)).read_bytes()
 assert digest(b)==meta['sha256'],cache
 assert blob(b)==meta['git_blob'],cache
 receipt=json.loads((ROOT/meta['receipt']).read_text())
 assert receipt.get('status')==200 and receipt['sha256']==digest(b),cache
 target=rawdir/cache
 target.write_bytes(b)
 validations.append({'file':rel(target),'sha256':digest(b),'git_blob':blob(b),'receipt':meta['receipt'],'receipt_status':200,'matches':True})
 sid='GG106-S3-'+r['case_id']+'-'+r['edition']+'-'+kind
 example='ggplot2:'+r['page_path']
 origin=meta['url']
 inherited=origin.split('#')[0] in prior_urls
 iscount=bool(countable and not inherited)
 sources.append({'id':sid,'source_id':sid,'questions':['Q4','Q5','Q6','Q7'], 'cases':[r['case_id']], 'original_url':origin,'immutable_url':origin,'fixed_url':origin,'preserved_location':rel(target),'accessed_utc':receipt['accessed_utc'],'direct_read_utc':UTC,'direct_read_method':'AI reread preserved original immutable raw text; PNG separately displayed with view_image where visual_read is true','publisher':'tidyverse/ggplot2','work_lineage':example,'lineage':example,'edition':r['version'],'location':{'fragment':r['fragment'],'section_lines':[r['section_start_line'],r['section_end_line']],'source_path':meta.get('path'),'examples_marker_lines':meta.get('examples_marker_lines')},'fingerprints':{'sha256':digest(b),'git_blob':blob(b),'bytes':len(b)},'sha256':digest(b),'observed':observation,'observation':observation,'supports':['Exact current section/reference/source relationship','Purpose and concrete API adjudication bounded to first example'],'refutes':['Filename/path/hash equality alone establishes semantic use or historical generation'],'limits':'R execution, actual browser fragment navigation and historical build G are 미확인. Received bytes and local image viewing are distinct from a live rendered page.','limitations':'R execution/browser navigation/build G 미확인','status':'계승' if inherited else ('신규' if iscount else '중복'),'category':category,'countable':iscount,'count_reason':'One conservative work-lineage unit; old/new copies and same-example code/payloads not counted again.' if iscount else ('Already counted in AF-RES-102.' if inherited else 'Same logical example already allocated to body or independent payload/source category; supporting read only.'),'duplicate_reason':'' if iscount else example,'logical_example_id':r['case_id'],'receipt':meta['receipt'],'visual_read':kind=='payload'})
 return rel(target)

lineage=[];extras=[]
for r in rows:
 case=r['case_id'];ed=r['edition'];stem=Path(r['page_path']).stem
 bodymeta={'url':r['raw_url'],'sha256':r['body_sha256'],'git_blob':r['body_git_blob'],'receipt':r['body_receipt']}
 # Only 4 main+2 prespecified supplement bodies count; 3 controls are allocated to independent source/payload works.
 bodycount=(r['group'] in ['main','supplemental'] and ed=='new')
 bodyraw=record(r,'body',bodymeta,f'{ed}-body-{stem}.html','body',bodycount,OBS[case])
 payloadraw=record(r,'payload',r['payload'],f'{ed}-asset-{stem}.png','figure_or_source',r['group']=='material_control' and ed=='new',OBS[case]+' PNG 실물을 별도 열람; 본문/소스와 연계했으며 그림 동일성만으로 후계 판정을 하지 않았다.')
 manraw=record(r,'man',r['render_source'],f'{ed}-man-{stem}.Rd','figure_or_source',False,OBS[case]+' man의 generated header와 examples 구간 확인.')
 authorraw=[]
 for i,a in enumerate(r['author_sources'],1):
  authorraw.append(record(r,'author'+str(i),a,ed+'-author-'+a['path'].replace('/','_'),'figure_or_source',False,OBS[case]+' 저자 원 코드 읽기; 공유 Rd의 구현 소스와 직접 @examples 보유 소스를 구분.'))
 actualtree=json.loads((D/('old-tree.json' if ed=='old' else 'new-publication-tree.json')).read_text())
 tree={x['path']:x for x in actualtree['tree'] if x['type']=='blob'}
 assert not actualtree['truncated'] and tree[r['page_path']]['sha']==r['body_git_blob']
 assert tree[r['payload']['relative_path']]['sha']==r['payload']['git_blob']
 assert 'id="'+r['fragment']+'"' in (rawdir/f'{ed}-body-{stem}.html').read_text()
 group=[x for x in rows if x['case_id']==case]; old=next(x for x in group if x['edition']=='old');new=next(x for x in group if x['edition']=='new')
 assert old['first_example_code']==new['first_example_code']
 observation=OBS[case]+' 양판 대표 PNG sha256은 다르다. 첫 코드 문자열 일치와 직접 이미지 판독은 의미 계승을 보조하지만 당시 생성 실행을 입증하지 않는다.'
 row={'case_id':case,'project':'ggplot2','stratum':predmap[case]['stratum'] if case in predmap else r['group'],'edition':ed,'vacant':'NO','version':r['version'],'section_url':r['original_dom_url'],'github_read_url':r['github_url'],'actual_fragment':r['fragment'],'section_start_line':r['section_start_line'],'section_end_line':r['section_end_line'],'payload_url':r['payload']['url'],'payload_urls':[r['payload']['url']],'source_url':r['render_source']['url'],'source_urls':[r['render_source']['url']]+[x['url'] for x in r['author_sources']],'payload_sha256':r['payload']['sha256'],'payload_git_blob':r['payload']['git_blob'],'source_sha256':r['render_source']['sha256'],'source_fingerprints':[r['render_source']]+r['author_sources'],'body_sha256':r['body_sha256'],'P':'YES','legacy_path_P':'YES','old_fragment_arrival':'YES','old_fragment_arrival_scope':'Static DOM id exists at normalized old page path; browser scroll is 미확인','U_original_purpose':'YES','U_visual_role':'YES','method_inherited':'YES','literal_data_identity':'YES','G':'미확인','first_example_code':r['first_example_code'],'observation':observation,'limitations':'R/Python 실행 미실시; raw URL은 text/plain이므로 HTML id 확인과 실제 브라우저 fragment 스크롤/표시를 구별한다. PNG 바이트 변경의 생성 시점/환경/원인 G 미확인.','evidence_files':[rel(D/'audit-extraction.json'),rel(D/'details'/f'{ed}-{stem}.json'),bodyraw,payloadraw,manraw]+authorraw,'evidence_file':rel(D/'details'/f'{ed}-{stem}.json'),'direct_read_utc':UTC,'group':r['group']}
 (lineage if r['group']=='main' else extras).append(row)

for p in pred:
 if p['vacant']=='YES':
  for ed,ver in [('old','3.4.0'),('new','3.5.0')]:
   lineage.append({'case_id':p['case_id'],'project':'ggplot2','stratum':p['stratum'],'edition':ed,'vacant':'YES','version':ver,'section_url':'미확인','actual_fragment':'미확인','payload_url':'미확인','payload_urls':[],'source_url':'미확인','source_urls':[],'payload_sha256':'미확인','source_sha256':'미확인','P':'미확인','legacy_path_P':'미확인','old_fragment_arrival':'미확인','U_original_purpose':'미확인','U_visual_role':'미확인','method_inherited':'미확인','G':'미확인','observation':'완전 새 발행 트리의 옛 대표 자원 경로 부재 후보=0. 탐색을 마친 결원이며 실제 음성/예측 유보와 다르다.','limitations':'실제 사례 없음; 부재 경로의 후계 성능은 이 층에서 측정 불가.','evidence_file':'evidence/ggplot2/stage2-summary.json','evidence_files':['evidence/ggplot2/stage2-summary.json','evidence/ggplot2/frame.csv','evidence/ggplot2/new-publication-tree.json']})
order={p['case_id']:i for i,p in enumerate(pred)}
lineage.sort(key=lambda x:(order[x['case_id']],x['edition']=='new'))
dump('lineage-final.json',lineage);dump('lineage-extra.json',extras)

for sha,obs in EVENT_OBS.items():
 j=json.loads((D/'changes'/f'{sha}.json').read_text())
 if 'committer_date' not in j:
  original=json.loads(((D/'.cache'/f'change-{sha}.json') if (D/'.cache'/f'change-{sha}.json').exists() else (rawdir/f'change-{sha}.json')).read_text())
  j['committer_date']=original['commit']['committer']['date']
 receipt=json.loads((ROOT/j['receipt']).read_text())
 raw=((D/'.cache'/f'change-{sha}.json') if (D/'.cache'/f'change-{sha}.json').exists() else (rawdir/f'change-{sha}.json')).read_bytes()
 assert digest(raw)==receipt['sha256']
 (rawdir/f'change-{sha}.json').write_bytes(raw)
 sid='GG106-S3-EVENT-'+sha[:12]
 sources.append({'id':sid,'source_id':sid,'questions':['Q2','Q4','Q5','Q6'],'cases':['GG-S1'] if sha.startswith('04a5') else (['GG-S2'] if sha.startswith('b9f') else (['GG-G1'] if sha.startswith('4daad') else [])),'original_url':j['url'],'immutable_url':j['url'],'fixed_url':j['url'],'preserved_location':rel(rawdir/f'change-{sha}.json'),'accessed_utc':receipt['accessed_utc'],'direct_read_utc':UTC,'publisher':'tidyverse/ggplot2','work_lineage':'ggplot2-commit:'+sha,'lineage':'ggplot2-commit:'+sha,'edition':'3.4.0→3.5.0 source DAG','location':{'commit':sha,'committer_date':j['committer_date'],'files':[f['filename'] for f in j['files']]},'fingerprints':{'response_sha256':digest(raw)},'sha256':digest(raw),'observed':obs,'observation':obs,'supports':['Different source-path change kinds do not by themselves determine public example continuity'],'refutes':['Every removed R file is a deleted logical reader example'],'limits':'For large API patches, selected exact local Git diff is also preserved. Metadata census complete; semantic outcomes only traced through 2 prespecified representative examples, not all57 linked pages.','limitations':'Actual historical build G 미확인','status':'신규','category':'publication_record','countable':True,'count_reason':'One distinct official author change event, counted once across API metadata/patch/selected diff. Not counted as another logical example.','receipt':j['receipt']})

# Failed convenience-reader requests never count as direct materials; native network raw reread succeeded separately.
for r in rows:
 if r['group']=='main' and r['edition']=='new':
  sid='GG106-S3-FAILED-WEB-'+r['case_id']
  sources.append({'id':sid,'source_id':sid,'questions':['Q4'],'cases':[r['case_id']],'original_url':r['raw_url'],'immutable_url':r['raw_url'],'preserved_location':'evidence/ggplot2/reader-failures.json','accessed_utc':UTC,'publisher':'tidyverse/ggplot2','work_lineage':'ggplot2:'+r['page_path'],'edition':r['version'],'observed':'search_service open returned DisabledError; no source bytes obtained through that reader. Existing raw originals and successful urllib raw response were read instead.','limits':'Failure is not an absence/content judgment.','status':'실패','category':'failed_reader','countable':False,'count_reason':'Failed fetch excluded.'})
dump('reader-failures.json',{'recorded_utc':UTC,'search_service_open_results':[{'case':r['case_id'],'url':r['raw_url'],'error':'DisabledError'} for r in rows if r['group']=='main' and r['edition']=='new'],'fallback':'Preserved exact original raw with HTTP200 receipts, git blob checks; resume-network-check.json independently re-fetched scale_shape unchanged.','optional_parser':'bs4 import failed; no install attempted; standard-library original HTML analysis used.'})
(D/'sources-stage3.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))

returns=[]
for p in pred:
 c=p['case_id']
 if p['vacant']=='YES':
  returns.append({'case_id':c,'project':'ggplot2','stratum':p['stratum'],'vacant':'YES','decision':'유보','old_url':'미확인','new_url':'미확인','old_fragment':'미확인','new_fragment':'미확인','old_payload_url':'미확인','new_payload_url':'미확인','additional_content_http_reads':0,'logical_work_reads':0,'change_condition':'같은 고정판 잔여 모집단에서 규칙에 맞는 실제 옛 외부자원 부재 후보가 발견되면 frame 누락을 먼저 교정 검토. 현재 전수 경로 판독에서는 후보0.','limitations':'결원; 존재하는 독자 질문을 유보한 사례가 아님','evidence_files':['evidence/ggplot2/stage2-summary.json']})
  continue
 pair=[x for x in rows if x['case_id']==c];o=next(x for x in pair if x['edition']=='old');n=next(x for x in pair if x['edition']=='new')
 receipt_files=set()
 for rr in pair:
  receipt_files.update([rr['body_receipt'],rr['payload']['receipt'],rr['render_source']['receipt']]+[a['receipt'] for a in rr['author_sources']])
  if c in ['GG-M1','GG-M2']:receipt_files.add('evidence/ggplot2/receipts/change-04a5ef274e912bee76180154b25d8bca0206feb1.json.json')
  if c=='GG-G1':receipt_files.add('evidence/ggplot2/receipts/change-4daadf7221439831260dedfa901b9616821154b0.json.json')
 after=[f for f in receipt_files if json.loads((ROOT/f).read_text())['accessed_utc']>p['prediction_utc']]
 returns.append({'case_id':c,'project':'ggplot2','stratum':p['stratum'],'vacant':'NO','decision':'두 판 병기','old_url':o['original_dom_url'],'new_url':n['original_dom_url'],'old_github_read_url':o['github_url'],'new_github_read_url':n['github_url'],'old_fragment':o['fragment'],'new_fragment':n['fragment'],'old_payload_url':o['payload']['url'],'new_payload_url':n['payload']['url'],'old_payload_sha256':o['payload']['sha256'],'new_payload_sha256':n['payload']['sha256'],'old_source_url':o['render_source']['url'],'new_source_url':n['render_source']['url'],'new_exact_location':f"#ref-examples; first image at line {n['first_image_line']}; first code block before that image",'additional_content_http_reads':len(after),'additional_content_http_receipts':sorted(after),'logical_work_reads':1+(1 if c in ['GG-M1','GG-M2','GG-G1'] else 0),'cost_definition':'Post-prediction successful original receipt requests attributable to this case (HTML+PNG+Rd+R+relevant official diff). Shared official event can occur in several case costs; do not sum as unique corpus size. Same example versions/artifacts remain one work for minimum-source counting. Resume rereads recorded separately.','support_urls':[o['raw_url'],n['raw_url'],n['render_source']['url']]+[a['url'] for a in n['author_sources']],'rationale':'Historical author can cite immutable old source+payload; reader of compared next release gets verified exact new DOM example and linked payload. Neither raw fragment nor new PNG proves historical generation.','change_condition':'정확한 새 절에서 첫 예제/목적/방법이 빠진다는 원문 관측, source-tag와 발행 예제의 실질 불일치, 또는 실제 브라우저가 fragment를 다른 예제로 보낸다는 관측이면 반환을 유보하거나 옛판 고정 인용으로 바꾼다.','limitations':'Both fixed raw URLs serve text/plain. Browser rendering/scroll 미확인; GitHub #L source-reading URL also supplied, never advertised as a rendered webpage. 2026 latest product guidance is outside these fixed historical versions.','evidence_files':[f'evidence/ggplot2/details/old-{Path(o["page_path"]).stem}.json',f'evidence/ggplot2/details/new-{Path(n["page_path"]).stem}.json']})
dump('returns-final.json',returns)
metrics=[]
for s,n in [('A',0),('M',2),('G',2)]:
 for axis in ['U_original_purpose','U_visual_role','method_inherited']:
  metrics.append({'project':'ggplot2','stratum':s,'axis':axis,'candidate_count':{'A':0,'M':57,'G':11}[s],'slots':2,'filled_pairs':n,'TP':n,'FP':0,'FN':0,'TN':0,'prediction_abstain':0,'outcome_unknown':0,'vacancies':2-n,'actual_positive':n,'actual_negative':0,'FPR':'산출 불가','FPR_reason':'Actual negative denominator=0. Vacancy is not a negative.','sensitivity':1 if n else '산출 불가'})
counted=[x for x in sources if x['countable']]
counts={'written_utc':UTC,'sealed_commit':SEAL,'main_pair_slots':6,'main_edition_slots':12,'main_filled_pairs':4,'main_vacancies':2,'metrics':metrics,'supplemental':{'metadata_D_R_events_all':4,'example_source_events':2,'selected_event_commits':2,'representative_examples':2,'linked_old_example_pages':57,'linked_old_pages_outside_main':55,'semantically_read_representatives':2,'actual_positive':2,'actual_negative':0,'U_unknown':0,'legacy_asset_present_but_selected_section_unused':0,'absent_legacy_asset_with_successor':0,'warning':'Selected events census is complete in specified DAG/R/man; semantic representative trace is limited to two. Do not claim 57 purpose outcomes and do not pool with main confusion tables.'},'minimum_materials':{'counted_new_works':len(counted),'by_category':dict(collections.Counter(x['category'] for x in counted)),'body_work_ids':[x['work_lineage'] for x in counted if x['category']=='body'],'independent_payload_source_work_ids':[x['work_lineage'] for x in counted if x['category']=='figure_or_source'],'official_event_work_ids':[x['work_lineage'] for x in counted if x['category']=='publication_record'],'count_rule':'One work per logical example regardless of two editions, HTML/man/R/PNG. Main/supplement bodies6; disjoint control payload/source works3; official events5. 102 inherited trees and source release metadata count0.','independence_from_102':'Full prior sources.jsonl read at fixed092f4c5; no selected case basename or official event SHA occurs; known first40+aliases excluded in frame.'},'residual_counterexample_search_bounds':{'new_path_membership':'Exhaustive68 eligible legacy representative paths in complete fixed new publication tree','semantic_section_use':'4 main+3 material controls+2 prespecified event representatives; not all68 new bodies','negative_claim':'No ggplot2 P-residual/unreferenced or old-asset-absent successor found within those inspected examples; absence outside that semantic scope is 미확인.'}}
dump('counts-stage3.json',counts)
dump('resume-static-validation.json',{'read_utc':UTC,'command':'python -B docs/workstreams/research/AF-RES-106/evidence/ggplot2/finalize_stage3.py','sealed_commit':SEAL,'verified_files':validations,'verified_count':len(validations),'new_first_example_substitutions':0,'main_pairs':4,'main_vacant_pairs':2,'first_example_code_equal_in_nine_inspected_pairs':True,'interpretation':'Hash equality tests only source-byte identity, not purposes. Purposes above were separately read from original code and inspected PNGs.','runtime_exec':'미실시','historical_G':'미확인'})
print(json.dumps({'lineage_main_rows':len(lineage),'lineage_extra_rows':len(extras),'returns_main_rows':len(returns),'sources_records':len(sources),'counted_new_works':len(counted),'count_categories':counts['minimum_materials']['by_category'],'validated_raw_files':len(validations)},ensure_ascii=False))
