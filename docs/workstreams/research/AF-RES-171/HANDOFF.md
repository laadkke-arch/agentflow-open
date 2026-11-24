# AF-RES-171 HANDOFF — PARTIAL

## 실제 상태
- **PARTIAL**. WCAG 자연 여섯 처분·문구 및 공개 반환 댓글 33개 모두 판독, 원제출자 후속 0(한 명의 원제출자; 미인지/동의/이의 모두 확정 불가). XPath 마지막 CR 여섯 원번호 모집 자체가 미완; 이전 회차와 PR 의견을 넣지 않았다. 12자리 중 6 처분 관측/6 미확인, 원제출자 입장은 12/12 미확인(6 공개 회신 없음, 6 접근/모집 미완).
- 보충 W774/W803 명시 답변 만족, W805 닫힘과 병존 이견, W806 원제출자 부분 수용·제3자 재개 요구, X30007 구체 표현 동의. 동일인 X30006의 다른 답변 및 마지막 CR 시점에 잘못 붙이는 가설 직접 기각. 학술 eLife 저자 응답·도시계획 기관의 특정 이의 철회/대표권 구분. 최종 절 링크·편집 처분·원회신은 각기 다른 질문의 근거이며, 회신 없음은 자동 동의 아님.
- 보수적 최소 고유 원자료 22/22 및 범주별 4+8+6+2+2 충족 (보충 포함, 완전 자연 모집 대체 불가). 출처 171행, 산입 99 고유 작성 저작, 96 URL, 30 관측 계보 버킷(통계 독립 아님); 접근 실패 20행. frame 120, comments 25, replies 83, advice 18. 일부 반복 열람/시도 1:1 로그 불완전, 당시 답변 draft와 후속 문서 전수 미완. 도시계획 PDF 대상 행 텍스트 추출, Winchester 해당 페이지 이미지 403. 자기점검만; 독립 검토/checkout/CI 미실시.
- 소유 경로만 수정; 중앙 dot-control 미수정. DB/검색엔진/Studio 연동은 후속 설계자에 유보.

## 입력·결과 고정점
- 계획 기준 53eaa286136019510f052179f5f51d901bdac858; 시작 chore/workspace-foundation 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc (ahead 2; 차이는 dot-control). 전체 JSON content API 빈 반환으로 시작 diff에서 AF-RES-171 배정 확인.
- 의존 AF-RES-163 360d971487259cb22496406fd3ef71e0654340c1 HANDOFF (중앙 DONE은 배정문, 고정 인계문 self PARTIAL). 선행 발신 35와 원 제출자 같은 통지 인지 행동 1 구별.
- ① b3a65c0da1ecbf568c032717561a94c890d147f9 범위·판정 선고정
- ② e7ee933d2e91f7168e3147a0c9392d8ed903b734 모집·출처
- ③ 6159ec4b10ae18f89032554cf3eea7dacbb3c9f3 주 관측
- ④ f246091edbe1f546a38b15fd01abcd1d3b562a1c 반례/분야 비교/질문별 주장
- ⑤ 331a0bd8bcf04af8f40d34409ce9eddf2ee265a8 결과/자체점검 및 자연 댓글 귀속 보정
- **결과 고정 SHA 2ace3010d630021286e1ee8200869d70d31fcb3c** — ⑤ 추가 보정: 복합 참조 S21;S22 분리 검사 시 누락 0, source ID 2곳 정정. 대표 파일 원격 재열람 확인. HANDOFF 자체 commit SHA는 커밋 이후 branch metadata에서 확정(자기참조 불가).
- 대표 파일: [RESULT.md](RESULT.md), [SELF_CHECK.md](SELF_CHECK.md), [SCOPE.md](SCOPE.md), [frame.csv](frame.csv), [sources.jsonl](sources.jsonl), [comments.csv](comments.csv), [replies.csv](replies.csv), [advice.csv](advice.csv).

## 첫 재개 행동
1. XPath 최종 CR 2016-12-13~2017-01-10에 실제 해당하는 공개 disposition/전환 요청 또는 W3C Bugzilla 퇴역 보관판의 XPath/XQuery/XSLT 제품별 issue 목록 원본을 발행자 공개 주소에서 찾는다. 이미 실패한 제품 경로 https://www.w3.org/Bugs/Public/describecomponents.cgi?product=XPath+%2F+XQuery+%2F+XSLT ; 확인한 월별 https://lists.w3.org/Archives/Public/public-qt-comments/2016Dec/ 와 https://lists.w3.org/Archives/Public/public-qt-comments/2017Jan/ 의 9+14 창은 제목·날짜 스크린에 그친다. 원번호 목록과 전체 수·누락 확인 전까지 X-slot1~6 유지; 30006/30007은 이전 CR, 30050/51은 PR이므로 제외. WCAG는 공식 전체 전환/처리표 접근 또는 공개 archive와 GitHub 81행 crosswalk 확인.
2. 모집 확정 뒤 동일 의견 ID 원문·처분·회신 메시지 ID·전후 절/판 목록을 고정한다. W752–757의 공개 외부 회신, W805 4/12 이후 같은 통지 응답, W806 #852/#853 및 후속 판, 도시계획 signed/adopted 판은 해당 원문만 확인. 비공개·로그인 우회 금지.
3. 다음 검사는 Codex Cloud가 원 입력을 확보한 뒤 수행(웹 작업자 실행 미실시). 입력: repo, branch, 이 결과 SHA, 위 owned path CSV/JSONL, 공개 처리표 원문과 (round_id,comment_id,original_actor,message_id,target,utc,section_anchor,version) join 목록. 명령:
```sh
git fetch origin work/research-af-res-171
git show 2ace3010d630021286e1ee8200869d70d31fcb3c:docs/workstreams/research/AF-RES-171/SELF_CHECK.md
git diff --name-only 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc 2ace3010d630021286e1ee8200869d70d31fcb3c
python - <<'PY'
import csv,json,pathlib,collections
p=pathlib.Path('docs/workstreams/research/AF-RES-171')
sources=[json.loads(x) for x in (p/'sources.jsonl').read_text().splitlines() if x]
ids={s['source_id'] for s in sources}
for name in ['frame','comments','replies','advice']:
    with (p/(name+'.csv')).open(newline='') as f:
        rows=list(csv.DictReader(f)); print(name,len(rows))
        if name=='replies':
            print('broken_refs',[(r['reply_id'],v) for r in rows for v in r['source_id'].split(';') if v.strip() not in ids])
        if name=='comments':
            print('natural',[(r['event_id'],r['original_position']) for r in rows if r['layer']=='natural'])
print('source_rows',len(sources),'works',len({s['work_id'] for s in sources if s['count']}))
PY
```
원본 확보 후에만 전체 목록과 원장을 번호·회차·메시지 ID로 비교, 끊긴 조인을 집계한다. 당사자 동의의 내용 판단은 텍스트 직접 판독 기록으로 검토해야 하며 자동화가 대체하지 않는다. 위 검사는 checkout 경로가 해당 SHA일 때 수행; 여기서는 실행했다고 주장하지 않는다.

색인 제안: AF-RES-171 — 표준 의견 편집 처분/절 변경/원제출자 인지·동의를 역할·회차·대상으로 분리; 자연 WCAG6/12, XPath 모집 6 미확인, 보충 반례와 타 분야 비교, PARTIAL.
