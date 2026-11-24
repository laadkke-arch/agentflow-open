# AF-RES-230 HANDOFF
**자체 상태: PARTIAL.** 자료수/순서/산출물 충족; 지명 두 원작성자의 후속 핵심 증거 없음, 최초 body revision 4건 모두 미확인, 실제 PCM 검증 0. 완료율이나 가림 성공률로 바꾸지 말 것. 웹 조사·설계 역할, 독립 검토 및 Codex 실행 미실시.

## 고정 결과와 작업 경로
- 통합 착수: 610bcdf35a3dc04bc7f55ce1ecf0a339d9d881e6. 요청판 914dbfa789ebec97063ed97130ea2a71c2e9f503 대비 6 commits ahead, dot-control만 변경; 230 배정 추가. 의존 219 고정 a2fdcb7da07d9d278fb038dd54d3699d05f946a8 중앙 DONE이나 자체 PARTIAL 그대로. 227–229 불필요. branch work/research-af-res-230.
- ① 최초 body만 보고 예측 봉인: 2dd710ad319633c68df5ff37d566c3468e4dfba9 (2026-11-24T23:02:20Z). ② 원장: d0bcce7cd4bc0494c3ff5d248454a8b7893b3e40. ③ 표/주관측: e740c12c1d2fe2a94f90b35f1c29ecf5fa4127be. ④ 반례/정정: d638a9c11870d949568f22cf6e5f2691296e1f68. ⑤ 결과/점검: a166c79fc1b53cc28582db5a79c26fe94e5069c5, 원장 그룹 집계·공통 노출시간창 정정 추가 커밋 **cb0cb98c87060f10be7f890caa1a5c736540235c**. 이것이 결과 고정 SHA이며 이 HANDOFF는 그 다음 단독 커밋.
- 결과 SHA 원격 재조회 검증 완료: 9개 필수/추가 파일(SCOPE, first-posts, first-routes, sources, followup, examples, counterexamples, RESULT, SELF_CHECK), 두 필수 표 exact header, Q1–Q7 7 headings, 마지막 약점 표 3행, JSONL 66행 전필수 키, 36 고유 포함 work IDs/19 lineage IDs, CSV first-posts 4/followup 19/examples 13 data rows, first-routes blob 981936514bb1ef93dc9de017982e5b548ceb204f. integration→결과 compare ahead 6 behind 0, 변경 9개 모두 owned_path, dot-control 미변경, branch head 일치. GitHub read/JSON/schema/경로 대조로 한정, 저장소 checkout/CI/test 실행 아님. ③ 최초 create_commit 인수 스키마 오류 뒤 재시도 성공; 최종 집계 other Audacity 20 오기→18 정정(4+6+18+4+4=36).
- 대표 파일 [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/cb0cb98c87060f10be7f890caa1a5c736540235c/docs/workstreams/research/AF-RES-230/RESULT.md), [first-routes.md 봉인판](https://github.com/laadkke-arch/agentflow-open/blob/2dd710ad319633c68df5ff37d566c3468e4dfba9/docs/workstreams/research/AF-RES-230/first-routes.md), [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/cb0cb98c87060f10be7f890caa1a5c736540235c/docs/workstreams/research/AF-RES-230/sources.jsonl), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/cb0cb98c87060f10be7f890caa1a5c736540235c/docs/workstreams/research/AF-RES-230/SELF_CHECK.md), examples.csv/followup.csv.

## 판정과 새 발견
지명 4/4 현행 단건 REST body 선판독, 최초 공개 revision 0/4. 2 즉답·2 조건부 링크·0 질문 우선. 후속 원작성자 2/4: #4811과 #5302는 첫 경로 유지(재시험 진술, 파일 검증 아님); #3402/#5797 동일인 후속 없어 판별불가. 반전 0, 실제 질문 응답 0, 지명 audio artifact 0. 원장 66 records / 36 included distinct works: issue4; forum4 지명+2 보강; other Audacity18; Ardour4; Inkscape4. topic 시작 독립 사건 10, 후발 별도 사용자 3 추가; 19 lineage IDs는 독립 실험 횟수 아님. 
핵심: 단위(track/clip/label range), 경계 제공자(top label/selection), 소리 선택(mute/solo/selectedOnly), 시간 원점(project zero/clip local), end basis, 채널·파일명·tag를 분리. 먼저 단위가 명시되었으면 묻지 않는다. stem 정렬 vs 곡별 시작은 trim의 다른 값, 같은 절일 수 있으므로 무조건 질문이 아니라 두 옵션 설명. F01/F03 vs F05 실제 반대 의도, F06 원래 offbeat로 질문 무용. 3.4.2 PCM E02→E07→E06→E04는 lower audio도 eligible, M01 위쪽만 설명 및 M03 selected muted 문구와 불일치; 3.5.0 channel UI 달라짐. F04 공개 PDF title과 artist/album 분리 확인, PCM 미확인. V01 checked 화면은 default 아님. 
중요 약점 3: (1) 원작성자 후속 2 결측·최초 revision 부재; (2) 고정 PCM code와 매뉴얼의 content 범위 충돌; (3) #4811 alpha short 422 및 2.3.3 regression/실제 retest 파일 없음. RESULT 마지막 표를 유지.

## 다음 첫 행동 / 실행 인계
1. 우선 #3402/#5797에서 **동일 작성자**의 추가 공개 발언 또는 edit history를 찾아 ID·시각·범위를 보존한다. GitHub UI edit history가 없으면 최초 revision 미확인 유지. 타인(#6034, plugin, #1552 등) 자료는 별도 사건/제품 증거. 2e235de·796e0db REST 422의 전체 SHA/공개 alpha build log 확인; short SHA 추측 금지. 
2. 실제 실행 담당(Codex)에게 아래 **입력과 기대/반전 조건**을 인계. 사용자가 승인한 기존 실행환경에서만 수행; 설치·유료 API 필요 시 별도 승인. 이 작업자에서는 명령 실행/DAW 설치/CI/독립 검토하지 않았음. checkout에서 결과 검증:
```sh
git fetch origin
git checkout --detach cb0cb98c87060f10be7f890caa1a5c736540235c
git diff --name-only 610bcdf35a3dc04bc7f55ce1ecf0a339d9d881e6 HEAD
git show 2dd710ad319633c68df5ff37d566c3468e4dfba9:docs/workstreams/research/AF-RES-230/first-routes.md
python -m json.tool --help
```
JSONL은 줄별 json.loads로 읽고 included true의 work_id distinct, lineage distinct, prefix group 4/6/18/4/4를 재계산. workbench.session/CI는 환경 규칙·실제 manifest 확인 뒤 실행; 기존 manifest 수정/공용 경로 쓰기 금지. 
3. Audacity exact source pins E01 3.3.3=43981edbdd8a1d9da0cf79a07ba694ad79cb7b47, E02 3.4.2=9dd60f25c6cd271879756ea57fd67e582fe17d91, E03 3.5.0=54275321175a6d796953e4bb47bfb6775535d276. `git ls-remote --tags https://github.com/audacity/audacity.git`에서 2.3.3/2.4.0 exact tag/peeled SHA 확인. 5305 merge/parent diff:
```sh
git clone https://github.com/audacity/audacity.git /tmp/af230-audacity
cd /tmp/af230-audacity
git show 425128b2a1846e7b039dac62e89438a9bbbf8a03 -- src/export/ExportAudioDialog.cpp
git checkout --detach 9dd60f25c6cd271879756ea57fd67e582fe17d91
```
checkout만으로 실행 성공 아님. 각 정확판 binary/build about 및 clean preference 기록. Old File > Export > Export Multiple; new File > Export Audio > Multiple Files. 44.1kHz PCM signed16 WAV, no effects, default pan center, tracks unmuted. 아래는 시험 fixture 생성 예시(실행 전용 작업 폴더).
```python
import math, struct, wave
for name,freq,seconds in [('A.wav',440,4),('B.wav',880,3)]:
    with wave.open(name,'wb') as w:
        w.setparams((1,2,44100,0,'NONE','not compressed'))
        data=bytearray()
        for i in range(44100*seconds):
            value=10000 if i==0 else round(10000*math.sin(2*math.pi*freq*i/44100))
            data.extend(struct.pack('<h',value))
        w.writeframes(data)
```
Import A at 0, B move clip precisely to 2s using Selection/clip time controls; confirm project end 5s and offset by screen. Export Tracks trim off→A 176400 frames, B 220500 with first 88200 blank; on→B 132300, first sample near 0 (resampling/dither may introduce low-level noise; use amplitude >100 as onset threshold, report sample rate and channel count, disable dither if testing exact zeros). Same project 0 ≠ same end. If onset/length not expected, revise E02 static inference, capture exact version/preferences.
C2 keep A/B, top point labels 1/3s, lower region 2–4s, place one WaveTrack above and other below top label. Select only lower label and export Labels; count 2, durations 2s each; 880Hz detectable in overlap under code prediction, M01 predicts below-label absent. Swap label order only→one 2s file; mute B→880 absent, count unchanged. Test include-before on/off with first label 1s, clean defaults; test selected muted Current Selection and stereo/panned mono 3.4.2 vs explicit channel UI 3.5.0. Compare #5302 before/after 5305 (actual binaries, note exact parent if available), files should contain individual frequencies rather than mix. F03 compare 2.3.3 and 2.4.0, both pref states. 
```sh
python - <<'PY'
import glob,wave,struct
for f in glob.glob('*.wav'):
    with wave.open(f,'rb') as w:
        n,c,s=w.getnframes(),w.getnchannels(),w.getframerate()
        if w.getsampwidth()!=2: print(f,'not signed16 PCM'); continue
        x=list(struct.iter_unpack('<h',w.readframes(n)))
        onset=next((i//c for i,v in enumerate(x) if abs(v[0])>100),None)
        print(f,n,c,s,onset)
PY
ffprobe -v error -show_format -show_streams output.wav
ffmpeg -v error -i output.wav -map 0:a:0 -f s16le - | sha256sum
```
FFT/Goertzel on same overlapping 2–3s interval compare 440/880 magnitudes; report threshold, channels and raw result, not mere binary success. C3 export same PCM twice changing only metadata title/artist; record `ffprobe` fields and decoded PCM hash. If title auto-overwritten, test artist field; if hash differs, check dither and channel/format before causal judgment.
4. Ardour exact installed version via About, session same A/B span 0–5, Export Stems or Export dialog, unprocessed/processed and profile trim/padding separately (A01–04). Report file name/rate/channels/duration/timecode and offsets, compare trim disabled vs enabled. Do not assume profile interaction. Inkscape exact installed version, fixture SVG page 600×600 (96dpi), triangle target x120 y120 bbox100×80, overlapping rect object separate. 
```sh
inkscape --version
inkscape --query-all fixture.svg
inkscape fixture.svg --export-type=png --export-area-page --export-filename=page.png
inkscape fixture.svg --export-id=target --export-filename=object.png
inkscape fixture.svg --export-id=target --export-id-only --export-filename=object-only.png
```
If options not supported check installed help; no assertion of run. Compare page 600×600 vs bbox100×80 and overlapping pixel differences. --export-id-only may change compositing; if output includes/excludes other object unexpectedly, revise Q6. Code/GUI tests should write separate allowed Codex task path, not mutate sealed first-routes.md.

## 색인 반영 제안
운영자가 230을 PARTIAL(자체 증거)로 색인할 것: audio export unit × range origin × content selection × naming/tag; 4/4 current-body isolated before seal, same-author 2/4, 36 works; 3.4.2 document/code contradiction unresolved, runtime pending. 결과 SHA cb0cb98c87060f10be7f890caa1a5c736540235c. 이 세션은 dot-control을 수정하지 않았다. 다음 계획은 운영자가 결정.
