# 봉인본 정정표 — 입력/판독 원본은 변경하지 않음

## E1 · SC hash 설명

봉인 `SC-common.json` interface는 hash 입력을 “file size plus sampled first/last1MB”라고 요약했다. 실제 고정 `Util::getFileHash`는 **file size를 분기·seek에만 사용**하고 MD5 입력에는 첫·끝 각1,000,000바이트만 넣는다. 파일 길이 값을 별도로 hash에 넣지 않는다. `CASEBOOK.md`, 사후 보고와 보조 코드는 실제 구현을 따른다. 두 SC 판독에 같은 잘못된 설명이 주어졌으므로 원문의 정확한 전달이라는 기준에는 결손이다.

SC-X의 두 입력 길이는 같고 1MiB 블록의 양끝은 바뀌지 않으므로 이 정정은 봉인된 collision 예측을 바꾸지 않는다. 길이가 다른 입력까지 “size가 섞여서 구별된다”고 일반화하면 안 된다. 새 가변 길이 예는 봉인 9자리 밖이다.

## E2 · SG C1의 저자 귀속

봉인 `SG-common.json`의 C1은 reference와 target을 사이에서 나누는 조건을 requester-supported로 표시했다. 현재 본문만으로는 split 위치가 충분히 특정되지 않았고, 사후 댓글은 **둘이 함께 새 장으로 이동하는 경우**가 실제 실패였다고 좁혔다. C1의 일반적인 목표 “split 뒤 footnote 대상 보존”은 작성자가 지지하지만, 봉인 N/E의 구체적 사이 분할은 연구자 확장이다. `BRIEFS.jsonl`과 packet 원본은 역사적 봉인을 보존하기 위해 고치지 않았다. 이 정정표와 최종 표의 귀속이 해석상 우선한다.

## E3 · 실행 가능성과 관찰 시점

`<!--SPLIT-->`은 입력 명세의 위치 표식이며 Sigil의 실제 자동 split marker가 아니다. native marker는 `<hr class="sigil_split_marker"/>` 등이다. 원문을 바꾸지 않고 cursor 위치를 연결하는 harness가 필요하다. SG-E의 `Text/parts/` 이동은 0.9.17 native 이름/폴더 제약에 막혀 있다. MS-E의 selected flag/list는 생성 직후 관찰해야 하지만 봉인 명세의 checkpoint가 명시적이지 않다. SC-E의 지정 후보 순서와 “identity confirmation 없음”도 native directory enumeration/OK 동작으로 연결해야 한다. 이를 뒤늦게 보완한 실행 성공으로 세지 않는다.

## E4 · 원장 계수의 보수적 재분류

최초 자료 묶음 커밋은 이름이 다른 원저작21개를 등록했다. 검토에서 같은 프로젝트의 코드와 설명서 사이의 상관을 지적했다. 이후 모든 대상 제품의 코드/설명서를 일관되게 한 보수적 계보로 합치고, 별도 분야의 원저작3개를 직접 더 읽었다. 최종 named works24개, conservative lineages21개다. 같은 자료를 반복해서 수를 늘린 것이 아니며 기존 커밋을 소급 수정하지 않았다. `COUNTING.md`와 최종 `SOURCES.jsonl`에서 두 수준을 재계산한다.

## E5 · 재개에서 확보한 MuseScore tracker의 부분 캐시와 시간 순서

2026-11-23 재개 검토자는 https://musescore.org/en/node/281441 의 검색 서비스 캐시 본문 일부를 읽었다. 표시 저자는 ericfontainejazz, 작성 표시는2019-01-08 19:55(시간대 미확인), Reported version은3.0이고 본문은2.3.2에서도 발생했다고 보고한다. source에서 notes 선택 뒤 parts를 만들면 실제 Selection에 없으면서 선택색이 남는다는 재현이다. 표시된 첫 이력은2019-01-16 제목 변경이다. 검색 서비스는 crawl을1.3 years ago로 표시했고, 후속 두 open과 root의 두 재열람은403이었다.

따라서 당시 접근 실패 기록은 유효한 과거 관측이지만, 현재 모든 저자·본문·신고판 정보가 전혀 없다는 서술은 `부분 캐시 확보, 최초판·전체 이력·원 서버 fresh 접근 미확인`으로 갱신한다. v3.0.1은2019-01-16 PR 이전판이지만2019-01-08 원 tracker 이후판이다. `pre-request`는 PR을 기준으로 한 설명에만 한정하며 신고판3.0/2.3.2와의 동등성은 미검증이다. 봉인 target SHA·BRIEFS·reader는 바꾸지 않았다. 원 요구에는 여전히 undo/reopen·범위 밖 성부 보존이 확인되지 않아 주 모집0/3은 유지된다. 자세한 agent/UTC/cache 근거는 `resume-review-musescore.json`과 `resume-sources.jsonl`에 있다.

## E6 · 추가로 확인한 구현 경계와 관찰 혼동

- Shotcut `ProxyReplacePostJobAction::doAction`은 `MainWindow::replaceAllByHash`를 호출하며 playlist/timeline 등의 hash 기준 교체로 이어진다. A1/B-F의 producer-scoped publication을 구현하려면 이 경로와 downstream `replaceClipsWithHash`도 검토·변경 대상이다. 기존 후보의 심벌 목록만으로 구현 범위가 닫혔다고 하지 않는다. frozen p2는H_BLUE라 해당 경로 때문에 p2가 실제 변경됐다고 관측한 것은 아니다.
- SC-X A1은 rebuild 필요, B-F는 명시적 recovery decision 대기를 적었다. 핵심 mechanism이 같다는0/3 집계를 모든 정책·쓰기 순서의 동일성으로 넓히지 않는다. A의 자동재생성이 확정돼 있다고도 읽지 않는다.
- MuseScore `Element::curColor`는 `selected()` 외 `Note::mark()`와 drop-target/printing 조건에도 영향을 받는다. MS-E는 생성 직후 selected flag와 Selection list·관련 표시조건을 함께 관찰해야 하며 파란색만으로 선택을 판정하지 않는다.
- Sigil nested-folder move를 수용하려면 `AnchorUpdates` 외 `FolderKeeper`·`OPFModel`·import/reopen 경로를 바꿔야 한다. frozen SG-E의 지원 불가를 flat rename으로 대체하지 않는다.

이는 사후 코드 검토가 추가한 실행 전제이며 새 목표 실행·봉인 입력 변경이 아니다. 재개 검토 보고3개에서 고정 URL·심벌·검토 범위를 확인할 수 있다.

## E7 · TEI 절 명칭

TEI P5 4.8.0 `#TCAPWL`의 정확한 표제는 **13.1.4.3 The Witness List**다. 과거 SOURCES 일부의 Witness Information은 상위절 이름과 혼합됐다. 봉인 packet의 실제 발췌·anchor·판과 선택은 변경하지 않고 최종 RESULT·SELF_CHECK와 새 source correction evidence에서 바로잡았다.
