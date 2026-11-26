# 요청과 답변 · 연구 지형
(a) 문서·공개 기록, (b) 고정 입력 실행, (c) 실제 사용자(이 주제 0건). [추측]은 이 담당의 재분류다.

## 1. 확정 · 정정 · 열림
**확정**
- 전체 설계서는 필수가 아니다. 011: 공개 질문 61건 중 부분 질문이 33건이고, 그중 10건에 선택·채택 신호가 있었다(a)[011]. 012: 발췌는 전체보다 nDCG가 낮았다(.238 대 .343). 다만 목표를 좁힌 K02.1은 .365로 전체 입력의 .268보다 높았다(b)[012].
- 부분 입력에서 답을 가르는 것은 선택 객체의 위치와 소비 역할이다. 107: 단일 편집은 발생 위치로 6/6, 공유 정의로 0/6(b)[107]. 159: 같은 UI 문구 48자리를 소비자 역할 48/48, 직접 키 42/48로 갈랐고 틀린 키 38/48도 같은 문자열을 냈다(b)[159]. 119: 원요구만 0/6, 인접 레코드·직접 참조 각 3/6(b)[r49].
- 값 하나가 첫 절을 바꾼다. 074: 구성 4쌍에서 값을 받으면 8/8이 정답 하나로 좁혀졌다. 그중 음성 2쌍은 값이 무엇이든 공통 행동으로 충분했다(b)[r21][074]. 256: S1(H=I≠W)은 두 답이 같은 절이라 질문 이득이 0이다. S2·S3은 첫 절이 달라지고 잘못 고르면 B가 사라진다. 이는 시험 기대값이며 실행은 0회다[256]. 264: Pandoc 2.3의 toc-title은 인쇄 제목만 바꾸고 책갈피 4개는 그대로다. 2.2.3.2 기본 템플릿은 무시한다. pdfbookmark는 노드를 더하고 기존 노드를 9.035pt 옮긴다(PDF 16/16, b)[264].
- 이미 있는 값을 다시 묻기 쉽다. 026: 봉인 질문 24개 중 8개는 값이 원문에 있었고 새로 채운 값은 0/24였다(a)[026]. 074 자연 3건과 189의 두 제보도 목적이 본문에 명시돼 있었다[074][189].
- 요구–절 대응을 주면 근거 회수가 오른다(규칙 판독기 기준). 021의 두 절 예산에서 주소만 6/23, 절 목록 9/23, 대응 14/23이었다. 대응을 잘못 붙이면 8/23이었다(b)[021].
- 즉답·조건부·질문 형태 분포: 230은 2·2·0[230], 243은 3·1·0[243], 256은 2·0·1(미선택 1)[256].

**정정**
- 140의 질문 후보 4개 중 C4·Y2는 사용자 선호가 아니라 기술 조건이었다. 144에서 CLI 149회 실행으로 해소됐다(b)[144].
- 230의 매뉴얼 해석 '아래 트랙 제외'는 251의 실제 내보내기 8/16회, WAV 12/28개에서 뒤집혔다(b)[251].
- 243이 '강한 추정'으로 둔 #4856 인쇄 목차 경로는 2.3에서만 성립한다[264]. 판을 모르면 조건부로 답해야 한다.
- 074 PAN-N2의 '보존 의무' 추론은 철회됐다. 필드 의미를 잘못 정하면 '이미 있는 값' 집계부터 틀린다[074].
- 256: Git 2.23 블로그의 restore 기본값 설명은 2.45 매뉴얼과 다르다. 고정판이 기준이다[256].

**열림**
- 되묻기의 편익은 한 번도 측정되지 않았다. 026 발송 0[026]. 030 정보 질문→직접 답→권고 변경 A 8→3→0, B 7→6→0(a)[030]. 070 분모 0[r21]. 243 응답 0/4[243], 256 발송 0[256], 189 실험 0[189]. 근거는 판별력뿐이다.
- 최초판: 256은 3/4 복구, 선노출로 가림 유효 0/4. 230·243의 최초 revision 0/4.
- 조건부 두 링크와 질문을 사람에게 비교한 적이 없다. 249는 24명 설계만 있고 참가자는 0명이다[249].

## 2. 근거 수준
- (a) 011·026·030·189·197·208·219·230·243·256. 256의 상태표는 시험의 기대값이다. (b) 074·107·119·144·159·251·264. 021·112·116·124는 AI·규칙 판독이다.
- gallim[gal]의 입력 계약(whole/partial, 선택·제외 ID, 목적 범위, 이웃 간선, 미상)과 '확인 하나'는 (a)다. 이 담당이 fc68f0d에서 테스트 12개를 실행해 통과했다(b). `next_check`는 후보 간에 상태가 갈리는 요구 하나를 고른다. 질문·회수·실행 확인은 구분하지 않는다.

## 3. 제품 설계로의 함의
**입력.** 원문을 보존하고 목적의 원문 범위를 받는다. 조건마다 대상·부정·시점·강제성·명시 여부를 기록한다(001)[001]. 선택·제외 ID와 이웃 간선도 받는다. 판·환경·현재 상태는 Studio가 채우는 칸이다. 칸마다 출처(명시·Studio·추론·사후)와 시각을 붙인다(256 evidence stamp, 026 규칙 5). 148은 원요청·범위·판·보존 조건을 최소로 두고 연결된 생산·소비 증거를 선택 항목으로 제안했다. 효과는 미실험이다[148].

**결정 순서**(설계 제안, 판별력 수준): ① 두 해석의 고정판 첫 절이 같으면 진행한다. ② 다르면 환경·판·상태·파일은 Studio에서 회수하고, 문서·코드 사실은 실행으로 확인한다. ③ 저자의 의도나 수신 측 계약에 달려 있고 잘못 고르면 되돌릴 수 없으면 한 번 묻는다. 그 밖에는 조건부 두 링크를 준다. 074에서는 사용자가 자기 목적을 알면 두 링크도 같은 선택을 전달했다.

| 처리 | 원 사례 |
| --- | --- |
| Studio에서 회수 | 설치판: Pandoc 2.2.3.2와 2.3(264), Git 2.23 이전에는 restore 없음(256). 현재 상태: 256 #14075581의 "`git status` 출력은?"은 작업 트리를 읽으면 필요 없다[가정]. 발생·소비 위치(107·159·119). 실제 파일: 030 DB04 'null이 따옴표 안인가', 144 C4 날짜 열. [추측] 030에서 물은 변수 15개 중 약 11개가 판·환경·traceback 같은 사실이다. |
| 한 번 질문 | 256 S2 "디스크의 B를 남기나, 둘 다 HEAD로 버리나"(reset 경로 절 대 restore EXAMPLES, 잘못 고르면 B 손실). 197 '전체 선택'이 현재 면인지 서버의 필터 전체인지. 189는 목적이 빠졌을 때 "검색어를 남겨야 하나, 추가 검색만 없으면 되나". 208 #4862 '이번부터'의 범위. 219는 첫 설정을 바꾸는 미확인 축 하나. 144 Y3 CRLF 보존 대 LF 허용(수신 측 계약). |
| 그대로 진행 | 목적이 명시된 경우: 189 두 제보, 243 #449·#3555·#4519, 026의 8/24. 결과가 같은 경우: 256 S1, 074 음성 2쌍. 되돌릴 수 있는 두 갈래: 조건부 두 링크(243 #4856은 인쇄 목차면 toc-title, 탐색창이면 pdfbookmark에 264의 판 조건을 붙인다). 답을 받아도 조건이 남는 경우: 보류하고 조건을 명시한다(026 P02/P06). 사후에 생긴 요구는 새 개정판으로 기록하고 소급하지 않는다(026 규칙 5). |

**답 형식.** 첫 링크는 고정판의 절과 줄이다(예: git-reset v2.45.0 L23–31, Pandoc 2.3 MANUAL L1368–1370). 이유 한 줄에는 충족하는 조건과 보존·변경되는 것을 쓴다(256의 H/I/W). 아는 조건의 반복은 경로를 못 바꿨다(112·116 A=B). 새 위치 단서는 2/6에서 바꿨다. 시험 링크를 더한 뒤 핵심 수정은 0/6이었다(124)[r32]. 근거 수준(문서/실행/미확인)을 표시한다. 설명은 설득 수단이 아니다. 058 D04: 설명 강조로 맞는 권고 수락 908→1,107/1,395, 틀린 권고 수락도 123→152/205(a)[058].

## 4. 뒤집거나 단순화할 근거
1. 되묻기는 판별력만 입증됐고 필요성은 입증되지 않았다. 074가 직접 그렇게 결론 냈다[074].
2. "첫 절이 같으면 묻지 않는다"가 256 S1, 074 음성, 230·243을 설명한다.
3. 질문 후보의 상당수는 회수·실행할 일이다(144 2/4, 030 약 11/15[추측]). 남는 질문은 되돌릴 수 없는 의도 분기다.
4. 질문은 중립적이지 않다. 026 Census의 probe는 해석과 회상을 흔들었다[026]. 249는 질문이 힌트가 된다고 보고 동결 뒤에만 묻는다[249].
5. [추측] gallim `next_check`에 회수·검증·질문 채널 표시만 붙여도 사전 질문 단계 없이 충분할 수 있다[gal].

## 5. 다른 담당에 주는 사실
- DB: 칸마다 출처와 시각, 조건부 답의 분기 키, 질문 레코드(발송·답·값·시각)를 저장한다. 늦은 요구는 새 request_revision으로 넣는다(gallim 불변 트리거와 양립).
- 수집·검색: 첫 링크가 절·줄 단위이므로 고정판 앵커와 과거판 색인이 필요하다(256은 v1.6.0~2.45를 사용). URL만으로는 264의 두 판을 가를 수 없다.
- 운영: 판이 바뀌면 첫 절이 뒤집힌다(264 toc-title, 256 restore, 253 axe 4.7.2→4.8.0[r49]). 답에 판 가정을 저장하고 릴리스 사건마다 재검토한다.
- 평가: 질문을 실제로 보내는 조건이 있어야 편익을 잴 수 있다. '두 해석의 첫 절 일치율'은 미리 계산할 수 있다.
- 판단: 문서 즉답은 실행에서 뒤집힐 수 있다(251). 핵심 주장에는 실행 영수증이 필요하다.

[r49]: https://github.com/laadkke-arch/agentflow-open/blob/c8f4b5f106bf35994ad033846c221beae60c5012/docs/workstreams/planning/REVIEW-49.md
[r21]: https://github.com/laadkke-arch/agentflow-open/blob/c8f4b5f106bf35994ad033846c221beae60c5012/docs/workstreams/planning/REVIEW-21.md
[r32]: https://github.com/laadkke-arch/agentflow-open/blob/c8f4b5f106bf35994ad033846c221beae60c5012/docs/workstreams/planning/REVIEW-32.md
[001]: https://github.com/laadkke-arch/agentflow-open/blob/4d6208c08f6f2657865ba000d6768f6537e832b6/docs/workstreams/research/AF-RES-001/HANDOFF.md
[011]: https://github.com/laadkke-arch/agentflow-open/blob/478c301b693896e2c6d777f46ac441f071bfdfe8/docs/workstreams/research/AF-RES-011/HANDOFF.md
[012]: https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/RESULTS.md
[021]: https://github.com/laadkke-arch/agentflow-open/blob/29049a5f15b6ef7cd7431f59a059598db6f5d857/docs/workstreams/research/AF-RES-021/RESULT.md
[026]: https://github.com/laadkke-arch/agentflow-open/blob/c6eff012a74451e9882d8d43b6a6e510b4d15225/docs/workstreams/research/AF-RES-026/HANDOFF.md
[030]: https://github.com/laadkke-arch/agentflow-open/blob/3f77073d6294b739bb340b23e3c4c10640c5b08c/docs/workstreams/research/AF-RES-030/HANDOFF.md
[058]: https://github.com/laadkke-arch/agentflow-open/blob/fefeb2146c7f63e49d0578f78989be49acd63291/docs/workstreams/research/AF-RES-058/HANDOFF.md
[074]: https://github.com/laadkke-arch/agentflow-open/blob/34f3a5595fde1dd8f2fe1c7f2801c132f2fa2be9/docs/workstreams/research/AF-RES-074/RESULT.md
[107]: https://github.com/laadkke-arch/agentflow-open/blob/54fccba38c764032f9ecc5fac5a676a9e2a898f5/docs/workstreams/research/AF-RES-107/HANDOFF.md
[144]: https://github.com/laadkke-arch/agentflow-open/blob/92833407f665a6e28e4292491c261b7e0725c69c/docs/workstreams/research/AF-RES-144/decisions.csv
[148]: https://github.com/laadkke-arch/agentflow-open/blob/7afb5730cf9b17effa4413380da69e000e74e15d/docs/workstreams/research/AF-RES-148/HANDOFF.md
[159]: https://github.com/laadkke-arch/agentflow-open/blob/fd703cfc31dcdf424c5302f33d841d2d8e00f9be/docs/workstreams/research/AF-RES-159/HANDOFF.md
[189]: https://github.com/laadkke-arch/agentflow-open/blob/6fa4492e0e1a8c0510f573e914b4288786e0e694/docs/workstreams/research/AF-RES-189/HANDOFF.md
[230]: https://github.com/laadkke-arch/agentflow-open/blob/896b13e51f18738e60d63977e999c0aa25027057/docs/workstreams/research/AF-RES-230/HANDOFF.md
[243]: https://github.com/laadkke-arch/agentflow-open/blob/001d09da8b4f9cbb0d77fff2fc41acbc46fb5e41/docs/workstreams/research/AF-RES-243/first-pass.csv
[249]: https://github.com/laadkke-arch/agentflow-open/blob/a61cee2b8882e79226f383217440ab71f2637f8c/docs/workstreams/research/AF-RES-249/protocol.md
[251]: https://github.com/laadkke-arch/agentflow-open/blob/676545d3443eed407f7aa7e7d5b10024bdf0273c/docs/workstreams/research/AF-RES-251/HANDOFF.md
[256]: https://github.com/laadkke-arch/agentflow-open/blob/17a7d6f69d6516929005f09239543b1ac54968c1/docs/workstreams/research/AF-RES-256/RESULT.md
[264]: https://github.com/laadkke-arch/agentflow-open/blob/a46205ae9cf9330b10f591ffd323ac000e63dabc/docs/workstreams/research/AF-RES-264/RESULT.md
[gal]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/demo.py
