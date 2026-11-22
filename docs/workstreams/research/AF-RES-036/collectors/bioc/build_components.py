"""Freeze observation-only N/H strings. No decisions or answer key are made."""
from pathlib import Path
import json,hashlib,re,datetime,csv
P=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
attempts=[json.loads(x) for x in (P/'attempts.jsonl').read_text().splitlines()]
A={r['attempt_id']:r for r in attempts}
refs=[json.loads(x) for x in (P/'references.jsonl').read_text().splitlines()]
R={r['ref_id']:r for r in refs}
out=P/'components';out.mkdir(exist_ok=True)

def cut(file,start,end,source_id,url,kind='text',member=None,page=None):
 s=(P/file).read_text();st=s.index(start) if isinstance(start,str) else start
 en=s.index(end,st) if isinstance(end,str) else end
 excerpt=s[st:en]
 return {'source_id':source_id,'url':url,'local_text_file':file,'text_file_sha256':sha(s.encode()),
         'start_offset':st,'end_offset':en,'location':('PDF page '+str(page)) if page else ('member '+member if member else 'cleaned HTML text'),
         'member':member,'page':page,'text_format':kind,'text':excerpt,'sha256':sha(excerpt.encode())}

base='https://bioconductor.org/packages/'
nh=[]
for rid in R:
 orig=A['N-'+rid+'-ORIGINAL'];nsp=[]
 nversion='Bioconductor 3.11';overlap=[]
 if rid=='R01':
  f='current/R01-original.txt';s=(P/f).read_text();st=s.index('Page Not Found');en=s.index('The page you were looking for was not found.')+len('The page you were looking for was not found.')
  nsp=[cut(f,st,en,'BIO-N01',orig['final_url'])];nversion='404 response; no content edition'
 elif rid=='R02':
  nsp=[cut('current/R02-original.txt','This package is for version','      Author:','BIO-N02',orig['final_url'])]
  overlap=['Current landing explicitly says this is Bioconductor3.11 and links to stable up-to-date release.']
 elif rid=='R03':
  f='section-members/N-R03-S4-utils.R';s=(P/f).read_text();st=s.index('setValidity2 <-');en=s.index('\nnew2 <-',st)
  nsp=[cut(f,st,en,'BIO-N03-SOURCE',A['N-R03-SOURCE']['url'],'R source','S4Vectors/R/S4-utils.R')]
  nversion='S4Vectors0.50.3 / Bioconductor3.23 (current landing)'
 elif rid=='R04':
  f='current/R04-manual.txt';s=(P/f).read_text();st=s.index('    DESeqDataSet is a subclass');en=s.index('    The constructor functions',st)
  nsp=[cut(f,st,en,'BIO-N04-MANUAL',A['N-R04-MANUAL']['url']+'#page=9','pdftotext -layout',page=9)]
  st=s.index('arguments provided to SummarizedExperiment including rowRanges');en=s.index('     sampleTable',st)
  nsp.append(cut(f,st,en,'BIO-N04-MANUAL',A['N-R04-MANUAL']['url']+'#page=10','pdftotext -layout',page=10))
  nversion='DESeq2 reference manual1.28.1; PDF cover October17,2020'
  overlap=['Landing says Bioconductor3.11; current manual text explicitly includes Note that for Bioconductor3.1.']
 elif rid=='R05':
  f='current/R05-vignette.txt';s=(P/f).read_text();st=s.index('The SingleCellExperiment class is a lightweight');en=s.index('2 Creating SingleCellExperiment instances',st)
  nsp=[cut(f,st,en,'BIO-N05-VIGNETTE',A['N-R05-VIGNETTE']['url'])]
  nversion='SingleCellExperiment1.10.1; displayed date28April2020'
  overlap=['Landing says Bioconductor3.11; current vignette is explicitly dated28April2020.']
 else:
  nsp=[cut('current/R06-original.txt','This package is for version','      Author:','BIO-N06',orig['final_url'])]
  f='current/R06-original.txt';s=(P/f).read_text();st=s.index('Depends\n');en=s.index('Imports\n',st)
  nsp.append(cut(f,st,en,'BIO-N06',orig['final_url']))
  overlap=['Current landing explicitly labels Bioconductor3.11 and offers a stable up-to-date release link.']
 nhead=f"Observed UTC: {orig['finished_utc']}\nRequested: {orig['url']}\nHTTP: "+' -> '.join([str(x['status']) for x in orig['redirect_chain']]+[str(orig['status'])])+f"\nArrival: {orig['final_url']}\nEdition: {nversion}\n"
 # A declared followed URI is an observation, not a replacement recommendation.
 if rid in ['R03','R04','R05']:nhead+='Followed source: '+nsp[0]['url']+'\n'
 ntext=nhead+'\n'+('\n[...]\n'.join(s['text'] for s in nsp)).strip()
 assert len(ntext)<=1600,(rid,len(ntext))
 N={'text':ntext,'codepoints':len(ntext),'utf8_bytes':len(ntext.encode()),'sha256':sha(ntext.encode()),
    'raw_excerpt':'\n[...]\n'.join(s['text'] for s in nsp),'spans':nsp,'source_ids':list(dict.fromkeys(s['source_id'] for s in nsp)),
    'original_get_attempt_id':orig['attempt_id'],'http_status':orig['status'],'redirect_chain':orig['redirect_chain'],'final_url':orig['final_url'],
    'original_fragment':'','fragment_check':'not_applicable_no_original_fragment','queried_utc':orig['finished_utc'],
    'edition':nversion,'overlap_history':bool(overlap),'overlap_history_evidence':overlap,
    'pre_exposed_current_target':rid=='R04','empty_evidence':False,
    'body_adequacy':'error response only; needed workflow absent' if rid=='R01' else 'exact stated target/section read; not an outcome judgement',
    'extra_fetch_attempt_ids':(['N-R03-MANUAL','N-R03-SOURCE'] if rid=='R03' else (['N-R04-MANUAL'] if rid=='R04' else (['N-R05-VIGNETTE'] if rid=='R05' else [])))}
 if rid=='R01':
  f='section-members/H-R01-text.txt';s=(P/f).read_text();st=s.index('Here we walk through');en=s.index('Contents',st)
  hsp=[cut(f,st,en,'BIO-H01',A['H-R01-ARCHIVE']['url'],'cleaned HTML','rnaseqGene/inst/doc/rnaseqGene.html')]
  hversion='rnaseqGene1.12.0 / Bioconductor3.11';hdate='vignette16October2019; packageDate/Publication2020-04-28'
  hsource=A['H-R01-ARCHIVE'];hmember='rnaseqGene/inst/doc/rnaseqGene.html';hpath='section-members/H-R01-rnaseqGene.html'
 elif rid=='R02':
  f='section-members/H-R02-IRanges-class.Rd';s=(P/f).read_text();st=s.index('\\description{');en=s.index('\\section{Constructor}',st)
  hsp=[cut(f,st,en,'BIO-H02',A['H-R02-ARCHIVE']['url'],'R documentation source','IRanges/man/IRanges-class.Rd')]
  hversion='IRanges2.22.0 / Bioconductor3.11';hdate='Date/Publication2020-04-27';hsource=A['H-R02-ARCHIVE'];hmember='IRanges/man/IRanges-class.Rd';hpath=f
 elif rid=='R03':
  f='section-members/H-R03-S4-utils.R';s=(P/f).read_text();st=s.index('setValidity2 <-');en=s.index('\nnew2 <-',st)
  hsource=A['R-EARLY-S4Vectors'];hmember='S4Vectors/R/S4-utils.R';hpath=f
  hsp=[cut(f,st,en,'BIO-H03',hsource['url'],'R source',hmember)]
  hversion='S4Vectors0.26.0 / Bioconductor3.11';hdate='Date/Publication2020-04-27'
 elif rid=='R04':
  f='section-members/H-R04-DESeqDataSet.Rd';s=(P/f).read_text();st=s.index('\\description{');en=s.index('\\details{',st)
  hsource=A['R-EARLY-DESeq2'];hmember='DESeq2/man/DESeqDataSet.Rd';hpath=f
  hsp=[cut(f,st,en,'BIO-H04',hsource['url'],'R documentation source',hmember)]
  hversion='DESeq2 1.28.0 / Bioconductor3.11';hdate='Date/Publication2020-04-27'
 elif rid=='R05':
  f='section-members/H-R05-SingleCellExperiment.Rd';s=(P/f).read_text();st=s.index('\\description{');en=s.index('\\details{',st)
  hsource=A['R-EARLY-SingleCellExperiment'];hmember='SingleCellExperiment/man/SingleCellExperiment.Rd';hpath=f
  hsp=[cut(f,st,en,'BIO-H05',hsource['url'],'R documentation source',hmember)]
  hversion='SingleCellExperiment1.10.0 / Bioconductor3.11';hdate='Date/Publication2020-04-27'
 else:
  f='section-members/H-R06-plotColData.Rd';s=(P/f).read_text();st=s.index('\\description{');en=s.index('\\details{',st)
  hsource=A['R-EARLY-scater'];hmember='scater/man/plotColData.Rd';hpath=f
  hsp=[cut(f,st,en,'BIO-H06',hsource['url'],'R documentation source',hmember)]
  hversion='scater1.16.0 / Bioconductor3.11';hdate='Date/Publication2020-04-27'
 hhead=f"Archived publisher material\nEdition: {hversion}\nPublisher date: {hdate}\nSource: {hsource['url']}\nMember: {hmember}\n"
 htext=hhead+'\n'+('\n[...]\n'.join(s['text'] for s in hsp)).strip()
 assert len(htext)<=1600,(rid,len(htext))
 H={'text':htext,'codepoints':len(htext),'utf8_bytes':len(htext.encode()),'sha256':sha(htext.encode()),
    'raw_excerpt':'\n[...]\n'.join(s['text'] for s in hsp),'spans':hsp,'source_ids':[hsp[0]['source_id']],
    'edition':hversion,'publisher_event_date':hdate,'queried_utc':hsource['finished_utc'],'read_utc':now(),
    'archive_url':hsource['url'],'archive_sha256':hsource['sha256'],'member':hmember,'member_sha256':sha((P/hpath).read_bytes()),
    'fetch_attempt_id':hsource['attempt_id'],'physical_fetch_reused_from_original_sampling':rid in ['R03','R04','R05','R06'],
    'contains_present_observation':False,'contains_collector_recommendation':False,'contains_answer_key':False,'empty_evidence':False,
    'shared_exact_excerpt_with_N':rid=='R03','semantic_overlap_with_N':rid in ['R02','R03','R04','R05','R06']}
 for k,obj in [('N',N),('H',H)]:
  (out/(rid+'-'+k+'.txt')).write_text(obj['text']);obj['exact_text_path']='components/'+rid+'-'+k+'.txt'
  for j,span in enumerate(obj['spans'],1):
   path='components/'+rid+'-'+k+'-source-'+str(j)+'.txt';(P/path).write_text(span['text']);span['committed_excerpt_path']=path
 nh.append({'ref_id':rid,'N':N,'H':H,'limitations':'Observations and excerpt construction only; no decisions/adjudication made.'})
(P/'evidence-components.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in nh))
print(json.dumps([{'ref_id':r['ref_id'],'Nchars':r['N']['codepoints'],'Hchars':r['H']['codepoints'],'HsameN':r['H']['shared_exact_excerpt_with_N']} for r in nh]))
