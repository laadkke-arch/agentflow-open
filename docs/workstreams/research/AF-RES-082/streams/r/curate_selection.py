import json,pathlib,datetime,re
D=pathlib.Path(__file__).resolve().parent
frame=json.load(open(D.parents[1]/'evidence/r-lib-frame.json'))['repositories']
case_specs=[('R1','archive',4,'v1.1.12','a4c6ec37fc8737a189ca7ec7095ec0161888f9e8','2025-03-24T12:32:51Z','https://archive.r-lib.org/',18),('R2','asciicast',5,'v2.3.1','f992b26f3cb30c799fbb95f6148852d8ae8a7f18','2024-01-21T20:50:48Z','https://asciicast.r-lib.org/',19),('R3','bench',9,'v1.1.4','45c72b2dcbba2b181d24c175ebb90ff8ed5eccad','2025-01-16T22:42:48Z','https://bench.r-lib.org/',14)]
cases={x[1]:x for x in case_specs}
reasons={1:('excluded','v2.11.4','Period formal tag supported by NEWS date 2025-10-08; README provides action documentation, example workflows, external help/blog/resources, but no publication instruction or website for this repository\'s own documentation. No own docs-site eligibility.'),2:('excluded','v2.0.0','Formal 2025-03-10 release. Recursive tree has only README.md as documentation; no reader-document source beyond README and no own docs-site link.'),3:('excluded_no_formal_release','','Releases=[] and tags=[]; NEWS first-public-release heading undated, DESCRIPTION 1.0.0.9000. No formal period tag verified.'),6:('excluded','1.2.0','Period release and man/*.Rd exist; README/DESCRIPTION only own GitHub repository and CRAN install/status links; no own docs-site publication link or instruction. All tags contains only 1.2.0.'),7:('excluded_no_period_release','v1.1.0','Last GitHub release 2022-07-13; tags and NEWS show no newer dated formal release in the period.'),8:('excluded','v1.5.0','Period release and man/*.Rd exist; README/DESCRIPTION link own GitHub repository, CRAN status/install, base-R manuals, but no own docs-site publication link or instruction.')}
updates=[]
for row in frame:
 r=dict(row); n=r['original_rank']; name=r['name']
 if name in cases:
  c=cases[name];r.update(status='included',case_id=c[0],last_2024_2025_formal_tag=c[3],tag_sha=c[4],published_at=c[5],site_url=c[6],exclusion_reason='',eligibility='man documentation source and DESCRIPTION URL at selected tag')
 elif n in reasons:
  s,t,reason=reasons[n];r.update(status=s,last_2024_2025_formal_tag=t,case_id='',exclusion_reason=reason)
 else:r.update(status='not_screened_after_third',last_2024_2025_formal_tag='',case_id='',exclusion_reason='Stop after first three eligible cases; release/tag/content not screened.')
 updates.append(r)
(D/'frame_updates.json').write_text(json.dumps({'org':'r-lib','frame_rows':164,'formal_release_candidates_screened':7,'selection_frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'first_three':case_specs,'rows':updates},ensure_ascii=False,indent=2)+'\n')
sources=[];receipts=[];attempts=[]
for i,p in enumerate(sorted((D/'raw').glob('*.json')),1):
 v=json.load(open(p));name=p.name.split('-')[0];
 if p.name.startswith('actions-files'):name='actions-files'
 case=cases.get(name); url=v.get('url',f'https://github.com/r-lib/{name}/tags');data=v.get('data','');status=v.get('status',200 if v.get('exit_code')==0 else 'failed')
 receipt={k:val for k,val in v.items() if k!='data'}
 receipt['cache_key']=p.stem
 receipts.append(receipt)
 if status!=200:
  attempts.append({'attempt_id':f'R-ATT-{i:03}','url':url,'opened_at_utc':v.get('opened_at_utc'),'result':v.get('error',v.get('stderr')),'counted':False});continue
 sid=f'R-{i:03}'
 fixed=case[3] if case else 'acquisition time / release metadata'
 loc='complete response, inspected selection fields'
 claim='recruitment eligibility only'
 obs='Public metadata inspected for formal tag/date and document-source/site eligibility.'
 if '-DESCRIPTION' in p.stem:
  loc='DESCRIPTION '+('L'+str(case[7])+' URL; L3 Version' if case else 'URL and Version fields')
  obs=(f'Declares package version {case[3].lstrip("v")} and public documentation address {case[6]}.' if case else 'Package description and URL fields do not advertise an own documentation site.')
  claim='supports public-site intent; does not establish historical content preservation'
 elif '-README' in p.stem:
  loc='README title, badges, installation, examples and links'
  obs={'archive':'Explains archive connections and extraction/writing examples; no old-version URL, navigation, publication-time or fixed-content policy found.','asciicast':'Shows SVG examples and refers to vignette; discusses product rendering features. These are not an explicit old-document-version preservation policy.','bench':'Explains mark/press/plotting examples and CRAN/GitHub installation; no old-document-version URL or preservation policy found.','actions-files':'Only title and one line describing files for r-lib/actions.','actions':'Refers to action subdirectories, examples, Tidyverse announcement and third-party help/resources; no own documentation-site publication instruction.','askpass':'R/SSH/Git credential examples and screenshots; only CRAN status/install and own repository links.','backports':'Function usage and links to base-R documentation; no own documentation-site publication instruction.'}.get(name,obs)
 elif '-NEWS' in p.stem:
  loc='NEWS version headings and selected release notes'
  obs={'archive':'Versions 1.1.9 through 1.1.12 say No changes; earlier entries concern runtime archive behavior. This does not promise a website snapshot.','asciicast':'2.3.1 adds display options; 2.1.0 says HTML is default in pkgdown for snapshots and animations still require SVG. This is a generator/content constraint, not an old-version URL promise.','bench':'1.1.4 fixes press/scale behavior and R requirement; no historical documentation route promise found.','actions':'NEWS explicitly dates v2.11.4 2025-10-08; later tags v2.12.0 onward are 2026. Formal period-tag fallback is observed.','ansistrings':'Only undated first release heading; no dated formal period tag.','available':'Development heading and latest stable 1.1.0; no newer stable version in NEWS.'}.get(name,obs)
 elif 'releases' in p.stem:
  loc='release tag_name,published_at,draft,prerelease; complete first page'
  vals=json.loads(data)
  obs='Period stable releases: '+str([(x['tag_name'],x['published_at']) for x in vals if not x['prerelease'] and not x['draft'] and '2024'<=x['published_at'][:4]<='2025'])
 elif 'tree' in p.stem:
  loc='recursive tree paths, documentation/source indicator only'
  obs='Tag contains '+('man/*.Rd documentation source and _pkgdown.yml file name (configuration contents not yet read).' if case else 'documentation paths checked; actions-files has only README, backports/askpass have man sources.')
 elif 'tag' in p.stem:
  loc='git tags / public tag object identifiers'
  obs=(f'Selected {case[3]} resolves to {case[4]}; full tag enumeration cross-checked where recorded.' if case else 'Tag enumeration supports period formal-tag screening; tag names alone are not dated release evidence.')
 sources.append({'source_id':sid,'lineage_id':f'r-lib/{name}'+('@'+case[3] if case else '/recruitment'),'source_type':'consumer_project_tag' if case else 'recruitment_metadata','url':url,'fixed_version':fixed,'fixed_sha':case[4] if case else None,'locator':loc,'opened_at_utc':v.get('opened_at_utc'),'questions':['Q1'] if case else ['recruitment'],'cases':[case[0]] if case else [],'observed':obs,'limitations':'Selection/requirements phase only; no deployment logs, hosting configuration, provider guide or current public HTML opened. Current org membership is not historical membership. Repeated files in this project are one lineage.','claim':claim,'polarity':'supports_scope_or_limits','count_as_independent':bool(case),'sha256':v.get('sha256'),'receipt_key':p.stem})
(D/'sources.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in sources))
(D/'receipts.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in receipts))
(D/'attempts.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in attempts))
req=[]
for c in case_specs:
 cid,repo,rank,tag,sha,pub,site,line=c
 sid=next(s['source_id'] for s in sources if s['cases']==[cid] and s['receipt_key']==f'{repo}-{tag}-DESCRIPTION')
 req.append({'case_id':cid,'original_rank':rank,'repo':'r-lib/'+repo,'language':next(x['language'] for x in frame if x['name']==repo),'tag':tag,'tag_sha':sha,'release_published_at':pub,'condition_id':cid+'-C1','condition_status':'supported_public_site_intent','role':'maintainer publication metadata -> external reader','requirement':'Package documentation is advertised at '+site,'original_utterance':'URL: '+site,'source_id':sid,'source_url':f'https://github.com/r-lib/{repo}/blob/{sha}/DESCRIPTION#L{line}','locator':f'DESCRIPTION L{line}','limitations':'A public address is evidence of intended entry point, not a promise of all historical versions or immutable content.'})
 req.append({'case_id':cid,'original_rank':rank,'repo':'r-lib/'+repo,'tag':tag,'tag_sha':sha,'condition_id':cid+'-C2','condition_status':'미확인','role':'reader preservation requirement','requirement':'미확인: independently promised old-version deep link, cross-version navigation, static-file publication or publication timing','original_utterance':None,'source_id':';'.join(s['source_id'] for s in sources if s['cases']==[cid] and any(t in s['receipt_key'] for t in ['README','NEWS','DESCRIPTION'])),'source_url':f'https://github.com/r-lib/{repo}/tree/{sha}','locator':'tag README, NEWS and DESCRIPTION read','limitations':'Product features and rendered examples were not converted into an invented website-preservation requirement; later maintainer policy evidence may refine this without replacing the case.'})
(D/'requirements.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in req))
print('selection rows',len(updates),'sources',len(sources),'independent consumer lineages',len(set(s['lineage_id'] for s in sources if s['count_as_independent'])),'requirements',len(req),'attempts',len(attempts))
