import json
import hashlib
from pathlib import Path
from collections import Counter

here=Path(__file__).resolve().parent
owned=here.parent.parent
repo=owned.parents[3]
packets=[json.loads(x) for x in (owned/'blind/cargo.jsonl').read_text().splitlines()]
reviews=[json.loads(x) for x in (here/'reviews.jsonl').read_text().splitlines()]
source_rows=json.loads((here/'sources.json').read_text())
receipts=[json.loads(p.read_text()) for p in sorted((here/'receipts').glob('RVC-O*.json'))]
checks=[]
def check(name,value):
    assert value, name
    checks.append({'check':name,'met':True})

check('33 unique masked candidates',len(reviews)==33==len({x['blind_key'] for x in reviews}))
pmap={x['blind_key']:x for x in packets}
check('candidate keys exactly match authorized input',set(pmap)=={x['blind_key'] for x in reviews})
for r in reviews:
    p=pmap[r['blind_key']]
    cp={x['package_key']:x for x in p['citation_packages']}
    check(r['blind_key']+' exact package set',set(cp)=={x['package_key'] for x in r['package_reviews']})
    conditions={x['id'] for x in p['question']['mandatory_predicates']}
    for pr in r['package_reviews']:
        package=cp[pr['package_key']]
        ids=lambda e:(e.get('source_id'),e.get('url'),e.get('section'))
        original={ids(e) for e in package['opened_evidence']}
        cited={ids(e) for e in package['returned_citations']}
        check(pr['package_key']+' condition denominator',conditions=={x['condition_id'] for x in pr['predicate_reviews']})
        for v in pr['predicate_reviews']:
            anchors={ids(e) for e in v['original_evidence']}
            check(pr['package_key']+v['condition_id']+' anchors from original package',anchors<=original)
            check(pr['package_key']+v['condition_id']+' original support is grounded',not v['support_in_original_opened'] or (v['status']=='supported' and bool(anchors)))
            check(pr['package_key']+v['condition_id']+' original citations are grounded',not v['support_in_original_citations'] or (v['support_in_original_opened'] and anchors<=cited))
        check(pr['package_key']+' opened aggregate',pr['opened_complete']==all(x['support_in_original_opened'] for x in pr['predicate_reviews']))
        check(pr['package_key']+' citation aggregate',pr['cited_complete']==all(x['support_in_original_citations'] for x in pr['predicate_reviews']))
check('37 citation packages',sum(len(x['package_reviews']) for x in reviews)==37)
check('156 mandatory predicate reviews',sum(len(p['predicate_reviews']) for x in reviews for p in x['package_reviews'])==156)
check('10 fresh primary URLs and14 audit calls',len(source_rows)==10 and len(receipts)==14 and len({x['source_url'] for x in receipts})==10)
required={'source_id','title','source_url','version','published_or_revised','checked_utc','sections_read','verified_content','limitations','producer','lineage_id','count_in_minimum','count_reason','related_questions'}
check('mandatory source schema',all(required<=set(s) for s in source_rows))
check('audit duplicates not incremented',all(s['count_in_minimum'] is False for s in source_rows))
check('all audit calls have request/time/hash',all({'request','started_utc','finished_utc','wall_seconds','raw_response_sha256'}<=set(r) for r in receipts))
check('audit not retroactive citation repair',all(r['may_repair_frozen_return_citations'] is False for r in receipts))
input_records={x['question_id']:x['question'] for x in packets}
for q,meta in input_records.items():
    p=repo/meta['input_path']
    check(q+' full input digest',hashlib.sha256(p.read_bytes()).hexdigest()==meta['input_sha256'])

differences=[]
conv={'support':'supported','conflict':'conflict','hold':'unknown'}
for r in reviews:
    cp={p['package_key']:p for p in pmap[r['blind_key']]['citation_packages']}
    for p in r['package_reviews']:
        for v in p['predicate_reviews']:
            initial={conv.get(e.get('status'),e.get('status')) for e in cp[p['package_key']]['required_bundle'][v['condition_id']]}
            if initial!={v['status']}:
                differences.append({'blind_key':r['blind_key'],'package_key':p['package_key'],'condition_id':v['condition_id'],'packet_statuses':sorted(initial),'review_status':v['status'],'reason':v['reason']})
result={'check_count':len(checks),'all_met':True,'checks':checks,'differences_from_packet_required_bundle':differences,'not_checked':['live behavior','historical releases','route/rank/top-three selection','human independence']}
(here/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
stats={
    'packet_sha256':hashlib.sha256((owned/'blind/cargo.jsonl').read_bytes()).hexdigest(),
    'reviewer':'jupyter_agent_same_model',
    'blind_keys':len(reviews),'citation_packages':sum(len(x['package_reviews']) for x in reviews),
    'questions':dict(Counter(x['question_id'] for x in reviews)),
    'package_statuses':dict(Counter(p['status'] for x in reviews for p in x['package_reviews'])),
    'predicate_statuses':dict(Counter(r['status'] for x in reviews for p in x['package_reviews'] for r in p['predicate_reviews'])),
    'opened_complete':sum(p['opened_complete'] for x in reviews for p in x['package_reviews']),
    'cited_complete':sum(p['cited_complete'] for x in reviews for p in x['package_reviews']),
    'audit_opened_complete':sum(p['audit_opened_complete'] for x in reviews for p in x['package_reviews']),
    'predicate_original_open_support':sum(r['support_in_original_opened'] for x in reviews for p in x['package_reviews'] for r in p['predicate_reviews']),
    'predicate_original_citation_support':sum(r['support_in_original_citations'] for x in reviews for p in x['package_reviews'] for r in p['predicate_reviews']),
    'no_route_or_rank_inference':True,'selection_as_top_three_not_inferred':True,
}
(here/'review-summary.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'all_met':True,'differences':differences},ensure_ascii=False,indent=2))
