# Stage 3 Schema Specification — EvidenceRecord (design case: WG-01)

**Review status:** specification (§1-§11) FROZEN at revision 7
(2026-09-17); revision 8 (2026-09-17) is a post-freeze documentation-only
correction to §12's worked examples, described near the end of this
document -- no rule or field requirement changed. Revision 4 was
reviewed and judged ready for freeze, then reopened after scoping and
then building `stage3_evidence_hierarchy.py` (the Stage 3 validator)
surfaced real gaps in rules 10 and 7, plus a documentation gap in §1,
described below.
This is a deliberate reopening, not a freeze failure: the freeze was
never written into this document (agreed to hold that until the
validator landed), and finding this kind of gap by testing the schema
against an implementation is exactly what the freeze discussion
anticipated as a legitimate trigger to reopen. In draft, revised a
second time after reviewing rev-3's actual field lists directly rather
than discussing the fix in the abstract. Revision 3 was retrofitted
against the WG-01 corpus
(28 records) and survived three independent reconciliation passes with zero
unresolved source/value/location discrepancies — but that stress test
surfaced a real schema gap: §3's two raw-count shapes (`raw_counts_two_arm`
/ `raw_counts_pooled`) were selected by
`study_classification.synthesis_design`, which broke on Reynolds' RCT
meta-analyses (`synthesis_design: meta_analysis`, i.e. "pooled") that
report arm-level totals rather than a single pooled N. "Was this pooled"
and "how are the counts reported in this source" turned out to be
independent facts. The first rev-4 draft replaced both shapes with one
unified `raw_counts` block plus an explicit `reporting_shape` enum; that
was revised again in favor of a smaller fix: keep two named objects,
decouple the choice between them from `study_design`/`synthesis_design`,
and let the object's presence — not a separate tag — declare the shape.
`raw_counts_two_arm` is renamed `raw_counts_by_group` (removing the false
"single two-arm study" implication that caused the original problem), and
`contributing_study_count` now lives in both objects instead of only
`raw_counts_pooled`, since the rename removes the reason it couldn't
before. §3 changes, as do validation rules 10 and 11 in §11 (a new rule 11
requires `structure_note` on `raw_counts_other` records, which renumbers
the former rules 11/12 to 12/13); §2, §4–§10 are unchanged from revision 3.
The four Reynolds RCT records that motivated this revision
(WG01-EV-018/019/020/021) have been migrated to raw_counts_by_group, and
WG01-EV-025/026 (Schlesinger) have been migrated to raw_counts_pooled -- a
reclassification, not a rename, since those two report a single combined total
rather than a group split; both correctly omit contributing_study_count, since
synthesis_design: none on both. §12's worked examples are synced. Every
remaining WG-01 record uses raw_counts_pooled; a further review pass (below)
renamed that object's own fields, which now touches these records too. No
live raw_counts_two_arm reference remains anywhere in the corpus; full audit
trail in corpus/stage3_evidence_records/WG-01.md §6.

**Third-pass refinements (2026-09-15, before freeze):** a further schema
review surfaced four smaller gaps, all documentation/naming fixes, no
further redesign. `raw_counts_pooled`'s field names
(`pooled_n_participants`/`pooled_n_events`) still implied a pooled
synthesis even after the object's own meaning was clarified in prose —
renamed to `combined_n_participants`/`combined_n_events`, applied to all
twelve WG-01 records using this object, not only the two reclassified
Schlesinger records, since none of their reported values change, only
the field names. `raw_counts_other` previously specified only its
`structure_note` requirement with no other fields at all; it now also has
`reported_values` (a verbatim transcription of the source's own labeled
counts) and a conditional `contributing_study_count`, resolving the
previously-unaddressed case of a `raw_counts_other` record that is
itself a synthesis. The two-question escalation test's second question
now explicitly reads "two named comparison groups *relevant to this
record's specific estimate*," so a source table with more than two
groups (e.g. four exposure quartiles) doesn't force `raw_counts_other`
merely because groups beyond the two this estimate uses also appear in
the table. Full detail in §3 and §11; corpus-wide field-rename audit
trail in `corpus/stage3_evidence_records/WG-01.md` §6.

**Revision 5 (2026-09-16): rule 10's scope clarified after implementation
surfaced a real gap.** Scoping `stage3_evidence_hierarchy.py` against the
actual WG-01 corpus (not just reading the schema) found 8 of 28
`QUANTITATIVE` records with zero raw-count objects at all — a real rule
10 violation, not a hypothetical one. Two of those eight (WG01-EV-027,
WG01-EV-028) turned out to be correctly exempt: both have
`extraction_status: NOT_REPORTED`, meaning the source states no value at
all for that record — there is no estimate for a raw-count object to
attach to, and rule 10 never said this case was different from a record
that has a real, reported or derived number. That was a genuine
underspecification, not a corpus error: rule 10 now states explicitly
that its exactly-one-object requirement applies only when
`extraction_status` is `SOURCE_REPORTED` or `SOURCE_DERIVED`. The
remaining six records this same scan found (WG01-EV-002/005/007/008/
010/013) are a real corpus-side gap, not a schema gap — their
`extraction_status` is `SOURCE_REPORTED`/`SOURCE_DERIVED`, so rule 10
does apply to them, and they are missing a raw-count object rule 10
already required.

**Revision 6 (2026-09-17): rule 7's scope clarified, for the same reason
and in the same shape as rule 10's.** Building the Stage 3 validator (not
just scoping it) and running it against WG-01 found two records —
WG01-EV-027, WG01-EV-028 — with `role: DIFFERENCE_MAKING` and no
`evidence_role.recommendation_citation`, which rule 7 as written requires
unconditionally. Both are the confirmed-absent gram-equivalent records:
`extraction_status: NOT_REPORTED`, no estimate at all.
`recommendation_citation` asks whether *this record's number* is what the
recommendation's evidence table cites — a question that presupposes a
number exists to be cited or not. A `NOT_REPORTED` record has none, so the
field has nothing to describe; populating it with `NOT_CITED` would
misrepresent a confirmed absence as a surfaced-but-ignored estimate, the
same category of error rule 10's fix was written to avoid for raw counts.
Rule 7 now states explicitly that its requirement applies only when
`extraction_status` is `SOURCE_REPORTED` or `SOURCE_DERIVED` — identical
carve-out condition to rule 10's, same underlying reason. No corpus action
needed: WG01-EV-027/028 already correctly omit `recommendation_citation`;
this revision only changes rule 7's own text to match what the corpus
already does. Full detail in `corpus/stage3_evidence_records/WG-01.md` §9.

**Revision 7 (2026-09-17): §1's field tree now says explicitly what the
corpus already does for `study_classification`.** Building the Stage 3
validator found that `study_classification` was listed in §1's field tree
with no "present only if..." qualifier -- unlike `numerical_provenance` and
`qualitative_content`, which both have one -- even though all 4 WG-01
`QUALITATIVE` records (and the schema's own §12 example C) have always
omitted it entirely, across three independent reconciliation passes. This
was a real documentation gap, not a corpus defect: the corpus already got
this right consistently: `study_classification` required for
`QUANTITATIVE`, absent for `QUALITATIVE`, never populated with nulls on a
`QUALITATIVE` record. §1's tree now says so explicitly, in the same
"present only if / absent (not null) otherwise" phrasing already used for
`numerical_provenance`. No corpus action needed -- this only makes the
schema doc match what every WG-01 record has always done.

**Freeze declaration (2026-09-17):** with rev-7 landed, the accumulated
work split into four commits matching this document's own revision
history (rev-5 mechanical retrofit, Figure-2 primary-source pass,
validator build + rule-3 fix + rev-6, rev-7), and
`stage3_evidence_hierarchy.py` run five times against the full WG-01
corpus with identical results every run (28 records, 0 errors, 0 notes,
exit 0) -- Nic declared Stage 3 frozen. Freezing here means: the schema
(§1-§13) and the WG-01 corpus it validates are both in a state the
validator confirms clean, and further changes to the specification
itself are a deliberate reopening, not a continuation of this design
pass. Stage 4 work can proceed against this as a stable foundation.

**Revision 8 (2026-09-17): §12's worked examples re-synced to the frozen
corpus.** A post-freeze check found that all five worked examples in §12
had drifted from the real WG-01 records they name -- see §12's own note
for the full per-example detail. This is a documentation-accuracy
correction, not a reopening of the specification: no rule, field
requirement, or validator behavior changed, only illustration. Filed as
revision 8, one level below the frozen §1-§11 specification, so the
freeze declaration above still accurately describes the specification
itself.

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
├── source_wording               optional; { text, is_verbatim_quote: bool } —
│                                populate only when the source's exact phrasing
│                                carries evidentiary weight (see note below)
├── source_location             see §6
├── study_classification        see §7 — present only if record_type = QUANTITATIVE, absent (not null) otherwise
├── numerical_provenance        see §2/§3 — present only if record_type = QUANTITATIVE, absent (not null) otherwise
├── qualitative_content         present only if record_type = QUALITATIVE — free-text claim + a category tag (MECHANISTIC | LIMITATION | QUALITY_CAVEAT | OTHER)
├── extraction_status           see §2 — set ONCE per record, applies uniformly to QUANTITATIVE and QUALITATIVE records
├── provenance_tier             see §4
├── pipeline_stage              see §5 — fixed at creation, never changes
├── quality_signals             see §8 — 0 or more, each independently tiered
├── evidence_role               see §7
├── reviewer                     set once at record creation, like pipeline_stage —
│                                who did the Stage 3 extraction, never updated afterward
└── review_date                  set once at record creation — when, not a running
                                verification log (see note below)
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

**On `source_wording` and `reviewer`/`review_date` — clarified this
revision, not redesigned:** scoping the Stage 3 validator against WG-01
found zero of the 28 records populate any of these three fields, despite
all three being listed above without a "present only if..." qualifier.
Rather than retrofitting 28 records with fields nothing has needed in
three independent reconciliation passes, `source_wording` is now
explicitly optional — the verbatim-vs-paraphrase distinction it was meant
to capture has been handled the whole time by the italic prose notes that
already follow most records, and that pattern is the accepted mechanism
going forward, not a workaround. `reviewer`/`review_date` are kept, but
their semantics are now explicit: they record who/when a record was
*originally extracted*, set once at creation exactly like `pipeline_stage`
(§5) — not a running "last independently verified" log. A record that is
later re-touched (a field rename, a reclassification, an independent
re-verification against the primary source) gets that fact recorded in
the corpus file's own dated audit-trail section, the same way every prior
pass in this document already has — `reviewer`/`review_date` are not a
substitute for that, and are never updated to reflect a later pass.

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
back-computing one group's size from `total −` the other group's). The
corpus is an extraction layer, not a calculation layer — that reduction is
Stage 5's job, once it exists, using inputs Stage 3 already made explicit.

**Revision 4 (revised a second time, after reviewing the actual rev-3 text
directly rather than discussing the fix in the abstract): keep two named
raw-count objects, but decouple the choice between them from
`study_design`/`synthesis_design`, and fix the name that caused the
Reynolds problem.** Revision 3 selected between `raw_counts_two_arm` and
`raw_counts_pooled` using `study_classification.synthesis_design` as a
proxy for "how are this record's counts reported" — treating "was this a
synthesis" and "does this source table report one total or a split" as
the same fact. They aren't: Reynolds' whole-grain RCT meta-analyses are
pooled syntheses (`synthesis_design: meta_analysis`, 11+ contributing
RCTs) whose source table reports arm-level totals, not a single pooled N.
`study_design`, `synthesis_design`, and how *this record's* counts happen
to be reported in *this* source table are three independent facts, and
only the third determines raw-count shape.

The name `raw_counts_two_arm` was itself part of the problem: it reads as
"this record represents one two-arm study," which is false for an
11-RCT pooled meta-analysis reported group-wise. Renamed to
`raw_counts_by_group` — a name that describes the reporting shape (counts
split by comparison group) without asserting anything about how many
studies produced those counts.

The exclusivity rule survives unchanged: **exactly one of
`raw_counts_by_group` / `raw_counts_pooled` is present on a
`QUANTITATIVE` record; the other is omitted entirely.** No separate shape
tag is needed — the presence of the object *is* the declaration, and an
explicit enum alongside it would just duplicate that information under a
second name.

```
numerical_provenance.raw_counts_by_group          (source reports counts split by group)
├── contributing_study_count
├── group_1                    maps to study_classification.exposure
├── group_2                    maps to study_classification.comparator
├── events_group_1
├── events_group_2
├── person_time
└── follow_up_duration

numerical_provenance.raw_counts_pooled            (source reports one combined figure)
├── contributing_study_count
├── combined_n_participants
├── combined_n_events
├── person_time
└── follow_up_duration

numerical_provenance.raw_counts_other             (neither of the above fits -- rare)
├── structure_note             required; free text, see below
├── reported_values            source's own labeled counts, verbatim
├── contributing_study_count   present only when synthesis_design != none
├── person_time
└── follow_up_duration
```

- **`raw_counts_by_group`** — Reynolds' RCT tables are the canonical case:
  11 contributing RCTs, `group_1: 498`, `group_2: 421`, no single pooled N
  reported anywhere in the table. `group_1` always corresponds to
  `study_classification.exposure`, `group_2` always to `comparator` —
  fixed by that field, never by which arm "sounds like" the intervention.
  Using `group_1`/`group_2` rather than `sample_size_intervention`/
  `comparator` is deliberate: a non-randomized cohort's exposure-quartile
  split belongs in this same shape (its counts are still reported
  group-wise), and calling a cohort's high/low-intake groups an
  "intervention" and "comparator" would misdescribe a study that assigned
  nothing.
- **`raw_counts_pooled`** — the source reports one combined figure, not
  a group split. Hu's and Schlesinger's cohort meta-analyses are the
  synthesis case (a pooled participant/event count across contributing
  studies); WG01-EV-025/026 (single-study Schlesinger cohorts,
  `synthesis_design: none`) are the non-synthesis case — one study
  reporting one combined total, with no group comparison in the table at
  all. Both belong here for the same reason: the source table gives one
  number, not two.
- **`raw_counts_other`** — a strict, narrow escape hatch, not a place
  for an extractor to put a record it merely isn't sure how to classify.
  It means: *the source reports numerical count information, but the
  reported structure genuinely cannot be represented as either a pooled
  total or two named comparison groups* (e.g. three or more named groups
  with no natural pairwise reduction, or a count structure with no group
  concept at all). Its structure (tree above): `structure_note`
  (required), `reported_values` (the source's own labeled counts,
  transcribed verbatim as `{label: value}` pairs using the source's own
  group or category names — never relabeled into `group_1`/`group_2` or
  `combined_n_participants`/`combined_n_events` terminology, since forcing
  that relabeling is exactly what this object exists to avoid),
  `contributing_study_count` (present only when `synthesis_design !=
  none`, same rule as the other two objects — rule 10), `person_time`,
  and `follow_up_duration`. Apply this two-question test before reaching
  for `raw_counts_other`: (1) *can the source's count structure be read as
  one combined figure?* — if yes, `raw_counts_pooled`, regardless of
  whether a synthesis occurred. (2) *can it be read as exactly two named
  comparison groups relevant to this record's specific estimate?* — if
  yes, `raw_counts_by_group`, regardless of what the source calls those
  groups (arms, quantiles collapsed to high/low, exposed/unexposed), and
  regardless of whether the source table also reports additional groups
  that this particular estimate doesn't use (e.g. a table with four
  exposure quartiles, where this record represents a high-vs-low
  comparison built from only two of them — the other two quartiles being
  present in the table doesn't push this record into `raw_counts_other`).
  `raw_counts_other` is for a source that answers no to both — not for a
  total or a two-way split that merely doesn't map onto an existing field
  name. Two extractors reading the same source table for the same
  record's estimate should reach the same answer to (1) and (2); if they
  wouldn't, that is a sign the source needs re-reading, not a sign
  `raw_counts_other` is the safe default. `structure_note` is mandatory;
  a record without one fails validation the same way a `SOURCE_DERIVED`
  record without `derivation_description` does (§11 rule 1). This is
  deliberate friction: without a mandatory explanation,
  `raw_counts_other` would quietly become the place where difficult
  extraction decisions go to disappear instead of getting resolved. Not
  observed in WG-01 to date.

**A note on the name `raw_counts_pooled`: it means "the source table
reports one combined, non-split figure," not "the estimate is a pooled
synthesis."** These are different facts, and rev-4 exists precisely
because revision 3 conflated them. `contributing_study_count`'s presence
is gated on `synthesis_design != none` (below), never on which raw-count
object is used — the two are independent axes. A meta-analysis whose
source table reports arm-level totals uses `raw_counts_by_group` despite
being a pooled synthesis (Reynolds' RCT records above); a single-study
observational cohort whose source table reports one combined
participant/event count uses `raw_counts_pooled` despite having no
synthesis at all and `synthesis_design: none` (WG01-EV-025/026). The
object name describes the reporting shape of the immediate source table
— one figure vs. a figure split by group — never whether a meta-analytic
pooling operation actually happened. Do not infer `synthesis_design !=
none` from the presence of `raw_counts_pooled`, or infer `synthesis_design:
none` from its absence; check `study_classification.synthesis_design`
itself.

**`contributing_study_count` lives in both objects**, rather than only in
`raw_counts_pooled` as revision 3 had it — the rename to
`raw_counts_by_group` removes the reason it couldn't live there before
(nesting it inside a block literally named "two_arm" would have implied
single-study identity; "by_group" carries no such implication). It means
**the number of studies contributing to the specific estimate this record
represents**, when the immediate source states it — not the number of
studies in the source paper, the review, or an unrelated table in the
same document. Reynolds' four affected records report 11, 3, 27, and 6
respectively, for four different estimates in the same paper; that
specificity is the reason to keep the field per-record rather than
per-source. Populated (as `"NOT_REPORTED"` if a synthesis occurred but no
count is stated) whenever `synthesis_design` is not `none`; the field is
simply absent when `synthesis_design: none`, since there is nothing to
count.

**Not yet observed in WG-01, but anticipated: a source reporting both a
pooled total and a per-group split for the same estimate** (e.g. a table
stating total N = 919 alongside intervention N = 498 / comparator N =
421). **The canonical representation in that case is
`raw_counts_by_group`, not `raw_counts_pooled` — this is a deterministic
rule, not a per-extractor judgment call.** Without it, two extractors
could reasonably make opposite choices and both would technically satisfy
the exactly-one-object rule (§11 rule 10), which would make the corpus
inconsistent in exactly the way this revision is trying to eliminate. The
group-specific counts preserve strictly more structural information than
the grand total (a reader can always sum a split but can never un-sum a
total), which is the principle behind the priority, not just a tie-break.
The also-reported grand total is noted as a documented aside on the
record (in `field` or a comparable free-text note, never as a schema
field) — never add a total-style field to `raw_counts_by_group` to hold
it, and never populate `raw_counts_pooled`'s fields alongside
`raw_counts_by_group`'s as if the pooled figure were independently
reported. Either would violate the exactly-one-object rule and the
no-reconstruction rule respectively.

`narrative`-design records don't carry raw counts at all, and typically
pair with `record_type: QUALITATIVE`.

Within either object, an individual field is either populated with the
value the source reports, or set to the literal string `"NOT_REPORTED"`
— no separate per-field status enum. `extraction_status` (§2) still
governs the record as a whole; these sentinel values are enough for
sub-fields.

**Worked examples, real WG-01 numbers — same synthesis-design family, two
different reporting shapes, which is exactly the point this revision
fixes.** Reynolds' whole-grain RCT body-weight estimate — `study_design:
RCT`, `synthesis_design: meta_analysis`, a pooled synthesis of RCTs whose
source table reports arm-level totals, not a single N:

```
raw_counts_by_group: { contributing_study_count: 11, group_1: 498, group_2: 421,
  events_group_1: "NOT_REPORTED", events_group_2: "NOT_REPORTED",
  person_time: "NOT_REPORTED", follow_up_duration: "NOT_REPORTED" }
```

(Body weight is a continuous outcome, so the `events_*` fields have
nothing to report; consistent with §2's elimination of `NOT_APPLICABLE`
as a sentinel, that's recorded the same way an unreported value would
be — no second sentinel is needed.)

Reynolds' CRC high-vs-low pooled cohort estimate — also `synthesis_design:
meta_analysis`, but the source reports one pooled figure, not a group
split:

```
raw_counts_pooled: { contributing_study_count: 7, combined_n_participants: "NOT_REPORTED",
  combined_n_events: "NOT_REPORTED", person_time: "6.8 million person-years",
  follow_up_duration: "9.5 years (average)" }
```

Both are `synthesis_design: meta_analysis`; one uses `raw_counts_by_group`,
the other `raw_counts_pooled` — shape is a fact about the source table,
never about the study or synthesis design.

**Migration note (executed 2026-09-15, two passes):** the first pass
renamed `raw_counts_two_arm` to `raw_counts_by_group`; added
`contributing_study_count` to that object (it already existed on
`raw_counts_pooled`); and renamed `sample_size_intervention`/
`sample_size_comparator` to `group_1`/`group_2` (mapped per each record's
own `study_classification.exposure`/`comparator`, confirmed during
migration, not assumed — never a blind field-name swap). That pass
touched only the six records whose raw-count object changed —
WG01-EV-018/019/020/021 (renamed to `raw_counts_by_group`) and
WG01-EV-025/026 (reclassified to `raw_counts_pooled`, not merely
renamed, since those two report a single total rather than a group
split). A second pass, following further schema review, renamed
`raw_counts_pooled`'s own fields — `pooled_n_participants`/
`pooled_n_events` — to `combined_n_participants`/`combined_n_events`: the
old names still implied a pooled synthesis even for `synthesis_design:
none` records, undermining the object-level clarification made earlier in
this same review round. This second rename touches all twelve WG-01
records using `raw_counts_pooled`, not only the two from the first pass,
since every one of them used the old field names; no reported value
changes on any of them, only the field name, plus this document's own
§12 worked examples. Both passes' full audit trail, including the
two-record reclassification's reasoning, is in
`corpus/stage3_evidence_records/WG-01.md` §6.



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
   not only when another record happens to share the same `claim_id` +
   outcome. This requirement applies only when the record carries an
   actual reported or derived value — `extraction_status: SOURCE_REPORTED`
   or `SOURCE_DERIVED`. A record whose `extraction_status: NOT_REPORTED`
   carries no `recommendation_citation` — there is no estimate for the
   recommendation to have cited or not cited, and populating the field
   would misrepresent a confirmed absence as a surfaced-but-ignored
   estimate.
8. An `AppraisalRecord` may only reference existing `evidence_id`s; it
   never carries its own free-standing numeric extraction.
9. A raw-count field (§3) is populated only when the immediate source
   explicitly reports it; it is never reconstructed from other reported
   values, even when the arithmetic is trivial.
10. Exactly one of `raw_counts_by_group` / `raw_counts_pooled` / rarely
    `raw_counts_other` is present on a `QUANTITATIVE` record; the
    others are omitted entirely — never present with `"NOT_REPORTED"`
    values standing in for a structurally inapplicable object. Which
    object is present is itself the shape declaration; no separate tag
    duplicates it, and the choice is never made by `study_design` or
    `synthesis_design` (§3). `contributing_study_count` is present only
    when `synthesis_design != none`; when present (in any of
    `raw_counts_by_group`, `raw_counts_pooled`, or `raw_counts_other`),
    it records the number of studies contributing to this specific
    estimate, and may
    be `"NOT_REPORTED"` when the synthesis does not state the count. It
    is absent — not populated as `1` or any other value — when
    `synthesis_design: none`, since there is nothing to count. When a
    source reports both a pooled total and a per-group split for the
    same estimate, `raw_counts_by_group` is the canonical
    representation — deterministically, not by extractor judgment —
    with the also-reported total recorded only as a note on the record,
    never as a field on either object — see §3. This exactly-one-object
    requirement applies only when the record carries an actual reported
    or derived value — `extraction_status: SOURCE_REPORTED` or
    `SOURCE_DERIVED`. A record whose `extraction_status: NOT_REPORTED`
    (the source states no value at all, so `estimate` itself is
    `"NOT_REPORTED"`) carries no raw-count object of any kind — there is
    no estimate for a count to attach to, and populating one would
    misrepresent a confirmed absence as a partially-measured value.
11. `raw_counts_other`'s fields (§3) are `structure_note` (required),
    `reported_values`, `contributing_study_count` (present only when
    `synthesis_design != none`, same rule as rule 10), `person_time`, and
    `follow_up_duration`. `structure_note` is mandatory; a
    `raw_counts_other` record without one fails validation, the same way
    `SOURCE_DERIVED` without `derivation_description` does (rule 1).
    `raw_counts_other` is reserved for a reporting structure that
    genuinely fits neither `raw_counts_by_group` nor `raw_counts_pooled`
    under the two-question test in §3 — not for a record an extractor is
    merely unsure how to classify.
12. `numerical_provenance` never contains an analytical instruction or
    downstream-model directive (e.g. `recommended_model`,
    `transform_to_log_rr`, `calculate_NNT`) — Stage 3 records what the
    evidence contains, never what a later stage should do with it.
13. `pipeline_stage` is set once at record creation and never changed
    afterward (§5); a record's downstream appraisal is discovered by
    querying other records that reference its `evidence_id`, not by a
    field mutation on the record itself.

---

## 12. Miniature WG-01 examples

> **Re-synced to the frozen corpus (revision 8, 2026-09-17).** These are meant to be live mirrors of real WG-01 records, not independent illustrations, and drift between the two is itself a documentation defect. A check against the current corpus found five: example A's `raw_counts_pooled` and `quality_signals` were pre-correction values (the real record has verified participant/event counts and a corrected follow-up-duration note, plus a second quality signal); example B was still the pre-rev-5 shape entirely (no `study_classification`, no `raw_counts_pooled`, no `CI`, and a shorter `derivation_description`); example C still carried the `numerical_provenance: <absent...>` placeholder line the rule-3 fix deleted from the real record; example D had an extra `population` field the real record doesn't carry and was missing its `quality_signals` block, plus a stale page value (`"35-50"` vs. the real `35`); example E was missing the `(CORRECTED...)` field annotation and `quality_signals` block, and had a shorter `source_location.table_or_figure`. All five now match the current `corpus/stage3_evidence_records/WG-01.md` records they name field-for-field, except `reviewer`/`review_date` -- omitted here as in every example in this section, since they're bookkeeping metadata, not part of what each example illustrates. No rule or field requirement changed — this section is illustration, not specification; §1-§11 remain frozen at revision 7.

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
  raw_counts_pooled: { contributing_study_count: 13,
    combined_n_participants: 912293, combined_n_events: 106112,
    person_time: "NOT_REPORTED", follow_up_duration: "NOT_REPORTED (5.4-26y
    is the paper-wide range across ALL 68 studies/all outcomes, not
    confirmed mortality-specific -- corrected this pass; do not restate as
    mortality-specific)" }
extraction_status: SOURCE_REPORTED
provenance_tier: T1
pipeline_stage: STAGE3_EXTRACTED
quality_signals: [{ signal_type: NOS, value: "7.74/9 (mean)",
  attributed_to: Hu 2023, provenance_tier: T1, source_location: p.151 },
  { signal_type: NutriGrade, value: "High", attributed_to: Hu 2023,
  provenance_tier: T1, source_location: p.155 }]
evidence_role: { role: DIFFERENCE_MAKING, recommendation_citation: CITED_DIRECTLY }
source_location: { document: Hu2023_WholeGrains_AJCN.pdf, page: 153 }
```

**B — `SOURCE_DERIVED`, the harmonization case:**

```
evidence_id: WG01-EV-005
claim_id: WG-01a
record_type: QUANTITATIVE
source_id: SRC-DGA-APP-4.4
derived_from_source_id: SRC-REYNOLDS-2019
field: "type 2 diabetes, per-30g/day whole-grain dose-response"
study_classification: { study_design: cohort, synthesis_design: meta_analysis,
  exposure: "whole grain intake, per 30g/day increment (DGA's doubling of
  Reynolds' per-15g figure, WG01-EV-010)",
  outcome: type 2 diabetes incidence, effect_measure: RR }
numerical_provenance:
  estimate: "24% lower risk"
  CI: "NOT_REPORTED"
  raw_counts_pooled: { contributing_study_count: "NOT_REPORTED",
    combined_n_participants: "NOT_REPORTED", combined_n_events: "NOT_REPORTED",
    person_time: "NOT_REPORTED", follow_up_duration: "NOT_REPORTED" }
extraction_status: SOURCE_DERIVED
derivation_description: "The DGA appendix reports '24% lower risk' per
  30g/day. The DGA discloses that this comes from doubling Reynolds' own
  per-15g figure under a stated linearity assumption: (1 - 0.88) x 2 = 24%.
  This pipeline verified that disclosed arithmetic against Reynolds' own
  reported RR (WG01-EV-010) and confirmed it reproduces; the pipeline did
  not perform or originate a calculation of its own -- the 24% figure is
  the DGA's, not this pipeline's."
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
extraction_status: SOURCE_REPORTED
provenance_tier: T1
pipeline_stage: STAGE3_EXTRACTED
evidence_role: { role: MECHANISTIC }
source_location: { document: "Scientific Report Appendices_FINAL_1.28.26.md",
  page: 178 }
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
  exposure: high WG intake, comparator: low WG intake,
  outcome: colorectal cancer incidence, effect_measure: RR }
numerical_provenance:
  estimate: 0.87
  CI: [0.79, 0.96]
  raw_counts_pooled: { contributing_study_count: 7,
    combined_n_participants: "NOT_REPORTED", combined_n_events: "NOT_REPORTED",
    person_time: "6.8 million person-years",
    follow_up_duration: "9.5 years (average)" }
extraction_status: SOURCE_REPORTED
provenance_tier: T1
pipeline_stage: STAGE3_EXTRACTED
quality_signals: [{ signal_type: GRADE, value: "Moderate",
  attributed_to: "Reynolds 2019 appendix Table C:2", provenance_tier: T1,
  source_location: "Table C:2, p.49" }]
evidence_role: { role: DIFFERENCE_MAKING, recommendation_citation: CITED_DIRECTLY }
source_location: { document: Reynolds2019_SupplementaryAppendix.md,
  table_or_figure: "Table C:1", page: 35 }
```

**E — `raw_counts_by_group` shape, a meta-analysis of RCTs reporting
arm-level totals (the case that motivated revision 4):**

```
evidence_id: WG01-EV-018
claim_id: WG-01a
record_type: QUANTITATIVE
source_id: SRC-REYNOLDS-2019
field: "body weight, whole-grain-specific RCTs (CORRECTED -- true Table 2 /
  Figure 4B data; the record previously here was Table 3's glycaemic-index
  panel, mislabeled)"
study_classification: { study_design: RCT, synthesis_design: meta_analysis,
  exposure: "whole grain intake (RCT arm)", comparator: control,
  outcome: body weight, effect_measure: MD }
numerical_provenance:
  estimate: -0.62
  CI: [-1.19, -0.05]
  raw_counts_by_group: { contributing_study_count: 11, group_1: 498,
    group_2: 421, events_group_1: "NOT_REPORTED",
    events_group_2: "NOT_REPORTED", person_time: "NOT_REPORTED",
    follow_up_duration: "NOT_REPORTED" }
extraction_status: SOURCE_REPORTED
provenance_tier: T1
pipeline_stage: STAGE3_EXTRACTED
quality_signals: [{ signal_type: GRADE, value: "Moderate (paper states
  bodyweight/cholesterol/blood-pressure evidence in this table is
  \"downgraded to moderate because of unexplained heterogeneity\", p.441;
  no more granular per-endpoint GRADE label is given in the main text)",
  attributed_to: "Reynolds 2019, p.441", provenance_tier: T1,
  source_location: p.441 }]
evidence_role: { role: DIFFERENCE_MAKING, recommendation_citation: NOT_CITED }
source_location: { document: Reynolds2019_CarbQuality_Lancet.pdf,
  table_or_figure: "Table 2 (data table); Figure 4B is the companion forest
  plot on a separate page, p.442", page: 438 }
```

Note that `study_design: RCT` and `synthesis_design: meta_analysis` are
identical to example A's `study_design: cohort` /
`synthesis_design: meta_analysis` pattern in one respect — both are
pooled syntheses — yet example A uses `raw_counts_pooled` and this uses
`raw_counts_by_group`. That's the point: shape is a fact about how *this*
source table reports its counts, never about `study_design` or
`synthesis_design`.

A sixth pattern is worth naming even without a full worked example:
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
