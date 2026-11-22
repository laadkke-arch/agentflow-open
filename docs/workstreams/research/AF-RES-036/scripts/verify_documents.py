"""Check deliverable structure, evidence pointers, acceptance arithmetic, and ownership."""
import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

P = Path(__file__).resolve().parents[1]
ROOT = P.parents[3]
parser = argparse.ArgumentParser()
parser.add_argument('--receipt', default='evidence/document-check.json')
parser.add_argument('--handoff', action='store_true')
args = parser.parse_args()
receipt = (P / args.receipt).resolve()
assert receipt.is_relative_to(P)
checks = []


def check(name, value, details=None):
    checks.append({'check': name, 'passed': bool(value), 'details': details})


text = (P / 'RESULT.md').read_text()
tables = []
for block in re.split(r'\n\s*\n', text):
    lines = block.splitlines()
    if lines and lines[0].startswith('| '):
        rows = [[v.strip() for v in x.strip().strip('|').split('|')] for x in lines if x.startswith('|')]
        if len(rows) >= 2:
            tables.append(rows)
headers = [
    ['참조 ID·원배포/목적','원 href·버전','현재 절 URL·확인 내용','과거 근거 URL·판','네 보기의 행동(B·B+N·B+H·B+N+H)','기준판정·독립성','미확인'],
    ['대조·목적 층','짝지은 참조 수','옳은 유지·교체','오교체·잘못 유지·보류','N 고정 후 H로 바뀐 사건 ID','노출 제외·판정 불가'],
    ['참조·조회 회차·구성','실제 요청·실패','받은 바이트·저장 바이트','같은 판 재사용·재열람·경과','실제·모의·미계측','결론을 바꿀 다음 자료'],
]
blocks = [b for b in re.split(r'\n\s*\n', text) if b.strip()]
check('first three blocks after title are required tables', len(blocks) > 3 and all(blocks[i].startswith('| ') for i in [1,2,3]))
for i,(rows,cols) in enumerate([(12,7),(14,6),(18,6)]):
    check('required table '+str(i+1)+' headers', tables[i][0] == headers[i])
    check('required table '+str(i+1)+' shape', len(tables[i])-2 == rows and all(len(r)==cols for r in tables[i]), {'rows':len(tables[i])-2,'columns':len(tables[i][0])})
last_header=['가장 중요한 불일치 또는 약점','근거 자료 주소','영향을 받는 결론','다음 조사 제안과 첫 자료']
check('last table has exactly three weaknesses and correct columns', tables[-1][0] == last_header and len(tables[-1])-2 == 3 and all(len(r)==4 for r in tables[-1]))
check('all eight questions answered in RESULT', len(re.findall(r'^## Q[1-8]\.',text,re.M))==8)
selfcheck=(P/'SELF_CHECK.md').read_text()
check('all eight SELF_CHECK rows', sorted(re.findall(r'^\| (Q[1-8]) \|',selfcheck,re.M))==['Q'+str(i) for i in range(1,9)])
accept=json.loads((P/'evidence/acceptance-evidence.json').read_text())
cc=accept['conditions'];summary=accept['summary']
check('acceptance IDs unique',len({c['id'] for c in cc})==len(cc))
check('acceptance arithmetic',summary=={'total':len(cc),'met':sum(c['met'] for c in cc),'unmet':sum(not c['met'] for c in cc),'unmet_ids':[c['id'] for c in cc if not c['met']]},summary)
check('each condition has scope and next minimum',all(isinstance(c['met'],bool) and c['fulfilled_scope_or_unmet_reason'] and c['next_minimum_check'] and c['evidence'] for c in cc))
missing=[e for c in cc for e in c['evidence'] if not (P/e['file']).exists() or not e.get('rows_or_location')]
check('acceptance evidence paths exist and locations supplied',not missing,missing)
missing_links=[]
for name in ['RESULT.md','SELF_CHECK.md']+(['HANDOFF.md'] if args.handoff else []):
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',(P/name).read_text()):
        if re.match(r'^[a-z]+:',target) or target.startswith('#'):continue
        filepart=target.split('#',1)[0]
        if not (P/filepart).exists():missing_links.append([name,target])
check('relative deliverable links resolve',not missing_links,missing_links)
ids={json.loads(l)['ref_id'] for l in (P/'references.jsonl').read_text().splitlines() if l}
check('table one has each reference once',set(r[0].split(' · ',1)[0] for r in tables[0][2:])==ids and len(tables[0][2:])==len(ids))
check('table two labels included and excluded IDs',all('포함:' in r[5] and '제외:' in r[5] for r in tables[1][2:]))
check('table three case rows name next exact source',all('](https://' in r[5] for r in tables[2][2:14]))
check('reported date and member corrections applied','2026-01-29 공식 stable 발표' in text and 'SingleCellExperiment/man/SingleCellExperiment.Rd' in text and '2026-01-28 공식 stable 발표' not in text)
check('gaps retained as REVIEW_READY_WITH_GAPS',accept['status']=='REVIEW_READY_WITH_GAPS' and summary['unmet']>0 and 'REVIEW_READY_WITH_GAPS' in text)
all_paths=set(subprocess.check_output(['git','diff','--name-only','9668632e915d508e93ddfdc5e8fe4b88bcbfec56','HEAD'],cwd=ROOT,text=True).splitlines())
all_paths.update(subprocess.check_output(['git','diff','--name-only'],cwd=ROOT,text=True).splitlines())
all_paths.update(subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines())
outside=[x for x in sorted(all_paths) if not x.startswith('docs/workstreams/research/AF-RES-036/')]
check('all changes within owned path',not outside,outside)
if args.handoff:
    h=(P/'HANDOFF.md').read_text()
    check('HANDOFF points to actual remote reread and session receipt','result-remote-reread.json' in h and 'session-result-execution.json' in h)
    remote=json.loads((P/'evidence/result-remote-reread.json').read_text())
    session=json.loads((P/'evidence/checks/session-result-execution.json').read_text())
    check('HANDOFF prerequisite receipts succeeded',remote['all_identical'] and session['exit_code']==0,{'result_commit':remote['commit'],'session_target':session['head']})
files=['RESULT.md','SELF_CHECK.md','evidence/acceptance-evidence.json','evidence/final-counts.json','references.jsonl','decisions.csv','packets.jsonl','sources.jsonl','attempts.jsonl','costs.csv']+(['HANDOFF.md'] if args.handoff else [])
data={'checked_utc':datetime.now(timezone.utc).isoformat(),'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
      'input_sha256':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in files},
      'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'all_passed':all(c['passed'] for c in checks),
      'scope':'document/evidence-pointer/ownership checks on exact working tree bytes; not external source truth or product execution'}
receipt.parent.mkdir(parents=True,exist_ok=True);receipt.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':data['passed'],'total':data['total'],'all_passed':data['all_passed'],'receipt':str(receipt.relative_to(P))},ensure_ascii=False))
raise SystemExit(0 if data['all_passed'] else 1)
