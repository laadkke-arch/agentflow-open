# AF-RES-017 진행

- source_commit: `0209117d8ec00af39bd25844d52a18edc7323207`
- branch: `work/research-af-res-017` (원격 부재 확인 후 기준 SHA에서 새로 만듦)
- 실행: ChatGPT 공유 Linux Cloud workspace; GPT-6 Astra Pro; cwd `/workspace/scratch/0514a89035ae/agentflow-open`.
- 고정 입력: 009 `7f627a81199f06da7f7b15f979e7fef25dd17602`,010 `0603f0d2990c7a501dbdfc45fbbba79155f505fc`,013 `eb569f07a3a34ffacf114384ae9b06ad062f5396`,016 `3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc`; 해당 HANDOFF와 요청한 제한 절 읽음. planning REVIEW-4는 `b373862baf009f3f8d37ac01b5437530434f7d31`에서 참고.

## 첫 커밋 전 익명 호스트 점검

2026-11-21 03:45:37~44 UTC; curl -I -L --max-time 15, 인증 미사용. root 응답은 개별 본문 성공 보장이 아니다.

| host | HTTP | 관측 |
|---|---:|---|
| github.com | 200 | ls-remote/clone/fetch도 성공 |
| api.github.com | 200 | 이 세션 root; 개별 API 별도 확인 |
| raw.githubusercontent.com | 200 | redirect 포함 root |
| www.bmj.com | 403 | 차단; 공개 PMC/저자판 또는 웹 열람 도구 사용, 우회 안 함 |
| pmc.ncbi.nlm.nih.gov | 203 | 본문 여부 개별 확인 |
| www.uspto.gov | 200 | 정상 |
| dl.acm.org | 403 | 차단; 공개 저자판 경로 |
| www.nber.org | 200 | 정상 |
| martinfowler.com | 200 | 정상 |
| netflixtechblog.com | 403 | 차단; 웹 공개 열람 경로의 결과 별도 기록 |
| aws.amazon.com | 403 | 차단; 공식 docs.aws.amazon.com 등 별도 공개 자료 사용 |

재개 명령: `curl -I -L --max-time 15 https://HOST` (실제 위 host 대입). 새 호스트는 첫 실제 익명 읽기의 응답/도구 상태를 수집 원장에 추가한다. root 차단을 프록시 변경·임의 우회로 해결하지 않는다.

## 다음 행동

SCOPE/SAMPLING을 원격 커밋한 뒤 계열별 병렬 조사. 원자료 요약은 각 evidence lane에 저장하고 통합 담당만 CASES/sources/SEARCH_LOG와 Git 커밋을 관리한다. coder-b는 A 동결 뒤 새 문맥에서 시작한다.
