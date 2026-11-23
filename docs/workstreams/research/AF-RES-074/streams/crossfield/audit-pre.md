# AF-RES-074 봉인 설계·원문 독립 모델 감사

검토자 `/root/crossfield`는 자연·대조 packet 원작성자와 다른 모델 판독자다. 사람 독립 판독이나 맹검은 아니다. 부모가 알려 준 위험도 인수했으므로 발견을 완전 독립 발생이라고 주장하지 않는다. 기준 봉인은 `0eb5235cd8f0f3d5ec3bfb92022990ee713d7d1c`다. 판정 집계·최종 결과는 아직 검토 범위 밖이다.

## 판정에 영향을 주는 발견

| 발견 | 현재 판독 | 결과에 필요한 처리 |
| --- | --- | --- |
| AUD-F01 PAN-N2 | [원요구](https://github.com/jgm/pandoc/issues/7022#issue-783984420)는 global lang 키 유지를 필수로 확정하지 않는다. 원하는 것은 서양폰트 분리와 중국어 따옴표의 원치 않는 글꼴 변화 회피이며 다른 해결책도 묻는다. | pre를 고치지 말고 `predicate_mismatch`를 사후 기록한다. 구현키 유지와 의미보존을 같은 must_retain으로 세지 말고 과잉질문·반대값 제약위반은 불명으로 둔다. 작성자가 이 시정에 동의했다. |
| AUD-F02 PAN-C1/C2 | [parse-raw](https://github.com/jgm/pandoc/blob/dcbd8d326cce4960e0d736e25e7d00f9057a1fc2/test/command/parse-raw.md) 두 LaTeX 블록은 같은 입력·다른 기대텍스트다. [sloppypar](https://github.com/jgm/pandoc/blob/dcbd8d326cce4960e0d736e25e7d00f9057a1fc2/test/command/sloppypar.md)는 같은 입력·완전히 같은 native AST 기대텍스트다. | stored expectation 수준의 양성·음성은 확인. 사후 결과를 보고 구성한 사실과 실제 실행 미실시를 유지한다. |
| AUD-F03 GDAL-C1 | [원시험](https://github.com/OSGeo/gdal/blob/258d73a17b1f7e93c9cf9b60a2411545d51879de/autotest/utilities/test_gdalwarp.py)의 nearest는 checksum, bilinear는 ref TIFF 대비 허용차1 검사다. 원 ref와 입력을 독립 회수해 2배 nearest 모형과 반례픽셀을 대조했다. | 원시험 기대·분석적 모형·현행 실행을 구분한다. 상세는 아래 수치 감사에 있다. |
| AUD-F04 GDAL-C2 | [원시험6/7](https://github.com/OSGeo/gdal/blob/258d73a17b1f7e93c9cf9b60a2411545d51879de/autotest/utilities/test_gdal_translate.py)의 checksum 일치만으로 완전파일동일성을 보장하지 않는다. | 원판에서는 20×20 입력·동일40×40 목표와 저장된 checksum 일치로 제한. 3.10.3의 추가 실행에서 확인한 바이트동일성은 그 판에만 귀속한다. |
| AUD-F05 PAN-N1 | [Lua 문서](https://github.com/jgm/pandoc/blob/dcbd8d326cce4960e0d736e25e7d00f9057a1fc2/doc/lua-filters.md)의 FORMAT과 RawBlock은 별개의 절이다. | strict 예산 이탈을 유지. 나중에 필터를 완성해도 기존 봉인의 예산을 소급해 복구하지 않는다. |
| AUD-F06 GDAL-N3 | 원 후보는3.1.4와3.2.1 혼합판이다. 추가로3.2.1 SetGeogCS 절도 직접 확인했으나 해당 TIFF의 EPSG 재식별 성공을 뜻하지 않는다. | 같은 판의 추가 근거는 expansion으로 기록. 원본문의 버전 변화 설명 또는 실제 성공까지 correct로 승격하지 않는다. |
| AUD-F07 PAN-C1 | 바뀐 기술 필드는 raw_tex 옵션이고 질문은 raw 보존 목적이다. | 기술 toggle 유효성과 질문의 정보가치를 분리. 자연 사건의 환경정보 질문 효과로 읽지 않는다. |
| AUD-F08 여러 자연 사건 | AST 검사·필터 구현·지원 범위 검토는 유용한 다음 행동이지만 변환 완료와 같지 않다. | hold/unjudgeable와 next_action을 따로 보존. 무응답을 false나 값2로 대입하지 않는다. |

## GDAL 수치 감사의 정확한 범위

[audit-gdal-pixels.json](audit-gdal-pixels.json)은 고정3.2.1 입력 TIFF와 bilinear ref TIFF를 원 URL에서 다시 받아 작성자의 파일과 SHA256이 같음을 확인한 기록이다. Pillow로 source20×20, reference40×40을 읽었다. 정규 affine GCP와 정확2배 grid라는 명시적 가정에서 nearest의2×2 반복 배열을 계산하면 `(x=1,y=0)`에서107, bilinear ref는111이다. 원시험 허용구간110–112와 겹치지 않으며 허용차1 밖의 픽셀은1380개다. **이것은 저장된 기대산출물과 분석적 모형의 비교이고3.2.1 엔진 실행은 아니다.**

별도로 작성자의3.10.3 실행영수증과 산출물4개를 읽었다. 기록한 파일 SHA와 실제 파일 SHA가 모두 같고, nearest/bilinear는1510픽셀이 다르다. pixels/percent는 파일 바이트도 같다. 새로 엔진을 재실행하지 않았으며, 이 현행판 확인으로 역사적3.2.1 실행 성공을 보고하지 않는다. 원시험의 checksum equality와 이 추가 확인은 다른 증거층이다.

## 출처와 남은 감사

[audit-pre.json](audit-pre.json)에 원문 접근9행과 발견8건, 판·blobSHA·확인UTC·Q 연결·판단을 바꿀 원자료를 남겼다. 감사 재열람은 원저작 최소량을 늘리지 않는다. 다음 감사는 최종 criteria/scores에서 위 제한·시정이 실제 분모와 출력 문구에 반영됐는지 확인하는 것이다.
