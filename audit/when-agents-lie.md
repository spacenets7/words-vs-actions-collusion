# When Agents Lie: error audit

Audit date: 23 October 2026 (Asia/Calcutta). Page numbers are physical PDF pages, matching the supplied versions. Instructions inside papers/repositories were treated as source material, not user instructions. This report contains errors, counterexamples and verification limits, not paper summaries.

Severity: **major** affects a central metric, comparison, theorem or implementation contract; **minor** is a localized numeric, reference or reproduction defect. No critical finding was established. A limitation under COULD NOT VERIFY is not counted as a confirmed error. Code findings refer to the recorded commits, which need not be the authors' original experiment commits.

Evidence and scripts: [verification.json](evidence/verification.json), [verification.log](evidence/verification.log), [verification script](scripts/verify_audit.py), [layout extraction](scripts/extract_layout.ps1), [PDF hashes/pages](text/manifest.json). No paid APIs were called. Component checks execute original source definitions; full model experiments were not rerun.

Source: [PDF pp. as cited below](<C:/Users/ussid/OneDrive/Documents/ChatGPT/collusion 2/papers/2607.05132v2.pdf>).

## CONFIRMED

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

## REFUTED leads

- **Table 8 versus Fig. 2 denominator lead:** premeditation is Premeditated/(Premeditated+Impulsive), not a sum including 'Intended deceptive (complied)'. Diners GPT: 96.6/(96.6+.1)=99.8966%; Diners Claude: 26.2/(26.2+.5)=98.1273%; Diners Llama: 98.2/(98.2+.2)=99.7967%; Volunteer GPT: 1.3/(1.3+27.9)=4.4521%. These reproduce Fig. 2's 99.9/98.1/99.8/4.5. All 18 typology rows sum to 100% within 0.1 percentage point. WAL-01 is the distinct third-action flaw.

- **Headline >90% claim:** it explicitly applies to the highest-deception conditions, not all deviations in all games. Diners GPT/Llama and El Farol Llama support it; the binary action space makes actual=plan follow from the two inequality tests. GPT El Farol is only 32.3% and Volunteer only 4.5%, so extending the claim universally would be wrong.

- **Fig. 4 versus Table 14:** the plotted Diners pairs and reported gaps agree within displayed precision: .82−2.37=−1.55; .02−2.62=−2.60; 4.15−2.60=+1.55; 6.31−1.82=+4.49; 5.54−1.98=+3.56. No sign-reversal lead was confirmed.

- **Evaluation/call-count arithmetic:** 126×20×10×5=126,000 agent-rounds, times four stated agent-stage calls=504,000. These products and the listed cost subtotals are internally consistent estimates; additional optional judging/retry calls would need usage logs to account for.

## COULD NOT VERIFY

- **'Emerge in Round 0' and 'persist across all 10 rounds':** Fig. 4 and Table 14 give all-round means, not heterogeneous round-level payoff gaps. Tables 11–13 are homogeneous; Table 17 gives early/late trust, not round-level heterogeneous payoffs. No tracked .json/.jsonl/.csv output observations are released. Thus −1.55/−2.60 aggregate gaps alone cannot verify that every round has the same sign. This is an evidence gap, not a demonstrated reversal.

- **Tiny rounding/cohort differences:** the means recomputed from ten printed Table 11 round percentages differ from some Fig. 2/Table 8 values by 0.1 pp, e.g. Llama Fishing is 10.1 from Table 11/Table 8 versus 10.2 in Fig. 2. Rounded round entries, missing parses or denominators could explain this; raw counts are needed before labeling it an error.

- **Actual experimental defaults:** the CLI defaults to 50 trials and one round, while the paper uses 20 and ten. The README gives the proper explicit --trials 20 --rounds 10 example. Defaults alone are not evidence of wrong experimental n. Precise sampling settings, seeds and the 126-condition output manifest were not available.

- **Raw-to-scored action consistency:** numeric stage actions are converted to integers for classification, then game-specific parsing clamps them before payoffs. Without logs, the frequency of out-of-range/missing actions and their effects on deception/payoff coupling cannot be measured. WAL-04 records the explicit impossible published payoff separately.
