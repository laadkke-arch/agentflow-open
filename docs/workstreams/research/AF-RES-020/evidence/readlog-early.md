# 내부 자료 읽기 기록 — 감사 A

읽은 작업: AF-RES-001·002·003·004·009·010. 각 SHA는 고정 입력에서 읽었으며 다른 새 작업 결과를 열지 않았다. 다음 표의 시각은 검토 뒤 동일 blob을 다시 연 마지막 확인 시각이다. 전체 외부 원문 재조사는 하지 않았다. 직접 열람은 `git show <sha>:<path>`이며 URL은 그 blob의 실제 GitHub 위치다.

| 출처 ID | 작업·SHA | 파일·읽은 범위 | 마지막 직접 확인 UTC | 바이트 SHA-256 |
| --- | --- | --- | --- | --- |
| I001-HANDOFF | AF-RES-001 / `4d6208c08f6f2657865ba000d6768f6537e832b6` | `HANDOFF.md` — 전체 L1–101 | 2026-11-21T05:18:17.234339Z | `5c28d4bfe6de55d8d5843151afebeb6af4e3bcf4019ff98a4efcc94acc8f2d84` |
| I001-RESEARCH | AF-RES-001 / `4d6208c08f6f2657865ba000d6768f6537e832b6` | `RESEARCH.md` — 전체 L1–187; 특히 L25–47,78–126,147–174 | 2026-11-21T05:18:17.239690Z | `ee0a115ac7cd70bb29208e7d12a5ad9a9884b9ab93b4db5eedaf7f962a859e0b` |
| I001-E01 | AF-RES-001 / `4d6208c08f6f2657865ba000d6768f6537e832b6` | `CASES.json` — L1–2336 구조·집계; K01.O5→P3 L307–320; K02 L397–784; K06 L1944–2336; 12 asked_to_user 행 | 2026-11-21T05:18:17.246273Z | `b0f95a2bf55d061adb052e098ce0dbfc6bb9a071b7f7771694d4450da9710922` |
| I002-HANDOFF | AF-RES-002 / `62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1` | `HANDOFF.md` — 전체 L1–149 | 2026-11-21T05:18:17.251891Z | `61d73b5c74efb6e28334c59eb1e97c7546aa6394c8138f5d3405353a7f335ccd` |
| I002-RESEARCH | AF-RES-002 / `62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1` | `RESEARCH.md` — 전체 L1–140; 특히 L39–76,93–110 | 2026-11-21T05:18:17.257700Z | `525e1344e0672171004accca65c41592be58515e35465da987bc4d7a90171945` |
| I002-E01 | AF-RES-002 / `62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1` | `evidence/p1.json` — L231–1088 queries 구조·질의·배치·시각; L1221–1244 P1-C01/C02; scope/limits | 2026-11-21T05:18:17.261914Z | `54c86758890282ce6b9bb792df96523d6e149008287a16da2608fe4283bd3ed4` |
| I002-E02 | AF-RES-002 / `62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1` | `evidence/p2.json` — L11–23 counting; L254 이후 queries; L799 이후 P2-X01; candidate_map/limits | 2026-11-21T05:18:17.266230Z | `36a4d7794d3592ea23ce907eb9c50ab554bb9fb8af2de1c2832d4ef3245bd834` |
| I003-HANDOFF | AF-RES-003 / `b13db3931b4021ff9e1ac6e404590c09526c3087` | `HANDOFF.md` — 전체 L1–116 | 2026-11-21T05:18:17.271114Z | `b97fe26c903ca8dbc3e1d683fe5b2c402f35de9bda8e71b1e15463bc05fb4dea` |
| I003-RESEARCH | AF-RES-003 / `b13db3931b4021ff9e1ac6e404590c09526c3087` | `RESEARCH.md` — 전체 L1–183; 특히 L39–56,70–82,99–142,146–181 | 2026-11-21T05:18:17.275246Z | `130b61a7d224e200aa1fa49e29c972a231adbc9ff15167c4a56bece0eecf070a` |
| I003-E01 | AF-RES-003 / `b13db3931b4021ff9e1ac6e404590c09526c3087` | `CASES.md` — 전체 L1–125; C01–C09 | 2026-11-21T05:18:17.279437Z | `7ec10eae2e0f4244024eae7257a902ccf8eecf3ffaf65917e2d7867c4f40afd7` |
| I003-E02 | AF-RES-003 / `b13db3931b4021ff9e1ac6e404590c09526c3087` | `SOURCES-STANDARDS.md` — 전체 L1–130; R02 L15–21, R06 L47–53, R09–R12 L71–101 | 2026-11-21T05:18:17.284152Z | `24685e973bff1d98a9da7221470ce1d77d69dece5b098a690152dc607c98dfad` |
| I004-HANDOFF | AF-RES-004 / `2b798c7d2b7355b649691c18de196104ceabb0f0` | `HANDOFF.md` — 전체 L1–115; 특히 L76–91 | 2026-11-21T05:18:17.290234Z | `6d1ed49f057464888eec19bb6ce203eebb0ffbe54747de97a607596d5eb0d180` |
| I004-PROTOCOL | AF-RES-004 / `2b798c7d2b7355b649691c18de196104ceabb0f0` | `PROTOCOL.md` — 전체 L1–87; L22–46 및 L78–87 | 2026-11-21T05:18:17.294860Z | `7b010107fbb8d5f5e707b1cffad7626135bde58f9e7316cd4e3dc59612effa96` |
| I004-E01 | AF-RES-004 / `2b798c7d2b7355b649691c18de196104ceabb0f0` | `EXPECTED.json` — 전체 구조 L1–960; 18 rows.label 재계산; R01–R05, R11/R12, R17 상세; R12 L521–594 | 2026-11-21T05:18:17.299084Z | `3cf187263ba92e1ee5b47fe0e6545688f99ba17e21c514e71ff060e86d6439ff` |
| I009-HANDOFF | AF-RES-009 / `7f627a81199f06da7f7b15f979e7fef25dd17602` | `HANDOFF.md` — 전체 L1–175 | 2026-11-21T05:18:17.303793Z | `c0d7b4626b37176e9a2d6311be205404a7711a20c555e76a3a03891ab301e732` |
| I009-GAP | AF-RES-009 / `7f627a81199f06da7f7b15f979e7fef25dd17602` | `GAP.md` — 전체 L1–229; L11,57–59,73–94,113–125 | 2026-11-21T05:18:17.308481Z | `dc7cbcc80c445bbde505ea646f567bd35c44445ecff748cf1fd013655b4bdddf` |
| I009-LANDSCAPE | AF-RES-009 / `7f627a81199f06da7f7b15f979e7fef25dd17602` | `LANDSCAPE.md` — 전체 L1–308; L13–68,157–158,179–207 | 2026-11-21T05:18:17.314246Z | `a9278cbfbd43a7fd7b1e1b0ce45a88d10b877ccb9f49047c77df84886f4b5132` |
| I009-E01 | AF-RES-009 / `7f627a81199f06da7f7b15f979e7fef25dd17602` | `SYSTEMS.json` — 전체 구조 L1–1642 및 systems[*].id/category; SYS-SOURCEGRAPH L518 이후, SYS-GREPAPP L565 이후, SYS-KEYCITE L1469 이후 상세 | 2026-11-21T05:18:17.318946Z | `5c58f5062bc738d7ebca24f45794b03dd93fac7e994a9436a4da354a7a3a5fdf` |
| I009-E02 | AF-RES-009 / `7f627a81199f06da7f7b15f979e7fef25dd17602` | `sources.json` — 구조·선택 5행: S-AC31 L899 이후, S-DE04 L1331 이후, S-FG24 L2803 이후, S-F01 L2889 이후, S-F10 L3132 이후 | 2026-11-21T05:18:17.325664Z | `51a40bae6c5b6288fe9e777e0d2756e324160dba4bb4f0c0a92960290b553793` |
| I010-HANDOFF | AF-RES-010 / `0603f0d2990c7a501dbdfc45fbbba79155f505fc` | `HANDOFF.md` — 전체 L1–131; L5–7,31–38,58–67 | 2026-11-21T05:18:17.332454Z | `827f0bc8869397844f6a0ef07960e1690edd4041cf25f777847c3b87d00c7325` |
| I010-REPRESENTATIONS | AF-RES-010 / `0603f0d2990c7a501dbdfc45fbbba79155f505fc` | `REPRESENTATIONS.md` — 전체 L1–79; L31–49,57–71 | 2026-11-21T05:18:17.336936Z | `11e3334f0ac9b62a5f8033ea6faa0678140eef651f664e8984328052b1207c3e` |
| I010-TRANSFER | AF-RES-010 / `0603f0d2990c7a501dbdfc45fbbba79155f505fc` | `TRANSFER_CASES.md` — 전체 L1–181; L5–28,75–86,140–147,159–181 | 2026-11-21T05:18:17.341327Z | `df7b95fcd897b850c8b993704f40f4636f04f2def23da31eb6856f583b1398e9` |
| I010-E01 | AF-RES-010 / `0603f0d2990c7a501dbdfc45fbbba79155f505fc` | `evidence/comparison-counts.json` — 전체 L1–265 | 2026-11-21T05:18:17.345566Z | `aa853d07016b649946ef9732126ceb9eae68e9c9bceb1bccf51bf459bd9e61e8` |
| I010-E02 | AF-RES-010 / `0603f0d2990c7a501dbdfc45fbbba79155f505fc` | `evidence/p1-judgments.json` — 구조 L1–637; 14 judgments 재계산; RP1-B02 상세, family/bucket/assessment_scope/runtime_observation 필드 | 2026-11-21T05:18:17.350146Z | `4a4449862b6eea168fd71c818f592fc0a5c76a2f34f5fb0fb1f716f43436eb05` |
| I010-E03 | AF-RES-010 / `0603f0d2990c7a501dbdfc45fbbba79155f505fc` | `evidence/p2-judgments.json` — 구조 L1–659; 11 judgments 재계산; RP2-C01 상세, family/bucket/assessment_scope/runtime_observation 필드 | 2026-11-21T05:18:17.354954Z | `c63d9534b522ac6eec7581bb808c86393b13842d00bb31ef235d4a8b1fd4800a` |
| I010-E04 | AF-RES-010 / `0603f0d2990c7a501dbdfc45fbbba79155f505fc` | `evidence/transfer-sources.json` — L6–11 counts; sources[*].id/original_author_transfer/case_ids; T01 L14–40; T10/T11 분류 L272–320 | 2026-11-21T05:18:17.359405Z | `073c28fecba870a323d1f562ff3780b6fe7a60e15b9566c532279534d79d4a14` |

## 대조 방법과 숫자

- 직접 읽은 내부 파일 26개, 고정 입력에 지정된 담당 6작업의 HANDOFF 및 필수 본문 모두 포함한다. JSON 전체 구조·행 집계와 선택 행 의미 대조의 범위를 구별했다.
- 주장 34개: 일치 33, 불일치 1. 2단계 대조 25개. 이 분포는 원 연구의 진실성 비율이 아니라 선택한 전달 주장과 고정 원 결과의 일치 여부다.
- 001: 사례 6, 문장36, 표현18, 추가 질문12, asked_to_user=true 0. 원 연구자의 합성 데이터다.
- 004: rows18의 라벨 재집계는 DIRECT7, MISMATCH6, INSUFFICIENT2, TRANSFER3. pack v1.2 작성자 기대 답이다.
- 009: systems35, category a4/b6/c4/d4/e6/f5/g6. 문서상 기능 비교다.
- 010: family7, 표현별 합계9, 후보 본문24, 판단14+11=25, 웹 질의8×8=64. 전이 본문11, 원 저작9, 사례10. 같은 숫자가 다른 단위로 등장하는 반례를 보존했다.

## 한계

이번 감사는 고정 원 결과와 하위 기록의 대응을 대조했다. 원 저자의 외부 자료가 실제 세계에서 참인지 독립 재실험하지 않았으며, 링크에 있는 현재 외부 내용으로 고정 판을 대체하지 않았다. 같은 모델 계열(GPT-6 Astra Pro)의 내부 별도 검토다.
