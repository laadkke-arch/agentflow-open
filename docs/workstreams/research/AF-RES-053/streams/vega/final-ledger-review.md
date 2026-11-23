# 최종 원장 교차 검토

검토자: `/root/vega_frame`. 검토 완료 시각: **2026-11-23T02:14:28.003878Z**. 이 검토는 같은 모델의 보조 작업자가 수행한 교차 검토다. 검토자는 Vega 모집틀·수신 문헌·후속 원장 작성에도 참여했다. **독립 사람 검토, 블라인드 평가, 독립 모델 검토로 표시하지 않는다.**

범위는 `outcomes.csv`, `evidence/comparison-counts.json`, `evidence/source-counts.json`, `assemble_sources.py`, `assemble_outcomes.py`와 frozen `predictions.csv`·`cards.csv`의 대응이다. 필요한 내부 근거로 각 stream의 원장, `sources.jsonl`, `replay/results.json`, 기존 봉인 영수증을 읽었다. 새 외부 자료를 열거나 renderer를 새로 실행하지 않았다. 이 파일과 검토용 비커밋 cache 외에는 쓰지 않았다. 아래 수정은 검토 의견을 받은 **root가** 수행했으며, 검토자가 공통 원장을 직접 수정하지 않았다.

## 1. 결론

마지막 재생성본을 대상으로 한 원장 대응·수량 검산은 **통과**했다. 필수 배당은 여전히 미충족이다. 이 둘을 구분해야 한다.

| 검토 축 | 확인 결과 | 의미와 제한 |
| --- | --- | --- |
| 전체 기록 | 188행, source_id 188개 | 실패·metadata·재열람을 포함한 기록 수다. 188개 원전을 뜻하지 않는다. |
| 최소수 적격 행 | 141행 | 동일 저작의 여러 위치가 포함되며 고유 저작 수와 다르다. |
| 보수적 고유 저작 | 71개 | 초기 72개에서 pointer-only #7372를 제외했다. 기존 원장·분류 규칙을 재계산한 수이며, 이 검토에서 외부 원문 71개를 다시 읽은 것은 아니다. |
| 필수 배당 | 요청자 5/6; 수신 문헌 5/4; 인쇄·지도 4/4; 독립 후속 0/6; 경계 원전 2/2 | 수신 문헌의 초과분으로 요청자·후속 결손을 상쇄하지 않는다. |
| 예정·충원 요구 | 예정 6, 충원 5, 미충원 1 | L03은 실측 분모에서 제외된다. |
| 카드·예측·결과 행 | 각각 18행, ID 집합 동일 | 충원 15행과 미충원 자리 3행이다. 18개 독립 요구가 아니다. |
| 공개 자료 대조 | 논리 검토칸 20, 정확 조건의 새 출력 완전 충족 관측 0 | 5요구 × normal/boundary × A/B. 20번 실제 실행을 뜻하지 않는다. |
| I 대 D | choice·normal·boundary 모두 같은 요구 5/5 | 사전 예측 동일성이며 공개 실측 정답 동률은 미확인이다. |
| 보조 재생 | 2요구, 보기 대응 6행, variant 실행 6회, SVG 5개, compile failure 1개 | 공개 후속 원전·작성자 역사 실행과 분리되어 있다. 보기 6행과 실행 6회가 우연히 같은 수이며 같은 단위가 아니다. |

## 2. 발견 사항과 반영 확인

| 발견 사항 | 최초 근거 | root의 반영 | 마지막 확인 |
| --- | --- | --- | --- |
| pointer-only #7372가 `substantive_work=true`로 최소수에 포함되어 총 72로 집계됨 | `sources.jsonl` VF07, 본문은 읽지 않은 PR #7222를 가리키는 한 문장; `streams/vega/cache/body-only.json`의 #7372 | frozen 원장 annotation은 유지하고 `assemble_sources.py`의 사후 보수적 제외 규칙을 추가 | 새 집계 71개·적격 141행. 제외 집합 차이는 #7372 한 저작이며 필수 배당은 변하지 않음 |
| 재생 `일치`와 `confirmed_I_D_ties=2`만 보면 V02 원래 정상 입력까지 검증된 것으로 읽힐 수 있음 | `replay/results.json` limits: V02 정상은 연구자 key-renaming 대조; V03은 한 출력의 정상9/경계1 부분집합 | `outcomes.csv`의 `replay_comparison`과 comparison-counts의 `tie_scope`에 적용 범위를 명시 | V02 세 행 모두 원작성자 정상 검증 제외, V03 세 행 모두 고정10행 부분집합이라는 문구 확인 |
| 비교 집계의 상당수가 상수여서 후속 원장이 바뀌어도 값이 남을 수 있음 | 최초 `assemble_outcomes.py`의 filled5/view18/public0/replay6·5·1/tie2 등 | 요구·보기·cell·replay status 및 I/D 비교 행에서 수량을 산출하도록 수정 | 같은 underlying 행을 별도로 계산해 5/18/20/0, 2/6/6/5/1, I/D 5/5와 일치함을 확인 |

초기 집계의 `assigned_unique_works=16`은 **배당에 사용된 고유 저작 16개**로서 맞다. 이를 `16/22`라는 충족률로 바꾸면 수신 문헌의 초과 1개가 결손을 덮게 된다. 배당별 표를 사용한다는 root의 방침과 일치한다. 각 배당의 필요 수로 cap한 산술 합은 15/22이지만, 이 수 역시 질문별 결손을 대신하지 않는다.

## 3. 중복 계보·배당 검토

`assemble_sources.py`는 같은 work_id의 재열람을 합치고, `vl-implementation → vl-official-manual`, `D-M02 → D-M01`을 추가 병합한다. 따라서 Vega API·구현의 여러 판과 QGIS User/Training 문헌이 각각 보수적인 하나의 계보에 들어간다. 같은 이슈의 댓글·그림·첨부·editor payload도 새 저작으로 늘리지 않는다.

71개 중 다수는 모집에서 제외한 이슈다. 선정 5요구의 요청자 배당과 독립 후속 배당에는 그런 이슈를 전용하지 않았다. 고유 총수 22개 이상이라는 조건이 충족되어도 요청자 5/6, 후속 0/6이 남아 `required_allocation_met=false`인 것이 맞다. 2020년 libass PR #384/#385는 L01 이전 배경 자료로 분리되어 후속 6건에 들어가지 않는다. 자체 재생 도구·라이브러리와 내부 선행 결과도 원전 최소수에서 제외된다.

각 배당 work_id는 적격 canonical 집합 안에 있고, 배당끼리 중복되지 않는다. 요청자 5개, 수신 5개, 도너 4개, 경계 2개의 합이 assigned 16개와 맞는다. 원문을 인용한 다른 저작을 열지 않고 그 저작까지 산입하는 오류는 이번 pointer-only 보수적 제외로 줄였다. 이 검토는 다른 stream의 모든 저작 독립성을 새 외부 조사로 재판정한 것은 아니다.

## 4. 분모와 판단의 분리

`outcomes.csv`는 같은 공개 관측을 N/I/D 세 행에 반복 연결한다. `logical_cells_reviewed`를 단순 합산하면 60이 되지만 올바른 요구별 중복 제거 결과는 **20**이다. assembler는 case 원장마다 한 번만 합산한다. L03의 세 빈 자리에는 논리칸 0, 미실시·미충원이 기입되어 있다.

동일한 이유로 I/D 예측동일 5/5를 15/15나 18/18로 바꾸면 안 된다. 충원된 다섯 요구에서 `choice`, `normal_prediction`, `boundary_prediction` 세 필드를 각각 비교했고 모두 동일했다. 서로 다른 I/D 예측의 조건부 분모가 0이므로 D의 새 정답 판정은 해당 없음이다. 공개 근거의 실제 동률은 미확인으로 유지한다.

보조 재생은 원래의 공개 관측 분모 20에 더하지 않는다. V02는 네 variant 시도 중 boundary B가 compile failure라서 SVG가 없고, V03은 fixed-A/B 두 실행에서 정상·경계 label 부분집합을 함께 본다. 따라서 재생 실행은 4+2=6회, SVG는 3+2=5개다. V03의 정상 라벨 9개를 실행 9회로 늘리지 않았고, V02의 4×4 subplot 16개도 별개의 요구나 A/B 실행 16회로 세지 않았다.

V02 boundary B의 실제 실패 방식은 compile error다. 봉인 예측은 값 접근 보존 실패를 범주적으로 예상했으므로 범주 선택 A만의 보조 일치는 가능하지만, 빈 SVG나 잘못된 점이 렌더된 것처럼 표현해서는 안 된다. 현재 `alternative_interpretation`에 이 차이가 남아 있다.

## 5. 사전봉인 보존과 검사 방법

기존 `outcome-retrieval-receipts.json`의 봉인 파일 hash와 현재 `predictions.csv`, `cards.csv`, `operations.json`, `evidence/operation-refinements.json`을 비교해 모두 같음을 확인했다. 18개 ID의 집합과 결과 `frozen_choice`도 원래 예측에 대응한다. 충원된 다섯 요구의 I/D 추가 단어 수·그림 수·예산 상한을 필드별 대조하여 모두 같음을 확인했다.

검산은 읽기 전용 Python으로 CSV/JSON을 파싱해 수행했다. assembler의 `main()`은 이 검토에서 실행하지 않았다. `assemble_sources.py`는 `runpy.run_path(..., run_name='ledger_review_only')`로 순수 분류 함수만 불러와 기존 원장에 적용했다. 공통 원장 재생성은 root가 수행했다. 별도 renderer 재실행이나 원문 재열람은 미실시다.

| 검토 대상 | 검토 완료 시 SHA256 |
| --- | --- |
| outcomes.csv | `fd06097e365dd43d64ce441dcf9172509c2d60e5e8854836e529bae9b29dc413` |
| evidence/comparison-counts.json | `82642438f2fe663b5c1e79b42795032e6f1276f2b9a52fe8bbbc3b5233ec61dd` |
| evidence/source-counts.json | `7e576a5deec014b2a66d7ac126f89d361dc7a32c9d4657a439a3f52023dc858c` |
| assemble_sources.py | `1b7d3b1be63603ac68962c7cde507f9817b3e12d5e30c00dbbe4ec024d1e6a7a` |
| assemble_outcomes.py | `b4e792fe5b98d179f3390384982d39ee577abf8f46f79c15971c00191b18d441` |
| predictions.csv | `d7e63a27513879e8691d7138efeb7c42c9245093e4bdc808a9e984f9a1e95db5` |
| cards.csv | `20ce5c7e01bc5fc8a2b1951262d3be6ce5e1e12c51566d2f3727bd2fcee5e7aa` |

이 시점의 원장 범위에서 해결되지 않은 산술·ID 대응 불일치는 발견하지 않았다. 연구 결손은 남아 있으며 특히 요청자 1자리, 독립 후속 6저작, 작성자 runtime과 같은 조건의 공개 출력이 미확보다. 결과 본문이나 HANDOFF 자체에 대한 검토는 이번 범위에 포함하지 않았다.
