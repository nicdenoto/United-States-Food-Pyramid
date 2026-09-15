# Stage 3 Schema Specification — EvidenceRecord (design case: WG-01)

**Review status:** revision 2, incorporating GPT's raw-count and
Stage 3/5-boundary review. Still not retrofitted into the existing WG-01
corpus — `stage3_evidence_hierarchy.py` stays a stub until this revision is
approved. Once approved, the next step is the actual retrofit/stress test
against WG-01, and only after that holds up does this become the frozen
Stage 3 schema for WG-02 onward.

**What this is:** a concrete answer to what `stage3_evidence_hierarchy.py`
should actually produce. The existing pipeline README describes Stage 3 as
"an LLM reconstructs which evidence types a claim relies on... and to what
severity" — accurate as a mission statement, silent on the data shape. This
document is that data shape, designed and sanity-checked against real
numbers already sitting in the WG-01 record.

---

## 1. `EvidenceRecord` — top-level shape

```
EvidenceRecord
├── evidence_id                 stable unique id, e.g. WG01-EV-004
├── claim_id                    the claim this record supports — see note below
├── record_type                 QUANTITATIVE | QUALITATIVE
├── source_id                   the immediate reporting source (points into corpus/01_sources/)
├── derived_from_source_id      optional; set only when value_status = SOURCE_DERIVED
├── field                       plain-language label, e.g. "all-cause mortality, high vs low WG intake"
├── source_wording               { text, is_verbatim_quote: bool }
├── source_location             see §6
├── study_classification        see §7
├── numerical_provenance        see §2/§3 — present only if record_type = QUANTITATIVE, absent (not null) otherwise
├── qualitative_content         present only if record_type = QUALITATIVE — free-text claim + a category tag (MECHANISTIC | LIMITATION | QUALITY_CAVEAT | OTHER)
├── value_status                see §2 — set ONCE per record, describing the primary reported estimate
├── provenance_tier             see §4
├── pipeline_stage              see §5
├── quality_signals             see §8 — 0 or more, each independently tiered
├── evidence_role               see §7
├── reviewer
└── review_date
```

**On `claim_id` and bundles:** WG-01 is a four-part bundle (prioritize whole
grains / reduce refined carbs / 2–4 servings target / chronic-disease
carve-out). `claim_id` resolves to a leaf sub-claim (`WG-01a`, `WG-01b`,
`WG-01c`, `WG-01d`), never to the bundle as a whole.

**Why `record_type` exists:** WG-01 already contains evidence that isn't a
number with a unit and a CI — the fiber→glucose/insulin→microbiota
mechanistic-pathway text, Reynolds' plain-language heterogeneity caveats.
`record_type` makes that fork explicit at the top of the record instead of
forcing everything through a numeric block.

---

## 2. `value_status`

Set **once per record** — it describes the record's primary reported
estimate (the number in `numerical_provenance.estimate`), not each raw-count
sub-field individually (those use a simpler sentinel, see §3).

```
SOURCE_REPORTED   value appears in the cited source as-is; no arithmetic
                  performed by anyone in the citation chain beyond a
                  straightforward unit restatement.

SOURCE_DERIVED    the immediate source computed/transformed this value from
                  another source's reported value. Requires
                  derived_from_source_id and a one-line
                  derivation_description (e.g. "doubled Reynolds' per-15g
                  percent reduction to express per-30g, on a stated
                  assumption of linearity").

MODEL_DERIVED     computed by this pipeline (an LLM judgment, a statistic
                  Stage 5 runs, an E-value we calculate). Reserved — NOT
                  permitted on any record living under corpus/ (see §9,
                  §10). Its only job is marking where the architecture's
                  boundary is; it should never actually appear in the
                  corpus.

NOT_REPORTED      the source was checked and does not state this value.
                  Still requires a source_location (see §6) — a claim of
                  absence is itself an extraction result, not a default.

NOT_APPLICABLE    there is no value to report because record_type is
                  QUALITATIVE. Distinguishes "we looked and it's missing"
                  from "a number was never the right shape for this record."
```

Worked split, using material already in the record: Hu's mortality RR is
`SOURCE_REPORTED`. The DGA appendix's 24% per-30g T2D figure is
`SOURCE_DERIVED` (from Reynolds' per-15g RR). The serving-to-gram
conversion is `NOT_REPORTED` (confirmed absent across five sources, not
merely unfound). The mechanistic-pathway quote is `NOT_APPLICABLE` because
it's a `QUALITATIVE` record.

*(Note: this field was called `derivation_note` in revision 1. Renamed to
`derivation_description` in this revision — same field, one name, so the
two don't drift into meaning slightly different things.)*

---

## 3. Raw-count fields in `numerical_provenance`

New in this revision. The rule governing all of it: **only populate a field
when the immediate source explicitly reports it. Never reconstruct a raw
count from other reported values, even when the arithmetic is trivial**
(e.g. never back-computing `sample_size_comparator` from
`sample_size_total − sample_size_intervention`). The corpus is an
extraction layer, not a calculation layer — that reduction is Stage 5's job,
once it exists, using inputs Stage 3 already made explicit.

**Two shapes, not one.** WG-01's actual evidence is overwhelmingly pooled
meta-analyses of cohort studies (dose-response and high-vs-low-quantile
estimates across many contributing studies), not two-arm trials. Forcing
every record through an RCT-shaped field set (`sample_size_intervention` /
`sample_size_comparator`) would mark those fields `NOT_REPORTED` on nearly
every WG-01 record for a reason that has nothing to do with the source
under-reporting — the two-arm shape is simply the wrong fit. So which shape
applies is selected by `study_classification.study_design`, and **only the
applicable shape's sub-object is present on the record; the other is
omitted entirely, not present with `NOT_REPORTED` values.**

```
study_classification.study_design ∈ { RCT, cohort, case-control,
  nested-case-control }
    → numerical_provenance.raw_counts_two_arm
        ├── sample_size_total
        ├── sample_size_intervention
        ├── sample_size_comparator
        ├── events_total
        ├── events_intervention
        ├── events_comparator
        ├── person_time
        └── follow_up_duration

study_classification.study_design ∈ { cohort-meta-analysis,
  umbrella-review }
    → numerical_provenance.raw_counts_pooled
        ├── contributing_study_count
        ├── pooled_n_participants
        ├── pooled_n_events
        ├── person_time
        └── follow_up_duration
```

(`study_design`'s enum gains `cohort-meta-analysis` in this revision —
revision 1's worked example A already used that value; it just wasn't in
the enum. `narrative` designs don't carry raw counts at all, and typically
pair with `record_type: QUALITATIVE`.)

Within whichever sub-object applies, an individual field is either
populated with the value the source reports, or set to the literal string
`"NOT_REPORTED"` — no separate per-field status enum. `value_status`
(§2) still governs the record's primary estimate; these sentinel values are
enough for sub-fields, so the schema doesn't grow a second status axis
nobody asked for.

**Worked example, real WG-01 numbers:** Reynolds' CRC high-vs-low pooled
estimate (7 studies, 6.8 million person-years, 9.5 y average follow-up) is
`study_design: cohort-meta-analysis`, so it gets `raw_counts_pooled`:
`contributing_study_count: 7`, `person_time: "6.8 million person-years"`,
`follow_up_duration: "9.5 years (average)"`, and `pooled_n_participants` /
`pooled_n_events`: `"NOT_REPORTED"` — Table C:1 gives person-years and
study count but not a pooled participant or event count, and that's a fact
about the table, not a gap in this extraction.

---

## 4. `provenance_tier`

**Unchanged from the existing corpus convention** — `T1` primary-verified,
`T2` secondary-sourced, `STRUCTURE` structure-inferred — kept as its own
field rather than folded into `value_status` (rejecting the `[T1-D]`
composite-tag idea, per the "independent dimensions" framing both reviewers
converged on). Tier answers *how directly did the pipeline verify this*;
`value_status` answers *was arithmetic performed, and by whom*. Orthogonal
axes; no composite tag needed.

| | SOURCE_REPORTED | SOURCE_DERIVED |
|---|---|---|
| **T1** | Hu's mortality RR — read directly from the supplied PDF | DGA appendix's 24% T2D figure — appendix authors' own disclosed harmonization, read directly |
| **T2** | A number inherited from a prior session's doc, not independently re-opened this pass | (no current example — would be a secondhand report of someone else's harmonization) |

---

## 5. `pipeline_stage`

Tags which stage produced or last touched this record, independent of what
the record contains:

```
STAGE2_ACQUIRED              a source is collected/verified; no evidence
                              record built from it yet
STAGE3_EXTRACTED             this EvidenceRecord's shape is set —
                              classification, value_status, provenance_tier
                              assigned by extraction, not judgment
STAGE4_APPRAISED             a framework judgment (GRADE/Bradford
                              Hill/E-value/QBA/ROBIS/AMSTAR-2) has been
                              applied BY THE PIPELINE — lives on a separate
                              AppraisalRecord, see §9
STAGE5_STATISTICALLY_EVALUATED
STAGE6_GAP_FLAGGED
```

A record's `pipeline_stage` can only move forward (2→3→4→5→6); nothing
here demotes a record, it only accumulates linked downstream records.

---

## 6. Source-location fields

```
source_location
├── document           file/citation the value lives in
├── page                page or page range
├── table_or_figure     e.g. "Table C:2, footnote i"; null if body text
├── section_heading     optional, e.g. "Strengths and Limitations"
├── extraction_date
└── extractor           reviewer id, e.g. "Claude"
```

Required on every record regardless of `value_status` — including
`NOT_REPORTED`, where it proves the absence was checked in a specific place
rather than assumed.

---

## 7. Study / outcome / exposure fields (evidence classification)

```
study_classification
├── study_design         RCT | cohort | case-control | nested-case-control
│                         | cohort-meta-analysis | umbrella-review | narrative
├── population
├── exposure
├── comparator
├── outcome
├── effect_measure        RR | HR | OR | MD | SMD | qualitative
└── follow_up             { value_status, value } — same NOT_REPORTED vs
                          NOT_APPLICABLE distinction as §2

evidence_role
├── role                  DIFFERENCE_MAKING | MECHANISTIC | QUALITY_CAVEAT
│                         | ALTERNATIVE_ESTIMATE
└── cited_by_recommendation_source   boolean, REQUIRED whenever more than
                                     one EvidenceRecord shares a claim_id +
                                     outcome pair
```

`cited_by_recommendation_source` is the fix for the competing-estimates
case already sitting in the record: Reynolds independently reports his own
whole-grain mortality dose-response (RR converting to ~12% per 30g), a
different number from Hu's 6% that the DGA appendix actually cites for that
outcome. Hu's record gets `cited_by_recommendation_source: true`;
Reynolds' independent estimate gets `false` and its own `evidence_role:
ALTERNATIVE_ESTIMATE`.

---

## 8. Source-reported quality fields

```
quality_signals[]   — zero or more, each its OWN tiny provenance record:
├── signal_type      GRADE | NOS | ROBIS | NutriGrade | funding_coi | other
├── value             e.g. "Moderate", "7.74/9", "no conflicts declared"
├── attributed_to     whose rating this is — always the SOURCE, never the
│                     pipeline, at Stage 3
├── provenance_tier
└── source_location
```

A quality signal is itself an extraction subject to the same verification
discipline as any other value — "the appendix's Table 2 says Moderate" and
"Reynolds' own GRADE table independently says Moderate" are two separate
`[T1]` facts that happen to agree, not one fact transcribed twice.

---

## 9. Stage 3 / Stage 4 boundary — made structural, not just documented

**Stage 3 (this schema) does:** capture what a source states, including any
quality/appraisal label the *source itself* already assigned. It
classifies — study design, exposure, outcome, evidence role — but renders
no new judgment of adequacy.

**Stage 4 does:** apply GRADE, Bradford Hill, E-value, QBA, ROBIS, AMSTAR-2
as the *pipeline's own* appraisal, via a separate record type:

```
AppraisalRecord
├── appraisal_id
├── framework            GRADE | Bradford-Hill | E-value | QBA | ROBIS | AMSTAR-2
├── references            [evidence_id, ...] — one or more EvidenceRecords
│                         this appraisal judges; NEVER edits them in place
├── judgment
├── value_status          MODEL_DERIVED by definition — this is the
│                         pipeline computing something new
├── pipeline_stage         STAGE4_APPRAISED
└── reviewer / date
```

Appraisal referencing evidence records rather than annotating them in place
is what enforces "I pull numbers from PDFs, I don't perform calculations"
as a fact about the data model, not a convention a reviewer has to
remember. An `AppraisalRecord` is `MODEL_DERIVED` by construction, which §2
and §10 say can't exist under `corpus/` — so `AppraisalRecord`s belong in
`analysis/`, never in the extraction corpus itself.

---

## 10. Stage 3 / Stage 5 boundary — new in this revision

The boundary is made explicit now, without designing Stage 5's statistical
model:

```
Stage 3
│
├── reported estimate
├── estimate type
├── CI / SE if reported
├── raw counts if reported          (§3)
├── exposure dose / unit
├── follow-up
└── provenance
        │
        ▼
   ANALYSIS-READY INFORMATION
        │
        ▼
Stage 5
└── the statistical model — not yet designed
```

Stage 3 answers *what numerical information does the evidence actually
contain*. Stage 5 later answers *what can be statistically done with that
information*. `EvidenceRecord` and its `numerical_provenance` block
therefore contain **inputs, never analytical instructions.** Concretely,
none of the following — nor anything with the same character — belongs in
`numerical_provenance` or anywhere else on an `EvidenceRecord`:

```
recommended_model: meta_analysis        ✗ analytical decision, not data
transform_to_log_rr: true               ✗ analytical decision, not data
calculate_NNT: ...                      ✗ analytical decision, not data
```

Those are Stage 5's decisions to make later, once it exists. This also
resolves the tension the pipeline README already creates by assigning
E-value/QBA to Stage 4: Stage 5 is not "everything downstream of Stage 3"
in one undifferentiated pile — it specifically consumes analysis-ready
`EvidenceRecord` fields (raw counts, CIs, dose/unit, follow-up) to run
statistical models Stage 4's fixed frameworks don't cover, while Stage 4
continues to own the named frameworks (GRADE, Bradford Hill, E-value, QBA,
ROBIS, AMSTAR-2) as its own `AppraisalRecord`s. Stage 5 can read
`EvidenceRecord`s directly; it does not have to wait on Stage 4's
`AppraisalRecord`s first, since the two consume the same upstream data for
different purposes.

---

## 11. Validation rules

1. `value_status = SOURCE_DERIVED` ⟹ `derived_from_source_id` is required
   and must resolve to an existing `source_id`, and `derivation_description`
   is required.
2. `value_status = MODEL_DERIVED` ⟹ the record is rejected under `corpus/`
   at ingestion; it belongs under `analysis/` as an `AppraisalRecord` or
   Stage-5 output.
3. `record_type = QUALITATIVE` ⟹ `numerical_provenance` must be entirely
   absent from the record, not present-with-nulls.
4. `value_status = NOT_REPORTED` ⟹ `source_location` is still required.
5. `provenance_tier` and `value_status` are set independently; no
   combination is disallowed, and no composite tag (`[T1-D]`) is used in
   place of the two fields.
6. Every `EvidenceRecord.claim_id` resolves to a leaf sub-claim, never a
   bundle claim with multiple independently-evidenced elements.
7. Whenever two or more `EvidenceRecord`s share a `claim_id` +
   `study_classification.outcome` pair, each must set
   `evidence_role.cited_by_recommendation_source` — silence on this field
   is a validation failure, not a default of `false`.
8. An `AppraisalRecord` may only reference existing `evidence_id`s; it
   never carries its own free-standing numeric extraction.
9. A raw-count field (§3) is populated only when the immediate source
   explicitly reports it; it is never reconstructed from other reported
   values, even when the arithmetic is trivial.
10. Exactly one of `raw_counts_two_arm` / `raw_counts_pooled` is present on
    a `QUANTITATIVE` record, selected by `study_classification.study_design`;
    the other is omitted entirely — never present with `"NOT_REPORTED"`
    values standing in for a structurally inapplicable field set.
11. `numerical_provenance` never contains an analytical instruction or
    downstream-model directive (e.g. `recommended_model`,
    `transform_to_log_rr`, `calculate_NNT`) — Stage 3 records what the
    evidence contains, never what a later stage should do with it.

---

## 12. Miniature WG-01 examples

**A — clean, `SOURCE_REPORTED`, pooled shape:**

```
evidence_id: WG01-EV-001
claim_id: WG-01a
record_type: QUANTITATIVE
source_id: SRC-HU-2023
field: "all-cause mortality, high vs low whole-grain intake"
study_classification: { study_design: cohort-meta-analysis, population: adults,
  exposure: high WG intake, comparator: low WG intake,
  outcome: all-cause mortality, effect_measure: RR }
numerical_provenance:
  estimate: 0.83
  CI: [0.78, 0.89]
  raw_counts_pooled: { contributing_study_count: "NOT_REPORTED",
    pooled_n_participants: "NOT_REPORTED", pooled_n_events: "NOT_REPORTED",
    person_time: "NOT_REPORTED", follow_up_duration: "5.4-26 y (range across
    contributing studies)" }
value_status: SOURCE_REPORTED
provenance_tier: T1
pipeline_stage: STAGE3_EXTRACTED
quality_signals: [{ signal_type: NOS, value: "7.74/9 (mean)",
  attributed_to: Hu 2023, provenance_tier: T1, source_location: p.151 }]
evidence_role: { role: DIFFERENCE_MAKING, cited_by_recommendation_source: true }
source_location: { document: Hu2023_WholeGrains_AJCN.pdf, page: 152 }
```

**B — `SOURCE_DERIVED`, the harmonization case:**

```
evidence_id: WG01-EV-005
claim_id: WG-01a
record_type: QUANTITATIVE
source_id: SRC-DGA-APP-4.4
derived_from_source_id: SRC-REYNOLDS-2019
field: "type 2 diabetes, per-30g/day whole-grain dose-response"
numerical_provenance: { estimate: "24% lower risk" }
value_status: SOURCE_DERIVED
derivation_description: "DGA appendix doubled Reynolds' per-15g percent
  reduction (1 − 0.88) × 2 = 24%, on a stated assumption of linearity — not
  a fresh re-derivation by this pipeline."
provenance_tier: T1
pipeline_stage: STAGE3_EXTRACTED
evidence_role: { role: DIFFERENCE_MAKING, cited_by_recommendation_source: true }
source_location: { document: "Scientific Report Appendices_FINAL_1.28.26.md",
  page: 173 }
```

**C — `QUALITATIVE`, the mechanistic-evidence case:**

```
evidence_id: WG01-EV-009
claim_id: WG-01a
record_type: QUALITATIVE
source_id: SRC-DGA-APP-4.4
field: "mechanistic pathway — fiber/glucose/insulin/microbiota"
qualitative_content: { category: MECHANISTIC,
  text: "fibers slow glucose absorption, reduce postprandial insulin
  spikes, and enhance gut microbiota diversity, thereby attenuating
  insulin resistance and systemic inflammation" }
numerical_provenance: <absent — record_type is QUALITATIVE>
value_status: NOT_APPLICABLE
provenance_tier: T1
pipeline_stage: STAGE3_EXTRACTED
evidence_role: { role: MECHANISTIC, cited_by_recommendation_source: true }
source_location: { document: "Scientific Report Appendices_FINAL_1.28.26.md",
  page: 179 }
```

**D — pooled shape with raw counts actually populated (new in this
revision):**

```
evidence_id: WG01-EV-011
claim_id: WG-01a
record_type: QUANTITATIVE
source_id: SRC-REYNOLDS-2019-APPENDIX
field: "colorectal cancer, whole grain, high vs low (Reynolds appendix)"
study_classification: { study_design: cohort-meta-analysis, population: adults,
  exposure: high WG intake, comparator: low WG intake,
  outcome: colorectal cancer incidence, effect_measure: RR }
numerical_provenance:
  estimate: 0.87
  CI: [0.79, 0.96]
  raw_counts_pooled: { contributing_study_count: 7,
    pooled_n_participants: "NOT_REPORTED", pooled_n_events: "NOT_REPORTED",
    person_time: "6.8 million person-years",
    follow_up_duration: "9.5 years (average)" }
value_status: SOURCE_REPORTED
provenance_tier: T1
pipeline_stage: STAGE3_EXTRACTED
evidence_role: { role: DIFFERENCE_MAKING, cited_by_recommendation_source: true }
source_location: { document: Reynolds2019_SupplementaryAppendix.md,
  table_or_figure: "Table C:1", page: "35-50" }
```

A fifth pattern is worth naming even without a full worked example:
Reynolds' independent mortality dose-response estimate would be
`evidence_id: WG01-EV-002`, same `claim_id`/outcome as example A, `role:
ALTERNATIVE_ESTIMATE`, `cited_by_recommendation_source: false` — validation
rule 7 forces that flag to exist the moment both records are filed.

---

## What happens after this

This revision incorporates: raw-count fields (§3, split by evidence shape
per Nic/GPT's agreed design), the `derivation_note` → `derivation_description`
rename, and the explicit Stage 3/5 boundary (§10). Per the agreed
sequencing: this document gets reviewed by Nic and GPT before any retrofit.
Once approved, the next step is the actual retrofit of the existing WG-01
corpus into this shape (the stress test proper), and only after that holds
up does this become the frozen Stage 3 schema for WG-02 onward.

**Reviewer:** Claude — 2026-09-15, revision 2.
