"""Meaningful integrity checks for AF-RES-023's source-backed research artifacts.
Does not simulate the external catalogs, run brew, or certify unknown history.
"""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import json,csv,hashlib,re,subprocess,argparse
P=Path(__file__).resolve().parents[1];REPO=P.parents[3]
ap=argparse.ArgumentParser();ap.add_argument('--check-handoff',action='store_true');ap.add_argument('--no-write',action='store_true');args=ap.parse_args()
checks=[]
def check(name,condition,detail):
 checks.append({'check':name,'passed':bool(condition),'detail':detail})
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def cardhash(c):return hashlib.sha256(json.dumps(c,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
sources=json.loads((P/'sources.json').read_text());sids={s['id'] for s in sources}
events=[json.loads(z) for z in (P/'events.jsonl').read_text().splitlines() if z.strip()]
primary=[e for e in events if e['primary_sample']];eids={e['event_id'] for e in primary}
cit=list(csv.DictReader((P/'citations.csv').open()));cids={c['downstream_id'] for c in cit}
rec=list(csv.DictReader((P/'reconstruction.csv').open()));counts=json.loads((P/'evidence/counts.json').read_text())
check('unique_source_ids_and_urls',len(sids)==len(sources)==len({s['url'] for s in sources}),len(sources))
required=['id','url','version_or_date','accessed_at_utc','sections_read','confirmed','limits','used_in','event_ids','lineage']
bad=[(s['id'],k) for s in sources for k in required if k not in s or s[k] in [None,'']]
check('source_ledger_required_fields',not bad,bad)
mini=[s for s in sources if s.get('minimum_counted')]
cats=Counter(s['minimum_category'] for s in mini)
check('conservative_counts_match_ledger',len(mini)==38 and dict(cats)==counts['minimum_by_category'],dict(cats))
check('minimum_counted_are_direct_originals',all(s.get('directly_opened') is True for s in mini),[s['id'] for s in mini if not s.get('directly_opened')])
per=Counter(e['collector'] for e in primary)
check('eighteen_cases_four_systems_max_eight',len(primary)==18 and len(per)==4 and max(per.values())<=8,dict(per))
check('source_references_resolve',all(s in sids for e in events for s in e['source_ids']),len(events))
check('downstream_references_resolve',all(c in cids for e in events for c in e.get('downstream_ids',[])),len(cids))
check('seven_external_consumer_records',sum(c['independent_external_original'].lower()=='true' for c in cit)==7,{'all_rows':len(cit),'external_independent':sum(c['independent_external_original'].lower()=='true' for c in cit)})
check('wd_citation_function_mapped',next(c for c in cit if c['downstream_id']=='WD-C01')['required_function_version']!='미확인','P910 category')
check('eighteen_times_three_rows',len(rec)==54 and Counter(r['event_id'] for r in rec)==Counter({e:3 for e in eids}),len(rec))
check('one_each_representation',all({r['representation'] for r in rec if r['event_id']==e}=={'1','2','3'} for e in eids),sorted(eids))
check('no_unknown_case_removed',{r['event_id'] for r in rec}==eids and all(r['key_completeness_limit'] for r in rec),'all18 retain key gap/limit fields')
check('scoring_not_external_or_runtime',all(r['scorer'].startswith('/root; source-exposed') and r['actual_user_misrecommendation']=='미확인' for r in rec),'54 self-check rows')
versions=Counter(r['input_version'] for r in rec)
check('composite_execution_provenance',versions==Counter({'v3-carried-to-v4-identical':48,'v4-repair':6}),dict(versions))
for file in sorted((P/'evidence').glob('frozen-manifest*.json')):
 m=json.loads(file.read_text());bad=[f for f,h in m['sha256'].items() if digest(P/f)!=h]
 check('frozen_hashes_'+file.name,not bad,bad)
for file in sorted((P/'evidence').glob('answer-freeze*.json')):
 m=json.loads(file.read_text());bad=[r['answer_file'] for r in m['readers'] if digest(P/r['answer_file'])!=r['answer_sha256']]
 check('answer_hashes_'+file.name,not bad,bad)
for i in [1,2,3]:
 v3=json.loads((P/f'reconstruction/views/v3-view-{i}.json').read_text());v4=json.loads((P/f'reconstruction/views/v4-view-{i}.json').read_text())
 a={c['event_id']:c for c in v3['cards']};b={c['event_id']:c for c in v4['cards']}
 check(f'carry_forward_content_and_common_rules_{i}',all(cardhash(a[e])==cardhash(b[e]) for e in eids-{'MB05','SW03'}) and all(v3[k]==v4[k] for k in ['question','method','missing_rule']),'16 cards + question/method/missing_rule')
 views=[]
 for j in [1,2,3]:views.append({c['event_id']:c for c in json.loads((P/f'reconstruction/views/v4-view-{j}.json').read_text())['cards']})
 check(f'same_common_inputs_all_representations_{i}',all(all(views[0][e][k]==v[e][k] for k in ['saved_url','short_reason','current_lookup','common_missing']) for e in eids for v in views),'18 shared URLs/reasons/current observations/missing rules')
for r in rec:
 reader=json.loads((P/r['answer_file']).read_text());ans=next(a for a in reader['answers'] if a['event_id']==r['event_id'])
 assert ans['target_answer']==r['target_answer'] and ans['function_version_reason_answer']==r['function_version_reason_answer'] and ans['destination_decision']==r['destination_decision']
 card=next(c for c in json.loads((P/f"reconstruction/views/v4-view-{r['representation']}.json").read_text())['cards'] if c['event_id']==r['event_id'])
 assert cardhash(card)==r['visible_card_sha256'] and json.loads(r['visible_information'])==card
check('answers_and_visible_information_not_rewritten',True,'all54 original answer texts and card hashes matched')
for i in [1,2,3]:
 b=list(csv.DictReader((P/f'comparisons/B0{i}.csv').open()))
 check(f'six_case_bundle_{i}',len(b)==18 and len({r['event_id'] for r in b})==6,{'rows':len(b),'cases':len({r['event_id'] for r in b})})
ident=list(csv.DictReader((P/'identity-layers.csv').open()));rest=list(csv.DictReader((P/'restoration.csv').open()))
check('identity_independent_columns',len(ident)==18 and all(k in ident[0] for k in ['original_url','catalog_entity','work_recording_release_or_real_object','organization_department','project_distribution_version','use_substitutability']),len(ident))
check('five_restoration_dimensions_per_case',len(rest)==90 and Counter(r['event_id'] for r in rest)==Counter({e:5 for e in eids}),len(rest))
result=(P/'RESULT.md').read_text();lines=result.splitlines()
heads=[l for l in lines if l.startswith('## ')]
check('required_four_tables_before_methods',[h.split(' · ')[0] for h in heads[:4]]==['## 표 1','## 표 2','## 표 3','## 표 4'],heads[:5])
first_after_title=next(l for l in lines[1:] if l.strip())
check('no_background_before_first_table',first_after_title.startswith('## 표 1'),first_after_title)
tail=[]
for line in reversed(lines):
 if line.startswith('|'):tail.append(line)
 elif tail:break
check('exactly_three_final_weakness_rows',len(tail)==5 and '중요한 불일치·약점' in tail[-1],len(tail)-2)
check('all_seven_question_sections',all(re.search(r'^## Q'+str(i)+r'\.',result,re.M) for i in range(1,8)),list(range(1,8)))
check('no_unexpanded_template_tokens','{{' not in result and '}}' not in result,'RESULT only')
missing=[]
for label,dest in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',result):
 if not dest.startswith(('https://','http://','#')) and not (P/dest.split('#')[0]).resolve().exists():missing.append(dest)
check('result_local_links_exist',not missing,missing)
paths=subprocess.check_output(['git','diff','--name-only','7f66165ad68610278df18855e1196a6cf52b035a','HEAD'],cwd=REPO,text=True).splitlines()
changed=subprocess.check_output(['git','ls-files','-m','-o','--exclude-standard'],cwd=REPO,text=True).splitlines()
prefix='docs/workstreams/research/AF-RES-023/'
check('all_changes_within_owned_path',all(f.startswith(prefix) for f in paths+changed),{'committed_paths':len(paths),'working_paths':len(changed)})
check('assigned_branch',subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()=='work/research-af-res-023','work/research-af-res-023')
if args.check_handoff:
 check('handoff_exists_after_self_check', (P/'HANDOFF.md').exists() and (P/'SELF_CHECK.md').exists() and (P/'evidence/acceptance-evidence.json').exists(),'final standalone handoff verified separately by commit history')
output={'at_utc':datetime.now(timezone.utc).isoformat(),'checks':checks,'passed':all(c['passed'] for c in checks),'check_count':len(checks),'failed':[c for c in checks if not c['passed']],'research_gaps_not_overridden_by_integrity_pass':True,'no_external_runtime_tests':True}
if not args.no_write:
 (P/'evidence/validation-results.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':output['passed'],'checks':len(checks),'failed':output['failed']},ensure_ascii=False))
raise SystemExit(0 if output['passed'] else 1)
