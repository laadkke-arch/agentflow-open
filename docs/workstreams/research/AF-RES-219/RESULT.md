| 사건 | 원작성자 요구 | 멈출 알림 | 유지할 알림 | 원문 주소·절 | 미확인 |
|---|---|---|---|---|---|
| N1 · 229919 | 운영자: 전체 분류 기본 mute와 MLM인데 일부 주제 메일이 옴 | 예상 밖 게시물 메일 | 최초글 미명시; #8에서 본인 글 메일 보존 강조 | [229919 #1](https://meta.discourse.org/t/notifications-from-muted-categories-when-mailing-list-mode-is-enabled/229919/1); #8,10,13,15 | 설치판, 메일 유형, 개인 상태 및 다음 수신 |
| N2 · 62748 (가이드) | 원작성자 자연 제보 없음; unsubscribe 옵션 설명 | 선택한 topic, category, MLM 또는 전체 구독 이메일 | 선택지별 tracking/다른 topic 가능 | [62748](https://meta.discourse.org/t/unsubscribe-from-a-topic-using-email/62748) L13–60 | 최초판, 실제 수신은 범위 밖 |
| N3 · 116393 | RGJ: 분리된 PM/일반 메일 설정 라벨이 watched/tracked 분류 관련 알림을 명확히 설명하도록 수정 | 중단 요청 없음 | 기존 전달을 바꾸라는 요구 없음 | [116393](https://meta.discourse.org/t/confusing-wording-for-email-notification-settings/116393) #1,5,7 | 최초판, 원작성자 수신 변화 |
| N4 · 280651 | 미확인 | 미확인 | 미확인 | [280651](https://meta.discourse.org/t/280651) 본문 접근 실패 | 저자·역할·판·요청 전체 |
| C1 · 관리자 기본값 (합성) | 새 가입자와 기존 사용자 범위 선택 | 지정 기본값에 따름 | 기존 사용자 선택 가능하면 보존 | [285619](https://meta.discourse.org/t/configuring-default-notification-settings-for-users/285619) D1; E14,E17,E18 | 실행·다음 수신 |
| C2 · 개인 상속 예외 (합성) | 개인이 변경한 값 보존하면서 default 변경 | 기본값 변경 대상 | 명시 선택(이전 기본값과 같은 값 포함) | E14,E18; D5 | 값 출처 구분 및 실제 갱신 |
| C3 · 단일 topic/전체 이메일 (합성) | scope와 channel의 선택 | 한 topic 알림 또는 전체 구독 이메일 | 다른 topic/화면 멘션 | [62748](https://meta.discourse.org/t/unsubscribe-from-a-topic-using-email/62748) N2; E10,E16 | 실행·화면 보존 |

표 1 행 단위: 지명 원출전 자리 4개 및 사전에 지정한 합성 통제 3개. 실제 수신 관측으로 합성 행을 산입하지 않는다.

| 입력 조건 | 첫 링크·설정 | 묻는 한 문장 | 다른 답이면 바뀔 절 | 관측과 한계 |
|---|---|---|---|---|
| N1 관리자, MLM 유지, 예상 밖 주제 메일 | [D1 관리자 기본값](https://meta.discourse.org/t/configuring-default-notification-settings-for-users/285619) → E12/E17 | 전체 분류 기본 mute인가요, 해당 분류에 명시적으로 mute를 설정했나요? | 암묵적 기본 → E17 positive row; 명시적 → E12 explicit exclusion; 이메일 유형도 확인 | #15 방문 후 normal row; 2022 환경 미확인, v3.3.0은 비교 |
| N2 문서의 단일 주제/전체 이메일 선택 | [N2 unsubscribe](https://meta.discourse.org/t/unsubscribe-from-a-topic-using-email/62748) | 이 주제만 멈출까요, 사이트 구독 이메일을 모두 끌까요? | 단일 unwatch/mute ↔ all email 4값 | E10 시험 기대; 안내 문서이지 자연 제보 아님 |
| N3 PM vs 일반 알림 라벨 | [D1 Emails](https://meta.discourse.org/t/configuring-default-notification-settings-for-users/285619) 및 [N3](https://meta.discourse.org/t/confusing-wording-for-email-notification-settings/116393) | 개인 메시지 메일인가요, 주제·분류 구독 메일인가요? | PM email_messages_level ↔ 일반 email_level | 라벨 요청 자체는 즉답 가능; 질문은 가상 opt-out에만 적용 |
| N4 본문 결측 | 추천 보류 | 어디서 멈추고 무엇은 계속 받나요? | 메일만 D1 Emails ↔ 특정 topic 종 D1 notification levels / D2 | 실제 원요구 아님; 평가 제외 |
| C1 신규/기존 관리자 기본 | [D1 default](https://meta.discourse.org/t/configuring-default-notification-settings-for-users/285619) | 새 가입자만인가요, 기존 사용자도 바꿀까요? | 신규 초기화 E1/E17 ↔ 기존 update flag E14/E18 | 정책/코드; 관측 아님 |
| C2 기존 선택 보존 | [E18 기존 사용자 업데이트](https://github.com/discourse/discourse/blob/5bbdc8a813caf55ab3147ac65b5ffafb5e0aab90/app/services/site_setting_update_existing_users.rb) | 기존 개인 선택은 이전 기본값과 같더라도 보존해야 하나요? | 값 일치 갱신 허용 ↔ 자동 업데이트 금지/별도 provenance 정책 | 같은 값에 명시 출처 판정 없음 |
| C3 한 주제만 줄이기 vs 모든 이메일 | [N2](https://meta.discourse.org/t/unsubscribe-from-a-topic-using-email/62748) | 한 주제의 일반 답글만 줄일까요, 모든 구독 이메일을 끄고 화면 알림을 남길까요? | unwatch/normal ↔ all email (MLM/PM/digest 확인) | 멘션 유지면 mute 금지; 실제 보존 미실험 |
| C3b 전달 채널 비교 (C3 세부 행) | [D1 Emails](https://meta.discourse.org/t/configuring-default-notification-settings-for-users/285619) | 메일만 끄고 화면 멘션은 남길까요, 해당 주제 멘션까지 끌까요? | email_level/MLM ↔ topic mute | E16 기대; 특정 topic의 email-only 전용 제어는 미확인 |

표 2 행 단위: 동일 자리별 제안 경로, C3 세부 대조 1행 추가. 모두 사후 구성 또는 합성; 답글 이전 예측 평가로 간주하지 않는다. 원자료는 sources.jsonl, 세 CSV의 ID로 연결된다.

## Q1. 원요구의 명시 범위
N1 #1의 주체는 관리 운영자, 전체 분류 default mute+MLM, 일부 thread mail을 문제로 삼는다. 유지 대상 own mail은 #8에서 확인되므로 최초글에 소급하지 않는다. N3 #1은 v2.3.0.beta6의 email_messages_level 및 email_level 분리 뒤 표시 문구 변경 요구로, 실제 알림 중단 요구와 다르다. #5는 watching 카테고리/first post/topic, #7은 tracking 단독 이메일이 아니라는 타인 정정. N2는 공식 사용법이며 최초판(2017 이후 편집) 미확인. N4 본문 미확인. 따라서 지명 자연 글 2건 확인(그 중 직접 알림 중단 문제 1, 문구 개선 1), 가이드 1, 결측 1. 제목이나 답글만으로 N4 분류 금지. requests.csv와 N1–4. 오판: 초기 보존 의도를 후속에서 역추정하거나 문구 제안을 delivery 버그로 분류하는 것.

## Q2. 한 질문이 첫 링크를 바꾸는 조건
최소 입력은 주체(본인/관리자), 대상(토픽·분류/태그·사이트), 채널(메일·화면·브라우저), 보존 event(mention/PM/first/all) 중 이미 명시된 것들을 제거하고 남은 **첫 제어를 바꾸는 축**이다. 예: 사이트의 모든 구독 이메일이라고 명확하면 N2 all/개인 이메일 환경설정 즉답, PM 여부만 모호하면 조건부 링크 두 개; 화면 mention 유지와 토픽 mute는 동시에 충족 못하므로 질문 한 번의 가치가 큼(E16). N1은 scope가 아니라 implicit/explicit 상태와 MLM 보존이 링크를 뒤집는다. N3은 원래 라벨 질문에 재질문 불필요, 라벨을 opt-out으로 해석할 경우 PM/일반 분기. N2 가이드의 두 선택지는 실제 이용자가 응답한 자료 아님. routes.csv. 사전 범위/일반 예측을 먼저 커밋했으나 body-only 접근 실패, 일부 답글 먼저 노출되어 사전 순차 판독은 불성립. 사용자의 실제 응답 및 경로 성공 0회 실험.

## Q3. 제어의 권한·단위·예외
settings.csv S1–S15. D1/N3/E1/E4: email_level(일반)과 email_messages_level(PM)은 0 always,1 away,2 never; 기본 1/0. D3/D4 digest는 또 별개. E4 기본 MLM false/disable true, E5 번역에서 MLM이 summary/email 설정을 우선, E12 적격 게시물 처리; muted user/topic/category/tag와 권한 필터, no echo frequency2. E13: topic enum 0 mute,1 normal,2 tracking,3 watching; category/tag에는 4 first post. D1: normal/track은 reply/mention 유지, tracking에 count, watching 모든 새 답글, WFP 새 topic 첫 글만(이후 읽기/답글/수동 선택 영향). E11/E16 topic mute면 직접 mention도 억제. D2/E5 종 dismiss=읽음 처리, browser push는 별개. N2/E10 email 링크 unwatch→tracking, mute→mute, category unwatch→row 제거, all→digest false/두 email level never/MLM false. E9 키/로그인 검사. 특정 topic의 mail-only 억제와 모든 화면 이벤트 유지가 독립적으로 가능한 제어는 확인 못했다. 오판: dismiss를 수신 중단으로, tracking을 all replies로, WFP를 topic 단위로 안내하는 것.

## Q4. 초기값과 기존 개인 상태
고정 Discourse v3.3.0 commit 5bbdc8a813caf55ab3147ac65b5ffafb5e0aab90 (tag peel; 현재 문서 및 2019/2022 사례의 실제 판 아님). E1 신규 UserOption set_defaults; E17 after_create category default rows(비 staged). E14 admin update_existing_user 플래그 없으면 신규 default 변경과 기존 값 일괄 변경 구분. E18 email 기존 갱신: 이전 값과 같은 기존 옵션만 변경; 다른 값 보존 후보. **같은 값이 개인의 명시 선택인지 구분하는 provenance 조건 없음**. 카테고리 추가는 existing row 없는 nonstaged real users, 제거는 이전 수준과 일치한 행 삭제 및 auto-watch reason 조정. E3/E8 category watch/track automation도 기존 정상 row를 승격할 수 있다. D5 그룹 가입 동작(2020 공지)은 상승/개인 override, 탈퇴 시 그대로라는 별개 정책; 현재판 검증 아님. 따라서 default를 매 수신마다 계산하는 live inheritance라고 설명 금지. C1/C2는 합성 비교이며 실행 관측 0.

## Q5. 요청→변경→다음 알림
- N1: artur #1(2022-06-14) 문제 → #8 own mail 보존, #10 watched/normal·staged, #13 구독하지 않은 분류, #15(7/12) 방문 후 없던 topic row가 normal=1이 되는 관찰 및 staged 사례, #16–17 응답. 동일 수신자, mail type, 설정 변경 뒤 다음 메일의 연결이 끊긴다. 설정이 실제 바뀐 기록(일부 row 관찰)과 전달 결과 구별.
- N3: RGJ #1(2019-04-30) 문구 요구 → #5 예시 보완 → Jonathan5 #7 tracking 정정 → Simon_Manning #11(2021) 다른 운영자의 로컬 문구 변경. 원작성자 설정/수신 결과 없음; 이 요청 자체에는 수신 결과 요구가 없음.
- N2 문서, N4 미확인. F1(2023) 관리자 WFP 권한 제안, 원작성자 변경·수신 없음. F2(2021) PM 용어 정정, #10 타인 wiki edit 화면만 보고; 원작성자 성공 아님. F3(2016) muted user MLM 재현 및 개발자 fix 링크, patch와 저자 재시험 미확인. F4(2021) 태그 수정 뒤 일부 메일 로그 및 타인 계속 수신 보고, 본인 이후 수신 없음 보고이나 설정 전후·동일 알림 유형 불명. 이들을 N1 해결의 대리 증거로 쓰지 않는다.
- 지명 4자리 중 실제 중단 문제 1건, 그 동일인 설정 변경→다음 전달 관측 완결 0건/1건; 나머지 2 범위 밖(가이드/문구), 1 결측. 별개 F1–4 완결 chain 미확인. 정책·시험 expectation은 수신 실측으로 세지 않음.

## Q6. GitHub 대조
G1 채널 Email/On GitHub, participating/watching. G2 참여·mention·assign/review가 구독을 만들고 unsubscribe 뒤 mention/team으로 재구독 가능. G3 repo unwatch는 참여/mention과 공존, ignore는 mention까지 억제. G4 개별 issue/PR custom(merge/close/reopen). Discourse normal vs mute 및 email delivery 축의 유추는 가능하나 GitHub repo ignore/자동 재구독을 Discourse topic에 동일 적용 금지; 분류/태그/사이트 초기화와 대응하지 않는 기능. G1 inbox에 두 채널을 켜라는 설명과 email을 deselect하고 On GitHub를 남기는 절이 공존하여 실제 inbox 보존 미확인. G5 2025-11 발표의 commit mention 중단 예정(12/8)과 이용자 의견: regs01 이메일 중단·구독 유지, Marcono1234 외부 기여 commit mention 가치. 이견을 별개 목표로 표시; 실제 전환 완료/사용자 다음 수신 미확인. 첫 링크는 repo watch인지 conversation인지 전달 채널인지 구분하며, 별도 서비스로 제시.

## Q7. 반증 및 오판 경계
(1) 화면 mention 유지 + 이메일 중단: E16에서 mute는 mention도 없애므로 탈락, 이메일 환경설정과 MLM/digest/PM 확인. (2) 한 topic 해제: unwatch=tracking과 mute를 구분, global unsubscribe는 다른 topic의 이메일을 잃음. (3) MLM+mute: E12는 explicit category/topic mute를 직접 제외하나 global default mute는 E17 watching_topic positive row>0 검사; normal=1도 포함 후보. 따라서 N1 같은 default mute+normal row는 예상 밖 메일 후보, explicit muted category+watched topic은 E12 제외. E15 직접 회귀시험은 watched row에서 1, explicit mute에서 0 기대; normal row 조건은 별도 실험 필요. N1의 2022 버그 원인 확정 아님. (4) 관리자 default 변경: E18 이전 값 일치/row 부재 판정은 실제 개인 의도 보존과 다름; old default와 같은 명시값도 바뀔 수 있다. C1/C2의 반전은 update flag/기존 값 provenance. 자세한 반례는 counterexamples.md. 실측·독립 검토 없음.

## 추가 해석: 첫 링크 설계 대안과 비용
일반 참여자는 좁은 범위의 변경을 선호할 수 있고, 운영자는 신규와 기존 사용자 적용이 중요하다. 메일 전용 사용자는 MLM own echo를 보존해야 할 수 있으며, 화면 사용자는 mention 유지가 중요하다. 이를 단순 keyword '알림 끄기'로 합치지 않는다. 추천은 (a) 명시 범위에 즉답 + 잔존 알림 설명, (b) 두 조건부 링크로 사용자가 직접 고름, (c) 한 질문으로 보존 조건을 확정. (a)는 빠르지만 숨은 override 손실, (b)는 왕복 없음/읽기 비용, (c)는 왕복 1회/잘못된 전역 변경 방지. 질문을 모든 요청에 강제하지 말고 대상/채널/보존 중 다음 설정이 바뀌는 축에만 사용. N1같이 구현 예외가 개입하면 일반 가이드+고정 코드의 두 층을 분리. 추천 모델의 정답률·질문 비용의 실측은 없음.

자료 분모: 35개 직접 고유 저작/파일(49 ledger rows). 지명 3/4, 공식 5/4, 코드 18/6, 별개 요청 4/4, GitHub 5/4. 총 하한 22 충족이나 지명 1 미달. 코드 파일들은 동일 계보, G1–4는 GitHub 공식 계보; 지명 자연 글 N1,N3 및 F1–4 6개 Discourse topic, G5 한 공개 토론(참여자 다수지만 한 work); 이 수를 독립 실험 수로 해석 금지. 계획 지명 4+통제 3, 관측 본문 3, 지명 결측1, 합성 통제3. 최초 수정판 확보 0/4, 응답 이전 블라인드 판독 불성립, 런타임/검사/독립 검토 미실시. 핵심 판별 미완: PARTIAL.

| 중요한 불일치 또는 약점 | 영향을 받는 판단 | 다음에 볼 특정 자료·검사 | 판정이 뒤집힐 관측 |
|---|---|---|---|
| 280651 결측, 최초판 및 사전 블라인드 미확보 | 지명 4건의 질문 필요성 및 자연 요청 분모 | canonical slug 첫 글/공개 revision, 독립 작업자가 답글 비노출 본문만 코딩 | 명시 채널/보존 조건이 현 분기와 다르거나 280651 가이드로 판명 |
| 229919 실제 메일 유형·판·동일 수신자 다음 수신 없음; implicit/explicit 비교는 v3.3.0 | MLM 예외 원인과 첫 진단 링크 | E12/E15/E17 고정판에서 implicit default+normal row vs explicit muted category+watched topic, 실제 관련 버전/로그 | normal row 후보가 발송되지 않거나 explicit mute에서 MLM 발송; 해당 메일이 MLM이 아님 |
| 기존 값 일치와 개인 의도 보존 불일치; GitHub inbox 문구 긴장 | 관리자 업데이트 안전성 및 채널 분리의 전이 | E18/E14의 old-value match fixture 및 G1 두 설정의 공개 재현 기록 | 동일값 명시 선택이 별도 보호되거나 email 해제 시 GitHub inbox가 실제 비활성 |
