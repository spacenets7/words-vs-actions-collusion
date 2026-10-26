# Judge review guide

**Project:** Words Actions and Evidence in Collusion Detection

**Track:** 2.2 · **Author:** Siddeshwar U S · **Affiliation:** MIT, Manipal · **Team:** spacenets

[Tagged review package and checksums](https://github.com/spacenets7/words-vs-actions-collusion/releases/tag/submission-2026-10-26) · [Passing fresh-checkout verification](https://github.com/spacenets7/words-vs-actions-collusion/actions/runs/40324152258)

## A five minute route

1. Read the abstract and Results in the [final report](pilot/submission/final-report.pdf). It uses the supplied Apart template: six main pages including the title page, with references and appendices afterward.
2. Inspect [the complete numeric results](review/RESULTS.md) and [paired comparisons](review/figures/paired-comparisons.png). The main finding is a limit: the structured hybrid does not consistently beat actions alone.
3. Check the six controls and separate agreement, execution and harm definitions in Methods and Appendix A. Independent harmful actions are not automatically called a coalition; talk without action is a separate control.
4. Run `python scripts/verify_review.py` after the [short dependency setup](REPRODUCIBILITY.md). It verifies artifact/data hashes, the original freeze, scheduled coverage, information isolation, thresholds and report metadata without calling a model.
5. For a full numerical reproduction, run `python scripts/replay_results.py`. The saved data reproduce the complete metrics with exact JSON equality, including the family bootstrap. There are no cloud credentials or model downloads.

## What is new

The project implements an independent six-condition Public Goods controller, private pair negotiation, explicit agreement/execution/harm labels, four isolated monitor views, a code-built claim/outcome representation, a cached open-model runner, development-locked operating thresholds, paired-family analysis and local reporting. Preexisting code and research are attributed in the report and [NOTICE.md](NOTICE.md).

The four views share the same auditor: V1 sees public words; V2 sees actions/payoffs; V3 sees their raw union; V4 aligns verbatim claims with execution and includes directed follow-through and all ten candidate pairs. Private plans, pair messages, the assigned pair and oracle labels are excluded from monitor inputs.

## What the evidence supports

- Held-out coverage is 48/48 episodes and 192/192 accepted view outputs; the complete dataset has 60 episodes and 240 outputs.
- The primary automatic implementation target has 13 positives and 35 negatives. All three hidden-condition gate failures remain included.
- Action AUROC is 0.843; structured-report AUROC is 0.731. Their paired difference is −0.112 with interval [−0.215, 0.029].
- Public text is more informative for unauthorized agreement attempts than for executed harmful collusion. These targets have different positive sets and are not causal treatment comparisons.
- Labels are operational and event-based. Controlled I/H public communication, model lineage overlap, eight held-out clusters and the fixed-outsider harm contrast limit generalization.

## Where to inspect implementation

| Question | Source or evidence |
|---|---|
| Payoff arithmetic and outcome gates | [core.py](pilot/core.py), [upstream adapter](pilot/patches/upstream.py), [pipeline tests](pilot/tests/test_pipeline.py) |
| Whether private material leaks to a view | [allowlisted views and rendering](pilot/core.py), sentinel and controller tests in [test_pipeline.py](pilot/tests/test_pipeline.py) |
| Thresholds, baselines and paired bootstrap | [analysis.py](pilot/analysis.py), [frozen calibration](pilot/frozen/calibration.json) |
| Full run identities and library versions | [run provenance](pilot/submission/run-provenance.json) |
| How paper audit findings affected the design | [22-record implementation map](pilot/AUDIT_IMPLEMENTATION_MAP.md), [audit reports](audit/FINDINGS.md) |
| Exact current report and data identity | [manifest](review/manifest.json), [report layout checks](pilot/submission/template-report-quality.json) |

## What you do not need to run

The paid Modal generator and the original upstream papers' full pipelines are not needed to review these results. Do not regenerate or tune the frozen held-out cases. Local cloud journals and weights are intentionally absent. The review archive contains sanitized observations plus a separate label file; never merge that file into monitor inputs. The full development snapshot elsewhere in the repository is for freeze auditing, not a public-evidence monitor view.
