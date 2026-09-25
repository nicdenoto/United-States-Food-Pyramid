# Claim inventory

One entry per claim, in the template below. WG-01 (whole grains) is the
only entry taken through the full deep pipeline (Stages 1-3, primary-source
verified, [T1] throughout) — it is "Trial 0," the foundation claim the rest
of the pipeline is being built and calibrated against.

The five entries below (RC-01, AS-01, SF-01, PR-01, PM-01) are a first-pass
catalog only, authorized 2026-09-17, covering appendix sections 4.1, 4.2,
4.6/4.7, 4.9, and 4.10. They are built from the appendix text alone — no
primary-study PDFs pulled, no front-end-report locators independently
verified (except SF-01's, added 2026-09-25 repo sweep), no per-study RCT/cohort breakdown — and are tagged [T2]/[STRUCTURE]
throughout rather than [T1]. Each carries its own "Depth flag" note. They do
not receive the WG-01-style deep pipeline run until WG-01's own run is
complete and its calibrated Stage 4 structure exists to apply to them.

Remaining appendix sections not yet catalogued even at this first-pass level:
4.3 (refined carbohydrates), 4.5 (low-carb diets), 4.8 (thermally stressed
added fats), 4.11/4.12 (life-stage and vegan/vegetarian considerations).

## WG-01 — Whole-grain / fiber-rich whole-grain recommendation bundle

**Claim as stated (front-end):** [T1 — confirmed 2026-09-14 by fetching the
front-end report directly from its official government host,
`cdn.realfood.gov/Scientific%20Report_508.pdf` ("The Scientific Foundation
for the Dietary Guidelines for Americans, 2025–2030"). Every phrase below
matched verbatim. Now archived locally as
`corpus/dga/DGA2025-2030_FrontEndReport_Scientific-Report_508.pdf` (corrected 2026-09-25 repo sweep:
this previously said "not yet archived"; see the acquisition log below).]
> "Prioritize fiber-rich whole grains." / "Significantly reduce the
> consumption of highly processed, refined carbohydrates, such as white
> bread, ready-to-eat or packaged breakfast options, flour tortillas, and
> crackers." / "Whole grains serving goals: 2–4 servings per day, adjusting
> as needed based on your individual caloric requirements." / "Individuals
> with certain chronic diseases may experience improved health outcomes when
> following a lower carbohydrate diet..."
Locator confirmed: front-end report, p. 21, Chapter 4 "Carbohydrates" —
"Recommendations: Whole Grains and Refined Carbohydrates."

**Sub-claim IDs** (definitions from `src/schema/evidence-record.md`, "On
`claim_id` and bundles"; added 2026-09-25 repo sweep to match the `claim_id`
values used in `corpus/stage3_evidence_records/WG-01.md`):
- WG-01a — prioritize (fiber-rich) whole grains
- WG-01b — reduce refined carbohydrates
- WG-01c — 2–4 servings/day target
- WG-01d — chronic-disease (lower-carbohydrate) carve-out

**GRADE certainty** [T1 — verified directly against `corpus/dga/appendices.md`,
Appendix 4.4, Table 2 (SoF Table), p. 183, and now independently cross-checked
against all three primary sources]. No single GRADE label attaches to the
recommendation itself — these are outcome-specific:
- All-cause mortality: High (RR 0.83, 95% CI 0.78–0.89) — Hu et al., 2023 [T1 — matches Hu's own "high vs low" subtotal (Figure 1) exactly; Hu's own NutriGrade quality rating for this outcome is "High"]
- Cardiovascular disease: High (RR 0.85, 95% CI 0.80–0.91) — Hu et al., 2023 [T1 — matches Hu's own "high vs low" subtotal (Figure 1) exactly; Hu's own NutriGrade quality rating for this outcome is "High"]
- Colorectal cancer: Moderate (RR 0.87, 95% CI 0.79–0.96) — Reynolds et al., 2019 [T1 — cross-verified directly against Reynolds' own published text, matches exactly]
- Obesity: Low (RR 0.85, 95% CI 0.79–0.91) — Schlesinger et al., 2019 [T1 — matches Schlesinger's own "high vs low" summary exactly; Schlesinger's own NutriGrade rating is "Low." Precision note: Schlesinger's actual outcome is "overweight/obesity" as a combined BMI-based endpoint (≥25, including the ≥30 obesity threshold), not obesity alone — the appendix's "Obesity" label is a simplification of that combined endpoint, not a wrong number.]
- Type 2 diabetes: Low (RR 0.67, 95% CI 0.58–0.78) — Reynolds et al., 2019 [T1 — cross-verified directly against Reynolds' own published text, matches exactly]

**FLAG — front-end/appendix discrepancy, all-cause mortality (added 2026-09-25
repo sweep)** [T1 — read directly from the local front-end PDF, printed p. 20
(PDF p. 39), Chapter 4 "Carbohydrates"]: the front-end states "Higher
whole-grain intake was associated with lower risk of all-cause mortality (7%,
High certainty evidence)", but Appendix 4.4 Table 2 (p. 183), the appendix's
own Summary of Evidence (p. 178: "a 17% lower risk of all-cause mortality"),
and Hu et al. 2023 all give RR 0.83, i.e. 17% lower risk. The same front-end
sentence's other four whole-grain figures (CVD 15%, CRC 13%, obesity 15%, T2D
33%) match the appendix, so this may be a transcription error, but as printed
the front-end understates its own appendix's headline mortality estimate by 10
percentage points. Record as an audit finding; do not silently harmonize.

**Appendix-internal CI discrepancy (added 2026-09-25 repo sweep):** the
Appendix 4.4 abstract (p. 167) prints the CVD CI as "0.79-0.96" and the CRC CI
as "0.76-0.96"; Table 2 (p. 183) and the primary sources agree on 0.80–0.91
(CVD) and 0.79–0.96 (CRC), the values used above.

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
  Appendix's own Strengths and Limitations (p. 178): "Most of the evidence
  was derived from observational cohorts, limiting causal inference due to
  residual confounding (e.g., lifestyle factors like physical activity)."
  **Correction from the reconciliation pass (2026-09-15), superseding the
  "null results" framing this bullet originally had:** whole-grain-specific
  RCT evidence does exist for surrogate risk-factor endpoints, and — per the
  Reynolds RCT table-mislabel correction below — it is NOT uniformly null.
  Body weight is significant (MD −0.62, 95% CI −1.19 to −0.05); total
  cholesterol, systolic blood pressure, and HbA1c remain non-significant.
  Case-analysis prose should say "no RCT evidence on hard disease outcomes;
  the whole-grain-specific RCT evidence that does exist (on risk factors) is
  mixed — significant for body weight, null for the other three," not "no
  RCT evidence exists" or "the RCT evidence is null."
- *Mechanistic* [T1]: **Corrected during the reconciliation pass — this was
  misattributed to the DGA appendix in every prior pass, including the
  WG-01 stress test's original version of this same claim.** The DGA
  appendix (p. 178) states the mechanistic pathway itself ("fibers slow
  glucose absorption, reduce postprandial insulin spikes, and enhance gut
  microbiota diversity, thereby attenuating insulin resistance and systemic
  inflammation") but does not raise the whole-grain-vs-fiber specificity
  question anywhere in its text — confirmed by an exhaustive keyword search
  (isolate/specific/attributable/distinguish/confound/disentangle) across
  the full Appendix 4.4 section. The specificity question is instead raised
  by **Reynolds 2019's own Discussion** (p. 442): "The similar protective
  effects of higher intakes of whole grain foods and of dietary fibre
  suggest that the beneficial effects of whole grains could be because of
  their high dietary fibre content. The GRADE criteria categorise the
  evidence linking most clinical outcomes with dietary fibre as moderate,
  and with whole grains as low quality. This could reflect the high fibre
  content of whole grains." (corrected 2026-09-25 repo sweep: an earlier "..." splice dropped
  the middle sentence, which is what "This" refers to.) Stated as open by
  Reynolds itself, not inferred here. The RCT findings below are directly relevant to this open question,
  though now less one-sidedly than "lean toward not whole-grain-specific"
  suggested: the fibre-general RCT evidence (Table 1) and the whole-grain
  RCT evidence (Table 2) both show a significant body-weight effect of
  similar magnitude (−0.37 vs. −0.62), which is at least consistent with —
  though does not prove — a shared, fibre-mediated mechanism.

**CORRECTED during the Stage 3 stress test (2026-09-15) — the previous
pass's "whole-grain-specific RCT" numbers were wrong.** Re-verified by
direct `pdftotext` read of the primary PDF against its own text, not
re-citing from the prior pass: Reynolds' paper reports RCT forest plots for
**three separate exposures**, tabulated on two pages and summarized in one
combined figure on a third — total dietary fibre (**Table 1, p.437** /
Figure 4A), whole grains (**Table 2, p.438** / Figure 4B), and glycaemic
index (**Table 3, same page as Table 2, p.438** / Figure 4C) — and the
numbers previously filed here as "whole-grain-specific RCTs, Table 2" are,
on direct re-check, actually the **glycaemic-index panel (Table 3 / Figure
4C)**, not Table 2 at all. (Figure 4 itself, with all three panels A/B/C, is
a separate forest-plot summary on p.442 — a distinct page from the tables it
summarizes; the original pass's single combined page citations had
conflated the two. Note for the record: an earlier correction pass in this
project also mis-stated these page numbers as 436/437/437/441, based on an
unreliable count of running-header markers in this 2-column-layout PDF's
flat text extraction; the numbers here are confirmed by direct per-page PDF
extraction, `pdftotext -f N -l N`, which is the reliable method and should
be preferred over marker-counting going forward.) The
paper's own text is explicit: "Mean differences in cardiometabolic risk
factors between higher and lower whole grain consumption are shown in
table 2 and summary forest plots in figure 4B" (p.441) — three of the four
previously-cited values (body weight MD −0.29, SBP MD −0.17, HbA1c SMD
+0.08, all with matching CIs) match the glycaemic-index panel's numbers
exactly, confirming the mislabel rather than a different dataset.
`value_status`/`provenance_tier` labeled this [T1] on the strength of a
direct PDF read — but the read pulled the wrong table, and the page
citation itself was imprecise even before that. Filing this correction as
the record of the error, not silently overwriting it.

**Corrected data, both panels, [T1] — re-verified directly against
Reynolds2019_CarbQuality_Lancet.pdf pp.437–442:**

- **Total dietary fibre RCTs** (Table 1 / Figure 4A — unaffected by the
  correction, already accurate): body weight (27 RCTs, 1294 intervention-
  arm/1201 control-arm participants, MD −0.37 kg, 95% CI −0.63 to −0.11,
  significant), systolic blood pressure (15 RCTs, 1064/988, MD −1.27 mmHg,
  95% CI −2.50 to −0.04, significant), total cholesterol (36 RCTs,
  1832/1671, MD −0.15 mmol/L, 95% CI −0.22 to −0.07, significant, flagged
  with unexplained heterogeneity >50%), HbA1c (6 RCTs, 191/189, SMD −0.35,
  95% CI −0.73 to 0.03, not significant).
- **Whole-grain-specific RCTs — TRUE Table 2 (p.438), Figure 4B (p.442)**
  (replaces the erroneous glycaemic-index numbers): body weight (**11 RCTs,
  498 intervention-arm/421 control-arm participants, MD −0.62 kg, 95% CI
  −1.19 to −0.05 — CI excludes zero, significant**, GRADE **Moderate**),
  total cholesterol (17 RCTs, 772/701, MD −0.09 mmol/L, 95% CI −0.23 to
  0.04, not significant, GRADE **Moderate**), systolic blood pressure (8
  RCTs, 493/432, MD −1.01 mmHg, 95% CI −2.46 to 0.44, not significant,
  GRADE **Moderate**), HbA1c (3 RCTs, 141/141, SMD −0.54, 95% CI −1.28 to
  0.20, not significant, GRADE **Low**). **Correction to the correction:**
  Table 2's own "GRADE quality" column reports all four per-endpoint labels
  directly (Moderate/Moderate/Moderate/Low) — an initial re-verification
  pass wrongly filed these as `NOT_REPORTED` ("not otherwise stated in the
  main text"), which was an unchecked assumption, not a checked absence.
  The paper's separate narrative statement that bodyweight/cholesterol/
  blood-pressure evidence is "downgraded to moderate because of unexplained
  heterogeneity" (p.441) is consistent with, not a substitute for, the
  table's own per-endpoint values.
- **Glycaemic-index RCTs (Table 3 / Figure 4C)** — the panel the previous
  pass actually read, mislabeled as whole grain: body weight (8 RCTs,
  464/335, MD −0.29 kg, 95% CI −0.62 to 0.03), total cholesterol (8 RCTs,
  605/478, MD −0.02 mmol/L, 95% CI −0.17 to 0.13), systolic blood pressure
  (4 RCTs, 519/397, MD −0.17 mmHg, 95% CI −1.03 to 0.69), HbA1c (2 RCTs,
  44/37, SMD +0.08, 95% CI −0.35 to 0.52) — all four CIs cross zero. Not
  relevant to WG-01 (a different exposure entirely); kept here only as the
  record of what the earlier pass actually extracted.

**Corrected synthesis:** whole-grain-specific RCT evidence shows a
**significant** reduction in body weight (MD −0.62 kg, CI excludes zero) —
the opposite of the previous pass's "essentially null effects on every
risk-factor endpoint" conclusion, which was built from the wrong panel.
Total cholesterol, systolic blood pressure, and HbA1c remain non-
significant for whole grains specifically. This changes, but doesn't
resolve, the mechanistic-leg question: the true whole-grain RCT evidence is
*not* uniformly null the way total-dietary-fibre RCT evidence is uniformly
positive, so the "benefit may be fiber-general rather than whole-grain-
specific" reading needs re-examination — three of four endpoints still
favor the fibre-general reading, but body weight now cuts the other way.
Left for Nic's case-analysis prose to characterize; not editorialized
further here.

**Flag for the case-analysis prose — revised in light of the correction:**
Reynolds' Discussion text (p.442) states: "The randomised controlled trials
involving an increase in the intake of whole grains showed reduction in
bodyweight and cholesterol." With the corrected Table 2 data: the
bodyweight claim is now **accurate** — MD −0.62, CI −1.19 to −0.05, genuinely
significant. The cholesterol claim remains an overstatement — MD −0.09, CI
−0.23 to 0.04, not significant. So the "certainty vs. evidence" tension
flagged in the previous pass holds for cholesterol specifically, but not
for bodyweight, where the prose turns out to be correct. This reverses part
of what the previous pass reported as a uniform overstatement.

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
data relating to the prospective observational studies," Table C:1 p. 35
(the CRC/T2D high-vs-low and dose-response rows specifically; pp. 36–46
are Figures C:1–C:22) and Table C:2 GRADE tables pp. 47–50 (CRC row p.49,
T2D row p.48 specifically; corrected 2026-09-25 repo sweep: previously "the table runs roughly
pp.35-47" and "Table C:2 … p. 48-50"), supplied by Nic 2026-09-14 — previously
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
years of follow-up, T2D's averages 10.8 years. Schlesinger's follow-up
duration (for the obesity outcome) is now extracted per study from
Supplemental Table 5 — see the Schlesinger section below (corrected 2026-09-25 repo sweep:
this previously said Table 5 was "not yet obtained").

**Deepened evidence-hierarchy detail (stage 3/4 pass, 2026-09-14)** [T1,
page-cited; full verbatim quotes for independent cross-check are in the
companion doc `WG-01 Stage 3-4 Deepening — Verbatim Quotes for Cross-Check`]:
- *Heterogeneity (I²):* the Hu-sourced dose-response estimates carry
  substantial between-study heterogeneity by Hu's own thresholds (>75% =
  high) — mortality I²=89.8%, CVD I²=82.9% (both p. 153). The Hu-sourced
  categorical ("high vs low") estimates are lower but still moderate-to-high:
  mortality I²=83.0% (p. 153), CVD I²=51.9% (p. 152) (corrected 2026-09-25 repo sweep by
  per-page PDF extraction: previously "p. 154" and "p. 152" for both). By contrast, the
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
  (P=0.144, P=0.409 respectively; pp. 154–155, corrected 2026-09-25 repo sweep from "p. 155") — CHD did show publication bias,
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

**Remaining items, reviewed and precisely labeled this pass (none affect
evidence tier; WG-01's five GRADE-rated outcomes all remain [T1]):**

- *Serving-to-gram conversion* — `value_status: NOT_REPORTED`, terminal.
  Confirmed absent by direct read of all five sources (front-end report,
  DGA appendix 4.4, Hu, Reynolds, Schlesinger) — this is not a search
  failure or an acquisition gap, it is a fact about the literature: no
  source anywhere converts the "2–4 servings/day" target to a gram figure.
  Nothing further to chase; case-analysis prose should treat this as a
  genuine reporting gap in the evidence base itself.
- *Per-study covariate/adjustment-factor detail* — status corrected this
  pass; the previous entry overstated how much of this was still missing.
  **Reynolds:** checked directly against his own wholegrain appendix
  (Appendix C, Tables C:1 and C:2): confirmed **absent** there. The same
  supplementary document *does* carry a full per-study covariate table for
  the total-dietary-fibre analysis (Table SUP10:2, a different exposure/
  appendix section) — so Reynolds' team clearly produces this kind of
  table when it exists, and its absence from Appendix C is a real
  absence, not an extraction miss. `value_status: NOT_REPORTED`, terminal.
  **Schlesinger:** *not actually missing.* Supplemental Table 5 (the same
  table already supplying follow-up duration) has a full "Adjustment
  factors" column, one entry per contributing study — see the extracted
  list below. **Hu:** remains the one genuinely open item — Supplemental
  Tables 1–5 are referenced in-text but still blocked by the same
  publisher bot-wall as everything else (see acquisition-attempt log
  below); closing this would need Nic to pull them the same way he pulled
  the other supplements already in hand.
- *Mechanistic-pathway specificity* (fiber → glucose/insulin → microbiota:
  whole-grain-specific, or attributable to fiber/dietary pattern
  generally) — **relabeled out of "open gaps" and into an unresolved
  evidentiary question.** This isn't something further acquisition can
  close: Reynolds 2019's own Discussion (p. 442) states the question is
  open — the DGA appendix does not raise it (see the Mechanistic bullet
  above; corrected 2026-09-25 repo sweep: previously attributed to the DGA appendix) — and
  none of the three primary papers settle it — Reynolds' RCT arm (traced above) is
  fiber-based and risk-factor-only, so it bears on the question without
  resolving it. This is itself a finding for the case-analysis (a
  mechanistic leg that the source material concedes is underspecified),
  not a corpus to-do.

**Schlesinger's per-study follow-up duration and covariate detail**
[T1 — exact provenance: `Schlesinger2019_SupplementaryData.pdf`,
Supplemental Table 5 ("General study characteristics of the included
studies investigating the association between whole grain intake and risk
of adiposity"), PDF p. 28 (document's own printed page 27), supplied by
Nic 2026-09-14; re-verified this pass by direct table read via `pdftotext`,
not just re-cited]: the 6 studies contributing to the whole-grain/adiposity
estimate report follow-up of 4 y (Bautista-Castaño 2013), 13 y (Bazzano
2005), 16 y (Boggs 2013), 5 y (De la Fuente-Arrillaga 2014), 12 y (Liu
2003), and 12 y (Quatela 2017) — each figure read directly off the table,
`value_status: SOURCE_REPORTED` per study. Reported here as the six
individual values rather than a single computed average or range label,
consistent with the Stage 3 schema's rule against the pipeline performing
arithmetic the source itself didn't state; if a single aggregate figure is
wanted for the case-analysis prose, that reduction should happen in the
prose itself (Nic's to write), not be baked into the corpus record.

The same table also carries each study's adjustment factors (previously
mischaracterized above as unobtained) and its sample size / case count —
`value_status: SOURCE_REPORTED` for all, same source and location:
- **Bautista-Castaño 2013** (n=2,213, 540 cases): age, sex, intervention
  group, weight at baseline, prevalence of diabetes mellitus at baseline,
  change in energy/alcohol/protein/SFA/PUFA/MUFA intake, change in smoking
  and physical activity.
- **Bazzano 2005** (n=22,071, 2,713 overweight cases / 1,550 weight-gain
  cases): age, smoking, baseline BMI, alcohol, physical activity, history
  of hypertension, history of high cholesterol, use of multivitamins.
- **Boggs 2013** (n=19,885, 7,183 cases): age, total energy intake,
  baseline BMI, vigorous exercise, television watching, education,
  geographic region, smoking status, parity, age at first birth, and all
  other components of the 2010 AHEI/DASH diet-quality indices.
- **De la Fuente-Arrillaga 2014** (n=9,267, 943 cases): age, sex, physical
  activity, TV watching, total sedentary time, smoking status, baseline
  BMI, fiber intake, total energy intake, olive oil, soft drinks, fast
  food.
- **Liu 2003** (n=74,091, 6,400 obesity cases / 657 weight-gain cases):
  age, changes in exercise/smoking/hormone-replacement-therapy status,
  changes in alcohol/caffeine/total-energy intake, changes in saturated/
  polyunsaturated/monounsaturated/trans fat and protein intake, BMI at
  baseline.
- **Quatela 2017** (n>58,000, 308 cases): smoking, managing income, area
  of residency, physical activity, hypertension, daily energy intake,
  fiber and other breakfast-cereal consumption, other dietary and
  non-dietary confounding factors.

Not folded into the five-outcome GRADE table above (that stays at the
pooled level per the appendix's own reporting), but now available at the
per-study level for whenever the Stage 3 retrofit builds individual
`EvidenceRecord`s under the pooled Schlesinger estimate.

**Acquisition-attempt log, this pass (2026-09-14) — everything below was
chased and confirmed still blocked, not left unfound; one item (Reynolds'
appendix) was subsequently closed the same day when Nic supplied it
directly, per the update above:**
- *Reynolds supplementary appendix* (pp. 35–50, cited in Reynolds' own
  Table 2 footnote as the source of the GRADE justifications, which carry
  the exact I² values for the colorectal-cancer and T2D whole-grain rows;
  corrected 2026-09-25 repo sweep: the footnote cites the appendix for GRADE justification,
  not I² values as such): the Lancet's own hosting
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
  precedent, closing the one item still open (Hu's supplemental tables;
  the other two were resolved the same day, corrected 2026-09-25 repo sweep) most likely
  requires Nic pulling it the same way he pulled the primary PDFs (institutional access or a
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
  (Table 1 p. 437, Table 2 p. 438, Figure 2 p. 440; corrected during the
  reconciliation pass -- confirmed by direct per-page PDF extraction after an
  earlier pass mis-stated these from an unreliable marker count). All WebFetch-sourced
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
  extracted and folded in above, all [T1]. (corrected 2026-09-25 repo sweep: a stale
  "Schlesinger's Supplemental Table 5 remains unobtained" sentence stood
  here; Table 5 was supplied 2026-09-14, see above.)

**Reviewer:** Claude — 2026-09-15 pass (remaining-gaps review; Schlesinger Table 5 verification; Reynolds RCT table mislabel correction).

---
## RC-01 — Highly processed foods (Appendix 4.1)

**Depth flag:** first-pass catalog only (authorized 2026-09-17), built from the appendix text alone — not yet deepened to WG-01's standard (no primary-study PDFs pulled, no front-end-report locator confirmed, no per-study RCT/cohort breakdown). Treat every field below as [T2] pending that pass, even where a number is quoted directly from the appendix.

**Claim as stated (appendix-level, NOT yet the confirmed front-end/consumer-report text — that still needs the same live-fetch verification WG-01 got against p. 21)** [T2 — Appendix 4.1 "Preliminary Recommendation Statement," p. 28; corrected 2026-09-25 repo sweep from "p. 29"]:
> "The evidence supports a strong recommendation for reduction in the consumption of highly processed foods for broad risk reduction for all-cause mortality, cancer, cardiovascular disease, liver disease, obesity, type 2 diabetes, dementia and depression."

**Back-end evidence** [T2]: umbrella review of 27 meta-analyses (all observational — no RCT arm reported anywhere in this appendix), 8 lead meta-analyses selected across 8 outcomes (Goran). High-vs-low HPF consumption:
- Type 2 diabetes: RR 1.48 (1.36–1.61), High
- Dementia: RR 1.44 (1.09–1.90), High
- Depression: RR 1.28 (1.19–1.38), High
- All-cause mortality: RR 1.15 (1.09–1.22), Moderate
- Cancer: RR 1.12 (1.06–1.19), Moderate
- Cardiovascular disease: RR 1.35 (1.18–1.54), Moderate
- Obesity: RR 1.55 (1.36–1.77), Moderate
- Liver disease: RR 1.58 (1.34–1.86), Low

Dose-response: a 10-percentage-point higher share of calories from HPF associated with +14% T2D, +13% cancer, +10% all-cause mortality, +7% obesity; each additional daily serving of HPF associated with +4% CVD risk. Appendix states "no study demonstrated any protective effect of HPF consumption."

**RWT legs, preliminary read** [STRUCTURE]: difference-making leg rests entirely on observational cohort/case-control evidence — the appendix's own methods describe 27 meta-analyses, all observational, with no RCT arm at all (unlike WG-01, which at least has whole-grain-specific risk-factor RCTs). Mechanistic leg not characterized in the appendix material reviewed this pass — a genuine gap to close in the deepening pass, not yet a finding.

**Note for the deepening pass:** "highly processed foods" is defined broadly here ("junk food," "ultra-processed food," "industrial food") — appendix's own Research Priorities section (Appendix 2) calls for "harmonized definitions" as an open problem, which is itself worth citing as a definitional-looseness flag on this claim.

---

## AS-01 — Added sugars, sugar-sweetened beverages, juice (Appendix 4.2)

**Depth flag:** first-pass catalog only, same caveats as RC-01 above.

**Unit of analysis** [STRUCTURE]: a four-exposure bundle (added sugars, sugar-sweetened beverages [SSBs], 100% fruit juice, non-sugar-sweetened beverages [NSSBs]) crossed against 8 outcomes — must not be treated as one claim, same discipline as WG-01's bundle.

**Claim as stated (appendix-level)** [T2 — Appendix 4.2 abstract, p. 53]: umbrella review synthesizing 54 meta-analyses (added sugars/SSB/100% juice) plus 19 (NSSBs); GRADE framework applied per exposure-outcome pair.

**Back-end evidence, selected outcomes** [T2]:
- Added sugars, all-cause mortality: RR 1.05 (95% CI 0.97–1.14) — **not significant**; appendix's own text: "no clear or significant association."
- Added sugars, NAFLD: 31% higher risk, Low-quality evidence.
- SSBs, dental caries: 57% higher risk, High.
- SSBs, adult obesity: 20% higher, Moderate.
- SSBs, type 2 diabetes: 39% higher, Moderate.
- SSBs, all-cause mortality: 10% higher, Low.
- SSBs, CVD: 20% higher, Low.
- SSBs, depression: 25% higher, Moderate.
- NSSBs, obesity (adults): RR 1.39 (0.96–2.01), Low, CI crosses 1.
- NSSBs, type 2 diabetes: RR 1.08 (1.02–1.15), Low.
- NSSBs, cognition/Alzheimer's: RR 1.42 (1.14–1.78), Moderate.

**Flag for case-analysis prose:** added sugars specifically show a **null** association with all-cause mortality — worth checking directly against whatever certainty label the front-end report attaches to an "added sugars" recommendation, since a null headline-mortality finding sitting under a confident reduction directive would be a direct certainty/evidence-structure mismatch, the same pattern this paper is built to catch elsewhere.

**RWT legs, preliminary read** [STRUCTURE]: difference-making leg — observational meta-analyses throughout what's been reviewed this pass; no RCT evidence surfaced yet for either added sugars or SSBs specifically. Mechanistic leg — not yet characterized; needs the deepening pass.

---

## SF-01 — Saturated fat (Appendices 4.6 and 4.7)

**Depth flag:** first-pass catalog only, but this one surfaced something significant enough to flag now rather than wait for deepening: **the two saturated-fat appendices disagree with each other**, not just with the front-end recommendation.

**Claim as stated (front-end, 2025–2030 report, printed p. 36 (PDF p. 55), Chapter 5 "Fats and Oils," "Recommendations: Healthy Fats")** [T1 — read directly from the local front-end PDF]: "In general, saturated fat consumption should not exceed 10% of total daily calories. Significantly limiting highly processed foods will help meet this goal. More high-quality research is needed to determine which types of dietary fats best support long-term health." (corrected 2026-09-25 repo sweep: this field previously presented the 2020–2025 DGA wording as the front-end claim.) Appendix 4.6's introduction (p. 211) quotes that older 2020–2025 wording instead: "For those two years and older, intake of saturated fat should be limited to less than 10 percent of calories per day by replacing them with unsaturated fats, particularly polyunsaturated fats." Two differences matter for the case analysis: the 2025–2030 text drops the replace-with-PUFA instruction, and its own closing hedge ("More high-quality research is needed…") is a front-end admission of uncertainty about fat types that should be weighed against the firm 10% ceiling it keeps.

**Back-end evidence — Appendix 4.6 (Zamora & Goran; GRADE + ROBIS, frequentist)** [T2]: of 9 systematic reviews of RCTs meeting inclusion criteria, only 3 were classified as estimating true causal substitution of SFA (all three: SFA replaced with omega-6 PUFA specifically). Pooled result: **no reduction in all-cause mortality (Moderate certainty) or CHD mortality (Moderate certainty); no consistent effect on CHD events (Very low certainty)**. Conclusion, quoted directly: "Causal evidence from RCTs does not demonstrate that reducing SFA to <10% of energy—particularly through replacement with linoleic acid rich vegetable oils—lowers CHD or all-cause mortality." Evidence for SFA replacement with monounsaturated fat, protein, or carbohydrate: "absent or insufficient."

**Back-end evidence — Appendix 4.7 (Brenna; Bayesian umbrella review)** [T2]: reviewed 26 studies (9 RCT syntheses, 17 cohort syntheses), 65 discrete risk estimates. Central finding: **nearly every review in this literature conflates saturated fat with trans fat from partially hydrogenated oil (PHO)** — a confounder the appendix's own author calls "universal" and says "invalidates all purported saturated fat meta-analytic and umbrella review conclusions, as the evidence base cannot distinguish saturated fat effects from those of trans fatty acids." For the resulting SF+PHO composite exposure: High certainty of no effect on total or CHD mortality (with a beneficial effect on stroke incidence); Moderate certainty of mild benefit on stroke mortality and mild harm on CHD/CVD incidence; Low certainty, equivocal effect on CVD mortality. Conclusion, quoted directly: current guidance to limit SFA to 10% of energy "lack[s] evidentiary support," and the author states an expectation that natural saturated fat studied without PHO confounding "will likely demonstrate it to be benign or beneficial for total mortality."

**Why this matters for the audit, stated plainly:** these are not two independent reviews reaching similar conclusions through different methods — 4.6 concludes the causal evidence for the current guidance is simply insufficient (an "unproven" verdict), while 4.7 goes further to argue the entire evidence base is confounded in a way that points toward the *opposite* conclusion (natural SF as likely benign-to-beneficial). Both appear in the same appendix volume, addressing the same guideline. A front-end recommendation setting a firm <10%-of-energy ceiling (as the 2025–2030 report does, albeit alongside its own "more high-quality research is needed" hedge on fat types) would be in tension with either back-end review individually, and the two back-end reviews are themselves in tension with each other on interpretation, if not on the raw effect estimates. This is a stronger, inter-appendix version of the certainty/evidence tension this audit tracks, and should likely anchor its own case-analysis subsection rather than being folded into a shorter treatment. (corrected 2026-09-25 repo sweep: premise softened from "confident, unqualified certainty," and a cross-reference to tension "already documented for whole grains (§WG-01) and refined carbohydrates" removed, since neither is documented in this file.)

**RWT legs, preliminary read** [STRUCTURE]: difference-making leg — contested between two reviews using different statistical paradigms (frequentist/GRADE vs. Bayesian) on overlapping RCT literature, with 4.7 raising an explicit, appendix-documented confounding argument (PHO) that functions as a real-world quantitative-bias-analysis case study in its own right — the raw material for an E-value/QBA treatment already exists in this corpus, not manufactured for the audit. Mechanistic leg not yet characterized from either appendix in what's been reviewed this pass.

---

## PR-01 — High-quality, nutrient-dense protein foods (Appendix 4.9)

**Depth flag:** first-pass catalog only, same caveats as RC-01/AS-01.

**Claim as stated (appendix-level "Preliminary recommendation statement," p. 413)** [T2]: "The evidence supports a strong recommendation that protein intakes between 1.2–1.6 g protein/kg body weight that prioritize high quality, nutrient dense animal and plant source protein foods, including red meat, improve nutrient (protein and/or micronutrient) adequacy when included as part of a healthy dietary pattern across most life stages."

**Back-end evidence** [T2]: certainty by outcome — Protein Density & Quality: High; Essential Amino Acid (EAA) Density & Quality: High in the evidence-to-decision box (p. 412) but **Moderate** in the Appendix G SoF table (p. 411), an internal DGA inconsistency; Micronutrient Adequacy: Moderate. Evidence base is mixed by design: 2 RCTs (higher vs. normal protein diets) rated Low specifically for the nutrient-adequacy question ("lack of sufficient data... beyond calcium"); the density-and-quality ratings rest on NHANES modeling survey studies that the SoF table annotates as "Supported by RCTs in KQ1a". (corrected 2026-09-25 repo sweep: previously gave EAA as High without the p. 411 conflict and said these ratings rested on survey/modeling studies "not RCTs.")

**Framing worth carrying into case-analysis prose, stated directly by the appendix itself:** this section is explicitly positioned as a corrective to prior DGA cycles — its own Relevance & Goals section (p. 348) states "for the past 20 years, the [DGAs] have failed to incorporate the entire range of protein and instead have modelled and recommended dietary patterns at the lower end with little to no experimental evidence to support this approach," and its evidence-to-decision table ("Problem & importance," p. 412) says of the prior plant-shift recommendation that "the majority of evidence to support this was epidemiological" (corrected 2026-09-25 repo sweep: this second quote was previously attributed to Relevance & Goals). This is a case where the appendix is arguing the *previous* guidance was itself a certainty/evidence-structure mismatch — a useful example of the same failure mode this paper investigates, occurring inside the DGA's own revision history rather than only between this paper and the DGA.

**RWT legs, preliminary read** [STRUCTURE]: difference-making leg is a mix of a small RCT base (Low certainty for the specific 1.2–1.6 g/kg nutrient-adequacy question) and larger survey/modeling evidence (higher certainty for density/quality proxies, not the same thing as adequacy at the stated range). Mechanistic leg not yet characterized this pass — protein's amino-acid/micronutrient pathways are presumably well-established in the literature generally, but not yet cited from this corpus specifically.

---

## PM-01 — Processed meats (Appendix 4.10)

**Depth flag:** first-pass catalog only, same caveats as above.

**Claim as stated (appendix-level, Abstract "Conclusions," p. 415)** [T2]: "No experimental evidence exists that processed meats, including meat alternatives, increase health risks. Since there is a lack of experimental evidence, a specific amount should not be established at this time. However, a more appropriate recommendation is to prioritize consuming unprocessed or minimally processed red meat/poultry/seafood as part of a healthy dietary pattern across all life stages." (corrected 2026-09-25 repo sweep: previously labeled the "Preliminary recommendation statement" with a "..." splice; that box, p. 422, adds after "health risks": "whereas the epidemiological evidence supports only a weak recommendation but is only evident among individuals with the highest usage.")

**Back-end evidence** [T2]: certainty — all-cause mortality: Low; cardiovascular disease risk: Low. Of 74 RCT papers screened, **zero** included a processed-vs-unprocessed or higher-vs-lower processed-meat comparison — the difference-making leg here has no RCT evidence of any kind, not even the surrogate-marker RCTs whole grains has. Epidemiological evidence: RR averaging ~1.23 (range 1.15–1.42), significant only when comparing highest vs. no/occasional intake, explicitly stated as non-linear across the intake range.

**Notable confounder-adjustment finding, appendix-cited:** one Netherlands cohort study, when adjusted for nitrite intake specifically, saw its total- and CVD-mortality associations with processed meat drop to null (HR 1.10 and 1.09 respectively — both essentially 1). This is a directly citable instance of a proposed mechanism (nitrite) being tested and the raw association weakening once it's controlled for — a ready-made quantitative-bias-analysis-style example already sitting in this corpus, similar in kind to the SF-01 PHO-confounding finding above.

**Historical framing, appendix-documented (Table 1, p. 416):** DGA language on this food group has shifted every cycle since 1985 — "salty foods" (1985) → "processed meat, poultry, and fish" (1990) → "high-fat processed meats" (1995, 2000) → "less processed items" (2005) → "processed meats" (2010) → "processed meats and poultry" (2015; corrected 2026-09-25 repo sweep, previously grouped with 2010) → "red and processed meats" (2020, 2025) — worth citing as evidence that the category itself has never stabilized, independent of the certainty question.

**RWT legs, preliminary read** [STRUCTURE]: difference-making leg — weakest of all five claims catalogued this pass: purely observational, non-linear, and only significant at extreme intake comparisons. Mechanistic leg — appendix states directly "no clear mechanism has been established," with several candidate mechanisms (nitrite, heme iron, PAHs, sodium) named but not adjudicated between; the nitrite-adjustment finding above is the strongest single piece of mechanistic-leg evidence available, and it cuts against the claim rather than for it.

