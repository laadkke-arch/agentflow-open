# SELF_CHECK — 원격 고정판 재계산 (같은 작업자의 자체 검산, 독립 판독 아님)

| 잠정 답 | 근거 자료 주소·위치 | 반대 가설 | 실제로 찾아본 반례와 결과 | 미확인 | 답을 바꿀 다음 관측 |
| --- | --- | --- | --- | --- | --- |
| Q1: 현재 모집창에서 8건 선택; 표본 최초판 불명 | [frame](frame.csv) 80행 / [packets](packets.jsonl) 앞8행, REQ-* | 분류/편집판이 선택을 바꾼다 | FreeCAD #11892/#11911, Joplin #9641 경계 사례; 기존 후보 유지하되 민감도 기록 | 최초 편집판·독립 분류 | 고정 원문/타 판독에서 층의 최초 두 건 달라짐 |
| Q2: R0 검색 전 8초안만 실제 | [drafts](drafts.jsonl) 8행, 43b1cd97b86d473395e8d0f2ea987ad4691abdbf | 신규처럼 보인 대안은 이미 인지 | None·AST·포트 제거·duplicate name·#9669 recurrence 이미 있음; FNV1a 8/8 일치 | 독립 초안, 원저자 최초인지 | R1/R2 독립 선봉인 초안 16개 및 기존 인지 목록 |
| Q3: A/B 효과는 미확인; 파일럿 8 표지 | [discovery](discovery.jsonl) 전체 8행; 227a522a2e6339345681fabc9e493827b1ee3916 | A만으로 충분하거나 B는 후보 주입 효과 | J-W2 Compose 확인 및 F-W2 동일 CAD; F-P2 ezdxf, J-W1 SAF 이름 주입, S11 접근 실패 | 동일 사건의 두 독립 검색·순위·시간 | 16개 새 검색 문맥·질의/원문 예산과 기록 봉인 |
| Q4: 근접 기능의 조건과 사후 이종 원리 제안 | S05,S07,S08,S10,S14,S16,S18,S21,S22,C01–C04 [sources](sources.jsonl) / [comparison](comparison.md) | 이름/원리가 같아도 보존값은 깨진다 | ezdxf XCLIP 미처리/scale, GDAL flat layer 및 dimension fallback; 원본 삭제/물리 lockout 무단 이식 기각; archive 예외 C05 | 실제 대응 시험, 그 시기 사용 가능성 | 실제 fixture가 치수·로컬 파일·내부 접근 보존하거나 위반 |
| Q5: 자기 수정8, 독립 수정0 | [readings](readings.jsonl) 8행; [adjudication](adjudication.csv) 8행 | 새 시험처럼 보이는 표현 변경 또는 본래 대안 | J-P1 기존 keyboard/Tab, J-W2 포트 제거 이미 앎, J-P2 recurrence 이미 앎; S04 오염 | 가림 배포·새 독자 및 원저자 채택 | 독립 사전/수정 16쌍, 각 근거 줄과 결정 비교 |
| Q6: 유효 짝0/8; 사후·중복 제외 후 동일 | [adjudication](adjudication.csv), [sources](sources.jsonl), [comparison](comparison.md) | A/B 같은 안 또는 새로운 안이 필수조건 위반 | AtomicFile lock 없음/URI 한계, F110 sticky footer, 고심각도 dismiss, Moby 특정 version; S11/C06/C07 제외, C01–C04 비분자 | 독립 가림 판독, 실제 실행 | 판독자가 사전 부재·원전 성립·보존·수정/시험을 모두 확인한 유효 짝 |
| Q7: 단계 경과만 계측; A/B 비용비 산출 불가 | [costs](costs.json) measured/unknown/group_counts | 추가 탐색·정리 시간이 편익보다 클 수 있다 | 22질의/22시도/21성공, 사후 6/8/6; 두 경과 209.244s 및105.899s, 동일 작업자 혼재 | 개별 문맥/사람 노동/원저자 재작업·편집자 시간 | 실제 각 역할 start/end, 실패와 개봉량, 유효 짝 비용 비교 |

## 실제 검사
고정판 caac3893405e1d3b655b495b7fdb61d1a6568e2e에서 8 원장/비용 파일을 GitHub fetch_file로 다시 읽어 CSV/JSONL 파싱, row join, ID·지문·분모·상한·시간을 JavaScript로 재계산했다. 표 1은 baseline packets + drafts + discovery, 표 2는 discovery + sources와 사후 4개 원전, 표 3은 readings + adjudication + 비용으로 생성했다. 국문 요약은 동일 R0의 수동 코딩이며 가림 판독 아님. 소스 내용 자체 재현/타 판독/실행 검증으로 오인하지 말 것. Git shell 접근 시도 실제 실패: `timeout 10 git ls-remote --heads https://github.com/laadkke-arch/agentflow-open.git work/research-af-res-145` → exit 128, Could not resolve host: github.com. 따라서 로컬 checkout/재현 스크립트 실행 못함; 다음 검산용 `python3 docs/workstreams/research/AF-RES-145/verify_ledgers.py` 입력은 현재 branch의 원장. 스크립트는 아직 실행 안 함.

```json
{
  "screened": 80,
  "classification": {
    "FreeCAD/FreeCAD P": 19,
    "FreeCAD/FreeCAD X": 18,
    "FreeCAD/FreeCAD W": 3,
    "laurent22/joplin X": 23,
    "laurent22/joplin P": 11,
    "laurent22/joplin W": 6
  },
  "chosen": 8,
  "earliest_strata": true,
  "packets": {
    "baseline_input": 8,
    "pilot evidence exposure log, NOT blinded delivery": 8
  },
  "selected_bodies_match": 8,
  "draft_hash_matches": 8,
  "joined": true,
  "distinct_source_ids": 38,
  "ledger_rows": 38,
  "counted_rows": 25,
  "counted_unique": 25,
  "counted_by_role": {
    "original request": 8,
    "supplier": 8,
    "boundary": 4,
    "supplier-extra": 1,
    "nonsoftware-control": 4
  },
  "counted_no_failed": true,
  "discovery_sources_exist": true,
  "reading_sources_exist": true,
  "judge_sources_exist": true,
  "queries": 22,
  "distinct_query_strings": 18,
  "attempts": 22,
  "successes": 21,
  "budget_ok": true,
  "blind_readers": 0,
  "valid_conditions": 0,
  "judge_classes": {
    "비교불가": 8
  },
  "test_executed": 0,
  "post_not_in_discovery": true,
  "post_time_order": true,
  "stage_wall_s": [
    209.244,
    105.899
  ]
}
```

- 하한: 8 + 8 + 4 + 4 = 24; 실제 25(추가 공급자 Ventus 1), 서로 다른 work_id 25. 접근 실패 3, 나머지 보충/중복 10. 독립 저작 수를 38행 또는 80모집 건으로 부풀리지 않았다. 사후 4원전과 C05–C08을 자발 발견에서 제외, 같은 원리/문서 재열람 제외 이후 비교가능 0/8 그대로. 유효분모 없으므로 비율 산출 불가.
- 실제 수정 8 자기쌍, 독립 목표16 중 0; 원전 열람 후 제안 시험과 실행(0)을 별도. 미확인 값 null/unknown으로 보존. 결론 PARTIAL.
