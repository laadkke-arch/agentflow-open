# AF-RES-122 자체 점검

| 질문 | 답과 source_id | 실제로 찾은 반례 | 판정이 바뀌는 조건 | 미확인 |
| --- | --- | --- | --- | --- |
| Q1 | 고정 Python API 16/16. PT-RELEASE, PT-EXPORT, PT-TMETHOD, PT-TFUNC, PT-LOAD | view의 dtype와 shape 오버로드 및 transpose의 sparse 저장소 차이 | 다른 판에서 공개 export, overload, layout 조건이 바뀐다 | sparse·TorchScript 전체 실행 미실시 |
| Q2 | qna/5. 정규 0/8. 공개 opening 13편, 별도 진단 10건. F-CATEGORIES, F-ORDER, F-ACTIVITY-4/6/7, FORUM-5952 | 활동 페이지 중복·4페이지 결손. 5952의 창 순서를 확인할 수 없음 | 공개 UTC·ID 목록과 시작/종료 경계 일치, 앞 240건 opening 검증 | UTC 오프셋·하위 카테고리·편집 이력. 포럼 호스트는 현재 클라우드 허용 목록 밖 |
| Q3 | 활성 12, 반려 6. KO-QUICK, KO-DATA, KO-INTRO, KO-SAMPLER, KO-VIEW, KO-AXES | 배치는 데이터와 인덱스 양쪽에 쓰임. 번역의 .T와 메서드 transpose는 다른 호출. 복사본은 C06의 반대 역할에 해당 | 같은 심벌의 조작·입출력을 실제 접속 경로에서 확인한 이전 별칭 또는 경계 단어가 발견된다 | 2.3.1-latest 공개 전의 저자별 표기. 현재 번역 화면의 빌드 SHA |
| Q4 | 정적 판독 304쌍. PT-TEST-DATA, PT-TEST-VIEW, PT-TEST-AUTOGRAD, PT-LSTM, PT-EMBED, PT-DDP | O3665는 F에 따라 reshape 가능성이 다르고 O3611의 겹친 창은 단순 view로 만들 수 없다 | 작성자 판의 실제 입력과 의도가 알려져 일부 조작의 남은 조건이 풀린다 | 작성자 후속의 별도 판독과 독립 사람·모델 판독 미실시 |
| Q5 | 76조회, 1,216점수, 4파일 두 재생 일치. FORUM-4437, FORUM-5952, KO-TRANSPOSE | O4437 잔류 코드 토큰이 D01을 올린다. 가린 O5952의 T07과 T01/T02가 서로 다른 단계에서 빠진다 | 공식 opening 원문과 재채집 해시가 다르거나 접사를 처리하면 후보 집합이 바뀐다 | 공식 API 응답·초판과 발췌의 일치. 독자의 가림 의미 이해 |
| Q6 | C01 가림 ON에서 D07이 3위→4위. PT-SAMPLER, PT-FETCH, PT-TEST-VIEW, PT-TEST-AUTOGRAD, PRIOR-118-LEDGER | C03의 동일 shape와 다른 배열. C05의 gradient 유지와 저장소 공유 교차. 118의 138 광의 충돌 중 7 명시충돌 | 원절의 역할 문맥 또는 새 판독에서 직접·일부·충돌 경계가 달라진다 | 사용자의 Core ML·CUDA worker·2.2.2 동작 |
| Q7 | 별칭당 근거 2–3개, 활성 4,916바이트, 조회당 카드 16개. GEO-GUIDE/TOWN/BAY, AAT-GUIDE/ACT/WORK/OIL | Frobisher Bay의 도시 이명과 해역, painting의 과정과 산출, oil paintings의 하위 관계 | 독자 확인 시험에서 역할 표기·확인 부담에 따라 실제 오연결이 변한다 | 검색 시간·클릭·만족, 편집 노동시간과 제품 UI |

- 최종 원장은 중간 생성기의 동일 source_id 44개 중복 행을 합쳤다. 다른 접근 방법의 실패 기록은 보존했다. 108 후보 주소, 69 본문 주소, 55 고유 1차 계보, 29 접근 실패 주소다. 13개 opening 중 진단에 사용한 10개와 정규 모집 공석을 분리했다. [출처](sources.jsonl) · [모집](frame.csv) · [집계](evidence/metrics.json)
- 전수 정렬, 8/3 상한, 표시의 조사 포함, 판독과 근거 ID, 사본과 투영 해시를 확인했다. 두 경로의 파일 검산은 같은 작업자가 같은 프로그램에 입력을 좁혀 실행했다. 공식 PyTorch CPU 동작은 별도 프로세스에서 재구성한 소형 입력으로 관측했다. 외부 공개 문서 및 원문 의미의 판독 주체는 동일한 작업자다. [집계 코드](summarize.py) · [재생](evidence/replay-receipt.json) · [CPU 실행](evidence/torch-probe.stdout.json)
- 고정 2.5.1의 공식 문서·구현·시험 단언과 소형 입력의 실측을 분리했다. 번역판에는 2.3.1-latest와 2026년 개인 글도 있다. 이 판의 언어 조회 결과를 다른 PyTorch 판과 전체 한국어 작성자의 비율로 적용할 근거는 미확인이다. [기능판](catalog.csv) · [출전](aliases.csv)
