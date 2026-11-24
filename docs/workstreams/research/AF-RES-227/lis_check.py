#!/usr/bin/env python3
"""Check the card and Sage examples against an independent pinned DP implementation."""
from bisect import bisect_left
from itertools import combinations, pairwise
import argparse
import doctest
import hashlib
import importlib.util
import json
from pathlib import Path

PIN = 'f506b58c91a55529c5efb42e168e6984140224feeb634c217f498206f4e48a3a'


def strict_witnesses(values):
    for length in range(len(values), -1, -1):
        witnesses = [list(s) for s in combinations(values, length)
                     if all(x < y for x, y in pairwise(s))]
        if witnesses:
            return sorted(witnesses, reverse=True)


def greedy_witness(values):
    tails, top_indices = [], []
    previous = [None] * len(values)
    for index, value in enumerate(values):
        pile = bisect_left(tails, value)
        if pile:
            previous[index] = top_indices[pile - 1]
        if pile == len(tails):
            tails.append(value)
            top_indices.append(index)
        else:
            tails[pile], top_indices[pile] = value, index
    witness = []
    index = top_indices[-1] if top_indices else None
    while index is not None:
        witness.append(values[index])
        index = previous[index]
    return tails, witness[::-1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dp_source', type=Path)
    args = parser.parse_args()
    if hashlib.sha256(args.dp_source.read_bytes()).hexdigest() != PIN:
        raise ValueError('unverified TheAlgorithms Python module')
    spec = importlib.util.spec_from_file_location('lis_dp', args.dp_source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    doctests = doctest.testmod(module, verbose=False)
    if doctests.failed:
        raise RuntimeError(doctests)

    examples = {
        '210_CE1': [2, 3, 1],
        'C2_rank': [2, 1],
        '210_two_witnesses': [2, 1, 3],
        'A01_pile_example': [7, 2, 8, 1, 3, 4, 10, 6, 9, 5],
        'E01_Sage_example': [5, 7, 1, 2, 6, 4, 3],
        'E04_doctest': [10, 22, 9, 33, 21, 50, 41, 60, 80],
        'nondecreasing_boundary': [1, 1, 1],
    }
    reports = []
    for name, values in examples.items():
        all_strict = strict_witnesses(values)
        tails, greedy = greedy_witness(values)
        dp = module.longest_subsequence(values)
        if greedy not in all_strict or (len(set(values)) == len(values) and dp not in all_strict):
            raise ValueError(f'{name}: invalid strict witness')
        reports.append({'id': name, 'input': values, 'strict_length': len(greedy),
                        'all_strict': all_strict, 'final_tops': tails, 'greedy': greedy,
                        'dp_nondecreasing': dp, 'dp_is_maximal_strict': dp in all_strict})
    print(json.dumps({'pinned_module_sha256': PIN, 'upstream_doctest_count': doctests.attempted, 'examples': reports}))


if __name__ == '__main__':
    main()
