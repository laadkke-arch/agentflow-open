# 반례·결측·보정

## 원자료와 비교
- **일반 고지가 충분할 때:** SDL_image release-3.2.4 두 예제의 머리말과 루트 notice가 동일 (S15–17). 해당 두 파일에 한해 B 확인 후 A/root로 요약 링크 가능. F1 심사의 다른 IMG_gif.c 분류 문제는 전체 확대의 반례(S05). 루트 고지의 충분성을 모든 파일에 적용하면 안 됨.
- **같은 프로젝트 내 고지가 다를 때:** jpeginfo 프로그램 GPL 대 test 이미지 NC-SA(S09–10). D3의 실제 목록에서 사진이 보이지 않음(S27–29). 반대로 darkslide 6.0.0-2의 WOFF2 파일은 포함되고 copyright에는 Apache만 있음(S02,S25,S26,S52). 포함은 허가의 증명도, 누락은 곧 금지의 증명도 아님.
- **다른 처리 원인:** D1 #976260 Message #10/#17의 meson 빌드 의존성 문제 수정은 #22/#29의 글꼴 고지/소스 이슈와 별개(S01). F4의 criterion 개발 의존성 제거, 중복 LICENSE 경고, Copr 실패는 사진 제외와 다른 사유(S08). D2의 용량 절감 제안은 실제 제거 결과를 관측하지 못했으며 렌더링 차이가 경쟁 설명. F2는 예제 미포장 범위 설명이지 해당 코드 권리 부정이 아님(S06,S18,S19,S31). 순수 크기·빌드·중복만으로 파일 제외한 별개 실증 사건은 미확인; 이를 양성이라 세지 않음.
- **결정이 바뀐 범위:** FreeCAD는 원저자 권리 표명 이후 Files-Excluded 항목 삭제(S04,S11–14), pillow-jxl은 새 고지 PR 병합 및 packager 반영 보고(S07,S20–22). rqrr은 crate include 패턴 변경(S08,S23). 세 사례 모두 실제 파일 내용 교체 후 동일 판정이 뒤집혔음을 입증하지 못함. 원 권리 추가·문서 정정·묶음 범위 변경을 파일 교체로 부르지 않음.
- **다른 분야:** Met 두 개별 이미지에 공개 표시(S32–33), basic data 범위와 이미지 범위가 다른 OA 정책(S34), self portrait 페이지의 별도 오디오에는 동일 표시 미확인. IMSLP 두 작품에서 편집판/녹음/관할별 조건 다름(S35–36). 정정 전후 판·기관과 실제 파일 검사 미확인. Smithsonian 개별 원자료 접근 실패(S47). 박물관·악보의 권리표기 관찰을 소프트웨어 라이선스 결론으로 이전하지 않음.

## 자기 재판독 보정
이전 원판: sources fc3a47b1126cb437ccab3e1d48836bb9c38e178c, frame b3a5536ae71f0083c314687f4c9c64c9cd0d8814, assets cb992185789f676e2b66027e3c4273cfe8bd1926, decisions b2958d019edd6f1502018ecf4a433c551e4030ce. 후속 커밋 17a3310 / 053ca70 / 81e9e3f / bb81e75:
- S02 및 A02: SourceSansPro 조건 미확인, OFL 언급은 Alegreya에 한정. S52 실제 copyright 두 Apache stanza 확인. D2의 B를 더 보수적으로 낮춤.
- S03 최초 보고 2/21, 권리 지적 2/25, 재포장/업로드 2/26. Message #25 sponsor 업로드 확인. C03, frame 날짜 정정. S09 실제 파일명 jpeginfo_test1/2/3.jpg 정정. 원문 첫 줄 jpegoptim 표기는 불일치로 보존.
- S01 초기 8.1.0-1과 +dfsg.1-1, 이후 제목 8.1.1+dfsg.1-1 분리. 8.1.3+dfsg-1 목록은 후속 버전으로만 표시. 별도 빌드 오류/수정 근거 보강.
- S52–54 원장 추가: 고지와 A 프로젝트 소개 2개 직접 읽음, Fedora 정책 접근 실패 1개. 원장 51→54행, 직접 40→42, 실패 11→12. 산입 고유 계보 22 그대로(8+5+5+2+2); 엄격 고정 상류 5/6. 모집창 결측 20 그대로. 규칙·대상 확대 없음.
- 파일 교체를 겨냥한 추가 검색은 2015/2017 보고와 범위 밖 policy 및 2026 보고가 반환되어 적격 원문을 추가하지 못함. 양성 0이 아니라 목표 사례 미확인. 최초 날짜순 모집 불가를 가릴 목적층 추가 없음.

## 재개 시 정적 비교
먼저 자연 모집창 복구. Debian BTS/UDD 및 Fedora Bugzilla/API/HyperKitty archive에서 2018–2025 report creation date와 숫자 ID를 원본에 연결하고, 같은 메시지 복제는 이슈 ID로 중복 제거. 두 창 10건씩 고정하기 전 처리 결과 기반 선택 금지. 이어 정확한 버전의 archive와 파일 목록을 비교. 파일 경로, 실제 해시, manifest, 고지, 날짜를 각기 기록. 아래 예시는 실행되지 않았다.
- D3: `apt-get source jpeginfo=1.7.1+dfsg-1`, `apt download jpeginfo=1.7.1+dfsg-1`, `dpkg-deb -c jpeginfo_1.7.1+dfsg-1_amd64.deb`; upstream v1.7.1 git archive/test/README와 Debian orig tar에서 세 jpeginfo_test*.jpg 존재 확인. 기대: upstream notice에는 세 파일, Debian 공개 목록에는 없음.
- D2: `apt-get source python-darkslide=6.0.0-2`, `apt download darkslide=6.0.0-2`, `dpkg-deb -x darkslide_6.0.0-2_all.deb darkslide-extract`; paths A02,A03, copyright, CSS data URI base64 decode → fc-scan/name table + SHA256; upstream 동일 파일 및 폰트 원판 비교. 실행·제품 빌드 불필요.
- D1: snapshot.debian.org package opentype-sanitizer 8.1.0+dfsg.1-1 / 8.1.1+dfsg.1-1 / 8.1.3+dfsg-1 확인, 각 .dsc 및 orig tar 파일 목록과 debian/copyright의 Files-Excluded를 비교. 과거 mentors 제안판이 archive에 없으면 그 결측 유지.
- D4: snapshot.debian.org/package/freecad/1.0.2%2Bdfsg-1/ 및 1.0.0+dfsg-1 이전 archive; source orig와 해당 버전 모든 binary (특히 freecad-common) 목록에 Y14.5-2018.ttf, Y14.5-FreeCAD.ttf 검색. 패치 전후 실제 파일의 sha256 비교.
- F1/F2: Koji build NVR은 review의 SRPM 및 official build에서 확정한 후 `koji download-build --arch=src --arch=x86_64 --arch=noarch <NVR>`; `rpm -qpl <rpm>` 각 main/devel/debugsource/debug packages 확인. F2 3.2.2-1.fc42와 후속 3.2.2-2.fc43 비교, docs/hello.c, examples/editbox.c/.h, tiny_ttf 정의 및 라이선스 경로 확인. F1 review 2338412의 정확 NVR, examples/showanim.c/showimage.c.
- F3: review 2354261의 1.3.2-1.fc41 SRPM, Koji 실제 build NVR 확인, test/images README patch 및 bench.png, 62AHB.jpg, 62AHB.jxl, sample 목록 비교. 원 StackOverflow post의 파일 원본과 라이선스 이력 및 libjxl/testdata 정확 revision 확보.
- F4: `curl -fL https://static.crates.io/crates/rqrr/rqrr-0.9.0.crate -o rqrr-0.9.0.crate` (0.9.1 동일 형태), `tar -tf rqrr-0.9.0.crate` (0.9.1 비교), Fedora 0.9.1-1.fc42 src 및 devel RPM 목록에서 tests/data/errors/should-not-panic-{1,2}.jpg 검색. 기대: 새 manifest의 include 패턴으로 tests/data 제외; 실제 검증 전까지 추정.
