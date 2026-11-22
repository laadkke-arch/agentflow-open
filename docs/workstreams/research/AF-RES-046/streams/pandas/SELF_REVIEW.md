# pandas 자체 재판독

검토시점: 2026-11-22 UTC. 선정 원격 고정 SHA `994e21aaea7c5da0c4322db9d1ce2c4f52fa6a2f`; 묶음2 원격 SHA `03df204224d89d5c7d6c3976116fc0ff047f9865`. 후속 결말의 첫 의미 판독은 22:12:16.432Z. 선택 전 우발 노출은 selection.json/REVISIONS.md에 별도로 남아 있어 완전 가림을 주장하지 않는다.

| 질문 | 답과 직접 대조한 위치 | 반대 관측/탐색 | 판정을 뒤집을 최소 자료 |
|---|---|---|---|
| Q1 표본 | [Jan query](https://api.github.com/search/issues?q=repo%3Apandas-dev%2Fpandas%20is%3Apr%20created%3A2023-01-01..2023-01-31&sort=created&order=asc&per_page=40&page=1), [Feb–Mar query](https://api.github.com/search/issues?q=repo%3Apandas-dev%2Fpandas%20is%3Apr%20created%3A2023-02-01..2023-03-31&sort=created&order=asc&per_page=40&page=1)에서 각40. 자연 rank3/9/11/14, 추가 rank6/13. frame.csv80행과 selection.json | #51110은 실행 예제가 있어 문서만이라는 제외를 정정하고 reviewerURL0로 유지; #51114 두patch는 공백뿐. 마지막에는 '#번호' 자동링크도 첫13행 reviewer발언에서 별도확인, 앞선 missed eligible 없음 | 같은 순위의 초기 구체 코드와 더 이른 적격 reviewer링크 원문이 발견되면 선정오류를 표기. 이미 결과를 본 뒤 조용히 교체하지 않음 |
| Q2 링크전 선택 | baselines.csv6행, [51116 SHA8941b7e masked.py L1380–1460](https://github.com/pandas-dev/pandas/blob/8941b7ebe7a2c6377b41f0844d96bcc0508e3a80/pandas/core/arrays/masked.py#L1380-L1460), [review1345163916](https://github.com/pandas-dev/pandas/pull/51116#pullrequestreview-1345163916) 3/17 01:59가 firstlink전 판을 고정 | earliest surviving precreation SHA는6건 모두 exact first public head 증명이 아님. 현재 REST base/head도 originalreviewbase가 아님 | PR개설/최초push archive에 head SHA가 기록되면 원초기판 확인으로 승격 |
| Q3 링크/읽음 | [51109 firstlink1454740098](https://github.com/pandas-dev/pandas/pull/51109#issuecomment-1454740098), [author1454857966](https://github.com/pandas-dev/pandas/pull/51109#issuecomment-1454857966); [51116 firstlink1474263974](https://github.com/pandas-dev/pandas/pull/51116#issuecomment-1474263974), [author1474292973](https://github.com/pandas-dev/pandas/pull/51116#issuecomment-1474292973) | 구체 target engagement2/2와 literalread0/2 구분.51166의sameauthor2/4개설은 사전인지 근거이며 최초발견 주장 반증. 자연50539의링크는author발행 | 자료를 처음 읽었거나 이미 알았다는 당사자의 당시 명시 진술. 최초발견을 단순 감사/답변에서 추론하지 않음 |
| Q4 실제같은목적변경 | [f95152e](https://github.com/pandas-dev/pandas/commit/f95152e78c8baa2b1f4e07ecebb31496b3956c65) groupby.py/ops.py 제거/추가호출과 [fixed test_any_all.py](https://github.com/pandas-dev/pandas/blob/f95152e78c8baa2b1f4e07ecebb31496b3956c65/pandas/tests/groupby/test_any_all.py#L1-L220)를 대조. L-P2 sameauthor successor1/2 | selectedPRpostlinkcommit0이면서 다른PRactualchange존재. L-P1 target보정ce2bedb9는다른저자. natural50533 docs-only/50539 explanation-only과CoWtest분리 | 응답이 target정보 때문에 새결정을 했음을 명시하고 해당후속patch/검사가 연결되면 엄격사슬 재검토. 삭제된sameauthor패치가복원되면L-P1 재판정 |
| Q5 사람노동 | labor.csv6행; [51109 benchmark1483371816](https://github.com/pandas-dev/pandas/pull/51109#issuecomment-1483371816)의 seconds는runtime. 생성→종결elapsed는190845/183166/74507/3296091/5951295/4039399초 | directworklog0, selfreportedworkduration0, pairedquality-humantime0. 숫자없음은 노동0이 아님. CI/주말을 비작업시간으로 자동환산하지 않음 | actor별 능동작업 시작/중지와 요구·품질을 맞춘 무링크 시간쌍. 이 없이는 savings 미확인 |
| Q6 경쟁설명 | [52043 opening](https://github.com/pandas-dev/pandas/pull/52043)3/17 03:36, [52053 opening](https://github.com/pandas-dev/pandas/pull/52053)16:00는firstlink18:45앞. [fecddcf8](https://github.com/pandas-dev/pandas/commit/fecddcf8ae8bb9d825410904ad40f3b7af31fa56)는phofl도움으로시험보정 | 실패시험,이미착수한통합,타인구현,reference후첨,author가reviewer교정,원설계유지 반례를 모두 보존. 날짜순서만 인과주장 못함 | 이전작업과link가추가로바꾼결정의경계를당시push/작성자결정기록으로분리 |
| Q7 주장수준 | cases.json6개 및 sensitivity.csv18행. natural reviewerlink0/4; link층2/2, semanticengagement2/2, sameauthorpostlink1/2, strict0/2, directlabor/selfreport/pairedtime 각각0/2관측 | 30일은링크0/2여도슬롯유지. 링크전착수L-P2제거하면sameauthorpostlink0/1. 타인대안구현까지포함하면관련코드공표2/2가능하나 strict증가는없음 | 읽음·새결정·동일목적patch·대응검사 및 사람시간의 부족한 고리를 원문으로 메워야 함 |

## 원장 검산

verification.json은 실제 Python CSV/JSON 파싱 결과다. 80 frame,6baseline,128event,23change,6labor,6case,18sensitivity,163source receipt를 대조했다. 최소수에 세는 독립 저작17개는 PR원제안4/review4/commit-test7/link-target2이며 중복 work_id0. events/changes/cases의 미해결source_id0. 이 검사는 연구 원장 일관성 검사이며 historical pandas 테스트 실행 결과가 아니다.

최소수에 세지 않은 검색결과·일부선별·같은저작재방문·oversizedmerge 잘린응답도 기록했다. 추가 영수증2개는 additional-sources.jsonl에 두며 sources.jsonl의 묶음2 원격판을 덮지 않았다. 합산할 때 두 파일을 함께 읽고 work_id로 중복 확인한다.

## 해석과 실행의 한계

GitHub PR/리뷰/commit/고정file 원문을 읽었다. pandas의 당시 환경을 설치하거나 pytest를 실행하지 않았으며 historicalCI완료·배포·실제사용으로 승격하지 않는다. 원자료의 시험 입력/기대값과 병합 SHA를 근거로만 기술했다.

같은 AI가 초안과 반례를 재판독했고 root가 통합 검산했다. 외부 독립 인간 판독은 수행하지 않았다. 처음부터의무와달리정정한 추가층R01의 원규칙·이유·영향행을 보존했고, 성공 결과에 맞춰 슬롯을 바꾸지 않았다.

## 다음 첫 행동

원장 집계자는 cases.json의 `same_author_change.after_first_link_across_PR`과 `after_first_review_runtime`을 혼동하지 않는다. natural의 앞 필드는 null/해당없음이다. L-P2의 실제후속변경을 남긴 채 `linked_change_already_started_prelink`를 필터해 감도를 계산한다. 이후 exactfirstpublichead 또는 사람노동에 추가 증거를 원할 때 해당 질문의 최소자료를 확보한다. 추가자료 없이시간절감값을산출하는것은재개행동이아니다.

