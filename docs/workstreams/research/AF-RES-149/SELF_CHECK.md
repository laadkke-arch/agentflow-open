# AF-RES-149 자체검사 (PARTIAL)

검사 대상 원격 결과 커밋: 978c3ed46eaf44008901b2bb287e36977b4b461b.
최초 통합 시작 f140af3179b7d9271710778104ccee5b4812e2ef, 동결 1eda0cc3d22457e8980a21ee0c944f473e644414. 중단 시점 c560f49b577c802a3b2befa75eb5e9b6fc55d79b에서 작업 브랜치에 재개했다. 재개 시 통합 HEAD 35ca756d1b18af5d89c3eb53659365c09f1f88e3; 통합 리베이스/병합 안 함. 원래 창·요구·순서·1링크 제한은 동결 그대로.

| 검사 | 실제 검산 | 결과 |
|---|---|---|
| 모집/원장 | GitHub 저장본 frame.csv 및 paths.jsonl 각각 36행, event_id 고유, status/work_id 대조 | 일치; 실제 32, 공백 4; 실패 2, 성공 30(제작자 17/중간 13) |
| 요구 판정 | judgments.csv 108행, event×요구 고유, path source_id 연결 | 일치; 직접 0, 조건부 5쌍/96 실제, 3 대상/32; 4 공백×3 요구도 미관측으로 남김 |
| 비용 | 저장본 CSV 파서로 24행 × 24 수치 필드(576개) 독립 재계산 | 전부 일치; 절반 17 실제·15 성공·2 적격, 전량 32·30·3, A 대비 추가 2; 대기·호출 미계측 |
| 출처 연결 | paths source_id 모두 해소, 83 출처 ID 고유, 71 성공, counted && success 41개 work_id 고유 | 일치; 종류 14/14/9/4, 언어 5, 발행자 표기 29, 외부는 컬렉션 단위 |
| 민감도 | 날짜 고정 2, 중간 설명 완화 4; 합치기 적격 3→3, 전체 표기 29→32; 제거 실험은 집합 차로 산출 | 결과표와 일치; 미확인 동일성, 외부 검증 실패를 성공으로 바꾸지 않음 |
| 문서 구조 | RESULT 첫 3 표 순서 확인, 끝 약점 표 3행 확인 | 완료 |
| 소유 경로 | GitHub compare API f140af3… → 978c3ed… : ahead 13 commits, 변경 파일 8, 전부 소유 폴더 | 완료; 후속 SELF_CHECK와 HANDOFF에 대해서도 최종 비교 필요 |
| 파일 저장 | 각 commit SHA에서 파일 내용 재열람 후 작성 문자열 동일 비교 | 완료; 최종 인계도 단독 커밋 재열람 예정 |
| 도구·계약 | shell git ls-remote https://github.com/laadkke-arch/agentflow-open.git refs/heads/work/research-af-res-149 refs/heads/chore/workspace-foundation : DNS 실패(exit 128); 앞 세션 TransportError | 로컬 git checkout / session manifest / 공통 CLI 계약검사 미수행; GitHub 연결로만 비교 |
| 원전 직접 열람 | sources.jsonl 각 열람/실패, 원문 주소, 판/시점, 주장/한계 기록; 검색 결과만 본 것은 산입하지 않음 | 41 산입은 기록에 따른 계수, 독립 감사/실행 검증 아님 |
| 품질 기준 | 직접 적격과 조건부 기제를 구분, 타 분야 실제 입수, 반례, 노출 결측 및 당시판 민감도 | 부분 충족; 동일 실비용·네 언어의 최신/과거 완전쌍·당시 노출·독립 블라인드 미충족 |

## 수치 재현 방법 (실제 수행한 JS 집계의 정의)
CSV는 quoted field 및 escaped quotes를 파싱. frame/paths를 event_id로 결합하고 3 요구의 judgments를 event_id+requirement로 결합. route/window/position 필터 후 status!=missing의 실제 자리 및 maker/intermediate 성공을 각각 count. 직/부분/전이 status 집합에 속하는 work_id의 Set이 적격; 같은 필터 A의 Set 차집합이 추가, 타 경로 Set과 차집합이 단독. 같은 조건 mechanism Set / 성공수 *100 (성공 0이면 NA). dated_status/relaxed_status로 바꾸어 각각 재계산. 각 cell의 3/6 위치 상한 유지, ALL은 합집합. 노출 수치는 입력하지 않음. 동일 판/제품 분리는 현재 work_id 기준으로만 계산하며 전역 동일성 보장 아님. 
결과표의 셀 실측 32/36은 B-W2 뒤 4자리 구조적 부재가 원인; 예산 36/36 준수는 최대치만 의미. 이중으로 채워 넣지 않는다. 실제 결손 4; 네 언어 비교는 5언어 원전 확보와 별개로 최신성 및 동일 종류 과거 목록 직접 확인 불충분. 정확한 최초 공개·MR·메일의 결손, 32/32 당시 노출 미확인, 실제 열람별 호출·대기 결손. 직접 적격 0은 연구 결과이지 누락 검증의 대체물이 아님.

## 판정
PARTIAL. 필요한 다음 첫 행동: 별도 사전등록된 보충 비교(동결 원장 수정 금지)를 만들고 B의 6행 확보 가능한 새 창 및 FR/KO 날짜 고정 원 목록 접근성부터 확인한다. 이어 원문 판·편입 경위 및 당시 노출 수치를 고정해 실측 호출/대기·독립 판정을 수집한다. 현재 보고는 후보 추천/최종 구현 선택을 확정하지 않는다.
