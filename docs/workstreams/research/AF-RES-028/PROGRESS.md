# AF-RES-028 진행

| 묶음 | 원격 커밋과 증거 | 마지막 ID | 다음 첫 행동 |
| --- | --- | --- | --- |
| ① 표집·관측 범위 | 이 파일 최초 커밋의 SCOPE.md, manifest.json, draw.py | 배정 AF-RES-028#1 | 사전 커밋을 확인하고 가린 42셀과 해시를 생성한다. |
| ② 가린 큐와 사전 판정식 | ① `e41cc32aa07011b904d0fb665849622b80381d07` GitHub blob 재조회. 이 단계의 [묶음 해시](receipts/preflight.json) | A028-42 · 계약 33종 | Q2 계약에 맞춰 검사 및 환경 드라이버를 작성하고 목표판과 T0를 실행한다. |
| ③a Node 최초 관측 | ② `668863cb3cf212d55bb3270bfc9bc58f9dae6197`의 큐·계약·잠금 파일을 GitHub에서 재조회. [Node 실행 영수증](receipts/node-first/summary.json) | A028-38 · Node 20셀 | Map 프로토타입 가정을 별도 보존·재검하고, CPython 빌드 및 실행을 완료한다. |
| ③b CPython 최초 관측·준비 수정 | ③a `e7571e41aa72c78ebb3a63fe9cb48e336bfb7cc8`. [CPython 최초 실행](receipts/python-first/summary.json) 및 [보존한 변경 이유](contract-amendments.jsonl) | A028-42 · CPython 22셀 | 같은 태그의 Tk 재빌드, 강한 공개 테스트 PEM으로 재실행, 변경 전후 관측과 원문 판독을 봉인한다. |
| ③c 가림 관측 봉인 | ③b `2026a3d3701647566277ac691dfe06c0745de503`. [실행 원본](receipts/first/raw.jsonl), [판정 경로](blind-review.jsonl), [봉인](observation-seal.json) | A028-42 · 전 42셀 | 이 커밋의 관측과 봉인을 GitHub에서 확인한 뒤에만 답 파일과 024의 D/S 원장을 연다. |
| ④ 공개·정책 조인·반례 | ③c `97d4774fe6ca7a94441096ed640ab4d54b83db52`의 봉인·가림 판정·배포 파일을 원격으로 직접 읽고 답 해시를 검증했다. [비교](comparison.csv) · [pydoc 후검](receipts/pydoc-post-reveal.jsonl) · [보고서](RESULT.md) | A028-42 · 불일치 A028-05·10·20 | 빈 작업 디렉터리로 한 번 더 실행해 입력·판정·결과 해시를 비교한다. |
| ⑤ 깨끗한 재생·자체 점검 | ④ `be34508e52cd791709744eed427e2b619efdc1ab`의 결과·비교·CLI 영수증 원격 재조회와 새 checkout 검증. [검산](evidence/verification.json) · [수용](evidence/acceptance-evidence.json) | A028-42 · 재생 75/75 | 이 ⑤ 커밋의 수용 근거 및 자체 점검을 GitHub에서 읽고, 해당 커밋에 대한 검사를 확인한 뒤 HANDOFF를 작성한다. |
