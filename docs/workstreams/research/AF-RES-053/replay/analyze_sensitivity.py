#!/usr/bin/env python3
"""Analyze post-seal version sensitivity separately from main predictions."""
from pathlib import Path
import collections
import datetime
import json
import re
import xml.etree.ElementTree as ET
BASE=Path(__file__).resolve().parent
original=json.loads((BASE/'inputs/V03-original.json').read_text())
sections=[r['section'] for r in original['data']['values']]
receipts=json.loads((BASE/'sensitivity-render-receipts.json').read_text()); rows=[]
for rec in receipts:
    row=dict(run_id=rec['run_id'],status=rec['status'],input_sha256=rec['input']['sha256'])
    if rec['status']=='rendered':
        sg=json.loads((BASE/rec['scenegraph']['path']).read_text())
        labels=[r for r in sg if r['role']=='axis-label']
        target=[r for r in labels if r.get('datum',{}).get('value') in sections]
        svg=ET.parse(BASE/rec['svg']['path']).getroot();groups=[]
        for group in svg.iter():
            if 'role-axis-label' not in group.attrib.get('class','').split():continue
            text=[]
            for item in group:
                if item.tag.rsplit('}',1)[-1]!='text':continue
                style=dict(re.findall(r'([\w-]+)\s*:\s*([^;]+)',item.get('style','')))
                text.append({'text':''.join(item.itertext()),'fill':item.get('fill',style.get('fill'))})
            groups.append(text)
        y=next(g for g in groups if any(t['text']=='4. Hygiene & Cleaning' for t in g))
        vg=json.loads((BASE/rec['compiled']['path']).read_text())
        row.update(total_axis_labels=len(labels),y_axis_labels=len(target),other_axis_labels=len(labels)-len(target),
                   y_axis_identities_match=collections.Counter(r['datum']['value'] for r in target)==collections.Counter(sections),
                   scenegraph_y_colors=dict(collections.Counter(r['fill'] for r in target)),
                   svg_y_colors=dict(collections.Counter(r['fill'] for r in y)),
                   y_axis_rows=[{'identity':r['datum']['value'],'scenegraph_fill':r['fill'],'svg':t} for r,t in zip(target,y)],
                   condition_survives_in_compiled_code=('datum.value ===' in json.dumps(vg) or 'datum.resilience ===' in json.dumps(vg)),
                   normalized_red_count=sum(r['fill'].lower() in ['red','#f00','#ff0000'] for r in target),
                   normalized_black_count=sum(r['fill'].lower() in ['black','#000','#000000'] for r in target))
    else:row['error']=rec.get('error')
    rows.append(row)
equal=(BASE/'outputs/V03-v270-A.vega.json').read_bytes()==(BASE/'outputs/V03-v270-B.vega.json').read_bytes()
out={'analysis_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'classification':'Exploratory version sensitivity added after main prediction seal. No preregistered score.',
     'main_pair':{'compiler':'5.1.0','runtime':'5.20.2','A_y_labels':{'red':1,'black':9},'B_y_labels':{'red':0,'black':10}},
     'sensitivity_pair':{'compiler':'2.7.0','runtime':'4.4.0'},
     'same_input_bytes_as_main':True,'input_changes':[],
     'changed_environment':'Compiler plus its contemporaneous locked runtime and full dependency bundle; not compiler-only isolation.',
     'observations':rows,'A_B_compiled_JSON_byte_equal':equal,
     'conclusion':'2.7.0 omits both labelColor condition expressions from compiled output; A and B both leave all ten section labels black. The same input-level A is not an available behaviorally equivalent option on this old compiler.',
     'limits':['Not proof that the original author used 2.7.0 or 5.1.0. Schema v2 is not exact runtime evidence.',
               'Other old-version defaults differ: six x-axis tick labels appear in addition to ten section labels.',
               'Both old and new runs use modern Node and no native canvas.',
               'No input repair, new API, or hypothesis replacement was performed.'],
     'count_for_primary_minimum':False,'public_followup_works_added':0,'preregistered_prediction_rows_added':0}
(BASE/'sensitivity-results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'compiled_equal':equal,'observed_y_counts':[{k:r.get(k) for k in ['run_id','normalized_red_count','normalized_black_count','total_axis_labels','y_axis_labels']} for r in rows]},ensure_ascii=False))
