# AF-RES-106 재현 절차

## 입력을 고정한 순서

이 묶음의 예측을 다시 계산하는 일과 이미 열린 정답을 모르는 상태로 새 실험을 수행하는 일은 다르다. 아래 재계산은 보존된 입력·선택·판독의 일관성을 검사한다. 사후 실행을 사전 예측의 새 증거라고 부르지 않는다.

| 단계 | 원격 고정판 | 그때 허용한 입력 |
| --- | --- | --- |
| 시작 통합판 | `32b6bb32989730df78d521c29a50dbebd3289b46` | 계획판 `49f603a98188fbf2009c4c490b0539f32d124e38`과 관련 파일 비교. 변경은 dot-control 한 파일이며 브리프·계약·운영 규칙은 같은 blob |
| 연구 입력 | `092f4c5c56451bceb53e632f4bddf33db6cda168` | AF-RES-102의 검사받은 결과·frame·predictions·lineage·counts. 운영 의존 핀은 `c1c0c863e1c349895533d5c66ac63ba6b4fc6176`이며 시작 끝과 일치 |
| ① 옛 모집단 | `ccbc56bb0891a5721e4f53438e431df81fc8b2a3` | 옛 배포 트리와 원 HTML·옛 source·목적. 새판 본문·그림·patch는 닫음 |
| ①b 규칙 교정 | `1ddac4cec4532121598c3ad3deac4450fc5ac6a5` | 새 경로 신호를 본 뒤 source-set 규칙을 교정했음을 공개. 새 본문·정답 개봉 전. man-only 원 초안 보존 |
| ② 예측 봉인 | `8054c2221d4023ba03c904d96f13928219d36c3d` | 완전한 새 경로 집합과 Git 변경 종류, 12자리·6 YES/2 NO/4 결원. 원 목적과 추가 일반 역할 모두 고정 |
| ③ 정답 판독 | `evidence/checkpoints.json`의 stage 3 | ② 원격 확인 후 양판 본문·실물·source·공식 patch·타 분야 및 별도 판독 |
| ④ 결과 | 최종 `HANDOFF.md`에 적은 검사 대상 결과 SHA | RESULT·SELF_CHECK·집계·반환·재현. 후속 영수증과 HANDOFF는 해당 결과 검사의 대상이 아니며 별도 커밋 |

`evidence/checkpoints.json`에는 각 묶음의 부모·tree·원격 확인 UTC·변경 경로와 blob/SHA-256이 있다. 예측 파일의 봉인 SHA-256은 `b963763c165faae527e3d214dcd44bb471f390778c49787c7744d696909e7d91`이다. `evidence/stage2-seal-manifest.json`의 14개 파일은 정답 개봉 뒤 수정하지 않았다.

## 환경과 실행의 의미

실제 조사 환경은 Python 3.12.14, lxml 6.1.1, Pillow 13.0.0이다. 저장소 공통 검사에 필요한 환경은 저장소 자체 계약을 따른다. GitHub에서 받은 R/Python 예제는 텍스트로 읽었고 실행하지 않았다. PNG/JPEG 디코드와 정적 HTML/JSON/XML 파싱을 실제 예제 실행이나 역사적 빌드 G로 바꾸어 보고하지 않는다. 브라우저의 redirect·fragment scroll·IIIF viewer·GUI/JavaScript 표시는 **미확인**이다.

고정 결과판을 checkout한 깨끗한 저장소 루트에서 아래 명령을 실행한다. 이 문서가 있는 브랜치의 최종 끝에는 영수증/HANDOFF가 추가되므로, 과거 검사와 같은 상태를 재현할 때는 HANDOFF의 **검사받은 결과 SHA**를 사용한다.

```sh
git status --porcelain
git rev-parse HEAD
python -B docs/workstreams/research/AF-RES-106/tools/verify.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-106/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

`tools/verify.py`는 입력 파일을 바꾸지 않고 구조·봉인 지문·선택식·혼동표·독립 자료수·원장 연결을 재계산한다. 저장소 session 검사는 명시한 manifest 1개를 검사한다. 공통 cloud 검사의 `sessions`가 자동 발견한 실제 세션 수는 따로 읽어야 한다. 자동 발견 0개를 명시한 연구 manifest의 검사를 통과한 것으로 해석하지 않는다. 실제 UTC·HEAD·종료값·stdout/stderr·clean 상태는 `evidence/validation/`의 영수증에서 확인한다.

## Q1: 옛 모집단

`frame.csv`는 제외를 포함한 803행이고 실제 잔여 적격은 547개다. ggplot2 reference HTML 195개, Matplotlib gallery HTML 608개가 원 목록이다. Matplotlib index/실행요약 51개를 경로로 분리하고 나머지 557개 중 redirect 36개와 논리 본문 521개를 구분한다. 선행40+교정2는 경로로 먼저 제외했으므로 직접 수신·파싱한 옛 HTML은 **515개=잔여 후보479+redirect36**이다. 이는557개 전체를 모두 새로 GET했다는 뜻이 아니다. 정확 수신 방식과 캐시/redirect 구분은 해당 수신 원장으로 대사한다. **자동 스캔 수를 신규 고유 자료수로 세지 않는다.**

프로젝트별 원장 `evidence/ggplot2/stage1-frame.csv`, `evidence/matplotlib/stage1-frame.csv`와 root `evidence/stage1-frame-summary.json`에서 제외 이유를 재계산한다. ggplot2는 기존40·교정2·선행 별칭3·잔여 내부 별칭4·Examples 없음57·연결 자원 없음21을 제외하여68이다. Matplotlib은 기존40·교정2·index/요약51·redirect36을 제외하여479이며, 이미지440·다운로드 전용39·인라인 전용0이다. 접근 실패와 인라인 전용은 별도 열/요약에 유지한다.

ggplot2의 별칭은 코드·데이터·목적·API와 실제 그림을 함께 비교했다. 해시가 같다는 이유만으로 qplot/stat_identity를 제외하지 않았다. Matplotlib `hyperlinks_sgskip`의 import-only 첫 블록은 실제 첫 scatter→set_urls→SVG 예제의 준비 코드로 이어진다. 이 경계 교정과 초기 validator 실패는 봉인 전에 기록했다.

원 수집/판독 스크립트는 `evidence/ggplot2/collect.py`, `finalize_stage1.py`, `old_author_sources.py`, `evidence/matplotlib/acquire_old.py`, `finalize_old.py`다. 출력 위치가 고정되어 있으므로 **재수신은 별도 복사본에서만** 실행한다. 전체 배포 archive와 Git object cache는 재취득 가능한 작업 캐시로 커밋하지 않았다. 필요한 경로 목록·blob·수신 영수증·선택한 실제 원문/절·지문은 커밋했다. 네트워크 재현 시 수신 실패도 새 영수증으로 보존한다.

## Q2–Q3: 경로 신호와 선택·예측

1. 프로젝트별 old/new 완전 tree 목록 및 `truncated=false`, subtree와 root의 연결, source DAG 완전성 영수증을 읽는다. 버전 디렉터리만 제거하고 대소문자·확장자·fragment·1x/2x는 유지한다.
2. 후보별 대표 외부 자원이 새 tree에 없으면 A. 아니면 옛 본문이나 확인한 예제 source-set의 경로가 사라지거나 이동했으면 M. 나머지는 G. blob 변경만으로 M을 만들지 않는다.
3. `SHA256(UTF8('AF106|' + project + '|' + old_section_path))`를 계산한다. project는 정확히 `ggplot2` 또는 `Matplotlib`; old_section_path에는 실제 옛 fragment가 포함된다. 각 층 hash 오름차순·동률 경로순 앞2개, 부족하면 결원이다.
4. 새 완전 tree에서 옛 자원 경로 존재→YES, 부재→NO, tree/외부 대상 불명→유보다. 결원은 유보와 다르다. 임시 URL은 새 루트+옛 페이지/fragment이며 결과 반환 URL과 별도로 남는다.

최종 모집은 ggplot2 A0/M57/G11, Matplotlib A3/M0/G476이다. 선택은 실제8쌍·결원4자리다. `tools/assemble_frames.py 2`와 `tools/assemble_predictions.py`는 root 파일을 덮어쓰므로 별도 복사본에서만 실행한다. 검사용 `tools/verify.py`는 보존 원장을 읽기만 한다. ①b의 규칙 교정과 Matplotlib 일반 역할 해석은 새 경로/선택 노출 뒤였다는 한계를 숨기지 않는다. 원 목적/예측을 사후에 교정하지 않았다.

## Q4–Q6: 원문, 후계, NO와 혼동표

프로젝트별 `audit.json`, `lineage.csv`, `returns.csv`, `sources.jsonl`은 같은 사례의 절→자원→발행 코드→저자 source→공식 변경을 잇는다. root `lineage.csv`는 결원까지 포함한24판 자리이며 root `returns.csv`는12자리다. `P`, 옛 경로 P, 옛 fragment DOM, 정적 redirect 연결, 실제 browser arrival, 원 목적 U, 일반 역할 U, 구체 방법/핵심 API, literal 데이터, G를 나눈다.

Matplotlib barchart 원 목적의 NO는 그 첫 URL에서 찾지 못했다는 뜻이 아니다. 새 발행 Python bundle522개에서 옛 basename·G1~G5·Men/Women·점수·bar/bar_label 특징을 전수 검색하고, 검색 후보5개와 공식 barchart 변경 diff를 직접 대조한 **해당 gallery 범위의 부재**다. 다른 예제에 Men/Women 점수만 있거나 막대가 비슷해도 side-by-side+수치 label이라는 원 목적/제약이 모두 이어지는지는 별도 읽는다. 저장된 검색 영수증과 후보 판독을 먼저 확인한다. 미확인을 NO로 채우지 않는다.

각 project×stratum에서 `U_original_purpose`와 `U_visual_role`을 따로 평가한다. YES 예측/YES 실측은 TP, YES/NO는 FP, NO/YES는 FN, NO/NO는 TN. 실측 미확인·예측 유보·결원은 혼동표 네 칸에 넣지 않는다. 실제 양성은 TP+FN, 음성은 FP+TN이며 분모0의 FPR/특이도는 `산출 불가`다. 주8쌍·보조·102 과거 사례를 합친 전체 성능을 만들지 않는다.

보조 경로는 봉인한 `supplemental-selection.json`의 committer UTC→SHA 순서다. ggplot2 연결 사건2개, Matplotlib raw D/R 관련6커밋은 merge를 합쳐3사건이다. 주표본 중복과 같은 사건 merge를 독립 사례로 추가하지 않는다. ggplot2 mass rename의 여러 경로는 경로검사였으며 모두 의미를 전수 재판독한 것은 아니다. 세부 의미 판독 대표와 아직 안 읽은 나머지를 별도 분모로 보고한다. 공식 추가 자료를 더 읽었어도 사전 보조 선택의 분모를 뒤에서 늘리지 않는다.

## Q7: IIIF와 JATS

현재 공개 실물의 보존 bytes·지문은 `evidence/crossdomain/`에 있다. 두 박물관 manifest, IIIF Presentation/Content State, JATS1.3, PLOS XML/HTML/그림의 14성공 URL을7저작으로 합친다. 아래 스크립트는 정적 관계를 재계산하지만 출력 파일을 갱신하므로 역시 별도 복사본에서 실행한다.

```sh
python -B docs/workstreams/research/AF-RES-106/evidence/crossdomain/analyze_static.py
```

확인할 값은 Night Watch Canvas1/painting1/thumbnail 분리, Fitzwilliam Choice17/comment32 및 null 좌표32, PLOS figure9/figure-xref20/실제 HTML id9다. Fig7의 xref5는 올바른 본문4와 지표가 어긋나는 Table3 caption1로 나눈다. XML의 점 구분 id를 실제 DOM의 하이픈 id와 혼동하지 않는다. IIIF 정확 payload는 `iiif-return-payloads.json`이며 실제 viewer URL이나 교정 좌표를 만들어 넣지 않았다.

## 자료수·검토·결과판 재열람

`sources.jsonl`은 각 직접 열람과 자동 스캔/실패/계승을 구별하고 `evidence/source-reconciliation.json`은 동일 논리 예제·양판·동일 사건·번들/그림/규격 앵커 중복을 합친다. body8 이상, 별계보 source/payload6 이상, 공식 기록6 이상, IIIF 규격/실물 및 JATS 규격/실물 각2 이상을 각각 확인한다. URL 수·HTTP 요청 수·독립 저작 수·독립 사례 수는 다르다.

별도 AI의 stage1/stage2 검토와 결과5사례의 독립 판독은 `evidence/crossdomain/review-stage*.json`, `independent-outcomes.json`에 있다. 같은 계열 모델의 분담이며 사람/외부 전문가 검증이 아니다. root의 원 XML·선택 code 재독은 작성자 결론을 안 상태의 확인으로, blind 판독에 합치지 않는다.

결과 커밋 후 GitHub의 고정 SHA에서 RESULT 세 표·대표 원근거/출력·이 재현 절차를 다시 연다. 반환 절의 actual DOM id와 고정 source line/자원 지문을 재대조하고, raw HTML#id를 실제 렌더된 역사 사이트의 scroll 성공으로 말하지 않는다. Matplotlib의 버전 사이트 URL은 실제 GET 원문과 고정본의 절/자원을 비교한 범위에서만 읽기 링크로 제시한다. 이 마지막 재열람 영수증과 두 저장소 검사 영수증을 추가 커밋한 다음 HANDOFF를 마지막 단독 커밋으로 남긴다.
