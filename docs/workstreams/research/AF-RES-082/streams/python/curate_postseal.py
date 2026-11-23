"""Curate already-opened public evidence; performs no network or deployment."""
import json, pathlib, re
D = pathlib.Path(__file__).resolve().parent
receipts = {r['key']: r for r in map(json.loads, (D/'http-receipts.jsonl').read_text().splitlines())}
sources = [r for r in map(json.loads, (D/'sources.jsonl').read_text().splitlines()) if r.get('phase') != 'postseal_verification']
cases = {
 'P1': ('bandersnatch', '7.0.1', '7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74'),
 'P2': ('build', '1.3.0', '60e8752f69178d2b2c3563e9c8fa17aa6e11b12c'),
 'P3': ('cibuildwheel', 'v3.3.0', '63fd63b352a9a8bdcc24791c9dbee952ee9a8abc'),
}
def lineage(c):
 r,t,_ = cases[c]
 return f'consumer-{r}-{t}'
def add(sid, key, c, kind, section, observed, limits, claim, qs=('Q2','Q4'), lin=None, version=None, count=False):
 r = receipts[key]
 sources.append(dict(source_id=sid,lineage_id=lin or lineage(c),kind=kind,url=r['url'],version=version or cases[c][2],section=section,opened_at_utc=r['opened_at_utc'],case_ids=[c],questions=list(qs),observed=observed,limitations=limits,claim_support=claim,sha256=r['sha256'],phase='postseal_verification',count_toward_minimum=count,receipt_key=key))
config_rows = [
 ('P1','RTD','.readthedocs.yml','L4–27','Ubuntu 24.04/Python 3.12; Sphinx html with docs/conf.py; fail_on_warning; pdf/htmlzip/epub; pip project plus requirements_docs.txt.','설정은 의도다. 대시보드 권한·공개판 활성화는 이 파일만으로 알 수 없다.'),
 ('P1','CONF','docs/conf.py','extensions, source_suffix, version/release, html_theme','Sphinx uses autodoc and CLI generation, RST+MyST Markdown, Furo, and installed bandersnatch version.','패키지를 설치하고 확장·테마를 같이 제공해야 한다. HTML 파일만으로 원본 생성 환경을 복원할 수 없다.'),
 ('P1','DEPS','requirements_docs.txt','pinned dependency list','Sphinx 8.2.3, Furo 2025.9.25, MyST 4.0.1 and CLI extension 1.20.1 are pinned.','태그 pin 자체는 설치 실행 증거가 아니다. 실제 로그에서 Sphinx 8.2.3 확인을 별도 기록했다.'),
 ('P1','TOX','tox.ini','doc_build environment','Local/CI doc_build emits html and linkcheck to docs/html.','이 로컬 산출물 경로를 RTD _readthedocs/html 게시 경로와 합치지 않는다.'),
 ('P1','GHA','.github/workflows/doc_build.yml','triggers and tox invocation','Push main/PR GitHub Actions invokes tox documentation build/link check. No publishing step in this workflow.','GitHub 검사 성공만으로 RTD 배포 성공을 주장하지 않는다.'),
 ('P2','RTD','.readthedocs.yml','L1–11','Ubuntu 22.04/Python 3.12; custom commands install uv latest then invoke Sphinx with docs input and $READTHEDOCS_OUTPUT/html output.','한 서비스가 있어도 사용자 명령과 산출물 계약이 필요하다. uv latest는 고정판이 아니다.'),
 ('P2','CONF','docs/conf.py','extensions, version, theme','Sphinx imports build version; uses autodoc, intersphinx, type hints, argparse CLI and issues extensions with Furo.','Sphinx 일반 시작 링크만으로 프로젝트 확장 의존 설치를 확인할 수 없다.'),
 ('P2','TOX','tox.ini','docs environment','tox docs invokes sphinx-build -n into its temporary output directory.','검사용 임시 출력은 RTD가 수집할 게시 디렉터리가 아니다.'),
 ('P2','GHA','.github/workflows/reusable-docs.yml','docs job','Reusable documentation workflow runs tox docs checks; no publication step is observed.','별도 GitHub Actions 실행은 오래된 run API에서 남지 않을 수 있다.'),
 ('P3','RTD','.readthedocs.yml','L3–11','Ubuntu 24.04; uv-managed Python 3.14; MkDocs strict build writes $READTHEDOCS_OUTPUT/html.','사용자 build.commands가 generator 실행을 책임진다. RTD 한 링크는 설정 0개를 뜻하지 않는다.'),
 ('P3','MKDOCS','mkdocs.yml','L1–59','docs source directory, relative navigation, custom theme overrides, CSS/JS, Markdown extensions, include-markdown/search/macros with docs/main and custom delimiters.','Markdown 자체로 Sphinx를 기각하지 않는다. 실제 MkDocs 설정·매크로·라우트의 동등 변환은 사전 B에 제공되지 않았다.'),
 ('P3','NOX','noxfile.py','docs session','nox docs installs the documentation group and invokes MkDocs build or serve.','로컬 생성·미리보기는 공개 게시가 아니다.'),
]
for c,suffix,path,section,obs,lim in config_rows:
 add(f'PY-{c}-{suffix}',f'{cases[c][0]}-post-{path}',c,'tag_build_configuration',section,obs,lim,'Supports actual responsibility boundary; does not establish the researcher alternative was adopted.')
for c in ['P2','P3']:
 n=cases[c][0]; dep=json.loads((D/(n+'-doc-dependencies.json')).read_text())
 add(f'PY-{c}-DEPS',f'{n}-post-pyproject.toml',c,'tag_dependency_contract','dependency-groups.docs','Documentation dependencies: '+', '.join(dep['docs_dependency_group']), 'No uv.lock was present in the inspected tag tree; unspecified ranges remain floating. P2 runtime Sphinx is separately observed in build log.', 'Supports version-specific generation contract; does not prove all current dependencies reproduce historical HTML.')

api_rows = [
 ('P1','VERSION','bandersnatch-rtd-version-7.0.1','named version 7.0.1','identifier equals tag SHA; active=false, built=false.'),
 ('P1','TAGBUILDS','bandersnatch-rtd-version-7.0.1-builds','all returned builds; count=0,next=null','No builds under named version 7.0.1. This is not absence of builds of its source SHA.'),
 ('P1','SHABUILDS','P1-commit-builds-retry1','commit filter, count=1,next=null','Build 30720077 under latest matches selected SHA and reports success; created 2025-12-16T17:50:37.578405Z.'),
 ('P2','VERSION','pypa-build-rtd-version-1.3.0','named version 1.3.0','identifier equals tag SHA; active=false, built=false.'),
 ('P2','TAGBUILDS','pypa-build-rtd-version-1.3.0-builds','all returned builds; count=0,next=null','No builds under named version 1.3.0, but selected SHA has latest/stable runs.'),
 ('P2','SHABUILDS','P2-commit-builds-retry1','commit filter, count=2,next=null','Builds 29061794 stable and 29061621 latest match selected SHA and report success on 2025-08-01.'),
 ('P3','VERSION','cibuildwheel-rtd-version-v3.3.0','named version v3.3.0','identifier equals selected SHA; active=true,built=true.'),
 ('P3','TAGBUILDS','cibuildwheel-rtd-version-v3.3.0-builds','all returned builds; count=2,next=null','Two successful runs 30298916 and 30298914 match selected SHA. API timestamps and raw command timestamps are not treated as the same publication time.'),
 ('P3','LEGACYVERSION','cibuildwheel-rtd-version-1.x','branch version 1.x','1.x is an active, built branch version. It is not an immutable patch version.'),
 ('P3','LEGACYBUILDS','cibuildwheel-rtd-version-1.x-builds','first 10 of 14 builds','Latest listed run 14073318 succeeded on 2021-06-22 at commit da84127892e79fab70b0ca4a4d22a23c1db53116.'),
 ('P3','LEGACYBUILDS2','P3-legacy-builds-page2','final 4 of 14 builds; next=null','Remaining four 1.x builds were in May 2021. Pagination has been read to the end.'),
 ('P3','LEGACYRUN','P3-legacybuild14073318','build 14073318','The 1.x run succeeded at da84127892e79fab70b0ca4a4d22a23c1db53116; created 2021-06-22T22:15:30.353364Z.'),
]
for c,suffix,key,sec,obs in api_rows:
 add(f'PY-{c}-{suffix}',key,c,'public_build_metadata',sec,obs,'API state is current public history, not an archived deployment manifest or continuous uptime record. No private publish transaction was observed.','Rejects inferring failure from inactive named tag alone; supports source-to-build linkage.',lin='incident-cibuildwheel-legacy-2021' if 'LEGACY' in suffix else None)

log_findings=[]
log_settings={
 'P1':(30720077,'8.2.3',646,647,720,645,'../_readthedocs/html'),
 'P2':(29061794,'7.4.7',77,94,133,76,'_readthedocs/html'),
 'P3':(30298916,'1.6.1 pinned; runtime banner not present',77,None,169,76,'_readthedocs/html'),
}
for c,(run,ver,cmdline,versionline,successline,exitline,out) in log_settings.items():
 lines=(D/(c+'-build-rawlog-analysis.txt')).read_text().splitlines()
 command=lines[cmdline-1]
 info=lines[exitline-1]
 findings=dict(case_id=c,run_id=run,source_sha=cases[c][2],generator='MkDocs' if c=='P3' else 'Sphinx',generator_version=ver,command=command,command_line=cmdline,command_exit_metadata=info,exit_metadata_line=exitline,success_line=successline,output_directory=out,metadata=dict(x.split(': ',1) for x in lines[1:8]),raw_log_receipt=receipts[c+'-build-rawlog'])
 log_findings.append(findings)
 obs=f'Exact selected SHA; {findings["generator"]} {ver}; generator command exit 0 and successful HTML generation into {out}.'
 lim='No retained artifact checksum links generated bytes to a historical served response. Build success is not a separate observed publication transaction.'
 if c=='P3':lim+=' API created/finished 19:28:06/19:28:22 differs from raw commands 19:33:07–19:33:20; do not collapse these clocks into one publish time.'
 add(f'PY-{c}-RAWLOG',c+'-build-rawlog',c,'historical_public_build_log',f'header L1–8; command L{cmdline}; exit L{exitline}; success L{successline}',obs,lim,'Supports actual historical generation, not merely YAML intent.')
 pagekey=f'{c}-build{run}-page'
 add(f'PY-{c}-BUILDPAGE',pagekey,c,'public_build_ui','source SHA/version and Raw text link','Build page links the source SHA and version to its raw text log.','Server HTML includes a hidden generic error/loading placeholder; without client evaluation it is not a failure observation. Use raw log/API status.','Supports raw-log discovery; rejects treating UI placeholder as failure.')
(D/'build-log-findings.json').write_text(json.dumps(log_findings,ensure_ascii=False,indent=2)+'\n')

html_obs={
 'P1-latest':('P1','title; current root','Current public latest is bandersnatch 8.2.0, not selected 7.0.1.'),
 'P2-root':('P2','redirect and title','Root resolves to en/stable and title identifies build 1.6.1, not selected 1.3.0.'),
 'P3-stable':('P3','HTTP response and relative navigation','Current stable public entry returns HTML. This moving alias alone does not identify the selected 2025 release.'),
 'P3-tag':('P3','version route and relative paths','Named v3.3.0 route returns HTML with relative options and changelog links.'),
 'P3-tag-options':('P3','options/#enable','Named v3.3.0 options page contains id=enable and corresponding relative navigation.'),
 'P3-tag-changelog':('P3','first release heading id=v330','Named v3.3.0 changelog begins with v3.3.0 and retains earlier release headings.'),
 'P3-legacy':('P3','en/1.x and readthedocs-data.js link','Legacy public entry returns HTML; Last-Modified is 2021-06-22.'),
 'P3-legacy-changelog':('P3','first release heading id=v1120','Legacy changelog begins with v1.12.0, distinct from the selected v3.3.0 site.'),
 'P2-old-domain':('P2','redirect to custom domain','Old RTD domain redirects to build.pypa.io/en/stable; final HTML SHA256 exactly equals independently fetched root redirect target.'),
}
for key,(c,sec,obs) in html_obs.items():
 f=D/(key+'-html-summary.json');d=json.loads(f.read_text());d['title']=d['title'].split('ContentsMenu')[0];f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 lin='incident-build-custom-domain-715' if key=='P2-old-domain' else 'incident-cibuildwheel-legacy-2021' if 'legacy' in key else None
 add('PY-'+key.upper(),key+'-html',c,'current_public_html',sec,obs,'Current response and Last-Modified header are not an independent historical archive. Hashes are current response fingerprints; no claim of byte immutability or uninterrupted availability.','Supports current reader access or version distinction, not past continuous availability.',qs=('Q4','Q5'),lin=lin)
add('PY-P3-LEGACYDATA','P3-legacy-rtddata','P3','served_build_identity','READTHEDOCS_DATA project/version/builder/commit','Served JavaScript identifies version 1.x, MkDocs, and commit da84127892e79fab70b0ca4a4d22a23c1db53116, equal to successful build14073318.','Build metadata can connect current legacy content to a source commit, but not prove it was available without interruption in 2025.','Strengthens current legacy artifact-to-source linkage.',qs=('Q4','Q5'),lin='incident-cibuildwheel-legacy-2021')

for c,ver,key in [('P1','8.2.3','sphinx823-build-manual'),('P2','7.4.7','sphinx747-build-manual')]:
 add('PY-SPHINX-'+ver.replace('.',''),key,c,'official_versioned_generator_contract','Synopsis/Description; -b; -M output semantics','Sphinx takes source and output directories, reads conf.py, and builds HTML. -M introduces builder subdirectories while -b writes the specified output.','Generator contract does not grant hosting rights or preserve version routes. Current RTD documentation is not retroactively treated as a 2025 platform contract.','Supports explicit generated-file handoff for B.',qs=('Q2','Q3'),lin='provider-sphinx',version=ver,count=c=='P1')
add('PY-MKDOCS-161','mkdocs161-deploy','P3','official_versioned_generator_contract','Project Pages; Custom Domains; Read the Docs; Other Providers','MkDocs 1.6.1 gh-deploy builds and pushes gh-pages; custom-domain CNAME must survive future builds. Other providers receive contents of site_dir; RTD can build hosted Git source.','This is an available alternative after freeze, not evidence cibuildwheel adopted Pages or proof that one gh-deploy retains 1.x alongside current docs.','Refutes equating two internal operations with two user-facing links; explains generator with deploy command.',qs=('Q2','Q5'),lin='provider-mkdocs',version='1.6.1',count=True)

incident_specs=[
 ('build-1031','PY-INC-STUCK','incident-build-stable-stuck-1031','P2','Issue body','Maintainer reports stable docs remained at 1.4.0 and identifies failed build32209794.','2026 incident is outside 2024–2025 selection window; do not retroactively score selected 1.3.0.','A managed-service entry point does not guarantee that the published moving alias advances.'),
 ('build-715','PY-INC-DOMAIN','incident-build-custom-domain-715','P2','Issue body plus linked comments','Maintainers proposed a custom build.pypa.io documentation domain.','Decision body alone does not prove DNS or RTD settings completed.','Actual consumer route migration must join DNS, service permissions and reader entry links.'),
 ('build-717','PY-INC-DOMAIN-PR','incident-build-custom-domain-715','P2','merged_at; linked file diff','PR717 merged 2024-01-17 and updated README/package links to build.pypa.io.','Merge is source adoption evidence; current redirect is separate reader-access evidence.','Supports owner adoption of custom-domain route.'),
 ('cibuildwheel-657','PY-INC-LEGACY','incident-cibuildwheel-legacy-2021','P3','1.x and 2.0 release checklists','Maintainer checklist creates 1.x branch/docs and links old docs for Python2 after dropping that support from new releases.','Checklist and later surviving site are not a complete availability history; 1.x is mutable series.','Independent legacy-preservation decision explains the later two reader conditions.'),
 ('bandersnatch-2090','PY-INC-THEME','incident-bandersnatch-theme-2090','P1','issue body with en/7.0.0 URL','Maintainer reported misformatted documentation at the named 7.0.0 route in November 2025.','Reported visual failure; original page was not archived here and issue is not a reproduction by this researcher.','Successful hosting and a reachable URL do not alone establish readable documentation.'),
 ('bandersnatch-2092','PY-INC-THEME-PR','incident-bandersnatch-theme-2090','P1','proposal and merged_at','PR2092 replaced an archived theme with Furo and merged 2025-11-28.','PR fix and confirmations refer to latest; old 7.0.0 page correction was not established.','A fix to latest must not be substituted for restoration of the original old-version URL.'),
]
ir={x['key']:x for x in json.loads((D/'incident-receipts.json').read_text())}
incidents=[]
for key,sid,lin,c,sec,obs,lim,claim in incident_specs:
 r=ir[key]
 sources.append(dict(source_id=sid,lineage_id=lin,kind='independent_consumer_incident',url=r['html_url'],version=r['metadata']['created_at'],section=sec,opened_at_utc=r['opened_at_utc'],case_ids=[c],questions=['Q5','Q6'],observed=obs,limitations=lim,claim_support=claim,phase='postseal_verification',count_toward_minimum='-PR' not in sid,repeated_external_request=True,first_request_timestamp='not captured; timed direct reread used'))
 incidents.append(dict(source_id=sid,lineage_id=lin,case_id=c,metadata=r['metadata'],url=r['html_url'],observed=obs,limitations=lim))
for key,sid,lin,c,obs,lim in [
 ('build715-comments','PY-INC-DOMAIN-COMMENTS','incident-build-custom-domain-715','P2','Comments1868266834/1868305900/1868324447/1868464918/1868465890 record maintainer agreement, DNS change, sole RTD owner obstacle, Henry added to RTD, and remaining domain-setting/link edits.','These are public reports of actions/permissions, not present-day access granted to this researcher.'),
 ('bandersnatch2092-comments','PY-INC-THEME-COMMENTS','incident-bandersnatch-theme-2090','P1','Comment3587230341 offers an HTML ZIP; 3589367702 and3589758959 report latest docs now readable.','ZIP was not downloaded. latest repair does not verify old7.0.0 route repair.'),
 ('build717-files','PY-INC-DOMAIN-DIFF','incident-build-custom-domain-715','P2','README and pyproject metadata replace old RTD URLs with build.pypa.io.','Source diff records adopted links, not DNS propagation history.'),
]:
 r=next(x for x in json.loads((D/'incident-subresource-receipts.json').read_text()) if x['key']==key)
 sources.append(dict(source_id=sid,lineage_id=lin,kind='incident_subresource',url=r['url'],version='public incident history',section='returned comments/files',opened_at_utc=r['opened_at_utc'],case_ids=[c],questions=['Q5','Q6'],observed=obs,limitations=lim,claim_support='Supports real manual work and route responsibility; same incident lineage as linked issue/PR.',phase='postseal_verification',count_toward_minimum=False))
add('PY-INC-STUCK-LOG','P2-stuck32209794-rawlog','P2','historical_failure_log','header; command L95 onward; docstrfmt failure','RTD32209794 stable at commit130b043d1a1c1a12a0558f2598430b769f074690 has Success=False. Installed build1.4.3; docstrfmt fails CHANGELOG.rst line49 for skipped title hierarchy and command exits1 before Sphinx publication.','Does not itself prove how long stable remained at1.4.0 or the later fix; issue supplies the user-visible lag report.','Direct failure contradicts assuming managed-service adoption is sufficient for release freshness.',qs=('Q5',),lin='incident-build-stable-stuck-1031',version='2026-04-10 build32209794')
(D/'incidents.json').write_text(json.dumps(incidents,ensure_ascii=False,indent=2)+'\n')

def data(name):
 d=json.loads((D/name).read_text());return d.get('data',d)
deployment=[]
for c in ['P1','P2','P3']:
 repo,tag,sha=cases[c]
 builds=data({'P1':'P1-commit-builds-retry1.json','P2':'P2-commit-builds-retry1.json','P3':'cibuildwheel-rtd-version-v3.3.0-builds.json'}[c])['results']
 htmlkeys={'P1':['P1-latest'],'P2':['P2-root','P2-old-domain'],'P3':['P3-stable','P3-tag','P3-tag-options','P3-tag-changelog','P3-legacy','P3-legacy-changelog']}[c]
 html=[]
 for k in htmlkeys:
  d=json.loads((D/(k+'-html-summary.json')).read_text());r=d['retrieval'];html.append(dict(key=k,url=r['url'],final_url=r['final_url'],opened_at_utc=r['opened_at_utc'],status=r['http_status'],sha256=r['sha256'],last_modified=r['headers'].get('last-modified'),title=d['title']))
 deployment.append(dict(deployment_id='PY-DEP-'+c,case_id=c,lineage_id=lineage(c),tag=tag,source_sha=sha,actual_path='RTD-managed build and hosting with '+('MkDocs' if c=='P3' else 'Sphinx'),builds=[{k:b.get(k) for k in ['id','version','commit','created','finished','duration','success']} for b in builds],log_source_id='PY-'+c+'-RAWLOG',observed_generation=True,observed_separate_publish_transaction=False,current_html=html,current_public_entry_open=True,current_selected_version_access='yes_version_identification_not_full_byte_provenance' if c=='P3' else 'no_at_inspected_named_or_promised_entry_urls',historical_both_conditions='unconfirmed' if c=='P3' else 'not_applicable_condition2_unconfirmed',evidence_level='historical source-to-successful-generation + current served HTML; no immutable served-artifact manifest',limitations=('Named tag inactive/404 does not refute historical publication under latest/stable. Current rolling entry identifies a newer version.' if c!='P3' else 'Selected source has successful tag builds and currently identifiable content. Legacy source identity survives, but contemporaneous2025 coavailability and full byte equality are unconfirmed. API and command clocks differ.'),researcher_AB_deployment_performed=False,archive_fingerprint=None,archive_status='Independent historical snapshot not obtained; current response fingerprints are not archives.'))
deployment.append(dict(deployment_id='PY-DEP-P3-LEGACY',case_id='P3',lineage_id='incident-cibuildwheel-legacy-2021',version='1.x',source_sha='da84127892e79fab70b0ca4a4d22a23c1db53116',run_id=14073318,success=True,run_created='2021-06-22T22:15:30.353364Z',current_served_js_same_commit=True,old_content_identification='Current legacy changelog begins v1.12.0',public_build_history_count=14,history_pagination_complete=True,historical_2025_coavailability='unconfirmed',series_not_immutable_patch=True,source_ids=['PY-INC-LEGACY','PY-P3-LEGACYRUN','PY-P3-LEGACYDATA','PY-P3-LEGACY-CHANGELOG']))
deployment.append(dict(deployment_id='PY-FAIL-STABLE',case_id='P2',lineage_id='incident-build-stable-stuck-1031',run_id=32209794,source_sha='130b043d1a1c1a12a0558f2598430b769f074690',run_date='2026-04-10T21:24:57.407834Z',success=False,failed_stage='pre-generation documentation formatting',last_observed_command_exit=1,published_prior_version='1.4.0 per maintainer issue; not independently replayed',scope='independent incident outside selected release period',source_ids=['PY-INC-STUCK','PY-INC-STUCK-LOG']))
(D/'deployments.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in deployment))
for r in json.loads((D/'connector-receipts.json').read_text()):
 if not r['key'].startswith(('P1','P2')):continue
 c=r['key'][:2]
 sources.append(dict(source_id='PY-'+r['key'].upper(),lineage_id=lineage(c),kind='historical_record_lookup',url=r['url'],version=cases[c][2],section='entire response',opened_at_utc=r['opened_at_utc'],case_ids=[c],questions=['Q4'],observed='No returned commit statuses' if 'status' in r['key'] else 'No returned GitHub Actions runs for selected head_sha',limitations='Empty current API results may reflect history retention. A default pending state with no statuses is not evidence of a pending or failed build. RTD direct sourceSHA-filtered runs provide the positive historical evidence.',claim_support='Does not support absence of historical execution; motivates direct RTD lookup.',phase='postseal_verification',count_toward_minimum=False))
(D/'sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in sources))
print(json.dumps({'sources':len(sources),'unique_lineages':len(set(x['lineage_id'] for x in sources if x.get('count_toward_minimum'))),'postseal_sources':sum(x.get('phase')=='postseal_verification' for x in sources),'deployments':len(deployment)},ensure_ascii=False))
