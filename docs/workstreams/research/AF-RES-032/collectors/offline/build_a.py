"""Extract the preregistered offline A rows from already-downloaded archives.

No network request and no destination/follow-up inspection is performed here.
"""
from pathlib import Path
import bz2, csv, datetime, hashlib, html.parser, io, json, re, tarfile, zipfile

ROOT = Path(__file__).resolve().parent
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def norm(t): return re.sub(r'\s+', ' ', t).strip()
class Links(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.text=''; self.links=[]; self.active=None; self.skip=0
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag in ('script','style'): self.skip+=1
        if tag=='a' and 'href' in attrs:
            self.active={'href':attrs['href'],'text':'','position':len(self.text),'line':self.getpos()[0]}
    def handle_endtag(self,tag):
        if tag in ('script','style'):self.skip=max(0,self.skip-1)
        if tag=='a' and self.active:self.links.append(self.active);self.active=None
    def handle_data(self,data):
        if self.skip:return
        self.text+=data
        if self.active:self.active['text']+=data

pgbytes=(ROOT/'cache/postgresql-12.2.tar.bz2').read_bytes()
sqlbytes=(ROOT/'cache/probe3.zip').read_bytes()
pg=tarfile.open(fileobj=io.BytesIO(bz2.decompress(pgbytes)),mode='r:')
sq=zipfile.ZipFile(io.BytesIO(sqlbytes))
archives={
 'PostgreSQL':{'version':'12.2','bytes':pgbytes,'archive_url':'https://ftp.postgresql.org/pub/source/v12.2/postgresql-12.2.tar.bz2','format':'official source tar.bz2 including prebuilt offline HTML','names':sorted(m.name for m in pg.getmembers() if m.isfile() and m.name.endswith('.html')),'read':lambda n:pg.extractfile(n).read(),'release_date':'2020-02-13','date_source':'PG-S04','observed_at_utc':'2026-11-22T07:12:13.853971+00:00'},
 'SQLite':{'version':'3.31.0','bytes':sqlbytes,'archive_url':'https://www.sqlite.org/2020/sqlite-doc-3310000.zip','format':'official offline HTML documentation zip','names':sorted(n for n in sq.namelist() if n.endswith('.html')),'read':sq.read,'release_date':'2020-01-22','date_source':'SQL-S04','observed_at_utc':'2026-11-22T07:11:46.187926+00:00'}}

purpose={
 'A-D03':('PostgreSQL','acronyms.html','https://en.wikipedia.org/wiki/American_National_Standards_Institute','ANSI 약어가 가리키는 기관의 배경을 읽는다.','background','American National Standards Institute의 정체와 ANSI 약어를 설명하는 본문에 도착한다.','특정판이나 특정날짜의 기관 설명을 보존하라는 요구는 없다. 현재판 필요성도 명시하지 않았다.','PG-S01'),
 'A-D04':('PostgreSQL','app-psql.html','https://tools.ietf.org/html/rfc4180','psql csv 출력에 쓰이는 인용부호 규칙의 명시된 표준 RFC 4180을 읽는다.','specific_standard','RFC 4180의 CSV 필드 분리·인용·이스케이프 규칙을 찾을 수 있어야 한다. 일반 CSV 설명이나 다른 RFC로의 교체는 이 조건을 대신하지 않는다.','RFC 번호는 명시됐지만 독자의 실제 클릭/실패와 특정 byte판 재현 의도는 미확인이다.','PG-S02'),
 'A-D05':('SQLite','about.html','http://en.wikipedia.org/wiki/Endianness','SQLite 파일의 플랫폼 간 복사 설명에서 big-endian/little-endian 의미를 배경 학습한다.','background','바이트 순서와 big/little endian의 구분을 설명하는 본문에 도착한다.','특정 Wikipedia revision이나 역사판 고정 의도는 명시되지 않았다. 실제 복사/실행 결과는 이 링크로 증명하지 않는다.','SQL-S01'),
 'A-D06':('SQLite','aff_short.html','http://www.darwinsys.com/file/','application_id로 구별한 파일을 file(1) 도구가 알아보는 사용 맥락에서 그 도구를 확인한다.','specific_tool_role','file(1)의 파일 유형 판별 도구 정보에 도착해야 한다. 홈페이지 도달만으로 특정 SQLite application_id 판별 지원까지 입증되는 것은 아니다.','독자가 file 도구 어느 버전을 설치할지와 당장 설치하려는지 배경만 읽으려는지는 미확인이다.','SQL-S02')}

frame=[];refs=[];sources=[]
for project,a in archives.items():
    selected=0
    for order,name in enumerate(a['names'],1):
        b=a['read'](name);p=Links();p.feed(b.decode('utf-8',errors='replace'))
        ext=[x for x in p.links if x['href'].startswith(('https://','http://','//'))]
        row={'route':'D','project':project,'version':a['version'],'release_date':a['release_date'],'archive_url':a['archive_url'],'member':name,'member_order':order,'absolute_external_href_count':len(ext),'nonexternal_href_count':len(p.links)-len(ext),'decision':'no_external_url' if not ext else 'selected_first_body_external_href','reference_id':''}
        if ext:
            key=next(k for k,v in purpose.items() if v[0]==project and v[1]==Path(name).name)
            pr=purpose[key];target=next(x for x in ext if x['href']==pr[2]);assert target is ext[0]
            row['reference_id']=key;selected+=1
            line=target['line'];pos=target['position'];text=norm(p.text[max(0,pos-400):pos+900])
            title=re.search(r'<title>(.*?)</title>',b.decode(),re.S).group(1)
            before_text=norm(p.text[max(0,pos-400):pos]);after_text=norm(p.text[pos+len(target['text']):pos+900])
            member_file='excerpts/'+Path(name).name;(ROOT/member_file).write_bytes(b)
            ref={'reference_id':key,'sample':'A','route':'D','consumer_project':project,'consumer_version':a['version'],'consumer_release_date':a['release_date'],'consumer_release_date_role':'official stated product release day; exact first HTML public-access time unverified','date_precision':'day; source timezone unspecified','date_source_id':a['date_source'],'archive_id':Path(a['archive_url']).name,'archive_url':a['archive_url'],'distribution_format':a['format'],'archive_sha256':sha(a['bytes']),'archive_size_bytes':len(a['bytes']),'member_path':name,'member_sha256':sha(b),'member_size_bytes':len(b),'consumer_document_title':title,'raw_href':target['href'],'href_kind':'absolute_http_url','document_base_url':'file:///<extraction-root>/'+name,'base_url_note':'Offline archive member context; href is absolute, so no base resolution required. The mutable online document is not substituted for this byte copy.','resolved_url':target['href'],'fragment':'','link_text':norm(target['text']),'raw_link_line':line,'context_before':before_text,'context_after':after_text,'context_window':text,'purpose':pr[3],'purpose_kind':pr[4],'minimum_success_condition':pr[5],'intent_unknown':pr[6],'source_ids':[pr[7]],'read_observed_at_utc':now,'archive_fetched_at_utc':a['observed_at_utc'],'record_prepared_at_utc':now,'seal_status':'prepared_for_root_remote_seal','future_read_before_seal':False,'upstream_current_opened':False,'followup_consumer_opened':False,'A_B_duplicate':'pending B selection','source_local_copy':'collectors/offline/'+member_file}
            refs.append(ref)
            sources.append({'source_id':pr[7],'source_type':'distributed_html_member','publisher':'PostgreSQL Global Development Group' if project=='PostgreSQL' else 'SQLite project','original_url':a['archive_url'],'document_locator':a['archive_url']+' :: '+name,'version':a['version'],'publication_date':a['release_date'],'publication_date_role':'official product release day; not a first-public-access timestamp','observed_at_utc':now,'directly_read_location':name+' line '+str(line)+' and surrounding paragraphs','findings':pr[3]+' 원 HTML raw href='+target['href'],'limitations':pr[6]+' 목적지의 현재 내용/역사 변화/후속 소비자 배포물은 아직 읽지 않음.','questions':['Q1','Q2'],'reference_ids':[key],'duplicate_group':project+'-'+a['version']+'-'+Path(name).name,'count_minimum':True,'minimum_bucket':'A_distribution','archive_sha256':sha(a['bytes']),'member_sha256':sha(b),'member_path':name,'local_copy':'collectors/offline/'+member_file})
        frame.append(row)
        if selected==2:break

extra=[
 {'source_id':'PG-S03','project':'PostgreSQL','file':'excerpts/pg-source-index.html','url':'https://ftp.postgresql.org/pub/source/v12.2/','location':'file listing postgresql-12.2.tar.bz2','findings':'공식 source 배포원장에서 20,363,545-byte tar.bz2와 checksum 파일을 확인. 2020-02-10 22:29는 원장 파일시각이다.','limits':'mtime은 최초 공개 시각/공식 출시일/독자 열람일이 아니다.','date':'2020-02-10 22:29','role':'listing mtime','count':False},
 {'source_id':'PG-S04','project':'PostgreSQL','file':'excerpts/release-12-2.html','url':archives['PostgreSQL']['archive_url'],'location':'postgresql-12.2/doc/src/sgml/html/release-12-2.html line 2; Release date','findings':'배포 archive의 릴리스 노트 원문에 Release date: 2020-02-13이 있다.','limits':'시각·timezone·첫 공개 접근 시간과 실제 독자 클릭은 미확인.','date':'2020-02-13','role':'stated release day','count':False},
 {'source_id':'SQL-S03','project':'SQLite','file':'excerpts/sqlite-chronology.html','url':'https://www.sqlite.org/chronology.html','location':'2020 release rows, 3.31.0 through 3.34.0','findings':'공식 chronology에서 2020년 첫판은3.31.0(2020-01-22), 다음3.31.1(2020-01-27)이다. 원장만 읽었고 후속판 본문은 열지 않았다.','limits':'현재 유지 원장이고 해당 시각의 다운로드 성공/독자 열람은 입증하지 않는다.','date':None,'role':'current official chronological ledger','count':False},
 {'source_id':'SQL-S04','project':'SQLite','file':'excerpts/3_31_0.html','url':archives['SQLite']['archive_url'],'location':'sqlite-doc-3310000/releaselog/3_31_0.html title and H2','findings':'zip 실제 멤버에 SQLite Release 3.31.0 On 2020-01-22가 있다.','limits':'초 단위 공개일/독자 클릭 시각은 미확인. archive zip metadata는 출판일 대신 사용하지 않는다.','date':'2020-01-22','role':'stated release day','count':False}]
for x in extra:
    b=(ROOT/x['file']).read_bytes()
    sources.append({'source_id':x['source_id'],'source_type':'distribution_ledger_or_release_date_receipt','publisher':x['project'],'original_url':x['url'],'version':archives[x['project']]['version'],'publication_date':x['date'],'publication_date_role':x['role'],'observed_at_utc':now,'directly_read_location':x['location'],'findings':x['findings'],'limitations':x['limits'],'questions':['Q1','Q2','Q6'],'reference_ids':['A-D03','A-D04'] if x['project']=='PostgreSQL' else ['A-D05','A-D06'],'duplicate_group':x['source_id'],'count_minimum':False,'minimum_bucket':'sampling_or_date_metadata','sha256':sha(b),'local_copy':'collectors/offline/'+x['file']})
for fname,rows in [('references.jsonl',refs),('sources.jsonl',sources)]:
    (ROOT/fname).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
with (ROOT/'frame.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(frame[0]));w.writeheader();w.writerows(frame)
summary={'prepared_at_utc':now,'references':len(refs),'distinct_documents':len(refs),'projects':2,'archive_html_counts':{k:len(a['names']) for k,a in archives.items()},'frame_docs_scanned_to_second_reference':len(frame),'selected_documents':len(refs),'documents_without_external_url':sum(x['decision']=='no_external_url' for x in frame),'excluded_navigation_external':0,'excluded_footer_external':0,'excluded_example_external':0,'excluded_package_without_url_in_frame':'included in document no_external_url count; individual tokens not enumerated','upstream_current_opened':False,'followup_consumer_opened':False,'note':'Initial exploratory inspection also printed a few later HTML candidate snippets from the same original archive; selection remains first two eligible documents. No upstream destination was fetched.'}
(ROOT/'seal-preparation.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
