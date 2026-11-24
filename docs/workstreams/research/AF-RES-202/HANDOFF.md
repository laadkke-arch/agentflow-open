# AF-RES-202 HANDOFF

## 실제 판정: PARTIAL
- 결과가 든 직전 SHA: `8ac03b53fff79787344ea6c7f4f38688e03cacd2`. 배정 브랜치 `work/research-af-res-202`; 시작 c860f8240ab7b7077e2d5b63e438ddd83ff69a27. 계획판 050278651b11a2a3a49d45baebf41c707c06b700에서 +4, 뒤처짐 0, 통합판 차이 control 파일만. 작업에서는 control 수정 없음.
- 대표: [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/8ac03b53fff79787344ea6c7f4f38688e03cacd2/docs/workstreams/research/AF-RES-202/RESULT.md), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/8ac03b53fff79787344ea6c7f4f38688e03cacd2/docs/workstreams/research/AF-RES-202/SELF_CHECK.md), [models.csv](https://github.com/laadkke-arch/agentflow-open/blob/8ac03b53fff79787344ea6c7f4f38688e03cacd2/docs/workstreams/research/AF-RES-202/models.csv), [cases.csv](https://github.com/laadkke-arch/agentflow-open/blob/8ac03b53fff79787344ea6c7f4f38688e03cacd2/docs/workstreams/research/AF-RES-202/cases.csv), [bundles.csv](https://github.com/laadkke-arch/agentflow-open/blob/8ac03b53fff79787344ea6c7f4f38688e03cacd2/docs/workstreams/research/AF-RES-202/bundles.csv), [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/8ac03b53fff79787344ea6c7f4f38688e03cacd2/docs/workstreams/research/AF-RES-202/sources.jsonl), [frame.csv](https://github.com/laadkke-arch/agentflow-open/blob/8ac03b53fff79787344ea6c7f4f38688e03cacd2/docs/workstreams/research/AF-RES-202/frame.csv), [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/8ac03b53fff79787344ea6c7f4f38688e03cacd2/docs/workstreams/research/AF-RES-202/SCOPE.md), [CONTRASTS.md](https://github.com/laadkke-arch/agentflow-open/blob/8ac03b53fff79787344ea6c7f4f38688e03cacd2/docs/workstreams/research/AF-RES-202/CONTRASTS.md).
- ① 6145440a45b96bc4bb9b80b66204cd56a6f249e3 범위; ② 299cad90a8f859f069df7407180466f6c1790509 원장/모집; ③ 64e2e0829e6f8c74a5ef78792c6bc1760cd2a92b 모델/사건/표 초안; ④ a58e87311a7c5982a951a3ccbc116ef88fc680f0 보강/반례/교차 분야/보정; ⑤ 8ac03b53fff79787344ea6c7f4f38688e03cacd2 RESULT/SELF_CHECK; ⑥ 이 문서 마지막 커밋.
- 자체 검토 후 고정 결과 SHA에서 9개 파일을 직접 다시 읽었다. RESULT blob 5ad0503972bbec5201f4fed1ed36b5963637b9bd, SELF_CHECK 4c6104b3c5e45625aa3fec1ce6f23a8eb940d3b5, sources.jsonl f73a5804c6ca3988cdccaf088c763bd9ae8a2bf4, models.csv 9b3cf0fcce3c1e1c2a6a60f86508fe0a1170ae4a. 3 필수 표 헤더 순서/마지막 약점 정확히 3행, 모델 12·사건 13·조합 9·frame 260·source ID 94 고유·산입 42 확인. 독립 검토 및 로컬 repo check 실행 없음.

## 수확과 부족
- A6(고정 메타데이터 6), B18(정확판 15+공식 live 3), C8(후보 사건 원문 3+동일인 후속 5), D4(배포 목록/패키지), E6(사전 계약/실제 배포 목록) 합계 42/22, 고유 work_id 42, 산입 계보 10. 비산입 52 포함 원장 총 94. C는 원문 수이지 사건 수 아님. S1–3 주표본 후보 3, X1–10 보강 10. 모든 하한은 기록 종류별 산입 수로 충족하나 엄격 최초성/바이너리 판독 조건은 미충족.
- Tesseract 5.3.0과 각 모음 tag 4.1.0 고정. 6/6 exact file metadata, 12/12 model×OEM 자리. 예상 지원 7, 예상 미지원 5. 구성표 직접 판독 **0/6(6 부족)**: raw binary contents 접근 실패/empty result, SHA/bytes와 README만 직접 확인. 실제 고정판 로드 **0/12(12 관측 없음)**. 공개 eng 예시 dump 크기 일치만으로 A03 증명하지 않음.
- ENOENT(C09)와 legacy 오류(C04)는 별개 단계임을 원문으로 연결. 아랍어의 tessdata legacy 제거는 고정 README 명시(B03); 실제 A02 components 불명. 품질 사례(C15–17) 및 다중 언어 일부 실패/출력(C29–30) 구별. 성공 사본 해시+경로 확인 0건. 3 후보 중 S1 OEM 명령 생략(로그 legacy; 후속 0–3), 검색 목록 텍스트 선별에 의존하여 최초성 독립 검증 0/3; 엄격 명시 OEM 기준에 따라 1자리 재모집 가능. 연결 forum 원문 F06 미열람. 사전 raw aff/dic 본문/짝 실행 미확인. 확정 판정으로 승격하지 말 것.
- 제품 설계 제안: 언어팩/모드 필수 구성/목적별 부속/실제 로드 경로를 분리한 후보 링크 조합; 최종 DB/순위 선택 보류. 188의 자산 연결≠선택, 193의 패키징 대안≠목적 충족을 각각 재확인.

## 다음 첫 행동 — Codex 검증용 명령(미실행)

정확 바이너리 6개를 scratch에 받아 blob SHA와 byte 수 확인 후 5.3.0 combine_tessdata로 구성표를 직접 판독한다. 아래는 후속 작업자용 명령이며 웹 조사에서 실행하지 않았다. 설치/빌드/새 벤치마크는 이번 작업 범위에 없었다. 이미 준비된 exact tools만 쓰고 판이 다르면 중단/기록. git hash-object는 Git blob identity, sha256sum은 추가 증거. stdout/stderr/exit, 파일별 구성 목록 및 버전/빌드 근거를 별도 원장에 남길 것. 모델 파일 자체는 owned_path에 커밋하지 않는다.

```bash
set -eu
git fetch origin work/research-af-res-202
git show 8ac03b53fff79787344ea6c7f4f38688e03cacd2:docs/workstreams/research/AF-RES-202/models.csv
git diff --name-only c860f8240ab7b7077e2d5b63e438ddd83ff69a27 origin/work/research-af-res-202
tesseract --version
tesseract --help-oem
# exact 5.3.0 engine/tool build provenance 확인 후 진행; 불일치하면 중단.
tmp=$(mktemp -d)
cat > "$tmp/pins.tsv" <<'EOF'
tessdata 4767ea922bcc460e70b87b1d303ebdfed0897da8 eng f4744c201359d02ced6914c77f0de68ee9bbdd74 23466654
tessdata 4767ea922bcc460e70b87b1d303ebdfed0897da8 ara 42e5c4b387e45f0e54213ce6964543dd6fc6aea0 2494806
tessdata_best e2aad9b983032bb1beff9133104a67cdbb87ca4d eng 176dc3220de7db34d3b3aecbfa42043a6038348b 15400601
tessdata_best e2aad9b983032bb1beff9133104a67cdbb87ca4d ara 4b687c7d54c86cf6219aebe781b47284fd5d41f0 12603724
tessdata_fast 65727574dfcd264acbb0c3e07860e4e9e9b22185 eng bbef4675053b5b468cdb477053e28b1c698ba08e 4113088
tessdata_fast 65727574dfcd264acbb0c3e07860e4e9e9b22185 ara c8d129c67821c1592cac46836686b057ecc203dc 1432056
EOF
while read -r family commit lang blob bytes; do
  mkdir -p "$tmp/$family"
  f="$tmp/$family/$lang.traineddata"
  curl -fL "https://raw.githubusercontent.com/tesseract-ocr/$family/$commit/$lang.traineddata" -o "$f"
  test "$(git hash-object "$f")" = "$blob"
  test "$(wc -c < "$f" | tr -d '[:space:]')" = "$bytes"
  sha256sum "$f"
  rc=0; combine_tessdata -d "$f" > "$f.directory.txt" 2>&1 || rc=$?
  printf '%s directory exit=%s\n' "$f" "$rc"
  cat "$f.directory.txt"
  rc=0; combine_tessdata -l "$f" > "$f.network.txt" 2>&1 || rc=$?
  printf '%s network exit=%s\n' "$f" "$rc"
  cat "$f.network.txt"
  # config가 directory에 실제 존재할 때만 추출해 sublangs 읽기:
  # combine_tessdata -e "$f" "$tmp/$family/$lang.config"
done < "$tmp/pins.tsv"
```

기대 관측은 규칙상 tessdata eng legacy+LSTM, tessdata ara LSTM only, best/fast eng·ara LSTM only; 실제 목록이 다르면 가설을 수정하고 old/new+근거 커밋. legacy 빌드 여부와 내부 unicharset,inttemp,pffmtable,normproto / lstm,lstm-unicharset,lstm-recoder를 각 파일에서 직접 확인한다. 선택적 config/DAWG와 필수 항목을 구별.

후속으로 명시 승인된 실행 검증에서만, 각 언어별 고정 PNG(영어/아랍어 한 개씩, 이미지 SHA256 및 원문/출처 저장)를 입력으로 아래 반복. 예시는 입력 경로 변수이며 현재 제공된 실제 파일이 아님; 고정 입력을 확보하기 전 실행 금지. OCR 정확도 비교를 하지 말고 초기화/로드·fallback·출력 유무만 기록. 실패 포함 12개 stdout/stderr/exit. 가능하면 read-only strace openat 로그로 실제 loaded pathname도 수집. 정확 엔진 빌드 및 각 data directory의 hash manifest와 로그를 결합한다.

```bash
# ENG_INPUT=/absolute/path/to/pinned-eng.png
# ARA_INPUT=/absolute/path/to/pinned-ara.png
# sha256sum "$ENG_INPUT" "$ARA_INPUT"
for family in tessdata tessdata_best tessdata_fast; do
  for lang in eng ara; do
    case "$lang" in eng) img="$ENG_INPUT";; ara) img="$ARA_INPUT";; esac
    for oem in 0 1; do
      base="$tmp/$family/$lang-oem$oem"
      rc=0
      tesseract "$img" stdout --tessdata-dir "$tmp/$family" -l "$lang" --oem "$oem" --psm 3 > "$base.out" 2> "$base.err" || rc=$?
      printf '%s\n' "$rc" > "$base.exit"
      # strace -f -e trace=open,openat -o "$base.open" tesseract "$img" stdout --tessdata-dir "$tmp/$family" -l "$lang" --oem "$oem" --psm 3
    done
  done
done
```

엄격 모집 재검증: L1/L101/L201 원 검색 목록에서 cutoff까지 원본문을 한 건씩 재판독(특히 #2888, #2872, #2927; 초기화 오류/품질 및 명시 mode 구분). 새로 적격 발견 또는 S1 탈락 시 2020 후속 페이지 L202, 이후 2021–25 연도별 날짜순 양 저장소 목록을 합쳐 최초 3 확정. GitHub 공개 API 예시(읽기 전용, 기존 도구/접근만):
```bash
for repo in tesseract tessdata; do
  gh api --method GET search/issues --paginate -f "q=repo:tesseract-ocr/$repo is:issue created:2020-01-01..2020-12-31" -f sort=created -f order=asc -F per_page=100 > "$tmp/$repo-2020.json"
done
# 각 적격/근접 사례:
gh api repos/tesseract-ocr/tesseract/issues/2927
gh api repos/tesseract-ocr/tesseract/issues/2927/comments --paginate
```
동일 작성자·실제 수정 파일·경로·output으로만 확인. 결손이면 유지. E02/E03 파일 목록에서 배포 원패키지/실제 aff/dic 파일 본문 및 variant 호환 근거를 직접 확인. F06 원문 접근 재시도. 외부 동시 과제는 필요 없음.

## 색인 반영 제안
PARTIAL 연구 자산으로 AF-RES-202 RESULT/SELF_CHECK/models/cases/bundles 링크 및 42 산입·6/6 metadata·0/6 component·0/12 runtime·3 후보 사건을 색인에 추가할 것을 제안. 데이터 구조 후보와 반례 링크 활용 가능, 완료 카운트/지원 판정 확정은 금지. 중앙 색인이나 dot-control.json 직접 수정하지 않았다.
