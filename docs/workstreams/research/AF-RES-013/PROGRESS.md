# AF-RES-013 진행

source_commit: a18d8d2e1575d9b679442134fd0f6f8e17423bfe.
현재: 규칙·의존 결과 직접 읽기, SCOPE/SAMPLING 사전 고정. branch 없음을 원격 확인하고 생성.
다음: 네 계열의 대체층/일반층을 스크리닝하고 역사적 prefix를 작성. prefix 모두 commit/push 후 gold commit.
manifest의 freshness_at_start=local_only는 CLI에 명시 local ref를 준 결과다. 별도 git ls-remote와 clone에서 같은 원격 SHA를 직접 확인했다.
초기 manifest 생성 rev-parse 실패는 의존 branch refs를 fetch하여 해결했다. 외부 API 직접 read-only curl 200 확인, web KEP template 한 주소 실패는 제외 기록 예정.
