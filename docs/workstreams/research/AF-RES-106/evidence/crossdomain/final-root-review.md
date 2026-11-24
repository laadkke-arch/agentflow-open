# AF-RES-106 최종 root 산출물의 별도 대사

검토 시각·입력별 SHA-256·검사 항목은 [final-root-review.json](final-root-review.json)에 있다. 검토 시 Git HEAD는 `a9aea90170ad8d96d0e6fcb0513473902c7d2d80`이고, 이 문서는 그 위에 작성 중인 결과 파일을 읽은 검토다. 아직 결과 커밋의 계약 검사나 고정 GitHub 재열람 영수증이 아니다. 작성자의 결과를 알고 수행한 같은 계열 AI의 별도 대사이며 새 맹검 판독으로 세지 않는다.

## 결과

독립적으로 작성한 [review_root_artifacts.py](review_root_artifacts.py)의 **318/318 대사가 통과**했다. root의 `verify.py`, `recalculate.py`, `build_report.py`를 import하거나 그 출력만 믿어 통과시킨 검사가 아니다. CSV/JSON/Markdown을 직접 읽어 표의 값과 분모를 다시 계산했다. 별도로 원문을 읽은 Q7·최소 자료수 검토의 범위는 [review-final.json](review-final.json)과 [source-count-review.json](source-count-review.json)을 따른다.

| 검토 대상 | 독립 대사 결과 | 해석의 범위 |
| --- | --- | --- |
| RESULT 시작과 필수 표 | 첫 내용이 모집·예측 표. 순서대로 12쌍 자리·24판 자리·12반환 자리, 열 수 6/7/6 | 빈 자리도 표시하며 실제 8쌍·결원4를 구분 |
| 첫 표와 봉인 예측 | 12행의 사례, UTC, tree URL, 실제 행의 옛 절·임시 URL 일치 | 새 예측을 작성하거나 과거 예측을 고치지 않음 |
| 판별 표와 lineage | 실제16행의 고정 HTML line, 실제 DOM fragment, payload/source URL와 SHA-256 앞12자리, P/옛 경로 P/fragment/U/방법/G 일치 | 실제 렌더나 예제 실행을 입증하지 않음. G는16판 모두 `미확인` |
| 오류·반환 표 | 12행의 층 분모, 오류, 반환 결정, 고정 위치, 새 fragment, 문서/HTTP 비용, 결정을 바꿀 관측 일치. 비용 영수증 수와 파일 존재도 대사 | 기록된 조사 비용이며 후속 사용자의 보편 비용 추정이 아님 |
| 모집·선정 봉인 | 803행 중547적격. 모든 hash를 정확한 `ggplot2`/`Matplotlib` 문자열로 재계산. 각 층 hash/path순 앞2 일치. frame/predictions/SCOPE/EVALUATION_TARGETS가8054 봉인 bytes와 일치 | 547개 모두의 의미·첫 예제 경계를 새로 독립 판독했다는 뜻이 아님 |
| 원 목적 혼동표 | GG M/G 각각TP2. MP A FN2. MP G TP1/FP1. A(GG), M(MP)는 각 결원2 | 실제 양성7·음성1. 음성0층 FPR는 `산출 불가` |
| 일반 역할 혼동표 | MP G가TP2로 바뀌며 실제 양성8·음성0 | 원 목적에 대한 MP-G2의 NO를 사후 YES로 덮지 않음 |
| 원자료 최소량 | root670행 중 countable38 ID가 독립 allowlist와 정확히 일치. 고유 ID38, 직접 판독표시 모두 존재 | 38=본문15+별계보 그림/source6+공식사건10+IIIF5+JATS2. 같은 예제의 source/PNG나 merge를 추가 자료로 중복 산입하지 않음 |
| SELF_CHECK·끝 표 | Q1~Q7 모두 존재. RESULT 마지막은 지정 열의 정확한3행 표 | SELF_CHECK에 같은 마지막 표를 강제하지 않음; 사용자가 지정한 대상은 RESULT/최종 답/HANDOFF |
| reproduce | 522 source 검색과 후보5+5=10본문, 정확한 session/cloud 명령, 읽기 전용 검증과 파일을 갱신하는 복사본 재현을 구분 | 검토 시 실제 clean 결과 SHA 실행은 아직 예정 작업 |

최초 자체 스크립트 실행은316/318이었다. 원인은 검토자가 union CSV의 ggplot2 `signal_stratum`을 읽지 않고 Matplotlib의 `stratum` 열만 적용한 것이다. 검토 스크립트의 열 fallback만 고쳐318/318을 얻었다. 연구 입력·선정·결론은 변경하지 않았다. 이 교정은 JSON에도 보존했다.

## 원문과 결론의 대조

Q7의 최종 문구는 별도 원문 판독 결과와 맞는다. IIIF의 thumbnail과 painting body, Canvas의 painting과 commentary annotation을 나눈다. Fitzwilliam의17 Choice와32개 null 영역을 실제 viewer 성공으로 바꾸지 않는다. PLOS Fig7의 올바른 본문 xref4회는3개 문단이고, Table3 caption의 추가 참조1개에서 Ncut/Nassoc 의미 충돌을 별도로 적었다. Fig8로 자동 교정하지 않으며 저자의 의도와 수정은 `미확인`으로 남긴다. JATS XML id와 발행 HTML id도 구분한다. 원자료 URL·보존 bytes·UTC는 [Q7 최종 판독](CROSSDOMAIN_FINAL.md)과 [재수신 영수증](review-network-receipts.json)에 있다.

MP-G2에 대한 중요한 한계도 결과에 그대로 드러난다. 같은 PNG 경로를 새 절이 계속 참조하므로 이것을 ‘옛 파일이 남았지만 새 절에서 미사용’ 반례라고 쓰지 않는다. 원래 Men/Women 점수 목적을 조건으로 FP이지만 grouped-bar 일반 역할을 조건으로 TP이다. 의미 음성은1개뿐이며, 그1개에 대한 층 내부1/1을 일반적인 거짓양성률로 추정하지 않는다. 엄격한 잔류·미사용 반례를 아직 못 찾았다는 약점, GG 미판독59개와 MP G 미판독470개, source-set와 일반 역할 정의의 경로/선택 노출 뒤 추가도 숨기지 않는다.

이 검토는 이전 Q7·자료수 독립 재열람에 더해 root 표/원장의 대응을 점검한 것이다. 주8쌍 전체를 다시 맹검 의미 판독하지 않았다. 과거5사례 별도 판독, 재개 A2/G2 검토, root의 결론을 안 상태의 원문 확인은 각자의 범위를 유지한다. 사람이나 외부 전문가의 검토는 수행하지 않았다.

## 요청한 문구 교정과 남은 절차

SELF_CHECK의 초기 ‘자료 접근 실패4회(편의 웹 리더 DisabledError)’는 전체 실패 횟수처럼 읽힐 수 있다. GG의4회와 별개로 [probe-failures.json](probe-failures.json)에 Q7 실패4회가 보존되어 있다: 웹 리더 Internal Error3회, 최초 일반 User-Agent GET의 HTTP403 1회. 부모 작업자에게 **GG 편의 웹 리더4회로 범위를 명시하고 Q7 probe를 따로 언급**하도록 요청했다. 모두 최소 자료수 산입0이므로38이나 혼동표 분모에는 영향이 없다. 최종 반영 여부는 SELF_CHECK의 결과판을 따른다.

검토 시 RESULT의 `VALIDATION.md`와 `HANDOFF.md` 상대 링크는 아직 생성 예정이었다. 다른 Markdown 상대 링크에는 누락이 없었다. 결과/SELF_CHECK 커밋 뒤 그 정확한 clean SHA의 workbench/session 검사와 공통 cloud 검사, 고정 GitHub 결과판·대표 근거·반환 fragment 재열람, 영수증 기록, 마지막 HANDOFF 단독 커밋이 남아 있다. 이 대사를 그 실행 영수증으로 대신하지 않는다.
