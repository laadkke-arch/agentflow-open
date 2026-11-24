# 경쟁 설명·반례·분야 전이 (묶음 ④)

## 관측과 변경 경계
- I197268/P197291/A197291: 숨겨진 탐색기에서 대상 선택이 누락되는 race 수정. 원제보자 mjbvz가 11/29 명령/선택을 특정해 재시험 통과 보고. 정확한 retest build/fixture/hidden state의 재진술 없음. 동일 요구(명령 실행 시 선택)가 개선됐다고 **보고했다**고 쓸 수 있으나 동일 전환경 확증은 아님. rzhao271의 선행 verified 후 질문, 다음 hooray는 서로 다른 행위이나 별도 테스트가 아님. I200124/P202026/A202026: 새 pane이 생성되지 않았을 때 getViewWithId가 null, 1월 openView 순서 수정. 동일 코드 근처이지만 별도 요구(showActiveFileInExplorer vs revealInExplorer); 첫 수정의 전범위 일반화를 반박. 원제보자 직접 라벨은 실행 증거 없음.
- I197319/P197511/A197511: 최초 close 반대→재개→수정. 원제보자와 다른 제보자가 링크 생성/URI를 바꿈. original heart는 bpasero의 workaround 설명(1793784107) 대상, PR merge 전; bot 요청에는 reaction 없음. /verified는 동작하고 있다고 말했으나 간헐 버그 재현 불가 및 원인 불확실도 함께 명시. bot label/수정자 thumbs-up을 독립 시험으로 셈하지 않음. 다른 사용자의 dialog 부재는 원문 실패와 동일하다고 가정 금지.
- I173563/P199503/A199503: Cmd-click default custom title 요구 vs right-click command center verification plan. native 변경 workaround는 통과 보고지만 동일 조건 아님; maintainer가 draggable region 제약 설명. penx는 다른 사용자의 조건부 수용/감사; 원제보자 확인 아님. verified label 붙어도 전체 titlebar 요구 미확인.
- I177059/P199952/A199952: 동일 원제보자 Windows에서 재현 불가, Mac에서 첫 click 실패, 다른 제보자도 실패. 자동 close는 R9 조건과 일치하는 관리 조치; reopen 및 최종 patch. 요청 및 타인 label은 마지막 close+30 밖. I31819: 최초 close 이틀 뒤 동일 증상 실패·reopen; 최종 closer notebook.css 예는 원 xterm.js Windows와 다름. 둘 다 첫 close와 final close 관찰창 분리.
- I107778: 다른 tester Mac에서 재현 불가, 원제보자의 뒤늦은 label을 독립 원시험으로 보지 않음. I127958: typed root path와 pasted nested path 구별; P89765는 전년도 별도 #32444 수정, 동일 링크 단어 유사성으로 최신 원요구 해결 추정 금지. I132428: closer 자신이 repro 오해 가능성 제기. I191667/I191799/I192113: 원문에 대응한 코드 변경 + label, 구체적 post-fix 실행 보고 없음.
- 자기보고자=수정자 반례: 선별 12건 중 링크된 8 PR의 원작성자와 PR 작성자는 다름. 선별 밖 X202839에서 원작성자의 code review acceptance를 실행과 구별했으나 원작성자=수정자 실례로 판정하지 못함; 별도 보강 한도 4 준수. 동일 사람의 PR+label은 독립 검증으로 승격 불가라는 규칙은 설계 추론이다.

## 분야 비교
| 원자료 | 요청 대상 키 | 수정/판정 주체 | 재확인 주체/범위 | 전이 금지 |
|---|---|---|---|---|
| E1 | Hairy loss-of-function에서 chromatin 변화/비억제 유전자 | 저자: 초기 다른 집단 기존 자료·후속 설명 | Reviewer 3: 요구한 집단 아님, reviewer 1 표현 개선 인정 | 논문 수락을 해당 실험 성공으로 승격 금지 |
| E2 | MBON-PAM 연결 기능적 sign | 저자: 해부·GRASP·NMDAR/행동 실험, 표현 완화 | 재심 전반 만족, 기능 imaging 없음; 저자도 생리학적 증명 미완 | accepted ≠ 기능 실측 |
| G1 | 특정 pavement 안전 이동/촉각 포장·폭·kerb | 시 개선 계획, Ombudsman complaint 처리 지연 인정/조치 | 주민 2023 재방문 개선 미미, 최종 실제 이동 재확인 미공개 | apology/meeting ≠ 안전 이동 |
| G2 | front ramp로 독립 출입 | OT는 rear lift 적합 판단, 시 ramp 완공, Ombudsman communication fault | 당사자/대리인 lift 거부; 완공 후에도 지연 불만 | 지연 불만 ≠ 현재 ramp 실패; 완료 ≠ 시험 |
| G3 | driveway car+wheelchair, garden access | building control certificate는 extension/remodel, council/contractor 작업 | caregiver 폭 문제, OT 설계 변경 미통지, adjudicator needs unmet | certificate scope ≠ user action |
| G4(보조) | 보행 crossing/road work 위치 | LCC 설치/완료 보고 | MDTC 별도 확인·부분 수리 보고 | resident same-use proof 없음 |

학술 저자는 VS Code fixer, reviewer는 독립 verifier/요구 제기자(일부 저자와 이해관계 다름), 편집자 결정은 close와 비슷하지만 동일하지 않다. 시민 신청자와 실사용자도 다를 수 있음(G2, G3); 당사자와 대리인을 별도 키로. LGO 원문 자체는 1차 공식 판정이지만 내부 인용/요약을 원제보자 발화 원본으로 처리하지 않는다. 시민 실제 최종 재시험을 보여주는 공개 원본 확보 실패(Z5; 검색 범위 FixMyStreet dropped kerb/wheelchair/fixed/still 및 SeeClickFix sidewalk/closed/reopened, LGO accessibility/council completed). 후보 재개: public original municipal ticket with requester identity stable, work order scope, signed update with same physical route/device after closure.

## 원장 보정
③의 match_scope/first_window index 오류를 ④에서 수정. 59 confirmation rows; 실행/재현에 관한 구별된 메시지 24 (동일 actor의 반복/실패/비교 포함, 통계적 독립 아님), 첫 close+30 내부 6, 마지막 close+30 내부 4; 원문 실행을 반복한 독립 실험 수는 알 수 없음. 연구자의 실행 0. 동일 명령·fixture·build·조건 전부 입증된 원제보자 post-fix 재시험 0 observed (missing, not proven absent). 원제보자가 특정 명령/결과를 직접 재시험했다고 말한 증거 I197268 1. I197319 author causal caveat. 자연 원작성자 30일 내 텍스트 댓글 관측 각 0, 공개 timeline 기준이며 private/deleted unknown. 보강 197268 1/1, 197319 3/1 (first/final), 200124 0/0 (direct label), 177059 0/0.
