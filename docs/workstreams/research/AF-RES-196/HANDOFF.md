# AF-RES-196 HANDOFF

**자체 판정 DONE. 독립 검토 미실시.** 고정된 AF-RES-186 인계의 네 실제 문장으로 A·B·C와 두 접근 조건을 검사했다. 거울 없이 세 안 모두 표시 문장·주체·기준일을 4/4 복원했다. 원문 구간을 다시 열고 보관 SHA-256과 대조한 안은 C 4/4였다. 거울이 있으면 A도 4/4 원문을 읽었고 B는 4/4 보관 SHA와 대조했다. 저장량은 네 문장 기준 A 1,192 B, B 2,078 B, C 5,134 B다. [결과표](RESULT.md) · [셀별 판정](matrix.csv) · [비용표](costs.csv)

## 고정 기준과 결과판

- 저장소 `laadkke-arch/agentflow-open`, 작업 `AF-RES-196` 시도 1, 브랜치 `work/research-af-res-196`, 허용 경로 `docs/workstreams/research/AF-RES-196/`. 계획판 `0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6`에서 세 진행표 커밋이 지난 `72cf39aea54e2de2ba78a245593aefdc40205a16`에서 시작했다. [범위](SCOPE.md)
- 직접 의존은 중앙 DONE 및 작성자 DONE으로 기록된 186의 `7042060cd73aad96f70ff290ec6d5f6adf22570b`다. 당시 제출·새 관측 영수증을 이 고정판과 여기서 연결된 고정 원문에서 읽었다. [186 고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/HANDOFF.md)
- **이 인계 직전 결과 SHA `a7ef347e91b4a54427023e6eb2bacb57f5bd208a`**. 이 판에서 RESULT의 첫 표와 마지막 약점 세 건, SELF_CHECK의 직접 자료 수, 골드, matrix 대조행, 재실행 및 전송 기록을 GitHub에서 다시 읽었다. [고정 결과](https://github.com/laadkke-arch/agentflow-open/blob/a7ef347e91b4a54427023e6eb2bacb57f5bd208a/docs/workstreams/research/AF-RES-196/RESULT.md) · [고정 자체점검](https://github.com/laadkke-arch/agentflow-open/blob/a7ef347e91b4a54427023e6eb2bacb57f5bd208a/docs/workstreams/research/AF-RES-196/SELF_CHECK.md)

| 묶음 | 커밋·대표 파일 |
| --- | --- |
| 범위·판정 규칙 | [3f515a6 · SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/3f515a6f26f98e030067b56cbf3b74107b54b064/docs/workstreams/research/AF-RES-196/SCOPE.md) |
| 직접 자료 및 정답표 | [eed4d55 · gold.json](https://github.com/laadkke-arch/agentflow-open/blob/eed4d55bad851d084a5a762f0b81278bbf68cc16/docs/workstreams/research/AF-RES-196/gold.json) · [입력 목록](inputs.json) · [출처 원장](sources.jsonl) · [모집표](frame.csv) |
| 핵심 오프라인 관측 | [d094aa5 · 회차 영수증](https://github.com/laadkke-arch/agentflow-open/blob/d094aa56866584b51b83055e70c60c0236f5f0d3/docs/workstreams/research/AF-RES-196/receipts/core.jsonl) · [A/B/C 묶음 지문](receipts/bundles/package-manifest.json) |
| 의도적 반례와 분야 대조 | [258f786 · 통제 영수증](https://github.com/laadkke-arch/agentflow-open/blob/258f78614227ba89dd116636e96fbad56a23c30c/docs/workstreams/research/AF-RES-196/receipts/controls.jsonl) · [공개 자료 대조](receipts/public-comparison.json) |
| 결과·자체점검 및 전송 한계 | [7fea1a4](https://github.com/laadkke-arch/agentflow-open/commit/7fea1a40007f8a253b884b634bb77880051093f1) · [a7ef347](https://github.com/laadkke-arch/agentflow-open/commit/a7ef347e91b4a54427023e6eb2bacb57f5bd208a) · [새 checkout 재실행](receipts/replay.json) · [PDF 전송 기록](receipts/public-pdf-transport.json) |

## 달성 범위와 남은 확인

- 주 분모 36셀은 실측 24셀과 원래 입력 결측 12셀이다. 실재 증거는 당시 제출 2건과 새 관측 2건이다. N1과 N2는 186의 발행 원장에 명시 미실행 문장이 없어 0/2다. H1 날짜의 시간대와 2020년의 suite·옵션·런타임·원로그는 미확인이다.
- 통제 7회는 별도다. 정확 경로는 정상 복원, basename 대체는 오판, 한 바이트와 기존 해시는 불일치·보류가 됐다. 원문과 해시를 함께 바꾼 대조는 묶음 내부에서 해시 일치를 냈고 독립 기준선과의 불일치가 드러났다. 주소만 둔 사본은 거울이 있을 때 원문을 되찾았다. 증거의 진위 판정에는 보존 묶음과 별도로 신뢰할 근거가 필요하다.
- 실재 고유 원문 36개를 직접 읽었다. 186 원로그·영수증 16개(최소 12), 인계·메타·고정 연결 원문 10개(최소 6), BagIt·의회도서관 3개(최소 2), NIST 로트 원성적서·제품 레코드 2개(최소 2), 보조 원문 5개다. 공개 분야 대조는 연감 p.50과 로트 성적서의 직접 판독으로 동결했다. 현재 상점 상세는 열리지 않았고 원 PDF 세 파일은 Cloud 터널 403으로 바이트 지문이 미확인이다. [공개 판독](receipts/public-freeze.json) · [접근 기록](receipts/public-pdf-transport.json)
- Python 3.12.14, Linux libseccomp2 2.6.0-2로 실행했다. 모든 실측·통제 회차에서 신규 파일과 소켓에 대한 차단 확인이 `EPERM`이었다. 깨끗한 코드 판 `258f78614227ba89dd116636e96fbad56a23c30c`의 새 checkout에서 묶음 12개와 판정·비용·원로그를 바이트 단위로 재대조했다. 묶음 생성, 본 실행, 통제, 공통 클라우드 검사와 재대조는 각각 종료 0이다. 최종 결과판 `a7ef347e91b4a54427023e6eb2bacb57f5bd208a`의 `python3 -B -m workbench.session check docs/workstreams/research/AF-RES-196/session.json --fetch`도 종료 0, `remote_checked`, 범위 밖 0이었다. 공통검사 코드 판과 본 인계의 문서 판은 위 SHA로 식별한다. [실행·재대조 기록](receipts/replay.json)

## 첫 재개 행동

결과 브랜치와 위 결과 SHA를 대조한다. 독립 검토는 `RESULT.md`의 [재실행 절차](RESULT.md#재사용-조건과-비용)로 동일 입력을 준비해 `matrix.csv`와 `costs.csv`를 다시 대조한다. 검토할 때는 C가 동봉한 인용 바이트만 재열람하는 성질, 거울이 있을 때 A도 충분했던 성질, C의 동시 변조 대조를 먼저 확인한다.

NIST 비교의 원바이트까지 확인할 때는 PDF에 접근할 수 있는 환경에서 다음을 실행한다. 이 주소의 원 PDF 전송은 이 실행 환경에서는 Cloud 터널 403으로 끝났다. PDF의 판독 비교와 별도의 확인이다.

```bash
set -euo pipefail
scratch=$(mktemp -d)
base=https://tsapps.nist.gov/srmext/certificates
curl --fail --location -o "$scratch/LL-198.pdf" "$base/archives/2197_LotLL-198_Cert_2024-07-17.pdf"
curl --fail --location -o "$scratch/LL-165.pdf" "$base/archives/2197_LotLL-165_Cert_2017-11-09.pdf"
curl --fail --location -o "$scratch/2026-product-list.pdf" "$base/documents/Annual_SRM_Product_List.pdf"
sha256sum "$scratch/"*.pdf
pdftotext -f 1 -l 1 -layout "$scratch/LL-198.pdf" -
pdftotext -f 1 -l 2 -layout "$scratch/LL-165.pdf" -
pdftotext -f 50 -l 50 -layout "$scratch/2026-product-list.pdf" -
```

색인 제안 — AF-RES-196 / 링크 단절 후 인용 구간의 오프라인 복원과 보존 비용 / 자체 DONE·독립 검토 미실시 / RESULT.md / AF-RES-186 고정판, 24실측·12입력 결측, 묶음 단독 원문 4/4는 C.
