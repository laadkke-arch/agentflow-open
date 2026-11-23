# Matplotlib 1단계: 이전 판과 일반층 확정

공식 3.6.3 발행의 gallery HTML 경로를 정렬하고 앞 40개 적격 예제를 고정했다. 총 47개 prefix 경로 중 인덱스·시간 집계 4개, 098 주 예제 2개, 그림 없는 frame_grabbing_sgskip 1개를 제외했다. JS data URL 애니메이션 12개는 설명용 그림이 실제 연결되므로 적격에 포함했다. 외부 파일 경로가 없다는 이유로 삭제층으로 분류하지 않는다.

일반층은 page.html#fragment를 포함한 site-relative 경로와 프로젝트 문자열 Matplotlib을 SHA-256 규칙에 넣은 첫 두 행이다. `MP-G1`은 ImageGrid 종횡비, `MP-G2`는 AxesDivider 색상 막대 예제다. 두 이전 본문·배포 Python 소스·PNG를 직접 읽고 PNG도 시각적으로 확인했다.

분류의 대응 소스는 본문의 Download Python 링크가 가리키는 정확한 `_downloads/<hash>/<name>.py`이다. 공식 release-tag 소스와 실제 문서 빌드의 버전 문자열이 다르므로 태그의 예제 파일을 배포 본문 소스로 대신하지 않는다. release source SHA와 공개 문서 버전 문자열의 source SHA는 각각 별도로 기록했다.

최신 live 3.6.3 index는 초기 발행 바이트와 다르며 처음 발행 커밋을 분석 기준으로 고정했다. 요청에 나온 matplotlib.github.io 저장소 API는 404였고 공식 matplotlib.github.com 발행 저장소를 확인했다. 현재 주소의 리다이렉트를 과거판으로 취급하지 않았다.

신판에서는 release/tag·발행 커밋 메타데이터만 읽었다. 신판 경로 목록·본문·그림·개별 CI 로그는 아직 열지 않았다. 원장 UTC와 지문은 receipts/, 단계 지문은 stage1.json에 있다. root의 1단계 커밋 확인 전에는 2단계에 들어가지 않는다.
