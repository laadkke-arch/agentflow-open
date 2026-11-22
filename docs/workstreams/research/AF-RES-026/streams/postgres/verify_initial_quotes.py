"""Read P04/P05 originals and first replies; retain hashes and comparison metadata only."""
import concurrent.futures, hashlib, json, re
from pathlib import Path
from datetime import datetime, timezone
from read_followups import read

P=Path(__file__).resolve().parent
initial={r['case_id']:r for r in map(json.loads,(P/'initial.jsonl').read_text().splitlines())}
reply={
 'P04':'https://www.postgresql.org/message-id/4024278.1641308516%40sss.pgh.pa.us',
 'P05':'https://www.postgresql.org/message-id/0b7219fe-2bfe-f01d-ce1b-025bfb07e24f%40matrix.gatewaynet.com'}
out=[]
for cid in ['P04','P05']:
    rows=list(concurrent.futures.ThreadPoolExecutor(max_workers=2).map(read,[{'case_id':cid,'url':initial[cid]['root_url']},{'case_id':cid,'url':reply[cid]}]))
    root,res=rows
    rps=root['read_body'];qps=res['read_body']
    norm=lambda s: re.sub(r'\s+',' ',s).strip()
    quote='\n'.join(re.sub(r'^>\s?','',line) for p in qps.values() for line in p.splitlines() if line.startswith('>'))
    substantive='\n\n'.join(rps[p] for p in (['p2','p3'] if cid=='P04' else ['p1']))
    full='\n\n'.join(rps.values())
    h=lambda s:hashlib.sha256(norm(s).encode()).hexdigest()
    substantive_quote=quote if cid=='P04' else quote.split('Thanks')[0]
    out.append({'case_id':cid,'root_url':root['url'],'root_message_id':root['headers']['Message-ID'],
      'root_submitted_utc':initial[cid]['submitted_utc'],'root_body_sha256_matches_t0':root['body_sha256']==initial[cid]['original_version']['body_sha256'],
      'first_reply_url':res['url'],'first_reply_message_id':res['headers']['Message-ID'],'first_reply_utc':res['headers']['Date'].replace(' ','T')+'Z',
      'quote_locations':'first reply p1–2' if cid=='P04' else 'first reply p2 and p7',
      'root_substantive_locations':'p2–3; greeting/thanks/signature p1,p4,p5 omitted' if cid=='P04' else 'p1 entire substantive request; p2 thanks/footer also quoted',
      'normalization':'strip one leading > and optional space per quoted line; collapse all whitespace; preserve other characters; SHA256 UTF8',
      'root_substantive_sha256':h(substantive),'first_reply_substantive_quote_sha256':h(substantive_quote),
      'substantive_equal':norm(substantive)==norm(substantive_quote),
      'entire_initial_body_equal_to_quote':norm(full)==norm(quote),
      'root_entire_whitespace_normalized_sha256':h(full),'all_first_reply_quote_sha256':h(quote),
      'observed':'첫 답의 인용에 최초 요청의 실질 내용 전체가 같은 순서/문자로 포함됨. P04 인사/서명은 생략됨.',
      'limitations':'공개 아카이브와 회신 인용의 교차 일치이며 원형 RFC822 Received나 신뢰된 타임스탬프 서명이 아님. 인용자가 알려지지 않은 초기 판을 생략했을 가능성을 논리적으로 제거하지 않음.',
      'count_in_minimum':False,'count_reason':'기존 대화 source ID의 원판 확인 보강; 새 원문 아님',
      'checked_utc':datetime.now(timezone.utc).isoformat()})
(P/'initial-quote-crosschecks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
