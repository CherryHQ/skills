#!/usr/bin/env python3
import json, re, os, sys, tempfile, zipfile, shutil
from datetime import date
from collections import Counter

if sys.platform == "win32":
    try: sys.stdout.reconfigure(encoding="utf-8")
    except: pass

TODAY = date.today()
N = chr(0x5e74); Y = chr(0x6708); R = chr(0x65e5)

CHECKS = {}
def check(sev, tag, desc):
    def d(fn):
        CHECKS[tag] = {"func": fn, "severity": sev, "description": desc}
        return fn
    return d

TECH = []
for chars in [
    [0x578b,0x53f7],[0x89c4,0x683c],[0x53c2,0x6570],[0x529f,0x7387],[0x7535,0x538b],[0x7535,0x6d41],
    [0x8f6c,0x901f],[0x91cd,0x91cf],[0x5c3a,0x5bf8],[0x6750,0x8d28],[0x7b49,0x7ea7],[0x9632,0x62a4],
    [0x7edd,0x7f18],[0x9891,0x7387],[0x5bb9,0x91cf],[0x626d,0x77e9],[0x901f,0x6bd4],[0x6a21,0x6570],
    [0x9f7f,0x6570],[0x76f4,0x5f84],[0x957f,0x5ea6],[0x5bbd,0x5ea6],[0x9ad8,0x5ea6],[0x539a,0x5ea6],
    [0x8d77,0x5347],[0x8fd0,0x884c],[0x8de8,0x5ea6],[0x8d77,0x91cd,0x91cf],[0x5de5,0x4f5c,0x7ea7,0x522b],
    [0x673a,0x6784],[0x7535,0x52a8,0x673a],[0x5236,0x52a8,0x5668],[0x51cf,0x901f,0x5668],
    [0x8054,0x8f74,0x5668],[0x6ed1,0x8f6e],[0x5377,0x7b52],[0x540a,0x94a9],[0x94a2,0x4e1d,0x7ef3],
    [0x6ed1,0x89e6,0x7ebf],[0x96c6,0x7535,0x5668],[0x53d8,0x9891,0x5668],[0x63a5,0x89e6,0x5668],
    [0x65ad,0x8def,0x5668],[0x7ee7,0x7535,0x5668],[0x6574,0x6d41],[0x7535,0x963b,0x5668],
    [0x53d8,0x538b,0x5668],[0x4f20,0x611f,0x5668],[0x9650,0x4f4d,0x5668],[0x7f16,0x7801,0x5668],
    [0x5b89,0x5168,0x5361,0x6263],[0x7535,0x52a8,0x846b,0x82a6],[0x624b,0x52a8,0x846b,0x82a6],
    [0x8d77,0x91cd],[0x7535,0x673a],[0x51cf,0x901f],[0x8f74,0x627f],[0x5bc6,0x5c01],[0x6da6,0x6ed1],
    [0x8054,0x8f74],[0x7f13,0x51b2],[0x6e05,0x626b],[0x4f9b,0x7535],
    [0x846b,0x82a6,0x5907,0x4ef6,0x7f16,0x53f7],
]:
    TECH.append("".join(chr(c) for c in chars))
@check("P0", "placeholders", "Remaining placeholders")
def ck_ph(all_text, docx_path, ctx):
    issues = []
    for pat, label in [(r"_[^_\s]{2,30}_", "underscore"), (r"\[[^\[\]]{2,40}\]", "bracket")]:
        found = re.findall(pat, all_text)
        found = [f for f in found if not f.startswith("[Content") and not f.startswith("[ISO") and not f.startswith("[http") and not any(t in f for t in TECH)]
        for f in found:
            issues.append(f"[{label}] {f}")
    return issues

@check("P0", "dates", "Date not updated")
def ck_dates(all_text, docx_path, ctx):
    issues = []
    dp = re.compile(r"(20\d{2})\s*" + N + r"\s*(\d{1,2})\s*" + Y + r"\s*(\d{1,2})\s*" + R)
    for m in dp.finditer(all_text):
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if y == TODAY.year and mo == TODAY.month and d == TODAY.day: continue
        if y > TODAY.year or y < 2010: continue
        issues.append(f"Old date: {m.group(0).strip()[:40]}")
    return issues

@check("P1", "company", "Company name issues")
def ck_co(all_text, docx_path, ctx):
    issues = []
    names = re.findall(r"[一-鿿]{4,20}(?:" + chr(0x6709)+chr(0x9650)+chr(0x516c)+chr(0x53f8) + r"|" + chr(0x80a1)+chr(0x4efd)+chr(0x6709)+chr(0x9650)+chr(0x516c)+chr(0x53f8) + r")", all_text)
    unique = list(set(names))
    # Only flag if more than 5 different company names (bid doc has buyer/agency/bank/bidder)
    if len(unique) > 5:
        for n, c in Counter(names).most_common():
            issues.append(f"{c}x: {n}")
    return issues

@check("P1", "empty", "Empty required fields")
def ck_emp(all_text, docx_path, ctx):
    issues = []
    ea = re.findall(r"\u00a5\s*" + chr(0x5143), all_text)
    if ea: issues.append(f"{len(ea)} empty amount fields")
    return issues

@check("P2", "suspicious", "Suspicious patterns")
def ck_sus(all_text, docx_path, ctx):
    issues = []
    if "XX" in all_text:
        xf = re.findall(r"XX[^\s]{0,10}", all_text)
        if xf: issues.append(f"Unresolved XX: {xf[:3]}")
    eb = re.findall(r"\u3010\s*\u3011", all_text)
    if eb: issues.append(f"{len(eb)} empty brackets")
    return issues

def extract_text(docx_path):
    td = tempfile.mkdtemp(prefix=".v_")
    try:
        with zipfile.ZipFile(docx_path, "r") as z: z.extractall(td)
        parts = []
        for r, d, fs in os.walk(td):
            for fn in fs:
                if fn.endswith(".xml"):
                    with open(os.path.join(r, fn), "r", encoding="utf-8") as f:
                        txt = f.read()
                    parts.extend(re.findall(r"<w:t[^>]*>(.*?)</w:t>", txt, re.DOTALL))
        return "".join(parts)
    finally:
        shutil.rmtree(td, ignore_errors=True)

def verify(docx_path, company_docx_path=None, strict=False):
    if not os.path.exists(docx_path):
        return {"error": f"Not found: {docx_path}"}
    print(f"  Audit: {docx_path}")
    all_text = extract_text(docx_path)
    print(f"  Text: {len(all_text)} chars")
    ctx = {}
    all_issues = []
    for tag, ci in CHECKS.items():
        try:
            for issue in ci["func"](all_text, docx_path, ctx):
                all_issues.append({"tag": tag, "severity": ci["severity"], "description": ci["description"], "detail": issue})
        except Exception as e:
            all_issues.append({"tag": tag, "severity": ci["severity"], "description": ci["description"], "detail": f"Error: {e}"})
    p0 = [i for i in all_issues if i["severity"] == "P0"]
    p1 = [i for i in all_issues if i["severity"] == "P1"]
    p2 = [i for i in all_issues if i["severity"] == "P2"]
    return {"file": docx_path, "passed": len(p0) == 0 and (not strict or len(p1) == 0), "total_issues": len(all_issues), "p0_fatal": len(p0), "p1_serious": len(p1), "p2_info": len(p2), "issues": all_issues}

def print_report(report):
    if "error" in report:
        print(f"[ERROR] {report['error']}")
        return
    print()
    print("=" * 60)
    s = "PASSED" if report["passed"] else "ISSUES FOUND"
    print(f"  Result: {s}  P0: {report['p0_fatal']}  P1: {report['p1_serious']}  P2: {report['p2_info']}")
    print("=" * 60)
    if not report["issues"]:
        print("  No issues.")
        return
    for sev, label in [("P0", "FATAL"), ("P1", "WARN"), ("P2", "INFO")]:
        items = [i for i in report["issues"] if i["severity"] == sev]
        if not items: continue
        print(f"[{label}] {len(items)}:")
        for item in items[:10]:
            print(f"  - [{item['description']}] {item['detail']}")
        if len(items) > 10:
            print(f"  ... +{len(items)-10} more")

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_bid.py <output.docx> [--company-docx file] [--strict] [--output file]")
        sys.exit(1)
    docx_path = sys.argv[1]
    cd = None; strict = False; out = None
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--company-docx" and i+1 < len(sys.argv):
            cd = sys.argv[i+1]; i += 2
        elif sys.argv[i] == "--strict":
            strict = True; i += 1
        elif sys.argv[i] == "--output" and i+1 < len(sys.argv):
            out = sys.argv[i+1]; i += 2
        else: i += 1
    report = verify(docx_path, cd, strict)
    print_report(report)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"Saved: {out}")
    sys.exit(0 if report.get("passed", False) else 1)

if __name__ == "__main__":
    main()
