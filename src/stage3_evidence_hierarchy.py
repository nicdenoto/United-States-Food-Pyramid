"""Stage 3 -- Evidence hierarchy / chain of authority.

Reconstruct which evidence types a claim relies on -- clinical trial, mechanism,
meta-analysis, expert opinion, systematic review -- and to what severity, and
validate every EvidenceRecord against the data contract in
`src/schema/evidence-record.md` (frozen at revision 7).

The pipeline README describes Stage 3's mission ("an LLM reconstructs which
evidence types a claim relies on... and to what severity"); the schema doc is
the concrete answer to what this module should actually produce and check. See
`src/schema/evidence-record.md`'s own "What this is" note.

Prompt templates live in ./prompts and must be versioned for replicability --
unaffected by this module, which is pure validation/aggregation over corpus
markdown files already on disk, not an LLM call.

=== Scope of this validator (scoped 2026-09-16 against schema rev-5 and the
combined WG-01 working tree, before writing this file) ===

Machine-checkable from a single EvidenceRecord snapshot, and implemented below:
  - Section 1 top-level shape (required fields; record_type-conditional fields)
  - Rule 1  (SOURCE_DERIVED requires derived_from_source_id + derivation_description,
             and derived_from_source_id must resolve to a source_id seen in the batch)
  - Rule 2  (MODEL_DERIVED must never appear in a corpus/ file)
  - Rule 3  (QUALITATIVE records carry no numerical_provenance at all)
  - Rule 4  (source_location, with a 'document', is required regardless of
             extraction_status)
  - Rule 5  (provenance_tier / extraction_status enum validity -- the rule's
             "no disallowed combination" clause has nothing to check structurally)
  - Rule 6  (claim_id looks like a leaf sub-claim, not a bundle id -- heuristic:
             flags a claim_id with no trailing lowercase letter, e.g. "WG-01"
             instead of "WG-01a"; this is a naming-convention proxy, not a real
             claim-inventory lookup, since the validator has no other source of
             truth for which ids are bundles vs. leaves)
  - Rule 7  (recommendation_citation required when role is DIFFERENCE_MAKING or
             ALTERNATIVE_ESTIMATE and extraction_status is SOURCE_REPORTED or
             SOURCE_DERIVED -- rev-6 added this same NOT_REPORTED carve-out
             rule 10 already had, see ambiguity (2) below, now resolved)
  - Rule 10 (exactly one raw-count shape on SOURCE_REPORTED/SOURCE_DERIVED
             QUANTITATIVE records, none on NOT_REPORTED ones; contributing_study_count
             present iff synthesis_design != none)
  - Rule 11 (raw_counts_other requires structure_note)
  - Rule 12 (no analytical-instruction keys inside numerical_provenance)
  - Rule 13, partial (every EvidenceRecord's pipeline_stage is STAGE3_EXTRACTED;
             the rule's "never changed afterward" clause needs revision history,
             not a single snapshot, so isn't checked here)

NOT machine-checkable from corpus markdown alone, and deliberately not
implemented as a check (asserting a pass here would be a false rigor):
  - Rule 8  (AppraisalRecord referencing only real evidence_ids) -- applies to a
             different record type that doesn't exist in this corpus yet
             (Stage 4 has not yet appraised the corpus; framework calibration is in progress). Nothing to validate until analysis/ has
             AppraisalRecords.
  - Rule 9  (a raw count is never reconstructed from other reported values) --
             requires comparing against the primary PDF/table, which is exactly
             the kind of cross-check this project has always done by hand
             (see corpus/stage3_evidence_records/WG-01.md's reconciliation
             passes). This module has no access to source PDFs and does not
             attempt to fake that check.
  - Rule 5's independence clause and rule 13's immutability clause, as noted
    above.

Two real ambiguities this scoping pass surfaced in the schema doc itself (both
documented inline below, at the checks they affect, rather than silently
resolved or silently ignored):

  1. RESOLVED (rev-7, 2026-09-17): section 1's field tree listed
     `study_classification` with no "present only if..." qualifier (unlike
     `numerical_provenance` and `qualitative_content`, which both had one),
     even though all 4 QUALITATIVE records in WG-01 (and the schema's own
     worked example C, WG01-EV-009) have always omitted it entirely, across
     three independent reconciliation passes. This validator already enforced
     actual established practice -- required for QUANTITATIVE, absent for
     QUALITATIVE -- so no check below changes; the schema doc (rev-7) now
     states this explicitly in S1's tree, in the same "present only if /
     absent (not null) otherwise" phrasing already used for
     `numerical_provenance`. Full detail in `src/schema/evidence-record.md`'s
     revision-7 note.

  2. RESOLVED (rev-6, 2026-09-17): rule 7 originally required
     `recommendation_citation` unconditionally whenever role was
     DIFFERENCE_MAKING or ALTERNATIVE_ESTIMATE, with no carve-out for
     `extraction_status: NOT_REPORTED` -- unlike rule 10's. Running the first
     version of this validator against WG-01 found two real instances,
     WG01-EV-027/028 (the confirmed-absent gram-equivalent records): `role:
     DIFFERENCE_MAKING`, `extraction_status: NOT_REPORTED`, no
     `recommendation_citation`, because there was no reported value for the
     recommendation to have cited or not cited. The schema doc (rev-6) now
     carves this out explicitly, in the same shape as rule 10's carve-out;
     this module's rule-7 check below matches it. Full detail in
     `src/schema/evidence-record.md`'s revision-6 note and
     `corpus/stage3_evidence_records/WG-01.md` §9.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field as _dc_field
from pathlib import Path
from typing import Optional

import yaml

RECORD_FENCE_RE = re.compile(r"```\n(evidence_id:.*?)\n```", re.DOTALL)

VALID_RECORD_TYPES = {"QUANTITATIVE", "QUALITATIVE"}
VALID_EXTRACTION_STATUS = {"SOURCE_REPORTED", "SOURCE_DERIVED", "MODEL_DERIVED", "NOT_REPORTED"}
VALID_PROVENANCE_TIERS = {"T1", "T2", "STRUCTURE"}
VALID_ROLES = {"DIFFERENCE_MAKING", "MECHANISTIC", "QUALITY_CAVEAT", "ALTERNATIVE_ESTIMATE"}
VALID_RECOMMENDATION_CITATION = {"CITED_DIRECTLY", "CITED_INDIRECTLY", "NOT_CITED"}
ROLES_REQUIRING_CITATION = {"DIFFERENCE_MAKING", "ALTERNATIVE_ESTIMATE"}
RAW_COUNT_SHAPES = ("raw_counts_by_group", "raw_counts_pooled", "raw_counts_other")
ALLOWED_NUMERICAL_PROVENANCE_KEYS = {"estimate", "CI"} | set(RAW_COUNT_SHAPES)


@dataclass
class Finding:
    evidence_id: str
    rule: str
    severity: str  # "error" | "note"
    message: str

    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.evidence_id} ({self.rule}): {self.message}"


@dataclass
class EvidenceHierarchy:
    records: list
    by_claim: dict
    findings: list = _dc_field(default_factory=list)

    @property
    def errors(self) -> list:
        return [f for f in self.findings if f.severity == "error"]

    @property
    def notes(self) -> list:
        return [f for f in self.findings if f.severity == "note"]

    def summary(self) -> str:
        lines = [
            f"{len(self.records)} records, {len(self.by_claim)} claim(s), "
            f"{len(self.errors)} error(s), {len(self.notes)} note(s)",
        ]
        for claim_id in sorted(self.by_claim):
            entries = self.by_claim[claim_id]
            lines.append(f"\n{claim_id} ({len(entries)} record(s)):")
            for e in entries:
                rc = f" -- {e['recommendation_citation']}" if e["recommendation_citation"] else ""
                lines.append(
                    f"  {e['evidence_id']} [{e['extraction_status']}, {e['provenance_tier']}] "
                    f"{e['role']}{rc}: {e['field']}"
                )
        if self.findings:
            lines.append("\nFindings:")
            for f in self.findings:
                lines.append(f"  {f}")
        return "\n".join(lines)


def parse_records(path) -> list:
    """Extract every fenced EvidenceRecord block from a corpus markdown file and
    parse it as YAML.

    A block is recognized by starting with `evidence_id:` -- this deliberately
    filters out any other fenced content that might share a file with evidence
    records (schema docs mix diagrams and examples into the same file; this
    parser is only ever pointed at corpus files, but the filter costs nothing
    and makes that safe).

    A block that starts with `evidence_id:` but fails to parse, or parses to
    something other than a mapping, is a data error worth stopping on -- not
    something to skip silently, which would hide a malformed record instead of
    reporting it.
    """
    text = Path(path).read_text(encoding="utf-8")
    blocks = RECORD_FENCE_RE.findall(text)
    records = []
    for block in blocks:
        try:
            parsed = yaml.safe_load(block)
        except yaml.YAMLError as exc:
            raise ValueError(
                f"Malformed EvidenceRecord block in {path}: {exc}\n---\n{block[:200]}"
            ) from exc
        if not isinstance(parsed, dict):
            raise ValueError(
                f"EvidenceRecord block in {path} did not parse to a mapping "
                f"(got {type(parsed).__name__}): {block[:200]}"
            )
        records.append(parsed)
    return records


def _present(record: dict, key: str) -> bool:
    return key in record and record[key] not in (None, "")


def validate_record(record: dict, known_source_ids: Optional[set] = None) -> list:
    """Validate a single parsed EvidenceRecord against schema rev-7. Returns a
    list of Findings; an empty list means no issues at any severity."""
    eid = record.get("evidence_id", "<missing evidence_id>")
    findings: list = []

    def flag(rule: str, message: str, severity: str = "error") -> None:
        findings.append(Finding(eid, rule, severity, message))

    # --- Section 1: always-required top-level fields ---
    for key in (
        "evidence_id", "claim_id", "record_type", "source_id", "field",
        "source_location", "extraction_status", "provenance_tier",
        "pipeline_stage", "evidence_role",
    ):
        if not _present(record, key):
            flag("shape", f"missing required top-level field '{key}'")

    record_type = record.get("record_type")
    if record_type not in VALID_RECORD_TYPES:
        flag("shape", f"record_type '{record_type}' not one of {sorted(VALID_RECORD_TYPES)}")

    # study_classification: required for QUANTITATIVE, absent for QUALITATIVE.
    # See module docstring, ambiguity (1) -- RESOLVED (rev-7): S1's tree now
    # marks this conditional explicitly, matching established practice across
    # all 28 WG-01 records and the schema's own worked example C.
    has_study_classification = "study_classification" in record
    if record_type == "QUANTITATIVE" and not has_study_classification:
        flag("shape", "QUANTITATIVE record missing study_classification")
    if record_type == "QUALITATIVE" and has_study_classification:
        flag(
            "shape",
            "QUALITATIVE record carries study_classification -- established "
            "practice (all 4 WG-01 QUALITATIVE records, schema section 12 example C) "
            "omits this entirely for QUALITATIVE records; section 1's field tree "
            "(rev-7) now marks it conditional the same way it does "
            "numerical_provenance/qualitative_content",
            severity="note",
        )

    # numerical_provenance / qualitative_content: record_type-exclusive (S1, rule 3)
    has_np = "numerical_provenance" in record
    has_qc = "qualitative_content" in record
    if record_type == "QUANTITATIVE":
        if not has_np:
            flag("shape", "QUANTITATIVE record missing numerical_provenance")
        if has_qc:
            flag("shape", "QUANTITATIVE record carries qualitative_content")
    if record_type == "QUALITATIVE":
        if has_np:
            flag("rule-3", "QUALITATIVE record carries numerical_provenance "
                            "(must be entirely absent, not present-with-nulls)")
        if not has_qc:
            flag("shape", "QUALITATIVE record missing qualitative_content")

    # --- section 2 / rules 1-2: extraction_status ---
    status = record.get("extraction_status")
    if status not in VALID_EXTRACTION_STATUS:
        flag("shape", f"extraction_status '{status}' not one of {sorted(VALID_EXTRACTION_STATUS)}")

    if status == "MODEL_DERIVED":
        flag("rule-2", "MODEL_DERIVED record present in a corpus/ file -- "
                        "belongs under analysis/ as an AppraisalRecord or Stage-5 output")

    if status == "SOURCE_DERIVED":
        dfs = record.get("derived_from_source_id")
        dd = record.get("derivation_description")
        if not dfs:
            flag("rule-1", "SOURCE_DERIVED without derived_from_source_id")
        elif known_source_ids is not None and dfs not in known_source_ids:
            flag("rule-1", f"derived_from_source_id '{dfs}' does not resolve to "
                            f"any source_id seen in this batch")
        if not dd:
            flag("rule-1", "SOURCE_DERIVED without derivation_description")

    # --- rule 4: source_location required regardless of extraction_status ---
    source_location = record.get("source_location")
    if not isinstance(source_location, dict) or not source_location.get("document"):
        flag("rule-4", "source_location missing, or missing its required 'document'")

    # --- rule 5: enum validity (the "independently set" clause has nothing
    # structural to check -- every combination is legal by definition) ---
    tier = record.get("provenance_tier")
    if tier not in VALID_PROVENANCE_TIERS:
        flag("shape", f"provenance_tier '{tier}' not one of {sorted(VALID_PROVENANCE_TIERS)}")

    # --- rule 6: claim_id should be a leaf sub-claim, never a bundle id.
    # Heuristic only: flags an id with no trailing lowercase letter (e.g.
    # "WG-01" instead of "WG-01a"). This is a naming-convention proxy, not a
    # real claim-inventory lookup.
    claim_id = record.get("claim_id")
    if claim_id and not re.match(r"^.+[a-z]$", str(claim_id)):
        flag("rule-6", f"claim_id '{claim_id}' doesn't look like a leaf sub-claim "
                        f"(expected a trailing letter, e.g. 'WG-01a', not a bundle id)")

    # --- rule 7: recommendation_citation required for these two roles ---
    evidence_role = record.get("evidence_role") or {}
    role = evidence_role.get("role")
    if role not in VALID_ROLES:
        flag("shape", f"evidence_role.role '{role}' not one of {sorted(VALID_ROLES)}")
    needs_citation = role in ROLES_REQUIRING_CITATION and status in ("SOURCE_REPORTED", "SOURCE_DERIVED")
    has_citation = "recommendation_citation" in evidence_role
    if needs_citation and not has_citation:
        flag("rule-7", f"role={role} requires evidence_role.recommendation_citation "
                        f"(rule 7; extraction_status={status} is SOURCE_REPORTED/SOURCE_DERIVED, "
                        f"so the rev-6 NOT_REPORTED carve-out does not apply here)")
    if has_citation and evidence_role["recommendation_citation"] not in VALID_RECOMMENDATION_CITATION:
        flag("shape", f"recommendation_citation "
                       f"'{evidence_role['recommendation_citation']}' not one of "
                       f"{sorted(VALID_RECOMMENDATION_CITATION)}")
    if not needs_citation and has_citation:
        flag("shape", f"role={role} carries recommendation_citation, not required "
                       f"or expected for this role", severity="note")

    # --- rules 10, 11: raw-count shape (rule 9 is not checked -- see docstring) ---
    numerical_provenance = record.get("numerical_provenance")
    if record_type == "QUANTITATIVE" and isinstance(numerical_provenance, dict):
        present_shapes = [s for s in RAW_COUNT_SHAPES if s in numerical_provenance]

        if status in ("SOURCE_REPORTED", "SOURCE_DERIVED"):
            if not present_shapes:
                flag("rule-10", "SOURCE_REPORTED/SOURCE_DERIVED record has no raw-count "
                                 "object (exactly one of raw_counts_by_group/"
                                 "raw_counts_pooled/raw_counts_other is required)")
            elif len(present_shapes) > 1:
                flag("rule-10", f"more than one raw-count object present: {present_shapes}")
        elif status == "NOT_REPORTED" and present_shapes:
            flag("rule-10", f"NOT_REPORTED record carries a raw-count object "
                             f"({present_shapes}) -- should carry none, since there is "
                             f"no estimate for a count to attach to")

        synthesis_design = (record.get("study_classification") or {}).get("synthesis_design")
        for shape in present_shapes:
            obj = numerical_provenance[shape]
            if not isinstance(obj, dict):
                flag("shape", f"{shape} is not a mapping")
                continue
            has_csc = "contributing_study_count" in obj
            if synthesis_design and synthesis_design != "none" and not has_csc:
                flag("rule-10", f"{shape} missing contributing_study_count although "
                                 f"synthesis_design={synthesis_design}")
            if synthesis_design == "none" and has_csc:
                flag("rule-10", f"{shape} carries contributing_study_count although "
                                 f"synthesis_design=none (should be absent entirely, "
                                 f"not populated as any value)")
            if shape == "raw_counts_other" and not obj.get("structure_note"):
                flag("rule-11", "raw_counts_other missing required structure_note")

        # Rule 9 (no reconstructed raw counts) needs the primary source to check
        # against and is not evaluated here -- see module docstring.

        # NOT_REPORTED QUANTITATIVE records state no value, so estimate must be
        # the literal "NOT_REPORTED" (S11 rule 10). A missing numerical_provenance
        # is already reported by the S1 shape check above, so only check here
        # when the block exists.
        if status == "NOT_REPORTED":
            estimate = numerical_provenance.get("estimate")
            if estimate != "NOT_REPORTED":
                flag("shape", f"NOT_REPORTED record's numerical_provenance.estimate is "
                               f"'{estimate}', expected the literal string 'NOT_REPORTED'")

    # --- rule 12: no analytical-instruction keys in numerical_provenance ---
    if isinstance(numerical_provenance, dict):
        extra = set(numerical_provenance.keys()) - ALLOWED_NUMERICAL_PROVENANCE_KEYS
        if extra:
            flag("rule-12", f"numerical_provenance carries unexpected key(s) "
                             f"{sorted(extra)} -- possible analytical instruction, which "
                             f"never belongs here")

    # --- rule 13 (partial): every EvidenceRecord is STAGE3_EXTRACTED.
    # The "never changed afterward" clause needs revision history, not a
    # single snapshot, and isn't checked here.
    stage = record.get("pipeline_stage")
    if stage != "STAGE3_EXTRACTED":
        flag("shape", f"pipeline_stage '{stage}' -- every EvidenceRecord should be "
                       f"STAGE3_EXTRACTED (section 5)")

    return findings


def build_evidence_hierarchy(*paths: str) -> EvidenceHierarchy:
    """Parse one or more corpus markdown files of EvidenceRecords, validate every
    record against the Stage 3 schema (src/schema/evidence-record.md, rev-7),
    and group the result by claim_id -- the claim-level view the schema doc
    itself motivates in section 7:

        DGA claim
           |-- Evidence A -- CITED_DIRECTLY
           |-- Evidence B -- CITED_INDIRECTLY
           `-- Evidence C -- NOT_CITED (alternative)

    Raises ValueError if any file contains a block that looks like an
    EvidenceRecord (starts with `evidence_id:`) but fails to parse as YAML or
    doesn't parse to a mapping -- a malformed record is reported immediately,
    not silently dropped. Structural/rule violations in an otherwise
    well-formed record do NOT raise; they're collected in the returned
    EvidenceHierarchy.findings so a single bad record doesn't block seeing
    every other issue in the same run.
    """
    if not paths:
        raise TypeError("build_evidence_hierarchy() requires at least one corpus file path")

    all_records: list = []
    for path in paths:
        all_records.extend(parse_records(path))

    known_source_ids = {r["source_id"] for r in all_records if r.get("source_id")}

    findings: list = []
    for record in all_records:
        findings.extend(validate_record(record, known_source_ids))

    by_claim: dict = {}
    for record in all_records:
        claim_id = record.get("claim_id", "<missing claim_id>")
        evidence_role = record.get("evidence_role") or {}
        by_claim.setdefault(claim_id, []).append({
            "evidence_id": record.get("evidence_id"),
            "field": record.get("field"),
            "role": evidence_role.get("role"),
            "recommendation_citation": evidence_role.get("recommendation_citation"),
            "extraction_status": record.get("extraction_status"),
            "provenance_tier": record.get("provenance_tier"),
        })

    return EvidenceHierarchy(records=all_records, by_claim=by_claim, findings=findings)


if __name__ == "__main__":
    import sys

    targets = sys.argv[1:] or ["corpus/stage3_evidence_records/WG-01.md"]
    hierarchy = build_evidence_hierarchy(*targets)
    print(hierarchy.summary())
    sys.exit(1 if hierarchy.errors else 0)
