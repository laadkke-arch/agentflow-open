"""Render the prescribed tables and the research synthesis from frozen judgments."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
P = "docs/workstreams/research/AF-RES-013/"
REPO = "https://github.com/laadkke-arch/agentflow-open/blob/"
RUN_COMMIT = "caa2a814727dd485ed0eb9bb8530d6b16fab9584"
JUDGE_COMMIT = "eaa156ced81cc889990a2ce0e7749e43159bb71f"
ROLES = ["같은 목적 완성품", "재사용 부품", "같은 분야의 다른 설계", "다른 언어·생태계", "다른 분야 원리", "표준·논문"]


def read(path):
    return json.loads((ROOT / path).read_text())


def link(label, url):
    return f"[{label}]({url})"


def own(label, path, commit=JUDGE_COMMIT):
    return link(label, REPO + commit + "/" + P + path)


def pct(n, d):
    return f"{n}/{d} ({100*n/d:.1f}%)" if d else "0/0 (해당 항목 없음)"


def esc(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |", *["| " + " | ".join(esc(v) for v in row) + " |" for row in rows]])


def main():
    cases = read("cases/CASES.json")["cases"]
    ag = read("evidence/AGGREGATES.json")
    metrics = {c["id"]: c for c in ag["cases"]}
    sources = {s["id"]: s for s in read("sources.json")["sources"]}
    totals = ag["baseline_totals"]
    judgments = read("JUDGMENTS.json")["judgments"]
    def src(sid, label=None):
        return link(label or sid, sources[sid]["url"])
    out = ["# AF-RES-013 — 실제 설계 문서의 선행 사례·대안 회수 기준선\n", "## §1 필수 결과 표\n", "### 표 1 — 사례별 결과\n"]
    rows = []
    for case in cases:
        cid = case["id"]
        m = metrics[cid]
        gids = {g["id"] for g in case["gold_items"]}
        names = {g["id"]: g["name"] for g in case["gold_items"]}
        found = {b: {g for _, g in m[b]["strict_historical_gold_pairs"]} for b in "AB"}
        common = sorted(gids - found["A"] - found["B"])
        def named(ids):
            return "; ".join(f"{gid}: {names[gid]}" for gid in ids) or "없음"
        missed = "공통: " + named(common)
        if found["B"] - found["A"]:
            missed += "; A만: " + named(sorted(found["B"] - found["A"]))
        if found["A"] - found["B"]:
            missed += "; B만: " + named(sorted(found["A"] - found["B"]))
        hist = [f"{m[b]['strict_historical_hits']}/{len(gids)}; 날짜 무관 {m[b]['all_matches_hits']}" for b in "AB"]
        useful = "; ".join(f"{b} {m[b]['nongold_useful']}/{m[b]['nongold_candidate_denominator']} (결정 전 {m[b]['nongold_historical_useful']})" for b in "AB")
        exposure = "; ".join(f"{b} 노출기록 {m[b]['recorded_exposure_entries']}, 사후 후보 {m[b]['date_status_candidates'].get('post_decision',0)}" for b in "AB")
        unknown = "; ".join(f"{b} 날짜 {m[b]['date_status_candidates'].get('unknown',0)}, 근거부족 {m[b]['insufficient_candidates']}" for b in "AB")
        unknown += f" — 미확인(runs/A/{cid}.json·runs/B/{cid}.json의 해당 URL을 cutoff 이전 판과 대조; H 미확인은 JUDGMENTS.remaining_check의 연결 조건 확인)"
        rows.append([cid, case["family"], link(case["canonical_id"] + " @ " + case["pinned_version"][:8], case["url"]), case["decision_date"], f"{len(gids)} (" + "·".join(str(m["gold_roles"].get(r,0)) for r in ROLES) + ")", *hist, missed, useful, f"A {m['A']['near_miss']}; B {m['B']['near_miss']}", f"A {m['A']['broken_or_fake']}; B {m['B']['broken_or_fake']}", exposure, unknown])
    out.append(table(["사례 ID", "계열", "원문 주소(고정 판)", "결정일", "정답 항목 수(완성품·부품·같은 분야 설계·다른 생태계·다른 분야·표준논문)", "기준선 A 적중", "기준선 B 적중", "놓친 정답 항목", "정답원 밖 유용 후보", "근접 오답", "깨진·가짜 링크", "누설·사후 자료", "미확인"], rows))
    out += ["\n### 표 2 — 역할별 집계\n"]
    rows = []
    for r in ag["roles"]:
        n = r["gold_denominator"]
        representative = ", ".join(r["A"]["missed_case_ids"][:4]) or "해당 항목 없음"
        un = "미확인(역할별 실제 효용은 해당 사례에 적용하여 판단)" if n else "미확인(이 역할을 포함한 별도 표본을 구성해야 평가 가능)"
        rows.append([r["role"], n, pct(r["A"]["strict_historical"], n) + f"; 날짜 무관 {r['A']['all_matches']}", pct(r["B"]["strict_historical"], n) + f"; 날짜 무관 {r['B']['all_matches']}", representative, un])
    out.append(table(["역할", "정답 항목 수(분모)", "기준선 A 적중(비율)", "기준선 B 적중(비율)", "대표 놓침 사례 ID", "미확인"], rows))
    out += ["\n### 표 3 — 주장 표\n"]
    c05 = next(c for c in cases if c["id"] == "C05")
    c29 = next(c for c in cases if c["id"] == "C29")
    gap = REPO + "7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/GAP.md"
    rows = [
        ["Q4: 다른 분야 관계 전이는 1/176(0.57%); 외부 다른 분야 자료 인용은 0/176", link("C05 고정 원문", c05["url"]) + "; " + src("RV-R123-TERM") + "; " + own("분류 정정", "cases/CASES.json"), "능동태의 주체·직접/간접 목적어를 Event 필드에 대응한 거절 대안1건. Clojure Atom은 별도 리뷰의 용어 유사성이다.", "최초 0건 분류를 원 SCOPE와 원문으로 반증하여1건으로 정정했다. 용어 차용과 외부 문헌 인용을 함께 부풀리지 않았다.", "미확인(현대 문서 및 비공개 설계자의 빈도는 템플릿 시대·목적별 새 표본으로 확인)"],
        ["Q8: AF009 반대 가설 A/B의 기각 조건은 충족 여부를 판정할 수 없음", link("AF009 GAP §2·§3·§5", gap) + "; " + own("집계", "evidence/AGGREGATES.json") + "; " + src("M03"), f"A 역사 적중 {pct(totals['A']['strict_historical_hits'],176)}, B {pct(totals['B']['strict_historical_hits'],176)}. 새 절차와의 쌍대 비교·오류율/시간 기준은 없다.", "낮은 recall로 제품 우위를 주장하려 했을 때, gold의 구조 대안 편중·정답 밖 후보·도구 접근 제한이 대안 설명으로 남는다.", "미확인(동일 입력·예산의 새 절차 비교와 사전 성공/오류/시간 기준을 실행해야 기각 가능)"],
        ["정답원이 유용한 참고자료 전체를 담지 않는다는 문서상 증거가 크지만, 더 좋은 설계라는 증거는 없음", own("후보별 판정", "JUDGMENTS.json") + "; " + own("C29 A 원 응답", "runs/A/C29.json", RUN_COMMIT) + "; " + src("M05") + "; " + src("M12"), f"정답 밖 A {totals['A']['nongold_useful']}/{totals['A']['nongold_candidate_denominator']}·31사례, B {totals['B']['nongold_useful']}/{totals['B']['nongold_candidate_denominator']}·30사례가 좁은 문서상 참고 조건 통과. 결정 전 근거는 A83/B30. 실제 적용에서 더 나음 확인0건.", "C05 B3의 미제시 grouping equality를 보충한 판정을 취소했고 C13 B1의 격리 경계를 미확인으로 뒀다. C29 partial type은 실제 후속 변경과 부분 대응한다.", "미확인(후보별 적용 및 설계자 비교 판단으로 유용성·우월성을 재평가)"],
        ["네 계열은 입력과 비교 절을 분리하지만, 형식적·빈 절이 실제로 존재함", "[TEMPLATES](TEMPLATES.md); " + src("RV-K177-EMPTY") + "; " + src("M26"), "KEP177의 Alternatives는 작성 안내 주석만 남아 있다. 템플릿 도입 시점과 실제 기입 관행, 리뷰 중 입력 수정은 별개다.", "절 제목 검색으로 적격을 확정하지 않고 R0085 결합 제목 누락을 복구하고 빈 비교절을 제외했다.", "미확인(Go·TC39·IETF·ADR 전체의 충실도는 각 계열 원장 표본 조사)"],
        ["깨진·가짜 링크 및 명시적 필수 제약 위반을 확정한 반환 후보는 0/342", own("판정", "JUDGMENTS.json") + "; " + own("URL 감사", "evidence/RUN_AUDIT.json") + "; " + src("M13") + "; " + src("M14"), "모든 후보와 열린 URL의 대응을 점검했다. 정확 URL 차이5건은 redirect·alternate path·fragment·metadata-only로 나눴다. INSUFFICIENT는21/342다.", "NSString 메타데이터만 열린 행을 지지 근거로 올리지 않고 URL 실패·도구 차단을 가짜로 세지 않았다. 원래 좁힌 참고 범위 밖의 제품 제약을 근접 오답으로 만들지 않았다.", "미확인(미래 가용성·실제 통합 오류는 같은 URL 재열람 및 구현 시험)"],
        ["독립 인용 정답의 불완전성은 다른 분야에서도 관측되나 점수를 무효로 만들지는 않음", src("M05") + "; " + src("M07") + "; " + src("M09") + "; " + src("M12") + "; " + src("M16"), "특허는 심사관 인용에 추가 판정을 더하고, 법률은 observed citations를 가리며, 학술은 실제 참고문헌 재현 편향을 논의한다.", "풀링 편향이 언제나 발생한다는 주장에는 M16의 조건부 반례를 확인했다. 특허12주제 관측을 설계31사례의 효과량으로 전용하지 않았다.", "미확인(새 후보 풀의 독립 적용 판정과 반복 run으로 이 과제의 누락·변동 효과 측정)"],
    ]
    out.append(table(["주장", "근거 자료 주소", "확인한 내용", "반증 시도", "미확인"], rows))
    out += [f"""
### 표의 단위와 판정 책임

- 관측 창은 결정일 **2000-07-27~2023-11-28**, 검색 실행은 **2026-11-20 UTC**다. 각 사례에 A/B를 한 번씩 실행했고 반환 상한은15개, 실제 A204개·B138개다. 표1의 적중 주수치는 결정 전으로 확인된 근거의 고유 `(사례, gold 항목)` 수다. 날짜 무관 수는 사후·미확인 일치도 포함하는 별도 관측이다. 날짜 bucket은 동일 gold에 다른 후보가 대응하면 중복될 수 있으므로 단순 합산하지 않는다.
- ‘놓친 항목’은 역사 적중 기준이다. ‘공통’은 A/B 모두 놓침, ‘A만/B만’은 반대 기준선만 회수한 항목이다. 이름을 찾았어도 당시 자료로 확인하지 못한 항목은 이 열에서 빠지지 않는다.
- 정답 분절·역할과 후보 판정은 **작업자 및 내부 별도 검토**가 수행했다. 문서 저자의 인용은 작업자와 독립된 원천이나, 이 연구의 라벨 자체가 외부 독립 정답은 아니다. 판정 모델 표시는 **GPT-6 Astra Pro**다.
- A/B 실행은 접두부·실행규칙만 받은 새 내부 문맥으로 기록되어 있다. B도 `gold_seen=false`인 내부 모델 번역이며 **정답을 본 사람 번역 기준선이 아니다**. 사람과의 비교, 파일시스템 강제 격리, 사전학습 기억 제거를 주장하지 않는다.
- 정답원 밖 유용 수는 gold와 일치하지 않는 후보 중 **원 응답이 한정한 참고 범위**에서 L/E/H 및 구체 T를 통과한 수다. 완성품 전체, 실제 구현 또는 설계자 효과를 통과한 수가 아니다. 시간 확인까지 통과한 수를 괄호에 별도로 적었다. A/B 사이 같은 후보가 반복되므로 두 수를 독립 선행 사례 수처럼 합산하지 않는다.
- ‘노출기록’은 같은 제안 관련 snippet뿐 아니라 실행자가 보수적으로 기록한 제외 저장소·비허용 목록 노출도 포함한다. 전부 정답 누설이라고 단정하지 않는다. 반환 후보의 제외 판정과 run의 노출 이력은 다르다.
- 역할의 완성품0·표준논문0은 이 표본과 기능 우선 코딩의 결과다. 논문 형식의 자료가 전혀 없었다는 뜻이 아니며 분모0을 실패율0%로 쓰지 않는다.

근거 수준은 문서·논문 본문 D1, 실제 고정 코드를 읽은 경우 D2, 검색 화면 D3-search, 페이지/API 관측 D3-fetch, 이 과제의 실행 기록 D3-run으로 구분한다. 원 문헌의 실험을 이번 D4 적용으로 올리지 않는다. 후속 조사·차별점 가능성은 H에 해당한다.

정확한 행·축·날짜·확인 방법은 {own('JUDGMENTS.json','JUDGMENTS.json')}, 재계산은 {own('AGGREGATES.json','evidence/AGGREGATES.json')}과 `tools/analyze_results.py`에 있다. 원 응답은 수정하지 않았다.

## §2 세부 질문별 답

### Q1. 정답원: 네 계열에서 분리 가능하나 절 이름만으로는 부족하다

Rust RFC, Python PEP, Swift Evolution, Kubernetes KEP의 템플릿·절차와 실제 문서를 직접 읽었다. Rust는 2014-03-10의 Alternatives, 2017-07-19의 Rationale and Alternatives, 2018-02-12 작성/02-27 통합된 Prior art를 구분했다. Swift의 2015-11-03 저장소 최초 템플릿에는 Introduction·Motivation과 Alternatives considered가 이미 나뉜다. PEP1의 대안·다른 언어 선례 지침은 2000-07-25부터 보이고, PEP12의 형식 안내 시작2002-08-26과 Rejected Ideas 절 골격 추가2019-03-08은 다른 사건이다. KEP의 최초 Alternatives 템플릿은 작성2017-08-31/통합2017-09-26이며 현재 경로의 생성일2020년으로 소급하지 않았다. 모든 고정 주소와 부모/커밋 검사는 [TEMPLATES.md](TEMPLATES.md)에 모았다. {src('R-TEMPLATE-PRIOR-MERGE')}; {src('PS-T-SWIFT-INITIAL')}; {src('PS-T-PEP12')}; {src('K-TEMPLATE-NOW')}

실제 접두부는 Summary·Motivation·Goals 등의 **문제 문장**만 연구자가 요약하고 제목·번호·최종 해법·대안명·링크를 제거했다. Rationale에 문제와 대안이 섞인 오래된 PEP는 절 전체를 잘라 넣지 않았다. 리뷰에서 초록·동기가 수정될 수 있다는 PEP642 토론과, 최종 특허 명세서에 이미 선행기술 검색 결과가 반영될 수 있다는 CLEF-IP 분석은 ‘절 이름이 결정 전처럼 보인다’는 것과 시점 적격성이 다르다는 근거다. {src('M26')}; {src('M06')}

빈 절의 반례도 확보했다. KEP177은 GA 이력을 가진 문서에서 Alternatives가 안내 주석뿐이며, 선정 원장에는 KEP177·265·284·361의 빈 템플릿 제외가 남아 있다. 리뷰 내용도 본문과 다르다. C22의 Sync·Tasksafe·Atom, C28의 추가 selector 대안은 별도 review pool에 남겼다. 따라서 이 정답원은 저자가 기록한 비교 집합이지 가능한 모든 관련 자료의 목록이 아니다. {src('RV-K177-EMPTY')}; {src('R-REVIEW-123')}; {src('PS-R-S21-LENS')}

### Q2. 사례 집합: 31개·4계열·채택 후 대체6개를 확보했다

공식 목록의 번호 오름차순, 계열 quota, 건너뛰기 규칙과 시드1313은 첫 커밋 `4398d0b`의 SCOPE·SAMPLING에 고정했다. 시드는 실행 순서용이며 확률 표집이라는 뜻이 아니다. 실제로는 Kubernetes6·Python9·Rust8·Swift8, 최대 계열9/31(29.0%), 항목 최소3개·합계176개다. 엄격한 채택 후 대체/부분 번복은 C07·C12·C14·C21·C29·C31의6개다. C10의 기각 후 대체, C11/C13의 초안 대체는 이6개에 넣지 않는다. 결정일은 수락·기각·설계 병합·대체 상태 반영 사건이며 출시일과 다르다. [SAMPLING](SAMPLING.md); {own('CASES','cases/CASES.json')}; {src('M05')}

접두부30개는 `8cb2b8e58f7d4278c11073956b31b30ad43aff18`, C14의 공식 수락일 정정은 `c9936188a885848a16b55b4e11ac965bd2d0b204`, 누락된 C31 복구는 `ba1cc08705e4a1c56fcdb1a8062193ca4748992e`다. 모두 첫 gold `f6f59a85949a001792b80260dd454c3fcc714a70`의 엄격 조상이다. C31은 LooseVersion·StrictVersion을 하나로 묶은 초기 분절 오류를 gold 공개 전에 바로잡은 사례이며, 기존 A 일부가 시작된 뒤였다는 절차 이탈을 숨기지 않았다. 31개 접두부 해시와 원 run의 입력 경로는 일치한다. [PREFIX_MANIFEST](cases/PREFIX_MANIFEST.json); [선정 원장](SAMPLING.md); {src('M02')}

목록·스크리닝·포함 수는 구별했다. Rust 원장40행, Python/Swift91행, KEP45행 중에는 자동 길이 검사나 부분 미리보기만 한 기록도 있어 전부 본문 출처로 세지 않았다. KEP686개 목록을 읽었다고686개 문서를 읽은 것으로 세지도 않았다. 비사례 최소수는 **25개·13사이트·사이트당 최대3개**다. 템플릿4, 방법론6, 특허·법률·학술 개요, 새 생성형 인용 평가2, 실제 리뷰 토론5를 분리해 확인했다. M25 수락 공고 대신 이미 읽은 실제 토론 PS-R-S21-LENS를 최소수에 넣어 좁은 토론 요건도 충족했다. [SOURCE_COUNT](evidence/SOURCE_COUNT.json); [sources](sources.json)

### Q3. 정답 항목은 외부 실체보다 내부 설계 대안에 치우쳤다

기능 역할은 같은 분야 다른 설계146/176, 재사용 부품17/176, 다른 언어·생태계12/176, 다른 분야 원리1/176이다. 채택1·거절99·참고76이며, 거절한 항목도 그 문서가 실제 고려한 대상이므로 회수 정답에 포함한다. 채택 권고의 정답과 혼동하지 않는다. 완성품이나 논문을 발행 형식만으로 우선 라벨링하지 않았다. {own('CASES','cases/CASES.json')}; {src('M07')}

별도 구분인 `external_entity`는30개, `structural_design`은146개다. 예컨대 Distutils LooseVersion·StrictVersion과 Python bytes는 특정 외부 대상이다. 반면 pod 설정을 status에 두기, closure receiver를 추론하기, underscore로 partial application을 표현하기는 구조 대안이다. A가 generic callback을 찾았다는 이유로 C14의 함수 지역 상태 보존 대안과 같게 세거나, C27에서 같은 arity의 callable을 찾았다는 이유로 다른 argument label을 구별한다고 세지 않았다. {own('경계 판정','JUDGMENTS.json')}; {src('PS-R-S21-LENS')}

최초 분류 오류는 정정 이력으로 남겼다. C05의 능동태 구조를 ‘외부 문헌이 없으므로 먼 분야가 아니다’라고 했던 오류1건, forum URL이 있다는 이유로 외부 실체처럼 분류한 구문/인터페이스4건을 수정했다. 후자에는 baseline이 못 찾은 lens·type-safe selector도 포함되어 적중에 유리한 항목만 바꾸지 않았다. 항목 identity·176개 분모·접두부·원 응답은 유지했다. 본문에서 리뷰 추가가 확인된 것은7개이고, 나머지169개의 추가 시점은 unknown이다. 이를 ‘리뷰 추가 아님’으로 바꾸지 않는다. 별도 리뷰7개 중 DRF는 기존 DataRaceFree의 별명이므로 확대 분모는182개다. 기준선은 이 별도 고유 리뷰6개를 추가 회수하지 못했다. {own('coding_revisions','cases/CASES.json')}; {src('R-REVIEW-123')}

### Q4. 다른 분야의 실제 인용: 구조 차용1건, 외부 자료 인용0건
"""]
    out.append(table(["계열", "전체 본문 gold", "다른 분야 구조/원리", "외부 다른 분야 자료 인용", "형태·전제"], [[f["family"], f["gold_denominator"], pct(len(f["crossfield_structural_items"]), f["gold_denominator"]), f"0/{f['gold_denominator']}", "능동태의 역할→Event 필드, 사람용이라는 거절 전제" if f["crossfield_structural_items"] else "선정된 비교절에서 해당 항목 확인 없음"] for f in ag["families"]]))
    out += [f"""
전체 **1/176(0.57%)**, 사례 기준1/31(3.23%)다. C05는 능동태의 행위 주체와 목적어 관계를 Event 데이터 필드에 대응한다. 가져온 것은 구조이며 단순 문구 장식으로 보기는 어렵다. 그러나 원문은 사람용 소비를 이유로 거절하고 외부 언어학 문헌을 인용하지 않는다. 같은 원문의 자동 분석 목표와 이 거절 이유에는 긴장이 있어 그 이유의 진실성까지 gold로 보증하지 않는다. 원리 도입 효과를 확인한 채택 사례는0건이며 A/B 모두 이 구조를 찾지 못해 다른 분야 항목 역사 적중은 각각0/1이다. {link('C05 고정판', c05['url'])}; {src('RV-C05-ACTIVE-VOICE')}

C22 리뷰의 Atom/Clojure 비교는 이름의 직관을 빌린 `term_only`이며 Rust trait에 Clojure 상태 관리 구조를 이전하는 제안이 아니다. 다른 언어 API, lens 같은 언어 설계 내부 개념, 표준문서의 출판 형식도 먼 분야로 자동 올리지 않았다. 이 구분을 넓히면 다른 분야 빈도가 커질 수 있지만, 여기서는 기능·객체·실패모드의 관계를 실제로 옮겼는지를 기준으로 한다. {src('RV-R123-TERM')}; {src('PS-R-S21-LENS')}

이 낮은 수는 ‘설계자는 다른 분야를 원하지 않는다’거나 ‘그 전이가 효과 없다’는 추정이 아니다. 비교 항목3개 이상과 번호순 선별 때문에 내부 대안이 많은 오래된 문서가 들어왔고 Rust8개는 모두 명시 Prior art 절 도입 전2014년이다. 기록된 인용의 선택성과 실제 효용의 차이는 학술 인용 추천에서도 확인된다. {src('R-TEMPLATE-PRIOR-MERGE')}; {src('M12')}

### Q5. 기준선 A: 전31사례의 실제 실행, 역사 적중16/176

각 접두부에 새 내부 문맥으로 웹 검색과 로그인 없는 공개 코드 검색을 시도했다. 원 응답204후보, 질의326개, 보수적 열람 비용561개를 남겼다. 사례별 상한은 질의12·문서20·후보15이고 실제 최대 후보는9개다. 공개 코드 검색 endpoint에서 HTTP200을 확인한 run은14/31이며 나머지17/31은 접근 실패·차단과 웹에 색인된 코드 fallback을 보존한다. HTTP200은 해당 후보가 모두 코드 검색으로 발견됐다는 뜻이 아니다. {own('RUN_AUDIT','evidence/RUN_AUDIT.json')}; {own('C03 A 실행 예','runs/A/C03.json',RUN_COMMIT)}

역사 적중은 **16/176(9.1%)**, 날짜 무관 일치는 **23/176(13.1%)**다. 다른 후보가 같은 항목을 회수한 중복을 제거한 수다. 후보의 날짜 판정은 pre103·post22·unknown79/204이며, post 일치2와 unknown 일치7에는 이미 다른 후보가 역사 적중한 항목이 일부 중복된다. Qt archive의 copyright, GHC 검색 메타데이터, 프로젝트의 최초 존재만으로 정확한 검증 본문을 과거 판으로 인정하지 않았다. {own('집계','evidence/AGGREGATES.json')}; {own('날짜 정정','evidence/judging-recovery/c21-c31/correction.json')}

구체적 성공은 C09의 Python range/xrange, C18의 Python bytes, C20의 L20n, C24의 Scala constructor, C31의 Distutils 비교기다. 반면 CPython의 특정 과거 패치를 PyPy type cache의 비슷한 원리와 같게 세지 않았고, C13의 interpreter-aware multiprocessing 제안을 기존 connection primitive와 같게 세지 않았다. 목적에 도움이 되는 후보 찾기와 저자의 모든 대안 복원은 다른 작업이었다. {own('C09 A','runs/A/C09.json',RUN_COMMIT)}; {own('C12 A','runs/A/C12.json',RUN_COMMIT)}; {own('C13 A','runs/A/C13.json',RUN_COMMIT)}

### Q6. 기준선 B: 목록·카탈로그에서 전31사례 실행, 역사 적중5/176

009의 기존 도구 범주에서 허용한 awesome 목록, AlternativeTo 계열, EIP, Azure 및 패턴 카탈로그를 발견 경로로 사용하고 연결 원문은 검증에 사용했다. A의 응답이나 gold를 준 사람 번역이 아니라 별도 내부 문맥의 모델 번역이다. 후보마다 `discovery_catalogue_url`와 실제 열린 목록 행이 있다. 31run·138후보·176질의, 원장698열람 행과 실패/find를 포함한 보수 비용703을 확인했다. 사례별 최대25페이지·531초로 B의25페이지 또는20분 조건을 충족한다. B에는 질의12회 상한이 없으므로 C31의17질의는 위반이 아니다. {own('RUN_AUDIT','evidence/RUN_AUDIT.json')}; {own('C05 B','runs/B/C05.json',RUN_COMMIT)}

역사 적중은 **5/176(2.8%)**, 날짜 무관 일치는 **14/176(8.0%)**다. pre37·post34·unknown67/138후보로 날짜가 밝혀지지 않은 live catalog 연결이 많았다. EIP의 원래 패턴은2003년 저자 서지로 확인했지만 페이지에 나중에 추가된 구현 예시까지 과거로 소급하지 않았다. 카탈로그는 일반 재사용 메커니즘을 찾는 데 자료를 주지만, 프로젝트 고유의 명명·구문·기각된 API 변형을 그대로 복원하는 성격과 거리가 있었다. {own('집계','evidence/AGGREGATES.json')}; {own('C22 B','runs/B/C22.json',RUN_COMMIT)}; {own('C31 B','runs/B/C31.json',RUN_COMMIT)}

### Q7. 채점: 적중·부분 참고·미해결 조건·링크를 분리했다

AF004의 L/E/H/T와 네 라벨을 그대로 썼다. A는 DIRECT_DOCUMENTED2·CONDITIONAL_TRANSFER192·INSUFFICIENT10/204, B는1·126·11/138이다. 확정한 제약 위반 라벨은0이다. 342행 모두 문서 기반 판정이며 runtime_observation은 not_performed다. 78행(A53/B25)은 원 응답이 한정한 참고 범위 밖의 제약이 하나 이상 있고, 모든 H를 범위 밖으로 처리한 행은0이다. 이런 행을 ‘전체 요구조건을 만족한 완성품’으로 해석하면 안 된다. {own('JUDGMENTS','JUDGMENTS.json')}; [AF004 PROTOCOL](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/PROTOCOL.md)

정답 밖 후보 분모는 A178·B120행이며 유용성 문서 조건 통과는 **A170/178(31사례), B109/120(30사례)**다. 결정 전 자료로 확인된 것은 A83·B30이고, 전체 gold 분자에 더하지 않는다. 이는 알려진 부품, 이미 일반적인 설계 원리, 선택안의 구현 참고도 포함한다. ‘새로운 대안279개’나 ‘더 좋은 해법279개’라는 뜻이 아니다. 거의 모든 유용 판정이 조건부 전이이므로 이 수의 가장 강한 의미는 **본문 대안 절이 참고 가능한 자료 전체를 열거하지 않는다**는 것이다. 더 나은 최종 설계를 만들었다는 직접 적용 증거는0건이다. {own('집계','evidence/AGGREGATES.json')}; {src('M03')}; {src('M12')}

반증 점검은 실제 판정을 바꿨다. C03 A4의 nsenter primitive를 node tool lifecycle 대안 전체의 적중으로 세지 않았고, C30 A3의 NSString initializer를 bridge 성능 개선 대안과 같게 세지 않았다. C05 B3에서는 실패 위험을 설명한 것과 해결 grouping equality를 제시한 것을 분리해 H unknown/INSUFFICIENT로 낮췄다. C13 B1의 clean README는 실제 값·수명 경계를 입증하지 않아 보류했다. 좁은 참고에 전체 제품 제약을 덮어씌워 오답을 늘리지도 않았다. {own('작업자 조정','evidence/judging-recovery/ROOT_ADJUDICATIONS.json')}; {own('내부 교차검토','evidence/judging-recovery/c11-c20/CROSS_REVIEW.json')}

모든 반환 URL과 원 열람 기록을 대조했다. 정확 URL 차이5행은 anchor, 공식 alternate path, slash, redirect 및 metadata-only 상태로 구분했다. 404·410 또는 확실히 다른 대상인 반환 링크는0/342이며 도구403·timeout은 가짜 증거로 쓰지 않았다. C30 A3는 URL이 존재해도 본문 근거 부족이므로 E supported로 올리지 않는다. 링크 존재와 답변 지지, 모델이 실제로 그 자료에 의존한 인과 관계는 서로 다르다. {own('URL 감사','evidence/RUN_AUDIT.json')}; {src('M13')}; {src('M14')}

### Q8. AF009의 반대 가설 A/B는 이번 결과만으로 기각되지 않는다

AF009의 반대 가설 A/B는 기존 조합 또는 구조화한 기존 조합이면 충분하다는 설명이다. 그 절의 기각 조건은 기존 조합이 새 절차와 동등 이상이면 H1 또는 새 조사 UI의 추가 가치를 기각하는 방향이며, 충분성 가설 자체를 기각한다는 뜻이 아니다. 이를 점검하려면 기존 조합과 **새 절차**를 같은 입력·예산·평가 기준에서 비교해야 한다. 이번에는 새 절차가 없다. ‘이 표본에서 모든 문서 항목을 복원한다’는 강한 해석은 낮은 회수율과 맞지 않지만, ‘설계자에게 충분히 유용한 참고를 준다’는 가설은 recall 하나로 반박할 수 없다. 반대로 정답 밖 후보의 조건부 참고 가치가 높다고 충분성이 입증된 것도 아니다. [AF009 GAP](""" + gap + f"""); {own('집계','evidence/AGGREGATES.json')}; {src('M03')}

다른 분야 항목은 한 개뿐이며 A/B 모두0/1이다. 이 관측은 해당 능동태 대응을 놓쳤다는 사례 수준의 사실이다. 새 제품이 그 한 항목을 찾았다는 비교, 설계자의 채택·오류 감소·시간 절감은 없으므로 차별점 증거로 삼을 수 없다. 외부 실체 항목의 A 역사 적중8/30과 구조 대안의8/146처럼 사례 유형별로 해석을 좁혀야 한다. 유지·갱신 가치 H2는 이번 설계에서 평가하지 않았다. {own('CASES','cases/CASES.json')}; {own('종류별 집계','evidence/AGGREGATES.json')}; {src('M15')}

## §3 추가 분석

### 3.1 계열·정답 종류·시간·노출을 나눈 관측
"""]
    out.append(table(["계열", "사례 / gold", "A 역사 / 날짜 무관", "B 역사 / 날짜 무관"], [[f["family"], f"{f['cases']} / {f['gold_denominator']}", f"{f['A']['strict_historical_hits']} / {f['A']['all_matches_hits']}", f"{f['B']['strict_historical_hits']} / {f['B']['all_matches_hits']}"] for f in ag["families"]]))
    out += ["\n"]
    out.append(table(["정답 종류", "분모", "A 역사 적중", "B 역사 적중", "A/B 날짜 무관"], [[r["kind"], r["gold_denominator"], pct(r["A"]["strict_historical"], r["gold_denominator"]), pct(r["B"]["strict_historical"], r["gold_denominator"]), f"{r['A']['all_matches']} / {r['B']['all_matches']}"] for r in ag["gold_types"]]))
    out += [f"""
두 기준선의 합집합은 역사17/176(9.7%), 날짜 무관29/176(16.5%)다. 이것은 두 개의 별도 예산을 합한 사후 분석이며 단일 같은 비용의 새로운 baseline 실행이 아니다. 역할 분류와 종류 분류는 다른 축이므로 같은 분야 설계146과 structural_design146의 숫자가 같아도 동일 집합이 아니다. {own('집계','evidence/AGGREGATES.json')}

노출 기록이 하나도 없는 보수 부분집합은 A18사례·93gold에서8/93(8.6%), B13사례·60gold에서1/60(1.7%)다. 서로 다른 사례 집합이므로 이 비율 차이를 누설의 인과 효과로 읽지 않는다. 전체 노출 run13/31와18/31도 실제 답 누설 빈도로 읽지 않는다. 여기서 통제한 것은 실행 입력과 반환 후보의 제외이며 모델 기억은 남는다. {own('집계의 no_recorded_exposure_subset','evidence/AGGREGATES.json')}; {src('M02')}

경계 일치의 민감도도 남겼다. C03 A4와 C30 A3의 넓은 component 해석을 다시 허용하면 A 날짜 무관 일치는23→25가 되지만 역사16은 변하지 않는다. C22 B1의 마지막 synthesis 이름을 개별 후보에 귀속하지 않으면 B 날짜 무관은14→13이며 역사5는 그대로다. 본표는 실제 사용 방식의 핵심 구조를 요구하는 판정이다. 관측을 유의성 검정·일반 성능 순위로 확대하지 않는다. {own('작업자 조정','evidence/judging-recovery/ROOT_ADJUDICATIONS.json')}; {src('M15')}

### 3.2 뒤집힌 결정의 이유를 결정 전 문맥으로 찾았는가

다음 표는 채택 뒤 대체/부분 번복6개를 모두 대조한다. 후속 정보는 baseline 입력에 없었고, 여기서의 대응은 사후 분석이다. 원 gold 분모에는 후속 항목을 더하지 않는다.
"""]
    out.append(table(["사례 / 후속", "실제 변경 범위와 이유", "기준선 원 응답의 관측", "판정과 확인 범위"], [
        ["C07 / PEP201 자체 수정", "무인수 zip을 TypeError에서 빈 결과로 바꿔 전치·역변환의 빈 레코드를 처리", "A5/B4후보에 zip(*[])·무인수 기저 사례 제안 없음", "해당 이유 회수0/9. Haskell의 고정2인수 중 빈 리스트와 구별. [고정 후속](" + cases[6]["superseded_by"][0]["url"] + ")"],
        ["C12 / PEP699", "3.11이 다른 guard를 사용하여 dict version 명세를 철회; 필드 재활용 가능", "A2 SELF의 write-triggered invalidation은 결정 전; JSC/Truffle 후보는 사후", "후속 관련 원리 단서는 있으나 실제 3.11의 필요 변화·명세 철회 이유 예측은 없음. [후속 대조](evidence/judging-recovery/c11-c20/Q8_SUCCESSORS.json)"],
        ["C14 / PEP649", "문자열화를 계산 함수·descriptor 지연 평가로 교체; 예전 lambda 기각 재검토", "A SQLAlchemy/SRFI45/Angular가 callback·promise 원리를 결정 전에 제시", "Python class/function-local scope와 descriptor 연결까지 찾지 못함. gold G01 적중 및 완성 후속 설계로 확대하지 않음. [후속 대조](evidence/judging-recovery/c11-c20/Q8_SUCCESSORS.json)"],
        ["C21 / RFC231", "explicit capture/receiver annotation을 추론으로 완화", "A의 per-variable capture는 원 대안 적중, B의 reference-default 관련 예는 사후", "capture/receiver inference 개선 이유 전체의 역사 회수 없음. [대조](evidence/judging-recovery/c21-c31/REVERSAL_NOTES.md)"],
        ["C29 / SE0169", "같은 파일·같은 타입의 extensions에 private 접근 공유", "A4는2006 C# partial declarations가 같은 타입의 선언 조각 사이에 private 권한을 공유함을 실제 제시", "결정 전 부분 메커니즘을 찾은 구체 사례. Swift same-file 경계와 실제 채택 효과는 미검증. [원 응답](" + REPO+RUN_COMMIT+"/"+P+"runs/A/C29.json)"],
        ["C31 / PEP440", "epoch·local identifier·개발 버전 순서 등 확장", "A Debian/RPM 후보에 epoch가 있으나 실제 열린 판 날짜 unknown", "후속 관련 요소는 있으나 당시 자료 확인과 특정 바뀐 순서의 회수 없음. [대조](evidence/judging-recovery/c21-c31/REVERSAL_NOTES.md)"],
    ]))
    out += [f"""
C29는 ‘원 gold 미적중이 곧 유용한 선례 없음’이라는 주장에 대한 구체 반례다. 다만 기준선이 미래 결정을 예측했다거나 원 설계자가 보았다면 결정을 바꾸었을 것이라는 인과 주장은 하지 않는다. C11의 PEP446·C13의 PEP734는 추가로 비교했으나 초안 교체이며 위6개 분모에 섞지 않았다. {own('C29 A','runs/A/C29.json',RUN_COMMIT)}; [초안 후속 대조](evidence/judging-recovery/c11-c20/Q8_SUCCESSORS.json)

### 3.3 다른 분야 세 가지의 독립 정답원과 알려진 편향
"""]
    out.append(table(["분야 / 원문", "독립 정답·평가 단위", "확인한 편향 및 반례", "이 조사에 적용한 판단"], [
        ["특허 — " + src("M05") + ", " + src("M07") + ", " + src("M06"), "CLEF-IP의 출원인/심사관 인용; NTCIR의 심사관 인용+전문가 검색+시스템 풀", "심사관의 목적·검색 종료와 최종 명세서 수정. CLEF 전문가7명/12주제 상위20 비교 및 인용34건 중13건 비관련 판정. NTCIR34주제는111run 중30개 pool을 보완", "최종 입력도 누설 가능. 문서 인용과 모든 관련 자료를 동일시하지 않으며 정답 밖 후보는 별도 판단. 법적 무효 요건을 L/E/H/T로 가져오지 않음"],
        ["법률 — " + src("M09") + ", " + src("M10"), "판결에서 noticed된 판례 검색과 문단 함의 과제를 분리", "명시 인용을 FRAGMENT_SUPPRESSED로 제거. 인용되지 않은 모든 관련 판례를 판정했다는 보장은 없음", "제안 번호·항목명을 접두부에서 제거. 입력 가림과 모델 기억 통제는 구별. 법률 자료의 편향 크기를 설계 corpus에 전용하지 않음"],
        ["학술 — " + src("M11") + ", " + src("M12"), "저자가 실제 넣은 참고문헌의 재추천", "자기 인용·친숙함·인지도·접근성·분량 선택. 검토된 지역 추천15/17이 실제 인용 재현 평가", "관측 선택 재현과 이상적 추천을 분리. 유용한 미인용 후보·실제 설계 효과를 gold recall에 섞지 않음"],
    ]))
    out += [f"""
정답 불완전성에 대한 문헌 반례가 평가 무용론을 뜻하지는 않는다. M01은 미판정의 처리 방식, M04는 풀 밖 결과와 공통 주제의 추가 판정 필요를 설명하며 M16은 조사 조건에서 예상한 일부 강화 편향이 발생하지 않았다는 반례를 제공한다. 이 연구는 bpref나 특허의 관련성 등급으로 AF004 축을 대체하지 않았다. 상세 원문 비교·읽은 절·한계는 [CROSSFIELD.md](evidence/methods/CROSSFIELD.md)에 있다. {src('M01')}; {src('M04')}; {src('M16')}

### 3.4 다섯 관점과 다섯 반례 탐색
"""]
    out.append(table(["관점", "이번 자료에서 필요한 판단", "직접 근거와 남은 확인"], [
        ["설계자", "목적·제약에 도움이 되는 부품과 완성 설계를 구별", "C29 partial type, C14 deferred computation. 실제 설계 수정·선택 효과는 적용 평가 필요"],
        ["리뷰어", "누락 대안·거절 이유·수정 시점을 확인", "C22/28 review pool, PEP642 수정 이력. 169개 항목의 review-added 시점은 추가 diff/토론 복원 필요"],
        ["기준선 사용자", "예산 내 검증한 후보와 사후 자료·접근 차단을 구별", "62개 run의 원 응답·502개 질의. 코드 검색 차단17/31과 현재판 날짜를 감안"],
        ["정보검색 평가 연구자", "불완전 정답·pool 편향·반복 변동을 분리", "M01/M04/M15/M16, gold 밖 후보 별도 분모. 단회 결과의 유의성·일반화는 미평가"],
        ["특허 선행기술 조사자", "시점 이전 문헌과 충분한 관계 증거를 확보", "M05–08의 최종 명세서·검색 종료·복합 근거. exact historical edition과 현재 설명을 구분"],
    ]))
    out += ["\n"]
    out.append(table(["찾아야 한 반례", "실제 탐색 기록·입력", "관측 결과", "미확인과 다음 확인"], [
        ["형식적·빈 선행 사례 절", "번호순 전체 비교절 검사, K-Q1–4 및 selection 원장; 직접 KEP177 재열람", "빈 template4개, 제목 누락 RFC85 복구. 절 존재≠충실한 gold", "미확인(제외 문서의 전체 토론을 읽어 문서 밖 대안 복원)"],
        ["gold에 없는 더 나은 선례", "A/B 모든 원 질의·178/120 nongold 후보의 L/E/H/T, C29 후속 대조", "문서상 부분 참고 A170/B109. C29는 후속 방향과 대응. 실제 더 나음 확인0", "미확인(동일 문제에 적용하여 설계자 판단·오류·시간 비교)"],
        ["뒤집은 이유의 사전 회수", "C07/12/14/21/29/31 원 응답 전체와 고정 후속 대조; REVERSAL/Q8_SUCCESSORS 파일", "C29 부분 메커니즘, C12/14 부분 원리. C07 핵심 무인수 이유0/9", "미확인(당시 자료판·실제 채택 효과 또는 사용자 반응 확인)"],
        ["가짜·다른 대상 링크", "342후보 URL↔opened_documents 비교; 차이5행의 정확 URL/redirect 추가열람", "확정 가짜0; metadata-only C30 A3는 근거 부족. 실패 URL은 별도 excluded", "미확인(재열람으로 현재 가용성, 당시 archive로 역사 가용성 확인)"],
        ["다른 분야의 실질 사용 대 장식", "C05 active voice 원문, RFC123 Atom 리뷰, lens/selector 경계 원문", "구조를 옮긴 거절 대안1; 용어 비유1은 review-only. 실효과 확인한 채택0", "미확인(현대 Prior art 절과 설계 변경 diff를 층화 표집하여 채택 관계 확인)"],
    ]))
    out += [f"""
문자열을 새로 만들어 실행한 것처럼 쓰지 않았다. 실제 검색어·URL 탐색·실패는 [SEARCH_LOG.json](SEARCH_LOG.json)의 원장 사본과 원 위치에 있다. D0 snippet·열람 실패·메타데이터만 읽은 자료는 최소 본문 자료 수에서 제외한다. {src('RV-K177-EMPTY')}; {src('RV-R123-TERM')}; {own('판정','JUDGMENTS.json')}

## §4 가장 중요한 불일치·약점 3건과 다음 조사 제안

### 1. 독립 문서 gold와 검색해야 할 외부 선례의 단위가 크게 다르다

**무엇이 어긋나거나 약한가:** gold176개 중146개는 구조 대안이며 완성품 역할은0개다. Rust8개는 모두 명시 Prior art 절 도입 전이다. 3개 이상 비교 항목을 가진 문서만 번호순으로 골라 내부 명명·구문 선택을 과대표집했다. 이것이 낮은 recall의 큰 대안 설명이다.

**근거 위치:** §2 Q2–Q4, §3.1 종류별 표, CASES.match_kind와 coding_revisions, TEMPLATES, SAMPLING. **이것이 틀리면 바뀌는 결론:** 현대의 명시적 외부 선례가 많은 문서에서도 같은 결과라면 외부 탐색의 누락 근거가 강해진다. 현재 결과만으로는 완성품·패턴 검색 제품 전반의 부족을 말할 수 없다.

**다음 조사 제안:** “명시 Prior art 절 도입 이후의 외부 실체 중심 문서에서도 누락이 유지되는가?” 필요한 자료는2018년 이후 Rust RFC·최근 PEP/KEP/Swift의 결정 전 판과 review diff다. 최소 **4계열×6사례=24사례**, 외부 실체 항목이3개 이상인 층과 내부 구조 대안 층을 각각12개 확보하고 별도 분모로 실행한다. 범위를 미리 고정하며 이번 표본을 결과에 맞춰 교체하지 않는다.

### 2. 현재 웹에서의 역사 평가와 충분한 기존 도구 조합의 실행 조건이 다르다

**무엇이 어긋나거나 약한가:** pre/post/unknown이 A103/22/79, B37/34/67로 갈리고 native code endpoint 성공은14/31뿐이다. 노출 기록과 사전학습 기억, 서로 다른 find 계수 방식도 남는다. 현재의 낮은 엄격 역사 적중은 탐색 실패와 과거 판 증명 실패를 함께 담는다.

**근거 위치:** §2 Q5–Q6, §3.1의 날짜·노출 민감도, RUN_AUDIT의 charge 보정, 각 run의 queries/opened_documents/date_evidence. **이것이 틀리면 바뀌는 결론:** cutoff 이전 판을 확보하면 일부 unknown 적중이 역사 적중으로 이동할 수 있다. 코드 접근이 정상인 동등 조합에서 결과가 달라지면 현 환경의 순위를 도구 일반 성능으로 설명할 수 없다.

**다음 조사 제안:** “같은 목적 입력에서 접근 가능한 코드 검색과 고정 역사 corpus가 있을 때 recall과 오류가 얼마나 바뀌는가?” 필요한 자료는 날짜 unknown 후보의 과거 release/commit·웹 archive 및 검색 서비스 접근 기록이다. 최소 **12사례(계열별3)×3반복**, 원 예산을 유지하고 현재 웹군과 판 고정군을 분리한다. 검색 시작 전에 미래 자료·노출 처리와 반복 비교 방법을 고정한다.

### 3. 낮은 gold recall과 높은 조건부 참고 수 사이에는 실제 효용 검증의 공백이 있다

**무엇이 어긋나거나 약한가:** 318/342가 CONDITIONAL_TRANSFER이고 원 답변의 부분 참고를 평가했다. C05 B3처럼 실패조건을 적었다는 이유로 필요한 연결을 확인한 것으로 올릴 위험이 실제로 발생했다. 다른 분야 항목1개와 C29의 부분 반례만으로 제품 차별점이나 수요를 증명할 수 없다. AF009의 새 절차 비교 조건도 아직 없다.

**근거 위치:** §2 Q7–Q8, JUDGMENTS의 H_assessment_scope/remaining_check, ROOT_ADJUDICATIONS, C29 원 응답, M03/M12. **이것이 틀리면 바뀌는 결론:** 정답 밖 조건부 후보를 실제로 적용해도 설계·오류·시간이 개선되지 않으면 ‘참고 가능한 자료의 불완전성’ 이상의 효용 주장은 사라진다. 반대로 새 절차가 같은 비용에서 일관되게 개선하면 그때 추가 가치 근거가 생긴다.

**다음 조사 제안:** “원 gold 회수와 정답 밖 조건부 후보 중 어느 것이 실제 설계 판단을 개선하는가?” 필요한 자료는 최소 **12개 실제 설계 과제**, 원문/새 후보의 가림 조건, 문제별 적용 patch 또는 판단 기록, 사전 정의한 위반·미확인·시간 기준이다. 가능하면 설계자·리뷰어2인 이상이 각 과제를 비교한다. 다른 분야 관계 전이가 명시된 과제4개 이상을 의도 층으로 두되 별도 분모로 보고한다. 기존 A/B와 새 절차를 같은 예산에서 비교하기 전 우위 주장을 하지 않는다.

## §5 한계

1. **모집단과 사이트 상한:** 이 결과는 네 공개 프로젝트 계열의 조건부 목적 표본이다. 사례31개의 고정 원문은 모두 GitHub 계열 호스트다. 최초 SAMPLING에서 사이트당3개 상한을 비사례 최소수에 적용하고 사례는 독립 프로젝트의 제안서 단위로 센 해석을 명시했다. 비사례25개는13사이트·최대3개로 충족한다. 상한을 사례 원문에도 문자 그대로 적용하면 사례 최소30 조건은 충족하지 못하며, 이 해석의 채택 여부를 무조건 충족으로 숨기지 않는다.
2. **독립성의 범위:** 저자·리뷰어가 기록한 원천은 연구자와 독립돼 있으나 항목 분절·역할·일치·조건부 유용성은 같은 모델 계열의 작업자/내부 검토 코딩이다. 경계36행 교차검토는 분류 신뢰도 연구나 전수 복수 독립 모델 평가가 아니다.
3. **입력과 시간:** 연구자가 요약한 접두부이며 실제 당시 사용자의 자연 질의를 수집한 것이 아니다. C31 선정 오류 보정, 수락일과 상태 반영일 차이, 일부 과거 merge object 접근 실패를 원장에 남겼다. 새 내부 문맥은 학습 기억이나 웹 snippet 노출을 제거하지 못한다.
4. **실행·예산:** 한 사례당 한 번의 A/B 실행이다. B는 사람 번역이 아니라 모델 번역이며 코드 검색 접근 실패·페이지별 차단이 있다. 성공·실패·find를 세는 방식이 완전히 같지 않아 전체 elapsed 합계로 속도 우위를 비교하지 않는다. 원 run들은 이전 커밋에 있었고 이번 재개에서는 이를 다시 검색하지 않고 판정·감사했다.
5. **효용과 미확인:** 모든 판정은 공개 문서 관계이며 D4 실제 적용, 사용자 반응, 설계 변경 성공, 비용 절감, 유지·갱신 우위는 측정하지 않았다. ‘더 좋은 선례’ 확인0은 실제로 존재하지 않는다는 증거가 아니다. 표의 날짜·필수 연결 미확인은 각 remaining_check의 원문/판/구현 검사로 해소해야 한다.
6. **자료 기록:** 직접 읽은 절·URL·판·요약·한계를 보존했고 공개 본문 전문·프로필을 저장하지 않았다. 시각 일부는 읽기 묶음 완료 시각이다. 재열람·이관된 같은 내용·D0·실패는 최소 자료 수를 늘리지 않는다. 원 저자 연구의 수치를 이 기준선의 효과량으로 바꾸지 않았다.

작성·판정 자료의 기준 커밋은 `{JUDGE_COMMIT}`이며, 원 실행 보존 커밋은 `{RUN_COMMIT}`다. 재계산 명령은 `python docs/workstreams/research/AF-RES-013/tools/analyze_results.py`, 표 재생성은 `python docs/workstreams/research/AF-RES-013/tools/render_result.py`다. JSON 숫자가 기준이며 표·서술이 이를 요약한다.
"""]
    (ROOT / "RESULT.md").write_text("\n\n".join(out).replace("\n\n\n", "\n\n").rstrip() + "\n")
    print(json.dumps({"file":"RESULT.md", "bytes":(ROOT/'RESULT.md').stat().st_size, "table1_rows":len(cases), "table2_rows":len(ROLES), "section4_entries":3}))


if __name__ == "__main__":
    main()
