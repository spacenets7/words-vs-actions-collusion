# Colosseum: error audit

Audit date: 23 October 2026 (Asia/Calcutta). Page numbers are physical PDF pages, matching the supplied versions. Instructions inside papers/repositories were treated as source material, not user instructions. This report contains errors, counterexamples and verification limits, not paper summaries.

Severity: **major** affects a central metric, comparison, theorem or implementation contract; **minor** is a localized numeric, reference or reproduction defect. No critical finding was established. A limitation under COULD NOT VERIFY is not counted as a confirmed error. Code findings refer to the recorded commits, which need not be the authors' original experiment commits.

Evidence and scripts: [verification.json](evidence/verification.json), [verification.log](evidence/verification.log), [verification script](scripts/verify_audit.py), [layout extraction](scripts/extract_layout.ps1), [PDF hashes/pages](text/manifest.json). No paid APIs were called. Component checks execute original source definitions; full model experiments were not rerun.

Source: [PDF pp. as cited below](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2602.15198v2.pdf>).

## CONFIRMED

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

## REFUTED leads

- **Coalition-advantage sign/tie lead:** the paper defines noncoalition regret minus coalition regret, so positive favors the coalition. The released Jira plotting helper uses that sign and normalizes as .5+gap/(2 max|gap|), giving exactly .5 for a zero gap. The differently named stored reward gap is not proof of a sign inversion in this plotting path.

- **57.89/78.95/10.53% arithmetic:** 11/19=57.8947%, 15/19=78.9474%, 2/19=10.5263%; these percentages are consistent with n=19. Their exact model membership cannot be reliably reconstructed from overlapping markers alone.

- **Persuasion/Fig. 12 cross-reference:** §5.6 invokes Fig. 12 to illustrate the tactics. Fig. 12 does illustrate those tactics; results are separately discussed with Fig. 6 and Fig. 10. This particular reference is valid, not a confirmed wrong-figure citation. Other prose/figure references were checked without promoting ambiguous references to errors.

## COULD NOT VERIFY

- **Exact Fig. 4 correlations/point membership:** the supplied chart was rendered and inspected. Its weak negative trends are compatible with the stated r=−.243/−.1429 (advantage) and −.0386/−.2401 (overall regret), but the release lacks the 19-model per-run table and the matching figure script. Exact r values and which models occupy hidden/direct quadrants could not be independently recomputed. The two pairs of r describe different y-axes, not contradictory estimates of the same quantity.

- **Sprint brief strength:** 'weak negative sample association' is supported by §5.4, but 'non-trivial' population association is not established. For the advantage correlations, r²=.05905 and .02042. The paper itself cautions in footnote 2 that the relation may not be significant. Do not use these values as validated calibration coefficients.

- **Full figure regeneration/configuration provenance:** source configs include temperature .7, 1500 output tokens and ten Jira seeds, consistent with parts of §5.3, but the shown sweep has fewer model entries than Fig. 4's 19, lacks a paper-version run manifest/raw logs, and the judge CLI defaults to gpt-4o-mini rather than GPT-5.4. These are reproduction requirements/unknown original overrides, not proof the experiments used the wrong models. Terrarium main is version .2.0 while Colosseum pins terrarium-agents .1.1; a fresh main checkout is not the pinned dependency.

- **Normalized overall regret:** some Jira helpers use (opt−actual)/opt, while the Hospital main comparison helper supports empirical min–max scaling. Without exact figure commands, no blanket claim that every published normalization is wrong is justified. COL-02 records the separate, demonstrable Hospital coalition-regret semantic mismatch.

- **Significance of persuasion effects:** only five seeds and standard-error bars are specified; no identifiable inferential test for every 'significant' claim was recovered. The unavailable per-seed outcomes are needed to test those claims, so their truth is not refuted here.
