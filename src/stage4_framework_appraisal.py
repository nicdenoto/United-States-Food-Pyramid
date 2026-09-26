"""Stage 4 — Framework appraisal.

Evaluate sub-references for their contribution to the primary references using
the four calibrated frameworks: GRADE, Bradford Hill, E-value, and QBA.

CALIBRATION: the evaluation LLM is anchored on gold-standard worked examples of
each framework before its judgments on the live corpus are trusted. See the LLM
calibration subsection in paper/02-methodology.md. Prompts are versioned in
src/prompts/ (E-value prototype in progress).

TODO: drop in the working implementation from the local environment.
"""


def appraise(*args, **kwargs):
    raise NotImplementedError("Stage 4 stub — add implementation.")
