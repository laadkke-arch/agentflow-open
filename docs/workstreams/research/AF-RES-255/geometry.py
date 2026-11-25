"""Load pinned bytes in independent WebDriver sessions and measure words and cues."""

import argparse
import base64
import contextlib
import hashlib
import json
import os
import signal
import socket
import subprocess
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import ProxyHandler, Request, build_opener

from reftest import CHROME_ARGS, HERE, MANIFEST, new_environment, picture_pair, utc, verify_inputs, write_json


MEASURE = (HERE / 'measure.js').read_text()
OPENER = build_opener(ProxyHandler({}))
FONT_PATH = '/fonts/Ahem.ttf'
CUE_PATH = '/caption/sintel-en.vtt'
WORDS = {'C1': ('aaaa bbb ccc dd ee', 8), 'W7': ('aaaa b c dddd ee', 7)}
REF_SELECTORS = {'002': ['.container'], '003': ['.green:nth-of-type(1)', '.green:nth-of-type(2)', '.blue']}
CUE_SELECTORS = ['#cue-3-wide', '#cue-3-narrow', '#cue-4-wide', '#cue-4-narrow']


def control_doc(text, width, mode):
    css_width = f'{width}ch' if isinstance(width, int) else width
    return (f'<!doctype html><link rel="stylesheet" href="/fonts/ahem.css">\n'
            f'<style>body {{ margin: 8px; }} #control {{ font: 20px/1 Ahem; width: {css_width}; '
            f'text-wrap: {mode}; white-space: normal; hyphens: none; word-break: normal; '
            f'overflow-wrap: normal; text-align: start; letter-spacing: 0; word-spacing: 0; }}</style>\n'
            f'<div id="control">{text}</div>\n').encode()


def build_controls():
    docs = {}
    for case, (text, width) in WORDS.items():
        first, second, rest = text.split(' ', 2)
        for mode in ('auto', 'balance'):
            docs[f'/{case}-{mode}.html'] = control_doc(text, width, mode)
            docs[f'/{case}-{mode}-forced.html'] = control_doc(f'{first} {second}<br>{rest}', width, mode)
    docs['/W7-exact-fit-control.html'] = control_doc('aaaa<br>b c<br>dddd ee', 7, 'auto')
    for suffix, width in [('plus-unit', 'calc(7ch + 0.015625px)'), ('plus-px', 'calc(7ch + 1px)')]:
        for mode in ('auto', 'balance'):
            docs[f'/W7-{mode}-{suffix}.html'] = control_doc(WORDS['W7'][0], width, mode)
    return docs


def result_files(root):
    return {'/' + item[key]: (root / item[key]).read_bytes()
            for item in MANIFEST['tests'] for key in ('input', 'reference')}


@contextlib.contextmanager
def serve(wpt, cases, missing_font=False, delay=0.35):
    files = {**cases, '/fonts/ahem.css': (wpt / 'fonts/ahem.css').read_bytes(), FONT_PATH: (wpt / 'fonts/Ahem.ttf').read_bytes()}
    events = []

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            path = urlsplit(self.path).path
            data = files.get(path)
            if path == FONT_PATH:
                time.sleep(delay)
                if missing_font:
                    data = None
            if data is None:
                self.send_error(404)
                events.append({'path': path, 'status': 404, 'utc': utc()})
                return
            mimetype = {'.html': 'text/html; charset=utf-8', '.css': 'text/css',
                        '.ttf': 'font/ttf', '.vtt': 'text/vtt; charset=utf-8'}[Path(path).suffix]
            self.send_response(200)
            self.send_header('Content-Type', mimetype)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(data)
            events.append({'path': path, 'status': 200, 'bytes': len(data),
                           'sha256': hashlib.sha256(data).hexdigest(), 'utc': utc()})

        def log_message(self, format, *args):
            pass

    with ThreadingHTTPServer(('127.0.0.1', 0), Handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f'http://127.0.0.1:{server.server_port}', events
        finally:
            server.shutdown()
            thread.join()


def request(base, route, method='GET', body=None):
    data = None if body is None else json.dumps(body).encode()
    http = Request(base + route, data=data, method=method, headers={'Content-Type': 'application/json'})
    try:
        with OPENER.open(http, timeout=22) as response:
            payload = json.load(response)
    except HTTPError as error:
        raise RuntimeError(f'{method} {route.rsplit("/", 1)[-1]} {error.code}: {error.read().decode()}') from error
    return payload['value']


@contextlib.contextmanager
def webdriver(args, out):
    with socket.socket() as reservation:
        reservation.bind(('127.0.0.1', 0))
        port = reservation.getsockname()[1]
    base = f'http://127.0.0.1:{port}'
    with tempfile.TemporaryDirectory(prefix='af255-geometry-', dir=args.profiles) as temporary:
        profile = Path(temporary)
        env = new_environment(profile)
        env['CHROME_LOG_FILE'] = str(out / 'chrome.log')
        if args.engine == 'chromium':
            command = [str(args.driver), f'--port={port}']
            capabilities = {
                'browserName': 'chrome',
                'goog:chromeOptions': {'binary': str(args.binary), 'args': ['--headless', *CHROME_ARGS,
                                        f'--user-data-dir={profile / "chromium"}']},
            }
        else:
            command = [str(args.driver), '--host=127.0.0.1', f'--port={port}']
            capabilities = {
                'browserName': 'MiniBrowser',
                'webkitgtk:browserOptions': {'binary': str(args.binary), 'args': ['--automation']},
            }
        # WebKitGTK may time out the first script while eager navigation is still in progress.
        capabilities['pageLoadStrategy'] = 'eager' if args.engine == 'chromium' else 'normal'
        write_json(out / 'driver-command.json', {'argv': command, 'capabilities': capabilities, 'cwd': str(Path.cwd()),
                                                 'started_utc': utc(), 'profile': str(profile)})
        with (out / 'driver.stdout.txt').open('wb') as stdout, (out / 'driver.stderr.txt').open('wb') as stderr:
            process = subprocess.Popen(command, stdout=stdout, stderr=stderr, env=env, start_new_session=True)
            session_route = None
            try:
                for _ in range(70):
                    if process.poll() is not None:
                        raise RuntimeError(f'WebDriver exited {process.returncode}')
                    try:
                        request(base, '/status')
                    except URLError:
                        time.sleep(0.15)
                    else:
                        break
                else:
                    raise RuntimeError('WebDriver status did not become ready')
                session = request(base, '/session', 'POST', {'capabilities': {'alwaysMatch': capabilities}})
                write_json(out / 'session-response.json', session)
                session_route = '/session/' + session['sessionId']

                def command_session(route, method='GET', body=None):
                    return request(base, session_route + route, method, body)

                command_session('/timeouts', 'POST', {'script': 15000, 'pageLoad': 15000, 'implicit': 0})
                yield command_session
            finally:
                if session_route:
                    with contextlib.suppress(URLError, RuntimeError, TimeoutError):
                        request(base, session_route, 'DELETE')
                if process.poll() is None:
                    os.killpg(process.pid, signal.SIGTERM)
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait()
                write_json(out / 'driver-exit.json', {'exit': process.returncode, 'ended_utc': utc()})


def execute(script, command, values=(), async_script=False):
    endpoint = '/execute/async' if async_script else '/execute/sync'
    result = command(endpoint, 'POST', {'script': script, 'args': list(values)})
    if isinstance(result, dict) and 'error' in result:
        raise RuntimeError(result['error'])
    return result


def viewport(command):
    offsets = execute('return [outerWidth-innerWidth, outerHeight-innerHeight]', command)
    command('/window/rect', 'POST', {'x': 0, 'y': 0, 'width': 800 + max(0, offsets[0]),
                                     'height': 600 + max(0, offsets[1])})


def measure_page(command, url, selectors, screenshot=None, cue=False):
    command('/url', 'POST', {'url': url})
    parsed_cues = execute(CUE_SCRIPT, command, async_script=True) if cue else None
    result = execute(MEASURE, command, [selectors], async_script=True)
    if parsed_cues is not None:
        result['parsed_cue_track'] = parsed_cues
    if screenshot:
        screenshot.write_bytes(base64.b64decode(command('/screenshot'), validate=True))
    return result


CUE_DOC = b'''<!doctype html><link rel="stylesheet" href="/fonts/ahem.css">
<style>.cue { font: 12px/1 Ahem; white-space: pre-line; } .wide { width: 42ch; } .narrow { width: 20ch; }</style>
<video preload="none"><track id="track" kind="subtitles" srclang="en" src="/caption/sintel-en.vtt"></video>
'''
CUE_SCRIPT = '''
const done = arguments[arguments.length - 1];
const track = document.querySelector('#track');
track.addEventListener('error', () => done({error: 'track load error'}), {once: true});
track.addEventListener('load', () => {
  const cues = Array.from(track.track.cues);
  const selected = cues.filter(cue => ['3', '4'].includes(cue.id)).map(cue => {
    for (const width of ['wide', 'narrow']) {
      const block = document.createElement('div');
      block.id = `cue-${cue.id}-${width}`;
      block.className = `cue ${width}`;
      block.textContent = cue.text;
      document.body.append(block);
    }
    return {id: cue.id, start: cue.startTime, end: cue.endTime, rawText: cue.text};
  });
  done({readyState: track.readyState, totalCues: cues.length, selected});
}, {once: true});
track.track.mode = 'hidden';
'''


def original(args, test, name, missing):
    out = args.output / name
    out.mkdir(parents=True)
    with serve(args.wpt, result_files(args.wpt), missing_font=missing) as (base, events):
        with webdriver(args, out) as command:
            viewport(command)
            selectors = test['primary_blocks'] + ([test['inline_comparison_block']] if test['id'] == '003' else [])
            actual = measure_page(command, base + '/' + test['input'], selectors, out / 'input.png')
            ref = measure_page(command, base + '/' + test['reference'], REF_SELECTORS[test['id']], out / 'reference.png')
    data = {'engine': args.engine, 'test': test['id'], 'font_route': '404' if missing else 'pinned',
            'font_route_delay_seconds': 0.35, 'input': actual, 'reference': ref, 'http': events,
            'pixels': picture_pair(out / 'input.png', out / 'reference.png', out / 'diff.png')}
    write_json(out / 'geometry.json', data)
    print(name, [block['rows'] for block in actual['blocks']], flush=True)


def controls(args):
    out = args.output / (args.engine + '-controls')
    out.mkdir(parents=True)
    cases = build_controls()
    test = MANIFEST['tests'][0]
    actual = (args.wpt / test['input']).read_bytes()
    for cut, prefix in [(2, b'123 567'), (3, b'123 567 901')]:
        assert actual.count(prefix + b' ') == 1
        cases[f'/002-explicit-cut{cut}.html'] = actual.replace(prefix + b' ', prefix + b'<br>', 1)
    ref = '/' + test['reference']
    cases[ref] = (args.wpt / test['reference']).read_bytes()
    with serve(args.wpt, cases) as (base, events):
        with webdriver(args, out) as command:
            viewport(command)
            results = {}
            for route in cases:
                label = Path(route).stem
                selector = '#control' if label.startswith(('C1', 'W7')) else '.container'
                result = measure_page(command, base + route, [selector], out / (label + '.png'))
                result['input_sha256'] = hashlib.sha256(cases[route]).hexdigest()
                results[label] = result
    comparisons = {}
    for case in WORDS:
        for first, second in [('auto', 'balance'), ('auto-forced', 'balance-forced'), ('balance', 'balance-forced')]:
            label = f'{case}-{first}-vs-{second}'
            comparisons[label] = picture_pair(out / f'{case}-{first}.png', out / f'{case}-{second}.png', out / (label + '.png'))
    for cut in (2, 3):
        label = f'002-explicit-cut{cut}-vs-reference'
        comparisons[label] = picture_pair(out / f'002-explicit-cut{cut}.png', out / (Path(ref).stem + '.png'), out / (label + '.png'))
    for suffix in ('plus-unit', 'plus-px'):
        label = f'W7-auto-vs-balance-{suffix}'
        comparisons[label] = picture_pair(out / f'W7-auto-{suffix}.png', out / f'W7-balance-{suffix}.png', out / (label + '.png'))
    write_json(out / 'controls.json', {'engine': args.engine, 'inputs': results, 'comparisons': comparisons, 'http': events})


def captions(args):
    fixture = args.vtt.read_bytes()
    assert hashlib.sha256(fixture).hexdigest() == MANIFEST['cue_fixture']['sha256']
    out = args.output / (args.engine + '-captions')
    out.mkdir(parents=True)
    with serve(args.wpt, {'/captions.html': CUE_DOC, CUE_PATH: fixture}) as (base, events):
        with webdriver(args, out) as command:
            viewport(command)
            result = measure_page(command, base + '/captions.html', CUE_SELECTORS, cue=True)
    raw = []
    for cue_block in fixture.decode('utf-8-sig').replace('\r\n', '\n').split('\n\n'):
        if not cue_block.strip():
            continue
        cue_id, *lines = cue_block.splitlines()
        if cue_id in MANIFEST['cue_fixture']['cue_ids']:
            timing, *text = lines
            raw.append({'id': cue_id, 'timing': timing, 'rawText': '\n'.join(text)})
    write_json(out / 'captions.json', {'engine': args.engine, 'fixture_sha256': MANIFEST['cue_fixture']['sha256'],
                                     'raw_cues': raw, 'measurement': result, 'http': events})


FONT_AUDIT = '''
const source = arguments[0];
const done = arguments[arguments.length - 1];
const frame = document.createElement('iframe');
frame.width = 800;
frame.height = 600;
const started = performance.now();
const state = {events: []};
let timer;
const timeout = setTimeout(() => { clearInterval(timer); done(state); }, 4000);
timer = setInterval(() => {
  const doc = frame.contentDocument;
  if (!doc || new URL(doc.URL).pathname !== source) return;
  clearInterval(timer);
  state.attachedMs = performance.now() - started;
  state.url = doc.URL;
  for (const type of ['loading', 'loadingdone', 'loadingerror']) {
    doc.fonts.addEventListener(type, event => {
      state.events.push({type, atMs: performance.now() - started,
        faces: Array.from(event.fontfaces, face => ({family: face.family, status: face.status}))});
      if (type === 'loadingdone' || type === 'loadingerror') {
        clearTimeout(timeout);
        state.faceSet = Array.from(doc.fonts, face => ({family: face.family, status: face.status}));
        done(state);
      }
    }, {once: true});
  }
}, 8);
frame.src = source;
document.body.append(frame);
'''

FONT_CALIBRATION = b'''<!doctype html>
<script>
window.fontCapture = [];
for (const type of ['loading', 'loadingdone', 'loadingerror']) {
  document.fonts.addEventListener(type, event => window.fontCapture.push({
    type, atMs: performance.now(),
    faces: Array.from(event.fontfaces, face => ({family: face.family, status: face.status})),
  }));
}
</script><link rel="stylesheet" href="/fonts/ahem.css">
<div style="font:20px Ahem">123 567 901</div>
'''


def font_audit(args):
    out = args.output / (args.engine + '-font-audit')
    out.mkdir(parents=True)
    docs = {**result_files(args.wpt), '/font-audit.html': b'<!doctype html><title>Font load event audit</title><body>',
            '/font-calibration.html': FONT_CALIBRATION}
    with serve(args.wpt, docs, delay=0.75) as (base, events):
        with webdriver(args, out) as command:
            command('/url', 'POST', {'url': base + '/font-calibration.html'})
            calibration = execute('return window.fontCapture', command)
            checks = []
            for test in MANIFEST['tests']:
                command('/url', 'POST', {'url': base + '/font-audit.html'})
                checks.append({'test': test['id'], **execute(FONT_AUDIT, command, ['/' + test['input']], async_script=True)})
    write_json(out / 'font-audit.json', {'engine': args.engine, 'font_route_delay_seconds': 0.75,
                                        'separate_calibration': calibration,
                                        'checks': checks, 'http': events})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wpt', required=True, type=Path)
    parser.add_argument('--engine', required=True, choices=('chromium', 'webkitgtk'))
    parser.add_argument('--driver', required=True, type=Path)
    parser.add_argument('--binary', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--profiles', type=Path, required=True)
    parser.add_argument('--mode', required=True, choices=('original', 'missing-font', 'controls', 'captions', 'font-audit'))
    parser.add_argument('--test', action='append', choices=('002', '003'))
    parser.add_argument('--repeat', action='append', type=int)
    parser.add_argument('--vtt', type=Path)
    args = parser.parse_args()
    args.output = args.output.resolve()
    args.profiles.mkdir(parents=True, exist_ok=True)
    verify_inputs(args.wpt)
    if args.mode == 'controls':
        controls(args)
    elif args.mode == 'captions':
        if args.vtt is None:
            parser.error('--vtt is required for captions')
        captions(args)
    elif args.mode == 'font-audit':
        font_audit(args)
    else:
        suffix = '-missing-font' if args.mode == 'missing-font' else ''
        for test in MANIFEST['tests']:
            if args.test is None or test['id'] in args.test:
                for repeat in args.repeat or ((1,) if suffix else (1, 2)):
                    original(args, test, f'{args.engine}-{test["id"]}-r{repeat}{suffix}', bool(suffix))


if __name__ == '__main__':
    main()
