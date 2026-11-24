# SELF_CHECK — AF-RES-211

상태: **PARTIAL** (고정 source/문서 및 설계 판별 확보, Q3 raw HTTP·HTML id 핵심 결손). 자기 검토만 수행; 독립 검토자 없음. 작성 전부터 과제에 이름 변경 경계, entry URL, 선행 PARTIAL이 노출된 목적 표집. blind 검토/무작위 표본 아님.

| 기준 | 실제/목표 | 판정 |
|---|---|---|
| fixed document/source | 8/8 | D01–D08, 4판 각 doc+source; P RST source 대체, 2 rendered numeric 실패 별도 |
| publisher | 4/4 | R01–R04; 추가 removal note 별도 |
| consumer | 5/4 | C01–C05 두 생태계 2개 이상, href 8; C06 역반례 supplemental |
| hosting/config | 9/3 | H01–H05 + Y03–Y06; raw actual logs |
| standard | 3/3 | W01–W03; Y07 동일 2025 판 중복 제외 |
| supplemental | 9 | 별도 실제 원문·코드; 동일 릴리스 wording/제목-only 제외 |
| 총 고유 자료 | 38/22 | 59 ledger rows = 38 count + 21 제외/미산입, 유형 모두 충족 |
| 사건 | 2 API changes + 1 standard revision | 자료 수와 다름; 5 소비자 issue는 보고 단위 |
| 비교 자리 | 18/18 기록, 15/18 본문/소스, 3/18 실패 | 9 rendered 본문, 6 SHA line range; 목적 반복은 독립 URL 아님 |
| raw HTTP & HTML id | 0/12 rendered slots; SHA 6/6 line range | F07 DNS, 웹 도구 text only. browser fragment 미실측 |
| 역사 슬롯 | 0/6 실제 당시 destination | consumer href 8개 모두 당시 snapshot 미확인 |
| runtime/benchmarks | 0 | source+기존 보고; Codex 재검증 항목에 남김 |

| 질문 | 판정 근거 | 반례/다음 자료 |
|---|---|---|
| Q1 | H01–H05 Y03–Y06 규칙/설정/실제 build 구분 | custom stable·inactive, numeric build 증거 추가; Y03–06는 F03–06 shell 후속 |
| Q2 | D01–D08 R01–R04 X03/X04; code SHA 직접 read | C06 역방향 에러; total/BICUBIC 불변, runtime 별도 |
| Q3 | destinations 18개, X01/X02 D01/D03 F01/F02 | F07 DNS, raw HTTP/id + historical archive 필요; root 실패 F11/F12 |
| Q4 | C01–C05 Y01/Y02 citations 8 | 원문의 당시판 알 수 없음; C03 old anchor 검사 |
| Q5 | 표3/COUNTEREXAMPLES old 지원/현행 미지원/이력의 의미 | U R02/X05, P X03/X06 history 양성; controls; raw link 생존 별도 |
| Q6 | W01–W03 Y07 | dated vs latest 실제 수정; runtime 대조 불가 |
| Q7 | A–D + 목적별 반환; C06 역반례 | 버전/최소판 확인이 답을 바꾸는 때만 질문 |

검토: 1.26.18 발표가 2.0.0보다 뒤라는 순서를 확인. X06 2.7.0 alias 유지 기록을 현행 지원으로 오해하지 않음. P old numeric build 부재 및 HTTP 404는 확정하지 않음. stable/latest actual build logs 후속 확인(원행 보존). 5단계 RESULT에서 표 1–3 먼저, Q1–7, 대안 및 약점 3건. 결과 SHA에서 readback·CSV 폭·JSONL ID·owned path 대조 후 마지막 HANDOFF만 작성할 계획. 실제 실행과 독립 검토를 했다고 표시하지 않음.
