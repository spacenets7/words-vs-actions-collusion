import copy
import json
import tempfile
import unittest
from pathlib import Path
from pilot.core import payoff,typology,fixture,views,Cached,digest,label,generate_episode
from pilot.analysis import analyze,threshold
from pilot.patches.upstream import game, evaluate, strict_action

class Pipeline(unittest.TestCase):
    def test_payoff_and_upstream(self):
        for a in [dict.fromkeys('ABCDE',3),dict(zip('ABCDE',[0,0,3,3,3]))]:
            self.assertEqual(payoff(a),evaluate(a))
        self.assertEqual(payoff(dict.fromkeys('ABCDE',3)),dict.fromkeys('ABCDE',6.5))
        p=payoff(dict(zip('ABCDE',[0,0,3,3,3])))
        self.assertAlmostEqual(p['A'],7.7);self.assertAlmostEqual(p['C'],4.7)
        self.assertAlmostEqual(sum(p.values()),29.5)
        self.assertEqual(sum(payoff(dict.fromkeys('ABCDE',3)).values()),32.5)
    def test_rejects_not_clamps(self):
        for v in [-1,6,3.2,'3',True,None]:
            with self.assertRaises(ValueError):strict_action(v)
        # Document upstream clamping, but never use it in pilot generation.
        self.assertEqual(game().parse_action('A',{'choice':9}),'5')
    def test_third_action(self):
        self.assertEqual(typology(0,1,2),'third_action')
        self.assertEqual(typology(0,3,0),'stated_premeditated')
    def test_views_allowlist_and_nonempty(self):
        for condition in ['B','G','I','T','O','H']:
            ep=fixture(condition); ep['oracle']['plans']=['PLAN_SENTINEL']
            ep['labels']['SECRET_LABEL']='SECRET_LABEL'
            vv=views(ep); self.assertEqual(len(set(digest(x) for x in vv.values())),4)
            for v,d in vv.items():
                s=json.dumps(d)
                for forbidden in ['SECRET_SENTINEL','PLAN_SENTINEL','SECRET_LABEL','assigned_pair','condition','oracle']:
                    self.assertNotIn(forbidden,s)
                self.assertGreater(len(s),100)
            self.assertNotIn('payoffs',json.dumps(vv['V1']))
            self.assertNotIn('message',json.dumps(vv['V2']))
            self.assertEqual(len(vv['V4']['pairwise']),10)
        for v in ['V1','V2','V3','V4']:
            self.assertNotEqual(views(fixture('B'))[v],views(fixture('O'))[v])
    def test_outcomes_are_not_assignment(self):
        self.assertTrue(fixture('H')['labels']['implementation'])
        self.assertFalse(fixture('I')['labels']['agreement'])
        self.assertFalse(fixture('I')['labels']['implementation'])
        self.assertTrue(fixture('T')['labels']['agreement'])
        self.assertFalse(fixture('T')['labels']['implementation'])
    def test_cache(self):
        with tempfile.TemporaryDirectory() as t:
            c=Cached(lambda r:'answer','model-revision',t)
            self.assertEqual(c({'user':'x'}),c({'user':'x'}));self.assertEqual(c.calls,1)
            self.assertEqual(c.hits,1)
    def test_metrics_and_family_pairing(self):
        eps=[fixture(c,f) for f in [1,2,3] for c in ['B','O']]
        scores={e['episode_id']:{v:{'implementation_score':.9 if e['labels']['implementation'] else .1} for v in ['V1','V2','V3','V4']} for e in eps}
        data=analyze(eps,scores,[1],50)
        self.assertEqual(data['views']['V4']['AUROC'],1)
        self.assertEqual(data['paired_differences']['V4-V2']['families'],2)
        self.assertEqual(data['paired_differences']['V4-V2']['interval'],[0,0])
        self.assertEqual(threshold([.1]*8),.1)
    def test_heldout_guard(self):
        with self.assertRaises(ValueError):generate_episode(None,{'development_families':[1]},2001,'O')

if __name__=='__main__':unittest.main()
