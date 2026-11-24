# AF-RES-187 — 범위·사전 판정 규칙
착수 UTC 2026-11-24 (사용자 로컬 11-25). 계획 0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6, 최신 시작 72cf39aea54e2de2ba78a245593aefdc40205a16 (비교 ahead 3, behind 0, 변경 파일 dot-control.json만). 지정 브랜치 미존재 확인 후 최신 SHA에서 생성. AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW, START_HERE, product/RESEARCH_BRIEF, research/INDEX 열람. INDEX에 해당 사건 없음; 진행표 일반 fetch는 빈 본문이었으나 blob f0c9a6ea6f8a385ca103fabcb95df3b1a3bd130e (1,459,037자) 직접 파싱: AF-RES-187 RUNNING attempt 1, dependency AF-RES-178 DONE result bbdf4dd15393062e59c16a9d46b38d8255c672f3, owned_path/brief 일치. 고정 HANDOFF 열람: 자체 PARTIAL, 3 exact patch 중 1 upstream merged, 첫 배포 태그 0/3 확인. 이 한계 때문에 merge, tag, 배포물, 설치, 재시험을 분리한다. 178 재조사 및 186 대기 없음. STATE/INDEX의 초기 미배정 표기는 최신 작업표와 다른 시점의 환경 설명.
## 사전 모집
- N: NumPy 1.26 array/asarray; 2.0 array/asarray; migration guide; NEP50가 아닌 copy 설계/2.0 release 또는 __array__ protocol (최소 4 고유).
- H: Datasets #6976, forum 93584, 직접 연결된 후속 최대 1; A: Astropy #16167 및 #16166, 직접 연결 후속 최대 1. 두 입구 호출이 다르면 분리; 코드 없는 질문 유지. 당사자 원문 최소 4.
- F: 각 PR의 실제 변경 parent/child caller + test 파일(최소 6). base SHA와 첫 부모 혼동 금지. 태그 전후 각 2개 release 후보는 정확 파일/커밋/시간 증거로 판정. 배포/후속 최소 4 별도 자료. 태그 포함 != wheel 내용 != 설치 != 동일 입력 재시험.
- X: 디지털 보존기관 원본/접근 사본 지침·사례 2, OS shared/private mapping 원전 2 (최소 4).
- 최소 총 22 = 4+4+6+4+4. 계획 슬롯은 frame.csv에서 포함·제외·실패·미열람까지 기록. 동일 PR HTML+diff 한 건; 별도 판/파일은 고유 자료일 수 있으나 같은 계보 표시. 독립 사건은 저장소+호출+객체+목적+배포판; 제보/패치가 다른 호출이면 별도. 새 빌드/실행 금지, Codex 재현 입력만 기록. 공개 원문만.
## 판정 규칙
값 반환, 메모리 공유, 쓰기 가능/변경 전파를 독립 속성으로 기록. 입력·dtype·order·변환·패키지 판 미상이면 미상 그대로. 문서 계약/테스트 assert는 기대, 보고는 당사자 보고, 파일/태그 관찰은 직접 파일 관측, 실행 결과 없음. 복사 금지는 NumPy 2.0 copy=False 계약(불가능하면 오류), 복사 허용은 asarray/None 조건; 1.26 동작을 2.0에 기계적으로 적용 금지. 공유가 요구라면 writeable 및 실제 mutation propagation의 별도 근거 요구. 최종 권고는 필요조건/기각 관측과 버전 링크 포함. 계획 최소치 또는 핵심 연결 미달 PARTIAL. 자기 검토와 독립 검토 분리.
## 노출
이 커밋까지 내부 규칙·고정 178 인계·진행표만 확인. 외부 원문 미열람; URL/후속은 모집 예정. DB/API/수집기/검색 순위 미결정. 허용 경로 밖 쓰기 금지. 작업 계약 manifest는 checkout 없는 문서 조사이며 지정 경로 제한 때문에 생성하지 않는다.
