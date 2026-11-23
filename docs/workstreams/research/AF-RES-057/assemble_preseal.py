"""Materialize frozen comparisons from the input-only research streams."""
from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json

P = Path(__file__).resolve().parent
ORDER = ['YN1', 'YN2', 'YT1', 'PN1', 'PN2', 'PT1']


def dump_csv(name, data):
    fields = list(dict.fromkeys(k for row in data for k in row))
    with (P / name).open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(data)


def render(value):
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def normalize_sources():
    all_sources = []
    for stream in ['yjs', 'prosemirror', 'donors']:
        f = P / 'streams' / stream / 'sources.jsonl'
        if not f.exists():
            continue
        for raw in f.read_text().splitlines():
            if not raw.strip():
                continue
            r = json.loads(raw)
            row = {
                'source_id': r['source_id'], 'work_id': r['work_id'],
                'kind_lineage': r.get('kind_lineage', r.get('kind', '')),
                'questions_cases': r.get('questions_cases', r.get('questions', []) + r.get('cases', [])),
                'original_url': r.get('original_url', ''),
                'fixed_url': r.get('fixed_url', r.get('pinned_url', '')),
                'version_date_hash': r.get('version_date_hash', {'version': r.get('version', r.get('date_or_hash', '')), 'source_sha256': r.get('source_sha256', '')}),
                'opened_UTC': r.get('opened_UTC', r.get('read_UTC', '')),
                'time_precision': r.get('read_time_note', 'See stream acquisition/read log; metadata retrieval and model reading are distinct.'),
                'location': r.get('location', r.get('locator', '')),
                'findings': r.get('findings', r.get('verified', r.get('confirmed', ''))),
                'limits': r.get('limits', r.get('scope_and_limits', r.get('scope_limits', ''))),
                'evidence_type': r.get('evidence_type', ''),
                'contrary_source_ids': r.get('contrary_source_ids', r.get('counterevidence_ids', [])),
                'access_status': r.get('access_status', r.get('read_status', '')),
                'external_minimum_eligible': r.get('external_minimum_eligible', r.get('count_external_primary', r.get('eligible_external_work', r.get('eligible_primary', False)))) is True,
                'source_group': r.get('source_group', r.get('kind', '')),
                'selected_request': r.get('selected_request', r['source_id'] in ['P-I892', 'P-I1341']),
                'reader': r.get('reader', 'same-model ' + stream + ' research agent'),
                'raw_record_path': 'streams/' + stream + '/sources.jsonl'
            }
            all_sources.append(row)
    (P / 'sources.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in all_sources))
    return all_sources


def main():
    now = datetime.now(timezone.utc).isoformat()
    cases = {}
    for stream in ['yjs', 'prosemirror']:
        for c in json.loads((P / 'streams' / stream / 'cases.json').read_text())['cases']:
            cases[c['case_id']] = c
    donors = json.loads((P / 'streams/donors/windows.json').read_text())
    donor_for = {case: w for w in donors for case in w['cases']}
    root_d = {r['case_id']: r for r in json.loads((P / 'evidence/root-D-preparation.json').read_text())['predictions']}
    cards, predictions, events, windows = [], [], [], []
    for case in ORDER:
        c, d = cases[case], donor_for[case]
        api, example = c['api_card'], c['example_card']
        for suffix, source in [('A', api), ('E', example)]:
            windows.append({'window_id': case + '-' + suffix, 'source_id': source['source_id'], 'url': source['url'], 'location': source['location'], 'text': source['text'], 'words': len(source['text'].split()), 'code_lines': source.get('code_lines', 0), 'figures': source.get('figures', 0)})
        for view in ['A', 'E', 'D']:
            src = api if view == 'A' else example if view == 'E' else {'source_id': d['source_id'], 'url': d['original_url'], 'location': d['locator'], 'text': d['window'], 'code_lines': d['code_lines'], 'figures': d['figure_count']}
            card = {'card_id': case + '-' + view, 'case_id': case, 'view': view, 'api_window_id': case + '-A',
                    'added_window_id': '' if view == 'A' else case + '-E' if view == 'E' else d['window_id'],
                    'source_id': src['source_id'], 'url': src['url'], 'location': src['location'],
                    'display_window': src['text'], 'word_count': len(src['text'].split()), 'figure_count': src.get('figures', 0),
                    'code_lines': src.get('code_lines', 0), 'cut': src.get('cut', src.get('location', '')),
                    'prior_exposure': c['prior_exposure'],
                    'outside_window': src.get('outside_window', d.get('outside_window_seen', '') if view == 'D' else ''),
                    'previous_source_exposure': src.get('previous_exposure', ''),
                    'pair_budget_note': 'E/D additional words and figures match; A is shared. Code/prose density and full-source exposure do not match.'}
            cards.append(card)
            pred = c['draft_predictions'][view] if view != 'D' else root_d[case]['D_prediction_before_new_PM_E_read']
            is_pm = case.startswith('P')
            get = lambda k: render(pred.get(('normal_' if is_pm else '') + k, '미확인'))
            normal = {k: v for k, v in pred.items() if k.startswith('normal_')} if is_pm else {k: v for k, v in pred.items() if k.startswith('op')}
            boundary = {k: v for k, v in pred.items() if k.startswith('boundary_')} if is_pm else c.get('variant_predictions', c['boundary_input'])
            predictions.append({'prediction_id': case + '-' + view, 'case_id': case, 'view': view,
                                'layer': 'diagnostic' if case[1] == 'T' else 'natural', 'choice': pred['choice'],
                                'prediction_scope': c['original_vs_researcher'],
                                'opA_undo': get('opA_undo'), 'opB_undo': get('opB_undo'),
                                'opA_redo': get('opA_redo'), 'opB_redo': get('opB_redo'),
                                'preserved_other_edits': render(c['preserved_variables']),
                                'normal_prediction': render(normal), 'boundary_prediction': render(boundary),
                                'basis': pred.get('basis', pred.get('reason', '')),
                                'donor_increment': root_d[case]['D_reason'] if view == 'D' else '',
                                'card_ids': case + '-A' + (';' + case + '-' + view if view != 'A' else ''),
                                'exposure_status': c['prior_exposure'],
                                'new_hit_eligible': 'no: semantic answer exposed via E before seal' if case == 'PT1' else 'only original assertion for opA; extensions separate' if case == 'YT1' else 'original exact matching/answer exposure limits; no blanket new-hit credit',
                                'prepared_UTC': now})
        for i, event in enumerate(c['events'], 1):
            events.append({'event_id': event.get('event_id', case + '-e' + str(i)), 'case_id': case, 'variant': 'source-described/main normalization; see provenance',
                           'sequence': i, 'actor': event.get('actor', ''), 'origin': event.get('origin', '미명시'),
                           'initial_state': c['initial_state'], 'operation': event.get('call', event.get('action', '')),
                           'changed_property': event.get('changed_property', event.get('content', '')),
                           'opA': render(c['opA']), 'opB': render(c['opB']), 'provenance': c['original_vs_researcher']})
        for variant in ['normal_input', 'boundary_input']:
            events.append({'event_id': case + '-' + variant, 'case_id': case, 'variant': variant, 'sequence': 'see JSON event order', 'actor': 'explicit in variant JSON',
                           'origin': 'explicit in variant JSON', 'initial_state': c['initial_state'], 'operation': render(c[variant]),
                           'changed_property': render(c['preserved_variables']), 'opA': render(c['opA']), 'opB': render(c['opB']), 'provenance': c['original_vs_researcher']})
    for d in donors:
        windows.append({'window_id': d['window_id'], 'source_id': d['source_id'], 'url': d['pinned_url'], 'location': d['locator'], 'text': d['window'], 'words': d['word_count'], 'code_lines': d['code_lines'], 'figures': d['figure_count']})
    (P / 'cases.json').write_text(json.dumps({'prepared_UTC': now, 'cases': [cases[k] for k in ORDER]}, ensure_ascii=False, indent=2) + '\n')
    (P / 'evidence/card-windows.json').write_text(json.dumps(windows, ensure_ascii=False, indent=2) + '\n')
    dump_csv('cards.csv', cards)
    dump_csv('predictions.csv', predictions)
    dump_csv('events.csv', events)
    sources = normalize_sources()
    freeze_files = ['cases.json', 'cards.csv', 'predictions.csv', 'events.csv', 'frame.csv', 'evidence/card-windows.json', 'evidence/root-D-preparation.json', 'streams/yjs/cases.json', 'streams/prosemirror/cases.json', 'streams/donors/windows.json']
    hashes = {f: hashlib.sha256((P / f).read_bytes().replace(b'\r\n', b'\n')).hexdigest() for f in freeze_files}
    for f in freeze_files:
        data = (P / f).read_bytes()
        if b'\r\n' in data:
            (P / f).write_bytes(data.replace(b'\r\n', b'\n'))
    (P / 'evidence/prediction-freeze.json').write_text(json.dumps({'prepared_UTC': now, 'phase': 'pre-outcome; remote seal SHA recorded in following receipt', 'cases': ORDER, 'file_sha256': hashes, 'newline_rule': 'LF normalized before seal; Git and working hashes identical', 'exposure_note': 'Selected assertions withheld; related E assertion exposure disclosed, especially PT1. D preparation preceded corrected PM E delivery but is not an independently blinded participant.'}, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cases': len(cases), 'cards': len(cards), 'predictions': len(predictions), 'events': len(events), 'sources': len(sources)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
