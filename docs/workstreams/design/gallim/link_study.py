"""Offline link-first comparison on AF-RES-012. Python 3.10+, standard library."""
import argparse
import csv
import hashlib
import io
import json
import math
import re
import subprocess
import unicodedata
from collections import Counter
from pathlib import Path
from statistics import mean


PIN = 'cb602858378db90adb1f085953016267f9afbd6d'
STUDY = 'docs/workstreams/research/AF-RES-012'
VARIANTS = ('URL', 'URL+한줄', 'URL+한줄+용도')
EXAMPLES = [('P03.w', 'toyota-jit'), ('P1.w', 'bazel-cache'),
            ('P2.w', 'forking-histories'), ('K02.2', 'paperless-ngx')]


def read_file(source, name):
    if (source / 'corpus/entries.jsonl').is_file():
        return (source / name).read_bytes().decode('utf-8')
    return subprocess.check_output(
        ['git', '-C', str(source), 'show', f'{PIN}:{STUDY}/{name}']
    ).decode('utf-8')


def tokens(text):
    return re.findall(r'[^\W_]+', unicodedata.normalize('NFKC', text).casefold())


def projections(entries, lang):
    all_docs = {name: {} for name in VARIANTS}
    for row in entries:
        url, title, desc = row['url'], row['D-a'][lang], row['D-b'][lang]
        prefix = row['name'] + ' — '
        assert desc.startswith(prefix)
        fields = [url, title, desc.removeprefix(prefix)]
        for n, name in enumerate(VARIANTS, 1):
            all_docs[name][row['id']] = fields[:n]
    return all_docs


def rankings(docs, queries, lang):
    words = {key: Counter(tokens(' '.join(fields))) for key, fields in docs.items()}
    lengths = {key: sum(counts.values()) for key, counts in words.items()}
    avg_len = mean(lengths.values())
    df = Counter(term for counts in words.values() for term in counts)
    idf = {term: math.log1p((len(words) - freq + 0.5) / (freq + 0.5))
           for term, freq in df.items()}
    tie = {key: hashlib.sha256(('12012:' + key).encode()).digest() for key in words}
    result = {}
    for question in queries:
        query = Counter(tokens(question[lang]))
        scored = []
        for key, counts in words.items():
            norm = 1.5 * (0.25 + 0.75 * lengths[key] / avg_len)
            score = sum(n * idf[term] * counts[term] * 2.5 / (counts[term] + norm)
                        for term, n in query.items() if term in counts)
            if score > 0:
                scored.append((-score, tie[key], key))
        result[question['id']] = [key for _, _, key in sorted(scored)]
    return result


def output_row(*cols):
    print('| ' + ' | '.join(str(x) for x in cols) + ' |')


def study(source):
    def jsonl(path):
        return [json.loads(line) for line in read_file(source, path).splitlines()]

    entries, queries = jsonl('corpus/entries.jsonl'), jsonl('queries/queries.jsonl')
    roles = {row['id']: row['role'] for row in entries}
    subset = {q['id']: q['whole_or_part'] for q in queries}
    assert len(entries) == len(roles) == 156 and len(queries) == len(subset) == 36
    # Retrieval sees only the three existing representations, never the judgments.
    runs = []
    for lang in ('ko', 'en'):
        for name, docs in projections(entries, lang).items():
            ranks = rankings(docs, queries, lang)
            field_bytes = sum(len(f.encode('utf-8')) for fields in docs.values() for f in fields)
            jsonl_bytes = sum(len((json.dumps([key, *fields], ensure_ascii=False,
                              separators=(',', ':')) + '\n').encode('utf-8'))
                              for key, fields in docs.items())
            runs.append((lang, name, ranks, field_bytes, jsonl_bytes))

    seed = {}
    pool = {}
    for path, dst in [('qrels/qrels.tsv', seed), ('results/pooled_judgments.tsv', pool)]:
        for row in csv.DictReader(io.StringIO(read_file(source, path)), delimiter='\t'):
            key = row['query_id'], row['entry_id']
            assert key not in dst and key[0] in subset and key[1] in roles
            dst[key] = row['grade']
    assert seed.keys().isdisjoint(pool)
    all_grades = seed | pool

    def eligible(g, group, q, e):
        if g not in {'1', '2'}:
            return False
        if group == '원리':
            return roles[e] == 'principle'
        if group == '부분 질의':
            return subset[q] == 'part'
        if group == '조건부 등급 1':
            return g == '1'
        return True

    def recall(grades, group, ranks):
        gold = {q: set() for q in subset}
        for (q, e), g in grades.items():
            if eligible(g, group, q, e):
                gold[q].add(e)
        ratios = [len(set(ranks[q][:10]) & ids) / len(ids) for q, ids in gold.items() if ids]
        return f'{mean(ratios):.3f}', len(ratios), sum(map(len, gold.values()))

    print('## 실측 표\n')
    output_row('언어·표현', '저장 필드 B', 'JSONL B', 'B/건', '직전 대비 B/건', '전체 R@10',
               '부분 질의 R@10', '원리 R@10', '등급 1 R@10', 'N/반환', '미판정/반환',
               '무응답 질의/36', '최초 판정만 R@10')
    print('| ' + ' | '.join(['---'] * 12) + ' |')
    for lang, name, ranks, field_bytes, jsonl_bytes in runs:
        if name == 'URL':
            last = None
        returned = [(q, e) for q, ids in ranks.items() for e in ids[:10]]
        unknown = sum(key not in all_grades for key in returned)
        bad = sum(all_grades.get(key) == 'N' for key in returned)
        groups = ('전체', '부분 질의', '원리', '조건부 등급 1')
        scores = [recall(all_grades, group, ranks)[0] for group in groups]
        output_row(f'{lang} {name}', field_bytes, jsonl_bytes, f'{jsonl_bytes / 156:.1f}',
                   '—' if last is None else f'{(jsonl_bytes - last) / 156:.1f}', *scores,
                   f'{bad}/{len(returned)}', f'{unknown}/{len(returned)}',
                   f'{sum(not ids for ids in ranks.values())}/36', recall(seed, '전체', ranks)[0])
        last = jsonl_bytes

    print('\n관련 분모(질의 수/관련 쌍 수) · ' + ' / '.join(
        f'{group} {nq}/{nd}' for group in ('전체', '부분 질의', '원리', '조건부 등급 1')
        for _, nq, nd in [recall(all_grades, group, runs[0][2])]))
    print(f'\n최초 판정 {len(seed)}, 추가 판정 {len(pool)}, 가능한 쌍 {len(roles)*len(subset)}.')

    print('\n### 기존 연구가 언급한 진단 사례\n')
    output_row('질의와 안정 ID', '등급', '언어', *VARIANTS, 'URL에서 겹친 어휘')
    print('| --- | --- | --- | --- | --- | --- | --- |')
    raw_urls = {row['id']: row['url'] for row in entries}
    raw_queries = {row['id']: row for row in queries}
    for q, e in EXAMPLES:
        for lang in ('ko', 'en'):
            values = []
            for run_lang, name, ranks, _, _ in runs:
                if lang == run_lang:
                    values.append(ranks[q].index(e) + 1 if e in ranks[q] else '일치어 없음')
            overlap = set(tokens(raw_queries[q][lang])) & set(tokens(raw_urls[e]))
            output_row(f'{q} · {e}', all_grades.get((q, e), '미판정'), lang, *values,
                       ', '.join(sorted(overlap)) or '없음')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='Git repo containing the pinned AF-RES-012 commit, or pinned study directory')
    study(parser.parse_args().source)
