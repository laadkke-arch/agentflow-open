"""Curate already-read public R records; performs no network requests."""
import csv
import datetime
import hashlib
import json
import pathlib
import re

B = pathlib.Path(__file__).resolve().parent
E = B / 'evidence'
RAW = B / '.workbench'
def read(sid):
    return (RAW / (sid + '.body')).read_bytes()
def jread(sid):
    return json.loads(read(sid))
def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')

baseline = [x for x in map(json.loads, (B/'sources.jsonl').read_text().splitlines()) if x['id'] in {x[0] for x in json.loads((B/'phase1-inputs.json').read_text())}]
baseline_ids = {x['id'] for x in baseline}
receipts = {p.name.removesuffix('.receipt.json'):json.loads(p.read_text()) for p in E.glob('*.receipt.json')}
rows = list(baseline)
attempts=[]
for sid,r in sorted(receipts.items(), key=lambda x:(x[1]['read_utc'],x[0])):
    if sid in baseline_ids:
        continue
    # Public response cookies and transport client identifiers are not needed evidence.
    r['headers']={k:v for k,v in r.get('headers',{}).items() if k.lower() not in ['set-cookie','x-ip']}
    dump(E/(sid+'.receipt.json'),r)
    case = 'R1' if sid.startswith('R1-') else ('R2' if sid.startswith('R2-') else 'R1;R2')
    lineage = 'github-pages-official-contract' if sid.startswith('R-SERVICE') else ('consumer-archive-v1.1.12' if case=='R1' else 'consumer-asciicast-v2.3.1')
    kind='publication_metadata'; eligible=True; observation=''; limit=''; sec='response body'; version='current retrieval of historical record'
    data=None
    try:data=jread(sid)
    except (ValueError,UnicodeError):pass
    extract=None
    if r['status']!=200:
        kind='access_failure';eligible=False
        observation=f"HTTP {r['status']} at stated UTC; historical payload unavailable."
        limit='Does not establish historical deployment failure or no capture. Affects publication logs/reader paths.'
        extract={'status':r['status'],'bytes':r['bytes'],'body_message':read(sid).decode(errors='replace')[:160] if r['bytes']<1000 else 'HTTP error body retained only in ignored raw cache.'}
    elif sid=='R-SERVICE-STATUS':
        kind='service_help';version='current service documentation @2026-11-23';sec='About deployment statuses / Data retention / Create a deployment status: auto_inactive'
        observation='현재 공식문서는 이전 상태 기록을90일 보존하고 그보다 오래된 이전 상태는REST/GraphQL에서 삭제하며 현재 상태는배포 나이와무관하게 유지한다고 설명한다. 자동 inactive는같은환경의이전성공배포에 추가된다.'
        limit='현재 조회에서 성공 이력이 사라질 수 있다는 설명. 2025 당시 정책 시작일/개별삭제 이력 및 관측 inactive가자동생성되었는지는미확인. 상태이름만으로 과거success를직접관측했다고세지않음.'
        extract={'section':sec,'quote':'Previous statuses older than 90 days are automatically deleted','paraphrase':'Current state is retained regardless of deployment age. Automatic inactive applies to prior successful non-transient, non-production deployments; manual inactive remains possible.'}
    elif 'CDX' in sid or 'AVAILABLE' in sid:
        kind='archive_locator';eligible=False
        observation=('정해진 URL/기간의CDX 결과가빈배열이다.' if data==[] else 'Wayback closest locator를읽었다; 실제내용판독과분리한다.')
        if sid=='R1-WAYBACK-AVAILABLE':observation+=' closest2025-02-27T04:30:36Z는주창밖/보조창안.'
        if sid=='R1-LEAF-AVAILABLE':observation+=' closest2025-11-21T13:49:24Z는보조창밖이므로내용조회제외.'
        if sid=='R2-WAYBACK-AVAILABLE':observation+=' closest2024-03-16T10:18:49Z는보조창밖이므로내용조회제외.'
        limit='빈색인/검색지시자는제공부재나실패증거가아니다; 내용확인점수0.';extract=data
    elif 'DISCUSSIONS-WINDOW' in sid:
        kind='search_result';eligible=False
        observation=f"범위한정GitHub원문검색 total_count={data['total_count']}, incomplete={data['incomplete_results']}; 생성UTC순서로모든본문판독."
        if case=='R1':observation+=' #111컴파일경고수정,#112CRAN경고,#113릴리스체크리스트; 구판문서유지기간약속없음.'
        limit='검색응답은원자료최소량제외. #113은정식issueendpoint로별도판독. API검색은GitHub Discussions별도탭전체를망라하지않음.'
        extract={'total_count':data['total_count'],'incomplete_results':data['incomplete_results'],'items':[{k:x.get(k) for k in ['number','created_at','html_url','title']} for x in data['items']]}
    elif sid=='R1-ARCHIVED-FEB27':
        kind='archived_http_response';version='2025-02-27T04:30:36Z / archive1.1.11';sec='captured HTML title; navbar line36; root examples'
        observation='보조창의root응답을실제로열어gzip해제한HTML에서archive1.1.11와예제를읽음;1.1.12출판전판이다.'
        limit='주관측창밖. 2025-03-24..26의root/leaf제공상태를입증하지않음. 아카이브전달gzip바이트와해제HTML지문을분리.'
        extract={'capture_utc':r['capture_utc'],'version':'1.1.11','title':'Multi-Format Archive and Compression Support • archive','download_bytes':r['bytes'],'download_sha256':r['direct_sha256'],'decoded_bytes':r['decoded_bytes'],'decoded_sha256':r['decoded_sha256']}
    elif 'GENERATED-COMMIT' in sid or sid in ['R1-NEXT-COMMIT','R1-LAST-COMMIT']:
        kind='generated_artifact_metadata';version=data['sha'];sec='commit.message; author/committer.date; changed file blob SHA'
        observation=f"생성커밋 {data['sha']}@{data['commit']['author']['date']}: {data['commit']['message']}. 생성HTML파일blobSHA와읽은파일의gitSHA1을대조."
        limit='커밋메시지는발행자의source provenance주장;R1선택소스는7자리접두만보고한다. 빌드run증명/서버의실제응답은별도.'
        extract={'sha':data['sha'],'commit':data['commit'],'selected_files':[{k:f.get(k) for k in ['sha','filename','status','blob_url']} for f in data['files'] if f['filename'] in ['index.html','reference/archive_read.html','articles/asciicast-demo.html','pkgdown.yml','dev/pkgdown.yml']]}
    elif any(x in sid for x in ['GENERATED-ROOT','GENERATED-LEAF','NEXT-ROOT','NEXT-LEAF','LAST-ROOT','LAST-LEAF']):
        kind='generated_html';body=read(sid);txt=body.decode();v=re.findall(r'title="Released version"[^>]*>([^<]+)',txt);version=';'.join(v)
        sec='navbar Released version; title; main text / usage or example'
        observation=f"고정생성커밋의HTML을직접읽음: 판{version}, {len(body)}bytes."
        if 'NEXT' in sid or 'LAST' in sid:
            observation+=' 다음또는주창마지막dev재생성커밋의root/leaf가선택45e0d9eb생성물과바이트동일하다.'
            eligible=False
        elif case=='R1':observation+=' 현재root/leaf1.1.14와바이트다름.'
        else:observation+=' 현재root/leaf2.3.1과바이트동일하다.'
        limit='Git생성물응답이며그당시공개도메인응답이아니다. 전체사이트assets/실행/연속성은미검사.'
        if not eligible: limit+=' 동일HTML의후속커밋조회는재게시반례검사용이며원자료최소량에서중복제외.'
        extract={'version':v,'title':re.search(r'<title>(.*?)</title>',txt,re.S).group(1),'direct_git_blob_sha1':hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest(),'direct_sha256':r['direct_sha256'],'bytes':len(body)}
    elif 'PKGDOWN-MANIFEST' in sid:
        kind='generated_metadata';sec='pkgdown; last_built; urls';version='selected output commit'
        observation=read(sid).decode().strip().replace('\n','; ')
        limit='발행자가생성물에쓴시각/목적URL;HTTP게재시각이나파일별산출물목록은아니다.'
        extract={'original':read(sid).decode()}
    elif sid.endswith('WORKFLOW') or sid.endswith('ORIGINAL-CONFIG'):
        kind='publisher_configuration';sec='.github/workflows/pkgdown.yaml build/deploy steps' if sid.endswith('WORKFLOW') else '_pkgdown.yml url/development.mode'
        observation=('R1non-PR은deploy_to_branch,PR은build_site;R2는build_site_github_pages뒤JamesIvesaction으로docs->gh-pages,clean:false. ' if sid.endswith('WORKFLOW') else 'root URL과development.mode:auto를선언;root/dev구분의설정의도. ')
        limit='설정본문을실제성공run/게시승인/경로응답으로세지않는다.'
        extract={'path':sec,'selected_lines':[f'L{i}: {l}' for i,l in enumerate(read(sid).decode().splitlines(),1) if any(q in l for q in ['mode:','url:','deploy_to_branch','build_site','clean:','branch: gh-pages','folder: docs','JamesIves'])]}
    elif sid=='R1-MAINTENANCE':
        kind='publisher_maintenance_note';sec='Current state / Known outstanding issues / Future directions'
        observation='안정화상태·UTF-8locale·암호보호archive향후방향. 웹문서구판유지기간약속없음.';limit='태그고정제품유지보수의견으로웹게시보증아님.';extract={'headings':['Current state','Known outstanding issues','Future directions'],'retention_promise_found':False}
    elif sid in ['R1-RELEASE','R2-RELEASE']:
        kind='publisher_release';version=data['tag_name'];sec='release target_commitish/published_at/body'
        observation=f"{data['name']} published{data['published_at']}, target{data['target_commitish']}. "+('No changes.' if case=='R1' else 'write_svg(show)/play개선;문서옛판유지정책없음.')
        limit='패키지릴리스와웹게시시각은다름.';extract={k:data.get(k) for k in ['id','tag_name','target_commitish','created_at','published_at','name','html_url']}
    elif sid=='R1-RELEASE-ISSUE':
        kind='publisher_release_decision';version='issue113 updated2025-03-24T12:33:05Z';sec='Prepare for release; Wait for CRAN checked list'
        observation='발행자#113에서urlchecker::url_check,GitHub release,dev-version bump를체크했다. 옛문서기간/영구판주소약속은없다.'
        limit='체크표시는발행자보고;명령원로그·당시응답200/판지문은아니다. 이슈수정이력전체미보존.'
        extract={k:data.get(k) for k in ['number','created_at','updated_at','html_url','state']};extract['checked_items']=['urlchecker::url_check()','usethis::use_github_release()','usethis::use_dev_version(push = TRUE)']
    elif sid=='R1-CRAN-COMMENTS':
        kind='excluded_discussion';eligible=False;sec='issue112 comment2741755308'
        observation='2025-03-20comment는릴리스가아직필요하다는내용;문서보존약속없음.';limit='제품CRAN수정논의로이과제자료량분모에서제외.';extract=[{k:x.get(k) for k in ['id','created_at','body','html_url']} for x in data]
    elif sid=='R1-COMBINED-STATUS' or 'CHECKRUNS' in sid or 'PAGES-RUNS-WINDOW' in sid or sid=='R2-DEPLOYMENTS-SOURCE':
        kind='empty_history_lookup';eligible=False
        observation='해당API의현재조회결과가빈목록이다. '+('combined state pending,total_count0은기록공석.' if sid=='R1-COMBINED-STATUS' else '')
        limit='옛실행/게시가없거나실패했다는반증이아니다. 삭제/보존한계가능.'
        extract={k:data.get(k) for k in ['state','sha','total_count','statuses','check_runs','workflow_runs']} if isinstance(data,dict) else data
    elif 'STATUS-' in sid or sid.endswith('DEPLOYMENT-STATUSES'):
        kind='deployment_status';sec='complete returned status array (no Link pagination)'
        observation='; '.join(f"status{x['id']} {x['state']}@{x['created_at']};environment_url={x['environment_url']!r};log={x['log_url']}" for x in data)
        limit='현재남은상태만읽음. 이전상태90일보존정책으로과거상태순서가소실될수있다;inactive만으로success/failure를대신하지않음.'
        if sid=='R1-STATUS-2329713750':limit+=' 이inactive시각은2025-10-21로주창/보조창밖;주창최종상태에소급하지않음.'
        extract=data
        (E/(sid+'.original.json')).write_bytes(read(sid))
    elif 'DEPLOYMENT' in sid:
        kind='deployment_object';sec='deployment ID, input sha/ref, UTC, environment/statuses_url'
        ds=data if isinstance(data,list) else [data]
        relevant=[x for x in ds if (case=='R2' or '2025-02-22'<=x.get('created_at','')<'2025-04-26')]
        extract=[{k:x.get(k) for k in ['id','created_at','updated_at','sha','ref','environment','statuses_url']} for x in relevant]
        observation=f"조회{len(ds)}개객체;관련{len(relevant)}개ID/입력SHA/시각판독. R1주창11개,보조창17개;선택객체입력45e0d9eb. R2출력SHA에1283145596객체발견." if case=='R1' else 'R2생성commit92fecbc0를입력으로한deployment1283145596@2024-01-21T20:55:45Z발견.'
        limit='객체생성은서버게시성공이아님. 다음페이지가있으면읽어대상창범위를확인함.'
        if sid in ['R1-DEPLOYMENTS-SAME','R1-DEPLOYMENTS-ALL-P2']:
            eligible=False;limit+=' 중복조회/창밖메타데이터로원자료최소량에추가하지않음.'
    else:
        raise RuntimeError('Unclassified '+sid)
    if extract is not None:dump(E/(sid+'.extract.json'),extract)
    rows.append({'id':sid,'lineage_id':lineage,'kind':kind,'url':r['url'],'version':version,'section':sec,'read_utc':r['read_utc'],'Q':['Q1','Q3','Q5','Q7'],'cases':case.split(';'),'claim_ids':['R-SERVICE-HISTORY' if case=='R1;R2' else case+'-HISTORY'],'observed':observation,'observer':'AF-RES-086 r_routes direct public retrieval and reading','support_refute':'supports-limited-claim; constrains-overclaim','limitations':limit,'receipt_path':'streams/r/evidence/'+sid+'.receipt.json','extract_path':'streams/r/evidence/'+sid+'.extract.json','direct_sha256':r['direct_sha256'],'publisher_hash':None,'bytes':r['bytes'],'primary_count_eligible':eligible})
    if not eligible:attempts.append({'id':sid,'url':r['url'],'read_utc':r['read_utc'],'status':r['status'],'reason':observation,'effect':limit,'original_count':0})

(B/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
(B/'attempts.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in attempts))
comparisons=json.loads((E/'file-comparison.json').read_text())
routes=[]
specs=[('R1','archive','a4c6ec37fc8737a189ca7ec7095ec0161888f9e8','45e0d9ebc168cf3632bc2d737c9db2318668a826','2025-03-24T00:00:00Z','2025-03-27T00:00:00Z',2328795124),('R2','asciicast','f992b26f3cb30c799fbb95f6148852d8ae8a7f18','92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1','2024-01-21T20:53:46Z','2024-01-24T20:53:46Z',1283145596)]
for case,repo,sha,out,start,end,dep_id in specs:
    commit=jread(case+'-GENERATED-COMMIT')
    dep=jread('R1-DEPLOYMENT') if case=='R1' else jread('R2-DEPLOYMENTS-OUTPUT')[0]
    statuses=jread(case+'-DEPLOYMENT-STATUSES')
    routes.append({'route_id':case+'-SOURCE-OUTPUT','case_id':case,'stage':'publisher_source_to_generated_commit','source_sha':sha,'publisher_source_identifier':'a4c6ec3' if case=='R1' else sha,'generated_commit':out,'generated_at_utc':commit['commit']['author']['date'],'publisher_message':commit['commit']['message'],'build_run_id':None,'window_start_utc':start,'window_end_utc_exclusive':end,'source_ids':[case+'-GENERATED-COMMIT',case+'-RELEASE',case+'-PKGDOWN-MANIFEST'],'limitation':'publisher provenance statement, not independently executed build'})
    routes.append({'route_id':case+'-DEPLOYMENT','case_id':case,'stage':'deployment_current_retained_status','source_sha':sha,'deployment_id':dep_id,'deployment_input_sha':dep['sha'],'created_utc':dep['created_at'],'environment':dep['environment'],'status_sequence_observed':[{k:x.get(k) for k in ['id','state','created_at','environment_url','log_url']} for x in statuses],'final_retained_status':'inactive','provider_reported_success_directly_observed':False,'historical_prior_success':'unconfirmed; auto_inactive possible inference only','source_ids':[case+'-DEPLOYMENT-STATUSES','R1-DEPLOYMENT' if case=='R1' else 'R2-DEPLOYMENTS-OUTPUT','R-SERVICE-STATUS'],'limitation':'previous statuses may have been pruned after90days; no whole historical sequence'})
    for x in [a for a in comparisons if a['case_id']==case]:
        part='ROOT' if x['file']=='index.html' else 'LEAF';cur=receipts[case+'-CURRENT-'+part];art=receipts[x['source_id']]
        routes.append({'route_id':case+'-'+part,'case_id':case,'stage':'generated_file_vs_current_reader_response','source_sha':sha,'generated_commit':out,'path':x['file'],'artifact_id':x['publisher_git_blob_sha1'],'publisher_hash_kind':'git_blob_sha1','publisher_hash':x['publisher_git_blob_sha1'],'direct_git_blob_sha1':x['direct_git_blob_sha1'],'direct_generated_sha256':x['direct_sha256'],'artifact_read_utc':art['read_utc'],'response_utc':cur['read_utc'],'final_url':cur['final_url'],'current_http_status':cur['status'],'current_sha256':cur['direct_sha256'],'current_matches_generated_bytes':x['current_equal'],'generated_version':x['version'][0],'current_version':'1.1.14' if case=='R1' else '2.3.1','section':'archive_read usage/examples' if case=='R1' and part=='LEAF' else ('asciicast-demo Example / Using SVG files' if case=='R2' and part=='LEAF' else 'root examples'),'historical_main_window_reader_response':'unconfirmed','source_ids':[x['source_id'],case+'-GENERATED-COMMIT',case+'-CURRENT-'+part],'limitation':'current byte comparison does not establish historical serving interval or whole site'})

all_deps=jread('R1-DEPLOYMENTS-ALL')+jread('R1-DEPLOYMENTS-ALL-P2')
timeline=[]
for d in sorted([x for x in all_deps if '2025-03-24'<=x['created_at']<'2025-03-27'],key=lambda x:x['created_at']):
    sid='R1-DEPLOYMENT-STATUSES' if d['id']==2328795124 else 'R1-STATUS-'+str(d['id']);status=jread(sid)[0]
    x={'deployment_id':d['id'],'input_sha':d['sha'],'created_at':d['created_at'],'retained_status':status['state'],'retained_status_at':status['created_at'],'status_in_main_window':'2025-03-24'<=status['created_at']<'2025-03-27','environment_url':status['environment_url'],'log_url':status['log_url'],'source_id':sid}
    timeline.append(x)
    routes.append({'route_id':'R1-REPUBLISH-'+str(d['id']),'case_id':'R1','stage':'republish_sequence','source_ids':['R1-DEPLOYMENTS-ALL',sid],**x,'limitation':'object/status timestamps do not identify unavailable earlier statuses, if any, or reader responses'})
dump(E/'R1-republish-timeline.json',timeline)
for label in ['NEXT','LAST']:
    commit=jread('R1-'+label+'-COMMIT');items=[]
    for part in ['ROOT','LEAF']:
        body=read('R1-'+label+'-'+part);initial=read('R1-GENERATED-'+part);items.append({'file':'index.html' if part=='ROOT' else 'reference/archive_read.html','equal_selected':body==initial,'direct_sha256':hashlib.sha256(body).hexdigest()})
    routes.append({'route_id':'R1-RETAINED-'+label,'case_id':'R1','stage':'generated_release_files_retained_across_dev_republish','generated_commit':commit['sha'],'generated_utc':commit['commit']['author']['date'],'publisher_message':commit['commit']['message'],'files':items,'source_ids':['R1-'+label+'-COMMIT','R1-'+label+'-ROOT','R1-'+label+'-LEAF'],'limitation':'two samples do not establish all intermediate generated trees or serving intervals'})
routes.append({'route_id':'R1-SUPPLEMENT-ROOT','case_id':'R1','stage':'archived_reader_response_supplement','capture_utc':'2025-02-27T04:30:36Z','response_version':'1.1.11','original_url':'https://archive.r-lib.org/','final_url':receipts['R1-ARCHIVED-FEB27']['final_url'],'direct_download_sha256':receipts['R1-ARCHIVED-FEB27']['direct_sha256'],'decoded_sha256':receipts['R1-ARCHIVED-FEB27']['decoded_sha256'],'source_ids':['R1-ARCHIVED-FEB27','R1-WAYBACK-AVAILABLE'],'limitation':'before selected1.1.12 and outside main window'})
(B/'routes.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in routes))

summary={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'requests_with_receipts':len(receipts),'download_bytes':sum(r['bytes'] for r in receipts.values()),'source_rows':len(rows),'primary_material_rows':sum(x['primary_count_eligible'] for x in rows),'conservative_lineages':sorted(set(x['lineage_id'] for x in rows if x['primary_count_eligible'])),'source_sha_to_generated_reported_links':'2/2','direct_git_blob_hash_matches':'4/4','provider_success_directly_observed':'0/2','retained_selected_status_identified':'2/2 inactive','reader_paths_identified_in_main_window':'0/4','currently_selected_version_reader_paths':'2/4','current_bytes_equal_selected_generated_html':'2/4','R1_additional_republish_same_selected_html':'4/4 at NEXT and LAST generated snapshots','dual_owner_requirements':'0/2 withinR subset; inherited whole6 denominator unchanged','dual_condition_joint_confirmation':'0/0 산출불가 for R1/R2 because no second owner promise','R1_deployment_objects_main':11,'R1_status_rows_main':10,'R1_status_rows_outside_main_and_supplement':1,'historical_failure_then_success_observed':False,'checks':{'4_publisher_blob_hashes_match_direct_git_objects':all(x['direct_git_blob_sha1']==x['publisher_git_blob_sha1'] for x in comparisons),'R1_current_pairs_differ':all(not x['current_equal'] for x in comparisons if x['case_id']=='R1'),'R2_current_pairs_equal':all(x['current_equal'] for x in comparisons if x['case_id']=='R2')},'cost_by_case':{c:{'requests':sum(k.startswith(c+'-') for k in receipts),'download_bytes':sum(v['bytes'] for k,v in receipts.items() if k.startswith(c+'-'))} for c in ['R1','R2']},'shared_service_help_requests':sum(k.startswith('R-SERVICE') for k in receipts),'shared_service_help_download_bytes':sum(v['bytes'] for k,v in receipts.items() if k.startswith('R-SERVICE')),'web_search_calls_without_byte_count':2,'web_search_queries':5}
dump(B/'summary.json',summary)
assert all(summary['checks'].values())
print(json.dumps(summary,ensure_ascii=False,indent=2))
