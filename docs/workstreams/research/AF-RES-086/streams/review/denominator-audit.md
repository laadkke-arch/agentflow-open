# AF-RES-086 독립 분모·자료량 감사

검토자: preservation 담당자의 추가 독립 검토. 검토 UTC: 2026-11-23T15:18:43.748981+00:00. 쓰기 범위는 이 파일 하나이며, 원장·설정·git은 수정하지 않았다. 공개 자료를 새로 조회한 감사가 아니라, 네 stream 원장 전체·관련 영수증/추출·사건 규칙·경로 원장·판 쌍 목록을 재열람하고 산술과 해석을 교차 검사했다.

## 1. 자료 최소량: 집계 일치, 행과 저작은 분리

| stream | 전체 원장 행 | 적격 직접 원문 행 | 제외 행 | 합쳐 센 계보 |
|---|---:|---:|---:|---:|
| python | 58 | 37 | 21 | 3 |
| r | 73 | 46 | 27 | 3 |
| incidents | 42 | 19 | 23 | 12 |
| preservation | 28 | 24 | 4 | 7 |
| 합계 | **201** | **126** | **75** | **25** |

적격 여부는 각 stream의 `countable_original`, `primary_count_eligible`, `counts_original` 중 실제 존재하는 필드로 계산했다. 적격 126행의 source ID와 정확한 URL은 각각 모두 고유했다. URL fragment 제거·query 순서 정렬 후 URL+판/절을 비교해도 중복은 0쌍이다. 적격 행의 영수증 경로 126/126이 존재했고, 직접/저장 payload SHA-256 필드도 126/126에 있었다.

다만 **126행은 독립 저작 126개가 아니다.** 다음 3쌍은 payload SHA-256가 같으며 시간·단계가 다르다. HTTP 단계를 보존하되 최소 자료량을 보수적으로 적을 때는 각 쌍을 한 번만 세면 **123개 고유 payload 지문**이 된다. 이 재집계로 계보 25는 변하지 않는다.

| 같은 바이트를 받은 적격 행 | 직접 SHA-256 | 두 행을 보존하는 이유 |
|---|---|---|
| `PY-P3-LEGACY-NOW` / `PY-CAP-LEGACY-20251114` | `5fae3b9eaad47ef3d274e1824196809e817473331dbac71e2d5263946bb77eff` | 현재 응답과 2025-11-14 보관 응답은 서로 다른 관측이다. 주창 동시성의 추가 증거는 아니다. |
| `R2-CURRENT-ROOT` / `R2-GENERATED-ROOT` | `cd5bab13fd944d99cae00a71e1877d1c140c527cfbea5a9a2d258d0525c2d6f0` | 독자 root 응답을 고정 생성 커밋의 파일과 비교했다. |
| `R2-CURRENT-LEAF` / `R2-GENERATED-LEAF` | `c812426f5a97f8361e64a7a3beb8a35d5dde4bd2270b70dc1f1567080471ca0c` | 독자 leaf 응답을 고정 생성 커밋의 파일과 비교했다. |

같은 빌드의 API v2/v3와 목록/상세, 같은 배포의 객체와 statuses, 같은 사건의 이슈·댓글·수정 커밋·후속 HTTP는 바이트가 달라도 독립 저작이 늘어난 것이 아니다. 이 때문에 payload 개수와 별도로 아래 계보 집계를 유지해야 한다. 압축 전송과 해제 HTML 지문도 서로 다른 hash domain이므로 한꺼번에 내용 중복 판별값으로 섞지 않았다.

| 계보 집합 | 계보 수 | 합산 규칙 |
|---|---:|---|
| 고정 소비자 cibuildwheel·bandersnatch·archive·asciicast | 4 | 각 소비자의 요구·소스·빌드·산출물·현재/보관 응답을 한 계보로 합침 |
| RTD 플랫폼 문서/코드, GitHub Pages 계약 | 2 | 한 플랫폼의 도움말 페이지를 각각 새 계보로 세지 않음 |
| 관련 사건 first12의 8개 + supplement4의 4개 | 12 | Typst 파생 조사 전체를 deploy-pages#383 안에 합침 |
| 보존 실례 Matplotlib·UMAP·GNU hello·Gitorious·Zenodo 철회 레코드 | 5 | 같은 저작의 두 판·파일·manifest는 한 계보 |
| Zenodo 정책·Software Heritage API 계약 | 2 | 실제 판 쌍과 별도인 제도 설명 계보 |
| 합계 | **25** | 정책 계보 4개를 전부 제외해도 실례·사건 **21계보** |

따라서 원자료 24개와 계보 20개 최소량은 충족한다. 이는 빌드·게시·당시 응답의 결손을 메우는 판정이 아니다. 본 감사는 출처 최저량 충족을 근거로 REVIEW_READY를 만들지 않는다. 원문 접근 실패·빈 검색·URL 제목뿐인 결과와 byte 중복 미러가 독립 자료량을 늘리지 않도록 원래 제외 플래그를 유지한다.

## 2. 사건 표본: 층화 first12와 supplement4를 별도 유지

근거: `streams/incidents/PROTOCOL.md`, `incidents.csv`, `NOTES.md`, `sources.jsonl`.

프로토콜은 2024–2025 created 이슈를 네 저장소에서 각각 같은 검색식으로 조회하고 **저장소별 최초 3개**를 선택한 뒤, 선택된 12개를 생성 UTC와 이슈 번호 순서로 판독하는 방식이다. 전 세계 사건의 최초 12개나 네 저장소를 한꺼번에 합친 전역 최초 12개가 아니다. 서버 요청은 병렬이었으므로 HTTP 요청까지 시간순이었다고도 서술하면 안 된다. RTD 후보 조회 상한 30은 문서에 남아 있다.

| 집합 | 직접 읽은 고유 사건 | 관련 사건 | 완결 강한 반례 | 제외/미완결 처리 |
|---|---:|---:|---:|---|
| first12 | 12/12 | 8/12 | **0/12** | RTD10990·11042, mike202, MkDocs3579의 4개는 원문을 읽었지만 관련 최소량에서 제외 |
| supplement4 | 4/4 | 4/4 | **0/4** | RTD11531, mike229, deploy-pages383, mike248; first12의 탈락 사건을 대체하지 않음 |
| 관련성 계보 합산에만 사용 | 16개 중 12개 | 12 | 강한 반례의 합성 성공률을 만들지 않음 | 19 적격 증거 행은 12 사건 계보에 귀속 |

특히 supplement RTD11531(2024-08-08)는 first12의 마지막 사건들보다 생성일이 빠르다. 이는 저장소별 최초 3개라는 층화 규칙과 양립한다. 보고서에 그 규칙을 생략하면 사후 표본 교체로 보일 수 있다.

강한 반례 0은 라우팅 장애 0이라는 뜻이 아니다. Typst는 생성물·게시 성공·옛 catalog 응답을 연결했으나 회복 뒤 기대 catalog 지문이 없다. MESA와 mike229는 표시 이름 차이가 판 차이라는 추론을 약화시키지만, 연구자가 당시 두 응답을 동시에 받은 실험은 아니다. 현재 MESA·Typst 응답과 Typst 후속 자료는 기존 사건의 추가 증거이며 새 계보가 아니다. 2026 댓글을 2024–2025 결과로 편입하지 않는다.

## 3. 타 분야: 두 기관, 세 판 쌍, 여섯 실제 판 기록

근거: `streams/preservation/pairs.json`, `NOTES.md`, `sources.jsonl`.

| 기관·저작 | 판 쌍 / 실제 기록 | 양쪽 파일 또는 manifest 직접 판독 | 경계 |
|---|---|---|---|
| Zenodo·Matplotlib | v3.1.0 record2893252 / v3.2.0 record3695547 | 양 레코드의 ZIP명·크기·발행자 MD5 manifest | ZIP을 다운로드하지 않았으므로 MD5 직접 검증으로 쓰지 않음 |
| Zenodo·UMAP | 1.0.0 record60943 / 1.1.0 record800648 | 양 tar 다운로드, MD5 일치, 내부 setup.py 판과 245/263개 archive entries 확인 | concept705645가 현재800648로 이동하는 사실은 당시 alias 상태의 증거가 아님 |
| Software Heritage·GNU hello | 2.9 revision55c14d… / 2.10 revisiondbdaa3… | 양 내부 directory manifest 29/30 entries, 양 configure.ac 바이트와 발행자 SHA-256 일치 | synthetic revision 날짜는 웹 빌드·게시 날짜가 아니며 archive visit과 분리 |
| 합계 | **2기관·3쌍·6기록** | **6/6 판의 파일 또는 manifest 판독** | 같은 저작 여러 판을 합쳐 이 표의 계보는 3 |

최소 요구인 두 제도·네 실제 판 기록과 양쪽 파일/manifest를 충족한다. Zenodo concept 레코드/리다이렉트는 새 일곱 번째 판으로 늘리지 않는다. 보존 실례 5계보 중 나머지 둘은 Gitorious의 옛 origin/보존 파일과 Zenodo 철회 tombstone이며 위 판 쌍 분모에 넣지 않는다. Gitorious 원주소는 이번 접근에서 proxy timeout이므로 origin의 404를 직접 확인했다고 쓰지 않는다. Zenodo 410은 내용 철회 레코드를 직접 확인한 것이며, 원래 파일의 바이트를 확보했다는 뜻은 아니다.

## 4. 생성·게시·응답은 다른 계수 단위

| 관측 | 분자/분모 | 단위와 근거 | 허용되는 문장 |
|---|---:|---|---|
| RTD 분석 대상 생성 성공 | **4/4** | 원 로그까지 읽은 30298914·30298916·30298915·30720077. API success=true와 HTML 생성 명령 exit0 | “선택한 네 run의 생성 성공 보고와 생성 로그를 확인했다.” |
| 그 네 run의 독립 게시 단계 성공 증거 | **0/4** | 별도 publication transaction·run별 파일 manifest를 확보하지 못함 | “별도 게시 증거를 확보한 run은 0/4다.” |
| Pages 선택 배포의 success 상태 직접 관측 | **0/2** | R1 2328795124, R2 1283145596 | “보존된 statuses에서 success를 직접 읽은 선택 배포는 0/2다.” |
| Pages 선택 배포의 남아 있는 inactive 상태 | **2/2** | R1 status6150834411, 2025-03-24T12:38:03Z; R2 status3093912083, 2024-01-21T20:58:36Z | “두 선택 배포에서 inactive 원행을 확인했으나 선행 상태 순서는 미확인이다.” |

RTD 4/4는 조회된 모든 run의 개수가 아니다. `PY-P3-SOURCEBUILDS`에는 같은 SHA의 latest30298913 success=true도 있으며, 분석한 원 로그 4run 분모에서는 제외한 보조 문맥이다. 과거 1.x14073318 성공은 ancestry 행이며 이 4run에 추가하지 않는다. 같은 프로젝트의 여러 run을 네 성공 프로젝트로 세지도 않는다.

Pages inactive를 당시 실패로 변환할 수 없다. 자동 inactive 가능성은 이전 success의 관측을 대신하지 않고, 로그 부재·빈 응답도 failure 상태가 아니다. R1의 같은 날 11개 재배포 객체는 선택 배포 1개를 11개로 바꾸지 않는다. 특히 마지막 배포의 남은 inactive 날짜는 2025-10-21로 창 밖이다.

그러므로 **4/6 배포 성공**, **0/6 게시 성공률**, **빌드4/4이므로 서비스 성공100%** 같은 합성은 금지한다. 각 분모는 관측·증거 확보 개수이며 서비스 모집단의 성공/실패율이 아니다. `is_uploaded=false`도 현재 공식 모델에서 upload API 유형과 관련된 필드이므로 독립 게시 실패 관측으로 집계하지 않는다.

## 5. 고정 경로 9슬롯 재계산

근거: `SCOPE.md`, `streams/python/routes.jsonl`, `streams/r/routes.jsonl`, 해당 NOW/CURRENT/GENERATED source ID와 영수증. P3 target은 v3.3.0 또는 약속된 1.x 계열, P1은7.0.1, R1은1.1.12, R2는2.3.1이다.

| 슬롯 | 현재 HTTP | 현재 목표판 식별 | 주창에 목표판을 받은 응답 식별 | 판독 근거 |
|---|---:|---:|---:|---|
| P3 stable/options/#enable | 200 | 아니오 | 미확인 | 현재 stable 본문은 v3.3.0과 다름. anchor 존재는 확인 |
| P3 1.x root | 200 | 예 | 미확인 | 실제 CPython2.7/3.5·PyPy2.7 내용, 1.x metadata |
| P3 v3.3.0/options/#enable | 200 | 예 | 미확인 | v3.3.0 metadata·enable의 해당 판 내용 |
| P1 latest root | 200 | 아니오 | 미확인 | 현재 title8.2.0 |
| P1 named7.0.1 root | 404 | 미확인 | 미확인 | 현재404를 과거의 실패로 소급하지 않음 |
| R1 root | 200 | 아니오 | 미확인 | 현재1.1.14, 선택 생성물1.1.12 |
| R1 reference/archive_read.html | 200 | 아니오 | 미확인 | 현재1.1.14, 선택 생성물1.1.12 |
| R2 root | 200 | 예 | 미확인 | 현재2.3.1·선택 생성물과 바이트 일치 |
| R2 articles/asciicast-demo.html | 200 | 예 | 미확인 | 현재2.3.1·선택 생성물과 바이트 일치 |
| 확인 수 | **8/9** | **4/9** | **0/9** | 각 행의 조회 UTC는 서로 다름 |

8/9는 이번 현재 응답 표본의 HTTP200 수이며 동일 순간 가동률이 아니다. 4/9는 목표판을 직접 식별한 경로 수이며 나머지 전부가 잘못 제공된 역사 사건이라는 뜻이 아니다. 목표판 미식별 5개 가운데 현재 다른 내용인 4개와 현재404인1개를 분리했다. 주창 0/9는 당시 제공되지 않았다는 반증 수가 아니다.

P3 2025-11-14의 stable options·stable root·legacy 보관본은 주창 `[2025-11-11,2025-11-14)` 밖이다. 두 경로 캡처 시각도 02:26:28Z와11:28:00Z로 다르므로 동시성 분자에 넣지 않는다. root 추가 판독을 열 번째 슬롯으로 늘리지 않는다. R2 바이트 일치 역시 당시 제공 시각을 만들지 않는다.

## 6. 두 조건의 원 분모와 완료 판정

두 독자 조건을 소유자가 약속한 원 모집은 **1/6**, 이번 고정 소비자는 **1/4**다. 공동 확인이 적용되는 프로젝트 P3에서 주창 두 조건 확인은 **0/1**, 미확인1/1이다. R1·R2처럼 원문에서 두 조건을 약속하지 않은 부분집합의 공동 확인은 **0/0 산출 불가**다. 0/2로 바꾸거나, 실패한 두 약속으로 간주하면 안 된다.

네 자리 권고 비교를 수행한 것은4/4이나, 동시 제공을 평가할 수 있는 약속의 분모는1이다. 사건의0/12·0/4와 네 소비자의0/1을 합산하지 않는다. 보존기관3쌍·6기록도 경로9슬롯에 추가하지 않는다.

**독립 감사 결론:** 잠정 산술은 모두 재현된다. 최종 자료량 표현은 “원장201행, 적격 직접 원문126행, 같은 payload3쌍을 합친123지문, 보수적25계보(정책4계보를 빼도21)”가 적절하다. 생성4/4·게시 증거0/4·Pages success 직접관측0/2·현재HTTP8/9·현재목표판4/9·주창목표판0/9·공동조건0/1은 각각 다른 분모로 유지한다. P3 주창 공동 제공 및 R1 완전한 당시 상태 순서/독자 제공의 결손이 남으므로 자료 최소량 충족만으로 PARTIAL을 REVIEW_READY로 바꾸지 않는다.

## 재현 범위와 남은 최소 확인

1. 적격 행 집계는 코드에 기록된 플래그를 독립적으로 합산했다. 각 행의 모든 긴 원문 전체를 이번 감사에서 다시 읽은 것은 아니며, 핵심 분모를 결정하는 추출·영수증·사건 행·판 쌍을 읽었다. 원문 직접 판독 여부의 최초 확인 주체는 각 stream 원장에 남아 있다.
2. URL·판 무중복은 문자열 정규화 검사다. 같은 API 객체의 다른 표현을 별도 저작으로 주장하지 않도록 위 계보 병합을 함께 적용했다. SHA-256가 같은3쌍과 다르게 생긴 같은 사건의 관계도 별도로 설명했다.
3. 남은 판정을 바꾸려면 P3의 주창 경로별 응답/유효 게시구간, R1의 누락된 선행 success/전체 상태 이력과 당시 root/leaf 응답이 필요하다. 단순히 더 많은 현재200이나 정책 자료를 추가하는 것으로 분자를 올릴 수 없다.

감사 입력 원장의 SHA-256:

| 파일 | SHA-256 |
|---|---|
| `streams/python/sources.jsonl` | `ad15e156db06f1107849e94ea46f67431184c8ab3c7060b1b36d5fb15104e07b` |
| `streams/r/sources.jsonl` | `a6e8975109f902375c4c614fb3e3dec92f253586b2a72d1ecd01b61438b3fb42` |
| `streams/incidents/sources.jsonl` | `10d9f3020f7f0a81c67db9257ec2ef1486ff49b2492cbab84bee10390150cff1` |
| `streams/preservation/sources.jsonl` | `e0803fefb306e9bdb1a378a9bd9fed915c64fa15f154629519abd901eb8b17e6` |

재현 핵심식:

```python
eligible = lambda r: bool(r.get("countable_original",
    r.get("primary_count_eligible", r.get("counts_original", False))))
# four streams; parse each nonempty JSONL row once
qualified = [r for r in all_rows if eligible(r)]
assert len(all_rows) == 201
assert len(qualified) == 126
assert len({r["lineage_id"] for r in qualified}) == 25
# Hash domains follow the source ledger: direct decoded file / downloaded body /
# connector snapshot, never publisher checksum substituted for a direct hash.
payload_hashes = [r.get("direct_sha256", r.get("download_sha256",
    r.get("snapshot_sha256"))) for r in qualified]
assert None not in payload_hashes
assert len(set(payload_hashes)) == 123
```
