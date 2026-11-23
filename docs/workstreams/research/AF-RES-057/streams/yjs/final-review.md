# Yjs final draft review

- 검토자: Yjs 분담 연구 에이전트. Yjs 자료 작성에도 참여한 같은 모델이며 독립 외부 심사자가 아니다.
- 검토 완료 UTC: **2026-11-23T03:47:50.380725+00:00**. 최종 보고서를 받은 뒤 이 시각까지 읽기·원장 대조만 했고 새 제품 실행이나 추가 자료 탐색은 하지 않았다.
- 변경 범위: 이 검토 파일만 작성했다. root RESULT/CSV/집계, 봉인 cases/cards/predictions는 수정하지 않았다.

## 실제 읽은 범위

`RESULT.md` 전체163행 중 Yjs의 첫 표9행, 둘째 표3행, 연구 순서·Q1~Q7·집계·마지막 약점 표의 Yjs 관련 주장을 검토했다. `observations.csv`의 YN1/YN2/YT1×A/E/D 9행, `predictions.csv` 관련9행, `cards.csv` 관련9행과 두 집계 JSON을 읽었다. raw 연구 stdout14변형, 사후 감도2변형, stream observations/source ledger 및 고정 원문 cache의 constructor/filter·gc 절·stopCapturing 절·선택 assertion을 대조했다. 원문204의13.0.8 명시도 재확인했다. PM 및 지도·회계 원전의 사실 진위는 이번 검토 범위 밖이다.

## 대조 결과

1. **정상 상태 전사18개(A/B×9보기) 모두 raw 출력과 일치**한다. before/undo/redo와 undo 깊이·undo/redo 깊이 쌍까지 비교했다. YN1의 끝 공백과 YN2의 `Hello123 World` 공백 위치가 보존됐다.
2. **봉인된 보기별 판정과 구분이 맞다.** YN1 A/E/D는 시대 호환 보조 입력에 조건부 A만, YN2는 모두 판별 불가, YT1은 A만이다. YN2의 사후 gc=false 성공을 새 정답으로 소급하지 않았다. E/D가 다르지 않은0/6과 조건부 분모0의 구분도 맞다.
3. **YT1 공개 assertion 범위가 맞다.** 고정 파일 L49–57, L56은 A undo=[1,2,3]만 선언한다. B/redo 확장은 연구 입력이며 원시험 실행 또는 CI 통과로 서술하지 않았다. helper의 세 사용자 가운데 선택군은 array0 하나만 편집한다.
4. **YN1 원사건과 연구 변형이 구분되어 있다.** actual author version/initial document는 미확인이고13.0.0-94는 이미 공개된 호환 프리릴리스 보조판이다. 위치 인자 생성자는 실제 source L105, origin filter는L129다. 역순 첫 화면 동률과 다음 undo의 차이도 raw 결과에 있다.
5. **YN2 판/한계가 맞다.** 원문은13.0.8을 명시한다. 두 Doc에 같은 gc bool을 적용하는 개입이며 private stack 대입·redo 성공은 공개 API 보증으로 승격하지 않았다. 원본문 근사 기대와 최초 수정본 미확보를 구분했다.
6. **문헌 절 위치가 맞다.** YN1 E L707–712, YN2 gc L466–470 및 E L692–694, YT1 E L1231–1233/API L321–343은 직접 열었던 고정 원문과 맞다. YN1-A code_lines 오류는 봉인값을 보존한 별도 정정으로 표시되어 있다.
7. **실행과 저작 분모가 맞다.** Yjs 주14와 사후2를 구분했다. root의 doc/undo implementation alias 적용 후 Yjs 고유 적격 work 수33은 stream에서 다시 센 값33과 같다. MAX_VALUE·390·392·454의4개 수정 계보는 중복하지 않으며 test+issue/fix를 따로 늘리지 않았다.

## 구체적 정정 요청

| 우선순위 | 위치·현재 문구 | 권고 수정 | 이유 |
| --- | --- | --- | --- |
| 필수 문구 정정 | RESULT.md L161 마지막 약점 표: `자연6자리 전체` | `여섯 자리 전체` 또는 목적이 자연층만이면 `자연4자리` | 여섯 자리 중 자연은4, 진단은2이다. 첫 표·집계와 모순되는 단순 표기다. |
| 출처 범위 명료화 | observations.csv YN1/YN2의 public_CI와 source_urls가 Y-CI-PROBES(13.6.28 및2022 fix SHA들)를 공통 참조 | `YN1/YN2 역사 SHA의 CI는 이 probe에 포함되지 않음; 동일입력 실행 미확인`을 명시 | 미확인 판정 자체는 맞다. 다만 diagnostic/fix SHA의0기록을 해당 자연판 SHA를 직접 조회한 결과로 읽히지 않게 한다. |
| 링크 라벨 정밀화 | RESULT.md L26: `stopCapturing API와 MAX_VALUE 회귀 시험` 링크가 UndoManager API 파일만 가리킴 | 라벨을 `stopCapturing API`로 줄이거나 별도 원시험 링크를 나란히 제공 | 클릭 한 번으로 보게 되는 내용과 라벨을 맞춘다. 원시험 링크 자체는 첫 표에 정확히 있다. |
| 서술 범위 권고 | RESULT.md L57: `연구 정상 순서에서는 내 삭제 뒤 상대 삽입...` | 문장 앞에 `PN1 보조의` 등 사례를 명시 | YN1 정상은 내 삽입→보호 삽입이며 삭제가 아니다. 전체 사례에 적용되는 공통 사건열처럼 읽힐 여지를 줄인다. |

이 정정들은 봉인 예측이나 관측 결과를 바꾸지 않는다. 연구 PARTIAL 판정과 E/D 동률·분모0 결론을 뒤집을 사실 충돌은 발견하지 못했다. 공개 원진단/원작성자/CI를 연구자의 재실행과 구분한 핵심 한계는 보고서에 유지되어 있다.

## 검토한 파일 판 식별

아래는 이 검토 시점의 파일 SHA256이다. 후속 문구 정정 후 해시가 달라지는 것은 예상되며, 이 검토를 나중 판 전체에 대한 자동 인증으로 사용하지 않는다.

| 파일 | SHA256 |
| --- | --- |
| `RESULT.md` | `7b90c04c278586852ba4c7fad0045474c2debb638d4f25efd1e58aaa58ec1cd8` |
| `observations.csv` | `146a081eb73c7984cfe6b2b7eb009a865cda0df41005406d7ddb657b85d5d3db` |
| `evidence/comparison-counts.json` | `38f32368beec7697b451252024e18de1e2592bb8b9b53229393d168e6d024023` |
| `evidence/final-counts.json` | `4a17736cb49db65031b595658371f1640e2b8a7f4217dd1d546fccd2ca4e5dac` |
| `predictions.csv` | `2942704582d82b600586e381bb1ef850256e5a15d20520c9fb36d456ebb2776c` |
| `cards.csv` | `e9211d85ba633a19c7c4fa23bcab8379e7b7d82e5b40fb2441c189a60e5f5300` |
