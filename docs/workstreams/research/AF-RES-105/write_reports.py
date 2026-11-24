"""Assemble the report and checklist from the sealed tables and attributed synthesis."""
from pathlib import Path
import json

P = Path(__file__).resolve().parent
sources = {s['source_id']: s for s in map(json.loads, (P / 'sources.jsonl').read_text().splitlines())}
counts = json.loads((P / 'evidence/source-counts.json').read_text())

def source_link(sid):
    s = sources[sid]
    return f'[{sid}]({s.get("immutable_url") or s["original_url"]})'

last_table = """| 가장 중요한 불일치·약점 | 다음 조사 제안·직접 열 자료 또는 실행할 입력 | 어떤 관측이면 판단을 바꿀지 |
| --- | --- | --- |
| 전체 조작의 새로움 판정 분모가 시간순0·보조0이며, 새 기능2건의 후속 실행은 미확인 | BL-N1의 [543409](https://blender.stackexchange.com/questions/313644#comment543409_313661), QG-N1의 [780200](https://gis.stackexchange.com/questions/477944#comment780200_477957) 뒤 같은 작성자가 연결한 실행 기록을 먼저 대조; 공개 기록이 더 없으면 다음 연구에서 사전 조작·직후 실행을 함께 수집 | 동일인·동일 입력·동일 변경 단계에 대해 제안 전 미인지와 제안 뒤 실행이 연결되면 해당 결합 판정에 산입 |
| 보조 모집은 닫힌 검색 가능 범위이며, ‘I tried that’은 제안 뒤 시험도 포함 | [26개 고정 질의](evidence/start/auxiliary-search-plan.json)와 [22건 원장](frame.csv)을 유지하고, 별도 사전등록한 2024 공개 댓글 모집을 새 층으로 수행 | 현재 슬롯보다 앞선 적격 진술이 새 범위에서 확인되면 범위 의존성을 인정; 기존 봉인 슬롯과 효과율은 소급 변경하지 않음 |
| 연결 파일·문서·원 사용자 판이 다르고 Blender GN 통합 fixture 두 개는403; 상류 시험은 판독만 함 | [Blender 재현](evidence/blender-official/reproduce.md)의 고정 blob/fixture 재조회와 [QGIS 재현](evidence/qgis-official/reproduce.md)의3.34 입력을 실행; BL-N1의 당시 파일·Compare 연산·각도부터 확인 | 당시 파일이 >90°/지정판과 맞거나 같은 입력의 실패가 확인되면 전체 예제 유보를 변경; 합성 현재판 성공만으로 원 사용자 채택을 인정하지 않음 |
"""

intro = """

# AF-RES-105 결과 — 익숙한 부분을 표시하고 바뀌는 단계까지 추적하기

## 판정과 사용 범위

**연구 산출물은 REVIEW_READY다. 시간순8자리와 진술4자리는 모두 실재 사건이며 결원0이다. 필수24개 구성을 채웠고, 고유1차자료32개를 보수적으로 산입했다.** 이 묶음은 후속 설계자가 따로 채택·폐기할 연구 입력이다. 제품 전체를 제외하는 정책과 조작별로 표시하는 정책 중 어느 쪽의 효과율이 높은지는 이번 자료로 산출할 수 없다. 모든 행의 `미확인`은 실패·비사용·무지의 뜻이 아니다. [재집계](evidence/reconciliation.json), [자료 수 대사](evidence/source-counts.json), [사전 계약](SCOPE.md).

세 번째 표의 `전체 신규 분자 / 판정 가능 분모 / 미확인`은 **동일한 전체 조작**에 대한 명시 인지 판정이다. 전체 조작은 대상, 연산, 입력 상태·단위, 주요 인자, 관측 결과, 판을 묶어 구분했다. 시간순은0/0/8, 보조는0/0/4이므로 비율은 **산출 불가**다. 보조의 Compare Direction과 GDAL `with` 지원은 더 좁은 기능 단위에서는 각각 신규인지가 명시되므로2건을 별도 보존했다. ‘전체 미확인’을 이유로 이 두 진술을 지우지 않았다. N은 이름·설명 언급, T는 시도, O는 관측된 결과다. 제작한 노드 그래프가 있다는 사실과 그 그래프의 평가 결과는 구분했다. [초기 원장](initial.csv), [후속 원장](followup.csv).

반환의 잠정 원칙은 **이미 아는 하위 단위를 표시하고, 제안이 바꾸는 입력·대상·인자와 정확한 문서 절을 함께 제시하는 것**이다. 그 차이를 정하는 값이 빠진 여섯 사건은 한 가지 질문으로 남겼다. 작성자에게 더 물을 필요가 없는 사실을 질문으로 바꾸지 않았고, 기능 인지가 새로워도 파일과 설명이 어긋나는 BL-N1은 전체 예제 반환을 유보했다. 이 판단은 관점별 해석이며 실제 이용자·답변자·문서 편집자를 모집해 일치도를 측정한 결과는 아니다. [반환 원장](returns.csv), [세 관점과 반대 관측](evidence/return-perspectives.json).

## 1. 모집 순서와 노출 경계

| 모집틀 | 실제로 읽은 범위 | 적격·제외 | 고정 자리·결원 | 제한 |
| --- | --- | --- | --- | --- |
| Blender 시간순 | 현재 geometry-nodes 태그, 2024-H1 생성순 첫80; q309037/01-01 11:39:17부터 q310379/01-22 22:34:36 UTC | 적격70, 제외10 | 적격순1–4위4자리, 결원0 | H1 전체·모든 GN 질문을 대표하지 않음. 현재/최초 태그 차이4건 |
| QGIS 시간순 | 현재 qgis 태그, 같은 H1 첫80; q473575/01-01 11:49:28부터 q474078/01-11 09:46:45 UTC | 적격47, 제외33 | 모집순1·3·4·7위4자리, 결원0 | 현재/최초 태그 차이16건. 설치·오류만의 요청 및 수행 조작 없는 글 등은 사유별 제외 |
| Blender 진술 | 시간순80의2024 공개 사건 + 고정 검색으로 추가11질문의 공개 사건; 닫힌 일치 발언9개 | 최초 적격 known단서3위, new4위 | BL-K1·BL-N1, 결원0 | 검색엔진 비색인·삭제 댓글·공개 API 밖은 미확인 |
| QGIS 진술 | 시간순80의2024 공개 사건 + 추가22질문의 공개 사건; 닫힌 일치 발언13개 | 최초 적격 new3위, known단서5위 | QG-N1·QG-K1, 결원0 | QG-K1의 문구는 제안 뒤 시험을 뜻함; 사전인지 양성으로 바꾸지 않음 |

모든 시간순160건의 최초판을 판독했다. 최초 생성시각과 숫자ID로 정렬했고, 페이지 경계의 동시각 확인은 별도 영수증에 남겼다. 사이트별4자리를 H1에서 얻었으므로 H2 연장은 사용하지 않았다. 현 태그로 검색한 뒤 최초 태그를 비교했기 때문에 과거에는 태그가 있었지만 지금 제거된 글의 누락 가능성은 남는다. [frame.csv](frame.csv), [Blender 판독](evidence/blender-initial/reading-notes.md), [QGIS 판독](evidence/qgis-initial/reading-notes.md), [QGIS 경계 확인](evidence/qgis-initial/boundary-check.json).

보조 검색은 미리 저장한13표현×2사이트26질의를 각각 한 번 실행했다. NFKC, 소문자, 곡선 아포스트로피 통일과 HTML entity 해제를 적용했고, 후자의 수정은 적중 본문을 판독·선정하기 전에 기록했다. 검색 결과의145개 고유URL에서139개 질문 메타데이터를 대조했다. 시간순 프레임과 겹치지 않는 추가 질문은 Blender11·QGIS22건이다. 실제 발언 생성시각·숫자ID·본문 위치로 정렬한22개 일치 사건의 제외·미선정 사유를 모두 원장에 남겼다. 풀은 **2026-11-23T23:49:08.391264Z**에 닫았다. 이 자리들은 그 닫힌 범위의 최초 적격이며, 사이트 전체2024년의 절대 최초는 아니다. [검색식](evidence/start/auxiliary-search-plan.json), [검색 반환](evidence/auxiliary/search-results.json), [닫힘 영수증](evidence/auxiliary/pool-close.json), [Blender 선별](evidence/blender-auxiliary/screening.json), [QGIS 선별](evidence/qgis-auxiliary/screening.json).

전체 원장182행은 시간순 요청160행과 보조 일치 사건22행이다. 182건을 독립 학습 사건으로 세지 않는다. 최종 선택은 서로 다른 질문12개·후보12개이며 두 모집틀의 질문 중복0이다. 시간순 BL-T1과 BL-T2는 같은 작성자64184다. 시간순의 확인된 사람ID는6명, 작성자ID 미확인 질문1건이고, 보조는4명이다. 합계는 확인된10명과 신원 미확인1자리다. QG-T1에서는 타인 제안 여부도 신원 대조로 확정하지 못했다. [별도 판독의 ID 역추적](evidence/independent-review/phase1-denominators.json), [기계 대사](evidence/reconciliation.json).

처음 읽은 root 연결시험이 BL-T1의 현재 채택ID·답 수·점수 메타데이터를 일부 노출했다. 답·후속 본문은 노출하지 않았으며 실제 최초판 판독자는 그 출력 없는 새 문맥에서 시작했다. 따라서 root의 완전 맹검은 주장하지 않는다. 최초판을 기계 투영하기 위해 API의 여러 revision을 취득한 것과 후속 본문을 모델이 읽은 것은 별개로 기록했다. QGIS 최초 적격 판정의 좁은 해석을 초기 독립 검토에서 교정한 것은 최초 묶음 봉인 전이며, 결과를 보고 순위를 고친 것이 아니다. [노출 원장](evidence/start/exposure-log.jsonl), [초기 별도 검토](evidence/start/initial-independent-review.md), [봉인 전 조정](evidence/qgis-initial/preseal-adjudication.json).

## 2. 분모를 바꾸지 않고 알 수 있는 것

| 판정 단위 | 시간순8사건·8후보 | 진술4사건·4후보 | 해석 |
| --- | --- | --- | --- |
| 전체 조작 명시 신규인지 | 분자0 / 판정0 / 미확인8 | 분자0 / 판정0 / 미확인4 | 비율 산출 불가 |
| 변경된 좁은 기능의 명시 신규인지 | 분자0 / 판정0 / 미확인8 | 분자2 / 판정2 / 미확인2 | Compare Direction·GDAL with 각각1. 문구로 모집했으므로 발생률 추정 금지 |
| 고정 제안의 작성자 시험 여부 | 판정0 / 미확인8 | 시험 보고1 / 미확인3 | QG-K1은 실패한 시험 D1. 보조에서는 진술의 지시대상 제안이며 스레드 첫 제안과 다를 수 있음 |
| 고정 제안 성공 | 분자0 / 판정0 / 미확인8 | 분자0 / 판정1 / 미확인3 | 보조 한 실패를 모든 후보의 실패율로 확대하지 않음 |
| 새로 배워 같은 조작을 이후 실행 | 분자0 / 판정0 / 미확인8 | 분자0 / 판정0 / 미확인4 | 결합 판정 산출 불가. 신규 기능2건의 후속 실행도 미확인 |

근거는 [followup.csv](followup.csv)와 [재집계](evidence/reconciliation.json)다. 현재 채택 배지·점수는 [현재 메타데이터](evidence/endorsements/current-metadata.json)와 [보조 현재 메타데이터](evidence/auxiliary-followup/current-endorsements.json)에 관측 시각과 함께 따로 남겼다. 채택 시점이 미확인이어서180일 내 행위로 소급하지 않는다. 침묵도 비사용으로 계산하지 않는다.

가장 실용적인 양성 관측은 **BL-K1의 두 번째 Align 설명은 이미 알았다는 말과, Pivot Field를 확인하지 않았다는 말의 대상이 다르다**는 점이다. 같은 답을 그대로 새 지식이라고 소개하면 과장이 된다. 반대로 ‘Align을 안다’는 이유로 답 전체를 제거하면 Pivot=Z 설명까지 없애게 된다. 다만 ‘확인하지 않았다’는 말은 ‘기능을 몰랐다’와 같지 않으므로 Pivot의 신규인지는 미확인으로 유지했다. [작성자539174](https://blender.stackexchange.com/questions/311094#comment539174_311115), [원 답311115](https://blender.stackexchange.com/questions/311094/311115#311115).

**BL-N1**에서는 반지름·호 길이 계산은 이미 했고 Compare Direction 기능은 몰랐다고 한 대상 분리가 명시적이다. **QG-N1**은 GDAL의 with 지원을 몰랐다는 진술이다. 그러나 둘 다 그 기능을 실제 적용했다는 후속은 없다. QG-N1의 OpenEx 성공·Close 발견은 with 제안보다 앞선 별도 단계다. 이 앞선 성공을 with 실행 증거로 옮기면 시간 순서가 뒤집힌다. [BL543409](https://blender.stackexchange.com/questions/313644#comment543409_313661), [QG780200](https://gis.stackexchange.com/questions/477944#comment780200_477957), [시각·지시대상 판독](evidence/auxiliary-followup/followup-part.json).

## 3. 처음 결론을 뒤집어 본 사례

‘같은 스레드에서 성공이라고 했으면 첫 추천이 통했다’는 해석은 두 곳에서 성립하지 않았다. BL-T2의 첫 가중 curve 링크에는 감사만 있고, 성공·Inverse Square Root 선호는 뒤의 Power/remap 제안에 대한 말이다. QG-K1의 첫0.5 치환에는 실패를 보고했지만, 다른 답을 `$length/0.002`로 고친 뒤 됐다고 썼다. 고정한 첫 제안을 나중 성공한 제안으로 교체하지 않았다. [BL534973·534974](https://blender.stackexchange.com/questions/309047#comment534974_309047), [QG784441](https://gis.stackexchange.com/questions/480481#comment784441_480481), [QG784443](https://gis.stackexchange.com/questions/480481#comment784443_480523).

보조 슬롯을 채운 뒤에도 반대 방향을 확인하기 위해 닫힌 풀의 뒤 사건 세 개를 별도 열었다. 이들은12자리나32개 최소량에 더하지 않았다. [대조 원장](evidence/auxiliary-counter/countercases.json).

| 추가 대조 | 직접 확인한 순서와 주체 | 어느 해석을 제한하는가 |
| --- | --- | --- |
| BL-C1 q322945 | 작성자187451은08-14에 Euler 순서를 이미 안다고 하고4.0 호환을 요구했다.08-15의 Rotate Euler+단일 Transform 답 뒤08-18에 잘 작동한다고 보고 | 이미 안다고 말한 부분이 있어도 다른 단계의 사용 보고가 가능. 다만 전체 새 조작 인지·독립 속도 측정은 미확인. [사전 말](https://blender.stackexchange.com/questions/322945#comment563323_322945), [다른 방법](https://blender.stackexchange.com/questions/322945/322995#322995), [사용 보고](https://blender.stackexchange.com/questions/322945#comment563659_322995) |
| BL-C2 q328659 |12-20 00:39:37의 Realize Instances 성공 보고가13:14:15의 다른 답과15:59:47의 levels를 몰랐다는 진술보다 먼저임 | 새 지식과 성공이 함께 있어도 ‘배워서 실행’의 시간 순서가 성립하지 않을 수 있음. [먼저 성공](https://blender.stackexchange.com/questions/328659#comment574773_328666), [나중 인지](https://blender.stackexchange.com/questions/328659#comment574826_328688) |
| QG-C1 q481552 | 작성자242921이05-20에 XYZ 재배열을 이미 시도했다고 말함.08-11의 -y 제안은 다른 사용자221706 | 이미 안다고 했다는 사실과 다른 방법 채택을 연결할 수 없음. [작성자](https://gis.stackexchange.com/questions/481552#comment785658_481556), [다른 사람](https://gis.stackexchange.com/questions/481552#comment790648_481556) |

새로 배워 같은 조작을 실행한 양성 사건을 찾으려고 BL-N1·QG-N1의180일 후속과 BL-C2의 앞뒤를 열었으나 그 결합은 확정하지 못했다. ‘이미 알고 다른 방법을 사용’하는 방향은 BL-C1의 D1 자기보고가 지지한다. 이는 원 파일·측정값으로 독립 재현한 성공이 아니다. 찾지 못한 양성을 만들어 넣거나 더 잘 맞는 뒤 사례로 봉인 슬롯을 갈아 끼우지 않았다.

## 4. 익숙한 이름과 실제 효과: 공식 판과 직접 실행의 분리

원 작성자들이 제시한 정확한 설치판은12자리 모두 미확인이다. 제안자가 명시한 Blender4.0.2(BL-T1),3.6.5(BL-N1), 문서4.0·3.6, QGIS3.34.0, GDAL3.8.4, 지금 실행한 Blender4.3.2·QGIS3.40.6/GDAL3.10.3을 각기 별도 열에 두었다. 현재 내려받은 blend의 헤더는 파일 형식 major/minor이고 `bpy.data.version`의 마지막 값은 내부 subversion이므로 설치판 patch로 바꾸지 않았다. [판별 기록](evidence/blender-followup/artifact-header-receipts.json), [보조 헤더](evidence/auxiliary-followup/blend-headers.json), [공식 판독](evidence/qgis-official/official-part.json).

| 비교 | 판·자료 | 관측 또는 상류의 기대값 | 반환에 주는 제한 |
| --- | --- | --- | --- |
| 같은 Accumulate, 다른 Selection | Blender4.0 매뉴얼; 연구자4.3.2 합성 triangle+quad | 기존 결정식과 random-index식 모두 island마다1edge; 선택 local index는0/0 대2/1 | 그룹화는 이미 해본 부분일 수 있음. 단일 seed 결과로 확률분포를 검증했다고 하지 않음 |
| 같은 GN 그룹, 다른 적용 범위 | Copy Modifiers4.0;4.3.2 native | target의 기존 Bevel stack이 source GN stack으로 교체되고 convert 뒤 두 mesh가 bake됨 | 기존 modifier를 보존해야 하는지가 전체 복사·적용의 적합성을 바꿈 |
| 같은 Align/Compare, 다른 인자 | Align Euler·Compare3.6/4.0;4.3.2 합성벡터 | Pivot Auto/Z와 Direction >90°/Not Equal0은 다른 설정이며 일부 입력의 결과가 달라짐 | node 이름을 알았다는 말만으로 이 인자를 안다고 단정하지 않음 |
| 같은 label, 다른 생성 위치 | QGIS3.34 label 구현;3.40.6 합성 선 | 200 Map Units 반복으로 ROAD5개를 얻었지만 위치별 거리 문자열은 생성되지 않음 | 반복 배치와 누적거리 값을 분리. 일반적인 거리 라벨 불가능성은 주장하지 않음 |
| 다른 label UI, 일부 같은 외관 | QGIS3.34 표현식;3.40.6 A/A/A/B 입력 | 배치만으로 A2+B1, 그룹조건으로 A1+B1. feature4개·속성·geometry는 유지 | 동일 좌표뿐인 입력에서는 비슷해 보여도 떨어진 같은 이름에서는 달라짐 |
| 같은 midpoint 기대, 다른 함수 | QGIS3.34 함수 도움말;3.40.6 합성 선 | 직선0→10에서 centroid와 길이/2 보간은(5,0)으로 같음. 꺾인 길이20에서는(7.5,2.5)와(10,0)으로 다름 | 다른 이름도 특정 입력에서는 겹치고, 다른 입력에서는 갈라짐 |
| 같은 length, 다른 단위 | QGIS3.34 도움말;3.40.6 project 단위 대조 | project를 km로 바꾸면 `$length`는0.01, `length($geometry)`는10 |0.5는 자동으로50%가 아님. 원 프로젝트 없이0.002 보정의 원인을 단정하지 않음 |
| 같은 VRT UI/API, 다른 기본값 | QGIS3.34 `buildvrt.py`와 상류 `testBuildVrt` | processing 인자 기본 SEPARATE=True이나 GUI override=False. False면 명령에서 `-separate`가 빠짐 | VRT라는 이름과 순서만으로 원 시도와 같은 연산이라고 판단할 수 없음 |
| 다른 lifetime 표기, 같은 한 입력 결과 | GDAL3.8.4 공식 절;3.10.3 연구자 GPKG | with와Close로 각각 쓴 뒤 한 feature의 POINT(3 4)를 다시 읽음. 두 파일의 binary hash는 다름 | 논리 출력 겹침은 전체 상태·모든 driver의 동등성이나 원 작성자 실행 증거가 아님 |

위 표의 실제 실행 영수증은 [Blender3개 probe](evidence/blender-official/controlled-probes-command-receipt.json), [결과](evidence/blender-official/controlled-probes-result.json), [QGIS2개 probe와 실패 시도](evidence/qgis-official/native-probe-attempts.jsonl), [결과](evidence/qgis-official/native-probe-results.json), [함수·GDAL 실행](evidence/auxiliary-official/execution-receipt.json), [입출력](evidence/auxiliary-official/probe-results.json)이다. 모두 연구자가 구성한 입력 D3이며, 원 작성자의 실행이나 과거 환경 복원으로 계산하지 않았다. QGIS 첫 probe의 enum AttributeError와 완료 실행의 AF_NETLINK 경고도 기록했다.

**BL-N1의 링크는 특별히 유보할 이유가 있다.** 답의 그림은 Compare Direction/Greater Than/90°인데 현재 연결 파일은 Direction/Not Equal/0이다. 본문은3.6.5로 저장했다고 하지만 내려받은 원·제안 파일의 헤더는400이고 내부 version은[4,0,36]이다. 현재 파일이2024 당시 파일과 같은지는 미확인이다. 파일 내용과 노드51개/21개는 autoexec를 끈4.3.2에서 구조를 읽었고 이 보조 파일의 simulation을 돌렸다고 주장하지 않는다. [원 답](https://blender.stackexchange.com/questions/313644/313661#313661), [파일 구조](evidence/auxiliary-followup/blend-inspection.json), [실행 범위 영수증](evidence/auxiliary-followup/execution-receipt.json).

GDAL의 당시 연결 주소는 현재404여서 같은 문서의 고정3.8.4 소스와 현재 새 주소를 따로 읽었다. with/Close 지원은3.8부터다. 고정 문서의 예제에는 SetGeometry 호출의 닫는 괄호가 빠져 리터럴 구문 검사가 실패했다. 이번 native 대조는 별도로 쓴 코드이며 그 문서 예제가 그대로 실행됐다는 뜻이 아니다. [고정 공식 절161–201행](https://github.com/OSGeo/gdal/blob/c2d2a61739ca770bae5a26be3eeb25a045dd3458/doc/source/api/python_gotchas.rst), [현재 공식 절](https://gdal.org/en/stable/api/python/python_gotchas.html#certain-objects-contain-a-destroy-method-but-you-should-never-use-it), [실패와 교정 범위](evidence/auxiliary-official/analysis.md).

### 상류 시험을 읽은 범위

Blender v4.0.2의 서로 다른 C++ 파일에서 axis 회전과 vector 비교의 실제 입력·예상 출력을 읽었다. 예컨대 (1,0,0)을 Z축으로π/2 회전한 기대값은(0,1,0)이다. 이들은 낮은 수준의 수학 함수 시험이며 GN Pivot integration과 동일 경로라고 주장하지 않는다. GN 회귀 blend fixture 두 개는403으로 얻지 못했고 산입하지 않았다. [BL-U1·U2와 한계](evidence/blender-official/official-part.json), [실패 응답](evidence/blender-official/acquisition.jsonl).

QGIS3.34의 `testqgsexpression.cpp`에서 array_first의 a/b/c→a 및 빈 배열→무효값 단언을 읽었다. `GdalAlgorithmsRasterTest.py`의 `testWarp`는1948행부터, `testBuildVrt`는2740행부터다. Warp target resolution10 입력의 기대 명령에는 `-tr 10.0 10.0`이 있고 None/0에서는 빠진다. 이 단위는 인자 사전→명령 문자열이며 TIFF pixel 결과 검사가 아니다. 이들 상류 C++/Python 시험은 실행하지 않았다. [QGIS 입력·기대 출력](evidence/qgis-official/upstream-examples.json), [실행 준비와 미확인 bootstrap](evidence/qgis-official/reproduce.md).

## 5. 다른 분야의 원 예제로 점검한 반례

**Calc: ‘절대’라는 이름은 모든 편집에 대해 셀이 고정된다는 뜻이 아니다.**24.2.0.3 공식 도움말은 복사에서 상대/절대 축이 달리 처리되고, 참조 대상 셀을 이동하면 두 참조가 모두 갱신되는 범위를 구분한다. 같은 판의 별도 상류 `testFormulaRefUpdate`는 A1=2를 참조하는 C3=A1과 C4=$A$1 앞에 두 행을 넣으면 각각 A3와$A$3으로 바뀌고, 참조 행 삭제에서는 둘 다 NoRef가 되는 입력·단언을 담는다. 같은 현재 값2는 다음 복사 때의 동작까지 같다는 뜻이 아니다. F4와 `$` 직접 표기는 같은 참조 형태를 만들 수 있지만 복사·이동의 적용 범위는 여전히 필요하다. [공식 설명51–66행](https://github.com/LibreOffice/help/blob/6409921048d4098f63109eeca0f0d2a4d7d7c8ae/source/text/scalc/guide/relativ_absolut_ref.xhp), [별개 원 시험1508–1713행](https://github.com/LibreOffice/core/blob/da48488a73ddd66ea24cf16bbc4f7b9c08e9bea1/sc/qa/unit/ucalc_formula.cxx).

**Audacity: 음량을 줄이는 UI들이 같은 편집 상태를 만들지는 않는다.**3.6.4 매뉴얼은 clip의 envelope control points, 전체 track Gain, 선택 sample에 적용하는 Amplify를 구분한다. envelope를 render하면 의도한 소리는 보존하되 편집 가능한 control point 상태는 달라진다. 별개 원 보고#2371의3.1.3 예제는30초 tone 중10–20초를 envelope 최저로 줄이는 경로와 그 구간을 Ctrl+L로0으로 만드는 경로에 +50dB Amplify를3회 적용했을 때의 차이를 보여 준다. 그림3개를 읽었지만 원 오디오·정확한 잔여진폭 측정값은 없다. ‘조용해 보임’을 동일한 zero sample로 간주할 수 없다는 반례로만 사용한다. [공식 envelope 절](https://github.com/audacity/audacity-manual/blob/991d4bc7a2be98840ca0e91c6e8c12a5763ea3b0/manual/man/envelope_tool.html), [원 보고2371](https://github.com/audacity/audacity/issues/2371), [그림 판독과 상태 구분](evidence/crossdomain/findings.md).

추가로#5099의3.3.3 Clip Fix가 envelope point를 움직인 보고와 두 그림을 읽었다. 매뉴얼 경고가 같은 이슈를 링크하므로 독립 재현 두 건으로 세지 않았다. Calc와 Audacity 앱 실행은 미실시다. 이 사례들은 누가 새로 알았는지의 표본이 아니며, **새 지식 여부와 무관하게 정확한 절·선택 범위·나중 편집 상태가 필요한 경우**를 보여 준다. [원 예제 계보](evidence/crossdomain/original-examples.json), [자료 수 제한](evidence/crossdomain/counting.json), [재현 입력](evidence/crossdomain/reproduce.md).

## 6. 자료 수, 보존 위치와 독립성

`sources.jsonl`은304행이다. 그중 보수적으로 산입한 서로 다른1차 저작은32개이며, 요구 구성24개와 추가8개를 나눈다. 아래 필수 구성의 URL과 판·절·해시는 모두 원장에 있고 각 행의 판독은 `reader_record`로 연결된다. 같은 사건의 최초판·답·댓글·그림·첨부를 여러 독립 사건으로 세지 않았고, 같은 문서의 여러 anchor·번역/미러·실패 응답·연구자 probe도 새1차 저작으로 더하지 않았다. 검토한 미선정 최초 요청152개는 원장에 기록했지만32개에 더하지 않는 보수적 집계다.

"""

category_names = {
    'chronological_requests': '시간순 원 요청', 'blender_official': 'Blender 공식 문서·구현',
    'qgis_official': 'QGIS 공식 구현', 'blender_upstream': 'Blender 상류 입력·단언 파일',
    'qgis_upstream': 'QGIS 상류 입력·단언 파일', 'calc': 'Calc 공식 설명+별개 원 예제',
    'audacity': 'Audacity 공식 설명+별개 원 예제',
}
min_table = '| 필수 범주 | 요구/직접 읽어 산입 | 원자료 ID·URL |\n| --- | --- | --- |\n'
for category, ids in counts['mandatory_source_ids'].items():
    min_table += f'| {category_names[category]} | {len(ids)}/{len(ids)} | ' + ' · '.join(source_link(s) for s in ids) + ' |\n'

end = """

추가8개는 보조 최초 요청4개, QGIS 함수 도움말 모음1개, GDAL Python Gotchas1개, spdep의 poly2nb 문서와 nb2lines 구현2개다. 여러 QGIS 함수 anchor는 한 모음으로만 산입했다. [sources.jsonl](sources.jsonl), [산입24개·추가8개 명세](evidence/source-counts.json), [별도 자료 감사](evidence/independent-review/source-audit.md).

모든 네트워크 취득에는 UTC·URL·상태·SHA256을 남기고 실제 텍스트/그림 판독 위치를 연결했다. 고정 Git blob과 Stack Exchange revision GUID는 불변 위치로, 현재 댓글·이슈·첨부는 수정 가능 자료로 구분했다. 원문 전체와 이미지/바이너리 캐시는 커밋하지 않았다. 커밋되는 것은 출처·해시·짧은 인용·판독·입출력·영수증이며, 캐시가 사라지면 공개 원문을 다시 취득해 지문을 비교해야 한다. 현재 첨부의 동일 URL과 해시가2024 당시 바이트까지 증명하지는 않는다. [재현 절차](reproduce.md).

## 7. 계승, 커밋과 검토 범위

AF-RES-101은 고정 연구 입력392ff3d의18후보, 제품 기준A7·조작 기준B14, B에만 남은7개 중 목적 적합·다른 실제 시도를 지지한 Typst2요청의3후보, 전체18개 사전/신규인지 미확인을 교정 출발점으로만 계승했다. 이전8요청의 재탐색, A/B 재실행, Typst 합성 실행 재시험, ImageMagick 래퍼/셸 오류 복원은 하지 않았다. [고정101결과](https://github.com/laadkke-arch/agentflow-open/blob/392ff3d651577ab6aacd65f4ed86884586b960d1/docs/workstreams/research/AF-RES-101/RESULT.md), [인수 대사](evidence/start/inherited-reconciliation-summary.json).

시작 시 실제 통합판은32b6bb32989730df78d521c29a50dbebd3289b46이었다. 계획판49f603a와 비교해 바뀐 파일은 dot-control.json뿐이며, 요구 읽기 파일·제품 브리프·계약·검사 스크립트의 blob은 같았다. 운영 의존 실제 tip은 등록된b29c25fe와 같았고 연구 입력392ff3d와의 차이는 HANDOFF 추가뿐이다. [시작 diff·blob 영수증](evidence/start/contract-read.json), [workbench manifest](manifest.json).

| 봉인 | 원격 SHA | 고정한 것 |
| --- | --- | --- |
| 규칙 |15ad66b68f974073d2a0ab880314a3130145c2c2 | 모집·동일 조작·검색·노출 규칙 |
| 묶음① |de11fb2b05c0e65cc1451826c720eebcbc3e52cd | 시간순160건·8자리·초기 시도·보조26검색식 |
| 묶음② |4a4aae107be25f71318dbb0c7b7cfa73506c5030 | 첫 제안8·보조지시대상4와 초기 지식 대응 |
| 묶음③ |242ccb21a00fb769b0bd40e54afc52f0a2f30fad | 작성자180일 후속·공식 동작·현재판 독립 실행·교차 분야·반례 |
| 묶음④ |이 RESULT.md를 포함한 결과 커밋; 실제 SHA는 최종 HANDOFF에 기록 | 독립 분모·반환표·재현·자가점검·별도 판독 |

각 묶음의 원격 확인UTC와 변경 경로는 [봉인 영수증](evidence/seals/commits.jsonl)에 있다. GitHub tree/commit/ref API의 예상 부모 lease로 게시한 뒤 git fetch·ls-remote로 확인했다. 직접 git push의 인증 실패는 성공으로 쓰지 않았다. `recalculate.py --check`는 시간순 초기8행이 묶음①과, 제안12행이 묶음②와 필드 단위로 같음을 확인한다. 뒤에 얻은 파일·후속 지식을 초기판에 소급하지 않았다. QGIS 보조 초기행의 source ID 교정 및 객체·입력·N/T/O 열 확장은 선택 변경 없이 최초판에서만 보완했고 별도 변경 내역에 남겼다. [표현 교정 내역](evidence/auxiliary/representation-corrections.json).

자기검토와 별도 에이전트 판독을 분리했다. Blender·QGIS 최초판은 각각 별도 문맥의 판독자가 읽었고, 세 번째 판독자는 초기12건 일부, 주체·시각·분모·자료 계보·최종 표를 대조했다. 그 검토자가 직접 작성한 QGIS 보조와 타 분야 부분의 재검토는 독립 판독으로 부풀리지 않는다. 외부 사람 검토, 전160건 이중 코딩, 실제 역할별 평가 실험은 미실시다. [별도 검토](evidence/independent-review/phase1-method-review.md), [수정 기록](evidence/independent-review/resolutions.json), [최종 표 검토](evidence/independent-review/final-tables-review.md).

결과와 SELF_CHECK를 먼저 커밋한 뒤, 동일 결과 SHA의 깨끗한 사본에서 명시 manifest 검사와 cloud_check를 각각 실행한다. 결과판 GitHub의 필수 표·대표 영수증·재현 절차도 다시 연다. 그 이후에만 HANDOFF를 단독 마지막 커밋한다. 실제 명령·UTC·SHA·종료값·자동 발견 세션 수·재열람 blob은 **HANDOFF의 완료 영수증**을 기준으로 한다. 이 결과 파일 작성 시점에 아직 수행하지 않은 최종 gate를 완료로 선기록하지 않는다. [SELF_CHECK](SELF_CHECK.md), [색인 제안 한 줄](INDEX_PROPOSAL.md).

## 다음 검토의 우선순위

가장 먼저 BL-N1의 당시 예제 파일과 Compare 연산·각도를 대조하면 유보 결정을 직접 바꿀 수 있다. 이어 QG-N1의 설치 GDAL 판과 with 실행 기록이 연결되면 기능 신규인지에서 실행까지의 결측을 줄일 수 있다. 공개 자료가 더 없으면 같은 사례의 침묵을 확대 해석하지 말고, 새 연구에서 사전 조작과 직후 실행을 함께 기록해야 한다. 필요한 미실시 C++·QGIS·R 명령과 합성 입력은 [재현 절차](reproduce.md) 및 분야별 문서에 있다.

"""

(P / 'RESULT.md').write_text((P / 'evidence/result-tables.md').read_text().rstrip() + intro + min_table + end + last_table)

self_check = """# AF-RES-105 SELF_CHECK

상태: **연구 범위 REVIEW_READY / 필수 자료 부족0 / 탐색완료 결원0 / 핵심 비교 미수행0**. 이는 모든 사용자 결과나 인지 상태가 확인됐다는 뜻이 아니다. 원 사용자 실행, 정확한 설치판, 과거 첨부 동일성의 미확인은 결과 자체이며 대체값으로 채우지 않았다. 직접 읽은 상류 시험 입력·단언과 현재판 연구자 실행을 비교하는 범위는 완료했다. 상류 시험 suite 실행·두 GN 통합 fixture·역사판 재현은 아래에 미실시/실패로 따로 둔다.

## Q1–Q7 자가점검

| 질문 | 답 | 직접 연 근거 URL·위치 | 판단에 반하는 경우·어디서 찾아 무엇을 확인했나 | 미확인·결론을 바꿀 최소 추가 조사 |
| --- | --- | --- | --- | --- |
| Q1 누가 어떤 결과를 시도했나 | 시간순160최초판, 적격BL70/GIS47; 첫4+4 실재·결원0. 보조4실재·중복0 | [BL-T1최초판](https://blender.stackexchange.com/revisions/22C194F7-78AB-493E-BDAF-845049EAC042/view-source) 본문·그림1/2; [QG-T2최초판](https://gis.stackexchange.com/revisions/FB7FD21E-6734-4CAB-96BA-26B0F00807B3/view-source) no20식; 전160행은[frame](frame.csv) | 초기 검토가 QGIS 구체 시도를 너무 좁게 판정한 행을 최초 봉인 전에 재판독했다. 현재/최초 태그 차이BL4/GIS16을 찾아 현재 태그 모집의 한계를 기록 | 현재 태그에서 사라진2024글은 미확인. 새로운 과거태그 프레임을 만들면 포함 범위가 바뀔 수 있으나 기존80순서는 유지 |
| Q2 최소 사전 지식 단위 | 대상·연산·입력/단위·인자·결과·판, N/T/O 분리. 원 작성자 판12미확인. BL-T3는 그룹 제작T이고 평가출력O는 미확인 | [BL-T3최초판](https://blender.stackexchange.com/revisions/76741916-EEC2-423F-8C4F-6E55997A299A/view-source) graph와 placeholder코드; [QG-K1최초판](https://gis.stackexchange.com/revisions/2E037C92-A853-4DF4-97F2-3E19A3008983/view-source) 두 함수 시도; [initial](initial.csv) | QG-T3의 GROUP BY는 아이디어N, 실행T가 아님. BL-K1둘째Align은 최초 그림에 없고 후속 회상N임. 별도 판독이 BL-T3의 T/O 과장을 찾아 최종표를 교정 | 원파일 현재byte를 최초 시도 당시로 소급하지 않음. 제안 전 그래프·입력·평가출력을 같이 찾으면 O를 바꿀 수 있음 |
| Q3 실제 첫 제안은 무엇이 다른가 | 시간순8개 모두30일 안 첫 구체 제안을 고정; 보조는 문구의 지시대상4개를 별도 고정 | [BL534953](https://blender.stackexchange.com/questions/309047#comment534953_309047) 연결296854; [QG773431](https://gis.stackexchange.com/questions/473611#comment773431_473611) 첫VRT방법; [proposals](proposals.csv) | BL-N1의 앞선313657과 진술대상313661, QG-N1의 첫OpenEx와 뒤with댓글을 분리. 같은 댓글의 VRT방법과 뒤 -tap/-tr방법도 하나로 합치지 않음 | QG-T1 작성자ID부재로 타인 여부 미확인. 사라진 선행 댓글이 확인되면 첫 제안의 관측가능성 한정을 변경 |
| Q4 명시 인지 진술은 무엇을 더 말하나 | 닫힌22적중 중4선정. BL-K1은 둘째Align기지, BL-N1/QG-N1은 좁은 기능신규2. QG-K1 known단서는 실제 사전인지 미확인 | [539174](https://blender.stackexchange.com/questions/311094#comment539174_311115); [543409](https://blender.stackexchange.com/questions/313644#comment543409_313661); [784441](https://gis.stackexchange.com/questions/480481#comment784441_480481); [780200](https://gis.stackexchange.com/questions/477944#comment780200_477957); [선별 원장](frame.csv) | ‘I tried that’이 제안 뒤 시험인QG-K1을 확인했다. 더 강한뒤known예제를 찾았지만 frozen4를 교체하지 않음. 원작성자와 다른사람·비조작감사·중복을 각각 걸렀음 | 사이트 전체 최소시각은 미확인. 26검색식밖 새수집은 별도층으로만 추가. 보조모집으로 인지발생비율 산출 불가 |
| Q5 180일 안 쓰거나 버렸나 | 고정제안 작성자실행은 시간순8미확인, 보조1실패보고·3미확인. 신규→같은실행 결합분모0 | [BL534974](https://blender.stackexchange.com/questions/309047#comment534974_309047); [QG784443](https://gis.stackexchange.com/questions/480481#comment784443_480523); [followup](followup.csv)와 각시각·주체 | 다른 제안에 대한 성공2곳을 첫제안으로 옮기지 않음. [BL-C1](https://blender.stackexchange.com/questions/322945#comment563659_322995)은 기지부분뒤다른방법사용D1; [BL-C2](https://blender.stackexchange.com/questions/328659#comment574826_328688)은 성공이새인지보다먼저. [QG-C1](https://gis.stackexchange.com/questions/481552#comment790648_481556)은다른사람말 | 감사·채택·투표·침묵은 관측그대로. 같은작성자의 후속파일·실행기록과제안의동일대상을연결하면결합분모변경 |
| Q6 이름과 실제 효과가 어긋나는가 | 같거나다른이름모두 입력·인자·범위에따라 겹치거나갈라짐. 판식별공식8·상류4읽음; 현재판독립probe 별도실행 | [Copy Modifiers4.0](https://docs.blender.org/manual/en/4.0/scene_layout/object/editing/link_transfer/link_data.html#copy-modifiers), [QGIS3.34 line_substring](https://github.com/qgis/QGIS/blob/ffbdd678812eec460ff02ff73bd36ee7955ac8a5/resources/function_help/json/line_substring), [상류VRT/Warp](https://github.com/qgis/QGIS/blob/ffbdd678812eec460ff02ff73bd36ee7955ac8a5/python/plugins/processing/tests/GdalAlgorithmsRasterTest.py) L1948/2740 | 현재판직선에서 centroid/보간동일, 꺾인선에서다름을실행. CopyModifiers가기존stack교체. BL-N1그림>90°와파일!=0불일치. GDAL문서괄호오류·옛URL404, GNfixture403도기록 | 원판/원입력미확인. 상류suite미실시; GN저수준수학시험을통합graph재현으로승격하지않음. [분야별실행준비](reproduce.md) |
| Q7 관점에 따라 반환 한 줄·절이 바뀌나 | 작성자기지부분·답변자의변경·문서의정확한절을12행에분리. 시간순 기존표시3/질문4/유보1, 보조 다른절1/질문2/유보1 | [반환12행](returns.csv), [Calc공식](https://github.com/LibreOffice/help/blob/6409921048d4098f63109eeca0f0d2a4d7d7c8ae/source/text/scalc/guide/relativ_absolut_ref.xhp) L51–66, [별개Calc원시험](https://github.com/LibreOffice/core/blob/da48488a73ddd66ea24cf16bbc4f7b9c08e9bea1/sc/qa/unit/ucalc_formula.cxx) L1508–1713, [Audacity공식](https://github.com/audacity/audacity-manual/blob/991d4bc7a2be98840ca0e91c6e8c12a5763ea3b0/manual/man/envelope_tool.html), [원2371](https://github.com/audacity/audacity/issues/2371) | 절대참조도대상행이동시갱신,같은음량외관도envelope/zero sample은다름. render로소리는같아도편집상태는다를수있음. 신규인지가없어도정확한절이필요 | 실제3역할판독자를모집한실험은미실시. 각관점은근거있는연구자해석. 다른UI범위·입력·판의반대관측이생기면해당행만변경 |

## 필수 표·분모·중복 대사

| 점검 | 관측 결과·범위 | 근거 |
| --- | --- | --- |
| 첫 표 | 시간순8+보조4=12실재; 모든 행 최초판URL·위치·미확인, 결원0 | initial.csv / RESULT 첫 표 |
| 둘째 표 | 자리별1에피소드·총12후보. 제안UTC·180일끝·같은작성자ID·후속대상 구분 | proposals.csv / followup.csv / reconciliation 시간 검사 |
| 셋째 표 | 시간순8사건8후보와보조4사건4후보 별도. 전체새로움0/0/8 및0/0/4; 좁은신규2는별도 | returns.csv / reconciliation.counts |
| 역추적 | 고유질문12·후보12·교차모집중복0. 댓글/수정사건ID 중복0. BL-T1/T2같은사람, QG-T1신원미확인 | phase1-denominators.json / recalculate.py |
| 최초판 봉인 | de11fb2의시간순8행 필드값 모두동일 | reconciliation.frozen_records.initial_changes=[] |
| 제안 봉인 |4a4aae1의12행 필드값 모두동일 | reconciliation.frozen_records.proposal_changes=[] |
| 고유1차자료 | 원장304행, 보수적산입32저작, 필수24=요청8+공식8+상류4+타분야4. 부족0 | sources.jsonl / source-counts.json / source-audit |
| 중복 제외 | 같은문서anchor·같은사건후속/첨부·미러·실패·연구자probe는새저작0. 미선정요청152도보수적으로별도 | counting·lineage와본문자료수표 |
| 반대방향 탐색 | 새로배워실행: BL-N1/QG-N1/BL-C2읽음,결합미확인. 기지뒤다른방법: BL-C1 D1양성,QG-C1타인이라제외 | auxiliary-counter/countercases.json |

## 실제 수행·실패·미실시 구분

직접 수행한 것은 최초판/제안/후속/그림/공식소스 판독, 기록된 파일 구조 조사, Blender4.3.2의3개 합성probe, QGIS3.40.6의2개 라벨probe, QGIS/GDAL 함수·수명 합성입력 실행, 원장 대사다. 실행별명령·UTC·binary판·출력·종료값은 각 `execution-receipt` 또는 `command-receipt`, `native-probe-attempts`에 있다. QGIS첫enum오류와옛GDAL404·두GN403·추정QGIS시험경로404를성공에포함하지않았다.

미실시는 Blender/QGIS/Calc 상류suite 실제빌드·실행, R/spdep 실행(R없음), Audacity 음원 재생/샘플측정, 역사판 사용자환경복원, 새인지2건의작성자실행확정, 실제세역할일치도실험이다. 완성된문서비교를넘어서는 실행의입력과명령·미확인bootstrap은 [reproduce.md](reproduce.md)에분리했다. 미실시를탐색완료결원으로부르지않는다.

## 자기 검토와 별도 판독

root가 최종해석·반환·재집계를 작성했다. 별도에이전트는 초기판12건의 부분대조, 주체/후속시각/후보결합의역추적, 자료계보/필수량, 최종표를 검사했다. Blender·QGIS 담당자는 서로분리된최초판독문맥에서80건씩읽었다. 별도감사자가작성한QGIS보조·교차분야를그감사자가다시읽은부분은자기재검토이며독립복제라고하지않는다. 외부사람검토·전160건이중판독·완전맹검은없다. [초기 검토](evidence/start/initial-independent-review.md), [분모검토](evidence/independent-review/phase1-denominators.json), [자료감사](evidence/independent-review/source-audit.md), [최종표 검토](evidence/independent-review/final-tables-review.md).

## 결과 SHA 검사 gate

이 파일과 RESULT를 먼저 커밋한 뒤 깨끗한 동일 SHA에서 아래를 수행한다. 아직 실행하지 않은 최종 gate의 성공을 이 파일에 예고 기록하지 않는다. **실제 결과 SHA·UTC·종료값·stdout 범위와 GitHub 고정판 재열람 영수증은 마지막 HANDOFF에만 확정 기록**한다. 명시 작업 manifest1개와 cloud_check가 자동 발견한 실제 세션 수를 따로 보고한다. 공통 검사가0개 발견해도 이 작업 manifest를 검사했다고 바꾸어 말하지 않는다.

```bash
python -B docs/workstreams/research/AF-RES-105/recalculate.py --check
python -B -m workbench.session check docs/workstreams/research/AF-RES-105/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

HANDOFF는 위 검사와 고정 GitHub RESULT 필수표·대표 원근거/출력·reproduce 재열람 이후에만 단독 마지막커밋으로 작성한다. 원장이나선정값을 gate통과를위해소급변경하지않는다. 소유경로밖변경과 dot-control 수정은허용하지않는다.
"""
(P / 'SELF_CHECK.md').write_text(self_check)
(P / 'INDEX_PROPOSAL.md').write_text('| AF-RES-105 | 익숙한 제품과 이미 시도한 조작의 구분: 시간순8·진술4, 신규 기능2/전체 새로움 분모0 | REVIEW_READY | [RESULT](docs/workstreams/research/AF-RES-105/RESULT.md) | AF-RES-101 운영b29c25fe / 연구입력392ff3d6 고정 |\n')
print('RESULT, SELF_CHECK and one-line INDEX_PROPOSAL written')
