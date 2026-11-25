"""Small configuration adapter; the MCP engine remains upstream SpaceDock."""
import argparse
import json
import os
from pathlib import Path
from upstream_configure import configure as upstream_configure


def configure(origin, state, workspace, port=8766):
    path = upstream_configure(origin, state, workspace, port)
    if os.environ.get('AGENTFLOW_ROOT_LAYOUT') != 'separate-roots-v1':
        return path
    workspace = Path(workspace).resolve()
    config = json.loads(path.read_text(encoding='utf-8'))
    basic = ['fs.read','fs.write','git.read','workspace.manage','recall.read','recall.write']
    roots = []
    for name in ('demo','agentflow-open','shared'):
        directory = workspace / name
        directory.mkdir(exist_ok=True)
        roots.append({'id':name, 'name':name, 'path':str(directory),
            'permissions':basic + ([] if name == 'shared' else ['command.execute'])})
    config['allowed_roots'] = roots
    path.write_text(json.dumps(config, indent=2), encoding='utf-8')
    os.chmod(path, 0o600)
    return path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('origin')
    parser.add_argument('--state', default='/state')
    parser.add_argument('--workspace', default='/workspace')
    args = parser.parse_args()
    configure(args.origin,args.state,args.workspace)
