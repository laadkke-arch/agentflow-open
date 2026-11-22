# 별도 현장 자료 — 검색 후보18과 분리

네 고유 원문은 세 현장 사건을 다룬다. 교통의 두 자료는 같은 감편 과정의 발표와 이후 실시간 자료 기반 집계 보고의 비교다. 문서4개를 독립 사건4개로 바꾸지 않는다. 이 자료는 Q6·Q7의 반증에만 쓰고 원 검색 순위/분자를 고치지 않는다.

## FIELD-TRANSIT-PLAN — 예정된 변경과 조정 주체

F01 [MTA 2020-03-24 발표](https://apps.cio.ny.gov/apps/mediaContact/public/view.cfm?parm=926C019C-DE79-DD17-D6493016DF74143F_5D9C1A27-C9C7-90C0-217C93A974EEA6D8)의 지하철·버스·통근철도 절은 단계별 적용일, 일부 노선의 대체 운행, 필요시 보충할 인력·차량, 웹·앱·역 안내를 연결한다. 소프트웨어에 참고할 관계는 새 운행 상태를 선택한 운영자가 여러 관측 지점에 알린다는 것이다. 실제 상태를 바꾸는 권한과 알리는 채널의 존재는 서로 다른 근거다.

이는 공표된 변경 계획의 1차 자료다. 여기의 수치·표현만으로 이후 모든 시간대의 실제 운행을 보장한다고 읽으면 안 된다. 물리적 차량·승무원 제약을 디지털 작업 복제 비용으로 그대로 옮길 수도 없다.

## FIELD-TRANSIT-EXCEPTION — 같은 목적의 발표가 이후 관측을 대체하지 않음

F02 [NYC Department of City Planning, 2020-04-21](https://www.nyc.gov/assets/planning/download/pdf/planning-level/transportation/covid19-transportation/20200421.pdf)의 인쇄p13은 2월13일·3월12일·4월16일의 시간대별 정차 패턴을 비교한다. 그림은 이후 시점의 출퇴근 시간대 편성이 줄고 주간 첨두/비첨두 구분이 약해졌음을 설명한다. **해시가 고정된 직접 PDF의 출처는 MTA Real Time data다.** 같은 바이트의 텍스트·로컬 렌더·재다운로드가 일치했다. 웹 screenshot만 GTFS라는 다른 표기를 보여 원 초안이 잘못 분류했다. 그 도구 불일치는 [재개 감사](resume-field-audit.md)에 보존했다.

F01과 함께 읽으면 선언한 보존 목적과 이후 다른 기관의 운영자료 집계를 구분해 확인해야 함을 보여 준다. DCP가 MTA 자료를 사용하므로 독립 측정 두 벌은 아니다. 날짜와 척도가 다르므로 즉시 약속 위반으로 단정하지 않는다. 이 연구는 원시 실시간 feed·집계 코드를 재실행하지 않았으므로 개별 열차의 실제 출발 전수를 입증하지 않는다. 다음 확인 자료는 2020-02-13·03-12·04-16의 보존된 feed, DCP 집계 코드와 예측/실현 판별 규칙이다.

## FIELD-STATS-HISTORY — 수정된 주장과 이전 주장의 연결

F03 [ONS 정정 페이지](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/articles/reconciliationofmidyearpopulationestimateswithcensus2021englandandwales/2023-02-28/previous/)와 [v2](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/articles/reconciliationofmidyearpopulationestimateswithcensus2021englandandwales/2023-02-28/previous/v2), [v1](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/articles/reconciliationofmidyearpopulationestimateswithcensus2021englandandwales/2023-02-28/previous/v1)을 직접 대조했다. §5의 연령별 설명과 그림4·5의 지역 표지 순서는 별도 정정 공지로 연결된다. 전후본문은 원문의 이전판 링크로 찾을 수 있다.

이 자료는 수정 이유·대상·판을 찾아갈 수 있음을 확인한다. 소비자가 최신판을 자동으로 읽었거나 분산된 사본을 되돌렸다는 근거는 없다. 저자가 수정할 권한을 가졌다는 전제를 권한이 없는 소비자의 취소/철회 능력으로 옮기면 대응이 깨진다.

## FIELD-STATS-BOUNDARY — 순이동이 같아도 구성 값은 틀릴 수 있음

F04 [공식 전후판 목록](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/estimatesofthepopulationforenglandandwales/mid20222023localauthorityboundaires)에서 2023-12-19 정정의 v1·v2 XLSX를 직접 받았다. `compare_ons.py`는 워크북을 수정하지 않고 MYE3의 지역코드357개를 맞춰 비교했다. 39개행의H/I열78셀만 달랐다. 이 표에서 순이동J열과 인구O열은 바뀌지 않았다.

| 자료 ID·위치 | 정정 전 유입 / 유출 | 정정 후 유입 / 유출 | 전후 순이동 | 확인 범위 |
| --- | --- | --- | --- | --- |
| F04 MYE3!H9:J9, England and Wales | 3,768,798 / 3,778,598 | 47,924 / 57,724 | −9,800 / −9,800 | 국가 안 이동을 총유입·유출에서 제외한 경계 수정 |
| F04 MYE3!H10:J10, England | 3,628,364 / 3,648,816 | 112,337 / 132,789 | −20,452 / −20,452 | 같은 방향의 수정 |
| F04 MYE3!H11:J11, North East | 133,150 / 123,406 | 66,260 / 56,516 | 9,744 / 9,744 | 지역 경계에서의 수정 |
| F04 MYE3!H12:J12, County Durham | 29,011 / 23,640 | 29,011 / 23,640 | 5,371 / 5,371 | 비교한 변경 없는 행 |

검사 입력 파일 SHA256·행별 차이·실행 범위는 [ons-correction-comparison.json](ons-correction-comparison.json)에 있다. 전체 워크북이나 추정 알고리즘의 재현은 아니다. 같은 최종 값이라는 표면 유사점만으로 중간 입력·범위·행위가 같은 원리라고 판단하면 이 반례를 놓친다.
