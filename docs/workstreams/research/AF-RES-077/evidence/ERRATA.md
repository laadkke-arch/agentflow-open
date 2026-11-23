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
