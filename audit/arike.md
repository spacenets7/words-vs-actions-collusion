# Arike et al.: error audit

Audit date: 23 October 2026 (Asia/Calcutta). Page numbers are physical PDF pages, matching the supplied versions. Instructions inside papers/repositories were treated as source material, not user instructions. This report contains errors, counterexamples and verification limits, not paper summaries.

Severity: **major** affects a central metric, comparison, theorem or implementation contract; **minor** is a localized numeric, reference or reproduction defect. No critical finding was established. A limitation under COULD NOT VERIFY is not counted as a confirmed error. Code findings refer to the recorded commits, which need not be the authors' original experiment commits.

Evidence and scripts: [verification.json](evidence/verification.json), [verification.log](evidence/verification.log), [verification script](scripts/verify_audit.py), [layout extraction](scripts/extract_layout.ps1), [PDF hashes/pages](text/manifest.json). No paid APIs were called. Component checks execute original source definitions; full model experiments were not rerun.

Source: [PDF pp. as cited below](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2601.21112v2.pdf>).

## CONFIRMED

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

## REFUTED leads

- **Sprint brief less-is-more claim:** supported, with scope. Fig. 3/Table 4 compare fixed model/environment combinations and include cluster-bootstrap confidence intervals. CoT+action is best only for SHADE-Arena with Claude-3.7-Sonnet among the main eight combinations; filtered protocols win or tie elsewhere. This does not imply that removing arbitrary detail universally improves monitoring.

- **16.8 percentage-point headline:** independently reproduced from the released reasoning-model CSV. EaE-minus-best-baseline combined gains across the five models are 22.1434, 17.3927, 14.8451, 12.0054 and 17.5660 pp; their mean is **16.7905 pp**, rounding to **16.8**. The paper explicitly averages models and sample-weights task subgroups; a percentage increase should not be substituted for a percentage-point gain.

- **Random log-AUROC baseline:** for TPR=FPR on [.01,1], normalized integral is (1−.01)/ln(100)=.2149758, matching the reported .215. The BCB metric helper uses a non-interpolated strict-threshold TPR@1% FPR, consistent with Appendix B.2. A separate MLE ROC utility interpolates, so its output should not be substituted without identifying the analysis route.

## COULD NOT VERIFY

- **Code/data discovery:** the PDF's Reproducibility Statement (p.10) identifies github.com/rajamoreno/info-access-mle-sabotage and github.com/Aether-AIS/cotrh-blue-team. Both Git repositories were obtained. The BCB Windows checkout failed on colon-containing paths; 400 valid files were recovered from the Git archive, with four invalid completed-ID names recorded in evidence/windows_checkout.json. This is a local platform limitation, not a research error.

- **SHADE-Arena regeneration:** p.10 explicitly keeps its repository private to avoid contamination and offers access to researchers. No public paper-specific SHADE repository was identified in the supplied PDF; its complete runs could not be regenerated here.

- **Raw MLE/BCB reruns:** MLE README links external Dropbox and Google Drive logs, and both releases include useful derived data. Those bulk external logs, API generation, Kaggle downloads and Docker tasks were not run/downloaded. Absence from the checkout does not establish absence from the advertised external release.

- **Fig. 7 price provenance:** the available price helper uses input-only token pricing and lacks EaE among its content categories, while the figure labels total I/O price and includes EaE. The matching figure command/inputs are needed to trace the plot. This is not sufficient evidence to claim the published Pareto frontier is numerically wrong.

- **'Four comparison pairs' monitorability wording (§5.3):** Fig. 5 favors DeepSeek-V3 over R1 when limited to GPT-4.1-mini protocols (best 67.3% versus 59.7%), but favors R1 when the stronger EaE evaluator is allowed (72.5% versus 70.1%). The claim's intended comparison set needs clarification; no unqualified reversal of the paper's strongest-elicitation claim is asserted.
