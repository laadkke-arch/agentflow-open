# AF-DOT-001 — 기존 조사 표본 검토

- 작업: AF-DOT-001 / 시도 1
- 기준: `laadkke-arch/agentflow-open@9c06a7a998a7040a708d9336545fbf3c9cdfd205`
- 범위: 기존 후보 4개의 역할·근거 수준·미확인 제약 검토와 AF-DOT-002 실행 인계.
- 원 관측 시각: `2026-11-19T10:00:21Z`. 이번 검토일: 2026-11-19.
- 상태: 기존 판단 유지. 외부 후보 실행·새 제품 설계·서비스 통합은 하지 않았다.

## 1. 핵심 판단

[조사 표본](https://github.com/laadkke-arch/agentflow-open/blob/9c06a7a998a7040a708d9336545fbf3c9cdfd205/docs/research/discovery-case-2026-11-19.json)의 네 후보는 같은 종류의 완성품 대안이 아니다. 발견 목록, 활동 지표 참고, 선택적 메타데이터 부품, 수동 비교 참고로 역할이 다르다. 표본의 D1 문서 확인과 D2 코드 관찰을 실행·계정 권한·프로젝트 적합성으로 올려 해석할 근거는 없다.

이번 작업은 표본의 판단을 검토하고 재현 가능한 인계로 남긴다. [향후 연구 브리프](https://github.com/laadkke-arch/agentflow-open/blob/9c06a7a998a7040a708d9336545fbf3c9cdfd205/docs/product/RESEARCH_BRIEF.md)의 구조·목적 기반 탐색 제품 전체에 대한 설계 결론은 아니다.

## 2. 후보별 역할·판단·조건

| 후보 | 유지할 역할과 결정 | 근거와 확인 범위 | 미확인 제약·판단을 바꿀 최소 확인 |
| --- | --- | --- | --- |
| OpenAlternative | 후보 이름·공식 링크를 찾는 `reference` | `oa-readme`, `oa-license` / D1. 고정 README의 awesome-list 전환 및 이전 Next.js 보일러플레이트 이동 공지, 현재 목록 LICENSE의 CC0 표기를 재열람했다. | 링크된 개별 소프트웨어·이전 앱의 라이선스, 실제 실행 코드, 서비스 API는 미확인. 앱 재사용 판단은 별도 코드·버전·라이선스를 확인한 뒤 한다. |
| OSSInsight | 저장소 활동 지표와 비교 방식을 참고하는 `reference` | `oi-about`, `oi-live-explore` / 기존 D1 관측; `oi-ask-code` / D2. 고정 코드의 `isExplorerUnderMaintenance()`가 true이고 `handlePOST()`가 모델 호출 전에 503을 반환하는 분기를 재열람했다. | live POST·다른 분석 API·배포 코드 일치·라이선스·비용은 미확인. 필수 검색 의존성 채택은 필요한 읽기 API의 실제 응답·데이터 시각·조건을 확인할 때 재검토한다. |
| Libraries.io | 선택적 패키지 메타데이터 `component` 후보. 결정은 `defer` | `lib-search-code`, `lib-fields-code` / D2. API 키 요구, serializer 연결과 필드, 선택적인 `updated_at`을 재열람했다. 문서·약관 템플릿과 사용자 이슈는 기존 D1 관측을 재사용했다. | 현재 키 발급·계정 권한·무료량·live 응답·갱신·약관 일치·이슈 재현은 미확인. 허용된 접근 조건으로 대표 패키지 읽기 응답과 현재 조건을 확인한 뒤 후보를 다시 비교한다. |
| AlternativeTo | 수동 후보 비교·대안 관계 참고인 `reference`. 경쟁 DB 콘텐츠 수집 용도는 `reject` | `at-terms`, `at-faq` / 기존 D1 관측. 표본이 10:00:21Z에 기록한 이용 조건·에디션 취급 판단을 유지한다. 이번에 live 약관·FAQ는 재조회하지 않았다. | 별도 데이터 이용 허가·API 제공·현재 약관·개별 에디션의 가격·조건은 미확인. 원 관측을 현재의 별도 법률 판단이나 이용 허가로 확대하지 않는다. |

### 직접 재열람한 고정 원문

이번 작업 안의 별도 읽기 전용 검토자가 아래 다섯 파일을 확인했다. 주 작성자는 표본·fixture·검사 코드와 그 검토 결과를 대조했다. 추가 후보를 검색하지 않았다.

- OpenAlternative: [README](https://github.com/piotrkulpinski/open-source-alternatives/blob/156045dde3d74a6bfdad675c13521718ca0e50b5/README.md), [LICENSE](https://github.com/piotrkulpinski/open-source-alternatives/blob/156045dde3d74a6bfdad675c13521718ca0e50b5/LICENSE).
- OSSInsight: [ask route](https://github.com/pingcap/ossinsight/blob/77538008b8fe8b0dd3dc6caa3fc4ba987e10360a/apps/web/app/api/explorer/ask/route.ts).
- Libraries.io: [검색 컨트롤러](https://github.com/librariesio/libraries.io/blob/16ef5c54bc2d2b984963aa1b342a47e595c8a85b/app/controllers/api/search_controller.rb), [serializer](https://github.com/librariesio/libraries.io/blob/16ef5c54bc2d2b984963aa1b342a47e595c8a85b/app/serializers/project_serializer.rb).

나머지 외부 출처는 표본의 저장된 관측·URL·확인일·미확인을 읽었다. 원 관측의 `checked_at_utc`를 이번 재검토 시각으로 바꾸지 않았다.

## 3. 반례와 조합 조건

- OpenAlternative 저장소를 지금 바로 배포 가능한 Next.js 앱으로 권하면 목록 전환 공지와 충돌한다. CC0도 링크된 모든 프로젝트로 확장할 수 없다.
- OSSInsight의 소개 문구나 코드 분기를 실제 배포 API의 성공·실패 응답으로 쓰면 관측 범위를 넘는다. 활동량은 요구사항 적합성 판정의 대체 지표가 아니다.
- Libraries.io의 `component` 분류는 채택 완료가 아니다. 문서 템플릿의 분당 60회 안내는 계정의 현재 권한을 증명하지 않고, 한 사용자 보고나 closed 이슈는 전체 장애·해결 완료의 증거가 아니다.
- AlternativeTo의 공개 열람 가능성을 경쟁 DB 수집 허가로 읽거나, 한 제품 항목의 태그를 모든 에디션의 현재 조건으로 쓰면 표본의 제약을 잃는다.

조건부로 함께 쓸 수 있는 역할은 '발견 목록에서 후보 찾기 → 개별 원출처 확인 → 허용된 메타데이터의 선택적 보강 → 활동 지표·수동 대안 비교 참고'다. 이는 역할의 조합 가능성 설명이며 구현 순서·필수 파이프라인·최종 제품 설계의 채택이 아니다. AlternativeTo 콘텐츠를 DB 공급원으로 넣는 조합은 저장된 판단과 충돌한다.

## 4. 다음 검사의 실제 입력과 보장 범위

[project.json의 `tasks.discovery`](https://github.com/laadkke-arch/agentflow-open/blob/9c06a7a998a7040a708d9336545fbf3c9cdfd205/lab/reference-audit/project.json)은 `lab/reference-audit`를 작업 디렉터리로 하여 `task.py fixtures/discovery.json`을 실행한다.

[task.py의 `audit()`와 진입부](https://github.com/laadkke-arch/agentflow-open/blob/9c06a7a998a7040a708d9336545fbf3c9cdfd205/lab/reference-audit/task.py)는 fixture의 `document`와 `sources`만 읽는다. `case_path`에 적힌 조사 원본 JSON은 열지 않는다.

| 확인 대상 | 실제 동작 |
| --- | --- |
| 잘못된 등록 출처 ID, 중복 ID, 정상 형식 표식의 미등록 ID 참조 | 오류로 보고한다. |
| 사용하지 않은 출처, 같은 GitHub 저장소 루트 URL | 진단을 제공한다. 그 자체로 실패시키지 않는다. |
| 잘못된 형식의 인용 표식, 인용 없는 주장 | 완전성 검사를 하지 않는다. |
| 조사 원본과 fixture의 일치, 주장·인용의 의미, D1/D2 적정성 | 검사하지 않는다. |
| URL 생존·현재 서비스·API 권한·가격·약관·추천 품질 | 검사하지 않는다. 네트워크에 접속하지 않는다. |

`repository_key()`가 묶는 것은 저장소 루트 URL이다. 고정 파일·문서 하위 URL을 포함한 자료 전체의 중복 여부까지 확인했다고 쓰지 않는다. 출력의 `claim_truth_checked: false`, `network_accessed: false`도 그대로 보존해야 한다.

별도 검토자의 정적 대조에서 원본은 4후보·11주장·13출처이고, fixture의 13출처는 `id/url/checked_at_utc/level/revision` 다섯 필드가 일치했다. 13개 ID 모두 문서의 표식에 등장한다. 이는 자료 대조 결과이며 이번 작업에서 `discovery` 명령을 실행한 결과가 아니다.

## 5. 실행 증거를 남길 때 주의

[workbench/cli.py의 `run_task()`, `tracked_inputs()`](https://github.com/laadkke-arch/agentflow-open/blob/9c06a7a998a7040a708d9336545fbf3c9cdfd205/workbench/cli.py)는 `.workbench/runs/reference-audit/<run-id>/`에 `receipt.json`, `stdout.txt`, `stderr.txt`를 만든다. `receipt.inputs`에는 lab 입력 6개와 공통 코드 4개의 해시가 들어가지만 조사 원본 JSON은 포함되지 않는다.

AF-DOT-002는 실행 SHA·원본 JSON 해시를 별도로 기록하고, 실제 receipt가 지목하는 세 파일을 자기 허용 폴더로 복사해 커밋해야 한다. 실패·timeout도 종료 코드와 로그를 보존한다. `verify-receipt`의 성공은 해시 일치이며 출처의 진실성 인증이 아니다.

이번 `manifest.json`은 사용자 지정 쓰기 범위를 지키기 위해 `docs/tasks/` 대신 이 폴더에 만들었다. `workbench.session check <manifest> --fetch`는 이 파일을 직접 검사할 수 있다. 기본 `check-all`은 `docs/tasks/*.json`만 찾으므로 이 manifest를 자동 발견하지 못한다. 다음 세션과 통합 담당자는 개별 `check`를 사용해야 한다.

## 6. 검토·미해결·색인 제안

독립 검토자는 표본의 네 후보 판단에서 확정 오류를 찾지 못했다. 주 작성자는 실제 입력 경로와 검사 코드의 범위를 대조했고, 가장 큰 오해 위험인 '출처 연결 통과 = 후보 사실·접근·실행 검증'을 위와 같이 분리했다. 내부 독립 검토는 새 웹 Pro 세션 교체 시험의 증거가 아니다.

남은 일은 AF-DOT-002가 GitHub 인계만으로 내용을 복원하고 discovery 명령을 실제 실행하여 이 경계를 유지하는지 확인하는 것이다. 이번 작업에서는 그 후속 과제를 시작하지 않았다.

편집 담당에게 제안할 색인 행: `AF-DOT-001 | 기존 후보 4개 판단과 출처 연결 검사 경계 | 검토 완료·후속 실행 대기 | docs/workstreams/dot-trial/AF-DOT-001/REVIEW.md | 원본 및 코드 9c06a7a998a7040a708d9336545fbf3c9cdfd205`. 공통 색인과 `dot-control.json`은 수정하지 않았다.

