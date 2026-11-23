# AF-RES-060 자체 검토

종합 주체: `/root`. 상태: **partial_handoff**. 공급자 설치·시험 실행0, 원 요청자의 성공 관측0. 파일·순위 무결성 검사와 연구 가설의 입증을 구분한다. 숫자의 출처는 evidence/comparison-summary.json, feature-freeze.json, source-counts.json이며 마지막 원격 재열람/계약 검사 결과는 evidence/verification에 별도 저장한다.

## Q1~Q7 주장·직접 근거·반대 탐색·뒤집힐 조건

| Q | 현재 주장 | 직접 근거·위치 | 반대 자료·탐색 결과 | 뒤집힐 조건 |
| --- | --- | --- | --- | --- |
| Q1 | 두 조건과 환경·guard를 유지해야 부분 기능을 전체 권고로 오인하지 않는다 | requirements.json 12자리의 source_location/condition_origin(s)/contrast_examples; H-SO-S01/S02/L01/L03 revision1 | JS-3에서 참조만 해결하고 required를 버리는 대비, LD-6 추출 후 가격을 버리는 대비. 실제 실행 실패가 아니라 논리적 근접음성. Schema rank2의 코드 보존 C2를 일관되게 인정하도록 순위 전 선정 정정 | 동일 원문·판에서 두 조건이 독립적이지 않다는 더 직접적인 의도 자료, 또는 같은 구현판의 공동 조건 입력·출력 |
| Q2 | 62행 전수 편집으로54행에154개 기능 원표기를 추가했다 | features.csv 모든 행·feature_evidence_json; source_ids; evidence/feature-freeze.json | LD-001 표준 준수명, SC-033 링크만 있는 README, Sophia 선택 모듈, wrapper의 위임. 빈 필드가 부재를 뜻하지 않음. SC-001/004 component release와 SC-010 전역 마지막 release 미확인 | 같은 규칙의 독립 편집자가 고정 창에서 다른 적격 기능 순서를 재현하면 추출 민감도 필요; 실제 자사 기능/판 근거가 나오면 해당 빈 행의 별도 새 판 갱신 가능 |
| Q3 | 정의 기반 질의와 공급자 원표기는 다른 축이다 | vocabulary.csv 59행; STD-SC-CORE07/VALID07, STD-LD-API11/FRAME11; holdout/vocabulary-amendment.json | validation→Validator는 Schema40행 적중; enum은 동적 instance 값 삽입 아님; RDF dataset은 Turtle text와 범위 다름; framing은 DOM/R/HTL 처리 아님 | 동일 고정 정의가 원문 입력·출력·연산 방향을 보존한다고 입증되면 별도 감도에서 허용; 런타임 교체 의도가 명시되면 환경 평가를 별도 갱신 |
| Q4 | F1에서 후보가 있는 요구는 L 0→3, V 2→6으로 증가하나 top3의 기존 미확인 후보가 밀린다 | matches.csv 48행; slots.csv 144행; changes.csv 12행; 별도 review/stage3-audit | SC-032가 JS-4 1→11, JS-6 1→5; SC-016이 JS-4 3→6. 완결 탈락0이지만 진위가 확인된 후보분모0. SC-035는 JS-6 검색 밖에서도 string property 메커니즘이 있는 사후 반대 사례 | 봉인 입력의 재생 오류가 발견되거나, 동일 순위·조건에서 밀린 완결 후보 직접 근거가 나오면 선택 손익 판정 변경 |
| Q5 | 같은 경로의 공동 조건 완결0; JS-6 Ajv만 C2 조건부 부분1쌍 | paths.csv 84행; PS-SC-005-P1 289–304행의 object.properties.bar:string 및 compile | literal-only 감도에서는 부분0. SC-036 integer→string은 일반 이름 변경과 다른 제약 전이. SC-040 inline/simpler, LD-008 framing/streaming writer의 근거를 섞지 않음 | 같은 허용 경로·고정 구현판에서 C1/C2/환경을 직접 연결하는 입력·출력. 추가 예산 실행은 별도 진단이며 기존 두 행동 결과를 소급 변경하지 않음 |
| Q6 | 확정오답 관측0은 오탐률0%가 아니며 정확도 산출 불가다 | 28쌍: 부분1/미확인27; 18표시슬롯: 부분1/미확인17; candidate-verdicts.json | optional/required 필드 추론과 배열/조건식의 다른 범위; broad aliases/runtimes. 같은 positive 통과·near-negative 실패의 실제 요구 실행은 미실시. all-withheld 신규쌍 진위도 미실시 | 진위가 직접 확인된 표본·분모가 생기면 해당 범위에서 오답/완결 수 변경. 불확실성을 모두 음성으로 처리하지 않음 |
| Q7 | 출처·개념·관계·판 기록은 검색 설명에 유용하지만 구현의 지원 증거를 대체하지 못한다 | AUTH060 LOC2/Getty2 실제 레코드, MARC 4XX/5XX/$w, Getty Terms/Scope/Relations; authority/findings.md | Lithographs 이전채택형, Lithography 상위, offset 두 개념의 distinguished from와 원이미지 조건. 이름·장비·출력을 한 동의어 집합으로 합칠 때 범위가 무너짐 | 기능명-정의-구현판-공동 조건을 연결한 같은 경로 근거가 나오면 반환 카드 승격; 전거 최신판 변경은 새 판 대조로만 반영 |

## 분모와 무결성

- 기존 F0 16비교 재생과 고정9파일 바이트 일치. 전체48 비교·144슬롯·43매치발생·28쌍·20게시행·84경로. 기존8은 튜닝층이고 새4만 봉인 후 모집층이다.
- 새 모집40자리 중35원본 직접 읽음, LD틀5개 부족. first2 적격씩은4/4 확보하여 미실시 요구0이다. 현재태그·revision1 한계 보존.
- 전체 후보 판정은 경로 전체를 선택하며 C1과 C2를 다른 경로에서 합치지 않았다. 28쌍 모두3경로다. 조건별 직접 근거와 저자 진술/연구자 전이를 분리한다.
- 출처193사건 중 실질 직접 열람165사건, 계보113원저작/신규95. 기존 목록 공급자57저작과 새 후속 utility2저작은59개 독립 엔진이 아니다. 실제 전거4개, 고정 정의4개, 목록/규약2개, 선정 요청4개와 서로 다른 공급자8개를 따로 확인했다.
- 엔진 계보는 별도 민감도다. stage3-audit의57→53표기는 최종 감사에서 SC-018의 Ajv 위임 누락을 발견해 정정한다. 새 사용자 첫 창에서 SC-008→Blaze도 확인했다. 이러한 계보 그룹을 독립 엔진 수라고 주장하지 않는다. 순위의 exact URL 규칙은 변경하지 않았다.
- 불일치·약점 표는 RESULT 마지막에 정확3행. 첫 두 표는48행+12행. 빈 슬롯, 관측0, 진위 미확인, 미실시, 해당없음의 분모를 구분한다.

## 예산·판·비용에 대한 반대 검토

1. **두 경로 초과:** P-SC-036-D3에서611표시단어가 실제 노출되어 JS-4/JS-6 P3가 엄격 예산 미충족이다. 고유 초과111, 두 경로 논리초과222를 구분한다. 원영수증·SHA·계수를 보존했고500으로 잘라 보았다고 주장하지 않는다.
2. **인수 경계:** JS-4/SC-032 P3의 제목 없는 JSON 표시 경계는 미확인이다. 새 JS-6의168단어 창을 소급 대입하지 않는다.
3. **편집 노출:** 허용 제목·기능 분리 해석을 고치며 추가1,411단어를 읽었다. 모두 새 모집과 순위 이전이지만 엄격한 무추가노출 연구라고 표현하지 않는다.
4. **비용 하한:** metadata≥190이며 누락된 초기 retry를0으로 채우지 않는다. 공유 응답·fragment·같은 엔진을 중복 독립 저작으로 세지 않는다. 돈·token·사람의 소요시간은 실측하지 않았다.
5. **판:** 고정 commit과 component 정식판, 당일 HTTP 응답, 실제 요청자의 설치판은 다르다. 일반 규격 최신 문서를 고정 구현의 실행 증거로 합치지 않는다.

이 결손 때문에 결과 파일을 모두 저장하고 기계 검사를 통과하더라도 연구 상태는 부분이다. 새 독자의 깨끗한 복제, 누락 판/요청 영수증, 동일 구현판의 실제 공동 조건 입력·출력이 최소 후속 자료다.

## 실제 검토 주체와 범위

`/root`는 계약·고정 입력·공식 정의·목록 규약을 인수/직접 읽고, 새 선정4본문 원문·조건 경계와 F1 추출 정정을 감사하고, SC-032의 새3경로를 읽고 모든 기계 원장을 종합했다. `/root/features_schema`와 `/root/features_ld`는 각각 배정된 공급자 편집·51/27경로를 독해했다. `/root/authority`는 새 모집35본문을 공급자표와 분리해 읽고 실제 전거4개를 조사했으며, 별도 순위 구현 및 최종 출처/경로/표 분모 감사를 수행했다.

LD 별도 검토자는4쌍12경로의 허용10창을 읽었다. Schema 별도 검토는 Ajv/Blaze 지정6창과 조건부 전이/조건 독립성에 한정된다. 전체 외부113저작을 또 다른 사람이 처음부터 다시 읽었다고 주장하지 않는다. 같은 모델 계열이며 일부 문맥을 상속했으므로 blind replication이 아니다. 실제 검토 결과와 지적은 evidence/review/final-audit.*, evidence/paths-ld/review-evidence.json, evidence/paths-schema/review-scope.json에 있다.
