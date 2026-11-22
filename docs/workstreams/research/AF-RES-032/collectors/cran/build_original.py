"""Reproduce original CRAN A observation ledgers from cached official archives.
No current target or subsequent edition is fetched. Inputs are pinned by SHA256.
"""
import pathlib,json,tarfile,hashlib,re,datetime,csv
from urllib.parse import urljoin,urlsplit
from lxml import html
R=pathlib.Path(__file__).parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')
archives=json.loads((R/'original-archives.json').read_text())
indices=json.loads((R/'index-receipts.json').read_text())
(R/'excerpts').mkdir(exist_ok=True)
refs=[];sources=[];frames=[];attempts=[];editions=[]
def squish(x):return ' '.join(x.split())
def first_sentence(x):
 x=squish(x)
 return re.split(r'(?<=[.!?])\s+(?=[A-Z])',x)[0] if x else None
purpose={
'DBI-1.html':('background_comparison','DBI의 공통 데이터베이스 인터페이스 발상에 대한 다른 언어의 선례인 Java JDBC를 읽는다.','Java JDBC가 DB 연결 인터페이스라는 설명에 접근할 수 있다.','원 HTML은 JDBC8 문서로 연결하지만 본문은 Java8 특정 API 재현을 요구하지 않는다. 제목의 문서 API0.1-6 및 본문 날짜2003과 배포일2021을 구별한다.'),
'DBI-advanced.html':('higher_level_library_recommendation','DBI보다 높은 추상화의 데이터 조작을 원할 때 dplyr를 알아본다.','로컬 data.frame과 원격 DB 조작을 설명하거나 적합한 DBI 기반 도구로 이어지는 dplyr 안내를 읽을 수 있다.','현재판을 반드시 사용하라는 명시나 dplyr의 특정 버전 요구는 없다.'),
'intro.html':('background_library','R curl 패키지의 바탕인 libcurl C 라이브러리의 개요와 지식을 얻는다.','libcurl C 라이브러리의 역할과 사용 안내로 접근한다.','libcurl 특정 판 고정이나 당시 정확한 byte 재현 의도는 명시되지 않았다.'),
'windows.html':('specific_configuration','Windows의 R curl에서 SSL backend를 OpenSSL로 바꾸는 CURL_SSL_BACKEND 환경변수 사용법을 확인한다.','CURL_SSL_BACKEND와 openssl 선택, R 로드 전 설정이라는 배포 문맥과 양립하는 libcurl 환경변수 설명을 읽는다.','모든 Windows/현재 curl판에서 OpenSSL backend가 제공된다는 보장은 이 옛 문서만으로 할 수 없다.'),
'datatable-faq.html':('historical_feature_explanation','v1.9.8(2016-11)에 추가된 datatable.WhenJisSymbolThenCallingScope 옵션과 j 심볼 해석의 긴 release-note 항목을 읽는다.','그 특정 옵션과 v1.9.8 동작 변경을 다루는 release-note 항목에 접근한다.','옛판 자체를 보존하려는 연구 재현 요구는 없다. 링크는 master NEWS지만 클릭 목적은 명시된 과거 기능 설명이다.'),
'datatable-importing.html':('historical_troubleshooting','plain R console에서 재현되지 않는 data.table·개발 helper 상호작용 문제를 과거 devtools issue192 사례와 비교한다.','지정된 devtools issue192의 문제·논의 내용을 읽어 현재 증상과 대조한다.','새 devtools 일반 매뉴얼이나 최신 버그를 요구하지 않는다. 해당 사용자의 실제 증상 동일성·해결 성공은 미확인이다.')}
for ix in indices:
 body=ix.get('body') or (R/'cache'/f"{ix['project']}-index.html").read_text();meta={k:v for k,v in ix.items() if k!='body'}
 meta.update(attempt_kind='official_archive_index',purpose='pre-outcome sampling frame',source_counted=False,limitation='Index server timestamps have no timezone label; original DESCRIPTION Date/Publication used separately.')
 attempts.append(meta)
 selected_names=[]
 for l in body.splitlines():
  m=re.search(r'href="([^\"]+\.tar\.gz)".*?(20(?:20|21|22|23|24)-\d\d-\d\d \d\d:\d\d)',l)
  if m:selected_names.append((m[2],m[1]))
 for day,name in sorted(selected_names):
  editions.append(dict(project=ix['project'],edition=name,url=ix['url']+name,listed_datetime=day,listed_timezone='미확인',inventory_scope='2020–2024 CRAN Archive visible entries',access='index listed only; no future content read',selected_original=any(a['name']==name for a in archives[:3])))
for a in archives:
 attempt={k:v for k,v in a.items() if k not in ('description','html_members')}
 attempt.update(attempt_kind='original_archive',source_counted=False,scope='Original archive only, no target content or subsequent editions',selected_for_A=a['project'] in ('DBI','curl','data.table'))
 attempts.append(attempt)
 if a['project'] not in ('DBI','curl','data.table'):continue
 archive_bytes=(R/'cache'/a['name']).read_bytes();assert hashlib.sha256(archive_bytes).hexdigest()==a['sha256']
 version=re.search(r'^Version:\s*(.+)',a['description'],re.M)[1]
 pub=re.search(r'^Date/Publication:\s*(.+)',a['description'],re.M)[1]
 pubiso=datetime.datetime.strptime(pub,'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=datetime.timezone.utc).isoformat().replace('+00:00','Z')
 (R/'excerpts'/f"{a['project']}-{version}-DESCRIPTION.txt").write_text(a['description'])
 with tarfile.open(R/'cache'/a['name']) as tf:
  taken=0
  for member in a['html_members']:
   if taken==2:break
   b=tf.extractfile(member).read();s=b.decode('utf-8');dom=html.fromstring(b)
   allanchors=dom.xpath('//body//a[@href]');external=[x for x in allanchors if urlsplit(x.get('href')).scheme in ('http','https')]
   frame=dict(frame_id='R-'+a['project']+'-'+pathlib.Path(member).stem,route='R',project=a['project'],edition=version,publication_utc=pubiso,distributor='CRAN',archive_url=a['url'],member_path=member,member_sha256=hashlib.sha256(b).hexdigest(),all_body_anchors=len(allanchors),external_http_anchors=len(external),internal_or_non_http_anchors=len(allanchors)-len(external),status='selected' if external else 'excluded_no_external_href',selected_reference_id='',first_eligible_external_href=external[0].get('href') if external else '',navigation_footer_excluded=0,example_uri_excluded=0,package_name_without_url_excluded=0,limitation='Internal/self anchors excluded from external-link frame; external first is body prose; no future outcome inspected.')
   frames.append(frame)
   if not external:continue
   x=external[0];taken+=1;rid=f'A-R{len(refs)+1:02d}';sid=f'R-S{len(refs)+1:02d}';frame['selected_reference_id']=rid
   block=x
   while block.getparent() is not None and block.tag not in ('p','li','dd','td'):block=block.getparent()
   while block.getparent() is not None and block.tag not in ('p','li','dd','td'):block=block.getparent()
   txt=squish(block.text_content());previous=block.getprevious();following=block.getnext()
   before=first_sentence(previous.text_content()) if previous is not None else None
   after=first_sentence(following.text_content()) if following is not None else None
   # Locate byte-exact enclosing p/li block; lxml's serialization is not called raw.
   target=x.get('href');rawhref=re.escape(target.replace('&','&amp;'))
   match=re.search(r'<a\b[^>]*href=[\"\']'+rawhref+r'[\"\'][^>]*>.*?</a>',s,re.S)
   if not match:raise ValueError((member,target))
   prefix=s[:match.start()];tag=block.tag;start=prefix.rfind('<'+tag)
   end=s.find('</'+tag+'>',match.end())+len(tag)+3
   rawblock=s[start:end];rawanchor=match[0]
   excerptpath=f'excerpts/{rid}.html-fragment.txt';(R/excerptpath).write_text(rawblock)
   # Short public reading receipt; metadata is not an additional independent original.
   kind,purp,minimum,unknown=purpose[pathlib.Path(member).name]
   source_same=(a['project']=='data.table' and 'Rdatatable/data.table' in target)
   ref=dict(reference_id=rid,sample='A',route='R',consumer_project=a['project'],consumer_edition=version,document_title=dom.xpath('//title')[0].text_content(),document_header_date=squish(' '.join(dom.xpath('//h4[contains(@class,"date")]/text()'))),archive_url=a['url'],archive_id=a['name'],archive_sha256=a['sha256'],archive_bytes=len(archive_bytes),member_path=member,member_sha256=hashlib.sha256(b).hexdigest(),member_bytes=len(b),raw_href=target,raw_citation_url=target,raw_anchor_html=rawanchor,raw_href_status='literal href read inside published archive HTML',base_url='file:///'+member,base_url_provenance='Calculation-only virtual offline archive root. Reader installation pathname is unknown. Absolute href ignores base.',resolution_rule='urllib.parse.urljoin; selected href is absolute so base-independent',resolved_url=urljoin('file:///'+member,target),fragment=urlsplit(target).fragment,link_text=squish(x.text_content()),context_before_sentence=before,context_link_paragraph=txt,context_after_sentence=after,click_purpose=purp,purpose_class=kind,minimum_success=minimum,purpose_unknown=unknown,external_to_archive=True,upstream_and_consumer_same_project=source_same,publication_utc=pubiso,publication_evidence=f"{a['url']}!/{a['project']}/DESCRIPTION Date/Publication",publication_metadata_role='CRAN publication timestamp explicitly encoded in original archive DESCRIPTION; not reader access',archive_index_time=a['date'],archive_index_timezone='미확인; not UTC-normalized',original_body_line=x.sourceline,raw_block_line_start=s[:start].count('\n')+1,raw_block_line_end=s[:end].count('\n')+1,excerpt_path=excerptpath,excerpt_sha256=hashlib.sha256(rawblock.encode()).hexdigest(),fetched_at=a['checked_at'],read_at=now,collector_frozen_at=now,upstream_current_or_later_read_before_freeze=False,source_ids=[sid],A_B_overlap='B not selected yet; exact consumer+purpose+event comparison deferred')
   refs.append(ref)
   sources.append(dict(source_id=sid,material_type='published package built HTML vignette',author_or_publisher=f"{a['project']} maintainers / CRAN",original_url=a['url'],distribution_member=member,version_or_tag=version,published_at=pubiso,published_at_basis='archive DESCRIPTION Date/Publication',checked_at_utc=now,fetched_at_utc=a['checked_at'],read_location=f'HTML line {x.sourceline}; block lines {ref["raw_block_line_start"]}–{ref["raw_block_line_end"]}; title and surrounding prose',confirmed=purp+' 실제 배포 HTML의 literal href와 링크문맥을 확인했다.',cannot_confirm='이 source만으로 링크 목적지의 당시/현재 내용·상류 변경·소비자 후속판 변경·독자의 실제 클릭 또는 실패는 미확인. '+unknown,questions=['Q1','Q2'],reference_ids=[rid],judgment='original artifact reference frozen before outcome',duplicate_group='R-'+a['project']+'-'+pathlib.Path(member).stem,counted_for_minimum=True,minimum_category='A_original',archive_sha256=a['sha256'],member_sha256=ref['member_sha256'],evidence_path=excerptpath,read_by='cran_a collector',read_mode='archive bytes fetched with urllib; HTML parsed/read locally'))
# Replace archive bodies in receipt with hashes and filenames so index evidence is concise.
cleanindex=[]
for x in indices:
 clean={k:v for k,v in x.items() if k!='body'};clean['sha256']=hashlib.sha256((x.get('body') or (R/'cache'/f"{x['project']}-index.html").read_text()).encode()).hexdigest();clean['cache_path']='cache/'+x['project']+'-index.html';cleanindex.append(clean)
(R/'index-receipts.json').write_text(json.dumps(cleanindex,ensure_ascii=False,indent=2)+'\n')
for name,rows in [('references.jsonl',refs),('sources.jsonl',sources),('attempts.jsonl',attempts)]:
 (R/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
for name,rows in [('frame.csv',frames),('editions.csv',editions)]:
 with (R/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=dict(reference_count=len(refs),project_count=len(set(r['consumer_project'] for r in refs)),distinct_html_documents=len(set((r['archive_url'],r['member_path']) for r in refs)),screened_documents=len(frames),excluded_documents_no_external_href=sum(f['status']=='excluded_no_external_href' for f in frames),outcome_targets_read=0,collector_frozen_at=now,original_archive_count=3,extra_original_archive_inventory_only='httr1.4.2 downloaded/description/memberlist inspected before quota confirmation; no HTML read or selected')
(R/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
for r in refs:print(r['reference_id'],r['archive_id'],r['member_path'],r['raw_href'])
