# Stage 3 Schema Specification — EvidenceRecord (design case: WG-01)

**Review status:** revision 3, incorporating GPT's second review (5
targeted fixes: `pipeline_stage` semantics, `extraction_status` for
qualitative records, tightened `SOURCE_DERIVED` definition, first-class
`recommendation_citation`, and `study_design`/`synthesis_design` split).
Still not retrofitted into the existing WG-01 corpus —
`stage3_evidence_hierarchy.py` stays a stub until this revision is
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
├── derived_from_source_id      optional; set only when extraction_status = SOURCE_DERIVED
├── field                       plain-language label, e.g. "all-cause mortality, high vs low WG intake"
├── source_wording               { text, is_verbatim_quote: bool }
├── source_location             see §6
├── study_classification        see §7
├── numerical_provenance        see §2/§3 — present only if record_type = QUANTITATIVE, absent (not null) otherwise
├── qualitative_content         present only if record_type = QUALITATIVE — free-text claim + a category tag (MECHANISTIC | LIMITATION | QUALITY_CAVEAT | OTHER)
├── extraction_status           see §2 — set ONCE per record, applies uniformly to QUANTITATIVE and QUALITATIVE records
├── provenance_tier             see §4
├── pipeline_stage              see §5 — fixed at creation, never changes
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

## 2. `extraction_status`

*(Renamed from `value_status` in this revision — see the note at the end of
this section for why.)*

Set **once per record**, and applies uniformly whether `record_type` is
QUANTITATIVE or QUALITATIVE:

```
SOURCE_REPORTED   the record's content (a number, or a qualitative
                  statement) appears in the cited source as-is — for a
                  QUANTITATIVE record, no arithmetic performed by anyone
                  in the citation chain beyond a straightforward unit
                  restatement; for a QUALITATIVE record, the statement is
                  directly present in the source (verbatim or a faithful
                  paraphrase), not synthesized by the pipeline.

SOURCE_DERIVED    the immediate source computed/transformed this value
                  from another source's reported value. Requires
                  derived_from_source_id and a one-line
                  derivation_description.

                  **Explicit rule, tightened this revision:**
                  SOURCE_DERIVED applies ONLY when the immediate reporting
                  source itself performed a calculation or transformation
                  on another source's reported value. It does NOT apply
                  merely because a source cites supporting literature.
                  "DGA derived this number from Reynolds via a stated
                  doubling method" is SOURCE_DERIVED. "DGA reports its own
                  number and cites Reynolds as supporting literature" is
                  SOURCE_REPORTED for DGA's number (with Reynolds' own
                  figure, if also filed, as its own separate
                  SOURCE_REPORTED record). The test: did THIS source do
                  arithmetic on someone else's number, or did it just
                  reference someone else's work?

MODEL_DERIVED     computed by this pipeline (an LLM judgment, a statistic
                  Stage 5 runs, an E-value we calculate). Reserved — NOT
                  permitted on any record living under corpus/ (see §9,
                  §10). Its only job is marking where the architecture's
                  boundary is; it should never actually appear in the
                  corpus.

NOT_REPORTED      the source was checked and does not state this value or
                  statement. Still requires a source_location (see §6) —
                  a claim of absence is itself an extraction result, not a
                  default. Applies the same way to a QUALITATIVE record:
                  e.g. "does the source specify whether this mechanism is
                  whole-grain-specific?" — if checked and not discussed,
                  that's a NOT_REPORTED qualitative record, not a blank.
```

Worked split, using material already in the record: Hu's mortality RR is
`SOURCE_REPORTED`. The DGA appendix's 24% per-30g T2D figure is
`SOURCE_DERIVED` (from Reynolds' per-15g RR). The serving-to-gram
conversion is `NOT_REPORTED` (confirmed absent across five sources, not
merely unfound). The mechanistic-pathway quote (p.179 of the DGA appendix)
is `SOURCE_REPORTED` — it's a qualitative statement, but it's directly and
verbatim present in the source, which `extraction_status` can now say
cleanly.

**Why the rename, and why `NOT_APPLICABLE` is gone:** revision 2 kept
`value_status` framed around "the primary reported estimate" and added a
`NOT_APPLICABLE` value specifically to route QUALITATIVE records around
that framing. That was a workaround, not a fix — it threw away real
information (a qualitative record can genuinely be "verbatim in the
source" vs. "checked for, not discussed," which are different facts worth
recording, not one collapsed `NOT_APPLICABLE` bucket). `extraction_status`
with four values, applied uniformly, says everything `value_status` +
`NOT_APPLICABLE` said, with no lost distinctions and one fewer enum value.

---

## 3. Raw-count fields in `numerical_provenance`

The rule governing all of it: **only populate a field when the immediate
source explicitly reports it. Never reconstruct a raw count from other
reported values, even when the arithmetic is trivial** (e.g. never
back-computing `sample_size_comparator` from `sample_size_total −
sample_size_intervention`). The corpus is an extraction layer, not a
calculation layer — that reduction is Stage 5's job, once it exists, using
inputs Stage 3 already made explicit.

**Two shapes, not one — keyed off `synthesis_design` (§7), not
`study_design`.** WG-01's actual evidence is overwhelmingly pooled
meta-analyses of cohort studies (dose-response and high-vs-low-quantile
estimates across many contributing studies), not two-arm trials. Forcing
every record through an RCT-shaped field set (`sample_size_intervention` /
`sample_size_comparator`) would mark those fields `NOT_REPORTED` on nearly
every WG-01 record for a reason that has nothing to do with the source
under-reporting — the two-arm shape is simply the wrong fit. Revision 2
keyed shape selection off `study_design` directly (using a
`cohort-meta-analysis` value), which conflated study design with synthesis
method — see §7 for why that's now split. The shape is keyed off
`synthesis_design` instead: **only the applicable shape's sub-object is
present on the record; the other is omitted entirely, not present with
`NOT_REPORTED` values.**

```
study_classification.synthesis_design = none
    → numerical_provenance.raw_counts_two_arm
        ├── sample_size_total
        ├── sample_size_intervention
        ├── sample_size_comparator
        ├── events_total
        ├── events_intervention
        ├── events_comparator
        ├── person_time
        └── follow_up_duration

study_classification.synthesis_design ∈ { meta_analysis,
  systematic_review, umbrella_review }
    → numerical_provenance.raw_counts_pooled
        ├── contributing_study_count
        ├── pooled_n_participants
        ├── pooled_n_events
        ├── person_time
        └── follow_up_duration
```

`narrative`-design records don't carry raw counts at all, and typically
pair with `record_type: QUALITATIVE`.

Within whichever sub-object applies, an individual field is either
populated with the value the source reports, or set to the literal string
`"NOT_REPORTED"` — no separate per-field status enum. `extraction_status`
(§2) still governs the record as a whole; these sentinel values are enough
for sub-fields.

**Worked example, real WG-01 numbers:** Reynolds' CRC high-vs-low pooled
estimate (7 studies, 6.8 million person-years, 9.5 y average follow-up) has
`study_design: cohort`, `synthesis_design: meta_analysis`, so it gets
`raw_counts_pooled`: `contributing_study_count: 7`, `person_time: "6.8
million person-years"`, `follow_up_duration: "9.5 years (average)"`, and
`pooled_n_participants` / `pooled_n_events`: `"NOT_REPORTED"` — Table C:1
gives person-years and study count but not a pooled participant or event
count, and that's a fact about the table, not a gap in this extraction.

---

## 4. `provenance_tier`

**Unchanged from the existing corpus convention** — `T1` primary-verified,
`T2` secondary-sourced, `STRUCTURE` structure-inferred — kept as its own
field rather than folded into `extraction_status` (rejecting the `[T1-D]`
composite-tag idea, per the "independent dimensions" framing both
reviewers converged on). Tier answers *how directly did the pipeline
verify this*; `extraction_status` answers *was arithmetic performed, and
by whom, and was the content present at all*. Orthogonal axes; no
composite tag needed.

| | SOURCE_REPORTED | SOURCE_DERIVED |
|---|---|---|
| **T1** | Hu's mortality RR — read directly from the supplied PDF | DGA appendix's 24% T2D figure — appendix authors' own disclosed harmonization, read directly |
| **T2** | A number inherited from a prior session's doc, not independently re-opened this pass | (no current example — would be a secondhand report of someone else's harmonization) |

---

## 5. `pipeline_stage`

**Redefined this revision.** Revision 2 described this as moving forward
(2→3→4→5→6) on a single record. That conflicts with §9's rule that
`AppraisalRecord`s reference `EvidenceRecord`s rather than editing them in
place — if an `EvidenceRecord` is never touched again after Stage 3 creates
it, nothing ever actually advances its `pipeline_stage`, so "moves forward"
was describing a mechanism that doesn't exist.

**Fixed instead:** `pipeline_stage` marks which stage *produced* a given
record, set once at creation and never changed. Each record type has
exactly one valid value:

```
STAGE2_ACQUIRED               a Source record (corpus/01_sources/) — a
                               source is collected/verified; no
                               EvidenceRecord built from it yet
STAGE3_EXTRACTED              every EvidenceRecord, always — its shape is
                               set by extraction: classification,
                               extraction_status, provenance_tier
STAGE4_APPRAISED              every AppraisalRecord, always (§9) — a
                               framework judgment the pipeline itself made
STAGE5_STATISTICALLY_EVALUATED   whatever record type Stage 5 eventually
                                  produces, once designed (§10)
STAGE6_GAP_FLAGGED            whatever record type Stage 6 produces
```

An `EvidenceRecord` is downstream-appraised by *other records being
created that reference it* (an `AppraisalRecord`, later a Stage 5 output),
never by its own `pipeline_stage` field changing. This makes "Stage 4
appraised this evidence" a fact you find by querying for `AppraisalRecord`s
whose `references` includes this `evidence_id`, not by reading a field on
the `EvidenceRecord` itself — which is also just a restatement of §9's
"reference, don't annotate in place" rule, now made consistent with this
field instead of contradicting it.

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

Required on every record regardless of `extraction_status` — including
`NOT_REPORTED`, where it proves the absence was checked in a specific place
rather than assumed.

---

## 7. Study / outcome / exposure fields (evidence classification)

**`study_design` and `synthesis_design` split this revision.** Revision 2
had a single `study_design` enum that mixed `RCT` / `cohort` (properties of
the underlying studies) with `cohort-meta-analysis` / `umbrella-review`
(properties of how those studies were combined) — meaning a cohort
meta-analysis was simultaneously "a cohort" and "a meta-analysis," which a
flat enum can't express. This is exactly the Reynolds/Hu case: both are
meta-analyses *of* cohort studies, and the flat enum forced a compound
value instead of two clean, independent facts.

```
study_classification
├── study_design         RCT | cohort | case-control | nested-case-control
│                         | narrative
├── synthesis_design      none | meta_analysis | systematic_review
│                         | umbrella_review
├── population
├── exposure
├── comparator
├── outcome
├── effect_measure        RR | HR | OR | MD | SMD | qualitative
└── follow_up             { extraction_status, value } — same
                          NOT_REPORTED semantics as §2

evidence_role
├── role                  DIFFERENCE_MAKING | MECHANISTIC | QUALITY_CAVEAT
│                         | ALTERNATIVE_ESTIMATE
└── recommendation_citation   see below — REQUIRED whenever role is
                              DIFFERENCE_MAKING or ALTERNATIVE_ESTIMATE
```

Worked reclassification: Hu's and Reynolds' whole-grain pooled estimates
are both `study_design: cohort`, `synthesis_design: meta_analysis`. A
single un-pooled cohort study (none exists yet in WG-01, but the shape
should hold up when one appears) would be `study_design: cohort`,
`synthesis_design: none` — and would then use the two-arm raw-count shape
(§3), correctly, since there's nothing pooled about it.

**`recommendation_citation` — upgraded from a boolean this revision.**
Revision 2's `cited_by_recommendation_source` was a boolean, validated only
"whenever two or more EvidenceRecords share a claim_id + outcome pair" —
a condition that depends on scanning other records rather than being a
fact about this one. Replaced with an explicit three-way relationship,
required unconditionally whenever `role` is `DIFFERENCE_MAKING` or
`ALTERNATIVE_ESTIMATE` (no cross-record condition needed):

```
recommendation_citation:
    CITED_DIRECTLY     this record's number is what the recommendation's
                        own evidence table/appendix cites and rests on.
    CITED_INDIRECTLY    referenced by the recommendation source as
                        supporting/background material, but not the
                        number actually tabulated.
    NOT_CITED           an evidence-relevant estimate the recommendation's
                        own evidence chain does not reference at all —
                        surfaced by this audit, not by the source.
```

This is the fix for the competing-estimates case already sitting in the
record: Reynolds independently reports his own whole-grain mortality
dose-response (RR converting to ~12% per 30g), a different number from
Hu's 6% that the DGA appendix actually cites for that outcome. Hu's record
gets `recommendation_citation: CITED_DIRECTLY`; Reynolds' independent
estimate gets `NOT_CITED` and its own `evidence_role.role:
ALTERNATIVE_ESTIMATE`. Making this a first-class field (rather than a
boolean inferred from context) is also what makes a claim-level view like

```
DGA claim
   ├── Evidence A — CITED_DIRECTLY
   ├── Evidence B — CITED_INDIRECTLY
   └── Evidence C — NOT_CITED (alternative)
```

queryable directly from the corpus, rather than requiring a reader to
reconstruct it from role tags and prose.

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
classifies — study design, synthesis design, exposure, outcome, evidence
role — but renders no new judgment of adequacy.

**Stage 4 does:** apply GRADE, Bradford Hill, E-value, QBA, ROBIS, AMSTAR-2
as the *pipeline's own* appraisal, via a separate record type:

```
AppraisalRecord
├── appraisal_id
├── framework            GRADE | Bradford-Hill | E-value | QBA | ROBIS | AMSTAR-2
├── references            [evidence_id, ...] — one or more EvidenceRecords
│                         this appraisal judges; NEVER edits them in place
├── judgment
├── extraction_status     MODEL_DERIVED by definition — this is the
│                         pipeline computing something new
├── pipeline_stage         STAGE4_APPRAISED, always (§5)
└── reviewer / date
```

Appraisal referencing evidence records rather than annotating them in place
is what enforces "I pull numbers from PDFs, I don't perform calculations"
as a fact about the data model, not a convention a reviewer has to
remember. An `AppraisalRecord` is `MODEL_DERIVED` by construction, which §2
and §10 say can't exist under `corpus/` — so `AppraisalRecord`s belong in
`analysis/`, never in the extraction corpus itself. Finding "was this
evidence appraised, and how" means querying `AppraisalRecord.references`
for this `evidence_id` — never reading a mutated field on the
`EvidenceRecord` (§5).

---

## 10. Stage 3 / Stage 5 boundary

The boundary is made explicit without designing Stage 5's statistical
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

1. `extraction_status = SOURCE_DERIVED` ⟹ `derived_from_source_id` is
   required and must resolve to an existing `source_id`, and
   `derivation_description` is required. `SOURCE_DERIVED` applies only
   when the immediate source itself performed the transformation (§2) —
   citing supporting literature is not derivation.
2. `extraction_status = MODEL_DERIVED` ⟹ the record is rejected under
   `corpus/` at ingestion; it belongs under `analysis/` as an
   `AppraisalRecord` or Stage-5 output.
3. `record_type = QUALITATIVE` ⟹ `numerical_provenance` must be entirely
   absent from the record, not present-with-nulls.
4. `extraction_status = NOT_REPORTED` ⟹ `source_location` is still
   required, regardless of `record_type`.
5. `provenance_tier` and `extraction_status` are set independently; no
   combination is disallowed, and no composite tag (`[T1-D]`) is used in
   place of the two fields.
6. Every `EvidenceRecord.claim_id` resolves to a leaf sub-claim, never a
   bundle claim with multiple independently-evidenced elements.
7. `evidence_role.recommendation_citation` is required whenever
   `evidence_role.role` is `DIFFERENCE_MAKING` or `ALTERNATIVE_ESTIMATE` —
   unconditionally, not only when another record happens to share the same
   `claim_id` + outcome.
8. An `AppraisalRecord` may only reference existing `evidence_id`s; it
   never carries its own free-standing numeric extraction.
9. A raw-count field (§3) is populated only when the immediate source
   explicitly reports it; it is never reconstructed from other reported
   values, even when the arithmetic is trivial.
10. Exactly one of `raw_counts_two_arm` / `raw_counts_pooled` is present on
    a `QUANTITATIVE` record, selected by
    `study_classification.synthesis_design` (§3); the other is omitted
    entirely — never present with `"NOT_REPORTED"` values standing in for
    a structurally inapplicable field set.
11. `numerical_provenance` never contains an analytical instruction or
    downstream-model directive (e.g. `recommended_model`,
    `transform_to_log_rr`, `calculate_NNT`) — Stage 3 records what the
    evidence contains, never what a later stage should do with it.
12. `pipeline_stage` is set once at record creation and never changed
    afterward (§5); a record's downstream appraisal is discovered by
    querying other records that reference its `evidence_id`, not by a
    field mutation on the record itself.

---

## 12. Miniature WG-01 examples

**A — clean, `SOURCE_REPORTED`, pooled shape:**

```
evidence_id: WG01-EV-001
claim_id: WG-01a
record_type: QUANTITATIVE
source_id: SRC-HU-2023
field: "all-cause mortality, high vs low whole-grain intake"
study_classification: { study_design: cohort, synthesis_design: meta_analysis,
  population: adults, exposure: high WG intake, comparator: low WG intake,
  outcome: all-cause mortality, effect_measure: RR }
numerical_provenance:
  estimate: 0.83
  CI: [0.78, 0.89]
  raw_counts_pooled: { contributing_study_count: "NOT_REPORTED",
    pooled_n_participants: "NOT_REPORTED", pooled_n_events: "NOT_REPORTED",
    person_time: "NOT_REPORTED", follow_up_duration: "5.4-26 y (range across
    contributing studies)" }
extraction_status: SOURCE_REPORTED
provenance_tier: T1
pipeline_stage: STAGE3_EXTRACTED
quality_signals: [{ signal_type: NOS, value: "7.74/9 (mean)",
  attributed_to: Hu 2023, provenance_tier: T1, source_location: p.151 }]
evidence_role: { role: DIFFERENCE_MAKING, recommendation_citation: CITED_DIRECTLY }
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
extraction_status: SOURCE_DERIVED
derivation_description: "DGA appendix doubled Reynolds' per-15g percent
  reduction (1 − 0.88) × 2 = 24%, on a stated assumption of linearity — not
  a fresh re-derivation by this pipeline."
provenance_tier: T1
pipeline_stage: STAGE3_EXTRACTED
evidence_role: { role: DIFFERENCE_MAKING, recommendation_citation: CITED_DIRECTLY }
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
extraction_status: SOURCE_REPORTED
provenance_tier: T1
pipeline_stage: STAGE3_EXTRACTED
evidence_role: { role: MECHANISTIC }
source_location: { document: "Scientific Report Appendices_FINAL_1.28.26.md",
  page: 179 }
```

(Note: `evidence_role.recommendation_citation` is omitted here — rule 7
only requires it for `DIFFERENCE_MAKING` / `ALTERNATIVE_ESTIMATE` roles; a
`MECHANISTIC` record doesn't compete to be "the cited number" for an
outcome, so the field doesn't apply.)

**D — pooled shape with raw counts actually populated:**

```
evidence_id: WG01-EV-011
claim_id: WG-01a
record_type: QUANTITATIVE
source_id: SRC-REYNOLDS-2019-APPENDIX
field: "colorectal cancer, whole grain, high vs low (Reynolds appendix)"
study_classification: { study_design: cohort, synthesis_design: meta_analysis,
  population: adults, exposure: high WG intake, comparator: low WG intake,
  outcome: colorectal cancer incidence, effect_measure: RR }
numerical_provenance:
  estimate: 0.87
  CI: [0.79, 0.96]
  raw_counts_pooled: { contributing_study_count: 7,
    pooled_n_participants: "NOT_REPORTED", pooled_n_events: "NOT_REPORTED",
    person_time: "6.8 million person-years",
    follow_up_duration: "9.5 years (average)" }
extraction_status: SOURCE_REPORTED
provenance_tier: T1
pipeline_stage: STAGE3_EXTRACTED
evidence_role: { role: DIFFERENCE_MAKING, recommendation_citation: CITED_DIRECTLY }
source_location: { document: Reynolds2019_SupplementaryAppendix.md,
  table_or_figure: "Table C:1", page: "35-50" }
```

A fifth pattern is worth naming even without a full worked example:
Reynolds' independent mortality dose-response estimate would be
`evidence_id: WG01-EV-002`, same `claim_id`/outcome as example A, `role:
ALTERNATIVE_ESTIMATE`, `recommendation_citation: NOT_CITED` — rule 7 forces
that field to exist the moment the record is filed, regardless of whether
a competing record exists yet.

---

## What happens after this

This revision incorporates GPT's second review in full: `pipeline_stage`
redefined as an immutable creation tag, `extraction_status` replacing
`value_status` (dropping `NOT_APPLICABLE`) so qualitative records get real
SOURCE_REPORTED/NOT_REPORTED semantics, an explicit test for
`SOURCE_DERIVED` vs. merely citing supporting literature,
`recommendation_citation` as a first-class three-way relationship
replacing the boolean, and `study_design`/`synthesis_design` split so a
cohort meta-analysis doesn't have to be squeezed into one compound enum
value. Per GPT's own framing: none of these required redesigning the
architecture, and the big decisions from revision 1/2 stand — two-arm vs.
pooled raw counts, source-reported-only population, explicit derivation
provenance, source-reported quality kept separate from the pipeline's own
appraisal, Stage 4 and Stage 5 both consuming `EvidenceRecord`s without
mutating them, leaf claims over bundle claims, and structural inapplicability
distinguished from genuine absence.

Per the agreed sequencing: freeze this draft, then run the WG-01 stress
test — not to look for reasons to reject the schema, but because WG-01
contains exactly the edge cases (competing estimates, pooled vs. two-arm
evidence, qualitative mechanistic claims, disclosed harmonization) that
tell us whether these decisions hold up against real data rather than
against three curated examples.

**Reviewer:** Claude — 2026-09-15, revision 3.
