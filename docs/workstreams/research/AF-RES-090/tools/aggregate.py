"""Combine committed research observations without repeating network reads.

Run from any directory. This writes only inside the AF-RES-090 owned path.
Source counts deliberately exclude tree/ref metadata, failed bodies and mirrors.
"""
from pathlib import Path
import collections
import datetime
import hashlib
import json
import subprocess

B = Path(__file__).resolve().parents[1]
REPO = B.parents[3]


def portable(x):
    if isinstance(x, dict):
        return {k: portable(v) for k, v in x.items()}
    if isinstance(x, list):
        return [portable(v) for v in x]
    if isinstance(x, str) and x.startswith(str(B) + '/'):
        return x[len(str(B)) + 1:]
    return x


def readjson(p):
    return json.loads((B / p).read_text())


def writejson(p, x):
    (B / p).write_text(json.dumps(portable(x), ensure_ascii=False, indent=2) + '\n')


def main():
    sources, assets, source_counts = [], [], {}
    category_map = {'project_guidance': 'publisher', 'publisher_source': 'publisher',
                    'referenced_file': 'asset', 'followup_resource': 'asset',
                    'asset': 'asset', 'method': 'method',
                    'cross_spec': 'cross', 'cross_work': 'cross'}
    for stream in ('python', 'r', 'methods', 'cross'):
        rows = [json.loads(x) for x in (B / 'streams' / stream / 'sources.jsonl').read_text().splitlines()]
        source_counts[stream] = len(rows)
        for r in rows:
            r['stream'] = stream
            r['stream_eligible'] = r['eligible']
            r['minimum_category'] = category_map.get(r['category'])
            if r['minimum_category'] is None:
                r['eligible'] = False
                r['counting_note'] = 'Supporting tree/tag/commit metadata or repeated/error evidence; excluded from 24-source composition minimum.'
            sources.append(portable(r))
        ap = B / 'streams' / stream / 'assets.jsonl'
        if ap.exists():
            for l in ap.read_text().splitlines():
                a = json.loads(l)
                a['stream'] = stream
                assets.append(portable(a))
    # Re-read the six inherited repository inputs at the supplied immutable SHAs.
    inherited = []
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    for name in ('HANDOFF.md', 'RESULT.md', 'cards.md', 'comparison.json', 'routes.jsonl', 'claims.csv'):
        sha = '6907534462af729f409c52ce08d3331de22c96e6' if name == 'HANDOFF.md' else 'e6a79c3ac05b84ea1c7db313233df1717cade756'
        path = 'docs/workstreams/research/AF-RES-086/' + name
        body = subprocess.check_output(['git', 'show', sha + ':' + path], cwd=REPO)
        row = {'source_id': 'IN-086-' + name.replace('.', '-').upper(), 'work_id': 'AF-RES-086',
               'lineage_id': 'inherited-AF-RES-086', 'category': 'inherited_research',
               'original_url': 'https://github.com/laadkke-arch/agentflow-open/blob/' + sha + '/' + path,
               'published_utc': None, 'retrieved_utc': now, 'version': sha, 'location': path,
               'questions': ['Q1', 'Q2', 'Q3', 'Q6'], 'cases': ['P3', 'P1', 'R1', 'R2'],
               'observation': '인수한 시작 URL·판·생성물 지문·추천 범위를 확인. 과거 관측창 결과는 이번 현재 열람 성공으로 사용하지 않음.',
               'excerpt': None, 'fingerprint': {'body_bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()},
               'support_refute': 'Defines inherited sample and hypotheses; not fresh external primary evidence.',
               'limitations': '선행 연구 결과이며 외부 직접 원자료 최소량에서 제외.',
               'reread_url': 'https://github.com/laadkke-arch/agentflow-open/blob/' + sha + '/' + path,
               'eligible': False, 'minimum_category': None, 'stream': 'inherited',
               'receipt_path': 'evidence/inherited-inputs.json'}
        inherited.append(row)
    sources += inherited
    writejson('evidence/inherited-inputs.json', {'recorded_utc': now, 'inputs': inherited})
    (B / 'sources.jsonl').write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in sources))
    (B / 'assets.jsonl').write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in assets))
    traversals = readjson('streams/python/traversals.json') + readjson('streams/r/traversals.json')['traversals']
    normal = []
    for x in traversals:
        y = {'traversal_id': x['traversal_id'].removeprefix('R-'),
             'purpose_id': x.get('purpose_id', x.get('target_id')), 'case_id': x['case_id'], 'route': x['route'],
             'target_body': x['target_body'], 'followup_resource': x['followup_resource'], 'same_version': x['same_version'],
             'static_output': x.get('static_output', 'not_applicable'),
             'view_count': x.get('view_count', x.get('views')),
             'response_bytes': x.get('response_bytes', x.get('direct_response_bytes')),
             'steps': x.get('steps', x.get('views')), 'final_url': x['final_url'],
             'raw_stream_record': 'streams/' + ('r' if x['case_id'].startswith('R') else 'python') + '/traversals.json',
             'first_target_body': x.get('first_target_body_status', x['target_body'])}
        y['purpose_kind'] = y['purpose_id'].split('-')[1]
        y['strict_success'] = y['target_body'] == 'confirmed' and y['same_version'] == 'confirmed' and (y['purpose_kind'] == 'body' or y['followup_resource'] == 'confirmed')
        y['same_version_subject'] = ('destination intended legacy series 1.x; NOT identical to 3.3.0 release' if y['case_id'] == 'P3' and y['purpose_kind'] == 'next' else 'containing HTML/static output only; no SVG/replay payload' if y['case_id'] == 'R2' and y['purpose_kind'] == 'next' else 'target document edition or external follow-up edition relation')
        normal.append(portable(y))
    writejson('evidence/normalized-traversals.json', normal)
    eligible = [s for s in sources if s['eligible']]
    counts = {'recorded_utc': now, 'primary_traversals': len(normal), 'paired_purposes': len({x['purpose_id'] for x in normal}),
              'primary_document_views': sum(x['view_count'] for x in normal),
              'primary_response_entity_bytes': sum(x['response_bytes'] for x in normal),
              'primary_status_counts': dict(collections.Counter(str(v['status']) for x in normal for v in x['steps'])),
              'axis_counts': {axis: dict(collections.Counter(x[axis] for x in normal)) for axis in ('target_body', 'followup_resource', 'same_version')},
              'strict_purpose_success': sum(x['strict_success'] for x in normal),
              'strict_body_success': sum(x['strict_success'] for x in normal if x['purpose_kind'] == 'body'),
              'strict_followup_success': sum(x['strict_success'] for x in normal if x['purpose_kind'] == 'next'),
              'direct_http_source_rows': sum(source_counts.values()), 'inherited_rows': len(inherited),
              'ledger_rows': len(sources), 'eligible_unique_sources': len(eligible),
              'eligible_categories': dict(collections.Counter(x['minimum_category'] for x in eligible)),
              'independent_lineages': len({x['lineage_id'] for x in eligible}),
              'lineages': sorted({x['lineage_id'] for x in eligible}), 'stream_row_counts': source_counts,
              'asset_records': len(assets),
              'interpretation': 'same_version is purpose-specific; P3 legacy relation and R2 static-only subject must not be erased. No population success estimate.',
              'measurement': 'Main document/resource response entity bytes only; excludes UI automatic subrequests, HTTP headers/TLS, search transport and human time.',
              'raw_cache_policy': 'Full downloaded entities were inspected and hashed locally. Commit short excerpts/receipts and canonical re-read URLs, not raw cache.'}
    writejson('evidence/counts.json', counts)
    print(json.dumps({k: v for k, v in counts.items() if k not in ('lineages',)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
