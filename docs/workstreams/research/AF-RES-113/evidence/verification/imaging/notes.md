# 영상 원전의 사후 대조

판정 봉인 `0b6287e5359257004900ef4b8e30f7abb7306024` 이후 읽었다. 이 독자는 A/B의 새 문맥 판독자가 아니며 원경로 성과를 다시 채점하지 않는다. **방법 제안자 원전 3개 본문**, 별도 survey 1개 본문을 읽었다. publisher 실패 2개와 요약만 본 van Herk 후보, 같은 저작 재열람은 고유 배당에서 제외했다. 정확한 읽은 절·UTC·파일 지문은 `sources.jsonl`, 취득 byte 영수증은 `acquisition.json`에 있다. 원문 전체나 PDF는 결과 파일에 재게시하지 않았다.

## 판정에 영향을 주는 대조

| 원자료·읽은 절 | 확인한 범위 | 요청에 대한 반대 증거와 한계 |
| --- | --- | --- |
| [Otsu1979](https://skynet.ecn.purdue.edu/~ace/vip/A_Threshold_Selection_Method_from_Gray-Level_Histograms_otsu.pdf), §II Eq1–19, §III–IV | Histogram의 두 클래스 분리를 최적화한다. | R4의 ndarray 차원 거부는 이 수학에서 나오지 않는다. 원문을 보고1D를 허용하면 원 요청의 계약을 바꾼다. `POST-IMG-OTSU-HIST`는 수학과 API 책임을 분리한다. |
| [Gil–Kimmel2002](https://www.cs.technion.ac.il/wp-content/ron-kimmel/papers/EfficientMorphology_KimmelGil_PAMI_2002.pdf), §1–3.3, §6 | 연속 창의 prefix/suffix 재사용. p1607은 border를 제외한다. | R5에서 중요한 경계 조건을 원전이 보장하지 않는다. 사각 창 분해를 비연속 footprint로 확대할 수도 없다. `POST-IMG-SPARSE`는 경계 영향을 제거한 반례다. |
| [Pye–Bangham1996](https://www.eurasip.org/Proceedings/Eusipco/1996/paper/pi_12.pdf), §2 Eq1–24, §3–4 | Flat line의 국소 최대 확장·부분 결과 max 결합. Eq24의 밖은−∞다. | 중립값의 역할은 비교할 수 있지만, 부분 신호 밖과 유한 이미지 경계는 같은 계약이 아니다. 원전의 trailing→centered 이동은 온라인 지연 조건까지 보존하지 않는다. |
| [Soille2002](https://utopia.duth.gr/~agaster/papers/cite/morphologicalrank.pdf), §2/Table1 | Reflection 여부가 다른 dilation 관례와 원점 포함 조건을 구별한다. | 같은 이름은 같은 연산을 보장하지 않는다. 비대칭 방향 문제와 경계 외삽 문제를 분리한다. Survey이므로 방법 제안자 배당에서 제외한다. |

## 관측·예상·실행의 구분

원 논문의 정의·문장·도표는 `source_observed`다. `test-proposals.json`의 수치 입력과 두 예상값은 작업자가 구성한 반례이며 실행하지 않았다. 두 번째 클릭에서 얻은 새 시험은 아니다. R5 경계 입력은 이미 봉인한 baseline을 사후 대조에 재사용했다. 원 API의 현 버전 출력,1D 예외 문자열,원 작성자의 후속 채택은 이 분담에서 관측하지 않았다.

PDF 수식 추출에는 잘못된 부호·글리프가 있었다. Otsu p63, Gil–Kimmel p1607, Pye–Bangham PDF p3, Soille pp528–529를 렌더해 실제 부호와 도표를 확인했다. Otsu Eq1의 비음수 조건과 Eq18 분모, Pye Eq24의−∞는 이미지로 확인했다. Gil–Kimmel §4–5의 전체 증명은 열람 범위에 포함시키지 않는다. Soille도 전체9페이지를 완독했다고 주장하지 않는다.

## 반환 설계에 주는 제한

R4는 일반 원방법 설명보다 이미 공통절에 있는 지원 차원·정상 입력과 실제 dispatch 검사가 직접적이다. R5는 경계 모드와 footprint의 정의를 먼저 검증해야 한다. 원논문의 빠른 알고리즘이나 같은 단어만 반환하면 보존해야 할 support·원점·시간 가정이 사라질 수 있다. 이 결론은 사후 반례이며 원경로 A/B 추가결정0을 긍정 효과로 바꾸지 않는다.
