"""Check report completeness, record schema, evidence and local link targets."""
import json
import re
from collections import Counter
from pathlib import Path
root=Path(__file__).resolve().parents[2]
audit=root/"audit"
findings=json.loads((audit/"evidence/findings.json").read_text(encoding="utf-8"))
ids=[f["id"] for f in findings]
assert len(ids)==len(set(ids))
assert all(f["confidence"]=="high" for f in findings)
assert all(f["severity"] in {"critical","major","minor","nit"} for f in findings)
expected={"colosseum.md":"Colosseum","traceguard.md":"TraceGuard",
          "when-agents-lie.md":"When Agents Lie","arike.md":"Arike et al.",
          "scheme.md":"Radev et al. / SCHEME"}
labels=["ID, paper, severity:","location:","what the paper says (short quote):",
        "what is wrong, with evidence:","confidence (and what would resolve it if not high):",
        "suggested fix:"]
for filename,paper in expected.items():
    content=(audit/filename).read_text(encoding="utf-8")
    for section in ["CONFIRMED","REFUTED leads","COULD NOT VERIFY"]:
        assert "## "+section in content,(filename,section)
    count=sum(f["paper"]==paper for f in findings)
    for label in labels:
        assert content.count("- "+label)==count,(filename,label)
    for target in re.findall(r"\]\(<([^>]+)>\)",content):
        target=re.sub(r":\d+$","",target)
        assert Path(target).exists(),(filename,target)
main=(audit/"FINDINGS.md").read_text(encoding="utf-8")
for label in labels:
    assert main.count("- "+label)==len(findings),label
assert len(re.findall(r"^\d+\. \*\*",main,re.M))==10
footer=main.split("## Sprint brief claims: final verdicts")[1]
assert footer.count("| **holds** |")==2
assert footer.count("| **weaker than stated** |")==3
manifest=json.loads((audit/"text/manifest.json").read_text(encoding="utf-8-sig"))
assert sum(p["pages"] for p in manifest)==161
assert all(p["pdftotext"] for p in manifest)
verification=json.loads((audit/"evidence/verification.json").read_text(encoding="utf-8"))
assert round(verification["arike_headline_EaE_gain"]["mean_pp"],1)==16.8
result={"records":len(findings),"severities":dict(Counter(f["severity"] for f in findings)),
        "required_reports":6,"local_links_exist":True,"all_required_sections":True,
        "ranked_items":10,"sprint_claims":5,"layout_pdf_pages":161}
(audit/"evidence/report_validation.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))
