"""Render only the already selected second-document responses; no network."""
import hashlib, importlib.util, json, re, sys
from pathlib import Path
from urllib.parse import unquote, urlsplit
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent.parent
SPEC=importlib.util.spec_from_file_location('pathprep',ROOT/'prepare_paths.py')
prep=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(prep)
renderer,renderer_hash=prep.local_renderer()
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def render(source):
 if source['status']=='access_failed':return source
 raw_path=BASE/source['raw_file'];raw=raw_path.read_bytes()
 assert sha(raw)==source['response_sha256'],source['source_id']
 if source.get('source_blob'):assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==source['source_blob']
 fragment=unquote(urlsplit(source['original_url']).fragment)
 if raw_path.suffix in {'.ts','.js','.json','.yaml','.yml','.py','.cpp','.h','.rs'}:
  visible=raw.decode();start=0;heading=None;anchor='headingless-code-start';serialization_sha=None
 else:
  markup,container=prep.content_html(raw_path,renderer);serialization_sha=sha(markup.encode())
  parser=renderer.Visible();parser.feed(markup);visible=''.join(parser.parts)
  heads=sorted((x for x in parser.items if x['tag'] in {'h1','h2','h3','h4','h5','h6'}),key=lambda x:x['start'])
  head=heads[0] if heads else None;start=head['start'] if head else 0;heading=prep.normalized(visible[head['start']:head['end']]) if head else None;anchor='first-heading' if head else 'headingless-document-start'
  if fragment:
   a=next((x for x in parser.items if x['attrs'].get('id')==fragment),None)
   if not a:return {**source,'status':'fragment_unresolved','fragment':fragment,'display_word_count':0,'window_file':None,'window_sha256':None}
   head=next((h for h in heads if h['start']<=a['start']<=h['end']),None)
   start=head['start'] if head else a['start'];heading=prep.normalized(visible[head['start']:head['end']]) if head else None;anchor='exact-fragment-derived-heading-id' if a['attrs'].get('data-af-derived-id') else 'exact-fragment-source-id'
 words=list(re.finditer(r'\S+',visible[start:]));n=min(500,len(words));a=start+words[0].start() if n else start;end=start+words[n-1].end() if n else start;text=visible[a:end]
 out=ROOT/'windows'/f"{source['source_id']}.txt";out.parent.mkdir(exist_ok=True);out.write_text(text+'\n')
 return {**source,'status':'window_ready' if n else 'empty_static_body','display_word_count':n,'window_file':str(out.relative_to(BASE)),'window_sha256':sha(text.encode()),'heading':heading,'anchor':anchor,'visible_character_range':[a,end],'container_serialization_sha256':serialization_sha,'renderer_sha256':renderer_hash,'read_status':'not_yet_directly_read'}

features={x['catalog_id']:x for x in load(BASE/'evidence/features-schema/features.json')}
plan=load(ROOT/'stage3-5d01a6208edd9f8a20be7b31f7b545cef2200597/prepared-paths.json')
github={x['id']:x for x in load(ROOT/'acquisition-github.json')}
http={x['id']:x for x in load(ROOT/'acquisition-http.json')}
sources={};edges=[]
def frozen_source(cid,sid,original):
 f=features[cid]
 return {'source_id':sid,'original_url':original,'fixed_url':f['fixed_url'],'implementation_sha':f['commit'],'version':f['version'],'raw_file':'evidence/features-schema/'+f['raw_cache']['path'],'response_sha256':f['raw_cache']['sha256'],'source_blob':f['raw_cache']['git_blob'],'status':'cached_response_reused','acquisition':'reuse frozen stage2 cache','acquisition_utc':f['windows'][0].get('retrieved_utc'),'source_role':'provider_document'}
for p in plan['providers']:
 cid=p['catalog_id'];sid='PS-'+cid+'-P1';src=frozen_source(cid,sid,p['original_destination_url'])
 src.update(window_file=p['window_file'],window_sha256=p['window_sha256'],display_word_count=p['display_word_count'],heading=p['first_heading'],status='window_ready',read_status='directly_read',reader='/root/features_schema',read_interval_utc=['2026-11-23T03:57:00Z','2026-11-23T03:59:00Z'])
 sources[sid]=src

def add_github(key,sid,original,role):
 r=github[key];s={'source_id':sid,'original_url':original,'fixed_url':r['fixed_url'],'implementation_sha':r['ref'],'version':'fixed commit '+r['ref'],'raw_file':'evidence/paths-schema/'+r['raw_file'],'response_sha256':r['response_sha256'],'source_blob':r['source_blob'],'status':'fetched','acquisition':'github_fetch_file base64','acquisition_utc':r['utc'],'source_role':role};sources[sid]=render(s);return sid
def add_http(key,sid,role):
 r=http[key];s={'source_id':sid,'original_url':r['original_url'],'fixed_url':r.get('fixed_url'),'implementation_sha':None,'version':'unversioned HTTP response; content hash fixed','raw_file':'evidence/paths-schema/'+r['raw_file'] if r.get('raw_file') else None,'response_sha256':r.get('response_sha256'),'source_blob':None,'status':r['status'],'acquisition':'urllib public HTTP GET','acquisition_utc':r['utc'],'last_modified':r.get('last_modified'),'source_role':role,'error':r.get('error')};sources[sid]=render(s);return sid

add_github('SUITE','PS-SUITE','https://github.com/json-schema-org/JSON-Schema-Test-Suite','independent_conformance_suite')
add_github('UNSUPPORTED','PS-CFW-UNSUPPORTED',github['UNSUPPORTED']['fixed_url'],'same_provider_code')
add_github('KR','PS-IMHONGLU-KR',github['KR']['fixed_url'],'same_provider_translation')
add_github('BENCH','PS-BENCH','https://github.com/ebdrup/json-schema-benchmark','independent_benchmark')
for key,role in [('AJV-DRAFT04','same_engine_live_docs_edition_unconfirmed'),('RFC8927','independent_standard'),('BOWTIE','independent_comparison_frontend'),('CORE-LATEST','independent_standard'),('JEDISON-DOCS','same_engine_live_docs_edition_unconfirmed'),('RFC6901','independent_standard')]:add_http(key,'PS-'+key,role)
for cid,fragment,sid in [('SC-008','overview','PS-BLAZE4J-OVERVIEW'),('SC-008','features','PS-BLAZE4J-FEATURES'),('SC-016','when-to-use-this-library','PS-EVERIT-WHEN')]:
 s=frozen_source(cid,sid,features[cid]['fixed_url']+'#'+fragment);s['fixed_url']=s['original_url'];sources[sid]=render(s)
sources['PS-SKEMA']=render(frozen_source('SC-015','PS-SKEMA','https://github.com/erosb/json-sKema'))
home=next(x for x in load(BASE/'evidence/root-paths/acquisition.json') if x['id']=='HOME')
sources['PS-HOME']=render({'source_id':'PS-HOME','original_url':'https://json-schema.org/','fixed_url':home['final_url'],'implementation_sha':None,'version':'homepage HTTP response','raw_file':'evidence/root-paths/raw/HOME.html','response_sha256':home['raw_sha256'],'source_blob':None,'status':'cached_response_reused','acquisition':'shared root HOME response','acquisition_utc':home['receipts'][0]['utc'],'source_role':'independent_standard_project_homepage'})
mapping={
 'SC-001':['PS-SUITE','PS-CFW-UNSUPPORTED'],
 'SC-004':['PS-SC-004-P1','PS-IMHONGLU-KR'],
 'SC-005':['PS-AJV-DRAFT04','PS-RFC8927'],
 'SC-006':['PS-SC-005-P1','PS-BENCH'],
 'SC-008':['PS-BLAZE4J-OVERVIEW','PS-BLAZE4J-FEATURES'],
 'SC-009':['PS-SUITE','PS-BOWTIE'],
 'SC-016':['PS-SKEMA','PS-EVERIT-WHEN'],
 'SC-021':['PS-HOME','PS-CORE-LATEST'],
 'SC-022':[], 'SC-023':['PS-HOME','PS-JEDISON-DOCS'], 'SC-024':[],
 'SC-027':['PS-HOME','PS-RFC6901']}
for p in plan['providers']:
 cid=p['catalog_id'];links=p['first_two_final'];assert len(links)==len(mapping[cid])
 for i in range(2):
  edges.append({'catalog_id':cid,'path_id':'P'+str(i+2),'selected_link':links[i] if len(links)>i else None,'second_source_id':mapping[cid][i] if len(mapping[cid])>i else None,'status':'selected_original_order' if len(links)>i else 'no_second_link_in_initial_window'})
(ROOT/'document-index.json').write_text(json.dumps(list(sources.values()),ensure_ascii=False,indent=2)+'\n')
(ROOT/'edge-index.json').write_text(json.dumps(edges,ensure_ascii=False,indent=2)+'\n')
for s in sources.values():print(s['source_id'],s['status'],s.get('display_word_count'),s.get('heading'))
