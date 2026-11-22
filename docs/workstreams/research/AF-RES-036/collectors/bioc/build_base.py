"""Build the six preregistered Bioconductor B rows from downloaded releases."""
from pathlib import Path
import csv, hashlib, json, re
from html_extract import extract

P=Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def jread(p): return json.loads(p.read_text())
attempts=[json.loads(l) for l in (P/'attempts.jsonl').read_text().splitlines()]
by_attempt={r['attempt_id']:r for r in attempts}

specs=[
 ('R01','DESeq2','DESeq2-early-inventory.json','DESeq2/inst/doc/DESeq2.html',0,
  'FASTQ 파일에서 count matrix를 생성하는 단계까지 포함한 더 느린 속도의 RNA-seq workflow 안내를 읽는다.',
  'current','원문은 typical workflow를 배우는 실제 작업을 명시하며 특정 과거 판을 재현하라고 하지 않는다.'),
 ('R02','GenomicRanges','GenomicRanges-inventory.json','GenomicRanges/inst/doc/GenomicRangesIntroduction.html',1,
  'GenomicRanges가 기반으로 삼는 IRanges infrastructure 패키지를 확인한다.',
  'ambiguous','패키지 의존 기반을 설명하나 현재 설치 작업인지 과거 구조의 재현인지 명시하지 않는다. 3.11 href만으로 재현 의도를 추정하지 않는다.'),
 ('R03','SummarizedExperiment','SummarizedExperiment-early-inventory.json','SummarizedExperiment/inst/doc/Extensions.html',1,
  '사용자 정의 클래스의 validity 함수를 만들기 위해 S4Vectors의 setValidity2가 제공하는 방법을 읽는다.',
  'current','개발자를 위한 best practices와 실제 validity method 정의를 설명한다. 특정 판을 고정하라는 문장은 없다.'),
 ('R04','SingleCellExperiment','SingleCellExperiment-early-inventory.json','SingleCellExperiment/inst/doc/devel.html',3,
  'genomic coordinates와 rowRanges를 갖는 클래스 설계 예로 DESeq2의 DESeqDataSet을 확인한다.',
  'ambiguous','기존 설계 이유를 설명하는 예시다. 최신 구현을 요구하거나 당시 특정 판 재현을 명시하지 않는다.'),
 ('R05','scater','scater-early-inventory.json','scater/inst/doc/overview.html',2,
  'scater가 기반으로 삼아 다른 분석 패키지와 상호운용하는 SingleCellExperiment 데이터 클래스를 확인한다.',
  'current','실제 quality control 작업과 상호운용 데이터 구조를 소개한다. 3.11 href를 역사 의도로 확대하지 않는다.'),
 ('R06','SingleCellExperiment','SingleCellExperiment-early-inventory.json','SingleCellExperiment/inst/doc/intro.html',0,
  'SingleCellExperiment를 중심 데이터 구조로 사용하는 scater 패키지를 확인한다.',
  'ambiguous','중심 데이터 구조의 적용 예를 가리킨다. 현재판 또는 과거판만 요구한다는 문장이 없다.'),
]
refs=[];sources=[];links_audit=[]
out=P/'evidence';out.mkdir(exist_ok=True)
for rid,project,invfile,member,linkidx,purpose,stratum,stratum_basis in specs:
 inv=jread(P/invfile);mi=next(x for x in inv['html_members'] if x['member']==member)
 local=P/mi.get('path','members/'+member)
 content=local.read_bytes();assert sha(content)==mi['sha256']
 parsed=extract(local);text=parsed['text'];http=[x for x in parsed['links'] if x['href'].startswith(('http:','https:'))]
 link=http[linkidx]
 if rid=='R01':
  st=text.index('This vignette explains');en=text.index('FASTQ files.',st)+len('FASTQ files.')
 else:st=link['block_start'];en=link['block_end']
 context=text[st:en];assert len(context)<=1200
 rawlines=content.decode('utf-8').splitlines(keepends=True)
 line=link['line'];raw_excerpt=''.join(rawlines[max(0,line-10):min(len(rawlines),line+15)])
 if rid=='R01': raw_excerpt=''.join(rawlines[409:435])
 (out/(rid+'-B-context.txt')).write_text(context,encoding='utf-8')
 (out/(rid+'-B-html-excerpt.txt')).write_text(raw_excerpt,encoding='utf-8')
 desc=(local.parents[2]/'DESCRIPTION')
 # For release tarball paths local is package/inst/doc/x.html; DESCRIPTION is package/DESCRIPTION.
 desc=local.parent.parent.parent/'DESCRIPTION'
 desc_text=desc.read_text() if desc.exists() else ''
 if desc_text:(out/(rid+'-DESCRIPTION.txt')).write_text(desc_text)
 title=parsed['title']
 if rid=='R01':title='Analyzing RNA-seq data with DESeq2' # literal title in malformed YAML table
 row={'ref_id':rid,'route':'R','project':project,'consumer_title':title,'consumer_version':inv['version'],
      'distribution_release':'Bioconductor 3.11','distribution_release_date':'2020-04-28',
      'package_date_publication':re.search(r'^Date/Publication: (.+)$',desc_text,re.M).group(1) if re.search(r'^Date/Publication: (.+)$',desc_text,re.M) else 'unknown',
      'package_date_limit':'DESCRIPTION Date/Publication and Bioconductor release date are distinct; first actual HTML upload UTC is unknown.',
      'original_distribution_url':inv['url'],'archive_sha256':inv['sha256'],'member':member,
      'member_sha256':sha(content),'member_bytes':len(content),'source_id':'BIO-B'+rid[-2:],
      'local_raw_member':str(local.relative_to(P)), 'raw_member_committed':False,
      'original_href':link['href'],'link_text':link['anchor_text'],'source_html_line':line,
      'context':context,'context_sha256':sha(context.encode()),'context_codepoints':len(context),
      'clean_text_start':st,'clean_text_end':en,'clean_text_sha256':sha(text.encode()),
      'minimal_purpose':purpose,'purpose_stratum':stratum,'purpose_stratum_basis':stratum_basis,
      'excerpt_path':'evidence/'+rid+'-B-context.txt','raw_excerpt_path':'evidence/'+rid+'-B-html-excerpt.txt',
      'fetch_attempt_id':inv['attempt_id'],'fetch_utc':by_attempt[inv['attempt_id']]['finished_utc'],
      'selected_before_original_href_fetch':True,'pre_exposed_current_target':rid=='R04',
      'pre_exposure_note':'R-L02 read the DESeq2 3.11 landing page as original-distribution metadata before the SCE->DESeq2 link was selected. Canonical overlap is suspected and must be checked after seal.' if rid=='R04' else 'Original href not fetched; see cross-case overlap and end-patch acquisition log.',
      'cross_case_overlap':['R04'] if rid=='R01' else (['R01'] if rid=='R04' else (['R06'] if rid=='R05' else (['R05'] if rid=='R06' else []))),
      'selection_rule':'first eligible foreign technical link in member-path order; self-package navigation and contact-only links excluded',
      'historical_version_required_by_sentence':False,
      'reconstruct_command':'python -B docs/workstreams/research/AF-RES-036/collectors/bioc/reconstruct_base.py '+rid}
 refs.append(row)
 source={'source_id':row['source_id'],'source_type':'original_distribution_consumer','publisher':'Bioconductor / '+project+' authors',
         'original_url':inv['url'],'fixed_version_url':inv['url'],'publication_date':'2020-04-27 (package metadata); 2020-04-28 (3.11 release)',
         'version':inv['version'],'checked_utc':row['fetch_utc'],'location':member+' HTML line '+str(line)+'; cleaned text offsets '+str(st)+':'+str(en),
         'confirmed':purpose+' 실제 href와 주변문장을 2020년 초기 안정판 배포 HTML에서 확인.',
         'supports':['Q1','Q2',rid],'limitations':'Current target not queried at selection; purpose stratum is a stated interpretation. Versioned href alone does not establish historical intent. '+row['pre_exposure_note'],
         'duplicate_group':project+'/'+member,'count_minimum':True,'count_categories':['original_consumer'],
         'read_status':'needed_content_confirmed','archive_sha256':inv['sha256'],'member_sha256':sha(content),'evidence_path':row['excerpt_path']}
 sources.append(source)
 for i,l in enumerate(http[:linkidx+1]):
  reason='selected' if i==linkidx else ('self_package_navigation' if project.lower() in l['href'].lower() and 'github.com' not in l['href'] else 'contact_only_not_technical_reading')
  links_audit.append({'ref_id':rid,'ordinal_external_http':i+1,'href':l['href'],'text':l['anchor_text'],'line':l['line'],'disposition':reason})

(P/'references.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in refs))
(P/'sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in sources))
(P/'link-selection.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in links_audit))
frames=[]
for f in sorted(P.glob('*inventory.json')):
 inv=jread(f)
 selected=[r['ref_id'] for r in refs if r['original_distribution_url']==inv['url']]
 html=inv.get('html_members',[])
 why=('selected_original' if selected else ('end_patch_candidate_acquired_before_earliest_archive_resolved' if f.name in [n+'-inventory.json' for n in ['DESeq2','edgeR','limma','SummarizedExperiment','S4Vectors','AnnotationDbi','SingleCellExperiment','scater']] else ('no_built_html' if not html else 'index_only_or_no_eligible_external_link')))
 frames.append({'project':inv['project'],'release':inv['release'],'version':inv['version'],'url':inv['url'],'attempt_id':inv['attempt_id'],'http_status':inv['status'],'html_member_count':len(html),'selected_ref_ids':';'.join(selected),'disposition':why,'sha256':inv['sha256']})
with (P/'frame.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(frames[0]),lineterminator='\n');w.writeheader();w.writerows(frames)
print(json.dumps({'references':len(refs),'unique_projects':len(set(r['project'] for r in refs)),'frame_rows':len(frames),'historical_stratum':sum(r['purpose_stratum']=='historical' for r in refs)},ensure_ascii=False))
