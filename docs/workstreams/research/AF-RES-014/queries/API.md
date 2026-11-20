# 질의 수집 영수증

- [metadata.json](metadata.json)을 고정 입력으로 쓴다. 61개(전체 28, 부분 33)를 모두 재생성했다. 최초판을 검증한 질문은 0개다. 해시는 AF-RES-011 고정 SHA의 요약을 정규화한 문자열에 대응한다.
- [api-attempts.json](api-attempts.json)의 직접 익명 요청은 Stack Exchange, HN Firebase/Algolia, Reddit, GitHub REST에 대해 프록시 CONNECT 403을 반환했다. 같은 호스트의 후속 요청은 최초 실패를 참조한다. Stack Exchange revisions는 같은 호스트의 확인된 정책 실패로 인해 송신되지 않았다.
- GitHub 연결 기능의 표준 이슈 API는 T052–T055의 본문을 반환했다. 네 이슈의 업데이트 시각이 최초 작성 시각을 지나며, 응답에 최초판 또는 본문 수정 이력이 없었다. 공개 이슈 화면의 현재 본문 길이도 API와 일치했다. 다음 표에는 본문·계정 정보를 저장하지 않았다.

| 질의 | API 문서 위치 | 최초 작성(UTC) | 최종 업데이트(UTC) | 판정 |
| --- | --- | --- | --- | --- |
| T052 | [이슈 1095](https://github.com/knolleary/pubsubclient/issues/1095) | 2026-10-14T10:01:26Z | 2026-10-20T19:17:30Z | 최초 판 미증명 |
| T053 | [이슈 15](https://github.com/rlemaigre/vue3-promise-dialog/issues/15) | 2023-11-24T19:02:12Z | 2026-11-10T09:28:05Z | 최초 판 미증명 |
| T054 | [이슈 546](https://github.com/mixelpixx/KiCAD-MCP-Server/issues/546) | 2026-11-14T12:01:37Z | 2026-11-15T16:44:33Z | 최초 판 미증명 |
| T055 | [이슈 7002](https://github.com/osTicket/osTicket/issues/7002) | 2026-10-26T20:22:09Z | 2026-10-30T09:51:26Z | 최초 판 미증명 |

T051은 이슈가 아닌 Discussions다. T056–T060에서는 최초 본문을 복원할 공개 버전 API를 확보하지 못했다. 업데이트 시각이 바뀌었다는 것은 본문 편집을 입증하지 않는다. 최초 판과 일치함도 입증하지 못한다.

고정 입력 재검증은 소유 폴더에서 `PYTHONDONTWRITEBYTECODE=1 python -m queries.generate`로 실행한다. 네트워크가 허용된 환경의 새로운 검증은 별도 체크아웃에서 `PYTHONDONTWRITEBYTECODE=1 python -m queries.generate --write-metadata`로 실행하고 새 해시와 출처 모드를 비교한다. 해시가 달라진 실행은 이번 고정 순위에 섞지 않는다.
