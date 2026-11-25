# AF-RES-003#1 — 최종 인계

## 1. 식별

- 작업 ID / 시도: **AF-RES-003 / 1**.
- 상태: **REVIEW_READY**. 배정된 문서 연구·반례 대조·검토는 완료했고 통합 담당의 채택·병합 판단을 남긴다.
- 작업 종류: 진행표의 배정 표기는 `web-pro`. 실제 작업은 이 ChatGPT 대화의 웹 원문 열람·GitHub 연결 도구·클라우드 checkout에서 수행했다. native 웹 Pro 작업 생성이나 별도 사용자 대화 인계 시험의 성공은 확인하지 않았다.
- 실제 모델·실행 위치: 대화 환경에 제공된 모델 표기는 GPT-6 Astra Pro. 계정의 native 선택 화면·요금제·서비스 내부 실행 ID는 별도 확인하지 않았다. 검사는 Linux 클라우드 checkout, Python `3.12.14`, Git `2.52.0`에서 실행했다.
- 공개 작업 참조: [PR #5](https://github.com/laadkke-arch/agentflow-open/pull/5). 비공개 작업 조회에는 `AF-RES-003#1`·저장소·브랜치를 사용한다. 비공개 서비스 ID는 저장하지 않았다.
- 저장소 / 브랜치: `laadkke-arch/agentflow-open` / `work/research-af-res-003`.
- 시작 통합 SHA: [`9d728dfe2c2f3a13d9995b5fdc14a252aeddfdad`](https://github.com/laadkke-arch/agentflow-open/commit/9d728dfe2c2f3a13d9995b5fdc14a252aeddfdad). 원격에 작업 브랜치가 없음을 확인한 뒤 이 SHA에서 만들었다.
- 실제 연구·검토 검사 SHA: [`caf806738b0ed07fe5bce8d4c5c173bada5286b3`](https://github.com/laadkke-arch/agentflow-open/commit/caf806738b0ed07fe5bce8d4c5c173bada5286b3).
- 인계 작성 직전 원격 저장 SHA: [`1ca4558a62e13800ce558f5bba19210da3b087a2`](https://github.com/laadkke-arch/agentflow-open/commit/1ca4558a62e13800ce558f5bba19210da3b087a2), 검사 영수증까지 포함. 이 HANDOFF와 STATUS는 그 뒤의 마지막 커밋에 저장한다. 이 파일을 포함한 정확한 결과 SHA는 아래 `git log` 명령으로 식별한다. 자기 커밋 SHA를 본문에 미리 적었다고 주장하지 않는다.
- 마지막 fetch에서 확인한 통합 SHA: `bdc2e052900b1658981dfcec354682f4e1fc29fb`. 시작 SHA 이후 차이는 진행 담당의 `dot-control.json` 변경뿐이며 AF-RES-003 배정·의존성·계약 fingerprint는 같았다.
- 마지막 실제 증거: 15:56:50 UTC 개별 계약 검사 통과, 15:58:00 UTC 문서 감사 통과, 15:59:40 UTC 초안 PR 생성. 조회 기준 **2026-11-19 16:00:01 UTC / 한국 2026-11-20 01:00:01**.
- PR 상태: [#5](https://github.com/laadkke-arch/agentflow-open/pull/5), open draft, 대상 `chore/workspace-foundation`. 병합은 수행하지 않았다.

## 2. 사용자 요구 / 작업 범위

질문은 미래 탐색기의 **identity와 storage**다. 제품·기능·메커니즘·출처를 구별해 오병합과 과분할을 줄이는 최소 표현, 같은 사례에 대한 저장 대안, 변경 시 보존할 연결을 조사했다. 최소 20개 직접 원문 열람 요구에 대해 **33개**를 기록했다. 검색 결과·접근 실패·반복 열람·I12의 재작성 요약은 집계에서 제외했다.

기준 입력은 시작 SHA의 [AGENTS.md](https://github.com/laadkke-arch/agentflow-open/blob/9d728dfe2c2f3a13d9995b5fdc14a252aeddfdad/AGENTS.md), [STATE.md](https://github.com/laadkke-arch/agentflow-open/blob/9d728dfe2c2f3a13d9995b5fdc14a252aeddfdad/STATE.md), [DOT_AUTOMATION.md](https://github.com/laadkke-arch/agentflow-open/blob/9d728dfe2c2f3a13d9995b5fdc14a252aeddfdad/docs/DOT_AUTOMATION.md), [RESEARCH_WORKFLOW.md](https://github.com/laadkke-arch/agentflow-open/blob/9d728dfe2c2f3a13d9995b5fdc14a252aeddfdad/docs/RESEARCH_WORKFLOW.md), [RESEARCH_BRIEF.md](https://github.com/laadkke-arch/agentflow-open/blob/9d728dfe2c2f3a13d9995b5fdc14a252aeddfdad/docs/product/RESEARCH_BRIEF.md), [INDEX.md](https://github.com/laadkke-arch/agentflow-open/blob/9d728dfe2c2f3a13d9995b5fdc14a252aeddfdad/docs/research/INDEX.md), [dot-control.json의 AF-RES-003 항목](https://github.com/laadkke-arch/agentflow-open/blob/9d728dfe2c2f3a13d9995b5fdc14a252aeddfdad/docs/automation/dot-control.json)이다. GitHub에서 직접 읽었고 `depends_on=[]`이므로 읽어야 할 선행 result_commit/HANDOFF는 없었다. 추가로 읽은 내부 문서는 [STATUS.md](STATUS.md)에 적었다.

허용 경로는 **`docs/workstreams/research/AF-RES-003/`**뿐이다. 해당 경로의 연구 묶음·검토·계약 핀·검사 증거·인계만 썼다. 다른 AF-RES 작업을 선행조건으로 삼지 않았고 기존 표본은 분류·미확인의 예로만 사용했다. 운영 환경·비공개 사용자 자료·계정 권한 변경은 이 작업의 입력이 아니다.

## 3. 실제 변경

| 파일 | 변경 사항 / 이유 | 확인 근거 |
| --- | --- | --- |
| [RESEARCH.md](RESEARCH.md) | 최소 구분, 조건부 A/B/C 조합, 확장·중단 조건, 병합·분리·대체 보존 원칙 | 33개 원문 원장, 동일 사례, 별도 검토 |
| [CASES.md](CASES.md) | 같은 근거와 미확인을 A/B/C에 준 수작업 9개 사례 | 출처 ID 연결, 과잉 추론·과분할 반례 |
| [SOURCES-IDENTITY.md](SOURCES-IDENTITY.md) | repo/docs/service, 배포, rename/fork/후계 원문 11개; 제외 보조 1개 | 자료별 URL·SHA/절·확인일·관측·한계 |
| [SOURCES-MECHANISMS.md](SOURCES-MECHANISMS.md) | 기능 조합·로그·업무 사건 관련 원문 10개 | 직접 포착 제약과 다른 구성 가능성을 분리 |
| [SOURCES-STANDARDS.md](SOURCES-STANDARDS.md) | 식별·provenance·주석·서지·연구자료·기존 표본 원문 12개 | 타 분야 전이 한계와 실패 접근도 기록 |
| [REVIEW.md](REVIEW.md) | 별도 검토자의 7개 반론, 수정 확인, 잔여 이견, 5개 입력 해시 | 6개 원문 재열람과 통합 원고 대조; 전체 33개 재검토는 아님 |
| [task-manifest.json](task-manifest.json) | 시작 SHA·계약 fingerprint·owned_path 고정 | 실제 `start ... --fetch`, 개별 `check ... --fetch` |
| [VALIDATION.json](VALIDATION.json) | 실행 명령, 입력 SHA·파일 해시, 종료 코드, 출력·범위 | 아래 §4 |
| [STATUS.md](STATUS.md), 이 파일 | 최종 진입점·인계·다음 첫 행동 | 앞선 연구 검사의 후속 관리 문서임을 구별 |

묶음별 저장 커밋:

| 묶음 | 커밋 |
| --- | --- |
| 범위·계약 핀 | `bf4dcb88a8e6b9e478c21e3e30447d5608fd395e` |
| 제품·계보 원장 | `414025d0f15ff44b3e19eacc46fe2b21606f12ab` |
| 기능·메커니즘 원장 | `afe9e8a1a65c2e73f039b7de06321ac630b6e367` |
| 표준·다른 분야 원장 | `937c94bdf3cbe9e511a36c0f204eed3676032f54` |
| 같은 사례의 대안 비교·종합 | `8813e129c3119d874ea8d84f59aa054e92d7117d` |
| 별도 검토 | `caf806738b0ed07fe5bce8d4c5c173bada5286b3` |
| 검사 증거 | `1ca4558a62e13800ce558f5bba19210da3b087a2` |
| 최종 상태·인계 | 이 파일을 추가한 마지막 커밋. 아래 조회 명령으로 확인 |

## 4. 실제 검증 결과

검사한 연구/검토 입력은 **`caf806738b0ed07fe5bce8d4c5c173bada5286b3`**다. 정확한 실행 명령 전체·출력·파일별 SHA256는 [VALIDATION.json](VALIDATION.json)에 있다.

| 검사 | 실제 결과 | 범위 / 한계 |
| --- | --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-003/task-manifest.json --fetch` | 종료 0, `passed`, `remote_checked`, errors/outside/unmerged 빈 배열 | Git 계약·허용 경로 검사. 내용의 진실·제품 실행 검사가 아님 |
| 원문 ID·사례·문서 참조·검토 해시 감사 | 종료 0, 원문 33 / 사례 9 / 검토 입력 5개 일치 | 파일 목록과 연결을 확인. 근거의 의미 검토는 REVIEW와 별개 |
| `git diff --check 9d728dfe2c2f3a13d9995b5fdc14a252aeddfdad caf806738b0ed07fe5bce8d4c5c173bada5286b3` | 종료 0 | 해당 커밋까지의 공백 오류 |
| 시작 SHA→검사 SHA 변경 경로·control blob 비교 | 모든 변경이 owned_path, `dot-control.json` 동일 | 최신 통합의 진행 담당 변경과 이 브랜치의 변경을 구별 |
| 원격 커밋 fetch와 로컬 바이트 대조 | 단계별 일치 후 로컬 HEAD 동기화 | 원격 저장을 성공 응답만으로 추정하지 않음 |

GitHub push workflow는 영수증 커밋 `1ca4558...`에서 [success를 보고했다](https://github.com/laadkke-arch/agentflow-open/actions/runs/44560961029). 그러나 `.github/workflows/session-check.yml`이 호출하는 `check-all`은 `workbench/session.py`에서 `docs/tasks/*.json`만 찾는다. **이 작업의 owned_path manifest를 직접 검사한 증거는 위 개별 명령**이다. 16:00:01 UTC 조회 시 [PR workflow](https://github.com/laadkke-arch/agentflow-open/actions/runs/44561042569)는 진행 중이었고, 실제 PR merge checkout SHA는 그 조회에서 확인하지 않았다. 후속 최종 인계 커밋까지 해당 run이 검사했다고 확대하지 않는다.

필수 문서·범위·계약 검사는 직접 수행했고, 실행 불가 때문에 남긴 필수 검사는 없다. **미실시/미확인:** 서비스 API POST, 설치·마이그레이션·FTS/session 조합 실행, D3/D4 제품 적합성, 사용자 시험, 저장안 비용·오병합률, 실제 다른 사용자 대화의 인계, 동적 원문의 전체 snapshot 복원. 이들 성공을 전제로 한 결론을 내리지 않았다. 원문 접근 실패와 대체 원문은 각 원장에 남겼다.

이 인계와 최종 STATUS는 위 검사 SHA 뒤의 관리 문서다. 해당 문서까지 같은 검사에 포함됐다는 주장은 하지 않는다. 다음 담당은 결과 SHA에서 아래 개별 검사와 diff를 다시 실행할 수 있다.

## 5. 판단·근거·미해결

**핵심 판단:** 주소·대상·주장의 의미는 구별하되 항상 서로 다른 영구 객체로 만들 필요는 없다. A의 짧은 메모도 조건을 보존할 수 있다. 반복 중복 귀속에는 B, 독립 정정·상충·전이 판단에는 필요한 부분만 C를 적용하는 조합을 제안한다. 이는 사용자 확정 설계가 아니다.

처음의 단순 결론을 좁힌 반례는 C02(주장 분해 중 관리형 백업의 부정 범위 손실), C05(직접 FTS 포착 제외를 모든 동기화 불가능으로 확대하는 오류), C06(순효과/상태 복원을 업무 사건 이력으로 오인), C09(모드 메모로 충분해 별도 객체가 불필요)다. rename/fork/후계와 외부 프로젝트의 변화는 카탈로그 기록 병합과 분리한다. 병합·분리 시 이전 참조와 미귀속 근거를 남기는 구체 원칙은 RESEARCH §7에 있다.

자료별 URL·확인일·고정 위치와 한계는 세 원장에 있다. 증거는 **D1 32개 + D2 1개**이며 근거 개수를 독립 검증 횟수나 전역 신뢰 점수로 쓰지 않는다. 다른 분야의 식별·주석 원리를 가져왔지만 그 표준 전체나 테이블 수를 채택하지 않았다.

잔여 이견은 C의 작성·정정 비용, 기능을 독립 대상으로 분리할 시점, 여러 작성자의 판정 일치도다. B의 범위 메모가 충분한 안과 핵심 주장만 미리 분리하는 안을 모두 남겼다. 더 복잡한 안으로 확대할 이유는 실제 반복 정정·귀속 실패여야 하며, 특정 자료 개수를 임계값으로 정하지 않았다. 답을 바꿀 최소 확인은 RESEARCH §9, 검토자의 반론은 REVIEW §§4–5를 참조한다.

다른 세션과 의미가 충돌할 수 있는 지점은 제품/기능의 단위, 배포 범위, URL 대표화, 근거와 unknown의 해석이다. 다른 결과가 도착하면 고정 커밋을 읽고 대조해야 한다. 이 연구로 최종 DB·API·검색순위·크롤러·갱신주기를 확정하지 않는다. 공개 원문과 자체 해석만 기록했으며 외부 본문 전체 복제·새 유료 서비스 호출은 수행하지 않았다.

### 공통 색인 변경 제안 — 편집 담당용

`docs/research/INDEX.md`는 수정하지 않았다. 통합 담당이 결과 커밋을 확인한 뒤 다음 한 행을 추가하고, 기존 “새 제품 연구 묶음 없음” 문구의 현행 여부를 정리할 수 있다.

| 고유 ID | 답하는 질문 | 현재 상태 | 파일 | 핵심 의존·충돌 |
| --- | --- | --- | --- | --- |
| AF-RES-003 | 제품·기능·메커니즘·출처를 어떻게 구별하고 최소한 무엇을 저장할까 | 검토됨 / 통합 검토 대기 / 최종 설계 미선택 | `docs/workstreams/research/AF-RES-003/RESEARCH.md` (결과 커밋 고정) | depends_on 없음. identity·scope·근거/unknown·URL 대표화의 의미 충돌을 통합 때 확인 |

## 6. 다음 대화의 첫 행동

1. [PR #5](https://github.com/laadkke-arch/agentflow-open/pull/5)의 현재 head·base·병합 여부를 다시 읽고, 아래 명령으로 최종 HANDOFF 커밋을 식별한다. 다른 작업 사본의 미저장 변경은 먼저 보존한다.
2. 마지막 검사 SHA `caf806738b0ed07fe5bce8d4c5c173bada5286b3`와 현재 작업 head의 diff를 비교한다. 예상 추가분은 검사 영수증·최종 상태·인계다. 연구 본문·사례·원장이 달라졌다면 REVIEW의 입력 해시와 다시 대조한다.
3. 첫 구체 작업은 **AF-RES-003 통합 검토**다. 입력은 PR의 정확한 결과 SHA, RESEARCH §1, CASES C02/C05/C07/C09, REVIEW의 잔여 이견이다. 기대 결과는 조건부 대안과 미확인을 유지한 색인 등록·채택/보류 판단이며, 자동으로 최종 스키마를 확정하는 것이 아니다.
4. B/C의 경계를 더 좁혀야 하면 C02·C09의 같은 메모를 서로 다른 작성자가 읽고 범위를 복원하는지, C07에 새 관측 하나가 들어왔을 때 어떤 문장만 정정하는지부터 수작업 대조한다. 새 입력/평가팩을 선행조건으로 만들지 않는다.
5. 다른 세션 의존성은 없다. 새 구현·운영 환경·유료 호출은 이 인계의 실행 지시가 아니다. 그런 목표가 새로 배정될 때 버전·입력·보존 요구를 고정한다.

이미 저장소 checkout이 있는 후속 담당의 재조회·검사 명령:

```sh
git fetch --no-tags origin
git rev-parse origin/work/research-af-res-003
git log -1 --format=%H origin/work/research-af-res-003 -- docs/workstreams/research/AF-RES-003/HANDOFF.md
git show origin/work/research-af-res-003:docs/workstreams/research/AF-RES-003/HANDOFF.md
git diff --name-status caf806738b0ed07fe5bce8d4c5c173bada5286b3 origin/work/research-af-res-003
git diff --check 9d728dfe2c2f3a13d9995b5fdc14a252aeddfdad origin/work/research-af-res-003
```

작업 브랜치의 해당 결과 SHA를 checkout한 뒤 실행한다:

```sh
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-003/task-manifest.json --fetch
```

문서 감사의 정확한 Python 명령은 VALIDATION.json의 `documentation_audit.command`에 있으며, 당시 입력 SHA와 해시는 같은 파일에 있다. 자료가 추가된 뒤에는 과거 수량 검사를 새 자료의 평가 기준으로 사용하지 않는다. 통합 담당은 이 HANDOFF를 읽는 것으로 후속 세션의 실제 실행까지 확인했다고 처리하지 않는다.
