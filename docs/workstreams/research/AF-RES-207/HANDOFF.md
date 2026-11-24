# AF-RES-207 #1 HANDOFF

**자체 판정 DONE. 독립 검토 미실시.** 195의 실제 문장 6건과 196의 단건 재열람 합격 형식을 비교했다. 원행을 정확히 인용한 실재 합계 2건은 A와 B 모두 복원했다. 통제에서는 A가 같은 값의 행 교체와 같은 참여자 관측 복제를 승인했고 B가 두 경우를 보류했다. ms/초 오기와 누락의 0 대체는 두 안이 보류했다. [결과표](RESULT.md) · [16행 판정](matrix.csv) · [자체점검](SELF_CHECK.md)

## 고정 입력과 결과판

- 저장소 `laadkke-arch/agentflow-open`, 브랜치 `work/research-af-res-207`, 소유 경로 `docs/workstreams/research/AF-RES-207/`. 시작 `c860f8240ab7b7077e2d5b63e438ddd83ff69a27`, 계획 `050278651b11a2a3a49d45baebf41c707c06b700`. [범위](SCOPE.md) · [계약](session.json)
- 195 고정 인계 `a674c67aaf2c4f1a6aaef4b1ac278dabf44188c0`는 중앙 DONE·자체 PARTIAL이며 PET 원행을 제공했다. 196 고정 인계 `6147197ee77016a096412353bd9c3a9f4cd61b1e`는 중앙·자체 DONE이며 O2 C가 오프라인 원출전 재열람에 합격했다. 직렬화 1,083 B로 선정했다. 두 tree의 실제 경로·SHA, 합격행·비용·원문 위치가 [입력 목록](inputs.json)에 있다.
- **결과가 든 직전 SHA `70217375b704529d9cac0c84addbbc3942ea8b66`.** 원격에서 이 판을 fetch한 뒤 필수 표 3개와 마지막 약점 3행, Q1–Q7, 자체점검, 모집·정답·출처·비용·판정과 원출력을 다시 읽었다. 2026-11-24 21:20 UTC에 `workbench.session check --fetch`와 `receipts/verify.py`가 종료 0이었다. 검사한 통합판 `3d8ae6326a1cd0ab7771aed68ef7022eb4b4faf1`에는 195·196 고정점이 유지됐고, 207 중앙 행은 당시 RUNNING이었다. 경로 이탈·계약 오류 0. [고정 결과](https://github.com/laadkke-arch/agentflow-open/blob/70217375b704529d9cac0c84addbbc3942ea8b66/docs/workstreams/research/AF-RES-207/RESULT.md) · [고정 자체점검](https://github.com/laadkke-arch/agentflow-open/blob/70217375b704529d9cac0c84addbbc3942ea8b66/docs/workstreams/research/AF-RES-207/SELF_CHECK.md)

| 묶음 | 저장 커밋·대표 파일 |
| --- | --- |
| ① 범위·분모 | `854e6a55264a5ae54dab4a74516b58453b16d755` · [SCOPE](SCOPE.md) |
| ② 원문·모집·정답 | `d5a4b599b547cc73677d6b55997c278d8d6d7ef4` · [frame](frame.csv) · [gold](gold.json) · [sources](sources.jsonl) |
| ③ 주 관측·표 초안 | `ddf96378be126ff90654be44e94215230e427757` · [audit](audit.py) · [주표본 원출력](receipts/core.jsonl) |
| ④ 통제·분야 대조 | `375058d11904e5f446306b8be175f33f241b623a` · [통제 원출력](receipts/controls.jsonl) · [철도와 생산자 대조](receipts/context.stdout.json) |
| ⑤ 결과·자체점검 | `157802ab29d1d82d52964be7ac197b6f55111330` · 위 결과판 `70217375b704529d9cac0c84addbbc3942ea8b66`에서 표의 연속 행과 Q3 문구를 교정했다. 판정 및 코드판은 그대로 재확인했다. |

## 달성 범위와 남은 확인

- 주표본 12셀에서 양쪽 각 정답 4·합리적 보류 2·빈 자리 0이었다. 네 통제는 별도 4행에 두 표현의 8회 관측을 기록했다. C1의 648,615 ms·111단어·5행·1인이 같아도 B는 행 교체를 검출했다. 이 검증은 정확한 원문 코호트와 배정의 고정판을 전제로 한다. 추가된 다섯 필드는 여섯 레코드에 2,335 B, M1에 397 B다. [통제](receipts/controls.jsonl#L1-L8) · [비용](costs.csv)
- 고유 직접 열람 30개다. 유형별 실제/최소는 195 8/6, 196 7/6, 인용 원출전 7/4, 표준·공식 통계 8/4다. 종류별 부족 0. 계보 14개와 원관측·실험 사건군 6개를 자체점검에서 구분했다. [출처 원장](sources.jsonl)
- Linux/Python 3.12.14, libseccomp2 2.6.0-2, strace 6.13에서 관측 20회 모두 종료 0. 새 GitHub checkout `375058d11904e5f446306b8be175f33f241b623a` 재생에서 출력 10개가 바이트 일치했다. 이 코드판의 클라우드 공통 검사도 종료 0이다. 7021737에서 고정 대표 파일과 계약을 다시 확인했다. [재생 명령](receipts/05.md) · [지문 대조](receipts/replay-compare.stdout) · [공통 로그](receipts/replay-cloud.json)
- 독립 QA 연결은 W1·W2의 번역자 보조 행 24개에서 0건이다. 동등 품질 총노동은 미확인이다. 195의 고정 HF TSV 동일성도 미확인으로 이어받았다. Eurostat 2024 값과 상태는 공식 API를 직접 열어 정규화 사본으로 재계산했다. 셸 원바이트 수신은 HTTP 403이었고 원 전송 지문은 미확인이다. [범위와 결손](SELF_CHECK.md) · [Eurostat 전송 재실행](receipts/04.md)

## 후속 검토의 첫 행동

GitHub에서 이 인계의 직전 결과 SHA와 [입력 고정점](inputs.json)을 확인하고, [동일 입력 재생](receipts/05.md)의 주표본·통제를 새 checkout에서 실행한다. C1에서 값과 수치 분모가 모두 같은데 권위 행이 다르다는 판정을 먼저 대조한다. 효과의 일반성을 검토할 때는 195의 다른 문서·조건을 독립 모집해, 비연속 인용에서도 A가 정확한지와 참조 코호트가 함께 틀릴 때 B가 어떤 판정을 내는지 확인한다. Eurostat 원 전송을 확인할 때는 [curl 주소와 --live-json 입력](receipts/04.md)을 사용한다.

색인 제안 · AF-RES-207 / 단건 원문 보관의 PET 집계 전이 / 자체 DONE / RESULT.md와 HANDOFF.md / AF-RES-195·196 두 고정판. 완전 인용의 두 합계는 A/B 동일, B가 행 교체·복제 통제를 보류.
