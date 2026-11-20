"""Validate frozen research-run coverage and budgets, retaining instrument differences."""
import json
import re
from pathlib import Path
from datetime import datetime
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

def stamp(value):
    value = value.replace(' UTC','+00:00').replace('Z','+00:00')
    return datetime.fromisoformat(value)

def main():
    expected = {c['id'] for c in json.loads((ROOT/'cases/CASES.json').read_text())['cases']}
    audit = {'runs':[], 'errors':[], 'notes':[], 'coverage':{}, 'schema_version':1}
    for b in ['A','B']:
        found = set()
        for f in sorted((ROOT/'runs'/b).glob('*.json')):
            r = json.loads(f.read_text()); cid=r['case_id']; found.add(cid)
            assert f.stem == cid and r['baseline'] == b
            assert cid in expected
            assert r['gold_seen'] is False and r['other_runs_seen'] is False
            assert r['execution_agent']=='internal separate context'
            assert r['model_label']=='GPT-6 Astra Pro'
            assert r['raw_response'].strip()
            assert r['execution_status']=='completed', (b,cid,r['execution_status'])
            assert r['budget']['candidate_count']==len(r['candidates'])<=15
            assert [c['rank'] for c in r['candidates']]==list(range(1,len(r['candidates'])+1))
            elapsed=(stamp(r['ended_at_utc'])-stamp(r['started_at_utc'])).total_seconds()
            assert elapsed>=0
            if b=='A':
                assert r['budget']['search_queries']<=12
                assert len(r['queries'])<=12
                assert r['budget']['opened_pages']<=20
            else:
                assert r['budget']['opened_pages']<=25 or elapsed<=1200
            openings = r['opened_documents']
            charged = max(r['budget']['opened_pages'], len(openings),
                          r['budget'].get('budget_pages_charged', 0),
                          r['budget'].get('charged_page_budget', 0),
                          r['budget'].get('open_attempts', 0))
            assert charged <= (20 if b == 'A' else 25) or (b == 'B' and elapsed <= 1200)
            if charged != r['budget']['opened_pages']:
                audit['notes'].append({'case_id':cid, 'baseline':b, 'issue':'opened_pages field counts successes but failure-inclusive charged total is larger; preserve both.', 'reported_opened_pages':r['budget']['opened_pages'], 'conservative_charged':charged})
            for c in r['candidates']:
                assert c['url'].startswith(('http://','https://'))
                assert c['date_status'] in ('pre_decision','post_decision','unknown')
                assert c['post_decision'] == (c['date_status']=='post_decision')
                if b=='B':
                    assert c['discovery_catalogue_url']
                    assert any(o['url']==c['discovery_catalogue_url'] and o.get('status')=='opened' for o in openings), (cid,c['rank'],'catalogue not opened')
                if c.get('evidence_opened') and not any(o['url']==c['url'] and o.get('status')=='opened' for o in openings):
                    audit['notes'].append({'case_id':cid,'baseline':b,'candidate_rank':c['rank'],'issue':'Candidate URL lacks exact successful URL row; check redirects/supporting source before scoring E.'})
            code = [q for q in r['queries'] if q.get('tool') in ['grep.app','github_public'] or 'grep.app/api/search' in q.get('q','') or ('github.com/search' in q.get('q','') and 'code' in q.get('q',''))]
            if b=='A': assert code, (cid,'no public code search attempt')
            # Every A code-search result note was manually reviewed: 14 runs
            # positively report HTTP 200, while 17 report inaccessible surfaces.
            # Do not mistake phrases such as "no native ... success" for success.
            native = any(re.search(r'HTTP\s+200',q.get('result_note',''),re.I) for q in code)
            # Endpoint response is not evidence that every candidate came from
            # code search, nor that all returned code snippets were read fully.
            audit['runs'].append({'case_id':cid,'baseline':b,'elapsed_seconds':elapsed,'queries_recorded':len(r['queries']),'query_attempts_budgeted':r['budget']['search_queries'],'retrievals_budgeted':r['budget']['opened_pages'],'retrievals_conservative_charged':charged,'opened_records':len(openings),'successful_open_records':sum(o.get('status')=='opened' for o in openings),'candidate_count':len(r['candidates']),'candidate_dates':dict(Counter(c['date_status'] for c in r['candidates'])),'exposure_count':len(r.get('exposures',[])),'exposure_stages':dict(Counter(x['stage'] for x in r.get('exposures',[]))),'native_code_success_reported':native if b=='A' else None,'code_query_records':code,'date_window_utc':[r['started_at_utc'],r['ended_at_utc']]})
        audit['coverage'][b]={'completed':len(found),'expected':len(expected),'missing':sorted(expected-found)}
    audit['notes'].append({'issue':'Agents sometimes conservatively count in-page finds or repeated opens in the document budget; preserve raw counts, do not pretend uniform effective browsing depth.'})
    (ROOT/'evidence/RUN_AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'coverage':audit['coverage'],'notes':len(audit['notes'])}))

if __name__=='__main__': main()
