# AF-RES-194 HANDOFF — PARTIAL

- 상태: **PARTIAL**. 네 PEP 핵심 비교와 설계 카드를 작성했지만 종류별 원자료 최소치와 일부 직접 반응 조건이 미충족이다. 완료 승격 금지.
- 배정 branch: `work/research-af-res-194`; owned_path: `docs/workstreams/research/AF-RES-194/`.
- 착수 통합 SHA: `72cf39aea54e2de2ba78a245593aefdc40205a16`; 계획 SHA `0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6`.
- 결과가 들어 있는 직전 SHA: **`6b685b8f6b4eebf4b2aa9d11f58c21b844a74e74`**. 이 SHA에서 아래 대표 파일 8개 모두 GitHub 재열람 성공. 이 HANDOFF는 그 뒤 마지막 커밋으로 작성한다.
- 선행 고정 입력 180 `6b1afbba225dac3f051ea4a8c7bb8a6585071aea`, 183 `ed7c7278be22a5ad6eb8e87255c7d7064d12c9fb`의 HANDOFF 확인. 진행표 변경하지 않음. 다른 작업 대기하지 않음.

## 대표 파일 (직전 결과 SHA 기준)

| 파일 | 내용 |
|---|---|
| [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/6b685b8f6b4eebf4b2aa9d11f58c21b844a74e74/docs/workstreams/research/AF-RES-194/RESULT.md) | 필수 3표, Q1–Q7, 경쟁 설명과 비용, 마지막 약점 정확히 3건 |
| [SCOPE.md](./SCOPE.md) | 계획/착수 차이·사전 분모·인과 판정·노출 이력 |
| [frame.csv](./frame.csv) | 모집 61행, 포함/미산입/실패/미열람 |
| [sources.jsonl](./sources.jsonl) | 원장 51행, 산입 39 URL, 산입 37 계보 |
| [timeline.csv](./timeline.csv) | 네 PEP의 41개 구별된 관측·사건 기록(독립 결정 수 아님) |
| [alternatives.csv](./alternatives.csv) | 후보 16행, 적용 조건·반례 |
| [cards.csv](./cards.csv) | 링크 카드 12행, 컷오프·보류·잔여 요구 |
| [SELF_CHECK.md](./SELF_CHECK.md) | Q별 자체검토 및 고정 입력·명령·fixture·관측 기준 |

## 달성 및 결론

- 고정 PEP 4/4: 당시 대안과 결정 원문 연결. 3142·559 기각, 616·618 채택/구현·출시. 559·616·618의 초기판→후속 반응 순서 복원. 3142 저자 직접 후속 회신 미확인.
- 559: 기존 local helper 충분성은 결정권자 이유와 일치하며 작성자도 초기판에서 이미 알고 있었다. 3142: takewhile이 기능을 충족해도 새 문법의 판단은 별개; 기각 원문에 대안이 이유라는 명시 없음. 616·618: 기존 대안이 있어도 오류 방지·공통 계약·발견성·실패 시점 요구 때문에 새 인터페이스의 여지가 남았고 실제 채택됨. 후기 618 외부 zip_equal 안정판은 최초 제안 뒤/결정 전 출시; eager/lazy 차이 존재.
- 기술적으로 대안을 쓰기 충분한 조건과 여전히 새 API 요구가 남는 조건을 각각 제시. 12개 카드의 분류는 기성 기능, 짧은 조합, 새 인터페이스 여지 및 보류를 구별. 완성 제품 DB·수집기·검색 순위 확정하지 않음.
- 명시적 미인지→선택 변경→시행의 연결을 입증한 사건 **0/4**(목적 표본 내 발견 수). 최초 인지일이나 절감 시간/도입률은 추정하지 않음.
- 직접 열람 원장 51행, 산입 39개 고유 URL, 37 계보. PEP 4/4, 메시지 12/6, 당시판 대안 9/5(최초 제안 전 7, 결정 전 비교판 2), 구현·배포·반대 12/5, 교통·도서관 2/4. 적격 사건 5(PEP 4+교통 1), 도서관 근접 대조 1 별도. 도서관 두 원문 X03/X04는 실제 자료 재활용/신규 제작의 명시 비교 및 선택 기록이 아니므로 제외.
- 자체점검: JSONL 51 고유 ID, CSV 필드 오류 0, source ID 참조 미해결 0, frame의 포함 ID와 ledger 산입 ID 차이 0; RESULT 앞 세 표의 열 이름/마지막 표 3행 확인. 자체 검토와 독립 검토 구별: 독립 검토 없음. 역사적 interpreter 실행 및 대량 검산·벤치마크 없음.

## 미충족 / 막힌 이유와 첫 재개 행동

1. **첫 재개 행동(원문 조사)**: 도서관의 기존 자료 재활용/신규 제작을 동일 사업에서 명시 비교한 원 제안서 및 실제 vote/결정 의사록 1쌍(2 원문)을 우선 찾는다. frame의 X03/X04 근접 사례는 승격하지 말고 별도 적격 사건으로 추가; 도서관 board packet의 marketing materials, educational kits, reading program collateral, 재인쇄 비용/신규 제작 계약을 대조하고 원 결의까지 연결. 현재 미달은 교통·도서관 2/4. X03/X04 PDF screenshot 410, 텍스트 확인만; 시각 검증 필요 시 공식 다른 URL 또는 접근 가능 PDF 사용.
2. 3142 2008-12~2009-02 python-ideas/dev의 Gerald Britton 초기 thread 및 2013-05 결정 인접 답글을 추적. M01에서 기각 사유 직접 증거는 없으며 I11은 후대 회고. 저자 직접 응답/구체적 사유 미확인(강한 '대안과 무관한 기각' 사례 미입증). 616 SC 별도 메일 접근 실패, 공식 issue 통지 M12 확보. 정확한 최초 인지일은 네 사례 모두 미확인.
3. **Codex Cloud 실행**: [SELF_CHECK.md](./SELF_CHECK.md)의 명세를 그대로 사용. 실제 실행 환경과 설치 권한 확인 후 CPython v3.0, v3.6.2, v3.8.2, v3.9.0, v3.10.0 고정 태그, more-itertools v8.2.0/v8.3.0을 checkout하고 빌드/실행. `git log --all --date=iso-strict --format='%H %ad %cd %s' -S 'def zip_equal' -- more_itertools/more.py`로 최초 dev SHA 확인; 최초 공개 시점/배포 기록과 대조. `SELF_CHECK.md`의 shell 명령 및 Python fixture로 실패 발생 단계·반환·소비 trace·early stop 관측; 예외·종료 코드와 SHA·환경 보존. 구버전 빌드 실패 가능, 재현 실패를 실제 동작으로 간주하지 않음. 사용자 제안 없는 신규 런타임 도입/제품 구현은 하지 않음. 이 조사에서 직접 historical 실행하지 않았음.
4. 고정 원자료를 독립 검토자에게 전달해 사례 코딩·기간 컷오프·인지 인과·적격성 재판정. 신규 원문 확보 시 이전 판단과 변경 이유를 같은 owned_path 새 커밋에 기록. 현재 HANDOFF 이후 수정은 새 작업 재개로 처리.

색인 제안: AF-RES-194 PARTIAL — 네 PEP의 기존 대안·직접 반응·최종 결정/출시를 분리한 링크 카드 12개; 기능 동등 ≠ API 필요성 소멸, 미인지·절감 인과 미확인, 도서관 적격 원문 2 부족; 재개는 도서관 제안/결정 쌍 우선.
