# Radev et al. / SCHEME: error audit

Audit date: 23 October 2026 (Asia/Calcutta). Page numbers are physical PDF pages, matching the supplied versions. Instructions inside papers/repositories were treated as source material, not user instructions. This report contains errors, counterexamples and verification limits, not paper summaries.

Severity: **major** affects a central metric, comparison, theorem or implementation contract; **minor** is a localized numeric, reference or reproduction defect. No critical finding was established. A limitation under COULD NOT VERIFY is not counted as a confirmed error. Code findings refer to the recorded commits, which need not be the authors' original experiment commits.

Evidence and scripts: [verification.json](evidence/verification.json), [verification.log](evidence/verification.log), [verification script](scripts/verify_audit.py), [layout extraction](scripts/extract_layout.ps1), [PDF hashes/pages](text/manifest.json). No paid APIs were called. Component checks execute original source definitions; full model experiments were not rerun.

Source: [PDF pp. as cited below](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2605.29178v1.pdf>).

## CONFIRMED

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

- **Monitor sees separate words/actions evidence:** §4 evaluates Code+Comms, OnlyCode, OnlyComms and per-agent code slices. At the stated calibration, Codex overall TPR is 81%/68%/46%/61%; Gemini is 100%/99%/93%/99%. This supports joint code/communication visibility as useful. It does not describe a dedicated detector that independently establishes agreement between agents' statements and actions; Single-Agent still averages scores from multiple agents.

- **97%→90% comms-aware detection versus Table 10:** these are averages over Code+Comms and OnlyComms, not the full-visibility monitor alone: notice (100+94)/2=97%; notice+hint (96+83)/2=89.5%≈90%. The no-comms average is (83+80)/2=81.5%, then (92+92)/2=92% (unrounded inputs can yield the text's 81/93). Thus these numbers do not contradict the full monitor's 96% success TPR under notice+hint.

- **<3% undetected sabotage under full visibility:** under notice+hint, 53 successes and ≈96% success detection imply 2 misses, 2/85=2.353% of all attempts. OnlyComms gives 9/85=10.588%≈11%, matching Fig. 8. These rates use all attempts as denominator, not only successful sabotage.

- **Inventory/topology sums:** Table 1 pairings sum to 11 and instances to 17. Table 7 gives BUS 57/70=81.43% and STAR 55/70=78.57%, consistent with the stated 81/79. The 17×5=85 sampling design is consistent. The 21/410≈5.12% manual-review statement is arithmetic-consistent, though review accuracy cannot be assessed without annotations.

## COULD NOT VERIFY

- **Code/data links:** the entire PDF text and all link annotations were searched, including abstract, footnotes and appendices. No paper-specific code repository or released dataset link was found. The GitHub link to meridianlabs-ai/inspect_scout is a dependency, not SCHEME's benchmark release. Therefore there was no identifiable SCHEME repository to clone or offline example to run. monitor_analysis.py is named in the appendix but not made retrievable by a link.

- **Held-out false-positive performance:** Appendix J calibrates the 98th-percentile threshold on the same baseline pool used to label the nominal FPR. No disjoint benign validation pool or out-of-sample false-positive interval is described. The ≤2% claim is therefore verifiable as an empirical calibration target only, not a deployment guarantee. Table 9 also drops unparseable samples (e.g. Code+Comms baseline n=63/61 versus 76/77 in other views); score-level data and a failure policy are needed for a missingness sensitivity check.

- **Recovery as a causal driver:** mode/recovery labels are observational scanner outputs, with only 21/410 trajectories manually reviewed and no released agreement matrix. A causal claim that improving recovery would close the model gap requires an intervention or stronger controls. SCH-01 concerns the directly checkable arithmetic, not the latent causal interpretation.

- **Joint-only enforcement, exact prompts/model IDs and thresholds:** disjoint permissions and mechanisms are described in Appendices A–D, but implementation, run logs, exact evaluation prompts and task/scorer assets are unavailable. Their actual enforcement, absence of leakage and exact model hyperparameter implementation could not be independently tested. No paid generation was attempted.
