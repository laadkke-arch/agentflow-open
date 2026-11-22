"""Assemble auditable ledgers from the already-read and hashed public material.

This does not execute either consumer product and does not change sealed A inputs.
Run from this directory, or by absolute path; all writes remain in followup/.
"""
from pathlib import Path
from html.parser import HTMLParser
import csv, datetime as dt, hashlib, json, re

P = Path(__file__).resolve().parent
BASE = P.parent
def readjl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line]
def writejl(name, rows):
    (P/name).write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in rows))
def writecsv(name, rows):
    with (P/name).open('w', newline='') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
refs={r['reference_id']:r for r in readjl(BASE/'references.jsonl')}
attempts=readjl(P/'attempts.jsonl')
bykey={r['key']:r for r in attempts if r.get('key')}
pg=readjl(P/'pg-editions.jsonl'); sq=readjl(P/'sqlite-editions.jsonl')
pgby={r['version']:r for r in pg}; sqby={r['version']:r for r in sq}
sources=[]

def webpage(sid, key, publisher, title, date, location, findings, limits, rids,
            group, count=True, category='upstream', version='current observation', cache=None):
    r=attempts[key] if isinstance(key,int) else bykey[key]
    assert r.get('http_status') == 200, (sid,r)
    sources.append(dict(source_id=sid, source_type='public_original_page', publisher=publisher,
        title=title, original_url=r['url'], final_url=r.get('final_url'), version=version,
        publication_date=date, publication_date_role='stated publication/revision date; not an execution date',
        observed_at_utc=r['observed_at_utc'], read_location=location, findings=findings,
        limits=limits, questions=['Q3','Q6','Q7'], reference_ids=rids,
        duplicate_group=group, count_minimum=count, count_category=category,
        body_sha256=r.get('sha256'), cache_path=cache or ('cache/'+str(key)),
        archive_body_committed=False))

webpage('PG-U01',0,'Wikipedia contributors / Wikimedia','American National Standards Institute',
 '미확인 (current revision oldid 1383360789)','article lead and institution identity',
 '현재 본문은 ANSI가 가리킨 기관을 설명한다. 목적지 객체를 확인한 것이며 기술적 권위로 사용하지 않는다.',
 '2020 본문 미확인: revision metadata 938900783/2020-02-03T02:17:46Z는 확보했으나 oldid HTML와 content API는 403. 현재 본문으로 과거 연속 유지·동일 문장·당사자 클릭을 입증할 수 없다.',
 ['A-D03'],'wikipedia-ANSI',cache='cache/current0.html')
webpage('PG-U02',1,'RFC Editor / IETF; Yakov Shafranovich','RFC 4180',
 '2005-10','Section 2, numbered quoting rules 5–7; current arrival includes full RFC body',
 '원 tools URL의 현재 최종 응답은 200이고 RFC-Editor info 주소에 CSV 문법 본문이 있다. 메타데이터만 있는 착지라고 볼 수 없다.',
 '원 요청의 중간 HTTP 상태 코드는 수집하지 않았고 마지막 200만 기록했다. 현재 redirect 경로를 과거 모든 시점에 소급할 수 없다. 실제 독자 실패·원 RFC 링크별 전환 시행일은 미확인.',
 ['A-D04'],'RFC4180-original-text',cache='cache/current1.html')
webpage('PG-U03','ietf-initial','IETF tools team','Transition from tools.ietf.org',
 '2021-10-18T16:32:44Z','README New service locations table and preceding redirect paragraph',
 '고정 commit의 표에 htmlized RFC의 tools 주소와 RFC-Editor HTML 주소가 대응한다. draft의 datatracker 경로와 RFC 경로를 구별한다.',
 '전체 서비스 전환 설명이며 RFC4180 개별 경로의 실제 시행 시각·독자 상태를 확정하지 않는다. 2021년 최초 공지 링크는 접근 실패.',
 ['A-D04'],'ietf-tools-transition-plan',version='9cc29af66b4f7548f05126d08a9fd00d55b08360')
webpage('PG-U03b','ietf-june','IETF tools team','Transition from tools.ietf.org',
 '2022-06-16T15:47:52Z','README New service locations and Work remaining',
 '2022년 고정판도 RFC와 draft 경로를 분리하고 남은 전환 작업을 열거한다.',
 '같은 문서의 버전이므로 최소 원문수에 중복 산입하지 않는다. RFC4180 개별 시행일 미확인.',
 ['A-D04'],'ietf-tools-transition-plan',count=False,version='863f121821da7d5600c99cc62ac9a196cf31245c')
webpage('PG-U03c','ietf-complete','IETF tools team','Transition from tools.ietf.org',
 '2022-09-09T18:30:19Z','README opening completion statement and RFC service row',
 '전환 완료라는 문구가 2022-09-09 고정 commit에 존재한다. 이 문구의 도입 시각과 특정 URL 시행 시각은 별개다.',
 '같은 원고의 후속 버전. 완료 문구만으로 개별 redirect 시행일을 산술하지 않는다.',
 ['A-D04'],'ietf-tools-transition-plan',count=False,version='1975a5025ceb448dce3ef23fe9a380cfc54be0dc')
webpage('PG-U04','ietf-blog','IETF; Robert Sparks','Finalizing the IETF tools transition',
 '2022-06-17; later update explicitly 2026-10-29','dated article lead and final update note',
 '2022 공지는 이후 수 주에 걸친 최종 전환 계획이다. RFC-Editor canonical 설명에는 2026-10-29 수정 표시가 있어 과거 공지 내용과 분리한다.',
 '공지일은 RFC4180 시행일이 아니다. 후대 추가 문장을 2022 당시 상태로 소급할 수 없다.',
 ['A-D04'],'ietf-transition-blog')
webpage('PG-U05','rfc7111-txt','RFC Editor / IETF; Michael Hausenblas et al.','RFC 7111',
 '2014-01','Abstract, Introduction, Section 1.1 and fragment definitions',
 'RFC4180을 updates하지만 주제는 text/csv의 행·열·셀 fragment 식별이다. CSV quoting을 읽으려는 문서에서 단순히 새 번호로 바꾸면 역할이 달라진다.',
 '2014 문서로 A 출판 이전 자료이며 후발 정정 사건이 아니다. psql 실행이나 독자 실패는 증명하지 않는다.',
 ['A-D04'],'RFC7111-original-text')
webpage('PG-U06','rfc4180-errata','RFC Editor / IETF','RFC4180 errata records',
 'individual record dates 2018–2025','records 5593, 5714, 5345, 6230, 7572; their status dates',
 '5593은 2019 보고/2024 검증, 5714는 2019 검증, 5345·6230은 2025 held 상태다. 원 RFC와 정정 상태의 날짜를 따로 남겨야 한다.',
 '현재 errata collection이다. 2025 상태를 2020·2024 독자 판단에 넣지 않았다. 이 표본이 해당 오류를 겪었다는 기록은 없다.',
 ['A-D04'],'RFC4180-errata-collection')
webpage('SQL-U01',2,'Wikipedia contributors / Wikimedia','Endianness',
 '미확인 (current revision oldid 1386817945)','article lead defining endianness and big/little endian',
 'raw HTTP 목적지는 현재 HTTPS 본문으로 도달하고 big/little endian 개념을 설명한다. 소비자가 선택한 페이지의 내용만 관측했다.',
 '2020 역사 본문 미확인: metadata는 936140889/2020-01-16T22:54:52Z이나 oldid/content 요청은 403. 기술 권위·과거 연속성 근거로 사용하지 않는다.',
 ['A-D05'],'wikipedia-Endianness',cache='cache/current2.html')
webpage('SQL-U02',3,'Ian Darwin','Fine Free File Command (and libmagic)',
 '미확인; displayed 1987-08-23 describes origin, not this page publication','opening home-page statement and What? file type guesser paragraph',
 '원 HTTP 주소는 현재 HTTPS의 file(1) 프로젝트 설명으로 도달하며 파일 내용을 보고 유형을 식별하는 도구라는 최소 목적을 충족한다.',
 'SQLite application_id를 지원한 정확한 file 버전·과거 화면·변경일은 미확인. 표시된 1987 날짜를 현재 페이지 또는 HTTPS 시행일로 쓰지 않는다.',
 ['A-D06'],'darwinsys-file-home',cache='cache/current3.html')
webpage('PG-U02b','rfc4180-txt','RFC Editor / IETF; Yakov Shafranovich','RFC4180 text representation',
 '2005-10','Section 2 quoting rules',
 '현재 도착한 RFC와 동일한 원 RFC 텍스트를 대조했다.',
 'HTML과 같은 원고라 최소수 제외.', ['A-D04'],'RFC4180-original-text',count=False)
webpage('PG-F-SOURCE-MAIL','pg-discussion','PostgreSQL pgsql-docs; Daniel Gustafsson',
 'tools.ietf.org is decommissioned and our links are redirected','2024-04-03 11:18:22; timezone not displayed',
 'message body and attached patch description','편집자의 변경 이유는 redirect로 인한 추가 network roundtrip 제거다. 본문 실패를 이유로 들지 않는다.',
 '패치 제안이며 빌드/출판 자체가 아니다. 작성자가 실제 링크 상태를 보고했지만 같은 목적의 독자 실패 보고는 아니다. 최소수는 보수적으로 제외.',
 ['A-D04'],'postgres-rfc-link-discussion',count=False,category='consumer_followup')
webpage('PG-F-NEWS1219','pg-release-news','PostgreSQL Global Development Group',
 'PostgreSQL 16.3, 15.7, 14.12, 13.15, and 12.19 Released!','2024-05-09',
 'Posted on date; opening released-version statement; update instructions',
 '공식 발행자가 12.19를 포함한 버전의 공개 릴리스를 알린 독립 출판 영수증이다.',
 '페이지 meta 2024-05-09T00:00:00에는 timezone이 없다. archive HTML 최초 공개 시각이나 독자 열람 시각은 아니다.',
 ['A-D03','A-D04'],'postgres-2024-05-09-release-announcement',category='consumer_followup')
webpage('PG-F-NEWS1219-MAIL','pg-release-mail','PostgreSQL Global Development Group',
 'Release announcement on pgsql-announce','2024-05-09 13:09:17; timezone unspecified',
 'Date, message ID, opening released-version list',
 '동일 공식 공지의 메일 발행 표시를 확인했다. raw GET는 일반 HTML로 돌아와 offset 있는 Date header를 확보하지 못했다.',
 'news와 같은 원고라 중복 제외. UTC 정밀도로 가장하지 않는다.',
 ['A-D03','A-D04'],'postgres-2024-05-09-release-announcement',count=False,category='consumer_followup')

edit=json.loads((P/'excerpts/pg-source-edit-current.json').read_text())
sources.append(dict(source_id='PG-F-SOURCE12',source_type='official_repository_commit',
 publisher='PostgreSQL; Daniel Gustafsson',original_url=edit['html_url'],version=edit['sha'],
 publication_date=edit['committed_utc'],publication_date_role='consumer source edit/commit; not public HTML publication',
 observed_at_utc=dt.datetime.strptime(edit['observed_end_utc'],'%Y-%m-%d %H:%M:%S UTC').isoformat()+'Z',read_location='doc/src/sgml/ref/psql-ref.sgml hunk near line 2710',
 findings='12 branch commit changes the exact RFC4180 href from tools to datatracker without changing its CSV quoting purpose.',
 limits='Source and commit receipt only; separate merge/build times unknown. Publication is established separately by archive HTML plus release notice.',
 questions=['Q4','Q6'],reference_ids=['A-D04'],duplicate_group='postgres-bfed705-source-edit',
 count_minimum=False,count_category='consumer_followup',body_sha256=sha(P/'excerpts/pg-source-edit-current.json'),
 local_copy='excerpts/pg-source-edit-current.json'))

for r in pg:
    minor=r['version'].split('.')[1]
    for m in r['members']:
        ispsql=m['member_path'].endswith('app-psql.html')
        rid='A-D04' if ispsql else 'A-D03'
        sid=f'PG-F{minor}-'+('PSQL' if ispsql else 'ACRONYMS')
        changed=ispsql and r['version']=='12.19'
        group=('postgresql12-psql-datatracker' if ispsql and int(minor)>=19 else
               'PostgreSQL-12.2-app-psql.html' if ispsql else 'PostgreSQL-12.2-acronyms.html')
        sources.append(dict(source_id=sid,source_type='distributed_html_member',publisher='PostgreSQL Global Development Group',
          original_url=r['archive_url'],version=r['version'],publication_date=r['release_date'],
          publication_date_role=r['release_date_role'],observed_at_utc=r['observed_at_utc'],
          read_location={'member':m['member_path'],'lines':m['read_lines']},
          findings={'href':m['target_href'],'same_purpose':True,'changed_from_baseline':ispsql and int(minor)>=19},
          limits='Package release day, exact first HTML upload time unknown. Same-topic unchanged versions are duplicate-counted false; no reader execution inferred.',
          questions=['Q3','Q4','Q6'],reference_ids=[rid],duplicate_group=group,count_minimum=changed,
          count_category='consumer_followup',archive_sha256=r['archive_sha256'],member_sha256=m['member_sha256'],
          relevant_bytes_sha256=m['relevant_bytes_sha256'],local_copy=m['relevant_copy']))
    sources.append(dict(source_id=f'PG-F{minor}-RELEASE',source_type='distributed_release_note',publisher='PostgreSQL Global Development Group',
       original_url=r['archive_url'],version=r['version'],publication_date=r['release_date'],publication_date_role=r['release_date_role'],
       observed_at_utc=r['observed_at_utc'],read_location=r['release_member']+' heading and Release date',
       findings='Official release day read inside actual archive.',limits='Date-only; no build or reader clock. Not counted toward minimum to avoid multiplying release-date lookups.',
       questions=['Q4','Q6'],reference_ids=['A-D03','A-D04'],duplicate_group='postgres-release-'+r['version'],
       count_minimum=False,count_category='consumer_followup',archive_sha256=r['archive_sha256'],member_sha256=r['release_member_sha256']))

for r in sq:
    code=r['version'].replace('.','_')
    for m in r['members']:
        about=m['member_path'].endswith('/about.html'); rid='A-D05' if about else 'A-D06'
        sources.append(dict(source_id='SQL-F'+code+'-'+('ABOUT' if about else 'AFF'),source_type='distributed_html_member',publisher='SQLite project',
          original_url=r['archive_url'],version=r['version'],publication_date=r['release_date'],publication_date_role=r['release_date_role'],
          observed_at_utc=r['observed_at_utc'],read_location={'member':m['member_path'],'lines':m['read_lines']},
          findings={'href':m['target_href'],'same_purpose':True,'changed_from_baseline':False},
          limits='Only 5 of 51 releases read including baseline. Intermediate change/reversion not ruled out. Same relevant text is not a new minimum-count source.',
          questions=['Q3','Q4','Q6'],reference_ids=[rid],duplicate_group='SQLite-3.31.0-'+('about.html' if about else 'aff_short.html'),
          count_minimum=False,count_category='consumer_followup',archive_sha256=r['archive_sha256'],member_sha256=m['member_sha256'],
          relevant_bytes_sha256=m['relevant_bytes_sha256'],local_copy=m['relevant_copy']))
    sources.append(dict(source_id='SQL-F'+code+'-RELEASE',source_type='distributed_release_note',publisher='SQLite project',
       original_url=r['archive_url'],version=r['version'],publication_date=r['release_date'],publication_date_role=r['release_date_role'],
       observed_at_utc=r['observed_at_utc'],read_location=r['release_member']+' heading, changes and release identifiers',
       findings='Actual 2024-12-07 offline archive includes the official SQLite 3.47.2 release note.' if r['version']=='3.47.2' else 'Release date from archive note.',
       limits='Independent publication receipt, not a correction or reader observation. Does not prove when the zip first became available.',
       questions=['Q4','Q6'],reference_ids=['A-D05','A-D06'],duplicate_group='sqlite-release-'+r['version'],
       count_minimum=r['version']=='3.47.2',count_category='consumer_followup',archive_sha256=r['archive_sha256'],
       member_sha256=r['release_member_sha256'],local_copy='excerpts/sqlite-'+r['version']+'-release.html'))

webpage('PG-L01',4,'PostgreSQL Global Development Group','Official source archive index','current inventory',
 'v12.0 through v12.22 entries','12-series inventory contains 23 versions; studied baseline 12.2 and every following version through 12.22.',
 'Current inventory does not prove historical upload timestamps. Pre-baseline 12.0 and 12.1 excluded from follow-up denominator.',
 ['A-D03','A-D04'],'postgres-source-index',count=False,category='consumer_followup',cache='cache/current4.html')
webpage('SQL-L01',5,'SQLite project','Release chronology','current inventory',
 'all rows dated 2020-01-01 through 2024-12-31','51 version rows, 5 studied including baseline; 46 intermediate archives not opened.',
 'Listed release does not prove an accessible documentation zip; untested zips are listed as unattempted rather than failed.',
 ['A-D05','A-D06'],'sqlite-release-chronology',count=False,category='consumer_followup',cache='cache/current5.html')
sources.extend(readjl(P/'web-reads.jsonl') if (P/'web-reads.jsonl').exists() else [])
writejl('sources.jsonl',sources)

class Rows(HTMLParser):
    def __init__(self):super().__init__();self.rows=[];self.row=None
    def handle_starttag(self,t,a):
        if t=='tr':self.row=''
    def handle_data(self,d):
        if self.row is not None:self.row+=d
    def handle_endtag(self,t):
        if t=='tr' and self.row is not None:self.rows.append(self.row);self.row=None
parser=Rows();parser.feed((P/'cache/current5.html').read_text())
chron=[]
for row in parser.rows:
    m=re.search(r'(202[0-4]-\d\d-\d\d)\s+(3\.\d+\.\d+)',row)
    if m:chron.append((m[1],m[2]))
chron.sort();assert len(chron)==51
editions=[]
for minor in range(2,23):
    v='12.'+str(minor);r=pgby.get(v);baseline=refs['A-D04']
    editions.append(dict(project='PostgreSQL',version=v,release_date=r['release_date'] if r else baseline['consumer_release_date'],
      ledger_source='PG-L01',archive_url=r['archive_url'] if r else baseline['archive_url'],
      archive_sha256=r['archive_sha256'] if r else baseline['archive_sha256'],archive_read=True,members_read=2,
      status='read',href_result='tools RFC4180' if minor<19 else 'datatracker RFC4180',
      inventory_scope='complete 12.2–12.22 series; no intervening editions missing',date_role='product release date, timezone unspecified'))
for date,v in chron:
    r=sqby.get(v);baseline=v=='3.31.0';b=refs['A-D05'];ver=list(map(int,v.split('.')))
    url=r['archive_url'] if r else b['archive_url'] if baseline else 'https://www.sqlite.org/'+date[:4]+'/sqlite-doc-'+str(ver[0]*1000000+ver[1]*10000+ver[2]*100)+'.zip'
    editions.append(dict(project='SQLite',version=v,release_date=date,ledger_source='SQL-L01',archive_url=url,
      archive_sha256=r['archive_sha256'] if r else b['archive_sha256'] if baseline else '',archive_read=bool(r or baseline),
      members_read=2 if r or baseline else 0,status='read' if r or baseline else 'unattempted; URL derived from documented naming, existence unverified',
      href_result='both original hrefs retained' if r or baseline else '미확인',inventory_scope='51 release entries; 5 archives read; 46 unattempted',
      date_role='product release date, timezone unspecified'))
writecsv('editions.csv',editions)

def current(rid, idx, description):
    r=attempts[idx]
    return dict(observed_at_utc=r['observed_at_utc'],requested_url=refs[rid]['raw_href'],
      request_method='GET, following redirects',final_http_status=r['http_status'],
      initial_and_intermediate_status_codes='미확인; not retained by urllib default redirect handler',final_url=r['final_url'],
      fragment=refs[rid]['fragment'],fragment_presence='해당 없음: sealed raw href has no fragment',
      required_section_exists=True,section_evidence=description,purpose_minimum_satisfied=True,
      historical_continuity='미확인',reader_actual_click='미확인',body_sha256=r['sha256'])
def unknown(why,last,nextone):return {'reason':why,'last_verified':last,'next_minimum_source':nextone}
cases=[]
for rid,idx,section in [('A-D03',0,'ANSI institution lead'),('A-D04',1,'RFC4180 Section2 quoting rules5–7'),
                        ('A-D05',2,'Endianness lead, big/little endian'),('A-D06',3,'file(1) home-page and file type guesser description')]:
    b=refs[rid];ispg=rid in ['A-D03','A-D04'];last=pgby['12.22'] if ispg else sqby['3.47.2']
    case=dict(reference_id=rid,sample='A',seal_commit='168d90b8519bcb4f673acc659bbaae895f79fca5',
      original_archive=b['archive_url'],original_archive_sha256=b['archive_sha256'],original_member=b['member_path'],
      original_member_sha256=b['member_sha256'],raw_href=b['raw_href'],purpose=b['purpose'],
      minimum_success_condition=b['minimum_success_condition'],original_intent_unknown=b['intent_unknown'],
      current=current(rid,idx,section),verdict='유지',verdict_actor='researcher assessing sealed click purpose at observation time',
      actual_consumer_href_changed=(rid=='A-D04'),upstream_event_key='ietf-tools-htmlized-rfc-service-migration' if rid=='A-D04' else None,
      source_edit=None,merge=None,build=None,publication={'last_read_version':last['version'],'release_day':last['release_date'],
         'role':'version release date; first HTML public availability time unknown'},reader_report=None,
      last_old=None,first_observed_new=None,latest_same_purpose_href=last['members'][0 if rid in ['A-D03','A-D05'] else 1]['target_href'],
      editions={'inventory_count':21 if ispg else 51,'actual_archives_read_including_baseline':21 if ispg else 5,
        'html_members_read_per_reference':21 if ispg else 5,'unread_editions':0 if ispg else 46,
        'scope':'PostgreSQL12.2–12.22' if ispg else 'SQLite3.31.0–3.47.2, listed 2020–2024 chronology'},
      strict_upstream_to_publication_interval_eligible=False,right_censored=False,
      reason_no_strict_interval='동일 사건의 실제 상류 시행 시계가 미확인. 시작을 모르는 것을 우측 검열로 세지 않음.',
      next_first_action='Open the specific missing source named under unknowns; do not change sealed sample.')
    if rid=='A-D04':
        old=pgby['12.18'];new=pgby['12.19']
        case['verdict_reason']='RFC4180의 인용 목적은 현재 옛 URL도 충족. 배포자가 주소를 갱신한 사실과 독자 목적상 교체 의무를 구별한다. 현재 경로를 병기하는 선택은 가능.'
        case['source_edit']={'commit':edit['sha'],'timestamp_utc':edit['committed_utc'],'source_id':'PG-F-SOURCE12','path':'doc/src/sgml/ref/psql-ref.sgml','line':2710}
        case['last_old']={'version':'12.18','release_day':old['release_date'],'archive_url':old['archive_url'],'member':old['members'][1], 'archive_sha256':old['archive_sha256'],'source_id':'PG-F18-PSQL'}
        case['first_observed_new']={'version':'12.19','release_day':new['release_date'],'archive_url':new['archive_url'],'member':new['members'][1], 'archive_sha256':new['archive_sha256'],'source_id':'PG-F19-PSQL',
           'first_claim_scope':'first changed offline release in fully read PostgreSQL12.2–12.22 lineage ONLY; not first all-major PostgreSQL edition or first website publication',
           'missing_between_last_old_and_new':0}
        case['publication']['first_changed_version_release_day']='2024-05-09'
        case['publication']['announcement_source_id']='PG-F-NEWS1219'
        case['publication']['announcement_mail_display_time']='2024-05-09 13:09:17; timezone unspecified'
        case['upstream_observations']=[{'date':'2021-10-18T16:32:44Z','role':'fixed mapping document commit','source_id':'PG-U03'},
           {'date':'2022-06-17','role':'planned final transition announcement','source_id':'PG-U04'},
           {'date':'2022-09-09T18:30:19Z','role':'transition plan completion wording commit','source_id':'PG-U03c'},
           {'date':'2024-04-03 11:18:22; timezone unspecified','role':'consumer maintainer observed redirects, not reader failure','source_id':'PG-F-SOURCE-MAIL'},
           {'date':attempts[1]['observed_at_utc'],'role':'current tools URL arrival to RFC-Editor info body','source_id':'PG-U02'}]
        case['source_ids']=['PG-S02','PG-U02','PG-U03','PG-U03b','PG-U03c','PG-U04','PG-U05','PG-U06','PG-F-SOURCE12','PG-F-SOURCE-MAIL','PG-F18-PSQL','PG-F19-PSQL','PG-F-NEWS1219','PG-F-NEWS1219-MAIL','PG-L01']
        case['unknowns']=[unknown('RFC4180 redirect 실제 시행 시각 미확인','PG-U03 RFC service mapping and PG-F-SOURCE-MAIL redirect report','dated IETF deployment/config receipt for /html/rfc4180'),
           unknown('12.19 HTML 최초 공개 UTC와 build 시각 미확인','PG-F19-PSQL bytes plus official 2024-05-09 notice','timestamped publication receipt naming this archive hash'),
           unknown('독자의 실제 열람/실패 미확인','official edit explains avoiding extra roundtrip','same-purpose psql reader report identifying edition and clicked URI')]
        case['counterexamples']=['RFC7111 updates4180 but concerns CSV fragments, so newer RFC alone is an erroneous replacement for quoting purpose.',
           'RFC4180 errata carry separate reporting/verification dates; 2025 status cannot be given to a 2020 reader.',
           'tools redirect still exposes required section; observed address change is not proof of user-visible failure.',
           'datatracker direct urllib GET returned403 while the web retrieval read Section2; neither single-client result generalizes to all readers.']
    else:
        case['verdict_reason']='현재 목표 본문이 봉인된 최소 읽기 목적을 충족한다. 과거 전 기간 유지 또는 특정 실행 성공을 주장하지 않는다.'
        if rid=='A-D03':
            case['source_ids']=['PG-S01','PG-U01','PG-F22-ACRONYMS','PG-L01']
            case['unknowns']=[unknown('2020 Wikipedia 본문 미확인; content API/oldid403','revision938900783 metadata and current article lead','public dated full body of Wikipedia revision938900783'),unknown('실제 독자 열람 미확인','published acronym link','reader citation/click report naming PG12.2 ANSI link')]
        elif rid=='A-D05':
            case['source_ids']=['SQL-S01','SQL-U01','SQL-F3_47_2-ABOUT','SQL-F3_47_2-RELEASE','SQL-L01']
            case['unknowns']=[unknown('2020 Wikipedia 본문 미확인; content API/oldid403','revision936140889 metadata and current lead','public dated full body of Wikipedia revision936140889'),unknown('46개 사이 배포물 내용 미검사','5 checkpoints and 51-entry chronology','2020 sqlite-doc-3310100.zip/about.html as first unread edition')]
        else:
            case['source_ids']=['SQL-S02','SQL-U02','SQL-F3_47_2-AFF','SQL-F3_47_2-RELEASE','SQL-L01']
            case['unknowns']=[unknown('file의 application_id 인식 버전/실행 미확인','current file homepage identifies tool; SQLite context asserts purpose','official versioned file magic definition containing SQLite application_id and corresponding release'),unknown('46개 사이 배포물 내용 미검사','5 checkpoints and 51-entry chronology','2020 sqlite-doc-3310100.zip/aff_short.html as first unread edition'),unknown('HTTP→HTTPS 시행일과 당시 본문 미확인','current GET final HTTPS200','dated official redirect deployment or archived page before/after')]
        case['counterexamples']=['A changed scheme or current page date does not by itself establish changed purpose; current200 does not establish historical continuity.']
    cases.append(case)
(P/'cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')

intervals=[]
for case in cases:
    intervals.append(dict(interval_id=case['reference_id']+'-strict',reference_id=case['reference_id'],event_key=case['upstream_event_key'] or 'no established change event',
        start_role='upstream effective change',start_value='미확인',start_source=';'.join(s for s in case['source_ids'] if '-U' in s),
        end_role='same-purpose consumer published correction',end_value='2024-05-09' if case['reference_id']=='A-D04' else '미확인',
        end_source='PG-F19-PSQL;PG-F-NEWS1219' if case['reference_id']=='A-D04' else '',precision='not established for both clocks',
        eligible=False,delta_days='',right_censored=False,reason=case['reason_no_strict_interval'],next_source=case['unknowns'][0]['next_minimum_source']))
delta=(dt.date(2024,5,9)-dt.date(2024,4,10)).days
assert delta==29
intervals.append(dict(interval_id='A-D04-source-publication-calendar',reference_id='A-D04',event_key='ietf-tools-htmlized-rfc-service-migration',
    start_role='consumer source commit UTC',start_value='2024-04-10T11:53:25Z',start_source='PG-F-SOURCE12',
    end_role='official product release notice calendar day',end_value='2024-05-09',end_source='PG-F19-PSQL;PG-F-NEWS1219',
    precision='source seconds UTC; publication day/timezone unspecified',eligible=False,delta_days=delta,right_censored=False,
    reason='29 is calendar-date subtraction only; exact elapsed UTC source→HTML publication latency ineligible; not upstream→consumer delay.',
    next_source='raw timezone-qualified release notice or timestamped archive publication receipt'))
writecsv('intervals.csv',intervals)
counts={'source_rows':len(sources),'counted_unique_upstream':sum(s['count_minimum'] and s['count_category']=='upstream' for s in sources),
        'counted_unique_consumer_followup':sum(s['count_minimum'] and s['count_category']=='consumer_followup' for s in sources),
        'A_references':4,'observed_consumer_href_changes':1,'strict_interval_eligible':0,'reader_failures_established':0,
        'pg_edition_archives_read':21,'pg_missing_edition_archives':0,'sqlite_edition_archives_read':5,'sqlite_unread_edition_archives':46,
        'calendar_aux_delta_days':29,'independent_human_review':False,'review_kind':'same collector recheck; parent integration separate internal reading'}
(P/'counts.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(counts,ensure_ascii=False))
