# AF-RES-044 · HANDOFF

**상태: 연구 수용 미충족 / 후속 관측 필요.** 요청된 네 묶음의 원격 커밋, 고정 결과·수용 원장 재열람, 실제 session check까지 마쳤다. 조사 산출물과 미충족 사유를 남기며 이 인계서만 마지막 별도 커밋으로 저장한다. 미관측 값을 성공이나 0으로 바꾸지 않았다.

## 고정 결과와 읽을 위치

| 항목 | 고정 값·위치 |
| --- | --- |
| 저장소·작업 브랜치 | `laadkke-arch/agentflow-open` · `work/research-af-res-044` |
| 결과·수용 원장 고정 SHA | **`176e2eee3c00257d7dcc64665c74b12bf4399913`** |
| 결과 | [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/176e2eee3c00257d7dcc64665c74b12bf4399913/docs/workstreams/research/AF-RES-044/RESULT.md) — 표1 헤더3행/본문5–16행(12요구), 표2 헤더18행/본문20–55행(36요구×방식). 제목 바로 뒤 두 표, 마지막 정확히 약점3행 |
| 수용 원장 | [acceptance-evidence.json](https://github.com/laadkke-arch/agentflow-open/blob/176e2eee3c00257d7dcc64665c74b12bf4399913/docs/workstreams/research/AF-RES-044/evidence/acceptance-evidence.json) — **27/33조건 충족**,6조건 미충족. 각 조건의 단위·분자/분모·파일/행·다음 첫 자료 포함 |
| 자체 점검 | [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/176e2eee3c00257d7dcc64665c74b12bf4399913/docs/workstreams/research/AF-RES-044/SELF_CHECK.md) — Q1~Q7 주장·원문 위치·반증·미확인·뒤집을 조건과 재현 명령 |
| 고정 재열람·실제 check 영수증 커밋 | **`c422cefcd0013148295f2402e93db1f3a82a33e5`** — `evidence/fixed-result-reopen.json`, `evidence/session-check.json` |
| 유일한 변경 범위 | `docs/workstreams/research/AF-RES-044/` |
| 배정시 통합 SHA | `333e83c9a46b0c005d22efcccbb5a055b27e904e` |
| 계획시 통합 SHA | `785880f7b7c380dd49e0e4e6e6d90715a9b27838` — 배정시 SHA와 구별해 manifest에 보존 |
| 실제 check 시 통합 HEAD | `606bced963b6591e8c64122169056c688e0b310f` — 계약 해시는 동일하며 check 통과 |
| 의존 결과 | AF-RES-040 `9bff55706d5b1a939e39185bda9cf6f22bea246b` — 고정 HANDOFF/RESULT/pool/losses/method-clarifications를 읽음. 기존8사례 재판정 안 함 |
| 실행 환경·모델 표시 | ChatGPT 공유 Linux shell+GitHub connector, Python3.12.14. 제공 모델 표시는 GPT-6 Astra Pro, 배정 worker는 web-pro, 실제 웹 UI 모델 선택은 **미확인** |

## 질문의 현재 답

세 자리 목록의 중복 제거는 **대표 문서가 이미 제공하는 완전 근거**, **뒤에 남은 별개 구현**, **같이 읽어야 하는 보완 절**, **도착 범위와 클릭 비용**에 따라 다른 결과를 냈다. 같은 상류 프로젝트라는 사실만으로 요청의 모든 필수조건을 대표가 입증하는 것은 아니다.

A는 동일 exact URL, B는 같은 상류 프로젝트, C는 표시 시점의 부품·용도·판·근거 역할을 사용했다. C에 완전 답안이나 gold 적격 등급을 넣지 않았으며 미확인 키는 개별 표시했다. 관측8풀에서는 C가 A와 같아 실제 C 병합 효과를 식별하지 못했다. P의4풀 결측을 무변화의 증거로 쓰지 않는다.

| 보강 요구 | 원풀 적격 | 직링크 완전 ID A/B/C | 두 클릭 원풀 ID별 도달 A/B/C | 해석 |
| --- | --- | --- | --- | --- |
| C1 Python HTTP client | 2 | 1/2/1 | 1/2/1 | B가 뒤의 Requests를 복원. 단, 확인된 한 시행 최대는1/1/1. HTTPX와 Requests를 다른 시행에서 읽은 결과를 한 사용자 답으로 합치지 않음 |
| C2 Python 표 데이터 시각화 | 11 | 11/10/11 | 11/11/11 | B는 Matplotlib의 직접 근거를 가리지만 ecosystem→chart 실제 href 두 클릭에서 원풀11을 한 시행에 확인. Altair/Bokeh는 첫 대표가 이미 입증하므로 새 복원으로 세지 않음 |
| C3 Python3.11 ExceptionGroup/except* | 1 | 0/0/0 | 1/0/1 | B는 보완 계약의 기본 두 클릭 완결을 가림. 같은 열린 문서의 추가 절만 허용하는 W에서 B도1로 바뀜 |
| C4 Python3.11 TaskGroup/async-with | 확인0 | 0/0/0 | 0/0/0 | 봉인한 A2의 두 await·예외 전달 절차를 원풀 strict 범위에서 입증하지 못함. 양성 미충족, 조건부 비율 **해당 없음** |

보강 전체의 직접 제공 수는 A/B/C 모두12/14, 두 클릭 ID별 수는 모두13/14다. 총합이 같아도 C1의 Requests 이득, C2의 직접 Matplotlib 손실, C3의 보완 계약 손실이 서로 상쇄된다. C2가 원풀 분모의11개를 차지하며11개는 frontend/library 대안이지 서로 독립인 렌더링 엔진11개가 아니다. 해법을 보고 고른 보강의 합계를 자연 발견률로 일반화하지 않는다.

자연 이름층4건과 계약층4건은 각각 Pandoc2풀 미관측, Vega-Lite2풀 관측이다. 관측된 Vega4풀에서 확인된 완전 대안은0이며 그 조건부 비율은 **해당 없음**이다. Pandoc의 분모는 **미확인**이다. V3는 `text` 토큰이 최초 원요구 명사에서 나오지 않아 원규칙 분석에서 제외되며 대체 fallback 풀은 미확인이다. 따라서 자연8건의 일반 회수 효과는 아직 판별하지 못했다.

C2의 IPython Vega와 qtpandas는 각각 같은 출발 카드→외부 저장소의 새 독립 시행에서 빠진 Python 조건을 채웠다. 실제 추가 시행은2회이고 A/B/C별6회가 아니다. 각 시행에서 기존10대안+추가1대안만 확인했으며 원풀 분모11과 회수 분자는 그대로다. 추가2개를 같은 두 클릭에 함께 읽었거나 Matplotlib까지 한꺼번에 확인했다고 집계하지 않았다.

**색인 제안:** `요구 atom → 근거 절 → 판·방향 → 원멤버` 연결을 보존하고, 카드 수·원풀 완전 대안 수·한 시행 확인량을 별도 필드로 내보낸다.

## 충족과 미충족

출처 원장은632관측행이며 중복·fragment·재독·접속 실패를 제외한 고유 산입 원문은 **84개**다. 추가 경로를 빼도 핵심 원문53개이며 Vega 추가 경로31개를 별도로 센다. 원요구8, 공식 비교/결정4, 공급자 근거25, 발행/호환/시험6, 박물관4, 교통4개의 최소 범주를 충족했다. 같은 원문을 여러 범주로 부풀린 총합을 원문 수로 쓰지 않는다.

자연48+보강24=72슬롯을 보존했다. 비빈41개는 모두 직접 열기를 시도했고 정확 도착창은40개에서 확인했다. C1-6은 HTTP200이어도 fragment가 없어서 실패다. 고유 exact URL41개, fragment를 접은 후보 원문22개와 완전 대안14개는 서로 다른 수다.36보기 기록은108반환칸이고, 관측 가능한24보기와 P 결측 fixture12보기를 구별한다.

고정 계획/관측1,924회, 별도 Requests browser1회, C2 exact-response 재검증2회로 **고유 시행1,927회**를 기록했다. 승인한 의미 판독 범위3,051개와 성공한 원문 도착3,367회도 따로 계산했다. 이는 사람의 클릭·이해·선택·채택 관측이 아니다. 문서상 계약을 외부 예제 프로그램의 실행 성공으로 승격하지 않았다.

| 미충족 수용 조건 | 확인 수/목표 | 막힌 이유·다음 첫 행동 |
| --- | --- | --- |
| 자연48 raw 순서 | 24/48 | Pandoc24슬롯의 원 발행 응답 바이트 결측. 공식 MANUAL 원응답을 새 획득 버전으로 먼저 봉인 |
| 원규칙 준수+관측된 자연 요구 | 3/8 | P4풀 결측 및 V3 `text` 토큰 이탈. 원요구 명사와 no-match fallback을 사전 고정한 별도 amendment |
| 관측된 입력을 가진36보기 | 24/36 | P12보기는 결측 fixture. 이를 실제 첫 화면 성공으로 세지 말고 새로운 원풀 관측부터 재개 |
| 완전 경로를 가진 보강4건 | 3/4 | C4 A2 미입증. 조건을 완화하지 않은 새 공식 해결/시험 사례를 찾아 자연6순서와 근접 오답부터 봉인 |
| 별개 원풀 대안 복원 양성2건 | 1/2 | C2 첫 대표가 뒤의 대안을 이미 입증. 첫 대표에 없는 별개 완전 대안이 실제로 돌아오는 새 비교 원문 필요 |
| 보완 문서·판 차이 양성2건 | 1/2 | C3만 원풀 완결 경로 입증. C4 외부 async-with 절의 존재를 원풀 양성으로 전용하지 않음 |

박물관에서는 Great Wave의 작품명과 각 인상 레코드의 objectID·치수·취득 기록을 구별했다. 교통에서는 A 노선명과 방향·지선·시간대, 시간표의 timepoint 생략을 구별했다. 한 PDF가 여러 방향을 담는 반례도 확인했다. 단일 대표가 충분한지는 이름 일치만으로 판단할 수 없다. 분야 사례와 W/U는 RESULT 후반 및 SELF_CHECK Q7에 있으며12요구 분모에 새 사례로 더하지 않았다.

## 커밋·검증 순서

| 순서 | 원격 SHA | 범위 |
| --- | --- | --- |
| ① | `0832f18bcb040871fa300db708a67d6f7f8866c7` | 표집·노출·그룹 키·클릭 규칙, manifest |
| ② | `b36cc513ccbc1616168401ec9564866038e880a3` | 최초 요청·80노출·72슬롯·보강 풀·요구 원자·표시 metadata 봉인 |
| ②b | `8c22675a2e90134c386f362cdd2aabe7d14d252e` | CSV LF 해시 정정과 v1 보존, 후기 browser 진단 |
| ③ | `ed63f44ff0586265d6640bedb82fc6c5c286f9b1` | 후보 근거·36보기·최소 완전 경로·실제 도착 원장;134파일 원격 blob 검산 |
| ④ | `c92cf9924ef4935fb77eb555d5bfedacc09ee9b3` | 요구별 짝 집계·반례·SELF_CHECK·수용 원장·203개 검산;13파일 원격 blob 검산 |
| 발행 확인 | `176e2eee3c00257d7dcc64665c74b12bf4399913` | 묶음④ 실제 SHA로 절차 조건 확정. 결과/수용 원장의 고정 결과 SHA |
| 재열람·check 영수증 | `c422cefcd0013148295f2402e93db1f3a82a33e5` | 고정 두 파일 GitHub 재열람·blob 일치 및 실제 session check stdout |
| 최종 인계 | 이 파일만 포함한 마지막 커밋, parent=`c422cefcd0013148295f2402e93db1f3a82a33e5` | HANDOFF.md; 자체 commit SHA를 파일 안에 순환 참조하지 않음 |

로컬 push는 HTTPS credential 부재로 실패했으므로 인증된 GitHub blob/tree/commit/update_ref로 원격에 저장하고 git fetch로 실제 내용을 검증했다. expected SHA를 지정했으며 강제 ref 갱신은 없었다. dot-control.json 및 허용 경로 밖 문서는 수정하지 않았다.

결과·수용 원장은 고정 SHA에서 다시 열어 내용과 Git blob SHA가 일치함을 확인했다. 필수12행·36행·약점3행, 동일 입력과 고정 라벨5자/설명0자, 비용≤2, 구현별·시행별 완결 ID와 양방향 손익 등 **203/203 검사 통과**다. 내부 에이전트 재판독도 같은 연구팀의 자체 점검으로 표시했다.

실제로 완료한 저장소 점검은 다음과 같다.

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-044/manifest.json --fetch
```

종료코드0, `status=passed`, `freshness=remote_checked`, `outside_paths=[]`, `unmerged_paths=[]`, `errors=[]`. 검사 완료 시각은2026-11-22T21:30:51.804931+00:00, 검사 checkout은 고정 결과SHA176e2eee다. Git 계약·소유 경계 검사의 통과가 실증 미충족6개를 해소하지는 않는다.

## 재현 명령·재개 입력

저장소 루트의 고정 결과 checkout에서 저장된 관측을 재집계하려면 다음 순서다. 새로운 네트워크 도착을 기존 시행으로 덮어쓰지 않는다.

```bash
python -B docs/workstreams/research/AF-RES-044/evidence/consolidate_sources.py
python -B docs/workstreams/research/AF-RES-044/evidence/calculate_results.py
python -B docs/workstreams/research/AF-RES-044/evidence/make_report.py
python -B docs/workstreams/research/AF-RES-044/evidence/verify_study.py
```

입력은 봉인된 `pool.csv`, `requirements.csv`, `views.jsonl`, 후보/두 번째 도착 의미 판독 파일, `trial-plan.jsonl`, `trial-observations.jsonl`, `browser-observations.json`, `control-second-hop-revalidated-trials.json`이다. 상세 파일 SHA는 발행 영수증과 내부 감사에 있다. 재실행의 생성 시각 변경은 기존 고정 SHA와 구별해 기록한다.

**막힌 부분의 다음 첫 행동은 Pandoc 공식 MANUAL의 원응답 바이트 확보다.** 이 환경에서는 shell403과 공식 fallback 부재를 기록했고 후기 browser DOM만 복구했다. 아래는 원응답을 받을 수 있는 승인된 실행 환경에서 재개할 명령과 입력이다. 이 명령의 새 성공 결과는 이 세션에서 실행·확인한 것으로 기록하지 않았다. 새 폴더에만 원응답·href 원순서를 남기며, 기존24결측이나 원규칙 수치는 바꾸지 않는다.

```bash
python -B - <<'PY'
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urljoin
from html.parser import HTMLParser
import json, hashlib, datetime
out = Path('docs/workstreams/research/AF-RES-044/evidence/reacquire-pandoc')
out.mkdir(parents=True, exist_ok=True)
url = 'https://pandoc.org/MANUAL.html'
receipt = {'url': url, 'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'primary_pool_changed': False, 'revision': 'new acquisition, preserve original missing pool'}
try:
    with urlopen(url, timeout=30) as response:
        raw = response.read()
        receipt.update(status=response.status, final_url=response.geturl(),
                       content_type=response.headers.get('content-type'))
    receipt['sha256'] = hashlib.sha256(raw).hexdigest()
    (out / 'MANUAL.html').write_bytes(raw)
    class Links(HTMLParser):
        def __init__(self):
            super().__init__(); self.rows = []
        def handle_starttag(self, tag, attrs):
            values = dict(attrs)
            if tag == 'a' and 'href' in values:
                self.rows.append({'dom_index': len(self.rows)+1, 'raw_href': values['href'],
                                  'resolved_url': urljoin(receipt['final_url'], values['href'])})
    parser = Links(); parser.feed(raw.decode('utf-8', errors='replace'))
    receipt['all_hrefs_in_original_order'] = parser.rows
except Exception as error:
    receipt.update(status='failed', error=type(error).__name__ + ': ' + str(error),
                   first_resume_source=url)
(out / 'receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='all_hrefs_in_original_order'}, ensure_ascii=False))
if receipt['status'] != 200:
    raise SystemExit(1)
PY
```

이후 MANUAL의 판·실제 목차 범주와 토큰 규칙을 봉인한 새 amendment를 만들고 P1–P4를 별도 재표집해야 한다. V3도 최초 문장의 `word cloud`와 원래 fallback을 먼저 고정한다. C2/C4 부족을 채우는 새 보강은 유지보수자 결정/시험 또는 공식 이관 예제에서 시작해 요구·자연6링크·순서·근접 오답을 그룹 계산 전에 고정한다. 사람의 과업별 클릭·확신·채택은 별도 관측으로 남는다.

## 마지막 약점과 후속 조사

| 중요한 불일치·약점 | 영향받는 판단과 근거 URL·행 | 다음 최소 조사·첫 자료 | 결과가 달라지는 조건 |
| --- | --- | --- | --- |
| 자연 표본의 획득 결측과 사전규칙 이탈 | P1–P4 raw HTML·원순서 및 V3 토큰; [MANUAL](https://pandoc.org/MANUAL.html), [V3 원요구](https://github.com/vega/vega-lite/issues/6135); pool.csv2–25행, source-scope/input audit | 같은 MANUAL 원응답 byte를 승인된 수집에서 확보해 SHA/href를 먼저 봉인. V3는 최초요구 명사만으로 새 amendment를 사전 고정; 기존 수치 유지. | 새 자연 풀에 실제 완전 경로가 생기거나 원규칙 V3 fallback이 다른 근거를 포함하면 이름/계약층의 회수·손실 판단이 달라짐. |
| 보강 양성의 부족과 해법 선정 편중 | C4 A2 및 C2 복원 양성의 해석; [Data model](https://docs.python.org/3.11/reference/datamodel.html#async-context-managers), [async-with](https://docs.python.org/3.11/reference/compound_stmts.html#async-with), [ecosystem](https://pandas.pydata.org/pandas-docs/version/2.0/ecosystem.html#visualization); requirements.csv C4행·gold-paths.csv | 새 독립 유지보수/이관 사례의 요구·자연6순서·근접오답을 그룹 계산 전에 봉인. C4를 사후 완화해 채우지 말고 완전 경로와 첫대표에 없는 별개 대안을 실제 확인. | 두 번째 복원 양성과 두 번째 보완 양성이 확보되거나, C4의 의미상 참조를 허용하는 별도 기준이 사전에 채택되면 대조 범위가 확대됨. |
| 키의 구별력과 통제 클릭의 외적 한계 | C=A인 관측8풀·U무변화·Requests HTTP/브라우저 차이; [Requests](https://requests.readthedocs.io/en/stable/user/advanced/#prepared-requests), [PEP](https://peps.python.org/pep-0654/#specification), [NumPy](https://numpy.org/doc/stable/reference/random/compatibility.html); groups.jsonl·clicks.csv | 표시 metadata가 실제 같은 C key로 합쳐지는 독립 풀 하나부터 봉인하고 같은3카드로 사람의 과업별 클릭/확신/채택을 별도로 관측. 첫 자료는 현재 views fixture와 원멤버/절 지도. | C가 실제 병합하면서 다른 구현을 살리거나 필수조건을 가리거나, 실제 독자가 긴 문서·형제 목록을 다르게 이용하면 표시·행동 결론이 달라짐. |
