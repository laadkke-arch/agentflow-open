# RFC 대조 (Q6)
원기록은 sources.jsonl R01–R10. 행은 관계 사건이며 같은 원문의 여러 표현을 독립 사건으로 세지 않는다.

| 관계 | 원레코드·당시 본문 | 효과 | 자동 링크 치환 반례 |
|---|---|---|---|
| 2119 → 8174 update | [R01](https://www.rfc-editor.org/info/rfc2119/) 1997-03 abstract/status L87–101,224–238; [R02](https://www.rfc-editor.org/info/rfc8174/) 2017-05 §2/status L160ff,258–269 | BCP14 정의 유지·대문자에 특별 의미 한정; 일반 소문자 요구문 가능 | 8174만 저장하면 2119 정의 소실; 역사적 1997 인용에 후대 해석 덮어쓰기 |
| 2616 → 7230–7235 obsoleted by | [R03](https://www.rfc-editor.org/info/rfc2616/) 1999-06, 상태 L10123–10131; [R04](https://www.rfc-editor.org/info/rfc7231/) 2014-06 L5804–5813 | 후계 6개, updates 별도 | URI/메시지/캐시/조건/인증을 하나의 후계로 환원 불가 |
| 7230 → 9110 + 9112; 7231 → 9110; 7234 → 9111 | [R06](https://www.rfc-editor.org/info/rfc7230/) L55–75; [R05](https://www.rfc-editor.org/info/rfc9110/) L75,126,7483–7486; [R07](https://www.rfc-editor.org/info/rfc9112/) L78–80,96–105; [R08](https://www.rfc-editor.org/info/rfc9111/) L72–76,95–100 | 2022-06 분할·재조립: semantics/HTTP1.1 messaging/caching | framing 문제를 9110 하나에 연결하면 부정확; 9111 캐시 별도. R07 현재 status에 9931 update 표시, 상세 범위 미확인 |
| RFC2119 EID499 Verified | [R10](https://www.rfc-editor.org/rfc/inline-errata/rfc2119.html) L0–1,33–51 | Abstract 문구에 NOT RECOMMENDED 삽입. 본래 §4 정의는 있음. inline rendering은 informative, 인용 원문 대용 불가 | erratum 반영 렌더로 원 RFC를 바꾸면 옛 인용·정오표 사건 소실 |
| errata 상태 | [R09](https://www.rfc-editor.org/series/rfc-errata/) L69–80 | verified vs reported/held/rejected; RFC 원문 파일 수정하지 않음 | reported 또는 merely related를 자동 normative correction 취급 금지 |

구분: document lineage → relation type(update, obsoletes, erratum_verified, related) → source edition+section → changed claim. 방향을 역조회하되 원래 레코드 관계 그대로 저장. 2616의 6개 분기 중 7232/3/4/5 개별 원문 전체는 미확인; R05/R08 레코드 근거만 사용. EID499 보고·검증일은 F05 실패로 미확인. 9110과 9112에 걸친 7230 특정 절별 완전 매핑은 미실시. RFC의 'obsoletes'를 WCAG 2.2의 전 버전 폐지로 유추하지 말 것(W12 L38–39).
