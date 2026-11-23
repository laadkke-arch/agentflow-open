# Frame A 최종 조사 메모 — 부분 인계 입력

이 stream은 root가 통합·커밋한다. 생성 파일은 모두 `docs/workstreams/research/AF-RES-062/streams/a/` 아래에 있다. 메타데이터 모집 동결판은 `fd80a75d5ee3a77f89291f82fd3fb2b90975be3b`, 운영규칙 R0은 `27dc28648c125186d1b79c5e629c97210e57b23e`이다. AF-RES-058 파일은 코호트/DOI 중복 확인에만 사용했고 그 원행을 재분석하지 않았다.

## 실제 모집·심사 상태

34개 원 서지 레코드 중 범위/토픽 메타데이터 제외5개, 후보29개. 발행일→DOI순 최초25개를 방법 심사 대상으로 동결했다. 현재 **원 방법 본문22건 + 저자 포스터 방법1건 =23/25**를 직접 확인했다. 적격2, 제외21, 본문 미확인2(A-F17,A-F21)다. 후보 밖 후속 자료로 빈자리를 채우지 않았다. 학회 native 검색은 접근 실패했고 한정된 검색엔진 반환 집합을 사용했으므로 전수 모집이라고 주장하지 않는다.

F06와F09는 publisher403 뒤 공개 Wayback PDF를 실제 회수해 방법을 읽었다. F17은 출판사 현행판, CityU 저자기관, ResearchGate, CDX pdf/full/epdf/landing과 보관 landing까지 확인했다. 보관 landing은 초록/참고문헌만 제공한다. F21은 출판사, NIM 저자목록, OPUS기관, ResearchGate, CDX 네 경로에서 본문을 회수하지 못했다. 요청 버튼을 눌러 저자에게 메시지를 보내지 않았다. 다음 최소 입력은 이 두 논문의 방법/보충판 공개 파일이다.

## 두 적격 자리와 네 자료 연결

| 주 자리 | 배정 | 같은 항목·자극 | 참값·도착 원문 | 최종 판단·수락 | 최초 확정 여부 |
| --- | --- | --- | --- | --- | --- |
| A01, A-F10, Łajewska2024 | [본문](https://krisztianbalog.com/files/sigir2024-transparent-cis.pdf) §3.1/4.3:한 사람1HIT,10문항,query순서 무작위.273제출/113탈락/160유지,조건별16. **HIT조건 무작위배정 미확인** | [고정 자극](https://github.com/iai-group/sigir2024-transparentCIS/blob/065ae48c802e5fcaf9f4c202fad6bfb0aaf0650d/data/input/input_data.csv) Id1–10. [원 output](https://github.com/iai-group/sigir2024-transparentCIS/blob/065ae48c802e5fcaf9f4c202fad6bfb0aaf0650d/results/user_study_output/mturk_output.csv)의`Input.query_id/response`:EC1↔9,EC3↔10 모두10/10동일 | 같은 자극파일`Response good/bad,Source,Source link`/noise열. [Id3 실도착](https://www.ibtimes.co.uk/watergates-40th-anniversary-president-nixons-resignation-1460491)마지막Nixon평판회복절은 현재 일치. 나머지 도착 당시판 전수 감사 미완료 | `WorkerId+Input.query_id+Answer.correctness_{id}.option_{1..4}`.1600평정은 실제 존재. 최종답 선택·권고 수락 종점은 **해당 없음(J4)**. perfect/imperfect≠순수 정오 | 앞선1–9방법 제외 확인. 발견 집합 내 최초 적격 확정; 검색 전수성 미확인 |
| A02 잠정, A-F18, Kim2025Study2 | [사전등록](https://aspredicted.org/bg22-yfw7.pdf)Q2/4,[본문](https://arxiv.org/pdf/2502.08554v1)§4.1:8형식 각1회,12문항중 형식배정/순서무작위.320수집/12제외/308유지 | AppendixF PDFpp23–26의24응답;§4.1.4 PDFpp8–9 설명제거·출처추가 규칙.12질문×2답×3원문=72링크자리,67고유URL; 추출은 독해가 아님 | AppendixF정답키/URL과 root의독립도착감사. 정정·반대원문은 키와 나란히 유지; 현재확인과2024당시판을 구분 | §4.1.2:Agreement=최종답=권고. Table1PDFp10은 평균만. 같은시행 원행/정수교차표는 **미확인(J3)**.정오별수락원개수0셀회수 | 앞선A-F17방법 미확인으로 두 번째 최초 적격은 잠정. A03공석/순위불확실 |

상세 연결·사건 사전은 [methods.md](methods.md)에 있다. 신뢰도·제한 단서가 동시 변경되는A01은 I3, 설명 수준을 고정해 링크를 덧붙이는A02의 비교는 I1이다. A01에는 원행이 있어도 목표 수락 종점이 없고, A02에는 목표 종점이 있어도 공개 원행을 회수하지 못했다.

## 배정·실제 클릭·독해

Kim은 source제공1232시행 중 클릭318/비클릭914를 정수로 보고한다. 클릭318 중 정권고164/오권고154. 사람별0/1/2/3/4과제 클릭빈도189/33/18/23/45는308명, 가중합318시행으로 맞는다. 이는 자발 클릭 분모이며 배정 비교와 분리한다. 본문Time은 질문표시→Next로, 출처 독해시간이 아니다. 원문을 실제 이해했는지는 미확인이다.

TransparentCIS의 source제공128유지참가자 중 source-details 기록 비공백65, link기록 비공백35를 직접 세었다. `source_details_{id}`/timestamp와 URL/일반`Sources`라벨이 섞인다. 배포client사전이 없으므로 비공백을 독해 완료로 부르지 않는다.원자료의 개인행은 재게시하지 않았다.

## 원개수/검산 상태

`outcomes.json`은 Kim의8요인셀(4응답구성×2정오) 및A01의4핵심조건을 담는다. Kim의 조건별 분석시행분모308은 설계/보고에 근거하지만 수락분자·최종정답분자는 미확인이다. Table1반올림 평균만으로 수락 정수를 역산하지 않았다. 출처−무출처 평균차는 무설명 정권고+6.2%p/오권고−10.0%p, 설명포함 정권고+1.7%p/오권고−5.9%p이며 **저자 평균의 기술차**다. 정수 복원/ITT 결과로 쓰면 안 된다. `a`가 없으므로 누락포함수락범위도 미확인이다.

`python -B docs/workstreams/research/AF-RES-062/streams/a/audit_transparent_cis.py`를 이 AI stream이 실제 실행했다. 표준 라이브러리만 사용하며 고정원본 재다운로드는`--fetch`를 붙인다.160명/10조건/1600평정,조건별16명×10문항,본문동일성10/10,각correctness평정의 단일선택을 확인했다. 처음 Boolean대소문자검사오류를 root가 발견했고 정정/재실행했다([audit-corrections.md](audit-corrections.md)). 원개수 수락에 대한 테스트/검산은 종점 부재 또는 원행 결손으로 **미실시**다.

## 파일 색인

- 모집: `candidate-freeze.json`, `frame.csv`, `crossref-candidates.json`, `search-log.jsonl`, `search-log-bibliography.jsonl`, `search-log-postfreeze.jsonl`.
- 직접 독해: `sources.jsonl`26행. 최소량에 산입한18저작=원연구보고서16+별도사전등록1+별도저자패키지1.한논문부록/미러/동일패키지파일은 중복 산입하지 않음. 보수적으로 모델방법심사/저자포스터/도착뉴스기사8행은 최소량에서 제외.
- 방법/자극: `methods.md`, `stimuli.csv`20행, `fostering-source-links.csv`72행.
- 종점/노출: `outcomes.json`12행, `voluntary-clicks.json`2기록, `transparent-cis-audit.json`, `audit_transparent_cis.py`.
- 회수 실패/고정판: `retrieval-log.json`, `archive-attempts.json`, `archive-retrieval.json`, `archive-attempts-remaining.json`, `health-archive-receipt.json`.
- 정정: `audit-corrections.md`.

PDF/원시응답/추출본문은 재현용 ignored `.cache`에만 두며 Git 산출물로 재게시하지 않는다. 고정 URL·해시·집계·명령이 커밋 대상이다.

## 통합 시 가장 중요한 세 약점 → 다음 최소 조사

1. A02수락 정수 없음 → Study2의배정/문항/답키/권고/최종답/제외를 묶는 공개 원행 또는 저자 정수교차표를 회수한다.
2. A01종점/정답키가 목표와 다름 → 평정을 수락으로 바꾸지 말고, 같은주장 binary최종답을 가진 별도 공개 비교를 요구한다.
3. 최초25중2본문·당시원문 전수연결 미확인 → F17/F21방법 파일과 선택된링크의2024당시판을 우선 회수해 순위·지지판정을 확정한다.
