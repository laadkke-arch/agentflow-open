# 독립 비교 재개 입력 / 실행 계획 (미실시)
## 첫 행동: 오염 없는 새 독자부터
1. 고정 모집판 f3a087f4b99b76643b3102cfa51cbcfb26d17f2e의 `packets.jsonl` 앞 8 baseline_input행만 받는다. 새 독자는 이 문서, RESULT, discovery, drafts, sources(S/C), readings, comparison, adjudication, 후속 issue 댓글을 먼저 열지 말 것. 담당 조정자만 아래 표를 읽는다. 공개 최초본 복원 또는 재분류는 별도 correction 묶음으로 기록하고 기존 봉인 삭제 금지.
2. 두 실제 별개 독자 R1/R2에 원래 문제지만 제공. 각 독자×8의 초안 UTC 및 내용 지문, 선택 범위·목표·보존값·현재 안·이미 아는 대안/시험을 각각 봉인. 사전 인지 없음이라는 답도 실제 기록. 세션 분리가 불가하면 실재 수만 남기고 PARTIAL.
3. 사건×A/B를 독립 검색 문맥 16개에서 수행. 동일 모델과 동일 예산(4질의, 직접 원문 6, 최대 3 링크); A 자유, B 입력·동작·보존값 관계 표현 추가, 특정 분야나 공급자 이름을 심지 말 것. 같은 서비스 결과 달라질 수 있으므로 질의별 UTC/원시 결과순서/실제 직접 URL open/거절/출처판/가격·토큰·시작끝 기록; 검색 결과 봉인 후에만 비SW 별도 비교. 기존 R0 자료는 정답 또는 seed로 제공하지 않음.
4. 조정자가 가림 ID로 URL·절·근거 한 문장·남은 조건 형식을 통일하고 출처 경로/조건/model 표시 제거. 다음 배정은 현재 8개 사건을 그대로 쓸 경우의 재개용 계획이지 실제 배포 아님. 각 독자는 같은 사건 두 꾸러미를 보지 않음. 공석도 동일 시간. 새 독자가 실제로 열린 URL 및 변경 전후 줄, 제안 시험, 채택/기각/보류/표현/무변경을 기록. 
| 사건 | 층 | R1 | R2 |
|---|---|---|---|
| F-P1 | 부분 | A | B |
| F-P2 | 부분 | B | A |
| F-W1 | 전체 | A | B |
| F-W2 | 전체 | B | A |
| J-P1 | 부분 | B | A |
| J-P2 | 부분 | A | B |
| J-W1 | 전체 | B | A |
| J-W2 | 전체 | A | B |

5. 새 가림 판독자는 baseline에 없었는지, 원전 동작 성립, 보존값 모순 없음, 실제 수정/판별시험을 각각 yes/no/unknown. 중복 원리·후기 출처·사전 인지·표현변경 제외 재집계. 실제 시험 실행과 계획 별도. 원저자 공개 후속 결정은 별도 시간/actor; 독자 채택으로 바꾸지 않는다.
6. 비용 역할별 계측: 검색자, 독자/설계자, 후속 조사자, 편집자 각각 실제 시작끝/읽은 양/실패/토큰·가격·human minute, 분모 구분. 사람 참여 없으면 null. 결과에 사건당 A만/B만/양쪽/없음/비교불가 및 층별 분모 기록. 

## 최소 대상 판별 시험 — 구현 전에는 시험 계획일 뿐
| 사건 | 고정 입력/fixture | 관찰/실패 기준 |
|---|---|---|
| F-P1 | 새 spreadsheet cell A1 기본값, A2 explicit RGB; A1 수식/글꼴/테두리 셋, setBackground('A1', getBackground('A1')), 명시 색에서 None reset; invalid string | TypeError 없이 기본값, 비대상 값/수식 그대로, 기존 RGB roundtrip/invalid rejection 유지; 테마 흰색은 별도 오염 후보 |
| F-P2 | DXF BLOCK B1 TEXT+DIMENSION+ATTRIB, INSERT 여러 개 및 MINSERT 2×3, rotated/nonuniform and nested, XCLIP, source handle | 6개 및 occurrence별 식별/좌표, clipped 외부 객체 없음 혹은 명시 미지원, skipped count; 치수 실제 의미 대조; source INSERT 보존 |
| F-W1 | DXF layers X,Y,Z, INSERT X with entities Y/Z/layer0, geometry-only 및 text/dim 혼합; merge on/off | 문서 tree/ownership 정책 명시, source ID stable, 기존 shape-only root 보존; 비선형 치수 훼손 발견 시 기각 |
| F-W2 | f(t)=sin(t), spreadsheet cell alias t, abs/sign/floor 및 singular case, trim domain then edit original expression | reserved variable conflict 처리, 미분 불능 명시 실패/정의된 의미; 제약/단위·trim 후 표현식 유지 |
| J-P1 | viewport 745×1147 및 더 작은 크기, 긴 changelog, 200% zoom, focusable links 및 footer buttons; Tab/Shift+Tab 순환 | 버튼 접근 유지, focus element가 sticky footer로 완전 가려지지 않음; 작은 화면에서 footer 예외 |
| J-P2 | 동일 sync fingerprint, 신규 item/revision 오류, 저위험 background 및 workflow-blocking 오류 | acknowledgement≠해결, blocking일 때 복구 행동, 낮은 위험 불필요 차단 없음, 재등장 규칙 사전 인지로 표시 |
| J-W1 | Android local provider vs cloud, cancel share, uninstall/reinstall, low disk, duplicate filename 및 동시에 동일 target 두 작업, attachments manifest/restore | 실제 로컬 readback, cancel에도 잔존, 삭제 후 접근/복원, 이름 변경 고지, incomplete/parallel 파일을 성공으로 표시하지 않음, lock 정책·원본 보존 |
| J-W2 | compose 앱/DB/proxy 3 service, DB ports 생략, 외부 호스트 및 내부 app 검사; optional localhost host port on 24.0.1 vs 28+ and routing/firewall modes | app DNS+connect 유지, host/LAN 접근 실제 실패(선언만 아님), optional route를 별도 측정; NAT mode 차이를 일반화 금지 |

실제 실행 환경·타깃 빌드/버전·권한 없으므로 위 fixture를 대상 프로젝트의 테스트 harness로 옮길 때 해당 보고 SHA/릴리스 checkout 및 동작 확인부터 한다. 예컨대 F-P1 원요청의 Python console 입력은 `spreadsheet.setBackground('A1', spreadsheet.getBackground('A1'))`; J-P1은 W3C F110의 Tab 절차([S14](https://www.w3.org/WAI/WCAG22/Techniques/failures/F110)); J-W2는 [S19](https://docs.docker.com/compose/how-tos/networking)의 네트워크 검사와 [S22](https://github.com/moby/moby/issues/45610)의 재현 입력을 그대로 읽고 분리된 시험 환경에서만 수행. 현재 대상 변경을 하지 않음. 실제 구현 시험의 명령은 해당 버전의 harness 확인 후 고정해야 하므로 임의 작동 명령/성공을 주장하지 않는다.
