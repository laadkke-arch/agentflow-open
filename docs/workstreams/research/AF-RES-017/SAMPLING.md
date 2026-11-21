# AF-RES-017 — SAMPLING v1 (수집 전 동결)

## 관측 창·정렬·시드

공개 사건의 결정·발견 관측 창: 1990-01-01~2026-11-21. 방법 문헌에는 그 이전 원전을 허용한다. 검색은 2026-11-21 이후 실제 세션 UTC를 기록한다. seed=`AF-RES-017-20261121-1717`, numeric=1717. 검색엔진 반환 순서대로 첫20개 고유 후보를 screening하고, 동일 query 확장 page/추가 질의는 로그에 기록한다. 순위가 제공되지 않으면 반환 순서라고 쓴다. 재검토/블라인드 패킷은 SHA256(seed+case_id)순이다. 확률표집이 아니다.

## 계열별 사전 검색 경로·질의

| 계열 | 경로 | 최초 질의(영문 그대로) | 목표 |
|---|---|---|---:|
| a engineering retrospective | 공식 엔지니어링 블로그→해당 구현/릴리스 | `"replaced our homegrown"`; `"didn't know" "library" "rewrote"`; `"why we built" "existing solutions"`; `"migrated back" "engineering"` | 14~16 |
| b public ADR | 공개 ADR GitHub→fixed SHA→superseding ADR | `"ADR" "superseded" "library"`; `"architecture decision" "replace" "custom"`; `"adr" "revert"` | 4~6 |
| c PR/issue | 공개 GitHub search→merged PR→commit/release | `"replace custom" "library"`; `"remove homegrown"`; `"use stdlib" "revert"`; `"did not know" "reinvent"` | 12~16 |
| d standard revision | 013 strict6 후보만→후속 원문 | C07/C12/C14/C21/C29/C31의 fixed `superseded_by`; 외부 실체와 늦은 인지 없으면 제외 | 0~3 |
| e postmortem | 공식 사고 보고→이전 기법의 날짜 근거 | `"postmortem" "did not know"`; `"outage" "learned" "circuit breaker"`; `"incident" "retry" "backoff"` | 4~8 |
| f empirical reinvention | 원논문/저자 공개판→관측 사례 식별 | `"software reuse" "reinvention" empirical`; `"not invented here" software study`; `"rediscovery" software engineering` | 사례0~4, 방법>=5 |

계열은 발행 플랫폼이 아니라 실제 증거 문서 종류로 고정한다. 블로그에 실린 공식 사고 보고는e, GitHub의 명시 ADR은b, 코드 PR은c. 같은 글을 여러 계열로 쪼개지 않는다. 목표 합계40 이상, 어느 계열도40% 초과 금지, 조직/저장소 최대3. 목표를 달성하지 못해도 계열 이름을 바꿔 배분하지 않는다.

## 순차 표집·건너뛰기

먼저 반례층(known_rejected>=5, adoption_rollback>=3)을 찾고 일반층을 채운다. 채택 후 되돌림은 실제 외부 해법 채택과 이후 철회를 모두 읽는다. vendor→vendor 이주만 있고 자체 구현·늦은 발견 관련성이 없으면 보조 비교로 둔다. source_family별 첫 적격을 채택하되 quota_exceeded는 이유와 함께 제외 원장에 남긴다. 동일 사건은 canonical URL+조직+선택 범위로 중복 제거한다. 공개 원문 미확보/월 미확인/발견 사실 미확인/직접 변경 증거 없음/단지 신규 출시/후기 추천/2차 전언/기존013 재표집은 각각 사유를 남긴다. 날짜가 부족한 후보는 완성 사례로 세지 않는다.

## 방법·비교 문헌 수집 경로

- 소프트웨어 재사용/NIH/재발명 실증>=5: ACM/IEEE 본문 또는 저자/기관 공개판; Frakes & Fox reuse factors, NASA reuse empirical work, reuse adoption/cost studies, NIH 조직 실증. 단순 논설을 실증으로 세지 않음.
- 의학>=3: Chalmers & Glasziou 2009; Lau1992 cumulative meta-analysis; Fergusson2005 aprotinin; 출판사/PMC/저자 공개판.
- 특허>=3: USPTO 재심사/IPR outcome 공식 통계; NBER/저자 공개판의 prior-art discovery·invalidation 연구.
- 다중 발견>=2: Merton 원문과 독립 재발견 실증 원문.
- 사후 판단>=2: Fischhoff1975 및 Roese/Vohs2012 원문/저자판.
- Q8 도입 경로>=5: circuit breaker, backpressure, queueing/Little, WIP/Kanban, double-entry ledger, checklist/incident command 중 실제 제작자/원논문. 기존010은 형식만 참고하고 이번에는 원문을 열어 역사 경로를 확인한다.

한 site 최대3개만 문헌 최소수에 산입, 실제 저작물 중복은 합친다. PDF 추출/본문 읽기는 허용되나 전문 저장은 안 하고 메모만 남긴다. 막히면 공개 저자판 등 정상 경로를 찾고 접근 통제를 우회하지 않는다.

## 사전 반증 질의

1. `"why we built" "didn't use" "library"` / `"knew" "existing" "homegrown"` — 합리적 거절.
2. `"reverted" "migration" "library"` / `"moved back" "database" engineering` — 늦은 채택 후 번복.
3. `"did not exist" "when we started" software` — 결정 당시 부재.
4. 각 고정 need의 보통명사1~2개만 질의 — 현재 easy-hit, 역사 발견 가능성과 분리.
5. `"circuit breaker" "metaphor"`; `"kanban" "not" "limit"`; `"backpressure" "analogy"` — 장식/기계적 대응 없는 이름.

## 현재 수집 상태

이 커밋 전에는 저장소 기준·고정 선행입력·호스트 접근만 읽었고 새 외부 사례/문헌 수집은 시작하지 않았다. 실제 질의/skip는 SEARCH_LOG.json과 evidence/<lane>/selection.json에, 추가 질의는 UTC·purpose·result_note와 함께 기록한다. 이 문서의 계획을 실제 실행 횟수라고 보고하지 않는다.

## 실행 뒤 추가한 관측 기록 — 사전 계획 변경 아님

수집 원장40건은 a16/b3/c16/e5이다. ADR 목표4–6에는 미달했다. d의 고정013후보는 외부 발견 근거가 없어 새로운 사건으로 넣지 않았고, f의 실증 자료는 개별 월별 사건 대신 방법·비교 문헌으로 사용했다. 최종40관측 중 월·결과를 갖춘 최소 사건18, 좁은 인과 양성4이며 나머지를 완성 사례로 승격하지 않았다. 이 차이가40적격사례 수량 조건의 미충족 이유다.

건너뛴 후보와 이유는 `evidence/blogs/selection.json`, `evidence/prs/selection.json`, `evidence/root/sources.json#excluded`에 있다. root에서는 PrestaShop ADR14/18(내부 이행 단계), Hardcount ADR007(외부 해법 실제 채택 없음), OpenedX devstack(취소된 내부 프로토타입), 원문을 얻지 못한 학생 ADR을 제외했다. B01·B15는 날짜 보강 후에도 미상으로 남겼다. 현재 검색40개는 각 lane의 원 반환과 통합 SEARCH_LOG에 남겼다. 모든 기록의 건수를 검색엔진의 전체 후보 수로 해석하지 않는다.
