"""Recover only issue opening events from the corresponding public GH Archive hour."""
import concurrent.futures,datetime,gzip,hashlib,json,pathlib,urllib.request

BASE=pathlib.Path(__file__).resolve().parents[2]
PRIVATE=BASE/'private'/'rclone'
OUT=BASE/'streams'/'rclone'

def recover(row):
    n=row['number']; hour=datetime.datetime.fromisoformat(row['created_at'].replace('Z','+00:00')).strftime('%Y-%m-%d-%H').replace('-0','-',1) if False else datetime.datetime.fromisoformat(row['created_at'].replace('Z','+00:00')).strftime('%Y-%m-%d-')+str(int(row['created_at'][11:13]))
    url=f'https://data.gharchive.org/{hour}.json.gz'; at=datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')
    result={'number':n,'url':url,'accessed_utc':at,'type':'archive_opening_recovery','count_toward_minimum':False,'comment_text_exposed':False}
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AF-RES-070-public-research'}),timeout=45) as r:
            result.update({'status':r.status,'archive_compressed_length':r.headers.get('Content-Length')})
            with gzip.GzipFile(fileobj=r) as stream:
                for lineno,line in enumerate(stream,1):
                    if b'"IssuesEvent"' not in line or b'rclone/rclone' not in line:continue
                    event=json.loads(line); payload=event.get('payload',{}); issue=payload.get('issue',{})
                    if event.get('type')!='IssuesEvent' or event.get('repo',{}).get('name')!='rclone/rclone' or payload.get('action')!='opened' or issue.get('number')!=n:continue
                    body=issue.get('body') or ''; raw=body.encode('utf-8')
                    (PRIVATE/f'issue-{n}-opened-event.json').write_bytes(line)
                    (PRIVATE/f'issue-{n}-opening-body.txt').write_bytes(raw)
                    current=(PRIVATE/f'issue-{n}-body.txt').read_bytes()
                    result.update({'found':True,'jsonl_line':lineno,'event_id':event['id'],'event_created_at':event['created_at'],'issue_created_at':issue['created_at'],'issue_updated_at_at_opening':issue['updated_at'],'opening_body_sha256':hashlib.sha256(raw).hexdigest(),'current_body_sha256':hashlib.sha256(current).hexdigest(),'opening_equals_current':raw==current,'opening_body_lines':len(body.splitlines()),'event_sha256':hashlib.sha256(line).hexdigest()})
                    break
                else:result.update({'found':False,'lines_scanned':lineno})
    except Exception as exc:result.update({'status':'failure','error':type(exc).__name__+': '+str(exc)})
    (PRIVATE/f'issue-{n}-opening-meta.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
    return result

if __name__=='__main__':
    import sys
    rows=json.loads((PRIVATE/'queue-first16.json').read_text())['rows'];start=int(sys.argv[1]) if len(sys.argv)>1 else 1;stop=int(sys.argv[2]) if len(sys.argv)>2 else 8
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results=list(pool.map(recover,[x for x in rows if start<=x['enrollment_rank']<=stop]))
    with (OUT/'access.jsonl').open('a') as f:
        for x in results:f.write(json.dumps(x,ensure_ascii=False)+'\n');print(json.dumps(x,ensure_ascii=False),flush=True)
