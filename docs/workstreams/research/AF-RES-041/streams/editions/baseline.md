# B03 판별표 · 묶음② 고정

확인시각: 2026-11-22T20:14Z. SCOPE v1(2021e2f236d56073125d940fafe158d2e6ea5c70)의 정확 제공판 조건을 그대로 적용한다. 아래는 원전측 독립 판독이다. 수신 소스는 lilypond 담당이 고정한다. 현재 직접 읽은 것은 서문·목록·공식 샘플이며, HWN이 사용한 물리판·해당 쪽은 **미확인**이다.

| 원전 후보 | 서지 직접 확인 | 본문 직접 확인 | 당시 가용성 | author-held 정확판 / 기호 위치 | 다음 첫 자료 |
| --- | --- | --- | --- | --- | --- |
| Schubert Auf dem Strom, Bärenreiter BA5635 | ED001 title/III: Dürr,©1988,3쇄2008,ISMN M-006-49329-6; BA5527 IV/14b에서 발췌. ED004 NCID BA27399877는 c1988 동일 제목/Dürr,24pp+2parts를 독립 확인하나 BA번호 없음 | 서문 II–III만. 음악쪽 없음 | 1988판 계열은1997보다 이르다. 2008쇄 자체는 늦다 | **미확인**. sharp/natural의 정확쪽과 형태변수도 **미확인** | BA5635의1997이전 인쇄본 title/colophon + 샤프·내추럴 쪽; 현재 preview로 대체하지 않음 |
| Schubert NSA BA5527 IV/14b | ED002 official:1988,WaltherDürr; ED003 기관:pp196–218 | IMSLP1014719 후보 있으나 실제pdf 접근 실패 |1988발행 기록; 실제 저자 독서는 별도 | **미확인**. 단행 BA5635와 전집 BA5527의 원본 선택 불명 | BA5527 IV/14b pp196–218와 title/imprint. IMSLP의14a 표기는 기관14b와 불일치 |
| Müller op64 Hofmeister FH6064,22Etüden für Waldhorn | ED005 publisher:32pp,Frehse,ISMN9790203460640. ED007 image footer6064 | 공식 sample 첫연습곡1 Moderato 전체450×620; sharp/flat 존재 | 인쇄연도 **미확인**.2023/07URL은 업로드 경로일 뿐 | **미확인**.1.0.1은 opus/권/판/쪽을 적지 않음 | 1997이전 FH6064 개체의 title/imprint와 double-sharp/flat쪽. IMSLP1035533·Merseburger C.M.1168관계 검증 |
| Müller op64 Hofmeister FH6065,12Etüden für Ventilhorn | ED006 publisher and ED008 image:Neubearbeitet von A.Frehse,FH6065 | 공식 sample I Nicht zu schnell; flat 존재 | 인쇄연도 **미확인** | **미확인**.6064와 다른 권·편집표기이므로 무단 합성 금지 | 1997이전 FH6065,plate10822 여부,해당 accidental쪽; IMSLP1035530은 목록후보 |
| Wanske Musiknotation,Schott1988 | LilyPond bibliography 제공값; 우리 institutional record 접근 실패ED018 | **미확인** | 수신 bibliography가1988을 적지만 별도 검증 미완 | sharpbeam끝 규칙 원문쪽 **미확인** | ISBN3-7957-2886-X 실물/정상공개본문의 accidentals section |
| Ross Teach yourself the art of music engraving and processing,HansenHouse1987 | LilyPond bibliography 제공값; Cornish record 접근 실패ED019 | **미확인** | **미확인**(해당판 기관검증) | 어떤 규칙을 적용했는지 **미확인** | HansenHouse1987판,edition/title/accidentals chapter |

## 고정된 해석 한계

1. 판번호 후보가 좁아져도 source comment의 출판사/작품명을 정확 물리판으로 자동 치환하지 않는다. Schubert의1988판 계열은 유력하지만1.0.1 comment만으로 BA5635/BA5527 선택은 알 수 없다.
2. Müller 공식 샘플은 실제 음악 표기 관측이다. 그러나 오늘의 출판사 샘플이1997당시 인쇄와 같은 판각/판면인지 확인되지 않았다. 이미지가 낡게 보여도 스캔 출처를 추정하지 않는다. 두 권은 opus64 한저작으로 최소수에 한 번만 산입한다.
3. 목록상 원자료 보유/발행, HWN의 실제 열람, 이번 조사자의 열람을 분리한다. IMSLP 업로드2026과1988출판은 다른 사건이다.
4. BA5635서문은 added principal-note accidental을 small print라 하지만 NSA2022 p14는 fullsize bracket이다. 두 원문이 다른 규칙임은 직접 확인했으나 변화연도·원인 또는 Feta 영향은 **미확인**이다. 이후판의 지침을 옛 원전의 불변속성으로 쓰면 실패한다.
5. Schubert/Müller의 정확쪽 미확인은 후대 일반 조판원문(Gould/NSA/MPA) 읽기로 닫히지 않는다. strict exact_donor는 **미확인** 유지한다.

## 최소수 제안

ED007 Müller op64 샘플1저작, ED009 Gould2011 공식excerpt, ED010 NSA2022 rulebook은 음악 배경3저작이다. root의 MPA1993을 더하면4저작. ED003 ÖAW/ED004 CiNii는 기관기록2건이며 root의 독립서지1건과 합산 가능하다. ED001 Schubert서문은 실독했지만 중복/판본 불확실성을 피하려고 현재 산입하지 않았다. ED002는 ED003과 NSA계통 겹침을 공개하고 추가기관분모에 쓰지 않았다.

## 묶음③ 추가 관측 · 원래 표 보존

2026-11-22T20:17:59Z: ED020은 BA5635 판매자 record에서 직접 연결된 실제음악 raster excerpt다. 마디127–135를 판독했고 sharp/natural/flat의 기본 형상을 관측했다. 따라서 "Schubert 악보본문을 전혀 못 보았다"는 서술은 이제 틀리다. 그러나 excerpt 안에 인쇄쪽번호·colophon은 없고 PDF생성일2015는 원인쇄연도가 아니다. 정확1997 제공판을 닫지는 않는다. 위 묶음②의 preview부재 판단은 그때 읽은 공식서문에 대한 기록으로 보존한다.

ED020을 ED001과 같은 Schubert저작 대표로 music_background에 산입해 이스트림 음악4·기관2가 되었다. 분모규칙은 바꾸지 않았다. 새 원문관측이 추가된 결과이며 이전5개원저작에서6개로 늘어난다. root MPA를 포함하면 음악5건이다.
