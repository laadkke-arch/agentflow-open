# 관측 정정과 영향 기록

사전 표본·선정·종점·분모 규칙은① `f3c8de473b52a64c92c862cc64927ce787525c1a` 이후 바꾸지 않았다. 아래는 원문을 더 읽어 코딩을 바로잡거나 같은 종점을 분리한 기록이다. 의존 작업 파일은 수정하지 않았다.

| ID | 종전 정보 | 직접 근거·정정 | 영향 행·결론 | 보존 시점 |
| --- | --- | --- | --- | --- |
| R01 | eXoaDocs 초기 분담 메모에서 제한시간 미확인 | NA-002 §5.3.2 p21에 전체40분 명시 | S02, J-NA-04, O-NA-04~08. 제한시간 내 all-pass3/12·1/12는 저자 집계로 보고 가능; 시간표 포함자와 pass자는 여전히 미연결 | ② baseline에 정정 후 봉인; streams/ncq-exoa/REVISIONS.md |
| R02 | 034의 광범위 browser 허용 요약은 Blueprint 조건을 충분히 구별하지 않음 | BC-01 p518의 Blueprint군 browser 금지, control Firefox+Adobe Community Help | S03, BC-J01, BC-O01~04B. 허용 자원까지 달라 explanation-only 귀속 불가 | ② baseline에 원문 차이 기록 |
| R03 | 분석 NCQ10명 전원이 과제를 마쳤다는 배경만 알려짐 | NA-004 §3의 예약14명·성공 세션10명·세션 중 철회4명 | S01/J-NA-03. 예약14를 무작위 배정분모로 간주하지 않고 철회 단계·조건을 미확인으로 유지 | ② source/baseline; ③ join |
| R04 | 분담 BC-O04에는 directed 코드와 exploratory 차트 품질이 한 레코드에 기술됨 | 서로 다른 과제·종점을 분리하는 사전 규칙 적용 | 통합 outcomes는 BC-O04A/B. 원 BC-O04와 origin 위치 보존; 수치·규칙 변경 없음 | ③ build_ledgers.py |
| R05 | Strata 출판표의 precision을 단일 참값으로 읽을 위험 | US-11 원 제작 자료와 PDF 그림은91.0%, 표는90.1%; recall 관계도 불일치 | O-US-05. 어느 값을 임의 정정하거나 합치지 않음 | ③ 원 제작 자료 감사 |
| R06 | DataShop shell에 Students/Transactions 문자열이 있음 | 실제 데이터 값이 아닌 공통 도움말임을 재확인 | X02, J-RT-02/03. dataset77/78은 후보 metadata이며 코호트/원행 확인 아님 | ③ datashop-metadata-fields.json |

②의 DataShop HTTP receipt에서 반복 UI 도움말 전문은③에서 제외하고 상태·응답 hash·주소·시각·사실 metadata만 보존했다. 접근 판정이나 원자료 분모는 바뀌지 않았다.

선별 후보 ALICE의 DOI는 원고 작성 중 출판사 metadata로 확인하여 `10.1109/ICSE.2019.00044`를 사용한다. 선별 결정에는 영향이 없다. 공개 파일에 오류를 발견해도 원 배정표·채점 원자료를 갖기 전까지 연구 저자의 값을 추측으로 교정하지 않는다.


통합 검토 R07: 요약 CSV가 상세 JSON의 알려진 상한·설계·분모를 미확인으로 내린 매핑, exact full-row 중복과 P×T의 정상1:N 혼합, BC-O04B rank sum 누락을③ 이전에 정정했다. eXoa40분, Blueprint600/900초, 동일10명과 독립25/25·15/15, 예정기회와 실제시간행을 명시했다. 추정치·분석 규칙의 사후 변경은 없으며 세 분담 검토의 지적·조치는 evidence/review-ledgers.json에 기록한다.

통합 검토 R08(④): RESULT 합성 과정의 Blueprint 그림/절 locator, CodeMend source ID·대조명·score 위치, BC-O07 범위와 실행 interpreter를 원장대로 바로잡았다. 두 군 이상에서 실제 파일 수준 탐색한 사실과 NCQ1군의 부분 참가자행 확보를 분리해 수용 판정을 보수적으로 정리했다. CSV는 git의 LF 정규화와 재현 hash가 일치하도록 writer의 줄끝을 명시했다. 사전 규칙·수치·원행·기존 커밋 CSV 내용은 바뀌지 않았다. evidence/review-result.json 참조.
