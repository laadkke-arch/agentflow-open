# 그래프 두 구현 최종 대조 검토

검토자 `/root/graph_audit`, 기준 커밋 `672366cdf4542d4ca9f579963d66c2745f4316ed`. 이는 별도 에이전트의 소스·원장 검토이며 독립 인간 피험자 실험이 아니다. 기존 구현 실행과 예측은 반복하거나 변경하지 않았다. 새 직접 독해는 [graph-sources.jsonl](graph-sources.jsonl), 실패 경로는 [graph-search-log.jsonl](graph-search-log.jsonl), 기계 판정은 [graph-review.json](graph-review.json)에 있다. 여섯 재열람은 기존 두 구성요소 계보이므로 새 고유 저작은 **관측 0**이다.

## 판정

기존 그래프 결론은 기록된 범위에서 유지할 수 있다. D3 두 행은 같은 판의 **연구자 보조 실행**으로 방향·거리 제한을 확인했다. Graphviz 두 행은 지정 좌표와 한 단계 호출을 고정하는 공개 계약을 확보하지 못해 **미확인**이다. 동종 A가 없는 Graphviz 두 행은 동률로 세지 않는다. 그래프만의 A/B 가용 행은 2, 운영적 불일치는 **관측 0/2**, 유지 표본은 4, 같은 판·같은 입력의 독립 원출력 확보는 **관측 0/4**다. 불일치 행의 적중률은 **해당 없음**이다.

봉인 커밋 `02359364000057f69b00594d8b43571ac72df298`과 현재 checkout의 graph baseline, A 예측, D3/GV A 창 및 전체 predictions.csv 다섯 파일은 바이트 단위로 같다. 기존 실행 결과의 원장·파일 분리는 적절하다. 기존 release/tag/package 영수증을 검토했으며 새 release 선정이나 환경 인증을 수행한 것은 아니다.

## 필수 8행 표에 옮길 그래프 네 행

| 사례·판 | 용도·고정 입력 | 차용 경로와 달라진 가정 | API / A / B | 관측과 판정 |
|---|---|---|---|---|
| D3-N · d3-force 3.0.0 | 두 노드 (0,0),(3,4), strength −30, alpha 1, 직접 force 호출 1회 | [README Many-Body](https://github.com/d3/d3-force/blob/156712c8c3285d77cb487e1685c5adafcd0394a4/README.md#many-body)와 [manyBody.js 29–90](https://github.com/d3/d3-force/blob/156712c8c3285d77cb487e1685c5adafcd0394a4/src/manyBody.js#L29-L90): Barnes–Hut 명명·위키 링크는 확인, 원논문 직접 채택 이력은 미확인. 벡터는 `alpha*s*delta/r²`, 크기는 1/r이며 중력 크기 1/r²와 다르다. | 세 보기 모두 서로 멀어지는 방향; 정확한 정상 수치는 사전 보류. B 강의 창은 집계 알고리즘만 추가. | [기존 실행](../graph/d3-run.json) D3-N: Δv=(−3.6,−4.8),(3.6,4.8). 고정 소스 재열람 FG001과 일치. **연구자 보조 실행**, 독립 원출력 아님. |
| D3-B · d3-force 3.0.0 | 같은 두 노드, distanceMax 4, 실제 거리 5 | [manyBody_distanceMax](https://github.com/d3/d3-force/blob/156712c8c3285d77cb487e1685c5adafcd0394a4/README.md#manyBody_distanceMax)와 [apply](https://github.com/d3/d3-force/blob/156712c8c3285d77cb487e1685c5adafcd0394a4/src/manyBody.js#L55-L90): 유한 거리 제한은 수신 API의 결정. | API/A/B 모두 두 속도 0. B에 추가된 독립 적중으로 세지 않음. | 같은 [실행](../graph/d3-run.json) D3-B에서 0,0/0,0. 근사 집계·거리 경계 일반화는 별도 반례에서 깨짐. |
| GV-N · Graphviz 14.1.1 sfdp | a--b, 제안 좌표 (0,0),(3,4), K 1, 한 단계 요구 | [sfdp 공식 문서](https://graphviz.org/docs/layouts/sfdp/)→[Hu 원고 §3.1](https://yifanhu.net/PUB/graph_draw_small.pdf), 그 논문→Barnes–Hut. B는 동종 그래프 논문이다. [tuneControl 200–224](https://gitlab.com/graphviz/graphviz/-/blob/a74b50c20fc624f46f72e24f981b261f6e5edf71/lib/sfdpgen/sfdpinit.c#L200-224)에는 maxiter 매핑이 없고 공개 시작은 random이다. | API 미확인 / A 미확보 / B 실제 구현 미확인, 원식만 C에 따른 조건부 방향. | 공개 입력 대응에서 끊김. Native 실행 **미실시**, 실제 한 단계 **미확인**. 사후 비공개 제어의 손계산을 주행의 결과로 승격하지 않음. |
| GV-B · Graphviz 14.1.1 sfdp | 같은 그래프, 제안 좌표 두 개 모두 (0,0) | [normal embedding 567–660](https://gitlab.com/graphviz/graphviz/-/blob/a74b50c20fc624f46f72e24f981b261f6e5edf71/lib/sfdpgen/spring_electrical.c#L567-660): random 시작으로 입력이 바뀜; 최소 거리·정규화·종료·후처리는 논문만으로 고정 안 됨. | API 미확인 / A 미확보 / B 원식 r=0 특이성 설명만 가능, 제품 동작 보류. | 공개 시작·한 단계 계약이 없으므로 **미확인**. private random_start=false의 무이동 손계산은 별도 사후 보조 행. |

## 코드 대응에서 확인한 것과 수정할 것

FG001–FG004의 고정 소스 네 파일 해시는 기존 `streams/graph/source-receipts.json`과 일치했다. D3의 signed strength, 절댓값 가중 중심, theta 검사보다 먼저 일어나는 합 0인 quad의 가지치기, strict cutoff 및 최소 거리 보정은 기록된 식과 맞는다. Graphviz는 주석 대신 실행 본문의 `KP=K^(1-p)`, `CRK=C^((2-p)/3)/K`를 대응시킨 기존 설명이 맞다. `getPos`만 보면 좌표 입력을 유지하는 것처럼 보이지만 이후 random 시작을 추적한 결론도 지지된다.

**실제 링크 정정 1건.** 고정 D3 README 348행 제목은 `Many-Body`이므로 반환 주소의 절은 `#many-body`다. 기존 graph/findings.md와 transfer-notes.md 일부에 있는 `#many-body-forces`는 맞지 않는다. 봉인 predictions.csv의 `#many-body`는 이미 맞으며 바꾸지 않는다. README의 `Source` 링크는 master로 향하므로 결과 카드에는 위 고정 소스 링크를 따로 둔다. 근거 FG005.

**표현 한정 1건.** “순차 갱신이므로 뒤 노드는 앞 노드의 갱신 좌표를 본다”는 두 노드 direct-pair 보조 계산과 인접 끌림에는 맞는다. n≥45의 normal 경로는 정점 루프 전에 quadtree를 만든다. 따라서 모든 집계 중심이 매 정점 이동 뒤 다시 구성된다고 일반화하면 안 된다. 근거 FG002, spring_electrical.c 587–599, 615–627, 648행. 기존 두 노드 보조 계산은 이 한정의 영향을 받지 않는다.

## 반례와 반환 카드에 필요한 결정 조건

| 구현 | 유지할 반례·근거 | 첫 링크 | 선택을 바꿀 최소 입력 |
|---|---|---|---|
| D3 | 같은 위치 jitter의 운동량 비대칭, signed sum 0의 theta=0 가지치기, 근사 집계 중심의 거리 제한은 [보조 원장](../graph/observations.csv)과 [apply](https://github.com/d3/d3-force/blob/156712c8c3285d77cb487e1685c5adafcd0394a4/src/manyBody.js#L55-L90)에 남아 있다. “천체 중력 코드이므로 그대로 적용”을 반박한다. 각 출력은 자체 진단이다. | [고정 API Many-Body](https://github.com/d3/d3-force/blob/156712c8c3285d77cb487e1685c5adafcd0394a4/README.md#many-body), 필요 시 apply. 현재 주 입력은 옵션 의미와 직접 호출 구분으로 해결된다. | 실제 과제가 오차 상한·계산 비용을 요구한다면 입력 분포·오차 지표·허용 시간부터 받고 원전/수치 방법을 먼저 제시. 필터링이나 울타리 목적이면 해당 제품 예제·설계를 먼저 제시. 사용자가 실제 링크를 읽고 결정을 바꿨다는 기록은 여전히 필요하다. |
| Graphviz | [#2283](https://gitlab.com/graphviz/graphviz/-/issues/2283)의 beautify 중첩과 [#2560](https://gitlab.com/graphviz/graphviz/-/issues/2560)의 scale 후 동일 좌표 보고는 그래프 가독성이 원식 외 후처리에 달림을 보인다. 다른 판·입력이므로 주 두 행의 검증 자료가 아니다. | [고정 tuneControl](https://gitlab.com/graphviz/graphviz/-/blob/a74b50c20fc624f46f72e24f981b261f6e5edf71/lib/sfdpgen/sfdpinit.c#L200-224). 첫 문장에서 최종 읽기 좋은 배치인지 제어된 내부 힘인지 사용 목적을 확인하도록 안내. | 공식적인 실제 초기 좌표·한 단계 trace가 생기면 직접 검증 가능. 읽기 부담이 우선인 실제 그래프와 라벨·간격 조건이 생기면 overlap 사용법 먼저. 근사 오차/비용이 우선이고 단위가 대응되면 Hu 원전 먼저. |

원전 저자는 물리·근사 가정을 설명할 수 있고, 유지보수자는 수신판의 예외와 초기화·후처리를 다루며, UI 개발자는 목표 화면과 제어 API를 선택한다. 움직임이나 시각적 혼잡에 민감한 사용자의 우선순위는 이번 수치 진단으로 측정하지 않았다. 원전 설명의 유용함을 실제 설계자 행동 변화로 바꾸어 보고하지 않는다.

## 아직 닫히지 않은 경계

Graphviz A를 사후 발견해도 기존 봉인 A의 결손을 소급해서 채울 수 없다. 새 자료는 사후 설명이나 새 비교로 둔다. Graphviz private harness도 공개 GV-N/B의 빈칸을 직접 채우지 못한다. 두 구현의 같은 판·같은 입력 원출력이 새로 나와도 현재 그래프 A/B의 운영적 예측이 같았다는 사실은 바뀌지 않으므로 새 원전 우월성 판정이 생기지 않는다.
