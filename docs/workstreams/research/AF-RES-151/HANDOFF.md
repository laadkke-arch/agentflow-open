# AF-RES-151#1 HANDOFF — PARTIAL (최종 보완 재시도 #2)

## 고정 기준 및 현재 결과
- 저장소 laadkke-arch/agentflow-open; 브랜치 work/research-af-res-151; 허용 경로 docs/workstreams/research/AF-RES-151/.
- 직전 인계 9686988e51e1e6635bb652918e9b9480f4e9b770에서 재개. [기준 인계 원문](https://github.com/laadkke-arch/agentflow-open/blob/9686988e51e1e6635bb652918e9b9480f4e9b770/docs/workstreams/research/AF-RES-151/HANDOFF.md) 보존. 기존 원장/비교/감사·후속 원장 수정 없음.
- **결과 SHA 489d03c0e96fd197597cbd4d52f76b9615cf26b7**: [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/489d03c0e96fd197597cbd4d52f76b9615cf26b7/docs/workstreams/research/AF-RES-151/RESULT.md) blob f38d3036972a35ef62fbebc612f5f521ed6c975d; [SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/489d03c0e96fd197597cbd4d52f76b9615cf26b7/docs/workstreams/research/AF-RES-151/SELF_CHECK.md) blob 257dc6bad95c5394274d458462f7bf6104a75695; [검산](https://github.com/laadkke-arch/agentflow-open/blob/489d03c0e96fd197597cbd4d52f76b9615cf26b7/docs/workstreams/research/AF-RES-151/retry2/verification.json) blob 329aee57b11b0e1ed8ea3fcd5278d1113a0148f9. 직접 고정 SHA 재열람 완료.
- 기준→결과 GitHub compare ahead10, behind0, 변경10 경로 = RESULT/SELF_CHECK 두 파일 + retry2 신규8. 기존 원장·중앙 색인 및 허용 경로 외 변경 없음. 이 인계는 결과 검증 후 마지막 별도 커밋으로 작성; 자신의 SHA는 실제 branch HEAD로 확인.

| 실제 작업 묶음 | 고정 commit |
| --- | --- |
| N0 접근 원장 / 복구 절차 | 748f2914108de9fe33f97d052c76127a0b308a2f / 4d30bfc23d12ed591036c7b17cffcef7ecc96d6e |
| 실제 CineLog 및 Syncthing patch | 5e4af2edfe422903116db0436ff6dc60438fd279 |
| 원사용자 결정 원장 / 출처 원장 | 7b15373c29b597f81e4aefdcf110eb1434a482be / 4b9bc748b4e9516bedccbd23b26f99a40e70d105 |
| 공개 원본 계약 receipt / 재현 script | 3f525744db2cf3a514840144358917784adc0c5f / 6be308f2cafc106c2638b9d19230778c2217e8ec |
| 엄격/완화 및 운영 수치 검산 | 8a0ccb1eb287fa5e7022cd2a9b42d9cba12f2a7e |
| 갱신 RESULT / SELF_CHECK | 637faf75715b8d3d0157f85d3b2741bf6743066d / 489d03c0e96fd197597cbd4d52f76b9615cf26b7 |

## 이번 실제 성과
1. 원 N0 동일 API query와 Wayback CDX/사이트/SEDE/공개 dump 경로 재시도. DNS exit6, no JSON, CDX inaccessible, SEDE 403; 2024-04-06 dump 목록은 열었지만 binary/Posts.xml 획득 실패. **N0 0/6 관측, 전체·원순서 미확인**. N1 5/6, N2 완화6/6·엄격5/6 별도. 검산: 완화18 판단행, 엄격15행 차이0. 엄격 N2 15 atom 확인10, 셀 S13/U16/X1, A8/10 B10/10 C활성0/10·보관10/10, 유일 손실 A2. 원 모집단 대체 및 층 합산 금지.
2. 공개 원본 계약: Syncthing #9313 원질문자가 지목한 고정 SHA의 원 Go 파일 4개 blob 일치 후 실제 6 upstream test + 1 추가 fixture PASS, generated protobuf 필요 1 test 제외. Node 실제 7/6/6/5/6→병합 diff 7/7/7/7/7. [PUBLIC_CONTRACT](retry2/PUBLIC_CONTRACT.md) 원 fixture/해시/명령/출력. 실제 원질문자 KeyWeeUsr의 PR #9314 merged 2024-01-02, 6파일 +12/-6. 공개 제작자 테스트, stdlib shim 및 UI 발췌 하니스, 실제 사용자 장치/전체 API/브라우저 배포 아님.
3. CineLog F-Droid metadata 삭제/복구 실제 diff 확보. 23 disable 추가→23 과거 항목 제거와 2.0.0 code40 pinned bfa57ec, AutoUpdateMode None→Version. restore target 2024-03-25 release의 plugin3.3.0/runtime3.2.2/schema9 그대로, Room rewrite 후속 4/9·5/13·5/15 patch와 다른 시점. GPLv3-or-later source license diff 2건과 공개 공지, #76 5댓글 확인. **DAO 변경이 해당 복구 직접 원인 아님**, 라이선스/소스 조건 변화가 복구 근거. 운영 commit 간 경과 78일23:43:46, 실제 인시/금액/다운타임 아님. rebuild/설치/3.3.0 binary-source 대응 미확인.
4. 원질문자 결정: R3 Cornelius PDF-XChange Viewer 시험/Wine1.8 동작 보고(보충6 중1, 나머지5 미확인), #9314 직접 수정 및 병합, #9328 수동 pause 선택 및 액수 불명 비용, #9028 restart workaround, quota 뒤 #9329 실제 모드 전환(자연 분모 제외). #9315 실제 운영 거절/사유 ~5MB GUI asset 추정 및 사전 생성 대안, 원사용자 감사만 확인. 지속 채택/효용·인시 미확인. 원래 fixed pair 및 엄격 양방향 반전0/6 보존. 새 근거 registry21행, 선택 registry11행, 기존 원전 수에 무조건 합산 금지.
5. 이전 가림/공개12/12 및 별 비교6/12, 변화0/12 재집계. **독립 판독자 0** (동일 연구자 자기 판독). 실제 새로운 원문·실측과 산술 재검산을 독립 의미 판독으로 부르지 않는다.

## 남은 미충족 / 재개
PARTIAL 유지; 완료 처리 금지. N0 고정 raw 또는 동일 API 결과 접근, 독립 무명 packet 판독, R3 실제 원 PDF·RO 정렬 및 R6 OS/실사용 routing, 엄격 우위 반전/실사용 후속, F-Droid 실제 빌드·배포 로그·plugin binary/source 대응, 관측 가능한 재취득 인시/금액·지속 채택은 남았다. N0 승인 네트워크 정확한 명령 및 dump 별도 재구성은 [N0_RECOVERY](retry2/N0_RECOVERY.md); 원 계약은 [contract-repro.sh](retry2/contract-repro.sh) (network 또는 AF151_SOURCE_DIR; 재구성 스크립트 자체 최초 실험 때 실행했다고 주장하지 않음), 원 실행 receipt 별도. shell Git DNS exit128로 checkout/manifest/workbench.session start/check/CI 미실시; 이전 SCOPE/SELF_CHECK 명령 참조. GitHub connector compare/readback은 shell 계약검사 대체 아님. 결과/검산 이후 허용 경로 내 HANDOFF 단독 마지막 커밋.
