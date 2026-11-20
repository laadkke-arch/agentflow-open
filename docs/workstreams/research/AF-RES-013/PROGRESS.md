# AF-RES-013 진행

source_commit: a18d8d2e1575d9b679442134fd0f6f8e17423bfe.
현재: 규칙·의존 결과 직접 읽기, SCOPE/SAMPLING 사전 고정. branch 없음을 원격 확인하고 생성.
다음: 네 계열의 대체층/일반층을 스크리닝하고 역사적 prefix를 작성. prefix 모두 commit/push 후 gold commit.
manifest의 freshness_at_start=local_only는 CLI에 명시 local ref를 준 결과다. 별도 git ls-remote와 clone에서 같은 원격 SHA를 직접 확인했다.
초기 manifest 생성 rev-parse 실패는 의존 branch refs를 fetch하여 해결했다. 외부 API 직접 read-only curl 200 확인, web KEP template 한 주소 실패는 제외 기록 예정.

## 접두부 묶음 준비

30개 접두부(Rust8/Python8/Swift8/KEP6)를 직접 점검했다. R0085의 결합 비교절 누락은 번호순 규칙에 맞춰 복구했고 R0130은 quota 밖으로 이동했다. S0025는 저장소 상태 반영일보다 앞선 공식 최종 결정일 2016-04-01을 cutoff로 쓴다. 중립 ID와 cutoff/내용 hash를 PREFIX_MANIFEST에 남겼다. 이 묶음에는 정답 파일을 포함하지 않는다. 실행은 이 접두부 공개 커밋 이후 시작한다.

## 실행 전 cutoff 정정 — C14

공식 PEP563 Resolution 메일(2017-12-04 16:42:38 UTC)을 직접 읽은 결과, 저장소 Accepted 반영일12월5일보다 하루 이르다. C14는 A/B 모두 미실행인 상태에서 접두부 cutoff만2017-12-04로 정정한다. 최초 접두부30개는8cb2b8e에 있고, 이 별도 정정도 gold 커밋보다 앞선다. 내용·선정·정답을 실행 결과에 맞춰 바꾸지 않았다.
