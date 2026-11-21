#!/usr/bin/env python3
"""Link complete actual experiment/audit logs into the preserved preparation index."""
import datetime, hashlib
from common import ROOT, load, save

def entry(path, category):
    blob = (ROOT/path).read_bytes()
    data = load(path)
    return {'ledger': path, 'category': category,
            'sha256': hashlib.sha256(blob).hexdigest(),
            'query_records': len(data.get('queries', [])) if isinstance(data, dict) else None,
            'event_records': len(data.get('events', [])) if isinstance(data, dict) and 'events' in data else None,
            'note': 'Original records remain in the referenced file; no missing query strings or timestamps are reconstructed.'}

def main():
    inventory = load('analysis/run-inventory.json')
    assert inventory and inventory['completed_runs'] == inventory['expected_runs'] == 106 and not inventory['errors']
    assert load('claims/verification-coverage.json')['claim_counts'] == {'A': 80, 'P': 80}
    value = load('SEARCH_LOG.json')
    value['phase'] = 'complete_execution_and_audits'
    value['final_indexed_at_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    value['additional_ledgers'] = [entry(p, kind) for p, kind in [
        ('evidence/root-rechecks.json', 'method body rechecks and failed/wrong-page observations'),
        ('evidence/run-search-log.json', 'all discovery and injected-check queries/document observations'),
        ('evidence/judging-search-log.json', 'blind relevance and separate reason-audit queries'),
        ('analysis/counterexamples.json', 'exhaustive recorded counterexample selectors and matched cases')]]
    for batch in load('claims/verification-manifest.json')['batches']:
        value['additional_ledgers'].append(entry(batch['output'], 'sampled-claim official-document verification'))
    value['limits'] = ('Preparation logs preserve the precision actually retained, including bounded sessions and explicitly missing early strings. '
                       'Experimental A/P queries and opened-document records are preserved in the106 raw runs. '
                       'The additional index does not convert snippets, navigation, access errors or uninspected pages into body evidence.')
    save('SEARCH_LOG.json', value)
    print({'additional_ledgers': len(value['additional_ledgers']), 'completed_runs': inventory['completed_runs']})

if __name__ == '__main__':
    main()
