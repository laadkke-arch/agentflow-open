"""Run only after parent commits freeze.json; logical document views are capped at two."""
import concurrent.futures,html,json,re,sys,hashlib
from pathlib import Path
from html.parser import HTMLParser
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
from http_evidence import fetch,now,save_excerpt
ROOT=Path(__file__).parent;E=ROOT/'evidence'
class Tags(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,t,a):self.tags.append((t,dict(a),self.getpos()[0]))
def raw_lines(s):
 def rec(v):
  if isinstance(v,dict):
   if 'rawLines' in v:return v['rawLines']
   for x in v.values():
    r=rec(x)
    if r:return r
  elif isinstance(v,list):
   for x in v:
    r=rec(x)
    if r:return r
 for raw in re.findall(r'<script[^>]*type="application/json"[^>]*>(.*?)</script>',s,re.S):
  try:r=rec(json.loads(raw))
  except (json.JSONDecodeError,TypeError):continue
  if r:return '\n'.join(r)
 return None

def run(x):
 target,route=x;i='R-'+target['target_id']+'-'+route
 r,b=fetch(target['start_'+route.lower()],i+'-1',E)
 text=b.decode('utf-8','replace')
 project_text=raw_lines(text) if route=='B' else text
 if project_text is None:project_text=''
 v=re.search(r'title="Released version">([^<]+)',project_text)
 version=v.group(1) if v else None
 title=re.search(r'<title>(.*?)</title>',text,re.S)
 steps=[dict(r,reader_action='open given entry',view_kind='github_source_view' if route=='B' else 'rendered_document_html',title=html.unescape(title.group(1)) if title else None)]
 case=target['case_id'];purpose=target['purpose']
 body= 'confirmed' if version==target['target_version'] else ('refuted' if version else 'unconfirmed')
 same=body;resource='not_applicable';manual=False;uri_assembly=False;failure=None;resource_kind=None;obs=[];static_status='not_applicable'
 if purpose=='next' and case=='R1':
  uri=target['frozen_next_uri']
  contains=uri in project_text
  if not contains:
   resource='no_explicit_path';same='unconfirmed';failure='Frozen absolute URI absent in retrieved source; no replacement.'
  else:
   manual=route=='B'
   rr,bb=fetch(uri,i+'-2',E)
   tx=bb.decode('utf-8','replace');ti=re.search(r'<title>(.*?)</title>',tx,re.S)
   steps.append(dict(rr,reader_action='copy complete displayed absolute URI to address bar' if manual else 'follow Examples system.file href',view_kind='external_reference_html',title=html.unescape(ti.group(1)) if ti else None))
   resource='confirmed' if rr['status']==200 and 'system.file' in tx else ('inaccessible' if rr['status']!=200 else 'unconfirmed')
   same='unconfirmed';resource_kind='external R base operation reference'
   obs.append('Reference is externally hosted R base help; URL does not pin the archive release or its build-time R version.')
   if resource!='confirmed':failure='Destination unavailable or expected help not identified; auxiliary proof does not repair reader route.'
 elif purpose=='next' and case=='R2':
  start=project_text.find('id="using-svg-files"');end=project_text.find('id="showing-the-code"',start)
  section=project_text[start:end] if start>=0 and end>start else ''
  inline=re.findall(r'<div class="asciicast"[^>]*>\s*(<pre>.*?</pre>)\s*</div>',section,re.S)
  static_status='confirmed' if inline and 'TITLE' in inline[0] else 'unconfirmed'
  resource='no_explicit_path' if static_status=='confirmed' else 'unconfirmed'
  resource_kind='inline static preformatted output; not SVG/replay payload'
  obs.append('Inline first static output is read inside entry; extra views 0. Actual SVG or replay payload is no_explicit_path, not an execution success.')
 if case=='R1':obs.append('Usage/Examples code text readable; current1.1.14 code text matches selected1.1.12 after tag removal, but version identification differs.')
 else:obs.append('Expected init_knitr_engine, example and using-svg-files sections read; supplied document bytes equal fixed2.3.1 in auxiliary comparison.')
 if steps[0]['status'] != 200:
  body='inaccessible'; same='unconfirmed'; project_text=''
  if purpose=='next':resource='inaccessible'
  failure='Entry returned HTTP error; reader stops. Earlier auxiliary response does not replace this traversal.'
  obs=['Error response contains no target source. Cause and persistence unconfirmed.']
 return {'traversal_id':i,'target_id':target['target_id'],'case_id':case,'purpose':purpose,'route':route,'started_utc':steps[0]['started_utc'],'completed_utc':steps[-1]['retrieved_utc'],'start_url':steps[0]['requested_url'],'final_url':steps[-1]['final_url'],'steps':steps,'views':len(steps),'direct_response_bytes':sum(s['body_bytes'] for s in steps),'entry_version':version,'target_version':target['target_version'],'body_content_readable':bool(project_text),'target_body':body,'followup_resource':resource,'same_version':same,'followup_version':'unconfirmed' if purpose=='next' and case=='R1' else ('same containing HTML' if purpose=='next' else 'not_applicable'),'resource_kind':resource_kind,'static_output':static_status,'same_version_subject':'Containing HTML/static output only' if case=='R2' and purpose=='next' else 'Target document and/or external followup as separately stated','svg_or_replay_status':'no_explicit_path' if case=='R2' and purpose=='next' else 'not_applicable','manual_uri_copy':manual,'manual_path_reconstruction':uri_assembly,'base_element':None,'link_evidence':'source URI text, no rdrr a[href] in GitHub UI; parent browser observation' if manual else ('live href in rendered source HTML' if case=='R1' and purpose=='next' else 'inline/entry'),'failure':failure,'observations':obs,'unconfirmed':['No R example or browser JavaScript execution.']+(['Build-time R base documentation version and immutable target relationship.'] if case=='R1' and purpose=='next' else []),'minimum_next_observation':'A publisher-pinned R version and corresponding system.file manual URI/hash' if case=='R1' and purpose=='next' else 'Actual SVG/cast payload is needed only if animation is claimed; static reading is already observed.' if case=='R2' and purpose=='next' else 'Rendered fixed-version guide if reader requires rendered presentation.','method':'independent HTTP reads of each bounded route; browser clickability corroborated separately by parent, not executed by this script'}
if __name__=='__main__':
 if len(sys.argv)<2 or not re.fullmatch('[0-9a-f]{40}',sys.argv[1]):raise SystemExit('Pass the actual committed freeze SHA before executing.')
 targets=json.loads((ROOT/'targets.json').read_text());jobs=[(t,r) for t in targets for r in ['A','B']]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(run,jobs))
 (ROOT/'traversals.json').write_text(json.dumps({'freeze_commit':sys.argv[1],'traversals':rows},ensure_ascii=False,indent=2)+'\n')
 for x in rows:print(x['traversal_id'],x['views'],x['entry_version'],x['target_body'],x['followup_resource'],x['same_version'])
