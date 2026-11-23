# AF-RES-096 · 읽기 순서와 재현

이 묶음은 새 Stack Overflow 요청8개의 동일한 두 질의·네 본문 접근에서, 주 도구4파일 노출(A)과 주 도구2+인접2파일 노출(B)을 비교한다. 경계6·같은범위대조2이며, 사전 완결은 양쪽5/어느쪽도3/A만0/B만0이다. 자료 하한46/24는 충족했지만 지정 의존 SHA와 현재 원격 끝의 불일치로 성공 계약 manifest가 생성되지 않아 최종 상태는 **PARTIAL**이다. 문서 완결과 원 사용자 실행 성공을 분리한다.

1. [RESULT.md](RESULT.md): 원 요청8행, 경로16행, 비교8행을 먼저 읽고 분모·방법·사후·다른분야·정확히3약점으로 이동한다.
2. [SELF_CHECK.md](SELF_CHECK.md): Q1–Q7의 답·직접 URL·반례탐색·한계·다음 최소 확인을 대조한다.
3. [cards.md](cards.md): 질문자·유지관리자·결과 편집자에게 줄 최대2링크와 한 가지 질문. 사후 편집안이며 사전 반환과 다르다.
4. [HANDOFF.md](HANDOFF.md): 마지막 단독 커밋의 상태·원격 SHA·검사 결과·첫 행동·색인 제안.

## 원장과 고정 입력

| 파일 | 의미 |
| --- | --- |
| SCOPE.md | ①의 사전 범위·시작 SHA·의존·예상 반례. RUNNING 표지는 당시 기록으로 남겼으며 최종상태는 RESULT/HANDOFF를 따른다. |
| frame.csv | 모집76행, 원순번·제외이유·가장이른 revision. 두 수집기의 원 필드를 합쳐 보존했으므로 jq의 decision_reason/selected와 pandoc의 reason/selected_case 별칭을 함께 읽는다. |
| protocol.json | 최종①의13조건·두 질의·파일 단위 순위·tie·merge·600자·예산·기억 고지. selected.json의 초기 제안보다 우선한다. |
| corpus-plan.json / corpus-files.jsonl | 게시 전 비교판8프로젝트와3,560파일 정체성·hash. 사전 archive 구축비용은 evidence/corpus-build-attempt1.json 및 receipts에 별도. |
| exposure.jsonl / evidence/ranking/ | 검색32·노출16·시도64·같은파일 절이동194 및 질의별/합친 전체48순위파일. 미노출/0점도 원순위를 보존. |
| evidence/routes/ | 경로별 exposure/access/judgment. ② 이후 불변. 완결로 판정한 경로의 모든 조건은 반환≤2파일과 연결된다. 미완결 경로의 추가 진단 근거는 별도로 표시한다. |
| pairs.csv / evidence/pre-outcome-metrics.json | ②의 사전 A/B와 절차상 엄격 비교. 후기 공개답이나 실행으로 고치지 않았다. |
| outcomes.csv / evidence/post-jq/ / evidence/post-pandoc/ | ② 원격 봉인 뒤 최초답·수정·채택·질문자30일 행동·답변자/연구자 실행·사후 링크의 귀속. |
| sources.jsonl / evidence/source-counts.json | 원 기록169행과 고유1차46의 하한 계산. canonical 필드와 original_note/원파일/행을 함께 보존. |
| evidence/post-evaluation-sensitivity.json | P3를 옵션만의 답으로 좁히는 사후 민감도(양쪽4/8)와8질문ID/독립 실제문제사건 미확인의 구분. 사전승패는 불변. |
| evidence/crossdomain/ | Sphinx/Graphviz, GDAL/PROJ의 알려진 조건 대조14원문. 신규 요청 발견 기여0. 라이선스 고지 포함. |
| evidence/audit/ | 별도 순위·접근·source·displacement·최종표 감사와 루트/태그 담당의 검토. 최초 오탐·경고 보존. |
| manifest.json | **성공 manifest 아님.** 지정 start의 종료값2, 원하는 고정계약과 실제 원격 의존 끝을 기록한 실패 영수증. |

## 다시 계산하기

저장소 루트에서 실행한다. 아래 두 생성기는 최종 통합 산출물을 다시 쓰므로 보존된 결과를 검토할 때는 별도 checkout에서 실행한다. 봉인 입력 파일을 변경하는 코드는 아니다.

```sh
python -B docs/workstreams/research/AF-RES-096/build_sources.py
python -B docs/workstreams/research/AF-RES-096/assemble_result.py
```

독립 감사 코드는 `evidence/audit/audit_ranking.py`, `audit_routes.py`, `audit_sources.py`, `audit_displacement.py`, `audit_unified_sources.py`다. archive·R0 본문 캐시는 Git에서 제외되어 있어 새 checkout에서 필요한 원문은 각 corpus/recruit/prepare 스크립트의 고정 URL·GUID·hash를 따라 재구축한다. 직접 확인 없는 cache 재생성을 새 연구자 열람으로 세지 않는다. Git full history가 있어야 원격 봉인 SHA 대조와 저장소 bundle 복원 검사가 가능하다.

## 실행 재현과 미실시

jq는 `evidence/post-jq/prepare_runtime.py`로 공식1.7.1 자산과 checksum을 확인한 뒤 `reproduce_runtime.py`로 커밋된 fixture를 재생할 수 있다. wrapper는 구문 검사만 했으며 실제 관측13회는 `run_frozen_filters.py`와 `run_boundary_counterexample.py`가 남긴 기록이다. 원잘림 JSON 실패와 범위밖 quoting 실패는 의도적으로 지우지 않았다.

Pandoc은 `evidence/post-pandoc/prepare-probes.py`가3.6 바이너리와 원 R0 입력을 고정 hash로 준비하고 `run-probes.py`가3개 P3 중간단계와2개 P4 검사를 수행한다. 준비 스크립트도 실제 실행·hash 확인했다. R 전체는 미실시이며 P4는 TeX format/PDF→SVG 의존성에서 실패했다. 필터가 쓰는 프로그램·원입력·명령은 execution.json에 있다. 정확한 TeX 및 converter 환경이 갖춰진 뒤 같은 입력과 봉인 Lua로 다시 실행한다.

Q7 프로그램 시험은 미실시다. `evidence/crossdomain/report.md`의 고정 SHA·입력·명령대로 Sphinx dot 유무와 GDAL/PROJ grid 유무를 깨끗한 별도 환경에서 비교해야 한다. source 기대값을 실제 실행 성공으로 취급하지 않는다.

## 보존과 귀속

원 질문·답의 긴 본문·이미지와 바이너리는 ignore된 cache에만 두고, 짧은 원문/실험 입력·사실 요약·원주소·revision/hash·실제영수증을 보존한다. 직접 인용/원시험 파일은 해당 원저작자의 자료다. 연구자 조합과 출력은 자체 관측으로 표시하고 외부1차자료 최소량에 더하지 않는다. 이 묶음 외 경로·중앙 진행표·다른 작업 branch는 수정하지 않는다.
