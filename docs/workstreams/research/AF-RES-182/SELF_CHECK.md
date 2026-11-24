# AF-RES-182 자체점검 — PARTIAL (독립 검토 미실시)

| 질문 | 답·근거 ID/원문 위치 | 반증 탐색 | 결과 | 미충족 |
|---|---|---|---|---|
|Q1|C1/C2 official collated HTML footer 2.24.4/2.26.0, X11–X26 exact tag/12 blob/part+measure key (fixtures.csv URL)|6+6 tag 재열람, first-measure 및 part-list+parts normalized 문자 대조, F11–F26 문서 원래 XML 링크 열기, R1/R2 release 페이지 시도|ID 6/6 유지, full blob 동일 0/6, normalized score body 동일 1/6(33b), m1 내부 동일 5/6. 02c 범위 처음 잘못 적은 것을 원문 재판독 후 보정.|문서 XML byte join 0/12. 전체 동일 입력 3쌍 조건 미충족. build command/options 미확인.|
|Q2|C4–C11 MusicXML 4.0 CG Report element pages; X14/X24 tie+tied; X12/X22 multiple-rest; X16/X26 part-name-display|같은 곡선이라도 음향 tie를 나타내는지 C8/C9 구분; 같은 count라도 glyph가 다른지 O12/O22; 다른 display vs same base name|음향/의미/인쇄 표지 분리 완료. DTD 구버전과 4.0을 동일 사양판으로 취급하지 않음.|구버전 사양 각각의 역사 규칙 완전 대조, 실제 edit/playback 없음.|
|Q3|C1/C2 소개, C3 contributor/musicxml-tests; O11–O26 실제 output URL과 물리 위치|신판 PNG/SVG 후보 G21–G26/H21,H22,H24,H26 열기 실패 → 공식 PDF 페이지 시각 확인. 구판 D6/D20/D25/D26 확대 대조|12/12 출판 자리 직접 열람; caption-only는 C1/C2로 따로 표시.|문서 XML 원바이트·standalone 신판 이미지 URL·개별 .ly·실제 빌드 명령 미확보.|
|Q4|O11/O21 first rest, O12/O22 3/16/12 vs 3/15/whole/12/3, O13/O23 cut C, O14/O24 F4 curve, O15/O25 slur, O16/O26 label|구판 33c endpoint PDF 확대해도 m1 끝점 모호, 신판 m3 식별 안 됨; 첫 위치 유지, supplemental 대조|12자리 처리, 첫 속성 11/12 판독 가능(보존 성공 수 아님), m3 추가 미확인. 동일 속성 시각 대조 4/6(02c,11a,33b,41i P1).|O15 endpoint, O25 m3, 판면·성부/음향 내부 정보 미확인.|
|Q5|C1 L85/93/355, C2 L149/159/620–622; X/O 각 6쌍; comparisons.md|02c 총합 일치해도 15+1 합쳐짐; 11a m7 print 변화에도 첫 기호 동일; 41i display 변화와 base name 동일; 33c caption 교차 곡선 미확인|02a/02c grouping 차이 직접, 33c nested 차이 후보, 입력 변화 및 판면/스타일/변환 손실 경쟁. 인과 확정 안 함.|동일 input × 양판 converter/renderer 옵션 고정 실험 없음; pixel/byte 동일성 없음.|
|Q6|T8/T9/T10/T11 Cinderella scan page5, T5/T6 Trek image5/OCR, T1/T2/T3/T4/T7 기관·서비스 문서|같은 페이지의 line-break/header vs 전사, OCR frcsn vs from, DVD menu/feature와 video payload, caption/timecode 정책; T12–16 접근 실패|실제 book scan/text 및 신문 기관 제공 비교 이미지 확인, AV 2 보고. 동일 출처/표현/기능 별개.|동일 AV master/access 재생 0쌍; raw Trek source/OCR, 개별 EPUB 산출물 미입수.|
|Q7|C8/C9 tie/tied, O14/O24, O12/O22, O16/O26, transfer.csv, RESULT 표3|인쇄 독자에 충분한 링크를 edit/playback에도 충분하다고 가정한 반례 탐색|A/B/C 조합 조건·검증 부담 정성 비교; 편집·재생은 추가 근거 요구.|실행, 실제 사용자 성공률/비용 실측, 제품 DB 설계 미실시(범위 밖).|

## 분모·직접 열람·검산

- sources.jsonl 79행, source_id 중복 0, 필수 필드 누락 0, 열람 성공 50·실패 29. unique yes work_id 36: XML 12(6시험/2판), 출판 그림 내용 10(12자리 직접, 새 11a/33b는 관측된 속성 같아 중복으로 제외), 문서 4(C1,C2,C3,C4; C5–C11 같은 사양), 타 분야 10(T10은 T9 전사 재표시로 제외). 검색 요약/접근 실패는 산입하지 않음. 두 판의 이미지 hash 동일 여부는 검증하지 못함.
- 엄격 파일 단위 그림 7(구판 PNG6, 신판 PDF1)로 8보다 1 부족; PDF 내 각 score 별 distinct visual content 10. 그림을 실제 판독한 범위와 독립 물리 원파일을 혼동하지 않음. 타 분야 실제 산출물 3 distinct(T8 scan, T9 전사, T5 비교화면); 10 자료 중 나머지는 문서/보고. 4개 실제 보존 산출물 기준 1 부족, 특히 AV 직접 원본·접근본 쌍 0. 22 총수 자체는 넘었지만 유형 및 엄격 동일 입력 최소 미충족.
- 6 시험 사건, 12 출판 자리(한 구현 계보); 타 분야 4 사례(전자책·신문 실제 대조 각1; AV 인수/정책 보고 각1). 직접 독립 **검토자** 0, 독립 **구현** 1; 새 실행 관측 0. 미확인 값을 0 실패로 코딩하지 않음. 전체 bytes 동일 0/6은 두 실제 tag SHA가 다르다는 관측, 문서-태그 bytes 미확인 12/12는 접근 실패여서 같지 않다는 결론 아님.
- 파일 참조 검산: fixtures 12행, observations 12행, sources 79행. observations의 O/X source ID 존재, 필수 source fields 존재 확인. RESULT가 요구한 표1로 시작하고 마지막 약점 3행임을 재열람. frame.csv T10 중복 산입 보정. 02c XML measure 실제 31→34, m4–18, m19, m20–31, 새 m32–34를 보정 commit 9f11fb1018703c74879b38312f8f689bd5e6cc69에 기록; ledger에도 보정. 처음 기준 위치 바꾸지 않음.
- 대표 commit 재열람 성공: SCOPE 9ab8c9f6e12709c2448f5250c928e316f8bd8779; fixtures 9f11fb1018703c74879b38312f8f689bd5e6cc69; observations adfdfd3851132c034c3f42be40fc141d314c9303; comparisons 6314a7478b2b478c89806d7d2677c736234c39d7; transfer 7eef8961cf9f015e837e87a83b1ca4daf33d8193; sources eb6e521d5dd05dbff2f3252f59ca731e3fa4bbe1; RESULT 7ac9f233e218391ba65c15c929a69b202a4e0d06. GitHub fetch로 고정 커밋에서 실제 내용 읽음. frame 보정 aafcf8e756d294f11ce29982e9a8c39272d7395f.
- 로컬 git diff/check, byte hash, XML validation, render/MIDI/edit, 독립 reviewer는 실행하지 않음. 단순 API 원문 텍스트 대조와 원장 구조 검사만 실시. 외부 HTTP 수집은 웹 도구로 수행했고 로컬 DNS 제한으로 재실행하지 않았다. HANDOFF에서 Codex Cloud 다음 행동 지정.

**자체 상태 PARTIAL**: 정확한 전체 동일 입력 3개 미달, 엄격 그림 파일/실제 타 분야 보존 산출물 하한 미달 가능성. 중앙 상태와 무관. 
