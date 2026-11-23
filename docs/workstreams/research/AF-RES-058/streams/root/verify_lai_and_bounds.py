"""Independent aggregate audit; no participant records emitted or stored in output.

Run from repository root after the diagnostic author-data download. Uses stdlib.
The two hypothetical worlds are mathematical examples, never observed studies.
"""
from pathlib import Path
import collections
import datetime
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / 'diagnostics/_cache/lai-data/label.jsonlist.gz'
OUTPUT = ROOT / 'independent-calculation.json'

raw = DATA.read_bytes()
records = [json.loads(line) for line in gzip.decompress(raw).decode().splitlines()]
tables = []
for condition in ('machine', 'machine_and_heatmap'):
    rows = [r for r in records if r['experiment'] == condition]
    assert len(rows) == 1600
    assert len({(r['anonymized_worker_id'], r['review_num']) for r in rows}) == len(rows)
    cells = collections.Counter()
    for row in rows:
        assert row['predicted_label'] in (0, 1)
        assert row['user_label'] in (0, 1)
        assert row['actual_label'] in (0, 1)
        cells[(row['predicted_label'] == row['actual_label'],
               row['user_label'] == row['predicted_label'])] += 1
    n_correct = sum(n for (correct, accepted), n in cells.items() if correct)
    n_wrong = sum(n for (correct, accepted), n in cells.items() if not correct)
    final_correct = cells[True, True] + cells[False, False]
    assert n_correct + n_wrong == 1600
    tables.append(dict(condition=condition, people=len({r['anonymized_worker_id'] for r in rows}),
                       correct_advice_D=n_correct, wrong_advice_D=n_wrong,
                       accept_correct=cells[True, True], reject_correct=cells[True, False],
                       accept_wrong=cells[False, True], reject_wrong=cells[False, False],
                       final_correct=final_correct, total=1600))
control, intervention = tables
contrasts = dict(
    correct_advice_accept_pp=100*(intervention['accept_correct']/1395-control['accept_correct']/1395),
    wrong_advice_accept_pp=100*(intervention['accept_wrong']/205-control['accept_wrong']/205),
    final_correct_pp=100*(intervention['final_correct']/1600-control['final_correct']/1600),
)
# Two allowable joint tables with exactly the same stated margins in both arms.
worlds = []
for world, cells in [('W1', [('explanation',78,18), ('control',62,2)]),
                     ('W2', [('explanation',62,2), ('control',78,18)])]:
    arms=[]
    for arm, accept_correct, accept_wrong in cells:
        reject_correct=80-accept_correct;reject_wrong=20-accept_wrong
        final_correct=accept_correct+reject_wrong
        assert final_correct == 80
        assert accept_correct+reject_correct+accept_wrong+reject_wrong==100
        arms.append(dict(arm=arm,correct_advice_D=80,wrong_advice_D=20,
                         accept_correct=accept_correct,reject_correct=reject_correct,
                         accept_wrong=accept_wrong,reject_wrong=reject_wrong,
                         final_correct=final_correct,total=100))
    delta_wrong=(arms[0]['accept_wrong']-arms[1]['accept_wrong'])/20
    delta_correct=(arms[0]['accept_correct']-arms[1]['accept_correct'])/80
    worlds.append(dict(world=world,kind='constructed_not_observed',arms=arms,
                       delta_wrong_accept_pp=100*delta_wrong,
                       delta_correct_accept_pp=100*delta_correct))
result=dict(executed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            actor='root assistant, independent stdlib aggregation',
            command='python -B docs/workstreams/research/AF-RES-058/streams/root/verify_lai_and_bounds.py',
            input_url='https://raw.githubusercontent.com/vivlai/deception-machine-in-the-loop/7c5ae6bb4b7dcd5613e620e4731b9c3c67ed8285/label.jsonlist.gz',
            input_sha256=hashlib.sha256(raw).hexdigest(),study_tables=tables,
            study_contrasts=contrasts,constructed_worlds=worlds,
            limits=['No roster of all randomized or withdrawn people.',
                    'No pre-advice answer or reading/click log.',
                    'Descriptive trial ratios; no iid trial significance inference.',
                    'Toy margins fix AI correctness and final accuracy, not overall acceptance.',
                    'If binary forced choice and overall acceptance also known, w=(acceptance+Nwrong-finalcorrect)/2; this toy does not deny that identity.'])
OUTPUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
