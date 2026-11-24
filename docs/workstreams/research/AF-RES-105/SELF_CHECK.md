# AF-RES-105 SELF_CHECK

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
