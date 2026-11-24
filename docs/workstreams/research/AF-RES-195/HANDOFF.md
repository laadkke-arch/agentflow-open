# AF-RES-195 #1 HANDOFF · PARTIAL

## 결과판과 저장 위치

- 저장소 `laadkke-arch/agentflow-open`, 작업 브랜치 `work/research-af-res-195`, 시작 통합 SHA `72cf39aea54e2de2ba78a245593aefdc40205a16`. 계획 SHA `0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6`부터의 변경은 진행표에 한정됐다. 의존 AF-RES-181 중앙 DONE·자체 PARTIAL 결과 `a5d9b2cc5f295fe5cb15764e3965c14326c872d9`를 고정했다.
- 결과 SHA는 이 인계의 직전 커밋 `a2fe008274607a4383e90a61d23a74938874d499`이다. 2026-11-24 20:37 UTC까지 해당 SHA와 원격 브랜치 일치를 확인했다. GitHub 고정 주소에서 결과 처음과 마지막, 자체점검, 입력, 배정 및 분절, 원장 및 검증 출력을 다시 읽었다. [고정 결과](https://github.com/laadkke-arch/agentflow-open/blob/a2fe008274607a4383e90a61d23a74938874d499/docs/workstreams/research/AF-RES-195/RESULT.md) · [자체점검](https://github.com/laadkke-arch/agentflow-open/blob/a2fe008274607a4383e90a61d23a74938874d499/docs/workstreams/research/AF-RES-195/SELF_CHECK.md)
- 묶음 ① `f826519f759b0dc2844f8da62aecd4f05166cead` [범위와 분모](SCOPE.md), ② `04a0dd7e1a4805ae1d8f7ce61c7cb558f9c6d0ba` [입력과 모집](inputs.json), ③ `723fbcd3434e1e33eb1b4adeab19adfab606cb67` [배정](assignments.csv)·[분절](segments.csv), ④ `118413f48a824f0abb11d57a13b631cf3d2344dc` [반례와 역할 경계](bounds.csv), ⑤ 위 결과 SHA의 [결과표](RESULT.md)·[자체점검](SELF_CHECK.md), ⑥ 이 인계. 02–05의 고정 SHA에서 체크섬 9/13/8/14건이 맞았다.

## 확인 범위와 남은 기준

- Codex Cloud Linux에서 고정 ZIP 두 개, 언어별 main 107문서에서 실제 첫 네 문서, 예정 24/24자리, 원 .pej와 완료 .per 24/24를 확인했다. 같은 원문에 서로 다른 세 사람을 연결했다. raw 96개 조건 분절과 고정 저자 파서의 지표·입출력 지문이 일치했다. 181 TUR HT 5/5행은 2,061,853ms와 111단어가 재현됐고 공개 뷰어의 다섯 행도 별도로 일치했다. 32 삼중쌍에서 PE1과 PE2는 각각 HT보다 9개에서 길었으며 ms 동률 0, canonical 미완료 0이다. 백업 미완료와 단위·생산자 반례를 별도 보존했다. [원장](sources.jsonl) · [실행](receipts/03.md) · [반례](receipts/04.md)
- 고유 최소치 산입은 .per 24, 코드 5, 설계·스키마·처리 4, 선행·타 분야 7로 40개다. 종류별 부족 수는 0이다. QA/수용에 연결된 독립 키와 노동 시간은 공개 원자료에서 0/96이며, 총노동은 미확인이다. 자체 검토가 종단 재생(파일 10개 일치)과 원자료 키 재검산을 통과했다. 별도 세션/사람의 독립 리뷰는 미확인이다. [재생 영수증](receipts/05.md)
- **미충족**은 정확한 HF 고정 `main.tsv` 대조다. 고정판 ZIP 재실행과 HF 공개 viewer 투영을 별도 근거로 사용했다. HF 고정 행의 복합 키·시간·출력 해시 대조는 ITA 0/48, TUR 0/48이다. 각 언어 최소 한 완전 문서가 필요하고 현재 각각 0/4다. shell의 정확한 resolve 요청은 HTTP 403(종료 22), HF Git 조회는 CONNECT 403, 공개 웹 파일 요청은 Xet CDN으로 넘어간 후 본문 접근 실패였다. 판·파일 SHA 메타데이터는 확인했다. 이 환경의 별도 권한 변경 승인은 없었고 파일 부재나 손상은 미확인이다. [다운로드 영수증](receipts/02.md) · [고정 파일](https://huggingface.co/datasets/GroNLP/divemt/blob/9abd1d1cea118ad7a9946e7f1f5a1a29c2a01762/main.tsv)
- 결과 SHA에서 `python -m workbench.session check docs/workstreams/research/AF-RES-195/session.json --fetch` 종료 0. 원격 통합판 `050278651b11a2a3a49d45baebf41c707c06b700`에서 계약 통과, 소유 경로 이탈 0이다. 진행표는 시작판 대비 diff가 없다.

## 재개의 첫 행동

공개 HF 고정 객체를 가져올 수 있는 실행환경에서 먼저 아래 파일의 바이트를 확보하고 SHA-256을 확인한다. 코드와 두 ZIP은 각각 동일 고정점으로 다시 공급한다. Python 3.12.14 및 pandas 2.2.3을 썼다. 아래 HF 획득 및 `--hf-main`을 통한 실제 파일 비교는 현재 환경에서 미완료다.

```sh
git fetch origin refs/heads/work/research-af-res-181:refs/remotes/origin/work/research-af-res-181
mkdir -p /workspace/af195-input/hf
git clone --no-checkout --no-tags https://github.com/gsarti/divemt.git /workspace/af195-input/divemt
git -C /workspace/af195-input/divemt checkout --detach 934c4106001adeaa982a882d063f33ce0a398217
curl -fL --max-time 120 -o /workspace/af195-input/hf/main.tsv \
  https://huggingface.co/datasets/GroNLP/divemt/resolve/9abd1d1cea118ad7a9946e7f1f5a1a29c2a01762/main.tsv
printf '%s  %s\n' d54867ff860c36a24649266b54d7638a7d503d74ce98a71627af180d92b2f8d9 /workspace/af195-input/hf/main.tsv | sha256sum -c -
d=docs/workstreams/research/AF-RES-195
replay=$(mktemp -d /workspace/af195-input/hf-replay.XXXXXX)
python "$d/extract.py" inventory --upstream /workspace/af195-input/divemt --prior-repo . --out "$replay"
python "$d/extract.py" measure --upstream /workspace/af195-input/divemt --prior-repo . --out "$replay" \
  --hf-main /workspace/af195-input/hf/main.tsv
```

기존 올바른 checkout은 재사용한다. `$replay/segments.csv`의 `hf_state`, `hf_tsv_record`, `hf_event_delta_ms`, `hf_src_words`, `hf_source_match`, `hf_draft_match`, `hf_target_match`의 96행을 확인한다. 특히 ITA doc 1 및 TUR doc 1의 조건별 다섯 분절(총 30행)이 전부 연결되는지 먼저 본다. 실제 바이트, 키나 지문이 다르면 가능한 원자료와 판 차이를 기록해 결과의 유지 여부를 결정한다. 다음 커밋도 이 소유 경로에만 남긴다.

색인 제안 · AF-RES-195 | PARTIAL | DivEMT ITA/TUR 24자리·96분절 원파일/저자 파서 복원, TUR 181의 5행 재현, 고정 HF 바이트 미확보 및 QA 노동 미확인 | RESULT.md + HANDOFF.md | AF-RES-181 a5d9b2cc5f295fe5cb15764e3965c14326c872d9
