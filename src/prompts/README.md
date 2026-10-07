# Prompts

Calibration and live-analysis prompt templates for the evaluation LLM.

Keep the calibration prompt(s) and the live-analysis prompt(s) as separate,
versioned files here. They form part of the replicability record alongside the
gold-standard calibration set and the model identifier/version.

Do not hardcode prompts inside the stage modules — reference them from here so a
single template change is tracked in one place.

## Conventions

- **One file per version.** Each file holds exactly the text pasted into the
  `<Framework>Application<N>` Project's instructions field, and nothing else. No
  header or commentary goes inside the file, so it can be copied as-is.
- **Released versions are never edited.** A revision is a new file with the next
  version number. The reason for each revision goes in the table below.
- **Naming:** `<framework>_calibration_v<N>.md` for calibration prompts, and
  `<framework>_analysis_v<N>.md` for the live-analysis prompt that a `Frozen`
  framework runs against the corpus. Frameworks: `evalue`, `grade`,
  `bradfordhill`, `qba`.
- **All future prompts go here**, for every framework, as they are approved.

## Version log

Model for every run: Claude Sonnet 5, Medium reasoning effort, in a hand-configured
isolated account. Web search, past-chat reference, memory and network egress are
off; code execution is on. The model sees only the prompt and one attached source
per chat.

| File | Framework | Status | Used in | Approved | Notes |
|---|---|---|---|---|---|
| `evalue_calibration_v1.md` | E-value | Superseded | `EvalueApplication1` (2026-09-25/26) | 2026-09-24 | Did not pass Gate 1: 5 / 1 / 2 Partials across Chats A–C, 0 Mismatches, 0 numeric errors. |
| `evalue_calibration_v2.md` | E-value | Superseded | `EvalueApplication2` (2026-09-26) | 2026-09-26 | Changes from v1: compute point and CI E-values for every estimate and shift; reproduce any derivation the source shows; final consistency check; state the conservatism point precisely; label claims not drawn from the source. Did not pass Gate 1: 2 / 1 / 1 Partials across Chats A–C, 0 Mismatches, 0 numeric errors. |
| `evalue_calibration_v3.md` | E-value | Superseded | `EvalueApplication3` (2026-09-27/28) | 2026-09-26 | No rules removed. The closing consistency check becomes a four-item checklist: point and CI E-values for every estimate and shift, including CI = 1; tables match the body; every quotation checked word for word, as one passage, on the cited page; no "the source says" before the model's own judgment. Also adds a page-citation rule, and says to write the filled-in Step 4 template without quotation marks. Did not pass Gate 1: Chat A 1 Mismatch (leukemia → 0.90 CI E-value called "not derivable"), Chat B 1 Partial (D5, adjustment depth reversed), Chat C clean. |
| `evalue_calibration_v4.md` | E-value | Superseded | `EvalueApplication4` (2026-09-28) | 2026-09-28 | No rules removed. Step 3 now makes the model check, for every estimate and shift, whether the null or target lies within the confidence limits: if it does, report 1 ("always determinable, never 'not derivable'"); otherwise use the limit closest to the null or target. Step 5 adds the adjustment-depth rule: thinner adjustment makes the same E-value less reassuring. Did not pass Gate 1: Chat A 2 Partials, Chat B 1, Chat C 1. Last prompt of Phase 1 (model alone). |
| `evalue_calibration_v5.md` | E-value | Superseded | `EvalueApplication5` (Phase 2, 2026-09-28) | 2026-09-28 | First Phase 2 prompt. The model fills a JSON input table and runs the embedded calculator (`src/stage4/evalue_calc.py`) with its code tool; the operator then runs the validator and quote verifier. Carries forward v5's attribution and page-citation rules (the standalone prompt-only v5 draft was folded in, not run). Cannot pass Gate 1: Chat A run 1 (the Lock-in run) had 1 Partial (D1), two shift rows entered without the confidence limits the source reports, so the calculator could not return their CI E-value of 1. Its remaining runs are kept as reliability data. |
| `evalue_calibration_v6.md` | E-value | Superseded before use | — (never run) | 2026-09-28 | Structural fix for the one defect that repeated in all five Chat A runs. Each estimate is entered once, with its confidence limits, and every shift goes in that entry's `targets` list (`rd_targets` for a risk difference), so a shift can no longer be entered without its interval. The prompt and the calculator's printout both state that a CI E-value of 1 is a result, not an artifact. The Step 3 wording, Part A field list and checklist item (a) change to match; no other rules change. Superseded before any run by v7: its duplicate-estimate warning would have told the model to merge two different studies that share a point estimate (VanderWeele, Ding & Mathur 2019, Section 3: RR 1.18 with different CIs), found while scoring Application5 Chat C run 1. |
| `evalue_calibration_v7.md` | E-value | Superseded | `EvalueApplication6` (2026-10-04 to 10-07) | 2026-10-05 | v6 with one change to the embedded calculator: the duplicate-estimate warning now fires only when two entries share the measure and point estimate and either report the same limits or one has no limits, so different studies with the same point estimate are not flagged. The prompt text is otherwise identical to v6. Did not pass Gate 1: each Lock-in run (Chats A, B, C) failed on one borderline evidence-path item. Across all nine runs: 6 Partials, 0 Mismatches, 3 clean runs. Its target was fixed (the CI E-value of 1 for a target inside the interval was reported in 9 of 9 runs; D1 9/9 against v5's 7/9); location-citation errors were the only repeated failure (5 of 9 runs). |
| `evalue_calibration_v8.md` | E-value | Proposed | `EvalueApplication7` | — | Targets the one repeated failure class under v7, location citations (a paraphrase placed in a table; a page given for a whole example; a section number inferred from a page number), plus one related attribution (an appendix said to confirm a formula it doesn't). The model builds and shows a section map before Part B and takes every section number from it; a location may be given only for a word-for-word quotation or a paraphrase followed by one; a page belongs only to the quotation it is attached to; no section is said to show or confirm something it can't be quoted for; new checklist item (e). Also a format fix: the evalue-table block holds only the JSON array, with the run lines kept out of it. Calculator unchanged. |

Unified diffs between consecutive versions are in `diffs/` (see `diffs/README.md`).

E-value is the prototype. The GRADE, Bradford Hill and QBA prompts are written only
after the E-value calibration has been run all the way through.
