# AF-RES-217 반례와 정정

## 주 실행과 분리한 대조

| 대조 | 의도한 틀린 추론 | 실제 관측 | 영수증 |
| --- | --- | --- | --- |
| CT01 명시 경로 누락 | 엔진의 파일 오류는 구성 문제다 | eng open 두 차례 ENOENT, 모델 read 없음, Init −1, exit 1, 0 B | [CT01 L1](receipts/controls.jsonl#L1) [trace](receipts/controls-trace/CT01.txt) |
| CT02 합성 1 B, eng.traineddata | basename과 open 성공이 유효한 모델을 보증한다 | 원본과 다른 합성 바이트. open 성공·read 양성, Init −1, exit 1, 0 B. 방금 대조와 동일한 첫 오류 문구 | [CT02 L2](receipts/controls.jsonl#L2) [trace](receipts/controls-trace/CT02.txt) |
| CT03 명시 A01, 환경 A05 | 동일 basename이면 어느 모음이든 선택될 수 있다 | OEM0에서 명시 A01만 읽음. Init/exit 0/0, 27 B | [CT03 L3](receipts/controls.jsonl#L3) [trace](receipts/controls-trace/CT03.txt) |
| CT04 명시 A05, 환경 A01 | 다른 경로에 legacy 파일이 있으면 자동으로 복구된다 | 명시 A05만 읽음. Init/exit −1/1, 0 B, legacy 구성 오류 | [CT04 L4](receipts/controls.jsonl#L4) [trace](receipts/controls-trace/CT04.txt) |
| CT05 흰 페이지 | 빈 문자열이 초기화 실패를 뜻한다 | A05 및 흰 입력 read, Init/exit 0/0, stdout 0 B·stderr 0 B | [CT05 L5](receipts/controls.jsonl#L5) [trace](receipts/controls-trace/CT05.txt) |
| CT06 eng+ara 요청, eng만 배치 | exit 0과 글자가 요청 언어 전체의 성공을 보증한다 | ara ENOENT 및 언어 실패, Init/exit 0/0, stdout 29 B, API 실제 eng만 | [CT06 L6, API L13](receipts/controls.jsonl#L6) [CLI trace](receipts/controls-trace/CT06.txt) [API](receipts/controls.jsonl#L13) |
| CT07 eng+ara 두 파일 | 두 언어의 실제 로드를 성공 상태에서 구분할 수 없다 | 두 파일 read, Init/exit 0/0, stdout 52 B, API 실제 eng·ara | [CT07 L7](receipts/controls.jsonl#L7) [CLI trace](receipts/controls-trace/CT07.txt) [API L14](receipts/controls.jsonl#L14) |
| CT08–10 en_GB 사전 | 사전 단어장만 있으면 접사와 철자 검사가 동작한다 | CT08 두 파일 read 및 exit 0. 출력은 qzxvnotaword 한 단어. aff 또는 dic을 뺀 CT09/10은 공히 사전 파일 오류·exit 1 | [CT08–10 L8–10](receipts/controls.jsonl#L8-L10) [CT08 trace](receipts/controls-trace/CT08.txt) |
| C ABI legacy 확인 | OEM0 양성이 LSTM 폴백일 수 있다 | A01 Init 0, 실제 eng, 효과 OEM 0. A05 Init −1. 이 API 프로세스는 측정 결과를 출력한 후 자체 exit 0 | [API-A01·A05 L11–12](receipts/controls.jsonl#L11-L12) |

같은 오류 문구여도 CT01·CT02의 증거가 다르다. CT01은 명시 경로를 수정할 근거다. CT02는 파일 바이트와 출처를 고칠 근거다. CT04처럼 legacy 구성만 없다면 모드 또는 모델 링크를 바꾼다. [E02 tessedit.cpp L82–96, L149–193](https://github.com/tesseract-ocr/tesseract/blob/080da83cc51c4ef8b324a7e03146fe0bd7e0944b/src/ccmain/tessedit.cpp#L82-L193)

## 구성 위치 보정

핵심 실행 묶음의 components.csv가 인용한 첫 directory offset은 여섯 파일 모두 192 B였다. −d 원출력의 값을 유지하되, 물리 파일 오프셋은 별도 열에 입력했다. 여섯 원본에서 앞 196 B를 읽었고 4 B entry count 값 24 및 이어지는 24개 8 B little-endian offset을 확인했다. 모든 nonnegative 엔트리의 실제 시작은 −d 표시보다 4 B 뒤였다. 각 payload 크기는 raw offset의 차분과 −d에 일치했다. 예컨대 A01 unicharset은 표시 192 B, 파일 시작 196 B, 길이 7,477 B다. Directory()의 시작 계산이 count를 제외하고 Serialize()는 포함하는 차이와 일치한다. 자산·구성·모드 판정은 동일하다. [E04 설명 위치 L176–222](https://github.com/tesseract-ocr/tesseract/blob/080da83cc51c4ef8b324a7e03146fe0bd7e0944b/src/ccutil/tessdatamanager.cpp#L176-L222) [헤더 원값](receipts/headers.jsonl) [구성표](components.csv)

A04의 545 B config에는 Cube 이름의 설명 주석과 숫자 1이 함께 있다. 5.3.0 enum에서 1은 LSTM이며, 명시 OEM0이 config 후에 적용돼 legacy 오류가 났다. A02의 27 B config도 숫자 1이다. 두 config 모두 tessedit_load_sublangs가 없고 나머지 네 파일에는 config 엔트리가 없다. 동반 언어를 요구하는 다른 모델은 별도 관측이 필요하다. [E12 OcrEngineMode L263–277](https://github.com/tesseract-ocr/tesseract/blob/080da83cc51c4ef8b324a7e03146fe0bd7e0944b/include/tesseract/publictypes.h#L263-L277) [A02/A04 config 원값 L2, L4](receipts/components.jsonl#L2-L4) [C06 sublanguage 보고](https://github.com/tesseract-ocr/tesseract/issues/4002)

## 사전 제작자의 대조

Hunspell v1.7.1 규격에서 dic은 단어와 플래그 목록, aff는 인코딩과 플래그에 붙는 접사 규칙이다. en_GB 3.1.4의 walk/SRGDB와 aff의 D 규칙을 읽었다. dic에 독립 walked 행이 없지만 CT08은 walk, walked, colour를 미인식 목록에 내보내지 않았다. 합성 qzxvnotaword는 양성 대조로 출력됐다. 동일 변종의 aff/dic 두 링크와 앱의 사전 선택이 필요하다. Tesseract 단일 traineddata의 내부 OEM 구성 차이와 Hunspell의 외부 동반 파일 계약은 같은 파일명 검사를 공유하고, 적합성을 확인할 단위는 각각 컨테이너 구성과 배포 쌍이다. [H01 규격 L5–18, L507–520](https://github.com/hunspell/hunspell/blob/1180421f50f211984211e968eb6801ffd3390b8f/man/hunspell.5#L5-L18) [H02 aff D 규칙 L385–410](https://github.com/LibreOffice/dictionaries/blob/da1d9d4db2f9a45f1665dfd3da3bc3e2937290b5/en/en_GB.aff#L385-L410) [H03 dic walk L93248](https://github.com/LibreOffice/dictionaries/blob/da1d9d4db2f9a45f1665dfd3da3bc3e2937290b5/en/en_GB.dic#L93248)
