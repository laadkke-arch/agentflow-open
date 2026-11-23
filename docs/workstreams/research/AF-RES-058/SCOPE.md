# AF-RES-058 — 모집·채점 규칙 (R0, 결과 열람 전)

작성 UTC: 2026-11-23T03:18:00Z. 실제 최초 시작판 `3f4d43b19cd76d56983e6f500eebe7010eb3fa51`. 계획의 `8036b862...`와 구별한다. 지정 의존 인계 `425f64dda404b4e275acf4eae5ff9244eab36d37`, 결과 `377facae73f5e49677cb5719a05fdac457d8357b`를 읽었다. 저장소 입력은 외부 저작 수에 넣지 않는다. 모든 편집과 일시 취득물은 이 소유 경로 안에 둔다. 공통 파일, dot-control.json, main, 다른 작업 브랜치를 변경하지 않는다.

## 1. 질문·예산·노출

2015-01-01–2025-12-31 공개 사람 실험. A층은 개발 도구/API/코드 예제/검색 결과의 적합성 선택, B층은 문서 분류/사실 판별/추천 의사결정. 각 층 네 자리(A01–A04, B01–B04), 각 층 최대 30개 고유 DOI를 방법 기준으로 순서대로 검토한다. 같은 논문의 다중 실험은 한 자리, 같은 코호트 재분석은 독립 실험으로 더하지 않는다. 빈 A자리에 B를 넣지 않는다. 모집 전에 열린 외부 결과표는 없다. 모델의 사전학습 지식은 무지 상태로 만들 수 없으며, 후속 검색 초록/제목의 결과 노출을 별도 기록한다. AF-054의 결손과 저자 집계는 출발 사실로만 인수한다.

목표 외부 1차 저작: 사람 실험 원논문 8, 별도 발행된 자극/도구/프로토콜 4, 별도 데이터/분석 패키지 4, 독립 반대/복제/다른 분야 실험 4. 동일 논문+부록은 한 저작, 패키지 README/CSV/노트북은 한 저작. 패키지를 자극과 분석으로 두 번 세지 않는다. 자극/분석이 한 패키지이면 분석 패키지로 우선 분류한다. 별도 실험 도구 저장소는 별도 배포·출처·버전이 확인될 때만 별도 저작이다. 정답 데이터셋과 척도 원논문은 보조 저작이며 목표 군 충족과 총수를 따로 보고한다. 확보 실패는 총수로 덮지 않는다.

## 2. 고정 모집 경로와 정확한 질의

실행 UTC, 요청 URL, 응답 상태, 원 순번, 반환 metadata를 각 stream의 search-log.jsonl/metadata.json에 기록한다. 모든 검색은 공개 자료 읽기만 하며 유료 API, 로그인, 저자 연락, 새 참가자 모집은 없다.

### Crossref 발견 API

`https://api.crossref.org/works`의 `query.bibliographic`에 아래 문자열을 각각 그대로 넣는다. 공통 매개변수는 `filter=from-pub-date:2015-01-01,until-pub-date:2025-12-31,type:proceedings-article`, `sort=published`, `order=asc`, `rows=100`, `offset=0`; 질의당 1페이지. 서버의 검색은 Boolean AND 보장이 없으므로 metadata 후처리와 native 목록으로 확인한다. 결과 전문/결과표는 아직 열지 않는다.

| 층 | query.bibliographic 값 |
| --- | --- |
| A | explanation search result relevance decision |
| A | rationale code recommendation user selection |
| A | evidence API recommendation decision |
| A | citation search result acceptance |
| B | explanation advice reliance decision |
| B | rationale classification human decision |
| B | evidence fact checking recommendation |
| B | explanation recommendation acceptance |

### ACM Digital Library와 ACL Anthology 공식 목록

ACM native `https://dl.acm.org/action/doSearch?AllField=...`에 A: `(explanation OR rationale OR evidence OR citation) AND ("search result" OR API OR code) AND (accept OR reliance OR decision OR selection)`, B: `(explanation OR rationale OR evidence OR citation) AND (recommendation OR advice OR classification OR "fact checking") AND (accept OR reliance OR decision)`를 사용한다. 연도 2015–2025, CHI/IUI/SIGIR 정식 proceedings만. publication date 오름차순, pageSize=50, startPage=0 한 페이지. 실제 UI/API가 이 문법/정렬을 허용하지 않으면 실패를 기록하고 동등하다고 주장하지 않는다.

ACL 공식 검색 `https://aclanthology.org/search/?q=...`에 A: `explanation search decision`, `rationale code recommendation`; B: `explanation human decision`, `evidence fact checking`를 각각 사용한다. 한 질의 첫 50결과까지, native 순서 그대로 보존하고 2015–2025 정식 Anthology 논문과 DOI를 metadata로 확인한다.

Native 접근/문법이 막힌 경우 사전 지정 fallback: web search에서 `site:dl.acm.org/doi <동일 층의 Crossref 질의>` 및 `site:aclanthology.org <동일 층의 Crossref 질의>`, 질의당 첫 10 반환 항목만 사용한다. 엔진은 system2; 결과 부족/공식 출처 검증은 system1로 같은 질의를 한 번 더. 순서는 엔진 순서로 원장 보존. fallback은 native 전수검색의 대체가 아니며 모집 재현 한계로 보고한다. DOI/공식 proceedings 목록을 확인해야 모집 pool에 들어간다.

### 중복·정렬·선정

DOI는 https://doi.org/ 및 doi: 접두부 제거, 소문자, trailing punctuation 제거. 같은 DOI 미러/저자판은 한 후보. 공식 metadata의 최초 publication date(online 우선, 없으면 print)를 YYYY-MM-DD로 기록하며 월/일 미상은 그 정밀도와 01 보간 정렬키를 함께 남긴다. 각 층 발견 pool에서 연도·venue·주제 관련성의 metadata 선별을 한 뒤 발행일, DOI 사전순으로 정렬하고 처음 30 DOI까지 방법을 읽는다. 방법 읽기 전 pool을 파일로 동결한다. 공식 DOI 없는 관련 논문은 진단층에 보존하고 DOI 30개에 끼워 넣지 않는다.

방법 적격: 실제 사람이 최종 선택/응답하고, 같은 항목의 후보/권고에 설명 유무를 대조할 의도가 방법에 존재한다. 정답표 유무, 결과 방향, 공개 데이터 성공은 선정 기준이 아니다. 순서상 처음 네 적격 후보를 슬롯에 고정한다. 이후 자극 감사에서 후보/순위/모델/신뢰도/시간이 함께 바뀌거나 자발적 열람뿐임을 알게 되면 슬롯 유지·등급 하향한다. 결과를 본 뒤 더 좋은 연구로 교체하지 않는다. 날짜순 전 세계 최초 네 연구라는 주장은 하지 않는다.

사전 키워드 누락 점검: 선정 논문의 backward/forward 인용과 저자 페이지에서 최대 12개 추가 논문, 최대 12개 패키지. D01 등의 진단 ID를 사용하며 primary 8자리를 바꾸지 않는다. venue 밖 독립 실험은 이 진단층에서만 비교한다. metadata·방법 판독 중 우연히 보인 초록/결과를 exposure 필드로 남긴다.

## 3. Q1–Q7 채점과 금지된 추정

- 동일성 E1: 항목 ID+조건 자극/스크립트로 권고·후보·순위 동일 확인. E2: 방법 문장만 동일 명시. EU: 미확인. 같은 모델이라는 이유만으로 E1 아님.
- 개입: 이유문장, 원문 발췌, 링크/앵커, 확률, 예제, 강조, 강제/선택 열람을 분리. 실제 원문 읽기 배정과 설명 제공 배정 구분. 클릭 없으면 읽음 미확인.
- 정답: 사전 키/기능 제약/전문가 rubric/데이터 라벨 출처·판·단위 확인. 취향, 설명만 오류, 높은 자신감은 오권고와 별도. 사후 다수결·복수 정답은 별도.
- 원행 연결: 배정표를 기준으로 사람×항목×조건×기간 키 유일성, 1:N 이벤트 집계, 정답·권고·최종 선택 왼쪽 결합. 공유키 없는 정렬 목록 연결 금지. 도움 전 답과 권고 일치/변경 분리.
- J1: 직접 연결한 공개 원행; J2: 저자 명시 교차 집계; J3: 주변수/그림 비율뿐; J4: 원 종점 부재; JU: 자료 미확인. 실제 읽은 범위만 등급 부여.
- 정오층별 분모 D: 판정 가능한 권고 시행. 수락 A: 최종 선택=권고. 최종 정답 C: 최종 선택=정답. 오권고 거절 후 제3의 오답은 A=0,C=0. binary일 때만 오권고 거절과 정답이 일치. 건너뜀/철회/미응답/미연결은 별도. 합의 답과 권고를 보고 바꾼 답을 섞지 않는다.
- 조건차: 같은 정의·분모의 개입 A/D − 대조 A/D, 정오층 각각. 사람배정 연구의 반복 시행을 독립 사람 수로 세지 않는다. inferential test와 새 신뢰구간은 필수 아님; 시행 비율은 기술량이며 사람 군집을 무시한 유의성을 주장하지 않는다.
- 백분율/반올림 평균에서 정수 역산 금지. 결측 m과 판정가능 D가 확실할 때만 (A)/(D+m)–(A+m)/(D+m) 같은 명시 가정별 범위. 권고 정오 자체가 미확인인 결측에는 정오층 m을 임의 할당하지 않는다.
- 주변수만으로 부호 비식별을 보이는 두 구성 집계표는 '진단 가상'으로 표시. AF-054의 6200조합/시간 계산 재실행 금지. 연구 간 정답 비중·모집단 다른 수치를 합산하지 않는다.

## 4. 단계와 검토

① 이 규칙+manifest를 원격 커밋 → 방법 기반 선정 동결(필요 시 ①a) → ② 조건 동등성·자극·정답 원천 → ③ 응답 연결·교차 집계·반증 → ④ 필수 두 표·자체 검토 → 고정판 재열람·session check → HANDOFF만 마지막 단독 커밋. 결과를 본 뒤 규칙 변경은 시각·이유·노출·주분석/감도로 명시한다.

독립 조사 stream은 A, B, 진단/반증으로 나눈다. 한 명 root가 공통 원장·표를 통합한다. assistant 간 검토는 실제 읽은 파일과 원문 범위를 기록하며 독립 인간 심사나 독립 참가자 복제로 부르지 않는다. 최소 한 공개 저자 집계를 분모부터 손검산하고, 자동 검산은 그 구체적 위험과 파일 연결만 확인한다.

최종 수용: 20저작 총수, 각 배당, 8자리 충원, 원래 정오별 분자/분모, 실제 자극·동일성, Q별 반증을 각각 판정한다. 저장/계약 통과와 연구 완전성은 별개. 부족하면 PARTIAL과 최소 재개 입력을 남긴다.

## R1 — 결과표 열람 전 발견 정렬 보정

2026-11-23T03:23Z. A/B 조사자가 각각 원문 결과표 미열람·미선정 상태임을 보고했다. R0 Crossref `sort=published,order=asc`는 broad soft-match에서 대부분 무관한2015년 결과로100칸을 채웠다(A 2질의200/2질의429; B3질의200/1질의429). Native ACM403, ACL은 JS shell 또는 추출 실패였고, fallback의 스니펫 노출은 있었다. 이를 빈 분야의 증거로 삼지 않는다.

**변경:** 동일8개 Crossref 질의·날짜/type filter·페이지 예산을 `sort=score,order=desc,rows=100,offset=0`으로 한 차례 더 실행한다. 요청은 각 조사 stream 내 순차로 수행하고429일 때 같은 URL 한 번만 재시도한다. 발견 metadata의 합집합을 기존 중복/venue/주제 선별 후 **발행일·DOI 순**으로 정렬하여 각 층 최대30 DOI의 방법 검토를 한다. 이 변경은 metadata 발견의 정렬만이며 선정 기준·종점·배당을 바꾸지 않는다. R0/R1 원시 목록은 별도 보존한다. 날짜순 검토와 score순 발견을 구별한다. 후속 결과 접근 전에 pool/선정을 별도 커밋한다.

노출: root는054 인수와 검색 실패보고를 읽었으며 새 외부 실험 결과표를 읽지 않았다. A에는SIGIR2020 Measuring Recommendation Explanation Quality 등의 제목/스니펫, B에는관련성 낮은CSUR/CSCW 스니펫이 보였다. 각 검색 원장에 개별 노출을 남긴다. 진단 조사자는 사전지식에서 출발한 논문을 별도층으로 읽고 있으며 primary선정의 효과 방향 기준으로 쓰지 않는다.
