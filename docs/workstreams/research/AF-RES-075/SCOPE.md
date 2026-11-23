# AF-RES-075 · 모집과 판정 사전 고정

## 시작과 인수 범위

계획 기준 SHA는 [39cadb6](https://github.com/laadkke-arch/agentflow-open/tree/39cadb6ecdf62d0b21c0cce67834f2aef3bf6853)이다. 그 판의 작업표에서 스키마·상태 필드를 확인했다. 075 항목은 이후 PLAN#18 반입 때 추가됐다. 첫 GitHub 조회에서 배정 커밋 3ac1f42628930ead89dfcb1bd38f3a8e74c9c192를 보았고, 브랜치 확인과 checkout 때의 통합 HEAD인 **817ee771ebfa63d4a177ee12f46b9818a6335308**에서 작업을 시작했다. 그 판의 AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW와 진행표의 075 항목(`RUNNING`, attempt 1)을 읽었다. 원격 작업 브랜치가 없었으며 [작업 계약](manifest.json)은 그 통합 SHA, 소유 경로, 의존 하나를 고정했다.

071의 인계는 [f8b3fc8의 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/f8b3fc86b8eb6ba71e02866b48551245b5dbd95f/docs/workstreams/research/AF-RES-071/HANDOFF.md)다. [cb4931b의 Q3·Q7](https://github.com/laadkke-arch/agentflow-open/blob/cb4931b38b3d75e98da1291628ec66966507be29/docs/workstreams/research/AF-RES-071/RESULT.md) 및 [storage.py의 보기 경계](https://github.com/laadkke-arch/agentflow-open/blob/cb4931b38b3d75e98da1291628ec66966507be29/docs/workstreams/research/AF-RES-071/experiment/storage.py)를 확인했다. 주 22쌍의 과거 원본 소실 재계산 0/22·0/22·22/22와 LOSS01 보류는 그 보고의 관측이다. 여기서는 아카이브/현재 진입점 분리, 문구/판정 분리, 손실 대조를 인수한다. 새 검증 단위는 당시 후보 모집의 완전성이다.

## 발행판과 모집

2024-12-31 UTC 시작 직전까지 공식 발행된 정식판 중 실제 출판 순서의 뒤 두 판을 택했다. PyPI 프로젝트 이력은 2.17.2(2023-11-21) → 2.18.0(2024-05-04) → 2.19.0(2025-01-05)이다. IANA 발행 색인은 2024a(2024-02-01) → 2024b(2024-09-05) → 2025a(2025-01-16)다. 반입한 정확한 SHA·태그 객체·원천 주소·파일·해시·바이트·전체 행 수는 [manifest](inputs/manifest.json)와 [모집틀](frame.csv)에 고정했다. IANA가 제공하는 두 버전의 원문 표는 웹으로 열었다. 셸에서 IANA 아카이브를 요청했을 때 CONNECT 403이어서 바이트 봉인은 유지관리자 공개 Git 태그 아카이브에서 추출하고 동일 커밋 Git blob과 대조했다. PyPI의 두 sdist는 발행 메타데이터 SHA-256과 태그 Git blob을 모두 맞췄다. [PyPI 발행 이력](https://pypi.org/project/Pygments/2.18.0/#history) · [IANA 발행 색인](https://data.iana.org/time-zones/releases/) · [취득 기록](evidence/acquisition.json)

| 분야 | 모집 단위 | 전 → 후 | 질의와 제외 조건 |
| --- | --- | --- | --- |
| PG | 배포한 LEXERS 딕셔너리의 클래스 키 1개가 후보 1개다. 기본 파일명 패턴이 비어 있어도 모집 행이다. | 575 → 584행 | `filenames`만 평가한다. 엔트리포인트 플러그인, `alias_filenames`, MIME, 내용 추정은 이 질의 밖이다. |
| TZ | `zone1970.tab`에서 주석과 공백 행을 제외한 열 3 이름 1개가 후보다. 열 1의 모든 쉼표 토큰을 평가한다. | 312 → 311행 | `zone.tab`, `zonenow.tab`, `backward` Link, 날짜별 오프셋, 지점의 실제 위치나 관할은 이 질의 밖이다. |

PG의 표시명·별칭·모듈 변경은 클래스 키가 같은 동안 같은 ID다. 클래스 키 자체를 바꾸면 전후 기록에서 제거+추가로 세며, 확인한 계보를 설명에 따로 둔다. TZ도 열 3 철자 그대로 식별한다. 과거 이름이나 `backward`의 Link는 별도 후보로 올리지 않는다. 행 순서와 표시 출력의 정렬은 독립이다. UTF-8의 Unicode 코드포인트 순으로 ID를 출력한다. 자료 인용의 줄 번호는 1부터 시작한다.

## 세 문장과 순위

- E `exists`는 적격 ID 수가 1 이상인지를 묻는다. 정확히 대응하는 한 원절이 참의 증인이다. 거짓에는 완전한 모집에서 공집합임을 확인한 기록이 필요하다.
- U `unique`는 적격 ID 수가 1인지 묻는다. 한 증인에 다른 후보가 없다는 근거가 더 필요하다. 서로 다른 두 적격 ID만 확보해도 거짓을 확정할 수 있다. 공집합의 거짓은 모집을 닫아야 확인된다.
- R `top`은 적격 중 최고 점수에 도달한 **모든 ID**를 묻는다. 공집합은 빈 배열이다. 인용을 대표할 한 ID가 필요할 때만 R의 첫 ID를 잡는다. 이 정렬은 동점 선택 기준으로 쓰이지 않는다.

PG 입력은 POSIX basename으로 해석한다. 대소문자를 구분하는 `fnmatchcase`로 패턴을 검사하고, 맞은 패턴 중 `*`, `?`, `[`를 포함하지 않는 패턴이 있으면 2, 그 외 맞은 패턴이 있으면 1이다. TZ는 정확히 대문자 ASCII 2글자 토큰을 요청한다. 열 1에 있으면 적격이며 첫 토큰으로 있으면 2, 그 뒤에 있으면 1이다. 점수 2는 이 연구의 우선 정책이다. TZ 표의 설명은 도시 인구와 표 순서에 관한 편집 규범을 별도로 둔다. PG 네이티브 filename 검색은 등록된 플러그인도 보고 파일명 보너스, 클래스 `priority`나 코드의 `analyse_text`, 클래스명으로 정렬한다. `guess_lexer_for_filename`은 `alias_filenames`와 본문 추정을 별도로 쓴다. 네이티브 결과는 자연 4쌍에서 설치 플러그인 없는 sdist로 보조 확인한다. [PG 네이티브 함수](https://github.com/pygments/pygments/blob/d7d11f6e6d3aa97805215c1cc833ea5f0ef1fcbb/pygments/lexers/__init__.py#L169-L208) · [TZ 열·순서 머리말](https://data.iana.org/time-zones/tzdb-2024b/zone1970.tab) · [결정 규칙](inputs/rules.json)

## 자연 표본과 통제 가설

자연 질의 시드는 PG `Android.bp`, `example.h`, `example.lean`, `example.m`이고 TZ `CA`, `DE`, `MN`, `PT`다. Soong·Lean은 2.18.0 발표, h·m은 파일명 충돌 관점의 고정 질의다. MN·PT는 2024b의 변경 요약, CA·DE는 다중·공유 국가 행의 대조다. 각 분야에서 두 판의 행 ID 합집합을 코드포인트 순으로 순회한다. 질의별로 어느 한 판에서라도 적격인 첫 ID를 앵커로 잡고, 앵커 ID 순으로 N01~N04를 배정한다. 앵커 동률이면 질의 문자열을 차순위로 쓴다. PG의 이 방법은 파일명에 대응하는 행이 한 판에만 있어도 포함한다. 앵커는 표본 선택에만 사용한다. 신·구 결과가 같은 질의를 교체하지 않는다. 발표를 보고 고른 목적 표본이므로 배포 전체나 일반 사용자 질의의 변화율을 추정할 수 없다. [PG 2.18.0 발표](https://github.com/pygments/pygments/releases/tag/2.18.0) · [TZ 2024b 공지](https://lists.iana.org/hyperkitty/list/tz-announce%40iana.org/message/IZ7AO6WRE3W3TWBL5IR6PMQUL433BQIE/)

통제는 두 분야 모두 최종 정식판 원본의 복사본이다. seed **75075**는 추가 별칭·가상 후보의 접미사를 재현하는 데만 쓰고 질의 선정이나 순위에는 쓰지 않는다.

| 통제 | PG | TZ | 관측 전 기대 |
| --- | --- | --- | --- |
| C01 | probe.abap의 ABAPLexer와 같은 키를 가진 가상 클래스 행 추가 | AD의 Europe/Andorra와 같은 국가 키를 가진 가상 행 추가 | E 유지, U 참→거짓, R 동률 확대 |
| C02 | probe.abap에서 ABAPLexer 행 제거 | DE에서 Europe/Berlin 행 제거 | PG 공집합, TZ 기존 단독 1위 탈락 및 후순위 승격 |
| C03 | example.m와 무관한 ABAPLexer 표시명 변경 | DE와 무관한 Europe/Andorra 주석 변경 | 후보·답·대표 원절 바이트 유지 |
| C04 | example.m의 MatlabLexer에 별칭 추가, 데이터 행 순서 반전 | DE에서 행 순서 반전, 국가 열 토큰 순서는 유지 | 후보·답 유지, 번호/PG 별칭은 변경 가능 |

주 분모 밖 SWAP01은 PG 동점 후보 중 대표가 아닌 하나를 같은 키의 가상 ID로 교체한다. 모집 및 적격 행 수와 대표 원절 해시를 유지하며 R은 달라져야 한다. LOSS01은 B의 대표 밖 동점 행 하나를 누락한다. LOSS02는 B/C의 옛 결정 규칙을 숨긴다. 검증 우회와 스스로 새 지문을 만든 목록도 부가 대조로 둔다. 이 기대는 판독기에 전달하지 않는다.

## 공평한 제공 범위와 확인

같은 옛 전체 스캔에서 A에 판·주소·대표 원절·증인 이유를 투영한다. B는 동일 A에 모든 모집 행의 질의 판별 키, 앵커로 사용할 당대 전체 스캔 영수증, 포함/제외 수, 최고점 동점 수와 규칙을 더한다. 필터 밖 행에도 ID와 판별 키가 있어 B가 직접 제외를 다시 적용할 수 있다. C는 A와 전체 파일, 파일 지문 및 규칙을 보존한다. 세 보기 각각 옛 출력 문자열 저장을 공통 비용에 넣고 표시 작업만에서 읽는다.

보존에서는 같은 주소로 과거판 바이트와 그때의 공개 규칙을 요청할 수 있다. 소실에서는 그 라우트만 실패한다. 모든 보기가 현재판의 동일 도메인 목록 진입점을 최대 1회 같은 한도로 읽는다. 과거는 필요한 경우 초기열람 1회, 기권 직후 진단 1회다. 파일당 전송 한도를 131072B로 둔다. 실험의 원본 서비스는 로컬 재생이며 현행판은 각 쌍의 후판이다. 발행사 파일 취득의 HTTP 관측은 별도다.

전수 정답기는 별도 프로세스·입력 폴더의 전체 원문과 질의만 받아 독립 파싱·매칭·집합 구축을 한다. 판독기는 투영 저장과 제한된 라우트만 받는다. 고유 쌍 ID, 실험 종류, 숨은 경쟁자, 기대 또는 정답은 판독 요청의 필드가 아니다. 정답·판독은 종료 후 합친다. 주 판정 분모는 16쌍의 E/U/R 각각 A/B/C × 두 조건으로 288자리다. 사람이나 별도 모델의 독립 검토 여부는 구현의 독립 판독과 따로 적는다.
