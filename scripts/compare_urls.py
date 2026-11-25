"""Optional comparison. Uses yarl only when already installed; never installs it."""
from importlib.metadata import version, PackageNotFoundError
import json
from pathlib import Path
from urllib.parse import urlsplit

root=Path(__file__).resolve().parents[1]
try:
    from yarl import URL
    yarl_version=version('yarl')
except (ImportError,PackageNotFoundError):
    URL=None
    yarl_version=None
cases=['https://GitHub.com/Python/CPython.git/', 'https://github.com/python/cpython',
       'https://github.com/a/b?b=2&a=1#part', 'https://@github.com/a/b']
result={'scope':'parser behavior, not performance or domain-correctness benchmark',
        'yarl_version':yarl_version,'w3lib':'documentation only; not executed','cases':[]}
for case in cases:
    result['cases'].append({'input':case,'urllib_roundtrip':urlsplit(case).geturl(),
                            'yarl_roundtrip':str(URL(case)) if URL else None})
print(json.dumps(result,indent=2))
