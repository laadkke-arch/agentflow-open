# Matplotlib 묶음③ 판독 영수증

예측 원격 봉인 `8054c2221d4023ba03c904d96f13928219d36c3d` 이후에만 새 본문·PNG·source·commit 메시지/diff를 열었다. 이 파일 생성 UTC: 2026-11-24T00:17:54.786470+00:00. 부모만 커밋/푸시한다.

## 입력 불변과 재생

- `stage1-frame.csv`, `frame.csv`, `predictions.csv`, `control-selection.json`, `supplemental-selection.json`, `purpose-axes-before-new-body.json`은 묶음③에서 쓰지 않는다.
- `python -B docs/workstreams/research/AF-RES-106/evidence/matplotlib/stage3_acquire.py`: 고정 본문18판/대표자원 및 download/author source, 보조6커밋 수신. 이 실행은 실제 예제 코드 실행이 아니다.
- `python -B docs/workstreams/research/AF-RES-106/evidence/matplotlib/stage3_followup.py`: 후보10 본문·merge first-parent diff·live version8본문/8PNG를 검사한다. HTTP 실패는 영수증에 유지한다.
- `python -B docs/workstreams/research/AF-RES-106/evidence/matplotlib/finalize_stage3.py`: 보존한 관측·명시적 판독을 조인하여12판자리,6반환자리와 축별 혼동표를 다시 계산한다. 네트워크 없이 실행된다.

## 실측과 제한

원 시각목적: A FN2, G TP1/FP1, M결원2. 일반 역할: A FN2, G TP2, M결원2. 모든 G는 역사생성의 의미에서 미확인. A2의 구체 방법 전체는 NO이나 core API는YES; G2의 원 API패턴은NO이나 offset+bar_label은YES. 이미지눈검사8개, 브라우저/GUI 실행 미실시.

full source bundle522개는 정확 new author path522개 및 blob522개와 일치한다. G2 음성 판정은 문자열·caption·API특징 후보10개 전체 source+본문, 공식2변경diff를 닫은 범위에서만 적용한다. `barchart-successor-candidates.json`은 유사한 AGG 막대코드가 다른 목적이라는 반례도 기록한다.

보조 selected6커밋은3사건,2사건이 주표와 겹친다. 기본 git show의 merge3개 빈 출력은 초기 영수증에 남기고 `--diff-merges=first-parent`로 다시 읽었다. 이는 실패를 성공으로 덮어쓴 것이 아니며 두 영수증을 보존했다. 공식 redirect 별도1개는 scatter_piecharts→scatter_custom_symbol이고 대상 body를 추가 저작으로 세지 않았다.

공개 download의 hash처럼 보이는 디렉터리는 내용 hash라는 보장이 없다. G1/G2는 같은 download 주소에 source bytes/blob이 바뀌었음을 실제 대조했다. 경로 생존과 내용 동일성을 분리한다.

`source-work-map.json`: 보수 admission body9+별계보source3+공식변경3+공식redirect1=16. old-only parser 검증2개와 barchart 공식followup2건은 최소량에서 추가로 세지 않는다. bundle과 member, old/new와1x/2x, 본문과같은example source/PNG는 중복 산입하지 않는다. 원장 `sources.jsonl`은 자동·계승·중복을 포함한 old+new 전체다.

`request-costs.json`: 각 주case postseal 알려진 HTTP 시도/성공/실패/고유URL 집합. tree/Git fetch와 bundle522스캔은 shared. Git의 내부 HTTP 수는 미확인이다. live8URL은 code/DOM/src와 RGBA를 확인했으나2PNG는 metadata제거로byte불일치. 고정SHA의근거는 그대로 유지한다.

검토: 본인 모든 main4쌍 직접 판독. 부모/독립검토 의견으로A2 bbox/default 구체방법과G2 원API패턴/일반핵심을 별도 축으로 작성했다. 독립된 전체4쌍 재판독 범위는 부모의 SELF_CHECK에서 별도로 기술해야 한다.
