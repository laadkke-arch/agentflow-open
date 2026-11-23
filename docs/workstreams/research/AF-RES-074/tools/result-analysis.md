
자연군의 질문·후보는 후속 댓글을 읽기 전에 C02/C03으로 봉인했다. 그때 읽은 것은 현재 본문이었고 최초판의 provenance 확인은 사후였다. 뒤늦게 회수한8개 최초 본문은 사전 목적·제약과 같았지만 열람 시점을 소급 변경하지 않았다. Pandoc의 실제 문서 열람은 후보별 지정절 예산을 넘었고, GDAL-N3은 두 후보의 판이 달랐다. 추가 문서를 읽고 해결한 사실로 원래 제한된 노출의 판단을 소급 정당화하지 않았다. [봉인 기록](evidence/seals.json), [원질문 packet](packets.jsonl), [판정 수정 내역](evidence/root-adjudications.json).

PAN-N2에서 확인된 것은 **서양 글꼴 분리와 중국어 인용부호 문제 회피라는 결과 조건**이다. `lang: zh-CN`이라는 전역 키 자체를 무조건 남겨야 한다는 금지는 직접 확인되지 않는다. “다른 해결책”도 요청한 [현재 본문](https://github.com/jgm/pandoc/issues/7022)을 root와 별도 모델이 재독해 사전 `must_retain` 추론을 철회했다. 원 packet과 정책의 봉인 당시 추론은 그대로 보존했고, 점수에는 과잉 질문 `null`과 반사실 충돌 해제라는 사후 수정을 표시했다. 필드 의미를 잘못 정하면 값이 이미 있는지 여부부터 잘못 센다는 반례다.

PAN-C1은 더 직접적인 설계 한계가 있다. 조작한 필드는 reader의 `raw_tex` on/off인데 질문은 사용자의 raw 보존 목적이다. 목적을 flag 선택에 대응시키는 **연구자 매핑**을 사용한 구성 실험이다. 같은 필드에 대한 실제 질문 응답 효과를 관측했다고 쓰지 않는다. PAN-C1의 기대 출력은 파서 구분자 오류로 먼저 노출됐고, PAN-C2는 같게 나오는 시험을 찾은 뒤 골랐다. 두 쌍은 기술 대조로 남기되 사전 예측 성공 수에 넣지 않았다. [Pandoc 사후 분석](streams/pandoc/post-analysis.json).

## Q3. 값 하나만 바꿔서 결과가 갈리는가

구성 대조의 Pandoc 고정판은 **2.11.3.2 / `dcbd8d326cce4960e0d736e25e7d00f9057a1fc2`**, GDAL 고정판은 **v3.2.1 / `258d73a17b1f7e93c9cf9b60a2411545d51879de`**다. 각 쌍에서 입력과 다른 옵션을 고정한 근거, 기대 산출물의 원위치와 해시는 [criteria.csv](criteria.csv)에 있다. 어느 판의 저장 기대값인지와 어느 엔진에서 실제 실행했는지는 다른 열이다.

**PAN-C1 양성:** [parse-raw L1–13](https://github.com/jgm/pandoc/blob/dcbd8d326cce4960e0d736e25e7d00f9057a1fc2/test/command/parse-raw.md#L1-L13)은 같은 LaTeX 입력에 대해 `latex+raw_tex`와 `latex`만 바꾼다. 전자는 알 수 없는 매크로 조각을 raw 형식으로 남기고 후자는 생략한다. 동일 입력 해시와 두 저장 텍스트의 차이가 판별 근거다. 추가 검증에서는 공식 배포된2.11.3.2 바이너리로 두 명령을 실제 실행해 저장 기대 stdout과 바이트가 일치함을 확인했다. 오늘 수행한 연구자 실행이며 과거 날짜의 CI 영수증은 아니다.

**PAN-C2 음성:** [sloppypar L1–23](https://github.com/jgm/pandoc/blob/dcbd8d326cce4960e0d736e25e7d00f9057a1fc2/test/command/sloppypar.md#L1-L23)은 같은328자 입력과 native writer를 유지하고 같은 flag만 바꾼다. 기대 AST910자의 SHA256은 두 값 모두 `f80891c6d9bfdd39328a2e1fda370ec8d6033b7b0304f33555bd87b5e998bb60`이다. 추가 고정판 실행에서도 두 stdout은 저장 기대값과 정확히 일치했다. 이 입력에서 raw flag를 묻지 않아도 기본 reader라는 공통 행동이 충분하다. 모든 LaTeX 입력에서 같은 결과라는 주장은 PAN-C1이 반박한다.

**GDAL-C1 양성:** [test_gdalwarp_5](https://github.com/OSGeo/gdal/blob/258d73a17b1f7e93c9cf9b60a2411545d51879de/autotest/utilities/test_gdalwarp.py#L117-L136)의20×20 원본과 직사각형 GCP를 그대로 사용한다. [test10/test11](https://github.com/OSGeo/gdal/blob/258d73a17b1f7e93c9cf9b60a2411545d51879de/autotest/utilities/test_gdalwarp.py#L218-L252)은 출력 크기를40×40으로 고정하고 `-rn`과 `-rb`만 바꾼다. 단, 최근접 시험은 checksum18784를 검사하고 쌍선형 시험은 reference TIFF와 최대 픽셀 차이1을 허용한다. 서로 다른 assertion을 같은 종류의 정답 두 개라고 놓고 비교하지 않았다.

원본 격자와 GCP가 정확한2배 직사각형을 만든다는 전제에서 최근접은 각 원픽셀을2×2로 복제한다. 그 명세 기반 예측의 `(x=1,y=0)` 값은107인데 [고정 쌍선형 reference](https://github.com/OSGeo/gdal/blob/258d73a17b1f7e93c9cf9b60a2411545d51879de/autotest/utilities/ref_data/testgdalwarp11.tif)는111이고 허용 범위는110–112다. 이 분석에서는1,380픽셀이 허용 오차 밖이다. **이는 명세·저장 기준·명시적 기하 가정에 따른 독립 판별이며, 과거 엔진 실행이 아니다.** 다른 모델이 원본을 별도로 다운로드해 입력·reference 해시와 이 계산을 대조했다. [분석 영수증](streams/gdal/analytical-discriminator.json), [독립 픽셀 검토](streams/crossfield/audit-gdal-pixels.json).

**GDAL-C2 음성:** [translate test6/test7](https://github.com/OSGeo/gdal/blob/258d73a17b1f7e93c9cf9b60a2411545d51879de/autotest/utilities/test_gdal_translate.py#L149-L177)과 [-outsize 명세](https://github.com/OSGeo/gdal/blob/258d73a17b1f7e93c9cf9b60a2411545d51879de/gdal/doc/source/programs/gdal_translate.rst#L85-L90)는20×20 입력에서40×40과200%×200%를 같은 목표로 바꿀 수 있음을 뒷받침한다. 두 시험의 저장 checksum은18784다. **요구한 크기·기본 재표본화 행동의 동치**를 판정했고, 과거 두 TIFF의 모든 메타데이터·파일 바이트가 같다는 증거로 checksum을 확대하지 않았다. 입력이20×20이 아니면 이 동치는 깨질 수 있다.

### 별도 실행층: GDAL3.10.3

실제 제공된 셸에는 GDAL3.10.3이 있었고, 같은 고정 입력으로 GCP 준비와 네 변환을 실행했다. 실행5개 모두 종료값0이다. 최근접 checksum18784, 쌍선형19664였으며 두 출력은1,510/1,600픽셀이 달랐다. 고정 reference 자체의 checksum19694와 현대 쌍선형 출력의 checksum은 다르지만 최대 픽셀 차이는1이라 해당 과거 시험의 허용 오차와 양립한다. 픽셀/퍼센트 크기 표현의 현대 출력은 배열·지리 변환·전체 파일 SHA가 같다. [실제 명령·버전·시각·종료값](streams/gdal/researcher-run3103.json).

실행 입력·reference·GCP·최종 출력의 정확한7개 파일 바이트를 [artifact 묶음](evidence/gdal3103-artifacts.json)에 base64와 해시로 커밋했다. 임시 폴더가 없어도 복원할 수 있다. 이 영수증은3.10.3의 연구자 실행이며, 3.2.1의 역사 실행이나 자연 요청자의 사용 성공을 대신하지 않는다. [복원·재실행 명령](REPRODUCE.md).

### 추가 고정판 실행: Pandoc2.11.3.2

공식 release API와 Linux 자산의 태그를 확인하고 배포 바이너리의 버전·SHA256을 기록했다. 양성·음성 대조4개 명령과 empty_paragraphs 반례4개 pipeline을 실행했다. **8개 fixture,12개 process invocation 모두 종료값0이며 최종 stdout이 공식 저장 기대값과 정확히 일치했다.** 입력·기대 텍스트·실제 출력·pipeline 연결 해시가 커밋되어 있다. 논리적 fixture 해시는 구분자 앞의 마지막 LF를 제외하고, 실제 stdin/stdout 해시는 마지막 LF를 포함하므로26/4/910자 기대 본문이27/5/911바이트 출력이 되는 층을 구분했다. [공식 배포 확인](evidence/pandoc-release-fetch.json), [고정 입력](evidence/pandoc-fixed-fixtures.json), [실행 영수증](evidence/pandoc-fixed-run.json).

이 실행은 기대값 노출 뒤 구성한 선정 이력이나 목적→flag 질문 매핑 문제를 없애지 않는다. 정확한 해당판의 기술 출력을 확인하는 근거만 보강한다.

## Q4. 단일 링크·조건부 답·질문이 실제로 전달하는 것

**A의 보류와 잘못된 기본값은 다른 결과다.** PAN-C1에서 A는 목적을 모르는 동안 보류하므로, C의 답이 돌아와 단일 명령을 줄 수 있게 된 변화는 완료 범위의 증가다. A의 오답을 줄인 것으로 세지 않았다. GDAL-C1에서 A는 기본 최근접을 선택했다고 밝힌다. 공개된 가상 목표가 bilinear일 때는 그 명령이 틀리며, C-value2 또는 B의 bilinear 조건을 따르는 명령이 요구에 맞는다. 이 한 구성 시나리오의 차이를 자연 문의에서 C가 오류를 줄이는 빈도로 확대하지 않는다.

**B는 조건을 읽어 하나를 고르는 경로가 있어야 사용 가능하다.** PAN-C1은 raw 보존 요구를, GDAL-C1은 요청한 재표본화 의미를 사용자가 알고 선택한다는 조건에서 실행 경로를 준다. 실제 독자가 그 의미를 이해했는지는 측정하지 않았다. 음성2쌍의 B는 둘을 나열한 뒤 공통 기본 명령을 명시하므로 단일 행동으로 분류했다. 특히 GDAL-C2의 원문 B는 K1로 정규화할 수 있다고 적혀 있다. 이를 두 링크라는 이유만으로 조건부 또는 미해결로 분류하지 않도록 root가 수정했다. [원답](policies.csv), [수정 이유](evidence/root-adjudications.json).

자연군의 B는 그렇지 않다. 헤더 magic이 ENVI라고 해서 파일이 정상으로 열리는 전체 조건을 충족하지 않고, `reference.docx` 링크를 열었다고 해서 해당 Word 글꼴 문제가 해결되지 않는다. PAN-N1의 FORMAT 링크는 필터를 **개발할 다음 행동**이고 실행 가능한 필터 완성품은 아니다. GDAL-N4의 SRS 문서는 실패 시 파일 무잔류를 보장하지 않는다. 따라서 표2의 자연군 B에는 선택 미해결 열거 또는 보류를 남겼다. 링크의 실제 원절은 표1과 각 criterion URL에 고정했다.

한 URL도 두 조건을 설명할 수 있다. GDAL-C1의 최근접/쌍선형 후보는 같은 `-r` 절에 있고, GDAL-C2의 두 크기 표현도 같은 `-outsize` 절에 있다. `displayed_link_references`, `distinct_answer_documents`와 최종 행동 수를 별도로 센 이유다. URL2개를 읽는다고 두 독립 근거를 읽은 것은 아니다.

## Q5. 묻지 않아도 되는 경우와 값이 없어 판정할 수 없는 경우

음성 대조는 **확인한 입력·목표 범위에서 같은 행동이 충분함**을 증명한다. PAN-C2와 GDAL-C2에서는 C-value1/value2/no_answer 모두 공통 행동을 줄 수 있다. 질문은 추가 선택을 만들지 않는다. 반면 양성 대조에서 값이 없으면 어느 출력을 원하는지 미확인이다. 이것은 값2이거나 부정이라는 뜻이 아니며, 무응답 행에서 정답 하나를 임의로 채우지 않았다.

현재 원문에 목적이 있는 PAN-N1의 형식별 CSS, PAN-N3의 표별 구조 옵션, GDAL-N4의 실패 시 무잔류 질문은 봉인 당시 읽은 본문에서 중복이다. 사후 회수한 최초 본문에서도 그 목적이 같음을 확인했다. 다만 실제 C를 제시한 실험은 아니므로 대화 효과율로 바꾸지 않는다. PAN-N2는 보존 의무가 애매하고 PAN-N4는 원래 번호 보존의 강도가 미확인이다. 두 경우 모두 미공개 값을 과잉 질문 아님으로 바꾸지 않고 `null`로 남겼다. GDAL-N1/N2/N3도 목적·환경 필드가 새로 확인되지 않아 과잉 여부가 미확인이다. [scores.csv](scores.csv)의 `avoidable_question_basis`가 판단 범위를 설명한다.

양성이라는 이유로 **C만 필수**라고 할 수는 없다. B가 조건과 행동을 모두 주고 독자가 값을 알고 있으면 왕복을 생략할 수 있기 때문이다. 본 연구에서 확인한 것은 GDAL-C1-A-value2의 ‘필요한 조건을 반영하지 않은 잘못된 선택’이며 ‘반드시 질문해야만 피할 수 있었던 오류’는 아니다. 자연군에서 필요한 질문 누락이 없었다는 증거도 없다. 표3의 자연군은 ‘확인0·미확인8’이다.

## Q6. 나중 발언은 값·결정·결과 중 무엇을 증명하는가

[events.csv](events.csv)는 회수한 최초 이벤트와 현재 본문의 일치를 연결한 요청8행과 후속 댓글27행, 합계35행이다. 최초 요청 행에는 실제 opened event ID와 출처를 붙였고 본문 판 차이는 별도 initial-version-review에 남겼다. 댓글이 없는 API 응답2개는 발언 행에 넣지 않고 [absence-observations](evidence/absence-observations.json)에 두었다. 실제 발언 ID, 작성·수정UTC, OP/유지보수자/제3자, 선택 필드와의 관계, 먼저 있었던 질문·조언의 ID를 연결했다. 현재 댓글의 수정 시각도 기록했으며 과거 댓글 최초판을 복원했다고 주장하지 않는다.

| 공개 사건 | 발언이 확인하는 것 | 확인하지 못하는 것 |
| --- | --- | --- |
| [PAN-N1 OP 758272588](https://github.com/jgm/pandoc/issues/7019#issuecomment-758272588) | 유지보수자의 사용 빈도 질문 뒤 기존 다중 형식 목적을 반복 | 사전 선택 필드의 새 값, 필터 적용 성공 |
| [PAN-N2 OP 1236589386](https://github.com/jgm/pandoc/issues/7022#issuecomment-1236589386) | 이전 styles.xml 검사 요청과 연결되는 w:val/w:eastAsia 진단 | literal lang 보존 질문의 실제 답, 처음 요구 전체의 성공 |
| [PAN-N2 maintainer 1237700534](https://github.com/jgm/pandoc/issues/7022#issuecomment-1237700534) | fix와 nightly 제공 계획 보고 | 정확한 commit의 공개 시험 실행 영수증, 별개 OP 성공 |
| [GDAL-N1 OP 755439157](https://github.com/OSGeo/gdal/issues/3346#issuecomment-755439157)·[755455797](https://github.com/OSGeo/gdal/issues/3346#issuecomment-755455797) | 발생원 질문에 GeoTools/EarthEngine 맥락을 답함; 제안 encoding을 시도할 계획 | 가린 목적값의 명시적 확정, 실제 적용 완료 |
| [GDAL-N2 OP 760159074](https://github.com/OSGeo/gdal/issues/3378#issuecomment-760159074) | 별도 질문 없이 EMPTY_DIR 설정을 제거하니 해결됐다는 보고 | 선택한 ENVI magic의 값, 다른 시점의 독립 성공 검증 |
| [GDAL-N3 OP 763806454](https://github.com/OSGeo/gdal/issues/3386#issuecomment-763806454) | 두 EPSG 후보 각60%라는 관측과 WKT 수정 계획 | 원 datum의 권위 있는 값, 수정 뒤 성공 |
| [GDAL-N4 제3자 771973963](https://github.com/OSGeo/gdal/issues/3427#issuecomment-771973963) | 출력 드라이버마다 실패 흔적이 달랐다는 로그 | 정확히 같은 실행판·입력, 작성자의 선택이나 성공 |

선정 필드의 **새로운 작성자 값 관측은0건**, 별개 자료로 확인한 작성자 성공도0건이다. 하지만 해결 보고 자체가 전혀 없었던 것은 아니다. GDAL-N2의 다른 필드와 해결 보고1건은 같은 댓글에 있다. 이를 ‘새 정보1건’과 ‘독립 성공1건’으로 두 번 쓰지 않았다. 다른 조언 뒤의 행동 의도는2건이고 완료가 아니다. A/B/C는 사람에게 제시하지 않았으므로 정책별 실제 선택·성공은0%가 아니라 **미측정**이다.

## Q7. 필드 하나가 충분하지 않은 반례

**고른 필드 밖에서 실패가 결정된다.** GDAL-N2의 사전 필드는 헤더의 ENVI magic이었다. 하지만 [3.2.0 헤더 발견 경로](https://github.com/OSGeo/gdal/blob/75134407dae4dff36b952c85d43f6e3e5a22f4ea/gdal/frmts/raw/envidataset.cpp#L2047-L2145)에 들어가려면 먼저 sibling header를 찾을 수 있어야 한다. 작성자는 EMPTY_DIR을 제거해 해결했다고 보고했고, [같은판 GDALOpenInfo 구현](https://github.com/OSGeo/gdal/blob/75134407dae4dff36b952c85d43f6e3e5a22f4ea/gdal/gcore/gdalopeninfo.cpp)은 그 설정 아래 현재 파일만 sibling 목록에 남기는 경로를 갖는다. 헤더를 발견하지 못하면 magic 두 값의 차이까지 도달하지 못할 수 있다. ‘기술적으로 의미 있는 질문’과 ‘그 사건의 병목을 짚는 질문’은 다르다.

**인접 단계의 값이 함께 필요하다.** [empty_paragraphs L1–33](https://github.com/jgm/pandoc/blob/dcbd8d326cce4960e0d736e25e7d00f9057a1fc2/test/command/empty_paragraphs.md#L1-L33)은 같은 AST를 docx로 쓴 뒤 다시 읽는다. 저장 기대값에서는 writer만 켜거나 reader만 켜면 빈 문단이 사라지고 둘 다 켜야 남는다. 하나의 field만 바꿔도 되는 것처럼 보이는 이름만 보고 끝까지 보존된다고 말할 수 없다. 이 시험은 반례층이며 공식 대조4쌍에 추가로 세지 않았다. 추가2.11.3.2 실행에서는 이4개 roundtrip의 결과도 저장 기대값과 정확히 일치했다.

**같은 형식·API 이름도 판과 나머지 의미가 다르면 혼입이다.** GDAL-N3의 원보고는 같은 PROJ7.2.1 아래 GDAL3.2.0/3.2.1을 비교한다. `FindMatches`의 [계약](https://github.com/OSGeo/gdal/blob/258d73a17b1f7e93c9cf9b60a2411545d51879de/gdal/ogr/ogrspatialreference.cpp#L10430-L10457)은 부분 대응을 허용한다. WGS84 ellipsoid만 보고 WGS84 datum으로 확정하는 것은 별개 주장이며, 사전 후보의3.1.4/3.2.1 혼합도 분모에서 뺐다. GDAL-N1 역시 타원체 수치 외에 datum 이름·AUTHORITY와 파일 형식의 표현 범위가 남는다. [WKT 표준 §8.2.1](https://docs.ogc.org/is/18-010r7/18-010r7.html), [GeoTIFF 표준 Class22/23](https://docs.ogc.org/is/19-008r4/19-008r4.html)은 이 의미 구분의 사후 확장 근거이며 봉인 당시 문서 예산 안에 있던 근거가 아니다.

**원하는 답이 둘 다 가능할 수 있다.** PAN-C2/GDAL-C2에서는 두 후보 명령이 공통 목적을 충족한다. 다른 분야에서도 낮은 정확도 요구는 더 정확한 변환을 금지하지 않고, CRS 정의와 재투영은 서로 배타적인 선택이 아니라 순차 단계일 수 있다. 이런 경우 하나의 값이 드러나도 옳은 후보가 반드시 하나로 줄지 않는다.

| 작업 역할·남은 일 | 공개 자료가 허용하는 다음 행동 | 완료로 치지 않은 이유 |
| --- | --- | --- |
| 변환 기능을 개발하는 작업자 | PAN-N1 FORMAT filter 구현, PAN-N3 AST/writer 전달 경로 설계 | 문서 링크에 완성 구현·회귀 통과 결과가 없음 |
| 도구 사용이 익숙하지 않은 작업자 | 입력 크기·헤더 발견·출력 조건을 확인하고 명령 선택 | 목적 용어를 이해했는지, 원자료 값을 알아낼 수 있는지 사람 자료 없음 |
| 유지보수 작업자 | 최소 재현 입력·정확 판을 받고 옵션과 드라이버별 회귀 대조 | 진단·패치 보고가 독립 사용자 성공을 뜻하지 않음 |

위 역할 표는 공개 절차에서 도출한 **작업별 분석**이다. 각 이슈 작성자의 숙련도를 측정하거나 ‘초심자’로 분류한 결과가 아니다.
