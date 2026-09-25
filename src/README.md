# Pipeline

The audit runs as six stages. Stages 1, 2, 4, 5 and 6 are **structured stubs**; Stage 3
is a working validator for the EvidenceRecord schema (`schema/evidence-record.md`,
§1–§11 frozen at revision 7). Each stub marks
the boundary and responsibility of a stage so the working code can be dropped in
without losing the stage separation or the provenance control that runs across all
of them. One stage (stage 5) is still methodologically open (noted below) and
should not be treated as settled.

For the authoritative description, see `paper/02-methodology.md`.

## Stages

1. **`stage1_organization_and_claim_selection.py` — Organization and claim
   selection.** Bodies are selected against four criteria: public/accessible
   reasoning; widespread and severe impact; documentable, organized references
   (DOIs, PMIDs, PDFs, downloadable tables); and firm, confident recommendations.
   *Claim identification stays a human responsibility and is not delegated to a
   model.* For this project, stages 1–2 are fixed to the DGA corpus rather than run
   against an open set of organizations.

2. **`stage2_reference_acquirer.py` — Reference and sub-reference collection.**
   Collects the references supporting each claim, and their references
   ("sub-references"), storing them as Markdown in an organized corpus.
   Collection runs on a custom script and LLM assistance in combination
   (resolved 2026-09-17).

3. **`stage3_evidence_hierarchy.py` — Evidence hierarchy / chain of authority.**
   The stage's mission is to reconstruct which evidence types a claim relies on
   (clinical trial, mechanism, meta-analysis, expert opinion, systematic review)
   and to what severity. The module itself is not an LLM call: it parses the
   EvidenceRecords in `corpus/stage3_evidence_records/`, validates each against
   `schema/evidence-record.md`, and groups them by claim.

4. **`stage4_framework_appraisal.py` — Framework appraisal.** Sub-references are
   evaluated for their contribution to the primary references using GRADE,
   Cochrane, STROBE, Bradford Hill, E-value, and QBA. The LLM is anchored on
   gold-standard worked examples of each framework before its judgments on the live
   corpus are trusted (see "LLM calibration" in the Methodology).

5. **`stage5_statistical_evaluation.py` — Statistical evaluation.** A statistical
   system applied across the stored references/sub-references. **Fully open:** its
   exact form is undetermined, as is how it should integrate with the qualitative
   appraisals from stage 4 rather than sit beside them disconnected.

6. **`stage6_gap_identification.py` — Gap identification and constructive
   challenge.** Where certainty outruns evidence — typically a claim resting
   entirely on difference-making evidence with a thin mechanistic leg — the gap is
   filled with existing mechanistic/anthropological evidence chosen to run against
   the claim, mirroring the beta-carotene precedent.

## Cross-cutting control: provenance tiers

Every claim the pipeline emits is tagged **[T1] primary-verified**,
**[T2] secondary-sourced**, or **[STRUCTURE] structure-inferred** (see the root
README). Two additional provenance *signals* are recorded across the corpus:
author–evidence overlap (an author rating the certainty of their own study) and
disclosed financial ties that co-vary with a recommendation's direction.

## Prompts

Calibration and live-analysis prompt templates belong in `prompts/`. They are part
of what must be versioned for replicability (alongside the calibration set and the
model identifier/version).
