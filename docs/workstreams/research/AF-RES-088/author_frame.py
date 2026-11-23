"""Preserve the deterministic recruitment frame and human R0 reading notes."""
import csv, hashlib, json, gzip
from datetime import datetime, timezone
from pathlib import Path
P=Path(__file__).resolve().parent
NOW=datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
P_NOTES=[
'pipe table 중간 연속선과 헤더선 굵기/색',
'styled HTML 수식을 AsciiDoc stem 블록으로 변환',
'RMarkdown PDF의 Noto 폰트와 특수문자 렌더링',
'Pandoc PDF 코드줄 번호를 여백 안으로 배치',
'Quarto PDF Markdown 표의 위/아래 수평선 제거',
'citeproc에서 페이지 없는 인용·bibliography 보존',
'groff 정렬/탭을 보존해 txt/md로 변환',
'단일 Markdown에서 문서와 release notes를 다른 순서로 생성',
'RMarkdown→Word 이미지 폭17cm로 출력',
'Pandoc 생성 OpenDocument XML을 OdfPy 기존 element에 추가',
'Markdown 특정 named fenced Div의 텍스트 추출, HTML출력 금지',
'Quarto chunk 출력은 보존하면서 기본 접기',
'DocBook XML→HTML에서 red 역할 색상 유지; Markdown·추가XSL설치 제약',
'Lua table 변환에서 crossref label을 LaTeX table에 유지',
'일부 이미지 caption만 제거하고 가운데 정렬; 전체 implicit_figures 해제 불가',
'배포 RConnect에서 비저장소 LaTeX패키지를 포함해 실제 Rmd→PDF 수행',
'Pandoc3.2 Markdown→PDF의 표를 grid 형태로 출력',
'HTML template 문자열 변수를 Pandoc template 입력으로 전달',
'Hakyll/Pandoc Haskell API에서 GFM alert를 HTML로 변환',
'classic custom writer의 Template 반환형 오류 해결',
'YAML target언어 값에 따라 CodeBlock을 제거해 ipynb 변환',
'비대상 언어 CodeBlock 삭제 후 빈 ipynb codecell도 제거',
'Eleventy Markdown→HTML 처리 오류에서 원 입력 파일명도 출력',
'Lua/TikZ→DOCX에서 생성 이미지 바로 아래 문자열 추가',
'DocBook→Markdown 제목 옆 section ID 표시 제거',
'LaTeX 수식·label을 이미지로 만들어 DOCX에 삽입; Inline 반환형 오류',
'RMarkdown PDF·표의 아랍어 방향과 plot title 렌더링',
'Quarto Markdown→LaTeX code output의 verbatim을 Verbatim으로 변경',
'Shinyapps에서 bslib+DT Rmd→HTML의 pandoc137 오류 재현·해결',
'GitLab CI에서 실제 Java파일 집계→PDF 변환; 패키지 오류 포함'
]
def main():
    packets=json.loads((P/'r0_packet.json').read_text()) if (P/'r0_packet.json').exists() else json.loads(gzip.decompress((P/'r0_packet.json.gz').read_bytes()))
    meta=json.loads((P/'frame_metadata.json').read_text())
    jr=json.loads((P/'support/frame_jq_review.json').read_text())
    jnotes={x['question_id']:x for x in jr['frame']}
    reqs=[json.loads(x) for x in (P/'requirements_r0.jsonl').read_text().splitlines()]
    selected={x['question_id']:x for x in reqs}
    rows=[]; sources=[]
    for q in packets:
        r=q['r0']; qid=q['question_id']; tag=q['tag']; rank=q['original_rank']; sel=selected.get(qid)
        original=next(x for x in meta if x['question_id']==qid and x['tag']==tag)
        note=jnotes[qid]['r0_summary'] if tag=='jq' else P_NOTES[rank-1]
        exposure=';'.join(jnotes[qid]['exposure']) if tag=='jq' else 'R0 title/body disclosed; present function/option names are requirement history, not outcome selection'
        tags0=r.get('tags',[])
        reason='태그 첫 적격2' if sel and sel['stratum']=='natural' else '자연층 이후 첫 별도본문수정 적격2' if sel else '정해진 네 자리 이후' if rank> (7 if tag=='jq' else 12) else '자연층 이후 별도본문수정 없음'
        rows.append(dict(tag=tag,original_rank=rank,question_id=qid,creation_utc=q['created_utc'],current_tags=';'.join(q['current_tags']),r0_tags=';'.join(tags0),tag_basis='query-time tags; original tags separately retained',current_title_machine_only=original['title'],r0_title=r.get('title',''),eligible='true',eligibility_reason='실제 사용·공개 입력 또는 변환 목적/출력 있음',r0_use_summary=note,selection='included' if sel else 'eligible_not_selected',case_id=sel['case_id'] if sel else '',stratum=sel['stratum'] if sel else '',selection_reason=reason,r0_guid=r['revision_guid'],r0_number=r['revision_number'],r0_url=f'https://stackoverflow.com/revisions/{qid}/{r["revision_number"]}',body_edits_30d_metadata=q['separate_body_edits_30d'],history_records=q['history_records'],history_complete='true',frame_page=1,page1_has_more='true',exposure=exposure,answers_scores_acceptance_used='false',r1_semantics_read_before_selection='false',missing='exact posting bytes; deleted/removed-tag questions outside observable frame',reviewer='manuals subagent + root selected-case read' if tag=='jq' else 'root'))
        if tag=='pandoc':
            sources.append(dict(source_id=f'FRAME-PD-{qid}',event_id=f'SO-{qid}',kind='public question earliest preserved body',url=f'https://stackoverflow.com/revisions/{qid}/{r["revision_number"]}',version=r['revision_guid'],location='full R0 body; paragraph/pre code positions in r0_packet.json',direct_read_utc=NOW,read_time_basis='root completed direct R0 reading in three batches before R1/answers',questions=['Q2','Q3'],cases=[sel['case_id']] if sel else [],claims=['frame eligibility','solution clues exposed before answers'],confirmed=note,observer='question author statement, read by root',supports='eligible under fixed use-question criterion',refutes='candidate mismatch is not a recruitment exclusion',limitations='No image-dependent additional facts inferred; original posting bytes unverified; current tag frame',counted_primary=True,raw_sha256=hashlib.sha256(r['body'].encode()).hexdigest()))
    with (P/'frame.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (P/'support/sources_frame_pandoc.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
    print('frame',len(rows),'selected',sum(bool(x['case_id']) for x in rows),'all R0 read; no outcome fields')
if __name__=='__main__':main()
