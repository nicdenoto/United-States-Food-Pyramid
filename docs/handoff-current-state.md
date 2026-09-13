# Handoff — Current State (as of Sept 13, 2026)

*Read this first in a new chat. This project is the DGA causal-claims audit paper, due Oct 1, 2026. Everything below is current as of this write.*

## What exists right now

**Live task ledger** (interactive, checkable): https://claude.ai/code/artifact/711b20f9-6c71-42ec-8d52-c1f7a8ebabd2
19 tasks across 3 weeks, each with checkable subtasks, stored in the artifact's own database. This is the source of truth for what's done — check it before assuming status from any static doc.

**Drafted paper sections** (all saved as project docs, all current):
- `claude/Draft - Introduction and Background.md`
- `claude/Draft - Methodology.md` — includes "RWT as the operationalizing lens" and "LLM calibration: justification/parameters/replicability"
- `claude/Paper Master Outline and Oct 1 Timeline.md`
- `claude/Source - Methodology Proposal (from GPT archive).md` — recovered appraisal-apparatus source, not yet reconciled into a polished theoretical-framework doc
- `claude/Agent Context Pack.md` — full standalone briefing for any agent (Claude or GPT) picking this up cold; the most complete single summary of scope, framework, pipeline, findings-so-far, and open questions

**Just delivered to Nic**: a zip (`GPT-Handoff-Package.zip`) containing the Agent Context Pack, the three drafts, and a static task-ledger snapshot — everything GPT's side doesn't already have from `Archive.zip`.

## Open items blocking progress (see Agent Context Pack §9 for full detail)
1. Claim inventory — still not located or rebuilt (ledger task t3)
2. LLM calibration Parameters/Replicability numbers — needs Nic's input (t4d, t4e)
3. Scope decision on HRT/beta-carotene/vitamin E — full case studies vs. short precedent paragraphs (t9, blocked)
4. Statistical-evaluation pipeline stage — form entirely undetermined
5. Why corpus narrowed to DGA beyond the 4 selection criteria; script vs. LLM for reference collection (t5)
6. Submission format/venue — not stated anywhere yet

## Biggest remaining lift
Writing the whole grains, vegetables, and saturated fat case analyses in full cited academic prose (t6–t8) — analysis is substantively done, prose is not written. This is Week 2's work and the rate-limiting step to Oct 1.

## Working notes for whoever picks this up
- Keep in-chat responses concise — Nic has asked for this explicitly.
- Provenance-tier discipline is non-negotiable: every claim tagged primary-verified [T1], secondary-sourced [T2], or structure-inferred [STRUCTURE]. Never conflate tiers.
- Match the existing academic voice (see Agent Context Pack §6) when drafting new prose.
- RWT (Russo-Williamson Thesis) is the operationalizing lens for every case analysis: check the difference-making leg and the mechanistic leg separately.
