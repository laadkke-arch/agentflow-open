# 반례·결손·정정

## 실제 반대 입력
- R01 (#211, Safari14 실험 플래그): showModal 존재를 native 완성으로 판단하면 close 누락/폼 제출/배경 처리 문제를 놓친다. 제보자는 실험 기능 자체를 한 시간 전 알았다고 명시: 일반적 발견 현상 부정의 반례. 그러나 외부 링크→완성된 네이티브 선택→동일인 실제 채택은 아님. 작성자는 workaround 제안, 회신은 비실험판을 기다리자는 입장. 원문 https://github.com/GoogleChrome/dialog-polyfill/issues/211 (R01 body/replies). 
- R03 (#233) Safari15.3 사용자는 Safari15.4 출시 후인 2022-07-01에도 Angular 모달 실패를 제보. 공급자 출시일 ≠ 이용 가능 환경. CSS/기능 감지 진단은 가설. https://github.com/GoogleChrome/dialog-polyfill/issues/233
- R02 (#217) slot/Shadow DOM focus; R05 (#193) 플래그에 따라 상반된 결과와 다른 환경의 재현 실패. 키보드 사용자의 목적은 focus 이동과 복구·배경 비활성화이며 API 이름만으로 검증되지 않는다. https://github.com/GoogleChrome/dialog-polyfill/issues/217 / https://github.com/GoogleChrome/dialog-polyfill/issues/193
- R04 (#237) 2023-07-17 dynamic CSS 선택 API 요청: 신기능 발견보다 판단 방법 필요. https://github.com/GoogleChrome/dialog-polyfill/issues/237
- R06 (#204) 0.5.2 타입 오류, 유지자 0.5.3 수정 보고, 사용자 후속 rollback 보고. F16 선언 존재를 실제 컴파일 보증으로 바꾸지 말 것. https://github.com/GoogleChrome/dialog-polyfill/issues/204
- D1 P05/A01은 문서 누락 발견을 직접 보여주나 원래 표준을 몰랐던 경우 아님. D2 P06은 타입 이동. C1 F01/F02는 native 우선 조건 분기. C2/C4 P02 P04 F07 F08은 동일 작성자/동일 공급 계보, 직접 복사 미입증. 네 패치를 독립 발견 사건으로 세지 않는다.
- T01/02/03 WMATA 동일 Red Line: 기존 철도 서비스가 원래 있었고 공사기간 대체버스·재개를 운영자가 공지. T03 실제 재개와 역별 집계 확인, 이용자별 선택 미확인. T02의 >850k trips를 사람수나 절약 시간으로 환산 금지. T04 날짜 표기 충돌: T01 Jun1–29/Jun30–Aug31, T04 Jun1–27/Jun1–Aug31; Takoma 날짜 정확히 단정하지 않는다. 네 역 Sept1 재개 결론은 T02/T03 일치.

## 정정 원장
이전 값은 37b7bf891b0f047ec88ab602d9e7a9bf2b889003 원장, 새 값은 이번 커밋. 
- F04: 이전 modal plugin calls dom.close; dialog reference; showModal line not shown in excerpt; 변경 base full L149–162: dom.open guard, dom.close() and dom.showModal(). 출처는 동일 원장 URL/재열람; 중복을 빼거나 정확한 줄을 읽은 결과.
- F06: 이전 8.18.1, Chrome >=109, last 2 Firefox/Safari, Firefox ESR; dialog-polyfill ^0.5.6; exact iOS line to re-read; 변경 8.18.1; Chrome/Edge>=109; last 2 ChromeAndroid/FirefoxAndroid/Firefox/Safari/Opera; Firefox ESR; iOS>=16; dependency ^0.5.6. 출처는 동일 원장 URL/재열람; 중복을 빼거나 정확한 줄을 읽은 결과.
- F11: 이전 counted true; 변경 counted false: same file at another version or release commit metadata supports already counted release; conservative unique file rule. 출처는 동일 원장 URL/재열람; 중복을 빼거나 정확한 줄을 읽은 결과.
- F14: 이전 counted true; 변경 counted false: same file at another version or release commit metadata supports already counted release; conservative unique file rule. 출처는 동일 원장 URL/재열람; 중복을 빼거나 정확한 줄을 읽은 결과.
- F15: 이전 counted true; 변경 counted false: same file at another version or release commit metadata supports already counted release; conservative unique file rule. 출처는 동일 원장 URL/재열람; 중복을 빼거나 정확한 줄을 읽은 결과.
- F17: 이전 counted true; 변경 counted false: same file at another version or release commit metadata supports already counted release; conservative unique file rule. 출처는 동일 원장 URL/재열람; 중복을 빼거나 정확한 줄을 읽은 결과.
- F18: 이전 counted true; 변경 counted false: same file at another version or release commit metadata supports already counted release; conservative unique file rule. 출처는 동일 원장 URL/재열람; 중복을 빼거나 정확한 줄을 읽은 결과.
- F19: 이전 counted true; 변경 counted false: same file at another version or release commit metadata supports already counted release; conservative unique file rule. 출처는 동일 원장 URL/재열람; 중복을 빼거나 정확한 줄을 읽은 결과.
- P01/P02/P06 한계 열 갱신: 최초 release 미확인 → F09/F10 tag / F11/F12 beta4 registry / F16 upstream root type (P06 registry 미확인 유지). 
- frame P/B/R/T: 8/4/pending/pending → 12/5/6/4; 6 PR 그대로. 29 counted 중 같은 파일 revision 및 release commit metadata 6을 제외해 23, 반례 6+교통 4 추가해 33. 전체 원장 60 rows, counted 33. 원문 댓글/미러/실패 별도 카운트 안 함. 
- 원인 판정: 4 code removal PRs, 2 controls; BL-linked pair → 3 consumer lineages (HDS/BL/DIM), 모두 같은 DP upstream을 사용하는 큰 계보. D1 HDS, D2 DP types. 실제 인과 사슬 관측 없음, 효과 부재 주장 금지.
