# 범위·원장 보정 (원판 보존)
원래 범위 6b27d5a329cfe78cf5de4ccd2972b9f6bf7476de 및 모집창 3387248581df67fecc3e4d5db4ff0d02fa2bd2e9는 수정하지 않는다. 결과 해석 시 본 보정을 함께 적용한다.

- pandas 최초 명시적 지원 후보: v1.5.0의 #46425 및 릴리스, v1.4.4의 실제 timezones.pyx와 v1.1.5/1.2/1.3/1.4.0의 심볼 비교. 이전 모든 공개 API에서 ZoneInfo가 불가능했다고 단정하지 않는다. 선택 창 v1.4.4→v1.5.0→v2.0.0→v2.1.0. 2.0/2.1의 전 변경 코딩은 미완.
- Django 3.1.7(2021-02-19), 3.2.9(2021-11-01)은 전환일보다 앞선 마지막 확인 판으로 고정. 3.1.8/3.2.10은 전환일과 동일하여 시간순 확인 전까지 별도 같은 날 경계로 보존한다. 후속은 기능판 단위. 5.0 제거는 별도 경계로만 사용하고 이후 두 판을 추적하지 않았음.
- pandas 두 번째 후속 기능판은 2026-11-24 UTC 현재 공개 릴리스 목록에서 미관측. 3.1.1(2026-11-04)은 패치이며 3.2를 만들어내지 않는다. right-censored. 
- release_refs.csv의 SHA는 GitHub refs API의 annotated tag object(커밋 SHA가 아님). 각 원전의 URL은 sources/timeline에 있다. 변경 ancestry, 모든 태그 peel 및 모든 시각 순서 직접 검증은 미실시.
- merge_parents.csv: PR API base와 실제 squash merge 부모는 다를 수 있음(P2/P7). 첫 편집 대신 현재 PR commits API의 첫 visible commit을 기록. D1/D2는 PR merged_at과 저자 commit 시간 구분(특히 D2 9/9 작성, 9/16 병합). 
- changes.csv P4 limit의 P5/P7은 P5/P8로 읽는다: #66818(P7)은 인접 JSON 문제이며 해당 최적화로 유발됐다고 입증하지 않았다. P6는 3.1 릴리스가 후속 수정 명시(S26). downstream.csv X3 및 S47의 diff 미열람을 S59로 보정(+32/-9 fixer, +54/-1 tests). 추가 기록을 원장에 append하고 기존 행을 유지.
- D0 #13073 초안은 미병합, 실제 자체 구현 대신 기존 pytz를 작성자의 shim으로 바꾼 PoC. 최초 닫힘 2020-06-17(웹 활동), API 최종 closed_at 2021-01-19로 서로 다른 상태 전이 가능. D2 #14848는 #14669 후속 재개이며 이전 본문은 미열람.
- 원전 확인 UTC 날짜만 보존(분/초 결측); 링크가 mutable이면 fixed_url null 또는 태그 정보/PR merge 보조. 원전 데이터 두 교통기관·두 방송 레코드 확인, 방송은 시각 자체가 없는 일자/부분일자이며 역사적 offset 없는 시각의 독립 예는 미확인. 
- 본 보정 전 원장 57행/28 고유, 보정으로 20행/1 고유 추가. 최종 원장 77행/29 고유(중복 제외). 실제 source body/selected diff를 읽은 것만 포함.
