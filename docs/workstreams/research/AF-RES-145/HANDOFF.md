# AF-RES-145 HANDOFF — PARTIAL

- 작업자 수용 상태: **PARTIAL** (원전 하한 충족, 독립 비교 필수 조건 미충족). 실제 작업자 현 단일 GPT-6.2 응답 문맥 R0, GitHub connector/공개 web. 독립 새 독자/검색 문맥을 실행할 수단 미확인. 가상의 독자·판독·원저자 채택·시험 결과를 생성하지 않았다.
- 실제 시작 SHA: 97a1e63cb48ff4900984104e1d2a3760f324eb79 (계획 기준 9ad2ffc5974bf3379ce1f3fb947a9cf19bbdf673보다 통합판 3 ahead, 0 behind, dot-control 한 경로). 유일 등록 선행 AF-RES-141 중앙 DONE이나 고정 인계 PARTIAL. 선행 [HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/db0e26aac95f34e77ad3c8bf898879f15558ae5c/docs/workstreams/research/AF-RES-141/HANDOFF.md) 및 [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/764e89364f0491d6f27f12347b5bf1b2b4af98e4/docs/workstreams/research/AF-RES-141/RESULT.md) 읽음. 다른 배정 대기 없음. 통합표 수정 없음.
- 브랜치: `work/research-af-res-145`. 허용 경로 `docs/workstreams/research/AF-RES-145/`만. 원격에서 결과판 `2f41c8650ff45e531ce501118cc8b28296c74db9`에 고정되어 있음. 이 HANDOFF는 별도의 마지막 단독 커밋; 자기 자신의 커밋 SHA를 본문에 재기록하는 것은 자기참조로 불가. 최종 branch ref를 작성 직후 다시 읽어 실제 HANDOFF SHA와 변경 경로를 외부 응답에 보고한다.
- 작업자의 결론: 가까운 부품 링크만으로 이미 정한 선택을 확인할 때도 있고, 원전의 실패 조건을 통해 시험을 구체화할 때도 있다. R0 자기 초안→수정본에서 이 차이를 관찰했으나 B가 A보다 새로운 선택을 더 만든다는 증거는 없다. 기록관리/제조 원전은 발견 봉인 후 대조이며 자발 발견 아님. 다음 설계자의 선택을 확정할 효과율/절감율 산출 불가.

## 커밋 및 원격 재열람
| 묶음 | 실제 원격 SHA | 대표 재열람 파일 / blob |
|---|---|---|
| ① 범위 및 판정 봉인 | 959c2509fa9f86336666e56ae902586bbaf333fe | SCOPE.md fe51847c53f6c7d3131e1fa27b7c00b597530276 |
| ② 모집·기준 입력 | f3a087f4b99b76643b3102cfa51cbcfb26d17f2e | frame.csv bc47abf3591b303dcc97275f7afa2ffc70b80364; packets.jsonl f1c3055917c9a36defb06b2b98bb5d6d28c68e8c |
| ②b 실제 R0 사전 초안 봉인 | 43b1cd97b86d473395e8d0f2ea987ad4691abdbf | drafts.jsonl 4090ed8509b5650f5311b5142839a5343fa321f5 |
| ③ 주 관측 봉인 | 227a522a2e6339345681fabc9e493827b1ee3916 | discovery.jsonl 1090040bee8eed8333bf0dbff8586b455e592189; readings.jsonl 6427dcc4966cd6619edce393e51c388174fc753e; sources.jsonl ba353951581999c689ca7989ab50b0712cd85530 |
| ④ 대조·반증·비용 | caac3893405e1d3b655b495b7fdb61d1a6568e2e | sources.jsonl cb9576dcb750b9adcd1659e9a716ba6ebfa6d217; comparison.md 3b406d2b12375d8ffd167a68c963f17b938bd03a; adjudication.csv 624aae885fb5a23d588c7634e3e4ff5b4ae05a31; costs.json 812f5eab1268e7f4fad48a7da4e2e28cd93f53b1 |
| ⑤ 필수 표 및 검산 | 2f41c8650ff45e531ce501118cc8b28296c74db9 | RESULT.md 69335bf738f3a2cfb7bc897099785d408b85822b; SELF_CHECK.md f7f97ffa98b23b125b182f265aae59610c3daecc; REPLAY.md e53dd4e1737df6f6d0f68bfb59f04fda0abc66b7; verify_ledgers.py 5e649ec398fff81d44b874bb07389e867409360e |

⑤ SHA와 실제 시작 SHA를 GitHub compare에서 다시 대조: 6 ahead, 0 behind, 14 변경 파일 전부 owned_path 내부; dot-control 포함 타 경로 변경 0. ⑤ 원격 파일 첫/마지막 행을 재열람하여 RESULT 필수 3표 시작과 마지막 약점표, SELF_CHECK의 검사 결과 확인. 모든 링크는 소스 원장에 있음. [RESULT.md](RESULT.md) · [SELF_CHECK.md](SELF_CHECK.md) · [REPLAY.md](REPLAY.md) · [sources.jsonl](sources.jsonl).

## 완료/결측·비교 분모
| 항목 | 실제 | 목표/제한 |
|---|---|---|
| 모집 | 최초 40씩=80; 각 repo W2 P2, 8건. 선정 8개 REST 직접 재열람, 현재 first body 일치 | 전체 4/부분 4 충족. 현재 편집판·최초판/첨부 일부 미확인, 모호 분류 있음 |
| 외부 1차 저작 | 25 distinct work_id=원요청8 + 공급자9 + 경계4 + 비SW4(기록관리 2, 제조/품질 2); 전체 ledger38행 | 24 하한 충족. 3 접근 실패, 10 보충·중복 등 제외. 날짜/판·절은 원장; 일부 후기 자료 |
| 사전/수정 | 실제 R0 자기 사전8 / 자기 수정8, 지문 8/8 일치 | 독립 2명×8=16쌍 목표 중 독립0; 가림 배포0, 판독0 |
| 검색 | 8 사건당 한 조건 표지 A4/B4, 22 질의(18 고유문자열), 직접 URL 22 시도/21 성공/1 실패. 사건별 상한 이내 | 동일 사건 두 조건 독립 검색 목표16 중 유효0; F-P2 ezdxf, J-W1 SAF 사전 이름/지식 주입; 배치 표시 순위·시각 한계 |
| 사후 대조 | 6질의/8시도/6성공(재열람 1 포함); 4 비SW 원전 최소량 산입 | 발견 봉인 후; 자발 발견에서 전부 제외; 사후 대조를 독자에게 실제 제공하지 않음 |
| 비교 결과 | A만0/B만0/양쪽0/없음0/비교불가8. 전체/부분 및 각 저장소 각각 4 비교불가, 유효분모0 | 분모0이므로 비율 산출 불가, 양 조건의 동률이나 효과 없음 뜻 아님 |
| 실행/채택/비용 | 대상 시험 실행0; 원저자 채택 미관찰. R0 주 단계 경과209.244s, 대조 단계105.899s | AI compute/토큰·가격, 사람·편집자·후속 조사자·원저자 재작업시간, A/B 비용 차이 미확인 |

## 실패 경로·검사
- 통합 dot-control contents API 빈 본문, raw fetch 실패 → blob ca510baf19a8b34ef45c92f4ad33206e551e3dbf로 145 항목 및 141 결과 SHA 복구. 통합 파일 수정 금지 준수.
- S11 SolidWorks 일반 help shell(본문 접근 실패), C06/C07 403. 검색 결과 목록만으로 산입하지 않음. C02 PDF 페이지 2–3 읽어 대체. S08 혼합 표시 순서 13번째 vs 초기 원장 11의 차이는 ④ correction에서 밝혔고 기관별 정확 순위는 미확인. S04 후기 논의가 R0에 노출된 오염 기록, 사전 초안 전에 원저자 후속 의사결정을 따로 복원하지 않음.
- 실제 JS 검산: ④ 고정판 CSV/JSONL을 직접 다시 읽어 선정의 최초 두 W/P, id join, 지문, source id/work id, 상한, 결측 분모, C01–04 봉인 순서 등을 확인했다. [SELF_CHECK.md](SELF_CHECK.md) 수치 및 Q1–7 근거. 이를 독립 판독·타깃 실행 검증으로 간주하지 않는다.
- 로컬 shell 실제 시도: `timeout 10 git ls-remote --heads https://github.com/laadkke-arch/agentflow-open.git work/research-af-res-145` → exit 128, `Could not resolve host: github.com`. 저장소 checkout 불가. 아래 명령을 네트워크/권한 있는 환경에서 실행. verify_ledgers.py는 저장했으나 Python 실행은 미실시; 원격 JS 자체 검산만 완료. 실제 대상 시험 fixture는 REPLAY에 별도.

## 다음 첫 행동 (정확한 재개 입력)
조정자는 현재 branch HEAD를 fetch하여 모든 변경이 owned_path에 있는지 확인하고 검산한다. 기존 파일 덮어쓰기 대신 correction/새 관측 묶음을 별도 커밋. 독립 독자에게 보이는 것은 결과 파일이 아니라 **② 고정 문제지의 8행만**이다.
```sh
git clone https://github.com/laadkke-arch/agentflow-open.git
cd agentflow-open
git fetch origin work/research-af-res-145
git checkout --detach origin/work/research-af-res-145
git diff --name-only 97a1e63cb48ff4900984104e1d2a3760f324eb79 HEAD
python3 docs/workstreams/research/AF-RES-145/verify_ledgers.py
git show f3a087f4b99b76643b3102cfa51cbcfb26d17f2e:docs/workstreams/research/AF-RES-145/packets.jsonl > /tmp/af-res-145-baseline.jsonl
```
- 입력 `/tmp/af-res-145-baseline.jsonl`의 baseline_input 8행만 R1/R2 각각에게 전달. 먼저 R1/R2 16 독립 초안(UTC+지문+이미 아는 대안/시험)을 봉인. 현 R0 초안이나 후보 원전, RESULT, REPLAY의 시험 정답은 독자에게 사전 공개 금지. 독립 검색자에게도 원요청만 제공; 같은 모델/상한 4질의·6원전·3링크, 검색 각 15분·독서 각 10분 및 공석 동일. [SCOPE.md](SCOPE.md) 가림/교차 계약, [REPLAY.md](REPLAY.md) 배정과 fixture는 조정자용. 단계별 새 파일 원장 및 실제 시각 기록.
- 독립 검색 16문맥과 가림 독자 16수정쌍, 새 가림 판독이 실재하면 원전 성립·보존 조건·사전 부재·수정 여부를 다시 판정한다. 실행은 해당 제품 버전/테스트 harness 확인 후 REPLAY fixture의 원요청 입력·성공/실패 조건을 적용. F-P1 첫 입력 `spreadsheet.setBackground('A1', spreadsheet.getBackground('A1'))` / J-P1 W3C F110 Tab/Shift+Tab / J-W2 Compose networking 및 Moby #45610 재현 입력. 실제 개발·실행 권한과 환경을 확보하지 않은 상태에서 명령 성공 주장 금지.
- 분모가 부족하면 동일 PARTIAL로 유지. 통합판 조정자의 판단 이전에 dot-control 상태 변경하지 말 것.

| 불일치·약점 | 판단에 미치는 영향 | 다음 조사와 자료 | 판정을 바꿀 관측 |
|---|---|---|---|
| 독립 독자/검색 문맥/가림 판독 부재, B 사전 이름 주입, 모집 및 S04 노출 | R0 자기 수정 8만 실제, A/B 효과 및 처음 인지의 유효분모0 | ② 고정 문제지에서 별개 R1/R2 초안, 16 독립 검색·가림 배포 및 판독 (REPLAY) | 동일 사건 양 조건에서 독립 사전 부재·원전 성립·보존·수정이 검증된 유효 짝 |
| 현재 편집판/후기 공급자 문서, W/P 경계, per-query 순위/시각 불명 | 원저자의 당시 가용성, 최초 적격 표본 및 검색 재현성 확정 불가 | 공개 edit history·고정판/아카이브, #11892/#11911/#9641 별도 재코딩 | 최초판/독립 분류에서 적격 선발이나 조건/당시 원전 가용성이 바뀜 |
| 제안 시험≠실행, 원저자 채택/사람 시간 미관찰, Git DNS 실패 | 기술 보존 및 노동 절감 주장 불가, J-W2 확인/J-P1 구체화 과대 해석 위험 | verify_ledgers.py 로컬 실행 및 REPLAY fixture 실제 측정, 역할별 시간, 원저자 후속 별도 | 실행된 판별 시험/실제 수정·채택 및 분리된 시간 원장이 확인됨 |
