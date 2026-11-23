import json,sys,re,hashlib,html
from pathlib import Path
from html.parser import HTMLParser
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
from http_evidence import now,save_excerpt
ROOT=Path(__file__).parent; E=ROOT/'evidence'; C=E/'raw'
class Tags(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,t,a):self.tags.append({'tag':t,'attrs':dict(a),'line':self.getpos()[0],'column':self.getpos()[1]})
def body(i):return (C/(i+'.bin')).read_text()
def receipt(i):return json.loads((E/(i+'.receipt.json')).read_text())
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
fixed1=body('R1-FIXED-HTML');fixed2=body('R2-FIXED-HTML')
s1=fixed1[fixed1.index('<div id="ref-examples">'):fixed1.index('<div class="col-md-3 hidden-xs hidden-sm"')]
s2=fixed2[fixed2.index('<h2 id="using-svg-files">'):fixed2.index('<h2 id="showing-the-code">')]
p1=Tags();p1.feed(s1);p2=Tags();p2.feed(s2)
first=next(x for x in p1.tags if x['tag']=='a' and x['attrs'].get('href','').startswith('http'))
inline=re.findall(r'<div class="asciicast"[^>]*>\s*(<pre>.*?</pre>)\s*</div>',s2,re.S)
assert first['attrs']['href']=='https://rdrr.io/r/base/system.file.html'
assert len(inline)==2
assert not [x for x in p2.tags if x['tag'] in ['svg','img','iframe','object','embed','script']]
freeze={'frozen_utc':now(),'phase':'before followup destinations requested','method':'public HTTP entity and HTML source/DOM inspection; browser execution not performed in this stream','R1':{'source_id':'R1-FIXED-HTML','source_sha256':receipt('R1-FIXED-HTML')['sha256'],'section':'#ref-examples','section_sha256':sha(s1),'selection':'first external operation reference in Examples; do not substitute local data.zip','first_operation_reference':first,'selected_next_uri':first['attrs']['href'],'base_element':None,'source_line':128,'uri_is_live_link_in_rendered_html':True,'uri_is_markup_text_on_github_source_view':True,'later_literal_file':'system.file(package = "archive", "extdata", "data.zip")','literal_local_file_is_web_link':False,'excluded_earlier_section':'Arguments options links occur before Examples but are outside the specified selection scope'},'R2':{'source_id':'R2-FIXED-HTML','source_sha256':receipt('R2-FIXED-HTML')['sha256'],'section':'#using-svg-files','section_sha256':sha(s2),'selected_next_uri':None,'base_element':None,'inline_payload_kind':'static preformatted output, not SVG XML, cast JSON, or player payload','first_inline_sha256':sha(inline[0]),'first_inline_bytes':len(inline[0].encode()),'inline_payload_count':2,'additional_document_views':0,'svg_or_replay_candidate':'no_explicit_path','first_link_in_section':'https://rdrr.io/r/base/options.html','first_link_exclusion':'option-function documentation is not SVG/replay asset; do not replace target','later_reference':'../reference/init_knitr_engine.html','later_reference_exclusion':'Showing the code is after Using SVG files and not the target asset','not_proved':['SVG payload','animation','JavaScript player execution','full example success']}}
(ROOT/'freeze.json').write_text(json.dumps(freeze,ensure_ascii=False,indent=2)+'\n')
urls={
'R1':('https://archive.r-lib.org/reference/archive_read.html','https://github.com/r-lib/archive/blob/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html'),
'R2':('https://asciicast.r-lib.org/articles/asciicast-demo.html','https://github.com/r-lib/asciicast/blob/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html')}
rows=[]
for case,version in [('R1','1.1.12'),('R2','2.3.1')]:
 for purpose in ['body','next']:
  rows.append({'target_id':case+'-'+purpose,'case_id':case,'purpose':purpose,'target_version':version,'section':'#ref-usage;#ref-examples' if case=='R1' else '#example;#using-svg-files','start_a':urls[case][0],'start_b':urls[case][1],'basis_source_ids':[case+'-DESCRIPTION',case+'-FIXED-HTML'],'owner_promise':'DESCRIPTION gives project documentation root; fixed article supplies example. No permanent historical host guarantee found in these inputs.','research_condition':'Read selected historical release now; compare service versus fixed GitHub HTML file within two document/resource views.','frozen_next_uri':freeze[case]['selected_next_uri'] if purpose=='next' else None,'inline_extra_views':0 if case=='R2' else None,'success_criterion':'Specified version and section identified' if purpose=='body' else ('First Examples operation reference readable; version linkage separately established' if case=='R1' else 'Read available inline output; actual SVG/replay payload absence remains separate and is not counted as animation success'),'selection_detail':freeze[case],'unconfirmed':'browser UI/Raw navigation to be observed by primary agent; no R/JS execution'})
(ROOT/'targets.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
sources=[]
for case in ['R1','R2']:
 for suffix in ['ENTRY-A','ENTRY-B','FIXED-HTML','DESCRIPTION']:
  i=case+'-'+suffix;r=receipt(i);s=body(i)
  fixed=case+'-FIXED-HTML';version=('1.1.14' if suffix=='ENTRY-A' else '1.1.12') if case=='R1' else '2.3.1'
  is_duplicate=suffix=='ENTRY-B' or (suffix=='ENTRY-A' and case=='R2')
  obs={'ENTRY-A':f'HTTP200; rendered documentation HTML declares released version {version}; section IDs retained. '+('Differs from selected1.1.12 file.' if case=='R1' else 'Entire response equals selected fixed HTML bytes.'),'ENTRY-B':'GitHub source-view HTML has embedded rawLines and an explicit Raw button; wrapper MIME text/html is not the project rendered documentation.','FIXED-HTML':f'Fixed generated HTML declares {version}; '+('Examples first operation link is system.file on rdrr.io, with data.zip only a local R path expression.' if case=='R1' else 'Using SVG files has inline static pre output; contains no svg/img/player/script resource in the section.'),'DESCRIPTION':f'Package Version is {version}; URL points to project documentation root; no release-specific reader retention duration in this file.'}[suffix]
  excerpt=({'R1':'system.file(package = "archive", "extdata", "data.zip")','R2':'options(asciicast_knitr_svg = TRUE)'}[case] if suffix in ['FIXED-HTML','ENTRY-A'] else ('Version: '+version if suffix=='DESCRIPTION' else 'Raw'))
  source={'source_id':i,'work_id':case+'-'+('DESCRIPTION' if suffix=='DESCRIPTION' else 'ARTICLE'),'lineage_id':case+'-publisher','category':'publisher_source','original_url':r['requested_url'],'published_utc':None,'retrieved_utc':r['retrieved_utc'],'version':version,'location':('DESCRIPTION Version/URL' if suffix=='DESCRIPTION' else ('reference/archive_read.html #ref-usage #ref-examples' if case=='R1' else 'articles/asciicast-demo.html #example #using-svg-files')),'questions':['Q1','Q2','Q3','Q4','Q5'],'cases':[case],'observation':obs,'excerpt':excerpt,'fingerprint':{'sha256':r['sha256'],'git_blob_sha1':r['git_blob_sha1'],'body_bytes':r['body_bytes'],'content_type':r['content_type']},'support_refute':'supports bounded content identification; refutes assuming a filename/source wrapper implies rendered or executable example','limitations':'Current HTTP/DOM observation only. No browser JS/R execution. Published UTC not directly provided by this response; Last-Modified is receipt metadata only. '+('Duplicate manifestation; excluded from unique minimum.' if is_duplicate else ''),'reread_url':r['requested_url'],'eligible':r['status']==200 and not is_duplicate,'duplicate_of':fixed if is_duplicate else None,'receipt_path':str((E/(i+'.receipt.json')).relative_to(ROOT.parents[1])),'excerpt_path':str((E/(i+'.excerpt.json')).relative_to(ROOT.parents[1]))}
  sources.append(source);save_excerpt(E,i,obs,[excerpt])
(ROOT/'sources.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in sources))
print(json.dumps({'targets':len(rows),'sources':len(sources),'eligible':sum(s['eligible'] for s in sources),'freeze':str(ROOT/'freeze.json')},ensure_ascii=False))
