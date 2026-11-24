# AF-RES-180 자체점검 — PARTIAL
자체점검 기준: ④ 01514cabe44c67346747ca9e8d926ed527c82cd1의 고정 CSV/JSONL을 직접 다시 읽고 열 수, source ID 조인, 선택된 이슈 수, count=true 원자료 분류를 프로그램으로 비교했다. 외부 독립 검토는 NOT_RUN이다.

| 질문 | 답·근거 ID/URL | 불리한 설명·탐색 | 결과·미충족 |
|---|---|---|---|
| Q1 | L246/L262, I173563~I177059; [milestones](https://github.com/microsoft/vscode/milestones?state=closed) · issues.csv 64행 | terminal/debug 등 52개 배제, created asc와 번호 순서 비교, 원작성자 본문 수정 가능성 | 현재 목록 각 30/자연 4씩 충족, 최초 본문 revision 12건 미확인; 전체 과거 목록 archive 미확인 |
| Q2 | R1–R7,R9 [Issue Tracking](https://github.com/microsoft/vscode/wiki/Issue-Tracking) 및 [1.85 commands.json](https://github.com/microsoft/vscode/blob/1.85.0/.github/commands.json) | verified 선부여/삭제, bot /verified vs manual, I177059 자동 close/reopen | 고정 태그 설정 직접 확인; 실행 stable SHA·정확한 당시 wiki revision 미확인 |
| Q3 | P199503,P197283,P197117,P197038,P197291,P197511,P202026,P199952 및 A계열, [1.85](https://code.visualstudio.com/updates/v1_85), [1.86](https://code.visualstudio.com/updates/v1_86) | P89765 과거 별개 수정, P197291 vs P202026 view 조건, I31819 최초 재개 | 8 merge ancestry 확인, 최종 patch 4건 미확인; 실제 실행 미실시 |
| Q4 | I197268 [원제보자 재시험](https://github.com/microsoft/vscode/issues/197268#issuecomment-1832685935), I107778 [다른 사람](https://github.com/microsoft/vscode/issues/107778#issuecomment-1841367932), I200124 | I197268 이전 타인 라벨/질문; label only, 창 밖 및 same actor 다른 OS 비교 | 명령·결과 연결 원제보자 재시험 1건 관측 및 타인/봇 대조 확인. 빌드/fixture/hidden 전체 동일성, 원제보자=수정자 사례 미확인 |
| Q5 | I197319 [제한된 수용](https://github.com/microsoft/vscode/issues/197319#issuecomment-1798073330), [수정 전 설명 반응](https://github.com/microsoft/vscode/issues/197319#issuecomment-1793784107), I173563, I177059, I31819 | 동의 대상·시간·generator 변경, 명시 반대/재개, 감사와 실행 분리 | 긍정 반응 단독 실행으로 승격하지 않음. 삭제·비공개 반응 미확인 |
| Q6 | E1/E2, G1–G3 (sources.jsonl); [Greenwich 판정](https://www.lgo.org.uk/decisions/transport-and-highways/traffic-management/23-008-951) | 재심의 요구 객체 불일치, certificate/공사 완료 vs 사용자 실제 접근; G4 근접 자료; SeeClickFix 접근 실패 | 심사 원자료 2 및 공개 판정 3 직접 열람. 시민 원요청 직접 원문 및 완료 후 동일 조작 직접 재확인 미충족 |
| Q7 | claims.csv 12행, RESULT 표 3, C행 59 | verified=실행, 반응=통과, 재개=같은 결함이라는 경쟁 설명을 좁힘 | 12개 추천 문장 범위 제한. 동일 전체 조건 원제보자 확증은 보류; 설계 대안만 제시 |

## 분모와 자료 유형 점검
| 종류 | 예정 최소 | 직접 산입 | 비고 |
|---|---:|---:|---|
| 원 이슈 스레드 | 8 | 12 | 자연 8 + 보강 4, 같은 스레드 댓글/반응/timeline은 한 건 |
| 수정 PR·테스트 계획 | 5 | 9 | 연결 PR 8 및 이전 다른 요구 비교 P89765 1 |
| 당시 운영 규칙/봇 기록 | 3 | 8 | R8 현재 wiki 제외; 정확한 runtime SHA 불명 |
| 배포·검증 자료 | 2 | 2 | 공식 릴리스 노트; ancestry 8은 같은 PR lineage 추가 관측 |
| 심사와 공공 개선 요청·판정 | 4 | 5 | 학술 공개 XML 2 + Ombudsman 공식 판정 3; 시민 원요청/사후 직접 재시험 엄격 요건 미충족 |
| 합 | 22 | 36 | 고유 원자료 ID 36, lineage 36; 엄격 요건 때문에 PARTIAL |

- source ledger 전체 126행, 고유 ID 126, count=true 36; 미산입 90행은 목록/접근 실패/중복 lineage/추가 관측 등의 근거 기록이다. 직접 산입 분류: {"issue_thread":12,"fix_pr_test":9,"historical_rule_bot":8,"release_verification":2,"peer_civic_primary":5}.
- frame.csv 77행(모집 60+보강 및 탐색/실패/대조 행), 모집 자연 8 / 제외 52 / 빈자리 0 / 보강 4, 실제 상세 사건 12, issues.csv 64행. 현재 bug label 및 milestone 스냅샷. 
- timeline.jsonl 297 행; confirmations.csv 59행; 별도 실행/재현 진술 24행(사전 실패 포함; 사람/빌드 단위 독립 시험이 아님), 최초 창 6 / 최종 창 4 (CSV 표기 별도 대조: 최초/최종 각각 6/4). 창 분포 전체: 최초 {"before":22,"in":31,"out":6}, 최종 {"before":29,"in":25,"out":5}. 
- 원제보자 후속 텍스트 자연 8 모두 관측 없음(최초/최종 창 각각 0/8), 보강 I197268 1/1, I197319 3/1, I200124 0/0(라벨만), I177059 0/0. 동일 원조작 및 전체 환경의 사후 직접 성공 증거 0건 관측, 12건 전체 조건 미확인(부재 증명 아님).
- CSV 각 행 열 수 일치, 필수 source_id 연결 누락 0건, 고유 source ID 중복 0건. claims.csv 이슈 12, confirmations.csv 사례 12. ④에서 match_scope 및 날짜창 열 인덱스 보정. 실행 검증/대량 재계산/원영상 미열람을 직접 검사로 위장하지 않았다. 대표 파일은 묶음⑤ SHA에서 다시 읽고 최종 HANDOFF에 남긴다.

## 판정
PARTIAL — 최소 자료 유형 숫자는 충족하되, 동일 조건 전체를 확인한 원제보자 기록, 원제보자=수정자 반례, 시민 직접 요청 및 완료 후 직접 동작 원자료, 정확한 과거 정책 실행 SHA와 4건 최종 수정 SHA가 부족하다. 사람 독립 검토 미실시.
