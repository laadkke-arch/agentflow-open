# Arrow 원장 · 입력과 검색 봉인 준비

`questions.jsonl`의 Q01–Q04는 2021년 최초 제안 메일 전문에서 출발한 부분2·전체2 설계 질문이다. `queries.jsonl`은 동일 전문 해시로 G/R 각3개 질의를 사전 고정한다. 후보 검색은 root가 원격 봉인 SHA를 확인하기 전에는 실행하지 않는다.

- `frame.csv`: 공식 월별 mbox의 비회신 제목·날짜 심사335행. 4선택, 제외, 상한 뒤 보류를 보존한다. 메타데이터 내용의 발행시각은 작성자 Date 헤더이며 독립 서버시각으로 승격하지 않는다.
- `SAMPLING.md`: 새 설계의 경계, 단순 사용지원/오류수정/첨부누락의 제외, 상한 뒤 초기본문 노출의 한계.
- `input-metadata.json`: 원 Message-ID, HTML/raw 주소, 월별 원장 위치, 디코딩 본문 해시.
- `restore_inputs.py`: 원격 원문을 다시 읽어 같은 G/R 입력 바이트를 복구한다. 원문 전문은 `cache/inputs/`에만 두며 Git 커밋에서 제외한다.
- `sources.json`: 선택한 최초 원문4건과 표집 보조/탈락 원문14건. 최소수 산입은4건이며 동일 원문의 mbox/raw/HTML은1건이다.
- `exposures.json`: 원질의 작성 전의 후속 snippet·동일사건 심사 노출. 초기본문의 침묵은 제안자의 미인지로 판정하지 않는다.

## 복구 명령과 정규화

저장소 루트에서 Python3 표준 라이브러리와 공개 HTTPS 접근으로 실행한다.

```sh
python docs/workstreams/research/AF-RES-025/streams/arrow/restore_inputs.py
```

MIME를 `email.policy.default`로 해독하고 `text/plain` part 전체를 개행 하나로 연결한다. 단일 plain message는 전체 body를 사용한다. 단일-message raw endpoint가 월별 mbox에서 보존한 맨 끝 LF를 생략한 경우, LF 하나를 붙여 **봉인한 SHA256과 정확히 일치할 때만** 복구를 수락한다. 나머지 공백·문구는 바꾸지 않는다. 다르면 실패하며 현재 본문으로 봉인 해시를 갱신하지 않는다. Q03에서 실제로 terminal LF1개 차이를 관측했다.

메일 전체의 재배포 라이선스는 확인하지 못했다. 공개아카이브라는 이유만으로 허가를 가정하지 않고 원문은 내부 읽기 캐시, 원격 결과는 원주소·해시·복구 코드·짧은 판독 요약으로 구성한다. G/R에는 같은 전문이 실제로 입력되며 복구 방식이 상이한 요약 입력을 뜻하지 않는다.

Q04의 링크된 README는 가장 이른 reachable commit에서 제목·목적만 있었다. 고정된 첫 메일의 구체 API/요구 전문을 입력으로 사용하며 메일 당시 외부 branch head 전체를 복원했다고 주장하지 않는다. 이후 판정에서 이 제한이 중요한 경우 해당 조건은 미확인으로 남긴다.
