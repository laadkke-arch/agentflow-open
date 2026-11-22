"""Render the 24 fixed first screens without importing hidden-member facts."""
import json
from pathlib import Path

P = Path(__file__).resolve().parent.parent


def clean(s):
    return str(s).replace('|', '\\|').replace('\n', ' ')


lines = ['# AF-RES-040 — 고정된 첫 화면 24개', '',
         '각 표는 3행, 채워진 행마다 원문 직링크 1개, 설명 80자 상한이다. '
         '대표가 같은 경우 제목·설명도 같다. 이 파일은 `views.jsonl`의 표시 필드만 렌더링하며 '
         '숨은 멤버의 사실을 카드에 보태지 않는다. 빈칸도 예산에 포함한다. 실제 사용자 클릭·채택 관측은 아니다.', '']
for raw in (P / 'views.jsonl').read_text().splitlines():
    v = json.loads(raw)
    lines += [f"## {v['case_id']} / {v['arm']}", '',
              '| 자리 | 제목 | 설명 | 원문 직링크 | 설명 글자수 / 상한 |',
              '| --- | --- | --- | --- | --- |']
    for c in v['cards']:
        if c['empty']:
            lines.append(f"| {c['position']} | 빈칸 |  | — | 0 / 80 |")
        else:
            lines.append(f"| {c['position']} | {clean(c['title'])} | {clean(c['description'])} | "
                         f"[{c['candidate_id']}]({c['direct_links'][0]}) | {c['description_length']} / 80 |")
    lines += ['']
(P / 'evidence/CARDS.md').write_text('\n'.join(lines))
print(json.dumps({'views': 24, 'card_rows': 72, 'output': 'evidence/CARDS.md'}))
