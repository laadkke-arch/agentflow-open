"""Reproduce original CRAN A observation ledgers from cached official archives.
No current target or subsequent edition is fetched. Inputs are pinned by SHA256.
"""
import pathlib,json,tarfile,hashlib,re,datetime,csv
from urllib.parse import urljoin,urlsplit
from lxml import html
R=pathlib.Path(__file__).parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')
archives=json.loads((R/'original-archives.json').read_text())
indices=json.loads((R.parent/'index-receipts.json').read_text())
(R/'excerpts').mkdir(exist_ok=True)
refs=[];sources=[];frames=[];attempts=[];editions=[]
def squish(x):return ' '.join(x.split())
def first_sentence(x):
 x=squish(x)
 return re.split(r'(?<=[.!?])\s+(?=[A-Z])',x)[0] if x else None
purpose={
'datatables.html':('library_background_for_example','HTML의 mtcars 표를 향상시키는 JavaScript DataTables 라이브러리를 알아본다.','HTML 표를 향상시키는 DataTables의 역할과 관련 안내로 접근한다.','이 배포 문서는 끝에서 자신을 toy example이라 부르고 DT 사용을 권한다. 특정 DataTables 판을 그대로 재현하라는 요구는 없다.'),
'docco-classic.html':('style_background_for_example','R Markdown vignette 예제가 쓰는 Docco 스타일을 알아본다.','예제의 문서/코드를 나란히 보여 주는 Docco 스타일과 해당 도구의 설명에 접근한다.','Classic 스타일의 예시는 명시됐지만 상류 Docco의 특정 버전 재현 요구는 없다.'),
'lua-filters.html':('specific_css_compatibility','R Markdown의 newpage/pagebreak를 HTML로 변환할 때 생성되는 page-break-after CSS 규칙을 읽는다.','page-break-after의 페이지 나누기 의미와 호환성/대체 관계를 확인할 수 있다.','같은 원판 뒤 문단은 break-after를 권하고 page-break-after를 호환성을 위해 남긴다고 이미 설명한다. 최신 속성으로 무조건 교체하라는 인용은 아니다.'),
'pandoc.html':('bundled_tool_installation','Pandoc을 별도 설치하지 않아도 되는 RStudio IDE를 구한다.','해당 rmarkdown 요구 Pandoc>=1.12.3을 포함하거나 그 제공 여부를 확인할 수 있는 RStudio IDE 다운로드/설치 안내에 접근한다.','href는 preview 경로지만 링크텍스트/본문은 RStudio IDE 일반 배포를 말한다. 반드시 preview판 또는 특정 IDE판을 보존하려는 의도는 미확인이다.'),
'compatibility.html':('package_successor_for_backend','dplyr에서 데이터베이스 코드가 분리된 dbplyr 패키지를 확인하여 backend 개발자가 호환성 변경을 이해한다.','dbplyr라는 후계 패키지와 데이터베이스 backend 관련 안내에 접근한다.','본문은 같은 문단의 별도 backend news 앵커도 제시한다. 선택 href는 패키지 루트이며 정확한 해당 news절의 독립 요구와 혼합하지 않는다.'),
'dplyr.html':('fixed_year_data_provenance','예제의 nycflights13::flights에 포함된 2013년 뉴욕 출발 항공편 데이터의 미국 교통통계국 출처를 확인한다.','항공 운항 정시성 데이터의 출처를 식별하고 2013년이라는 예제 범위와 구별할 수 있다.','예제 데이터는 2013년으로 명시됐지만 클릭한 BTS 페이지가 2013년 고정 스냅샷이어야 한다는 별도 의도는 미확인이다. 원표 링크는 DatabaseInfo이며 개별2013원자료파일이 아니다.')}

for ix in indices:
 body=ix.get('body') or (R.parent/'cache'/f"{ix['project']}-index.html").read_text();meta={k:v for k,v in ix.items() if k!='body'}
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
 attempt.update(attempt_kind='original_archive',source_counted=False,scope='Original archive only, no target content or subsequent editions',selected_for_A=a['project'] in ('knitr','rmarkdown','dplyr'))
 attempts.append(attempt)
 if a['project'] not in ('knitr','rmarkdown','dplyr'):continue
 archive_bytes=(R.parent/'cache'/a['name']).read_bytes();assert hashlib.sha256(archive_bytes).hexdigest()==a['sha256']
 version=re.search(r'^Version:\s*(.+)',a['description'],re.M)[1]
 pub=re.search(r'^Date/Publication:\s*(.+)',a['description'],re.M)[1]
 pubiso=datetime.datetime.strptime(pub,'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=datetime.timezone.utc).isoformat().replace('+00:00','Z')
 (R/'excerpts'/f"{a['project']}-{version}-DESCRIPTION.txt").write_text(a['description'])
 with tarfile.open(R.parent/'cache'/a['name']) as tf:
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
   source_same=False
   ref=dict(reference_id=rid,sample='A',route='R',consumer_project=a['project'],consumer_edition=version,document_title=dom.xpath('//title')[0].text_content(),document_header_date=squish(' '.join(dom.xpath('//h4[contains(@class,"date")]/text()'))),archive_url=a['url'],archive_id=a['name'],archive_sha256=a['sha256'],archive_bytes=len(archive_bytes),member_path=member,member_sha256=hashlib.sha256(b).hexdigest(),member_bytes=len(b),raw_href=target,raw_citation_url=target,raw_anchor_html=rawanchor,raw_href_status='literal href read inside published archive HTML',base_url='file:///'+member,base_url_provenance='Calculation-only virtual offline archive root. Reader installation pathname is unknown. Absolute href ignores base.',resolution_rule='urllib.parse.urljoin; selected href is absolute so base-independent',resolved_url=urljoin('file:///'+member,target),fragment=urlsplit(target).fragment,link_text=squish(x.text_content()),context_before_sentence=before,context_link_paragraph=txt,context_after_sentence=after,click_purpose=purp,purpose_class=kind,minimum_success=minimum,purpose_unknown=unknown,external_to_archive=True,upstream_and_consumer_same_project=source_same,publication_utc=pubiso,publication_evidence=f"{a['url']}!/{a['project']}/DESCRIPTION Date/Publication",publication_metadata_role='CRAN publication timestamp explicitly encoded in original archive DESCRIPTION; not reader access',archive_index_time=a['date'],archive_index_timezone='미확인; not UTC-normalized',original_body_line=x.sourceline,raw_block_line_start=s[:start].count('\n')+1,raw_block_line_end=s[:end].count('\n')+1,excerpt_path=excerptpath,excerpt_sha256=hashlib.sha256(rawblock.encode()).hexdigest(),fetched_at=a['checked_at'],read_at=now,collector_frozen_at=now,upstream_current_or_later_read_before_freeze=False,source_ids=[sid],A_B_overlap='B not selected yet; exact consumer+purpose+event comparison deferred')
   refs.append(ref)
   sources.append(dict(source_id=sid,material_type='published package built HTML vignette',author_or_publisher=f"{a['project']} maintainers / CRAN",original_url=a['url'],distribution_member=member,version_or_tag=version,published_at=pubiso,published_at_basis='archive DESCRIPTION Date/Publication',checked_at_utc=now,fetched_at_utc=a['checked_at'],read_location=f'HTML line {x.sourceline}; block lines {ref["raw_block_line_start"]}–{ref["raw_block_line_end"]}; title and surrounding prose',confirmed=purp+' 실제 배포 HTML의 literal href와 링크문맥을 확인했다.',cannot_confirm='이 source만으로 링크 목적지의 당시/현재 내용·상류 변경·소비자 후속판 변경·독자의 실제 클릭 또는 실패는 미확인. '+unknown,questions=['Q1','Q2'],reference_ids=[rid],judgment='original artifact reference frozen before outcome',duplicate_group='R-'+a['project']+'-'+pathlib.Path(member).stem,counted_for_minimum=True,minimum_category='A_original',archive_sha256=a['sha256'],member_sha256=ref['member_sha256'],evidence_path=excerptpath,read_by='cran_a collector',read_mode='archive bytes fetched with urllib; HTML parsed/read locally'))
# Replace archive bodies in receipt with hashes and filenames so index evidence is concise.
cleanindex=[]
for x in indices:
 clean={k:v for k,v in x.items() if k!='body'};clean['sha256']=hashlib.sha256((x.get('body') or (R.parent/'cache'/f"{x['project']}-index.html").read_text()).encode()).hexdigest();clean['cache_path']='cache/'+x['project']+'-index.html';cleanindex.append(clean)
(R/'index-receipts.json').write_text(json.dumps(cleanindex,ensure_ascii=False,indent=2)+'\n')
for name,rows in [('references.jsonl',refs),('sources.jsonl',sources),('attempts.jsonl',attempts)]:
 (R/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
for name,rows in [('frame.csv',frames),('editions.csv',editions)]:
 with (R/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=dict(reference_count=len(refs),project_count=len(set(r['consumer_project'] for r in refs)),distinct_html_documents=len(set((r['archive_url'],r['member_path']) for r in refs)),screened_documents=len(frames),excluded_documents_no_external_href=sum(f['status']=='excluded_no_external_href' for f in frames),outcome_targets_read=0,collector_frozen_at=now,original_archive_count=3,extra_original_archive_inventory_only='jsonlite1.6.1 downloaded/description/memberlist inspected while checking candidate ordering; no HTML selected or read',sampling_revision='Date then CRAN archive URL then member path; supersedes provisional-project-order before any outcome target read')
(R/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
for r in refs:print(r['reference_id'],r['archive_id'],r['member_path'],r['raw_href'])
