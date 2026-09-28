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
3. Build the input table and compute every E-value with the calculator. Add one row for every estimate and every shift the source presents or mentions, including shifts to a non-null target value and confidence-interval limits the source discusses on their own. Add the row even if the source reports only one of the E-values, or none. A source not reporting a value is never a reason to leave a row out. Then run the calculator on the whole table with your code tool, and take every E-value you report from its output. Do not compute E-values by hand, and do not edit the calculator. The calculator applies E = RR + √(RR × (RR − 1)) after inverting RR < 1. For a shift, it uses the ratio to the target. It sets the E-value for the confidence interval to 1 when the null or target lies inside the interval, and otherwise uses the confidence limit closest to it. For a risk-difference confidence interval, or any non-null risk-difference shift, it says a grid search is needed: report the source's own value with its citation. If the source shows how the E-value formula is derived, reproduce that derivation step by step in Part B.
4. State the result using the standard interpretive template, preserving all three of its load-bearing elements: "With an observed [effect measure] of [value], an unmeasured confounder that was associated with both the [exposure] and the [outcome] by a risk ratio of [E-value]-fold each, above and beyond the measured confounders, could explain away the estimate, but weaker confounding could not." Use the phrase "E-value for the confidence interval" — not "confidence interval for the E-value," which is a different and generally non-recommended quantity; if the source discusses the difference between the two, explain it. A non-null E-value states how much confounding would be needed to move the estimate to the target value; do not describe it as a measure of the association's overall robustness. Write your filled-in version of the template as your own sentence, without quotation marks; use quotation marks only when you reproduce the source's own interpretive sentence word for word.
5. Reach a qualitative robustness judgment without applying any fixed numeric threshold. Do not state or imply that any specific E-value cutoff (e.g., "above 2") makes an association robust or not robust in general. Instead, reason about what confounding strength is plausible for this specific exposure-outcome pair, considering how common risk factors of that strength are for this particular outcome in the existing literature. If the source discusses how the same E-value should be read differently depending on the outcome or context, report that reasoning. An E-value is relative to the adjustment set: the thinner the adjustment, the more confounding remains unaccounted for, so the same E-value is less reassuring; with richer adjustment, an unmeasured confounder would have to act through pathways independent of more measured covariates.
6. Where relevant, check: whether the source describes a single dominant confounder or a vector of several acting together (the E-value applies to the joint effect of a set of unmeasured confounders, and a set can more plausibly reach a given strength than any single variable), and whether there is any stated reason that the standard E-value calculation would be unusually conservative for this specific case. The standard E-value lets the confounder take whatever prevalence is most damaging, so it is conservative when a plausible confounder is known to be rare. A covariate the study failed to adjust for is a candidate unmeasured confounder; it does not make the E-value "conservative" or "anti-conservative."
7. Where relevant, do not conflate the E-value with a Rosenbaum-style design sensitivity (Γ) figure if one appears in the source or the task — they are defined on different scales (odds ratio vs. risk ratio) and answer different questions; converting between them without addressing that scale difference is an error worth flagging explicitly, not silently working around.

Cite specific numbers, direct quotes, and page/table references from the supplied source throughout. A conclusion without a traceable evidence path — one that could be checked step by step against the source's own text — is insufficient even if the final number is correct. Put only verbatim source text inside quotation marks; do not splice separate passages into one quotation. Paraphrases and your own inferences must be unquoted and must not be attributed to the source unless the source actually says them. If you state a quantitative fact that does not come from the attached source, label it as coming from outside the source, or leave it out. Cite section numbers. Add a page number only if you can see that number printed on the page that contains the quoted text; never infer or estimate it.

Part A format. Put the table in a code block labelled evalue-table, as a JSON array with one object per row, and then show the calculator's printed output. Use these fields, and null where a field doesn't apply:
- "id": a short label, e.g. "Example 1" or "Example 1, target 0.90"
- "location": section number, plus a page only if you can see it printed
- "measure": "RR", "OR", "HR", "SMD" or "RD"
- "est", "lo", "hi": the point estimate and the 95% CI limits exactly as reported (for a CI-limit-only illustration, leave "est" null)
- "se": the standard error, for an SMD
- "p1", "p0": the risks in the exposed and unexposed, for an RD
- "target": the target on the risk-ratio scale (1 for the null)
- "common": true if the outcome is common (15–85%), false if rare; for prevalence above 85%, reverse the coding and enter the reversed estimate with false
- "rarity_basis": "stated in source", "my inference", or "not applicable"
- "contrast": the two exposure levels compared, if the exposure is continuous
- "adjustment_set": the covariates as listed in the source, or "not stated"
- "candidate_confounders": any unmeasured confounders the source names
- "source_E_point", "source_E_ci": any E-values the source itself prints for this row

Run it with:
TABLE = [ ... your rows ... ]
results = run_table(TABLE)

Before finishing, run this checklist on your whole answer and fix anything that fails:
(a) Every estimate and every shift the source presents or mentions has its own row, and every E-value in Part B comes from the calculator's output.
(b) Every number in Part B matches Part A, any ranking is correctly ordered, and no unresolved self-corrections remain.
(c) Re-read every pair of quotation marks. Each quoted string must appear word for word, as one continuous passage, on the page you cite; an ellipsis may mark an omission only within that single passage. Remove the quotation marks from anything you wrote yourself, including filled-in templates and single words.
(d) Remove any phrase such as "the source says," "the source notes," "the source itself draws out," "the source emphasizes," "the source treats," or "the source is careful to" unless you can quote the sentence where the source does so. When you quote a short phrase, keep it attached to the same subject the source attaches it to.

Calculator (run exactly as given):
```python
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
```
