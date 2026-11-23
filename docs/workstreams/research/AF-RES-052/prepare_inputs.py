"""Normalize the already sealed local ledgers; no network or candidate reading."""
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parent
SLOTS = ['P-N1','P-N2','M-N1','M-N2','P-S1','P-S2','M-S1','M-S2']

def read(path):
    with (ROOT / path).open(newline='') as f:
        return list(csv.DictReader(f))

def write(path, rows, fields=None):
    fields = fields or list(dict.fromkeys(k for r in rows for k in r))
    with (ROOT / path).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)

def pool(row, origin, diagnostic):
    case = row.get('slot_id') or row.get('pool_id')
    rank = int(row['original_rank'])
    return dict(pool_row_id=f'{case}-R{rank}', case_id=case,
        layer='diagnostic' if diagnostic else 'supplemental',
        source_row_id=row.get('row_id', row.get('pool_row_id')),
        origin_file=origin, purpose_id=row.get('purpose_id',row.get('requirement_id','')),
        catalog_url=row['catalog_url'], catalog_commit=row['catalog_commit'],
        catalog_blob=row['catalog_blob'], section=row.get('heading',row.get('section')),
        source_line=row['source_line'], original_rank=rank,
        label=row.get('display_name',row.get('label')),
        description=row.get('description',''),
        description_locator=row.get('description_source_lines',row['source_line']),
        description_characters=row.get('description_characters',''),
        description_sha256=row.get('description_sha256',''),
        exact_url=row['exact_url'], raw_target=row.get('raw_target',row['exact_url']),
        upstream=row['upstream'],component=row['component'],
        public_purpose=row.get('public_use',row.get('public_purpose','')),
        product_version=row['product_version'],document_role=row['document_role'],
        missing_fields=row['missing_fields'],
        prior_body_exposure=row.get('body_exposure_before_array','no'),
        destination_opened_before_array=row.get('destination_opened','False'))

def groups(cases, pools, status):
    rows=[]
    for case in cases:
        ps=sorted([p for p in pools if p['case_id']==case],key=lambda p:p['original_rank'])
        for method in 'ABC':
            gs={}
            for p in ps:
                rank=p['original_rank']
                fields=[p[k] for k in ('upstream','component','public_purpose','product_version','document_role')]
                key = (p['exact_url'] or f'unresolved:{rank}') if method=='A' else ((p['upstream'] or f'unknown:{rank}') if method=='B' else ('|'.join(fields) if all(fields) else f'unknown:{rank}'))
                gs.setdefault(key,[]).append(rank)
            all_groups=[{'key':k,'representative':v[0],'members':v} for k,v in gs.items()]
            visible=all_groups[:3]
            rows.append(dict(group_row_id=f'{case}-{method}',case_id=case,method=method,
                representatives=json.dumps([g['representative'] for g in visible]),
                hidden_siblings=json.dumps([v for g in visible for v in g['members'][1:]]),
                cut_groups=json.dumps([g['representative'] for g in all_groups[3:]]),
                all_groups=json.dumps(all_groups,ensure_ascii=False),
                status=status.get(case,'diagnostic_only'),
                prior_body_exposure='routing README same work' if case=='D-M1' else 'none',
                target_layer='diagnostic' if case.startswith('D-') else 'primary'))
    return rows

frame=[]
slots=[]
pools=[]
diagnostics=[]
for domain in ['python','markdown']:
    pref=f'evidence/{domain}/'
    for r in read(pref+'frame.csv'):
        frame.append(dict(record_kind='issue_screen',origin_file=pref+'frame.csv',**r))
    for r in read(pref+'slot-status.csv'):
        case=r['slot_id']
        rr=dict(slot_id=case,layer='natural' if '-N' in case else 'supplemental',
            purpose_id=case if '-N' in case else r.get('purpose_id',r.get('requirement_id','')),
            catalog_section=r.get('section',r.get('catalog_section','')),
            pool_size=int(r.get('candidate_count',r.get('pool_size',0))),
            status=r.get('selection_status',r.get('status','')),
            missing=r.get('missing',''),origin_file=pref+'slot-status.csv')
        slots.append(rr)
        frame.append(dict(record_kind='slot_selection',row_id=case+'-STATUS',**rr))
    scan='functional-scan.csv' if domain=='python' else 'section-scan.csv'
    for r in read(pref+scan):
        frame.append(dict(record_kind='catalog_section_screen',domain=domain,origin_file=pref+scan,**r))
    pools.extend(pool(r,pref+'pools.csv',False) for r in read(pref+'pools.csv'))
    diagnostics.extend(pool(r,pref+'diagnostic-pools.csv',True) for r in read(pref+'diagnostic-pools.csv'))

slots.sort(key=lambda r:SLOTS.index(r['slot_id']))
write('frame.csv',frame)
write('slots.csv',slots)
write('pools.csv',pools)
write('groups.csv',groups(SLOTS,pools,{r['slot_id']:r['status'] for r in slots}))
write('evidence/diagnostic-pools.csv',diagnostics)
write('evidence/diagnostic-groups.csv',groups(['D-P1','D-M1'],diagnostics,{}))
print(json.dumps({'issue_rows':sum(r['record_kind']=='issue_screen' for r in frame),
    'section_screen_rows':sum(r['record_kind']=='catalog_section_screen' for r in frame),
    'primary_slots':len(slots),'primary_pool_rows':len(pools),'primary_group_rows':len(SLOTS)*3,
    'diagnostic_pool_rows':len(diagnostics)},ensure_ascii=False))
