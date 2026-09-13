# DGA Causal-Claims Audit

A semi-automated pipeline for auditing the causal claims made in public-health
nutrition guidance, applied to *The Scientific Foundation for the Dietary
Guidelines for Americans, 2025–2030* and its appendices.

**Core research question.** Does the certainty a guidance document *asserts* for a
causal claim match the *evidence structure* that actually supports it? The project
is not an attempt to decide whether a recommendation is correct; it asks whether
the confidence placed behind it is earned by the evidence on record.

**Constructive aim.** Where certainty outruns support, the audit does not stop at
naming the gap. For each such claim it supplies a concrete piece of *existing*
contrary evidence — mechanistic or anthropological — that runs against the claim
as stated. The goal is to supplement with evidence the guidance omitted, not to
propose new studies.

Research position held at SUNY Poly, supervised by Dr. Schneider and Dr. Abeya.
Target: submission-ready paper by **October 1, 2026**.

---

## Evaluative framework

The backbone is the **Russo–Williamson Thesis (RWT)**: a causal claim is
established only when it carries both a **difference-making** leg (RCTs, cohort
studies, clinical observation — does the outcome vary with the cause) *and* a
**mechanistic** leg (a plausible, evidenced physiological pathway). Each case
analysis checks the two legs separately, because a claim can be well-supported on
one and thin on the other, and neither leg alone establishes causation.

RWT sits alongside a supporting appraisal apparatus — GRADE, the Bradford Hill
criteria, the Cochrane risk-of-bias tools (RoB 2, ROBINS-I), STROBE, the E-value,
and quantitative bias analysis (QBA), with ROBIS / AMSTAR-2 / CONSORT used where
design-specific evaluation is warranted. See `paper/02-methodology.md` and
`docs/agent-context-pack.md` §2–3 for the full treatment.

## Provenance-tier discipline (non-negotiable)

Every factual claim in this project is tagged by how it is known. The tiers are
never conflated — conflating them is treated as a methodological error, not a
style issue:

- **[T1] primary-verified** — checked directly against a primary document
  (the DGA report, an appendix, an original trial report).
- **[T2] secondary-sourced** — obtained via search or a secondary/AI-research
  pass; must be verified against the primary source before final citation.
- **[STRUCTURE] structure-inferred** — inferred from the shape of the document
  or evidence base rather than stated outright.

Any new prose written into this repo is expected to carry the same tags.

## The two-layer audit

The DGA corpus is read as two layers, and a claim can fail at either
independently:

- **Front-end** — the main report / Scientific Foundation: the GRADE-labeled
  claims a policymaker actually reads.
- **Back-end** — the appendices: the systematic and umbrella reviews, evidence
  tables, and ROBIS/GRADE assessments that are supposed to support those claims.

---

## Repository layout

```
.
├── README.md                     ← you are here
├── STATUS.md                     ← current state + open decisions (mirrors the task ledger)
├── paper/                        ← the manuscript
│   ├── 01-introduction-and-background.md
│   ├── 02-methodology.md         (RWT-as-operationalizing-lens; LLM calibration)
│   ├── 03-theoretical-framework.md   (placeholder — reconciliation still to do)
│   ├── outline-and-timeline.md
│   └── sources/
│       └── methodology-proposal-gpt-archive.md   (recovered supervisor proposal)
├── docs/                         ← project briefing / onboarding
│   ├── agent-context-pack.md     (full standalone briefing — read first)
│   ├── handoff-current-state.md
│   └── task-ledger-snapshot.md   (static export of the live ledger)
├── src/                          ← the six-stage pipeline (code stubs — see src/README.md)
│   ├── README.md
│   ├── stage1_organization_and_claim_selection.py
│   ├── stage2_reference_acquirer.py
│   ├── stage3_evidence_hierarchy.py
│   ├── stage4_framework_appraisal.py
│   ├── stage5_statistical_evaluation.py   (form undetermined — open)
│   ├── stage6_gap_identification.py
│   ├── prompts/                  (calibration + live-analysis prompt templates)
│   └── requirements.txt
├── corpus/
│   ├── dga/appendices.md         (DGA appendices — US federal work, public domain)
│   ├── claim-inventory.md        (placeholder — to be rebuilt from the appendices)
│   └── reference-library/        (methodology PDFs — gitignored; see its README)
└── notes/                        ← raw working notes the drafts were built from
```

## A note on the code

The pipeline scripts under `src/` are **structured stubs**, not the working
implementation. The live code lives in the local development environment; drop it
into the matching stage files, keeping the six-stage boundaries and the provenance
control intact. `src/README.md` describes what each stage is responsible for and
which stages are still methodologically open (stage 2 collection mode; stage 5
statistical evaluation).

## A note on the corpus

The **DGA appendices** (`corpus/dga/appendices.md`) are a work of the U.S. federal
government and are in the public domain, so they are tracked here. The
**methodology reference PDFs** under `corpus/reference-library/` are copyrighted
published papers; they are present locally for convenience but are **gitignored**
and are *not* committed. `corpus/reference-library/README.md` is a citation
manifest that records each one and where to obtain it. If you make this repository
private and want the PDFs tracked, remove the matching line from `.gitignore`.

## Where to start

New here? Read `docs/agent-context-pack.md` first — it is the complete standalone
briefing (scope, framework, pipeline, findings so far, open questions). Then
`STATUS.md` for what is and isn't done.
