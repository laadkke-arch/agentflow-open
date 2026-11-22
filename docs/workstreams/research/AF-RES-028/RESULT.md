# AF-RES-028 문서상 유지와 고정판 실행의 대조

| 익명 셀 ID·생태계 | T0 주장·환경·근거 URL | 분기말 판·검사·기대값 | T0·해당 판 실측·영수증 | 공개 후 기존 판정·일치 여부 | 미확인 원인 |
| --- | --- | --- | --- | --- | --- |
| A028-05 · Node | EC import의 `NODE-ED25519` 곡선, Linux x64. [T0 §EcKeyImportParams](https://raw.githubusercontent.com/nodejs/node/e5873d786249d9b6aa1d8c422f856036c2c53e5e/doc/api/webcrypto.md#L1175-L1196) | v24.9.0 · 고정 SPKI를 ECDSA+해당 곡선으로 import한다. P-256을 대조한다. | 같은 호출은 `DataError` → `NotSupportedError`. P-256 양쪽 성공. NODE 전용 알고리즘 import 성공 → 실패, 표준 Ed25519는 그 역방향. [원 로그](receipts/first/raw.jsonl) | 무효 → 문자 그대로 최초 오류. NODE 전용 이름을 뜻했다면 무효 일치. | T0 두 설명을 한 계약으로 합치면 안 된다. 다른 키 형식 미확인. |
| A028-10 · Python | 기본 홈 `.netrc`에 암호와 불안전한 권한이 있으면 예외, POSIX. [T0 §netrc](https://raw.githubusercontent.com/python/cpython/2cd268a3a9340346dd86b66db2e9b428b3f878fc/Doc/library/netrc.rst#L19-L39) | v3.11.2 · 일반 로그인 0644 예외 / 0600 파싱. 유일한 추가 분기는 dummy anonymous 로그인이다. | 일반 0644 `NetrcParseError`, 0600 파싱 양쪽 동일. anonymous 0644 예외 → 파싱. [원 로그](receipts/first/raw.jsonl) | 무효 → 일반 로그인 계약 유지. anonymous 포함 읽기는 무효 일치. | 파일 소유자 불일치와 실제 계정은 사용하지 않았다. |
| A028-20 · Python | `pydoc` 명령으로 모듈의 docstring을 출력, Linux x64. [T0 §pydoc](https://raw.githubusercontent.com/python/cpython/2cd268a3a9340346dd86b66db2e9b428b3f878fc/Doc/library/pydoc.rst#L24-L46) | v3.11.1 · `python -m pydoc`의 문서 출력. 공개 후 설치된 `pydoc3`와 맨 이름도 점검. | 두 판의 모듈 경로와 `pydoc3`는 센티널 출력·0. `pydoc`는 두 판 모두 127. [CLI 재검](receipts/pydoc-post-reveal.jsonl) | 보류 → 모듈/버전 이름으로는 성립. 맨 이름을 요구하면 관측 설치에서는 최초 오류. | 다른 Linux 패키징의 unversioned alias 미확인. |
| A028-23 · Node | `histogram.percentiles`의 누적 분포 Map, Linux x64. [T0 §histogram.percentiles](https://raw.githubusercontent.com/nodejs/node/e5873d786249d9b6aa1d8c422f856036c2c53e5e/doc/api/perf_hooks.md#L925-L933) | v24.3.0 · [1,2,2]의 Map·끝점, reset 뒤 [5]. | 양쪽 `instanceof Map=false`, Map brand=true 및 native get(100)=2, reset 5/5. [v1](receipts/node-first/raw.jsonl) · [v2](observations.jsonl) | 유지 → 실제 Map 계약 유지. v1 프로토타입 검사는 양쪽에서 기각. | 부동소수점·빈 Map·BigInt·모든 메서드는 미확인. |
| A028-11, 12, 19 · Node | preview1 `new WASI({args,env})`에서 version 생략, 실험 플래그. [T0 예제 및 생성자](https://raw.githubusercontent.com/nodejs/node/e5873d786249d9b6aa1d8c422f856036c2c53e5e/doc/api/wasi.md#L18-L32) | v24.3.0 / v22.3.0 / v20.3.1 · `start`가 WASM 전역을 0→1로 바꾼다. | T0 0→1, 세 목표판은 options.version `ERR_INVALID_ARG_TYPE`. 명시 preview1은 세 판 모두 0→1. [봉인](observations.jsonl) | 무효 → 무효 3셀. 같은 이유 한 군. | WASI 시스템 호출과 다른 옵션 조합은 미확인. |
| A028-02, 25, 36 · Python | SSL 빌드, 로컬 TLS, `IMAP4_SSL(keyfile=…, certfile=…)`. [T0 §IMAP4_SSL](https://raw.githubusercontent.com/python/cpython/2cd268a3a9340346dd86b66db2e9b428b3f878fc/Doc/library/imaplib.rst#L85-L117) | v3.11.2 / v3.11.1 / v3.13.2 · 양쪽 PEM, 서버가 client cert를 확인하고 NOOP이 OK. 누락 PEM은 예외. | T0·3.11.1·3.11.2 성공, 누락 `FileNotFoundError`. 3.13.2 `TypeError`, 같은 판 SSLContext 대안 성공. [실행](observations.jsonl) | 앞 두 셀 유지 일치, 마지막 무효 일치. | 첫 1024-bit fixture가 준비에서 실패했고 3072-bit로 복구했다. 배포 당시 OpenSSL 조합 미확인. |
| A028-22 · Python | Tk+디스플레이에서 `python -m turtledemo`. [T0 데모 뷰어](https://raw.githubusercontent.com/python/cpython/2cd268a3a9340346dd86b66db2e9b428b3f878fc/Doc/library/turtle.rst#L2373-L2397) | v3.10.4 · 실제 X 창 제목, DISPLAY를 없앤 부정 검사. | 같은 태그 _tkinter 보완 뒤 두 판에서 창 확인 및 별도 `TclError`. [준비 실패](receipts/python-first/raw.jsonl) · [복구](receipts/tk-repair.json) · [실행](receipts/first/raw.jsonl) | 유지 일치. | 실제 사람의 입력이나 개별 데모의 기능은 미확인. |
| A028-15 · Python | 별도 패키지 없이 표준 distutils로 build/install. [T0 setup.py 예제](https://raw.githubusercontent.com/python/cpython/2cd268a3a9340346dd86b66db2e9b428b3f878fc/Doc/distutils/introduction.rst#L58-L113) | v3.14.2 · 무패키지 설치, build 출력과 stage 경로에 대조용 모듈. | T0 build/install 파일 생성, 목표판 두 호출 모두 `ModuleNotFoundError`. [원 로그](receipts/first/raw.jsonl) | 무효 일치. | Setuptools 호환은 이 계약에 적용하지 않았다. |
| A028-40 · Python | BinHex4 ASCII를 RLE 해제 없이 디코딩, Linux x64. [T0 §a2b_hqx](https://raw.githubusercontent.com/python/cpython/2cd268a3a9340346dd86b66db2e9b428b3f878fc/Doc/library/binascii.rst#L89-L95) | v3.12.1 · `!!!!:`에서 000000과 끝 표시, 불법 문자 부정. | T0 hex 000000/1과 `Error`; 목표판 속성 없음. [실행](observations.jsonl) | 무효 일치. | BinHex 대체 패키지 전환 비용 미확인. |
| A028-32 · Python | 고정 Linux에서 winreg 핸들 사용 후보. [T0 Windows 표식](https://raw.githubusercontent.com/python/cpython/2cd268a3a9340346dd86b66db2e9b428b3f878fc/Doc/library/winreg.rst#L1-L16) | v3.12.1 · `ConnectRegistry` 호출 경로 및 site 미로드 대조. | 두 판 Linux에서 모듈 없음. [실행](observations.jsonl) | 최초 오류 일치. | 다른 플랫폼인 Windows 실제 핸들 미검사. |
| A028-29 · Python | `imghdr.tests` 콜백을 헤더 감지에 등록. [T0 §tests](https://raw.githubusercontent.com/python/cpython/2cd268a3a9340346dd86b66db2e9b428b3f878fc/Doc/library/imghdr.rst#L67-L86) | v3.12.6 · 센티널 검출/다른 헤더 None. | 두 기대값 양쪽 일치, 목표판 제거 예정 DeprecationWarning. [원 로그](receipts/first/raw.jsonl) | 유지 일치. | 실제 영상 디코딩·3.13 이후 미검사. |
| A028-16 · Node | 점이 있는 ext를 넘긴 `path.format`. [T0 POSIX 예제](https://raw.githubusercontent.com/nodejs/node/e5873d786249d9b6aa1d8c422f856036c2c53e5e/doc/api/path.md#L205-L253) | v21.7.1 · `/file.txt`, base 우선순위와 점 없는 확장자 대조. | 주 계약·base 대조 양쪽 동일. 점 없는 입력만 `/filetxt` → `/file.txt`. [실행](observations.jsonl) | 유지 일치. | Windows 경로와 다른 입력 규칙 미검사. |
| 전체 A028-01–42 | 33가지 실험 계약의 원문 위치·환경. [계약](contracts.jsonl) · [출처](sources.json) | 22 목표판, 계열별 한 개의 T0. [판·해시](artifacts.csv) | 모든 행의 T0/목표 반환값, 원 로그 해시, 종료 코드. [실행 원장](observations.jsonl) | [공개 후 42개 행](comparison.csv)과 [층별 교차표](tabulations.json). | 범위를 초과한 용도와 모집틀 밖은 미확인. |

| 표집층·생태계 | 전체·추출·독립 이유·릴리스 수 | 직접 실행·공식 과거 실행·정적 확인 | 성립·불성립·보류 | 불일치 수·미확인 양끝 | 해석 범위 |
| --- | --- | --- | --- | --- | --- |
| 유지 · CPython | 416 / 16 / 11 / 10 | 16 직접 쌍, 과거 미확인, 구현·테스트·제거 정적 근거 10셀 | 16 / 0 / 0 | 0, 숨은 무효 0–0/16 | 포함확률 1/26, Linux x86-64 같은 태그 재빌드 |
| 유지 · Node | 481 / 16 / 15 / 8 | 16 직접 쌍, 과거 미확인, 구현·테스트·제거 정적 근거 6셀 | 16 / 0 / 0 | 0, 숨은 무효 0–0/16 | 포함확률 16/481, 공식 Linux x64 바이너리 |
| 유지 · 합계 | 897 / 32 / 26 / 18 | 32 직접 쌍 | 32 / 0 / 0 | 0, 숨은 무효 0–0/32 | 표본 밖 865셀 미검사 |
| 무효 대조 · CPython | 64 / 4 / 4 / 4 | 4 직접 쌍, 과거 미확인, 구현·테스트·제거 정적 근거 4셀 | 1 / 3 / 0 | 1/4 · 1–1/4 | 1/16. A028-10의 넓은 해석에서는 일치 |
| 무효 대조 · Node | 31 / 4 / 2 / 4 | 4 직접 쌍, 과거 미확인, 구현·테스트·제거 정적 근거 4셀 | 0 / 3 / 0, 최초 오류 1 | 1/4 · 1–1/4 | 4/31. 3회의 WASI는 같은 이유, A028-05의 전용 이름 해석에서는 일치 |
| 최초 오류 대조 · 계열 통합 | 16 / 1 / 1 / 1 | 1 직접 쌍 · Python | 최초 오류 1 | 0/1, 표집틀 최초 오류 재확인 | 1/16. A028-32 Linux |
| 보류 대조 · 계열 통합 | 16 / 1 / 1 / 1 | 1 직접 쌍 · Python | 1 / 0 / 0 (동결된 모듈 범위) | 상태 변경 1/1, 엄격한 맨 이름은 최초 오류 | 1/16. A028-20의 설치 관례를 별도 판독 |
| 대조 전체 | 127 / 10 / 8 / 9 | 10 직접 쌍, 역사적 영수증 미확인 | 2 / 6 / 0, 최초 오류 2 | 선택된 검사 범위에서 서로 다른 상태 3/10 | 제어 표본은 유지 셀 비율의 분모에 합치지 않는다. |

| 정책·표본층 | 같은 셀의 옛 혼동표 | 검증 가능한 셀의 수정 혼동표 | 미방문·참값 불일치·검열 | 추가 획득·빌드·판독 비용 | 반례와 미확인 |
| --- | --- | --- | --- | --- | --- |
| D · 유지 32 | TP·FP·FN·TN = 0·0·0·32 | 0·0·0·32, 32 쌍 | 원문 6/32 읽음, 26 미방문, 참값 변경·검열 0 | 표본 공동 비용은 [원장](costs.csv). 예측을 다시 실행하지 않았다. | 원문 미방문이 런타임 오판을 뜻하지 않는다. |
| S · 유지 32 | 0·0·0·32 | 0·0·0·32, 32 쌍 | 원문 4/32 읽음, 28 미방문, 신호 27, 참값 변경·검열 0 | D/S 동일 실행 결과를 사용하며 별도 정책 비용 청구는 해당 없음. | 신호와 실행 실패의 관계는 이 층에서 추정할 사건 0. |
| D · 무효 8 | 7·0·1·0 | 같은 이진 7셀에서 6·0·1·0 → 5·1·1·0 | 원문 0/8. A028-10 TP→FP, A028-05는 새 이진에서 검열. 새 FN 1은 미방문. | netrc 공식 테스트와 판 읽은 비용은 공동 원장에 포함했다. | anonymous 포함 민감도에서 FP가 사라진다. |
| S · 무효 8 | 4·0·4·0 | 같은 이진 7셀에서 3·0·4·0 → 3·0·3·1 | 원문 0/8. A028-10 FN→TN, A028-05는 새 검열. 새 FN 3은 미방문. | 신호 8/8, 할당 탈락은 새 비용으로 합치지 않는다. | 세 미방문 FN은 같은 WASI 이유의 세 분기다. |
| D · 전체 42 교차 | 7·0·1·32, 검열 2 | 교집합 39에서 6·0·1·32 → 5·1·1·32. 수정 채점 40에서 5·1·1·33. | 원문 7/42. A028-20의 모듈 해석이 새 TN 1, A028-05와 A028-32가 새 검열 2. | 처음 읽은 raw 파일 105개 3,669,760B, 개별 configure·make·install 합계는 Q7. | 대조를 함께 집계한 것은 셀 이동 검산이다. 발생률과 모집단 순위는 미확인. |
| S · 전체 42 교차 | 4·0·4·32, 검열 2 | 교집합 39에서 3·0·4·32 → 3·0·3·33. 수정 채점 40에서 3·0·3·34. | 원문 4/42. 새 검열 2. A028-20 엄격 해석에서는 새 TN 1이 다시 검열된다. | 공동 직접 검사 75/75 회. 초회 실패·대기·설치 항목은 [비용](costs-summary.json). | 보고의 기억 상태와 현재 셀의 새 보고를 구별했다. 42셀 신규 보고 0. |

| Q 번호·주장·적용 범위 | 근거 원문 URL·정확한 절 또는 실행 영수증 | 확인한 내용·분자·분모 | 반례를 찾은 곳과 결과 | 미확인·판단을 바꿀 최소 자료 |
| --- | --- | --- | --- | --- |
| Q1 · 비복원 42셀 입력 가림 | [설계](draw.py) · [할당·해시](scope-lock.json) · [재추출 영수증](receipts/preflight.json) | 계열별 유지 16·16, 무효 4·4, 최초 오류·보류 1·1. 같은 코드의 출력과 답 해시 일치. | 스키마 사전 확인의 T0 노출은 공개 후 A028-04·08·13·18·24·26·34·35와 겹친다. | 작성자와 완전히 무관한 맹검은 미실시. 별도 작성자에게 큐만 주면 확인 가능. |
| Q2 · 반환과 부작용 계약 | [33 계약](contracts.jsonl) · [개정 및 이유](contract-amendments.jsonl) | 33/33 양성·경계 입력이 있고 42셀에 연결했다. | Map prototype 가정 실패와 Netrc 범위 변경, WebCrypto 이름 두 해석을 같은 기록으로 검산. | 다른 타이핑·배포 관례·제품 요구에서 동일한 용도인지는 별도 판정이다. |
| Q3 · 정확한 태그의 Linux 실행 | [배포물과 해시](artifacts.csv) · [런타임 출력](receipts/first/versions.jsonl) · [Node 예시 릴리스](https://nodejs.org/en/blog/release/v24.9.0#shasums) | CPython 13 소스 빌드, Node 11 공식 바이너리. 24/24 버전·아키텍처·바이너리 해시 검증. | www.python.org 소스 도메인의 초기 shell 403 뒤 공식 Git 태그 소스. Tk 헤더와 PEM 조합은 첫 실행에서 실패했다. | CPython 당시 커널·배포물의 원 바이너리 동일성은 미확인. 해당 환경 이미지 또는 vendor 영수증이 필요하다. |
| Q4 · 같은 입력·옵션과 직접 관측 | [42쌍](observations.jsonl) · [원 로그](receipts/first/raw.jsonl) | 양성·경계 기준 34 성립, 6 무효, 2 최초 오류. 42/42 직접 시도와 구조화 관측. | A028-29 경고와 유지, A028-16 경계 입력에만 변화, A028-36 이름 유지와 키워드 제거. | 문서가 다른 파일로 이관된 독립 사건은 이 표본에서 직접 확인하지 못했다. 같은 파일의 절 위치 변화는 관측했다. |
| Q5 · 동일 셀의 상태와 독립 관측 경로 | [가림 판독](blind-review.jsonl) · [옛/새 대조](comparison.csv) · [CLI 재검](receipts/pydoc-post-reveal.jsonl) | 유지 32/32, 무효 6/8 직접 재확인, A028-05·10의 대안은 2/2 무효에 합치. 최초 오류 1/1 재확인, 보류 1셀 조건부 좁힘. | WASI 목표판 생성자 절은 필수, getImportObject 절은 생략 가능 문구를 남겼다. Netrc와 pydoc의 문장 범위가 결말을 바꾼다. | 2021–25 자동화의 사람 판독 및 당시 공식 테스트 영수증 미확인. 이 실험의 공식 테스트 재실행은 4/4이다. |
| Q6 · 고정 D/S 예측과 유지 분모 | [층·정책 원장](tabulations.json) · [024 고정 visits.csv](https://github.com/laadkke-arch/agentflow-open/blob/4af1300841c1c39f9ef6e76d78579034d1ae0c51/docs/workstreams/research/AF-RES-024/visits.csv) | 표의 교집합 39. 유지 표본 숨은 무효 0/32·미확인 0/32, 직접 32/32. | 무효 판정이 남은 WASI 3셀의 정책 미방문과 A028-10의 참값 재정의를 구별했다. | 865개 미검사 유지 셀과 원 모집단의 새로운 D/S 순위 미확인. |
| Q7 · 준비와 검사 증분 비용 | [획득](receipts/acquisition.json) · [비용](costs.csv) · [실행 벽시간](receipts/first/time.txt) | 공식 raw 요청 106 중 105, 3,669,760B, 배포 24/25, 663,116,103B. 첫 완전 실행 75/75, 19.874초. | web 자료 열기 바이트와 실제 사람 판독 시간은 미계측. 준비 실패 8회와 깨끗한 재생을 분리했다. | 2022년 연결 속도, 새 제품 운영비 미확인. |
| Q8 · 인증·fixity와 용도 시험 | [SRM 342a](https://tsapps.nist.gov/srmext/certificates/342a.pdf) pp. 1–4 · [BagIt §3](https://www.rfc-editor.org/rfc/rfc8493.txt) · [Domesday 보존](https://atsf.co.uk/dottext/domesday.html) · [InSPECT pp. 17–19](https://significantproperties.kdl.kcl.ac.uk/inspect-finalreport.pdf) | 71개 고유 산입 원문 중 계측 2, 디지털 보존 4. 독립 외부 관측은 342a 개정·Domesday·InSPECT·CAMiLEON 사용자 시험의 네 단위. | 은닉 변화와 역반례를 모두 찾았다. InSPECT에서 이미지 치수는 보존됐고 색 변화는 보였다. CAMiLEON 소규모 사용자 연구는 이관과 에뮬레이션 군 사이 큰 차이를 입증하지 않았다. | 342a 구 인증 수치와 Domesday 동일 파일 체크섬 영수증 미확인. 각각 옛 인증서와 측정 로그, 원 이미지와 대조 캡처가 필요하다. |

## Q1–Q3 표집과 계약 고정

표집은 024의 유지 897, 무효 95, 최초 오류 16, 보류 16을 그대로 썼다. 층별 포함확률은 표 2와 [잠금](scope-lock.json)에 있다. 층 안에 중복 분기와 기능을 그대로 뒀으며 같은 이유는 동일 테스트를 재사용했다. 유지 표본의 서로 다른 이유는 26, 목표판은 18, 이유–판 조합은 32다. 전체는 이유 33, 목표판 22, 이유–판 조합 42다. 동일 판의 2026년 실행과 2021년 당시 운영 환경의 복원은 다른 주장이다. [분모](tabulations.json)

가림 큐를 만들기 전에 Node 일부 이유와 T0 초기 상태에 노출됐다. 그중 유지 표본 8셀과 실제 겹쳤다. 원 분기별 배정 라벨과 근거, 정책 결과는 관측을 봉인할 때까지 표집 코드 밖에서 열지 않았다. 같은 작성자가 가림을 설계하고 판독했으므로 모델의 사전 지식과 추측을 배제할 수 없다. 원 계약과 보강 가정은 별도 판으로 남겼다. [범위·노출 원장](SCOPE.md) · [가림 봉인](observation-seal.json)

Node는 공개 SHA-256으로 다운로드를 대조했다. CPython의 커밋 주소 아카이브 SHA-256은 이 시점에 측정한 포장 바이트 해시다. 프로젝트 서명의 독립 검증으로 쓰지 않았다. 각각의 upstream 태그가 가리키는 커밋을 별도로 조회했다. 구판도 같은 태그에서 빌드했다. 실행 영수증의 OpenSSL·아키텍처와 보조 드라이버는 동일한 2026년 Debian 환경에 한정된다. [획득·서명 범위](artifacts.csv) · [버전](receipts/first/versions.jsonl)

## Q4–Q5 같은 동작을 입증하는 조건

A028-05의 매뉴얼 표는 일반 EC 매개변수와 제품 전용 곡선을 같이 적었다. 고정 P-256 SPKI는 성공했고 일반 ECDSA에 Ed25519 SPKI를 넣은 T0 테스트는 실패했다. 같은 SPKI로 NODE 전용 알고리즘은 T0에 성공했고 목표판에서 실패했다. 따라서 문장대로 일반 EC 사전으로 읽으면 최초 오류, 이름이 바뀐 전용 사용을 의도했다면 024의 무효가 설명된다. 현대 Ed25519 성공은 기존 호출의 복구 영수증에서 제외했다. 대상 환경의 공통 실패 가능성은 두 버전의 P-256과 각각의 다른 알고리즘 성공으로 대조했다. [T0 import 분기](https://raw.githubusercontent.com/nodejs/node/e5873d786249d9b6aa1d8c422f856036c2c53e5e/lib/internal/crypto/webcrypto.js#L459-L490) · [봉인](blind-review.jsonl)

A028-10은 명세가 암호가 있는 모든 로그인에 적용되는지에 달렸다. 동일 EUID·모드와 dummy 입력일 때 일반 로그인은 두 판에서 예외다. anonymous 입력의 T0 예외가 목표판 파싱으로 바뀌며 v3.11.2 공식 매뉴얼에도 예외가 적혀 있다. 그러므로 좁은 계약에서 D의 고정 TP가 FP로, S의 고정 FN이 TN으로 이동한다. T0 문장을 예외 없이 읽으면 D/S의 이 행은 024와 각각 같다. 소유 불일치는 공식 테스트 주석도 시험하지 못했다고 밝힌다. [v3.11.2 매뉴얼](https://raw.githubusercontent.com/python/cpython/878ead1ac1651965126322c1b3d124faf5484dc6/Doc/library/netrc.rst#L19-L47) · [봉인](observations.jsonl)

A028-20은 기능과 설치 이름이 다른 주장이다. 맨 이름의 실행을 후검사했고 이 빌드의 T0·목표판에서 둘 다 127이다. `pydoc3`와 단일 버전의 모듈 호출은 둘 다 0이고 같은 문서 센티널을 출력했다. 이 장의 주 혼동표는 가린 실행에서 미리 지정한 모듈 경로를 쓰며, 맨 명령 이름을 요구할 때의 채점은 별도로 계산했다. 다른 Python 배포판의 alias는 두 소스 빌드에서 추론하지 않는다. [후검사 원 로그](receipts/pydoc-post-reveal.jsonl) · [엄격 민감도](tabulations.json)

A028-23의 이전 검사식은 Map의 프로토타입 연결을 과다 요구했다. Node의 SafeMap 구현과 두 판의 native Map brand 및 메서드 호출을 대조했고, 입력 데이터 분포도 동일하다. v1의 실패 관측을 보존한 뒤 v2 판정식을 썼다. A028-29는 경고 추가와 기능 손실을 구별했다. A028-16은 문서에서 같은 예제가 계속 유효하지만 점 없는 ext의 동작이 달라졌음을 구별한다. A028-03·33의 importlib 절은 줄 위치가 이동했고 이름 생략과 모듈 실행이 계속 됐다. 문서 절 시작점을 기능 신호로 쓸 경우 이런 변화도 후보에 섞인다. [SafeMap 생성 방식](https://raw.githubusercontent.com/nodejs/node/741975041995a272ff7e378bcbb6d6fa4b93f38f/lib/internal/per_context/primordials.js#L392-L411) · [실측](observations.jsonl)

실험 당시 주요 A028-36 제거와 A028-11·12·19 옵션의 무효는 원본 구현의 인자 단계에서도 설명된다. 같은 TLS 서버에서 SSLContext가 작동했고 명시 preview1이 실행됐으므로 환경이 전체 기능을 막았다는 설명은 이 경우 맞지 않는다. A028-22와 IMAP 최초 실패는 반대 사례로 남는다. 라이브러리 표면에서 실패하기 전에 데비안 개발 헤더 부족 또는 좁은 TLS 인증서 조건이 실패했다. 재구축 뒤 같은 환경에서 통과했다. [환경 개정](contract-amendments.jsonl) · [tk 복구](receipts/tk-repair.json) · [고정 테스트 판독](blind-review.jsonl)

## Q6 표본 밖과 정책 해석

기존 유지 32셀에서 T0 폐기 표식은 8/32, 024 사건 공지가 그 분기까지 알려진 이유는 3/32, S의 당시 기억 경고는 8/32였다. S 신호는 27/32이고 024의 문서 절 존재는 32/32다. 각 하위 분모에서 유지가 관측됐다. 전체 42셀에서는 같은 집계가 각각 11, 11, 8, 35, 41이다. 절이 unlocated인 한 셀은 A028-40으로 실행 무효였다. 이 층들을 서로 독립 표본으로 인용할 수 없다. [상세 분모와 행](tabulations.json)

기존 유지 표본에서 미확인은 0개다. 미확인을 모두 성립 또는 모두 무효로 두어도 관측 범위는 0–0/32다. 숫자는 사전 정의하거나 독립 경계 대조로 바로잡은 좁은 계약에서만 성립한다. 표본 밖 865개의 실제 실패·미확인 수와 새 전체 D/S 혼동표·순위는 계산하지 않았다. 무효 8개 대조의 6개 일치, 최초 오류·보류 2개의 진단도 유지 모집단의 추정치에 섞지 않았다. [영역과 민감도](tabulations.json)

현재 분기에 정책 새 보고는 D/S 각각 0/42였다. 실제 원문 방문은 이유에 귀속된 attempt와 같은 경로의 성공된 공유 읽기로 셌다. 무효 행에서 기억된 경보가 있었어도 현재 분기의 원문 방문을 뜻하지 않는다. 무효 유지 상태에 대한 D 미방문 FN은 A028-19 1셀, S는 A028-11·12·19 3셀이다. A028-10의 다른 판정은 방문 회피가 아니라 좁은 명세에서 참값 변화이며, A028-05와 A028-20은 이진 분모의 진입·이탈을 바꾼다. [정책 조인](comparison.csv)

## Q7 획득·재검 비용

공식 raw 파일 105개의 응답 본문은 3,669,760B였다. 한 건은 이전 distutils 문서 경로 404로 같은 태그의 제거 공지를 확인했다. 자료 조사 웹 열람에는 크기를 재지 못한 페이지가 있고, 원문 문헌 수에는 들어가더라도 바이트에 덧셈하지 않았다. 24개 배포·태그 아카이브 663,116,103B 및 Node 체크섬 파일 11개 35,762B, 데비안 보조 패키지 10개 6,916,464B를 분리했다. 배포 시도 25개 중 한 원래 CPython 소스 다운로드가 실패했다. 태그 조회 응답과 실행 영수증은 문헌 수 밖이다. [획득](receipts/acquisition.json) · [비용](costs-summary.json)

CPython 13판의 configure, make, install은 각 작업 벽시간의 합으로 249.750초, 1,024.664초, 58.180초였다. 동시 작업이 포함되어 실제 작업 전체의 경과시간과 다르다. 동일 태그 Tk 복구 두 건의 합은 1.5424초다. 첫 Node 검사 37/37, 초기 CPython 30/38에서 8건의 준비 실패·판 대기를 기록했다. 복구 후 최초 전체 실행은 75/75 개별 검사에서 구조화된 관측을 생성했고 19.874초에 드라이버 종료 0이었다. 한 ID에서 나오는 무효 판정은 관측 성공으로 세고 기능 성공과 구별한다. [비용 원장](costs.csv)

## Q8 다른 분야의 판정 단위

NIST 342a는 병으로 공급하는 물질에 성분별 인증 질량분율·확장불확도·보관·혼합·시료 양을 묶는다. Table 1의 Si는 2.733%와 확장불확도 0.025 퍼센트포인트다. pp. 2–3의 혼합 1분, 시험 시료 0.2g 이상 및 Table 2 방법을 함께 확인해야 이 수치의 재검 사용을 옮길 수 있다. 2019년에는 황을 제외한 인증값·불확도 이력이 갱신됐다. NIST FAQ의 1999년 원 인증서 설명은 인증서 개정 이력에서 1970년 처음 발행으로 적힌 부분과 다르다. 여기서는 시점 증명에 인증서 이력을 썼다. 같은 지정 번호가 최신 값·판·측정 조건까지 식별하지 않는 사례다. [인증서 pp. 1–4](https://tsapps.nist.gov/srmext/certificates/342a.pdf) · [NIST 정책 §5.1.4·5.1.7](https://www.nist.gov/metrology/metrological-traceability)

BagIt의 완전성·fixity 합격 단위는 manifest와 경로별 옥텟이다. Domesday 참여자가 같은 판독 가능한 디지털 데이터 맥락에서 보고한 Windows 에뮬레이션은 원 프로그램의 통계 지도 오버레이를 되살렸고 역공학 이관은 원 인터페이스·화면 크기를 요구하지 않았다. 동일 파일 해시 영수증을 자체 확인하지 않았으므로 원판 보존과 조작의 구별을 보여주는 질적 관측으로 사용했다. InSPECT는 실제 포맷 변환에서 치수는 유지됐어도 색이 달랐고, CAMiLEON 사용자 시험은 디스크 이미지 에뮬레이션과 Windows 재작성 양쪽에서 원 장비와의 작은 동작 차이를 사람 눈으로 확인했다. 가독성이나 사용자 성과를 목표로 할 경우 높은 충실도의 이관도 대안이 된다. [BagIt §§2–3](https://www.rfc-editor.org/rfc/rfc8493.txt) · [Domesday](https://atsf.co.uk/dottext/domesday.html) · [InSPECT](https://significantproperties.kdl.kcl.ac.uk/inspect-finalreport.pdf) · [CAMiLEON 사용자 시험](https://webdoc.gwdg.de/edoc/aw/rlgdn/preserv/diginews/diginews5-6.html)

판·파일 체크섬은 대상을 다시 찾고 비교할 수 있게 한다. 배포물을 실행해 본다는 것은 렌더러나 시료 조건을 추가해 사용 결과를 확인하는 또 다른 단위다. 물질은 채취·열화시킬 수 있고 인증값은 불확도를 갖는다. 디지털 해시와 API의 유한 fixture 관측은 그 물리적 특성에 그대로 비유할 수 없다. 반대로 한 번의 성공도 지원 플랫폼 전체나 미래 버전의 보증은 아니다. 예를 들어 A028-16의 점 있는 suffix 결과를 다른 입력으로 옮기면 이미 달라진다. [대조 실행](observations.jsonl)

## 관점과 적용 조건

| 성공을 확인하는 사람 | 결정 기준 | 관측에 붙는 대안 |
| --- | --- | --- |
| 배포판 관리자 | 원격 태그, 배포 바이트, 대상 OS·옵션의 재현 가능한 출처 | 배포 표와 검증된 매니페스트로 파일 동일성의 질문에 답한다. API 경로 변경 판정은 동일 환경의 실행 또는 정확한 명세가 필요하다. |
| T0에 고정한 사용자 | 동일 호출이 보존된 런타임의 같은 입력을 처리함 | 원 인증서·원판을 보관하는 경로처럼, 정확한 바이너리 또는 소스·호환 환경을 보존한다. 오래된 OpenSSL/Tk 조건은 현재 호스트에서 추가 확인한다. |
| 목표판으로 이관하는 사용자 | 같은 입력·목적을 달성하는지와 호출 전환 비용 | WASI에는 명시 preview1, IMAP에는 SSLContext가 실측 대안이다. 기존 계약의 무효와 호환 경로 성공을 각각 기록한다. |
| 추천 이유를 재검하는 편집자 | 출처·용도 조건을 검증하고 정확한 라벨과 미확인을 분리 | 정확한 dated 생성자에서 제거를 확인하면 저비용 정적 판독이 충분한 경우가 있다. SafeMap처럼 타입 의미가 걸리면 실측한다. 빌드·플랫폼이 없고 파일 존재만 확인되면 원래 조건을 기록하고 미확인으로 남긴다. |

실행을 요구할 이유는 Q2의 반환·부작용처럼 두 설명이 공존하거나 맨 명령의 설치 여부가 걸린 경우다. 버전 문서만으로 충분한 질문은 폐기 고지 확인 또는 정확한 제거 공지의 날짜를 찾는 경우다. 새 빌드에 Tk가 빠져 있던 최초 실행, Windows 실제 레지스트리, 역사적 공식 테스트는 그 조건을 제공하는 환경·영수증 없이는 현재 호스트 결과로 채울 수 없다. [원문·한계](sources.json)

## 재현 경로

`draw.py`로 같은 024 Git 객체에서 키를 임시 디렉터리에 재생성하고 `run.py`는 각 검사를 빈 폴더에서 실행한다. `seal.py`가 가린 규칙 해시를 만들고 `compare.py`는 봉인 SHA와 답 SHA가 맞은 뒤 같은 024 D/S 원장을 조인한다. [실행 명령](REPLAY.md) · [자체 점검](SELF_CHECK.md)

| 중요한 불일치·약점 | 근거 ID·URL | 영향을 받는 결정 | 다음 조사 질문·찾을 자료·최소 확인 |
| --- | --- | --- | --- |
| ① 유지 32개에서 0건, 865개 유지 셀은 미검사 | [분모](tabulations.json) · [A028-16](observations.jsonl) | 024 모집단 재채점과 감독 간격 | 먼저 중복 이유의 서로 다른 판·경계 입력을 층별 추가로 고정한 뒤 양쪽 직접 실행을 한 묶음 더 한다. |
| ② 문장의 이름·인자 범위가 무효와 최초 오류 및 D/S 교차표를 바꾼다 | [A028-05·10·20·23](comparison.csv) · [Node WebCrypto T0](https://raw.githubusercontent.com/nodejs/node/e5873d786249d9b6aa1d8c422f856036c2c53e5e/doc/api/webcrypto.md#L1175-L1196) | 오경보 정의와 편집자의 추천 이유 | 결과를 모르는 검토자가 API의 문자 그대로/제품 관례를 별도 표기한 뒤 네 사례의 사전 계약 일치율을 확인한다. |
| ③ 정확한 태그를 실행했어도 현재 Linux 빌드와 작은 fixture의 한계가 남는다 | [Tk·TLS 첫 실패](receipts/python-first/raw.jsonl) · [NIST 342a](https://tsapps.nist.gov/srmext/certificates/342a.pdf) | 오래된 환경에서의 재현성과 회복 비용 | 두 번째 독립 Linux 이미지에 당시 OpenSSL/Tk에 가까운 조건을 기록해 A028-02·22·36의 두 판을 다시 실행한다. |
