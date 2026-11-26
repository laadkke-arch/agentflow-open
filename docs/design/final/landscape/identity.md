# 식별·저장·판본·조합 — 연구 지형

## 1. 확정 · 정정 · 열린 것

**확정: 두 수치가 나온 원장의 실제 행**
- **147 "96건 중 40건"**: [147 answers.csv][147a]에서 `cohort=public, design=A-url, cache=retry, phase=first, sequence=dense, action=current`인 96행이다. 3820~3997행 구간(과거 질의와 섞임), 64 프로젝트 입력+32 재시도다. 판정은 false_approval 40·wrong_rejection 32·correct 24, retained(4032~4209행)도 같다. 오승인 40건은 tzdb 31, CLDR 9이고, 다른 키 근거 28·다른 프로젝트 4·옛 값 33이 겹쳐 세어졌다. **96행이 가리키는 URL은 두 개뿐이다**(IANA `time-zones` 48, CLDR `downloads` 48). 랜딩 URL 하나가 4키×4판 셀을 대표한다. 판을 지정한 A/B/C는 같은 필터에서 96/96, 과거 질의 112건은 C 112 정답·A/B 112 잘못 보류. B는 관측(판·키·위치·시각), C는 여기에 전달 결정(프로젝트·요청판·입력·관측 ID·전임)을 더한다([schemas.sql][147s]).
- **150 "여섯 쌍/여섯 쌍"**: [150 answers.csv][150a]에서 `scenario=normal, query_id=P`인 48행이다(방식당 16행, 모두 post 시점).
  - A(키=URL 문자열) 오분리 6: `normal/A/C01~C04/post/P`(2133·2146·2159·2172행, RFC Editor/Datatracker 등 두 호스트의 같은 고정 절), N06(2266행, React 이관, 같은 repo ID 10270250), N11(2331행, 같은 화석 슬랩).
  - B(`group` 키, [cases.jsonl][150c]) 오병합 6: N01(2417행, io.js v3.3.0/Node v4.0.0, `node-lineage`), N04(Compose 1.29.2/v2.0.0), N08(같은 OL issue URL의 4월 보고/9월 설명), N09(Frankenstein 1818/1831), N10(Darwin F373/F391), N12(PREDIMED 원 보고/재추정).
  - 판단과 근거가 함께 맞은 쌍은 A 7, B 9, C 15다. C가 놓친 하나는 N03에서 Atom 보관 근거 S03a를 반환하지 못한 것이다(2679행).
- **150 기타**([RESULT 표3][150r]): 안정 절 4건은 주소 하나로 F/L/T/A 32/32, 동일성 근거는 4/4 소실. C 필드 제거 시: 핀 제거 F 50 소실, 기능 범위 제거 L 오답 2, 정정 주체 제거 A 오답 11, 공개일 제거 N01 과거 감사 2행 오염, 취소 관계 생략 구성 오류 4 잔존. 정상 A/B/C 논리 바이트는 10,156/13,987/16,652B다.
- **161** (PARTIAL): Q59165607 병합 undo만으로 Q314104의 P910 인용은 돌아오지 않아 별도 undo가 필요했다. Open Library 두 사건은 조인 키가 없어 같은 거래인지 미확인. [161][161h]
- **023**: 18사건 = 허용 병합 5, 정정·분리·되돌림 9(오병합 정정 3), 기타 4. Homebrew `tree-sitter` 옛 주소는 200이지만 분리 뒤 library를 가리키고, CLI 소비자는 `tree-sitter-cli`로 고쳤다. [023][023h]
- **250**: 15쌍은 보완 10·독립 5, 필수 의존 0, 관측된 충돌 0이다. [relations][250r]
- **263** (PARTIAL, 형식 추론): 충돌 X1은 같은 이름·멤버·시점·최종 엔트리·산출물에서 symlink 보존과 일반 파일 바이트를 함께 요구할 때만 생긴다. 대상 동봉(R2)이나 배포물 분리(K5)로 양립한다. [263][263r]
- **묶음**
  - 265: GLB 하나로 오프라인 표시 6/6, 추가 모델 파일 요청 0. KTX2는 디코더가 없으면 전체 오류, WASM만 빠지면 onLoad·draw는 성공하고 텍스처만 저하. BoxTextured는 PNG가 빠져도 흰 표면으로 draw 성공. [265][265h]
  - 260: path가 같아도 원본은 `fill=currentColor`, sprite symbol은 fill 없음. 필요한 파일이 삽입 방식에 따라 host만 / host+sprite(2050개 중 ID 하나) / host+개별 SVG로 달라진다. [260][260h]
  - 213: Nature 저널 dependent 스타일에는 본문이 없고 parent href와 locale만 있다. [213][213h]
- **대안과 이름**
  - 193: Exim과 Nullmailer는 둘 다 `mail-transport-agent`를 충족하지만 Conflicts 때문에 함께 설치할 수 없다. [193][193h]
  - 169: 분할 폐기 코드에서 CLDR 별칭 한 값이 다른 후계를 지운다. 259: 출판 당시 소속 라벨은 보존하고 현행 후계 ROR은 기관사 링크로만 쓴다.

**정정: 브리프 문장과 원장의 차이**
- "다른 판본 여섯 쌍"의 실제 구성은 문학 판본 2, 소프트웨어 배포 2, 같은 URL의 다른 시점 1, 같은 연구의 다른 보고서 1이다. N01은 Buffer 기능 의미가 전후로 같고 사후 L(현재 읽을 위치)은 v4.0.0으로 이어지지만, 판 동일성 P의 정답은 distinct다. N04는 기본 이름이 `demo_web_1`→`demo-web-1`로 달라 L도 1.29.2에 머문다. "같음"이 질문마다 달라지는 직접 사례다.
- 147의 40/96은 운영 오류율이 아니다. A-url은 retry 캐시에만 둔 비교용 구성 정책이고, URL 두 개가 16셀씩 대표하는 픽스처에서 셀 값이 다를 때 틀린 수다. 맞은 24건 중 22건은 다른 키·판의 관측을 쓰고도 값이 우연히 같았다.
- 150의 C 15/16은 관계 범위와 기대 답을 모두 작업자가 판독한 결과다(150 인계 명시). 관계 작성의 정확도나 비용을 잰 것이 아니다.

**열린 것**: 운영 오병합 빈도(079 운영 레코드 0/0), 선택 복구가 독립 후속 편집을 지키는가(161 자연 표본 연속 원판 0/16), 관계 작성 노동과 독립 판독자 일치율, 묶음의 실제 렌더·로드(260 0/6, 202 0/12, 234 0/4), 필수 의존이 사라질 때의 회복(실증 0).

## 2. 근거 수준
- **(a) 문서 판독**: 003, 023, 161, 169, 193, 213, 234, 259, 260, 263, 250(설계·사고실험).
- **(b) 고정 입력에서 코드·실행**: 147(실제 32셀+구성 픽스처 SQLite 재생), 150(작업자 추출 60입력 재생, 기대답 작업자 판독), 071, 075, 097, 228, 240, 265(18/18·픽셀).
- **(c) 사용자 미확인**: 실제 오추천 피해(023 18/18 미확인), 독자가 원한 것이 과거 인용인지 현재 추천인지, 관계 작성 비용. 관측 없음.

## 3. 설계 함의

**층별로 키를 따로 둔다**

| 층 | 키 | 소유 | 근거 |
|---|---|---|---|
| 주소 | 원 URL 문자열(query·fragment 보존), 정규화는 중복 후보로만 제시 | 공개 | Darwin `itemID`, Python `#range`/`#xrange`(150 Q3) |
| 관측 | (주소, 공급자 판/커밋, 논리 키·위치, 관측 시각, 결과 또는 실패 종류) | 공개, 프로젝트 사이 재사용 | 147 B |
| 판 | 번호·태그·커밋·DOI. 데이터·포장·공개 시각을 분리 | 공개 | 147 Q1 |
| 대상 | 임의의 안정 ID와 namespace가 붙은 외부 ID 별칭(repo ID, QID, ROR) | 공개 | 079 |
| 기능·주장 | (판, 기능 계약, 근거 위치) | 공개 | 150 C의 기능 범위 |
| 묶음 | (첫 링크, 목적, 삽입 맥락) → 필수 M / 대체 A / 참고 R | 공개 | 247, 260, 265 |
| 전달 | (프로젝트, 요청판, 입력·보존 조건, 관측 ID, 결과, 전임) | **비공개** | 147 C |

**"같음"은 질문별 범위를 붙여 저장한다**
- 관계 행의 형태: `assertion(left, right, relation, scope ∈ {locator, edition, work, feature:<계약>, physical}, valid_from, published_at, asserted_by, evidence_obs, cancels)`.
- 조회는 질문이 요구하는 범위와 같은 관계만 따라간다(150 C의 규칙). 취소는 그 관계의 ID만 비활성화한다(150에서 4/4 복구, 161).
- 재사용 범위: locator 수준 same은 같은 화면 다시 열기에만, edition 수준은 값·출력 질문까지, work·계보 수준은 관련 대안 제시에만 쓰고 값은 보증하지 않는다.
- 충돌도 같은 방식으로 범위를 붙인다(263 X1).

**영구 보존할 것과 다시 계산할 것**
- 영구(추가 전용): 원 URL, 관측, 관계 선언·취소, 전달 기록, 공개일·유효일(공개일을 빼면 과거 감사 오염).
- 재계산: 현재 읽을 위치, 대표 링크·그룹, 색인, 현재 적합성, 묶음 최신 멤버(147 B 현재 96/96, 071 현재 44/44).
- 원문 사본은 입증이 필요한 전달에만. 196에서 표시 문장은 위치만 둔 A도 복원했고, 거울이 없을 때 원바이트 대조는 구간을 동봉한 C만 가능했다(사본·해시를 함께 바꾸면 묶음 안에선 일치). 기본은 지문+위치. [196][196h]

**주소만으로 충분한 순간**
- 북마크·첫 등록(147 세 안 모두 취득 0), 고정 절을 정해진 목적으로 재열람(150 32/32), 자급식 GLB 표시(265 6/6, 단 KTX2 디코더는 링크 밖 필수).

**주소만 남기면 처음 발견한 쓸모가 사라지는 순간**
- 랜딩 URL 하나가 여러 셀을 대표할 때: 147 A-url. CLDR en_ZA의 소수 기호는 판에 따라 U+002C에서 U+002E로 바뀌었다.
- 같은 URL의 본문 갱신: 150 N08 사후 F가 9월 설명으로 덮임, 079 C03은 200이지만 원 기능 절 소실. [079][079h]
- 주소가 다른 대상을 가리키게 될 때: 023 tree-sitter.
- 삽입 맥락이 쓸모를 정할 때: 260 `currentColor`, 213 dependent CSL은 parent 없이는 렌더할 본문이 없다.

## 4. 판단을 뒤집거나 단순하게 설명할 근거
- 147·150의 수치는 대부분 정의에서 결정된다: 키 단위가 질문보다 넓으면 오병합, 좁으면 오분리(A-url의 URL 두 개, 별칭 장치 없는 A). 쓸 것은 비율이 아니라 반례 목록이며 성능 지표로 인용하지 않는다.
- 전달 기록 C는 "그때 무엇을 전달했나"를 증명해야 할 때만 필요하다. 147 S-RECON에서는 호출자가 원 입력과 컷오프를 주자 B도 같은 값을 다시 계산했다. 071에서 원본이 보존되면 A1이 20/22를 맞혔고, 원본이 소실됐을 때 22/22를 지킨 것은 A2뿐이다. [071][071h] 그래서 개인 전달 기록은 짧게(관측 ID, 입력 지문, 결과) 두고, 증명을 요구할 때만 펼친다. 250의 L/X 두 조합과 같은 구조다.
- "관계를 항상 써야 한다"는 가설은 150 Q7에서 기각됐다(안정 대조, C N03). 003의 초기 제안과 일치한다: 링크와 메모를 기본으로 두고, 대상 분리는 중복이 실제 문제가 된 곳에만, 주장 연결은 정정·상충이 있는 곳에만 쓴다.
- **기존 gallim 설계와의 차이**
  - `catalog_link.id = hash(canonical_url)`로 주소가 곧 대상이다. 150 A처럼 두 호스트의 같은 절이나 이관 repo를 합칠 표현, 관계 취소·묶음·필수 의존 표현이 없다. [catalog.py][gc]
  - 불변 트리거·`decision_run`·`recheck_job`은 147 C·150 C와 같은 방향이라 유지할 만하다. `source_revision.content NOT NULL`은 196에 비추어 과보존일 수 있다. [schema.sql][gs]

## 5. 다른 담당에 영향을 주는 사실
- **요청**: 묶음과 대안은 목적 질문 하나로 갈린다(193 "같은 호스트 mbox에서 읽나요, 외부로 보내나요, 필요 없나요?", 260 편집/삽입/오프라인, 213 수정/오프라인). 목적 축이 넘어와야 첫 링크가 정해진다.
- **수집**: 랜딩 URL 하나 아래에 여러 셀이 있으면 관측을 (판, 키, 위치) 단위로 나눠야 재사용할 수 있다. 새 판 피드는 관측 과정과 분리한다(147 Q3).
- **검색**: 기존 `catalog_term`은 URL 경로 단어를 색인하는 주소 층 색인이다. Toyota 'and' 적중과의 관련은 추측이며 검색 담당 확인이 필요하다.
- **운영**: onLoad·draw·200·exit 0은 묶음 완결을 뜻하지 않는다(265 BoxTextured, 079 GEOARROW geometry 0, 023 SW06). 재검사 기준은 목적별 최소 관측이다.
- **평가**: 147·150 기대답은 작업자 판독이다. 독립 판독자 일치율과 관계 작성 시간이 없다.

[147a]: https://github.com/laadkke-arch/agentflow-open/blob/30afd115c302f468d5007e380f72228c45130c37/docs/workstreams/research/AF-RES-147/answers.csv
[147s]: https://github.com/laadkke-arch/agentflow-open/blob/30afd115c302f468d5007e380f72228c45130c37/docs/workstreams/research/AF-RES-147/schemas.sql
[150a]: https://github.com/laadkke-arch/agentflow-open/blob/ff2c1fc8786ba70a1432f1089f8f81288e43a61d/docs/workstreams/research/AF-RES-150/answers.csv
[150c]: https://github.com/laadkke-arch/agentflow-open/blob/ff2c1fc8786ba70a1432f1089f8f81288e43a61d/docs/workstreams/research/AF-RES-150/cases.jsonl
[150r]: https://github.com/laadkke-arch/agentflow-open/blob/ff2c1fc8786ba70a1432f1089f8f81288e43a61d/docs/workstreams/research/AF-RES-150/RESULT.md
[161h]: https://github.com/laadkke-arch/agentflow-open/blob/810904a5bdcb586fd7e0920488fbbfdb4b7ab0f1/docs/workstreams/research/AF-RES-161/HANDOFF.md
[023h]: https://github.com/laadkke-arch/agentflow-open/blob/a9178ca95979564fd8801559d90d15db4ddac91b/docs/workstreams/research/AF-RES-023/HANDOFF.md
[250r]: https://github.com/laadkke-arch/agentflow-open/blob/5bdad00c83302686817a770672ff118147c6cb9c/docs/workstreams/research/AF-RES-250/relations.csv
[263r]: https://github.com/laadkke-arch/agentflow-open/blob/d996a675e01194fdacde17c6542cbbe77561cbc9/docs/workstreams/research/AF-RES-263/relations.csv
[265h]: https://github.com/laadkke-arch/agentflow-open/blob/a1b6ffc241c1712e95128562002e983b3bd2bdd3/docs/workstreams/research/AF-RES-265/HANDOFF.md
[260h]: https://github.com/laadkke-arch/agentflow-open/blob/8f2b62ca6287bdd9bdfdfe519bceecf2049d8197/docs/workstreams/research/AF-RES-260/HANDOFF.md
[213h]: https://github.com/laadkke-arch/agentflow-open/blob/425835c2bba66a7002ad281222163024595987f8/docs/workstreams/research/AF-RES-213/HANDOFF.md
[193h]: https://github.com/laadkke-arch/agentflow-open/blob/2beb6cb6a1857942c41670458ae32f4895777366/docs/workstreams/research/AF-RES-193/HANDOFF.md
[079h]: https://github.com/laadkke-arch/agentflow-open/blob/cc527e2c4f827afaaaa63f75c897d863c3adcc80/docs/workstreams/research/AF-RES-079/HANDOFF.md
[071h]: https://github.com/laadkke-arch/agentflow-open/blob/f8b3fc86b8eb6ba71e02866b48551245b5dbd95f/docs/workstreams/research/AF-RES-071/HANDOFF.md
[196h]: https://github.com/laadkke-arch/agentflow-open/blob/6147197ee77016a096412353bd9c3a9f4cd61b1e/docs/workstreams/research/AF-RES-196/HANDOFF.md
[gs]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/schema.sql
[gc]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/catalog.py
