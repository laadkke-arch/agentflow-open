# AF-RES-074 재현 명령과 남은 정확 입력

명령은 저장소 루트에서 실행한다. 실제 작업 checkout은 `/workspace/scratch/3ae3dbdde3fd/agentflow-open`, 허용 출력은 `docs/workstreams/research/AF-RES-074/`다. 셸은 있었고 연구·검사 명령을 직접 수행했다. `evidence/runtime/`와 각 stream의 비공개 캐시는 운송용 산출물이 아니며, 커밋된 입력·출력·해시·receipt만 결과로 사용한다.

## 1. 계약과 구조 검사

실제로 사용한 시작 명령은 아래와 같다. 이미 있는 계약을 처음부터 새로 만든 것처럼 반복하지 않는다. 시작 영수증은 `evidence/session-start.json`, manifest의 실제 base는 `817ee771ebfa63d4a177ee12f46b9818a6335308`이다.

```bash
python -B -m workbench.session start af-res-074 --allow docs/workstreams/research/AF-RES-074/ --dependency work/research-af-res-070=1a92715786d444f57976082329470a24e2a291b6 --output docs/workstreams/research/AF-RES-074/manifest.json --fetch
```

최종 커밋을 checkout한 뒤 구조·봉인·원장·artifact를 확인한다.

```bash
python -B docs/workstreams/research/AF-RES-074/tools/validate.py --require-expanded --actor 'root model in supplied cloud shell'
python -B -m workbench.session check docs/workstreams/research/AF-RES-074/manifest.json --fetch
```

검사자는 자신의 실제 주체를 `--actor`에 적는다. 구조 PASS와 연구 PARTIAL은 동시에 성립한다. 최종 결과 SHA에서 수행한 check의 종료값은 HANDOFF의 별도 영수증을 확인한다. 자동 검사는 최초판 회수 시점을 봉인 전으로 바꾸거나 실제 사람 효과를 증명하지 않는다.

원장·표를 다시 생성하려면 다음 순서를 사용한다. 생성된 파일의 diff를 검토하고 별도 커밋한다. 봉인된 `streams/*/packets-pre.json`, `controls-pre.json`은 바꾸지 않는다.

```bash
python -B docs/workstreams/research/AF-RES-074/tools/build_initial_review.py
python -B docs/workstreams/research/AF-RES-074/tools/build_pre_ledgers.py
python -B docs/workstreams/research/AF-RES-074/tools/build_post_ledgers.py
python -B docs/workstreams/research/AF-RES-074/tools/build_report.py
```

## 2. 최초 요청 원본

원선정8건의 최초판은 모두 사후 회수했다. 아래 URL의 gzip JSONL에서 `type=IssuesEvent`, `payload.action=opened`, repository, `payload.issue.number`, event ID를 함께 확인한다. 다른 시점의 현재 issue body를 원 event로 대체하지 않는다. 원본·현재 해시는 `initial-version-review.csv`에 있다.

| 요구 | 정확한 hour URL | opened event ID |
| --- | --- | --- |
| PAN-N1 /7019 | https://data.gharchive.org/2021-01-11-22.json.gz | 14783471077 |
| PAN-N2 /7022 | https://data.gharchive.org/2021-01-12-7.json.gz | 14787294287 |
| PAN-N3 /7027 | https://data.gharchive.org/2021-01-13-10.json.gz | 14803475608 |
| PAN-N4 /7028 | https://data.gharchive.org/2021-01-13-13.json.gz | 14805657080 |
| GDAL-N1 /3346 | https://data.gharchive.org/2021-01-05-20.json.gz | 14721159701 |
| GDAL-N2 /3378 | https://data.gharchive.org/2021-01-13-19.json.gz | 14810105216 |
| GDAL-N3 /3386 | https://data.gharchive.org/2021-01-15-18.json.gz | 14836481598 |
| GDAL-N4 /3427 | https://data.gharchive.org/2021-02-02-14.json.gz | 15035487168 |

이 표의 URL·ID는 아래 원장으로 모두 기계 대조한다. 완전한 archive에는 연구와 무관한 많은 사건이 있으므로 필요한 issue event만 판독·해시한다. 일반 공개 URL에서403이면 실패 시도를 남기며 인증·프록시 우회는 하지 않는다. 이번에는 뒤 순번 archive가 정상 응답한 뒤 동일 URL의 일반 HTTP 재시도로 회수했다.

```bash
python -B docs/workstreams/research/AF-RES-074/streams/gdal/verify_initial_archives.py
```

Pandoc도 `streams/pandoc/opening-retry-provenance.json`의 정확한 URL·event ID·행 번호를 따라 같은 검사를 할 수 있다. `sources-opening-retry.jsonl`은 같은 issue의 판이므로 새 원저작 수를 늘리지 않는다. 추가 모집 중 GDAL3566은 HTTP200 뒤 gzip EOF로 원문 회수가 실패했다. 그 실패는 메인8건의 복원 성공과 별개다.

## 3. Pandoc2.11.3.2 — 실제 수행했고 다시 실행 가능한 고정판 시험

공식 자산은 `https://github.com/jgm/pandoc/releases/download/2.11.3.2/pandoc-2.11.3.2-linux-amd64.tar.gz`다. 다운로드23,291,353바이트의 SHA256은 `422c1f38b4731edfafcc0f8011a8dc46ce3a84e61b896ef15e3a23e0a9b453d6`, 추출 binary SHA256은 `762b2b574da6b7da29af1cb13eaeb5d3974a92b10e3d7a1e4ff6614ee5ec4d9b`다. release API·도착 호스트/경로·버전 출력은 `evidence/pandoc-release-fetch.json`에 있다. 일회성 공개 다운로드의 서명 query만 생략했다.

고정 source commit은 `dcbd8d326cce4960e0d736e25e7d00f9057a1fc2`다. `evidence/pandoc-fixed-fixtures.json`에는 parse-raw/sloppypar 각각 첫2블록과 empty_paragraphs 첫4블록의 정확 입력·명령·기대 stdout이 있다. 저장된 논리적 텍스트 해시는 final LF를 제외하고, 실제 stdin/stdout 해시는 포함한다.

실제로 수행한 명령:

```bash
python -B docs/workstreams/research/AF-RES-074/tools/run_pandoc_fixed.py --binary docs/workstreams/research/AF-RES-074/evidence/runtime/pandoc-2.11.3.2
```

이미 내려받은 바이너리가 없다면 공식 자산을 owned path 아래에 내려받아 위 두 SHA를 확인하고, 해당 binary 경로로 실행한다. 재실행은 원 영수증을 덮지 않도록 다른 output을 지정한다.

```bash
python -B docs/workstreams/research/AF-RES-074/tools/run_pandoc_fixed.py --binary /absolute/path/to/pandoc-2.11.3.2 --output evidence/runtime/pandoc-replay.json
```

실제 결과는8fixture·12process, 전부exit0/기대 stdout exact match다. 입력·중간 pipeline 해시와 모든 stdout은 `evidence/pandoc-fixed-run.json`에 있다. 새로운 바이너리로 실행하면 버전 검사에서 중지한다. 이것은 오늘 수행한 해당 고정판의 연구자 실행이며 과거 날짜의 upstream CI 영수증은 아니다.

## 4. GDAL 입력·reference·실제3.10.3 출력의 복원

정확한7개 파일은 `evidence/gdal3103-artifacts.json`에 base64로 있다. 원본20×20 `byte.tif`의 SHA256은 `59ed6e9dd19291bbdc230092ab7f6bc46fb0537ee4c9eec15dd58021cd9c12be`, 고정 bilinear reference는 `fbbd267d5c6d5cc0a57e902f81c16fc1123799defa43192680fad88ec99be113`다. v3.2.1 source는 `258d73a17b1f7e93c9cf9b60a2411545d51879de`다.

```bash
python -B docs/workstreams/research/AF-RES-074/tools/restore_gdal_artifacts.py
```

이 명령은 네트워크 없이 해시·길이를 확인하고 `evidence/runtime/restored-gdal3103/`에 복원한다. 다른 바이트의 기존 파일을 덮지 않는다. 입력과 reference는 고정3.2.1 원본이며 `recheck3103/`의5개 파일은 실제3.10.3 실행물이다. 실행 actor·argv·UTC·종료값은 `streams/gdal/researcher-run3103.json`, 픽셀 비교는 `streams/crossfield/audit-root-aggregation.json`을 따른다.

## 5. GDAL3.2.1 — 이번 환경에서 미실행한 정확 명령

현재 환경은 GDAL3.10.3이며 Docker/Podman 실행기가 없다. 아래 명령은 **GDAL3.2.1 실행 환경을 제공받아 수행할 다음 작업**이다. 다른 버전을 대신 실행해 완료라고 표시하지 않는다. 최소 추가 입력은 작동하는3.2.1 `gdalinfo/gdal_translate/gdalwarp` 바이너리 경로와 연결된 PROJ/드라이버 버전 정보다. 현재 결과의 자연 사건 비교에는 PROJ7.2.1 등 사건별 버전도 별도로 고정해야 한다.

다음의 `AF074_GDAL321_BIN`만 실제 경로로 바꾼다. 입력은 위 복원 파일이며 새로운 출력 디렉터리를 사용한다. 이미 파일이 있는 디렉터리를 재사용해 과거 결과를 새 실행으로 오인하지 않는다.

```bash
AF074_GDAL321_BIN=/absolute/path/to/GDAL-3.2.1/bin
AF074_INPUT=docs/workstreams/research/AF-RES-074/evidence/runtime/restored-gdal3103/byte-input.tif
AF074_OUTPUT=docs/workstreams/research/AF-RES-074/evidence/runtime/gdal321-new-run
mkdir -p "$AF074_OUTPUT"
"$AF074_GDAL321_BIN/gdalinfo" --version
"$AF074_GDAL321_BIN/gdal_translate" -a_srs EPSG:26711 -gcp 0 0 440720.000 3751320.000 -gcp 20 0 441920.000 3751320.000 -gcp 20 20 441920.000 3750120.000 0 -gcp 0 20 440720.000 3750120.000 "$AF074_INPUT" "$AF074_OUTPUT/gcp.tif"
"$AF074_GDAL321_BIN/gdalwarp" -ts 40 40 -rn "$AF074_OUTPUT/gcp.tif" "$AF074_OUTPUT/nearest.tif"
"$AF074_GDAL321_BIN/gdalwarp" -ts 40 40 -rb "$AF074_OUTPUT/gcp.tif" "$AF074_OUTPUT/bilinear.tif"
"$AF074_GDAL321_BIN/gdal_translate" -outsize 40 40 "$AF074_INPUT" "$AF074_OUTPUT/pixels.tif"
"$AF074_GDAL321_BIN/gdal_translate" -outsize 200% 200% "$AF074_INPUT" "$AF074_OUTPUT/percent.tif"
"$AF074_GDAL321_BIN/gdalinfo" -json -checksum "$AF074_OUTPUT/nearest.tif"
"$AF074_GDAL321_BIN/gdalinfo" -json -checksum "$AF074_OUTPUT/bilinear.tif"
"$AF074_GDAL321_BIN/gdalinfo" -json -checksum "$AF074_OUTPUT/pixels.tif"
"$AF074_GDAL321_BIN/gdalinfo" -json -checksum "$AF074_OUTPUT/percent.tif"
```

공식 기준은 nearest checksum18784, bilinear는 저장 reference와 최대 픽셀 차이≤1, 크기 두 표현은40×40 및 각checksum18784다. checksum만으로 전체 raster/file 동일성을 주장하지 말고, `tools/validate.py`의 제한된 uncompressed uint8 TIFF 판독처럼 실제 배열·변환·파일 바이트를 별도로 비교한다.3.10.3에서 bilinear checksum19664/reference19694였지만 tolerance1을 만족한 사실이 그 구분의 이유다.

## 6. 자연 사례별 재개 최소 입력

| 요구 | 가장 먼저 필요한 입력·검사 | 아직 주장할 수 없는 완료 |
| --- | --- | --- |
| PAN-N1 | 실제 설치판, 한 Markdown 원고, 최소2개 출력 target, FORMAT filter 구현과 CSS 기대 차이 | 문서 링크만으로 각 슬라이드 형식 CSS dispatch 완료 |
| PAN-N2 | 원 input.md·reference.docx·Word 환경·서양글꼴/중국어따옴표 기대값을 고정; 키 유지가 아닌 결과 제약으로 질문 재정의 | 전역lang 제거나 reference-doc가 두 결과조건을 동시에 보존 |
| PAN-N3 | 정확한 개발 commit·table AST 입력·필요한 표별 옵션·writer 기대 XML | 기존 Table 스타일 링크로 미구현 구조 기능 제공 |
| PAN-N4 | #7028 첨부 Test.doc.docx의 exact bytes, 원 numbering.xml·기대 HTML 번호, Pandoc2.11.2 | 새 연속 번호를 붙이는 것이 원 번호 보존과 같음 |
| GDAL-N1 | 정확 CRS 원문·원 raster·권위 datum/AUTHORITY·보존목표;3.1.4에서 양값 비교 | SetGeogCS 한 호출로 모든 저장 형식의 문자열 보존 |
| GDAL-N2 | 원 .dat/.Hdr의 bytes·파일명·전체 설정과3.2.0 환경; EMPTY_DIR와magic을 별도 요인으로 검사 | magic 값 하나가 모든 파일 열기 실패를 설명 |
| GDAL-N3 | RGB.byte.tif의 exact bytes·권위 datum·GDAL/PROJ/Rasterio 고정판 및 동일판 후보 문서 | 두60% EPSG 후보 중 하나가 독립 정답 |
| GDAL-N4 | 같은 입력·드라이버·3.1.4에서 잘못된 SRS 전후 파일 생성 검사·무잔류 기대 | overwrite 또는 SRS 정의 문서가 실패 원자성을 보장 |

현재8건의 최초판을 다시 모집할 필요는 없다. 계약을 완전히 충족하려면 기존 봉인 실패를 수정한 것처럼 보이게 바꾸지 말고, **새 미노출 입력으로 같은 필드 질문·두 값·같은판 두 후보·허용 지정절을 먼저 봉인하는 별도 반복**이 첫 행동이다. 이번 범위에는 새로운 사람에게 질문하는 실험이 없다.
