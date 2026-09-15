# Claim inventory

One entry per claim, in the template below. Remaining food groups (refined
carbohydrates, added sugars, saturated fat, protein, processed meats —
appendix sections 4.1, 4.2, 4.6, 4.7, 4.9, 4.10) still need entries built the
same way.

## WG-01 — Whole-grain / fiber-rich whole-grain recommendation bundle

**Claim as stated (front-end):** [T1 — confirmed 2026-09-14 by fetching the
front-end report directly from its official government host,
`cdn.realfood.gov/Scientific%20Report_508.pdf` ("The Scientific Foundation
for the Dietary Guidelines for Americans, 2025–2030"). Every phrase below
matched verbatim. Note: verified by live fetch, not yet archived as a local
file in this repo — see the acquisition log at the bottom of this entry.]
> "Prioritize fiber-rich whole grains." / "Significantly reduce the
> consumption of highly processed, refined carbohydrates, such as white
> bread, ready-to-eat or packaged breakfast options, flour tortillas, and
> crackers." / "Whole grains serving goals: 2–4 servings per day, adjusting
> as needed based on your individual caloric requirements." / "Individuals
> with certain chronic diseases may experience improved health outcomes when
> following a lower carbohydrate diet..."
Locator confirmed: front-end report, p. 21, Chapter 4 "Carbohydrates" —
"Recommendations: Whole Grains and Refined Carbohydrates."

**GRADE certainty** [T1 — verified directly against `corpus/dga/appendices.md`,
Appendix 4.4, Table 2 (SoF Table), p. 183, and now independently cross-checked
against all three primary sources]. No single GRADE label attaches to the
recommendation itself — these are outcome-specific:
- All-cause mortality: High (RR 0.83, 95% CI 0.78–0.89) — Hu et al., 2023 [T1 — matches Hu's own "high vs low" subtotal (Figure 1) exactly; Hu's own NutriGrade quality rating for this outcome is "High"]
- Cardiovascular disease: High (RR 0.85, 95% CI 0.80–0.91) — Hu et al., 2023 [T1 — matches Hu's own "high vs low" subtotal (Figure 1) exactly; Hu's own NutriGrade quality rating for this outcome is "High"]
- Colorectal cancer: Moderate (RR 0.87, 95% CI 0.79–0.96) — Reynolds et al., 2019 [T1 — cross-verified directly against Reynolds' own published text, matches exactly]
- Obesity: Low (RR 0.85, 95% CI 0.79–0.91) — Schlesinger et al., 2019 [T1 — matches Schlesinger's own "high vs low" summary exactly; Schlesinger's own NutriGrade rating is "Low." Precision note: Schlesinger's actual outcome is "overweight/obesity" as a combined BMI-based endpoint (≥25, including the ≥30 obesity threshold), not obesity alone — the appendix's "Obesity" label is a simplification of that combined endpoint, not a wrong number.]
- Type 2 diabetes: Low (RR 0.67, 95% CI 0.58–0.78) — Reynolds et al., 2019 [T1 — cross-verified directly against Reynolds' own published text, matches exactly]

**Back-end evidence it rests on** [T1]: Appendix 4.4, "Whole Grains, Refined
Carbohydrates, Fiber, Glycemic Index & Disease" — an umbrella review of 19
meta-analyses (Goran, Zamora, Bikman), pp. 166–189. Dose-response (per 30 g/day
increase in whole grains), now independently confirmed against each primary
source directly:
- All-cause mortality: 6% lower — Hu et al. 2023, RR 0.94 (95% CI 0.92–0.97) [T1]
- CVD: 8% lower — Hu et al. 2023, RR 0.92 (95% CI 0.88–0.96) [T1]
- Colorectal cancer: 6% lower — derived, see harmonization note below [T1]
- T2D: 24% lower — derived, see harmonization note below [T1]
- Obesity: 7% lower — Schlesinger et al. 2019, RR 0.93 (95% CI 0.89–0.96) [T1]

The CRC/T2D figures are the appendix authors' own harmonization of Reynolds'
original per-15g estimates, disclosed as resting on an assumption of
linearity. Reynolds' own text (independently confirmed [T1]) reports, per
15 g/day increase in whole grains: RR 0.97 (95% CI 0.95–0.99) for colorectal
cancer and RR 0.88 (95% CI 0.81–0.95) for T2D. The harmonization method is
precisely reconstructable: the appendix doubled the *percent reduction*, not
the RR itself — (1 − 0.97) × 2 = 6% for CRC, (1 − 0.88) × 2 = 24% for T2D —
both match the appendix's reported 30 g/day figures exactly. This is a
disclosed harmonization, not an independent re-derivation, and case-analysis
prose should describe it this way rather than as a doubled RR.

No serving-to-gram conversion for the "2–4 servings/day" target exists
anywhere in the appendix, the front-end report, or any of the three primary
sources — confirmed absent this pass across all five documents, not merely
unfound.

**Provenance signal (funding/COI), primary-source level** [T1]: Hu et al.
2023 report no conflict of interest and public funding only (National Natural
Science Foundation of China; Natural Science Foundation of Guangdong
Province; Natural Science Foundation of Shenzhen). Schlesinger et al. 2019
report no conflicts of interest among the authors who screened/extracted data
and public funding only (NutriAct-Competence Cluster Nutrition Research
Berlin-Potsdam; German Federal Ministry of Education and Research). Neither
paper's disclosures suggest industry influence on the whole-grain estimates.

**RWT legs carried:**
- *Difference-making* [T1]: cohort-only across all five GRADE-rated disease
  outcomes; no RCT component in how those five headline RRs were derived.
  Appendix's own Strengths and Limitations (p. 178–179): "Most of the
  evidence was derived from observational cohorts, limiting causal inference
  due to residual confounding (e.g., lifestyle factors like physical
  activity)." **Correction/addition from the direct-read pass below: this is
  true for the disease outcomes, but whole-grain-specific RCT evidence does
  exist for surrogate risk-factor endpoints — it just shows null results.**
  See the full breakdown below; case-analysis prose should say "no RCT
  evidence on hard disease outcomes, and the whole-grain-specific RCT
  evidence that does exist (on risk factors) is null," not "no RCT evidence
  exists."
- *Mechanistic* [T1]: p. 179 — "fibers slow glucose absorption, reduce
  postprandial insulin spikes, and enhance gut microbiota diversity, thereby
  attenuating insulin resistance and systemic inflammation." The appendix
  does not isolate whether this is whole-grain-specific versus attributable
  to total fiber or a broader dietary pattern — stated as open in the source
  itself, not inferred here. The RCT findings below are directly relevant to
  this open question and lean toward "not whole-grain-specific."

**Resolved and substantially extended this pass — the RCT evidence picture,
now via a direct read of Reynolds' own PDF (Table 1 p. 437, Table 2 p. 438,
supplied by Nic 2026-09-14; upgraded from the prior WebFetch-sourced pass)**
[T1]:

Reynolds ran the RCT analysis *twice* — once for total dietary fibre
(Table 1) and once specifically for whole grains (Table 2) — and the two
tell different stories:

- **Total dietary fibre RCTs** (not whole-grain-specific): body weight (27
  RCTs, MD −0.37 kg, 95% CI −0.63 to −0.11, GRADE High — CI excludes zero,
  significant), systolic blood pressure (15 RCTs, MD −1.27 mmHg, 95% CI
  −2.50 to −0.04, GRADE Moderate — significant), total cholesterol (36 RCTs,
  MD −0.15 mmol/L, 95% CI −0.22 to −0.07, GRADE Moderate — significant,
  flagged with unexplained heterogeneity >50%), HbA1c (6 RCTs, SMD −0.35,
  95% CI −0.73 to 0.03, GRADE Low — CI crosses zero, not significant).
- **Whole-grain-specific RCTs** (Table 2, same four endpoints): body weight
  (8 RCTs, MD −0.29 kg, 95% CI −0.62 to 0.03, GRADE High), HbA1c (2 RCTs,
  SMD +0.08, 95% CI −0.35 to 0.52, GRADE Very low), total cholesterol (6
  RCTs, MD −0.02 mmol/L, 95% CI −0.17 to 0.13, GRADE Moderate), systolic
  blood pressure (4 RCTs, MD −0.17 mmHg, 95% CI −1.03 to 0.69, GRADE High).
  **All four confidence intervals cross zero — none reach statistical
  significance**, despite two of the four being rated High-quality evidence.

So: whole-grain-specific RCT evidence exists, is reasonably high-quality by
GRADE, and shows essentially null effects on every risk-factor endpoint
tested — while the broader total-dietary-fibre RCT evidence (which includes
whole grains plus other fiber sources/supplements) shows small but
significant benefits on three of the four same endpoints. This is a
meaningful data point for the mechanistic-leg question above: it points
toward the appendix's benefit being attributable to fiber more broadly
rather than whole grains specifically, though it doesn't settle the question
outright (small trial counts, esp. n=2 for whole-grain HbA1c).

**Flag for the case-analysis prose — a direct "certainty vs. evidence"
tension, exactly the kind this paper is built to catch:** Reynolds'
Discussion text (p. 442) states: "The randomised controlled trials involving
an increase in the intake of whole grains showed reduction in bodyweight and
cholesterol." Table 2's own numbers (above) show negative point estimates
for both (consistent with "reduction") but with confidence intervals that
cross zero — i.e., not statistically significant by the paper's own
convention. The prose characterizes a non-significant trend as a "showed
reduction" finding. Reported here as a fact for Nic to characterize; not
editorialized further.

**Also newly available: Reynolds' own independent whole-grain dose-response
estimates for all-cause mortality and CHD incidence** (Figure 2, p. 440 —
these are Reynolds' own pooled estimates, separate from Hu et al., and not
what the appendix cites for WG-01's mortality/CVD fields, which come from
Hu): all-cause mortality RR 0.94 (95% CI 0.92–0.95) per 15 g/d whole grains;
CHD incidence RR 0.93 (95% CI 0.89–0.98) per 15 g/d. Worth flagging as a
cross-check point: converting Reynolds' per-15g mortality estimate to a
per-30g-equivalent using the appendix's own doubling-the-percent-reduction
method gives ~12% (vs. Hu's directly-reported 6% per 30 g/d) — two
independent meta-analyses of overlapping cohort literature landing on
different effect magnitudes for what both call "whole grains and all-cause
mortality." Not a contradiction (both are inverse associations, same
direction), but a real difference in size worth naming precisely rather than
treating the appendix's chosen (Hu) estimate as the only one that exists.

**Heterogeneity and follow-up duration, resolved this pass via Reynolds'
Lancet supplementary appendix (pp. 35–50, Appendix C: "Wholegrain intake
data relating to the prospective observational studies," Table C:1 p. 37
and Table C:2 GRADE table p. 48–50, supplied by Nic 2026-09-14 — previously
blocked on the open web, see the gap-chase pass)** [T1]:

- *Colorectal cancer, whole grain, high vs low* (7 studies): RR 0.87 (0.79,
  0.96), **I² = 51.9%** (p-heterogeneity = 0.053), average time followed
  **9.5 years**, 6.8 million person-years, GRADE **Moderate**. Sensitivity
  analysis (Table C:2, footnote j): initial I² was 51.9%; one study (Fung
  2010) strongly influenced the pooled result, and removing it did not
  change direction or significance (RR 0.82, 95% CI 0.75–0.90) but did drop
  I² to 20%.
- *Colorectal cancer, whole grain, per-15g dose-response* (8 studies, 5.7
  million person-years): RR 0.97 (0.95, 0.99), **I² = 45%**
  (p-heterogeneity = 0.009).
- *Type 2 diabetes, whole grain, high vs low* (8 studies): RR 0.67 (0.58,
  0.78), **I² = 82.4%** (p-heterogeneity < 0.001), average time followed
  **10.8 years**, 3.9 million person-years, GRADE **Low** (downgraded for
  inconsistency, footnote i). Sensitivity analysis: initial I² was 82.4%;
  data from one cohort (NHS I, within de Munter 2007) strongly influenced
  the pooled result, and removing it did not change direction or
  significance (RR 0.70, 95% CI 0.59–0.83) but heterogeneity remained high
  at I² = 78.5% — i.e., unlike the CRC row, this one's heterogeneity is not
  resolved by dropping the single most-influential study.
- Both GRADE labels (Moderate for CRC, Low for T2D) match what the DGA
  appendix already reported in Table 2 — this is now doubly grounded rather
  than resting on the DGA appendix's transcription alone.

This closes the "Reynolds' and Schlesinger's aggregate follow-up duration"
gap for Reynolds specifically: CRC's pooled evidence base averages 9.5
years of follow-up, T2D's averages 10.8 years. Schlesinger's aggregate
follow-up duration (for the obesity outcome) remains open — it lives in
Schlesinger's own Supplemental Table 5, not yet obtained.

**Deepened evidence-hierarchy detail (stage 3/4 pass, 2026-09-14)** [T1,
page-cited; full verbatim quotes for independent cross-check are in the
companion doc `WG-01 Stage 3-4 Deepening — Verbatim Quotes for Cross-Check`]:
- *Heterogeneity (I²):* the Hu-sourced dose-response estimates carry
  substantial between-study heterogeneity by Hu's own thresholds (>75% =
  high) — mortality I²=89.8%, CVD I²=82.9% (both p. 154). The Hu-sourced
  categorical ("high vs low") estimates are lower but still moderate-to-high:
  mortality I²=83.0%, CVD I²=51.9% (p. 152). By contrast, the
  Schlesinger-sourced obesity estimate shows *no* heterogeneity at all —
  I²=0% for both the categorical and dose-response pooled RRs (p. 208) —
  markedly more consistent across its 5–6 contributing studies than either
  Hu-sourced outcome. Worth stating precisely in case-analysis prose: the
  mortality/CVD numbers are directionally robust and match the appendix
  exactly, but rest on meta-analyses with real between-study disagreement;
  the obesity number doesn't have that caveat.
- *Quality-tool domain detail:* Hu's mean Newcastle-Ottawa Scale score for
  the whole-grain studies was 7.74/9 (p. 151) — "high quality" by their own
  0–3/4–6/7–9 banding. Hu's own NutriGrade discussion (p. 155) confirms CVD
  and all-cause mortality both rated "High" — the same label the appendix
  uses, now doubly grounded. Schlesinger's own NutriGrade rating for
  whole-grain/overweight-obesity is "Low" (p. 212), matching the appendix.
- *Sensitivity/subgroup analyses:* Hu — CVD's heterogeneity disappeared when
  stratified by region, and sensitivity analyses (leave-one-study-out) were
  "stable" for both CVD and mortality (p. 153). Publication-bias testing
  (Egger's) found none for the CVD or mortality dose-response relationships
  (P=0.144, P=0.409 respectively; p. 155) — CHD did show publication bias,
  but CHD isn't one of WG-01's five tracked outcomes. Schlesinger —
  excluding the one study that didn't adjust for energy intake "confirmed
  all findings of the primary analysis" for obesity (p. 212).
- *New data point, supplementary (not one of the appendix's original five
  outcomes):* Schlesinger et al. also report whole grains vs. **weight
  gain** — RR 0.83 (95% CI 0.70–0.97) high vs low intake (I²=16%), RR 0.91
  (95% CI 0.82–1.02) per 30 g/d dose-response (I²=69%, CI crosses 1), quality
  "Very Low" — notably weaker evidence than the obesity outcome from the
  same paper (pp. 208, 212). Flagged here as supplementary context available
  if useful, not folded into the five-outcome GRADE table above since the
  appendix itself doesn't track this outcome for WG-01.

**Provenance tier:** [T1] across the board as of this pass — front-end claim
text, all appendix-sourced fields, and all three primary studies (Hu 2023,
Reynolds 2019, Schlesinger 2019) are now directly verified. Stage 2
(reference acquirer) is complete for WG-01: no field in this entry rests on
an unverified secondary source any longer. The front-end report and all
three primary-study PDFs are now filed as local corpus files as well (see
log below) — the local-archive housekeeping gap is closed.

**Open gaps (all non-blocking, none affect evidence tier):** serving-to-gram
conversion (confirmed absent across all five sources); per-study covariate
lists (in online supplements, not in this repo — Schlesinger's own
Supplemental Table 5 now supplies whole-grain follow-up duration, but not
the full covariate/adjustment-factor detail for every outcome); whether the
mechanistic pathway described in Appendix 4.4 (fiber → glucose/insulin →
microbiota) is whole-grain-specific or attributable to fiber/dietary pattern
generally — stated as open in the appendix itself, and not resolved by any
of the three primary papers either (Reynolds' RCT arm, now traced above, is
fiber-based and risk-factor-only, so it doesn't settle this either way).

**Schlesinger's per-study follow-up duration, resolved this pass via her
own Supplemental Table 5 (supplied by Nic 2026-09-14, `Schlesinger2019_
SupplementaryData.pdf`)** [T1]: the 6 studies contributing to the
whole-grain/adiposity estimate report follow-up of 4 y (Bautista-Castaño
2013), 13 y (Bazzano 2005), 16 y (Boggs 2013), 5 y (De la Fuente-Arrillaga
2014), 12 y (Liu 2003), and 12 y (Quatela 2017) — each figure read directly
off the table, `value_status: SOURCE_REPORTED` per study. Reported here as
the six individual values rather than a single computed average or range
label, consistent with the Stage 3 schema's rule against the pipeline
performing arithmetic the source itself didn't state; if a single aggregate
figure is wanted for the case-analysis prose, that reduction should happen
in the prose itself (Nic's to write), not be baked into the corpus record.

**Acquisition-attempt log, this pass (2026-09-14) — everything below was
chased and confirmed still blocked, not left unfound; one item (Reynolds'
appendix) was subsequently closed the same day when Nic supplied it
directly, per the update above:**
- *Reynolds supplementary appendix* (pp. 35–50, cited in Reynolds' own
  Table 2 footnotes as the source of the exact I² values for the
  colorectal-cancer and T2D whole-grain rows): the Lancet's own hosting
  (`thelancet.com`, both `/fulltext` and `/journals/.../fulltext` paths)
  returned HTTP 403 to direct fetch; the University of Dundee green-OA
  manuscript copy (already on file, `discovery.dundee.ac.uk`) does not
  include the appendix — confirmed by direct read, it ends at the reference
  list (p. 26). Searched ResearchGate, Otago's institutional repository
  (Te Morenga is an Otago-affiliated co-author), and CORE.ac.uk for a mirror
  that bundles the appendix — none found. **Resolved same day:** Nic
  supplied the appendix directly (saved from his own access as
  `ReynoldsAppendix.pdf`); exact I² values, aggregate follow-up duration,
  and sensitivity-analysis detail extracted and folded into the record
  above — no longer an open gap.
- *Hu et al. 2023 supplemental tables*: the paper's own aggregate follow-up
  range (5.4–26 y) is already in hand from the supplied full-text PDF and
  matches what this record already states — not actually an open gap.
  Supplemental Tables 1–5 themselves (search terms, per-study
  characteristics) are referenced in-text but blocked the same way as
  everything else below.
- *Schlesinger et al. 2019 supplemental tables*: the whole-grain-specific
  study-characteristics table (follow-up duration for the studies behind
  the overweight/obesity estimate) is explicitly not in the main text —
  the paper points to "Supplemental Table 5" for it. `academic.oup.com` and
  the post-2022-migration mirror `advances.nutrition.org` both returned 403;
  the PMC copy (PMC6416048) served a reCAPTCHA wall instead of content; a
  ResearchGate copy of the main PDF is available but does not carry the
  supplement. **Resolved same day:** Nic supplied the full supplementary
  data bundle directly (`Schlesinger2019_SupplementaryData.pdf`);
  Supplemental Table 5's per-study follow-up duration extracted and folded
  into the record above — no longer an open gap.
- *Common thread*: every block above is the same publisher-side bot-wall
  already logged for Hu's and Schlesinger's primary PDFs in the entry below
  — journal/PMC hosts refuse automated fetches uniformly, including for
  supplementary files, not just the main article. Consistent with that
  precedent, closing these three items most likely requires Nic pulling
  them the same way he pulled the primary PDFs (institutional access or a
  logged-in browser session), not a different search strategy.
- *Front-end report, local archival copy*: **resolved.** Filed as
  `corpus/dga/DGA2025-2030_FrontEndReport_Scientific-Report_508.pdf` (90
  pages, matches the `cdn.realfood.gov`-hosted copy exactly). Public domain,
  same status as `corpus/dga/appendices.md`, so it is tracked in the repo.

**Reference acquisition log:**
- Front-end report — fetched `cdn.realfood.gov/Scientific%20Report_508.pdf`
  directly (public domain, U.S. federal work, officially hosted), 2026-09-14.
  Confirmed.
- Reynolds et al. 2019 (*Lancet*) — initially fetched the University of
  Dundee institutional-repository copy (`discovery.dundee.ac.uk`, green-OA
  author manuscript), 2026-09-14; full PDF then supplied directly by Nic the
  same day, and every figure re-verified via direct page read against it
  (Table 1 p. 437, Table 2 p. 438, Figure 2 p. 440). All WebFetch-sourced
  figures from the first pass matched exactly on direct read — no
  corrections needed, only additions (the whole-grain-specific RCT table,
  the heterogeneity flags, and Reynolds' own independent mortality/CHD
  dose-response estimates, all above). This closes the transparency gap
  flagged at the end of the previous pass.
- Hu et al. 2023 (*Am J Clin Nutr*) — open-web fetch blocked (HTTP 403,
  2026-09-14); full text supplied directly by Nic, 2026-09-14. Confirmed,
  matches appendix figures exactly (both categorical and dose-response).
- Schlesinger et al. 2019 (*Adv Nutr*) — open-web fetch blocked (HTTP 403 /
  reCAPTCHA, 2026-09-14); full text supplied directly by Nic, 2026-09-14.
  Confirmed, matches appendix figures exactly.
- Reynolds et al. 2019 supplementary appendix (*Lancet*, pp. 35–50) —
  open-web fetch blocked (HTTP 403 on `thelancet.com`; no open-access
  mirror bundles it), 2026-09-14; full appendix supplied directly by Nic
  the same day (`ReynoldsAppendix.pdf`, converted to `.md` for extraction).
  Appendix C (whole-grain data, Table C:1 and Table C:2 GRADE tables, pp.
  35–50) read directly; exact I² values, aggregate follow-up duration, and
  sensitivity-analysis detail for the CRC and T2D whole-grain rows
  extracted and folded in above, all [T1]. Schlesinger's Supplemental
  Table 5 remains unobtained.

**Reviewer:** Claude — this pass, 2026-09-14.
