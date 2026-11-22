# AF-RES-036 진행·봉인 원장

| 순서 | 고정 커밋/기록 | 범위 | 다음 단계와 제한 |
| --- | --- | --- | --- |
| 1 | bdc4135b0f9f67e08060a4ba5c78d30e276d927d | SCOPE·manifest·prior exclusion·사전 방법 검토·측정 fetch 도구 | 두 경로의 원배포만 수집. 현재 href/H/기준판정 아직 열람하지 않음 |
| 2 | f5be64952dbd7fdc38e44db938bd863a487f82cb | 네 새 문맥의 Latin-square 배정 봉인 | 실제 판독은 뒤에 수행 |
| 3 | bd3c17ef2f989b3d9e0566405d82357fc17f47bb | B12·원배포12출판·표집58행 봉인 | G06/R04 수집 사전노출을 숨기지 않음 |
| 4 | 129d87ca98a46d68e37bffc86c8d085503d9f77f | 지리·서지 보조 원문·반례 | 소프트웨어 분모와 별개 |
| 5 | f26232bb567f26ea86ece55215097be1185f75cb | 채점·제외·조건부 비용 계산 사전 계약 | 판독/기준 전 |
| 6 | 442292b34237fa7aa2d68493e2a96802f52ed728 | 동일 N/H 카드·48보기·판독 입력 봉인 | 원문/metadata 길이 구별은 ERRATA E02 |
| 7 | 550cc0632aa31723ce943892f937d4f75a781cbc | 수집 관측·중복제거 원문·실측 비용 | 후속 기준판정 원장 누락은 ERRATA E01로 정정 |
| 8 | 5fbde38a04613fbd6f057fd562bd173b7193f2c9 | 네 새 문맥의 48결정 봉인 | 이후 기준판정; 답안은 변경하지 않음 |
| 9 | 5d6acbc87068c2c1f0cfa7ae95846c409c1f7ad1 | 실제 보관 표현·Q7 추가 정정 원문 | C1/C2 2회차는 모의 |
| 10 | f403243dbf5f097536a1fd9fda55dfce4382329a | 별도 문맥 기준판정·짝지은 민감도 | 요청 #2의 재개 시작판; RESULT/SELF_CHECK/수용/HANDOFF 미완료였음 |

## #2 재개 범위

최신 작업판 f403243과 integration `8dd88b74735eb512c133f1a30890ac82fbf61ecf`를 GitHub ref·git ls-remote·새 clone에서 확인했다. 기존 manifest의 최초 시작판 `9668632e915d508e93ddfdc5e8fe4b88bcbfec56`와 모든 봉인 입력·판독·기준판정을 보존했다. 새 배포물 표집이나 48판독을 반복하지 않았다. 실제 환경과 미관측 모델UI는 `evidence/resume-context.json`에 있다.

세 내부 감사는 정량/소프트웨어원문/보조분야·비용으로 분리했다. 기준판정64source와64attempt의 canonical 누락을 고쳤고 적격 최소원문50은 그대로다. 재개 감사10GET와24웹도구동작·1로컬실패는 별도 phase이며 두 번째 C1/C2 실행이 아니다. 원장 정정과 보고 문구 정정은 `ERRATA.md`, 의미 검토는 `review/resume-*/`에 남긴다.

완료된 감사의 당시 실행 영수증은 정량69/69, 비용57/57, 재개 원장까지 통합한 정량81/81이다. 이 수를 이후 문서까지 검증한 값으로 소급하지 않는다. 인계 전 최종 문서·수용 근거·hash 조인·소유경로 검사를 다시 수행하고 고정 결과를 원격에서 읽은 뒤 HANDOFF를 작성한다. 작업 중 상태의 검사 대상은 HEAD와 working-tree 입력hash를 함께 기록한다.

원장·감사 정정 묶음은 **`b47d567c4285821e59af0db0081e3b79f0675f26`**으로 원격에 커밋했다. 공개 git fetch 후59파일의실제본문이로컬과같음을확인했다(`evidence/resume-audit-remote-receipt.json`). fast-forward와expected_sha를사용했으며기존커밋이나작업파일을초기화하지않았다.

그 위에서 작성한RESULT/SELF_CHECK/수용파일은문서21/21,원장81/81을실제로검사했다. 수용조건은33중28충족·5미충족(C05/C07/C09/C15/C28)이며상태는REVIEW_READY_WITH_GAPS다. 검사입력SHA256과실제HEAD를각영수증에남겼다. 다음은이결과묶음의원격커밋·고정SHA재독·인계직전session check다.

## 다음 단계

1. 원장·감사 정정 묶음을 원격 커밋하고 SHA를 실제 조회한다.
2. RESULT·SELF_CHECK·조건별 수용 근거와 최종 검산을 별도 결과 커밋으로 고정한다.
3. 고정 SHA의 RESULT/SELF_CHECK/수용파일을 원격에서 재독하고 `python -B -m workbench.session check docs/workstreams/research/AF-RES-036/manifest.json --fetch`를 실제 실행한다.
4. 실제 결과 SHA·미충족·다음 첫 자료·검사영수증을 HANDOFF에 적고 마지막 커밋을 확인한다.

## #2 고정 결과·인계

결과 묶음은 **`ef839d30d300e20f092dd7f0d57542f0773b77f8`**으로 원격에 고정했다. 2026-11-22 17:25:14 UTC에GitHub에서RESULT·SELF_CHECK·수용·집계·검사6파일의본문을다시읽어모두일치함을확인했다. 같은결과SHA에서원장81/81,문서21/21,`workbench.session check --fetch` exit0/passed/remote_checked(17:25:49 UTC)를확인했다. 영수증은`evidence/result-remote-reread.json`, `review/resume-quant/audit-result-sha.json`, `evidence/document-check-result-sha.json`, `evidence/checks/session-result-execution.json`이다.

위 확인 뒤 **HANDOFF.md를작성했다**. 상태는REVIEW_READY_WITH_GAPS(28/33)다. 완료된묶음을다시반복할필요가없다. 남은연구의첫자료는NULDL000040/ESTCR17253의Norton표기이전고정catalog record와정정영수증이며,기존12참조와48판독은보존한다. 최종인계SHA는`git log -1 --format=%H -- docs/workstreams/research/AF-RES-036/HANDOFF.md`로확인한다. 자기커밋SHA를미리만들어기록하지않는다.

셸 push는 인증 없음(exit128)으로 실패했다. 계정/credential을 변경하지 않고 기존 GitHub connector의 지정 계정으로 tree/commit/ref를 만들었다. 원격 branch는 시작 integration의 자손이다. 이후 묶음도 원격 커밋 후 fetch/read로 확인한다. 내부 local-only 39277b4는 원격 완료 SHA가 아니다.

## 카드 공개 전 판독 개선

prior 검토자가 제안한 four-context Latin square를 reading-plan.json에 고정했다. seed360032와 48배정을 공개 전에 저장하며, 4개의 새 문맥은 fork_turns=none로 시작한다. 동일 사례 재노출을 줄이지만 사람/독립 모델/실서비스 실험이라는 뜻은 아니다. 표집/현재/이력/기준판정 담당은 이 입력에 엄격 미노출이 아니다.
