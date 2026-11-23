# 독자에게 반환할 링크와 읽을 범위

**연구 상태: PARTIAL.** 확인일은2026-11-23 UTC / 2026-11-24 KST다. 아래 카드는 본문을 읽는 목적과 다음 자료를 읽는 목적을 구별한다. 원 A/B 비교는 **16판독·8쌍·22열람**, 응답 본문 **1,890,350bytes**이며 지정판 본문 목적의 엄격한 성공은3/8, 후속 목적 전체의 엄격한 성공은0/8이다. 후속 문서 하나가 열리거나 정적 출력이 보이는 부분 확인도 별도로 남겼다. [evidence/counts.json](evidence/counts.json)

추가로 제안하는 고정 소스·표·자원 링크는 이번 보조 조회에서 실제 읽은 주소다. 이를 원래 입구에서 두 번 안에 도달한 성공으로 소급하지 않는다. 전체 예제 실행, Python/R 환경, SVG 애니메이션, 과거 서비스 제공과 미래 영구 보존은 이번 카드의 확인 범위에 포함되지 않는다.

## P3 — cibuildwheel 3.3.0

### 목적 가: 3.3.0의 enable 설명 읽기

**독자에게 할 말:** “[cibuildwheel 3.3.0의 enable 절](https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable)을 보세요. CPython3.13의 free-threading opt-in과3.14이상의 기본 포함을 이 절에서 구별할 수 있습니다. 설정 설명과 인라인 TOML/YAML 예제를 읽는 데는 이 링크 하나로 충분합니다.”

**실제 열람:** B 고정판 입구는1회로 지정 본문을 읽었다. A [stable/options](https://cibuildwheel.pypa.io/en/stable/options/#enable)는 첫 화면의 옵션이3.3.0과 달랐지만, 실제 버전 메뉴의 v3.3.0 항목을 따라2회째에 목표 본문으로 도착했다. 따라서 첫 화면이 다르다는 사실만으로 두 번 안의 읽기가 불가능하다고 말하지 않는다. 별도 실브라우저 클릭도 이 메뉴 경로를 확인했다.

**본문에서 끝낼 조건:** 해당 판의 enable 설정 설명과 예제 자체가 목적일 때. 지원 종료 Python의 OS별 지원표까지 필요하다면 아래1.x 링크를 추가한다. 원문 근거: [고정 README](https://github.com/pypa/cibuildwheel/blob/63fd63b352a9a8bdcc24791c9dbee952ee9a8abc/README.md), [고정 options 소스](https://github.com/pypa/cibuildwheel/blob/63fd63b352a9a8bdcc24791c9dbee952ee9a8abc/docs/options.md). 근거 ID: `PY-P3-README`, `PY-P3-START-B`, `PY-P3-OPTIONS-SOURCE`, `PY-READ-P3-body-A-2`, `PY-READ-P3-body-B-1`, `UI-P3-BODY-A`.

### 목적 나: 안내된1.x의 정확한 지원표 읽기

**독자에게 할 말:** “지원 종료 Python의 구계열 안내가 필요하면 [1.x의 What does it do? 지원표](https://cibuildwheel.pypa.io/en/1.x/#what-does-it-do)를 직접 보세요. 이 표에는 CPython2.7·PyPy2.7 등이 포함됩니다. **1.x는3.3.0과 같은 릴리스가 아닙니다.** 두 설명이 모두 필요할 때 위3.3.0 enable 링크와 이 표의 링크를 함께 드립니다.”

**실제 열람:** A/B 모두 두 번째 열람은 [1.x/options](https://cibuildwheel.pypa.io/en/1.x/options/)에 도착했다. 버전 메뉴가 현재의 options 경로를 유지했기 때문이다. 여기에는 cp27·pp27을 확인할 수 있는 다른 build-identifier 표가 있지만, 봉인한 root의 OS별 지원표에는 도달하지 못했다. root 표를 직접 연 보조 조회는200이었다. 그 보조 조회와 원 A/B 경로의 결과를 합치지 않는다.

**본문에서 끝낼 조건:** 필요한 것이 cp27·pp27 식별자 유무뿐이라면 도착한 options의 다른 표가 충분할 수 있다. 이번 목적처럼 root의 지정 지원표를 인용해야 하면 정확한 표 링크를 추가해야 한다. 다음 판정을 바꿀 관측은 원 options 입구의 현재 UI에서 root 표로 직접 연결되는 경로다. 근거 ID: `PY-READ-P3-next-A-2`, `PY-READ-P3-next-B-2`, `PY-P3-LEGACY-ROOT`, `UI-P3-NEXT-B`.

## P1 — bandersnatch 7.0.1

### 목적 가: 7.0.1의 첫 설정 예제 읽기

**독자에게 할 말:** “7.0.1의 첫 설정 예제를 인용하려면 [고정 소스의 Mirror Configuration → Examples → Minmal](https://github.com/pypa/bandersnatch/blob/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/docs/mirror_configuration.md#minmal)을 보세요. `Minmal`은 원문의 철자입니다. 이 주소는 고정 소스 문서이며7.0.1을 서비스하는 rendered 문서 주소가 아닙니다.”

**실제 열람:** B [named7.0.1 입구](https://bandersnatch.readthedocs.io/en/7.0.1/)는1회째404로 끝났다. A [latest root](https://bandersnatch.readthedocs.io/en/latest/)에서 [mirror_configuration#minmal](https://bandersnatch.readthedocs.io/en/latest/mirror_configuration.html#minmal)로2회째에 도착했지만 title/nav는8.2.0이다. 다만 첫 설정 예제395문자는 고정7.0.1 원문과 정확히 같았다. **예제 내용의 동일성은 확인했으며, latest를7.0.1 문서라고 소개하지 않는다.** 위 고정 소스 대안은 별도 보조 대조로 확보한 권고다.

**본문에서 끝낼 조건:** 첫 Minmal 예제의 값과 주석을 읽는 목적일 때는 고정 소스 한 파일로 충분하다. 후행 filtering 문서나 문서 말미의 `example.conf`를 추가할 필요는 없다. 특히 [고정 example.conf](https://github.com/pypa/bandersnatch/blob/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/src/bandersnatch/example.conf)의 timeout10/global-timeout1800과 첫 Minmal의15/18000은 다르므로 두 예제를 바꾸어 인용하지 않는다. 근거 ID: `PY-P1-CONFIG-SOURCE`, `PY-P1-TAG`, `PY-READ-P1-body-A-2`, `PY-READ-P1-body-B-1`, `PY-P1-EXAMPLE-CONF`.

### 목적 나: 첫 설정 예제가 지목한 upstream 확인

**독자에게 할 말:** “이 예제의 첫 동작 URI는 `master = https://pypi.org`입니다. upstream의 현재 홈페이지를 확인하려면 [PyPI](https://pypi.org)를 여세요. 이 링크는 bandersnatch7.0.1과 같은 판으로 고정된 자원 주소가 아닙니다. 홈페이지 확인만으로 mirror/API 동작까지 확인됐다고 말할 수 없습니다.”

**실제 열람:** A는 root와 설정 문서에 이미2회를 사용했다. master URI는 코드의 문자로 표시되고 해당 URI의 href는 없으므로, 주소창으로 **완전 URI를 수동 복사**해 열려면 세 번째 문서 열람이 필요하다. 주 판독은 설정 문서에서 끝났다. B는 named 입구404에서1회로 끝났다. PyPI 홈페이지의200은 별도 보조 요청에서 확인했다.

**추가 링크를 붙일 조건:** 예제 안의 master 값만 확인하면 위 고정 설정 문서에서 끝낼 수 있다. upstream 홈페이지 자체를 읽으려는 독자에게는 설정 문서와 PyPI 주소를 함께 제시한다. 뒤에 나오는 [고정 filtering 문서](https://github.com/pypa/bandersnatch/blob/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/docs/filtering_configuration.md)는 필터 설정을 별도로 묻는 경우에만 추가하며, 봉인한 첫 URI를 대신하지 않는다. 같은 판 관계는 미확인이다. 근거 ID: `PY-P1-CONFIG-SOURCE`, `PY-READ-P1-next-A-2`, `PY-READ-P1-next-B-1`, `PY-P1-UPSTREAM`, `PY-P1-FILTER-SOURCE`.

## R1 — archive 1.1.12

### 목적 가: archive_read의 Usage와 Examples 읽기

**독자에게 할 말:** “1.1.12의 설명은 [고정 archive_read HTML 원문](https://raw.githubusercontent.com/r-lib/archive/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html)에서 읽을 수 있습니다. 파일 안의 `ref-usage`와 `ref-examples`를 찾으세요. HTML 소스 텍스트이며 옛 사이트를 렌더링한 화면은 아닙니다. 함수 인자와 이미 출력된 예제를 읽는 목적은 이 파일 안에서 끝납니다.”

**실제 열람:** A [현재 archive_read](https://archive.r-lib.org/reference/archive_read.html)는1회로 읽혔지만1.1.14였다. B [고정 GitHub 파일 보기](https://github.com/r-lib/archive/blob/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html)의 주 판독은1회째HTTP503으로 끝났다. 고정 Raw 원문은 별도 보조 요청에서1.1.12와 지문을 확인했다. 사전 source 보기와 별도 실제 브라우저의 source→Raw2회 관측도 있었지만, 이 결과로 주 B의503을 대체하지 않는다.

**본문에서 끝낼 조건:** 지정판의 Usage·예제 코드·기록된 출력만 읽을 때. 현재1.1.14와 고정1.1.12의 Usage/Examples 코드 텍스트는 지정한 정규화 후 각각 동일했으므로, 코드 설명만 필요한 현재 독자에게 현재 페이지도 유용하다. 판 인용이 목적이면 고정 원문을 쓴다. ZIP이나 R 실행환경의 동작은 이 한 파일로 확인되지 않는다. 근거: [고정 DESCRIPTION](https://github.com/r-lib/archive/blob/a4c6ec37fc8737a189ca7ec7095ec0161888f9e8/DESCRIPTION), `R1-DESCRIPTION`, `R1-FIXED-HTML`, `R1-ENTRY-A`, `R-R1-body-B-1`, `UI-R1-RAW`, [선택 코드 대조](streams/r/evidence/R1-section-comparison.json).

### 목적 나: Examples의 첫 동작 참조 읽기

**독자에게 할 말:** “Examples에서 처음 연결한 함수 도움말은 [system.file](https://rdrr.io/r/base/system.file.html)입니다. 설치된 패키지 안의 파일을 찾는 동작이 필요하면 이 링크를 함께 보세요. 이 외부 문서가 archive1.1.12를 생성할 당시의 R판과 같은지는 확인하지 못했습니다.”

**실제 열람:** A에서는 현재 archive_read→system.file의2회 경로로 도움말200을 읽었다. 첫 문서는1.1.14이고 후속 URI는 R판을 고정하지 않는다. B는503 입구에서1회로 멈춰 수동 URI 복사에 이르지 못했다. 별도 브라우저에서 GitHub source의 해당 URI는 문자이며 실제 outgoing href가 아님을 확인했다. source→Raw로2회를 쓰면 Raw 화면의 활성 링크도0개였고, 후속 URI를 여는 세 번째 열람은 예산을 넘는다.

**추가 링크를 붙일 조건:** `system.file` 동작을 더 읽어야 하는 독자에게만 고정 본문과 도움말 주소를 함께 제공한다. 코드와 출력만 읽으면 본문에서 끝낸다. 코드의 `data.zip`은 웹 링크가 아니라 로컬 package 경로다. 별도로 읽은 [고정 source의 ZIP](https://raw.githubusercontent.com/r-lib/archive/a4c6ec37fc8737a189ca7ec7095ec0161888f9e8/inst/extdata/data.zip)은 실제 존재하지만 첫 참조 system.file의 같은 판 문제를 해결하거나 주 경로 도달을 대신하지 않는다. 근거 ID: `R1-FIXED-HTML`, `R-R1-next-A-2`, `R-R1-next-B-1`, `R1-DATA-ZIP`, `R1-SOURCE-TREE`, `R1-SYSTEMFILE-OFFICIAL`, `UI-R1-RAW`.

## R2 — asciicast 2.3.1

### 목적 가: init_knitr_engine과 Using SVG files 설명 읽기

**독자에게 할 말:** “[현재 asciicast 예제](https://asciicast.r-lib.org/articles/asciicast-demo.html#example)에서 engine 초기화 설명을 읽고 같은 문서의 [Using SVG files 절](https://asciicast.r-lib.org/articles/asciicast-demo.html#using-svg-files)로 이동하세요. 현재 응답은2.3.1이며 선택한 고정 생성 HTML과 전체 바이트가 같습니다. 두 절은 같은 파일 안에 있으므로 설명을 읽는 데 추가 문서가 필요하지 않습니다.”

**실제 열람:** A 현재 예제는1회로 목표판 본문이 읽혔다. B [고정 GitHub HTML](https://github.com/r-lib/asciicast/blob/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html)의 이 body 판독은1회째503이었다. 과거판 내용을 고정해 인용하려면 별도 보조 조회에서 확인한 [고정 HTML 원문](https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html)을 사용할 수 있다. 그 주소는 source 텍스트이며 rendered 예제가 아니다.

**본문에서 끝낼 조건:** 초기화 코드, SVG 설정 방법, 기록된 정적 출력을 읽는 목적일 때. source 재사용은 별도 목적이다. 문서 머리의 [Source HEAD 링크](https://github.com/r-lib/asciicast/blob/HEAD/vignettes/asciicast-demo.Rmd)가 지금 가리키는 Rmd는 원2.3.1 source와 달라졌다. 이때만 [고정2.3.1 Rmd](https://github.com/r-lib/asciicast/blob/f992b26f3cb30c799fbb95f6148852d8ae8a7f18/vignettes/asciicast-demo.Rmd)를 추가할 이유가 있다. 동일 HTML을 받았다는 사실로 Source HEAD의 판까지 고정됐다고 말하지 않는다. 근거 ID: `R2-ENTRY-A`, `R2-FIXED-HTML`, `R-R2-body-B-1`, `R2-RMD-FIXED`, `R2-RMD-HEAD`, `R2-RMD-HEAD-PINNED`, `UI-R2-CURRENT`.

### 목적 나: 해당 예제의 SVG/재생 자원 또는 인라인 데이터 읽기

**독자에게 할 말:** “[Using SVG files](https://asciicast.r-lib.org/articles/asciicast-demo.html#using-svg-files)에서 실제 읽히는 것은 인라인 정적 출력입니다. 그 출력만 읽으려면 같은 문서에서 끝납니다. 이 절의 실제 SVG 파일이나 재생 payload 주소는 찾지 못했으므로 별도 SVG 링크를 제공하거나 재생이 확인됐다고 안내할 수 없습니다.”

**실제 열람:** 이 next 목적의 A/B는 각각1회로 현재 HTML 또는 고정 source 안의 정적 `<pre>` 출력을 읽었다. 추가 자원 열람은0회다. `static_output=confirmed`와 엄격한 SVG/재생 후속축 `no_explicit_path`를 함께 유지한다. 같은 판 확인도 포함 HTML과 정적 출력에 한정한다. B-body가503이었다는 다른 판독의 결과와 B-next가200이었다는 이 판독의 결과를 서로 덮어쓰지 않는다.

**유보 이유와 다음 확인:** 선택 절에 실제 SVG XML, 이미지 src, cast JSON 또는 player payload가 없다. 발행자가 이 예제에 대응하는 실제 SVG/cast 자원을 지정하면 그 URL과 같은 판 지문을 추가로 확인할 수 있다. 뒤의 다른 예제나 footer 로고 SVG를 대체 목표로 선택하지 않는다. [고정 init_knitr_engine reference](https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/reference/init_knitr_engine.html)와 [현재 reference](https://asciicast.r-lib.org/reference/init_knitr_engine.html)는 같았지만, 이는 선택한 SVG 자원이 아니다. 근거 ID: `R2-FIXED-HTML`, `R-R2-next-A-1`, `R-R2-next-B-1`, `R2-REFERENCE-FIXED`, `R2-REFERENCE-CURRENT`, `UI-R2-CURRENT`, [코딩 구분 기록](streams/r/evidence/R-coding-adjustment.json).

## 현재 사용자·과거판 인용자·보존 발행자의 선택

| 프로젝트 | 당장 쓰는 독자 | 과거판 내용을 인용하는 독자 | 생성물을 보존한 발행자에게 필요한 연결 |
|---|---|---|---|
| P3 | 현재 지원판은 [stable enable](https://cibuildwheel.pypa.io/en/stable/options/#enable).3.3.0 설정이 목적이면 [고정 enable](https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable) 한 링크 | 3.3.0 본문과 필요할 때만 [1.x root 표](https://cibuildwheel.pypa.io/en/1.x/#what-does-it-do)를 함께 인용. 두 릴리스의 관계를 명시 | 버전 메뉴가 options 경로를 유지한다는 점을 고려해 지정 root 표의 직접 링크도 보존.1.x는 계열 주소이므로 영구적인 patch/bytes 고정 약속으로 확대하지 않음 |
| P1 | [latest 설정 문서](https://bandersnatch.readthedocs.io/en/latest/mirror_configuration.html#minmal)는8.2.0. 확인한 첫 예제는7.0.1과 같음 | [고정7.0.1 소스](https://github.com/pypa/bandersnatch/blob/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/docs/mirror_configuration.md#minmal). named 서비스404는 별도 기재 | 소스 문서와 실제 `example.conf`를 구별해 연결. upstream PyPI의 현재 홈페이지·서비스 동작·과거 동작을 같은 판 주장으로 합치지 않음 |
| R1 | [현재 archive_read](https://archive.r-lib.org/reference/archive_read.html#ref-examples)의 코드·출력은 읽을 수 있음. 현재판1.1.14를 표시 | [고정1.1.12 HTML 원문](https://raw.githubusercontent.com/r-lib/archive/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html). source 표시와 주 GitHub503을 명시 | 외부 R 도움말의 판 관계와 package ZIP의 고정 source 위치를 별도로 제공해야 동일판 주장 범위를 넓힐 수 있음. 모든 독자에게 ZIP을 추가할 필요는 없음 |
| R2 | [현재2.3.1 예제](https://asciicast.r-lib.org/articles/asciicast-demo.html#using-svg-files) 한 문서로 설명·정적 출력 읽기 | [고정 HTML](https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html); source 재사용이면 [고정 Rmd](https://github.com/r-lib/asciicast/blob/f992b26f3cb30c799fbb95f6148852d8ae8a7f18/vignettes/asciicast-demo.Rmd)도 추가 | 움직이는 Source HEAD를 고정 source와 연결. 실제 SVG/재생을 제공하려면 해당 payload·같은 판 지문을 따로 보존. 현재 정적 출력을 실제 재생 자원으로 표시하지 않음 |

조회 실패의 지속성이나 원인은 이번 카드에서 확정하지 않는다. 후속 작업은 새 UTC의 실제 응답을 별도 원장행으로 추가하고, 이번16판독의 실패·미도달·명시 경로 없음은 원 관측으로 유지해야 한다.
