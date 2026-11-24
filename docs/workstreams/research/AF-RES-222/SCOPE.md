# 범위 및 사전 예측
착수 통합 SHA f3895893e32e2c055cefde446d34f1467fa27b4c. 계획 fc095c323d0177401d34f1daa7b4d1c529e2351f 대비 +5/-0, dot-control.json만 변경(264 추가/9 삭제); 계획판에는 222 항목이 아직 없고 실제판은 RUNNING, attempt 1, depends_on 211/213, owned_path 일치. 대형 진행표 contents API 빈 본문은 blob 449f580659cac8affef11c502e23cbb25305152d로 복구해 실제 항목 확인. AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW, START_HERE, RESEARCH_BRIEF 읽음. 작업 브랜치 신규 생성. 211 고정 인계 873621fcdeb1bf57c8e6477a0a2c0c9959583a7d 및 RESULT/destinations/versions, 213 425835c2bba66a7002ad281222163024595987f8 및 RESULT/objects/resolutions 직접 열람. 중앙 DONE이나 실제 인계는 양쪽 PARTIAL; 211 별칭 생존≠고정판 지원, 213 별칭 ID≠공통 부모 본문. 216–218 제외.
## 고정 분모
- U+01A2, A015, 2118, FE18 네 정정 및 000A, FEFF 대조. UCD 6.0.0, 6.1.0, 16.0.0: 18 code/version 자리. Name은 필드 1(0부터), <control>은 placeholder. NameAliases의 모든 대상 행을 보존, NamesList 설명과 구별.
- CPython v3.13.0 / ICU release-76-1, 6×2×3=36 기본 방향; 여러 별칭 및 ICU name choices는 하위 관측(별도 분모). 제어의 old Name 부재는 N/A이지 실패 0이 아님.
- 자료 목표 22, UCD 배포/변경 7, 정책/규격/표 4, 소비자 7(각 >=3), LOC 4. 독립 사건은 4 correction+2 control/alternate 사례; 동일 원출전의 다중 소비 및 판간 동일 바이트는 독립 사건이 아니다. LOC는 별개 인물 사례; 동일 literal label로 자동 병합 금지.
- 노출 순서: 범위→원자료→주관측→반례→결론→readback→handoff. 직접 API 실행·설치·제품 구현 없음. 관측(정적 원행), 문서/시험 기대, 추론, 미확인 분리.
## 예측 (외부 원자료 열기 전)
P1: 정정 이름이 공식 Name을 덮지 않고 동일 코드로 연결된다. 반증: 판간 Name 변경/다른 코드 할당.
P2: alias 목록의 판별 부재/존재가 최초 검색 가능 시기를 제한하나 소비자 배포 시점과 같지 않다. 반증: 옛 소비자 독자 별칭, 옛 UCD 행 발견.
P3: Python lookup은 정정 및 control/abbreviation을 수용, name은 고정 Name만; ICU는 choice별 alias 종류 제한 예상. 반증: pinned 구현에서 별칭 전종 수용/역방향 차이 없음.
P4: NamesList 설명은 formal alias가 아니며 같은 사람 이름은 전거 ID 없이는 식별 불가. 반증: 모든 annotation을 공인 unique name으로 규정.
대안 A code-only; B code+판+역할+입력 문자열/소비자; C B+정정 원행/출처·관측. 판 변경에 따른 역사 인용 및 검색 정확도 비용 비교; 최종 설계 확정 안 함.
