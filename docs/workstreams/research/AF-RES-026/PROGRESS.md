# AF-RES-026 진행

| 묶음 | 원격 커밋·확인 | 마지막 ID | 다음 첫 행동 |
| --- | --- | --- | --- |
| ① 원장·날짜·표집·판정 | cecbfb981b9a7ccfd59f7bc40a23445a19d020fa, SCOPE 원격 읽기 확인 | 내부 입력 021/022 | 최초 요청만 판독 |
| ②C curl 8건·24메시지 | 682b77f015e63ce05d6b6c2fcdc6348052c6d472, frozen-responses 원격 확인 | C08 | 전체 봉인 대기 |
| ②P PostgreSQL 8건·24메시지 | e6ab7fd35d163b6907c56800913945e79e8b0d11, frozen-responses 원격 확인 | P08 | 전체 봉인 대기 |
| ②S SQLite 8건·24메시지 | 7c901b8e89bcbb43318d04a523d46d232a696f4f, frozen-responses 원격 확인 | S08 | 전체 봉인 대기 |
| ② 전체 24건·72메시지 | 이 커밋의 evidence/t0-seal.json과 정본 initial/frozen-responses | S08/P08/C08 | 이 커밋을 원격에서 확인한 뒤에만 T1 열람 |

현재 원장 149행은 149개의 독립 질문을 뜻하지 않는다. 답장 metadata·상한 이후 미심사 항목을 분리 집계한다. S01 노출을 숨기지 않고 전체 24와 엄격 미열람 23을 나눈다. 계열별 판독자는 같은 사람이 T0/T1을 맡는 자기 점검이다.

CLI start --fetch는 manifest-cli.json에 성공 영수증을 보존했다. 최종 check는 결과 통합 뒤 실행한다. 원격 SHA가 없는 파일은 최종 근거로 간주하지 않는다.
