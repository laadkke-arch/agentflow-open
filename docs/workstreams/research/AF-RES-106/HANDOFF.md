# AF-RES-106 인계

상태: **COMPLETE_WITH_LIMITATIONS**. 지정된 네 연구 묶음, 결과판의 실제 계약/공통 검사, 고정 GitHub 결과·원근거·반환 fragment 재열람을 완료했다. 고유1차 자료 하한 부족은0개다. 탐색을 마친 경로층 결원4쌍, 엄격한 잔류·미사용 반례 미확보, 역사 생성·실제 브라우저 실행 미확인은 서로 다른 제한이다. 연구 결과는 후속 설계자가 별도로 채택·폐기할 수 있는 한 묶음이며 제품 구현·상시 크롤러·DB 설계를 확정하지 않는다.

- 작업 브랜치: `work/research-af-res-106`.
- 소유 경로: `docs/workstreams/research/AF-RES-106/`만 변경했다. 중앙 `dot-control.json`은 수정하지 않았다.
- **검사받은 결과 SHA: `506f2f6e597899e653d99ab021ed36df0f1e45d6`.** RESULT·SELF_CHECK·집계·재현 코드가 포함된 묶음④다.
- 검사/재열람 영수증 커밋: `fe2504613d05b48024495443b7874730e7a9f3a9`; 원격 확인 UTC `2026-11-24T00:40:37.337Z`.
- 이 HANDOFF는 위 영수증 커밋을 부모로 하는 마지막 단독 파일 커밋이다. 영수증과 HANDOFF를 앞선 clean 결과 SHA 검사에 소급 포함하지 않는다.

## 커밋과 입력 고정

| 묶음 | 원격 커밋 SHA | 원격 확인 UTC | 변경 파일·범위 |
| --- | --- | --- | --- |
| ① 옛 모집단·목적·규칙 | `ccbc56bb0891a5721e4f53438e431df81fc8b2a3` | 2026-11-23 23:40:33 | 579경로; 옛판 입력 |
| ①b source-set 교정 공개 | `1ddac4cec4532121598c3ad3deac4450fc5ac6a5` | 2026-11-23 23:46:44 | 2경로; 새 경로 노출 뒤·새 본문/정답 개봉 전 |
| ② 층·12자리·예측 봉인 | `8054c2221d4023ba03c904d96f13928219d36c3d` | 2026-11-23 23:56:46 | 67경로; 정답 개봉 전 원격 확인 |
| ③ 양판 근거·후계·대조 | `a9aea90170ad8d96d0e6fcb0513473902c7d2d80` | 2026-11-24 00:26:58.715614 | 803경로; 통합 원장과 직접 판독 |
| ④ 결과·집계·반환·재현·자가점검 | `506f2f6e597899e653d99ab021ed36df0f1e45d6` | 2026-11-24 00:37:05.560 | 17경로; 실제 검사의 대상 |
| 결과판 실행·재열람 영수증 | `fe2504613d05b48024495443b7874730e7a9f3a9` | 2026-11-24 00:40:37.337 | 27경로; 결과 파일/봉인 변경 없음 |

각 묶음의 전체 변경 경로·blob·SHA-256·tree·부모는 [checkpoints.json](evidence/checkpoints.json)에 있다. 영수증 묶음의27경로는 해당 Git commit diff로 확인한다. 인증된 GitHub Git Data API의 blob/tree 지문을 로컬 index와 대조하고 `expected_sha`, `force=false`로 게시했다. 기존 커밋·브랜치를 초기화하거나 덮어쓰지 않았다. 로컬 `git push` 인증 실패는 앞선 영수증에 남겼으며 인증 설정을 바꾸지 않았다.

계획 통합판은 `49f603a98188fbf2009c4c490b0539f32d124e38`, 최초 시작 통합판은 `32b6bb32989730df78d521c29a50dbebd3289b46`, 재개 및 검사 끝의 실제 통합판은 `d678d6a92c130380cad96bfcd9e9846f9680503b`다. 관련 파일의 차이는 dot-control 한 파일이며 브리프·운영 규칙·계약은 같은 내용이다. 등록 운영 의존102와 실제 끝은 모두 `c1c0c863e1c349895533d5c66ac63ba6b4fc6176`; 연구 입력은 계속 `092f4c5c56451bceb53e632f4bddf33db6cda168`이다. 기존 workbench manifest를 유지했으며 최신 원격 계약 검사에 통과했다. [재개 비교](evidence/resume-contract.json), [끝 원격 확인](evidence/validation/end-contract.json).

14개 사전 봉인 파일을 그대로 유지했다. `frame.csv` SHA-256은 `5e2010d546b64841c915bc42628d52a1c5bb534886adbeee579eda6997e5147e`, `predictions.csv`는 `b963763c165faae527e3d214dcd44bb471f390778c49787c7744d696909e7d91`다. source-set와 일반 역할의 정의가 경로/선택 노출 뒤 추가됐다는 한계는 [METHOD_AMENDMENT.md](METHOD_AMENDMENT.md), [EVALUATION_TARGETS.md](EVALUATION_TARGETS.md)에 공개했다. 사후 결과로 원 예측·원 목적을 수정하지 않았다.

## 핵심 수치와 결과

[RESULT.md](RESULT.md)는 필수 모집·예측12자리 → 판별24판 자리 → 오류·반환12자리 순서로 시작한다. [frame.csv](frame.csv)는 제외 포함803행, 잔여 적격은 ggplot2 68 + Matplotlib 479 =547개다. A/M/G는 ggplot2 0/57/11, Matplotlib 3/0/476이다. 실제 주 사례8쌍·결원4쌍, 실제 판독16판·결원8판이며, 결원을 실측 음성이나 예측 유보에 넣지 않았다.

| 프로젝트·층 | 원 목적 TP/FP/FN/TN | 실제 양성/음성 | 예측유보/실측미확인/결원 | 일반 시각 역할에서 달라지는 점 |
| --- | --- | --- | --- | --- |
| ggplot2 A | 0/0/0/0 | 0/0 | 0/0/2 | 동일 |
| ggplot2 M | 2/0/0/0 | 2/0 | 0/0/0 | 동일 |
| ggplot2 G | 2/0/0/0 | 2/0 | 0/0/0 | 동일 |
| Matplotlib A | 0/0/2/0 | 2/0 | 0/0/0 | 동일 |
| Matplotlib M | 0/0/0/0 | 0/0 | 0/0/2 | 동일 |
| Matplotlib G | 1/1/0/0 | 1/1 | 0/0/0 | TP2, 양성2/음성0으로 변경 |

원 목적의 실제 양성7/음성1과 일반 역할의 양성8/음성0은 자리 재고다. 층·보조·102 결과를 합친 성능 비율을 만들지 않았다. 음성0인 층의 FPR은 **산출 불가**다. Matplotlib G의 원 목적 FPR1/1은 선택된 음성1개에 대한 값이며 제품 전체 오류율 추정이 아니다. [counts.json](counts.json), [재계산](tools/recalculate.py).

Matplotlib의 두 A 사례는 옛 자원 경로가 없어도 공식 rename/통합과 실제 새 예제가 목적을 잇는 FN이다. `text_rotation`의 회전 후 정렬 목적은 계속되지만 특정 bbox 강조 방법은 바뀐다. G1은 목적/방법은 유지되고 `#multiple-yaxis-with-spines`가 `#multiple-y-axis-with-spines`로 바뀐다. G2는 같은 페이지·fragment·PNG 경로가 계속 사용되면서 Men/Women 점수에서 펭귄 예제로 바뀐다. 원 구체 목적에서는 FP, 일반 grouped-bar 설명에서는 TP다. **G2를 ‘남은 파일이 새 절에서 미사용’ 사례로 세지 않았다.**

보조 추적은 ggplot2 관련 D/R 사건2개의 대표2쌍(양성2/음성0), Matplotlib 적격6커밋을 merge 중복 제외3사건으로 합친 뒤 주 A1/A2와 겹치지 않는 mathtext→text 1쌍(FN1, 양성1/음성0)이다. 주 오류율과 합치지 않았다. 엄격한 잔류·미사용 반례는 이 범위에서 미확보다. 경로는547개 전수 검사했지만 의미 판독은 제한됐다. GG 새 본문68개 중9개를 읽었고59개는 미확인, MP G476개 중6개를 읽었고470개는 미확인이다. [보조 분모](evidence/supplemental-summary.json), [GG 최종 판독](evidence/ggplot2/FINAL_AUDIT.md), [MP 최종 판독](evidence/matplotlib/FINAL_AUDIT.md).

고유 신규1차 자료는 **38개**다: 서로 다른 예제 본문15, 그와 별계보 그림/소스6, 공식 변경 사건10, IIIF5, JATS2. `sources.jsonl`의670행은 고유 저작수가 아니다. 양판·같은 문서 앵커·같은 예제 PNG/source·merge·재열람·102 계승·실패를 중복 산입하지 않았다. [sources.jsonl](sources.jsonl), [38개 allowlist와 계보](evidence/crossdomain/source-count-review.json), [정규화 기록](evidence/source-reconciliation.json).

IIIF에서는 Canvas/AnnotationPage/painting body와 thumbnail을 구분했고 Fitzwilliam의 Choice17·null 좌표32건은 viewer의 정상 영역 이동으로 간주하지 않았다. JATS 수학적 graph-clustering 논문은 figure9/xref20의 내부 연결과 실제 HTML id를 대조했다. Fig7 본문 참조4회는3문단이며, 별도 Table3 caption의 Ncut→Fig7 Nassoc 의미 충돌을 보존했다. Fig8로 자동 교정하지 않았다. [Q7 원근거·판독](evidence/crossdomain/CROSSDOMAIN_FINAL.md), [정확 IIIF payload](evidence/crossdomain/iiif-return-payloads.json).

## 실제 검사와 재열람

모든 명령은 결과 SHA `506f2f6e597899e653d99ab021ed36df0f1e45d6`의 깨끗한 사본에서 실행했다. 실행 전후 HEAD가 같고 clean이었으며 영수증 쓰기는 검사 종료 뒤였다.

| 실제 명령 | UTC 시작 → 종료 | 종료값·확인 범위 |
| --- | --- | --- |
| `python -B docs/workstreams/research/AF-RES-106/tools/verify.py` | 2026-11-24 00:37:15.142873 → 00:37:15.486327 | 0; 구조·봉인·원장·선정·자료계보·fragment·필수표147개 통과 |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-106/manifest.json --fetch` | 2026-11-24 00:37:15.497066 → 00:37:21.866396 | 0; 명시 manifest1개 remote_checked, 변경1452경로 owned 안, outside/unmerged/errors0 |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 2026-11-24 00:37:21.875573 → 00:37:42.556186 | 0; 공통 검사 통과. 자동 sessions0은 not-executed/no_active_sessions/not_checked |
| `python -B docs/workstreams/research/AF-RES-106/tools/readback_result.py` | 2026-11-24 00:37:53.191183 → 00:38:35.698997 | 0; 고정 결과24파일+고정 원 HTML16절+MP 버전8문서, 48/48 성공 |

명시 작업 검사1개와 공통 자동 발견0개를 분리했다. 공통 acceptance의55+7+9 단위검사는 workbench용이며 연구 의미 판독의 정확도 검사가 아니다. 고정 결과24파일에는 대표 PNG5개와 필수 표·재현 절차가 포함된다. root가 GitHub connector로 RESULT 세 표와 reproduce를 직접 다시 읽었으며, HTTP 원문/지문/actual id와 실제 browser scroll을 구분했다. 전체 명령·출력·SHA-256·UTC·원격 확인은 [VALIDATION.md](VALIDATION.md), [실행 영수증](evidence/validation/run.json), [48건 재수신](evidence/validation/readback.json)에 있다.

별도 AI의 원장/표 대사318개가 통과했고, A2/G2·Q7·자료계보를 다른 담당자가 직접 재검토했다. 과거5사례 별도 판독에는 일부 결과 노출이 있어 완전 맹검이라고 부르지 않는다. 같은 모델 계열의 AI 분담이며 사람·외부 전문가 검토는 없다. [별도 대사](evidence/crossdomain/final-root-review.md), [A2/G2 검토](evidence/ggplot2/review-matplotlib.json), [Q1~Q7 자체 점검](SELF_CHECK.md).

## 미확인·미실시와 재개 첫 행동

실제16판의 당시 생성 G는 모두 **미확인**이다. run ID·환경 lock·실행별 output manifest/digest와 발행 연결을 확보하지 못했다. 소스·정적 참조·파일 존재를 G로 바꾸지 않았고, 선행의 빈 역사 실행36조회를 반복하지 않았다. 브라우저 redirect/fragment scroll·IIIF viewer·R/Python 예제 실행은 **미실시**다. 현재 버전 사이트 PNG2개는 고정판과 bytes가 다르지만 픽셀이 같고 metadata 차이임을 확인했다. [byte/pixel 대조](evidence/matplotlib/live-byte-vs-pixel-review.json).

남은 핵심 불확실성을 조사할 때 첫 행동은 **현재 원격 끝과 이 HANDOFF를 읽고, 기존 예측을 유지한 별도 사전등록 범위를 만드는 것**이다. 엄격한 잔류·미사용 방향은 `frame.csv`의 GG 미판독59개·MP G미판독470개를 후보로 삼되 이번 선택12자리를 사후 보충하지 않는다. G2의 원 목적 NO를 반박하려면 고정 새 gallery 안에서 Men/Women·G1~G5·원 점수·수치라벨 목적과 저자 계보를 함께 잇는 실제 절을 제시해야 한다.

검사 재현의 정확한 입력은 위 결과 SHA의 clean checkout, 해당 SHA의 manifest, 등록 의존 `c1c0c863e1c349895533d5c66ac63ba6b4fc6176`이다. 그 checkout의 저장소 루트에서 위 `verify.py`, `workbench.session check`, `cloud_check.py` 명령을 그대로 실행한다. raw 자료 재수신/저자용 재생성은 파일을 갱신하므로 [reproduce.md](reproduce.md)의 별도 복사본 절차를 따른다.

브라우저 도착을 추가 확인할 입력은 [returns.csv](returns.csv)의 `old_rendered_url`/`new_rendered_url` 8개와 MP-A1/A2의 새 루트에서 옛 경로를 여는 임시 주소다. 특히 `https://matplotlib.org/3.7.0/gallery/text_labels_and_annotations/text_rotation.html#default-text-rotation-demonstration`과 `https://matplotlib.org/3.7.0/gallery/spines/multiple_yaxis_with_spines.html#multiple-yaxis-with-spines`를 실제 브라우저에서 열고 최종 URL·실제 스크롤된 절·화면 영수증을 남긴다. 새 권장 주소는 각각 `demo_text_rotation_mode.html#text-rotation-mode`, `multiple_yaxis_with_spines.html#multiple-y-axis-with-spines`다. 이 절차는 이번에 실행하지 않았다. 역사 G는 대응 run을 아직 특정할 수 없어 실행 명령을 확정할 수 없으며, 필요한 첫 입력은 해당 고정 발행의 보존 run ID와 실행별 output manifest다.

색인 제안 한 줄: **AF-RES-106 — 첫40 밖 고정 두 판의 예제 링크 후계: 잔여547·주8실제쌍/4결원, 원 목적 MP A FN2·G FP1(일반역할 TP로 전환), 자료38, 미사용 잔류 반례 미확보·G16미확인; exact fragment/payload와 목적별 반환 선택지·재현·검사 근거는 RESULT/HANDOFF 참조.** [INDEX_PROPOSAL.md](INDEX_PROPOSAL.md).

| 가장 중요한 불일치·약점 | 다음 조사 제안·직접 열 자료 또는 실행할 입력 | 어떤 관측이면 판단을 바꿀지 |
| --- | --- | --- |
| 잔류 경로·새 절 미사용의 엄격한 반례는 미확보. G2는 같은 경로의 내용 교체이며 원 목적 FP/일반 역할 TP로 갈린다. | 같은 고정판 GG 미판독59개·MP G미판독470개를 새 규칙으로 사전등록하고 exact section/src/srcset/source를 검사한다. | 자원 경로가 남아도 대응 목적 절에서 미사용인 실제 예제, 또는 G2 원 점수 목적의 정확한 후계가 나오면 해당 방향·NO 판정을 바꾼다. |
| source-set와 일반 역할 정의가 경로/선택 노출 뒤 추가됐고, 원 목적 음성은1개다. | 보존된 man-only와 넓은 source-set을 다른 미노출 버전/프로젝트에서 고정해 비교하고 독자의 필수 목적을 먼저 기록한다. | 정의·표본 변화에 따라 FP/FN이 사라지거나 반전되면 신호의 효용과 목적 단위를 재평가한다. |
| 정적 참조와 실제 도착·역사 생성은 다르며 G16판과 browser/viewer 동작은 미확인이다. | 정확 반환 URL/fragment의 실제 브라우저 이동, 같은 과거 발행의 보존 run ID·환경 lock·output manifest/digest를 확보한다. | 실제 이동이 다른 절을 가리키면 반환을 수정하고, 실행별 출력과 발행 연결이 확인되면 해당 G를 YES/NO로 갱신한다. |
