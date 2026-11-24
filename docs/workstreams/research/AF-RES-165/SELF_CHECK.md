# AF-RES-165 SELF_CHECK — 동일 작업자 자기검산

검산 대상 e1918c1d2ed988734b81d54112e81fb2bf847d3f. GitHub에서 sources.jsonl, frame.csv, assets.csv, decisions.csv, advice.csv 원문을 다시 읽음. JSONL 파싱 54행, ID 고유 54, 직접 42, 실패 12. CSV는 줄 수(헤더 제외) frame 23, assets 16, decisions 8, advice 10, 각 문서의 S번호 정규식 추출 및 원장 존재 검산에서 미연결 ID 0. 이는 정적 행/ID 검사이며 CSV 라이브러리의 완전 구문검사·독립 법적 사실 판정 아님. 원격 원문 비교 확인. 독립 검토 없음.

| 질문 / 주장 또는 미확인 | 출처 URL·정확 위치 | 원장 행·분모 | 반증 조건 |
|---|---|---|---|
| Q1 단위 구분; output 미확인 | [jpeginfo test README](https://github.com/tjko/jpeginfo/blob/v1.7.1/test/README) 전체 및 [SDL hello.c](https://github.com/libsdl-org/SDL_ttf/blob/release-3.2.2/docs/hello.c) extern tiny_ttf; [darkslide report](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=998076) Message #5 --embed | S09/S10/S19/S02; A02/A05/A06/A11, 전체 assets 16 | 고정판에서 데이터 참조가 없거나 동일 고지가 명시적으로 모든 산출물을 포함 |
| Q2 같은 notice 충분과 별도 notice | [showimage](https://github.com/libsdl-org/SDL_image/blob/release-3.2.4/examples/showimage.c) header, [root notice](https://github.com/libsdl-org/SDL_image/blob/release-3.2.4/LICENSE.txt) 전체; [D2 copyright](https://metadata.ftp-master.debian.org/changelogs//main/p/python-darkslide/python-darkslide_6.0.0-2_copyright) 31줄 | S15–17 1계보; S52 실제 copyright; 엄격 상류 5/6 | 같은 태그의 다른 권리 문단, 원권리자에게 해당 폰트까지 포함하는 명시 증거 |
| Q3 결정·다른 이유 | [OTS](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=976260) #10/#17, #22/#29/#34; [jpeginfo](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1064380) #8/#15/#25; [rqrr](https://bugzilla.redhat.com/show_bug.cgi?id=2350889) 댓글 1,3–6 | S01/S03/S08; 결정 8행 중 D2 최종 미확인 | sponsor가 다른 이유만으로 제거했음을 보여 주는 changelog/patch, 실제 같은 파일 포함 |
| Q4 같은 판 실제 목록 | [source test dir](https://sources.debian.org/src/jpeginfo/1.7.1%2Bdfsg-1/test) 목록 2개, [amd64 filelist](https://packages.debian.org/trixie/amd64/jpeginfo/filelist) 전체 5개, [package version](https://packages.debian.org/trixie/jpeginfo) arch table; [darkslide filelist](https://packages.debian.org/trixie/all/darkslide/filelist) examples/_assets | S25–29, 사건 8개 중 지정 source+binary 경로 동일판 연결 1(D3); D2 binary만 연결; 다른 6 완전 미확인 | 정확 archive에서 해당 jpg 발견, filelist와 package NVR 불일치 |
| Q5 A/B/C 및 교체 반례 | [FreeCAD 1.0.2 notice](https://github.com/FreeCAD/FreeCAD/blob/1.0.2/src/Mod/TechDraw/Gui/Resources/fonts/Y14.5Font.license) 전체; [BTS](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1091771) 원저자 2025-08-19 및 1.0.2+dfsg-1 changelog; [pillow README](https://github.com/Isotr0py/pillow-jpegxl-plugin/blob/a8cb191/test/images/README.md) 전체 | S04/S11/S12/S20–22; 8사건 중 결정 변화 2, 실제 파일 교체에 의한 뒤집힘 미확인 8 | 원판→교체 파일 해시와 새 고지 및 실제 포함의 인과 연결 |
| Q6 타 분야 범위 | [Met](https://www.metmuseum.org/art/collection/search/436532) Public Domain/Audio/Object 67.187.70a; [Met OA](https://www.metmuseum.org/hubs/open-access) OA Initiative; [Bach](https://imslp.org/wiki/Cello_Suite_No.1_in_G_major,_BWV_1007_(Bach,_Johann_Sebastian)) #483287/#310845; [Beethoven](https://imslp.org/wiki/Piano_Sonata_No.6_(Beethoven)) #00006/#585387 | S32–36; 작품 기록 2+2, 실제 정정 이력 0/4 확인 | 동일 객체별 역사적인 rights field 변경 및 file-specific grant |
| Q7 반환 문구 | [jpeginfo purpose](https://packages.debian.org/trixie/jpeginfo) 설명/arch, [D3 source](https://sources.debian.org/src/jpeginfo/1.7.1%2Bdfsg-1/test); [F2 reviewer](https://bugzilla.redhat.com/show_bug.cgi?id=2352900) 댓글 6–7 | R01–R10, 예시 10/10, 실제 사용자 검증 0/10 | 실제 사용자 목적이 복제였거나 문장이 패키지 포함을 우리 배포 승인으로 오해시킴 |

## 경쟁 설명과 강도 하향

D2 크기 이슈(보고자 추정 >75%, 약 400KiB)는 실제 제외로 관측되지 않음. SourceSansPro 조건 미상이며 OFL 언급은 Alegreya로 한정(원판 오독 정정, S02/S52). D1 build failure 해결이 권리 문제 해결과 같은 조치라는 설명은 시점/메시지 분리로 반박. F4 criterion과 중복 LICENSE 경고가 사진 제외 사유라는 설명은 S08의 별도 항목 및 명시 사진 지적으로 약화. 그러나 순수 비권리 파일 제외 실증은 없음. F2 후속 fc43 installed-tests는 예제 자체가 전혀 배포 안 된다는 일반화를 약화; fc42 exact source/devel/debugsource 미확인. D4 새 허가는 파일 교체와 다르고 F3 고지 명시화도 실제 포함이 아니므로 결과표에서 판정 하향.

## 종료 조건 체크

- 자연창 0/20 복원, 두 배포처 하한 미확인. 분모 0 빈도 계산 안 함. frame은 일부 합성 순위 및 미열람/배제, 목적층을 분리했다. 첫 검색 원반환 전체 미보존.
- 22 고유 계보 총량, 엄격 상류 5/6(남은 1); 8 하류 넓은 사건, 동일판/적격 확인 미달. 배포 목록 5, 그 중 후속판 2. 박물관 2, 악보 2 권리 표시를 읽었으나 정정 원자료 미달. S23은 파일 자체 권리 고지가 아니므로 6번째로 세지 않음.
- 일반 notice 자동 허가 또는 하류 제외=법적 금지로 쓰지 않음. 사용자의 목적 및 조직/관할별 확인을 표시.
- 실제 패키지 다운로드/해시 비교/제품 실행/빌드/독립 검토 미실시. 정확 재개 명령·입력·기대값은 COUNTEREXAMPLES.md. GitHub 원격 파일 읽기와 compare만 실제 수행. workbench session manifest 및 검사 미실시(이 웹 작업에서 명령 실행하지 않음); 인계에 적음.
- 결과를 본 뒤 바뀐 해석은 phase 4 정정 커밋 및 COUNTEREXAMPLES에 남김. 원판 유지, 산입 분모 그대로. 최종 상태 PARTIAL.
