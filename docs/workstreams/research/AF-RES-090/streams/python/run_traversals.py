"""Run only after the parent has committed the candidate freeze.

This records HTTP/DOM readings along previously observed browser links. It does
not claim that urllib executes JavaScript or clicks a rendered UI.
"""
import sys,json,concurrent.futures
from pathlib import Path
from urllib.parse import urldefrag
sys.path.insert(0,str(Path(__file__).parents[2]/'tools'))
from http_evidence import fetch,now
R=Path(__file__).parent;E=R/'evidence'

def run_one(task):
 target,ab=task
 purpose=target['purpose_id'];tid=purpose+'-'+ab
 first=target['starts'][ab]
 second=target.get('candidate_second_views',{}).get(ab)
 result=[]
 for step,url in enumerate([first,second] if second else [first],1):
  sid='PY-READ-'+tid+'-'+str(step)
  rec,raw=fetch(url,sid,E)
  rec['wire_url']=urldefrag(url)[0]
  result.append({'view':step,'source_id':sid,'requested_url':url,'wire_url':rec['wire_url'],'final_url':rec['final_url'],'status':rec['status'],'content_type':rec['content_type'],'body_bytes':rec['body_bytes'],'sha256':rec['sha256'],'started_utc':rec['started_utc'],'retrieved_utc':rec['retrieved_utc'],'redirects':rec['redirects'],'error':rec['error'],'receipt_path':str(E/(sid+'.receipt.json'))})
  if rec['status']!=200:break
 return {'traversal_id':tid,'purpose_id':purpose,'case_id':target['case_id'],'route':ab,'candidate_freeze_utc':json.loads((R/'freeze.json').read_text())['frozen_utc'],'entry_url':first,'sealed_target_url':target.get('sealed_next_resource'),'views':result,'view_count':len(result),'total_response_body_bytes':sum(v['body_bytes'] for v in result),'method':'HTTP GET along frozen HTML/browser-exposed hrefs; browser observations separately owned by parent; not JavaScript execution','manual_reconstruction':False,'maximum_views':2,'finished_utc':now()}

if __name__=='__main__':
 if len(sys.argv)!=2 or len(sys.argv[1])!=40:
  raise SystemExit('Pass the actual parent candidate-freeze commit SHA after permission to proceed.')
 targets=json.loads((R/'targets.json').read_text())
 tasks=[(t,ab) for t in targets for ab in ['A','B']]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(run_one,tasks))
 for row in results:row['candidate_freeze_commit']=sys.argv[1]
 (R/'traversals.raw.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps([{'id':r['traversal_id'],'count':r['view_count'],'status':[v['status'] for v in r['views']],'bytes':r['total_response_body_bytes']} for r in results],indent=2))
