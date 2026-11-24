# 출처 최소량·중복 별도 검토

검토자 `/root/contract_prior_audit`가 canonical `sources.jsonl`을 다시 대사했다. 정확한 입력 SHA256·UTC는 `source-audit.json`에 있다. 검토하는 동안 새 후속 영수증이 합쳐져 원장 행 수는 안내받은293에서 **301**로 늘었지만, 산입된 고유1차자료는 **32**, 필수24의 ID는 변하지 않았다.

## 결론

**자료를 직접 읽는 최소량은 범위를 명시하면 충족한다.** 필수24개가 모두 존재하고 산입되어 있으며, 산입32개에 같은 저작/요청의 중복 계보는 찾지 못했다. 다만 QGIS GDAL 시험의 정확한 행 설명이 뒤바뀌어 있으므로 최종 출판 전 위치를 고쳐야 한다. 이 검토가 사용자 결과나 GN 전체 회귀 실행까지 인증하는 것은 아니다.

| 필수 범주 | 요구 | 대사 결과 | 범위 |
|---|---:|---:|---|
| 시간순 원 요청 | 8 | 8 | 고정 최초판8; 보조4를 섞지 않음 |
| Blender 공식 문서/구현 | 4 | 4 | 4.0의 서로 다른 Accumulate Field, Sample Curve, Link Data, Extrude Mesh 페이지 |
| QGIS 공식 문서/구현 | 4 | 4 | 3.34.0의 labeling, expression, Build VRT, Warp 구현 파일 |
| Blender 상류 시험/입출력 | 2 | 2 | **저수준 C++ 수학 단위시험의 입력·기대출력**, GN 통합 fixture는 아님 |
| QGIS 상류 시험/입출력 | 2 | 2 | literal expression→값, 처리 매개변수→예상 CLI 문자열; 픽셀 결과 시험 아님 |
| Calc 설명+별도 원 예제 | 2 | 2 | pinned24.2 설명과 별도 formula C++ 시험 |
| Audacity 설명+별도 원 예제 | 2 | 2 | pinned3.6.4 설명과 3.1.3 보고자의 원 재현 사례/그림 |
| **필수 합계** | **24** | **24** | 문서의 여러 앵커·같은 사건 댓글·이미지·연구자 synthetic probe를 추가 산입하지 않음 |

추가8은 보조 원 요청4, QGIS function help1, GDAL gotchas1, spdep의 별도 문서/구현2다. 따라서 총산입32와 필수 구성24를 별도로 보고하는 것이 맞다.

## Blender 상류 두 시험을 어떻게 인정하는가

[회전 시험](https://projects.blender.org/blender/blender/src/tag/v4.0.2/source/blender/blenlib/tests/BLI_math_rotation_test.cc)과 [벡터 시험](https://projects.blender.org/blender/blender/src/tag/v4.0.2/source/blender/blenlib/tests/BLI_math_vector_test.cc)의 저장된 원문을 직접 다시 읽고, API base64 내용·UTF8 SHA256·Git blob SHA1이 원장의 고정값과 일치함을 확인했다.

- 회전 시험 L317–331은 `(1,0,0)`을 Z축으로 π/2 또는 π만큼 회전한 기대값 `(0,1,0)`과 `(-1,0,0)`을 명시한다. L453 이후는 같은 벡터에 tracking/up axis를 달리한 기대 quaternion을 제공한다.
- 벡터 시험 L89–107은 정수와 실수 보간에 대한 실제 입력·기대값을 명시한다. L138–172는 sqrt, reciprocal 및 안전 처리의 입력·기대값을 명시한다.

이것은 generic smoke test가 아니라 실제 상류 수학 단위시험 두 저작이다. 그러므로 사용자/SCOPE의 ‘서로 다른 상류 시험·입출력 예제’라는 읽기 범주에 산입하는 것은 방어 가능하다. 그러나 **노드 이름이 비슷하다는 이유로 그 함수가 해당 GN 노드의 동일 호출 경로라고 증명되지는 않는다.** 두 파일은 Pivot Auto 동작, 전체 가중 curve graph, 도메인 평가, 랜덤 분포 또는 원 작성자 graph의 회귀 fixture를 대체하지 못한다. 최종 표현은 ‘Blender C++ 수학 단위시험2개를 읽음; GN 통합 fixture 확보/실행 미실시’로 제한해야 한다. 후자의 결측을 source quota 충족으로 지워서는 안 된다.

## 발견한 위치 오류 — 반드시 정정

`QG-T-U-GDAL`은 읽은 내용의 결론은 맞지만, `location.read_sections`가 BuildVrt와 Warp의 행 번호를 서로 바꾸어 적었다. 고정 파일의 실제 위치는 다음과 같다.

| 내용 | 올바른 위치 |
|---|---|
| `testWarp` 시작 | L1948 |
| `TARGET_RESOLUTION=10.0` → `-tr 10.0 10.0` | L2078–2087 |
| `testBuildVrt` 시작 | L2740 |
| 생략된 `SEPARATE` → `-separate` | L2747–2757 |
| `SEPARATE=False` → `-separate` 없음 | L2769–2779 |

원본: [고정 QGIS 시험 파일](https://github.com/qgis/QGIS/blob/ffbdd678812eec460ff02ff73bd36ee7955ac8a5/python/plugins/processing/tests/GdalAlgorithmsRasterTest.py). 원장과 해당 판독/최종 표의 행 링크를 함께 정정해야 한다. 이것은 봉인된 선정이나 결과값을 바꾸는 수정이 아니라 출처 위치의 오류 수정이다.

## 스키마와 표현 주의

- QGIS 필수6개는 개별 최소량 플래그가 참이지만 canonical `category`는 아직 `supplementary_evidence`다. category만 합산하면 잘못된 구성표가 나온다. 명시적인 필수ID→범주 매핑 또는 정규화가 필요하다.
- Blender4.0 실제 문서는 `Group Index`, `Scale`이라는 표기를 쓴다. 원장의 `Group ID`, `Offset Scale`은 그래프 UI와 대응하는 표현이므로 정확한 매뉴얼 인용/절 제목처럼 표시하지 않는다. 기능 해석은 상충하지 않았다.
- QGIS GDAL 시험은 명령 생성의 기대문자열이다. 원 TIFF를 읽거나 실제 픽셀을 비교하지 않았다는 한계가 이미 기록되어 있으며 계속 유지해야 한다.
- 후속/보조의 같은 사건 여러 댓글, 한 test file의 여러 절, 현재 매뉴얼과 pinned 사본, 같은 버그의 첨부그림, 실패 응답은 총32에 중복 산입되지 않았다.
- 이번 검토는 최종 RESULT/반환표 검토 전이며 모든301개 기록의 내용을 전수 재판독한 검증이 아니다. 필수 출처의 구성·계보와 선택한 원문 위치를 대사했다. 교차 분야 자료의 내용은 이 검토자가 작성한 것이므로 그 부분은 자기 확인이다.
