#!/usr/bin/env python3
"""Audit explicit code-search attempts in preserved logs, not search success."""
import datetime,json,re,urllib.parse
from common import load,save

def main():
    rows=[]
    for d in load('questions/dispatch.json')['order']:
        run=load(d['output']);events=[]
        for kind,records in [('query',run.get('queries',[])),('document',run.get('opened_documents',[]))]:
            for index,event in enumerate(records):
                text=urllib.parse.unquote(json.dumps(event,ensure_ascii=False))
                if re.search(r'grep\.app|github\.com/search',text,re.I):
                    strict=bool(re.search(r'grep\.app|type=code|type:code',text,re.I))
                    events.append({'kind':kind,'index':index,'explicit_code_surface':strict,'record':event})
        rows.append({'qid':d['qid'],'condition':d['condition'],'source_file':d['output'],
                     'explicit_code_surface_attempt_recorded':any(e['explicit_code_surface'] for e in events),
                     'events':events})
    deviations=[{'qid':r['qid'],'condition':r['condition'],'source_file':r['source_file'],
                 'finding':'Only a GitHub repository-search surface is recorded, not the explicitly required code-search surface.',
                 'action':'Preserve frozen run and primary analysis; report an exploratory complete-pair sensitivity excluding this question. Do not retroactively spend an extra query or relabel repository search as code search.'}
                for r in rows if not r['explicit_code_surface_attempt_recorded']]
    result={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'runs':len(rows),'explicit_attempt_records':sum(r['explicit_code_surface_attempt_recorded'] for r in rows),
            'rows':rows,'deviations':deviations,
            'limits':'Endpoint-string evidence in preserved query/document records, not independent server instrumentation or successful native code search. Blocked attempts satisfy the attempt requirement; code-through-web remains a separately described fallback. Audited before outcome aggregation.'}
    save('analysis/code-search-audit.json',result)
    print(json.dumps({k:result[k] for k in ['runs','explicit_attempt_records','deviations']},ensure_ascii=False))

if __name__=='__main__':main()
