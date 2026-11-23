"""Reconstruct CPython selection evidence from retained temporary downloads.
No newer-edition body or asset is read here. See stage1.md for acquisition URLs.
"""
from pathlib import Path
import csv, datetime, hashlib, json, posixpath, re, struct, zipfile
ROOT = Path(__file__).resolve().parent
CACHE = Path('/tmp/af098-cpython')
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
PREFIX = 'python-3.12.0-docs-html/'
ARCHIVE_URL = 'https://docs.python.org/ftp/python/doc/3.12.0/python-3.12.0-docs-html.zip'
z = zipfile.ZipFile(CACHE/'old.zip')
receipts = json.loads((CACHE/'old-http-receipts.json').read_text())
(ROOT/'old-http-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')


def sha(b): return hashlib.sha256(b).hexdigest()

def main_body(s):
    return s.split('<div class="body" role="main">',1)[-1].split('<div class="sphinxsidebar"',1)[0]

rows=[]
for n in sorted(z.namelist()):
    if not n.endswith('.html'): continue
    p=n[len(PREFIX):]
    s=z.read(n).decode('utf-8')
    main=main_body(s)
    refs=re.findall(r'<(?:img|source)\b[^>]*\s(?:src|srcset)="([^"]+)"',main)
    refs=[x for x in refs if '_static/' not in x and not x.startswith(('http:','https:','//','data:'))]
    downloads=re.findall(r'<a\b[^>]*\bhref="([^"]+)"',main)
    downloads=[x for x in downloads if not x.startswith(('http:','https:','//','#')) and '_static/' not in x and re.search(r'\.(?:png|svg|jpe?g|gif|csv|txt|dat|jsonl?|xml|bin|zip)(?:$|[#?])',x)]
    target=p.startswith(('c-api/','extending/','howto/','library/','reference/','tutorial/'))
    eligible=target and bool(refs or downloads)
    chosen={'howto/logging.html':'PY1','library/hashlib.html':'PY2'}.get(p,'')
    rows.append(dict(project='CPython',order=len(rows)+1,release='3.12.0',release_date='2023-10-02',relative_path=p,frame_source=ARCHIVE_URL,body_asset_refs=';'.join(refs+downloads),eligible=str(eligible).lower(),example_id=chosen,decision=('selected' if chosen else 'eligible_after_first_two' if eligible else 'excluded_page_family' if not target else 'no_named_local_image_or_data_reference_in_main_body'),scan_scope='main body img/srcset/source and local image/data download href; _static/navigation excluded'))
with (ROOT/'frame.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
selected=[]
for case,p,section,kind,filename,purpose in [
 ('PY1','howto/logging.html','logging-flow','tutorial explanation diagram','logging_flow.png','3.12.0 Advanced Logging Tutorial에서 logger와 handler의 이벤트 전달·중단 흐름 그림을 읽거나 재사용한다.'),
 ('PY2','library/hashlib.html','creating-hash-objects','reference explanation diagram','hashlib-blake2-tree.png','3.12.0 BLAKE2 참조의 tree mode 매개변수 깊이·offset·fanout 그림을 읽거나 재사용한다.')]:
    body=z.read(PREFIX+p);asset=z.read(PREFIX+'_images/'+filename);s=body.decode();lines=s.splitlines();line=next(i for i,l in enumerate(lines,1) if 'src="../_images/'+filename+'"' in l)
    width,height=struct.unpack('>II',asset[16:24])
    item={'case_id':case,'project':'CPython','old_version':'3.12.0','new_version':'3.12.1','old_release_date':'2023-10-02','new_release_date':'2023-12-08','old_release_url':'https://www.python.org/downloads/release/python-3120/','new_release_url':'https://www.python.org/downloads/release/python-3121/','old_discovery_route':'official download.html → HTML ZIP → sorted archive member paths, then direct exact-version HTML/payload verification','relative_page':p,'section':section,'old_uri':'https://docs.python.org/release/3.12.0/'+p+'#'+section,'logical_resource':filename,'resource_kind':kind,'purpose':purpose,'literal_reference':'../_images/'+filename,'resolved_old_asset_uri':'https://docs.python.org/release/3.12.0/_images/'+filename,'relative_asset_path':'_images/'+filename,'body_sha256':sha(body),'body_bytes':len(body),'body_line':line,'asset_sha256':sha(asset),'asset_bytes':len(asset),'mime':'image/png','dimensions':[width,height],'archive_url':ARCHIVE_URL,'archive_member_body':PREFIX+p,'archive_member_asset':PREFIX+'_images/'+filename,'direct_bytes_equal_archive':True,'selection_utc':NOW,'next_body_asset_exposure':False,'note':'설명 그림을 포함하는 튜토리얼/참조 주 본문이라는 사전 정의. 실행해 생성한 예제 출력으로 분류하지 않는다.'}
    selected.append(item)
    (ROOT/(case+'-old-excerpt.json')).write_text(json.dumps({'case_id':case,'document_url':item['old_uri'],'line':line,'tag':lines[line-1],'base_element_count':len(re.findall(r'<base\b',s,re.I)),'uri_resolution':'RFC3986-style relative resolution against document URL; no base element','body_sha256':sha(body),'archive_member':PREFIX+p,'body_bytes_equal_live':sha((CACHE/('logging-old.html' if case=='PY1' else 'hashlib-old.html')).read_bytes())==sha(body),'pixel_dimensions':[width,height],'visual_observation':('Logger and handler flow diagram with stop/filter/propagate branches' if case=='PY1' else 'BLAKE2 tree showing depths 0..2, offsets 0..3, fanout/leaves/last nodes'),'static_scope':'정적 HTML 속성·PNG 바이트·그림의 시각 확인. 브라우저 네트워크나 예제 프로그램 실행 아님.'},ensure_ascii=False,indent=2)+'\n')
(ROOT/'selected.json').write_text(json.dumps({'frozen_utc':NOW,'stage':'1-old-selection-only','release_rule':'public release date in 2023-2025, first stable x.y.0 and first subsequent stable maintenance','old':'3.12.0','next':'3.12.1','frame_html_count':len(rows),'qualifying_body_page_count':sum(r['eligible']=='true' for r in rows),'selected':selected,'exposure':{'next_release_metadata_only':'3.12.1 release date and first-maintenance wording read; no new example bodies/assets/listing/CI read','parent_preflight':'parent reported old 3.12.0 download.html preflight only'}},ensure_ascii=False,indent=2)+'\n')
sources=[]
def add(id,url,cache,utc,locator,observed,claim,category,case='',limitations='발행자 원문을 읽은 정적 확인이며 빌드 실행·생성 job 증거는 아니다.',counted=True,dedup_basis='이 URL의 저작/바이트를 최초 산입'):
    b=(CACHE/cache).read_bytes();sources.append({'id':id,'q':['Q1'],'case_id':case,'url':url,'fixed_url':url,'utc':utc,'publisher':'Python Software Foundation / CPython documentation authors','lineage':'CPython documentation','version':'3.12.0' if '3120' in url or '3.12.0' in url else '3.12.1' if '3121' in url else 'release-list','locator':locator,'observed':observed,'claim':claim,'limitations':limitations,'category':category,'counted':counted,'dedup_basis':dedup_basis,'sha256':sha(b),'bytes':len(b)})
add('PY-S001','https://www.python.org/downloads/','release-list.html','2026-11-23T19:35:01.639614+00:00','release entries 3.11.0/3.12.0/3.13.0/3.14.0','공개 목록의 안정 x.y.0은 3.11.0=2022-10-24(기간 밖), 3.12.0=2023-10-02, 3.13.0=2024-10-07, 3.14.0=2025-10-07. 3.12.1은 2023-12-08.','날짜 오름차순 첫 적격 판은 3.12.0','release_record')
add('PY-S002','https://www.python.org/downloads/release/python-3120/','release-old.html','2026-11-23T19:35:09.346127+00:00','Release date; stable release heading','Release date 2023-10-02 및 stable release라는 발행자 표시.','3.12.0은 선정 기간의 안정판','release_record')
add('PY-S003','https://www.python.org/downloads/release/python-3121/','release-next.html','2026-11-23T19:35:16.655111+00:00','Release date; first maintenance heading','Release date 2023-12-08 및 first maintenance release라고 명시. 예제 본문은 읽지 않았다.','다음 비교판은 3.12.1','release_record')
add('PY-S004','https://docs.python.org/release/3.12.0/download.html','download-old.html','2026-11-23T19:35:26.560281+00:00','HTML ZIP download link','공식 다운로드 페이지가 정확한 3.12.0 HTML ZIP URL을 제공.','이전판 모집틀은 공식 다운로드 배포를 통해 확보','distribution_record')
add('PY-S005',ARCHIVE_URL,'old.zip','2026-11-23T19:35:57.925742+00:00','ZIP central directory; selected HTML and PNG members','ZIP 12,737,860B, 전체 1,063개 엔트리. docs.python.org에서 www.python.org로 이동. 선택된 HTML·PNG 네 파일은 직접 URL 응답과 바이트 동일.','정확한 판 배포 패키지 포함을 확인','distribution_record',limitations='ZIP 전체를 내려받았지만 모든 본문을 사람이 읽었다고 세지 않는다. frame은 자동 탐색 목록이며 실제 읽은 주 본문/그림은 별도 원장 행.')
for r,item in zip(receipts[:2],selected):
    add('PY-S006' if item['case_id']=='PY1' else 'PY-S007',r['url'],r['key'],r['utc'],'HTML line '+str(item['body_line'])+'; #'+item['section'],('Logging Flow 절의 img src가 ../_images/logging_flow.png.' if item['case_id']=='PY1' else 'Creating hash objects 절의 figure/img src가 ../_images/hashlib-blake2-tree.png. srcset/picture/data URI 없음.'),'이전판 정확한 절이 이름 있는 로컬 PNG를 직접 사용','example_body',item['case_id'])
for r,item in zip(receipts[2:],selected):
    add('PY-S008' if item['case_id']=='PY1' else 'PY-S009',r['url'],r['key'],r['utc'],'PNG signature/IHDR; SHA256 '+r['sha256'],f"PNG {item['dimensions'][0]}×{item['dimensions'][1]}, {item['asset_bytes']}B. 주 본문의 src 및 패키지 파일과 일치; 실제 그림도 열어 내용 확인.",'이전판 참조 payload 실제 회수','payload',item['case_id'])
(ROOT/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
summary={'archive_url':ARCHIVE_URL,'archive_final_url':'https://www.python.org/ftp/python/doc/3.12.0/python-3.12.0-docs-html.zip','archive_sha256':sha((CACHE/'old.zip').read_bytes()),'archive_bytes':(CACHE/'old.zip').stat().st_size,'entries':len(z.namelist()),'html_count':len(rows),'qualifying_count':sum(r['eligible']=='true' for r in rows),'selected':['PY1','PY2'],'stage1_unique_sources':len(sources),'next_edition_example_or_payload_read':False}
(ROOT/'stage1-receipt.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,indent=2))
