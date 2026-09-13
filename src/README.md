# Pipeline

The audit runs as six stages. The files here are **structured stubs**: each marks
the boundary and responsibility of a stage so the working code can be dropped in
without losing the stage separation or the provenance control that runs across all
of them. Two stages are still methodologically open (noted below) and should not
be treated as settled.

For the authoritative description, see `docs/agent-context-pack.md` §3 and
`paper/02-methodology.md`.

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
   **Open:** whether collection is code-only, LLM-assisted, or both is undetermined.

3. **`stage3_evidence_hierarchy.py` — Evidence hierarchy / chain of authority.**
   An LLM (custom prompt) reconstructs which evidence types a claim relies on
   (clinical trial, mechanism, meta-analysis, expert opinion, systematic review)
   and to what severity.

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
