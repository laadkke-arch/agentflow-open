#!/usr/bin/env python3
"""Read actual frozen-run SVG/scenegraph; never change a renderer input."""
from pathlib import Path
import collections
import csv
import datetime
import hashlib
import json
import math
import re
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parent
def load(path): return json.loads((BASE / path).read_text())
def save(path, data): (BASE / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
def unescape(s): return re.sub(r'\\([.\[\]\\])', r'\1', s)
def canon(x): return json.dumps(x, sort_keys=True, ensure_ascii=False)
def counter(values): return collections.Counter(values)
def color(c):
    c = c.lower().replace(' ', '')
    if c in ('black', '#000', '#000000', 'rgb(0,0,0)'): return 'black'
    if c in ('red', '#f00', '#ff0000', 'rgb(255,0,0)'): return 'red'
    return c

def svg_role(path, role):
    root = ET.parse(BASE / path).getroot()
    rows = []
    for group in root.iter():
        if 'role-' + role not in group.attrib.get('class', '').split(): continue
        for item in group:
            if item.tag.rsplit('}', 1)[-1] == 'text':
                rows.append(dict(text=''.join(item.itertext()), fill=item.get('fill'),
                                 opacity=item.get('opacity'), transform=item.get('transform')))
    return rows

def v02(receipt):
    if receipt['status'] != 'rendered':
        return dict(run_id=receipt['run_id'], status='compile_failed',
                    error=receipt['error']['message'], svg_exists=False,
                    inference='Original frozen B does not supply accessible values or titles because compilation stops. No empty SVG or wrong-point rendering was observed.')
    spec=load(receipt['input']['path']); vg=load(receipt['compiled']['path']); sg=load(receipt['scenegraph']['path'])
    groups=vg['marks']; cells=[]
    axis_text=[r for r in sg if r['role']=='axis-title']
    actual_svg_titles=svg_role(receipt['svg']['path'],'axis-title')
    for i, group in enumerate(groups):
        symbol=next(m for m in group['marks'] if m['type']=='symbol')
        update=symbol['encode']['update']
        x_field=next(x['field'] for x in reversed(update['x']) if isinstance(x.get('field'),str))
        y_field=next(y['field'] for y in reversed(update['y']) if isinstance(y.get('field'),str))
        expected_x=unescape(spec['repeat']['column'][i%4]); expected_y=unescape(spec['repeat']['row'][i//4])
        points=[p for p in sg if p['role']=='mark' and p['marktype']=='symbol' and p['name']==symbol['name']]
        axes=[a for a in group['axes'] if 'title' in a]
        titles=[]
        for axis in axes:
            texts=[t for t in axis_text if t['datum']['scale']==axis['scale']]
            expected=expected_x if axis['orient']=='bottom' else expected_y
            titles.append(dict(scale=axis['scale'], orient=axis['orient'], field=expected,
                               compiled_title=axis['title'], scenegraph_text=[t['text'] for t in texts],
                               correspond=axis['title']==expected and len(texts)==1 and texts[0]['text']==expected))
        observed_values=[dict(x=p['datum'].get(unescape(x_field)), y=p['datum'].get(unescape(y_field)),
                              x_position=p.get('x'), y_position=p.get('y'), color=p.get('stroke')) for p in points]
        cells.append(dict(cell=i,row=i//4,column=i%4,group=group['name'],
                          x_field=x_field,y_field=y_field,expected_literal_x=expected_x,expected_literal_y=expected_y,
                          field_correspondence=unescape(x_field)==expected_x and unescape(y_field)==expected_y,
                          titles=titles, point_count=len(points), observed_values=observed_values,
                          datum_matches_input=counter(canon(p['datum']) for p in points)==counter(canon(r) for r in spec['data']['values']),
                          positions_finite=all(isinstance(p.get(k),(int,float)) and math.isfinite(p[k]) for p in points for k in ['x','y'])))
    legend=[r['text'] for r in sg if r['role']=='legend-title']
    svg_legend=svg_role(receipt['svg']['path'],'legend-title')
    expected_color=unescape(spec['spec']['encoding']['color']['field'])
    save('outputs/'+receipt['run_id']+'.cell-checks.json',cells)
    return dict(run_id=receipt['run_id'], status='rendered', cell_count=len(cells),
                point_count=sum(c['point_count'] for c in cells), observed_axis_title_count=len(axis_text),
                all_cell_fields_correspond=all(c['field_correspondence'] for c in cells),
                all_input_datums_preserved=all(c['datum_matches_input'] for c in cells),
                all_positions_finite=all(c['positions_finite'] for c in cells),
                all_titles_correspond=all(t['correspond'] for c in cells for t in c['titles']),
                axis_scenegraph_svg_text_multiset_equal=counter(t['text'] for t in axis_text)==counter(t['text'] for t in actual_svg_titles),
                legend_title=legend, expected_legend_field=expected_color,
                legend_title_corresponds=legend==[expected_color] and [t['text'] for t in svg_legend]==legend,
                title_backslash_count=sum(t['text'].count('\\') for t in axis_text)+sum(t.count('\\') for t in legend),
                cell_checks='outputs/'+receipt['run_id']+'.cell-checks.json',
                number_note='Counts are observed after rendering, not added numerical pre-registered predictions.')

def v03(receipt):
    if receipt['status']!='rendered': return dict(run_id=receipt['run_id'],status='failed',error=receipt.get('error'))
    sg=load(receipt['scenegraph']['path']); spec=load(receipt['input']['path'])
    labels=[r for r in sg if r['role']=='axis-label']
    svg=svg_role(receipt['svg']['path'],'axis-label')
    original=[r['section'] for r in spec['data']['values']]
    expected={s: ('red' if receipt['operation']=='A' and s=='4. Hygiene & Cleaning' else 'black') for s in original}
    observed=[]
    for index, label in enumerate(labels):
        identity=label['datum']['value']; svg_item=svg[index] if index<len(svg) else {}
        observed.append(dict(axis_identity=identity, scenegraph_text=label['text'],
                             scenegraph_fill=color(label['fill']), svg_text=svg_item.get('text'),
                             svg_fill=color(svg_item.get('fill') or ''), expected_color=expected.get(identity),
                             color_matches=color(label['fill'])==expected.get(identity) and color(svg_item.get('fill') or '')==expected.get(identity),
                             svg_text_truncated=svg_item.get('text')!=label['text'],
                             axis_datum_keys=sorted(label['datum'])))
    save('outputs/'+receipt['run_id']+'.axis-checks.json',observed)
    return dict(run_id=receipt['run_id'],status='rendered',axis_label_count=len(labels),
                axis_identities_match_input=counter(x['axis_identity'] for x in observed)==counter(original),
                scenegraph_color_counts=dict(counter(x['scenegraph_fill'] for x in observed)),
                svg_color_counts=dict(counter(x['svg_fill'] for x in observed)),
                all_expected_colors_match=all(x['color_matches'] for x in observed) and len(labels)==len(svg)==10,
                target_svg_full_text=[x for x in observed if x['axis_identity']=='4. Hygiene & Cleaning'],
                svg_truncated_labels=sum(x['svg_text_truncated'] for x in observed),
                axis_only=True, legend_text_excluded=True,
                axis_checks='outputs/'+receipt['run_id']+'.axis-checks.json')

receipts=load('render-receipts.json')
rows=[v02(r) if r['requirement_id']=='V02' else v03(r) for r in receipts]
by_id={x['run_id']:x for x in rows}
normal_equal=(BASE/'outputs/V02-normal-A.svg').read_bytes()==(BASE/'outputs/V02-normal-B.svg').read_bytes()
def v02_good(r):
    return r['status']=='rendered' and all(r[k] for k in ['all_cell_fields_correspond','all_input_datums_preserved','all_positions_finite','all_titles_correspond','axis_scenegraph_svg_text_multiset_equal','legend_title_corresponds']) and r['title_backslash_count']==0
v02_matches=all(v02_good(by_id[x]) for x in ['V02-normal-A','V02-normal-B','V02-boundary-A']) and by_id['V02-boundary-B']['status']=='compile_failed'
v03_matches=all(by_id[x]['all_expected_colors_match'] for x in ['V03-fixed-A','V03-fixed-B'])
matches=[]
for requirement, good in [('V02',v02_matches),('V03',v03_matches)]:
    for view in ['N','I','D']:
        matches.append(dict(prediction_id=requirement+'-'+view, frozen_choice='A만',
                            observed_researcher_choice='A만' if good else '미확인',
                            categorical_comparison='일치' if good else '검토 필요',
                            historical_same_version_scoring='미확인; author renderer patch unknown',
                            new_D_over_I=False,
                            qualification='B compilation error is an observed failure mode; no B rendered point-loss image exists.' if requirement=='V02' else 'Fixed 10-row original sample only; A identity predicate does not generalize to changed zero-category.'))
summary=dict(analysis_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
             frozen_sha='9b13473a76a381fe27d775524aa65416ec28f591',
             panel='researcher replay only',compiler='5.1.0',runtime='5.20.2',
             attempted_variant_runs=6,rendered_svg_runs=sum(r['status']=='rendered' for r in receipts),
             compile_failed_runs=sum(r['status']=='failed' for r in receipts),
             normal_A_B_identical_SVG=normal_equal,observations=rows,prediction_comparison=matches,
             comparison_denominators={'requirements':2,'NID_rows':6,'attempted_A_B_variant_runs':6,
                                      'D_new_correct_over_I':0,'D_I_ties':2,
                                      'historical_author_same_patch_confirmations':0,'public_followup_works_added':0},
             limits=['No full expected SVG was pre-registered; frozen categorical predictions only.',
                     'Node 24 modern host, no native canvas; text width estimated by pinned scenegraph package.',
                     'V02 normal is researcher key-renaming control, not author external normal example.',
                     'V03 original schema v2 retained; actual compiler is 5.1.0.',
                     'SVG structural/semantic inspection is not a raster/font-fidelity measurement or reader study.'])
save('results.json',summary)
with (BASE/'prediction-comparison.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(matches[0]));writer.writeheader();writer.writerows(matches)
print(json.dumps({k:summary[k] for k in ['attempted_variant_runs','rendered_svg_runs','compile_failed_runs','normal_A_B_identical_SVG','comparison_denominators']},ensure_ascii=False))
for r in rows:
    print(json.dumps({k:v for k,v in r.items() if k not in ['target_svg_full_text']},ensure_ascii=False))
