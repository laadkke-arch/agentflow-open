"""Record four pre-registered judgments; unknown is not a false contact."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'evidence/table-data.json'
tables=json.loads(path.read_text())
rows=[]
for case in ['B01','B03']:
    for baseline in ['I','C']:
        initial=baseline=='I'
        pdf=case=='B01'
        row={
            'judgment_id':case+'-'+baseline,'case_id':case,
            'baseline':'최초안' if initial else '기존 코드',
            'baseline_definition':('최초 남은1996 제안; hz노출 전 원안은 미확인' if initial else '0.12h 보존코드 및1998 구현보고→0.14f; 최초안과 다른 질문') if pdf else ('최초 남은0.0.1/0.1.0은 MusiXTeX; 최초 미공개 원안은 미확인' if initial else '같은 flat의0.1.22→0.1.23; 이전 코드도 이미Schubert를 인용'),
            'exact_donor':'미확인',
            'exact_donor_evidence':'B01-P001 pp117–118 refs40/43; B01-P006 p34,pp49/54/56–57; ROOT-R007 catalog Zapf93' if pdf else 'B03-L001 fonts.docL11–23, feta-toevallig.mfL11–14; ED001III;ED003 NSA IV14b196–218;ED007/008 currentpublisher samples',
            'exact_donor_missing':'URW1993 영어 원판과 Zapf1993 본문 직접 대조; 사용판·최초독서의 식별' if pdf else '저자 사용 Schubert/Müller의 정확 판·쇄·쪽·기호; 현행샘플의 당시판 동일성',
            'available_then':'참' if pdf else '미확인',
            'available_then_evidence':'B01-P006p34의1993영어책자 출판관계;ROOT-R007의Zapf1993서지.1996제안보다이른 저작존재를 확인' if pdf else 'ED001/002/003/004는Schubert1988판계열 존재;Müller정확판연도 미확인. B03-L018은수신0.1.23공개상한1997-10-20이며donor독서증거는아님',
            'author_citation':'참',
            'author_citation_evidence':'B01-P001§4p38: hz출판물영감+구현정보부재;2000회고한계통' if pdf else 'B03-L011/012L2–5: flat귀속Schubert→Müller;B03-L001L11–14기호별명명;당대주석',
            'author_link':'미확인',
            'author_link_missing':'정확원문의규칙을읽고같은기준선선택을바꿨다는날짜있는직접연결. 포괄적영감과구별',
            'change_same_baseline':'미확인' if initial else '참',
            'change_same_baseline_evidence':('B01-P004p248에이미폭축/문단줄바꿈제안;그보다앞선대안·첫독서선후미확인' if initial else 'B01-P012 primitive/line_break부분→B01-P013L5108–5129,5460–5469;B01-P005p288후처리와P001pp69–71단계비교') if pdf else ('B03-L026musix20·L002musix20/16은구현기준선;독서전최초형태원안미확인' if initial else 'B03-L011L119–167→L012L114–205,같은Flat/-1/flat유지·함수와비율재작성'),
            'same_purpose_reflection':'참',
            'same_purpose_reflection_evidence':'문단줄맞춤목적유지;B01-P013정적소스+P001pp69–71/P003pp146–148설명. P005Fig1/P014Fig2는각논문내저장출력쌍' if pdf else 'flat기보의미와생성호출유지;B03-L001/011/012정적소스. L016Fig5/L017slide9는후대저장출력으로별도',
            'verification_scope':'작성소스 직접관측;저자설명;저장출력 직접판독(서로다른시점);역사실행없음',
            'strict_chain_status':'미확인',
            'complete_count':'0',
            'case_denominator':'1',
            'primary_grade':'같은 기능 반영까지',
            'after_counter_grade':'같은 기능 반영까지; 동일 최초 결정의 인과는 미확인',
            'retrospective_allowed_grade':'포괄적영감+동일기능반영;정확판·같은최초안인과미확인' if pdf else '당대출처명명+코드반영;후대형상설명추가에도정확판·첫독서미확인',
            'code_baseline_sensitivity':'기존코드동일기능변경은참;다섯접점엄격완결은0/1',
            'publisher_family_sensitivity':'계열일치를허용해도첫독서·동일최초안변경연결미확인;엄격분자에추가안함',
            'deleted_contact':'author_link' if pdf else 'exact_donor',
            'deletion_operation':'P001p38연결발언을제외하고기능소스·설명을다시읽음' if pdf else '정확원판접점을제외하고당대출처명명·코드변화를다시읽음',
            'deletion_grade':'미확인: 기능대응은남으나hz영감귀속은보류' if pdf else '같은 기능 반영까지: 이미미확인인접점제거라강도불변',
            'deletion_complete_count':'0',
            'deletion_interpretation':'완결0불변은견고성입증이아님;부족한접점삭제를조건완화로사용하지않음',
            'counter_sources':'B01-P001p38;P004p248;P006p38/p54;P008p75;P010Objections1–3;ROOT-R004' if pdf else 'B03-L001L25–27;L020L18–46;L021;L022;ED001III;ED010p14;ROOT-R001p12;ROOT-R002pp5–6',
            'first_exposure':'미확인','current_explorer_retrievability':'미확인',
            'next_minimum_source':'URW1993영어책자/ZapfEPODD6(3)283–288;1996제안전후날짜있는독서·변경메일' if pdf else '1997이전MüllerFH6064/6065간기+flat/double-sharp쪽;0.1.22→23패치설명/메일;SchubertBA5527IV14b196–218',
            'source_ids':'B01-P001;B01-P003;B01-P004;B01-P005;B01-P006;B01-P008;B01-P010;B01-P012;B01-P013;B01-P014;ROOT-R004;ROOT-R007' if pdf else 'B03-L001;B03-L002;B03-L011;B03-L012;B03-L016;B03-L017;B03-L018;B03-L020;B03-L021;B03-L022;B03-L026;ED001;ED003;ED004;ED007;ED008;ED010;ROOT-R001;ROOT-R002',
            'review_kind':'같은 작업의 자체점검;독립인간검증아님',
        }
        rows.append(row)
tables['judgments']=rows
path.write_text(json.dumps(tables,ensure_ascii=False,indent=2)+'\n')
print('four judgments recorded; strict initial 0/2; strict code 0/2; function reflection 2/2')
