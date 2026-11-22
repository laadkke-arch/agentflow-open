# 반증·대안 필드·판정 변경 최소자료

이 파일은 주 표본의 실제 사용판을 확인했다는 결론을 반박하거나, 쉬운 대체값을 골라 성공률을 올리는 오류를 막는 관측을 모은다. 모든 보조 자료는 `sources.jsonl`의 중복/배당 규칙을 따른다. 자체 재판독이며 외부 독립 판독자의 평가는 아니다.

| ID·가설 | 반대 관측과 정확한 위치 | 판정·영향 | 뒤집을 최소자료 |
|---|---|---|---|
| N-E00: 본문에 외부 필드의 계보가 약하면 소비 사례에서 제외한다 | [논문 §3](https://essd.copernicus.org/articles/14/1/2022/#section3) L260–261는 WoRMS를 실제 사용했다는 진술과 기능적 Group 출력을 함께 보임 | A01 선정 정정. 입력 필드 계보의 결측은 이후 측정값이다. 판의 보존성을 선정 조건으로 삼지 않음 | 실제 외부 자료를 사용하지 않았다는 본문 정정, 또는 Q1의 다른 명시적 적격 규칙 |
| N-E00: Amphipoda가 지금도 있으니 당시 WoRMS 값과 일치한다 | [발행자 current register](https://www.marinespecies.org/imis.php?dasid=4159&module=dataset) L61–62는 Order를 설명; [당대 자체 ZIP](https://doi.iow.de/doi/2021/data-2021-0002-01/data-2021-0002-01.zip) DOCX para35–36는 Group과 Taxa를 구별 | 현재 이름의 일치일 뿐 역사적 멤버십/필드 투입 미확인. V=false | 당대 WoRMS 파일/조회 응답과 Taxa→Group 변환 기록, 동일 실행 연결 |
| N-E00: 자체 release2가 외부 입력의 사용판이다 | [저자 archive](https://doi.iow.de/10.12754/data-2021-0002-01) Version과 내부 DOCX para10–12 | 저자 생산 출력 판과 WoRMS170 입력판은 다른 객체. U=false 유지 | WoRMS export의 고유 판/파일ID와 저자 사용 기록 |
| X-E00-OUT: 동일 숫자/분류는 같은 판을 식별한다 | v1/v2 `Raw_Single_Measurments_Factors` F5=Amphipoda, G5=Abludomelita obtusata 양쪽 같음. ZIP SHA256은 ea9918…와 a5c004…로 다름. 두 바다 합친 summary는 전 셀 값 동일 | “값 같음→동일 판” 반례. 자체 출력 보조 비교이며 주 V에 합치지 않음 | 판별력이 있는 파일 해시/판ID를 원 사용 기록과 연결 |
| X-E00-ROW: 같은 위치 숫자는 같은 행을 뜻한다 | v1/v2 `Factors Baltic Sea` B148=1 양쪽 동일, A148은 Hippeutis complanatus→Hirudinea. `Factors North Sea` B21=1 양쪽 동일, A21은 Apherusa ovalipes→Apolochus neapolitanus | 숫자와 좌표만으로 같다고 하면 서로 다른 분류 대상의 행을 혼합. 키+단위+영역 필요 | 같은 taxon 키를 사용한 대조, 행 번호를 식별자로 쓰지 않음 |
| X-E00-REGION: 파일명/설명만 바뀌었다 | 원시행7319(ID7315, Heteranomia squamula),13310(ID13306, Ophelia borealis)의 Station/Region 변경. 숫자 Q7319=0.49475003172186133, Q13310=0.27210496292069408은 같지만 Baltic→North 이동. [두 공식 ZIP](https://doi.iow.de/doi/2021/data-2021-0002/data-2021-0002.zip), `iow-edition-comparison.json` | 내용상 지역 귀속이 바뀌어 “메타데이터만” 반례. 지역별 재사용에는 유효성이 달라짐; 전체 해역 요약에는 영향 없음 | 공식 정정문으로 변경 이유 확인. 현재는 관측된 변경과 그 계산상 영향만 진술 |
| N-E01: 발행자 v3.0.0을 찾으면 소비자가 쓴 판도 특정된다 | [BCO publisher assets](https://essd.copernicus.org/articles/13/491/2021/essd-13-491-2021-assets.html) Data sets v3.0.0; [소비자 §4](https://essd.copernicus.org/articles/14/19/2022/#section4)는 Stephan2021 인용만 | P=true, U/R/V=false. 발행판 존재와 소비판은 별도 | 같은 Fig5 생성 실행의 input manifest 및 파일명/해시 |
| N-E01: 정확한 산점도 첫 점이 없으니 다른 보정식을 주 필드로 바꾼다 | [Fig5](https://essd.copernicus.org/articles/14/19/2022/#section4) T산점도에는 정량 출력이 있음. RH 보정식 Eq5는 다른 필드 | 최초 필드 T를 보존하고 정확한 점값/키 미확인. RH5.5+Z/140은 보조만 | 첫 점을 유일하게 식별하는 시각·고도·소스·값 대응표 |
| N-E02: 공식 대체 서비스면 원 RUC 판이다 | [EPA p5](https://gaftp.epa.gov/aqmg/SCRAM/models/preferred/aermod/AERMOD_Data_Resources.pdf)는 RUC 소실 설명. 현재 IGRA2.2 자료 존재는 확인했지만 export 동일성은 없음 | 접근 실패와 값 불일치 구별. 현재 IGRA로 원 입력판 성공을 채우지 않음 | RUC export와 IGRA 객체의 동일성/변환 이력, 원 저자 기록 |
| N-E02: 코드 MD5 일치면 원 분석을 확인했다 | [Zenodo5714474](https://zenodo.org/records/5714474) 코드 체크섬은 일치. stats code L21/25의 local latest glob과 L80/83/92는 입력 파일 집합/원 실행을 고정하지 않음 | 코드 객체 바이트만 확인. 입력 해시·사용 선언·실행 ID의 빈자리는 그대로 | 실제 파일 목록, 저장된 입력 바이트, 시간/실행 ID, 결과 연결 |
| N-E02: living book의 고정 CID가 원 소비 실행을 대신한다 | [현재 예제](https://howto.eurec4a.eu/merian_cloudradar.html) L72 catalog CID, L105는 Jan27, traceback은 Python3.13. 주 필드는 Jan19 | 후대 다른 실행의 성공/실패를 원 당대 분석과 합치지 않음 | 원 Jan19 분석 실행에 대한 입력 및 코드 식별 기록 |
| N-E02: median2.68과11은 값 불일치다 | [코드](https://zenodo.org/records/5714474/files/calc_mean_max_min_LWP_paper.py?download=1) L64–68은 전체 시간대 median 주석2.6817865; [소비자 §4](https://essd.copernicus.org/articles/14/33/2022/#section4) L455는 cloudy-only median11 | 필터/모집단이 달라 비교 불합격. 먼저 조건을 고정해야 함 | 같은 기간/필터/결측/반올림을 적용한 입력값과 실행 결과 |
| N-E02: 출력 DOI235의 V2가 RUC 훈련판 정정 성공이다 | [논문 §5](https://essd.copernicus.org/articles/14/33/2022/#section5) L480 및 [DOI235 metadata](https://api.datacite.org/dois/10.25326/235) | 출력 radar product의 정정 이유만 확인. 훈련 입력판/같은19일 LWP 값은 미확인 | 원/새 출력의 같은 키·변수·단위·필터 값과 원 훈련 입력 기록 |
| N-E03: 새2015–2018 값은 옛1986–1989 값의 정정이다 | [Inuvik §3·§5.2](https://essd.copernicus.org/articles/14/57/2022/)와 [PANGAEA935027](https://doi.pangaea.de/10.1594/PANGAEA.935027)의 관측 기간 | 시대 비교가 목적에 맞는 유효한 차이다. 같은 대상 시점의 판 정정과 구별 | 같은 과거14점의 수정판 또는 GNIP 원 저자 오류 정정문 |
| N-E03: n 표기 불일치를 외부 입력 오류로 단정한다 | Fig3(a) own-data n=33, caption n=34; Fig3(b) GNIP n=14 | 내부 새 자료 수 표기 문제. GNIP 정정으로 확대하지 않음 | 저자 erratum과 정확한 포함/제외 sample 목록 |

## RUC 보존본 후속 반증

2020/2021의 원 NOAA 안내와2022의 형식·station history를 실제 읽어 발행자 원문 결측 하나를 회복했다. 자세한 URL·최종 캡처·UTC·한계는 `RUC_FOLLOWUP.md`와S-E059–077에 있다. 발행자 원문 열람의 성공과 특정 입력판의 식별을 분리했다. NetCDF의 FSL1.3은 schema version으로, Wayback의2022 캡처는 문서 보존 시점으로, station history의1971 이후는 위치 이력의 유효기간으로만 사용한다. 어느 것도 저자의1994–2016 훈련 export를 특정하지 않는다.

stat2000.txt L90–91의 WMO78954 metadata와 소비자 TableA1은 그대로 숫자가 같지 않다. 부호/좌표 표기·이력 기간·실제 export 선택을 확정하지 못했으므로 접근실패도, 원 분석의 값 오류도 아니다. 주 LWP 필드를 이 metadata로 교체하지 않았다.

## 이해관계자별 필요한 정보와 사라질 수 있는 근거

| 관점 | 이 사례들에서 필요한 최소정보 | 사라지거나 혼동될 수 있는 근거 | 현재 결론 |
|---|---|---|---|
| 발행자 | 판/수정일, 파일ID/해시, 행 키·단위·기준기간, 수정 이유/이전판 연결 | 동적 WoRMS DOI와 currentyear citation; RUC 서비스 중단; archive의 잘못 해석된 상대 링크 | 객체를 계속 제공하는 것과 과거 판을 구별하게 제공하는 것은 다름 |
| 분석 작성자 | 사용한 정확 입력 객체와 대상 필드, 원 실행ID·시각·입력 목록, 필터/결측/반올림, seed/weights | local latest glob, 저장하지 않은 export, 후대 실행으로 대체된 notebook | 코드 공개만으로 원 실행이 확정되지 않음 |
| 나중에 감사하는 사람 | 서로 다른 계보의 발행자 파일과 당대 사용 기록이 같은 키/값에서 만나는 증거 | 복사본을 독립 근거로 세기; 같은 숫자지만 행/지역/시점이 다른 자료 | 독립 동시 대조의 엄격 양성은 ESSD 주3건에서0 |
| 최신값을 원하는 이용자 | 최신 수정의 사유·대상기간·목적, 이전 결과에 영향받는 필터/영역 | 과거 재현값을 무조건 최신값으로 바꾸기; 전체값 같다고 지역별 수정 무시 | IOW 지역별 재사용은 정정 검토 필요; 합친 요약은 값 유지 가능. RUC 원 소비판은 계속 보류 |

## 수행하지 못한 검사

원래 분석 실행은3건 모두 재현하지 못했다. 원 입력 파일과 실행 연결이 없으므로 현재 내려받기나 로컬 코드를 실행하는 것만으로 그 검사에 합격시킬 수 없다. 필요한 입력/첫 행동은 `runs.csv`와 `findings.md`에 사례별로 적었다. 실제 실행한 검사는 두 IOW **저자 출력판**의 셀/키 비교이며, `python -B docs/workstreams/research/AF-RES-047/collection/essd/compare_iow.py`로 다시 수행할 수 있다. 이 검사 성공을 주 입력판 검증 성공으로 세지 않는다.
