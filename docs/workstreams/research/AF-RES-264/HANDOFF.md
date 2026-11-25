# AF-RES-264 인계

**작업자 자체 상태 DONE.** 고정 결과 SHA는 `9cf1b3437e7d793fcb25cc478505694ef383ba49`다. 고정판 재생·계약·저장소 검증 영수증은 `e34c9dda1ed625d03a47ece5c417a93628a938d4`다. [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/9cf1b3437e7d793fcb25cc478505694ef383ba49/docs/workstreams/research/AF-RES-264/RESULT.md) · [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/9cf1b3437e7d793fcb25cc478505694ef383ba49/docs/workstreams/research/AF-RES-264/SELF_CHECK.md) · [고정판 검증 영수증](https://github.com/laadkke-arch/agentflow-open/tree/e34c9dda1ed625d03a47ece5c417a93628a938d4/docs/workstreams/research/AF-RES-264/receipts/verification)

## 완료 결과

- Pandoc 2.2.3.2/2.3의 공식 Linux amd64 실행 파일, 실제 추출 템플릿, 태그 원파일을 고정했다. 같은 pdfTeX 환경에서 8셀×2회 모두 3패스 성공했다. 최종 16개 PDF와 pass별 로그·PDF·보조파일을 남겼다. [행렬 CSV](https://github.com/laadkke-arch/agentflow-open/blob/9cf1b3437e7d793fcb25cc478505694ef383ba49/docs/workstreams/research/AF-RES-264/matrix.csv) · [실행·재생](replay.md)
- 2.3 기본 article의 `--toc`에서 `toc-title`이 인쇄 제목을 바꾼다. 2.2.3.2 기본 템플릿은 `Contents`를 유지한다. 양방향 교차와 블록 삭제에서 변화는 템플릿을 따랐다. 고유값만 바꾼 경우 최종 본문 책갈피의 네 Title·부모·목적지가 동일했다. `--toc` 토글은 목표 이름·좌표에 영향을 줬다. [2.3 원 PDF](receipts/matrix/v23-on-unique-r1/case.pdf) · [교차 비교](receipts/comparisons.json)
- 목차를 끈 8회는 최종 인쇄 TOC 정상 공석, 주행렬 16회는 최종 책갈피 4개다. 합성 `bookmarks=false` 제어는 두 파서 종료 0과 최종 정상 공석을 보였다. 깨진 파일은 두 파서 exit 1이었다. 같은 입력 반복 8쌍의 원 PDF는 날짜/ID 값만 달랐다. 동일 epoch 재실행은 원바이트도 일치했다. [반례](COUNTEREXAMPLES.md)
- EPUB 2/2의 판독과 공개 배포 XML을 재검산했다. CC의 nav는 spine 안, Page Blanche의 nav는 spine 밖이다. 4/4 배포 XML의 LF/CRLF 차이 외에는 고정 원파일과 일치했다. PDF 검증 분모에서 EPUB를 분리했다. [EPUB 결과](receipts/epub/) · [출처 원장](sources.jsonl)

## 착수와 보존

착수 통합 `3c32c1b44bd139819485548cb50e69e254288fad`, `work/research-af-res-264`, 단독 소유 `docs/workstreams/research/AF-RES-264/`. 직접 의존 AF-RES-243의 중앙 DONE 및 자체 PARTIAL은 구별했다. 의존 ref와 HANDOFF `001d09da8b4f9cbb0d77fff2fc41acbc46fb5e41`, 선행 분석 고정 `5f4cc61469f2a7f39d773fe7e1fe0381f39ecb88`을 확인했다. 진행표와 통합 색인은 통합 담당의 경로다. [착수판과 자료 노출](SCOPE.md) · [시작 명령·종료 0](receipts/start/) · [세션 핀](session.json)

| 묶음 | 커밋과 내용 |
| --- | --- |
| 범위·입력·경쟁 예측 | `9a2b113b273c190561015e86c62c6eb5cee97d25` |
| 직접 자료 원장 4묶음 | `f4656b33ec74c2c4820f1329a619d7391f434089` 요청·수정·릴리스, `fc7c3ac545843e2145085cbc0b4be19c84725ad0` 판별 코드·시험, `5a82dbe9530475d4a03ab026c2eebbe734bf4522` TeX·PDF, `84a8342296fb9d94d0f89ea1e59a100093d8e7c1` EPUB |
| 주행렬 | `683db1be46c3d969e564b2d1a527dafe4f959dcd` |
| 추가 통제와 정정 | `e945b0e8e9df0f14a74138cddc9a40e2b1eff707` 첫 판독 → `9bca691052e910d1600e55ea36bd7ca2af72d5c3` CRLF·PDF 버전·바이트 비교 |
| 결과·검토 | `0212b440690c6f1ad05c64d8066881e0c7249df0` 결과 및 재생 → `9cf1b3437e7d793fcb25cc478505694ef383ba49` 자체 검토 포함 고정판 |
| 검증 기록 | `e34c9dda1ed625d03a47ece5c417a93628a938d4` 검증 영수증 및 SCOPE 열람점 |
| 최종 인계 | 이 파일 단독 커밋 |

## 고정판 검사

| 실행 | 대상·종료 | 범위 및 원영수증 |
| --- | --- | --- |
| `python -m workbench.session check docs/workstreams/research/AF-RES-264/session.json --fetch` | 고정 결과 SHA, exit 0, remote_checked | 원격 통합 `22aae408745883788adf3cc19f88ecd01b7808bd`, 의존 브랜치 SHA, 계약, 소유 경로 검증. 720 변경 모두 소유 경로. dot-control blob 동치. [개별 검사](receipts/verification/session.stdout.txt) · [범위](receipts/verification/scope.json) |
| `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 같은 고정 SHA, exit 0, 시작/끝 clean | doctor·acceptance·reference-audit discovery·original smoke 완료. `scripts/check.py --require-git`는 내부 명령이며 테스트 55/7/9를 통과했다. `check-all`의 세션 판정은 `no_active_sessions`이고 이 작업의 nested manifest는 앞 행에서 개별 검증했다. [서브 명령·종료·환경](receipts/verification/cloud-check.json) · [기본 검사 로그](receipts/verification/cloud-check-logs/) |
| `prepare_tools.py` → `run.py matrix` → `run.py controls` → `read_epub.py` → `compare.py` → `verify.py --replay-root …` | 같은 고정 SHA의 별도 clean checkout 및 새 폴더. 각 exit 0 | PDF 26회·78패스, 요소별 판독 일치, AST/TeX 및 날짜·ID 마스킹 뒤 전체 최종 PDF 26/26 일치, 원바이트 3/26 일치. EPUB 2/2 및 파서 실패 통제 재생 완료. [검증 출력](receipts/verification/validate.stdout.txt) · [case별 해시](receipts/verification/replay.json) · [재생 원판독](receipts/verification/replay-observations.tar.gz) · [보존 파일 해시](receipts/verification/SHA256SUMS) |

저장소 검사가 실행된 SHA는 위 결과판이다. 그 이후 커밋은 검증 영수증과 열람점, 인계다. 두 PDF 엔진의 독립 판독을 수행했고 별도 작업자 검토는 미실행이다.

## 미확인과 다음 첫 행동

핵심 표본 미달 0이다. 자료 하한은 25 고유 직접 원자료로 충족했다. 원글 사용자의 설치판·후속 PDF와 upstream 서명은 미수신 또는 미확인이다. 다른 엔진과 class, 역사 GUI 및 EPUB 리더 UI는 미실행이다. Adobe PDF 32000-1 전체 원문 경로는 직접 열기 제한이 있었고 원장 5개 접근 실패 중 하나로 남겼다. 적용한 포맷·파서 근거는 나머지 직접 읽은 원자료와 PDF raw tree에 있다.

다음 검토자의 첫 행동은 고정 2.3 맞춤 표본에서 `case.tex` L62/L65, `pages.txt` L5/L6–10과 pypdf의 네 name/좌표를 나란히 확인하는 것이다. 새 실제 요청이 인쇄 제목이면 해당 매뉴얼 절을, 뷰어 탐색 제목이면 별도 `pdfbookmark`와 대상 검산 절을 사용한다. 원작자의 실제 파일이 발견되면 해당 PDF/생성 TeX를 이 세 층으로 우선 판독한다. [고정 TeX](receipts/matrix/v23-on-unique-r1/case.tex) · [페이지 판독](receipts/matrix/v23-on-unique-r1/pages.txt) · [책갈피 원판독](receipts/matrix/v23-on-unique-r1/pypdf.json)

색인 제안 — **AF-RES-264 · DONE · Pandoc 2.2.3.2→2.3**. 인쇄 목차 제목 옵션의 템플릿 경로, 책갈피 Title·이름 대상·페이지 좌표, pass 공석·파서 실패, PDF 메타데이터 지문, 두 EPUB nav/spine 대조. 고정 결과 `9cf1b3437e7d793fcb25cc478505694ef383ba49` 및 의존 AF-RES-243 `001d09da8b4f9cbb0d77fff2fc41acbc46fb5e41`.
