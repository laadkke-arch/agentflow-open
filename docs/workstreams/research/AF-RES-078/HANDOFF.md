# AF-RES-078 #1 인계 — REVIEW_READY

## 1. 식별

- 작업 ID와 시도는 **AF-RES-078 / #1**이다. 실행·조사·재판독 주체는 동일 Codex Cloud 작업자다.
- 저장소와 작업 브랜치 링크는 [laadkke-arch/agentflow-open · work/research-af-res-078](https://github.com/laadkke-arch/agentflow-open/tree/work/research-af-res-078)다.
- 계획 기준 SHA는 `0d2b08431067e8d87212a66ecb27657c65722a59`. 배정 레코드를 읽고 브랜치를 만든 실제 통합 SHA는 `9bb5b7f63115b2a5d85aee3556bce6f690e2688e`다.
- 세션 시작 검사의 원격 통합 ref는 이후의 `d73c8ec85d375f37451795b575dd7d0e6b2f3594`였다. 작업의 base는 위 실제 시작 SHA다.
- **고정 결과와 재생 대상**은 `c23f6262b733d9a710a77de8b474689e510fb57c`다. **수용 근거 커밋**은 `c0b757fac1f1e947447022aab1a7ea2e48ac8c74`다.
- 결과 파일과 수용 원장을 원격에서 마지막으로 다시 읽은 시각은 **2026-11-23 11:33:11.924300 UTC**다. 그 커밋의 54개 파일을 새 GitHub 복제에서 읽어 전부 바이트 대조했고, 같은 커밋의 개별 계약 검사가 종료 0이었다.
- 지정 범위의 연구 수용 기준을 충족했다. 중앙 상태 및 통합은 배정자가 담당한다. 인계 기록은 이 파일 단독의 마지막 작업 커밋이다.

결과와 판정의 고정 링크는 [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/c23f6262b733d9a710a77de8b474689e510fb57c/docs/workstreams/research/AF-RES-078/RESULT.md), [수용 원장](https://github.com/laadkke-arch/agentflow-open/blob/c0b757fac1f1e947447022aab1a7ea2e48ac8c74/docs/workstreams/research/AF-RES-078/evidence/acceptance-evidence.json), [자체 점검](https://github.com/laadkke-arch/agentflow-open/blob/c23f6262b733d9a710a77de8b474689e510fb57c/docs/workstreams/research/AF-RES-078/SELF_CHECK.md)이다.

## 2. 작업 범위와 선행 결과

선택한 부분 작업은 SQLite CLI의 CSV를 Python csv로 읽어 키·타입·값을 유지하는 경로와, Pillow로 PNG 방향을 적용하고 Info-ZIP으로 원래 상대경로를 묶는 경로다. 작성 경로는 `docs/workstreams/research/AF-RES-078/`다. 기본 실행물 네 개를 확보해 지정 조합을 모두 사용했다.

실제 시작 통합판에서 지침, 상태, Dot 절차, 연구 브리프와 워크플로를 읽고 `dot-control.json`의 자기 행과 단일 의존을 확인했다. 074에서 넘겨받은 사실은 Pandoc의 빈 문단이 reader/writer 양쪽에 걸렸고 GDAL 역사판과 현재판의 실행 증거를 합칠 수 없었다는 점이다. [입수 원장](evidence/intake.json), [074 인계](https://github.com/laadkke-arch/agentflow-open/blob/b25a389ef33094fde4982a6198fd5649076ccd66/docs/workstreams/research/AF-RES-074/HANDOFF.md), [074 고정 결과](https://github.com/laadkke-arch/agentflow-open/blob/34f3a5595fde1dd8f2fe1c7f2801c132f2fa2be9/docs/workstreams/research/AF-RES-074/RESULT.md).

## 3. 커밋과 산출물

| SHA | 내용 |
| --- | --- |
| `5e6fe957779c56459f010cbd41b75c6b1dbfeb61` | 배정, 범위, 계약 시작 |
| `fa70495915d285a5d16205f4b16545de22f9eb65` | 생성기, 첫 독립 판독 규칙과 두 비공개 시드의 해시 |
| `7891081ba0641b707a65ffbfdb8cc99530fddbed` | 실제 단독 실행 8회와 합성 실행 이전 ZIP 이름 오라클 보정 |
| `7e1ba3454b68099fce36a62ddc05390ef81f7ba4` | 합성 실행 이전 A/B 408개 요건 예측 |
| `a3b0cd2361bad38ab53a8e01ec11c8b72a6ea9ff` | 정상·중단·재시도 32시도 |
| `2006bdea896b6467c126624ebbe9c5d2adc57a4c` | 봉인 재료 생성·열람 이전 C의 경계 예측 68행 |
| `67489dfcac506e04be02df70d6a7774134fcd0b8` | 시드 공개, 경계 16시도, 별도 진단 18행 |
| `072416a778f182846ec0a8fc85334cf6cfa31eaa` | 필수 표, Q1–Q7, 카드, 자체 점검과 원장 재생기 |
| `c23f6262b733d9a710a77de8b474689e510fb57c` | 설치 경로와 실행판 식별을 분리한 재생기 및 고정 결과 |
| `c0b757fac1f1e947447022aab1a7ea2e48ac8c74` | 수용 판정, 계약·클라우드·재생·원격 대조 영수증 |

필수 원장과 역할은 [SCOPE.md](SCOPE.md), [contracts.csv](contracts.csv), [fixtures.jsonl](fixtures.jsonl), [predictions.csv](predictions.csv), [runs.jsonl](runs.jsonl), [comparisons.csv](comparisons.csv), [sources.jsonl](sources.jsonl), [search-log.jsonl](search-log.jsonl)에 있다. 원본·중간·끝·임시 바이트와 명령 출력은 [artifact 원장](evidence/artifacts.jsonl)에서 SHA-256으로 찾고, 다음 도구 선택에 필요한 두 링크와 조건은 [cards.md](cards.md)에서 읽는다.

## 4. 검증

- 계약 시작은 Codex Cloud 작업자가 실제 base `9bb5b7f63115b2a5d85aee3556bce6f690e2688e`에서 `--fetch`로 실행해 종료 0이었다. [session-start.json](evidence/session-start.json).
- 고정 결과에서 `workbench.session check ... --fetch`는 2026-11-23T11:32:20.266469Z, 종료 0, `remote_checked`, 경로 이탈 0이었다. `cloud_check.py --environment codex-cloud --fetch-contract --require-clean`도 종료 0이었다. 전역 세션 탐색은 `no_active_sessions`를 반환했으므로 지정 manifest에 대한 근거는 개별 검사 영수증을 사용한다. [개별 계약](evidence/session-check.json), [공통 검사](evidence/cloud-check.json).
- 새 GitHub 체크아웃에서 48개 본실험 시도와 18개 진단 행을 재생했다. 본실험의 입력·교환·완료 지문 및 종료값이 일치했고 **6,368개 검사**가 종료 0이었다. 본실험 프로세스 124개, 진단 44개, 단독 8개, 버전 확인 5개는 재생에서도 별도로 셌다. [재생 영수증](evidence/replay.json).
- 최초 원격 대조의 49개 파일이 고정 결과에서 정확히 일치했다. 수용 근거를 붙인 뒤 54개 전체와 RESULT의 동일 Git blob `dc9b34a6fbf8aa12e48ca6b6378e14e3ceec6821`을 확인했다. 원격 체크아웃 `c0b757f…`의 재검사 역시 2026-11-23T11:33:11.917452Z, 종료 0, `remote_checked`였다. [49파일 영수증](evidence/remote-readback.json), [고정 결과 Github Actions 성공](https://github.com/laadkke-arch/agentflow-open/actions/runs/45166083651).
- 직접 연 원문은 원장 39행, 보수적으로 센 독립 1차 자료 **25개**이며 표 11, 이미지/ZIP 10, 교차 분야 4개다. 실패/판 변화 원사건 5개를 중복 없이 확인했다.
- 8셀×3시나리오 24개를 판정했다. 정상과 봉인은 각각 16개 시도, 후단 실제 중단 8개, 동일 입력 재제출 8개다. 깨끗한 16쌍 중 결과가 있는 14쌍은 바이트 동일, I01의 2쌍은 두 실행에서 모두 완료품 부재였다. 612개 요건/전체 비교 행을 독립 정답과 다시 조인했다.

## 5. 판단과 적용 한계

- **표 T01**은 빈 NULL 표기와 Python 3.13.5 QUOTE_NOTNULL을 맞췄을 때 정상·봉인·재시도 집계에서 모두 지지됐다. 같은 옵션 이름의 3.12.14에서는 NULL 타입이 사라졌다. 명시적 리터럴 표기를 쓰면 동일 리터럴과 중간 필드가 충돌한다. 별도 NUL 대조는 앞단 절단과 typed adapter의 복구를 실측했다.
- **이미지 I00**은 트리와 ZIP 경로를 둘 다 보존한 새 ZIP의 정상·봉인에서 지지됐다. I01은 ZIP 중복 이름 오류, I10/I11은 앞단 덮어쓰기 후 종료 0이었다. I00 재제출의 기본 add는 이전 멤버를 섞었다. 별도 `-FS`와 fresh-and-replace 실험에서는 요구된 두 멤버만 남았다.
- A 전체 거짓 채택은 T 주 1/8, 봉인 1/4다. I의 A 전체 거짓 채택은 0이지만 개별 요건의 주 거짓 채택 9/48, 봉인 9/24가 있었다. B 주의 거짓 채택과 거짓 배제는 0이고, 별도 미래 C 답의 봉인 전체는 분야마다 양성 한 건을 보류했다. 주 C는 같은 입력의 사후 진단이다.
- 실측 범위는 동일 작업자가 설계하고 재판독한 합성 자료와 지정 Linux 판이다. 이번 T 봉인에는 NUL이 없었다. 전원 장애·동시 게시, 별도 실제 사용자/압축 해제기와 태그 우선 뷰어의 결과는 미확인이다. CIPA의 원문 PDF 접근 실패는 검색 원장에 남겼으며 최소량에 넣지 않았다.

## 6. 이어받을 첫 행동

작업 브랜치의 최신 SHA와 이 파일을 다시 읽고, 고정 결과 `c23f6262b733d9a710a77de8b474689e510fb57c` 이후 파일 범위를 확인한다. 확인할 새 입력은 사용하려는 자료의 실제 NUL 유무와 해제기·로캘의 Unicode 인식 조건이다. 같은 두 가지 결과를 다시 확인하려면 [고정 런타임 취득 및 재생 명령](REPRODUCE.md)을 사용한다.

```bash
git fetch origin refs/heads/work/research-af-res-078
git show FETCH_HEAD:docs/workstreams/research/AF-RES-078/HANDOFF.md
AF078_DIR=docs/workstreams/research/AF-RES-078
python -B -m workbench.session check "$AF078_DIR/manifest.json" --fetch
AF078_OUT=$(mktemp -d /tmp/af078-review-XXXXXX)
bash "$AF078_DIR/tools/replay.sh" "$AF078_OUT"
```

검사 입력은 커밋된 `fixtures.jsonl`, `inputs/`와 위 네 실제 실행판이다. 범위를 넓힐 때에는 *같은 원본 둘과 기존 완성 ZIP 하나*를 먼저 준비해 의도한 해제기에서 이름·개수·크기·코너를 다시 읽는다. 파일 게시 경합을 검증할 때에는 같은 이전 ZIP과 같은 새 PNG 트리를 두 제출에 공유할지 먼저 명시하고 게시 위치와 시각을 각각 기록한다.
