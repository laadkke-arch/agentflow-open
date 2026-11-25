"""One command for workbench tests, two real lab tasks, reuse and restore checks."""
import os
from pathlib import Path
import subprocess
import sys

root=Path(__file__).resolve().parents[1]
out=root/'.workbench'
out.mkdir(exist_ok=True)
env=os.environ.copy()
env.update(PYTHONPATH=str(root),PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1')
commands=[['-m','unittest','discover','-s','workbench','-p','test_*.py','-v'],
          ['scripts/acceptance.py',*sys.argv[1:]]]
for number,args in enumerate(commands):
    proc=subprocess.run([sys.executable,*args],cwd=root,env=env,capture_output=True,
                        text=True,encoding='utf-8',timeout=180)
    text=proc.stdout+proc.stderr
    (out/f'check-{number}.log').write_text(text,encoding='utf-8')
    print(text,flush=True)
    if proc.returncode:
        raise SystemExit(proc.returncode)
