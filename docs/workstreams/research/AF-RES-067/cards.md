# AF-RES-067 — 사실 문장 카드 (후보; 8개 사건 확정 아님)

**Debian 업로드 원저자 관점:** “Debian FTP Masters는 2024-02-29 jq 1.7.1-3의 source upload 수락 기록에서 `jq_1.7.1-3_amd64.buildinfo`의 SHA256을 게시했다.” [원위치](https://tracker.debian.org/news/1508449/accepted-jq-171-3-source-into-unstable/) lines 13–40. **이 문장에** 'jq amd64 .deb는 이 시도에서 만들어졌다'나 '설치된 도구를 모두 호출했다'를 붙이지 않는다. 첫 추가 확인은 같은 빌드의 buildd attempt ID, 실제 signed binary .changes 및 .deb digest.

**빌드 감사자:** `.buildinfo`의 `Installed-Build-Depends`는 설치되어 빌드에 영향을 줄 수 있는 패키지 목록이다. 도구 사용 여부를 묻는다면 동일 run 명령/파일-access 기록이 필요하다. [정의](https://manpages.debian.org/testing/dpkg-dev/deb-buildinfo.5.en.html).

**보정 과학자:** “CRDS_CTX는 보정 참조 선택용 pmap 라벨이며 R_FLAT은 flat 참조 파일명이다.” 두 키의 공식 정의는 [CRDS_CTX](https://archive.stsci.edu/jwst/keyword/build9.3/meta_ref_file_crds_context_used.html), [R_FLAT](https://archive.stsci.edu/jwst/keyword/build8.0/meta_ref_file_flat_name.html). 이번 4개 선정 cal FITS의 **실제 헤더는 미확인**이므로 어떤 파일을 처리했다고 말하지 않는다. 첫 추가 확인은 각 제품 URI/재처리 이력/원헤더/보정 단계/해시.

**과거 결과 인용 사용자:** source version이나 observation name은 run 키가 아니다. 보존된 같은 산출물의 SHA256 또는 FITS 데이터 무결성 필드만으로는 당시 다른 입력을 실제 읽었는지 결론 내릴 수 없다. 동일 run에서의 읽기 지문과 산출 지문까지 묶어야 한다. 제품 재처리 이후 링크가 동일해도 바이트와 해석이 달라질 수 있으므로 게시 시점의 고정 원본/해시가 첫 확인이다. 현재 8자리 자료 없음.
