REVIEW_READY

# AF-RES-024 인계

2021년 말의 CPython과 Node.js 공식 문서에서 32개씩 뽑은 64개 이유를 2025년 말까지 16분기 재생했다. 1,024개 이유×분기 중 992개를 채점했고 초기 오류 16개 셀과 판정 보류 16개 셀을 보존했다. 확정된 변경은 11개 이유, 10개 사건군이다. [보고서](RESULT.md) · [수용 근거](evidence/acceptance-evidence.json)

| 분기당 상한 20 | 확인 이유와 사건군 | 상태 TP·FP·FN·TN | 끝까지 놓친 이유 | 요청과 원문 |
| --- | --- | --- | --- | --- |
| N · 재검토 없음 | 0/11 · 0/10 | 0·0·95·897 | 11 | 0 · 0 |
| D · 정기 직접 확인 | 11/11 · 10/10 | 86·0·9·897 | 0 | 320 · 319 |
| S · 신호 뒤 원문 확인 | 8/11 · 8/10 | 54·0·41·897 | 3 | 320 · 211 |
| O · 주소를 받은 상한 | 11/11 · 10/10 | 95·0·0·897 | 0 | 8 · 8 |

S 선별 925건 중 유지 상태 827건과 보류 12건을 확인했다. D의 시행 후 확인 중앙값은 90일이고 최대 348일이다. S는 확인된 8건에서 중앙 90일, 최대 1,019일이다. S가 덜 연 본문은 108개이고 더 받은 HTTP 몸체는 5,672,462B다. 예산 40에서는 D/S 모두 11/11이고 S가 원문을 107개 적게 읽는다. 정책 순위는 놓침과 판독의 비용 단가에 따라 바뀐다. [지연](discoveries.csv) · [비용](costs.csv) · [환경별 계산](decisions.csv)

## 고정 입력과 저장 위치

- 작업 ID와 시도는 AF-RES-024#1이다. 저장소는 `laadkke-arch/agentflow-open`, 작업 브랜치는 `work/research-af-res-024`다. 시작 통합 커밋은 `c3a0db2847bfb52731e97041617a6fa8113b93dd`, 계획 기준판은 `b507fbcab09724a77270e658355f4b661cc35f02`다. [범위](SCOPE.md) · [작업 계약](manifest.json)
- AF-RES-019의 `034ba6e2360301be23c49c66cf42af5c36f9e534`에서 인계, RESULT Q2–Q7, 매칭, 혼동, 주기와 015 연결을 읽었다. 019의 주소가 주어진 재생은 결과의 범위를 비교할 때만 사용했다. [입력판](https://github.com/laadkke-arch/agentflow-open/tree/034ba6e2360301be23c49c66cf42af5c36f9e534/docs/workstreams/research/AF-RES-019)
- ① 사전 기준 `da455ddbefb5310de8a8ec3492dfe1fcad9c78a0`, ② 미래 자료 이전 표본 잠금 `485044097a51954264cbd9772ce50578e86ac82f`, ③ 마지막 관측 `b4dd9f85e40d5bb49eda4e984418c40e1a9f6a39`, ④ 검증한 결과 `1606df16ed0ffe5d60bd19064f5c63f9d6eb17c7`, 자체 점검과 수용 증거 `87914901356bd760fb42dc8b2a4d1e51bb50372d`를 모두 원격에서 확인했다. 이 파일을 담은 마지막 커밋은 브랜치의 원격 HEAD에서 확인한다. [진행 기록](PROGRESS.md) · [원격 브랜치](https://github.com/laadkke-arch/agentflow-open/tree/work/research-af-res-024/docs/workstreams/research/AF-RES-024)
- 작업·검사는 관리형 Codex Cloud Linux의 `/workspace/af-res-024` 및 새 원격 체크아웃에서 수행했다. 모델은 GPT-6 기반 Codex로 식별됐다. 세부 모델·추론 강도 표기는 미확인이다. Python 3.12.14와 Git 2.52.0을 썼다. [검증 영수증](evidence/verification.json)

## 검증과 재현

91개 고유 원문에 T0 판·정확한 절, 나중 판의 릴리스 또는 공식 구현·테스트, 두 다른 분야의 원문이 들어 있다. 동일 공지와 운영 입력 밖 자료를 구별했다. 최초 수집 한 번과 로컬 캐시 재사용 두 번의 스냅샷은 일치했다. 원격 결과 커밋에서 재생 출력 6개의 sha256과 바이트 일치, 작업 계약 원격 검사, 공통 cloud_check를 확인했다. [원문 원장](sources.json) · [자체 점검](SELF_CHECK.md) · [검사 해시](evidence/verification.json)

```sh
p=docs/workstreams/research/AF-RES-024
out=$(mktemp -d)
python -B "$p/verify.py"
python -B "$p/replay.py" --out "$out"
for name in timeline.jsonl visits.csv costs.csv metrics.csv discoveries.csv decisions.csv
do
  cmp "$p/$name" "$out/$name"
done
python -m workbench.session check "$p/manifest.json" --fetch
python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

새 수집을 재현할 최소 입력은 cohort.csv와 releases.csv, 두 공개 Git 호스트, 빈 캐시 폴더다. 아래의 캐시를 세 실행에서 같이 사용한다. 예전 스냅샷을 새 영수증으로 덮지 않기 위해 새 출력 폴더에서 실행한다. 재수집의 팩과 벽시간은 달라질 수 있다.

```sh
cache=$(mktemp -d)
output=$(mktemp -d)
for phase in cold reuse1 reuse2
do
  python -B "$p/acquire.py" --run "$phase" --cache "$cache" --out "$output/$phase" \
    --quarters T0 2022Q1 2022Q2 2022Q3 2022Q4 2023Q1 2023Q2 2023Q3 2023Q4 \
    2024Q1 2024Q2 2024Q3 2024Q4 2025Q1 2025Q2 2025Q3 2025Q4
done
```

Crossref REST와 상태 다이얼로그의 연결은 미확인이다. 필요한 환경에서 아래 DOI와 발행사 정정 본문을 비교하면 등록 관계를 확인할 수 있다. 이번 코호트의 정답과 점수에는 들어가지 않는다. [PLOS 정정](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3003792)

```sh
curl -fsS 'https://api.crossref.org/works/10.1371/journal.pbio.3003792'
curl -fsS 'https://crossmark.crossref.org/dialog/?doi=10.1371%2Fjournal.pbio.3003726&domain=journals.plos.org'
```

## 색인 제안과 다음 첫 행동

진행 담당의 색인에 AF-RES-024, `REVIEW_READY`, RESULT.md, 019 의존 SHA, 64이유·16분기와 D 11/11·S 8/11을 등록할 수 있다. 색인과 진행표 검토에는 마지막 원격 HEAD의 이 인계와 수용 근거를 먼저 사용한다. 다음 연구의 첫 행동은 2023Q4와 2024Q4의 공개판 입력을 복사하고, 이유·시작 주소·공개판 색인만 보는 별도 판독자의 큐를 만든 뒤 D/S의 실제 판독 시간과 예산 중단점을 비교하는 것이다. [원격 수용 근거](https://github.com/laadkke-arch/agentflow-open/blob/87914901356bd760fb42dc8b2a4d1e51bb50372d/docs/workstreams/research/AF-RES-024/evidence/acceptance-evidence.json)

## 가장 중요한 약점과 후속 질문

1. 결과는 두 프로젝트의 몇 출시 파동에 집중된다. 결과를 모르는 다른 공개 프로젝트와 장기 지원판을 추가하고 출시 단위로 재생하면 D/S의 차이가 유지되는가?
2. 매뉴얼이 유지된 897셀의 모든 동작을 실행하지 않았다. 같은 이름이 살아도 무너질 사용을 고정판의 공식 테스트와 대비하면, 문서 절 변화가 없는 추가 사건이 드러나는가?
3. 수집 및 로컬 재사용 비용은 실측했고 독립 편집자의 판독 시간과 역사적 네트워크 비용은 미확인이다. 첫 방문과 재방문의 사람 시간까지 재면 20회 상한에서 판독·누락 비용의 역전 경계가 움직이는가?
