# SELF_CHECK — AF-RES-258
자체 상태 **PARTIAL**: 고정 소스 추적 및 원자료 하한 충족. 동일 입력 저자 update 실행 시험 미확보(QUnit TODO), 신규 runtime·사용자 관측 미실행, A/B 독립 맹검 미실시. 자체 점검이지 독립 검토 아님.

| 질문 | 직접 근거·위치 | 자기 결론을 깨는 실제/탐색 반례 | 미확인·최소 다음 행동 |
|---|---|---|---|
| Q1 | J01 L60–80, J02 L112–122, J03 L81–103, J04 L162–165 | local position과 world matrix 불일치/zoom, A+ API만 추론 | 독립 A reader가 구현 없이 규칙 봉인 |
| Q2 | predictions.csv 24행, J01/T01–03, 봉인 6931ef0 | P4 B lower equality 오류; A 집합은 고유 답 아님 | A/B 정보 차단 새 평가 |
| Q3 | T01 L1176–1188/1514–1532, T05 L334–380/1045–1095, T06 L97–138, T04 L32–49, T07 L89–124 | T05와 T06 등호 다름, min runtime/NaN/dual mode, span vs setpoint | 실제 온도 기기 실측은 이 과제 밖; exact tag 코드 확인으로 충분한 규칙 증거 |
| Q4 | J04 L51–75,106–154,156–204; J05 L80–129,143–147; J08 diff/J09 issue | getObjectForDistance raw vs normalized, 최초 flag 외부 개입, update TODO | transfer.md 정확 입력 Node 실행, author update 동일 시험 재탐색 |
| Q5 | E01 L258–271/306–311, E02 L246–290, E03 L26–61, E04 L112–124, E05 L46–124; D01–04 | 화면 높이 2/16 at d100, timed/spatial fade, GPU Resident Drawer, parent-child, shadow batching, inspector state | 실제 renderer 설정/패널 영상 필요; 그림자 문제를 단계 전환으로 오인 금지 |
| Q6 | J04 L173–198; transitions.csv; T05/T06 | x=90 유지 vs 89.999 복귀, unknown initial, zero h, zoom | 동일 SHA flag/level raw receipts |
| Q7 | RESULT 표1/표2, 사전 6931ef0, J09 L135–143 | P1 C 적중, P4 B 오류; h0 동률, A+ 가능; 실제 차용 문장 없음 | 독립 blind A/B, 실측과 장치/사용자 반응은 별도 |

## 분모·산입·정정
- sources.jsonl parse 33행, 성공26/실패7; 산입24 distinct work_id (three8>=7, 온도7>=6, 타 엔진5>=5, 보고4>=4), 13 lineage. J09·D05 성공이나 보수적 미산입; X01–07 실패 미산입. 재열람/요청 총 횟수 미집계, 원장 기록 건수와 고유 자료수 분리. 묶음 종료 UTC만 기록. 네 경로는 자료수 제외. 일부 웹 원문 판/발행일 미확인 표시. 자료 그룹 동일 원저작 artifact 중복 제외, 동일 lineage 문서/코드는 별개 저작이지 독립 연구 아님.
- primary 4×3=12 endpoints, h0 별도12; 단계 10×3 per h. 소스 추적 20/20 프레임, 통제 별도 12 rows (transitions 총32). 실제 실행 0/20, 동일 경로 저자 시험 미확보 0/8, 정상 공석 0, 시각 관측 대상 밖/미확인. 예상·소스·저자 기대·실행을 분리. 원장/CSV 필드 완비 확인.
- 단계 행 재집계(데이터 비교만, 제품 실행 아님): A=4 singleton/6 미결, B=8/2, C=6/4. RESULT 첫 커밋 7c3ae0d6227cfc27b04992e21e8aca96efbc6441의 C 7/3 오기 발견, 6a83916c92c5a55dbf08e73fe54a063f8afdacaa에서 6/4로 정정; endpoint 변경 없음. 원판 예측 P4 B 오류는 그대로 보존. B′ 사후.
- 두 표는 RESULT 시작, 각각 요청 열과 단위/분모 및 마지막 3개 약점 행. B 대 A +3/-1/0, A 미결4; B 대 C +2/0/2. h0 모두 정확. C-mix 별도. 설계 인과·사용자 체감 확정 없음.
- 통합 base c64c54d2aae4045b0e2a28a1fdfca9f9313de765와 RESULT 정정 커밋 6a83916c92c5a55dbf08e73fe54a063f8afdacaa 비교: 7개 파일, owned_path 밖 0개, control 수정 없음. 통합·배포·실행 없음. 최종 HANDOFF는 별도 단독 커밋으로 작성. 
- 다음 첫 행동: transfer.md 명령을 정확 pin으로 별도 Codex 실행하여 stderr/stdout/exit/HEAD/node raw receipt 저장; 실패 기준에 따라 결과 재평가. 새 사용자 실측은 승인 후 별도 설계.