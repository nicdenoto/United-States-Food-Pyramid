"""Operator-side validator for Phase 2 E-value outputs.
Usage: python3 validate_evalue.py OUTPUT.md KEY.json
1. Parses the evalue-table JSON block from the model's output.
2. Checks required fields and flags empty ones, and flags any estimate entered more than
   once (from v6, every shift belongs in one entry's "targets" list).
3. Expands each entry into one line per target and recomputes every line with the
   operator's own copy of the calculator. Older one-target tables (v5) still work.
4. Matches rows to the answer key: missing key rows (completeness/targets, D3/D6),
   wrong inputs (D1) and wrong conversion path (D2).
5. Lists every number in the text that looks like an E-value and isn't a computed value (±0.01)."""
import json, re, sys
from evalue_calc import row, expand, duplicates

REQUIRED = ["id", "location", "measure"]
TOL_IN = 0.005

def parse_table(text):
    m = re.search(r"```\s*evalue-table\s*\n(.*?)```", text, re.S)
    if not m:
        sys.exit("No evalue-table block found.")
    return json.loads(m.group(1))

def close(a, b, t=TOL_IN):
    return a is not None and b is not None and abs(float(a) - float(b)) <= t

def matches(r, k):
    if r.get("measure") != k["measure"]:
        return False
    if k["measure"] == "RD":
        null_k = k["target"] == 1.0
        null_r = r.get("rd_target") in (0, 0.0, None)
        return close(r.get("p1"), k["p1"], 1e-4) and close(r.get("p0"), k["p0"], 1e-5) and null_k == null_r
    est_ok = (k.get("est") is None and r.get("est") is None) or close(r.get("est"), k.get("est"))
    alt = k.get("alt")
    if not est_ok and alt:
        est_ok = close(r.get("lo"), alt.get("lo")) and r.get("est") is None
    return est_ok and close(r.get("target", 1.0), k["target"])

def main(out_path, key_path):
    text = open(out_path).read()
    entries, key = parse_table(text), json.load(open(key_path))
    table = [ln for e in entries for ln in expand(e)]
    print(f"Entries in model table: {len(entries)}; lines after expanding targets: "
          f"{len(table)}; rows in key: {len(key)}\n")
    print("== One entry per estimate ==")
    dup = duplicates(entries)
    for a, b in dup:
        print(f'DUPLICATE ESTIMATE: "{a}" and "{b}" (a shift entered as its own row)')
    if not dup:
        print("OK   no estimate entered twice")
    print()
    computed = []
    print("== Field check and recompute ==")
    for r in table:
        empty = [f for f in REQUIRED if r.get(f) in (None, "")]
        if r.get("measure") in ("OR", "HR") and r.get("common") is None:
            empty.append("common")
        try:
            o = row(**{k: v for k, v in r.items() if k in
                       ("measure", "est", "lo", "hi", "target", "common", "se", "p1", "p0", "rd_target")
                       and v is not None and not (k == "target" and isinstance(v, str))})
        except Exception as e:
            o = {"E_point": None, "E_ci": None, "note": f"ERROR {e}"}
        computed.append(o)
        fmt = lambda v: v if not isinstance(v, float) else round(v, 3)
        print(f'{r.get("line_id")}: E_point={fmt(o.get("E_point"))} E_ci={fmt(o.get("E_ci"))} '
              f'{"MISSING FIELDS " + str(empty) if empty else ""} {o.get("note","")}')
    print("\n== Completeness and targets against key (D3/D6), inputs (D1), path (D2) ==")
    for k in key:
        hit = [r for r in table if matches(r, k)]
        if not hit:
            print(f'MISSING ROW: {k["id"]}  (measure {k["measure"]}, target {k["target"]})')
            continue
        r = hit[0]
        issues = []
        for f in ("lo", "hi", "se"):
            if f in k and k[f] is not None and not close(r.get(f), k[f]):
                issues.append(f"{f}={r.get(f)} (key {k[f]})")
        if "common" in k and r.get("common") is not None and bool(r["common"]) != k["common"]:
            issues.append(f'path: common={r["common"]} (key {k["common"]})')
        print(f'{"OK   " if not issues else "CHECK"} {k["id"]} -> line "{r.get("line_id")}" {"; ".join(issues)}')
    print("\n== Numbers in text that look like E-values but aren't computed ==")
    vals = [v for o in computed for v in (o.get("E_point"), o.get("E_ci")) if isinstance(v, float)]
    body = re.sub(r"```.*?```", "", text, flags=re.S)
    for m in re.finditer(r"(?:E(?:-value)?\s*(?:=|≈|of)\s*|by a risk ratio of\s*)(\d+\.\d+)", body):
        x = float(m.group(1))
        if not any(abs(x - v) <= 0.01 or abs(round(v, 1) - x) < 1e-9 or abs(round(v, 2) - x) < 1e-9 for v in vals):
            print(f"  {x}  ...{body[max(0,m.start()-60):m.end()+20].strip()}...")
    print("(Source-printed values and rounding appear here too; the scorer reviews each.)")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
