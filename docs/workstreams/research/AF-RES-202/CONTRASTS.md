# 반례·교차 분야 대조 (04)

## 판정 분리
- 앱 개발자: 파일을 내려받는 링크만 필요하지 않다. 실행판/빌드 옵션/요구 언어/OEM/실제 data directory가 함께 맞아야 한다. [B06](https://github.com/tesseract-ocr/tesseract/blob/5.3.0/src/ccmain/tessedit.cpp) L82–190, [B07](https://github.com/tesseract-ocr/tesseract/blob/5.3.0/src/ccutil/ccutil.cpp) L39–91. 파일이 이미 로드 가능한 경우 엔진 설치 재권고·모델 재다운로드를 생략할 수 있다.
- 배포자: 모음 README는 계약이지 각 blob의 구성표가 아니다. tessdata Arabic/Indic legacy 제거(B03) 및 fast integer(B05) 때문에 모음 일반화를 금지. A01–06 각각 blob과 byte 수만 확보. B01 공개 eng dump의 마지막 offset+size가 A03 크기와 같으나 hash가 없으므로 동일 파일 판정하지 않는다. C31의 보고 크기와 맞아도 고정 blob 확인 아님.
- 원제보자: X1 실제 strace ENOENT(C09)와 S2 legacy components not present(C04)를 분리. S3는 slash 추측에서 LSTM-only 자가 진단(C06–08)으로 바뀌었으나 교체/실행 결과 없다. X3 정상 초기화 후 whitelist 공간 문제(C15–17), X9 일부 언어 누락 후 출력(C29–30)도 있다. 경고가 사라지거나 파일이 list-langs에 나타났다는 사실은 모든 언어 성공의 증거가 아니다.
- 철자 사전 유지자: E01 aff 규칙/encoding과 dic 어휘·flag의 의미가 맞아야 한다. E02와 E03 배포 목록은 en_US와 en_GB 각각 두 파일을 별도 표시한다. E04 LibreOffice UI/템플릿/AutoText 언어팩과 철자 사전 분리, E05 문서 언어 선택 별개. 파일 존재, 두 파일의 짝, 언어 variant, 호출자의 선택을 구분. OCR에서는 traineddata 내부 구성과 companion 언어팩을 다르게 링크한다. Hunspell actual body/parser·runtime은 이번 조사에서 미확인; 패키지 목록을 본문으로 승격하지 않는다.

## 경쟁 설명
1. 이름은 맞지만 경로가 다름: X1 /tmp//tesseract/share/tessdata vs /tmp/tessdata; strace ENOENT, 유지자 재현/quoted macro 제안(C09,C10,C37). 이 사례는 해당 컴파일판 특수 경로이며 5.3.0 동일 버그를 입증하지 않는다.
2. 경로는 보이지만 컨테이너 내용이 부적합: S1 크기 2364 B, 다른 파일 복사 자가 진단(C01–03); S2 OEM1 작동 vs OEM0 실패(C04); S3 파일 존재 목록과 legacy 에러(C06–08). X4 유지자의 HTML 가설(C38)→fast 모델 설명(C19); 실제 blob을 확보하지 않아 어느 것도 확정하지 않는다.
3. 파일이 열렸는데 품질/목적이 다름: X3 같은 언어의 설정 및 모드 차이(C15–17); X9 누락 grc에도 출력, μ 인식 문제 별개(C29–30). 실제 모든 언어 init과 결과 품질을 분리. X6 5.3.0에서 best chi_tra 하위언어 설정과 순서에 따라 빈 basename warning(C23–25,C39–41); 데이터 파일 구성/선택과 엔진 해석 버그가 공존할 수 있다.

## 변경 원장
- 03 cases.csv의 X1 날짜 2021-05(오류) → 2021-08-19(C09); 보강 원작성자 placeholder를 원장에 있는 이름으로 치환. X3 Linux(C15), X8 Ubuntu18.04 Docker(C27), X7/X8 원 오류 경로 복원.
- 02 C10/C19/C24/C25에 같은 사건의 복수 댓글 내용을 합쳤던 것을 별도 댓글 C37–41로 분리; 이전 주장과 URL 매핑을 명시. C41의 작성자와 정확 게시일은 미확인으로 낮춤. 원자료 수 산입하지 않음.
- 2020 page3 L202를 비산입 모집 기록에 추가. 전체 2021–25 원문 읽지 않았으므로 선별의 완전성 보장 없음. 신규 고정 바이너리 판독/실행은 하지 않았다.
