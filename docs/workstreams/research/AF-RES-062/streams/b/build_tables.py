"""Assemble reviewed frame-B audit tables; no participant-row analysis in this script."""
from pathlib import Path
import json,csv,datetime,collections,urllib.parse
p=Path(__file__).parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
freeze=json.loads((p/'candidate-freeze.json').read_text())
sources={r['source_id']:r for r in map(json.loads,(p/'sources.jsonl').read_text().splitlines())}
review={
'DIG42':('full_primary_methods','excluded','B-S18','Task and age differ with paper/live-web availability; not same-claim access comparison.'),
'SEARCH12':('full_primary_methods','pending_affordance','B-S01|B-S02','Companion papers share recruitment and complementary excluded conditions. Same rebuttal plus source previews is promising, but live-click affordance and delivered screen set are 미확인; retain source-badge diagnostic, not confirmed access trial.'),
'DIG23':('full_primary_methods','excluded','B-S12','Training differs; both arms already have live web access.'),
'DIG40':('full_primary_methods','excluded','B-S15','Expertise groups observational; all can browse.'),
'DIG36':('fulltext_access_failed','pending_methods','','Publisher403; OpenAlex closed; author-list links recovered but no full method. Abstract training design is not a substitute for exact method.'),
'DIG24':('full_primary_methods','excluded','B-S04','Single-arm educational pre/post; alternate source tasks; no original-access difference.'),
'DIG35':('fulltext_access_failed','pending_methods','','Publisher403 and author directory DOI-only; OpenAlex no OA. Possible earlier curriculum pilot overlap unconfirmed.'),
'DIG26':('full_primary_methods','excluded','B-S16','Observational assessment; same live web availability.'),
'DIG32':('fulltext_access_failed','pending_methods','','Publisher403; institutional/author abstract and OpenAlex checked. Classroom dialogue analysis likely adjacent, full method unresolved.'),
'SEARCH4':('full_primary_methods','excluded','B-S03','Education intervention, same source access for every arm.'),
'SEARCH5':('full_primary_methods','excluded','B-S05','Both groups explicitly can browse; pop-up/incentive changes, not independent source access.'),
'SEARCH11':('fulltext_access_failed','pending_methods','','Wiley full route redirects to abstract/sign-in; author/institutional/DOI and OpenAlex checked; formative-study details insufficient.'),
'DIG22':('precursor_and_author_tasks_partial','pending_final_methods','B-S13|B-S17','Precursor and publisher task appendix show training with same access. Main VoR blocked; 464 precursor versus499 published abstract not reconciled; do not treat full method as read.'),
'DIG31':('fulltext_access_failed','pending_methods','','Publisher403; author directory and OpenAlex checked; full classroom-method report not retrieved.'),
'DIG30':('full_primary_methods','excluded','B-S10','50 institutional guides are not human final judgments; November2022 issue date refines year-only placeholder.'),
'DIG29':('precursor_methods_partial','excluded_precursor_scope','B-S14','Author explicitly identifies preprint lineage; all access live web and different sources assigned. Published version slightly differs, exact VoR method not directly read.'),
'DIG27':('full_primary_methods','excluded','B-S06','All students have source access; curricular lessons and pre/post content differ.'),
'DIG28':('full_review_no_new_methods','excluded','B-S20','Conceptual synthesis, no new human allocation.'),
'SEARCH6':('author_questionnaire_methods_only','excluded_author_task_scope','B-S22','Original author questionnaire pp3,5 explicitly gives every arm original-source links. Training changes; main report inaccessible.'),
'SEARCH7':('fulltext_access_failed','pending_methods','','Publisher403; Technion author/institutional abstract and OpenAlex checked. Game intervention details not enough to confirm same-item independent access.'),
'SEARCH1':('full_primary_methods','eligible_I2_provisional_order','B-S08','Same news claims, person-level assigned external search encouragement; extra instructions and effort cochange. Earlier pending methods mean earliest eligible rank not secured.'),
'DIG21':('publisher_metadata_review_only','excluded_review_metadata','','Publisher/PubMed designate review, no new experiment in accessible metadata; full review blocked and not counted as read.'),
'DIG25':('full_primary_methods','excluded','B-S07','Same Internet access, alternate pre/post sources; possible subset of2023 cross-curriculum cohort retained pending explicit participant crosswalk.'),
'SEARCH8':('full_primary_methods','excluded','B-S09','Source-name correction only; author Discussion p15 says actual fact-check links not supplied.'),
'SEARCH10':('full_primary_methods','excluded','B-S19','Same accessible paired fabricated webpages; prime/errors varied, not independent original access.')
}
merged={'SEARCH2':'SEARCH12','DIG33':'DIG40','DIG34':'DIG29','DIG37':'DIG22'}
corrections=[
 dict(correction_id='B-C01',kind='date_precision',key='DIG30',before='2022-01-01 (year-only placeholder)',after='2022-11-01 (month)',evidence_url=sources['B-S10']['fixed_url'],location='83(6) issue header November2022',impact='Within-window order refined, no eligibility change'),
 dict(correction_id='B-C02',kind='cohort_dedup_confirmed',key='DIG33',before='separate rank17',after='merged into DIG40 rank5 original',evidence_url='https://www.tandfonline.com/doi/full/10.1080/07370008.2021.1908288',location='publisher Notes1:participants same as2019;Notes2:4 declined historical task',impact='SEARCH8 moves into first25. Full2022body blocked; direct publisher notes were visible in indexed source.'),
 dict(correction_id='B-C03',kind='cohort_dedup_conservative',key='SEARCH2',before='separate rank3',after='merged into SEARCH12 originalrank2; both papers retained',evidence_url=sources['B-S01']['fixed_url']+' | '+sources['B-S02']['fixed_url'],location='Methods same613 MidAtlantic spring2016 recruits;both Notes1 exclude43 repeat participations and complementary platform/source/algorithmic conditions; exact matching per-cell integers not published in both reports',impact='SEARCH10 also moves into first25. Identical-person crosswalk absent; sensitivity without merge keepsSEARCH10 outside first25. Both papers excluded from separate cohort/work counts.'),
 dict(correction_id='B-C04',kind='precursor_identity_confirmed',key='DIG34',before='tentative precursor',after='author explicitly identifies preprint ofDIG29',evidence_url='https://www.samwineburg.com/writing/paged-4/2/',location='Educating for Misunderstanding entry; report p1/Methods',impact='No additional cohort or date slot'),
 dict(correction_id='B-C05',kind='precursor_identity_pending',key='DIG37',before='tentative report linkedtoDIG22',after='retain one conservative lineage; exact counts differ464vs499',evidence_url=sources['B-S17']['fixed_url']+' | '+sources['B-S13']['fixed_url'],location='ReportFieldtest methods;journal abstract',impact='No new slot granted. If cohorts distinct, reinsert report by2019-12-04 and re-run first25. This is residual chronology uncertainty.'),
 dict(correction_id='B-C06',kind='possible_cohort_overlap_pending',key='DIG25',before='separate rank25',after='retain screen row; countminimum merged withDIG27',evidence_url=sources['B-S07']['fixed_url']+' | '+sources['B-S06']['fixed_url'],location='2021–22 grade9 biology/fivehour lessons and one-teacher subset',impact='If explicit crosswalk confirms overlap, corrected unique candidate count becomes24; do not silently drop before confirmation.')
]
active=[]
for old in freeze['all_candidates']:
 if old['status']=='in_window_metadata' and old['discovery_key'] not in merged:
  x=dict(old);x['original_rank']=old.get('rank','미확인');x['original_date']=old['date']
  if x['discovery_key']=='DIG30':x.update(date='2022-11-01',date_precision='month')
  active.append(x)
active.sort(key=lambda x:(x['date'],x['doi'].lower() or x['discovery_key']))
rank={x['discovery_key']:i+1 for i,x in enumerate(active)}
rows=[]
for old in freeze['all_candidates']:
 k=old['discovery_key'];r=dict(frame='B',candidate_id=k,original_rank=old.get('rank','해당 없음'),corrected_rank=rank.get(k,'해당 없음'),title=old['title'],doi=old['doi'],original_date=old['date'],effective_date='2022-11-01' if k=='DIG30' else old['date'],date_precision='month' if k=='DIG30' else old['date_precision'],first_online_date='-'.join(map(str,old.get('online_date',[]))) or '미확인',discovery_url=old['discovery_url'],metadata_url=old['metadata_url'],in_original_first25=old.get('methods_window',False),in_corrected_first25=k in rank and rank[k]<=25,duplicate_of=merged.get(k,''),existing_AF058_match='No DOI match in fixed AF058 full60-row A/B frame (prior-cohort-match.json); no prior participant rows read',selection_slot='B01 provisional' if k=='SEARCH1' else '',strict_primary_original_access='미확인',method_status='',eligibility='',source_ids='',method_urls='',reason='',next_input='')
 if k in review:
  r['method_status'],r['eligibility'],r['source_ids'],r['reason']=review[k]
  ids=r['source_ids'].split('|') if r['source_ids'] else []
  r['method_urls']=' | '.join(sources[i]['fixed_url'] for i in ids)
  r['strict_primary_original_access']='I2 search encouragement; I1 미확인' if k=='SEARCH1' else ('미확인' if r['eligibility'].startswith('pending') else '해당 없음')
  if r['eligibility'].startswith('pending'):r['next_input']='Author accepted manuscript/full Methods plus condition screen-flow, source clickability and allocation details; linked package if available.'
 elif k in merged:
  r.update(method_status='cohort_or_work_companion',eligibility='merged_not_new_slot',source_ids='B-S01' if k=='SEARCH2' else ('B-S15' if k=='DIG33' else ('B-S14' if k=='DIG34' else 'B-S17')),reason='Preserve original entry; see corrected-order.json for evidence and certainty.',next_input='Participant crosswalk for tentative merges; no further participant reanalysis required to establish identity.')
 else:r.update(method_status='not_screened_outside_year',eligibility='excluded_date',reason='Final issue/publication year outside2018–2025; online date sensitivity preserved.')
 rows.append(r)
fields=list(rows[0]);
with (p/'frame.csv').open('w',newline='') as f:w=csv.DictWriter(f,fields);w.writeheader();w.writerows(rows)
active_rows=[r for r in rows if r['in_corrected_first25']]
summary=dict(created_utc=now,prior_freeze_commit='10de6313282ba8cfeeec75057050056ef8b74bad',metadata_candidates=33,initial_window_publications=27,initial_first25=25,corrected_unique_screen_units=len(active),corrected_first25=len(active_rows),full_primary_methods=sum(r['method_status']=='full_primary_methods' for r in active_rows),method_status_counts=dict(collections.Counter(r['method_status'] for r in active_rows)),eligibility_counts=dict(collections.Counter(r['eligibility'] for r in active_rows)),strict_confirmed_I1=0,provisional_I2_slots=1,empty_slots=['B02','B03'],earliest_slot_certainty='미확인: earlier pending methods/affordance and cohort/date sensitivity',dedup_certainty='confirmed one later companion; conservative same613 merge; precursor and subset merges partially unresolved',corrections=corrections,corrected_order=[dict(rank=i+1,key=x['discovery_key'],date=x['date'],doi=x['doi']) for i,x in enumerate(active)],method_fulltext_failures=[r['candidate_id'] for r in active_rows if r['method_status']=='fulltext_access_failed'],limitations=['Native author lists are explicit bounded coverage, supplemental publisher search was relevance-ranked; no exhaustive field census.','Search-tool merged batches did not expose accurate perquery result counts or native query URLs.','Six full-method retrievals remained blocked despite publisher/author/institutional/OpenAlex attempts; no result-direction replacement.','Dates/merges were revised after outcomes became available; original frozen records and correction reasons retained.','Same source access with education differences is excluded from access effect even if accuracy improves.'])
(p/'corrected-order.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k in ['corrected_unique_screen_units','method_status_counts','eligibility_counts']},ensure_ascii=False))
