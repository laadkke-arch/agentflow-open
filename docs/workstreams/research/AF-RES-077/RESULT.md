# AF-RES-077 결과 — PARTIAL

## ① 표1. 대상·고정판·원 요구·보존 조건·구현 지점

| 대상 / 모집 결과 | 고정판과 판의 한계 | 원 요구 절·작성자 위치 | 보존할 두 조건과 귀속 | 변경 전 구현 지점 |
| --- | --- | --- | --- | --- |
| **SC — Shotcut**. `proxy`/`relink` 합집합 첫10. 주 표본 공석, #910을 보조 사례로 고정. | `v20.09.13` → `0898bdf3fc0f9f3fbf78336bad21d5506e19c118`. 작성자가 20.09.13/Windows10을 명시했지만 설치 바이너리·요구 최초판은 미검증. | [#910 본문](https://github.com/mltframework/shotcut/issues/910), 신고자 johnnydepup. 외부 도구로 크기를 바꾼 영상을 같은 이름으로 대체한 뒤 Source 재생과 달리 timeline이 검다는 요구. 원본 이동·다른 폴더의 동명 영상 요구는 확인되지 않음. | C1: proxy 해제·저장·재열기에서 원래 입력 연결 보존 — 코드 계약을 참고한 연구 조건. C2: 불확실한 동명 후보를 다른 원본으로 확정하지 않고 p2 보존 — 연구자 확장. 둘 다 작성자가 동시에 제시한 두 조건으로 세지 않음. | `ProxyManager::resource/filterXML/processProperties`, `MltXmlChecker::checkForProxy/fixUnlinkedFile`, `UnlinkedFilesDialog::lookInDir`, `Util::getHash/getFileHash`. 완료 후 `ProxyReplacePostJobAction::doAction` → `MainWindow::replaceAllByHash` → playlist/timeline의 hash 교체도 범위 보존의 검토 지점. [고정 소스](https://github.com/mltframework/shotcut/tree/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src) |
| **MS — MuseScore**. `part`/`undo` 합집합 첫10. 주 표본 공석, PR4590을 보조 사례로 고정. | `v3.0.1` → `06a66a2206fc5f3c2c33d7ee4123badf496bc4dd`. PR 이전 릴리스지만 원 tracker 신고 이후판이다. 신고판 3.0/2.3.2와 동등한 affected build라고 확정하지 않음. | [PR4590 본문](https://github.com/musescore/MuseScore/pull/4590), 기여자 ericfont. selected source에서 parts를 만들면 실제 Selection에 속하지 않은 clone이 선택색을 띠는 문제. [원 tracker281441](https://musescore.org/en/node/281441)의 캐시 본문 일부는 ericfontainejazz·2019-01-08 19:55·Reported version3.0을 보여 주지만 최초판·전체 이력은 미확인. | C1: 새 part의 selected flag와 실제 Selection을 일치시킴 — 본문 지지. C2: 음악 link/track와 범위 밖 P2 음·배치 보존 — 연구 조건. undo/reopen 요구가 원 신고에 있었다고 세지 않음. | `Element` 복사 생성자·`selected/setSelected/curColor/linkedClone`, `Selection`, `Excerpt::createExcerpt/cloneStaves`, `ScoreElement::linkTo/unlink`, `LinkUnlink`, `Element::writeProperties/readProperties`. [고정 libmscore](https://github.com/musescore/MuseScore/tree/06a66a2206fc5f3c2c33d7ee4123badf496bc4dd/libmscore) |
| **SG — Sigil**. `split`/`anchor` 합집합 첫10. 엄격한 작성자·영향판 확인 주 표본 공석, #450을 보조 사례로 고정. | `0.9.17` → `30419827123d533d10ad482b1634dcec05ff0e1b`. 같은 날 신고 전 공개 릴리스라는 운영상 고정판. 작성자의 newest version을 이 숫자 판의 확인으로 바꾸지 않음. | [#450](https://github.com/Sigil-Ebook/Sigil/issues/450), 신고자 gennaios. self-file-qualified footnote link의 split 뒤 대상 보존. [후속 설명](https://github.com/Sigil-Ebook/Sigil/issues/450#issuecomment-520258201)은 reference와 target이 **함께 새 장으로 이동**하면서 옛 파일명이 남는 경우를 특정. | C1: split 뒤 원 footnote를 가리킴 — 본문 지지. 봉인 N/E의 둘 사이 분할은 연구 확장. C2: 다른 장의 같은 fragment를 합치지 않음 — 기존 코드 주석을 참고한 연구 조건. 임의 하위 폴더 이동은 원 요구로 확인되지 않음. | `Book::CreateSectionBreakOriginalResource/CreateNewSections`, `AnchorUpdates::GetIDLocations/UpdateAllAnchorsWithIDs/UpdateExternalAnchors`, `TextResource::SetText/SaveToDisk`. SG-E의 폴더 이동까지 구현하려면 `FolderKeeper`·`OPFModel`·import/reopen 경로가 추가됨. [고정 소스](https://github.com/Sigil-Ebook/Sigil/tree/30419827123d533d10ad482b1634dcec05ff0e1b/src) |

모집 30행과 탈락 사유는 [FRAME.csv](FRAME.csv), 봉인된 요구·입력은 [BRIEFS.jsonl](BRIEFS.jsonl)에 있다. **주 모집 적격은 0/3이며, 보조 사례는 3/3이다.** 이를 성공 사례 세 개로 읽지 않는다. 기존 봉인의 오류·후속 발견은 원본을 덮어쓰지 않고 [ERRATA.md](evidence/ERRATA.md)에 연결했다. MS 원 tracker의 이번 부분 확보는 별도 검토자의 검색 서비스 캐시 판독이며, root와 후속 open은 403이었다. 접근 성공 범위를 실제 원 서버 전체 이력 확보로 확대하지 않는다.

## ② 표2. 보기 A·B, 원전 절, 옮긴 변수와 선택·시험의 차이

| 대상·보기 / 실제 원문 문자수 | 제공한 1저작·최대2절·판 | 선택과 옮긴 변수 | 선택·시험에서 관측된 차이 | 전이가 깨지거나 원문이 보장하지 않는 부분 |
| --- | --- | --- | --- | --- |
| SC-A / **1,410** | Kdenlive manual, 표시판26.08/revision8a74558. [Proxy Settings](https://docs.kdenlive.org/en/project_and_asset_management/project_settings/proxy_settings.html), [Using Camera Proxy Clips](https://docs.kdenlive.org/en/tips_and_tricks/useful_info/using_camcorder_proxy_clips.html). | A1: 원본·proxy 역할을 분리하고 producer별 full-content provenance, 확인 전 거부, 안전한 생성·공개 순서 제안. 기존 코드 그대로인 A0와 경쟁. | SC-B와 정규화한 핵심 방식은 같음. 구현된 변경·성공 관측은 없음. | 동종 원문도 역할·경로/파일명 대응을 설명할 뿐 full digest·snapshot·atomicity를 제공하지 않는다. 2026 문서를 2020 개발자의 당시 자료로 보지 않음. |
| SC-B / **1,517** | [darktable4.8 sidecar](https://github.com/darktable-org/dtdocs/blob/9d2c663bbe2a3390fd3750fdce780025933a5045/content/overview/sidecar-files/sidecar.md), [duplicate manager](https://github.com/darktable-org/dtdocs/blob/9d2c663bbe2a3390fd3750fdce780025933a5045/content/module-reference/utility-modules/darkroom/duplicate-manager.md). 같은 매뉴얼 계보. | B-F: 원본 identity와 편집본 metadata를 분리; association/generation/state와 full digest 검증. sampled-hash 관계표 B-S와 경쟁. | 경쟁 후보의 표현·세대 필드는 달라짐. 선택은 A1과 같은 provenance/보수적 거부 계열. SC-X의 A는 rebuild 필요, B는 명시적 복구 결정 대기를 적어 **정책 전체 동일**은 아님. | sidecar가 현재 원본의 과거 bytes를 되살리지 않는다. 외부 교체·stale cache·동일 bytes의 서로 다른 역할은 별도 문제. hash와 generation은 연구자의 설계다. |
| MS-A / **949** | [MuseScore3 Handbook](https://musescore.org/en/print/book/export/html/278625)의 Parts overview/save, Undo and redo. live print판, 후대3.x 내용 포함. | A-C1: excerpt 생성 경계에서 destination clone만 deselect. 일반 복사·음악 link·기존 undo/save 유지. 전역 copy 생성자의 flag 제거 A-C2와 경쟁. | MS-B도 local reset을 선택. 고정 세 입력에서 local/global의 예상 성공 출력은 같음. 실제 과거 PR은 global을 선택하여 연구 선호와 불일치. | Handbook은 음/표시 공유 범위를 설명하지만 어떤 C++ 수정 지점이 최선인지 보장하지 않음. 고정 입력은 whole/scoped rollback을 가르지 못함. |
| MS-B / **1,571** | [TEI P5 4.8.0](https://tei-c.org/Vault/P5/4.8.0/doc/tei-p5-doc/en/html/TC.html), 2024-09-02/revision4e6e41b0b. §13.1.2 Readings [`TCAPLR`](https://tei-c.org/Vault/P5/4.8.0/doc/tei-p5-doc/en/html/TC.html#TCAPLR), §13.1.4.3 **The Witness List** [`TCAPWL`](https://tei-c.org/Vault/P5/4.8.0/doc/tei-p5-doc/en/html/TC.html#TCAPWL). | reading의 witness 식별·해당 위치의 유효 집합을 음악 link membership/track scope/local Selection의 구분에 제한해 대응. B-local 선택, B-global 경쟁. | 핵심 선택 변화0/1. 원전 근거를 넘는 undo journal·inverse reconstruction은 명시적으로 기각. | witness는 시간순 명령 로그가 아니다. `wit`나 유효 집합만으로 이전 pitch·명령 순서·역연산을 얻을 수 없음. live TC의 4.12.0과 봉인4.8.0을 혼동하지 않음. |
| SG-A / **1,234** | [EPUB3.3, 2023-05-25 Recommendation](https://www.w3.org/TR/2023/REC-epub-33-20230525/), §4.2.5 URLs in the OCF abstract container와 §6.1.2 XHTML requirements. | A-C1: `(original document URL, fragment)`를 최종 대상으로 옮기는 operation-local plan. 기존 A-C0, durable staging/journal A-C2와 경쟁. | SG-B와 같은 문서별 대응을 선택. 영구 content inventory는 선택하지 않음. | URI 규칙은 대상 주소의 해석을 제공하지만 split provenance·동시 편집·복구 프로토콜을 구현하지 않음. 2023 규격은 2019 당시 채택 증거 아님. |
| SG-B / **1,824** | [OCFL1.1](https://ocfl.io/1.1/spec/), 발행2022-10-07/갱신표시2024-11-07. §3.5.2 [Manifest](https://ocfl.io/1.1/spec/#manifest), §3.5.3.1 [Version](https://ocfl.io/1.1/spec/#version). | B-scoped: bytes identity·현재 논리 위치를 구분하고 source document/fragment/occurrence→새 대상 대응. 전역 digest catalog는 경쟁 가설로 기각. | 핵심 선택 변화0/1. digest는 plan stale 검사용 후보일 뿐 영구 inventory로 채택하지 않음. | object-at-rest 규격은 EPUB fragment의 의미·문서 내부 발생 위치·inverse split·원자 저장을 보장하지 않는다. 같은 문서의 duplicate ID는 문서 범위 추가만으로 해소되지 않음. |

각 보기의 실제 packet·common 전체 문자수, 언어, 해시, 선택 시각, 추가 열람0, 봉인 SHA는 [VIEWS.csv](VIEWS.csv)에 있다. 공통 입력/원문 packet은 `9518c3d…`, A 출력은 `7c1df93…`, B 출력은 `7bc2d1f…`에 차례로 봉인했다. 여섯 판독은 별도 모델 문맥이지만 같은 모델 계열이고, 사전학습 인지 여부·완전한 역할 지시 동일성은 검증하지 못했다. 결과는 **기술 대조**이며 독립 인과효과 분모는 0이다. 구체적인 후보13개와 쓰기·거부·유지 부담은 [CASEBOOK.md](CASEBOOK.md)와 원본 `readers/`에 보존했다.

## ③ 표3. 봉인 입력·두 예상·확인 방식·관측·실패 시 결정

아래 A/B는 각 보기의 **선택안**이다. 선택되지 않은 경쟁안의 예상까지 포함한39개 예측, source/assertion/당사자 보고/보조 실행/미실행 열은 [TESTS.csv](TESTS.csv)에 있다. 결과 칸의 소스 판독이나 보조 predicate는 목표 프로그램 통과가 아니다.

| 입력·초기 상태·순서 | A / B의 봉인 예상 | 확인 방식과 실제 관측 | 실패 시 결정·뒤집을 최소 증거 | 빈자리·분모 |
| --- | --- | --- | --- | --- |
| **SC-N 정상**. p1 원본RED·proxy H1, 원본 유지. proxy 해제→저장→재열기. | A: 원본 경로·XML·RED 유지. B: 동일 원본 복원; 검증되지 않은 legacy proxy는 해제 동작에 필요 없음. | 고정 XML/resource 경로를 읽음. 실제 MLT project·valid-media·rendered RED 출력 미확보. | 해제만으로 다른 source/원본 속성 소실이면 저장·복원 경로 수정. 고정 빌드의 active resource, 저장XML, 재열기 디코딩 증거 필요. | 목표 실행 **0/1**, 입력9 중1. |
| **SC-E 경계**. missing RED, 후보순서 BLUE 동명→RED sample-match, p2는BLUE. 확인 없이 탐색→proxy→저장·재열기. | A/B: RED를 제안해도 trusted historical full digest나 확인이 없으므로 새 binding을 거부, p1 unresolved·p2 BLUE 유지. B-S 경쟁안은 유일 sample match 수락 예측. | 보조 Python에서 고정순서의 filename/hash 조건과 first-match를 재현. native `QDir` 순서·Accepted gate·repair·p2·proxy·저장·재열기는 실행하지 않음. | 제안 row를 확정 오연결로 세지 않음. 실제 사용자 수락 유무를 정하고 변경된 producer 집합·완료 작업의 hash fan-out을 관찰해야 함. | 보조 predicate **1/1**, 목표 **0/1**. 거부≠복구 완료. |
| **SC-X 음성대조**. 3MiB A/B/C→A/D/C, 같은 경로·길이·옛 metadata/proxy. | A: 과거 full provenance 없으면 옛 proxy 보류, rebuild 필요. B: unverified/refuse, 명시적 recovery decision 대기. 양쪽 모두 현재 hash만으로 과거 변경을 증명하지 못함. | 실제 synthetic bytes의 첫·끝1,000,000바이트 MD5가 같고 full SHA256은 다름. 영상 파일·preview 출력은 아님. | sample identity만으로 내용 동일성 판단을 기각. 유효 영상·과거 full digest를 추가하는 시험은 새 입력층이어야 함. | 보조 predicate **1/1**, 목표 **0/1**; native 입력 결손. |
| **MS-N 정상**. m1=60 unselected, 새P1, P2=67/offset8. 생성→62 편집→1회undo→저장·재열기. | A/B:60→62→60, P1 비선택·link 유지·P2불변. | 원 `tst_parts/tst_links` 및 `.mscx` 입력·참조 파일을 읽음. 원 breath fixture의0→2→0 및 undo-reference=input byte 관계를 정적 확인. 이 m1/u1 입력 실행은 없음. | 실제 score·pitch command·link/track/P2 layout checkpoint를 구현해야 함. unrelated 중간 수정이 없는 입력으로 whole/scoped rollback 우열을 말할 수 없음. | 목표 **0/1**, 원시험 실행 영수증 **0**. |
| **MS-E 경계**. N과 같되 source selected=true. P1은 직접 선택하지 않음. | A/B: 생성 직후 source selection 유지·P1 flag=false/list empty; 이후60 복귀·P2불변. local/global 후보 모두 같은 예상. | 복사 flag와 Selection의 다른 경로를 확인. `curColor`는 `selected()` 외 `Note::mark()` 등에도 영향받음. 고정 입력의 즉시 checkpoint는 불충분. | 생성 직후 flag/list/mark·color를 함께 관찰. reopen 뒤 색상만 확인하면 원 결함을 놓침. global/local를 가를 copy contract나 coverage 반례 필요. | 목표 **0/1**. 현재 입력은 선택안 사이 우열 미판별. |
| **MS-X 음성대조**. 재열기 파일 current pitch62, 옛 pitch·명령 없음, undo stack empty. | A/B: undo unavailable/no-op/거부, 현재62와 link 유지. 옛60을 다른 입력에서 가져오지 않음. | TEI는 witness identity만, 원 undo source는 별도 command 정보를 다룸. 구체적 GUI·file 출력 미실행. | 이전 snapshot/command가 없는 inverse 추론 기각. 같은 초기 상태의 실제 unavailable/거부와 불변 저장 상태를 관찰해야 함. | 목표 **0/1**. 옛 pitch는 **미상**. |
| **SG-N 정상**. `#fn` ref와 FOOTNOTE_A 사이 split→ch1/ch1_1→저장·재열기. | A/B:`ch1_1.xhtml#fn`로A 보존. | 연구 XHTML의 literal href/ID와 기계적 분할 뒤 URI를 보조 검사. `<!--SPLIT-->`은 native marker가 아니며 실제 cursor/EPUB/save/reopen 미실행. | comment의 cursor 위치·실제 EPUB·지원되는 이름 변경을 정의한 후 실행. 원 #450의 둘이 함께 이동하는 경우와 별도 유지. | 보조 predicate **1/1**, 목표 **0/1**. |
| **SG-E 경계**. ch1/fn=A, ch2/fn=B, toc 각 ref. ch1 분할→`Text/parts/ch1_tail.xhtml`→저장·재열기. | A/B: self/toc A는A, toc B는B. 전역 digest catalog 경쟁안은 후보2개로 거부. | URI/ID 관계 보조 확인. 고정0.9.17의 고정 Text 폴더와 `/`·`\` 이름 거부 때문에 해당 native 이동은 지원되지 않음. | 성공/실패로 채점하지 않음. flat rename 또는 후대판 이동은 새 case로 봉인해야 함. 폴더 모델·import/reopen 변경 없이 대응표만 추가해 해결했다고 말할 수 없음. | 보조 predicate **1/1**, 목표 **0/1**, native 적용성 결손. |
| **SG-X 음성대조**. 원 문서 안에 fn가FIRST/SECOND 두 번, 신뢰할 기존 선택 없음. | A/B: 쓰기 전 duplicate key 거부·원 bytes 유지, 대상을 추측하지 않음. | 보조 strict resolver는 같은 문서의 후보2개를 관찰. 기존 코드 hash overwrite와는 별개. 실제 Sigil 거부/무변경은 미실행. | current bytes/digest만으로 의미를 복원한다는 전이 기각. 실제 split의 경고·대상 선택·원문 보존을 관찰해야 함. | 보조 predicate **1/1**, 목표 **0/1**. |

**분모:** 봉인 입력9, 선택안 예측18, 모든 후보 예측39, 목표 실행0/9, 목표 통과·실패 모두 미확인(9자리 전부 미실행), 동일 입력의 공개 실행 영수증0/9, 보조 predicate 관측5/9, 완전한 보조 workflow0/9, 적격 주 표본0/3. 0/9는 실패율이 아니며, native 성공률은 실행 분모0이라 산출하지 않는다. [실제 보조 receipt](evidence/auxiliary/observed-run-20261123/receipt.json)는 Python worker 종료0, 입력·출력 해시와 범위를 보존한다. 그 이전 workspace HEAD 아래에서 실행됐던 스크립트의 bytes와 뒤에 커밋된 bytes를 검사하며, 아직 커밋되지 않았던 파일을 당시 HEAD가 포함했다고 주장하지 않는다.

## ④ Q별 근거·선택·기각·공석 및 추가 분석

## Q1. 작성자가 바꾸려던 부분과 두 보존 조건은 무엇인가?

세 모집은 `[2019-01-01, 2025-12-31]`에서 각 저장소의 두 단어 조회를 합쳐 생성시각·동시 번호순 첫10으로 고정했다. 사후 좋은 사례를 발견했다고 순서를 바꾸지 않았다. SC는 동명 원본 이동·오연결 요구 대신 외부 대체 후 검은 timeline이라는 가까운 요구가 남았다. MS는 linked part를 만드는 순간의 UI flag 불일치이며 undo/reopen 요구가 아니었다. SG는 실제 링크 보존 요구가 가장 가깝지만 affected numeric build와 최초판 확인이 부족하고, 봉인 경계 입력은 작성자가 말한 조작과 다르다. `FRAME.csv`의 공석을 보조층으로 메우지 않는다.

MS 재개 검토는 원 tracker의 부분 캐시로 요구 기원을 보강했다. 초기 작업에서403이었던 사실과 이번 부분 반환을 함께 보존한다. 원 신고는2019-01-08, 고정 v3.0.1은 그 이후·PR 이전이므로 기존의 “요구 전 시행 지점” 표현은 PR 기준에 한정해야 한다. 이 결과로 원 연구의 C2나 undo/reopen 요청이 새로 확인되는 것은 아니다. [MS 재검토](evidence/resume-review-musescore.md), [모집 보고](recruitment/musescore/REPORT.md), [ERRATA](evidence/ERRATA.md).

최초 본문 revision은 여전히0/3이다. 현재 GitHub 본문의 created_at은 본문 최초판의 증명이 아니다. 원 body와 수정 이력·당시 binary까지 결합한 자료가 들어오면 Q1의 적격 판단을 다시 할 수 있지만, 기존 모집/판독의 입력을 소급 바꾸지는 않는다. 원저작의 저자, 요구 작성자, 해당 프로젝트 유지보수자, 본 연구 제안자를 각각 분리했다.

## Q2. 동종 자료만 보았을 때 무엇을 선택했는가?

SC-A는 proxy는 편집 대체물이고 최종 출력은 원본이라는 동종 설명과 강한 공통 보존 조건을 받아 full provenance 및 legacy 확인/거부를 골랐다. full read·generation snapshot·임시 공개는 문서에 그대로 있는 기능이 아니라 판독자의 설계다. 원본이 없어져도 아무 후보나 자동 연결하는 가용성보다 잘못된 연결 거부를 택했으므로 복구 완료의 비율과 안전한 거부의 비율은 별도여야 한다.

MS-A는 파트 생성이라는 요청 범위 때문에 destination clone의 selected bit만 없애는 local 방식을 골랐다. global copy mask도 두 번째 안으로 제시했고, 음악 link와 현재 undo·저장은 유지했다. 어떤 clone route도 놓치지 않아야 한다는 유지 부담과 일반 copy 계약 변경이라는 부담을 비교했지만 고정 입력은 둘의 예상 출력을 나누지 못한다.

SG-A는 URI의 source base와 fragment를 함께 해석하는 계획표를 골랐다. 단순 id→new file보다 구체적이지만 permanent inventory나 durable journal은 기본안에서 제외했다. snapshot·journal 경쟁안은 추가 복구 비용이 있는 별도 후보로 남겼다. 이 세 선택은 [A 봉인](https://github.com/laadkke-arch/agentflow-open/tree/7c1df93b11e06ca8b7f44ac5b7ff996879aebd09/docs/workstreams/research/AF-RES-077/readers)에서 B 전에 확인된다.

## Q3. 제공 원전은 실제로 무엇을 다루고 무엇을 보장하지 않는가?

darktable4.8의 sidecar와 duplicate manager는 원 이미지를 공유하는 여러 편집본의 metadata·history, database/sidecar의 관계를 설명한다. 이 구분은 proxy association의 역할을 생각하는 재료지만 영상 producer의 full digest, 외부 덮어쓰기 탐지, crash 복구를 제공하지 않는다. 같은 입력이라는 전제가 깨지는 SC-X가 전이의 한계다.

TEI4.8.0은 reading을 witness에 귀속시키고, 위치에 따라 활성 증거본이 다를 수 있음을 다룬다. 옮길 수 있는 것은 identity와 참여 범위의 분리다. 명령의 순서·이전 값·역연산은 해당 두 절에서 얻을 수 없으므로 “TEI 때문에 범위별 undo journal을 채택”이라는 설명은 기각한다. §13.1.4.3의 정확한 제목은 **The Witness List**이며 기존 원장 일부의 Witness Information은 상위절 제목과 섞인 표기였다. 최신 release URL을 과거 archive4.8.0으로 간주하지 않았다.

OCFL1.1 manifest는 digest와 보관된 content 경로를, version state는 특정 버전의 논리 경로를 연결한다. 동일 bytes와 현재 파일명은 별개라는 구분이 유용하다. 그러나 EPUB anchor는 파일 내부의 의미 있는 위치다. 파일 digest가 같거나 inventory가 valid라는 사실만으로 ref가 의도한 footnote를 가리키는지, split을 되돌릴 수 있는지, 두 파일 저장이 원자적인지 결정되지 않는다. 이 한계는 원 규격의 object-at-rest 범위와도 맞는다. 정확한 원절은 표2와 [reading notes](reading/NOTES.jsonl)에 연결했다.

## Q4. 대상 코드의 어느 식별자·저장 단위·복구 절차가 달라지는가?

**SC**의 두 선택은 producer association에 과거 내용 증거를 남기고 원본/생성 proxy를 확인하는 추가 metadata를 제안한다. B는 generation/state를 더 구체적으로 적었다. 결정적 추가 검토 지점은 완료된 proxy가 `ProxyReplacePostJobAction::doAction`에서 hash를 기준으로 배포되는 경로다. `MainWindow::replaceAllByHash`와 playlist/timeline downstream 교체를 그대로 두고 metadata만 producer별로 만들면 제안의 범위 보존은 아직 구현되지 않는다. 이는 새로 확인한 **변경 지점 누락**이다. frozen p2는 다른 hash를 가지므로 실제 p2가 바뀌었다는 관측으로 확장하지 않는다. [고정 postjobaction](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/jobs/postjobaction.cpp), [고정 mainwindow](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/mainwindow.cpp), [SC-R1](evidence/resume-review-shotcut.md).

**MS**의 선택은 지속 식별자나 저장 형식 추가 없이 excerpt destination의 SELECTED를 정리한다. `linkedClone`, track mapping, link serialization은 기존대로 유지하는 가설이다. local finalization이 모든 중첩 clone을 방문하는지는 미확인이다. global alternative는 `Element` copy constructor 한 지점이지만 모든 consumer의 복사 계약에 영향을 준다. 실제 과거 patch가 global을 골랐다는 사실은 이 대가를 없애지 않으며, TEI가 어느 함수를 지정한 것도 아니다.

**SG**의 선택은 원래 문서 URL+fragment(+발생 위치)를 최종 문서/fragment에 연결하는 임시 plan과 duplicate 검사를 추가한다. `SetText`와 `SaveToDisk` 사이 및 split의 새 resource 생성 시점이 rollback 설계에 중요하다. SG-E의 nested folder 이동은 `AnchorUpdates`만 고쳐서 성립하지 않으며 `FolderKeeper`·`OPFModel`·import/reopen을 포함한 capability 변경이다. 기본 선택의 세션 내 복원과 추가 journal안의 crash 복구를 구별한다. source mapping 자체로 atomic EPUB commit이 생기지 않는다.

## Q5. 같은 입력에서 서로 다른 결과를 낼 관찰 지점은 무엇인가?

세 경우 모두 경쟁안 두 개 이상은 있으나 **구별 시험을 충분히 실현한 것은 아니다**. SC-E는 filename/sample 수락 계열과 역사적 full evidence 요구 계열의 결정을 가를 수 있다. 관찰은 먼저 candidate row/warning, 다음 Accepted/checker gate, 다음 실제 p1/p2 변경, 마지막 proxy·저장XML·재열기여야 한다. 후보를 제안한 순간을 자동 오연결로 세면 오판이다. SC-X의 sampled edges 일치는 내용 전체 일치가 아니지만, 지금 full hash를 처음 얻는 것만으로 과거 변경을 판정할 수도 없다.

MS-E는 생성 직후 `selected()`와 `Selection` list를 함께 보면 copied flag를 가릴 수 있다. 색상만 보면 `Note::mark()`, drop-target, printing 조건 때문에 오판할 수 있고, 마지막 reopen만 보면 비직렬화 UI 상태가 사라져 차이를 놓칠 수 있다. local/global 후보는 고정 세 입력에서 같은 출력을 예측한다. 또한 P2 중간 독립 수정이나 stale snapshot이 없으므로 whole-state rollback과 scoped-command rollback을 이 자료로 구별했다고 할 수 없다.

SG-E의 의도된 관찰은 각 ref를 원래 base에서 해석한 `(document, fragment)`와 실제 target text다. SG-X에서는 같은 source 안의 duplicate를 관찰해야 하며 처음/마지막 occurrence를 무심코 선택해서는 안 된다. 그러나 SG-E의 native action이 불가능하므로 URI 모델의 올바른 예상도 목표 실행의 성공이 아니다. 입력9개를 바꾸지 않은 채 이 결손을 남겼다. 추가로 만들 판별 입력은 새로운 후속 봉인층에 둬야 한다.

## Q6. 원전의 전제가 사라지는 반례와 동종 대조는 무엇인가?

| 반례·동종 대조 | 직접 읽은 다른 저작과 확인 범위 | 결정에 주는 제한 |
| --- | --- | --- |
| 동일 bytes/식별자가 과거 값·의도를 제공하지 않음 | [PROV-DM §5.2.1](https://www.w3.org/TR/2013/REC-prov-dm-20130430/#term-Derivation), [RFC7089 §1.1/1.3](https://www.rfc-editor.org/rfc/rfc7089.html#section-1.1) | SC-X 과거 bytes, MS-X 옛 pitch가 실제 기록돼야 한다. lineage나 현재 label만으로 복구 성공을 주장하지 않음. |
| undo는 witness 참조와 다른 운영 정보가 필요 | [Qt5.15 Undo Framework](https://doc.qt.io/archives/qt-5.15/qundo.html) | command와 stack이라는 동종 대안이 더 직접적. MuseScore가 Qt의 stack을 사용한다는 증거로 전용하지 않음. |
| 공유 data와 로컬 표시의 분리가 또 다른 공유 경로로 깨짐 | [Blender3.6 Duplicate Linked](https://docs.blender.org/manual/en/3.6/scene_layout/object/editing/duplicate_linked.html) | mesh/transform 구분이 있어도 shared Action은 변환에 영향을 줄 수 있음. MS local flag 수정만으로 모든 범위 밖 보존을 보장하지 않음. |
| 문서 base가 이미 동종 답을 줌 | [RFC3986 §3.5/5.2](https://www.rfc-editor.org/rfc/rfc3986.html#section-5.2), EPUB3.3 | SG의 문서+fragment는 B만의 새 원리가 아님. 상대 path와 각 ref의 base를 보존해야 함. |
| 같은 문서 duplicate ID | [XML1.0 typed ID 규칙](https://www.w3.org/TR/2008/REC-xml-20081126/#sec-attribute-types), [당시 Sigil guide Links and IDs](https://github.com/Sigil-Ebook/sigil-user-guide/blob/d101fa2b5dc09ea0d2e1ac987d061c3338745710/src/OEBPS/Text/links.html) | SG-X는 문서 범위만으로도 모호. XML typed-ID 규칙이 모든 untyped attribute를 자동 검증한다고 확대하지 않음. |
| 포장/내용 무결성과 참조 의미는 별개 | [BagIt §3](https://www.rfc-editor.org/rfc/rfc8493.html#section-3), [Pro Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects) | checksum-valid 포장 또는 blob/tree identity가 의미상 잘못된 href를 고치지 못함. |
| inventory가 있어도 원자 저장은 자동으로 생기지 않음 | [SQLite Atomic Commit §3/5/9](https://www.sqlite.org/atomiccommit.html) | rollback 정보 선행 보존, flush, 다중 파일 조정과 장애 가정이 필요. 이를 실제 대상 filesystem에서 시험한 것은 아님. |

반례·대안은 named9저작이며 재열람/번역/버전 반복으로 늘리지 않았다. 원 제공3, 동종3, 요청3과 대상 code 계보를 합쳐 named24, 제품별 manual/code를 일관되게 묶으면 conservative21이다. 전체 최소량20을 넘겼다는 사실은 “당시판 대상 문서·코드·시험 독립6저작”을 충족시키지 않는다. 해당 층은 named6→conservative4이고 당시판이 확인되는 독립 계보는3이므로 미달을 유지한다. [COUNTING.md](evidence/COUNTING.md), [SOURCES.jsonl](SOURCES.jsonl).

## Q7. 원시험·실제 파일·판독 가능한 출력이 어디까지 가르는가?

**공개 결과와 source assertion을 분리했다.** SC #910의 issue close는 성공 영수증이 아니며 마지막 작성자 답변도 검은 화면이 남았다고 한다. MS의 실제 병합은 `16851045c9e50eafb016c5cf4f2733f974e841bf` /2019-03-07로 확인되며, `Element` copy constructor의 SELECTED 제거 한 줄과 시험 변경0개를 확인했다. 이것은 historical adoption이고 봉인 input9의 실행 결과는 아니다. [MS 사후 원자료](postseal/musescore/report.json).

MS 원시험 source·실제 `.mscx`·golden reference는 link와 undo/read-write의 검사 의도를 보여 준다. breath input/reference의 bytes와 요소 수 관계를 읽었다는 사실만으로 `tst_parts`가 실행돼 통과했다고 하지 않았다. 과거 CI metadata가 비어 있거나404라는 사실도 당시 검사가 없었다/실패했다는 증명이 아니다. 실제 command/exit/stdout·빌드 environment가 필요하다.

SG의 [역사적 수정 ae60e3e…](https://github.com/Sigil-Ebook/Sigil/commit/ae60e3e63a2f9343b40d316f179b9dfbcb6d838b)은 file-qualified local link의 더 좁은 분기를 고쳤다. 당시 댓글의 manual 확인과 patch 존재는 보존하되, 동일9입력의 실행 영수증으로 채점하지 않았다. 공개 축소 `test_split2.epub`은 실제 archive를 열어 marker와 href를 확인했다. marker는 ref/target 둘 앞에 있고, `../Section0001.xhtml#here`는 없는 `OEBPS/Section0001.xhtml`로 해석된다. 원 bytes를 수정한 뒤 “원시험 성공”으로 세지 않았다. [fixture inspection](postseal/sigil/originals/fixture-inspection.json), [SG 재검토](evidence/resume-review-sigil.md).

이 환경에는 고정 대상 binaries와 필요한 Qt/MLT 개발환경·cmake/ctest가 없어 목표 build/run을 수행하지 않았다. 기존 qmake·pkg-config 확인의 종료1을 [environment.json](evidence/environment.json)에 남겼다. Python 보조 실행은 실행 가능했고5개 input predicate를 확인했으며 종료0이다. 대상GUI·완전 workflow는0이다. 상세 command/input은 [RUNBOOK](postseal/musescore/RUNBOOK.md), [보조 재현](evidence/auxiliary/README.md)와 최종 HANDOFF에 있다.

## Q8. 같은 예산에서 바뀐 것은 선택·시험·설명 중 무엇인가?

| 집계 단위 | 분자 / 분모 | 해석 |
| --- | --- | --- |
| 정규화한 핵심 선택 변화 | **0/3** | SC full provenance, MS local deselection, SG document-scoped relocation으로 A/B가 수렴. 이것은 full implementation·recovery policy 동일성 주장이 아님. |
| 경쟁 후보 집합의 차이 | **2/3** | SC의 sampled 관계표, SG의 digest catalog 등 표현·구조가 달라짐. 독립 source-only 인과효과는 미식별. |
| 새 시험 입력 | **0/9** | 입력은 자료 노출 전에 고정했으므로 뒤에서 새 입력으로 갈아끼우지 않음. 시험 발견 효과를 측정한 설계가 아님. |
| 선택안의 핵심 안전 조건에서 상충하는 예측 | **0/9** | 양쪽이 같은 보존/거부 계열을 예측. SC-X의 복구 결정 시점 등 세부 정책 차이는 남음. 실행 확인치가 아님. |
| 원전별 설명·기각 근거 | **3/3** | sidecar/history, witness scope, content/logical path의 구분을 설명하고 과도한 전이를 기각. 학습 효과의 크기나 유일한 기여로 해석하지 않음. |
| 독립 인과효과·원 개발자 시간절감 | **분모0 / 미측정** | 같은 모델 계열·강한 공통 배경·사전 인지 불명·root 결말 요약 노출·역할 지시 동일성 미증명 때문에 산출 불가. |

예산은 각1저작·최대2절·원문2,000자 상한·추가 reader open0으로 같다. **실제 노출량은 같지 않다.** A 원문 합계3,593자, B4,912자다. 공통 JSON과 URL·메타데이터까지 독자가 본 파일 전체는 별도 열에 기록했다. 영어 원문을 주고 연구 제안을 받았으며 번역/모델 토큰·활성 작업시간은 계측하지 않았다. 시간·문자수·문서 수를 하나의 동일 실현 비용으로 바꾸지 않았다.

재개 전 보존된 외부 요청 구성은222건, 일부 web 보고2건을 포함하면224건이나, 탐색·재판독·내부 retry가 빠진 **하한성 구성 합계**다. 이번 재개 검토50건은 open/find를 포함하는 별도 **읽기 연산**이고 HTTP 요청 수와 합산하지 않는다. GitHub 규칙/의존/결과 재열람·publish는 연구 자료 비용과 별도다. developer minutes와 실제 tool billing은 미관측이다. [COSTS.csv](COSTS.csv), [EXPOSURE.md](evidence/EXPOSURE.md), [재개 원장 설명](evidence/RESUME_REGISTRY.md).

MS의 과거 global patch가 존재한다는 채택 사실은 구체적으로 말할 수 있다. 그러나 2024 TEI·이번2026 판독이2019 원 개발자의 선택을 바꿨다는 인과·시간절감 주장은 성립하지 않는다. 나머지 제안 역시 target 수정·적용·GUI 성공으로 보고하지 않는다. 외부 원전이 쓸모없다는 결론도 이3개 보조 사례·강한 공통 조건·판독 설계로는 도출할 수 없다.

## 검산·분모·재개 범위

| 요구 항목 | 충족 범위 / 남은 결손 |
| --- | --- |
| 20개 이상 독립 원문 | 보수적21계보. 원저작별 URL·판·절·확인/미확인·접근 실패를 SOURCES에 기록. 제거한 full-text cache의 raw hash는 현재 파일만으로 재계산 불가이며 영수증 기반임을 표시. |
| 모집·요구 최초판·고정판 | 첫10×3=30행, 소스 tag SHA3/3, 엄격한 주 표본0/3·최초 body revision0/3. MS cache 부분 확보도 최초판 보증 아님. |
| 대상별 경쟁안·보기 봉인 | 보기6, 후보13, 선택안 예측18, 모든 후보 예측39. A before B와 공통 packet hash 대조. |
| 9자리 실패 시험 | 입력9/9, 좁은 보조 관측5/9, 완전한 목표/보조 workflow0/9. 원시험 source·fixture·당사자 보고·미실행 열 분리. |
| 고정판 대상 자료 독립6저작 | named6, 보수적4, 당시판 확인3: **미달**. 코드 파일·test·release를 서로 다른 저작으로 세지 않음. |
| 자가·분담 검토 | 원 연구와 같은 모델 계열. 재개3개 분담 검토는 사후 감사이며 blind reader/독립 인간 추가0. |
| 파일·범위·원격 확인 | 결과의 actual checker 시각·명령·종료값·해시는 SELF_CHECK, evidence/acceptance-evidence.json 및 마지막 HANDOFF를 기준으로 함. 검사 통과는 모집/실행 결손을 지우지 않음. |

이 결과는 `2f7e075…` 이후 미완료였던 결과·검산·인계 묶음을 완성한다. 기존 A/B 판독을 반복하지 않았고 기존 커밋·브랜치를 reset하지 않았다. 중앙 dot-control.json의 상태 갱신은 배정자 역할이다. source 변경에서 실제 작동으로 넘어갈 때 필요한 최소 후속은 아래3개 결손에 묶었다.

## ⑤ 불일치·약점 — 정확히 3건과 다음 조사 제안

1. **요구·판·조작의 대응이 주 표본을 충족하지 못했다.** SC의 실제 문제는 원본 이동이 아니고, MS는 undo/reopen 요구가 아니며, SG는 작성자 영향판과 봉인 split 방식이 맞지 않는다. MS 원 tracker 부분 확보로 “원 요구 이전 v3.0.1” 표현도 정정했다. 다음 조사는 기존30행을 유지한 채, 원 body revision·당시 binary·native 조작이 함께 확인되는 새 모집층을 별도 봉인한다. 적격0/3을 유지보수자의 세 요구로 포장하지 않는다.

2. **자료 교체의 독립 효과와 구현안의 우열을 식별하지 못했다.** 공통 배경에 심벌·강한 보존 조건·실패 입력이 이미 있고, 원문 길이·역할 지시·사전 인지 통제가 부족하다. A/B 핵심 선택은0/3 변화이고 MS의 실제 historical global 채택은 두 판독의 local 선호와 다르다. 다음 조사는 역할 지시와 실제 노출 길이를 맞추고 source name/결말을 보지 않은 새 판독에, local/global 또는 whole/scoped가 다른 출력을 낼 native 입력을 **사전에** 고정한다. 현재0/3에서 원전 무용성·시간절감을 추정하지 않는다.

3. **식별자·계획표의 타당성과 실제 복구·저장 성공 사이에 실행 공백이 남았다.** 목표0/9, 원 실행 영수증0/9이며 SG-E는 native 미지원, SC-X는 비영상이고 MS-E는 checkpoint·색상 혼동 위험이 있다. SC 완료 시 hash fan-out, SG 폴더/import 경계, MS clone coverage는 추가 구현 검토가 필요하다. 다음 조사는 고정 환경에서 실제 파일과 단계별 객체/XML/EPUB·출력 로그를 남기고, 중단 복구는 별도의 failure injection으로 검증한다. 기존 입력을 몰래 고쳐 성공을 추가하지 않고, 새 입력·새 구현·새 비용층을 함께 봉인한다.
