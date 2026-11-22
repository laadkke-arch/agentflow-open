# AF-RES-023 — 실제 병합·분리 뒤 옛 링크와 추천 이유의 복원

## 인계 상태

**REVIEW_READY_WITH_GAPS.** 실제 사건 18개, 네 시스템, 보수적으로 산입한 고유 외부 원문 38개, 외부 독립 소비자 원문 7개와 세 표현 비교 54행을 커밋했다. 그러나 모든 사건의 원 ID·전후 판·정정 연결을 완성한 것은 아니며, 날짜가 검증된 소비자 이력 6개와 약 3분의 1씩의 표본 구성도 충족하지 못했다. 수용 조건은 **31개 중 26개 충족, 5개 미충족**이다. 정합 검사 통과를 이 미충족 조건의 통과로 바꾸지 않는다.

이 파일은 SELF_CHECK.md와 수용 근거를 포함한 선행 커밋 `2260df91e9c71e939581ca8b71754e6cfa4f7303`을 GitHub에서 다시 읽어 내용 일치를 확인하고, 로컬 HEAD도 그 커밋이며 작업 트리가 깨끗한 것을 확인한 **뒤에 작성했다**. 마지막 커밋에는 이 HANDOFF.md만 넣는다. 자체 커밋 SHA는 파일 안에 자기 참조로 만들지 않고 아래 확인 명령으로 찾는다.

## 핵심 결과와 실제 분모

| 단위 | 결과 | 판정 범위 |
| --- | --- | --- |
| 실제 본 사건 | 18 = MusicBrainz 6 + ROR 6 + Homebrew 5 + Wikidata 1 | 시스템별 최대 6. 기각·별칭·동일 ID 오염 정정도 각자 별도 코드이며 모두 실제 병합이라고 부르지 않는다. |
| 표본 구성 | 허용 병합 5 / 정정·분리·되돌림 9 / 기타 4 | 목표 약 6/6/6에 미달. 정정군 9개 중 문자 그대로의 오병합 정정은 3개다. |
| 출처 원장 | 135개 ID·135개 URL | 실패·보충·같은 사건의 전후 화면을 포함하므로 135개 독립 근거라고 세지 않는다. |
| 보수적 고유 원문 | 38 = 사건 대표 18 + 정책·지침 12 + 소비자 기록 8 | 같은 사건의 여러 화면은 대표 하나만 최소 수에 산입. 소비자 8개 중 하나는 같은 시스템의 별도 Wikidata 항목이다. |
| 외부 독립 소비자 | 7개 | 날짜가 있는 후속 체인은 4개(외부 3 + Wikidata 내부 1), 불변 전후 인용 diff는 3개. ROR 소비자 4개의 최초 인용·정정 날짜는 미확인이다. |
| 세 표현 복원 비교 | 54 = 18 × 3 | v3의 동일한 16사건 48행과 v4의 두 사건 재판독 6행. 단일 54행 재실행이나 실제 역사 추천문 18개에 대한 시험이 아니다. |
| 식별·복원 필드 | 독립 식별 열 18행, 복원 차원 90행(18 × 5) | AUTO는 해당 정보로 필드를 결정할 수 있다는 해석이다. 자동 복구 실행은 0/18이다. |
| 실제 사람의 오추천 피해 | 18/18 미확인 | 공개 소비자 파일 수정·운영자 장애 보고·기계적 오도착 가능성과 실제 사람의 피해를 구별했다. |

분모는 [sources.json](sources.json), [events.jsonl](events.jsonl), [citations.csv](citations.csv), [reconstruction.csv](reconstruction.csv), [counts.json](evidence/counts.json)에 연결되어 있다. 미확인과 보류를 분모에서 빼지 않았다.

### 1. 주소가 열려도 이전 기능까지 보존된 것은 아니다

Homebrew SW06의 옛 `tree-sitter` formula 주소는 이번 HTTP 관측에서 200이었지만, 분리 후에는 library를 가리켰다. CLI가 필요했던 소비자의 후속 파일은 `tree-sitter-cli`로 고쳤다. 반대로 SW02의 옛 `main` 파일 경로는 404였지만, 이름 변경 전 고정 커밋에서 libxml++ 3.2.4 recipe 본문을 읽을 수 있었다. 고정 커밋 URL에 대한 HTTP 시도는 503이었고 GitHub 연결 도구로 본문을 읽었으므로, 이를 고정 URL의 HTTP 200으로 바꾸어 쓰지 않았다. 근거: SW-S05·SW-S14·SW-S25, SW-D02, [RESULT Q3](RESULT.md#q3-전후-id-판-http는-어디를-가리켰는가), `collectors/software/http-observations.json`.

### 2. 개체를 되돌리는 일과 인용·속성을 복구하는 일은 별도다

WD01에서는 기관 항목의 병합을 되돌린 뒤 건물 항목의 P910 인용을 별도 revision으로 되돌렸다. 이 한 소비자 복구가 전체 그래프 복구를 증명하지는 않는다. ROR07은 v1.60 고정 변경 JSON에서 이탈리아 이름·웹사이트·상위 기관을 복구했지만 Spain/Leioa 위치가 남아 있었다. 이는 해당 고정 변경 파일의 관측이며 2026년 전체 live API가 같은 상태라고 주장하지 않는다. MB06의 AcoustID issue는 옛 MBID 전파 문제와 처리 재개 뒤 복제 미반영을 구별한다. 근거: WD-S06·08·09, ROR-S31, MB-S23, [restoration.csv](restoration.csv).

### 3. 이력은 과거 주장을 복원해도 현재 대체 대상 하나를 정하지 못할 수 있다

ROR05의 옛 ZFH 기록은 역사적 평가 인용에 여전히 필요하지만 후계가 네 곳이므로 프로그램 정보 없이 현재 문의처 하나를 정할 수 없다. ROR07에서 잘못 이식된 스페인 기관의 올바른 ROR는 이번 자료로 미확인이다. SW05에서는 고정 PostgreSQL 14 판을 보존하는 목적과 Rails 소비자가 최신 PostgreSQL 16을 원한 목적이 다르다. 따라서 관계 이력을 추가한 ③에서도 HOLD·CONDITIONAL을 남겼다. 근거: ROR-S17–20·ROR-S30–31·SW-S20, ROR05·07 사건 원장과 SW-D01 인용 원장, [RESULT Q6](RESULT.md#q6-세-저장-표현은-무엇을-복원했는가).

### 4. 짧은 링크가 충분한 경우와 실제 중복도 남겼다

MB04의 좁은 recording 조회 목적은 같은 retained MBID와 짧은 이유만으로 맞출 수 있었다. SW01은 같은 배포 archive를 가리키는 중복 formula였고, MB05는 트랙 누락이 있는 중복 release를 보완한 뒤 병합했다. 차이가 있다는 이유만으로 모두 분리하면 이 중복을 놓친다. 다만 음원 자체·archive 바이트·실물 음반을 이번 실행에서 비교한 것은 아니며, 허용된 catalog 편집을 모든 사용 목적의 동등성으로 확대하지 않는다. 근거: MB-S17, MB05 편집 48434703·48447069, SW-S01 및 [alternatives.md](alternatives.md).

## 입력·결과 커밋과 확인 위치

| 항목 | 고정 값 또는 확인 위치 |
| --- | --- |
| 저장소·브랜치·소유 경로 | `laadkke-arch/agentflow-open` · `work/research-af-res-023` · `docs/workstreams/research/AF-RES-023/` |
| 배정 시 foundation | `7f66165ad68610278df18855e1196a6cf52b035a` |
| 계획 기준판 | `b507fbcab09724a77270e658355f4b661cc35f02` |
| 고정 의존 입력 | AF-RES-020 `856e6b40ae12d43197a6f02f7bf6ab7a7506fd35`의 HANDOFF 전체, B19 전체, RESULT Q1·Q3, DECISIONS D04–D06. 절·행은 [SCOPE.md](SCOPE.md). |
| 실행 위치·모델 | ChatGPT 공유 Linux workspace `/workspace/scratch/05a4ed6cd8b5/agentflow-open`; 세션 표기 GPT-6 Astra Pro. 내부 조사자·판독자도 같은 모델 계열. 사람의 독립 시험이 아니다. |
| 원문 관측 창 | 2026-11-22 03:09–04:09 UTC, Asia/Seoul 같은 날 12:09–13:09. 이후 파일 점검·커밋 수행. |
| 시스템별 사건 커밋 | Wikidata `add402d0203693fa2d0c9efc3b07a9e9d9a614fb`; software `60cb76c1a8f64abe585a99a789833450446ce7af`; ROR `c5fb3e8d4e923a94b6f0cf79efc527d8cd2114d1`; MusicBrainz `64644506d75dad84de350d53d354320d65ae4786`. |
| 여섯 사건씩 비교 커밋 | B01 `b2879a0e669268ca4a7fdfada63bb7d3ed8570c6`; B02 `db9d7fe9bace6cd45ee6c76fbd9aa0ddeda945c9`; B03 `d05b7269a0eeff7a0958de5c58dba9744e4a2a5a`. |
| 결과·검사 선행 커밋 | **`2260df91e9c71e939581ca8b71754e6cfa4f7303`**. [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/2260df91e9c71e939581ca8b71754e6cfa4f7303/docs/workstreams/research/AF-RES-023/RESULT.md), [고정 SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/2260df91e9c71e939581ca8b71754e6cfa4f7303/docs/workstreams/research/AF-RES-023/SELF_CHECK.md), [고정 수용 근거](https://github.com/laadkke-arch/agentflow-open/blob/2260df91e9c71e939581ca8b71754e6cfa4f7303/docs/workstreams/research/AF-RES-023/evidence/acceptance-evidence.json). SELF_CHECK blob `de9d7a9e65ef4885055ad07da8cf8c1375ee5cb5`, 수용 근거 blob `752975f7ede2c78a8e10d44bae635ec95e800031`을 원격 재열람했다. |
| 전체 묶음·보기/답안 고정 순서 | [PROGRESS.md](PROGRESS.md), [선행 14커밋 원장](evidence/commit-log.json), `evidence/frozen-manifest*.json`, `evidence/answer-freeze*.json`, `evidence/exposure-log.jsonl`. 위 결과·검사 커밋과 마지막 HANDOFF 커밋은 Git 이력으로 덧붙여 확인한다. |

공통 계약·진행표·색인·`dot-control.json`·제품 코드·main을 수정하지 않았다. 작업 결과를 공통 브랜치에 병합하지 않았다. 새 integration을 이 작업의 입력으로 소급하지 않았다. 마지막 session check가 관측한 integration은 `2f3593a43f77f6023d0d176bcc0f21905883af45`이며, 배정 시 base는 그대로 유지했다.

## 복원 비교의 해석과 열린 판단

보기와 사후 키를 분리해 먼저 고정하고, 각 표현만 받는 새 내부 문맥에서 답을 저장한 뒤 대조했다. root와 수집자는 원문·정답에 노출되어 있으므로 최종 채점은 **자기 점검**이다. 실제 소비자의 추천문 18개를 발견한 것처럼 표현하지 않는다. 짧은 이유는 공개 기록의 문맥으로 만든 통제된 예시다.

초기 입력의 경로·공통 ID 표기·관계 정보 혼입을 v3에서 고쳤고, 원문에는 있으나 보기에서 빠졌던 MB05 survivor와 SW03 정정 후 버전은 v4에서 보강했다. v1과 v3의 옛 답안·오류를 그대로 남겼다. 최종 54행은 바뀌지 않은 v3 카드 48행과 v4 두 사건 6행이며, 공통 질문·누락 규칙·카드 해시와 불변 키를 검사했다. [protocol-errata.md](evidence/protocol-errata.md)와 [scoring-rubric.md](evidence/scoring-rubric.md)에 변경 원인과 범위를 기록했다.

목적지 원답안 분포는 ① SELECT 3/HOLD 15, ② SELECT 5/HOLD 12/CONDITIONAL 1, ③ SELECT 15/HOLD 2/CONDITIONAL 1이다. **성공률로 읽지 않는다.** MB03①은 B4 문맥을 검증하지 않은 채 retained 2:32를 골라 `WRONG_FOR_REQUEST`다. ROR06②의 선택은 당시 v1.66의 SLP 표기에 한정되므로 `HISTORICAL_ONLY`이며, 현재의 올바른 SLP ID를 복원했다는 뜻이 아니다. ROR05②도 역사적 EQAR 기록만 고른 답이다. 모델 변동·인과효과·전체 오병합률은 추정하지 않았다.

아직 열려 있는 수용 조건은 다음과 같다. 각 행의 `met=false`와 최소 보강 입력은 [acceptance-evidence.json](evidence/acceptance-evidence.json)에 보존했다.

| 조건 | 미충족 이유 | 판단을 바꿀 최소 입력 |
| --- | --- | --- |
| C06 완전 전후 이력 18개 | MB01 source 매핑은 추론, MB03·04 source ID 미노출, MB06 즉시 target 미확인. ROR02 기각의 전후 전체 dump도 없음. | 공식 edit_data 60587125·68967621·92853437·151147443와 필요한 redirect 행; ROR 해당 전후 고정판. |
| C13 날짜 있는 소비자 체인 6개 | 후속 날짜 체인 4개, 불변 인용 diff 3개. ROR 네 소비자의 현재 페이지는 최초 인용·수정 시점을 증명하지 않음. | 각 소비자의 변경 전 불변 파일/보관판 및 후속 commit·배포 날짜. |
| C15 외부 ID 발급자 원문 전수 확인 | catalog에 적힌 ISRC·GRID·ISNI·GND 등을 발급기관의 당시 원문과 전수 대조하지 못함. | 해당 시점 발급자 record와 ID를 옮긴 편집의 provenance. |
| C23 약 3분의 1씩 표집 | 실제 5/9/4. 원하는 균형을 맞추려고 오염 정정을 허용 병합으로 재코딩하지 않음. | 원 ID·정정 키가 완전한 허용 병합/승계·기각 표본의 추가 조사. |
| C30 ROR 전체 배포판 검증 | 공식 fixed changed JSON와 배포 댓글까지 읽었고, 전체 release dump·live API와의 대조는 미실시. | v1.38·v1.60 등 해당 공식 전체 배포 파일과 배포 manifest, 동일 ROR 필드 비교. |

## 수행한 점검과 재확인 명령

선행 커밋의 정합 검사 **41개 통과(exit 0)**, 원격 갱신을 포함한 `workbench.session check --fetch`도 **passed / remote_checked / exit 0**였다. 근거는 [validation-results.json](evidence/validation-results.json), [session-check.json](evidence/session-check.json). 마지막 원문 재열람은 Q1–Q7에 걸친 핵심 7개에 수행했으며 [final-source-recheck.json](evidence/final-source-recheck.json)에 정확한 위치를 기록했다. 모든 135 URL의 영구 가용성을 검사했다는 뜻은 아니다.

다음 명령은 저장소 루트에서 실행한다. 첫 명령은 파일을 다시 쓰지 않는다. HANDOFF 존재 항목을 포함하면 정합 항목은 42개가 된다. 별도로 마지막 커밋의 파일 목록이 HANDOFF 하나인지 확인해야 한다.

```bash
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-023/scripts/validate_research.py --no-write --check-handoff
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-023/manifest.json --fetch
git status --porcelain
git log -1 --format=%H -- docs/workstreams/research/AF-RES-023/HANDOFF.md
git diff-tree --no-commit-id --name-only -r HEAD
git diff --name-only 7f66165ad68610278df18855e1196a6cf52b035a HEAD
```

음원 비교, brew 설치·과거 keg 재현, AgentScript build, 전체 AcoustID replica 검사는 실행하지 않았다. 따라서 그 결과가 필요한 기능 동등성·전파 완결성은 편집자 진술 또는 문서 범위로 제한했다. 이 연구의 구조 검사를 해당 외부 실행의 성공으로 대체하지 않는다.

## 다음 첫 행동과 미실행 입력·명령

**첫 행동은 MusicBrainz 공식 snapshot의 네 edit_data 원행을 확보해 source/즉시 target의 빈칸을 메우는 것이다.** 현재 redirect를 과거 target으로 소급하지 않는다. MB01의 추론을 확정하거나 반박하고, MB03·04의 원 source, MB06의 2022년 즉시 target을 확인한 뒤 C06과 복원 키를 다시 판정한다.

공식 `20261121-002203/mbdump-edit.tar.bz2`에 대한 HEAD는 HTTP 200, Content-Length 17,284,315,658바이트였다. 전체 다운로드·해제·행 추출은 **미실시**이며, 접근 차단이나 데이터 손실이 확인된 것은 아니다. 아래는 재개용 명령이다. archive member와 COPY 첫 열 형식도 아직 확인하지 않았으므로 먼저 목록·checksum·schema를 검증해야 한다. 원본 대용량 dump를 Git에 넣지 말고, 필요한 ID·판·관계와 검증값만 요약해 소유 경로에 커밋한다. 자세한 입력 관측은 [DUMP_FOLLOWUP.md](collectors/musicbrainz/DUMP_FOLLOWUP.md).

```bash
AF_RES_023_MB_BASE='https://data.metabrainz.org/pub/musicbrainz/data/fullexport/20261121-002203'
AF_RES_023_MB_DIR='docs/workstreams/research/AF-RES-023/collectors/musicbrainz/dump-input'
mkdir -p "$AF_RES_023_MB_DIR"
curl --fail --location --output "$AF_RES_023_MB_DIR/mbdump-edit.tar.bz2" "$AF_RES_023_MB_BASE/mbdump-edit.tar.bz2"
curl --fail --location --output "$AF_RES_023_MB_DIR/SHA256SUMS" "$AF_RES_023_MB_BASE/SHA256SUMS"
sha256sum "$AF_RES_023_MB_DIR/mbdump-edit.tar.bz2"
rg 'mbdump-edit.tar.bz2' "$AF_RES_023_MB_DIR/SHA256SUMS"
tar --list --bzip2 --file "$AF_RES_023_MB_DIR/mbdump-edit.tar.bz2"
```

checksum이 일치하고 실제 member가 `mbdump/edit_data`, 첫 열이 edit ID인 tab 구분 형식임을 확인한 뒤에만 다음 필터를 쓴다. 두 압축 순회가 발생하므로 운영자가 별도 추출 환경을 쓰더라도 결과 요약은 지정 소유 경로에 남긴다.

```bash
tar --extract --bzip2 --to-stdout --file "$AF_RES_023_MB_DIR/mbdump-edit.tar.bz2" mbdump/edit_data \
  | awk -F '\t' '$1 == 60587125 || $1 == 68967621 || $1 == 92853437 || $1 == 151147443 { print }'
```

그 다음 ROR07의 전체 배포판을 확인한다. 입력은 **공식 배포 manifest로 판을 확인한 v1.38 및 v1.60 전체 JSON**, 대상은 `https://ror.org/041xzk838`이다. 이 실행에서는 전체 dump 다운로드 URL을 확정하지 않았으므로 추측 URL을 기록하지 않는다. `collectors/ror/sources.json`의 ROR-S28·31 및 그 원 출처에서 배포판의 정식 파일을 찾아 각각 아래 경로에 저장한 뒤 실행한다. 다음 스크립트도 미실행이며, 최상위 배열 형식이 아니면 멈추고 공식 schema에 맞게 입력을 확인하도록 했다.

```bash
python - docs/workstreams/research/AF-RES-023/collectors/ror/dump-input/ror-v1.38.json docs/workstreams/research/AF-RES-023/collectors/ror/dump-input/ror-v1.60.json <<'PY'
import json, sys
from pathlib import Path
for name in sys.argv[1:]:
    records = json.loads(Path(name).read_text())
    if not isinstance(records, list):
        raise SystemExit(f'공식 schema 확인 필요: {name}')
    matches = [r for r in records if r.get('id') == 'https://ror.org/041xzk838']
    if len(matches) != 1:
        raise SystemExit(f'ID 일치 수 확인 필요: {name}: {len(matches)}')
    print(json.dumps({'input': name, 'record': matches[0]}, ensure_ascii=False))
PY
```

전체 배포판에서도 이름·URL·상위 관계 복구와 위치 잔존이 함께 확인되는지 비교하고, 현재 live 값은 별도 관측 시점으로 기록한다. 공식 changed JSON과 전체 dump가 다르면 현 결론의 범위를 수정한다. 소비자 후속 조사에서는 COMTES·EQAR·CoLab·OpenAlex의 사전 고정판 및 정정 날짜를 먼저 확보한다. 현재 페이지의 차이만으로 실제 전파 지연 기간을 계산하지 않는다.

## 진행 담당에게 넘길 색인 반영 제안

공통 색인에는 다음 범위의 참조를 제안한다. **“B19 운영 식별 사건 보강: AF-RES-023, 실제 18사건·4시스템·보수적 원문 38·복원 비교 54행, REVIEW_READY_WITH_GAPS. URL 생존/과거 대상/기능·판/목적과 관계 이력을 구별하며, 전체 전후 이력 18개를 완성한 자료는 아님.”** AF-RES-003·020의 정의를 반복 집계하지 말고, MB04·SW01의 좁은 링크 충분 사례와 SW06·WD01·ROR05/07의 반례를 연결하면 된다.

제품 DB·ID 체계·자동 병합 정책을 확정하지 않는다. 엄격 병합/가역 별칭/관련 후보 병렬 표시의 조건과 관측 비용은 alternatives.md의 제안으로만 넘긴다. 다른 PLAN 5 작업의 파일·완료를 기다리지 않았으며, 이번 결과를 이유로 공통 진행 상태를 직접 고치지 않았다.

## 가장 중요한 약점 3건과 다음 조사 제안

| 중요한 불일치·약점 | 근거 ID·주소 | 이 약점이 바꿀 판단 | 다음 조사 질문·자료·최소 확인 |
| --- | --- | --- | --- |
| 원 source/중간 target 및 전체 배포판·발급자 원문이 일부 비어 있다. | C06·C15·C30; [MusicBrainz dump 입력](collectors/musicbrainz/DUMP_FOLLOWUP.md), ROR-S31, [events.jsonl](events.jsonl). | 이력이 있으면 원 ID·인용·외부 ID까지 충분히 복원된다는 결론은 보류한다. 공개 UI 미노출을 실제 정보 소실로 판정할 수 없다. | edit_data 네 행과 필요한 redirect를 먼저 추출한다. 이어 ROR v1.38/v1.60 전체 dump와 당시 발급자 record를 비교해 고정 변경 파일의 관측 범위가 유지되는지 확인한다. |
| 소비자 원문 수는 충족하지만 날짜 있는 사전·사후 체인은 부족하고 실제 사람의 피해는 미확인이다. | C13; [citations.csv](citations.csv) ROR-C01–04·MB-C01·SW-D01/02·WD-C01. | “옛 추천이 실제로 잘못 사용됐다”, 전파 지연 기간, 소비자 정정률을 계산할 수 없다. | ROR 네 소비자의 사전 불변판과 후속 commit/배포일을 확보한다. 사용 목적·작성 시점·교정 도착점을 한 체인으로 묶을 수 있는 외부 사례를 최소 두 개 더 확인한다. |
| 표집은 5/9/4로 치우쳤고 복원 비교는 같은 모델 계열의 내부 자기 점검이다. | C23; [protocol-errata.md](evidence/protocol-errata.md), [reconstruction.csv](reconstruction.csv), [exposure-log.jsonl](evidence/exposure-log.jsonl). | ③의 SELECT 증가를 성공률·운영 효과·전체 오류율로 일반화할 수 없다. 입력 누락 보강과 실제 관계 미보존을 구별해야 한다. | 완전한 정정 키를 가진 허용 병합·승계 사례와 실제 당시 추천문을 추가한다. 고정된 동일 보기·누락 조건으로 별도 사람 또는 외부 판독을 실시하고 오답·보류를 같은 분모에 남긴다. |
