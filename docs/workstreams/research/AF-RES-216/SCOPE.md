# AF-RES-216 조사 범위

## 기준과 질문

PyPI의 여섯 릴리스 배너를 현재 파일 단위 metadata에 연결한다. 정확한 파일과 판을 요구하는 개발자, 새 호환 범위를 쓰는 개발자, 기설치 구성을 설명하는 개발자의 링크 판단을 각각 검토한다. 원문의 해당 부분과 적용 이유를 돌려주는 탐색기 연구이며 배포·설치·결함 재현은 범위 밖이다.

- GitHub 최신 통합 `87ffc1539bcf33da0fccf45eb15982a02d93e409`에서 원격 작업 브랜치 부재를 확인하고 `work/research-af-res-216`을 만들었다. 계획판 `bb146773bbffba5e724e8c842951e2c25198c2da`보다 5커밋 앞서고 0커밋 뒤에 있다. 차이는 진행표 한 파일의 AF-RES-205~207 결과 반영과 후속 작업 등록·배정이다. 제품 브리프·연구 운영 규칙은 두 기준에서 동일하다. 관련 색인 문자열 조회는 AF-RES-200·216 및 프로젝트·철회 항목을 발견하지 못해 고정 의존에서 시작했다. [시작 SHA](https://github.com/laadkke-arch/agentflow-open/commit/87ffc1539bcf33da0fccf45eb15982a02d93e409) · [계획 대비](https://github.com/laadkke-arch/agentflow-open/compare/bb146773bbffba5e724e8c842951e2c25198c2da...87ffc1539bcf33da0fccf45eb15982a02d93e409)
- 진행표는 AF-RES-200을 중앙 `DONE`, `result_commit=1ae3b56d3f445188109c343b00a1b67516f683ce`로 표시한다. 해당 인계의 실제 판정은 `PARTIAL`이며 파일 원값 0/88, 원응답 0/8과 post1 수정 증거 결손을 명시한다. 이 SHA의 releases·notices·advice에서 분모, 날짜/증거 상한, 목적별 구문을 가져온다. 별도 브랜치의 증거 의존으로 고정했다. [진행표](https://github.com/laadkke-arch/agentflow-open/blob/87ffc1539bcf33da0fccf45eb15982a02d93e409/docs/automation/dot-control.json) · [고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/1ae3b56d3f445188109c343b00a1b67516f683ce/docs/workstreams/research/AF-RES-200/HANDOFF.md)
- [시작 계약](af-res-216.json)의 소유 경로는 이 폴더로 한정한다. 공용 계약, 진행표와 색인은 편집 담당자의 영역이다. AF-RES-205의 NumPy 버퍼, 206의 영국 격자, 207의 DivEMT 집계는 표집 밖이다. [제품 브리프](https://github.com/laadkke-arch/agentflow-open/blob/bb146773bbffba5e724e8c842951e2c25198c2da/docs/product/RESEARCH_BRIEF.md) · [연구 운영](https://github.com/laadkke-arch/agentflow-open/blob/bb146773bbffba5e724e8c842951e2c25198c2da/docs/RESEARCH_WORKFLOW.md)

## 사전에 고정한 모집

| 프로젝트 | 앞판 | 대상판 | 뒤판 | 삭제 집단 자리 |
| --- | --- | --- | --- | --- |
| matplotlib | 3.9.0 / 29 | 3.9.1 / 24 | 3.9.1.post1 / 29 | 3.9.1 Windows wheel 집단 1 |
| pytest | 8.0.2 / 2 | 8.1.0 / 2 | 8.1.1 / 2 | 0 |

파일 고유 키 88개(대상 26, 인접 62)와 집단 1개는 고정한다. 이 숫자는 사건 2건이나 직접 연 자료 수와 별개다. 직접 읽을 22자리의 유형별 하한은 version JSON 6, Simple JSON 2, HTML 6, 규칙 3, 당시 원기록 3, 출판 원문·공고 2다. 읽기 실패·미러·동일 원문의 절·검색 요약·파일행·합성 통제는 하한 산입에서 제외한다. 사후 보강은 근거 원장에 따로 표기한다.

## 판정과 반증 규칙

- Q1. PyPI 공개 HTTPS에서 여섯 version JSON과 두 project Simple JSON을 우선 한 번씩 받는다. Simple에 지정 Accept를 보낸다. 응답 상태·최종 URL·Content-Type·조회 UTC·원 바이트의 SHA-256 및 원레코드 위치를 남긴다. 오류와 정상 목록의 부재를 구별한다. 캐시/조회 간 변화는 직렬 번호와 HTTP 날짜를 함께 본다.
- Q2. version JSON의 info는 판 문맥으로만 사용하고 파일 판정은 urls 배열의 boolean yanked와 별도 yanked_reason에 둔다. Simple files 배열의 false, true, 비어 있지 않은 문자열은 각각 미철회, 무사유 철회, 사유 있는 철회를 뜻한다. 키 결측과 명시적 false는 다른 원값이다. Simple 빈 문자열은 현행 규격에서 허용된 사유 문자열이 아니므로 별도 이상/보류로 분류한다. HTML Simple 링크의 빈 속성 규칙은 JSON에 옮기지 않는다. 모든 원값·형을 보존한다.
- Q3. 기준판과 두 현 응답을 프로젝트·정확한 판·정확한 filename으로 전수 합집합 조인한다. 파일명에서 wheel 태그, 이름의 프로젝트 및 판을 읽고 version route와 충돌하면 밝힌다. 동일 이름·타판이나 인접판 prefix를 끌어오지 않는다. digest·태그·중복·한쪽 누락·신규·양쪽 부재를 기록한다. 중복에 최초/최후 레코드를 임의 선택하지 않는다. 기준 목록에 없는 현재 파일도 신규 자리로 남긴다.
- Q4. 파일별 Python 제약·업로드 원값, HTML release 배너와 날짜를 대조한다. 태그와 URL 표시는 설치 지원이나 배포물 내려받기 성공을 측정하지 않는다. 삭제 자리의 정확 파일명·태그·시각에는 별도 원출전이 필요하다.
- Q5. 현재 플래그를 과거 플래그 시점으로 소급한 행의 목표는 0이다. 업로드, 현재 페이지가 표기하는 철회 날짜, 유지자 발언, 당시 소비자 실측 로그를 연결해도 최초 철회 시간과 실제 고장 범위는 각각의 증거로만 기록한다.
- Q6. 200에서 연결한 출판사 원저·공고 한 쌍을 직접 대조한다. 판, 공고 대상, 일자, 원문 주소 상태를 읽는다. 학술 편집 상태와 설치기의 후보 선택은 각각 자기 문서의 규칙을 따른다.
- Q7. 합성 통제로 원필드 결측·false·true·빈 이유·문자열, 같은 파일명의 타판, 신규·누락·삭제·digest/태그 차이·중복을 검증한다. 실제 입력과 경로 및 집계를 분리한다. 접근 가능·다운로드·후보·실제 실패를 독립 축으로 유지한다.

## 노출과 완료

범위 고정 전에 AF-RES-200의 사용자 목적별 판단, 예상 목록과 표시 날짜, 세 규격 문서의 방법론을 읽었다. 기존 목록 일치 및 대상판 철회가 가설이다. 이 범위 커밋 전에는 AF-RES-216의 API 응답이나 파일별 값을 보지 않았다.

여덟 직접 응답 및 UTC·지문, 기존 키 88과 삭제 집단 1, 현 합집합과 26/62 분리, 통제와 새 프로세스 재생, 종류별 하한, Q별 근거와 반증을 확인한다. 핵심 접근·재생·최소치가 실패하면 실제 수치와 재개 지점을 PARTIAL로 남긴다. 계약·범위 검사와 고정 결과 재독을 HANDOFF의 별도 마지막 커밋에 앞세운다.
