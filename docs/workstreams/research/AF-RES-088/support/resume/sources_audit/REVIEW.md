# AF-RES-088 #2 — 자료·타 분야 대조 재개 검토

검토 종료 체크포인트: 2026-11-23T15:38:59.772502Z. 검토자: `/root/resume_sources`.

기존 결론과 자료 원장을 읽은 뒤 수행한 **동일 팀의 재개 자료 검토**다. 독립 맹검 후보 판정, 독립 평가자 일치도, 60개 모집 본문의 새 독립 재판독으로 세지 않는다. 주파일·기존 판정·Git 이력은 변경하지 않았다. 이 디렉터리의 재열람 35행은 모두 `count_primary=false`이며 자료·사건 수를 늘리지 않는다.

## 판정

**자료량·Q7 타 분야·플랫폼 근거 게이트는 충족한다.** 재집계 대상 `sources.jsonl`의 SHA-256은 `b78b9e21072e61829b7568bfda08ce5bb49e38e4f27b24801b6fc3c309ecf66f`다. 185기록 중 원자료 단위 120개, 독립 저작·사건 87개로 기존 수치와 일치한다. 질문별 event ID는 모집·후속판·답에서 일관되며, 같은 질문의 답 수로 독립 사건을 늘리지 않았다. API 재표현·댓글·동일 URL 재열람 제외도 최종 원장에 반영되어 있다.

| 게이트 | 확인한 분모·범위 | 결과 |
| --- | --- | --- |
| 원자료 24개 이상 | 최종 원장 120개; 회복 초안의 원장 구조와 계산을 직접 확인 | 충족 |
| 독립 저작·사건 20개 이상 | 87개; 서로 다른 질문 60개와 별도 해법 삽입 대조 1개가 동일 사건 ID 규칙을 사용 | 충족 |
| 선정 SO 원사건 8개 | JN1/JN2/JE1/JE2/PN1/PN2/PE1/PE2가 각기 기존 원문·판·답 원장에 연결됨 | 자료 연결 확인; 의미 재판독은 다른 검토 범위 |
| CLI 6개 이상의 독립 자료·사건 | 기존 12자료/9저작·사건; 이 검토에서 그중 8개 공식 원자료를 고정 SHA로 다시 읽음 | 충족 |
| IETF 실제 판 쌍 2사건 | QUIC transport-27→28, TLS13-27→28 및 각각 후속 인용 | 2/2 |
| 프리프린트 실제 판 쌍 2사건 | Attention v1→v2, Kalb–Ramond v1→v2 및 각각 후속 인용 | 2/2 |
| 첫판·편집·채택 원정책 | revision schema/endpoint/filter/paging, 2022 정책판26, accepted-answer Help, 제목-only·롤백 대조 | 실제 원문과 API로 재확인 |

이 판정은 전체 연구를 `REVIEW_READY`로 올리는 근거가 아니다. PE1 옛 이미지와 후보 적용의 미확인 등 남은 필수 비교 근거는 부모의 최종 검토 대상이다.

## Q7 네 사슬의 실제 대조

| 사건 | 재열람한 원판·다음판·후속 인용 | 확인된 범위와 유지할 제한 |
| --- | --- | --- |
| QUIC | [transport-27](https://www.ietf.org/archive/id/draft-ietf-quic-transport-27.html), [transport-28](https://www.ietf.org/archive/id/draft-ietf-quic-transport-28.html), [ATSSS-00](https://datatracker.ietf.org/doc/html/draft-bonaventure-quic-atsss-overview-00) | §14의 Initial 최소 payload는 두 판 모두 1200이다. 초과시 전제는 -28에서 path와 peer를 함께 적는다. 후속 초안은 transport-28을 명시한다. 실제 구현·패킷 관측은 아니다. |
| TLS | [tls13-27](https://datatracker.ietf.org/doc/html/draft-ietf-tls-tls13-27), [tls13-28](https://datatracker.ietf.org/doc/html/draft-ietf-tls-tls13-28), [rfc8447bis-00](https://www.ietf.org/archive/id/draft-ietf-tls-rfc8447bis-00.html) | binder 검증 실패시 handshake 중단 규칙은 유지된다. E.6은 Static RSA에서 새 PSK identity 노출 설명으로 바뀐다. 후속 참고문헌은 -28과 날짜를 지정한다. 절 번호만 보관하면 조건 출처가 어긋날 수 있다. |
| Attention | [v1 PDF](https://arxiv.org/pdf/1706.03762v1), [v2 PDF](https://arxiv.org/pdf/1706.03762v2), [v2 metadata](https://arxiv.org/abs/1706.03762v2), [BERT v1](https://arxiv.org/html/1810.04805v1) | v1 abstract 41.0/3.5일, v2 abstract 41.2/4.5일·본문 41.17·Table2 41.0을 추출 텍스트로 확인했다. BERT는 2017 출판본과 구현을 인용하며 특정 preprint판을 지목하지 않는다. 따라서 후속 인용을 v1/v2 실사용판으로 확정할 수 없다. |
| Kalb–Ramond | [v1](https://arxiv.org/html/2401.14452v1), [v2](https://arxiv.org/html/2401.14452v2), [정정 metadata](https://arxiv.org/abs/2401.14452), [fluid v1](https://arxiv.org/html/2406.01412v1) | v1 amplitude 한계 절과 v2 최저차수 phase-only 설명·해당 절 부재가 대비된다. 후속 fluid 논문은 더 넓은 parity 위반 주장을 인용한다. v2 정정으로 그 후속 인용 전체가 틀렸다고 할 수 없다. metadata의 출판 erratum은 진행 중 진술이다. |

[BERT v1 제출시각](https://arxiv.org/abs/1810.04805v1)은 2018-10-11T00:50:01Z, [fluid v1 제출시각](https://arxiv.org/abs/2406.01412v1)은 2024-06-03T15:12:42Z다. arXiv의 [공식 정책](https://info.arxiv.org/help/versions.html)은 이 시각을 제출 완료 조작의 시각으로 정의한다. 실제 독자의 독서시각이나 즉시 공개시각으로 바꾸어 해석하지 않는다.

## 플랫폼 재확인과 실패 경로

공개 정책 revision26 URL과 두 Meta 공개 이력 URL은 이번 웹 재열람에서 inaccessible이었다. 실패는 `attempts_audit.jsonl` 3행에만 남겼고 원자료 수에 넣지 않았다. 공식 공개 API가 모두 성공하여 정책판26과 제목-only·롤백 대조를 확인했다. 기존 보존판을 현재 페이지로 대체하지 않았다.

`platform_recheck.json`의 8개 확인값이 모두 true다. 정책판26의 GUID·UTC·본문 SHA는 기존 기록과 같았다. 302285의 판2에는 제목 필드만 있고, 판3의 `last_body`는 판1의 본문과 같았다. 17038 판3은 새 GUID/UTC의 rollback이며 판1 본문을 복구한다. 판34–37은 HTML 지문이 2개지만 보조 텍스트 정규화 지문은 1개다. 후자는 이 사건의 표현 변화 보조 확인이며 일반 의미동일 판정기가 아니다.

## 정정할 표현 한 곳

`support/solution_insertion_control.md`는 원시 원장에서 `count_primary=true`인 3행을 원자료 수로 설명한다. 그러나 `assemble_sources.py`는 그중 댓글 `CTRL-SOL-05`를 보수적으로 제외하므로 **최종 집계는 2개**다. 최종 `sources.jsonl`·`metrics.json`의 120/87은 이 제외를 이미 반영한다. 따라서 수치를 바꾸지 말고 보조 문서 문장을 “원시 후보 3행 중 댓글 1행을 제외해 최종 원자료 2개”로 맞추는 것이 적절하다. 원사건은 어느 집계에서도 1개다.

## 파일과 재사용

- `sources_audit.jsonl`: 실제 재열람 35행, 확인한 절·UTC·관측주체·한계·기존 source ID 연결. 모두 최종 최소량의 추가 계수에서 제외한다.
- `count_audit.json`: 검토한 원장 지문과 수량·게이트 스냅샷.
- `manual_receipts.json` 및 고정 원자료 `.txt`: 8개 공식 자료의 URL·HTTP200·SHA256·수신 경로. 전체 파일을 받은 경우에도 읽은 범위는 행 기록에 한정한다.
- `policy_receipt.json`, `platform_controls_receipt.json` 및 대응 JSON: 공개 역사 API 응답과 지문.
- `platform_recheck.json`: 원장 주장과 새 API 값의 8개 대조 결과.
- `attempts_audit.jsonl`: 실패한 웹 이력 경로 3개와 성공한 API 대안.

재열람 35행을 주원장에 병합하더라도 최소량 기여는 0이다. 기존 단계의 120개 원자료·87개 독립 저작을 새로 155개·122개로 늘리지 않는다. 이 검토는 원래 8자리·32쌍의 모집이나 사전 판정을 수정하지 않았다.
