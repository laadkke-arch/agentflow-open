"""Make separate whitelisted route inputs, excluding search snippets and other routes."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
fields=['id','question_id','ledger','canonical_id','scope','whole_or_partial','title','initial_url','fixed_version','initial_text_file','initial_text_sha256','source_id','caller','input','output','limits','source_sections','whole_must','partial_must','independent_partial_purpose','independently_useful_next_action','remaining_adapter','preferences','original_named_families','original_named_components','named_component_roles','same_name_wrong_actor_output_failure','route_order']
for q in map(json.loads,(P/'questions.jsonl').read_text().splitlines()):
 d=P/'common'/q['id'];start=json.loads((d/'start.json').read_text())
 for route in ['A','B']:
  data={'question':{k:q[k] for k in fields if k in q},'common_open_receipts':[str(x.relative_to(P)) for x in sorted(d.glob('open-*.json'))],'common_baseline_return':f'common/{q["id"]}/baseline-return.json','common_provider_packet':{k:v for k,v in start.items() if k in ['question_id','opened','allowed_providers','budget','provider_pages','allowed_provider_ids','allowed_url_prefixes','common_start_status','budgets','instrumentation']},'input_commit':'3475576d56b4307bd75964b9a27dc2a60093efbf','isolation':'No search receipt, opposite route, later draft, 025 candidate list, supplementary source or current proposal body is authorized as route input.'}
  if route=='A':data['literal_queries']=q['a_queries']
  else:data['navigation_rule']='Follow actually observed common-provider links: table of contents/reference index, then API/type with greatest overlap with distinctive frozen input/output terms, then official example. Ties on-page order then lexical URL. At most two navigation/index requests, each response used as evidence also debits body limit. No new provider or guessed deep URL.'
  dest=P/'route-inputs'/route/f'{q["id"]}.json';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('Prepared 24 route-specific inputs.')
