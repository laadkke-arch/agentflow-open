# AF-RES-223 HANDOFF

- status: **PARTIAL**
- result_commit: c3895c3c8ad5a7be5c94cfa112ca89ac456c18b6
- result branch: work/research-af-res-223
- owned_path: docs/workstreams/research/AF-RES-223/
- source/integration start: f3895893e32e2c055cefde446d34f1467fa27b4c
- planning SHA: fc095c323d0177401d34f1daa7b4d1c529e2351f (223 항목은 이 판에 없고 착수판 RUNNING/attempt1/depends_on AF-RES-212).
- fixed dependency: AF-RES-212 DONE control result_commit 98cd710af3470b8908545ed2a542a5a1df7907c0; 해당 HANDOFF 내부 PARTIAL 및 이전 result SHA f4b08aa... 별도 기록. 212의 엄격 GOV 0/6에서 출발. 216–218 제외.

## 대표 결과
- [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/c3895c3c8ad5a7be5c94cfa112ca89ac456c18b6/docs/workstreams/research/AF-RES-223/RESULT.md) — 필수 두 표, Q1–Q7, 중요 약점 3건.
- [anchors.csv](https://github.com/laadkke-arch/agentflow-open/blob/c3895c3c8ad5a7be5c94cfa112ca89ac456c18b6/docs/workstreams/research/AF-RES-223/anchors.csv) — 12자리: Apply 6 (accept offer reference type/name, course/mode, phone/address), Register 2 (completed Apply-import draft CheckDetails의 training route/education phase), 결측 4.
- [returns.csv](https://github.com/laadkke-arch/agentflow-open/blob/c3895c3c8ad5a7be5c94cfa112ca89ac456c18b6/docs/workstreams/research/AF-RES-223/returns.csv) — 12자리 + 4 대조, test expectation/controller와 실제 관측 구분.
- [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/c3895c3c8ad5a7be5c94cfa112ca89ac456c18b6/docs/workstreams/research/AF-RES-223/sources.jsonl), [frame.csv](https://github.com/laadkke-arch/agentflow-open/blob/c3895c3c8ad5a7be5c94cfa112ca89ac456c18b6/docs/workstreams/research/AF-RES-223/frame.csv), [copy.md](https://github.com/laadkke-arch/agentflow-open/blob/c3895c3c8ad5a7be5c94cfa112ca89ac456c18b6/docs/workstreams/research/AF-RES-223/copy.md), [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/c3895c3c8ad5a7be5c94cfa112ca89ac456c18b6/docs/workstreams/research/AF-RES-223/SCOPE.md), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/c3895c3c8ad5a7be5c94cfa112ca89ac456c18b6/docs/workstreams/research/AF-RES-223/SELF_CHECK.md).
- source ledger 174 unique IDs / 76 unique counted work_ids: service components/templates 12 + shared gem 1; route/controller/translation etc 29; forms 13; actual service published spec files 12; standards/AT/design publisher 5; library list/records 4. Failed 11 excluded. Minimum 22 & categories met. Source timestamps are ledger creation times, individual first-open UTC not recorded. Frame 197 paths (160 Apply, 37 Register) metadata, not 197 full direct reads.
- Screen/anchor 4/6 conditional source-linked; 8/12 source-linked; 4/12 missing Register. Exact same-screen written click+return expectations 2/8 (A2); no actual execution, service screenshot, accessibility tree, or AT utterance public observation found; observed evidence count 0 (not evidence of no events). Library 2 distinct bib record IDs, holding/transaction verified 0/2. Do not count shared form/guide/placeholder as new strict slot.
- Main findings: same visible Change can point to different field/step; different calculated names can open exactly same full form (feedback); same route helper can differ by step (degrees), same title/format/author can be separate bibliographic records (2012/2009). Name alone is not identity; preserve target tuple and focus/mutation/return. Apply earliest inherited accept-offer displaced degree as later contrast. Register manual variant and feedback not used to fill missing. Actual accessible name remains conditional on rendered DOM and CSS.
- Important unknowns: register two more independent screens; actual role/name/field focus/route expansion and full value preservation; A3-2 follow-up address form, A3-1 return_to resolver; R1 final check return; exact duplicate same-field simultaneous link not established; library holding IDs and actual action request. Public releases endpoint [] both; tag-only list blocked by 400; fixed default branch SHAs not deployed versions. No independent review.

## 결과판 재열람 및 경계
At c3895c3c8ad5a7be5c94cfa112ca89ac456c18b6, fetched all 8 result files at exact ref, checked 174 ledger rows and 174 distinct IDs, 76 unique counted work_ids, 11 failure, 197 frame, 12 anchors (8/4), 16 returns, RESULT starts exact table1, table2, Q1–Q7 and last weakness 3 rows. Rechecked CSV and linked Markdown source references: 116 CSV refs, 80 linked Markdown refs, missing IDs 0; initial crude regex included source-line Lxx, corrected by bracketed source-link matching. Own self-check, not independent review. Compare API against f3895893e32e2c055cefde446d34f1467fa27b4c ahead_by 15: only eight owned files, outside paths empty, dot-control unchanged. No product execution, install, automated product verification, login, API key, or deploy. This HANDOFF is last standalone commit; result_commit identifies pre-handoff results rather than self-referential SHA.

## 다음 첫 행동 / Codex handoff (실행하지 않음)
1. Begin by reading frame.csv and anchors.csv at result_commit, then verify the fixed Register 37 paths and actual route callers; do not silently expand recruitment. Record any new eligible R2/R3 screen and first two distinct field destinations; if none under fixed rule preserve four missing. If expanding beyond check/review/summary names create separate cohort and explicit rule change. Use a clean approved test environment, no login to actual service.
2. Exact fixed inputs, commands for code worker (not run here):

    git clone https://github.com/DFE-Digital/apply-for-teacher-training.git
    cd apply-for-teacher-training
    git checkout a8244a455a02955bee016058484b06a485a0518d
    git ls-tree -r --name-only HEAD app/components app/views | grep -Ei 'check|review|summary' | sort
    git grep -n 'return_to_after_edit' -- app
    git grep -n 'address_line1' -- app/views/candidate_interface/contact_details
    bundle exec rails routes | grep -E 'accept_offer_references_edit_(type|name)|edit_course_choices_(which_course_are_you_applying_to|course_study_mode)|edit_(phone_number|address_type|address)'
    bundle exec rspec spec/helpers/references_path_helper_spec.rb spec/components/candidate_interface/references_review_component_spec.rb spec/components/candidate_interface/application_review_component_spec.rb spec/system/candidate_interface/course_selection/candidate_edits_course_choices_spec.rb spec/system/candidate_interface/entering_details/candidate_entering_contact_details_spec.rb
    cd ..
    git clone https://github.com/DFE-Digital/register-trainee-teachers.git
    cd register-trainee-teachers
    git checkout 76099e8258aec4695442d7eccc98a506844668ca
    git ls-tree -r --name-only HEAD app/components app/views | grep -Ei 'check|review|summary' | sort
    git grep -n 'trainee_editable?\|save_as_origin!\|last_origin_page_path' -- app/controllers app/helpers
    bundle exec rails routes | grep -E 'check_details|training_route|course_education_phase|feedback|personal_details'
    bundle exec rspec spec/features/user_feedback_spec.rb spec/view_objects/mappable_field_row_spec.rb spec/features/trainee_actions/edit_trainee_training_route_spec.rb spec/features/form_sections/teacher_training_data/edit_course_education_phase_spec.rb spec/features/form_sections/personal_and_education_details/edit_personal_details_spec.rb

Use repo README setup prerequisites only in an already authorized environment; if dependency/DB/browser missing report blocked with exact error, no unauthorized install. For gem source use x-govuk/govuk-components v6.6.0 commit 3dbcb727a2916b3c92a6eee7f9daca1e91d401dc and verify lockfile package checksum if accessible.

3. Fixtures to record (synthetic, no real candidate): A1 valid offer, not_requested_yet reference with name/type present; second fixture same name different reference ID, requested status; A2 unsubmitted course both study modes and multiple/single sites; A3 editable complete phone/address, UK/non-UK and missing postcode variants. R1 Apply-import draft, course_details complete expanded, editable, non-early-years, training_route and phase present; manual draft personal name/DOB and early-years/readonly/incomplete variants; feedback session saved satisfaction/suggestion/name/email. At each selected anchor record ordered DOM outerHTML, visible text, href including arguments, role/AX name/description, focus immediately after click, exact input name/id, initial value, changed value, unchanged values, validation, return URL and focus after Save and continue/Back. Explicitly assert other answers preserved except legitimate dependent site/course changes. Test links list NVDA+F7 and sequential/tab (browser, NVDA version, OS, settings, actual speech transcript, distinct from AX computed). Test same-name collisions and same-href JS focus; failure if expected name or destination/return differs. Use local test server, not live authentication.
4. Library: L01 list page L460–481; record links S93C2582762 and S93C2333799. Public read-only DOM inspect whether hold control has record/holding identifier and name role; public bib/holding mapping only. If transaction requires authentication, stop and report required approved sandbox/test account; no actual hold submitted. Record whether two IDs share real hold group. 
5. Repo scope/validation for reviewer (not local-run here; compare API already checked):
    git fetch origin work/research-af-res-223
    git show c3895c3c8ad5a7be5c94cfa112ca89ac456c18b6:docs/workstreams/research/AF-RES-223/RESULT.md
    git diff --name-only f3895893e32e2c055cefde446d34f1467fa27b4c c3895c3c8ad5a7be5c94cfa112ca89ac456c18b6
    git diff --exit-code f3895893e32e2c055cefde446d34f1467fa27b4c c3895c3c8ad5a7be5c94cfa112ca89ac456c18b6 -- docs/automation/dot-control.json

## 색인 반영 제안
운영자/통합 작업만 dot-control 갱신: AF-RES-223 PARTIAL; result_commit c3895c3c8ad5a7be5c94cfa112ca89ac456c18b6 (또는 마지막 HANDOFF commit으로 기록하는 운영 규약이면 해당 SHA 별도 확인); branch work/research-af-res-223; acceptance evidence RESULT/SELF_CHECK/anchors/returns/sources/frame + HANDOFF; next_action Register 4 missing slots 및 fixed-fixture DOM/AX/return checks. DONE/12/12/실측 성공으로 색인하지 말 것. 본 worker dot-control 수정 안 함.
