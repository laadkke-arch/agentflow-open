#!/usr/bin/env python3
"""Mechanically capture and map fixed upstream manuals, without semantic selection.

Modes: --toc-only prepares maker-visible headings before gold reading;
--capture-im captures every top-level www/*.html at each fixed ImageMagick commit;
--build creates the corpus and the excluded-link/mapping ledgers from those files.
"""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import posixpath
import re
import subprocess
import sys
import time
from urllib.parse import unquote, urljoin, urlsplit

BASE=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE))
from fetch_public import fetch

PANDOC=[('2.19.2','p2192'),('2.14.0.3','p21403'),('3.8.3','p383')]
IM=[('7.1.1-3','i7113'),('7.1.1-4','i7114'),('7.1.1-6','i7116')]
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
BLOCK={'address','article','aside','blockquote','dd','details','div','dl','dt','figcaption','figure','h1','h2','h3','h4','h5','h6','header','hr','li','main','ol','p','pre','section','summary','table','tbody','tfoot','thead','tr','ul'}
SKIP={'head','script','style','noscript','iframe','form','svg','canvas'}


def utc():return datetime.now(timezone.utc).isoformat()
def sha(raw):return hashlib.sha256(raw if isinstance(raw,bytes) else raw.encode()).hexdigest()
def dump(path,data):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def commit(project,version):return json.loads((BASE/'documents/metadata'/f'{project}-{version}-commit.json').read_text())['sha']


class Node:
    def __init__(self,tag,attrs=None,parent=None,line=1,col=0,data=None):
        self.tag=tag;self.attrs=dict(attrs or []);self.parent=parent;self.children=[];self.line=line;self.col=col;self.data=data
    def walk(self):
        yield self
        for c in self.children:yield from c.walk()
    def text(self):return ''.join(n.data or '' for n in self.walk() if n.tag=='#text')


class Tree(HTMLParser):
    def __init__(self,html):
        super().__init__(convert_charrefs=True)
        self.root=Node('#root');self.stack=[self.root];self.feed(html);self.close()
    def handle_starttag(self,tag,attrs):
        line,col=self.getpos();n=Node(tag,attrs,self.stack[-1],line,col);self.stack[-1].children.append(n)
        if tag not in VOID:self.stack.append(n)
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if tag not in VOID:self.stack.pop()
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==tag:self.stack=self.stack[:i];break
    def handle_data(self,data):
        line,col=self.getpos();self.stack[-1].children.append(Node('#text',parent=self.stack[-1],line=line,col=col,data=data))


def descendants(root,tag=None):return [n for n in root.walk() if tag is None or n.tag==tag]
def normalize(s):return re.sub(r'\s+',' ',s).strip()
def content_root(tree,project):
    if project=='imagemagick':
        ms=descendants(tree.root,'main')
        if ms:return ms[0],'first_main'
    bs=descendants(tree.root,'body')
    return (bs[0] if bs else tree.root),'body_without_site_chrome'


def toc_nodes(root,project):
    if project=='pandoc':
        nav=next((x for x in root.walk() if x.tag=='nav' and x.attrs.get('id')=='TOC'),None)
        return [nav] if nav else []
    # Official ImageMagick entry pages place their actual jump list in a centered
    # paragraph within magick-header. Only that markup is considered its TOC.
    result=[]
    for n in root.walk():
        if n.tag=='p' and 'text-center' in n.attrs.get('class','').split():
            links=[a for a in n.walk() if a.tag=='a' and urlsplit(a.attrs.get('href','')).fragment]
            if links:result.append(n)
    return result


def skipped(n,project):
    classes=n.attrs.get('class','').lower()
    if n.tag in SKIP or 'adsbygoogle' in classes or n.attrs.get('role')=='advertisement':return True
    if project=='imagemagick' and n.tag in ('nav','footer'):return True
    return False


def render_pandoc():
    receipts=[]
    version=subprocess.check_output(['pandoc','--version'],text=True).splitlines()[0]
    for v,prefix in PANDOC:
        d=BASE/'documents/pandoc'/v;inp=d/'MANUAL.txt';out=d/'MANUAL.rendered.html';rpath=d/'MANUAL.rendered.html.build.json'
        if out.exists() and rpath.exists():receipts.append(json.loads(rpath.read_text()));continue
        command=['pandoc','--from=markdown','--to=html5','--standalone','--toc',str(inp),'--output',str(out)]
        at=utc();tic=time.monotonic();r=subprocess.run(command,capture_output=True,text=True)
        receipt={'mode':'machine_render_no_semantic_read','started_utc':at,'finished_utc':utc(),'wall_seconds':time.monotonic()-tic,'command':command,'exit_code':r.returncode,'stderr':r.stderr,'renderer':version,'input_sha256':sha(inp.read_bytes()),'output_sha256':sha(out.read_bytes()) if out.exists() else None,'limitation':'historical official MANUAL.txt rendered by locally installed pandoc 3.1.11.1; not captured historical public HTML; default TOC depth=3; no historical CSS/layout claim'}
        dump(rpath,receipt);receipts.append(receipt)
        if r.returncode:raise RuntimeError('Pandoc rendering failed; see preserved stderr')
    return receipts


def make_toc_only():
    receipts=render_pandoc();rows=[]
    for project,items in [('pandoc',PANDOC),('imagemagick',IM)]:
        for v,prefix in items:
            path=BASE/'documents'/project/v/('MANUAL.rendered.html' if project=='pandoc' else 'command-line-processing.html')
            raw=path.read_text();tree=Tree(raw);root,basis=content_root(tree,project)
            selected=toc_nodes(root,project);entries=[]
            for section in selected:
                for a in section.walk():
                    if a.tag=='a' and urlsplit(a.attrs.get('href','')).fragment:
                        entries.append({'label':normalize(a.text()),'anchor':unquote(urlsplit(a.attrs['href']).fragment),'original_href':a.attrs['href'],'source_html_line':a.line,'source_html_column':a.col})
            rows.append({'project':project,'version':v,'start_doc_id':prefix if project=='pandoc' else prefix+'_processing','start_url':'https://pandoc.org/MANUAL.html' if project=='pandoc' else 'https://imagemagick.org/script/command-line-processing.php','fixed_commit':commit(project,v),'input_file':str(path.relative_to(BASE)),'input_sha256':sha(raw),'toc_extraction':'generated nav#TOC in source heading order' if project=='pandoc' else 'official magick-header p.text-center fragment-link list, original order','entries':entries,'machine_extracted_utc':utc(),'semantic_body_read_by_maker':False})
    data={'schema':1,'purpose':'packet author sees headings/anchors only; no body, gold, recommendation, or witness path','created_utc':utc(),'documents':rows,'render_receipts':[str((BASE/'documents/pandoc'/v/'MANUAL.rendered.html.build.json').relative_to(BASE)) for v,p in PANDOC]}
    dump(BASE/'documents/TOC_ONLY.json',data)
    print(json.dumps({'toc_only_file':'documents/TOC_ONLY.json','documents':len(rows),'toc_items':{x['start_doc_id']:len(x['entries']) for x in rows}},ensure_ascii=False))


def capture_im():
    jobs=[];tree_receipts=[]
    for v,prefix in IM:
        c=commit('imagemagick',v);rel=f'documents/metadata/imagemagick-{v}-tree.json';path=BASE/rel
        if path.exists():raw=path.read_bytes();receipt=json.loads(path.with_name(path.name+'.receipt.json').read_text())
        else:raw,receipt=fetch(f'https://api.github.com/repos/ImageMagick/ImageMagick/git/trees/{c}?recursive=1',rel)
        tree_receipts.append(receipt)
        if raw is None:continue
        tree=json.loads(raw)
        if tree.get('truncated'):raise RuntimeError('upstream tree truncated; no complete allowlist')
        allowed=[x for x in tree['tree'] if x['type']=='blob' and re.fullmatch(r'www/[^/]+\.html',x['path'])]
        dump(BASE/'documents/metadata'/f'imagemagick-{v}-allowlist.json',{'version':v,'commit':c,'rule':'all direct www/*.html blobs; no subdirectories/API docs','tree_sha':tree.get('sha'),'tree_truncated':False,'files':allowed,'fixed_utc':utc(),'semantic_selection':False})
        for x in allowed:
            rel=f'documents/imagemagick/{v}/'+x['path'].split('/')[-1]
            if (BASE/rel).exists() and (BASE/(rel+'.receipt.json')).exists():continue
            jobs.append((f'https://raw.githubusercontent.com/ImageMagick/ImageMagick/{c}/{x["path"]}',rel))
    results=[]
    with ThreadPoolExecutor(max_workers=12) as ex:
        futures={ex.submit(fetch,url,rel):rel for url,rel in jobs}
        for fut in as_completed(futures):
            raw,receipt=fut.result();results.append(receipt)
            if len(results)%25==0:print(json.dumps({'captured_or_failed':len(results),'planned_fetches':len(jobs)}),flush=True)
    data={'method':'mechanical_fixed_tree_allowlist_capture','completed_utc':utc(),'semantic_read_count':0,'new_fetch_attempts':len(jobs),'successful_new_fetches':sum(r.get('status')==200 for r in results),'failed_new_fetches':sum(r.get('status')!=200 for r in results),'tree_receipts':tree_receipts,'capture_receipt_files':[r['output']+'.receipt.json' for r in results]}
    dump(BASE/'documents/metadata/imagemagick-capture.json',data)
    print(json.dumps({k:data[k] for k in ['new_fetch_attempts','successful_new_fetches','failed_new_fetches']}))


class Converter:
    def __init__(self,root,project,did,source_file,link_prefix):
        self.root=root;self.project=project;self.did=did;self.source_file=source_file;self.link_prefix=link_prefix;self.parts=[];self.length=0;self.links=[];self.anchors={};self.mapping=[];self.nav=[];self.excluded=[];self.images=[];self.tocs=set(toc_nodes(root,project));self.link_count=0
    def emit(self,text,node,kind='source_text'):
        if not text:return
        start=self.length;self.parts.append(text);self.length+=len(text)
        self.mapping.append({'plain_start':start,'plain_end':self.length,'html_line':node.line,'html_column':node.col,'html_tag':node.tag,'kind':kind})
    def last(self):return self.parts[-1][-1] if self.parts else ''
    def br(self,node):
        if self.parts and self.last()!='\n':self.emit('\n',node,'block_separator')
    def walk(self,n,pre=False):
        if n.tag=='#text':
            s=n.data if pre else re.sub(r'\s+',' ',n.data)
            if not pre and (not self.parts or self.last().isspace()):s=s.lstrip()
            self.emit(s,n);return
        if skipped(n,self.project):
            self.excluded.append({'kind':'excluded_markup','tag':n.tag,'line':n.line,'column':n.col,'reason':'script/style/non-text canvas/site chrome/ad/form'});return
        if n.tag in BLOCK:self.br(n)
        for key in ('id','name'):
            if n.attrs.get(key):
                self.anchors.setdefault(n.attrs[key],self.length)
        nav_start=self.length if n in self.tocs else None
        if n.tag=='br':self.br(n);return
        if n.tag=='img':
            alt=n.attrs.get('alt','')
            if alt:self.emit(alt,n,'image_alt_only')
            self.images.append({'src':n.attrs.get('src'),'alt':alt,'line':n.line,'column':n.col,'rendered_pixels':False});return
        if n.tag=='a' and 'href' in n.attrs:
            self.link_count+=1;lid=f'{self.link_prefix}l{self.link_count}'
            start=self.length;marker=f'[{lid}] ';self.emit(marker,n,'inserted_link_id')
            self.nav.append({'start':start,'end':self.length})
            content_start=self.length
            for c in n.children:self.walk(c,pre)
            label=''.join(self.parts)[content_start:self.length].strip()
            if not label:
                # Image-only/empty links cannot supply a meaningful visible label.
                self.excluded.append({'kind':'empty_label_link','href':n.attrs['href'],'line':n.line,'column':n.col,'marker_start':start})
            self.links.append({'id':lid,'start':start,'end':self.length,'label':label,'href':n.attrs['href'],'html_line':n.line,'html_column':n.col})
        else:
            for c in n.children:self.walk(c,pre or n.tag=='pre')
        if n.tag in BLOCK:self.br(n)
        elif n.tag in ('td','th'):self.emit('\t',n,'table_cell_separator')
        if nav_start is not None and self.length>nav_start:self.nav.append({'start':nav_start,'end':self.length})
    def convert(self):
        self.walk(self.root);return ''.join(self.parts)


def corpus_sources():
    result=[]
    for v,prefix in PANDOC:
        result.append({'project':'pandoc','version':v,'prefix':prefix,'id':prefix,'file':BASE/'documents/pandoc'/v/'MANUAL.rendered.html','url':'https://pandoc.org/MANUAL.html','upstream_path':'MANUAL.html','commit':commit('pandoc',v)})
    for v,prefix in IM:
        allow=json.loads((BASE/'documents/metadata'/f'imagemagick-{v}-allowlist.json').read_text())
        for x in allow['files']:
            name=x['path'].split('/')[-1];p=BASE/'documents/imagemagick'/v/name
            if not p.exists():continue
            stem=Path(name).stem
            did=prefix+('_processing' if name=='command-line-processing.html' else '_'+re.sub(r'[^A-Za-z0-9_-]','_',stem))
            # The input schema deliberately keeps identifiers short.
            if len(did)>38:did=prefix+'_'+sha(name)[:12]
            result.append({'project':'imagemagick','version':v,'prefix':prefix,'id':did,'file':p,'url':'https://imagemagick.org/script/'+stem+'.php','upstream_path':name,'commit':allow['commit'],'git_blob_sha':x['sha']})
    return result


def build():
    started=utc();tic=time.monotonic();sources=corpus_sources();docs=[];conversion={};excluded=[];index={}
    for doc_index,src in enumerate(sources,1):
        raw=src['file'].read_text();tree=Tree(raw);root,basis=content_root(tree,src['project'])
        cv=Converter(root,src['project'],src['id'],str(src['file'].relative_to(BASE)),f'n{doc_index}');txt=cv.convert();conversion[src['id']]=cv
        receipt_path=(src['file'].parent/'MANUAL.txt.receipt.json') if src['project']=='pandoc' else src['file'].with_name(src['file'].name+'.receipt.json')
        transport=json.loads(receipt_path.read_text())
        doc={'id':src['id'],'url':src['url'],'version':src['version'],'source_sha':sha(src['file'].read_bytes()),'upstream_commit':src['commit'],'source_file':str(src['file'].relative_to(BASE)),'capture_receipt':str(receipt_path.relative_to(BASE)),'upstream_source_url':transport.get('original_url'),'observed_source_arrival_url':transport.get('arrived_url'),'machine_capture_completed_utc':transport.get('finished_utc'),'text':txt,'links':[],'anchors':cv.anchors,'navigation_spans':cv.nav,'content_selection':basis,'source_transform':'pandoc 3.1.11.1 rendered historical MANUAL.txt, then offline DOM plain text' if src['project']=='pandoc' else 'fixed official HTML main content to offline DOM plain text','image_omissions':cv.images}
        docs.append(doc);index[(src['project'],src['version'],src['upstream_path'])]=doc
    byid={d['id']:d for d in docs}
    for src in sources:
        doc=byid[src['id']];cv=conversion[src['id']]
        for link in cv.links:
            href=link['href'];parsed=urlsplit(href);fragment=unquote(parsed.fragment)
            target_doc=None;reason=None
            if not link['label']:reason='empty visible label'
            elif parsed.scheme in ('mailto','javascript','data'):reason='not a document navigation URL'
            elif src['project']=='pandoc':
                resolved=urlsplit(urljoin(src['url'],href))
                if resolved.netloc in ('pandoc.org','www.pandoc.org') and resolved.path in ('/MANUAL.html','/MANUAL'):target_doc=doc
                else:reason='outside sealed Pandoc main-manual-only allowlist; linked doc/example/spec not captured'
            else:
                resolved=urlsplit(urljoin(src['url'],href));path=resolved.path
                if resolved.netloc not in ('imagemagick.org','www.imagemagick.org','legacy.imagemagick.org'):reason='external publisher or non-document host'
                elif '/api/' in path:reason='API subdirectory excluded by mechanical top-level www allowlist'
                else:
                    filename=posixpath.basename(path)
                    if filename.endswith('.php'):filename=filename[:-4]+'.html'
                    elif not filename:filename='index.html'
                    target_doc=index.get(('imagemagick',src['version'],filename))
                    if target_doc is None:reason='not a successfully captured top-level HTML document'
            if target_doc is not None and fragment and fragment not in target_doc['anchors']:
                reason='target fragment absent from frozen converted document';target_doc=None
            if reason is not None:
                excluded.append({'source_doc':src['id'],'source_file':str(src['file'].relative_to(BASE)),**link,'resolved_url':urljoin(src['url'],href),'reason':reason,'clickable':False})
            else:
                doc['links'].append({k:link[k] for k in ('id','start','end','label')}|{'target_doc':target_doc['id'],'target_offset':target_doc['anchors'].get(fragment,0),'fragment':fragment,'original_href':href,'html_line':link['html_line'],'html_column':link['html_column']})
        mapping_path=BASE/'documents/mappings'/f'{src["id"]}.json'
        dump(mapping_path,{'doc_id':src['id'],'source_file':doc['source_file'],'source_sha256':doc['source_sha'],'text_sha256':sha(doc['text']),'plain_unicode_offsets':True,'source_coordinate_kind':'HTMLParser original start line/column of source text node or tag; whitespace/entity normalization maps a whole emitted span to that node, not a one-to-one character map','mappings':cv.mapping,'anchors':cv.anchors,'excluded_markup':cv.excluded,'images':cv.images})
    # Excluded link labels remain source text, but their inserted IDs must not
    # look like selectable IDs. Remove only the generated [ID] prefix and shift
    # all source mappings/anchors/links/nav spans accordingly, preserving words.
    # Keeping raw identifiers would falsely advertise non-captured destinations.
    corrections=[]
    for doc in docs:
        bad=[e for e in excluded if e['source_doc']==doc['id']]
        cuts=sorted([(e['start'],e['start']+len('['+e['id']+'] ')) for e in bad])
        if not cuts:continue
        def shift(x):return x-sum(max(0,min(x,b)-a) for a,b in cuts if x>a)
        text=doc['text'];chunks=[];cursor=0
        for a,b in cuts:chunks.append(text[cursor:a]);cursor=b
        chunks.append(text[cursor:]);doc['text']=''.join(chunks)
        for x in doc['links']:x['start']=shift(x['start']);x['end']=shift(x['end'])
        doc['anchors']={k:shift(v) for k,v in doc['anchors'].items()}
        doc['navigation_spans']=[{'start':shift(x['start']),'end':shift(x['end'])} for x in doc['navigation_spans'] if shift(x['end'])>shift(x['start'])]
        mp=BASE/'documents/mappings'/f'{doc["id"]}.json';m=json.loads(mp.read_text())
        m['mappings']=[{**x,'plain_start':shift(x['plain_start']),'plain_end':shift(x['plain_end'])} for x in m['mappings'] if shift(x['plain_end'])>shift(x['plain_start'])]
        m['anchors']=doc['anchors'];m['text_sha256']=sha(doc['text']);m['removed_generated_link_markers']=[{'start_before':a,'end_before':b} for a,b in cuts];dump(mp,m)
        corrections.append({'doc_id':doc['id'],'removed_marker_count':len(cuts)})
        for e in bad:e['plain_start_after_marker_removal']=shift(e['start']);e['plain_end_after_marker_removal']=shift(e['end'])
    # Target offsets must use the finally shifted anchor maps of destination docs.
    for doc in docs:
        for link in doc['links']:
            target=byid[link['target_doc']];link['target_offset']=target['anchors'].get(link.get('fragment',''),0)
    corpus={'schema':1,'documents':docs}
    dump(BASE/'corpus.json',corpus)
    (BASE/'corpus.json.gz').write_bytes(gzip.compress((BASE/'corpus.json').read_bytes(),mtime=0))
    (BASE/'documents/catalog.jsonl').write_text(''.join(json.dumps({k:d[k] for k in ['id','url','version','source_file','source_sha','upstream_commit','capture_receipt','upstream_source_url','observed_source_arrival_url','machine_capture_completed_utc','content_selection','source_transform']}|{'characters':len(d['text']),'clickable_links':len(d['links']),'anchors':len(d['anchors']),'mechanical_capture_not_semantic_read':True},ensure_ascii=False)+'\n' for d in docs))
    (BASE/'documents/excluded-links.jsonl').write_text(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in excluded))
    from reader import Corpus
    loaded=Corpus.load(BASE/'corpus.json.gz')
    starts=[p for v,p in PANDOC]+[p+'_processing' for v,p in IM]
    for did in starts:loaded.render(did,0)
    receipt={'method':'mechanical_capture_and_DOM_mapping_no_semantic_selection','started_utc':started,'finished_utc':utc(),'wall_seconds':time.monotonic()-tic,'corpus_file':'corpus.json.gz','corpus_sha256':loaded.sha256,'corpus_gzip_bytes':(BASE/'corpus.json.gz').stat().st_size,'corpus_json_bytes':(BASE/'corpus.json').stat().st_size,'gzip_mtime':0,'source_documents':len(docs),'start_doc_ids':starts,'clickable_links':sum(len(d['links']) for d in docs),'excluded_links':len(excluded),'source_text_codepoints':sum(len(d['text']) for d in docs),'source_html_coordinates_preserved':True,'machine_captured_not_semantically_read':True,'natural_or_independent_reader_trials':0,'allowlist':{'pandoc':'Only each fixed MANUAL.txt rendered locally; all other manual-linked documents, examples, and external specifications are excluded and logged.','imagemagick':'Every successfully captured direct www/*.html at each fixed upstream commit; API/subdirectories and external resources excluded.'},'limitations':['Plain text with original order and inserted IDs; not native-browser layout.','Pandoc uses installed 3.1.11.1 renderer on historical manual sources, default TOC depth 3; historical HTML/CSS not reconstructed.','HTML entities and whitespace normalized; source-node line/column mapping is exact but per-character reverse mapping after normalization is not one-to-one.','Pixels/diagrams not rendered; img alt text only and omissions logged.','A missing link target or absent fragment is not clickable and is an allowlist limitation, not proof the full official web manual lacks a path.','All captured pages require later human/AI semantic reading before counting as directly-read primary works.'],'removed_marker_receipts':corrections,'builder_sha256':sha(Path(__file__).read_bytes())}
    dump(BASE/'viewer/corpus-build.json',receipt)
    print(json.dumps({k:receipt[k] for k in ['source_documents','start_doc_ids','clickable_links','excluded_links','corpus_sha256']}))


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--toc-only',action='store_true');p.add_argument('--capture-im',action='store_true');p.add_argument('--build',action='store_true');a=p.parse_args()
    if not any((a.toc_only,a.capture_im,a.build)):p.error('choose a mode')
    if a.toc_only:make_toc_only()
    if a.capture_im:capture_im()
    if a.build:build()


if __name__=='__main__':main()
