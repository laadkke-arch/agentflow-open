#!/usr/bin/env python3
import csv,json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
rows=[]
for domain,name in [('pandoc','opening-retry-analysis.json'),('gdal','selected-initial-recovery-addendum.json')]:
    for r in json.loads((P/'streams'/domain/name).read_text()):
        pan=domain=='pandoc';n=r.get('number',r.get('issue_number'));repo='jgm/pandoc' if pan else 'OSGeo/gdal'
        rows.append(dict(case_id=r['case_id'],repository=repo,issue_number=n,original_url=f'https://github.com/{repo}/issues/{n}',archive_url=r['archive_url'],event_id=r['event_id'],event_created_utc=r.get('event_created_utc',r.get('event_created_at')),recovered_utc=r.get('opening_body_directly_read_utc',r.get('retrieved_utc')),opening_body_sha256=r.get('opening_body_sha256',r.get('initial_body_sha256')),current_body_sha256=r['current_body_sha256'],exact_body_equal=r.get('same_body_as_current',r.get('current_equals_initial_exact')),goal_constraints_changed=r.get('semantic_request_difference_observed',r.get('prespecified_field_goal_constraints_changed')),opening_verified=True,verified_before_policy_seal=False,difference_summary=r.get('original_goal_and_constraints',r.get('semantic_difference')),source_ledger=f'streams/{domain}/{name}',prior_failure_ledger='streams/pandoc/opening-provenance.json' if pan else f'streams/gdal/opening-{n}-provenance.json'))
with (P/'initial-version-review.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader()
    w.writerows({k:json.dumps(v) if isinstance(v,bool) else v for k,v in r.items()} for r in rows)
print(json.dumps({'recovered':len(rows),'exact_body_equal':sum(r['exact_body_equal'] for r in rows),'goal_constraints_changed':sum(r['goal_constraints_changed'] for r in rows)}))
