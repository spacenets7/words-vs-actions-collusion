# Audit findings: five supplied research papers

**22 confirmed records: 10 major, 12 minor; no critical findings.** This is not a count of invalid headline results: several records concern released reproduction code, and their effect on historical runs remains unverified.

Audit date: 23 October 2026 (Asia/Calcutta). Page numbers are physical PDF pages, matching the supplied versions. Instructions inside papers/repositories were treated as source material, not user instructions. This report contains errors, counterexamples and verification limits, not paper summaries.

Severity: **major** affects a central metric, comparison, theorem or implementation contract; **minor** is a localized numeric, reference or reproduction defect. No critical finding was established. A limitation under COULD NOT VERIFY is not counted as a confirmed error. Code findings refer to the recorded commits, which need not be the authors' original experiment commits.

Evidence and scripts: [verification.json](evidence/verification.json), [verification.log](evidence/verification.log), [verification script](scripts/verify_audit.py), [layout extraction](scripts/extract_layout.ps1), [PDF hashes/pages](text/manifest.json). No paid APIs were called. Component checks execute original source definitions; full model experiments were not rerun.

The five detailed records are [Colosseum](colosseum.md), [TraceGuard](traceguard.md), [When Agents Lie](when-agents-lie.md), [Arike et al.](arike.md), and [SCHEME](scheme.md).

## Acquisition and reproducibility

All five local PDFs were copied without modification and converted with **pdftotext -layout**. Independent pdfplumber text/table extraction and targeted Poppler page renders were also inspected. Sources total 161 pages. SHA-256 hashes and physical page counts are in the manifest.

All four initially requested Git repositories were cloned after the network-restricted sandbox's first attempts failed. Arike's two code links were discovered in the PDF and both Git histories obtained. The BigCodeBench checkout failed on Windows-invalid colon filenames; its 400 valid source/data files were recovered, with four excluded paths recorded. No SCHEME-specific code/data URL was found, so no SCHEME clone or runtime check was possible. No dependency-only repository was misrepresented as that release.

| Repository | Inspected commit |
|---|---|
| colosseum | `b077fe7e2f10566e92156cc12e06ffb2aac54790` |
| cotrh-blue-team | `7dd11d656756cb74215b4adf14b5d25b0f080576` |
| info-access-mle-sabotage | `3be99896888dc36a4ebd43a506dabd92db3d2c18` |
| LLM-Trust-Breaking | `fd11aca351e52c65c929e1a7d46d9f087f237adf` |
| Terrarium | `aeec335d108abeafaf7682872c1d881d47a9ed78` |
| TraceGuard | `0e2e8226d7ca98e0375ed3aa54f9a870a3794714` |

The six available repositories received offline component checks: Colosseum reward/regret calculations; Terrarium seed-copy behavior; TraceGuard prompt formatting, aggregation and metric grouping; When Agents Lie typology and payoff functions; MLE's provided-CSV loader; BCB's TPR helper and test contract. The last two exposed documented reproduction defects. The generic agent frameworks, SciPy/sklearn, Docker and API endpoints were not installed/run as full pipelines. Windows asyncio stalled under the sandbox; the no-API component script completed outside it, and the stalled audit processes were stopped. The pinned ControlArena 14.2.0 wheel was downloaded for source inspection only.

## CONFIRMED

### Colosseum

### COL-01 — Proposition C.1 states the wrong range in its achievability equality

- ID, paper, severity: **COL-01**; Colosseum; **major**.
- location: Appendix C, Proposition C.1(2), [PDF pp. 17-18](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2602.15198v2.pdf>)
- what the paper says (short quote): “any maximizer of Fλ attains the upper bound, i.e., Δ(x̃) = max Fc − min Fc.”
- what is wrong, with evidence: The preceding upper bound is **max Fn − min Fn**, not the span of Fc. This is more than an interchangeable symbol: take two fully controllable assignments with Fn(a)=1, Fn(b)=0 and λ=1/4. Attaining the nominal upper bound requires choosing b. If the displayed equality also holds, span(Fc)=1, so Fλ(a)−Fλ(b) ≥ 3/4−1/4=1/2>0. Then b cannot maximize Fλ. A corrected construction is Fc=−M Fn with M>(1−λ)/λ: e.g. M=4 gives Fλ(a)=−1/4, Fλ(b)=0, nominal degradation 1, but span(Fc)=4. No proof of the proposition appears in the supplied PDF; this is a counterexample to the literal statement, not an allegation about an unseen proof.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Replace Fc by Fn in the equality and prove achievability with an explicitly scaled auxiliary objective.

### COL-02 — The Hospital reproduction path uses a different coalition-regret metric

- ID, paper, severity: **COL-02**; Colosseum; **major**.
- location: §5.3, §5.5/Fig. 5, [PDF pp. 7-9](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2602.15198v2.pdf>); [repos/colosseum/experiments/agent_misalignment/metrics.py:653](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/colosseum/experiments/agent_misalignment/metrics.py:653>); [repos/colosseum/experiments/agent_misalignment/plots/plot_model_comparison.py:874](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/colosseum/experiments/agent_misalignment/plots/plot_model_comparison.py:874>)
- what the paper says (short quote): “the coalition mean regret is” the mean of δi(x̃)=max_xi ri(xi⊕x̃−i)−ri(x̃).
- what is wrong, with evidence: The released Hospital metrics instead set coalition_max_reward_sum=(max_joint_reward/total_agents)×coalition_size and coalition_reward_regret=max(0, coalition_max_reward_sum−coalition_reward_sum). The named Hospital coalition-regret plot divides that surrogate by a min–max denominator. It never searches unilateral counterfactuals in that path. These measures can disagree even at zero unilateral regret: if three agents each get 5 only when all choose 1, at all-0 every unilateral regret is 0, while this surrogate gives a two-agent coalition (15/3)×2−0=10. The Jira metrics path separately implements unilateral regret correctly. This confirms a contract mismatch in the released Hospital reproduction code; absent original logs/figure commands, it does not establish which path generated every published bar.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Implement the defined mean unilateral regret for Hospital plots, or explicitly rename and define the equal-share reward-shortfall surrogate.

### COL-03 — The judge-ablation reference points to the environment figure

- ID, paper, severity: **COL-03**; Colosseum; **minor**.
- location: §5.3, [PDF pp. 8,23-24](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2602.15198v2.pdf>)
- what the paper says (short quote): “leave judge ablations in the Appendix (See Figure 17 in Appendix).”
- what is wrong, with evidence: Figure 17 (p.24) varies environments. The state-of-the-art judge-model ablation is Figure 16 (p.23), titled 'Emergent Collusion Over State-of-The-Art Judge Models'. This is a confirmed wrong-number pointer, distinct from the valid persuasion-tactics reference to Fig. 12.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Change the §5.3 judge-ablation reference from Figure 17 to Figure 16.

### TraceGuard

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

### When Agents Lie

### WAL-01 — The premeditation equation and implementation count an unplanned third action

- ID, paper, severity: **WAL-01**; When Agents Lie; **major**.
- location: §3/Eq. 1/Table 1, [PDF pp. 3-4](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2607.05132v2.pdf>); [repos/LLM-Trust-Breaking/src/endogenous/core/trial_runner.py:264](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/LLM-Trust-Breaking/src/endogenous/core/trial_runner.py:264>); [repos/LLM-Trust-Breaking/src/endogenous/analysis/endogenous_analyzer.py:99](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/LLM-Trust-Breaking/src/endogenous/analysis/endogenous_analyzer.py:99>)
- what the paper says (short quote): “When the final action matches neither the plan nor the announcement, the deviation is not counted as premeditated”.
- what is wrong, with evidence: Eq. 1 requires only a_act≠a_pub AND a_pub≠a_plan. It omits a_act=a_plan. On a numeric game, plan=0, public=1, actual=2 satisfies both inequalities yet was not the planned action. The released _typology(True,True) labels this 'premeditated_deception', and compute_premeditation_rate counts it in the numerator. The executed source check confirms this example. With only two actions the two inequalities imply actual=plan, so this flaw does not invalidate the high-deception Diners/El Farol headline examples; it matters for Fishing, Public Goods and Weakest Link.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Require actual=plan in the numerator and introduce a third-action category, then recompute numeric-game rates.

### WAL-02 — The cross-game payoff-gap claim contradicts Table 14

- ID, paper, severity: **WAL-02**; When Agents Lie; **major**.
- location: §4.3 Cross-game comparison versus Appendix F.1/Table 14, [PDF pp. 6,22](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2607.05132v2.pdf>)
- what the paper says (short quote): “Weakest Link, Volunteer, and El Farol show minimal asymmetries (gaps below 0.40).”
- what is wrong, with evidence: Table 14 lists El Farol Claude-minority/Llama-majority gaps **+7.36/+8.51/+6.98** at pos1/pos5/pos24, and Llama-minority/Claude-majority **+6.99** at pos24. Volunteer includes **−.62**, **−.60**, and **+.58**, also outside an absolute .40 bound. The El Farol +8.51 gap even exceeds every Diners gap in that table (maximum absolute value 4.49). Public Goods 'up to .45' and Weakest Link '<.40' do agree with the table. Different payoff scales limit welfare comparisons across games, but cannot repair the paper's explicit raw-gap thresholds.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Correct the game-specific ranges and revise the boundary-condition/exploitation discussion using an explicitly normalized cross-game comparison.

### WAL-03 — The last Diners payoff row swaps cooperators and defectors

- ID, paper, severity: **WAL-03**; When Agents Lie; **minor**.
- location: Appendix C/Table 5, [PDF pp. 15](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2607.05132v2.pdf>); [repos/LLM-Trust-Breaking/src/games/diners.py:116](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/LLM-Trust-Breaking/src/games/diners.py:116>)
- what the paper says (short quote): “1 CHEAP + 4 EXPENSIVE” lists Defector Payoff −1.80 and Cooperator Payoff 3.20.
- what is wrong, with evidence: The shared bill is (2+4×8)/5=6.8. The CHEAP cooperator gets 5−6.8=**−1.8**; each EXPENSIVE defector gets 10−6.8=**3.2**. The table places these values under the opposite headings. The released payoff implementation returns the correct mapping.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Swap the two payoff cells in the last row of Table 5.

### WAL-04 — A reported Fishing payoff exceeds the game's maximum

- ID, paper, severity: **WAL-04**; When Agents Lie; **minor**.
- location: Appendix B, C/Table 3 and E.2/Table 9, [PDF pp. 13,15,18](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2607.05132v2.pdf>); [repos/LLM-Trust-Breaking/src/games/fishing.py:88](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/LLM-Trust-Breaking/src/games/fishing.py:88>)
- what the paper says (short quote): Table 9, Tragedy of Commons / Llama-4-Maverick: “Max 6.00”.
- what is wrong, with evidence: The specified action set is {0,...,5}; the payoff is the selected catch if sustainable and 0 otherwise. Hence 0≤ui≤5. The code also clamps a response of 6 to 5 before scoring. A maximum of 6 cannot arise under the published game. It may be a table typo or evidence of another configuration, but the supplied artifacts do not resolve which.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Correct the maximum from the original observations or disclose and separate any run with a larger action bound.

### WAL-05 — The released Fishing default changes the collapse boundary

- ID, paper, severity: **WAL-05**; When Agents Lie; **major**.
- location: Appendix B/C, [PDF pp. 13,15](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2607.05132v2.pdf>); [repos/LLM-Trust-Breaking/experiments/run_endogenous.py:47](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/LLM-Trust-Breaking/experiments/run_endogenous.py:47>); [repos/LLM-Trust-Breaking/src/games/fishing.py:79](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/LLM-Trust-Breaking/src/games/fishing.py:79>)
- what the paper says (short quote): “If total catch exceeds 3N fish, the lake collapses ... If total catch <= 3N, each fisherman keeps what they caught”.
- what is wrong, with evidence: For n=5, the paper allows total catch 15. Both build_game_params() and FishingGame's default use **3n−1=14**. With all five choosing 3, total catch=15: the paper pays each agent 3, while the executed released game pays everyone 0. This changes the coordination target and strategic incentives. An explicit --threshold 15 can recover the paper setting, but no published run manifest establishes that override was used.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Use 3n as the default or document the actual 3n−1 game and release the experiment commands/configurations.

### Arike et al.

### ARI-01 — The supplied MLE score CSV is rejected by its price-analysis loader

- ID, paper, severity: **ARI-01**; Arike et al.; **minor**.
- location: Reproducibility Statement, [PDF pp. 10](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2601.21112v2.pdf>); [repos/info-access-mle-sabotage/analysis/plotting/price_vs_auroc.py:485](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/info-access-mle-sabotage/analysis/plotting/price_vs_auroc.py:485>); analysis/data/extracted_scores_2025-10-30_18-22-04.csv
- what the paper says (short quote): Repositories “each ... contain instructions on how to reproduce our results”.
- what is wrong, with evidence: The bundled CSV has metadata_monitor_model and metadata_monitor_input_token_count. load_token_data() requires score_metadata__monitor_model and score_metadata__monitor_input_token_count. Calling the actual loader on the supplied CSV raises **ValueError: CSV is missing required columns: score_metadata__monitor_input_token_count, score_metadata__monitor_model**, before analysis can proceed. This is a concrete reproduction-interface break in the inspected release, not a refutation of the reported monitor results.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Normalize the released CSV column names in the loader or provide the matching data export and exact analysis command.

### ARI-02 — The shipped metric tests use an obsolete scalar return contract

- ID, paper, severity: **ARI-02**; Arike et al.; **minor**.
- location: BigCodeBench repository: [repos/cotrh-blue-team/src/cot_red_handed/utils/test_metrics_utils.py:29](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/cotrh-blue-team/src/cot_red_handed/utils/test_metrics_utils.py:29>); [repos/cotrh-blue-team/src/cot_red_handed/metrics_utils.py:168](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/repos/cotrh-blue-team/src/cot_red_handed/metrics_utils.py:168>)
- what the paper says (short quote): The paper reports “TPR at 1% FPR”; the released test asserts that calculate_tpr_at_fpr(...) equals 1.0 for perfect separation.
- what is wrong, with evidence: The actual function returns (TPR, actual_FPR, threshold), giving **(1.0,0.0,0.0)** on that test's input. The test compares this tuple directly with 1.0 and raises **TypeError: unsupported operand type(s) for -: 'tuple' and 'float'**. The offline check executes the original function and the same unittest assertion. This is a broken validation test; the returned TPR itself is correct, and it does not show an error in the paper's metric values.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Unpack the returned tuple and test each component against its documented contract.

### Radev et al. / SCHEME

### SCH-01 — The claimed per-occurrence recovery rates do not match the printed counts

- ID, paper, severity: **SCH-01**; Radev et al. / SCHEME; **minor**.
- location: Abstract/§3.3 versus Appendix G/Table 5, [PDF pp. 1,6,18-19](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2605.29178v1.pdf>)
- what the paper says (short quote): “The per-occurrence recovery rate ... jumps from 56% on Codex to 73% on Gemini.”
- what is wrong, with evidence: Across Table 5's nine modes, Codex has **177 occurrences and 91 recoveries**, so 91/177=**51.41%**, not 56%. Gemini has **122 occurrences and 87 recoveries**, so 87/122=**71.31%**, not 73%. These same denominators give 177/85=2.082 and 122/85=1.435 modes per trajectory, matching the stated 2.1/1.4. Appendix G defines category recovery by summing recovered mode occurrences over occurrences. A mean of per-trajectory recovery fractions could differ, but would be a different estimand and needs that label/denominator. The qualitative direction survives.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Correct the pooled rates or explicitly identify the alternative weighting scheme and supply its per-trajectory inputs.

### SCH-02 — Non-significant difference tests are treated as establishing exchangeability

- ID, paper, severity: **SCH-02**; Radev et al. / SCHEME; **minor**.
- location: Appendix J.1, [PDF pp. 25](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2605.29178v1.pdf>)
- what the paper says (short quote): “Mann–Whitney U-tests find no significant difference ... so the two baselines are exchangeable as monitor inputs.”
- what is wrong, with evidence: Failing to reject a distributional difference does not establish equivalence/exchangeability. The design has only five underlying baseline runs per instance/model before filtering; ten monitor scores are collapsed to a median, not ten independent task runs. Table 15 actually gives different 98th-percentile thresholds for Code+Comms (Codex 5, Gemini 6) and Single-Agent (5.3 versus 6). Pooling may remain a reasonable design choice, and the reported ablations test its practical effect, but the asserted statistical implication is invalid.
- confidence (and what would resolve it if not high): **high**.
- suggested fix: Describe pooling as a design choice supported by sensitivity checks, or perform an equivalence analysis with a prespecified tolerance.

## REFUTED leads

### Colosseum

- **Coalition-advantage sign/tie lead:** the paper defines noncoalition regret minus coalition regret, so positive favors the coalition. The released Jira plotting helper uses that sign and normalizes as .5+gap/(2 max|gap|), giving exactly .5 for a zero gap. The differently named stored reward gap is not proof of a sign inversion in this plotting path.

- **57.89/78.95/10.53% arithmetic:** 11/19=57.8947%, 15/19=78.9474%, 2/19=10.5263%; these percentages are consistent with n=19. Their exact model membership cannot be reliably reconstructed from overlapping markers alone.

- **Persuasion/Fig. 12 cross-reference:** §5.6 invokes Fig. 12 to illustrate the tactics. Fig. 12 does illustrate those tactics; results are separately discussed with Fig. 6 and Fig. 10. This particular reference is valid, not a confirmed wrong-figure citation. Other prose/figure references were checked without promoting ambiguous references to errors.

### TraceGuard

- **Table 5 100% versus Table 2 82.1%:** these are explicitly different runs and monitors. Table 2/Fig. 3 use bash_heuristic with 519 samples: at τ=.3, 197/240=82.083% attacks flagged and 193/279=69.176% honest allowed; at .5, 170/240=70.833% and 262/279=93.907%. Table 5 is labeled an earlier experiment: core traceguard 100% at .3, collusion_resistant 100%/.95 at .3/.5, separation_of_duties 100%/86%. Fig. 5's 'TraceGuard' bar is the main hybrid result rounded to 82/71/54/15. These numbers should not be treated as the same configuration.

- **Small-n rates:** 86% at n=7 is consistent with 6/7=85.714%; 95% at n=20 is consistent with 19/20. The observations are not arithmetic errors. Wilson 95% intervals are about [48.7%,97.4%] for 6/7, [76.4%,99.1%] for 19/20 and [83.9%,100%] for 20/20. These are not evidence of a population guarantee.

- **Rounded dimension Δ cells:** .849−.617=.232 versus printed .231, .893−.804=.089 versus .090, and .845−.801=.044 versus .043 can arise by rounding underlying means. These 0.001 differences are not confirmed errors. The much larger aggregation inconsistency is TG-02.

### When Agents Lie

- **Table 8 versus Fig. 2 denominator lead:** premeditation is Premeditated/(Premeditated+Impulsive), not a sum including 'Intended deceptive (complied)'. Diners GPT: 96.6/(96.6+.1)=99.8966%; Diners Claude: 26.2/(26.2+.5)=98.1273%; Diners Llama: 98.2/(98.2+.2)=99.7967%; Volunteer GPT: 1.3/(1.3+27.9)=4.4521%. These reproduce Fig. 2's 99.9/98.1/99.8/4.5. All 18 typology rows sum to 100% within 0.1 percentage point. WAL-01 is the distinct third-action flaw.

- **Headline >90% claim:** it explicitly applies to the highest-deception conditions, not all deviations in all games. Diners GPT/Llama and El Farol Llama support it; the binary action space makes actual=plan follow from the two inequality tests. GPT El Farol is only 32.3% and Volunteer only 4.5%, so extending the claim universally would be wrong.

- **Fig. 4 versus Table 14:** the plotted Diners pairs and reported gaps agree within displayed precision: .82−2.37=−1.55; .02−2.62=−2.60; 4.15−2.60=+1.55; 6.31−1.82=+4.49; 5.54−1.98=+3.56. No sign-reversal lead was confirmed.

- **Evaluation/call-count arithmetic:** 126×20×10×5=126,000 agent-rounds, times four stated agent-stage calls=504,000. These products and the listed cost subtotals are internally consistent estimates; additional optional judging/retry calls would need usage logs to account for.

### Arike et al.

- **Sprint brief less-is-more claim:** supported, with scope. Fig. 3/Table 4 compare fixed model/environment combinations and include cluster-bootstrap confidence intervals. CoT+action is best only for SHADE-Arena with Claude-3.7-Sonnet among the main eight combinations; filtered protocols win or tie elsewhere. This does not imply that removing arbitrary detail universally improves monitoring.

- **16.8 percentage-point headline:** independently reproduced from the released reasoning-model CSV. EaE-minus-best-baseline combined gains across the five models are 22.1434, 17.3927, 14.8451, 12.0054 and 17.5660 pp; their mean is **16.7905 pp**, rounding to **16.8**. The paper explicitly averages models and sample-weights task subgroups; a percentage increase should not be substituted for a percentage-point gain.

- **Random log-AUROC baseline:** for TPR=FPR on [.01,1], normalized integral is (1−.01)/ln(100)=.2149758, matching the reported .215. The BCB metric helper uses a non-interpolated strict-threshold TPR@1% FPR, consistent with Appendix B.2. A separate MLE ROC utility interpolates, so its output should not be substituted without identifying the analysis route.

### Radev et al. / SCHEME

- **Monitor sees separate words/actions evidence:** §4 evaluates Code+Comms, OnlyCode, OnlyComms and per-agent code slices. At the stated calibration, Codex overall TPR is 81%/68%/46%/61%; Gemini is 100%/99%/93%/99%. This supports joint code/communication visibility as useful. It does not describe a dedicated detector that independently establishes agreement between agents' statements and actions; Single-Agent still averages scores from multiple agents.

- **97%→90% comms-aware detection versus Table 10:** these are averages over Code+Comms and OnlyComms, not the full-visibility monitor alone: notice (100+94)/2=97%; notice+hint (96+83)/2=89.5%≈90%. The no-comms average is (83+80)/2=81.5%, then (92+92)/2=92% (unrounded inputs can yield the text's 81/93). Thus these numbers do not contradict the full monitor's 96% success TPR under notice+hint.

- **<3% undetected sabotage under full visibility:** under notice+hint, 53 successes and ≈96% success detection imply 2 misses, 2/85=2.353% of all attempts. OnlyComms gives 9/85=10.588%≈11%, matching Fig. 8. These rates use all attempts as denominator, not only successful sabotage.

- **Inventory/topology sums:** Table 1 pairings sum to 11 and instances to 17. Table 7 gives BUS 57/70=81.43% and STAR 55/70=78.57%, consistent with the stated 81/79. The 17×5=85 sampling design is consistent. The 21/410≈5.12% manual-review statement is arithmetic-consistent, though review accuracy cannot be assessed without annotations.

## COULD NOT VERIFY

### Colosseum

- **Exact Fig. 4 correlations/point membership:** the supplied chart was rendered and inspected. Its weak negative trends are compatible with the stated r=−.243/−.1429 (advantage) and −.0386/−.2401 (overall regret), but the release lacks the 19-model per-run table and the matching figure script. Exact r values and which models occupy hidden/direct quadrants could not be independently recomputed. The two pairs of r describe different y-axes, not contradictory estimates of the same quantity.

- **Sprint brief strength:** 'weak negative sample association' is supported by §5.4, but 'non-trivial' population association is not established. For the advantage correlations, r²=.05905 and .02042. The paper itself cautions in footnote 2 that the relation may not be significant. Do not use these values as validated calibration coefficients.

- **Full figure regeneration/configuration provenance:** source configs include temperature .7, 1500 output tokens and ten Jira seeds, consistent with parts of §5.3, but the shown sweep has fewer model entries than Fig. 4's 19, lacks a paper-version run manifest/raw logs, and the judge CLI defaults to gpt-4o-mini rather than GPT-5.4. These are reproduction requirements/unknown original overrides, not proof the experiments used the wrong models. Terrarium main is version .2.0 while Colosseum pins terrarium-agents .1.1; a fresh main checkout is not the pinned dependency.

- **Normalized overall regret:** some Jira helpers use (opt−actual)/opt, while the Hospital main comparison helper supports empirical min–max scaling. Without exact figure commands, no blanket claim that every published normalization is wrong is justified. COL-02 records the separate, demonstrable Hospital coalition-regret semantic mismatch.

- **Significance of persuasion effects:** only five seeds and standard-error bars are specified; no identifiable inferential test for every 'significant' claim was recovered. The unavailable per-seed outcomes are needed to test those claims, so their truth is not refuted here.

### TraceGuard

- **The causal collusion interpretation:** using the same model family in monitor/agent roles is not itself a test of an intentionally colluding monitor. The released monitor prompts ask for security evaluation, and no trained/adversarial collusion policy, collusion signal experiment, or monitor-side adversarial objective is supplied. The paper acknowledges fixed attack policies, but its stronger mechanism claim ('structure constrains collusion') remains unestablished; TG-01 supplies a concrete alternative explanation for the baseline collapse.

- **95–100% overview versus 70.8% main pipeline:** the overview/Key Takeaways quote earlier structured-monitor observations, not the larger hybrid run. They should be read with named variants, thresholds and n. No new matched baseline rerun supports attributing the whole improvement to decomposition.

- **Train/test leakage and tuning:** weights are described as intuitive/iteratively calibrated, but there is no released split/task-ID manifest to establish disjoint calibration and evaluation sets. Leakage cannot be confirmed or excluded. AgentHarm category means without per-category n, benign controls, or detection targets do not verify cross-domain discrimination.

- **Runtime model/configuration provenance:** run_eval.py defaults to GPT-4o/GPT-4o-mini and limit=5, whereas §4.1 names Claude Sonnet 4/GPT-4.1-mini and 20 samples/configuration. Overrides can reconcile these values; missing commands/logs prevent deciding which were used. No API evaluation was run.

### When Agents Lie

- **'Emerge in Round 0' and 'persist across all 10 rounds':** Fig. 4 and Table 14 give all-round means, not heterogeneous round-level payoff gaps. Tables 11–13 are homogeneous; Table 17 gives early/late trust, not round-level heterogeneous payoffs. No tracked .json/.jsonl/.csv output observations are released. Thus −1.55/−2.60 aggregate gaps alone cannot verify that every round has the same sign. This is an evidence gap, not a demonstrated reversal.

- **Tiny rounding/cohort differences:** the means recomputed from ten printed Table 11 round percentages differ from some Fig. 2/Table 8 values by 0.1 pp, e.g. Llama Fishing is 10.1 from Table 11/Table 8 versus 10.2 in Fig. 2. Rounded round entries, missing parses or denominators could explain this; raw counts are needed before labeling it an error.

- **Actual experimental defaults:** the CLI defaults to 50 trials and one round, while the paper uses 20 and ten. The README gives the proper explicit --trials 20 --rounds 10 example. Defaults alone are not evidence of wrong experimental n. Precise sampling settings, seeds and the 126-condition output manifest were not available.

- **Raw-to-scored action consistency:** numeric stage actions are converted to integers for classification, then game-specific parsing clamps them before payoffs. Without logs, the frequency of out-of-range/missing actions and their effects on deception/payoff coupling cannot be measured. WAL-04 records the explicit impossible published payoff separately.

### Arike et al.

- **Code/data discovery:** the PDF's Reproducibility Statement (p.10) identifies github.com/rajamoreno/info-access-mle-sabotage and github.com/Aether-AIS/cotrh-blue-team. Both Git repositories were obtained. The BCB Windows checkout failed on colon-containing paths; 400 valid files were recovered from the Git archive, with four invalid completed-ID names recorded in evidence/windows_checkout.json. This is a local platform limitation, not a research error.

- **SHADE-Arena regeneration:** p.10 explicitly keeps its repository private to avoid contamination and offers access to researchers. No public paper-specific SHADE repository was identified in the supplied PDF; its complete runs could not be regenerated here.

- **Raw MLE/BCB reruns:** MLE README links external Dropbox and Google Drive logs, and both releases include useful derived data. Those bulk external logs, API generation, Kaggle downloads and Docker tasks were not run/downloaded. Absence from the checkout does not establish absence from the advertised external release.

- **Fig. 7 price provenance:** the available price helper uses input-only token pricing and lacks EaE among its content categories, while the figure labels total I/O price and includes EaE. The matching figure command/inputs are needed to trace the plot. This is not sufficient evidence to claim the published Pareto frontier is numerically wrong.

- **'Four comparison pairs' monitorability wording (§5.3):** Fig. 5 favors DeepSeek-V3 over R1 when limited to GPT-4.1-mini protocols (best 67.3% versus 59.7%), but favors R1 when the stronger EaE evaluator is allowed (72.5% versus 70.1%). The claim's intended comparison set needs clarification; no unqualified reversal of the paper's strongest-elicitation claim is asserted.

### Radev et al. / SCHEME

- **Code/data links:** the entire PDF text and all link annotations were searched, including abstract, footnotes and appendices. No paper-specific code repository or released dataset link was found. The GitHub link to meridianlabs-ai/inspect_scout is a dependency, not SCHEME's benchmark release. Therefore there was no identifiable SCHEME repository to clone or offline example to run. monitor_analysis.py is named in the appendix but not made retrievable by a link.

- **Held-out false-positive performance:** Appendix J calibrates the 98th-percentile threshold on the same baseline pool used to label the nominal FPR. No disjoint benign validation pool or out-of-sample false-positive interval is described. The ≤2% claim is therefore verifiable as an empirical calibration target only, not a deployment guarantee. Table 9 also drops unparseable samples (e.g. Code+Comms baseline n=63/61 versus 76/77 in other views); score-level data and a failure policy are needed for a missingness sensitivity check.

- **Recovery as a causal driver:** mode/recovery labels are observational scanner outputs, with only 21/410 trajectories manually reviewed and no released agreement matrix. A causal claim that improving recovery would close the model gap requires an intervention or stronger controls. SCH-01 concerns the directly checkable arithmetic, not the latent causal interpretation.

- **Joint-only enforcement, exact prompts/model IDs and thresholds:** disjoint permissions and mechanisms are described in Appendices A–D, but implementation, run logs, exact evaluation prompts and task/scorer assets are unavailable. Their actual enforcement, absence of leakage and exact model hyperparameter implementation could not be independently tested. No paid generation was attempted.

## Ranked top 10 for building a words-versus-actions collusion detector

1. **Repair TraceGuard's blind baselines before trusting the 0%→95% comparison (TG-01).** A monitor that never sees the action is not a usable reference implementation.
2. **Define premeditation with actual=plan where that is the intended target (WAL-01).** Preserve a separate third-action category; announcement breaking alone is not proof the eventual action was privately planned.
3. **Resolve TraceGuard's score provenance before importing its thresholds (TG-02/TG-04).** Published dimension means, composite means and aggregation rules currently cannot all describe the same released pipeline.
4. **Keep unilateral regret separate from reward shortfall (COL-02).** They answer different questions and can disagree at zero unilateral regret. Check the exact environment/plot route before labeling collusion.
5. **Report attack detection, honest false positives and actual task success separately (TG-03).** An honest action allowed through may still fail the task; a detected attack need not be a prevented successful attack.
6. **Give trusted components an explicit alarm rule if adversarial monitors can suppress scores (TG-06).** Majority weight alone does not give the claimed protection, and same-backbone tests do not establish resistance to deliberate collusion.
7. **Use paired code/communication views with a clearly defined denominator.** SCHEME supports added value from combined visibility, but its best rates use ten monitor draws per trajectory, calibrated thresholds, and all attempted sabotage as positives. Its full-view <3% stealthy rate is a fraction of all attempts.
8. **Retain the supported information-filtering result.** Arike's 16.8 pp EaE gain reproduces from its released aggregate CSV; its less-is-more finding supports testing filtered context alongside full context. It does not prove arbitrary detail removal is beneficial.
9. **Validate game/condition boundaries instead of generalizing a single headline.** Binary high-deception conditions support >90% stated premeditation; numeric-game metrics need repair. El Farol's large payoff gaps contradict the advertised <.40 boundary (WAL-02), and Fishing's default boundary also differs (WAL-05).
10. **Budget for independent validation and pin artifacts.** Colosseum's negative sample correlations are weak/unrecomputed; TraceGuard's n=7/20 observations are imprecise; SCHEME's ≤2% FPR is calibrated on its baseline pool. Release aligned scores, task IDs, prompts, thresholds and run manifests before training/tuning a detector on these findings.

## Sprint brief claims: final verdicts

| Paper | Claim used in the sprint brief | Verdict | Evidence-qualified interpretation |
|---|---|---|---|
| Colosseum | Action coalition advantage has a weak but non-trivial anti-correlation with conversation scores. | **weaker than stated** | Negative sample r is reported (−.243/−.1429, n=19); meaningful population association is not established and exact raw-data recomputation was unavailable. |
| When Agents Lie | More than 90% of deviations were already stated in private plans. | **holds** | Explicitly limited to highest-deception binary-game conditions; it is self-reported planning, not verified latent intent. It does not hold over all games. |
| Radev et al. / SCHEME | Monitors look for multiple agents coordinating independently on what they say and do in sabotage. | **weaker than stated** | The study compares unified code+communication, code-only, communication-only and per-agent code views; it does not implement the more specific independent words/actions coordination detector implied by the wording. |
| TraceGuard | Multiple dimensions improve a single-dimension monitor from 0% to >70%. | **weaker than stated** | Those observed numbers are reported, but the released baseline is blind, runs/configurations differ, and the main >70% hybrid also adds heuristics, recalibration and intent analysis. A causal gain from dimensions alone is not verified. |
| Arike et al. | Giving a monitor too much detail can degrade performance. | **holds** | Specific full-context monitors underperform filtered variants in the evaluated settings; this is a conditional result, not a universal rule. |
