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
| `evalue_calibration_v4.md` | E-value | Current | `EvalueApplication4` (in progress) | 2026-09-28 | No rules removed. Step 3 now makes the model check, for every estimate and shift, whether the null or target lies within the confidence limits: if it does, report 1 ("always determinable, never 'not derivable'"); otherwise use the limit closest to the null or target. Step 5 adds the adjustment-depth rule: thinner adjustment makes the same E-value less reassuring. |

E-value is the prototype. The GRADE, Bradford Hill and QBA prompts are written only
after the E-value calibration has been run all the way through.
