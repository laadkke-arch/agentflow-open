"""Run one tracked WPT reftest per fresh browser and retain its original receipts."""

import argparse
import base64
import gzip
import hashlib
import json
import os
import shutil
import signal
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageChops


HERE = Path(__file__).resolve().parent
MANIFEST = json.loads((HERE / 'manifest.json').read_text())
PRODUCTS = {'chromium': 'chrome', 'webkitgtk': 'webkitgtk_minibrowser'}
CHROME_ARGS = ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage',
               '--disable-background-networking', '--force-device-scale-factor=1']
WPT_MAIN = 'from tools import localpaths; from wptrunner.wptrunner import main; raise SystemExit(main())'


def utc():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def new_environment(profile):
    env = os.environ.copy()
    for key, basename in {
        'XDG_CACHE_HOME': 'cache', 'XDG_CONFIG_HOME': 'config',
        'XDG_DATA_HOME': 'data', 'XDG_RUNTIME_DIR': 'runtime',
    }.items():
        folder = profile / basename
        folder.mkdir(parents=True, mode=0o700)
        env[key] = str(folder)
    env.update(NO_PROXY='localhost,127.0.0.1,::1', no_proxy='localhost,127.0.0.1,::1',
               GDK_SCALE='1', GDK_DPI_SCALE='1', PIP_NO_CACHE_DIR='1')
    return env


def verify_inputs(root):
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    if revision != MANIFEST['wpt']['commit']:
        raise ValueError(f'Unpinned WPT revision: {revision}')
    expected = {}
    for test in MANIFEST['tests']:
        expected[test['input']] = test['input_sha256']
        expected[test['reference']] = test['reference_sha256']
    for key in ('font', 'font_css'):
        item = MANIFEST['wpt'][key]
        expected[item['path']] = item['sha256']
    for path, sha in expected.items():
        if digest(root / path) != sha:
            raise ValueError(f'Input fingerprint differs: {path}')


def picture_pair(test_png, ref_png, diff_png):
    with Image.open(test_png) as actual, Image.open(ref_png) as reference:
        info = {'input_px': list(actual.size), 'reference_px': list(reference.size),
                'input_sha256': digest(test_png), 'reference_sha256': digest(ref_png)}
        if actual.size != reference.size:
            return {**info, 'different_pixels': None, 'size_mismatch': True}
        # Complement the runner relation with an exact comparison of decoded pixels.
        delta = ImageChops.difference(actual.convert('RGBA'), reference.convert('RGBA'))
        mask = delta.getchannel(0)
        for i in range(1, 4):
            mask = ImageChops.lighter(mask, delta.getchannel(i))
        out = Image.new('RGB', actual.size, 'white')
        out.paste((255, 0, 128), mask=mask.point(lambda n: 255 if n else 0))
        out.save(diff_png, optimize=True)
        return {**info, 'different_pixels': actual.width * actual.height - mask.histogram()[0],
                'bbox_xyxy_exclusive': mask.getbbox(), 'diff_sha256': digest(diff_png)}


def summarize(out, test, exit_code):
    result = {'runner_exit': exit_code, 'test': test['id']}
    raw = out / 'raw.jsonl'
    if not raw.exists():
        return {**result, 'status': 'NO_TEST_END'}
    data = raw.read_bytes()
    (out / 'raw.jsonl.gz').write_bytes(gzip.compress(data, mtime=0))
    raw.unlink()
    result['raw_uncompressed_sha256'] = hashlib.sha256(data).hexdigest()
    events = [json.loads(line) for line in data.splitlines()]
    ends = [event for event in events if event['action'] == 'test_end']
    if len(ends) != 1:
        return {**result, 'status': 'NO_TEST_END', 'test_end_count': len(ends)}
    end = ends[0]
    if end['test'] != '/' + test['input']:
        raise ValueError(f'Unexpected test end: {end["test"]}')
    result.update(status=end['status'], expected=end.get('expected', end['status']),
                  test_path=end['test'], message=end.get('message'))
    report_path = out / 'wptreport.json'
    if report_path.exists() and report_path.stat().st_size:
        report = json.loads(report_path.read_text())
        result['report_status'] = [row['status'] for row in report['results'] if row['test'] == end['test']]
        result['report_sha256'] = digest(report_path)
    screenshots = end.get('extra', {}).get('reftest_screenshots')
    if screenshots:
        actual, relation, reference = screenshots
        if (actual['url'], relation, reference['url']) != (
            '/' + test['input'], {'match': '==', 'mismatch': '!='}[test['reference_relation']], '/' + test['reference']
        ):
            raise ValueError('Runner screenshot URLs or relation differ from the sample')
        for src, name in [(actual, 'input.png'), (reference, 'reference.png')]:
            (out / name).write_bytes(base64.b64decode(src['screenshot'].split(',')[-1], validate=True))
        result['relation'] = relation
        result['runner_screenshot_hashes'] = [actual.get('hash'), reference.get('hash')]
        result['pixels'] = picture_pair(out / 'input.png', out / 'reference.png', out / 'diff.png')
    return result


def run_one(args, engine, test, repeat):
    name = f'{engine}-{test["id"]}-r{repeat}'
    out = args.output / name
    out.mkdir(parents=True)
    env = new_environment(args.profiles / name)
    paths = ['--metadata', str(args.wpt), '--tests', str(args.wpt)]
    if engine == 'chromium':
        command = [str(args.wpt / 'wpt'), 'run', '-y', PRODUCTS[engine]]
        options = ['--headless', '--browser-channel', 'stable', '--browser-version', '156.0.8078.79',
                   '--binary', str(args.chromium_binary), '--webdriver-binary',
                   str(args.chromium_driver), '--binary-arg=' + f'--user-data-dir={args.profiles / name / "chromium"}']
        options += ['--binary-arg=' + option for option in CHROME_ARGS]
    else:
        command = [str(args.wpt / '_venv3/bin/python'), '-c', WPT_MAIN, '--product', PRODUCTS[engine], *paths]
        options = ['--browser-version', '2.54.3', '--binary', str(args.webkit_binary), '--webdriver-binary',
                   str(args.webkit_driver), '--host-cert-path', str(args.wpt / 'tools/certs/web-platform.test.pem'),
                   '--host-key-path', str(args.wpt / 'tools/certs/web-platform.test.key'),
                   '--ca-cert-path', str(args.wpt / 'tools/certs/cacert.pem')]
    command += [*options, '--include', test['input'], '--test-types', 'reftest', '--processes', '1',
                '--retry-unexpected', '0', '--max-restarts', '0', '--no-pause-after-test',
                '--ssl-type', 'pregenerated', '--no-install-fonts', '--no-manifest-update', '--no-manifest-download',
                '--reftest-screenshot', 'always', '--log-mach', '-', '--log-raw', str(out / 'raw.jsonl'),
                '--log-raw-level', 'debug', '--log-wptreport', str(out / 'wptreport.json')]
    context = ['DISPLAY', 'GDK_SCALE', 'GDK_DPI_SCALE', 'LD_LIBRARY_PATH', 'NO_PROXY', 'AF255_WEBKIT_ROOT',
               'AF255_WEBKIT_SHIM',
               'XDG_CACHE_HOME', 'XDG_CONFIG_HOME', 'XDG_DATA_HOME', 'XDG_RUNTIME_DIR',
               'WEBKIT_DISABLE_SANDBOX_THIS_IS_DANGEROUS', 'WEBKIT_DISABLE_DMABUF_RENDERER']
    write_json(out / 'command.json', {'argv': command, 'cwd': str(args.wpt), 'env': {key: env[key] for key in context if key in env},
                                      'wpt': MANIFEST['wpt']['commit'], 'started_utc': utc()})
    with (out / 'stdout.txt').open('wb') as stdout, (out / 'stderr.txt').open('wb') as stderr:
        process = subprocess.Popen(command, cwd=args.wpt, env=env, stdout=stdout, stderr=stderr, start_new_session=True)
        try:
            exit_code = process.wait(timeout=args.timeout)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
            exit_code = 124
    summary = summarize(out, test, exit_code)
    summary.update(run_id=name, engine=engine, repeat=repeat, ended_utc=utc())
    write_json(out / 'summary.json', summary)
    shutil.rmtree(args.profiles / name)
    print(name, summary['status'], exit_code, summary.get('pixels', {}).get('different_pixels'), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wpt', type=Path, required=True)
    parser.add_argument('--chromium-binary', type=Path, default=Path('/usr/bin/chromium'))
    parser.add_argument('--chromium-driver', type=Path)
    parser.add_argument('--webkit-binary', type=Path)
    parser.add_argument('--webkit-driver', type=Path)
    parser.add_argument('--engine', action='append', choices=PRODUCTS, required=True)
    parser.add_argument('--test', action='append', choices=['002', '003'])
    parser.add_argument('--repeat', action='append', type=int)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--profiles', type=Path, required=True)
    parser.add_argument('--timeout', type=int, default=90)
    args = parser.parse_args()
    args.wpt, args.output, args.profiles = (path.resolve() for path in (args.wpt, args.output, args.profiles))
    verify_inputs(args.wpt)
    for engine in args.engine:
        if engine == 'chromium' and args.chromium_driver is None:
            parser.error('--chromium-driver is required for Chromium')
        if engine == 'webkitgtk' and (args.webkit_binary is None or args.webkit_driver is None):
            parser.error('--webkit-binary and --webkit-driver are required for WebKitGTK')
        for test in MANIFEST['tests']:
            if args.test is None or test['id'] in args.test:
                for repeat in args.repeat or (1, 2):
                    run_one(args, engine, test, repeat)


if __name__ == '__main__':
    main()
