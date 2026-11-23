# AF-RES-061 출처 계보·분모 최종 감사

- 감사자: `/root/source_audit`, UTC `2026-11-23T06:25:31.267057+00:00`. 고정 입력 `672366cdf4542d4ca9f579963d66c2745f4316ed`.
- 기존 예측·실험을 재실행하지 않았다. 커밋된 원장의 계보와 분모를 점검했고 E003의 설계 분모 의문만 원문을 다시 열어 확인했다.

## 결과

**외부 1차 고유 저작 31개**를 확인한 원장이 있다. 이는 최소 20개를 충족한다. 루트 원장은 봉인 전 50행만 있어 후속 독해를 합쳐야 하며, 스트림 전체는 150개의 고유 source_id다. 루트50행은 스트림에 내용이 동일하게 중복되고 충돌은 관측0이다. `count_eligible=true`32행 가운데 D001/D013은 같은 Hu 저작이므로 고유 저작은31이다.

| 겹치지 않는 배당 | 실제/요구 | work_id |
|---|---:|---|
| component_lineage | 4/4 | `d3-force`, `graphviz`, `ANDROID-DYNAMIC-1.1.0`, `react-spring-v10.0.3` |
| independent_issue_or_design | 13/4 | `ANDROID-CANCEL-LINEAGE`, `ANDROID-REMOVE-ANIMATIONS-2022`, `d3-issue-166`, `d3-issue-169`, `d3-issue-186`, `graphviz-issue-2852`, `graphviz-issue-2283`, `graphviz-issue-2560`, `graphviz-issue-2129`, `graphviz-issue-2572`, `react-spring-stale-updates-2377-2381`, `react-spring-precision-jank-1389`, `react-spring-clamp-placement-813` |
| original_source_astronomy | 2/2 | `SALMON-WARREN-1992-1994`, `DEHNEN-2002` |
| original_source_oscillator | 2/2 | `VANDERBILT-LAB-2020`, `JAYAPRASAD-2013` |
| independent_output_study | 4/4 | `HU-2005`, `FRUCHTERMAN-REINGOLD-1991`, `HEER-ROBERTSON-2007`, `DRAGICEVIC-2011` |
| additional_boundary_or_accessibility | 6/4 | `MIT-1803SC-2011`, `OPENSTAX-UP1-2016`, `DEMMEL-CS267-1996`, `W3C-WCAG22-ANIMATION`, `WEBKIT-CRAIG-2017-MOTION`, `react-motion-v0.5.2` |

동일 저작을 원천분야 할당과 원출력 할당 양쪽에 사용하지 않았다. Hu는 출력 연구에만 배당했고, 천체 원전 두 개는 Salmon/Warren와 Dehnen이다. 진동 원전은 Vanderbilt 실험서와 Jayaprasad 원 실험 보고서다. MIT/OpenStax/강의는 보조 설명으로 분리한다. 각 저작의 직접 읽은 절·원장 위치·source_id는 [JSON](source-audit.json)의 eligible_works에 있다.

## 반드시 고칠 원장 연결

1. `sources.jsonl`을 canonical source_id150개로 합친다. 루트 원문의 모든50행은 그대로 보존 가능하며, 같은 내용의 중복은 acquisition_refs로 합친다.
2. `ANDROID-N/B`라는 초기 별칭7행을 정규 사례 키 `AN-N/B`와 연결한다. 원 독해 필드를 덮어쓰지 않고 canonical_cases를 추가한다.
3. metadata-only가 source 대표 행인 d3/Graphviz는 G011/G020 및 G012/G025/G026 등의 본문 독해와 함께 한 계보로 센다. 릴리스 메타데이터만 읽었다고 주장하지 않으며 반대로 릴리스 목록을 별도 저작으로 늘리지 않는다.

## 결론이 넘으면 안 되는 경계

- 독립 출력4저작은 네 수신 구현의 같은판·같은입력 원출력4개가 아니다. Hu/FR의 역사적 배치와 Heer/Dragicevic의 화면 지각 실험을 부수 근거로만 쓴다.
- 원전 추가가 구현 결과를 새로 맞혔다는 주장에는 봉인된 차이, 동일 입력의 독립 출력, 원전 절 근거가 함께 필요하다. 원장31개로 부족한 조건을 대신할 수 없다.
- D3의 Barnes–Hut 원1986본문은 접근 결손이 남고 B는 학술 강의 대체다. Hu B는 동종 그래프 연구다. Android/react-spring의 MIT 창은 연구자 유추이며 채택자 기록이 아니다.
- 이 조사의 인간 설계자 링크 효과/행동 변화 검사는 **미실시**다. 이슈 작성자의 설정 변경 보고나 유지보수자의 수정은 역사적 저자 보고다.
- E002는 같은24명이 두 실험에 참여했다. E003은 본실험12명·파일럿4참여 기록이며 겹침은 미확인이다. 이를 고유 참가자40명으로 합산하지 않는다.

## 반대 근거 재열람

E003 PDF pp5–6의 설계에는 12명×4기법×(3+2)프로필×12반복이 제시되면서 총2280시험으로 인쇄되어 있다. 산술값2880은 연구자 계산이고, 원시자료 또는 저자 정정이 없으므로 어느 쪽을 원시험 분모로 확정하지 않는다. 이 불일치가 해당 연구의 존재나12명 표본 자체를 없애지는 않지만 합산 정확률·메타분석 분모에는 쓰지 않는다. [원문](https://www.cs.au.dk/~elm/pdf/timedistort.pdf#page=6), [재독해 원장](source-audit-sources.jsonl).

D010 재열람은 웹 DisabledError로 실패했으며 [검색 원장](source-audit-search-log.jsonl)에 남겼다. 앞 세션의 본문 독해와 원문 파일 해시 영수증을 없애거나 이 감사의 새 독해로 세지 않았다.

## 판정

자료 최소 수·분리 배당은 충족. 주 8행의 같은판 원출력, Graphviz의 A 보기/한단계 공개 입력, Android의 최초 적격 이슈 모집 완전성 등은 이 출처 수 감사로 해소되지 않는다. 전체 작업의 수용 상태는 그 결손을 그대로 반영해야 한다.
