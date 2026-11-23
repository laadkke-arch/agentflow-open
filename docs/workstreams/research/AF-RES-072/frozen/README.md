# 고정 본문과 재배포

`body/ID.gz`는 발행 기관이 공개한 Git 저장소의 정확한 응답 본문을 mtime 0으로 압축한 것이다. 내용 수정은 없으며 문서가 연결한 외부 리소스를 포함하거나 실행하지 않는다. [취득 manifest](manifest.jsonl)는 원주소·실시간 응답 지문·압축 지문·상태·UTC를, [corpus](../corpus.jsonl)는 원발행 주소·판·절·권리를 기록한다. 원격에 다시 방문하는 경우에도 Git 커밋이 포함된 같은 주소를 쓴다.

- A01–A08은 Apache Software Foundation의 원 xdoc이다. [Apache License 2.0](notices/Apache-2.0.txt)과 [각 프로젝트 NOTICE](notices/Apache-NOTICE.txt)를 동봉했다. 원문의 copyright·attribution 댓글은 파일에 남아 있다.
- W01–W06은 W3C CSV on the Web Working Group의 발행 스냅샷이다. 원 HTML에 W3C® (MIT, ERCIM, Keio, Beihang)의 2015 또는 2016 copyright, 상태, 정식 날짜판 링크가 있다. 외부 예시·그림 파일은 동봉하지 않았다. [저장소 라이선스 고지](notices/W3C-repository-license.md) · [공식 Document License](https://www.w3.org/copyright/document-license-2023/) · [2015 이전 판](https://www.w3.org/copyright/document-license-2015/)
- N01–N06은 U.S. NARA Digital Preservation Unit의 CC0 1.0 계획 원문이다. 링크된 제3자 콘텐츠와 다른 포맷 사본은 동봉하지 않았다. [NARA 원 고지](notices/NARA-CC0.md)

원본 취득 바이트와 압축 보관량은 실험 인프라의 별도 비용이다. L의 상주 검색 설정은 공개 주소 행만 포함하며 원문 보관본은 실험용 HTTPS 대역이다. I와 H는 같은 카드 파일을 쓴다.
