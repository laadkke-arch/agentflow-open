#!/usr/bin/env python3
"""Conservative original-document ledger; retain duplicate observations as rows.

Counts concern documents, not independent trials. Versions/sections/mirrors of
one original are grouped. Manual equivalences, when needed, are explicit data.
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urldefrag, urlsplit, urlunsplit

BASE = Path(__file__).resolve().parents[1]


def norm(url):
    url = urldefrag(url or '')[0]
    p = urlsplit(url)
    host, path = p.netloc.lower(), unquote(p.path).rstrip('/')
    # A Git source file is one original across ref names and revisions.
    if host in ('github.com', 'raw.githubusercontent.com'):
        bits = path.strip('/').split('/')
        if host == 'raw.githubusercontent.com' and len(bits) >= 4:
            return 'gitfile:' + '/'.join(bits[:2] + bits[3:])
        if len(bits) >= 5 and bits[2] in ('blob', 'raw'):
            return 'gitfile:' + '/'.join(bits[:2] + bits[4:])
    rfc = re.search(r'/rfc(\d+)(?:\.(?:html|txt|pdf))?$', path)
    if rfc and host in ('www.rfc-editor.org', 'rfc-editor.org', 'datatracker.ietf.org'):
        return 'rfc:' + rfc[1]
    # Do not remove queries generally: they may identify an actual revision.
    return urlunsplit((p.scheme.lower(), host, path, p.query, ''))


def load_rows(path):
    value = json.loads(path.read_text())
    if isinstance(value, dict):
        value = value.get('sources', value.get('rows', []))
    return value


def main():
    paths = [BASE / 'evidence/initial-sources.json']
    paths += [BASE / 'streams' / n / 'sources-candidates.json' for n in ('arrow', 'cargo', 'jupyter')]
    paths += sorted((BASE / 'reviews').glob('*/sources.json'))
    paths += sorted((BASE / 'followups').glob('*/sources.json'))
    paths += sorted((BASE / 'supplements').glob('sources.json'))
    manual = {}
    if (BASE / 'evidence/source-equivalences.json').exists():
        for group in json.loads((BASE / 'evidence/source-equivalences.json').read_text()):
            for sid in group['source_ids']:
                manual[sid] = group['document_id']
    observations = []
    seen_ids = set()
    for path in paths:
        if not path.exists():
            continue
        for original in load_rows(path):
            r = dict(original)
            sid = r.get('source_id', r.get('id'))
            if not sid:
                raise ValueError(f'Missing source ID in {path}')
            if sid in seen_ids:
                raise ValueError(f'Duplicate source observation ID {sid}')
            seen_ids.add(sid)
            r['source_id'] = sid
            r['observation_file'] = str(path.relative_to(BASE))
            r['source_url'] = r.get('source_url', r.get('url', 'unknown'))
            r['version'] = r.get('version', r.get('fixed_version', '미확인'))
            r['published_or_revised'] = r.get('published_or_revised', r.get('published_date', '미확인'))
            r['checked_utc'] = r.get('checked_utc', r.get('observed_utc', '미확인'))
            r['sections_read'] = r.get('sections_read', r.get('read_sections', '미확인'))
            r['verified_content'] = r.get('verified_content', r.get('finding', '미확인'))
            r['limitations'] = r.get('limitations', r.get('limit', '미확인'))
            r['producer'] = r.get('producer', '미확인')
            r['related_questions'] = r.get('related_questions', r.get('question_ids', []))
            r['lineage_id'] = r.get('lineage_id', norm(r['source_url']))
            role = r.get('source_role', r.get('source_category', r.get('kind', 'exploration')))
            if path.name == 'initial-sources.json' and r.get('count_in_minimum'):
                role = 'initial_design'
            if role in ('candidate_provider', 'provider_original'):
                role = 'provider'
            if '/reviews/' in str(path):
                role = 'audit_provider'
            if '/followups/' in str(path):
                role = r.get('source_role', 'followup_decision')
            if '/supplements/' in str(path):
                role = r.get('source_role', 'supplemental_original')
            r['source_role'] = role
            r['observation_type'] = r.get('observation_type', 'provider_statement' if 'provider' in role else 'direct_document_read')
            r['minimum_eligible_before_deduplication'] = bool(r.get('count_in_minimum', False))
            r['minimum_eligibility_reason'] = r.get('count_reason', '미확인')
            r['document_identity'] = manual.get(sid, r.get('original_document_id', norm(r['source_url'])))
            observations.append(r)

    # Join equivalences both by explicit lineage and URL identity, avoiding a
    # silent assumption that different observation IDs are independent sources.
    parent = {r['source_id']: r['source_id'] for r in observations}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        parent[find(b)] = find(a)
    identifiers = {}
    for r in observations:
        sid = r['source_id']
        keys = [('document', r['document_identity']), ('url', norm(r['source_url']))]
        if r.get('lineage_id'):
            keys.append(('lineage', r['lineage_id']))
        for key in keys:
            if key in identifiers:
                union(identifiers[key], sid)
            else:
                identifiers[key] = sid
    groups = {}
    for r in observations:
        groups.setdefault(find(r['source_id']), []).append(r)
    original_counts = Counter()
    for members in groups.values():
        eligible = [r for r in members if r['minimum_eligible_before_deduplication']]
        representative = eligible[0] if eligible else members[0]
        did = 'DOC-' + hashlib.sha256(representative['document_identity'].encode()).hexdigest()[:12]
        for r in members:
            r['original_document_id'] = did
            r['representative_source_id'] = representative['source_id']
            r['count_in_minimum'] = bool(eligible) and r is representative
            r['count_reason'] = (r['minimum_eligibility_reason'] if r['count_in_minimum']
                else ('동일 원문의 중복 관측; 산입 대표 ' + representative['source_id'] if eligible else r['minimum_eligibility_reason']))
        if eligible:
            original_counts[representative['source_role']] += 1
    (BASE / 'sources.json').write_text(json.dumps(observations, ensure_ascii=False, indent=2) + '\n')
    summary = {
        'observation_rows': len(observations),
        'unique_document_groups_including_unread': len(groups),
        'counted_unique_direct_originals': sum(r['count_in_minimum'] for r in observations),
        'counted_by_role': dict(original_counts),
        'counted_source_ids': [r['source_id'] for r in observations if r['count_in_minimum']],
        'not_counted_source_ids': [r['source_id'] for r in observations if not r['count_in_minimum']],
        'experimental_independent_question_events': 12,
        'independence_limit': 'Document count is not a sample of independent trials. The experiment has 12 distinct first-design question events; candidates and multiple sources within one event are correlated. Supplementary fields do not increase the experiment denominator.',
        'source_files': [str(p.relative_to(BASE)) for p in paths if p.exists()],
    }
    (BASE / 'evidence/source-counts.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in summary.items() if not k.endswith('_ids')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
