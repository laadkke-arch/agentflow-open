# AF-RES-136 인계

**상태: PARTIAL.** 18개 보존 답의 가림 판독 및 두 봉인, 해제 후 원 평가·후속 작성자 발언 대조, 결과표·검산을 커밋했다. 다만 2차 판독 선노출, 일부 타 분야 원전 부족, checkout 검사의 미실시를 완료로 포장하지 않는다.

- 저장소/브랜치: `laadkke-arch/agentflow-open` / `work/research-af-res-136`
- 유일 쓰기 범위: `docs/workstreams/research/AF-RES-136/`. 중앙 `dot-control.json` 및 제품 코드는 수정하지 않았다.
- 실제 시작 기준 SHA: `67eb3c65404bf70de554bee6eb4c126344a3cd4a` (계획 기준 `42260ca230e028e1303667be943b861a1d5953e4`).
- 고정 의존: AF-RES-132 인계 `510e9db7742ea2edc09c17d0fd4e3e8fbf48ca49`, 보존 결과 `99be7bebb9561756fea04621120dd020cecf40b3`; AF-RES-128 패킷 `3c8a3cf52c84cd9a8c5a06421087733bb8319e6b`.
- 결과 고정 SHA: `a081ca3d619c6aa6676cd1ec9d8e8a33bb739ebb` (RESULT.md 및 원장). 원격 재검산 SHA: `0846afafa2c54350979a9925019e7800e9f8a1f6`. SELF_CHECK 최종 SHA: `32b5989bae6abb332c333fa8c009ee53f2dc45b1`. 이 인계는 마지막 별도 커밋으로 추가한다.

## 묶음별 고정 위치

| 묶음 | 경로 | 커밋 / 확인 |
|---|---|---|
| 사전 규칙 | SCOPE.md | `f33ee9a8c35485371dc803d443e8ccdefa464d4a` |
| 투영 및 합성 검사 | projection/protocol.js, projection/preflight.json | `4a991cf7c7dced08676a2de16901c360d6480162`, `947984f5e62a91d9dde5e5ed074f9a57f5364d0d` |
| 원요구 | requirements.csv | `1cbd0b7617f41a91b1b8daf388299a9103d11360` |
| 1차 봉인 | blind-ratings.jsonl | `c748c9332501c6c89fa547a8db609f56c6456d5c` |
| 2차 봉인 | support.csv, evidence/second-seal.json | `ffc28399ab12b8f46de6d6641314814bda36999f`, `05a346424a3e1a2ed181a10075d9a58516eb7de4` |
| 해제 | projection/unsealed-map.json | `187bf2b56d743d66146fd88967c1b467a5689b0e` |
| 원작성자·대조 | evidence/postrelease-issues.jsonl, concordance.csv | `32abdc34f2b71abdc5d36be441f48445c048380b`, 대조표 고정 재열람판 `a081ca3d619c6aa6676cd1ec9d8e8a33bb739ebb` |
| 타 분야·원전 원장 | sources.jsonl | `0dcf1999d12f11ef8c67e61bdb312bb7c826a9cc` |
| 필수 표·결과 | RESULT.md | `a081ca3d619c6aa6676cd1ec9d8e8a33bb739ebb` |
| 원격 검산·자기검사 | evidence/remote-recheck.json, SELF_CHECK.md | `0846afafa2c54350979a9925019e7800e9f8a1f6`, `32b5989bae6abb332c333fa8c009ee53f2dc45b1` |

## 결론과 검증 범위

- 입력 결합 6사건×3답=18/18, 원행·4필드 길이 및 해시 일치. 요청 33절을 별도 기록했다. 합성 3단계·중복 슬롯·중복 패킷 거부 검사와 SHA-256 알려진 값 검사, 원격 재투영 배정/요청/답 해시 일치.
- 첫 봉인 SHA-256 `b7a3d23d131107fb31e63dd28860820e19815d2159ecb3f0ee145e0fc83f2afa`; 둘째 봉인 SHA-256 `7b43b7e244cb907a9bb14f0e4d8d41f40dc32295e9f8d5ecf80ad66735d4c026`. 두 봉인을 커밋한 뒤 선행 점수·인계·결과를 개봉했다. 봉인 전 원답의 F/둘째 면 등 자체 단서와 반복 인지는 제거하지 않았다.
- 1차 답 18개: 제안 수준 충족 3, 조건부 12, 불명 3. 이는 실제 실행·채택·핵심 조건 해결 건수가 아니다. 6사건의 최종 확정 핵심 해결 0/6. b→c: 좁은 근거 보강 3, 검사 구체화 1, 조건부 대안 1, 변화 없음 1. 원 평가와 사건별 핵심 유보 6/6 일치하나 세부 판정 차이는 보존했다. 좁은 지지와 핵심 해결을 합치지 않는다.
- 2차 장부 22행(무면 6, 답-면 연결 16), 당시 열람 이벤트 10개/고유 본문 9개. 원격 도구 내 예비 결합에서 face_count 누락·라벨 충돌로 뒤 단계 면을 선노출했다. 이후 이벤트 cutoff로 재결합한 결과만 장부화했으나 노출 자체는 취소할 수 없으므로 2차 판독은 오염 가능 층이다. second-seal의 서술상 8은 오기이며 구조 필드 및 재검산의 9를 따른다. 앞선 답 12개 반복 인지 제외 시 현 판독의 완전 비교쌍 0; 원 독자 쪽 P2 반복 제외 5사건과 뒤늦은 조건 제외 2사건은 별도 감도 표를 참조한다.
- 직접 원전 원장 41행, 열람 29행, 실패 11행, 목록만 1행. 적격 고유 work_id 25(보수적으로 CPython 구현 파일 통합 시 24), 원질문 6/6, 정의·구현 8/6, 별도 시험·예제 6/6, 서지 3/3, 음악 2/3. 마지막 범주 부족 및 1872년 비교판 이미지 미열람 때문에 총량만으로 DONE 판단하지 않는다. 원질문 6건과 댓글 19개를 봉인 이후 열었다. 댓글 최초 공개시각/편집 이력 및 PR2624 병합 직접 검증, 원작성자의 실제 채택은 미확인이다.
- Darwin 1859년판 원면과 1872년판 전사 사이 문구·쪽 배치 차이, Schumann Op.73 동일 편곡 총보/A·B♭ 클라리넷 파트의 첫 진입 동일/기보음 다름은 별도 분야 사례다. 소프트웨어 6사건과 합산하지 않는다.
- 실제 구조 변경: 작업 경로에 기존 132 방식의 JS SHA-256/필드 투영 검사를 재사용하고 가명/순열·중복 검사와 이벤트 cutoff를 보강했으며 장부/결과 파일을 추가했다. 외부 계약·공통 실행기·제품 코드 수정 없음.
- 독립성: 원 답 작성자와 별도 대화에서 판독했으며 원 독서 시험/원 예제 실행을 반복하지 않았다. 이번 작업 안의 원격 재집계 및 SELF_CHECK는 자기 재검사이지 또 다른 독립 평가가 아니다. 새 독자 채택률·사람의 시간·둘째 링크 인과효과를 측정하지 않았다.

## 재개 첫 행동 및 검사

먼저 인증된 checkout에서 아래 브랜치와 입력을 가져와 현재 원격 인계 커밋 및 최초 기준·의존을 대조한다. 기존 manifest가 있는지 확인하고 있으면 재사용한다. 없다면 workbench.session의 start가 기존 진행 커밋과 최초 기준을 보존하는지 확인한 후 지정 명령을 사용한다. **원래 봉인과 원장은 절대 재작성하지 말 것.** 오염되지 않은 다른 판독자에게는 이벤트별 실제 열람면만 가린 새 투영으로 제공하고 2차 판정에 새 장부를 추가할 것.

```sh
git fetch origin chore/workspace-foundation work/research-af-res-136 work/research-af-res-132
git switch work/research-af-res-136
# 로컬 브랜치가 없으면: git switch --track origin/work/research-af-res-136
git rev-parse HEAD
python -B -m workbench.session start af-res-136 --allow docs/workstreams/research/AF-RES-136/ --dependency work/research-af-res-132=510e9db7742ea2edc09c17d0fd4e3e8fbf48ca49 --output docs/workstreams/research/AF-RES-136/manifest.json --fetch
python -B -m workbench.session check docs/workstreams/research/AF-RES-136/manifest.json --fetch
```

웹 GitHub 경로만 사용했으므로 위 checkout 명령은 **미실시**, 검사 stdout/stderr·종료값·실행 SHA는 미확인(null). 실행 후 실제 SHA, 입력 manifest, 명령, stdout/stderr, 종료값을 evidence/에 저장한다. 기존 기준을 덮어쓰지 않고 다른 편성의 악보 원면/공식 기보 출처 및 1872판 실물 이미지를 보충하며, 원 이슈 편집/병합 시점도 독립 확인할 것. 현재 원격 재검산은 고정 결과와 영수증을 재열람하여 재투영·해시·행수·쓰기 범위를 확인한 것에 한정한다.

색인 제안(중앙 변경 안 함): 136을 **PARTIAL — blind answer re-rating / narrow support vs core resolution / postrelease condition / projection contamination**으로 표기하고 RESULT, concordance, 두 봉인, 이 인계를 함께 참조한다. 결과의 양적 비교에 원독자의 실제 채택률이나 외삽된 인과효과를 넣지 않는다.

| 중요한 불일치·약점 | 다음 조사·원문 또는 실험 | 판단을 바꿀 관측 |
|---|---|---|
| 2차 예비 결합에서 뒤 면 선노출 및 현 판독 반복 인지. 엄격 제외 시 완전 비교쌍 없음. | 다른 대화에서 이벤트별 cutoff 및 본문 해시를 기계 검증한 새 투영으로 18답 근거 재판독, 원 봉인과 비교 | 선노출 없는 판독에서 좁은 지지/핵심 유보/조건부 변경의 사건별 일치 여부가 달라짐 |
| fq 조건부 후보와 원 작성자의 도구 최소화, multi-cd 등 뒤늦은 조건의 실제 공개 시점·채택 불명 | 원 이슈 수정 이력과 댓글 시각, PR2624 실제 병합 및 작성자 해결 보고 직접 확인 | 해당 제약이 원 요청 시 이미 공개되었거나 작성자가 동일 조건의 처방을 실제 채택했다는 증거 |
| 음악 2/3, 다른 편성 원판과 1872년 비교판 실제 이미지 미열람, checkout 검사 미실시 | 해당 원판·편성 원면 및 독립 기관 자료 추가 열람, 지정 manifest/check 실행 | 실물 쪽·판·마디·이조/편성의 직접 일치 또는 반례, 그리고 실제 검사 종료값과 변경 범위 확인 |
