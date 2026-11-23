"""Compile observed Q6 records; never infer successful publication from status labels."""
import csv, hashlib, json, re
from pathlib import Path
P=Path(__file__).resolve().parent
E=P/'evidence'
# Order = creation UTC, then issue number; selection was three per prespecified family.
D={
('readthedocs/readthedocs.org',10990): dict(relevant=False,kind='logging_not_route',finding='관리 서버의 SysLogRenderer 예외와 의존성 pin 논의. 문서 독자 경로 사건이 아님.',reason='생성·게시·독자 응답 연결과 무관한 운영 로그 오류.',quote="'SysLogRenderer' object has no attribute '_level_to_color'",next='없음: 독자 경로 반례 표본에서 탈락.'),
('readthedocs/readthedocs.org',11001): dict(relevant=True,kind='project_deletion',finding='CherryPy 문서가 사라져 모니터링이 경고했고 유지관리자의 프로젝트 삭제가 원인으로 확인되었다.',reason='실제 접근 손실 사례이나 성공한 생성/게시 뒤 route만 틀린 사건은 아님.',quote='removed the project as a reaction to many notifications from RTD',next='삭제 전 마지막 게시의 run·artifact와 삭제시각의 보관 응답.'),
('readthedocs/readthedocs.org',11042): dict(relevant=False,kind='dashboard_design',finding='Crispy layout API와 Django 템플릿의 배치 논의.',reason='독자 URL·판·게시 사건이 없는 검색 오탐.',quote='Forms: avoid Crispy layout API?',next='없음: 관련성 탈락.'),
('jimporter/mike',199): dict(relevant=True,kind='generation_failure_control',finding='!relative YAML 파싱 때문에 deploy 전 생성 실패. 유지관리자 패치 뒤 제보자의 작동 확인이 있다.',reason='실제 생성 실패 대조. 생성 성공을 만족하지 않아 강한 route-only 반례가 아님.',quote="could not determine a constructor for the tag '!relative'",next='회복 뒤 실제 build run은 없으므로 재현 지문 필요.'),
('jimporter/mike',202): dict(relevant=False,kind='forge_feature_request',finding='다른 forge 지원 요청과 GitLab public 디렉터리 배치 경험. 특정 독자 경로 실패가 고정되지 않았다.',reason='일반 설정·기능 논의이며 고정 사건 아님.',quote='Improve usability on non-Github forges',next='고정 repository/ref/URL을 가진 별도 배포 사건 필요.'),
('mkdocs/mkdocs',3579): dict(relevant=False,kind='theme_policy_discussion',finding='RTD와 MkDocs 테마 지원 설명의 부정확성과 수정 PR 논의.',reason='독자 판·URL의 배포 실패가 아니라 안내문 범위 논쟁.',quote='Documentation: indicate that the Read the Docs platform accepts other themes',next='없음: 관련성 탈락.'),
('mkdocs/mkdocs',3583): dict(relevant=True,kind='green_build_404',finding='gessha.dev 소유자가 build 성공 후 GitHub 404를 보고. 댓글은 Q/A로 이동했다는 안내만 있다.',reason='생성 성공은 제보이고 게시 성공·ref·회복 응답은 없다.',quote='the build succeeded but the page shows the GitHub 404',next='2024-02-27 소스SHA·Pages 상태·후속 Q/A 원문.'),
('mkdocs/mkdocs',3593): dict(relevant=True,kind='absolute_asset_path',finding='404.html의 절대 CSS 경로를 오류로 제보했으나 유지관리자는 중첩 URL에서 필요한 동작과 site_url 확인을 설명했다.',reason='초기 진단 반대 근거. 두 단계 success의 사건도 원 버전 오제공도 아님.',quote='404 page has wrongly linked css',next='같은 site_url의 생성 HTML과 중첩 요청 두 개의 HTTP 지문.'),
('jimporter/mike',223): dict(relevant=True,kind='old_deeplink_lost',finding='FireFly의 버전 없는 namespaces 딥링크는404, 최신판 경로는 존재한다고 소유자가 보고. mike 유지관리자는 자동 구주소 이동을 지원하지 않는다고 설명했다.',reason='원래 주소 손실과 내용 존속의 역사 보고. 동일 ref 빌드/게시 success·복구 지문 없음.',quote="a `404` page is rendered",next='2024-07-22 FireFly build/publish run와 구·신 URL capture.'),
('actions/deploy-pages',365): dict(relevant=True,kind='artifact_missing_control',finding='성공한 Vite React 빌드 뒤 assets가 복사되지 않았다는 제보와 run 링크.',reason='산출물 누락 대조. 원 run은 현재404이며 게시 성공이 없다.',quote='No assets artifact found after successful build',next='run10222259682의 보존 로그와 업로드 artifact manifest.'),
('actions/deploy-pages',373): dict(relevant=True,kind='publish_success_404',finding='artifact1952676306, source843e4097e3d59d74c555e6a753713046e11743b7에 대한 publish success 로그를 제보자가 보존했고 독자404를 보고했다.',reason='공개 생성과 회복 원문이 부족하다. 대상 private repo의 원 run은 현재404.',quote='Reported success!',next='run10939969440 생성 산출물·전체 요청 URL·복구 응답의 공개 최소 재현.'),
('actions/deploy-pages',377): dict(relevant=True,kind='failed_publish_control',finding='deploy-pages v2의 Invalid artifact url 실패와 옛 사이트까지404라는 보고. v4로 바꾼 뒤에도 Validation 오류라고 답했다.',reason='게시 실패 대조이며 성공 후 route-only 반례가 아니다.',quote='while a new deployment fails, my site shows a 404',next='실패 전/후 deployment statuses와 이전 artifact 보관.'),
('readthedocs/readthedocs.org',11531): dict(relevant=True,kind='same_revision_different_label',finding='mesa release-r24.03.1과 stable의 하단 git hash가 같지만 old-version 경고만 달랐다고 발행자가 보고. RTD 담당자는 수동 stable은 실제 alias가 아니라고 답했다.',reason='다른 이름/경고가 다른 소스판이라는 추론에 대한 반대 보고. 전체 파일 바이트 동일성은 없다.',quote='the git hash at the bottom of the page remains identical',next='2024-08-08 두 URL의 HTML/본문 지문과 version metadata.'),
('jimporter/mike',229): dict(relevant=True,kind='alias_label_nochange',finding='1.0.0에1.0·stable을 붙였을 때 표시 alias가 바뀐다는 재현. maintainer는 같은 real version을 가리키는 동등 포인터라고 설명했다.',reason='표시 문자열의 변경이 내용판 변경을 의미하지 않는 역대조. 웹 publish/run 검증 없음.',quote='only one of the aliases is shown in the version selector',next='그 deploy의 versions.json과 두 alias를 해석한 실제 HTML 지문.'),
('actions/deploy-pages',383): dict(relevant=True,kind='success_stale_artifact',finding='같은 source SHA에서 다른 artifact로 success를 받아도 release 경로는 옛 catalog를 제공한 typst 발행자 원기록을 추적했다. dispatch 회복은 발행자 보고까지다.',reason='생성물·publish success·잘못된 공개 JSON 연결은 강함. 회복 뒤 실제 catalog 지문과 원 run은 현재 확보 못해 완결 강한 반례는 미확인.',quote='The previous deployed artifacts is served instead.',next='typst runs#9/#10/#11의 보관 artifact와 dispatch 직후 catalog.json 출력.'),
('jimporter/mike',248): dict(relevant=True,kind='trailing_slash_redirect_loop',finding='docs.eda.dev/blog/가25.4를 반복 붙이는 루프. 소유자는 루트404.html 부재로 SPA 처리됨을 확인하고 versioned404를 루트에 복사해 회복을 보고.',reason='route 설정 오류/회복의 발행자 원문. 두 단계 success·고정 artifact 지문 없음.',quote='leads to an endless redirect.',next='2025-07-24의 publish run와 루트404·/blog/ 전후 응답.'),
}
FIRST={('readthedocs/readthedocs.org',10990),('readthedocs/readthedocs.org',11001),('readthedocs/readthedocs.org',11042),('jimporter/mike',199),('jimporter/mike',202),('mkdocs/mkdocs',3579),('mkdocs/mkdocs',3583),('mkdocs/mkdocs',3593),('jimporter/mike',223),('actions/deploy-pages',365),('actions/deploy-pages',373),('actions/deploy-pages',377)}
rows=[];sources=[];attempts=[];extracts=[]
def body_data(path):
 raw=path.read_bytes();j=json.loads(raw);return j,hashlib.sha256(raw).hexdigest(),len(raw)
def sid(repo,n):return 'I-'+repo.split('/')[0].upper()+'-'+str(n)
for (repo,n),d in D.items():
 base=repo.replace('/','--')+'-'+str(n)
 p=E/('issue-'+base+'.json');j,h,size=body_data(p);a=j['data'];source=sid(repo,n);lineage='incident:'+repo+'#'+str(n)
 group='first12' if (repo,n) in FIRST else 'supplement4'
 row=dict(incident_id=source,lineage_id=lineage,sampling_group=group,created_utc=a['created_at'],issue_number=n,repository=repo,url=a['html_url'],title=a['title'],kind=d['kind'],relevant_for_minimum=d['relevant'],finding=d['finding'],strong_complete_counterexample=False,admission_or_rejection=d['reason'],next_minimum=d['next'],source_ids=source+'-BODY;'+source+'-COMMENTS')
 rows.append(row)
 for suffix,fn in [('BODY','issue-'),('COMMENTS','comments-')]:
  fp=E/(fn+base+'.json');jj,hh,sz=body_data(fp);dd=jj['data']
  count=d['relevant'] and suffix=='BODY'
  observed=d['finding'] if suffix=='BODY' else '해당 사건 댓글의 설명·반박·회복 보고를 함께 읽었다. 사건 계보는 본문과 동일하며2026 댓글은 역사 판단에서 제외한다.'
  sources.append(dict(source_id=source+'-'+suffix,id=source+'-'+suffix,lineage_id=lineage,kind='public_issue_body' if suffix=='BODY' else 'public_issue_comments',url=jj['url'],version=a['created_at']+' (currently retrieved mutable record)',section='body' if suffix=='BODY' else 'comments; dated2024–2025 only for claims',read_utc=jj['observed_utc'],questions=['Q6','Q7'],cases=['incident_sample'],claim_ids=['Q6-'+d['kind']],observed=observed,observer='publisher/reporters; researcher reads public record',support_refute=d['reason'],limitations='Mutable issue fetched now; timestamps identify reports, not independent HTTP capture. '+('Directly read but excluded from minimum as irrelevant.' if not d['relevant'] else 'No general occurrence rate inferred.'),receipt_path='streams/incidents/evidence/'+fp.name,countable_original=count,independent_lineage_countable=d['relevant'],transport='github_connector',snapshot_bytes=sz,snapshot_sha256=hh))
  attempts.append(dict(id=source+'-'+suffix,url=jj['url'],requested_utc=jj['observed_utc'],transport='github_connector',connector_calls=1,http_status=None,body_read=True,download_wire_bytes=None,snapshot_bytes=sz,snapshot_sha256=hh,effect='issue/report evidence only',reused_request=False))
 extracts.append(dict(source_id=source+'-BODY',lineage_id=lineage,url=a['html_url'],created_utc=a['created_at'],updated_utc=a['updated_at'],short_quote=d['quote'],finding=d['finding'],limitation=d['reason']))
rows.sort(key=lambda x:(x['created_utc'],x['issue_number'],x['repository']))
for i,r in enumerate([x for x in rows if x['sampling_group']=='first12'],1):r['chronological_rank_first12']=i
for r in rows:r.setdefault('chronological_rank_first12','')
fields=['incident_id','lineage_id','sampling_group','chronological_rank_first12','created_utc','issue_number','repository','url','title','kind','relevant_for_minimum','finding','strong_complete_counterexample','admission_or_rejection','next_minimum','source_ids']
with (P/'incidents.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
# Follow the 2024–2025 #383 event into the publisher's own retained record; same lineage.
for name,count,kind,obs,lim in [
 ('supplement-0.json',True,'publisher_incident_with_retained_log','Typst issue1 preserves artifact4575825543 at2025-11-15T06:00:13Z, publisher digestd53e4f18…, source7d14b2f…, publish success, and catalog old/new name mismatch.','Recovery same-SHA dispatch reported, but exact recovered catalog bytes/run unavailable.'),
 ('chain-2.json',True,'git_commit_metadata','Fixed source7d14b2f45ed78db82f976e5cd2dec5c7ffac2f9f has commit time2025-10-28T02:45:41Z.','Commit time is not generation/publication time.'),
 ('chain-3.json',True,'fixed_workflow_source','gh-pages.yaml at7d14b2f… defines build_catalog with RELEASE_EVENT and deploy needs build, upload-pages-artifact v3 and deploy-pages v4.','Config explains dynamic inputs but is not an execution success record.'),
 ('chain-4.json',True,'release_record_manifest','Release262635061 published2025-11-15T06:00:00Z; two uploaded assets with size/digest, including tagtypst-main.2025-11-14.0da0165.','Release asset manifest is not Pages catalog artifact or received site content.'),
]:
 fp=E/name;j,h,size=body_data(fp);source='I-TYPST-'+name[:-5].upper()
 sources.append(dict(source_id=source,id=source,lineage_id='incident:actions/deploy-pages#383',kind=kind,url=j['url'],version='2025-11-15 report; source7d14b2f45ed78db82f976e5cd2dec5c7ffac2f9f',section='body/log/config/manifest',read_utc=j['observed_utc'],questions=['Q6','Q7'],cases=['incident_sample'],claim_ids=['Q6-success_stale_artifact'],observed=obs,observer='publisher; researcher retrieval',support_refute='Supports a stale-reader-content counterexample short of a complete recovery fingerprint.',limitations=lim,receipt_path='streams/incidents/evidence/'+name,countable_original=count,independent_lineage_countable=True,transport='github_connector',snapshot_bytes=size,snapshot_sha256=h))
# Every supplementary request is counted, including404 and empty lists.
for glob in ['supplement-*.json','chain-*.json']:
 for fp in sorted(E.glob(glob)):
  j,h,size=body_data(fp);d=j['data'];error= isinstance(d,dict) and d.get('isError',False)
  empty=(d==[]) or (isinstance(d,dict) and d.get('total_count')==0)
  attempts.append(dict(id='I-'+fp.stem,url=j['url'],requested_utc=j['observed_utc'],transport='github_connector',connector_calls=1,http_status=404 if error and '404' in json.dumps(d) else None,body_read=not error,empty_response=empty,download_wire_bytes=None,snapshot_bytes=size,snapshot_sha256=h,effect='Run missing/empty lists cannot establish non-deployment.' if error or empty else 'Supplementary publisher/source evidence',reused_request=False))
for fp in sorted(E.glob('search-*.json')):
 j,h,size=body_data(fp)
 attempts.append(dict(id='I-'+fp.stem,url='https://github.com/search',query=j['query'],requested_utc=j['observed_utc'],transport='github_connector_search',connector_calls=1,http_status=None,body_read=False,download_wire_bytes=None,snapshot_bytes=size,snapshot_sha256=h,effect='Discovery metadata; excluded from original count.',reused_request=False))
for fp in sorted(E.glob('*.receipt.json')):
 j=json.loads(fp.read_text());j.update(transport='direct_public_http',connector_calls=0,body_read=True,download_wire_bytes=j.get('bytes_downloaded'),effect='Current observation only; cannot date historical recovery.',reused_request=False);attempts.append(j)
 source='I-HTTP-'+j['id'].upper()
 sources.append(dict(source_id=source,id=source,lineage_id={'typst':'incident:actions/deploy-pages#383','firefly':'incident:jimporter/mike#223','eda':'incident:jimporter/mike#248','mesa':'incident:readthedocs/readthedocs.org#11531'}[j['id'].split('-')[0]],kind='current_http_response',url=j['url'],version='current request2026-11-23 only',section='response title/metadata/catalog names',read_utc=j['completed_utc'],questions=['Q6','Q7'],cases=['incident_sample'],claim_ids=['Q6-current_not_historical'],observed=f"HTTP{j.get('status')}; final={j.get('final_url')}; bytes={j.get('bytes_downloaded')}; sha256={j.get('sha256')}",observer='researcher',support_refute='Neither confirms nor refutes2024–2025 response interval.',limitations='Current observation; failed endpoints do not count as originals. Anonymous response headers limited to documentary fields.',receipt_path='streams/incidents/evidence/'+fp.name,countable_original=j.get('status')==200,independent_lineage_countable=True,transport='direct_public_http',snapshot_bytes=j.get('bytes_downloaded'),snapshot_sha256=j.get('sha256')))
web=json.loads((E/'web-discovery-receipt.json').read_text())
attempts.append({**web,'url':'https://github.com/search','body_read':False,'connector_calls':0,'download_wire_bytes':None,'effect':'Discovery only; excluded from originals.'})
for fn,obj in [('sources.jsonl',sources),('attempts.jsonl',attempts),('extracts.jsonl',extracts)]:
 (P/fn).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in obj))
metrics={'first12_read':12,'first12_relevant':sum(r['relevant_for_minimum'] for r in rows if r['sampling_group']=='first12'),'supplement_events':4,'supplement_relevant':4,'unique_issues_read':16,'relevant_independent_lineages':12,'source_rows':len(sources),'countable_original_rows':sum(s['countable_original'] for s in sources),'first12_strong_complete':0,'supplement4_strong_complete':0,'publisher_chain_stale_content':1,'recovery_output_fingerprint_missing':1,'direct_http_logical_get_calls':6,'direct_http_exchange_count':None,'redirecting_logical_calls':1,'direct_http_responses_status200':3,'direct_http_responses_status404':3,'direct_http_body_bytes':sum(a.get('bytes_downloaded',0) or 0 for a in attempts if a.get('transport')=='direct_public_http'),'github_connector_calls':sum(a.get('connector_calls',0) for a in attempts),'github_http_requests_and_wire_bytes':None,'wire_byte_boundary':'Public HTTP body bytes only; headers/TLS/redirect exchanges and connector wire bytes unknown.','search_web_queries':2,'search_web_tool_calls':1,'actual_walltime_or_money':None,'original_minimum_rule':'Only relevant body records and actual source/manifest/200-response records counted. Comments, discovery, failures and irrelevant issue bodies excluded. Same event never adds lineage.'}
(P/'COSTS.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n')
assert len(rows)==16 and len([r for r in rows if r['sampling_group']=='first12'])==12
assert len({s['source_id'] for s in sources})==len(sources)
assert len({s['lineage_id'] for s in sources if s['countable_original']})==12
print(json.dumps(metrics,ensure_ascii=False,indent=2))
