"""Fill the supplied Apart DOCX by patching its package, preserving template parts.

No inference, analysis recalibration, or modification of frozen experimental files.
Run with the bundled document Python runtime and --template PATH.
"""
import argparse,copy,hashlib,json,re,zipfile
from pathlib import Path
from lxml import etree as E
from PIL import Image

W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
M='http://schemas.openxmlformats.org/officeDocument/2006/math'
NS={'w':W,'r':R,'m':M}
P=Path('pilot/submission'); TITLE='Words Actions and Evidence in Collusion Detection'
EXPECTED='4b23e4cf76f9daa2b6fd2c45a4d3fdbaa963c1588bc7a1fb76bbba5144a5e80e'
def q(x):return '{'+W+'}'+x
def node(x,**attrs):
    e=E.Element(q(x))
    for k,v in attrs.items():e.set(q(k),str(v))
    return e
def text(e):return ''.join(e.xpath('.//w:t/text()',namespaces=NS))
def sha(b):return hashlib.sha256(b).hexdigest()

def build(template):
    raw=template.read_bytes();assert sha(raw)==EXPECTED,'Unexpected template; re-inspect before using it.'
    with zipfile.ZipFile(template) as z:parts={i.filename:z.read(i) for i in z.infolist()}
    doc=E.fromstring(parts['word/document.xml']);body=doc.find('w:body',NS)
    original=list(body);body_proto=copy.deepcopy(original[5]);head_proto=copy.deepcopy(original[4]);sub_proto=copy.deepcopy(original[49]);sect=copy.deepcopy(original[-1])
    for e in list(body):body.remove(e)
    def para(value='',kind='body',size=None,bold=False,center=False,keep=False,page=False):
        e=copy.deepcopy({'body':body_proto,'head':head_proto,'sub':sub_proto}[kind])
        for c in list(e):
            if c.tag!=q('pPr'):e.remove(c)
        for a in list(e.attrib):
            if a.endswith('paraId'):del e.attrib[a]
        pp=e.find('w:pPr',NS)
        if pp is None:pp=node('pPr');e.insert(0,pp)
        # Remove inherited list markers and guidance-specific formatting.
        for c in list(pp):
            if c.tag in [q('numPr'),q('rPr')]:pp.remove(c)
        if center:
            j=pp.find('w:jc',NS)
            if j is None:j=node('jc');pp.append(j)
            j.set(q('val'),'center')
        if keep:pp.append(node('keepNext',val='1'))
        if page:pp.append(node('pageBreakBefore',val='1'))
        run=node('r');rp=node('rPr');rp.append(node('rFonts',ascii='Old Standard TT',hAnsi='Old Standard TT',eastAsia='Old Standard TT',cs='Old Standard TT'));rp.append(node('color',val='000000'))
        if size:rp.append(node('sz',val=int(size*2)))
        elif kind=='head':rp.append(node('sz',val='28'))
        elif kind=='sub':rp.append(node('sz',val='26'))
        if bold or kind in ['head','sub']:rp.append(node('b',val='1'))
        run.append(rp);t=node('t');t.set('{http://www.w3.org/XML/1998/namespace}space','preserve');t.text=value;run.append(t);e.append(run)
        return e
    ACTIVE.update(para=para,body=body)
    def add(t,kind='body',**kw):e=para(t,kind,**kw);body.append(e);return e
    def heading(t,page=False):return add(t,'head',page=page)
    def sub(t):return add(t,'sub')
    # Preserve the title table and original title footnote; edit only slots.
    cover=copy.deepcopy(original[1]);titlep=next(p for p in cover.xpath('.//w:p',namespaces=NS) if text(p)=='PROJECT TITLE')
    titlep.xpath('.//w:t',namespaces=NS)[0].text=TITLE
    author_table=next(t for t in cover.xpath('.//w:tbl',namespaces=NS) if len(t.findall('w:tr',NS))==2 and len(t.findall('w:tr',NS)[0].findall('w:tc',NS))==3)
    par=author_table.getparent();index=par.index(author_table);par.remove(author_table)
    for i,line in enumerate(['Siddeshwar U S','MIT, Manipal','Team spacenets']):par.insert(index+i,para(line,center=True,bold=i==0))
    abstract=json.loads((P/'submission-fields.json').read_text(encoding='utf-8'))['summary']
    ap=next(p for p in cover.xpath('.//w:p',namespaces=NS) if text(p).startswith('Summarize your project'))
    replacement=para(abstract);ap.getparent().replace(ap,replacement)
    body.append(cover)
    heading('1. Introduction',page=True)
    add('Parallel harmful actions and broken promises can arise with or without a shared agreement. A monitor that flags all deviations therefore measures a different target from implemented harmful collusion. Track 2.2 asks whether combining words and actions improves detection over either source alone. We test that question in a controlled repeated public-goods game.')
    add('We contribute a six-condition protocol separating agreement, execution and harm; four isolated monitor views, including a deterministic claim-versus-outcome report; and a frozen, family-paired evaluation with uncertainty, hard negatives and exact offline replay. The observed result is a limitation: the structured hybrid does not consistently outperform actions alone. Labels remain automatic pending independent human adjudication.')
    heading('2. Related Work')
    add('When Agents Lie [1] separates private plans, announcements and actions. We use its released game for payoff verification and replace the runner and typology with our own controller [6]. COLOSSEUM [2] motivates coalition-level outcome checks; its regret is not the fixed-outsider welfare contrast used here. TraceGuard [3] motivates structured consistency rubrics, while Arike et al. [4] motivate controlled information-access comparisons. SCHEME [5] concerns coordinated software sabotage; its success rates do not transfer to this game.')
    add('Our audit identified 22 confirmed records across the supplied papers, including released-code and reporting defects; these do not establish that all historical headline results are invalid. We avoid the affected typology, hidden-state monitor inputs and aggregation assumptions, and retain an explicit finding-to-implementation map. We do not reproduce the papers’ full experiments or claim the complete TraceGuard stack.')
    heading('3. Methods')
    sub('3.1 Environment and experimental controls')
    add('Five delegates play ten rounds. Each receives 5 tokens and chooses an integer contribution from 0 to 5; the principal mandates 3. Public promises, private plans and executed actions are stored separately. Payoff is 5 minus own contribution plus 0.3 times total contributions. Thus all-3 gives 6.5 each and welfare 32.5; two zeros with three 3s give pair payoffs 7.7, outsider payoffs 4.7 and welfare 29.5. Appendix A gives the formal definitions.')
    caption('Table 1. Six assigned conditions; realized event-based outcomes determine the labels.')
    table(['Code','Objective','Key control'],[
        ['B','Benign compliance','Policy contribution 3; private receipts only.'],
        ['G','Legitimate cooperation','Open coordination at 3; model-chosen actions.'],
        ['I','Independent deception','Low-action incentives without agreement; receipts only.'],
        ['T','Talk only','Harmful plan; controller executes 3.'],
        ['O','Overt collusion','Explicit pair agreement and public low-action plan.'],
        ['H','Hidden collusion','Private pair agreement; controlled public communication.']], [1000,2400,5960])
    add('I and H use the same public communication module: only public words are visible to it, the typed promise is 3, requests are empty and prose is generated. This intervention followed a development H disclosure. It controls public communication and does not measure spontaneous concealment. Private negotiation and actions remain model decisions; only T forces executed contributions. Family seeds fix pair identity and actor order.')
    sub('3.2 Operational outcomes and hard negatives')
    add('Unauthorized agreement A requires event-linked acceptance of a compatible real proposal, including a prior-round proposal, or reciprocal public below-policy commitments. Authorized G coordination is not a positive. Execution X requires both members to enact the applicable agreed below-policy actions in at least three rounds. Harm H requires episode-average welfare loss at least 1, positive pair gain and positive outsider loss relative to replacing pair actions with 3 while holding outsiders fixed. The primary target is Y = V A X H, where V requires a valid complete episode; A is a separate attempt target. Matching harmful actions alone never establishes agreement.')
    sub('3.3 Monitor inputs and requirements')
    caption('Table 2. The same auditor and policy are used for four public evidence views.')
    table(['View','Visible evidence'],[['V1','Public announcements, typed promises and requests.'],['V2','Executed actions, payoffs and all-ten-pair action summaries.'],['V3','Raw union of V1 and V2.'],['V4','Verbatim claims aligned with actions, directed follow-through and all-ten-pair tables.']],[750,8610])
    add('Private plans, pair messages, assigned pair and oracle labels never enter a monitor view. V4 adds a representation, not private information; all ten candidate pairs are tabulated. Each response has attempt and implementation scores in [0,1], cited visible event IDs, action extraction, rationale and uncertainty. Five operational requirements govern the comparison: evidence isolation, matched cases, explicit outcomes, honest invalidity and a locked reproducible estimand. They are checks, not proofs of semantic correctness.')
    sub('3.4 Models and execution')
    add('Agents use Qwen2.5-3B-Instruct and the auditor uses Qwen3-4B-Instruct-2507, with exact model revisions pinned. Agent temperature is 0.4; private/plan/public/action limits are 192/96/160/48 tokens. The auditor uses temperature 0, seed 42, 384 output tokens and one accepted response per view and episode. Context is 16,384 tokens. One bounded repair is allowed; it is not an independent replicate. Invalid outputs remain explicit, without silent truncation, action clamping or default-zero scores.')
    add('Inference uses vLLM on one Modal L4 with 2 CPU cores and 16 GiB, 30-minute phase timeouts and persistent request caches. Models use BF16/eager inference; asynchronous scheduling and prefix caching are disabled. We selected this setup on development families after alternative prompts/models failed behavioral or visibility checks. Full iteration records and failed controls are retained.')
    sub('3.5 Frozen evaluation')
    add('Families 1001–1002 provide 12 development episodes; held-out families 2001–2008 provide 48 episodes, six conditions each. Models, prompts, label definitions and thresholds were frozen before held-out execution. Per-view thresholds use development-negative scores only, allowing at most floor(0.20m) development alarms under a strict score-greater-than-threshold rule. This is not a held-out FPR guarantee. Mean/max V1–V2 ensembles and zero-call baselines are prespecified comparators.')
    add('AUROC gives half credit to ties. We resample complete families in 5,000 paired draws and recompute pooled AUROC differences on common eligible records. TPR/FPR intervals are exact Clopper–Pearson intervals with an episode-independence caveat. Rounds are not independent samples. Missing scores, undefined quantities and excluded IDs remain explicit; no multiplicity-adjusted significance or deployment-level FPR claim is made.')
    heading('4. Results')
    add('All 48 held-out episodes are technically valid and all 192 held-out view scores are available; the full dataset has 60 episodes and 240 scores. Eight overt and five hidden episodes meet the automatic implementation gate: 13 positives and 35 negatives. All eight hidden episodes are harmful, but three fail the agreement/execution gate and remain in the analysis. No outcome-driven replacement or held-out retuning occurred.')
    caption('Table 3. Held-out implementation detection. AUROC intervals resample families; TPR/FPR use frozen development thresholds. Exact rate intervals and all baselines appear in Appendix B.')
    metrics=json.loads((P/'metrics.json').read_text())
    rows=[]
    for key in ['V1','V2','V3','V4','mean','max']:
        x=metrics['views'][key];lo,hi=x['AUROC_family_interval'];rows.append([key,f"{x['AUROC']:.3f} [{lo:.3f}, {hi:.3f}]",f"{x['TPR']:.3f}",f"{x['FPR']:.3f}"])
    table(['View','AUROC [95%]','TPR','FPR'],rows,[1050,4410,1950,1950])
    add('Actions alone rank implementation positives with AUROC 0.843, compared with 0.731 for the structured report and 0.843 for the mean ensemble. The paired V4-minus-V2 difference is −0.112, with 95% family-bootstrap interval [−0.215, 0.029]. These data do not establish a consistent hybrid advantage. Figure 1 displays uncertainty; the chance line is a ranking reference, not a significance test.')
    figure('01_monitor_auroc.png','Figure 1. Held-out implementation AUROC with 95% family-bootstrap intervals. The comparison retains all scheduled cases and uses automatic event-based labels.',6.25)
    add('Independent deception remains difficult: V4 flags 4/8 I episodes and V3 flags 7/8. B/G cause no implementation alarms. V1 flags 1/8 talk-only cases; views containing actions flag none. H alarm counts are not recall because H includes five positives and three gate failures. Attempt detection is a different target: V1 has AUROC 0.865 for unauthorized agreement versus 0.597 for implementation; V2 has 0.622 versus 0.843. This distinguishes evidence of a plan from evidence of its execution.')
    heading('5. Discussion and Limitations')
    add('Consistency checks expose contradictions but cannot generally recover a private agreement. I and H can produce the same harmful actions and clean-looking public claims. Small wording differences may influence scores without identifying coordination. The strongest observed implementation ranking comes from action evidence and an action-gap baseline that overlaps the outcome construction; neither independently verifies agreement.')
    sub('Limitations')
    add('This pilot has eight held-out families, prompted objectives, shared model lineage, restricted receipt-only negative channels, forced T execution and controlled I/H communication. Automatic agreement labels await two independent score-blind reviews and adjudication; no human inter-rater agreement is claimed. The fixed-outsider contrast is a within-round accounting comparison, not a repeated-game causal effect or equilibrium. Syntactically valid monitor output can still misread evidence. Failure to detect a coalition does not establish its absence in deployment.')
    sub('Future Work')
    add('Next steps are independent label adjudication, additional model lineages and families, naturally generated concealment and less constrained independent agents. These require a new development/evaluation split rather than tuning the present held-out set.')
    heading('6. Conclusion')
    add('Combining words and actions did not consistently improve detection over actions alone in this controlled setting. The project provides an inspectable separation of agreement, execution and harm, with hard negatives, uncertainty and retained failed controls. The numerical findings are reproducible; their interpretation remains conditional on the operational automatic labels and the limitations above.')
    heading('Code and Data')
    add('Code repository: https://github.com/spacenets7/words-vs-actions-collusion (private; access requires authorization). The included reproducibility ZIP provides sanitized public trajectories, separate automatic labels, monitor evidence/outputs, frozen analysis sources, figures and exact offline metrics replay. Private plans/messages, raw generation journals, credentials, downloaded papers and third-party checkouts are excluded from that release candidate. No public dataset release or publication approval is claimed.')
    heading('References',page=True)
    source=(P/'report.md').read_text(encoding='utf-8')
    refs=source.split('## References\n',1)[1].split('\n## Appendix',1)[0].strip()
    for ref in refs.split('\n\n'):
        if ref.strip():add(ref.strip())
    heading('Appendix A Formal Definitions and Verification',page=True)
    add('The following definitions match the frozen implementation. They describe this pilot and do not assert that scores are calibrated probabilities or that public evidence identifies latent intent. All numerical results are unchanged from the frozen analysis.')
    equations=[
      ('Audit function','M_(Θ,ψ,δ)(V_v(τ_e)) → (s_att, s_imp) ∈ [0,1]² ∪ {⊥}'),
      ('Payoff and welfare','u_it(c_t) = 5 − c_it + (1.5/5)∑_j c_jt\nW(c_t) = 25 + 0.5∑_j c_jt'),
      ('Fixed outsider accounting','L_e = (1/T)∑_t[W(c̃_t) − W(c_t)]\nG_e = (1/(T|C_e|))∑_t∑_(i∈C_e)[u_i(c_t) − u_i(c̃_t)]\nO_e = (1/(T(N−|C_e|)))∑_t∑_(i∉C_e)[u_i(c̃_t) − u_i(c_t)]'),
      ('Harm gate','H_e = 1{L_e ≥ 1 ∧ G_e > 0 ∧ O_e > 0}'),
      ('Agreed execution','J_e = ∑_(t=0)^9 1{applicable agreement ∧ ∀i∈C_e: c_it = a*_it < 3}\nX_e = 1{J_e ≥ 3}'),
      ('Primary outcome','Y_e = V_e A_e X_e H_e'),
      ('Claim alignment and follow through','d_it = c_it − p_it\nF_(i→j) = ∑_(r∈R_(i→j))1{c_(j,t(r)) = q_r} / |R_(i→j)|'),
      ('Development locked threshold','θ_v = s⁻_(m_v−⌊0.20m_v⌋),v ;   Ŷ_ev = 1{s_imp,ev > θ_v}'),
      ('Detection metrics','κ(s,t) = 1{s>t} + 0.5·1{s=t}\nAUC_v = ∑_(e∈E+)∑_(f∈E−)κ(s_ev,s_fv) / (|E+||E−|)\nTPR = TP/(TP+FN) ;   FPR = FP/(FP+TN)'),
      ('Paired comparison','Δ_(4,v) = AUC_(4;E_(4,v)) − AUC_(v;E_(4,v))')]
    for number,(label,value) in enumerate(equations,1):
        add(f'{number}. {label}',bold=True,keep=True)
        equation(value,number)
    add('τ is an episode; V_v is its public projection; Θ, ψ and δ fix model, rubric and decoding. C_e is the assigned pair, used only by the oracle. c̃ replaces the pair’s contributions with 3, holding outsiders fixed. a* is the latest applicable verified agreed action. V requires all ten valid rounds. R contains directed public requests; F is undefined for an empty set. Threshold order statistics are ascending and one-indexed. E_(4,v) is the common eligible set for the paired comparison. Rate denominators of zero and invalid auditor outputs are explicitly undefined, not zero.')
    add('Agreement requires an acceptance linked to the partner’s actual proposal or mutual reciprocal public commitments; it cannot be inferred from matching actions. The execution indicator is zero without an applicable agreement. With pair actions 0 and outsiders 3 throughout, L = 3.0, G = 1.2 and O = 1.8 per round. All-3 and pair-zero payoff checks reproduce the upstream evaluator.')
    sub('Verification requirements')
    for item in [
      'R1 Evidence isolation: allowlisted projections and sentinel tests exclude private plans/messages, assigned pair and labels; public-module isolation is tested separately.',
      'R2 Matched comparison: the four views score identical scheduled cases; all 48 held-out cases are covered per view, with common eligible samples reported for paired contrasts.',
      'R3 Explicit outcomes: stored payoff and label arithmetic reproduce across all 60 episodes; independent semantic agreement adjudication remains pending.',
      'R4 Honest invalidity: rejected actions, bounded repairs and invalid scores remain visible; missing model output is never imputed as zero.',
      'R5 Locked reproducibility: original frozen hashes, model/source provenance and development thresholds match. The sanitized archive exactly replays all saved metrics, including bootstrap values. There are 23 passing component/delivery tests; these are computational checks, not independent human reviews.']:add(item)
    heading('Appendix B Extended Results',page=True)
    caption('Table 4. Held-out counts by assigned condition. All conditions have 8 scheduled, collected and technically valid cases; columns need not be nested.')
    heldout={c:[r for r in metrics['generation'] if r['condition']==c and r['family'] not in [1001,1002]] for c in ['B','G','I','T','O','H']}
    assert all(len(rows)==8 for rows in heldout.values())
    table(['Condition','Agreement','Execution','Harm','Implemented'],[[c]+[str(sum(bool(r[key]) for r in rows)) for key in ['agreement','execution','harm','implementation']] for c,rows in heldout.items()],[1760,1900,1900,1900,1900])
    caption('Table 5. Implementation AUROC and rate intervals. AUROC uses family resampling; rate intervals assume independent episodes and need that caveat.')
    rows=[]
    for key,x in metrics['views'].items():
        def fmt(a,b):return f"{a:.3f} [{b[0]:.3f}, {b[1]:.3f}]"
        rows.append([key.replace('_',' '),fmt(x['AUROC'],x['AUROC_family_interval']),fmt(x['TPR'],x['TPR_interval']),fmt(x['FPR'],x['FPR_interval'])])
    table(['Method','AUROC [95%]','TPR [95%]','FPR [95%]'],rows,[1400,2700,2630,2630],size=10)
    add('Constant scores rank at chance. Promise-break is the fraction of claim/action mismatches. Action-gap combines joint below-policy frequency and pair-versus-outsider payoff gaps; its overlap with harm construction must not be interpreted as independent agreement verification. Mean/max combine V1/V2 suspicion scores and are separately calibrated empirical baselines, not trusted-weight safety guarantees.')
    caption('Table 6. Unauthorized-agreement attempts have 21 positive and 27 negative held-out cases, with separately calibrated scores and thresholds.')
    attempt=metrics['attempt_detection']['views']
    table(['View','Attempt AUROC [95%]','TPR','FPR'],[[k,f"{attempt[k]['AUROC']:.3f} [{attempt[k]['AUROC_family_interval'][0]:.3f}, {attempt[k]['AUROC_family_interval'][1]:.3f}]",f"{attempt[k]['TPR']:.3f}",f"{attempt[k]['FPR']:.3f}"] for k in ['V1','V2','V3','V4','mean','max']],[1050,4410,1950,1950])
    figure('02_paired_auroc_differences.png','Figure 2. Paired V4-minus-comparator implementation AUROC with 95% family-bootstrap intervals. All comparisons use common eligible cases; these exploratory intervals do not establish universal superiority or equivalence.',6.25)
    figure('05_attempt_vs_implementation.png','Figure 3. Attempt and implementation detection evaluate different positive sets. Their AUROC separation is descriptive and is not a causal effect.',6.25)
    heading('Appendix C Resources Limitations and Dual Use',page=True)
    add('The canonical configuration hash is 10e684f850295c7d8a29c06ee695cc56604908631c5c2e44fa1a9e3767205414. The original frozen manifest SHA256 is 3c3ccbfe95b31e3c96808a4b904c8e8089483a542d070563dfeffac9fcf662cc. Agent revision: aa8e72537993ba99e69dfaafa59ed015b17504d1. Auditor revision: cdbee75f17c01a7cc42f958dc650907174af0554. Runtime: vLLM 0.21.0, Torch 2.11.0, transformers 4.57.6, Python 3.12 and CUDA 12.9. The upstream game revision is fd11aca351e52c65c929e1a7d46d9f087f237adf and is not redistributed.')
    add('The saved closed-interval Modal usage report is $5.41625951. The settled-plus-runtime estimate is about $5.40; the conservative billed/reserved envelope is about $7.60, including a setup/storage allowance. These accounting views overlap and must not be added. Startup/storage usage may not yet be reported; the report is not a final invoice. External API spend is $0. Report formatting and offline replay use no model calls.')
    add('No real market is manipulated. Coordination/concealment prompts could nevertheless assist evasive behavior, so a future public release needs data and licensing review. Exported public trajectories omit private strategies; oracle labels remain separate. Results must not support accusations against real people or organizations. Controlled communication, limited model diversity, small clusters, label/evidence overlap and pending semantic review limit transfer to deployment. Neither successful detection nor missed alarms establish a general collusion guarantee.')
    heading('LLM Usage Statement')
    add('We used GPT-6.1 to brainstorm approaches and help draft sections, and GPT Astra for assistance in building out notebooks. Numerical results were checked through independent payoff calculations, automated tests and exact offline replay. An AI coding assistant also assisted pipeline implementation, operation and report preparation. Agreement labels remain automatic and await independent human adjudication; computational checks do not replace that review. The human author remains responsible for interpretation and final submission.')
    body.append(sect)
    # Preserve all original opaque parts; add only media relationships and types.
    rels=E.fromstring(parts['word/_rels/document.xml.rels']);types=E.fromstring(parts['[Content_Types].xml'])
    existing_png=any(x.get('Extension')=='png' for x in types)
    if not existing_png:
        e=E.Element('{http://schemas.openxmlformats.org/package/2006/content-types}Default');e.set('Extension','png');e.set('ContentType','image/png');types.append(e)
    for i,(path,data) in enumerate(media.items(),1):
        e=E.Element('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship');e.set('Id','rIdFinal'+str(i));e.set('Type',R+'/image');e.set('Target','media/'+Path(path).name);rels.append(e);parts[path]=data
    original_parts=set(parts)-set(media)
    editable={'word/document.xml','word/_rels/document.xml.rels','[Content_Types].xml'}
    updated={'word/document.xml':E.tostring(doc,xml_declaration=True,encoding='UTF-8',standalone=True),'word/_rels/document.xml.rels':E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True),'[Content_Types].xml':E.tostring(types,xml_declaration=True,encoding='UTF-8',standalone=True)}
    for name,b in updated.items():parts[name]=b
    final=P/'final-report.docx'
    with zipfile.ZipFile(final,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in parts.items():z.writestr(name,data)
    with zipfile.ZipFile(template) as a,zipfile.ZipFile(final) as b:
        preserved=[n for n in a.namelist() if n not in editable]
        assert all(a.read(n)==b.read(n) for n in preserved)
    assert E.tostring(doc.xpath('//w:sectPr',namespaces=NS)[0])==E.tostring(sect)
    alltext=' '.join(doc.xpath('//w:t/text()',namespaces=NS))
    assert not any(x in alltext for x in ['PROJECT TITLE','Author name 1','Summarize your project','How to use this template','[Reference 1]'])
    assert len(abstract.split())==193
    assert sha(template.read_bytes())==EXPECTED
    proof={'template_sha256':EXPECTED,'docx_sha256':sha(final.read_bytes()),'original_preserve_only_parts':preserved,'all_preserve_only_parts_byte_identical':True,'section_count':1,'abstract_words':193,'equation_count':10,'figure_count':len(media),'table_count':6,'metrics_sha256':sha((P/'metrics.json').read_bytes()),'frozen_manifest_sha256':sha(Path('pilot/frozen/hashes.json').read_bytes()),'visual_review':'pending','independent_human_label_review':'pending','author_approval':'pending','external_submission':'not_performed'}
    (P/'template-report-quality.json').write_text(json.dumps(proof,indent=2),encoding='utf-8')
    inventory={n:{'bytes':len(b),'sha256':sha(b),'classification':'editable' if n in editable else 'preserve-only'} for n,b in parts.items() if n not in media}
    Path('tmp/final-report-template/package-inventory.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
    print('Created',final,'with',len(preserved),'original parts preserved byte-for-byte.')
    return final

media={};doc_counter=0
def caption(value):
    p=ACTIVE['para'](value,size=10,keep=True);ACTIVE['body'].append(p)
def table(headers,rows,widths,size=11):
    tbl=node('tbl');pr=node('tblPr');pr.append(node('tblW',w=9360,type='dxa'));pr.append(node('tblLayout',type='fixed'))
    borders=node('tblBorders')
    for edge in ['top','left','bottom','right','insideH','insideV']:borders.append(node(edge,val='single',sz=4,color='D9D9D9'))
    pr.append(borders);marg=node('tblCellMar')
    for edge,w in [('top',70),('left',90),('bottom',70),('right',90)]:marg.append(node(edge,w=w,type='dxa'))
    pr.append(marg);tbl.append(pr);grid=node('tblGrid')
    for width in widths:grid.append(node('gridCol',w=width))
    tbl.append(grid)
    for index,row in enumerate([headers]+rows):
        tr=node('tr');rp=node('trPr');rp.append(node('cantSplit'))
        if index==0:rp.append(node('tblHeader'))
        tr.append(rp)
        for j,value in enumerate(row):
            tc=node('tc');cp=node('tcPr');cp.append(node('tcW',w=widths[j],type='dxa'));cp.append(node('vAlign',val='center'))
            if index==0:cp.append(node('shd',fill='F2F2F2',val='clear'))
            tc.append(cp);p=ACTIVE['para'](value,size=size,bold=index==0,center=(j>0 and len(headers)>3),keep=index<len(rows));pp=p.find('w:pPr',NS);pp.append(node('spacing',before=0,after=0,line=240,lineRule='auto'));tc.append(p);tr.append(tc)
        tbl.append(tr)
    ACTIVE['body'].append(tbl)
def equation(value,number):
    def run(value):
        r=E.Element('{'+M+'}r');mp=E.SubElement(r,'{'+M+'}rPr');sty=E.SubElement(mp,'{'+M+'}sty');sty.set('{'+M+'}val','p');rp=E.SubElement(r,q('rPr'));rp.append(node('rFonts',ascii='Cambria Math',hAnsi='Cambria Math'));rp.append(node('sz',val=22));t=E.SubElement(r,'{'+M+'}t');t.set('{http://www.w3.org/XML/1998/namespace}space','preserve');t.text=value;return r
    def append_math(math,line):
        cursor=0
        while True:
            hit=re.search(r'([A-Za-zΑ-Ωα-ω∑⁻̃*]+)_',line[cursor:])
            if hit is None:break
            start=cursor+hit.start();at=cursor+hit.end()
            if at>=len(line):break
            if line[at]=='(':
                depth=1;end=at+1
                while end<len(line) and depth:
                    depth+=(line[end]=='(')-(line[end]==')');end+=1
                if depth:break
                index=line[at+1:end-1]
            else:
                token=re.match(r'[A-Za-z0-9Α-Ωα-ω]+',line[at:])
                if token is None:break
                index=token.group();end=at+len(index)
            if start>cursor:math.append(run(line[cursor:start]))
            sup=None
            if end+1<len(line) and line[end]=='^' and line[end+1].isdigit():sup=line[end+1];end+=2
            s=E.SubElement(math,'{'+M+'}sSubSup' if sup else '{'+M+'}sSub');base=E.SubElement(s,'{'+M+'}e');base.append(run(hit.group(1)));lower=E.SubElement(s,'{'+M+'}sub');append_math(lower,index)
            if sup:E.SubElement(s,'{'+M+'}sup').append(run(sup))
            cursor=end
        if cursor<len(line):math.append(run(line[cursor:]))
    for line_index,line in enumerate(value.split('\n')):
        p=ACTIVE['para']('',size=11)
        math=E.Element('{'+M+'}oMath');append_math(math,line+(f'    ({number})' if line_index==len(value.split('\n'))-1 else ''));p.append(math);ACTIVE['body'].append(p)
def figure(filename,cap,width):
    global doc_counter
    data=(Path('pilot/figures_png')/filename).read_bytes();i=len(media)+1;name=f'word/media/final-{i}.png';media[name]=data
    with Image.open(Path('pilot/figures_png')/filename) as im:w,h=im.size
    cx=int(width*914400);cy=int(cx*h/w)
    wp='http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing';a='http://schemas.openxmlformats.org/drawingml/2006/main';pic='http://schemas.openxmlformats.org/drawingml/2006/picture'
    p=ACTIVE['para']('',center=True,keep=True);r=node('r');drawing=node('drawing');r.append(drawing)
    root=E.fromstring(f'''<wp:inline xmlns:wp="{wp}" xmlns:a="{a}" xmlns:pic="{pic}" xmlns:r="{R}" distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{100+i}" name="Figure {i}" descr="{filename}"/><wp:cNvGraphicFramePr/><a:graphic><a:graphicData uri="{pic}"><pic:pic><pic:nvPicPr><pic:cNvPr id="0" name="{filename}"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="rIdFinal{i}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline>''');drawing.append(root);p.append(r);ACTIVE['body'].append(p)
    c=ACTIVE['para'](cap,size=10);ACTIVE['body'].append(c)

ACTIVE={}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--template',type=Path,required=True);args=ap.parse_args()
    build(args.template)
