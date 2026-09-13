# Prompts

Calibration and live-analysis prompt templates for the evaluation LLM.

Keep the calibration prompt(s) and the live-analysis prompt(s) as separate,
versioned files here. They form part of the replicability record alongside the
gold-standard calibration set and the model identifier/version.

Do not hardcode prompts inside the stage modules — reference them from here so a
single template change is tracked in one place.
