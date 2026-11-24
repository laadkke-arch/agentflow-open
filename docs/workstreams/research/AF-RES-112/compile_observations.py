"""Rebuild exposure/answer ledgers from append-only recipient event files."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line]


def rows_to_csv(rows, fields):
    import io
    s = io.StringIO(newline='')
    w = csv.DictWriter(s, fields, lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    return s.getvalue()


def build():
    packets = read_jsonl(ROOT / 'packets.jsonl')
    trails, answers, summaries = [], [], []
    expected_real = 0
    for packet in packets:
        sid = packet['packet_id']
        event_paths = sorted((ROOT / 'readers' / sid / 'events').glob('*.json'))
        events = [json.loads(p.read_text()) for p in event_paths]
        by_type = {}
        for event in events:
            by_type.setdefault(event['type'], []).append(event)
        exposures = by_type.get('exposure', [])
        judgments = by_type.get('judgment', [])
        final = by_type.get('final', [])
        starts = by_type.get('start', [])
        choices = by_type.get('choice', [])
        if packet['status'] == 'ready':
            expected_real += 1
            assert len(starts) == 1, (sid, 'missing start')
            assert len(final) == 1, (sid, 'must have one final')
            assert len(exposures) == len(judgments) <= 3, sid
            assert sum(x['exposed_codepoints'] for x in exposures) <= 4500, sid
            assert starts[0]['input']['url'] == packet['url'], sid
            assert starts[0]['input']['request'] == packet['request'], sid
            assert starts[0]['input']['hint'] == packet['hint'], sid
        elif events:
            raise AssertionError((sid, 'vacant packet must not run'))
        for step in range(1, 4):
            exp = next((x for x in exposures if x['step'] == step), None)
            jud = next((x for x in judgments if x['step'] == step), None)
            if exp:
                assert len(exp['exposed_text']) == exp['exposed_codepoints'] <= 1500, sid
                assert len(exp['exposed_text'].encode()) == exp['exposed_utf8_bytes'], sid
                assert exp['at_utc'] <= jud['at_utc'], sid
                next_exp = next((x for x in exposures if x['step'] == step + 1), None)
                if next_exp:
                    assert jud['at_utc'] <= next_exp['at_utc'], sid
                copy = {**exp, 'case_id': packet['case_id'], 'condition': packet['condition'],
                        'exposed_sha256': hashlib.sha256(exp['exposed_text'].encode()).hexdigest()}
                copy['event_file'] = next(str(p.relative_to(ROOT)) for p, e in zip(event_paths, events) if e is exp)
                choice = next(e for e in choices if e['next_step'] == step)
                assert choice['at_utc'] <= exp['at_utc']
                copy['choice_event_file'] = next(str(p.relative_to(ROOT)) for p, e in zip(event_paths, events) if e is choice)
                copy['choice'] = choice
                connector_view = exp.get('transport', '').startswith('GitHub')
                copy['arrival_url_kind'] = 'connector_logical_source_address' if connector_view else 'observed_http_final_address'
                copy['http_final_url_observed'] = not connector_view
                copy['arrival_metadata_qualification'] = 'raw helper arrival_confirmed denotes connector display/source address, not observed HTTP redirect destination' if connector_view else 'urllib response final URL observed; expired signing query removed in metadata derivative'
                trails.append(copy)
                status = 'observed'
            else:
                status = 'not_recruited' if packet['status'] != 'ready' else 'early_stop'
            answers.append({
                'session': sid, 'case_id': packet['case_id'], 'condition': packet['condition'],
                'step': step, 'status': status,
                'disposition': jud['disposition'] if jud else '',
                'answer': jud.get('answer', '') if jud else '',
                'citations': json.dumps(jud.get('citations', []), ensure_ascii=False) if jud else '',
                'counterexample': jud.get('counterexample', '') if jud else '',
                'unknown': jud.get('unknown', '') if jud else packet.get('unexecuted_reason', 'early stop'),
                'prior_knowledge': jud.get('prior_knowledge', '') if jud else '',
                'source_url': exp['arrival_url'] if exp else '',
                'source_entry': exp.get('archive_entry') or '' if exp else '',
                'source_locator': json.dumps({'start': exp['source_view_start'], 'end': exp['source_view_end'],
                                             'capture_start': exp['capture_codepoint_start'],
                                             'capture_end': exp['capture_codepoint_end']}, ensure_ascii=False) if exp else '',
                'exposed_codepoints': exp['exposed_codepoints'] if exp else 0,
                'exposed_utf8_bytes': exp['exposed_utf8_bytes'] if exp else 0,
                'cumulative_codepoints': exp['cumulative_codepoints'] if exp else '',
                'cumulative_utf8_bytes': exp['cumulative_utf8_bytes'] if exp else '',
                'is_final_observed_step': bool(exp and step == len(exposures)),
                'final_disposition': final[0]['disposition'] if final and step == len(exposures) else '',
            })
        summaries.append({'session': sid, 'case_id': packet['case_id'], 'condition': packet['condition'],
                          'status': 'completed' if final else packet['status'],
                          'observed_steps': len(exposures),
                          'codepoints': sum(x['exposed_codepoints'] for x in exposures),
                          'utf8_bytes': sum(x['exposed_utf8_bytes'] for x in exposures),
                          'final': final[0] if final else None,
                          'started_at_utc': starts[0]['at_utc'] if starts else None,
                          'finished_at_utc': final[0]['at_utc'] if final else None})
    counts = {'planned_main_packets': len(packets), 'constructed_main_packets': expected_real,
              'completed_main_packets': sum(x['status'] == 'completed' for x in summaries),
              'not_recruited_packets': sum(x['status'] == 'not_recruited' for x in summaries),
              'planned_main_stage_positions': len(answers),
              'observed_main_stages': len(trails),
              'not_recruited_stage_positions': sum(x['status'] == 'not_recruited' for x in answers),
              'early_stop_stage_positions': sum(x['status'] == 'early_stop' for x in answers),
              'main_total_exposed_codepoints': sum(x['exposed_codepoints'] for x in trails),
              'main_total_exposed_utf8_bytes': sum(x['exposed_utf8_bytes'] for x in trails)}
    assert counts['planned_main_packets'] == 12
    assert counts['planned_main_stage_positions'] == 36
    assert sum(counts[k] for k in ['observed_main_stages','not_recruited_stage_positions','early_stop_stage_positions']) == 36
    return {'trails.jsonl': ''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in trails),
            'answers.csv': rows_to_csv(answers, list(answers[0])),
            'evidence/reader-summaries.json': json.dumps(summaries, ensure_ascii=False, indent=2) + '\n',
            'evidence/observation-counts.json': json.dumps(counts, ensure_ascii=False, indent=2) + '\n'}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--check', action='store_true')
    a = p.parse_args()
    outputs = build()
    for name, content in outputs.items():
        path = ROOT / name
        if a.check:
            assert path.read_text(encoding='utf-8') == content, name
        else:
            path.write_text(content, encoding='utf-8')
    print(json.dumps({'status': 'passed', 'mode': 'check' if a.check else 'rebuild',
                      'files': list(outputs)}, ensure_ascii=False))
