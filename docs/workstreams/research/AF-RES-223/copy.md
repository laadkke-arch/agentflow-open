# Copy / action identity — 조건부 설계 제안 (실험 결과 아님)

## 무엇을 이름에 남기는가

접근 가능한 이름은 (동작, 대상 종류/필드, 대상 인스턴스 구별자) 중 현재 목록에서 실제로 다른 동작을 구별하는 최소 정보다. 설명은 결과의 범위, 부작용, 대기·권한 같은 판단 보조에 쓰고 이름의 필수 구별자를 description에만 밀어 넣지 않는다. 링크의 보이는 문구를 이름에서 제거하지 않는다. 다른 이름을 붙였다고 다른 목적지인 것은 아니다.

| 실제 상태 | 짧은 보이는 이름 + 접근 가능한 이름 | 설명 / 배치 | 합칠 수 있는 조건 |
|---|---|---|---|
| A1, 같은 reference의 type/name 각기 전용 폼 | Change + reference type for {reference label}; Change + name for {reference label} | reference 카드 헤더, 이름 중복 시 확인 가능한 비민감 구별자 (예: 순번/기관) | 서로 다른 input이므로 합치지 않음 |
| A2, course/study mode 각각 편집 | Change course for {course name/code}; Change full time or part time for {course name/code} | 모드 변경 시 location 선택 재요구 가능 안내 | route args/step 및 연쇄 변경 동일해야 함; 여기서는 별개 |
| A3, phone/address | Change phone number; Change address | 주소는 거주 국가 질문부터 시작; 다단계 여부 안내 | 별개 |
| R1, course/education phase | Change course; Change education phase | 첫 화면은 training route; 더 정직한 대안 Change training route and course (실제로 route 이후 course 선택일 때); phase 수정 후 course details 단계 안내 | 별개 |
| R feedback | Change feedback (한 개); 또는 각 행에 Change satisfaction level / Change improvement suggestion, 해당 필드에 안정된 focus/fragment 지원 시 | 현재 같은 전체 form; 보조 설명 'Opens the feedback form' | action, 대상 레코드, 범위, 권한, 저장/복귀 계약 및 focus 모두 동일하고 행별 빠른 이동을 잃지 않는다면 통합 |
| R manual personal details | Change personal details (한 개), 또는 해당 field focus가 입증된 Change full name / Change date of birth | 동일 전체 form, 이름은 first/middle/last 그룹 | 단순 href 같음만으로 통합 금지; 이동 범위/의도 확인 |
| Library eBook 2012/2009 | Place hold: Pride and Prejudice — 2012 eBook / 2009 eBook | publisher AUK Classics / Penguin USA; copy availability/time-stamped snapshot; item/holding 선택이 필요하면 추가 선택 | 동일 bibliographic record와 실제 hold target/format/edition/holding policy, 비용 및 복귀까지 동일할 때만 통합; 이 사례는 다른 record IDs라 별개 |

세 가지 대안:
1. **짧고 명시적인 이름**: 목록에서 바로 구별. 동일 출판년/형식 또는 동명이인 충돌 시 edition/기관/식별 가능한 순번 추가. 모든 내부 ID를 발화할 필요 없음. 화면의 폭이 늘 수 있다.
2. **보이는 Change + 숨은 구별자 + 보조 설명**: 행을 순서대로 읽을 때 시각적 밀도는 낮다. 링크 목록에는 computed name이 중요; description/인접 행/카드 제목이 포함된다는 가정 금지. 보이는 Change만 클릭하는 키보드/음성 제어 사용자를 위한 discoverability와 label-in-name도 검토. 대상은 이름에, 부작용은 설명에.
3. **통합 링크**: 같은 전체 편집 화면이면 탭 횟수와 문구 관리량을 줄일 수 있다. 단, 해당 행의 바로가기·스크롤·focus·오류 위치를 잃거나 다른 ID/step/permission을 합치면 실패. 카탈로그 두 판본은 동일 제목/형식/같은 보이는 동사로는 통합할 수 없다. 통합하더라도 선택 화면에서 판·형식·소장 옵션을 명시해야 함.

### 관점별 손실과 검증

- 키보드/보조기기: 같은 이름을 반복해 듣는 탐색 비용, 잘못된 레코드/필드로 가서 수정·취소·재방문하는 비용; 정확한 focus 복귀, link list, 읽기 순서, 음성 제어를 각각 측정. 실제 발화 0건 공개 확인, 예상만.
- 일반 독자: 화면 내 row label이 보이는 경우 Change의 반복이 읽기 쉬울 수 있으나 좁은 화면, 카드 여러 개, 행이 접히면 맥락 상실. 링크 목록 외에도 선택 메뉴·검색 결과를 확인.
- 콘텐츠 편집자: 이름의 source of truth를 row key/action contract로 맞추되 번역의 조사, 대소문자, 동명이인, 비어 있는 값, 동일 type/title 중복을 시험. 카드 title을 무조건 자동 suffix로 붙여 중복시키지 않음.
- 개발자: href 대신 target tuple = (resource id, field/group, step, allowed state, focus, mutation/validation, return path). 동일 문자열/URL 여부는 별도 signal. renderer의 숨은 span과 aria-label/labelledby 우선순위, nil href 미렌더링, record ID/step, focus/validation test를 분리.

### 반증 조건
- 같은 이름이 다른 tuple이고 링크 목록에서 구별 불가하면 이름 규칙 실패. 다른 이름이 동일 tuple이고 동일 focus일 때 개별 링크의 가치가 입증되지 않으면 통합 후보.
- suffix가 다른데도 실제 accessibility tree에서 누락/aria override/숨김이면 개선 가설 실패. 반대로 링크 목록이 실제로 안정적인 행/카드 context까지 제공하면 이름에 더 짧은 구별자만 남길 수 있음.
- 합친 링크가 더 많은 키보드 탐색/취소/수정 실패를 유발하면 통합 제안 철회. 실제 A2/A3/R1에는 연쇄 단계가 있으므로 한 필드만 바뀐다고 단정하지 않음.
- 도서관은 record link 클릭만 확인했다. 예약 요청·holding ID·실제 button name 미확인. 같은 action label 추출은 L01, 다른 bibliographic ID는 L02/L03. 추천 카피는 검증 전이며 출판연도/판·발행처 중 사용자 판별에 필요한 최소만 남긴다.
