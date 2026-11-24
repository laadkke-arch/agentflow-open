# AF-RES-243 SELF_CHECK
자체 판정: **PARTIAL**. 원자료 하한, 네 현행 본문 사전 판정과 별도 후속 열람, 결과 파일 및 EPUB 두 예제의 원파일 구조 대조는 충족. 최초 revision, 실제 질문 응답, 역사 정확 템플릿/패키지 및 출력 관측 결측을 완료로 바꾸지 않는다. 독립 검토 0, binary/repeated measurement 0; 아래는 자체 읽기/구조 점검.

## Q별 대조 및 반증
| Q | 원근거 ID (sources.jsonl) | 반증을 찾은 곳·판정 변경 조건 | 예정/관측/결측 |
|---|---|---|---|
| Q1 | I449 I3555 I4519 I4856 ISO | #4856 toc-title을 outline 이름으로 요구했을 가능성, PR diff P4853는 A에 부합하지만 원글 수정 가능성. #449 명시 sidebar; X7731 'TOC'만으로 불충분 | 원글 현행 4/4, 최초 0/4, exact engine 0/4 원글(LaTeX 추정/후속 확인 별도), #4519 exact Pandoc 판 1/4 |
| Q2 | Mcur M119 M223 Hcur H18 W119 T23 P449 | X639855 X529058는 printed TOC 불필요; X194720은 printed TOC 링크가 목표. H18 §5.23에서 같은 tocdepth 경로일 수 있음. B 첫 목적지의 #449 정정은 출력층 유지, code route 변경 | 4/4 사전 선택, 4/4 A/B 경로, 실제 질문 0/4, 효율 eligible 0 |
| Q3 | M119 W119 T213 T223 T23 P449 H18 HP99 Hcur Bpkg ISO G119 | H18 §9.1.38 titlesec 비호환; §5.23 shared/override depth; Bpkg 1회 가능성. G119 submodule 발견, gitlink 미확인. 현재판 소급하지 않음 | 당시 코드 patch 1, later reported T213 1; initial template 1.19.2.1 0/1; exact package pin 0/4; runtime 0 |
| Q4 | I3555 C3555 W119 SH119 W223 H18 I4856 P4853 M223 T223 T23 CH23 X7731 | raw TeX vs Markdown 비교, 일반 math/LaTeX logo 대비; CH23 reader fix는 writer fix 아님. class가 contentsname을 bookmark에도 쓰는 조건은 시험 필요. Z7731 image 실패 | 2/2 제목 사례 원문+코드 비교, 0/2 three-layer actual PDF; #7731 screenshot 0/1 |
| Q5 | C449 C3555 C4519 C4856 P449 P4853 CH23 X57284 H18 | #449 hickford thanks only, pkaramol 별도 사람. #4519 bookmark after titlesec, custom template loading order; last heading removed. #4856 PR 생성일 이슈 이전 | 댓글 목록 4/4; 동일인 댓글 3/4, 실질 2/4; 유지2/반전0/미확인2; 실제 retest 파일 0/4; 정확 댓글 UTC 일부 null |
| Q6 | E33 E33S ECOP ECNAV EPOP EPNAV ESOP ESNAV | Page Blanche nav manifest에는 있고 spine에는 없음; CC 반대, SVG 보강. §5.7.2 nav spine optional. 다른 페이지에 별도 목차 그림 여부 미검사 | 두 필수 EPUB 2/2 nav+OPF, 보강1쌍; reader 0/3; 제출 provenance 0/2 beyond repo/metadata |
| Q7 | first-pass I449 I3555 I4519 I4856 X639855 X529058 X194720 X33696 H18 X7731 | 위치 명시 3건 반복 질문 비용; A 강한 추정 4856; strict print-only no outline 실제 사례 미확인, synthetic control 제안; same depth route 공통; engine ambiguity | 정책 모의 비교 4/4; 실제 시간 0, 질문 답 0, eligible 0/4 |

예정 21 distinct works, 실제 30: named4 other7 Pandoc7 PDF5 EPUB7. 51행 중 성공 41, 실패 10, 성공 중 중복/같은 원저작/댓글 11 미산입. 20 포함 lineage ID. 별도 사건 시작 10 (지명4+다른 요청6); 같은 이슈 후발 별도 작성자 1 추가. PR/patch/판/댓글을 독립 사건으로 세지 않음. 자료 count를 검정 표본 수로 바꾸지 않는다. 판이 없는 곳은 미확인, 실제 질문 0은 관측한 0, #7731과 EPUB는 지명 4사건 판정률 적용 대상 밖.

## 구조 및 봉인 검사
- 범위 커밋 a19452869e226020dbdce15195e04858e2a40d2e; 사전 판정 커밋 95d6946fc000f32312b92015dfd4dd506c7074e8. 원문 title/body/date만 읽고 4행 저장한 뒤 comments/PR 읽음. #4856 원글에 PR 존재 선노출 명시. 첫 링크 후보와 사후 절 보강을 구별. RESULT의 첫 표는 4 데이터행 5열; 둘째 표는 3 데이터행 5열; 끝 약점 표 3행 4열. Q1~Q7 제목 각각 1개.
- 중간 결과 c341ea66388198653428cf992b0eae41fb4af175에서 SCOPE/first-pass/sources/formats/followup/COUNTEREXAMPLES/RESULT 일곱 파일을 GitHub connector로 다시 읽음. first-pass blob f51aef0964ff50018a8d774af7d6327f41322e93, sources blob cc9f82f664a3639f3250f89ec70f0ccc4d22f9da, RESULT blob 1764b2dda663c72e468117f5caf836ecb690e42f. JS JSON parse 51/51, 필수 키 누락 0, source_id 중복 0; CSV 인용 셀 매칭 first-pass 5줄×12열, formats 18줄×8열, followup 18줄×9열(각 헤더 포함). RESULT 세 필수 헤더 일치, Q1~Q7 존재, 끝 약점 3행 각 4열. URL 원장 및 서술의 ID/URL·위치 수동 대조; 링크의 모든 영구 유효성/리디렉션 재검사는 하지 않음.
- base d1353701530ffd4c68587276c15d988d2cc92972 대비 위 중간 결과 ahead 9, behind 0, changed 7/7 소유경로. 중앙 진행표/통합 변경 없음. 이 점검 파일 commit 후 고정 결과에서 다시 읽고 HANDOFF만 별도 최종 commit 예정(작업 순서 표기, 실행 결과 주장은 최종 HANDOFF에만).
- 실패/미확인: 1.19.2.1 default.latex submodule gitlink SHA 미확인 (G119, Z119a–f), 정확 2012/2017/2018 hyperref install 판 및 class 없음, #7731 이미지 실패, ISO screenshot 실패이나 text 열람, 3.9 release web 실패로 one-pass 현재 Pandoc 주장 제외. H18 September 2018은 사건보다 늦은 비교 자료. 230의 결측은 그대로 유지하며 238–242 자료 미사용.
- runtime 검증은 HANDOFF의 재현 절차 참조. 실제 binary 설치·실행, PDF inspection, 독립 검토는 수행하지 않았음. 일반화·인과·시간 효율 확정 금지.
