# E01 최종 출판본·정오표 경로 재확인

## 판정

**최종 출판본의 해당 표 값과 정오표는 이번에도 확인하지 못했다.** DOI에서 공식 APA 경로로 이동한 실제 요청은403이었다. Crossref가 `content-version: vor`로 명시한 최종 PDF 경로를 확인했으나 HTTP·HTTPS 모두403을 반환했다. 저자 소속기관 PDF와 기관 저장소는 timeout/502/503으로 막혔다.

따라서 현재 유지하는 관측은 **이미 읽은54쪽 저자 원고의 Appendix B Table B2에4.75가 인쇄되어 있고, 공개 SAV의 Cond0/TimeP0/KPre 평균은4.573275862라는 사실**이다(CD-P01-VIS, CD-D01). 최종 출판본 오류, 오타, 판 차이 또는 데이터 오류 중 어느 설명인지 확정하지 않는다. 이번 경로 확인은 같은 DOI의 재확인이며 고유 저작 수·선정·효과 분석을 바꾸지 않는다.

## 직접 요청 결과

시각은 native 요청 시작 UTC이다. `web` 도구의 정확한 초는 보존하지 못했으므로 해당8행은 날짜 정밀도로 기록했다. 실제 HTTP 상태와 도구 오류 표현은 구별했다. 모든15개 접근 행은 `sources.jsonl`의 `CD-VOR-W01`–`W08`, `CD-VOR-N01`–`N07`에 있다.

| 경로 | 직접 URL | native UTC·상태 | 도구 경로와 실패 단계 | source ID |
| --- | --- | --- | --- | --- |
| DOI→공식 APA | https://doi.org/10.1037/edu0000433 → https://doi.apa.org/doi/10.1037/edu0000433 |02:28:39.259873;403, HTML960 bytes | DOI open은 redirect 뒤 도구500/accessibility error; APA landing 직접 open도 접근 불가. 논문 본문 앞에서 실패 |W01/W02/N01 |
| APA PsycNet record | https://psycnet.apa.org/record/2019-71474-001 |02:28:39.261330;403, HTML960 bytes | web 도구는 restricted URL fetch failure. 정오표 표지·record correction 필드를 읽지 못함 |W03/N03 |
| Crossref DOI 메타데이터 | https://api.crossref.org/works/10.1037/edu0000433 |02:28:39.260594;200, JSON2955 bytes | `link`의 VOR 경로와 `relation`, 갱신 필드를 직접 읽음; 본문 열람이 아님 |N02 |
| Crossref가 연결한 VOR PDF | http://psycnet.apa.org/journals/edu/112/7/1320.pdf |02:29:18.420413;403, HTML960 bytes | web 도구는 HTTPS 주소로 접근 불가. PDF 바이트가 아니므로 표 대조 불가 |W07/N05 |
| 같은 VOR PDF의 HTTPS | https://psycnet.apa.org/journals/edu/112/7/1320.pdf |02:29:18.421168;403, HTML960 bytes | 공식 PDF 주소 그대로 요청; 본문 앞에서 실패 |W08/N06 |
| 저자 소속기관 PDF | https://www.psy.uni-muenchen.de/ffp/publications/_data/2019/journals/bichler_schwaighofer2019.pdf |02:29:18.421885;503, text98 bytes | web TimeoutError; native upstream remote connection failure |W04/N07 |
| 공저자 소속기관 저장소 | https://orbilu.uni.lu/handle/10993/45413 |02:28:39.261900;503, text98 bytes | web502 Bad Gateway; native upstream remote connection failure |W05/N04 |
| 저자 소속기관 출판목록 | https://www.psy.uni-muenchen.de/ffp_en/publications/index.html |web만 요청, 정확한 초 미보존 | 도구400 Timeout fetching; 링크 본문 직접 재확인 불가 |W06 |

이때 Crossref 응답의 SHA256은 `92b2463ffdfd243614354f35fab3064d44e1a7903c2726f665c8ea94427ede40`이다. `link`는 공식 PDF를 VOR로 표시하고, `relation={}`, `update-to`/`updated-by` 필드는 없으며 deposit은2024-02-05T22:48:23Z이다. **갱신 메타데이터의 부재가 정오표 부재를 증명하지는 않는다.** 각 실패 응답의 바이트 수·SHA256은 source 행에 남겼으며 오류 HTML이나 원문 전체를 재게시하지 않는다.

## 정오표 검색 범위

2026-11-23에 `search_service_web_run`의 `system1_search_query`를 사용했다. 첫 묶음의 두 질의와 둘째 묶음의 두 질의는 아래와 같다. 새 연구 선정 검색이 아니라 이미 정한 한 논문의 판 대응 점검이다.

| 묶음 | 실제 q 문자열 | 추가 domains 인자 | 응답 범위·제한 |
| --- | --- | --- | --- |
|1 |`site.apa.org "10.1037/edu0000433"` |없음 |묶음 전체의 검색 결과10개와 DOI open 오류가 반환됨. 도구가 개별 질의별 결과를 분리하지 않아 각 질의의 정확한 반환 수를 만들지 않음 |
|1 |`"How Working Memory Capacity and Shifting Matter" correction erratum` |없음 |같은 묶음. 기관 metadata·저자 원고·서지/복제 페이지가 반환되었으나 해당 논문 정오표를 특정하지 못함 |
|2 |`"edu0000433" (correction OR corrigendum OR erratum)` |`["apa.org", "psycnet.apa.org"]` |묶음 전체 검색 결과10개와 저자 출판목록 open 오류가 반환됨. 일반 APA 수정 정책은 해당 논문 정오표로 보지 않음 |
|2 |`"Bichler" "Schwaighofer" "Stadler" "Correction" "working memory"` |없음 |같은 묶음. 관련 논문·서지·일반 정책 결과만으로 정오표가 없다고 단정하지 않음 |

묶음1의 응답 표시 순서는 `turn307591380search0,1,2,8,9,3,4,5,6,7`, 묶음2는 `turn577655562search9,0,1,2,3,4,5,6,7,8`이었다. 이 식별자는 검색 도구 영수증이며 고유1차 저작 수가 아니다. 검색 결과에 보인 ORBilu의 publisher postprint/요청 가능 문구나 LMU 원고의 non-copy-of-record 문구를 최종 PDF 직접 열람으로 승격하지 않았다. 검색 결과의 긴 초록은 저장하지 않았다.

## 남은 첫 행동과 판단이 바뀔 조건

재개 시 가장 먼저 **공식 최종 출판본** `https://psycnet.apa.org/journals/edu/112/7/1320.pdf`를 정상적으로 읽을 수 있는 경로에서 열고, 해당 무압박 문제풀이군58명의 사전평균 표·본문 및 연결 정오표를 대조한다. 필요 입력은 DOI `10.1037/edu0000433`, 조건 `Cond=0, TimeP=0`, 변수 `KPre`, 원고 Table B2의4.75, 공개 SAV 평균4.573275862이다. 최종판의 표 번호가 원고와 다르면 제목·행 이름·조건으로 대응해야 한다.

공식 최종판이4.573 계열로 고쳤다면 현재 관측은 원고판 불일치로 더 좁힐 수 있다. 최종판도4.75이고 동일 코호트·변수·파일판임이 확인되면 출판표와 공개자료의 불일치로 말할 수 있으나 어느 쪽이 잘못됐는지는 정오표·계산 정의가 추가로 필요하다. 이번에는 그 대조가 **접근 실패로 미실시**였으며 값이나 기존 SAV를 수정하지 않았다.

## 범위와 실행 기록

- 새 표본·선정·효과 분석 없음. 동일 DOI 미러·메타데이터·실패를 고유 저작에 더하지 않음.
- 새 source15행, 그중 본문 접근 실패14행·Crossref 메타데이터 직접 열람1행; 고유1차 저작 증가0.
- 첫 native 스크립트는 `requests` 모듈 부재로 import 단계에서 종료되어 실제 URL 요청이 일어나지 않았다. 이어 Python 표준 라이브러리 `urllib.request`로 위 요청을 실행했고 각 스크립트 종료코드는0이었다. 실제 네트워크 실패는 위 HTTP 상태로 기록했다.
- 전역 RESULT/수용 원장/고유 저작 집계는 이 작업에서 수정하지 않았다. 이 파일과 해당 stream의 sources 추가만 수행했다.
