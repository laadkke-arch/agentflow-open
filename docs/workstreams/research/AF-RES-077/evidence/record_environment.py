"""Read-only availability check; does not install, build, or launch target GUIs."""
import datetime
import json
import platform
import shutil
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
row = {'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'checker': 'root', 'phase': 'after_B_seal', 'python': platform.python_version(),
       'target_execution_attempted': False, 'build_attempted': False,
       'reason': 'Pinned target binaries, cmake/ctest, and required pkg-config development packages are unavailable.',
       'availability': [], 'commands': []}
for name in ('shotcut','musescore','mscore','sigil','qmake','cmake','ctest','ffmpeg','ffprobe','xvfb-run','pkg-config'):
    row['availability'].append({'command': name, 'path': shutil.which(name)})
for cmd in (['qmake','-v'], *(['pkg-config','--modversion',x] for x in ('Qt5Core','Qt5Widgets','mlt-framework','mlt-framework-7','libxml-2.0'))):
    p = subprocess.run(cmd, capture_output=True, text=True)
    row['commands'].append({'argv': cmd, 'exit_code': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr})
(root/'evidence/environment.json').write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'receipt':'evidence/environment.json', 'target_gui_runs':0,
                  'commands':[(x['argv'],x['exit_code']) for x in row['commands']]}))
