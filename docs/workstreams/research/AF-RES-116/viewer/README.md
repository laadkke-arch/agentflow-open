# AF-RES-116 고정 문서 뷰어

이 도구는 문서 본문을 판독하거나 정답을 만들지 않는다. 고정된 문서 텍스트에서 독자가 실제 선택한 위치와 보인 내용을 기록한다. 브라우저 시험이나 사람 시험이 아니며, 같은 파일시스템에 있는 다른 자료의 접근을 OS 수준에서 차단하지 않는다. 독립 문맥 제공과 금지 파일 미열람은 호출자의 별도 증거가 필요하다.

## Corpus 입력

`schema: 1`, `documents` 배열을 받는다. 각 문서는 다음 구조다.

파일 확장자가 `.gz`이거나 gzip magic bytes로 시작하면 gzip을 풀어 JSON을 읽는다. `corpus_sha256`에는 압축을 풀기 전 실제 입력파일 바이트의 해시를 쓴다. 같은 내용의 plain JSON과 gzip JSON은 문서 표시가 같고 corpus 해시만 다르다. 재현용 corpus 압축은 `gzip mtime=0`으로 생성한다.

```json
{
  "id": "manual",
  "url": "https://example.invalid/manual.html",
  "version": "v1.0",
  "source_sha": "fixed-upstream-commit-or-file-sha256",
  "text": "Contents\n[p001] Operation\n\nOperation\nOriginal body.\n",
  "links": [
    {"id": "p001", "start": 9, "end": 25, "label": "Operation", "target_doc": "manual", "target_offset": 27, "fragment": "operation"}
  ],
  "anchors": {"operation": 27},
  "navigation_spans": [{"start": 0, "end": 25}]
}
```

위 JSON은 schema 설명용이며 실제 조사는 원문 매핑으로 생성해야 한다. `start`와 `end`는 Python 유니코드 문자열의 `[start:end]` offset이다. 해당 범위에 완전한 링크 ID와 원래 label이 모두 있어야 한다. `end`는 끝 문자 다음 위치다. ID는 corpus 전체에서 고유한 ASCII 영숫자·밑줄·하이픈 1–48자다. `open`, `next`, `again`, `back`은 예약 이름이다. 링크 토큰은 겹칠 수 없다. `target_doc`, `target_offset`은 이미 고정된 corpus 안에서만 이동한다. 외부 URL 입력은 받지 않는다.

Corpus 제작자는 실제 원문의 순서·앵커·링크 관계를 보존해야 한다. 도구는 링크 표지가 실제 공식 문서에 있었는지, HTML 텍스트 추출이 정확한지 자체 증명하지 않는다. 원 HTML·변환기·offset 매핑을 별도로 보존한다. `anchors`는 원 앵커 이름→평문 offset 매핑이다. URL/fragment는 이 매핑에서 재구성한 원문 위치이며 실제 HTTP 도착 관측이 아니다.

`navigation_spans`에는 실제 목차 영역과 삽입한 링크 ID 표기의 원문평문 범위를 지정할 수 있다. 겹치는 범위는 합집합으로 센다. `content_*`는 그 범위를 뺀 본문, `total_navigation_*`는 문서 목차/표기와 뷰어 헤더/푸터를 합친 비용이다. 이 둘은 항상 `display_*`와 합계가 같다. 과거 이름의 `body_*`는 목차도 포함한 전체 source slice, `navigation_*`는 헤더/푸터만 뜻하므로 의미상 본문/내비게이션 비교에는 앞의 disjoint 필드를 사용한다. `navigation_spans`를 제공하지 않으면 그 분류가 없었다는 플래그를 남긴다.

## 표시와 예산

매 개봉은 원문 평문 최대 1,350자와 짧은 문서 ID·판·offset 헤더 및 내비게이션을 표시한다. 헤더/내비게이션용으로 150자를 고정 예약한다. 실제 내비게이션이 150자보다 짧으면 남은 공간을 본문으로 채우지 않는다. 전체 표시량은 반드시 1,500자 이하다. 링크 토큰이 절단점에 걸리면 가능한 한 다음 구간으로 온전히 넘긴다. 원문은 삭제하거나 관련성 순서로 재정렬하지 않는다. 극단적으로 긴 토큰이 한 본문면보다 크면 토큰은 분할되어 클릭 불가이며 `partial_link_ids`에 기록된다.

`open`/`choose`의 stdout은 실제 표시 문자열 하나뿐이다. URL·체크섬·허용 행동 목록 등 추가 상세 메타데이터는 원장에만 남기므로 독자에게 숨겨진 목표 위치를 내보이지 않는다. 명령 완료·오류 안내는 문서 본문이 아닌 제어 응답이며 개봉으로 더하지 않는다. 거절된 행동은 원장에 남고 새 문서를 노출하지 않는다. `[back]`의 고정 표기는 이전 열람이 있는 경우에만 활성화된다. 첫 면의 `[back]`은 활성화되지 않는다.

첫 `open`을 포함해 최대 세 번이다. 보인 링크 ID, 현재 면의 `next`, `again`, 실제 이전 면이 있을 때 `back`만 허용된다. 앞 단계에서 보인 링크는 계속 기억한 선택지로 사용할 수 있다. 각 면을 읽은 뒤 `answer`를 기록해야 다음 개봉을 할 수 있다. 단계 답은 수정할 수 없다. 세 번 전의 종료는 명시적 `--stop`이어야 한다. 원장에는 완료하지 않은 조기종료 자리를 남긴다.

## 수신 CLI

공통 옵션은 하위 명령보다 앞에 쓴다. 예시의 폴더·corpus·ID는 실제 고정 입력으로 바꾼다.

```sh
python -B docs/workstreams/research/AF-RES-116/viewer/reader.py --session r01 init --corpus docs/workstreams/research/AF-RES-116/corpus.json --start-doc manual --reader-id fresh-context-r01
python -B docs/workstreams/research/AF-RES-116/viewer/reader.py --session r01 open --reason '공통 시작 문서의 목차와 처음 본문을 확인한다.'
python -B docs/workstreams/research/AF-RES-116/viewer/reader.py --session r01 answer --operation '현재 확인한 동작 또는 미확인' --preservation '현재 확인한 보존 성질 또는 미확인' --exceptions '반례 확인 또는 미확인' --disposition '보류' --citations-json '[{"quote":"실제 보인 짧은 원문","doc_id":"manual","start":0,"end":10}]'
python -B docs/workstreams/research/AF-RES-116/viewer/reader.py --session r01 choose --action p001 --reason '방금 목차에 표시된 동작 절을 확인한다.'
```

두 번째 면에도 `answer`, 이후 남은 예산에서 `choose`와 `answer`를 반복한다. 마지막은 `finish --summary '최종 답·근거·미확인'`. 조기 종료는 `finish --stop --summary '더 읽지 않은 이유와 남은 미확인'`. `answer --json '{...}'`으로도 operation/preservation/exceptions/disposition/citations를 한 번에 전달할 수 있다. disposition은 원 독자의 자유 텍스트이며 도구가 정답을 강제하지 않는다.

기본 원장은 `readers/<session>/events.jsonl`이다. `--sessions`로 다른 자기 경로를 지정할 수 있다. 입력 corpus와 뷰어 코드의 SHA-256을 init 시 고정한다. 이후 하나라도 바뀌면 이어 읽기를 거절한다. 각 JSONL 행은 이전 행의 해시를 포함한다. 파일 잠금 아래 순차 append한다. 이 해시는 변경 탐지이며 외부 시각 인증이나 암호학적 저자 서명이 아니다.

## 도달성 전수 열거와 증인 재생

```sh
python -B docs/workstreams/research/AF-RES-116/viewer/enumerate_paths.py --corpus docs/workstreams/research/AF-RES-116/corpus.json --start-doc manual --out docs/workstreams/research/AF-RES-116/reach/manual
python -B docs/workstreams/research/AF-RES-116/viewer/enumerate_paths.py --corpus docs/workstreams/research/AF-RES-116/corpus.json --start-doc manual --witness '["open","p001","next"]' --out docs/workstreams/research/AF-RES-116/reach/witness-1.json
```

`paths.jsonl`은 길이 1–3의 모든 실제 허용 행동열, 누적 알려진 링크, 각 단계 원문 구간과 표시 지문, 다음 허용 행동을 남긴다. `views.jsonl`은 고유 표시 문자열·전체 비용·원문 offset을 보존한다. `summary.json`의 `enumeration_complete`가 false이면 예산상 불가능이라고 판정할 수 없다. 기본 상한은 200,000개 경로 노드다. 전수 열거는 정확한 문서 위치의 가능성만 증명하며 충분한 근거 구간을 gold에 연결하는 판정은 별도다. 같은 위치라도 앞서 본 링크와 직전 면이 다르므로 경로를 합쳐 버리지 않는다.

`--witness`는 같은 렌더러와 허용 행동 검사를 쓰는 결정론적 위치 재생이다. 실제 독자의 새 선택·판단으로 기록하지 않는다. 이미 있는 출력 경로는 덮어쓰지 않으며 수정 실험은 새 경로에 저장한다.

## 검증

```sh
python -B docs/workstreams/research/AF-RES-116/viewer/test_reader.py
```

합성 문서 두 개로 전체 표시예산/Unicode·바이트, 숨은 링크/단계답/3개봉 제한, 같은 면의 동일 표시와 조기종료, 완전열거·증인재생·상한 미완료 표시, corpus·원장 변조 탐지, gzip 입력의 동일 표시/실제 입력바이트 해시를 확인한다. 합성 세션은 실행 중 임시 viewer 하위 폴더에 생성 후 지우고 영수증 `synthetic-checks.json`만 남긴다. 이 실행은 자연 18꾸러미나 54단계에 더하지 않는다.

UTC는 제공 환경의 시계다. command wall time은 함수 호출 시간이며 AI 또는 사람의 능동 독해시간이 아니다. 노출→단계답 사이와 전체 세션 wall duration에는 도구 호출·대기 시간이 포함된다. 사람 시간 절약은 추정하지 않는다.
