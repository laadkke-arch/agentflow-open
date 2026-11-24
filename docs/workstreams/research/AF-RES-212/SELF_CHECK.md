# AF-RES-212 자체 점검
자체 검토자: 이 작업 작성 세션. 독립 검토자 없음. 최신 기기 실행/신규 실험/사람 성공률 없음. 201 의존 결과와 사용자 가설 사전 노출. 실제 문서 읽기/게시 코드/도착면과 이름 계산 기대/관측 보고를 분리.
|질문|근거|반례/결손|다음 원문|
|---|---|---|---|
|Q1|D01–D05,L01–L05|CE1, GOV 0/6; strict 6/12|공식 service raw DOM 및 distinct href|
|Q2|W03,W04,W08,D02,D05|CE2,CE6,CE7; tree 미측정|fixed WD+실제 accessibility tree|
|Q3|T01–T06,D09,D13,R02|CE6,CE10; rotor guide 429; 명시 description output 미확인|NVDA/VO versioned list+continuous existing logs/fixture|
|Q4|W01,W02,W05,W06,W09,W10,D12|CE2,CE4,CE5; 동일 name+다른 실제 href strict 미확인|실제 HTML pair/도착면|
|Q5|W07,D09–D13,R01,R02|CE3,CE7,CE8; 길이 통제 연구 부족|GOV/USWDS 원시험·당사자 길이/voice command|
|Q6|P01–P04,F04,F05,F06|CE9; publisher supplement file 미열람|실제 공식 supplement file/landing 및 library sample|
|Q7|cards.md,W01–W10,T01,T02,D09,D13|CE1,4,6,7,8; A/B/C/D 실제 기기 검증 없음|같은 card fixture, 두 mode, speech command|
## 분모와 자료 유형
정규 계획 12 anchors/6 examples. 확인 6 anchors/3 examples (GOV 0/6, US 6/6); 2 unique href; 4 supplemental anchors (2 fake href, 2 raw HTML 미확인). frame 23행: 12 planned + 11 screen/jump, 전 페이지 모집 후보 전수 보장 아님. examples.csv/names.csv 각 16행. 원장 47행: 유형별 하한 산입 35 (W3C 10/5, tool 6/5, design 13/7, publication 4/3, user 2/2), 보강 5, 실패·본문 부족 7. 동일 D05 3 variants는 1저작; 같은 문서 절/미러·실패는 추가 산입하지 않음. 서로 다른 저작이더라도 동일 계보/결함이면 독립 관측으로 합산 금지. 독립 사용성 사건 수 전수 코딩 미실시; survey 2건 별개, D09/D13 리뷰 사례, D10/D11 한 계보. 
## 자체 재검토 및 결손
- URL 실제 도착과 제목 의미 대조: dashboard는 소개 기사. 날짜 차이 유지.
- GOV fake href를 성공한 실제 목적지로 승격하지 않음; 실제 서비스 raw code 미확인으로 보강 유지.
- 같은 목적지 동일 name 대조 및 같은 name/다른 목적지 모의 예제와 기존 제보 분리; 후자의 실제 strict pair 부족.
- 201 결과 전제: 중앙 DONE이지만 인계 자체 PARTIAL; C E3 static path, E4 없음. 생성 코드/논문/그림 구별.
- 표 1–3 열 순서 준수, 마지막 약점표 3행. 기기 output은 names.csv 전부 미측정. 결과 고정 SHA에서 원장/표/반례 다시 읽고 검증 후 HANDOFF 별도 커밋할 것.
- PARTIAL: strict 모집 미달 6/12, Q3 정확 rotor 출력/설명, Q4 실제 같은 이름/다른 href pair, Q5 길이 연구, Q6 publisher supplement 실제 파일 미확인. 35/22 자료 하한 자체 충족은 완료 대체 아님. 
