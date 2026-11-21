#!/usr/bin/env python3
"""Index recorded document observations and literal searches without rerunning them."""
import argparse,datetime,re
from common import ROOT,load,save
def main(partial):
    sources=[];excluded=[];events=[];count=0
    states={r['dispatch_index']:r for r in load('runs/DISPATCH_STATE.json')['assigned']}
    for d in load('questions/dispatch.json')['order']:
        run=load(d['output'])
        if not run or len(run.get('checks',[]))!=3:
            if partial:continue
            raise AssertionError(('unfinished run',d['output']))
        count+=1;receipt=load(f'runs/freeze/{d["condition"]}-{d["qid"]}.json')
        for i,q in enumerate(run['queries']):
            events.append({'id':f'RUN-{d["condition"]}-{d["qid"]}-Q{i+1:02d}',
                           'kind':'literal_query','condition':d['condition'],'qid':d['qid'],
                           'stage':'discovery' if i<receipt['query_prefix_count'] else 'checks',
                           'raw_record':q,'source_file':d['output']})
        for i,doc in enumerate(run['opened_documents']):
            status=str(doc.get('status',''));op=str(doc.get('operation',''))
            read=status.lower().startswith(('opened','ok','partial:','redirect landing page'))
            stage='discovery' if i<receipt['document_prefix_count'] else 'checks'
            sid=f'RUN-{d["condition"]}-{d["qid"]}-D{i+1:02d}'
            events.append({'id':sid,'kind':'document_event','condition':d['condition'],'qid':d['qid'],
                           'stage':stage,'raw_record':doc,'source_file':d['output']})
            if not read:
                excluded.append({'id':sid,'url':doc['url'],'accessed_at_utc':doc['at_utc'],
                                 'status':status,'confirmed':doc.get('confirmed'),
                                 'reason':'No successful readable-body status in the preserved observation; not counted as a body reading.',
                                 'source_file':d['output'],'counted':False});continue
            level='D2' if re.search(r'/blob/[0-9a-fA-F]{40}/',doc['url']) else 'D1'
            sources.append({'id':sid,'url':doc['url'],'accessed_at_utc':doc['at_utc'],
                            'source_type':'public document observation during experimental '+stage,
                            'title':doc.get('title') or 'Title not separately recorded; identified by observed URL',
                            'version_or_date':doc.get('published_or_version') or 'live',
                            'sections_read':doc.get('sections_read') or 'See preserved run observation; complete-body coverage is not asserted',
                            'confirmed':doc.get('confirmed') or doc.get('notes') or 'No independent factual finding recorded beyond the page observation.',
                            'limits':doc.get('limits') or 'Document inspection only; no installation or user adoption established. Partial/undated/current text does not establish historical availability. Read with the run-specific limitations.',
                            'level':level,'used_in':['Q4','Q7']+(['Q3'] if stage=='checks' else ['Q6']),
                            'counted_as':'execution_document_not_method_literature',
                            'condition':d['condition'],'qid':d['qid'],'stage':stage,'status':status,'operation':op,
                            'date_status':doc.get('date_status'),'post_decision':doc.get('post_decision'),
                            'reader':states[d['dispatch_index']]['agent'],'source_file':d['output']})
    save('evidence/run-readings.json',{'sources':sources,'excluded':excluded,'completed_runs':count,
                                    'partial':partial,'note':'Repeated observations remain distinct IDs tied to exact log events; none increases the29 methodological-paper count.'})
    save('evidence/run-search-log.json',{'events':events,'completed_runs':count,'partial':partial,
                                      'generated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                      'note':'Indexed original records, not newly executed searches.'})
    print({'completed_runs':count,'body_observations':len(sources),'excluded_events':len(excluded),'query_and_document_events':len(events)})
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--partial',action='store_true');a=p.parse_args();main(a.partial)
