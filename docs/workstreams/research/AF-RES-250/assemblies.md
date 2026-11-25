# 두 가지 합리적 전달안 — 설계 입력 예시

공통 전제: 6 고정 사례는 각 독립 사건/기관 기록/자산 계보/규격 개정/연구 데이터이며 하나의 실험이 아니다. 사례 간 필요관계 0/15; 보완은 증거 합산/인과가 아님. 패킷은 편집자가 교체 가능; recovery index는 ID→외부 첫 원문만 별도 유지한다(삭제된 주장/요약을 은닉하여 복구했다고 세지 않음). 실제 제품 schema나 모델 성능 채택·측정 아님.

## L — first-link/reversible (개발자)

목표: 빠르게 다음 원문을 고른다. 각 항목은 id, 목적/질문, 좁은 동사, 첫 링크, 보류 이유, 철회 조건, 선택하지 않은 대안. 실제 전달 예:

- A: 트랙 별 개별 export 첫 링크/재시험 확인. #5302 원작성자는 기존 혼합 출력 문제를 제기했고 이후 같은 계정으로 재시험했다고 보고했다. #5305는 selectedOnly 인자를 전달하도록 변경하여 병합되었다. 첫 원문 https://github.com/audacity/audacity/issues/5302#issuecomment-1746468973 ; 보류/철회: 재시험에 사용한 build, PCM·출력 파일·파라미터, 독립 검증·모든 사용자 성공 미확인. 감사나 close로 대체 채택/성공 단정 금지. comment actor 불일치/수정된 원문에서 재시험 진술이 사라지면 A-report 철회; PR diff가 달라지면 A-code만 수정; 실제 PCM 검사가 실패하면 성공 추론 금지 유지.
- B: 동명이인·저작/번역/편집 역할 연결. BnF는 Dumas père와 fils에 별도 ARK를 주며 W02와 W03에서 각각 fils, père의 역할을 구분한다. W01은 한 서지에 둘을 별도로 링크한다. 첫 원문 https://catalogue.bnf.fr/ark:/12148/cb38665336s ; 보류/철회: 제목 문자열만으로 원저자 확정, 모든 판의 저작 귀속, 원고/표제면·raw MARC 확인, 동일 저자라고 병합 금지. BnF authority merge/role correction or title-page contradiction 시 해당 role edge 재개; 다른 저작·편집자 관계는 유지.
- C: 그림 원자산 참조와 실제 렌더 구분. 고정 OSM Bright style poi-level-3는 적격 school Point를 school_11에 연결한다. tile id40551996 type1 rank32 class school level 없음, atlas rect 85,123,17,17 DPR1은 334×157 안에 있다. 첫 원문 https://github.com/maplibre/demotiles/blob/601ae60796ceceda2cbd2ed3d2ea92d17a84be4b/styles/osm-bright-gl-style/style.json ; 보류/철회: 카메라 zoom≥16/overzoom, 실제 네트워크, DPR, 충돌·가시성·픽셀 재현, 최종 사용 미확인. strict sample의 3/3으로 O-I 승격 금지. style/filter/feature ID/class/metadata/index/atlas digest 바뀌면 C의 해당 edge만 재검토; rendered result 다른 경우 static claim 유지 가능, runtime claim은 별개.
- D: 역사 인용·현행 검증을 별도 판으로 저장. WCAG 2.1의 2018 Parsing 원문과 2025 2.1 note, 2024 2.2 removed 상태를 구별한다. 이전 텍스트/앵커 보존과 적용 상태가 다르다. 첫 원문 https://www.w3.org/TR/2018/REC-WCAG21-20180605/#parsing ; 보류/철회: 모든 파싱 버그가 무해함, 모든 규정에서 무조건 같은 판 적용, 테스트 도구 실제 결과를 규격 문장만으로 추론 금지. 공식 판·errata 또는 사용자가 지정한 적용판 바뀌면 current judgment 재개; 역사 인용은 원판 자체 바뀌지 않는 한 유지.
- E: 추천 링크 읽음·이해·선택·실제 사용 분리. #8793에서 기존 Reimport 버튼 사용 설명 후 공식 문서 링크가 추천되었고 같은 원작성자가 읽었다고 말했으나 설명이 불명확하고 잘못 생각했다며 명확성 요청을 유지했다. 첫 원문 https://github.com/godotengine/godot-proposals/issues/8793#issuecomment-1877111832 ; 보류/철회: 읽음 자기보고≠실제 click log, 정확히 읽은 historical stable bytes, 이해 완료, 대체 선택/실행/산출물/만족. no observed artifact != never used. 동일 actor or sequence or read claim 반증 시 E-report 재개; actual artifact 나오면 usage separately update; A의 다른 사람 retest로 보충 금지.
- F: 작성자 노동과 총노동·검수·인수를 분리. METR early data 한 행의 두 시간은 README Data Spec상 동일 작성자의 initial/post-review 작업이다. dev655 issue1 232/10분, issue2 36/0분. reviewer/acceptance join 근거는 없다. 첫 원문 https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/README.md ; 보류/철회: 0 post-review 작성자 시간 ≠ reviewer 0; 전체 팀 노동, 인수 품질, AI 효과/절감, 12행의 모집 대표성 미확인. data dictionary 또는 author/row key 반증 시 actor/time 해석 재개; 추가 reviewer logs가 있으면 total-labor hold 재개, 기존 author times 그대로 유지.

L에서 C는 첫 원문+index로 조건부 매핑까지만 복구한다. 특정 타일 feature 및 PNG dimension까지 주장하는 것은 X로 전환한다. B는 두 서지의 역할이 필요한 때 B04를 추가 열고 authority 강제 연결은 X에서. A는 보고까지만, patch 논의는 A02를 추가하는 X. D는 판 선택에 세 버전 모두 필요. E는 issue 한 문서에서 댓글 순서, F는 정의+행 두 문서가 최소. L 전달에서 강한 문장 제거 시 각 ID, 첫 원문, 보류 이유는 남겨 둔다(단 카드 자체 제거 실험에서는 ID/URL recovery index만). 

## X — conditional expansion (설계자, 반박 편집자)

L의 항목을 기본으로 다음 조건에서만 펼친다: 구현 교체/재현 요청, 판 충돌, 행위자 불일치, 고비용 또는 비가역 결정. 전체 예시에서 C는 entity(style sha+layer92), inputs(tile id40551996/type1/rank32/class/level absence), derivation token→sprite key, coordinates+pixelRatio+atlas hash, static machine parse vs live render unobserved, role/agent producer; D는 source/edition/anchor/observed date + historical state and current applicable state; A/E는 actor identity→utterance→artifact unknown; B는 authority ARK/role/edition and W01 shared record; F는 row key/actor/unit/stage/independent join missing. 상세는 packets.md. 관계는 relations.csv의 보완/독립을 읽되 hard need로 바꾸지 않는다. 각 주장별 required evidence는 packets의 필요 근거이며 다른 카드에 연결되지 않는다. 

예시 교체: C 제거 → recovery index의 C01 고정 SHA style → C02 index → C03 TileJSON → C04 PBF → C05 PNG header. 5 originals total(4 additional) 복구 후 다시 static 판단만. 화면 증거가 필요하면 별도 실행 영수증이 있어야 함. A 삭제 → E를 근거로 테스트 성공 결론을 만들지 말고 A01 issue, X에서 A02 diff; 원작성자 artifact 미확인. B 삭제 → 같은 이름의 다른 판을 D의 version relation으로 합치지 말고 B03→B04→B01→B02. 

## 복구 비용/결정

12자리 상세 removals.csv; 한 자리는 조합×제거 카드 한 개. 추가 열람 수는 최초 원문 이후 해당 조합의 좁은 결론 복구에 계획한 추가 원저작(같은 issue의 여러 댓글은 한 문서, 같은 판의 서로 다른 파일은 다른 원산출물). L 합계 5 추가, X 합계 12 추가; 총 최초 문서 각각 6개 별도. 반복 제거가 중복 원문을 재열 수 있음. C/A/B에서 L은 축소된 결론이므로 X와 같은 정보량 아님. 예상 읽기 수만이며 실제 시간/모델 정확도/사용자 행동 미측정. 필요 원문 접근 불가 시 UNKNOWN/hold, 대체 카드로 채우지 말 것.
