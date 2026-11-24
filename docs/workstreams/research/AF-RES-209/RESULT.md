# AF-RES-209 — JPEG 방향과 보존 단서를 더한 검색의 실제 첫 링크 비교

| 원요구 | 보존 대상·원문 주소 | A 질의 | B의 유일한 단서·근거 | 미확인 |
|---|---|---|---|---|
| 703 폰 세로 사진이 90° 돌아가 저장되고 EXIF가 있으면 디코딩 시 바르게 보이게 | 표시 방향 명시, 저장 데이터 변경 요구 없음. [S01 body](https://github.com/libjpeg-turbo/libjpeg-turbo/issues/703) | portrait mode phone pictures rotated by 90 degrees EXIF metadata image viewers open right way up | Orientation — [M02 L210–222](https://github.com/exiftool/exiftool/blob/master/html/TagNames/EXIF.html#L210) | 계수, 픽셀 불변량, 경계·썸네일, 입력 파일 미확인 |
| 774 디코딩 시 설정한 회전 정보가 일부 이미지에 적용되지 않음 | 바른 방향 명시; 보존 조건 없음. [S02 body](https://github.com/libjpeg-turbo/libjpeg-turbo/issues/774) | image rotation information when decoding the image decoded images were not rotated correctly | EXIF — M02 태그표에 근거한 경쟁 가설, 원문 EXIF 명시 아님 | JPEG는 저장소 문맥만; 회전 설정의 API/메타데이터 형식·샘플 미확인 |
| 847 crop/drop 확대에서 불완전 edge block 보존, 오른쪽 4px 손실 | 경계 픽셀 보존 및 artifact 허용 명시; 회전 요구 아님. [S03 body](https://github.com/libjpeg-turbo/libjpeg-turbo/issues/847) | incomplete edge blocks disappear crop retain them disable trimming | iMCU — [M01 L633–713,715–748](https://github.com/libjpeg-turbo/libjpeg-turbo/blob/main/doc/usage.txt) | 배포 버전, 직접 계수/픽셀 측정 미확인 |
| 265 Orientation을 정수로 쓰기, 6 실패·8이 180°가 됨; 추가 태그 이의 | 올바른 메타데이터 값, 추가 태그 별도 보존 관심. [S04 body](https://github.com/exiftool/exiftool/issues/265) | Writing Orientation may not work when specified as int value Rotate 90 CW | IFD0 — [M02 L210–222](https://github.com/exiftool/exiftool/blob/master/html/TagNames/EXIF.html#L210); 필드 위치이지 PrintConv 해법 아님 | 픽셀 회전/계수 보존 명시 없음; 동일 입력 실제 쓰기와 바이트 차이 미확인 |

| 사건·질의 | 검색면·시각 | 실제 1~3위 URL | 누른 경로·횟수 | 도착 절의 충족·누락 | 결측 |
|---|---|---|---|---|---|
| 703 A (1) | fast 개별, 2026-11-24 UTC | 1 [Mozilla X04](https://support.mozilla.org/en-US/questions/1172599); 2 [iFormat P1.2](https://iformat.io/blog/how-to-fix-a-sideways-photo-from-your-phone-exif-rotation); 3 [MultiTools P1.3](https://multitoolsa.com/blog/exif-orientation-bug-photos-rotating-sideways) | 1번 열람, 추가 0회 | X04 L133–150,204–221: 뷰어 차이, 디코더 구현 없음; 폭/높이만으로 방향 판단 불가 | native rank 및 개별 정확 시각 미확인; 2/3 본문 미열람 |
| 703 B (2) | 동일 | 1 [iFormat X05](https://iformat.io/blog/how-to-fix-a-sideways-photo-from-your-phone-exif-rotation); 2 [Mozilla P2.2](https://support.mozilla.org/en-US/questions/1172599); 3 [WipeTheAI P2.3](https://wipetheai.com/guides/why-photo-is-sideways-exif-orientation) | 1번→[F03 EXIF](https://exiftool.org/TagNames/EXIF.html) 1회 403 | X05 L88–114: 태그값·정규화 설명, 정확한 디코더 통합 없음 | F03 접근 실패; 나머지 공통 결측 |
| 774 B (3) | 동일 | 1 [MWG X01](https://uploads.guim.co.uk/2021/02/08/mwg_guidance.pdf); 2 [nvJPEG P3.2](https://docs.nvidia.com/cuda/nvjpeg/); 3 [nvJPEG 11.7 P3.3](https://docs.nvidia.com/cuda/archive/11.7.0/pdf/nvJPEG.pdf) | 1번 열람, 추가 0회 | X01 §5.4 p39: EXIF 및 썸네일 규칙, 실제 API/입력 미확인 | 공통 결측 |
| 774 A (4) | 동일 | 1 [ITU-T T.84 X02](https://www.itu.int/rec/dologin_pub.asp?id=T-REC-T.84-199607-I%21%21PDF-E&lang=e&type=items); 2 [Ascend P4.2](https://www.hiascend.com/doc_center/source/en/CANNCommunityEdition/910/acce/dvpp/aclcppdevg_03_0355.html); 3 [sglang P4.3](https://github.com/sgl-project/sglang/issues/33464) | 1번 열람, 추가 0회 | X02 §F.2.3.2.4 table F.8 p49: SPIFF 회전/flip; EXIF 아님 | 원제보 SPIFF 여부/공통 결측 |
| 847 A (5) | 동일 | 1 [원제보 S03](https://github.com/libjpeg-turbo/libjpeg-turbo/issues/847); 2 [quilting P5.2](https://quiltgarden.jp/qwp/wp-content/uploads/2021/10/6c4f5b298457bbb1c3c333959218960a.pdf); 3 [Mojang P5.3](https://bugs.mojang.com/browse/MCPE-124841) | 1번 열람, 추가 0회 | S03/R03/R04/R08 L141–143,171–211 및 댓글: 정확한 4px/확대/버전 조건 | 실제 배포/성능/공통 결측 |
| 847 B (6) | 동일 | 1 [mozjpeg X03](https://github.com/mozilla/mozjpeg/blob/master/usage.txt); 2 [NXP P6.2](https://community.nxp.com/pwmxy87654/attachments/pwmxy87654/imx-processors/212272/1/MCUXpresso%20SDK%20API%20Reference%20Manual_MIMX8QX6.pdf); 3 [Mojang P6.3](https://bugs.mojang.com/browse/MCPE-124841) | 1번 열람, 추가 0회 | X03 L2801–2883: 일반 iMCU 규칙; 해당 확대 문제와 dev/3.2 변경 누락 | 공통 결측; X03 계보 중복으로 원장 하한 비산입 |
| 265 B (7) | 동일 | 1 [원제보 S04](https://github.com/exiftool/exiftool/issues/265); 2 [mirror P7.2](https://githubhelp.com/exiftool/exiftool/issues/459); 3 [Android P7.3](https://android.googlesource.com/platform/frameworks/support.git/%2B/18ff3abef5c26888c3feb53c02dbcdcc08736b7e/exifinterface/exifinterface/src/main/java/androidx/exifinterface/media/ExifInterface.java) | 1번→[F01 CLI](https://exiftool.org/exiftool_pod.html#n---printConv), [F02 FAQ](https://exiftool.org/faq.html#Q6) 2회 모두 403 | S04/R05 L218–228,280–293: PrintConv 단축형, 추가 mandatory tags; 정수 쓰기 명령의 공식 도착절 실패 | F01/F02 실패·공통 결측 |
| 265 A (8) | 동일 | 1 [원제보 S04](https://github.com/exiftool/exiftool/issues/265); 2 [W3C P8.2](https://www.w3.org/TR/css-writing-modes/); 3 [ITU T.505 P8.3](https://www.itu.int/rec/dologin_pub.asp?id=T-REC-T.505-199101-S%21%21PDF-E&lang=e&type=items) | 1번→F01,F02 2회 모두 403 | S04/R05 같은 첫 절/같은 실패 | F01/F02 실패·공통 결측 |

| 사건 | A와 B 판정 | 적합한 첫 링크 | 틀릴 입력 | 사용 결과 증거·미확인 |
|---|---|---|---|---|
| 703 | 응답순 판정불가: B 설명 구체화, 필수 디코더 통합 미충족; native rank 판정불가 | 관측 X05 L88–114는 태그값 안내에 유용하나 정확한 구현은 수동 보강 [R01 댓글](https://github.com/libjpeg-turbo/libjpeg-turbo/issues/703#issuecomment-1611830602), [D01 exif_transpose](https://pillow.readthedocs.io/en/stable/reference/ImageOps.html#PIL.ImageOps.exif_transpose) | 이미 정상 1/태그 없음, 무시하는 뷰어, 이중 회전 | 실제 처리/계수 비교 없음. D02 회귀 코드만 읽음 |
| 774 | 응답순 판정불가; EXIF 가설 하 B 유용, SPIFF이면 A가 더 관련; native rank 판정불가 | X01 §5.4 또는 X02 table F.8, 입력 확인 후 수동 보강 [R02 댓글](https://github.com/libjpeg-turbo/libjpeg-turbo/issues/774#issuecomment-2186739246) | SPIFF, 명시 디코더 rotation 인자, EXIF 없음 | 입력 포맷·API·재현 결과 없음 |
| 847 | 응답순 B 악화; native rank 판정불가 | [S03/R08 해당 사건/구현 댓글](https://github.com/libjpeg-turbo/libjpeg-turbo/issues/847#issuecomment-3708270773), 실제 노출 A 첫 이슈 | 구버전 crop extension vs 신버전; 부분 iMCU; perfect 실패 | 제작자/신고자 발언, 직접 출력·배포 버전 미확인 |
| 265 | 응답순 동률(동일 첫 URL과 실패); native rank 판정불가 | 관측 [S04/R05 답변](https://github.com/exiftool/exiftool/issues/265#issuecomment-2132429005); 별도 수동 [M06 L686–703](https://github.com/exiftool/exiftool/blob/master/html/exiftool_pod.html#L686) | bare =8 단축형, 새 IFD mandatory 태그, Orientation과 실제 픽셀 불일치 | 원제보 로그만, 자체 실행·metadata diff 미확인 |

## 판정 범위
표 2의 1~3은 **도구가 개별 검색 응답에 반환한 실제 나열 위치**이며 검색 사업자의 원래 유기적 순위가 아니다. Pn.k는 paths.csv의 query_order=n 및 response_position=k 노출 영수증, 본문 근거가 아니다. 첫 결과 URL 8/8 열람, 24/24 응답 위치 기록, 5회 실제 링크 따라가기 시도 중 성공 0 (모두 403). 날짜 UTC 2026-11-24; SCOPE 동결 commit 21:29:00Z, 원장 stage2 21:31:42Z, 영수증 stage3 21:32:13Z. 개별 검색 정확한 시각과 네이티브 순위, raw snippet 원문, 외부 재조회 가능한 SERP permalink 미제공; paths에는 보이는 문구의 요약과 세션 ref를 보존. 반환 순서가 있으므로 다른 검색면 전체를 반복하지 않았으며 native rank 판정은 보류한다. Native rank가 필수인 해석에서는 PARTIAL(0/8 verified native rank). 개별 관측 응답 비교는 4쌍 중 0 개선/1 악화/1 동률/2 판정불가. 이 숫자를 다른 검색면/전체 사용자에게 일반화하지 않는다. 703 B가 더 자세하다고 해서 필수 조건을 충족했다고 계산하지 않았다.
원문 37행, 직접 열린 34, 중복 계보 X03 비산입 1, 실패 3, 산입 33 고유 work_id/15 lineage_id. 사건 4개, 계획 자리 24개. 필수 유형 4/4,7/7,5/5,4/3,3/3; 추가 10. 댓글은 독립 저작 답변이지만 동일 사건/제작자 계보이며 별개 표본 아님. PDF 2개는 실제 페이지 screenshot 확인. SCOPE의 원요구/매뉴얼 사전 노출로 평가자 비맹검.

## Q1–Q7
**Q1** S01–04에서 보기 방향, 저장 픽셀, 계수, 경계, 썸네일을 분리했다. 703/774는 화면/디코드 목표, 847은 경계 요구(회전 아님), 265는 정수 메타데이터와 불청구 태그 변경. JPEG 저장 픽셀 변경이나 계수/썸네일 보존 요구를 임의로 보태지 않았다. 원래 revision 및 개인 입력은 미확인; 다음은 공개 최소 재현 샘플 확인.
**Q2** SCOPE 사전 커밋 47773aacc4957539115c547cef399641ea166a7a에서 AB/BA 교대 8개 고정. 각 B는 A+공백+단일 토큰, 같은 영어/검색면/예산. 703 이미 EXIF, 265 이미 Orientation: 기술어 중복의 수익 체감, 774 EXIF 가설 명시. 다음은 공개 SERP 스냅샷의 고정 지역/정렬/브라우저 실험.
**Q3** paths.csv는 8개 개별 호출, 24 자리와 원주소·문구 요약·세션 ref. 원래 검색엔진 순위 미공개, 정확한 클릭 경로 관측과 분리. 추가 검색면에선 동일 A/B 전체를 별도 실험으로 진행해야 하고 이 결과와 합치면 안 된다.
**Q4** 첫 결과 실제 도착 절은 표 2, 본문 범위는 sources.jsonl. 847 A만 정확한 문제+버전 응답, 265 양쪽 정확한 이슈이나 공식 후속 403, 나머지 불충분. 수동 GitHub M05/M06/M02는 403을 메워주는 별도 참고 자료이지 성공한 클릭이 아니다. 다음은 기관/공식 링크 접근 가능 환경에서 동일 예산 재판독.
**Q5** (M01–07 R01–08 D01–06 X01–02) EXIF 표시 태그(1 정상, 6=90 CW, 8=270 CW) 수정은 압축 계수 회전과 다른 작업. 디코더가 태그를 읽지 않으면 보기 결과 다름. DCT 재배치는 재양자화 없이 가능하지만 부분 iMCU 제약과 파일 마커/태그는 별개; trim은 경계 손실, perfect는 거부; 픽셀 디코드/회전/재인코드는 또 다른 해법. MWG 썸네일 동기 요구와 D02 idempotence 시험 코드 확인. 직접 변환/해시 검사 없음.
**Q6** I01 §1.1·2·4.3·4.6: region→size→mirror/rotation→quality→format, 이미지 반환만 규정. [I03 L108–124 LOC](https://www.loc.gov/apis/micro-services/image-services/) 동일 ID 문서 제공 0/90 주소쌍과 info.json은 COUNTEREXAMPLES.md. 기관이 반환한 접근용 표현과 원본 보존 업무 분리; I02 843px 파생 크기 제한, I04 다른 ID 회전 예. IIIF 요청 성공 자체가 마스터 불변/계수 유지 증거가 아님. 다음은 권한 있는 fixture 저장소에서 master hash 전후 비교 및 capability 확인.
**Q7** 검색 노출 순서, 첫 문서 필수 조건 충족, 실제 목적 달성은 각각의 평가. 847 A 한 문서만으로 문제/개발 브랜치 답변 충분, B가 밀어냄. 265 둘 다 같은 첫 결과, 추가 단서가 2/3 순서를 달리해도 핵심 첫 링크 개선 없음. 실제 성공 증거는 같은 입력·버전·flag·출력·태그·경계 검사 필요. 사용자 실험 미실시, 다음 Codex 절차는 HANDOFF.

## 제품 설계에 건넬 대안 (채택 전 검증)
1. **원요구 A 보존 + 메커니즘 B 병렬**: 검색문 두 개를 독립 실행하고 상위 후보 union을 제약별로 재판정. 원문 A만으로 정확한 답변이 나오면 추가 토큰 강제 금지. 847 실제 반례, 비용 쿼리 2배·중복 및 열람 비용. 검색 전 EXIF/JPEG를 추론한 경우 가설 표기; 774처럼 포맷 미확인 시 SPIFF/decoder flag 문서를 제거하지 않음. B가 필수 조건을 실제 채워야 승격.
2. **표시/데이터/계수/edge/tag 불변량 슬롯 분리**: 사용자에게 요구 확인 또는 원문 명시/추론/미확인 유지. 703 화면 표시 우선이면 viewer/decoder 문서, 파일 저장 요구 시 M01과 tag sync 조건, 265 PrintConv 우선이면 M06. 단일 lossless 레이블로 합치지 않음. 추가 설명 길이·분류 비용; 보존 불필요한 순수 조회라면 오히려 불필요한 링크.
3. **원문 직링크 + 도착절 요건 체크**: 코드/버전/조건이 갖춰진 일치 이슈와 maker 문서를 연결하되 실제 탐색 경로와 연구자 수동 추천을 분리. 403 처리: 접근 불가로 표시, 공개 GitHub HTML 대응을 별도 선택지로 제공. 대체 링크 성공은 실제 경로 성공으로 계산 금지. 링크 접근/버전 drift 검증 비용.
4. **다른 분야의 반환 표현 vs 원본**: IIIF처럼 변환을 주소에 드러낸 파생본 반환으로 원본 관리 문제를 분리. 원본 변경이 필수면 해결 아님. 회전 capability/순서/캐시/권한 확인. URL 표준이 원본 hash를 보장하지 않음.
5. **결과 검증을 검색 점수와 분리**: 같은 입력으로 실제 작업 후 바이트, 계수의 기하 대응, decoded 픽셀과 전체 경계, main/thumbnail EXIF를 각기 판정. 도구 설치/실행/비용은 이 조사 밖. 경쟁 설명이 확인되면 774 추천을 EXIF에서 SPIFF/API로 바꾸고 847에 실제 배포 버전이 없으면 dev/3.2 추천을 조건부로 강등.

| 불일치·약점 | 영향을 받는 결론 | 다음에 열 원자료·조사 | 판정을 바꿀 관측 |
|---|---|---|---|
| 검색 도구 반환 순서 24/24, 실제 유기적 순위 0/8, exact timestamp 및 원문 snippet 미보존 | A/B의 검색 우위 일반화 금지; strict PARTIAL | 동일 동결 질의 8건을 공개 검색면에서 순차 실행, 원시 스냅샷·순위·URL·UTC·동일 예산 기록 | #847에서 B가 정확한 이슈를 앞세우거나 A가 잃음; 나머지 쌍 필수 조건 변화 |
| 774 EXIF 가설·703 디코더 실제 입출력 미확인; 표본 847은 회전 아님 | 보존 단서 추가가 항상 개선이라는 주장 불가 | 원제보 공개 fixture/API/메타데이터 명세, D02 고정 테스트 및 무시 flag를 이용한 별도 실험 | 동일 입력에 대한 실제 포맷/회전 설정 확인 및 decoded 출력 정상화 |
| #847 dev/3.2 배포 및 #265 CLI 후속 링크 403, 원본/썸네일/계수 실측 0 | 정확한 링크 ≠ 성공·무손실·보존 보장 | 고정 release/commit 847 재현, 265 FAQ/CLI 접근 가능 재검색, 메타데이터 diff, IIIF master/derivative fixture | 버전별 경계/정수 태그 출력 및 불변량 검증; 기관 master 해시 전후 |
