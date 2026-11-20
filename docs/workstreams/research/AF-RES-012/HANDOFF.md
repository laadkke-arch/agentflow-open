# AF-RES-012#1 최종 인계

**REVIEW_READY.** Python 3.12에서 기본 18개 검색 조합과 교차언어 9개를 실행했다. 모델 다운로드는 403이었고, 사전에 정한 TF-IDF+LSA로 M2를 대체했다. 결과는 고정 자료집에서 관측한 검색 품질이다.

## 커밋과 입력

작업 브랜치는 `work/research-af-res-012`다. GitHub의 `chore/workspace-foundation` 최신 `04441f931200fe1bc7e4273422655daa31cf8a06`에서 시작했다. 해당 SHA의 AGENTS.md, STATE.md, DOT_AUTOMATION.md, RESEARCH_WORKFLOW.md, RESEARCH_BRIEF.md, AF-RES-012 진행표 항목과 기존 네 후보 자료를 읽었다.

| 선행 결과 | 고정 SHA와 실제 읽은 범위 |
| --- | --- |
| AF-RES-001 | `4d6208c08f6f2657865ba000d6768f6537e832b6` · HANDOFF, 세 출처 원장, K01–K06 CASES |
| AF-RES-002 | `62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1` · HANDOFF, methods·p1·p2 원장, PROTOCOL, METHODS |
| AF-RES-003 | `b13db3931b4021ff9e1ac6e404590c09526c3087` · HANDOFF, IDENTITY·MECHANISMS·STANDARDS 원장, RESEARCH §5 |
| AF-RES-004 | `2b798c7d2b7355b649691c18de196104ceabb0f0` · HANDOFF, sources, CASES, EXPECTED |

[manifest](manifest.json)에 기준, 계약, 소유 경로, 의존성 네 개를 원격 조회로 고정했다. 사전 판정 `632a844f246935eeb396f3834374b68808263026` 이후 코드 `1596d95af9bcfe3a1079e1137c09edfd7968fdb9`, 초기 실행 `73a4907c9f6465793657d1092f94d6da959be6d9`, 풀링과 별도 검토 `d760616cf3c0e353f6d2659b1e1bf37381af060c`가 차례로 올라갔다. 인계 직전 원격 검사를 한 SHA는 `ae60ba893205613d8106430c9d9defc9a59a5251`이다. **result_commit은 이 HANDOFF.md 한 파일을 추가한 자식 커밋**이다.

## 결론과 적용 한계

| 질문 | 결론 한 줄 | 적용 한계 |
| --- | --- | --- |
| Q1 | D-a의 완성품·부품·원리 recall@10은 각각 .182·.147·.150이었다. | 공식 원문·레지스트리 문구·제목 대체가 섞여 있다. |
| Q2 | D-b의 원리 recall은 .150→.205였다. P1/P2에서 새 원리를 찾았고 P03의 Toyota 사례에서는 하락했다. | 질의별로 15개 개선, 11개 하락, 6개 동일이다. |
| Q3 | D-c는 평균 recall .269→.323과 N .394→.755가 함께 나타났다. | N의 상위 10개 진입 91건과 이탈 13건이 공존한다. |
| Q4 | 한국어 질의의 영어 설명 검색에서 recall .234→.124, 방식마다 74/108개 무신호였다. | 실행된 M2는 LSA이며 한국어 형태소 분석이나 학습된 언어 정렬을 적용하지 않았다. |
| Q5 | 전체 nDCG .343과 부분 .238이었다. 중복 금지처럼 초점이 좁은 K02.1은 전체보다 높았다. | 전체와 발췌의 필수 조건과 정답표가 다르다. |
| Q6 | 실패 24건에서 역할, 구성·부정, 언어별 개념, 출처·판정 연결의 보존 필요성을 확인했다. | 이 필드를 실제 순위에서 사용하는 효과는 후속 실험 대상이다. |
| Q7 | 156개 작성 구간 9분 14초, 최종 실행 3.210초, 깨끗한 가상환경에서 3.574초였다. | 작성 시간에는 읽기가 겹치고 색인 크기는 논리 바이트 기준이다. |
| Q8 | 독립 판정으로 M2/M3의 작은 순서 차가 뒤집혔다. 절반 자료집은 P04의 직접 후보를 잃었다. | 내부 검토자 한 명이고 부분집합에는 새로운 미판정 결과가 남는다. |

가장 강한 근거는 다음 세 가지다.

1. **실행 전후가 분리된 커밋과 일치한 재현 결과.** 156개 자료와 36개 질의에서 초기 판정을 코드보다 먼저 동결했고, 새 Python 환경에서 순위 27개와 결과 CSV를 바이트 단위로 재현했다. [검증 기록](VERIFICATION.json)
2. **같은 질의–항목에서 관측한 부정 반례.** K02.2에서 D-c 추가 뒤 Paperless-ngx가 BM25 한국어 20위 밖에서 1위로 왔다. 그 한계 문장이 K02.2가 금지하는 첫 폴더 파일 삭제를 다룬다. K01.2의 RabbitMQ는 같은 비교에서 RRF 한국어 7위→20위 밖이었다. [실패 원장](ERRORS.md)
3. **풀링과 별도 판정의 분리.** 1,858쌍에 사후 등급을 부여해 관련 135쌍과 근접 오답 22쌍을 추가했다. 별도 검토는 고정 15개에 대해 독립 판정을 제공했다. 두 판정 아래 nDCG 선두가 바뀌어 평균 차이를 방식의 일반적 우위로 해석하기 어렵다. [결과 Q8](RESULTS.md#q8-판정과-자료집이-바뀌면-결론도-바뀌는가) · [검토 범위](qrels/INDEPENDENT_REVIEW.md)

다국어 모델이 의미 표현의 다른 번역을 연결하거나, 주제에 덜 편중된 새로운 질의에서 짧은 공식 문구가 충분하면 이 결론의 적용 범위가 달라진다. 지원 여부를 별도 조건으로 검사하면 D-c가 만든 오탐이 줄면서 발견 이득이 유지될 수도 있다. 둘 다 이번 실행의 관측 밖이다.

## 검증 범위

본문을 연 공식 출처 53개와 실행 방법 원문 8개, 버전이 있는 무료 레지스트리 메타데이터 65개를 기록했다. 공식 원문에 적힌 접근시각은 수집 구간을 닫은 기록 시각이다. 38개 항목에서 D-a는 원장 제목을 사용했다. 전체 한국어와 부분 발췌는 고정 자료와 대조했다. 영문은 이 작업 에이전트가 작성했다. 사람 번역·검토는 미실시다.

단위시험 6개, 초기 순위, 풀링 후 평가와 별도 판정 평가, 가상환경 재실행, 저장 경로 검사를 마쳤다. 공통 cloud check와 명시적인 manifest 검사 모두 종료 0이다. 자동 세션 검사는 `no_active_sessions`였고 작업 폴더의 manifest는 별도로 `--fetch` 검사했다. 관리형 Codex 작업공간에서 GitHub 읽기·로컬 실행·푸시를 관측했다. 별도 계정 UI의 환경 발행이나 다른 새 웹 Pro 세션 연결은 확인 범위 밖이다. [자기 점검](SELF_CHECK.md) · [정확한 실행 정보](VERIFICATION.json)

공통 색인 제안은 아래 한 행이다.

| ID | 질문 | 상태 | 파일 | 핵심 의존과 적용 범위 |
| --- | --- | --- | --- | --- |
| AF-RES-012 | 링크와 짧은 설명으로 제품·부품·원리를 얼마나 찾는가 | REVIEW_READY | `docs/workstreams/research/AF-RES-012/RESULTS.md` | AF-RES-001~004 고정 입력, 소형 KO/EN 비교, M2 LSA 대체, 기준 스택은 미결정 |

## 다음 첫 행동

**이 파일의 원격 blob과 최종 브랜치 HEAD를 확인하고 [RESULTS.md](RESULTS.md)의 Q3·Q8부터 검토한다.** 다음 세션에서 보존할 입력은 최종 SHA의 corpus, queries, seed qrels, pool과 별도 qrels다. 풀의 판정과 순위는 각각 고정 표에 있다.

```sh
git fetch origin refs/heads/work/research-af-res-012:refs/remotes/origin/work/research-af-res-012
git rev-parse origin/work/research-af-res-012
git log -1 --format=%H origin/work/research-af-res-012 -- docs/workstreams/research/AF-RES-012/HANDOFF.md
git show origin/work/research-af-res-012:docs/workstreams/research/AF-RES-012/HANDOFF.md
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-012/manifest.json --fetch
```

벤치마크 입력이 있는 checkout의 작업 폴더에서 실행한다. `python -m src.run --all`은 실행 산출물을 다시 쓰고, 시간이 달라지는 색인 비용 파일도 갱신한다.

```sh
cd docs/workstreams/research/AF-RES-012
af012_venv=$(mktemp -d)
uv venv --python 3.12 "$af012_venv"
uv pip install --python "$af012_venv/bin/python" -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 "$af012_venv/bin/python" -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 "$af012_venv/bin/python" -m src.run --all
```

**다운로드 차단으로 남은 검사.** 허용된 네트워크의 별도 Python 3.12 환경에서 동일 고정 입력의 신경망 결과를 얻는 명령이다. 현재 관리형 작업공간의 가중치와 config URL 요청은 각각 HTTP 또는 CONNECT 403을 반환했다. 재개의 첫 기술 행동은 아래 첫 요청의 응답을 확인하는 것이다. 성공하면 같은 156개·36개·235쌍의 입력을 별도 폴더로 복사해 다시 실행하고, 신경망 순위에서 생긴 새 풀을 판정한다. LSA 풀과 신경망 풀이 달라질 수 있다.

```sh
curl --head --fail --silent --show-error --max-time 20 \
  https://huggingface.co/intfloat/multilingual-e5-small/resolve/0a1c1d9ee03224db176563ffcfbc3bbc38f35266/model.safetensors
uv pip install --python "$af012_venv/bin/python" --index-url https://download.pytorch.org/whl/cpu 'torch==2.7.1+cpu'
uv pip install --python "$af012_venv/bin/python" 'sentence-transformers==4.1.0' 'transformers==4.52.4'
af012_e5_inputs=$(mktemp -d)
cp -R corpus queries qrels sources.json "$af012_e5_inputs/"
PYTHONDONTWRITEBYTECODE=1 "$af012_venv/bin/python" -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 "$af012_venv/bin/python" -m src.run --all --m2 e5 --root "$af012_e5_inputs"
```

이 절의 임베딩 명령은 후속 입력이다. 이번 결과에는 E5의 가중치나 점수가 없다.
