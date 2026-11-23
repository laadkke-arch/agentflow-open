# Python 두 자리 — 판독과 자원 대조

후보 봉인 `c2a3f387cc962abd1ef383e39f750cc23ee5e51a` 뒤 독립 8판독을 실행했다. 실제 문서 열람은 13회, 응답 entity body 합은 1,206,482 bytes다. HTTP/DOM은 직접 읽었으며 실제 클릭 노출은 주 작성자의 `streams/ui` 브라우저 증거와 연결한다. urllib를 브라우저 JavaScript 실행으로 부르지 않는다.

## 네 대응쌍

| 목적 | A의 실제 경로·관측 | B의 실제 경로·관측 | 판정과 반대 근거 |
|---|---|---|---|
| P3-body | [stable/options](https://cibuildwheel.pypa.io/en/stable/options/#enable) → 동적 버전 메뉴의 [v3.3.0/options](https://cibuildwheel.pypa.io/en/v3.3.0/options/), 2회 | [v3.3.0/options/#enable](https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable), 1회 | 둘 다 최종 3.3.0 본문 확인. A 첫 화면은 목표와 다르지만 두 번째 열람으로 회복한다. 정적 HTML에 메뉴 href가 없다는 사실만으로 이 회복을 불가능하다고 결론 내리면 틀린다. |
| P3-next | stable/options → [1.x/options](https://cibuildwheel.pypa.io/en/1.x/options/), 2회 | v3.3.0/options → 같은 [1.x/options](https://cibuildwheel.pypa.io/en/1.x/options/), 2회 | 정확히 봉인한 [1.x root의 what-does-it-do 표](https://cibuildwheel.pypa.io/en/1.x/#what-does-it-do)는 미도달. 도착한 options에는 **다른** build-identifier 표가 있어 cp27/pp27 정보를 읽는다. 다른 표로 주 성공을 바꾸지 않되 좁은 지원정보의 충분성이라는 반례를 보존한다. |
| P1-body | [latest root](https://bandersnatch.readthedocs.io/en/latest/) → [mirror_configuration#minmal](https://bandersnatch.readthedocs.io/en/latest/mirror_configuration.html#minmal), 2회 | [named 7.0.1 root](https://bandersnatch.readthedocs.io/en/7.0.1/) 404, 1회 | A 최종 title/nav는 8.2.0. 그러나 첫 Minmal 코드 395문자는 고정 7.0.1 소스에서 추출한 예제와 정확히 같다. 예제 같음과 지정판 같음을 분리한다. B의 현재 실패는 과거 미생성이나 모든 소스 손실의 증거가 아니다. |
| P1-next | latest root → mirror_configuration#minmal, 2회에서 종료 | named 7.0.1 root 404, 1회에서 종료 | 고정 첫 예제의 첫 동작 URI는 `master = https://pypi.org`다. HTML에서는 span 문자이며 링크가 아니다. URI를 복사해 열려면 세 번째 문서가 된다. [PyPI](https://pypi.org)는 별도 보조 요청으로 200을 읽었으나 주 경로 성공으로 합치지 않았다. |

네 쌍 모두 실행했고 목표 전체 성공은 P3-body의 A/B 두 판독이다. P3-next의 후속 목적판 `1.x`는 확인했지만 목표 root 표의 읽기 성공은 없다. P3의 `same_version=confirmed`는 지정된 **구계열 목적판 식별**을 뜻하며 1.x와 3.3.0이 동일 릴리스라는 뜻이 아니다. P1-next의 PyPI에는 bandersnatch 7.0.1이라는 자원판이 존재한다고 확인할 수 없다. 이 미확인을 8.2.0과 같은 판 반박으로 단순화하지 않는다.

## Q1·Q2 — 원문 약속과 목적 선정

P3 고정 [README](https://github.com/pypa/cibuildwheel/blob/63fd63b352a9a8bdcc24791c9dbee952ee9a8abc/README.md)의 CPython 3.13 free-threading 주석은 stable/options/#enable을, unsupported Python 독자 문장은 1.x를 지목한다. [고정 options 소스](https://github.com/pypa/cibuildwheel/blob/63fd63b352a9a8bdcc24791c9dbee952ee9a8abc/docs/options.md)에는 3.13의 opt-in과 3.14+의 기본 포함이 구별돼 있다. 같은 본문에 TOML/YAML 예제가 들어 있어 설정 **설명을 읽는 목적**에는 외부 자원을 추가할 필요가 없다. 환경 설치·빌드·실행 성공은 별개다. 근거 PY-P3-README, PY-P3-OPTIONS-SOURCE, PY-P3-START-B.

P1의 [7.0.1 README](https://github.com/pypa/bandersnatch/blob/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/README.md)는 latest 문서로 연결한다. [index.rst](https://github.com/pypa/bandersnatch/blob/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/docs/index.rst)는 CLI synopsis를 생성하고 Mirror Configuration을 목차에 둔다. 첫 설정 예제는 [mirror_configuration.md](https://github.com/pypa/bandersnatch/blob/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/docs/mirror_configuration.md)의 Examples → `Minmal`(발행자 철자), L13–39로 고정했다. 최초 웹 URI는 L23의 upstream `https://pypi.org`다. L20의 `/srv/pypi`는 로컬 출력경로이고, L38의 filtering 문서 링크는 뒤에 나온다. Examples 공통 도입의 L11 링크는 개별 예제 범위 밖이다. 이 경계와 모든 후보는 목적지 열람 전 봉인했다.

초기 논의에서는 후행 filtering 문서를 선택할 가능성을 고려했으나, 첫 동작 URI도 보존하라는 계약을 다시 대조하고 **어떤 목적지도 열기 전** master URI를 선택했다. 이전에 커밋된 다른 target은 없었다. `freeze.json`이 이 사전 논의와 원 후보를 보존한다. 질문 목적 자체는 연구 조건이며, 발행자가 고정판 URL을 영구 보존한다고 약속한 것으로 꾸미지 않는다.

## Q3·Q4 — 첫 화면, 링크, 마지막 화면

P3 stable/options와 고정 v3.3.0/options의 정적 HTML 모두 `1.x` href는 0개이고 `<base>`도 없다. 그러나 실제 브라우저의 ReadTheDocs shadow-DOM 버전 메뉴는 경로를 유지한 `/en/1.x/options/` 링크를 노출한다. 따라서 정적 원문만 검사한 경로 판단은 불충분하다. 반대로 메뉴가 구판으로 갔다는 사실만으로 root의 특정 표에 도달했다고 할 수도 없다. `Home href=".."`를 추가하면 root로 가지만 이미 두 문서를 읽었기 때문에 주 분모에서는 중단했다. 근거 PY-READ-P3-next-A-2/B-2와 `streams/ui/freeze.json`.

P1 latest root에는 `mirror_configuration.html#minmal` 직접 목차 링크가 있다. 상대 URL은 현재 latest 경로를 유지하므로 도착 문서는 8.2.0이다. 두 번째 문서의 first ini block은 `https://pypi.org`를 `<span class="s">`로 표시한다. master URI 자체의 href는 없으며 같은 예제 뒤의 `filtering_configuration.html`은 클릭 가능하다. 뒤의 쉬운 링크를 주 target으로 바꾸지 않았다. 근거 PY-READ-P1-body-A-2, PY-READ-P1-next-A-2.

첫 화면에서 판이 틀리는 것과 예산 안에서 회복되는 것은 다른 관측이다. P3-body A는 전자 반박·후자 확인이다. P1-body A는 최종판까지 목표와 다르지만 예제 내용은 같다. 404는 P1 B 두 판독에만 직접 실패로 남긴다. Python 경로에서는 소스 보기나 Raw 버튼이 주 시작 경로에 없으며, 고정 GitHub/Raw 원본 비교는 모두 보조 예산이다.

## Q5 — 파일·내용·판의 증거 강도

태그 원문을 이번에 다시 읽었다. [bandersnatch tag 7.0.1](https://api.github.com/repos/pypa/bandersnatch/git/ref/tags/7.0.1)은 `7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74`를 직접 지목한다. [cibuildwheel v3.3.0 ref](https://api.github.com/repos/pypa/cibuildwheel/git/ref/tags/v3.3.0)는 annotated tag 객체를 지목하며, 그 [tag 객체](https://api.github.com/repos/pypa/cibuildwheel/git/tags/45616d2b12f67573cd48b844c047f8cda2809f43)를 별도로 열어 `63fd63b352a9a8bdcc24791c9dbee952ee9a8abc`와 연결했다. ref의 tag 객체 SHA를 source commit으로 잘못 대체하지 않았다.

`evidence/comparison.json`에는 두 핵심 대조가 있다. P1의 7.0.1 source ini fence와 8.2.0 HTML pre에서 tag 제거·HTML entity 해제만 한 텍스트는 공백 정규화 없이 395문자 전부 같고, SHA256은 `6850998fbae53e09075799d6576191d7a66be2d9083ca9baf5ef285c81562c6c`다. 이것은 코드 예제의 동일성이며 문서 파일 전체의 동일성이 아니다. P3의 root 지원 matrix는 OS 열9개, options의 build-identifier 표는 묶음 열4개이고 두 HTML table 지문도 다르다. Python2 지원정보의 교집합이 있어도 같은 표로 채점하지 않는다.

보조로 실제 다른 파일도 읽었다. 고정 [filtering_configuration.md](https://github.com/pypa/bandersnatch/blob/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/docs/filtering_configuration.md)는 플러그인 활성화·allowlist/blocklist 안내를 보존한다. 고정 [example.conf](https://github.com/pypa/bandersnatch/blob/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/src/bandersnatch/example.conf)는 문서 끝의 literalinclude가 지목하는 파일이다. 실제 Git blob 해시는 발행자 고정 tree의 값과 일치한다. 이 파일은 timeout10/global-timeout1800이고 첫 Minmal 예제는15/18000이므로, 둘을 같은 예제라고 바꾸면 안 된다. 파일 존재·원문 확인은 주 경로 도달과 분리돼 `assets.jsonl`에 기록된다.

## Q6 — 실제 반환 카드 제안

- **P3의 3.3.0 설정 문장 인용:** [v3.3.0/options/#enable](https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable) 한 링크. 3.13 opt-in과3.14+ 기본 포함을 볼 절로 명시한다. stable도 메뉴로2회 안에 회복할 수 있지만 고정 링크는 처음부터 지정 본문에 도착한다.
- **P3의 구계열 root 지원표 인용:** [1.x/#what-does-it-do](https://cibuildwheel.pypa.io/en/1.x/#what-does-it-do)를 추가한다. 3.3.0과 같은 릴리스라 부르지 않는다. 단순 cp27/pp27 identifier 확인이라면 두 번째 options 표로 충분한 다른 목적이 존재하지만 이번 봉인 목표를 대체하지 않는다.
- **P1의 7.0.1 첫 설정 예제 인용:** [고정 source의 Minmal](https://github.com/pypa/bandersnatch/blob/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/docs/mirror_configuration.md#minmal)을 source 문서라고 안내한다. 지정된 named 서비스 입구는404이고 latest는8.2.0이다. 고정 source의 링크 반환은 보조 대조에서 얻은 권고이며 원 A/B 경로의 성공으로 소급하지 않는다.
- **P1의 예제가 가리킨 upstream 확인:** [PyPI](https://pypi.org) 링크를 추가할 수 있지만 현재 비판정 URI의 홈페이지 확인 범위만 말한다. 7.0.1의 동일판 외부 자원이나 mirror/API 실행 성공이라는 주장은 유보한다. 후행 filtering source 링크는 사용자가 필터 설정을 별도로 요구할 때만 안내한다.

## 원자료·비용·남은 빈칸

원장30행 중 중복/실패/보조 태그·목록 제외 적격13자료, 계보3개다. guidance8·실제 다른 문서/자원5로 분류된다. 같은 바이트의 재요청은 한 번만 세고, P3 options 소스는 대응 생성 HTML과 보수적으로 중복 제외했다. 총 계측30 GET·1,812,725 응답본문 bytes에는 초기 후보 조사·주 판독·보조 대조가 함께 들어 있다. 그중 주 판독13 GET·1,206,482 bytes만을 독자 비용으로 쓴다. 브라우저 자동 하위요청·TLS·헤더·사람 소요 시간·금전은 합하지 않았다.

미확인 사항은 HTML/정적 자원 이후 JS/R/Python 실행, PyPI의 모든 API 동작, 고정 URL의 미래 불변성이다. 역사 제공·장애 회복·이전 빌드 로그는 재조회하지 않았다. 다른 분야 Q7은 이 stream 범위가 아니며 주 작성자의 별도 연구와 연결한다. 주 결론을 바꿀 최소 관측은 정해진 options 입구에서 root 표로 직접 연결되는 현재 UI 링크, 또는 named7.0.1에서 목표판 본문을 제공하는 새 응답이다. 새로운 관측은 이번16행에 덮어쓰지 않고 별도 회차로 남겨야 한다.
