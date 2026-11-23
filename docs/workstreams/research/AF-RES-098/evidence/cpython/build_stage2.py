"""Pre-prediction stage: open newer ZIP central-directory names ONLY.
No ZipFile.read, extract, or newer HTML/payload/CI lookup is performed.
"""
from pathlib import Path
from urllib.request import build_opener, HTTPRedirectHandler
from datetime import datetime, timezone
import csv, hashlib, json, posixpath, zipfile
ROOT=Path(__file__).resolve().parent
CACHE=Path('/tmp/af098-cpython')
URL='https://docs.python.org/ftp/python/doc/3.12.1/python-3.12.1-docs-html.zip'
record={'stage':2,'url':URL,'utc':datetime.now(timezone.utc).isoformat(),'redirects':[],'request_count':1,'new_html_asset_file_reads':0}
class Redirects(HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        record['redirects'].append({'from':req.full_url,'status':code,'to':newurl})
        return super().redirect_request(req,fp,code,msg,headers,newurl)
try:
    with build_opener(Redirects()).open(URL,timeout=60) as response:
        record.update({'status':response.status,'final_url':response.url,'content_type':response.headers.get('Content-Type')})
        # Store opaque transfer bytes; do not decompress any member.
        with (CACHE/'new.zip').open('wb') as dst:
            while block:=response.read(1024*1024):dst.write(block)
    record['received_bytes']=(CACHE/'new.zip').stat().st_size
    z=zipfile.ZipFile(CACHE/'new.zip')
    names=z.namelist()
    prefix='python-3.12.1-docs-html/'
    normalized=[n[len(prefix):] if n.startswith(prefix) else n for n in names]
    record.update({'listing_complete':True,'central_directory_entries':len(names),'normalized_listing_sha256':hashlib.sha256('\n'.join(normalized).encode()).hexdigest(),'new_payload_hashes_used':False})
except Exception as e:
    names=[];normalized=[];record.update({'error':repr(e),'listing_complete':False,'central_directory_entries':None})
(ROOT/'new-member-list.txt').write_text('\n'.join(normalized)+'\n')
selected=json.loads((ROOT/'selected.json').read_text())['selected'];pred=[]
for s in selected:
    target=s['relative_asset_path'];exact=normalized.count(target);basename=posixpath.basename(target);matches=[p for p in normalized if posixpath.basename(p)==basename]
    choice='UNKNOWN' if not record['listing_complete'] else 'YES' if exact==1 else 'HOLD' if exact>1 or matches else 'NO'
    pred.append({'case_id':s['case_id'],'project':'CPython','old_version':'3.12.0','new_version':'3.12.1','old_section_uri':s['old_uri'],'logical_resource':s['logical_resource'],'purpose':s['purpose'],'old_relative_asset_path':target,'list_url':URL,'list_utc':record['utc'],'list_complete':record['listing_complete'],'list_entries':record['central_directory_entries'],'exact_path_matches':exact,'basename_candidates':';'.join(matches),'prediction_U':choice,'prediction_target':'same next-edition section uses frozen logical resource','reason':'exact normalized relative path occurs once' if choice=='YES' else choice,'prediction_utc':datetime.now(timezone.utc).isoformat(),'new_content_files_opened':0,'listing_requests':1,'exposure':'new ZIP received opaquely; central-directory names only; no member read/extract, no new HTML/payload/CI'})
with (ROOT/'predictions.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(pred[0]));w.writeheader();w.writerows(pred)
record['predictions']=pred
record['cost']={'logical_download_requests':1,'transport_redirects':len(record['redirects']),'directory_listing_reads':1 if record['listing_complete'] else 0,'newer_document_asset_member_reads':0}
record['exposure_boundary']='New archive bytes were received and stored opaquely. zipfile.namelist only; no ZipFile.read/extract or parsing of new member contents, no CI record inspected. No blob/asset SHA used for prediction.'
record['stage1_commit']='c0d31ca194e47fe69bc51dc0ef85d6e346b50774'
(ROOT/'stage2-receipt.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
source={'id':'PY-S010','q':['Q2'],'case_id':'PY1;PY2','url':URL,'fixed_url':URL,'utc':record['utc'],'publisher':'Python Software Foundation','lineage':'CPython documentation','version':'3.12.1','locator':'ZIP central directory names only; _images/logging_flow.png and _images/hashlib-blake2-tree.png','observed':f"complete={record['listing_complete']}; entries={record['central_directory_entries']}; exact matches PY1={pred[0]['exact_path_matches']}, PY2={pred[1]['exact_path_matches']}",'claim':'두 정확 상대경로가 유일하므로 다음 판 절 사용을 YES로 사전 예측','limitations':'목록의 존재만 확인. 새 본문/파일 내용/생성 기록을 아직 읽지 않아 실제 사용·바이트 동일성·생성을 증명하지 않는다.','category':'distribution_record','counted':bool(record['listing_complete']),'dedup_basis':'별도 판 배포 목록; 개별 멤버를 새 자료 수로 세지 않음','sha256':None,'bytes':record.get('received_bytes'),'listing_sha256':record.get('normalized_listing_sha256'),'full_archive_payload_inspected':False}
with (ROOT/'sources.jsonl').open('a') as f:f.write(json.dumps(source,ensure_ascii=False)+'\n')
print(json.dumps(record,ensure_ascii=False,indent=2))
