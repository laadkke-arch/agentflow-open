#!/usr/bin/env python3
"""Small synthetic calibration; this is not a run of either upstream suite."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
CACHE = ROOT / '.cache' / 'cross-domain'
CACHE.mkdir(parents=True, exist_ok=True)
records = []

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')

def run(argv, cwd, label, expected=0):
    started = utc()
    env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null', LC_ALL='C')
    p = subprocess.run(argv, cwd=cwd, env=env, text=True, capture_output=True)
    record = dict(label=label, command=argv, cwd='synthetic-fixture', started_utc=started,
                  ended_utc=utc(), exit_code=p.returncode, expected_exit=expected,
                  stdout=p.stdout, stderr=p.stderr)
    records.append(record)
    if p.returncode != expected:
        raise RuntimeError(json.dumps(record))
    return p.stdout

def git_state(folder):
    return {'HEAD': run(['git', 'show', 'HEAD:f.txt'], folder, 'inspect-head'),
            'index': run(['git', 'show', ':f.txt'], folder, 'inspect-index'),
            'worktree': (folder / 'f.txt').read_text()}

summary = {'kind': 'researcher-synthetic-calibration', 'started_utc': utc(),
           'upstream_suites_executed': False,
           'pinned_git_source': 'bea9ecd24b0c3bf06cab4a851694fe09e7e51408',
           'pinned_ffmpeg_source': 'af25a4bfd2503caf3ee485b27b99b620302f5718',
           'historical_request_execution': False}
with tempfile.TemporaryDirectory(prefix='fixture-', dir=CACHE) as temp:
    fixture = Path(temp)
    summary['git_runtime'] = run(['git', '--version'], fixture, 'git-version').strip()
    summary['ffmpeg_runtime'] = run(['ffmpeg', '-version'], fixture, 'ffmpeg-version').splitlines()[0]
    gitdir = fixture / 'git'
    gitdir.mkdir()
    run(['git', 'init', '-q'], gitdir, 'git-init')
    (gitdir / 'f.txt').write_text('base\n')
    run(['git', 'add', 'f.txt'], gitdir, 'git-add-base')
    run(['git', '-c', 'user.name=AF-RES-101 synthetic fixture', '-c', 'user.email=fixture@example.invalid',
         'commit', '-qm', 'Synthetic base'], gitdir, 'git-fixture-commit')
    gtests = [
        ('G1-worktree', ['git', 'restore', '--worktree', '--', 'f.txt']),
        ('G2-index', ['git', 'restore', '--staged', '--', 'f.txt']),
        ('G3-explicit-both', ['git', 'restore', '--source=HEAD', '--staged', '--worktree', '--', 'f.txt']),
        ('G4-alias-both', ['git', 'restore', '-s@', '-SW', '--', 'f.txt']),
    ]
    summary['git_cases'] = []
    for label, command in gtests:
        run(['git', 'restore', '--source=HEAD', '--staged', '--worktree', '--', 'f.txt'], gitdir, label+'-reset-fixture')
        (gitdir / 'f.txt').write_text('index\n')
        run(['git', 'add', 'f.txt'], gitdir, label+'-stage-input')
        (gitdir / 'f.txt').write_text('worktree\n')
        before = git_state(gitdir)
        run(command, gitdir, label)
        summary['git_cases'].append(dict(id=label, command=command, before=before, after=git_state(gitdir)))

    avdir = fixture / 'ffmpeg'
    avdir.mkdir()
    common = ['ffmpeg', '-hide_banner', '-nostdin', '-loglevel', 'error', '-y']
    generator = common + ['-f', 'lavfi', '-i', 'testsrc2=size=16x16:rate=1:duration=1',
         '-f', 'lavfi', '-i', 'sine=frequency=440:duration=1',
         '-f', 'lavfi', '-i', 'sine=frequency=880:duration=1',
         '-map', '0:v', '-map', '1:a', '-map', '2:a',
         '-c:v', 'ffv1', '-c:a', 'pcm_s16le', 'source.mkv']
    run(generator, avdir, 'ffmpeg-input-generator')
    summary['ffmpeg_input'] = dict(generator=generator, sha256=hashlib.sha256((avdir/'source.mkv').read_bytes()).hexdigest())
    def inspect(name, label):
        data = json.loads(run(['ffprobe', '-v', 'error', '-show_entries',
             'stream=index,codec_name,codec_type,channels', '-of', 'json', name], avdir, label+'-streams'))
        packet_json = json.loads(run(['ffprobe', '-v', 'error', '-show_packets', '-show_data_hash', 'sha256',
             '-show_entries', 'packet=stream_index,data_hash', '-of', 'json', name], avdir, label+'-packets'))
        return dict(streams=data.get('streams', []), packet_hashes=packet_json.get('packets', []),
                    file_sha256=hashlib.sha256((avdir/name).read_bytes()).hexdigest())
    summary['ffmpeg_input'].update(inspect('source.mkv', 'source'))
    ftests = [
        ('F1-auto-copy', ['-c', 'copy'], 'auto.mkv'),
        ('F2-all-copy', ['-map', '0', '-c', 'copy'], 'all.mkv'),
        ('F3-alias-copy', ['-map', '0', '-codec', 'copy'], 'alias.mkv'),
        ('F4-all-audio-transcode', ['-map', '0', '-c:v', 'copy', '-c:a', 'flac'], 'transcoded.mkv'),
    ]
    summary['ffmpeg_cases'] = []
    for label, options, filename in ftests:
        command = common + ['-i', 'source.mkv'] + options + [filename]
        run(command, avdir, label)
        summary['ffmpeg_cases'].append(dict(id=label, command=command, output=inspect(filename, label)))
    g = summary['git_cases']
    f = summary['ffmpeg_cases']
    summary['checks'] = {
       'G1_retains_index_changes_restores_worktree_from_index': g[0]['after'] == dict(HEAD='base\n', index='index\n', worktree='index\n'),
       'G2_restores_index_from_HEAD_retains_worktree': g[1]['after'] == dict(HEAD='base\n', index='base\n', worktree='worktree\n'),
       'G3_G4_alias_same_observed_state': g[2]['after'] == g[3]['after'] == dict(HEAD='base\n', index='base\n', worktree='base\n'),
       'F1_selects_2_of_3_streams': len(f[0]['output']['streams']) == 2,
       'F2_selects_all_3_streams': len(f[1]['output']['streams']) == 3,
       'F2_F3_alias_same_streams_and_packet_hashes': f[1]['output']['streams'] == f[2]['output']['streams'] and f[1]['output']['packet_hashes'] == f[2]['output']['packet_hashes'],
       'F4_keeps_3_streams_changes_audio_codec': len(f[3]['output']['streams']) == 3 and [x['codec_name'] for x in f[3]['output']['streams']] == ['ffv1', 'flac', 'flac'],
    }

summary['ended_utc'] = utc()
summary['checks_passed'] = sum(summary['checks'].values())
summary['checks_total'] = len(summary['checks'])
summary['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(OUT/'receipt.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False)+'\n')
(OUT/'commands.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in records))
print(json.dumps({k: summary[k] for k in ['git_runtime','ffmpeg_runtime','checks','checks_passed','checks_total','ended_utc']}, indent=2))
if not all(summary['checks'].values()):
    raise SystemExit(1)
