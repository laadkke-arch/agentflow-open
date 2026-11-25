| 판단 묶음·사용자 목적 | 좁은 주장·원근거 주소/위치 | 필요한 다른 묶음 | 대안·충돌·폐기 조건 | 보류할 주장 |
| --- | --- | --- | --- | --- |
| A·230 / 개발자: 독립 트랙 출력 | #5302 같은 원작성자의 재시험 진술 [A01](https://github.com/audacity/audacity/issues/5302#issuecomment-1746468973), comment1746468973; [A02](https://github.com/audacity/audacity/pull/5305) DoExport diff/merge selectedOnly | 없음; A01 보고, A02 patch는 내부 분리 | Tracks vs Labels; actor 불일치면 report 철회, diff 불일치면 patch만 재개 | 실제 PCM·정확 build·독립 실행·전체 성공 |
| B·233 / 편집자: 저작·역할 구별 | [B03](https://catalogue.bnf.fr/ark:/12148/cb38665336s) W02 fils; [B04](https://catalogue.bnf.fr/ark:/12148/cb35752325z) W03 père; B01/B02 별도 ARK, [B05](https://catalogue.bnf.fr/ark:/12148/cb45830647g) W01 한 서지 둘 | 없음; B01–04 role+identity | name index vs authority+role+edition; 한 역할 정정은 해당 edge만 재개 | 모든 판 저작 귀속·표제면 검증·기관간 동일성 |
| C·234 / 설계자: 학교 그림 asset | [C01](https://github.com/maplibre/demotiles/blob/601ae60796ceceda2cbd2ed3d2ea92d17a84be4b/styles/osm-bright-gl-style/style.json) poi-level-3 index92, C04 tile id40551996 Point rank32 class school level 없음 → [C02](https://github.com/maplibre/demotiles/blob/601ae60796ceceda2cbd2ed3d2ea92d17a84be4b/styles/osm-bright-gl-style/sprite.json) school_11 85,123,17,17 DPR1; C05 PNG334×157 | 없음; C01–05 내부 조건 | 정적 lookup vs 렌더; digest/filter/feature 바뀌면 해당 연결 재개; C06 별 World contrast | 실제 로드·카메라·충돌·DPR·가시성/픽셀·사용 |
| D·235 / 편집자: 옛 인용/새 상태 | [D01](https://www.w3.org/TR/2018/REC-WCAG21-20180605/#parsing) 2.1 2018 원문, [D02](https://www.w3.org/TR/2025/REC-WCAG21-20250506/#parsing) 2025 note, [D03](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#parsing) 2.2 removed; 각각 4.1.1 | 없음; D01/02/03 판 비교 | 역사+현행 병렬 vs latest-only; 적용판 변경 시 current만 재개 | 모든 파싱 오류 무해·법적 적용판·도구 실행 |
| E·236 / 개발자: 링크 읽음과 선택 | #8793 [E01](https://github.com/godotengine/godot-proposals/issues/8793#issuecomment-1877111832) comment1877111832 같은 원작성자 읽음·불명확 진술, recommendation1877072086, continued1877143602; E02 fixed docs L29–49 | 없음; E01 thread, E02 설명 | 링크 vs 재설명; actor/발언 수정 시 읽음 판단 재개; 산출물 발견 시 사용 별 갱신 | 클릭 기록·실제 선택/대체/실행·추천 당시 stable bytes |
| F·237 / 설계자: author vs total labor | [F01](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv) dev655 issue1 232/10, issue2 36/0분; [F02](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/README.md) Data Spec 두 시간은 같은 작성자 | 없음; F01+F02 필요 | author-time만 vs reviewer/acceptance join; actor/field 재정의 시 재개 | 0 reviewer 시간·총노동·인수·대표성·AI 효과 |

표 1 단위: 지명 판단 묶음 한 행, 예정 6/관측 원자료 연결 6/결측 0(좁은 주장만; 더 강한 주장의 증거는 별도 결측). C06 W-I는 별도 대조이며 234 원모집 분모에 합치지 않는다. 모든 선행 중앙 DONE/자체 PARTIAL을 유지한다.

| 조합안·제외한 묶음 | 유지할 결정·출처 | 다시 열 결정 | 최소 복구 원문 | 추가 열람·미확인 |
| --- | --- | --- | --- | --- |
| L −A | B(B01–B05), C(C01–C05), D(D01–D03), E(E01/E02), F(F01/F02) | 개별 트랙 경로·재시험 주장; 교차 일반화도 재개 | [A 첫 원문](https://github.com/audacity/audacity/issues/5302#issuecomment-1746468973) | 0 추가 계획; X에서 PR 추가; PCM 미확인 |
| L −B | A(A01/A02), C(C01–C05), D(D01–D03), E(E01/E02), F(F01/F02) | Dumas 역할/authority 연결; 교차 일반화도 재개 | [B 첫 원문](https://catalogue.bnf.fr/ark:/12148/cb38665336s) | 1 추가 계획; B04; X B01/B02 추가; raw MARC 미확인 |
| L −C | A(A01/A02), B(B01–B05), D(D01–D03), E(E01/E02), F(F01/F02) | 정적 학교 자산 연결; 교차 일반화도 재개 | [C 첫 원문](https://github.com/maplibre/demotiles/blob/601ae60796ceceda2cbd2ed3d2ea92d17a84be4b/styles/osm-bright-gl-style/style.json) | 1 추가 계획; L 조건부 key까지만; X C02–05; 실제 렌더 미확인 |
| L −D | A(A01/A02), B(B01–B05), C(C01–C05), E(E01/E02), F(F01/F02) | 인용/적용판 분리; 교차 일반화도 재개 | [D 첫 원문](https://www.w3.org/TR/2018/REC-WCAG21-20180605/#parsing) | 2 추가 계획; D02/D03 추가; 적용판/도구 미확인 |
| L −E | A(A01/A02), B(B01–B05), C(C01–C05), D(D01–D03), F(F01/F02) | 읽음/선택/실사용 분리; 교차 일반화도 재개 | [E 첫 원문](https://github.com/godotengine/godot-proposals/issues/8793#issuecomment-1877111832) | 0 추가 계획; 같은 thread; X E02 추가; 역사 bytes/산출물 미확인 |
| L −F | A(A01/A02), B(B01–B05), C(C01–C05), D(D01–D03), E(E01/E02) | 작성자 두 시간/총노동 분리; 교차 일반화도 재개 | [F 첫 원문](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/README.md) | 1 추가 계획; F01 추가; reviewer/acceptance 없음 |
| X −A | B(B01–B05), C(C01–C05), D(D01–D03), E(E01/E02), F(F01/F02) | 개별 트랙 경로·재시험 주장; 교차 일반화도 재개 | [A 첫 원문](https://github.com/audacity/audacity/issues/5302#issuecomment-1746468973) | 1 추가 계획; X에서 PR 추가; PCM 미확인 |
| X −B | A(A01/A02), C(C01–C05), D(D01–D03), E(E01/E02), F(F01/F02) | Dumas 역할/authority 연결; 교차 일반화도 재개 | [B 첫 원문](https://catalogue.bnf.fr/ark:/12148/cb38665336s) | 3 추가 계획; B04; X B01/B02 추가; raw MARC 미확인 |
| X −C | A(A01/A02), B(B01–B05), D(D01–D03), E(E01/E02), F(F01/F02) | 정적 학교 자산 연결; 교차 일반화도 재개 | [C 첫 원문](https://github.com/maplibre/demotiles/blob/601ae60796ceceda2cbd2ed3d2ea92d17a84be4b/styles/osm-bright-gl-style/style.json) | 4 추가 계획; L 조건부 key까지만; X C02–05; 실제 렌더 미확인 |
| X −D | A(A01/A02), B(B01–B05), C(C01–C05), E(E01/E02), F(F01/F02) | 인용/적용판 분리; 교차 일반화도 재개 | [D 첫 원문](https://www.w3.org/TR/2018/REC-WCAG21-20180605/#parsing) | 2 추가 계획; D02/D03 추가; 적용판/도구 미확인 |
| X −E | A(A01/A02), B(B01–B05), C(C01–C05), D(D01–D03), F(F01/F02) | 읽음/선택/실사용 분리; 교차 일반화도 재개 | [E 첫 원문](https://github.com/godotengine/godot-proposals/issues/8793#issuecomment-1877111832) | 1 추가 계획; 같은 thread; X E02 추가; 역사 bytes/산출물 미확인 |
| X −F | A(A01/A02), B(B01–B05), C(C01–C05), D(D01–D03), E(E01/E02) | 작성자 두 시간/총노동 분리; 교차 일반화도 재개 | [F 첫 원문](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/README.md) | 1 추가 계획; F01 추가; reviewer/acceptance 없음 |

표 2 단위: 조합안 하나에서 카드 하나를 제거한 사고실험 한 행, 예정 2×6=12, 작성·검토 12, 실제 사용자/모델 실행 0(범위 밖). 유지 출처 ID는 sources.jsonl의 외부 원문으로 연결되며 제거 대상의 숨겨진 주장에 의존하지 않는다. L/X 복구는 범위별로 다르다. L은 A-report, B-role, C-conditional key까지; X는 patch, authority, 특정 feature/atlas까지. 1차 원문에 같은 issue의 여러 댓글은 포함한다. 표의 추가 열람 수는 계획치이며 실제 독자 비용이 아니다.

# AF-RES-250 판단과 조사 근거

## Q1. 질문·대상·판·동사·직접 증거

A–F 카드가 질문·대상·입력판·관찰 동사·보류 문장을 독립적으로 보존한다([packets.md](packets.md)). 외부 원자료 연결: A01 issue body+comment, A02 DoExport 소스 diff (I230-3 followup 두 행); B01–05 BnF authority/bib 역할 (I233-3 W01–W05); C01–05 고정 layer/tile/sprite (I234-3 R05–R08); D01–03 4.1.1 history/notes/removed (I235-3 T03/T14/T15); E01 reply 및 E02 docs (I236-3 M2); F01/F02 CSV+Data Spec (I237-3 stages). 발행자/기관 기록, static artifact, 사후 actor report, machine data를 구분한다. 특히 A02의 merge와 A01의 retest가 같은 사건 맥락이어도 exact tested build는 미확인. E의 read report와 recommendation 사이 순서는 있으나 선택의 인과는 없다. F issue1 author pair 232+10=242분만 계산할 수 있고 총노동 아님. 
반례 B05의 한 서지 두 Dumas, C06의 같은 프로젝트 다른 style, D의 텍스트 잔존/현행 상태 변화, E의 읽었지만 이해가 어렵다는 회신, F issue2 post 0 vs reviewer unknown. 모두 원문에서 직접 확인(상세 [COUNTEREXAMPLES.md](COUNTEREXAMPLES.md)).

## Q2. 목격/원천 계보

[S01 PROV Primer](https://www.w3.org/TR/prov-primer/) §3.1–3.6, [S02 PROV-DM](https://www.w3.org/TR/prov-dm/) §5.2.1–2에서 entity, activity, agent, derivation/revision/quotation을 다르게 취급한다. 여기서는 간단한 경량 관계만 차용(표준 전체 도입을 결정하지 않음).

| 실제 예 | 관계의 최소 표기 | 독립 증거로 더할 수 있는가 |
|---|---|---|
| I230-3 retest 행과 A01 동일 comment | report derived from original utterance, original actor | 아니오. 내부 요약은 같은 목격의 재전달 |
| A01 issue/author reply와 A02 PR | issue entity, utterance activity, code change activity; linked issue | 별도 source work/행위지만 동일 사건 계보; code diff ≠ test result |
| B05 한 서지의 두 Dumas link | one bibliographic entity, two role claims, same provider | 역할은 둘, 동일 서지/목격을 두 독립 사건으로 세지 않음 |
| C01 style과 C02 index/C04 PBF/C05 PNG | 여러 entity와 static lookup activity, producer; actual render 활동 없음 | 파일은 별 원산출물, lineage는 하나의 asset chain |
| D01/D02 | 동일 WCAG2.1 work, 두 판 entity; revision | 판은 각각 보존하되 work 하한 중복 제외 |
| E01 추천자 comment와 원작성자의 뒤 reply | agent, reply activity, link target; self-report, no artifact | 서로 다른 발화, 같은 issue 사건; 추천자와 사용자 혼동 금지 |
| F01 rows / F02 Data Spec | machine output entity + methodology; field/row→actor | 같은 연구 계보; row별 data, 별 연구가 아님 |
| H05 PLOS와 H06 PMC | 동일 DOI 재게재 | source_id는 별도, work 하나 |

동일 주석을 복사한 인계 카드가 추가 목격을 제공하는 것으로 보지 않는다. 별도 actor의 회신도 관측된 행위/발언에만 범위 한정. 여섯 사례 간 공유 직접 원자료를 찾지 못했다. 공통 분석 표준 S01–04는 경험 사건의 공동 원천이 아니다. [H01](https://training.cochrane.org/handbook/current/chapter-04) §4.6.2의 report vs study 구분과도 일치.

## Q3. 필요·보완·충돌·독립 15쌍

[relations.csv](relations.csv)에서 전 15 무순서 쌍과 양방향 삭제 영향 기록. 직접 필요 0, 보완 10, 독립 5, 관측된 논리적 충돌 0. 예 A–E는 보완: 같은 actor 내 발언 수준 비교에 도움, 서로 다른 사례라 E 읽음으로 A 실행 또는 A 재시험으로 E 사용을 증명할 수 없음. C–D는 source version의 필요성을 보완하나 D 규격 갱신으로 C style 변경 여부를 추론할 수 없음. B–D는 authority entity와 version state를 구분하는 데 보완; B–F는 독립. 원천 공유가 있는 경우라도 주장별 최소 근거를 별도 유지한다: B05에서 한 역할만 정정되면 해당 role edge만 철회; D02 current applicability가 바뀌더라도 역사 D01을 보존. 
삭제 규칙: 제거 카드에 연결된 decision만 재개, 나머지 다섯 좁은 결정 유지; 두 카드의 일반화 가설은 재개하거나 폐기. 충돌 0은 scoped observation이며 충돌 전무라는 외삽 금지. "모든 충돌 해결"의 보증 아님.

## Q4. 위치/판/상태를 고정하는 최소 경로

[S03 Web Annotation](https://www.w3.org/TR/annotation-model/) §4.2.4–4.2.5 Example23, L943–993: exact/prefix/suffix와 position selector는 보완적이며 텍스트 이동/동적 포함에 취약하여 State와 함께 쓰는 것이 좋다. [S04 DCAT3](https://www.w3.org/TR/vocab-dcat-3/) previousVersion/Example34: 대체와 이전 판 관계는 구별. 구현 권고는 source ID + fixed URL/SHA or edition + local selector + observed UTC window + actor/evidence kind + missing state; floating URL은 사용자가 보았던 정확 판을 보장하지 않음.

| 카드 | 주소/선택자 | 별도 상태 |
|---|---|---|
| A | issue+comment ID/actor/time, PR merge sha+diff function/line | 발화와 병합은 관측; artifact/build 미확인 |
| B | ARK/edition+Auteur(s) 및 Autre(s) auteur(s) | 기관 주장; physical title page/raw MARC 미확인 |
| C | commit SHA+file path/layer index+ID/JSON key, tile z/x/y+feature id, sprite rect+DPR+blob | static JS wire parse & PNG header observed; actual render 미확인 |
| D | 날짜 포함 REC URL+#parsing, 4.1.1 note/status | history retained vs current applicability; tool run 미확인 |
| E | original/recommendation/reply IDs, same actor; pinned docs heading | comment times inherited, direct actor/body; historical floating bytes 미확인 |
| F | fixed CSV blob+dev_id/issue_id+column+minute, README Data Spec | author time observed, reviewer/acceptance join missing |

중앙 DONE은 발행자 주장의 성공/실제 사용/실행 관측이 아니다. 6 선행 자체 PARTIAL. I234-4 고정 layers.csv W-I 19 vs header20: [C06 원문](https://github.com/maplibre/demotiles/blob/601ae60796ceceda2cbd2ed3d2ea92d17a84be4b/style.json) 8 layers, no icon-image, no sprite. 정정 20열 row와 공석/적용 대상 밖 구별은 COUNTEREXAMPLES.md. C04 binary 직접 회수 및 최소 wire parse 1867 poi features/target properties 확인. C05 PNG header width/height로 rect bounds 확인. 비ASCII 이름 decode 오류는 제외, 픽셀/CRC/런타임 보류.

## Q5. 실제 결정 기록의 대안·철회·판 분리

[P12 PEP 1](https://peps.python.org/pep-0001/) status/resolution, [P13 Rust template](https://github.com/rust-lang/rfcs/blob/main/0000-template.md) Drawbacks/Rationale/Unresolved, P14 MADR quickstart는 양식 입구이며 실제 결정 하한에서 제외.

| 원결정·위치 | 채택/배제 및 이유 | 재고 조건 또는 이 작업 제안 |
|---|---|---|
| [P01 PEP572](https://peps.python.org/pep-0572/) Rejected alternative proposals L479–506 | :=, EXPR as NAME 대안은 다른 의미/범위 충돌, scope 변경은 호환성 문제로 철회 | 과거 이유 보존; 호환성 증거 바뀌면 재검토(제안) |
| [P02 PEP622](https://peps.python.org/pep-0622/) superseded; [P03 PEP634](https://peps.python.org/pep-0634/) Abstract; [P04 PEP635](https://peps.python.org/pep-0635/) Abstract | 622를 spec/rationale/tutorial로 분리, 이전 번호 추적 | 실제 supersession; spec vs rationale 단위 삭제 가능성은 따로 평가 |
| [P05 PEP703](https://peps.python.org/pep-0703/) Acceptance | 단계적 도입; 문제 크면 전체 rollback도 가능 | 원결정 자체가 재고 조건 명시. 최신 실행 상태는 별개 |
| [P06 RFC2005](https://rust-lang.github.io/rfcs/2005-match-ergonomics.html) Alternatives | reference inference 단독 대안, binding ergonomics 선택 이유, custom autoderef 후속 | 사용자 경험/호환성 다시 관찰(제안) |
| [P07 RFC2229](https://rust-lang.github.io/rfcs/2229-capture-disjoint-fields.html) Drawbacks/Alternatives | 전체 capture 직관 vs disjoint, preborrow workaround | 변경 후 의미/호환성 반례 발생 시 재개(제안) |
| [P08 RFC2497](https://rust-lang.github.io/rfcs/2497-if-let-chains.html) rationale/alternatives | && let 대 comma/if 및 미래 OR; 설문 373명(자체선택) | 설문 대표성·후속 구현 별도, 새 근거 시 재고(제안) |
| [P09 MADR0008](https://github.com/adr/madr/blob/develop/docs/decisions/0008-add-status-field.md) Outcome/Pros Cons | YAML front matter, parser 지원; badges/text/table/no status 비교 | 명시 rollback 없음; 소비자 parser 지원 바뀌면 재검토(제안) |
| [P10 MADR0009](https://github.com/adr/madr/blob/develop/docs/decisions/0009-support-links-between-adrs-inside-an-adrs.md) Outcome/Pros Cons | More Information links; 유연성 vs 파싱 부담; 표 링크 유효성 문제 | 자동 조립·선택 필요하면 typed relation 추가 검토(제안) |
| [P11 MADR0016](https://github.com/adr/madr/blob/develop/docs/decisions/0016-outcome-before-detailed-pros-cons.md) Outcome/Pros Cons | 결론 먼저, 상세 장단점 뒤; logical flow 역전 단점 | 독자가 반박/검토 목적이면 근거 함께 펼침(제안) |

실제 결정 원저작 10개(PEP622와 PEP634는 별 문서이나 한 결정 계보; PEP635 산입 제외); 독립 결정 계보 7(정확 lineage ID 기준 PEP pattern 1, Python572/703, Rust3, MADR 1). 별도 결정 문서와 독립 실험은 다른 분모. 실제 재고 조건이 없는 사례는 후대 제안을 원작성자의 조건으로 인용하지 않는다. L의 outcome+first link+reason은 P11, X의 판/대안/상충/재개 조건은 P01/P05/P10에 대응한다. 반례: 링크만 자유 서술하면 파싱 부담과 유효 링크 식별이 남는다(P10). YAML 하나로 판단의 역사·동사·scope를 대체하는 결론은 지원하지 않는다.

## Q6. 타 분야 종합·갱신

[H01 Cochrane Handbook ch4](https://training.cochrane.org/handbook/current/chapter-04) §4.6.2와 [H02 ch5](https://training.cochrane.org/handbook/current/chapter-05) §5.2.1/5.5.4: 복수 report를 같은 study에 연결, 데이터가 다른 경우 보존하고 우선 report 선택 이유 명시. 별도 추출 후 조정도 가능. Handbook은 두 절/장 하나의 work로 보수 집계. [H05 PRISMA 2020](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1003583) Box1/2: record/report/study, 제외 이유·프로토콜 변경·민감도 보고를 분리, 방법론 품질 도구 자체는 아님.
[H03 실제 review](https://pmc.ncbi.nlm.nih.gov/articles/PMC6464774/) Results L492–501: 20 publications→5 included studies; 2015년 추가 두 report를 이미 포함된 Newnham 1993에 연결. History L911–914 결론 유지. 별개 trials/하위집단은 독립 행이며 secondary outcome의 subgroup 결합하지 않음(L859–866,1546). [H04 다른 review](https://pmc.ncbi.nlm.nih.gov/articles/PMC8941847/) What's new/History L429–444: 형식 변환과 2007-09-24 결론 변경 substantive amendment 구별. 정확히 어떤 이전 수치가 바뀌었는지는 미확인. 이 둘은 report 수와 판단 변화가 1:1이 아님을 보여 준다. 개발에 전이할 때 원보고서, 관측 사건, 주장, 변경 이유를 따로 남기되 의학적 연구 결과를 개발 제품 효과의 증거로 쓰지 않는다.

## Q7. 누구에게 어떤 조합이 필요한가

[assemblies.md](assemblies.md) 실제 입력 예, [removals.csv](removals.csv) 12행. L: 첫 링크/짧은 목적·동사·보류 이유·철회 조건으로 되돌릴 수 있는 개발 판단을 돕는다. X: 판/원자료 selector/actor/lineage/type/unknown/dependency를 조건부로 펼쳐 대체 설계나 편집자의 반박을 돕는다. X가 항상 유리하지 않음: 문서량과 반박에 필요한 비용, 유효 관계 유지 비용이 더 크다. 반대로 L만으로 C의 특정 feature 증명이나 B의 기관 identity, A의 patch까지 확장하면 근거 부족. 
12행에서 남은 5개의 local decision을 추적하는 링크가 있고 제거된 decision은 복구 index의 첫 원문부터 다시 열도록 기록했다. L의 추가 열람 5, X 12(각각 최초 6 별도, 재열람 포함); X에서 C 복구 +4가 가장 많음. 실제 성능은 측정하지 않았다. 미확인에 직접 결론을 만들어 붙이지 않는다. 좁은 주장에 강한 문장 제거 조건을 명시하고, 제거한 주장 이외의 source URL·보류 이유는 유지한다.

## 비용·대안·추가 분석

- 공통 6장의 자료 접근 index를 보존하는 비용, 변경 시 locator 재확인 비용은 미계측. L은 첫 링크 안내와 저비용 판단, X는 근거 교체/판 충돌/행위자/고비용 결정에 적합. 검토자는 X에서 모든 필요한 raw input과 주장 단위 교체 가능성 확인. 최종 schema 도입이나 독립 성능 평가는 미확인.
- 원장 71 records: counted 37 고유 원저작/원산출물(사례19, 결정10, 표준4, 종합4) 및 23 source lineage IDs. 원저작 수는 산출물 수: PBF/PNG/JSON은 distinct publisher artifacts지만 같은 asset lineage, PEP622/634는 같은 decision lineage, PROV Primer/DM 두 표준 원문 같은 lineage. Handbook 두 장은 1 work, PEP635 같은 설명 계보로 하한 미산입, PRISMA PMC duplicate 제외. 보수적으로 PEP622/634 중 하나와 PROV Primer를 제외하더라도 총35, 단 표준 4개 원문 요구는 각 독립 W3C 문서 기준 충족. 19 case works에서 6 사례별 최소 1 충족; 6 지명 사례는 서로 다른 관측 단위이지 6 독립 재현 실험이 아님. 재실험 0, 모델 실험 0(범위 밖). 
- 먼저 원장 기반 claim-level retrieval과 deletion tests를 수행하고, 렌더/PCM/실제 노동 데이터는 별도 실측 작업에 인계한다. 238–242 사용하지 않음. 이전 AF-RES-020 숫자는 brief의 문제 동기, 이번 독립 관측으로 재산정하지 않음.

| 중요한 불일치 또는 약점 | 영향을 받는 판단 | 다음에 볼 구체적 원자료·검사 | 판정이 바뀌는 관측 |
| --- | --- | --- | --- |
| 정적 연결/실행 자기보고가 실제 사용·성공 산출물과 다름; W-I 원표 19/20 열 정정 | A·C·E의 성공/사용·render; static과 report 좁은 주장 유지 | A01 exact test build+PCM receipt 및 A02 merge; C01–05 fixed tile/sprite/viewport/DPR render receipt; E01 같은 actor 후속 artifact | 정확한 actor/build/asset digest+observed artifact/actual pixels/usage receipt 확보 또는 기존 input 반증 |
| 기관 역할 및 과거 인용과 현행 판을 동일성으로 묶기 어려움 | B·D identity/version/current applicability | B01–05 raw MARC/표제면; W3C D01–03 및 적용판·tool tag/output | authority role correction, 새 판/errata, 적용 범위 또는 tool receipt가 명시 |
| 작성자 time pair의 0/결측과 reviewer/acceptance 증거 없음; 두 조합은 사고실험 | F 총노동/인수 및 L/X의 실제 비용·효과 | F01/F02의 row key에 join 가능한 reviewer logs, acceptance events; 독립 설계자 blinded deletion comparison | 독립 reviewer/acceptance key 및 time unit·대상 일치; 실제 L/X 독립 사용 결과가 예상 추적성과 다름 |
