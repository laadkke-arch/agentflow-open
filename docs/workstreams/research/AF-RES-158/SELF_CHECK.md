# AF-RES-158 SELF_CHECK (⑤, remote structural check)
기준 결과 전판: 6bbb70b088c4eb4c1d5d84075ba2570bc44e70a0; RESULT.md 자체 최초 커밋 b0f5438241d131e66d8fe07ef641bee1edda0e1a. 이 세션에서 GitHub connector로 고정 SHA의 파일을 재열람하여 JS로 구조/참조/개수를 검사했다. 별도 실행기, checkout, 제품 재실행, 독립 코더는 없음. 154의 검증 영수증은 154에서 실행된 별도 증빙일 뿐이다.

## 원장 재검산
| 검사 | 실제 결과 |
| --- | --- |
| 최초 4 쿼리 반환 / 고유 / 중복 | 104 / 99 / 5 |
| frame 총행 / 모집 고유 | 113 / 36 |
| P 모집 적격/제외 | 10/2 (첫12) |
| D 모집 적격/QA/제외 | 4/6/14 (24까지 확장); 4 중 curator 집합 1, strict 직접 3 |
| traces/state_checks/answers | 28 / 28 / 15 |
| sources 행/성공/실패/하한 고유 work_id | 113 / 107 / 6 / 66 |
| source_id 중복 / trace·answers·state source_id 미해결 / 적격 trace 누락 | 0 / 0 / 0 |
| frame/traces/answers/state_checks 필드수 오류 | 0 / 0 / 0 / 0 |
| frame/traces/answers/state_checks 빈 문자열 셀 | 0 / 0 / 0 / 0 (미확인 명시값은 결측으로 유지) |
| state_checks case 불일치 | 0 |
| 별도 통지 수신 승인 / 원본 바이트 검증 승인 / 최종 공개 판 검증 승인 | 0 / 0 / 0 |
| RESULT 필수 표 제목·끝 표 | 1→2→3; 마지막 정확히 3행 |
| 실제 base→검사판 diff | ahead13/behind0, owned 8 files, 경로 외 변경 0 |

검사는 CSV 문자열 파서(인용부호·쉼표 처리; multiline 셀 없음)와 JSON.parse로 실시. 해시 문자열은 GitHub blob ID이지 내용의 별도 SHA-256 실측 아님.
frame=27df14fa5071de29352b9c60d8e2fe6832516aea, traces=92d552d62227f4056fb3cc9132350ea6873ea844, answers=ec0c00ff8530280441b980b5a929c593f0f1e9a2, sources=7a6cc3d6e61157e1df9e5099087fb0460b1903e2, raw=1501351bd7be9a4f395e297f18a6ffd3f195291c, states=9a82a2dc2d575789bf35cf07a1bc0b33eac483a6, RESULT=13dd5d23c5cc18734ce1b20b3f92cde1875189d6.

## Q별 양방향 대조
| Q | 주장 → 출처/위치 → 원장 | 역방향 및 한계/판정을 뒤집을 관측 |
| --- | --- | --- |
| 1 | #5215 본문 Description/Steps/Expected [P5215-B](https://github.com/paperless-ngx/paperless-ngx/issues/5215#issue-2063137483), [P5215-C](https://github.com/paperless-ngx/paperless-ngx/issues/5215#issuecomment-1875261885), [P5542](https://github.com/paperless-ngx/paperless-ngx/discussions/5542) L122–133, 154 [RESULT 표1](https://github.com/laadkke-arch/agentflow-open/blob/0b24a986db03d6f1427f38630eeed91aaba1b7a7/docs/workstreams/research/AF-RES-154/RESULT.md), traces P5215 | 동일 저자 archive derivative만 수용, 1/25 재확인; 첫 댓글 시각 미확인, 별도 알림 요청/수신 단정하지 않음; 최초 저자 실제 수신·복구 진술이면 수정 |
| 2 | search_returns 4 query의 created asc, frame의 rank/created/duplicate/eligible, 36 body source_id | 제외·QA 모두 남고 14 적격에 trace 있음; query 총 모집단/누락률 미확인. API total_count, incomplete_results, 날짜 동률 경계 완전 재현 시 수정 |
| 3 | [PAPI113 L236–261](https://github.com/paperless-ngx/paperless-ngx/blob/v1.11.3/docs/api.md#L236-L261) vs [PCODE113 L614–631](https://github.com/paperless-ngx/paperless-ngx/blob/v1.11.3/src/documents/views.py#L614-L631) / P2435-C UUID; [DDIRECT L4–10/63–85](https://guides.dataverse.org/en/5.12.1/developers/s3-direct-upload-api.html#adding-the-uploaded-file-to-the-dataset), DNATIVE511-R L1407–1434; state_checks receipt/terminal | P2471/P2588 대기, P2667 오류 역전, D9425 목록 부재; 당시판 실제 HTTP+ID와 같은 종단 record 확보 시 수정 |
| 4 | [PAPI122 L59–70](https://github.com/paperless-ngx/paperless-ngx/blob/v1.12.2/docs/api.md#L59-L70), [DACCESS L99–121](https://guides.dataverse.org/en/5.12.1/api/dataaccess.html#basic-file-access), [D9469-B](https://github.com/IQSS/dataverse/issues/9469) DOI/file, P11004-B 최초/중복 log doc5 | 원본과 파생·등록·발행 별도; D9469 DOI 500 실패, hash/권한/버전/실제 수신 미확인. exact file ID + original retrieval + digest가 조인될 때 승인 |
| 5 | traces 및 state_checks 28행; [P2573-C](https://github.com/paperless-ngx/paperless-ngx/issues/2573#issuecomment-1412265251), [P11004-B](https://github.com/paperless-ngx/paperless-ngx/issues/11004), [P10579-B](https://github.com/paperless-ngx/paperless-ngx/issues/10579), [P10250-B](https://github.com/paperless-ngx/paperless-ngx/issues/10250), [D9696-C](https://github.com/IQSS/dataverse/issues/9696#issuecomment-1632723622), D10313-B/D10209-B | 같은 실패 파일 재시도 보고는 P2573, 그러나 단일 record/hash 없음. D9696 실제 수동 restart, 추천 대안은 미실행. duplicate ≠ active, media ≠ DB; UI/로그/QA/외부 발송 수신 구분. 재시도 버튼만 실제 관측된 사건 미확인. 동일 제출자 알림 읽음 + 동일 파일 재시도 영수증이면 수정 |
| 6 | answers 5 groups × A/B/C; 각 source_id와 URL; A1/A2 paperless versions, A3–5 DV versions | 1/2/1 절만 비용. C는 소개 일부 길이 대략 비슷하나 정량 길이 매칭/맹검/사용자 실측 없음. A1 실제 code에 UUID; C에서 답 승인 0. 같은 판 사례와 원본 확인 결측을 가리면 결과 기각 |
| 7 | ARC-PROV L118–125, ARC-NARA pp18–19 (이미지 재확인), ARC-JHU L62–89, ARC-HARVARD L36–77 table1, LOG-USPS printed p2 image, LOG-AU L823–834, LOG-FAQ L59–65/86–87 → RESULT Q7 | 기관별 업무/권한 비교만. PROV/NARA 실제 운영이나 개별 SIP receipt 없음; AIHT는 별도 공개 시험. USPS OIG 물리 표본 vs scan; AU 실제 SMS 수신은 보고, 수령은 미확인. PDF 이미지 404는 텍스트 성공과 분리. 개별 receipt/signature가 공개되면 연결 강화 |

## 반례를 찾은 경로
정방향만 검색하지 않았다. 2023–2025 최초 고정 모집창 이후 Paperless duplicate/already/upload 및 Dataverse duplicate/upload를 별도 검색. P11004 최초 성공 ID5와 중복 거절, P10579 휴지통, P10250 고아 파일, D10313 삭제 후 중복, D10209 경로 없는 경고를 직접 읽어 근거 등급을 낮춤. P2667의 사용자 error/성공 역전 및 D9679의 운영 로그 error/시험 성공도 반례. 관측한 것과 제안(Globus, retry, supplier fix)을 분리. 동일 저작의 서로 다른 댓글/판을 하한에 반복 산입하지 않음.

## 미실행/결측
- 원장 일부 재열람은 같은 기록으로 합쳤거나 시각을 분 단위로 기록, 모든 시도/반복 열람의 정확 UTC 및 전체 댓글 앵커는 재현 미완. 66은 고유 저작의 현재 원장상 하한, 이슈 후보/경계/요청 포함. 요청 카테고리별 직접 당사자 P10/D strict3 이상, 공급자 고유 7 이상, 별개 QA·운영 4 이상, 기록보존 운영 2·물류 2. 본문/절 텍스트 판독, 이미지/첨부 파일 직접 검증 미완. 각 사건의 원본 hash와 최종 상태/수신자를 연결할 공개 자료 부족. 일반 사건의 긍정 폐쇄 사슬 없음; 실제 확인 불가와 부정 결과 분리.
- workbench.session start/check --fetch 및 scripts/check.py 실행 없음. 별도 runner에서 아래 입력으로 먼저 세션 계약/owned 경로 검산 후, 이 결과판·인계판의 diff와 JSON/CSV parser를 독립 실행할 것. manifest는 허용 경로만 쓴다. 시작 manifest를 지금 생성해 당시 시작 기록으로 위조하지 않는다.
- GitHub repository public connector를 통한 remote structure verification only. 외부 비용/설치/merge/deploy 없음. 독립 reviewer 없음.
