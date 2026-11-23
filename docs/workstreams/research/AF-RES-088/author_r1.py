"""Post-seal documentary re-reading. Does not fetch or inspect answers."""
import csv, hashlib, html, json, re, subprocess
from pathlib import Path
from collect import load_revisions, utc
P=Path(__file__).resolve().parent
R0_COMMIT='42e46d5788278efa8d5b8ab0272ace48830fb477'

NOTES={
'JN1':dict(kind='input_completion_and_formatting',requirement_change=False,input_information_change=True,solution_clue_added=False,note='작성자가 중간 rev2에 FULL json을 추가하고 rev3은 재서식했다. R1에서 전체 JSON이 파싱되며 DailyForecasts 5개와 두 요청 field가 확인된다. C1 배열화와 C2 값보존은 유지. 전체 입력을 다시 요구할 필요가 줄었다.',locations='R0 p1/Query1/Query2 → R1 p1/Query1/Query2 및 마지막 FULL json code block',image_comparison='해당 없음'),
'JN2':dict(kind='identical_body',requirement_change=False,input_information_change=False,solution_clue_added=False,note='별도 본문 수정 없음. 두 이력 중 후속은 yaml 태그 추가이며 본문 R1=R0.',locations='동일 R0/R1 pre2와 마지막 p',image_comparison='해당 없음'),
'JE1':dict(kind='presentation_only',requirement_change=False,input_information_change=False,solution_clue_added=False,note='Arun이 heading/strong을 문단으로 바꾸고 코드 fence·들여쓰기와 최종 docs 분리를 정리했다. page_data와 metadata 두 조건·입출력 예의 의미는 같다. 제시된 Python snippet은 어느 판에서도 완전 실행가능 코드로 보증하지 않는다.',locations='R0 h3/h6/pre1 → R1 p1/p2/pre1/pre2',image_comparison='해당 없음'),
'JE2':dict(kind='presentation_and_copyedit',requirement_change=False,input_information_change=False,solution_clue_added=False,note='oguz ismail이 _rid 인라인 코드와 표현을 정리하고 jquery 태그를 제거했다. Documents 각 객체를 JSONL로, 내부 _rid 보존이라는 조건은 같다.',locations='R0 p2/pre2 → R1 p2/pre2',image_comparison='해당 없음'),
'PN1':dict(kind='identical_body',requirement_change=False,input_information_change=False,solution_clue_added=False,note='후속 태그 변경은 있으나 별도 본문 수정 없음. 연속선·굵기/색·2.9.2.1 보고를 그대로 유지한다.',locations='동일 첫 문단·표 code block·마지막 문단',image_comparison='출력 이미지는 요구 문장의 보조; 별도 pixel 검증 미실시'),
'PN2':dict(kind='identical_body',requirement_change=False,input_information_change=False,solution_clue_added=False,note='전체 이력 한 행으로 별도 본문 수정 없음. HTML span 수식과 AsciiDoc stem 목적 동일.',locations='동일 HTML pre1·목적 문단·실패 출력 pre2',image_comparison='수식 이미지 자체 pixel 검증 미실시; HTML/요구 문장으로 범위 판정'),
'PE1':dict(kind='image_replacement_and_embedding',requirement_change=False,input_information_change=False,solution_clue_added=False,note='작성자가 이미지 URL을 두 번 바꾸고 tarleb가 링크를 본문 이미지로 표시했다. 주목적·Markdown/PDF 경로의 문구는 그대로다. R0 이미지 접근 실패로 두 이미지의 시각적 동등성은 미확인이며 텍스트 의미 비교와 구분한다.',locations='동일 p1/마지막 p; R0 A0Wtm.png 링크 → R1 avk9k.png img',image_comparison='R0 asset shell403/web inaccessible; R1 web image endpoint found but no pixel inspection; visual equivalence unknown'),
'PE2':dict(kind='presentation_only',requirement_change=False,input_information_change=False,solution_clue_added=False,note='Shafee가 문단으로 보이던 코드 fence를 pre/code로 고쳤다. 출력 접기 목적과 sessionInfo 예는 그대로이며 code-fold는 R0부터 있던 비교 단서다. Pandoc 태그는 후속 별도 행에 추가됐다.',locations='R0 p2..p5/p8..p10 → R1 pre1/pre2; 요구 문단 동일',image_comparison='해당 없음')
}

def dump_csv(name,rows):
    with (P/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)

def main():
    now=utc()
    revs=load_revisions();qs=json.loads((P/'frame_metadata.json').read_text())
    rows=[json.loads(x) for x in (P/'revisions.jsonl').read_text().splitlines()]
    base=subprocess.check_output(['git','show',R0_COMMIT+':docs/workstreams/research/AF-RES-088/judgments.csv'],text=True)
    original=list(csv.DictReader(base.splitlines()))
    assert len(original)==32 and all(x['revision']=='R0' for x in original)
    judgments=original[:];pairs=[];sources=[];req1=[]
    (P/'evidence/r1').mkdir(parents=True,exist_ok=True)
    for row in rows:
        case=row['case_id']; qid=row['question_id'];q=next(x for x in qs if x['question_id']==qid)
        rr=sorted([x for x in revs if x['post_id']==qid and 'body' in x and x['creation_date']<=q['creation_date']+30*86400],key=lambda x:(x['creation_date'],x.get('revision_number',0),x['revision_guid']))
        r=rr[-1];body=r['body'];fp=f'evidence/r1/{qid}.html';(P/fp).write_text(body)
        r1=dict(row['r0']);r1.update(revision='R1',guid=r['revision_guid'],revision_number=r['revision_number'],revision_utc=utc(r['creation_date']),revision_url=f'https://stackoverflow.com/revisions/{qid}/{r["revision_number"]}',body_path=fp,raw_sha256=hashlib.sha256(body.encode()).hexdigest(),lf_sha256=hashlib.sha256(body.replace('\r\n','\n').replace('\r','\n').encode()).hexdigest(),direct_read_utc=now,r1_body_exposed=True,read_by='root; same reader as selected R0; reverse case order then same-format diff',evidence_location=NOTES[case]['locations'])
        r1['revision_editor']=r.get('user',{})
        if case=='JN1':
            full=[]
            for block in re.findall(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>',body,re.S):
                try:
                    d=json.loads(html.unescape(block))
                    if isinstance(d,dict) and 'DailyForecasts' in d:full.append(d)
                except json.JSONDecodeError:pass
            assert len(full)==1
            data=full[0]; f=data['DailyForecasts']
            r1['complete_input_observation']={'forecast_count':len(f),'rain_values':[x['Day']['RainProbability'] for x in f],'grass_values':[x['AirAndPollen'][1]['Value'] for x in f],'grass_names':[x['AirAndPollen'][1]['Name'] for x in f],'method':'Python parses public example and projects requested fields; not a jq execution','read_utc':now}
            r1['input_structure']='Complete JSON object with Headline and DailyForecasts array of 5; all requested fields present'
        row.update(r1=r1,r1_read_after_r0_commit=R0_COMMIT,body_bytes_changed=row['r0']['raw_sha256']!=r1['raw_sha256'],semantic_comparison=NOTES[case])
        row['revision_editors']=[{'guid':x['revision_guid'],'number':x.get('revision_number'),'utc':utc(x['creation_date']),'user':x.get('user',{}),'comment':x.get('comment'),'is_rollback':x.get('is_rollback',False),'body': 'body' in x,'title':'title' in x,'tags':'tags' in x} for x in sorted([y for y in revs if y['post_id']==qid],key=lambda z:(z['creation_date'],z.get('revision_number',0)))]
        req1.append(r1)
        sources.append(dict(source_id=f'PAIR-{case}-R1',event_id=f'SO-{qid}',kind='preserved question revision and same-format comparison',url=r1['revision_url'],history_url=row['history_url'],version=r['revision_guid'],location=NOTES[case]['locations'],direct_read_utc=now,questions=['Q1','Q3','Q5'],cases=[case],claims=['revision identity','same candidate before/after','body change vs requirement change'],confirmed=NOTES[case]['note'],observer='root; original/revision author metadata separately stored',supports='C1/C2 text unchanged; input completion JN1 distinguished',refutes='all byte changes imply changed recommendation',limitations=NOTES[case]['image_comparison']+'; strict posting bytes and actual success environment unverified',counted_primary=(row['r0']['guid']!=r1['guid']),primary_unit=f'SO-{qid}-REV-{r1["guid"]}',raw_sha256=r1['raw_sha256']))
        for old in [x for x in original if x['case_id']==case]:
            new=dict(old);new.update(revision='R1',question_revision_guid=r['revision_guid'],question_url=r1['revision_url'],question_evidence_location=NOTES[case]['locations'],read_utc=now,r1_or_answers_exposed='R1=true; answers=false',reason=old['reason']+' R1 재판독: '+NOTES[case]['note'])
            response_changed=case=='JN1' and old['candidate_id']=='JQ-map'
            if response_changed:
                new['next_minimum_input']='전체 JSON은 R1에서 확보됨. JSON 배열을 Bash의 native indexed array로 소비할지와 실제 jq판/실행 성공은 별도 확인'
                new['reason']+=' 제시된 완전 입력의 예상 배열은 rain [2,1,7,6,9], grass [12,12,13,29,69]이며 이는 데이터 투영이지 jq 실행 결과가 아니다.'
            judgments.append(new)
            comparable=old['assessment']!='미확인' and new['assessment']!='미확인'
            pairs.append(dict(pair_id=case+'-'+old['candidate_id'],case_id=case,stratum=row['stratum'],candidate_id=old['candidate_id'],r0_guid=row['r0']['guid'],r1_guid=r1['guid'],manual_sha=old['reference_sha'],r0_assessment=old['assessment'],r1_assessment=new['assessment'],r0_return_status=old['return_status'],r1_return_status=new['return_status'],paired_bodies_available='true',documentary_comparable=str(comparable).lower(),assessment_changed=str(old['assessment']!=new['assessment']).lower() if comparable else 'unknown',return_label_changed=str(old['return_status']!=new['return_status']).lower(),condition_or_next_question_changed=str(response_changed).lower(),changed_single_axis='input completeness only' if response_changed else 'none in C1/C2; '+NOTES[case]['kind'],counterexample='raw HTML changed with same requirement' if row['body_bytes_changed'] and not NOTES[case]['requirement_change'] else 'full history with identical body',missing=new['next_minimum_input'],r0_url=row['r0']['revision_url'],r1_url=r1['revision_url'],manual_url=old['manual_url']))
    (P/'revisions.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
    (P/'requirements_r1.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in req1))
    (P/'support/sources_pairs.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
    dump_csv('judgments.csv',judgments);dump_csv('pairs.csv',pairs)
    assert len(judgments)==64 and len(pairs)==32
    print('R1 complete',len(rows),'pairs',len(pairs),'documentary comparable',sum(x['documentary_comparable']=='true' for x in pairs),'condition/next-question change',sum(x['condition_or_next_question_changed']=='true' for x in pairs))
if __name__=='__main__':main()
