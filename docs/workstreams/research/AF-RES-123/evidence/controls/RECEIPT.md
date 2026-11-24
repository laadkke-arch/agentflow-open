# 원형의 대조 입력

입력 커밋 `1001383dd80873e80ceeeb32f0c085050ea53e91`와 봉인 좌표를 사용했다. [환경](environment.json) · [stdout](stdout.txt) · [stderr](stderr.txt) · [종료](exit.txt) · [본행과 대조를 합친 요약](../summary-with-controls.json)

```sh
node docs/workstreams/research/AF-RES-123/replay/drive.cjs --mode controls --engine /tmp/af123-vendor --out /tmp/af123-primary.tDxbMl/controls
python -B docs/workstreams/research/AF-RES-123/replay/analyze.py --main /tmp/af123-primary.tDxbMl/main --controls /tmp/af123-primary.tDxbMl/controls --out /tmp/af123-primary.tDxbMl/analysis-all
```

실행과 분석 종료 0, stderr 0바이트다. 원형의 9가지 대조를 두 렌더러의 두 새 페이지씩 실행했다. 아래 각 결과는 네 페이지에서 같았다. 관측자 해제 4행은 의도한 event 공석이며 hit 비교 분모 밖이다. [시도 원장](../../runs.jsonl) · [관측 원장](../../events.jsonl)

| 대조 | start / first / up에서 가른 것 | 대표 원파일 |
| --- | --- | --- |
| C01 / C02 | x를 100에서 멈추면 May, 바로 다음 x=101에서는 May·Jun. 화면 경계는 예상과 일치했다. | [100](C01-edge-out-svg-1.json) · [101](C02-edge-in-svg-1.json) |
| C03 / C04 | brush 위 click은 [70,170]과 4–9월을 보존했다. 바깥 click은 down에서 [210,210]과 빈 tuple이었다. 두 입력 모두 move는 없다. | [내부](C03-click-in-svg-1.json) · [외부](C04-click-out-svg-1.json) |
| C05 | 내부 역방향 + brush는 [69,169] → [30,130]으로 폭을 보존했다. 끝 enum은 2–7월이다. | [Canvas](C05-reverse-in-canvas-1.json) |
| C06 / C07 | 바깥 역방향의 같은 x 궤적에서 mark (x offset 201)는 [9,8]의 Jan 뒤 빈 tuple, plot은 [210,209]의 Nov 뒤 9–11월이다. | [막대](C06-reverse-out-mark-svg-1.json) · [plot](C07-reverse-out-plot-svg-1.json) |
| C08 | x=110을 고정하고 막대에서 y=6으로 올라가면 unit x offset 101 → 0에 맞춰 [9,9] → [9,110], 1–6월이다. | [SVG](C08-vertical-exit-svg-1.json) · [Canvas](C08-vertical-exit-canvas-1.json) |
| C09 | DOM과 Vega 관측자를 둘 다 등록하지 않아 callback 0이다. 같은 renderer/repeat의 본 empty·mark와 down/first/up extent, enum, fill, 최종 surface SHA가 일치하는지 후속 검산에 포함했다. | [Canvas](C09-observers-off-canvas-1.json) · [대응 본 행](../main/M-original-canvas-empty-mark-1.json) |
