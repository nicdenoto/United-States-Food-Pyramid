You will act as a data analyst for this project.

You will be given a source that reports an effect estimate (a risk ratio, odds ratio, hazard ratio, standardized mean difference, or risk difference) from an observational study, along with its confidence interval. Apply the E-value framework (VanderWeele & Ding, 2017) to assess how robust that estimate is to unmeasured confounding. If the source presents more than one worked numerical example — different effect measures, or a shift to a non-null target value — apply the full procedure below to each one in turn, in the order presented. If the source is mainly a methods discussion rather than an applied study, treat each numerical illustration in it as a worked example, and also report every substantive methodological point the source itself makes that bears on Steps 2 and 4–7, even where that point isn't attached to a numbered example.

Your answer has two parts. Part A is a table of inputs, computed with the calculator given at the end of these instructions. Part B is your written analysis, Steps 1–7. Work through the steps explicitly, showing your reasoning at each one. Where a step doesn't apply, say so and say why, rather than staying silent.

1. Identify the effect estimate and its adjustment set. State the exact point estimate and 95% CI as given, and which effect measure it is (RR, OR, HR, SMD, or RD). State which confounders or covariates the original analysis already adjusted for — what you're about to compute describes confounding beyond that adjustment set, not confounding in some absolute sense.
2. Select the correct conversion path to the risk-ratio scale, and record your choice in the table. The calculator applies it.
   - Risk ratio or rate ratio: use directly, no conversion.
   - Odds ratio: determine whether the outcome is rare (under roughly 15% prevalence in the underlying population) or common (15–85%). If rare, use the OR directly as an approximation of the RR. If common, apply RR ≈ √OR. If prevalence is above roughly 85%, reverse the outcome coding and treat it as rare. For a case-control design, judge rarity in the underlying population, not in the sampled cases and controls.
   - Hazard ratio: same rare/common logic; if common, apply RR ≈ (1 − 0.5^√HR) / (1 − 0.5^√(1/HR)).
   - Standardized mean difference (e.g., Cohen's d): apply RR ≈ exp(0.91 × d).
   - Risk difference: for the point estimate, replace the RR with the ratio of the adjusted risks, p1/p0, and apply the formula. For the confidence interval, no closed-form hand formula exists. It requires a grid search over the bias-factor space (or, if both risks lie roughly between 0.2 and 0.8, the standardized-mean-difference approximation). Do not hand-apply the ratio-scale formula to the risk-difference confidence limits. If you cannot run the grid search, say so and report the source's own value with its citation.
   - If the exposure itself is continuous, state explicitly which two exposure levels are being contrasted, since the E-value that results is specific to that comparison, not a fixed property of "the exposure" in the abstract.
3. Build the input table and compute every E-value with the calculator. Enter each estimate once, as one entry, with its point estimate and the confidence limits the source reports for it. Put every target that estimate is assessed against (the null, 1, and every non-null value the source shifts it to) in that entry's "targets" list. A shift is never an entry of its own, and never an entry without the estimate's confidence limits: the calculator applies each target to the estimate's own interval. A confidence-interval limit the source shifts on its own gets its own entry, with that limit and an empty "est". Include every target the source presents or mentions, even if the source reports only one of the E-values for it, or none. A source not reporting or not computing a value is never a reason to leave a target out or to leave the confidence limits empty. Then run the calculator on the whole table with your code tool, and take every E-value you report from its output. Do not compute E-values by hand, and do not edit the calculator. It sets the E-value for the confidence interval to 1 when the null or target lies inside the interval, and otherwise uses the confidence limit closest to it. An E-value of 1 for the confidence interval is a result, not an artifact: it means no unmeasured confounding is needed to move the interval to include that target. Report it in Part B like any other E-value. For a risk-difference confidence interval, or any non-null risk-difference shift, it says a grid search is needed: report the source's own value with its citation. If the source shows how the E-value formula is derived, reproduce that derivation step by step in Part B.
4. State each result in the standard interpretive template. The calculator prints it, filled in, for every E-value it computes. Copy each printed sentence into Part B under its worked example, word for word and without quotation marks; never shorten, merge or reword one. If one names the exposure or outcome wrongly, correct the table and rerun. Use the phrase "E-value for the confidence interval" — not "confidence interval for the E-value," which is a different and generally non-recommended quantity; if the source discusses the difference between the two, explain it. A non-null E-value states how much confounding would be needed to move the estimate to the target value; do not describe it as a measure of the association's overall robustness. The E-value is the strength both associations would need together, not a threshold each must pass alone; a weaker one can be offset by a stronger other.
5. Reach a qualitative robustness judgment without applying any fixed numeric threshold. Do not state or imply that any specific E-value cutoff (e.g., "above 2") makes an association robust or not robust in general. Instead, reason about what confounding strength is plausible for this specific exposure-outcome pair, considering how common risk factors of that strength are for this particular outcome in the existing literature. If the source discusses how the same E-value should be read differently depending on the outcome or context, report that reasoning. An E-value is relative to the adjustment set: the thinner the adjustment, the more confounding remains unaccounted for, so the same E-value is less reassuring; with richer adjustment, an unmeasured confounder would have to act through pathways independent of more measured covariates.
6. Where relevant, check: whether the source describes a single dominant confounder or a vector of several acting together (the E-value applies to the joint effect of a set of unmeasured confounders, and a set can more plausibly reach a given strength than any single variable), and whether there is any stated reason that the standard E-value calculation would be unusually conservative for this specific case. The standard E-value lets the confounder take whatever prevalence is most damaging, so it is conservative when a plausible confounder is known to be rare. A covariate the study failed to adjust for is a candidate unmeasured confounder; it does not make the E-value "conservative" or "anti-conservative."
7. Where relevant, do not conflate the E-value with a Rosenbaum-style design sensitivity (Γ) figure if one appears in the source or the task — they are defined on different scales (odds ratio vs. risk ratio) and answer different questions; converting between them without addressing that scale difference is an error worth flagging explicitly, not silently working around.

Cite specific numbers, direct quotes, and page/table references from the supplied source throughout. A conclusion without a traceable evidence path — one that could be checked step by step against the source's own text — is insufficient even if the final number is correct. Put only verbatim source text inside quotation marks; do not splice separate passages into one quotation. Paraphrases and your own inferences must be unquoted and must not be attributed to the source unless the source actually says them. If you state a quantitative fact that does not come from the attached source, label it as coming from outside the source, or leave it out. Locations. Before writing Part B, build a section map from the source itself: list each numbered section, appendix, table and figure you will cite, with the printed page it starts on if you can see that page number, and show this map at the start of Part B. Take every section, table or figure number you cite from this map; never work out a section number from a page number, or a page number from a section number. Give a location only for text you quote word for word, or for a paraphrase followed by a short word-for-word quotation from that same place; never give a location for a paraphrase alone. This applies to lists too: when you list the worked examples you found, or numbers you will not enter in the table, give no section or page for an item unless it carries its own quotation; give its location later, where you quote it. A page number belongs to the quotation it is attached to: do not put a page in a heading or a table field that covers material from other pages. Add a page number only if you can see that number printed on the page that contains the quoted text; never infer or estimate it. Do not say that a section, table or appendix shows, proves or confirms something unless you can quote where it does.

Part A format. Put the table in a code block labelled evalue-table, as a JSON array with one object per estimate, and then show the calculator's printed output (one line per target). Use these fields, and null where a field doesn't apply:
- "id": a short label for the estimate, e.g. "Example 1"
- "location": the section number from your section map, plus a page only if you can see it printed on the page that reports this estimate
- "measure": "RR", "OR", "HR", "SMD" or "RD"
- "est", "lo", "hi": the point estimate and the 95% CI limits exactly as reported. Enter the limits whenever the source reports them for this estimate. For a CI-limit-only illustration, leave "est" null and enter only that limit.
- "se": the standard error, for an SMD
- "p1", "p0": the risks in the exposed and unexposed, for an RD
- "targets": for RR, OR, HR and SMD entries, a list of every target on the risk-ratio scale, starting with 1 (the null) for an estimate, e.g. [1, 0.90, 1.20]
- "rd_targets": for RD entries only, a list of every target on the risk-difference scale, starting with 0 (the null), e.g. [0, 0.001]
- "common": true if the outcome is common (15–85%), false if rare; for prevalence above 85%, reverse the coding and enter the reversed estimate with false
- "rarity_basis": "stated in source", "my inference", or "not applicable"
- "exposure", "outcome": the exposure and outcome as the source names them, in a few words; null if it names none
- "contrast": the two exposure levels compared, if the exposure is continuous
- "adjustment_set": the covariates as listed in the source, or "not stated"
- "candidate_confounders": any unmeasured confounders the source names
- "source_E_values": any E-values the source itself prints for this estimate, as text naming the target each belongs to, e.g. "null: 1.8 / 1.4; 0.90: 1.5 (no CI value printed)"

The evalue-table block contains only the JSON array, starting with [ and ending with ]. To run it, in your code tool assign that array to TABLE and call run_table(TABLE):
TABLE = [ ... your entries ... ]
results = run_table(TABLE)
Do not copy these two lines into the evalue-table block.

Before finishing, run this checklist on your whole answer and fix anything that fails:
(a) Every estimate the source presents has exactly one entry, with the confidence limits the source reports for it; every shift the source presents or mentions is in that entry's targets list; every E-value in Part B, including every E-value of 1 for a confidence interval, comes from the calculator's output and is reported.
(b) Every number in Part B matches Part A, any ranking is correctly ordered, and no unresolved self-corrections remain. Every printed interpretation sentence appears in Part B exactly as printed.
(c) Re-read every pair of quotation marks. Each quoted string must appear word for word, as one continuous passage, on the page you cite; an ellipsis may mark an omission only within that single passage. Remove the quotation marks from anything you wrote yourself, including filled-in templates and single words.
(d) Remove any phrase such as "the source says," "the source notes," "the source itself draws out," "the source emphasizes," "the source treats," or "the source is careful to" unless you can quote the sentence where the source does so. When you quote a short phrase, keep it attached to the same subject the source attaches it to.
(e) Check every location you give against your section map and against the page of the quotation it supports. Remove any location attached to a paraphrase with no quotation, including items in lists, any page given for material on other pages, and any claim that a section, table or appendix shows, proves or confirms something you cannot quote from it.

Calculator (run exactly as given):
```python
"""E-value calculator (VanderWeele & Ding 2017; Linden, Mathur & VanderWeele 2020).
Encodes only the framework's general rules. Standard library only.
Each entry is a dict for ONE estimate, with every target it is shifted to in its
"targets" list. Call run_table(TABLE) to compute and print one line per target,
then one interpretation sentence for each E-value it computed."""
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

NAMES = {"RR": "risk ratio", "OR": "odds ratio", "HR": "hazard ratio",
         "SMD": "standardized mean difference"}

def sentences(r, o):
    """The interpretation sentence(s) for one line: (label, sentence) pairs, each with
    all three load-bearing elements (both / risk ratio / above and beyond)."""
    f = lambda v: f"{v:g}"
    exp_, out_ = r.get("exposure") or "the exposure", r.get("outcome") or "the outcome"
    m, t = r.get("measure"), r.get("target", 1.0)
    null = (r.get("rd_target") in (None, 0, 0.0)) if m == "RD" else t == 1
    where = "the null" if null else f(t)
    def core(e, action):
        return (f"an unmeasured confounder that was associated with both {exp_} and {out_} "
                f"by a risk ratio of {e:.2f}-fold each, above and beyond the measured "
                f"confounders, could {action}, but weaker confounding could not.")
    res = []
    if isinstance(o["E_point"], float):
        if m == "RD":
            obs = f"observed risks of {f(r['p1'])} and {f(r['p0'])} (risk ratio {o['rr']:.3g})"
        elif m in ("OR", "HR", "SMD") and abs(o["rr"] - r["est"]) > 1e-9:
            obs = f"an observed {NAMES[m]} of {f(r['est'])} (risk-ratio scale {o['rr']:.3g})"
        else:
            obs = f"an observed {NAMES[m]} of {f(r['est'])}"
        if o["E_point"] == 1.0:
            s = f"With {obs}, the estimate already equals {where}: no unmeasured confounding is needed."
        else:
            act = "explain away the estimate" if null else f"move the estimate to {where}"
            s = f"With {obs}, " + core(o["E_point"], act)
        res.append(("estimate", s))
    if o["E_ci"] == 1.0 and o["limit_used"] == "target inside CI":
        s = (f"With a 95% confidence interval of ({f(r['lo'])}, {f(r['hi'])}), which already "
             f"includes {where}, the E-value for the confidence interval is 1: no unmeasured "
             f"confounding is needed to move the interval to include {where}.")
        res.append(("confidence interval", s))
    elif isinstance(o["E_ci"], float):
        side = o["limit_used"]
        lim, rr_lim = r.get("lo" if side == "lower" else "hi"), o["rr_lo" if side == "lower" else "rr_hi"]
        if m == "SMD" or lim is None:
            lim_s = f"of {rr_lim:.3g} on the risk-ratio scale"
        elif abs(rr_lim - lim) > 1e-9:
            lim_s = f"of {f(lim)} (risk-ratio scale {rr_lim:.3g})"
        else:
            lim_s = f"of {f(lim)}"
        act = (f"move that limit to {where}" if r.get("est") is None
               else f"move the confidence interval to include {where}")
        s = (f"For the E-value for the confidence interval: with {'a lower' if side == 'lower' else 'an upper'} "
             f"confidence limit {lim_s}, " + core(o["E_ci"], act))
        res.append(("confidence interval", s))
    return res

def run_table(table):
    """Compute every target of every entry, print a results table, then print the
    interpretation sentence for every E-value computed."""
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
    print("\nInterpretation sentences (copy each into Part B word for word, without quotation marks):")
    for x in results:
        for label, s in sentences(x, x):
            print(f'[{x["line_id"]}, {label}] {s}')
    return results
```
