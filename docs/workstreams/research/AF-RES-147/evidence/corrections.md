# 01 · 배포 파일 접근 보정

범위 봉인 후, 출력 셀 판독 전에 네 공식 바이너리 진입점(IANA data 및 www, Unicode apex 및 www)을 HEAD로 조회했다. 이 실행 환경에서 모두 터널 403이었다. 웹의 IANA 리리스 색인과 Unicode Public 디렉터리는 직접 읽었다. 유지보수 CLDR 43.1/44.1은 공식 목록의 Data 칸이 n/a이고 정식 Git 태그를 배포 주소로 제공한다. 네 IANA 발표는 리리스에 대응하는 Git 커밋을 직접 명시한다. 두 계열 모두 공급자가 공개한 정확 커밋의 원본 Git 트리 아카이브를 읽는 동일 대체 경로를 쓴다. 원래의 tar/ZIP 주소, 서명/체크섬 경로와 접근 실패는 남긴다.

정확 커밋의 원본 규칙과 XML은 판독·재생 기준으로 유효하다. 생성된 GitHub 아카이브와 배포 tar/ZIP의 바이트 동일성, 서명 및 소비자 배포 전처리 동일성은 미확인으로 둔다. 계열·판·셀·보존조건·실패·분모의 봉인 규칙은 유지된다. [IANA 정식 주소](https://www.iana.org/time-zones/releases) · [CLDR 태그 및 ZIP 배포](https://cldr.unicode.org/index/downloads#download)
