"""Adapt only the pinned upstream diagnostic's demo root and truthful labels."""
from pathlib import Path
root = Path('/opt/kc-mcp/scripts')
source = root / 'check_live.py'
text = source.read_text(encoding='utf-8')
old = "{'root_id':'projects','path':'demo','mode':'checkout'}"
assert text.count(old) == 1, 'Upstream diagnostic changed; review before patching'
(root / 'check_live_upstream.py').write_text(text, encoding='utf-8')
text = text.replace(old, "{'root_id':'demo','path':'.','mode':'checkout'}")
text = text.replace('public HTTPS', 'configured endpoint').replace("'public ", "'endpoint ")
source.write_text(text, encoding='utf-8')
