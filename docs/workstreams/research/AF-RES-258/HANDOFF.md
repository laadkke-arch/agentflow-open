# HANDOFF — AF-RES-258
**작업자 자체 상태: PARTIAL.** 사전 봉인, 4경로×3설명, h0 통제, 고정판 소스 손추적, 원자료 그룹별 하한, 본표 및 자체 점검 완료. r170 동일 경로 저자 실행 시험 확보 못함(update TODO); 신규 런타임 및 사용자 체감 미실행. 독립 A/B 맹검/독립 검토 없음. 중앙 진행표 수정하지 않음.
- 고정 결과 SHA (HANDOFF 직전): `a6581c8f2bd2d004990ac62a09c8017bb0781370`
- 시작 통합 SHA: `c64c54d2aae4045b0e2a28a1fdfca9f9313de765`; 배정 control blob `b33c62aab6f9db2ce3b2d5305633acba0fb7faf7`; 258 RUNNING attempt1, depends_on 245 중앙 DONE/자체 PARTIAL handoff `a8cbbdc0bd29f0e74594f1eae17cedd946c34aa2`. actual_model control null, 실행 환경 모델 배정과 실증 구분.
- 브랜치: [work/research-af-res-258](https://github.com/laadkke-arch/agentflow-open/tree/work/research-af-res-258/docs/workstreams/research/AF-RES-258/); 소유 경로만 편집.
- 판: [three.js r170 LOD.js](https://github.com/mrdoob/three.js/blob/beab9e845f9e5ae11d648f55b24a0e910b56a85a/src/objects/LOD.js#L156-L204); [저자 시험](https://github.com/mrdoob/three.js/blob/beab9e845f9e5ae11d648f55b24a0e910b56a85a/test/unit/src/objects/LOD.tests.js#L105-L147).
- 봉인 SHA `6931ef06a34e4bffe7039b41eede778f3e470b43` (구현·시험 직접 열람 전); A/B 독립 차단 아님. 원자료 묶음 `a244cc90c3d1387cab340f843c4eb812e4f30b19`, `6c5d839a8b202b24c1881c5b94692ba404c4c199`; 반례 `5964b500acf2a278446838d28ce3fa5f21ddff41`; 자체 집계 오기 정정 `6a83916c92c5a55dbf08e73fe54a063f8afdacaa`.
## 결과 고정 링크
- [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/a6581c8f2bd2d004990ac62a09c8017bb0781370/docs/workstreams/research/AF-RES-258/SCOPE.md)
- [predictions.csv](https://github.com/laadkke-arch/agentflow-open/blob/a6581c8f2bd2d004990ac62a09c8017bb0781370/docs/workstreams/research/AF-RES-258/predictions.csv)
- [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/a6581c8f2bd2d004990ac62a09c8017bb0781370/docs/workstreams/research/AF-RES-258/sources.jsonl)
- [transitions.csv](https://github.com/laadkke-arch/agentflow-open/blob/a6581c8f2bd2d004990ac62a09c8017bb0781370/docs/workstreams/research/AF-RES-258/transitions.csv)
- [transfer.md](https://github.com/laadkke-arch/agentflow-open/blob/a6581c8f2bd2d004990ac62a09c8017bb0781370/docs/workstreams/research/AF-RES-258/transfer.md)
- [COUNTEREXAMPLES.md](https://github.com/laadkke-arch/agentflow-open/blob/a6581c8f2bd2d004990ac62a09c8017bb0781370/docs/workstreams/research/AF-RES-258/COUNTEREXAMPLES.md)
- [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/a6581c8f2bd2d004990ac62a09c8017bb0781370/docs/workstreams/research/AF-RES-258/RESULT.md)
- [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/a6581c8f2bd2d004990ac62a09c8017bb0781370/docs/workstreams/research/AF-RES-258/SELF_CHECK.md)
## 결과와 제한
최종 95, h=.1 P1/P2/P3/P4 = N/F/F/F, h0=N/N/N/N (소스 추적). F.visible이 true이면 D−Dh=90, >=를 만족하면 F; P4에서 90 equality 유지. B의 <=90 off 가설 오류. 사전 h=.1 endpoint A 미결4/4, B 적중3 오류1, C 적중1 오류3. B−A singleton 추가 적중3/오류1, B−C 추가 적중2/동률2. h0 4동률 정확. B′ lower strict는 사후, 점수 소급 금지. 실제 차용·사용자 안정성 미확인. 원장33행, 성공26, 실패7, 산입24(8/7/5/4), 13 lineage, 실제 신규 프레임 관측0. 
## 미달과 다음 첫 행동
1. transfer.md의 명령을 그대로 별도 Codex에서 정확 SHA로 실행. Node version, git HEAD, exit, stderr/stdout raw JSONL, flag/level/query 포함. P4 frame2 N이면 추적 수정, B 재채점; 다른 경로 불일치도 검토. 원저자 공개 시험의 같은 입력/실행 영수증 별도 조사. 실행/로그 없으면 완료로 올리지 않는다.
2. A/B 독립 문서 접근 차단 재실험: A에게 r170 API만, B에게 원 분야 자료 추가, 양쪽 커밋 후 구현 및 평가 공개. A+가 정확 4/4면 순증분0 가능. 
3. 사용자 떨림/프레임 개선은 화면과 렌더러/자산/경계 진동/프레임 시간을 통제하는 별도 과제. 거리와 화면비를 혼용하지 않는다.
## 색인 제안
주제: hysteresis / state-dependent threshold / cross-domain mechanism transfer / boundary equality / LOD. 연결: AF-RES-245 (제약이 실제 선택을 좁히는지, 반례 정정); 관련 제약 전이와 단일 임계/혼합 대안. 242/251/254/255 의존 없음. 중앙 dot-control은 통합 담당만 갱신. 
