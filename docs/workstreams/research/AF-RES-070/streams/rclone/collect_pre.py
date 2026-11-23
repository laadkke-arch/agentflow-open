"""Read issue initial bodies; never print comment objects or outcome metadata."""
import concurrent.futures, datetime, hashlib, html, json, pathlib, re, urllib.request

BASE = pathlib.Path(__file__).resolve().parents[2]
PRIVATE = BASE / 'private' / 'rclone'
OUT = BASE / 'streams' / 'rclone'

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')

def get(url):
    at = utc()
    try:
        req=urllib.request.Request(url, headers={'User-Agent':'AF-RES-070-public-research','Accept':'application/vnd.github+json' if 'api.github.com' in url else 'text/html'})
        with urllib.request.urlopen(req,timeout=35) as r:
            data=r.read()
            return {'url':url,'accessed_utc':at,'status':r.status,'sha256':hashlib.sha256(data).hexdigest(),'body':data.decode('utf-8')}
    except Exception as exc:
        return {'url':url,'accessed_utc':at,'status':'failure','error':type(exc).__name__+': '+str(exc)}

def collect(row):
    n=row['number']
    api=get(f'https://api.github.com/repos/rclone/rclone/issues/{n}')
    (PRIVATE/f'issue-{n}-rest.json').write_text(json.dumps(api,ensure_ascii=False,indent=2))
    page=get(f'https://github.com/rclone/rclone/issues/{n}')
    (PRIVATE/f'issue-{n}.html').write_text(page.get('body',''))
    d=json.loads(api['body']) if api.get('status')==200 else None
    info={'number':n,'api_status':api['status'],'html_status':page['status'],'rest_accessed_utc':api['accessed_utc'],'html_accessed_utc':page['accessed_utc'],'html_sha256':page.get('sha256')}
    if d:
        body=d.get('body') or ''
        (PRIVATE/f'issue-{n}-body.txt').write_bytes(body.encode())
        info.update({'author':d['user']['login'],'created_at':d['created_at'],'body_sha256':hashlib.sha256(body.encode()).hexdigest(),'body_lines':len(body.splitlines()),'body_characters':len(body)})
    if page.get('status')==200:
        s=page['body']; a=s.find('data-testid="issue-body"'); b=s.find('id="issue-body-viewer"',a); header=s[a:b] if a>=0 and b>=0 else ''
        info.update({'initial_header_present':bool(header),'initial_header_edited_text':bool(re.search(r'>\s*edited\s*<',header,re.I)),'initial_header_text':html.unescape(re.sub('<[^>]*>',' ',header)).strip(),'edits_section':re.findall(r'<div[^>]*class="[^"]*editsSection[^>]*>([\s\S]*?)</div>',header)})
        for attrs,raw in re.findall(r'<script([^>]*)>([\s\S]*?)</script>',s):
            if 'react-app.embeddedData' not in attrs:continue
            try:i=json.loads(raw)['payload']['issueViewerRoute']['data']['repository']['issue']
            except (KeyError,json.JSONDecodeError):continue
            info.update({'initial_payload_number':i.get('number'),'lastEditedAt_key_present':'lastEditedAt' in i,'lastEditedAt':i.get('lastEditedAt'),'lastUserContentEdit_key_present':'lastUserContentEdit' in i,'lastUserContentEdit':i.get('lastUserContentEdit'),'bodyVersion':i.get('bodyVersion'),'html_body_matches_rest':i.get('body')==d.get('body') if d else None})
    (PRIVATE/f'issue-{n}-pre-meta.json').write_text(json.dumps(info,ensure_ascii=False,indent=2))
    accesses=[]
    for source in [api,page]:
        accesses.append({k:v for k,v in source.items() if k!='body'}|{'stage':'A-before-seal','comment_text_exposed':False,'number':n})
    return info,accesses

if __name__=='__main__':
    import sys
    rows=json.loads((PRIVATE/'queue-first16.json').read_text())['rows']
    start=int(sys.argv[1]) if len(sys.argv)>1 else 1; stop=int(sys.argv[2]) if len(sys.argv)>2 else 8
    chosen=[r for r in rows if start<=r['enrollment_rank']<=stop]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        results=list(pool.map(collect,chosen))
    with (OUT/'access.jsonl').open('a') as f:
        for info,accesses in results:
            for a in accesses:f.write(json.dumps(a,ensure_ascii=False)+'\n')
            print(json.dumps(info,ensure_ascii=False))
