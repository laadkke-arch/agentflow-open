# AF-RES-136 — 보존 답 새 판독, 원문 연결의 범위

## 표 1 — 가명 답·사건 / 작성자의 요구·당시 확인 가능 범위 / 답의 제안·보존·유보 / 당시 본 근거 / 좁은 지지·핵심 해결·미확인

| 가명/사건·단계 | 요청 조건 및 범위 | 제안·보존·유보 | 당시 열람한 URL·코드포인트 구간 [시작,끝) | 좁은 지지 / 핵심 / 미확인 |
|---|---|---|---|---|
| B-bc2419820c / J1-a | 큰 JSON 스트림→id별 전체 객체; jq 1.6·메모리 한도/중복 정책 미정 | INDEX 전체 복원 스트림; 중복/누락 id·스트림 경계·RAM 유보 | 0면 | 근거 미제시; 1차 unknown; 실제 핵심 확정 없음 / 중복/누락 id·스트림 경계·RAM |
| B-83ae643cf0 / J3-a | cd 접두사 뒤 suffix, 실패 빈 문자열, 입력별 출력; jq 1.6; 일반 정규식 목표 미정 | startswith와 .[3:] 또는 빈 문자열; 정확한 버그 기제·일반화·동일 판 실행 유보 | 0면 | 근거 미제시; 1차 fulfilled-proposal; 실제 핵심 확정 없음 / 정확한 버그 기제·일반화·동일 판 실행 |
| B-5c1e6ce08b / P1-c | append로 기존 0과 새 42 행 분리; 실제 끝 바이트·dialect 미확인 | 동일 + dialect 규칙; EOF/인코딩/인용·dialect 유보 | [F V-dba3f82d7d7b](https://github.com/python/cpython/blob/deaf509e8fc6e0363bd6f26d52ad42f976ec42f2/Doc/library/csv.rst#L191) [7854,9354); [O V-de7a10707781](https://github.com/python/cpython/blob/deaf509e8fc6e0363bd6f26d52ad42f976ec42f2/Doc/library/csv.rst#L222) [9354,10854) | DictWriter 순서; unix LF/인용 규칙; 1차 conditional; 실제 핵심 확정 없음 / EOF/인코딩/인용·dialect |
| B-2b4a557eb7 / J3-c | cd 접두사 뒤 suffix, 실패 빈 문자열, 입력별 출력; jq 1.6; 일반 정규식 목표 미정 | 동일 + sub/gsub 일반 시험, sub 후보; 정확한 버그 기제·일반화·동일 판 실행 유보 | [F V-7b6ee5c62764](https://github.com/jqlang/jq/blob/2e01ff1fb69609540b2bdc4e62a60499f2b2fb8e/docs/content/3.manual/v1.6/manual.yml#L2370) [85988,87488); [O V-4037f00e4a40](https://github.com/jqlang/jq/blob/2e01ff1fb69609540b2bdc4e62a60499f2b2fb8e/tests/onig.test#L62) [1674,2571) | gsub 비중첩 전역 대체; 다른 패턴 시험; 1차 fulfilled-proposal; 실제 핵심 확정 없음 / 정확한 버그 기제·일반화·동일 판 실행 |
| B-cfc170960a / P3-b | 81 위치/54 키, 빈값과 순서 보존; 3.9.12·첨부 미확인 | 동일 + dict 매핑·길이 차이 근거; 실제 파일·3.9.12 유보 | [F V-fff85ac281d2](https://github.com/python/cpython/blob/b28265d7e6a41a4a0e227b37f4fbbc4d03a0a707/Doc/library/csv.rst#L149) [6317,7817) | dict 필드·길이 규칙; 1차 conditional; 실제 핵심 확정 없음 / 실제 파일·3.9.12 |
| B-fbc64753ec / J1-b | 큰 JSON 스트림→id별 전체 객체; jq 1.6·메모리 한도/중복 정책 미정 | 동일 + INDEX 정의; 중복/누락 id·스트림 경계·RAM 유보 | [F V-e80b5a033007](https://github.com/jqlang/jq/blob/2e01ff1fb69609540b2bdc4e62a60499f2b2fb8e/docs/content/3.manual/v1.6/manual.yml#L1964) [70763,72263) | INDEX signature; 1차 conditional; 실제 핵심 확정 없음 / 중복/누락 id·스트림 경계·RAM |
| B-18c4eeaa27 / P1-a | append로 기존 0과 새 42 행 분리; 실제 끝 바이트·dialect 미확인 | 유효 CSV, 끝 종결자 없을 때만 추가; EOF/인코딩/인용·dialect 유보 | 0면 | 근거 미제시; 1차 conditional; 실제 핵심 확정 없음 / EOF/인코딩/인용·dialect |
| B-ec223b092f / J2-b | 내부 YAML 문자열→객체, 외부 IO 아님; 순수 jq·도구 허용 미정 | fromjson은 JSON에만 해당; jq-native·허용 도구·YAML 의미 유보 | [F V-4cef9ffbe3d3](https://github.com/jqlang/jq/blob/2e01ff1fb69609540b2bdc4e62a60499f2b2fb8e/docs/content/3.manual/v1.6/manual.yml#L1770) [63133,64633) | fromjson JSON 규칙; 1차 unknown; 실제 핵심 확정 없음 / jq-native·허용 도구·YAML 의미 |
| B-f330dcba7b / P3-a | 81 위치/54 키, 빈값과 순서 보존; 3.9.12·첨부 미확인 | 중복 헤더 가설, 위치 기반 배열; 실제 파일·3.9.12 유보 | 0면 | 근거 미제시; 1차 conditional; 실제 핵심 확정 없음 / 실제 파일·3.9.12 |
| B-44c780fe9b / P2-c | SEP=; 인식, 실제 헤더·값 보존; 표준/옵트인/문법 미정 | 동일, 새 근거 없음; SEP 문법 및 정상 첫 행 보존 유보 | [F V-fff85ac281d2](https://github.com/python/cpython/blob/deaf509e8fc6e0363bd6f26d52ad42f976ec42f2/Doc/library/csv.rst#L149) [6317,7817) | 첫 행/kwargs; 1차 conditional; 실제 핵심 확정 없음 / SEP 문법 및 정상 첫 행 보존 |
| B-2abf7972e0 / P1-b | append로 기존 0과 새 42 행 분리; 실제 끝 바이트·dialect 미확인 | 동일 + DictWriter 매핑; EOF/인코딩/인용·dialect 유보 | [F V-dba3f82d7d7b](https://github.com/python/cpython/blob/deaf509e8fc6e0363bd6f26d52ad42f976ec42f2/Doc/library/csv.rst#L191) [7854,9354) | DictWriter 순서; 1차 conditional; 실제 핵심 확정 없음 / EOF/인코딩/인용·dialect |
| B-de585772a7 / P2-a | SEP=; 인식, 실제 헤더·값 보존; 표준/옵트인/문법 미정 | 옵트인 SEP 첫 줄 소비; SEP 문법 및 정상 첫 행 보존 유보 | 0면 | 근거 미제시; 1차 conditional; 실제 핵심 확정 없음 / SEP 문법 및 정상 첫 행 보존 |
| B-77ea3761f3 / J1-c | 큰 JSON 스트림→id별 전체 객체; jq 1.6·메모리 한도/중복 정책 미정 | 동일 + 댓글의 정확한 샘플; 중복/누락 id·스트림 경계·RAM 유보 | [F V-e80b5a033007](https://github.com/jqlang/jq/blob/2e01ff1fb69609540b2bdc4e62a60499f2b2fb8e/docs/content/3.manual/v1.6/manual.yml#L1964) [70763,72263); [N V-3f7b4c472b50](https://github.com/jqlang/jq/issues/2528#issuecomment-1405388586) [0,283) | INDEX signature; 같은 입력·출력 댓글 보고; 1차 conditional; 실제 핵심 확정 없음 / 중복/누락 id·스트림 경계·RAM |
| B-d3743a745a / P2-b | SEP=; 인식, 실제 헤더·값 보존; 표준/옵트인/문법 미정 | 동일 + 첫 행과 kwargs 근거; SEP 문법 및 정상 첫 행 보존 유보 | [F V-fff85ac281d2](https://github.com/python/cpython/blob/deaf509e8fc6e0363bd6f26d52ad42f976ec42f2/Doc/library/csv.rst#L149) [6317,7817) | 첫 행/kwargs; 1차 conditional; 실제 핵심 확정 없음 / SEP 문법 및 정상 첫 행 보존 |
| B-2f81da7700 / J3-b | cd 접두사 뒤 suffix, 실패 빈 문자열, 입력별 출력; jq 1.6; 일반 정규식 목표 미정 | 동일 + gsub 일반 정의; 정확한 버그 기제·일반화·동일 판 실행 유보 | [F V-7b6ee5c62764](https://github.com/jqlang/jq/blob/2e01ff1fb69609540b2bdc4e62a60499f2b2fb8e/docs/content/3.manual/v1.6/manual.yml#L2370) [85988,87488) | gsub 비중첩 전역 대체; 1차 fulfilled-proposal; 실제 핵심 확정 없음 / 정확한 버그 기제·일반화·동일 판 실행 |
| B-f32d379834 / J2-c | 내부 YAML 문자열→객체, 외부 IO 아님; 순수 jq·도구 허용 미정 | fq 조건부 후보 추가; jq-native·허용 도구·YAML 의미 유보 | [F V-4cef9ffbe3d3](https://github.com/jqlang/jq/blob/2e01ff1fb69609540b2bdc4e62a60499f2b2fb8e/docs/content/3.manual/v1.6/manual.yml#L1770) [63133,64633); [N V-30dabe45cc1d](https://github.com/jqlang/jq/issues/2530#issuecomment-1403891054) [0,278) | fromjson JSON 규칙; fq 샘플 댓글 보고; 1차 conditional; 실제 핵심 확정 없음 / jq-native·허용 도구·YAML 의미 |
| B-8007f6ef61 / J2-a | 내부 YAML 문자열→객체, 외부 IO 아님; 순수 jq·도구 허용 미정 | 내부 파서/허용 도구 가정; jq-native·허용 도구·YAML 의미 유보 | 0면 | 근거 미제시; 1차 unknown; 실제 핵심 확정 없음 / jq-native·허용 도구·YAML 의미 |
| B-fe91855504 / P3-c | 81 위치/54 키, 빈값과 순서 보존; 3.9.12·첨부 미확인 | 동일 + len(set(fieldnames)) 검사; 실제 파일·3.9.12 유보 | [F V-fff85ac281d2](https://github.com/python/cpython/blob/b28265d7e6a41a4a0e227b37f4fbbc4d03a0a707/Doc/library/csv.rst#L149) [6317,7817) | dict 필드·길이 규칙; 1차 conditional; 실제 핵심 확정 없음 / 실제 파일·3.9.12 |

## 표 2 — 사건·단계 전후 / 새 판독·종전 판독 / 실제 바뀐 결정 / 당시와 뒤늦은 조건 / 불일치·반례

| 사건·단계 | 새 판독 / 종전 자기판독 | 실제 바뀐 결정 | 당시 조건 / 뒤늦은 조건 | 불일치·반례 |
|---|---|---|---|---|
| P3 a→b / b→c | 근거만 / 근거만; 검사 구체화 / 검사 구체화 | 81 위치 보존 처방 유지, distinct header 수 검사 | 당시 81 vs 54, 3.9.12; 뒤늦게 3.13 재현 보고·작성자가 54 fieldnames로 질문 변경 | [3.13 보고](https://github.com/python/cpython/issues/112958#issuecomment-1850636441), [작성자](https://github.com/python/cpython/issues/112958#issuecomment-1851875594); 첨부 미확인 |
| P2 a→b / b→c | 근거만 / 근거만; 유지 / 유지 | 새 링크 없음, opt-in 유지, c에서 일부 예외 설명 축소 | 당시 SEP=; 예, 뒤늦게 대소문자 무관·skip/seek/strip 제안 | [작성자](https://github.com/python/cpython/issues/109644#issuecomment-1737485816); 공백 delimiter/비seek/정상 첫 행 반례 |
| J1 a→b / b→c | 근거만 / 근거만; 근거만 / 근거만 | INDEX 명령 같음; 새 판독 a unknown→b conditional이나 처방 변경 아님 | 큰 파일, jq 1.6; 뒤늦은 도구 수락 증거 없음 | [정확 샘플 댓글](https://github.com/jqlang/jq/issues/2528#issuecomment-1405388586), [reduce 구현](https://github.com/jqlang/jq/blob/2e01ff1fb69609540b2bdc4e62a60499f2b2fb8e/src/builtin.jq#L290-L310) |
| J2 a→b / b→c | 근거만 / 근거만; 조건부 후보 / 조건부 후보 | fq map(from_yaml) 추가, 순수 jq 해결은 아님 | 당시 내부 값 파싱, 뒤늦게 추가 도구 최소화 명시 | [fq 보고](https://github.com/jqlang/jq/issues/2530#issuecomment-1403891054), [작성자](https://github.com/jqlang/jq/issues/2530#issuecomment-1411829108) |
| P1 a→b / b→c | 근거만 / 근거만; 근거만 / 근거만 | EOF 조건부 repair 유지, dialect 근거 추가 | 당시 병합 예, 뒤늦게 첫 append만 실패 | [첫 append](https://github.com/python/cpython/issues/100821#issuecomment-1374503526), [EOF 가설](https://github.com/python/cpython/issues/100821#issuecomment-1374869968); RFC 마지막 개행 선택 |
| J3 a→b / b→c | 근거만 / 근거만; 근거만(대안: sub 조건부 추가) / 근거만 | 접두 처방 같음; 실제 실행은 미확인 | 당시 단일 접두사 예, 뒤늦게 한 줄 여러 cd와 g 실패 | [작성자](https://github.com/jqlang/jq/issues/2532#issuecomment-1409603192), [후속 보고](https://github.com/jqlang/jq/issues/2532#issuecomment-1599128800); 처음 sample용 proposal 충족과 실제 전체 해결 유보를 구분 |

## 표 3 — 조건별 분모와 편집자 결정

| 배정 조건 | 예정/적격/비교 가능 사건; 추가 제시/열람 | a→b 근거/검사/조건부/핵심/유보 | b→c 근거/검사/조건부/핵심/유보·악화/유지 | 선노출 제외 | 편집자가 줄 절·남은 비용 |
|---|---|---|---|---|---|
| F P3/P2 | 2/2/2; 0/0 | 2/0/0/0/0 | 0/1/0/0/0/1 | 원 독자 동일 F 후노출 P2 제외 1건; 현 판독 반복 사건 제외 0 | P3 실제 헤더/코드, P2 명시 규칙; 원 입력/정책 확인 |
| F+O P1/J3 | 2/2/2; 2/2 | 2/0/0/0/0 | 2/0/0/0/0/0 (J3 대안 분류 가능) | 원 독자 제외 2, 현 반복 제외 0 | EOF 실제 바이트; 동일 판 정확한 regex test |
| F+N J1/J2 | 2/2/2; 2/2 | 2/0/0/0/0 | 1/0/1/0/0/0 | 원 독자 제외 2, 현 반복 제외 0 | 동일 입력 보고에 판·RAM·도구 제약 표기 |
| 전체 | 6/6/6; 4/4 | 6/0/0/0/0 | 3/1/1/0/0/1 | 원 독자 P2 제외 5: 3/1/1/0/0/0; 현 반복 엄격 제외 0, 비율 산출 불가 | 추가 면이 보존·금지 조건을 직접 증명할 때 우선; 실제 시간/비용 미측정 |
| 뒤늦은 주요 조건 명시 사건 제외 | P3/P2/J2/J3 제외, P1/J1 2/2/2; 2/2 | 2/0/0/0/0 | 2/0/0/0/0/0 | P2를 단순 문법 명확화로 보면 P1/P2/J1 3건(유지 1); P1 후속 관측까지 제외하면 J1 1건 | 모집단 일반화 금지 |
| 현 판독 최초 노출만 | 6/6/0 단계쌍; 각 요청 첫 답 1개 | 산출 불가 | 산출 불가 | 12/18 반복 인지 행 제외, 남은 6답 | 독립 세션 교차 재판독 필요 |

위 수는 원 독자의 실제 열람과 새 판독의 주분류 기술통계. a→b 6쌍, b→c 6쌍, 답 18개, 사건 6개, 좁은 주장 비교 21개. 각각 별도 분모. 추가면 4/6 제시, 4/4 제시 중 열람, 추가 제시 없는 F 0/0 열람률 산출 불가. 원 독자 10면·전역 고유 9면·11,958 코드포인트(동일 본문 제거 10,458); 현재 16 answer-face pair(6×0, 6×1, 2×1+4×2)이고 16회 원래 읽기가 아니다. 주분류는 상호 배타적으로 유지/보강/검사/조건부/핵심/유보·악화. 유지된 유보를 새 유보로 세지 않는다. 좁은 사실의 지지와 전체 해결은 다른 축.

## Q1. 가림과 무변형 결합
- 통합 기준 67eb3c65404bf70de554bee6eb4c126344a3cd4a, 계획판 42260ca230e028e1303667be943b861a1d5953e4. 입력 132 결과 99be7bebb9561756fea04621120dd020cecf40b3, 인계 510e9db7742ea2edc09c17d0fd4e3e8fbf48ca49, 128 패킷 3c8a3cf52c84cd9a8c5a06421087733bb8319e6b. 중앙 행 RUNNING·의존 132 읽음, 수정하지 않음.
- [사전 규칙](SCOPE.md), [projection/protocol.js](projection/protocol.js), [preflight](projection/preflight.json) 고정. tool-side allowlist: 요청 request, 답 operation/preserve/exception/hold와 가명. 원문 row/field SHA-256, CP 길이, slot·answer_id join. 18/18, 6×3, 중복 없음; 합성 3단계·중복 phase·packet 실패 검사, SHA-256 known-answer. 가명·고정 시드 순열 해시 a75a12a88cf53e5e201acb66dad250a6f0faef30acbabaccd5dbff76b6511410. 첫 판독 전에 원 결과·점수·실제 URL을 출력하지 않음. 요청 안 자체 링크는 남기고 열지 않음.
- 1차 봉인 c748c9332501c6c89fa547a8db609f56c6456d5c, 2차 support ffc28399ab12b8f46de6d6641314814bda36999f 및 봉인 영수증 05a346424a3e1a2ed181a10075d9a58516eb7de4. 그 뒤 매핑/원 평가 전문 공개 187bf2b56d743d66146fd88967c1b467a5689b0e. 원 질문 후속 재열람 32abdc34f2b71abdc5d36be441f48445c048380b. 1차·2차 파일 SHA와 원문 길이 지문은 별도 장부에 저장.
- 한계: 현재는 AF-RES-132 독자와 다른 대화로 처리했으나 모델의 이전 학습/접근 여부 인증 불가능. 같은 세션 안의 새 판독을 여러 사람/모델로 포장하지 않는다. 답의 문구 자체로 F, 둘째 면 등 단계 추정 가능. 최초 요청 노출 6, 반복 인지 12/18. 가림은 데이터 필드 차단이지 의미 단서 제거가 아님.

## Q2. 요청 자체 조건
[requirements.csv](requirements.csv) 33행/6요청. 명시(E), 합리적 가정(A), 미확인(U)으로 나눈 정확한 위치·지문. P3 중복 이름 가설과 빈 열 보존; P2 SEP= 문법·호환 요구; J1 큰 파일/스트림 및 고유 id 정책; J2 내부 값 파싱·외부 IO 금지와 도구 허용; P1 원래 파일 보존과 끝 경계; J3 단일 sample vs 더 넓은 정규식 요구. 합리적 가정을 명시 조건으로 승격하지 않았다. 후속 댓글은 Q5에서만 열고 당시 요구에는 소급하지 않았다.

## Q3. 증거를 모르는 판독
[blind-ratings.jsonl](blind-ratings.jsonl) 18행, 모든 답의 operation/preserve/exception/hold claim_units 위치와 해시. core_resolution=fulfilled-proposal 3(J3), conditional 12, unknown 3. 이 값은 실행 성공이 아니라 제시된 처방의 문장상 충족 가능성이다. 전 답이 근거 미제시이고 그 상태를 과잉 확정과 구분했다. 모든 18개에 유보 기록. J1a와 b의 같은 명령이 서로 다르게 평가됨은 채점 문턱 불안정의 반례; 근거 개입 효과가 아니다. 좁은 지지, 핵심 해결, 조건부 선택지, 근거 넘은 확정, 정당한 유보 각각 분리. 명시된 최소 반증 입력과 위치는 판독 원장에 남겼다. 1차 봉인 뒤 수정 없음.

## Q4. 실제 본 면만의 증명
[support.csv](support.csv) 22행(무면 6+면-답 16), 좁은 근거 14 일반 매뉴얼/시험 pair, 2 댓글 보고 pair, 전체 핵심 조건 증명 0/18. 판정 가능한 근거 수 16/16 pair; 좁은 규칙/보고를 지지하는 것과 해당 입력·판 실행을 구분. P2 첫 행 매핑은 해당 규칙 하나에는 충분하지만 SEP 자동 처리에는 불충분. J1 N은 동일 샘플의 당사자 아닌 제3자 보고, RAM·1.6은 미확인. J2 N은 fq 조건부 후보, jq 자체 기능 아님. P1 O는 dialect 예시, append 경계 아닌 w; J3 O는 다른 정규식 시험, 원 질문의 앵커와 lookahead를 증명하지 않는다.
- [second-seal](evidence/second-seal.json) 본문 주석의 '8 distinct'는 오기: 구조화 집계 및 mapping에서 실제 고유 body hash 9. 원 face_count가 b/c 12답에서 없으므로 mismatch 12는 누락 필드이지 기록된 수와의 모순이 아니다. reading.jsonl의 각 답 seal_commit 이전 face_opened를 슬롯별 연결한 결과를 사용. 16 pair 전부 body hash/CP 길이 일치. face_count 기반 예비 join은 F/O 라벨 충돌 및 b에 뒤 면 과포함을 일으켰고, 일부 뒷면을 보기 전 되돌릴 수 없었음. 이 때문에 2차는 순수 가림 판독이 아니다. 선노출 보존, 모든 행을 오염 가능 층으로 보고, 2차 통계로 독립 재현 성공을 주장하지 않는다. 원 점수는 두 봉인 전까지 보지 않았다. 해시·길이 비교는 보존본 내부 검산이며 원 서버 원문 byte와의 별도 완전 비교는 하지 않았다. 해제 뒤 원 문서 범위 재열람은 사후 근거로만 취급한다.

## Q5. 원 작성자의 공개 시점과 요구
[evidence/postrelease-issues.jsonl](evidence/postrelease-issues.jsonl) 6 원 이슈 및 19 댓글. 원 게시/수정/닫힘 시각은 API 값, 댓글의 created/updated 값 미제공 및 edit history 전문 미확인. 댓글 순서·내용은 확인하되 최초 공개의 정확한 시각은 미확인. 원 투영에 없는 조건은 당시 독자가 알았다고 판정하지 않는다. P3 작성자가 중복 확인 후 질문 자체를 fieldnames 의미로 옮김; P2 대소문자 무관/seek workaround; J2 common/default tool 선호; P1 첫 append만 실패; J3 multi-cd 목표/실제 capture+sed 사용. J1 동일 명령 보고는 채택과 다름. J3 PR 2624 보고는 병합·동일 판 실행 확인 아님. P3/P2/J1/J2/P1의 제안이 실제 채택되었다는 원 작성자 기록 미확인; J3 후속 workaround 보고는 존재하나 새 독자 제안 채택이 아니다. 원 이슈 전체 히스토리 및 첨부 파일 미확인.

## Q6. 새 판독과 자기판독
[concordance.csv](concordance.csv): claim 21행(19 agree, 2 partial; 비교 가능한 문장상 교차표이고 동일 점수 아님), transition 12행(11 주분류 agree, J3 1 primary agree/alternative plausible), case 6행(핵심 조건 유보 6/6 일치). 2 partial은 P3.1 실제 중복 count와 J3.1 좁은 sample의 proposal 판정. P3 실제 파일 없이 중복 설명 확정 못함, J3 새 판독이 sample 해결 처방을 인정했지만 이전 평가는 일반 요구/실행 유보. 엄격한 동일 루브릭의 숫자 일치율은 산출 불가. 서로 다른 증거 단위와 척도를 억지 합산하지 않는다.
- 반대 사례: CPython dict(zip)와 원본 3.9.12 차이; RFC 4180 마지막 개행 선택과 Go reader NoEOLTest, Python fresh-file writer test는 다른 조작. Ruby/Rust explicit header 옵션은 SEP 자동 규칙 아님. jq reduce 누적 및 중복 키 대체; Perl lookahead는 jq 엔진 시험 아님. YAML spec anchor/alias/tag와 yq 단순 내부 파싱 예는 일반적 YAML 보존을 증명하지 않음. 각각 [sources](sources.jsonl) D/E 항목. 동일 판 실제 실행은 미실시.
- 원 요청자: 도구/판/보존값이 절대 조건이라면 후보와 해법을 구별해 달라. 원 독자: 이미 구체적인 제안이 있으면 좁은 원문 하나로 해당 규칙만 증명 가능. 새 판독자: 동일 처방의 근거 보강을 변화로 세지 말고 검사 구체화·조건부 후보·확정 변경 분리. 편집자: 링크 하나는 같은 입력/판/연산과 보존 조건이 정확히 일치하는 좁은 주장, 추가 원문은 예외·제약을 직접 해결하는 경우, 먼저 확인 질문은 도구 허용/판/실제 입력/정책이 갈라지는 경우. 링크 전달 권한은 사용자 지정 범위·공개 자료에 한정, 비공개 자료는 동의 없이 인용하지 않음.
- 대안 판정 J3 sub를 실제로 조건부 선택지로 분류하면 b→c 근거만 2, 조건부 2, 검사 1, 유지 1(분모 6); 실제 핵심 확정 0은 유지. P2 c 예외 설명 축소를 악화로 본다면 유지 0/악화 1; 실제 처방은 동일. 현재 반복 인지 12/18 제외하면 한 사건당 한 답만 남아 단계쌍 0; 선행 원 독자의 동일 F 반복 P2 제거와 별개. 후속 조건 제외 감도는 표3. 원 독자 6건의 조건 배정·사건 난이도·언어가 혼재해 링크 추가의 인과효과, 새 독자 채택률, 사람 시간 미측정. 독립 세션 간 결과를 비교했으나 완전 가림 성공으로 부풀리지 않는다.

## Q7. 새 분야 대조 — 시험 6건에 합산하지 않음
| 자료에서 만든 질문 | 직접 연 자료·판·쪽/마디 | 좁은 지지 / 보존 조건·반례 |
|---|---|---|
| Darwin 1859 초판 인쇄 p1의 첫 문장을 판과 쪽을 고정하여 인용 | [표제지 scan3](https://en.wikisource.org/wiki/Page:Origin_of_Species_1859_facsimile.djvu/3), [목차 scan5](https://en.wikisource.org/wiki/Page:Origin_of_Species_1859_facsimile.djvu/5), [본문 scan11](https://en.wikisource.org/wiki/Page:Origin_of_Species_1859_facsimile.djvu/11), [scan13 인쇄 p3](https://en.wikisource.org/wiki/Page:Origin_of_Species_1859_facsimile.djvu/13), 각각 연결된 이미지 실제 열람. 1859 John Murray; 목차 Intro p1, Ch I p7–43. [F373](https://darwin-online.org.uk/content/record?itemID=F373) ix+502pp | 본문 p1의 좁은 구절 “inhabitants of South America”는 scan11에서 직접 확인. 표제지 하나는 날짜만 충분. Freeman은 1859 날짜만으로 초판 식별 불가(1859 날짜 2판도 존재), [MARC250](https://www.loc.gov/marc/bibliographic/bd250.html) 판 정보는 실제 쪽 확인 아님. |
| 같은 문구를 1872 제6판의 같은 쪽에서 옮겨도 되는가 | [F391](https://darwin-online.org.uk/content/record?itemID=F391) eleventh thousand, xxi+458pp; [전사본](https://darwin-online.org.uk/content/contentblock?basepage=1&hitpage=210&itemID=F391&viewtype=text) piii title, pv Ch I p5–32, p1 Intro “organic beings inhabiting South America”. 원판 scan 링크 접근 실패 | 전사에서 문구와 장 쪽수 변화 확인. 동일 제목·Intro p1이라도 그대로 인용 불가. 비교판 실제 이미지 미열람이라 facsimile 기준 확정 유보. [Freeman 서지 설명](https://darwin-online.org.uk/EditorialIntroductions/Freeman_OntheOriginofSpecies.html) 판별 기준; 표제지/본문 이미지 재검증 필요. |
| Schumann Fantasiestücke Op.73, Larocque 2014, 첫 A clarinet 진입 마디와 기보/실음 보존 | [총보 380759](https://s9.imslp.org/files/imglnks/usimg/f/f7/IMSLP380759-PMLP57120-SCHUMANN-Fantasiest%C3%BCcke_Op.73%3Dclar-pno_-_Piano_Score.pdf), [A파트 380760](https://s9.imslp.org/files/imglnks/usimg/1/1f/IMSLP380760-PMLP57120-SCHUMANN-Fantasiest%C3%BCcke_Op.73%3Dclar-pno_-_Clarinet_in_A.pdf), [Bb파트 380761](https://s9.imslp.org/files/imglnks/usimg/0/04/IMSLP380761-PMLP57120-SCHUMANN-Fantasiest%C3%BCcke_Op.73%3Dclar-pno_-_Clarinet_in_Bb.pdf). 각각 PDF p1 이미지 직접 열람, 같은 Moli 221012·ISMN 979-0-56003-057-5. I Zart und mit Ausdruck, 4/4, m1 half rest+quarter rest 뒤 4박 quarter note. 총보 “Partition en sons réels” C5, A파트 3♭ 기보 Eb5, Bb파트 2# 기보 D5 | [VSL notation](https://www.vsl.co.at/academy/woodwinds/clarinet) A -3 semitones, Bb -2. 세 자료의 실음 C5, 기보음은 다르다. 제목과 편곡자가 같아도 A에 Bb 파트를 주면 기보 보존 실패. m1 진입 주장만이면 지정 파트 한 면으로 충분, 실음 보존에는 전조 기준·총보 필요. 전체 음정/리듬·원곡 대조 미실시. |
| 다른 편성도 동일 원판인가 | [IMSLP 목록](https://imslp.org/wiki/Fantasiest%C3%BCcke,_Op.73_(Schumann,_Robert)) #816553 violin+piano first ed Plate 124, flute/oboe #383929, viola #887728. [RCM D2427](https://archive.org/details/RCM-D2427?view=theater) bound scores/parts; 실제 해당 페이지 직접 접근 실패 | 다른 편성의 실제 원판 비교는 미확인. A/Bb 직접 대조는 악기/기보 차이의 반례지만 별도 편곡 원전 수로 중복 계상하지 않음. 원판/대체 편곡 실제 PDF 확보가 재개 조건. |

## 원전 수와 완료 상태
[sources.jsonl](sources.jsonl) 41행, 적격 독립 work_id 25개(원질문 6, 공식 정의/구현 8, 독립 시험·예제 6, 서지 3, 음악 2); CPython 두 구현 파일을 단일 구현 저작으로 합쳐도 24개. 같은 이슈 댓글, 동일 판·본문면·편곡의 총보/파트 중복 제거. 16행은 동일 계보 추가 면·설명만·접근 실패로 최소량 제외. 지정 음악 카테고리 3/2 부족 1 및 1872 실물 비교판 면, 원 이슈 편집 이력, 원문 서버 byte 비교 및 로컬 manifest/check 미확인. 소프트웨어 원 예제 실행은 지시상 반복하지 않음. 웹 원격 재열람·재집계만 수행. **PARTIAL**, 완료를 주장하지 않음. 판독자에게 사전 노출이 발생한 2차 층은 원장과 함께 보존한다. [SELF_CHECK](SELF_CHECK.md), [HANDOFF](HANDOFF.md)에 재개 사항.

| 중요한 불일치·약점 | 다음 조사·원문 또는 실험 | 판단을 바꿀 관측 |
|---|---|---|
| J3 sample 처방 충족 vs 실제 조건 유보; J1 동일 처방 판독 문턱 차이 | 기존 18답을 수정하지 않고 독립 세션에서 반복 제거, 동일 루브릭 및 정확한 예외를 교차 비교 | 단계와 무관하게 동일한 처방을 일관되게 판정하고 좁은 지지/핵심 해결 분리 |
| 2차 조인 예비 과포함·반복 인지, J2 뒤늦은 도구 제약 | face event cutoff만 허용하는 재판독; 원 작성자 도구 허용과 실제 동일판/입력 검증은 별도 승인 연구 | 오염 제거 뒤에도 근거 보강과 조건부 후보를 구분하며 핵심 제약 충족 증거 발견 |
| 비교판 실제 이미지·다른 편성 원판·workbench 검사 누락 | F391 표제지/본문 p1, IMSLP 816553 또는 별도 편자의 실제 총보/파트, manifest/check 수행 | 실제 판/편성·마디가 일치하거나 반례로 드러나면 관련 판정 조정; check 성공 후 검증 상태 상향 |
