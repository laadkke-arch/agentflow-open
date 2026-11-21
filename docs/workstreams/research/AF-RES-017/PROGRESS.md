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

## 묶음2 — 1차 관측20개

블로그10/PR8/ADR2개를 우선 저장했다. 사례 수는 원문 관측 수이며 엄격한 늦은 발견 적격 수가 아니다. 날짜·실제 채택·원인 진술을 분리하고 후속 검증 중이다. 미구현 ADR의 superseded 상태를 채택 후 되돌림으로 오인할 수 있음을 발견했다. `git push`는 저장된 터미널 인증이 없어128로 실패하므로 기존 GitHub 연결의 tree/commit/ref 기능으로 같은 tree를 게시한다. 계정·권한은 변경하지 않았다.

## 묶음3 — 관측40개 원장

원문 관측40개(a16/b3/c16/e5)를 모았다. 한 계열 최대16/40(40%). 40개 모두를 엄격한 늦은 발견 사례라고 부르지 않는다. 명시적 무지와 실제 수정이 연결된 양성, 알고 거절한 대안, 늦게 출시된 기능, 문서상 계획만 있는 사건을 구분한다. 자료가 없는 날짜·이행 결과는 발명하지 않았다. 묶음2 원격 SHA는 `ad4c76a4afbca53aa755001f79f7c05e3fe12841`. 다음은 고정 판·존재·어휘 입력 검증과 코딩 동결이다.

## 묶음4 — 시점·기능 버전·어휘·현재 검색

묶음3 원격 SHA는 `9f0c34f34db7d05c45c568305aaeccf31f47d1f3`.40관측 중 최소 월별 사건18, A의 좁은 인과 양성4를 구분했다. 존재 yes25/no3/unknown12, 어휘 겹침 중앙값1(0–4), 현재 본문 검증 hit7/40이며 과거 발견 가능성·제품 추가 가치와 분리한다. 모든40need를 별도 INPUTS로 남겼다. 두 ADR은 git fetch 후 고정 SHA 본문으로 재확인했다. 이후 A동결 커밋을 선행시키고 새 문맥·별도 선택 모델의 B코딩을 수행한다.

네트워크 절차의 한계: 첫 커밋 전 계획한11호스트는 점검했지만 검색 과정에서 새로 만난 모든 호스트를 첫 커밋 전에 미리 알 수는 없었다. 새 호스트의 1회 익명 응답은 `evidence/network-followup.json`과 `evidence/methods/NETWORK.json`에 실제 시각으로 기록하며 사전 점검으로 소급하지 않는다. 개별 api.github.com GET는 이번 추가 확인에서403이었다. 재시도나 우회 없이 앞서 성공한 내부 수집 경로의 원문 기록과 정상 git fetch를 사용했다.

## 묶음5 — coder-a 동결

묶음4 원격 SHA `510a6e042a620728d4c290a54b2e56a86adf9eed`. A40개와 라벨을 제거한 원자료 요약 packet,7개 합성 변별력 진단을 동결한다. A의 SHA256은 `84243b48d11f6cd60f3bf9576c0324b3c1446dc9aa68763df9cac58a630a21b4`. 이 커밋을 원격 게시한 뒤에만 B를 시작한다. B는 새 문맥 `gpt-6.2-sol`로 선택하고 A·결과를 읽지 않도록 한다.
