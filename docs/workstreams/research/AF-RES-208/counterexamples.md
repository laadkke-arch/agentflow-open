# 반례 및 정정 기록 (4단계)

- C1: 원래 3/16인 예외가 3/27로 보이면 화면상의 '3/23 이후'에는 포함되지만 원래 순서에서는 제외된다. 역방향 3/30→3/20도 반대. K1 §3.8.4.4, E1. 원래 순서의 의미와 사용자가 실제 원하는 표시일 집합을 분리한다. RID는 mutation key로 쓰고 scope 의도 자체는 질의로 결정할 수 있다.
- C2: 3/30 취소는 absence가 아니라 tombstone/EXDATE다. old truncate + new insert만 하면 새 3/30가 생길 수 있다. K1 §3.8.5.1, K2 §3.2.5, K3, K4, K5. 분할 추천에 보존 계획이 없다면 추천을 조건부로 낮춘다. 반대로 취소를 복원한다는 명시적 요청이면 이 보존은 오답.
- C3: MO+WE 중 MO만 FR은 uniform RANGE로 WE도 움직이는 반례(K1 §3.8.4.4 명시적 note). 반대로 무예외 단순 weekly +1h는 동일 표시 결과를 만들 수 있어 무조건 분할만 권하지 않는다. 화면 등가와 UID/참여 응답 등가는 다르다.
- C4: Berlin 3/29 DST +01→+02. 3/23 09 local=08Z, 3/30 09 local=07Z. local +1h라면 09Z/08Z. UTC-fixed 09Z라면 10/11 local. 어느 보존 의도인지 명확히 하지 않으면 첫 링크도 잘못된다. §3.3.5, §3.3.10; 실제 엔진 미실행.
- 경쟁 설명: (A) #8957 UI cache만의 문제라면 readback에서 새 DTSTART/RRULE가 일치해야 한다. N1 readback이 TH인 점은 A만으로 부족; F3 다른 클라이언트 차이도 보고. 그러나 서버 parser가 잘못 해석한 것인지 웹이 잘못 보낸 것인지 raw request 없음. (B) #8450 단순 참석자 UI 버그라면 organizer raw exception의 attendee는 있고 receiver raw moved instance도 있어야 한다. 둘 다 원자료 없음. (C) #6437 stale BYMONTH 추정은 아직 데이터 없음. BYMONTH가 없거나 새 RRULE가 AUG 일치하고 UI만 틀리면 첫 링크는 expansion/receiver 증거 쪽으로 이동.
- 정정: 원장 K2는 §2.1.5, §3.2.5를 포함한다. §4.4.3은 구체 취소 RID 19970801T210000Z; §4.4.5 location change 예문은 'RECURRENCE-ID;THISANDFUTURE'로 표기되어 K1 문법 'RANGE=THISANDFUTURE'와 불일치. 이를 그대로 문법 추천하지 않음. §4.4.7은 entire reschedule REQUEST에서 instance-specific information 명시 포함 없으면 소실된다고 설명한다. Google 현재 가이드에서 과거 two-request/reset warning을 확인하지 못한 결손과 별개이다. RFC 여러 절은 신규 work로 세지 않음.
- F8은 같은 경로 버전 차이를 직접 읽었으나 하한 제외. F9와 E4는 하나의 변경 계보 내 patch vs test file이라는 별개 저작; 독립 확인 횟수로 세지 않음. F10은 yearly UI 변경일 뿐 #6437 해결로 승격 금지. 원장 X1 ZIP 열람 실패; X2/X3 미디어 미확인. 작성자 초기 본문 revision을 확보하지 못했고 body_freeze는 현재 본문을 댓글 전 기록한 것일 뿐.
- 직접 사건 4, 합성 통제 4, C0/C3b/역방향은 보조 비교. 고유 30 작업, 사건 단위 분모와 독립 검토 분모를 섞지 않는다. 독립 재현/벤치마크/실제 사용자 질문 0.
