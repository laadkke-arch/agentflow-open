# AF-RES-033 SELF_CHECK — 질문별 반증·분모·미확인

작성 기준은 관측 묶음 원격 [889c5e792a3db3856bf5be8c90d9486490ce8677][observation]과 그에 연결된 봉인 입력·원 검색·144개 대응이다. **현재 원장에서는 S/R 어느 쪽도 상위 1개·3개에서 고정 부분 목표를 인용 완료한 수신 설계가 없다. 전체 18문서를 읽으면 R05–L06 한 쌍이 지지되지만, 두 원 검색 모두 상위 3개에서 놓쳤고 그 원리는 수신 최초 요청에 이미 있다.** 새 원리 발명, 설계자의 실제 미인지, 실제 채택 또는 자유 웹 발견의 성공으로 세지 않는다.

이 문서는 결과의 의미와 현재 원장 수를 점검한다. 작성 시점의 evidence/recount.json과 분야별 검사 기록을 읽었고, 작성자가 읽기 전용 Python으로 현재 CSV/JSONL의 핵심 건수도 재계산했다. 최종 작업트리 전체 해시/ID 조인, 고정 결과 SHA 원격 재독, 마지막 workbench.session check 영수증은 아직 작성되지 않았다. 아래 ‘최종 검사와의 경계’에 예정 경로를 구별했으며, 최종 HANDOFF가 실제 대상 SHA·종료 코드로 확정해야 한다.

## Q1–Q7: 주장과 실제 반례

아래의 줄은 별도 표시가 없으면 원장에 해시가 붙은 고정 추출본의 1-based 행이다. PDF는 인쇄/물리 페이지를 함께 쓴다. 직접 원문 판독, 별도 문맥의 원문 재검, 구조·해시 검산은 서로 다른 근거다. 이 작성자는 제공 원문 감사와 통계 48행 판독, 현장/후속 분석을 맡았고, 다른 두 분야 및 5행 비판 판독은 해당 별도 문맥의 기록을 읽어 통합했다. 세 분야 144행을 이 문서 작성 때 새로 독립 판독했다고 주장하지 않는다.

| 주장 | 직접 읽은 근거 주소·위치 | 결론이 틀리는 조건 | 실제로 찾아본 반례·확인 결과 | 남은 미확인·다음 자료 |
| --- | --- | --- | --- | --- |
| **Q1 — 수신 출발점:** 2020–2024 메타데이터 원장 3,415건에서 사전 생성 시각/번호 순의 최종 선정 접두부 23건을 확인해 Rust 4·Kubernetes 4를 택했다. 현재 8개는 모두 2020년 1월이며 전체 설계 3·부분 설계 5다. 제출 당시 opening head에 연결된 본문 8개를 확인했다. | [R01 최초본][r01] L9–33, [R03 최초본][r03] L128–164·336–360, [R04 최초본][r04] L84–97·112–144, [R05 최초본][r05] L98–117, [R06 최초본][r06] L208–223·353–356 등. 전 8개 원문/개별 위치는 inputs.jsonl R01–R08와 judgments/*-attempts.jsonl. 출처 연결은 [initial-source-binding-audit](evidence/initial-source-binding-audit.md)의 8행과 checks.json의 head/tree/path/blob. [resume-input-audit](evidence/resume-input-audit.md)의 23=8+15 재검. | 첫 생존 커밋을 최초 제출 head로 잘못 취급했거나, 접두부의 더 이른 적격 제안/파일을 누락했거나, 결과를 보고 scope를 바꿨다면 표본 주장이 무너진다. opening head 검증은 개인이 처음 쓴 사적 초안을 증명하지 않는다. | 사전 감사는 ‘09시 초안 A→10시 완성 B→11시 PR 생성’의 반례와 임의 blob/잘못된 경로 결합을 실제 복원기 검사에 넣었다. 생존 이력의 불확실성을 보존하고 GH Archive의 opened 사건 및 tree/blob 연결로 최종 8개를 확인했다. 15개 접두부 제외도 최초 추가 제안 경로 부재를 확인. 전체/부분 할당은 [본문 전 보완](evidence/pre-body-amendment.md)으로 미리 정했고 최종 quota displacement는 0이다. | 2020년 초의 복원 가능한 접두부라는 선택 편향과 R01/R03의 공유 문제 맥락은 남는다. 5개 연도 균등 표본이나 독립 실험 8회로 해석하지 않는다. 판정을 바꿀 첫 자료는 checks.json이 연결한 해당 hourly opened-event 보존본의 다른 head 또는 접두부 제외 PR의 새 제안 added/renamed diff다. |
| **Q2 — 제공 분야의 닫힌 집합:** 수신 본문 전에 고정한 영어권 발행처·기간·상위 발견 목록·제목/URL 정렬에 따라 분야별 6, 총 18개 작품을 봉인했다. 현재 전이 가능성과 당시 이용 가능성은 별도다. | [SCOPE §4](SCOPE.md), [corpus 봉인](evidence/corpus-seal.json), corpus.jsonl L01–L06/S01–S06/T01–T06. 실제 원문 예: [VPL L06][l06] L3·64–106, [ABS S03][s03] ¶24.107·24.118–129, [TransLink T04][t04] 2018-06판 인쇄 p7·9·44. [제공 재개 감사](evidence/resume-donor-audit.md)는 18개 body/raw 신원과 추출 경계를 점검했다. | 수신 조건을 본 뒤 유리한 발행처/문서를 골랐거나, 발견 목록을 공식 사이트 전수로 부르거나, 번역·이전판·재요청을 새로운 문서로 세면 독립 표집/분모 주장이 틀린다. 날짜 없는 현재 HTML을 2020년에도 같은 조항이었다고 간주하면 역사적 가용성이 과장된다. | TX14는 T06의 이전판으로 합쳤고, ABS 여러 판/표현은 S03 한 작품, F03의 세 캡처·F04의 목록/두 XLSX는 각각 한 작품으로 묶었다. L04의 HTTP 202 실패와 공식 웹 리더의 실질 본문을 구분했다. T02 제목 한 행 잔존을 실제 범위 위반으로 발견했고 원값을 보존했다. 당시 가용이 확인된 고정판은 T04 1/18뿐이며 10개 후발·7개 미상이다. | 연구자가 고른 닫힌 발행처·발견 목록이지 다른 분야 전체의 대표 표본이 아니다. 최신판도 고정 발견/링크 범위에서 최신이다. 역사적 결론을 바꿀 첫 자료는 L06의 2020년 1월 이전 동일 두 분류 절 보존본 또는 S03의 당시 정확 판·개정 절이다. 단순히 오래된 기관이라는 사실은 대체 근거가 아니다. |
| **Q3 — 표현 변경의 원 반환:** 같은 18문서·영어/80토큰 상한·BM25·200토큰 창 규칙의 16검색을 봉인했다. 전체 점수 288행, 0점 문서 점수행 8, 빈 검색 0, 상위 반환 48슬롯/37고유 문서-창이다. 엄격 상위1·3은 S/R 모두 0/8이다. | [원 순위](rankings.csv)의 모든 R01–R08×S/R×18행, [retrieval-receipt](evidence/retrieval-receipt.json), [반환창 판독](evidence/returned-window-audit.jsonl), [recount](evidence/recount.json). R05의 [수신 최초본][r05] L98–117와 [VPL][l06] L3·64–106 대응은 S10/R12로 상위3 밖이다. 원 검색은 [a2ce15d][retrieval-seal]에 후속 전에 봉인됐다. | query-author가 제공 제목/용어를 미리 봤거나, 사후 표현 수정·다른 후보·후속 답을 원 검색에 섞었거나, 문서 전체 근거를 실제 반환 한 창의 근거로 바꾸면 비교가 무효다. 0점 행과 빈 검색을 같은 단위로 세어도 틀린다. | 실제 S와 R의 길이는 동일하지 않다: S 56–78, R 64–74 raw토큰. 사전 합성 점검에서 부정어 not 제거 때문에 긍정/부정의 남은 단어가 같아지는 반례도 확인했다. R은 관계를 기술한 질의지만 이 검색기는 역할·순서·부정을 이해하지 않는다. T02 표제 제거 별도 16검색에서 순위/상위집합은 0변화, T02 포함 3슬롯의 창 해시는 변화했다. | 어떤 R 표현도 효과가 없다는 결론은 내릴 수 없다. 서로 다른 실제 길이·generic 어휘와 정해진 lexical BM25의 관측이다. 다음 판별은 같은 수신 조건으로 별도 작성자가 길이/고유 토큰 수를 맞춰 쓴 질의와 고정 역순·부정 최소쌍의 사전등록 비교다. 원 16검색과 합산하지 않는다. |
| **Q4 — 공통 단어와 전이 가능성:** 144대응의 판정은 support1/conflict9/partial50/unverified84, 필수 조건 근거 객체 504개다. 일부 역할/상태 단서와 고정 목표 전부의 지지를 분리했다. 전체 설계 support는 0이다. | [maps.csv](maps.csv) pair_id별 양측 위치/mandatory_evidence/남는 접합/새 핵심. 결정적 원문: [R01][r01] L9–10·31–33와 [MBTA T02][t02] 인쇄 p1 L14–33 및 p2–3 L63–88; [R07][r07] L260–294와 [ABS S03][s03] ¶24.120–129; [R05][r05] L98–117와 [VPL][l06] L3·64–106. | 소재 단어만 같음을 지지로 세거나, 기술명이 원문에 없다는 이유로 구조 대응을 거절하거나, 제공 쪽의 부재를 명시적 금지로 바꾸면 판정이 틀린다. 같은 기간·변수와 새 vintage 중 무엇을 동일 객체로 잡는지도 결과에 영향을 준다. | R01–T02는 대체 노선의 일부 역 생략·시간/빈도 차이가 동일 실행 보존과 충돌한다. R07–S03은 같은 객체 매핑에서 값 개정이 field 불변성과 충돌한다. 별개 vintage를 새 객체로 잡는 대안에서는 충돌이 약해지지만 생성 진리표·N+4·권위 규약은 남는다. R05–L03은 혼합 자료가 기록물 제외의 예라는 재독 후 초안 conflict를 partial로 내렸다. | 9개 충돌은 명시한 대응에 대한 충돌이며 가능한 모든 매핑의 불가능성 증명이 아니다. R05–L06은 두 목록의 차이가 복합 책 접수 허용을 함의한다는 해석에 의존한다. 명시적 허용 문장만 인정하면 partial로 내려간다. 첫 추가 자료는 VPL의 해당 복합 자료 신청 양식/접수·전달 운영 규칙이다. |
| **Q5 — 반환 밖의 더 나은 대응:** 전수 8×18 목록에서 유일한 엄격 부분 목표 지지는 R05–L06이며 S10/R12로 두 경로 모두 놓쳤다. strict 적격 질문 분모 1에서 양쪽 놓침 1/1이다. 다른 7개 질문은 이 집합에서 엄격 적격 후보가 없으므로 같은 종류의 회수 실패로 세지 않는다. | [maps.csv](maps.csv) R05–L06, [recount](evidence/recount.json) strict_all_list_support_pairs/strict_both_missed_pairs/per_recipient. [VPL][l06]의 신청 불가 L64–80와 제공관이 보내지 않을 수 있음 L82–106, [R05][r05] L98–117. 가까운 오답은 [R03][r03] L132–164·345–360와 [T04][t04] PE.3 인쇄 p44/L1836–1861의 turnover 지표. | 실제 전수 판독 없이 상위3만 읽고 나머지에 더 나은 원리가 없다고 말하거나, 부분 단서를 엄격 적격으로 합치거나, 접수/실현 분리 원리가 수신에 새로 생겼다고 하면 틀린다. | 상위 검색 밖 R05–L06을 실제로 발견했다. R03–T04의 공간 재사용 지표는 안전한 마지막 읽기/쓰기 시점 규칙이 아니어서 partial이다. 넓은 문서 기준 top1은 S5/R4, top3 S5/R5이지만 반환창 완결 수가 아니다. R05 최초 요청 자체가 API 접수와 제공자 역량을 이미 구분한다. | 엄격 지지 1건을 목록 함의 없이 읽으면 0건이 되고, ‘양쪽 모두 놓친 비율’의 적격 분모는 0이라 **해당 없음**이 된다. 성공률 0/8은 유지된다. 첫 자료는 위 VPL 접수/전달 규칙과 동일 판의 두 목록이다. 더 큰 corpus나 다른 query로 얻은 양성은 별도 사후 실험이어야 한다. |
| **Q6 — 실제 사례와 수신자의 행동:** 현장 4고유 원문·2분야·3사건과 수신 8건 후속을 확인했다. 규칙 적용·정정·후속 부분 동작은 확인되지만 제공 원리의 직접 인용·인과적 채택은 8건 모두 미확인이다. | [F01 MTA 발표][f01] Subways and buses 등 L23–30, [F02 DCP][f02] p13, [F03 v1][f03-v1] §5/L152와 [정정판][f03-current] §5/L159·배너 L75–82, [F04 v1][f04-v1]/[v2][f04-v2] MYE3!A9:O365·Correction notice!A1:A3. 수신 후속은 [R01 구현 #68404][r01-impl] 본문, [R03 후속 #2873][r03-replacement], [R07 후속 #3298][r07-replacement], [현재 AppArmor 문서][r07-doc]. 전체 연결은 [field-and-followup](analysis/field-and-followup.md). | 발표를 모든 실제 운행으로, 현재 문서를 최초 모든 조건의 구현으로, 미병합 종료를 일률 거절로, 도메인 일치 0을 사적 지식 부재로 읽으면 틀린다. 과거 교통 screenshot의 GTFS 표기를 고정 PDF보다 우선해도 틀린다. | F02의 해시 고정 PDF·로컬 렌더·동일 바이트는 **MTA Real Time**으로 일치해 GTFS 분류를 철회했다. F04는 357키 중39행/78셀 H/I만 바뀌고 J/O가 같아 최종 출력 동일성만으로 과정 정확성을 판단하는 반례다. R01 구현은 forwarding 뒤 deprecation을 미뤘다. R03/R07의 닫힌 PR은 대체 경로로 이어졌다. | 원시 실시간 feed/집계 코드를 재현하지 않았고, F04 전체 추정 모형도 재실행하지 않았다. 도메인 기계검사 1,315기록/913본문+현재 PR8의 일치0은 간접 인용·개인 지식·실제 채택 부재를 뜻하지 않는다. 다음 첫 자료는 F02의 세 날짜 보존 feed·DCP 코드, R01 #70173의 경고 도입 시험, R07 #24의 최종 변환/불변성 시험이다. |
| **Q7 — 짧은 설명·역할·반례 검토:** 설명은 원리 이름만 제시하지 않고 양측 절, 옮길 한 단계, 깨지는 조건을 붙인다. 수신 설계자·제공 운영자·반례 검토자 관점과 역할 뒤집기/근거 제거를 실제 매핑에 적용했다. | [critical-review.jsonl](judgments/critical-review.jsonl) 지정5쌍, [critical-review-notes](judgments/critical-review-notes.md)의 교란 점검. 원문은 [VPL][l06] L3·64–106, [R05][r05] L98–117; [MCL][l03] L39–57·105–115·193–219와 [R04][r04] L112–144·329–351; [F04 두 판][f04-v2] MYE3!H9:O12. 세 관점의 짧은 설명은 [field-and-followup §5](analysis/field-and-followup.md). | 짧은 설명에 실제 공급 보장·자동 복구·동일 객체 복원을 덧붙이거나, 사후 좋은 표현을 최초 질의/반환이라고 제시하거나, 교란마다 반드시 분류가 바뀌어야 한다고 강제하면 틀린다. | R05–L06의 복합 책 L106을 제거하면 support→partial, 제공관 재량을 접수 재량으로 뒤집으면 conflict다. R04–L03의 6개월 계정 이력은 공개 인프라와 승인된 동일 그룹 복원을 제공하지 않아 partial. R01–T02/R07–S03/R08–T06은 한 근거절을 빼도 다른 충돌 절이 남는 경우를 확인했다. | 5쌍은 의도적으로 선택한 취약 사례이며 전체 144행의 독립 일치율이 아니다. 판독자는 모두 같은 표시 모델의 별도 문맥이고 실제 설계자/운영자/독립 인간 검토자는 참여하지 않았다. 첫 다음 자료는 원 R05 목적을 보는 실제 설계자의 접합·오해 기록과 VPL 운영자의 복합 책 접수 규칙 설명이다. 사전 과제·평가 기준·시간 비용을 고정해야 유용성 실험이 된다. |

## 원문 수·중복·단위 재계산

작성자가 현재 sources/frame/rankings/maps와 evidence/recount.json을 읽고 일회성 읽기 전용 Python으로 아래의 단순 건수를 재계산했다. 실행은 종료 코드 0이었으며 다른 파일은 쓰지 않았다. 이 좁은 재계산을 최종 전체 해시/모든 ID 조인 검사로 부르지 않는다.

| 단위 | 현재 원장 수와 구성 | 세지 않는 것·주의점 |
| --- | --- | --- |
| sources.jsonl 행 | 61행: counted_minimum=true 30, false 31 | 61행 모두를 실질 직접 열람 최소수로 표현하지 않음. 발견/제외/보강의 지위는 각 행의 read_status·kind로 구분 |
| 최소 고유 외부 원문 | 30 = 수신8 + 후보18 + 현장4. 최소 산입 duplicate_group 30개 모두 고유 | AF-RES-010/029 과거 표본·후보, 검색 요약, 같은 원문의 PDF/HTML/이전판·재요청·연구자가 만든 표를 추가하지 않음 |
| 분야별 후보 | 도서관6 + 교통6 + 통계6 = 18 | 당시 이용 가능 문서 수와 다름. 고정판 가용1/후발10/미상7 |
| 현장 | 4작품, 교통2·통계2, 3사건 | F01/F02 같은 감편 과정; F03/F04 서로 다른 ONS 정정. 독립 기관/사건4회라고 하지 않음 |
| 후속 추가 원문 | OUT-DOC 3 + OUT-R* 4 = 7, 모두 counted_minimum=false | 30개 최소수를 채우는 데 쓰지 않음. 원 수신 PR 재조회도 새 수신 원문이 아님 |
| frame.csv | 3,863행 = recipient_pr 3,415 + provider_discovery_candidate 424 + provider_issuer 24 | 3,863개 원문을 열었다는 뜻이 아님. 수신 최종 선정 접두부 23=선정8+제외15를 전체 제외 기록과 구별 |
| 수신 범위 | 8개, 저장소별4; 전체 설계3(R03/R04/R06), 부분 설계5 | 질문별 집계 단위8은 통계적 독립성 보장이 아님. 모두2020년1월인 날짜순 접두부 |
| 원 검색·점수 | 16검색 × 18 = 288점수행; 0점행8, 빈검색0 | 0점행8은 고유 문서8개가 아니며 빈검색8회도 아님 |
| 원 반환 | 48슬롯, 고유 candidate/window 조합37 | 동일 창의 두 경로/여러 질문 반복을 새 원문으로 추가하지 않음 |
| 대응·필수 근거 | 144고유 pair = 8×18; mandatory_evidence 객체504 = 분야별168×3 | 144개 독립 설계, 504개 독립 실험 또는 504개 다른 원문이 아님 |
| 판정 | support1 + conflict9 + partial50 + unverified84 = 144 | 전체 설계 support0. unverified는 반대 근거가 없는 부재/미확인도 포함하며 conflict와 구별 |

원문 계수에 적용한 구체 중복 처리는 sources.jsonl의 aliases/duplicate_group/edition 연결 및 [source-audit](evidence/source-audit.md)에 있다. TX14→T06, ABS S03의 여러 판, F03의 v1/v2/정정 캡처, F04의 목록/v1/v2를 확인했다. SX01의 Government Finance Statistics와 S03의 National Accounts는 같은 발행처라도 다른 작품으로 구분하며, SX01은 최소 후보에 넣지 않는다. L04는 직접 HTTP challenge 응답 대신 공식 페이지 웹 리더 본문을 읽었으므로 ‘18개 native 원파일 다운로드 성공’이라고 표현하지 않는다.

## 분자·분모와 민감도

| 비교 | 현재 고정 관측 | 해석의 범위 |
| --- | --- | --- |
| 엄격 상위1 | S0/8, R0/8 | 양쪽 모두 인용 완료0. 질문별 엄격 후보가 corpus에 없는 경우와 회수 실패를 구분 |
| 엄격 상위3 | S0/8, R0/8; 엄격 완결 반환슬롯0/48 | 한 반환창 안에 모든 필수 제공 근거가 있어야 함. 전체 문서 판독을 소급하지 않음 |
| 전체 목록의 엄격 부분 목표 | R05–L06 1쌍, 적격 질문1/8 | 이 질문에서 둘 다 놓침1/1. R05-L06은 S10/R12이며 수신 원문에 이미 요청된 관계 |
| 넓은 문서 기준 상위1 | support+partial을 포함하면 S5/8, R4/8 | 반환 문서 전체에서의 부분 단서 포함 기준. 인용 완료율/전이 완료율/실제 채택률이 아님 |
| 넓은 문서 기준 상위3 | S5/8, R5/8 | S만 R01, R만 R02, 양쪽 R03/R04/R05/R06. 같아진 총수가 같은 문서/원리를 뜻하지 않음 |
| R01 제외 | 엄격 S/R0/7; 넓은 top1 S4/R4, top3 S4/R5 | R01/R03 공유 문제 맥락을 한쪽씩 제외한 사전 민감도 |
| R03 제외 | 엄격 S/R0/7; 넓은 top1 S4/R3, top3 S4/R4 | 반대쪽을 남기는 대칭 점검. 유리한 한쪽만 선택하지 않음 |
| R04 제외 | 엄격 S/R0/7; 넓은 top1 S4/R3, top3 S4/R4 | workflow 설계와 요구 강도 문제의 영향. 원래 적격 표본에서 삭제하지 않음 |
| R08 제외 | 엄격 S/R0/7; 넓은 top1 S5/R4, top3 S5/R5 | 기본값 전환이라는 얇은 목표의 영향. 기존 eviction 동작을 새로 제안한 것으로 바꾸지 않음 |
| R04-M07 권고 하위절 완화 | 3분야의 R04×6, 총18판정 변화0; 엄격지지 증가0 | 산출물/과정 회고 내용만 선호로 내림. 공개 중단·인프라 보관·비공개 제외·M06/M08은 유지. 원문보다 강한 조건이라는 결함 자체를 면책하지 않음 |
| T02 제목 한 행 제외 | 별도16검색; top1/top3집합/전체순서 변화0. T02 반환의 R01-S, R02-R, R07-S 3슬롯 창 해시는 변화 | 원 corpus/원 검색은 보존. 첫 줄69UTF-8바이트/raw10·검색8토큰 제거 뒤 feature/창을 다시 계산. 원16검색과 추가16검색을 합산하지 않음 |
| 당시 고정판만 | T04 1/18문서, 8/144대응; support0. 후발10문서80대응, 미상7문서56대응 | 당시 엄격 적격 질문 분모0이므로 ‘양쪽 놓침 비율’은 **해당 없음**. 같은 원리가 더 과거부터 존재했을 가능성을 부정한 결과가 아님 |
| 질의 작성자 제공 노출 제외 | 기록상 해당 행0, 분모8과 원 집계 동일 | 노출0 기록은 사전학습 또는 모든 과거 지식 무노출의 증명이 아님. 평가 문맥의 별도 범위 위반과 구별 |
| 제출 opening-head 검증만 | 8/8 유지, 집계 동일 | GH Archive 사건과 tree/blob에 연결된 제출판을 뜻함. 개인의 최초 저술 초안을 뜻하지 않음 |

위 수치는 [evidence/recount.json](evidence/recount.json)의 sensitivities 및 [T02-title-excluded-receipt](sensitivities/T02-title-excluded-receipt.json)의 16회 추가실행 결과와 연결된다. T02의 순위가 같다는 사실로 반환 텍스트까지 같았다고 쓰지 않는다. 엄격 지지 후보 L06은 이 변형에서도 원 상위집합 밖이고 교통 support가 없으므로 엄격 분자는 증가하지 않는다.

R05–L06을 더 좁게 읽는 **증거 강도 민감도**도 남긴다. VPL의 두 분류 목록이 요청 허용을 함의한다는 독해를 거부하고 명시적 허용 문장만 요구하면 support1→0, partial50→51이다. 원 상위1·3의 엄격0/8은 같지만 전체 목록에 대응이 있었다는 결론과 조건부 놓침1/1은 바뀐다. [critical-review-notes](judgments/critical-review-notes.md)의 R05 절은 이 약점을 별도로 지적한다. 이것을 원 판정의 조용한 교체로 적용하지 않는다.

## 독립성·노출·해석의 자기 점검

- **분야 전수 판독:** library/statistics/transport 각48행은 같은 GPT-6 Astra Pro의 별도 문맥에서 순위·질의·후속을 보지 않고 고정 최초 목표와 제공 본문으로 작성했다. 문맥 분리는 독립 인간 또는 다른 모델군의 재현을 뜻하지 않는다. source/condition 읽기 범위는 각 attempts에 있으며 통계는 긴 수신 원문 전행을 새로 의미 코딩했다고 주장하지 않는다.
- **5행 비판 판독:** R05–L06, R01–T02, R04–L03, R07–S03, R08–T06을 별도 문맥에서 원문으로 읽었다. 주 분류는 1 support/1 partial/3 conflict로 기존 5행과 같지만, 이것은 취약 사례를 고른 검토이며 전체144의 무작위 일치율이 아니다. 목록 함의·객체 정체성·역할 역전의 대체 읽기는 계속 남는다.
- **실제 범위 위반:** library와 critical-review의 초기 corpus 출력에 신원·경로 외의 제공 특징 벡터/선정 메타데이터가 포함됐다. 완벽히 제한된 판독이었다고 표시하지 않는다. 원 질의 작성자에게 제공 제목/내용이 전달된 사건과는 다르며, 기록상 질의 작성자 제공 노출은0이다. 이 평가 문맥의 노출이 영향을 주지 않았다고 인과적으로 증명하지 않는다.
- **자기 재검:** library의 R05–L03 conflict 후보를 partial로 낮춘 것은 같은 작성자의 재독이다. 통계 S03의 세 충돌에서 동일 객체 매핑을 거부하면 unverified로 읽을 수 있다는 대안도 같은 문맥의 재검이다. critical R07 대안은 별개 vintage를 새 객체로 잡으면 partial로 읽을 수 있어 엄격 양성은 같아도 대안 분류는 완전히 일치하지 않는다.
- **사후 결과 인지:** 후속 최초 조회는 2026-11-22 17:14:22 UTC 이후이며 원 검색 봉인 a2ce15d의 17:12:59 UTC 뒤다. 이 작성자는 통계48 판독을 마친 뒤 후속을 읽었고 통계 파일 해시는 06241f054fd43ac3705111dfd898394e0b6445eab27666e5b4679905f12bd337로 유지됐다. 후속 인지로 최초 적합 판정을 소급 변경하지 않았다.
- **F02 정정 우선순위:** 과거 GTFS/정적 시간표 설명은 철회된 이력이다. 최신 판단 근거는 [resume-field-correction.json](field/resume-field-correction.json), [resume-field-audit](field/resume-field-audit.md), 현재 field_sources F02다. 고정 PDF는 MTA Real Time을 명시하지만 원시 로그·집계 재실행은 아니다.

이 연구가 실제로 찾은 반례는 같은 단어라도 다른 방향의 상태 변화, 접수와 실행 능력의 차이, 기록 보존과 실제 복원의 차이, 최종 출력과 입력 경계의 차이다. 반례를 못 찾은 모든 행을 검증된 적합으로 올리지 않았다. unverified84행에는 고정 제공 본문에서 필요한 관계를 못 찾은 범위와 다음 자료가 maps.csv 및 원 판단 JSONL에 남아 있다. 이 범위 밖의 모든 문서·모든 매핑에 반례나 성공이 없다는 주장은 하지 않는다.

## 현재 확인한 검사와 최종 검사와의 경계

초기 작성 때의 미완료 표시는 결과 후보89a5b4f46912c01fedd0bbb9ee66dad371eb30b3에 보존돼 있다. 아래는 그 후보를 실제 검사하고 원격 재독한 뒤의 갱신이며 Q1–Q7의 근거·판정·집계는 바꾸지 않았다.

| 검사 층 | 실제 확인한 사실 | 영수증·범위 |
| --- | --- | --- |
| 기존 입력·원문 감사 | initial-source-binding, resume-input-audit, resume-donor-audit와 분야별 실제 원문/해시 검사 및 독립 집계 | 기존 시점·파일 범위를 유지하며 원문 링크를 읽은 것으로 대체하지 않음 |
| 결과 봉인 전 작업트리 검산 | 네 명령 모두 종료0, 핵심 파일 전후 해시 불변 | [pre-result-validation](evidence/pre-result-validation.json); 당시 HEAD889c5e와 작업트리 파일 해시 |
| 결과 봉인 전 계약 검사 | --fetch 종료0·passed·소유밖/충돌/오류0 | [session-check](evidence/session-check.json); HEAD889c5e, 통합421009aa06da33c5b57ababec1fb624cf43410c2 |
| 고정 결과 후보 SHA 재검 | 89a5b4f46912c01fedd0bbb9ee66dad371eb30b3에서 입력/검색재생/재집계/원문포함결과검산 네 명령 모두 종료0, 핵심 해시 불변 | [result-candidate-verification](evidence/result-candidate-verification.json) |
| 고정 결과 후보 계약 검사 | 같은89a5b4f에서 --fetch 종료0·passed·오류0 | [result-candidate-session-check](evidence/result-candidate-session-check.json); 통합421009aa06da33c5b57ababec1fb624cf43410c2 |
| 고정 후보 RESULT·SELF_CHECK·수용 파일 원격 재독 | GitHub에서89a5b4f의 세 전체본문을 수신해 로컬 고정본문과 문자/바이트 내용 및 Git blob SHA 일치 확인. 0/8·144분포·마지막3약점·미충족 A07/A10 및 당시 대기 A31/A32를 재독 | [result-candidate-remote-read](evidence/result-candidate-remote-read.json) |
| 갱신된 수용 파일의 최종 고정판 재검 | 이 갱신을 커밋한 뒤 다시 검사할 단계. 아직 수행한 것으로 소급하지 않음 | evidence/final-verification.json, evidence/final-session-check.json, evidence/remote-result-read.json을 실제로 기록한 뒤에만 HANDOFF 작성 |

계약 검사 통과는 경로·의존 SHA·작업 상태의 검사다. 매핑 의미, 직접 인용 부재, 사용자 유용성의 인증이 아니다. 마지막 갱신판 검사와 재독의 실제 SHA/종료코드는 최종 HANDOFF와 해당 영수증이 확정한다. A07/R04 요구 강도와 A10/T02 표제 잔존은 검사 성공으로 없애지 않은 원 실험 편차다.

## 남겨야 할 가장 중요한 약점 세 건

| 가장 중요한 불일치 또는 약점 | 근거 자료 주소 | 영향을 받는 결론 | 다음 조사 제안과 첫 자료 |
| --- | --- | --- | --- |
| 유일한 전체 목록 support가 VPL 두 목록의 구조적 함의에 의존하고 그 작동 관계는 수신 최초 요청에 이미 있음. 현재 고정판의2020년 가용성도 미확인. | [VPL 신청 불가/제공 불가 가능성][l06] L64–106·중계 L3; [R05 최초안][r05] L98–117; critical-review R05–L06 | 전체 목록 엄격 지지1 및 조건부 양쪽 놓침1/1은 증거 강도에 민감하다. 원 상위1·3 엄격0/8, 새 원리 발명/실제 채택 미확인은 유지. | 첫 자료는 VPL 복합 책 신청 양식·중계 규약의 명시적 접수 문장과2020년1월 이전 해당 두 절 보존본. 복합 대상을 접수하지 않는다는 운영 규칙이 확인되면 현재 support를 내릴 근거가 되고, 명시적 허용/전달이면 목록 함의를 보강한다. |
| 폐쇄18문서·현재판·어휘 BM25·불균등 실제 질의 길이·고정200토큰 창으로는 분야명 없는 일반 발견 능력이나 관계 이해의 효과를 추정할 수 없음. | [SCOPE §4–6](SCOPE.md), [실제16질의](inputs.jsonl), [원288점수](rankings.csv), [TransLink T04][t04] 및 고정판 날짜 원장 | S/R0/8을 일반 검색의 실패율이나 R의 인과적 무용성으로 확대할 수 없다. 당시 가용 적격질문0에서 놓침 비율은 해당 없음. | 원 입력8건과 동일 고정 corpus를 첫 자료로 삼아, 제공 무노출 새 작성자의 동일 실제 토큰 예산 질의와 역할/부정 최소쌍을 사전등록한다. 문서 회수·근거창 선택·전이 판독을 분리해 어떤 단계가 바뀌는지 비교하며 원16회에 합산하지 않는다. |
| 부분 후속 유사성·도메인 검색0·발행자 현장 기록은 실제 설계자 채택이나 모든 운영 성과를 증명하지 않음. | [R01 구현 #68404][r01-impl], [R07 후속 #3298][r07-replacement], [F02 p13][f02], [F04 v1][f04-v1]/[v2][f04-v2], [도메인 검사 영수증](evidence/followup-citation-screen.json) | 실제 직접 인용/채택8건 모두 미확인. R01경고 완료·R07최초7조건·모든 실제 운행·전체 추정모형 검증을 주장할 수 없음. | 첫 자료는 #68404가 잇는 #70173의 경고 시험과 #3298이 잇는 #24의 최종 변환 시험, F02 세 날짜 보존 feed/DCP 코드다. 제공 자료를 결정 전에 읽고 선택을 바꿨다는 설계 기록/참여자 확인이 나와야 인과적 채택 판정을 별도로 바꿀 수 있다. |

[observation]: https://github.com/laadkke-arch/agentflow-open/commit/889c5e792a3db3856bf5be8c90d9486490ce8677
[retrieval-seal]: https://github.com/laadkke-arch/agentflow-open/commit/a2ce15d10415c556574d1a65af77718a81052d01
[r01]: https://github.com/rust-lang/rfcs/blob/d5fe87812fc95f2699e770993848179b6c071f2c/text/0000-llvm-asm.md
[r03]: https://github.com/rust-lang/rfcs/blob/5559913ccacbe1e6c6c5d26d33a08f9b09641c5e/text/0000-inline-asm.md
[r04]: https://github.com/rust-lang/rfcs/blob/c80e28415d8a7f94448661badb963d3d6fc9efb2/text/0000-project-groups.md
[r05]: https://github.com/kubernetes/enhancements/blob/6d97b64e59854ec7744d8bc3bfb9fadac29b52fe/keps/sig-network/20200103-mixed-protocol-lb.md
[r06]: https://github.com/kubernetes/enhancements/blob/50f8b89cb8f0b3d10b1b0d5bc278122abbd23c84/keps/sig-cluster-lifecycle/wgs/20200108-instance-specific-componentconfig.md
[r07]: https://github.com/kubernetes/enhancements/blob/63f35ac4f5d381ffae6bb5f9bacd67dfd93ba7a7/keps/sig-node/20200110-apparmor-ga.md
[l03]: https://multcolib.org/interlibrary-loan
[l06]: https://www.vpl.ca/borrowing/interlibrary-loans
[s03]: https://www.abs.gov.au/statistics/detailed-methodology-information/concepts-sources-methods/australian-system-national-accounts-concepts-sources-and-methods/edition-8/chapter-24-quality-national-accounts/revisions
[t02]: https://cdn.mbta.com/sites/default/files/2026-09/2026-09-16-mbta-diversion-service-standards-for-subway-regional-rail-and-ferry-accessible.pdf
[t04]: https://www.translink.ca/-/media/translink/documents/plans-and-projects/managing-the-transit-network/transit-oriented-communities/transit-services-guidelines-public-summary.pdf
[f01]: https://apps.cio.ny.gov/apps/mediaContact/public/view.cfm?parm=926C019C-DE79-DD17-D6493016DF74143F_5D9C1A27-C9C7-90C0-217C93A974EEA6D8
[f02]: https://www.nyc.gov/assets/planning/download/pdf/planning-level/transportation/covid19-transportation/20200421.pdf#page=13
[f03-v1]: https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/articles/reconciliationofmidyearpopulationestimateswithcensus2021englandandwales/2023-02-28/previous/v1
[f03-current]: https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/articles/reconciliationofmidyearpopulationestimateswithcensus2021englandandwales/2023-02-28/previous/
[f04-v1]: https://www.ons.gov.uk/file?uri=%2Fpeoplepopulationandcommunity%2Fpopulationandmigration%2Fpopulationestimates%2Fdatasets%2Festimatesofthepopulationforenglandandwales%2Fmid20222023localauthorityboundaires%2Fprevious%2Fv1%2Fmye22tablesew2023geogs.xlsx
[f04-v2]: https://www.ons.gov.uk/file?uri=%2Fpeoplepopulationandcommunity%2Fpopulationandmigration%2Fpopulationestimates%2Fdatasets%2Festimatesofthepopulationforenglandandwales%2Fmid20222023localauthorityboundaires%2Fprevious%2Fv2%2Fmye22tablesew2023geogsv2.xlsx
[r01-impl]: https://github.com/rust-lang/rust/pull/68404
[r03-replacement]: https://github.com/rust-lang/rfcs/pull/2873
[r07-replacement]: https://github.com/kubernetes/enhancements/pull/3298
[r07-doc]: https://kubernetes.io/docs/tutorials/security/apparmor/#securing-a-pod
