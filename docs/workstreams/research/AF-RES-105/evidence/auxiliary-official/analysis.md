# 보조 사건의 공식 동작과 반례

이 문서는 묶음② 원격 봉인 `4a4aae107be25f71318dbb0c7b7cfa73506c5030` 뒤에 작성했다. 작성자 인지·실행 진술과 연구자의 현재 환경 시험은 별도 증거다.

## QG-K1: 같은 수치와 같은 함수 이름의 한계

[QGIS 3.34 line_substring](https://github.com/qgis/QGIS/blob/ffbdd678812eec460ff02ff73bd36ee7955ac8a5/resources/function_help/json/line_substring)의 `start_distance`·`end_distance`는 시작점으로부터의 거리다. 예제 `(0,0)→(10,0), 2→6`은 `(2,0)→(6,0)` 부분 선을 반환한다. 따라서 기존 식의 0/1을0.5로 바꾼다는 첫 댓글은 자동으로 전체 선의 중간 점을 지정하지 않는다. LineString 출력과 Point 출력도 다르다.

[같은 판 line_interpolate_point](https://github.com/qgis/QGIS/blob/ffbdd678812eec460ff02ff73bd36ee7955ac8a5/resources/function_help/json/line_interpolate_point) 역시 거리 인수를 받는다. 0.5는 길이10 선에서 x=0.5이며 x=5가 아니다. 선 길이의 절반을 넣어야 해당 평면 선의 중간 지점을 얻는다. 다만 `length($geometry)`와 `$length`는 항상 같은 단위가 아니다. [length 도움말](https://github.com/qgis/QGIS/blob/ffbdd678812eec460ff02ff73bd36ee7955ac8a5/resources/function_help/json/length)은 geometry SRS의 평면 길이, [$length 도움말](https://github.com/qgis/QGIS/blob/ffbdd678812eec460ff02ff73bd36ee7955ac8a5/resources/function_help/json/%24length)은 프로젝트 타원체·거리 단위를 구분한다.

`probe-results.json`의 현재 QGIS3.40.6 시험에서는 길이10 직선에서 centroid와 길이 절반의 interpolate가 모두 `(5,0)`이었다. 꺾인 `(0,0)→(10,0)→(10,10)`에서는 centroid `(7.5,2.5)`와 interpolate `(10,0)`으로 갈라졌다. 다른 이름의 두 방법은 어떤 입력에서 효과가 겹치지만 일반적으로 동일하지 않다. EPSG:27700·타원체NONE 조건에서 expression 거리단위를km로 지정하면 `$length=0.01`, `length($geometry)=10`이었다. 이는 가능한 불일치이며 작성자의 `$length/0.002` 성공 보고의 원인을 확정한 것이 아니다.

[별도 답 그림](https://i.sstatic.net/26H5xTyM.png)은 Point/MultiPoint Geometry Generator와 세 점 라벨을 보여 준다. 화면의 Millimeters는 label placement distance에 붙어 있으므로 그것만으로 표현식의 길이 단위를 단정할 수 없다. 작성자의 [784443](https://gis.stackexchange.com/questions/480481#comment784443_480523)은 이 별도 답을 수정한 결과이고, 고정한 첫0.5 제안의 성공이 아니다. 반환할 한 질문은 **“현재 식을 라벨의 Geometry Generator에 적용했는지, 심볼의 Geometry Generator에 적용했는지 확인할 수 있나요?”**다. 답을 받으면 해당 적용 위치·단위 절로 안내할 수 있다. 현재 공개 글은 Geometry Generator라고만 하며 완전한 설정이 없다.

## QG-N1: 배웠다는 사실과 호환되는 실행은 별도

당시 받은 [원 링크](https://gdal.org/api/python_gotchas.html#certain-objects-contain-a-destroy-method-but-you-should-never-use-it)는 현재 직접 HTTP 조회에서404였다. 검색 도구의 이전 캐시 본문은 반환되었지만 그것을 현재 원 주소 접근 성공으로 세지 않았다. [현재 공식 주소](https://gdal.org/en/stable/api/python/python_gotchas.html#certain-objects-contain-a-destroy-method-but-you-should-never-use-it)와 [v3.8.4 고정 소스](https://github.com/OSGeo/gdal/blob/c2d2a61739ca770bae5a26be3eeb25a045dd3458/doc/source/api/python_gotchas.rst)의 해당 절은 직접 읽었다. v3.8.4는 [공식 배포 목록](https://gdal.org/en/stable/download_past.html)에2024-02-18로 표시되어3월 제안 시점 전에 제공되었다. 작성자의 설치판은 미확인이다.

그 절은 context manager 및 Close가 GDAL3.8부터임을 명시한다. 이전 판의 Destroy/참조해제와 현재 with/Close를 한 이름으로 묶으면 호환성을 놓친다. 현재 GDAL3.10.3에서 연구자가 만든 GeoPackage 한 점 `(3,4)`를 with 종료와 명시적 Close로 각각 저장하고 다시 열면 둘 다 feature1개와 같은 WKT를 얻었다. 파일 바이트는 다르다. 이 결과는 저장 내용의 제한된 겹침이며, 자원 수명 전체·오류 처리·모든 드라이버·작성자의 실행을 같다고 증명하지 않는다.

또한 v3.8.4 문서의 예제179–185행을 변경 없이 `ast.parse`하면 SetGeometry 줄의 닫는 괄호 누락으로 실패했다. 현재 공식 본문에도 같은 누락이 보인다. 자체 시험은 별도로 작성한 입력을 사용했다. 링크와 정확한 절은 필요하지만 그 예제의 무수정 실행 가능성까지 보장되지는 않는다. 작성자의 새 인지 진술은 **with 지원**에 한정하고, 그보다 앞선 OpenEx의 “works”를 합치지 않는다.

## BL-N1: 같은 링크도 그림·현재 파일·본문이 다르다

원 글의 제안 전 추가 파일 `vWxY64rZ`와 제안자 파일 `oDnRekJL`을 공개 Blend-Exchange API와 실제 다운로드 경로로 열었다. 조회 경로와 바이트 지문은 `../auxiliary-followup/acquisition.jsonl`, 구조는 `blend-inspection.json`, 압축 해제12byte 헤더는 `blend-headers.json`에 있다. 두 현재 파일의 헤더는 `BLENDER-v400`이다. `bpy.data.version=[4,0,36]`의 마지막 수는 패치 릴리스로 해석하지 않았다.

봉인한 제안 그림은 Compare Vector/Direction/Greater Than,90° 경계이고, 현재 다운로드 파일은 Direction/Not Equal,Angle0이다. 두 식은 같은 비교가 아니다. 원 답 본문은3.6.5로 저장했다고 하지만 현재 연결 파일의 형식은4.00이다. 현재 파일을 과거에 작성자가 받은 정확한 파일이라고 확정할 수 없다. 파일의 그래프에는51nodes, 원 작성자 파일에는21nodes가 있다. 파일 구조를 읽었으며 simulation 실행·성공을 주장하지 않는다.

이 불일치는 **알고 있는 이름을 빼는 규칙**뿐 아니라 **링크 하나면 충분하다는 규칙**의 반례다. Direction이라는 새 기능의 인지 진술은 유지되지만, 정확한 비교 연산·임계값·판과 원 입력을 따로 표시해야 한다.
