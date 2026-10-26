#!/usr/bin/env python3
"""Repeatable validation. Run from project root: python3 validation/validate.py"""
import csv, os, re, sys
R=[]
def chk(name, ok, detail=""):
    R.append((name, ok, detail)); print(("PASS " if ok else "FAIL ")+name+(" - "+detail if detail else ""))
def load(p):
    with open(p,newline="") as f: return list(csv.DictReader(f))
base=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(base)
try:
    P=load("data/competitor_pricing.csv"); F=load("data/feature_comparison.csv"); S=load("data/source_register.csv"); K=load("data/pkhosting_baseline.csv"); L=load("data/research_log.csv")
    chk("All CSVs parse",True)
except Exception as e:
    chk("All CSVs parse",False,str(e)); sys.exit(1)
names=[r["provider"] for r in P]
chk("Exactly 15 competitor rows (REQUIRED)", len(P)==15, f"found {len(P)}")
chk("No duplicate providers", len(set(names))==len(names))
chk("Feature matrix covers same providers as pricing", [r["provider"] for r in F]==names)
blank=[(r["provider"],k) for r in P for k,v in r.items() if v.strip()==""]
chk("No blank pricing fields", not blank, str(blank))
nv=[r["provider"] for r in P for v in r.values() if "not verified" in v.lower()]
chk("No 'Not verified' values", not nv, str(nv))
regs={s["source_url"] for s in S}
chk("Every pricing URL is in source register", all(r["official_pricing_url"] in regs for r in P))
chk("Every pricing URL is on provider's own domain", all(re.sub(r"^https?://(www\.)?","",r["provider_website"]).split("/")[0] in r["official_pricing_url"] for r in P))
chk("Currency explicit and single-valued per row", all(r["original_currency"] in ("USD","PKR","EUR","GBP") for r in P))
bad=[]
def num(x):
    try: return float(x)
    except: return None
for r in P:
    try:
        rate=num(r["introductory_price_per_month"]); term=num(r["billing_term_months"]); up=num(r["total_upfront_calc"]); eff=num(r["effective_monthly_intro_calc"])
        if rate is None: bad.append(r["provider"]+":intro not numeric"); continue
        if up is not None and term:
            if r["upfront_basis"].startswith("calculated") and abs(round(rate*term,2)-up)>0.011: bad.append(r["provider"]+":upfront")
            if abs(up/term-eff)>0.011 and abs(rate-eff)>0.011: bad.append(r["provider"]+":effective")
        if num(r["renewal_price_per_month"]) is None or num(r["renewal_price_per_month"])<=0: bad.append(r["provider"]+":renewal")
    except Exception as e: bad.append(r["provider"]+":"+str(e))
chk("Derived upfront/monthly values reproduce from inputs", not bad, str(bad))
same=[r["provider"] for r in P if r["renewal_price_per_month"]==r["introductory_price_per_month"] and "no surprise" not in r["renewal_basis"].lower()]
chk("Intro and renewal kept separate (equal only where provider states no renewal hike)", not same, str(same))
chk("Commitment disclosed for every row", all(len(r["minimum_commitment"])>3 for r in P))
chk("Verification dates are valid ISO dates", all(re.fullmatch(r"\d{4}-\d{2}-\d{2}",r["verification_date"]) for r in P+F+K))
for must in ["GoDaddy","HostGator"]:
    chk(f"{must} has complete verified pricing record", must in names)
chk("PKHosting baseline has 3 plans", len(K)==3)
txt=open("README.md").read()
links=re.findall(r"\]\(((?!http)[^)]+)\)",txt)
chk("README relative links exist", all(os.path.exists(l) for l in links), str([l for l in links if not os.path.exists(l)]))
for f in ["CHANGELOG.md","report/competitive_positioning_report.md","report/executive_summary.md","report/methodology.md"]:
    chk(f"{f} exists", os.path.exists(f))
rep=open("report/competitive_positioning_report.md").read()
chk("Report mentions every provider in pricing CSV", all(n in rep for n in names))
chk("Report has >=5 recommendations", len(re.findall(r"^### R\d",rep,re.M))>=5)
fails=[n for n,o,_ in R if not o]
print(f"\nSUMMARY: {len(R)-len(fails)} passed, {len(fails)} failed")
if fails: print("FAILED CHECKS:", "; ".join(fails))
sys.exit(1 if fails else 0)
