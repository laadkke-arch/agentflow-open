# AF-RES-167 SELF_CHECK — 같은 작업자 자기검산
고정 재열람 5b76dba5a2b1249e7732a94c0441e69180f17887. 외부 실행/빌드/재변환 없이 원격 GitHub 파일 7종을 같은 SHA에서 다시 읽고 JSONL·CSV 행/ID를 계산했다. 독립 검수 아님.

```json
{
  "fetched": 7,
  "sourceRows": 97,
  "uniqueSourceIds": 97,
  "counted": 56,
  "distinctCountedWorkIds": 56,
  "by": {
    "exchange": 38,
    "standard": 8,
    "implementation": 6,
    "MARC": 2,
    "AV": 2
  },
  "exchangeRows": 38,
  "propertyRows": 43,
  "linkRows": 7,
  "frameRows": 268,
  "named": [
    "M02",
    "M05",
    "M07",
    "M08",
    "I04",
    "I09",
    "I10",
    "M13",
    "M15",
    "I13",
    "I16"
  ],
  "strict": [
    "I10"
  ],
  "roundtrip": [],
  "errors": []
}
```

## 질문별 주장→원문 위치→원장→반증
| 질문 | 주장/미확인 | 정확한 URL과 위치 | 행·분모 | 반증 조건 |
|---|---|---|---|---|
| Q1 | 사용자가 요구한 보존은 보이는 화면과 다름; I09 추가 요구 분리 | [M08](https://github.com/musescore/MuseScore/issues/25472) 본문 instrumentation 및 첫 마디; [I09](https://github.com/IfcOpenShell/IfcOpenShell/issues/3954) 본문/후속 parametric; [M07](https://github.com/musescore/MuseScore/issues/24971) 본문 rest 및 후속 reset | M07/M08/I09 3 사례, 11 공개 명명 보고 중 | 동일 원문이 최초부터 단순 보기만 필요했다고 명시하거나 편집값 모두 직접 확인 |
| Q2 | 규약·제품 옵션·인증·실제 결과 별개, 역사판 두 절 미완료 | [S01r](https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/measure-repeat/) definition; [S02](https://standards.buildingsmart.org/MVD/RELEASE/IFC4/ADD2_TC1/RV1_2/HTML/schema/views/reference-view/index.htm) scope; [D04](https://help.autodesk.com/cloudhelp/2024/ENU/Revit-DocumentPresent/files/GUID-E029E3AD-1639-4446-A935-C9796BC34C95.htm) exporter settings; [D05](https://help.graphisoft.com/AC/24/INT/_AC24_Help/115_IFC/115_IFC-30.htm) import mapping | S01/S02/S03/S04/C03/D04/D05/D06/D07; 구현6+표준시험8 고유 원전, 목적6 중 역사 양판+관측 절 0 | 정확한 두 제품/릴리스/방향/프로필/속성별 동일 파일 결과 공개 |
| Q3 | I04만 직접 고정 전체 파일, M15 인라인 전체는 첨부 해시 미확인; I10 보고상 고정 ZIP | [I04 원파일](https://github.com/OpeningDesign/BIM_Objects/blob/e14b80573684f26940dc8542460103fa407e3f62/IFC_Objects/06%20-%20Wood%2C%20Plastics%2C%20and%20Composites/060523%20-%20W_P_C%20-%20Fastenings%20-%20IFC2X3.ifc) header/#45/#46/#120; [M15](https://github.com/musescore/MuseScore/issues/15575) 본문 XML; [I10](https://github.com/IfcOpenShell/IfcOpenShell/issues/6113) 본문 빌드 및 #5889 댓글 | 38 사례, 명명 11; exact public version+file report1; byte/두 판/수신값 직접 0 | 첨부/원소스/실제 수신 로그의 동일 지문 확인 |
| Q4 | 단위 값 직접 I04, 초기 발신/수신/설정 구분 불가 사례 있음 | [I04](https://github.com/IfcOpenShell/IfcOpenShell/issues/2053) tolerance/cache 댓글, [I02](https://github.com/IfcOpenShell/IfcOpenShell/issues/2566) HasPorts 후속, [I15](https://github.com/IfcOpenShell/IfcOpenShell/issues/3380) 30k limit, [M11](https://github.com/musescore/MuseScore/issues/13214) root edit 유지, [M06](https://github.com/musescore/MuseScore/issues/29458) 인라인 -1/-1 | I04/M15 직접 송신 텍스트 2(전체 고정 원파일1); 43 속성행, 수신값 직접 0 | 원본 및 실제 수신값의 동일성 또는 설정 변경 없이도 재현되는 반례 |
| Q5 | 자연 대조 후보 있으나 완결 왕복/엄격 자연쌍 확인 없음 | [M08](https://github.com/musescore/MuseScore/issues/25472) 본문, [I16](https://github.com/IfcOpenShell/IfcOpenShell/issues/3978) 두 exporter, [I12](https://github.com/IfcOpenShell/IfcOpenShell/issues/2913) reexport False, [M05](https://github.com/musescore/MuseScore/issues/24870) Finale 재수입/수동 편집 | 38 후보, 11 보고, 1 exact version+file report; 자연층 적격 분모 미확정, 0 완결 왕복. 교정 C01/C04 별도 | 같은 원 파일 두 소비판 결과 또는 두 송신판 같은 소비판 값, 2차 export와 최초 소비에서 요구값 |
| Q6 | 인수 검사와 규격은 별도; MARC tag-specific 교환 부족 | [A01](https://d-scholarship.pitt.edu/35264/1/Todd%2C%20Christopher%20R.%20-%20Librarian%20as%20Data%20Migrator%20-%20A%20Functional%20Pathway%20from%20Millennium%20to%20Koha.pdf) text228–252; [A02](https://cdn.ymaws.com/www.cilip.org.uk/resource/collection/9919FC08-2BB3-4138-A8A5-1AD79ED9A1FB/C%26I_193_Penny_Doulgeris.pdf) text77–108; [A03](https://repository.si.edu/server/api/core/bitstreams/b9a3c2c7-cb0d-4207-949e-7ee0ce01bc05/content) pp24–27; [A04](https://www.bfi.org.uk/features/open-reel-open-source-digital-preservation-uks-videotape-heritage/) vendor transfer/MediaConch/frameMD5 | MARC 기관2/2(원면 0/2; 태그별 두 구현 미확정), AV2/2 | 동일 기록의 필드 및 수락표가 송신 규격만으로 충분하다고 직접 입증 또는 예외 분류와 판정을 수정 |
| Q7 | 한 절은 표현 가능만; 양판/사건 링크로 조건 제한 | [M08](https://github.com/musescore/MuseScore/issues/25472) 실제 결과, [D07](https://handbook.musescore.org/en_gb/file-management/working-with-musicxml-files) 설정, [I10](https://github.com/IfcOpenShell/IfcOpenShell/issues/6113) 본문/댓글 | L01–07 7 묶음, 표3 6 목적; 역사 양판 절+직접 관측 0/6 | 해당 판의 두 구현 절과 실제 입력/출력 값이 동일 조건으로 확인 |

가장 강한 경쟁 설명: (a) I15 수신 object limit와 I02 구 질의는 파일값 손실 아닌 설정/질의; (b) M11 root는 화면만 누락/편집 중 살아 있음; (c) I04 수정 precision/cache, I09 별도 형상 샘플, M05 편집 XML은 서로 다른 파일/조건이라 자연짝 승격 금지. I18 private 파일의 두 판 보고도 공개 파일 조건에서 제외. I10 geometry 내부 직접값 미확인으로 보고 이상 승격하지 않았다. 원창 100+100은 실제 반환을 얻었지만 첫 적격 8+조건부 8 고정 및 포럼 병합 순서 미완료. 원창의 양성이 0이라고 주장하지 않음.

원전 하한 고유 56은 충족; 교환 원전은 후보 38, 공개 명명 보고 11(6+5, I13 인라인 발췌; 전체 공개 6+4), exact report 1(0+1); 직접 검증 0, 실제 하한 부족. 동일 조직/자가 5 이슈 및 C02 자체 시험 별도, 서로 다른 조직의 공동 교환 시험 0 확인. C01/C04는 독립 교정 연구 2저작. 날짜 정밀도 일자. 표 1–3 및 결측표를 수동 재독. RESULT 마지막 표 3개 약점. 원전 URL/ID의 의미 전수 독립 재검증 및 로컬 git diff/check는 수행하지 않았고 후속 작업에 남긴다.
