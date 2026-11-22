# PostgreSQL 실제 확인 왕복 비용 감사

입력 커밋: `47e62e4de3f1acb38db234dead5eedd3927ba1bd`. 기존 T0/T1 파일은 보존하고 새 감사 파일에서만 비용 정의를 통일했다.

**전역 정의로 확인된 완료 왕복은 0회다. 일반적인 응답자→작성자 직접 회신은9쌍이며 모두 심사했다.** 이 두 수가 다른 이유는9쌍의 직접 선행 응답이 설명·예시·권고였고, 작성자의 후속 발화가 요청받은 추가 사실의 답이 아니었기 때문이다.

## 정의 대응

| 지표 | 뜻 | 결과 |
| --- | --- | ---: |
| 기존 P actual_clarification_roundtrips | 봉인 변수 자체의 요청→명시 답 | 0 |
| 기존 P general respondent→author pairs | 질문 유무와 무관한 직접 회신 | 9 |
| 전역 normalized 확인 왕복 | 어느 추가 사실·목적이든 실제 요청→그 요청을 채운 저자 답 | 0 |

숫자가 우연히 같아졌지만 기존 source 지표와 normalized 지표의 뜻이 같았다고 소급하지 않는다.

## 직접 회신9쌍 전수

| 쌍·사례 | 공개 메시지 | 응답자 UTC → 저자 UTC | 달력 시간 | 선행 추가 질문 / 요청 충족 / 산입 | 제외 근거 |
| --- | --- | --- | ---: | --- | --- |
| P-COST-01 · P01 | [응답](https://www.postgresql.org/message-id/CA%2BbJJbwsUtM-fpcPAVcNuPoyGkqwhoSnFTBY8gSBJ5zOKpBdug%40mail.gmail.com) p2–5 → [저자](https://www.postgresql.org/message-id/TYXOG__NifhiS2fEiqgnNDH9w-sqvHeSXz2osjUdnfS-9lN3IAsJ8uv4Z_c9fOHBxLDroEZ1YkUl9sGZacdCqMC4SXdY0Wqonu3aqCbeAnk%3D%40protonmail.com) p2–4 | 2022-01-02T15:54:49Z → 2022-01-02T19:41:56Z | 3.785278 | 없음 / 해당 없음 / 0 | 목적을 묻는 별도 메시지는 2022-01-03 08:04:22로 이 저자 발화보다 뒤이며, 그 뒤 저자 답은 없음. |
| P-COST-02 · P03 | [응답](https://www.postgresql.org/message-id/20220106.183908.758244498024205160.horikyota.ntt%40gmail.com) p2–4 → [저자](https://www.postgresql.org/message-id/DB9PR07MB718015C40BC021957A7165F5CB4C9%40DB9PR07MB7180.eurprd07.prod.outlook.com) p3–5 | 2022-01-06T09:39:08Z → 2022-01-06T10:20:49Z | 0.694722 | 없음 / 해당 없음 / 0 | 앞선 다른 응답의 use_remote_estimate/fetch_size 질문에 해당 값으로 답하지도 않음. 실제 ID 물리 원천은 미확인. |
| P-COST-03 · P03 | [응답](https://www.postgresql.org/message-id/CAM%2B6J975qVC5AiQW29J8uE-z%2Ba2atQW9GHwi3NM5XmJCB1a%2B2w%40mail.gmail.com) p3–5 → [저자](https://www.postgresql.org/message-id/DB9PR07MB7180C7235B334F3D8D6EED1FCB4C9%40DB9PR07MB7180.eurprd07.prod.outlook.com) p2–4 | 2022-01-06T12:52:56Z → 2022-01-06T14:31:46Z | 1.647222 | 없음 / 해당 없음 / 0 | 소스 읽기에 열려 있다면 읽어보라는 권고를 사실 확인 질문으로 세지 않음. DELETE 계획은 제안된 비용 설정의 실행 결과라고 밝히지 않음. |
| P-COST-04 · P07 | [응답](https://www.postgresql.org/message-id/20220105111258.GA18163%40depesz.com) p2–3 → [저자](https://www.postgresql.org/message-id/CA%2Bi5JwY_%3DzsFewDrTWQ7fw5E6EBjnYVHBfTEUVfZV-pD%2BAXoUQ%40mail.gmail.com) p1–2 | 2022-01-05T11:12:59Z → 2022-01-05T11:22:34Z | 0.159722 | 없음 / 해당 없음 / 0 | Ray의 별도 의도 확인은 4분17초 앞선 다른 회신 가지. 저자는 depesz 예를 인용하며 새 질문을 했고 Ray 질문에 명시적으로 답하지 않음. |
| P-COST-05 · P08 | [응답](https://www.postgresql.org/message-id/41274.1641394465%40sss.pgh.pa.us) p2–3 → [저자](https://www.postgresql.org/message-id/CA%2Bi5JwZRMwu_Mo8wfrS-_VWANG%2BRpaGEXth_orym-s_2joKKYA%40mail.gmail.com) p1–2 | 2022-01-05T14:54:25Z → 2022-01-05T16:11:28Z | 1.284167 | 없음 / 해당 없음 / 0 | 더 적은 복잡성을 원한다면 hstore라는 조건부 제안은 그 선호값을 회신하라는 질문과 구별. |
| P-COST-06 · P08 | [응답](https://www.postgresql.org/message-id/299857.1641399856%40sss.pgh.pa.us) p2 → [저자](https://www.postgresql.org/message-id/CA%2Bi5JwZEVzxPyMo7VEZkn%2Bw8Kh6J5RkrF%2BvRd65Mf0_G1CNLzw%40mail.gmail.com) p1–3 | 2022-01-05T16:24:16Z → 2022-01-05T20:26:21Z | 4.034722 | 없음 / 해당 없음 / 0 | 저장소 사용법 질문과 후보 탐색이지 요청받은 환경·목적의 값이 아님. |
| P-COST-07 · P08 | [응답](https://lists.osgeo.org/pipermail/postgis-users/2022-January/045168.html) p1–17 → [저자](https://lists.osgeo.org/pipermail/postgis-users/2022-January/045171.html) p3–7 | 2022-01-07T21:19:10Z → 2022-01-08T02:24:41Z | 5.091944 | 없음 / 해당 없음 / 0 | 실제 질문자 목적 확대를 응답자의 질문이 먼저 유도했다고 바꿔 쓰지 않음. |
| P-COST-08 · P08 | [응답](https://lists.osgeo.org/pipermail/postgis-users/2022-January/045173.html) p1–4 → [저자](https://lists.osgeo.org/pipermail/postgis-users/2022-January/045174.html) p2–4 | 2022-01-08T04:20:23Z → 2022-01-08T14:15:59Z | 9.926667 | 없음 / 해당 없음 / 0 | 인용된 앞선045172의 포괄적 불명확성 표현은 별도 사건으로 검토. 저자 회신은 이미 제시한 처리 관심을 재진술하며 특정 누락값을 제공하지 않음. |
| P-COST-09 · P08 | [응답](https://lists.osgeo.org/pipermail/postgis-users/2022-January/045173.html) p1–4 → [저자](https://lists.osgeo.org/pipermail/postgis-users/2022-January/045192.html) p2–3 | 2022-01-08T04:20:23Z → 2022-01-11T16:04:10Z | 83.729722 | 없음 / 해당 없음 / 0 | 같은045173을 두 번 회신한 것을 두 개의 새로운 질문/답 왕복으로 계산할 수 없음. |

달력 시간은 설명 뒤 회신까지의 간격이다. 완료된 확인 왕복의 지연값은 분모0으로 **해당 없음**이며0시간이라고 쓰지 않는다. 같은 요청을 인용한 두 후속과 겹치는 대화 간격을 합쳐 총 질문 비용으로 만들지 않는다.

## 다른 회신 가지와 인용된 질문

| 맥락 | 실제 요청·관측 | 작성자 답 판정 |
| --- | --- | --- |
| P-CTX-01 · P01 | [원문](https://www.postgresql.org/message-id/CA%2BbJJby3c3ri_x_fW1-zbByQemtNvdAC1neVGDJaxg_DcDMH3A%40mail.gmail.com) p2,p5; 목표 설명 요청 | 요청 뒤 작성자 답이 없다. P01 data-entry 발화는 이 요청 이전이다. |
| P-CTX-02 · P02 | [원문](https://www.postgresql.org/message-id/3561426.1641226689%40sss.pgh.pa.us) p2; 실제 SELECT가 오류 없이 끝나는가 | 작성자 후속 자체가 없다. |
| P-CTX-03 · P03 | [원문](https://www.postgresql.org/message-id/CAM%2B6J96xK1Wu18%3DMSLkekA_QKhCxpEtk8yPw2uknVd9%2Bkz0WZQ%40mail.gmail.com) p3; use_remote_estimate/fetch_size 설정값 | 뒤의 작성자는 local/remote 실행과 다른 DELETE 쿼리를 말하지만 이 설정값은 제공하지 않는다. |
| P-CTX-04 · P06 | [원문](https://www.postgresql.org/message-id/6515271a-9bda-3f15-0cda-f120089d66a7%40enterprisedb.com) p2–5; SQL·기대값·실제값·PG판 | 원 스레드 저자 답 없음; OSGeo 원장 보강에서도 동일 저자 값을 확보하지 못함. |
| P-CTX-05 · P07 | [원문](https://www.postgresql.org/message-id/3716cb3b-21e9-a204-1b2c-37a4f023c72f%40rodonnell.ie) p4; 제시한 SQL 함수 예가 의도한 것인가 | 별도 회신 가지에서 저자가 DO/Oracle 호환 질문을 한다. 이를 포괄적 의도 재진술로 볼 여지는 있지만 명시적 답/정정 관계를 확인하지 못한다. |
| P-CTX-06 · P07 | [원문](https://www.postgresql.org/message-id/20220105113426.GA14488%40depesz.com) p2; 구체 Oracle SQL과 실행 오류 제시 | 이 요청 뒤에는 Merlin의 제3자 답만 있고 저자 코드/오류 회신이 없다. |
| P-CTX-07 · P08 | [원문](https://www.postgresql.org/message-id/eca47936-bd32-58ae-94d0-fd44700038b1%40aklaver.com) p2; 왜 오래된 kv-pair 저장소를 쓰려는가 | pgsql-general 저자 후속 없음. OSGeo의 jsonb/hstore 질문을 kv-pair 사용 이유 답으로 연결할 근거 없음. |
| P-CTX-08 · P08 | [원문](https://lists.osgeo.org/pipermail/postgis-users/2022-January/045172.html) p2; 무엇을 묻는지 불명확하다는 포괄적 표현 | 실제 문장에는 물음표가 있지만 특정 누락 사실을 지정하지 않고 이어서 기능 예를 설명한다. 저자는 이후 가능성에 동의하고 대안을 질문한다. 요청값을 새로 채운 완료로는 확인되지 않는다. |
| P-CTX-09 · P05 | [원문](https://www.postgresql.org/message-id/0b7219fe-2bfe-f01d-ce1b-025bfb07e24f%40matrix.gatewaynet.com) p3–6; 사용판을 찾아 해당 문서를 읽으라는 절차 권고 | 작성자 회신이 없으며 버전을 답장해 달라는 요청인지도 명시되지 않는다. |

P01의 data entry 목적은 응답자의 목적 확인 요청보다 먼저 나왔다. 이를 실제 목적 질문의 답으로 코딩하면 시간 순서를 뒤집는다. P03의 설정 질문에는 설정값이 돌아오지 않았으며, local 실행경계에 대한 자발적 발화도 그 설정 질문의 답이 아니다.

P07의 다른 가지에 있는 포괄적 의도 확인과 P08의 앞선 불명확성 표현은 모두 남겼다. 의도 재진술이나 새 질문까지 답으로 넓혀 읽는 경우의 불확실성이 있지만, 이 두 사건에서 요청값을 명시적으로 채운 완료를 확인하지 못했다. 주 합계에는 넣지 않으며, 독립적인 구체 사실 확인 쌍을 확보한 것처럼 표현하지 않는다.

## 재현과 한계

`clarification-cost-audit.json`의9개 pair에는 두 URL·Message-ID·UTC·본문 위치·간격·요청 유무·답 충족·same_frozen_variable·산입 여부가 모두 있다. 본문 전문은 저장하지 않았다. `input_file_sha256`는 기존11개 파일이 보존됐음을 확인하며, 재열람 파일은 요청 문장의 위치와 해시·UTC만 보관한다.

전체 대화의 원문 최소수는 늘어나지 않는다. 9개 회신쌍은 독립 사용자나 독립 채택 사건도 아니다. 발신자의 실제 읽기 시각·기다린 이유·클릭·공급자 투입시간은 관측하지 못했다. 이번13개 관련 메시지 재열람의 본문 hash는 입력 영수증과 모두 일치했다. 이는 현재 관측 내용의 일치이며2022년 제출시각의 암호학적 보증은 아니다. 원래 영수증이나 T0/T1 내용을 덮어쓰지 않았다.
