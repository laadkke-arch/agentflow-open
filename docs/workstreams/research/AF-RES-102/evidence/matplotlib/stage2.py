from pathlib import Path
import csv,json,datetime,hashlib
from fetch import ROOT
T=json.loads((ROOT/'cache/stage2-new-edition-tree.bin').read_bytes());M={x['path']:x for x in T['tree']};complete=T.get('truncated') is False
if not complete:
 raise RuntimeError('Incomplete publication tree: do not classify missing paths or seal predictions')
F=[x for x in csv.DictReader(open(ROOT/'frame.csv')) if x['eligible']=='YES'];F.sort(key=lambda x:x['hash_sha256'])
G=json.load(open(ROOT/'selected-general.json'))['selected'];Gpaths={x['old_section_path'] for x in G}
O=[]
for x in F:
 a=x['old_asset_path'];sp=x['source_path'];newsp=M.get(sp)
 r=dict(x);r.update({'legacy_asset_path_applicable':bool(a and x['asset_kind']=='external-relative'),'legacy_asset_path_present':a in M if a else None,'old_source_path_present':sp in M if sp else None,'new_blob_at_old_source_path':newsp.get('sha') if newsp else None,'corresponding_source_blob_changed':bool(newsp and newsp['sha']!=x['source_blob']),'new_body_same_path_present':x['page_path'] in M,'general_already_selected':x['old_section_path'] in Gpaths})
 r['A_eligible']=bool(r['legacy_asset_path_applicable'] and not r['legacy_asset_path_present'] and complete and not r['general_already_selected'])
 r['C_eligible']=bool(r['legacy_asset_path_applicable'] and r['legacy_asset_path_present'] and sp and (not r['old_source_path_present'] or r['corresponding_source_blob_changed']) and not r['general_already_selected'])
 O.append(r)
now=datetime.datetime.now(datetime.timezone.utc).isoformat();selected=[]
for letter,stratum,group in [('G','general',[next(r for r in O if r['old_section_path']==x['old_section_path']) for x in G]),('A','old_resource_absent',[r for r in O if r['A_eligible']][:2]),('C','resource_retained_source_changed',[r for r in O if r['C_eligible']][:2])]:
 for i in [1,2]:
  cid=f'MP-{letter}{i}'
  if i>len(group):
   selected.append({'case_id':cid,'project':'Matplotlib','stratum':stratum,'stratum_rank':i,'vacancy':True,'vacancy_reason':'No eligible candidates in frozen first-40 frame after general deduplication','prediction_U':'VACANT','prediction_utc':now,'new_body_asset_ci_reads':0});continue
  r=dict(group[i-1]);r.update({'case_id':cid,'stratum':stratum,'stratum_rank':i,'vacancy':False,'vacancy_reason':'','prediction_U':'YES' if r['legacy_asset_path_present'] else 'NO' if r['legacy_asset_path_applicable'] and complete else 'UNKNOWN','prediction_utc':now,'new_body_asset_ci_reads':0,'new_section_provisional_url':'https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/410d8388303fab638bbedbd1d2eace0e5efb0de9/3.7.0/'+r['old_section_path'],'new_resource_provisional_url':'https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/410d8388303fab638bbedbd1d2eace0e5efb0de9/3.7.0/'+r['old_asset_path'] if r['old_asset_path'] else '', 'rule_misses':'Intentionally ignores renamed/replaced/inline resources and retained-but-unused legacy paths. Exact-path existence is the sole U prediction signal.'});selected.append(r)
used={x['old_section_path'] for x in selected if not x['vacancy']}
supp=[x for x in O if x['old_section_path'] not in used][:20]
for i,r in enumerate(supp,1):r['supplemental_id']=f'MP-S{i:02}';r['supplemental_rank']=i
(ROOT/'all40-signals.json').write_text(json.dumps({'utc':now,'tree_complete':complete,'signals':O},ensure_ascii=False,indent=2)+'\n')
(ROOT/'selected-stage2.json').write_text(json.dumps({'selected_utc':now,'complete_tree':complete,'stratum_pools':{'general':len(G),'old_resource_absent':sum(x['A_eligible'] for x in O),'resource_retained_source_changed':sum(x['C_eligible'] for x in O),'inline_not_path_applicable':sum(not x['legacy_asset_path_applicable'] for x in O)},'selected':selected},ensure_ascii=False,indent=2)+'\n')
(ROOT/'supplemental-order.json').write_text(json.dumps({'frozen_utc':now,'rule':'Unselected members of the same first-40 eligible frame; same SHA256 ascending order; first20 maximum; auxiliary only','selected':supp},ensure_ascii=False,indent=2)+'\n')
fields=['case_id','project','stratum','stratum_rank','old_section_path','purpose','old_asset_path','source_path','source_blob','new_blob_at_old_source_path','legacy_asset_path_present','old_source_path_present','corresponding_source_blob_changed','new_body_same_path_present','hash_sha256','prediction_U','prediction_utc','vacancy','vacancy_reason','new_section_provisional_url','new_resource_provisional_url','new_body_asset_ci_reads','rule_misses']
with open(ROOT/'predictions.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(selected)
for x in selected:print({k:x.get(k) for k in ['case_id','old_section_path','old_asset_path','source_path','legacy_asset_path_present','old_source_path_present','corresponding_source_blob_changed','prediction_U','vacancy']})
print('POOLS',json.load(open(ROOT/'selected-stage2.json'))['stratum_pools'])
