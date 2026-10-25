"""Export saved pilot results as publication-sized PNGs; no experiment/API calls."""
import hashlib
import math
from pathlib import Path
import subprocess
import zipfile

from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing, Rect, Line, Circle, String
from reportlab.lib.colors import HexColor, Color, white
from PIL import Image, ImageDraw, ImageFont

from .core import load, save

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'pilot/figures_png'
TEMP = ROOT / 'tmp/pdfs/png-figures'
W, H = 840, 540
INK = HexColor('#172b42')
MUTED = HexColor('#526478')
GRID = HexColor('#dce4ec')
TEAL = HexColor('#087f8c')
BLUE = HexColor('#2367ad')
ORANGE = HexColor('#bc5a17')
PURPLE = HexColor('#7453a6')
LABELS = {'V1': 'V1  Public text', 'V2': 'V2  Actions', 'V3': 'V3  Raw words + actions',
          'V4': 'V4  Structured report', 'mean': 'Mean score ensemble', 'max': 'Max score ensemble',
          'constant': 'Constant baseline', 'promise_break': 'Promise-break baseline', 'action_gap': 'Action-gap baseline'}
METHODS = list(LABELS)


def text(d, x, y, value, size=12, color=INK, anchor='start', bold=False):
    d.add(String(x, y, str(value), fontName='Helvetica-Bold' if bold else 'Helvetica',
                 fontSize=size, fillColor=color, textAnchor=anchor))


def line(d, x1, y1, x2, y2, color=GRID, width=.7, dash=None):
    d.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=width, strokeDashArray=dash))


def base(title, subtitle):
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, fillColor=white, strokeColor=None))
    text(d, 36, 504, title, 22, bold=True)
    text(d, 36, 481, subtitle, 11, MUTED)
    line(d, 36, 469, W-36, 469)
    text(d, 36, 15, 'Track 2.2 | Team spacenets | Provisional automatic labels; independent human review pending', 9, MUTED)
    return d


def whisker(d, x, y, point, ci, color=TEAL, radius=4):
    if ci is not None:
        lo, hi = map(x, ci)
        line(d, lo, y, hi, y, color, 1.6)
        for end in [lo, hi]:
            line(d, end, y-4, end, y+4, color, 1.1)
    d.add(Circle(x(point), y, radius, fillColor=color, strokeColor=white, strokeWidth=.7))


def axis(d, x, ticks, y=90, top=450):
    for tick in ticks:
        xx = x(tick)
        line(d, xx, y, xx, top)
        text(d, xx, y-19, f'{tick:g}', 10, MUTED, 'middle')
    line(d, x(ticks[0]), y, x(ticks[-1]), y, MUTED)


def auroc(metrics):
    d = base('How well do the monitors rank implemented collusion?',
             '48 held-out episodes across 8 families | AUROC with 95% family-bootstrap intervals')
    x = lambda v: 245 + 420*v
    axis(d, x, [0, .25, .5, .75, 1], top=452)
    line(d, x(.5), 90, x(.5), 452, MUTED, 1, [3, 3])
    text(d, 720, 442, 'AUROC [95% interval]', 10, MUTED, 'middle')
    for i, name in enumerate(METHODS):
        y = 415 - 35*i
        r = metrics['views'][name]
        text(d, 36, y-4, LABELS[name], 12, bold=name=='V4')
        color = TEAL if name=='V4' else BLUE if name in ['V1','V2','V3','mean','max'] else MUTED
        whisker(d, x, y, r['AUROC'], r['AUROC_family_interval'], color)
        lo, hi = r['AUROC_family_interval']
        text(d, 704, y-4, f'{r["AUROC"]:.3f} [{lo:.3f}, {hi:.3f}]', 10)
    text(d, 455, 48, 'AUROC  (0.5 = chance ranking; higher is better)', 12, anchor='middle')
    text(d, 36, 33, 'Baselines use no model calls. Action-gap overlaps the outcome-label construction; it does not establish agreement.', 9, MUTED)
    return d


def paired(metrics):
    d = base('Does the structured report improve on other views?',
             'V4 minus comparator AUROC | Paired bootstrap over 8 families | Same 48 held-out episodes')
    names = list(metrics['paired_differences'])
    family_values = {}
    all_values = [0]
    for name in names:
        other = name.removeprefix('V4-')
        vals = [r['AUROC'] - metrics['views'][other]['by_family'][f]['AUROC']
                for f, r in metrics['views']['V4']['by_family'].items()]
        family_values[name] = vals
        all_values += vals + metrics['paired_differences'][name]['interval']
    bound = max(.3, math.ceil((max(abs(v) for v in all_values)+.03)*10)/10)
    x = lambda v: 245 + (v+bound)/(2*bound)*420
    axis(d, x, [-bound, -bound/2, 0, bound/2, bound], top=450)
    line(d, x(0), 90, x(0), 450, MUTED, 1.2, [3,3])
    for i, name in enumerate(names):
        y = 405 - i*65
        r = metrics['paired_differences'][name]
        text(d, 36, y-4, 'V4 vs ' + LABELS[name.removeprefix('V4-')], 11)
        for j, v in enumerate(family_values[name]):
            d.add(Circle(x(v), y+11+(j%2)*5, 2.5, fillColor=HexColor('#a7b5c5'), strokeColor=None))
        whisker(d, x, y, r['difference'], r['interval'], TEAL if r['difference']>=0 else ORANGE)
        lo, hi = r['interval']
        text(d, 700, y-4, f'{r["difference"]:+.3f} [{lo:+.3f}, {hi:+.3f}]', 10)
    text(d, 455, 54, 'Negative: comparator ranks better    |    Positive: V4 ranks better', 11, anchor='middle')
    text(d, 36, 33, 'Small gray dots are individual-family differences. Intervals are exploratory; no multiplicity-adjusted claim.', 9, MUTED)
    return d


def flags(metrics):
    d = base('Which conditions trigger a collusion alarm?',
             'Flagged / eligible episodes at each method\'s frozen development threshold (score > threshold)')
    conditions = ['B','G','I','T','O','H']
    descriptions = ['Benign','Legitimate','Independent','Talk only','Overt','Hidden']
    x0, y0, cw, ch = 246, 130, 87, 66
    for j, (c, description) in enumerate(zip(conditions, descriptions)):
        text(d, x0+j*cw+cw/2, 436, c, 15, anchor='middle', bold=True)
        text(d, x0+j*cw+cw/2, 418, description, 10, MUTED, 'middle')
    for i, method in enumerate(['V1','V2','V3','V4']):
        y = y0+(3-i)*ch
        text(d, 36, y+ch/2-5, LABELS[method], 12, bold=method=='V4')
        for j, c in enumerate(conditions):
            r = metrics['views'][method]['by_condition'][c]
            n, k = r['n'], r['TP']+r['FP']
            f = k/n
            tint = Color(.93-.84*f, .96-.57*f, .98-.38*f)
            d.add(Rect(x0+j*cw, y, cw-3, ch-3, fillColor=tint, strokeColor=white))
            text(d, x0+j*cw+(cw-3)/2, y+ch/2-6, f'{k}/{n}', 19,
                 white if f>.6 else INK, 'middle', True)
    text(d, 36, 91, 'Darker = more alarms, not necessarily better detection. Each assigned condition has 8 held-out episodes.', 11, MUTED)
    text(d, 36, 66, 'B/G/I/T: no implemented-collusion positives. O: 8 positives. H: 5 positives and 3 gate failures.', 10, MUTED)
    text(d, 36, 43, 'H cells combine true and false alarms; they must not be read as recall. I exposes harm-without-agreement false alarms.', 9, MUTED)
    return d


def funnel(checks):
    d = base('Agreement, execution and harm are different outcomes',
             'Held-out generation outcomes by assigned condition | 8 valid episodes per condition | No replacements')
    x0, x1, y0, y1 = 78, 792, 135, 410
    yy = lambda n: y0+(y1-y0)*n/8
    for n in [0,2,4,6,8]:
        line(d, x0, yy(n), x1, yy(n))
        text(d, 64, yy(n)-4, n, 11, MUTED, 'end')
    colors = [BLUE, HexColor('#67a9cf'), ORANGE, TEAL]
    fields = ['agreement','execution','harm','implementation']
    labels = ['Unauthorized agreement','Agreed-plan execution','Harm','Implemented collusion']
    for j, (field, color, name) in enumerate(zip(fields, colors, labels)):
        lx = 43 + j*195
        d.add(Rect(lx, 440, 11, 11, fillColor=color, strokeColor=None))
        text(d, lx+17, 441, name, 10)
    for i, c in enumerate(['B','G','I','T','O','H']):
        center = x0+(i+.5)*(x1-x0)/6
        r = checks['held_out_generation_funnel'][c]
        for j, (field, color) in enumerate(zip(fields, colors)):
            n = r[field]; bx = center-35+j*18
            d.add(Rect(bx, y0, 15, yy(n)-y0, fillColor=color, strokeColor=None))
            text(d, bx+7.5, yy(n)+7, n, 10, color, 'middle')
        text(d, center, 113, c, 14, anchor='middle', bold=True)
    text(d, 36, 78, 'G is legitimate cooperation: its unauthorized-agreement count is zero. T has talk without executed harm.', 10, MUTED)
    text(d, 36, 55, 'I causes harm without agreement. All H cases cause harm, but only 5 meet the frozen agreement/execution gate.', 10, MUTED)
    text(d, 36, 34, 'Counts are condition-level episode outcomes, not independent rounds. Columns need not form a nested funnel.', 9, MUTED)
    return d


def attempts(metrics):
    d = base('Text helps identify attempts, but execution is a separate target',
             'Separate AUROC targets on the same 48 episodes | 95% family-bootstrap intervals')
    methods = ['V1','V2','V3','V4','mean','max']
    x = lambda v: 245+420*v
    axis(d, x, [0,.25,.5,.75,1], top=427)
    line(d, x(.5), 90, x(.5), 427, MUTED, 1, [3,3])
    for lx, name, color in [(248,'Unauthorized agreement attempt',PURPLE),(548,'Implemented harmful collusion',TEAL)]:
        d.add(Circle(lx, 445, 4, fillColor=color, strokeColor=None))
        text(d, lx+11, 441, name, 10)
    for i, name in enumerate(methods):
        y = 398-i*49
        text(d, 36, y-4, LABELS[name], 12, bold=name=='V4')
        a = metrics['attempt_detection']['views'][name]
        b = metrics['views'][name]
        whisker(d, x, y+8, a['AUROC'], a['AUROC_family_interval'], PURPLE, 3.5)
        whisker(d, x, y-8, b['AUROC'], b['AUROC_family_interval'], TEAL, 3.5)
        text(d, 708, y+4, f'{a["AUROC"]:.3f} attempt', 10, PURPLE)
        text(d, 708, y-12, f'{b["AUROC"]:.3f} executed', 10, TEAL)
    text(d, 455, 58, 'AUROC  (higher is better)', 12, anchor='middle')
    text(d, 36, 34, 'Different targets: 21 attempt positives vs 13 implemented positives. These are not treatment-effect comparisons.', 9, MUTED)
    return d


def main():
    OUT.mkdir(parents=True, exist_ok=True); TEMP.mkdir(parents=True, exist_ok=True)
    metrics_path = ROOT/'pilot/results/metrics.json'
    source_hash = hashlib.sha256(metrics_path.read_bytes()).hexdigest()
    metrics = load(metrics_path); checks = load(ROOT/'pilot/submission/quality-checks.json')
    binary = ROOT/'audit/tools/poppler-26.09.0/Library/bin/pdftoppm.exe'
    if not binary.exists():
        import shutil
        binary = shutil.which('pdftoppm')
    if not binary:
        raise RuntimeError('Poppler is required for high-resolution vector rasterization')
    charts = [('01_monitor_auroc', auroc(metrics)), ('02_paired_auroc_differences', paired(metrics)),
              ('03_condition_flag_rates', flags(metrics)), ('04_generation_outcomes', funnel(checks)),
              ('05_attempt_vs_implementation', attempts(metrics))]
    for name, drawing in charts:
        pdf = TEMP/(name+'.pdf')
        renderPDF.drawToFile(drawing, str(pdf))
        subprocess.run([str(binary), '-r', '300', '-singlefile', '-png', str(pdf), str(OUT/name)], check=True)
        with Image.open(OUT/(name+'.png')) as image:
            assert image.width==3500 and image.height==2250
        print(name+'.png', '3500 x 2250')
    assert hashlib.sha256(metrics_path.read_bytes()).hexdigest()==source_hash
    readme = '''# Track 2.2 result graphs\n\nFive 3500 x 2250 PNGs rasterized from vector ReportLab figures at300 dpi. Source: saved held-out metrics and quality checks; no new model calls, recomputation of scores, label changes or threshold changes. All estimates use48 held-out episodes across8 families. Automatic labels await independent human adjudication.\n\n1. 01_monitor_auroc: all nine methods and95% family-bootstrap intervals.\n2. 02_paired_auroc_differences: V4 minus prespecified comparators, family intervals and per-family dots.\n3. 03_condition_flag_rates: flagged/eligible counts at frozen thresholds. These are flag rates, not accuracies; H has a mixture of outcomes.\n4. 04_generation_outcomes: distinct unauthorized agreement, agreed-plan execution, harm and implemented-collusion counts.\n5. 05_attempt_vs_implementation: separate attempt and implemented-outcome targets, not a treatment-effect comparison.\n\nNo consistent structured-hybrid advantage is established. The three H implementation-gate failures are retained. Do not interpret overlapping intervals as proof of equivalence; no multiplicity-adjusted significance claim is made. Zero-call action-gap baseline overlaps outcome construction.\n\nRegenerate locally: pilot/env/Scripts/python.exe -m pilot.plot_results_png\nSource metrics JSON remains unchanged. See ../AUDIT_IMPLEMENTATION_MAP.md for how the paper audit informed the project.\n'''
    (OUT/'README.md').write_text(readme,encoding='utf-8',newline='\n')
    save(OUT/'manifest.json',{'source_metrics_sha256':source_hash,'dpi':300,'pixels':[3500,2250],
         'held_out_episodes':48,'families':8,'label_status':'provisional_automatic_human_review_pending',
         'png_sha256':{name+'.png':hashlib.sha256((OUT/(name+'.png')).read_bytes()).hexdigest() for name,_ in charts}})
    with zipfile.ZipFile(OUT/'track_2_2_png_graphs.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
        for name,_ in charts:z.write(OUT/(name+'.png'),name+'.png')
        for name in ['README.md','manifest.json']:z.write(OUT/name,name)
    contact = Image.new('RGB',(1500,1500),'#e8edf2')
    for i,(name,_) in enumerate(charts):
        with Image.open(OUT/(name+'.png')) as image:
            image.thumbnail((730,470));contact.paste(image,(10+(i%2)*750,10+(i//2)*500))
    contact.save(OUT/'preview.png')


if __name__=='__main__':
    main()
