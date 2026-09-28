"""Reproduces every Phase 1 answer-key value (tolerance 0.05), plus Gate 2, Gate 3 and the transfer check.
From v6: also checks that one entry with a targets list expands to one line per target,
each using the entry's own CI, and that a duplicated estimate is flagged."""
from evalue_calc import row, ev, expand, duplicates
T = 0.05
cases = [
 ("Victora RR 3.9", dict(measure="RR", est=3.9, lo=1.8, hi=8.7), 7.263, 3.000),
 ("AHRQ leukemia", dict(measure="RR", est=0.80, lo=0.71, hi=0.91), 1.809, 1.429),
 ("Moorman OR rare", dict(measure="OR", est=0.5, lo=0.3, hi=0.8), 3.414, 1.809),
 ("Oddy OR common", dict(measure="OR", est=1.47, lo=1.12, hi=1.93, common=True), 1.71, 1.31),
 ("Reinisch SMD", dict(measure="SMD", est=-0.42, se=0.14), 2.28, 1.54),
 ("Linden HR common", dict(measure="HR", est=0.1048772, lo=0.0430057, hi=0.2557622, common=True), 8.245, 4.483),
 ("Linden SMD", dict(measure="SMD", est=-0.383382, se=0.037920), 2.187, 1.981),
 ("Linden RD", dict(measure="RD", p1=397/78954, p0=51/108829), 20.947, None),
 ("2017 RD", dict(measure="RD", p1=0.00503, p0=0.000469), 20.9, None),
 ("leukemia -> 0.90", dict(measure="RR", est=0.80, lo=0.71, hi=0.91, target=0.90), 1.5, 1.0),
 ("leukemia -> 1.20", dict(measure="RR", est=0.80, lo=0.71, hi=0.91, target=1.20), 2.366, 1.967),
 ("Huybrechts null", dict(measure="RR", est=1.06, lo=0.93, hi=1.22), 1.31, 1.0),
 ("Huybrechts -> 1.20", dict(measure="RR", est=1.06, lo=0.93, hi=1.22, target=1.20), 1.52, None),
 ("Huybrechts lower 0.93 -> 1.01", dict(measure="RR", est=0.93, target=1.01), 1.39, "no CI entered"),
 ("2019 Study A", dict(measure="RR", est=1.18, lo=1.04, hi=1.33), 1.64, 1.24),
 ("2019 Study B", dict(measure="RR", est=1.18, lo=1.12, hi=1.24), 1.64, 1.49),
 ("2019 limit 1.12 only", dict(measure="RR", lo=1.12), None, 1.49),
 ("Gate 2 Poole naive", dict(measure="RR", est=3.00, lo=1.92, hi=4.69), None, 3.25),
 ("Gate 3 OR common", dict(measure="OR", est=2.2, lo=1.6, hi=3.0, common=True), 2.33, 1.84),
 ("Gate 3 -> RR 1.3", dict(measure="OR", est=2.2, lo=1.6, hi=3.0, common=True, target=1.3), 1.54, 1.0),
 ("Transfer R&J", dict(measure="RR", est=1.14, lo=1.10, hi=1.19), 1.54, 1.43),
]
fails = 0
for name, args, ep, ec in cases:
    o = row(**args)
    ok = True
    if ep is not None: ok &= abs(o["E_point"] - ep) <= T
    if isinstance(ec, float): ok &= isinstance(o["E_ci"], float) and abs(o["E_ci"] - ec) <= T
    if isinstance(ec, str): ok &= o["E_ci"] == ec
    fails += not ok
    print(("PASS" if ok else "FAIL"), name, o["E_point"], o["E_ci"], o["limit_used"], o["note"])

# v6: one entry per estimate, shifts in its targets list
expansions = [
 ("leukemia entry, targets [1, 0.90, 1.20]",
  dict(id="AHRQ", measure="RR", est=0.80, lo=0.71, hi=0.91, targets=[1, 0.90, 1.20]),
  [(1.809, 1.429), (1.5, 1.0), (2.366, 1.967)]),
 ("Huybrechts entry, targets [1, 1.20]",
  dict(id="Huy", measure="RR", est=1.06, lo=0.93, hi=1.22, targets=[1, 1.20]),
  [(1.31, 1.0), (1.52, 1.0)]),
 ("Huybrechts limit-only entry, targets [1.01]",
  dict(id="Huy lower", measure="RR", lo=0.93, targets=[1.01]),
  [(None, 1.39)]),
 ("Gate 3 entry, targets [1, 1.3]",
  dict(id="G3", measure="OR", est=2.2, lo=1.6, hi=3.0, common=True, targets=[1, 1.3]),
  [(2.33, 1.84), (1.54, 1.0)]),
 ("RD entry, rd_targets [0, 0.001]",
  dict(id="HH", measure="RD", p1=0.00503, p0=0.000469, rd_targets=[0, 0.001]),
  [(20.9, None), (None, None)]),
]
for name, entry, exp_vals in expansions:
    lines = expand(entry)
    ok = len(lines) == len(exp_vals)
    for ln, (ep, ec) in zip(lines, exp_vals):
        o = row(**ln)
        if ep is not None: ok &= o["E_point"] is not None and abs(o["E_point"] - ep) <= T
        else: ok &= o["E_point"] is None
        if ec is not None: ok &= isinstance(o["E_ci"], float) and abs(o["E_ci"] - ec) <= T
    fails += not ok
    print(("PASS" if ok else "FAIL"), name, [ln["line_id"] for ln in lines])
dup = duplicates([dict(id="a", measure="RR", est=0.8, lo=0.71, hi=0.91, targets=[1]),
                  dict(id="b", measure="RR", est=0.8, targets=[0.9])])
ok = dup == [("a", "b")]
fails += not ok
print(("PASS" if ok else "FAIL"), "duplicate estimate flagged", dup)
n = len(cases) + len(expansions) + 1
print(f"{n-fails}/{n} passed")
