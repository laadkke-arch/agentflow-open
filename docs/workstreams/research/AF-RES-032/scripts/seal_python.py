import pathlib, json, csv, re, hashlib, html
from datetime import datetime,timezone
from urllib.parse import urlsplit,urljoin
from lxml import html as lh
R=pathlib.Path(__file__).resolve().parents[1]/'collectors'/'python'
cs=json.loads((R/'candidates.json').read_text()); at=datetime.now(timezone.utc).isoformat()
references=[];sources=[];frame=[]
purposes=[('배경 읽기','Python 도움말이 사용한 reStructuredText 표기/원문 형식을 알아본다.','reStructuredText가 무엇이고 문서 원문 형식을 이해할 수 있는 공식 설명.','실행 API나 특정 markup 판/역사적 byte 재현을 요구한다는 문구는 없다.'),('현재 작업 안내','Python 문서에 대해 이미 접수된 열린 오류 목록을 찾아 중복 보고를 피한다.','documentation 분류의 접수된 열린 issue 목록으로 갈 수 있다.','특정 issue 재현이나 2020년 목록 고정 의도는 없다. 현재 보고 절차로 이어지는 문맥이다.')]
for i,c in enumerate(cs[:2],1):
    member=c['member']; path=member.split('/',1)[1]; b=(R/path.replace('/','__')).read_bytes()
    doc=lh.fromstring(b);body=doc.xpath('//div[@class="body"]')[0]; links=body.xpath('.//a[starts-with(@href,"http")]');a=links[0]
    href=a.get('href');selected=c['links'][0];rid=f'A-D0{i}';sid=f'PY-S0{i}';base='https://docs.python.org/3.8/'+path
    context=selected['context']; artifact=c['archive']
    # raw attribute lexical bytes differ from DOM href when HTML entities occur.
    raw=selected['href'];kind,purpose,success,unknown=purposes[i-1]
    r={'reference_id':rid,'sample':'A','route':'D','consumer_project':'CPython documentation','consumer_version':'3.8.2','consumer_release_date':'2020-02-24','publication_date_role':'official Python software release date; exact offline HTML first publication unknown','publication_source_id':'PY-PUB01','artifact_url':artifact['url'],'artifact_id':'python-3.8.2-docs-html.tar.bz2','artifact_sha256':artifact['sha256'],'artifact_bytes':artifact['bytes'],'member':member,'member_sha256':c['member_sha256'],'document_title':doc.find('.//title').text,'raw_href':href,'raw_href_html_attribute':raw,'base_url':base,'resolved_url':urljoin(base,href),'fragment':urlsplit(href).fragment,'link_text':' '.join(a.itertext()).strip(),'surrounding_text':context,'purpose_type':kind,'purpose':purpose,'minimum_success':success,'intent_unknown':unknown,'external_to_artifact':True,'consumer_equals_target_issuer':i==2,'source_ids':[sid,'PY-PUB01','PY-IDX01'],'observed_at_utc':artifact['observed_at_utc'],'sealed_at_utc':at,'upstream_read_before_seal':False,'future_consumer_read_before_seal':False,'archive_mtime_role':'2020-02-25T11:45:36Z HTTP Last-Modified / index timestamp; not proved first publication','duplicate_key':f'CPython-3.8.2-{path}','A_B_duplicate':None}
    references.append(r)
    (R/f'{rid}-excerpt.html').write_text(selected['html_fragment']+'\n')
    sources.append({'source_id':sid,'kind':'consumer_original_distribution_html','publisher':'Python Software Foundation','original_url':artifact['url'],'version':'3.8.2','publication_date':'2020-02-24','publication_date_role':'software release, not archive first exposure','observed_at_utc':artifact['observed_at_utc'],'read_location':member+'; '+str(body.xpath('.//h1')[0].text_content())+' first body external href','findings':context+' 목적 판정: '+purpose,'limits':unknown+' 실제 독자 클릭/실패와 당시 서버상태는 확인하지 않았다.','questions':['Q1','Q2'],'reference_ids':[rid],'duplicate_group':r['duplicate_key'],'count_minimum':True,'count_category':'A_original','artifact_sha256':artifact['sha256'],'member_sha256':c['member_sha256'],'local_evidence':f'collectors/python/{rid}-excerpt.html'})
    frame.append({'frame_id':rid,'route':'D','project':'CPython','edition':'3.8.2','date':'2020-02-24','member':member,'disposition':'selected','reason':'first eligible external body link in member path order','excluded_navigation_links':len(c['links'])-len(links),'external_body_links':len(links),'selected_href':href})
    for j,ln in enumerate(links[1:],2):frame.append({'frame_id':rid+f'-L{j}','route':'D','project':'CPython','edition':'3.8.2','date':'2020-02-24','member':member,'disposition':'excluded','reason':'one reference per distinct published HTML document','selected_href':ln.get('href')})
access=[json.loads(x) for x in (R/'access.jsonl').read_text().splitlines()]
for sid,rec,kind,findings,limits in [('PY-IDX01',access[0],'distribution_index','실제 tar.bz2/zip HTML 배포목록과2020-02-25 timestamp를 읽음.','index timestamp는 최초공개 영수증이 아니다.'),('PY-PUB01',access[1],'official_release_receipt','Python3.8.2 Release date Feb.24,2020 및 Online Documentation link를 읽음.','이 날짜가 docs archive 첫 publication이라는 보장은 없다.')]:
    sources.append({'source_id':sid,'kind':kind,'publisher':'Python Software Foundation','original_url':rec['url'],'version':'3.8.2','publication_date':'2020-02-24' if sid=='PY-PUB01' else None,'observed_at_utc':rec['observed_at_utc'],'read_location':'main release/date/docs links' if sid=='PY-PUB01' else 'HTML tar.bz2 listing','findings':findings,'limits':limits,'questions':['Q1','Q4','Q6'],'reference_ids':['A-D01','A-D02'],'duplicate_group':sid,'count_minimum':False,'count_category':'method_support','sha256':rec['sha256']})
for fn,rows in [('references.jsonl',references),('sources.jsonl',sources)]:
    (R/fn).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
keys=list(dict.fromkeys(k for r in frame for k in r));f=(R/'frame.csv').open('w');w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(frame);f.close()
# Keep complete bytes in ignored cache; retain only excerpts and hashes in the committed evidence.
for p in R.glob('*.html'):
    if not p.name.endswith('-excerpt.html'):p.rename(R/'cache'/p.name)
print(json.dumps(references,ensure_ascii=False,indent=2))
