# P2 사후 조사: 최초판과 인지·채택을 분리

원 검색 영수증 봉인 `fbc05801af45f21e60d6901f3293f9af9969ef8d` 뒤에만 읽었다. 이 자료는 원 검색의 적중 분자에 추가하지 않는다. 추가 비용은 검색0, 웹 open4, 웹 click1, GitHub 내용 조회12, 합계17회다. SPEC9 Discourse의 두 URL은 접근 실패이고, 성공한 GitHub PR은 그 실패를 대신 성공으로 바꾼 것이 아니다. 커넥터 내부 HTTP 요청 수는 측정하지 않았다.

## 가장 큰 수정: 첫 main과 첫 공개 PR은 다르다

실험 입력은 2024-09-10의 첫 main 병합판 `846579d4`이었다. 사후에 PR323의33개 커밋을 조회한 결과 2024-06-05T00:46:03Z의 [`6ddd0d85` 최초 PR blob](https://github.com/scientific-python/specs/blob/6ddd0d85a8acf184e2e7e35899c0d80af639dc94/spec-0009/index.md)을 확보했다. 해당 [커밋](https://github.com/scientific-python/specs/commit/6ddd0d85a8acf184e2e7e35899c0d80af639dc94)은 이 경로를 added로 기록한다. 따라서 모집 원장의 “first Git addition”은 **main에서의 최초 추가**로 한정해야 한다. 모든 앞선 공개 Git 초안을 조사했다는 뜻으로 쓸 수 없다. P2-D01과 provenance-audit.json이 정정 기록이다.

앞선 초안에도 C1(줄135–138), C2(줄171–173), 역할·권한·기록에 관한 질문(줄54–61)이 있다. 봉인한 질의가 보존한 조건과 행위 주체는 이 판에서도 지지된다. 그러나 최초 PR에는 기업/단일판매자 대안이 있었고 [6월19일 패치](https://github.com/scientific-python/specs/commit/750a088acb40e843817d94f770259618ae6f8222)에서 삭제했다. [다른6월19일 패치](https://github.com/scientific-python/specs/commit/e3d22270629f97ff197389f9e9b40a31e3c0999f)가 Open Source Way를 Notes에 넣었다. OSSWatch의 템플릿 링크는 최초 PR부터 있으므로 OSSWatch 전체를 나중에 처음 알았다고 해석하면 안 된다.

원 모집의 main-first 순번을 소급하여 바꾸지 않았다. PR-first 이력으로 전체 후보의 순서를 다시 계산하지 않았고, summit에서 작성된 Git 이전 파일도 확보하지 않았다. 최초 창설판으로 완결된 모집이라고 주장하려면 이 입력이 남아 있다. 같은 C1/C2라는 사실이 이미 실행한 검색을 창설 초안을 처음 본 실험으로 바꾸지는 않는다.

## Q7: 새로운 자료였는가

| 관측 | 인지 근거 | 아직 모르는 것 |
|---|---|---|
| Matplotlib 전환 사례 | [6월5일 reviewer 제안과 저자 답변](https://github.com/scientific-python/specs/pull/323#issuecomment-2150697486) | C가 반환한 현재 charter의 정확한 규칙을 읽었는지 |
| Jupyter 옛 거버넌스 | [6월19일 저자의 직접 판독 보고](https://github.com/scientific-python/specs/pull/323#discussion_r1646622257) | 옛 문서를 읽은 결과 어떤 운영 방식을 실제 적용했는지 |
| Jupyter2023 전환 발표 | [Ivanov의6월5일 링크](https://github.com/scientific-python/specs/pull/323#issuecomment-2150811435) | 주저자가 그 발표까지 직접 읽었는지 |
| Open Source Way | 6월19일 Notes 추가, 9월 main 입력에 이미 인용 | 6월5일 이전 인지 시점 |

따라서 원실험 C의 책 재발견은 실제 사용한 9월 입력에서 이미 알려진 자료다. Matplotlib이라는 사례 자체도 그 입력 이전에 저자가 인정했다. 정확한 상세 규칙까지 새로웠는지는 미확인이다. 이 구별을 원장의 URL 신규성과 행동 신규성에 유지한다.

[Jupyter 공식 블로그의2023-01-13 발표](https://blog.jupyter.org/announcing-a-new-jupyter-governance-model-and-our-first-executive-council-39b3989dc064)는 이미 일어난 구조 교체와 선거를 당사자가 보고한 원기록이다. 공헌에 대한 인정과 의사결정 권한을 나누려 했다는 동기도 적혀 있다. 이는 SPEC9 이전에 사용할 수 있었던 전환 사례를 확인한다. 같은 구성이 SPEC9에 채택되었거나 효과가 입증되었다는 근거는 아니다. 공개된 투표 집계 스크립트는 열거나 실행하지 않았다.

## 승인은 초안 병합이었다

PR323의9월 리뷰는 명시적으로 초안으로 승인했다. [병합 직전 발언](https://github.com/scientific-python/specs/pull/323#issuecomment-2341907505)과 병합 시각을 연결했으며, GitHub PR의 draft:false와 문서의 is-draft:true를 구별했다. 전자는 PR 인터페이스 상태이고 후자는 제안 문서 상태다.

마지막 변경판 [00fa7c15](https://github.com/scientific-python/specs/blob/00fa7c15c3ada4a1f3ae80559b628c31ce17658f/spec-0009/index.md)도 초안 표시와 빈 endorsed-by를 가진다. 관측된 세 후속 main 패치는 배지·저자 추가, discussion header 제거, 책 링크 교체였다. 배지를 넣는 방법은 실제 채택자가 있다는 증거가 아니다. 이 문서에 채택 기록이 없다는 사실을 전 세계 어느 프로젝트도 사용하지 않았다는 주장으로 바꾸지 않았다. P2-D05/D06이 이 경계다.

## C2를 뒤집는 실제 당사자 관점

원순위에서 유보한 [SciPy2024 토론](https://discuss.scientific-python.org/t/guidance-around-in-person-or-synchronous-discussions/1333)은 사후에만 직접 읽었다. Ralf Gommers는 공개 최종 결정과 비공개 준비 작업을 구분하고, 공개 논의를 거쳐야 결정할 수 있다고 제안했다. 참여자들은 다시 논의할 권리, 유지보수자 시간, 위임된 책임의 필요성을 다르게 평가했다. 이는 모든 준비·논의 기록을 공개하라는 표현과 공개 결정권을 확보하라는 요구가 같지 않다는 당사자 반례다. 토론에서 찬성이 나왔다는 사실로 가이드 채택을 선언하지 않았다.

연결된 [현재 SciPy Core Developer Guide](https://scipy.github.io/devdocs/dev/core-dev/index.html#decision-making-process)는 commit rights를 council이 결정한 뒤 공지한다고 적는다. 승인자와 관찰자는 다르다. 이 현재 가이드가 그2024 토론의 결과로 바뀌었다는 패치는 확보하지 않았으므로 그 인과는 미확인이다.

## 수치·인계

sources.jsonl17행은 이미 모집에서 센 SPEC9 계보의 여러 판·메타데이터와 실패2행을 포함한다. 새로 산입하는 독립 저작은 SciPy 토론, Jupyter 전환 발표, SciPy Core Developer Guide의3건이다. GitHub PR 댓글·47개 review/comment 기록·33개 커밋을 독립 저작으로 부풀리지 않았다. decisions.csv는9행×18열이며 원 선택, 후행 발언, 저자의 인지, 당시 이용 가능성, 문서 채택과 실제 운영 결과를 별도 열에 남겼다.

원실험의 A/B/C 두 조건 적격0은 바뀌지 않는다. 목표 시스템 적용·실행·성과는 미측정이다. 원문 확인자가 재개할 첫 입력은 모든 모집 후보의 최초 PR 추가판 목록이고, 구현자가 재개할 첫 입력은 권한 변경 제안·승인된 판·공개되는 기록을 잇는 최소 사례다. 관리자는 민감한 인선·신고를 포함하는 전체 공개 C2를 유지할지, 공개 결정·이유·요약으로 바꿀지 명시적으로 결정해야 한다.
