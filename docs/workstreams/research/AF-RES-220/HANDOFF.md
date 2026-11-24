# AF-RES-220 HANDOFF — PARTIAL

- 결과판 SHA: 7364e529addc20042f45ca68b7012e6ffa1b1988. 브랜치 work/research-af-res-220. 착수 f3895893e32e2c055cefde446d34f1467fa27b4c; 계획 fc095c323d0177401d34f1daa7b4d1c529e2351f 대비 5 commits ahead, control만 변경. 최신 blob에서 실제 배정 및 209 의존 확인. 의존 result 187cb91aa385ac7c403749e82d9646ffb1ebd135 (중앙 DONE, 자체 PARTIAL), 216–218 제외.
- 결과 요약: GitHub REST 실제 개별 응답 8/8, positions 21/40 + 정상 비어 있음19 + 미관측0, incomplete0, 정상 raw 빈 배열0. 외부 후보 있음4/8, 외부 없음4/8(only self). 자기 원1위5/8, 배열에 포함7/8. 4쌍×2 분모 모두 관측. 부분 관련성 포함 시 원1위 B 개선1/동률3/악화0/U0, 자기 제외 개선0/동률4/악화0/U0. 실제 해결 조작만 보면 양쪽 모두 개선0/동률4. #12856 개선은 자기 정확 재현 확인일 뿐 해결 아니며, 좁은 partial 기준은 raw U1/동률3. #11583 자기 rank5→2이나 첫 도착은 JSON timestamp→TSV ID 보존으로 바뀌어 DATE 해결 없음.
- 대표 파일: RESULT.md(필수 2표, Q1–7, 마지막 약점 3건), queries.csv, receipts/INDEX.json 및 raw 8개, paths.csv, pairs.csv, SCOPE.md, sources.jsonl, COUNTEREXAMPLES.md, DUPLICATE_SCREEN.md, SELF_CHECK.md. 자료 42 ledger rows, 39 counted unique works/18 lineages(원4/GitHub4/소비자·패치20/제작자·규격6/발행자5), 사건 계보10·지명4. P05 페이지 이미지 실패 보수적 제외 시 38, 발행자4. 직접 하한 충족. 영수증 자료수 제외.
- 결론 한계: 같은 공개 GitHub 연결을 사용했지만 실제 API version/HTTP header 비노출, 원문 초기 revision 전체 미확인, 비가림. #15376 original TSV SHA와 최종 VARCHAR schema 및 오류 행번호 불일치, #12856 patch/실행 확인 없음. PDF P05 본문 추출 확인했으나 screenshot 실패. 원자료별 일부 UTC는 정확한 개별 시각 아닌 읽기 시간창. 이에 protocol PARTIAL, 순위 측정 자체는 완료. 이전 stage2 P01/UTC 원장 정정은 stage4에 보존. 독립 검토 및 새 소프트웨어 실행 없음.

## 묶음과 결과판 재열람
1. ac14b425d6bda727bdc24606321b1798f0a0a56c — SCOPE/queries 사전 동결.
2. 07ab63018275e6794685540de61e8bed96c6c001 — 제공자 raw 및 초기 원장.
3. 274a4692fdc6f846a6422298c71bb2779e4e711f — 주관측·필수 표·경로·쌍·duplicate.
4. 61576d73a239f5371639a8bc576c5875a45b1fed — 반례·정정·추가 원장.
5. 7364e529addc20042f45ca68b7012e6ffa1b1988 — RESULT/SELF_CHECK.
6. 이 HANDOFF 단독 마지막 commit (자기 SHA는 commit 이후 ref에서 확인).

결과판 SHA로 11개 문서/CSV/원장/INDEX와 8개 raw JSON을 다시 읽었다. 8/8 query URL=INDEX, raw total/incomplete=INDEX, raw items 순서=INDEX=paths; 40행/21 item/19 absent 및 4 pairs, 39 work/18 lineages 재계수 일치. RESULT 첫 표와 Q1–Q7, 마지막 3건 확인. base→result compare ahead5/behind0, 변경 19개 모두 owned_path 아래. 자체 구조 대조만 수행, 외부 재실행·독립 평가 아님. 209나 다른 작업 경로, dot-control, main 미변경.

## 다음 첫 행동 (정확한 입력과 검증)
우선 고정판의 receipts 및 queries.csv를 읽고 과거 검색 순위를 바꾸지 말 것. GitHub API 버전 헤더를 고정할 수 있는 허용된 공개 호출 환경에서 **별도 반복**으로 아래 GET 수행. 인증 헤더는 보존하지 말고 UTC before/after, HTTP status, selected API version header와 raw JSON만 저장. 동일 공개 연결로 순차 8회, rate limit 준수. 원순위가 달라져도 이 결과를 덮어쓰지 않는다. 현재 세션은 connector 외 HTTP 헤더/버전을 강제할 수 없었다.

```sh
git fetch origin work/research-af-res-220
git show 7364e529addc20042f45ca68b7012e6ffa1b1988:docs/workstreams/research/AF-RES-220/queries.csv
git show 7364e529addc20042f45ca68b7012e6ffa1b1988:docs/workstreams/research/AF-RES-220/receipts/INDEX.json
git diff --name-only f3895893e32e2c055cefde446d34f1467fa27b4c 7364e529addc20042f45ca68b7012e6ffa1b1988
curl -sS -D response-01.headers -H 'Accept: application/vnd.github+json' \
  -H 'X-GitHub-Api-Version: 2022-11-28' --get \
  --data-urlencode 'q=ignore leading zeros repo:duckdb/duckdb is:issue in:title,body created:<2025-01-01' \
  --data 'per_page=5' --data 'page=1' \
  'https://api.github.com/search/issues' > response-01.json
```

나머지 q는 동결 queries.csv 2–8 순서/원문 그대로. 실제 선택 API version 확인; 2022-11-28은 다음 실험의 명시 선택이며 이번 응답의 확인된 버전 아님. 공개 편집 이력은 각 issue의 edited history가 실제 제공되는지 직접 확인, revision id/원문/UTC 보존. 현재 body만 가능하면 그 상태 표시.

별도 Codex 검증(설치/실행 승인된 환경에서만; 이 조사에서는 미실행):
- #11411 v0.9.2 Python: fips.csv 내용 헤더 fips, 데이터 01,12. default read_csv_auto vs read_csv(types={'fips':'INTEGER'}) 및 VARCHAR 후 cast. DESCRIBE, 원값, 결과값, 출력형, CLI/패키지 버전 기록. 예상 default VARCHAR, 명시 변환 1/12; 다른 판이면 구분. 고정폭 발행코드가 목적일 때는 01을 유지하는 대조.
- #11583 v0.10.2-dev504 2e6f74803b 및 v1.0.1-dev4803 c84676023c: 원 8개 quoted dates는 O02 body(03-11583-B/04-11583-A raw items 중 #11583)에서 그대로 회수. SELECT * FROM read_csv('dates.csv', dateformat='%b %-d, %Y'); 명시 columns DATE와 strptime::DATE 대조. DESCRIBE, 8행 값 비교. C06은 성공 보고; 실제 CSV fix commit은 c84676023c 자체가 아니므로 history 추적.
- #15376 1.1.3: g_patent.tsv 원문 링크의 동일 데이터 판과 SHA를 먼저 확인. 합성 대조 TSV 헤더 patent_id + 다른 열, 20,480보다 큰 수치 quoted 행, 마지막 D1000263, 별도로 전부 quoted numeric. default CTAS, sample_size=-1 CTAS, types={'patent_id':'VARCHAR'} CTAS; 각 DESCRIBE, count, D1000263/leading zeros 및 오류 기록. LIMIT100 성공을 전체 성공으로 보지 말 것. uncompressed/seekable 여부와 actual sample 선택 기록. dev2261 quote 오류 fixture를 별도 재현하고 C08/O03 두 행번호 충돌 확인. 판정 반전: -1에서도 오류/BIGINT이면 권고 축소; 실제 VARCHAR·값 보존이면 해당 양쪽 등급2 가능.
- #12856 v1.0.1-dev2164: pipe CSV header text|number, 반복 abc|123,000의 2047 및 2048 data rows(헤더 제외). O04 원 SQL/fixture 그대로, 추가로 SELECT * FROM read_csv('test.csv', delim='|', decimal_separator=','); DESCRIBE/SUMMARIZE, explicit DOUBLE 대조. 실제 row count, build SHA, 같은 값·형 확인. Fix commit/회귀 테스트 찾아 버전별 2047/2048 비교. #17093의 quoted 100,000.00은 다른 문법의 대조. 첫 답의 순위·적합성 판정은 원시 영수증의 관측으로 고정한다.

## 색인 반영 제안 (통합자용, 직접 변경하지 않음)
AF-RES-220 — CSV lexical preservation vs typed conversion; single GitHub REST A/B 4 cases/8 requests, 21 returned+19 normal absent; self-excluded first answer improvement 0/4; self-included partial relevance 1/4, strict solution 0/4. 39 works, PARTIAL(API version/revision and execution uncertainties). Refer fixed result SHA and this HANDOFF. 209의 provider-order 결손에 대한 직접 순위 계측 대안이나 전체 검색 품질 결론 아님.
