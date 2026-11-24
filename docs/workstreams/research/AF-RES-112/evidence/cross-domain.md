# 타 분야 보조층

주 6사건의 성과에 더하지 않는다. 원 규격과 실제 사례 두 분야/네 저작을 별도 대사한다.

| 분야 | 원 규격 | 실제 사례 | 같은 URL의 서로 다른 질문 | 반례·한계 |
| --- | --- | --- | --- | --- |
| 박물관 컬렉션 | IIIF Presentation 2.1.1 §2.1; 3.0 같은 계보 재열람 | Harvard object299843 원 Manifest; `evidence/harvard-manifest-observation.json` | 작품 전체를 찾기 / 7개 Canvas 중 원하는 뷰를 고르기 | Canvas를 이미지 파일이나 작품으로 합치지 않는다. 숫자 label에서 앞·뒷면을 추측하지 않는다. |
| 기술 표준 | RFC9110 §8.6/§9.3.2 | Werkzeug3.1.3 `test_response_304_no_content_length` | 일반 응답의 길이 / HEAD 또는304의 길이 의미·허용 생략 | 본문이 없으니 항상0이어야 한다는 해석은 규격과 다르다. 테스트는 미실행이다. |

IIIF2.x의 sequences/canvases와3.x의items를 혼동하지 않았다. Harvard JSON은 웹 텍스트 렌더가거절했지만 동일 원 URL을 셸로직접열어 확인했다. 전송 경로 실패를 원작품/매니페스트 부재로 판정하지 않는다.
