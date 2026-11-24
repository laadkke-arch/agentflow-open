# 반례와 정정 (bundle 4)

이 문서는 위임된 판독이다. N=지명, D=공식, F=별개 공개 요청, E=고정 소스, G=GitHub. sources.jsonl에서 출처/절/한계를 추적한다.

1. **메일만 꺼야 하는 경우**: 화면 @mention이 보존 조건이면 topic mute는 잘못이다. E16에서 normal/tracking/watching mention +1, mute 0 기대; E11은 muted topic에서 처리 종료. 이메일 환경설정의 일반 알림과 PM은 E1/N3에서 분리; digest D3, MLM E5/E12도 별도. MLM 켜진 채 email_level=never만 바꾸어 모든 게시물 메일이 멈춘다고 말할 수 없다. N2 all 구독 이메일은 네 값 변경, E10 기대. 시스템 이메일/화면 잔존 실측 없음.
2. **한 topic만**: N2의 unwatch는 tracking으로 전환; mention까지 끄는 mute와 같지 않다(E10/E16). 다른 topic과 PM/메일을 보존하려면 global unsubscribe가 과잉. 메일 한 채널만 특정 topic에서 억제하고 그 topic의 모든 화면 알림을 그대로 유지하는 전용 제어는 조사한 v3.3.0 근거에서 확인되지 않음; 정상/track으로 다운그레이드도 event 자체를 줄임. 사용자에게 선택의 손실을 알려야 한다.
3. **MLM + mute 예외**: N1의 2022 보고에서 일반 수준 row(1)와 staged 사용자 사례; 최초 요청에는 own mail 보존이 명시되지 않고 #8에서 확정. E12의 explicit muted topic/category/tag/user SQL 제외와 E17의 implicit global mute positive row >0은 별개. default mute + normal row + 다른 제외 없음이면 코드상 통과 후보; explicit category mute + watching topic이라도 E12 직접 제외. E15에는 기본 mute + watched topic/category/tag 사례의 예상 한 통, explicit mute의 예상 0이 있지만, default mute + normal row의 직접 시험은 확보하지 못함. N1에 나온 설명을 모든 판·메일 유형에 일반화하지 않음. F3 muted user의 2016 fix는 다른 사건이며 원작성자 retest 없음. F4 태그 수정+일부 로그는 설정 동일성/메일 수신 인과 검증이 되지 않음.
4. **관리자 기본값**: 새 가입자만이면 E1/E17 초기화, 기존 사용자 변경이면 E14 flag 및 E18 값 비교/카테고리 row 유무. 기존 값이 old default와 같지만 명시적으로 선택한 사람도 값 기반 갱신 대상이 될 수 있다. 다른 값은 보존되는 조건이 있고, category 새 추가는 기존 row가 없는 사람만; 삭제는 old level 일치 행 제거 및 auto-watch 조정. 따라서 개인 선택을 항상 보호하는 상속이라고 부르지 않는다. D5 그룹 가입 때 수준이 상승하는 정책은 별개(2020 공지, 최신 적용 미실험).
5. **타서비스 반례**: G2/G4 unsubscribe 뒤 mention/team으로 재구독; G3 repo ignore는 mention도 억제, unwatch와 다름. G1에는 inbox에 두 채널을 켜라는 표현과 On GitHub 활성 + email 해제 안내가 공존하므로 실제 보존은 미확인. G5의 commit mention 중단 예정에 대한 사용자의 서로 반대 요구(메일만 제거, 타인 commit mention 유지)를 구분. Discourse 규칙으로 GitHub를 해석하지 않음.

## 노출 순서 정정
- 최초 229919/116393 등 전체 topic 페이지와 검색 결과에서 댓글 일부가 노출되어 first-only 판독과 답글 전 예측이 깨졌다. body_freeze.md는 당시에 확보한 상태의 기록이지 블라인드 자료가 아니다.
- 62748은 body freeze 이후 정식 slug를 통해 직접 열람했다. 문서로 판정하고 네 번째 지명 행 대신 채우지 않았다. 280651의 숫자/JSON/검색 대체 경로는 실패했다. 나머지 첫 글도 최초 수정판 확인 못함.
- 사후 예측표/합성 통제는 검증된 성공률이 아니다. 실제 사용자에게 질문하지 않았고, 다음 알림 관측도 수행하지 않았다.
- 35개 독립 저작/파일(49 ledger 행)은 자료 수이지 35 독립 사건이 아니다. 코드·시험은 한 버전 계보, 한 Meta topic은 한 계보, G1–4 공식 문서 묶음. 22 전체 하한 충족; 지명 직접 열람 3/4 미달. 결론 PARTIAL.
