"""Recover fixed first PEP versions. Metadata-only history; no supplier lookup."""
import urllib.request, urllib.error, json, pathlib, hashlib, datetime, re, sys
BASE=pathlib.Path(__file__).parent

def get(url, dest, use):
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    req=urllib.request.Request(url,headers={'User-Agent':'AF-RES-029-research','Accept':'application/vnd.github+json'})
    rec={'url':url,'checked_utc':now,'saved':str(dest.relative_to(BASE)),'use':use,'counted':False}
    try:
        res=urllib.request.urlopen(req,timeout=40); body=res.read(); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(body)
        rec.update({'http_status':res.status,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'headers':{k:v for k,v in res.headers.items() if k.lower() in ['etag','last-modified','link','x-ratelimit-remaining','x-ratelimit-reset']}})
        with (BASE/'raw/attempts.jsonl').open('a') as f: f.write(json.dumps(rec)+'\n')
        return body,dict(res.headers)
    except Exception as e:
        rec['error']=str(e)
        with (BASE/'raw/attempts.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
        return None,{}

def recover(number):
    cid=f'pep-{number:04d}'; histories=[]
    for path in [f'{cid}.rst',f'peps/{cid}.rst',f'{cid}.txt',f'peps/{cid}.txt']:
        # All PEPs in this cohort use .rst, but historical .txt path is checked only if .rst absent.
        if path.endswith('.txt') and histories:continue
        url='https://api.github.com/repos/python/peps/commits?path='+path+'&per_page=100'
        stem=path.replace('/','_').replace('.','_')
        b,h=get(url,BASE/f'raw/{cid}/{stem}-history-1.json','Official Git commit metadata only; do not read later text or status')
        if b is None:continue
        data=json.loads(b)
        if not isinstance(data,list):continue
        histories.extend((c,path) for c in data)
        link=h.get('Link') or h.get('link') or ''
        last=re.search(r'<([^>]+)>; rel="last"',link)
        if last:
            u=last.group(1); bb,_=get(u,BASE/f'raw/{cid}/{stem}-history-last.json','Last history page needed to recover first commit; metadata only')
            if bb:histories.extend((c,path) for c in json.loads(bb))
    if not histories:
        print(json.dumps({'canonical_id':cid,'error':'No recovered history'}));return
    # Earliest committer timestamp is chronology, then SHA; later edits are not read.
    histories.sort(key=lambda cp:(cp[0]['commit']['committer']['date'],cp[0]['sha'],cp[1]))
    earliest,path=histories[0]; sha=earliest['sha']; raw=f'https://raw.githubusercontent.com/python/peps/{sha}/{path}'
    body,_=get(raw,BASE/f'originals/{cid}-{sha[:12]}.rst','First recoverable official Git text; substantive source')
    if body is None:
        print(json.dumps({'canonical_id':cid,'sha':sha,'path':path,'error':'First raw request failed'}));return
    txt=body.decode(); header=txt.split('\n\n',1)[0]
    fields={k.strip():v.strip() for k,v in (l.split(':',1) for l in header.splitlines() if ':' in l)}
    rec={'canonical_id':cid,'first_commit_sha':sha,'first_commit_author_date':earliest['commit']['author']['date'],'first_commit_committer_date':earliest['commit']['committer']['date'],'initial_git_path':path,'fixed_url':f'https://github.com/python/peps/blob/{sha}/{path}','raw_url':raw,'local_original':f'originals/{cid}-{sha[:12]}.rst','sha256':hashlib.sha256(body).hexdigest(),'first_title':fields.get('Title'),'created_header':fields.get('Created'),'discussion_to_header':fields.get('Discussions-To'),'post_history_header':fields.get('Post-History'),'initial_status_exposure':fields.get('Status'),'history_entries_received':len(histories),'method':'Earliest committer timestamp among both historical root and current peps/ path history; first and last pages of long history. No later bodies read.'}
    (BASE/f'raw/{cid}/recovery.json').write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps(rec))
for n in map(int,sys.argv[1:]):recover(n)
