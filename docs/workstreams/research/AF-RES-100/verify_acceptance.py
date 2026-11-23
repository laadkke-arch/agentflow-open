"""Post-seal re-open of three public accepted-answer timeline events."""
from pathlib import Path
import datetime,hashlib,json,urllib.request
ROOT=Path(__file__).resolve().parent
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def main():
    rows=[json.loads(x) for x in (ROOT/'evidence/resume2/outcomes/sources.jsonl').read_text().splitlines()]
    detail=json.loads((ROOT/'evidence/resume2/outcomes/evidence-details.json').read_text())
    expected={c['case_id']:c['acceptance_events_within_window'] for c in detail['cases'] if c.get('acceptance_events_within_window')}
    receipts=[];sources=[];cache=ROOT/'evidence/_cache/acceptance-verification';cache.mkdir(parents=True,exist_ok=True)
    for r in rows:
        if r['source_id'] not in ['SO-API-0007','SO-API-0011','SO-API-0019']:continue
        started=utc();url=r['direct_url'];cid=r['case_id']
        req=urllib.request.Request(url,headers={'User-Agent':'AF-RES-100-public-postseal-research/1.0'})
        with urllib.request.urlopen(req,timeout=45) as response:raw=response.read();status=response.status
        finished=utc();obj=json.loads(raw);events=[x for x in obj['items'] if x['timeline_type']=='accepted_answer']
        assert not obj.get('has_more'), 'pagination required'
        (cache/(cid+'.json')).write_bytes(raw)
        observed=[{'post_id':x['post_id'],'creation_date':x['creation_date'],
                   'creation_utc':datetime.datetime.fromtimestamp(x['creation_date'],datetime.timezone.utc).isoformat()} for x in events]
        exp=[{k:x[k] for k in ['post_id','creation_date','creation_utc']} for x in expected[cid]]
        assert observed==exp,(cid,observed,exp)
        receipt={'case_id':cid,'source_id':'ROOT-ACCEPT-'+cid,'direct_url':url,'started_utc':started,'checked_utc':finished,
                 'http_status':status,'response_sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),
                 'prior_response_sha256':r['body_sha256'],'same_response_bytes':hashlib.sha256(raw).hexdigest()==r['body_sha256'],
                 'matched_preserved_events':True,'has_more':obj.get('has_more'), 'events':observed}
        receipts.append(receipt)
        sources.append({'source_id':'ROOT-ACCEPT-'+cid,'q_numbers':['Q7'],'case_id':cid,'direct_url':url,'fixed_url':url,
                        'checked_utc':finished,'author_publisher':'Stack Exchange API / Stack Overflow public timeline',
                        'lineage':'Re-open of concurrent '+r['source_id']+'; public accepted-answer event, not actor attribution',
                        'version':'API2.3 snapshot '+finished,'exact_section_payload':{'selector':'items[timeline_type=accepted_answer]','events':observed},
                        'body_sha256':hashlib.sha256(raw).hexdigest(),'confirmed':observed,
                        'supports':'Three acceptance event timestamps within30days of original question, beyond original current-snapshot-only evidence.',
                        'limits':['Mutable public API; deleted/private event history may be absent.','Timeline owner/answerer metadata does not identify the acceptance actor.','Acceptance does not establish versions, complete inputs, outputs, or original execution.'],
                        'count_minimum':False,'count_group':'post_outcome_attribution','research_phase':'post-seal2 integration verification',
                        'duplicate_reason':'Re-opened existing post-outcome timeline; excluded from32primary sources.'})
        print(json.dumps(receipt,ensure_ascii=False),flush=True)
    (ROOT/'evidence/outcomes/acceptance-verification.json').write_text(json.dumps({'records':receipts,'all_events_matched':True},ensure_ascii=False,indent=2)+'\n')
    (ROOT/'evidence/outcomes/acceptance-sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
if __name__=='__main__':main()
