# scikit-image 공통 시작 절 검토 — 두 번째 링크 개봉 전

판독자 `/root/recruit_skimage`. 2026-11-24 04:05–04:06 UTC에 배포 HTML 두 개와 해당 고정 태그의 함수 docstring만 직접 읽었다. 두 번째 링크·구현 본문·회귀시험은 열지 않았다. 모집의 첫3건은 #6664, #6665, #6670으로 유지한다. 정확한 URL·도착·문자수·지문·링크 DOM 순서는 [skimage-common.json](skimage-common.json)에 있다.

## 판과 공통 경계

root가 확인한 공식 API 목차는 `https://scikit-image.org/docs/0.26.x/api/api.html`이다. 이 검토자는 그 목차에서 지정한 `skimage.filters.rank.html`, `skimage.morphology.html` 두 배포 페이지의 목표 `dt` 부모 `dl.py.function`만 공통 절로 추출했다. 페이지 제목은 모두 **0.26.0**, source href의 tag는 **v0.26.0**이었다. 원 소스 docstring은 root가 확인한 tag commit `ee0a7a3ebd9ac8c2602f40e55bc015a3c8a81ae8`에 고정했다.

배포 파일의 HTTP Last-Modified는 두 개 모두 `2026-11-21T01:15:01Z`다. 이것을 v0.26.0 릴리스일이나 2023 이슈 당시 상태로 해석하지 않는다. `0.26.x` URL은 바뀔 수 있으므로 이번 본문의 SHA256과 독해 시각을 함께 보존한다.

| 요청 | 공통 시작 | 본문 문자수·지문 | 실제 링크 선택 |
| --- | --- | --- | --- |
| R4 #6664 | [rank.otsu](https://scikit-image.org/docs/0.26.x/api/skimage.filters.rank.html#skimage.filters.rank.otsu) | 1,384 Unicode code points; `05a03708f2138740c7d6eff98a72b8913d6f95763adf3dd769c521b198e69de4` | A=DOM4 Rank filters; B=없음 |
| R5 #6665 | [morphology.dilation](https://scikit-image.org/docs/0.26.x/api/skimage.morphology.html#skimage.morphology.dilation) | 3,407; `4192b4f6765766a2df9755bd17ce86f899279b262ffbe7b3b0f43a9b513a0a1d` | A=DOM8 cornea inpainting; B=없음 |
| R6 #6670 | 공석 | 0; 지문 없음 | A/B 모두 시작 심벌 대응 공석 |

3,000자 상한은 **추가 열람**에만 적용한다. 따라서 R5의 공통 절 3,407자를 임의로 자르지 않았다. HTML의 제목/매개변수/Notes/References/inline Examples/같은 dl의 gallery title은 모두 양쪽에 주어질 공통 노출이다.

## R4: rank.otsu의 이미 알려진 선택

[원글](https://github.com/scikit-image/scikit-image/issues/6664)은 1D 입력이 잘못됐을 때 3D만 허용한다는 듯한 진단을 바꾸려 한다. 원글 Proposed solution의 LF31–38에는 정상 2D와3D 반환 분기를 두고 나머지 입력에 오류를 내는 코드가 있다. 이 차원 분기 자체를 예제나 출전에서 새로 얻었다고 셀 수 없다.

공통 절은 입력 shape `([P,] M, N)`, uint8/uint16, 같은 shape·dtype의 출력, 양수 mask의 포함 규칙, footprint 안에 있어야 하는 이동 중심을 명시한다. inline Examples는 2D camera와 3D random volume, disk와 ball footprint, 그리고 영상과 local threshold를 비교하는 순서를 이미 준다. 따라서 후속 gallery가 같은 2D threshold 코드를 반복하면 추가 선택은 아니다.

사전 시험 R4-C0은 원글 그대로 `otsu(np.eye(10).ravel(), disk(3))`의 오류문구를 가른다. 기존 예상은 3D만 언급하는 오류, 원글 제안 예상은 2D/3D를 함께 언급하는 오류다. 현재 v0.26.0의 실제 오류는 실행하지 않았다. R4-C1은 공통 예제의 정상2D/3D 입력에서 shape·dtype을 보존하며 1D만 거부하는지 확인할 시험이다. 공통 문서에는 사용 코드가 있으나 그 실행 로그나 출력 배열은 없다.

### A/B 링크

- DOM1 source, DOM2 같은 심벌 anchor는 두 경로의 추가 자료가 아니다.
- DOM3은 Wikipedia의 Otsu 설명이다. 방법 제안자가 쓴 원저작 링크가 아니므로 B에서 제외한다. 여기서 Wikipedia를 열거나 그 안의 논문으로 다시 이동하면 사전 규칙 밖이다.
- DOM4의 [Rank filters](https://scikit-image.org/docs/0.26.x/auto_examples/applications/plot_rank_filters.html)가 A의 첫 실제 연결 예제다. DOM5 [Thresholding](https://scikit-image.org/docs/0.26.x/auto_examples/applications/plot_thresholding_guide.html)은 적격 예제지만 두 번째 순위이므로 대체하지 않는다.

해당 gallery thumbnail은 함수 `dd` 안에 있으며 함수 뒤 sibling이 아니다. 뒤에는 `hr`와 다음 함수 `percentile`의 dl이 있다.

## R5: dilation은 시작 절 자체에 중요한 모순이 있다

[원글](https://github.com/scikit-image/scikit-image/issues/6665)의 기지안은 비compact footprint가 영상 밖을 샘플링할 때 reflect로 내부값을 복제하지 않고 자료형 최소값을 넣는 방식과, 사용자에게 경계모드를 고르게 하는 방식이다. 따라서 상수 경계값 또는 경계모드 선택 자체는 후속 발견으로 세지 않는다.

공통 절에는 `mode`와 `cval`이 이미 노출돼 있고 0.23에 추가됐다고 적혀 있다. 기본은 reflect다. Notes는 footprint 분해 순서, grayscale과 binary dilation의 비대칭 footprint 방향 차이, `mirror_footprint`도 이미 설명한다. 원글은 2023 사건이지만 이번 판단은 2026년에 이 공통 절을 읽은 시점이다. 현행 매개변수 추가를 원 작성자가 당시 알고 있었던 사실로 바꾸지 않는다.

**Parameters→mode에는 내부 모순이 있다.** min/ignore를 설명하면서 영상 밖에 자료형의 **최대값**을 둔다고 쓰고, 그러면 결과에 영향을 주지 않는다고 덧붙인다. 같은 절의 dilation 정의는 이웃의 최대값 선택이다. 이는 원글의 중립 최소값 제안과도 충돌한다. 이 문장은 [고정 tag의 gray.py](https://github.com/scikit-image/scikit-image/blob/ee0a7a3ebd9ac8c2602f40e55bc015a3c8a81ae8/src/skimage/morphology/gray.py)의 docstring **206–208행**에도 있다. HTML 변환만의 차이가 아니다.

아직 구현을 읽지 않았으므로 min/ignore의 실제 연산을 확정하지 않는다. 사전 R5-C1은 `image=np.array([[7]], dtype=np.uint8)`와 `footprint=np.array([[1,0,1]], dtype=np.uint8)`를 사용한다. 반사 확장은 7, 명시적 constant cval0은0, 문서의 최대값 문장을 그대로 적용한 해석은255를 예측한다. 이 세 값은 **연구자의 수학적 예상**이며 실제 실행 결과가 아니다. 이 입력은 footprint의 중심을 제외해 경계 영향과 시작점/방향 혼동을 분리하려는 구성 입력이다.

공통 inline example은 5×5 영상의 중앙 밝은 픽셀을 3×3 block으로 넓히며 결과 배열을 보여 준다. 그것은 중앙 내부의 결과를 보여 주므로 이 요청의 경계 정책 차이를 구별하지 못한다. 해당 출력은 문서의 관측값이고 이 검토자의 실행값이 아니다.

### A/B 링크

DOM3 rank.maximum, DOM4 disk, DOM7 mirror_footprint는 함수 cross-reference다. source·자기 anchor와 함께 A/B의 적격 독립 자료에서 제외한다. 이 dl에는 방법 원저작 reference가 없으므로 B는 공석이다.

A는 DOM8의 [Restore spotted cornea image with inpainting](https://scikit-image.org/docs/0.26.x/auto_examples/applications/plot_cornea_spot_inpainting.html)이다. 뒤의 fluorescence, Morphological Filtering, Rank filters, inpainting, segmentation label 예제들은 순위가 뒤다. 더 직접적으로 보이는 Morphological Filtering으로 교체하지 않았다. 여기서도 gallery는 함수 dl 안에 있으며 다음 sibling은 `hr`와 `disk` 함수의 dl이다.

## R6: 심벌이 불명확한 요청을 보존한다

#6670의 첫 목표는 `test_lab_lch_roundtrip_dtypes`다. 본문 코드는 rgb2lab로 입력을 준비하고 `lch2lab(lab2lch(lab))`라는 두 단계 왕복을 비교한다. 최초 목표 API 하나가 명확하다는 근거가 부족하다. root와 원글을 교차 검토한 뒤 공통 시작 절을 비워 두었다. 관련 논문이나 gallery가 풍부한 함수로 교체하지 않는다. dtype·허용오차·big-endian 실패라는 원 요청은 유효하며 두 예정 hop 자리는 계속 유지한다.

## 실제 노출과 재사용 경계

함수 경계의 gallery 위치를 조사할 때 다음 함수 percentile과 disk의 첫500자와 링크 목록까지 도구 출력에 들어갔다. 특히 disk에 붙은 원전 URL도 노출됐다. 해당 자료를 클릭하지 않았고, 이 다른 함수의 reference를 R5의 B로 편입하지 않았다. `skimage-common.json.exposure_note`에 이 과다 노출을 기록했다. 이 검토자를 완전히 가려진 독자로 부르면 안 된다.

경로별 새 판독자에게는 cache의 `.text.json`에서 목표 `text`만 제공하고 `dom_location.following_siblings`는 주지 않아야 한다. raw HTML·원 소스 전체는 기계 취득 캐시다. 실제 독해는 위의 목표 함수 본문, 허용된 함수 docstring, 기록된 불필요한 sibling 일부뿐이다. 원 소스 전체 파일을 읽었다고 산입하지 않는다. docstring과 배포 HTML은 같은 함수 저작의 두 표현이므로 고유 자료 수를 두 배로 세지 않는다.

이 단계의 **A/B 링크 개봉0, 원 프로젝트 실행0, 그림 열람0, 댓글·채택 검사0**이다. 다음 행동은 공통 입력과 링크 선택을 원격 봉인한 뒤 A의 두 링크를 같은 추가 예산으로 여는 것이다. mode 모순의 구현·회귀 입력 대조는 사전 판정 봉인 이후에 한다.
