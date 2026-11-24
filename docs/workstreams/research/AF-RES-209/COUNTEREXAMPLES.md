# 반례·대안 적용 조건·정정
## 서로 다른 보존 대상
|관점|필요한 불변량|가능한 조치|실패/비용과 반증|
|---|---|---|---|
|촬영자/뷰어|보기 방향만 맞음; 파일 바이트까지 보존하려면 읽기 시 변환|EXIF Orientation을 읽어 표시할 때만 변환 (M02, D03, D04, R01)|OpenCV IMREAD_UNCHANGED 및 IGNORE_ORIENTATION은 적용하지 않음. 태그만 바꾸면 무시하는 뷰어에서 여전히 옆으로 보임. 정상 1 또는 없는 태그에는 무조건 90° 적용하면 안 됨.|
|파일 배포자|저장 픽셀 좌표 자체가 정상, 모든 뷰어|DCT 블록 변환 가능한 JPEG: jpegtran -perfect, 이후 Orientation 정규화/제거 및 썸네일 검토 (M01–04 X01)|회전 후 기존 태그 6을 남기면 태그 존중 뷰어에서 두 번 회전. -copy all만으로 썸네일/Orientation 동기 보장 불가. -perfect 실패 시 사용자가 허용한 대안 선택.|
|코덱 작성자/보존 담당자|DCT 계수의 가역 대응 및 전체 표시 영역; 동일 바이트와 다름|jpegtran rearranges DCT coefficients; 90/270 조건이 샘플링/부분 iMCU에 의존 (M01 M03 M04)|홀수 크기/부분 iMCU: 기본은 비변환 영역 남김, trim은 경계 버림, perfect는 거절. transpose만으로 90° 대체 불가. jpegtran 재출력 바이트/메타데이터 전체 동일을 약속할 수 없음.|
|847 확대/붙이기|오른쪽 4px 보존, artifact 허용|정확한 이슈와 버전별 crop extension 동작 확인 (S03 R03 R04 R08 M01)|입력 92×32→200×32, 300×300과 16×16 블록 조합에서 경계 손실; 회전 예가 아님. 이전 3.1.0 구현/mozjpeg 문서에서 새 개발 브랜치 동작을 약속하지 않음. dev/3.2 실제 배포 버전 미확인.|
|메타데이터 편집자|tag 값만 의도대로; 타 태그 보존은 별도|ExifTool -Orientation#=6 또는 -n -Orientation=6; 출력 -n -Orientation 확인 (M02 M05 M06 M07 R05 R06)|bare =8이 180 텍스트 단축형으로 해석된 원제보. IFD 생성 시 mandatory tags 추가 가능. NoMandatory는 스펙 적합성과 충돌할 수 있으므로 자동 적용 금지. 태그 변경은 전체 파일 바이트 변경 가능.|
|다른 분야: 기관 이미지 열람|마스터를 재작성하지 않는 조회, 필요한 표시 파생본|IIIF rotation 매개변수와 info.json capability (I01–04)|회전 지원 제한(LOC 90° 배수), 압축/알고리즘/원본 관리 API 밖; 전체 해상도 JPEG도 마스터 동일 파일 증거 아님. 기관 정책과 권리, cache/네트워크 비용 고려.|
|픽셀 처리 사용자|완전한 좌표 변환, DCT 보존 요구 없음|Pillow ImageOps.exif_transpose; 필요 시 PNG/새 JPEG 저장 (D01 D02 D06)|저장 JPEG 재인코딩 가능, 계수 보존 아님. 메타데이터 동기/ICC/썸네일 별도. 저장용 코덱·품질 선택 필요.|
## 직접 발견한 반례 vs 추론
- 직접: S03 원문 오른쪽 4픽셀, R03/04/08 제작자 응답. X03 구버전/fork 설명의 일반 iMCU 단서로는 새 crop extension 해결 상태 알 수 없음. 따라서 B=악화(응답 순서 기준).
- 직접: S04 bare 8→Rotate 180 보고, R05 PrintConv 단축 설명, M06 정수 쓰기 경로. 숫자 자체가 충분하지 않으며 IFD0를 붙여도 첫 URL 같고 FAQ/CLI 접근 실패.
- 직접: D03 두 flag 값과 무시 규칙. X02 SPIFF IMGOR 0..3/IMGFLIP vs X01 EXIF 1..8: 774의 원본문은 어느 형식인지 명시하지 않음. 경쟁 설명이 SPIFF/명시 API rotation이면 B의 EXIF 문서 우위 주장은 폐기.
- 직접 읽은 회귀 시험 (D02 고정 12.0.0, L402–436): EXIF 없는 base, 2–8 방향 JPEG/WebP, 재호출이 동일 픽셀이어야 함. 코드 존재만 확인; 실행 결과가 아님. 정상 Orientation=1 입력과 태그/픽셀 이중 적용은 아래 설계 입력에 포함. 정상 태그=1에 90°를 적용하거나 tag6을 남긴 채 90° 픽셀 회전하는 실패는 규칙에 따른 기대 반례이며 직접 시험하지 않았다.
- X01 p39: 소비자가 main orientation 존중/thumbnail fallback 가능, 변환자가 thumbnail 일관성 유지. 썸네일만 회전하지 않았거나 본 이미지와 태그 불일치 시 보기 결과가 달라질 수 있음. 네 원제보의 필수 조건으로 끼워 넣지 않음.
## IIIF 실제 주소쌍 (문서 제공 그대로)
I03 Library of Congress docs L108–124의 동일 identifier, 동일 region/size/quality/format, rotation만 다름:
- https://tile.loc.gov/image-services/iiif/service:sgp:sgpbatches:batch_dlc_anacostia_ver01:data:sn84025948:0023728866A:1942081001:0202/full/full/0/default.jpg
- https://tile.loc.gov/image-services/iiif/service:sgp:sgpbatches:batch_dlc_anacostia_ver01:data:sn84025948:0023728866A:1942081001:0202/full/full/90/default.jpg
- https://tile.loc.gov/image-services/iiif/service:sgp:sgpbatches:batch_dlc_anacostia_ver01:data:sn84025948:0023728866A:1942081001:0202/info.json
I01 §1.1/2/4.6 L75–90,236–245: client-requested derivative, 순서 region→size→mirror then rotate→quality→format. 서버 원본 관리/압축 알고리즘은 명세 밖. 위 실제 문서 주소쌍을 판독했으나 바이너리 요청/해시/마스터 변경 관찰은 안 함.
I02 Art Institute docs L199–287 ID 2d484387-2509-5e8e-2c43-22f9981972eb, 843px width 캐시용 반환 및 크기 제한; 회전 지원을 추정하지 않음. I04 Rijks docs L24–42 RFwqO 같은 ID의 PNG/gray JPEG와 다른 ID ohGMs의 90° 예를 혼동하지 않음.
## 정정과 노출
- S03 원제보의 leftmost→rightmost 명시 정정: 현재 본문 rightmost 4px을 기준 삼음. 과거 표현으로 회귀하지 않음.
- D02 원장 이전 L402–422, tag 제거 일반 설명 → 동일 파일 고정 SHA를 재열어 L402–436 및 438–462 확인. absent-tag base와 반복 호출 픽셀 일치 assertion을 추가. 실행을 주장하지 않음.
- 날짜: SCOPE 동결 commit 실제 created_at 2026-11-24T21:29:00Z, 세션 시작 약 21:28Z. 검색 각각의 정확한 UTC는 도구에 없음. 첫 검색 이전 커밋은 확인.
- M01 main 최신 문서와 3.1.0 M03/M04, fork X03 구분. R08 dev/3.2 주장만 확인. 고정 배포 검증 전 지원 보장 금지.
- 원제보와 메커니즘 문서 사전 열람은 설계에 필요했으나 blind retrieval 평가가 아님. 결과 노출 후 질의 변경 없음. 
