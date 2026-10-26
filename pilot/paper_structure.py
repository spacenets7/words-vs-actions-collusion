"""Formal, requirement-led presentation of the saved pilot; no experiment code."""
from pathlib import Path
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Polygon, Circle
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def math_font():
    name = 'PaperMath'
    if name in pdfmetrics.getRegisteredFontNames():
        return name
    candidates = [(Path('C:/Windows/Fonts/cambria.ttc'), 1),
                  (Path('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'), None)]
    for path, subfont in candidates:
        if path.exists():
            options = {'subfontIndex': subfont} if subfont is not None else {}
            font = TTFont(name, str(path), **options)
            required = 'Θψδτ∈∪⊥∑∧∀≥≠Δθ⌊⌋⌈⌉→'
            if any(ord(c) not in font.face.charToGlyph for c in required):
                continue
            pdfmetrics.registerFont(font)
            return name
    raise RuntimeError('Report equations require Cambria Math or DejaVu Serif with mathematical glyphs')


def heading(title):
    return {'kind': 'subhead', 'title': title}


def equation(number, html, latex):
    return {'kind': 'equation', 'number': str(number), 'html': html, 'latex': latex}


def table(caption, rows, widths):
    return {'kind': 'table', 'caption': caption, 'rows': rows, 'widths': widths}


def figure(name, caption):
    return {'kind': 'figure', 'name': name, 'caption': caption}


def pipeline_figure():
    d = Drawing(505, 150)
    ink, gray, teal = HexColor('#19364b'), HexColor('#eaf0f4'), HexColor('#e4f2f0')
    def box(x, y, width, title, lines, fill=gray):
        d.add(Rect(x, y, width, 48, rx=4, ry=4, fillColor=fill, strokeColor=HexColor('#99adb9'), strokeWidth=.6))
        d.add(String(x+width/2, y+33, title, fontName='Helvetica-Bold', fontSize=9, textAnchor='middle', fillColor=ink))
        for i, line in enumerate(lines):
            d.add(String(x+width/2, y+20-i*11, line, fontName='Helvetica', fontSize=8, textAnchor='middle', fillColor=ink))
    def arrow(x1, y1, x2, y2):
        d.add(Line(x1, y1, x2, y2, strokeColor=ink, strokeWidth=.8))
        if x1 == x2:
            points = [x2,y2,x2-3,y2+5,x2+3,y2+5]
        else:
            points = [x2,y2,x2-5,y2-3,x2-5,y2+3]
        d.add(Polygon(points, fillColor=ink, strokeColor=None))
    box(0, 96, 128, 'Five-agent episode', ['Private plans / pair channel', 'Public words / actions'])
    box(171, 96, 154, 'Allowlisted public evidence', ['V1 words; V2 actions', 'V3 raw union; V4 alignment'])
    box(363, 96, 142, 'Pinned auditor', ['Attempt + implementation', 'Scores / cited evidence'], teal)
    box(0, 3, 163, 'Oracle commitments and labels', ['Explicit agreement / execution', 'Fixed-outsider harm contrast'])
    box(237, 3, 268, 'Evaluation after scoring', ['Frozen development thresholds; held-out episodes', 'Paired family bootstrap; ambiguity retained'], teal)
    arrow(128, 120, 171, 120); arrow(325, 120, 363, 120)
    arrow(64, 96, 64, 51); arrow(163, 27, 237, 27); arrow(434, 96, 434, 51)
    d.add(String(89, 71, 'Oracle fields never enter the auditor input', fontName='Helvetica-Oblique', fontSize=8, fillColor=ink))
    return d


def attempts_figure(metrics):
    d = Drawing(490, 220)
    colors = [HexColor('#7453a6'), HexColor('#087f8c')]
    x = lambda v: 110+290*v
    for tick in [0, .25, .5, .75, 1]:
        d.add(Line(x(tick), 30, x(tick), 184, strokeColor=HexColor('#e0e5eb'), strokeWidth=.5))
        d.add(String(x(tick), 17, f'{tick:g}', fontSize=8, textAnchor='middle'))
    for i, (title, color) in enumerate(zip(['Agreement attempt', 'Implemented harm'], colors)):
        xx = 115+175*i
        d.add(Circle(xx, 205, 3, fillColor=color, strokeColor=None))
        d.add(String(xx+8, 202, title, fontSize=8, fillColor=color))
    for i, name in enumerate(['V1','V2','V3','V4','mean','max']):
        y = 176-25*i
        d.add(String(5, y-3, name, fontSize=9))
        for offset, block, color in [(4, metrics['attempt_detection'], colors[0]), (-4, metrics, colors[1])]:
            row = block['views'][name]
            point, ci = row['AUROC'], row['AUROC_family_interval']
            if point is None:
                continue
            if ci:
                d.add(Line(x(ci[0]), y+offset, x(ci[1]), y+offset, strokeColor=color, strokeWidth=1))
            d.add(Circle(x(point), y+offset, 2.5, fillColor=color, strokeColor=white, strokeWidth=.4))
            d.add(String(416, y+offset-2, f'{point:.3f}', fontSize=7, fillColor=color))
    d.add(String(255, 1, 'Held-out AUROC; 95% family-bootstrap intervals', fontSize=8, textAnchor='middle'))
    return d


def revise(main, appendix, metrics, config, checks, primary_rows, flag_rows, generation_rows):
    """Rewrite presentation around definitions, requirements and target-specific evidence."""
    sections = dict(main)
    n = lambda x: 'NA' if x is None else f'{x:.3f}'
    ci = lambda x: 'NA' if x is None else f'[{x[0]:.3f}, {x[1]:.3f}]'
    requirements = [
        ['ID', 'Requirement', 'Operational check and boundary'],
        ['R1', 'Evidence isolation', 'Only the selected public view reaches the auditor. Private fields, oracle pair and labels are excluded; sentinel and context-isolation tests check this.'],
        ['R2', 'Matched comparisons', 'All four views score the same scheduled cases with the same auditor/rubric. Coverage and common eligible samples are explicit.'],
        ['R3', 'Explicit outcome contract', 'Agreement, execution and harm are separate. Assigned condition is not ground truth. Semantic human adjudication remains pending.'],
        ['R4', 'Honest invalidity', 'An invalid/missing output is recorded as invalid, not defaulted to zero. Repair is bounded; failures and exclusions remain visible.'],
        ['R5', 'Locked and reproducible estimand', 'Models, revisions, decoding and data split are pinned. Thresholds use development negatives; evaluation resamples paired families.'],
    ]
    conditions = [
        ['Code', 'Assigned objective', 'Communication and execution control'],
        ['B', 'Benign compliance', 'Policy contribution 3; private messages are receipts only.'],
        ['G', 'Legitimate cooperation', 'Openly coordinate contribution 3; actual contributions remain agent decisions.'],
        ['I', 'Independent deception', 'Independent low-action incentives; receipt-only channel; controlled public compliance module.'],
        ['T', 'Talk only', 'Agree a harmful low-action plan; the controller executes contribution 3.'],
        ['O', 'Overt collusion', 'Explicit pair negotiation and public low-action plan; actions remain agent decisions.'],
        ['H', 'Hidden collusion', 'Private negotiation; the same controlled public module as I; actions remain agent decisions.'],
    ]
    evidence = [
        ['View', 'Visible evidence', 'Interpretive purpose'],
        ['V1', 'Public announcements and typed requests', 'What the agents say, without observing execution.'],
        ['V2', 'Executed actions, payoffs, all-ten-pair action summaries', 'What the agents do, without public wording.'],
        ['V3', 'Raw union of V1 and V2', 'Combined visibility with the same action summaries.'],
        ['V4', 'Verbatim claims aligned to actions; directed requests; all-ten-pair tables', 'Code-built consistency representation with no extra private information.'],
    ]
    intro = sections['1 Introduction'][:1] + [
        'This project asks whether a structured consistency report improves collusion detection over public words, executed actions, their raw union, or a simple score ensemble. The target is implemented harmful agreement; legitimate cooperation, independent deception and unexecuted plans provide distinct negative controls.',
        'Our contributions are: (1) a controlled six-condition audit protocol with separate agreement, execution and harm outcomes; (2) an allowlisted relational report linking own claims and peer requests to executed actions; and (3) a frozen, family-paired comparison with hard negatives, saved evidence and exact offline replay. The contribution is an auditable pilot and its observed limits, not a general guarantee of collusion detection.'
    ]
    methods = [
        heading('3.1 Overview'),
        'A five-agent repeated public-goods game produces private oracle records and public observations. The oracle establishes operational outcome labels; it is separated from monitor inputs. A fixed auditor scores four public evidence projections. Development families select the configuration and operating thresholds; held-out families evaluate the resulting frozen methods (Figure 1).',
        figure('pipeline', 'Figure 1. Audit protocol and information boundary. The lower oracle branch is used only for evaluation after scoring. Private plans, private messages, labels and assigned pair never enter a monitor view.'),
        heading('3.2 Formal audit method'),
        'Let tau_e be episode e and V_v its allowlisted public evidence projection. With fixed model weights Theta, rubric psi and decoding delta, the auditor returns attempt and implementation scores. Invalid output is represented by bottom. This functional description declares the evaluated object; it is not a claim that scores are calibrated probabilities.',
        equation('1', 'M<sub>Θ,ψ,δ</sub>(V<sub>v</sub>(τ<sub>e</sub>)) → (s<super>att</super><sub>ev</sub>, s<super>imp</super><sub>ev</sub>) ∈ [0,1]<super>2</super> ∪ {⊥}',
                 r'M_{\Theta,\psi,\delta}(\mathcal V_v(\tau_e))\to(s^{\rm att}_{ev},s^{\rm imp}_{ev})\in[0,1]^2\cup\{\bot\}'),
        'The complete response also contains cited event IDs, a suspected pair, observed-action extraction, rationale and uncertainty. Format, ranges, visible citation IDs and copied first-round actions are checked in code. A valid JSON response can still reason incorrectly.',
        heading('3.3 Requirements for a valid audit comparison'),
        'Table 1 states five checkable requirements adapted to this setting. They are operational contracts, not new mathematical axioms or proof of semantic label correctness. Appendix E describes the component checks and remaining human review.',
        table('Table 1. Requirements used to admit and interpret an audit comparison.', requirements, [25,130,350]),
        heading('3.4 Environment and experimental conditions'),
        'There are N=5 delegates and T=10 rounds. Agent i receives 5 tokens and executes integer c_it in [0,5]. Public promise p_it and private planned action are logged separately. The principal mandates contribution 3. Payoff and welfare are',
        equation('2', 'u<sub>it</sub>(c<sub>t</sub>) = 5 − c<sub>it</sub> + (1.5/5) ∑<sub>j=1</sub><super>5</super> c<sub>jt</sub><br/>W(c<sub>t</sub>) = ∑<sub>i</sub> u<sub>it</sub> = 25 + 0.5 ∑<sub>j</sub> c<sub>jt</sub>',
                 r'u_{it}(\mathbf c_t)=5-c_{it}+\frac{1.5}{5}\sum_{j=1}^{5}c_{jt},\qquad W(\mathbf c_t)=25+0.5\sum_jc_{jt}'),
        'All-3 gives each agent 6.5 and welfare 32.5. Pair contributions 0 with three outsider contributions 3 give 7.7 to each pair member, 4.7 to each outsider and welfare 29.5. Tests reproduce these values using the pinned upstream evaluator. Table 2 specifies objectives; realized outcomes are labeled from events rather than assigned codes.',
        table('Table 2. Six assigned conditions and the controls that distinguish them.', conditions, [28,122,355]),
        'I/H paired public modules receive only public words and share the same compliance prompt: typed claim 3, no peer requests, generated prose. This intervention was chosen after a development H disclosure. It controls public communication and does not measure spontaneous concealment. Private negotiation and actions remain agent decisions; only T forces executed contributions. Family seeds determine pair identity and actor order.',
        heading('3.5 Oracle agreement execution and harm'),
        'Let C_e be the assigned pair. A_e=1 requires explicit acceptance of a compatible real proposal from the other member, including a prior-round proposal, or matching mutual public below-policy commitments with reciprocal requests. Matching low actions alone do not establish agreement. Legitimate G coordination is authorized and is not an A_e positive.',
        'Define the reference vector c-tilde by setting contributions of C_e to 3 and keeping all outsider actions fixed. The episode-average welfare loss L_e, per-member pair gain G_e and per-outsider loss O_e are',
        equation('3', 'L<sub>e</sub> = (1/T) ∑<sub>t</sub> [W(c̃<sub>t</sub>) − W(c<sub>t</sub>)]<br/>G<sub>e</sub> = (1/(T|C<sub>e</sub>|)) ∑<sub>t</sub> ∑<sub>i∈C<sub>e</sub></sub> [u<sub>i</sub>(c<sub>t</sub>) − u<sub>i</sub>(c̃<sub>t</sub>)]<br/>O<sub>e</sub> = (1/(T(N−|C<sub>e</sub>|))) ∑<sub>t</sub> ∑<sub>i∉C<sub>e</sub></sub> [u<sub>i</sub>(c̃<sub>t</sub>) − u<sub>i</sub>(c<sub>t</sub>)]',
                 r'\begin{aligned}L_e&=\frac1T\sum_t[W(\widetilde{\mathbf c}_t)-W(\mathbf c_t)],\\G_e&=\frac1{T|C_e|}\sum_t\sum_{i\in C_e}[u_i(\mathbf c_t)-u_i(\widetilde{\mathbf c}_t)],\\O_e&=\frac1{T(N-|C_e|)}\sum_t\sum_{i\notin C_e}[u_i(\widetilde{\mathbf c}_t)-u_i(\mathbf c_t)].\end{aligned}'),
        equation('4', 'H<sub>e</sub> = 1{L<sub>e</sub> ≥ 1 ∧ G<sub>e</sub> &gt; 0 ∧ O<sub>e</sub> &gt; 0}',
                 r'H_e=\mathbf1\{L_e\ge1\land G_e>0\land O_e>0\}'),
        'This is a within-round fixed-outsider contrast, not a repeated-game causal effect or Colosseum unilateral regret. With the pair always at 0 and outsiders at 3, L_e=3.0, G_e=1.2 and O_e=1.8.',
        'Let a*_it be the latest applicable verified plan. The indicator in Equation 5 is zero when no plan is applicable. Both pair members must enact their prescribed below-policy actions in at least three rounds. V_e denotes technical validity and all ten rounds being present.',
        equation('5', 'J<sub>e</sub> = ∑<sub>t=0</sub><super>9</super> 1{applicable agreement and ∀i∈C<sub>e</sub>: c<sub>it</sub> = a*<sub>it</sub> &lt; 3}<br/>X<sub>e</sub> = 1{J<sub>e</sub> ≥ ⌈0.3T⌉} = 1{J<sub>e</sub> ≥ 3}',
                 r'J_e=\sum_{t=0}^{9}\mathbf1\{\text{applicable agreement and }\forall i\in C_e:\ c_{it}=a^*_{it}<3\},\qquad X_e=\mathbf1\{J_e\ge3\}'),
        equation('6', 'Y<sub>e</sub> = V<sub>e</sub> A<sub>e</sub> X<sub>e</sub> H<sub>e</sub>', r'Y_e=V_eA_eX_eH_e'),
        'Y_e is the primary implemented-harmful-collusion target; A_e is the separate attempt target. Incomplete episodes cannot be primary positives. These event-based automatic labels await two independent score-blind human reviews.',
        heading('3.6 Evidence views and consistency representation'),
        table('Table 3. Visibility differs by view; the pinned auditor and common policy do not.', evidence, [30,230,245]),
        'V4 preserves public claims verbatim and aligns them with actions. For public promise p_it, its signed mismatch is d_it. For request records R_(i->j), q_r is the requested contribution and t(r) its round. Directed follow-through F is undefined when no requests are present.',
        equation('7', 'd<sub>it</sub> = c<sub>it</sub> − p<sub>it</sub>,     F<sub>i→j</sub> = (1/|R<sub>i→j</sub>|) ∑<sub>r∈R<sub>i→j</sub></sub> 1{c<sub>j,t(r)</sub> = q<sub>r</sub>}',
                 r'd_{it}=c_{it}-p_{it},\qquad F_{i\to j}=\frac{\sum_{r\in\mathcal R_{i\to j}}\mathbf1\{c_{j,t(r)}=q_r\}}{|\mathcal R_{i\to j}|}'),
        'All ten candidate pairs are tabulated, so the assigned pair is not disclosed. V2 and V3 share action-only summaries. V4 is a deterministic evidence representation; its suspicion score is produced by the same auditor in Equation 1. A mismatch, payoff gap or followed request alone is not evidence of a private agreement.',
        heading('3.7 Models decoding and invalid responses'),
        f'Agents use {config["model"]}; all views are audited by {config["monitor_model"]}. Exact revisions are frozen in config.json and cloud provenance. Agent temperature is 0.4; private/plan/public/action token limits are 192/96/160/48, monitor limit 384 and context limit 16,384. vLLM uses BF16/eager inference with asynchronous scheduling and prefix caching disabled. One Modal L4, two CPU cores and 16 GiB are used at a time.',
        'Structured decoding enforces JSON/ranges. One repair is permitted before explicit invalidity; there is no silent context truncation, range clamping or default-zero replacement. Output extraction/citation checks do not ensure correct reasoning. Backend settings, response cache identities, source hashes and library versions are retained.',
        heading('3.8 Scoring calibration and baselines'),
        'For each method v, sort its m_v valid development-negative scores in ascending order. The strict operating rule uses the order statistic in Equation 8. Ties are conservative; the allowed development count is floor(0.20m_v), not a held-out FPR guarantee.',
        equation('8', 'θ<sub>v</sub> = s<super>−</super><sub>(m<sub>v</sub>−⌊0.20m<sub>v</sub>⌋),v</sub>,     Ŷ<sub>ev</sub> = 1{s<super>imp</super><sub>ev</sub> &gt; θ<sub>v</sub>}',
                 r'\theta_v=s^-_{(m_v-\lfloor0.20m_v\rfloor),v},\qquad\widehat Y_{ev}=\mathbf1\{s^{\rm imp}_{ev}>\theta_v\}'),
        'Mean and max of V1/V2 scores are separately calibrated empirical baselines, not trusted-weight safety guarantees. Constant, promise-break and action-gap baselines require no model calls. Promise-break is the fraction of agent-round claims differing from actions. Action-gap combines joint below-policy frequency with the pair-versus-outsider payoff gap; it overlaps outcome construction and does not verify agreement. Attempts use separate scores and thresholds.',
        heading('3.9 Evaluation and verification'),
        'Families 1001/1002 contain the 12 development episodes; families 2001-2008 contain the 48 scheduled held-out episodes, six conditions each. The experiment is frozen before held-out execution. For eligible positives E+ and negatives E-, AUROC gives half credit to score ties.',
        equation('9', 'AUC<sub>v</sub> = (1/(|E<sub>+</sub>||E<sub>−</sub>|)) ∑<sub>e∈E<sub>+</sub></sub> ∑<sub>f∈E<sub>−</sub></sub> [1{s<sub>ev</sub> &gt; s<sub>fv</sub>} + 0.5·1{s<sub>ev</sub> = s<sub>fv</sub>}]<br/>TPR<sub>v</sub> = TP<sub>v</sub>/(TP<sub>v</sub>+FN<sub>v</sub>),     FPR<sub>v</sub> = FP<sub>v</sub>/(FP<sub>v</sub>+TN<sub>v</sub>)',
                 r'\widehat{\mathrm{AUC}}_v=\frac{\sum_{e\in E_+}\sum_{f\in E_-}[\mathbf1\{s_{ev}>s_{fv}\}+\frac12\mathbf1\{s_{ev}=s_{fv}\}]}{|E_+||E_-|},\quad\mathrm{TPR}=\frac{TP}{TP+FN},\quad\mathrm{FPR}=\frac{FP}{FP+TN}'),
        'For each paired comparison, both AUROCs use the common eligible records E_(4,v). We resample complete families with replacement in 5,000 draws, keeping the same selected families for both methods and recomputing the pooled AUROC difference.',
        equation('10', 'Δ<sub>4,v</sub> = AUC<sub>4;E<sub>4,v</sub></sub> − AUC<sub>v;E<sub>4,v</sub></sub>,     v ∈ {1,2,3,mean,max}',
                 r'\Delta_{4,v}=\widehat{\mathrm{AUC}}_{4;E_{4,v}}-\widehat{\mathrm{AUC}}_{v;E_{4,v}},\quad v\in\{1,2,3,\mathrm{mean},\mathrm{max}\}'),
        'Percentiles 2.5/97.5 form family-bootstrap intervals. Gray family dots are descriptive, not the estimand in Equation 10. Rate intervals are exact Clopper-Pearson with an episode-independence caveat. Undefined quantities and method-specific exclusions remain explicit. No deployment-level FPR, equivalence from nonsignificance, or multiplicity-adjusted significance claim is made. Rounds are not independent samples.'
    ]
    original_result = sections['4 Results']
    attempt_rows = [['Method','N','Attempt AUROC [95%]','TPR [exact 95%]','FPR [exact 95%]']]
    for name in ['V1','V2','V3','V4','mean','max']:
        r = metrics['attempt_detection']['views'][name]
        attempt_rows.append([name,str(r['n']),n(r['AUROC'])+' '+ci(r['AUROC_family_interval']),
                             n(r['TPR'])+' '+ci(r['TPR_interval']),n(r['FPR'])+' '+ci(r['FPR_interval'])])
    results = [
        heading('4.1 Generation coverage and outcome validity'),
        'The held-out schedule contains 48/48 collected and technically valid episodes. Table 4 reports generation outcomes, Table 5 and Figure 2 report primary held-out performance, and Table 6 and Figure 3 report condition-level alarms and paired contrasts. All thresholds remain frozen. Failed scientific controls are retained; no post-test prompt tuning or outcome-driven replacement occurred.',
        original_result[3],
        f'All four views have {metrics["views"]["V4"]["n"]} eligible held-out scores. Under automatic labels there are {metrics["views"]["V4"]["positives"]} implementation positives and {metrics["views"]["V4"]["negatives"]} negatives. The three H gate failures remain included; no outcome-driven replacement was performed.',
        table('Table 4. Held-out outcome counts by assigned condition. Agreement means unauthorized agreement; columns need not be nested.', generation_rows, [64]+[63]*7),
        heading('4.2 Primary implemented collusion detection'), original_result[1], original_result[2],
        table('Table 5. Implemented-collusion detection on held-out episodes. AUROC intervals resample families; rate intervals are episode-binomial.', primary_rows,[60,25,140,140,140]),
        figure('auroc','Figure 2. Held-out implementation AUROC with 95% family-bootstrap intervals. The dashed reference denotes chance ranking, not a significance test.'),
        heading('4.3 Hard negatives and paired contrasts'),
        'Independent deception is a critical hard negative: at the frozen threshold, V4 flags 4/8 I episodes and V3 flags 7/8. B/G produce no implementation alarms for any view. V1 flags 1/8 talk-only episodes, while views containing actions flag none. H mixes five operational positives and three gate failures, so its flagged count is not recall.',
        table('Table 6. Flagged / eligible cases at frozen thresholds by assigned condition, irrespective of automatic outcome labels.', flag_rows,[61]+[74]*6),
        figure('paired-differences','Figure 3. Paired V4-minus-comparator AUROC with 95% family-bootstrap intervals and descriptive family dots. All contrasts use common eligible records. These exploratory intervals do not establish universal superiority or equivalence.'),
        heading('4.4 Attempt detection differs from implemented harm'),
        f'Unauthorized agreement has {metrics["attempt_detection"]["views"]["V1"]["positives"]} positive and {metrics["attempt_detection"]["views"]["V1"]["negatives"]} negative held-out labels. V1 attempt AUROC is {n(metrics["attempt_detection"]["views"]["V1"]["AUROC"])}, versus implementation AUROC {n(metrics["views"]["V1"]["AUROC"])}; V2 has {n(metrics["attempt_detection"]["views"]["V2"]["AUROC"])} versus {n(metrics["views"]["V2"]["AUROC"])}. The different targets explain why evidence of a plan must not be scored as proof of execution. They are not treatment-effect comparisons.',
        table('Table 7. Secondary unauthorized-agreement detection. Its operating thresholds are calibrated separately from implementation.',attempt_rows,[60,25,140,140,140]),
        'Figure 4 in Appendix F visualizes the target comparison. Its positive sets differ; the plotted separation is not a causal effect.',
        'Appendix D shows the earliest available held-out H/I/T first-round traces, chosen by schedule rather than favorable scores. Oracle event references appear only in the ground-truth explanation, never monitor inputs.'
    ]
    discussion = [heading('5.1 Evidence and interpretation')] + sections['5 Discussion and Limitations'][:1] + [
        heading('5.2 Limitations and scope')] + sections['5 Discussion and Limitations'][1:2] + [
        'The I/H public module, receipt-only negative channel and T execution controller are deliberate interventions. Requirements R1-R5 make the comparison inspectable but do not validate latent intent, generalize to unconstrained agents, or replace independent human annotation. Prior-paper audit corrections guide our implementation; missing original artifacts remain unavailable. We do not infer a general benefit from giving a monitor more context.',
        heading('5.3 Future work')] + sections['5 Discussion and Limitations'][2:]
    appendix = list(appendix) + [('Appendix E Verification of the Audit Requirements', [
        'R1: sentinel view tests verify nonempty distinct projections and absence of private/oracle fields; public-module isolation is tested separately. R2: explicit view indexes and common samples produce 48/48 scores per held-out view. R3: stored payoff and label arithmetic reproduce for all 60 episodes; semantic agreement/pair adjudication is still pending.',
        'R4: rejection, bounded repair and invalid-output handling are tested; no model failure is imputed as contribution/score zero. R5: original experiment hashes and cloud source/model provenance match; exported records exactly replay the saved metrics, including bootstrap values. The project has 23 passing component/delivery tests. These are computational checks, not a human-reviewed gold standard.',
        'The complete notation sheet FORMULAS.md, audit-to-implementation map, frozen configuration and code accompany the local package. The presentation adopts explicit definitions and checkable requirements, as in the author-provided PrefKit reference; no PrefKit experiment, CMS value, preference outcome, or coauthor identity is transferred into this study.'
    ]), ('Appendix F Attempt and Implementation Comparison', [
        figure('attempts','Figure 4. Attempt and implementation AUROC with separate family-bootstrap intervals. The targets have different positive sets; visual separation is not a causal effect.')
    ])]
    revised = [('1 Introduction',intro), ('2 Related Work',sections['2 Related Work']), ('3 Methods',methods),
               ('4 Results',results), ('5 Discussion and Limitations',discussion),
               ('6 Conclusion',sections['6 Conclusion']), ('Code and Data',sections['Code and Data'])]
    return revised, appendix
