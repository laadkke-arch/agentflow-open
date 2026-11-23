from pathlib import Path
import json,re,subprocess,hashlib,datetime
from lxml import html
P=Path(__file__).parent
BLOCK=set('div p h1 h2 h3 h4 h5 h6 li ul ol dl dt dd blockquote pre table tr td th br section article header details summary'.split())
ALLOW={'features','feature','supported features','functionality','capabilities','operations','api','api reference','public api'}
def rst_markdown(t):
    t=re.sub(r'^\.\. image::.*(?:\n[ \t]+.*)*\n?','',t,flags=re.M)
    t=re.sub(r'^\.\. (?:code|code-block)::[^\n]*','',t,flags=re.M)
    t=re.sub(r'^(.+)\n([=\-~^]+)\s*$',lambda m:'## '+m[1],t,flags=re.M)
    t=re.sub(r'`([^`<>]+) <([^>]+)>`_+',r'[\1](\2)',t)
    t=re.sub(r':(?:function|class|meth|mod):`([^`]+)`', r'`\1`', t)
    t=t.replace('``','`')
    lines=t.splitlines(); out=[]; i=0
    while i<len(lines):
        line=lines[i]
        if line.strip()=='::':
            i+=1
            while i<len(lines) and not lines[i].strip(): i+=1
            code=[]
            while i<len(lines) and (not lines[i].strip() or lines[i].startswith('   ')):
                code.append(lines[i][3:] if lines[i].startswith('   ') else lines[i]); i+=1
            out += ['```']+code+['```']; continue
        out.append(line);i+=1
    t='\n'.join(out)
    return t
def render(raw,suffix):
    if suffix=='.html':return raw
    if suffix=='.rst':raw=rst_markdown(raw)
    js="import { marked } from '/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js'; import fs from 'node:fs'; process.stdout.write(marked.parse(fs.readFileSync(0,'utf8')));"
    return subprocess.check_output(['node','--input-type=module','-e',js],input=raw,text=True)
def window(raw,suffix,forced_fragment=None):
    doc=html.fragment_fromstring(render(raw,suffix),create_parent='div')
    if suffix=='.html':
        mains=doc.xpath('.//main') or doc.xpath('.//article')
        if mains: doc=mains[0]
    for el in doc.xpath('.//script|.//style|.//nav|.//footer|.//img|.//button|.//svg'):el.drop_tree()
    for el in doc.xpath('.//a'):
        if el.text_content().strip() in {'#','§'}:el.drop_tree()
    text=[];positions=[];headers=[]; links=[];offset=0; ids={}
    def add(s):
        nonlocal offset
        if s:text.append(s);offset+=len(s)
    def walk(el):
        tag=el.tag if isinstance(el.tag,str) else ''
        if not tag: return
        if tag in BLOCK:add('\n')
        start=offset
        if el.get('id'):ids[el.get('id')]=start
        if el.get('name'):ids[el.get('name')]=start
        if re.fullmatch('h[1-6]',tag):headers.append({'heading':' '.join(el.text_content().split()),'start':start,'id':el.get('id')})
        if el.text:add(el.text)
        for c in el:
            walk(c)
            if c.tail:add(c.tail)
        end=offset
        if tag=='a':links.append({'label':' '.join(el.text_content().split()),'href':el.get('href'),'start':start,'end':end})
        if tag in BLOCK:add('\n')
    walk(doc);full=''.join(text)
    def norm(h):return re.sub(r'^\s*\d+[.)\s]*','',h).strip().strip(':')
    qualified=[h for h in headers if norm(h['heading']).casefold() in ALLOW and not re.match(r'^(Installation|Benchmark|License|Contributing|Changelog|Supported drafts)\b',norm(h['heading']),re.I)]
    chosen=qualified[0] if qualified else (headers[0] if headers else {'heading':'NO_HEADING_DOCUMENT_START','start':0})
    start=chosen['start']
    if forced_fragment:
        frag=forced_fragment.lower().replace('_','-')
        hs=[h for h in headers if h.get('id')==forced_fragment or re.sub(r'[^\w\- ]','',h['heading'].lower()).replace(' ','-')==frag]
        if forced_fragment in ids:
            start=ids[forced_fragment];chosen={'heading':'fragment:'+forced_fragment,'start':start}
        elif hs:chosen=hs[0];start=chosen['start']
        else:return {'heading':'unresolved-fragment:'+forced_fragment,'feature_heading_found':False,'rendered_words':0,'text':'','links':[],'first_api_features_link':None,'boundary':'fragment missing in acquired response','rendering':'not-readable-at-specified-fragment'}
    words=list(re.finditer(r'\S+',full[start:]));end=start+(words[499].end() if len(words)>=500 else len(full[start:]))
    win=full[start:end].strip()
    visible=[x for x in links if x['start']>=start and x['start']<end]
    eligible=[x for x in visible if x['href'] and x['label'] and re.search(r'api|features?',x['label']+' '+x['href'],re.I) and not re.search(r'badge|shield|github.com/[^/]+/[^/]+/(?:actions|issues)',x['href'])]
    return {'heading':chosen['heading'],'feature_heading_found':bool(qualified),'rendered_words':len(win.split()),'text':win,'links':visible,'first_api_features_link':eligible[0] if eligible else None,'boundary':'first qualifying heading; otherwise first heading/document start; 500 rendered whitespace words','rendering':'marked GFM -> lxml visible block text; badges/images excluded; rst preconversion when applicable'}
def main():
    acq=json.loads((P/'acquisition.json').read_text())
    for id in ['LD-020','LD-021']:
        x=json.loads((P/(id+'-crate-metadata.json')).read_text());acq.append(x)
    out=[]
    (P/'windows').mkdir(exist_ok=True)
    for a in acq:
        if a.get('fetch_status')!='success':continue
        fp=Path(a['raw_file']); raw=fp.read_text(); w=window(raw,fp.suffix); w.update({k:a.get(k) for k in ['id','sha','version','fixed_url','read_utc','blob','repo','repository']});w['raw_sha256']=hashlib.sha256(raw.encode()).hexdigest()
        w['window_sha256']=hashlib.sha256(w['text'].encode()).hexdigest();w['window_file']='windows/'+a['id']+'.txt'
        (P/w['window_file']).write_text(w.pop('text')+'\n')
        out.append(w)
    (P/'window-metadata.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    for x in sorted(out,key=lambda a:(a['id'].startswith('LD'),a['id'])):
        print(x['id'],x['heading'],x['rendered_words'],'next='+str(x['first_api_features_link']) if not x['feature_heading_found'] else '')
if __name__=='__main__': main()

