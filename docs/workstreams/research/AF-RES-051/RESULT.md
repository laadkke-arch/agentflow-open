| 분야·run ID·조건 | 발행판·파일 URL·해시 | 실제 열린 경로·행·필드 | 출력 셀·원값·보고값 | 독립 정답·검증 위치 | 경로/내용/결과 기여 | 미확인 |
| --- | --- | --- | --- | --- | --- | --- |
| 통계 [S1-1](runs.jsonl#L1) C1 원본 | [88fed814](https://raw.githubusercontent.com/nychealth/coronavirus-data/88fed814aae58e2b92fd4df5e9fa1ae3dc81f965/trends/data-by-day.csv) D 71f2a36140cd… F 774609e1eba1… | statistics.csv 386행 BX·BK 값, 진단일 키 스캔 | S-BXBK-2021-03-19 · 469+831 = 1300명 → 1300명 | [GT-S1-1](evidence/truth-verification.jsonl#L1) · B-S 386행/별도 CSV · SQL·strace | 참 / 참 / 참 | 관측 범위 밖 I/O·후일 확정값 |
| 통계 [S1-2](runs.jsonl#L4) C1 원본 | [88fed814](https://raw.githubusercontent.com/nychealth/coronavirus-data/88fed814aae58e2b92fd4df5e9fa1ae3dc81f965/trends/data-by-day.csv) D 71f2a36140cd… F 774609e1eba1… | statistics.csv 386행 BX·BK 값, 진단일 키 스캔 | S-BXBK-2021-03-19 · 469+831 = 1300명 → 1300명 | [GT-S1-2](evidence/truth-verification.jsonl#L2) · B-S 386행/별도 CSV · SQL·strace | 참 / 참 / 참 | 관측 범위 밖 I/O·후일 확정값 |
| 통계 [S2-1](runs.jsonl#L7) C2 복사 | [88fed814](https://raw.githubusercontent.com/nychealth/coronavirus-data/88fed814aae58e2b92fd4df5e9fa1ae3dc81f965/trends/data-by-day.csv) D 71f2a36140cd… F 774609e1eba1… | statistics.csv 386행 BX·BK 값, 진단일 키 스캔 · extra/statistics.csv 열기 관측 0 | S-BXBK-2021-03-19 · 469+831 = 1300명 → 1300명 | [GT-S2-1](evidence/truth-verification.jsonl#L3) · B-S 386행/별도 CSV · SQL·strace | 거짓 / 참 / 거짓 | 관측 범위 밖 I/O·후일 확정값 |
| 통계 [S2-2](runs.jsonl#L10) C2 복사 | [88fed814](https://raw.githubusercontent.com/nychealth/coronavirus-data/88fed814aae58e2b92fd4df5e9fa1ae3dc81f965/trends/data-by-day.csv) D 71f2a36140cd… F 774609e1eba1… | statistics.csv 386행 BX·BK 값, 진단일 키 스캔 · extra/statistics.csv 열기 관측 0 | S-BXBK-2021-03-19 · 469+831 = 1300명 → 1300명 | [GT-S2-2](evidence/truth-verification.jsonl#L4) · B-S 386행/별도 CSV · SQL·strace | 거짓 / 참 / 거짓 | 관측 범위 밖 I/O·후일 확정값 |
| 통계 [S3-1](runs.jsonl#L13) C3 헤더 | [88fed814](https://raw.githubusercontent.com/nychealth/coronavirus-data/88fed814aae58e2b92fd4df5e9fa1ae3dc81f965/trends/data-by-day.csv) D 71f2a36140cd… F 774609e1eba1… · probe 3e2b4e6c087d… | probe/statistics.csv 헤더 1377 B · statistics.csv 386행 BX·BK 값, 진단일 키 스캔 | S-BXBK-2021-03-19 · 469+831 = 1300명 → 1300명 | [GT-S3-1](evidence/truth-verification.jsonl#L5) · B-S 386행/별도 CSV · SQL·strace | 참 / 거짓 / 거짓 | 관측 범위 밖 I/O·후일 확정값 |
| 통계 [S3-2](runs.jsonl#L16) C3 헤더 | [88fed814](https://raw.githubusercontent.com/nychealth/coronavirus-data/88fed814aae58e2b92fd4df5e9fa1ae3dc81f965/trends/data-by-day.csv) D 71f2a36140cd… F 774609e1eba1… · probe 3e2b4e6c087d… | probe/statistics.csv 헤더 1377 B · statistics.csv 386행 BX·BK 값, 진단일 키 스캔 | S-BXBK-2021-03-19 · 469+831 = 1300명 → 1300명 | [GT-S3-2](evidence/truth-verification.jsonl#L6) · B-S 386행/별도 CSV · SQL·strace | 참 / 거짓 / 거짓 | 관측 범위 밖 I/O·후일 확정값 |
| 통계 [S4-1](runs.jsonl#L19) C4 경계 | [88fed814](https://raw.githubusercontent.com/nychealth/coronavirus-data/88fed814aae58e2b92fd4df5e9fa1ae3dc81f965/trends/data-by-day.csv) D 71f2a36140cd… F 774609e1eba1… | statistics.csv 386행 BX·BK 값, 진단일 키 스캔 | S-BXBK-2021-03-19 · 469+831 = 1300명 → 1300명 | [GT-S4-1](evidence/truth-verification.jsonl#L7) · B-S 386행/별도 CSV · SQL·strace | 참 / 참 / 거짓 | 관측 범위 밖 I/O·후일 확정값 |
| 통계 [S4-2](runs.jsonl#L22) C4 경계 | [88fed814](https://raw.githubusercontent.com/nychealth/coronavirus-data/88fed814aae58e2b92fd4df5e9fa1ae3dc81f965/trends/data-by-day.csv) D 71f2a36140cd… F 774609e1eba1… | statistics.csv 386행 BX·BK 값, 진단일 키 스캔 | S-BXBK-2021-03-19 · 469+831 = 1300명 → 1300명 | [GT-S4-2](evidence/truth-verification.jsonl#L8) · B-S 386행/별도 CSV · SQL·strace | 참 / 참 / 거짓 | 관측 범위 밖 I/O·후일 확정값 |
| 교통 [T1-1](runs.jsonl#L25) C1 원본 | [2ce6aa79](https://raw.githubusercontent.com/google/transit/2ce6aa79e3fa7bdbaf19d2a12765cee5b9fdd699/gtfs/spec/en/examples/sample-feed-1.zip) D 46404f91b8f8… F 426755e489ba… | routes 6행 route_id, calendar 2·3행 서비스·요일·기간, calendar_dates 2행 날짜·예외, trips 9–12행 trip_id·direction_id | T-AAMV-2007-01-06-D0 · AAMV1/3 · 2→2 trip ID | [GT-T1-1](evidence/truth-verification.jsonl#L9) · B-T ZIP/별도 txt · SQL·strace | 참 / 참 / 참 | 실 운행·독립 발행 feed_version |
| 교통 [T1-2](runs.jsonl#L28) C1 원본 | [2ce6aa79](https://raw.githubusercontent.com/google/transit/2ce6aa79e3fa7bdbaf19d2a12765cee5b9fdd699/gtfs/spec/en/examples/sample-feed-1.zip) D 46404f91b8f8… F 426755e489ba… | routes 6행 route_id, calendar 2·3행 서비스·요일·기간, calendar_dates 2행 날짜·예외, trips 9–12행 trip_id·direction_id | T-AAMV-2007-01-06-D0 · AAMV1/3 · 2→2 trip ID | [GT-T1-2](evidence/truth-verification.jsonl#L10) · B-T ZIP/별도 txt · SQL·strace | 참 / 참 / 참 | 실 운행·독립 발행 feed_version |
| 교통 [T2-1](runs.jsonl#L31) C2 복사 | [2ce6aa79](https://raw.githubusercontent.com/google/transit/2ce6aa79e3fa7bdbaf19d2a12765cee5b9fdd699/gtfs/spec/en/examples/sample-feed-1.zip) D 46404f91b8f8… F 426755e489ba… | routes 6행 route_id, calendar 2·3행 서비스·요일·기간, calendar_dates 2행 날짜·예외, trips 9–12행 trip_id·direction_id · extra/trips.txt 열기 관측 0 | T-AAMV-2007-01-06-D0 · AAMV1/3 · 2→2 trip ID | [GT-T2-1](evidence/truth-verification.jsonl#L11) · B-T ZIP/별도 txt · SQL·strace | 거짓 / 참 / 거짓 | 실 운행·독립 발행 feed_version |
| 교통 [T2-2](runs.jsonl#L34) C2 복사 | [2ce6aa79](https://raw.githubusercontent.com/google/transit/2ce6aa79e3fa7bdbaf19d2a12765cee5b9fdd699/gtfs/spec/en/examples/sample-feed-1.zip) D 46404f91b8f8… F 426755e489ba… | routes 6행 route_id, calendar 2·3행 서비스·요일·기간, calendar_dates 2행 날짜·예외, trips 9–12행 trip_id·direction_id · extra/trips.txt 열기 관측 0 | T-AAMV-2007-01-06-D0 · AAMV1/3 · 2→2 trip ID | [GT-T2-2](evidence/truth-verification.jsonl#L12) · B-T ZIP/별도 txt · SQL·strace | 거짓 / 참 / 거짓 | 실 운행·독립 발행 feed_version |
| 교통 [T3-1](runs.jsonl#L37) C3 헤더 | [2ce6aa79](https://raw.githubusercontent.com/google/transit/2ce6aa79e3fa7bdbaf19d2a12765cee5b9fdd699/gtfs/spec/en/examples/sample-feed-1.zip) D 46404f91b8f8… F 426755e489ba… · probe b3756864dfc7… | probe/trips.txt 헤더 74 B · routes 6행 route_id, calendar 2·3행 서비스·요일·기간, calendar_dates 2행 날짜·예외, trips 9–12행 trip_id·direction_id | T-AAMV-2007-01-06-D0 · AAMV1/3 · 2→2 trip ID | [GT-T3-1](evidence/truth-verification.jsonl#L13) · B-T ZIP/별도 txt · SQL·strace | 참 / 거짓 / 거짓 | 실 운행·독립 발행 feed_version |
| 교통 [T3-2](runs.jsonl#L40) C3 헤더 | [2ce6aa79](https://raw.githubusercontent.com/google/transit/2ce6aa79e3fa7bdbaf19d2a12765cee5b9fdd699/gtfs/spec/en/examples/sample-feed-1.zip) D 46404f91b8f8… F 426755e489ba… · probe b3756864dfc7… | probe/trips.txt 헤더 74 B · routes 6행 route_id, calendar 2·3행 서비스·요일·기간, calendar_dates 2행 날짜·예외, trips 9–12행 trip_id·direction_id | T-AAMV-2007-01-06-D0 · AAMV1/3 · 2→2 trip ID | [GT-T3-2](evidence/truth-verification.jsonl#L14) · B-T ZIP/별도 txt · SQL·strace | 참 / 거짓 / 거짓 | 실 운행·독립 발행 feed_version |
| 교통 [T4-1](runs.jsonl#L43) C4 경계 | [2ce6aa79](https://raw.githubusercontent.com/google/transit/2ce6aa79e3fa7bdbaf19d2a12765cee5b9fdd699/gtfs/spec/en/examples/sample-feed-1.zip) D 46404f91b8f8… F 426755e489ba… | routes 6행 route_id, calendar 2·3행 서비스·요일·기간, calendar_dates 2행 날짜·예외, trips 9–12행 trip_id·direction_id · AAMV2(10행) 제외 | T-AAMV-2007-01-06-D0 · AAMV1/3 · 2→2 trip ID | [GT-T4-1](evidence/truth-verification.jsonl#L15) · B-T ZIP/별도 txt · SQL·strace | 참 / 거짓 / 거짓 | 실 운행·독립 발행 feed_version |
| 교통 [T4-2](runs.jsonl#L46) C4 경계 | [2ce6aa79](https://raw.githubusercontent.com/google/transit/2ce6aa79e3fa7bdbaf19d2a12765cee5b9fdd699/gtfs/spec/en/examples/sample-feed-1.zip) D 46404f91b8f8… F 426755e489ba… | routes 6행 route_id, calendar 2·3행 서비스·요일·기간, calendar_dates 2행 날짜·예외, trips 9–12행 trip_id·direction_id · AAMV2(10행) 제외 | T-AAMV-2007-01-06-D0 · AAMV1/3 · 2→2 trip ID | [GT-T4-2](evidence/truth-verification.jsonl#L16) · B-T ZIP/별도 txt · SQL·strace | 참 / 거짓 / 거짓 | 실 운행·독립 발행 feed_version |

| 같은 run ID·기록 방식 | 물은 사실 | 사전 규칙의 판정 | 검증된 정답 | 거짓 양성·거짓 음성·보류·일치 | 추가 필드·바이트 | 근거 주소·행 | 한계 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1-1 P0 | A/K/R/I | 미·미·미·미 | 확·확·확·확 | 보류4 / 지름길 일치4 | +2 필드 +218 B / 218 B | [PK-S1-1-P0](packets.csv#L2) · [D-S1-1-P0 2–5행](decisions.csv#L2) | 주소와 의도 |
| S1-1 P1 | A/K/R/I | 미·미·미·확 | 확·확·확·확 | 보류3 일치1 / 지름길 일치4 | +4 필드 +319 B / 537 B | [PK-S1-1-P1](packets.csv#L3) · [D-S1-1-P1 6–9행](decisions.csv#L6) | 발행 객체 바이트 대조 |
| S1-1 P2 | A/K/R/I | 확·확·확·확 | 확·확·확·확 | 일치4 | +7 필드 +650 B / 1187 B | [PK-S1-1-P2](packets.csv#L4) · [D-S1-1-P2 10–13행](decisions.csv#L10) | 통제 자식의 명시적 조회 범위 |
| S1-2 P0 | A/K/R/I | 미·미·미·미 | 확·확·확·확 | 보류4 / 지름길 일치4 | +2 필드 +218 B / 218 B | [PK-S1-2-P0](packets.csv#L5) · [D-S1-2-P0 14–17행](decisions.csv#L14) | 주소와 의도 |
| S1-2 P1 | A/K/R/I | 미·미·미·확 | 확·확·확·확 | 보류3 일치1 / 지름길 일치4 | +4 필드 +319 B / 537 B | [PK-S1-2-P1](packets.csv#L6) · [D-S1-2-P1 18–21행](decisions.csv#L18) | 발행 객체 바이트 대조 |
| S1-2 P2 | A/K/R/I | 확·확·확·확 | 확·확·확·확 | 일치4 | +7 필드 +650 B / 1187 B | [PK-S1-2-P2](packets.csv#L7) · [D-S1-2-P2 22–25행](decisions.csv#L22) | 통제 자식의 명시적 조회 범위 |
| S2-1 P0 | A/K/R/I | 미·미·미·미 | 반·반·반·확 | 보류4 / 지름길 FP3 일치1 | +2 필드 +218 B / 218 B | [PK-S2-1-P0](packets.csv#L8) · [D-S2-1-P0 26–29행](decisions.csv#L26) | 주소와 의도 |
| S2-1 P1 | A/K/R/I | 미·미·미·확 | 반·반·반·확 | 보류3 일치1 / 지름길 FP3 일치1 | +4 필드 +319 B / 537 B | [PK-S2-1-P1](packets.csv#L9) · [D-S2-1-P1 30–33행](decisions.csv#L30) | 발행 객체 바이트 대조 |
| S2-1 P2 | A/K/R/I | 반·반·반·확 | 반·반·반·확 | 일치4 | +7 필드 +673 B / 1210 B | [PK-S2-1-P2](packets.csv#L10) · [D-S2-1-P2 34–37행](decisions.csv#L34) | 통제 자식의 명시적 조회 범위 |
| S2-2 P0 | A/K/R/I | 미·미·미·미 | 반·반·반·확 | 보류4 / 지름길 FP3 일치1 | +2 필드 +218 B / 218 B | [PK-S2-2-P0](packets.csv#L11) · [D-S2-2-P0 38–41행](decisions.csv#L38) | 주소와 의도 |
| S2-2 P1 | A/K/R/I | 미·미·미·확 | 반·반·반·확 | 보류3 일치1 / 지름길 FP3 일치1 | +4 필드 +319 B / 537 B | [PK-S2-2-P1](packets.csv#L12) · [D-S2-2-P1 42–45행](decisions.csv#L42) | 발행 객체 바이트 대조 |
| S2-2 P2 | A/K/R/I | 반·반·반·확 | 반·반·반·확 | 일치4 | +7 필드 +673 B / 1210 B | [PK-S2-2-P2](packets.csv#L13) · [D-S2-2-P2 46–49행](decisions.csv#L46) | 통제 자식의 명시적 조회 범위 |
| S3-1 P0 | A/K/R/I | 미·미·미·미 | 확·반·반·반 | 보류4 / 지름길 FP3 일치1 | +2 필드 +218 B / 218 B | [PK-S3-1-P0](packets.csv#L14) · [D-S3-1-P0 50–53행](decisions.csv#L50) | 주소와 의도 |
| S3-1 P1 | A/K/R/I | 미·미·미·반 | 확·반·반·반 | 보류3 일치1 / 지름길 FN1 일치3 | +4 필드 +319 B / 537 B | [PK-S3-1-P1](packets.csv#L15) · [D-S3-1-P1 54–57행](decisions.csv#L54) | 발행 객체 바이트 대조 |
| S3-1 P2 | A/K/R/I | 확·반·반·반 | 확·반·반·반 | 일치4 | +7 필드 +754 B / 1291 B | [PK-S3-1-P2](packets.csv#L16) · [D-S3-1-P2 58–61행](decisions.csv#L58) | 통제 자식의 명시적 조회 범위 |
| S3-2 P0 | A/K/R/I | 미·미·미·미 | 확·반·반·반 | 보류4 / 지름길 FP3 일치1 | +2 필드 +218 B / 218 B | [PK-S3-2-P0](packets.csv#L17) · [D-S3-2-P0 62–65행](decisions.csv#L62) | 주소와 의도 |
| S3-2 P1 | A/K/R/I | 미·미·미·반 | 확·반·반·반 | 보류3 일치1 / 지름길 FN1 일치3 | +4 필드 +319 B / 537 B | [PK-S3-2-P1](packets.csv#L18) · [D-S3-2-P1 66–69행](decisions.csv#L66) | 발행 객체 바이트 대조 |
| S3-2 P2 | A/K/R/I | 확·반·반·반 | 확·반·반·반 | 일치4 | +7 필드 +754 B / 1291 B | [PK-S3-2-P2](packets.csv#L19) · [D-S3-2-P2 70–73행](decisions.csv#L70) | 통제 자식의 명시적 조회 범위 |
| S4-1 P0 | A/K/R/I | 미·미·미·미 | 확·확·반·확 | 보류4 / 지름길 FP1 일치3 | +2 필드 +218 B / 218 B | [PK-S4-1-P0](packets.csv#L20) · [D-S4-1-P0 74–77행](decisions.csv#L74) | 주소와 의도 |
| S4-1 P1 | A/K/R/I | 미·미·미·확 | 확·확·반·확 | 보류3 일치1 / 지름길 FP1 일치3 | +4 필드 +319 B / 537 B | [PK-S4-1-P1](packets.csv#L21) · [D-S4-1-P1 78–81행](decisions.csv#L78) | 발행 객체 바이트 대조 |
| S4-1 P2 | A/K/R/I | 확·확·반·확 | 확·확·반·확 | 일치4 | +7 필드 +650 B / 1187 B | [PK-S4-1-P2](packets.csv#L22) · [D-S4-1-P2 82–85행](decisions.csv#L82) | 통제 자식의 명시적 조회 범위 |
| S4-2 P0 | A/K/R/I | 미·미·미·미 | 확·확·반·확 | 보류4 / 지름길 FP1 일치3 | +2 필드 +218 B / 218 B | [PK-S4-2-P0](packets.csv#L23) · [D-S4-2-P0 86–89행](decisions.csv#L86) | 주소와 의도 |
| S4-2 P1 | A/K/R/I | 미·미·미·확 | 확·확·반·확 | 보류3 일치1 / 지름길 FP1 일치3 | +4 필드 +319 B / 537 B | [PK-S4-2-P1](packets.csv#L24) · [D-S4-2-P1 90–93행](decisions.csv#L90) | 발행 객체 바이트 대조 |
| S4-2 P2 | A/K/R/I | 확·확·반·확 | 확·확·반·확 | 일치4 | +7 필드 +650 B / 1187 B | [PK-S4-2-P2](packets.csv#L25) · [D-S4-2-P2 94–97행](decisions.csv#L94) | 통제 자식의 명시적 조회 범위 |
| T1-1 P0 | A/K/R/I | 미·미·미·미 | 확·확·확·확 | 보류4 / 지름길 일치4 | +2 필드 +222 B / 222 B | [PK-T1-1-P0](packets.csv#L26) · [D-T1-1-P0 98–101행](decisions.csv#L98) | 주소와 의도 |
| T1-1 P1 | A/K/R/I | 미·미·미·확 | 확·확·확·확 | 보류3 일치1 / 지름길 일치4 | +4 필드 +319 B / 541 B | [PK-T1-1-P1](packets.csv#L27) · [D-T1-1-P1 102–105행](decisions.csv#L102) | 발행 객체 바이트 대조 |
| T1-1 P2 | A/K/R/I | 확·확·확·확 | 확·확·확·확 | 일치4 | +7 필드 +2974 B / 3515 B | [PK-T1-1-P2](packets.csv#L28) · [D-T1-1-P2 106–109행](decisions.csv#L106) | 통제 자식의 명시적 조회 범위 |
| T1-2 P0 | A/K/R/I | 미·미·미·미 | 확·확·확·확 | 보류4 / 지름길 일치4 | +2 필드 +222 B / 222 B | [PK-T1-2-P0](packets.csv#L29) · [D-T1-2-P0 110–113행](decisions.csv#L110) | 주소와 의도 |
| T1-2 P1 | A/K/R/I | 미·미·미·확 | 확·확·확·확 | 보류3 일치1 / 지름길 일치4 | +4 필드 +319 B / 541 B | [PK-T1-2-P1](packets.csv#L30) · [D-T1-2-P1 114–117행](decisions.csv#L114) | 발행 객체 바이트 대조 |
| T1-2 P2 | A/K/R/I | 확·확·확·확 | 확·확·확·확 | 일치4 | +7 필드 +2974 B / 3515 B | [PK-T1-2-P2](packets.csv#L31) · [D-T1-2-P2 118–121행](decisions.csv#L118) | 통제 자식의 명시적 조회 범위 |
| T2-1 P0 | A/K/R/I | 미·미·미·미 | 반·반·반·확 | 보류4 / 지름길 FP3 일치1 | +2 필드 +222 B / 222 B | [PK-T2-1-P0](packets.csv#L32) · [D-T2-1-P0 122–125행](decisions.csv#L122) | 주소와 의도 |
| T2-1 P1 | A/K/R/I | 미·미·미·확 | 반·반·반·확 | 보류3 일치1 / 지름길 FP3 일치1 | +4 필드 +319 B / 541 B | [PK-T2-1-P1](packets.csv#L33) · [D-T2-1-P1 126–129행](decisions.csv#L126) | 발행 객체 바이트 대조 |
| T2-1 P2 | A/K/R/I | 반·반·반·확 | 반·반·반·확 | 일치4 | +7 필드 +2992 B / 3533 B | [PK-T2-1-P2](packets.csv#L34) · [D-T2-1-P2 130–133행](decisions.csv#L130) | 통제 자식의 명시적 조회 범위 |
| T2-2 P0 | A/K/R/I | 미·미·미·미 | 반·반·반·확 | 보류4 / 지름길 FP3 일치1 | +2 필드 +222 B / 222 B | [PK-T2-2-P0](packets.csv#L35) · [D-T2-2-P0 134–137행](decisions.csv#L134) | 주소와 의도 |
| T2-2 P1 | A/K/R/I | 미·미·미·확 | 반·반·반·확 | 보류3 일치1 / 지름길 FP3 일치1 | +4 필드 +319 B / 541 B | [PK-T2-2-P1](packets.csv#L36) · [D-T2-2-P1 138–141행](decisions.csv#L138) | 발행 객체 바이트 대조 |
| T2-2 P2 | A/K/R/I | 반·반·반·확 | 반·반·반·확 | 일치4 | +7 필드 +2992 B / 3533 B | [PK-T2-2-P2](packets.csv#L37) · [D-T2-2-P2 142–145행](decisions.csv#L142) | 통제 자식의 명시적 조회 범위 |
| T3-1 P0 | A/K/R/I | 미·미·미·미 | 확·반·반·반 | 보류4 / 지름길 FP3 일치1 | +2 필드 +222 B / 222 B | [PK-T3-1-P0](packets.csv#L38) · [D-T3-1-P0 146–149행](decisions.csv#L146) | 주소와 의도 |
| T3-1 P1 | A/K/R/I | 미·미·미·반 | 확·반·반·반 | 보류3 일치1 / 지름길 FN1 일치3 | +4 필드 +319 B / 541 B | [PK-T3-1-P1](packets.csv#L39) · [D-T3-1-P1 150–153행](decisions.csv#L150) | 발행 객체 바이트 대조 |
| T3-1 P2 | A/K/R/I | 확·반·반·반 | 확·반·반·반 | 일치4 | +7 필드 +3065 B / 3606 B | [PK-T3-1-P2](packets.csv#L40) · [D-T3-1-P2 154–157행](decisions.csv#L154) | 통제 자식의 명시적 조회 범위 |
| T3-2 P0 | A/K/R/I | 미·미·미·미 | 확·반·반·반 | 보류4 / 지름길 FP3 일치1 | +2 필드 +222 B / 222 B | [PK-T3-2-P0](packets.csv#L41) · [D-T3-2-P0 158–161행](decisions.csv#L158) | 주소와 의도 |
| T3-2 P1 | A/K/R/I | 미·미·미·반 | 확·반·반·반 | 보류3 일치1 / 지름길 FN1 일치3 | +4 필드 +319 B / 541 B | [PK-T3-2-P1](packets.csv#L42) · [D-T3-2-P1 162–165행](decisions.csv#L162) | 발행 객체 바이트 대조 |
| T3-2 P2 | A/K/R/I | 확·반·반·반 | 확·반·반·반 | 일치4 | +7 필드 +3065 B / 3606 B | [PK-T3-2-P2](packets.csv#L43) · [D-T3-2-P2 166–169행](decisions.csv#L166) | 통제 자식의 명시적 조회 범위 |
| T4-1 P0 | A/K/R/I | 미·미·미·미 | 확·확·반·확 | 보류4 / 지름길 FP1 일치3 | +2 필드 +222 B / 222 B | [PK-T4-1-P0](packets.csv#L44) · [D-T4-1-P0 170–173행](decisions.csv#L170) | 주소와 의도 |
| T4-1 P1 | A/K/R/I | 미·미·미·확 | 확·확·반·확 | 보류3 일치1 / 지름길 FP1 일치3 | +4 필드 +319 B / 541 B | [PK-T4-1-P1](packets.csv#L45) · [D-T4-1-P1 174–177행](decisions.csv#L174) | 발행 객체 바이트 대조 |
| T4-1 P2 | A/K/R/I | 확·확·반·확 | 확·확·반·확 | 일치4 | +7 필드 +2974 B / 3515 B | [PK-T4-1-P2](packets.csv#L46) · [D-T4-1-P2 178–181행](decisions.csv#L178) | 통제 자식의 명시적 조회 범위 |
| T4-2 P0 | A/K/R/I | 미·미·미·미 | 확·확·반·확 | 보류4 / 지름길 FP1 일치3 | +2 필드 +222 B / 222 B | [PK-T4-2-P0](packets.csv#L47) · [D-T4-2-P0 182–185행](decisions.csv#L182) | 주소와 의도 |
| T4-2 P1 | A/K/R/I | 미·미·미·확 | 확·확·반·확 | 보류3 일치1 / 지름길 FP1 일치3 | +4 필드 +319 B / 541 B | [PK-T4-2-P1](packets.csv#L48) · [D-T4-2-P1 186–189행](decisions.csv#L186) | 발행 객체 바이트 대조 |
| T4-2 P2 | A/K/R/I | 확·확·반·확 | 확·확·반·확 | 일치4 | +7 필드 +2974 B / 3515 B | [PK-T4-2-P2](packets.csv#L49) · [D-T4-2-P2 190–193행](decisions.csv#L190) | 통제 자식의 명시적 조회 범위 |

두 표의 주 실행은 **관측 16/16**이다. 두 번째 표는 **관측 48/48 구성**, 구성별 4사실로 **192/192 판정**이다. A는 대상 경로 열기, K는 대상 행·필드 조회, R은 사전 지정한 변경에 대한 보고값 변화, I는 지목한 발행 멤버의 전체 바이트 동일성이다. 순서는 A/K/R/I이며 확·반·미는 확인·반증·미확인이다. 표 1의 세 판단은 경로 열기·산식에 들어간 동일 내용·국소 보고 감도 순서다. D는 배포 단위, F는 발행 파일/멤버의 SHA256 접두사다. 전체 해시와 후보 경로의 해시를 함께 확인할 수 있다. [입력 원장](evidence/inputs.json) · [주 실행 원장](runs.jsonl)

## Q1. 발행판과 선택 필드

**확인.** NYC DOHMH는 Git 커밋으로 발행 스냅샷을 고정한다. D는 루트 Git 트리의 raw manifest 바이트, F는 공식 CSV 전체다. 원본 행 키는 진단일 `03/19/2021`이고 두 측정은 Bronx와 Brooklyn의 일별 확진자 수다. 보고일과 기준일을 따로 둔다. 사전 68행에서 INCOMPLETE는 표시용 보조 열로 정의된다. 합과 100명 단위 반올림은 이번 통제 산식이다. [S01](https://raw.githubusercontent.com/nychealth/coronavirus-data/88fed814aae58e2b92fd4df5e9fa1ae3dc81f965/trends/data-by-day.csv) · [S03](https://raw.githubusercontent.com/nychealth/coronavirus-data/a1dcaf47997accb4bc601f18d63b943815536f83/README.md) · [S10](https://raw.githubusercontent.com/nychealth/coronavirus-data/88fed814aae58e2b92fd4df5e9fa1ae3dc81f965/trends/Readme.md)

GTFS 예제의 D는 ZIP 전체, F는 정확한 ZIP 멤버 `trips.txt`다. `routes.route_id=AAMV`를 `trips.route_id`와 조인하고 날짜별 활성 `service_id`와 상대 방향 0을 고른다. 기준일은 `America/Los_Angeles`의 2007-01-06이다. 예제 ZIP의 서비스 범위는 2007-01-01~2010-12-31이고 `feed_info.txt`는 없다. Cairo 예제는 `feed_version=0.5`와 서비스 시작·끝을 별도로 선언한다. MBTA도 아카이브의 효력일과 버전 이름을 별도 열로 둔다. [T01](https://raw.githubusercontent.com/google/transit/2ce6aa79e3fa7bdbaf19d2a12765cee5b9fdd699/gtfs/spec/en/examples/sample-feed-1.zip) · [T03](https://raw.githubusercontent.com/transportforcairo/Metro-GTFS/9f65d9f17a8c38faeda585b1c59d5be65fc2f3e3/feed_info.txt) · [T02](https://cdn.mbta.com/archive/archived_feeds.txt) · [T10](https://gtfs.org/documentation/schedule/reference/)

| 이름이나 값이 같은 경우 | 확인한 차이 | 근거 |
| --- | --- | --- |
| 같은 노선명 Airport - Amargosa Valley | 방향 0의 AAMV1·AAMV3과 방향 1의 AAMV2·AAMV4 | [T01](https://raw.githubusercontent.com/google/transit/2ce6aa79e3fa7bdbaf19d2a12765cee5b9fdd699/gtfs/spec/en/examples/sample-feed-1.zip) routes 6행, trips 9–12행 |
| 같은 지역 Bronx | 누적 CASE_COUNT 134314명과 CASE_RATE 9470.69명/10만 명 | [S05](https://raw.githubusercontent.com/nychealth/coronavirus-data/88fed814aae58e2b92fd4df5e9fa1ae3dc81f965/totals/by-boro.csv) 2행 · [S11](https://raw.githubusercontent.com/nychealth/coronavirus-data/88fed814aae58e2b92fd4df5e9fa1ae3dc81f965/totals/Readme.md) 117–136행 |
| 같은 값 228 | Bronx 일별 확진 건수 2021-03-14, 2021-03-20 | [S01](https://raw.githubusercontent.com/nychealth/coronavirus-data/88fed814aae58e2b92fd4df5e9fa1ae3dc81f965/trends/data-by-day.csv) 381·387행 |

## Q2. 실행이 본 것과 읽은 것

**확인.** 파일은 준비 단계에서 해시와 후보 목록을 만들었다. 각 새 분석 자식은 해당 local fixture에만 접근했다. GTFS 11개 멤버 중 `routes.txt`, `calendar.txt`, `calendar_dates.txt`, `trips.txt` 네 개가 주 변환에 들어갔다. `agency.txt`의 시간대와 `frequencies.txt`가 AAMV에 적용되지 않는 사실은 발행물 확인 단계에서 읽었다. 출발 횟수로 확장한 결과나 실제 운행을 추론하려면 별도 근거가 필요하다. [T01](https://raw.githubusercontent.com/google/transit/2ce6aa79e3fa7bdbaf19d2a12765cee5b9fdd699/gtfs/spec/en/examples/sample-feed-1.zip) · [T10](https://gtfs.org/documentation/schedule/reference/) · [입력 목록과 의존](evidence/inputs.json)

**확인.** 애플리케이션 I/O 이벤트와 Linux `strace -yy`의 fixture 경로가 일치했다. C3의 probe는 통계 1377 B, 교통 74 B까지만 읽었다. 날짜/노선 후보의 바이트 파싱, 논리 필드 명시 조회, 산식에 반영된 키를 각각 남겼다. 선행 취득·캐시 읽기, 선택되지 않은 라이브러리 경로, 이 자식 외부의 프로세스와 기존 공개 소비자의 실행은 **미확인**이다. [X01–X04](evidence/contrasts.md) · [실행 영수증](evidence/execution.json)

## Q3. 정답의 독립성

**확인.** 구조 정답 `truth.csv`를 먼저 고정했다. 실행 전 원표에서 AWK가 별도 공개 표현으로 읽은 469와 831을 손으로 합해 1300을 고정했다. GTFS는 `unzip -p`와 번호화한 원표에서 1월 6일 토요일, `WE`, AAMV1·AAMV3을 대조해 2를 고정했다. 코드 실행에서도 별도 plain-line 입력·SQLite 조인으로 원값·보고값을 검산했다. 운영체제로 후보 경로를 확인했고 정확한 한 행의 사전 참조를 가로채는 별도 진단 자식으로 키 조회를 대조했다. 양성 8회는 조회 위치를 발견했고 음성 8회는 같은 조회로 들어가지 않았다. 32개 한 셀 짝의 값·관계가 봉인값과 맞았다. 별도 파일 표현은 같은 발행자 계보여서 독립 생산 관측은 **미확인**이다. [S14](https://raw.githubusercontent.com/nychealth/coronavirus-data/88fed814aae58e2b92fd4df5e9fa1ae3dc81f965/trends/cases-by-day.csv) · [T01b](https://raw.githubusercontent.com/google/transit/2ce6aa79e3fa7bdbaf19d2a12765cee5b9fdd699/gtfs/spec/en/examples/sample-feed-1/trips.txt) · [사전 기준선](evidence/baseline.json) · [정답 검증 행](evidence/truth-verification.jsonl) · [짝 원장](evidence/pairs.csv)

## Q4. 기록 방식별 판정과 오판

| 방식 | 주 규칙 일치 / 정답 관측 | 주 규칙 거짓 양성·거짓 음성·보류 | 지름길 일치·거짓 양성·거짓 음성 / 64 | 구성당 추가 필드 | 총 JSON B / 전 단계 추가 B |
| --- | --- | --- | --- | --- | --- |
| P0 | 관측 0 / 64 | 관측 0 · 관측 0 · 64 | 36 · 28 · 관측 0 | 2 | 3520 / +3520 |
| P1 | 16 / 64 | 관측 0 · 관측 0 · 48 | 44 · 16 · 4 | 4 | 8624 / +5104 |
| P2 | 64 / 64 | 관측 0 · 관측 0 · 관측 0 | 64 · 관측 0 · 관측 0 | 7 | 38088 / +29464 |

**확인.** P1은 I에서만 16사실을 풀었다. 그중 12개는 같은 바이트, 4개는 변형 probe였다. P2는 A/K/R의 48사실을 더 풀었다. P1 동일성을 사용에 복사하면 C2의 A/K/R에서 12 거짓 양성, C4의 R에서 4 거짓 양성, C3의 A에서 4 거짓 음성이 나왔다. 주소·목적만 긍정하는 P0 지름길은 28 거짓 양성이었다. 조건부 확정판정의 오판율은 P0에서 분모 0이므로 **해당 없음**이다. 192사실에 검증된 정답이 있었고 미확인 정답은 **관측 0**이었다. 이 점수는 사전 규칙의 대조이며 사람의 판독 시험은 **미실시**다. [공개 구성](packets.csv) · [사실별 판정](decisions.csv)

## Q5. 같은 바이트와 경로 미사용

**확인.** C2 네 실행의 extra는 main과 전체 SHA256이 일치했다. extra 경로 열기는 **관측 0**, main의 같은 내용이 산식에 들어간 것은 4/4, extra의 지정 변경에 따른 보고값 변화는 **관측 0**이었다. C3에서는 probe가 실제 열렸고 내용 해시는 달랐으며 데이터 값을 조회하지 않았다. S4는 산식에 들었고 원합은 바뀌었다. T4의 AAMV2는 명시적으로 읽은 뒤 방향에서 버렸다. 파일이 열렸다는 한 문장으로는 네 상태를 구별할 수 없다. [P01](https://www.w3.org/TR/2013/REC-prov-dm-20130430/#term-Usage) · [X01–X04](evidence/contrasts.md)

## Q6. 같은 보고값과 다른 계보

| 통제 또는 공식 판 대조 | 원값 → 보고값, 기여 집합 | 확인 상태 |
| --- | --- | --- |
| S4의 선택값 469→470, 동일한 보고 구간 | 1300→1300 vs 1301→1300명. BX·BK 두 필드 유지 | 통제 두 짝에서 확인 |
| S-A-MISS, BX 값만 공란 | 1300→1300 vs 831→800명. 유효 2→1 | 통제 양성 확인 |
| NYC 3/24판→3/25판, 같은 3/19 진단일 | 469+831=1300→1300 vs 483+848=1331→1300명 | 두 공식판 확인 |
| NYC 3/20판→3/24판, 최근 공통 3/17 진단일 | 107+260=367→400 vs 485+897=1382→1400명. 3/20판의 3/19 값은 미확인 | 두 공식판과 결측 확인 |
| T-A-DIR, 01-06 방향만 0→1 | 원값/보고값 2→2 유지. AAMV1/3→AAMV2/4 | 통제 다른 계보 확인 |
| T-A-SAME와 T-A-DATE, 서비스일만 변경 | 01-07은 2와 같은 행. 01-08은 평일이라 WE가 비활성이고 관측 0 | 통제 음성·양성 확인 |
| T-A-EXCEPTION 및 비교 | 06-04 AB 방향 0은 FULLW 제거로 관측 0. 06-05는 AB1 1 | 발행된 예외 적용 확인 |
| T-A-EDITION 2016→2026 저장소판 | 서비스 구간·ZIP과 11개 멤버·AAMV1/3·보고값 2 동일 | 별도 개정 feed_version 미확인 |

자료의 기준일과 발행일, 더 작은 원값과 보고 단위를 함께 붙여야 같은 숫자를 올바르게 비교할 수 있다. Eurostat의 2024-12 유로지역 실업률 6.3%→6.2%는 별도 공식 보도표의 개정이다. 두 형식의 통계 원 API 파일은 실행 환경에서 미확인으로 유지했다. [S01a](https://raw.githubusercontent.com/nychealth/coronavirus-data/333f451e429d85afe62c909f6d2c6186040074d1/trends/data-by-day.csv) · [S01](https://raw.githubusercontent.com/nychealth/coronavirus-data/88fed814aae58e2b92fd4df5e9fa1ae3dc81f965/trends/data-by-day.csv) · [S01b](https://raw.githubusercontent.com/nychealth/coronavirus-data/482b5e40f0745d57352f013b0fa860a28588afe3/trends/data-by-day.csv) · [S04](https://ec.europa.eu/eurostat/web/products-euro-indicators/w/3-04032025-ap) · [S06](https://ec.europa.eu/eurostat/web/products-euro-indicators/w/3-30012025-bp) · [T01a](https://raw.githubusercontent.com/google/transit/832150450d06885fd28869ce17249c28b89ef58f/gtfs/spec/en/examples/sample-feed-1.zip) · [대조 원장](evidence/contrasts.md)

## Q7. 목적별 최소 기록과 비용

| 목적 | 조건부 제안 | 확인 범위와 남는 항목 |
| --- | --- | --- |
| 분석 재현자 | 같은 run·출력 ID, 발행판과 실제 경로 입력 해시, 변환·키·단위·결측 규칙을 보존한다. 미사용을 주장하려면 독립적으로 확인한 계측 범위가 필요하다. | P2로 48/48 A/K/R을 판정했다. T1-1의 사용 항목이 빠지면 보류하며, 완전하다고 잘못 표시하면 A/K/R에 거짓 음성 3건이 생긴다. [누락 감도](evidence/receipt-sensitivity.json) |
| 현재 자료 재사용자 | 주소와 목적에서 출발해, 현행 판·기준일·단위·정정 사유를 확인한다. 선택 셀을 계산해야 할 때 변환을 더 조회한다. | P1의 16 I는 당시 바이트 귀속 판단이다. 현행 판의 적합성은 발행자의 정정 정책이 필요하다. [S03](https://raw.githubusercontent.com/nychealth/coronavirus-data/a1dcaf47997accb4bc601f18d63b943815536f83/README.md) · [T14](https://github.com/mbta/gtfs-documentation/blob/master/reference/gtfs-archive.md) |
| 원자료 발행자 | 판 목록·배포와 멤버 식별·효력 범위·정오를 우선 제공한다. 소비자가 사용을 보고할 때 공동 입력·결과 식별자로 연결한다. | 보관된 판은 나중에 교체될 수 있다. 공개 배포 목록의 일치와 소비 실행의 열기·필드 기여를 각각 확인한다. [T02](https://cdn.mbta.com/archive/archived_feeds.txt) · [T05](https://www.bart.gov/schedules/developers/gtfs) |

**확인.** P0→P1은 구성당 319 B를 추가해 I 16개를 해결했다. P1→P2는 구성당 평균 1841.5 B를 추가해 A/K/R 48개를 해결했다. P2 합계는 38088 B, 구성별 1187~3606 B다. 측정값은 공개 canonical UTF-8 JSON이며 별도 strace·사전 기준·서명·보관본 및 판독 노동의 비용은 **미확인**이다. [바이트 원장](packets.csv) · [수용 원장](evidence/acceptance-evidence.json)

**다른 분야 직접 대조.** PyPI의 urllib3 2.5.0 wheel은 실제 129795 B를 해시해 publish 영수증의 SHA256과 맞췄다. predicate가 null이므로 확인되는 주장은 발행자와 파일이다. npm의 @sigstore/verify 2.1.1은 실제 15807 B tar의 SHA512와 두 발행·빌드 statement의 subject가 일치한다. 빌드 영수증에는 invocation과 Git 소스 한 건이 있고, 같은 커밋의 workflow는 npm ci를 명세한다. 어떤 로컬 패키지 파일이 산출물에 기여했는지는 두 자료로 확인되지 않았다. Debian의 Installed-Build-Depends는 정확 버전의 설치 환경과 후보 대안까지 담고, SLSA의 resolvedDependencies 완전성은 best effort다. 두 실제 영수증의 서명 신뢰 사슬 검증은 **미실시**다. [P05](https://pypi.org/integrity/urllib3/2.5.0/urllib3-2.5.0-py3-none-any.whl/provenance) · [P06](https://registry.npmjs.org/-/npm/v1/attestations/@sigstore/verify@2.1.1) · [P07](https://raw.githubusercontent.com/sigstore/sigstore-js/b5af5ac566fd569b3585fd5133acee2eb2083dba/.github/workflows/release.yml) · [P02](https://manpages.debian.org/bookworm/dpkg-dev/deb-buildinfo.5.en.html) · [P03](https://slsa.dev/spec/v1.2/build-provenance) · [원문 디코딩과 산출 해시](evidence/attestation-check.json)

**의존 작업 배경.** AF-RES-047은 기존 소비자 우선 6건에서 발행판 4, 특정판 사용 선언 1, 원 실행의 외부 입력 연결 0, 선택 필드 독립 검증 0이었다. 실행 기록 우선 2건의 외부 입력 연결은 1, 선택 필드 독립 검증은 0이었다. 이번 16개 새 통제 실행과 분모를 합치지 않았다. [047 당시 인계](https://github.com/laadkke-arch/agentflow-open/blob/a6ef2b0bcb6412d9e6fa7a9eb59b5e863c621ff0/docs/workstreams/research/AF-RES-047/HANDOFF.md)

직접 열람 기록은 42행이다. 독립 배당으로 인정한 고유 원문은 **26/22**이며 통계 발행 5/4, 통계 정의·검증 4/4, 교통 발행 4/4, 교통 정의·검증 5/4, 계보·빌드 8/6이다. 같은 저작의 판·표현·문서가 원자료를 인용한 관계는 소급 연결했다. 실패는 10행이고 배당에서 제외했다. [직접 열람과 실패 원장](sources.jsonl)

| 불일치 또는 약점 | 영향받는 결론 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀌는 조건 |
| --- | --- | --- | --- | --- |
| 계측 대상 또는 수집 범위의 표시가 잘못되면 P2에도 오판이 생긴다 | P2 64/64와 로컬 미사용 근거를 운영 분석에 적용하는 범위 | [T1-1 누락 감도](evidence/receipt-sensitivity.json) · [PROV Usage](https://www.w3.org/TR/prov-dm/#term-Usage) | 캐시·네이티브 로더가 있는 별도 산출에서 외부 추적과 영수증을 대조 | 수집 누락이 검출되면 해당 사용 판정을 보류한다. 독립 추적으로 닫힌 경로만 확인 범위에 둔다 |
| 국소 교란에서 보고값이 같을 수 있으며 T-C4의 단일 ID 교체는 stop_times를 갱신하지 않는다 | 읽기·입력 기여·보고 감도를 더 큰 변형과 전 피드 적합성에 적용하는 범위 | [S4/T4 짝](evidence/pairs.csv) · [X03/X04](evidence/contrasts.md) | 참조를 보존하는 보류 행의 비키 선택값 하나와 각 반올림 경계에서 독립 변형 | 같은 변환의 유효 입력에서 달라지는 결과가 관측되면 그 변형의 R을 바꾼다 |
| GTFS의 2016/2026 저장소판은 같은 예제 ZIP을 재포함한다 | 실제 운영 사업자의 독립 개정판에 대한 감도 | [T-A-EDITION](runs.jsonl) · [MBTA 발행 원목록](https://cdn.mbta.com/archive/archived_feeds.txt) | 같은 서비스일을 포함하며 게시 시각이 보존된 사업자 ZIP 두 개의 원본 확보 | 양쪽 원본과 동일 노선·서비스일·방향을 확인하면 운영 개정판을 별도 결과로 추가한다 |
