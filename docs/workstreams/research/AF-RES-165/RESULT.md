# AF-RES-165 — 기능 원문 링크와 파일별 배포 근거

## 표 1 — 요청 목적·파일 경로·판 / 상류 원문·고지 URL / 하류 안건·이견 URL / 배포물에서 확인한 파일·판 / 미확인

| 요청 목적·파일 경로·판 | 상류 원문·고지 URL | 하류 안건·이견 URL | 배포물에서 확인한 파일·판 | 미확인 |
|---|---|---|---|---|
| D1 시험 글꼴, OTS 8.1.0→8.1.1 | 원 test font의 개별 조건 미확인 | [S01 #976260](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=976260), 고지/소스/예약명, +dfsg 보고 | [S24 8.1.3+dfsg-1 tests](https://sources.debian.org/src/opentype-sanitizer/8.1.3%2Bdfsg-1/tests) 글꼴 없음 | 원 보고판과 후속판 불일치, 정확한 제외 경로·바이너리 |
| D2 HTML 슬라이드, 6.0.0-2 examples/_assets/SourceSansPro.woff2 및 themes/*/css/theme.css | [S53 소개](https://github.com/ionelmc/python-darkslide); 원 글꼴 고지 미확인; [S52 하류 copyright](https://metadata.ftp-master.debian.org/changelogs//main/p/python-darkslide/python-darkslide_6.0.0-2_copyright) Apache만 | [S02 #998076](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=998076), SourceSansPro 조건 미상, Alegreya Sans 별도 OFL 지적 | [S25 all filelist](https://packages.debian.org/trixie/all/darkslide/filelist) WOFF2와 CSS 및 landscape.jpg 존재, [S26 판](https://packages.debian.org/trixie/darkslide) | CSS 내부 실제 데이터, 원저자 조건, 담당자 처분 |
| D3 JPEG 검사 원리 또는 test/jpeginfo_test{1,2,3}.jpg, v1.7.1 | [S09 test README](https://github.com/tjko/jpeginfo/blob/v1.7.1/test/README) NC-SA; [S10 program COPYRIGHT](https://github.com/tjko/jpeginfo/blob/v1.7.1/COPYRIGHT) GPL | [S03 #1064380](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1064380), NC 지적 후 repack 및 업로드 | [S27 source](https://sources.debian.org/src/jpeginfo/1.7.1%2Bdfsg-1/test) README/test.py만; [S28 amd64](https://packages.debian.org/trixie/amd64/jpeginfo/filelist) jpg 없음, [S29 판](https://packages.debian.org/trixie/jpeginfo) | 직접 tar 바이트·AI 생성 자료의 독립 권리 확인 |
| D4 CAD 원/수정 Y14.5 글꼴, 1.0.0→1.0.2 | [S11 font license](https://github.com/FreeCAD/FreeCAD/blob/1.0.0/src/Mod/TechDraw/Gui/Resources/fonts/Y14.5Font.license), [S12 동일 고지 1.0.2](https://github.com/FreeCAD/FreeCAD/blob/1.0.2/src/Mod/TechDraw/Gui/Resources/fonts/Y14.5Font.license) | [S13 upstream issue](https://github.com/FreeCAD/FreeCAD/issues/18622); [S04 BTS](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1091771) 저자 CC0 이후 제외 항목 삭제 | S04 changelog 1.0.2+dfsg-1에서 Files-Excluded 항목 제거 | 실제 포함/파일 동일성; 운영 폰트로 모집 경계 |
| F1 이미지 표시 예제, release-3.2.4 examples/showimage.c, showanim.c | [S15 showimage](https://github.com/libsdl-org/SDL_image/blob/release-3.2.4/examples/showimage.c), [S16 showanim](https://github.com/libsdl-org/SDL_image/blob/release-3.2.4/examples/showanim.c), [S17 LICENSE](https://github.com/libsdl-org/SDL_image/blob/release-3.2.4/LICENSE.txt) 일치 | [S05 #2338412](https://bugzilla.redhat.com/show_bug.cgi?id=2338412) debugsource 분류 및 IMG_gif.c 별도 조건 | 리뷰에 적힌 debugsource 목록(보고) | 정확 Koji NVR·실제 RPM, 다른 이미지 자산 |
| F2 텍스트/폰트 예제, release-3.2.2 docs/hello.c 및 examples/editbox.c/.h | [S18 editbox.c](https://github.com/libsdl-org/SDL_ttf/blob/release-3.2.2/examples/editbox.c), [S19 hello.c](https://github.com/libsdl-org/SDL_ttf/blob/release-3.2.2/docs/hello.c) 별도 짧은 고지 | [S06 #2352900](https://bugzilla.redhat.com/show_bug.cgi?id=2352900) 예제 미포장 발언 | [S30 main](https://packages.fedoraproject.org/pkgs/SDL3_ttf/SDL3_ttf/fedora-43.html), [S31 devel](https://packages.fedoraproject.org/pkgs/SDL3_ttf/SDL3_ttf-devel/fedora-43.html) 3.2.2-2.fc43, 원 예제 경로 없음·installed-tests 실행 파일 존재 | fc42 심사판 및 debugsource, tiny_ttf 원권리 |
| F3 이미지 샘플 bench.png/62AHB.jpg/.jxl 및 test/images, 1.3.2→a8cb191 | [S20 원저자 답변](https://github.com/Isotr0py/pillow-jpegxl-plugin/issues/97), [S21 고정 README](https://github.com/Isotr0py/pillow-jpegxl-plugin/blob/a8cb191/test/images/README.md) | [S07 #2354261](https://bugzilla.redhat.com/show_bug.cgi?id=2354261), 고지 반영 발언; [S22 PR](https://github.com/Isotr0py/pillow-jpegxl-plugin/pull/98) | 심사 종료 및 업데이트 보고, 실제 목록 없음 | 원 게시자의 권한, 모든 sample 파일별 출전, SRPM/RPM |
| F4 QR 시험 사진 tests/data/errors/should-not-panic-1.jpg, -2.jpg; 0.9.0→0.9.1 | [S23 Cargo.toml](https://github.com/WanzenBug/rqrr/blob/v0.9.1/Cargo.toml) include 범위·코드 조건; 사진 허가 미확인 | [S08 #2350889](https://bugzilla.redhat.com/show_bug.cgi?id=2350889), lookaside 전 제외·새 판 보고 | crate include 규칙에서 tests/data 경로 빠짐, 실제 archive 목록 없음 | PR/원 crate/RPM 파일 목록, 제3자 화면 권리 |

**단위·분모:** 보충/목적층 사건 8개(하류 보고 8개 직접 읽음, 파일·범위 단위 16행); 자연층 예정 20자리, 원순위 복원 0, 결측 20. 자연층 확장 여부는 판단 불가. 독립 공개 source/binary 목록이 있는 사건 4(D1,D2,D3,F2); 정확 같은 심사판에 연결되는 것은 D2,D3 2개, 나머지 6개는 완전한 같은 판 목록 연결 미확인. D2는 source 목록 미확인, D3만 source 및 binary의 지정 경로 모두 확인. 넓은 사례로 시험 파일/운영 폰트도 포함되어 엄격 모집 하한 8건 달성이라고 하지 않는다. [assets.csv](assets.csv), [frame.csv](frame.csv), [sources.jsonl](sources.jsonl).

## 표 2 — 사건·원래 결정 / 다른 이유 또는 반례 / 후속 고지·교체·실제 포함 근거 / 바뀐 범위 / 판정

| 사건·원래 결정 | 다른 이유 또는 반례 | 후속 고지·교체·실제 포함 근거 | 바뀐 범위 | 판정 |
|---|---|---|---|---|
| D1 [S01](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=976260) 테스트 폰트 제거 권고 | #10/#17 별도 meson 누락/수정; 소스 부재와 예약명 | #29 +dfsg 업로드, #34 sponsor 의사, [S24 후속 폴더](https://sources.debian.org/src/opentype-sanitizer/8.1.3%2Bdfsg-1/tests) | 소스 묶음 | 후속판 보강, 원판 완결 아님 |
| D2 [S02](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=998076) 고지 누락 신고 | 보고자는 크기 절감도 희망(실제 제거 미관측), 렌더링 차이 | [S52 Apache만](https://metadata.ftp-master.debian.org/changelogs//main/p/python-darkslide/python-darkslide_6.0.0-2_copyright), [S25 파일 여전히 존재](https://packages.debian.org/trixie/all/darkslide/filelist) | 실제 포함과 고지 범위 상충 | 처분 미확인; 포함을 허용으로 승격 금지 |
| D3 [S03](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1064380) NC 이미지 제거 요구 | 프로그램 GPL과 다름 | [S09](https://github.com/tjko/jpeginfo/blob/v1.7.1/test/README), #15/#25 repack·업로드, [S27](https://sources.debian.org/src/jpeginfo/1.7.1%2Bdfsg-1/test), [S28](https://packages.debian.org/trixie/amd64/jpeginfo/filelist) | 소스 및 설치본 지정 파일 제외 | 가장 강한 연결, 다른 조직의 재사용 금지라는 결론 아님 |
| D4 [S04](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1091771) 수정 허가 미확인·제외 | [S13](https://github.com/FreeCAD/FreeCAD/issues/18622) 특정 프로젝트 허가와 모든 사용자 허가 구별 | 원저자 2025-08-19 CC0; 1.0.2+dfsg-1 changelog | 제외 목록 항목 제거; 원 저작과 수정 글꼴 구별 | 결정 역전, 실제 파일 교체·포함은 미확인 |
| F1 [S05](https://bugzilla.redhat.com/show_bug.cgi?id=2338412) 라이선스 분류 질의 | [S15](https://github.com/libsdl-org/SDL_image/blob/release-3.2.4/examples/showimage.c)·[S17](https://github.com/libsdl-org/SDL_image/blob/release-3.2.4/LICENSE.txt) 동일, 다른 디코더 예외 | 댓글 36–39 수정·설명 | 동일 notice 대상 두 예제에는 요약 가능 | 일반 고지 충분의 좁은 대조 |
| F2 [S06](https://bugzilla.redhat.com/show_bug.cgi?id=2352900) 예제 고지 분리 | 미포장 결정 ≠ 권리 금지; [S19](https://github.com/libsdl-org/SDL_ttf/blob/release-3.2.2/docs/hello.c) tiny_ttf 별도 | [S31 후속판](https://packages.fedoraproject.org/pkgs/SDL3_ttf/SDL3_ttf-devel/fedora-43.html) 설치 테스트 실행물 | 바이너리 vs source 범위 | 같은 버전·모든 subpackage 확인 전 보류 |
| F3 [S07](https://bugzilla.redhat.com/show_bug.cgi?id=2354261) 이미지 출처 질의 | 자가 촬영과 외부 이미지 서로 다름 | [S20](https://github.com/Isotr0py/pillow-jpegxl-plugin/issues/97)·[S21](https://github.com/Isotr0py/pillow-jpegxl-plugin/blob/a8cb191/test/images/README.md)·[S22](https://github.com/Isotr0py/pillow-jpegxl-plugin/pull/98), 반영 보고 | 고지 추가, 이미지 교체 증거 없음 | 저자의 진술 범위만 강화 |
| F4 [S08](https://bugzilla.redhat.com/show_bug.cgi?id=2350889) 사진 제거 요구 | unused criterion, duplicate LICENSE, 후속 Copr failure는 별개 | [S23 manifest](https://github.com/WanzenBug/rqrr/blob/v0.9.1/Cargo.toml) | crate publish 범위 변경, 사진 자체 권리 그대로 미상 | 원저장소/실제 crate/하류 rpm 대조 필요 |

**단위·분모:** 사건별 처리 비교 8/8 직접 보고 판독; 별도 사유 실제 확인 D1,F4(각각 빌드·중복/빌드 지적), D2 크기 제안 1(제거 미관측). 실제 파일 교체 이후 판정 변화 완결 사례 미확인 8/8; 고지/권리 표명에 따른 후속 결정 2(D4,F3), 묶음 범위 변경 F4. 순수 크기/빌드/중복으로 실제 파일 제외가 확인된 대조 사건 0개 확보, 모집 표본의 발생률 아님. [decisions.csv](decisions.csv), [COUNTEREXAMPLES.md](COUNTEREXAMPLES.md).

## 표 3 — 원리를 읽거나 파일을 반출하려는 요구 / A·B·C로 확인한 범위 / 실제 반환 링크·짧은 문장 / 확인할 배포 조건 / 보류 근거

| 요구 | A·B·C로 확인한 범위 | 실제 반환 링크·짧은 문장 | 확인할 배포 조건 | 보류 근거 |
|---|---|---|---|---|
| R01 JPEG 검사 원리 | A 설명; B 프로그램 고지; C 목록은 원리 질문에 불필요 | [S29](https://packages.debian.org/trixie/jpeginfo) 작동 원리 참고. 사진 복제 승인 아님. | 코드 실제 복제 시 별도 | 읽기만 전제 |
| R02 시험 사진 복사 | A 도구; B NC-SA; C 같은 판 지정 파일 제외 | [S09](https://github.com/tjko/jpeginfo/blob/v1.7.1/test/README)·[S27](https://sources.debian.org/src/jpeginfo/1.7.1%2Bdfsg-1/test) Debian 소스 test 폴더에 해당 jpg 없음. | 이용 목적·표시·공유조건·원권리 | GPL이나 Debian 제외로 우리 법적 결론 금지 |
| R03 HTML 단독 출력 | A [S53](https://github.com/ionelmc/python-darkslide); B 미확인; C [S25](https://packages.debian.org/trixie/all/darkslide/filelist) 실제 WOFF2 존재 | [S26](https://packages.debian.org/trixie/darkslide)·[S02](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=998076) 원리 참고, --embed 출력은 별도 확인. | CSS 내장 폰트 및 출력 | 원 폰트 출전 미확인 |
| R04 CAD 폰트 | A 기능 이슈; B 구 고지; C 제외 항목 삭제 | [S11](https://github.com/FreeCAD/FreeCAD/blob/1.0.0/src/Mod/TechDraw/Gui/Resources/fonts/Y14.5Font.license)·[S04](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1091771) 원저자 후속 권리 표명 확인. | 원/수정판·실제 tar/RPM 경로 | 최종 포함 미확인 |
| R05 이미지 표시 코드 | A 예제; B 같은 notice; C 심사 보고만 | [S15](https://github.com/libsdl-org/SDL_image/blob/release-3.2.4/examples/showimage.c)·[S17](https://github.com/libsdl-org/SDL_image/blob/release-3.2.4/LICENSE.txt) 해당 코드와 조건을 참고. | 출처·변경·고지, 이미지 데이터 별도 | RPM 포함은 미확인 |
| R06 텍스트 예제와 글꼴 | A 코드; B 별도 허가 문단; C 미포장 발언 및 후속판 | [S19](https://github.com/libsdl-org/SDL_ttf/blob/release-3.2.2/docs/hello.c)·[S06](https://bugzilla.redhat.com/show_bug.cgi?id=2352900) 내장 데이터와 코드는 별개. | tiny_ttf 원권리, debugsource | 자료 미상 |
| R07 샘플 이미지 변환/복제 | A 프로젝트; B 자가 사진/외부 데이터 분리; C update 보고 | [S21](https://github.com/Isotr0py/pillow-jpegxl-plugin/blob/a8cb191/test/images/README.md)·[S07](https://bugzilla.redhat.com/show_bug.cgi?id=2354261) 표기된 조건만 확인. | 변환·출전·CC 조건·원 게시자 권한 | 각 sample과 실제 패키지 미확인 |
| R08 QR 사진 | A 기능; B include; C 제외 요구 | [S08](https://bugzilla.redhat.com/show_bug.cgi?id=2350889)·[S23](https://github.com/WanzenBug/rqrr/blob/v0.9.1/Cargo.toml) 권리 미상 파일 반출 보류. | 원 사진·웹페이지 권리 및 archive | manifest는 실제 배포 목록 아님 |
| R09 박물관 이미지 | A 작품; B 공개 표시; C 정책 | [S32](https://www.metmuseum.org/art/collection/search/335537)·[S34](https://www.metmuseum.org/hubs/open-access) 해당 이미지 표시와 basic data 범위를 구별. | 특정 이미지/오디오, 정책 범위 | 정정 이력 미확인 |
| R10 악보·녹음 | A 작품; B 판·녹음 ID; C 기관의 표시 | [S36](https://imslp.org/wiki/Cello_Suite_No.1_in_G_major,_BWV_1007_(Bach,_Johann_Sebastian)) #483287과 #310845 조건 다름. | 판/녹음/관할 | 파일 실물·정정판 미확인 |

**단위·분모:** 구성한 반환 문장 10/10, 실제 제품 사용자 테스트 0/10, 실사용 효과 미확인 10/10. A 링크 충분 사례 R01/R03은 읽기 목적에서만 제안; 독립 평가 없음. [advice.csv](advice.csv).

## Q1–Q7 답과 근거 (PARTIAL)

**Q1 단위.** 원리 읽기, 특정 코드 복사, 독립 자산 및 생성물로 갈린다. D3 program/test images, F2 예제/tiny_ttf, D2 --embed output이 최소 구분을 지지한다. 경로가 없는 D1 글꼴은 파일별 확정 제외 대상이 아니라 묶음 보고다. generated output 권리 자체를 관측하지 못했으므로 입력 자산의 배포 여부를 다시 확인하라는 수준.

**Q2 출전과 조건.** 원 파일 머리말, 별도 README, 하류 copyright, upstream author 응답을 다른 타입으로 둔다. S09–10은 같은 판에서 서로 다른 조건, S15–17은 같은 notice, S18–19는 별도 짧은 고지, S11–12는 태그 두 개에서 동일한 구 notice가 후속 CC0를 설명하지 못하는 사례. S52는 Files:*가 Apache라 해도 reporter가 문제를 제기한 글꼴 자체를 자동으로 덮지 못함을 보여 준다. 이 결과는 출처가 확인된 조건의 기록이지 권리의 독립 보증이 아니다.

**Q3 주체와 이유.** D3 sponsor와 uploader가 실제 repack/업로드를 보고. D4 저자의 CC0와 Debian의 exclusion 변경, F3 원저자 notice와 packager 업데이트는 사건·역할·시점 분리. D2 reporter뿐인 상태에서는 처분 unknown. D1 build dependency 수정과 F4 dev-dep/중복/실패는 권리 이슈와 독립. 실제 크기/중복만으로 제외된 대조는 미확인.

**Q4 최종 배포.** 가장 명확한 D3는 v1.7.1 notice, +dfsg-1 source tree의 test 경로와 amd64 binary filelist를 연결. D2 같은 판의 실제 WOFF2 존재는 강하지만 원 글꼴 및 CSS payload 미상. D1과 F2는 후속판 확인이므로 정확 심사판을 대신하지 못함. F4 include 선언은 crate 실제 파일 목록이 아니다. F3, D4도 최종 binary 보류. 전체 아카이브 직접 추출/제품 실행 미실시.

**Q5 A/B/C.** A만으로 읽기 탐색 시작 가능(제품 기능 설명). B에서 원 코드/자산이 분리되고 C는 배포자의 조건 적용 범위를 설명한다. SDL_image 같은 notice 두 코드에는 B를 확인한 뒤 루트 링크로 단순화 가능. jpeginfo는 A/GPL만으로 이미지 반출 답을 만들 수 없음. FreeCAD/pillow-jxl은 표명 또는 고지가 바뀌어 후속 판단이 바뀌었으나 파일 교체 뒤 판정 역전이라는 더 강한 목표는 미달.

**Q6 외부 분야.** Met의 [S32 Wheat Field](https://www.metmuseum.org/art/collection/search/335537) (64.125.3) 및 [S33 Self-Portrait](https://www.metmuseum.org/art/collection/search/436532) (67.187.70a)는 개별 공개 이미지 표시, 후자의 audio는 동일 표시 미확인. [S34 OA policy](https://www.metmuseum.org/hubs/open-access)는 basic data와 public-domain 이미지의 범위 명시. IMSLP [S35 Beethoven](https://imslp.org/wiki/Piano_Sonata_No.6_(Beethoven)) #00006 Schenker PD와 #585387 Bradley-Fulgoni CC-BY-NC-ND4.0, #707185 Jank non-PD US; [S36 Bach](https://imslp.org/wiki/Cello_Suite_No.1_in_G_major,_BWV_1007_(Bach,_Johann_Sebastian)) #483287 manuscript PD와 #310845 Carr CC-BY-NC-ND3.0, #517651 Fournier non-PD US. 실제 표시 주체는 기관/기여자의 기록이며 원저작·촬영·편집·녹음·관할이 다르다. 2+2 개별 자료 표시는 읽었지만 정정 전후 원판, 파일 자체 및 추가 기관 대조 미확인. 정책을 소프트웨어의 라이선스 승인으로 이식하지 않음.

**Q7 반환 문장.** 표 3, advice.csv. 세 문장 유형: “작동 원리 참고(기능 링크)”, “이 배포판/파일 목록에 해당 경로 포함 또는 없음(버전·아키텍처)”, “우리 배포 방식에서 원권리·변경·고지·출력 확인(보류 이유)”. 제외는 하류 처리 사실이고 불법 판정이 아니다. 권리 미상은 검색 링크를 삭제해야 한다는 의미도 아니다.

## 대안 및 조합 조건

- A 가벼운 링크: 원리 탐색 비용 낮음, 파일 복사 답을 요구할 경우 B로 전환. 같은 notice인지 확인되지 않으면 프로젝트 단위의 권리 답 금지.
- B 파일별 출전과 조건: 동일 파일/고지 계보에는 요약 가능, 정확판·파일·의존 자산을 잃으면 다시 분리. 고지와 실제 행위가 다르면 C로 이동.
- C 하류 판정 및 파일 목록: 한 배포자의 실제 선택·운영 조건을 좁게 전달. 정책/버전/관할이 다르면 다른 결과를 가져올 수 있어 B와 결합하되 승인 엔진으로 만들지 않음.
- 증거의 최소 결합 단위 후보는 목적, 대상 경로/판, 원 고지 적용범위, 배포자/판정/실제 목록, 미확인 및 필요한 다음 자료. 데이터베이스 최종 설계는 정하지 않음.

## 자료 충족과 완료 상태

PARTIAL. 원장 54행, 직접 42(중복·보조·진입점 포함), 차단 12. 보수적으로 별도 산입한 고유 계보 22개(하류 8, 엄격 상류 5, 배포 목록 5, 박물관 2, 악보 2); 추가 상류 범위 결정 1은 사진 권리 표시가 아니므로 제외. 22 총수 자체는 맞으나 상류 하한 6에 1 부족; 배포 목록 5 중 다른 판 후속 관측 2, 정확 연결 수와 독립 문서 수를 혼동하지 않음. 하류 8은 보충층 넓은 사건 수(미해결/경계 포함); 자연 적격 8건을 보장하지 않음. 원목록 창 2개 모두 미확보, 실제 파일 교체 반례와 크기/중복 등 비권리 제거 확증 없음. 다른 분야의 역사적 정정 사례도 미확인. 차단된 파일은 후속 정적 비교 입력으로 남김. [SCOPE](SCOPE.md) · [SCOPE_DELTA](SCOPE_DELTA.md) · [COUNTEREXAMPLES](COUNTEREXAMPLES.md) · [SELF_CHECK](SELF_CHECK.md).

| 불일치·약점 | 영향을 받는 판단 | 다음 조사와 자료 | 결론을 뒤집을 관측 |
|---|---|---|---|
| 모집 원순위 0/20, 두 검색창 미복원 | 대표성 및 적격 사례 수 | BTS/UDD 및 Bugzilla/HyperKitty 원목록 | 2018–2025 최초 보고순 10+10 고정과 모든 후보 심사 |
| 실제 파일 교체·최종 포함 연결 부족, 상류 권리 5/6 | 파일 복사·조건 변화 안내 | D4 exact source/binary, F3 SRPM, F4 .crate 0.9.0/0.9.1, 원 폰트 및 이미지 고지 | 동일 경로의 교체 전후 해시·고지·실제 목록과 결정자가 연결되는 기록 |
| 다른 분야 정정 이력과 비권리 제외 대조 미확인 | 외부 원리 이전 범위 및 배제 이유 | 박물관/악보 권리 정정 원판, 크기·빌드·중복만을 이유로 제거한 패키징 원자료 | 정정 전후 동일 자산/판 기록 및 다른 사유만으로 실제 제거된 파일 목록 |
