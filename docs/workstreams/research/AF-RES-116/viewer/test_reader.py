#!/usr/bin/env python3
"""Synthetic checks of actual study risks; these are not natural reader trials."""
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import json
import gzip
import unittest
from reader import Corpus, run, read_events, digest, utc
from enumerate_paths import enumerate_paths, replay

HERE=Path(__file__).resolve().parent


def fixture():
    t='Guide\n[first] Operation\n'+'α'*1315+'\n[late] Exception\n'+'끝'*200
    first=t.index('[first]');late=t.index('[late]')
    return {'schema':1,'documents':[
        {'id':'guide','url':'https://example.invalid/guide','version':'fixture-1','source_sha':'synthetic-only','text':t,
         'links':[{'id':'first','start':first,'end':first+len('[first] Operation'),'label':'Operation','target_doc':'detail','target_offset':0},
                  {'id':'late','start':late,'end':late+len('[late] Exception'),'label':'Exception','target_doc':'detail','target_offset':25}],
         'anchors':{'guide':0},'navigation_spans':[{'start':0,'end':first+len('[first] Operation')},{'start':late,'end':late+len('[late] Exception')}]},
        {'id':'detail','url':'https://example.invalid/detail','version':'fixture-1','source_sha':'synthetic-only','text':'Operation preserves hue.\nException: transparency needs separate proof.\n','links':[],'anchors':{'operation':0,'exception':25}}
    ]}


class ReaderRiskTests(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory(prefix='synthetic-',dir=HERE)
        self.root=Path(self.tmp.name)
        self.path=self.root/'corpus.json'
        self.path.write_text(json.dumps(fixture(),ensure_ascii=False))
        self.corpus=Corpus.load(self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def call(self,session,command,**kw):
        d=dict(session=session,sessions=str(self.root/'sessions'),command=command,
            corpus=str(self.path),start_doc='guide',start_offset=0,reader_id='synthetic-test',
            reason='test selection',action='',json=None,operation='unknown',preservation='unknown',exceptions='unknown',disposition='hold',citations_json='[]',notes='',stop=False,summary='fixture only')
        d.update(kw)
        return run(SimpleNamespace(**d))

    def events(self,session):
        with (self.root/'sessions'/session/'events.jsonl').open() as f:return read_events(f)

    def test_01_total_budget_unicode_and_whole_tokens(self):
        a=self.corpus.render('guide',0)
        self.assertLessEqual(len(a['display_text']),1500)
        self.assertEqual(a['display_codepoints'],a['body_codepoints']+a['navigation_codepoints'])
        self.assertEqual(a['display_utf8_bytes'],a['body_utf8_bytes']+a['navigation_utf8_bytes'])
        self.assertEqual(a['display_codepoints'],a['content_codepoints']+a['total_navigation_codepoints'])
        self.assertEqual(a['display_utf8_bytes'],a['content_utf8_bytes']+a['total_navigation_utf8_bytes'])
        self.assertGreater(a['display_utf8_bytes'],a['display_codepoints'])
        self.assertEqual(a['visible_link_ids'],['first'])
        b=self.corpus.render('guide',a['next_offset'])
        self.assertIn('late',b['visible_link_ids'])
        self.assertEqual(a['body_text']+b['body_text'],fixture()['documents'][0]['text'])

    def test_02_hidden_link_and_answer_before_next(self):
        self.call('r01','init');self.call('r01','open')
        with self.assertRaisesRegex(ValueError,'answer before'):self.call('r01','choose',action='next')
        self.call('r01','answer')
        with self.assertRaisesRegex(ValueError,'not been fully shown'):self.call('r01','choose',action='late')
        self.assertEqual(len([e for e in self.events('r01') if e['event']=='exposure']),1)
        self.call('r01','choose',action='next')
        self.call('r01','answer')
        self.call('r01','choose',action='first')  # Remembered from stage one.
        self.call('r01','answer')
        with self.assertRaisesRegex(ValueError,'budget exhausted'):self.call('r01','choose',action='again')
        self.call('r01','finish')
        self.assertEqual(len([e for e in self.events('r01') if e['event']=='exposure']),3)

    def test_03_identical_input_same_display_and_immutable_answers(self):
        outputs=[]
        for sid in ['ra','rb']:
            self.call(sid,'init');outputs.append(self.call(sid,'open'));self.call(sid,'answer')
        self.assertEqual(outputs[0],outputs[1])
        with self.assertRaisesRegex(ValueError,'already sealed'):self.call('ra','answer')
        with self.assertRaisesRegex(ValueError,'explicit --stop'):self.call('ra','finish')
        self.call('ra','finish',stop=True)
        self.assertEqual(self.events('ra')[-1]['unobserved_early_stop_positions'],2)

    def test_04_enumeration_and_replay_cover_actions(self):
        nodes,views,summary=enumerate_paths(self.corpus,'guide')
        self.assertTrue(summary['enumeration_complete'])
        allpaths={tuple(x['actions']) for x in nodes}
        self.assertIn(('open','next','first'),allpaths)
        self.assertNotIn(('open','late'),allpaths)
        self.assertIn(('open','first','back'),allpaths)
        for node in nodes:
            witness=replay(self.corpus,'guide',node['actions'])
            self.assertEqual([x['view']['display_sha256'] for x in witness['steps']], [views[key]['display_sha256'] for key in node['views']])
        _,_,cut=enumerate_paths(self.corpus,'guide',max_nodes=2)
        self.assertFalse(cut['enumeration_complete'])
        self.assertGreater(cut['remaining_queue_entries'],0)

    def test_05_corpus_and_event_tamper_are_detected(self):
        self.call('r01','init');self.call('r01','open')
        old=self.path.read_text();self.path.write_text(old+' ')
        with self.assertRaisesRegex(ValueError,'corpus changed'):self.call('r01','answer')
        self.path.write_text(old)
        path=self.root/'sessions/r01/events.jsonl'
        events=path.read_text().replace('test selection','changed selection')
        path.write_text(events)
        with self.assertRaisesRegex(ValueError,'event chain changed'):self.call('r01','answer')

    def test_06_gzip_equivalence_and_input_bytes_hash(self):
        compressed=gzip.compress(self.path.read_bytes(),mtime=0)
        gz=self.root/'corpus.json.gz';gz.write_bytes(compressed)
        renamed=self.root/'magic-only.dat';renamed.write_bytes(compressed)
        for p in [gz,renamed]:
            loaded=Corpus.load(p)
            self.assertEqual(loaded.sha256,digest(compressed))
            self.assertNotEqual(loaded.sha256,self.corpus.sha256)
            self.assertEqual(loaded.documents,self.corpus.documents)
            self.assertEqual(loaded.render('guide',0)['display_text'],self.corpus.render('guide',0)['display_text'])


if __name__=='__main__':
    started=utc()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ReaderRiskTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    receipt={'method':'synthetic_engine_risk_checks','started_utc':started,'finished_utc':utc(),'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'successful':result.wasSuccessful(),'engine_sha256':digest((HERE/'reader.py').read_bytes()),'enumerator_sha256':digest((HERE/'enumerate_paths.py').read_bytes()),'test_sha256':digest(Path(__file__).read_bytes()),'natural_trials_added':0,'synthetic_fixture_documents':2,'checks':['whole display budget, Unicode vs bytes, no dropped text','hidden link blocked, answer-before-next, remembered links, maximum opens','same display independent of session label, immutable answers, early stop slots','all permitted action paths and exact witness replay, cutoff does not mean impossible','fixed corpus and event-chain tamper detection','gzip suffix/magic loading preserves exact display and hashes actual compressed input bytes']}
    (HERE/'synthetic-checks.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
