"""Normalize audited stream ledgers; no primary responses or new effect estimates.

Run at repository root. Inputs remain separately versioned under streams/ so the
normalization choices, including conservative exclusions, are inspectable.
"""
from collections import Counter
from pathlib import Path
import csv
import json
import re

BASE = Path(__file__).resolve().parent
UNKNOWN = '미확인'
NA = '해당 없음'


def jl(path):
    return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]


def csvrows(path):
    return list(csv.DictReader(path.open(newline='')))


def writecsv(path, rows):
    keys = list(dict.fromkeys(k for row in rows for k in row))
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)


def pick(r,*names,default=UNKNOWN):
    for n in names:
        if n in r and r[n] is not None and r[n] != '':return r[n]
    return default


def text(v):
    return '; '.join(map(str,v)) if isinstance(v,list) else str(v)


def normalize_sources():
    rows=[];seen={}
    for stream in ('a','b','supplement','root'):
        for index,r in enumerate(jl(BASE/'streams'/stream/'sources.jsonl'),1):
            sid=r['source_id'];kind=pick(r,'source_type')
            work=pick(r,'work_lineage_id','work_id');cohort=pick(r,'cohort_or_event_lineage_id','cohort_lineage_id','cohort_id')
            url=pick(r,'original_url');fixed=pick(r,'fixed_url')
            # Same published paper recovered in two independent search streams.
            if 's41586-023-06883-y' in url or 's41586-023-06883-y' in fixed:
                work='ASLETT2024-SOTEN'
            elif 's41598-022-09168-y' in url or 's41598-022-09168-y' in fixed:
                work='PANIZZA2022'
            counted=pick(r,'count_toward_minimum','count_minimum','counts_as_work','minimum_count',default=False)
            category=pick(r,'count_category','minimum_count_category',default='')
            if not category:
                if kind in ('original_study_report',):category='original_human_report'
                elif kind=='preregistration':category='stimulus_task_preregistration'
                elif kind=='author_data_code_stimuli_package':category='author_data_code_package'
                elif kind.startswith('truth_'):category='independent_truth_source'
                else:category='unassigned_or_not_counted'
            if category in ('author_data_codebook_analysis_package','author_data_package','author_data_codebook_package'):
                category='author_data_code_package'
            if category=='independent_truth_original':
                category='independent_truth_source'
            reason=pick(r,'count_reason',default='원 stream의 직접 독해·계보·최소량 판정을 유지')
            # Respect the instruction excluding the AF054 time/task research.
            if sid=='A-S19':
                counted=False;reason='AF054 시간/과제 연구 재모집 제외 경계로만 읽음; 엄격 최소량에서도 제외'
            if sid=='B-S10':
                counted=False;reason='도서관 안내서의 내용분석은 유용한 주변 원저이나 사람 자료접근 실험/반대결과가 아니므로 엄격 최소량에서 제외'
            duplicate=''
            if counted:
                if work in seen:
                    counted=False;duplicate=seen[work];reason=f'동일 저작 계보의 중복 독해; {duplicate}에서1회 산입'
                else:seen[work]=sid
            row=dict(source_id=sid,work_lineage_id=work,cohort_or_event_lineage_id=cohort,
                source_type=kind,author=text(pick(r,'author','creator')),title=pick(r,'title',default=work),
                original_url=url,fixed_url=fixed,version_or_sha_or_date=pick(r,'version_or_date','version'),
                read_utc=pick(r,'read_utc','accessed_utc'),read_time_precision=pick(r,'read_time_precision','read_utc_note','accessed_utc_semantics',default='원 stream 열람 시각'),
                direct_read_locations=text(pick(r,'direct_read_location','direct_locations','read_location','direct_read_locations')),
                confirmed=text(pick(r,'confirmed','findings','verified_content')),
                scope_and_limits=text(pick(r,'scope_limit','limits','limitations')),
                questions=pick(r,'questions',default=[]),case_ids=pick(r,'case_ids','cases',default=[]),
                minimum_count=bool(counted),minimum_count_category=category,count_reason=reason,
                duplicate_of=duplicate,reader=pick(r,'reader',default=stream+' AI'),
                stream_ledger=f'streams/{stream}/sources.jsonl',stream_record=index)
            rows.append(row)
    assert len({r['source_id'] for r in rows})==len(rows)
    (BASE/'sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    counted=[r for r in rows if r['minimum_count']]
    stats=dict(ledger_records=len(rows),minimum_distinct_primary_works=len(counted),
        categories=dict(Counter(r['minimum_count_category'] for r in counted)),
        counted_source_ids=[r['source_id'] for r in counted],
        information_retrieval_human_reports=[r['source_id'] for r in counted if r['source_id'].startswith('A-') and r['minimum_count_category']=='original_human_report'],
        factchecking_literacy_human_reports=[r['source_id'] for r in counted if r['source_id'].startswith('B-') and r['minimum_count_category']=='original_human_report'],
        accounting='저작 수. 참가자 수/독립 코호트 수/비교 셀 수가 아님. 중복·미러·한패키지 파일·접근실패는 추가 산입하지 않음.')
    (BASE/'evidence/source-counts.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n')
    return stats


def normalize_frames():
    rows=[]
    for r in csvrows(BASE/'streams/a/frame.csv'):
        rows.append(dict(frame='A',candidate_id=r['frame_id'],original_order=r['rank'],corrected_order=r['rank'],
            title=r['title'],doi=r['doi'],publication_sort_date=r['sort_date'],date_precision=r['date_precision'],
            in_first25=r['first25'],metadata_status=r['metadata_status'],method_status=r['method_read_scope'],
            eligibility=r['method_decision'],slot=r['slot'],source_ids=r['source_id'],
            method_or_discovery_url='streams/a/sources.jsonl; streams/a/search-log.jsonl',
            reason=r['method_reason'],prior_cohort_match='AF058선정6건 DOI와 새주선정중복 없음; A-F19는 AF054경계',
            original_stream='streams/a/frame.csv'))
    for r in csvrows(BASE/'streams/b/frame.csv'):
        rows.append(dict(frame='B',candidate_id=r['candidate_id'],original_order=r['original_rank'],corrected_order=r['corrected_rank'],
            title=r['title'],doi=r['doi'],publication_sort_date=r['effective_date'],date_precision=r['date_precision'],
            in_first25=r['in_corrected_first25'],metadata_status='duplicate:'+r['duplicate_of'] if r['duplicate_of'] else 'candidate',
            method_status=r['method_status'],eligibility=r['eligibility'],slot=r['selection_slot'] or NA,
            source_ids=r['source_ids'].replace('|',';') or UNKNOWN,method_or_discovery_url=r['method_urls'] or r['discovery_url'],
            reason=r['reason'],prior_cohort_match=r['existing_AF058_match'],original_stream='streams/b/frame.csv',
            next_minimum_input=r['next_input'] or NA))
    for r in csvrows(BASE/'streams/supplement/frame.csv'):
        rows.append(dict(frame='S',candidate_id=r['candidate_id'],original_order=r['chronological_order'],corrected_order=r['chronological_order'],
            title=NA+' — DOI/최초패키지 식별',doi=r['doi'],publication_sort_date=r['publication_date_final_rule'],date_precision='원메타데이터참조',
            in_first25=NA+' — 보강7후보별도',metadata_status='candidate',method_status=r['raw_access_status'],
            eligibility=r['decision'],slot=r['supplement_slot'],source_ids=r['source_ids'],
            method_or_discovery_url=r['methods_evidence_url'],reason=r['reason'],prior_cohort_match=r['overlap'],
            original_stream='streams/supplement/frame.csv',package_first_lead_url=r['package_first_lead_url']))
    def rank(r):
        v=r['corrected_order'];return (r['frame'],int(v) if v.isdigit() else 999,r['candidate_id'])
    rows.sort(key=rank);writecsv(BASE/'frame.csv',rows)


def normalize_outcomes():
    rows=[]
    for i,r in enumerate(json.loads((BASE/'streams/a/outcomes.json').read_text()),1):
        kim=r['case_id']=='A-F18';truth=r['advice_correctness']
        rows.append(dict(outcome_id=f'A-O{i:02d}',case_id='A02' if kim else 'A01',cohort=r['cohort'],
            sample_layer='main_provisional' if kim else 'main_confirmed_order',condition=r['condition'],
            truth_stratum=truth if kim else UNKNOWN,author_quality_label=NA if kim else truth,
            allocation_unit=r['allocation_unit'],assigned_people_N=UNKNOWN,assigned_trials_N=UNKNOWN,
            retained_people_N=r['retained_person_records'],observed_judgment_N=r['retained_trial_denominator'],
            acceptance_n=r['acceptance_n'],acceptance_N=r['acceptance_N'],final_correct_n=r['final_correct_n'],final_correct_N=r['final_correct_N'],
            CND_or_abstention_n=r['observed_abstention'],assigned_missing_m=UNKNOWN,
            acceptance_percent_author=r.get('acceptance_rate_author_percent',NA),final_accuracy_percent_author=r.get('final_accuracy_author_percent',NA),
            acceptance_difference_pp=r.get('source_minus_no_source_acceptance_pp',NA),final_accuracy_difference_pp=r.get('source_minus_no_source_final_accuracy_pp',NA),
            difference_basis=r.get('rate_delta_basis','수락종점해당없음'),assigned_acceptance_bounds=r['missingness_bounds'],
            evidence_grade=r['evidence_grade'],join_keys=r['join_keys'],source_url=r['source_url'],source_location=r['location'],
            initial_answer_agreement=UNKNOWN+' — 사전답 없음/미공개',limits=r['limits'],stream_record=f'streams/a/outcomes.json#{i}'))
    for i,r in enumerate(csvrows(BASE/'streams/b/outcomes.csv'),1):
        rows.append(dict(outcome_id=f'B-O{i:02d}',case_id=r['case_id'],cohort=r['cohort'],sample_layer=r['stratum'],condition=r['condition'],
            truth_stratum=r['truth_stratum'],author_quality_label=NA,allocation_unit=r['allocation_unit'],
            assigned_people_N=r['assigned_people_N'],assigned_trials_N=r['assigned_trials_N'],retained_people_N=UNKNOWN,
            observed_judgment_N=r['observed_trials_N'],acceptance_n=r['acceptance_n'],acceptance_N=r['acceptance_N'],
            final_correct_n=r['final_correct_n'],final_correct_N=r['final_correct_N'],CND_or_abstention_n=r['CND_n'],
            assigned_missing_m=r['assigned_missing_m'],acceptance_percent_author=NA,final_accuracy_percent_author=NA,
            acceptance_difference_pp=r['acceptance_diff_pp_search_minus_control'],final_accuracy_difference_pp=r['accuracy_diff_pp_search_minus_control'],
            difference_basis='정수 원행의 기술차; 반복/군집 유의성 검정 미실시',assigned_acceptance_bounds=r['assigned_acceptance_bounds'],
            evidence_grade=r['evidence_grade'],join_keys=r['join_keys'],source_url=r['original_url'],
            source_location='streams/supplement/aslett-aggregates.json groups/contrasts; '+r['analysis_sample'],
            initial_answer_agreement=UNKNOWN+' — Study1 사전답 없음',limits=r['limits'],stream_record=f'streams/b/outcomes.csv record{i}'))
    for truth,n0,n1,acc0,acc1 in [('correct',452,164,74.8,81.7),('incorrect',462,154,24.2,37.0)]:
        for condition,n,acc in [('not_clicked',n0,acc0),('clicked',n1,acc1)]:
            rows.append(dict(outcome_id=f'A-CLICK-{truth}-{condition}',case_id='A02',cohort='Kim2025Study2',
                sample_layer='voluntary_click_descriptive_only',condition=condition,truth_stratum=truth,author_quality_label=NA,
                allocation_unit='비무작위 자발클릭 person×question',assigned_people_N=NA,assigned_trials_N=NA,
                retained_people_N=UNKNOWN,observed_judgment_N=n,acceptance_n=UNKNOWN,acceptance_N=n,
                final_correct_n=UNKNOWN,final_correct_N=n,CND_or_abstention_n=UNKNOWN,assigned_missing_m=NA,
                acceptance_percent_author=UNKNOWN,final_accuracy_percent_author=acc,acceptance_difference_pp=UNKNOWN,
                final_accuracy_difference_pp=round(acc1-acc0,1) if condition=='clicked' else NA,
                difference_basis='저자 반올림평균 차이; 자발클릭이므로 인과효과 미식별',assigned_acceptance_bounds=UNKNOWN,
                evidence_grade='J3 means; J2 reported clicked denominators; complementary notclicked N derived from616',
                join_keys=UNKNOWN,source_url='https://arxiv.org/html/2502.08554v1',source_location='§4.3.2',
                initial_answer_agreement=UNKNOWN,limits='분모 정수와 최종정답/수락 분자 회수는 다름. 클릭은 독해/이해가 아님.',
                stream_record='streams/a/voluntary-clicks.json; root R-S16'))
    writecsv(BASE/'outcomes.csv',rows)


def normalize_stimuli():
    rows=[]
    for i,r in enumerate(csvrows(BASE/'streams/a/stimuli.csv'),1):
        rows.append(dict(stimulus_id=f'A01-S{i:02d}',case_id='A01',item_id=r['item_id'],item_id_basis=r['item_id_basis'],
            claim_or_question=r['question'],author_advice_or_key='perfect/imperfect≠binarytruth; source='+r['source_quality_author'],
            conditions=r['conditions'],same_item_advice_evidence=r['same_advice_scope'],source_url=r['source_url'],
            exact_source_section_or_snapshot=r['source_passage_version'],source_relation=r['entailment_scope'],
            independent_destination_read=r['independent_destination_read'],allocation_and_exposure=r['exposure'],
            cointerventions=r['cointervention'],version=r['source_passage_version'],
            stimulus_evidence_url=r['study_source_location'],source_ids=r['source_ids'].replace('|',';'),limits='조건 무작위화 미확인; 저자 보관발췌와 원문 직접열람 구분'))
    audit={
        'https://www.usgs.gov/special-topics/water-science-school/science/water-you-water-and-human-body':('반박:폐83%,피부64%','2024-08-01 보관판 Mitchell1945 인용단락','R-S02;R-S13'),
        'https://medlineplus.gov/genetics/understanding/traits/fingerprints/':('반박:지문없는 adermatoglyphia 예외','2024-06-13 보관판 absentdermatoglyphs단락','R-S03;R-S14'),
        'https://science.nasa.gov/moon/moon-walkers/':('일부지지:달보행12명;해구와비교전체미확인','2024-08-01보관판 WhoHasWalkedontheMoon','R-S04;R-S17'),
        'https://www.sciencedaily.com/releases/2022/08/220807102043.htm':('반론경로:감소미검출은증가증명이아님','FullStory→2022원비판;2023저자응답함께보존','R-S06;R-S07;R-S09'),
        'https://humanorigins.si.edu/human-characteristics/brains':('무관시간창:10만년비교직접검증불가','현재6–2M,2M–800k,800k–200k단락','R-S10'),
        'https://louisvillezoo.org/gorilla-forest/gorilla-facts/':('불충분:사람과털밀도두배비교없음','현재GorillaFacts본문','R-S11'),
        'https://www.rmg.co.uk/stories/topics/what-was-first-animal-space':('불충분:바퀴벌레수태와첫발사구분','현재도착본문Animals/firstfacts','R-S12'),
    }
    for i,r in enumerate(csvrows(BASE/'streams/a/fostering-source-links.csv'),1):
        url=r['source_url'];relation=UNKNOWN;section=UNKNOWN;ids=r['source_id'];read=UNKNOWN
        if url in audit:relation,section,extra=audit[url];ids+=';'+extra;read='직접확인 — 한정범위 streams/root/source-audit.md'
        elif '10.3389/fevo.2021.742639' in url:
            relation='원저의감소주장지지;2022비판/2023응답과논쟁';section='2021Methods,Tables1–2,Fig1B';ids+=';R-S05;R-S06;R-S09';read='직접확인 — contestedauthortruth'
        elif any(x in url for x in ['aao.org/eye-health','PMC6850423','NBK572136','worldheritagesite.org/tentative/id/5430']):
            read='접근불가/확인화면;직접독해미산입';relation='접근불가';section='streams/root/search-log.jsonl'
        rows.append(dict(stimulus_id=f'A02-S{i:02d}',case_id='A02',item_id=r['derived_item_id'],item_id_basis=r['item_id_basis'],
            claim_or_question=r['question'],author_advice_or_key=r['author_truth_label']+':'+r['advice_direction']+';key='+r['author_correct_answer'],
            conditions='sourcepresent vsabsent within sameexplanation/correctness',same_item_advice_evidence=r['same_advice_evidence'],
            source_url=url,exact_source_section_or_snapshot=section,source_relation=relation,independent_destination_read=read,
            allocation_and_exposure=r['exposure'],cointerventions=r['cointervention'],version=r['paper_version'],
            stimulus_evidence_url=r['paper_source_location'],source_ids=ids,limits='72linkslots inventory is not72directreadworks; externalcurrent/historicalfindingslimited toverifiedsubset'))
    for i,r in enumerate(csvrows(BASE/'streams/b/stimuli.csv'),1):
        rows.append(dict(stimulus_id=f'B-S{i:02d}',case_id=r['case_id'],item_id=r['item_ids_or_pool'],item_id_basis='원저 pool/key 설명',
            claim_or_question=r['item_ids_or_pool'],author_advice_or_key=r['cohort'],conditions=r['conditions'],
            same_item_advice_evidence=r['same_item_evidence'],source_url=r['truth_or_target_url_and_passage'],
            exact_source_section_or_snapshot=r['truth_or_target_url_and_passage'],source_relation=r['support_refutation'],
            independent_destination_read=r['version_scope_limits'],allocation_and_exposure=r['allocation_and_flow']+';'+r['actual_open_event_definition'],
            cointerventions=r['cointerventions'],version=r['version_scope_limits'],stimulus_evidence_url=r['stimulus_or_method_url'],
            source_ids=r['source_ids'].replace('|',';'),limits=r['original_source_provision']))
    for i,r in enumerate(csvrows(BASE/'streams/supplement/stimuli.csv'),1):
        rows.append(dict(stimulus_id=f'S-DIAG-S{i:02d}',case_id=r['case_id'],item_id=r['same_item_key'],
            item_id_basis='보강/진단층; '+r['stratum'],claim_or_question=r['recommendation_or_claim'],
            author_advice_or_key=r['truth_reference'],conditions=r['conditions'],same_item_advice_evidence=r['same_item_key'],
            source_url=r['evidence_urls'],exact_source_section_or_snapshot=r['source_passage'],
            source_relation=r['truth_assessment'],independent_destination_read=r['actual_exposure'],
            allocation_and_exposure=r['assignment']+'; '+r['event_definition'],cointerventions=r['cointerventions'],
            version=r['versions'],stimulus_evidence_url=r['evidence_urls'],source_ids=r['source_ids'],
            limits=r['source_access']+'; 독립신규S슬롯배정으로세지않음'))
    writecsv(BASE/'stimuli.csv',rows)


if __name__=='__main__':
    stats=normalize_sources();normalize_frames();normalize_outcomes();normalize_stimuli()
    print(json.dumps(stats,ensure_ascii=False,indent=2))
