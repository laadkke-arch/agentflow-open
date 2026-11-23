# 재개 조사 원장 정규화

## 범위와 계수 단위

이 파일은 AF-RES-077#2의 사후 재검토 자료를 SOURCES/COSTS에 연결한다. 원 모집·봉인 packet·reader·FRAME·TESTS를 다시 쓰지 않았다. 모집·효과·실행 분모도 바꾸지 않는다.

- 원래 원장 **302행**에 재개 원장 **56행**을 연결한다. 재개 행은 외부 도구 read-operation 50행과 이미 보존된 원시험·fixture의 로컬 재판독 6행이다.
- 재개 원장 전부 `core20_eligible=false`. 기존 저작의 확인·한계·반례 재대조이므로 named works **24**, conservative lineages **21**을 유지한다.
- MS 공식 tracker 281441의 캐시 원문은 PR4590과 **MS-REQUEST-4590** 계보로 묶는다. 별도 신규 원저작으로 세지 않는다.
- SG의 기존 audit 내부 식별자 `SIGIL-ISSUE-450`은 최종 원장의 기존 **SG-REQUEST-450**에 대응한다.
- `SOURCES.jsonl` 행 수는 문서/작품 수·독립 표본 수·HTTP 수와 같지 않다.

## 비용

| 재개 주체 | 도구 read operations | GitHub reads | web open | web find | 접근 실패 | find 불일치 |
|---|---:|---:|---:|---:|---:|---:|
| Shotcut 검토자 |15|10|5|0|0|0|
| MuseScore 검토자 |16|4|7|5|2|2|
| Sigil 검토자 |17|10|2|5|0|2|
| root tracker 재요청 |2|0|2|0|2|0|
| 합계 |**50**|**24**|**16**|**10**|**4**|**4**|

기존 기록의 **222 recorded / 224 reported**는 **재개 이전 top-level request 구성요소의 불완전한 합계**로 보존한다. 재개 50은 cached web find를 포함한 도구 read-operation 단위다. 두 수를 더해 HTTP 전체 요청이나 총 작업량을 만들지 않는다. 재개 네 비용행의 `incremental_request_attempts_to_existing_root`는 모두 **0**이며 `resume_*` 열에서만 더한다.

도구 내부 HTTP 재시도·캐시 hit·redirect·token·과금·전체 active work는 계측하지 않았다. 재개 50도 정확한 전체 비용이 아니다. SOURCE에 추가한 로컬 원시험 source 2개·reference fixture 3개·원 EPUB 1개는 외부 read-operation 기여 0이며, 개별 로컬 open 수의 완전한 원장은 아니다. 기존 보조 실행을 재실행하거나 새 목표 실행으로 세지 않았다. 새 봉인 reader 노출 **0**, 새 native 실행 **0**이다.

## 보존한 정정·접근 경계

TEI P5 4.8.0의 `#TCAPWL`은 **§13.1.4.3 The Witness List**다. 기존 ROOT-TEI48의 “Witness Information”은 상위절 §13.1.4 제목과 섞인 표기다. 새 `RESUME-MS-TEI48` 및 그 재열람 행의 `correction_evidence`가 정확한 하위절을 명시한다. 과거 원문 발췌·판독·접근실패 기록은 변경하지 않았다.

원 tracker의 캐시 본문 확인은 새 증거층이다. 과거 `MS-ORIGINAL-281441`와 `MS-POST-original_issue`의 HTTP403은 당시 요청 결과로 그대로 유효하다. 캐시 확인 후 검토자의 두 line-open과 root의 두 재요청 역시403이었다. 캐시가 보였다는 이유로 직접 origin 접근이나 최초본문을 확인했다고 쓰지 않는다.

root는 `https://musescore.org/en/node/281441`의 두 failed web open을 약 **2026-11-23 12:33–12:34 UTC**로 보고했다. refs는 `turn435172662view0`와 `turn377002549view0`이다. 첫 요청은 URL, 둘째는 agent ref로 같은 원문을 다시 열었다. 두 원본 tool-response payload는 audit JSON에 보존되지 않았으므로, `RESUME-ROOT-MS-TRACKER403-1/2`는 **root의 관측 요약+원 tool ref**에 근거한다. 정확한 per-call UTC·raw-response 재검산은 미확인이다.

## metadata 결손

- SC는 일부 요청의 직접 시간과 나머지의 인접 시각 bounds를 구분한다. metadata가 없는 duration을 계산하지 않는다.
- MS는 같은 날 확인 및 기록 시각만 있고 정확한 요청별 UTC가 없다. page 캐시의 “1.3 years ago” 표시를 실제 게시·개정일로 바꾸지 않는다.
- SG의 `2026-11-23T12:33:47Z`는 완료 상한이며 각 요청 시각이 아니다.
- 이 정규화 작업은 세 검토자의 read metadata를 결합한다. 기존 review에서 직접 읽은 원문을 다시 네 번째 독립 판독으로 세지 않는다.

## 재생성 및 idempotence 검사

재생성 명령:

```sh
python -B docs/workstreams/research/AF-RES-077/evidence/assemble_registry.py
```

generator는 기존 COSTS에서 자신이 생성한 POSTSEAL·RESUME·AUXILIARY 행을 먼저 제거하고 입력 ledger에서 다시 붙인다. SOURCE는 네 input JSONL을 처음부터 결합한다.

**실제 두 번 실행:** 2026-11-23T12:40:02.418090+00:00에 종료를 기록했다. 주체는 재개 사후 원장 정규화 담당 모델이며 두 실행 종료값은 모두 **0**이다. 두 실행 사이 출력 세 파일의 SHA-256이 모두 일치했다. 기준 코드는 현재 작업 트리의 assemble_registry.py이며 아직 새 커밋 SHA는 부여되지 않았다. 뒤의 root 검사는 최종 결과판을 별도로 확인한다.

| 생성 파일 | 두 실행에서 일치한 SHA-256 |
|---|---|
| SOURCES.jsonl | b27dba46d63ae580b2e9746ad1662cb085fbfc723711c954234a0368e5a803b5 |
| COSTS.csv | 5534f8a421f9a0b3c1e5fb750bdd150d49f9e0ae167bb77563c080427a5814c0 |
| evidence/COUNTS.json | 15330e3cba8add639adb5864e7c380d5401831a2aa036f194e1616efa25f4a6e |

출력은 source358행, named24/conservative21, frozen9, target execution0, narrow auxiliary predicates5, pre-resume reported requests224를 두 번 동일하게 반환했다. 이 통과는 원장 재생성의 결정성만 확인한다. 연구 가설이나 목표 GUI 동작의 시험 통과가 아니다.

