# AF-RES-079 가림 재판독

## 판독자·입력·가림의 범위

판독자는 별도 도구 에이전트 `/root/standards_evidence`다. 인간 검토나 다른 모델의 독립성을 주장하지 않는다. 외부 표준 조사를 먼저 맡았으나 본 연구의 GIS·OSS·대조 첫 판정, 수선안, events/relations/notes와 RESULT는 읽지 않았다. 입력은 SCOPE.md, 각 분야의 source-only evidence packet 세 개, 원문 URL과 발행판·절이다. 입력 파일의 SHA256·시각과 원문 URL은 `blind-review.json`에 고정했다.

첫 판정과 수선안은 가려졌지만, 연구자가 선택한 사건·출처·옛/새 대상 표기는 보였다. 발행판의 전체 모집틀과 제외 순위는 이번 재판독에서 독립 전수검사하지 않았다. 부모 에이전트가 GIS 모집 정정 및 원문 날짜 충돌을 알렸고 C02의 추가 원문 주소를 제공했다. 관계 코드와 첫 수선안은 전달받지 않았다. 따라서 **판정 가림은 유지되었으나 출처 선정과 모든 발견 과정이 가려진 것은 아니다.**

최초 GIS packet에는 잠정 G01=ARG, G02=Parquet가 있었다. 해당 원문을 읽은 뒤 최종 packet(2026-11-23 11:35:48 UTC)의 G01=Rasdaman, G02=ARG로 다시 판독했다. 잠정 Parquet는 최종 6건에 넣지 않았다. 과거 접근 영수증은 삭제하지 않았으며 `http-receipts.jsonl`에서 당시 key와 실제 URL로 구별할 수 있다. 원래 ARG 접근 영수증은 최종 G02의 근거다. O02의 처음 제공된 `quadrature.py` 주소는 404였고 같은 커밋의 `_quadrature.py`를 직접 열었다. 최종 packet은 이미 올바른 주소를 담고 있다.

모든 행동 판단은 직접 읽은 구현·문서·공급자 보고에 기반한다. 이 판독자는 GDAL·SciPy·PIL 등을 설치하거나 동일 입력 시험을 실행하지 않았다. 아래 숫자 예시는 소스에서 유도한 **예측**이다. 첫 판정과의 일치율은 계산하지 않았다. 범위가 같은 주장끼리 사후 비교할 수 있도록 한 사건의 여러 단위를 따로 표시했다.

## 여섯 사건의 관계 판단

| 사건 | 먼저 고정한 식별 단위 | 주 판정 | 별도로 남긴 관계·보류 |
| --- | --- | --- | --- |
| G01 Rasdaman | 논리적 GDAL RASDAMAN driver와 배포·소스 보관 위치를 구별 | ① 논리적 driver ID 유지 | ④ core 안의 구성요소 → 별도 extra-drivers 보관물. 실제 설치 가능한 대체물이나 출력 기능의 동일성은 미확인 |
| G02 ARG | 역사적 GDAL driver, 지정되지 않은 후속 | ① 옛 driver ID 유지 | ⑤ 대체 대상 보류. 3.8 폐기 예고와 3.9 등록 제거를 보존 |
| O01 MAD | 기본값과 scale 의미를 포함한 공개 callable 계약 | ④ 옛 callable → 인자 변환이 필요한 후속 callable | 기존 한 레코드가 두 계약을 섞었을 때만 ③ 조건부 분리 |
| O02 SciPy 이름 캠페인 | fully-qualified 함수/분포 이름별 네 쌍 | ② 1.6.0 범위의 쌍별 별칭 | 네 쌍을 같은 기능으로 합치지 않음. 이후 판의 별칭 존속은 미확인 |
| C01 scikits.learn | 동일 프로젝트의 import namespace | ② 0.9에서 확인한 namespace 별칭 | ① 프로젝트 유지. 전체 학습 기능의 판간 동작은 별도 |
| C02 PIL/Pillow | 배포물·프로젝트, 공유 import 이름, PyPI 소유권을 구별 | ④ PIL → Pillow fork/후속 | 레코드가 실제로 여러 단위를 섞었을 때만 ③ 조건부 분리 |

어느 packet도 실제 운영 중인 혼합 레코드를 제공하지 않았다. 따라서 ③을 확정한 혼합 사례나 관측된 거짓 병합으로 세지 않는다. 같은 이름을 가진 서로 다른 대상이라는 발견과 기존 레코드가 이미 섞였다는 발견은 다르다.

### G01: 소스 계보 유지와 실행 가능한 부품의 부재

[GDAL 3.7.0 NEWS](https://github.com/OSGeo/gdal/blob/ab9cb1a1d4928cdcf2877d8e0c6ad9fc2c79fbc9/NEWS.md#L37-L38), [유지관리자 발언](https://github.com/OSGeo/gdal/issues/4808#issuecomment-1465303489), [수신 저장소 커밋](https://github.com/OSGeo/gdal-extra-drivers/commit/ffe0c44714a491eb90ba82d8df74f621ac6003e7)은 Rasdaman 소스의 이동을 가리킨다. 수신 커밋과 발언은 2023-03-12다. 이 명시적 계보 아래 논리적 driver ID를 보존한다.

다만 [수신 README](https://github.com/OSGeo/gdal-extra-drivers/blob/ffe0c44714a491eb90ba82d8df74f621ac6003e7/README.md)는 해당 소스를 빌드에 포함하지 않은 영역에 둔다. core에 들어 있는 driver와 별도 보관된 소스의 공급 상태는 다르다. 두 컨테이너 사이에 방향 있는 이동 관계④를 기록하되, 새 URL만으로 설치·작동 가능성을 넘겨받지 않는다. README의 목록 위 일반 제목은 GDAL 3.5 제거라고 되어 있지만 Rasdaman의 정확한 이동 커밋·3.7 NEWS와 맞지 않는다. 이 포괄 제목을 Rasdaman의 제거판으로 삼지 않는다.

P1에서는 [이전 등록 코드](https://github.com/OSGeo/gdal/blob/b77481ccf9f84a708fd37a13a7e0a3384fdf1622/frmts/gdalallregister.cpp#L158-L160)에 있던 등록이 3.7에서 사라졌다. stock GDAL의 기존 lookup/open 성공을 예측할 수 없다. 더구나 [driver 문서](https://github.com/OSGeo/gdal-extra-drivers/blob/ffe0c44714a491eb90ba82d8df74f621ac6003e7/not_integrated_in_build/rasdaman/rasdaman.rst)는 파일 대신 rasql 질의를 사용하고 지리참조 읽기·쓰기를 지원하지 않는다. 고정 raster fixture의 지리참조 전체 계약은 이전판에서도 성립하지 않는다. P2의 생성·쓰기 계약 역시 [이전 등록 구현](https://github.com/OSGeo/gdal/blob/b77481ccf9f84a708fd37a13a7e0a3384fdf1622/frmts/rasdaman/rasdamandataset.cpp#L700-L716)의 open 중심 구성과 문서로 지지되지 않는다. 동일 driver 계보를 인정해도 P2 성공이 따라오지 않는다.

재개에는 정확한 GDAL판에 맞춰 빌드한 extra-driver, 동일 rasql 데이터베이스 입력과 결과·오류 fixture가 필요하다. 지리참조·쓰기 기능을 충족하려면 이를 지원하는 실제 구현 근거가 추가되어야 한다. 첫 판정이 배포물 단위를 사용했다면 이 리뷰의 ④ 항목과 비교해야 한다. 논리 driver 단위의 ①과 직접 맞대어 불일치로 세면 단위 차이를 판정 차이로 오인한다.

### G02: 폐기 기록은 남지만 후속 ID는 만들어지지 않는다

[3.8 NEWS](https://github.com/OSGeo/gdal/blob/c46fe7e20e33925735ae4b785752795af72823bc/NEWS.md#L25)와 [3.9 NEWS](https://github.com/OSGeo/gdal/blob/bb5ea618e23e498e79e8b8e6bd7215ad94bb2103/NEWS.md#L25)는 ARG의 예고와 제거를 연결한다. [옛 driver 문서](https://github.com/OSGeo/gdal/blob/c46fe7e20e33925735ae4b785752795af72823bc/doc/source/drivers/raster/arg.rst#L16-L37)의 보편적 포맷으로 변환하라는 조언은 특정 후속을 지정하지 않는다. 그러므로 ARG의 옛 ID·원절·폐기판은 유지하고, 후속 수선은 보류한다.

[공급자 시험](https://github.com/OSGeo/gdal/blob/c46fe7e20e33925735ae4b785752795af72823bc/autotest/gdrivers/arg.py#L48-L51)은 폐기 driver를 명시적 설정으로 켠다. 시험 정의가 있다는 사실로 기본 설정의 P1 성공을 주장할 수 없다. 3.9 이후 등록 부재는 기존 driver 사용 불가를 예측하게 하지만 실제 실행 결과는 아니다. P2에는 선택한 대체 포맷, 동일 ARG 입력, 이전 소비자판, 값·형·순서·CRS·nodata·손상 파일의 오류 비교가 필요하다. live raster 목록으로 옛 URL을 바꿔도 특정 대체 기능은 생기지 않는다.

### O01: 같은 두 판에서 P1과 P2의 결론이 달라진다

[1.4.1 옛 함수](https://docs.scipy.org/doc/scipy-1.4.1/reference/generated/scipy.stats.median_absolute_deviation.html)와 [1.5.0 새 함수](https://docs.scipy.org/doc/scipy-1.5.0/reference/generated/scipy.stats.median_abs_deviation.html)는 scale의 기본값과 곱셈/나눗셈 의미가 다르다. [PR11431](https://github.com/scipy/scipy/pull/11431)과 [고정 구현](https://github.com/scipy/scipy/blob/4c0fd79391e3b2ec2738bf85bb5dab366dcd12e4/scipy/stats/stats.py#L2878-L3151)은 옛 이름의 wrapper를 남기고 숫자 scale을 역수로 바꿔 전달한다. 따라서 프로젝트와 계산 목적은 이어지지만 공개 호출 계약은 무조건 별칭으로 합칠 수 없다.

P1에서 옛 호출을 그대로 두면 wrapper가 수치 계약을 보존한다는 정적 근거가 있다. 새 경고 정책과 경계 입력은 별도다. P2에서 이름만 새 함수로 바꾸면 `y=[1,3,2]`의 기본 결과는 옛 1.4826에서 새 1.0으로 달라질 것으로 예측된다. `scale=2`는 옛 결과 2.0, 새 결과 0.5를 구별한다. 이는 실행값이 아니라 소스 의미에서 유도한 예측이다. 이름만 바꾼 교체는 거절하고, 명시적 scale 역변환 후 dtype·NaN·축·빈 입력·오류 검사를 거친 교체를 재개 대상으로 둔다.

### O02: 한 변경 사건 안에서도 기능 ID는 네 쌍이다

[1.6.0 공지](https://github.com/scipy/scipy/blob/ab1c0907fe9255582397db04592d6066745018d3/doc/release/1.6.0-notes.rst), [PR12927](https://github.com/scipy/scipy/pull/12927), [PR12934](https://github.com/scipy/scipy/pull/12934)는 [공통 issue12924](https://github.com/scipy/scipy/issues/12924)의 이름 변경을 구현한다. 하나의 조정된 이름 변경 사건으로 세는 것은 타당하다. 하지만 integrate의 simps, trapz, cumtrapz와 stats의 trapz는 서로 다른 기능이다. 특히 짧은 이름 trapz만으로 수치적분과 확률분포를 합칠 수 없다.

[옛 구현](https://github.com/scipy/scipy/blob/19acfed431060aafaa963f7e530c95e70cd4b85c/scipy/integrate/_quadrature.py)과 [새 구현](https://github.com/scipy/scipy/blob/ab1c0907fe9255582397db04592d6066745018d3/scipy/integrate/_quadrature.py)의 적분 wrapper는 대응하는 새 함수에 같은 인자를 보낸다. 1.6.0 범위에서 각 쌍의 별칭②를 인정한다. P1 옛 이름과 P2 새 이름 모두 정적 호환 근거가 있지만, 전체 dtype·축·잘못된 shape 예외의 양판 실행은 이 판독자가 하지 않았다. stats 쌍은 별도의 분포 입력을 써야 하며 quadrature fixture의 결과를 옮겨 성공으로 세지 않는다. 이후 판에도 옛 이름이 계속 존재한다고 추정하지 않는다.

### C01: namespace 별칭은 프로젝트 전체의 행동 보증이 아니다

[0.9 공지](https://scikit-learn.sourceforge.net/0.9/whats_new.html#api-changes-summary)와 [새 옛-namespace 파일](https://raw.githubusercontent.com/scikit-learn/scikit-learn/3f1ea662ee1b1b08cee63cc31e4e3e36ec532208/scikits/learn/__init__.py)은 scikits.learn에서 sklearn으로 바뀌고 호환 wrapper가 유지됨을 보인다. 프로젝트를 별개 fork로 나누지 않고 0.9에 한정한 namespace 별칭을 기록한다.

같은 공지에는 fit 인자와 gamma 기본값 등 다른 API 변화도 있다. 따라서 P1의 top-level import 정적 근거로 모든 옛 모델의 계산 보존을 인정하지 않는다. P2에는 구체 estimator·데이터·인자·예외를 먼저 지정해야 한다. SciPy sampled-data 입력은 이 대조에 그대로 적용되지 않는다. 0.11의 별칭 제거는 이 문서의 예고이며 이번 packet에서 실제 제거 구현까지 확인한 종료판은 아니다.

### C02: 옛 도메인의 오늘 페이지가 옛 발행자의 말은 아니다

[현재 pythonware.com 페이지](https://www.pythonware.com/products/pil/)의 footer는 이곳이 과거 PythonWare의 홈페이지였고 현재 자료가 새로 작성되었다고 밝힌다. 따라서 현재 본문을 Fredrik Lundh의 원 발언이나 이관 동의로 쓰지 않는다. 이 페이지의 2011 마지막 출시 표기도 공식 Pillow 설명과 [고정 README의 귀속된 PIL1.1.7 원문](https://raw.githubusercontent.com/python-pillow/Pillow/baea361b9a29e9a1dfa5a9b8e11bc9624a9cee46/README.rst)의 2009-11-15와 충돌한다. 후자는 downstream이 보존한 귀속 복사본이라는 출처 한계도 남긴다.

[Alex Clark의 2010 fork 공지](https://mail.python.org/pipermail/image-sig/2010-July/006423.html)와 [원 저자의 답변](https://mail.python.org/pipermail/image-sig/2010-August/006429.html)을 직접 읽었다. 두 당사자가 fork를 인식한 근거는 있지만 동일 제품의 단순 rename이나 전면 이관 동의를 선언한 것으로 읽지는 않는다. [공식 About](https://pillow.readthedocs.io/en/stable/about.html)의 fork 계보, [PyPI 조정 댓글](https://api.github.com/repos/python-pillow/Pillow/issues/1535/comments?per_page=100)의 2020 소유권 변경은 서로 다른 시점·단위다. PIL 배포물과 Pillow 배포물은 별도 ID 사이의 fork/후속④로 연결한다.

[원래 설치 보고](https://mail.python.org/pipermail/image-sig/2010-August/006480.html)는 같은 PIL1.1.7도 easy_install과 setup.py 설치에 따라 import 형태가 달랐다고 보고한다. 본 리뷰는 이 import 보고 절을 읽었으며 그 페이지의 모든 시험 결과를 재검증했다고 주장하지 않는다. [공식 porting 문서](https://pillow.readthedocs.io/en/stable/porting.html)는 import 수정, plugin 자동 탐색, core extension 누락 오류, Python2 지원 종료 같은 경계를 제시한다. P1/P2의 무조건 교체 적합성은 성립하지 않는다. 정확한 Pillow판, Python판, 설치 방식, 동일 이미지와 plugin/core 오류 입력을 확보하면 보류를 좁힐 수 있다.

## 비교·재개에 필요한 최소 조건

- 자연 4건과 대조 2건을 모두 판독했다. 실제 실행 분자는 0이다. 정적 근거로 확인한 관계와 실행되지 않은 행동 적합성을 같은 성공 분자로 합치지 않는다.
- G01은 logical driver, 배포물 구성요소, 보관 소스의 단위를 맞춘 뒤 비교한다. G02는 후속이 없으므로 새 ID 또는 관계를 만들어 채우지 않는다.
- O01은 기본값과 scale 역변환, O02는 fully-qualified pair와 판을 반드시 비교키에 넣는다. 하나의 이름 캠페인을 네 독립 자연 사건으로 늘리지 않는다.
- C01의 namespace 관계와 C02의 배포물 fork 관계는 기능 시험의 성공을 대신하지 않는다. C02의 원 도메인 생존 역시 원 발행자 자격을 대신하지 않는다.
- 첫 판정과 이 재판독을 고정한 뒤에만 범위별 비교를 한다. ③의 조건부 제안은 실제 혼합 레코드 또는 관측된 오류의 분자에 넣지 않는다.

가장 작은 후속 실행은 양판이 설치된 격리 환경에서 각 기능에 맞는 동일 입력을 저장하고, 정상·경계·오류·dtype/metadata를 별개 행으로 남기는 것이다. 이 리뷰는 실행을 하지 않았으므로 설치·실행 종료값을 꾸미지 않는다. 입력과 예상 구별점은 `blind-review.json`의 각 P1/P2 및 reopen 항목에 있다. 연구 전체의 실행 명령과 수용 여부는 부모 연구자가 최종 HANDOFF에서 통합해야 한다.
