# AF-RES-032 진행 원장

| 묶음 | 고정 입력/결과 SHA | 원격 재독·증거 경로 | 다음 행동 |
| --- | --- | --- | --- |
| ① 표집·시계·판정 | f18b6f8d452bca42d60abba5129f2001099dc5e8 | SCOPE blob93ae8ea02fa3aa2563c2a728ce9adeb83ca51601; evidence/session-start.txt 및manifest | A 배포 원문 봉인 |
| ② A12 원문·목적 봉인 | 168d90b8519bcb4f673acc659bbaae895f79fca5 | 07:18:08Z references blob e38024668d0b0321056831dad761f421c28bd792; evidence/a-seal-remote.json | 이 시점 뒤에만 상류·후속 판 열람 |
| ③ B6 사건 봉인 | ffbce62e4c01459ebbfb006a5d6c67e425ed7c17 | b-sealed blob d31a257bdfcaea85ab7ac2507d146b5704636f61; collectors/b/remote-seal-receipt.json | 이 시점 뒤 소비자 질의18·후보17, 실패·중복도 보존 |

현재 묶음은 실제 소비자판·타 분야·세 보기 관측·통합 원장이다. 이 묶음의 SHA는 다음 결과 커밋에서 기록한다. 로컬 fetch는 명시적 origin 브랜치 refspec을 사용한다. 최초 B봉인 뒤 fetch는 FETCH_HEAD만 갱신되어 비교가실패했으며, 명시적 remote refspec으로 갱신한 뒤 index일치를 재검했다. 이는 연구 실패나 force push가 아니다.

입력: foundation172c6bc37bdf91b91c86b9b3be29cb5b44fa4971 / dependency02742dadeeb632301108e1fc83ba393db971ec28b15. 원 A12prefix SHA256 b3c2f68b905102f0fa682ab45a34c0f3401a69b61ba0a59327045e04a626d562는 유지된다.

검산: R18/18, offline 원문검산, 별도내부 root archive 재독27개, root freshGET4건. 각targetHEAD/inputhash/exit와 동일작업자·별도판독 구분은 collectors의 verification/audit 및 evidence/primary-reread.json에 있다. 최신 통합검산은 evidence/counts.json과통합audit에 연결한다.
