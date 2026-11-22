# scikit-learn 선정 기록

자연층 첫40, 추가층 첫40 각각 API created asc, number asc. 조회UTC와 검색total은 selection.json. 자연선정은 #25265,#25268(잠정),#25269,#25274; 선정순번2,4,5,8. #25265는 as_frame/return_X_y 등의 데이터 표현 입력 유효성, #25269는 행렬 축소 입력 유효성, #25274는 DataFrame 역변환 검증이다. #25268 본문에는 mixin 예외/whitelist 수정 설명이 있으나 실제 첫 코드가 없어 concrete implementation 적격성까지 미확인이다. 새 PR로 바꾸지 않는다.

추가층 원규칙은 자연층의 IO변경 제한을 중복 적용하여 engine/메모리view를 탈락시켰다. root가 사용자 Q1 원문에 근거해 이 과잉제약을 정정했고, 후속 응답/패치 판독 전에 원순서로 재심사했다. 첫2는 #25535(순번3)와 #25540(순번6). #25531은20inline+4review+13issue-comment에서 작성자/봇을 제외한 URL 없음; #25538은 실제 예제코드여도1inline+2review+1issue-comment에서 URL 없음. #25530 문서설명, #25536 CI설정은 선례 사건의 대상 구현이 아니다. 뒤 순번의 임시선별은 frame.original_rule_status에 보존하며 새 슬롯으로 승격하지 않는다.

## 판독 경계와 우발 노출

- 초기 GitHub 검색과 API raw는 프로그램 메모리에 수신됐으나 status/closed/merged 및 작성자 댓글은 출력하지 않았다. 최초 공개 head를 API의 current head나 surviving commit과 동일시하지 않는다.
- #25268 commits=[], inline=[]였고 current head=base=62a017efa047e9581ae7df8bbaa62cf4c0544ee4. 초기구현 복구 목적으로 timeline의 committed/force-push 메타데이터만 출력했다. 2023-01-04T22:30:47Z force-push가 있었으나 옛 SHA를 이 응답은 주지 않는다. 댓글본문/종결은 읽지 않았다.
- #25275는 자연층 쿼터 뒤 예비 조회에서 preopen commit이 없어 첫 surviving commit을 fallback한 실수가 있었다. author date는1월2일이나 committer date는9월22일인 a1e27d172838449a73ca996b4acc5d6aa14cd0e9의 후대patch를 읽었다. 이를 최초코드/선정/결과 사슬에 사용하지 않는다.
- #25535의 reviewer URL 필터 첫 실행은 모든 URL-bearing reviewer문장을 출력하여 2023-09-01 reviewer의 branch 상태/force-push 제안도 우발 노출됐다. 이는 선정에 쓰지 않으며 원본 최종코드, 작성자응답, merge/close 상태는 여전히 열지 않았다. 이 층의 완전한 결과가림 수용 조건은 미충족으로 남겨야 한다. 이후 필터는 각 endpoint의 첫 URL-bearing reviewer발언만 반환하도록 좁혔다.
- #25563 reviewer의 첫URL이 원 재현코드 시험 결과를 언급했다. 이는 선례제안이 아닌 검증/재현링크로 분리했다. #25579는 현재 body에 tests-only에서 parameter validation으로 고친 후첨 내용이 이미 들어 있었음을 확인했다. 두 행 모두 추가층 첫6안에서 선택한 슬롯을 바꾸지 않는다.
- 자연본문에 원제안자의 시험성공 주장/일반 PR템플릿이 있었지만 후속 결과로 별도 사용하지 않았다. search issue.updated_at은 활동갱신 시각이며 body편집시각으로 코딩하지 않는다. 최초body판 동일성은 모두 미확인이다.

## 다음 행동

root가 frame/selection의 원격 봉인 SHA를 회신한 다음에만 6슬롯의 author응답·review원문·후속commit·종결·노동증거를 판독한다. 부족한 옛 코드/시간은 미확인으로 보존한다.
