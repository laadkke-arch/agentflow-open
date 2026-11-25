# 반례와 판정 정정

사전 합격표의 판은 `ffe11059acf34169890e49fcea5df835f2a2bf7f`다. 이 파일은 그 판과 실제 실행의 차이를 기록한다. 대조 조작은 지명 원본의 실적 밖에서만 센다. [사전 합격표](https://github.com/laadkke-arch/agentflow-open/blob/ffe11059acf34169890e49fcea5df835f2a2bf7f/docs/workstreams/research/AF-RES-265/SCOPE.md)

| 앞선 판정/의심 | 반증 관측 | 정정 및 한계 |
| --- | --- | --- |
| 선행 247의 BoxTextured 끝 2 B를 BIN chunk 바깥 정렬 바이트로 해석할 수 있다 | BIN length와 `/buffers/0/byteLength`는 둘 다 4592 B, 최종 view 끝 4590 B, 끝 두 바이트 `0000`. Lamp도 7829084 B 안에 view 바깥 끝 3 B가 있다 | 선언 buffer 안의 미참조 정렬용 꼬리와 GLB BIN chunk의 추가 padding을 분리. 이번 세 파일의 추가 BIN pad 0 B |
| 의도한 재질의 파일이 유실되면 모델 전체 로더가 실패할 수 있다 | BoxTextured PNG만 미제공하면 PNG 404·decode 오류와 함께 onLoad·draw·동일 geometry. 표준판 대비 59,388 px에서 RGB 채널 차이 ≥3. 참조 제거 모델과 프레임 SHA가 같음 | 화면 성공과 표면 재현 성공을 분리. HTTP 404·texture decode 결손이 콜백 성공으로 가려질 수 있다 |
| 선언된 이미지가 유효하면 소비 과정이 가져올 수 있다 | 같은 BoxTextured 합성판에서 이미지 제공/미제공 모두 Three 요청 0, 선택 0, draw 1, 픽셀 일치. Validator는 이 구성에서 PNG를 포함해 두 파일을 읽음 | 참조 도달과 도구의 eager read를 따로 적는다. 해당 로더에서만 요청 0 |
| required 확장 자원의 미충족은 늘 onError로 드러날 수 있다 | Lamp KTX2 decoder 미등록은 onError. 등록 후 WASM 404이면 KTX2 4개 200이어도 decode 0, onLoad·draw 성공, 19,612 px 변화(≥3) | 등록 여부·decoder 전달·선택된 source 해석·픽셀을 별도 조건으로 검사 |
| 같은 JSON의 core source가 있으면 오류 시 항상 PNG로 이어질 수 있다 | 합성 Lamp JSON에서 미등록이면 PNG 4 선택, 등록이면 KTX2 4 선택. 등록하고 KTX2들만 미제공하면 4×404·onLoad·draw, PNG 재시도 0 | capability fallback과 선택 이후의 I/O 실패 정책을 구별. 다른 로더에서는 재시험이 필요 |
| GLB만 제공하면 최소한 형상이 나온다 | 합법 합성 Box GLB `/buffers/1/uri`의 `external.bin`을 주면 원본과 같은 draw·픽셀, 없으면 404·onError·프레임 미생성 | 컨테이너 식별 이후 소비하는 bufferView가 도달하는 파일을 확인 |
| 단일 EPUB archive의 manifest로 선택된 코덱을 알 수 있다 | 같은 본문의 MP4·WebM 모두 들어 있고 p30/p40은 자막 형식이 다름. EPUBCheck의 별도 두 후보는 모두 원격 주소 | 둘 다 선언되고 들어 있어도 실제 선택과 작동은 reader 별도 계측 |

위치와 원문 값은 해당 두 회차의 [runs.csv](runs.csv), [프레임 대조](frame-diffs.csv), [검증기](receipts/validator.json), [출판물 추출](receipts/epub-read.json), 원장 A·N·L·C·E·X 행을 따른다.

## 계측에서 재실행한 이유

- Playwright 환경에서 초기 smoke의 결손 probe는 응답 헤더만 읽고 종료하여 404 본문 완료 이벤트가 남지 않았다. probe의 본문 읽기를 추가하자 이 probe는 통과했다. 이어 실제 Three FileLoader도 일부 404를 헤더로 거절해 두 진단 회차의 프로세스가 1을 반환했다. 빈 404 본문만으로는 같은 증상이 남았다.
- 최종 harness에서 비성공 HTTP 헤더를 받은 사건은 `response(status)`로 기록하고, `requestfinished` 없는 사건은 `non2xxWithoutFinish`로 보존했다. 응답/실패 모두 없는 URL은 여전히 `outstandingRequests`에 남아 실행을 실패시킨다. 성공 응답은 완료 이벤트를 기다린다. 로더 코드·픽셀 합격 기준·자산은 같고, 최종 두 회차 프로세스는 각각 0이다.
- 디버그 행은 주검사/대조 공식 분모에서 제외했다. 절차의 앞뒤와 원문은 [계측 진단](receipts/instrumentation.json), 최종 [실행 명령](receipts/experiment-commands.json)에 있다. 브라우저 probe, 화면·파일 선택, 교정 및 재확인은 동일 작성자가 수행했다.
