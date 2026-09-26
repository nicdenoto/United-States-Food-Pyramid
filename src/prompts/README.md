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
| `evalue_calibration_v2.md` | E-value | Current | `EvalueApplication2` (in progress) | 2026-09-26 | Changes from v1: compute point and CI E-values for every estimate and shift; reproduce any derivation the source shows; final consistency check; state the conservatism point precisely; label claims not drawn from the source. |

E-value is the prototype. The GRADE, Bradford Hill and QBA prompts are written only
after the E-value calibration has been run all the way through.
