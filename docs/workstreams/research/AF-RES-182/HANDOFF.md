# AF-RES-182 HANDOFF — PARTIAL

- 작업자 자체 PARTIAL, 독립 검토 미실시. 중앙 dot-control.json 수정하지 않음. 계획판 `128f673685ec804c526a38e3f89d4d8a43fcd299`, 시작 통합판 `6fa67328360b02bc7e7270d4ad3300bfe0f286bd`, branch `work/research-af-res-182`. 의존 고정판 AF-RES-173 `317d79c74935afae00d1fd4c6b4ea33a840f7fb0`, AF-RES-175 `b36b50399f7851fb785744576f4906e7fdadd963`; 두 HANDOFF 직접 읽음.
- 결과 SHA(자체점검까지의 확정 결과): `43864bce94e7a499c2ff13c7d7baf51d7b1b9c5f`. 이 HANDOFF 자체의 최종 SHA는 GitHub의 이 파일 추가 커밋 응답/branch HEAD로 확인할 것(파일에 자신의 커밋 SHA를 넣는 것은 불가능). RESULT 고정 SHA `7ac9f233e218391ba65c15c929a69b202a4e0d06` [원문](https://github.com/laadkke-arch/agentflow-open/blob/7ac9f233e218391ba65c15c929a69b202a4e0d06/docs/workstreams/research/AF-RES-182/RESULT.md).
- 대표 파일: RESULT.md(3필수 표, Q1~7, 마지막 3 약점), SELF_CHECK.md, sources.jsonl(79행, 36 unique 산입), fixtures.csv(12행/12 tag blobs), observations.csv(12자리), comparisons.md(실제 XML 변화/반례), transfer.csv(3 목적/타분야), frame.csv, SCOPE.md.
- 판정 범위: 공식 2.24.4와 2.26.0 출판 자리 12/12 직접 열람; 11/12 첫 선정 속성 판독 가능, O15 first endpoint 및 O25 supplemental cross-voice 미확인. 02c 실제 출력 3,16,12→3,15,whole-rest,12,3; 같은 첫 3의 glyph 변화. 33b 곡선 동일, 사양은 tie(소리)와 tied(표기) 분리. 태그 full blob 동일 0/6, part-list+parts 단순 정규화 동일 1/6, m1 내부 동일 5/6, 국소 선택 속성·시각 대조 4/6. 엄격 동일 입력 3쌍 미달; 개별 문서 XML bytes join 0/12 (12 미확인, 404/unsupported XML), 신판 standalone PNG 미확보 6/6. PDF 내 독자 figure 내용 10, distinct 원파일 URL 7(엄격 그림 하한 8보다 1 부족). 타분야 원문 10, 실제 distinct 보존/표현 산출물 3, AV 구체 master/access pair 미확인(0 확인). 사양/제작 문서 4 고유 work. 원장 50 읽음/29 실패, 36 고유 산입; 자료/사건/독립 관측 분리. 미확인을 실패로 처리하지 않았다.
- 확인: GitHub 고정 SHA에서 SCOPE, fixtures, observations, comparisons, transfer, sources, RESULT 각각 재열람. JSONL source ID·필드, fixtures/observations 12행, 참조 ID 및 RESULT 끝 약점 3행 검사. 시작 SHA→자체점검 SHA compare: 14 commits, 9개 파일 모두 owned_path 추가만, 중앙 파일 변경 없음. 로컬 git diff --check, 실제 XML bytes, build, 렌더, MIDI/edit 검사는 안 했다.

## 다음 첫 행동 (Codex Cloud, 기존 정상 환경 이용)

먼저 **fixtures.csv의 published_xml_url 12개를 그대로 요청**하고 HTTP 상태/Content-Type/최종 URL/bytes hash를 기록한다. 2.24 old 404와 2.26 XML tool 400을 구별하고, 같은 주소를 무한 재시도하거나 제한을 우회하지 않는다. 실패 시 tag 후보와 문서 원바이트의 미확인을 유지한다. 새 자료의 원문과 실제 출력이 없으면 완료로 바꾸지 않는다. 실행은 이 브랜치에서 scratch 파일을 repo 외부에 보관하고 승인된 owned_path 내 보고서에만 결과 기록. 다음 명령은 아직 실행하지 않았다.

```bash
git fetch origin chore/workspace-foundation work/research-af-res-182
git switch work/research-af-res-182
git log -1 --format='%H %s'
git diff --check 6fa67328360b02bc7e7270d4ad3300bfe0f286bd HEAD
git diff --name-only 6fa67328360b02bc7e7270d4ad3300bfe0f286bd HEAD
python -m workbench.session --help
# 정확한 12개 URL/판/파일명/예상 blob은 이미 fixtures.csv에 고정.
# HTTP 접근이 정상인 환경에서 임시 폴더 사용, 재시도 없음.
export AF182_TMP="$(mktemp -d)"
python - <<'PY'
import csv, os, pathlib, subprocess, hashlib
p=pathlib.Path(os.environ['AF182_TMP'])
f=pathlib.Path('docs/workstreams/research/AF-RES-182/fixtures.csv')
for r in csv.DictReader(f.open()):
    dest=p/(r['source_id']+'.xml')
    ret=subprocess.run(['curl','-L','--fail','--max-time','30','--silent','--show-error','-w','%{http_code} %{content_type} %{url_effective}\\n','-o',str(dest),r['published_xml_url']],capture_output=True,text=True)
    print(r['source_id'],ret.returncode,ret.stdout.strip(),ret.stderr.strip())
    if ret.returncode==0 and dest.exists():
        raw=dest.read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\\x00'+raw).hexdigest()
        print('sha256',hashlib.sha256(raw).hexdigest(),'git blob',blob,'tag match',blob==r['git_blob_sha'])
PY
# 비교는 exact tag checkout의 동일 파일을 사용. 이미 존재하는 공개 upstream checkout 경로를 지정.
# git -C "$LILYPOND_SOURCE" show v2.24.4:input/regression/musicxml/33b-Spanners-Tie.xml > "$AF182_TMP/33b-fixed.xml"
# git -C "$LILYPOND_SOURCE" diff v2.24.4 v2.26.0 -- input/regression/musicxml/
# 두 published PDF의 고해상도 판독(새 빌드 아님):
curl -fL --max-time 60 https://lilypond.org/doc/v2.24/input/regression/musicxml/collated-files.pdf -o "$AF182_TMP/old.pdf"
curl -fL --max-time 60 https://lilypond.org/doc/v2.26/input/regression/musicxml/collated-files.pdf -o "$AF182_TMP/new.pdf"
pdftoppm -f 20 -l 20 -r 300 -png "$AF182_TMP/old.pdf" "$AF182_TMP/old33c"
pdftoppm -f 26 -l 26 -r 300 -png "$AF182_TMP/new.pdf" "$AF182_TMP/new33c"
```

그다음에만 새 렌더 검증: 고정 두 설치의 절대 실행경로와 실제 --version으로 2.24.4/2.26.0 확인, 같은 binary/font/locale 기록. 새 설치나 계정 변경은 하지 말고 없는 경우 보류. 양쪽에서 같은 v2.24.4 tag XML bytes를 input으로 사용하고, 원자료 문서와 별개인 새 실험으로 표시. 33b 외에는 02c,11a를 우선 동일입력 3쌍으로 실험. 각 XML sha256, stdout/stderr, 생성 .ly, PDF sha256, 동일 객체 위치를 남긴다.

```bash
# 전제: L24, L26에 각각 정확 설치의 bin 디렉터리; LILYPOND_SOURCE에는 두 tag 존재.
# 각 version/환경이 고정된 경우만 실행
for exe in "$L24" "$L26"; do
  "$exe/lilypond" --version
  "$exe/musicxml2ly" --version
done
for name in 02c-Rests-MultiMeasureRests 11a-TimeSignatures 33b-Spanners-Tie; do
  git -C "$LILYPOND_SOURCE" show "v2.24.4:input/regression/musicxml/$name.xml" > "$AF182_TMP/$name.xml"
  sha256sum "$AF182_TMP/$name.xml"
  for v in 24 26; do
    if [ "$v" = 24 ]; then bin="$L24"; else bin="$L26"; fi
    d="$AF182_TMP/$v/$name"; mkdir -p "$d"
    "$bin/musicxml2ly" -o "$d/input.ly" "$AF182_TMP/$name.xml" > "$d/convert.log" 2>&1 || continue
    "$bin/lilypond" -o "$d/output" "$d/input.ly" > "$d/render.log" 2>&1 || continue
    sha256sum "$d/input.ly" "$d/output.pdf"
  done
done
```

기대 관측: 02c P1 m1–3 count3 및 m4–18/m19 분리 여부, 11a m1 cut C, m2 C, m3 numeric 2/2 및 m7 system break, 33b P1 F4 m1→m2의 curve endpoints. 새 build가 실제 release PDF와 동일 옵션/출력임은 별도 확인 필요. MIDI/음향은 같은 고정 33b input의 생성 .ly에서 MIDI 생성 조건(실제 버전 musicxml2ly --help) 확인 후 두 F4의 onset/offset, 재발음·duration trace 별도; 편집 객체 검증에는 실제 editable import/export 구현과 버전/도구 필요. 시각 관측을 MIDI 성공으로 간주하지 않음. AV는 T2 공개 accession과 동일 master/접근본 ID+caption/menu 실제 산출물 확보가 다음 자료 조사. T5 원본 raw OCR/image는 T12 접근 가능한 경우에만 별도 확인.

색인 제안: AF-RES-182 PARTIAL — MusicXML→LilyPond 양판 12자리 직접 인쇄 관측, 동일 입력·표기·편집·재생 범위 분리 및 전자책/영상 전이; 엄격 input join/AV pair 미충족.
