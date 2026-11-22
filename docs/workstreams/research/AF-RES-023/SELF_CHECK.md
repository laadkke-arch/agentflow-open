# AF-RES-023 — 자기 점검과 수용 판정

**판정: REVIEW_READY_WITH_GAPS.** 자료 수·비교행·보고서 구조·브랜치 소유 범위는 확인했다. 완전한 전후 ID/정정판18건, 날짜가 있는 소비자 인용6체인, 약3분의1씩의 표집 구성은 충족하지 못했다. 구조 검사가 통과했다고 이 미확인을 성공으로 바꾸지 않는다.

## 실제 분모

| 단위 | 확인값 | 해석 제한 |
| --- | --- | --- |
| 주 사건 | 18 = MusicBrainz6 + ROR6 + Homebrew5 + Wikidata1 | 적용병합·분리·기각·동일ID오염정정을 별도 코드로 유지. 완전 전후 chain18이 아님. |
| 구성 | 허용 catalog 병합5 / 정정·분리·되돌림9 / 기타4 | 목표6/6/6 대비 정정군 과다. 정정9중 literal merge 정정3. |
| 출처 원장 | 135행, 고유 ID135·고유 URL135 | 접근 실패·보충·같은 사건의 전후판을 포함. 전체를 독립 증거로 세지 않음. |
| 보수적 최소 원문 | 38 = 사건 대표18 + 정책/지침12 + 소비자 원장8 | 같은 사건 화면은 대표1개만 최소수에 산입. policy는 사건 성공 증명이 아님. |
| 소비자 | 원장13행; 최소수8, 외부 발행자 독립7 | dated 후속chain4(외부3+Wikidata 내부1), 불변전후diff3. ROR4원문의 최초작성/수정일 미확인. |
| 복원 비교 | 54 =18×3 | v3 동일16사건48행 + v4 두사건 재판독6행. 실제 역사 추천문18개가 아닌 통제된 보기. |
| 필드 점검 | identity 독립열18행; restoration18×5=90행 | AUTO는 구조화 필드 추출가능성 해석. 자동 복구 실행0/18. |

분모의 기계 대조는 `evidence/counts.json`, `evidence/reconstruction-summary.json`, `scripts/validate_research.py`에 있다. 미확인 사건을 분모에서 제거하지 않았다.

## Q별 결론·근거·반증·미확인·검사

| Q | 결론과 범위 | 실제 근거 위치 | 반증 탐색·반대 근거 | 미확인·최소 다음 입력 | 검사 결과 |
| --- | --- | --- | --- | --- | --- |
| Q1 | 동일 표면의 변경도 중복병합/정상rename/분리/기각/오염정정으로 다르다. | RESULT.md117행 Q1; events.jsonl MB01–06/ROR01·02·05–08/SW01·02·03·05·06/WD01; sources MB-S37·SW-S14·ROR-S09 | MB04/05/06 허용, ROR02 기각, SW04 이유불명 취소를 분리. 시스템별 SEARCH_LOG에 열린편집ID/제외근거. | MB01 source매핑추론, MB03/04source ID, MB06즉시target. 공식edit_data4행부터. | 사건18·4시스템·최대6은통과; 완전전후18은미충족. |
| Q2 | URL/record/실체/판/목적을 독립 판단. | RESULT.md127행 Q2; identity-layers.csv18행; MB-S10·ROR-S23·WD-S06·SW-S01 | MB01 같은DiscID다른release vs MB05 누락트랙중복; SW01 다른이름같은archive; ROR 본교/지부와 동명기관. | 외부 ID 발급기관 원문 전수검증 없음. 원 ISRC/GRID/ISNI/GND record와 당시provenance 필요. | 독립열·제안/반대근거 필드 확인; 발급자 전수검증은미충족. |
| Q3 | 200과기능보존,404와역사판존재를 구별. | RESULT.md139행 Q3; software/http-observations.json; SW-S05·14·25, MB-S23, ROR-S28·31 | SW06 oldformula200/library, SW02 old main404/fixedrecipe본문; MB06현재target을2022에소급하지않음. | MB/ROR HTTP·중간chain; fixed원행/응답관측 필요. | 실제HTTP15관측과문서열람분리. 요구한두반례확보. |
| Q4 | 본체취소와소비자/속성복구는 따로 확인. | RESULT.md149행 Q4; restoration.csv90행; WD-S06/08/09, ROR-S31, MB-S06/10 | WD P910별도undo1건; ROR07이탈리아이름과Spain/Leioa잔존; AcoustIDissue닫힘뒤replication문제. | 모든incominglink·원source·지문전수복원. 원changedrecord전체dump/소비자diff 필요. | 90칸존재확인; 자동실행성공으로채점안함. 실제소실과미열람구별. |
| Q5 | 소비자파일수정/운영자보고와실제사람오추천을 구별. | RESULT.md161행 Q5; citations.csv MB-C01,SW-D01/02,WD-C01,ROR-C01–04 | COMTES좁은회사lookup·EQAR역사기관유지 vs Rails최신목적변경·AcoustID전파. SW-D03은분리전저장링크수에서제외. | ROR최초인용/정정날짜4건; 날짜있는6체인은부족. 과거고정판+사후diff 필요. | 외부독립원문7은통과; dated6체인은미충족. 사람오추천18/18미확인. |
| Q6 | 이력은정정대상을찾는정보를더하나목적/키가없으면보류. | RESULT.md179행 Q6; reconstruction.csv54행; key/answer-key.json; frozen-manifest-v4.json | MB04①충분, MB03①잘못선택, ROR05③후계4보류, ROR07③SpanishID보류, SW01②좁은목적선택. | 실제추천문·완전정정키·인간/외부독립판독 없음. v1입력오류와v4부분재판독을보존. | 54조합/원답안/카드해시일치. source-exposed root 자기점검, 인과효과 주장없음. |
| Q7 | 인용역할·판·시점을옮기되분야경계를같은edge로합치지않음. | RESULT.md206행 Q7; alternatives.md13행 쌍A/28행 쌍B; SW-FS01–03,ROR-X01–03 | recording/release vs project/CLI/fork; 조직승계/본부지부 vs category/institution/building. 실제합병2016과catalog2026분리. | 법적승계고시·운영시간/비용·전체발생률 미측정. 구체업무/판요구에대한후속표본 필요. | 실제2쌍·네관점·비용관측단위 확인. 최종DB결정없음. |

## 절차·정합 검사 결과

- `PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-023/scripts/validate_research.py`: **41개 정합 항목 통과**, exit0. 출처/사건/소비자 참조, 최소수,54행과 세표현, frozen view/answer 해시,48+6판독계보,6사건씩의비교파일,18개식별열/90개복원행,표순서/끝3행,로컬링크/소유범위를 확인했다. 이는 소프트웨어 설치·외부catalog 재현 시험이 아니다.
- 첫 실행의 소비자 boolean 검사에서 CSV의 `true`를 `True`와 비교한 검사기 형식 오류1건을 발견했다. 실제 데이터의7개 독립 소비자 값은 맞았으며, 대소문자 정상화 후 재실행해 통과했다. 이 오류를 연구 실패나 성공 수로 합산하지 않았다.
- `PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-023/manifest.json --fetch`: **exit0 / status passed / freshness remote_checked**, 2026-11-22T04:07:39Z. 시작base7f66165… 유지, 확인된최신integration2f3593a43f77f6023d0d176bcc0f21905883af45, outside_paths·unmerged_paths·errors는빈배열. 새integration을작업결과에임의merge하지않았다.
- 마지막 원문 재열람은Q1–Q7에걸친7개 핵심 원문에 수행했다. `evidence/final-source-recheck.json`에 MB-S17/12,WD-S08,MB-S23,ROR-S31,SW-S05,SW-FS03의정확한위치와Git blob/웹ref를 남겼다. 전체135 URL의항상가용성을검사했다는주장이아니다.
- 내부별도감사자는숫자·원문/보기누락·판독범위·보고서구조를읽기전용검토했다. 수정한입력결함과원문누락을`protocol-errata.md`에구별했다. 마지막검토에서추가실질오류를찾지못했다는결과는독립외부검증이아니다.

## 하지 않은 실행과 재개 입력

MusicBrainz `20261121-002203` edit dump는접근이막힌것이아니다. HEAD200/17,284,315,658바이트를확인했으나전체다운로드·해제·필요4개edit_data행추출은미실시다. [DUMP_FOLLOWUP.md](collectors/musicbrainz/DUMP_FOLLOWUP.md)에정확한입력과미실행명령을남겼다. 따라서‘공개화면에source가없다’를‘원시기록이삭제됐다’로채점하지않았다.

ROR는공식changedJSON과배포댓글을읽었으며해당전체release dump/liveAPI와전수대조하지않았다. brew설치·과거keg재현·AgentScript build·음원비교·전체AcoustIDreplica검사는실행하지않았다. 이실행을요구하는주장은확정하지않고HANDOFF에최소입력과명령/우선순위를명시한다.

## 인계 전 결론

수용 근거는 `evidence/acceptance-evidence.json`의 배열이다. 거짓인 조건은 이유와 첫 보강 입력을 함께 둔다. 이 SELF_CHECK와 수용 근거를 포함한 검사 커밋을 GitHub에서 확인한 **뒤에만** HANDOFF.md를 작성한다. 마지막 HANDOFF는 단독 커밋으로 저장하며 그 부모 커밋을 결과·검사 고정판으로 안내한다. 공통계약·dot-control·색인 변경은 진행담당에게 제안만 넘긴다.
