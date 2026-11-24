# 사후 분야 전이·반례 판독

사전 판정 `0b6287e5359257004900ef4b8e30f7abb7306024` 이후에만 열었다. 이 묶음의 자료는 A/B 추가 링크의 발견 수·도달 수·새 결정 수에 들어가지 않는다. 고유 배당은 **음향 측정 2저작 + 지도 표본화 2저작**이다. 두 음향 저작의 저자가 같고 두 지도 저작은 표준과 구현 설계가 연결된 계보이므로, 독립된 네 집단의 재현 실험이라고 해석하지 않는다.

## 직접 읽은 자료와 강한 반대 증거

| 고유 배당 | 직접 읽은 주소·절 | 확인과 반대 관측 | 적용 한계 |
| --- | --- | --- | --- |
| EXT-ACOUST-FARINA2000 | [저자 PDF](https://angelofarina.it/Public/Papers/134-AES00.PDF), §2 pp2–6, §5–7 pp10–12 | 순환 처리의 꼬리 접힘과 선형 처리, 조화 성분을 분리하는 시간 간격을 구별했다. | 시계 불일치에 견고하다는 초기 주장을 무제한 보장으로 옮길 수 없다. |
| EXT-ACOUST-FARINA2007 | [저자 PDF](https://www.angelofarina.it/Public/Papers/226-AES122.pdf), §3.4 pp13–15, 그림32–33; §3.3·3.5 | 같은 저자의 후속 원저작이 시계 불일치로 생긴 skew와 보정을 실제 측정으로 보여 준다. 앞선 주장에 필요한 한계다. | 단일 비율 보정의 효과가 불규칙 timestamp·샘플 유실의 해결을 입증하지 않는다. |
| EXT-MAP-OGC11 | [GeoTIFF1.1](https://docs.ogc.org/is/19-008r4/19-008r4.html), §7.2.1, 부록B.2.2·B.6 | 표본의 위치와 셀 영역을 별도로 정의하고, 지정 tiepoint에서의 정확성을 내부 보간의 정확성과 구별한다. | 부록B는 informative다. 이 문서는 dilation 경계의 값이나 음향 시간 방향을 정의하지 않는다. |
| EXT-MAP-GDAL33 | [RFC33](https://gdal.org/en/stable/development/rfc/rfc33_gtiff_pixelispoint.html), 전체 본문, 특히 Rationale·CompatibilityIssues | 구현자가 원 명세를 다시 읽어 위치 해석을 고쳤지만, 과거 구현이 만든 파일에는 호환성 피해가 생긴다. | 표준 준수와 기존 출력 보존은 서로 다른 요구다. 해당 버전의 GDAL 실행은 하지 않았다. |

Müller–Massarani 2001은 [RWTH 목록](https://publications.rwth-aachen.de/record/192865)과 [AES 목록](https://aes.org/publications/elibrary/elibrary-page/?id=10189)에서 저자·권호를 확인했다. 구 AES PDF는404, CiteSeer는 도구별403/404였다. 이후 [공개 저널 사본](https://www.kanedayyy.jp/asp/thesis/zTransfer-Function_Measurement_with_Sweeps_AES_2001443.PDF)의 §1.8·2.4·4.1–4.2와 그림8–9를 읽었다. ±0.5표본 jitter에서 상대적 견고성과 잔여 오염이 함께 보인다. 제3자 호스팅의 독립 보증이 없으므로 **배당에서 제외**했다. 별도52쪽 확장판은 첫 쪽만 대조했으며 방법 본문을 읽었다고 세지 않았다. 접근·원문 지문은 acquisition-receipts.json, 세부 판독은 sources.jsonl에 있다.

## 옮길 수 있는 관계와 옮기면 안 되는 결론

음향 측정에서 신호는 값 배열과 물리적 시간축을 함께 가진다. 지도 raster도 값 배열과 좌표 변환을 함께 가진다. 두 분야의 공통 검산 관계는 **같은 배열 인덱스가 같은 물리적 위치를 뜻하는지**다. 이 관계를 R1의 block/sample-rate 정렬 시험에 적용할 수 있지만, 어느 문헌도 MKV를 여는 디코더 선택을 제공하지 않는다. 관련성이 있어도 원 오류의 해법으로 반환하면 안 되는 사례다.

R5의 경계 문제에서 위치 정렬과 외부 값 선택은 분리해야 한다. 반 픽셀 이동은 어떤 위치의 값을 참조하는지 바꾸고, min/ignore/reflect는 바깥 위치의 값을 어떻게 정의하는지 바꾼다. 한쪽의 수정이 다른 쪽을 증명하지 않는다. R3의 빈 이웃 행 역시 물리적 표본 누락과 동일한 개념으로 놓을 수 없다. 그래프의 고립은 관계가 없다는 뜻이고 시간축 누락은 좌표 정보 문제이므로, 원전의 직접 계보 없이 같은 해결책으로 합치지 않았다.

현장 사용자의 가장 강한 반론은 원전대로 고친 결과가 기존 파일·출력의 의미를 바꿀 수 있다는 RFC33 사례다. 구현자의 반론은 문헌상 조건을 코드가 어디서 책임지는지 별도 확인해야 한다는 것이다. 원 분야 저자의 반론은 자신의 후속 연구가 드러낸 실패 조건을 초기 문장의 일반화보다 우선해야 한다는 것이다. 원 AF-RES 요청자의 실제 후속 채택은 이 자료로 확인할 수 없다.

## 구성 입력과 관측의 구분

transfer-tests.json에는 여섯 개의 사후 구성 입력을 저장했다. `counterexample_arithmetic.py`는 그중 네 개의 배열·삼각함수·좌표·시간 간격 계산만 검사한다. 이는 원 논문 실험, librosa/skimage/GDAL 실행, 새로운 A/B 링크 효과가 아니다. 실제 원전의 측정은 source_observations에, 구성 예상은 predicted_outputs에 분리했다. 현 단계에서 판단을 바꿀 가장 작은 추가 입력은 원 MKV의 코덱·실제 표본 시간축, 위치 의미가 알려진 PixelIsPoint 파일의 생성기 버전, 그리고 원전의 측정 원시 신호다.
