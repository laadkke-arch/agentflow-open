# AF-RES-032 통합 원장 내부 감사

**PASS_WITH_NONBLOCKING_NOTES · 27/27 조건 통과 · 종료 코드 0.**

검사 UTC: 2026-11-22T08:03:38.099378Z. 대상 HEAD: `ffbce62e4c01459ebbfb006a5d6c67e425ed7c17`. 아래 입력 SHA256으로 특정한 작업 트리를 감사했으며 이후 커밋으로 검사 범위를 소급하지 않는다.

## 재계산 결과

| 항목 | 실측 | 판정 |
| --- | ---: | --- |
| source 행 / 고유 ID | 395 / 395 | 일치 |
| 보수적 최소 산입 | 75 | 범주 합계 일치 |
| A 원문 / 상류 / 소비자 후속 / 타 분야 | 12 / 34 / 8 / 8 | 필요 범주 합계62 |
| 기타 / B 소비자 / B 보조 | 1 / 5 / 7 | 추가13 |
| A archive / 문서 상태 / 실제 HTML / 부재 | 123 / 246 / 211 / 35 | source에서 독립 재구성 |
| A href 수정 참조 / 독립 소스사건 | 5 / 4 | 단위 분리 |
| B 시도 / 질의 / 후보 | 6 / 18 / 17 | 기록 상한 준수 |
| B 실제 archive / 버전 웹 / 역사 HTML 없음 | 3 / 2 / 1 | 매체 차이 보존 |
| B의 A 중복 / 추가 독립 HTML 소비자 | 1 / 4 | B05 중복 제외 |
| 엄격 날짜쌍 / 조건부 분모 / 우측 검열 | 0 / 0 / 0 | 해당 없음; 0일 아님 |
| A 소스→배포 보조쌍 / 독립 소스사건 / B 보조쌍 | 3 / 2 / 1 | 다른 시계와 분리 |
| 동일 매체 독자 실패 / 별도 live-web 보고 | 0 / 1 | 후자를 사슬에 편입 안 함 |

A 첫12행 50,326바이트는 원격 봉인 commit `168d90b8519bcb4f673acc659bbaae895f79fca5`의 references와 정확히 같다. 접두 SHA256은 `b3c2f68b905102f0fa682ab45a34c0f3401a69b61ba0a59327045e04a626d562`다. A는6프로젝트·각2문서·두경로 각6문서다.

## 발견과 수정 후 재검

| 발견 | 수정 전 문제 | 수정 후 확인 |
| --- | --- | --- |
| IA-F01 | 원문·다른 라이브러리 상태·문서 부재가 같은 중복 그룹에 묶임 | `minimum_counting_group`은 보수적 선택으로 명명하고 동일본문 주장을 제거. 실제 `duplicate_group`과 이전 collector 그룹을 분리. |
| IA-F02 | 보조 interval7행 최상위 event/source 조인 공백 | 7/7 복구, source ID 모두 존재. |
| IA-F03 | B6의 최소 성공·의도 한계 null | 봉인 L2 추출자 입력 전재와 provenance 확인. A 바이트 유지. |
| IA-F04 | B02 출판 clock null | CRAN2022-05-04T00:20:02Z와 B02-httr-1.4.3 기록. |

추가로 B04의 원 artifact는 현재 HTML이 아니라 PyPI2.2.0 README.rst이며 `published_html_eligible=false`다. 소스 업로드 시각은 HTML 출판 시각과 분리됐다.

## 중복과 과잉 해석 점검

같은 archive URL을 공유하는 산입 문서 쌍은7그룹이다. 각 쌍은 서로 다른 HTML member SHA256을 가지므로 URL만 같다는 이유로 합치지 않았다. 선택된 정확중복 그룹과 최소산입 그룹의 복수 대표는0개이고 중첩 필드를 포함한 출처 ID 누락도0개다.

R01 simple-datatables 변경과 R06 Star Wars 변경은 원 예제 목적의 링크 정정으로 과대계수하지 않는다. R04 문서 폐기도 정정 분자에서 제외된다. B02의200/fragment 소실, B04의옛429/별도새200이 분리된다. A-D02 당사자 보고는 live /3/ 웹 문서이며 봉인 offline판과 같은 노출 매체라고 주장하지 않는다.

75는 보수적으로 선택한 최소 원문 수이며 모든 의미상태를 세는 완전한 원고 총수가 아니다. SQLite 실제5판은 재구성했고 46개 미검사판의 한계가 남아 있다. 51항목 외부 원장은 이 감사에서 다시 열지 않았으므로 전체원장 재열람으로 보고하지 않는다.

## 남은 비차단 메모

보조 배열의 반복 source ID도 재검 시점에는 제거됐다.

역사적 HTML 최초 공개일, B04 역사 HTML, SQLite 미검사판과 동일 매체 독자 관측은 이미 명시된 연구 공백이며 이 감사가 해소한 것은 아니다.

## 입력 SHA256

| 파일 | SHA256 |
| --- | --- |
| sources.jsonl | `eb85acaadebbfb3642983a73fb2eb8c9ae0f86e6ef1c804f2610fd357f653e30` |
| evidence/source-deduplication.json | `ade735018736c6bf2aaef65b4bf64c1376c4bda852f8368bcd3674f1a58badc2` |
| evidence/counts.json | `f46693c99380bc952facacc1a2a91ed16da3ce88be1834c7a83a6b95d4b5233e` |
| references.jsonl | `4619053263c403b7136bd7ca571c890db5226cba29e989b721ce74662a9e6742` |
| chains.csv | `6dafbc73592270340070fdfc8c0b976f8a99b71333e29bf929d54b4eb5e2768c` |
| intervals.csv | `ada545a9b32397b11c6e3c60dcd56d95d6de31cd25de79b9ea0a6e66a57e5987` |

## 독립성·실행 범위

root의 집계·정규화·조인에 대한 별도 내부 검산이다. 감사자는 R 수집과 B 카드 판독을 맡았으므로 R 근거 자체의 완전한 독립 원문 검증이나 외부 검토가 아니다. 외부 원문 추가 열람은0개다. 395개 metadata 레코드와75개 산입 레코드의 필수 정보, 핵심 반례를 검사했으며 모든 외부 원문의 render-equivalence를 다시 검증했다고 주장하지 않는다.

실제 로컬 Python을 실행했고 git show/rev-parse는 읽기만 했다. 첫 감사 실행은 root가 제거한 full_collector_fields를 가정해 KeyError로 중단됐으며 파일 쓰기 전이었다. 표준 findings.member_present를 사용해 재실행한 결과가 위27조건이다. [integration-audit.json](integration-audit.json)에 수정 전후 해시·조건별 관측·종료 코드가 있다. 감사자가 쓴 파일은 이 문서와 해당 JSON뿐이며 원장은 수정하지 않았다.
