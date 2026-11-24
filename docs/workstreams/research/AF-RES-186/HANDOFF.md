# AF-RES-186 HANDOFF — DONE

## 식별과 상태

- AF-RES-186 시도 1, Codex Cloud의 Debian 13 amd64 실행. 작업자 완료 판정은 **DONE**, 독립 검토 상태는 **REVIEW_READY / 미실시**다.
- 저장소 `laadkke-arch/agentflow-open`, 작업 브랜치 `work/research-af-res-186`, 허용 경로 `docs/workstreams/research/AF-RES-186/`.
- 시작 `fa32c7b712231bd1d43974ded8072bda5196239f`. 계획 기준 `128f673685ec804c526a38e3f89d4d8a43fcd299`. 직접 의존은 AF-RES-176의 중앙 DONE, 작성자 PARTIAL 인계 `a347a373cdd46910f2cd2cf53419849ba48ee03a` 한 건이다. [선행 인계](https://github.com/laadkke-arch/agentflow-open/blob/a347a373cdd46910f2cd2cf53419849ba48ee03a/docs/workstreams/research/AF-RES-176/HANDOFF.md)
- 결과 SHA는 **`7182108b635189f6b866d99e2eaadc210d59d9f9`**다. 자체점검까지 들어 있다. 이 인계는 다음 단독 커밋이며 인계 SHA는 원격 브랜치 HEAD에서 확인한다. [고정 결과 커밋](https://github.com/laadkke-arch/agentflow-open/commit/7182108b635189f6b866d99e2eaadc210d59d9f9)
- 최신 실행은 2026-11-24 19:33:57.106042–19:34:00.675941 UTC다. [실행 감사](receipts/execution/audit.stdout.log)

## 범위와 실제 판정

W3C suite `8811ba2a3bcae883ac91efacffb70ef08d84e92f`의 열 입력을 Gold `0dbcf4d641a409700208f66945c0d2af7754fba9`와 JS `30f9067c40066519c917721b8ca4a374eabf15e7`로 두 번씩 실행했다. 원 입력 IRI를 base로 고정하고 JSON-LD 1.1, 로컬 파일 로더와 문맥을 사용했다. `ordered`는 manifest대로 생략했고 두 구현의 자체 키 정렬을 판독했다. [입력·환경](inputs.json) [재실행 절차](runner/README.md)

- 기본 실행 40/40, 모두 별도 PID 및 nonce. Gold 18/20 합격, JS 20/20 합격, 전체 38/40 합격과 규격 불합격 2건. 미실행·비교 불가 0건. 채점기 대조 10/10과 구조 대조 2/2를 별도로 실행했다. [runs.csv](runs.csv) [대조 로그](receipts/controls/checks.stdout.log)
- 반복 일치 20/20, 두 엔진 간 반환·오류 일치 9/10. Expansion `t0123`에서 Gold는 두 번 모두 `http://example.com/baz z`를 datatype으로 포함한 JSON을 반환했다. JS는 두 번 모두 `invalid typed value`를 냈다. 정상 T01은 두 엔진 모두 `[]`, T06은 두 엔진 모두 `{}`를 두 번 반환했다. [Gold T04](receipts/gold-T04-r1/stdout.log) [JS T04](receipts/js-T04-r1/stderr.log) [50행 비교 원장](comparison.csv)
- 고정 원파일 48개 직접 열람, 고유 SHA-256 42개, 원장 63행. 2020년 두 보고의 20개 단언을 읽었고 현 판정과 20/20 일치했다. 각 20건의 당시 suite SHA·옵션·런타임·원로그와 운영자 독립성은 미확인이다. 현재 행은 한 환경의 실행이며 별도 환경의 재현은 미확인이다. 두 분야 사례는 176 자료의 구조 검산이었다. [출처 원장](sources.jsonl) [자체점검](SELF_CHECK.md)

## 대표 파일과 검증

| 묶음 | 고정 SHA | 다시 읽은 대표 파일 |
| --- | --- | --- |
| 입력·검사 계약 | `d55ace5a871d7951c345d1de9ab64f9d3fecd8a2` | [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/d55ace5a871d7951c345d1de9ab64f9d3fecd8a2/docs/workstreams/research/AF-RES-186/SCOPE.md) |
| 원자료·지문 | `c8c36361374b433bd87b01a0a0dc074ec6e44c44` | [inputs.json](https://github.com/laadkke-arch/agentflow-open/blob/c8c36361374b433bd87b01a0a0dc074ec6e44c44/docs/workstreams/research/AF-RES-186/inputs.json) |
| 두 어댑터·채점 대조 | `5c7f746cee0d4663a3a3d74d84e6d2a3bbec80f0` | [대조 원로그](https://github.com/laadkke-arch/agentflow-open/blob/5c7f746cee0d4663a3a3d74d84e6d2a3bbec80f0/docs/workstreams/research/AF-RES-186/receipts/controls/checks.stdout.log) |
| 원 실행·비교 | `da569818ca2bb95593cf359c40396afe592f3a1d` | [Gold T04 r2](https://github.com/laadkke-arch/agentflow-open/blob/da569818ca2bb95593cf359c40396afe592f3a1d/docs/workstreams/research/AF-RES-186/receipts/gold-T04-r2/stdout.log) [JS T04 r2](https://github.com/laadkke-arch/agentflow-open/blob/da569818ca2bb95593cf359c40396afe592f3a1d/docs/workstreams/research/AF-RES-186/receipts/js-T04-r2/stdout.log) |
| 표·자체점검 | `7182108b635189f6b866d99e2eaadc210d59d9f9` | [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/7182108b635189f6b866d99e2eaadc210d59d9f9/docs/workstreams/research/AF-RES-186/RESULT.md) [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/7182108b635189f6b866d99e2eaadc210d59d9f9/docs/workstreams/research/AF-RES-186/SELF_CHECK.md) |

- 매트릭스·감사 명령의 종료코드는 0이다. `inputs.json` SHA-256은 `3acf912b706dc31d64700b3f3d3778129f2653cddda5dd9565593e4e211d3e73`다. raw stdout·stderr 80개, 요청·출력 메타데이터 및 50개 비교 행을 재검산했다. [실행 및 검사 영수증](receipts/execution/)
- 결과 SHA의 `python -B -m workbench.session check docs/workstreams/research/AF-RES-186/session.json --fetch`는 종료 0, `remote_checked`, 범위 밖 경로 0이었다. 원격 통합판 `0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6`의 계약과 의존 SHA를 확인했다. [작업 계약](session.json)
- 같은 깨끗한 결과 SHA의 `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean`는 종료 0이었다. doctor, 공통 55개와 lab 7·9개, export·Git bundle, discovery와 smoke를 확인했다. 공통 `check-all`의 상태는 `no_active_sessions`이며, 186 계약은 바로 위 명령으로 별도 확인했다. 전체 코드 검사는 결과 SHA를 대상으로 했다.

## 첫 재개 행동

검토자는 먼저 원격 브랜치와 이 인계에 적힌 결과 SHA를 확인한다. [재실행 절차](runner/README.md)의 세 고정 checkout을 준비하고 저장소 루트에서 다음을 실행하면 기존 영수증의 해시·채점·과거 조인을 먼저 재검산할 수 있다.

```sh
owned=docs/workstreams/research/AF-RES-186
python -B "$owned/runner/verify.py" "$owned" --suite "$scratch/suite"
```

기대 요약은 `raw_and_grade_rechecked=40`, 반복 20 일치, 엔진 간 9 일치·1 이견, 과거 판정 20 일치다. 다음 독립 확인에서는 T04와 정상 T01을 우선 읽고 결과가 달라지면 I04 지문·런타임·옵션부터 맞춘다. 과거 원값을 주장할 때 필요한 자료는 2020년 해당 단언의 suite SHA·옵션·런타임·원로그다.

색인 제안 — AF-RES-186 / 고정 JSON-LD 열 시험에서 Gold·JS 각각 두 반복 / DONE·독립 검토 대기 / RESULT.md / AF-RES-176 의존, t0123만 현 엔진 이견 및 과거 조건 미확인.
