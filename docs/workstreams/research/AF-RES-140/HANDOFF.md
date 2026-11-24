# AF-RES-140 HANDOFF

**상태: PARTIAL.** 현재 공개 이슈 본문층의 8사건을 대상으로 두 경로의 사전 분기와 사후 댓글을 순차 저장했다. 최초 본문 복원·개별 댓글 시각·신문 독립 원면/원시 OCR·checkout 검사가 남았다. 중앙 DONE 여부와 이 인계의 PARTIAL은 별개다.

- 작업 브랜치: `work/research-af-res-140`
- 실제 통합 기준: `b6255317d161b5d1742bdd7cf1b80a2136cdc786`; 계획 기준 `1d65b0b7aaef85350df8842dfc05a6be69148b38`. AGENTS, STATE, START_HERE, RESEARCH_BRIEF, DOT_AUTOMATION, RESEARCH_WORKFLOW 읽음. 중앙 JSON 전체 fetch가 빈 본문을 반환해 실제 기준 커밋의 diff에서 자기 행 RUNNING, attempt 1, web-pro, depends_on AF-RES-136, owned_path를 확인했다. 중앙 source_commit null, 136 DONE은 중앙 전체 행에서 재검증하지 못했다.
- 유일 등록 선행 고정 인계 `547b59212c164c904705ed0abea46f8e9a7d4a02`, 결과 `a081ca3d619c6aa6676cd1ec9d8e8a33bb739ebb`. 136 HANDOFF, RESULT, concordance, second-seal, remote-recheck 직접 읽음. 이전 과포함/반복 인지 문제를 참고했으며 136 여섯 사례/18답을 재채점하거나 효과 근거로 사용하지 않았다.
- 결과판: `a43dad1ece967452a996985541773396ea4363a5` (RESULT.md).
- 검사판: `ce789b9b93cbb8ddd1c9023219b5d9710c3af24e` (SELF_CHECK), 검산 영수증 `746e8600e3912c6eeb5bdf24c8e0f74272fde54f` (원격 재열람·compare; CLI 미실시).

## 단계별 원격 커밋

| 묶음 | SHA | 대표 경로 |
|---|---|---|
| 절차·노출 규칙 | `3a9309de143b54c363caee6560f1b7f3a0fe44a6` | SCOPE.md |
| 번호·생성시각 60 고정 | `d2c2fe2f42201529d0d0f2dd100e2b42a31e1272` | frame.csv |
| 현재 본문 판정 | `fca03b3b2b7d31feb4d946bfee7c961514bd9d16` | frame.csv |
| 요구 봉인 | `a6e9234b1cad8bfa19d1cb3364f0b2c70c4e7ad3` | requirements.csv |
| 첫 링크·초기 답 | `689b0d345607af0707910baffba69a0c06a58263` | first-links.csv |
| 둘째 면 예측·질문 A/B 사전 봉인 | `56dd466ed568cd54748843b5f926e11b603d2bf2` | branches.csv |
| 둘째 면 판독 | `2bc6ab91b5fa1cc59b490fb586d661ebd05f02ff` | branches.csv |
| 후속 대화 열람 | `d6a59215da5ea3c3146a8e74ed8e6f775974ec39` | followup.csv |
| 타 분야 | `e6626587ae28e26dc20d3d910f226edccc76a7cc` | domains.csv |
| 원장 | `b4ea12c77629a6b88625616081b9cddd2d6debe3` | sources.jsonl |
| 필수 표·해석 | `a43dad1ece967452a996985541773396ea4363a5` | RESULT.md |
| 자기반증 | `ce789b9b93cbb8ddd1c9023219b5d9710c3af24e` | SELF_CHECK.md |
| 원격 검산 | `746e8600e3912c6eeb5bdf24c8e0f74272fde54f` | evidence/remote-recheck.json |
| 최종 인계 | 이 파일의 커밋 (자기 SHA 미기입) | HANDOFF.md |

모든 위 대표 파일은 각 고정 SHA에서 재열람하여 blob 일치 확인. 사전 분기 8행이 이후 판독의 각 행 접두사로 보존됨. GitHub compare 기준→SELF_CHECK 12 commits, behind 0, 10 변경 파일 전부 owned_path. 원격 검산 파일도 새 읽기로 내용 일치. 중앙 파일 수정하지 않음. 파일별 API 커밋을 사용하여 같은 묶음 내 파일은 순차 별도 커밋이다.

## 실제 수행과 미실시

- 모집 60번호/생성시각(30+30), 본문 20개, 채택 8명(4+4), 제외/정원 후 추가 판독 12, 나머지 40 미열람, 확장층 0. 검색 시각 필드 null로 메타데이터만 다시 투영. 초기 #1190 updated_at 함께 노출; #1500, #1501 채택은 경계적; #1191 generic reproduction 제외 역시 판단 여지. 모든 최초판은 현재 본문만 확인, 편집 전 버전 미확인. 엄격 최초판 확인 0/8, 비교 0/0(비율 미산출).
- 공통 첫 절 8/8, 1200 CP씩; 추가 절 성공 7/8(4 CSV, 3 YAML), 1200 CP씩. Y1 고정 후보 404를 사후 대체하지 않았다. 5/7 기존 답 유지·보강(hold 2, 근거/계약 3), C4 1/7 후보 좁힘, Y3 1/7 조건부 후보, 둘째 절 신규 핵심 해결 0/7(관찰 판독 분류, 인과 아님). 사전 가상 질문 8개, 실제 발송 0회, Y4 질문 불필요 판정.
- 후속 댓글 24개, original author 후속 4/8, 미응답 4/8. C3 escape 거절, C4 in2csv workaround, Y2 수정 빌드 성공, Y3 CRLF/LF 비교. Y2는 질문했던 null 정책이 아니라 결함 수정이 해법. C3 출력 표현 의무는 기술 문서만으로 결정 불가, Y3 입력 차이와 정규화 허용은 별개. 모든 작성자 시행은 보고 수준이며 독립 실행하지 않았다. comment created/updated_at null, 재시도에도 날짜 미복원.
- 원장 63행, 산입 고유 저작 27(현재 본문 포함), 공식 csvkit 5/yq 6, 별도 시험/사양 4, CPython 문서 1, 신문 기관 1, 음악 2, 원저작 8. 독립 원면 없이 기관 가이드의 원면/OCR 병치 화면에서 실제 같은 문장 비교. LOC 독립 원면, raw OCR, gallery, IIIF 403/불가. 신문 1/2 엄격 산입이므로 부분 완료. 음악 총보와 4파트 실제 PDF 면 5개, m2 C-low와 Bb 동일 실음·상이 기보, C-high 옥타브 반례. 동일 편곡 1 work.
- 동일 판독자/현재 본문 층. 이전 학습, 실제 edit history, 독립 블라인드, 사용자 반응 비용·응답률·인과효과 미검증. C1 입력 첨부·Y2 실제 CI 입력, C3 실제 버전 1.0.7/Python 3.11.2의 정확한 시험, Y3 원본 bytes 미확인.
- 실제 checkout, manifest 생성 및 workbench.session check는 **미실시**. 실행 SHA·종료값·stdout/stderr 모두 null. 소프트웨어 재현 테스트도 미실시. 영수증은 원격 파일/커밋/경로 검산만 뜻한다.

## 첫 재개 행동

사전 봉인 파일은 그대로 보존한다. 먼저 원 이슈 8개의 최초판 edit history, 댓글 개별 시각을 접근 허용 GitHub 경로에서 확보한다. 현재 읽은 독자는 후속 답을 알고 있으므로 독립 새 판독에서만 엄격 최초판층을 재실험한다. LOC Trek image 5 독립 스캔과 raw OCR/좌표를 공공 접근 가능한 viewer 또는 IIIF로 재확인한다. 실패 시 권한 우회하지 않고 PARTIAL을 유지한다. Y1 고정 경로 실패는 기존 분모 그대로 유지하고 올바른 후보는 후속 자료층에만 추가한다.

checkout 있는 다음 작업자는 아래를 실행한다. 기존 manifest가 있는지 먼저 확인하고, 없으면 start가 이미 진행된 작업의 최초 기준을 보존하는지 구현을 확인한다. 기존 봉인과 base를 다른 값으로 재고정하지 않는다. 사용자 지시 명령 및 입력:

```sh
git fetch origin chore/workspace-foundation work/research-af-res-140 work/research-af-res-136
git switch work/research-af-res-140
git rev-parse HEAD
python -B -m workbench.session start af-res-140 --allow docs/workstreams/research/AF-RES-140/ --dependency work/research-af-res-136=547b59212c164c904705ed0abea46f8e9a7d4a02 --output docs/workstreams/research/AF-RES-140/manifest.json --fetch
python -B -m workbench.session check docs/workstreams/research/AF-RES-140/manifest.json --fetch
```

정확한 원판별 소프트웨어 재현 입력은 requirements.csv와 followup.csv에 있다: C3 quote embedded CSV `csvformat -T -B -P X` 및 alternate `-Q~`를 csvkit 1.0.7/Python 3.11.2에서 비교; C4 1.0.5 `in2csv test.csv --date-format "%d/%m/%Y" | csvstat`; Y2 4.30.6 vs 4.30.7 세 carriage return과 두 carriage return merge; Y3 동일 1.yml/2.yml CRLF/LF의 `yq '.values |= load_str("2.yaml")'` 및 style=literal. C1 XLS 원본 및 C2 정확 DDL/방언은 사전 확인 필요. 실행 환경·입력 bytes·출력·종료값 별도 기록. 실제 CLI 검사 뒤 대상 SHA/변경 경로 및 stdout/stderr를 evidence/에 추가.

색인 한 줄: **AF-RES-140 PARTIAL — 현재 본문 8건의 추가 기술절 vs 보존값 질문 사전봉인/후속 24댓글; 기술 계약과 원저자 표현 의무 분리, 결함 수정 반례, 최초판·신문 원면·CLI 결측.**

| 중요한 불일치·약점 | 다음 조사·자료 또는 실험 | 결론을 바꿀 관측 |
|---|---|---|
| 현재 body 최초판 미복원 8/8, 댓글 시각 null | edit history/공개시각 확보, 새 독립 가림 판독 | 사후 요구가 최초판에 이미 명시되었거나 초기 노출 없음을 증명 |
| 둘째 자료 1건 404, C3 버전 차이·Y2 정책질문과 수정판의 불일치 | 정확판 최소 재현과 대안 링크 사후층, 실제 사용자 변수 검증 | 추가 문서 자체가 보존 계약을 충족하거나 질문 없이 선택이 확정됨 |
| 신문 독립 원면·raw OCR 불가 및 checkout 검사 미실시 | LOC image 5 원면/OCR 위치 검증, 지정 workbench 명령 실행 | 원철자·배치·검색 목적 일치/불일치와 실제 검사 성공 또는 실패 확인 |
