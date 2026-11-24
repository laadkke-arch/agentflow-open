# AF-RES-180 HANDOFF

- work_id: AF-RES-180
- self_status: PARTIAL
- status: PARTIAL
- independent_review: NOT_RUN
- branch: work/research-af-res-180
- owned_path: docs/workstreams/research/AF-RES-180/
- result_commit: c6a99088bdcf582cfee8a4abf3f95fcb43c519f7 (⑤ 결과·자체점검 고정판; 이 HANDOFF 자체의 commit은 branch tip에서 별도로 확인. 자기 SHA 순환 기재하지 않음)
- plan_commit: 128f673685ec804c526a38e3f89d4d8a43fcd299
- starting_integration_commit: 6fa67328360b02bc7e7270d4ad3300bfe0f286bd
- dependency: AF-RES-171 f8a9f723a7acd15ec33664c684a48b3e2bada46b (HANDOFF 직접 읽음, 자체 PARTIAL)
- representative_files: RESULT.md, SELF_CHECK.md, claims.csv, confirmations.csv, issues.csv, sources.jsonl, frame.csv, SCOPE.md; 보조 COMPARISONS.md, timeline.jsonl.

## 판정 범위 및 결과
자연 모집 2×30건, 자연 적격 4+4, 제외 52, 빈자리 0, 결과 기준 별도 보강 4. 전체 상세 사건 12. 현재 마일스톤 ID 246/262(1.86 실제 명칭 December / January 2024). 30일 최초 마감 창과 재마감 창 별도. 원자료 36개(이슈 12, PR/테스트 9[실제 연결 8+근접 비교 1], 운영 8, 배포 2, 심사/공공 5); 126 ledger rows, 297 timeline rows, 59 confirmation rows, 24 별도 실행/재현 진술 행(사전 실패/반복 포함; 독립 실험 수 아님), 최초/최종 30일 창 6/4. 직접 UI 실행 0. 동일 전체 조건으로 원제보자 사후 성공 확증 0건 관측, 12건 환경/결과 전체 동일성 미확인. 자연 8에서 창 내 원제보자 텍스트 후속 0 관측; 미공개 자료 부재 증명 아님.

- 원제보자가 동일 명령의 대상 선택을 재시험했다고 명시한 #197268: [보고](https://github.com/microsoft/vscode/issues/197268#issuecomment-1832685935)와 [PR](https://github.com/microsoft/vscode/pull/197291) 연결. 빌드/원 fixture/hidden 상태의 재진술이 없어 엄격한 동일 조건 확증으로 올리지 않는다.
- #107778의 타인 비재현, #191667의 타인 라벨, #200124의 원제보자 라벨+봇 요청은 다른 증거 수준이다. #197319의 원제보자 /verified는 생성기 변경 및 간헐 실패 불확실성 때문에 제한적 수용이며 봇 라벨과 thumbs-up은 같은 관측 lineage다. #173563의 native workaround와 custom title 요구, #177059의 Windows/Mac 차이, #31819의 최초 마감 후 실패/재개가 반례다.
- P197291/P202026은 이미 존재하는 explorer와 미생성 explorer의 서로 다른 조작 조건. 8개 merge SHA의 해당 stable tag ancestry 확인, 실제 배포 활성화 시각/동작 증명 아님.
- E1/E2 학술 재심의 요구 대상 차이, G1–G3 공식 시민 판정의 완료/요구/사용자 인수 차이. 원 시민 메시지 및 완료 뒤 직접 동일 동작 기록 부족. DB·수집기·검색 포맷 고정하지 않음.
- 핵심 문장: verified가 붙은 사건은 라벨 작성자·시각·대상만 주장한다. 원제보자 확인은 동일 계정의 명시 실행/결과를 연결하고, 같은 조건 확인은 원입력·문서·명령·환경·수정 전후 판의 일치를 추가로 증명해야 한다. 반응의 대상 메시지와 실제 실행의 대상 요구는 다른 키다.

## validation / 자체점검
⑤ SHA에서 10개 파일을 다시 fetch했다. RESULT.md 첫 세 표 열 이름 정확히 일치, 마지막 표 정확히 3행. SCOPE/RESULT/SELF_CHECK/COMPARISONS 및 CSV/JSONL 대표 파일 읽기 성공. source_id 누락 0, 중복 0, CSV 열 수 일치, claims 12/confirmations 59. ④에서 확인표 열 인덱스 및 날짜 창 재계산 보정, actor/event ID 대조 불일치 0. 표의 모든 모집 슬롯 채웠다. 독립 검토와 GUI 재실행은 수행하지 않았다.

| 묶음 | 커밋 | 내용 |
|---|---|---|
| ① | 68d8c31b5cfff0fa56243b4fd2699d53478d6dae | 모집·판정 규칙 |
| ② | bc9f3e35d944e8ea3b669a5a5d09fc629c4c6499 / 1968f315fe18ea0c55dcf96b5a9aca2042d4b27f | 모집 고정·원장/표본 |
| ③ | 845995bf31818b019ab0af9776a1512f23d0256e | 확인 행·초기 판정 |
| ④ | 01514cabe44c67346747ca9e8d926ed527c82cd1 | 경쟁 설명·분야 비교·열 보정 |
| ⑤ | c6a99088bdcf582cfee8a4abf3f95fcb43c519f7 | 필수 표·자체점검 |
| ⑥ | 이 파일을 포함하는 branch tip | 최종 인계 |

## blockers / 미충족
1. 원제보자 동일 전체 조건 사후 확증 미확인 12건(그중 동일 명령/출력의 명시 재시험 1건), 원제보자=수정자 실제 사례 미확보. 정확한 사후 시험 build/fixture/환경 미기재·영상 미열람; I197319는 generator 자체 변경과 간헐성.
2. 최초 원본문 revision 12건 불명, 최종 수정 연결 SHA 미확인 4건(I31819/I107778/I127958/I132428); 실제 당시 wiki revision/triage stable action 실행 SHA 불명. dot-control.json 전체 파일 응답이 비어 최신 integration diff의 AF-RES-180 행과 사용자 지정 SHA에 의존했다(행의 RUNNING/depends_on/attempt/owned_path/branch 확인). 171 중앙 DONE은 배정문에 따른 값; 171 자체 PARTIAL은 고정 HANDOFF에서 확인했다. 현재 milestone 목록은 created asc proxy이며 번호 오름차순은 관측 확인했으나 전체 페이지 수치 정렬 검산은 미실시.
3. 시민 원요청과 동일 당사자 완료 후 직접 조작 확인의 직접 원본문 미확보(공개 판정 3건의 중계 진술은 산입하되 직접 시민 메시지로 간주하지 않음, SeeClickFix 후보 접근 403). 학술 재심 2건은 직접 공개 XML. 종류별 수치 최소 이상이지만 엄격한 직접 인수 요건 미달. 실행 및 독립 검토 부족으로 PARTIAL.

## next_action / 첫 재개 행동
Codex Cloud에서 우선 다음 고정 입력을 읽고 범위·형식 검산 후 #197268 동일 원입력 재시험 환경을 확보한다. 이전 작업을 바꾸거나 중앙 제어 파일을 수정하지 않는다.

```sh
git fetch origin work/research-af-res-180
git show c6a99088bdcf582cfee8a4abf3f95fcb43c519f7:docs/workstreams/research/AF-RES-180/RESULT.md
git show c6a99088bdcf582cfee8a4abf3f95fcb43c519f7:docs/workstreams/research/AF-RES-180/SELF_CHECK.md
git diff --name-only 6fa67328360b02bc7e7270d4ad3300bfe0f286bd origin/work/research-af-res-180
gh api --paginate 'repos/microsoft/vscode/issues/197268/timeline?per_page=100'
gh api --paginate 'repos/microsoft/vscode/issues/197319/timeline?per_page=100'
gh api --paginate 'repos/microsoft/vscode/issues/comments/1832685935/reactions?per_page=100'
for m in 246 262; do
  gh api --paginate "repos/microsoft/vscode/issues?milestone=$m&labels=bug&state=all&sort=created&direction=asc&per_page=100" | jq -s 'add | map(select(.pull_request|not)) | sort_by(.number)[:30] | map(.number)'
done
git clone --filter=blob:none https://github.com/microsoft/vscode.git /tmp/vscode-af-res-180
git -C /tmp/vscode-af-res-180 merge-base --is-ancestor 0e9376c25a9018dfe3a42eae5dde98443b0dd835 1.85.0
git -C /tmp/vscode-af-res-180 merge-base --is-ancestor b5d2084dfbc68836bf0aae82748d250205aef785 1.86.0
git clone https://github.com/microsoft/vscode.wiki.git /tmp/vscode-wiki-af-res-180
git -C /tmp/vscode-wiki-af-res-180 log --until=2024-01-31T23:59:59Z -- Issue-Tracking.md Automated-Issue-Triaging.md
```

검산 기대: 변경 파일은 owned_path만, 숫자 정렬 상위 30은 frame.csv와 일치(차이 시 모집 보정), merge-base 명령 0, wiki log에서 당시 판 후보 식별. 실행 로그의 external stable action SHA는 해당 workflow run의 checkout log 보존 여부 먼저 점검하며 얻지 못하면 미확인 유지. 위 명령은 인계용이며 로컬 재실행하지 않았다.

### GUI 재시험 입력 (새 빌드/설치/실행 권한과 격리된 환경이 확보된 뒤)
- macOS Darwin arm64 격리 VM, 원 #197268 1.85.0-insider a9d8fbca…(원문 전체 SHA 확보), 목표 고정 태그 1.85.0 및 1.86.0, 또는 해당 commit 전후 재현 가능 빌드. 실제 빌드/OS는 Help: About 및 `code-insiders --version`, `code --version`, `sw_vers`로 수집한다. 전후 동일 user-data-dir의 복제본 사용, 실사용 설정/파일 제외. 원 제보자가 사용한 정확한 수정 후 build는 아직 모른다.
- 빈 작업 폴더에 test/ 및 파일 생성. 개발 확장 command 등록: `vscode.commands.executeCommand('revealInExplorer', vscode.Uri.joinPath(vscode.workspace.workspaceFolders[0].uri,'test'))`. package.json에 activationEvents/onCommand 및 command contribution, main.js에 activate(context) 등록. 각 빌드의 실행 파일에 `--user-data-dir /tmp/af180/profile-copy --extensions-dir /tmp/af180/extensions --extensionDevelopmentPath /tmp/af180/testext /tmp/af180/ws`로 실행. 탐색기를 먼저 열었다가 chat view로 숨긴 상태와 explorer pane 미생성 상태를 분리하고 autoReveal on/off를 기록한다. 예상: #197268 원조건에서 원판 선택 누락/수정판 test 선택, 단 미생성 view는 별도. #200124는 autoReveal=false 및 debug view 열기, Shift+Cmd+E를 workbench.files.action.showActiveFileInExplorer에 바인딩한 뒤 같은 파일의 활성 위치 확인. 구체적 성공/실패 영상과 단계 기록, 빌드/입력 SHA 보존.
- #197319 기존 실제 파일 /tmp/af180/ws/test.txt 준비, macOS에서 `open 'vscode://file//tmp/af180/ws/test.txt'` 및 `open 'vscode://file/tmp/af180/ws/test.txt'`를 동일 앱 대상으로 실행(단일/이중 슬래시와 open dialog setting 분리). 각 10회 콜드/웜 시도, 파일 탭 열림/포커스만/대화상자 관측; 원 생성기 변경 효과와 패치 효과를 분리. 원제보자 과거 성공의 인과가 자동 확증되는 것은 아님.
- #173563 macOS custom/native × command center on/off × 제목 Cmd-click/오른쪽 클릭; 경로 메뉴/Finder 열림 여부 분리. #107778 Mac file.txt에 동일 문구를 쓰고 검색→rename FILE.txt→재검색 결과 개수 기록; case-sensitive volume 차이도 구별. #31819 원 2017 Windows xterm.js 및 dist/xterm.js open nonactive와 2023 close 예시 비교. #127958 multi-root a/foo.txt 및 a/folder/foo.txt를 붙여넣기/타이핑 각각. #132428 Windows11 두 편집기와 explorer, viewport width 변화에서 find 필드 겹침을 기록.
- 공공 사례는 당사자 공개 ticket 원본문, municipal work order scope/close, 당사자 동일 이동/사용 후속 발화가 함께 있는 1건 이상 먼저 확보; 없다면 직접 확인 주장 보류. 자기보고자는 PR author와 issue author 동일 계정을 직접 연결하고 독립 검증자와 분리한다.

## index_proposal
AF-RES-180 | PARTIAL | VS Code 1.85/1.86 자연 8+보강 4, verified/봇/원제보자/타인 증거 귀속과 요구·조작·환경 키의 교차 판정; 동일 전체 환경·시민 직접 인수 미확인 | RESULT.md @ c6a99088bdcf582cfee8a4abf3f95fcb43c519f7
