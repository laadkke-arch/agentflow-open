# AF-RES-095 인계

**연구 COMPLETE · 개별 원격 계약 검사 실패.** Quarto 1.4.553 행렬 12/12를 렌더했다. PDF 12/12, 판독 가능 표 18/18, 셀 144/144 보존, 반복 일치 6/6, 무인수와 두 인수의 실측 동률 4/4이다. 1차 직접 자료 40건과 독립 사건·저작 계열 17개를 원장에 보존했다. [고정 결과의 세 표](https://github.com/laadkke-arch/agentflow-open/blob/55eb703075163a84b38fdc7eb577f66207e9980e/docs/workstreams/research/AF-RES-095/RESULT.md) · [원장](sources.jsonl)

문서 공통 재정의는 두 번째 표에도 적용됐다. 두 후보 모두 첫 표만 TeX 그룹으로 감싸면 뒤 표의 3선을 보존했다. 원본 호출의 빈 noalign에서는 동률이었고, raw tabular에서는 두 필수 인수가 셀 첫 글자를 소비하거나 종료 명령을 받아 엔진 오류를 냈다. 원 질문자의 실제 프로그램판과 실행 성공률은 미확인·산출 불가다. [D-Z-1](evidence/matrix/D-Z-1/) · [D-T-1](evidence/matrix/D-T-1/) · [반례와 실제 그룹](evidence/probes/README.md)

## 브랜치와 원격 커밋

브랜치 `work/research-af-res-095`, 시작 통합 SHA `f72073277e6be643302a33f204d70baeb2c749a4`, 소유 경로 `docs/workstreams/research/AF-RES-095/`다. 결과 SHA와 네 묶음은 각 push 직후 GitHub 원격에서 확인했다. 작업 diff의 소유 범위 밖은 0개다.

| 묶음 | 원격 SHA | 볼 파일 |
| --- | --- | --- |
| ① R0·입력·기대 | [3278577900a88bd11a90a176a88002702af106c1](https://github.com/laadkke-arch/agentflow-open/commit/3278577900a88bd11a90a176a88002702af106c1) | [범위](SCOPE.md) · [세 원입력과 대조](fixtures/README.md) · [고정 manifest](manifest.json) |
| ② 배포·교정 | [6e18a1a9038746936df075ff21f4f7ef0307f043](https://github.com/laadkke-arch/agentflow-open/commit/6e18a1a9038746936df075ff21f4f7ef0307f043) | [환경](environment.json) · [양성·음성 교정](evidence/calibration/README.md) |
| ③ 12자리 원 출력 | [845cbf84238ccb68fc4bacf47841bf215e49cdea](https://github.com/laadkke-arch/agentflow-open/commit/845cbf84238ccb68fc4bacf47841bf215e49cdea) | [행렬 원장](runs.jsonl) · [PDF·TeX·로그](evidence/matrix/README.md) |
| ④ 결과·반례·자가검산 | [55eb703075163a84b38fdc7eb577f66207e9980e](https://github.com/laadkke-arch/agentflow-open/commit/55eb703075163a84b38fdc7eb577f66207e9980e) | [RESULT](RESULT.md) · [SELF_CHECK](SELF_CHECK.md) · [카드](cards.md) · [재현](reproduce.md) |
| 마지막 인계 | 이 파일을 추가한 단독 커밋 | 검사, 남은 불확실성, 첫 행동 |

## 실제 검사와 원격 재열람

대상은 **`55eb703075163a84b38fdc7eb577f66207e9980e`**이다. 2026-11-23 UTC에 시작·종료 모두 clean인 checkout에서 실행했다.

| 검사 | UTC 및 종료값 | 확인·결손 |
| --- | --- | --- |
| `python -B docs/workstreams/research/AF-RES-095/audit.py --reread-pdfs` | 18:31:42–43, **0** | 12 PDF 재판독. 18 표·144셀·6반복쌍, 원장 및 표 2 재계산, 프로브·CSS·Calc 원 결과 검산. |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-095/manifest.json --fetch` | 18:31:43–44, **1** | remote_checked. 통합판 f720732, 변경 428개(도구의 manifest 제외), 범위 밖 0개. 단일 오류 `dependency changed: work/research-af-res-092`. 요청 핀 e0d7ecda64bab2bd5d5779a9fb2a18d39a83bcdf와 실제 원격 헤드 e742bc665efde0d3883ec4d0f5479e03e914fcbf가 달랐다. |
| 같은 session check, 고정 ref 전용 독립 checkout, `--fetch` 생략 | **0** | local_only. 동일 결과 SHA, 범위 밖 0 및 오류 0. 요청 핀으로의 로컬 검사이며 원격 freshness 결손은 위 행에 남는다. [시작 계약](evidence/intake/contract.md) |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 18:31:44–49, **0** | doctor, acceptance, research-case, original-smoke 종료 0. 자동 세션 탐색은 `not-executed/no_active_sessions`였고 위 개별 계약은 실제 실행했다. |
| `python -B scripts/check.py --require-git` | 18:31:49–54, **0** | 공통 단위 55, lab 7·9, 독립 내보내기 및 Git bundle 복원. 복원 bundle SHA-256 `68f1318f52a51af050228a9c67a475d37c9d63d78a5172271adfd65e20d9c8ac`. |

18:31:49Z에 결과 SHA에서 GitHub 원본 17개를 다시 받아 로컬과 바이트 대조했다. 필수 세 표 행/열은 6×5, 12×6, 5×5다. 69행 원장 산입 40, 독립 계열 17, 본 실행 12·표 18, 반례의 TeX 오류 및 토큰 4행을 원격 파일에서 재계산했다. 일시적인 HTTP 503은 같은 URL 재시도로 복구했다.

| 원격 대조한 핵심 파일 | 일치한 Git blob |
| --- | --- |
| RESULT.md | `badb702b139bc6682dc8506d862126f00a1b0017` |
| sources.jsonl | `8eb1ba28162115c8bd8f952d1788d993fa7aabf7` |
| runs.jsonl | `005bdbc6ba6e52c434964e8f53e881a524f2b487` |
| SELF_CHECK.md | `345fdd1fab0e786618eadb45aabd343ce4c7730b` |
| metrics.json | `aadbb7a8bb0cd5ece2ecdbabf371c6561f97c2ea` |
| evidence/probes/P-BARE-BOTTOM-T/document.tex-log.txt | `43182262df42acd98890ec568d3e31dc7858eed8` |
| evidence/probes/P-TABULAR-T/pdf-raw.json | `e4e53ce69f0c784e986cbecdc7787d8555fbc518` |

RESULT SHA-256 `1d4f3ac59d53951da05b994e0a1ee4bedf3eada97e3d9091c6eed5d806205d03`. 원격에서 manifest·환경·카드·재현·CSS/Calc 증거·D-T-1 PDF도 확인했다. 위 검사는 이 인계 커밋의 부모인 결과 SHA를 대상으로 했다.

## 다음 첫 행동

진행 담당은 **지정 의존 SHA와 현행 브랜치 헤드의 차이를 먼저 확인**한다. 실제 사용한 092 입력은 사용자가 고정한 결과 `707216d8a7f2f09948bb79bfb30e9b2d62cde9ef`의 바이트이며, 원격 헤드까지 next-inputs 파일들이 같은 바이트임을 검증했다. 현재 manifest는 지정 인계 SHA e0d7을 보존한다. 진행 담당이 계약의 사용할 ref 또는 새 핀을 정한 뒤 결과 SHA의 개별 원격 검사를 다시 실행할 수 있다.

```bash
git ls-remote --heads origin chore/workspace-foundation work/research-af-res-092 work/research-af-res-095
python -B -m workbench.session check docs/workstreams/research/AF-RES-095/manifest.json --fetch
```

원 플러그인 파일, 원 질문자 적용 후 PDF 및 당시 버전은 미확인이다. 원 첨부는 셸 CONNECT 403이고 웹 도구에서 시각 데이터가 없었다. 현재 조건의 다시 실행할 명령은 [재현 문서](reproduce.md)에 있으며 원 회귀와 판 확대는 아래 최소 입력이 필요하다. 주 행렬 1차 TeX 로그는 덮여 미확인이고 동일 tex의 [별도 엔진 두 패스 재생](evidence/probes/engine-replay.jsonl)에서 6/6 경고가 2차에 해소됐다.

## 세 약점의 다음 조사

1. **원 질문자 환경.** 당시 Quarto·Pandoc·TeX 버전, 실제 전체 Qmd·명령·적용 후 PDF를 확보해 같은 판에서 비교한다. 당사자 환경·명령·출력이 연결된 관측이 있어야 과거 성공 판정을 바꾼다.
2. **커스텀·다중 페이지.** 캡션·반복 헤더가 있는 longtable 및 booktabs 뒤 재정의를 덮는 템플릿을 추가한다. 정의·후속 토큰·그룹 경계를 읽고 두 표의 선과 셀에 차이가 생기는지 본다.
3. **검출기 범위.** 짧고 얇은 선 및 병합·여러 줄 셀을 수동 라벨링해 288/576 DPI와 별도 엔진을 비교한다. 실제 선·셀 누락, 밑줄·페이지 경계 오탐 또는 독립 판독의 일치가 적용 범위를 바꾼다.

## 중앙 색인 제안

AF-RES-095 · 연구 COMPLETE · Quarto 1.4.553 렌더 12/12·표 18/18·반복 6/6, 두 매크로 동률 및 두 번째 표 적용, 한 표 그룹 격리와 토큰 반례 · 원자료 40/사건 계열 17 · 결과 55eb703075163a84b38fdc7eb577f66207e9980e · 개별 계약은 092 헤드 이동으로 종료 1 · [결과 경로](RESULT.md).
