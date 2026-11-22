REVIEW_READY

# AF-RES-028 인계

AF-RES-028#1의 유지 표본 32셀에서 사전 정의한 사용 범위가 모두 성립했다. CPython 16/16, Node.js 16/16에서 T0와 목표판을 직접 실행했다. 숨은 무효와 미확인은 각 0/32다. 024의 유지 865셀은 이 표본 밖에 있어 전체 D/S 새 순위는 미확인이다. [결과](RESULT.md) · [층·분모](tabulations.json)

| 분모 | 검산 결과 |
| --- | --- |
| 024 입력 | 64이유×16분기 1,024셀. 유지 897, 무효 95, 최초 오류·보류 각 16. |
| 028 표본 | 유지 32, 무효 대조 8, 최초 오류·보류 대조 각 1. 합계 42/42 직접 쌍. |
| 무효 대조 8 | 무효 재확인 6. Web Crypto 1은 문자 그대로의 EC 인자에서 최초 오류이고 NODE 전용 알고리즘을 뜻하면 무효다. Netrc 1은 일반 로그인 시험에서 유지이며 anonymous까지 포함하면 무효다. |
| 추가 대조 2 | Linux winreg 최초 오류 재확인. pydoc 보류 행은 두 판의 모듈·pydoc3 진입에서 성립, 맨 명령 이름에서 두 판 127. |
| 정책 짝비교 | 이진 교집합 39셀. 고정 D 예측의 024 대비 좁은 런타임 TP→FP 1과 S의 FN→TN 1은 같은 netrc 행의 조건 차이다. 실제 새 무효의 미방문 FN은 D 1셀, S 3셀이며 모두 같은 WASI 이유다. |
| 획득·원문 | 공식 Node Linux x64 11판과 CPython 고정 태그 재빌드 13판. 고유 원문 71개. 공식 테스트 4개는 2026년의 원본 시험 재실행이다. |

전체 가림 관측은 원래 라벨이 공개되기 전에 봉인했다. 가림 실험을 같은 작성자가 설계·실행했고 스키마 확인 중에 8개 Node 표본의 T0 초기 문구와 겹치는 내용을 봤다. 명제의 해석 범위와 024의 정책 보고를 교차할 때 이 점을 고려한다. [가림 설계와 노출](SCOPE.md) · [봉인](observation-seal.json) · [공개 후 행별 대조](comparison.csv)

## 고정판과 검사

- 저장소 `laadkke-arch/agentflow-open`, 브랜치 `work/research-af-res-028`, 소유 경로 `docs/workstreams/research/AF-RES-028/`. 배정 통합판 `4375541e48d1104cd88abc667809092b0e955d72`, 계획판 `e2d0917ccd0e0010e14627a2f919265c332cec53`, 입력 AF-RES-024 `4af1300841c1c39f9ef6e76d78579034d1ae0c51`. 실행은 GPT-6 기반 Codex와 관리형 Debian 13.6 x86-64에서 했다. 세부 모델 선택값·추론 강도와 2021–25년 당시 호스트는 미확인이다. [범위](SCOPE.md) · [작업 계약](manifest.json)
- 공개 전 관측은 `97d4774fe6ca7a94441096ed640ab4d54b83db52`, 공개 후 대조는 `be34508e52cd791709744eed427e2b619efdc1ab`, 고정 결과·자체 점검·수용 증거는 `a3d07901bd90dd16e1dbce7c71c8e629b2cf2cdf`다. 최종 인계 커밋은 GitHub의 작업 브랜치 ref에서 확인한다. [단계별 진행](PROGRESS.md) · [수용 증거](https://github.com/laadkke-arch/agentflow-open/blob/a3d07901bd90dd16e1dbce7c71c8e629b2cf2cdf/docs/workstreams/research/AF-RES-028/evidence/acceptance-evidence.json)
- GitHub에서 새로 받은 ④ checkout의 빈 실행 폴더에서 24개 배포 캐시를 재사용했다. 전체 시험 드라이버는 19.874초와 20.466초에 각각 종료 0이었다. 75/75 고유 관측, 표집 큐·잠금·비교 CSV·집계 JSON이 바이트 일치했다. [검증 영수증](evidence/verification.json)
- 입력 SHA-256 `f1c9a73ba16e53110b19e0d8be5e619969407ebdad5440b6d5afc04a95553c51`, 정규화 판정 SHA-256 `74d72753621dafa42099a3d498e50baed5d7ccfefbbdcd1046e6fa22b1a380d3`. ⑤의 원격 복사본에서 `verify.py`의 출력 바이트를 확인했고, `workbench.session check --fetch` 및 `cloud_check.py --require-clean`은 각각 종료 0이었다. 검사 시 통합 ref는 `b420fb7e1e01f4a366512fa71c0f507051aa6a19`였다. 공통 스캐너는 활성 manifest 자동 검색을 보고하지 않아 작업 manifest는 직접 검사했다. [검사 출력](evidence/verify-output.json) · [재현 입력·명령](REPLAY.md)

```sh
git ls-remote origin refs/heads/work/research-af-res-028
p=docs/workstreams/research/AF-RES-028
git show a3d07901bd90dd16e1dbce7c71c8e629b2cf2cdf:"$p/evidence/acceptance-evidence.json"
python -B "$p/verify.py"
python -B -m workbench.session check "$p/manifest.json" --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

## 판단 범위와 색인

색인에는 AF-RES-028, `REVIEW_READY`, 결과·수용 증거 경로, 024 의존 SHA, 유지 32/32와 직접 42/42를 기록할 수 있다. 원점의 계약 범위, 직접 재생의 조건, 표본 밖 분모를 결과와 함께 전달한다. 다음 첫 행동은 진행 담당이 작업 ref에서 이 인계를 읽고 ⑤의 수용 근거·직접 쌍 42·원문 71을 확인한 뒤 색인 등록을 판단하는 것이다. [원격 작업 묶음](https://github.com/laadkke-arch/agentflow-open/tree/work/research-af-res-028/docs/workstreams/research/AF-RES-028)

## 중요한 약점과 후속 조사

1. 유지 32개에서 발견되지 않은 붕괴가 865개 남은 셀에 있을 수 있다. 다른 분기·중복 이유·경계 입력을 고정한 추가 표본에서 실패 가능성을 재검한다. [표집·분모](tabulations.json)
2. Web Crypto, Netrc, pydoc과 Map은 문구의 범위와 관측식에 따라 채점이 달라진다. 별도 판독자에게 가린 큐만 주고 API 이름·입력·배포 관례를 먼저 정의해 해석 차이를 좁힌다. [불일치](comparison.csv) · [원래 계약과 개정](contract-amendments.jsonl)
3. CPython은 현재 Linux에서 고정 소스로 재빌드했다. 당시와 가까운 OpenSSL·Tk 조건의 두 번째 Linux 이미지에서 두 판을 실행해 A028-02·22·36의 환경 의존성을 확인한다. [실패와 복구](receipts/python-first/raw.jsonl) · [보조 버전](receipts/python-aux-runtime.json)
