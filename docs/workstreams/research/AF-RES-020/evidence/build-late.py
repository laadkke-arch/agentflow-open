"""AF-RES-020 internal audit B: deterministic serialization of reviewed notes.

Run from repository root. Only writes this workstream's owned path.
Claims are manually selected; this script does not infer truth from keyword matches.
"""
from pathlib import Path
import json
import subprocess
from datetime import datetime, timezone

OUT = Path('docs/workstreams/research/AF-RES-020')
FIX = json.loads((OUT/'evidence/fixed-inputs.json').read_text())['fixed']
NOW = datetime.now(timezone.utc).isoformat()

def full(t, p):
    return f'docs/workstreams/research/AF-RES-{t}/{p}'

def url(t, p, lines=''):
    return f'https://github.com/laadkke-arch/agentflow-open/blob/{FIX["AF-RES-"+t]}/{full(t,p)}' + ('#'+lines if lines else '')

def ref(t, p, loc, lines=''):
    return dict(task='AF-RES-'+t, sha=FIX['AF-RES-'+t], path=full(t,p), locator=loc, url=url(t,p,lines))

def dump(p, obj):
    (OUT/p).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')

CLAIMS=[]
def claim(b,t,p,loc,text,hop=None,hoploc=None,calculation=None,note='', lines=''):
    seq=1+sum(c['bundle_id']==b for c in CLAIMS)
    c=dict(claim_id=f'C-{b}-{seq:02}', bundle_id=b, claim=text, source_task='AF-RES-'+t,
           sha=FIX['AF-RES-'+t], path=full(t,p), locator=loc,
           second_hop_path=full(t,hop) if hop else None, verdict='일치',
           mismatch_type=None, note=note or '고정 원 결과의 범위·분모·판정 주체를 유지해 대조했다.',
           source_url=url(t,p,lines), checked_by='GPT-6 Astra Pro 내부 별도 검토', checked_at_utc=NOW)
    if hop:
        c['second_hop_locator']=hoploc
        c['calculation']=calculation
        c['second_hop_sha']=FIX['AF-RES-'+t]
        c['second_hop_url']=url(t,hop)
    CLAIMS.append(c)

claim('B11','011','HANDOFF.md','표본·단위 L34–39','61개 공개 질문에서 whole 28개, part 33개, 답·후속 단위 635개다(2014–2026년 편의 표본; 2026-11-20 동결).','CASES.json','$.cases[*].whole_or_part; $.cases[*].answers','len(cases)=61; Counter(whole_or_part)={whole:28,part:33}; sum(len(answers))=635',lines='L34-L39')
claim('B11','011','HANDOFF.md','Q7 L116–128','부분 질문 33개 중 명시 선택·사용 신호 6개와 현재 accepted 답이 있는 질문 5개의 합집합은 10개다(중복 1개). 통합 성공률이 아니다.','CASES.json','$.cases[whole_or_part=part].answers[*].outcome','|adopt_cases|=6; |accepted_cases|=5; intersection=1; union=10',lines='L116-L128')
claim('B11','011','CODEBOOK.md','입력·반응 L24–44','I1은 수집자가 남긴 URL이며 I8은 단독 질문에서 해당 없음일 수 있다. accepted·top_voted·asker_response는 분리하고 thanks를 채택이나 통합 성공으로 바꾸지 않는다.',lines='L24-L44')

claim('B12','016','RESULT.md','표1 L9–17, Q5 L162–166','011의 동일 120개 표본에서 S1 일치 94/120, S2 85/120, S3 결합 75/120이다. S2 comparison은 코더 A 0/120, B 14/120이다.','coding/coder-a.json','$.rows[unit_id startswith 011 or T].S1/S2/S3; coder-b.json 같은 unit_id 조인','원 두 코더 JSON을 unit_id로 조인; 011 표본 ID는 sample/units.json으로 식별; agreement.json main과 재대조',note='두 코더 모두 GPT-6 Astra Pro. A의 사전 라벨 노출을 보존한다. comparison 차이는 같은 코드북 아래 실제 코딩 차이다.',lines='L9-L17')
claim('B12','016','CODEBOOK.md','S3 L39–43','S3 contribution은 S2의 동일 값을 재사용하며 후보 형태만 별도 분류한다. S3를 기여 판단의 독립 반복으로 세지 않는다.',lines='L39-L43')
claim('B12','016','RESULT.md','Q7 L170–174','불일치 30개 문서 감사에서 동일 판단을 양쪽 역할에 재사용하여 변화 0/30, 근접 오답 1개, 정보 부족 14개, 전체 판정 미부여 15개였다.','evidence/impact.json','$.serialization_note; $.summary; $.rows','summary label_only_judgment_changes=0, reviewed_unique_disagreements=30, known_mismatch_cases=1, insufficient_cases=14, overall_label_not_assigned_cases=15',note='원 수치는 일치. 역할 표시의 인과 효과가 없다는 의미로 승격하면 과대 일반화다.',lines='L170-L174')

claim('B13','012','RESULTS.md','표1·표4 L5–9·49–53','012 full/pooled/동일 언어 6조건×36질의에서 D-b→D-c recall 평균 .268722→.323378, N 평균 .393519→.754630이었다. N 슬롯 건수는 85/2160→163/2160이다(2026-11-20 실행).','results/metrics.csv','corpus=full,judgments=pooled,scope=all,query_language=corpus_language; representation D-b/D-c','각 표현6행의 macro mean; N각행×36 합=85,163; query-condition denominator216,slots2160',note='N의 본문 .394/.755는 질의·조건당 평균 개수이며 슬롯 비율이 아니다. 원 수치·설명 일치.',lines='L49-L53')
claim('B13','014','RESULT.md','표1·Q2 L7–30','014 terms/answers/all 3방법×61질의에서 D-b→D-c N은 17→11건, 질의·조건당 평균 .092896→.060109, 슬롯당 17/1830→11/1830이다(2026-11-20 실행).','results/metrics.csv','bridge=terms,judgments=answers,scope=all,condition b/c','N counts BM25 5→3,LSA5→5,RRF7→3; sum17→11; mean divide183; slots1830',note='원 평균은 맞다. 012와 문서·질의·한계 추가 범위가 달라 경험적 동일조건 모순으로 처리하지 않는다.',lines='L23-L30')
claim('B13','014','RESULT.md','사례 표·필터 반례 L69–84','한계 인라인 추가의 방향은 후보별로 다르다: T004 Librarika는 LSA 11→1위, T044 Guacamole는 BM25 10→24위였다(동일 014 실행).','results/counterexamples.json','$.inline_increases_N; $.inline_reduces_N','저장 순위 11→1 및 10→24 직접 대조',note='두 후보 모두 연구자가 지정한 N. 평균 방향을 모든 후보의 개선·악화로 확대하지 않는다.',lines='L69-L84')

claim('B14','012','RESULTS.md','판정 출처 민감도 L135–145','동일 15질의에서 pooled nDCG는 M2 .335327 > M3 .334482지만 내부 별도 판정에서는 M3 .308483 > M2 .307296였다.','results/metrics.csv','corpus=full,scope=all,judgments=review_pool/review_independent,동일 언어 셀 평균','review_pool/review_independent별 M1/M2/M3의 동일 실험 셀 평균 재계산',note='순위 뒤집힘은 작고 정답 수집 범위도 다르다. 방법 우월성의 확정 근거가 아니다.',lines='L135-L145')
claim('B14','014','RESULT.md','표3 L34–41','동일 10질의에서 실제 답 nDCG는 BM25 .4650 > RRF .4035 > LSA .3313, 내부 별도 판정은 BM25 .4758 > LSA .4449 > RRF .4357이다.','results/metrics.csv','bridge=terms,condition=b,scope=all,judgments=review_answers/review_independent','각 judgment의 BM25/LSA/RRF 행 직접 대조',note='MRR 순위는 바뀌지 않았다. 동일 모델 계열 내부 별도 검토이며 사람 정답이 아니다.',lines='L34-L41')
claim('B14','014','RESULT.md','Q5 L107','내부 검토 290쌍의 전체 일치 279/290과 달리 새 관련 판정의 합집합은 12쌍, 공통은 3쌍이었다. 다수 음성 일치만으로 양성 판정 신뢰도를 보증하지 않는다.','qrels/independent.tsv','query_id/doc_id 관련 판정 집합; qrels/pooled.tsv 동일 pair 대조','reviewed 290pair 중 원 pool과 독립 grade 합의 집계; relevant union12 intersection3',note='관련 판정이 희소하므로 전체 일치율과 관련 판정 집합 겹침을 병기한다.',lines='L107')

claim('B15','013','RESULT.md','Q1·표4 L89–101·161–166','31개 설계 사례의 gold 176개는 external_entity 30개와 structural_design 146개이며, 역할 축의 같은 분야 다른 설계 146개와 동일 집합이라는 뜻이 아니다.','cases/CASES.json','$.cases[*].gold_items[*].role/match_kind','gold 총176; match_kind별30/146; role별146/17/12/1; role×match_kind 교차표 계산',note='결정창 2000-07-27~2023-11-28, 검색일2026-11-20. gold는 채택1/기각99/참조76을 포함하며 모두 정답 추천은 아니다.',lines='L89-L101')
claim('B15','013','RESULT.md','Q3–Q4 L120–136','동일 gold176에 대해 역사 시점까지 인정한 A 적중16/176, B5/176; 날짜를 무시한 합치기는 A23/176, B14/176이다. 후보 수 A204/B138과 gold 분모를 혼동하지 않는다.','evidence/AGGREGATES.json','$.baseline_totals.A/B; $.corpus','strict_historical_gold_pairs16,5; all_matches_gold_pairs23,14; candidate_count204,138',note='A와 B는 검색 예산·정보 접근 방식이 달라 단순 공정 성능 순위가 아니다.',lines='L120-L136')
claim('B15','013','RESULT.md','판정·실제 적용 L134–146','342 후보 판정 중 CONDITIONAL 318/342, DIRECT 3/342, INSUFFICIENT 21/342이며 실제 적용 결과는 0/342다.','evidence/AGGREGATES.json','$.baseline_totals.A.labels; $.baseline_totals.B.labels','A 192/2/10 + B126/1/11 = CONDITIONAL318/DIRECT3/INSUFFICIENT21',note='부분 범위의 조건부 쓸모와 역사적 gold 적중 및 실제 적용은 별도 지표다.',lines='L134-L146')

claim('B16','015','RESULT.md','표2 L22–33','2026-11-20 관측에서 HTTP404/410은 판정 가능한 이유92개 중 TP0/FN3/FP2, archived는 이유124개 중 TP0/FN5/FP10이었다.','results/confusion.json','$.http_dead.strict; $.github_archived.strict','n=TP+FN+FP+TN 각각92/124; 원 이유의 중복 후보 유지',note='같은 날 상태를 맞춘 후향 관측이며 향후 붕괴 예측률이 아니다. 초기 오류·순환 판정 제외.',lines='L22-L33')
claim('B16','015','RESULT.md','비용 L75','동일 12개 항목에서 직접 확인 A는 본문24쪽, 신호 뒤 선별 C는 본문14쪽(10/24 감소)이었지만 알려진 후발 붕괴2건 모두 선별에서 놓쳤다. 사람 노동 시간은 측정하지 않았다.','results/cost.json','$.summary.A/C; $.manual_reviewer','A body_pages_read24,C14,n12; C unflagged lists에 Directus/Dcoder; human participants0',note='도구 대기·네트워크 시간은 사람 검토 시간으로 바꾸지 않는다.',lines='L75')
claim('B16','015','RESULT.md','재생 L77','정확한 날짜가 있는 후발 사건2개의 주기 재생에서 월·분기·연 확인 지연 중앙값은 12.5/58/242일이다. 실제 운영에서 측정한 지연이 아니다.','results/cadence.json','$.events; $.summary[cohort=exact_date,scenario=first_public_proof]','n2, 월12.5 분기58 연242; all cohort4와 분리',note='요청이 없으면 탐지되지 않는 우측 검열과 요청 주기의 가정을 함께 남긴다.',lines='L77')

claim('B17','015','RESULT.md','Q1–Q2 L59–67','유의미한 이유500개 중 현재 판정 가능한195개는 성립175·약화6·무너짐14이고, 판단 불가305개는 분모 밖이다(2026-11-20).','REASONS.jsonl','reason_type != 이유 없음; now_verdict','537행-이유없음37=500; Counter(now_verdict) 성립175 약화6 무너짐14 판단불가305',note='현재 무너짐14/195는 처음부터 틀린 이유도 포함하여 노후화 사건률로 읽지 않는다.',lines='L59-L67')
claim('B17','015','RESULT.md','Q2 L67','당시 성립하고 현재를 판단할 수 있는 이유83개 중 후발 무너짐은5개, 확인된 답 날짜의 하위집합77개에서는2개다. 처음부터 틀린4개는 분리했다.','REASONS.jsonl','then_verdict=성립 and now_verdict in [성립,약화,무너짐]; answer_date non-null','후발 분모83/분자5, then_verdict 처음부터 틀림4; 확인 답 날짜는 answer_date non-null',note='후발 이유5개 중 Almond2행은 같은 사건이며 OpenZFS1행은 기존 제약 해소다.',lines='L67')
claim('B17','015','RESULT.md','민감도 L93–95','연결 URL 이유275개 중 현재 판정 가능한102개에 무너짐9개, 직접 링크 이유147개 중 현재 판정 가능한50개에 무너짐2개다. 단위·링크 정의가 다르다.','REASONS.jsonl','url_origin 및 now_verdict; direct=원문 지정 또는 011 답 직접 링크','전체500, linked275, direct147; 상태 판정102/50 및 무너짐9/2 집계',note='원문 링크와 후속 보강 링크를 같게 합치면 손상률이 달라 보인다. 연간 발생률을 산출하지 않는다.',lines='L93-L95')

claim('B18','012','RESULTS.md','재현·제약 L108–123','012는 학습형 E5 가중치 접근 실패 후 TF-IDF+LSA를 사용했고, 새 환경에서 top-20 순위27개와 metrics/per_query/pool이 byte-equal이었다.','VERIFICATION.json','$.pooled_replay; $.clean_replay; $.workload','rank_files_byte_equal27; core18+cross_language9; clean replay file list 확인',note='이 재현은 원 결과의 D3-run 보고다. 이번 감사는 그 고정 결과를 재계산했으며 E5를 실행하지 않았다.',lines='L108-L123')
claim('B18','014','HANDOFF.md','재현 L30–34','014는 새 환경에서 순위파일21개와 두 CSV·pool이 byte-equal이었다.','VERIFICATION.json','$.reproducibility','rank_files21; rank_byte_equal=true; metrics/per_query hashes; test_exit0',note='성공한 데이터·코드 재생이지 실제 사용자 업무에서 유용함을 입증한 D4가 아니다.',lines='L30-L34')
claim('B18','014','RESULT.md','E5 차단 L88','HuggingFace와 ModelScope E5 시도는 프록시 CONNECT403으로 막혔고 학습 의미 임베딩 실험을 하지 못했다. LSA를 학습형 의미 모델 결과로 부르지 않는다.','VERIFICATION.json','$.model_access','E5 URL들의 CONNECT403 기록; PyTorch 레지스트리200은 모델 가중치 획득과 별개',note='020은 이 호스트를 재시도하거나 우회하지 않았으며 원 결과의 범위를 대조했다.',lines='L88')

claim('B21','011','HANDOFF.md','Q3 L112','61개 공개 질문의 635답 중 분야·제품군을 넘는 연결은14답/5질문에서 기록됐지만 질문자의 수락·거절은 관측되지 않았다.','evidence/metrics.json','$.main.cross_domain_answers','len=14; unique case_id5; 모든 response none',note='관측창2014–2026 편의 표본. 전이 효용이 없다는 결론이 아니다.',lines='L112')
claim('B21','013','RESULT.md','분야 간 관계 L101–116','176gold 중 다른 분야 원리는1개(1/31사례)이며 외부 다른 분야 인용은0/176이었다. 그 한 사례는 active voice를 Event 필드에 대응한 기각 논거다.','cases/CASES.json','$.cases[*].gold_items[role=다른 분야 원리]','해당 role1; match_kind structural_design; stance rejected; crossdomain external0',note='기록된 역사 문서의 인용 분포이며 수요나 실제 효용의 상한이 아니다.',lines='L101-L116')
claim('B21','013','RESULT.md','반례·새 연결 L144–185','013의 기존 조합 비교에는 새 절차 비교군이 없고, nongold의 다른 생태계 부분 선언 연결은 실제 적용·전이 효과를 측정하지 않았다.',note='H1의 지지·반증 모두 보류한다. 낮은 gold 적중과 nongold 조건부 쓸모는 같은 질문을 재는 값이 아니다.',lines='L144-L185')

claim('B23','014','RESULT.md','입력 L23·130–132','014의 검색 질의는 원 질문0/61, 011 작업자의 요약61/61이다. 결과를 원문 질문 검색 성능으로 전달하지 않는다.','queries/metadata.json','$[*].source/mode/version','61행 source=summary 및 mode=summary; 원문0',note='원문 개정판 획득 실패는 질의 의미 보존의 미확인으로 남긴다.',lines='L23')
claim('B23','014','RESULT.md','질의 변환 L32·126','KO 요약을 EN 자료에 직접 넣은 BM25 recall .1819에서 기술어 브리지 terms .3982로 바뀌었고 무신호 질의는18/61→2/61이었다.','results/metrics.csv','method=BM25,condition=b,judgments=answers,scope=all,bridge raw/terms','동일61개질의, recall 분모59; raw→terms row 비교; queries_without_signal18→2',note='원문 대 요약의 인과 비교가 아니며 브리지는 기술 범주를 알고 작성했다.',lines='L126')
claim('B23','014','RESULT.md','오류 사례 L103','C#/C++의 토큰 합침과 T053 요약의 지시 대상 소실이 기록됐으며 실제 후보가 200위 아래로 내려간 사례가 있다.',note='의미 보존을 보장하는 입력 계약은 검증되지 않았다. 원문·요약·용어 변환 버전과 근거 위치를 별도 보존할 필요를 보여 주는 사례다.',lines='L103')

claim('B24','014','RESULT.md','필터 L67·표1 L7–23','명시 must68개 중39개가 필터 속성으로 매핑됐고, 실제 일치 검사는5문서·8질의·9충돌이었다. BM25 N5→3/610슬롯, recall .3982→.3993이었다.','results/metrics.csv','terms/BM25/answers/all condition b/filter; queries/metadata.json must 집계','N count5→3; recall59질의 평균; 질의61/슬롯610; must 원자료 합68',note='매핑되지 않은 필드를 위반으로 처리하지 않는 작은 실험이며 모든 제약을 검증한 결과가 아니다.',lines='L67')
claim('B24','014','RESULT.md','후보 제거 반례 L84','Boost 의존성의 유효 충돌을 적용하면 답 기반 grade1 GGL이 제거되어 T017 LSA recall .8→.6이 된다.','results/counterexamples.json','$.filter_counterexamples[query_id=T017]','valid_declared_conflict=true; grade1; rank8 제거; recall .8→.6',note='답 기반 관련성과 필수조건 적합성이 다른 정답 정의이므로 이 값만으로 필터 오작동이라고 판정하지 않는다.',lines='L84')
claim('B24','014','RESULT.md','극성 오독 반례 L84','PDF 편집이 필요 없다는 말을 편집 기능 금지로 오독하면 Word의 BM253위가 제거되고 nDCG .306574→.177239, MRR .333333→.1이 된다.','results/counterexamples.json','$.filter_counterexamples[query_id=T021]','valid_declared_conflict=false; rank3 제거; recall .5 유지, ndcg/mrr 하락',note='같은 답 grade1 제거라도 T017은 정의 차이, T021은 입력 극성 해석 오류다.',lines='L84')

BUNDLES=[]
def bundle(i,title,questions,decision,summary,conditions,failure,unknowns,alternatives,relations,nextcheck,levels='D1(원 결과) / 원 연구 D3-run·D3-fetch / H(조립 제안)'):
    claims=[c for c in CLAIMS if c['bundle_id']==i]
    refs=[]
    for c in claims:
        r=dict(task=c['source_task'],sha=c['sha'],path=c['path'],locator=c['locator'],url=c['source_url'])
        if r not in refs: refs.append(r)
    obj=dict(id=i,title=title,brief_questions=questions,decision=decision,summary=summary,
             source_refs=refs,evidence_level=levels,conditions=conditions,failure=failure,
             unknowns=unknowns,status='조건부 채택·보류·교체 가능 / 최종 선택 없음')
    BUNDLES.append(obj)
    path=OUT/'bundles'/f'{i}.md'
    if i in ['B11','B12']:
        return
    lines=[f'# {i} — {title}','','## 식별·질문','',f'- 브리프: {", ".join(questions)}.',f'- 결정 단위: {decision}',
           '- 다른 묶음의 최종 선택 없이 이 보존·운영 원칙의 채택·보류·교체를 판단한다. 실제 성능은 아래 선행 입력이 있어야 비교할 수 있다.',
           '','## 짧은 핵심','',summary,'','## 근거','',
           '고정 SHA의 원 결과와 지정 증거를 2026-11-21 직접 대조했다. 판정자는 앞선 작업자 및 명시된 같은 모델 계열 내부 별도 검토다. 원 연구의 실행·관측과 이번 D1 문서 감사를 구별한다.',
           '','| 주장 ID | 핵심·분모·관측 창 | 원 결과 위치 | 2단계 확인 |','| --- | --- | --- | --- |']
    for c in claims:
        h='없음(문서 정의·해석 대조)' if not c['second_hop_path'] else f'[{c["second_hop_path"].split("/AF-RES-")[-1]}]({c["second_hop_url"]}); {c["second_hop_locator"]}'
        lines.append(f'| {c["claim_id"]} | {c["claim"]} | [{c["source_task"]} {c["locator"]}]({c["source_url"]}) | {h} |')
    lines += ['','## 대안·기발한 조합','',alternatives,'','## 반례·한계','',failure,'',f'적용 조건: {conditions}',f'미확인: {unknowns}',
              '','## 관계','',relations,'','## 검토','',
              'GPT-6 Astra Pro 내부 별도 검토. 근거와 산출 값을 CLAIM_CHECK 및 evidence/audit-numeric-late.json에 남겼다. “일치”는 원 결과의 전달 정확성 판정이며 제품 효과·일반 모집단 타당성 승인이 아니다.',
              '','## 다음 확인','',nextcheck,'']
    path.write_text('\n'.join(lines))

bundle('B11','실제 질문과 부분 질문의 관측 계약',['scope','input'],'질문의 선택 범위와 후속 반응을 별도로 기록한다.',
       '61질문(whole28/part33)·635답. part33에서 명시 선택·사용6와 accepted5의 합집합10; 통합 성공률 아님.',
       '2014–2026 편의 표본; 원 질문 버전·해석자·반응 단계 보존','범위 최초 일치6/15, 역할75/149; 10/33을 통합 성공률로 읽으면 실패','실제 통합 후속; 입력칸 의무화 효과','','','',levels='D1 / 원 연구 URL 관측 D3-fetch')
bundle('B12','후보 형태와 문제에 대한 기여 분리',['identity','evaluation'],'대상 형태와 문제 상대 기여를 별도 축으로 보존한다.',
       '011 동일120개: S1 94/120, S2 85/120, S3 결합75/120. Q7 0/30은 동일 판정 재사용 감사다.',
       '선택 범위·제안 사용·원 라벨·판정자 보존','S2 comparison A0/B14; 세분화만으로 재현성 개선 보장 안 됨','역할 표시 인과 효과·사람 재현성','','','',levels='D1 / 원 연구 코딩 집계 D3-run / H')
bundle('B13','한계 문장을 검색 본문에 넣는 효과',['storage','retrieval'],'한계 문장을 본문에 합칠지 별도 필드로 보존할지 결정한다.',
       '인라인 한계의 평균 방향은 012와 014에서 다르다. 012 N85→163/2160슬롯, 014 N17→11/1830슬롯이다. 같은 검색 문제가 아니므로 방향 차이를 범용 법칙이나 동일조건 모순으로 만들지 않는다.',
       '문서·질의·언어·판정원·추가한 한계의 수를 고정한 비교','014에서도 Librarika11→1의 악화와 Guacamole10→24의 개선이 공존한다. 014 새 자료329개 중 한계 추가15개, 012의156개 일괄 추가와 조건이 다르다.',
       '학습 임베딩에서의 방향, 한계 문장 자체와 전체 색인 변화의 분리',
       '본문 합침은 즉시 검색 가능하지만 부정 어휘도 끌어온다. 별도 필드는 B24의 필터나 검증에 쓸 수 있지만 정규화 비용이 든다. **H:** 원 한계 문장과 출처를 보존하고 인덱스 포함 여부를 버전 있는 투영으로 둔다.',
       'B24는 같은 문제의 별도 제외 검사 대안이며 병용도 가능하다. B14의 판정원, B23의 질의 변환, B12의 역할 분류가 효과 해석의 선행 조건이다.',
       '동일30질의·동일 후보 집합에서 각 질의에 한계 관련 N과 정상 후보를 함께 두고 본문/별도 필드/둘 다를 비교한다. 최소10개의 알려진 제약 위반을 확보하기 전 평균만으로 위치를 고정하지 않는다.')
bundle('B14','판정 출처와 검색 순위의 민감도',['evaluation'],'실제 답·연구자 판정·별도 판정을 분리해 평가한다.',
       '012의15질의와014의10질의 모두 판정 출처에 따라 LSA·RRF의 nDCG 순서가 바뀌었다. 014 전체 일치279/290에 비해 관련 합집합12 중 공통3이라는 값이 양성 판정의 불안정성을 드러낸다.',
       '동일 질의·동일 순위 결과를 여러 qrel로 재평가하며 판정원과 시간 명시','채택 답도 부분 유용성일 수 있고 실제 조건 위반을 포함할 수 있다. 전체 일치율이 높은 것은 음성이 많아서일 수 있다.',
       '독립 사람 판정·실제 사용 성과와의 연결',
       '하나의 정답원을 표준으로 둘 수도 있으나 다른 판정원을 삭제하면 재분석이 불가능하다. **H:** 원 답 신호, 문서 근거 판정, 적용 결과를 각각 저장하고 성능 비교에는 사전 지정한 정답원과 민감도 표를 함께 쓴다.',
       'B11의 반응 구분과 B12의 역할 신뢰도에 의존한다. B15의 역사적 gold는 다른 평가 목적의 대안이다. B24에서 관련성과 필수조건 적합성의 충돌을 설명한다.',
       '최소30질의에서 알려진 관련/무관/제약 위반 후보를 섞어 두 판정원과 별도 판정자가 평가한다. 각 양성 유형10쌍 이상을 확보하고 순위 교환뿐 아니라 어떤 라벨이 바뀌었는지 보존한다.')
bundle('B15','역사적 cutoff와 외부 gold의 단위',['evaluation'],'결정 당시 찾을 수 있었던 근거와 현재 유용 후보를 구분한다.',
       '31설계 사례 gold176개는 외부 실체30·구조적 설계146개다. A의 역사 적중16/176과 전체 날짜 합치기23/176, B5/176과14/176을 구별한다. 조건부 후보318/342와 실제 적용0/342는 역사적 재발견과 별도의 축이다.',
       '결정창2000-07-27~2023-11-28; 검색2026-11-20; gold·cutoff·후보 날짜·부분 범위 보존','같은 분야146과 구조적 설계146은 숫자가 우연히 같지만 집합이 다르다. 기각된 선례도 gold에 포함돼 추천 정답으로 옮기면 의미가 바뀐다.',
       '당시 검색 가용성·공정한 동량 검색 예산·D4 적용 효과',
       '역사 gold는 독립성·시점 통제를 돕지만 문서가 남긴 선례만 담는다. 현재 사용자 문제와 성공한 적용 결과는 다른 정답원이다. **H:** historical_retrieval과 present_utility를 별도 점수표로 둔다.',
       'B14와 같은 평가 문제의 다른 답이며 병용 가능하다. B17의 당시/현재 상태 분리와 함께 쓰인다. B21의 분야 간 탐색 필요성을 gold 빈도만으로 결정하지 않는다.',
       '최소10사례에서 결정 이전 공개·접근 가능성의 독립 증거를 보강하고, 동일 예산의 새 절차 비교군을 둔다. 실제 설계 개선은 최소3건의 적용 사례로 별도 검증한다.')
bundle('B16','값싼 유지 신호와 확인 비용',['maintenance'],'어떤 신호를 검토 대기열에 쓰고 언제 직접 내용을 확인할지 정한다.',
       'HTTP·archive 같은 값싼 신호는 이유의 참·거짓을 대신하지 못한다. 12항목에서 선별은 본문24→14쪽으로 줄였지만 확인된 후발 붕괴2건을 모두 놓쳤다. 비용 절감과 포착률을 같이 보존해야 한다.',
       '2026-11-20 단면 관측; 신호와 상태가 모두 알려진 이유가 분모; 중복 후보 유지','archive FN5는5독립사건이 아니며 HTTP dead FN3/FP2였다. 직접 링크가 살아 있어도 라이선스·기능 이유가 변할 수 있다.',
       '사람 노동 시간·전향 포착률·신호별 독립 양성 충분성',
       '주기 확인, 요청 시 확인, 신호 기반 대기열을 별도로 선택할 수 있다. **H:** 낮은 비용 신호는 검토 우선순위로만 쓰고, 추천 시 핵심 이유는 확인한다. 요청이 없는 자료의 장기 미확인을 명시한다.',
       'B17의 당시/현재 판정이 신호 성능의 정답 전제다. B18의 fetch/run 구분으로 비용의 의미를 고정한다. B13·B24의 제외 조건을 현재형 사실로 갱신하는 데 함께 쓴다.',
       '최소30개 확인된 후발 사건과30개 안정 대조를 모으고 신호별 독립 오경보·놓침5개 이상을 확보한다. 최소3명 검토자가30개 이유를 동일 범위로 읽어 사람 시간을 별도 측정한다.')
bundle('B17','추천 당시 오류와 후발 이유 붕괴 분리',['maintenance'],'내용 상태를 시간 축의 이유 단위로 저장한다.',
       '현재 무너짐14/195와 당시 성립한 이유의 후발 무너짐5/83은 다른 분모다. 5행은5독립사건도 아니며 OpenZFS처럼 옛 제약이 사라진 개선도 포함한다. 이유가 없던37행과 판단 불가305개를 거짓으로 바꾸지 않는다.',
       '답 날짜·당시 근거·현재 확인 시각·이유 방향·동일 사건ID를 보존','현재 틀림을 모두 노후화로 세거나, 부정 제약의 해소를 추천 악화로 세면 방향이 뒤집힌다. 본문 URL과 보강 URL의 표본도 다르다.',
       '305/500의 현재 상태와 대부분 사건의 정확한 변화 시점',
       '문서 단위 최신성은 싸지만 어떤 주장에 영향이 있는지 알 수 없다. 이유 단위 기록은 비싸지만 부분 갱신과 이주가 가능하다. **H:** 처음에는 핵심 추천 이유1개라도 원문 위치·시각·방향을 묶어 남기고 나중에 원자화한다.',
       'B16의 신호 평가에 선행한다. B15의 시점 통제와 함께 사용하며 B24의 제외 조건에 버전·시점을 제공한다. 자료 이름의 정체성과 이유 유효성을 분리한다.',
       '정확한 답 날짜가 있는 후발 사건30개를 확보해 초기 오류·개선·악화를 별도로 코딩한다. 동일 사건 중복을 묶은 값과 이유별 값을 함께 제시한다.')
bundle('B18','재현 가능한 실행과 근거 수준의 경계',['evaluation'],'문서 확인·검색 관측·재실행·실제 적용을 분리해 전달한다.',
       '012의27개,014의21개 순위 파일 재현은 실행 산출물의 동일성을 뒷받침한다. E5가 차단되어 LSA를 쓴 사실은 남겨야 한다. 결과를 사용자 과제 성공 D4나 학습 임베딩 결과로 올려 부르지 않는다.',
       '고정 데이터·코드·환경·판정 파일·실행 로그를 함께 보존','HTTP200은 내용 타당성을 보증하지 않고 byte-equal은 판정의 정답성을 보증하지 않는다. 같은 모델 계열의 검토를 사람 또는 독립 다른 모델로 부르지 않는다.',
       'E5 실행 결과·독립 환경의 실제 사용자 적용',
       '실행을 모두 다시 하는 안은 비용이 높다. **H:** 먼저 고정 산출물·분모를 재계산하고 결론을 바꾸는 실행만 다시 한다. D3-search/fetch/run을 각각 붙여 필요한 재확인의 종류를 드러낸다.',
       'B13·B14·B23·B24의 실험 효과 전달에 함께 쓴다. B22의 인수 상태와 내용 수준은 독립이며 실행 성공으로 수용 조건을 자동 충족시키지 않는다.',
       '동일 모델 가중치 접근이 허용된 환경에서만 지정 revision·질의·판정 파일을 입력해 E5 비교를 실행한다. 네트워크 우회 없이 실행 명령과 입력을 인계하며 실제 유용성은 별도 사용자 사례로 평가한다.')
bundle('B21','다른 분야 원리 수요의 빈칸',['scope','retrieval'],'다른 분야 탐색을 기본 기능으로 할지 선택 기능으로 둘지 판단한다.',
       '011에는 전이 연결14답/5질문과 반응 미관측,013에는 다른 분야 gold1/176과 외부 인용0/176이 있다. 둘은 유용성 없음의 증거가 아니다. 현재 묶음은 수요·효과의 빈칸을 명시하며 기본 기능 채택을 열어 둔다.',
       '관측된 인용·참여자 반응·실제 전이 성공을 별개 변수로 다룬다.','문서가 원리를 명시 인용하지 않아도 설계에 영향을 주었을 수 있다. nongold 조건부 연결이 유용해 보여도 실제 적용 효과는 관측되지 않았다.',
       '분야 간 탐색을 원한 실제 문제의 수요·실패율·추가비용 대비 효과',
       '기본 탐색에 포함, 사용자가 요청할 때만 확장, 연구용 채널로 분리하는 세 선택을 보존한다. **H:** 같은 문제에서 분야 내 후보가 막힌 이유를 먼저 적고 구조 대응이 가능한 분야로 확장한다.',
       'B11의 실제 수요와 B15의 역사적 gold는 보완 입력이지만 어느 하나가 선택을 강제하지 않는다. B20의 대안 보존 원칙을 적용한다. AF-RES-017~019의 결과는 읽지 않았고 해당 후속 입력은 대기 상태다.',
       '분야 내 후보로 해결하지 못한 실제 문제 최소10개를 사전 선정해 분야 내/분야 간 탐색을 동일 예산으로 비교한다. 최소3개는 구조 대응을 실제로 적용하고 음성·실패 사례도 남긴다.',levels='D1 / 원 연구 D3-search·D3-fetch / H / 빈칸 묶음')
bundle('B23','원문 질의와 요약 질의의 의미 보존',['input'],'원문·요약·기술어 변환을 별도 버전으로 저장한다.',
       '014는 요약61개만 검색했으며 원문은0개다. 용어 브리지가 BM25 recall .1819→.3982로 바꿨지만 원문 보존의 효과를 검증한 것은 아니다. 질의를 덮어쓰면 나중에 조건 소실의 원인을 복구할 수 없다.',
       '원문 URL·시점·해시 또는 허용 범위 인용, 요약 작성자·변환 규칙·검색 질의 보존','C#/C++ 토큰 합침과 지시 대상 소실은 짧은 요약이 의미를 지울 수 있음을 보여 준다. 카테고리를 알고 만든 브리지는 범용 질의 성능이 아니다.',
       '같은 원문/요약의 짝지은 성능·충족 조건 보존률',
       '원문 바로 검색, 요약 검색, 구조화+브리지 검색은 대체 가능하다. **H:** 질의 생성기를 교체 가능한 투영으로 두고 사용자의 원 요구를 변형 결과로 덮어쓰지 않는다.',
       'B11의 원 질문·선택 범위와 함께 쓰인다. B24의 극성·force 해석에 선행하며 B13의 저장 효과 비교에서 질의 버전을 고정해야 한다.',
       '최소30개의 동시 확보 원문·요약 쌍을 두 판정자가 조건 단위로 비교하고, 부정·예외·지시 대상·고유 토큰을 포함한 known-bad 변환을 넣는다. 보존 실패가 있는 변환은 원문 재확인 단계로 되돌린다.')
bundle('B24','별도 제외 필터의 양면',['retrieval','storage'],'불명확·선호·명시 필수 위반을 구분해 후보를 제외할지 결정한다.',
       '014의 별도 필터는5문서·8질의·9충돌이라는 작은 범위에서 BM25 N5→3/610을 보였다. 그러나 관련 grade1 제거에는 유효 must 충돌과 극성 오독이라는 서로 다른 원인이 있다.',
       '제약의 대상·극성·강제성·출처 위치가 알려졌을 때만 제외; 미매핑은 unknown','T017 GGL은 유효 Boost 충돌로 제거돼 답 기반 recall이 낮아지고, T021 Word는 편집 불필요를 편집 금지로 오독해 잘못 제거된다. 두 사례를 같은 필터 실패로 합치지 않는다.',
       '더 넓은 제약 유형·독립 판정에서의 오제외율과 실제 사용자 비용',
       'hard filter, 순위 감점, 검증 대기 표시는 대안이다. **H:** 근거가 충분한 명시 must만 hard filter로 쓰고 원문 위치와 배제 사유를 복구 가능한 로그로 남긴다. 한계 본문을 보존하면서 필터 적용 여부만 바꿀 수 있다.',
       'B13과 대체 또는 병용. B23의 의미 보존과 B11의 must/prefer 구분이 선행하며 B14의 관련성 정답과 적합성 판정 차이를 병기해야 한다. B17은 시간에 따라 변하는 조건을 갱신한다.',
       '최소30질의에서 명시 위반·선호·불명확·극성 경계 각10쌍 이상을 확보하고 두 판정자가 원문 위치를 독립 확인한다. 알려진 나쁜 후보를 포함하여 recall와 위반 제거, 정상 후보 오제외를 함께 측정한다.')

for c in CLAIMS:
    extra={
        'C-B12-01':[('016','coding/coder-b.json'),('016','sample/units.json'),('016','evidence/agreement.json')],
        'C-B14-03':[('014','qrels/pooled.tsv')],
        'C-B24-01':[('014','results/per_query.csv'),('014','corpus/entries.jsonl'),('014','queries/metadata.json'),('014','src/constraints.py')],
    }.get(c['claim_id'],[])
    if extra:
        c['additional_second_hops']=[dict(sha=FIX['AF-RES-'+t],path=full(t,p),url=url(t,p)) for t,p in extra]
dump('evidence/claims-late.json',CLAIMS)
dump('evidence/bundles-late.json',BUNDLES)

SOURCES=[]
def source(t,p,id,sections,confirmed,limits,questions,reported=None):
    s=dict(id=id,url=url(t,p),accessed_at_utc=NOW,source_type='internal_result' if not p.endswith(('.json','.jsonl','.csv','.tsv','.py')) else 'internal_evidence',
           title=f'AF-RES-{t} {p}',version_or_date=FIX['AF-RES-'+t],sections_read=sections,
           confirmed=confirmed,limits=limits,level='D1',used_in=questions,
           access_method=f'git show {FIX["AF-RES-"+t]}:{full(t,p)}')
    if reported:s['reported_evidence_level']=reported
    SOURCES.append(s)

for t,files in {
 '011':['HANDOFF.md','CODEBOOK.md','CASES.json'],
 '012':['HANDOFF.md','RESULTS.md'],
 '013':['HANDOFF.md','RESULT.md','SELF_CHECK.md'],
 '014':['HANDOFF.md','RESULT.md','SELF_CHECK.md'],
 '015':['HANDOFF.md','RESULT.md','SELF_CHECK.md'],
 '016':['HANDOFF.md','RESULT.md','VOCAB_MAP.md','CODEBOOK.md','evidence/vocab-map-data.json']}.items():
    for p in files:
        section='전체 본문(표·정의·방법·한계)' if p!='CASES.json' else '루트 구조; cases의 개수·scope·platform·answer 개수·반응 필드 집계만'
        # File-level confirmations intentionally describe what this source verifies, not external facts.
        conf={
          '011':'질문·답 단위, whole/part, accepted와 사용 보고의 구분 및 표본·재판정 한계를 확인했다.',
          '012':'D-a/b/c 검색 실험의 분모, N 평균, 판정원 민감도, LSA 대체와 실행 재현 범위를 확인했다.',
          '013':'31설계 사례·176gold의 역할/종류 구분, cutoff·후보 날짜·조건부 판정과 당시 인수 차단 상태를 확인했다.',
          '014':'요약61/원문0, 한계 본문·필터의 서로 다른 효과, 판정원 민감도 및 원문 의미 손실 사례를 확인했다.',
          '015':'현재 상태와 후발 붕괴의 분모, 값싼 신호 오경보·놓침, 도구 비용과 사람 시간의 차이를 확인했다.',
          '016':'S1/S2/S3의 판단 대상, 실제 두 코더 차이, Q7 판정 재사용, 42행 어휘 대응의 보존 원칙을 확인했다.'}[t]
        source(t,p,f'I{t}-'+p.replace('evidence/','').replace('.md','').replace('.json','').replace('/','-').upper(),section,conf,
               '앞선 연구의 고정 결과를 읽은 것이며 원 외부 자료를 재조사하거나 사용자 적용 효과를 새로 측정하지 않았다.',
               ['Q1','Q2','Q3','Q4','Q5','Q6','Q7'],reported='원 결과에 명시된 D1/D2/D3를 GLOSSARY에서 세분화')

extras=[
 ('011','evidence/metrics.json','$.main(특히 scope,answer_units,cross_domain_answers,partial_questions)','주요 집계와 단위·반응 미관측을 확인했다.'),
 ('012','results/metrics.csv','full/pooled/review*/all·whole·part 및 동일 언어 행','실험 셀별 평균·분모를 직접 계산했다.'),
 ('012','VERIFICATION.json','pooled_replay,clean_replay,workload,corpus_creation_observation','27개 순위 파일과 clean replay 범위를 확인했다.'),
 ('013','evidence/AGGREGATES.json','corpus,baseline_totals,roles,gold_types,union','후보 수와 gold 적중 분모, 판정 라벨 총계를 확인했다.'),
 ('013','cases/CASES.json','cases[*].gold_items의 role/match_kind/stance 집계 및 분야 간 1항목','gold 역할과 종류가 다른 축임을 교차 집계했다.'),
 ('014','results/metrics.csv','terms/raw,answers/review*,b/c/filter,scope별 행','N 평균의183질의·조건과1830슬롯, 판정원·필터 효과를 확인했다.'),
 ('014','VERIFICATION.json','acceptance_counts,reproducibility,model_access','21개 순위 파일, 원문0/요약61 및 모델 차단을 확인했다.'),
 ('014','results/counterexamples.json','filter_counterexamples,inline_reduces_N,inline_increases_N,adopted_beyond_20','두 다른 원인의 제외 사례와 인라인 효과의 양방향 반례를 확인했다.'),
 ('014','queries/metadata.json','$[*]의 source,mode,must,whole_or_part,I5 집계','요약61, must 원자료 개수, 질문 하위 집단을 확인했다.'),
 ('014','qrels/independent.tsv','전체 pair·grade 및 pooled pair 대조','독립 판정290쌍과 양성 공통/합집합을 재계산했다.'),
 ('014','qrels/pooled.tsv','독립 검토와 공통인 pair·grade','같은290쌍의 원 pool 판정을 비교했다.'),
 ('014','qrels/EXCLUSIONS.md','전체','명시 must와 필터 제외의 조건을 확인했다.'),
 ('015','REASONS.jsonl','reason_type/then_verdict/now_verdict/url_origin/reason_direction 및 시점 집계','현재195·후발83·이유500의 분모와 중복 사건을 확인했다.'),
 ('015','results/confusion.json','각 signal의 strict와 weak_positive 및 오류 사례','각 신호의 분모·FN·FP를 확인했다.'),
 ('015','results/cost.json','summary.A/B/C,counting,manual_reviewer','12항목의 페이지·HTTP·도구 시간과 사람 참여0을 확인했다.'),
 ('015','results/cadence.json','events,summary exact_date/all','정확 날짜2사건과4사건 민감도, 주기 지연을 확인했다.'),
 ('015','src/report_tables.py','분모·날짜·링크 집계 함수','REASONS 집계의 필터와 날짜 판정 기준을 확인했다.'),
 ('015','VERIFICATION.json','offline_outputs_identical,checks,not_executed,resumption','원 결과의 재생·미실행 경계를 확인했다.'),
 ('016','evidence/agreement.json','main,baseline,S3_decomposition,paired_011_differences','원 코더 파일과 일치율·comparison 주변 분포를 대조했다.'),
 ('016','evidence/impact.json','serialization_note,method,summary,rows,new_use_hypotheses','0/30이 동일 판정 재사용이며 14정보부족·15미부여를 포함함을 확인했다.'),
 ('016','coding/coder-a.json','metadata; rows unit_id,S1,S2,S3','코더 A의 사전 노출과 실제 선택을 확인했다.'),
 ('016','coding/coder-b.json','metadata; rows unit_id,S1,S2,S3','코더 B의 별도 코딩과 comparison 사용을 확인했다.'),
 ('016','sample/units.json','units의 ID와 sample 분류; 텍스트 내용 재수집 없음','011/012/004 표본 분리용 식별자를 확인했다.'),
 ('014','results/per_query.csv','terms/BM25/filter/answers의61행과 conflicts','충돌이 있는8질의,9개 충돌을 재집계했다.'),
 ('014','corpus/entries.jsonl','id,exclusions 및 D-b/D-c 차이 집계','제외 조건이 있는5문서, 한계 설명이 달라진171/485문서를 확인했다.'),
 ('014','src/constraints.py','NEEDS,BANS,normalize_target,query_concepts,conflicts','정확 일치·극성 검사로 must68개 중39개를 매핑한 규칙을 읽고 재계산했다.'),
 ('014','src/concepts.tsv','기술어 영어·한국어 대응표 전체','기술 범주를 알고 작성한 브리지의 실제 용어 범위를 읽었다.')
]
nums={}
for t,p,sec,conf in extras:
    nums[t]=nums.get(t,0)+1
    source(t,p,f'I{t}-E{nums[t]:02}',sec,conf,
           '고정 원 연구의 판정·산출물이 입력이다. 새 독립 정답이나 외부 서비스의 현재 상태를 확인한 것이 아니다.',
           ['Q1','Q2','Q3','Q4','Q5','Q6','Q7'],reported='D3-run' if p.endswith(('.csv','.tsv','.py')) else 'D3-fetch 또는 D3-run: 원 파일별 명시')
dump('evidence/sources-late.json',dict(sources=SOURCES,excluded=[]))

v=json.loads(subprocess.check_output(['git','show',FIX['AF-RES-016']+':'+full('016','evidence/vocab-map-data.json')]))
additions=[
 dict(task='013',term='gold / adopted / rejected / referenced',question='결정 기록의 비교 대상인가, 채택 결과인가',mapping='014 relevance·012 grade와 직접 동치 없음',not_equal='gold176은 adopted1/rejected99/referenced76을 포함한다. 추천 승인이 아니다.',source='RESULT.md L97–101; cases/CASES.json'),
 dict(task='013',term='role / match_kind',question='기여 종류인가, 맞추는 실체의 단위인가',mapping='016 form/contribution과도 별도 정의',not_equal='같은 분야146과 structural_design146은 수가 같아도 동일 집합이 아니다.',source='RESULT.md L161–166; cases/CASES.json'),
 dict(task='013',term='strict historical / any-date match',question='cutoff 이전 근거로 찾았는가',mapping='015 then/now는 타당성 상태를 묻는 별도 축',not_equal='현재 URL 확인이나 이름 일치가 당시 접근·적합을 증명하지 않는다.',source='RESULT.md L120–136'),
 dict(task='013',term='CONDITIONAL / nongold useful',question='부분 범위에 조건부 쓸모가 있는가',mapping='004 CONDITIONAL_TRANSFER와 범위·근거 조건을 동시 보존',not_equal='318/342 CONDITIONAL, D4 적용0/342. gold 재발견이나 실제 성공이 아니다.',source='RESULT.md L134–146'),
 dict(task='014',term='answers / pooled / review_independent',question='누가 어떤 근거로 relevance를 부여했는가',mapping='012 seed/pooled/review와 판정 출처 축만 대응',not_equal='정답 출처를 합쳐 단일 truth로 덮어쓰면 LSA/RRF 순위 반전 원인을 잃는다.',source='RESULT.md L34–41·107'),
 dict(task='014',term='N@10 mean / N count / n_per_slot',question='질의당 개수인가, 슬롯 비율인가',mapping='012 near_misses_at10와 평균 개념만 대응',not_equal='.0929=17/183이며17/1830은 슬롯 비율이다. 원 결과는 둘을 구별한다.',source='RESULT.md L23–30; results/metrics.csv'),
 dict(task='014',term='must / prefer / mapped / conflict / removed_relevant',question='명시 강제조건인가, 기계 매핑인가, qrel 손실인가',mapping='004 H와 조건부 연결',not_equal='관련1 후보의 제거가 유효 제약 충돌일 수도 있고 극성 오독일 수도 있다.',source='RESULT.md L67·84; results/counterexamples.json'),
 dict(task='014',term='original / summary / raw / terms',question='원 질문인가, 입력 요약인가, 검색 변환인가',mapping='001 formulation과 유사한 표현 축',not_equal='raw는 원문을 뜻하지 않는다. 014의 원문은0/61, raw도 요약의 무브리지 버전이다.',source='RESULT.md L23·126·130'),
 dict(task='015',term='성립 / 약화 / 무너짐 / 판단 불가 / 이유 없음',question='특정 이유의 현재 유효성은 어떠한가',mapping='003 동일성 hold·004 INSUFFICIENT와 직접 동치 없음',not_equal='원자 이유의 상태이며 제품 전체 생존 여부나 추천 적합성은 아니다.',source='RESULT.md L59–67; REASONS.jsonl'),
 dict(task='015',term='처음부터 틀림 / 후발 무너짐',question='추천 당시부터 틀렸는가, 성립하다 바뀌었는가',mapping='013 cutoff는 근거 시점, 별도의 진위 축',not_equal='14/195 현재 무너짐과5/83 후발 무너짐의 분모·사건이 다르다.',source='RESULT.md L63–67'),
 dict(task='015',term='추천 속성 / 제약 또는 비교 주장',question='이유의 방향이 바뀌면 추천에 어떤 의미인가',mapping='014 positive/negative condition과 조건부 관계',not_equal='OpenZFS의 옛 제약 해소는 이유 붕괴이지만 기능 개선이다.',source='RESULT.md L67; results/cadence.json'),
 dict(task='015',term='signal positive / TP / FN / FP / stale',question='관측 신호와 내용 상태가 어떻게 대응하는가',mapping='D3-fetch 신호와 D1 내용 확인을 분리',not_equal='archive·404는 판정 자체가 아니다. 같은 날 관계를 향후 예측률로 바꾸지 않는다.',source='RESULT.md L22–33'),
 dict(task='015',term='tool seconds / human labor / detection delay',question='기계 대기인가, 사람 검토인가, 재생 지연인가',mapping='012 run elapsed와 비용의 일부만 대응',not_equal='사람0명·정확 사건2개. 도구 시간과 가정된 지연을 실운영 노동 절감으로 읽지 않는다.',source='RESULT.md L75–77')
]
dump('evidence/vocab-late.json',dict(base_task='AF-RES-016',base_sha=FIX['AF-RES-016'],
     base_path=full('016','evidence/vocab-map-data.json'),base_rows_preserved_verbatim=v['rows'],
     base_header=v['header'],base_row_count=len(v['rows']),additions=additions,
     note='기존42행 원 데이터는 수정하지 않았다. 009 추가·상태 정규화·최종 GLOSSARY는 root가 조립한다.'))
print(json.dumps(dict(bundles=len(BUNDLES),claims=len(CLAIMS),second_hop=sum(bool(c['second_hop_path']) for c in CLAIMS),sources=len(SOURCES),vocab_base=len(v['rows'])),ensure_ascii=False))
