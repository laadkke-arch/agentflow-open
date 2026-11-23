# AF-RES-077 자기검산 — PARTIAL

## 검토 주체와 범위

원 연구는 root와 같은 모델 계열의 모집·판독·사후 조사 문맥을 사용했다. 재개 root는 원격 `2f7e07542b4a59839556e00c9e266179150b21a3`의 커밋된 파일을 읽고 결과를 작성했다. 재개 Shotcut/MuseScore/Sigil 검토자 3명은 원 A/B 판독자가 아니지만 **사후 source 검토자**이며 새 blind reader·독립 인간 표본으로 세지 않는다. 최종 결과 작성·기계 검사·통합 판정은 root가 맡았다. 검토자의 원문 재열람과 자기 재판독을 독립 효과 표본으로 바꾸지 않는다.

읽기 전용 [verify.py](evidence/verify.py)는 파일 구조·봉인 bytes·해시·원장 조인·계수·허용 경로를 검사한다. source assertion의 의미, native 실행 성공, 연구 인과효과를 보증하지 않는다. 원 요구·연구자 조건·실제 채택은 아래 질문별로 분리한다. 최종 실행 명령·SHA·시각·종료값은 [acceptance-evidence.json](evidence/acceptance-evidence.json)과 마지막 HANDOFF에 실제 측정값으로 기록한다.

## Q1. 원 작성자의 목적·두 조건·최초판·판 대응

| 질문 | 주장 또는 미확인 | 원문 URL·판·절 또는 실행 행 | 확인한 내용 | 적용 한계 | 찾아본 반례와 결과 | 답을 바꿀 최소 후속 확인 |
| --- | --- | --- | --- | --- | --- | --- |
| Q1-SC | 동명 대체 후 timeline black은 작성자 요구. 이동·동명 타 폴더 오연결은 연구 조건. | [#910](https://github.com/mltframework/shotcut/issues/910), `SC-REQ-910`; v20.09.13/0898bdf3…; FRAME SC 순위 4. | 현재 body와 댓글 11개, tag/소스 blob 재확인. 마지막 작성자 보고도 black. | 최초 body revision·실제 binary·원본 이동 요구 미확인. | issue close를 해결로 읽는 반례를 마지막 댓글에서 확인, 성공 해석 기각. | 최초 body/실제 project·media와 numeric binary가 결합된 적격 요청. |
| Q1-MS | source selected flag가 parts로 복제되는 문제. 원 tracker 일부 캐시 확보. | [PR4590](https://github.com/musescore/MuseScore/pull/4590), [tracker281441](https://musescore.org/en/node/281441); `resume-review-musescore.json`. | ericfontainejazz·2019-01-08 표시·Reported version 3.0 및 2.3.2 보고, part 생성 순서. | 캐시 일부; 후속/root 요청 403, 최초판·전체 이력·표시 시각의 시간대 미확인. v3.0.1은 원 신고 이후. | undo/reopen·P2 보존을 원 신고 요구로 만들 수 없음. 주 표본 공석 유지. | 최초 tracker revision 및 3.0/2.3.2와 v3.0.1의 affected-path 동등성. |
| Q1-SG | split 뒤 footnote 대상 보존은 요구. N/E의 사이 분할·동명 두 장·nested move는 확장. | [#450](https://github.com/Sigil-Ebook/Sigil/issues/450), [댓글520258201](https://github.com/Sigil-Ebook/Sigil/issues/450#issuecomment-520258201), 0.9.17/30419827…. | 실제 설명은 ref와 target이 함께 새 장으로 이동하는 경우. | newest version만으로 numeric installed build 확정 못함. | 원 공개 EPUB marker가 둘 앞에 있어 봉인 N/E와 다름. 귀속 E2 정정. | 최초 body와 영향 build, 올바른 원 ref target을 담은 native fixture. |

모집 30행의 순번·중복·쿼리 소속은 검사기에서 확인한다. 목적/행동/판을 모두 만족하는 주 표본 0/3을 유지한다. 현재 body의 created_at을 최초 요구문 날짜로 대신하지 않는다.

## Q2. 동종 자료의 기본 선택·쓰기 시점·실패 정책

| 질문 | 주장 또는 미확인 | 원문 URL·판·절 또는 실행 행 | 확인한 내용 | 적용 한계 | 찾아본 반례와 결과 | 답을 바꿀 최소 후속 확인 |
| --- | --- | --- | --- | --- | --- | --- |
| Q2-SC | A1 full provenance/확인 전 거부 선택. 원문이 digest를 처방한 것은 아님. | [Kdenlive Proxy Settings](https://docs.kdenlive.org/en/project_and_asset_management/project_settings/proxy_settings.html), [Camera Proxy](https://docs.kdenlive.org/en/tips_and_tricks/useful_info/using_camcorder_proxy_clips.html); packets/SC-A.json; readers/SC-A.json@7c1df93…. | 원본/편집 대체물 역할과 path/name 변환, A0/A1 두 안. | 2026년 판; full read·snapshot·publication 순서는 추론. | legacy에는 과거 full digest 없어 안전한 거부가 복구를 막음. | 동일 원문·native 입력으로 거부율/오연결/복구 완료를 구분한 실행. |
| Q2-MS | A-C1 local excerpt reset, A-C2 global copy reset 경쟁. | [Handbook3](https://musescore.org/en/print/book/export/html/278625), Parts와 Undo; readers/MS-A.json@7c1df93…. | 공유 musical data와 local presentation·save/undo를 참고한 제안. | live handbook은 2019년 판 동등성 미확인. | 실제 historical PR은 global 선택; local이 최선이라는 관측 없음. | 모든 copy consumer 계약과 local clone coverage를 가르는 원시험. |
| Q2-SG | A-C1 original document+fragment 계획표, C0 그대로 / C2 journal 경쟁. | [EPUB3.3 2023년 판](https://www.w3.org/TR/2023/REC-epub-33-20230525/#sec-container-iri), XHTML 절; readers/SG-A.json. | 원 base/fragment 해석과 target scope를 선택에 사용. | 원문은 split transaction·inverse 저장 프로토콜 아님. | 동종 자료가 이미 B와 같은 핵심 답을 줌. | source-only 통제와 실제 URI·save/reopen 결과. |

## Q3. 공여 원전의 대상·조작·불변조건·예외

| 질문 | 주장 또는 미확인 | 원문 URL·판·절 또는 실행 행 | 확인한 내용 | 적용 한계 | 찾아본 반례와 결과 | 답을 바꿀 최소 후속 확인 |
| --- | --- | --- | --- | --- | --- | --- |
| Q3-SC | shared input과 edit metadata/history 구분만 대응 가능. | [darktable sidecar 고정판](https://github.com/darktable-org/dtdocs/blob/9d2c663bbe2a3390fd3750fdce780025933a5045/content/overview/sidecar-files/sidecar.md), 같은 SHA duplicate-manager.md; ROOT-DARKTABLE*. | sidecar/database와 복수 편집본 관계. | full digest·snapshot·producer transaction을 원문에 귀속하지 않음. | 외부 원본 overwrite로 shared immutable input 전제가 사라짐. | 과거 bytes/provenance를 실제 보존한 복구 흐름. |
| Q3-MS | witness identity/위치별 scope만 제한적으로 대응. inverse 도출 기각. | [TEI4.8.0 TCAPLR](https://tei-c.org/Vault/P5/4.8.0/doc/tei-p5-doc/en/html/TC.html#TCAPLR), [TCAPWL](https://tei-c.org/Vault/P5/4.8.0/doc/tei-p5-doc/en/html/TC.html#TCAPWL). | reading/witness와 유효 집합, §13.1.4.3 The Witness List. | live 4.12.0과 archive 4.8.0 구분. 명령 순서·이전 값 없음. | MS-X history 없이 옛 pitch 복구 불가. | 실제 command log/previous snapshot이 제공되는 별도 입력. |
| Q3-SG | content digest·물리 path·버전 logical path 구분. | [OCFL1.1 Manifest](https://ocfl.io/1.1/spec/#manifest), [Version](https://ocfl.io/1.1/spec/#version). | 원전의 manifest/state와 object-at-rest 범위. | fragment semantic identity와 atomic save 보장 없음. | 같은 파일 duplicate ID, checksum-valid 잘못된 href. | actual target identity/occurrence와 중단 복구를 검증한 저장 절차. |

## Q4. 코드의 식별자·저장 단위·복구 절차 변경

| 질문 | 주장 또는 미확인 | 원문 URL·판·절 또는 실행 행 | 확인한 내용 | 적용 한계 | 찾아본 반례와 결과 | 답을 바꿀 최소 후속 확인 |
| --- | --- | --- | --- | --- | --- | --- |
| Q4-SC | A1/B-F metadata 외에 완료 시 hash fan-out 경로가 추가 검토 대상. | [postjobaction.cpp](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/jobs/postjobaction.cpp), [mainwindow.cpp](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/mainwindow.cpp), SC-R1. | doAction→replaceAllByHash→playlist/timeline 교체. | frozen p2는 다른 hash. 실제 범위 밖 변경을 관측한 것은 아님. | producer별 설명만으로 hash 기준 전파의 범위가 보존되지 않을 수 있음. | 같은 hash를 공유하는 producer/작업 완료 경합을 명시한 새 시험과 수정 diff. |
| Q4-MS | local deselect는 new destination flag만, global은 copy 계약 전체에 해당. | [Element](https://github.com/musescore/MuseScore/blob/06a66a2206fc5f3c2c33d7ee4123badf496bc4dd/libmscore/element.cpp), [Excerpt](https://github.com/musescore/MuseScore/blob/06a66a2206fc5f3c2c33d7ee4123badf496bc4dd/libmscore/excerpt.cpp). | flags와 Selection/link/track 저장이 구분됨. | local 방문 범위·실제 역연산/serialization 성공 미확인. | historical global patch와 local 선호 불일치. | clone 하위 객체 누락과 selected 보존이 필요한 copy 경로 조사. |
| Q4-SG | 임시 SplitLinkPlan과 duplicate 검사, SetText/SaveToDisk 경계. | [Book](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/BookManipulation/Book.cpp), [AnchorUpdates](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/SourceUpdates/AnchorUpdates.cpp), resume SG. | 새 resource 생성과 수정·저장이 별도. nested folder는 FolderKeeper/OPFModel까지 필요. | source-only plan은 crash atomicity/이동 capability를 생성하지 않음. | SG-E의 native 이동 불가. | 지원 조작을 고정한 새 입력 또는 명시적 capability 변경 후 정확한 수정/복구 범위. |

## Q5. 입력·두 예상·관찰 지점·오판 조건

| 질문 | 주장 또는 미확인 | 원문 URL·판·절 또는 실행 행 | 확인한 내용 | 적용 한계 | 찾아본 반례와 결과 | 답을 바꿀 최소 후속 확인 |
| --- | --- | --- | --- | --- | --- | --- |
| Q5-SC | row 제안/Accepted gate/repair/완료 publication/저장·재열기를 분리해야 함. | TESTS SC-N/E/X, `UnlinkedFilesDialog::lookInDir`, auxiliary SC-E/SC-X stdout. | first-match 예시와 sample 동일/full 상이를 관측. | Qt 목록 순서·GUI 수락·유효 영상·원본 의도 미관측. | 자동 오연결/복구 완료로 해석하는 비약 기각. | valid MLT와 native event trace, producer별 before/after. |
| Q5-MS | 생성 직후 selected와 list를 함께 보아야 함. | TESTS MS-N/E/X, `Element::curColor`, resume MS audit. | Note::mark/drop-target/printing도 색상에 영향. | checkpoint가 모호하며 reopen이 표시 차이를 없앨 수 있음. | local/global 예상은 동일하며 whole/scoped 차이 없음. | mark 등을 통제한 즉시 관찰, P2의 중간 독립 수정을 가진 새 case. |
| Q5-SG | 각 ref의 base+fragment→실제 text, source 중복 수 관찰. | TESTS SG-N/E/X; original XHTML 5개; RFC3986 §5.2. | E의 문서별 A/B와 X의 동일 문서 모호함을 보조 검사. | comment는 native hr이 아니며 E의 폴더 조작은 미지원. | 원 #450과 N/E의 분할 위치가 다름. | full EPUB/cursor/저장 archive/reopen의 단계별 관찰을 새 층에 기록. |

## Q6. 반례·대안·같은 답을 주는 동종 자료

| 질문 | 주장 또는 미확인 | 원문 URL·판·절 또는 실행 행 | 확인한 내용 | 적용 한계 | 찾아본 반례와 결과 | 답을 바꿀 최소 후속 확인 |
| --- | --- | --- | --- | --- | --- | --- |
| Q6-SC | identity/history와 bytes 복구를 분리. | [PROV-DM](https://www.w3.org/TR/2013/REC-prov-dm-20130430/#term-Derivation), [Memento](https://www.rfc-editor.org/rfc/rfc7089.html#section-1.1). | derivation/과거 representation 보존은 서로 다른 정보. | 대상 media 실행·archive 복원을 하지 않음. | 현재 digest가 없던 과거 값을 만들지 못함. | 실제 과거 bytes와 그 정체를 입증하는 기록. |
| Q6-MS | witness/scope는 명령 역연산이 아니며 공유의 다른 경로도 확인. | [Qt5Undo](https://doc.qt.io/archives/qt-5.15/qundo.html), [Blender3.6](https://docs.blender.org/manual/en/3.6/scene_layout/object/editing/duplicate_linked.html). | command stack과 mesh/transform/shared Action 예외. | MuseScore가 Qt Undo를 사용한다는 주장이 아니며 Blender 실행 없음. | local appearance 수정만으로 모든 독립성 보장 불가. | MuseScore 고정판의 실제 link·layout·history 경로별 시험. |
| Q6-SG | URL scope는 동종 규격에 있고 checksum은 semantic 참조 보장이 아님. | [RFC3986](https://www.rfc-editor.org/rfc/rfc3986.html#section-5.2), [BagIt](https://www.rfc-editor.org/rfc/rfc8493.html#section-3), [GitObjects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects), [XML](https://www.w3.org/TR/2008/REC-xml-20081126/#sec-attribute-types), [SQLite](https://www.sqlite.org/atomiccommit.html). | path/fragment·typed ID·content integrity·journal/flush의 별도 역할. | 환경별 crash/FS 동작 미시험, untyped ID 자동 검증으로 확대 금지. | SG-X의 동일 문서 중복과 SG 원 fixture의 missing member. | 의미 대상·storage fault를 분리한 native 실험. |

## Q7. 원시험·실제 파일·판독 가능한 출력

| 질문 | 주장 또는 미확인 | 원문 URL·판·절 또는 실행 행 | 확인한 내용 | 적용 한계 | 찾아본 반례와 결과 | 답을 바꿀 최소 후속 확인 |
| --- | --- | --- | --- | --- | --- | --- |
| Q7-SC | native 실행 0/3, 보조 predicate 2/3. | postseal/shotcut/REPORT.md; auxiliary/observed-run-20261123/receipt.json; 고정 util 코드. | sample MD5 변함없음/full SHA 변경; first candidate 조건; worker exit 0. | synthetic bytes는 비영상. native preview/p2/reopen 없음. | close된 issue도 최종 black 보고. | 정확한 20.09.13·MLT/Qt 환경과 valid media/프로젝트·event 출력. |
| Q7-MS | native 실행 0/3; source fixture·실제 global 병합 확인. | [merge16851045](https://github.com/musescore/MuseScore/commit/16851045c9e50eafb016c5cf4f2733f974e841bf); tst_parts/tst_links/readwriteundoreset와 postseal receipt. | patch 1 line/test 0, breath 원 입력/undo-reference bytes 일치 및 요소 수 관계. | 원시험 실행 영수증 없음. 빈 CI 목록≠과거 실패. | local 연구 선택과 global 실제 채택 불일치. | RUNBOOK 고정 빌드에서 tests+새 고정 case를 실행하고 stdout/exit/fixture hash 확보. |
| Q7-SG | native 실행 0/3, 보조 predicate 3/3; 실제 EPUB 정적 판독. | [ae60e3e6](https://github.com/Sigil-Ebook/Sigil/commit/ae60e3e63a2f9343b40d316f179b9dfbcb6d838b); postseal/sigil/originals/test_split2.epub·fixture-inspection.json. | 실제 marker/ref/target 위치 및 없는 archive 경로, 좁은 수정 patch. | import/post-import normalization/save/reopen 미관측; golden EPUB 없음. | 원 bytes 그대로의 ref 결손을 고쳐 원시험 성공으로 세지 않음. | 원 fixture를 그대로 보존하며 import 전/후/split/save/reopen 관찰. |

## Q8. 예산·노출·변화·채택·시간

| 질문 | 주장 또는 미확인 | 원문 URL·판·절 또는 실행 행 | 확인한 내용 | 적용 한계 | 찾아본 반례와 결과 | 답을 바꿀 최소 후속 확인 |
| --- | --- | --- | --- | --- | --- | --- |
| Q8-선택 | 핵심 선택 변화 0/3, 후보 집합 차이 2/3. | VIEWS 6행, readers 원본 6개, A 7c1df93…/B 7bc2d1f…, CASEBOOK. | 선택 ID와 기전 정규화·원문 기각 구분. | SC-X의 rebuild/decision 세부 정책은 다름. | 원전명이 다르면 새 구현으로 세는 오류 기각. | 미리 정한 기전/정책별 coding과 독립 판독. |
| Q8-시험 | 새 입력 0/9, 선택안의 핵심 안전 예측 상충 0/9. | packets의 common 3개@9518c3d…, TESTS 9행, candidate 예측 39개. | 모든 봉인 bytes/예측 조인·고정 input 유지. | source 추가 후 시험 발견 효과를 측정하는 설계가 아님. 관측 0. | MS의 whole/scoped와 local/global은 고정 입력으로 우열이 갈리지 않음. | 새 판별 입력을 결과 전에 봉인한 별도 실험. |
| Q8-비용 | 상한은 같고 실제 노출/노동 비용은 다름. | VIEWS/COSTS/EXPOSURE/RESUME_REGISTRY. | source A 3593/B 4912자; 과거 요청 222/224; 재개 50 read ops는 별도(find 10 포함). | per-call UTC 부분 결손, 내부 retry/전체 시간/token/billing 미측정. | HTTP request와 cached find를 합산하지 않음. | 동일한 실제 노출·전체 작업 계측과 지시문 bytes를 사전 고정. |
| Q8-인과 | 독립 효과 분모 0, 개발자 시간 절감 미측정. MS의 과거 global 채택은 별개. | exposure/readers/merged PR·검토 보고. | 같은 모델 계열·root 사전 노출·역할 지시 동일성 미확인. | 현대 공여 자료가 2019년 개발자에게 영향을 줬다는 주장 불가. | B의 선택이 역사적 채택과 다른 사례 보존. | 실제 개발자 사용과 시간/결정 이력의 전향적 관측. |

## 귀속·문서→실행 비약 검사

| 검사 항목 | 대조 결과 | 최종 처리 |
| --- | --- | --- |
| SC hash 입력에 파일 크기 추가 | 고정 소스는 size를 분기/seek에만 사용하며 MD5에 size bytes 미포함. | E1 유지. 1MiB fixture와 1,000,000 byte sampling 구별. |
| SG-C1을 requester-supported로 전부 귀속 | target 보존은 지지, 봉인된 사이 분할은 연구자 확장. | E2 유지, RESULT/Q1에서 명시. |
| MS pin을 원 요구 이전판으로 표현 | 원 tracker Jan 8, PR Jan 16; pin은 원 신고 이후. | E5 정정. 봉인 원문 보존. |
| TEI Witness Information 절명 | #TCAPWL은 The Witness List. | E7과 재개 source 정정 행. |
| A/B 선택 동일→모든 세부 정책 동일 | SC-X의 rebuild 필요/명시적 결정 대기 차이. | 정규화한 핵심 기전 0/3으로 한정. |
| source/fixture 읽음→native pass | target 실행 0, source assertion/expected file/local probe는 별도. | TESTS의 서로 다른 열 유지. |
| actual adoption→우리 자료의 효과 | MS의 2019년 global 채택, 제공 TEI 2024·판독 2026. | historical fact만 보고. |
| source 계보 수→전체 기준 충족 | conservative 21이나 target contemporary 3/6. | PARTIAL 유지. |

## 해시·조인·누락·비용 검산

검산기는 모집판/packet판/A/B 출력 봉인 SHA의 원 bytes와 현재 파일을 비교한다. `BRIEFS.jsonl`의 역사적으로 잘못된 귀속은 수정하지 않고 ERRATA로 분리한다. FRAME은 원 모집 후 작성된 파생 원장으로, 924a030…의 bytes와 조회 순서·rank membership을 함께 대조한다. 원문 등록 358행은 기존 302+재개 56이며, 이 중 재개 50개는 외부 read 연산이고 6개는 보존된 원시험·fixture의 로컬 재판독이다. 후자는 새 외부 요청도 새 원저작도 아니다.

source ID 유일성, required fields, `independent_work_id`와 `conservative_lineage_id`, eligible 계보 24/21, view의 work/sections/char count/sha, reader의 common packet, TESTS의 input/선택안/실행 분모를 기계 검사한다. 고정 대상별 code/manual을 일관되게 합친 계수이고, failed read/metadata/같은 판/번역을 독립 원저작으로 추가하지 않는다. full text cache가 제거된 원문의 raw hash는 영수증에만 남아 있어 현재 원문 bytes 재계산 범위에서 제외한다. preserved source·packet·fixture·보조 출력의 해시는 실제 파일과 대조한다.

비용에서는 POST-SC8을 root POST-SC와 중복 합산하지 않고, MS 58의 54+4 하위 분해·SG failed subset·시간 보고를 다시 더하지 않는다. 재개 SC 15/MS 16/SG 17/root 2는 50 read operations로 별도 집계하며 web find 10을 HTTP 요청 증가분에 넣지 않는다. 초기 222/224 하한과 재개 50을 274 requests로 표현하지 않는다. 전체 비용 UNKNOWN과 사전 원문 A/B의 실제 길이 차이를 유지한다.

## 필수 산출물·분모와 수용 판정

| 필수 항목 | 실제 범위 | 수용 판단 |
| --- | --- | --- |
| SOURCES / FRAME / BRIEFS | 358 source 행/30 모집 행/3 보조 brief | 형식·계보·조회 기록 수용. 주 모집 0/3·최초판 0/3 미달. |
| VIEWS / CASEBOOK | 보기 6개/후보 13개/실제 노출·원리·쓰기·실패 부담 | 기술 대조 수용. 인과효과 미식별. |
| TESTS | 입력 9개/선택 예측 18개/전체 예측 39개 | 명세와 한계 수용. 목표 실행 0/9·원 실행 영수증 0/9; 목표 통과·실패는 미확인. |
| COSTS | 30행; 과거 요청 222/224+별도 재개 50개 연산 | 부분 비용 수용. 전체 시간·토큰·과금 미측정. |
| 독립 원문 최소 20 | named 24/conservative 21 | 전체 수 충족. 당시판 대상 자료 3/6층은 미달. |
| 반례/최종 약점 | named counterexample works 9개; RESULT 끝의 약점 3개 | 단순 유사성→역연산/원자성 비약 기각. |
| 범위·중간 커밋·원격 재열람 | 기존 7개 묶음+재개 결과/검사·인계 묶음 | 실제 SHA/종료값은 acceptance와 HANDOFF에 기록. 중앙 진행표 무수정. |

**판정은 PARTIAL이다.** 파일 완성과 기계 검사 통과를 적격 요구·native 성공으로 바꾸지 않는다. 결과판에서 충족 범위와 결손을 동시에 인계한다.

## 실제 검사 명령과 재현 한계

저장소 루트에서 실행하는 읽기 전용 검사:

```sh
python -B docs/workstreams/research/AF-RES-077/evidence/verify.py --phase final
python -B -m workbench.session check docs/workstreams/research/AF-RES-077/manifest.json --fetch
```

공통 코드·기존 fixture의 회귀는 연구 목표 적용과 구별한다. 필요한 게이트를 실행할 때에는 결과판의 별도 clean 작업 사본에서 다음 명령을 사용하고, command/exit/stdout/stderr를 owned_path 안에 저장한다.

```sh
python -B scripts/cloud_check.py --environment chatgpt-executor --fetch-contract --require-clean
```

이 환경 이름은 실행자 표지이며 특정 Codex 계정의 연결 증명이 아니다. 자세한 검사 기준 SHA·출력 해시·실제 종료값은 수용 기록에 남긴다. 원격 재열람은 GitHub의 정확한 result SHA에서 필수 파일 본문과 blob을 다시 받아 로컬 Git blob과 비교한다. acceptance 파일 자체와 나중 HANDOFF의 자기 참조 hash를 내장한 것처럼 주장하지 않는다.

목표 실행에는 고정 binary/Qt·MLT 환경과 완전한 native input/harness가 필요하다. [MS RUNBOOK](postseal/musescore/RUNBOOK.md), [SG build commands](postseal/sigil/report.json), [SC scope](postseal/shotcut/REPORT.md), 각 TESTS.minimum_followup을 사용한다. SG-E의 미지원 동작이나 SC-X의 비영상 입력을 몰래 교체하지 않는다. 보조 probe 재실행은 가능하지만 native 결손을 해소하지 않으므로 이번 재개에서 불필요하게 반복하지 않았다.
