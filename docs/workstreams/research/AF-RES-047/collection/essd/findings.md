# ESSD 소비자 우선층 — 조사 결과와 통합 주의사항

확인 UTC: 2026-11-22. 주 사례는 **N-E00(ESSD 14,1), N-E01(14,19), N-E02(14,33)**이고, N-E03(14,57)은 최초 봉인 표본의 감도 분석으로 남긴다. `cases.json`의 `included_in_primary`로 구별한다. `readings.csv`는 4×3=12행이며 주 표본은 9행이다. 원 선정의 3×3 행과 3개 사례는 `*-before-A01.*`에 보존했다.

## Q1: 노출·선정·정정

[2022 issue1](https://essd.copernicus.org/articles/14/issue1.html)과 [issue2](https://essd.copernicus.org/articles/14/issue2.html)의 원문 연구/응용 글을 발행일, DOI 문서 식별자의 문자순으로 정렬하여 첫 30노출을 `frame.csv`에 남겼다. 첫 30번째는 2022-02-09의 `essd-14-559-2022`다. `first_opened_utc`는 이 원장에서 **목록 노출 시각**이며 본문 첫 열람은 `consumers.csv`/`sources.jsonl`에서 따로 기록한다. 첫 적격 입력을 본문 순서, 첫 대응 표/그림의 출력 필드를 표/그림 순서로 정했으며, 수치가 도형 점으로만 존재하면 그 사실과 정확값 결측을 함께 보존했다.

처음에는 1쪽 논문의 `Group`이 WoRMS의 직접 필드인지 불분명하다는 이유로 경계로 남기고 19,33,57쪽 논문을 봉인했다. 이는 선정 전에 조사 대상인 추적성 요건을 요구할 위험이 있다. [1쪽 논문 §3](https://essd.copernicus.org/articles/14/1/2022/#section3)은 WoRMS로 종명을 표준화했다는 실제 외부 자료 이용을 명시하고, Table2에 분류 결과가 있다. 부모는 **이용 여부를 Q1에서 판단하고, 특정 출력 필드의 계보는 Q3–5에서 미확인으로 남기는** A01 정정을 결정했다. 결정 통지는 WoRMS 발행자 첫 열람 22:18:24 UTC보다 앞섰지만, 원격 정정 커밋 `26a6dcb72fac3642384e8c36bb6e385120c0d982`은 그 뒤다. 엄격한 사전 원격 커밋이라고 부르지 않는다.

2번째 [5쪽 논문](https://essd.copernicus.org/articles/14/5/2022/)은 §§2–5를 읽어 자체 생산한 잎/토양 데이터가 중심임을 확인했다. 선행 방법·현장 설명·지도 인용은 있으나, 확인한 범위에서 독립된 제3자 공개 자료를 분석 입력으로 삼은 적격 사례는 확정하지 못했다. 현장 기상 관측의 생산 주체/공개성에는 불확실성이 남는다. 이 한계와 제외 근거를 원장에 유지하며, “외부 자료가 전혀 없다”로 확대하지 않는다.

## 핵심 결과

| 사례 | 고정한 입력·출력 | P: 분간 가능한 입력 발행판 | U: 소비자가 특정 입력판 사용 명시 | R: 실행과 입력 객체 연결 | V: 같은 필드의 독립 값 대조 |
|---|---|---:|---:|---:|---:|
| N-E00 | WoRMS 명칭 표준화 → Table2 Group=Amphipoda | 미확인 | 미확인 | 미확인 | 미확인 |
| N-E01 | BCO radiosonde → Fig5 기온 T(K), 첫 점의 정확 키/값 미확인 | 확인: v3.0.0 존재 | 미확인 | 미확인 | 미확인 |
| N-E02 | NOAA RUC Grantley Adams 훈련 profiles → 2020-01-19 일평균 LWP=1 g/m² | 미확인 | 미확인 | 미확인 | 미확인 |
| N-E03, 감도만 | GNIP Inuvik 1986–1989 → Fig3b, 개별 첫 점 미확인; 보조 회귀식 기울기 7.33 | 미확인 | 미확인 | 미확인 | 미확인 |

주 표본 분모 3에서 **P=1/3, U=0/3, R=0/3, V=0/3, 엄격 양성=0/3**이다. 최초 19,33,57 표본도 같은 1/3,0/3,0/3,0/3이지만 사례 구성이 같다는 뜻은 아니다. U가 있는 경우의 R 비율처럼 분모가 실제 0인 조건부 비율은 **해당 없음**이다. `publisher_object_exists`와 엄격 P는 구분했다. WoRMS 현재 자료군의 존재는 확인되지만 특정 과거 판을 구별할 수 없어 P를 올리지 않았다.

## N-E00: 같은 분류 문자열과 실제 투입 필드가 다르다

[소비자 §3, Table2](https://essd.copernicus.org/articles/14/1/2022/#section3)는 WoRMS 2021을 이용한 종명 표준화를 명시한다. 같은 문단은 `Group`이 Phylum에서 Order까지 서로 다른 계급을 섞은 기능적 요약임을 설명한다. 고정 출력은 Table2 첫 행 `Amphipoda`이며, 기능적 Group이 WoRMS의 어느 필드에서 어떻게 만들어졌는지는 확인하지 못했다. 수치 변환계수는 저자 자체 계측에서 계산되므로 외부 WoRMS 값으로 바꾸어 세지 않았다.

발행자의 [DOI170 현재 페이지](https://www.marinespecies.org/imis.php?dasid=1447&doiid=170) L45는 2026 인용을 표시하고, L67–69는 분류 관리의 성격, 매일 수정, 사본 신청을 설명한다. [About](https://www.marinespecies.org/about.php) L53,61–64는 매일 갱신과 이름의 안정된 식별자, 여러 포털 표시를 구별한다. [World Amphipoda Database](https://www.marinespecies.org/imis.php?dasid=4159&module=dataset) L61–62는 현재 Amphipoda를 Order로 설명한다. 같은 단어를 지금 찾았다는 것만으로 2021의 멤버십이나 실제 사용판은 결정되지 않는다. 별도 subregister DOI368을 소비자가 인용한 DOI170의 판 DOI로 바꾸지 않았다. [Amphipoda 페이지](https://www.marinespecies.org/amphipoda/index.php) 2020 감사 문단에는 소비자 공동저자 Michael Zettler도 있으므로, 사람 집합까지 완전히 독립적인 생산자라고 단정하지 않는다.

C에는 [저자 자체 release2](https://doi.iow.de/10.12754/data-2021-0002-01)와 [공식 ZIP](https://doi.iow.de/doi/2021/data-2021-0002-01/data-2021-0002-01.zip)을 더했다. ZIP의 `data-2021-0002-01.docx` 문단10–12는 release2, 2021-06-28, 관측 완료2020을 기록한다. 문단35의 Group은 기능적 분류이며, 문단36의 Taxa는 WoRMS가 수용한 이름이다. XLSX `Raw_Single_Measurments_Factors`의 F4=`Group`, G4=`Taxa`, F5=`Amphipoda`, G5=`Abludomelita obtusata`; A5의 고유 ID는1, B5는 `NGW8-2009-11`이다. 이 성공은 **당대 저자 출력 기록의 재독**이다. 별도 계보의 WoRMS 입력 사본 또는 실제 실행 영수증은 없다.

공식 ZIP을 두 번 내려받아 같은 SHA256을 확인한 것은 현재 반환되는 출력 파일 바이트의 일치다. 2021의 분석이 그 바이트를 읽었다는 증거가 되지 않는다. 원 DOI 경로에서 상대 링크를 따라간 요청은404였지만, 같은 서버의 루트 상대 경로를 복구하여 읽었다. 주소 접근 실패와 자료 자체 소실을 구별해야 한다.

### 자체 release1→2 보조 반례 X-E00-OUT

[release1](https://doi.iow.de/10.12754/data-2021-0002)에는 release2로 가는 `IsPreviousVersionOf` 관계가 있고, ZIP 내부 문서에는 2021-04-19가 적혀 있다. 두 ZIP/XLSX의 바이트 해시는 다르지만, **F5 Group과 G5 Taxa는 두 판 모두 같다**. 두 바다를 합친 `Factors North and Baltic Seas` 시트의 비어 있지 않은 셀 값은 모두 같았다. 반면 원시 시트에는 설명·수정일 2셀과 관측 2건의 Station/Region 4셀이 달랐다. `B7319`와 `B13310`의 OB20/OB40은 DB20/DB40으로, 같은 행 `S7319`와 `S13310`은 Baltic Sea에서 North Sea로 바뀐다. 원시 수치 자체는 이 비교에서 바뀌지 않았지만 지역별 요약이 바뀐다. 따라서 파일명/설명만 바뀐 판이라고 부를 수 없고, 합계 값이 같다는 이유로 판을 특정할 수도 없다.

`Factors Baltic Sea` B148의 숫자1은 양쪽 판에서 같지만 A148의 종명은 Hippeutis complanatus에서 Hirudinea로 바뀐다. `Factors North Sea` B21의1도 Apherusa ovalipes와 Apolochus neapolitanus를 각각 지칭한다. 행 이동 뒤 같은 숫자/셀 주소가 다른 대상을 가리키는 실제 반례이며, taxon 키로 다시 맞추면 두 종이 Baltic에서 North 요약으로 이동했음이 드러난다.

이는 **소비자가 생산한 출력의 보조 판 대조**다. WoRMS 원 입력판 대조의 성공률에 합치지 않는다. `iow-edition-comparison.json`과 `compare_iow.py`에 실제 명령·입력 URL·셀/키 비교를 보존했다. 이 검사는 원 분석 재실행이 아니며, 시트의 셀/수식을 비교한 범위를 넘어서 발표되지 않은 정정 의도를 추정하지 않는다. 첫 파서 오류는 ZIP의 빈 디렉터리 멤버를 문서로 열어 생긴 것이었고, 원격 파일 오류가 아니었다. 이 진단 오류를 정정 기록에 남긴다.

## N-E01: 발행판이 있지만 소비자 선택은 별도 사실이다

[RAAVEN §4, Fig5](https://essd.copernicus.org/articles/14/19/2022/#section4)는 BCO radiosonde와 관측 시각 차이1시간 이내, 20m 고도 간격으로 기온을 대조한다. 2020-01-24~02-16 캠페인을 당시 상태로 검토하는 목적을 고정했다. 정량 산점도가 존재하므로 선정했으나, 정확한 첫 점과 대응 관측 키는 공개 그림에서 확정하지 못했다. Fig5를 숫자가 없다고 처리하지도, 읽기 쉬운 RH 보정식으로 주 필드를 바꾸지도 않았다.

[발행자 Stephan 등 §4](https://essd.copernicus.org/articles/13/491/2021/#section4)와 [Assets](https://essd.copernicus.org/articles/13/491/2021/essd-13-491-2021-assets.html)는 L0 원시 `.mwx`, L1 품질 관리1초 자료, L2 10m 고도 격자와 v3.0.0을 구별한다. [DOI137 DataCite](https://api.datacite.org/dois/10.25326/137) 제목에서도 v3.0.0을 읽었다. 이것은 B가 A에 추가한 P 근거다. 소비자 본문은 Stephan 등2021을 인용하지만 어떤 판·level·파일을 실제 읽었는지 명시하지 않는다. 소비자의 자체 RAAVEN B1/원시 A1 보관 설명은 BCO 입력판의 근거가 아니다.

원 데이터 DOI/landing 접근은 실패했으며, C에 해당하는 BCO 입력 명세·실행 기록은 찾지 못했다. C의 추가 슬롯은 그대로 결측이다. 다음 최소 자료는 Fig5 생성에 쓰인 원시 점 대응표(시간·고도·변수)와 같은 실행에 연결된 BCO 파일 목록/판/해시다. 다른 실행이나 새로 내려받은 v3.0.0을 원 실행과 합치지 않는다.

## N-E02: 코드 바이트는 입력 파일이나 실행 영수증이 아니다

[논문 §2.1와 AppendixA](https://essd.copernicus.org/articles/14/33/2022/#appendixA)는 NOAA RUC 국제 radiosonde의 Grantley Adams 00078954에서 1994–2016년 프로파일을 사용한 ANN을 설명한다. 41,588개 중 70%인29,111개를 무작위 훈련에, 10%/20%를 검증/시험에 쓴다. Table3 첫 적용 행인2020-01-19의 일평균 LWP=**1 g/m²**를 고정했다. 입력 기간과 최종 접근일2021-12-23은 특정 배포 파일의 식별자가 아니다.

원 [RUC 주소](https://ruc.noaa.gov/raobs/intl/)는 열리지 않았고, [EPA 공식 자료 안내](https://gaftp.epa.gov/aqmg/SCRAM/models/preferred/aermod/AERMOD_Data_Resources.pdf) 2026-07 개정판 p5는2024년 가을 이후 RUC 서비스가 없어졌다고 설명한다. 현재 IGRA2.2와 station list도 보았지만 RUC의 당시 export와 동일한 자료라고 확인하지 못했으므로 대체 판으로 세지 않았다. 같은 station 번호의 현대 좌표와 논문 좌표가 다르다는 관측도 출처/관측 시점/이력 설명 없이 정정으로 판정하지 않았다.

후속 집중 탐색에서는 [원 RUC 2020-12-18 캡처](https://web.archive.org/web/20201218094634id_/https://ruc.noaa.gov/raobs/intl/)와 [원 General Information 2021-12-05 캡처](https://web.archive.org/web/20211205084551id_/https://ruc.noaa.gov/raobs/General_Information.html)를 실제 읽었다. 원 발행자는 IGRA와 GSL/GTS 병합 자료, station history에 대응 항목이 있어야 관측을 출력한다는 조건, 출력 형식/level/단위 선택을 명시한다. 형식 문서는 요청한2021 캡처에서 실제2022-07-06 캡처로 이동했으며, ASCII의0.1°C와 NetCDF의kelvin, 결측 코드/원자료 source구분을 확인했다. NetCDF 예시의 FSL1.3은 형식의 버전이며 훈련 export의 판이 아니다. 원문 열람은 회복했지만 특정 입력판 P와 사용/실행/값 판정은 그대로다.

[원 station history](https://web.archive.org/web/20220706050741id_/https://ruc.noaa.gov/raobs/stat2000.txt) L90–91에서78954를 찾았다. 역사적 유효기간이 다른 두 행의 raw fields는13.07/59.50/56(1965–1971)과13.07/59.50/47(1971이후)이다. 논문 TableA1과 숫자가 그대로 같지 않지만 캡처일, 역사적 유효기간, 좌표 표기/부호, 저자의 export 선택을 고정하지 못해 원 분석 오류로 단정하지 않는다. 훈련기준기간1994–2016의 profile 파일을 찾은 것도 아니다. 자세한 요청/최종 캡처·실패·다음 행동은 `RUC_FOLLOWUP.md`에 남겼다.

[저자 Zenodo V1](https://zenodo.org/records/5714474)의 실제 코드 두 파일을 열어 게시 MD5와 내려받은 바이트가 일치하는지 확인했다. `calc_mean_max_min_LWP_paper.py`의 L21,25는 로컬 `latest/with_DOI/daily_intake`와 glob을 사용하고, L80,83,92는 파일을 열어 `liquid_water_path`에 `np.nanmean`을 적용한다. [원 파일](https://zenodo.org/records/5714474/files/calc_mean_max_min_LWP_paper.py?download=1)에는 고정된 훈련 입력 export나 원 실행 ID가 없다. [LWP 추가 코드](https://zenodo.org/records/5714474/files/add_LWP_to_new_ncdf_files.py?download=1) L851–855도 로컬 reprocessed 경로에서 파일을 읽는다. 이 코드는 절차와 코드 객체의 동일성을 더하지만 입력판·무작위 split·seed·weights·실행을 연결하지 못한다. 코드를 실행하지 않았다.

[현재 living book](https://howto.eurec4a.eu/merian_cloudradar.html)의 고정 catalog CID와 파일 생성 시각도 확인했다. 그러나 예시는2020-01-27을 선택하고 Python3.13 실행 흔적을 보이는 후대 예다. 본 사례의 원래2020-01-19 분석 실행으로 합칠 수 없다. 고정 catalog가 있어도 실행이 다르면 원 실행의 빈자리는 남는다.

[논문 §5](https://essd.copernicus.org/articles/14/33/2022/#section5)는 자체 radar 출력 DOI156이 DOI235로 대체된 이유를 표준 후처리 버그와 LWP 신경망 데이터셋 정정으로 설명한다. DataCite의 DOI235는 V2이지만, 이는 원 RUC 입력판과 별도다. 옛/새 출력의 같은19일 LWP 실제값은 확인하지 못했으므로 정정값 일치/불일치로 세지 않았다. 같은 자료에서도 all-time median 코드 주석2.6817865와 논문의 cloudy-only median11은 필터가 달라 직접 불일치로 처리하지 않았다.

## N-E03: 최초 선택의 감도 분석 보존

[Inuvik 논문 §3·Fig3b·§5.2](https://essd.copernicus.org/articles/14/57/2022/)은 GNIP1986–1989 월별14점으로 과거선을 만들고 새2015–2018 관측과 비교한다. GNIP 첫 개별 점의 키/값은 미확인이고, 보고된 보조 회귀 기울기는7.33, 절편−3.55다. [WISER](https://nucleus.iaea.org/wiser)는 로그인 경로로 바뀌어 원 파일을 읽지 못했다. GNIP2020 인용과2021-07-04 접근일은 판 객체가 아니다.

[PANGAEA935027](https://doi.pangaea.de/10.1594/PANGAEA.935027)은 저자의 새로운2015–2018 자료이며 과거 GNIP 입력이 아니다. 새 기울기7.39/절편−6.70은 다른 대상 시점의 자료이므로 과거 값을 정정한 것으로 취급하지 않는다. Fig3(a)의 n=33과 caption의 n=34 불일치는 자체 새 관측의 표기 한계로 별도 기록하고, GNIP 값 정정으로 확장하지 않는다.

## Q4·Q7: 구성 변화와 정보 제거

A/B/C의 12행은 `readings.csv`에 있으며, 같은 논문/복사본은 독립 근거가 아니다. N-E00 C는 저자 기록 재독이고, N-E02 C는 코드 절차 재독이다. 두 경우 모두 별도 계보의 원 입력 값 검증 성공은0이다.

| 제거 정보 | 적용 사례와 원래 가능한 주장 | 제거 후 달라지는 판정 | 엄격 양성 변화 |
|---|---|---|---|
| 시간 목적·기준일 | N-E02의1994–2016 훈련/2020-01-19 출력, N-E03의 과거/현대 비교 | 현대 IGRA 또는2015–2018 GNIP 대체가 원 값 정정인지 구별하지 못함. 현재 재사용 판단 보류 | 0→0; 목적 적합성 판단이 사라짐 |
| 자료 식별자 | N-E01의 BCO와 자체 RAAVEN B1, N-E00의 WoRMS170와 자체 IOW release2 구별 | 외부 입력판 존재를 자체 출력판으로 잘못 채울 위험. 자료군 사용 주장도 불명확 | 0→0; P의 대상이 불명확해짐 |
| 실제 사용 근거 | N-E00 §3의 표준화 진술, N-E01 §4의 실제 비교 | 발행자 객체 존재만 남음. 이 분석이 자료군을 실제 썼다는 주장을 할 수 없음 | 0→0; 자료군 이용 선언 단계까지 후퇴 |
| 당시 값 | N-E00 Table2/당대 F5, N-E02 Table3의1 g/m² | 논문의 목적/자료군은 남지만 동일 출력의 재독 여부를 판단할 기준이 사라짐 | 0→0; 재독 성공도 미확인 |
| 현재 정정·변경 | N-E00 자체 원시자료 지역 변경, N-E02 DOI156→235 정정 설명 | 당시 재현의 범위는 남으나 최신 지역별 요약/LWP 재사용에서 수정 필요를 거를 수 없음 | 0→0; 현재 적합성 판단 보류 |

기록이 보완되어도 실제 이용자의 제품 추천 채택은 관측하지 않았다. 이 연구가 바꾸는 것은 기록에 기대어 말할 수 있는 문장의 범위다. 모든 주 사례의 “그 원 실행이 그 입력판의 그 값을 사용했다”는 판정은 현재 **보류**다. 저자 출력의 확인된 Group·LWP 보고값 자체는 유지하고, 잘못된 판 식별이나 최신 재사용으로의 승격은 정정한다.

## 직접 원문 수와 배당

현재 `sources.jsonl`은 77개 출처/접근 기록이다. 같은 저작의 판·파일·다른 절·재방문·접근 실패를 합쳐 최소수로 산입한 것은 **8저작**: 소비자 원문3, 발행자 자료/판 원문3(BCO, WoRMS, 보존된 원 NOAA RUC), 저자 당대 기록2(IOW release, Zenodo code)이다. WoRMS 현재 원문을 읽었다는 수는 엄격 P의 양성 수와 다른 지표다. RUC는 후속 집중 탐색에서 원 발행자 안내·형식·station history의 보존 원문을 읽어 한 저작을 추가했다. 여러 캡처/파일은 이 한 저작으로만 센다. 실제 훈련 파일/판은 여전히 확보하지 못했다. IGRA·EPA 일반 설명을 배당으로 대체하지 않았다. GNIP 논문과 보조 페이지는 최초 선택의 감도로 보존하며 주 배당을 늘리지 않는다. 통합 최소24와 분류 배당의 충족 여부는 부모의 전체 원장에서 다시 세어야 한다.

## 재개 첫 행동과 명령

- N-E00: 저자 당대 WoRMS export 또는 명칭 조회 영수증과 Taxa→Group 변환 기록을 확보한 뒤, 해당 요청/실행 ID와 입력 해시를 확인한다. 공개 접근으로는 현재 빈 슬롯이다.
- N-E01: Fig5의 원 paired-point table과 그 실행의 BCO level/파일 목록을 확보한다. DOI137 재접근은 입력값을 읽는 데 도움이 되지만 원 소비판을 자동 입증하지 않는다.
- N-E02: 원 RUC export, station/date 범위와 파일 목록, train/validation/test 구성 및 weights/seed를 확보한다. 이어 동일 실행의 radar 출력과 Table3 집계 입력을 연결한다. 현재 Zenodo 코드 실행은 로컬 파일 의존성 때문에 의미 있는 재현이 안 된다.
- N-E03: 저자가 보관한2021 GNIP Inuvik export와 monthly field keys를 확보한다. 다른 시대의 자체 PANGAEA 파일로 대체하지 않는다.

실행한 보조 비교를 다시 수행하는 명령은 저장소 루트에서 `python -B docs/workstreams/research/AF-RES-047/collection/essd/compare_iow.py`다. 두 입력은 파일 안에 명시한 공식 release1/release2 ZIP URL이다. 소스 ZIP은 메모리에서만 읽고, 해시·선택 셀·차이 요약만 owned path에 쓴다. 이는 원 소비 분석 실행이 아닌 저작자 출력판의 비교다. HTTP 응답이 실패하면 파일 값 불일치로 판정하지 않는다.

자체 재판독은 원문·ZIP·코드를 다시 읽은 조사자 검사다. 외부 독립 판독자 평가나 실행 재현을 수행했다고 주장하지 않는다. 부모는 통합 결과 고정 SHA에서 필수 표와 수용 원장을 재열람해야 한다.
