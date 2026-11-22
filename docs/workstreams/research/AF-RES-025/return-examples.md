# 실제 반환 예시 — 부분과 전체, 완결과 보류

조회일은 2026-11-22 UTC다. 아래는 봉인된 반환에서 고른 예시이며 이후 찾은 문서로 원 인용을 보강하지 않았다. ‘현재 조건부 제안’과 ‘최초 제안 시점의 이용 가능성’을 별도로 표시한다. 신규 대상 주 지표를 통과한 예시는 이번 실행에서 0개다.

## 부분 질문 Q11: 코드 밖 metadata를 실행 주체에 전달

최초 설계는 셀 metadata를 코드 문자열의 magic 문법에 주입하지 않고 실행 요청과 연결하고, 수신 커널이 실행의 입력으로 해석하거나 무시할 수 있게 하려 했다. `content.metadata`를 쓴 최초 예시를 현재 수신자의 root `message.metadata` 경계와 혼동하면 안 된다.

**실제 G의 첫 링크:** [ipykernel kernelbase.py](https://github.com/ipython/ipykernel/blob/main/ipykernel/kernelbase.py), `Kernel.execute_request` 관측 표시행3506–3578 및 `Kernel.do_execute` 표시행3643–3665. 자료 JP-C021, 슬롯 Q11-G-1, 후보 JP-K019, 가린 키 B-4f391993bf95.

반환 이유는 같은 메시지에서 code와 root metadata를 읽고, 호환되는 `do_execute` 하위클래스에 `cell_meta`로 전달하는 정확한 코드 경계가 보인다는 것이다. 이 사용 경계에서 P1(요청별 구조화 부가자료), P2(수신 실행 주체가 사용), P3(코드 문법과 분리)를 원 인용 한 URL의 두 절로 확인할 수 있다. 클라이언트가 실제로 root metadata를 보내며 하위클래스가 해당 인자를 받는 조건의 제안이다. 모든 커널 지원, 노트북 metadata의 자동 전송, 최초 `content.metadata` 예제의 무수정 호환을 뜻하지 않는다.

G의 나머지 원 반환은 [NBClient의 cell hooks](https://github.com/jupyter/nbclient/blob/main/docs/client.rst)(JP-C022, Q11-G-2)와 [Datalayer 실행 경로](https://jupyter-mcp-server.datalayer.tech/architecture/)(JP-C024, Q11-G-3)다. 전자는 실행을 둘러싼 callback을 설명하지만 원격 커널에 같은 구조화 metadata를 전달한다는 근거가 부족하고, 후자는 문서·셀 식별 및 backend 실행 경로만으로 해당 metadata 전달 전체를 입증하지 못해 보류했다. 순위와 인용을 사후 바꾸지 않았다.

**당시판:** 정확한 cell_meta 어댑터는 2023-11-21 PR1169와 v6.27.0에서 도입됐으므로 2021-04-22 당시에는 이용 불가다. 이 역사 근거는 `followups/jupyter/candidate-history.jsonl` JP-K019에 있으며 최초 반환에는 덧붙이지 않았다. 최초 문서는 Jupyter를 명시하지만 `ipykernel`/`cell_meta`라는 문자열은 없다. 따라서 ‘알려진 호스트의 새 부품’ 보조 지표 1건이며 당사자에게 이미 알려진 부품이었다고 추론하지 않는다.

**상위 1 링크 민감도:** 같은 파일의 두 절이므로 이 예시의 현재 완결 판정은 유지된다. 이것이 여러 URL로 만든 근거 묶음도 첫 후보 하나만 남기면 그대로 완결이라는 뜻은 아니다.

## 전체 질문 Q10: 바인딩부터 후속 클라이언트 연결까지

최초 설계 전체는 프로세스가 실제 사용할 포트를 바인딩해 확보하고, 시작 주체에게 그 주소를 돌려주며, 여러 프로세스·채널을 구별해 나중 클라이언트도 재사용하도록 연결정보를 노출하는 것이다. ‘빈 포트를 찾는 함수’만으로는 전체를 대체할 수 없다.

원 Q10-R은 세 후보에 네 URL을 붙여 최종 세 URL 상한을 넘겼다. 아래는 그 사실을 지우지 않는 **사후 세 URL 제한판**이며 새 실행 결과가 아니다.

| 남긴 실제 URL | 원 후보·위치 | 읽은 이유 | 전체 제안 판정 |
| --- | --- | --- | --- |
| [Node net.md](https://github.com/nodejs/node/blob/main/doc/api/net.md) | Q10-R-1, JP-K009; listening L400–402, server.address L413–429, listen(port) L557–567 | port0으로 실제 바인딩하고 배정된 주소를 조회하는 경계 | P1/P2의 부품 근거. P3까지는 미확인 |
| [Node v25.8.0 child_process](https://nodejs.org/download/release/v25.8.0/docs/api/child_process.html) | 같은 Q10-R-1; message L1026–1034, send L1218–1271, server object L1273–1314, IPC 제한 L756–757 | 확보한 주소 또는 서버 객체를 부모–자식 IPC로 전달 | 다중 채널의 영속 연결 기록과 늦은 클라이언트 재사용이 비어 있어 전체는 보류 |
| [PCP RFC6887](https://www.rfc-editor.org/info/rfc6887/) | Q10-R-2, JP-K010; §10.1 p33–34 L1827–1896 | 확보·매핑·회신·게시 순서의 설계 선례 | 적용 주체와 연결정보 계약의 차이를 명시한 조건부 비교. 전체 필수 묶음은 보류 |

원 Q10-R-3의 [TAPS RFC9622](https://datatracker.ietf.org/doc/html/rfc9622) §7.2–7.3은 네 번째 고유 URL이라 제한판에서 빈 슬롯이 된다. 원 후보·순위는 `returns-raw.jsonl`에 남아 있다. RFC9622는 January2025 판이며, 그보다 이른 draft의 기능 계보는 별도 미확인이다.

Node의 bind/address/IPC 일부는 v14.15.3(2020-12-17)에도 존재함을 후속 감사에서 읽었다. 그러나 프로젝트가 당시 존재했다는 사실로 전체 연결 수명주기의 부족한 P3를 채우지 않았다. **이 전체 질문에는 바로 채택할 완결 대안 링크를 확보하지 못했으며, 위 링크는 경계가 드러난 부품·설계 참고와 보류 사유로 반환한다.**

## 여러 문서가 필요한 부분 질문의 반례 Q01

Q01-G-1의 현재 제안은 [PyArrow large-type 읽기 옵션](https://arrow.apache.org/docs/dev/python/parquet/parquet_type_handling.html), [Java LargeBinary/LargeList 형](https://arrow.apache.org/java/main/reference/org.apache.arrow.format/org/apache/arrow/flatbuf/package-summary.html), [Arrow 구현·상호운용 상태](https://arrow.apache.org/docs/status.html)라는 세 URL을 필요로 한다. 저장된 Arrow schema가 없거나 목적 large형과 일치하는 입력이라는 조건도 붙는다. PyArrow 옵션 하나만 보여 주고 Java 경계까지 입증했다고 할 수 없다.

상위 첫 후보를 남기는 보조 분석에서는 세 문서 묶음을 유지하지만, 첫 URL 하나만 남기는 민감도에서는 필수 인용 전체가 없어 탈락한다. 현재 문서의 조건부 완결, 실제 Python→Java 통합 실행, 2GiB 초과 경계, 2021 당시 이용 가능성은 네 가지 다른 판단이다. 이 실행에서 뒤의 통합·큰 경계는 미실시, 정확한 옵션의 당시 이용 가능성은 후발로 확인됐다.
