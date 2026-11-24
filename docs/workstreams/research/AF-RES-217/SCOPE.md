# AF-RES-217 범위와 판정 규칙

## 질문과 기준

고정 Tesseract 5.3.0에서 eng·ara 언어 파일 여섯 개의 내부 구성과 OEM 0/1 시작 가능성을 확인한다. 탐색기가 개발자의 부분 설계에 필요한 엔진, 모델, 적용 이유를 원문 링크로 묶을 때, 파일 이름에 더해 바이트 식별자·실제 로드 경로·엔진 기능 조건을 제시할 수 있는지 검토한다.

- 배정 1차. 작업 브랜치 work/research-af-res-217, 소유 경로 docs/workstreams/research/AF-RES-217/. 원격 작업 브랜치가 없음을 확인하고 2026-11-24 UTC 최신 통합판 87ffc1539bcf33da0fccf45eb15982a02d93e409에서 시작했다.
- 비교 기준 bb146773bbffba5e724e8c842951e2c25198c2da에서 5커밋 전진, 역방향 0. 두 트리의 차이는 docs/automation/dot-control.json 한 파일이다. 기준판에는 AF-RES-217 항목이 없으며 실제 시작판에 1차 RUNNING, 의존 AF-RES-202, 소유 경로와 실행 정의가 있다. [시작판 작업표](https://github.com/laadkke-arch/agentflow-open/blob/87ffc1539bcf33da0fccf45eb15982a02d93e409/docs/automation/dot-control.json), [기준판 작업표](https://github.com/laadkke-arch/agentflow-open/blob/bb146773bbffba5e724e8c842951e2c25198c2da/docs/automation/dot-control.json)
- 시작판의 AGENTS.md, STATE.md, DOT_AUTOMATION.md, RESEARCH_WORKFLOW.md, CLOUD_WORKFLOW.md, START_HERE.md, 현재 색인의 관련 진입점과 제품 연구 브리프를 읽었다. 제품 브리프와 연구 절차는 지시의 기준판에서도 동일하다. [제품 브리프](https://github.com/laadkke-arch/agentflow-open/blob/bb146773bbffba5e724e8c842951e2c25198c2da/docs/product/RESEARCH_BRIEF.md), [연구 절차](https://github.com/laadkke-arch/agentflow-open/blob/bb146773bbffba5e724e8c842951e2c25198c2da/docs/RESEARCH_WORKFLOW.md)
- 직접 의존은 AF-RES-202 한 건이다. 중앙 DONE은 인계가 확인된 작업 상태다. 인계의 연구 판정은 PARTIAL이며 exact 파일 메타데이터 6/6, 구성 0/6, 실행 0/12를 구별한다. 인계 SHA와 의존 핀은 cc543b8d1b8f8748fa363999b76a55f05de2266c다. models.csv의 12행과 bundles.csv의 목적별 전제를 사용한다. [고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/cc543b8d1b8f8748fa363999b76a55f05de2266c/docs/workstreams/research/AF-RES-202/HANDOFF.md)
- 202 공개 제보의 모집 순서·원사용자 품질과 해결 여부, 재학습과 정확도 순위, AF-RES-205/206/207 데이터와 결과를 표집 밖에 둔다. 아카이브의 제보는 오류 단계의 사례로만 읽는다. 새로운 종합 제품 설계는 이 묶음의 범위 밖이다.

## 모집과 노출

| 단위 | 사전 계획 | 판정 대상 |
| --- | ---: | --- |
| 모델 | 6 | AF-RES-202 A01–A06의 4.1.0 고정 커밋, Git blob과 바이트 수 |
| 모델 × 모드 | 12 | 각 파일 × OEM 0/1의 초기화 및 AF-RES-202 예상과의 대조 |
| 주 실행 | 24 | 12자리 × 독립 프로세스·빈 작업 디렉터리 2개 |
| 직접 원자료 | ≥22 | 고유 모델 6, 고정 모음 안내 3, 엔진 5.3.0 코드·도구·테스트 6, 202 고정 원장·공개 제보 4, Hunspell 공식 계약·실제 aff/dic 3 |
| 통제·사후 보강 | 별도 | 누락 디렉터리, 다른 바이트의 동일 basename, 두 모음과 명시 경로, 흰 페이지, 두 언어 일부 실패, Hunspell 짝 |

범위 확정 시 202의 예상 7(legacy 빌드 조건부 1 포함)·미지원 5, 원장에 요약된 공개 제보, 설치본 판과 5.3.0 패키지의 버전 출력에 노출됐다. 2026-11-24T21:31:30Z에 시작 계약을 만들었고 이 범위 묶음을 고정할 때 여섯 모델의 구성·OCR 실행을 수행하기 전이었다. 탐색 주소, 같은 파일의 절·미러, 검색 요약, 열람 실패는 직접 원자료 하한에서 제외한다. 사후 추가는 사유와 시점을 원장에 남긴다.

## Q1–Q7 판정 규칙

1. **바이트.** 고정 URI에서 받은 원본에 git hash-object, SHA-256, 파일 크기를 계산한다. 202 Git blob과 크기 중 하나라도 다르면 해당 파일 두 모드를 판 불일치로 남긴다. 확인할 수 없는 자산은 환경·접근 결손으로 남긴다.
2. **구성.** 정확판 combine_tessdata -d/-l의 stdout·stderr·종료를 각각 보존한다. legacy 핵심은 unicharset/inttemp/pffmtable/normproto, LSTM 핵심은 lstm/lstm-unicharset/lstm-recoder로 대조한다. config가 있을 때만 -e로 읽고 하위 언어 지시와 기존 사전을 구별한다. 디렉터리 성공, 신경망 역직렬화, 실행 관측은 별개다.
3. **빌드.** CLI와 combine_tessdata를 동일 Debian Tesseract 5.3.0-2 패키지 계열에서 잡고 libtesseract와 실제 Leptonica를 확인한다. 5.5.0 시스템판은 판 식별에만 사용한다. legacy 가능은 도움말 외에 정확 tessdata eng OEM0의 실행으로 확인한다. 구성 부재와 빌드 결측은 별도 원인이다.
4. **실제 접근.** 주 실행마다 새 디렉터리에 검증 바이트 한 파일을 넣고 별도 프로세스에서 명시 tessdata-dir, 단일 언어, 지정 OEM을 사용한다. locale C.UTF-8, OMP_THREAD_LIMIT=1, cwd, PATH, 동적 라이브러리 경로, TESSDATA_PREFIX 조건을 명시한다. strace에서 traineddata open 성공/실패와 실제 fd 읽기를 찾고, 실행 전후의 파일 해시·인벤토리와 묶는다. 다른 모델 접근·누락·이미지 오류는 따로 표시한다.
5. **단계.** 동일한 자체 생성 흑백 두 줄 페이지를 고정한다. 의도한 인쇄 내용은 OFFLINE OCR CHECK와 اختبار القراءة이며, 300 dpi와 PSM 6에서 실행한다. CLI의 Init 실패 메시지와 반환 분기, 실제 접근·본문 처리 후의 종료값, stdout 바이트, 공백 제외 빈 출력, 원문을 각각 기록한다. 결과 판정은 저장된 원출력에서 새 프로세스로 재생한다.
6. **반례.** 주 분모 밖에서 명시 경로가 없는 경우, basename만 맞는 합성 파일, 서로 다른 모음의 eng 같은 이름 두 경로, 흰 페이지, eng+ara의 한쪽 파일만 있는 경우를 확인한다. Hunspell의 공식 aff/dic 계약과 하나의 배포 사전 쌍을 열고 동반 파일 생략을 시험한다. 통제 자료와 원자료를 구별한다.
7. **추천.** 202의 12행 각각을 규칙·직접 구성·경로·Init 결과에 잇는다. 빌드, 언어, OEM 기준으로 최소 링크를 쓰고 다른 조건에서 바뀌는 판단을 명시한다. 단일 페이지 OCR 문자열로 일반 정확도와 사용자 문제 해결 여부를 판정하지 않는다.

초기화 성공은 요청한 모든 언어 파일과 실행 조건을 충족한 경우에만 그 조합의 성공으로 집계한다. CLI 전체 Init이 성공해 일부 언어만 로드된 경우는 부분 성공으로 따로 남긴다. 5개 예상 음성에 대한 정확 파일 접근 및 구성 오류는 유효 관측이다. 핵심 자리·종류별 하한이 미달하면 실제/목표와 사유를 인계하며 PARTIAL을 사용한다.

## 시작 계약

2026-11-24T21:31:30Z, exit 0. 다음 명령의 stdout은 session.json과 바이트가 일치했다. 같은 경로에서 인계 전에 check --fetch를 수행한다.

~~~sh
owned=docs/workstreams/research/AF-RES-217
python -m workbench.session start af-res-217 --allow "$owned/" \
  --dependency work/research-af-res-202=cc543b8d1b8f8748fa363999b76a55f05de2266c \
  --output "$owned/session.json" --fetch
~~~
