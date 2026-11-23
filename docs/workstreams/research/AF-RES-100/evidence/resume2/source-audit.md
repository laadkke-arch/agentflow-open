# 봉인② 이후 원문·밀림 감사

대상 사전 결과는 `5d81bcbeb5f1248fc1dd2ce2d825cf6467353673`이다. 이 조사는 `evidence/resume2/postseal-access.jsonl`에 별도로 기록했다. 원 파일 지문을 검증하고 실제 표시한 원문 구간의 Unicode/UTF-8 경계를 남겼다. 전체 압축파일 다운로드만으로 읽은 자료를 세지 않는다. 사전 패킷 접근 비용·절 이동·독자 판정에는 이 열람을 더하지 않는다.

| 사례 | A에서 빠진 3·4위 | B에 들어온 3·4위 | 이득·손실과 반례 |
|---|---|---|---|
| J2 | `src/util.c`, `tests/jq.test` | sed 매뉴얼, `testsuite/bsd.sh` | from_entries의 독립 원 시험을 잃고 문자열 치환의 설명·원 시험을 얻는다. 핵심 JSON 연산은 유지된 jq 매뉴얼에 있어 F는 양쪽 완결이다. 원 파이프라인에서 `+`를 삭제하는 것이 항상 안전하다는 결론은 내리지 않는다. 해당 실제 손실은 미관측이다. |
| J3 | `src/main.c`, `src/parser.c` | Terminal schema, Snippets 설계안 | A의 `--argjson` argv 소비 설명을 잃고 출력 소비자의 `schemes` 구조를 얻는다. 어느 쪽도 필수 Bash 변수 확장·quoting 경계를 충분히 설명하지 못한다. 설계안의 shell/command 어휘를 지원 기능으로 잘못 읽지 않았다. |
| J4 | `src/jv.c`, `src/jv.h` | AWS describe-volumes 예제, EMR helptext | 주 도구의 저수준 C 객체 API 대신 실제 입력 발행자의 배열/Tags 구조를 얻는다. 질문 자체가 그 구조를 이미 제공했고 jq 매뉴얼이 남아 F 완결은 양쪽이다. EMR의 IOPS 옵션은 다른 서비스 문서이며 원 입력에 없는 수치를 채울 근거가 아니다. |
| P1 | PowerPoint writer, EPUB 설명 | knitr `plot.R`, `hooks-latex.R` | writer의 SVG/EMF 유형 인식 근거를 잃고 외부 그림 경로→include_graphics→출력 클래스의 필수 연결을 얻는다. helper 허용 주 해석에서만 B 단독 완결이다. LaTeX에서 확장자를 출력할지 정하는 옵션은 입력 그림의 기본 형식을 고르는 옵션이 아니다. |
| P2 | Lua filter 설명, source guide | CeTZ README, bezier 구현 | reader 이후의 filter와 구현 탐색 설명을 잃고 라이브러리 자체 설치·tytanic·WASM 자원 요구를 얻는다. Pandoc의 @preview 로더와 원 0.3.4 import 성공은 여전히 없다. 실패 원인의 후보를 발견하는 것과 실패 조건을 제거하는 것을 구분한다. |
| P3 | Lua filter 설명, CLI options 구현 | 2개 공석 | 주 매뉴얼에도 PDF engine 및 외부 filter 의존 설명이 남는다. 고정 가능한 최신 안정 이미지와 원 custom template 결손은 일반 옵션 설명으로 복구되지 않는다. 두 공석을 B 패배나 A 승리로 바꾸지 않았다. |

`displacement.csv`는 경계 6건마다 빠진 주 파일 2개와 추가한 인접 자리 2개, 총 24자리를 기록한다. 같은 자리의 F/S 범위 및 F 사전 인용이 S에 완전히 들어가는지를 함께 제공한다. 둘의 교집합이 일부 존재하는 것만으로 필수 조건을 충분히 지지한다고 세지 않는다. 모든 의미 판정은 실제 절, 조건, 원 요구를 읽고 구분했다.

## 반대 설명을 찾은 결과

1. **인접 문서가 늘 필요하다:** 반례는 Pandoc 매뉴얼의 PDF 엔진 요구, FAQ의 엔진/글꼴 제약, Lua filter 문서의 외부 interpreter/library 요구이다. 주 도구 설명만으로 외부 의존을 알 수 있다. 위치는 `AUD-PD-0001`, `AUD-PD-0007`, `AUD-PD-0012`에 고정했다.
2. **인접 문서가 늘 더 직접적이다:** Terminal Snippets 설계안과 AWS EMR helptext는 원 질문 어휘가 겹치지만 필요한 실행 경계를 설명하지 않는다. CeTZ bezier는 구체적인 WASM 요구를 보여도 Pandoc resolver 해결책은 아니다.
3. **인접 정책이 주 근거를 반드시 해친다:** J2는 독립 jq 시험을 잃지만 남아 있는 매뉴얼이 같은 핵심 연산을 설명한다. J4도 원 입력과 매뉴얼의 충분성이 유지된다. 이 표본에서는 A 단독 완결을 확인하지 못했다.
4. **한 건의 B 이득이 안정적이다:** P1은 helper 호출로 바꾸는 것을 허용한 사전 해석에 의존한다. 내장 옵션 또는 기존 호출 불변만 허용하면 B 단독 이득은 사라진다. 현재 태그와 최초 태그의 차이도 모집 민감도에 남긴다.
5. **원 시험이라는 이름이면 독립 근거다:** CeTZ의 `tests/empty/test.typ`는 주석 한 줄이어서 최소 개수에서 제외한다. jq `tests/man.test`는 매뉴얼 예제에서 파생된 중복 근거로 별도 독립 시험 개수에 넣지 않는다. CeTZ helper도 독립 회귀 사례로 중복 산입하지 않는다.

주 A/B 승패가 같으면서 필수 실패 조건이 제거되었다고 확정할 사례는 찾지 못했다. 구조 확인·독립 시험·빌드 제약의 발견은 기록했지만 제거된 실패로 승격하지 않았다. 이 부재는 작은 제한 코퍼스의 관측이며 일반적 불가능성 주장이 아니다.

## 다시 만들기

`python -B docs/workstreams/research/AF-RES-100/assemble_supplement.py --check`

고정 원문 캐시가 없으면 `hydrate_ledgers.py`와 `restore_cache.py --all`을 먼저 실행한다. 이 명령은 보존한 실제 읽기 영수증과 주석을 재조합하며 새로운 독립 읽기나 상류 시험 실행을 뜻하지 않는다. 원 상류 시험 4개 이상을 직접 읽었지만 jq/sed/knitr/CeTZ의 버전 일치 시험 실행은 아직 수행하지 않았다. 다른 분야의 별도 로컬 smoke는 `crossdomain/report.md`에서 판 차이와 함께 보고한다.
