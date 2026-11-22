from pathlib import Path
from html.parser import HTMLParser
import json, csv, hashlib, tarfile, zipfile, io, re, datetime

P = Path(__file__).resolve().parent
C = P / 'cache'
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
receipts = []
for p in sorted(P.glob('downloads[0-9]*.json'), key=lambda p: int(re.search(r'\d+', p.name).group())):
    receipts.extend(json.loads(p.read_text()))
known = {r['file']: r for r in receipts}

def body(f, member=None):
    b = (C / f).read_bytes()
    if member and f.endswith('.tar.gz'):
        with tarfile.open(fileobj=io.BytesIO(b)) as a:
            return a.extractfile(member).read()
    if member and f.endswith('.zip'):
        with zipfile.ZipFile(io.BytesIO(b)) as a:
            return a.read(member)
    return b

def source(sid, event, f, kind, publisher, version, location, finding, limit,
           date=None, role=None, member=None, count=False, group=None):
    r = known[f]
    b = body(f, member)
    return {
        'source_id': sid, 'reference_ids': [event], 'questions': ['Q3', 'Q4', 'Q5', 'Q6', 'Q7'],
        'source_type': kind, 'publisher': publisher, 'original_url': r['url'],
        'version': version, 'publication_date': date, 'publication_date_role': role,
        'observed_utc': r['observed_utc'], 'directly_read': True,
        'read_location': location, 'member': member, 'verified': finding, 'limitations': limit,
        'artifact_sha256': r['sha256'], 'artifact_bytes': r['bytes'],
        'member_sha256': hashlib.sha256(b).hexdigest() if member else None,
        'http_status': r.get('status'), 'final_url': r.get('final_url'),
        'http_last_modified': r.get('last_modified'),
        'last_modified_is_not_publication_date': True,
        'duplicate_group': group or sid, 'count_minimum': count,
        'category': 'B_auxiliary', 'cache_file': 'cache/' + f,
    }

S = [
 source('CB-S01','B01','yarn-notice.html','official migration notice','Yarn / Maël Nison','Yarn 2.0 release',
        'What will happen to the legacy codebase / future plans',
        '옛 웹을 classic으로 옮기고 next를 주 도메인으로 옮길 계획; 대부분 2020-02-01까지 완료될 것으로 예상한다.',
        '계획일이 실제 시행일은 아니다. 루트가 봉인한 B-U01과 같은 원문이라 중복 산입하지 않는다.',
        '2020-01-24','article date; day precision; timezone unspecified',group='B-U01'),
 source('CB-S02','B04','google-notice.html','official migration notice','Google / Lizzi Sassman','Search Central consolidation',
        'Centralizing help information to one site',
        'Search Console 사용법은 Help Center에 남고 crawling/indexing/Search 지침은 며칠에 걸쳐 새 사이트로 이동한다고 구분한다.',
        '개별 article75712 이동 시행일이나 모든 옛 URL의 실패를 증명하지 않는다. B-U04와 중복.',
        '2020-11-11','article date; day precision; timezone unspecified',group='B-U04'),
 source('CB-S03','B06','hashicorp-notice.html','official migration notice','HashiCorp / Geoffrey Grosenbach','Developer public beta',
        'opening; mirror paragraph; Introducing; Try Our New Developer Experience',
        '2022-06-21 Vault와 Waypoint 자료의 새 통합 사이트 mirror를 공개 beta로 제공한다고 명시한다.',
        'old learn 도메인 중단이나 redirect 시행을 말하지 않는다. B-U06와 중복.',
        '2022-06-21','public beta announcement day; timezone unspecified',group='B-U06'),
 source('CB-S04','B01','rails6021.html','official versioned published HTML','Ruby on Rails','6.0.2.1',
        'Getting Started §3.2, package.json row',
        'package.json의 npm 의존성을 설명하면서 Yarn 일반 정보로 https://yarnpkg.com/lang/en/을 실제 href로 제공한다.',
        '버전 경로와 현재 바이트는 확인했다. 원 HTML 최초 공개일과 고정 archive/build receipt는 미확인. HTTP Last-Modified 2019-12-18을 출판일로 계산하지 않는다.',count=True),
 source('CB-S05','B01','rails603.html','official versioned published HTML','Ruby on Rails','6.0.3',
        'Getting Started §3.1.3 and §3.2 package.json row',
        '같은 package.json 설명의 옛 href는 유지한다. 별도 설치 문단은 classic.yarnpkg.com/en/docs/install로 가며 Yarn1.22.0 출력을 예시로 든다.',
        '설치 링크 추가를 package.json 배경 링크의 정정으로 합칠 수 없다. 전체 중간판 내용 및 HTML 최초 공개일은 미확인.',count=True),
 source('CB-S06','B01','rails60.html','current branch documentation HTML','Ruby on Rails','6.0 branch',
        'Installing Node.js and Yarn; package.json row',
        '현재 6.0 branch 문서도 설치 classic과 배경 old URI가 함께 남는다.',
        '변경 가능한 branch 페이지이며 앞선 6.0.3과 선택 문단이 같아 별도 최소수 미산입.',group='CB-S05'),
 source('CB-S07','B04','django30.zip','official offline HTML archive','Django','3.0',
        'ref/contrib/sitemaps.html, Pinging Google and all external hrefs',
        '실제 ZIP 멤버를 확인했다. google.com/webmasters/tools 및 News publisher 링크가 있으나 봉인 old support.google.com/webmasters URI는 없다.',
        '선택 사건의 소비자로 부적격. 검색 결과가 sitemap을 언급했다는 이유로 옛/새 문서 정정 사례로 삼지 않는다.',member='ref/contrib/sitemaps.html'),
 source('CB-S08','B06','vaultr110.tar.gz','CRAN built HTML vignette','vaultr authors / CRAN','1.1.0',
        'vaultr/inst/doc/vaultr.html, authentication and KV sections; DESCRIPTION',
        '실제 빌드 HTML에는 vaultproject.io의 KV/auth 주소가 있다. learn.hashicorp.com과 developer.hashicorp.com href는 없다.',
        'B06 봉인 URI와 다른 문서 계열이므로 이 사건의 교체/미교체 분자에 넣지 않는다.',
        '2021-06-09T14:00:02Z','DESCRIPTION Date/Publication, not Packaged',member='vaultr/inst/doc/vaultr.html'),
 source('CB-S09','B06','vaultr111.tar.gz','CRAN built HTML vignette','vaultr authors / CRAN','1.1.1',
        'vaultr/inst/doc/vaultr.html, authentication and KV sections; DESCRIPTION',
        '다음 실제 배포 HTML도 vaultproject.io 주소를 유지하며 봉인 learn/developer href는 없다.',
        '소비자 후보 제외. vaultproject.io가 같은 회사라는 것만으로 봉인 사건과 동일 노출이라고 간주하지 않는다.',
        '2022-08-22T11:30:02Z','DESCRIPTION Date/Publication, not Packaged',member='vaultr/inst/doc/vaultr.html',group='CB-S08'),
 source('CB-S10','B04','sphinxsitemap-advanced.html','current consumer HTML','Sphinx Sitemap / Jared Dillard','latest',
        'Advanced Configuration, Version Support and Language Support',
        '여러 판/언어별 sitemap 위치를 sitemapindex에 모으라는 문맥에서 Google answer75712를 실제 href로 사용한다.',
        '현재 웹만 확인했고 과거 HTMLzip는404다. 현재 Last updated 표시는 최초출판/당시바이트 증명이 아니다.'),
 source('CB-S11','B06','starlingx60-vault.html','official archived-version HTML','StarlingX','stx.6.0',
        'Vault Aware, introductory paragraphs and See also/Vault REST API',
        '애플리케이션이 Vault REST API로 secrets를 읽고 쓸 때 참고하도록 learn.hashicorp.com/vault/getting-started/apis를 제공한다.',
        '명시된 버전 웹 HTML을 직접 읽었으나 해당 바이트의 2022년 최초 출판이나 불변 archive receipt는 미확인. 2026 HTTP수정일을 과거 출판일로 사용하지 않는다.',count=True),
 source('CB-S12','B06','starlingx70-vault.html','official archived-version HTML','StarlingX','stx.7.0',
        'Vault Aware, introductory paragraphs and See also/Vault REST API',
        '6.0과 같은 목적·같은 old learn href를 유지한다.',
        '같은 본문으로 묶는다. 버전명만으로 이 링크가 언제 처음 공개됐는지 결론내리지 않는다.',group='CB-S11'),
 source('CB-S13','B06','starlingx-vault.html','current consumer HTML','StarlingX','latest observed',
        'Vault Aware, See also/Vault REST API',
        '현재판에도 같은 old learn href가 있다.',
        '같은 원고의 현재 경로이므로 중복 산입하지 않는다. 실제 클릭·API 실행 결과는 미확인.',group='CB-S11'),
 source('CB-S14','B04','sphinxsitemap210.tar.gz','PyPI source-distributed documentation','Sphinx Sitemap / Jared Dillard','2.1.0',
        'README.rst, sitemapindex reference definition and version/language guidance',
        '출판 source README에 Google answer75712 주소가 있으며 HTML 멤버는0개다.',
        'RST source distribution은 실제 렌더링 HTML 노출의 증명이 아니다. 동일 안내의 PKG-INFO 복제는 중복이다.',
        '2020-02-23T01:19:10.837816Z','PyPI upload_time_iso_8601; source release',member='sphinx-sitemap-2.1.0/README.rst'),
 source('CB-S15','B04','sphinxsitemap220.tar.gz','PyPI source-distributed documentation','Sphinx Sitemap / Jared Dillard','2.2.0',
        'README.rst, sitemapindex reference definition and version/language guidance',
        '공지 전 마지막 listed sdist의 README도 같은 Google old 주소다. HTML멤버0개.',
        '완전한 PyPI원장에서 공지 전 마지막 sdist를 식별했지만 HTML출판 원장과 동일시하지 않는다.',
        '2020-08-06T02:13:55.526488Z','PyPI upload_time_iso_8601; source release',member='sphinx-sitemap-2.2.0/README.rst',group='CB-S14'),
 source('CB-S16','B04','sphinxsitemap-post.tar.gz','PyPI source-distributed documentation','Sphinx Sitemap / Jared Dillard','2.2.1',
        'README.rst, Versioning Configuration / Multilingual Configuration / sitemapindex definition',
        '공지 후 처음 listed sdist(2022-11-12)도 old 주소를 유지한다. HTML멤버0개이며 2.2.0과2.2.1 사이 추가sdist는 원장상0개다.',
        'source배포에서 유지된 관측이며, HTML정정·독자실패·최초HTML출판의 관측은 아니다.',
        '2022-11-12T03:41:08.913002Z','PyPI upload_time_iso_8601; source release',member='sphinx-sitemap-2.2.1/README.rst',group='CB-S14'),
 source('CB-S17','B01','yarn-old.html','current official destination via old URL','Yarn','Classic homepage',
        'top version banner; dependency management explanation',
        '실제 shell GET에서 old /lang/en/이301로 classic/en/에 도착하고 최종200; 본문은Yarn1을 명시하고 의존성 관리를 설명한다.',
        '현재 한 관측이다. 2020의 redirect 시작 시각·과거 연속 접근·설치 성공은 미확인.',count=True),
 source('CB-S18','B01','yarn-classic.html','current official destination','Yarn','Classic installation',
        'version banner; Installation; Install via npm',
        '이 페이지가Yarn2 이전 판용임을 명시하고 yarn@1 설치를 안내한다.',
        '실제 설치를 실행하지 않았다. 현재 문자열을 2020의 원문으로 소급하지 않는다.',count=True),
 source('CB-S19','B06','vault-apis.html','current official destination via old URL','HashiCorp','Learn to use Vault HTTP API',
        'opening; Prerequisites; Headers and paths; auth method',
        'old URI에서3회의308을 거쳐 최종공식HTTP API tutorial에200도착. 현재본문이 API·토큰헤더·HTTP methods 설명을 포함한다.',
        '현재 튜토리얼의 예제 버전/개선 내용을2022판에 소급하지 않는다. StarlingX환경에서 실행 검증은 하지 않았다.',count=True),
 source('CB-S20','B04','google-sitemapindex.html','current official destination','Google Search Central','large-sitemaps',
        'Manage your sitemaps with a sitemap index file; Example sitemap index; reference table',
        '현재 공식 새URI에서200, 여러 sitemap을 index에 모으는 목적과XML tag설명이 존재한다.',
        'old URL의shellGET은429였다. 도구가보여준redirect와 별도로 새공개URI를 읽었으므로 old→final200실측이라고 합치지 않는다. 현재수정일2025-12-10은2020이관일아님.',count=True),
 source('CB-S21','B06','vaultr-index.html','public release ledger','CRAN','Archive/vaultr',
        'complete listed tar.gz filenames and date columns',
        '1.0.2/1.1.0/1.1.1의 보존 목록을 확인했다.',
        '목록날짜를DESCRIPTION출판시각보다 우선하지 않는다.'),
 source('CB-S22','B01','packer-index.html','public release ledger','CRAN','Archive/packer',
        'listed tar.gz entries',
        '가장 이른 listed 0.0.6을 실제 다운로드해 도움말HTML 유무를 확인했다.',
        '그 배포물의HTML은템플릿뿐이므로원문수미산입.'),
 source('CB-S23','B01','rhino-index.html','public release ledger','CRAN','Archive/rhino',
        '0.6.4 and1.0.0 entries and subsequent versions',
        '첫 두 listed 배포를 실제 열었다. 0.6.4는 vignetteHTML 두 개에Yarn href가없고1.0.0은HTML이없다.',
        '관련도구라는이름만으로배포도움말에링크가있다고간주하지않음.'),
 source('CB-S24','B04','sphinxsitemap-pypi.json','public release ledger','PyPI / Sphinx Sitemap','release JSON',
        'releases2.0.0–2.6.0, upload_time_iso_8601 and sdists',
        '2020–2024원장에서2020-08-06 다음sdist가2022-11-12임을확인했다.',
        '이JSON과개별version JSON은같은원장의표현이다.렌더링문서출판원장은아님.'),
 source('CB-S25','B06','starlingx-archive.html','official archive locator','StarlingX','Documentation Archive',
        'Archived Release Documentation; raw hrefs',
        '화면의Release6/7/8/9 링크가모두같은stx.6.0 URI를가리키는것을원HTML에서확인했다.',
        '레이블만보고서로다른배포물을확인했다고세지않았다.7.0실제URL은별도GET으로열었다.'),
]
(P/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in S))

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.cur=None; self.out=[]
    def handle_starttag(self,t,a):
        if t=='a': self.cur={'raw_tag':self.get_starttag_text(),'raw_href':dict(a).get('href'),'link_text':''}
    def handle_data(self,d):
        if self.cur: self.cur['link_text']+=d
    def handle_endtag(self,t):
        if t=='a' and self.cur: self.out.append(self.cur); self.cur=None

refs=[]
for event,f,sid,key,purpose in [
 ('B01','rails6021.html','CB-S04','yarnpkg.com','package.json과Yarn의역할을배경으로읽음'),
 ('B01','rails603.html','CB-S05','yarnpkg.com','배경 링크와 별도 Yarn1 설치 링크를 용도별로 구분'),
 ('B04','sphinxsitemap-advanced.html','CB-S10','support.google.com/webmasters','여러판/언어별sitemap을하나의index에모으는방법'),
 ('B06','starlingx60-vault.html','CB-S11','learn.hashicorp.com','Vault API를이용해secrets를읽고쓸때기본API설명참고'),
 ('B06','starlingx70-vault.html','CB-S12','learn.hashicorp.com','Vault API를이용해secrets를읽고쓸때기본API설명참고'),
]:
    b=body(f); parser=Links(); parser.feed(b.decode('utf-8','replace'))
    for a in parser.out:
        if key in (a['raw_href'] or ''):
            a.update(reference_id=event,source_id=sid,base_url=known[f]['url'],raw_href_byte_offset=b.find(a['raw_href'].encode()),context_paraphrase=purpose)
            refs.append(a)
(P/'references.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in refs))

queries={
 'B01': [('system2','Rails Symfony documentation "classic.yarnpkg.com" "yarnpkg.com"','직접소비자배포물근거부족;SymfonyCasts는snippet만'),('system1','site:guides.rubyonrails.org "yarnpkg.com" "6.0"','검색이정확공식결과를주지않아공식version URI직접열람'),('system1','"yarnpkg.com" "packer" "R" package','직접소비자배포물근거없음;CRAN공식원장에서후보파일형식확인')],
 'B04': [('system2','Django documentation "support.google.com/webmasters" sitemap','Googleforum중심잡음;소비자HTML증거없음'),('system1','site:docs.djangoproject.com "support.google.com/webmasters" "sitemaps"','Django3.0/4.0/4.2문서후보발견;실제3.0zip는봉인URI없음'),('system1','"support.google.com/webmasters/answer" "sphinx" sitemap','정확소비자결과부족;SphinxSitemap공식문서직접열람')],
 'B06': [('system2','vaultr "learn.hashicorp.com"','직접소비자근거없음'),('system1','"vaultr" "learn.hashicorp.com"','질문게시판혼합결과;CRAN배포물직접확인'),('system1','"learn.hashicorp.com" "hvac" documentation','StarlingX Vault Aware공식문서발견;hvac과거zip는learn href없음')]
}
candidates={
 'B01': [('Rails Getting Started','versioned web HTML, old background href retained; new installation link is a different purpose'),('packer CRAN vignette candidate','0.0.6 has templates only, no built manual HTML'),('rhino CRAN vignette candidate','0.6.4 built HTML lacks Yarn href;1.0.0 has no HTML'),('JupyterLab installation manual','1.2.6/1.2.x/2.0.x HTMLzip requests404; no original counted')],
 'B04': [('Django sitemap manual','3.0 offline HTML lacks sealed old/new URI'),('Sphinx Sitemap manual','current HTML old href;2.1.0/2.2.0/2.2.1 RST source retained old URI;historicalHTMLzip404')],
 'B06': [('vaultr vignette','1.1.0/1.1.1 built HTML uses different vaultproject URI family; excluded'),('StarlingX Vault Aware','6.0/7.0/current versioned HTML retain old href;historicalpublicationdates unconfirmed'),('hvac manual','v0.11.2 HTMLzip has89members;fullhrefscan nolearn/developer URI;excluded')],
}
attempts=[]
for event,qs in queries.items():
    for n,(engine,q,result) in enumerate(qs,1):
        attempts.append({'attempt_id':f'{event}-Q{n}','reference_id':event,'kind':'consumer_search_query','engine':engine,'query':q,'result':result,'count_minimum':False,'recorded_utc':NOW,'time_note':'각검색초는미기록;고정입력봉인후,첫다운로드들전후의순서로실행.이필드는사후원장기록UTC.'})
for event,cs in candidates.items():
    for n,(name,result) in enumerate(cs,1):
        attempts.append({'attempt_id':f'{event}-C{n}','reference_id':event,'kind':'candidate_publication_family','name':name,'result':result,'count_minimum':False,'recorded_utc':NOW})
for n,r in enumerate(receipts,1):
    attempts.append({'attempt_id':f'CB-GET{n:02}','kind':'public_GET','count_minimum':False,**r})
attempts += [
 {'attempt_id':'CB-WEB-75712','kind':'web_direct_open_failure','url':'https://support.google.com/webmasters/answer/75712?hl=en','result':'search service observed redirect to developers.google.com/search/docs/advanced/sitemaps/large-sitemaps then nonretryable retrieval error; shell separately429. Direct canonicalpage200 is a different GET.','recorded_utc':NOW,'count_minimum':False},
 {'attempt_id':'CB-CONTAMINATION','kind':'masked_review_prior_exposure','rid':'A-D04','result':'L1/L2봉인후 root허용 b-sealed.jsonl전체를읽는중B05의IETF전환요약·A-D04중복가능성에노출.즉시root에보고.다른A상류결말은읽지않음.','recorded_utc':NOW,'count_minimum':False},
]
(P/'attempts.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in attempts))

cases=[
 {'reference_id':'B01','sample':'B','event_key':'yarn-classic-docs-2020','announcement_source':'CB-S01','announcement_date':'2020-01-24','event_implementation_date':None,'implementation_unknown_reason':'공지의Feb1은예상완료일','consumer':'Ruby on Rails Getting Started','before_observation':'CB-S04 Rails6.0.2.1 package.json row','after_observation':'CB-S05 Rails6.0.3 same row','old_href':'https://yarnpkg.com/lang/en/','later_href':'https://yarnpkg.com/lang/en/','replacement_in_same_purpose':False,'separate_new_link':'classic.yarnpkg.com/en/docs/install은별도설치용문단의추가','consumer_publication_dates':None,'artifact_form':'official versioned web HTML; separate downloadable immutable archive not obtained','current_destination':'https://classic.yarnpkg.com/en/','current_http':'301→200 measured2026-11-22','current_section_presence':'Yarn1 banner anddependency-management introduction present','purpose_judgment':'유지 — 관측한 배경 읽기 목적은현재redirect로충족;설치나실행성공판정아님','strict_correction_chain':False,'eligible_latency':False,'right_censored':False,'status':'RETAINED_OLD_HREF_WITH_CURRENT_REDIRECT; HISTORICAL_PUBLICATION_GAP','queries_used':3,'candidate_families':4,'missing_releases_between_observed_HTML':'미확인;firstchange주장없음','A_duplicate':False,'duplicate_reason':'A의consumer-purpose-event조합과일치없음','unconfirmed':['실제2020이관시행일','최초배포HTML일','중간판모두의내용','독자클릭/실패/설치'],'last_checked':'CB-S04/05/17/18','next_material':'Rails6.0.x전체HTML배포원장또는날짜있는build artifact영수증1개'},
 {'reference_id':'B04','sample':'B','event_key':'google-help-consolidation-2020','announcement_source':'CB-S02','announcement_date':'2020-11-11','event_implementation_date':None,'implementation_unknown_reason':'overnextfewdays는계획이며article75712시행일은없음','consumer':'Sphinx Sitemap','before_observation':'CB-S15 PyPI2.2.0 sourceREADME','after_observation':'CB-S16 PyPI2.2.1 sourceREADME; CB-S10 currentHTML','old_href':'https://support.google.com/webmasters/answer/75712?hl=en','later_href':'https://support.google.com/webmasters/answer/75712?hl=en','replacement_in_same_purpose':False,'consumer_publication_dates':['2020-08-06T02:13:55.526488Z','2022-11-12T03:41:08.913002Z'],'publication_date_role':'PyPI sourceupload only; notbuiltHTMLpublication','artifact_form':'source tarballs include0HTML; historicHTMLzip404; currentHTMLread','current_destination':'https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps','current_http':'old GET429; webtoolobservedredirect; independentcanonicalGET200','current_section_presence':'sitemapindex purpose, XMLexample andrequiredtags present','purpose_judgment':'보류 — 같은설명으로이어지는새공식본문은읽었지만원경로의최종200및과거배포HTML은미확인','strict_correction_chain':False,'eligible_latency':False,'right_censored':False,'status':'SOURCE_RELEASE_RETAINS_OLD_URI; PUBLISHED_HTML_PAIR_UNCONFIRMED','queries_used':3,'candidate_families':2,'missing_source_releases_between_selected_pair':0,'missing_HTML_releases':'미확인','A_duplicate':False,'duplicate_reason':'A의consumer-purpose-event조합과일치없음','unconfirmed':['원문HTML전후판','개별URI이동시행일','현재원경로최종200','독자실패'],'last_checked':'CB-S10/15/16/20/24','next_material':'SphinxSitemap2.2.0또는2.2.1의날짜있는렌더링HTML artifact1개'},
 {'reference_id':'B06','sample':'B','event_key':'hashicorp-developer-beta-2022','announcement_source':'CB-S03','announcement_date':'2022-06-21','event_implementation_date':'2022-06-21','implementation_role':'Vault/Waypoint publicbeta mirror availabletoday; redirectshutdown clock isunknown','consumer':'StarlingX Vault Aware','before_observation':'CB-S11 stx.6.0 HTML','after_observation':'CB-S12 stx.7.0 HTML;CB-S13currentHTML','old_href':'https://learn.hashicorp.com/vault/getting-started/apis','later_href':'https://learn.hashicorp.com/vault/getting-started/apis','replacement_in_same_purpose':False,'consumer_publication_dates':None,'artifact_form':'officialarchived-versionwebHTML;historicalbuildtimeunconfirmed','current_destination':'https://developer.hashicorp.com/vault/tutorials/get-started/learn-http-api','current_http':'308→308→308→200 measured2026-11-22','current_section_presence':'HTTPAPI explanation,headers,authmethod present','purpose_judgment':'유지 — API기초참고목적은현재redirect로충족;StarlingX명령실행및옛Vault판호환은미확인','strict_correction_chain':False,'eligible_latency':False,'right_censored':False,'status':'RETAINED_OLD_HREF_ACROSS_VERSIONED_HTML; PUBLICATION_DATE_GAP','queries_used':3,'candidate_families':3,'missing_releases_between_observed_HTML':'완전원장미확인;firstchange주장없음','A_duplicate':False,'duplicate_reason':'A의consumer-purpose-event조합과일치없음','unconfirmed':['정확한옛→새redirect시행일','6.0/7.0해당HTML최초출판일','전체소스수정·build영수증','독자클릭/실패/실행'],'last_checked':'CB-S03/11/12/19','next_material':'StarlingX6.0/7.0 VaultAwareHTML의날짜있는build·출판영수증1개'},
]
(P/'cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')

with (P/'editions.csv').open('w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=['source_id','reference_id','version','url','member','publication_date','publication_date_role','observed_utc','sha256','status','count_minimum'])
    w.writeheader()
    for s in S:
        w.writerow({'source_id':s['source_id'],'reference_id':s['reference_ids'][0],'version':s['version'],'url':s['original_url'],'member':s['member'],'publication_date':s['publication_date'],'publication_date_role':s['publication_date_role'],'observed_utc':s['observed_utc'],'sha256':s['artifact_sha256'],'status':s['http_status'],'count_minimum':s['count_minimum']})
summary={'completed_utc':NOW,'seal_commit':'ffbce62e4c01459ebbfb006a5d6c67e425ed7c17','events':3,'queries':9,'queries_per_event':{'B01':3,'B04':3,'B06':3},'candidate_families_per_event':{'B01':4,'B04':2,'B06':3},'strict_correction_chains':0,'eligible_latency_pairs':0,'right_censored_cases':0,'sources_rows':len(S),'counted_unique_originals':sum(s['count_minimum'] for s in S),'counted_originals_cannot_replace_A12':True,'public_GET_attempts':len(receipts),'additional_A_outcome_read':'A-D04 B05sealedsummary contamination only; L1/L2alreadysealed','same_worker_recheck':True,'external_independent_review':False,'json_parse_and_limits_check':'performed by build and subsequent QA; no installs/API commands executed'}
(P/'QA.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False))
