"""Join original runner and independent geometry receipts without imputing missing cells."""

import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
MANIFEST = json.loads((HERE / 'manifest.json').read_text())
ENV = json.loads((HERE / 'env.json').read_text())
RUN_FIELDS = ['run_id', 'test', 'engine', 'repeat', 'build', 'driver_build', 'runner_product',
              'status', 'runner_exit', 'report_status', 'relation', 'different_pixels', 'input_sha256',
              'reference_sha256', 'diff_sha256', 'raster_width_px', 'raster_height_px', 'geometry_status',
              'font_http', 'font_face', 'font_event', 'font_sha256', 'dpr', 'viewport_width_css_px',
              'viewport_height_css_px', 'document_width_css_px', 'block_width_css_px', 'main_words_by_line',
              'reference_words_by_line', 'summary_receipt', 'report_receipt', 'geometry_receipt']
WORD_FIELDS = ['run_id', 'page', 'role', 'block', 'selector', 'word_index', 'word', 'fragment', 'line',
               'x_css_px', 'y_css_px', 'width_css_px', 'height_css_px', 'geometry_receipt']


def read(path):
    return json.loads(path.read_text()) if path.is_file() and path.stat().st_size else {}


def join_page(blocks):
    return ' | '.join(' / '.join(row['text'] for row in block['rows']) for block in blocks)


def write(path, fields, rows):
    with path.open('w', newline='') as output:
        writer = csv.DictWriter(output, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main():
    runs = []
    words = []
    for test in MANIFEST['tests']:
        for engine, build in ENV['engines'].items():
            for repeat in (1, 2):
                run_id = f'{engine}-{test["id"]}-r{repeat}'
                run_dir = HERE / 'receipts' / 'primary' / run_id
                geometry_path = HERE / 'receipts' / 'geometry' / run_id / 'geometry.json'
                summary = read(run_dir / 'summary.json')
                geometry = read(geometry_path)
                pixels = summary.get('pixels', {})
                metadata = geometry.get('input', {})
                records = geometry.get('http', [])
                responsive_font = next((x for x in records if x['path'] == '/fonts/Ahem.ttf'), {})
                main_blocks = metadata.get('blocks', [])[:len(test['primary_blocks'])]
                raster = pixels.get('input_px', ['', ''])
                viewport = metadata.get('viewport', ['', ''])
                row = {
                    'run_id': run_id, 'test': test['id'], 'engine': engine, 'repeat': repeat,
                    'build': build['browser_version'], 'driver_build': build['driver_version'],
                    'runner_product': build['wpt_product'], 'status': summary.get('status', '미확인'),
                    'runner_exit': summary.get('runner_exit'), 'report_status': '|'.join(summary.get('report_status', [])),
                    'relation': summary.get('relation'), 'different_pixels': pixels.get('different_pixels'),
                    'input_sha256': pixels.get('input_sha256'), 'reference_sha256': pixels.get('reference_sha256'),
                    'diff_sha256': pixels.get('diff_sha256'), 'raster_width_px': raster[0], 'raster_height_px': raster[1],
                    'geometry_status': 'observed' if geometry else '미확인', 'font_http': responsive_font.get('status'),
                    'font_face': '|'.join(f"{x['family']}:{x['status']}" for x in metadata.get('faces', [])),
                    'font_event': '|'.join(event['type'] for event in metadata.get('fontEvents', [])),
                    'font_sha256': responsive_font.get('sha256'), 'dpr': metadata.get('dpr'),
                    'viewport_width_css_px': viewport[0], 'viewport_height_css_px': viewport[1],
                    'document_width_css_px': metadata.get('documentWidth'),
                    'block_width_css_px': '|'.join(str(block['width']) for block in main_blocks),
                    'main_words_by_line': join_page(main_blocks),
                    'reference_words_by_line': join_page(geometry.get('reference', {}).get('blocks', [])),
                    'summary_receipt': str((run_dir / 'summary.json').relative_to(HERE)) if summary else '',
                    'report_receipt': str((run_dir / 'wptreport.json').relative_to(HERE)) if summary.get('report_status') else '',
                    'geometry_receipt': str(geometry_path.relative_to(HERE)) if geometry else '',
                }
                runs.append(row)
                for page in ('input', 'reference'):
                    for index, block in enumerate(geometry.get(page, {}).get('blocks', []), 1):
                        role = 'external-reference' if page == 'reference' else (
                            'primary' if index <= len(test['primary_blocks']) else 'inline-comparison')
                        for word in block['words']:
                            for n, rect in enumerate(word['fragments'], 1):
                                words.append({
                                    'run_id': run_id, 'page': page, 'role': role, 'block': index,
                                    'selector': block['selector'], 'word_index': word['index'], 'word': word['text'],
                                    'fragment': n, 'line': rect['line'], 'x_css_px': rect['x'], 'y_css_px': rect['y'],
                                    'width_css_px': rect['width'], 'height_css_px': rect['height'],
                                    'geometry_receipt': str(geometry_path.relative_to(HERE)),
                                })
    write(HERE / 'runs.csv', RUN_FIELDS, runs)
    write(HERE / 'words.csv', WORD_FIELDS, words)
    print(f'{len(runs)} planned slots, {len(words)} measured fragment rows')


if __name__ == '__main__':
    main()
