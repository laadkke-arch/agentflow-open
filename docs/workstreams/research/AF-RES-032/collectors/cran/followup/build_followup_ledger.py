"""Build research ledgers from read-only archive observations; no network or git writes.

Only followup/ is mutated. Original final/ sampling records remain immutable.
"""
from pathlib import Path
import csv, datetime as dt, hashlib, json, re, subprocess, tarfile
from collections import Counter
from lxml import html

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
NOW = dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00', 'Z')
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads((HERE / p).read_text())
def put(p, obj): (HERE / p).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
def lines(p): return [json.loads(s) for s in p.read_text().splitlines() if s.strip()]
refs = {x['reference_id']: x for x in lines(BASE / 'final/references.jsonl')}
obs = lines(HERE / 'archive_observations.jsonl')
obs.sort(key=lambda x: (x['publication_utc'], x['url']))
observed = {(o['project'], o['version']): o for o in obs}
current = {x['reference_id']: x for x in load('current-http.json')}
extra = {x['id']: x for x in load('additional-fetches.json')}
extra.update({x['id']: x for x in load('bts-official-fetches.json')})
extra['U-bts-airline-catalog'] = load('bts-catalog-fetch.json')
extra['U-rstudio-download'] = load('rstudio-download-fetch.json')
extra.update({x['id']: x for x in load('supporting-fetches.json')})
git_read = {x['id']: x for x in load('github-reread-receipt.json')}
sources, excerpt_manifest, sid_by_doc = [], [], {}
(HERE / 'excerpts').mkdir(exist_ok=True)

def source(sid, kind, pub, url, version, date, readat, location, findings,
           limits, rids, group, counted, category, **more):
    d = dict(source_id=sid, kind=kind, publisher=pub, original_url=url,
             version=version, publication_date=date if date is not None else '미확인', UTC=readat,
             read_location=location, findings=findings, limits=limits,
             reference_ids=rids, questions=['Q3', 'Q4', 'Q6', 'Q7', 'Q8'],
             duplicate_group=group, count_minimum=counted, count_category=category)
    d.update(more)
    if date is None:
        d['publication_unknown'] = dict(reason='No independently fixed publication time was established for this observed body; an HTTP Date header does not supply it.',
                                        last_evidence=url, next_source='Publisher dated edition/tag or a dated publication/deployment receipt for this exact body')
    sources.append(d)
    return d

def save_exact(name, body, location, parent_sha, note='Exact byte slice; no reserialization'):
    out = 'excerpts/' + name
    (HERE / out).write_bytes(body)
    row = dict(path=out, sha256=sha(body), bytes=len(body), source_location=location,
               parent_sha256=parent_sha, note=note)
    excerpt_manifest.append(row)
    return row

def archive_bytes(o):
    for root in (HERE / 'cache', BASE / 'cache'):
        f = root / o['archive_id']
        if f.exists(): return f
    raise FileNotFoundError(o['archive_id'])

key_versions = {
 'A-R01': ['1.29','1.30','1.46','1.47','1.49','1.50','1.52'],
 'A-R02': ['1.29','1.30','1.45','1.46','1.52'],
 'A-R03': ['2.1','2.32'],
 'A-R04': ['2.3','2.4','2.32'],
 'A-R05': ['1.0.1','1.0.2','1.1.0','1.1.1','1.2.1'],
 'A-R06': ['0.8.5','1.0.0','1.2.1']}
minimum_followups = {('A-R01','1.30'),('A-R02','1.30'),('A-R05','1.0.2'),('A-R06','1.0.0')}
supplemental = []
for o in obs:
    for d in o['documents']:
        rid = d['reference_id']
        sid = 'R-F%03d' % (len(sid_by_doc)+1)
        sid_by_doc[(rid,o['version'])] = sid
        findings = dict(member_present=d['original_member_present'], old_href_present=d['old_href_present'],
                        links=d.get('links', []), purpose_paragraphs=d.get('paragraphs', []),
                        other_members=d.get('matching_html_other_members', []))
        ep = []
        if o['version'] in key_versions[rid]:
            with tarfile.open(archive_bytes(o), 'r:gz') as t:
                if d['original_member_present']:
                    body=t.extractfile(d['member_path']).read()
                    doc=html.fromstring(body)
                    terms={
                      'A-R01':['datatables','toy example'],
                      'A-R02':['docco','knit_child'],
                      'A-R03':['page-break-after','compatibility reason'],
                      'A-R04':['Pandoc','RStudio'],
                      'A-R05':['dbplyr','backend news'],
                      'A-R06':['nycflights','Bureau of Transportation','starwars','Star Wars']
                    }[rid]
                    elements=[e for e in doc.xpath('//p|//h1|//h2|//h3') if any(w.lower() in e.text_content().lower() for w in terms)]
                    rawlines=body.splitlines(keepends=True)
                    selected=[]
                    for e in elements[:12]:
                        start=e.sourceline-1
                        end=start
                        closing=('</'+e.tag+'>').encode()
                        while end<len(rawlines)-1 and closing not in rawlines[end]: end+=1
                        fragment=b''.join(rawlines[start:end+1])
                        er=save_exact(f'{rid}-{o["version"]}-{len(ep)+1}.html-fragment.txt', fragment,
                                      f'{o["url"]}!/{d["member_path"]}:L{start+1}-L{end+1}', d['member_sha256'])
                        ep.append(er)
                        selected.append(dict(line=start+1,text=' '.join(e.text_content().split()),
                                             hrefs=e.xpath('.//a/@href'),excerpt_path=er['path']))
                    findings['boundary_direct_read']=selected
                    supplemental.append(dict(reference_id=rid,version=o['version'],publication_utc=o['publication_utc'],
                                             read_at_utc=NOW,source_id=sid,fragments=selected))
                else:
                    # Preserve publication inventory for a missing member, not invented HTML.
                    er=save_exact(f'{rid}-{o["version"]}-html-inventory.txt',
                                  ('\n'.join(o['html_members'])+'\n').encode(),
                                  o['url']+' tar member inventory',o['archive_sha256'],
                                  'Derived listing of all compiled HTML members; not an original HTML byte slice')
                    ep.append(er)
        counted=(rid,o['version']) in minimum_followups
        reason=('Changed compiled HTML state: one selected followup per distinct manuscript'
                if counted else 'Duplicate/original/unchanged purpose text or extra boundary state; excluded from minimum')
        source(sid,'actual_CRAN_archive_compiled_HTML' if d['original_member_present'] else 'actual_CRAN_archive_missing_member_inventory',
               o['project']+' authors / CRAN',o['url'],o['version'],o['publication_utc'],
               o['response_completed_utc'],d['member_path']+'; '+o['project']+'/DESCRIPTION Date/Publication',
               findings,
               ['Publication metadata explicitly says UTC; archive-index mtime is not used as publication time.',
                'No package installation, browser execution, successful click, or reader failure is established.',
                'All retained listed CRAN source archives were read; other channels or deleted unlisted archives remain outside this inventory.',
                'Missing member is checked against every compiled HTML member by recorded href/title/topic searches; no claim of global documentary absence.'],
               [rid], 'consumer-'+rid+('-followup' if counted else '-additional-state'), counted, 'consumer_followup',
               minimum_count_reason=reason, archive_sha256=o['archive_sha256'], member_sha256=d.get('member_sha256'),
               original_member_present=d['original_member_present'],publication_role='consumer_publication',
               publication_evidence=o['project']+'/DESCRIPTION Date/Publication', excerpt_paths=[x['path'] for x in ep],
               inventory_evidence='all-editions-inventory.json', automated_observation='archive_observations.jsonl',
               inspection_method='Read actual compressed archive and compiled HTML; extracted all relevant href/topic paragraphs. Critical before/after boundary text separately reread and preserved.',
               detailed_boundary_reread_utc=NOW if ep else None)

# Upstream actual HTTP observations. HTTP body, fragment, and purpose have separate fields.
current_findings = {
'A-R01': 'Raw HTTP and www variants redirect to https://datatables.net/. Body identifies DataTables as a table/data-grid library. Current generation has changed; the frozen purpose does not demand the old example run unchanged.',
'A-R02': 'Raw github.io Docco URL redirects to ashkenas.com/docco/. The body still explains Docco and displays comments alongside corresponding code.',
'A-R03': 'Raw legacy MDN path redirects to /Web/CSS/Reference/Properties/page-break-after. The property description and Page break aliases section remain; always maps to page. Deprecation is compatible with the sealed consumer paragraph, which already explains replacement and compatibility.',
'A-R04': 'The raw preview path redirects to the current RStudio IDE guide, with #rstudio-ide-oss-downloads. That exact id exists as a deliberately retained span in Install links and points readers to ./download.html. Current guide states Revision 47 Published 2026-11-13; this is not the first redirect date.',
'A-R05': 'The raw hadley/dbplyr URL redirects to tidyverse/dbplyr. The current README identifies dbplyr as the database backend for dplyr; the package-successor purpose survives. A separate historical NEWS anchor is not the selected reference.',
'A-R06': 'HTTP 200 final payload is BorderCrossing.aspx with no airline content. Its onload redirect() script names a transborder/TBDR_BC destination. No browser execution or reader failure is inferred; the explicitly requested script destination separately returned 503.'}
purpose_results={'A-R01':'satisfied_generic_library_background','A-R02':'satisfied_style_background','A-R03':'satisfied_compatibility_property','A-R04':'partially_satisfied_IDE_download_path; exact_preview_and_Pandoc_binary_unverified','A-R05':'satisfied_package_successor','A-R06':'not_satisfied_airline_provenance'}
for i,(rid,c) in enumerate(sorted(current.items()),1):
    sid='R-U%02d'%i
    body=(HERE/'cache'/c['cache_file']).read_bytes()
    doc=html.fromstring(body)
    fragment=c['final_url'].partition('#')[2]
    anchor=bool(doc.xpath('//*[@id=$v or @name=$v]',v=fragment)) if fragment else None
    source(sid,'actual_HTTP_response_and_primary_body',
           ['DataTables / SpryMedia','Jeremy Ashkenas / Docco','MDN contributors','Posit','tidyverse / dbplyr','US Bureau of Transportation Statistics'][i-1],
           c['url'],'current observed response',None,c['checked_at_utc'],c['final_url'],current_findings[rid],
           ['A current HTTP response is not a historical server observation.',
            'HTTP Date header is not used as publication, correction, or effective-change time.',
            'The source does not establish reader access, successful execution, or first deployment.'],
           [rid], 'upstream-current-'+rid, rid!='A-R06','upstream',
           sha256=c['sha256'],status=c['status'],final_url=c['final_url'],redirect_chain=c['redirect_chain'],
           raw_fragment=refs[rid]['fragment'],final_fragment=fragment or None,final_fragment_present=anchor,
           needed_section_present=False if rid=='A-R06' else True,
           purpose_result=purpose_results[rid], publication_role='observed_at_only',
           minimum_count_reason='BTS empty redirect payload is technical evidence, not a substantive original; excluded' if rid=='A-R06' else 'Directly read primary target body')

extra_specs=[
('R-U07','U-datatables2','DataTables / Allan Jardine','2024-03-15','DataTables 2 release','Release announcement; legacy API removal / v1 maintenance / jQuery dependency',
 'The announcement demonstrates product/version change while retaining the broad table-library role. It does not date HTTP/www redirects, and the original consumer does not pin a DataTables version.', ['A-R01'],True,'datatables-2-release'),
('R-U08','U-posit-rename','Posit / J.J. Allaire and Hadley Wickham','2022-07-27','RStudio is becoming Posit','Company-name announcement and explicit continuation of RStudio IDE name',
 'The company rebrand is distinct from the IDE name and from the raw preview redirect. Consumer pandoc.html had already been removed in 2020; no causal correction chain to this 2022 event is claimed.', ['A-R04'],True,'posit-rename-2022'),
('R-U09','U-bts-2014-table','US Bureau of Transportation Statistics','2014-09-17','State Transportation Statistics 2014 table 4-7','SOURCE paragraph; 2012/2013 airport on-time table',
 'A dated official statistics table cites Airline On-Time Performance Data at DatabaseInfo.asp?DB_ID=120 as of July 2014. This supports the old subject association, not an HTTP capture of selected DB_ID=120&Link=0 nor the last correct server state.', ['A-R06'],True,'bts-sts2014-table4-7'),
('R-U10','U-bts-rosap-2013','US Bureau of Transportation Statistics / NTL ROSA-P','2013-01-01','Airline Service Quality Performance 234 [2013-01]','Title, publisher metadata, Abstract, Download document link / DOI',
 'Official repository record identifies January 2013 airline performance data and a downloadable ZIP. Metadata publication date is not a verified original web deployment date. Only January is covered, not all NYC 2013 flights; ZIP contents were not downloaded or compared.', ['A-R06'],True,'bts-rosap-2013-01'),
('R-U11','U-bts-airline-catalog','US Bureau of Transportation Statistics',None,'Airline Service Quality Performance 234 monthly catalog','Title and 2013 section, all 12 month links',
 'Current official catalog names On-Time performance and links all 12 months of 2013. It is a scoped replacement for identifying airline data provenance/year, not proof of identity with the exact filtered nycflights13 table or accessibility of every ZIP.', ['A-R06'],True,'bts-monthly-airline-catalog'),
('R-U14','U-rstudio-download','Posit',None,'RStudio IDE guide 2026.11.0 Download RStudio','RStudio Desktop and Server download sections',
 'Current page gives explicit RStudio Desktop/Server installer links. It resolves the general IDE-download component but is not the old preview distribution and does not prove installed Pandoc version or compatibility with rmarkdown 2.1.', ['A-R04'],True,'rstudio-current-download'),
('R-U15','U-rmd-find-pandoc','rmarkdown authors / Posit',None,'find_pandoc reference','dir argument and Note',
 'Current official function reference states that the IDE bundles Pandoc and exposes RSTUDIO_PANDOC. This is documentation of bundled-tool behavior, not an executed check of a particular 2020 or 2026 installer.', ['A-R04'],False,'rmd-current-find-pandoc'),
('R-U16','U-rmd-lesson','rmarkdown authors / Posit',None,'Introduction / lesson 1','Installation paragraph',
 'The current introductory lesson supplies R package installation guidance; it does not restore the removed pandoc.html paragraph or establish the raw preview URL purpose.', ['A-R04'],False,'rmd-current-lesson1'),
]
# The first two BTS fetch ids were established by the fetch ledger; tolerate their exact names without guessing URLs.
bts_keys=list(json.loads((HERE/'bts-official-fetches.json').read_text()))
for row in bts_keys:
    if 'state_transportation' in row['url']: extra['U-bts-2014-table']=row
    elif 'rosap.ntl.bts.gov/view/dot/6741' in row['url']: extra['U-bts-rosap-2013']=row
for sid,key,publisher,date,version,loc,finding,rids,count,group in extra_specs:
    x=extra[key]
    source(sid,'official_primary_document',publisher,x['url'],version,date,
           x.get('response_completed_utc',x.get('request_started_utc')),loc,finding,
           ['Dates refer to the document/metadata role stated; effective redirect or consumer-change dates remain unverified.',
            'No downloaded package is executed and no user click/failure is implied.'],rids,group,count,'upstream',
           sha256=x.get('sha256'), status=x.get('status'),final_url=x.get('final_url'),cache_file=x.get('cache_file'),
           publication_role='source_document_date' if date else '미확인')

commits=[
('R-C01','knitr-redirect','knitr-redirect.json',['A-R01','A-R02'],['vignettes/datatables.Rmd','vignettes/docco-linear.Rmd'],
 'One source commit says resolve 301 redirects and changes HTTP DataTables to HTTPS plus Docco github.io to ashkenas.com. The actual knitr 1.30 HTML independently contains both changes. This is one source-edit event affecting two references, not two independent upstream-effective events.'),
('R-C02','dplyr-links','dplyr-links.json',['A-R05'],['vignettes/compatibility.Rmd'],
 'The source patch changes dbplyr package-root and separate NEWS links from hadley to tidyverse. The message attributes the work to check_win_devel hints; the check log itself was not retrieved and not treated as executed evidence.'),
('R-C03','rmd-remove','rmd-remove.json',['A-R04'],['vignettes/pandoc.Rmd','pkgdown/_pkgdown.yml'],
 'The source commit removes the Pandoc installation vignette and calls it no longer useful. Actual CRAN 2.4 archive omits that HTML. This is retirement, before the 2022 company rename, not a proved redirect repair.'),
('R-C04','dplyr-switch','dplyr-switch.json',['A-R06'],['vignettes/dplyr.Rmd'],
 'The source changes the introductory example from 2013 NYC flights/BTS to Star Wars. Later CRAN 0.8.5 still publishes the old example; CRAN 1.0.0 first contains the new example among enumerated editions. A later SWAPI URL change also means the original source-patch target is not byte-identical to the 1.0.0 SWAPI target.'),
('R-U12','docco-cname','docco-cname.txt',['A-R02'],['CNAME'],
 'The 2017 source configuration adds ashkenas.com as CNAME. It is source configuration, not proof of DNS/Pages deployment, an exact redirect-start time, or a consumer failure.')]
for sid,key,cache,rids,paths,finding in commits:
    obj=json.loads((HERE/'cache'/cache).read_text()); rec=git_read[key]
    ev=dict(sha=obj['sha'],html_url=obj['html_url'],author=obj['commit']['author'],committer=obj['commit']['committer'],
            message=obj['commit']['message'],parents=[p['sha'] for p in obj['parents']],
            relevant_files=[{k:f.get(k) for k in ('filename','status','previous_filename','patch')} for f in obj['files'] if f['filename'] in paths])
    out='excerpts/'+sid+'-source-change.json';put(out,ev)
    source(sid,'official_repository_commit',obj['html_url'].split('/')[3:5],obj['html_url'],obj['sha'],obj['commit']['committer']['date'],
           rec['read_completed_utc'],'; '.join(paths),finding,
           ['Commit time is consumer_source_edit or upstream_source_configuration, not build, merge, public deployment, or reader observation.',
            'A fetched API/HTML representation is one original commit, not multiple independent sources.'],
           rids,'source-commit-'+obj['sha'],sid=='R-U12','upstream' if sid=='R-U12' else 'consumer_followup',
           publication_role='upstream_source_configuration' if sid=='R-U12' else 'consumer_source_edit',
           evidence_path=out,api_url=obj['url'],source_edit_utc=obj['commit']['committer']['date'])

# Fixed MDN source is useful temporal counterevidence, conservatively deduplicated with the property manuscript.
mdn=extra['U-mdn-fixed-2020']
source('R-U13','official_fixed_repository_source','MDN contributors',mdn['url'],
       'dc9089417852530f233c345bd6821d6e06f11b1e','2020-12-18T10:05:08Z',mdn['response_completed_utc'],
       'files/en-us/web/css/page-break-after/index.html; legacy-property note and page-break-alias table',
       'The fixed December 2020 source already describes page-break-after as legacy and maps always to break-after: page. The consumer January 2020 distribution independently already contains a compatibility qualifier.',
       ['This source is not proof of the January 2020 MDN web response or actual deployment time.',
        'Same property manuscript as R-U03; excluded from minimum to avoid counting representations/near-identical content twice.'],
       ['A-R03'],'upstream-current-A-R03',False,'upstream',sha256=mdn['sha256'],publication_role='source_commit',
       source_commit_url='https://github.com/mdn/content/commit/dc9089417852530f233c345bd6821d6e06f11b1e')
history=json.loads((HERE/'cache/mdn-new-history.txt').read_text())
move=next(x for x in history if x['sha']=='2d78abb3e793352e24e976ce0e68c08d817bd7f3')
put('excerpts/R-U17-mdn-path-history.json',dict(sha=move['sha'],html_url=move['html_url'],commit=move['commit']))
source('R-U17','official_repository_path_history','MDN contributors',move['html_url'],move['sha'],move['commit']['committer']['date'],NOW,
       'Commit-history record for files/en-us/web/css/reference/properties/page-break-after/index.md',
       'The history record dates the CSS property path reorganization source commit to 2025-10-30. Current request independently follows a redirect to that path.',
       ['Only the path-history commit record was read, not the entire many-file diff. This is not an actual redirect deployment timestamp.',
        'Excluded from minimum; event/supporting metadata rather than a distinct fully read primary manuscript.'],
       ['A-R03'],'mdn-property-path-metadata',False,'upstream',evidence_path='excerpts/R-U17-mdn-path-history.json',publication_role='upstream_source_edit')

# Preserve source-to-generated-document correspondence for the Docco classic variant.
ko=observed[('knitr','1.30')]
with tarfile.open(archive_bytes(ko),'r:gz') as t:
    b=t.extractfile('knitr/vignettes/docco-classic.Rmd').read()
    save_exact('A-R02-classic-generator.Rmd',b,ko['url']+'!/knitr/vignettes/docco-classic.Rmd',sha(b),
               'Complete very short generator source; shows readLines of docco-linear.Rmd and knit_child. It was read, not executed.')

# Exact current response snippets, with parent and fragment hashes.
snip_specs=[
 ('A-R01-current.html',b'DataTables',1500,'R-U01-current-fragment.txt'),
 ('A-R02-current.html',b'<p>',1600,'R-U02-current-fragment.txt'),
 ('A-R03-current.html',b'id="page_break_aliases"',2000,'R-U03-aliases-fragment.txt'),
 ('A-R04-current.html',b'<section id="install-links"',1600,'R-U04-install-anchor-fragment.txt'),
 ('A-R05-current.html',b'database backend',1700,'R-U05-readme-fragment.txt'),
 ('A-R06-current.html',b'',10000,'R-U06-full-redirect-payload.html')]
for cache,needle,length,name in snip_specs:
    b=(HERE/'cache'/cache).read_bytes();i=b.lower().find(needle.lower())
    if i<0: i=0
    save_exact(name,b[i:i+length],cache+' byte offset '+str(i),sha(b))

# Event boundaries: first means only among every enumerated retained CRAN archive in this investigation.
def ed(rid,version):
    r=refs[rid];o=observed[(r['consumer_project'],version)];d=next(z for z in o['documents'] if z['reference_id']==rid)
    return dict(version=version,publication_utc=o['publication_utc'],url=o['url'],archive_sha256=o['archive_sha256'],
                member_path=d['member_path'],member_present=d['original_member_present'],member_sha256=d.get('member_sha256'),
                source_id=sid_by_doc[(rid,version)],observed_at_utc=o['response_completed_utc'])
def boundary(rid,old,new,kind,oldhref,newhref,same=True):
    project=refs[rid]['consumer_project'];seq=[o['version'] for o in obs if o['project']==project]
    return dict(kind=kind,last_observed_old=ed(rid,old),first_observed_new=ed(rid,new),
                old_href=oldhref,new_href=newhref,same_frozen_purpose=same,
                enumerated_intervening_versions=seq[seq.index(old)+1:seq.index(new)],
                uninspected_intervening_count=0,
                first_claim_scope='First among every retained CRAN source archive enumerated from the frozen starting edition through the observed current edition; no global first-publication claim across deleted/unlisted releases or other channels.')
boundaries={
 'A-R01':[boundary('A-R01','1.29','1.30','same-purpose literal href correction','http://www.datatables.net','https://www.datatables.net'),
           boundary('A-R01','1.46','1.47','same-purpose canonical host change','https://www.datatables.net','https://datatables.net'),
           boundary('A-R01','1.49','1.50','different library recommendation / changed example','https://datatables.net','https://github.com/fiduswriter/simple-datatables/',False)],
 'A-R02':[boundary('A-R02','1.29','1.30','same-purpose literal href correction','http://jashkenas.github.io/docco/','http://ashkenas.com/docco/'),
           boundary('A-R02','1.45','1.46','introductory external link sentence removed; Docco style instructions remain','http://ashkenas.com/docco/',None,False)],
 'A-R03':[],
 'A-R04':[boundary('A-R04','2.3','2.4','original HTML document retired; no same-purpose link replacement established',refs['A-R04']['raw_href'],None,False)],
 'A-R05':[boundary('A-R05','1.0.1','1.0.2','same-purpose owner/scheme href correction',refs['A-R05']['raw_href'],'https://github.com/tidyverse/dbplyr/'),
           boundary('A-R05','1.1.0','1.1.1','compatibility document retired; in-packages dbplyr source example has different purpose','https://github.com/tidyverse/dbplyr/',None,False)],
 'A-R06':[boundary('A-R06','0.8.5','1.0.0','example replaced by Star Wars; airline-provenance purpose retired',refs['A-R06']['raw_href'],'http://swapi.dev',False)]}

specs={
'A-R01':dict(event='datatable-http-www-canonicalization',verdict='유지',
 rationale='봉인된 목적은 DataTables 라이브러리 배경 읽기이며 현재 정식 홈페이지가 그 역할을 충족한다. HTTPS/현재 정식 주소를 병기할 수 있다. knitr 1.50의 simple-datatables는 다른 라이브러리 예제로 바뀐 결과이므로 원 예제 링크를 그 대상으로 무조건 바꾸지 않는다.',
 unknown='HTTP→HTTPS/www 정리의 실제 시행일과 마지막 정상 원주소 서버 상태 미확인.',next='당시 DataTables 발행자의 시행 공지 또는 시간 고정 HTTP redirect 보존본',
 source='R-C01',related=['R-U01','R-U07','R-C01'],latest='1.52'),
'A-R02':dict(event='docco-github-pages-to-ashkenas-domain',verdict='유지',
 rationale='현재 리다이렉트 도착 본문은 Docco 스타일 설명을 제공한다. 2017 CNAME 소스와 2020 소비자 소스 수정·배포를 구분한다. 1.46에서 링크 문장은 없어져도 Docco 스타일 지침은 남으며 이를 도구 실패로 해석하지 않는다.',
 unknown='CNAME 설정의 실제 배포와 redirect 시행일 미확인.',next='GitHub Pages의 당시 배포 영수증 또는 시행 시각이 고정된 Docco 이전 공지',
 source='R-C01',related=['R-U02','R-U12','R-C01'],latest='1.52'),
'A-R03':dict(event='mdn-css-reference-path-reorganization',verdict='유지',
 rationale='원판이 호환성용 page-break-after와 현대 break-after를 이미 구분한다. 현재 문서도 구 속성의 의미와 alias를 설명한다. 단지 deprecated라는 이유로 원 링크를 break-after 문서로 덮어쓰면 원 코드의 설명이 약해진다. 32개 배포판에서 raw href가 유지됐다.',
 unknown='2025-10-30 소스 경로 변경이 실제 웹 redirect로 시행된 시점 미확인; 고장 시작을 관측하지 않았다.',next='MDN 배포 이력 또는 해당 경로의 날짜 고정 HTTP 보존본',
 source=None,related=['R-U03','R-U13','R-U17'],latest='2.32'),
'A-R04':dict(event='rstudio-preview-path-to-posit-user-guide',verdict='보류',
 rationale='현재 IDE 다운로드 경로와 살아 있는 호환 앵커는 확인된다. 그러나 원 URL의 preview 의도와 해당 구판 요구를 충족하는 특정 IDE/Pandoc 배포물은 확인하지 못했다. 소비자 문서 자체는 2020년 2.4에서 폐기됐으므로 2022 회사명 변경에 대한 링크 정정으로 셀 수 없다.',
 unknown='preview 판을 요구한 원 의도·원 링크의 단계별 redirect 시행일·현 다운로드가 rmarkdown 2.1에 주는 실제 Pandoc/실행 호환성 미확인.',next='2020 해당 IDE preview 배포 HTML 또는 편집자 설명(왜 preview를 선택했는지); 실행이 필요하면 고정 IDE/Pandoc 설치 판과 rmarkdown 2.1로 별도 검증',
 source='R-C03',related=['R-U04','R-U08','R-U14','R-U15','R-C03'],latest='2.32'),
'A-R05':dict(event='dbplyr-github-owner-hadley-to-tidyverse',verdict='유지',
 rationale='원 링크는 별도 backend NEWS 앵커가 아니라 dbplyr 패키지 루트다. 현재 redirect는 후계 패키지와 데이터베이스 backend 설명에 도착하므로 봉인된 최소 목적을 충족한다. 1.0.2의 literal href 정정은 실제 HTML에 있다.',
 unknown='GitHub owner 이전과 redirect 시행일·check_win_devel 원 로그·별도 backend NEWS 절의 정확한 역사 상태 미확인.',next='당시 dbplyr 소유권 이전 공지/시간 고정 redirect 관측(선택 링크 루트와 동일 사건)',
 source='R-C02',related=['R-U05','R-C02'],latest='1.2.1'),
'A-R06':dict(event='bts-db120-to-border-crossing-redirect',verdict='교체',
 rationale='현재 raw URL은 HTTP 200이어도 항공통계가 없는 국경통과 redirect payload로 끝나므로 출처 식별 목적에 실패한다. 공식 Airline Service Quality Performance 234 카탈로그는 2013년 12개월을 명시하므로 원 2013 설명과 함께 병기/교체할 근거가 있다. 1.0.0의 Star Wars는 전혀 다른 예제로, 원2013 출처를 교체할 후보가 아니다.',
 unknown='항공 페이지가 국경통과 경로로 바뀐 시행일·마지막 정상 HTTP 상태·2013 원파일과 nycflights13의 정확한 가공/필터 동일성·실제 독자 실패 미확인.',next='옛 DatabaseInfo.asp?DB_ID=120&Link=0의 날짜 고정 항공통계 본문/redirect 보존본; 정확 데이터 재현에는 2013 월별 ZIP과 nycflights13 생성 스크립트',
 source='R-C04',related=['R-U06','R-U09','R-U10','R-U11','R-C04'],latest='1.2.1')}
cases=[]
source_lookup={x['source_id']:x for x in sources}
for rid,sp in specs.items():
    r=refs[rid];c=current[rid];docs=[o for o in obs if o['project']==r['consumer_project']]
    source_info=source_lookup.get(sp['source'])
    date_roles=dict(upstream_effective=None,upstream_effective_status='미확인',
                    upstream_source_configuration='2017-06-20T18:33:17Z' if rid=='A-R02' else None,
                    upstream_source_edit='2025-10-30T16:59:53Z' if rid=='A-R03' else None,
                    consumer_source_edit=source_info.get('source_edit_utc') if source_info else None,
                    source_edit_role='same-purpose href correction' if rid in ['A-R01','A-R02','A-R05'] else ('purpose/document retirement' if sp['source'] else 'no matching source correction established'),
                    consumer_merge=None,consumer_build=None,reader_report=None,reader_click=None,
                    consumer_merge_status='미확인',consumer_build_status='미확인',reader_report_status='미확인',reader_click_status='미확인',
                    current_http_observed_at=c['checked_at_utc'])
    cases.append(dict(reference_id=rid,sample='A',route='R',frozen_purpose=r['click_purpose'],minimum_success=r['minimum_success'],
        upstream_event_key=sp['event'],raw_href=r['raw_href'],current_http=source_lookup['R-U%02d'%int(rid[-2:])],
        verdict=sp['verdict'],verdict_subject='researcher reassessment of reusing the originally sealed recommendation, at current observation',
        rationale=sp['rationale'],unknowns=[dict(reason=sp['unknown'],last_evidence=sp['related'],next_source=sp['next']),
          dict(reason='merge/build/reader clocks have no matching primary record in the inspected sources',last_evidence=sp['related']+[sid_by_doc[(rid,sp['latest'])]],next_source='Same-event build/publication receipt or first-person reader report stating the same document and purpose')],
        date_roles=date_roles,boundaries=boundaries[rid],last_observed_old=boundaries[rid][0]['last_observed_old'] if boundaries[rid] else ed(rid,sp['latest']),
        first_observed_new=boundaries[rid][0]['first_observed_new'] if boundaries[rid] else None,
        first_new_meaning=boundaries[rid][0]['kind'] if boundaries[rid] else 'No href change observed in all enumerated editions; no broken-purpose event start established',
        latest_distribution=ed(rid,sp['latest']),source_ids=sp['related']+[sid_by_doc[(rid,v)] for v in key_versions[rid]],
        enumerated_archives=len(docs),read_archives=len(docs),uninspected_enumerated_archives=0,
        missing_unlisted_editions='미확인: retained public CRAN inventory scope only',
        strict_delay_eligible=False,right_censored=False,strict_delay_reason='Upstream effective start is not established; retirement events are also not same-purpose corrections.',
        reader_failure_observed=False,reader_failure_status='미확인; researcher HTTP probe is not a reader report',
        replacement_url=extra['U-bts-airline-catalog']['url'] if rid=='A-R06' else None,
        blinded_comparison_status='not performed by collector; these are full-context adjudications, not masked-view predictions'))

def seconds(a,b):return int((dt.datetime.fromisoformat(b.replace('Z','+00:00'))-dt.datetime.fromisoformat(a.replace('Z','+00:00'))).total_seconds())
intervals=[]
for case in cases:
    rid=case['reference_id']
    intervals.append(dict(interval_id='R-I-'+rid+'-strict',reference_id=rid,event_key=case['upstream_event_key'],
       clock_pair='upstream_effective→consumer_public_same_purpose_correction',start=None,end=None,
       eligible=False,classification='미확인',right_censored=False,numerator=0,
       conditional_eligible_denominator=0,reason=case['strict_delay_reason'],
       next_source=case['unknowns'][0]['next_source'],source_ids=case['source_ids']))
    if rid in ['A-R01','A-R02','A-R05','A-R04','A-R06']:
        start=case['date_roles']['consumer_source_edit'];end=case['first_observed_new']['publication_utc'];s=seconds(start,end)
        same=rid in ['A-R01','A-R02','A-R05']
        intervals.append(dict(interval_id='R-I-'+rid+'-source-publication',reference_id=rid,
           event_key=case['date_roles']['source_edit_role']+':'+str(start),
           clock_pair='consumer_source_edit→observed_CRAN_publication',start=start,end=end,
           precision='seconds encoded in commit committer timestamp and original DESCRIPTION Date/Publication UTC',
           seconds=s,days=s/86400,eligible_for_aux_source_publication=same,
           eligible_for_strict_upstream_publication=False,right_censored=False,
           classification='same-purpose compiled href correction' if same else 'retirement/replacement auxiliary interval; excluded from correction lag',
           reason='Verified source diff and actual compiled HTML of same purpose' if same else 'Document/purpose changes; BTS source target also changes before publication',
           source_ids=[specs[rid]['source'],case['first_observed_new']['source_id']],
           missing_merge=True,missing_build=True,missing_reader=True))

put('cases.json',cases);put('intervals.json',intervals);put('chains.json',[dict(reference_id=c['reference_id'],upstream_event_key=c['upstream_event_key'],date_roles=c['date_roles'],boundaries=c['boundaries'],source_ids=c['source_ids'],unknowns=c['unknowns']) for c in cases])
put('boundary-direct-reads.json',supplemental);put('excerpt-manifest.json',excerpt_manifest)
(HERE/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))

# Search/failed access are kept out of the original-source minimum.
queries=[
'site:posit.co/blog RStudio becoming Posit 2022 name change',
'site:datatables.net/blog DataTables 2 2024 jQuery',
'site:github.com/jashkenas/docco ashkenas.com docco',
'site:bts.gov "DatabaseInfo.asp?DB_ID=120"',
'site:bts.gov airline on time performance data 2013 download',
'site:github.com/rstudio/rmarkdown "pandoc.Rmd" remove',
'site:github.com/yihui/knitr "docco-classic" "removed"',
'site:docs.posit.co RStudio Pandoc bundled',
'site:rmarkdown.rstudio.com RStudio includes Pandoc version']
attempts=[dict(attempt_id='R-Q%02d'%(i+1),kind='discovery_search',query=q,
               recorded_at_utc=NOW,request_utc='미확인; exact query-request wallclock was not separately saved',
               result='Primary sources opened are separately recorded in sources.jsonl; snippets not counted',count_minimum=False) for i,q in enumerate(queries)]
attempts.append(dict(attempt_id='R-HTTP-FAIL-01',kind='actual_HTTP_failure',**extra['U-bts-js'],count_minimum=False,
                     result='Source-visible downstream JS destination fetched directly; no browser JS execution'))
attempts.extend([
 dict(attempt_id='R-GH-PATH-01',kind='official_repository_path_history',url='https://api.github.com/repos/yihui/knitr/commits?path=vignettes/docco-classic.Rmd&since=2020-06-01T00:00:00Z&until=2020-09-23T00:00:00Z',
      result='No commit in classic generator path; archive generator reads docco-linear.Rmd, whose patch is in R-C01',count_minimum=False),
 dict(attempt_id='R-GH-PATH-02',kind='official_repository_path_history',url='https://api.github.com/repos/jashkenas/docco/commits?path=CNAME&sha=gh-pages',
      result='Empty history at this path; actual CNAME source found at jashkenas/jashkenas.github.io',count_minimum=False)])
(HERE/'attempts.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in attempts))

summary=dict(generated_at_utc=NOW,seal_sha='168d90b8519bcb4f673acc659bbaae895f79fca5',
             reference_count=6,archive_count=len(obs),document_observation_count=sum(len(o['documents']) for o in obs),
             read_archives_by_project=dict(Counter(o['project'] for o in obs)),
             uninspected_enumerated_archives=0,failed_enumerated_archives=sum('error' in o for o in obs),
             minimum_counted_sources_by_category=dict(Counter(s['count_category'] for s in sources if s['count_minimum'])),
             minimum_counted_sources=[s['source_id'] for s in sources if s['count_minimum']],
             source_records=len(sources),verdict_counts=dict(Counter(c['verdict'] for c in cases)),
             actual_same_purpose_literal_href_corrections=3,reference_denominator=6,
             independent_same_purpose_source_edit_events=2,auxiliary_source_publication_reference_pairs=3,
             strict_upstream_publication_pairs=0,strict_pair_eligible_denominator=0,
             strict_pair_applicability='해당 없음: eligible denominator 0; six examined references retain unknown starts or non-comparable purpose changes',
             right_censored_cases=0,reader_failure_reports=0,
             collector_role='Internal parallel collector; not independent external reviewer or blinded judge',
             scope='All writes confined to collectors/cran/followup; no git mutation and no sealed A change')
put('summary.json',summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))
