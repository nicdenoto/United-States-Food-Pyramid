"""Stage 3 — Evidence hierarchy / chain of authority.

Reconstruct (via a custom LLM prompt) which evidence types a claim relies on
-- clinical trial, mechanism, meta-analysis, expert opinion, systematic review --
and to what severity.

Prompt templates live in ./prompts and must be versioned for replicability.

TODO: drop in the working implementation from the local environment.
"""


def build_evidence_hierarchy(*args, **kwargs):
    raise NotImplementedError("Stage 3 stub — add implementation.")
