# 공개 저자 입력에서 진단 집계 다시 만들기

## 실행한 범위

실행 주체: diagnostics assistant의 제공된 cloud workspace, Python 표준 라이브러리. 실제 명령·UTC·산출 행 수는 `execution.json`, 실제 읽은 입력 URL·바이트·SHA256은 `input-receipt.json`이다. 현재 고정판의 author raw data를 읽었고 새 참가자 모집, 실험 웹 앱 실행, 저자 R 모델 재적합은 하지 않았다. Bansal/Lai의 응답 원행을 저장소에 재게시하지 않는다.

저장소 루트에서 다음을 실행한다.

```bash
python -B docs/workstreams/research/AF-RES-058/streams/diagnostics/reproduce_diagnostics.py --download
```

`--download`는 고정 git SHA의 세 입력만 `_cache/inputs/`에 받는다. URL만 고정하는 데 그치지 않고 기대 SHA256을 확인한다. 캐시가 이미 있는 이번 실행에서는 `--download` 없이 같은 해시의 복제 저장소 파일을 읽었다. `_cache/`는 커밋하지 않는다. 산출물은 이 stream 안의 aggregate JSON이며 명령을 다시 실행하면 실제 실행 UTC와 파일을 갱신한다. 입력 취득이 실패하면 파일을 추정·대체하지 않고 종료한다.

| 입력 | 고정판 | SHA256 | 실제 용도 |
| --- | --- | --- | --- |
| Bansal decision-result-filter.csv | uw-hai/Complementary-Performance@6cebab4ffd2b332ebec5e27e7632e7bf1c36ba5f | 0cc48875d451e095db8307e7b2cf616d5ad2277e200c8d2579e07db174c1f9f0 | 원 저자 분석파일66040행, 원개수 집계·중복 감사 |
| Bansal decision-result-prefilter.csv | 같은 판 | 1074a05e0a4f113a1f8b8bfe8a887f455ad57dec5a4838fbe5357c85e3e84af6 | 68810행, 필터 전후 차이·키 포함관계 |
| Lai label.jsonlist.gz | vivlai/deception-machine-in-the-loop@7c5ae6bb4b7dcd5613e620e4731b9c3c67ed8285 | d3616e73d4db03d6e21f574246d318e7f0300facdfe6ff88aa2630cef8364c5f | 전체14400행, 조건별 분모·수락·최종 정답·콘텐츠 일관성 |

## 열·키·분모

Bansal: person=`assignmentId`, item order=`questionId`, task=`task`, condition=`condition`, recommendation=`pred`, truth=`y`, final=`choice`; 추가`pred2/conf/conf2/time`. README가 questionId를 문제 순번으로 정의하므로 자극 JSON의 id/testid와 멋대로 맞추지 않는다. 같은 응답 행 안의 값으로 A와C를 계산한다. 스크립트는 키 중복을 발견한 뒤 임의 first/last를 선택하지 않는다.

Lai: person=`anonymized_worker_id`, condition=`experiment`, trial order=`review_num`, recommendation=`predicted_label`, truth=`actual_label`, final=`user_label`, item content=`review_text`. 문자열 내용의 SHA256은 조건별 권고·참값의 일치 감사에만 사용한다. 공유키 없는 다른 파일과 연결하거나 새 participant key를 만들지 않는다. four no-prediction conditions의6400행은 predicted_label=`N.A.`이므로 정오별 권고 수락표에 넣지 않는다.

정오층 g와 조건 c에 대해 다음을 계산한다.

```text
D(c,g) = count(record where condition=c and (prediction=truth)==g)
A(c,g) = count(same records where final=prediction)
C(c,g) = count(same records where final=truth)
O(c,wrong) = count(same records where final!=prediction and final!=truth)
ΔA(g) = A(intervention,g)/D(intervention,g) - A(control,g)/D(control,g)
```

모든 분모는 공개 파일에서 판정 가능한 기록의 수다. 사람 단위 배정을 유지해 person key수를 별도 표기한다. 한 사람의20/50행을 독립 사람으로 세지 않는다. 추론 검정·새 신뢰구간을 만들지 않고 기술적 비율과 차이만 계산한다. Bansal Human 조건의 pred는 비제공 counterfactual prediction일 수 있으므로 수락A는 `null`이다.

## 수작업 검산

Lai machine / heatmap 각각 공개80명,20행이므로80×20=1600. 권고 정오 분모는1395+205=1600. 원행 집계A값은908/123 대1107/152다. 이진 과제이므로 final correct가908+205−123=990,1107+205−152=1160으로 계산된다. 각각61.875%,72.5%이며 저자 Fig3의61.9%,72.5%에 맞는다. 틀린 권고 수락123/205=60%,152/205=74.146…%는 Fig4의60%,74.1%에 맞는다. 정수는 원행에서 셌고 그림에서 역산하지 않았다.

최종 정확도차=(1160−990)/1600=10.625%p, 틀린 권고 수락차=(152−123)/205=14.146341…%p. 맞는 권고 수락차=(1107−908)/1395=14.265233…%p. 동일한1395/205 혼합비에서 평균과 오류 선별의 방향이 갈린다. `root` assistant가 별도 코드로 같은 네 셀과 전체 정답을 재확인했다고 보고했으며 실제 별도 코드/출력은 `../root/verify_lai_and_bounds.py`, `../root/independent-calculation.json`에서 확인한다. 이는 독립 인간 심사나 새 참가자 복제가 아니다.

LSAT Single: 총101명×20=2020, 권고정답101×13=1313, 권고오답101×7=707. 오권고 층의358 AI수락+300최종정답+49제3오답=707. 거절349와 정답300을 같게 놓을 수 없다. 비교 Conf.는102명×7=714,331+338+45=714. 이 두 조건에는 발견된 Beer 중복키가 없다.

## 중복과 감도

주 기록 집계=`D01:author-filtered-records`66040행. 키 모호200개에 속하는400행을 모두 제외한 감도=`D01:unambiguous-key-subset`65640행. 감도는 모집단/사람 수가 달라진 다른 분석 집합이며 원배정 전체 추정이 아니다.400행이 모두 Beer에 있으므로 Amazon/LSAT의 분자·분모는 두 분석에서 같다. 실제 조건별 사람 key와분모는 outcome/audit JSON에서 다시 읽는다. ID가 충돌했는지 동일인이 반복했는지는 알 수 없으므로 중복의 정답 판정을 하지 않는다.

## 불가능한 칸과 필요한 다음 입력

| 칸 | 상태·이유 | 다음 최소 입력 |
| --- | --- | --- |
| 전체 배정 대비 결측 범위 | 미확인: 공개분석파일 내부 missing0은 모집·탈락 전체 missing0을 뜻하지 않음. 정오층별 사라진 D도 모름 | 사람·배정·screening/제외/중단과 item 연결표 |
| 권고를 보고 바꾼 비율 | D01/D04 미확인: preanswer가 없음 | same person/item preanswer와 final choice |
| 실제 설명 읽음의 효과 | 미확인: 설명 제공조건과 실제 reading을 분리할 로그 없음 | 사전 배정된 노출 방식, click/viewport/체류 로그와 원응답키 |
| D02 원분자/분모 | 미확인: Table2는 adjusted marginal mean, χ² N663은 풀된 수 | participant/block/condition/item/AI/truth/final 및 main/exploratory flag |
| D03 이산 정오·수락 | 원 종점 부재(J4): continuous prediction/loss, 합성 outlier actual_price=-1 | 별도 사전 이산 판정 프로토콜; 기존 자료에 사후기준을 붙여 본 과제 원결과로 보고하지 않음 |
| D05 정오층 switch/acceptance | 미확인: confidence bin별 그림, old/new cohort, assignment 미공개 | exp/cohort/person/item/condition/preanswer/pred/truth/final |

분모 m이 알려지지 않으므로 최대/최소 결측 범위를 수치로 제시하지 않았다. 그룹마다 읽음·이해·진정한 동의·권고로 인한 변경을 동일하게 취급하지 않는다. 저자 R 분석을 재실행하려면 Poursabzi 패키지 README의 `make`와 R 의존성이 필요하지만 이산 수락 질문을 새로 답하지 못하므로 본 조사에서 실행하지 않았다.
