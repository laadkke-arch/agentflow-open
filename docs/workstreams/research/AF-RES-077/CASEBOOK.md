# AF-RES-077 사례집 — 전이의 채택보다 경계를 먼저 판정

## 판독 단위와 주장 주체

이 사례집의 **선택**은 여섯 개 새 모델 문맥이 남긴 연구 제안이다. 제품 작성자의 요청, 원전 저자의 주장, 동종 문서의 설명, 실제 저장소에 병합된 변경과 구별한다. 원문 요구의 모집 적격 주 표본은 0/3이고, SC910·MS4590·SG450 세 보조 사례를 고정판 인터페이스와 함께 사용했다. 전체 first-ten 후보는 `FRAME.csv`, 출처와 한계는 `SOURCES.jsonl`, 직접 노출과 봉인은 `VIEWS.csv`다.

공통 배경에는 이미 구체적 코드 심벌과 연구자가 정한 불변조건·입력 9자리가 들어 있다. 따라서 후속 원전만이 선택을 만들었다고 식별할 수 없다. A는 동종 원문, B는 제공 외부 원문이다. 각 1저작·최대2절·2,000자 상한이고 추가 열람은 0이다. 실제 문자수는 서로 다르다. 여섯 판독 모두 둘째 후보를 냈으며 총 후보는 13개다. 원본 제안 JSON을 축약하면서도 아래에서는 주장하지 않은 실행 성공을 추가하지 않았다.

## SC — 원본/프록시 연결과 내용 변경

### 원래 목적과 보존 조건

[#910](https://github.com/mltframework/shotcut/issues/910)의 johnnydepup는 20.09.13/Windows10에서 외부 도구로 영상 크기를 바꾸고 같은 이름으로 대체한 뒤 Source에서는 재생되지만 timeline은 검게 보인다고 썼다. 동명 두 폴더의 오연결이나 이동 원본 탐색 요구를 작성자의 말로 인용할 수 없다. C1은 프록시를 꺼서 저장·재열기해도 원래 입력 연결을 보존하는 것, C2는 불확실한 후보를 다른 원본으로 확정하지 않고 관계없는 p2를 유지하는 것이다. 이 두 조건은 기존 코드 계약을 참고한 **연구 조건**이다.

### 두 보기의 후보와 선택

| 보기·후보 | 그대로 두는 부분 | 바꾸는 객체·키·위치 | 이벤트별 쓰기와 실패 정책 | 추가 부담 |
|---|---|---|---|---|
| A0 기존 코드 | 원본 resource, sampled hash/cache, filename fallback, 기존 XML 저장 | 없음 | 첫 filename/hash 후보 제안, 경고; 수락 뒤 기존 repair | 구현 비용0, 기존 불확실성 유지 |
| **A1 선택** | 원본 경로 권위, 기존 resource 복원, sampled hash는 탐색 힌트 | producer별 `shotcut:originalSha256`, `shotcut:proxySourceSha256`; lookInDir/fixUnlinkedFile/checkForProxy/filterXML/processProperties 및 별도 full-hash helper | 모든 후보 수집→과거 full digest 또는 확인→안정된 입력 snapshot→임시 proxy 생성→완료 proxy 공개→해당 producer 바인딩→XML 교체. 과거 증거 없는 legacy는 거부 | 두 digest, full read, 입력 snapshot·임시 proxy 공간, migration·obsolete job·정리 |
| B-S sampled 관계표 | sampled hash 알고리즘, 원본 경로 | association_id/proxy_generation/binding_state 및 producer별 row | 유일한 sample match만 자동 선택→임시 생성→파일 공개→binding→XML. filename-only·다중 후보 거부 | 작은 XML 확장, sampled I/O, 미완료 출력 정리; 중간 바이트 변경 검출 못함 |
| **B-F 선택** | B-S의 범위 제한과 기존 resource 복원 | source_digest/proxy_source_digest/digest_algorithm; full verification helper | 과거 증거 또는 확인→snapshot/full digest→proxy 공개→세대 binding→XML. 사용 전에 재검사. 증거 없거나 변경됐으면 거부/재생성 안내 | 전체 읽기·snapshot·schema·legacy 확인 비용; 원전이 이를 구현해 주지 않음 |

A의 [Kdenlive proxy/camera-proxy 문서](https://docs.kdenlive.org/en/tips_and_tricks/useful_info/using_camcorder_proxy_clips.html)는 원본/편집용 대체물의 역할과 폴더·이름 변환을 설명한다. B의 [darktable4.8 sidecar](https://github.com/darktable-org/dtdocs/blob/9d2c663bbe2a3390fd3750fdce780025933a5045/content/overview/sidecar-files/sidecar.md) 및 [duplicate manager](https://github.com/darktable-org/dtdocs/blob/9d2c663bbe2a3390fd3750fdce780025933a5045/content/module-reference/utility-modules/darkroom/duplicate-manager.md)는 같은 입력을 공유하는 편집본의 metadata/history와 database/sidecar 권위 충돌을 설명한다. 양쪽은 모두 full-digest provenance를 선택했지만 digest·snapshot·임시 공개·거부 문턱은 **원문에 없는 공학적 추론**이다. 동일 모델의 다른 문맥이 같은 강한 공통 조건을 받아 같은 방향으로 간 것까지 확인된다.

### 깨지는 전제와 실제로 가르는 관찰

SC-E는 legacy sampled hash만 준다. B-S는 유일한 H_RED 후보를 받아들이지만 A1/B-F는 과거 full digest나 사람 확인이 없어 거부한다. 이 거부는 다른 파일을 붙이지 않는 조건을 만족할 수 있어도 복구 완료와 같지 않다. 사람 의도를 식별하는 능력과 바이트가 같은지를 구별해야 한다. 두 파일의 bytes가 같아도 외부 프로젝트에서 서로 다른 역할을 가진 원본일 수 있다.

SC-X의 중간 bytes만 바꾼 예는 shared input 불변이라는 darktable 전제를 제거한다. full hash를 **지금 처음** 계산한다고 과거 bytes를 복원할 수 없다. A1/B-F가 말한 것은 stale proxy의 원인을 증명했다는 성공이 아니라 증거 없는 proxy를 사용하지 않는 정책이다. [PROV-DM §5.2.1](https://www.w3.org/TR/2013/REC-prov-dm-20130430/#term-Derivation)의 entity/derivation 식별도 없던 이전 bytes를 생성하지 않는다.

고정 [Util::getFileHash](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/util.cpp)는 1,000,000바이트씩 양 끝을 MD5한다. fixture의 1MiB 블록 단위와 혼동하지 않았다. [lookInDir](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/dialogs/unlinkedfilesdialog.cpp)의 first-match는 제안 row를 바꾼다. [MainWindow의 수락 gate](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/mainwindow.cpp)가 있으므로 제안→오연결 완료라는 비약은 기각한다. 원 보고의 종료도 해결 성공이 아니었다. 자세한 후속은 `postseal/shotcut/REPORT.md`다.

## MS — 연결된 음악 내용과 로컬 선택 표시

### 목적과 조건

[PR4590](https://github.com/musescore/MuseScore/pull/4590)의 ericfont(CONTRIBUTOR)은 selected source에서 파트를 만들면 파트 Selection은 비어 있는데 복제 요소가 파랗게 표시된다고 썼다. v3.0.1은 PR 전날의 고정 가능한 소스이지 작성자가 확정한 affected build가 아니다. C1은 새 파트의 선택 flag와 선택 list를 일치시키는 저자 지지 조건이다. C2는 음악 link/track mapping과 범위 밖 P2의 음·배치를 보존하는 연구 조건이다. undo/reopen 요구를 이 작성자의 원 요구로 확장하지 않았다.

| 보기·후보 | 그대로 두는 부분 | 바꾸는 지점 | 쓰기/취소/실패 순서 | 추가 부담 |
|---|---|---|---|---|
| **A-C1 선택** | Element의 일반 복사, source Selection, 음악 link/track/system 예외, 현재 XML | `Excerpt::createExcerpt/cloneStaves`의 destination-only finalization에서 새 요소·자식 selected=false | clone/link 등록→독점 소유 clone의 선택 제거→공개→기존 pitch command/undo→현재 state 저장·읽기. 실패 생성은 자신의 새 객체/link만 정리 | 새 clone 방문 O(n), 저장 형식 변경0, 모든 excerpt route의 coverage 유지 |
| A-C2 | 음악적 필드·link·mapping | `Element` copy constructor에서 SELECTED(0x40) mask | 복사 시 flag 제거→autoplace/link→기존 edit/undo/save | 요소당 mask1, 모든 copy consumer 의미 검토 |
| **B-local 선택** | A-C1과 같은 범위 | excerpt materialization boundary | local appearance와 musical association을 분리, inverse는 기존 기록이 있을 때만 | persistence 추가0; 중첩 clone 누락 위험 |
| B-global | A-C2와 같은 범위 | 모든 Element copy constructor | 생성 초기부터 선택을 제거, history는 만들지 않음 | 단순한 한 지점 대신 전체 복사 계약 영향 |

A의 [MuseScore3 Handbook](https://musescore.org/en/print/book/export/html/278625)은 공유 음악 데이터와 파트별 presentation·save 및 undo/redo를 설명한다. B의 [TEI P5 4.8.0 Critical Apparatus](https://tei-c.org/Vault/P5/4.8.0/doc/tei-p5-doc/en/html/TC.html#TCAPWL)는 reading의 witness 식별과 해당 위치에서 유효한 witness 집합을 다룬다. 옮길 수 있는 변수는 **음악 link membership / 해당 part·track의 적용 범위 / 로컬 selection**을 하나의 상태로 취급하지 않는 구분이다. TEI의 `wit`나 witness complement를 실행 명령이나 “영향받은 범위 undo journal”로 바꾸는 추론은 원전이 보장하지 않아 기각했다. 실제 코드 심벌·고쳐야 할 flag는 공통 배경에서 이미 주어졌다.

### 반례와 실제 채택의 불일치

MS-X는 이전 pitch와 command/snapshot이 없는 새 세션이다. 두 선택 모두 현재 pitch62를 보존하며 역사적 undo를 거부한다. [Qt5.15 Undo Framework](https://doc.qt.io/archives/qt-5.15/qundo.html)는 명령 객체와 명령 stack이라는 별도 운영 정보를 설명한다. 이 문서를 MuseScore가 QUndoStack을 사용한다는 증거로 삼지 않았다. TEI나 [PROV-DM](https://www.w3.org/TR/2013/REC-prov-dm-20130430/) 식별자는 없는 역연산을 제공하지 않는다.

두 판독 모두 local boundary를 선호했다. 사후 열람한 실제 PR은 2019-03-07에 **copy constructor에서 SELECTED를 지우는 한 줄**을 병합했고 추가 시험 파일은 없었다. 이는 실제 역사적 채택이 연구 제안과 다르다는 사례다. “B 덕분에 원 개발자가 채택했다”라는 이야기를 지지하지 않는다. 전역 copy 계약 검토와 clone coverage라는 상충 비용은 제안에 남아 있으며 고정 3입력만으로 어느 쪽이 더 나은지는 결정되지 않는다.

MS-N/E는 P2의 중간 독립 변경이나 오래된 snapshot을 넣지 않았다. 그러므로 whole-state rollback과 scoped-command rollback이 둘 다 같은 최종값을 낼 수 있다. MS-E는 파트 생성 직후 flag/list를 보면 copied-selected와 cleared-selected를 가를 수 있지만, 봉인 입력의 checkpoint가 충분히 구체적이지 않으며 마지막 reopen만 보면 선택 비직렬화가 차이를 지울 수 있다. 이 결손을 새 성공 시험으로 메우지 않았다. 원본 `.mscx`·참조 출력과 `tst_parts/tst_links`는 `postseal/musescore/`에 있으며 source assertion과 실제 실행은 별도다.

## SG — 장의 위치와 참조 대상의 구별

### 목적과 조건

[#450](https://github.com/Sigil-Ebook/Sigil/issues/450)의 gennaios는 상업 학술 EPUB의 자기 파일명을 포함한 footnote links가 split 뒤 잘못된 대상을 가리킨다고 설명했다. “newest version”만 있어 0.9.17은 직전 공개 릴리스라는 운영상 고정판이다. C1은 split 뒤 원 footnote를 계속 가리키는 저자 지지 조건, C2는 다른 장의 같은 fragment 이름을 합치지 않는 연구 조건이다. 실제 요구에 동일 이름 두 장과 임의 folder move가 모두 있었다고 쓰지 않는다.

| 보기·후보 | 바꾸는 객체·키 | 쓰기 순서·거부·복구 | 저장/유지 부담 |
|---|---|---|---|
| A-C0 기존 | 없음; id→filename hash, split-derived/external 두 pass | 기존 split/save/SetText; 별도 rollback 추가 없음 | 증가0, move 경로 미확인 |
| **A-C1 선택** | `OriginTargetKey(original content URL, fragment)`와 duplicate count/final location; Book orchestration/GetIDLocations/anchor pass | 원래 base로 href 해석→split·최종 경로 계획→검증→문자열 적용→저장. 중복 source ID는 쓰기 전 거부. 세션 내 원문 복원만 제안 | 임시 O(target+link+changed text), 영구 식별자0; URL/move caller 유지 |
| A-C2 | C1 + staging/journal/snapshot/recovery coordinator | 계획 검증→staged book→prepared journal→지원되는 저장소에서 교체→완료 기록 | book copy+snapshot·I/O·crash 복구 구현 부담; 필요성 미확인 |
| B-digest catalog | manifest[digest] / version.state[digest]의 경로 목록; 전역 fragment multimap | snapshot→계획→전역 후보가 singleton일 때만 적용→저장→inventory 공개. 중복 후보면 거부 | 영구 catalog·revision·retention·checksum 재계산; 논리 대상 식별은 미해결 |
| **B-scoped 선택** | `SplitLinkPlan`: 원래 문서+fragment+source occurrence→새 target; text digest는 plan stale 확인에 한정 | 원래 source/base 캡처→중복 검사→분할/이동 대응→최종 상대 href→검증→SetText→SaveToDisk. 실패 시 부분 적용 정리; crash atomicity 미확인 | 임시 text snapshot/maps; 영구 inventory 불필요 |

A의 [EPUB3.3 URL 절](https://www.w3.org/TR/2023/REC-epub-33-20230525/#sec-container-iri)과 [RFC3986 §3.5/5.2](https://www.rfc-editor.org/rfc/rfc3986.html#section-5.2)는 문서 base와 fragment의 관계를 이미 설명한다. B의 [OCFL1.1 manifest/version](https://ocfl.io/1.1/spec/#manifest)은 내용 digest·물리 경로·버전별 논리 경로를 분리한다. 원전에서 얻은 유용한 구별은 bytes가 같다는 것과 현재 논리 위치가 같다는 것이 다르다는 점이다. 원래 문서/anchor/segment 대응표, 쓰기 전 거부, 실행 순서와 rollback은 연구자가 만든 설계다.

### 원전 과잉 적용을 가르는 대조

SG-E의 두 장에 각각 `fn`이 있으면 전역 digest catalog 후보는 둘이라 거부한다. 문서별 대응은 각 원 target을 구별한다. 단, 그 결과는 제안의 예측이며 **0.9.17에서 Text/parts/...로 이동하는 native 동작은 확인되지 않고 소스의 고정 폴더·이름 제약에 막힌다**. 동종 원문만 받은 A도 이미 문서별 대응표를 선택했다. 이 사례에서 외부 원전만의 새로운 핵심 선택은 관찰되지 않았다.

SG-X는 같은 원 문서 안에 duplicate ID가 있다. 문서 범위를 추가해도 하나로 정해지지 않는다. [당시 Sigil guide의 Links and IDs](https://github.com/Sigil-Ebook/sigil-user-guide/blob/d101fa2b5dc09ea0d2e1ac987d061c3338745710/src/OEBPS/Text/links.html)는 같은 파일의 동일 ID를 금한다. [XML1.0의 typed-ID 규칙](https://www.w3.org/TR/2008/REC-xml-20081126/#sec-attribute-types)도 문서별 유일성의 다른 관점이지만 untyped 속성까지 자동 검증한다고 확대하지 않는다. [BagIt §3](https://www.rfc-editor.org/rfc/rfc8493.html#section-3)의 checksum-valid 포장이나 [Git blob/tree](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)는 잘못된 참조 의미를 고쳐 주지 않는다. OCFL의 object-at-rest 규격을 원자적 저장 프로토콜이나 inverse split로 전환하는 것도 기각한다.

사후 실제 댓글은 원래 결함을 더 좁혔다. reference와 target 사이를 나누는 경우보다 **둘이 함께 새 장으로 이동하면서 href에 옛 파일명이 남는 경우**가 핵심이었다. 따라서 봉인 N/E가 실제 보고의 결함을 대표한다고 말할 수 없다. 원 공개 축소 EPUB와 fix commit은 `postseal/sigil/`에 보존했다. 그 축소 fixture의 상대 경로에도 별도 결손이 있어 파일 bytes를 고쳐서 원시험 성공으로 세지 않았다.

## 추가 분야의 반례 검산 — 판독자에게는 미노출

[SQLite Atomic Commit §3·§5·§9](https://www.sqlite.org/atomiccommit.html)은 이전 page 내용을 journal에 먼저 보존하고 flush 순서·여러 파일의 super-journal·복구 시 이름 보존을 요구하는 구체적 프로토콜을 설명한다. 따라서 OCFL inventory나 darktable sidecar가 있다는 사실만으로 A-C2/B-F가 제안한 중단 복구를 얻는다는 추론은 더 약해진다. 이 문서를 읽었다고 대상 제품에 SQLite를 넣으라고 결론 내리지 않았다. SQLite 내부의 과거 구현과 OS 가정이 섞인 설명이고, 우리 대상의 실제 파일시스템 내구성은 검사하지 않았다.

[Blender3.6 Duplicate Linked](https://docs.blender.org/manual/en/3.6/scene_layout/object/editing/duplicate_linked.html)는 두 객체가 mesh를 공유해도 transform은 따로 가질 수 있음을 설명한다. 그러나 같은 animation Action을 공유하면 분리돼 보이는 transform도 동일한 animation 값에 따라간다. MS에서 “로컬 flag만 지웠으니 모든 범위 밖 영향도 없다”는 비약을 점검할 다른 분야의 반례다. Musical link, selection, layout의 공유 경로를 각각 조사해야 한다. Blender 동작을 실행하거나 이 설명으로 MuseScore의 구조를 증명하지 않았다.

[RFC7089 §1.1·§1.3](https://www.rfc-editor.org/rfc/rfc7089.html#section-1.1)은 현재 Original Resource와 이전 상태를 실제로 담는 Memento, 가용 버전 목록을 제공하는 TimeMap을 분리한다. 이것은 TEI witness 식별이나 현재 digest만으로 잃어버린 history가 생기지 않는다는 MS-X/SC-X의 한계를 뒷받침한다. 실제 과거 body를 archive에서 복원했다는 결과는 없고 최초 요구판은 여전히 미확인이다.

이 세 저작은 모두 B 봉인 뒤 compiler가 읽은 대안/반례다. 원전 교체 비교의 추가 노출로 소급 계산하지 않았으며 A/B 입력도 변경하지 않았다. 원전명이 다른24저작과 제품 설명서를 보수적으로 합친21계보의 차이는 `evidence/COUNTING.md`에 있다. 봉인 배경 자체의 두 정정과 실행 가능성 한계는 `evidence/ERRATA.md`가 우선한다.

## 비교 판정과 비용의 해석

선택의 핵심 기전은 SC full-content provenance, MS local deselection, SG source-document scoped relocation으로 A/B 모두 같다: **달라진 핵심 선택0/3**. SC와 SG의 비교 후보 집합은 다르다(2/3). 그 자체도 모델 문맥 차이와 source-only 효과를 분리하지 못한다. 고정한 9개 입력·질문은 바꾸지 않았으므로 새 시험 입력0/9이며, 선택안의 핵심 예상 결과도 상충0/9이다. field 이름·세대 metadata·staging 설명까지 같은 구현이라는 뜻은 아니다.

원전별 설명과 거부 이유는 3/3에서 제공됐다. 이는 관찰된 텍스트 차이이지 교육 효과의 추정치가 아니다. 같은 상한에서의 기술 대조를 했을 뿐, 실제 문자수·구성 시간·추가 조사 비용이 동일하지 않다. 원 개발자의 채택이나 개발 시간 절감을 본 기록으로 말할 수 없다. 실제 historical PR 채택, 공개 원시험 source, 보조 실행과 미실행은 `TESTS.csv`의 서로 다른 열을 따른다.
