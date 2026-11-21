#!/usr/bin/env python3
"""Index actual independent judging/audit reads without treating them as literature."""
import datetime
from common import ROOT, load, save

FIELDS = ['url', 'accessed_at_utc', 'title', 'version_or_date',
          'sections_read', 'confirmed', 'limits', 'level']

def main():
    assert (ROOT/'judging/key.json').exists(), 'Release the key after complete blind coverage first'
    manifests = [('JUDGE', load('judging/judge-manifest.json')),
                 ('REASON', load('judging/reason-manifest.json'))]
    sources, excluded, searches = [], [], []
    for family, jobs in manifests:
        for index, job in enumerate(jobs, 1):
            value = load(job['output'])
            assert value and value.get('raw_response'), job['output']
            reader = value.get('judge_id', value.get('judge'))
            for n, row in enumerate(value.get('readings', []), 1):
                assert all(k in row for k in FIELDS), (job['output'], n, set(FIELDS)-set(row))
                assert row['level'] in ['D1', 'D2', 'D3-fetch'], (job['output'], n, row['level'])
                sources.append({'id': f'{family}-{index:02d}-D{n:03d}', **row,
                                'source_type': row.get('source_type', 'public official document inspected in independent internal judgment'),
                                'used_in': ['Q3', 'Q5', 'Q8'],
                                'counted_as': 'judgment_verification_not_methods',
                                'reader': reader, 'source_file': job['output']})
            excluded.extend({'source_file': job['output'], **r} for r in value.get('excluded_readings', []))
            for n, query in enumerate(value.get('queries', []), 1):
                searches.append({'id': f'{family}-{index:02d}-Q{n:03d}',
                                 'reader': reader, 'source_file': job['output'], 'raw_record': query})
    save('evidence/judging-readings.json', {'sources': sources, 'excluded': excluded,
         'limits': 'Actual recorded inspections only. Repeated pages and judgments do not add to the methodological-paper count.'})
    save('evidence/judging-search-log.json', {'events': searches,
         'indexed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()})
    print({'judging_body_observations': len(sources), 'excluded_observations': len(excluded),
           'query_records': len(searches)})

if __name__ == '__main__':
    main()
