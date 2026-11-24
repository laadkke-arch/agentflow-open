# 가림 투영 재현 및 감사

**판독 전에 동결된 원 규칙:** [SCOPE.md @ 99746d7](https://github.com/laadkke-arch/agentflow-open/blob/99746d7da62c5bac396fa1cd6a1b6ac046df6f40/docs/workstreams/research/AF-RES-128/SCOPE.md). 이 README는 사후 정리이며 원 규칙을 고치지 않는다.

## 허용 필드 및 시험
출력 객체는 새로 생성한 `{id,request,answer,views:[{id,body}]}`만 허용한다. 원본 행 객체 전체를 넘기지 않는다. case_id, stage, URL 메타데이터, group, confidence, change, provisional_self_assessment, score, gold, 사후 판정, 다른 답, 선택 이유는 출력하지 않는다. 요청·원문 자체에 포함된 문장, URL, 단계 단서는 변경하지 않는다. SCOPE의 판독 전 JS 소형 시험은 가짜 score=999, anchor_url=LEAK_URL, group=LEAK_GROUP을 삽입하여 허용된 출력 키와 금지 표지 부재를 확인(PASS). 실제 허용된 출력은 [blind-packets.jsonl](blind-packets.jsonl), 최초 투영 커밋 62f09763ccb6d8b55ba93f7dc1258a884f81b885. 판독 봉인 418cf8865711c96c2b3a045f5a94a266fba417d4 이전 원 점수 미열람.

## 재현 순서
1. 124 고정판 7dd19f7fdac69b9dad4d6170ea247580b857f9b4의 prior.jsonl, after-first.jsonl, final-answers.jsonl, trails.jsonl과 120 고정판 de99023970ca060e8227594c41448e6938efed23의 packets.jsonl, evidence/natural-views.jsonl을 **도구 내부**에서만 파싱한다. 원 요청은 case_id별 자연층 issue_body를 고정하고 중복 본문이 같은지 확인한다. 답 파일에서는 case_id로 조인하되 answer만 투영한다.
2. 보관 면 body를 Unicode code point 배열로 세어 characters와 end-offset를 검사한다. FNV1a 32-bit: 초기 2166136261; 각 codepoint XOR 후 16777619 곱, mod 2^32. 보관 면에 기록된 값과 비교한다. 불일치·중복 조인·누락 시 그 답을 차단한다. 56/56 확인한 실제 작업은 SCOPE와 봉인판 기록 참조.
3. trails 중 실제 anchor_url 및 offset/end/characters가 존재하고 보관 면과 정확히 맞는 13행만 취한다. stop 5행 제외. prior=0면, after-first=stage 1의 1면, final=실제 열린 모든 면(stage 오름차순). P1 final은 3면; 동예산 비교에서는 stage 3 제외.
4. case_id 오름차순 × [prior,after-first,final] 순으로 18쌍 생성. seed 1282026, Fisher-Yates 뒤에서 앞으로: state=(1664525*state+1013904223) mod 2^32; j=state%(i+1), swap. 결과 B01..B18. 각 답의 views는 E1부터 번호. 아래처럼 출력 구조만 생성한다(개념 코드, 추가 실행한 스크립트 아님).

```js
function project(id, request, answer, visibleBodies) {
  return {id, request, answer, views: visibleBodies.map((body,i)=>({id:"E"+(i+1),body}))};
}
```

5. 한 답씩 판독자에게 반환한다. 주장별 지지/태도 및 등급을 원장에 봉인한 후에만 124 HANDOFF, RESULT, scores, assignments, projection-remote-check을 개봉한다. 실제 작업은 18개 별도 호출로 읽었으나 한 작업자에게 같은 사건이 반복되어 12행에서 인지되었다. 완전한 독립 눈가림으로 볼 수 없다. 새로 재현 시 독립 읽기 관측으로 세지 말 것. 해제 대응은 concordance.csv.

정식 checkout/CLI 검사는 미실행. 이 절차와 원격 재집계는 계약 검사를 대체하지 않는다.
