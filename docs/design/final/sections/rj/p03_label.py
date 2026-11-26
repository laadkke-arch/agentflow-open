"""Label P03.w matches by token class using hand-written intake lists (demonstration of the procedure)."""
import json, sys, importlib.util
spec = importlib.util.spec_from_file_location('r', sys.argv[2]); r = importlib.util.module_from_spec(spec)
sys.argv = [sys.argv[0], sys.argv[1], 'none']; spec.loader.exec_module(r)
q = next(x for x in r.queries if x['id'] == 'P03.w')
NAME = {'python', '3', '13', 'asyncio'}                       # target part: Python 3.13 asyncio
POS = {'pending','concurrent','work','saving','slower','conversion','admission','completion','signaling',
       'queue','items','item','jobs','run','producer','wait','sink','slows','resume','recovery','capacity',
       'worker','lazy','iterator','pause','storage'}          # 대상어·동작어 from goal/target/given/H1-H3 positive parts
NEG = {'create','tasks','inputs','ahead','time','move','unbounded','buffer','passing','alone','allow',
       'exceeded','dropping','prohibited','pushes','indefinitely'}   # 금지 절·부정 전제
OUT = {'ram','byte','held','memory','throughput','improvement','figures','forced','immediate','cancellation','crash'}
def cls(t):
    if t in r.FW_EN: return 'FW'
    if t in NAME: return 'NAME'
    if t in POS: return 'OP'
    if t in NEG: return 'NEG'
    if t in OUT: return 'OUT'
    return 'OTHER'
def verdict(ms):
    c = {cls(t) for t in ms}
    if 'OP' in c: return '작동·대상 일치'
    if 'NAME' in c: return '이름·판 일치만'
    return '우연 적중'
for n, name in enumerate(r.VARIANTS, 1):
    d = r.docs_for('en', n); res = r.rank(d, q['en'])
    print('==', name)
    for i, (k, ms, s) in enumerate(res[:10], 1):
        print(i, k, r.qrels['P03.w'].get(k, '-'), verdict(ms), {t: cls(t) for t in ms if cls(t) != 'FW'})
    for k in ('toyota-jit', 'asyncio-queue', 'asyncio-semaphore', 'reactive-streams'):
        pos = next((i for i, (kk, ms, s) in enumerate(res, 1) if kk == k), None)
        ms = next((ms for kk, ms, s in res if kk == k), [])
        print('  ', k, pos, verdict(ms) if ms else '-', sorted(t for t in ms if cls(t) != 'FW'))
