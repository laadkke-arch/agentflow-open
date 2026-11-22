# AF-RES-032 원장 의미

## 식별과 노출

reference_id는 소비자 배포 HTML의 한 문맥에서 클릭하는 한 참조다. document_key는 발행프로젝트+배포판+member로 고정한다. 동일 원고의 미러/렌더링은 duplicate_group로 묶고 고유 원문 최소수에서 한 번만 센다. A는 소비자-first, B는 사건-first 탐색 시도여서 합계 분모를 만들지 않는다. 같은 consumer+purpose+event_key는 겹침이다.

artifact_sha256은 내려받은 압축파일 전체, member_sha256은 압축 안 HTML 원바이트다. 원 HTML attribute의 entity 표기는 raw_href_html_attribute, 브라우저가 읽는 값은 raw_href, 해소 주소는 resolved_url이다. file:// base는 실제 독자의 경로가 아니라 절대href 해석에 영향 없는 계산용임을 표시한다. 현재 final_url로 원 href를 덮어쓰지 않는다.

## 시간

| 필드 | 뜻 | 대체해서는 안 되는 것 |
| --- | --- | --- |
| upstream_effective | 상류 주소/내용 변경의 시행 또는 증명된 경계 | 발표계획·PR작성·현재404 |
| consumer_source_edit | 관련 source 문구가 바뀐 commit | 배포된 HTML |
| merge_at | 그 변경의 branch 통합 | build/독자 노출 |
| build_at | 실제 HTML생성 영수증 | 공개발행·실제열람 |
| consumer_publication | 그 HTML을 포함한 판의 공개 | mtime·후대수집일 |
| reader_report | 같은목적 독자의 열람/실패 당사자문장 | 파일접근가능 |
| observed_at | 이번 조사 도구가 자료를 읽은UTC | 당시 사건일 |

날짜가 일단위이면 UTC timezone이 증명된 경우에만 그날00:00~다음날00:00의 구간으로 산술한다. timezone불명이면 날짜문구 그대로 유지한다. strict_first는 판목록 완전성과 사이배포 bytes검사까지 필요하다. first_observed는 이번 조사에서 처음 본 새판이며 최초출판과 다르다.

## 결측과 판정

- `미확인`: 알 수 없는 사실+이유+마지막 확인 위치+다음 필요한 원문. 빈시각은0일이 아니다.
- `해당 없음`: 같은목적 변경사건이 없거나 조건부분모가0인 질문. 미확인과 구별한다.
- `관측 실패`: 이 환경의404/403/timeout/원장누락 등 도구결과. 실제 과거 부재의 증거가 아니다.
- `확인 범위 안 유지`: 실제 읽은전후 자료에서 용도가 유지됨. 사이 모든날·실제실행 성공을 보장하지 않는다.
- `교체`: 같은목적에 부적합한 옛 경로와 적합한 대체를 원문으로 확인. 출처 원판 기록은 보존한다.
- `보류`: 목적·필요절·판·시계·교체효과 중 필수 증거가 부족함.

right_censored=true는 시작 사건이 확인되고 정한 관측종료까지 같은사건을 추적한 경우만. 시작일미상·서로다른목적·원문찾기실패는 검열로 만들지 않는다. 전체사슬0이면 그표본에서 적격쌍0일뿐 실제문제0이 아니다.

## 보기와 비용

L1=URL만, L2=URL+링크텍스트·목적·소비자판, L3=배포물/앵커/출처이력 추가. masked_decision은 제한된입력에서 먼저작성한 판정, adjudicated_decision은 뒤 원문대조 결과다. 동일 작업자가 이력을 이미 읽은 사후재판정은 retrospective로 구분한다. 기준판정미확인은 accuracy분모에서빼고 unresolved로 보고한다. 보류는 정답과별도이며 wrong_replace/wrong_keep는 반대행동의근거가 확인된 경우만.

read_count는 실제 기록된 원문열람/재열람 단위다. distinct source수와 URL수, query수와 후보문서수는 서로 다르다. 사람시간·API비용·독자클릭비율로 전환하지 않는다.
