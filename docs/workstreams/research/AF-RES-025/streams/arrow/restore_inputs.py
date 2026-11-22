"""Restore exact initial email inputs from the official archive; no later replies.

Full original messages are an untracked local reading cache. The repository
stores immutable Message-ID, raw URL and decoded-body SHA256 instead of assuming
that a public archive grants blanket republication rights.
"""
import email,email.policy,hashlib,json,pathlib,urllib.request,sys
P=pathlib.Path(__file__).resolve().parent

def restore(row):
    with urllib.request.urlopen(row['raw_source_url'],timeout=30) as response:
        raw=response.read()
    msg=email.message_from_bytes(raw,policy=email.policy.default)
    if str(msg.get('Message-ID'))!=row['message_id']:
        raise ValueError('Message-ID differs: '+row['id'])
    text='\n'.join(x.get_content() for x in msg.walk() if x.get_content_type()=='text/plain') if msg.is_multipart() else msg.get_content()
    sha=hashlib.sha256(text.encode()).hexdigest()
    restored_terminal_lf=False
    # The raw single-message endpoint can omit the final LF supplied by the
    # monthly mbox separator. Restore only when it matches the sealed hash.
    if sha!=row['input_sha256'] and hashlib.sha256((text+'\n').encode()).hexdigest()==row['input_sha256']:
        text+='\n'
        sha=hashlib.sha256(text.encode()).hexdigest()
        restored_terminal_lf=True
    if sha!=row['input_sha256']:
        raise ValueError('Decoded initial body hash differs: '+row['id']+' '+sha)
    target=P/'cache'/'inputs'/(row['id']+'.md')
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(text)
    return {'id':row['id'],'source_url':row['raw_source_url'],'sha256':sha,'bytes':len(text.encode()),'status':'restored_exact','restored_terminal_lf':restored_terminal_lf}

if __name__=='__main__':
    rows=json.loads((P/'input-metadata.json').read_text())
    wanted=set(sys.argv[1:])
    for row in rows:
        if not wanted or row['id'] in wanted:print(json.dumps(restore(row)))
