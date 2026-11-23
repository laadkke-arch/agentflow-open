# AF-RES-102 재현 — 사전 자료와 사후 판독 분리

아래는 표본/예측을 바꾸지 않고 기록을 다시 읽는 절차다. 정확한 검사 SHA·UTC·종료값은 결과 커밋 후 작성한 검증 영수증과 마지막 HANDOFF를 따른다. 인터넷 접근 실패는 부재·미사용·미생성으로 변환하지 않는다.

## 1. 입력과 브랜치

```sh
git fetch origin chore/workspace-foundation work/research-af-res-102 work/research-af-res-098
git switch work/research-af-res-102
git rev-parse HEAD
git status --short
```

기존 작업 사본에 미저장 변경이 있으면 덮어쓰지 않는다. [input-contract.json](evidence/input-contract.json)에서 시작 통합판·계획판·운영 의존판·고정 연구 입력의 차이와 사용 blob을 읽는다. 시작 계약은 저장소의 `workbench.session start` 실제 실행으로 생성했다. 연구 규칙을 덧붙인 manifest의 `research` 필드는 소스 버전·모집·예측을 명시하며 생성된 contract/base/dependency 값을 바꾸지 않는다.

## 2. 사전 묶음만 읽기

새 결과를 보지 않은 재현자가 필요하면 체크포인트 ①의 고정 SHA에서 아래 파일을 먼저 읽는다. `git show SHA:PATH` 또는 같은 SHA의 GitHub blob을 사용한다.

- `SCOPE.md`, `manifest.json`.
- `frame.csv`와 프로젝트별 `evidence/ggplot2/frame.csv`, `evidence/matplotlib/frame.csv`.
- 프로젝트별 `editions.json`, `selected-general.json`, `stage1.json`, 이전판의 tree 투영/접근 영수증.
- [stage1-seal.json](evidence/stage1-seal.json)의 파일 지문.

페이지 경로순 첫40 적격 예제와 앞선 배제 이유를 확인한다. 각 옛 절 경로는 버전 루트 상대 `page.html#fragment`이다. 프로젝트 문자열은 정확히 `ggplot2`, `Matplotlib`이다.

```python
import hashlib
key = f"AF-RES-102|{project}|{old_relative_section_path}"
sort_key = hashlib.sha256(key.encode("utf-8")).hexdigest()
```

각 프로젝트 후보를 `(sort_key, old_relative_section_path)`로 정렬해 일반층 첫2개가 일치하는지 본다. 첫 설명용 그림은 본문 절의 순서를 따른다. 페이지 이름이나 가장 흥미로운 후속 그림으로 바꾸지 않는다.

## 3. 경로 자료와 예측만 읽기

체크포인트 ②의 SHA에서 새 tree 경로·대응 소스 path/blob 투영, `predictions.csv`, `evidence/prediction-seal.json`을 읽는다. 아직 사후 `lineage.csv`, `audit.json`, RESULT를 열지 않는다.

일반층을 제외한 후보 중 옛 자원 상대경로가 완전 다음판 tree에서 없는 후보를 해시순 첫2개 고른다. 이어 옛 자원 경로가 남고 대응 소스 경로가 없어졌거나 blob이 달라진 후보를 해시순 첫2개 고른다. ggplot2의 비교 소스는 `man/<page>.Rd`, Matplotlib은 실제 발행 본문의 Python source download 경로다. 층당 부족하면 결원으로 남긴다. 내장 그림으로 옛 상대경로가 없는 경우를 삭제 후보로 넣지 않는다.

예측 규칙은 정확 상대경로 존재 YES, 완전 tree에서 부재 NO, 불완전/모호 미확인이다. 경로 이름 변경이나 내장 후계는 규칙이 의도적으로 보지 못한다. 봉인시각은 사후 접근시각보다 앞서야 하며 첫 새본문/새그림 시각은 모든 조사자의 기록을 합쳐 비교한다.

## 4. 봉인 뒤 판독 자료 읽기

예측을 확인한 다음 `lineage.csv`와 프로젝트별 audit/receipts를 읽는다. 사례의 두 판에서 다음 연결을 따른다.

1. 고정 공식 발행 commit/버전 루트 → 정확 HTML fragment 또는 동급 제목 경계.
2. 절 안 `src`, `srcset`, `picture`, base, data URL·JS 또는 내부 패키지 member.
3. 실제 도착 payload의 응답/형식/바이트 길이/SHA-256, 필요하면 직접 연 소스·캡션/기능.
4. 옛 그림 역할을 잇는 현재 참조인지, 옛 파일이 단지 남은 것인지, 절/후계가 없어졌는지.
5. 배포 포함 P, 해당 논리 예제의 절 사용 U, 특정 실행의 신규 바이트 생성 G를 각각 판정한다.

같은 해시나 다른 해시만으로 4번을 결정하지 않는다. `legacy_path_P`는 옛 경로 생존이며 실제 따라간 자원의 P와 다를 수 있다. U=NO는 정확 절과 가능한 대체 표현을 조사한 범위의 음성이다. 이름만 비슷한 다른 예제를 후계로 삼지 않는다. G는 실제 job의 입력/환경/출력 digest 연결이 없으면 미확인으로 남긴다.

프로젝트의 수집 스크립트는 URL·캐시를 읽고 속성·지문을 추출한 도구다. 과거 자료를 지금 재요청하는 것은 당시 생성 실행의 재현이 아니다. 원본 전체를 저장소에 복제하지 않으며 직접 재요청한 캐시는 각 프로젝트 `.gitignore` 범위에 둔다.

## 5. 보조 반례와 타분야

보조 후보 순서는 사전에 기록된 나머지 모집틀 해시순이며 프로젝트당 최대20개다. 주표본의 결원을 보조 사례로 채우지 않는다. ① 경로 잔류/절 미사용 ② 경로 소멸/다른 자원으로 같은 목적 ③ 이름·hash 동일/목적 변경 ④ 바이트 변경/같은 목적의 네 유형과 미발견 범위를 각각 읽는다.

[타 분야](evidence/cross-domain/)에서는 EPUB 파일 하나의 container→OPF→spine/nav→XHTML/JS/CSS 참조와 실제 멤버, wheel의 RECORD→entry_points→모듈 정의를 따라간다. ZIP 목록과 RECORD 해시 검사는 포함/무결성을 검증하며 reader 표시나 entrypoint 실행을 증명하지 않는다. 외부 패키지를 설치하거나 entrypoint를 실행할 필요가 없다.

## 6. 산술·자료수·검사

`counts.json`은 각 프로젝트×층의 TP/FP/FN/TN/유보/결원과 실제 양성·음성 분모를 담는다. 세 층의 비율을 합산하지 않는다. `sources.jsonl`의 산입 여부·저작 계보·동일 바이트·중복 사유를 먼저 확인하고 범주별 고유 수를 계산한다. 실패 응답·미리보기·자동 적격성 스캔만 한 자료·상속 098 자료는 신규 자료에 더하지 않는다. 직접 읽어 발행 범위의 완전성과 포함을 확인한 공식 deployment listing은 별도의 1차 근거다.

작업별 계약 검사와 공통 검사는 결과 commit에서 다음 명령으로 실행한다. 실행일/종료값/범위는 최종 영수증을 확인한다.

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-102/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

공통 `sessions`가 `no_active_sessions`이면 그 과정의 종료0을 이 manifest의 자동검사 성공으로 표시하지 않는다. 명시적 작업별 check 결과와 실제 자동검사 세션 수를 별도로 보고한다. GitHub에 고정한 결과판의 필수표·대표 증거·이 파일을 다시 연 영수증을 읽고 HANDOFF의 마지막 단독 commit을 확인한다.

## 7. 정확한 체크포인트와 재계산 명령

| 단계 | 원격 commit | 읽기 순서 |
|---|---|---|
| ① 판·옛 모집·일반층 | 5f664a87df16f453151ec985e9ad37913e3bda90 | SCOPE, manifest, frame, selected-general, stage1-seal |
| ② 새 목록·층·예측 봉인 | f1c5d6ff927fd5fbe108565598810ca7e94c5753 | 새 tree 투영, predictions, stage2 노출 일지, prediction-seal |
| ③ 사후 근거 | be9c4cfa09a59da937d40f71cdf7c675fb42c0fa | 양판 본문·payload·소스·build 검색·보조20씩·교차 분야 |
| ④ 최종 통합·별도 검토 반영 | 최종 HANDOFF가 지정한 result SHA | root lineage/sources/counts/RESULT/SELF_CHECK와 검토 기록 |

각 commit의 원격 확인 UTC와 변경 파일 지문은 evidence/checkpoints.json에 있다. 현재 파일과 단계3의 source ledger를 혼합해 고유 수를 계산하지 않는다. 단계3은 잠정116, 단계4는 별도 검토로 발견한098 동일저작5개를 뺀111이다. 원천 GG ledger57을 보존한 이유와 최종52의 대응은 source-reconciliation.json에 있다.

아래 검사는 파일을 수정하지 않고 봉인 지문·모집 hash·예측/관측 join·혼동표·자료수·표의 행수·반대 검토 반영을 재계산한다. 네트워크 요청·예제 실행·역사적 생성의 검사는 아니다.

~~~sh
python -B docs/workstreams/research/AF-RES-102/tools/verify.py
~~~

다음 두 통합 명령과 프로젝트의 수집/분석 스크립트는 결과 파일을 다시 쓴다. 따라서 보존 중인 봉인 사본에서 바로 실행하지 않는다. 별도 사본에서 입력 SHA를 확인한 뒤 결과를 비교한다. assemble_evidence.py는098 고정 commit이 로컬 Git 객체에 있어야 하며, 네트워크 없이 해당 sources.jsonl을 읽어5개의 계승 중복을 제외한다.

~~~sh
python -B docs/workstreams/research/AF-RES-102/tools/assemble_evidence.py
python -B docs/workstreams/research/AF-RES-102/tools/assemble_result.py
~~~

자료별 수신은 evidence/ggplot2 및 evidence/matplotlib의 수집 스크립트와 receipts URL을 사용한다. 무조건 전체 네트워크 조사를 반복할 필요는 없다. 본문 하나의 사용 판정이 의심되면 그 case_id의 두 HTML 정확 경계, 실제 src/srcset, 최종 payload, 논리 소스만 먼저 다시 연다. G가 의심되면 build-search/generation-search에 기록된 SHA·날짜 창을 입력으로 보존 job과 출력 digest 연결을 찾는다. 현재 재빌드 결과를 그 빈칸에 쓰지 않는다.

원격 고정판 재열람은 아래처럼40자리 결과 SHA를 입력한다. 각 응답을 Git의 같은 commit blob과 비교하며 성공·실패·UTC·HTTP·SHA-256을 출력 파일에 기록한다. 출력 파일 경로는 허용 경로 안이어야 한다.

~~~sh
python -B docs/workstreams/research/AF-RES-102/tools/readback.py --commit RESULT_SHA --output docs/workstreams/research/AF-RES-102/evidence/validation/readback.json
~~~

readback의 기본22개 파일은 필수3표, 자기검토, 재현 절차, 모집/예측/관측/자료수, 대표 양프로젝트 audit와 교차 분야 실물 감사, 원 PNG4개와 그 출처 색인을 포함한다. 이는 새 외부 자료 산입이 아니라 저장한 결과가 GitHub에서 같은 바이트로 읽히는지의 검증이다.
