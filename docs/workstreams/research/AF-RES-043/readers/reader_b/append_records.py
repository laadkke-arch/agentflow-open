import json,sys,pathlib
p=pathlib.Path(__file__).parent
obj=json.load(sys.stdin)
for key,name in [('reads','reads.jsonl'),('judgments','judgments.jsonl')]:
    records=obj.get(key,[])
    if records:
        with (p/name).open('a',encoding='utf-8') as f:
            for record in records:
                f.write(json.dumps(record,ensure_ascii=False,separators=(',',':'))+'\n')
if obj.get('notes'):
    with (p/'reader-notes.md').open('a',encoding='utf-8') as f:
        f.write(obj['notes']+'\n')
print(json.dumps({'reads_appended':len(obj.get('reads',[])),'judgments_appended':len(obj.get('judgments',[]))}))
