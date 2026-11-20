"""Render authored discussion with counts from explicit judgments, not invented prose."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'evidence/RESULT_DISCUSSION.template.md'


def render():
    a = json.loads((ROOT / 'evidence/AGGREGATES.json').read_text())
    assert not a['pending'], 'Finish every candidate judgment before rendering.'
    assert all(a['baselines'][b]['complete_all_cases'] for b in ['A', 'B'])
    values = {}
    for b in ['A', 'B']:
        d = a['baselines'][b]
        mapping = {'ID':'identity_hit_count', 'H':'historical_hit_count',
                   'TOTAL':'candidate_count', 'USE':'nongold_useful',
                   'NONGOLD':'nongold_candidates_judged', 'HUSE':'nongold_historical_useful',
                   'NARROW':'nongold_useful_with_narrowed_H',
                   'ALLPASS':'nongold_useful_all_H_pass', 'BROKEN':'broken_or_fake',
                   'EXPOSED':'exposed_run_count', 'RAW_H':'historical_hits_using_original_run_dates'}
        for short, key in mapping.items():
            values[b+'_'+short] = d[key]
        for short, key in [('N','cases'),('DEN','gold_denominator'),
                           ('ID','identity_hits'),('H','historical_hits')]:
            values[b+'_CLEAN_'+short] = d['clean_subset'][key]
        for short, kind in [('EXT','external_entity'),('STRUCT','structural_design')]:
            m = a['match_kinds'][kind]['baselines'][b]
            values[b+'_'+short] = m['identity_hits']
            values[b+'_'+short+'_H'] = m['historical_hits']
        for short, key in [('MIN','candidate_count_range'),('QMIN','query_count_range'),
                           ('PMIN','opened_budget_range')]:
            values[b+'_'+short] = d[key][0]
            values[b+'_'+short.replace('MIN','MAX')] = d[key][1]
        ds = d['candidate_dates']
        values[b+'_DATES'] = '결정 전 {}/사후 {}/시점 미확인 {}'.format(
            ds.get('pre_decision',0), ds.get('post_decision',0), ds.get('unknown',0))
        values[b+'30_ID'] = a['original_thirty_sensitivity'][b+'_identity_hits']
        values[b+'30_H'] = a['original_thirty_sensitivity'][b+'_historical_hits']
    values.update(UNION_ID=a['union']['identity_hits'], UNION_H=a['union']['historical_hits'],
                  B_ONLY=a['union']['B_only_identity'])
    values['B_ENTITY_ONLY'] = a['mechanism_match_sensitivity']['B_without_Jed_mechanism_hit']['identity_hits']
    family = ['| 계열 | 사례 수 | 정답 분모 | A 동일/결정 전 | B 동일/결정 전 |',
              '|---|---:|---:|---:|---:|']
    for name, d in a['families'].items():
        row = [name, str(d['case_count']), str(d['gold_count'])]
        for b in ['A','B']:
            v = d['baselines'][b]
            row.append(f"{v['identity_hits']}/{d['gold_count']} · {v['historical_hits']}/{d['gold_count']}")
        family.append('| '+' | '.join(row)+' |')
    values['FAMILY_TABLE'] = '\n'.join(family)
    quality = ['| 고정 라벨 | A 후보 수/204 | B 후보 수/'+str(a['baselines']['B']['candidate_count'])+' |',
               '|---|---:|---:|']
    for label in ['DIRECT_DOCUMENTED','CONDITIONAL_TRANSFER','SURFACE_OR_CONSTRAINT_MISMATCH','INSUFFICIENT']:
        quality.append('| '+label+' | '+' | '.join(str(a['baselines'][b]['labels'].get(label,0)) for b in ['A','B'])+' |')
    values['QUALITY_TABLE'] = '\n'.join(quality)
    text = TEMPLATE.read_text()
    tokens = set(re.findall(r'@@([^@]+)@@', text))
    assert tokens <= values.keys(), tokens-values.keys()
    text = re.sub(r'@@([^@]+)@@', lambda m: str(values[m[1]]), text)
    # The authored source lives in evidence/, while RESULT.md lives at ROOT.
    def relink(m):
        target = m[1]
        if re.match(r'^[a-zA-Z]+:', target) or target.startswith('#'):
            return m[0]
        path, sep, anchor = target.partition('#')
        resolved = (TEMPLATE.parent/path).resolve()
        relative = resolved.relative_to(ROOT).as_posix()
        if path.endswith('/'):
            relative += '/'
        return ']('+relative+(sep+anchor if sep else '')+')'
    text = re.sub(r'\]\(([^\s)]+)\)', relink, text)
    result = ROOT/'RESULT.md'
    old = result.read_text() if result.exists() else ''
    prefix = old.split('## §2',1)[0] if '## §2' in old else ''
    result.write_text(prefix+text)
    print(json.dumps({'rendered':str(result.relative_to(ROOT)),'tokens':len(tokens)},ensure_ascii=False))


if __name__ == '__main__':
    render()
