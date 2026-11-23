# AF-RES-101 자가점검

작성 기준 UTC: 2026-11-23T22:29:31Z. 대상은 [SCOPE](SCOPE.md), 첫 봉인 `9d646592613ba2fd9c52bc9bbf3dbc28bac68693`, 후보 봉인 `4e7539906eb03abd46e6910643ed5317f97ddb45`, 동작·후속 묶음 `c68b40e646dffcc41261ea21974c2bbfeab53348`과 이 문서 작성 시점의 분모 대조다. 최초판과 후보 원순서·필터 결과를 사후 근거로 덮어쓰지 않았다. 아래의 직접 확인은 [자료 원장](sources.jsonl)에 URL·UTC·위치·지문을 남긴 작업팀의 실제 원문 열람과 실행을 가리킨다. 이 문서 작성자가 모든 실행을 별도로 재실행했다는 뜻은 아니다.

**연구판에서 같은 제품의 다른 조작을 A가 숨기는 근거는 확보했다. 완전한 후보를 질문자가 이미 알고 있었는지, 새로 알았는지, 원 환경에서 성공했는지를 비교하는 근거는 부족하다.** 이것을 B의 종합 추천 성능이나 인지율로 확대하지 않는다. 최종 RESULT 표 대조, 정확한 결과 SHA의 저장소 검사와 GitHub 재열람은 이 문서 작성 시점에 미실시다. 실제 명령·UTC·종료값·대상 SHA·공통 검사의 세션 수는 이후 HANDOFF의 영수증으로 확인해야 한다.

## Q1~Q7 답과 반대 근거

| 질문 | 답 | 직접 확인한 URL·위치 | 내 결론이 틀릴 경우·찾아본 반대 근거와 결과 | 미확인·판단을 바꿀 최소 후속 확인 |
| --- | --- | --- | --- | --- |
| Q1. 최초 시도 이력을 기준으로 누구를 뽑았는가 | 2024년 상반기 UTC 창에서 현재 태그로 모집한 ImageMagick 첫 60건과 Typst 27건을 생성시각·숫자 ID 순으로 검토했다. 각 태그의 특정 시도 명시 2건·미명시 2건으로 8자리를 채워 하반기 연장은 필요 없었다. 최초 공개 revision으로 선정했으며 답 수·채택·점수로 선정하지 않았다. 최초판 미확보로 채운 자리는 없고 같은 질문 ID의 중복 산입도 없다. | [ImageMagick 질문 API](https://api.stackexchange.com/2.3/questions?site=stackoverflow&tagged=imagemagick&fromdate=1704067200&todate=1719791999&sort=creation&order=asc&pagesize=60), [Typst 질문 API](https://api.stackexchange.com/2.3/questions?site=stackoverflow&tagged=typst&fromdate=1704067200&todate=1719791999&sort=creation&order=asc&pagesize=60), [frame 87행](frame.csv), [IM 획득 영수증](evidence/imagemagick/acquisition-h1.json), [TY 획득 영수증](evidence/typst/acquisition.json). 각 frame 행의 최초 revision URL·본문 해시·탈락 이유를 연결했다. | 현재 제목을 과거로 소급하면 TY #77831146의 정렬 목표를 안다고 오인할 수 있다. 최초판은 확보했으나 목표 이미지가 접근 실패여서 해당 건을 제외했다. IM #77772356의 포맷 지원 목록 질의를 구체 변환 과제로 넓게 보면 IM-A2가 바뀔 수 있으므로 [선정 경계 검토](evidence/initial-boundary-review.md)에 보존했다. TY-U1의 LaTeX 예시는 인지 증거이나 실행 주장과 같지 않다. | 삭제·비공개 질문과 현재 태그에서 사라진 질문은 포착하지 못한다. API 결과는 조회 당시의 공개 표본이다. #77831146의 최초 목표 이미지나 #77772356의 구체 입력·필수 변환 목표가 확보되면 선정 민감도를 다시 계산한다. 원 봉인 표본은 바꾸지 않는다. |
| Q2. 이미 쓴 것은 제품인가, 특정 입력의 조작인가 | 8개 최초 본문의 입력·판·호출/인수·오류·변경 허용 범위를 별도 기록했다. 실제 사용이 있는 A층 4건과 실제 제품 사용 미확인인 U층 4건을 구분했다. TY-A2는 기존 helper와 실패한 plain `red` 인지를 보였고, TY-A1은 페이지 배경과 저자 grid를 사용했다. 언급·예시·희망 구문만으로 실제 사용을 만들지 않았다. | [initial 8행](initial.csv)의 `history`, `original_location`, `initial_body_sha256`; [TY-A2 최초판](https://stackoverflow.com/revisions/1AC32ECA-E650-4B91-BB27-4782FAC3E660/view-source) HTML 3행의 helper·작동 호출·실패 설명; [TY-U1 최초판](https://stackoverflow.com/revisions/8F4CA364-4C5A-456D-8E2A-08242AFE175E/view-source)의 LaTeX 예시와 Typst 질문; [IM-A1 최초판](https://stackoverflow.com/revisions/77774582/1)의 알려진 CLI와 QuickMagick 실행 블록. 재현 가능한 위치는 각 [IM 최초 이력](evidence/imagemagick/initial-part.json)·[TY 최초 이력](evidence/typst/initial-part.json)에 있다. | 코드가 있으면 실행한 것으로 보는 대안 해석을 검토했다. TY-U1은 LaTeX 문법을 알고 있으나 실제 실행 또는 Typst 시도를 진술하지 않는다. TY-A1에서 `grid()` 함수 자체를 보존 조건으로 만들면 per-item box 같은 대안을 부당하게 배제하므로, 봉인 전에 저자 내용·격자 배치 보존과 함수명 고정을 구분했다. IM-A1의 CLI 지식은 후보 C3 전체 Open3 사용 지식과 구별했다. | U층의 무언급은 경험 없음이라는 음성 증거가 아니다. 실제 시도한 정확한 입력·호출·판이 공개되면 제품 동일성과 조작 동일성을 따로 재평가한다. 후속 자기 답이나 실행 보고를 최초 이력으로 소급하지 않는다. |
| Q3. 실제로 돌아온 후보는 무엇인가 | 생성시각부터 30일 안의 질문자 외 답·댓글에서 시간→숫자 ID→본문 위치로 최초 3조작을 고정했다. 24자리 중 실제 18·빈자리 6이며 외부 검색으로 결원을 채우지 않았다. 원래 받은 링크/절, 링크 없는 명령, 나중에 찾은 공식 절을 구별했다. TY-U2의 동시 자기 답은 외부 제안이 아니므로 세 자리 모두 빈자리다. | [candidates 24행](candidates.csv)의 `first_proposal_utc`, `origin_evidence`, `related_or_merged_origins`; [IM 제안 획득](evidence/imagemagick/stage2-acquisition.json), [TY 제안 획득](evidence/typst/proposals-acquisition.json). [TY-A1 최초 CSS 댓글](https://stackoverflow.com/questions/77790135#comment137137082_77790135), [TY-A1 답 revision 1](https://stackoverflow.com/revisions/8CB224AD-BB4B-4DA3-81B0-216EC6E4F442/view-source), [IM-U2 최초 댓글](https://stackoverflow.com/questions/77776955#comment137122439_77776955)과 [다음 댓글](https://stackoverflow.com/questions/77776955#comment137133948_77776955)의 본문 위치·시간·해시를 원장에 연결했다. | TY-A1의 CSS를 목적 부적합이라는 이유로 뒤늦게 빼면 사전 고정된 시간순 후보풀이 바뀐다. 따라서 C1로 보존하고 유효성에서 반박한다. IM-U2의 generic perspective와 `+distort`/출력 크기 제안은 독립 인수 제안으로 나눴으나 하나의 구체화로 합칠 여지도 있다. 병합하면 실제 17·빈자리 7, A 반환 6·B 반환 13이다. | 댓글의 과거 수정 이력과 삭제 댓글은 미확인이다. `has_more=false`는 현재 공개 API 페이지의 순회 완료이지 당시 모든 대화의 완전성은 아니다. 더 이른 공개 revision/조작이나 동일 조작의 인용 반복이 확인되면 순서·병합 민감도를 별도 재계산한다. |
| Q4. 제품 필터와 조작 필터가 무엇을 숨기는가 | A는 실제 시도 제품과 같은 9개를 제외하고 7개를 반환했다. B는 입력 상태·효과 인자·단계까지 동일한 실제 시도임이 입증되는 후보가 없어 0개를 제외하고 14개를 반환했다. B만 반환 7·A만 반환 0이다. 생존과 앞 두 자리 반환을 구별했다. 제품 사용 미확인은 제품이 다르다는 증거가 아니다. | [봉인 후보](candidates.csv)의 `product_identity_proof`, `operation_identity_proof`, A/B 결정·반환 위치·이동 순위; [후속 열람 전 봉인](evidence/seals/candidates.json), [실제 CSV 교차 검토](evidence/independent-review.md) 개수·반환 재계산. [TY-A2 outer binding 제안](https://stackoverflow.com/revisions/AA8F9AD2-55CE-4AC1-A5AC-928BFADEC850/view-source)과 [인자 `#red` 댓글](https://stackoverflow.com/questions/77861495#comment137401034_77894083)은 기존 helper와 호출 상태/인수가 다르다. | B가 이미 아는 핵심을 살릴 가능성을 IM-A1-C3의 기존 grouped CLI와 TY-U1의 직접 page/새 helper에서 찾았다. 완전한 후보의 과거 사용은 입증되지 않았다. ImageMagick engine을 동일 제품으로 보는 A에는 QuickMagick·RMagick·Open3의 wrapper 차이가 감춰진다. B 제외 0건인 자료로 B의 중복 억제력이 좋다고 주장할 수 없다. | 비교 자격을 가진 완전 중복 후보가 없어 재추천 제거율은 산출 불가다. 원 입력·상태·인수·단계가 모두 같은 사전 실행 기록 한 건이 나오면 해당 후보의 B 제외와 중복 분모를 재계산한다. wrapper를 제품 경계로 삼는 대안은 현재 engine 기준 결과와 구분해야 한다. |
| Q5. 남기거나 숨긴 조작이 목적을 충족하는가 | 고정 공식 자료와 연구 실행은 같은 도구의 다른 조작 TY-A1-C2·TY-A2-C1/C2 세 후보를 지지했다. A는 3/3을 숨기고 B는 0/3을 숨겼다. 두 요청에 속한 세 후보이며 역사적 사용자 성공 세 건이 아니다. TY-A2-C2를 원문 문자 그대로만 인정하면 분모 2, A 2/2·B 0/2다. | Typst v0.10.0 [container.rs](https://github.com/typst/typst/blob/70ca0d257bb4ba927f63260e20443f244e0bb58c/crates/typst/src/layout/container.rs) L32–177, [math.rs](https://github.com/typst/typst/blob/70ca0d257bb4ba927f63260e20443f244e0bb58c/crates/typst/src/eval/math.rs) L24–31, [scope.rs](https://github.com/typst/typst/blob/70ca0d257bb4ba927f63260e20443f244e0bb58c/crates/typst/src/foundations/scope.rs) L47–101; [고정판 실행 영수증](evidence/typst-official/run-receipt.json)·[출력 대조](evidence/typst-official/metrics.json). ImageMagick 7.0.10-61 [옵션 문서](https://github.com/ImageMagick/ImageMagick/blob/eeb41d70c9baf418a3aa75c424fb305362a1b280/www/command-line-options.html) threshold L6870–6907, size L6498–6508, perspective L2231–2243·L2479–2496; [IM 평가](evidence/imagemagick/stage3/assessment-part.json)·[반대 실행](evidence/root-supplement/probe-receipt.json). | B의 추가 반환 7개 중 나머지 IM 4개에는 API/판·수치·셸 인용·문법·크기 보존 문제가 있어 모두 유효 대안으로 세지 않았다. TY-U1-C1의 문자 그대로 `#pagebreak`는 함수명을 출력하고 1페이지, 수정형 호출은 3페이지다. TY-A2-C2의 원 댓글 `s_2`와 원 수식 `s_2^-` 적용형을 별도 실행했다. outer `red=blue` 상태에서는 같은 helper 호출이 파란색이 되어 입력 상태 차이의 반례도 확인했다. | 원 사용자판+원 입력의 전체 재현 확인은 0, 실제 후보 18개 모두 그 검증층에서는 미확인이다. 연구판 증거를 무효로 만드는 것은 아니지만 역사적 성공으로 승격할 수 없다. 원 파일·판·변경 불가 조건에서 지지 후보가 필수 출력을 깨면 해당 손실 분모를 줄인다. 원문 수정형 성공으로 봉인 후보를 교체하지 않는다. |
| Q6. 질문자가 이미 알았거나 새로 알았고 실제 바꿨는가 | 90일 창의 OP 기록을 후보 봉인 뒤 읽었다. 실제 후보 18개 중 완전한 제안 조작의 사전 인지 독립 근거와 명시 신규 인지 증언은 모두 미확인이다. 명시 신규 인지 관측은 0건이지만 인지율 0%가 아니다. IM-A1-C1 수정형과 연결된 실행 보고 1에피소드는 실패였으며 정확한 원 제안 실행·입력판출력 연계는 확인되지 않았다. | [followup 8행](followup.csv), [IM 후속 원장](evidence/imagemagick/stage3/followup-part.json), [TY 후속 원장](evidence/typst/stage3/followup-part.json). IM-A1 [revision 2](https://stackoverflow.com/revisions/77774582/2) 2024-01-07 20:52:40Z와 [댓글](https://stackoverflow.com/questions/77774582#comment137114172_77774667) 20:53:23Z는 같은 수정형 실행이다. [TY-U1 반응](https://stackoverflow.com/questions/77876109#comment137297957_77878373) 01-25 13:28:09Z, [TY-A2 반응](https://stackoverflow.com/questions/77861495#comment137334800_77894083) 01-29 14:39:47Z, [TY-U2 동시 자기 답](https://stackoverflow.com/revisions/5337E644-F174-44B9-8BC0-A747D9660F16/view-source)의 시점·위치를 대조했다. | 감사·Interesting·현재 채택을 학습/성공으로 읽는 해석을 검토했으나 명시 기준을 충족하지 않는다. TY-U1의 수동임을 확인한 말은 거절이나 자동 floating 필수조건의 증거가 아니다. TY-U2 첫 자기 답은 prose의 import와 code의 include가 충돌하며, 125일 뒤 다른 편집자가 수정했다. 현재 답만 읽으면 역사적 성공을 오인한다. IM-A1의 revision과 댓글을 두 실행으로 세지 않았다. | 공개 회고가 없고 댓글 수정·삭제 이력과 외부 실행은 보이지 않는다. 원 제안 이전에 정확한 조작을 알고 있었다는 명시 기록, 처음 알았다는 직접 증언, 판·입력·출력을 연결한 실행 중 하나가 필요하다. 최초/현재 질문 본문 변화 3/8, 실제 시도 이력 변화 1/8, 목표 세부 변화 1/8이지만 확정 A/B 반환 변경은 각각 0/8이며 최초판 봉인은 보존한다. |
| Q7. 어떤 한 줄을 보여줄 것인가 | 제품명보다 바뀌는 대상·입력 상태·인수·처리 단계를 한 줄에 적는다. 같은 이름의 다른 효과와 다른 표기의 같은 효과를 모두 확인했다. 사건별 즉답/같은 도구의 다른 절/조건부 두 링크/한 질문은 유효성·기지 여부의 불확실성을 따라 선택하며, 타 분야 4자료와 합성 대조를 주 표본의 인지 분모에 더하지 않는다. | Git v2.45.2 [restore 매뉴얼](https://github.com/git/git/blob/bea9ecd24b0c3bf06cab4a851694fe09e7e51408/Documentation/git-restore.txt) L21–26·58–64·194–213, [t2070](https://github.com/git/git/blob/bea9ecd24b0c3bf06cab4a851694fe09e7e51408/t/t2070-restore.sh) L37–85. FFmpeg n7.0.1 [매뉴얼](https://github.com/FFmpeg/FFmpeg/blob/af25a4bfd2503caf3ee485b27b99b620302f5718/doc/ffmpeg.texi) L274–327·499–517·1742–1782, [FATE](https://github.com/FFmpeg/FFmpeg/blob/af25a4bfd2503caf3ee485b27b99b620302f5718/tests/fate/ffmpeg.mak) L137–143·168–170·188–192. [실제 명령·출력](evidence/cross-domain/commands.jsonl), [영수증](evidence/cross-domain/receipt.json), [8사건 근거](evidence/followup-cases.json). | restore의 worktree/index를 바꾸면 대상과 기본 원천이 바뀌지만 `-s@ -SW`는 긴 표기의 별칭이다. FFmpeg `-c copy`만으로 두 번째 음성이 보존되지 않았고 `-map 0`을 더하면 보존됐으며 `-codec copy` 별칭의 packet 결과는 같았다. 입력이 이미 같거나 음성이 하나라면 차이가 사라지는 반대 조건도 남겼다. 새 helper 이름이 기존 page 동작에 자동 float 기능을 더한다고 가정하지 않았다. | Git 2.56.1·FFmpeg 7.1.5의 합성 실행이며 고정판 상류 전체 스위트는 미실시다. [재생 입력·명령](evidence/cross-domain/RESULT.md)의 원 판 시험이 의미 차이를 반박하면 보조 원리를 제한한다. 8사건별 최소 반대 관측은 최종 반환표에서 원 필수조건·실제 시도·작성자 결과와 연결해 다시 대조해야 한다. |

## 자리·분모 검산

이 문서를 작성하면서 `csv.DictReader`로 현재 작업 파일의 행 수와 필드를 다시 읽었다. 실제 필터·반환 재계산은 [분담 교차 검토](evidence/independent-review.md), 후속과 유효성 분모의 대조는 [분모 검토](evidence/denominator-review.md)에 있다. 아래 수치는 빈자리를 제외한 후보 단위와 요청 단위를 섞지 않는다.

| 확인 항목 | 값 | 근거와 해석 범위 |
| --- | ---: | --- |
| 모집틀 | 87행 | ImageMagick 60 + Typst 27. IM API `has_more=true`는 첫 60건 제한 밖에 질문이 더 있다는 뜻이다. TY `has_more=false`. |
| 최초 요청 / 후보 자리 / 후속 요청 | 8 / 24 / 8 | `initial.csv`, `candidates.csv`, `followup.csv`. 최종 RESULT의 세 표가 이 자리 수를 그대로 담는지는 최종 생성 뒤 확인할 항목이다. |
| 실제 후보 / 빈자리 | 18 / 6 | 빈자리: IM-A2-C3, IM-U2-C3, TY-A2-C3, TY-U2-C1/C2/C3. 빈자리는 인지 미확인 18개의 분모에 다시 더하지 않는다. |
| A 제외 / 생존 / 반환 / 생존하나 2위 밖 | 9 / 9 / 7 / 2 | 제외와 반환되지 않음을 구분한다. |
| B 제외 / 생존 / 반환 / 생존하나 2위 밖 | 0 / 18 / 14 / 4 | 동일성 미확인으로 남긴 후보가 많다. B의 중복 억제 성공을 실측한 표본이 아니다. |
| B만 반환 / A만 반환 | 7 / 0 | IM-A1-C1/C2, IM-A2-C1/C2, TY-A1-C2, TY-A2-C1/C2. 이 중 연구판 유효성으로 지지한 다른 조작은 아래 3개다. |
| 연구판에서 지지된 다른 유효 조작 손실 | A 3/3, B 0/3 | TY-A1-C2, TY-A2-C1/C2. 2요청·3후보의 조건부 조작 평가다. 나머지 15개를 모두 실패로 코딩하지 않는다. |
| 원문 문자 그대로만 인정하는 손실 민감도 | A 2/2, B 0/2 | TY-A2-C2의 축약 예시와 원 수식 적용형을 구별해 C2를 분모에서 뺀 경우. |
| 역사적 원 사용자판·원 입력 전체 재현 | 확인 0 / 미확인 18 | 연구판 결과와 독립된 강화 검증층이다. 분모 0의 성공/실패 비율은 산출 불가다. |
| 완전한 후보의 사전 인지 비교 분모 | 0 / 미확인 18 | 재추천 제거와 이미 아는 방법 반환의 비율 모두 산출 불가. 기존 helper나 CLI 핵심의 부분 인지는 별도 양성 증거로 보존했다. |
| 명시 신규 인지 | 관측 0 / 신규 여부 미확인 18 | 18개 음성 정답 또는 0% 신규 인지율로 쓰지 않는다. |
| 수정형 실행 보고 / exact 원문 실행 확인 | 1에피소드 / 0 | 수정된 IM-A1-C1의 실패. exact 원문 실행 여부는 실제 후보 18개 모두 미확인이다. |
| 최초/현재 질문 본문 변화 / 실제 시도 이력 변화 | 3/8 / 1/8 | [대조 원장](evidence/original-current-comparison.json). 목표 세부 변화 1/8. 확정 A/B 반환 변경은 각각 0/8이며, 내용 변화 자체가 없었다는 뜻이 아니다. |
| IM-U2 두 제안을 합치는 민감도 | 실제 17 / 빈자리 7 / A 반환 6 / B 반환 13 | 한 요청의 단계적 구체화로 합칠 때. 봉인된 18/6/7/14 원표는 보존하고, 분리된 두 후보가 독립 유효 대안 둘이라고 단정하지 않는다. |

## 고유 자료 하한과 실패 응답

[자료 집계](evidence/source-counts.json)의 원장 191행 중 고유 산입은 **35개**, 필수 범주만 세면 **29개**다. 같은 프로젝트에서 나온 파일들은 같은 저작 계보를 갖는다. 35개의 독립 사건·실험이라는 뜻이 아니다.

| 자료 범주 | 고유 수 | 하한 대조 |
| --- | ---: | --- |
| 선정된 공개 요청 사건 | 8 | 요구 8. 같은 사건의 댓글·답·revision은 별도 사건 수로 늘리지 않음. |
| ImageMagick 고정 공식 문서·구현 | 5 | 각 도구 3개 이상 충족. |
| Typst 고정 공식 문서·구현 | 7 | 각 도구 3개 이상, 두 도구 합계 12로 요구 8 충족. |
| ImageMagick 상류 시험 | 2 | 아래 Typst 묶음과 합계 5로 요구 4 충족. |
| Typst 상류 입력·예상 출력 묶음 | 3 | 대응 ref PNG는 각 묶음에 포함하며 자료를 추가 산입하지 않음. |
| Git 공식 매뉴얼·회귀 시험 | 2 | 요구 2 충족. |
| FFmpeg 공식 문서·FATE | 2 | 요구 2 충족. |
| 보조 1차 자료 | 6 | QuickMagick, RMagick 변경 기록·binding, Ruby Open3·Shellwords, CSS. 필수 29개 충족과 별도. |

서로 다른 앵커, 같은 파일의 현재판·고정판, 미러, 댓글, 재인용, 모집 탈락 건은 고유 하한을 늘리는 데 쓰지 않았다. 선정되지 않은 직접 열람 기록도 원장에는 남겼다. 실패 응답은 [TY 최초 이미지 영수증](evidence/typst/initial-images.json), [IM 최초 revision HTML 실패](evidence/imagemagick/revision-html-failures.json), [IM 이미지 획득](evidence/imagemagick/stage3/image-acquisition.json), [보조 자료 실패](evidence/root-supplement/failures.jsonl)로 보존했다. 403/503 등으로 못 읽은 파일은 읽었다고 세지 않았으며, 원 이미지 미확보를 합성 입력 성공으로 대체하지 않았다.

## 봉인·노출·검토 독립성

최초 이력은 첫 원격 봉인, A/B 판단은 두 번째 원격 봉인 후에만 작성자 후속을 열었다. API가 기계에 반환한 이후 revision·현재 채택·OP 기록과 모델에 표시한 projection은 [IM 최초 노출](evidence/imagemagick/exposure.json), [TY 최초 노출](evidence/typst/exposure.json), [IM 제안 노출](evidence/imagemagick/proposals-exposure.json), [TY 제안 노출](evidence/typst/proposals-exposure.json), [root 제안 노출](evidence/seals/root-proposals-exposure.json)에 분리했다.

완전 맹검은 주장하지 않는다. 다른 답변자의 댓글이 OP의 요구나 “덜 수동인 업데이트”를 간접 언급한 노출은 남겼다. Git/FFmpeg 보조 자료는 후보 봉인 전 병렬로 읽었으며 후보 봉인의 `official_behavior_read=false`는 주 ImageMagick/Typst 후보의 공식 동작 평가를 가리킨다. root의 보조 실행은 후속 요약을 읽은 뒤 수행했다. 반면 Typst 공식 평가자는 OP 후속 없이 평가를 고정한 뒤 분모 검토에서 처음 후속을 읽었다. 정확한 범위는 [동작·후속 노출 기록](evidence/seals/behavior-exposure.json)에 있다.

CSV 봉인의 로컬 SHA-256과 GitHub 저장 바이트의 SHA-256이 다른 것은 CRLF→LF 정규화 때문이다. [전송 정규화 대조](evidence/seals/transport-normalization.json)는 원 로컬 해시, 원격 LF 해시, git blob, `crlf_to_lf_only=true`를 5파일별로 기록한다. parsed 내용·순서 변화는 0이다. 재현자는 GitHub 바이트에 `committed_sha256`을 사용해야 한다. 원 봉인 해시를 사후 교체해 같은 바이트였다고 가장하지 않았다.

이 문서는 작업의 자기검토다. 별도의 실제 검토로 [선정 경계 대조](evidence/initial-boundary-review.md), [CSV·반환 교차 검토](evidence/independent-review.md), [후속·분모 비판 검토](evidence/denominator-review.md)가 있다. CSV 검토자는 Typst 모집·후보·후속 작성자이므로 Typst 부분은 자기검토이고 ImageMagick·통합 CSV는 다른 작성자의 결과와 대조한 것이다. 분모 검토자는 Typst 공식 실행·교차 분야 작성자이므로 자신의 실행을 독립 재현한 검토가 아니다. 사람의 검토나 작업 전체에 대한 완전히 독립적인 맹검 검토는 수행하지 않았다.

## 완료 전 남은 운영 확인

현재 확보한 자료는 지정 공개 범위의 관측과 연구판 동작 비교를 마칠 수 있는 근거다. **최종 운영 절차 완료는 아직 주장하지 않는다.** root가 결과 묶음을 커밋한 정확한 SHA에서 다음을 실행하고 영수증을 읽어야 한다.

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-101/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

이 문서 작성 시점에는 두 최종 검사 모두 미실시다. 실행 후 명령·UTC·종료값·범위·공통 검사에서 실제 자동 확인한 세션 수를 기록하고, 실패와 미실시를 구분해야 한다. 최종 RESULT의 요청 8자리·후보 24자리·후속/반환 8자리, 분자·분모·미확인, 대표 원자료·출력·재현 절차를 정확한 결과 SHA의 GitHub URL에서 다시 연 뒤에만 HANDOFF를 마지막 단독 커밋으로 쓴다. 이후 HANDOFF 커밋을 앞서 검사한 결과 SHA에 포함됐다고 하지 않는다.

필수 자료·30일/90일 공개 페이지 순회·핵심 조작 비교·결과 재검증 중 실제 미완료가 남으면 정확한 결손과 재개 첫 행동을 적어 PARTIAL로 인계한다. 양성 신규 인지 증언을 찾지 못한 결과와 후속 조사 자체를 수행하지 못한 상태를 같은 결손으로 다루지 않는다. 공개 자료에서 확인할 수 없는 원 환경·인지·실행은 완료 상태와 관계없이 미확인으로 유지한다.
