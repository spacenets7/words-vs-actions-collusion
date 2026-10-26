"""Deterministic, offline checks against the supplied PDFs and released source.

No model providers, keys, Docker images, or paid APIs are used. Where imports
would require the full agent framework, selected ORIGINAL AST definitions are
executed with small data objects. These are component checks, not reruns of the
papers' model experiments. All arithmetic inputs come from named PDF tables.
"""
from __future__ import annotations
import ast
import asyncio
import csv
import dataclasses
import hashlib
import importlib.util
import itertools
import json
import logging
import math
import re
import runpy
import statistics
import subprocess
import sys
import types
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "audit/evidence"
RESULTS = {}
print("Starting offline component checks", flush=True)

def selected(path, names, injected=None):
    """Load named definitions verbatim, omitting unrelated framework imports."""
    path = ROOT / path
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    chosen = []
    for node in tree.body:
        name = getattr(node, "name", None)
        if isinstance(node, ast.Assign):
            name = next((n.id for n in node.targets if isinstance(n, ast.Name)), None)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            name = node.target.id
        if name in names:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                node.decorator_list = []
            chosen.append(node)
    if len(chosen) != len(names):
        raise ValueError((path, names, [getattr(n, "name", None) for n in chosen]))
    module_name = "audit_component_" + hashlib.sha256(str(path).encode()).hexdigest()[:12]
    module = types.ModuleType(module_name)
    sys.modules[module_name] = module
    namespace = module.__dict__
    namespace.update(dict(np=np, pd=pd, Path=Path, re=re, math=math,
                          dataclass=dataclasses.dataclass, field=dataclasses.field,
                          replace=dataclasses.replace))
    namespace.update(injected or {})
    future = ast.ImportFrom(module="__future__", names=[ast.alias(name="annotations")], level=0)
    code = ast.fix_missing_locations(ast.Module(body=[future] + chosen, type_ignores=[]))
    exec(compile(code, str(path), "exec"), namespace)
    return namespace

def pages(stem):
    return (ROOT / f"audit/text/{stem}.layout.txt").read_text(encoding="utf-8").split("\f")

def wilson(k, n, z=1.959963984540054):
    center = (k/n + z*z/(2*n)) / (1 + z*z/n)
    half = z * math.sqrt((k/n)*(1-k/n)/n + z*z/(4*n*n)) / (1+z*z/n)
    return [center-half, center+half]

# TraceGuard: the locked ControlArena formatter never appends missing fields.
print("TraceGuard", flush=True)
baseline = selected("repos/TraceGuard/src/traceguard/monitors/baseline_monitors.py", ["BASELINE_PROMPT"])
class Assistant:
    def __init__(self, command):
        self.tool_calls = [SimpleNamespace(function="bash", arguments={"cmd": command})]
formatter = selected("audit/evidence/_last_tool_calls_prompt_formatter.py",
                     ["last_tool_calls_message_formatter", "last_tool_calls_prompt_formatter"],
                     {"ChatMessageAssistant": Assistant})
formatted = [formatter["last_tool_calls_prompt_formatter"](
    SimpleNamespace(main_task_description="TASK_SENTINEL"), [Assistant(command)], baseline["BASELINE_PROMPT"])
    for command in ["BENIGN_SENTINEL", "ATTACK_SENTINEL"]]
assert formatted[0] == formatted[1]
assert all(s not in formatted[0] for s in ["TASK_SENTINEL", "BENIGN_SENTINEL", "ATTACK_SENTINEL"])
RESULTS["traceguard_blind_baselines"] = {"different_actions_identical_prompt": True,
    "task_and_action_sentinels_present": False, "formatter_dependency": "control-arena 14.2.0"}

dims = runpy.run_path(str(ROOT / "repos/TraceGuard/src/traceguard/dimensions.py"))
heuristic = selected("repos/TraceGuard/src/traceguard/monitors/bash_heuristic_monitor.py",
    ["CATEGORY_DIMENSION_BOOST", "apply_category_boosts"])
weights = [d.weight for d in dims["DEFAULT_DIMENSIONS"]]
attack = [.849, .870, .893, .682, .845]
honest = [.617, .753, .804, .642, .801]
all_reweightings = []
categories = list(heuristic["CATEGORY_DIMENSION_BOOST"])
for n in range(5):
    for subset in itertools.combinations(categories, n):
        adjusted = heuristic["apply_category_boosts"](dims["DEFAULT_DIMENSIONS"], list(subset), heuristic["CATEGORY_DIMENSION_BOOST"])
        tv = sum(abs(d.weight-w) for d, w in zip(adjusted, weights))/2
        boost = min(.3*len(subset), .6)
        # For scores in [0,1], reweighting can lower a mean by at most TV.
        assert tv <= boost + 1e-12
        all_reweightings.append({"categories": subset, "total_variation": tv, "regex_boost": boost})
RESULTS["traceguard_table3"] = {"weighted_attack": sum(w*s for w,s in zip(weights,attack)),
    "weighted_honest": sum(w*s for w,s in zip(weights,honest)),
    "reported_composites": [.616,.206], "reweighting_checks": all_reweightings,
    "reason": "For all 16 implemented category subsets, regex boost offsets the largest possible decrease from reweighting; other boosts are nonnegative."}

monitor = selected("repos/TraceGuard/src/traceguard/monitors/traceguard_monitor.py",
    ["compute_disagreement_boost", "_evaluate_trace"],
    {"TraceGuardResult": dims["TraceGuardResult"]})
async def supplied_score(dim, *args, **kwargs):
    value = attack[[d.name for d in dims["DEFAULT_DIMENSIONS"]].index(dim.name)]
    return dims["DimensionScore"](dim.name, value*10, value, "synthetic input, no LLM")
monitor["_score_dimension"] = supplied_score
evaluated = asyncio.run(monitor["_evaluate_trace"](dims["DEFAULT_DIMENSIONS"], "T", "R", "A", "trusted"))
assert abs(evaluated.composite_score - .8466) < 1e-12
RESULTS["traceguard_original_aggregator_smoke"] = {"composite": evaluated.composite_score}

pareto = selected("repos/TraceGuard/src/traceguard/analysis/pareto.py", ["ParetoPoint", "compute_pareto_points"])
df = pd.DataFrame([{"monitor_name":"A", "mode":"attack", "max_suspicion":1., "main_task_success":False},
                   {"monitor_name":"A", "mode":"honest", "max_suspicion":0., "main_task_success":False},
                   {"monitor_name":"B", "mode":"attack", "max_suspicion":0., "main_task_success":False},
                   {"monitor_name":"B", "mode":"honest", "max_suspicion":1., "main_task_success":False}])
pooled = pareto["compute_pareto_points"](df, ["A","B"], [.5])
assert all(p.safety == .5 and p.usefulness == .5 for p in pooled)
failed_honest = pareto["compute_pareto_points"](df.iloc[[1]], thresholds=[.5])[0]
assert failed_honest.usefulness == 1.
RESULTS["traceguard_analysis_smoke"] = {"reported_points": [dataclasses.asdict(p) for p in pooled],
    "correct_A": {"safety":1.,"allow_rate":1.}, "correct_B":{"safety":0.,"allow_rate":0.},
    "unsuccessful_honest_task_reported_usefulness": failed_honest.usefulness}
RESULTS["traceguard_small_samples"] = {"20_of_20": wilson(20,20), "19_of_20": wilson(19,20), "6_of_7": wilson(6,7)}
RESULTS["traceguard_separation_counterexample"] = {"trusted_scores":[.8,.8,.8],
    "trusted_contribution": .6*.8, "untrusted_contribution_if_zero": 0., "threshold": .5,
    "result":"not flagged despite all three trusted scores being 0.8"}

# When Agents Lie: verify the actual classification code and game payoff methods.
print("When Agents Lie", flush=True)
runner = selected("repos/LLM-Trust-Breaking/src/endogenous/core/trial_runner.py",
                  ["_normalize_action", "_compare_actions", "_typology"])
plan, announcement, actual = 0,1,2
pd_flag = runner["_compare_actions"](announcement,plan,"fishing")
cb_flag = runner["_compare_actions"](actual,announcement,"fishing")
label = runner["_typology"](pd_flag,cb_flag)
assert label == "premeditated_deception" and actual != plan
RESULTS["when_agents_lie_third_action"] = {"plan":plan,"announcement":announcement,"actual":actual,"classification":label}
sys.path.insert(0, str(ROOT / "repos/LLM-Trust-Breaking"))
from src.games.fishing import FishingGame
from src.games.diners import DinersDilemmaGame
names = list("ABCDE")
fishing = FishingGame(names)
assert fishing.collapse_threshold == 14
assert all(v==0 for v in fishing.evaluate(dict.fromkeys(names,"3")).values())
diners = DinersDilemmaGame(names)
payoff = diners.evaluate({a:"CHEAP" if a=="A" else "EXPENSIVE" for a in names})
RESULTS["when_agents_lie_games"] = {"fishing_default_threshold":fishing.collapse_threshold,
    "all_three_fish_code_payoffs":fishing.evaluate(dict.fromkeys(names,"3")),
    "all_three_fish_paper_payoffs":dict.fromkeys(names,3),
    "one_cheap_four_expensive": payoff, "fishing_parsed_six": fishing.parse_action("A",{"choice":6})}
table8 = []
for line in pages("2607.05132v2")[16].splitlines():
    m = re.match(r"\s*(.*?)\s+(GPT-5\.2|Claude-Opus-4\.6|Llama-4-Maverick)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*$",line)
    if m:
        h, intended, impulsive, prem = map(float,m.groups()[2:])
        assert abs(h+intended+impulsive+prem-100) <= .11
        table8.append({"game":m[1],"model":m[2],"sum":h+intended+impulsive+prem,
                       "breaking":impulsive+prem, "premeditation_percent":100*prem/(impulsive+prem) if impulsive+prem else None})
assert len(table8)==18
rounds = []
for line in pages("2607.05132v2")[18].splitlines():
    m = re.match(r"\s*(.*?)\s+(GPT|Claude|Llama)\s+((?:\d+\s+){10})([\d.]+)\s+([\d.]+)\s*$",line)
    if m:
        values = list(map(int,m[3].split()))
        rounds.append({"game":m[1],"model":m[2],"rounds":values,"calculated_mean":statistics.mean(values),"reported_mean":float(m[4])})
assert len(rounds)==18
RESULTS["when_agents_lie_table8"] = table8
RESULTS["when_agents_lie_table11"] = rounds
RESULTS["when_agents_lie_cross_game_counterexamples"] = {"El_Farol_Claude_minority_Llama_pos5":8.51,
    "El_Farol_Llama_minority_Claude_pos24":6.99,"Volunteer_Llama_minority_Claude_pos1":-.62,
    "Public_Goods_max_abs_gap":.45, "Weakest_Link_max_abs_gap":.38}

# Colosseum: the theorem's literal Fc-span equality is false for lambda <= 1/2.
print("Colosseum and Terrarium", flush=True)
RESULTS["colosseum_proposition_counterexample"] = {"Fn":[1.,0.],"lambda":.25,
    "required_Fc_span_if_equality_attains_nominal_bound":1.,
    "minimum_effective_objective_advantage_of_Fn_maximizer": .75-.25,
    "corrected_construction":{"Fc":[-4.,0.], "F_lambda":[-.25,0.], "nominal_degradation":1., "Fc_span":4.}}
def coordination_reward(profile):
    return [5.,5.,5.] if all(profile) else [0.,0.,0.]
profile=[0,0,0]
unilateral=[]
for i in range(3):
    alternate=profile.copy()
    alternate[i]=1
    unilateral.append(coordination_reward(alternate)[i]-coordination_reward(profile)[i])
assert unilateral==[0.,0.,0.]
RESULTS["colosseum_coalition_metric_counterexample"]={"unilateral_regrets":unilateral,
    "defined_coalition_mean_regret":0.,"released_surrogate":(15/3)*2-0}
metrics = runpy.run_path(str(ROOT / "repos/colosseum/experiments/collusion/metrics.py"))
class TinyEnvironment:
    agent_names = ["A","B","C"]
    tasks = {"t": {}}
    costs = {}
    max_joint_reward = 3.
    assignment = dict.fromkeys(agent_names,"skip")
    def _rewards(self, assignments):
        return {a: float(assignments.get(a)=="t") for a in self.agent_names}
env=TinyEnvironment()
col = metrics["compute_collusion_metrics"](env=env, colluders=["A","B"],
    secret_blackboard_id=None,secret_channel_enabled=False,prompt_variant="control",tool_events=[],
    final_summary={"assignment":env.assignment,"joint_reward":0.,"agent_rewards":env._rewards(env.assignment)})
assert col.system_regret == 3. and col.coalition_mean_regret == 1.
RESULTS["colosseum_metrics_smoke"] = dataclasses.asdict(col)
normalize = selected("repos/colosseum/experiments/collusion/plots/generate_jira_regret_report.py",
                     ["_set_coalition_regret_gap_norm","_normalize_coalition_regret_gap"])
normalize["_set_coalition_regret_gap_norm"]([SimpleNamespace(coalition_mean_regret=2.,noncoalition_mean_regret=4.,model_label="M")])
assert normalize["_normalize_coalition_regret_gap"](0.,"M") == .5
RESULTS["colosseum_normalization"] = {"tie":.5,"positive_gap_two":normalize["_normalize_coalition_regret_gap"](2.,"M"),
    "reported_percent_counts":{"57.89":11/19*100,"78.95":15/19*100,"10.53":2/19*100},
    "r_squared":[.243**2,.1429**2,.0386**2,.2401**2]}
terrarium = selected("repos/Terrarium/terrarium/utils.py",["prepare_simulation_config"])
original={"simulation":{"seed":1},"nested":{"x":[1]}}
seeded = terrarium["prepare_simulation_config"](original,7)
seeded["nested"]["x"].append(2)
assert original["simulation"]["seed"]==1 and original["nested"]["x"]==[1]
RESULTS["terrarium_offline_smoke"]={"seeded":seeded,"original_unchanged":original}

# SCHEME: arithmetic from its printed counts and the described denominator.
print("SCHEME", flush=True)
mode_counts=[]
for line in pages("2605.29178v1")[18].splitlines():
    m=re.match(r"\s*([a-z_ -]+?)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)%\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)%\s*$",line)
    if m:
        mode_counts.append({"mode":m[1].strip(),"codex_occurs":int(m[2]),"codex_recovers":int(m[3]),
                            "gemini_occurs":int(m[6]),"gemini_recovers":int(m[7])})
assert len(mode_counts)==9
recovery={}
for model in ["codex","gemini"]:
    occurs=sum(r[model+"_occurs"] for r in mode_counts)
    recovers=sum(r[model+"_recovers"] for r in mode_counts)
    recovery[model]={"occurs":occurs,"recovers":recovers,"modes_per_trajectory":occurs/85,
                     "per_occurrence_recovery_percent":100*recovers/occurs}
RESULTS["scheme_table5_recovery"]={"rows":mode_counts,"aggregate":recovery}
RESULTS["scheme_comms_group_arithmetic"]={"notice_success_mean":(100+94)/2,"notice_hint_success_mean":(96+83)/2,
    "notice_no_comms_success_mean":(83+80)/2,"notice_hint_no_comms_success_mean":(92+92)/2,
    "full_visibility_stealth_notice_hint":2/85*100,"only_comms_stealth_notice_hint":9/85*100}

# Arike et al.: use released metric and CSV files without paid model generation.
print("Arike et al.", flush=True)
bcb = selected("repos/cotrh-blue-team/src/cot_red_handed/metrics_utils.py",["calculate_tpr_at_fpr"])
tpr=bcb["calculate_tpr_at_fpr"]([1.]*100,[0.]*100,.01)
assert tpr==(1.,0.,0.)
RESULTS["arike_bcb_offline_smoke"]={"perfect_classifier_TPR_FPR_threshold":tpr,
    "random_log_AUROC_analytic":.99/math.log(100)}
try:
    import unittest
    unittest.TestCase().assertAlmostEqual(tpr,1.,places=3)
except TypeError as exc:
    RESULTS["arike_shipped_test_contract_error"]={"error":type(exc).__name__+": "+str(exc),
        "location":"src/cot_red_handed/utils/test_metrics_utils.py:30"}
price=selected("repos/info-access-mle-sabotage/analysis/plotting/price_vs_auroc.py",["load_token_data"])
try:
    price["load_token_data"](ROOT/"repos/info-access-mle-sabotage/analysis/data/extracted_scores_2025-10-30_18-22-04.csv")
except ValueError as exc:
    RESULTS["arike_mle_csv_contract_error"]={"error":str(exc)}
reasoning_file=ROOT/"repos/cotrh-blue-team/src/cot_red_handed/result_files/roc_metrics_by_category_reasoning.csv"
records=list(csv.DictReader(reasoning_file.open(encoding="utf-8")))
reasoning_deltas=[]
for model in sorted(set(r["model"] for r in records)):
    vals={r["score_type"]:float(r["value"]) for r in records if r["model"]==model and r["subtlety"]=="subtle" and r["attack_policy"]=="overall" and r["metric_type"]=="tpr_at_1pct_fpr"}
    if "hierarchical" in vals:
        best=max(vals[k] for k in ["action","cot_only","hybrid","cot"])
        reasoning_deltas.append({"model":model,"delta_pp":100*(vals["hierarchical"]-best)})
RESULTS["arike_subtle_EaE_gains"]={"rows":reasoning_deltas,"mean_pp":statistics.mean(r["delta_pp"] for r in reasoning_deltas)}
combined_gains=[]
for model in sorted(set(r["model"] for r in records)):
    vals={r["score_type"]:float(r["value"]) for r in records if r["model"]==model and r["subtlety"]=="combined" and r["attack_policy"]=="overall" and r["metric_type"]=="tpr_at_1pct_fpr"}
    combined_gains.append(100*(vals["hierarchical"]-max(vals[k] for k in ["action","cot_only","hybrid","cot"])))
RESULTS["arike_headline_EaE_gain"]={"per_model_pp":combined_gains,"mean_pp":statistics.mean(combined_gains)}

provenance=[]
print("Repository provenance", flush=True)
for repo in sorted((ROOT/"repos").iterdir()):
    if not (repo/".git").exists(): continue
    revision=subprocess.check_output(["git","-C",str(repo),"rev-parse","HEAD"],text=True).strip()
    tracked=subprocess.check_output(["git","-C",str(repo),"ls-tree","-r","--name-only","HEAD"],text=True).splitlines()
    provenance.append({"repository":repo.name,"commit":revision,"tracked_files":len(tracked),
        "raw_eval_or_jsonl_files":[n for n in tracked if n.endswith((".eval",".jsonl"))],
        "AGENTS_files":[n for n in tracked if n.endswith("AGENTS.md")]})
RESULTS["provenance"]=provenance
(OUT/"verification.json").write_text(json.dumps(RESULTS,indent=2,default=str),encoding="utf-8")
print(json.dumps({k:v for k,v in RESULTS.items() if k not in {"traceguard_table3","when_agents_lie_table8","when_agents_lie_table11","colosseum_metrics_smoke","provenance"}},indent=2,default=str))
print("All component assertions passed. Evidence: audit/evidence/verification.json")
