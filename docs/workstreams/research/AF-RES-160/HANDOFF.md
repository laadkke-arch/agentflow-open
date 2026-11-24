# AF-RES-160 HANDOFF — PARTIAL

## 상태와 재개 지점
- 배정 원문: dot-control의 AF-RES-160, RUNNING. 계획판 ff5a037d4926e5c3ce6032bfa22c75b62f3c6aa8, 실제 base ff2302a9c02fe72eea915dc1612d1791d5c780ec (ahead 4, behind 0, 진행표만 변경). AF-RES-156 의존 39a138ca2b02e2c4f790efe197f6d33d41237878 고정, 지정 5 파일 및 상위 규칙 읽음. dot-control 변경하지 않음.
- 결과판 고정 SHA: 43a4c2fee6b48fa19f3bca026ef0a4dfd23805a2. [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/43a4c2fee6b48fa19f3bca026ef0a4dfd23805a2/docs/workstreams/research/AF-RES-160/RESULT.md), [SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/43a4c2fee6b48fa19f3bca026ef0a4dfd23805a2/docs/workstreams/research/AF-RES-160/SELF_CHECK.md), [원장](https://github.com/laadkke-arch/agentflow-open/blob/43a4c2fee6b48fa19f3bca026ef0a4dfd23805a2/docs/workstreams/research/AF-RES-160/sources.jsonl). 이 HANDOFF는 결과판과 구별한 마지막 별도 커밋이며 자기 SHA는 자기 파일에 넣지 않는다.
- **PARTIAL**: 정식 A/B 모집 순서·분모 미확인, GitLab 검색/원장 차단, NTRS native search 실패. 외부 검색으로 확인한 보조층은 대표 표본 아님. SEL 10개 프로젝트의 기술·기술관리 단계별 집계와 별도 이식 1개는 확인했으나 원카드·독립 인수 및 정확한 발행일 없음. 소프트웨어 12 비교 후보 중 동등 실측 대조 0. 90일 원장 0 확인(후속 작업 없음이 아니라 미관측). 원보고서 3개/독립 관측 계보 2로 6 요건 미달, 독립 배포·후속 결정 6 완결 미달. 개인별 성과 평가 없음.
- 고유 원문 22개(58 열람 원장 행, 28 success + 3 success text + 19 failure + 8 pending; 중복·초록/차단 제외). 방법 7, 교통 2, 기록관 2. 연속 화면 열기를 논리 열람 한 행으로 묶었으며 정확한 UTC 시분초 대신 일자 기록: 형식 미달. frame 28+8행(실패 조회 10, 보조 A10/B16), time-entries 166, deliveries 16, comparisons 12. 비교 가능한 OSUL의 4.25h/10점은 기술통계로만 기록.
- 전달할 핵심: SAMPEXTS 안정된 소스와 검토/문서 통합(2,038h 단계 인쇄총계), POWITS 다른 자세제어 계열 부품 채택·성능 미달 및 지연(11,677h). 두 임무는 동등 대안이 아니므로 차액·절감 단정 금지. GOESIM-REHOST 이식 실제 1,061.9 staff-hours, 이 중 컴파일 405.7, 시험 307.9; FORTRAN 198–220 staff-days는 가정 추정. G1 GitLab old artifact 제거/하류/CI 템플릿 수정, G3 vendoring/import 변경은 시간 미확인. 지원·교육·운영 경계를 함께 표시. EUVEDSIM 20,775h/121주 모델값은 실제로 오인하지 않도록 별도 보정.

## 커밋·검사
| 묶음 | SHA | 원격 재열람 결과 |
|---|---|---|
| ① 범위 | 3060d7c127166e58506ec5662b9ab8451e488848 | SCOPE.md exact |
| ② 모집 | 82ed3870c3b9c0993b065d4d1138538f5249876b | frame.csv exact |
| ③ 관측 | 9295c551b2ab6b217c840029ca09578b5d3dc1f0 | time-entries, deliveries exact |
| ④ 반례·비용 | 829b35383d37f6a524770f9504ffa27a67744b99 | time-entries, comparisons, frame-extra, sources exact |
| 보정 | e27b55e6809be66231ab06055c4b9e065e36a1a2 | 6 변경 파일 exact; 원판 보존 |
| ⑤ 결과·자기검산 | 43a4c2fee6b48fa19f3bca026ef0a4dfd23805a2 | RESULT, SELF_CHECK exact; base→결과 ahead6, behind0, 10개 변경 파일 모두 owned_path |

SELF_CHECK 입력 원격 파일을 JS로 직접 파싱: CSV 열수 오류/빈 셀/중복 ID/원장 참조 누락/duplicate_key 중복 각각 0. T2-7/T2-5 인쇄 합과 항목 합이 1–2h 차인 일부 프로젝트를 보존, 임의 수정하지 않음. GRODY 1989 합 22,863h, rehost 두 분해 각각 1,061.9h. 개별 근무 원카드는 미확보. 독립 검토 없음. 원격 텍스트 재열람 및 구조·산술 검사만 실행했고, checkout·manifest·workbench check·CI 또는 별도 실행기의 실제 검사는 수행하지 않았다. 체크아웃을 사용하지 않은 연구 작업이므로 manifest 생성은 당시 실행하지 못했다. 외부 원장 재현을 위한 실제 실행기 입력/명령은 아래.

## 다음 첫 행동
허용된 공개 네트워크에서 원래 모집을 다시 실행한다. GitLab 6 질의 모두 결과 HTTP 상태 및 페이지별 반환, X-Next-Page/다음 링크, 생성일·유형·iid·검색어를 보존하고 scope=all/issues, state=all, created_at asc, 전 페이지 동일 경계. 중복을 통합한 뒤 12/추가12를 확정, 공개 time_stats 및 timelog 존재/0/접근 여부를 먼저 기록한 후에 결정/납품 본문 조사. 사용자 계정·토큰 없이 접근 불가하면 공개 상태 그대로 저장하고 접근을 우회하지 않는다. NTRS native 검색 화면에서 1980–2005, SEL 발행자 필터와 네 가지 (software reuse/Ada reuse)×(effort/person-hours) 검색을 각각 실행, 보고서 번호·발행일·원본 URL의 반환 분모를 봉인. 이번 원장과 보조표본을 정식 frame에 자동 편입하지 않는다. 다음 최소 원문: SAMPEXTS FDD-552-91/007, EUVE TS FDD/552-90/045, Ada Reuse Study CSC/TM-91/6065; 실제 raw cards/승인 산출물과 후속 WMEF 필요. 
실행기가 있는 후속 세션에서는 현재 result SHA를 읽고 작업 충돌/허용 경로 먼저 확인한다. 원격 검사 재현 명령(별도 checkout에서, 검사 실행한 것으로 간주 금지):

```sh
git clone https://github.com/laadkke-arch/agentflow-open.git
cd agentflow-open
git fetch origin
git checkout work/research-af-res-160
task=docs/workstreams/research/AF-RES-160
python -B -m workbench.session start af-res-160 --allow "$task/" --dependency work/research-af-res-156=39a138ca2b02e2c4f790efe197f6d33d41237878 --output "$task/manifest.json" --fetch
python -B -m workbench.session check "$task/manifest.json" --fetch
git diff --name-only ff2302a9c02fe72eea915dc1612d1791d5c780ec HEAD
python - <<'PY'
import csv,json,pathlib
p=pathlib.Path("docs/workstreams/research/AF-RES-160")
s=[json.loads(x) for x in (p/"sources.jsonl").read_text().splitlines() if x]
assert len(s)==len({x["source_id"] for x in s})
print("sources",len(s),"counted unique",len({x["work_id"] for x in s if x["counted"]}))
for name in ("frame.csv","frame-extra.csv","time-entries.csv","deliveries.csv","comparisons.csv"):
    with (p/name).open(newline="") as f: rows=list(csv.reader(f))
    assert all(len(r)==len(rows[0]) for r in rows[1:])
    assert len({r[0] for r in rows[1:]})==len(rows)-1
    print(name,len(rows)-1)
PY
# 공개 API 응답 여부 확인 (다음 페이지까지 직접 순회; 아래는 첫 페이지)
curl --get --include 'https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab/issues' \
  --data-urlencode 'search=replace' --data 'scope=all' --data 'state=all' \
  --data 'created_after=2023-01-01T00:00:00Z' --data 'created_before=2026-01-01T00:00:00Z' \
  --data 'order_by=created_at' --data 'sort=asc' --data 'per_page=100'
# merge_requests 및 두 나머지 검색어로 반복. 각 확정 iid의 /time_stats 및 공개 timelogs.
```
재개 manifest는 후속 세션의 검사 기록이지 이번 작업 시작 당시 존재했다는 뜻이 아니다. 산출물 수정은 허용 경로 내 별도 재개 커밋으로 한다. 색인 제안: "AF-RES-160 · 노동 비용 원장/실제 대비 추정 · PARTIAL · 결과 43a4c2fee6b48fa19f3bca026ef0a4dfd23805a2 · SEL 단계집계/이식 및 GitLab 접근 실패, matched 순절감 미확인".

| 불일치·약점 | 영향을 받는 결론 | 다음 조사·자료 | 결론을 바꿀 관측 |
|---|---|---|---|
| GitLab 검색/시간 원장 차단, NTRS 원순서 미확인 | 정식 12+12 분모·빈도·대표성 | 6+4 공개 질의의 전체 반환·정렬 및 원장 먼저 확인 | 순서 확정 후보의 실제 시간/명시0/기본0/접근불가 분모 |
| 독립 원장 6개 미달, 납품/동등 대안 미확인, 모델 보정/반올림 차 | matched 순절감 부호 및 독립 납품 2건 | 개발 이력 FDD-552-91/007 등, 승인·원카드, 같은 기능/품질/기간 양쪽 노동 | 원카드→납품 일치 및 2개 이상 동등 실측 쌍 |
| 최초 발행 이후 90일 기록 없음, 교육·지원·하류 귀속 미확인 | 총 노동/후속 비용 역전 | 날짜 있는 release/WMEF 및 소비자/생산자 원장 | 양쪽 동일 창의 비중복 총계와 순증가/역전 여부 |
