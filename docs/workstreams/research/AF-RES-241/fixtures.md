# AF-RES-241 로컬 입력

동일 Git SHA와 빌드 이미지는 [environment.json](environment.json), 이미지-원본 해시는 [Apply](receipts/bootstrap/apply-source-image-match.json)와 [Register](receipts/bootstrap/register-source-image-match.json)에 있다. Rails 8.1.4.1, Ruby 4.0.10, test, I18n en이다. 사이트 언어와 Chromium en-GB 및 문서 lang은 별도로 확인했다. upstream이 빌드한 JS/CSS를 사용했고 이미지의 Node와 저장소가 선언한 Node 버전 차이를 environment.json에 남겼다.

| 화면 | 공개 factory·역할·상태 | 고정 초기값 및 저장 입력 |
| --- | --- | --- |
| A1 Accept offer | Apply candidate, completed_application_form, offered application_choice, 두 not_requested_yet reference. CandidateHelper의 One Login mock 후 정상 accept route | Morgan Example academic, Taylor Example professional. Morgan의 Type을 professional 또는 Name을 Morgan Edited로 하나씩 변경. 연락처와 관계값은 합성. offer 수락 버튼 자체는 사용하지 않음 |
| A2 Course review | Apply candidate, 같은 provider의 open courses, unsubmitted application_choice. 두 모드와 각 두 site 조건 | AF241 Mathematics (T241), full time, Original Site. 두 코스 funding_type=fee 고정. A2-1 AF241 English (T242), full time 단일 site를 같은 Original Site에 연결. A2-2 part time, site 질문이 나오면 같은 site의 part-time option을 유지 선택 |
| A3 Contact review | Apply candidate, 편집 가능한 unsubmitted application_form, 완료된 UK 주소·전화·거주 응답 | 07700 900241 → 07700 900242. 주소 24 Example Street → 25 Example Street, line2 Test building, London, SW1A 1AA, GB. UK 및 since_birth=yes 유지 확인. 오류 재생은 전화에 `not a phone` |
| R1 Check details | Register DfE sign-in mock의 소속 provider, trainee :draft / :with_apply_application / :provider_led_postgrad 및 course_details progress | Fixture Trainee, non-early-years, secondary, Mathematics, 11–16, full_time, 2026-09-01~2027-07-31, course_uuid nil, no_initiative, 지원금 플래그 false, UK nationality, sex_not_provided, AF241-LOCAL, 과목 매핑 고정. R1-1 school_direct_salaried로 변경, 안내된 후속 폼에 기존 값 재입력. R1-2 primary로 변경, 필요한 경우 Primary with mathematics/5–11 종속 선택. 실제 변경과 후속 재입력은 영수증에서 구분 |

합성 식별 이메일은 example.test. A2 fixture의 두 코스, 라우트 변경 시 재입력 및 R1 새 단계의 종속 값은 작업자가 결정한 테스트 입력이다. 두 서비스의 일부 공개 factory 기본값과 DB 식별자는 실제 생성값이며 각 JSON의 resource 및 before 모델로 식별한다. Apply는 기존 Rails system helper의 mid-cycle 시계, Register는 실행 시각의 테스트 학년과 테스트에 넣은 날짜를 사용한다. A2 기존 작성 시험은 fixture와 코스명이 다른 upstream 제공 시험으로 별도 실행했다.

저장과 즉시 Back마다 공개 factory로 독립 레코드 및 초기 세션을 만들고, Apply의 기존 transactional fixture와 Register의 기존 DatabaseCleaner 설정을 사용한다. 앱의 신원 제공자는 테스트 mock을 사용한다. 모델 저장·route·render·CSS·JS는 두 공개 앱의 원래 코드이다. Chromium은 별도 프로필이고 호스트와 컨테이너 사이의 두 방향 통신은 loopback→Unix socket→loopback이다. DB·캐시 네트워크는 로컬 internal이다.

최종 입력에서는 Ruby와 Faker의 seed를 여정별 241로 고정했다. 초안 실행의 course funding 샘플에 따라 A2 fee 설명 행이 달랐고 R1의 degree 등 기본값도 달랐다. 최종 실행에서는 S/B 초기 요약행 전체를 비교해 8쌍 모두 동치임을 확인했다. 새 레코드·새 세션에서 실제 생성된 ID와 시각은 별도 값이다.
