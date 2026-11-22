"""Write explicit coverage decisions; workflow receipts follow the fixed result commit."""
import json
import hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def jl(p):return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
def main():
    validation=json.loads((ROOT/'evidence/validation.json').read_text())
    summary=json.loads((ROOT/'evidence/analysis-summary.json').read_text())
    src=jl(ROOT/'sources.jsonl');sl={s['source_id']:i for i,s in enumerate(src,1)}
    def evidence(file,lines,unit):return {'file':file,'lines':lines,'unit':unit}
    def source(sid):return evidence('sources.jsonl',[sl[sid]],sid)
    conditions=[]
    def add(cid,met,unit,n,d,ev,reason='',resume='해당 없음',required=True):
        conditions.append({'condition_id':cid,'met':bool(met),'required_for_full_acceptance':required,'verification_unit':unit,'numerator':n,'denominator':d,'evidence':ev,'unmet_reason':reason if not met else '해당 없음','minimum_resume_material':resume if not met else '해당 없음'})
    add('initial_repo_and_dependencies_read',True,'필수 운영입력과 고정 의존 HANDOFF',[5,2],[5,2],[evidence('evidence/input-receipt.json','전체','GitHub 읽은 blob 및 고정SHA'),evidence('manifest.json','전체','session start --fetch 실제 성공')])
    add('preregistered_scope_before_fresh_discovery',True,'범위 원격커밋이 최초 새조회 전에 존재',1,1,[evidence('SCOPE.md','전체','v1 고정'),evidence('PROGRESS.md','묶음①','remote a6cc61d4c2b6baf7cae47569c1454b371986ce47;2026-11-22T20:09:19Z')])
    add('four_first25_frames_preserved',True,'두 자연원장·통계·학술 최초25 목록',4,4,[evidence('frame.csv','전체106record','50natural+25statistics+31journalraw; journalfirst25unique endsraw26')])
    add('strict_sampling_order_and_consumer_query_trace',False,'원장/검색의 엄격 순서·노출 재구성 가능',2,4,[evidence('collection/statistics/search-metadata.json','전체','initial merged10 query rank unknown'),evidence('collection/journals/consumer-search.csv','J02 행','failed query/detail omission/retry')], '자연2프레임은목차순서가있지만 통계초기query별순위와J02소비검색일부상세목록은미확인. 새검색으로소급수정하지않음.','당시 tool call별전체결과 로그. 없으면 기존표본을보존하고 새프레임별도사전등록.')
    add('direct_primary_unique_total_at_least24',True,'중복·실패·미러를 뺀 고유 발행자 원문 하한',28,24,[evidence('evidence/source-count-audit.json','counted_primary_unique_lower_bound.works','대표28source_id/URL/locator')])
    add('required_composition_8_8_4_4',False,'소비/대상/별도공지/공식규칙',23,24,[evidence('evidence/source-count-audit.json','strict_allocation','7+8+4+4'),source('S-JOUR-J01-CONSUMER-PUBLISHER-HTML')], 'J01소비자는PMC전문으로목적을확인했으나BMJ발행자본문열람실패. 미러제외규칙상소비자7/8. 다른보조문서로대체하지않음.','https://bmjopen.bmj.com/content/11/2/e041022 Methods/Results 및 reference16')
    add('consumer_purpose_observed_in_published_text',True,'소비자별 실제 인용목적; J01은PMC보관전문임을명시',8,8,[evidence('versions.csv','2–9','consumer source/locator/purpose'),source('S-JOUR-J01-CONSUMER-PMC')])
    add('old_and_current_editions_attempted',True,'모든슬롯의옛판/현재판 시도; 성공과분리',8,8,[evidence('sources.jsonl','전체119행','access failures retained'),evidence('versions.csv','2–9','old/current pointers')])
    add('separate_dated_correction_revision_notices',True,'대상과별개산입되는발행공지',4,4,[source('S-STAT-T01-N-DATED'),source('S-STAT-T02-N'),source('S-JOUR-J01-CORRECTION'),source('S-JOUR-J02-CORRECTION')])
    add('official_citation_revision_rules',True,'별도공식규칙',4,4,[source('POL01'),source('POL02'),source('POL03'),source('POL04')])
    add('B_L_X_source_and_locator_separation',True,'B원href/목적, L종류/존재근거, X출처/절의분리기록',8,8,[evidence('key.jsonl','1–8','L_kind/L_existed_at_consumption/X_source_id/X_locator'),evidence('components.jsonl','1–8','실제요소')])
    add('complete_X_from_old_section',False,'실제옛절에서뽑은X가있는사례',7,8,[evidence('key.jsonl',[4],'N-S-02 X_available=false'),evidence('collection/natural/evidence-notes.md','UCLA 항목','옛판실패')], 'UCLA당대본문이없어X를만들지않았다. 미확인표시는발췌가아님.','http://www.ats.ucla.edu/stat/stata/webbooks/reg/chapter4/statareg_self_assessment_answers4.htm 의 날짜 있는 발행자 보관본; GitHub issue808의당대인용기록부터추적.')
    add('L_is_edition_specific_for_all_cases',False,'판/발표전용L; 단순저작·이관locator와구별',5,8,[evidence('key.jsonl','1–8','L_version_pinned/L_kind'),evidence('evidence/acceptance-audit-notes.md','판 식별 항목','DOI work identity != immutable version')], 'J01/J02는직접저작HTML+절이며불변판주소미확인. UCLA는이관위치. 5개도당시URL존재와바이트불변성을일괄입증한것은아님.','J01/J02 발행자의날짜있는원판보관본; UCLA당대판. 기존L을교체하지말고후속자극별도등록.')
    add('current_criterion_coverage',False,'현재목적기준을직접문서로정할수있는사례',7,8,[evidence('key.jsonl','1–8','C_criterion_confirmed')], 'UCLA의옛소비자료와현행관련자료의외부동등기준미확인. 관측유지/보류를정오로승격하지않음.','UCLA당대Stata Answer1 발행판과현재보관페이지의명시적판관계')
    add('main_historical_criterion_coverage',False,'실제소비자가명시한저작/판의H본기준',4,8,[evidence('key.jsonl','1–8','H_criterion_confirmed; J02한계포함')], '자연4건은외부대상판을명시하지않아실제소비판기준미확인. 추가판검증을대체분모로쓰지않음.','소비자의대상버전/다운로드시점/원파일기록. 첫자료: statsmodels0.14.0 Rolling Regression 원출력·실행자료')
    add('32_cards_identical_elements_and_hashes',True,'8사례×4구성',32,32,[evidence('cards.jsonl','1–32','본문·hash·order'),evidence('evidence/validation.json','identical_elements/body_hashes/sealed_key_cards_components','전부일치')])
    add('q3_neutrality',False,'연구자정답단서가없는자극이라는주장',0,1,[evidence('components.jsonl',[3],'N-S-01 B 마지막문장'),evidence('evidence/acceptance-audit-notes.md','후속 감사','직접식별영향1/8사례·4/32C')], '시간의도부재는소비문장이아닌연구자해석으로C보류를암시할수있다. key비노출과별개. 다른7사례의완전중립보증도아님.','N-S-01의부재해석문장과추가시간구분지시를제거한새사전등록4C자극; 기존판독에노출안된독자')
    add('64_raw_card_task_observations',True,'32카드×2과업',64,64,[evidence('judgments.csv','2–65','원판정+별도채점'),evidence('evidence/read-seal.json','file_sha256','③봉인')])
    add('two_open_budget_and_failed_attempt_accounting',True,'과업별최대2;실패도1',64,64,[evidence('reads.csv','2–110','73publisher/32local/4same-document'),evidence('evidence/validation.json','publisher_budget','55과업1회+9과업2회')])
    add('first_url_visible_in_card',True,'첫요청의카드URL',64,64,[evidence('evidence/validation.json','first_url_card_visible','위반0')])
    add('second_move_actual_parent_link',True,'둘째요청의실제부모링크ID/anchor근거',9,9,[evidence('evidence/analysis-audit.md','second-link audit','actualparent+linkID'),evidence('reads.csv','parent_read_id/href_evidence','추측주소없음')])
    add('literal_href_preservation',False,'둘째요청의원HTML href철자',2,9,[evidence('evidence/amendments.md','§1','③1개검사→④7개결측정정'),evidence('evidence/analysis-audit.md','미확인7행','각read_id')], '도구의clickUI가rawhref를드러내지않은7건. 이중rc-038은requested_url도미확인. 도착주소·실제링크ID는있다.','부모응답의literal href를노출/보존하는수집기. 사후찾은주소를원관측에소급기입하지않음.')
    add('key_masking_and_prior_exposure_recorded',True,'키비노출·앞카드노출기록',64,64,[evidence('judgments.csv','2–65','key_exposure=none;prior_card_exposure'),evidence('readers/reader_b/reader-notes.md','전체','방법선택과순서')])
    add('raw_observation_fields_unchanged_by_grading',True,'원64판정기존필드',64,64,[evidence('evidence/validation.json','raw_judgment_fields_unchanged','불일치0'),evidence('evidence/adjudication.jsonl','1–64','별도채점')])
    add('64_one_element_pairs_and_partition',True,'8×2×4짝과배타분할',64,64,[evidence('pairs.csv','2–65','원64짝'),evidence('evidence/analysis-audit.md','재계산','32both+12hold+20unknown')])
    add('two_separate_sensitivities',True,'S-X 및S-I를따로원규칙과비교',2,2,[evidence('evidence/analysis-summary.json','pair_summary48행','16original+16SX+16SI'),evidence('RESULT.md',[163,176],'층·과업·구성별감도')])
    add('local_quote_and_publisher_evidence_separated',True,'H판독의증거수준',32,32,[evidence('judgments.csv','H 행','16publisher/6local-only/10unverified;natural4reconstructedseparate')])
    add('L_helpful_and_L_redundant_cases_observed',True,'반대방향의문서/판독사례',2,2,[source('FINAL-T01-O'),source('FINAL-T02-O'),evidence('pairs.csv','T01-H/T02-H','날짜판이득과원B충분')])
    add('old_quote_correct_but_current_reuse_wrong',True,'실제정정전후주장관계;판독인과오도와구별',1,1,[source('S-JOUR-J01-TARGET'),source('FINAL-PLOS-RAW-J01'),evidence('pairs.csv','J01-C X비교','실제단정오류0')])
    add('same_url_200_semantic_change_strong_form',False,'같은URL의과거/현재200본문을직접관측',0,1,[source('FINAL-T02-V1'),source('FINAL-T02-V2')], '발행자superseded/current의Quarter1→Quarter2의미변화는확인했지만2024년같은URL200을직접측정한기록은없다. 현재두판열람을그대신으로부르지않음.','ONS의2024-09-30수정전후동일주소응답보관기록. 첫자료: https://www.ons.gov.uk/economy/grossdomesticproductgdp/bulletins/quarterlynationalaccounts/apriltojune2024/previous/v1')
    add('correction_not_affecting_selected_claim',True,'좁은인용주장과정정범위의대조',1,1,[source('S-JOUR-J02-CONSUMER'),source('FINAL-PLOS-RAW-J02'),evidence('judgments.csv','rc-j024','현재유지근거')])
    add('cross_field_initial_and_revised_value_reports',True,'같은계열최초값보고서와수정값보고서',2,2,[source('FINAL-T01-C'),source('FINAL-T01-2026')])
    add('table1_32_rows_immediately_after_title',True,'RESULT첫표',32,32,[evidence('RESULT.md',[3,36],'header+32rows'),evidence('evidence/validation.json','required_tables_first','검사통과')])
    add('table2_16_stratum_task_comparisons',True,'RESULT둘째필수표',16,16,[evidence('RESULT.md',[40,57],'header+16rows')])
    add('Q1_Q7_primary_locator_recheck',True,'질문별핵심URL/절재점검',7,7,[evidence('SELF_CHECK.md','Q1–Q7','claim/support/refutation/unknown/flip'),evidence('evidence/final-source-checks.jsonl','1–17','최종원문재열람'),evidence('evidence/publisher-body-verification.jsonl','1–3','PLOS현재발행자본문직접확인;시행에비합산')])
    add('source_schema_and_unique_ids',True,'필수필드및고유source_id',len(src),len(src),[evidence('sources.jsonl','1–119','산입·중복·실패·해석구분')])
    add('unknowns_explicit_in_canonical_ledgers',True,'frame/versions/reads/judgments/pairs의공란',5,5,[evidence('evidence/normalization-log.json','전체','원관측/분모변경없음'),evidence('evidence/validation.json','no_implicit_missing_*','공란0')])
    add('three_final_weaknesses_with_next_actions',True,'RESULT마지막표의정확히세행',3,3,[evidence('RESULT.md',[200,204],'3행'),evidence('evidence/weaknesses.json','1–3objects','HANDOFF동일표의원본')])
    add('owned_path_only_and_dot_control_untouched',True,'쓰기범위와운영제어파일',1,1,[evidence('evidence/validation.json','owned_path_only/dot_control_unchanged','검사통과')])
    add('same_model_limitations_and_no_cost_claims',True,'측정범위공개',1,1,[evidence('RESULT.md','Q3–Q7/검증범위','인간행동·시간·비용·인과확정주장없음'),evidence('evidence/analysis-audit.md','scope','same-family self-audit')])
    record={
      'task_id':'AF-RES-043','attempt':1,'phase':'④ fixed research result; postcommit workflow receipts are finalized in HANDOFF commit',
      'full_research_acceptance':all(c['met'] for c in conditions if c['required_for_full_acceptance']),
      'reporting_integrity_pass':validation['integrity_pass'],
      'case_slots':8,'cards':32,'judgments':64,'pairs':64,'source_rows':len(src),
      'strict_source_composition':{'consumer':7,'target':8,'separate_notice':4,'official_rule':4},
      'distinct_direct_primary_lower_bound':28,
      'observed_outcomes_not_acceptance_thresholds':{k:summary[k] for k in ['C_supported_n','C_criterion_n','strict_H_supported_n','strict_H_criterion_n','valid_X_displays_H','publisher_opens','publisher_failures']},
      'conditions':conditions,
      'unmet_condition_ids':[c['condition_id'] for c in conditions if not c['met']],
      'fixed_prior_commits':{'scope':'a6cc61d4c2b6baf7cae47569c1454b371986ce47','key':'b3aa200fce66f0635e74aa39c4cb008cafd86eff','reads':'6c58c98d60351b9b125a8611887fec0972aeae1f'},
      'result_sha_and_postcommit_checks':'HANDOFF.md and evidence/postcommit-verification.json: created only after this result/acceptance commit is reopened from GitHub and session check --fetch executes.',
      'result_sha256':hashlib.sha256((ROOT/'RESULT.md').read_bytes()).hexdigest(),
      'key_sha256':hashlib.sha256((ROOT/'key.jsonl').read_bytes()).hexdigest(),
      'raw_reads_sha256':hashlib.sha256((ROOT/'reads.csv').read_bytes()).hexdigest(),
    }
    (ROOT/'evidence/acceptance-evidence.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'conditions':len(conditions),'met':sum(c['met'] for c in conditions),'unmet':record['unmet_condition_ids'],'full_research_acceptance':record['full_research_acceptance']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
