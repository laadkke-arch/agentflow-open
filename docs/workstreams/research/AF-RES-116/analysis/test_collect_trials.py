#!/usr/bin/env python3
"""Three error-focused exporter checks using actual frozen reader logs."""
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import hashlib
import json
import unittest
from collect_trials import Corpus, collect, quote_matches, utc
from reader import run as reader_run

HERE=Path(__file__).resolve().parent
ENGINE=HERE.parent/'viewer/reader.py'


class ExportRiskTests(unittest.TestCase):
    def setUp(self):
        self.temp=TemporaryDirectory(prefix='synthetic-export-',dir=HERE)
        self.root=Path(self.temp.name);self.readers=self.root/'readers'
        self.path=self.root/'corpus.json'
        data={'schema':1,'documents':[{'id':'fixture','url':'https://example.invalid/manual','version':'synthetic-1','source_sha':'synthetic-only','text':'Alpha operation. Preservation unknown.\n','links':[],'anchors':{'start':0},'navigation_spans':[]}]}
        self.path.write_text(json.dumps(data));self.corpus=Corpus.load(self.path)
        self.engine_sha=hashlib.sha256(ENGINE.read_bytes()).hexdigest();self.packets=[]
        for i,condition in enumerate('ABC',1):
            request='Synthetic only';hint='' if condition=='A' else 'Synthetic hint';full=request+'\n'+hint
            self.packets.append({'packet_id':f'r{i:02d}','case_id':'fixture-case','condition':condition,'layer':'synthetic','start_doc_id':'fixture','start_url':'https://example.invalid/manual','document_version':'synthetic-1','corp_sha256':self.corpus.sha256,'common_request':request,'hint':hint,'full_packet_text':full,'hint_codepoints':len(hint),'hint_utf8_bytes':len(hint.encode()),'request_codepoints':len(request),'request_utf8_bytes':len(request.encode()),'packet_codepoints':len(full),'packet_utf8_bytes':len(full.encode()),'case_condition_order':'ABC'})

    def tearDown(self):self.temp.cleanup()

    def call(self,sid,command,**kw):
        args=dict(session=sid,sessions=str(self.readers),command=command,corpus=str(self.path),start_doc='fixture',start_offset=0,reader_id='synthetic-only',reason='Read fixture.',action='again',json=None,operation='Alpha is visible.',preservation='Unknown.',exceptions='Unknown.',disposition='Hold.',citations_json='[{"doc_id":"fixture","quote":"Alpha operation."}]',notes='',stop=False,summary='Synthetic log only')
        args.update(kw);return reader_run(SimpleNamespace(**args))

    def make_session(self,sid,count):
        self.call(sid,'init')
        for i in range(count):
            self.call(sid,'open' if i==0 else 'choose');self.call(sid,'answer')
        self.call(sid,'finish',stop=count<3)

    def collect(self):return collect(self.packets,self.readers,self.corpus,self.engine_sha,expected_packets=3)

    def test_01_chain_tamper_is_retained_but_not_verified(self):
        self.make_session('r01',1)
        path=self.readers/'r01/events.jsonl'
        path.write_text(path.read_text().replace('Read fixture.','Altered after recording.'))
        out=self.collect()
        self.assertFalse(out['summary']['protocol_audit_passed'])
        self.assertEqual(out['summary']['validated_logged_exposures'],0)
        self.assertEqual(len(out['trails']),1)
        self.assertFalse(out['trails'][0]['session_audit_valid'])
        self.assertFalse(out['citation_checks'][0]['verified_quote_presence'])

    def test_02_quote_cannot_bridge_gap_or_wrong_document(self):
        docs={'d':{'text':'ABCDEFGHIJKLMNO'},'other':{'text':'ABCDEFGHIJKLMNO'}}
        def view(a,b,did='d'):
            return {'doc_id':did,'offset_start':a,'offset_end':b,'display_text':docs[did]['text'][a:b],'display_sha256':'synthetic'}
        gap=[view(0,5),view(10,15)]
        for quote in ['ABCDEKLMNO','ABCDEFGHIJKLMNO']:
            result=quote_matches({'doc_id':'d','quote':quote},gap,docs)
            self.assertFalse(result['strict_supported'])
        contiguous=[view(0,5),view(5,10)]
        self.assertTrue(quote_matches({'doc_id':'d','quote':'CDEFGHI'},contiguous,docs)['strict_supported'])
        wrong=quote_matches({'doc_id':'other','quote':'ABCDE'},gap,docs)
        self.assertEqual(wrong['match_status'],'quote_visible_only_in_different_document')
        self.assertFalse(wrong['strict_supported'])

    def test_03_planned_slots_and_real_engine_sequence_reconcile(self):
        empty=self.collect()
        self.assertEqual(empty['summary']['stage_status_counts'],{'observed':0,'early_stop':0,'unstarted':9})
        self.assertTrue(empty['summary']['protocol_audit_passed'])
        self.make_session('r01',3);self.make_session('r02',1)
        out=self.collect();s=out['summary']
        self.assertTrue(s['protocol_audit_passed'],s['audit_errors'])
        self.assertEqual(s['packet_status_counts'],{'observed':1,'early_stop':1,'unstarted':1})
        self.assertEqual(s['stage_status_counts'],{'observed':4,'early_stop':2,'unstarted':3})
        self.assertEqual(s['validated_logged_exposures'],4)
        self.assertEqual(s['citation_counts']['verified_quote_presence'],4)
        self.assertTrue(all(x['answer_original'] is not None for x in out['trails']))
        self.assertTrue(all(x['semantic_grade']=='not_evaluated' for x in out['trails']))


if __name__=='__main__':
    start=utc();suite=unittest.defaultTestLoader.loadTestsFromTestCase(ExportRiskTests);result=unittest.TextTestRunner(verbosity=2).run(suite)
    receipt={'method':'three_synthetic_exporter_error_checks','started_utc':start,'finished_utc':utc(),'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'successful':result.wasSuccessful(),'exporter_sha256':hashlib.sha256((HERE/'collect_trials.py').read_bytes()).hexdigest(),'frozen_reader_sha256':hashlib.sha256(ENGINE.read_bytes()).hexdigest(),'natural_trials_added':0,'checks':['unrehashed choice tampering retains evidence while invalidating audit','quotes do not bridge unshown gaps or wrong documents; contiguous seen spans work','empty roster and actual-reader completed/early-stop/missing sessions reconcile exactly']}
    (HERE/'exporter-synthetic-checks.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
