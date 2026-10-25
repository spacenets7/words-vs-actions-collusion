"""Delivery integrity tests use development artifacts only, never held-out data."""
import copy
import tempfile
import unittest
from pathlib import Path

from pilot.core import load
from pilot.deliver import audit, export_data, ROOT


class Delivery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load(ROOT / 'pilot/runs/readiness-check/all.json')
        cls.metrics = load(ROOT / 'pilot/runs/readiness-check/analysis/metrics.json')
        cls.config = load(ROOT / 'pilot/frozen/config.json')

    def test_development_rehearsal_cannot_pass_as_complete_design(self):
        with self.assertRaisesRegex(ValueError, 'Incomplete design'):
            audit(self.data, self.metrics, self.config)
        result = audit(self.data, self.metrics, self.config, require_complete=False)
        self.assertEqual(result['held_out_episodes'], 0)
        self.assertEqual(len(result['missing_design_cells']), 48)

    def test_duplicate_cells_are_not_independent_samples(self):
        data = copy.deepcopy(self.data)
        data['episodes'].append(data['episodes'][0])
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            audit(data, self.metrics, self.config, require_complete=False)

    def test_saved_payoff_tampering_is_detected(self):
        data = copy.deepcopy(self.data)
        data['episodes'][0]['rounds'][0]['payoffs']['A'] += .5
        with self.assertRaisesRegex(ValueError, 'payoff'):
            audit(data, self.metrics, self.config, require_complete=False)

    def test_saved_label_tampering_is_detected(self):
        data = copy.deepcopy(self.data)
        data['episodes'][0]['labels']['implementation'] = True
        with self.assertRaisesRegex(ValueError, 'labels do not reproduce'):
            audit(data, self.metrics, self.config, require_complete=False)

    def test_public_export_separates_oracle_and_replays_metrics(self):
        import json
        from pilot.analysis import analyze
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            export_data(self.data, folder)
            read = lambda p: [json.loads(s) for s in p.read_text(encoding='utf-8').splitlines()]
            public = read(folder / 'public-trajectories.jsonl')
            self.assertTrue(all(set(ep) == {'episode_id', 'family_id', 'config_hash', 'valid', 'rounds'} for ep in public))
            oracle = {x['episode_id']: x for x in read(folder / 'oracle-labels.jsonl')}
            self.assertTrue(all('private' not in x and 'plans' not in x for x in oracle.values()))
            for ep in public:
                row = oracle[ep['episode_id']]
                ep['oracle'] = {'condition': row['condition'], 'typology': row['descriptive_typology']}
                ep['labels'] = row['automatic_labels']
            scores = {}
            for row in read(folder / 'monitor-evidence-and-outputs.jsonl'):
                if row['output'] is not None:
                    scores.setdefault(row['episode_id'], {})[row['view']] = row['output']
            replayed = analyze(public, scores, self.config['development_families'])
            self.assertEqual(replayed, self.metrics)


if __name__ == '__main__':
    unittest.main()
