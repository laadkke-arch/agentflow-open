# 두 타 분야 대조와 구조 전이의 한계

## 공식 사건 기록과 원 관찰 연구

| 원기록 | 시간순 개입과 유지·변경 | 원 분모와 판정 단위 | 소프트웨어 조사에 적용할 규칙 | 남은 원입력 |
| --- | --- | --- | --- | --- |
| [CF-P1: T2074/13](https://www.epo.org/boards-of-appeal/decisions/pdf/t132074eu1.pdf) | D1/D2 쟁점 뒤 보조 청구에 wet heat/HF 조건을 추가해 2018-05-04 제출. 6월5일 심판은 늦은 범위 확대와 추가 검색 필요 때문에 이를 수용하지 않음 | 목적 선택한 심판 1건의 요청별 청구항1. 전체 특허의 분모는 없음 | 수정이 관측돼도 외부 해법의 제품 채택·실행과 동일시하지 않는다. 자료 적합성과 절차 시점을 함께 보존한다 | 최초 검색 통지, 응답, 각 제출 시점 청구 세트. register403 |
| [CF-P2: T2526/17](https://www.epo.org/boards-of-appeal/decisions/pdf/t172526eu1.pdf) | D1/D2에 맞서 전체 예비 픽셀 회로와 부분 소자의 차이를 주장. 2018-04-16 원 청구의 단일성을 인정. 별도로 수정된 허여 청구 세트도 존재 | 심판1건, 원32개 청구, 6개 추가 검색료. 환급을 발명 비용 절감으로 보지 않음 | 후보의 부분 유사성을 전체 대체 가능성으로 승격하지 않는다. 최종 결론이 반대 진술을 지우지 않는다 | 원 검색 서신과 최종 허여 청구의 정확한 문자 차이, 실제 납부액 |
| [CF-E1: Chan·Schunn 2014](https://joelchan.github.io/files/2014-cogsci-analogy.pdf), §2–3 | 시간순 유추 뒤 새 개념 생성은 늘지만, 바로 앞 개념과의 기능 거리는 오히려 작아 큰 도약 가설을 반박 | 전문팀1개, 회의2개, 발화4594행. 5/10행 창과 개념이 단위. Study2 모형 N=938 | 소개, 새 아이디어, 최종 선택, 제작을 따로 센다 | 원 녹음·코딩표와 최종 채택·제작 기록 |
| [CF-E2: Cheong·Hallihan·Shu 2014](https://www.cambridge.org/core/journals/ai-edam/article/design-problem-solving-with-biological-analogies-a-verbal-protocol-study/F69BBEE77460DA27C40972AD03C10C21), §3–5 | 같은 제시문에도 전략 대응과 표면 연상이 갈림. 해체 과제3팀 중1팀만 기대한 유추 기반 해법을 생성 | 녹음 학생30명, 9팀, 3과제, 10초 구간. 비녹음4명은 질적 관찰로 분리 | 형상 결합→부품 결합, 환경 변화→해체 조건이라는 두 대응을 이름 언급과 구별한다 | 부품 시험, 다른 해법과의 비교, 최종 채택 기록 |

네 원문은 A/B 사례 수에 더하지 않는다. EPO Register의 홈과 두 실제 application 경로는403이었으므로, 같은 유형의 공식 EPO 심판 PDF 원문 두 건으로 대체했다. 판결에 실린 전후 주장과 청구 조건은 읽었지만 원 검색 통지→응답 원본을 전부 연결하는 요건은 충족하지 못했다.

CF-E1의 세 분석은 같은 녹음의 재분석이다. 97개 유추 블록과843개 일반 블록의 구성, 모형 N=938, 본문의144/147 유추 표기는 각각 다른 원 위치대로 보존하며 임의로 합산·교정하지 않는다. CF-E2의22.1%는 성공한 팀의 비율이 아니라 Team2의 활동 중10초 구간 가운데 전략 비교 구간의 비율이다. 유사성 코딩의 합의 방식과 활동 모드 코딩의 일치도도 별개다. 어느 연구도 소프트웨어 팀에 이른 링크를 제공했을 때의 노동 절감을 측정하지 않았다.

## X-S1 · 이름과 실제 작동 관계를 구별한 추가 대조

Shopify의2020 Semian 운영 설명을 과거 코드와 연결했다. 2015 회고가 말하는2014 도입은 표집 창 밖이어서 새 A/B로 넣지 않았다. 2020 글 이전 고정 코드 `66994784f2740e54d1ddbe6f2ff9d8616bc7c747`에는 이름 외에 실제 제어 관계가 있다.

| 원 분야 관계 | 받아온 코드·운영 대응 | 적용 조건과 차이 |
| --- | --- | --- |
| 지속 과전류 또는 단락이 trip을 유발한다. [Eaton2018, PDFp3](https://www.eaton.com/content/dam/eaton/markets/machinebuilding/protect-personnel-assets-and-machine-reliability/documents/documents-english-language/eaton-safety-above-standard-whitepaper-wp012011-en.pdf) | 오류 시각을 window에 넣고 error_threshold에 닿으면 open한다. [코드L53–59,112–128](https://github.com/Shopify/semian/blob/66994784f2740e54d1ddbe6f2ff9d8616bc7c747/lib/semian/circuit_breaker.rb) | 전류의 물리 기작과 서비스 오류의 지속성 가정은 다르다 |
| 접점을 열어 유해한 전류 흐름을 끊는다. Eatonpp2–3 | open이면 driver 호출 전에 예외로 중단한다. 같은 코드L25–29,45–50 | 적합한 자원 식별자와 fallback이 필요하다 |

이 대응은 코드에 존재하지만 Shopify가 Eaton 자료를 직접 읽었다는 계보는 없다. 당사자가 말한 전달 경로는 Hystrix와 Release It라는 다른 소프트웨어 생태계다. 이를 타 분야 해법의 직접 발견 양성으로 승격하지 않는다.

2020 운영자는 Hystrix를 알고 조정 인자의 차이를 설명한다. 이 차이는 자체 유지의 근거가 될 수 있지만 실제 교체 검토·거절 결정 날짜는 미확인이다. circuit state는 worker별이고 bulkhead 접근 상한은 server-wide라는 조건도 다르다. 코드·README·회고는 같은 생산자의 한 제품 계보다.

263%→4%는42개 실패 의존성 등 입력을 둔 모형의 추가 사용률이다. Redis p99<50ms는 저자가 보고한 운영 입력이고, 절약한 인시·서비스 비용은 아니다. 저자는 success_threshold의 효과가 계산식에 잘못 들어갔다고 수정했다. 수치가 크다는 사실만으로 조기 소개의 인과적 절감을 주장할 수 없다.

## 반증 경로와 미발견 범위

공식 심판과 원 연구에서 ‘선행자료 제시→기존 주장 포기’, ‘먼 유추→큰 설계 도약’, ‘좋은 유추 제공→구조 전이 완료’의 반례를 각각 CF-P2·CF-E1·CF-E2로 확인했다. 심판·녹음·학생 과제의 분모를 합치지 않았다.

늦은 원리 명명은 `"later learned" "circuit breaker" software`, `"reinvented" "circuit breaker" pattern`, `"did not know" "bulkhead" software`를 검색했다. 원저장소와 회고 계열을 찾았지만 교육용 재구현·2024년 이후의 글·동음이의 자료가 주로 나왔고, 2018–2024 선택에서 초기 구현→나중 명명 진술을 잇는 새 엄격 사례는 확보하지 못했다. 기존017의 Kanban과7기원을 재산입하지 않는다. 다음 최소 입력은 다른 이름으로 작성된 초기 커밋과 뒤늦은 명명 발언의 날짜 쌍이다.

모든 직접 원문·실패·선정 밖 검색은 sources.json과 search-log.json에 URL, 위치, 판, 확인 시각, 한계를 남겼다.
