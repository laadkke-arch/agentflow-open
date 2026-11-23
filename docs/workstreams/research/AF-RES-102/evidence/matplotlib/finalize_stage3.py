import json,csv,hashlib,datetime,re,io
from pathlib import Path
from lxml import html
from fetch import ROOT
R=ROOT;now=datetime.datetime.now(datetime.timezone.utc).isoformat()
A=json.load(open(R/'main-audit-raw.json'))['records'];S=json.load(open(R/'selected-stage2.json'))['selected'];BY={x['case_id']:x for x in S};D=json.load(open(R/'supplemental-audit-raw.json'))['pairs'];E=json.load(open(R/'editions.json'))
GT={'old':{x['path']:x for x in json.load(open(R/'old-publication-tree.json'))['tree']},'new':{x['path']:x for x in json.load(open(R/'cache/stage2-new-edition-tree.bin'))['tree']}}
DOC={'old':'655f616e86e2c0f7724d7c88717d4ac4eb438c57','new':'235131a6bc2527aee7eea370fd5f94564a48c20d'}
main_review={
'MP-G1':{'purpose':'ImageGrid의 2×2 셀에서 행 또는 열의 종횡비를 2로 설정했을 때 배치가 달라지는 원리','old_source_lines':'7–22','new_source_lines':'7–22','reason':'두 배포 Python 소스가 동일하고 ImageGrid 두 개의 같은 인덱스에 set_aspect(2)를 적용한다. 양쪽 절이 같은 001 그림을 직접 참조한다. PNG 픽셀은 같고 Software 메타데이터 등 바이트 지문은 다르다.','role_change':'없음'},
'MP-G2':{'purpose':'AxesDivider.append_axes로 오른쪽·위쪽에 색상 막대를 붙이고 위쪽 막대의 눈금 위치를 조정','old_source_lines':'14–39','new_source_lines':'14–39','reason':'본문의 append_axes 설명과 배포 소스가 양판에 같으며 right/top으로 만든 cax를 colorbar에 전달한다. 첫 그림과 2x srcset을 양판에서 확인했다.','role_change':'없음'},
'MP-C1':{'purpose':'두 이미지 축의 종횡비를 유지하면서 HBoxDivider로 높이를 같게 조정','old_source_lines':'15–43','new_source_lines':'17–32','reason':'옛 그림의 설명 상자가 신판에서는 본문 설명으로 옮겨졌고 첫 그림은 여전히 두 축의 같은 높이를 설명한다. 신판 두 번째 그림은 VBoxDivider의 같은 너비를 추가한다. 저자 commit 8ecd60d가 같은 소스 파일에 VBox 예제를 추가한 변경을 확인한다. 기존 예제를 삭제한 것이 아니다.','role_change':'기존 HBox 목적 유지 + VBox 목적 추가; title/fragment 변경'},
'MP-C2':{'purpose':'첫 그림에서 inset_axes의 절대/상대 크기, loc, borderpad로 네 모서리에 삽입 축을 배치','old_source_lines':'9–40','new_source_lines':'9–40','reason':'첫 그림 생성부의 실행 코드는 같고 뒤 설명 및 제목의 대소문자/구두점이 바뀌었다. 소스 blob 변화가 목적 변화라는 결론을 반박한다. 그림 픽셀은 같고 PNG Software 메타데이터가 판별로 달라진다.','role_change':'없음'}
}
supp_purposes={
'MP-S01':'곡선 격자/극좌표를 직사각형 축 안에 표시하면서 axis_direction에 따른 축 방향을 비교',
'MP-S02':'감쇠 사인파 데이터를 생성기로 공급하고 애니메이션 도중 x축 범위를 확장',
'MP-S03':'선의 y 데이터를 반복 변경하여 사인 곡선을 이동시키는 애니메이션',
'MP-S04':'축에 고정한 텍스트·도형·크기 막대와 anchored helper의 배치',
'MP-S05':'첫 그림에서 Divider의 고정 인치 크기·간격과 locator로 축 격자를 배치',
'MP-S06':'부동 축의 방향, 축 제목 방향, 눈금 문자 방향을 나란히 비교',
'MP-S07':'host 축의 위쪽 twin 축에 π 단위 눈금을 추가',
'MP-S08':'inset_axes로 색상 막대의 위치·높이·너비를 통제',
'MP-S09':'확대한 inset image 옆에 inset colorbar를 덧붙임',
'MP-S10':'zoomed_inset_axes와 크기 막대·mark_inset 연결로 확대 영역을 설명',
'MP-S11':'새 관측마다 베이지안 사후분포를 갱신하고 이론값 수직선과 비교',
'MP-S12':'첫 그림에서 Divider/Size.Fixed로 축의 실제 인치 크기와 여백을 고정',
'MP-S13':'산점도와 주변 히스토그램을 make_axes_locatable로 정렬',
'MP-S14':'ImageGrid로 폭이 다른 세 이미지를 공통 배치 안에 정렬',
'MP-S15':'AxesX/AxesY와 Divider로 서로 다른 축 범위에 비례한 2×2 배치를 설정',
'MP-S16':'AxesZero에서 원점을 지나는 x/y 축에 화살표 스타일을 설정',
'MP-S17':'HostAxes/twin 변환으로 고유운동과 선속도 단위를 한 그림의 양 축에 연결',
'MP-S18':'axes divider로 이미지 오른쪽에 상대 너비 색상 막대를 배치',
'MP-S19':'첫 그림에서 긴 y 눈금 문자가 들어가도록 축 면적을 자동 조정',
'MP-S20':'2×2 이미지 격자에 공통 또는 개별 색상 막대를 배치하는 여러 구성을 비교'
}
# Exact main semantic adjudication after source/caption/URI/payload inspection.
rows=[]
for a in A:
 x=BY[a['case_id']];ed=a['edition'];a['G']='미확인'
 if a['vacancy']:
  a.update({'P':'미확인','U':'미확인','U_reason':'Frozen first40 had no absent-path candidates; this is a vacant slot, not an observed negative.','generation_search':'evidence/matplotlib/generation-search.json'})
  rows.append({'case_id':a['case_id'],'project':'Matplotlib','edition':ed,'version':a['version'],'vacant':True,'P':'미확인','U':'미확인','G':'미확인','legacy_path_P':'미확인','evidence':'evidence/matplotlib/audit.json','limitation':a['reason']});continue
 rev=main_review[a['case_id']];a['U']='YES';a['semantic_review']=rev;a['review_utc']=now;a['logical_role_retained']=True;a['legacy_reference_U']='YES';a['legacy_resource_role_U']='YES';a['provisional_fragment_valid']=a['old_fragment_present'];a['static_fragment_scope']='Full fixed HTML id search; no browser execution or generic JS anchor alias inferred.'
 t=html.fromstring((R/'cache'/(Path(a['body_receipt']).stem+'.bin')).read_bytes());sec=t.xpath('//*[@id=$x]',x=a['section_id'])[0]
 a['paragraph_locations']=[p.sourceline for p in sec.xpath('./p') if 'Gallery generated' not in p.text_content()]
 b=(R/'cache'/(Path(a['body_receipt']).stem+'.bin')).read_bytes();path=x['page_path'];gb=hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest();a['body_git_blob_sha1']=gb;a['body_matches_publication_blob']=gb==GT[ed][path]['sha']
 for q in a['first_payloads']:
  pb=(R/'cache'/(Path(q['receipt']).stem+'.bin')).read_bytes();gb=hashlib.sha1(f'blob {len(pb)}\0'.encode()+pb).hexdigest();q['git_blob_sha1']=gb;q['matches_publication_blob']=gb==GT[ed][q['path']]['sha']
 a['G_missing_link']='Exact source/docs/publication commit and created-window run/status/check searches returned no retained records. Build rules and byte identity do not identify a particular generating invocation or output manifest.'
 a['generation_search']='evidence/matplotlib/generation-search.json';q=a['first_payloads'][0]
 row={'case_id':a['case_id'],'project':'Matplotlib','edition':ed,'version':a['version'],'vacant':False,'body_url':a['body_url'],'section_url':a['section_url'],'section_locator':f'section#{a["section_id"]}, HTML L{a["section_lines"][0]}–L{a["section_lines"][1]}','literal_reference':q['literal'],'base_uri':a['body_url'],'payload_url':q['url'],'payload_mime':'image/png','payload_bytes':q['bytes'],'payload_sha256':q['sha256'],'P':a['P'],'U':'YES','G':'미확인','legacy_path_P':a['legacy_path_P'],'source_url':a['delivered_source']['url'],'publication_url':'https://github.com/matplotlib/matplotlib.github.com/commit/'+E[ed]['publication_sha'],'evidence':'evidence/matplotlib/audit.json','receipt':a['body_receipt']+';'+q['receipt'],'limitation':'Reference/use verified, browser/example execution not performed; exact byte-generation job missing.','actual_fragment':a['section_id'],'provisional_fragment_valid':a['provisional_fragment_valid'],'srcset_urls':';'.join(p['url'] for p in a['first_payloads'][1:]),'source_sha256':a['delivered_source']['sha256'],'documented_source_sha':DOC[ed],'release_source_sha':E[ed]['source_sha'],'legacy_reference_U':'YES','legacy_resource_role_U':'YES'}
 rows.append(row)
for cid in main_review:
 _both=[a for a in A if a['case_id']==cid and not a['vacancy']]
 _sets=[]
 for a in _both:
  _html=html.fromstring((R/'cache'/(Path(a['body_receipt']).stem+'.bin')).read_bytes())
  _sets.append(set(_html.xpath('//*[@id]/@id')))
 _shared=sorted(i for i in _sets[0].intersection(_sets[1]) if i.startswith('sphx-glr-gallery-'))
 for a in _both:a['shared_generated_source_anchors']=_shared
for x in D:
 if x['id']=='MP-S11':x['inherited_work_exclusion']='098 sources.jsonl MPL-OLD-FINAL-bayes_update already read same3.7.0 example work; both editions excluded from new minimum.'
 x['logical_U']='YES';x['purpose_review']={'purpose':supp_purposes[x['id']],'review_utc':now,'basis':'Both scoped bodies, first figure URI/JS expression, delivered Python source and source diff directly read. AST/pixel equality are auxiliary, not sole purpose evidence.','same_role':True}
 if x['id']=='MP-S02':x['purpose_review']['change']='New source explicitly saves100frames; generator and expanding x-axis purpose continues. Inherited098 work excluded from minimum.'
 elif x['id']=='MP-S20':x['purpose_review']['change']='Code refactored from helpers to direct ImageGrid configurations; same subplot/colorbar configurations and first-figure pixels retained.'
 elif x['id']=='MP-S10':x['purpose_review']['change']='Title gains a space before2; static fragment changes inset-locator-demo2 -> inset-locator-demo-2; old role retained.'
 else:x['purpose_review']['change']='Same source operations, or prose-only changes, preserve described first-figure role.'
 x['counterexample_results']={'type1_path_present_but_not_used':False if x['new']['legacy_path_applicable'] else 'not-applicable-inline','type2_old_path_absent_successor_used':'not-eligible-no-old-relative-path' if not x['new']['legacy_path_applicable'] else False,'type3_same_name_and_hash_different_purpose':False,'type4_bytes_differ_same_purpose':not x['comparison']['first_payload_bytes_same']}
fields=['case_id','project','edition','version','vacant','body_url','section_url','section_locator','literal_reference','base_uri','payload_url','payload_mime','payload_bytes','payload_sha256','P','U','G','legacy_path_P','source_url','publication_url','evidence','receipt','limitation','actual_fragment','provisional_fragment_valid','srcset_urls','source_sha256','documented_source_sha','release_source_sha','legacy_reference_U','legacy_resource_role_U']
with open(R/'lineage.csv','w') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
first_body=min(a['body_utc'] for a in A if not a['vacancy'] and a['edition']=='new');first_payload=min(json.load(open(R/Path(p['receipt']).relative_to('evidence/matplotlib')))['utc'] for a in A if not a['vacancy'] and a['edition']=='new' for p in a['first_payloads'])
corrections=[{'issue':'Initial scope end estimated from serialized lxml newline count','fix':'Final main bounds use matching section close via HTMLParser source positions','impact':'No URI/payload/selection/prediction or U changes'}, {'issue':'Inline JS frame parser required semicolon although assignments omit it; raw None==None equality was not valid','fix':'Optional semicolon; first PNG decoded; equality requires real digests; JS Image.src and target img connections retained','impact':'No frozen selection or prediction changed; final supplemental20/20 bytes differ; first3 inline digests now valid'}, {'issue':'Stage2 reproduction script had no early truncated-tree failure guard','fix':'Added guard to unsealed stage2.py after review without rerunning or rewriting sealed data','impact':'Observed new tree already truncated=false; no actual outcome changes'}]
audit={'project':'Matplotlib','versions':['3.6.3','3.7.0'],'stage1_remote_commit':'5f664a87df16f453151ec985e9ad37913e3bda90','prediction_seal_commit':'f1c5d6ff927fd5fbe108565598810ca7e94c5753','prediction_seal_verified_utc':'2026-11-23T22:07:47.803Z','first_new_main_body_utc':first_body,'first_new_main_payload_utc':first_payload,'adjudicated_utc':now,'main':A,'source_distribution_links':'evidence/matplotlib/source-distribution-links.json','generation_search':'evidence/matplotlib/generation-search.json','source_docs_revision':DOC,'main_summary':{'slots':12,'pairs_filled':4,'pairs_vacant':2,'P_yes':8,'U_yes':8,'U_no':0,'G_unknown_filled':8,'general':{'TP':2,'FP':0,'FN':0,'TN':0,'abstention':0,'vacancy':0,'actual_positive':2,'actual_negative':0},'resource_absent':{'TP':0,'FP':0,'FN':0,'TN':0,'abstention':0,'vacancy':2,'actual_positive':0,'actual_negative':0},'source_changed':{'TP':2,'FP':0,'FN':0,'TN':0,'abstention':0,'vacancy':0,'actual_positive':2,'actual_negative':0},'provisional_static_fragment_corrections':['MP-C1'],'negative_denominator_warning':'No observed negative in either filled stratum; specificity/false-positive-rate undefined. Do not aggregate stratum error rates.'},'supplemental_summary':{'scoped_pairs':20,'external_first_images':17,'inline_JS_first_images':3,'logical_U_yes':20,'logical_U_no':0,'bytes_differ_same_role':20,'pixel_changes':2,'fragment_changes':['MP-S10'],'type1_found':0,'type2_found':0,'type3_found':0,'type3_same_name_and_hash_opportunities':0,'inherited_exclusion':['MP-S02','MP-S11'],'note':'Auxiliary search not inserted into main denominator; actual first-frame image is decoded, animation/browser execution unperformed.'},'self_corrections':corrections,'review_scope':'This worker semantic adjudication is self-review; root/another-agent stage-selection review is separate. No human review claimed.'}
(R/'audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
(R/'supplemental-audit.json').write_text(json.dumps({'fixed_order_source':'supplemental-order.json','review_utc':now,'pairs':D,'summary':audit['supplemental_summary']},ensure_ascii=False,indent=2)+'\n')
(R/'self-corrections.json').write_text(json.dumps(corrections,ensure_ascii=False,indent=2)+'\n')
returns=[]
for x in S:
 cid=x['case_id']
 if x['vacancy']:returns.append({'case_id':cid,'decision':'유보','reason':'no eligible A candidates in sealed frame; cannot fabricate a historical/current example link','next_minimal_check':'A separately preregistered version/frame could examine deletion; do not fill this frozen vacancy after outcome.'});continue
 old=next(a for a in A if a['case_id']==cid and a['edition']=='old');new=next(a for a in A if a['case_id']==cid and a['edition']=='new')
 oldurl='https://github.com/matplotlib/matplotlib.github.com/blob/'+E['old']['publication_sha']+'/3.6.3/'+x['page_path']+'#L'+str(old['section_lines'][0]);live='https://matplotlib.org/3.7.0/'+x['page_path']+'#'+new['section_id']
 warning='이 링크는 조사한3.7.0 예제이며2026년 최신판·새 생성 실행을 증명하지 않습니다.'
 if cid=='MP-C1':warning='옛 #hboxdivider-demo는 이3.7.0 정적 본문에 없습니다. #hboxdivider-and-vboxdivider-demo의 첫 HBox 그림을 보세요.'
 returns.append({'case_id':cid,'decision':'두 판 병기' if cid=='MP-C1' else '목적에 따라 옛판 유지/새 위치 제공','historical_citation_url':oldurl,'historical_section':old['section_id'],'historical_payload_url':old['first_payloads'][0]['url'],'current_selected_version_url':live,'current_section':new['section_id'],'current_fixed_body_url':new['section_url'],'shared_generated_source_anchor_url':E['new']['live_base_url']+x['page_path']+'#'+new['shared_generated_source_anchors'][0] if new['shared_generated_source_anchors'] else None,'shared_anchor_scope':'Observed both fixed editions only, not a permanence promise; static DOM verified.','current_payload_url':new['first_payloads'][0]['url'],'reproduction_source_url':'https://github.com/matplotlib/matplotlib/blob/'+DOC['new']+'/'+x['tag_source_path'],'reproduction_distribution_url':json.load(open(R/'new-distribution.json'))['url'],'reproduction_rule_url':'https://github.com/matplotlib/matplotlib/blob/d6dd1b79142e4e2483244c25ff1e3ddb664722d3/doc/devel/release_guide.rst#L359','reproduction_missing':'actual generating invocation/environment/output digest manifest; sourceZIP/guide not proof that historical bytes will regenerate','cheaper_sufficient_check':'설명만 읽으면 정확판 본문+실제 fragment 1회. 그림 재사용이면 해당 절→payload 1회 추가. 생성 귀속을 묻지 않으면 CI 조회 생략.','warning':warning,'root_live_validation':['evidence/return-url-checks.json','evidence/return-url-scope-comparison.json','evidence/live-payload-checks.json'],'new_definition':'current selected edition3.7.0, not2026latest'})
(R/'returns.json').write_text(json.dumps(returns,ensure_ascii=False,indent=2)+'\n')
# Merge detailed primary ledger, with cross-version work deduplication.
SOURCES={}
for p in ['sources-stage1.jsonl','sources-stage2.jsonl']:
 for line in (R/p).read_text().splitlines():
  q=json.loads(line);SOURCES[q['source_id']]=q
for k in ['MP-new-release','MP-new-pub-metadata-com']:
 if k in SOURCES:SOURCES[k]['countable']=False;SOURCES[k]['duplicate_reason']='Inherited098 same3.7.0 release/publication event; retained as input evidence, not new minimum'
for k in ['MP-old-doc-revision']:
 if k in SOURCES:SOURCES[k]['questions']=['Q1','Q5']
def add(key,category,obs,cases,questions,countable=True,dup='',location='',lineage=None):
 rp=R/'receipts'/f'{key}.json'
 if not rp.exists():return
 r=json.load(open(rp));sid='MP-'+key
 q={'source_id':sid,'questions':questions,'cases':cases,'original_url':r['url'],'fixed_url':r['url'],'accessed_utc':r['utc'],'publisher':'Matplotlib maintainers','lineage':lineage or 'Matplotlib release/docs publication lineage','category':category,'version':'3.6.3' if ('/3.6.3/' in r['url'] or 'old' in key) else '3.7.0','location':location or key,'sha256':r['sha256'],'observation':obs,'claims_supported':[obs],'claims_refuted':[],'limitations':['Static publication/reference/content evidence; no exact invocation-to-output generation proof.'],'countable':bool(countable and r['status']==200),'duplicate_reason':dup if r['status']==200 else 'Failed response excluded','receipt':'evidence/matplotlib/receipts/'+key+'.json'}
 if sid in SOURCES:
  # Do not recalculate old count decisions solely because the same receipt was reused.
  old=SOURCES[sid];q['countable']=old['countable'];q['duplicate_reason']=old['duplicate_reason'];q['accessed_utc']=old['accessed_utc']
 SOURCES[sid]=q
for a in A:
 if a['vacancy']:continue
 cid=a['case_id'];ed=a['edition'];work='Matplotlib example '+BY[cid]['page_path'];main=main_review[cid]
 add(Path(a['body_receipt']).stem,'example_body',main['purpose']+'; '+main['reason'],[cid],['Q4','Q6','Q7'],ed=='old','Same article/work across editions; old edition counted once' if ed=='new' else '',f'HTML L{a["section_lines"][0]}–L{a["section_lines"][1]}, section#{a["section_id"]}',work)
 for i,p in enumerate(a['first_payloads']):add(Path(p['receipt']).stem,'image_payload',main['purpose']+f'; PNG {p["image"]["width"]}×{p["image"]["height"]}, {p["bytes"]} bytes; exact publication Git blob matches.',[cid],['Q4','Q6'],ed=='old' and i==0,'Same illustrative work across edition/density variants; counted once at old1x' if ed=='new' or i>0 else '',p['path'],work+' first figure')
 add(Path(a['delivered_source']['receipt']).stem,'example_source',main['reason']+'; downloaded .py directly read.',[cid],['Q4','Q6'],False,'Same code represented in example body; exact source retained without double counting',main[ed+'_source_lines'],work)
 add(f'exact-doc-source-{cid}-{ed}','example_source','Actual documented source revision, delivered .py and official gallery ZIP member have identical SHA256 for this example.',[cid],['Q1','Q4'],False,'Duplicate exact source bytes already represented by downloaded .py/body',BY[cid]['tag_source_path'],work)
for x in D:
 work='Matplotlib example '+x['frame_path'];inherited=bool(x['inherited_work_exclusion'])
 for ed in ['old','new']:
  q=x[ed];body=q['body'];fig=q['first_figure'];src=q['source'];dup='Inherited098 example work (animate_decay or bayes_update); not new' if inherited else 'Same article/work across editions; old counted once' if ed=='new' else ''
  add(Path(body['receipt']).stem,'example_body',supp_purposes[x['id']]+'; '+x['purpose_review']['change'],[x['id']],['Q4','Q6'],ed=='old' and not inherited,dup,f'HTML L{body["section_lines"][0]}–L{body["section_lines"][1]}, section#{body["section_id"]}',work)
  add(Path(src['receipt']).stem,'example_source',supp_purposes[x['id']]+'; both delivered sources and operative source change reviewed.',[x['id']],['Q4','Q6'],False,'Code duplicates the same illustrative work in body',src['path'],work)
  if fig['kind']=='external':add(Path(fig['receipt']).stem,'image_payload',supp_purposes[x['id']]+f'; PNG {fig["image"]["width"]}×{fig["image"]["height"]}, {fig["bytes"]}B; current exact section resolves this first figure.',[x['id']],['Q4','Q6'],ed=='old' and not inherited,'Inherited098 work' if inherited else 'Same figure work across versions, old counted once' if ed=='new' else '',fig['path'],work+' first figure')
# Official publication/build rules and author evidence.
extra=[
('new-doc-revision','publication_record','New HTML source metadata resolves to235131a6bc2527aee7eea370fd5f94564a48c20d; commit comments out next-release notes.',True,''),
('new-gallery-index','distribution_record','Exact publication gallery index links the official Python ZIP.',False,'Discovery pointer; opened source ZIP counted once'),
('new-gallery-bundle','distribution_bundle','Opened1296753B ZIP with522members; all four selected sources match corresponding documented source revision and deployed download bytes.',False,'Same gallery source distribution work across versions; old bundle counted once'),
('build-old-release-guide','build_rule','L359–398 separates installed release tag, ver-doc source, html/pdf build and manual rsync into versioned publication repository.',False,'Inherited098 same release-guide work; repeated old/new identical bytes not new minimum'),
('build-new-release-guide-tag','build_rule','Same release guide bytes as old; versioned publication copy is distinct from generation.',False,'Inherited098 same release-guide work and identical old-guide bytes'),
('hbox-author-commit','change_record','Author commit8ecd60d (2022-10-17) modifies HBox example to add VBox and test; supports purpose continuation plus expansion.',True,''),
('change-hbox-history','change_record','Path history points to8ecd60d; history query used to locate exact author change.',False,'Same change event as exact author commit'),
('main-MP-C1-new-vbox-payload','image_payload','New second picture demonstrates vertically arranged axes with equal widths, supporting added VBox role distinct from preserved first HBox role.',True,'')]
for ed in ['old','new']:
 for kind,obs in [('circle-config','CircleCI config defines documentation build artifacts, doctree cache and doc bundle; no selected output digest binding.'),('deploy-docs','L5–23 restricts main non-PR deployment and copies doc/build/html into matplotlib/devdocs; not a selected release-publication run.'),('doc-conf','Release build image compression, 2x srcset, animation support and plot_gallery controls are configuration, not invocation evidence.'),('doc-makefile','Makefile exposes Sphinx html and html-noplot (plot_gallery=0); an HTML build can be configured without fresh gallery images.')]:extra.append((f'build-{ed}-{kind}','build_rule',obs,ed=='old','Same build-rule work across two revisions; old counted once' if ed=='new' else ''))
for key,cat,obs,co,du in extra:add(key,cat,obs,[],['Q1','Q4','Q5','Q6'],co,du)
for q in json.load(open(R/'generation-search.json'))['queries']:
 add(q['id'],'build_search',f'Exact queried scope {q["target"]}; HTTP{q["http_status"]}; visible retained count{q.get("total_count")}. No historical nonexistence inferred.',[],['Q5'],False,'Empty historical lookup is a search receipt, not an additional primary work',q['url'])
# Reconcile same work already directly read in098, without altering sealed earlier ledgers.
for _key in ['MP-build-old-doc-conf','MP-build-new-doc-conf']:
 if _key in SOURCES:SOURCES[_key]['countable']=False;SOURCES[_key]['duplicate_reason']='Inherited098 MPL-DOC-CONF same doc/conf.py work across versions; not a new primary work'
for _id,_q in SOURCES.items():
 if _q.get('cases')==['MP-C1'] and 'main-new-body' in _id:_q['claims_refuted']=['Same page/image path guarantees the historical title-derived fragment stays valid.']
# Same byte content is counted once, even if different work IDs were given.
seen={}
for q in SOURCES.values():
 if not q['countable']:continue
 digest=q.get('sha256')
 if digest and digest in seen:q['countable']=False;q['duplicate_reason']='Identical bytes to '+seen[digest]+'; not counted twice'
 elif digest:seen[digest]=q['source_id']
(R/'sources.jsonl').write_text(''.join(json.dumps(q,ensure_ascii=False)+'\n' for q in SOURCES.values()))
counts={'source_rows':len(SOURCES),'unique_countable_primary':sum(q['countable'] for q in SOURCES.values()),'categories':{},'main':audit['main_summary'],'supplemental':audit['supplemental_summary'],'count_policy':'Same work across editions/density/code presentation merged. Identical bytes across work IDs merged. Inherited3.7.0 release/pub event, release guide, doc/conf.py, animate_decay and bayes_update work excluded. Frame-only automated scans uncounted. Empty jobs and failed URLs uncounted.'}
for q in SOURCES.values():
 if q['countable']:counts['categories'][q['category']]=counts['categories'].get(q['category'],0)+1
(R/'counts-project.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2)+'\n')
assert len(rows)==12 and sum(not r['vacant'] for r in rows)==8
assert all(a['body_matches_publication_blob'] and all(p['matches_publication_blob'] for p in a['first_payloads']) for a in A if not a['vacancy'])
assert len(D)==20 and all(x['logical_U']=='YES' and x['old']['first_figure'].get('sha256') and x['new']['first_figure'].get('sha256') for x in D)
print(json.dumps(counts,ensure_ascii=False,indent=2))
