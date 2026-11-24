# AF-RES-132 — 한 AI 독자의 순차 실제 열람과 처방 변화

## ① 사건별 관측 (봉인 당시만)

| 사건·배정 | 요청만 본 답 (a) | 첫 면 뒤 답 (b) | 둘째 면 제시·열기·중단 | 최종 답 (c)과 달라진 주장 | 당시 본 근거 URL·코드포인트 구간 [시작,끝) | 미확인 |
|---|---|---|---|---|---|---|
| 1 P3 B · F | 중복 헤더 가설; 위치 기반 리스트로 81열/빈값 보존 | DictReader 첫 행·dict 매핑과 길이 불일치 구별; 처방 유지 | 원함, 미제시·미열람; 종료 | len(set(fieldnames))=54인지 검사 구체화. 원래 처방과 보존 조건 유지 | [F](https://github.com/python/cpython/blob/b28265d7e6a41a4a0e227b37f4fbbc4d03a0a707/Doc/library/csv.rst#L149) [6317,7817), 상대 4–11,13–17 | 첨부 CSV, 실제 54 고유 헤더, 3.9.12 동작 |
| 2 P2 C · F | 명시 호환 모드에서 정확한 SEP=; 첫 줄만 소비, 실제 헤더·값 보존 | 첫 행 키와 kwargs 직접 근거; excel 이름만으로 지원 확정 금지 | 원함, 미제시·미열람; 종료 | 동일 처방, 기본 자동 인식 보류 | [F](https://github.com/python/cpython/blob/deaf509e8fc6e0363bd6f26d52ad42f976ec42f2/Doc/library/csv.rst#L149) [6317,7817), 상대 1–11,13–19 | SEP 관례/정확한 문법, 정상 헤더 오인, BOM 등 |
| 3 J1 B · F+N | 복원한 전체 스트림을 INDEX(stream; .id)에 전달, 최종 인덱스 메모리 별도 | 두 인자 정의가 스트림 값별 키임을 확인; 처방 동일 | 원함·제시·열람; 한 면 뒤 종료 | 동일 명령과 결과의 댓글 보고 추가; 좁은 근거만 보강 | [F](https://github.com/jqlang/jq/blob/2e01ff1fb69609540b2bdc4e62a60499f2b2fb8e/docs/content/3.manual/v1.6/manual.yml#L1964) [70763,72263), 상대 1–5; [N](https://github.com/jqlang/jq/issues/2528#issuecomment-1405388586) [0,283), 상대 1–15 | 1.6 실행, 중복/누락 id, RAM, 스트림 경계 |
| 4 J2 C · F+N | 내부 YAML 문자열 단위 파서, 외부 도구 허용 시 대안, 순수 jq 불확실 | fromjson은 JSON 입력의 값 단위 변환; YAML 해결 아님 | 원함·제시·열람; 한 면 뒤 종료 | jq 자체가 필수 아니라면 fq map(from_yaml) 구체적 조건부 후보 추가; 순수 jq 유지 유보 | [F](https://github.com/jqlang/jq/blob/2e01ff1fb69609540b2bdc4e62a60499f2b2fb8e/docs/content/3.manual/v1.6/manual.yml#L1770) [63133,64633), 상대 1–7,9–18; [N](https://github.com/jqlang/jq/issues/2530#issuecomment-1403891054) [0,278), 상대 1–13 | 실제 fq 판/실행, YAML 타입·복수 문서/태그·오류, 순수 jq |
| 5 P1 B · F+O | 유효한 기존 비빈 CSV에 마지막 종결자 없을 때만 추가 뒤 writerow, 0과 42 보존 | DictWriter 필드 순서/키; 경계 수리 규칙은 아님 | 원함·제시·열람; 한 면 뒤 종료 | dialect 차이(LF 및 인용)만 보강; EOF 처방 동일, 'w' 예제와 append 구별 | [F](https://github.com/python/cpython/blob/deaf509e8fc6e0363bd6f26d52ad42f976ec42f2/Doc/library/csv.rst#L191) [7854,9354), 상대 4–16; [O](https://github.com/python/cpython/blob/deaf509e8fc6e0363bd6f26d52ad42f976ec42f2/Doc/library/csv.rst#L222) [9354,10854), 상대 5–20,32–34 | 원본 끝 바이트/인용/인코딩·dialect, 실제 append |
| 6 J3 C · F+O | startswith("cd ") 단일 분기와 .[3:]로 접두사 제거, 불일치 빈문자 | gsub 전역 비중첩 대체 정의; 앵커 원인 유보 | 원함·제시·열람; 한 면 뒤 종료 | sub/gsub 일반 예제로 좁은 차이 보강; sub는 검증 전 후보, 기존 접두 처방 유지 | [F](https://github.com/jqlang/jq/blob/2e01ff1fb69609540b2bdc4e62a60499f2b2fb8e/docs/content/3.manual/v1.6/manual.yml#L2370) [85988,87488), 상대 1–9; [O](https://github.com/jqlang/jq/blob/2e01ff1fb69609540b2bdc4e62a60499f2b2fb8e/tests/onig.test#L62) [1674,2571), 상대 1–25,27–36 | 1.6 실행, ^·부정 lookahead 실제 기제, 일반 정규식 |

## ② 좁은 직접 지지와 핵심 조건 판독 (해제 뒤 자기판독, 독립 아님)

| 사건·주장 | 좁은 근거 지지 | 핵심 조건 해결·유보 | 반대 근거·판 (사후만) | 과잉 확정·악화 | 판독자 |
|---|---|---|---|---|---|
| P3.1–4 | F의 키 매핑/길이; 가설 지지, 실제 파일 아님 | 유보: 81열 실제 중복과 3.9.12 | [구현](https://github.com/python/cpython/blob/b28265d7e6a41a4a0e227b37f4fbbc4d03a0a707/Lib/csv.py#L93-L127) dict(zip); [원 이슈](https://github.com/python/cpython/issues/112958) 3.13 보고 및 요청 변경(고유 헤더 수) | 검사 제안이지 성공 확정 아님; 실제 파일 없음 | 본 독자 자기판독 |
| P2.1–3 | F의 첫 행/kwargs 지지 | 유보: 표준/확장, 기본 기능 변경 | [원 이슈](https://github.com/python/cpython/issues/109644#issuecomment-1737485816) skip/seek/strip 보고; 정당한 SEP= 헤더 오인·비seek 스트림, 공백 구분자 | opt-in은 보존 조건; 완전 호환 미주장 | 동일 |
| J1.1–4 | N의 정확한 샘플 명령·출력은 댓글 보고, F의 INDEX 정의 | 유보: 메모리·id 정책·판 | [구현](https://github.com/jqlang/jq/blob/2e01ff1fb69609540b2bdc4e62a60499f2b2fb8e/src/builtin.jq#L290-L310) reduce 축적·동일 키 덮어씀 | 원 처방 그대로; 성공/메모리 과잉 확정 없음 | 동일 |
| J2.1–4 | N의 정확한 입력 방향/샘플은 댓글 보고 | 유보: 순수 jq, 허용 도구, YAML 의미 | [원 작성자](https://github.com/jqlang/jq/issues/2530#issuecomment-1411829108)가 추가 도구를 원치 않음; JSON 시험은 YAML 아님 | 조건부 추가만; 무조건 채택이었다면 악화. 실제 조건을 나중에 확인하니 채택 보류 | 동일 |
| P1.1–3 | F의 DictWriter, O의 dialect만 직접 지지 | 유보: EOF 경계와 실제 파일 | [RFC 4180 §2](https://www.rfc-editor.org/rfc/rfc4180), [writer 구현](https://github.com/python/cpython/blob/deaf509e8fc6e0363bd6f26d52ad42f976ec42f2/Modules/_csv.c#L1298-L1327) suffix 추가 후 write; [댓글](https://github.com/python/cpython/issues/100821#issuecomment-1374869968) 자동수리 호환성 | 실제 파일 검사 조건 유지 | 동일 |
| J3.1–3 | F·O 일반 전역 대체/단일 대체 비교 지지 | 유보: 정확한 버그·넓은 요구 | [원 작성자](https://github.com/jqlang/jq/issues/2532#issuecomment-1409603192)의 다중 cd 요구와 g 실패; [후속 보고](https://github.com/jqlang/jq/issues/2532#issuecomment-1599128800) 다른 판 PR | 단일 prefix로 일반화하지 않음; 확대 요구에는 부족 | 동일 |

## ③ 배정·실제 열람·비용 비교

| 배정 조건·계열 | 예정/완료/금지 노출 없음/제시/추가 열람 | 처방 변경/근거만 보강/새 유보/악화 | 고유·누적 문자 / 관측 비용 | 비교 한계 |
|---|---|---|---|---|
| F · B P3/C P2 | 2/2/2/0/0 | 0/0/0/0; P3 검사 구체화 1 | 사건내 고유 3000, 누적 3000; 조건내 정확한 본문 고유 1500 | 실제 추가 열람률 0/0 산출 불가; 슬롯2 반복 노출 |
| F+O · B P1/C J3 | 2/2/2/2/2 | 0/2/0/0 | 사건내 고유·누적 5397; 4면 | O는 일반 근거, 버그 핵심 조건 부재 |
| F+N · B J1/C J2 | 2/2/2/2/2 | 1(조건부)/1/0/0 | 사건내 고유·누적 3561; 4면 | J1은 기존 처방 예상; J2는 실제 제약에 불합 |
| 계열 B | 3/3/3/2/2 | 0/2/0/0; 검사 구체화 1 | 6283; 5면 | 세 사건이 다름 |
| 계열 C | 3/3/3/2/2 | 1(조건부)/1/0/0 | 5675; 5면 | 슬롯2 동일 본문 재노출 |
| 전체 | 6/6/6/4/4 | 1/3/0/0; P3 구체화 1, P2 변화 없음 1 | 사건내 고유·누적 11958, 전역 고유 10458, 실제 10면·고유 9면; 면당 1500 이하 | 시간/도구대기 미측정; 한 AI, 6개 사건, 조건당 2 |

분모: 예정 6/6 완료·세 단계 모두 봉인; 금지 필드 누출 관측 0/6, 독립성 보장 아님. 첫 면 6/6, 추가 면 원함 6/6, 제시 4/6, 열람 4/4 제시(4/6 배정 전체), 사용(좁은 주장 포함) 4/4 열람, 핵심 증거로 새롭게 쓰인 샘플 2/4(N 둘), 처방 변경 1/4 열람(1/6 전체), 조건부 후보가 아닌 확정 핵심 조건 해결 0/6; 핵심 유보 유지 6/6. 추가를 거절하거나 중간 중단한 경우 0/4 제시, 둘째 면 후 종료 4/4, F-only 종료 2/2; 같은 사건 재독 0. 직접 좁은 근거 6/6(첫 면 후에도 6/6); 보강만/변경은 사건 단위 상호 배타적 주분류이며 개별 주장에 복수 태그 허용. 사건 간 같은 본문은 슬롯1·2의 두 판 1500자; 이 중 뒤 노출 1건 제외 시 5/6, F 1/2·O 2/2·N 2/2, 변경 1/5, 보강만 3/5; F 누적 1500자, 총 10458자. 문서 계보 공유까지 엄격히 제외할 독립 표본은 확정 불가. 읽기와 도구대기 타임스탬프 신뢰할 수 없어 null, Git commit 시각을 읽기 시간으로 변환하지 않음. 요청 원문 길이 6250자는 별도(면 예산/합계에 미산입).

## Q1–Q2 가림·배정 검산

- 시작판 `adafe971a088300e3a5319f95c5341db4c27e334`, 계획판 `f5279cabf578ae93dd2374adb4f6fb525ce06b9d`; 선행 인계 `cdf5522ccfad9c240ded4e658b6fcc638ee14199`, 선행 결과 `3c8a3cf52c84cd9a8c5a06421087733bb8319e6b`. 선행 파일 전문은 여섯 번째 c 커밋 후 열었다.
- tool-side 4파일만 사용, raw row·기존 점수·정답·그룹·후속 면 반환 금지. 초기 구조/길이 검산은 집계만 출력; synthetic 5개 금지 필드 검사 0 누출, SHA-256 known-answer test 통과. 첫 노출 전에 [preflight](projection/preflight.json) 및 배정 해시 커밋 `b237b98f83d35c5432833923324a8166aa612d47`. [assignments](assignments.json)에서 2계열×3 배정, 해시 동일 `baad4da683f50e765170d51ce512e5d8a033d16330ce4d0d1d1ab885e693af0b`. [절차 코드](projection/protocol.js) 포함. 18 bundle 중 18 확인, F/O 위치 연결 및 N exact case_id, 세 번째 면 제외(P1). 실제 면 10/10을 해제 후 외부 직접 다시 대조: [F/O](evidence/external-slice-check.json) 8/8 정확 일치, [N](evidence/external-N-check.json) 2/2 raw CRLF 정확 일치(LF 정규화하면 2/2 불일치). 이 검산은 사전 가림 검사에 소급하지 않는다.
- 봉인 시에는 투영된 불투명 슬롯·요청·현재 면 ID와 본문만 받았다. 요청 자체에 이슈/첨부 링크가 있더라도 허용 요청 내용이며 외부 열기 하지 않음. 모델이 이전 답을 지식으로 가지고 있지 않다는 것은 증명 불가. 슬롯2 반복을 인지했고 다른 슬롯도 Python/jq 문서·일반 함수의 사전 인지 기록. AF-RES-124/128 연구 세션과 현재 작업자의 모델 계열이나 학습 데이터가 겹칠 수 있음; 현재는 새 대화의 단일 독자, 앞 편집자와 세션상 구분, 현재 채점자는 같은 독자. 새 독자 역할 여러 개를 모사하지 않음.
- 18 단계 GitHub 고정 커밋별 파일 동일 재열람 성공. 마지막 독자 봉인 `be71c73cb15c45dc70fc017675e082e442bb4cb0`. [answers.jsonl](answers.jsonl) 및 [reading.jsonl](reading.jsonl) 18/46행, [release-check](evidence/release-check.json) 집계. 본문·원장 합산 시 구간 지문 포함; 당시 근거와 해제 후 근거 분리.

## Q3–Q6 해석·반례와 권고 (사후)

a→b: 여섯 건 모두 요청 단계에서 이미 일반 지식으로 작동 후보가 있었다. F는 정확한 좁은 규칙을 지지했으나 처방 변화 0/6. b→c: F-only P3에서 검사 방법을 구체화했으나 작동/보존 처방은 유지. 따라서 무추가에서도 표현·진단 수정 가능(1/2), 실질 처방 수정은 0/2. 추가 면 열고도 처방 변경 없음 3/4; 근거를 정확히 구분하면 N J1은 같은 입력의 좁은 보고, O P1/J3는 주변 규칙·다른 입력의 시험이다. J2가 유일한 구체 도구 후보 추가; 후보가 순수 jq라는 주장이 없으며, 원 작성자의 추가 도구 기피 조건을 사후 확인한 결과 전체 채택은 보류. 이 조건을 감춘다면 오히려 부적절. 명시적으로 지지 없는 확정 0/6, 실제 악화 0/6(자기판독·이견 가능), 새 유보 0/6(유보 유지 6/6). J3의 sub는 실행 전 후보 언급이지 주 처방 변경이 아님.

실제 반증 탐색: (1) P3는 3.13 보고와 3.9.12 요구의 판 차이, dict(zip) 소스와 실제 첨부 미확인; (2) P2는 Ruby/Rust의 명시 헤더/구분자 사례와 SEP= 헤더 오인; (3) J1의 누락/중복 id, reduce 메모리; (4) J2 원작성자 반대 댓글과 다른 도구 yq/JSON round-trip의 방향 차이; (5) P1 RFC 마지막 개행 생략, Go reader NoEOLTest와 CPython fresh write 시험은 다른 조작; (6) J3은 다중 cd를 한 줄에 처리하는 후속 요구 및 ^/lookahead 없는 일반 패턴. 각 행의 소스는 [sources.jsonl](sources.jsonl), 주장 대응은 [claims.csv](claims.csv). 과거 128의 9/18 가림 재판독 일치는 별도의 과거 채점 안정성 관측; 과거 독자 답과 현재 a/b/c가 일부 동일/다르다는 사실을 링크 효과로 계산하지 않음. 외부 댓글은 저자 보고, 코드 정적 확인은 해당 판, 실제 독서 결과만 이 세션 관측.

**설계 조건부 제안:** 첫 문서로 이미 처방 가능한 사건은 보존·예외 조건을 한 줄로 고정하고, 둘째 문서는 그 미해결 조건을 직접 입증하거나 반증하는 최소 구간일 때만 우선 제공. 둘째 면의 유사 제목·일반 예제·다른 실행기·다른 판은 별도 범위 표시. 바꾸지 않은 답도 성공/실패 어느 쪽으로 강제 채점하지 말고 좁은 근거 증가와 핵심 해결을 독립 표시. 도구 허용/성능/입력·판 조건은 검색 순위보다 우선하는 필터 후보. 제시와 자발적 열람을 구분. 본시험은 6건 한 AI 독자, 특정 사건별 난이도, 조건당 2건, N이 둘 다 jq 사건이며 공유 계보도 다름. 처방 변경 1/2 N vs 0/2 O는 기술적 기술통계, 모집단 효과·사람 독서 시간·유의성·일반적 N 우월성 추정 금지. 모든 제시를 열었으므로 중단 설계의 효과도 미관측.

## Q7 사후 별도 영역 대조 (본시험 6건에 합산하지 않음)

| 사례 | 직접 연 안내 → 실제 면 | 확인한 보존 조건과 다른 판단 | 반례/한계 |
|---|---|---|---|
| 서지 BIB.1–3 | [1813 1권 색인](https://en.wikisource.org/wiki/Index:Jane_Austen,_Pride_and_Prejudice_(1st_ed,_1813,_vol_1).pdf), [Title scan 6](https://en.wikisource.org/wiki/Page:Jane_Austen,_Pride_and_Prejudice_(1st_ed,_1813,_vol_1).pdf/6), [본문 scan 8](https://en.wikisource.org/wiki/Page:Jane_Austen,_Pride_and_Prejudice_(1st_ed,_1813,_vol_1).pdf/8) — 각 페이지에서 실제 JPEG 스캔을 클릭해 읽음 | 색인 London, 1813, Egerton, OCLC 931247407; 표제지에는 3권 구성·Vol I·저자 대신 Sense and Sensibility 저자·London T Egerton 1813. 색인 인쇄 p1=PDF 8(실제 본문 시작·서명 B·소장 도장); scan 6은 표제지. 따라서 같은 작품 제목에서 인쇄 페이지·스캔 페이지·권·판을 함께 지정해야 실제 인용 위치를 보존. 판권면 대신 당시 표제지 사용. | [1817](https://en.wikisource.org/wiki/Pride_and_Prejudice_(1817)) 제3판 2권(표제 전사), 1813과 권/쪽 계보 다름. 1833 색인은 미교정·면 미검증. [MARC 020](https://www.loc.gov/marc/bibliographic/bd020.html) 반복 ISBN에 매체/권·유효 여부 표시 가능; ISBN만으로 물리 페이지 결정 불가. 현대 판권면 부재/전체 페이지 대응 미검사. |
| 음악 MUS.1–3 | [Sibley 안내](https://urresearch.rochester.edu/institutionalPublicationPublicView.action?institutionalItemVersionId=16571) → [총보 PDF](https://urresearch.rochester.edu/fileDownloadForInstitutionalItem.action?itemFileId=52762&itemId=16807) / [파트 PDF](https://urresearch.rochester.edu/fileDownloadForInstitutionalItem.action?itemFileId=52763&itemId=16807) — 각각 PDF 첫 두 페이지 이미지 실제 열람(표지 및 인쇄 p2) | K581 op108, F.X. Gleichauf 편곡, J. André plate 11034, A clarinet + piano. 안내 제목은 원곡 5중주, 표지에 여러 다른 편성 나열, 실제 총보 p2는 3단(클라리넷 1 + 피아노 2). 파트 p2 같은 plate/arranger/Clarinetto in A; 첫 Allegro 6마디 쉼표가 파트에서 한 묶음 6으로 표시, 제7마디 여덟분쉼 뒤 상승 음형 동일. 첫 상승 음형의 낮은 C4(아래 첫 덧줄) 같은 기보 위치; A 클라리넷의 기보 C4는 실음 A3. 총보 클라리넷 조표 0, 피아노 3#; 음표를 일괄 실음 취급하면 틀림. 보존: 제7마디 진입, 음높이/길이/쉼표·순서·이조 악기, 반주와의 동시성. | 원곡 A clarinet+strings와 피아노 축약판은 같은 제목이라도 다른 편성. [Boosey 2017](https://www.boosey.com/cr/music/Karl-Jenkins-Symphonic-Adiemus-version-for-concert-band/103565)의 Bb/Eb/실음·음자리표 대체 파트 안내는 실제 파트 확인을 요구. [Argue](https://www.scoringnotes.com/tips/djas-notes-music-preparation-basics/) 총보 실음/기보 명시, 옥타브 악기 예외, 연주자 파트 및 페이지 넘김. 전체 마디·모든 음·음향 직접 대조 아님. |

편집자는 서지의 경우 색인→표제지→본문 3개, 음악의 경우 안내→표지/총보 p2→파트 표지/p2의 페이지 4개를 찾아야 했다(탐색 시간/토큰 계측 없음). 원 작성자의 실제 요구가 이번 사례에 별도 기록된 것은 아님: 도서 인용 시 판·권·쪽/물리면 보존, 편곡자는 악기·마디·음·리듬·이조와 다른 파트의 동시성 보존이라는 자료에서 추론한 설계 조건. 이번 사후 독자가 실제 읽은 것은 위 스캔 2개와 악보 페이지 4개 및 안내/문헌이지 전체 작품이 아니다. 표제와 실제 페이지가 다르면 설명/원문 매핑을 보류하고, 총보와 파트 중 하나가 없으면 음 보존 판정 유보. 실제 비용을 사람의 독서 시간으로 환산하지 않는다.

## 원전·검사와 제한

[sources.jsonl](sources.jsonl): 35 기록 행, 적격 29행/고유 24저작(원질문 6, 공식 정의·구현 6, 별도 시험·예제 6, 서지 3, 음악 3). 동일 이슈 댓글, 동일 시험 suite, 동일 판의 여러 페이지/PDF는 하나로 집계. 6행은 실패 또는 설명만 확인으로 제외(LOC 두 URL 403, Gutenberg 실패, 1833 색인만, Mutopia/IMSLP 설명만). 브라우저 확인 정확 UTC 미제공인 행은 원장 작성 UTC와 별도 표기. [evidence/external-slice-check.json](evidence/external-slice-check.json)·[evidence/external-N-check.json](evidence/external-N-check.json) 실제 비교는 해제 후이며 읽기 분모가 아님. [SELF_CHECK](SELF_CHECK.md) Q1–Q7 자기검사. 로컬 checkout/workbench 명령 및 jq/Python 원문 예제 실행은 하지 않음; user scope상 jq/Python 실험 제외, manifest/check만 별도 재개 필요. 따라서 상태 **PARTIAL**(순차 새 읽기와 원전 최소량 충족, 지정 workbench check 미실시, 원본 CSV 부재 및 독립 재현/가림 인지 제약). 

| 중요한 불일치·약점 | 다음에 열 자료 또는 수행할 검사 | 판단을 바꿀 관측 |
|---|---|---|
| J2 구체 처방은 추가 도구 거부 조건과 충돌 | 동일 버전의 jq 내장 기능/허용 도구 목록과 실제 YAML 내부 값 요구를 확인 | 기존 도구 내에서 실제 샘플과 보존 예외를 충족하면 채택 가능; 아니면 조건부 후보도 보류 |
| 하나의 AI·공유 F·조건별 다른 사건 난이도 및 자기판독 | 새 독립 세션의 동등 사건 교차 배정·가림 채점, 선노출 제외 | N이 핵심 조건 해결을 반복 늘리고 악화를 만들지 않는 관측; 반대면 우선순위 폐기 |
| workbench 지정 검사 미실행·실제 CSV/대용량/regex 재현 미확인 | 정확한 manifest/check 명령을 checkout에서 수행; 원 입력과 판을 확보해 별도 승인 연구 | 검사 성공 및 실제 보존/조건 재현이면 확신 상향; 불일치면 관련 주장 하향 |
