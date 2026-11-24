# SELF_CHECK · 동일 작업자 자기검산 (독립 검토 아님)
원격 RESULT 기준판 6d5f4cab3b8b75c0812dcb80deb85e7799dc864e에서 원장들을 재열람하고 JSON/CSV 행 및 식별자를 도구로 재집계했다. 실행 환경은 웹 도구/커넥터; 제품·계정 실행 및 독립 조사자 검증 없음.

| 질문 | 주장 또는 미확인 → 출처·위치 | 원장 행·분모 | 반증/판정을 바꿀 최소 증거 |
|---|---|---|---|
| Q1 | P/S/E/GA/O 별도; planned end≠실제 완료, rollout rollback: [A05](https://github.blog/changelog/2025-01-13-evolving-github-issues-public-preview/) L22,41–75; [A07](https://github.blog/changelog/2025-02-26-increased-items-in-github-projects-now-in-public-preview/) L18–32; [A14](https://workspaceupdates.googleblog.com/2024/02/import-convert-excel-files-into-client-side-encrypted-google-sheets-now-generally-available.html) L75–96; [A15](https://workspaceupdates.googleblog.com/2024/02/manage-comments-faster-google-docs-sheets-slides.html) L65–99; [A17](https://workspaceupdates.googleblog.com/2025/05/use-gemini-google-sheets-advanced-actions.html) L65–86,108–125; [A18](https://workspaceupdates.googleblog.com/2025/01/generate-charts-and-insights-with-gemini-google-sheets.html) L94–120; [O09](https://workspaceupdates.googleblog.com/2023/12/easy-access-to-people-documents-blocks-in-google-docs.html) L65–98, Update Jan24/Jan30 | rollouts 17개; E15/16 집단 전이; 자연 20자리 중 6잠정·14결측 | 원 공지의 첫 판·변경 이력과 대상 집단의 실제 완료 시점; GA와 완료가 동시에 검증되는 운영 기록 |
| Q2 | 당시 CSE 에디션·관리자 설정 필요, preview 승인 별도; 설정 기본값/강제 구분: [A14](https://workspaceupdates.googleblog.com/2024/02/import-convert-excel-files-into-client-side-encrypted-google-sheets-now-generally-available.html) L75–96; [A17](https://workspaceupdates.googleblog.com/2025/05/use-gemini-google-sheets-advanced-actions.html) L65–86,108–125; [P03](https://github.blog/changelog/2024-09-30-evolving-github-issues-public-beta/) L17–39,69–73; [P04](https://github.blog/changelog/2024-10-18-new-terminology-for-github-previews/) L22–60; [P05](https://knowledge.workspace.google.com/admin/releases/choose-when-users-get-new-features) L94–141; [P06](https://knowledge.workspace.google.com/admin/security/about-client-side-encryption) L109–136,163; [P07](https://knowledge.workspace.google.com/admin/security/manage-google-workspace-smart-features-for-your-users) L167–181,193; [P08](https://workspace.google.com/blog/product-announcements/updated-smart-feature-settings-give-users-increased-choice-and-control?e=48754805) L40–62; [P09](https://workspaceupdates.googleblog.com/2023/06/add-or-remove-client-side-encryption-from-google-sheets-and-slides-files.html?m=0) L67–100 | P01–09 9개(4 날짜 명시, 5 현행), AD06/07 공식 전제 대조; 동일 플랜 두 계정 실제 대조 0 | 당시 동일 에디션의 ON/OFF 실제 조작과 정책 강제 여부; 당시판에서 지원 대상이 다름 |
| Q3 | 생성≠목록 표시, flag≠한도 초과, 클릭≠정상 결과: [O01](https://github.com/orgs/community/discussions/86507) L218–255,294–314; [O02](https://github.com/orgs/community/discussions/106785) L443–499,518–535,578–625; [O03](https://github.com/orgs/community/discussions/148714) L325–351,531–568; [O07](https://github.com/orgs/community/discussions/152407) L766–786,887–902; [O08](https://github.com/orgs/community/discussions/121113) L118–146,208–223; [O10](https://github.com/orgs/community/discussions/139932) L343–362,507–545,709–735,776–792 | O01–10 10저작; E01–18 18행; Google 직접 사용자 0; E18 최초 추정 부재 제외 | 동일 조작 실제 결과 확인; 공개 댓글 본문과 시각·설정 확보; F06–10 실패 복구 |
| Q4 | 엄격 최초 활성 쌍 0; 두 동일 작성자 수리 후보일 뿐: [O03](https://github.com/orgs/community/discussions/148714) L325–351,531–568; [O04](https://github.com/orgs/community/discussions/148715) L839–851,1260–1324,1333–1336; [O06](https://github.com/orgs/community/discussions/148713) L178–182,278–328,429–466; [O09](https://workspaceupdates.googleblog.com/2023/12/easy-access-to-people-documents-blocks-in-google-docs.html) L65–98, Update Jan24/Jan30 | E06/E11 2 수리 후보; cohort incomplete 13, different project/surface/reporter 3, group only 2, 합 18 | 같은 계정/조작/표면·플랜·설정이 유지된 실제 실패→성공(타 계정 혼합 금지), 시각 정밀도; rollback 전후 별도 관측 |
| Q5 | 날짜만의 오답과 맞는 대조 동시: [O01](https://github.com/orgs/community/discussions/86507) L218–255,294–314; [O04](https://github.com/orgs/community/discussions/148715) L839–851,1260–1324,1333–1336; [O08](https://github.com/orgs/community/discussions/121113) L118–146,208–223; [O09](https://workspaceupdates.googleblog.com/2023/12/easy-access-to-people-documents-blocks-in-google-docs.html) L65–98, Update Jan24/Jan30; [O10](https://github.com/orgs/community/discussions/139932) L343–362,507–545,709–735,776–792; [A14](https://workspaceupdates.googleblog.com/2024/02/import-convert-excel-files-into-client-side-encrypted-google-sheets-now-generally-available.html) L75–96; [A16](https://workspaceupdates.googleblog.com/2025/02/improvements-to-everyday-google-sheets-actions.html) L65–103 | AD01–14; A 보고 충돌 3/14·공식 충돌 3/14·보고 일치 1/14·공식 일치 1/14·정답 미확인 6/14; B hold 9, C hold 6; 구성 비교, 대표오류율 아님 | 일자 동일 다른 계정에서도 같은 조작 성공, 또는 부재 원인이 버그/표면/권한으로 검증되면 날짜/rollout 귀인 철회 |
| Q6 | 운영자 개통과 실제 이용량; 지점별 전자자료 접속 쌍 부족: [T01](https://board.tfl.gov.uk/documents/s17927/Elizabeth%20Line%20Operations%20and%20Further%20Opening%20Stages.pdf) p1 §§3.1,4.1 (screenshot and extracted text), p2 §5 heading; [T02](https://www.metro.net/about/media-relations/l-a-metros-regional-connector-transit-project-officially-opens-giving-riders-immediate-access-to-more-dtla-stations-destinations-with-transfer-free-rides-from-east-l-a-to-santa-monica-azu/) L17–31; [D01](https://www.urbanlibraries.org/innovations/ereader-lending-program?page_id=47) L26–42; [D02](https://www.amigos.org/node/3507) L68–76; [D03](https://company.overdrive.com/2013/11/12/overdrive-media-stations-engage-ebook-and-audiobook-readers-inside-the-library/) L1596; [R01](https://company.overdrive.com/2013/11/12/overdrive-media-stations-engage-ebook-and-audiobook-readers-inside-the-library/) L1595–1602; [D04](https://www2.halifaxpubliclibraries.ca/archives/annual-reports/2020-21/) L225–288,394–411 | T 2저작, D 4저작/R01 중복. 도서관 엄격 0/2; Curbside와 전자자료 섞지 않음 | 같은 도서관의 둘 이상 지점에서 특정 전자자료 pilot→정식 실제 접속일/관측 로그 |
| Q7 | 발표 질문과 실제 사용 질문의 조건·보류 분리: [A05](https://github.blog/changelog/2025-01-13-evolving-github-issues-public-preview/) L22,41–75; [A14](https://workspaceupdates.googleblog.com/2024/02/import-convert-excel-files-into-client-side-encrypted-google-sheets-now-generally-available.html) L75–96; [O08](https://github.com/orgs/community/discussions/121113) L118–146,208–223; [O09](https://workspaceupdates.googleblog.com/2023/12/easy-access-to-people-documents-blocks-in-google-docs.html) L65–98, Update Jan24/Jan30; [P01](https://docs.github.com/en/get-started/using-github/exploring-early-access-releases-with-feature-preview) L19–42; [P07](https://knowledge.workspace.google.com/admin/security/manage-google-workspace-smart-features-for-your-users) L167–181,193 | AD 14개; C 보고 일치 4, 공식 일치 4, hold 6. 실제 개인 현재 상태 확인 0 | 링크 자체가 동일 사용자의 현재 자격·설정·성공을 확인해 주는 명시적 증거; 당시/현재 조건 변화 |
 
## 원격 재집계
```json
{
  "ledger": 83,
  "unique_sources": 43,
  "frame_rows": 66,
  "rollout_rows": 17,
  "observations": 18,
  "advice": 14,
  "join": {
    "cohort incomplete": 13,
    "different project": 1,
    "different surface": 1,
    "different reporter": 1,
    "group only": 2
  },
  "A": {
    "wrong_observed": 3,
    "unverifiable": 6,
    "correct_observed": 1,
    "wrong_policy": 3,
    "correct_policy": 1
  },
  "B": {
    "hold": 9,
    "correct_policy": 5
  },
  "C": {
    "correct_observed": 4,
    "hold": 6,
    "correct_policy": 4
  }
}
```
- sources 고유 work 43(목록 28·실패 11·D03 재열람 1 제외), 전체 83. 공지 17, 퇴역 1, 관측 10, 규약 9, 교통 2, 도서관 4. A02/07/11 동일 한도 계보를 합치면 공지 최소 15 계보. 독립 검토 아닌 자기 재판독.
- 20 자연자리 중 태그 잠정 6, 결측 14. 원순서 완전 인증 0/4. GH tag에서 더 이상의 명시 G가 없다는 제한적 판정과 GO 아카이브 접근 불완전을 구분. 목록 전체 원순위 및 모든 후보 수는 복원하지 못함. 후보/보충·퇴역 제외의 행은 frame에 따로 보존.
- 가장 그럴듯한 경쟁 설명은 발표 이후 고객 불만이 rollout이 아닌 기능별 접근/표면/버그/권한 문제라는 것. E04 beta slice-by 제한, E09 Projects 검색 미지원, E06/E11 직원 수리·작성자 확인, E08 필터와 bulk edit 차이로 지지. 최초 활성 지연 판정을 모두 미확인으로 낮췄다. 반대 방향 E14 당일 활성, E17 broad preview 전 opt-in 사용, E15/16 집단 rollback 보존.
- 당시/현행 정책 차이, URL의 현재판 수정 가능성, 최초 발행판 고정 미완료, 시간대/시각 정밀도, 댓글 정확 permalink 미확정, 1~6월 전체 후보 순서 미복원으로 PARTIAL. 날짜 단위 L/U는 시각상 정확한 interval 아님. 같은 일자 flag와 배너의 성공을 하나로 합치지 않았다.
- RESULT 제목 바로 아래 필수 표 3개 순서, 각 분모, 마지막 약점 표 정확히 3행 확인. 결과표와 원장 ID가 연결되나 URL 본문은 동적으로 바뀔 수 있음. 알려진 현재 계정 성공을 의미하는 행 없음.
- 다음 검사: GitHub 원격 최종 SHA 및 base 대비 변경 경로 확인, HANDOFF 별도 마지막 커밋. 실제 계정 시험은 수행하지 않음; 별도 Codex는 필요시 읽기/원장 파싱과 git 범위 검사만 한다.
