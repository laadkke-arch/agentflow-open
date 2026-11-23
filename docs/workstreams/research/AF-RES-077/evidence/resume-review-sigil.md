# AF-RES-077#2 — Sigil 사후 재검토

검토 대상 연구판: `2f7e07542b4a59839556e00c9e266179150b21a3`. 검토자: `/root/review_sigil` (같은 모델 계열의 새 사후 검토 문맥). 원래 모집자·A/B 판독자가 아니지만 전체 지시와 두 보기를 모두 본 상태다. 이 문서는 독립 눈가림 판독이나 새 실험 표본이 아니다. 마지막 외부 재열람 완료 확인: **2026-11-23T12:33:47Z**. 개별 요청의 시작/종료 시각은 계측하지 않았으므로 이 시각은 일괄 완료 상한이다.

## 판정

기존 사후 기록의 **PARTIAL**, `SG-E=TARGET_NOT_RUN_NATIVE_ACTION_UNSUPPORTED`, `SG-N/SG-X=TARGET_NOT_RUN_HARNESS_INCOMPLETE`를 지지한다. 새 실제 목표 프로그램 실행은 **0**이다. 봉인된 입력·판독 파일은 수정하지 않았고 5개 파일을 해당 봉인 커밋과 바이트 대조해 모두 일치했다.

별도 최종 수정이 필요한 새 코드 오류는 찾지 못했다. 다만 결과 보고서에는 아래 세 구분을 유지해야 한다. 과거 모집/BRIEFS의 좁은 귀속을 그대로 옮기면 안 된다.

1. **원요구와 봉인 입력의 분리:** #450의 실제 실패는 reference와 target이 함께 새 장으로 옮겨지고 자기 파일명을 담은 href가 옛 파일명을 유지하는 경우로 좁혀졌다. 봉인 SG-N/E는 둘 사이를 나누므로 그 회귀를 대표하지 않는다. `BRIEFS.jsonl`의 SG-C1 “when splitting separates the reference and target”와 모집 보고서 P1의 직접 저자 귀속은 `ERRATA.md:E2`의 적용을 받는다. 최종 표1/Q1에서는 일반 목표만 저자 지지라고 하고, 구체적인 사이 분할·동명 ID 두 장·하위폴더 이동은 연구자 확장으로 쓴다.
2. **예측과 실행 가능성의 분리:** SG-E를 두 안 중 하나가 통과했다고 쓰지 않는다. 기존 0.9.17의 native 폴더/rename 표현으로 `Text/parts/ch1_tail.xhtml`을 만들 수 없다. 새 구현으로 이 동작까지 지원하려면 AnchorUpdates 외에 FolderKeeper·OPFModel·import/reopen 경로도 바뀌어야 한다. 봉인 판독의 “move caller unknown”은 실제 구현 부담의 결손이다.
3. **전이와 원전의 분리:** A-C1과 B-scoped는 둘 다 operation-local `(original document, fragment)` 대응을 선택했다. B의 “digest catalog”는 연구자가 비교용으로 만든 가설이지 OCFL이 권고한 Sigil 구현이 아니다. 관측된 핵심 선택 차이는 **0/1 비교**, native 효과는 **0/3 실행**이다. 저장 순서·거부·rollback은 원전에서 보장되지 않는다.

## 직접 원문 재대조

| 원문 / 판·절 또는 심벌 | 다시 확인한 내용 | 적용 한계 |
|---|---|---|
| [Sigil #450](https://github.com/Sigil-Ebook/Sigil/issues/450), 현재 본문 | gennaios의 자기 파일명 포함 링크가 split 뒤 원래 파일/첫 split을 가리킨다는 보고. created 2019-08-10T23:45:39Z, 49 comments. | 최초 편집판·정확한 reporter build 없음. 현재 body가 최초판이라는 주장을 하지 않는다. |
| [Doug Massay 520258201](https://github.com/Sigil-Ebook/Sigil/issues/450#issuecomment-520258201), 2019-08-11 | 사이 분할은 동작했고 href 자체가 새 파일로 이동해야 실패했다는 구분. | 당시 개발자 보고. 이번 실행 영수증이 아니다. |
| [Kevin Hendricks 520259623](https://github.com/Sigil-Ebook/Sigil/issues/450#issuecomment-520259623) | `file_id==resource_filename`인 새 파일 내 target 때문에 수정 분기에 들어가지 않는 debug 설명. | 댓글 붙여넣기 로그; 독립 CI 또는 native 실행으로 세지 않는다. |
| [0.9.17 tag object](https://api.github.com/repos/Sigil-Ebook/Sigil/git/tags/add8e4126dd33776e83f2faea66abaaccb29b4a1) | commit `30419827123d533d10ad482b1634dcec05ff0e1b` 연결. | 운영상 고정판이며 저자 설치판 증거가 아니다. |
| [AnchorUpdates.cpp](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/SourceUpdates/AnchorUpdates.cpp), `GetIDLocations`·`UpdateAnchorsInOneFile`·`UpdateExternalAnchorsInOneFile` | ID→filename hash의 뒤 항목 덮어쓰기, 다른 파일일 때만 갱신하는 기존 분기, 외부 chapter의 originating filename 필터. | 순서·분기 소스 확인. Gumbo/Qt/GUI 실제 동작 관측은 없다. |
| [repair ae60e3e](https://github.com/Sigil-Ebook/Sigil/commit/ae60e3e63a2f9343b40d316f179b9dfbcb6d838b) | 1파일 수정. same-file이고 href base에 파일명이 없을 때 `#fragment`로 바꾸는 분기 추가. | 회귀 테스트·nested-folder 지원·document identity 일반 해법의 추가가 아니다. |
| [FolderKeeper.cpp](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/BookManipulation/FolderKeeper.cpp), `AddContentFileToFolder`; [OPFModel.cpp](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/MainUI/OPFModel.cpp), `FORBIDDEN_FILENAME_CHARS` | HTML 고정 Text 폴더 배치; category folders 비편집; 파일명에 slash/backslash 거부. | 사용자 플러그인·외부 ZIP 수정까지 일반 금지한다는 뜻은 아니다. 그런 조작은 봉인 native 사례와 다르다. |
| [XhtmlDoc.cpp](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/BookManipulation/XhtmlDoc.cpp), `BREAK_TAG_SEARCH` | 실제 자동 split marker는 해당 class의 hr 태그다. | `<!--SPLIT-->`을 실제 marker라고 주장하지 않는다. cursor harness는 별도 명세가 필요하다. |
| [ExportEPUB.cpp](https://github.com/Sigil-Ebook/Sigil/blob/30419827123d533d10ad482b1634dcec05ff0e1b/src/Exporters/ExportEPUB.cpp), `WriteBook`·final-file copy | SaveAllResourcesToDisk 후 임시 publication/archive를 만들고 실제 파일을 WriteOnly/Truncate로 열어 복사한다. | 관찰된 crash 결과는 없다. 원자적 저장을 보장하는 코드라고 읽을 수 없다. |
| [OCFL 1.1](https://ocfl.io/1.1/spec/#manifest), §§3.5.2·3.5.3.1, Introduction Note | digest가 physical content paths와 version logical paths를 연결하며 여러 경로가 같은 digest를 공유할 수 있다. 명세는 object-at-rest를 다룬다. | fragment target/역연산/중단 복구 프로토콜을 제공하지 않는다. 2022 판·2024 update이며 2019 저자의 당시 노출 자료가 아니다. |
| [EPUB 3.3, 2023-05-25](https://www.w3.org/TR/2023/REC-epub-33-20230525/#sec-container-iri), §4.2.5 | XHTML의 base가 HTML 기준이며 통상 content document URL이라는 동종 설명. | 실제 Sigil 수정·유일 target 판정·transaction 구현을 제공하지 않는다. 2019 contemporaneous 원문으로 제시하지 않는다. |

현재 공개 원문 재열람은 GitHub **10회**, web 도구 **4호출/7명령**(open 2, find 5)이다. HTTP 도구 오류는 없었고 OCFL find 2건은 문구 일치 없음이었다. 모두 이미 등록된 원저작의 재열람/메타데이터이며 독립 원저작 수 증분은 **0**이다. URL·분류·내용 한계는 동명 JSON에 기록했다.

## 원본 EPUB와 입력·출력 구분

커밋된 `postseal/sigil/originals/test_split2.epub`을 Python zipfile로 다시 열었다. SHA-256은 `244dc0107a2cb1ad17ef2bf80c858e90e3b7396a63bb78869ae024206d6aa7df`로 기존 기록과 일치했다. `OEBPS/Text/Section0001.xhtml`의 실제 marker는 reference와 target 앞에 있고, href `../Section0001.xhtml#here`의 단순 상대 경로는 존재하지 않는 `OEBPS/Section0001.xhtml`을 가리킨다. 대상 파일 자체는 `OEBPS/Text/Section0001.xhtml`에 있다.

이것은 **정적 원자료 archive 검사**이며 native import·split·저장·재열기 실행이 아니다. fixture의 import 이후 문자열·정규화 동작을 독립 관측한 것으로 쓰면 안 된다. 원래 archive를 고치거나 새 golden output을 만들지 않았다. 2019 당시 attachment bytes와 현재 공개 bytes의 동일성은 당시 해시가 없어 미확인이다.

## 다음 첫 행동과 필요한 입력

원 봉인 9자리의 분자·분모는 유지한다. 새 후속층을 시작할 때 첫 행동은 **native 고정판에서 지원되는 동작을 먼저 명세**하는 것이다. SG-E의 하위폴더 요구를 조용히 flat rename으로 바꾸지 않는다. 새 입력에는 별도 ID·새 봉인이 필요하다.

1. 현재 source SHA의 실행환경(기록된 Linux build 문서의 QtWebEngine 포함 Qt5, CMake, C++ 및 Python 의존성)을 준비하고 전체 버전/빌드 로그를 남긴다. 아직 설치·빌드하지 않았다.
2. source 디렉터리 `sigil-src`를 `30419827123d533d10ad482b1634dcec05ff0e1b`로 고정하고 sibling `sigil-build`에서 문서 명령을 실행한다:

```sh
cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release ../sigil-src
make -j4
```

3. 원 attachment를 그대로 import하고 **import 직후 href·실제 resource path·ID**, split 직후, 저장된 EPUB, 재열기 뒤의 네 관찰점을 기록한다. 동일 archive에 대한 후대 repair SHA 대조는 별도 실행으로 표시한다.
4. 연구자의 문서별 `fn` 두 개 사례는 동일 target 내용과 별도 chapter scope를 관찰하되, 새 native 동작 명세 없이 실행 성공으로 집계하지 않는다. 같은 문서의 duplicate IDs는 기존 의도를 알 수 없는 음성대조로 남긴다.

재현할 자동 anchor-test 명령은 확보하지 못했다. 위 configure/build 명령은 행동 시험 명령이 아니다. 이번 검토로 새 PASS/FAIL·역사적 채택·시간 절감·독립 효과 증거는 추가되지 않았다.

