# AF-RES-135 최종 인계

**PARTIAL.** 두 소프트웨어 축의 정식판·신호·실행과 비용은 검산했다. 지도는 소스 64판·63쌍과 AF-RES-131의 브라우저 4판을 구별했고, d3-scale은 27판·26쌍에서 두 출력 전환을 확인했다. 두 깨끗한 경로의 각 79/79 실행은 동일했다. C는 d3-scale 3.2.4의 null 변경 1쌍을 놓쳤고 D는 변화 2쌍을 요청하면서 전체 26쌍 중 25쌍을 요청했다. 적격 고유 원전은 32건이다. Q7의 Vienna 인쇄면 2개와 실재 재스캔 쌍, WSDOT Thanksgiving 날짜별 화면은 미확인이다. [결과](RESULT.md) · [대조와 비용](decisions.csv) · [도메인 증거](evidence/cross-domain.md)

## 입력·결과·검사

- 기준 계획 `42260ca230e028e1303667be943b861a1d5953e4`, 원격 작업 브랜치의 시작 `5840e5fe1221188b12895b0e61808856a61b6464`, manifest 시작 검사 통합 `67eb3c65404bf70de554bee6eb4c126344a3cd4a`. 기존 로컬 `work` ref의 이름 충돌 때문에 로컬 `codex/research-af-res-135`에서 지정 원격 `work/research-af-res-135`에 발행했다. 단일 소유 경로만 편집했다. [manifest](manifest.json)
- 의존 AF-RES-131 인계 `5cf6899ec26ec40045a62b4352076477793bd45a`, 고정 결과 `de62ead16f71041f0a1c3cc37c651a0de3d760a5`다. 131의 배포·예측·브라우저 원장, release history, 수용 기록을 읽었다. 관련 raw 32건은 해시와 고정 URL로 참조한다. 기존 지도·QGIS·Audacity의 새 실행은 0회다. [고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/5cf6899ec26ec40045a62b4352076477793bd45a/docs/workstreams/research/AF-RES-131/HANDOFF.md) · [고정 결과](https://github.com/laadkke-arch/agentflow-open/blob/de62ead16f71041f0a1c3cc37c651a0de3d760a5/docs/workstreams/research/AF-RES-131/RESULT.md)
- 결과 겸 검사 SHA `a6a52f73843d8340024cdefb9c6cba7b0b73621c`. 검사 시 통합 `a5fb54e09f0819cd4806397af36145cd9333ca51`. 명시 `workbench.session check … --fetch`와 생성기에서 독립한 CSV/JSONL 재집계 각각 종료 0, stderr 빈 값. 33개 변경 경로는 모두 소유 폴더에 있었고 세션 검사의 32개는 manifest를 제외한 수다. 검사는 같은 작업자가 실행했고 별도 모델 대화 판독은 미실시다. [검사 명령·stdout·stderr·종료코드](evidence/acceptance.json)

## 묶음

| 묶음 | 경로와 원격 재열람 SHA | 완료 근거 |
| --- | --- | --- |
| ① 표본·규칙·입력 봉인 | [912a1122a7b4b0e20f03e9232ef0959fb5468068 · SCOPE](https://github.com/laadkke-arch/agentflow-open/blob/912a1122a7b4b0e20f03e9232ef0959fb5468068/docs/workstreams/research/AF-RES-135/SCOPE.md) | manifest, 공개 후보, 입력 및 질의 순서 |
| ② 배포·기능 절 | [9923501d3823d56f79047c79eaccf27954fe40d9 · releases](https://github.com/laadkke-arch/agentflow-open/blob/9923501d3823d56f79047c79eaccf27954fe40d9/docs/workstreams/research/AF-RES-135/releases.csv) | 타르 91개 integrity 확인, 고정 절 91개 |
| ③ 신호 판정 봉인 | [1db7e6785e6ade12d598766ba740a2d4886ebf57 · signals](https://github.com/laadkke-arch/agentflow-open/blob/1db7e6785e6ade12d598766ba740a2d4886ebf57/docs/workstreams/research/AF-RES-135/signals.csv) | 두 순서의 A–D와 dependency lock을 첫 실행 전에 보존 |
| ④ 실행·깨끗한 재생 | [860252f7500a7769baaf52a164ecf71134dbfe85 · replay 영수증](https://github.com/laadkke-arch/agentflow-open/blob/860252f7500a7769baaf52a164ecf71134dbfe85/docs/workstreams/research/AF-RES-135/evidence/replay.json) | 27판, 공유 의존 대응 26쌍, raw만으로 출력 비교 |
| ⑤ 대조·비용·타 분야 | [a88d033aafd74fe4fb2735d32c11e11de58790e3 · cross-domain](https://github.com/laadkke-arch/agentflow-open/blob/a88d033aafd74fe4fb2735d32c11e11de58790e3/docs/workstreams/research/AF-RES-135/evidence/cross-domain.md) | 판정 11,280행, 질의 840행, 출처 48건 및 Q7 접근 결과 |
| ⑥ 결과와 검산 | [a6a52f73843d8340024cdefb9c6cba7b0b73621c · RESULT](https://github.com/laadkke-arch/agentflow-open/blob/a6a52f73843d8340024cdefb9c6cba7b0b73621c/docs/workstreams/research/AF-RES-135/RESULT.md) · [aa85a3a22c02070550bf64d590b6a6e9a58902d4 · 검사](https://github.com/laadkke-arch/agentflow-open/blob/aa85a3a22c02070550bf64d590b6a6e9a58902d4/docs/workstreams/research/AF-RES-135/evidence/acceptance.json) | 세 표, Q1–Q7, 고정판에서 검산 종료 0 |
| ⑦ 최종 인계 | 이 파일 하나를 마지막 별도 커밋으로 발행 | 소유 경로와 끝 표를 재검사 |

등록소 무결성 검사와 파일 취득을 한 공통 코드에 두고 신호·실행에서 재사용했다. OpenLayers의 기존 판·계약·raw를 이어 썼고 조건 생략의 정적 줄을 추가 판독했다. d3-scale에서는 같은 probe를 UMD의 require와 ESM의 import에 사용하고, 공유 직접 의존을 제어한 잠금을 별도 저장했다. 판정 결합 전에 raw 전용 출력 비교를 커밋했다. 저장소 세션 검사와 별도 원장 감사로 scope와 재집계를 확인했다. [재생 코드](replay/run.py) · [문의 재생](replay/analyze.py) · [검산 코드](replay/audit.py)

## 첫 재개 행동

Vienna 원면 두 건을 내려받아 첫 페이지의 하단 좌우 범례와 조사·인쇄 식자를 열고, 동일 도엽의 Lake Anne 주변을 비교한다. 이 환경에서 USGS GeoPDF의 웹 파서 반환과 Chromium 연결이 실패했다. PDF 원문에 접근 가능한 경로에서 아래의 실제 URI를 사용한다. 파일 획득 후에는 두 파일의 SHA-256, 스캔 식별자, PDF에 든 XML, 해당 페이지와 좌표를 기록한다. 같은 종이의 기관 재스캔은 topoView의 판별 메타데이터나 보존 이력의 서로 다른 취득 날짜부터 확인한다. [접근 영수증과 비교 대상](evidence/cross-domain.md)

```sh
map_dir=$(mktemp -d /tmp/af135-vienna.XXXXXX)
map_base='https://prd-tnm.s3.amazonaws.com/StagedProducts/Maps/HistoricalTopo/PDF/VA/24000'
curl -fSL "$map_base/VA_Vienna_187062_1966_24000_geo.pdf" -o "$map_dir/187062.pdf"
curl -fSL "$map_base/VA_Vienna_187064_1973_24000_geo.pdf" -o "$map_dir/187064.pdf"
sha256sum "$map_dir/187062.pdf" "$map_dir/187064.pdf"
pdfinfo "$map_dir/187062.pdf"
pdfinfo "$map_dir/187064.pdf"
pdfdetach -list "$map_dir/187062.pdf"
pdfdetach -list "$map_dir/187064.pdf"
pdftoppm -f 1 -l 1 -r 170 -png "$map_dir/187062.pdf" "$map_dir/187062"
pdftoppm -f 1 -l 1 -r 170 -png "$map_dir/187064.pdf" "$map_dir/187064"
```

WSDOT 날짜별 화면에는 `2026-11-26`, Seattle 출발, Bainbridge Island 도착을 선택한다. 게시 시점이 지나 일일 화면이 닫혔으면 운영기관의 날짜별 보존본 또는 승인된 API에서 매개변수 `2026-11-26/7/3`을 사용한다. 계절/공지로 확인한 06:10과 날짜별 실제 출력, 운항 기록을 따로 남긴다. [날짜 선택](https://wsdot.com/FERRIES/SCHEDULE/schedulebydate.aspx) · [API 계약](https://www.wsdot.wa.gov/ferries/api/schedule/rest/help)

소프트웨어의 반복 검증 진입점은 다음과 같다. 입력과 의존은 고정돼 있고 각 실행 디렉터리는 새 경로다. 원격 AF-RES-131 커밋 객체가 있어야 마지막 합치기와 감사에서 32개 raw 링크를 검증한다. 결과를 새로 쓸 경우 지정된 작업 경로만 사용한다. [설치 핀](replay/locks.json) · [실행 영수증](evidence/replay.json)

```sh
root=docs/workstreams/research/AF-RES-135
scratch=$(mktemp -d /tmp/af135-replay.XXXXXX)
git fetch origin work/research-af-res-131
python -B "$root/replay/run.py" run --folder "$scratch/A" --cache "$scratch/cache-A" --output "$scratch/A.jsonl"
python -B "$root/replay/run.py" run --folder "$scratch/B" --cache "$scratch/cache-B" --output "$scratch/B.jsonl"
python -B "$root/replay/run.py" combine --first "$scratch/A.jsonl" --second "$scratch/B.jsonl"
python -B "$root/replay/audit.py"
python -B -m workbench.session check "$root/manifest.json" --fetch
```

색인 제안 — AF-RES-135 · 기능 링크의 배포별 재확인 신호, Translate와 scaleLinear의 변화·재생·비용 · PARTIAL (Q7 원면 및 직접 서비스일) · 선행 AF-RES-131. [결과](RESULT.md)

| 중요한 불일치·약점 | 다음 조사·원문 또는 실험 | 판단을 바꿀 관측 |
| --- | --- | --- |
| 3.2.4는 README를 그대로 두고 null 출력을 바꿨고 D는 25/26 공개쌍에 경보했다. | [3.2.4 공지](https://github.com/d3/d3-scale/releases/tag/v3.2.4) 같은 배포 노트와 좁힌 위임 지문을 다음 기능에서 사전 봉인한다. | 놓침을 줄이며 새 기능의 실제 실행과 읽은 바이트도 줄면 채택 근거가 된다. |
| OpenLayers의 브라우저 양끝 비교는 1/63쌍이다. | [고정 브라우저 입력](runs.jsonl)과 동일 조건에서 필요할 때 다중 멤버의 geometry·다른 renderer의 hit를 따로 측정한다. | 같은 목록 또는 하나의 거부에서도 보존된 값이 달라지면 반환할 근거 범위를 좁힌다. |
| Vienna 두 원면 0/2와 기관 재스캔 0/1, 휴일 직접 날짜표 1/2가 남았다. | [고정 지도 ID·공휴일 입력](evidence/cross-domain.md)부터 열어 범례와 두 날짜의 동일 터미널 셀을 대조한다. | 재스캔의 식자가 동일하거나 날짜별 셀이 휴일표와 불일치하면 해당 분야의 갱신 판단을 조정한다. |
