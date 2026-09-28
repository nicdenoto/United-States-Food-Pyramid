"""E-value calculator (VanderWeele & Ding 2017; Linden, Mathur & VanderWeele 2020).
Encodes only the framework's general rules. Standard library only.
Each row is a dict. Call run_table(TABLE) to compute and print every row."""
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
        se=None, p1=None, p0=None, **_):
    """Point and CI E-values for one row. lo/hi are the CI limits as reported.
    target is on the risk-ratio scale (1 = the null). For a CI-limit-only
    illustration, give only lo (or hi) and leave est empty."""
    out = {"rr": None, "rr_lo": None, "rr_hi": None,
           "E_point": None, "E_ci": None, "limit_used": None, "note": ""}
    if measure == "RD":
        if target != 1.0:
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
        out["E_ci"] = "no CI given"
        return out
    if rr_lo is not None and rr_hi is not None and rr_lo <= target <= rr_hi:
        out["E_ci"], out["limit_used"] = 1.0, "target inside CI"
        return out
    if rr is not None:
        use_lo = rr > target
    else:
        use_lo = rr_lo is not None
    lim = rr_lo if use_lo else rr_hi
    out["E_ci"], out["limit_used"] = ev(lim, target), ("lower" if use_lo else "upper")
    return out

def run_table(table):
    """Compute every row and print a results table."""
    print("id | RR | CI on RR scale | target | E point | E CI | limit | note")
    results = []
    for r in table:
        o = row(**r)
        results.append({**r, **o})
        f = lambda v: "-" if v is None else (f"{v:.3f}" if isinstance(v, float) else str(v))
        print(f'{r.get("id")} | {f(o["rr"])} | ({f(o["rr_lo"])}, {f(o["rr_hi"])}) | '
              f'{r.get("target", 1.0)} | {f(o["E_point"])} | {f(o["E_ci"])} | '
              f'{o["limit_used"] or "-"} | {o["note"]}')
    return results
