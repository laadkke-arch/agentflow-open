## 표 1

| 문장·주체·기준일 | 원자료 고정 SHA·경로 | 원문 위치·증거 URL | 실제 입력 유무 | 미확인 |
| --- | --- | --- | --- | --- |
| H1 · 시험 주체 https://github.com/piprate/json-gold의 2020-04-06T17:15:22.676634 EARL 단언은 https://w3c.github.io/json-ld-api/tests/compact-manifest#t0001 결과를 passed로 보고했다.<br>주체 https://github.com/piprate/json-gold · 2020-04-06T17:15:22.676634 | `8811ba2a3bcae883ac91efacffb70ef08d84e92f`<br>`reports/jsonld-gold-earl.ttl` | L31–L42 · [E01 원문](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-gold-earl.ttl#L31-L42) · [186의 연결](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/comparison.csv#L30) | 있음 | Gold 날짜의 시간대, 당시 suite·옵션·실행 원로그 |
| H2 · 시험 주체 https://github.com/digitalbazaar/jsonld.js의 2020-04-15T21:59:04.000Z EARL 단언은 https://w3c.github.io/json-ld-api/tests/compact-manifest#t0001 결과를 passed로 보고했다.<br>주체 https://github.com/digitalbazaar/jsonld.js · 2020-04-15T21:59:04.000Z | `8811ba2a3bcae883ac91efacffb70ef08d84e92f`<br>`reports/jsonld-js-earl.ttl` | L29–L40 · [E02 원문](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-js-earl.ttl#L29-L40) · [186의 연결](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/comparison.csv#L31) | 있음 | 당시 suite·옵션·실행 원로그 |
| O1 · gold는 2026-11-24T19:33:57.106042Z에 gold-T01-r1에서 []를 반환했다.<br>주체 gold · 2026-11-24T19:33:57.106042Z | `7042060cd73aad96f70ff290ec6d5f6adf22570b`<br>`docs/workstreams/research/AF-RES-186/receipts/gold-T01-r1/receipt.json` | L2–L6, L52, L74–L77 · [R01 원문](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/gold-T01-r1/receipt.json) · [186의 연결](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/runs.csv#L2) | 있음 | 별도 환경에서의 재현 |
| O2 · js는 2026-11-24T19:33:57.136989Z에 js-T01-r1에서 []를 반환했다.<br>주체 js · 2026-11-24T19:33:57.136989Z | `7042060cd73aad96f70ff290ec6d5f6adf22570b`<br>`docs/workstreams/research/AF-RES-186/receipts/js-T01-r1/receipt.json` | L2–L6, L55, L81–L84 · [R07 원문](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/js-T01-r1/receipt.json) · [186의 연결](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/runs.csv#L12) | 있음 | 별도 환경에서의 재현 |
| N1 · 미실행 자리 | — | 미실행 인용 없음 · [M05의 40행](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/runs.csv) | 입력 결측 | 해당하는 미실행 문장·주체·기준일·원문 |
| N2 · 미실행 자리 | — | 미실행 인용 없음 · [M05의 40행](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/runs.csv) | 입력 결측 | 해당하는 미실행 문장·주체·기준일·원문 |

## 표 2

| 저장안·가용성·문장 | 필드 복원 | 원문 재열람·해시 대조 | 오판·보류 | 로그·해시 | 바이트·열람 수 |
| --- | --- | --- | --- | --- | --- |
| A · 거울 · [H1](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-gold-earl.ttl#L31-L42) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 거울 원문 일치 · 저장 해시 없음 | 0 · 0 | [영수증](receipts/core.jsonl#L1) · `f3b375d046c7` | 334 B · 묶음 1 / 원파일 1 / 동봉 구간 0 / 실패 0 |
| A · 묶음만 · [H1](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-gold-earl.ttl#L31-L42) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 원문 없음 · 미대조 | 0 · 원문 보류 | [영수증](receipts/core.jsonl#L2) · `6c76658ed5ec` | 334 B · 묶음 1 / 원파일 0 / 동봉 구간 0 / 실패 1 |
| B · 거울 · [H1](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-gold-earl.ttl#L31-L42) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 거울 원문 일치 · 재계산 일치 | 0 · 0 | [영수증](receipts/core.jsonl#L3) · `c5c8f277799c` | 539 B · 묶음 1 / 원파일 1 / 동봉 구간 0 / 실패 0 |
| B · 묶음만 · [H1](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-gold-earl.ttl#L31-L42) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 원문 없음 · 미대조 | 0 · 원문 보류 | [영수증](receipts/core.jsonl#L4) · `17621f9036dc` | 539 B · 묶음 1 / 원파일 0 / 동봉 구간 0 / 실패 1 |
| C · 거울 · [H1](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-gold-earl.ttl#L31-L42) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 동봉 원문 구간 일치 · 재계산 일치 | 0 · 0 | [영수증](receipts/core.jsonl#L5) · `15bce9ff2da1` | 1460 B · 묶음 1 / 원파일 0 / 동봉 구간 1 / 실패 0 |
| C · 묶음만 · [H1](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-gold-earl.ttl#L31-L42) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 동봉 원문 구간 일치 · 재계산 일치 | 0 · 0 | [영수증](receipts/core.jsonl#L6) · `3c9731da981b` | 1460 B · 묶음 1 / 원파일 0 / 동봉 구간 1 / 실패 0 |
| A · 거울 · [H2](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-js-earl.ttl#L29-L40) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 거울 원문 일치 · 저장 해시 없음 | 0 · 0 | [영수증](receipts/core.jsonl#L7) · `a7269769d3d4` | 336 B · 묶음 1 / 원파일 1 / 동봉 구간 0 / 실패 0 |
| A · 묶음만 · [H2](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-js-earl.ttl#L29-L40) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 원문 없음 · 미대조 | 0 · 원문 보류 | [영수증](receipts/core.jsonl#L8) · `e6d0a10ade73` | 336 B · 묶음 1 / 원파일 0 / 동봉 구간 0 / 실패 1 |
| B · 거울 · [H2](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-js-earl.ttl#L29-L40) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 거울 원문 일치 · 재계산 일치 | 0 · 0 | [영수증](receipts/core.jsonl#L9) · `92c96982d7a8` | 539 B · 묶음 1 / 원파일 1 / 동봉 구간 0 / 실패 0 |
| B · 묶음만 · [H2](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-js-earl.ttl#L29-L40) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 원문 없음 · 미대조 | 0 · 원문 보류 | [영수증](receipts/core.jsonl#L10) · `710c922809a2` | 539 B · 묶음 1 / 원파일 0 / 동봉 구간 0 / 실패 1 |
| C · 거울 · [H2](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-js-earl.ttl#L29-L40) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 동봉 원문 구간 일치 · 재계산 일치 | 0 · 0 | [영수증](receipts/core.jsonl#L11) · `ccd9b2b76558` | 1464 B · 묶음 1 / 원파일 0 / 동봉 구간 1 / 실패 0 |
| C · 묶음만 · [H2](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-js-earl.ttl#L29-L40) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 동봉 원문 구간 일치 · 재계산 일치 | 0 · 0 | [영수증](receipts/core.jsonl#L12) · `fcba47d15055` | 1464 B · 묶음 1 / 원파일 0 / 동봉 구간 1 / 실패 0 |
| A · 거울 · [O1](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/gold-T01-r1/receipt.json) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 거울 원문 일치 · 저장 해시 없음 | 0 · 0 | [영수증](receipts/core.jsonl#L13) · `9e993afe5a36` | 264 B · 묶음 1 / 원파일 1 / 동봉 구간 0 / 실패 0 |
| A · 묶음만 · [O1](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/gold-T01-r1/receipt.json) | 문장·주체·기준일·파일 일치, 인용 구간 미확인 | 원문 없음 · 미대조 | 0 · 원문 보류 | [영수증](receipts/core.jsonl#L14) · `825815b42ecf` | 264 B · 묶음 1 / 원파일 0 / 동봉 구간 0 / 실패 1 |
| B · 거울 · [O1](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/gold-T01-r1/receipt.json) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 거울 원문 일치 · 재계산 일치 | 0 · 0 | [영수증](receipts/core.jsonl#L15) · `25a95db5fc94` | 504 B · 묶음 1 / 원파일 1 / 동봉 구간 0 / 실패 0 |
| B · 묶음만 · [O1](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/gold-T01-r1/receipt.json) | 문장·주체·기준일·파일 일치, 인용 구간 미확인 | 원문 없음 · 미대조 | 0 · 원문 보류 | [영수증](receipts/core.jsonl#L16) · `4dc8c121b090` | 504 B · 묶음 1 / 원파일 0 / 동봉 구간 0 / 실패 1 |
| C · 거울 · [O1](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/gold-T01-r1/receipt.json) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 동봉 원문 구간 일치 · 재계산 일치 | 0 · 0 | [영수증](receipts/core.jsonl#L17) · `6d85405415bf` | 1127 B · 묶음 1 / 원파일 0 / 동봉 구간 1 / 실패 0 |
| C · 묶음만 · [O1](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/gold-T01-r1/receipt.json) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 동봉 원문 구간 일치 · 재계산 일치 | 0 · 0 | [영수증](receipts/core.jsonl#L18) · `beecb5816a1f` | 1127 B · 묶음 1 / 원파일 0 / 동봉 구간 1 / 실패 0 |
| A · 거울 · [O2](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/js-T01-r1/receipt.json) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 거울 원문 일치 · 저장 해시 없음 | 0 · 0 | [영수증](receipts/core.jsonl#L19) · `eac27ae51b3a` | 258 B · 묶음 1 / 원파일 1 / 동봉 구간 0 / 실패 0 |
| A · 묶음만 · [O2](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/js-T01-r1/receipt.json) | 문장·주체·기준일·파일 일치, 인용 구간 미확인 | 원문 없음 · 미대조 | 0 · 원문 보류 | [영수증](receipts/core.jsonl#L20) · `b89f21a04705` | 258 B · 묶음 1 / 원파일 0 / 동봉 구간 0 / 실패 1 |
| B · 거울 · [O2](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/js-T01-r1/receipt.json) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 거울 원문 일치 · 재계산 일치 | 0 · 0 | [영수증](receipts/core.jsonl#L21) · `b7e8092b9276` | 496 B · 묶음 1 / 원파일 1 / 동봉 구간 0 / 실패 0 |
| B · 묶음만 · [O2](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/js-T01-r1/receipt.json) | 문장·주체·기준일·파일 일치, 인용 구간 미확인 | 원문 없음 · 미대조 | 0 · 원문 보류 | [영수증](receipts/core.jsonl#L22) · `0abe62f3d693` | 496 B · 묶음 1 / 원파일 0 / 동봉 구간 0 / 실패 1 |
| C · 거울 · [O2](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/js-T01-r1/receipt.json) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 동봉 원문 구간 일치 · 재계산 일치 | 0 · 0 | [영수증](receipts/core.jsonl#L23) · `8fffc884fadf` | 1083 B · 묶음 1 / 원파일 0 / 동봉 구간 1 / 실패 0 |
| C · 묶음만 · [O2](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/js-T01-r1/receipt.json) | 문장·주체·기준일·파일 일치, 인용 위치 일치 | 동봉 원문 구간 일치 · 재계산 일치 | 0 · 0 | [영수증](receipts/core.jsonl#L24) · `5fa24f1a1d7d` | 1083 B · 묶음 1 / 원파일 0 / 동봉 구간 1 / 실패 0 |
| A · 거울 · N1 | 입력 결측 | 미측정 | 판정 제외 | — | — |
| A · 묶음만 · N1 | 입력 결측 | 미측정 | 판정 제외 | — | — |
| B · 거울 · N1 | 입력 결측 | 미측정 | 판정 제외 | — | — |
| B · 묶음만 · N1 | 입력 결측 | 미측정 | 판정 제외 | — | — |
| C · 거울 · N1 | 입력 결측 | 미측정 | 판정 제외 | — | — |
| C · 묶음만 · N1 | 입력 결측 | 미측정 | 판정 제외 | — | — |
| A · 거울 · N2 | 입력 결측 | 미측정 | 판정 제외 | — | — |
| A · 묶음만 · N2 | 입력 결측 | 미측정 | 판정 제외 | — | — |
| B · 거울 · N2 | 입력 결측 | 미측정 | 판정 제외 | — | — |
| B · 묶음만 · N2 | 입력 결측 | 미측정 | 판정 제외 | — | — |
| C · 거울 · N2 | 입력 결측 | 미측정 | 판정 제외 | — | — |
| C · 묶음만 · N2 | 입력 결측 | 미측정 | 판정 제외 | — | — |

## 표 3

| 사용 목적 | 충분했던 최소안 | 더 필요한 원자료 | 반례 | 원판에서 확인할 다음 행동 |
| --- | --- | --- | --- | --- |
| 운영자가 당시 화면의 문장과 문장에 적힌 주체·기준일을 복원 | A · 두 조건 모두 4/4 | 화면에서 빠진 주체나 날짜가 필요하면 해당 단언·영수증 | H1 주소만 남기면 거울 없이 주체·기준일도 복원하지 못했다. [주소 대조](receipts/controls.jsonl#L7) | 표시 문장에 필요한 필드가 실제로 포함되는지 확인한다. [골드](gold.json) |
| 독자가 접근 가능한 정확판의 인용을 읽음 | A · 거울 4/4 | 접근 가능한 정확판 파일과 올바른 경로·구간 | C가 필요한 환경에서도 고정 URL이 열리는 동안에는 A로 인용을 읽을 수 있다. 주소만 둔 H1도 거울에서 출전의 필드를 복원했다. [정확판 H1](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-gold-earl.ttl#L31-L42) · [대조](receipts/controls.jsonl#L6) | 원저자 링크의 판과 인용 줄을 확인한다. |
| 보존 담당자가 거울의 인용 구간을 남겨 둔 SHA-256과 대조 | B · 거울 4/4 | 고정 거울 파일 및 내용과 독립해 신뢰할 수 있는 기록 | B의 해시 문자열은 거울이 사라지면 0/4 검증에 그쳤다. [B의 묶음 조건](receipts/core.jsonl#L4) | 고정 파일을 열고 보존한 값과 실제 인용 해시를 대조한다. |
| 링크·거울 단절 뒤 정확한 인용 구간을 열고 보존 SHA와 대조 | C · 묶음만 4/4 | 전문·인용 주변 문맥 또는 독립 기준 해시가 필요한 목적에는 별도 보존 | 원문과 해시를 같이 바꾸면 묶음 내부 SHA는 여전히 일치했다. 독립 정답표는 변경을 잡았다. [이중 변경 대조](receipts/controls.jsonl#L5) | 여러 구간의 원판 위치와 보존 묶음과 별도로 관리한 판·지문을 대조한다. |

## Q1. 사전 고정한 문장과 정답

중앙에 기록된 186의 인계 SHA `7042060cd73aad96f70ff290ec6d5f6adf22570b`와 네 정답을 먼저 커밋했다. 당시 제출 20개 후보를 파일 경로와 인용 시작행으로 정렬해 각 EARL 파일의 첫 인용인 두 T06 단언을 골랐다. 새 관측은 40행의 최초 반복 중 엔진별 첫 경로인 두 T01 영수증이다. 원문 두 종류에서 주체·날짜·사건 값·인용 경계와 전체 파일 지문을 고정했다. [봉인 커밋](https://github.com/laadkke-arch/agentflow-open/commit/eed4d55bad851d084a5a762f0b81278bbf68cc16) · [모집표](frame.csv) · [정답표](gold.json)

미실행 입력은 0/2다. 186이 발행한 `not_run_reason`은 40행 모두 비어 있고, 실행 감사의 `spawned`는 40이다. 제외된 시험 정의 621행과 합성 대조 12행은 대상 실행의 미실행 근거가 되지 않는다. N1·N2에 대한 12셀은 입력 결측으로 기록했다. EARL 결과일은 원래 표기를 유지했다. H1의 시간대는 미확인이다. [186 runs.csv](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/runs.csv) · [186 실행 감사](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/execution/audit.stdout.log)

## Q2. 저장한 세 표현

A는 원저자가 연결한 주소와 짧은 표시 문장이다. B는 A에 판·유형·상대경로·인용 구간 SHA-256을 추가한다. C는 B에 인용의 정확한 원문 조각과 줄·바이트 위치를 추가한다. 역사 단언은 연속 1구간, 새 관측 영수증은 주체·시점·실제 결과를 담은 비연속 3구간이다. 구간의 순서와 경계를 보존하기 위해 각 조각 앞에 8바이트 길이를 붙여 연결한 뒤 SHA-256을 계산했다. Base64는 UTF-8 JSON 안에 원바이트를 넣기 위한 직렬화이며 해시 입력은 디코딩한 바이트다. 시험 네 문장의 원문 합은 1,784바이트다. [입력 목록](inputs.json) · [묶음 지문과 크기](receipts/bundles/package-manifest.json)

## Q3. 허용된 파일과 실제 열람

거울은 186 고정 경로의 243파일과 연결된 정확판 EARL 원문 2개로 구성했다. 전체 245파일 2,556,106바이트의 경로와 SHA-256을 먼저 확인했다. 각 회차에 새 임시 디렉터리를 만들고 필요한 파일 descriptor만 열었다. 복원 단계 이후 seccomp는 신규 파일 열기와 소켓 생성 probe를 모든 실측 회차에서 `EPERM`으로 막았다. 묶음만 있는 12실측셀의 복원 프로세스에는 묶음 descriptor 한 개만 열렸다. 정답표는 결과 점수 산정 프로세스에서만 읽었다. 비용에는 실제 묶음 읽기·고정 원파일 읽기·동봉 구간 디코딩·실패를 기록했다. [회차 로그](receipts/core.jsonl) · [실행 환경과 명령](receipts/core-run.json)

## Q4. 복원, 재열람, 대조의 분리

A와 B의 묶음만 있는 조건은 각각 표시 문장·주체·기준일 4/4를 복원했다. 이 필드들은 문장에 적혀 있었다. H1·H2는 A의 URL 자체가 정확판과 인용 줄을 가리킨다. O1·O2의 비연속 줄 위치는 그 URL로 기록되지 않았으며 A와 B의 묶음에서 미확인이다. 네 원문을 열지 못했으므로 해당 주체·기준일의 원증거도 열지 못했다. B가 보유한 해시 네 개도 비교되지 않았다. [묶음만 회차](matrix.csv) · [B/H1 대조 로그](receipts/core.jsonl#L4)

거울 조건은 A·B의 실제 원문 구간이 모두 4/4 일치했다. A의 복원기는 독립적으로 채점할 후보 바이트 지문을 계산했지만 대조할 보관 해시가 없었다. B는 입력에서 읽은 실제 구간이 저장 SHA와 4/4 일치했다. C는 두 조건에서 동봉 원문 구간을 4/4 디코딩해 보관 SHA와 비교했다. 독립된 실험 정답표의 정확판 구간과도 각각 4/4 일치했다. 대조의 객체는 인용 구간이다. 전체 파일 바이트나 역사적 사건의 독립 진위를 시험하지 않았다. [회차 기록](receipts/core.jsonl) · [고정 지문](gold.json)

## Q5. 잘못된 복원과 보류의 대조

- `basename_correct`에서 Gold와 JS의 파일명은 모두 `receipt.json`이었고 B는 Gold의 정확 경로에서 원문을 읽었다. Gold 경로를 감춘 `basename_missing`은 보류했다. 파일명만 따라간 의도적 비교 판독 `basename_naive`는 JS 경로를 읽고 원문 주체·기준일·구간을 오판했다. 두 원로그의 값이 모두 `[]`라는 사실만 보면 잘못된 귀속이 가려진다. [대조 1–3](receipts/controls.jsonl#L1-L3)
- `one_byte`는 O1의 시작 연도 한 바이트를 바꾸고 기존 SHA를 보존했다. C는 해시 불일치를 기록하고 원문 귀속을 보류했다. `both_changed`에서는 조각과 해시를 함께 바꿨다. C의 자체 해시가 일치했지만 독립 정답과 대조하여 원문 기준일과 구간을 오판으로 기록했다. [대조 4–5](receipts/controls.jsonl#L4-L5)
- H1에서 주소 외 모든 필드를 제거했다. 정확판 거울 조건은 본문의 주체·일자·인용 구간을 모두 열었지만 원래 화면 문구는 미확인이다. 묶음만 있으면 포인터가 남고 주체·일자·구간 바이트는 모두 미확인이다. 이 결과와 정상 경로 대조는 모든 주소를 일률적으로 보류하는 규칙도 반박한다. [대조 6–7](receipts/controls.jsonl#L6-L7)

## Q6. BagIt과 NIST에서 확인한 역할

RFC 8493에서 payload는 실제 파일이며 manifest는 그 경로와 체크섬을 연결한다. 선택적 fetch는 가져올 URL·길이·저장 위치를 담으며 fetch에 든 파일도 payload manifest에 있어야 한다. 완전한 bag에는 요구된 파일이 있어야 하고, 유효한 bag은 추가로 체크섬 대조를 통과해야 한다. 의회도서관의 holey bag 설명에서도 다운로드와 대조를 거친 후 완결된다. 로컬 역할 예는 동일한 manifest와 fetch에서 payload가 없으면 미확인, 원바이트가 있으면 일치, 변조하면 불일치를 냈다. 간이 역할 대조이며 bagit-python 적합성 검사는 실시하지 않았다. [RFC 8493 §1.4](https://www.rfc-editor.org/rfc/rfc8493.html#section-1.4) · [§2.2.3](https://www.rfc-editor.org/rfc/rfc8493.html#section-2.2.3) · [의회도서관 보존 설명](https://blogs.loc.gov/thesignal/2012/01/from-there-to-here-from-here-to-there-digital-content-is-everywhere/) · [bagit-python](https://libraryofcongress.github.io/bagit-python/) · [로컬 대조](receipts/public-comparison.json)

NIST 2026년 제품 목록 PDF p.50의 2197 행은 제품과 세트·2 mm 용도를 회수할 수 있다. 같은 제품의 로트·판 날짜·인증 흡수에너지·확장불확도는 그 행에서 확인할 수 없다. LL-198 성적서 p.1은 2024-07-17, 19.1 J, 확장불확도 0.2 J를 명시한다. LL-165 성적서는 같은 제품으로 표시되나 2017-11-09, 17.3 J, 0.098 J다. 동결된 판독 기록의 다섯 필드 대조는 카탈로그 1일치·4미확인, 정확판 5일치, 다른 로트 1일치·4불일치였다. 아카이브 인덱스를 함께 열면 정확판 링크를 찾을 수 있었다. 현재 상점 상세와 PDF 원바이트는 미확인이다. 세 PDF 파일의 직접 전송 요청은 모두 Cloud 터널 403으로 종료했다. [2026 제품 목록 p.50](https://tsapps.nist.gov/srmext/certificates/documents/Annual_SRM_Product_List.pdf#page=50) · [LL-198 p.1](https://tsapps.nist.gov/srmext/certificates/archives/2197_LotLL-198_Cert_2024-07-17.pdf#page=1) · [LL-165 p.1–2](https://tsapps.nist.gov/srmext/certificates/archives/2197_LotLL-165_Cert_2017-11-09.pdf#page=1) · [아카이브](https://shop.nist.gov/ccrz__CCPage?pageKey=SRMArchive) · [원바이트 접근 기록](receipts/public-pdf-transport.json)

지정 진입점에서 연계한 Pine Needles 연구 260-156은 2004년 발행의 분석 보고이고, SRM 1575a의 2022년 성적서 p.1은 판과 유효기간을 표시한다. 해당 판의 표지에서 독립 로트 번호를 찾지 못했다. 로트 비교에는 명시 번호가 있는 Charpy 시편을 사용했다. [2004 원보고 p.6](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=903454#page=6) · [1575a 성적서 p.1](https://tsapps.nist.gov/srmext/certificates/archives/1575a.pdf#page=1)

## Q7. 목적별 충분성과 관측 비용

거울의 A·B·C는 각각 4복원·0보류·0오판이었다. 묶음만 있는 A·B는 각각 0완전복원·4보류·0오판이었다. 같은 조건의 C는 4복원·0보류·0오판이다. 완전복원은 표 2의 표시값 및 원증거와 인용 위치가 정답과 일치한 상태다. 처리 지문에 대한 별도 대조가 필요한 목적에는 A의 `no_stored_hash`가 남는다. 12개 입력 결측셀과 7개 통제셀은 이 분모 밖이다. [판정 원장](matrix.csv) · [결정 비용](costs.csv)

## 경쟁 설명

1. 정확판 주소와 그 시점의 원문 가용성이 회복을 설명할 수 있다. A의 주소에는 원래부터 SHA와 경로가 있었고 두 과거 단언에는 줄 위치도 있었다. A는 거울 접근으로 인용을 4/4 회수했다. H1 주소는 초기 동결 과정에서 그 고정 원파일을 HTTP 200으로 가져오게 했다. 깨진 주소 자체가 A의 모든 상황을 대표한다는 설명은 성립하지 않는다. [H1](https://github.com/w3c/json-ld-api/blob/8811ba2a3bcae883ac91efacffb70ef08d84e92f/reports/jsonld-gold-earl.ttl#L31-L42) · [A/H1 거울](receipts/core.jsonl#L1)
2. 표시 문장이 정확하다는 설명과 과거 원문까지 보존되었다는 설명은 별개다. 동일한 주소·문장이라도 B의 해시만 남은 회차는 확인할 파일이 없었으며 C가 실제 동봉 바이트를 읽었다. 오래된 엔진 실행을 다시 검증했다는 결론은 이 비교에서 도출할 수 없다. [B/H1 묶음](receipts/core.jsonl#L4) · [C/H1 묶음](receipts/core.jsonl#L6)
3. 해시 비교가 독립 진위를 보장한다는 설명은 원문·해시 동시 변경에서 반박됐다. 제3자가 별도로 고정한 해시, 신뢰한 서명 또는 원판이 있어야 동봉한 값과 다른 증거로 대조할 수 있다. NIST 예에서도 부모 제품 식별자가 동일해도 시점과 로트가 바뀐다. [동시 변경](receipts/controls.jsonl#L5) · [제품·로트 대조](receipts/public-comparison.json)

## 재사용 조건과 비용

네 문장이 한 번 보관되는 분모에서 A는 1,192 B, B는 2,078 B, C는 5,134 B다. 주소 값의 UTF-8 합은 556 B다. B 메타데이터의 순증분은 886 B, C에 추가한 locator와 Base64 원문 직렬화는 3,056 B다. 이 증분이 담은 인용 구간의 원바이트 합은 1,784 B다. 비용은 파일 단위 JSON의 실제 바이트로 측정했으며 압축·중복 제거·스토리지 청구비·거울 운영비는 측정하지 않았다. [직렬화 비용](costs.csv)

거울이 있을 때 A·B는 각각 묶음 4회와 원파일 4회를 읽어, 원파일에서는 각각 1,642,494바이트를 읽었다. 거울이 없으면 각 안에서 원파일 조회 네 건이 실패했다. C는 두 조건 모두 묶음 4회와 동봉 구간 4회 디코딩으로 끝났다. 독립 디렉터리에 245파일을 준비하고 descriptor를 열어 둔 셋업은 이 열람 수와 별도다. A/B의 I/O가 큰 이유는 이 시험의 판독기가 전체 원파일에서 줄 위치를 찾거나 읽기 때문이다. 인덱스·범위 읽기 비용은 실측 범위 밖이다. [경로·크기 기록](receipts/core.jsonl) · [비용](costs.csv)

동일한 원천에 써 볼 때는 주소의 고정판과 인용 위치 표현, 표시 문장의 필드 포함 여부, 거울 보장 수준, 보존 해시를 독립 저장할 수 있는지를 먼저 확인한다. 새 문서 형식에서 원본 구간을 찾는 데 필요한 locator가 달라질 수 있다. 다음 절차는 고정 입력을 다시 준비하고 별도 임시 경로에서 복원한다. Bash, Python 3.12 및 Linux libseccomp.so.2를 사용했다. GitHub fetch와 원문 두 개 내려받기는 동결 입력 준비에만 필요하다.

```bash
set -euo pipefail
owned=docs/workstreams/research/AF-RES-196
prior=docs/workstreams/research/AF-RES-186
dep=7042060cd73aad96f70ff290ec6d5f6adf22570b
suite=8811ba2a3bcae883ac91efacffb70ef08d84e92f
scratch=$(mktemp -d)
mirror="$scratch/mirror"
repo_source="$mirror/laadkke-arch/agentflow-open/$dep"
report_source="$mirror/w3c/json-ld-api/$suite/reports"
mkdir -p "$repo_source" "$report_source" "$scratch/replay"
git fetch --no-tags origin "$dep"
git archive "$dep" "$prior/" | tar -x -C "$repo_source"
for name in jsonld-gold-earl.ttl jsonld-js-earl.ttl; do
  curl --fail --show-error --location -o "$report_source/$name" \
    "https://raw.githubusercontent.com/w3c/json-ld-api/$suite/reports/$name"
done

python3 -B "$owned/make_bundles.py" --inputs "$owned/inputs.json" --gold "$owned/gold.json" \
  --mirror "$mirror" --out "$scratch/replay/bundles"
python3 -B "$owned/audit.py" run --inputs "$owned/inputs.json" --gold "$owned/gold.json" \
  --mirror "$mirror" --bundles "$scratch/replay/bundles" --out "$scratch/replay"
python3 -B "$owned/audit.py" controls --inputs "$owned/inputs.json" --gold "$owned/gold.json" \
  --mirror "$mirror" --bundles "$scratch/replay/bundles" --out "$scratch/replay"
cmp "$owned/matrix.csv" "$scratch/replay/matrix.csv"
cmp "$owned/costs.csv" "$scratch/replay/costs.csv"
```

## 추가 분석

주 표본에서 복원 단위는 네 문장이고 기간별 증거는 제출 단언 두 건과 실행 영수증 두 건이다. 같은 실행의 stdout과 영수증은 다른 파일이지만 실행을 늘리지 않는다. 표본은 한 186 릴리스의 T06 compact와 T01 expand 두 입력에 한정된다. 실제로 읽은 보조 영수증의 실행 ID는 12개이며 같은 환경에서 왔다. 외부 보존 자료와 통제 사본은 더 많은 기존 JSON-LD 실행 증거가 아니다. [출처 원장](sources.jsonl) · [자체점검](SELF_CHECK.md)

| 불일치·약점 | 영향을 받는 주장 | 다음 조사와 원자료 | 판단을 뒤집을 관측 |
| --- | --- | --- | --- |
| 미실행 유형 0/2, 실재 문장은 한 고정 인계와 두 시험 키에 집중 | 셋의 충분안이 다른 미실행 기록·자료 형식에도 성립하는지 | 다음 완료 인계에서 실제 미실행 사유·기록일·정확 위치를 가진 원영수증과 다른 형식의 출판물을 추가한다. [186 원장](https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/runs.csv) | 미실행 기록에서 동일한 창이 여러 의미를 가져 C만으로 주체·기준일을 구별하지 못하거나, 다른 자료에서 A가 동봉 근거 없이 원문을 복원한다. |
| C의 바이트와 해시를 함께 바꾸면 묶음 내부 비교가 통과 | C의 일치를 독립적으로 신뢰할 수 있는지 | 같은 구간의 원판·분리 저장된 기준 해시·검증 가능한 서명을 확보하고 동시 변조를 다시 판독한다. [동시 변경 통제](receipts/controls.jsonl#L5) | 독립 지문을 사용한 C 대조가 변조 바이트를 거절하고 동일한 정본을 계속 회수한다. |
| NIST 비교는 직접 연 PDF 본문 판독에 의존하며 현재 상점과 원 PDF 바이트를 확보하지 못함 | 카탈로그를 통한 정확한 과거 로트 접근과 PDF 바이트 일치 | 공식 2197 상점, 연감과 LL-198·LL-165 원 PDF를 파일로 확보하고 SHA 및 로트·판·수치를 대조한다. [동결 판독](receipts/public-freeze.json) | 같은 특정 판·로트의 성적서 내용을 제품 레코드 자체가 모두 보존하거나, 같은 주소에 다른 판의 원바이트가 관측된다. |
