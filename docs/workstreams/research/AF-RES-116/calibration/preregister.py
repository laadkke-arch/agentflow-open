#!/usr/bin/env python3
"""Construct and freeze the two calibration specifications before replay."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

OWN = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(OWN / 'viewer'))
from reader import Corpus

def now():
    return datetime.now(timezone.utc).isoformat()

def main():
    corpus = Corpus.load(OWN / 'corpus.json.gz')
    doc = corpus.documents['p383']
    def interval(quote, condition):
        a = doc['text'].index(quote)
        return dict(doc_id='p383',start=a,end=a+len(quote),quote=quote,condition=condition)
    common = dict(layer='constructed_calibration',author='/root',start_doc='p383',
                  start_url='https://pandoc.org/MANUAL.html',version='3.8.3',
                  corpus_sha256=corpus.sha256,created_utc=now(),
                  natural_sample_denominator=False,new_reader_choice_observed=False,
                  exposure='Root selected these questions after reading the four recorded manual views; authored natural hints were already remotely sealed and were not edited.')
    c1 = dict(common,case_id='K1',kind='reachable_positive',
        request='UTF-8 Markdown을 담은 input.txt를 독립 HTML 파일로 저장하고 한국어 문자 입출력의 인코딩 조건을 확인한다. 지역 인코딩이 UTF-8이 아니면 어떤 추가 처리가 필요한가?',
        operation='-s/--standalone 및 -o로 완전한 HTML 파일을 쓴다.',
        preservation='Pandoc의 입출력은 UTF-8이며 지역 인코딩이 다르면 iconv 변환이 필요하다. HTML 인코딩 헤더는 standalone일 때 포함된다.',
        witness_actions=['open','n3l3','n3l5'],
        required_intervals=[
            interval('To produce a standalone document (e.g. a valid HTML file including <head> and <body>), use the -s or --standalone flag:\npandoc -s -o output.html input.txt','operation'),
            interval('Pandoc uses the UTF-8 character encoding for both input and output. If your local character encoding is not UTF-8, you should pipe input and output through iconv:\niconv -t utf-8 input.txt | pandoc | iconv -f utf-8','preservation_and_exception'),
            interval('Note that in some output formats (such as HTML, LaTeX, ConTeXt, RTF, OPML, DocBook, and Texinfo), information about the character encoding is included in the document header, which will only be included if you use the -s/--standalone option.','exception')],
        minimal_source='Using pandoc + Character encoding',
        anticipated_result='Three visible-link opens can cover all required spans; replay must verify this without hidden navigation.',
        limits='A document-evidence control; no Pandoc conversion or byte-for-byte round trip is claimed.')
    c2 = dict(common,case_id='K2',kind='same_label_exception_trap',
        request='Markdown 제목 수준을 -1로 이동할 때 기존 제목 구조와 문서 제목의 처리 조건을 확인한다. 문서 첫 level-1 제목과 뒤에 나오는 level-1 제목이 같은 결과가 되는가?',
        operation='--shift-heading-level-by=-1로 제목 수준을 한 단계 올린다.',
        preservation='level 1보다 낮아질 제목은 일반 문단이 된다. 예외로 문서 시작의 level-N 제목은 -N 이동 때 메타데이터 title을 대체한다.',
        witness_actions=['open','n3l10'],
        near_wrong_actions=['open','n3l19','next'],
        near_wrong_label='Reader options',
        correct_fragment='reader-options',near_wrong_fragment='reader-options-1',
        required_intervals=[
            interval('Shift heading levels by a positive or negative integer. For example, with --shift-heading-level-by=-1, level 2 headings become level 1 headings, and level 3 headings become level 2 headings.','operation'),
            interval('Headings cannot have a level less than 1, so a heading that would be shifted below level 1 becomes a regular paragraph. Exception: with a shift of -N, a level-N heading at the beginning of the document replaces the metadata title.','preservation_and_exception')],
        anticipated_result='First Reader options contains semantics and exception; second identical label is a command/defaults mapping and two successive views omit the necessary heading exception.',
        limits='The wrong path is intentionally constructed after reference reading, not an observed reader mistake or a natural A/B/C outcome.')
    dest = OWN/'calibration'/'preregistered-cases.json'
    if dest.exists():
        raise SystemExit('Refusing to overwrite preregistration')
    dest.write_text(json.dumps([c1,c2],ensure_ascii=False,indent=2)+'\n')
    with (OWN/'calibration'/'exposure-log.jsonl').open('a') as f:
        f.write(json.dumps(dict(at_utc=now(),actor='/root',action='reread_saved_four_views',
            file='calibration/preselection-source-reads.jsonl',fully_seen_anchors=['using-pandoc','character-encoding','reader-options','reader-options-1'],
            original_read_utc='2026-11-24T04:26:17Z',original_transport='context overflow/truncation; complete exposure not assumed',
            reread_transport='four displays fully returned in one ~1582-token tool result',
            calibration_preregistered_before_replay=True,natural_hints_unchanged=True),ensure_ascii=False)+'\n')
    print(json.dumps({'output':str(dest),'cases':2,'executed_replays':0,'created_utc':now()}))

if __name__=='__main__': main()
