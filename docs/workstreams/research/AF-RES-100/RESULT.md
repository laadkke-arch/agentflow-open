# AF-RES-100 결과 — 파일 전체와 제한 발췌의 문서 근거 가용성

## 1. 모집·의도 표

| 사례·질문 ID / 최초 revision | 원 필수 결과·수단 / 인접 경계 | 사용자판 / 연구판 | 누락·제외·재게시 | 사전 판정 기준·원문 구간 |
|---|---|---|---|---|
| J1 [79694539](https://stackoverflow.com/revisions/770D470B-094C-44A8-8293-5EB88893F4A1/view-source) · control · 태그순위 1 | 두 파일 JOIN/INDEX의 break 오류에서 중간값·입력 소비를 관측하는 다음 진단 절차<br>jq 내부 진단; 대조. 외부 블로그는 설명 출처이며 실행 경계 아님 | jq=미확인<br>연구: jq1.7.1 | jq 실제판·두 전체 원 파일·정확한 최종 JOIN 기대값 없음. 재게시 선언 없음; 사건 독립성 미확인 | C1: 원 호출에 적용할 관측 가능한 debug/input 위치를 문서로 지지. 최종 JOIN 복구는 별도 민감도<br>R0 HTML C1 U[668,790),[834,897),[1773,2740) |
| J2 [79699191](https://stackoverflow.com/revisions/77962A23-F898-4295-99B6-0CD81D12DEAF/view-source) · boundary · 태그순위 2 | 각 Event의 Data를 Name→content 사전으로 바꾸고 content 결손에서도 실패하지 않기<br>evtx_dump→sed→yq→sed→jq; 바로 앞 sed를 선택. 단순 전달자가 아닌 문자열 치환 | jq=미확인; sed=구현·판 미확인; yq=명령 형태는 -p xml -o json; 판 미확인; evtx_dump.py=발행자·판 미확인; bash=판 미확인<br>연구: jq1.7.1; 4.9 | 전체 Event envelope·원 evtx/XML·정확한 jq/yq/sed 판 없음. TRUE 추정은 금지; 사건 독립성 미확인 | C1: 같은 Event의 이름과 값 결합. C2: 결손 null 명시. 주 해석은 원문 .Event[] 경계에 조건부<br>R0 HTML C1 U[601,2345),[2346,3065); C2 U[2346,3065) |
| J3 [79711268](https://stackoverflow.com/revisions/C0FE71BE-B69D-428D-A53F-E976CBA5F209/view-source) · boundary · 태그순위 4 | Bash JSON 내용 변수를 jq --argjson으로 넘겨 schemes에 추가하고 나머지 설정·.new 출력 보존<br>최초 본문 순서의 출력 소비자 Windows Terminal 선택. Bash도 직접 후보이나 주 분석에서 뒤순위 | jq=1.7 (원문 명시); OS=Ubuntu 24.04.2 LTS in WSL2; Bash=판 미확인; Windows Terminal=판 미확인; cat=구현·판 미확인<br>연구: jq1.7.1; v1.22.11751.0 | Bash 판·실제 argv·완전 설정·Terminal 판/적용 과정 없음. 옛 사용법 링크는 새 적중 아님; 독립성 미확인 | C1: 객체 추가와 기존 배열 보존. C2: 원 내용 변수의 quoting/확장·출력 경계까지 근거 필요<br>R0 HTML C1 U[317,469),[568,1659),[4689,6051); C2 U[1660,2121),[2122,4531) |
| J4 [79727040](https://stackoverflow.com/revisions/5C479B29-6078-4E9A-94FE-5EAFC91A3B9C/view-source) · boundary · 태그순위 6 | volume마다 VolumeId·VolumeType·Size·Iops와 같은 volume의 Key=VolName 값 결합<br>AWS CLI describe-volumes→jq. object/array 모두 허용 | jq=미확인; AWS CLI=major/version 미확인; EC2 API=모델 판 미확인<br>연구: jq1.7.1; 2.28.3 | Iops 원값 없음; null로 남김. 실패 코드 Name과 자연 요구 VolName 불일치. 실제 판·전체 출력 없음; 독립성 미확인 | C1: sibling 필드 보존. C2: 같은 volume의 VolName 태그 연결. 다른 태그와 섞지 않기<br>R0 HTML C1 U[1199,1585),[1926,2092); C2 U[111,1198),[1199,1324),[1586,2092) |
| P1 [79692729](https://stackoverflow.com/revisions/32603E8D-E453-4BCB-895B-83AFBE3FB468/view-source) · boundary · 태그순위 1 | R Markdown→PowerPoint에서 include_graphics 외부 그림의 기본 선택을 SVG/EMF로 설정<br>knitr 입력 함수 경계. 현재 pandoc 태그로 모집됐으나 R0 본문·최초 태그에는 Pandoc 없음 | pandoc=R0 본문·최초 태그에 이름과 판 없음; knitr=미제공; rmarkdown=미제공; external_graphics=JPEG filename only; SVG/EMF variants existence unknown<br>연구: Pandoc3.6; v1.50 | 각 도구판·실제 SVG/EMF 파일·helper 구현·결과 PPT 없음. 재게시 선언 없음; 사건 독립성 미확인 | C1: 전역 선택 또는 한 번 등록한 helper 허용. C2: 선택 경로가 함수 입력에 연결. 호출명 변경 필요<br>R0 HTML C1 U[0,364); C2 U[569,864) |
| P2 [79701174](https://stackoverflow.com/revisions/245AC802-E2BD-486D-9214-F598A55EDD93/view-source) · boundary · 태그순위 2 | @preview/cetz:0.3.4 import를 유지하면서 상대 모듈 a=123과 제목/본문을 같은 Markdown으로 변환<br>Pandoc Typst reader→CeTZ package; 원 Typst compile 성공은 다른 도구/출력 | pandoc=3.1.3; typst=0.13.1 (unknown hash); cetz=0.3.4; showman=미제공<br>연구: Pandoc3.6; v0.4.0 | 원 Pandoc3.1.3·Typst0.13.1·CeTZ0.3.4; 연구는 Pandoc3.6·CeTZ0.4.0. 패키지 로딩·WASM 지원 미확인 | C1: 외부 import 보존. C2: a=123과 같은 Markdown. import 삭제·빈 모듈 치환으로 완료 처리 금지<br>R0 HTML C1 U[1150,1400); C2 U[1619,1796) |
| P3 [79703916](https://stackoverflow.com/revisions/8AA85F98-D6E0-4E96-8BE7-3175E15F8B24/view-source) · boundary · 태그순위 3 | Docker로 기존 build.sh·수정 Eisvogel·pdflatex·두 filter를 보존해 여러 Markdown→한 PDF<br>pandoc/extra container 실행/파일 경계; 호스트에 각 의존을 따로 설치하지 않기 | pandoc_image=pandoc/extra:latest-ubuntu; example run uses pandoc/extra without explicit tag; pandoc=실행 당시 core 판/digest 미제공; eisvogel=custom fork 본문·원판 미제공; pdflatex=미제공; pandoc-latex-environment=미제공; pandoc-latex-unlisted=미제공<br>연구: Pandoc3.6; 인접 고정판 공석 | 질문 이전 최신 안정 이미지 소스 불확정. B3·4 공석. 원 image digest·수정 template·6개 입력·filter판 미제공 | C1: 원 script/layout/template 연결. C2: 명시 engine/filters 보존. F/S 두 쌍 엄격 분모에서 제외<br>R0 HTML C1 U[717,1017); C2 U[2667,2965) |
| P4 [79714790](https://stackoverflow.com/revisions/C5257A15-1963-4E0E-A00B-2D7F337F9210/view-source) · control · 태그순위 4 | YAML title 값 Heading1: Heading2의 콜론을 보존하고 mapping parse 오류 회피<br>Markdown metadata 입력; 대조. 이름만 등장한 mermaid/eqnos filter는 바꾸지 않기 | pandoc=2.18; pandoc-types=1.22.2; texmath=0.12.5.1; skylighting=0.12.3.1; citeproc=0.7; ipynb=0.2; hslua=2.2.1; Lua=5.4<br>연구: Pandoc3.6 | 사용자 Pandoc2.18, 연구3.6. 전체 document/filter/TeX환경과 실제 metadata/종료값 없음. 재게시 선언 없음 | C1: 콜론 의미값 유지. C2: 원 Markdown 입력 경계에서 quoting. PDF 전체 성공은 별도 미확인<br>R0 HTML C1 U[0,123); C2 U[124,323) |

## 2. 32자리 근거 표

U는 원 파일 Unicode 문자, B는 UTF-8 바이트의 0기반 반열린 구간이다. 파일 ID 링크는 아래 고정 원문 주소로 연결된다. 접근/이동/표시/고유는 과금 접근 수, 무료 절 이동 수, 반복 포함 표시 문자 수, 패킷 안 중복을 제거한 표시 문자 수이다. 전체 파일에 접근할 수 있다는 사실을 전체를 읽었다고 세지 않았다. 판정은 필수 조건의 문서 충분성이며 원 사용자 실행 성공이 아니다.

| 질문·정책·읽기 / 패킷 ID | 순위 1–4 / 노출 U·B 범위 | 접근 / 절 이동 / 표시 / 고유 문자 | 조건별 판정·근거 URL/절/정확한 구간 | 완결·누락·오염·첫 판정 UTC |
|---|---|---|---|---|
| J1/A/F / `cc86f215a28e` | 1 [JQ-0001][JQ-0001] U[0,141450) B[0,141452)<br>2 [JQ-0080][JQ-0080] U[0,40020) B[0,40026)<br>3 [JQ-0004][JQ-0004] U[0,10903) B[0,10903)<br>4 [JQ-0002][JQ-0002] U[0,58478) B[0,58478) | 4 / 6 / 17,118 / 16,605<br>[각 구간 로그](evidence/packet-access/cc86f215a28e.jsonl) | C1 지지: [JQ-0001][JQ-0001] §Input/output: input and inputs U[123208,123930) B[123210,123932); [JQ-0001][JQ-0001] §Input/output: debug and input position U[123933,125410) B[123935,125412); [JQ-0004][JQ-0004] §SQL-ish operators: INDEX and JOIN U[10494,10903) B[10494,10903); [JQ-0002][JQ-0002] §f_input U[38482,38825) B[38482,38825) | 완결; 부족 필수 조건 없음; 실행 미확인은 표1<br>관측 오염 0; 선행 공유파일 0<br>R1 2026-11-23T20:01:12.619640+00:00 |
| J1/A/S / `28483f232965` | 1 [JQ-0001][JQ-0001] U[0,1200) B[0,1200)<br>2 [JQ-0080][JQ-0080] U[0,1200) B[0,1203)<br>3 [JQ-0004][JQ-0004] U[0,1200) B[0,1200)<br>4 [JQ-0002][JQ-0002] U[765,1965) B[765,1965) | 4 / 0 / 4,800 / 4,800<br>[각 구간 로그](evidence/packet-access/28483f232965.jsonl) | C1 유보: [JQ-0001][JQ-0001] §Manual introduction U[0,1200) B[0,1200); [JQ-0004][JQ-0004] §Opening helper definitions U[0,1200) B[0,1200) | 미완결; 부족 C1<br>관측 오염 0; 선행 공유파일 0<br>R2 2026-11-23T20:00:41.581Z |
| J1/B/F / `2f20d4696820` | 1 [JQ-0001][JQ-0001] U[0,141450) B[0,141452)<br>2 [JQ-0080][JQ-0080] U[0,40020) B[0,40026)<br>3 [JQ-0004][JQ-0004] U[0,10903) B[0,10903)<br>4 [JQ-0002][JQ-0002] U[0,58478) B[0,58478) | 4 / 8 / 17,520 / 15,601<br>[각 구간 로그](evidence/packet-access/2f20d4696820.jsonl) | C1 지지: [JQ-0001][JQ-0001] §input, inputs, debug, input_filename, input_line_number U[123208,125480) B[123210,125482); [JQ-0004][JQ-0004] §debug(msgs), INDEX and JOIN definitions U[10173,10903) B[10173,10903); [JQ-0002][JQ-0002] §f_input and f_debug U[38492,39160) B[38492,39160) | 완결; 부족 필수 조건 없음; 실행 미확인은 표1<br>관측 오염 0; 선행 공유파일 0<br>R3 2026-11-23T20:01:46.931Z |
| J1/B/S / `90c5d90f8abc` | 1 [JQ-0001][JQ-0001] U[0,1200) B[0,1200)<br>2 [JQ-0080][JQ-0080] U[0,1200) B[0,1203)<br>3 [JQ-0004][JQ-0004] U[0,1200) B[0,1200)<br>4 [JQ-0002][JQ-0002] U[765,1965) B[765,1965) | 4 / 0 / 4,800 / 4,800<br>[각 구간 로그](evidence/packet-access/90c5d90f8abc.jsonl) | C1 유보: [JQ-0001][JQ-0001] §Manual introduction: filters U[0,1200) B[0,1200); [JQ-0004][JQ-0004] §Initial builtin definitions through recurse U[0,1200) B[0,1200) | 미완결; 부족 C1<br>관측 오염 0; 선행 공유파일 0<br>R4 2026-11-23T20:07:43.659Z |
| J2/A/F / `b6aad97ea044` | 1 [JQ-0001][JQ-0001] U[0,141450) B[0,141452)<br>2 [JQ-0090][JQ-0090] U[0,12888) B[0,12890)<br>3 [JQ-0075][JQ-0075] U[0,37577) B[0,37577)<br>4 [JQ-0080][JQ-0080] U[0,40020) B[0,40026) | 4 / 6 / 15,378 / 14,055<br>[각 구간 로그](evidence/packet-access/b6aad97ea044.jsonl) | C1 지지: [JQ-0001][JQ-0001] §map(f) U[37458,38500) B[37458,38500); [JQ-0001][JQ-0001] §Object construction U[26075,28280) B[26075,28280); [JQ-0001][JQ-0001] §to_entries/from_entries U[43318,44651) B[43318,44651); [JQ-0001][JQ-0001] §Update-assignment U[129722,131900) B[129724,131902)<br>C2 지지: [JQ-0001][JQ-0001] §Object identifier-index U[16169,17386) B[16169,17386); [JQ-0001][JQ-0001] §Object construction U[26075,28280) B[26075,28280); [JQ-0001][JQ-0001] §from_entries U[43318,44651) B[43318,44651) | 완결; 부족 필수 조건 없음; 실행 미확인은 표1<br>관측 오염 0; 선행 공유파일 2<br>R4 2026-11-23T20:08:40.649Z |
| J2/A/S / `3ea1130ebcab` | 1 [JQ-0001][JQ-0001] U[1268,2468) B[1268,2468)<br>2 [JQ-0090][JQ-0090] U[66,1266) B[66,1266)<br>3 [JQ-0075][JQ-0075] U[809,2009) B[809,2009)<br>4 [JQ-0080][JQ-0080] U[0,1200) B[0,1203) | 4 / 0 / 4,800 / 4,800<br>[각 구간 로그](evidence/packet-access/3ea1130ebcab.jsonl) | C1 부분: [JQ-0090][JQ-0090] §Array iteration tests U[1099,1260) B[1099,1260)<br>C2 부분: [JQ-0090][JQ-0090] §Missing object-property test U[540,588) B[540,588) | 미완결; 부족 C1,C2<br>관측 오염 0; 선행 공유파일 2<br>R1 2026-11-23T20:02:21.780124+00:00 |
| J2/B/F / `14f044b30814` | 1 [JQ-0001][JQ-0001] U[0,141450) B[0,141452)<br>2 [JQ-0090][JQ-0090] U[0,12888) B[0,12890)<br>3 [SED-0001][SED-0001] U[0,165398) B[0,165399)<br>4 [SED-0022][SED-0022] U[0,9656) B[0,9656) | 4 / 6 / 17,791 / 15,932<br>[각 구간 로그](evidence/packet-access/14f044b30814.jsonl) | C1 지지: [JQ-0001][JQ-0001] §map(f) U[37458,39500) B[37458,39500); [JQ-0001][JQ-0001] §Object Construction U[26075,28900) B[26075,28900); [JQ-0001][JQ-0001] §to_entries/from_entries U[43545,45400) B[43545,45400); [JQ-0001][JQ-0001] §Update-assignment U[129714,131089) B[129716,131091)<br>C2 지지: [JQ-0001][JQ-0001] §Object Identifier-Index U[16161,17376) B[16161,17376); [JQ-0001][JQ-0001] §to_entries/from_entries U[43545,45400) B[43545,45400) | 완결; 부족 필수 조건 없음; 실행 미확인은 표1<br>관측 오염 0; 선행 공유파일 1<br>R2 2026-11-23T20:01:30.606Z |
| J2/B/S / `2d1378170a3d` | 1 [JQ-0001][JQ-0001] U[1268,2468) B[1268,2468)<br>2 [JQ-0090][JQ-0090] U[66,1266) B[66,1266)<br>3 [SED-0001][SED-0001] U[185,1385) B[185,1385)<br>4 [SED-0022][SED-0022] U[0,1200) B[0,1200) | 4 / 0 / 4,800 / 4,800<br>[각 구간 로그](evidence/packet-access/2d1378170a3d.jsonl) | C1 부분: [JQ-0001][JQ-0001] §Synopsis: map example and input stream U[1268,2468) B[1268,2468); [JQ-0090][JQ-0090] §Field lookup and array iteration tests U[66,1266) B[66,1266)<br>C2 부분: [JQ-0090][JQ-0090] §Missing-field lookup produces null U[66,1266) B[66,1266) | 미완결; 부족 C1,C2<br>관측 오염 0; 선행 공유파일 1<br>R3 2026-11-23T20:02:37.459Z |
| J3/A/F / `a13997d37fef` | 1 [JQ-0001][JQ-0001] U[0,141450) B[0,141452)<br>2 [JQ-0016][JQ-0016] U[0,397278) B[0,397278)<br>3 [JQ-0070][JQ-0070] U[0,27721) B[0,27721)<br>4 [JQ-0072][JQ-0072] U[0,153926) B[0,153926) | 4 / 7 / 18,358 / 15,761<br>[각 구간 로그](evidence/packet-access/a13997d37fef.jsonl) | C1 지지: [JQ-0001][JQ-0001] §--arg, --argjson, --slurpfile U[9370,10420) B[9370,10420); [JQ-0001][JQ-0001] §Addition U[30647,31187) B[30647,31187); [JQ-0001][JQ-0001] §Assignment and update-assignment U[127474,130839) B[127476,130841); [JQ-0001][JQ-0001] §Arithmetic update-assignment U[130839,131776) B[130841,131778)<br>C2 부분: [JQ-0001][JQ-0001] §Invoking jq: shell quoting guidance U[3325,4597) B[3325,4597); [JQ-0070][JQ-0070] §--argjson option processing U[17844,18754) B[17844,18754) | 미완결; 부족 C2<br>관측 오염 0; 선행 공유파일 1<br>R3 2026-11-23T20:03:44.034Z |
| J3/A/S / `8591724781d4` | 1 [JQ-0001][JQ-0001] U[309,1509) B[309,1509)<br>2 [JQ-0016][JQ-0016] U[11388,12588) B[11388,12588)<br>3 [JQ-0070][JQ-0070] U[30,1230) B[30,1230)<br>4 [JQ-0072][JQ-0072] U[1797,2997) B[1797,2997) | 4 / 0 / 4,800 / 4,800<br>[각 구간 로그](evidence/packet-access/8591724781d4.jsonl) | C1 유보: [JQ-0001][JQ-0001] §Manual introduction U[309,1509) B[309,1509)<br>C2 유보: [JQ-0070][JQ-0070] §Includes and usage preamble U[30,1230) B[30,1230) | 미완결; 부족 C1,C2<br>관측 오염 0; 선행 공유파일 1<br>R4 2026-11-23T20:09:11.869Z |
| J3/B/F / `0be2a4830a4c` | 1 [JQ-0001][JQ-0001] U[0,141450) B[0,141452)<br>2 [JQ-0016][JQ-0016] U[0,397278) B[0,397278)<br>3 [WT-0021][WT-0021] U[0,107447) B[0,107473)<br>4 [WT-0039][WT-0039] U[0,32520) B[0,32586) | 4 / 11 / 24,468 / 20,174<br>[각 구간 로그](evidence/packet-access/0be2a4830a4c.jsonl) | C1 지지: [JQ-0001][JQ-0001] §Array construction U[24727,24995) B[24727,24995); [JQ-0001][JQ-0001] §Addition U[30675,31185) B[30675,31185); [JQ-0001][JQ-0001] §Assignment U[127820,129225) B[127822,129227); [JQ-0001][JQ-0001] §Arithmetic update-assignment U[131097,131505) B[131099,131507)<br>C2 부분: [JQ-0001][JQ-0001] §--arg and --argjson U[9396,10073) B[9396,10073); [JQ-0001][JQ-0001] §Invoking jq: Unix shell quoting U[3460,3880) B[3460,3880) | 미완결; 부족 C2<br>관측 오염 0; 선행 공유파일 1<br>R1 2026-11-23T20:03:36.948789+00:00 |
| J3/B/S / `a76ec0d77f82` | 1 [JQ-0001][JQ-0001] U[309,1509) B[309,1509)<br>2 [JQ-0016][JQ-0016] U[11388,12588) B[11388,12588)<br>3 [WT-0021][WT-0021] U[0,1200) B[0,1200)<br>4 [WT-0039][WT-0039] U[0,1200) B[0,1200) | 4 / 0 / 4,800 / 4,800<br>[각 구간 로그](evidence/packet-access/a76ec0d77f82.jsonl) | C1 유보: [JQ-0001][JQ-0001] §Filter-composition introduction U[309,1509) B[309,1509)<br>C2 유보: [JQ-0001][JQ-0001] §Filter-composition introduction U[309,1509) B[309,1509) | 미완결; 부족 C1,C2<br>관측 오염 0; 선행 공유파일 1<br>R2 2026-11-23T20:02:00.079Z |
| J4/A/F / `a0007d0fb17a` | 1 [JQ-0001][JQ-0001] U[0,141450) B[0,141452)<br>2 [JQ-0007][JQ-0007] U[0,45252) B[0,45252)<br>3 [JQ-0045][JQ-0045] U[0,51876) B[0,51877)<br>4 [JQ-0046][JQ-0046] U[0,10505) B[0,10505) | 4 / 6 / 20,681 / 17,125<br>[각 구간 로그](evidence/packet-access/a0007d0fb17a.jsonl) | C1 지지: [JQ-0001][JQ-0001] §Array/Object Value Iterator; Pipe U[20022,23700) B[20022,23700); [JQ-0001][JQ-0001] §Array and Object Construction U[24719,28900) B[24719,28900); [JQ-0001][JQ-0001] §Object Identifier-Index U[16161,17376) B[16161,17376)<br>C2 지지: [JQ-0001][JQ-0001] §Object Construction U[26075,28900) B[26075,28900); [JQ-0001][JQ-0001] §select(boolean_expression) U[44666,45340) B[44666,45340); [JQ-0001][JQ-0001] §Iterator; Pipe; Parenthesis U[20022,23700) B[20022,23700); [JQ-0001][JQ-0001] §Array Index U[18230,19200) B[18230,19200) | 완결; 부족 필수 조건 없음; 실행 미확인은 표1<br>관측 오염 0; 선행 공유파일 1<br>R2 2026-11-23T20:02:53.668Z |
| J4/A/S / `d018c8051020` | 1 [JQ-0001][JQ-0001] U[5933,7133) B[5933,7133)<br>2 [JQ-0007][JQ-0007] U[22375,23575) B[22375,23575)<br>3 [JQ-0045][JQ-0045] U[6282,7482) B[6283,7483)<br>4 [JQ-0046][JQ-0046] U[537,1737) B[537,1737) | 4 / 0 / 4,800 / 4,800<br>[각 구간 로그](evidence/packet-access/d018c8051020.jsonl) | C1 유보: [JQ-0001][JQ-0001] §Output formatting switches U[5933,7133) B[5933,7133); [JQ-0046][JQ-0046] §jv scalar and array API declarations U[537,1737) B[537,1737)<br>C2 유보: 패킷 안 충분한 인용 없음 | 미완결; 부족 C1,C2<br>관측 오염 0; 선행 공유파일 1<br>R3 2026-11-23T20:04:29.486Z |
| J4/B/F / `837da1ed6706` | 1 [JQ-0001][JQ-0001] U[0,141450) B[0,141452)<br>2 [JQ-0007][JQ-0007] U[0,45252) B[0,45252)<br>3 [AWS-0706][AWS-0706] U[0,3698) B[0,3698)<br>4 [AWS-0248][AWS-0248] U[0,29016) B[0,29016) | 4 / 5 / 18,161 / 17,895<br>[각 구간 로그](evidence/packet-access/837da1ed6706.jsonl) | C1 지지: [JQ-0001][JQ-0001] §Object/array indexing and value iteration U[16169,22000) B[16169,22000); [JQ-0001][JQ-0001] §Array and object construction U[24000,28280) B[24000,28280); [JQ-0001][JQ-0001] §Pipe and grouping U[22000,24000) B[22000,24000)<br>C2 지지: [JQ-0001][JQ-0001] §select(boolean_expression) U[44666,45400) B[44666,45400); [JQ-0001][JQ-0001] §Optional iteration and array indexing U[16169,22000) B[16169,22000); [JQ-0001][JQ-0001] §Array and object construction U[24000,28280) B[24000,28280); [JQ-0001][JQ-0001] §Pipe and parentheses U[22000,24000) B[22000,24000) | 완결; 부족 필수 조건 없음; 실행 미확인은 표1<br>관측 오염 0; 선행 공유파일 1<br>R4 2026-11-23T20:10:05.098Z |
| J4/B/S / `a032f9aa185e` | 1 [JQ-0001][JQ-0001] U[5933,7133) B[5933,7133)<br>2 [JQ-0007][JQ-0007] U[22375,23575) B[22375,23575)<br>3 [AWS-0706][AWS-0706] U[0,1200) B[0,1200)<br>4 [AWS-0248][AWS-0248] U[2299,3499) B[2299,3499) | 4 / 0 / 4,800 / 4,800<br>[각 구간 로그](evidence/packet-access/a032f9aa185e.jsonl) | C1 부분: [AWS-0706][AWS-0706] §describe-volumes Example 1 output U[920,1170) B[920,1170)<br>C2 유보: 패킷 안 충분한 인용 없음 | 미완결; 부족 C1,C2<br>관측 오염 0; 선행 공유파일 1<br>R1 2026-11-23T20:04:17.419737+00:00 |
| P1/A/F / `523094dc11e7` | 1 [PD-0012][PD-0012] U[0,147280) B[0,147310)<br>2 [PD-0001][PD-0001] U[0,284739) B[0,284775)<br>3 [PD-0227][PD-0227] U[0,119866) B[0,119866)<br>4 [PD-0005][PD-0005] U[0,6110) B[0,6114) | 4 / 9 / 16,087 / 15,335<br>[각 구간 로그](evidence/packet-access/523094dc11e7.jsonl) | C1 부분: [PD-0012][PD-0012] §FORMAT global U[8857,9115) B[8858,9116); [PD-0012][PD-0012] §Image fields U[40888,41164) B[40911,41187); [PD-0227][PD-0227] §PowerPoint image extension selection U[37330,37731) B[37330,37731); [PD-0001][PD-0001] §--default-image-extension U[23275,23562) B[23275,23562)<br>C2 유보: [PD-0012][PD-0012] §Lua filter structure and invocation U[2630,3145) B[2630,3145) | 미완결; 부족 C1,C2<br>관측 오염 0; 선행 공유파일 0<br>R1 2026-11-23T20:05:28.933053+00:00 |
| P1/A/S / `932ed36d42d8` | 1 [PD-0012][PD-0012] U[2564,3764) B[2564,3764)<br>2 [PD-0001][PD-0001] U[11,1211) B[11,1211)<br>3 [PD-0227][PD-0227] U[78,1278) B[78,1278)<br>4 [PD-0005][PD-0005] U[0,1200) B[0,1204) | 4 / 0 / 4,800 / 4,800<br>[각 구간 로그](evidence/packet-access/932ed36d42d8.jsonl) | C1 유보: [PD-0012][PD-0012] §Lua filter structure U[2564,3764) B[2564,3764)<br>C2 유보: [PD-0012][PD-0012] §Lua filter structure U[2564,3764) B[2564,3764); [PD-0227][PD-0227] §Powerpoint.Output module header/imports U[78,1278) B[78,1278) | 미완결; 부족 C1,C2<br>관측 오염 0; 선행 공유파일 0<br>R2 2026-11-23T20:03:17.755Z |
| P1/B/F / `2c39a224e483` | 1 [PD-0012][PD-0012] U[0,147280) B[0,147310)<br>2 [PD-0001][PD-0001] U[0,284739) B[0,284775)<br>3 [KN-0024][KN-0024] U[0,24804) B[0,24804)<br>4 [KN-0013][KN-0013] U[0,19168) B[0,19168) | 4 / 6 / 18,468 / 15,286<br>[각 구간 로그](evidence/packet-access/2c39a224e483.jsonl) | C1 지지: [KN-0024][KN-0024] §include_graphics documentation and implementation U[13900,18600) B[13900,18600); [KN-0013][KN-0013] §Plot hook filename manipulation with sub and sprintf U[7662,8178) B[7662,8178); [PD-0001][PD-0001] §--default-image-extension U[23274,23950) B[23274,23950)<br>C2 지지: [KN-0024][KN-0024] §include_graphics path argument, R-chunk use, S3 path return, auto_pdf branch U[13900,18600) B[13900,18600); [KN-0024][KN-0024] §dev2ext and generated-plot device extensions U[0,1200) B[0,1200) | 완결; 부족 필수 조건 없음; 실행 미확인은 표1<br>관측 오염 0; 선행 공유파일 0<br>R3 2026-11-23T20:06:09.356Z |
| P1/B/S / `edb07d55ddaf` | 1 [PD-0012][PD-0012] U[2564,3764) B[2564,3764)<br>2 [PD-0001][PD-0001] U[11,1211) B[11,1211)<br>3 [KN-0024][KN-0024] U[0,1200) B[0,1200)<br>4 [KN-0013][KN-0013] U[0,1200) B[0,1200) | 4 / 0 / 4,800 / 4,800<br>[각 구간 로그](evidence/packet-access/edb07d55ddaf.jsonl) | C1 유보: [KN-0024][KN-0024] §auto_exts and dev2ext U[0,1200) B[0,1200)<br>C2 유보: [KN-0013][KN-0013] §Default plot-hook documentation U[0,1200) B[0,1200); [PD-0012][PD-0012] §Lua filter structure U[2564,3764) B[2564,3764) | 미완결; 부족 C1,C2<br>관측 오염 0; 선행 공유파일 0<br>R4 2026-11-23T20:10:33.832Z |
| P2/A/F / `169dbf5f4342` | 1 [PD-0001][PD-0001] U[0,284739) B[0,284775)<br>2 [PD-0007][PD-0007] U[0,7933) B[0,7933)<br>3 [PD-0012][PD-0012] U[0,147280) B[0,147310)<br>4 [PD-0018][PD-0018] U[0,10756) B[0,10756) | 4 / 7 / 13,572 / 13,572<br>[각 구간 로그](evidence/packet-access/169dbf5f4342.jsonl) | C1 유보: [PD-0001][PD-0001] §Input format list U[10890,11404) B[10890,11404); [PD-0012][PD-0012] §Lua filters introduction U[0,1200) B[0,1200)<br>C2 유보: [PD-0001][PD-0001] §Description and architecture U[0,1200) B[0,1200); [PD-0018][PD-0018] §Document representation and basic architecture U[1469,3299) B[1469,3299) | 미완결; 부족 C1,C2<br>관측 오염 0; 선행 공유파일 2<br>R4 2026-11-23T20:11:56.053Z |
| P2/A/S / `2f55c804a8f3` | 1 [PD-0001][PD-0001] U[0,1200) B[0,1200)<br>2 [PD-0007][PD-0007] U[0,1200) B[0,1200)<br>3 [PD-0012][PD-0012] U[0,1200) B[0,1200)<br>4 [PD-0018][PD-0018] U[0,1200) B[0,1200) | 4 / 0 / 4,800 / 4,800<br>[각 구간 로그](evidence/packet-access/2f55c804a8f3.jsonl) | C1 유보: [PD-0012][PD-0012] §Introduction: filter processing phase U[120,520) B[120,520)<br>C2 유보: 패킷 안 충분한 인용 없음 | 미완결; 부족 C1,C2<br>관측 오염 0; 선행 공유파일 2<br>R1 2026-11-23T20:06:01.184415+00:00 |
| P2/B/F / `7e9b0eaaaf03` | 1 [PD-0001][PD-0001] U[0,284739) B[0,284775)<br>2 [PD-0007][PD-0007] U[0,7933) B[0,7933)<br>3 [CE-0001][CE-0001] U[0,3839) B[0,3839)<br>4 [CE-0004][CE-0004] U[0,16865) B[0,16865) | 4 / 5 / 9,924 / 9,859<br>[각 구간 로그](evidence/packet-access/7e9b0eaaaf03.jsonl) | C1 유보: [PD-0001][PD-0001] §Input formats U[10890,11404) B[10890,11404); [CE-0001][CE-0001] §Usage and Installing U[1135,2354) B[1135,2354); [CE-0004][CE-0004] §bezier module imports and plugin initialization U[0,1200) B[0,1200)<br>C2 유보: [PD-0001][PD-0001] §Input formats U[10890,11404) B[10890,11404); [PD-0001][PD-0001] §Markdown heading output option U[45661,46367) B[45661,46367) | 미완결; 부족 C1,C2<br>관측 오염 0; 선행 공유파일 1<br>R2 2026-11-23T20:04:15.106Z |
| P2/B/S / `342eea14f081` | 1 [PD-0001][PD-0001] U[0,1200) B[0,1200)<br>2 [PD-0007][PD-0007] U[0,1200) B[0,1200)<br>3 [CE-0001][CE-0001] U[0,1200) B[0,1200)<br>4 [CE-0004][CE-0004] U[0,1200) B[0,1200) | 4 / 0 / 4,800 / 4,800<br>[각 구간 로그](evidence/packet-access/342eea14f081.jsonl) | C1 유보: [PD-0001][PD-0001] §Synopsis and general architecture U[0,1200) B[0,1200); [CE-0004][CE-0004] §CeTZ bezier imports and plugin declaration U[0,1200) B[0,1200)<br>C2 유보: 패킷 안 충분한 인용 없음 | 미완결; 부족 C1,C2<br>관측 오염 0; 선행 공유파일 1<br>R3 2026-11-23T20:06:41.576Z |
| P3/A/F / `c0b7629f5619` | 1 [PD-0001][PD-0001] U[0,284739) B[0,284775)<br>2 [PD-0007][PD-0007] U[0,7933) B[0,7933)<br>3 [PD-0012][PD-0012] U[0,147280) B[0,147310)<br>4 [PD-0022][PD-0022] U[0,51623) B[0,51623) | 4 / 7 / 16,520 / 15,940<br>[각 구간 로그](evidence/packet-access/c0b7629f5619.jsonl) | C1 부분: [PD-0001][PD-0001] §Multiple input files U[2138,2648) B[2138,2648); [PD-0001][PD-0001] §--template U[31261,32067) B[31261,32067)<br>C2 부분: [PD-0001][PD-0001] §--pdf-engine U[60024,61100) B[60024,61100); [PD-0001][PD-0001] §--filter and filter lookup/order U[24270,27150) B[24270,27150); [PD-0012][PD-0012] §Filter introduction U[0,1200) B[0,1200) | 비교불가(문서 미완결); 부족 C1,C2<br>관측 오염 0; 선행 공유파일 3<br>R3 2026-11-23T20:07:29.421Z |
| P3/A/S / `78178fae9374` | 1 [PD-0001][PD-0001] U[202,1402) B[202,1402)<br>2 [PD-0007][PD-0007] U[0,1200) B[0,1200)<br>3 [PD-0012][PD-0012] U[2564,3764) B[2564,3764)<br>4 [PD-0022][PD-0022] U[4823,6023) B[4823,6023) | 4 / 0 / 4,800 / 4,800<br>[각 구간 로그](evidence/packet-access/78178fae9374.jsonl) | C1 유보: [PD-0001][PD-0001] §Description and architecture U[202,1402) B[202,1402)<br>C2 유보: [PD-0007][PD-0007] §FAQ: PDF engine U[0,1200) B[0,1200); [PD-0012][PD-0012] §Lua filter structure U[2564,3764) B[2564,3764) | 비교불가(문서 미완결); 부족 C1,C2<br>관측 오염 0; 선행 공유파일 3<br>R4 2026-11-23T20:12:38.460Z |
| P3/B/F / `5480c02357ef` | 1 [PD-0001][PD-0001] U[0,284739) B[0,284775)<br>2 [PD-0007][PD-0007] U[0,7933) B[0,7933)<br>3 공석(1접근 과금)<br>4 공석(1접근 과금) | 4 / 7 / 15,743 / 14,691<br>[각 구간 로그](evidence/packet-access/5480c02357ef.jsonl) | C1 부분: [PD-0001][PD-0001] §Multiple input files U[2340,2515) B[2340,2515); [PD-0001][PD-0001] §--template U[31511,32030) B[31511,32030)<br>C2 부분: [PD-0001][PD-0001] §--pdf-engine U[60024,60390) B[60024,60390); [PD-0001][PD-0001] §--filter U[24265,24815) B[24265,24815); [PD-0001][PD-0001] §Filter lookup and ordering U[25220,25660) B[25220,25660) | 비교불가(문서 미완결); 부족 C1,C2<br>관측 오염 0; 선행 공유파일 2<br>R1 2026-11-23T20:06:48.227426+00:00 |
| P3/B/S / `09c26140214f` | 1 [PD-0001][PD-0001] U[202,1402) B[202,1402)<br>2 [PD-0007][PD-0007] U[0,1200) B[0,1200)<br>3 공석(1접근 과금)<br>4 공석(1접근 과금) | 4 / 0 / 2,400 / 2,400<br>[각 구간 로그](evidence/packet-access/09c26140214f.jsonl) | C1 유보: [PD-0001][PD-0001] §General conversion and AST/filter introduction U[202,1402) B[202,1402); [PD-0007][PD-0007] §FAQ opening, standalone output and PDF engine U[0,1200) B[0,1200)<br>C2 유보: [PD-0007][PD-0007] §FAQ opening, standalone output and PDF engine U[0,1200) B[0,1200); [PD-0001][PD-0001] §General conversion and AST/filter introduction U[202,1402) B[202,1402) | 비교불가(문서 미완결); 부족 C1,C2<br>관측 오염 0; 선행 공유파일 2<br>R2 2026-11-23T20:04:43.414Z |
| P4/A/F / `ac9beb264939` | 1 [PD-0001][PD-0001] U[0,284739) B[0,284775)<br>2 [PD-0024][PD-0024] U[0,40718) B[0,40718)<br>3 [PD-0012][PD-0012] U[0,147280) B[0,147310)<br>4 [PD-0031][PD-0031] U[0,25423) B[0,25423) | 4 / 3 / 13,492 / 12,588<br>[각 구간 로그](evidence/packet-access/ac9beb264939.jsonl) | C1 지지: [PD-0001][PD-0001] §yaml_metadata_block: escaping rules and quoted-title example U[190704,192200) B[190713,192209)<br>C2 지지: [PD-0001][PD-0001] §yaml_metadata_block: delimiters and metadata reading U[188840,190704) B[188849,190713); [PD-0012][PD-0012] §Introduction: filters between parsing and writing U[0,1200) B[0,1200) | 완결; 부족 필수 조건 없음; 실행 미확인은 표1<br>관측 오염 0; 선행 공유파일 2<br>R2 2026-11-23T20:05:35.000Z |
| P4/A/S / `4b6da2f3c82a` | 1 [PD-0001][PD-0001] U[0,1200) B[0,1200)<br>2 [PD-0024][PD-0024] U[86,1286) B[86,1286)<br>3 [PD-0012][PD-0012] U[0,1200) B[0,1200)<br>4 [PD-0031][PD-0031] U[20,1220) B[20,1220) | 4 / 0 / 4,800 / 4,800<br>[각 구간 로그](evidence/packet-access/4b6da2f3c82a.jsonl) | C1 유보: 패킷 안 충분한 인용 없음<br>C2 부분: [PD-0012][PD-0012] §Introduction: filters between parsing and writing U[0,1200) B[0,1200) | 미완결; 부족 C1,C2<br>관측 오염 0; 선행 공유파일 2<br>R3 2026-11-23T20:08:12.579Z |
| P4/B/F / `529295ca2f71` | 1 [PD-0001][PD-0001] U[0,284739) B[0,284775)<br>2 [PD-0024][PD-0024] U[0,40718) B[0,40718)<br>3 [PD-0012][PD-0012] U[0,147280) B[0,147310)<br>4 [PD-0031][PD-0031] U[0,25423) B[0,25423) | 4 / 3 / 17,328 / 14,965<br>[각 구간 로그](evidence/packet-access/529295ca2f71.jsonl) | C1 지지: [PD-0001][PD-0001] §Extension: yaml_metadata_block; YAML escaping and quoted-title example U[188838,193650) B[188847,193659)<br>C2 지지: [PD-0001][PD-0001] §Extension: yaml_metadata_block U[188838,193650) B[188847,193659); [PD-0012][PD-0012] §Lua filters introduction U[0,1200) B[0,1200) | 완결; 부족 필수 조건 없음; 실행 미확인은 표1<br>관측 오염 0; 선행 공유파일 2<br>R4 2026-11-23T20:13:30.141Z |
| P4/B/S / `3092b6d907de` | 1 [PD-0001][PD-0001] U[0,1200) B[0,1200)<br>2 [PD-0024][PD-0024] U[86,1286) B[86,1286)<br>3 [PD-0012][PD-0012] U[0,1200) B[0,1200)<br>4 [PD-0031][PD-0031] U[20,1220) B[20,1220) | 4 / 0 / 4,800 / 4,800<br>[각 구간 로그](evidence/packet-access/3092b6d907de.jsonl) | C1 유보: 패킷 안 충분한 인용 없음<br>C2 부분: [PD-0012][PD-0012] §Introduction: filter processing phase U[120,520) B[120,520) | 미완결; 부족 C1,C2<br>관측 오염 0; 선행 공유파일 2<br>R1 2026-11-23T20:07:42.271771+00:00 |

## 3. 비교·반환 표

반환은 봉인 후 만든 편집안이며 질문별 최대 두 링크이다. 서로 다른 패킷 또는 사후 자료를 조합한 반환 링크는 주32판정의 근거를 추가하지 않는다. 특히 P1의 둘째 writer 링크는 A에 있던 출력 단서이고 P3 Docker README는 사후에만 연 오래된 고정판이다. 두 링크가 모든 조건을 덮지 못하면 실패 조건에 명시했다.

| 질문 | F의 A·B | S의 A·B | 밀림·추가 근거 | 줄 링크·볼 절·한계 | 사후 질문자 행동·미확인 |
|---|---|---|---|---|---|
| J1 | A 완결 / B 완결 | A 미완결 / B 미완결 | A/B 동일. S는 input/debug/INDEX·JOIN 핵심 절을 놓침 | [JQ-0001][JQ-0001] — Input/output: input·inputs·debug·input_filename<br>[JQ-0004][JQ-0004] — SQL-ish INDEX/JOIN 정의<br>실패 조건: 원 두 파일 없이 실제 break 원인이나 최종 JOIN 성공은 확정할 수 없다. | 질문자는 inputs[]로 오류는 사라졌지만 JOIN은 안 됐다고 보고. 진단/정확 출력 검증 없음<br>[공개 후속](https://stackoverflow.com/questions/79694539#comment140577987_79694539) |
| J2 | A 완결 / B 완결 | A 미완결 / B 미완결 | jq 원 시험을 잃고 sed 설명·시험을 얻음. 핵심은 남은 jq 매뉴얼; F 양쪽 완결, S 일부 null 근거만 남음 | [JQ-0001][JQ-0001] — Object/array lookup, map, from_entries, update assignment<br>[SED-0001][SED-0001] — s command / replacement / g flag<br>실패 조건: 원 envelope·EventData 없는 사건과 + 치환의 의미를 확인해야 전체 파이프라인 성공을 말할 수 있다. | 자기답의 설명이 수정됐고 채택답은 yq 경로로 바꿈. UserData 사건 추가 공개; 원 전체 로그 실행은 미검증<br>[공개 후속](https://stackoverflow.com/a/79700162) |
| J3 | A 미완결 / B 미완결 | A 미완결 / B 미완결 | argv 수신 구현을 잃고 Terminal schema를 얻음. 필수 Bash 경계는 양쪽 부족; snippets 설계안은 대체 근거 아님 | [JQ-0001][JQ-0001] — --argjson, addition, update assignment<br>[JQ-0070][JQ-0070] — --argjson argv 처리<br>실패 조건: 이 두 링크만으로 Bash 변수 확장·word splitting과 리다이렉션을 모두 지지하지 못한다. | 질문자는 $@ 파일 인수 대안의 성공을 보고. 원 JSON 내용 변수 방식·출력 파일·판 일치는 미검증<br>[공개 후속](https://stackoverflow.com/questions/79711268#comment140613190_79711304) |
| J4 | A 완결 / B 완결 | A 미완결 / B 미완결 | 저수준 jv API 대신 실제 입력 예제를 얻지만 주 매뉴얼과 원 질문으로 F 둘 다 충족. EMR 문서는 어휘 중복 | [JQ-0001][JQ-0001] — object construction, select, from_entries, operator grouping<br>[AWS-0706][AWS-0706] — Examples 1 and 4: Volumes·Tags<br>실패 조건: 예제의 Iops 숫자나 Name 태그를 원 요구에 대신 넣을 수 없다. | 채택답이 VolName과 null Iops에 맞음. 답변자 예시 출력만 있고 질문자 실행보고 없음<br>[공개 후속](https://stackoverflow.com/a/79727098) |
| P1 | A 미완결 / B 완결 | A 미완결 / B 미완결 | 출력 writer 근거를 잃고 knitr 입력 함수 연결을 얻어 F에서만 B 단독 완결. 내장 옵션 한정이면 이득 0 | [KN-0024][KN-0024] — include_graphics path/auto_pdf/file.exists/return class, chars13900–18600<br>[PD-0227][PD-0227] — image type mapping: Svg and Emf<br>실패 조건: helper 호출로 바꾸고 실제 대체 파일이 있어야 한다. 내장 SVG/EMF 기본 옵션 또는 원 PowerPoint 실행은 입증되지 않았다. | 질문자는 이미 helper를 쓰며 수용 가능하다고 함. 새 채택·개선 효과로 귀속할 수 없고 내장 옵션은 미확인<br>[공개 후속](https://stackoverflow.com/questions/79692729#comment140579507_79692729) |
| P2 | A 미완결 / B 미완결 | A 미완결 / B 미완결 | CeTZ의 설치·tytanic·WASM 요구를 얻으나 Pandoc resolver 근거는 없음. F/S A/B 모두 미완결 | [PD-0001][PD-0001] — input format typst; reader/filter phase<br>[CE-0001][CE-0001] — Usage and local installation (0.4.0)<br>실패 조건: 연구판 README의 local import가 원 0.3.4와 Pandoc3.1.3에서 같은 결과를 낸다고 볼 수 없다. | 답·30일 댓글·후속 수정 없음. 공개 부재는 기술적으로 불가능하다는 증거가 아님<br>[공개 후속](https://stackoverflow.com/questions/79701174) |
| P3 | A 미완결 / B 공석 → 비교불가 | A 미완결 / B 공석 → 비교불가 | 주 문서의 외부 의존 설명은 남지만 두 인접 공석을 채울 수 없음. 오래된 고정 README는 사후 반환에만 사용 | [PD-0001][PD-0001] — multiple input files, --template, --pdf-engine, --filter<br>[Docker 고정 README](https://github.com/pandoc/dockerfiles/blob/7f10864aea88fc746c727f12a61a24cdc0eb93d5/README.md) — Usage / ENTRYPOINT / Building custom images; 사후·오래된 고정판<br>실패 조건: 과거 latest 이미지와 원 template/filters가 없으므로 사후 문서로 사전 공석을 복구하거나 원 PDF 성공을 주장할 수 없다. | 질문자가 작동 Dockerfile을 만들었다고 보고했지만 취득한 스레드에는 실제 파일·digest·PDF가 없음; 비교불가 유지<br>[공개 후속](https://stackoverflow.com/questions/79703916#comment140597463_79703916) |
| P4 | A 완결 / B 완결 | A 미완결 / B 미완결 | A/B 동일. F 매뉴얼 깊은 YAML 절로 충족하지만 S 헤더에서 해당 문법 근거를 얻지 못함 | [PD-0001][PD-0001] — Extension: yaml_metadata_block, chars188840–192200<br>[PD-0012][PD-0012] — Introduction: filters operate after parsing<br>실패 조건: 메타데이터 문법의 문서 충분성이다. 원 Pandoc2.18 실행·필터·최종 PDF를 확인하거나 렌더링하지 않았다. | 같은 title을 따옴표로 감싼 답을 채택. 질문자 실행로그·PDF 성공 보고 없음<br>[공개 후속](https://stackoverflow.com/a/79714812) |

[AWS-0248]: https://github.com/aws/aws-cli/blob/75930d5779a99149020e242c5b834d2f28b3669f/awscli/customizations/emr/helptext.py
[AWS-0706]: https://github.com/aws/aws-cli/blob/75930d5779a99149020e242c5b834d2f28b3669f/awscli/examples/ec2/describe-volumes.rst
[CE-0001]: https://github.com/cetz-package/cetz/blob/f91db3185576a92fd121d15d2cd893e18133fd42/README.md
[CE-0004]: https://github.com/cetz-package/cetz/blob/f91db3185576a92fd121d15d2cd893e18133fd42/src/bezier.typ
[JQ-0001]: https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml
[JQ-0002]: https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/builtin.c
[JQ-0004]: https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/builtin.jq
[JQ-0007]: https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/compile.c
[JQ-0016]: https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/decNumber/decNumber.c
[JQ-0045]: https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/jv.c
[JQ-0046]: https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/jv.h
[JQ-0070]: https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/main.c
[JQ-0072]: https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/parser.c
[JQ-0075]: https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/util.c
[JQ-0080]: https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/tests/jq.test
[JQ-0090]: https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/tests/man.test
[KN-0013]: https://github.com/yihui/knitr/blob/01bf7eff974903d1498e76e92a3e4b3bf9273cf5/R/hooks-latex.R
[KN-0024]: https://github.com/yihui/knitr/blob/01bf7eff974903d1498e76e92a3e4b3bf9273cf5/R/plot.R
[PD-0001]: https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/MANUAL.txt
[PD-0005]: https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/doc/epub.md
[PD-0007]: https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/doc/faqs.md
[PD-0012]: https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/doc/lua-filters.md
[PD-0018]: https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/doc/short-guide-to-pandocs-sources.md
[PD-0022]: https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/src/Text/Pandoc/App/CommandLineOptions.hs
[PD-0024]: https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/src/Text/Pandoc/App/Opt.hs
[PD-0031]: https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/src/Text/Pandoc/Citeproc.hs
[PD-0227]: https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/src/Text/Pandoc/Writers/Powerpoint/Output.hs
[SED-0001]: https://git.savannah.gnu.org/cgit/sed.git/tree/doc/sed.texi?h=v4.9
[SED-0022]: https://git.savannah.gnu.org/cgit/sed.git/tree/testsuite/bsd.sh?h=v4.9
[WT-0021]: https://github.com/microsoft/terminal/blob/73948072120beb51d355b3c74b5f774a6526b277/doc/cascadia/profiles.schema.json
[WT-0039]: https://github.com/microsoft/terminal/blob/73948072120beb51d355b3c74b5f774a6526b277/doc/specs/%231595%20-%20Suggestions%20UI/Snippets.md

## 4. 예산·층별 분모와 민감도

| 읽기/층 | 배정 쌍 | 비교 가능 | A만 | B만 | 양쪽 | 모두 미완결 | 비교불가 |
|---|---|---|---|---|---|---|---|
| F/all | 8 | 7 | 0 | 1 | 4 | 2 | 1 |
| F/boundary | 6 | 5 | 0 | 1 | 2 | 2 | 1 |
| F/control | 2 | 2 | 0 | 0 | 2 | 0 | 0 |
| S/all | 8 | 7 | 0 | 0 | 0 | 7 | 1 |
| S/boundary | 6 | 5 | 0 | 0 | 0 | 5 | 1 |
| S/control | 2 | 2 | 0 | 0 | 0 | 2 | 0 |

| 읽기 | 배정 자리 | 과금 접근 | 절 이동 | 접근 가능한 문자 | 실제 표시 문자(반복 포함) | 패킷별 고유 표시 문자 합 |
|---|---|---|---|---|---|---|
| F | 16 | 64 | 102 | 6509235 | 270609 | 245384 |
| S | 16 | 64 | 0 | 74400 | 74400 | 74400 |

| 자료 종류 | 최소 요구 | 고유 산입 |
|---|---|---|
| new_initial_questions | 8 | 8 |
| main_official | 5 | 16 |
| adjacent_official | 5 | 10 |
| upstream_tests | 4 | 5 |
| crossdomain_official_docs | 2 | 5 |
| crossdomain_fixtures | 2 | 2 |

### 해석 민감도 — 각각 하나씩 적용한 문서 충분성 재분류

| 조건 | 읽기 | 배정 | 비교 가능 | A만 | B만 | 양쪽 | 모두 미완결 | 비교불가 |
|---|---|---|---|---|---|---|---|---|
| P1 내장 옵션·기존 호출 불변만 허용 | F | 8 | 7 | 0 | 0 | 4 | 3 | 1 |
| P1 내장 옵션·기존 호출 불변만 허용 | S | 8 | 7 | 0 | 0 | 0 | 7 | 1 |
| 최초 태그·본문에 Pandoc 없는 P1 제외 | F | 7 | 6 | 0 | 0 | 4 | 2 | 1 |
| 최초 태그·본문에 Pandoc 없는 P1 제외 | S | 7 | 6 | 0 | 0 | 0 | 6 | 1 |
| J1 최종 JOIN 성공까지 필수 | F | 8 | 7 | 0 | 1 | 3 | 3 | 1 |
| J1 최종 JOIN 성공까지 필수 | S | 8 | 7 | 0 | 0 | 0 | 7 | 1 |
| 사후 J2 이질 EventData/UserData 전체 실행 필수 | F | 8 | 7 | 0 | 1 | 3 | 3 | 1 |
| 사후 J2 이질 EventData/UserData 전체 실행 필수 | S | 8 | 7 | 0 | 0 | 0 | 7 | 1 |
| P4 최종 PDF 전체 성공까지 필수 | F | 8 | 7 | 0 | 1 | 3 | 3 | 1 |
| P4 최종 PDF 전체 성공까지 필수 | S | 8 | 7 | 0 | 0 | 0 | 7 | 1 |

민감도는 주 판정을 고치지 않는다. P1/J1/P4 해석 분기는 공개 전 protocol에 있었다. J2의 이질 EventData/UserData 전체 실행은 사후 새로 알려진 조건을 적용한 별도 엄격 분석이다. P1 제외는 모집 민감도다. 이 행들을 합산하거나 동일 관측처럼 취급하지 않는다.

## 5. 판별할 수 있는 것과 판별할 수 없는 것

**이 제한된 공개 자료 묶음에서는 인접 링크의 문서 근거 이득이 읽기 단위에 따라 달랐다.** 같은 후보 목록에서 F는 P1 한 건만 B 단독 완결이고 S는 그런 건이 없다. F의 A 단독 완결은 0건이다. 이것은 이 모집·순위·구간 규칙에서 관측한 근거 가용성의 차이이며, 인접 정책의 일반 우월성이나 동등성의 추정이 아니다. 전체 원 사용자 실행 성공은 주 지표가 아니다.

비교 가능한 F 7쌍에서 A는 4/7, B는 5/7의 문서 완결이다. 경계 5쌍은 A2/5·B3/5, 대조 2쌍은 양쪽2/2이다. S의 비교 가능한 7쌍은 양쪽0/7이다. P3의 두 비교는 인접 연구판을 고정하지 못했으므로 제외했다. 8개 배정 쌍 또는 16개 배정 자리를 분모로 제시할 때에도 그 공석을 패배로 처리하지 않는다. F의 승패가 갈린 쌍은 1개이고 B가 1/1이다. S의 승패가 갈린 쌍은 0개여서 그 안에서의 승률은 **산출 불가**다. 독립 사용자 집단의 효과 크기나 유의확률은 산출하지 않았다. [주 판정](judgments.jsonl), [16쌍](pairs.csv), [자동 집계](evidence/derived/metrics.json).

파일에서 발췌로 바꾸면 16개 정책·질문 자리 중 9개가 완결에서 미완결로 바뀐다. 질문 수준에서는 J1·J2·J4·P1·P4의 5개 행이 바뀐다. J3·P2는 양쪽 읽기 단위에서 미완결이고 P3는 양쪽 비교불가다. 고정 후보가 같으므로 이 전환을 파일 선택 변경으로 설명할 수는 없다. 그러나 표시한 문자·절 이동·사람의 시간은 같지 않다. F에서 접근 가능한 문자 합은 6,509,235자지만 실제 표시한 것은 반복 포함 270,609자이며, S는 74,400자다. F에는 102번의 추가 절 이동이 있고 S에는 없다. 따라서 비용을 “파일 접근 네 번”으로만 나타내면 F의 추가 독해 자원을 숨기게 된다. [원 접근 로그](evidence/packet-access/), [구간 규칙](protocol.json).

### 충분한 근거를 못 찾은 경우와 패킷에 충분한 근거가 없는 경우

초기 독자와 사전 별도 근거 대조 사이 완결 변경은 **0건**이다. 이번 기록에서 “허용된 패킷에 충분한 근거가 있었는데 초기 독자가 완결로 판단하지 못했다”고 확인된 자리는 0개다. 이는 그런 실패가 없다는 보편적 증명이 아니다. F에서 미완결인 J3는 C1 추가 연산은 지지하지만 필수 Bash 경계가 부분이고, P2는 원 import와 같은 결과를 잇는 근거를 찾지 못했다. S에서는 J2의 null/배열 순회, J4 B의 입력 구조, P4의 필터 단계 같은 일부 단서가 있어도 전체 필수 조건을 모두 지지하지 못했다. 관측된 불충분과 기술적 불가능성을 구분한다. [초기 32판정](evidence/initial-judgments.jsonl), [사전 변경 원장](evidence/audit/pre-outcome-changes.jsonl), [사후 별도 의미 검토](evidence/resume2/semantic-review.md).

F 완결 9자리에서 문서의 깊은 절을 직접 인용할 수 있었던 것이 S에서 차단되는 사례가 핵심이다. 예를 들어 P1 B는 knitr `plot.R`의 문자13900–18600에 있는 함수 경계를 이용한다. P4는 Pandoc 매뉴얼의 문자188840–192200에 있는 YAML 절을 이용한다. 최초 어휘 일치 주변의 한 구간은 이 절들을 제공하지 않는다. “S에서 못 찾음”은 그 파일 전체에 근거가 없다는 뜻이 아니다. 첫 일치가 도입부·라이선스·다른 용례일 수 있는 현재 추출 규칙의 성질까지 포함한 결과다. [knitr 고정 구현](https://github.com/yihui/knitr/blob/01bf7eff974903d1498e76e92a3e4b3bf9273cf5/R/plot.R), [Pandoc 고정 매뉴얼](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/MANUAL.txt).

### 가장 불리한 해석으로 다시 읽기

P1의 주 해석은 공개 전부터 전역 설정 또는 한 번 등록한 helper를 허용했다. 그러나 제안된 helper를 정의하기만 하면 기존 `knitr::include_graphics(...)`가 자동으로 바뀌는 것은 아니다. 기존 호출을 helper 이름으로 바꾸어야 한다. 내장 옵션만 허용하거나 기존 호출을 전혀 바꾸지 않는 해석에서는 F B 단독 이득이 사라진다. P1을 최초 Pandoc 연관성이 없는 모집 사례로 제외해도 남은 6개 비교 가능 F쌍의 B 단독 이득은 0이다. 이 두 민감도는 유일한 양성 결과가 얼마나 좁은 조건에 매여 있는지 보여 준다. [사전 P1 해석](protocol.json), [원 최초 질문](https://stackoverflow.com/revisions/32603E8D-E453-4BCB-895B-83AFBE3FB468/view-source), [별도 의미 검토](evidence/resume2/semantic-review.json).

J2의 F 완결도 원문이 명시한 `.Event[]`와 Data 형태에서의 조건부 변환 근거이다. 실제 전체 로그의 envelope와 EventData 없는 사건까지 무조건 처리했다는 주장이 아니다. 사후 자기답에는 UserData만 있는 사건과 원 설명의 수정이 나타난다. 이를 새 필수 조건으로 넣으면 두 F 자리를 미완결로 읽는 엄격 민감도가 필요하다. J1에서 최종 JOIN 복구, P4에서 최종 PDF 전체 실행까지 요구하는 경우도 사전 등록한 좁은 진단/파싱 기준과 구분했다. 표4의 민감도는 각각 따로 적용했으며 합산하지 않는다. [J2 최초 자기답](https://stackoverflow.com/revisions/CE0C3B2C-23EA-43DE-8F89-4B01A7CC654A/view-source), [수정 자기답](https://stackoverflow.com/revisions/5931D56D-480F-4826-9124-71C9BDE946CB/view-source).

## 6. 밀려난 절, 신규 제약, 공개 후속의 귀속

경계 요청 6건의 교체는 A3·4 두 파일과 B3·4 두 자리, 총24자리로 보존했다. J2의 B는 jq `from_entries` 원 시험을 밀어내지만 남은 매뉴얼이 같은 연산을 설명한다. J3는 jq argv 소비 구현을 잃고 Terminal 설정 schema를 얻어도 Bash 문제를 해결하지 못한다. J4의 AWS 예제는 입력 구조를 확인하지만 원 질문에 없던 Iops를 채우지 못한다. P1에서만 knitr 함수 입력 연결을 얻어 주 완결이 달라진다. P2의 CeTZ 소스는 WASM 자원 요구를 드러내지만 Pandoc resolver 성공을 제공하지 않는다. [24자리 밀림 원장](displacement.csv), [원 절 대조](evidence/resume2/source-audit.md).

승패는 같으나 **필수 실패 조건이 제거됐다**고 확정할 자연 요청은 찾지 못했다. 추가 구조 정보·시험·제약을 얻은 경우는 있으나 제거된 실패로 세지 않았다. 반대로 “외부 의존을 알기 위해 언제나 인접 도구 링크가 필요하다”는 주장은 Pandoc 매뉴얼의 LaTeX 엔진 요구, FAQ의 글꼴/엔진 제약, Lua filter 문서의 외부 interpreter/library 설명과 맞지 않는다. 같은 주 파일 안에서도 필요한 외부 의존이 설명될 수 있다. [Pandoc PDF 설명](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/MANUAL.txt#L110-L134), [Lua filter 도입부](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/doc/lua-filters.md#L1-L44).

재개 흐름의 공개 후속은 봉인②를 원격에서 관측한 **2026-11-23T20:29:13Z 이후**에만 열었고, 그 흐름의 첫 API 요청은20:32:07Z이다. 원래 흐름은20:22:57Z의원격봉인후20:25:18Z에첫후속을열었다. 두흐름의시작시각을합치지않는다. 20개 API 응답의 실패는 0이며 8질문·5답·29revision·30일 내 댓글18개를 확인했다. 현 채택은 J2·J4·P4 3건이다. **같은 판·완전한 원 입력·필수 출력을 모두 연결한 실행 확인은 0/8**이다. 질문자 자기보고가 없다는 뜻은 아니며, 그 자기보고의 범위가 다르다는 뜻이다. [봉인 원격 관측](evidence/resume2/concurrency.json), [후속 CSV](outcomes.csv), [최초·수정·현재 연결](evidence/resume2/outcomes/evidence-details.json), [후속 검증](evidence/resume2/outcomes/validation.json).

- J1은 오류가 사라졌지만 원 JOIN을 하지 못했다는 질문자 보고다. 정상 종료를 목표 충족으로 바꾸지 않았다.
- J2는 최초 자기답의 원인 설명이 바뀌었고, 채택답은 yq 중심의 다른 경로와 한 Event 예제를 제시했다. 사전의 sed 선택이나 원 조건을 결과에 맞춰 교체하지 않았다.
- J3는 파일명 인수를 쓰는 대안의 성공 보고다. 원 JSON 내용 변수를 전달하는 방식과 .new의 실제 내용을 검증한 것은 아니다.
- J4와 P4는 채택 및 답변자 제안과 주 해석이 맞지만 질문자 실행로그가 없다.

원래흐름의추가행동집계는5답/4질문,질문자30일내댓글·자기답5/8,질문자본문수정3/8,합집합7/8이다. J4/P4의수정은답보다먼저이므로7/8을답채택뒤실행으로읽지않는다. 두흐름의60entity대조에서귀속차이는없었으며이집계는 [통합귀속감사](evidence/audit/concurrent-outcome-review.md)에남겼다.
- P1은 helper가 이미 쓰이던 방법이라는 질문자 보고다. 새 제안으로 인한 채택이나 개선 효과로 귀속하지 않았다.
- P2는 후속이 없으므로 계속 미확인이다. P3는 작동 Dockerfile 자기보고가 있으나 파일·digest·PDF가 없으므로 연구판 공석과 원 입력 결손을 해소하지 못한다.

원래 흐름의 사후 감사가 채택 시점을 미확인이라고 기록한 것은 당시 수집 범위의 한계다. 이번 재개는 공식 question timeline의 accepted_answer 항목(SO-API-0007·0011·0019)에서 J2·J4·P4의 30일 내 시각을 추가로 확인했다. 이벤트의 user는 답 작성자 메타데이터이며 실행한 사람의 증명이 아니다. 두 흐름을 새 답이나 새 성공으로 중복 세지 않는다.

이 문단의 각 귀속은 [후속 상세 보고서](evidence/resume2/outcomes/report.md)의 해당 질문 URL, 최초 답 revision, 수정 revision, 댓글 ID와 연결된다. 답변자·질문자·다른 참여자의 역할을 구분했으며, 공개 프로필로 유지관리자 여부를 추측하지 않았다. 어떤 참여자에게도 연락하지 않았다.

## 7. 독자·유지관리자·검색 결과 편집자의 후속 판단

| 질문 | 독자 | 유지관리자 | 검색 결과 편집자 |
|---|---|---|---|
| J1 | stderr 진단과 입력 소비를 먼저 관측하고 두 원 파일·기대 출력을 보존한다. | break 재현은 전체 입력과 jq 판이 있어야 가능하다. 관측용 probe와 수정 성공을 별개 시험으로 둔다. | 첫 링크는 debug와 input 절까지 이동시켜 제공하고 INDEX/JOIN 정의를 둘째로 준다. 헤더 발췌만으로 완료 표시하지 않는다. |
| J2 | Data의 Name/content 변환과 바깥 Event 형태를 구분하고 실제 결손 항목의 기대값을 확인한다. | EventData 없는 UserData 사건과 결손 content를 서로 다른 fixture로 보존할 필요가 있다. | 사전 반환은 jq 변환 절+sed 전처리 제약이다. 채택된 yq 대안은 사후 별도 경로로 표시하며 사전 sed 선택을 바꾸지 않는다. |
| J3 | 현재 제안의 argv를 기록하고 내용 문자열 인수와 파일명 인수를 구별한다. | --argjson 수신 시험과 Bash 인용 시험은 별도다. 파일 인수 대안 성공을 원 내용 변수의 성공으로 합치지 않는다. | 주 반환 링크 두 개에도 Bash 근거가 빠졌다고 표시한다. Terminal schema를 더 상단에 놓는 것만으로 해결되지 않는다. |
| J4 | 태그 이름을 VolName으로 고정하고 누락 Iops는 null로 구분해 출력한다. | 다른 tag와 absent-Iops를 포함한 입력 fixture를 확보해야 실제 데이터 회귀를 검증한다. | jq scope/괄호 절을 먼저, 발행자 입력 구조 예제를 둘째로 제공한다. EMR 결과는 같은 EBS 어휘라도 제외 근거를 표시한다. |
| P1 | 기존 knitr::include_graphics 호출을 helper 호출로 바꾸는 수단을 받아들일지, 대체 파일이 있는지 확인한다. | 외부 파일 선택 API의 auto_pdf 범위와 출력 hook의 확장자 표기 옵션을 분리해 문서화할 수 있다. | 반환 첫 링크를 include_graphics 실제 절로 고정한다. PowerPoint writer 링크는 출력 형식 인식만 보완하며 실행 보증으로 쓰지 않는다. |
| P2 | 원 @preview import와 local a를 유지한 입력으로 실패 단계를 분리한다. | Pandoc resolver, Typst library 함수, WASM plugin 지원을 각각 재현해야 한다. | 두 링크는 지원 범위와 라이브러리 사용법을 주지만 해결 링크로 표시하지 않는다. 버전 차이를 링크 옆에 남긴다. |
| P3 | 작동했다는 Dockerfile과 image digest, 원 template·입력을 먼저 확보한다. | 원 의존의 image build·mount·entrypoint를 고정한 회귀 fixture가 필요하다. | Pandoc 인수 설명과 과거 고정 Docker README를 함께 주되 최신 안정판 조건 미충족과 사후 반환이라는 표지를 붙인다. |
| P4 | title scalar의 의미값을 유지하며 YAML quoting을 적용한다. | 파싱과 필터/PDF 전체 실행을 별개 gate로 다룬다. | YAML 절의 실제 문법 문장을 반환한다. 매뉴얼 파일 제목과 첫 1200자만으로 답을 완결했다고 표시하지 않는다. |


## 8. 다른 분야의 반례와 적용 한계

**GDAL/PROJ:** 새 명명 사례는 warp의 수직 보정이다. 고정 GDAL3.10.0 주 문서는 자동 수직 변환의 단일 밴드 조건과 `-novshift`를 직접 설명한다. 대응 상류 fixture는 100인 한 픽셀과 상수20 GTX 그리드에서 기대120을 검사한다. 선택적 결손 그리드 시험은 100을 유지한다. PROJ9.5.1 문서는 자원 탐색 순서와 `@` 선택적 결손의 의미를 더 구체적으로 설명한다. 따라서 주 설명만으로 충분한 조건과 실제 자원을 확보해야 완성되는 조건을 나눌 수 있다. [GDAL 주 문서](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/doc/source/programs/gdalwarp.rst#L624-L652), [새 상류 fixture](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/autotest/utilities/test_gdalwarp_lib.py#L1865-L1935), [PROJ 자원 탐색](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/docs/source/resource_files.rst#L19-L82), [선택적 그리드](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/docs/source/operations/transformations/vgridshift.rst#L23-L45).

기존 환경의 GDAL3.10.3/PROJ9.6.0으로 수행한 별도 보조 실험은 한 밴드100→120, 두 밴드100유지, novshift100유지, 선택적 결손100유지, 필수 그리드 결손 예외의 5조건 모두 기대와 일치했다. 일부는 상류 fixture의 재구성이고 일부는 문서로부터 만든 연구 변형이다. 고정판 상류 테스트 실행이나 실제 geoid 정확도 검증으로 주장하지 않는다. [명령·입력·기대·실제값](evidence/resume2/crossdomain/gdal-runtime.json).

**Sphinx/Graphviz:** 새 사례는 inheritance-diagram의 클래스·캡션과 PNG/SVG fixture이다. 주 문서는 어떤 클래스를 지정하고 캡션을 넣는지 설명한다. native Graphviz 실행 파일과 출력 renderer 지원은 별도 확인이 필요하다. 상류 시험의 `if_graphviz_found`는 명령을 시작할 수 있는지 확인하지만 `check=False`라서 gate 통과만으로 정상 종료나 SVG 지원을 보증하지 않는다. 로컬 Graphviz2.42.4의 작은 DOT→SVG probe는 성공했으나 Sphinx/docutils/pytest 환경이 없어 Sphinx 상류 테스트는 실행하지 않았다. [상속도 문서](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/doc/usage/extensions/inheritance.rst#L11-L42), [새 PNG/SVG 시험](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/tests/test_extensions/test_ext_inheritance_diagram.py#L156-L262), [실행 기록](evidence/resume2/crossdomain/graphviz-runtime.json).

이 두 지명 사례는 신규 검색 적중·8요청·32자리·16쌍에 넣지 않았다. 096의 OSR OnlyBest/BETA2007 또는 일반 graphviz/text-cache 예제를 다시 사용하지 않았다. 다만 공통 gate `sphinx/testing/fixtures.py`는 096에서 이미 읽은 보조 파일이라 재사용을 명시하고 신규 최소개수·새 fixture에서 제외했다. 문서·구현·시험이 같은 저자 계보를 공유할 수 있으므로 고유 파일 수를 독립 연구 수로 바꾸지 않는다. [계보·버전·새 fixture 범위](evidence/resume2/crossdomain/report.md), [보조 파일 산입 검증](evidence/resume2/crossdomain/validation.json).

## 9. 모집·눈가림·자료 수의 자가검산

모집은 2025-07-01~12-31 UTC의 현재 jq/pandoc 태그 검색 결과를 생성시각, 숫자 ID순으로 정렬했다. 프레임은 jq24·Pandoc15 총39행이고 최초 본문을 직접 연 것은 jq7·Pandoc15 총22건이다. 각 태그의 경계3·대조1이 채워져 2026Q1 보충은 사용하지 않았다. 이전68 ID와 겹치는 선정 ID는 없고, 이미 답을 읽은 질문을 새 적중으로 넣지 않았다. 본문의 기존 참고 질문/블로그는 같은 사건 재게시 증명이 아니며 독립성 미확인으로 남겼다. jq 현재 제목24개의 최초본문 전 노출은 모집 단계의 실제 이탈로 기록했다. J4의 선두 jq 표기 변화 외 선정 제목은 같았고, 답·점수·댓글·채택은 그때 보지 않았다. P1의 현재 태그와 최초 태그 차이는 표1과 민감도에 남긴다. [프레임](frame.csv), [모집 고정 규칙](protocol.json), [범위](SCOPE.md).

4개 모델 읽기 문맥에 Latin square로 배정했고 같은 질문의 네 패킷은 다른 문맥이었다. 파일 URL은 출처 증명을 위해 보였으므로 정책을 추측할 가능성까지 제거한 눈가림이라고 주장하지 않는다. OS 차단도 아니며 모델의 훈련 기억은 관측할 수 없다. 선행 질문에서 같은 파일을 본 자리는24/32이고 같은 질문의 다른 경로를 먼저 보았다고 선언한 주 자리는0이다. 주 지표를 독립적인 사람의 발견률이 아닌 패킷 안 근거 가용성으로 한정한다. [배정](evidence/assignments/), [구조 검토](evidence/audit/independent-integrity-review.json).

초기 판정은 32자리·60조건·115인용이고, 각 인용은 허용 원 파일의 문자/바이트 경계 안이며 첫 판정 이전에 표시된 구간으로 덮인다. 재개 중 이전 세션의 봉인②가 원격에 나타난 후 중복 읽기를 즉시 중단하고 격리했다. 그 부분 판정과 접근은 주 지표·주 비용에 포함하지 않는다. 이후 의미 검토는 정책과 기존 판정을 아는 별도 모델 문맥이며 사람이 한 검토가 아니다. 그 검토의 변경 권고도0이다. [격리 기록](evidence/resume2/concurrency.json), [중복 제외 자료](evidence/resume2/duplicate-reading/), [별도 의미 검토](evidence/resume2/semantic-review.json).

337개 통합 출처 원장 행 중 고유 최소개수 산입은46개다. 재개에서 감사한160행과 원래 흐름의143행, 통합 뒤 채택타임라인/실행계획의 비산입 보조기록을 함께 보존하며, 원래143행과 새보조기록은 추가 산입하지 않는다. 원 질문8, 주 공식16, 인접 공식10, 독립 상류시험5, 타 분야 공식5·fixture2이며 요구된 26개 및 각 하위 하한을 충족한다. 원 질문 추가 모집14행, 후속 답/댓글/API83행, 빈 시험·파생 시험·동일 fixture 보조 파일은 별도 비산입이다. 같은 원문을 A/B/F/S에서 다시 열어도 한 개다. 모든 산입 자료에는 고정 URL·UTC·지문·실제 확인 내용·한계·저작 계보가 있다. 전체 원문 재배포 대신 재열람 주소·짧은 필요한 근거·해시를 남겼다. 외부 본문 cache를 다시 내려받는 것은 독해 수에 추가되지 않는다. [sources.jsonl](sources.jsonl), [원문 표시 영수증](evidence/resume2/postseal-access.jsonl).

## 10. 재현·계약·검사 범위

저장소의 기존 시작판은 `01177554d0fbd33a914ea9c982c348d442d1358d`, 이번 재개 때 직접 읽은 통합판은 `daf01339d0a81a3a8f19fad43b497480aa62515f`이다. 배정 계획판은 `fcde6becc49120c5be91adf43fb5b4aa42e71d48`이다. 096의 연구 결과 입력은 `1d399f630930d2763459e16509c5224b0cded9a0`, 인계/운영 의존은 `fce8d0ded93fe1f13f2c4978ed273c1ceef32934`이다. 의존 원격은 같았고 연구 입력을 바꾸지 않았다. 원천 결과·중앙 dot-control은 수정하지 않았다. [작업 manifest](manifest.json), [재개 확인](evidence/resume.json).

① `e0cb8eaec3cbd9a7e5d40291a5a883f33473ec2f`에서 모집·조건·순위·읽기 예산과 패킷을 봉인했다. ② `5d81bcbeb5f1248fc1dd2ce2d825cf6467353673`에서 32사전 판정과 근거 대조를 봉인했다. `747359a546daf5300d82afa0904cbbf71e211202`은 동시 세션 결과를 보존하고 재개 중복 읽기를 격리한 커밋이다. ③ `866ee7a68eec0f5c7077fec364685d6039d5ca75`는 후속·밀림·다른 분야·별도 의미 검토를 저장했다. 이후 `82e21d89eb592769f6f44ed75c9937400a565641`에서 원래 흐름③ `b3d7af5a3a55eba78adc6c3bd31db7eaf9de49b1`도 병합한 원격을 인수했다. 원래 흐름32개와재개46개는서로다른감사계수집합이다. 고정URL+본문지문으로28개가겹치며원래쪽에만4개·재개쪽에만18개가있다. 32가46의부분집합이라는뜻도아니며두수를더하지않는다. 최종46에는사후의더오래된DockerREADME가있지만초기P3공석을채우지않는다. 두 흐름의 원32판정은 동일하다. 최종 합성기는 재개 감사 subset의46개만 산입하고 원래143개 원장 행은 비산입으로 보존한다. 자세한 조정은 `evidence/resume2/concurrency-stage4.json`에 있다. ④ 결과판의 SHA와 마지막 작업별/공통 검사, GitHub 원격 재열람 영수증은 마지막 단독 [HANDOFF.md](HANDOFF.md)에 기록한다. 검사 명령을 제시한 것만으로 실행했다고 세지 않는다.

저장소 루트에서 아래 순서로 재구성한다. `hydrate_ledgers.py`는 커밋된 gzip 원장을 정확한 hash로 복원한다. `restore_cache.py --all`은 등록한 고정 source archive와 원 최초 질문만 복원하며, 새 원문이나 현재 답으로 대체하지 않는다. 검증은 신규 질문 모집이나 독립 독자 실험의 반복이 아니다.

```bash
python -B docs/workstreams/research/AF-RES-100/hydrate_ledgers.py
python -B docs/workstreams/research/AF-RES-100/restore_cache.py --all
python -B docs/workstreams/research/AF-RES-100/packet_builder.py --verify
python -B docs/workstreams/research/AF-RES-100/assemble_preseal.py --check
python -B docs/workstreams/research/AF-RES-100/validate_ledger.py
python -B docs/workstreams/research/AF-RES-100/assemble_supplement.py --check
python -B docs/workstreams/research/AF-RES-100/recompute.py --check
python -B -m workbench.session check docs/workstreams/research/AF-RES-100/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

`recompute.py --write`는 원장과 `case-notes.json`, 이 설명 파일에서 필수3표·층별 집계·민감도·RESULT를 다시 만든다. `--check`는 파일을 쓰지 않고 바이트 동일성을 검사한다. 인용 115개의 위치·바이트 변환과 최초 판정 전 노출까지 함께 검증한다. 결과판 공통 검사가 개별 session을 찾지 못해 건너뛰는 경우 별도 `workbench.session check` 결과와 구분해 인계한다. [자가검산](SELF_CHECK.md).

자연 요청의 jq/Pandoc/R/Typst/Docker 원 실행은 수행하지 않았다. 전체 입력·사용자판이 없는 경우 연구자 예제로 채우지 않았다. P4는 렌더링하지 않았다. 읽은 jq/sed/knitr/CeTZ 상류 원 시험은 실행 결과로 표시하지 않았다. Sphinx 고정판 시험의 필요한 node·환경과 GDAL 보조 입력은 [fixtures.json](evidence/resume2/crossdomain/fixtures.json)에 있다. 재현 가능한 문서 충분성·밀림·손실과 실행 미확인을 구분한 상태로 이 작업을 완료한다.


### 통합 후 추가 반례와 재검토

원래흐름의자료에서도결론을더좁히는반례를읽었다. AWS describe-volumes Example1의KmsKeyId닫는따옴표결손은원문그대로의JSONparse에서오류였다. [입력구간·오류영수증](evidence/supplemental/aws-example-validation.json)은AWS실제API실패나J4원입력실패를뜻하지않는다. 공식예시의Iops값을질문자값으로복사하지않았다.

GDAL3.10.0 원시험135s의2247행은f접두사없이 `{empty_grid_gtx}`를전달한다. 일반예외assertion만으로생성한grid의빈값이실패원인이라고보증하지않았다. Sphinx8.1.3 원시험의class_info순회는각원소의membership을확인하므로허용목록5개/6개를실제전체출력개수로보고하지않았다. [고정원문·정확행·반례](evidence/crossdomain/report.md), [원시험명령과입력](evidence/crossdomain/unrun.md)에다음최소확인을남겼다. 재개GDAL보조runner는expectation_met를기록하므로재실행시종료값만보지말고5개기대일치값도함께읽어야한다.

통합작성자는J2/J4/P4의공식accepted_answer timeline을다시열어각2025-07-14 21:04:27UTC,2025-08-06 11:30:01UTC,2025-07-25 13:35:19UTC와답ID일치를확인했다. [재열람영수증](evidence/outcomes/acceptance-verification.json)은변동가능HTTP응답의새지문을남기며원응답바이트가같다고가정하지않는다. 채택행위자·실행판·완전입력·필수출력을추가로입증한것은아니다. [별도통합귀속검토](evidence/audit/concurrent-outcome-review.md)는두흐름의질문8·답5·댓글18·revision29인60개공유entity대조와세타임라인재열람을구분했다.

최종재현순서는 [REPRODUCE.md](REPRODUCE.md),실행하지않은jq/sed/knitr/Pandoc고정원시험의실제runner·입력·환경은 [upstream-execution-plan.md](evidence/audit/upstream-execution-plan.md)에있다. 공통검사는수정없는결과SHAcheckout을owned cache안에만들어실행하며 [run_result_checks.py](run_result_checks.py)에실제명령과기록절차가있다.

### 실제 결과판 검사

| 검사 | 실제 대상SHA | 종료값 | 범위·건너뜀 |
|---|---|---|---|
| workstream check --fetch | 8b22a47f9daaf8f6bfaaec06f441edb7c78a9ff9 | 0 | af-res-100 manifest, fetched integration/dependency pins, ancestry, conflict and owned-path checks; original research execution excluded |
| common cloud_check | 8b22a47f9daaf8f6bfaaec06f441edb7c78a9ff9 | 0 | Common gates doctor:0, acceptance:0, research-case:0, original-smoke:0, sessions:0; individual-session result {"status": "not-executed", "reason": "no_active_sessions", "count": 0, "freshness": "not_checked", "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc"} |

[실제명령·UTC·stdout/stderr영수증](evidence/result-checks.json). 이표는실제검사한SHA를명시하며,영수증추가후속커밋을소급해검사했다고하지않는다. 최종GitHub재열람과마지막검사대상은HANDOFF에기록한다.

## 가장 중요한 남은 불일치·약점

| 가장 중요한 불일치·약점 | 다음에 열 자료 또는 실행할 입력 | 어떤 관측이면 결론을 바꿀지 |
|---|---|---|
| 유일한 B 이득 P1은 helper 호출 변경 허용과 현재 Pandoc 태그 모집에 의존한다. 최초 본문·태그에는 Pandoc이 없고 실제 SVG/EMF·helper·PPT가 없다. | 원 helper 구현, 실제 JPEG/SVG/EMF 파일과 같은 R Markdown 호출·knitr/rmarkdown/Pandoc 판을 고정한 입력. 기존 호출 불변 조건과 helper 조건을 나누어 실행한다. | 기존 호출을 바꾸지 않고 내장 옵션만으로 같은 선택이 되거나, helper 조건에서도 원 출력이 실패하면 P1의 해석 및 유일 이득의 범위를 바꾼다. |
| F/S는 같은 네 파일 접근이지만 표시량·절 이동·시간이 다르며 24/32자리에 선행 공유파일 노출이 있다. S의 첫 일치 규칙과 사람의 독립 발견률은 분리되지 않았다. | 동일 원 질문·고정 파일에서 절 선택 방식과 표시량/시간을 별도 배정한 새 맹검 문맥. 현재 원장은 `recompute.py --check`로 먼저 보존 확인한다. | 같은 표시 예산·독립 문맥에서도 P1의 이득이나 9자리 손실이 유지/반전되는 관측이 나오면 전달 단위에 관한 해석을 좁히거나 바꾼다. |
| 같은 판·완전한 원 입력·필수 출력 실행 검증은 0/8이고 P3는 고정 연구판 공석이다. J2 사후 UserData 사건도 원 조건부 변환 밖에 있다. | P3의 취득한 스레드에 없는 작동 Dockerfile·image digest·custom template·두 filter·원 Markdown, J2의 원 Security.json/evtx와 전체 envelope. 고정 GDAL/Sphinx node는 fixtures.json 명령대로 준비한다. | 원 자료로 최신 안정 소스와 실행이 연결되면 P3 비교 가능성을 재연구한다. 같은 입력의 성공·실패가 주 조건과 어긋나면 문서 충분성과 원 실행의 관계를 수정한다. |
