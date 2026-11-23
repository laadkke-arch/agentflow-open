# AF-RES-091 #1 인계 · REVIEW_READY

## 식별과 결과

- Codex Cloud에서 `laadkke-arch/agentflow-open`의 `work/research-af-res-091`을 작업했다. 계획판은 `62a80b9f111c695527a8ca87bcb867796d2e96bb`, 실제 계약 시작은 `c2709abf8d25163eed75a7553ebcbde966105b55`다. DONE 의존은 AF-RES-087 `36a76b384810730b7d819a5ed469e6e8ded92f8a`다. [범위·시작 이력](SCOPE.md) · [작업 계약](manifest.json).
- 마지막 검사 및 GitHub 재열람 결과 SHA는 **`952c81311dc7b5917fa04af6e4513dc5fd7020b0`**다. 조회 경로는 아래 결과판이다. 이 파일만 마지막 단독 커밋에 추가했다. PR은 미생성이다. [고정 결과판](https://github.com/laadkke-arch/agentflow-open/tree/952c81311dc7b5917fa04af6e4513dc5fd7020b0/docs/workstreams/research/AF-RES-091) · [인계 파일 이력](https://github.com/laadkke-arch/agentflow-open/commits/work/research-af-res-091/docs/workstreams/research/AF-RES-091/HANDOFF.md).

| 묶음 | 원격 커밋 |
|---|---|
| ① 입력·수작업 정답·T/P 통제식 | `9b50163c4b810e387adfcc41f88958693ae29bac` |
| ② 고정 writer·5개 파일·3개 거절·footer·공개 소비 코드 | `2a61924a955d74f63d9941ad86e2d710ac3065c9` |
| ③ 16자리·실제 10개 reader·대조·원 출력 | `65e44c2094a0f6093fd429a3a5dd572a63a242ea` |
| ④ 세 표·권고·동일 bytes 반례·원장·자가검산 | `952c81311dc7b5917fa04af6e4513dc5fd7020b0` |

## 판정과 근거

WKB 4셀과 동종 2D native 1셀의 성공한 10/10 판독은 T와 P 모두 예상 ID·score를 반환했다. 혼형 native S1–S3은 빈 단수 Point가 함께 있어 writer가 ArrowInvalid로 거절했고, 해당 6회 및 6대응쌍은 미관측이다. 가능한 대응쌍 2개는 S0이다. 지정 좌표의 S0에서 원 T는 A/B이고 P는 A이므로 각 술어를 자기 정답에 대조했다. [세 표와 분모](RESULT.md) · [판독 집계](evidence/read/summary.json).

별도 혼형 native 파일은 A를 MultiPoint로 복원해 교차 P에는 A를 남기고 exact T에서 A를 뺐다. A/B 중 원 Point인 행을 바꾸어도 같은 native bytes를 얻었다. E만 제외한 S2의 유한 Z 두 값은 유지됐고 S3의 B는 footer 표현에 NaN Z가 있어도 고정 reader에서 2D였다. 위치만 검사하는 현재 호출과 원 타입·Z에 의존하는 호출에 다른 링크 조건을 붙인다. [동일 bytes](evidence/auxiliary/type-alias.json) · [Z raw](evidence/auxiliary/S3-drop-E.json).

[원장](sources.jsonl)은 직접 읽은 산입 52건과 독립 저작·사건 38개를 담는다. [후보 검색](evidence/consumer-search/README.md)은 세 지정판의 exact T 결원과 libpysal의 다섯째 P 결원을 기록했다. exact T의 외부 공개 사례 및 Dask 실제 .cx 호출, 별도 Arrow/Pillow 원 시험은 [소비 원장](consumers.csv)과 [실행 영수증](evidence/external/upstream-tests.json)에 있다.

## 원격 재열람과 검사

모든 종료값은 **결과 `952c81311dc7b5917fa04af6e4513dc5fd7020b0`** 대상이다. 2026-11-23 16:59 UTC GitHub 새 checkout의 tree는 `5bbf6d499de56774abcf7292a93ec26de7bb54c2`였다. 변경 79/79 경로가 허용 경로 안에 있고 Git blob과 로컬 검증 bytes가 일치했다. GitHub 파일 도구로 세 결과표·원장·성공 판독·writer 오류·동일 bytes 반례를 다시 열어 5개 blob을 대조했다. [자가검산](SELF_CHECK.md).

| 명령 | 종료·확인 범위 |
|---|---|
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-091/manifest.json --fetch` | **0** · passed / remote_checked, manifest 자체를 제외한 78경로와 고정 087 의존. 범위 이탈·미통합·오류 각각 0. |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | **0** · doctor, `scripts/check.py --require-git`, reference-audit discovery, 원 smoke 모두 종료 0. 공통 check-all은 no_active_sessions를 반환했다. 091 계약은 위 개별 검사로 실시했다. |
| `python -B docs/workstreams/research/AF-RES-091/audit.py` | **0** · 쓰기와 판독 자리, T/P·차원·원 결과, 원장 하한과 표 연결. [명령과 입력](reproduce.md) |

결과 SHA 검사에서 stderr는 세 명령 모두 0 bytes였다. 저장한 stdout 지문은 task check `17286eb374135207c30482b4255d83d6dfbbb0a56d713841989acd1001f8709f`, 공통 `920d2786f19f03df70445dd0c61fe580453bfbfd00a79eff62922f3f79433b6f`, 자가검산 `26c4f60f1d9036b3fd0171cc922c6336efa5560bb2a330eb539c26ce2e17fdb7`다. 원격 결과 [RESULT.md](RESULT.md)의 SHA-256은 `0efee5b042be5579e05b35b287b8fe7a33d23b076fcc4556b127f4d5e3ce8dee`, [sources.jsonl](sources.jsonl)은 `87ec23c98258e291352c1a588d4be74375027dd89d090f6afbd8784e1a3f822c`, [runs.jsonl](runs.jsonl)은 `12c2dc06799f24ec9edd3512b98fd322481ecdad257ba46d8a2439dec4503305`다.

087의 기존 격자·옛 GDAL·원 48개와 독립 검토는 미실시다. 새 스택, 다른 거리/조인, 087 안내의 실제 하류 실패 이력은 미확인이다. [검증 범위](SELF_CHECK.md).

## 색인 제안

> AF-RES-091 · REVIEW_READY · 결과 952c81311dc7b5917fa04af6e4513dc5fd7020b0 · 쓰기 8개 중 5파일/3거절, 16자리 중 실제 10판독 모두 T/P 일치 · 동일 native bytes에서 원 Point 행이 달라질 수 있음 · reader와 행 선택·타입·Z 계약을 함께 인계.

## 다음 첫 행동과 핵심 약점 3건

1. 원격 결과판의 [S1 거절](evidence/build/S1-native-writer.json)과 [S3-drop-E 파일](evidence/auxiliary/S3-drop-E.parquet)을 먼저 연다. 새 고정 스택에서 원 S1 단일 native 쓰기와 기존 S3-drop-E SHA의 B를 대조한다. E를 포함해 생성되거나 같은 B의 NaN Z가 3D로 판정되면 판별 링크를 새 판별로 갱신한다.
2. 실제 사용자의 공간 호출에 경계점과 2좌표 MultiPoint가 있는 표본을 확보한다. 정렬 ID·score 또는 Point gate 결과가 달라지면 위치용 안내를 해당 술어 및 입력군에 좁힌다.
3. 087 문구 인용, 파일 SHA, reader import 판, 원 기대 ID/Z가 함께 남은 하류 보고를 한 건 찾는다. 동일 환경에서 실패를 확인한 경우에 문서 수정 필요도를 다시 판정한다. [조사 조건 3건](RESULT.md#핵심-약점과-판정을-바꿀-관측-3건).
