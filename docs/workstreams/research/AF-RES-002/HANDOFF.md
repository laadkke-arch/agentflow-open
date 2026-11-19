# AF-RES-002#1 — 연구 인계

## 1. 식별

- 작업 ID / 시도: **AF-RES-002 / 1**.
- 배정 종류: `web-pro`. 실제 수행: ChatGPT의 관리형 Linux 작업 공간에서 공개 검색·GitHub 읽기·문서 작성·GitHub 커밋을 수행했다.
- 실제 모델: 세션에서 제공된 식별은 **GPT-6 Astra Pro**다. Dot 화면의 모델 선택·새 웹 대화 생성은 관측하거나 시험하지 않았다.
- 작업자 참조: 공개 작업 URL 없음. 이 저장소·브랜치와 `AF-RES-002#1`로 조회한다. 내부 병렬 조사자 두 명과 별도 검토자 한 명을 사용했다.
- 저장소 / 브랜치: `laadkke-arch/agentflow-open` / `work/research-af-res-002`.
- 시작 커밋: **`46c874671c6d066292750401d75af50136ef95d6`**, 시작 시 확인한 `chore/workspace-foundation`의 최신 커밋. 작업 브랜치가 없어 그 커밋에서 만들었다.
- 마지막 본문·검토 검사 커밋: **`3bf691afcb3ef398b84cd745875a03814d0effaa`**.
- 이 파일 작성 전 마지막 확인한 원격 저장 커밋: **`d34e490f42de2620632f76c51d3c5871d7e6c539`**. 해당 커밋의 `VERIFICATION.json`을 GitHub에서 다시 읽었다.
- 최종 결과 커밋: **이 HANDOFF를 추가한 커밋**이다. 파일이 자기 커밋 SHA를 포함할 수 없으므로 작성 전 확인 SHA와 구별했다. 진행 담당은 브랜치 최신 SHA와 이 파일의 추가 커밋을 재조회해 `result_commit`에 사용한다. 마지막 커밋은 이 파일만 추가한다.
- 마지막 실제 진행 증거: 검토 묶음의 검사 통과, 검사 기록의 원격 커밋 및 재열람. 작성 시 최종 확인 **2026-11-19 15:41:30 UTC / 2026-11-20 KST**.
- PR: 생성하지 않았다. 통합 브랜치나 main에 병합하지 않았다.
- 상태: **REVIEW_READY**. 연구 범위 완료, 인계를 막는 사유 없음. `dot-control.json`의 상태는 수정하지 않았다.

## 2. 사용자 요구와 작업 범위

같은 목적의 완성품과 다른 분야의 유용한 부분·원리를 어떻게 함께 찾을지 조사했다. 검색 전에 제품명이 없는 개발 문제 두 개를 고정하고, 각각 완성품·부품·다른 분야 메커니즘 경로를 실제 공개 검색과 원문으로 비교했다. 최소 20개 자료를 읽고 주소·확인 내용·한계와 첫 결론을 제한하는 반례를 남기라는 요구를 따랐다.

쓰기 허용 경로는 **`docs/workstreams/research/AF-RES-002/`뿐**이다. 모든 결과 파일이 그 안에 있다. 공통 색인·계약, `dot-control.json`, 제품 코드, 기존 AgentFlow Studio는 바꾸지 않았다. 새 검색기·제품 DB·공통 벤치마크·최종 순위 알고리즘을 만들지 않았다.

### 읽은 기준과 고정 입력

주요 기준은 모두 시작 SHA에서 GitHub로 직접 읽었다.

| 기준 | 고정 원본 |
| --- | --- |
| 작업 규칙 | [AGENTS.md](https://github.com/laadkke-arch/agentflow-open/blob/46c874671c6d066292750401d75af50136ef95d6/AGENTS.md) |
| 현재 상태 | [STATE.md](https://github.com/laadkke-arch/agentflow-open/blob/46c874671c6d066292750401d75af50136ef95d6/STATE.md) |
| 자동화와 작업 경계 | [DOT_AUTOMATION.md](https://github.com/laadkke-arch/agentflow-open/blob/46c874671c6d066292750401d75af50136ef95d6/docs/DOT_AUTOMATION.md) |
| 연구 절차 | [RESEARCH_WORKFLOW.md](https://github.com/laadkke-arch/agentflow-open/blob/46c874671c6d066292750401d75af50136ef95d6/docs/RESEARCH_WORKFLOW.md) |
| AF-RES-002 항목 | [dot-control.json](https://github.com/laadkke-arch/agentflow-open/blob/46c874671c6d066292750401d75af50136ef95d6/docs/automation/dot-control.json) |
| retrieval 질문 범위 | [RESEARCH_BRIEF.md](https://github.com/laadkke-arch/agentflow-open/blob/46c874671c6d066292750401d75af50136ef95d6/docs/product/RESEARCH_BRIEF.md) |
| 기존 연구와 네 후보 연결 표본 | [INDEX.md](https://github.com/laadkke-arch/agentflow-open/blob/46c874671c6d066292750401d75af50136ef95d6/docs/research/INDEX.md), [discovery-case-2026-11-19.json](https://github.com/laadkke-arch/agentflow-open/blob/46c874671c6d066292750401d75af50136ef95d6/docs/research/discovery-case-2026-11-19.json) |

추가로 START_HERE, RESEARCH_PROTOCOL, CLOUD_WORKFLOW, 협업 README와 HANDOFF_TEMPLATE을 읽었다. 계획의 고정 입력 `23d71361ca3fbf51a66793121718b16f01e03f37` 및 NEXT_TASKS를 대조했고, AF-DOT-001 인계는 `ba62d1fa8ce5ff9631c20167a9fa4dc61cd1daea`, AF-DOT-002 인계는 `06a57eba60c64389c614b5ce01238d9c4e337fbf`에서 읽었다. 이 연결·출처 ID 시험은 검색 성능의 증거로 사용하지 않았다.

AF-RES-002의 `depends_on`은 **빈 배열**이다. 의존 작업의 result_commit을 기다릴 항목은 없었다. 다른 새 연구 작업 AF-RES-001·003·004의 결과를 읽거나 선행조건으로 사용하지 않았다. 운영 계정 접속, 후보 제품 실행·배포, 유료 API 호출, 권한 변경, 상시 수집은 수행하지 않았다.

## 3. 실제 변경과 저장된 묶음

| 파일 | 내용과 확인 방법 |
| --- | --- |
| [PROTOCOL.md](PROTOCOL.md), [manifest.json](manifest.json) | 제품명 없는 두 문제·세 경로·근거 등급·범위를 고정. 기존 세션 도구로 manifest 생성·검사 |
| [METHODS.md](METHODS.md) | 검색 방법의 작동 원리·비용·설명·결합 조건, 기존 네 발견 채널의 역할, 반대 문헌 |
| [CASE_P1.md](CASE_P1.md) | 문서 묶음 처리의 실제 탐색, 후보 조건, 실패·재시도·캐시·공개 경계 |
| [CASE_P2.md](CASE_P2.md) | 오프라인 공동 기록의 실제 탐색, 보존·수렴·표시·의미 충돌 구별 |
| [RESEARCH.md](RESEARCH.md) | 두 사례의 종합 판단, 실제 전이와 가설, 오탐·관측 누락·방법 조합·최소 후속 확인 |
| [methods.json](evidence/methods.json), [p1.json](evidence/p1.json), [p2.json](evidence/p2.json) | 정확한 질의·시각·필터·관측 후보·선택/보류·출처 위치·확인 내용·한계 |
| [REVIEW.md](REVIEW.md), [review.json](evidence/review.json) | 별도 검토자의 원문 14개 재열람, 수정 확인, 미해결 이견, 대상 8개 파일의 지문 |
| [VERIFICATION.json](VERIFICATION.json) | 실제 명령·입력 SHA·출력·종료 코드·집계·허용 경로·계약 검사·원격 재열람 |
| HANDOFF.md | 이 인계. 마지막 커밋으로 추가 |

실제로 GitHub 브랜치에 저장한 묶음은 다음과 같다.

| 커밋 | 완료한 묶음 |
| --- | --- |
| `940ea97b67c155eee6c34d909f0dfe0aa827a21e` | 두 문제와 관측 규칙·manifest |
| `ec88b9f3503140e36bc2d47f88deb63699e1116d` | 방법·발견 채널의 원문 비교 |
| `f6e7c1ac22ffc91de7718de162132e1d7ed24133` | P1 사례와 출처·질의 기록 |
| `92acf27fde99d5b9ca9abd4ca85aff9f14d87e98` | P2 사례와 출처·질의 기록 |
| `5b9c3c925d0f3a76c88b0fde4e0a1a7643081d30` | 종합문서, 반례·경로·질의 집계 보정 |
| `3bf691afcb3ef398b84cd745875a03814d0effaa` | 독립 검토와 마지막 공백 보정 |
| `d34e490f42de2620632f76c51d3c5871d7e6c539` | 실제 검사 기록 |
| 이 파일의 추가 커밋 | 최종 인계 |

셸의 HTTPS push는 인증 수단이 없어 실패했다. 사용 가능한 GitHub 연결의 tree/commit/ref 갱신으로 각 묶음을 저장했고, 예상 부모 SHA를 확인하며 fast-forward했다. 이후 fetch로 로컬을 맞췄다. 인증 실패가 남은 차단 사유는 아니며 로컬 미전송 커밋을 결과로 제시하지 않는다.

## 4. 실제 검증 결과와 재검사 명령

검사한 연구·검토 커밋은 **`3bf691afcb3ef398b84cd745875a03814d0effaa`**다. 전체 명령 문자열·출력·입력 지문은 [VERIFICATION.json](VERIFICATION.json)에 있다. 이 검사 기록과 HANDOFF는 그 뒤의 기록 추가이므로, 앞선 검사에서 미래 커밋을 이미 시험했다고 표현하지 않았다.

| 검사 | 실제 결과 |
| --- | --- |
| `python -m workbench.session check … --fetch` | 종료 0, passed, remote_checked, 허용 경로 밖 변경·병합 충돌·오류 없음 |
| `git diff --check 46c874671c6d066292750401d75af50136ef95d6 HEAD` | 최종 검사 종료 0. 앞선 검사에서 찾은 P1 말미 빈 줄 1개를 수정·커밋한 뒤 통과 |
| Python 출처·질의 무결성 검사 | 종료 0. 출처 45개 기록 중 열람 44, 본문/문서/코드 관련 절 43와 초록 1; 중복 URL 없음 |
| 근거 연결·코드 pin 검사 | 출처 참조 116개·질의 참조 38개 모두 유효. D2 코드 5개 모두 40자리 commit URL |
| 검토 대상 지문 | 8개 모두 현재 파일과 일치 |
| 상대 링크 파일 대상 | 27개 검사, 누락 0. 제목 anchor와 원격 URL 가용성 자동 검사는 범위에 넣지 않음 |
| 변경 범위·공통 제어 파일 | 소유 경로 밖 변경 0. dot-control blob `c1052b87254895cdca066169eb154b6681b29be7` 동일 |
| 작업 트리 | 검사 커밋에서 `git status --porcelain=v1 --untracked-files=all` 출력 없음 |
| 원격 재열람 | 검사 커밋의 RESEARCH와 `d34e490…`의 VERIFICATION을 GitHub에서 읽음 |

검사 때 통합 브랜치는 `9d728dfe2c2f3a13d9995b5fdc14a252aeddfdad`로 전진했지만 계약 SHA-256은 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`로 같았고 검사에 통과했다. 다른 작업의 변경을 이 연구 브랜치에 병합하지 않았다.

### 다음 세션에서 실행할 명령과 입력

저장소 루트의 해당 작업 브랜치에서 실행한다. 아래 첫 조회는 원격 결과를 확인하기 위한 것이며 이 파일의 자기 SHA 문제를 해결한다.

```bash
git fetch origin refs/heads/work/research-af-res-002:refs/remotes/origin/work/research-af-res-002
git rev-parse origin/work/research-af-res-002
git show origin/work/research-af-res-002:docs/workstreams/research/AF-RES-002/HANDOFF.md
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-002/manifest.json --fetch
git diff --check 46c874671c6d066292750401d75af50136ef95d6 HEAD
git status --porcelain=v1 --untracked-files=all
```

검사받은 본문·검토 파일과 현재 파일이 같은지 확인하는 입력은 VERIFICATION의 `audit.content_sha256`이다.

```bash
PYTHONDONTWRITEBYTECODE=1 python - <<'PY'
import hashlib, json
from pathlib import Path
p = Path('docs/workstreams/research/AF-RES-002')
report = json.loads((p / 'VERIFICATION.json').read_text())
for name, expected in report['audit']['content_sha256'].items():
    assert hashlib.sha256((p / name).read_bytes()).hexdigest() == expected, name
print('verified research/review content matches recorded inputs')
PY
```

필수 연구 검사 중 실행하지 못한 항목은 없다. 제품 설치·실행·중단 주입·두 장치 사용자 시험·배포·D4 목표 통합, 검색 알고리즘의 성능 실험은 **미실시**다. 두 사례는 실제 제품 채택을 확정하지 않았으므로 임의 버전의 설치 명령이나 가상의 공통 실행 CLI를 만들지 않았다.

후속 채택 검증이 필요하면 [P1 §8](CASE_P1.md#8-수정한-결론과-다음-검증의-입력)의 정상/손상/중복 입력·공개 전후 중단과 [P2 반례](CASE_P2.md#4-첫-유망-결론을-깨는-반례)의 두 장치 상충·앱 재시작·의미 모순을 입력으로 사용한다. 첫 행동은 실제 후보의 릴리스·설정과 관측할 결과를 고정해 후보별 명령을 정하는 것이다. 이것은 연구 완료를 막는 대기 실행이 아니라 별도 채택 단계다.

## 5. 판단과 근거

**발견 경로와 후보가 책임지는 요구 부분을 유지하며 비교하는 조합을 제안한다.** 완성품·부품·원리 후보를 단일 점수로 섞거나 항상 같은 순서로 찾을 효과는 입증하지 못했다. 전체 사용 경험이 필요하면 목적·제품군에서, 필요한 부분이 정해졌으면 그 동작·실패 조건에서 시작할 수 있다.

| 질문 | 남긴 판단 | 최초 결론을 제한한 근거 |
| --- | --- | --- |
| P1 문서 묶음 처리 | 완성품 후보를 유지하며 버전·기본값·영속 성공·공개 상태를 확인 | 중복 탐지와 거부 정책은 다름. retry/ACK/작업 ID, 계산 캐시, 공개 유일성도 서로 다른 보장 |
| P2 오프라인 공동 기록 | 보존·수렴·상충 표시·의미 판단을 나눠 요구와 연결 | 보존된 다른 수정이 기본 조회에서는 숨겨질 수 있음. 명시적 분기 이력도 검토 부담을 만듦 |
| 다른 분야 전이 | 원 분야의 관계·전제를 설명할 수 있을 때 가설로 보존 | Reflow의 분야 사용은 제작자 문서, TreeDB는 연구 제안, NASA는 시제품 보고. P1/P2 적용 성공으로 승격하지 않음 |
| 검색 방법 | 목적·부분·추상 관계의 관측 차이를 기록하고 근거로 다시 좁힘 | 표본·주석·너무 넓은 추상·평가 후보 집합 편향 때문에 보편적 우위를 주장할 수 없음 |

서로 다른 외부 자료 **44개**를 직접 열었다. **43개는 본문·문서·코드의 관련 부분, 1개는 초록·서지**다. D1 39개와 D2 5개이며 D3/D4는 없다. 주 작성자는 이 중 23개를 직접 열람했고, 별도 검토자는 14개를 다시 열어 교차 확인했다. 재열람을 총수에 더하지 않았다. 차단 원문·검색 snippet·같은 논문 미러·내부 지침도 성공 자료 수에 포함하지 않았다.

실제 자료별 주소·확인일·버전/위치·관측·한계는 세 근거 JSON에 있다. 고정 소스와 live 문서를 구분했다. 특히 Paperless의 기본 브랜치 스냅샷을 안정 릴리스나 사용자의 배포 동작으로 일반화하지 않았고, 같은 작업 ID에 관한 Celery 경고를 `Task.retry` 자체의 잘못으로 해석하지 않았다.

P1의 질의는 고유 9개·제출 10개·호출 6회, P2는 고유 7개·제출 10개다. 초기 혼합 반환·반복 제출·실패한 API URL 요청을 독립된 성공 표본으로 계산하지 않았다. 다른 경로에서 나중에 찾은 사례는 **이번 반환 창의 관측 누락**으로만 남겼다. 키워드 역할 혼동·동명이름은 관측했으나 인기도의 인과 효과, 전체 재현율·누락률·검색 품질 우위는 측정하지 않았다.

독립 검토는 최초 결론의 반례, canonical 출처 연결, 질의 수 단위, 순서 일반화, 문헌과 실제 실행의 구분을 확인했다. 검토 범위에서 인계를 차단할 확정 사실 오류는 없었으나 어느 순서·결합 비중이 더 유리한지는 미해결로 남겼다. HANDOFF는 검토자의 8개 대상 파일에 포함하지 않았다.

외부 근거는 공개된 문서·논문·코드의 필요한 범위만 읽고 요약했다. 후보 라이선스 전체, 운영 권한, 비용, 실제 배포의 적합성을 확정하지 않았다. AlternativeTo의 자료 재사용 제한과 source/API 접근 조건은 METHODS에 한정해 기록했으며 제품 DB 수집·재배포로 확대하지 않았다.

## 6. 다음 대화의 첫 행동

1. 위 명령으로 **`work/research-af-res-002`의 최신 SHA와 이 HANDOFF 추가 커밋**을 재조회한다. 입력 기준은 `46c8746…`, 실제 연구 검사 기준은 `3bf691a…`이며 서로 바꾸지 않는다.
2. [RESEARCH.md](RESEARCH.md) → 두 CASE → [REVIEW.md](REVIEW.md) → [VERIFICATION.json](VERIFICATION.json) 순으로 수용 근거와 남은 이견을 확인한다. 이 읽기 순서는 인계 편의를 위한 것이며 검색 방식의 우위 주장이 아니다.
3. 진행 담당의 첫 구체 작업은 **AF-RES-002 수용 여부 판단과 최종 result_commit 연결**이다. 작업자는 dot-control을 수정하지 않았다. 새 AF 작업 ID나 선행조건은 만들지 않았다.
4. 수용 후 공통 `docs/research/INDEX.md`에 이 종합문서·두 사례·검토·인계를 연결하는 항목을 추가할 수 있다. 제안 표기는 “AF-RES-002 — 완성품·부분·타 분야 원리의 실제 탐색 비교, 44개 원문(관련 본문43/초록1), D1/D2, D3/D4 미실시”다. 공통 색인 변경은 이번 브랜치에 하지 않았다.
5. 실제 채택을 판단해야 하는 다음 작업이라면 P1 후보의 정확한 버전·중복 정책 또는 P2의 기록 한 종류·상충 인지 기준 중 선택을 바꿀 한 가지부터 고정한다. 아직 선택되지 않은 제품의 실행 성공을 이 인계에서 이어받지 않는다.

막힌 이유: **없음**. 연구 인계에 필요한 추가 확인·승인을 요청하지 않는다. 다른 새 연구 세션의 결과 의존성도 없다. 최종 커밋 후 원격 HANDOFF와 작업 트리를 다시 확인하고 종료한다.
