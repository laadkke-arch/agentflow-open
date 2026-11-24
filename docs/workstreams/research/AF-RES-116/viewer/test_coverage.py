#!/usr/bin/env python3
"""Synthetic coverage risks: no joining across gaps/documents or false negatives."""
from pathlib import Path
import hashlib
import json
import unittest
from analyze_coverage import Graph, union_intervals, covered, normalize_interval, analyze_mode, utc


class CoverageRiskTests(unittest.TestCase):
    def test_contiguous_union_and_overlapping_duplicates(self):
        u=union_intervals([{'doc_id':'d','start':0,'end':10},{'doc_id':'d','start':10,'end':20},{'doc_id':'d','start':4,'end':8}])
        self.assertEqual(u,{'d':[[0,20]]})
        self.assertTrue(covered(u,{'doc_id':'d','start':2,'end':19}))

    def test_unread_gap_and_different_documents_cannot_be_stitched(self):
        u=union_intervals([{'doc_id':'d','start':0,'end':10},{'doc_id':'d','start':11,'end':20},{'doc_id':'other','start':10,'end':11}])
        self.assertFalse(covered(u,{'doc_id':'d','start':0,'end':20}))
        self.assertTrue(covered(u,{'doc_id':'d','start':11,'end':20}))
        self.assertFalse(covered(u,{'doc_id':'missing','start':0,'end':1}))

    def graph(self,complete=True):
        def row(node,depth,ints,actions,views):
            return {'node_id':node,'depth':depth,'intervals':ints,'visible_union':union_intervals(ints),'actions':actions,'views':views,'cumulative_display_codepoints':100*depth,'cumulative_display_utf8_bytes':100*depth}
        first={'doc_id':'d','start':0,'end':10};second={'doc_id':'d','start':10,'end':20}
        return Graph(Path('synthetic-only'),{'enumeration_complete':complete,'start_doc':'d'},[row('n1',1,[first],['open'],['v1']),row('n2',2,[first,second],['open','next'],['v1','v2'])],{'v1':{'display_sha256':'synthetic1'},'v2':{'display_sha256':'synthetic2'}},[])

    def test_graph_semantic_and_missing_input_are_separate(self):
        case={'case_id':'fixture','semantic_gold_complete':False}
        mode={'alternatives':[[{'doc_id':'d','start':0,'end':20}]]}
        summary,matches=analyze_mode(case,'full',mode,self.graph(),{'d':100})
        self.assertEqual(summary['earliest_depth'],2)
        self.assertEqual(summary['interval_reachability'],'reachable')
        self.assertEqual(summary['semantic_reachability'],'unknown')
        case['semantic_gold_complete']=True
        case['missing_inputs']=['unread exception source']
        summary,_=analyze_mode(case,'full',mode,self.graph(),{'d':100})
        self.assertEqual(summary['semantic_reachability'],'unknown')
        case['missing_inputs']=[]
        nohit={'alternatives':[[{'doc_id':'d','start':50,'end':60}]]}
        summary,_=analyze_mode(case,'full',nohit,self.graph(False),{'d':100})
        self.assertEqual(summary['semantic_reachability'],'unknown')
        summary,_=analyze_mode(case,'full',nohit,self.graph(True),{'d':100})
        self.assertEqual(summary['semantic_reachability'],'unreachable_in_fixed_viewer')

    def test_or_alternatives_outside_and_empty_are_explicit(self):
        case={'case_id':'fixture','semantic_gold_complete':True}
        mode={'alternatives':[[{'doc_id':'d','start':50,'end':60}],[{'doc_id':'d','start':0,'end':10}]]}
        summary,matches=analyze_mode(case,'operation',mode,self.graph(),{'d':100})
        self.assertEqual(summary['earliest_depth'],1)
        self.assertEqual(len(matches),2)
        outside={'alternatives':[[{'doc_id':'external','start':0,'end':10}]]}
        summary,_=analyze_mode(case,'full',outside,self.graph(),{'d':100})
        self.assertEqual(summary['semantic_reachability'],'unreachable_in_fixed_viewer')
        self.assertEqual(len(summary['outside_corpus_intervals']),1)
        empty={'alternatives':[[]]}
        summary,_=analyze_mode(case,'full',empty,self.graph(),{'d':100})
        self.assertEqual(summary['matching_paths'],0)
        self.assertEqual(summary['semantic_reachability'],'unknown')
        self.assertEqual(normalize_interval({'doc_id':'d','start':0,'end':101},{'d':100})['classification'],'invalid')


if __name__=='__main__':
    before=utc();suite=unittest.defaultTestLoader.loadTestsFromTestCase(CoverageRiskTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    here=Path(__file__).resolve().parent
    receipt={'method':'synthetic_coverage_helper_risk_checks','started_utc':before,'finished_utc':utc(),'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'successful':result.wasSuccessful(),'helper_sha256':hashlib.sha256((here/'analyze_coverage.py').read_bytes()).hexdigest(),'natural_cases_analyzed':0,'reader_or_corpus_modified':False}
    (here/'coverage-synthetic-checks.json').write_text(json.dumps(receipt,indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
