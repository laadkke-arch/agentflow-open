#!/usr/bin/env python3
"""Build the AF-RES-047 audit ledgers from preserved collection fragments.

This does not rerun the published scientific analyses or infer missing evidence.
All edits and output paths remain inside this workstream.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = ['RJ01', 'RJ02', 'RJ03', 'N-E00', 'N-E01', 'N-E02', 'RUN01', 'RUN02']
C_SLOTS = {
    'RJ01': 'author code present; research_data.xlsx and original run absent',
    'RJ02': 'contemporary input manifest and derived feature record present; original run receipt absent',
    'RJ03': 'author recipe present; saved Iris Rmonad object/session/run absent',
    'N-E00': 'contemporary author output present; WoRMS snapshot/query/run absent',
    'N-E01': 'missing contemporary BCO input manifest/run slot; no replacement by own RAAVEN output',
    'N-E02': 'contemporary author code present; actual RUC export/training run absent',
    'RUN01': 'local execution records present in two distinct artifact editions; external source and cross-stage identity unresolved',
    'RUN02': 'same-archive execution graph/log/output present; selected R1 publisher linkage confirmed by full bytes and exact-path publisher MD5; selected CHROM V unresolved',
}
ORIGINAL_NATURAL = ['RJ01', 'RJ02', 'RJ03', 'N-E01', 'N-E02', 'N-E03']
CATEGORIES = {
    'consumer': 'consumer_original', 'consumer_original': 'consumer_original',
    'original_run_report': 'consumer_original', 'consumer_or_run_report': 'consumer_original',
    'consumer_or_original_run': 'consumer_original',
    'publisher': 'publisher_edition_file_correction',
    'publisher_edition_file_correction': 'publisher_edition_file_correction',
    'publisher_editions_files': 'publisher_edition_file_correction',
    'author_record': 'author_contemporary_record',
    'author_contemporary_record': 'author_contemporary_record',
    'provenance_case': 'author_contemporary_record',
    'author_provenance': 'author_contemporary_record',
    'official_statistics': 'official_statistics', 'earth_science': 'earth_science',
    'supplementary': 'supplementary',
}
REQUIRED = {'consumer_original': 8, 'publisher_edition_file_correction': 8,
            'author_contemporary_record': 4, 'official_statistics': 2, 'earth_science': 2}


def read_json(path):
    return json.loads(path.read_text())


def truth(value):
    return value is True or str(value).lower() in ('true', '1', 'yes')


def pick(row, *keys, default=None):
    for key in keys:
        if key in row and row[key] is not None:
            return row[key]
    return default


def csv_read(path):
    with path.open(newline='') as f:
        return list(csv.DictReader(f))


def csv_write(path, rows, fields=None):
    if fields is None:
        fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value, ensure_ascii=False) if isinstance(value, (list, dict))
                             else value for key, value in row.items()})


def save_json(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def source_rows():
    all_rows = []
    files = [ROOT / 'collection' / group / 'sources.jsonl'
             for group in ('rjournal', 'essd', 'runs', 'domain')]
    files.append(ROOT / 'collection/root-reviews.jsonl')
    if (ROOT / 'collection/root-followups.jsonl').exists():
        files.append(ROOT / 'collection/root-followups.jsonl')
    if (ROOT / 'collection/review-reopens.jsonl').exists():
        files.append(ROOT / 'collection/review-reopens.jsonl')
    seen_admitted = {}
    for path in files:
        for number, line in enumerate(path.read_text().splitlines(), 1):
            if not line.strip():
                continue
            row = json.loads(line)
            original_count = truth(pick(row, 'minimum_count', 'count_toward_minimum', 'count_minimum', default=False))
            original_category = pick(row, 'allocation', 'quota_category', 'minimum_category', default='unallocated')
            category = CATEGORIES.get(original_category, original_category or 'unallocated')
            work = row['work_id']
            duplicate = row.get('duplicate_of')
            count = original_count
            count_reason = 'collection author admitted a directly read work; counted once across all ledgers'
            if count and work in seen_admitted:
                duplicate = duplicate or seen_admitted[work]
                count = False
                count_reason = 'cross-collection duplicate work; no additional minimum count'
            elif count:
                seen_admitted[work] = row['source_id']
            else:
                count_reason = 'not admitted to minimum in collection: duplicate, screening, metadata, failure or auxiliary without qualifying allocation'
            status = pick(row, 'access_status', 'status', default='미확인')
            item = {
                'source_id': row['source_id'], 'work_id': work,
                'edition_id': row.get('edition_id', '미확인'),
                'source_url': row.get('source_url', row.get('url', '미확인')),
                'final_url': row.get('final_url', row.get('source_url', row.get('url', '미확인'))),
                'publisher': row.get('publisher', '미확인'), 'kind': row.get('kind', '미확인'),
                'published_at': pick(row, 'published_at', 'published_date', 'publication_date', 'published', default='미확인'),
                'modified_at': pick(row, 'modified_at', 'modified_date', 'modified', default='미확인'),
                'opened_utc': pick(row, 'opened_utc', 'first_opened_utc', default='미확인'),
                'checked_utc': pick(row, 'checked_utc', 'semantic_verified_by_utc', 'opened_utc', default='미확인'),
                'time_precision': pick(row, 'timestamp_precision', 'first_open_precision', 'time_note', default='see original receipt'),
                'locator': row.get('locator', '미확인'),
                'observation': pick(row, 'observation', 'confirmed', 'observed', default='미확인'),
                'limitation': pick(row, 'limitation', 'limitations', default='미확인'),
                'questions': row.get('questions', []),
                'case_ids': pick(row, 'case_ids', 'cases', default=[]),
                'duplicate_of': duplicate,
                'count_toward_minimum': count,
                'minimum_category': category,
                'count_reason': count_reason,
                'access_status': status,
                'original_count_flag': original_count,
                'original_allocation': original_category,
                'collection_file': str(path.relative_to(ROOT)), 'collection_line': number,
                'tool_ref': pick(row, 'tool_ref', 'web_ref', default=None),
            }
            all_rows.append(item)
    return all_rows


def merge_frames():
    output = []
    groups = [('rjournal', 'frame.csv', 'consumer_first_RJournal'),
              ('essd', 'frame.csv', 'consumer_first_ESSD'),
              ('runs', 'frame-first30.csv', 'execution_first')]
    for group, filename, layer in groups:
        path = ROOT / 'collection' / group / filename
        rows = csv_read(path)
        assert len(rows) == 30, (group, len(rows))
        for number, row in enumerate(rows, 1):
            output.append({
                'stratum': layer, 'exposure_order': number,
                'publication_date': pick(row, 'publication_date', 'published', 'date', default='미확인'),
                'document_id': pick(row, 'document_id', 'doi', 'identifier', 'id', default='미확인'),
                'title': row.get('title', ''),
                'url': pick(row, 'url', 'source_url', 'landing_url', default='미확인'),
                'exposure_type': 'observed_metadata; body read only where explicitly recorded',
                'semantic_read': pick(row, 'semantic_read', 'body_read', default='see status and source ledger'),
                'status': pick(row, 'selection', 'status', 'decision', 'eligibility', default='미확인'),
                'selection_reason': pick(row, 'selection_reason', 'screening_reason', 'reason', 'eligibility_reason', default='see collection row'),
                'opened_utc': pick(row, 'first_opened_utc', 'opened_utc', default='see collection receipt'),
                'outcome_exposure': pick(row, 'outcome_exposure', default='see collection selection freeze'),
                'original_file': str(path.relative_to(ROOT)), 'original_csv_row': number + 1,
                'original_row': row,
            })
    csv_write(ROOT / 'frame.csv', output)


def load_cases():
    by_id = {}
    for group in ('rjournal', 'essd', 'runs'):
        path = ROOT / 'collection' / group / 'cases.json'
        rows = read_json(path)
        if isinstance(rows, dict):
            rows = rows.get('cases', rows)
        for row in rows:
            case = dict(row)
            case['stratum'] = ('consumer_first_RJournal' if case['case_id'].startswith('RJ') else
                               'consumer_first_ESSD' if case['case_id'].startswith('N-E') else 'execution_first')
            case['included_in_primary'] = case['case_id'] in PRIMARY
            case['source_collection'] = str(path.relative_to(ROOT))
            for flag in ['publisher_exists', 'specific_usage', 'run_link', 'value_checked', 'strict_positive']:
                case[flag] = truth(case.get(flag, False))
            case.setdefault('candidate_value_checked', False)
            case.setdefault('local_run_link', False)
            case['specific_usage_collection_original'] = case['specific_usage']
            if case['case_id'] == 'RUN01':
                case['specific_usage'] = False
                case['specific_usage_local'] = True
                case['specific_usage_scope_adjudication'] = 'U_external=0; original collection flag refers to archived local input. Preserved rather than silently counted as external publisher edition.'
            elif case['case_id'] == 'RUN02':
                case['specific_usage_local'] = True
            for configuration in ('A', 'B', 'C'):
                cfg = dict(case[configuration])
                if case['case_id'].startswith('RUN'):
                    cfg['specific_usage_local'] = truth(cfg.get('specific_usage', False))
                    cfg['specific_usage_collection_original'] = cfg.get('specific_usage', False)
                    cfg['specific_usage'] = cfg['specific_usage_local'] if case['case_id'] == 'RUN02' else False
                    cfg['local_run_link'] = truth(pick(cfg, 'local_run_link', 'record_run_link', default=False))
                case[configuration] = cfg
            by_id[case['case_id']] = case
    assert set(PRIMARY + ['N-E03']) <= set(by_id), sorted(by_id)
    return by_id


def consolidate():
    by_id = load_cases()
    primary = [by_id[key] for key in PRIMARY]
    save_json('cases.json', primary)
    save_json('legacy-cases.json', [by_id['N-E03']])
    consumer_fields = ['case_id', 'stratum', 'analysis_title', 'consumer_url', 'consumer_locator',
                       'purpose', 'target_time', 'input_name', 'field', 'reported_value', 'unit',
                       'usage_edition', 'usage_evidence', 'consumer_first_opened_utc',
                       'consumer_first_recorded_open_utc', 'publisher_first_opened_utc',
                       'publisher_first_recorded_open_utc', 'outcome_exposure',
                       'publisher_exists', 'specific_usage', 'run_link', 'value_checked',
                       'candidate_value_checked', 'local_run_link', 'strongest_claim',
                       'missing_reason', 'source_ids']
    csv_write(ROOT / 'consumers.csv', primary, consumer_fields)
    editions = []
    runs = []
    readings = []
    for group in ('rjournal', 'essd', 'runs'):
        base = ROOT / 'collection' / group
        for row_number, row in enumerate(csv_read(base / 'editions.csv'), 2):
            if row.get('case_id') in PRIMARY:
                editions.append({**row, 'source_collection': f'collection/{group}/editions.csv',
                                 'source_csv_row': row_number})
        for row_number, row in enumerate(csv_read(base / 'runs.csv'), 2):
            if row.get('case_id') in PRIMARY:
                runs.append({**row, 'source_collection': f'collection/{group}/runs.csv',
                             'source_csv_row': row_number})
    csv_write(ROOT / 'editions.csv', editions)
    csv_write(ROOT / 'runs.csv', runs)
    for case in primary:
        cumulative_urls = []
        for configuration in ('A', 'B', 'C'):
            cfg = case[configuration]
            cumulative_urls = list(dict.fromkeys(cumulative_urls + cfg.get('visible_urls', [])))
            values = cfg.get('visible_values')
            if values is None:
                if 'visible_value' in cfg:
                    values = [cfg['visible_value']] if cfg['visible_value'] is not None else ['미확인: C의 output 내부를 아직 추가하지 않은 구성']
                else:
                    values = [case['reported_value']]
            local_run = truth(pick(cfg, 'local_run_link', 'record_run_link', default=False))
            usage = truth(pick(cfg, 'publisher_usage_specific', 'usage_specific', 'specific_usage', 'consumer_usage_specific', default=False))
            if case['case_id'] == 'RUN01':
                usage = False
            packet_field, packet_time, packet_purpose = case['field'], case['target_time'], case['purpose']
            if configuration in ('A', 'B') and case['case_id'] == 'RUN01':
                packet_field = 'predictions.h5의 첫 논리적 데이터 열 coord_x; 행의 값·보조좌표는 C 미포함'
                packet_time = '공개 CPM 실행 보고; 두 판의 metadata publication_date=2023-02-25, v1.1 record created=2023-06-29; 상세 실행 시각은 C 미포함'
            elif configuration in ('A', 'B') and case['case_id'] == 'RUN02':
                packet_field = 'output gVCF 첫 비header 행의 CHROM; 값·POS·END·DP는 C 미포함'
                packet_time = '공개 NA12878 variant-calling 실행 보고; 상세 실행 timestamp와 로컬 파일 시각은 C 미포함'
                packet_purpose = '공개된 NA12878 variant-calling 분석. 구체 염색체 설정·input graph·출력의 값은 C 미포함.'
            readings.append({
                'case_id': case['case_id'], 'stratum': case['stratum'], 'configuration': configuration,
                'purpose': packet_purpose, 'target_time': packet_time, 'field': packet_field,
                'visible_urls': cumulative_urls,
                'visible_values': values,
                'exact_locations': cfg.get('evidence', '미확인'),
                'publisher_specific': truth(pick(cfg, 'publisher_specific', 'publisher_exists', 'publisher_edition_specific', default=False)),
                'usage_specific': usage,
                'local_usage_specific': truth(cfg.get('specific_usage_local', False)) if case['case_id'].startswith('RUN') else False,
                'run_link': truth(cfg.get('run_link', False)),
                'local_run_link': local_run,
                'value_checked': truth(pick(cfg, 'value_checked', 'same_field_value_checked', default=False)),
                'candidate_value_checked': truth(cfg.get('candidate_value_checked', False)),
                'record_reread': truth(cfg.get('record_reread', False)) or (configuration == 'C' and case['case_id'] in ['N-E00', 'RUN01', 'RUN02']),
                'judgment': cfg.get('judgment', '미확인'), 'new_fact': cfg.get('new_fact', '미확인'),
                'missing_reason': cfg.get('missing_reason', cfg.get('judgment', '미확인')),
                'C_slot_status': C_SLOTS[case['case_id']] if configuration == 'C' else 'not applicable',
                'audit_only_full_field': case['field'],
                'audit_only_full_purpose': case['purpose'],
                'audit_only_full_target_time': case['target_time'],
                'audit_only_full_missing_reason': case['missing_reason'],
                'packet_boundary': 'audit_only_* columns are excluded from A/B/C visible packet; not a blinded experiment',
            })
    csv_write(ROOT / 'readings.csv', readings)
    sources = source_rows()
    # A work can first appear as metadata and later be read as original content.
    # Keep those later locations attached to its single admitted representative.
    for source in sources:
        if source['count_toward_minimum']:
            source['same_work_content_evidence_source_ids'] = [other['source_id'] for other in sources
                if other['work_id'] == source['work_id'] and other['access_status'] not in
                ['metadata_only', 'failed', 'access_failed', 'authentication_redirect', 'tool_fetch_failed', 'unsupported_content_type']]
    (ROOT / 'sources.jsonl').write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in sources))
    admitted = [row for row in sources if row['count_toward_minimum']]
    allocation = Counter(row['minimum_category'] for row in admitted)
    save_json('source-count-summary.json', {
        'ledger_rows': len(sources),
        'conservative_unique_direct_works_admitted': len(admitted),
        'admitted_work_ids': [row['work_id'] for row in admitted],
        'allocation': dict(allocation),
        'required_allocation': REQUIRED,
        'quota_eligible_unique_works': sum(allocation.get(key, 0) for key in REQUIRED),
        'minimum24_met': len(admitted) >= 24,
        'minimum24_all_admitted_met': len(admitted) >= 24,
        'minimum24_required_roles_met': sum(allocation.get(key, 0) for key in REQUIRED) >= 24,
        'all_allocations_met': all(allocation.get(key, 0) >= n for key, n in REQUIRED.items()),
        'method': 'Same work counted once. Selection/screening metadata, mirrors, extra versions, failed access and revisits add zero. Supplementary works do not fill missing core quotas. Original admission flags and collection line retained.',
    })
    def counts(ids):
        rows = [by_id[key] for key in ids]
        return {'case_ids': ids, 'denominator': len(rows), **{
            flag: sum(bool(row.get(flag)) for row in rows)
            for flag in ('publisher_exists', 'specific_usage', 'run_link', 'local_run_link',
                         'value_checked', 'candidate_value_checked', 'strict_positive')},
            'strict_value_given_authenticated_run': '해당 없음' if not any(row['run_link'] for row in rows)
            else {'numerator': sum(row['value_checked'] and row['run_link'] for row in rows),
                  'denominator': sum(row['run_link'] for row in rows)}}
    save_json('analysis-summary.json', {
        'definitions': {'P': 'publisher distinguishable candidate edition exists',
                        'U': 'specific consumer usage declaration; byte validation separate',
                        'R': 'original execution linked through to the external publisher input object',
                        'R_local': 'execution linked to an archived local input only',
                        'V': 'authentic used edition and selected field independently corroborated',
                        'candidate_value': 'publisher candidate value matches without authentic usage identification'},
        'natural_primary_after_A01': counts(PRIMARY[:6]),
        'natural_original_before_A01': counts(ORIGINAL_NATURAL),
        'execution_supplement': counts(PRIMARY[6:]),
        'combined_descriptive_only': counts(PRIMARY),
        'configuration_counts': {cfg: {flag: sum(row[flag] for row in readings if row['configuration'] == cfg)
                                      for flag in ('publisher_specific', 'usage_specific', 'run_link', 'local_run_link',
                                                   'value_checked', 'candidate_value_checked', 'record_reread')}
                                 for cfg in ('A', 'B', 'C')},
        'warning': 'A/B/C are cumulative evidence-availability audits, not blinded experiments. Natural and run-first denominators remain separate.',
    })
    merge_frames()
    print(json.dumps({'cases': len(primary), 'readings': len(readings), 'editions': len(editions),
                      'run_rows': len(runs), 'source_rows': len(sources), 'admitted_works': len(admitted),
                      'allocation': dict(allocation)}, ensure_ascii=False))


if __name__ == '__main__':
    consolidate()
