# AF-RES-219 HANDOFF

상태 **PARTIAL** — 결과는 GitHub에 커밋됐으나 지명 원문 1자리 결측 및 사전 순차 예측 실패. 실제 전달/런타임/독립 검토 미실시.

- 시작 기준: chore/workspace-foundation f3895893e32e2c055cefde446d34f1467fa27b4c; 계획판 fc095c323d0177401d34f1daa7b4d1c529e2351f 대비 5 ahead, 0 behind, dot-control.json만 변경. 현재 219 RUNNING, depends_on 208 중앙 DONE, 고정 인계 4b700b6a8ab597f7561508a7feb2f94035220996의 자체 상태 PARTIAL. 216–218 제외. 작업 브랜치 work/research-af-res-219 생성. 
- **결과판 SHA** (이 인계 직전): b6ee9d2ed8592c2ef1fb10790616c60628c2a64b. 이 인계는 별도 마지막 커밋. 대표 파일: [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/b6ee9d2ed8592c2ef1fb10790616c60628c2a64b/docs/workstreams/research/AF-RES-219/RESULT.md), [sources](https://github.com/laadkke-arch/agentflow-open/blob/b6ee9d2ed8592c2ef1fb10790616c60628c2a64b/docs/workstreams/research/AF-RES-219/sources.jsonl), [SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/b6ee9d2ed8592c2ef1fb10790616c60628c2a64b/docs/workstreams/research/AF-RES-219/SELF_CHECK.md), requests.csv/settings.csv/routes.csv, SCOPE.md/body_freeze.md/counterexamples.md.
- 결과판 원격 재열람: 9개 파일 모두 fetch_file 성공, JSONL parse 49행, included 35 고유 work, 15 고유 lineage(공식 문서·고정 코드 계보 포함; 독립 실험 수 아님), 유형 N3/D5/E18/F4/G5, failed 12행, 나머지 미산입 2행. RESULT 첫 표·둘째 표 헤더, Q1–7, 최종 약점 표 3행 확인. requests 4 지명 + 3 통제 존재. base→결과 9 commits ahead, 0 behind, 변경 파일 9개 모두 owned_path. dot-control 미변경. 문서 재열람·형식/카운트 확인이며 코드/CI/제품 테스트가 아님.
- 커밋: ① b1c0ff881efa92aed29415ef530cc3b513315044 scope; 9f2d6cf5206a52ae327a03e23cbea7152aea5d4f body freeze(비블라인드); ② a368b3049871478a1f4ebdccb8f80d0d1b68178a ledger; ③ 27022253f710a04589cb7b2af595365a9c57ece6 requests, 3cc5415c60becda99dcd949e23c76af64bd93f01 settings, c1ad4191e8aa491eeb2b3c159d60ab31dcf77dfd routes; ④ 23fc39b33ade6cc073c2324a4283733bb4a8d63e 반례; ⑤ 489197b7a97a857cd8183134c05592b840a705c8 RESULT, b6ee9d2ed8592c2ef1fb10790616c60628c2a64b SELF_CHECK. 필수 표 Markdown은 ③ CSV 이후 ⑤에서 최초 커밋하여 요구 순서와 차이가 있다.

## 핵심
- scope(한 topic/분류/사이트), actor(개인/관리자), channel(메일/화면/browser), event(mention/PM/first/all), 유지 조건을 분리. 이미 명시된 축을 되묻지 말고 첫 설정을 바꾸는 미확인 축에서만 한 질문. 즉답/두 조건부 링크/한 질문의 대안을 남김.
- v3.3.0 고정판: topic mute는 mention도 막음; unwatch는 tracking; email_level, PM, digest, MLM 별개. MLM의 global implicit default mute + positive topic/category/tag row(regular=1 포함 후보)와 explicit muted category/topic 제외는 다른 처리. 관리자 기본값 existing update는 old-value match와 category row 유무 기반이며 개인 명시 선택 provenance가 동일값에 보장되지 않음. 과거 N1 실제 원인 확정 아님.
- GitHub repo unwatch/ignore/conversation unsubscribe의 mention 재구독 예외는 별도 서비스; email/On GitHub 문서의 표현 긴장 및 실제 보존 미확인.
- 지명 본문 3/4, 62748 가이드(자연 요청 제외), 116393 라벨 개선(실제 중단 요청 아님), 229919 운영자 제보, 280651 미확인. 최초판 0/4. N1 동일 수신자 변경→다음 알림 완결 0/1, 2 범위 밖, 1 결측; 통제 3개 합성·실행 0. 최소 22 전체는 충족하였으나 지명 4개 하한 미달. URL /1 및 /1.json 실패, 검색/전체 페이지 답글 노출로 사전 질문 예측 불성립. 62748은 후속 canonical 직접 확인. 정확한 개별 UTC 열람 시각 미기록. 독립 검토 없음.

## 다음 첫 행동
1. 280651 공개 canonical slug/첫 글/공개 revision 확보부터. 예: https://meta.discourse.org/t/280651, 공개 topic metadata의 canonical URL, post 1 permalink 및 공개 revision history. 일반 접근 거부/삭제면 우회하지 말고 결측 유지. 별개 작업자가 답글 보지 않은 상태로 4 지명 글 최초 공개 판(없으면 현재 #1)만 읽고 즉답/조건부 2 링크/1 질문을 새 SHA에 고정한 뒤 응답 비교. 원문 저자와 타인 후속을 구분. 
2. 229919의 실제 발생 당시 Discourse 판, mail type, affected user의 이전/이후 topic/category/tag rows 및 동일 user 다음 메일 공개 로그가 있다면 읽기. 개인 로그/실계정 접근 승인 없이 하지 않음. F3의 개발자 fix https://github.com/discourse/discourse/commit/664feca199cf1f4c76945a48a4d5b964de7d064d 원패치 확인; N1 category 사건과 혼동하지 말 것. GitHub G1의 Email/On GitHub 실제 동작 확인은 별도 공개 재현 또는 허가된 시험.

## Codex 인계: 실행할 명령과 입력 (여기서는 미실행)
이미 의존성이 준비된 격리 Discourse 시험 환경이 있을 때만 다음; 새 설치·외부 발송은 별도 승인.
```sh
git clone https://github.com/discourse/discourse.git /tmp/af219-discourse
cd /tmp/af219-discourse
git checkout --detach 5bbdc8a813caf55ab3147ac65b5ffafb5e0aab90
git rev-parse HEAD
git grep -n 'watching_topic\|mute_all_categories_by_default' -- app/models/user.rb app/jobs/regular/notify_mailing_list_subscribers.rb
git grep -n 'update_existing_user\|previous_value' -- app/controllers/admin/site_settings_controller.rb app/services/site_setting_update_existing_users.rb
bundle exec rspec spec/jobs/notify_mailing_list_subscribers_spec.rb spec/services/post_alerter_spec.rb spec/requests/email_controller_spec.rb spec/models/category_user_spec.rb spec/models/topic_user_spec.rb
```
- 기존 spec은 E15/E16/E10/E8/E7의 실제 검사를 재현. 실패 시 환경/판/명령 및 출력 기록, 기대값을 관측으로 바꾸지 말 것. DB/mail backend는 격리 fake/test sink, 실제 수신자 이메일 사용 금지.
- 신규 합성 fixture(별도 Codex 승인 경로에서): 사용자 A MLM enabled, site disable_mailing_list_mode=false, frequency=1, mute_all_categories_by_default=true; 같은 접근 가능 category/topic/post, muted user/tag 없음, rate/bounce gate 통과. A1 topic row 없음 (기대 MLM 0); A2 topic row normal=1 (코드 추론 기대 1, 직접 기존 시험 미확인); A3 topic watching=3 (기대1); A4 topic watching=3 + explicit category mute=0 (기대0); A5 explicit topic mute=0 + category watch=3 (기대0). 각 post별 job 및 enqueue/actual test mail count/notification count/recipient fixture 기록. 결과가 다르면 E12/E17 판정 변경. Own echo frequency1 vs2도 분리.
- 개인 B topic normal/tracking/watching/muted 각 경우 @mention, ordinary reply, first post 실험; E16 expected mention +1/1/1/0, first post는 category WFP로만 설정. Email never/MLM off 및 PM/digest 별도 선택; screen notification row와 fake mail count를 둘 다 비교. E10 unsubscribe topic=tracking vs mute=0 vs all four values. 해당 topic만 이메일 끄고 화면의 모든 event를 유지하는 독립 제어의 존재 여부 확인.
- 관리자 C old default email_level=1, new=2; 사용자 U1 명시 선택 없는 1, U2 명시 선택 1, U3 개인 0, U4 신규, U5 staged. 기존 update flag false/true 각각 별도 fixture로 초기화. U1/U2 same value match, U3 다른 값, U4 new default; category addition existing row/absent row 및 removal old level 일치 여부. 실제 UserOption/CategoryUser/TopicUser 및 notifications_reason_id 전후 비교, E18 expected old-match로 U2도 변경 후보. 명시 선택 출처를 별도 식별하는 관측이 있으면 판정 수정.
- GitHub G1/G2/G3/G4의 채널 설정/재구독은 공개 문서 추가 확인 또는 허가된 테스트 계정에서만; 실계정 설정 변경 금지. 질문 UI/제품 구현은 별도 작업.

색인 반영 제안(직접 수정하지 않음): AF-RES-219 PARTIAL — 알림 요청의 scope/channel/actor/event/keep 최소 분기, implicit default vs explicit mute, existing old-value update provenance, GitHub resubscription 예외. RESULT/requests/settings/routes 및 반례, 35 direct works, 지명 280651 결측 및 비블라인드. 최종 설계 단정 금지; 208 원래 identity vs display state와 연결 가능한 비교.
