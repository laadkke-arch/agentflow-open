"""Rebuild the prespecified deletion control separately from the main trials."""
import argparse
import hashlib
import json
from pathlib import Path
from compile_observations import read_jsonl, rows_to_csv

ROOT = Path(__file__).resolve().parent


def build():
    trails, answers, summaries = [], [], []
    for packet in read_jsonl(ROOT / 'negative-packets.jsonl'):
        sid = packet['packet_id']
        event_paths = sorted((ROOT / 'readers' / sid / 'events').glob('*.json'))
        events = [json.loads(p.read_text()) for p in event_paths]
        exposures = [e for e in events if e['type'] == 'exposure']
        judgments = [e for e in events if e['type'] == 'judgment']
        finals = [e for e in events if e['type'] == 'final']
        starts = [e for e in events if e['type'] == 'start']
        if packet['status'] == 'ready':
            assert len(starts) == len(finals) == 1
            assert len(exposures) == len(judgments) <= 3
            assert sum(e['exposed_codepoints'] for e in exposures) <= 4500
            for key in ('request', 'url', 'hint'):
                assert starts[0]['input'][key] == packet[key]
        else:
            assert not events
        for step in range(1, 4):
            exp = next((e for e in exposures if e['step'] == step), None)
            jud = next((e for e in judgments if e['step'] == step), None)
            if exp:
                assert len(exp['exposed_text']) == exp['exposed_codepoints'] <= 1500
                assert len(exp['exposed_text'].encode()) == exp['exposed_utf8_bytes']
                assert exp['at_utc'] <= jud['at_utc']
                later = next((e for e in exposures if e['step'] == step + 1), None)
                assert later is None or jud['at_utc'] <= later['at_utc']
                trails.append({**exp, 'case_id': packet['case_id'], 'condition': packet['condition'],
                               'event_file': str(event_paths[events.index(exp)].relative_to(ROOT)),
                               'exposed_sha256': hashlib.sha256(exp['exposed_text'].encode()).hexdigest()})
            answers.append({'session': sid, 'case_id': packet['case_id'], 'condition': packet['condition'],
                            'step': step, 'status': 'observed' if exp else 'not_recruited',
                            'disposition': jud['disposition'] if jud else '',
                            'answer': jud.get('answer', '') if jud else '',
                            'citations': json.dumps(jud.get('citations', []), ensure_ascii=False) if jud else '',
                            'counterexample': jud.get('counterexample', '') if jud else '',
                            'unknown': jud.get('unknown', '') if jud else packet['reason'],
                            'prior_knowledge': jud.get('prior_knowledge', '') if jud else '',
                            'exposed_codepoints': exp['exposed_codepoints'] if exp else 0,
                            'exposed_utf8_bytes': exp['exposed_utf8_bytes'] if exp else 0,
                            'is_final_observed_step': bool(exp and step == len(exposures)),
                            'final_disposition': finals[0]['disposition'] if finals and step == len(exposures) else ''})
        summaries.append({'session': sid, 'case_id': packet['case_id'],
                          'status': 'completed' if finals else 'not_recruited',
                          'steps': len(exposures), 'codepoints': sum(e['exposed_codepoints'] for e in exposures),
                          'utf8_bytes': sum(e['exposed_utf8_bytes'] for e in exposures),
                          'final': finals[0] if finals else None,
                          'started_at_utc': starts[0]['at_utc'] if starts else None,
                          'finished_at_utc': finals[0]['at_utc'] if finals else None})
    counts = {'planned_control_packets': 2, 'completed_control_packets': len([s for s in summaries if s['status'] == 'completed']),
              'planned_control_stage_positions': 6, 'observed_control_stages': len(trails),
              'not_recruited_control_stages': sum(a['status'] == 'not_recruited' for a in answers),
              'control_total_codepoints': sum(t['exposed_codepoints'] for t in trails),
              'control_total_utf8_bytes': sum(t['exposed_utf8_bytes'] for t in trails),
              'included_in_main_denominators': False}
    assert counts['observed_control_stages'] + counts['not_recruited_control_stages'] == 6
    return {'control-trails.jsonl': ''.join(json.dumps(t, ensure_ascii=False) + '\n' for t in trails),
            'control-answers.csv': rows_to_csv(answers, list(answers[0])),
            'evidence/control-summaries.json': json.dumps(summaries, ensure_ascii=False, indent=2) + '\n',
            'evidence/control-counts.json': json.dumps(counts, ensure_ascii=False, indent=2) + '\n'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for name, content in build().items():
        path = ROOT / name
        if args.check:
            assert path.read_text() == content, name
        else:
            path.write_text(content)
    print(json.dumps({'status': 'passed', 'mode': 'check' if args.check else 'rebuild'}))
