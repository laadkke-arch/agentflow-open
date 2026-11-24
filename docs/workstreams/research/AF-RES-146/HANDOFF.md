# AF-RES-146 HANDOFF

**작업자 판정 COMPLETE · 수용 상태 REVIEW_READY**

시도 1, Codex Cloud, 저장소 `laadkke-arch/agentflow-open`, 브랜치 `work/research-af-res-146`. 통합 계획 SHA는 `9ad2ffc5974bf3379ce1f3fb947a9cf19bbdf673`, 실제 시작 SHA는 `277e27e1125e4cd26e750e6068dd5a9edf5e9d78`이다. 등록 선행은 중앙 DONE/인계 PARTIAL인 [AF-RES-142](https://github.com/laadkke-arch/agentflow-open/blob/1fa95555b2806f0c5cba492bff67cca6143a7b87/docs/workstreams/research/AF-RES-142/HANDOFF.md) 한 건이다. 기록·리플레이는 `docs/workstreams/research/AF-RES-146/`에 저장했다.

## 설계 판단에 넘기는 수치

- 원본은 표시 한도를 첫 검색에 전달한다. 두 매칭 링크만 있는 plain 교정에서는 2와 3 모두 Paperless 제외와 NARA 보류를 저장했다. 합성이 1위를 차지하는 교정에서는 2에서 잘린 NARA가 3에서 보류로 돌아오고, 합성은 두 조건 모두 미판독이다. 작업 사본 제안은 최초 폴더 및 재시도 중복 보존의 증명이 아니다. [원본 추적](evidence/prototype.json)
- 142의 242쌍과 132자리 중 표시 1·공석 131을 재집계했다. K22/L에서 표시 3을 유지하고 검토 3→8로 바꾸면 교정 C-P1-07/S04 하나가 표시되며, 잠정 신규 6건은 회복 0이다. 직접 두 쌍을 넓은 목표에 따라 일부로 바꾸면 직접 기회는 0이다. 138 교정 본문 지문 5/5 일치, 142 잠정 신규는 역할 span만 검증했다. [결과와 분모](RESULT.md)
- 새 자료층은 최초 공개 글 60건 중 4건과 고정 12장이다. 독립 48쌍에서 직접 0·일부 15·충돌 14·미확인 19다. 동일 표시 3자리에서 3→8은 조건부 1→4, 공석 11→8, 조사 중 충돌 6→10, 표시된 충돌 0→0이었다. 세 추가 링크는 모두 P-A에서 복구했다. 이견 7/25를 보존했으며 별도 판독자가 좁은 표시 게이트와 달리 적용 가능한 조건을 해석한 사례가 있다. [기준](truth.csv), [이견](evidence/analysis-join.json)
- 실제 읽은 별도 외부 저작 27이고, 원장에는 제외·실패를 포함해 147행이 있다. 3→8 로컬 대조는 142 19→42, 새 자료 10→25다. 로컬 개봉은 각각 12→19와 5→8, 비용·캐시·시간 분모는 요청별로 저장했다. 고정 8과 순차 판독은 이 분모에서 같은 횟수로 끝났다. 0점 대조는 P-B에 7번을 추가했지만 회복 0이다. [원전](sources.jsonl), [비용](costs.csv), [비용·재생 지문](evidence/receipts.json)

## 커밋과 원격 확인

GitHub raw 경로에서 각 대표 파일을 재열람해 해당 커밋의 바이트 및 Git blob과 일치시켰다. 최종 재열람은 2026-11-24 15:19:16–17 UTC다. 각 기록의 변경 경로는 소유 폴더에 속한다.

| 묶음 | 원격 커밋 | 재열람 파일 | Git blob |
| --- | --- | --- | --- |
| ① 범위·계약 | `57e6ae95d7e382b62ef1eb277cf595e6dfa9645f` | SCOPE.md | `e0e55578dd1587e94a9b64b3f64f1c9bc1068fe6` |
| ②a 재고 | `c1790e9a312c49791adca23b021105ef1c603392` | inventory.jsonl | `bcc7de88591d33003f3ecf695cb6511a6c6af10c` |
| ②b 모집 | `bc6dc637cd4b12c05023388e5924e2013a03db0d` | frame.csv | `32ce782bde36b62db22392242fc3d3ff1f84e798` |
| ③a 원본·게이트 | `b91878e2ead712aa32c90ab109808ccde25fbebd` | replay/gate-new.csv | `52bb3c84d60dc43fb770476b785261c0dd0bf1ab` |
| ③b 단계 | `d2a7f9ff1d9f1dafcfb389974d04edf59d81b7d4` | stages.csv | `0887c62c271a30730df22e64a4ad940bb1d19448` |
| ④ 독립·비용 | `3b13248b8447589463af602391c1d907bce9ae73` | truth.csv | `3cb00f9192ab7eadd20c61d00b05b54689bccb43` |
| ⑤ 결과표·자기 검산 | `73e05925b4535193f0c1a0845763d0de8d4f3bc3` | RESULT.md | `36df184a569ff4a33d95347f9ecf966a36b9bb75` |
| ⑤ 보정 및 실제 검사 대상 | `91b10340abca933bb2696ff7372c3168999892ac` | RESULT.md | `f9470fb1b62a94f3c1a2b26c84f1879e8a9da852` |
| ⑤ 검사 증거 | `d5f460ac540c38a33e066d0d9472e61300b4ef12` | evidence/checks.json | `e7837794263c5656ad936c477fbfebe4bc7e864d` |

## 실제 검사와 미확인

`91b10340abca933bb2696ff7372c3168999892ac`의 새 GitHub checkout에서 Python 3.12.14·SQLite 3.53.1로 다음을 실행했다. 처음과 끝 모두 Git clean이었다. 시작 시 `workbench.session start`가 고정한 계약 v2의 원격 최신 상태 및 등록 의존을 지정 매니페스트로 검사했다.

| 실행 | 종료·범위 |
| --- | --- |
| `python -m workbench.session check docs/workstreams/research/AF-RES-146/session.json --fetch` | 0, 원격 확인·의존·변경 소유 경로 30개 검사 |
| [독립 빈 디렉터리 2개 재생·조인·cmp](replay/README.md) | 각각 0. 입력 SHA-256 `7de3ef7b0e6af24b43ace0e171fb8a63609954b0e599f20a0b08493f8cf0f145`. 단계·전환·원본 해시 그대로. 시간 재실측은 [검사 증거](evidence/checks.json)에 구분 |
| 원본 `test_roundtrip.py` | 0, 7개 통과 |
| `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 0, doctor·acceptance·demo·원본 smoke. 공통 `check-all`은 `no_active_sessions`이며 지정 매니페스트는 위 별도 검사로 확인 |
| `python scripts/check.py --require-git` | 0, 공통 55 및 기존 lab 7·9, export·Git bundle 복원 등 |
| `git diff --check 277e27e1125e4cd26e750e6068dd5a9edf5e9d78..HEAD` | 0, 경로 목록과 표 형식·표본 수·원전 수도 검산 |

업스트림 PyTorch·OCRmyPDF·Paperless의 제품 실행, 실제 저자 PDF의 서명·OCR 객체·ZIP 디렉터리 상태는 미확인이다. 로컬 런타임에는 `ocrmypdf`, `pikepdf`, `django`, `torch`가 없었다. 시험 원문과 적용 판의 실행 명령·fixture는 [재생 안내](replay/README.md)에 기록했다. 기관 PDF의 전문 바이트, 별도 판독자의 실제 활성 시간·CPU는 미계측이다. ⑤ 검사 증거와 마지막 인계는 검사 대상 커밋 이후 저장한 문서다.

## 다음 첫 행동

[결과표의 P-A / P01·P04·L01](RESULT.md)에서 조건부 세 링크를 확인한다. 이어 별도 제품 검증이 배정되면, 유효한 서명을 넣은 QA용 PDF 한 장을 Paperless-ngx `v2.2.1`의 시험 인스턴스에 입고해 실제 실패·성공을 확인한다. 입력은 최초 파일 `signed-original.pdf`, 성공 시 해당 문서의 `/api/documents/<id>/download/?original=true` 응답 `returned-original.pdf`, 그리고 처리 로그다. 입고 전후 해시와 서명 상태는 아래처럼 비교할 수 있다. 기본 download의 파생본도 함께 기록하면 원본과 파생본의 식별을 검증할 수 있다.

```sh
sha256sum signed-original.pdf returned-original.pdf
pdfsig signed-original.pdf
pdfsig returned-original.pdf
```

색인 제안 한 줄 — 표시 3 유지·검토 3→8에서 142 기노출 교정 직접 +1, OCR/Paperless 새 층 일부 +3에 집중. 독립 48쌍 직접 0, 외부 원전 27건, 두 재생 일치.

| 불일치·약점 | 판단에 미치는 영향 | 다음 조사와 자료 | 판정을 바꿀 관측 |
| --- | --- | --- | --- |
| 142 직접 두 쌍은 하위 출력 기준이고 회복 하나는 이미 답이 노출된 교정 | 신규 직접 표시 효과는 아직 관측되지 않았다. 0점·목록 밖은 깊이만으로 되찾지 못한다 | 신규 미노출 최초 요청의 전체/하위 반환 구절과 독립 카드 원절 | 직접 적격이 4–8위에서 회복되며 보존 조건을 통과한다 |
| 새 요청 네 건과 게이트 이견 7/25, 실제 signed PDF와 O-B 텍스트 객체 미확인 | 조건부 +3의 적용 범위가 P-A 한 건에 집중된다 | 시험용 유효 서명 파일·원본/파생 응답·로그, 비가시·가시 OCR의 v17.14.2 strip fixture | 무 OCR 입고에서 실제 서명·바이트·실패 원본 사본이 유지되거나, 비래스터 층 제거가 확인된다 |
| 재생은 로컬 공급자 절·기관 판독 기록을 사용하고 순차는 같은 횟수로 끝났다 | 벽시계 수치의 운영 적용과 순차 절약을 이 자료로 확정할 수 없다 | 처음 3–7위에서 세 적격이 채워지는 미노출 요청과 최초 개봉/반복 비용 실측 | 같은 표시·충돌에서 실제 원문 읽기 횟수와 전체 지연이 줄어든다 |
