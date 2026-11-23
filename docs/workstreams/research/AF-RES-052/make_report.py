"""Render the report and acceptance ledger from frozen and observed records."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
INDEX=json.loads((ROOT/'evidence/ledger-index.json').read_text())
COUNTS=json.loads((ROOT/'evidence/source-counts.json').read_text())

WEAKNESSES=r'''| 불일치 또는 약점 | 영향받는 결론 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀌는 조건 |
| --- | --- | --- | --- | --- |
| 1. 기능 절 정의를 목록 노출 뒤 정정했고, 자연4풀은 빈 매치·보강3자리는 미충원·P-S1은 목적 미연결이다. | 주표본에서 독립 구현의 요구별 승격·손실을 추정하거나 B를 기본 형식으로 채택할 수 없다. | [PY 목록 L18–35](https://github.com/pypa/packaging.python.org/blob/5ecbc0db967843e64d55da165b72e773888860c5/source/key_projects.rst#L18-L35), [Markdown 범주 L34–98](https://github.com/remarkjs/awesome-remark/blob/82427708991528ad21475151aea2311f2699d549/readme.md#L34-L98); CORRECTIONS C01, slots.csv2–9, groups.csv2–25 | 새 차수에서 발행자가 기능별로 구성한 공식 목록과 독립 사용자 목적을 먼저 고정하고 같은 정원·순서 규칙으로 다시 모집한다. 현재 빈 자리는 유지한다. | 같은 사전 규칙으로 매치된 요구·목록 절에 실제4–6위의 별개 구현이 있고 두 필수조건의 동일판 근거가 확보될 때. |
| 2. 제품판·문서 역할 등의 표시 결측으로 엄격 C의 실제 충돌을 확보하지 못했다. | C=A는 C의 유효성·안전성 검증이 아니다. 판 미상만 완화해도 다른 결측·부품 차이가 남는다. | [PY 목록 L21–24](https://github.com/pypa/packaging.python.org/blob/5ecbc0db967843e64d55da165b72e773888860c5/source/key_projects.rst#L21-L24), [Official L36–41](https://github.com/remarkjs/awesome-remark/blob/82427708991528ad21475151aea2311f2699d549/readme.md#L36-L41); pools.csv2–6, sensitivity.csv30–41 | 목적지를 보기 전에 다섯 필드가 모두 명시된 충돌 쌍과 뒤의 별개 URL을 확보한다. 모르는 역할을 목적지 내용으로 채우지 않는다. | 알려진5필드 충돌로 앞3 대표가 달라지고 같은 목적의 독립 완결 ID 또는 필요한 보완 절의 접근성이 변할 때. |
| 3. 생성 당시 이슈·첨부, 일부 정확 도착과 같은 snapshot, 실제 설치·화면 시행이 미확인이다. 라우팅 README는 먼저 노출됐다. | 역사판 완결, 모든 목적지의 비노출, 실제 UI 두 동작 효과를 주장할 수 없다. D-M1은 현재 소스 창의 C1만 양성이다. | [#941 본문8–10·첨부](https://github.com/remarkjs/remark/issues/941), [옵션 L160–167](https://github.com/remarkjs/remark/blob/1146b3a274fc1f4607111e5d6607a3a769a0e89a/packages/remark-stringify/readme.md#L160-L167), [PyPI 초기 주소](https://pypi.org/project/bandersnatch); PY-A04/07/10/17, ME-HISTORY, sources.jsonl111–112·151 | 원 package.json/lockfile와 첨부를 확보하고, 정확 URL·fragment의 고정 응답을 보존한 새 시행에서 같은 입력을 실행한다. REPRODUCE.md와 Markdown REPLAY_PLAN.md의 입력·명령을 사용한다. | 역사 패키지 식별과 판이 확정되고, 한 시행의 실제 도착 창 또는 실행에서 C1/C2가 함께 확인되거나 현재의 부분 양성이 반증될 때. |
'''

BODY=r'''
# AF-RES-052 · 부분 인계

**주표본에서는 B 또는 C가 요구를 완결하는 독립 구현을 늘리거나 잃게 했다고 판정할 수 없다.** 자연4자리는 사전 기능명사와 공식 목록 제목/별칭이 맞지 않아 반환 후보가 없었다. 보강4자리 중 한 메타데이터 풀만 확보했으며 그 풀에도 사전 사용자 목적을 연결하지 못했다. 이는 생태계에 해결책이 없다는 결론이나 성공률0%가 아니다. 정의된 모집·매칭과 요구 연결에서의 결과다. [원장: slots.csv2–9, groups.csv2–25, evidence.csv2–23]

별도로 보존한 **D-M1 진단**에서는 B가 원6번 명세 URL을 올렸고, 그룹→원4번의2동작 경로에서 필수조건 C1이 새로 보였다. 그러나 그 명세는 실행 구현이 아니며, 어느 방식에서도 두 조건을 함께 확인하는 완결 ID는 관측0이었다. 부분 증거의 증가와 완결 구현의 증가는 다른 결과다. [원장: changes.csv26–28, paths.csv148, evidence.csv30–38]

위 첫 표는 본표8자리, 둘째 표는 같은 자리×A/B/C의24행이다. `P-*`는 Python, `M-*`는 Markdown, `N`은 자연, `S`는 보강이다. 모든 목록판은 해당2022년 요구보다 뒤여서 **현재 재탐색**이다. `관측 0`은 정해진 반환/창에서 얻은 빈 집합, `미확인`은 부족한 자료 때문에 판정할 수 없음, `해당 없음`은 조건부 분모나 시행이 없음이다. 원문·입력·경로의 ID→행 번호는 [ledger-index.json](evidence/ledger-index.json)에 있다.

## 진단 표 — 본표의 빈 자리를 대체하지 않음

| 원장·목적 | 대표 원순번·숨은 형제 | 원풀 공급자의 정답 | 직접 완결 ID | ≤2동작 완결 합집합 | 한 시행 최대·경로 | 요구 원자의 증감 | 원풀 밖 도착 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D-M1-A / M-N1 |1,2,3; 형제 없음;4,5,6 잘림 | 조건부 현재 D2 `IM-M1-current-configured` 1계보; 역사판 미확인 | 관측0 | 관측0 |0 /18경로 | 확인된 C1/C2 원자 없음 | CommonMark·unified; 완결 관측0 |
| D-M1-B / M-N1 |1,6;1의 형제2,3,4,5 | 같은 원풀·같은 조건부 정답 | 관측0 | 관측0 |0 /14경로; B-P08은 C1만 | A 대비 C1 +1; 완결 ID +0/−0 | unist; 완결 관측0 |
| D-M1-C / M-N1 |1,2,3; 형제 없음;4,5,6 잘림 | 같은 원풀·같은 조건부 정답 | 관측0 | 관측0 |0 /18경로 | A와 같음 | CommonMark·unified; 완결 관측0 |

조건부 현재 D2 정답은 remark-stringify11.0.0의 [manifest](https://github.com/remarkjs/remark/blob/1146b3a274fc1f4607111e5d6607a3a769a0e89a/packages/remark-stringify/package.json#L8-L12)·[wrapper](https://github.com/remarkjs/remark/blob/1146b3a274fc1f4607111e5d6607a3a769a0e89a/packages/remark-stringify/lib/index.js#L23-L38), mdast-util-to-markdown2.0.0의 [handler](https://github.com/syntax-tree/mdast-util-to-markdown/blob/655f117443d99a08cb839765ff7489aa759f72d0/lib/handle/code.js#L20-L72)·[시험](https://github.com/syntax-tree/mdast-util-to-markdown/blob/655f117443d99a08cb839765ff7489aa759f72d0/test/index.js#L794-L979)을 연결한 것이다. `fences=true`, backtick marker, 사용자 덮어쓰기 없음으로 한정한다. `^2.0.0`은 허용 범위이며 실제 설치가2.0.0이었다는 관측이 아니다. utility는 원4번 구현의 계보이므로 독립 대안을 하나 더 만들지 않는다. 설치·시험 실행은 하지 않았다. [ME-GOLD-C1/C2; M-CODE-*; M-TEST-UTILITY]

D-P1은 정정 전 Python 소속 부모의6개 링크를 보존한 별도 진단이다.5개 URL과 build:index 미해결1개이며57경로 행 중49행은 시작 URL이 알려진 경로다. 그 안에도 정확fragment·접근 실패·부분 창 결측이 남는다. 목적이 없어 완결 증감은 미확인이다. 이 진단이나 D-M1을 보강 정원에 넣지 않는다. [evidence/python/observation-summary.json; evidence/diagnostic-pools.csv]

## Q1 · “쓸 수 있는 부품”의 조건을 먼저 정했는가

Python의230개 기간 내 issue 중 생성 UTC/번호 순서 첫40개, remark의 해당 기간40개를 직접 읽었다. PR은 제외했다. Python에서 이관된 #1020은 공개 생성 시각 기준28위를 유지했다. 선정은 Python2위 #564·6위 #574, Markdown1위 #941·2위 #955다. 기존 구성/버그 질문도 설정 선택이 필요한 경우 포함하는 규칙을 먼저 고정했다. #563의 라이선스 값 문의는 두 독립 기능조건·부품 선택이 부족해 탈락했다. 이 경계는 첫 자연 요구를 바꿀 수 있는 판독 가정이다. [frame.csv의 issue_screen80행; evidence/python/requirements.md; evidence/markdown/requirements.json]

| 요구 | 명시 입력·방향·필수조건 | 환경 및 부정 조건의 판독 | 사전 근접 오답·허용 조합 |
| --- | --- | --- | --- |
| P-N1 | pyproject.toml/setup.cfg/setup.py·src 데이터→editable 설치(R1)와 텍스트/문서 파일 가용성(R2) | Debian11, Python3.9.2, pip21.3.1, setuptools>=42. console_scripts·파일 버전 값은 추가 필수조건으로 세지 않았다. 권한 오류는 보고된 실패이며 관리자 권한 금지를 발명하지 않았다. | wheel만 생성 또는 editable만 설명하면 부족. frontend/backend와 데이터 설정의 같은 호환 체인은 허용. [#564 body61–72](https://github.com/pypa/packaging-problems/issues/564) |
| P-N2 | readme.md 내용→long_description(R1), Markdown content type·PyPI 설명(R2) | Windows10, Python3.9.7, pip22.0.3. setup.py 부재는 입력 상태와 질문자의 가설이며 추가 금지가 아니다. | HTML 변환기·short description·파일명 문자열만 넣기는 근접 오답. 같은 배포물의 backend/config+배포 문서 조합 허용. [#574 body19–43](https://github.com/pypa/packaging-problems/issues/574) |
| M-N1 | code AST→Markdown: lang 없는 노드에도 backtick(C1), javascript 언어·내용 유지(C2) | 원문 literal react-stringify10.0.2·unified10.1.1. 패키지 이름을 고치지 않았고 기대 문자열의 fence 줄바꿈 모호성은 미확인으로 뒀다. | HTML code 렌더러·구문강조만으로 부족. AST 처리기와 serializer의 같은 판 조합 허용. [#941 body22–64](https://github.com/remarkjs/remark/issues/941) |
| M-N2 | Markdown→raw HTML: inline span의 <와 > entity(C1), pre/code도 entity와 language-html(C2) | unified10.1.1·rehype-stringify9.0.3·remark-parse10.0.1·remark-rehype10.1.0. named/numeric entity는 원문의 대안. | 렌더링만 같거나 >가 literal로 남는 것은 실패 조건. parser→bridge→serializer의 호환 체인 허용. [#955 body22–35](https://github.com/remarkjs/remark/issues/955) |

두 조건은 질문 본문·코드/설정에서 읽었으며 “같은 구현·판의 한 체인”이라는 결합 규칙은 판독자가 더한 조건으로 분리했다. 네 본문 모두 최초 가용 현재 REST 본문이며 생성 당시 판은 복원하지 못했다. updated_at을 본문 수정 증거로 쓰지 않았다. 선정에 후속 댓글을 쓰지 않았고 Markdown 두 첨부는 접근 실패다. 뒤에 읽은 bandersnatch 이슈 댓글은 후보 경로 관측으로만 남겼다. [sources.jsonl2·6·71–72·111–112]

## Q2 · 발행 목록의 순서와 후순위 후보

| 발행 저작·판 | 적용 범위·순서 | 조사 범위·실제 후보 |
| --- | --- | --- |
| PY-LIST · PyPA key_projects.rst · commit5ecbc0d, blobf6e282f | 공식 안내서 index의 첫 명시 프로젝트 목록. 원본 reST 편집 순서를 사용; 검색 순위 아님. | 원heading23개 중 소속 부모2·자기 안내서1을 제외한 첫20 기능 절. bandersnatch 절5개: Docs, Issues, GitHub, PyPI, AWS S3. |
| M-LIST-PRIMARY · awesome-remark readme.md · commit8242770, blobea5a8dd | remark README가 첫 번째로 안내한 플러그인 목록. 편집 범주 Official/Plugins/Built on/Built with/Related lists. | 범주5개는 단일 처리 목적의 기능 절이 아님. Official의8링크 중 첫6은 D-M1으로만 보존. |
| PY-RULE / M-LIST-RULES | [PyPA 기여 규칙](https://github.com/pypa/packaging.python.org/blob/5ecbc0db967843e64d55da165b72e773888860c5/source/contribute.rst), [remark 플러그인 안내](https://github.com/remarkjs/remark/blob/1146b3a274fc1f4607111e5d6607a3a769a0e89a/doc/plugins.md) | 독립 저작의 목록 범위·기여 안내 배당. 후보 수가 많다는 이유로 이쪽으로 주목록을 바꾸지 않았다. |

P-S1 원1–5는 [원문 L21–31](https://github.com/pypa/packaging.python.org/blob/5ecbc0db967843e64d55da165b72e773888860c5/source/key_projects.rst#L21-L31)의 편집 순서다. `:pypi:` 선언의 정확 URL은 해당 생성 규칙으로 확인했다. 원4번은 bandersnatch의 등록 레코드이고 원5번이 AWS다. 정확 URL5개·상류 프로젝트2개·독립 완결 구현 수·실제 채택 수를 구별한다. 이름이 다른 공급자가 있다는 사실만으로 같은 요구의 대안이 되는 것은 아니다. [pools.csv2–6; PY-PYPI-ROLE; PY-E05/06]

목록 노출 뒤 기능 절/소속 범주 혼동을 발견해 v2로 정정했다. 정정 전 원격cd940aa와 정정 후ea4fa69를 모두 보존했고, 새로운 목적지 관측은 후자 뒤에 시작했다. 단 remark 라우팅 README는 D-M1 원1과 같은 저작이라 먼저 노출됐음을 공개했다. 자연 요구·명사·예산·최대3대표는 바꾸지 않았다. [CORRECTIONS.md C01–C04; evidence/crossfield/critique.md]

읽지 못한 build:index를 추정 index.html로 채우지 않았다. 공식 intersphinx inventory4건은403으로 실패했고, 다른 주소의 build base 매뉴얼을 읽은 것은 별도 맥락 자료다. 목록 소진과 접근 실패를 섞지 않았다. [PY-INV-*; PY-O14; D-P1-R6]

## Q3 · 같은 후보에서 표시만 바꾸기

A는 query/fragment까지 포함한 정확 URL, B는 발행자가 귀속한 상류 프로젝트, C는 상류·부품·공개 용도·제품판·문서 역할이 전부 알려져 같은 경우만 합친다. 조직 이름만 같다고 다른 프로젝트를 합치지 않았다. 목록 SHA나 latest/stable을 제품판으로 바꾸지 않았다. 각 그룹 첫 멤버가 대표이며 명칭·설명 길이·원순서·목적지를 고정했다. [SCOPE.md; pools.csv; groups.csv]

P-S1의 A/C는1,2,3이고 B는1,5다. B에 세 번째 그룹이 없어 슬롯이 비어 있는 것이 정상이다. C는 상류·부품·용도가 모두 미상인 게 아니다. 이들은 알려져 있지만 제품판·문서 역할이 결측이어서 단독이다. D-M1의 C도 제품판 결측과 역할 결측 또는 부품 차이 때문에 합치지 않았다. 나중에 읽은 제품판·옵션으로 사전 키를 보충하지 않았다. [groups.csv14–16; evidence/diagnostic-groups.csv; CE05]

## Q4 · 두 동작에서 무엇을 함께 읽었는가

출발 목록은 이미 보인다. 대표 열기1회, 보이는 두 대표 각각 열기2회, 그룹 목록→멤버2회, 대표→그 창의 첫 두 정보 href 중 하나2회다. 대표를 연 뒤 그룹을 열고 멤버까지 읽으면3회라서 제외한다. 원문 fragment 절 또는 첫 제목 뒤 최대800 whitespace 단어라는 같은 판독 범위를 적용했다. 도착의 로컬 Contents 링크는 실제 정보 절로 인정하며 더 유용한 셋째 링크로 바꾸지 않았다. [SCOPE.md; evidence/path-plan.json]

P-S1은49경로(A18/B13/C18), D-M1은50경로(A18/B14/C18)를 재구성했다. D-P1의57행 중8행은 미구체화 자리다. root paths.csv177행에는 이156경로 행 외에 빈 상태21행이 들어 있으므로177회 사용자 시험이 아니다. 같은 도착 관측을 방식별로 재사용했으며 서로 다른 시행의 조건을 합치지 않았다. [evidence/NORMALIZATION.md; paths.csv]

| 정확 도착의 경계 | 확인 | 주장하지 않은 것 |
| --- | --- | --- |
| P-S1 원5주소 | 모두 직접 텍스트 반환을 읽음. 온전한 동일 snapshot 창4개, 초기 PyPI7.0.0은347단어 부분 창1개. | 웹 읽기 도구가 주지 않은 HTTP200·redirect chain을 추정하지 않음. 뒤의8.2.0 응답을 이어 붙이지 않음. |
| P-S1 후속 링크 | PEP381, 이슈2개, PyPI통계, AWS기능2개를 읽음. -h 정확fragment는 미확인, Compose tree는 실패. | pinned Compose 소스를 원 tree 도착 성공으로 세지 않음. withdrawn PEP를 현재 구현 시험으로 세지 않음. |
| D-M1 원6주소 | 실제 HTTP200, 같은 최종URL·HTML SHA·source currentOid 확보. |800단어 소스 투영을 viewport·스크롤·독자 이해로 부르지 않음. 라우팅 README 비노출을 주장하지 않음. |
| D-M1 양성 C1 | 원4 옵션 L160–167이 정확HTML에서 접힌 details 밖임을 확인. | 같은 창의 일반 설명으로 C2 언어·내용 보존까지 추정하지 않음. 코드/시험 D2를 사용자 두 동작에 더하지 않음. |

## Q5 · 대안 상승·보완 손실을 반대로 시험한 결과

처음의 기대였던 “같은 상류를 합치면 네 번째 이후의 독립 대안이 올라온다”는 이 자료에서 요구별 완결 양성으로 확인되지 않았다. 실제로 올라온 S3는 보완 저장 서비스, mdast는 명세였다. 그와 반대로 “완결 ID 차이가0이면 유용한 증거 차이도 없다”는 결론은 D-M1-B-P08의 C1 노출 때문에 성립하지 않는다. [CE01–03; PY-E06; ME-R4-C1; ME-R6-C1/C2]

| 반례·원장 | 관측 | 유지해야 할 한계 |
| --- | --- | --- |
| CE04 보완 절 접근 손실 | A/C는 Issues→#2059를2동작에 읽고 B는 그룹→Issues까지만2동작이라 본문에는3동작 필요. | 사전 목적이 없어서 필요한 필수 절의 손실 양성으로 세지 않는다. Compose 예제도 길이는 달라지나 실제 원도착 실패다. |
| CE06 뒤쪽 병합 | trove-classifiers의 원4·6은 같은 classifiers URL. A가 뒤에서 병합해도 앞3은 C와 동일. | 이 맥락 절을 새 보강 양성으로 추가하지 않는다. [목록 L284–294](https://github.com/pypa/packaging.python.org/blob/5ecbc0db967843e64d55da165b72e773888860c5/source/key_projects.rst#L284-L294) |
| CE07 대표 한 개에 여러 이름 | remark root는4패키지, build 매뉴얼 비교 절은 여러 도구 역할을 설명한다. | 각 독립 구현의 모든 조건·판을 입증하지 않는 이름 수는 완결 수가 아니다. |
| CE08 유효한 출력과 요청된 출력 | CommonMark는 indent code도 허용하지만 사용자는 backtick을 요구한다. utility의 fences=false·tilde 설정은 구체 근접 오답이다. | 요구자 제약을 의미 동등성으로 임의 완화하지 않는다. |
| CE09 릴리스와 코드의 충돌 | [remark15 릴리스](https://github.com/remarkjs/remark/releases/tag/15.0.0)는 기본 fences 변경을 기록하며 false 설명 일부는 현재 옵션·코드·시험과 반대다. | 기본 변경과 잘못될 수 있는 마이그레이션 설명을 구별; 해당 문장을 역사판 성공 증거로 쓰지 않는다. |
| CE10 같은 주소의 다른 응답 | 초기 PyPI7.0.0과 후속8.2.0 창이 달랐다. | 조사 중 실제 제품이 바뀌었다고 단정하지 않고 캐시/응답 차이로 남긴다. |

전체12건과 각각 결론을 뒤집을 최소 조건은 [counterexamples.csv](counterexamples.csv)에 있다. 목표 양성의 존재 자체는 종료 조건으로 두지 않았지만, 목적 연결·표본 충원·원판/도착 결손 때문에 이번 인계는 부분 상태다.

## 대표 카드와 Q7 · 채택할 형식, 보류할 주장

| 형태·카드 | 주소·용도·깨지는 조건을 포함한 한 줄 |
| --- | --- |
| 원문1개 · K-M1-1 | [stringify 옵션 L160–167](https://github.com/remarkjs/remark/blob/1146b3a274fc1f4607111e5d6607a3a769a0e89a/packages/remark-stringify/readme.md#L160-L167): 현재 C1 확인·C2 미확인; B 형제 경로2동작, 역사 패키지에는 소급 불가. |
| 보완 절 · K-M1-2 | [옵션](https://github.com/remarkjs/remark/blob/1146b3a274fc1f4607111e5d6607a3a769a0e89a/packages/remark-stringify/readme.md#L160-L167)+[handler](https://github.com/syntax-tree/mdast-util-to-markdown/blob/655f117443d99a08cb839765ff7489aa759f72d0/lib/handle/code.js#L20-L72)+[시험](https://github.com/syntax-tree/mdast-util-to-markdown/blob/655f117443d99a08cb839765ff7489aa759f72d0/test/index.js#L794-L979):11.0.0/2.0.0의 조건부 D2 조합; 현재2동작 밖이며 실행 미확인. |
| 구현2개 · K-M1-3 | [serializer](https://github.com/remarkjs/remark/tree/main/packages/remark-stringify)+[mdast 명세](https://github.com/syntax-tree/mdast): 독립 완결 구현 둘로 반환 **보류**, 입력/출력·문서 역할이 다름. |
| 원문1개 · K-P1-1 | [bandersnatch 매뉴얼](https://bandersnatch.readthedocs.io/en/latest/): 미러 명령 개요; 사전 목적 미연결·과거 환경/필터 조합 미확인. |
| 보완 절 · K-P1-2 | [저장 장](https://bandersnatch.readthedocs.io/en/latest/storage_options.html)+[Compose 소스](https://github.com/pypa/bandersnatch/blob/81a81eb894fa5a014298c04be2c956f620864648/src/bandersnatch_docker_compose/README.md): 저장/서빙 검토 자료; 원 tree 실패를 복구한 두 동작 성공으로 표시하면 깨짐. |
| 구현2개 · K-P1-3 | [bandersnatch](https://github.com/pypa/bandersnatch)+[S3](https://aws.amazon.com/s3/): 두 독립 대안으로 반환 **보류**, 미러와 보완 저장 서비스이고 목적 미연결. |

자연4자리와 미충원3자리의 빈 카드도 [cards.md](cards.md)에 있다. **조건부로 제안할 수 있는 형식은 주소·역할·판·확인된 필수조건·남은 조건을 함께 표시하는 카드**다. 실제 사용성은 검증하지 않았다. B를 모든 요구에 기본 적용하기, C를 검증된 안전 병합으로 부르기, 세 자리가 충분하다고 일반화하기는 보류한다.

## 추가 슬롯·판 결측 감도

| 감도 ID·대상 |3자리→4자리 또는 판만 완화 | 정확히 바뀌는 rank·조건 | 완결 증감 |
| --- | --- | --- | --- |
| P-S1-A/C-SLOTS |1,2,3→1,2,3,4 | 원4 PyPI만 직접 추가. AWS 원5가 A/C에도 보이려면5슬롯 필요. | 목적 미연결로 미확인 |
| P-S1-B-SLOTS |1,5→1,5 | 두 그룹에서 소진 | 미확인 |
| MS-SLOT4-A/C |1,2,3→1,2,3,4 | 원4의 C1을 직접1동작에 읽음; B의2동작 원자 우세는 사라짐 | 현재 완결 +0/−0; C2 없음 |
| MS-SLOT4-B |1,6→1,6 | 두 그룹 소진 | 현재 완결 +0/−0 |
| P-S1-C-VERSION-ONLY / MS-C-VERSION-SENTINEL | 제품판 미상만 동일값으로 취급 | 문서 역할 결측 또는 다른 부품/용도 때문에 병합 없음 | P-S1 미확인; D-M1 현재 +0/−0 |
| 자연4 및 미충원3 | 빈 배열 유지 | 슬롯 증가는 무매치나 적격 기능 절 부재를 해결하지 않음 | 빈 반환0 / 미충원 미확인을 구별 |

감도40행은 [sensitivity.csv](sensitivity.csv)다. 목적지에서 얻은 제품판으로 C를 채우는 감도는 하지 않았다. 결과 방향이 바뀌는 관측 조건은 D-M1의 **원4번이4번째 직접 슬롯에 들어오는 것**이다. 이때 변화하는 것은 C1의 접근 경로이며 전체 완결 결론은 그대로다.

## Q6 · 다른 독자·다른 분야의 특정성

설계자의 “어떤 도구라도”에는 입력/출력과 독립 대안의 역할이 중요하고, 사용자 문서 작성자의 “이 버전의 이 방향”에는 제품판·기본값이 중요하다. 유지보수자의 “두 부품을 함께 쓰는 법”에는 호환 체인과 보완 설치·설정 절이 필요하다. 같은 상류 이름은 세 목적을 대신하지 않는다. 아래 대조는 소프트웨어 적중에 합산하지 않는다. [cards.md; evidence/crossfield/findings.md]

| 사례·원장 | 개별 발행 기록에서 확인 | 이름 찾기와 특정 실현 찾기의 차이 | 반대 증거·한계 |
| --- | --- | --- | --- |
| 녹음 X01/X02 | [UNT1999 여성 합창](https://digital.library.unt.edu/ark:/67531/metadc84597/)의 Foster Beautiful Dreamer track14·2:56과 [UNT2010 Rinaldi](https://digital.library.unt.edu/ark:/67531/metadc89020/) track1·2:41은 연주자·날짜·ARK가 다르다. | 작품명 검색은 같은 곡 아래 둘 수 있으나 특정 연주를 찾으면 각각의 레코드가 대표여야 한다. | 녹음 미청취·편곡 동일성 미확인. XML 접근 표시는 각각 unt/public이므로 둘 다 재생 차단됐다고 쓰지 않음. |
| 서체 X03/X04 | [Inter v3.19 설명](https://github.com/rsms/inter/blob/5fa70f6e8c0ecad97544e19aba2d5062aa8c3e7a/misc/dist/variable.txt#L2-L16)은 다축/weight-only와 이름만 다른 Inter V를 구별; [v4.0 설명](https://github.com/rsms/inter/blob/2ce9119398be143fa289c3e180824db1b7ed803e/misc/dist/help.txt#L13-L44)은 weight/optical size·upright/italic 파일을 안내한다. | 공개 family Inter는 같아도 slant/optical size 목적에는 판·flavor에 맞는 개별 문서가 필요하다. | 내부 설치 이름은 다를 수 있다. fvar·브라우저는 미검사. 반대로 Inter와 Inter V의 이름 차이만으로 독립 구현2라고 세면 틀림. |

한 원문이 여러 flavor를 이미 설명한다는 서체 반례는 “항상 한 이름당 한 문서만”도 “항상 이름마다 독립 구현”도 적절하지 않음을 보인다. 엄격 C는 알려진 제품판이 다르면 나눠야 하므로 이 사례를 C의 실측 실패로 세지 않았다.

## 자료 수·실행·재현 상태

| 단위 | 확인값 | 해석 |
| --- | --- | --- |
| 필수 배당 저작 |24: 요구4·공식목록/규칙4·공급자8·릴리스/시험4·다른분야4 | 중복 저작·실패 제외. 추가 문서는 배경으로 남김. |
| 전체 출처 원장 |151행; 직접 확인한 고유 work_id132; 실패/정확fragment 미확인13행 |80개 모집 issue와 맥락 자료를 포함하는 넓은 단위.132개 후보나 구현이라는 뜻이 아님. |
| 자연층 | 요구4/4, 비어 있지 않은 풀0/4, 메타데이터 기회0/4 | 원문 누락 때문에 빈 목록이라고 한 것이 아니라 고정 제목 매칭 결과임. |
| 보강층 | 메타데이터 풀1/예정4, 미충원3, 목적 연결0/확보1 | 목적 연결된 완결 양성 비율의 분모0 → 해당 없음. |
| 본표 URL·상류 | URL5, 발행자 귀속 상류2, 완결 구현 수 미확인 | 원4는 기존 프로젝트 레코드, 원5는 보완 서비스. |
| 진단 D-M1 | URL6, 조건부 D2 계보1, 창 완결0, B만 C1 원자1 | 독립 runtime 승격 관측0; 역사판 미확인. |
| 실행 | 자료 직접 열람·목록/배열·경로 계산·원장 검사 수행 | 공급자 행동시험 D3·패키지 설치·실제 브라우저/사용자 시행·녹음 재생·폰트 fvar는 미실행. |
| 사람의 실제 채택 | 미측정 | URL 수·문서 확인 수·도입 수를 바꾸어 쓰지 않음. |

필수24 source ID와 배당은 [source-counts.json](evidence/source-counts.json), 실패 주소·시도·오류·최소 복구 자료는 [sources.jsonl](sources.jsonl)에 있다. 공급자8은 bandersnatch 매뉴얼/README, AWS S3 문서군, build 매뉴얼, remark-parse/stringify/cli 문서, mdast 명세다. 릴리스/시험4는 bandersnatch CHANGES·S3시험, remark15 릴리스·utility시험이다. 시험 원문을 읽은 것이 실행을 뜻하지 않는다.

검증 명령·미실행 재현 입력은 [REPRODUCE.md](REPRODUCE.md), Q별 답·반대 증거는 [SELF_CHECK.md](SELF_CHECK.md), 상태·분자·분모·행은 [acceptance-evidence.json](evidence/acceptance-evidence.json)에 있다. 고정 결과 커밋의 원격 재열람과 실제 session check 출력/종료 코드는 결과 동결 뒤의 검증 영수증에 기록하며, 그 확인 후에만 HANDOFF를 마지막 단독 커밋으로 작성한다.

## 실제 보존한 순서

| 단계 | 원격 커밋 | 보존한 내용 |
| --- | --- | --- |
|① 사전 규칙·요구 |842b7099bba6869000abad23f0316d34556bd080;817ebda103ee5926c308ad563a5879c2cf66fc32 | 시작 manifest·범위·80개 모집·조건·명사·목적 후보 |
|② 목록·정정 |cd940aa340a5396611d028002ffc7150981f853a;ea4fa69f841dca2c470b62c3fdf1ee4d9029712e | 잠정 배열, 기능 절 정정, 본표/진단 분리, 목적지 전 배열/경로 규칙 |
|③ 관측·짝 비교·반례 |37a82ee278c9db48b67c41e1c906eab6e976501b | 실제 도착·출처·경로·D2/창 분리·12반례·카드·감도 |
|④ 결과·점검·수용 |이 파일을 포함하는 결과 커밋; 정확 SHA는 마지막 HANDOFF 및 검증 영수증 | 본표8·24행, 자기점검, 수용 상태. 결과 SHA를 자기 파일에 재귀적으로 넣지 않음. |

계획 통합판d8c8d029bfb6107520ae74d2a172b2b18840e764와 실제 시작판522ea9092d4d56ef6db0bd4f707bfc90032e179e를 manifest에 따로 남겼다. 읽은 의존 HANDOFF는033의03ff2eb1264b85016266de1f36ddebe45f5fface와048의132e0108e652bdd2413edb71dfd6531507ea63e8이다. 기존033의0/8,048의두풀·각3후보는 배경이며 이번 수치에 더하지 않았다. dot-control 및 owned_path 밖은 편집하지 않았다.

## 영향이 큰 불일치·약점 세 가지

'''

SELF=r'''# AF-RES-052 자체 점검

판정: **부분 인계**. 최소 직접 자료 배당,8자리/24행의 보존, 고정 순서 A/B/C 계산, 진단 경로·반례·감도는 갖췄다. 본표에서 요구와 연결된 비어 있지 않은 풀을 얻지 못해 독립 완결 구현의 요구별 증감은 일반화할 수 없다. 양성0 자체를 실패 기준으로 삼지 않았다.

| 질문 | 답·확인 범위 | 근거 파일·행/ID | 반대 증거 | 남은 결손 | 다음 첫 행동 |
| --- | --- | --- | --- | --- | --- |
| Q1 |80개 생성순 모집·첫 적격2개씩·필수조건2개/옵션/근접 오답/조합을 목적지 전 고정 | frame.csv issue_screen80; evidence.csv2–9; PY-I564/I574; M-ISS-941/955 | setup.py 부재는 금지 아님; HTML 렌더 동등성은 raw 출력 조건을 만족하지 않음 | 생성 당시 본문4건·첨부2건·941 literal 패키지 식별 | 원 첨부/lockfile 확보; 현재 REST본문을 원판으로 바꾸어 부르지 않기 |
| Q2 | 원본 commit/blob/편집 순서 고정; 자연4무매치; 보강1메타데이터풀·3미충원 | pools.csv2–6; slots.csv2–9; domain function/section scans | 원4 PyPI는 같은 구현 계열; Official은 기능 절 아님 | 기능 절 정의가 목록 노출 뒤 정정; D-P1 build:index 정확URI | 새 공식 기능 목록을 새 차수의 사전 규칙으로 고정; 현재빈자리대체금지 |
| Q3 | A정확URL/B상류/C5필드·첫대표·최대3을 사전 봉인 | groups.csv2–25; ea4fa69; CORRECTIONS C01–C04 | C는 제품판/역할 결측 또는 부품 차이로 A와 같음 | 실제5필드 C충돌 없음; routing README 선노출 | 결과 독립인 표시5필드가 모두 알려진 충돌 풀 확보 |
| Q4 | P-S1 49·D-M1 50·D-P1 57경로행; 같은 창/동작예산·한 시행 근거만 결합 | paths.csv; domain arrivals; ME-GOLD-C1/C2 vs ME-R4-C1/C2 | B-P08은 C1만; D2 정답은 사용자2동작 밖; 원4 PyPI부분창 | UI실험·D3·역사판·-h/Compose/build정확도착 | REPRODUCE·REPLAY_PLAN의 입력으로 고정판/정확주소 재현; 불완전경로 성공처리금지 |
| Q5 | URL승격과 구현승격·원자증거·보완문서접근을 분리 | changes.csv2–28; counterexamples.csv2–13; paths.csv148 | AWS보완서비스, mdast명세, trove뒤쪽병합; 완결0이어도 C1증가 | 주표본 목적 연결0으로 효용효과 식별 불가 | 요구 일치 목적을 먼저 고정한 새 프레임; 동일판 완결창 확보 |
| Q6 | 개별 연주2레코드·Inter2판의 문서와 식별을 비교, software분모 제외 | sources.jsonl133–138; crossfield/findings.md; X01–04 | Inter/Inter V는 이름만 다름; 한 원문이 여러flavor설명 | 음향/편곡·fvar·브라우저미검사 | 그 조건이 실제요구라면 승인된녹음/고정배포파일로 검사 |
| Q7 | 세 카드형식·빈풀카드·3→4슬롯·판결측감도·정확rank조건 | cards.md; sensitivity.csv2–41; RESULT 두표 및 카드 절 | slot4에원4가들어오면C1경로우세사라지나완결0유지 | 기본B/C채택·독자효용·사용자채택미검증 | 역할·판·확인조건 표시카드부터 새연구에서 비교; 범용정책채택보류 |

## 미확인과0 구분

- 자연층의 반환 ID0은 고정 매치 배열의 관측이다. 생태계의 구현 존재는 미확인이다.
- 미충원 보강3자리의 완결 ID·증감은 미확인이다. 시행 최대·조건부 비율은 해당 없음이다.
- P-S1은5URL을 읽었어도 사전 목적이 없어 완결·증감은 null이다.
- D-M1의 현재 창 완결0과 역사판 미확인은 다르다. 조건부 현재 D2 계보1도 실제설치·실행1이 아니다.
- 사람의 채택은 미측정이다. 독립 모델 판독을 사람 간 일치도나 실제사용자실험으로 쓰지 않는다.

## 검증과 잔여 실행

검토자는 evidence/crossfield/stage3-review.md에서13파일의해시와원장을 독립 대조했다. verify_research.py는8/24행·소유경로·출처중복/실패제외·경로≤2·ID참조·단위/null·동결입력불변·결과말미3행을검사한다. 구조통과가역사적정답·UI효용의통과는아니다.

실제 명령·stdout/stderr·종료 코드는 evidence/local-validation.json 및 고정결과후 evidence/final-verification.json으로 확인한다. session check는사용자가지정한--fetch를그대로쓴다. 원격재열람은고정SHA의RESULT와acceptance를직접읽고로컬gitblob과동일성을비교한다. 이증거를남기기전HANDOFF는작성하지않는다.

설치/동작시험은이번D2조사의실행결과로주장하지않았으며, 역사요구재현에필요한첨부는결손이다. REPRODUCE.md와evidence/markdown/REPLAY_PLAN.md에명령·입력·전제·기대조건을남긴다. 코드·시험읽기,목록재구성,동일창경로재사용,별도저작자료배당을독립적으로점검했다.
'''

def evidence_ref(file, ids):
    return {'file':file,'ids':ids,'lines':[INDEX[file][i] for i in ids]}
def criterion(cid,status,num,den,unit,refs,reason=''):
    return {'acceptance_id':cid,'status':status,'numerator':num,'denominator':den,'unit':unit,
            'evidence':refs,'unmet_reason':reason}

criteria=[
 criterion('AC01-start-and-pins','satisfied',1,1,'session start receipt',[
     {'file':'manifest.json','locator':'base_sha, integration_sha, dependencies, research_context'},
     {'file':'evidence/start-receipt.json','locator':'exit_code and stdout'}]),
 criterion('AC02-natural-frame','satisfied_with_limits',80,80,'direct issue bodies',[
     {'file':'frame.csv','locator':'record_kind=issue_screen'},
     evidence_ref('sources.jsonl',['PY-I564','PY-I574','M-ISS-941','M-ISS-955'])],
     'Creation revisions not recovered; later comments not used; two Markdown attachments inaccessible.'),
 criterion('AC03-natural-selection','satisfied',4,4,'selected natural requirements',[
     evidence_ref('slots.csv',['P-N1','P-N2','M-N1','M-N2']),
     evidence_ref('evidence.csv',['E-P-N1-R1','E-P-N1-R2','E-P-N2-R1','E-P-N2-R2','E-M-N1-C1','E-M-N1-C2','E-M-N2-C1','E-M-N2-C2'])]),
 criterion('AC04-supplemental-pools','partial',1,4,'metadata pools for planned slots',[
     evidence_ref('slots.csv',['P-S1','P-S2','M-S1','M-S2']),
     {'file':'CORRECTIONS.md','locator':'C01; v1 cd940aa, v2 ea4fa69'}],
     'Three slots unfilled. Python first20 functional sections yielded no strict C collision; Markdown five categories yielded zero functional sections. Definition corrected after catalog exposure.'),
 criterion('AC05-purpose-linked-supplemental','not_estimable',0,1,'linked purposes among observed metadata pools',[
     evidence_ref('evidence.csv',['PY-E01','PY-E05','PY-E06'])],
     'No prefrozen eligible user purpose matches mirroring/cloud storage. Do not turn null completion into observed failure.'),
 criterion('AC06-arrays-before-arrivals','satisfied_with_limits',24,24,'primary A/B/C rows sealed',[
     {'file':'groups.csv','lines':[2,25],'commit':'ea4fa69f841dca2c470b62c3fdf1ee4d9029712e'},
     {'file':'SCOPE.md','locator':'v2 routing exposure disclosure'}],
     'Diagnostic remark root README was also routing input and pre-exposed. All keys remain catalog-only; no full blindness claim.'),
 criterion('AC07-strict-C-collision','unobserved',0,20,'Python functional sections with eligible known-field collision',[
     {'file':'evidence/python/functional-scan.csv','locator':'all20'},
     {'file':'evidence/markdown/section-scan.csv','locator':'five editorial categories, zero functional sections'}],
     'Unknown product version/document role or different fields prevent eligible collision. Markdown conditional section denominator0 is not applicable.'),
 criterion('AC08-primary-arrival-window','partial',4,5,'complete bounded source windows',[
     {'file':'evidence/python/arrivals.jsonl','lines':[1,2,3,4,5]}],
     'PyPI rank4 initial7.0.0 retained347 words; later8.2.0 response cannot complete that snapshot. Exact-h anchor and Compose second hop also incomplete/failed.'),
 criterion('AC09-two-action-accounting','satisfied_with_limits',156,156,'path ledger rows, including8 uninstantiated diagnostic rows',[
     {'file':'paths.csv','lines':[23,178]},
     evidence_ref('paths.csv',['D-M1-B-P08'])],
     'This is paired reconstruction from directly obtained source windows, not156 human traversals. Eight D-P1 rows retain unresolved starts/hops;21 empty status rows are separate.'),
 criterion('AC10-required-tables','satisfied',24,24,'primary comparison rows',[
     {'file':'RESULT.md','locator':'first two tables:8 slots and24 methods'},
     {'file':'evidence/required-table-data.json','locator':'table1.rows8/table2.rows24'}]),
 criterion('AC11-source-allocation','satisfied',24,24,'deduplicated credited primary works',[
     {'file':'evidence/source-counts.json','locator':'credited_source_ids and allocation_counts'}]),
 criterion('AC12-counterexamples-and-sensitivity','satisfied',12,12,'explicit counterexample investigations',[
     {'file':'counterexamples.csv','lines':[2,13]},{'file':'sensitivity.csv','lines':[2,41]}]),
 criterion('AC13-crossfield','satisfied_with_limits',4,4,'individual recording/version records',[
     evidence_ref('sources.jsonl',['X01','X02','X03','X04'])],
     'No audio playback or fvar/runtime checks; these cases are not software-hit counts.'),
 criterion('AC14-Q1-Q7','satisfied_with_limits',7,7,'questions with direct evidence or concrete unknown/restart',[
     {'file':'SELF_CHECK.md','locator':'Q1–Q7 table'},{'file':'RESULT.md','locator':'Q1–Q7 sections'}],
     'Independent completed implementation gain/loss remains unidentifiable in primary sample; target positive existence is not a completion gate.'),
 criterion('AC15-fixed-result-verification','pending_after_result_freeze',None,1,'remote reread and actual session check',[
     {'file':'evidence/final-verification.json','locator':'to be written only after result commit; no fabricated execution status'}],
     'Cannot verify the result commit before it exists. This row is finalized in a separate post-result verification commit before HANDOFF.'),
]
acceptance={'task':'AF-RES-052','overall_status':'partial_handoff','research_result_status':'partial',
    'positives_are_not_a_completion_requirement':True,
    'reason':'Required source quota and complete reporting are satisfied; matched-purpose nonempty primary pools, strict C collision, historical identity and some exact arrivals remain unavailable.',
    'units':{'natural_opportunity':{'numerator':0,'denominator':4,'unit':'natural requests'},
        'supplemental_metadata':{'numerator':1,'denominator':4,'unit':'planned slots'},
        'supplemental_purpose_linked':{'numerator':0,'denominator':1,'unit':'observed metadata pool'},
        'supplemental_completion_rate':{'numerator':None,'denominator':0,'unit':'purpose-linked pools','display':'해당 없음'},
        'original_primary_urls':5,'primary_complete_implementation_count':None,'human_adoption':'미측정'},
    'source_counts':COUNTS,'criteria':criteria,
    'next_first_action':'In a new preregistered round, locate an official functional section matching an independently fixed eligible user purpose; preserve this frame and empty slots.'}

(ROOT/'RESULT.md').write_text((ROOT/'evidence/required-tables.md').read_text()+BODY+WEAKNESSES)
(ROOT/'SELF_CHECK.md').write_text(SELF)
(ROOT/'evidence/weaknesses.md').write_text(WEAKNESSES)
(ROOT/'evidence/acceptance-evidence.json').write_text(json.dumps(acceptance,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'result_lines':len((ROOT/'RESULT.md').read_text().splitlines()),'criteria':len(criteria),'status':acceptance['overall_status']},ensure_ascii=False))
