# 공통 색인 반영 제안 — 미적용

## 1. 편집 기준

읽은 색인은 foundation `7b4334e55a0563225295618eaf3ad299b415d9f7`의 docs/research/INDEX.md다. 그 문서가 요구하는 고유 ID / 답하는 질문 / 현재 상태 / 파일 / 핵심 의존·충돌 열을 그대로 제안한다. ‘새 제품 연구 미배정·아직 없음’은 당시 설명이며 현재 배정을 취소하지 않는다. 원본 전체를 색인에 복제하지 않고 개별 고정 결과로 연결한다.

020의 RESULT는 결과 묶음 커밋에 있으며 최종 HANDOFF는 자기 점검 뒤 별도 커밋으로 작성한다. 아래 020 행은 명시적인 작업 브랜치 링크다. **편집 담당은 최종 HANDOFF 커밋과 acceptance 파일을 확인한 뒤 이 링크를 해당 결과 SHA로 고정한다.** 24묶음 링크는 원 인용 위치 교정을 포함한 결과 묶음 커밋 `18bb267b0048be18b13203df129e9d7c4bdbe146`로 고정했다. 사용자 요청에 따라 공통 색인·진행표·계약은 수정하지 않았다.

## 2. 대표 행 한 개

| 고유 ID | 답하는 질문 | 현재 상태 | 파일 | 핵심 의존·충돌 |
| --- | --- | --- | --- | --- |
| AF-RES-020 | 001~016의 결과를 어떤 독립 묶음으로 채택·보류·교체하고 다시 조합할 수 있는가 | REVIEW_READY_WITH_GAPS — 연구 산출 조건과 운영 절차 미충족을 분리; 최종 설계 미선정 | [RESULT·HANDOFF·묶음](https://github.com/laadkke-arch/agentflow-open/tree/work/research-af-res-020/docs/workstreams/research/AF-RES-020) | 12고정 입력; 24묶음·276쌍·16충돌·3구성; proposed_use 누락·평가 정의·전환 보존 조건; 017~019 대기 |

## 3. 개별 묶음으로 바로 읽을 행

대표 행 아래 별도 하위 색인으로 둘 수 있다. 공통 색인에24행을 모두 넣을 필요는 없으며 bundles.json을 진입점으로 써도 된다. 수용 상태는020 인계와 함께 읽고, 내용의 채택 여부는 최상위 설계자가 결정한다.

| 고유 ID | 답하는 질문 | 현재 상태 | 파일 | 핵심 의존·충돌 |
| --- | --- | --- | --- | --- |
| B01 | 원문과 해석 연결·대상·극성·시간·강제성을 첫날 보존할지 | 조건부 검토 가능·효과/최종 선택 아님 | [원 질문·부정·제약을 보존하기](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B01.md) | CF02; CF16; 선행·조건은 RELATIONS |
| B02 | 없는 정보 때문에 모든 탐색을 멈출지, 판정을 바꾸는 문맥만 받을지 | 조건부 검토 가능·효과/최종 선택 아님 | [부분 입력에서 필요한 문맥만 추가하기](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B02.md) | CF02; 선행·조건은 RELATIONS |
| B03 | 목적·속성·관계 경로를 언제 사용하고 검색 후 어떤 보장을 다시 확인할지 | 조건부 검토 가능·효과/최종 선택 아님 | [발견 경로와 기능 보장을 분리하기](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B03.md) | CF04; CF07; CF08; 선행·조건은 RELATIONS |
| B04 | 주소·설명 대상·산출물·목적상 대체의 동일성을 분리할지 | 조건부 검토 가능·효과/최종 선택 아님 | [동일성의 네 질문과 관계를 분리하기](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B04.md) | CF01; CF16; 선행·조건은 RELATIONS |
| B05 | 링크+조건 설명으로 시작하고 실제 정정 실패 때 구조를 추가할지 | 조건부 검토 가능·효과/최종 선택 아님 | [가벼운 링크·설명의 저장 경계](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B05.md) | CF06; CF16; 선행·조건은 RELATIONS |
| B06 | 독립 정정과 반례 전파가 필요한 문장을 별도 근거 단위로 관리할지 | 조건부 검토 가능·효과/최종 선택 아님 | [주장·근거·제외 조건을 연결하기](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B06.md) | CF03; CF10; CF13; CF16; 선행·조건은 RELATIONS |
| B07 | 후보 전체 등급 대신 용도·설정·근거별 판정을 남길지 | 조건부 검토 가능·효과/최종 선택 아님 | [문제·후보·사용 방식별 판정](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B07.md) | CF01; CF07; CF09; CF10; CF11; CF12; CF13; CF16; 선행·조건은 RELATIONS |
| B08 | 원거리 원리를 켤 때 관계·bridge·제외·실패 입력을 기록할지 | 조건부 검토 가능·효과/최종 선택 아님 | [원거리 원리의 전이 계약](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B08.md) | CF04; CF07; CF08; 선행·조건은 RELATIONS |
| B09 | 자체 자료집 없는 기존 LLM·코드 검색·목록+검증층을 시작 구성으로 유지할지 | 조건부 검토 가능·효과/최종 선택 아님 | [범위와 기존 도구 조합](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B09.md) | CF05; 선행·조건은 RELATIONS |
| B10 | 단발 검증 효용·변경 재검토 효용·기존 흐름의 작은 절차를 독립 선택할지 | 조건부 검토 가능·효과/최종 선택 아님 | [구조화 기록 가치 H1·H2의 선택 경계](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B10.md) | CF05; CF06; 선행·조건은 RELATIONS |
| B11 | 질문의 선택 범위와 후속 반응을 별도로 기록한다. | 조건부 검토 가능·효과/최종 선택 아님 | [실제 질문과 부분 질문의 관측 계약](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B11.md) | CF02; CF08; CF09; 선행·조건은 RELATIONS |
| B12 | 대상 형태와 문제 상대 기여를 별도 축으로 보존한다. | 조건부 검토 가능·효과/최종 선택 아님 | [후보 형태와 문제에 대한 기여 분리](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B12.md) | CF01; CF04; CF09; CF11; CF12; CF13; CF14; CF16; 선행·조건은 RELATIONS |
| B13 | 한계 문장을 본문에 합칠지 별도 필드로 보존할지 결정한다. | 조건부 검토 가능·효과/최종 선택 아님 | [한계 문장을 검색 본문에 넣는 효과](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B13.md) | CF02; CF03; CF08; 선행·조건은 RELATIONS |
| B14 | 실제 답·연구자 판정·별도 판정을 분리해 평가한다. | 조건부 검토 가능·효과/최종 선택 아님 | [판정 출처와 검색 순위의 민감도](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B14.md) | CF01; CF03; CF05; CF08; CF09; CF11; CF12; CF14; 선행·조건은 RELATIONS |
| B15 | 결정 당시 찾을 수 있었던 근거와 현재 유용 후보를 구분한다. | 조건부 검토 가능·효과/최종 선택 아님 | [역사적 cutoff와 외부 gold의 단위](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B15.md) | CF01; CF04; CF05; CF08; CF09; CF11; CF14; 선행·조건은 RELATIONS |
| B16 | 어떤 신호를 검토 대기열에 쓰고 언제 직접 내용을 확인할지 정한다. | 조건부 검토 가능·효과/최종 선택 아님 | [값싼 유지 신호와 확인 비용](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B16.md) | CF06; CF10; 선행·조건은 RELATIONS |
| B17 | 내용 상태를 시간 축의 이유 단위로 저장한다. | 조건부 검토 가능·효과/최종 선택 아님 | [추천 당시 오류와 후발 이유 붕괴 분리](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B17.md) | CF06; CF08; CF10; 선행·조건은 RELATIONS |
| B18 | 문서 확인·검색 관측·재실행·실제 적용을 분리해 전달한다. | 조건부 검토 가능·효과/최종 선택 아님 | [재현 가능한 실행과 근거 수준의 경계](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B18.md) | CF07; CF08; CF11; CF15; 선행·조건은 RELATIONS |
| B19 | 실제 편집 시스템의 병합·분리·되돌림 근거를 추가할지 | 빈칸 포함·추가 사례 필요 | [운영 식별·병합 사례의 빈칸](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B19.md) | 직접 충돌 미선정; 선행·조건은 RELATIONS |
| B20 | 대안의 공통 보존 경계와 좁힐 시점을 어디에 둘까 | 조건부 검토 가능·효과/최종 선택 아님 | [대안 보존과 조립 결정 기록](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B20.md) | CF05; CF07; CF15; CF16; 선행·조건은 RELATIONS |
| B21 | 다른 분야 탐색을 기본 기능으로 할지 선택 기능으로 둘지 판단한다. | 빈칸 포함·추가 사례 필요 | [다른 분야 원리 수요의 빈칸](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B21.md) | CF04; 선행·조건은 RELATIONS |
| B22 | 재사용 가능한 내용과 완료 인수를 어떻게 구별할까 | 조건부 검토 가능·효과/최종 선택 아님 | [색인의 내용 상태와 인수 상태 분리](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B22.md) | CF15; 선행·조건은 RELATIONS |
| B23 | 원문·요약·기술어 변환을 별도 버전으로 저장한다. | 조건부 검토 가능·효과/최종 선택 아님 | [원문 질의와 요약 질의의 의미 보존](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B23.md) | CF02; CF03; 선행·조건은 RELATIONS |
| B24 | 불명확·선호·명시 필수 위반을 구분해 후보를 제외할지 결정한다. | 조건부 검토 가능·효과/최종 선택 아님 | [별도 제외 필터의 양면](https://github.com/laadkke-arch/agentflow-open/blob/18bb267b0048be18b13203df129e9d7c4bdbe146/docs/workstreams/research/AF-RES-020/bundles/B24.md) | CF03; CF09; 선행·조건은 RELATIONS |

## 4. 통합되지 않은 원 결과의 고정 진입점

원 결과는 foundation 작업 트리에 없을 수 있으므로 브랜치 HEAD 대신 지정 result_commit을 사용한다. 원 인계 상태를 이번 표준 어휘로 덮어쓰지 않는다. 이 목록은 독립 연구의 승인 목록이 아니다.

| 원 작업 | 고정 result_commit | 인계 파일 | 상태 주의 |
| --- | --- | --- | --- |
| AF-RES-001 | 4d6208c08f6f2657865ba000d6768f6537e832b6 | [AF-RES-001 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/4d6208c08f6f2657865ba000d6768f6537e832b6/docs/workstreams/research/AF-RES-001/HANDOFF.md) | 원 HANDOFF 확인; 문서·실행·효과 범위 구분 |
| AF-RES-002 | 62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1 | [AF-RES-002 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1/docs/workstreams/research/AF-RES-002/HANDOFF.md) | 원 HANDOFF 확인; 문서·실행·효과 범위 구분 |
| AF-RES-003 | b13db3931b4021ff9e1ac6e404590c09526c3087 | [AF-RES-003 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/b13db3931b4021ff9e1ac6e404590c09526c3087/docs/workstreams/research/AF-RES-003/HANDOFF.md) | 원 HANDOFF 확인; 문서·실행·효과 범위 구분 |
| AF-RES-004 | 2b798c7d2b7355b649691c18de196104ceabb0f0 | [AF-RES-004 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/HANDOFF.md) | 원 HANDOFF 확인; 문서·실행·효과 범위 구분 |
| AF-RES-009 | 7f627a81199f06da7f7b15f979e7fef25dd17602 | [AF-RES-009 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/HANDOFF.md) | 원 HANDOFF 확인; 문서·실행·효과 범위 구분 |
| AF-RES-010 | 0603f0d2990c7a501dbdfc45fbbba79155f505fc | [AF-RES-010 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/0603f0d2990c7a501dbdfc45fbbba79155f505fc/docs/workstreams/research/AF-RES-010/HANDOFF.md) | 원 HANDOFF 확인; 문서·실행·효과 범위 구분 |
| AF-RES-011 | 478c301b693896e2c6d777f46ac441f071bfdfe8 | [AF-RES-011 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/478c301b693896e2c6d777f46ac441f071bfdfe8/docs/workstreams/research/AF-RES-011/HANDOFF.md) | 원 HANDOFF 확인; 문서·실행·효과 범위 구분 |
| AF-RES-012 | cb602858378db90adb1f085953016267f9afbd6d | [AF-RES-012 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/HANDOFF.md) | 원 HANDOFF 확인; 문서·실행·효과 범위 구분 |
| AF-RES-013 | eb569f07a3a34ffacf114384ae9b06ad062f5396 | [AF-RES-013 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/HANDOFF.md) | 원 BLOCKED — SITE_CAP_CASES; DONE과 정합성은 별도 인수 확인 |
| AF-RES-014 | 42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9 | [AF-RES-014 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9/docs/workstreams/research/AF-RES-014/HANDOFF.md) | 원 HANDOFF 확인; 문서·실행·효과 범위 구분 |
| AF-RES-015 | e39d23c9a7307ba83c974580f60115d90e221084 | [AF-RES-015 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/e39d23c9a7307ba83c974580f60115d90e221084/docs/workstreams/research/AF-RES-015/HANDOFF.md) | 원 HANDOFF 확인; 문서·실행·효과 범위 구분 |
| AF-RES-016 | 3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc | [AF-RES-016 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/HANDOFF.md) | 원 core_artifacts_complete_with_blocked_named_original_reading; 고전0/2 미열람 |

## 5. 편집 담당의 다음 첫 행동

최종020 HANDOFF 커밋에서 RESULT·SELF_CHECK·acceptance-evidence를 함께 연다. 연구 종료 조건 미충족 1건과 절차상 미충족 3건을 따로 확인하고 대표 행의 브랜치 링크를 검토한 SHA로 고정한다. 그런 다음 원013/016의 DONE 처리에 대응하는 인수 기록이 있는지 진행 담당에게 확인할 질문을 남긴다. 이 연구에서 질문을 전송하거나 상태를 변경하지 않았다.

## 한계

색인의 최종 계층·통합 커밋·정규화 정책은 편집 담당의 결정이다. 현재 파일은 적용 가능한 행 제안이며 공통 파일을 수정한 결과가 아니다. 이름이 비슷한 역할·gold·완료 상태를 단일 라벨로 합치지 않는다. ADR X10의 이력 보존과 근거 지도 X14·X15의 범위/빈칸 분리는 편집 제안의 방법 근거이며 상태의 외부 검증은 아니다.
