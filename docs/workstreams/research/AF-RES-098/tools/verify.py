#!/usr/bin/env python3
"""Read-only AF-RES-098 consistency check; optional fresh exact-URL receipt.

Default: reads committed/workspace evidence and git objects, prints JSON, writes nothing.
--network --output NEW_FILE: also opens 12 HTML + 12 primary PNG URLs. No archives,
examples, document builds, browser execution, or edits to original evidence are made.
A successful check authenticates internal consistency, not every external claim or G.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
from urllib.error import HTTPError
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.request import HTTPRedirectHandler, build_opener

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
REL = ROOT.relative_to(REPO).as_posix()
STAGE1 = 'c0d31ca194e47fe69bc51dc0ef85d6e346b50774'
STAGE2 = '0df9ea9edbcee995d631eef54b65fd43f73c245f'
CASE_IDS = {'MP1', 'MP2', 'PY1', 'PY2', 'GG1', 'GG2'}
AXES = ('P_included', 'U_section_uses', 'G_build_generated')
MINIMUMS = {'all_primary': 25, 'example_bodies': 10, 'payloads': 6,
            'publication_build_listing': 5, 'epub_spec_and_package': 2,
            'data_rules_and_records': 2}
PUB_CATEGORIES = {'release_record', 'deployment_listing', 'publication_record',
                  'build_rule', 'distribution_record', 'build_record', 'publication'}
NULL_FIXED_URL_IDS = {'GG-RELEASES', 'GG-OLD-DEPLOYS', 'GG-NEW-DEPLOY-DATES'}
FROZEN1 = ['SCOPE.md', 'freeze.json', 'frame.csv', 'manifest.json',
           'evidence/matplotlib/release-frame.json',
           'evidence/ggplot2/release-selection.json'] + [
    f'evidence/{g}/{name}' for g in ('matplotlib', 'cpython', 'ggplot2')
    for name in ('frame.csv', 'selected.json')]
FROZEN2 = ['predictions.csv', 'evidence/prediction-seal.json'] + [
    f'evidence/{g}/{name}' for g in ('matplotlib', 'cpython', 'ggplot2')
    for name in ('predictions.csv', 'stage2-receipt.json')]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def utc():
    return datetime.now(timezone.utc).isoformat()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def read_csv(path):
    with path.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args], stderr=subprocess.PIPE)


def bool_value(value):
    return str(value).lower() == 'true'


def valid_url(value):
    return isinstance(value, str) and urlparse(value).scheme in ('http', 'https') and bool(urlparse(value).netloc)


def verify_frozen():
    findings = []
    for revision, files in ((STAGE1, FROZEN1), (STAGE2, FROZEN2)):
        for name in files:
            saved = git('show', f'{revision}:{REL}/{name}')
            current = (ROOT / name).read_bytes()
            normalized = current.replace(b'\r\n', b'\n')
            require(current == saved or normalized == saved, f'Sealed file changed: {name} versus {revision}')
            findings.append({'file': name, 'sealed_commit': revision, 'sealed_sha256': sha(saved),
                             'workspace_sha256': sha(current),
                             'workspace_line_endings': 'identical' if current == saved else 'CRLF_to_LF_only'})
    return findings


def source_counts(sources):
    required = {'id', 'q', 'case_id', 'url', 'fixed_url', 'utc', 'publisher', 'lineage',
                'version', 'locator', 'observed', 'claim', 'limitations', 'counted',
                'dedup_basis', 'category', 'canonical_lineage'}
    ids = set()
    urls = {}
    hashes = {}
    families = Counter()
    categories = Counter()
    counted = []
    for row in sources:
        require(required <= row.keys(), f'Source fields missing: {row.get("id")}')
        require(row['id'] not in ids, f'Duplicate source ID: {row["id"]}')
        ids.add(row['id'])
        for key in required - {'counted', 'fixed_url'}:
            require(bool(row[key]), f'Empty source field {key}: {row["id"]}')
        require(isinstance(row['counted'], bool), f'counted is not boolean: {row["id"]}')
        require(isinstance(row['q'], list) and row['q'] and set(row['q']) <= {f'Q{i}' for i in range(1, 8)}, f'Invalid Qs: {row["id"]}')
        require(valid_url(row['url']), f'Invalid source URL: {row["id"]}')
        if row['fixed_url'] is None:
            require(row['id'] in NULL_FIXED_URL_IDS, f'Unexpected missing fixed URL: {row["id"]}')
            require(isinstance(row.get('fixed_url_status'), str) and row['fixed_url_status'].strip(),
                    f'Missing fixed URL needs explicit unavailable status: {row["id"]}')
            require(isinstance(row['limitations'], str) and row['limitations'].strip(),
                    f'Missing fixed URL needs limitation: {row["id"]}')
            require(isinstance(row.get('sha256'), str) and re.fullmatch('[0-9a-f]{64}', row['sha256']),
                    f'Mutable listing needs observed response digest: {row["id"]}')
        else:
            require(valid_url(row['fixed_url']), f'Invalid fixed source URL: {row["id"]}')
        stamp = datetime.fromisoformat(row['utc'].replace('Z', '+00:00'))
        require(stamp.tzinfo is not None and stamp.utcoffset().total_seconds() == 0, f'UTC required: {row["id"]}')
        digest = row.get('sha256')
        if digest:
            require(re.fullmatch('[0-9a-f]{64}', digest), f'Invalid SHA256: {row["id"]}')
        if row.get('bytes') is not None:
            require(isinstance(row['bytes'], int) and row['bytes'] >= 0, f'Invalid byte length: {row["id"]}')
        if not row['counted']:
            continue
        require(row['category'] not in {'failed_access', 'empty_query', 'calibration', 'discovery_listing'}, f'Nonqualifying source counted: {row["id"]}')
        require(not row['canonical_lineage'].startswith('CAL-'), f'Calibration counted as new: {row["id"]}')
        require(row.get('status', 200) in (200, '200'), f'Failure counted: {row["id"]}')
        canonical_url = urldefrag(row['url'])[0]
        require(canonical_url not in urls, f'Same URL/anchor counted twice: {row["id"]}, {urls.get(canonical_url)}')
        urls[canonical_url] = row['id']
        if digest:
            require(digest not in hashes, f'Identical bytes counted twice: {row["id"]}, {hashes.get(digest)}')
            hashes[digest] = row['id']
        counted.append(row)
        categories[row['category']] += 1
        families[row['canonical_lineage']] += 1
    for row in sources:
        for field in ('duplicate_of', 'global_duplicate_of'):
            if row.get(field):
                require(row[field] in ids, f'Unknown duplicate target: {row["id"]}')
    observed = {
        'all_primary': len(counted),
        'example_bodies': categories['example_body'],
        'payloads': categories['payload'] + categories['image_payload'],
        'publication_build_listing': sum(categories[k] for k in PUB_CATEGORIES),
        'epub_spec_and_package': sum(r['category'] == 'epub' or r['canonical_lineage'] == 'RULE-epub' for r in counted),
        'data_rules_and_records': sum(r['canonical_lineage'] in {'DATA-data-citation-corpus', 'RULE-datacite', 'RULE-zenodo'} for r in counted),
    }
    for key, minimum in MINIMUMS.items():
        require(observed[key] >= minimum, f'Minimum shortfall {key}: {observed[key]} < {minimum}')
    return counted, categories, families, observed


def markdown_tables(text):
    """Read GFM pipe tables outside fenced blocks; return row and line boundaries."""
    lines = text.splitlines()
    tables = []
    fence = None
    i = 0
    def cells(line):
        return [c.strip() for c in re.split(r'(?<!\\)\|', line.strip().strip('|'))]
    def separator(line):
        cs = cells(line)
        return len(cs) > 1 and all(re.fullmatch(r':?-{3,}:?', c.replace(' ', '')) for c in cs)
    while i < len(lines):
        match = re.match(r'^\s*(`{3,}|~{3,})', lines[i])
        if match:
            marker = match.group(1)[0]
            fence = None if fence == marker else marker if fence is None else fence
            i += 1
            continue
        if fence is None and '|' in lines[i] and i + 1 < len(lines) and separator(lines[i + 1]):
            start = i
            header = cells(lines[i])
            i += 2
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                row = cells(lines[i])
                require(len(row) == len(header), f'Malformed Markdown table row at line {i + 1}')
                rows.append(row)
                i += 1
            tables.append({'header': header, 'rows': rows, 'start_line': start + 1, 'end_line': i})
        else:
            i += 1
    return tables


def verify_documents(lineage):
    report = {}
    result = ROOT / 'RESULT.md'
    if result.exists():
        text = result.read_text(encoding='utf-8')
        tables = markdown_tables(text)
        require(len(tables) >= 4, 'RESULT needs first 3 required tables and final weakness table')
        require(len(tables[0]['rows']) == 6, 'RESULT recruitment/prediction table must retain 6 cases')
        require(len(tables[1]['rows']) == 12, 'RESULT adjudication table must retain 12 slots')
        require(len(tables[2]['rows']) == 7, 'RESULT return table must retain 7 purpose rows')
        first_ids = [re.findall(r'\b(?:MP[12]|PY[12]|GG[12])\b', ' '.join(row)) for row in tables[0]['rows']]
        require({ids[0] for ids in first_ids if ids} == CASE_IDS, 'RESULT first table case IDs missing')
        for record in lineage:
            require(any(re.search(r'\b' + record['case_id'] + r'\b', ' '.join(row)) and record['version'] in ' '.join(row) for row in tables[1]['rows']), f'RESULT slot missing {record["case_id"]}/{record["version"]}')
        final = tables[-1]
        require(len(final['rows']) == 3 and len(final['header']) == 3, 'RESULT must end with exactly 3 weakness rows in 3 columns')
        require('불일치' in final['header'][0] or '약점' in final['header'][0], 'Final table first column must name mismatch/weakness')
        require('다음' in final['header'][1] and '결론' in final['header'][2], 'Final table needs next input and conclusion-changing observation columns')
        require(all(all(cell.strip() for cell in row) for row in final['rows']), 'Empty final weakness cell')
        require(not '\n'.join(text.splitlines()[final['end_line']:]).strip(), 'Content follows final weakness table')
        report['RESULT.md'] = {'status': 'passed', 'first_three_table_rows': [len(t['rows']) for t in tables[:3]], 'final_weakness_rows': 3}
    else:
        report['RESULT.md'] = {'status': 'not_present_not_checked'}
    selfcheck = ROOT / 'SELF_CHECK.md'
    if selfcheck.exists():
        tables = markdown_tables(selfcheck.read_text(encoding='utf-8'))
        qrows = []
        for table in tables:
            for row in table['rows']:
                match = re.search(r'\bQ([1-7])\b', row[0])
                if match:
                    qrows.append((int(match.group(1)), row))
        require(Counter(q for q, _ in qrows) == Counter(range(1, 8)), 'SELF_CHECK must retain exactly one row per Q1–Q7')
        for q, row in qrows:
            require(len(row) >= 4 and all(row), f'SELF_CHECK Q{q} answer/evidence/falsifier/limit missing')
            require(re.search(r'https?://', ' '.join(row)), f'SELF_CHECK Q{q} lacks actual evidence URL')
        report['SELF_CHECK.md'] = {'status': 'passed', 'q_rows': 7}
    else:
        report['SELF_CHECK.md'] = {'status': 'not_present_not_checked'}
    return report


def walk_dicts(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_dicts(child)


def network_expectations(lineage):
    """Recover transport MIME/length from original receipts, not guessed file suffixes."""
    receipts = defaultdict(list)
    for path in (ROOT / 'evidence').rglob('*.json'):
        for item in walk_dicts(read_json(path)):
            url = item.get('requested_url') or item.get('url')
            mime = item.get('content_type') or item.get('mime')
            if isinstance(url, str) and item.get('sha256') and isinstance(item.get('bytes'), int) and mime and item.get('status') in (200, '200'):
                receipts[(urldefrag(url)[0], item['sha256'])].append({'bytes': item['bytes'], 'mime': str(mime).split(';', 1)[0].strip().lower(), 'record': path.relative_to(ROOT).as_posix()})
    targets = []
    for row in lineage:
        for kind in ('body', 'payload'):
            url = urldefrag(row[f'{kind}_url'])[0]
            digest = row[f'{kind}_sha256']
            baseline = receipts[(url, digest)]
            require(baseline, f'No original MIME/length receipt for {row["case_id"]}/{row["version"]}/{kind}')
            lengths = {b['bytes'] for b in baseline}
            require(len(lengths) == 1, f'Conflicting original lengths: {url}')
            mimes = sorted({b['mime'] for b in baseline})
            if kind == 'payload':
                require(next(iter(lengths)) == int(row['payload_bytes']), f'CSV/receipt length differs: {url}')
                require(row['payload_mime'].split(';', 1)[0] in mimes, f'CSV/receipt MIME differs: {url}')
            targets.append({'case_id': row['case_id'], 'version': row['version'], 'edition': row['edition'], 'kind': kind,
                            'url': url, 'expected_sha256': digest, 'expected_bytes': next(iter(lengths)),
                            'expected_transport_mime': mimes, 'original_receipt': baseline[0]['record']})
    require(len(targets) == 24, 'Network plan must contain 12 bodies and 12 primary payloads')
    return targets


def local_check():
    seals = verify_frozen()
    freeze = read_json(ROOT / 'freeze.json')
    cases = {c['case_id']: c for c in freeze['cases']}
    require(set(cases) == CASE_IDS and len(freeze['cases']) == 6, 'Frozen six-case population changed')
    frame = read_csv(ROOT / 'frame.csv')
    for project in ('Matplotlib', 'CPython', 'ggplot2'):
        candidates = [r for r in frame if r['project'] == project]
        require(candidates, f'Missing frame: {project}')
        ordered = sorted(candidates, key=lambda r: int(r['candidate_order']))
        require([int(r['candidate_order']) for r in ordered] == list(range(1, len(ordered) + 1)), f'Frame order gap: {project}')
        paths = [r['relative_path'] for r in ordered]
        require(paths == sorted(paths) and len(set(paths)) == len(paths), f'Frame paths not distinct lexical order: {project}')
        chosen = {r['relative_path'] for r in ordered if r['selection'] == 'selected'}
        require(chosen == {c['page_path'] for c in cases.values() if c['project'] == project}, f'Frame/freeze selection differs: {project}')
        for row in ordered:
            require('2023-01-01' <= row['old_release_date'][:10] <= '2025-12-31', f'Out-of-interval release: {project}')
    predictions = read_csv(ROOT / 'predictions.csv')
    require(len(predictions) == 6 and {r['case_id'] for r in predictions} == CASE_IDS, 'Predictions must retain exactly six cases')
    for row in predictions:
        c = cases[row['case_id']]
        for key in ('project', 'old_version', 'new_version'):
            require(row[key] == c[key], f'Prediction/freeze {key} differs: {row["case_id"]}')
        old = tuple(map(int, c['old_version'].split('.')))
        new = tuple(map(int, c['new_version'].split('.')))
        require(old[2] == 0 and old[:2] == new[:2] and new[2] > 0, 'Stable x.y.0 and subsequent patch required')
        require(row['old_section_uri'] == c['old_uri'] and row['old_asset_path'] == c['asset_path'], f'Prediction target changed: {row["case_id"]}')
        require(row['prediction_U'] in {'YES', 'NO', 'HOLD', 'UNKNOWN'}, 'Invalid prediction value')
        require(int(row['new_body_asset_ci_reads']) == 0, 'Pre-seal outcome exposure must be disclosed, not accepted as unexposed')
        if bool_value(row['listing_complete']) and int(row['exact_path_count']) == 1:
            require(row['prediction_U'] == 'YES', f'Frozen exact-path rule not followed: {row["case_id"]}')
    lineage = read_csv(ROOT / 'lineage.csv')
    require(len(lineage) == 12, 'Lineage must retain 12 slots')
    require({(r['case_id'], r['edition']) for r in lineage} == {(c, e) for c in CASE_IDS for e in ('old', 'new')}, 'Lineage slot duplication/missing')
    for row in lineage:
        c = cases[row['case_id']]
        require(row['version'] == c[f'{row["edition"]}_version'], f'Wrong lineage version: {row["case_id"]}')
        for key in AXES:
            require(row[key] in {'YES', 'NO', 'UNKNOWN'}, f'Invalid axis {key}')
        for key in ('source_sha256', 'body_sha256', 'payload_sha256'):
            require(re.fullmatch('[0-9a-f]{64}', row[key]), f'Invalid lineage digest {row["case_id"]}:{key}')
        for key in ('source_url', 'body_url', 'base_uri', 'payload_url', 'publication_record_url'):
            require(valid_url(row[key]), f'Invalid lineage URL {row["case_id"]}:{key}')
        require(int(row['payload_bytes']) > 0 and row['payload_mime'] == 'image/png', 'Primary PNG length/MIME missing')
        require(urljoin(row['base_uri'], row['literal_reference']) == row['payload_url'], f'Relative reference resolves elsewhere: {row["case_id"]}/{row["version"]}')
        require(row['section_locator'] and row['limitation'] and (ROOT / row['evidence']).is_file(), 'Scope/limitation/evidence missing')
        if row['G_build_generated'] == 'YES':
            require(valid_url(row['generation_record_url']), 'G=YES needs exact generation record URL')
    sources = [json.loads(line) for line in (ROOT / 'sources.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
    counted, categories, families, observed = source_counts(sources)
    counts = read_json(ROOT / 'evidence/counts.json')
    for key, actual in [('source_rows', len(sources)), ('unique_primary_sources', len(counted)), ('slots', 12), ('source_family_count', len(families))]:
        require(counts[key] == actual, f'counts.json differs: {key}')
    require(counts['categories'] == dict(categories), 'Category totals differ')
    require(counts['canonical_source_families'] == dict(families), 'Source-family totals differ')
    require(counts['minimums'] == MINIMUMS and counts['observed_minimums'] == observed, 'Minimum/count formula mismatch')
    require(counts['selected_publication_dataset_lineage_count'] == len(counts['selected_publication_dataset_lineages']) == 5, 'Selected publication/dataset lineages differ')
    require(set(counts['selected_publication_dataset_lineages']) <= set(families), 'Selected lineage has no counted evidence')
    pairs = []
    for prediction in predictions:
        actual = next(r['U_section_uses'] for r in lineage if r['case_id'] == prediction['case_id'] and r['edition'] == 'new')
        expected = prediction['prediction_U']
        verdict = ('UNASSESSABLE' if actual == 'UNKNOWN' else 'HELD' if expected in {'HOLD', 'UNKNOWN'} else
                   'TRUE' if expected == actual else 'FALSE_ATTRIBUTION' if expected == 'YES' else 'MISSED_CONNECTION')
        pairs.append({'case_id': prediction['case_id'], 'prediction_U': expected, 'observed_U': actual, 'verdict': verdict})
    require(counts['pairs'] == pairs and counts['prediction_counts'] == dict(Counter(p['verdict'] for p in pairs)), 'Prediction counts/pairs differ')
    assessable = sum(p['verdict'] in {'TRUE', 'FALSE_ATTRIBUTION', 'MISSED_CONNECTION'} for p in pairs)
    require(counts['assessable_prediction_denominator'] == assessable, 'Assessable denominator differs')
    axes = {label: dict(Counter(r[key] for r in lineage)) for label, key in zip(('P', 'U', 'G'), AXES)}
    require(all(counts[label] == value for label, value in axes.items()), 'Axis counts differ')
    targets = network_expectations(lineage)
    report = {'status': 'passed', 'utc': utc(), 'mode': 'local_read_only', 'head': git('rev-parse', 'HEAD').decode().strip(),
              'sealed_files_checked': len(seals), 'seals': seals, 'frame_rows': len(frame), 'lineage_slots': 12,
              'predictions': 6, 'prediction_counts': counts['prediction_counts'], 'assessable_denominator': assessable,
              'axes': axes, 'source_rows': len(sources), 'unique_primary_sources': len(counted),
              'observed_minimums': observed, 'source_families': len(families), 'documents': verify_documents(lineage),
              'network_plan': {'body_requests': 12, 'primary_png_requests': 12, 'archives': 0},
              'scope': 'Seal bytes, schema, dedup, counts, slots, URI resolution, known receipts and document structure. External factual truth and fresh-generation provenance are not certified.'}
    return report, targets


def fetch_target(target):
    record = {**target, 'started_utc': utc(), 'redirects': []}
    class Redirects(HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            record['redirects'].append({'from': req.full_url, 'status': code, 'to': newurl})
            return super().redirect_request(req, fp, code, msg, headers, newurl)
    try:
        with build_opener(Redirects()).open(target['url'], timeout=30) as response:
            data = response.read(16 * 1024 * 1024 + 1)
            require(len(data) <= 16 * 1024 * 1024, 'Response exceeds 16 MiB safety bound')
            mime = response.headers.get('Content-Type', '')
            record.update({'status': response.status, 'final_url': response.url, 'content_type': mime,
                           'bytes': len(data), 'sha256': sha(data)})
            record['sha256_matches'] = record['sha256'] == target['expected_sha256']
            record['length_matches'] = len(data) == target['expected_bytes']
            record['mime_matches'] = mime.split(';', 1)[0].strip().lower() in target['expected_transport_mime']
            if target['kind'] == 'payload':
                record['png_signature_matches'] = data.startswith(b'\x89PNG\r\n\x1a\n')
                if record['png_signature_matches'] and len(data) >= 24:
                    record['dimensions'] = list(struct.unpack('>II', data[16:24]))
            record['passed'] = response.status == 200 and all(record[k] for k in ['sha256_matches', 'length_matches', 'mime_matches']) and record.get('png_signature_matches', True)
    except HTTPError as exc:
        record.update({'status': exc.code, 'final_url': exc.url, 'error': str(exc), 'passed': False})
    except Exception as exc:
        record.update({'status': None, 'error': f'{type(exc).__name__}: {exc}', 'passed': False})
    record['finished_utc'] = utc()
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--network', action='store_true', help='Open only 12 exact HTML + 12 primary PNG URLs')
    parser.add_argument('--output', type=Path, help='New JSON receipt path; required with --network; existing files refused')
    args = parser.parse_args()
    if args.network != bool(args.output):
        parser.error('--network and --output NEW_FILE must be used together')
    if args.output and (args.output.exists() or not args.output.parent.is_dir()):
        parser.error('--output must be a nonexistent file in an existing directory')
    try:
        report, targets = local_check()
        if args.network:
            # Exclusive creation reserves a new destination and never overwrites evidence.
            with args.output.open('x', encoding='utf-8') as receipt:
                with ThreadPoolExecutor(max_workers=4) as executor:
                    observations = list(executor.map(fetch_target, targets))
                report.update({'mode': 'local_plus_fresh_network', 'network': observations,
                               'network_passed': sum(r['passed'] for r in observations),
                               'network_attempts': len(observations), 'finished_utc': utc(),
                               'status': 'passed' if all(r['passed'] for r in observations) else 'failed'})
                json.dump(report, receipt, ensure_ascii=False, indent=2)
                receipt.write('\n')
            public = {k: v for k, v in report.items() if k not in {'network', 'seals'}}
            public['new_receipt'] = str(args.output.resolve())
            print(json.dumps(public, ensure_ascii=False, indent=2))
            return 0 if report['status'] == 'passed' else 1
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({'status': 'failed', 'utc': utc(), 'error': f'{type(exc).__name__}: {exc}',
                          'scope': 'No original evidence files changed.'}, ensure_ascii=False, indent=2))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
