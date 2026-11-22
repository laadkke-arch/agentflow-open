# AF-RES-039 · 단일 저장물 재조회 인계

**REVIEW_READY_WITH_GAPS · 수용 조건 15/18.** 결과 커밋은 **`7e7773cdec4c2213d2e81e0094fa5b6e742ec0e8`**다. 12참조의 48실행과 24짝, 두 예산의 판정·실측, 원문 33건, R01/G05 빈 폴더 재생 8건을 원격 브랜치에 저장했다. [고정 결과](https://github.com/laadkke-arch/agentflow-open/blob/7e7773cdec4c2213d2e81e0094fa5b6e742ec0e8/docs/workstreams/research/AF-RES-039/RESULT.md) · [고정 수용 파일](https://github.com/laadkke-arch/agentflow-open/blob/7e7773cdec4c2213d2e81e0094fa5b6e742ec0e8/docs/workstreams/research/AF-RES-039/evidence/acceptance-evidence.json)

- 실행 지점은 `laadkke-arch/agentflow-open`의 `work/research-af-res-039`이다. 배정 기준 `de544231bc72fa6f2ddb3e91f9c0e8d16a0d1f62`, 계획 기준 `922bf3171cab62f30469720ac80327ad3f24fbf9`, 의존 AF-RES-036 `5682b0d61a80edc159d4b510d213bbb4c69543be`다. 모델 표시 범위는 Codex·GPT-6 계열이며 정확한 모델 변형과 추론 강도는 미확인이다. 관리형 Linux와 제한 egress를 사용했다. [manifest](manifest.json)
- 고정 RESULT의 3–52행에 필수 표 1의 실행 48행, 54–59행에 필수 표 2의 예산별 네 행이 있다. 111–115행에 우선순위 약점 세 행이 있다. [실행 원장](attempts.jsonl) · [48행 검산](runs.csv) · [24짝 검산](pairs.csv) · [원문 원장](sources.jsonl)

## 검증한 결론

| 과업 | C1 | C2 | 확인 범위 |
| --- | --- | --- | --- |
| T현재 | G02 유지 1/12, 보류 11/12 | G02 유지 1/12, 보류 11/12 | 새 현재 기준은 4/12에서 확인했다. 기준이 있는 네 건 중 하나에서 필요한 본문을 얻었다. |
| T복원 | 정확 N 1/12, H 0/12, N+H 0/12 | 정확 N 1/12, 로컬 H 12/12, N+H 1/12 | 양쪽 예산의 완전 성공 결과가 같다. G02 C2의 독립 H는 논리 기준에서 2개 발췌 중 1개, 엄격 기준에서 0개다. |
| 실제 비용 | 47 논리 GET, 7 문서 HTTP 교환, 956,276B | 47 논리 GET, 8 문서 HTTP 교환, 724,028B | 받은 내용과 성공 범위가 달라 동일 산출물 절감액은 미확인이다. C2는 원 직렬화로 25,992B 더 보관한다. |

94 논리 GET 중 88건은 실패했고 80건은 HTTPS CONNECT에서 거부됐다. R01/G05 같은 입력 8건의 경로·상태·해시·행동이 본실행과 같았다. G05의 두 GNU 원문과 R01의 같은 발행자 release HTML을 공개 웹에서 별도 확인했으며, 이 응답은 48건 비용과 성공 분자에서 제외했다. [실제 계측](evidence/receipts.json) · [재실행](evidence/replication.csv)

## 미충족 및 재개 첫 자료

| 조건 | 미확인 범위 | 첫 자료 |
| --- | --- | --- |
| A07 | 현재 기준은 12곳 중 4곳 확인. 2018 POSIX, GNU FTP 및 Bioconductor 3.11 원 경로는 새 접근에서 다수 보류됐다. | [G03 2018 index](https://pubs.opengroup.org/onlinepubs/9699919799/mindex.html), [G05 현재 -MM](https://gcc.gnu.org/onlinedocs/gcc/Preprocessor-Options.html#index-MM), [기준 원장](evidence/current-criteria.jsonl) |
| A10 | R01의 036 당시 3.11 대체 HTML과 1.12.0 tarball은 각각 접근 거부됐다. 현재 release HTML과 1.12.0 작성 소스는 읽었다. | [정확한 3.11 대체 절](https://bioconductor.org/packages/3.11/workflows/vignettes/rnaseqGene/inst/doc/rnaseqGene.html#preparing-quantification-input-to-deseq2) · [1.12.0 archive](https://bioconductor.org/packages/3.11/workflows/src/contrib/rnaseqGene_1.12.0.tar.gz) |
| A13 | 고유 소비자 문서의 멤버와 목적 12/12 중 정확 소비 원판 HTML 해시 일치는 8/12였다. G06/R03/R04/R06은 다른 판의 HTML을 열었고 R03/R04/R06은 고정판 작성 소스도 확인했다. | [고정 036 멤버 목록](https://github.com/laadkke-arch/agentflow-open/blob/5682b0d61a80edc159d4b510d213bbb4c69543be/docs/workstreams/research/AF-RES-036/references.jsonl) · [직접 열람 원장](sources.jsonl) |

공개 발행처 접근이 가능한 동급 환경에서 **R01과 G05의 같은 저장 파일**로 가장 먼저 복제 실행한다. 정확한 locator가 필요한 후속 시도는 원실행과 따로 저장한다. 저장소 루트에서 실행한다.

```sh
git fetch --no-tags origin refs/heads/work/research-af-res-036:refs/remotes/origin/work/research-af-res-036
p=docs/workstreams/research/AF-RES-039
python -B -m workbench.session check "$p/manifest.json" --fetch
python -B "$p/audit.py" --documents-only
replay_out=$(mktemp -d /tmp/af039-next.XXXXXX)
python -B "$p/batch.py" replication --capture-dir "$replay_out/body" --journal "$replay_out/replication.jsonl"
cat > "$replay_out/known-urls.json" <<'JSON'
[
  ["DG-G03-2018", "https://pubs.opengroup.org/onlinepubs/9699919799/mindex.html"],
  ["DG-G05-current", "https://gcc.gnu.org/onlinedocs/gcc/Preprocessor-Options.html#index-MM"],
  ["DG-R01-archive", "https://bioconductor.org/packages/3.11/workflows/src/contrib/rnaseqGene_1.12.0.tar.gz"],
  ["DG-R01-HTML", "https://bioconductor.org/packages/3.11/workflows/vignettes/rnaseqGene/inst/doc/rnaseqGene.html#preparing-quantification-input-to-deseq2"],
  ["SRC-G06-exact", "https://ftp.gnu.org/gnu/gettext/gettext-0.20.2.tar.xz"],
  ["SRC-R03-exact", "https://bioconductor.org/packages/3.11/bioc/src/contrib/Archive/SummarizedExperiment/SummarizedExperiment_1.18.0.tar.gz"],
  ["SRC-R04-R06-exact", "https://bioconductor.org/packages/3.11/bioc/src/contrib/Archive/SingleCellExperiment/SingleCellExperiment_1.10.0.tar.gz"]
]
JSON
python -B "$p/probe.py" diagnostic "$replay_out/known-body" "$replay_out/known-urls.json" > "$replay_out/known-attempts.jsonl"
git show 5682b0d61a80edc159d4b510d213bbb4c69543be:docs/workstreams/research/AF-RES-036/references.jsonl
```

정확 원판 자료가 열리면 G06 `gettext-0.20.2/gettext-tools/doc/FAQ.html`, R03 `SummarizedExperiment/inst/doc/Extensions.html`, R04·R06 `SingleCellExperiment/inst/doc/devel.html`와 `intro.html`의 바이트를 `tar -xOf ARCHIVE MEMBER | sha256sum`으로 확인한다. R01의 이력 멤버는 `rnaseqGene/inst/doc/rnaseqGene.html`다. 3.11 HTML에서 §2의 anchor와 목적을 확인한다. 실제 프로세스 48건을 새로 시작하려면 새 경로에 `batch.py main`을 실행하고 그 시점의 기준을 다시 확인한다. 고정 원장에 새 실행을 합산하지 않는다.

## 원격 저장과 검사

| 단계 | 원격 확인 SHA 또는 실제 결과 |
| --- | --- |
| 범위·입력 봉인 | `52048b3d238966da17c9739639f4619ef2890bd7` |
| 알고리즘·패킷 경계 봉인 | `2982044f4fb1cb7de4b7f239c193f7f95bcf7d40` |
| 48건 원실행 봉인 | `64589b5c9786f7a94d01fe1a37de77bff0e1a35c` |
| 결과·판정·원문·수용 봉인 | `7e7773cdec4c2213d2e81e0094fa5b6e742ec0e8` |
| 결과와 수용 원격 재독 | GitHub에서 고정 결과 SHA의 두 문서 본문을 열었다. Git blob이 로컬과 각각 `b4a96603b798ce35cfedfe57dd13de4e9fe2a9d9`, `9a25fb28d8d588a1c0389ff627804460fa426556`로 일치했다. 코드 재계산에서 표 행 48/4/3, 수용 15/18, 소유 범위 26파일을 확인했다. |
| 개별 계약 검사 | 2026-11-22 19:05:16 UTC, `python -B -m workbench.session check docs/workstreams/research/AF-RES-039/manifest.json --fetch` 결과 SHA의 exit 0, passed, remote_checked. 통합 SHA 및 계약 불변, 범위 이탈 0. |
| 저장소 공통 검사 | GitHub의 같은 결과 SHA를 새로 복제해 `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean`을 실행했다. exit 0, 55+7+9 단위 테스트·demo·export·Git 복원·출처 구조 검사 통과. 자동 manifest 검색은 `no_active_sessions`였으며 이 작업은 위 명시적 검사로 확인했다. |

## 색인용 한 줄

**AF-RES-039 · 12참조 × 2구성 × 2목적의 48실행·24짝 및 고유 원문 33. 현재 목적 각 1/12, 정확 N+H 0/12→1/12, C2 로컬 H 12/12. 제한 egress의 88/94 논리 실패와 15/18 수용 조건을 보존했다. 결과 `7e7773c`와 원격 HANDOFF를 연결한다.**

## 우선순위 약점과 다음 확인

| 순위와 약점 | 영향 | 다음 첫 확인과 결론이 바뀌는 조건 |
| --- | --- | --- |
| 1. CONNECT 거부와 현재 기준 4/12 | 보관 증분의 현재 결정 효과와 1/12 복원의 일반화가 제한된다. | 공개 발행처가 열리는 환경에서 같은 G05/R01 패킷의 원 경로와 필요 절을 다시 얻는다. 다른 구성에서만 맞는 행동이 나오면 현재 결론의 범위를 바꾼다. [실행 영수증](evidence/raw-observations.json) |
| 2. G02의 로컬 H와 독립 H 증명 및 redirect | 같은 정확 출력의 독립 검증·취득비는 미확인이다. | [2.11 README](https://raw.githubusercontent.com/scop/bash-completion/refs/tags/2.11/README.md)와 [2.11 공표 노트](https://github.com/scop/bash-completion/releases/tag/2.11) 두 H 원문을 새 예산에서 직접 검증한다. 양쪽이 같은 정확 출력에 도달하면 비용을 대조한다. |
| 3. 고정 소비 원판 4건과 특정판 목적지 및 서지의 예전 상태 | 읽은 인용과 전 바이트·정정 시점의 증거 범위가 다르다. | [2018 POSIX](https://pubs.opengroup.org/onlinepubs/9699919799/mindex.html), R04/R06 1.10.0 두 멤버, [나고야 NULDL000040](https://da.adm.thers.ac.jp/en/item/n003-20230901-00040)의 날짜 있는 정정 전 레코드부터 확인한다. 실제 해시·원 절·날짜가 독립 관측되면 정확 판 재현 범위를 갱신한다. |
