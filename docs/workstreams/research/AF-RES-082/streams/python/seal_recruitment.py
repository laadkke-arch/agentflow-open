import json,pathlib,datetime
D=pathlib.Path(__file__).resolve().parent
frame=json.load(open(D.parents[1]/'evidence/pypa-frame.json'))['repositories']
receipts=[json.loads(s) for s in (D/'http-receipts.jsonl').read_text().splitlines()]
bykey={x['key']:x for x in receipts}
selections=[('P1','bandersnatch','7.0.1','7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74',5,3,'https://bandersnatch.readthedocs.io/en/latest/'),('P2','build','1.3.0','60e8752f69178d2b2c3563e9c8fa17aa6e11b12c',9,4,'https://build.pypa.io'),('P3','cibuildwheel','v3.3.0','63fd63b352a9a8bdcc24791c9dbee952ee9a8abc',10,5,'https://cibuildwheel.pypa.io/en/stable/')]
selected=[];updates=[];sources=[];reqs=[]
def source(sid,lineage,key,kind,version,section,cases,observed,limitations,support,count=False,questions=['Q1']):
 r=bykey[key]
 sources.append(dict(source_id=sid,lineage_id=lineage,kind=kind,url=r['url'],version=version,section=section,opened_at_utc=r['opened_at_utc'],case_ids=cases,questions=questions,observed=observed,limitations=limitations,claim_support=support,sha256=r['sha256'],phase='recruitment_and_requirements_before_link_freeze',count_toward_minimum=count))
for i,row in enumerate(frame,1):
 n=row['name'];out={k:row[k] for k in ['org','original_rank','name','full_name','language']};out.update(case_id='',last_2024_2025_formal_tag='',formal_release_published_at='',eligible_candidate_rank='',status='',exclusion_reason='')
 if i>10:out.update(status='not_screened_after_third',exclusion_reason='First three eligible documentation projects were fixed at original rank 10; later rows retained without release/source inspection.')
 elif n in ['.github','advisory-database','bootstrap','bot-test','browntruck']:
  out.update(status='excluded_no_formal_release',exclusion_reason='Public releases endpoint returned zero releases and tags endpoint returned zero tags; no 2024–2025 formal tag identified. No inference about releases outside GitHub.')
  source('PY-FRAME-'+str(i).zfill(2),'recruitment-pypa-'+n,n+'-releases','release_inventory','retrieved 2026-11-23','JSON array',[],out['exclusion_reason'],'Current repository ownership and API visibility do not reconstruct historic organization membership.','Excluded from formal-release candidate count.')
 elif n in ['abi3audit','auditwheel']:
  release=json.load(open(D/f'{n}-releases-summary.json'))['eligible_releases'][0]; meta=json.load(open(D/f'{n}-tag-metadata.json'))
  out.update(last_2024_2025_formal_tag=release['tag_name'],formal_release_published_at=release['published_at'],eligible_candidate_rank=1 if n=='abi3audit' else 2,status='excluded_no_documentation_site_source_pair',exclusion_reason='Tag README and recursive tree provide no separate reader documentation source plus project documentation-site publication link. README-only usage, package links, third-party standards/blogs are not the required pair.')
  source('PY-FRAME-'+str(i).zfill(2),'recruitment-pypa-'+n,n+'-tag-tree','tag_tree',meta['commit_sha'],'recursive tree (truncated=false)',[],out['exclusion_reason'],'No claim that the project has no documentation anywhere; criterion is documentation-site pair at selected formal tag.','Excluded before deployment outcome inspection.')
 else:
  case,n,tag,sha,rank,crank,url=next(s for s in selections if s[1]==n)
  release=json.load(open(D/f'{n}-releases-summary.json'))['eligible_releases'][0];meta=json.load(open(D/f'{n}-tag-metadata.json'))
  out.update(case_id=case,last_2024_2025_formal_tag=tag,formal_release_published_at=release['published_at'],eligible_candidate_rank=crank,status='included',exclusion_reason='Included: docs source in selected tag and external reader documentation link in its README. No deployment evidence used for selection.')
  selected.append(dict(case_id=case,repository='pypa/'+n,original_rank=rank,eligible_candidate_rank=crank,language='Python',tag=tag,tag_sha=sha,release_published_at=release['published_at'],release_url=release['html_url'],reader_url=url,source_paths=[p for p in meta['paths'] if p.startswith('docs/')],requirements_count=2 if case=='P3' else 1,selection_basis='README site link + docs/ tree, before provider guides/deployment inspection',preexposure='README includes Read the Docs badge and docs links; tree exposes config filenames but config content not read.'))
 updates.append(out)
for case,n,tag,sha,rank,crank,url in selections:
 source('PY-'+case+'-REL','consumer-'+n+'-'+tag,n+'-releases','formal_release_record',tag,'latest non-draft, non-prerelease published_at within 2024–2025',[case],f'Last qualifying formal release: {tag}; exact date retained in selection.json.','Release publication is package-release evidence, not documentation deployment evidence.','Supports selected tag and temporal frame.',True)
 sections={'P1':'README.md L4,L18,L99; documentation links','P2':'README.md L7,L13,L30–31; documentation links','P3':'README.md L5,L12,L53; stable/legacy documentation links'}
 observed={'P1':'README sends readers to en/latest/ and also the documentation root. It does not promise immutable 7.0.1 URLs or version navigation.','P2':'README sends readers to build.pypa.io for full information; badge points to en/latest/. It does not promise an immutable 1.3.0 site.','P3':'README sends current readers to stable documentation, provides stable option deep links, and directs users of unsupported Python versions such as Python 2 to en/1.x/.'}
 source('PY-'+case+'-README','consumer-'+n+'-'+tag,n+'-readme','consumer_tag_readme',sha,sections[case],[case],observed[case],'A linked URL is an owner-published navigation promise, not proof that its target was deployed or remains reachable. Current organization list does not establish tag-time ownership.','Supports reader-facing condition(s); rejects inventing a second condition from one URL.',False)
 c1={'P1':'독자용 문서 진입점 https://bandersnatch.readthedocs.io/en/latest/ 제공','P2':'전체 사용설명 문서 진입점 https://build.pypa.io 제공','P3':'현재 독자에게 stable 문서와 옵션 심층링크 제공'}[case]
 reqs.append(dict(case_id=case,requirement_id=case+'-R1',status='observed_owner_statement',requirement=c1,role='maintainer to documentation reader',tag=tag,tag_sha=sha,url=f'https://github.com/pypa/{n}/blob/{sha}/README.md',section=sections[case],source_id='PY-'+case+'-README',short_quote='Documentation' if case!='P2' else 'for full information',limit='Moving latest/stable/root entry point is not a promise of immutable tag content.',reader_url=url))
 if case=='P3':
  reqs.append(dict(case_id=case,requirement_id=case+'-R2',status='observed_owner_statement',requirement='Python 2 등 지원종료 Python 대상 사용자가 cibuildwheel 1.x 문서로 이동할 수 있음',role='maintainer to legacy-version documentation reader',tag=tag,tag_sha=sha,url=f'https://github.com/pypa/{n}/blob/{sha}/README.md',section='README.md L53',source_id='PY-P3-README',short_quote='cibuildwheel 1 documentation',limit='1.x is a branch/series URL. The README does not assert immutable bytes or a specific 1.x point-release snapshot.',reader_url='https://cibuildwheel.pypa.io/en/1.x/'))
 else:
  reqs.append(dict(case_id=case,requirement_id=case+'-R2',status='unconfirmed',requirement='두 번째 독립 보존 요구 미확인',role='documentation reader',tag=tag,tag_sha=sha,url=f'https://github.com/pypa/{n}/blob/{sha}/README.md',section='README plus selected-tag documentation/release policy search',source_id='PY-'+case+'-README',short_quote='',limit='No additional condition created from the existence of a public URL; immutable versions, downloads and publication deadlines not asserted.',reader_url=''))
extra=[('P1','bandersnatch','docs/index.rst','PY-P1-INDEX','index content and toctree','문서원본은 설치·저장소·미러설정·필터·서빙·기여·모듈을 연결하고 CLI를 생성하는 지시문을 가진다. 구판 사이트 보존 약속은 없다.'),('P1','bandersnatch','docs/CONTRIBUTING.md','PY-P1-CONTRIB','Making a bandersnatch release to GitHub + PyPI','버전/변경기록 갱신 후 GitHub release를 만들면 PyPI 게시 workflow를 사용하라고 안내한다. 문서 사이트 게시·고정 URL 약속은 확인되지 않았다.'),('P1','bandersnatch','MAINTAINERS.md','PY-P1-MAINT','Releasing to PyPI','유지관리자 합의와 PyPI 패키지 배포 단계를 명시한다. 이것을 문서사이트 게시 승인으로 전용하지 않는다.'),('P2','build','docs/index.rst','PY-P2-INDEX','CLI directive and Usage/Contributing toctree','CLI·설치·변경기록·API·릴리스 페이지를 문서원본에서 연결한다. 구판 보존 약속은 없다.'),('P2','build','docs/release.rst','PY-P2-RELEASE-POLICY','Release Process','버전·changelog·signed tag·GitHub release 과정이다. 문서사이트 게시 여부는 언급하지 않는다.'),('P2','build','docs/mission.rst','PY-P2-MISSION','Mission Statement','사용자 자신의 패키지관리와 분리되는 빌드 도구 목적과 최소 의존을 설명한다. 문서 URL 보존 요구가 아니다.'),('P3','cibuildwheel','docs/contributing.md','PY-P3-CONTRIB','L102–111, L190–208','문서 build/serve용 nox 명령과 패키지 release 절차가 있다. 생성·개발 미리보기와 문서의 공개 게시를 동일시하지 않는다.')]
for case,n,p,sid,sec,obs in extra:
 tag=next(s[2] for s in selections if s[1]==n);sha=next(s[3] for s in selections if s[1]==n)
 source(sid,'consumer-'+n+'-'+tag,n+'-'+p,'consumer_tag_policy_or_source',sha,sec,[case],obs,'Only the named sections were used for requirements; CI configuration and deployment logs remain unread before link freeze.','Supports documentation source scope and the explicit absence of another promise in these inspected locations.')
(D/'frame_updates.json').write_text(json.dumps(updates,ensure_ascii=False,indent=2)+'\n')
(D/'selection.json').write_text(json.dumps({'fixed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'frame_total':58,'original_rows_inspected':10,'formal_release_candidates_inspected':5,'selected_count':3,'selected':selected,'stop_rule':'third included case at original rank 10; no replacement'},ensure_ascii=False,indent=2)+'\n')
for filename,rows in [('requirements.jsonl',reqs),('sources.jsonl',sources)]: (D/filename).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
# Keep metadata and hashes, not wholesale README/policy/changelog copies.
for p in D.glob('*-analysis.txt'):p.unlink()
for p in D.glob('*-releases-summary.json'):
 v=json.loads(p.read_text())
 for row in v['eligible_releases']:row.pop('body',None)
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print('sealed',len(updates),'frame rows,',len(reqs),'requirement slots,',len(sources),'source records')
