# AF-RES-022 범위·표집 동결

## 고정 입력과 실제 실행

- 저장소: laadkke-arch/agentflow-open. 작업 브랜치: work/research-af-res-022.
- 배정 시 직접 읽은 foundation SHA: `435a5099a0abb0bb4b3c08d40401d0e304e82153`.
- 계획 기준판: `b507fbcab09724a77270e658355f4b661cc35f02` (브리프 지정 입력; 계획의 다른 작업 결과는 읽지 않음).
- 의존 AF-RES-017: `34c14d6d2ad8802cf68ff9d9db4a3f810b4e057a`; HANDOFF 전체, RESULT Q2·Q4–Q8, cases/CASES.json ID·대상·URL, evidence/statistics.json의 전체 구조/집계. 기존40관측 및 별도7기원은 중복 배제용이며 새 표본으로 세지 않는다.
- 의존 AF-RES-020: `856e6b40ae12d43197a6f02f7bf6ab7a7506fd35`; HANDOFF와 bundles/B21.md. 발견·전이 관측과 실제 효용의 분모가 다름을 입력 한계로 보존한다.
- 실제 모델의 세션 표기: **GPT-6 Astra Pro**. 같은 상속 모델의 내부 하위 에이전트가 ADR·Apache·B 조사 경로를 나누어 읽는다. 사람 코더나 독립 모델간 재현 실험은 아니다.
- 실제 실행 위치: ChatGPT 제공 Linux cloud workspace `/workspace/scratch/3742f7a04774/agentflow-open`, Bash·Python·Git 및 GitHub 연결/공개 웹 검색. 사용자의 PC에서 실행하지 않았다. UI의 별도 모델 선택·reasoning 등급은 관측하지 않았다.
- 모든 저장소 변경은 `docs/workstreams/research/AF-RES-022/` 아래. 공통 계약·진행표·색인·제품 코드와 main은 수정하지 않는다.
- 공통 manifest start --fetch는 exit0, 의존 두 SHA를 그대로 고정함. 실제 명령/결과는 manifest.json에 있다.

## 사전 고정 모집 경로

관측 창: 최초 공개 제안/새 선택이 **2018-01-01~2024-12-31**에 있는 결정. 결과 검색은 실행 확인일인2026-11-22 UTC까지 허용하되 당시 정보와 분리한다. 각 날짜는 제안·필요·최초 공개 구현·공식 결정·발견·시행 중 무엇인지 명시한다. 뒤 날짜를 처음 고민한 날로 대체하지 않는다.

A는 **한 팀의 한 선택**24건을 세 계열에서 연속 적격8건씩 고른다. 결과·revert·미인지·발견 진술은 선정 변수에서 제외한다. 제목/목록/생성 메타데이터를 먼저 보았고 검색 결과에 부수 노출된 상태는 선정에 쓰지 않았다. 본문은 포함 여부를 확인할 때 최소한으로 읽고 선정 뒤에 후속 결과를 읽는다. 완전한 실험적 맹검이 아닌 결과 비조건 표집이다.

| 계열·ID | 원장/고정판 | 시작점·정렬·상한 | 포함·탈락 규칙 |
| --- | --- | --- | --- |
| F1 저장소에 보존된 결정 문서 A01–A08 | Backstage docs/architecture-decisions/index.md, ffe93e7aa7ebcc429ed98bfd02810314a6f27c73; Kibana legacy_rfcs/README.md 및text/, dd31e406be605f8db329a9d3bf36164c1425a43c (각2024년 말 마지막 커밋) | 각 프로젝트2018-01-01 시작, 최초 공개 제안시각 오름차순·동률 경로순; 프로젝트당4, 합8 | 구현/재사용/구매의 구체 선택. 내부 구현 대안도 포함. 문체·명명만·관리절차·오탈자만은 제외. 공개 제안시각이 없으면 최초 파일 commit을 대리로 명시. |
| F2 Apache 공개 제안·표결 A09–A16 | Flink Improvement Proposals Confluence page65145551; CQL 원본은 streams/apache/frame_inventory.json | 원 page 생성2018-01-01 시작, 생성 UTC 오름차순·동률 번호; Flink 상한8 | 런타임/API/의존성 구현 선택. 원 제안이2018년 이전이면 제외하고 다음 순번. 문서/명명/거버넌스만 제외. linked discussion/vote를 따라가되 결과를 표집에 쓰지 않음. |
| F3 조직 공개 설계 검토 PR A17–A24 | rust-lang/rfcs GitHub PR 원장; query repo:rust-lang/rfcs is:pr created:2018-01-01..2024-12-31 sort created asc | 2018-01-01 시작, created_at 오름차순·동률 PR번호; 프로젝트 상한8 | 언어/표준라이브러리/도구 구현의 구체 선택. 동작을 바꾸는 개정안은 새 선택, 단순 오탈자/문서 링크/이름/관리절차는 제외. 동일 선택의 여러PR은 연결하고1건. 미병합/거절/미실행도 적격이면 남김. |

F1은 채택된 문서의 생존편향이 있고 F3은 거절/미병합도 포함한다. 이 차이를 감추지 않으며 F1의 분모를 조직 전체 의사결정이라고 부르지 않는다. Kibana의 현재 ADR 경로 `x-pack/platform/plugins/shared/workflows_management/dev_docs/adr/`는2024년 뒤 자료이므로 역사표본에 넣지 않고 공개 legacy RFC 원장을 사용한다. 실제 경로 발견/전환 근거는 streams/adr에 남긴다. 접근 불가 항목은 탈락/미확인으로 남기고 같은 원장 다음 순번을 따른다. 임의 성공 사례로 교체하지 않는다.

B는 A와 별도의 **발견 진술을 겨냥한 목적표집8건 이상**이다. 두 모집 경로는 (1) 유지보수자의 공개 GitHub issue/PR 답글 (2) 당사자 engineering 회고 및 연결 토론. 최초 선택2018–2024, 프로젝트당2, 017중복 제외, 같은 선택의 여러 문서는1건이다. 정확한 질의·검색순·탈락은 streams/b/recruitment-plan.json과search-log.json에 보존한다. 명시 미인지/처음 소개/알던 대안 재평가/단순 언급/인지 미확인을 구별한다. A와 겹치면 linked_A_id로 연결해 B 고유추가분에 세지 않는다. B로 발생률을 계산하지 않는다.

반례 검색은 후기발견 자체유지, 소개후무변경, 외부채택후철회 각각3표현 이상×GitHub토론/회고2계열. 실패 검색도 저장한다. 긍정 사례 부족은 실패가 아니라 자료 공백이며 강한 판정을 억지로 만들지 않는다.

## 사전 판정

- 엄격 연결(connected_chain): 원 의도와 시간, 당시 사용할 수 있던 공식 판/조건, 누가 언제 무엇을 알았다는 직접 진술, 실제 실행 근거가 모두 연결됨. 직접 미인지와 발견 때문에 선택을 바꿨다는 인과진술(strict_discovery_change)은 별도 더 강한 하위집합이다.
- 처음 소개된 메시지는 제안자가 알던 시점만 증명할 수 있다. 결정자의 답이 없으면 결정자 인지는 미확인이다. ADR accepted/PR merged는 제안·문서 수용과 제품 구현을 구별한다.
- alternative availability: yes/no/unknown. 최초 저장소 공개/필요 기능 추가/안정판/팀의 사용가능 시점을 분리한다. 현재 문서로 과거 기능을 소급하지 않는다.
- outcome: retained/replaced/partial_adoption/trial_reverted/change_unconfirmed. 제안거절이 자체 제품 구현의 유지까지 증명하지 않으면 change_unconfirmed로 둔다.
- 비용: observed_effort / calendar_elapsed / change_size / author_estimated_saving / researcher_counterfactual_unknown. 원 단위·귀속 범위가 같은 경우만 합산. 삭제줄=버린 노동, 경과일=인일, 전체장애=미인지비용으로 바꾸지 않는다. 재사용한 부분도 기록한다.
- A 비율의 분모는24고정. 엄격 발견 수와 인지 미확인 수, 후발 대안을 따로 보고한다. 가능한 관측범위는 미확인을 모두 음성/모두양성으로 놓은 논리적 민감도이며 통계적 신뢰구간이나 모집단 추정이 아니다. 후발 대안은 조기추천 가능양성 상한에서 제외한다.
- 타 분야: 특허 심사 전후 청구항 변경/유지와 공학설계 시간순 관찰 원 연구, 각2고유 원문 이상. EPO원장이 막히면 동일 유형 공식 공개 특허 원장/심판기록을 사용하고 실패URL을 보존한다. 논문이라는 운반 형식·다른 언어 구현·진짜 타 분야 구조를 분리한다. 017의7경로는 재산입하지 않는다.

## 자료 원장과 검사

sources.json 각 항목: source_id, case_ids, questions, url, published_or_version, checked_utc, location, observed, limitation, evidence_kind, lineage, count_category, count_in_minimum, access. 직접 읽은 고유 외부 원문만 산입한다. 검색결과·초록만·차단·미러·내부보고는 별도이며 동일저작의 재게시를 독립 근거로 세지 않는다. 사실/저자진술/이번실행/연구자해석을 분리한다. 저작별 직접인용은25단어 이내, 본문은 짧은 자기말 요약이다.

최소 원문36=당시결정16+별도후속10+공식판6+타분야4(각분야2). 이것은 표본32와 독립인 문헌수 하한이다. 모든 A의 최초근거와 후속검색범위를 보존한다. 필수 표1~4를 RESULT 제목 바로 뒤에 두고 끝은정확히3개 약점행 표. SELF_CHECK·acceptance를 먼저 커밋하고 검사 후 HANDOFF를 마지막 별도커밋. 남은 조건은false로 두어 REVIEW_READY_WITH_GAPS/BLOCKED로 인계한다.

## 묶음 순서

1. 이 범위·표집·모집경로 동결과 원격 확인.
2. A F1/F2/F3 각8건과 원문원장을 별도커밋.
3. B 고유발견·중복·반례/타분야.
4. 시점/비용 재대조·표·SELF_CHECK·수용근거, 명령실행/해시/분모검사.
5. HANDOFF 마지막커밋 및 고정SHA 원격본문 재독.
