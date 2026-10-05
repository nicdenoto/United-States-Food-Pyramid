"""E-value calculator (VanderWeele & Ding 2017; Linden, Mathur & VanderWeele 2020).
Encodes only the framework's general rules. Standard library only.
Each entry is a dict for ONE estimate, with every target it is shifted to in its
"targets" list. Call run_table(TABLE) to compute and print one line per target."""
from math import sqrt, exp

def ev(x, target=1.0):
    """E-value needed to move ratio-scale value x to target (default: the null)."""
    r = x / target
    if r < 1:
        r = 1 / r
    return 1.0 if r == 1 else r + sqrt(r * (r - 1))

def to_rr(x, measure, common=False):
    """Convert an OR or HR to the risk-ratio scale (RR is returned unchanged)."""
    if measure == "RR":
        return x
    if measure == "OR":
        return sqrt(x) if common else x
    if measure == "HR":
        return (1 - 0.5 ** sqrt(x)) / (1 - 0.5 ** sqrt(1 / x)) if common else x
    raise ValueError("measure must be RR, OR or HR here (SMD and RD are handled in row)")

def row(measure, est=None, lo=None, hi=None, target=1.0, common=False,
        se=None, p1=None, p0=None, rd_target=None, **_):
    """Point and CI E-values for one estimate and ONE target. lo/hi are the CI
    limits as reported. target is on the risk-ratio scale (1 = the null).
    rd_target is on the risk-difference scale (0 = the null), for RD only.
    For a CI-limit-only illustration, give only lo (or hi) and leave est empty."""
    out = {"rr": None, "rr_lo": None, "rr_hi": None,
           "E_point": None, "E_ci": None, "limit_used": None, "note": ""}
    if measure == "RD":
        if rd_target not in (None, 0, 0.0):
            out["note"] = "non-null RD: needs grid search; report the source's values"
            return out
        out["rr"] = p1 / p0
        out["E_point"] = ev(out["rr"])
        out["note"] = "RD CI needs grid search; report the source's value"
        return out
    if measure == "SMD":
        rr = exp(0.91 * est)
        rr_lo, rr_hi = exp(0.91 * est - 1.78 * se), exp(0.91 * est + 1.78 * se)
    else:
        rr = to_rr(est, measure, common) if est is not None else None
        rr_lo = to_rr(lo, measure, common) if lo is not None else None
        rr_hi = to_rr(hi, measure, common) if hi is not None else None
    out.update(rr=rr, rr_lo=rr_lo, rr_hi=rr_hi)
    if rr is not None:
        out["E_point"] = ev(rr, target)
    if rr_lo is None and rr_hi is None:
        out["E_ci"] = "no CI entered"
        out["note"] = "correct only if the source reports no CI for this estimate"
        return out
    if rr_lo is not None and rr_hi is not None and rr_lo <= target <= rr_hi:
        out["E_ci"], out["limit_used"] = 1.0, "target inside CI"
        out["note"] = ("CI E-value is 1: no confounding is needed to move the CI "
                       "to include the target (a result, not an artifact)")
        return out
    if rr is not None:
        use_lo = rr > target
    else:
        use_lo = rr_lo is not None
    lim = rr_lo if use_lo else rr_hi
    out["E_ci"], out["limit_used"] = ev(lim, target), ("lower" if use_lo else "upper")
    return out

def expand(entry):
    """One estimate entry -> one line per target, each using the entry's own CI."""
    if entry.get("measure") == "RD":
        tl = entry.get("rd_targets")
        if tl is None:  # older one-target format
            t = entry.get("target")
            tl = [0] if t in (None, 1, 1.0) else [t]
        return [dict(entry, rd_target=t, target=1.0,
                     line_id=f'{entry.get("id")} -> RD {t}{" (null)" if t == 0 else ""}')
                for t in tl]
    tl = entry.get("targets")
    if tl is None:  # older one-target format
        tl = [entry.get("target", 1.0)]
    return [dict(entry, target=t,
                 line_id=f'{entry.get("id")} -> {t}{" (null)" if t == 1 else ""}')
            for t in tl]

def duplicates(table):
    """Estimates entered more than once (a shift belongs in the targets list).
    Two entries count as the same estimate if they share the measure and point
    estimate and either report the same limits or one of them has no limits.
    Different studies that happen to share a point estimate but report
    different intervals are not flagged."""
    dup = []
    for i, a in enumerate(table):
        if a.get("est") is None:
            continue
        for b in table[i + 1:]:
            if any(a.get(k) != b.get(k) for k in ("measure", "est", "p1", "p0")):
                continue
            la, lb = (a.get("lo"), a.get("hi")), (b.get("lo"), b.get("hi"))
            if la == lb or la == (None, None) or lb == (None, None):
                dup.append((a.get("id"), b.get("id")))
    return dup

def run_table(table):
    """Compute every target of every entry and print a results table."""
    for a, b in duplicates(table):
        print(f'WARNING: "{a}" and "{b}" are the same estimate. Merge them into one '
              f'entry and list every target in its "targets" list.')
    print("line | RR | CI on RR scale | target | E point | E CI | limit | note")
    results = []
    for e in table:
        for r in expand(e):
            o = row(**r)
            results.append({**r, **o})
            f = lambda v: "-" if v is None else (f"{v:.3f}" if isinstance(v, float) else str(v))
            t = f'RD {r["rd_target"]}' if r.get("measure") == "RD" else r["target"]
            print(f'{r["line_id"]} | {f(o["rr"])} | ({f(o["rr_lo"])}, {f(o["rr_hi"])}) | '
                  f'{t} | {f(o["E_point"])} | {f(o["E_ci"])} | '
                  f'{o["limit_used"] or "-"} | {o["note"]}')
    return results
