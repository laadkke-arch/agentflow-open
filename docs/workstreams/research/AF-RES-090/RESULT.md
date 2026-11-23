# RESULT — AF-RES-090

**연구 상태: PARTIAL.** 현재의 제한된 독자 경로를 비교했다. 아래 판정은 역사적 제공·배포·빌드 성공에 대한 재판정이 아니다. 직접 원자료와 실패 응답을 모두 보존했으며, 지정판 본문·후속 자원·판 관계를 따로 채점했다.

## 표 1. 목적과 고정된 비교 조건

| 프로젝트·독자 목적 | 발행자 약속 또는 연구 조건 | 목표판·절·후속 자원 | 시작 A·B URL | 성공 기준 | 미확인 |
|---|---|---|---|---|---|
| P3 cibuildwheel · 3.3.0 설정을 인용하는 독자 (`P3-body`) | [PY-P3-README](https://raw.githubusercontent.com/pypa/cibuildwheel/63fd63b352a9a8bdcc24791c9dbee952ee9a8abc/README.md)는 free-threading 설명을 stable/options에 연결한다. 3.3.0 본문 확인은 연구 조건. | 3.3.0 · enable · cpython-freethreading, 3.13/3.14+ 구별. 후속 없음. | [A](https://cibuildwheel.pypa.io/en/stable/options/#enable) · [B](https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable) | 판과 설정 값을 같은 열람 경로에서 식별 | stable의 정확한 현재 릴리스 번호·실행 성공 |
| P3 · Python2 등 구계열 지원 표가 필요한 독자 (`P3-next`) | [PY-P3-README](https://raw.githubusercontent.com/pypa/cibuildwheel/63fd63b352a9a8bdcc24791c9dbee952ee9a8abc/README.md)의 “cibuildwheel 1 documentation” 안내. root의 지원 표를 연구 목표로 봉인. | 1.x root의 지원 matrix. 봉인 원URI [1.x/](https://cibuildwheel.pypa.io/en/1.x/). 목적판은 3.3.0과 다른 계열. | [A](https://cibuildwheel.pypa.io/en/stable/options/#enable) · [B](https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable) | 2회 안에 그 표·목적판을 함께 읽음 | options의 다른 표는 목표 대체 불가. patch판 미확인 |
| P1 bandersnatch · 7.0.1 첫 설정 예제 인용 (`P1-body`) | [PY-P1-README](https://raw.githubusercontent.com/pypa/bandersnatch/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/README.md)의 안내는 latest. [PY-P1-CONFIG-SOURCE](https://raw.githubusercontent.com/pypa/bandersnatch/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/docs/mirror_configuration.md)의 첫 Minmal을 연구 조건으로 선택. | 7.0.1 · Mirror Configuration → Examples → Minmal, 첫 ini block | [A](https://bandersnatch.readthedocs.io/en/latest/) · [B](https://bandersnatch.readthedocs.io/en/7.0.1/) | 7.0.1 판과 첫 예제 모두 확인 | named 7.0.1의 현재 본문; mirror 실행 |
| P1 · 첫 예제의 upstream 확인 (`P1-next`) | [PY-P1-CONFIG-SOURCE](https://raw.githubusercontent.com/pypa/bandersnatch/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/docs/mirror_configuration.md) L23 master의 원URI. 발행자의 동일판 외부서비스 약속은 없음. | master = [https://pypi.org](https://pypi.org). 코드의 문자 URI이며 비고정 서비스. | [A](https://bandersnatch.readthedocs.io/en/latest/) · [B](https://bandersnatch.readthedocs.io/en/7.0.1/) | 2회 안에 해당 URI의 실제 응답을 읽고 판 관계를 별도 판정 | API/mirror 동작·7.0.1 당시 endpoint 내용 |
| R1 archive · 1.1.12 archive_read 설명 인용 (`R1-body`) | [R1-DESCRIPTION](https://raw.githubusercontent.com/r-lib/archive/a4c6ec37fc8737a189ca7ec7095ec0161888f9e8/DESCRIPTION)의 문서 안내와 [R1-FIXED-HTML](https://raw.githubusercontent.com/r-lib/archive/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html)의 실제 Usage/Examples. 고정판 인용은 연구 조건. | 1.1.12 · #ref-usage, #ref-examples | [A](https://archive.r-lib.org/reference/archive_read.html) · [B](https://github.com/r-lib/archive/blob/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html) | 지정판과 지정 본문을 함께 읽음 | 브라우저 렌더링·R 실행·앞으로의 URL 생존 |
| R1 · 예제의 첫 동작 참조 확인 (`R1-next`) | [R1-FIXED-HTML](https://raw.githubusercontent.com/r-lib/archive/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html) Examples의 첫 동작 관련 href를 DOM 순서로 선택. | 1.1.12 예제 → [system.file 도움말](https://rdrr.io/r/base/system.file.html). local data.zip 문자열보다 앞. | [A](https://archive.r-lib.org/reference/archive_read.html) · [B](https://github.com/r-lib/archive/blob/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html) | 2회 내 도움말 payload 확인; 생성 당시 R판과 관계는 별도 | 외부 도움말이 archive 생성 당시 R판인지 |
| R2 asciicast · 2.3.1 엔진·SVG 설정 설명 읽기 (`R2-body`) | [R2-DESCRIPTION](https://raw.githubusercontent.com/r-lib/asciicast/f992b26f3cb30c799fbb95f6148852d8ae8a7f18/DESCRIPTION)와 [R2-FIXED-HTML](https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html)의 init_knitr_engine 및 Using SVG files 안내. | 2.3.1 · #example, #using-svg-files | [A](https://asciicast.r-lib.org/articles/asciicast-demo.html) · [B](https://github.com/r-lib/asciicast/blob/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html) | 2.3.1 표지와 지정 본문·옵션을 식별 | 실제 SVG/JS/R 실행은 본문 읽기와 별개 |
| R2 · Using SVG files의 실제 출력 자원 확인 (`R2-next`) | [R2-FIXED-HTML](https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html)에서 첫 SVG/재생 자원 또는 내장 payload를 찾도록 봉인. options 함수 링크로 교체하지 않음. | 첫 내장 정적 pre 출력 341B. SVG/cast/player payload 경로 없음. | [A](https://asciicast.r-lib.org/articles/asciicast-demo.html) · [B](https://github.com/r-lib/asciicast/blob/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html) | 요구 SVG/재생 payload와 정적 텍스트 읽힘을 분리; 내장 출력은 추가0회 | SVG/재생 자원 부재를 재생 성공으로 표시하지 않음 |

## 표 2. 16판독의 실제 도착과 판정

| 목적·A/B | 실제로 연 URL 순서·횟수 | 마지막 판·본문·자원 관측 | 동일판 근거 URL·지문 | 실패·수동 재구성·미확인 |
|---|---|---|---|---|
| P3-body-A | [1](https://cibuildwheel.pypa.io/en/stable/options/#enable) (200) → [2](https://cibuildwheel.pypa.io/en/v3.3.0/options/) (200); **2회**, 305,710B | 처음 stable에는 목표 free-threading 값이 없음. 버전 메뉴 뒤 v3.3.0의 enable을 읽음.<br>본문 확인 / 후속 해당 없음 / 목적별 판 확인 | [PY-P3-OPTIONS-SOURCE](https://raw.githubusercontent.com/pypa/cibuildwheel/63fd63b352a9a8bdcc24791c9dbee952ee9a8abc/docs/options.md); 마지막 응답 SHA256 `4576ddf765b2…`; [영수증](streams/python/evidence/PY-READ-P3-body-A-2.receipt.json) | 첫 화면 판 반박 → 최종 확인. 메뉴 펼치기는 문서0회. 수동 조립 없음. |
| P3-body-B | [1](https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable) (200); **1회**, 146,504B | v3.3.0에서 3.13 opt-in과3.14+ 기본 포함을 읽음.<br>본문 확인 / 후속 해당 없음 / 목적별 판 확인 | [PY-P3-OPTIONS-SOURCE](https://raw.githubusercontent.com/pypa/cibuildwheel/63fd63b352a9a8bdcc24791c9dbee952ee9a8abc/docs/options.md); 마지막 응답 SHA256 `4576ddf765b2…`; [영수증](streams/python/evidence/PY-READ-P3-body-B-1.receipt.json) | 본문에서 종료. 실행성은 미확인. |
| P3-next-A | [1](https://cibuildwheel.pypa.io/en/stable/options/#enable) (200) → [2](https://cibuildwheel.pypa.io/en/1.x/options/) (200); **2회**, 212,371B | 1.x/options의 cp27·pp27 표는 읽힘. 봉인한 root 지원 matrix는 없음. 앞서 읽은 stable 본문도 목표3.3.0과 다름.<br>본문 판 반박 / 후속 미확인 / 목적별 판 확인 | [PY-P3-LEGACY-ROOT](https://cibuildwheel.pypa.io/en/1.x/); 마지막 응답 SHA256 `42cd3d28c09d…`; [영수증](streams/python/evidence/PY-READ-P3-next-A-2.receipt.json) | 목표 표 미도달·예산 소진. 같은 판=목적 legacy1.x이며3.3.0과 동일 release라는 뜻 아님. |
| P3-next-B | [1](https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable) (200) → [2](https://cibuildwheel.pypa.io/en/1.x/options/) (200); **2회**, 199,669B | 앞서3.3.0 본문은 읽음. 마지막1.x/options에는 다른 identifier 표만 있음.<br>본문 확인 / 후속 미확인 / 목적별 판 확인 | [PY-P3-LEGACY-ROOT](https://cibuildwheel.pypa.io/en/1.x/); 마지막 응답 SHA256 `42cd3d28c09d…`; [영수증](streams/python/evidence/PY-READ-P3-next-B-2.receipt.json) | 목표 root 표는 추가 Home 열람이 필요하나 중단. 다른 표로 사후 대체하지 않음. |
| P1-body-A | [1](https://bandersnatch.readthedocs.io/en/latest/) (200) → [2](https://bandersnatch.readthedocs.io/en/latest/mirror_configuration.html#minmal) (200); **2회**, 168,571B | Mirror Configuration 제목/탐색판8.2.0. 첫 Minmal395문자는7.0.1과 같음.<br>본문 판 반박 / 후속 해당 없음 / 목적별 판 판 반박 | [PY-P1-CONFIG-SOURCE](https://raw.githubusercontent.com/pypa/bandersnatch/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/docs/mirror_configuration.md); 마지막 응답 SHA256 `f2215df9a8ae…`; [영수증](streams/python/evidence/PY-READ-P1-body-A-2.receipt.json) | 예제 텍스트 동일과 문서판 동일을 구분. 지정7.0.1 판 반박. |
| P1-body-B | [1](https://bandersnatch.readthedocs.io/en/7.0.1/) (404); **1회**, 2,543B | 404 오류 본문. 지정판이나 예제 없음.<br>본문 접근 불가 / 후속 해당 없음 / 목적별 판 미확인 | [PY-P1-CONFIG-SOURCE](https://raw.githubusercontent.com/pypa/bandersnatch/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/docs/mirror_configuration.md); 마지막 응답 SHA256 `09fd43d02642…`; [영수증](streams/python/evidence/PY-READ-P1-body-B-1.receipt.json) | 입구1회에서 종료. 보조 고정 소스로 주 실패를 치환하지 않음. |
| P1-next-A | [1](https://bandersnatch.readthedocs.io/en/latest/) (200) → [2](https://bandersnatch.readthedocs.io/en/latest/mirror_configuration.html#minmal) (200); **2회**, 168,571B | 8.2.0 설정까지2회. master URI는 span 문자로만 보이며 PyPI는 주 경로에서 열지 못함.<br>본문 판 반박 / 후속 미확인 / 목적별 판 미확인 | [PY-P1-CONFIG-SOURCE](https://raw.githubusercontent.com/pypa/bandersnatch/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/docs/mirror_configuration.md); 마지막 응답 SHA256 `f2215df9a8ae…`; [영수증](streams/python/evidence/PY-READ-P1-next-A-2.receipt.json) | 수동 복사라면 세 번째 문서가 필요. 실제 주 경로 수동 조립0; 후속 미확인. |
| P1-next-B | [1](https://bandersnatch.readthedocs.io/en/7.0.1/) (404); **1회**, 2,543B | 입구404. 다음 URI까지 읽지 못함.<br>본문 접근 불가 / 후속 접근 불가 / 목적별 판 미확인 | [PY-P1-CONFIG-SOURCE](https://raw.githubusercontent.com/pypa/bandersnatch/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/docs/mirror_configuration.md); 마지막 응답 SHA256 `09fd43d02642…`; [영수증](streams/python/evidence/PY-READ-P1-next-B-1.receipt.json) | 접근 불가. 보조 PyPI200은 이 행의 성공이 아님. |
| R1-body-A | [1](https://archive.r-lib.org/reference/archive_read.html) (200); **1회**, 14,062B | 본문 표지1.1.14. Usage139B·Examples1401B 코드 텍스트는1.1.12와 같음.<br>본문 판 반박 / 후속 해당 없음 / 목적별 판 판 반박 | [R1-FIXED-HTML](https://raw.githubusercontent.com/r-lib/archive/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html); 마지막 응답 SHA256 `6f173ffa014d…`; [영수증](streams/r/evidence/R-R1-body-A-1.receipt.json) | 지정판 반박. 코드 읽힘은 보존; HTML 전체 동일 주장은 하지 않음. |
| R1-body-B | [1](https://github.com/r-lib/archive/blob/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html) (503); **1회**, 56,635B | GitHub Unicorn! 오류 HTML503. 목표 소스는 이 응답에 없음.<br>본문 접근 불가 / 후속 해당 없음 / 목적별 판 미확인 | [R1-FIXED-HTML](https://raw.githubusercontent.com/r-lib/archive/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html); 마지막 응답 SHA256 `5ea81d0616df…`; [영수증](streams/r/evidence/R-R1-body-B-1.receipt.json) | 1회 종료. 사전/UI200과 다른 관측; 원인·지속성 미확인. |
| R1-next-A | [1](https://archive.r-lib.org/reference/archive_read.html) (200) → [2](https://rdrr.io/r/base/system.file.html) (200); **2회**, 97,167B | 현재1.1.14 본문 → system.file 도움말200. 실제 참조 내용 읽힘.<br>본문 판 반박 / 후속 확인 / 목적별 판 미확인 | [R1-SYSTEMFILE-OFFICIAL](https://stat.ethz.ch/R-manual/R-devel/library/base/html/system.file.html); 마지막 응답 SHA256 `ecea655d27ed…`; [영수증](streams/r/evidence/R-R1-next-A-2.receipt.json) | 외부 도움말 R판과 archive1.1.12 생성판 관계 미확인. 수동 조립 없음. |
| R1-next-B | [1](https://github.com/r-lib/archive/blob/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html) (503); **1회**, 56,635B | GitHub 입구503. 후속 참조에 도달하지 못함.<br>본문 접근 불가 / 후속 접근 불가 / 목적별 판 미확인 | [R1-FIXED-HTML](https://raw.githubusercontent.com/r-lib/archive/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html); 마지막 응답 SHA256 `5ea81d0616df…`; [영수증](streams/r/evidence/R-R1-next-B-1.receipt.json) | 1회 종료. UI에서 보인 URI 수동 복사 가능성은 보조 관측에만 둠. |
| R2-body-A | [1](https://asciicast.r-lib.org/articles/asciicast-demo.html) (200); **1회**, 15,974B | 렌더링 안내2.3.1의 init_knitr_engine·SVG 옵션 읽힘. article15974B는 고정 HTML과 같음.<br>본문 확인 / 후속 해당 없음 / 목적별 판 확인 | [R2-FIXED-HTML](https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html); 마지막 응답 SHA256 `c812426f5a97…`; [영수증](streams/r/evidence/R-R2-body-A-1.receipt.json) | 1회 본문 충족. 같은 HTML의 Source HEAD까지 고정됐다는 뜻은 아님. |
| R2-body-B | [1](https://github.com/r-lib/asciicast/blob/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html) (503); **1회**, 56,635B | GitHub 입구503. 본문판 미확인.<br>본문 접근 불가 / 후속 해당 없음 / 목적별 판 미확인 | [R2-FIXED-HTML](https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html); 마지막 응답 SHA256 `5ea81d0616df…`; [영수증](streams/r/evidence/R-R2-body-B-1.receipt.json) | 독립 next-B200으로 이 실패를 덮어쓰지 않음. |
| R2-next-A | [1](https://asciicast.r-lib.org/articles/asciicast-demo.html) (200); **1회**, 15,974B | 2.3.1 HTML의 정적 pre 출력2개, 첫341B. 추가 열람0. SVG/재생 payload 경로 없음.<br>본문 확인 / 후속 명시 경로 없음 / 목적별 판 확인 | [R2-FIXED-HTML](https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html); 마지막 응답 SHA256 `c812426f5a97…`; [영수증](streams/r/evidence/R-R2-next-A-1.receipt.json) | 정적 출력 확인; 엄격 후속축=no_explicit_path. JS/R 실행 미확인. |
| R2-next-B | [1](https://github.com/r-lib/asciicast/blob/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html) (200); **1회**, 370,786B | GitHub 소스200. rawLines를 복원한15974B가 고정 HTML과 같고 첫 정적 출력도 읽힘.<br>본문 확인 / 후속 명시 경로 없음 / 목적별 판 확인 | [R2-FIXED-HTML](https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html); 마지막 응답 SHA256 `da793c1187eb…`; [영수증](streams/r/evidence/R-R2-next-B-1.receipt.json); wrapper와 복원 HTML을 구분: 복원 `c812426f5a97…` | 소스 보기이며 렌더링 안내 아님. SVG/재생은 본문 내 명시 경로 없음; 정적 출력만 확인. |

## 표 3. 독자에게 반환할 링크와 주장 범위

| 독자에게 할 말 | 반환 URL·볼 절 | 본문에서 끝낼 조건 | 추가할 자원 URL 또는 유보 이유 | 반례·다음 확인 |
|---|---|---|---|---|
| P3 · 3.3.0 설정 설명을 인용하세요. | [v3.3.0/options/#enable](https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable) | 3.13 opt-in과3.14+ 기본 포함의 구별만 필요하면 한 절로 종료. | 이 목적에는 추가 자원 없음. | stable도 메뉴를 통해2회 안에 회복했다. 첫 화면만으로 불가라 판정하면 틀림. |
| P3 · 구계열 지원 matrix는 별도 표를 여세요. | [1.x/#what-does-it-do](https://cibuildwheel.pypa.io/en/1.x/#what-does-it-do) | cp27/pp27 identifier만 필요한 별도 목적에는 options 표로도 충분할 수 있음. | [3.3.0 본문](https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable)과 legacy 표를 함께 반환. 동일 release라는 설명 금지. | options 버전 메뉴가 정확한 root 표로 직행하는 새 링크가 생기면 재판정. |
| P1 · 7.0.1 인용에는 고정 설정 원문을 제시하세요. | [7.0.1 mirror_configuration.md · Minmal](https://raw.githubusercontent.com/pypa/bandersnatch/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/docs/mirror_configuration.md) | 첫 ini 예제395문자만 필요한 현재 사용 독자에게는8.2.0 예제도 내용상 같다고 한정 가능. | named7.0.1은404. 고정 소스 대안은 보조 비교에서 얻은 링크이며 원 B의 성공이 아님. | 최신 예제와판 동일을 혼동하지 않음. 7.0.1 named 응답이 복구되면 새 회차로 확인. |
| P1 · master의 현재 서비스 확인 링크를 함께 주세요. | [고정 예제의 master 값](https://raw.githubusercontent.com/pypa/bandersnatch/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/docs/mirror_configuration.md) | 설정값을 읽기만 하면 본문에서 종료. | [PyPI 현재 홈페이지](https://pypi.org);7.0.1 귀속·API/mirror 성공은 유보. | 코드 URI는 클릭 불가 문자. current root→config 뒤 추가 열람은 세 번째. |
| R1 · 1.1.12 보존 내용은 HTML 소스로 읽는다고 알리세요. | [고정 archive_read.html](https://github.com/r-lib/archive/blob/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html) · ref-usage/ref-examples | Usage/Examples 코드만 필요하면 현재1.1.14에서도 같은 텍스트를 읽을 수 있음. | 고정 파일은 이번 HTTP 주 판독503, 보조 UI에서는 소스 확인. 렌더링 보장 유보. | Raw도 plaintext HTML이며 active href0. Raw를 거치면 외부 문서에 쓸 두 번째 열람을 소진. |
| R1 · system.file 참조는 외부 R 문서로 구분하세요. | [system.file 도움말](https://rdrr.io/r/base/system.file.html) | 로컬 package 경로 식의 뜻만 이해하면 참조 설명에서 종료. | 고정 본문과 함께 반환하되 생성 당시 R판 일치는 유보. | 같은 소스 tree에 data.zip이 있다는 사실은 웹독자의2회 도달 증거가 아님. |
| R2 · 2.3.1 설명·정적 출력은 현재 안내 한 파일로 읽을 수 있습니다. | [asciicast-demo · Example / Using SVG files](https://asciicast.r-lib.org/articles/asciicast-demo.html) | 엔진 설정법과 이미 표시된 텍스트 결과만 필요하면 추가0회. | 과거 인용이면 [고정 HTML](https://github.com/r-lib/asciicast/blob/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html)을 보존 근거로 병기. | current/fixed HTML은 같지만 Source HEAD의 Rmd는 다름. 고정 HTML=모든후속 고정이 아님. |
| R2 · SVG/재생 확인 요청에는 확인 범위를 유보하세요. | [Using SVG files](https://asciicast.r-lib.org/articles/asciicast-demo.html#using-svg-files) | 정적 pre 출력 읽기 목적은 충족. | 실제 SVG/cast/player URI 또는 내장payload가 없어 반환할 자원 없음. 다른 예제로 교체하지 않음. | 실제 SVG/XML·castJSON이 붙은 동일판 payload를 받으면 자원축을 다시 판정. |

## 모집·실행·비교 분모와 결원

모집은 지정된 **4프로젝트 × 2목적 × A/B = 16판독**, 목적별 **8대응쌍**이다. 대체 모집이나 중도 제외는 없다. 16행 모두 실제로 요청했고, 각 경로는 입구를 포함해 1~2문서에서 끝났다. 전체 **22문서 열람·1,890,350 응답 본문 bytes**이며 HTTP200은17응답,404는2응답,503은3응답이다. 이 수는 문서/자원의 응답 entity만 세며 브라우저 하위요청·TLS·헤더·검색·사람 독해 시간을 포함하지 않는다. 원장과 집계는 [traversals.csv](traversals.csv), [정규화 원행](evidence/normalized-traversals.json), [counts.json](evidence/counts.json)에 있다.

**지정판 본문 목적의 엄격한 충족은3/8**: P3 A/B, R2 A. **후속 목적의 엄격한 충족은0/8**: 지정 본문, 봉인한 후속 내용, 요구한 판 관계를 모두 만족한 행이 없다. 이것은 네 고정 자리의 현재 관측이며 서비스 전체 성공률 추정이 아니다. 단순히 후속 문서 payload를 읽은 것은 R1-next A **1/8**이고 그 외부 문서의 판 관계는 미확인이다. R2-next의 정적 출력2행은 확인됐지만 SVG/재생 성공 수에 넣지 않았다.

세 축을16행 전체에 적용하면 본문은 **확인6·판 반박5·접근 불가5**, 후속은 **확인1·명시 경로 없음2·미확인3·접근 불가2·해당 없음8**, 목적별 판은 **확인7·반박2·미확인7**이다. 본문축은 경로 중 읽은 지정판 본문을 뜻하므로 마지막 문서와 다를 수 있다. **판 확인7에는 P3의 legacy1.x 식별2행과 R2의 포함HTML/정적출력 식별2행이 들어 있다. 이것을 “본문과 외부 자원이 동일 release인7행”이라고 바꾸면 안 된다.** 엄격 성공은 각 목적의 대상·판 주어를 보존한 교집합이다.

자료 원장은 직접HTTP91행과 인수자료6행, 총97행이다. 미러·재요청·오류·선행 연구·tree/ref 메타데이터를 보수적으로 제외한 **고유 직접1차자료45건, 독립 저작·사건 계보18개**를 확보했다. 요구 구성은 발행자 안내/문서15≥8, 실제 다른 파일/후속자원17≥6, 생성·호스팅·경로 공식자료8≥6, 타분야 규격/실제저작5≥4다. 마지막5건은 IIIF 규격·공식manifest·실제사건과 EPUB 규격·실제패키지다. package와 그 안의 별개 파일은 별도 자료이고, 같은 파일의 ZIP 사본과 Git 사본은 중복 산입하지 않았다. [sources.jsonl](sources.jsonl), [assets.jsonl](assets.jsonl), [원장 집계 코드](tools/aggregate.py)

**PARTIAL의 이유는 빈칸을 음성 결과와 섞지 않기 위해서다.** 세 GitHub 주 입구의503으로 그 판독의 본문/후속은 접근 불가, R1 외부 R문서의 생성 당시 판 관계는 미확인, IIIF 과거 필수 tile 실패의 현재 재현은 proxy503 때문에 미확인이다. 반면 P1 named404, R2의 지정 절에 SVG/재생 payload가 없는 것, P3의 정확한 표 미도달은 실제 관측한 제한이다. JS·R/Python 예제 실행과 EPUB reader/viewer 실행은 실시하지 않았다. 실행 성공률은 **0/0 산출 불가**다. IIIF 과거 실패를 현재 origin 응답으로 완결 재현한 비율도 **0/0 산출 불가**다.

## 8대응쌍에서 실제로 갈린 것

| 대응 목적 | 실제 열람 | 비교 결과 |
|---|---|---|
| P3-body | A2회 / B1회 | 둘 다 지정 본문 확인. 고정 입구가 한 문서 적지만 이동 서비스도 메뉴를 통해 회복 가능. |
| P3-next | A2회 / B2회 | 둘 다1.x/options. exact root 표는 미도달하나 cp27/pp27 정보는 읽힘. |
| P1-body | A2회 / B1회 | A는 다른 판의 같은 예제, B는404. 내용 동일과판 동일이 분리됨. |
| P1-next | A2회 / B1회 | A는 문자 URI 앞에서 예산 소진, B는 입구404. 둘 다 PyPI를 주 경로에서 못 읽음. |
| R1-body | A1회 / B1회 | A는 다른 판의 같은 코드, B는503. 보조 UI 소스200은 별도 관측. |
| R1-next | A2회 / B1회 | A는 외부 도움말을 읽으나 R판 관계 미확인, B는503. |
| R2-body | A1회 / B1회 | A에서2.3.1 본문 확인, B는503. 고정 파일 자체는 보조 증거로 존재 확인. |
| R2-next | A1회 / B1회 | A 렌더링 안내/B HTML소스 모두 같은 정적 출력; SVG/재생 자원은 명시 경로 없음. |

## 방법과 변경 이력

계약 도구로 고정한 실제 시작판은 `chore/workspace-foundation@c2709abf8d25163eed75a7553ebcbde966105b55`다. 계획판 `62a80b9f…`과 다름을 [SCOPE.md](SCOPE.md)에 보존했다. 선행 인계는 [AF-RES-086 HANDOFF@69075344](https://github.com/laadkke-arch/agentflow-open/blob/6907534462af729f409c52ce08d3331de22c96e6/docs/workstreams/research/AF-RES-086/HANDOFF.md), 선행 결과·cards/comparison/routes/claims는 [e6a79c3a의 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/e6a79c3ac05b84ea1c7db313233df1717cade756/docs/workstreams/research/AF-RES-086/RESULT.md)와 같은 디렉터리의 지정 파일을 인수했다. 선행의 주 관측창0/9나 P3 보조 캡처를 이번 현재 성공 분모에 더하지 않았다. [인수 파일 지문](evidence/inherited-inputs.json)

목적·선정 규칙은 원격 `973897922e07d0e63a4c68c377422b1a65ce0f27`, 시작문서·DOM 후보 봉인은 `c2a3f387cc962abd1ef383e39f750cc23ee5e51a`에 커밋했다. **목적지 요청은 이 두 번째 원격 커밋 뒤에 시작했다.** 실제 판독·반례·타분야 원장은 `833071b378ab379188c7b62c4a013621a4958bdf`에 커밋했다. 후보 선정의 원값은 [Python freeze](streams/python/freeze.json), [R freeze](streams/r/freeze.json), [UI freeze](streams/ui/freeze.json)에 남아 있다. 최종 결과/검사/HANDOFF SHA는 마지막 인계에서 연결한다.

P1에서는 첫 Minmal 예제의 경계를 먼저 고정했다. 그 코드에서 최초 웹 URI는 master의PyPI이고 `/srv/pypi`는 로컬 출력경로다. 뒤의 filtering 링크가 클릭하기 쉽다고 바꾸지 않았다. P3는 README의 원URI `/en/1.x/`와 root 지원 표를 봉인했다. 실제 `#what-does-it-do` anchor는 보조 원문 열람에서 확인한 값으로, 봉인 전 원URI에 fragment가 있었다고 소급하지 않는다. R1은 Examples 안 첫 동작 href인 system.file을 선택했고 Arguments 절의 앞선 링크나 로컬data.zip으로 바꾸지 않았다. R2는 Using SVG files 안의 payload를 조사해 정적 출력과 실제SVG/재생 경로 부재를 함께 봉인했다. [targets.csv](targets.csv)

판독은 봉인된 실제 href/URI를 HTTP로 각각 독립 요청했다. 정적 HTML만으로 파악할 수 없는 ReadTheDocs shadow-DOM 메뉴와 GitHub Raw 버튼은 실제 브라우저에서 조작했다. 메뉴 펼치기·동일 문서 anchor 이동은 문서0회, HTML/자원 새 응답은1회다. HTTP 자동redirect는 같은 열람의 체인에 기록한다. 모든 경로에서 실제 도달점 이후는 주 예산 밖으로 남겼다. 소스 복원·tree 대조·공식문서·타분야는 보조 연구 예산이다. [UI observations](streams/ui/observations.json)

R2-next를 처음 “정적 출력 확인”이라는 넓은 의미의 confirmed로 작성한 해석은 독립 검산에서 바로잡았다. 봉인 목표와 실제 데이터는 변경하지 않았고, 최종 `followup_resource=no_explicit_path`, `static_output=confirmed`로 분리했다. 이전값·수정 이유·UTC는 [R-coding-adjustment](streams/r/evidence/R-coding-adjustment.json)에 보존했다. 독립 검산은 [peer-review](streams/cross/peer-review.json)에서 P1의 예제 경계, P3의 두 표, R503, R2의 소스복원 해시와 분모를 다시 확인했다.

## Q1–Q3. 누구의 어떤 목적에서 한 절이 충분한가

발행자에게 확인한 약속은 “안내되는 문서·지원 정보·예제”의 범위다. 네 프로젝트 모두가 고정판 URL이나 전이된 모든 자원의 영구 보존을 보장한다고 가정하지 않았다. 독자가 과거판을 정확히 인용해야 한다는 조건은 연구자가 명시한 목적이다. P3의 고정 README에는 Python2 등 현재 미지원 Python의 독자를 구계열 문서로 안내하는 문장이 있다. P1 README는 latest로 연결하지만 고정 source의 첫 예제에 directory·master·workers·timeout 등의 실제 값이 있다. R1의 Usage는 archive 안 파일을 읽는 연결을 설명하고 Examples는 system.file을 사용한다. R2는 init_knitr_engine과 SVG 옵션을 설명하지만 현재 생성 HTML의 출력 표현은 정적 텍스트다. [PY-P3-README/PY-P1-README/R1-DESCRIPTION/R2-DESCRIPTION와 표1의 고정 원문]

실제 내용 차이는 판 표지에 덧붙여 확인했다. P3 stable의 enable에는 `cpython-freethreading` 항목이 없고 `pyodide-eol`이 있다. 고정3.3.0에는3.13 opt-in과3.14+의 차이가 있다. 그래서 stable이라는200 응답만으로 목표판 성공이라 할 수 없다. 그러나 실제 메뉴에서3.3.0으로 이동한 A-body는2회 안에 성공한다. 이 긍정 반례 때문에 “이동 서비스 입구는 항상 부적합”이라는 결론도 성립하지 않는다. [PY-P3-START-A/B, UI-P3-BODY-A]

반대로 P1의 최신8.2.0과 고정7.0.1의 첫 Minmal 코드는 태그 제거·entity 해제 뒤 공백을 보존한395문자 전체가 같다. 지문은 `6850998fbae53e09075799d6576191d7a66be2d9083ca9baf5ef285c81562c6c`다. R1도 Usage139B와 Examples1401B의 추출 코드가 각각 같다. 따라서 지금 그 문장을 이해하려는 독자에게 유용할 수 있으나, 그 내용만으로 문서판7.0.1/1.1.12를 식별하면 틀린다. [Python comparison](streams/python/evidence/comparison.json), [R1 section comparison](streams/r/evidence/R1-section-comparison.json)

같은 판 표지를 가진 두 생성 HTML의 본문이 다르다는 직접 사례는 이번 지정 네 자리에서 확보하지 못했다. R2의 표지2.3.1과 article HTML은 오히려 동일했다. 다음 절의 Source HEAD 차이는 **연결된 원문 파일의 차이**이며 그 자리를 “같은 표지의 HTML 본문 차이”로 바꾸지 않았다. 해당 좁은 반례는 미확인이고, 다음 최소 관측은 같은2.3.1 표지를 가진 별도 생성파일 두 개의 본문·해시를 실제로 확보하는 것이다.

## Q4–Q5. 고정된 파일과 다음 자원의 관계

P3의 version menu는 경로를 유지해서1.x/options로 이동한다. root matrix의9개 OS 열과 도착options의4개 묶음 열은 다른 표이며 table 지문도 다르다. 두 번째 문서에cp27/pp27이 있다는 사실은 “아무 구계열 정보도 읽을 수 없다”는 주장을 반박하지만, 처음 정한 정확한 표 성공으로 승격하지는 않는다. 이 목표에는 본문 링크와root 표 링크의 조합이 독자에게 더 명확하다. [PY-READ-P3-next-A-2/B-2, PY-P3-LEGACY-ROOT]

R1의 GitHub blob에는 보존된 HTML과1.1.12 표지가 있으며 source tree의 data.zip도 실제 존재한다. 하지만 브라우저에서 blob은 HTML 코드 보기다. 실제 Raw 버튼을 누르면 raw.githubusercontent.com의 plaintext HTML이 나오며 active link는0개다. source 속system.file URI를 직접 복사하면 이론상 blob→외부문서2회가 가능하지만, 이번 엄격 주 B 경로는 입구503에서 끝났다. Raw를 먼저 거친 보조 경로는 그 자체로2회이므로 외부문서는 세 번째가 된다. 파일 존재, URI 문자열 확인, 실제 클릭 도달, 같은 판 귀속은 별개다. [R1-FIXED-HTML/R1-GENERATED-TREE/R1-DATA-ZIP, UI-R1-RAW]

R2 current와 fixed article은15,974B·SHA256 `c812426f5a97f8361e64a7a3beb8a35d5dde4bd2270b70dc1f1567080471ca0c`로 같다. current/fixed의 init_knitr_engine reference도10,917B로 같고 pkgdown.js도4,406B로 같다. 이 두 정상 대조를 함께 보존했다. 그러나 article의 Source 링크는 `blob/HEAD/vignettes/asciicast-demo.Rmd`다. 원2.3.1 source의4,419B와 현재4,440B는 다르고, 현재HEAD를 `a0076449feec11c835ff46f7934fe75232f7d759`에 고정한 재응답은 현재파일과 일치한다. 내용 차이는 chunk 옵션 표현의 `#|` 형식 등이며, 이것만으로 실행 동작 변화나 새 named version을 주장하지 않는다. [R2-RMD-FIXED/HEAD/HEAD-PINNED, resource comparisons](streams/r/evidence/R-resource-comparisons.json)

또 다른 절의 문자 `../inst/examples/hello.R`을 현재 웹주소에 수동으로 해석하면404지만, 고정 source tree에는22B script가 있고 안내 본문에 Hello world 정적 출력도 있다. 이것은 “상대 경로가 깨지면 본문도 쓸모없다”의 반례다. 해당 문자열은 href가 아니며, 주SVG 목적을 이 쉬운 예제로 교체하지 않았다. R2의 Using SVG files에는 출력pre2개가 있고 첫출력은341B·SHA256 `64eb0d80bae83cc4b40efc545937d1ea82807edffce84f750f781d0a470fd376`다. 이 정적 출력 읽기는 추가0회지만 SVG XML·castJSON·재생 payload 성공은 아니다. [R2-HELLO-WEB-LITERAL/R2-HELLO-FIXED/R2-FIXED-HTML]

## 생성·호스팅·경로 규칙의 공식 대조

| 자료 | 직접 읽은 규칙과 적용 | 넘어갈 수 없는 한계 |
|---|---|---|
| [M01](https://docs.github.com/en/repositories/working-with-files/using-files/getting-permanent-links-to-files) | commit ID의 permalink는 선택한 파일판을 고정하는 주소다. | 파일 안 외부URI까지 고정하지는 않는다. |
| [M02](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files) | GitHub는 source/rich view를 구별하고 HTML commit richdiff 직접지원을 제한한다. | 그 정책만으로 모든Raw MIME를 추정하지 않음. 이번 두 URL의UI 관측을 별도로 사용. |
| [M03](https://html.spec.whatwg.org/multipage/urls-and-fetching.html) | HTML 상대URL은 첫base href 또는 document fallback URL을 기준으로 해석한다. | 소스 보기의href 문자열은 live anchor가 아니다. 위치가 다르면 같은HTML도 다른 목적지가 가능. |
| [M04](https://pkgdown.r-lib.org/reference/build_articles.html) | pkgdown은 외부 이미지 탐지와 resource_files 지정, 문서 output 형식을 설명한다. | 현재 설명은 과거 archive/asciicast 생성 실행의 증명이 아니다. |
| [M05](https://docs.readthedocs.com/platform/stable/versioning-schemes.html) | ReadTheDocs는 multi/single-version URL scheme을 설정하며 scheme변경시 링크가 깨질 수 있다고 설명한다. | 이 일반 규칙을 P1의404 원인으로 단정하지 않음. |
| [M06](https://www.mkdocs.org/user-guide/writing-your-docs/) | MkDocs는 Markdown 상대문서 링크를 HTML 출력경로로 변환하며anchor를 유지한다. | source URL과생성 URL은 자동으로 동일하지 않다. |
| [M07](https://www.sphinx-doc.org/en/master/usage/referencing.html) | Sphinx download role은 실제 파일을 _downloads의해시경로로 복사하고 링크한다. | role의존재와해당출력파일의현재존재는 별도검증 대상. |
| [XF-IIIF-PROCESS](https://iiif.io/api/cookbook/recipe/) | IIIF Cookbook은 실제 recipe와안정적으로관리할이미지자원을연결하도록작성규칙을둔다. | 규칙이 있다는 사실로 모든공개manifest의현재외부이미지성공을대신할수없다. |

## Q7. IIIF와 EPUB에서 확인한 적용 조건과 반례

IIIF는 식별자와 별도 열어야 하는 필수 자원을 구별한다. [Presentation 3.0 Canvas 규격](https://iiif.io/api/presentation/3.0/#53-canvas)과 [실제 공식 manifest](https://iiif.io/api/cookbook/recipe/0001-mvm-image/manifest.json)를 직접 읽었다. 1,188B manifest에 Canvas·AnnotationPage·painting Annotation이 내장되어 있다. 그 [Canvas URI](https://iiif.io/api/cookbook/recipe/0001-mvm-image/canvas/p1)는 301 뒤 `https://iiif.io//404.html`의 HTTP 200·HTML 오류 페이지로 끝났지만, 필수 [PNG](https://iiif.io/api/presentation/2.1/example/fixtures/resources/page1-full.png)는 200·128,352B·1200×1800으로 manifest 선언과 맞았다. 내장 Canvas의 설명을 읽는 데는 추가 0회다. 별도 id의 soft 404를 필수 이미지 실패로 세면 오판이다. [XF-IIIF-SPEC/MANIFEST/CANVAS/IMAGE]

반대 방향에는 [Internet Archive IIIF 사건 61](https://github.com/internetarchive/iiif/issues/61)의 실제 2024-03-04 제보가 있다. 제보자는 manifest/viewer와 tile 404를 함께 제시했고, 댓글은 예외가 404로 변환될 수 있다고 원인 추정을 정정한다. 이번에 [old manifest](https://iiif.archivelab.org/iiif/naeb-b101-f02-23/manifest.json)와 [old tile](https://iiif.archivelab.org/iiif/naeb-b101-f02-23$0/1024,2048,1024,1024/256,/0/default.jpg)을 열었지만 proxy 503이었다. [댓글의 대체 tile](https://iiif.archive.org/iiif/naeb-b101-f02-23$0/1024,2048,1024,1024/256,/0/default.jpg)은 301 뒤 200·JPEG·25,134B였다. 현재 필수 이미지 연결은 2쌍 시도 중 1쌍 판정 가능·1쌍 미확인이고, 판정 가능 쌍의 필수 이미지 실패는 0/1이다. 과거 404 제보와 현재 503을 합쳐 현재 origin 실패라고 쓰지 않았다. [XF-IIIF-INCIDENT/INCIDENT-COMMENTS/NAEB-MANIFEST/OLD-TILE/NEW-TILE]

[W3C EPUB 3.3 고정 규격](https://www.w3.org/TR/2026/REC-epub-33-20260113/)과 [공개 Accessible EPUB3](https://github.com/IDPF/epub3-samples/releases/download/20230704/accessible_epub_3.epub)를 직접 읽었다. 실제 4,051,892B ZIP의 container→package.opf→spine/cover.xhtml→내부 JPEG를 추적했다. ZIP 38 entries, manifest 35항목 모두 실재, spine 22항목 모두 연결, manifest remote href 0이었다. 표지 목적은 인라인 CSS와 패키지 내 JPEG로 충족될 정적 자료를 갖추므로 별도 인터넷 그림 링크를 추가할 필요가 없다. 그러나 규격은 일부 remote resource를 허용하며 실제 ch04에는 외부 O’Reilly 탐색 링크도 있다. 35/35는 선언된 파일 존재의 검사이지 전체 독서기 실행이나 외부 링크 생존을 확인한 값이 아니다. [XF-EPUB-SPEC/PACKAGE/ROOT/OPF/COVER/COVER-IMAGE/CH04]

동일 소스 태그 20230704는 `46d7e07e1b39b2d0a0245ececaf896edcd9de4b2`다. Git 소스와 ZIP의 표지 JPEG 820,269B는 원바이트가 같다. container/OPF/XHTML은 CRLF 차이 때문에 원바이트가 다르지만 CRLF→LF 변환 후 같다. 원바이트 동일과 정규화 내용 동일을 나누어 [package audit](streams/cross/evidence/epub-package-audit.json)과 [Q7 상세](streams/cross/findings.md)에 남겼다. EPUB reader/viewer 실행은 미확인이다.

소프트웨어 도움말에 옮길 수 있는 조건은 세 가지다. 독자가 원하는 내용이 본문/내장 표현에 완전히 들어 있으면 추가 열람 0으로 취급한다. 필수 자원이 외부에 있으면 그 실제 payload와 판 관계를 별도로 확인한다. 목록·tree·spine의 존재만으로 자원 도달이나 실행 성공을 대신하지 않는다. 이 조건은 HTTP 문서와 패키지 내부 파일의 전송 단위가 다르다는 한계를 함께 둔다. EPUB의 내부 파일 해결을 웹의 한 번 클릭과 같은 비용으로 환산하지 않았다.

## Q6. 현재 사용자·과거판 인용자·보존 발행자의 선택

현재 사용자는 필요한 한 절과 값을 읽었는지부터 판단할 수 있다. P3 설정, P1 첫 예제, R1 Usage/Examples, R2 정적 출력은 좁은 목적에서 본문만으로 유용하다. 다만 P1/R1 현재판의 내용 동일성은 그 문서가 과거판이라는 인용을 허용하지 않는다. 과거판 인용자는 고정 source/생성 HTML과 판별 근거를 받아야 하고, 필요한 후속 자원이 외부라면 판 연결의 미확인을 함께 받아야 한다. 발행자는 생성 HTML뿐 아니라 필수 파일의 tree/manifest·기준 URL·자원 지문과 내장 여부를 보존하면 좋다. 이는 이번 증거에서 내린 설계 제안이며 어느 호스팅 제품의 영구 보존 보장이라고 쓰지 않는다. 실제 배포하거나 생성기를 다시 실행하지 않았다. [cards.md](cards.md), M01/M03/M04/M07, Q7 자료

사람 소요 시간·비용·읽기 난이도는 측정하지 않았다. 주 16판독의 바이트는 본문 entity에 한정되어 GitHub source wrapper 370,786B와 실제 HTML 15,974B의 차이도 드러낸다. 큰 응답이 독자에게 더 느리거나 불편했다는 인과 주장은 하지 않는다. HTTP 수집 전체는 주 판독 외에 예비·보조 자료가 포함되며, 이 추가 요청을 독자 2회 예산에 숨겨 넣지 않았다. 수동 URI 복사와 상대 경로 조립도 구분했다. 주 16행에서 실제 수동 조립은 0회이며, P1의 필요 수동 복사는 예산 때문에 실시하지 못했다. R2 hello.R의 웹 경로 조립은 명시적으로 보조 반례 관측이다.

## 검증 범위와 재실행

자료별 원출처·열람 UTC·판/파일/절·관측·지문·지지/반박·한계·재열람 경로는 [sources.jsonl](sources.jsonl)에 있다. 짧은 본문 발췌와 실패 영수증은 각 stream의 evidence/에 커밋했다. 다운로드 전체 raw cache는 임시 검산용으로만 썼고 고유 자료 수를 늘리지 않았다. Python stream 48검사, R stream 원응답/복원 해시 검사, IIIF/EPUB 21응답·ZIP 연결 검사는 각 검산 영수증에서 대상 작업트리와 시점을 구분했다. 통합 Q1–Q7 검산은 [SELF_CHECK.md](SELF_CHECK.md)에 있다.

최종 결과 SHA에서 실행할 계약 검사는 `python -B -m workbench.session check docs/workstreams/research/AF-RES-090/manifest.json --fetch`, 공통 검사는 `python -B scripts/check.py --require-git`다. 실제 대상 SHA·명령·종료값은 이후 커밋되는 검사 영수증과 최종 HANDOFF에 적는다. 파일 안의 이 명령만으로 실행 완료라고 주장하지 않는다. 사례의 R/Python/JS 전체 실행과 EPUB reader 실행은 이 연구의 정적 읽기 결론에 더하지 않으며, 필요한 입력과 다음 행동은 HANDOFF에 남긴다.

## 마지막: 가장 중요한 불일치 또는 약점 정확히 3건

| 틀릴 수 있는 주장 | 다음 조사 대상·입력 | 판정을 바꿀 관측 |
|---|---|---|
| “고정 GitHub HTML 입구는 독자가 쓰기 어렵거나 못 읽는다.” 이번 주 B 3행 503과 보조 UI 200은 측정 수단·시점이 갈린다. | 같은 R1/R2 blob URL, 새 UTC를 고정한 일반 브라우저와 HTTP 동시 1회 관측. 각 2열람 제한, Raw 여부와 소스 모드 기록. | 정상 소스가 같은 시점 두 수단에서 읽히면 새 회차 접근축을 변경. 현재 16행은 보존. 렌더링 및 외부 href 도달까지 보이면 별도 판정 확장. |
| “현재 HTML이 같으면 다음 자료도 같은 판이다” 또는 “인라인 출력이 있으면 SVG가 성공했다.” R2는 두 주장 모두 지지하지 않는다. | R2 고정 2.3.1 HTML의 Using SVG 절과 Source HEAD/고정 Rmd; 실제 SVG XML/cast JSON이 있다면 그 원 URI·MIME·bytes·commit을 받음. R1은 생성 시 R 버전과 고정 system.file 문서. | 실제 재생 payload가 같은 판으로 연결되면 R2 자원축 변경. R1에 생성판 R 문서의 고정 근거가 생기면 외부 판 관계 변경. 정적 pre만으로는 변경하지 않음. |
| “목록에 있지만 열리지 않는 필수 자원 실패를 현재 직접 재현했다.” IIIF Canvas는 선택적 식별자이고 old IA는 proxy 503이라 그 강한 주장은 미확인. | 사건 61의 정확한 old manifest·tile URL을 정상 연결에서 같은 UTC 구간에 1회씩 열고 MIME/body/status를 함께 기록. P3에는 정확 root 표로 직행하는 현재 UI 후속 링크도 확인. | 정상 manifest와 필수 tile의 실패가 같은 현재 관측에서 연결되면 Q7 현재 실패 사례 확보. P3에서 봉인 root 표에 2회 내 도달하면 그 목적의 새 회차 점수 변경. |

