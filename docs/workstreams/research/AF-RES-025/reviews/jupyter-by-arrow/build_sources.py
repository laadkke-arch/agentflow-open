"""Build audit-source records and cost receipts; not a discovery replay."""
import collections
import datetime
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[1]
packets = [json.loads(x) for x in (BASE/'blind/jupyter.jsonl').read_text().splitlines()]
source_by_url = {s['source_url']:s for p in packets for s in p['sources']}
calls = [json.loads(x.read_text()) for x in sorted((OUT/'receipts').glob('RVJ-*.json'))]
by_id = collections.defaultdict(list)
for c in calls:
    by_id[c['source_id']].append(c)

# Only passages actually displayed and read in this reviewer session.
observations = {
 'RVJ-001': ([], '독립 원문 재확보 실패. 웹 열람은 403 또는 내용 없는 repository HTML, 동일 URL HTTP GET은 PDF 대신 HTML이었다.', '판정은 봉인 패킷의 원문 관측에 의존한다. 비규범판이라는 지위가 탈락 사유는 아니다.'),
 'RVJ-002': (['§4.1.2 L116–120','§4.3–4.3.1 L136–158','§6 L162–167'], '202, callback challenge 검증, 콘텐츠 POST를 분리한다. subscriber의 echo 송신이 hub의 검증 완료를 관측하는 신호는 아니다.', '2016-11-24 Working Draft의 설계 관계만 판독했다. 구현 배포 또는 최종 권고와의 관계를 조사하지 않았다.'),
 'RVJ-003': (['Event listening L400–402','server.address() L413–431','server.listen(port) L557–568'], '실제 바인딩 이후 listening 이벤트와 bound address 조회가 가능하다. 포트 0은 OS가 배정한다.', 'main의 불변 commit/tag를 새로 고정하지 않았다. 다른 절에서 보인 BoundSocket 기능을 원 반환에 추가하지 않았다.'),
 'RVJ-004': (['subprocess.send L1218–1271','Sending a server object L1272–1314'], '자식의 process.send와 부모 message 수신이 구별되며 열린 server handle 전달 예제가 있다. send callback은 수신 완료 신호가 아니다.', 'v25.8.0의 현재 사용 관계다. 다언어 전달·지속 manifest 및 당시판 지원은 확인하지 않았다.'),
 'RVJ-005': (['§7.1 L511–518','§7.1 L550–555; p9–10'], '서버가 동적 포트를 bind한 뒤 파일·URI·IPC로 클라이언트에 알리는 관계가 명시된다.', '원 패킷의 §6 표제는 틀리고 해당 쪽·행은 §7.1이다. 여러 커널·채널의 명명·갱신 계약까지 설명하지 않는다.'),
 'RVJ-006': (['Kernel.execute_request L3506–3578','Kernel.do_execute signature L3643–3667'], '같은 요청에서 content.code와 root metadata를 분리하고 지원하는 do_execute 인자에 cell_meta를 전달한다.', '파일의 metadata 자동 전송 및 모든 하위 kernel의 해석은 보장하지 않는다. main과 최초 제안의 역사적 계보는 열지 않았다.'),
 'RVJ-007': (['§16.5.1.1 L669–692','§16.6 L990–1007','§16.6.1.1–3 L1138–1210','Kernel provisioning L475–582','§16.6.2 L1211–1216 (audit-only locator beyond original subsection)'], 'form의 타입·선택값·기본값·범위와 template 치환을 제공하지만 사용자 kernel.json 및 Launcher 항목을 생성한다.', '동일 페이지의 최신 반환에서 행 번호가 2줄 이동했다. audit-only §16.6.2를 원 인용에 추가하지 않았고 P3는 원 §16.6 및 provisioning 절로 판정했다. HPC 도입 비용과 당시판은 미검증이다.'),
 'RVJ-008': (['Schema Definition L438–476','Template Variables L479–497','Environment Variables L509–527'], 'tool schema의 type/default/required와 args/env 치환을 확인했다.', '사용자에게 입력을 요청하는 client 경계 및 enum 검증은 이 절에서 확인되지 않았다. 문서명 JSON Schema만으로 전체 구현 준수를 추론하지 않는다.'),
 'RVJ-009': (['Tools with Arguments L440–515'], '동적 인자, template 대입, executeWithArguments 및 자동 schema 검증을 설명한다.', 'user input이 가능하다는 문장과 사용자에게 실제로 묻는 흐름은 다르다. enum 지원과 고정 release는 확인하지 않았다. CTX 문서와 같은 제품 계보다.'),
 'RVJ-010': (['Guaranteed Delivery printed p52–54; parser P51–53 L1713–1781'], 'READY는 publisher가 필요한 수의 ACK 연결을 관측하는 callback이며 보장에는 1입력 블록:1출력 블록 전제가 있다.', '같은 client가 입력 publisher와 출력 subscriber를 겸할 수 있으나 그 대응이 원 제안에서 완성되었다고 추론하지 않았다. 가변 개수 셀 출력에 대한 보장은 미확인이다.'),
 'RVJ-011': (['Subscription overview L102–106','Subscription workflow L107–114','Default subscription properties L131–141'], '생성 이후 발행분의 제공과 전달 이후 처리 ACK를 구별한다.', '생성 완료를 관측하는 API 응답 및 첫 실행과의 순서를 이 개요만으로 확정하지 않는다. 별도 pubsub-basics 패키지에는 이 감사를 합쳐 보강하지 않았다.'),
 'RVJ-012': (['Document/execution association L37–48','Notebook/backend execution L87–96','Extension and hooks L125–140'], 'notebook의 backend 매핑, HTTP 실행 경로 및 실행 hook을 분리해 설명한다.', 'startup config·cell identity·observability를 임의의 per-cell metadata 입력 전송과 같게 보지 않았다. 문서의 추가 backend 제품명은 새 후보로 사용하지 않았다.'),
 'RVJ-013': (['JavaScript Resource Extension Interface L114–170'], '서버 handler가 요청별 params와 별도 body input을 받아 읽으며 input 문서는 불변이다.', '실행되는 것은 설치된 module이다. 요청 body에 담긴 셀 소스를 실행하는 adapter의 존재는 이 절로 입증되지 않는다.'),
}
sources=[]
for sid in sorted(by_id):
    group=by_id[sid]
    u=group[0]['url']; original=source_by_url[u]
    sections,verified,limits=observations[sid]
    questions=sorted({p['question_id'] for p in packets if any(s['source_url']==u for s in p['sources'])})
    sources.append({
      'source_id':sid,'title':original['title'],'source_url':u,
      'version':original['version'],
      'published_or_revised':original.get('published_or_revised','not established; version label from blind packet'),
      'checked_utc':max(c['completed_utc'] for c in group),
      'sections_read':sections,'verified_content':verified,'limitations':limits,
      'producer':original['producer'],
      'lineage_id':'ctx-tool-argument-docs' if sid in ('RVJ-008','RVJ-009') else 'blind-original:'+original['source_id'],
      'count_in_minimum':False,
      'count_reason':'Audit reopening of an already counted candidate original; do not inflate external unique-source minimum.' if sections else 'No original body obtained; failed exploration only.',
      'related_questions':questions,'packet_source_ids':[original['source_id']],
      'direct_original_body_read':bool(sections),
      'read_receipts':['receipts/'+c.get('receipt_id',c['source_id'])+'.json' for c in group],
      'new_return_evidence':False,
    })
(OUT/'sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')

inputs=[]
repo=BASE.parents[3]
for q in sorted({p['question_id'] for p in packets}):
    packet=next(p for p in packets if p['question_id']==q)
    spec=packet['question']; f=repo/spec['input_path']; b=f.read_bytes()
    observed=hashlib.sha256(b).hexdigest();assert observed==spec['input_sha256']
    inputs.append({'question_id':q,'input_path':spec['input_path'],'expected_sha256':spec['input_sha256'],'observed_sha256':observed,'lines_read':'complete text','line_count':len(b.decode().splitlines()),'initial_url':spec['initial_url']})
(OUT/'receipts'/'initial-inputs.json').write_text(json.dumps(inputs,ensure_ascii=False,indent=2)+'\n')
summary={
 'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'tool_web_open_calls':sum(c['request'].get('open') is not None for c in calls),
 'http_get_calls':sum(c['request'].get('method')=='GET' for c in calls),
 'total_audit_retrieval_calls':len(calls),
 'unique_original_urls_attempted':len({c['url'] for c in calls}),
 'unique_original_urls_read':sum(s['direct_original_body_read'] for s in sources),
 'failed_retrieval_calls':sum(c['error_observed'] for c in calls),
 'sum_individual_retrieval_wall_ms':sum(c['wall_ms'] for c in calls),
 'sum_is_parallel_wall_time':False,
 'first_retrieval_started_utc':min(c['started_utc'] for c in calls),
 'last_retrieval_completed_utc':max(c['completed_utc'] for c in calls),
 'new_discovery_search_queries':0,
 'tokens':'not provided','human_person_hours':'not observed',
 'local_preparation_failures':['requests import unavailable before network; urllib used instead','one batched cache-save command exceeded OS argument length; saved responses individually without repeating retrieval'],
}
(OUT/'receipts'/'cost-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False))
