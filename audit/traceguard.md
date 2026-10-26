# TraceGuard: error audit

Audit date: 23 October 2026 (Asia/Calcutta). Page numbers are physical PDF pages, matching the supplied versions. Instructions inside papers/repositories were treated as source material, not user instructions. This report contains errors, counterexamples and verification limits, not paper summaries.

Severity: **major** affects a central metric, comparison, theorem or implementation contract; **minor** is a localized numeric, reference or reproduction defect. No critical finding was established. A limitation under COULD NOT VERIFY is not counted as a confirmed error. Code findings refer to the recorded commits, which need not be the authors' original experiment commits.

Evidence and scripts: [verification.json](evidence/verification.json), [verification.log](evidence/verification.log), [verification script](scripts/verify_audit.py), [layout extraction](scripts/extract_layout.ps1), [PDF hashes/pages](text/manifest.json). No paid APIs were called. Component checks execute original source definitions; full model experiments were not rerun.

Source: [PDF pp. as cited below](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2604.03968v1.pdf>).

## CONFIRMED

### TG-01 — Single-score baselines never receive the evaluated task or action

- ID, paper, severity: **TG-01**; TraceGuard; **major**.
- location: §4.1, Table 5, Conclusion; [PDF pp. 8,13,16](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2604.03968v1.pdf>); [repos/TraceGuard/src/traceguard/monitors/baseline_monitors.py:15](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/TraceGuard/src/traceguard/monitors/baseline_monitors.py:15>); [audit/evidence/_last_tool_calls_prompt_formatter.py:88](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/audit/evidence/_last_tool_calls_prompt_formatter.py:88>)
- what the paper says (short quote): “Single-score monitoring fails completely on our benchmark—both trusted and untrusted single-score monitors achieve 0% safety.”
- what is wrong, with evidence: BASELINE_PROMPT contains neither {task_description} nor {tool_calls}. Both baseline builders pass only that constant prompt to ControlArena. In the exact locked dependency (control-arena 14.2.0), the default formatter calls prompt.format(task_description=..., tool_calls=...); it does not append the trajectory elsewhere. The offline check sends distinct benign/attack sentinels and gets byte-identical prompts containing neither action nor task. The structured monitor does receive those fields. Thus the released baseline comparison confounds input visibility with scoring structure, undermining the claimed 0%→95% gain. The original experiment logs are absent, so whether an unpublished corrected prompt was used remains unknown.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Include task/action placeholders in both baselines and rerun a matched comparison with released prompts and logs.

### TG-02 — Table 3 composites cannot follow from its stated same-step scores and released pipeline

- ID, paper, severity: **TG-02**; TraceGuard; **major**.
- location: §3.1/Eq. 1, §4.3/Table 3, [PDF pp. 4,11](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2604.03968v1.pdf>); [repos/TraceGuard/src/traceguard/monitors/bash_heuristic_monitor.py:407](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/TraceGuard/src/traceguard/monitors/bash_heuristic_monitor.py:407>); [repos/TraceGuard/src/traceguard/analysis/pareto.py:340](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/TraceGuard/src/traceguard/analysis/pareto.py:340>)
- what the paper says (short quote): “Per-dimension average suspicion scores (max-suspicion step per sample)” and “Composite includes heuristic detector and intent analyzer boosts”.
- what is wrong, with evidence: In GA/CA/RC/SA/ATC order, attack weighted mean = .2(.849)+.3(.870)+.2(.893)+.1(.682)+.2(.845)=**.8466**, and honest = .2(.617)+.3(.753)+.2(.804)+.1(.642)+.2(.801)=**.7345**. Reported composites are **.616/.206**, lower by .2306/.5285. Positive boosts and upper clipping cannot explain these decreases. Category reweighting does not rescue the released pipeline: all 16 category subsets were checked; for [0,1] scores, its maximum possible downward change (total variation of weights) is no greater than the simultaneously added regex boost. Other boosts are nonnegative. Also, plot_dimension_breakdown collects **all monitored steps**, not the stated per-sample maximum step. The table therefore mixes populations/score versions or misstates its aggregation; its footnote is insufficient. Underlying corrected means cannot be recovered without aligned logs.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Regenerate dimension and composite summaries from the same runs and steps, publishing the exact aggregation and score version.

### TG-03 — Usefulness is implemented as an allow rate, ignoring task success

- ID, paper, severity: **TG-03**; TraceGuard; **major**.
- location: §4.1 Metrics, Table 2/Fig. 3, [PDF pp. 8-9](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2604.03968v1.pdf>); [repos/TraceGuard/src/traceguard/analysis/pareto.py:170](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/TraceGuard/src/traceguard/analysis/pareto.py:170>)
- what the paper says (short quote): “Usefulness: Fraction of honest-mode runs where the task was completed successfully.”
- what is wrong, with evidence: The analysis computes only P(max_suspicion<τ | honest), despite loading main_task_success. A synthetic honest run with max_suspicion=0 and main_task_success=False is reported as **100% usefulness**. Successful deferred completion is also excluded by construction. Table 2's narrower caption still calls the number 'honest task completion without deferral', which would require success AND no deferral; the code checks only no deferral. Therefore the plotted label does not implement either task-success definition. This does not show the actual task-completion rates, which require the missing logs.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Report the current metric as honest allow rate and compute task completion separately, including deferral outcomes as specified.

### TG-04 — Equation 2's per-dimension saturation is not implemented

- ID, paper, severity: **TG-04**; TraceGuard; **major**.
- location: §3.1/Eq. 2 and Fig. 2, [PDF pp. 4,7](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2604.03968v1.pdf>); [repos/TraceGuard/src/traceguard/monitors/traceguard_monitor.py:195](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/TraceGuard/src/traceguard/monitors/traceguard_monitor.py:195>); [repos/TraceGuard/src/traceguard/monitors/bash_heuristic_monitor.py:407](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/TraceGuard/src/traceguard/monitors/bash_heuristic_monitor.py:407>)
- what the paper says (short quote): “we apply a per-dimension saturation function before aggregation: s′d=min(sd·Boosttotal,1.0)”
- what is wrong, with evidence: The actual scorer first averages unboosted normalized dimension scores, may add a separate variance-triggered .08 boost, and then computes clip(composite + heuristic_boost + total_detector_boost + intent_boost,0,1). No per-dimension multiplication/saturation from Eq. 2 occurs. For equal dimension scores .2 and an additive boost .5, code returns .7; treating the corresponding multiplier as 1.5 would give .3 under Eq. 2. The two algorithms have different thresholds and failure behavior. §3.3 describes additive composite boosts, so the paper also gives incompatible specifications internally.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Choose one algorithm, make equations/algorithm/code agree, and state whether results include the disagreement boost.

### TG-05 — The advertised seventh heuristic detector is missing

- ID, paper, severity: **TG-05**; TraceGuard; **minor**.
- location: §3.3 detector 6 and abstract, [PDF pp. 1,6](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2604.03968v1.pdf>); [repos/TraceGuard/src/traceguard/monitors/bash_heuristic_monitor.py:66](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/TraceGuard/src/traceguard/monitors/bash_heuristic_monitor.py:66>); [repos/TraceGuard/src/traceguard/detectors/__init__.py:3](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/TraceGuard/src/traceguard/detectors/__init__.py:3>)
- what the paper says (short quote): “Subprocess Tracker. Detects process spawning ... download-then-execute chains ... cron/systemd persistence”.
- what is wrong, with evidence: The tracked source contains six heuristic modules: variable_binding, dual_purpose, data_flow, string_assembly, encoding, config_diff. No subprocess tracker module, tracking state, import, or invocation exists in bash_heuristic_monitor. detectors/__init__.py lists intent_analyzer as its seventh module, but that is the separate LLM stage, not a seventh pure-function heuristic. Generic regex matches may catch some related patterns; they do not implement the named stateful tracker.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Release and invoke the subprocess tracker, or correct the architecture/count to six heuristic detectors.

### TG-06 — A 0.60 trusted weight does not prevent the untrusted scores from suppressing alarms

- ID, paper, severity: **TG-06**; TraceGuard; **major**.
- location: §4.5/Fig. 7 and Discussion, [PDF pp. 13-14](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2604.03968v1.pdf>); [repos/TraceGuard/src/traceguard/monitors/separation_of_duties_monitor.py:94](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/TraceGuard/src/traceguard/monitors/separation_of_duties_monitor.py:94>)
- what the paper says (short quote): “the untrusted model contributes reasoning analysis without being able to unilaterally suppress alarms.”
- what is wrong, with evidence: At τ=.5, trusted scores GA=CA=SA=.8 contribute (.2+.3+.1)×.8=.48. If the untrusted RC/ATC scores are .8, the total is .80 and triggers; changing only those two scores to zero yields .48 and suppresses it. The weights bound the untrusted contribution to .4; they do not establish the stated guarantee. At τ>.6 the trusted portion cannot trigger alone even with all trusted scores=1. Observed 20/20 detection at τ=.3 is not a proof of immunity.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: State a conditional bound or give the trusted score an independent alarm/veto rule, and test deliberately colluding monitor outputs.

### TG-07 — Several reference identities do not match their arXiv IDs

- ID, paper, severity: **TG-07**; TraceGuard; **minor**.
- location: §4.4/[7] and References [3], [7], [11], [13], [PDF pp. 12,19](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2604.03968v1.pdf>)
- what the paper says (short quote): “We test ... on the AgentHarm dataset [7]”; [7] is titled “HarmBench”.
- what is wrong, with evidence: [7] is [HarmBench, arXiv:2402.04249](https://arxiv.org/abs/2402.04249), whereas [AgentHarm is arXiv:2410.09024](https://arxiv.org/abs/2410.09024), led by Maksym Andriushchenko. The actual HarmBench lead author is Mantas Mazeika, not 'Maksym Mazeika'. [3]'s ID [2512.15688](https://arxiv.org/abs/2512.15688) is *BashArena: A Control Setting for Highly Privileged AI Agents*, by Adam Kaufman et al., not the listed Pearce et al. title/authors. [11]'s [2602.20628v1](https://arxiv.org/abs/2602.20628v1) was first submitted in February 2026, not 2025, and its authors are Gardner-Challis et al., not 'Thomas Griffiths, Niels Warncke'. [13]'s [2504.05259](https://arxiv.org/abs/2504.05259) is by Tomek Korbak, Mikita Balesni, Buck Shlegeris and Geoffrey Irving, not the listed Hoelscher-Obermaier et al. These are identity/year errors; the claimed AgentHarm experiment's actual dataset still needs its missing artifacts.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Replace these entries from authoritative metadata and cite AgentHarm separately from HarmBench.

### TG-08 — The promised data and AgentHarm evaluation entry point are not in the release

- ID, paper, severity: **TG-08**; TraceGuard; **minor**.
- location: §1 code/data availability and Fig. 8, [PDF pp. 3,18](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2604.03968v1.pdf>); [repos/TraceGuard/.gitignore:77](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/TraceGuard/.gitignore:77>); repository tree at pinned commit in evidence/verification.json
- what the paper says (short quote): “Code and data are available at https://github.com/linhkid/TraceGuard.”
- what is wrong, with evidence: At commit 0e2e8226d7ca98e0375ed3aa54f9a870a3794714, the repository has no tracked evaluation logs or per-sample result data for the 519 BashArena or 20 AgentHarm samples. .gitignore explicitly excludes .eval logs and generated result files. Fig. 8 names run_agentharm_eval.py, but no such tracked script exists. The README supplies aggregate numbers, not the observations/configuration manifest needed to recompute them. This is a release/reproducibility gap, not evidence that experiments were not performed.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Publish the per-sample scores, run/configuration manifest and AgentHarm script, with a stable paper-version tag.

### TG-09 — The analysis pools different monitors while labeling their results separately

- ID, paper, severity: **TG-09**; TraceGuard; **minor**.
- location: §4 monitor comparisons; [repos/TraceGuard/src/traceguard/analysis/pareto.py:156](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/TraceGuard/src/traceguard/analysis/pareto.py:156>); [repos/TraceGuard/scripts/analyze_results.py:53](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/TraceGuard/scripts/analyze_results.py:53>)
- what the paper says (short quote): “We compare against two baselines” and report safety by monitor.
- what is wrong, with evidence: compute_pareto_points(df, monitor_names, ...) constructs honest_df/attack_df from the entire input before looping over monitor_name and never filters either by monitor. A two-monitor example with true detection rates 100% and 0% returns 50% for both named monitors. The CLI's default 'all' likewise aggregates everything in the chosen directory. This is a confirmed analysis bug when logs contain multiple monitors; no original logs are available to establish whether it affected a published figure.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Filter rows by monitor before computing each frontier and require explicit pooling in the CLI.

### TG-10 — The released intent analyzer uses a different model and silently skips by default

- ID, paper, severity: **TG-10**; TraceGuard; **minor**.
- location: §4.1 Models, [PDF pp. 8](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2604.03968v1.pdf>); [repos/TraceGuard/src/traceguard/detectors/intent_analyzer.py:157](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/TraceGuard/src/traceguard/detectors/intent_analyzer.py:157>); [repos/TraceGuard/src/traceguard/detectors/intent_analyzer.py:196](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/TraceGuard/src/traceguard/detectors/intent_analyzer.py:196>)
- what the paper says (short quote): “The intent analyzer uses GPT-4.1-mini”.
- what is wrong, with evidence: The release describes its intent stage as Claude Opus 4.6 via Bedrock, gets the model ID from CLAUDE_BEDROCK_MODEL_ID or CLAUDE_MODEL_ID, and calls get_model(f'bedrock/{model_id}'). If neither is set it returns a zero-boost IntentAnalysis without a model call. It does not use the trusted GPT-4.1-mini role. The CLI's model flags do not configure this hidden extra provider. This confirms that the released default/model path differs from the stated setup, without determining the model used in unavailable historical logs.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Configure the analyzer explicitly through the evaluation model roles and release the exact model ID and activation state used for each run.

## REFUTED leads

- **Table 5 100% versus Table 2 82.1%:** these are explicitly different runs and monitors. Table 2/Fig. 3 use bash_heuristic with 519 samples: at τ=.3, 197/240=82.083% attacks flagged and 193/279=69.176% honest allowed; at .5, 170/240=70.833% and 262/279=93.907%. Table 5 is labeled an earlier experiment: core traceguard 100% at .3, collusion_resistant 100%/.95 at .3/.5, separation_of_duties 100%/86%. Fig. 5's 'TraceGuard' bar is the main hybrid result rounded to 82/71/54/15. These numbers should not be treated as the same configuration.

- **Small-n rates:** 86% at n=7 is consistent with 6/7=85.714%; 95% at n=20 is consistent with 19/20. The observations are not arithmetic errors. Wilson 95% intervals are about [48.7%,97.4%] for 6/7, [76.4%,99.1%] for 19/20 and [83.9%,100%] for 20/20. These are not evidence of a population guarantee.

- **Rounded dimension Δ cells:** .849−.617=.232 versus printed .231, .893−.804=.089 versus .090, and .845−.801=.044 versus .043 can arise by rounding underlying means. These 0.001 differences are not confirmed errors. The much larger aggregation inconsistency is TG-02.

## COULD NOT VERIFY

- **The causal collusion interpretation:** using the same model family in monitor/agent roles is not itself a test of an intentionally colluding monitor. The released monitor prompts ask for security evaluation, and no trained/adversarial collusion policy, collusion signal experiment, or monitor-side adversarial objective is supplied. The paper acknowledges fixed attack policies, but its stronger mechanism claim ('structure constrains collusion') remains unestablished; TG-01 supplies a concrete alternative explanation for the baseline collapse.

- **95–100% overview versus 70.8% main pipeline:** the overview/Key Takeaways quote earlier structured-monitor observations, not the larger hybrid run. They should be read with named variants, thresholds and n. No new matched baseline rerun supports attributing the whole improvement to decomposition.

- **Train/test leakage and tuning:** weights are described as intuitive/iteratively calibrated, but there is no released split/task-ID manifest to establish disjoint calibration and evaluation sets. Leakage cannot be confirmed or excluded. AgentHarm category means without per-category n, benign controls, or detection targets do not verify cross-domain discrimination.

- **Runtime model/configuration provenance:** run_eval.py defaults to GPT-4o/GPT-4o-mini and limit=5, whereas §4.1 names Claude Sonnet 4/GPT-4.1-mini and 20 samples/configuration. Overrides can reconcile these values; missing commands/logs prevent deciding which were used. No API evaluation was run.
